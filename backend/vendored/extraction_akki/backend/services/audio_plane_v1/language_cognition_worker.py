"""Language-cognition worker — runs ONLY on the admitted GPU host (akki-vm-ii).

Shipped as reviewed code by the control plane; credentials arrive on stdin inside
the pinned SSH channel and never touch disk. Phases (CP-AIP-LANGUAGE-COGNITION):
  corpus_census    — list + stage `google-transcripts/datasets/<code>/<session>/{audio,transcript,metadata}`
                     on the host volume, unpack archive-only sessions, and read the corpus AS A DATABASE
                     (AIP §1.1: every file is an estate, segments are rows) into `corpus_db/*.jsonl`.
  register_bases   — pull the two Doc-20 bases (Whisper encoder · VoxLingua107 ECAPA), pin weight sha256.
  speaker_linkage  — link session-local speaker ids into presenters with a speaker-verification
                     embedding (biometric, AIP §6.2: embeddings destroyed after cluster assignment;
                     only opaque cluster ids persist). Makes the split presenter-disjoint (MUST-DO §3).
  gate_eval        — pre-trained overlay agreement (Whisper-LID + VoxLingua107) against folder labels.
  train_baseline   — LoRA over the Whisper encoder fused with frozen VoxLingua107 embeddings, 2 s
                     windows inside transcribed speech, presenter-disjoint held-out split, archive-only
                     sessions as a second test set, deterministic span rule, no-speaker-ID probe
                     (MUST-DO §4). A MEASURED compute receipt — NOT the final model (MUST-NOT §1).
Every measurement is a fact read on this host; nothing is asserted.
"""
import hashlib
import json
import os
import random
import re
import shutil
import socket
import subprocess
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

LANGUAGES = {"kik": "Kikuyu", "ebu": "Embu", "swa": "Kiswahili", "luo": "Luo", "kln": "Kalenjin", "guz": "Kisii",
             "mer": "Meru", "bxk": "Bukusu", "kam": "Akamba", "mrg": "Maragoli", "lwg": "Luhya", "mas": "Maasai"}
TARGET_FIVE = ("Kikuyu", "Luo", "Sheng", "Swahili", "English")
AUDIO_EXT = {".wav", ".mp3", ".flac", ".m4a", ".ogg", ".opus", ".aac", ".wma"}
WHISPER_ISO = {"swa": "sw", "eng": "en"}                  # Whisper's 99-language set covers only Swahili here
VOX_ISO = {"swa": "sw", "eng": "en"}                      # VoxLingua107 set likewise
WINDOW_SECONDS = 2.0
SAMPLE_RATE = 16000
MIN_SPAN_SECONDS = 0.5      # mirrors sealed WINDOW_AND_SPAN_RULE_DEFAULT (worker ships standalone)
HYSTERESIS_WINDOWS = 2
PRESENTER_MINIMUM_N = 20    # mirrors sealed SPEAKER_DISJOINT_SPLIT_CONTRACT_DEFAULT (DQ-21 pending)
SPEAKER_REPO = "speechbrain/spkrec-ecapa-voxceleb"


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


class State:
    """Progressive job state on the host volume (E1 reads it by one bounded status RPC)."""

    def __init__(self, job_dir):
        self.job_dir = Path(job_dir)
        self.job_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.job_dir / "state.json"
        self.doc = {"phase": None, "status": "running", "started_at": now(), "progress": {}, "events": []}

    def update(self, **fields):
        self.doc.update(fields)
        self.doc["updated_at"] = now()
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.doc, indent=1, default=str))
        os.replace(tmp, self.path)

    def event(self, message):
        self.doc["events"].append({"at": now(), "message": message[:400]})
        self.update()


def _s3(config):
    import boto3
    from botocore.config import Config
    return boto3.client("s3", endpoint_url=config["endpoint"], region_name=config["region"],
                        aws_access_key_id=config["access_key_id"], aws_secret_access_key=config["secret_access_key"],
                        config=Config(signature_version="s3v4", connect_timeout=10, read_timeout=60,
                                      retries={"max_attempts": 3}, max_pool_connections=32))


# ---------------------------------------------------------------- corpus layout (pure)
def list_objects(sdk, bucket, prefix, state=None):
    """Files under a prefix; zero-byte extension-less keys are prefix markers, not files (they collide
    with directories at staging → IsADirectoryError) and are counted separately."""
    objects, markers, token = [], 0, None
    while True:
        kwargs = {"Bucket": bucket, "Prefix": prefix, "MaxKeys": 1000}
        if token:
            kwargs["ContinuationToken"] = token
        page = sdk.list_objects_v2(**kwargs)
        for o in page.get("Contents", []):
            key, size = o["Key"], int(o["Size"])
            if key.endswith("/") or (size == 0 and "." not in key.rsplit("/", 1)[-1]):
                markers += 1
                continue
            objects.append((key, size))
        if state:
            state.update(progress={"listed_objects": len(objects)})
        if not page.get("IsTruncated"):
            return objects, markers
        token = page.get("NextContinuationToken")


def classify_objects(objects):
    """`datasets/<code>/<session>/{audio,transcript,metadata}/<id>.*` + `datasets/<code>/<session>.tar.xz` + manifests."""
    per = {}
    for key, size in objects:
        parts = key.split("/")
        code = parts[1] if len(parts) > 2 and parts[1] in LANGUAGES else None
        if code is None:
            u = per.setdefault("_unclassified", {"objects": 0, "bytes": 0, "sample_keys": []})
            u["objects"] += 1; u["bytes"] += size
            if len(u["sample_keys"]) < 5:
                u["sample_keys"].append(key)
            continue
        lang = per.setdefault(code, {"language": LANGUAGES[code], "audio": {"objects": 0, "bytes": 0, "extensions": {}},
                                     "transcript": {"objects": 0, "bytes": 0}, "metadata": {"objects": 0, "bytes": 0},
                                     "archives": {"objects": 0, "bytes": 0}, "manifests": 0, "other": 0,
                                     "sessions": set(), "archive_sessions": set(), "audio_ids": set(), "transcript_ids": set()})
        name = parts[-1]; ext = Path(name).suffix.lower()
        folder = next((f for f in ("audio", "transcript", "metadata") if f in parts[2:-1]), None)
        if folder:
            session = parts[parts.index(folder) - 1]
            lang["sessions"].add(session)
            lang[folder]["objects"] += 1; lang[folder]["bytes"] += size
            if folder == "audio":
                lang["audio"]["extensions"][ext] = lang["audio"]["extensions"].get(ext, 0) + 1
                lang["audio_ids"].add((session, Path(name).stem))
            elif folder == "transcript":
                lang["transcript_ids"].add((session, Path(name).stem))
        elif name.endswith(".tar.xz"):
            lang["archives"]["objects"] += 1; lang["archives"]["bytes"] += size
            lang["archive_sessions"].add(name[:-len(".tar.xz")])
        elif ext == ".tsv" and name.startswith("manifest"):
            lang["manifests"] += 1
        else:
            lang["other"] += 1
    for code, lang in per.items():
        if code.startswith("_"):
            continue
        paired = lang["audio_ids"] & lang["transcript_ids"]
        lang["pairing"] = {"matched_pairs": len(paired), "audio_without_transcript": len(lang["audio_ids"] - paired),
                           "transcript_without_audio": len(lang["transcript_ids"] - paired)}
        lang["session_count"] = len(lang["sessions"])
        lang["archive_only_sessions"] = len(lang["archive_sessions"] - lang["sessions"])
        for k in ("sessions", "archive_sessions", "audio_ids", "transcript_ids"):
            lang.pop(k)
    return per


def read_segments(transcript):
    """`start\tend\tspeaker\ttext` rows → (start, end, speaker, text); malformed rows are skipped."""
    rows = []
    for line in Path(transcript).read_text(errors="ignore").splitlines():
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        try:
            start, end = float(parts[0]), float(parts[1])
        except ValueError:
            continue
        rows.append((start, end, parts[2].strip(), parts[3].strip()))
    return rows


def read_metadata(path):
    """`metadata/<id>.tsv` → {speaker_id: {gender, age, device, environment, locale}} (blank cells → None)."""
    out = {}
    path = Path(path)
    if not path.exists():
        return out
    lines = path.read_text(errors="ignore").splitlines()
    if not lines:
        return out
    header = [h.strip().lower() for h in lines[0].split("\t")]
    for line in lines[1:]:
        row = dict(zip(header, (c.strip() for c in line.split("\t"))))
        if row.get("speaker_id"):
            out[row["speaker_id"]] = {k: (row.get(k) or None) for k in ("gender", "age", "device", "environment", "locale")}
    return out


def _transcript(wav):
    return wav.parent.parent / "transcript" / (wav.stem + ".txt")


def _metadata_path(wav):
    return wav.parent.parent / "metadata" / (wav.stem + ".tsv")


def _sessions(root):
    """{code: {session: dir}} for every `datasets/<code>/<session>/audio` present on the host."""
    corpus = Path(root) / "corpus" / "datasets"
    out = {}
    if not corpus.exists():
        return out
    for code_dir in sorted(p for p in corpus.iterdir() if p.is_dir() and p.name in LANGUAGES):
        sessions = {d.name: d for d in sorted(code_dir.iterdir()) if (d / "audio").is_dir()}
        if sessions:
            out[code_dir.name] = sessions
    return out


def _origins(root):
    path = Path(root) / "sessions_index.json"
    return json.loads(path.read_text()) if path.exists() else {}


def _wavs(session_dir):
    return sorted(p for p in (session_dir / "audio").iterdir() if p.suffix.lower() in AUDIO_EXT)


def _corpus_files(root, per_language_limit=None, seed=7, origins_allowed=None):
    """{code: [wav]} on the host, optionally filtered by session origin and sampled per language."""
    origins = _origins(root)
    files = {}
    for code, sessions in _sessions(root).items():
        audio = [w for s, d in sessions.items() if origins_allowed is None or origins.get(f"{code}/{s}", "folder") in origins_allowed
                 for w in _wavs(d)]
        if per_language_limit:
            random.Random(seed).shuffle(audio)
            audio = audio[:per_language_limit]
        if audio:
            files[code] = audio
    return files


def _session(path):
    return path.parent.parent.name


# ---------------------------------------------------------------- corpus_census
def _survey_bucket(sdk, bucket):
    top = sdk.list_objects_v2(Bucket=bucket, Delimiter="/", MaxKeys=1000)
    out = {"root_objects": [{"key": o["Key"], "bytes": int(o["Size"])} for o in top.get("Contents", [])], "prefixes": {}}
    for prefix in (c["Prefix"] for c in top.get("CommonPrefixes", [])):
        objects, markers = list_objects(sdk, bucket, prefix)
        ext = {}
        for key, _ in objects:
            e = Path(key).suffix.lower() or "(none)"
            ext[e] = ext.get(e, 0) + 1
        out["prefixes"][prefix] = {"objects": len(objects), "bytes": sum(s for _, s in objects), "prefix_markers": markers,
                                   "extensions": dict(sorted(ext.items(), key=lambda kv: -kv[1])[:8])}
    return out


def _stage(sdk, bucket, objects, target, state, parallelism):
    todo = [(k, s) for k, s in objects
            if not (target / k).is_dir() and (not (target / k).exists() or (target / k).stat().st_size != s)]
    done = [0, 0]

    def pull(item):
        key, size = item
        dest = target / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        sdk.download_file(bucket, key, str(dest))
        done[0] += 1; done[1] += size
        if done[0] % 200 == 0:
            state.update(progress={"stage": "staging", "staged_objects": done[0], "staged_bytes": done[1], "to_stage": len(todo)})

    with ThreadPoolExecutor(max_workers=parallelism) as pool:
        list(pool.map(pull, todo))
    return {"to_stage": len(todo), "objects_pulled_this_run": done[0], "bytes_pulled_this_run": done[1],
            "objects_present": sum(1 for k, _ in objects if (target / k).is_file())}


def extract_archives(root, state, parallelism=12):
    """`<code>/<session>.tar.xz` whose session folder is absent is unpacked beside it; every session's
    origin (folder | archive | folder+archive) is indexed so splits can hold archive-only sessions out."""
    corpus = Path(root) / "corpus" / "datasets"
    index_path = Path(root) / "sessions_index.json"
    index = _origins(root)
    jobs = []
    for code_dir in sorted(p for p in corpus.iterdir() if p.is_dir() and p.name in LANGUAGES) if corpus.exists() else []:
        for d in code_dir.iterdir():
            if d.is_dir() and not d.name.endswith(".partial"):
                index.setdefault(f"{code_dir.name}/{d.name}", "folder")
        for archive in sorted(code_dir.glob("*.tar.xz")):
            session = archive.name[:-len(".tar.xz")]
            key = f"{code_dir.name}/{session}"
            if (code_dir / session).is_dir():
                if index.get(key) == "folder":
                    index[key] = "folder+archive"
            else:
                jobs.append((archive, code_dir / session, key))
    done, failed = [0], []

    def unpack(job):
        archive, dest, key = job
        tmp = dest.with_name(dest.name + ".partial")
        shutil.rmtree(tmp, ignore_errors=True); tmp.mkdir(parents=True)
        result = subprocess.run(["tar", "-xJf", str(archive), "-C", str(tmp)], capture_output=True, timeout=1800, check=False)
        if result.returncode != 0:
            failed.append({"key": key, "error": result.stderr.decode(errors="replace")[-200:]})
            shutil.rmtree(tmp, ignore_errors=True)
            return
        inner = list(tmp.iterdir())
        if len(inner) == 1 and inner[0].is_dir() and not (tmp / "audio").exists():
            os.replace(inner[0], dest); shutil.rmtree(tmp, ignore_errors=True)
        else:
            os.replace(tmp, dest)
        index[key] = "archive"
        done[0] += 1
        if done[0] % 50 == 0 and state:
            state.update(progress={"stage": "extracting archives", "extracted": done[0], "of": len(jobs)})

    with ThreadPoolExecutor(max_workers=parallelism) as pool:
        list(pool.map(unpack, jobs))
    index_path.write_text(json.dumps(index, indent=0, sort_keys=True))
    origins = {}
    for v in index.values():
        origins[v] = origins.get(v, 0) + 1
    return {"archives_to_extract": len(jobs), "extracted_this_run": done[0], "failed_count": len(failed), "failed": failed[:10],
            "session_origins": origins}


def corpus_census(control, state):
    """Measure the labelled corpus, stage it inside the perimeter, unpack archive-only sessions, read it as a database."""
    obs, root = control["connector"], Path(control["root"])
    bucket, prefix = control.get("bucket", "google-transcripts"), control.get("prefix", "datasets/")
    sdk = _s3(obs)
    objects, markers = list_objects(sdk, bucket, prefix, state)
    per = classify_objects(objects)
    receipt = {"bucket": bucket, "prefix": prefix, "object_count": len(objects), "prefix_markers_skipped": markers,
               "volume_bytes": sum(s for _, s in objects),
               "layout": "datasets/<code>/<session>/{audio,transcript,metadata}/<id>.{wav,txt,tsv} + datasets/<code>/<session>.tar.xz + manifests",
               "languages": per,
               "target_five_coverage": {name: any(v.get("language") == name or (name == "Swahili" and v.get("language") == "Kiswahili")
                                                   for v in per.values()) for name in TARGET_FIVE},
               "code_switched_spans_labelled": 0,
               "honest_gap": ("English and Sheng are absent; transcripts are time-aligned and speaker-attributed but carry NO per-span "
                              "language label, so code-switched spans are unlabelled (MUST-NOT §1 stands for the final model).")}
    if control.get("survey", True):
        state.update(progress={"stage": "surveying bucket"})
        receipt["bucket_survey"] = _survey_bucket(sdk, bucket)
    if control.get("stage", True):
        target = root / "corpus"
        target.mkdir(parents=True, exist_ok=True)
        state.update(progress={"stage": "staging", "to_stage": None})
        receipt["staged"] = {**_stage(sdk, bucket, objects, target, state, int(control.get("parallelism", 24))),
                             "root": str(target), "custody": "RMS_TENANT · host volume · never leaves perimeter"}
        (root / "corpus_manifest.json").write_text(json.dumps({"bucket": bucket, "prefix": prefix, "objects": objects, "measured_at": now()}))
        if control.get("extract_archives", True):
            state.update(progress={"stage": "extracting archives"})
            receipt["archives"] = extract_archives(root, state)
        state.update(progress={"stage": "reading corpus as database"})
        receipt["measured_on_host"] = measure_staged(root)
    return receipt


def _audio_probe(path):
    """ffprobe facts: duration, actual codec, sample rate, channels (the `.wav` suffix is a declaration, not a fact)."""
    cmd = ["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,sample_rate,channels:format=duration", "-of", "json", str(path)]
    try:
        doc = json.loads(subprocess.run(cmd, capture_output=True, timeout=60, check=False).stdout or b"{}")
        stream = (doc.get("streams") or [{}])[0]
        duration = float(doc.get("format", {}).get("duration"))
    except (ValueError, TypeError, OSError, subprocess.TimeoutExpired):
        return None
    return {"seconds": duration, "codec": stream.get("codec_name"), "sample_rate": int(stream.get("sample_rate") or 0), "channels": stream.get("channels")}


def measure_staged(root, parallelism=24):
    """AIP §1.1 — the corpus read as a database: one row per file (`corpus_db/files.jsonl`) and one row per
    transcribed segment (`corpus_db/segments.jsonl`) with language / session / origin / speaker / condition
    columns; no audio bytes, no text. Returns the per-language census of those rows."""
    root = Path(root)
    origins = _origins(root)
    db = root / "corpus_db"
    db.mkdir(exist_ok=True)
    out = {}

    def read(item):
        session, wav = item
        return session, wav, _audio_probe(wav), read_metadata(_metadata_path(wav)), (read_segments(_transcript(wav)) if _transcript(wav).exists() else [])

    with open(db / "files.jsonl", "w") as files_out, open(db / "segments.jsonl", "w") as segs_out, ThreadPoolExecutor(max_workers=parallelism) as pool:
        for code, sessions in _sessions(root).items():
            row = {"language": LANGUAGES[code], "sessions": len(sessions), "session_origins": {}, "audio_files": 0, "unreadable_audio": 0,
                   "audio_seconds": 0.0, "codecs": {}, "sample_rates": {}, "transcribed_files": 0, "segments": 0, "speech_seconds": 0.0, "speakers": set(),
                   "speakers_with_gender_suffix": 0, "metadata_gender": {}, "metadata_condition_cells_filled": 0, "metadata_condition_cells": 0}
            for session in sessions:
                origin = origins.get(f"{code}/{session}", "folder")
                row["session_origins"][origin] = row["session_origins"].get(origin, 0) + 1
            for session, wav, probe, meta, segs in pool.map(read, [(s, w) for s, d in sessions.items() for w in _wavs(d)]):
                origin = origins.get(f"{code}/{session}", "folder")
                speech = sum(max(0.0, e - s) for s, e, _, _ in segs)
                row["audio_files"] += 1
                if probe is None:
                    row["unreadable_audio"] += 1
                else:
                    row["audio_seconds"] += probe["seconds"]
                    row["codecs"][probe["codec"]] = row["codecs"].get(probe["codec"], 0) + 1
                    row["sample_rates"][str(probe["sample_rate"])] = row["sample_rates"].get(str(probe["sample_rate"]), 0) + 1
                if segs:
                    row["transcribed_files"] += 1; row["segments"] += len(segs); row["speech_seconds"] += speech
                for spk, m in meta.items():
                    row["metadata_gender"][m.get("gender") or "blank"] = row["metadata_gender"].get(m.get("gender") or "blank", 0) + 1
                    for k in ("age", "device", "environment"):
                        row["metadata_condition_cells"] += 1; row["metadata_condition_cells_filled"] += int(bool(m.get(k)))
                speakers = sorted({s for _, _, s, _ in segs})
                for spk in speakers:
                    row["speakers"].add((session, spk)); row["speakers_with_gender_suffix"] += int(spk.endswith(("_m", "_f")))
                files_out.write(json.dumps({"code": code, "language": LANGUAGES[code], "session": session, "file": wav.stem, "origin": origin,
                                            "declared_suffix": wav.suffix.lower(), "bytes": wav.stat().st_size, "audio": probe, "segments": len(segs),
                                            "speech_seconds": round(speech, 3), "speakers": speakers, "metadata": meta}) + "\n")
                for s, e, spk, text in segs:
                    segs_out.write(json.dumps({"code": code, "session": session, "file": wav.stem, "start": s, "end": e, "speaker": spk,
                                               "chars": len(text), "language_label_source": "folder", "code_switch": "unlabelled"}) + "\n")
            row["session_local_speaker_ids"] = len(row.pop("speakers"))
            row["audio_hours"] = round(row.pop("audio_seconds") / 3600.0, 2); row["speech_hours"] = round(row.pop("speech_seconds") / 3600.0, 2)
            out[code] = row
    out["_reading"] = ("Speaker ids are numbered per session (Speaker_1_m …) and are not linked across sessions by the corpus; the "
                       "speaker_linkage phase links them biometrically so the split can be presenter-disjoint. Condition columns "
                       "(age/device/environment) are mostly blank → condition stratification is unmeasured. `codecs` records the "
                       "actual container codec behind the declared .wav suffix.")
    out["_database"] = {"files_jsonl": str(db / "files.jsonl"), "segments_jsonl": str(db / "segments.jsonl")}
    return out


# ---------------------------------------------------------------- register_bases
def _licence_from_card(model_dir):
    readme = Path(model_dir) / "README.md"
    if readme.exists():
        m = re.search(r"^license:\s*[\"']?([\w\.-]+)", readme.read_text(errors="ignore"), re.MULTILINE)
        if m:
            return m.group(1)
    return None


def _pull_model(root, repo):
    from huggingface_hub import snapshot_download
    local = snapshot_download(repo, cache_dir=str(Path(root) / "models" / "hf_cache"), token=False)
    weights = sorted(p for p in Path(local).rglob("*") if p.suffix in {".safetensors", ".bin", ".ckpt", ".pt"} and p.is_file())
    digest = hashlib.sha256()
    for w in weights:
        digest.update(w.name.encode()); digest.update(bytes.fromhex(sha256_file(w)))
    return {"repo": repo, "revision": Path(local).name, "local_path": local, "weight_files": [w.name for w in weights],
            "weight_bytes": sum(w.stat().st_size for w in weights), "weight_sha256": digest.hexdigest(),
            "licence_card": _licence_from_card(local), "pulled_at": now()}


def register_bases(control, state):
    import torch
    root = Path(control["root"])
    (root / "models").mkdir(parents=True, exist_ok=True)
    out = {}
    for entry, repo in (("whisper-lid-v1-mit", control.get("whisper_repo", "openai/whisper-small")),
                        ("speechbrain-voxlingua107-apache-2-0", "speechbrain/lang-id-voxlingua107-ecapa")):
        state.event(f"pulling {repo}")
        out[entry] = {**_pull_model(root, repo), "execution_mode": "cuda" if torch.cuda.is_available() else "cpu",
                      "lora_adapter_declaration": ("LoRA r=16 on encoder q_proj/v_proj; base frozen" if "whisper" in repo
                                                   else "frozen ECAPA embedding fused into the classifier; no adapter")}
    (root / "base_registration.json").write_text(json.dumps(out, indent=1))
    return out


# ---------------------------------------------------------------- audio helpers
def _load_audio(path, max_seconds=None):
    """Decode via ffmpeg to mono 16 kHz float32 (no python codec zoo)."""
    import numpy as np
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SAMPLE_RATE)]
    if max_seconds:
        cmd += ["-t", str(max_seconds)]
    cmd.append("-")
    raw = subprocess.run(cmd, capture_output=True, timeout=300, check=False).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def speech_windows(segments, audio_samples, max_windows, seed=0):
    """Candidate 2 s windows inside transcribed speech segments only (music/silence never gets a language
    label), each attributed to the segment's speaker; sampled evenly across the file. Returns (start_sample, speaker)."""
    win = int(WINDOW_SECONDS * SAMPLE_RATE)
    candidates = []
    for s, e, speaker, _ in segments:
        a, b = int(s * SAMPLE_RATE), min(int(e * SAMPLE_RATE), audio_samples)
        candidates.extend((i, speaker) for i in range(a, b - win + 1, win))
    if len(candidates) > max_windows:
        random.Random(seed).shuffle(candidates)
        candidates = sorted(candidates[:max_windows])
    return candidates


def spans(seq, min_span=MIN_SPAN_SECONDS, hysteresis=HYSTERESIS_WINDOWS):
    """Deterministic window→span rule: a label change needs `hysteresis` consecutive windows;
    spans shorter than `min_span` seconds fold into `unmeasured`. Each span carries start/end seconds."""
    out, current, pending = [], None, []
    for start, label, conf in seq:
        end = start + WINDOW_SECONDS
        if current is None:
            current = {"start": start, "end": end, "label": label}; continue
        if label == current["label"]:
            current["end"] = end; pending = []; continue
        pending.append((start, label))
        if len(pending) >= hysteresis and all(p[1] == label for p in pending):
            out.append(current); current = {"start": pending[0][0], "end": end, "label": label}; pending = []
        else:
            current["end"] = end
    if current:
        out.append(current)
    return [{**s, "label": s["label"] if s["end"] - s["start"] >= min_span else "unmeasured"} for s in out]


# ---------------------------------------------------------------- speaker_linkage
def _clusters(root):
    path = Path(root) / "speaker_clusters.json"
    return json.loads(path.read_text())["clusters"] if path.exists() else {}


def _conditions(root):
    """AIP §4.3 condition column from the corpus database: source sample rate per file (11 kHz telephone-band
    material vs 44.1/48 kHz studio) — the confound a language model must not learn instead of the language."""
    path = Path(root) / "corpus_db" / "files.jsonl"
    out = {}
    if path.exists():
        for line in path.read_text().splitlines():
            row = json.loads(line)
            audio = row.get("audio") or {}
            out[(row["code"], row["session"], row["file"])] = f"{audio.get('sample_rate') or 0}Hz"
    return out


def speaker_crops(segments, audio, per_speaker, crop_seconds=3.0, min_seconds=1.5):
    """Up to `per_speaker` crops per session-local speaker from that speaker's longest segments (verification
    material, transient: never written to disk)."""
    by = {}
    for s, e, speaker, _ in segments:
        if e - s >= min_seconds:
            by.setdefault(speaker, []).append((s, e))
    out = {}
    for speaker, segs in by.items():
        crops = []
        for s, e in sorted(segs, key=lambda se: -(se[1] - se[0]))[:per_speaker]:
            length = min(crop_seconds, e - s)
            a = int((s + min(0.2, (e - s - length) / 2)) * SAMPLE_RATE); b = a + int(length * SAMPLE_RATE)
            if b <= audio.shape[0]:
                crops.append(audio[a:b])
        if crops:
            out[speaker] = crops
    return out


def cluster_presenters(embeddings, threshold):
    """Average-linkage clustering on cosine distance; two session-local ids closer than `threshold` (cosine
    similarity) are one presenter. Returns 1-based labels."""
    import numpy as np
    from scipy.cluster.hierarchy import fcluster, linkage
    if len(embeddings) < 2:
        return [1] * len(embeddings)
    return [int(x) for x in fcluster(linkage(np.stack(embeddings), method="average", metric="cosine"), t=1.0 - threshold, criterion="distance")]


def speaker_linkage(control, state):
    """Link session-local speaker ids into presenters with a speaker-verification ECAPA embedding (AIP §6.2:
    embeddings are destroyed after cluster assignment; only opaque presenter ids persist)."""
    import numpy as np
    import torch
    from speechbrain.inference.speaker import EncoderClassifier
    root = Path(control["root"])
    device = "cuda" if torch.cuda.is_available() else "cpu"
    instrument = _pull_model(root, control.get("speaker_repo", SPEAKER_REPO))
    enc = EncoderClassifier.from_hparams(source=instrument["local_path"], savedir=str(root / "models" / "spk_run"),
                                         run_opts={"device": device + ":0" if device == "cuda" else device})
    threshold = float(control.get("cosine_threshold", 0.45))
    per_speaker = int(control.get("crops_per_speaker", 6))
    max_audio = float(control.get("max_audio_seconds_per_file", 900))
    origins = _origins(root)
    clusters, report = {}, {}

    def crops_for(wav):
        segs = read_segments(_transcript(wav)) if _transcript(wav).exists() else []
        if not segs:
            return wav, {}
        try:
            audio = _load_audio(wav, max_audio)
        except Exception:
            return wav, {}
        return wav, speaker_crops(segs, audio, per_speaker)

    for code, sessions in _sessions(root).items():
        wavs = [w for d in sessions.values() for w in _wavs(d)]
        local = {}                       # (session, speaker) -> [crops]
        with ThreadPoolExecutor(max_workers=int(control.get("parallelism", 24))) as pool:
            for n, (wav, crops) in enumerate(pool.map(crops_for, wavs)):
                for speaker, items in crops.items():
                    local.setdefault((_session(wav), speaker), []).extend(items[:per_speaker])
                if n % 100 == 0:
                    state.update(progress={"stage": "cropping", "language": code, "files_done": n, "of": len(wavs), "local_ids": len(local)})
        keys = sorted(local)
        embeddings = []
        with torch.no_grad():
            for n, key in enumerate(keys):
                by_len = {}
                for crop in local[key]:
                    by_len.setdefault(crop.shape[0], []).append(crop)
                vectors = []
                for items in by_len.values():
                    sig = torch.from_numpy(np.stack(items)).to(device)
                    vectors.append(torch.nn.functional.normalize(enc.encode_batch(sig).squeeze(1).float(), dim=-1).cpu().numpy())
                mean = np.concatenate(vectors).mean(0)
                embeddings.append(mean / (np.linalg.norm(mean) + 1e-9))
                if n % 200 == 0:
                    state.update(progress={"stage": "embedding", "language": code, "local_ids_done": n, "of": len(keys)})
        labels = cluster_presenters(embeddings, threshold)
        del embeddings, local                                    # §6.2.4 — destroyed after cluster assignment
        clusters[code] = {f"{session}|{speaker}": label for (session, speaker), label in zip(keys, labels)}
        members, sessions_of, genders_of = {}, {}, {}
        for (session, speaker), label in zip(keys, labels):
            members[label] = members.get(label, 0) + 1
            sessions_of.setdefault(label, set()).add(session)
            genders_of.setdefault(label, set()).add(speaker[-1] if speaker.endswith(("_m", "_f")) else "?")
        report[code] = {"language": LANGUAGES[code], "session_local_ids": len(keys), "presenters": len(members),
                        "presenters_spanning_sessions": sum(1 for s in sessions_of.values() if len(s) > 1),
                        "singleton_presenters": sum(1 for m in members.values() if m == 1),
                        "largest_presenter_ids": max(members.values()) if members else 0,
                        "presenters_with_mixed_gender_suffix": sum(1 for g in genders_of.values() if {"m", "f"} <= g),
                        "sessions": len(sessions), "session_origins": {}, "meets_presenter_minimum_n": len(members) >= PRESENTER_MINIMUM_N}
        for session in sessions:
            o = origins.get(f"{code}/{session}", "folder")
            report[code]["session_origins"][o] = report[code]["session_origins"].get(o, 0) + 1
        state.update(progress={"stage": "clustered", "languages_done": len(report)})
    (root / "speaker_clusters.json").write_text(json.dumps({"instrument": instrument["repo"], "instrument_weight_sha256": instrument["weight_sha256"],
                                                             "cosine_threshold": threshold, "linked_at": now(), "clusters": clusters}, indent=0))
    return {"instrument": instrument, "method": f"ECAPA-TDNN speaker embedding, mean of ≤{per_speaker} crops per session-local id, average-linkage cosine clustering",
            "cosine_threshold": threshold, "presenter_minimum_n_default": PRESENTER_MINIMUM_N, "per_language": report,
            "custody": "embeddings held in memory only and destroyed after cluster assignment (AIP §6.2.4); persisted: opaque presenter ids per session-local speaker id",
            "reading": ("Presenters are inferred by voice similarity at the recorded threshold — a measured linkage, not ground truth. "
                        "presenters_with_mixed_gender_suffix is the visible error signal.")}


# ---------------------------------------------------------------- gate_eval
def gate_eval(control, state):
    """Overlay agreement of the two pre-trained bases against folder labels. Measured, never asserted."""
    import torch
    from speechbrain.inference.classifiers import EncoderClassifier
    from transformers import WhisperForConditionalGeneration, WhisperProcessor
    reg = json.loads((Path(control["root"]) / "base_registration.json").read_text())
    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = WhisperProcessor.from_pretrained(reg["whisper-lid-v1-mit"]["local_path"])
    whisper = WhisperForConditionalGeneration.from_pretrained(reg["whisper-lid-v1-mit"]["local_path"]).to(device).eval()
    vox = EncoderClassifier.from_hparams(source=reg["speechbrain-voxlingua107-apache-2-0"]["local_path"],
                                         savedir=str(Path(control["root"]) / "models" / "vox_run"), run_opts={"device": device + ":0" if device == "cuda" else device})
    lang_ids = {}
    for tok, idx in processor.tokenizer.get_vocab().items():
        m = re.fullmatch(r"<\|([a-z]{2,3})\|>", tok)
        if m:
            lang_ids[idx] = m.group(1)
    if not lang_ids:
        raise ValueError("WHISPER_LANGUAGE_TOKENS_NOT_FOUND")
    files = _corpus_files(control["root"], int(control.get("per_language_limit", 60)))
    threshold = float(control.get("confidence_threshold", 0.5))
    report = {"per_language": {}, "confidence_threshold": threshold, "window": "first 30 s of each file (Whisper) / first 10 s (VoxLingua107)"}
    for code, paths in files.items():
        expected_w, expected_v = WHISPER_ISO.get(code), VOX_ISO.get(code)
        row = {"language": LANGUAGES.get(code), "files": 0, "whisper": {"agree": 0, "abstain": 0, "top": {}},
               "voxlingua107": {"agree": 0, "abstain": 0, "top": {}},
               "in_whisper_vocabulary": expected_w is not None, "in_voxlingua107_vocabulary": expected_v is not None}
        for path in paths:
            try:
                audio = _load_audio(path, 30)
            except Exception:
                continue
            if audio.size < SAMPLE_RATE:
                continue
            row["files"] += 1
            feats = processor(audio, sampling_rate=SAMPLE_RATE, return_tensors="pt").input_features.to(device)
            with torch.no_grad():
                enc = whisper.model.encoder(feats).last_hidden_state
                start = torch.tensor([[whisper.config.decoder_start_token_id]], device=device)
                logits = whisper(encoder_outputs=(enc,), decoder_input_ids=start).logits[0, -1]
                ids = torch.tensor(list(lang_ids), device=device)
                probs = torch.softmax(logits[ids], dim=-1)
                conf, arg = probs.max(0)
                label = lang_ids[int(ids[arg])]
            if float(conf) < threshold:
                row["whisper"]["abstain"] += 1
            else:
                row["whisper"]["top"][label] = row["whisper"]["top"].get(label, 0) + 1
                row["whisper"]["agree"] += int(label == expected_w)
            with torch.no_grad():
                sig = torch.tensor(audio[: 10 * SAMPLE_RATE]).unsqueeze(0).to(device)
                out_prob, _score, _index, text_lab = vox.classify_batch(sig)
                vconf = float(torch.softmax(out_prob[0], dim=-1).max())
                vlabel = text_lab[0].split(":")[0].strip()
            if vconf < threshold:
                row["voxlingua107"]["abstain"] += 1
            else:
                row["voxlingua107"]["top"][vlabel] = row["voxlingua107"]["top"].get(vlabel, 0) + 1
                row["voxlingua107"]["agree"] += int(vlabel == expected_v)
        for k in ("whisper", "voxlingua107"):
            judged = row["files"] - row[k]["abstain"]
            row[k]["agreement_rate"] = round(row[k]["agree"] / judged, 4) if judged else None
            row[k]["abstention_rate"] = round(row[k]["abstain"] / row["files"], 4) if row["files"] else None
            row[k]["top"] = dict(sorted(row[k]["top"].items(), key=lambda kv: -kv[1])[:5])
        report["per_language"][code] = row
        state.update(progress={"languages_evaluated": len(report["per_language"]), "of": len(files)})
    report["gate_default_threshold"] = 0.90
    report["reading"] = ("Agreement is measurable only for languages inside a base's vocabulary; the Kenyan languages "
                         "outside both vocabularies are structurally unknown to the overlay — the census marks them unmeasured.")
    return report


# ---------------------------------------------------------------- train_baseline
def split_by_presenter(items, seed=11, held_fraction=0.2):
    """items: (code, presenter, origin). Folder sessions → train / held-out by PRESENTER (no presenter in both);
    archive-only sessions → a second, session-disjoint test set. Returns per-item assignment + per-language counts."""
    rnd = random.Random(seed)
    per_code = {}
    for n, (code, presenter, origin) in enumerate(items):
        per_code.setdefault(code, {"train_pool": {}, "archive": []})
        if origin == "archive":
            per_code[code]["archive"].append(n)
        else:
            per_code[code]["train_pool"].setdefault(presenter, []).append(n)
    assignment, summary = {}, {}
    for code, pools in per_code.items():
        presenters = sorted(pools["train_pool"])
        rnd.shuffle(presenters)
        total = sum(len(v) for v in pools["train_pool"].values())
        held, held_windows = set(), 0
        for p in presenters:
            if len(presenters) - len(held) <= 1 or (held_windows >= held_fraction * total and held):
                break
            held.add(p); held_windows += len(pools["train_pool"][p])
        for p, idx in pools["train_pool"].items():
            for n in idx:
                assignment[n] = "held" if p in held else "train"
        for n in pools["archive"]:
            assignment[n] = "archive_test"
        summary[code] = {"presenters_train": len(presenters) - len(held), "presenters_held": len(held),
                         "windows_train": total - held_windows, "windows_held": held_windows, "windows_archive_test": len(pools["archive"]),
                         "meets_presenter_minimum_n": len(presenters) - len(held) >= PRESENTER_MINIMUM_N}
    return assignment, summary


def _speaker_probe(features, presenters, seed=5, min_windows=20):
    """MUST-DO §4: a linear speaker-identification probe on the artefact's representation of HELD-OUT presenters,
    50/50 per presenter. Reported against chance and the majority baseline — measured, not hoped."""
    import torch
    by = {}
    for i, p in enumerate(presenters):
        by.setdefault(p, []).append(i)
    keep = {p: idx for p, idx in by.items() if len(idx) >= min_windows}
    if len(keep) < 2:
        return {"measured": False, "reason": f"fewer than two held-out presenters with ≥{min_windows} windows"}
    rnd = random.Random(seed)
    labels = {p: i for i, p in enumerate(sorted(keep))}
    tr, te = [], []
    for p, idx in keep.items():
        idx = idx[:]; rnd.shuffle(idx); h = len(idx) // 2
        tr += [(i, labels[p]) for i in idx[:h]]; te += [(i, labels[p]) for i in idx[h:]]
    x = torch.as_tensor(features, dtype=torch.float32)
    x = (x - x.mean(0)) / (x.std(0) + 1e-6)
    xtr, ytr = x[[i for i, _ in tr]], torch.tensor([y for _, y in tr])
    xte, yte = x[[i for i, _ in te]], torch.tensor([y for _, y in te])
    lin = torch.nn.Linear(x.shape[1], len(labels))
    opt = torch.optim.Adam(lin.parameters(), lr=1e-2, weight_decay=1e-3)
    for _ in range(300):
        opt.zero_grad(); torch.nn.functional.cross_entropy(lin(xtr), ytr).backward(); opt.step()
    with torch.no_grad():
        acc = float((lin(xte).argmax(-1) == yte).float().mean())
    counts = torch.bincount(yte, minlength=len(labels)).float()
    chance, majority = 1.0 / len(labels), float(counts.max() / counts.sum())
    return {"measured": True, "presenters": len(labels), "test_windows": len(te), "accuracy": round(acc, 4), "chance": round(chance, 4),
            "majority_baseline": round(majority, 4), "above_chance": acc > max(chance, majority) + 0.05}


def train_baseline(control, state):
    import numpy as np
    import torch
    from peft import LoraConfig, get_peft_model
    from speechbrain.inference.classifiers import EncoderClassifier
    from torch import nn
    from transformers import WhisperModel, WhisperProcessor
    torch.backends.cuda.matmul.allow_tf32 = True
    root = Path(control["root"])
    reg = json.loads((root / "base_registration.json").read_text())
    device = "cuda" if torch.cuda.is_available() else "cpu"
    budget = float(control.get("max_seconds", 9000)); train_share = float(control.get("train_share", 0.65)); t0 = time.time()
    clusters, origins, sessions, conditions = _clusters(root), _origins(root), _sessions(root), _conditions(root)
    codes = sorted(sessions)
    label_of = {c: i for i, c in enumerate(codes)}
    per_language_files = int(control.get("per_language_files", 0)) or None
    max_windows_per_file = int(control.get("max_windows_per_file", 40))
    max_windows_per_language = int(control.get("max_windows_per_language", 16000))
    max_audio_seconds = float(control.get("max_audio_seconds_per_file", 900))
    files = _corpus_files(root, per_language_files)
    plan = [(code, wav, min(max_windows_per_file, max(1, max_windows_per_language // len(paths))))
            for code, paths in files.items() for wav in paths]
    state.update(progress={"stage": "windowing", "files": len(plan), "classes": codes})

    def prepare(item):
        code, wav, cap = item
        segs = read_segments(_transcript(wav)) if _transcript(wav).exists() else []
        if not segs:
            return []
        try:
            audio = _load_audio(wav, max_audio_seconds)
        except Exception:
            return []
        win = int(WINDOW_SECONDS * SAMPLE_RATE)
        session = _session(wav); origin = origins.get(f"{code}/{session}", "folder")
        condition = conditions.get((code, session, wav.stem), "unmeasured")
        out = []
        for start, speaker in speech_windows(segs, audio.shape[0], cap, seed=int(hashlib.sha256(wav.stem.encode()).hexdigest()[:8], 16)):
            presenter = f"{code}:{clusters.get(code, {}).get(f'{session}|{speaker}', f'{session}|{speaker}')}"
            out.append(((audio[start:start + win] * 32767.0).astype(np.int16), label_of[code], presenter, origin, str(wav), start / SAMPLE_RATE, condition))
        return out

    windows = []
    with ThreadPoolExecutor(max_workers=int(control.get("parallelism", 24))) as pool:
        for n, out in enumerate(pool.map(prepare, plan)):
            windows.extend(out)
            if n % 200 == 0:
                state.update(progress={"stage": "windowing", "files_done": n, "of": len(plan), "windows": len(windows), "elapsed_s": round(time.time() - t0)})
    assignment, split_summary = split_by_presenter([(codes[w[1]], w[2], w[3]) for w in windows])
    sets = {"train": [], "held": [], "archive_test": []}
    for n, w in enumerate(windows):
        sets[assignment[n]].append(w)
    train_w, held_w, archive_w = sets["train"], sets["held"], sets["archive_test"]
    if not train_w or not held_w:
        raise ValueError(f"SPLIT_EMPTY: train={len(train_w)} held={len(held_w)}")
    state.update(progress={"stage": "features", "train_windows": len(train_w), "held_windows": len(held_w), "archive_test_windows": len(archive_w),
                           "split": split_summary})
    processor = WhisperProcessor.from_pretrained(reg["whisper-lid-v1-mit"]["local_path"])
    base = WhisperModel.from_pretrained(reg["whisper-lid-v1-mit"]["local_path"]).encoder.to(device)
    for p in base.parameters():
        p.requires_grad = False
    lora = get_peft_model(base, LoraConfig(r=int(control.get("lora_r", 16)), lora_alpha=32, lora_dropout=0.05,
                                            target_modules=["q_proj", "v_proj"], bias="none"))
    vox = EncoderClassifier.from_hparams(source=reg["speechbrain-voxlingua107-apache-2-0"]["local_path"],
                                         savedir=str(root / "models" / "vox_run"), run_opts={"device": device + ":0" if device == "cuda" else device})
    hidden = base.config.d_model
    win = int(WINDOW_SECONDS * SAMPLE_RATE)
    with torch.no_grad():
        vox_dim = int(vox.encode_batch(torch.zeros(1, win, device=device)).shape[-1])   # measured (VoxLingua107 ECAPA: 256)
    head = nn.Sequential(nn.LayerNorm(hidden + vox_dim), nn.Dropout(0.1), nn.Linear(hidden + vox_dim, len(codes))).to(device)
    frames = int(WINDOW_SECONDS * 50)  # encoder positions covering the window (Whisper: 50 positions / second)

    def features(chunk):
        arr = [w[0].astype(np.float32) / 32767.0 for w in chunk]
        try:
            feats = processor.feature_extractor(arr, sampling_rate=SAMPLE_RATE, return_tensors="pt", device=device).input_features
        except TypeError:
            feats = processor.feature_extractor(arr, sampling_rate=SAMPLE_RATE, return_tensors="pt").input_features
        return feats.to(device), torch.from_numpy(np.stack(arr)).to(device)

    def embed(chunk):
        feats, sig = features(chunk)
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device == "cuda"):
            enc = lora(input_features=feats).last_hidden_state[:, :frames].float().mean(1)
        with torch.no_grad():
            vemb = vox.encode_batch(sig).squeeze(1).float()
        return enc, torch.cat([enc, vemb.detach()], dim=-1)

    params = [p for p in lora.parameters() if p.requires_grad] + list(head.parameters())
    trainable = sum(p.numel() for p in params)
    optim = torch.optim.AdamW(params, lr=float(control.get("lr", 3e-4)), weight_decay=0.01)
    dp = {"requested": bool(control.get("dp_sgd", True)), "applied": False,
          "reason": ("Opacus per-sample gradients are not applied through the frozen Whisper encoder + PEFT wrappers in this "
                     "baseline; DP-SGD remains DEFAULT for the final commissioned model (DQ-24 fork stands).")}
    batch, eval_batch = int(control.get("batch_size", 64)), int(control.get("eval_batch_size", 128))
    threshold = float(control.get("confidence_threshold", 0.6))
    art = root / "artefacts" / control["job_id"]; art.mkdir(parents=True, exist_ok=True)

    def evaluate(items, keep_features=False):
        lora.eval(); head.eval()
        per = {c: {"windows": 0, "correct": 0, "abstain": 0} for c in codes}
        per_condition = {}
        confusion, window_labels, feats_enc, feats_logits, presenters = {}, {}, [], [], []
        with torch.no_grad():
            for i in range(0, len(items), eval_batch):
                chunk = items[i:i + eval_batch]
                enc, fused = embed(chunk)
                logits = head(fused)
                probs = torch.softmax(logits, dim=-1)
                conf, pred = probs.max(-1)
                if keep_features:
                    feats_enc.append(enc.cpu()); feats_logits.append(logits.cpu()); presenters += [w[2] for w in chunk]
                for w, c, p in zip(chunk, conf.tolist(), pred.tolist()):
                    code = codes[w[1]]; per[code]["windows"] += 1
                    cond = per_condition.setdefault(w[6], {"windows": 0, "correct": 0, "abstain": 0, "languages": {}})
                    cond["windows"] += 1; cond["languages"][code] = cond["languages"].get(code, 0) + 1
                    if c < threshold:
                        per[code]["abstain"] += 1; cond["abstain"] += 1; label = "unmeasured"
                    else:
                        label = codes[p]; per[code]["correct"] += int(p == w[1]); cond["correct"] += int(p == w[1])
                        confusion.setdefault(code, {}); confusion[code][label] = confusion[code].get(label, 0) + 1
                    window_labels.setdefault(w[4], []).append((w[5], label, round(c, 3)))
        for row in list(per.values()) + list(per_condition.values()):
            judged = row["windows"] - row["abstain"]
            row["accuracy"] = round(row["correct"] / judged, 4) if judged else None
            row["abstention_rate"] = round(row["abstain"] / row["windows"], 4) if row["windows"] else None
        judged_all = sum(r["correct"] for r in per.values()), sum(r["windows"] - r["abstain"] for r in per.values())
        report = {"windows": len(items), "per_language": per, "per_condition_sample_rate": per_condition,
                  "overall_accuracy_on_judged": round(judged_all[0] / judged_all[1], 4) if judged_all[1] else None,
                  "overall_abstention_rate": round(sum(r["abstain"] for r in per.values()) / len(items), 4) if items else None,
                  "confidence_threshold": threshold, "confusion_top": {c: dict(sorted(v.items(), key=lambda kv: -kv[1])[:4]) for c, v in confusion.items()}}
        lora.train(); head.train()
        extra = (torch.cat(feats_enc).numpy(), torch.cat(feats_logits).numpy(), presenters) if keep_features and feats_enc else None
        return report, window_labels, extra

    rnd = random.Random(3)
    curve_subset = held_w[:] ; rnd.shuffle(curve_subset); curve_subset = curve_subset[:int(control.get("curve_windows", 2048))]
    steps, losses, curve, epoch = 0, [], [], 0
    eval_every = int(control.get("eval_every_steps", 300))
    lora.train(); head.train()
    stop = False
    while not stop:
        rnd.shuffle(train_w)
        for i in range(0, len(train_w), batch):
            if time.time() - t0 > budget * train_share:
                stop = True; break
            chunk = train_w[i:i + batch]
            _, fused = embed(chunk)
            y = torch.tensor([w[1] for w in chunk], device=device)
            loss = nn.functional.cross_entropy(head(fused), y)
            optim.zero_grad(); loss.backward(); optim.step()
            losses.append(float(loss.detach())); steps += 1
            if steps % 20 == 0:
                state.update(progress={"stage": "training", "epoch": epoch, "step": steps, "loss": round(float(np.mean(losses[-20:])), 4),
                                       "elapsed_s": round(time.time() - t0), "budget_s": budget, "train_windows": len(train_w),
                                       "gpu_mem_gb": round(torch.cuda.max_memory_allocated() / 1e9, 2) if device == "cuda" else None,
                                       "curve_last": curve[-1] if curve else None})
            if steps % eval_every == 0:
                point, _, _ = evaluate(curve_subset)
                curve.append({"step": steps, "elapsed_s": round(time.time() - t0), "loss": round(float(np.mean(losses[-eval_every:])), 4),
                              "held_subset_accuracy_on_judged": point["overall_accuracy_on_judged"], "held_subset_abstention": point["overall_abstention_rate"]})
            if steps % 1000 == 0:
                lora.save_pretrained(str(art / "lora_adapter")); torch.save({"head": head.state_dict(), "classes": codes, "step": steps}, art / "head.pt")
        epoch += 1
        if not train_w:
            break
    state.update(progress={"stage": "evaluating held-out presenters", "steps": steps, "elapsed_s": round(time.time() - t0)})
    held_report, held_labels, held_feats = evaluate(held_w, keep_features=True)
    archive_report = evaluate(archive_w)[0] if archive_w else None
    probe = {"measured": False, "reason": "no held-out features"}
    if held_feats:
        state.update(progress={"stage": "no-speaker-id probe", "elapsed_s": round(time.time() - t0)})
        enc_f, logit_f, presenters = held_feats
        per_lang = {}
        for code in codes:
            idx = [i for i, p in enumerate(presenters) if p.startswith(code + ":")]
            if len(idx) >= 40:
                per_lang[code] = {"encoder_representation": _speaker_probe(enc_f[idx], [presenters[i] for i in idx]),
                                  "artefact_output_logits": _speaker_probe(logit_f[idx], [presenters[i] for i in idx])}
        probe = {"measured": bool(per_lang), "per_language": per_lang,
                 "any_language_above_chance": {k: any(v[k].get("above_chance", False) for v in per_lang.values()) for k in ("encoder_representation", "artefact_output_logits")},
                 "reading": "linear probe on held-out presenters (≥20 windows each), 50/50 split per presenter; above_chance = accuracy > max(chance, majority) + 0.05"}
    spans_example = {Path(path).name: spans(sorted(seq)) for path, seq in list(held_labels.items())[:3]}
    lora.save_pretrained(str(art / "lora_adapter"))
    torch.save({"head": head.state_dict(), "classes": codes, "window_seconds": WINDOW_SECONDS, "threshold": threshold, "vox_dim": vox_dim}, art / "head.pt")
    digest = hashlib.sha256()
    for f in sorted(p for p in art.rglob("*") if p.is_file()):
        digest.update(f.name.encode()); digest.update(bytes.fromhex(sha256_file(f)))
    condition_mix = {}
    for w in train_w:
        condition_mix.setdefault(codes[w[1]], {}); condition_mix[codes[w[1]]][w[6]] = condition_mix[codes[w[1]]].get(w[6], 0) + 1
    manifest = {"train_files": sorted({w[4] for w in train_w}), "held_files": sorted({w[4] for w in held_w}), "archive_test_files": sorted({w[4] for w in archive_w}),
                "windows": {"train": len(train_w), "held": len(held_w), "archive_test": len(archive_w)}, "split": split_summary,
                "train_condition_mix": condition_mix}
    manifest_text = json.dumps(manifest, sort_keys=True)
    (art / "training_manifest.json").write_text(manifest_text)
    per_lang_pass = {c: (r["accuracy"] is not None and r["accuracy"] >= 0.90) for c, r in held_report["per_language"].items() if r["windows"]}
    return {"classes": codes, "class_names": {c: LANGUAGES.get(c) for c in codes}, "trainable_parameters": trainable,
            "lora": {"r": int(control.get("lora_r", 16)), "target_modules": ["q_proj", "v_proj"], "base": reg["whisper-lid-v1-mit"]["repo"]},
            "fusion": f"Whisper encoder (LoRA) mean-pooled over the 2 s window ⊕ frozen VoxLingua107 ECAPA embedding ({vox_dim}-d) → linear head",
            "split": {"kind": "presenter-disjoint (biometric speaker linkage) for held-out; archive-only sessions as session-disjoint second test set"
                      if clusters else "session-local-speaker-disjoint (no speaker_linkage receipt on host); archive-only sessions as second test set",
                      "speaker_linkage_used": bool(clusters), "presenter_minimum_n_default": PRESENTER_MINIMUM_N, "per_language": split_summary,
                      "files": {"train": len(manifest["train_files"]), "held": len(manifest["held_files"]), "archive_test": len(manifest["archive_test_files"])},
                      "windows": manifest["windows"], "train_condition_mix_sample_rate": condition_mix,
                      "condition_reading": "source sample rate is the one measurable condition column (AIP §4.3); held-out accuracy is reported per condition so a rate-confound is visible, not hidden"},
            "training": {"steps": steps, "epochs_completed": epoch, "batch_size": batch, "lr": float(control.get("lr", 3e-4)),
                         "final_loss": round(float(np.mean(losses[-50:])), 4) if losses else None, "curve": curve,
                         "elapsed_seconds": round(time.time() - t0), "budget_seconds": budget, "device": device,
                         "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None,
                         "gpu_max_memory_gb": round(torch.cuda.max_memory_allocated() / 1e9, 2) if device == "cuda" else None,
                         "precision": "bf16 autocast" if device == "cuda" else "fp32"},
            "dp_sgd": dp,
            "held_out": held_report, "archive_test": archive_report, "no_speaker_id_probe": probe,
            "span_rule": {"window_seconds": WINDOW_SECONDS, "min_span_seconds": MIN_SPAN_SECONDS, "hysteresis_windows": HYSTERESIS_WINDOWS, "examples": spans_example},
            "artefact": {"path": str(art), "sha256": digest.hexdigest(), "training_manifest_sha256": hashlib.sha256(manifest_text.encode()).hexdigest(),
                         "custody": "RMS_TENANT · stays on akki-vm-ii · not admitted", "final_model": False,
                         "moac": {"per_language_accuracy_default": 0.90, "per_language_pass": per_lang_pass,
                                  "code_switch_span_accuracy_default": 0.85, "code_switch_material_present": False,
                                  "no_speaker_id_probe_passed": (probe.get("measured") and not probe["any_language_above_chance"]["artefact_output_logits"]) if probe.get("measured") else None,
                                  "abstention_reported": True,
                                  "verdict": "NOT ADMISSIBLE — MUST-NOT §1 (clean-monolingual only: no labelled code-switched spans); "
                                             "per-language and no-speaker-ID readings above are measured on presenter-disjoint material"}}}


def train_corrective(control, state):
    import fcntl
    from services.audio_plane_v1.corrective_training import train
    # A host-local allocation lock, not a new scheduler. A second owner of this GPU must refuse.
    with open(Path(control['root']) / f"corrective_gpu_{control['gpu_index']}.lock", 'w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        os.environ['CUDA_VISIBLE_DEVICES'] = str(control['gpu_index'])
        os.environ['HF_HUB_OFFLINE'] = '1'
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
        return train(control, state)


PHASES = {"corpus_census": corpus_census, "register_bases": register_bases, "speaker_linkage": speaker_linkage,
          "gate_eval": gate_eval, "train_baseline": train_baseline, "train_corrective": train_corrective}


def execute(control):
    """Entry point on the host: run one phase, write the receipt beside the job state."""
    state = State(control["job_dir"])
    state.update(phase=control["phase"], job_id=control["job_id"], hostname=socket.gethostname(), runtime_id=control["runtime_id"])
    receipt = {"protocol": "akki-language-cognition-v1", "job_id": control["job_id"], "phase": control["phase"],
               "runtime_id": control["runtime_id"], "hostname": socket.gethostname(), "started_at": state.doc["started_at"],
               "code_sha256": control["code_sha256"], "status": "failed"}
    try:
        if socket.gethostname() != control["hostname_expected"]:
            raise ValueError("HOST_IDENTITY_MISMATCH")
        receipt["result"] = PHASES[control["phase"]](control, state)
        receipt["status"] = "completed"
    except Exception as exc:
        receipt["error"] = {"type": type(exc).__name__, "message": str(exc)[:500], "trace": traceback.format_exc()[-3000:]}
    receipt["finished_at"] = now()
    body = json.dumps({k: v for k, v in receipt.items()}, sort_keys=True, default=str).encode()
    receipt["receipt_sha256"] = hashlib.sha256(body).hexdigest()
    path = Path(control["job_dir"]) / "receipt.json"
    path.write_text(json.dumps(receipt, indent=1, default=str))
    state.update(status=receipt["status"], finished_at=receipt["finished_at"], receipt_sha256=receipt["receipt_sha256"])
    return receipt
