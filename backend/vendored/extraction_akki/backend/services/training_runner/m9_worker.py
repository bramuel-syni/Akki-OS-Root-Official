"""M9 governed training worker — runs on the admitted GPU host, never on E1.

Modality-agnostic text path (Doc 17 A17.12 'modality-agnostic runner'): sealed corpus with per-example
provenance → test set sealed BEFORE training → calibration at several data volumes → two-arm optimizer
comparison (A17.5) → LoRA/PEFT run with checkpoint-resume → MOAC six-criteria card on the uncurated
held-out set → DAP-31 egress distance probe (canary exposure + verbatim extraction) → DAP-37 pruning pass
re-evaluated as a new artefact → DAP-38 training manifest. Nothing is admitted here; the receipt is read
back by E1 and routed through the existing admission ceremony.
"""
import fcntl
import hashlib
import json
import math
import os
import random
import re
import socket
import string
import time
import traceback
from pathlib import Path

LANGUAGES = {"kik": "Kikuyu", "swa": "Kiswahili", "luo": "Luo", "kln": "Kalenjin", "guz": "Kisii",
             "kam": "Kikamba", "lwg": "Luhya", "bxk": "Bukusu", "ebu": "Embu", "eng": "English"}
ABSTAIN_CONFIDENCE = 0.6
M_A_IMPROVEMENT_DEFAULT = 0.05      # MOAC M-a: beat the base by 5 points on the target strata (DEFAULT)
M_B_REGRESSION_TOLERANCE = 0.02     # MOAC M-b: non-target perplexity may not worsen by more than 2 % (DEFAULT)
PARITY_TOLERANCE = 0.005            # A17.5 quality parity band for the candidate optimizer (DEFAULT)
RPO_GPU_COMPUTE_SECONDS = 900       # BC Tier 1 (owner-ratified 2026-09-30 · 5a): never lose more than ~10–15 min of GPU compute
MTBF_BOOTSTRAP_SECONDS = 86400      # Young/Daly bootstrap MTBF until the host cluster has its own failure history
PER_STRATUM_RULING = "owner ruling 2026-09-30 (1a): per-stratum acceptance = held-out accuracy ≥ the Outcome's recorded floor AND no regression below the base (Docs 17–19 · §26.2)"


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def tree_sha256(directory, exclude=()):
    digest = hashlib.sha256()
    for f in sorted(p for p in Path(directory).rglob("*") if p.is_file() and p.name not in exclude):
        digest.update(str(f.relative_to(directory)).encode()); digest.update(bytes.fromhex(sha256_file(f)))
    return digest.hexdigest()


class State:
    """Progressive job state on the host volume; E1 reads it by one bounded RPC."""

    def __init__(self, job_dir):
        self.job_dir = Path(job_dir); self.job_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.job_dir / "state.json"
        self.doc = {"phase": None, "status": "running", "started_at": now(), "progress": {}, "stages": {}, "events": []}

    def update(self, **fields):
        self.doc.update(fields); self.doc["updated_at"] = now()
        tmp = self.path.with_suffix(".tmp"); tmp.write_text(json.dumps(self.doc, indent=1, default=str)); os.replace(tmp, self.path)

    def stage(self, name, summary):
        self.doc["stages"][name] = {"at": now(), **summary}; self.update()

    def event(self, message):
        self.doc["events"].append({"at": now(), "message": message[:400]}); self.update()


# ------------------------------------------------------------------ base acquisition (Doc 20 A20.1 · licence → checksum)
def _licence_from_card(model_dir):
    readme = Path(model_dir) / "README.md"
    if readme.exists():
        m = re.search(r"^license:\s*[\"']?([\w\.-]+)", readme.read_text(errors="ignore"), re.MULTILINE)
        if m:
            return m.group(1).lower()
    return None


def acquire_bases(control, state):
    """Pull licence-verified open bases into host custody; weight sha pinned at acquisition (A20.1, A17.11)."""
    from huggingface_hub import snapshot_download
    root = Path(control["root"]); (root / "hf_cache").mkdir(parents=True, exist_ok=True)
    reg_path = root / "base_registration.json"
    registration = json.loads(reg_path.read_text()) if reg_path.exists() else {}
    for entry in control["bases"]:
        state.event(f"acquiring {entry['repo']}")
        local = snapshot_download(entry["repo"], cache_dir=str(root / "hf_cache"), token=False,
                                  allow_patterns=["*.json", "*.safetensors", "*.txt", "*.md", "*.model", "*.tiktoken", "*.py"])
        weights = sorted(p for p in Path(local).rglob("*.safetensors") if p.is_file())
        if not weights:
            raise ValueError("NO_WEIGHTS_ACQUIRED:" + entry["repo"])
        digest = hashlib.sha256()
        for w in weights:
            digest.update(w.name.encode()); digest.update(bytes.fromhex(sha256_file(w)))
        licence = _licence_from_card(local)
        if licence != entry["expected_licence"].lower():
            raise ValueError(f"LICENCE_MISMATCH:{entry['repo']}:card={licence}:expected={entry['expected_licence']}")
        registration[entry["registry_id"]] = {
            "repo": entry["repo"], "revision": Path(local).name, "local_path": local, "licence_verified": licence,
            "weight_files": [w.name for w in weights], "weight_bytes": sum(w.stat().st_size for w in weights),
            "weight_sha256": digest.hexdigest(), "dimension": entry.get("dimension", "text"), "acquired_at": now()}
        reg_path.write_text(json.dumps(registration, indent=1))
    return {k: {kk: vv for kk, vv in v.items() if kk != "weight_files"} for k, v in registration.items()}


# ------------------------------------------------------------------ corpus assembly (qualified units → sealed split)
def _read_tsv_transcript(path):
    rows = []
    for line in Path(path).read_text(errors="ignore").splitlines():
        parts = line.split("\t")
        if len(parts) < 4:
            continue
        try:
            start, end = float(parts[0]), float(parts[1])
        except ValueError:
            continue
        rows.append((start, end, parts[2].strip(), parts[3].strip()))
    return rows


def _chunks(text, max_chars):
    words, out, cur = text.split(), [], ""
    for wd in words:
        if cur and len(cur) + 1 + len(wd) > max_chars:
            out.append(cur); cur = wd
        else:
            cur = f"{cur} {wd}".strip()
    if cur:
        out.append(cur)
    return out


def _normalise(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def _transcript_units(control, state):
    """Transcript text of the authorised local corpus: one unit per transcript turn (chunked), keyed to the
    same presenter linkage the audio plane uses, so text splits are presenter-disjoint too."""
    source = Path(control["source_root"])
    clusters_path = source / "speaker_clusters.json"
    clusters = json.loads(clusters_path.read_text())["clusters"] if clusters_path.exists() else {}
    origins_path = source / "sessions_index.json"
    origins = json.loads(origins_path.read_text()) if origins_path.exists() else {}
    corpus = source / "corpus" / "datasets"
    units, files = [], 0
    for code_dir in sorted(p for p in corpus.iterdir() if p.is_dir() and p.name in LANGUAGES):
        code = code_dir.name
        for session_dir in sorted(p for p in code_dir.iterdir() if (p / "transcript").is_dir()):
            session = session_dir.name
            for transcript in sorted((session_dir / "transcript").glob("*.txt")):
                files += 1
                for idx, (start, end, speaker, text) in enumerate(_read_tsv_transcript(transcript)):
                    presenter = f"{code}:{clusters.get(code, {}).get(f'{session}|{speaker}', f'{session}|{speaker}')}"
                    for part, chunk in enumerate(_chunks(text, control["max_chars"])):
                        if len(chunk) < control["min_chars"]:
                            continue
                        units.append({"text": chunk, "stratum": code, "group": presenter,
                                      "origin": origins.get(f"{code}/{session}", "folder"),
                                      "provenance": {"modality": "transcript_text", "file": str(transcript.relative_to(source)),
                                                     "turn": idx, "part": part, "start": start, "end": end, "speaker_local": speaker,
                                                     "language_label_source": "folder"}})
            if files % 200 == 0:
                state.update(progress={"stage": "reading transcripts", "files": files, "units": len(units)})
    return units, {"files": files}


def _digicow_units(control, state):
    """Sealed, independently inspected DIGICOW units (M3 verified result) — the only admissible DIGICOW material."""
    units = []
    for path in control["unit_files"]:
        for line in Path(path).read_text().splitlines():
            if not line.strip():
                continue
            unit = json.loads(line)
            record = unit.get("record") or {}
            question, answer = str(record.get("question") or "").strip(), str(record.get("answer") or "").strip()
            if not question or not answer:
                continue
            units.append({"text": f"Question: {question}\nAnswer: {answer}", "prompt": f"Question: {question}\nAnswer:",
                          "stratum": f"training_{record.get('training_id')}", "group": unit["unit_id"], "origin": "sealed_artefact",
                          "provenance": {"modality": "digicow_unit", "unit_id": unit["unit_id"], "artefact": str(path),
                                         "locator": (unit.get("provenance") or {}).get("locator"),
                                         "defensibility_class": (unit.get("defensibility") or {}).get("defensibility_class")}})
    # Small strata are folded so every stratum can carry a measured per-stratum result.
    counts = {}
    for u in units:
        counts[u["stratum"]] = counts.get(u["stratum"], 0) + 1
    for u in units:
        if counts[u["stratum"]] < control.get("min_stratum_units", 12):
            u["stratum"] = "training_other"
    return units, {"unit_files": len(control["unit_files"])}


def _assign_splits(units, held_fraction, seed):
    """Group-disjoint (presenter / unit) split per stratum: train / dev / held; archive origins → archive_test."""
    by_stratum = {}
    for i, u in enumerate(units):
        by_stratum.setdefault(u["stratum"], {}).setdefault(u["group"], []).append(i)
    assignment = [None] * len(units)
    for stratum in sorted(by_stratum):
        groups = sorted(by_stratum[stratum])
        archive = [g for g in groups if all(units[i]["origin"] == "archive" for i in by_stratum[stratum][g])]
        pool = [g for g in groups if g not in set(archive)]
        random.Random(f"{seed}:{stratum}").shuffle(pool)
        total = sum(len(by_stratum[stratum][g]) for g in pool)
        held, dev, n_held, n_dev = set(), set(), 0, 0
        for g in pool:
            if len(pool) - len(held) - len(dev) <= 1:
                break
            if n_held < held_fraction * total:
                held.add(g); n_held += len(by_stratum[stratum][g])
            elif n_dev < held_fraction * total / 2:
                dev.add(g); n_dev += len(by_stratum[stratum][g])
            else:
                break
        for g in groups:
            split = "archive_test" if g in set(archive) else "held" if g in held else "dev" if g in dev else "train"
            for i in by_stratum[stratum][g]:
                assignment[i] = split
    return assignment


def _canaries(count, seed):
    rnd = random.Random(f"canary:{seed}")
    alphabet = string.ascii_lowercase + string.digits
    return ["".join(rnd.choice(alphabet) for _ in range(12)) for _ in range(count)]


def assemble(control, state):
    """Qualified units → deduplicated, group-disjoint split, test set sealed BEFORE any training (A17.11)."""
    root = Path(control["root"]); out = root / "corpora" / control["corpus_id"]
    if (out / "manifest.json").exists() and not control.get("force", False):
        manifest = json.loads((out / "manifest.json").read_text())
        return {k: v for k, v in manifest.items() if k not in ("unit_ids",)} | {"reused_existing": True, "manifest_sha256": (out / "manifest.sha256").read_text().strip()}
    out.mkdir(parents=True, exist_ok=True)
    units, source_summary = (_transcript_units if control["kind"] == "transcript_text" else _digicow_units)(control, state)
    if not units:
        raise ValueError("NO_QUALIFIED_UNITS")
    state.update(progress={"stage": "deduplicating", "units": len(units)})
    seen, kept, duplicates = set(), [], 0
    for u in units:
        key = sha256_text(_normalise(u["text"]))
        if key in seen:
            duplicates += 1; continue
        seen.add(key); u["sha256"] = sha256_text(u["text"]); kept.append(u)
    units = kept
    assignment = _assign_splits(units, control["held_fraction"], control["seed"])
    for i, u in enumerate(units):
        u["split"] = assignment[i]; u["id"] = f"{control['corpus_id']}:{u['sha256'][:16]}"
    groups = {s: {u["group"] for u in units if u["split"] == s} for s in ("train", "dev", "held", "archive_test")}
    if any(groups[a] & groups[b] for a in groups for b in groups if a < b):
        raise ValueError("GROUP_OVERLAP_REFUSED")
    # DAP-31 canaries: inserted at known repetition counts; reference canaries are never trained on.
    canary_repeats = control.get("canary_repeats", [1, 2, 4])
    inserted = _canaries(control["canary_count"] * len(canary_repeats), control["seed"])
    reference = _canaries(control["canary_count"] * 4, control["seed"] + 1)
    canaries = []
    for n, secret in enumerate(inserted):
        repeats = canary_repeats[n % len(canary_repeats)]
        canaries.append({"secret": secret, "repeats": repeats})
        for r in range(repeats):
            units.append({"id": f"canary:{secret}:{r}", "text": f"The reference code is {secret}.", "stratum": "__canary__",
                          "group": f"canary:{secret}", "origin": "synthetic", "split": "train", "sha256": sha256_text(secret),
                          "provenance": {"modality": "synthetic_canary", "repeats": repeats}})
    (out / "canaries.json").write_text(json.dumps({"inserted": canaries, "reference": reference, "template": "The reference code is {secret}."}))
    with (out / "units.jsonl").open("w") as f:
        for u in units:
            f.write(json.dumps(u, ensure_ascii=False) + "\n")
    real = [u for u in units if u["stratum"] != "__canary__"]
    held_sorted = sorted((u for u in real if u["split"] == "held"), key=lambda u: u["id"])
    held_ids = [u["id"] for u in held_sorted]
    seal = {"corpus_id": control["corpus_id"], "held_unit_count": len(held_ids),
            "held_ids_sha256": sha256_text("\n".join(held_ids)),
            "held_text_sha256": sha256_text("\n".join(u["text"] for u in held_sorted)),
            "strata": sorted({u["stratum"] for u in real}), "sealed_at": now(), "rule": "sealed before any training step; never re-drawn"}
    (out / "test_set_seal.json").write_text(json.dumps(seal, indent=1))
    per = {}
    for u in real:
        row = per.setdefault(u["stratum"], {"train": 0, "dev": 0, "held": 0, "archive_test": 0, "groups_train": set(), "groups_held": set()})
        row[u["split"]] += 1
        if u["split"] in ("train", "held"):
            row[f"groups_{u['split']}"].add(u["group"])
    for row in per.values():
        row["groups_train"], row["groups_held"] = len(row["groups_train"]), len(row["groups_held"])
    manifest = {"corpus_id": control["corpus_id"], "kind": control["kind"], "rights_ref": control["rights_ref"],
                "source": source_summary, "units": len(real), "duplicates_removed": duplicates, "chars": sum(len(u["text"]) for u in real),
                "splits": {s: sum(1 for u in real if u["split"] == s) for s in ("train", "dev", "held", "archive_test")},
                "per_stratum": per, "test_set_seal": seal, "canaries": {"inserted": len(canaries), "repeats": canary_repeats, "reference": len(reference)},
                "unit_ids": {s: [u["id"] for u in real if u["split"] == s] for s in ("train", "dev", "held", "archive_test")},
                "assembled_at": now(), "split_rule": "group-disjoint per stratum (presenter for transcripts, unit for sealed records); archive sessions → archive_test"}
    text = json.dumps(manifest, sort_keys=True)
    (out / "manifest.json").write_text(text)
    manifest["manifest_sha256"] = sha256_text(text)
    (out / "manifest.sha256").write_text(manifest["manifest_sha256"])
    return {k: v for k, v in manifest.items() if k != "unit_ids"}


def load_corpus(root, corpus_id):
    out = Path(root) / "corpora" / corpus_id
    units = [json.loads(l) for l in (out / "units.jsonl").read_text().splitlines() if l.strip()]
    manifest = json.loads((out / "manifest.json").read_text())
    canaries = json.loads((out / "canaries.json").read_text())
    return units, manifest, canaries, (out / "manifest.sha256").read_text().strip()


# ------------------------------------------------------------------ Muon (A17.5 first named candidate)
def _newton_schulz(G, steps=5, eps=1e-7):
    import torch
    a, b, c = 3.4445, -4.7750, 2.0315
    X = G.to(torch.bfloat16); X = X / (X.norm() + eps)
    transposed = G.size(0) > G.size(1)
    if transposed:
        X = X.T
    for _ in range(steps):
        A = X @ X.T
        X = a * X + (b * A + c * A @ A) @ X
    return (X.T if transposed else X).to(G.dtype)


class Muon:
    """Momentum-orthogonalised update for 2-D parameters; AdamW for the rest. Reference algorithm, no download."""

    def __init__(self, params, lr, momentum=0.95, weight_decay=0.0, adamw_lr=None):
        import torch
        params = list(params)
        self.matrix = [p for p in params if p.ndim == 2]
        self.other = [p for p in params if p.ndim != 2]
        self.lr, self.momentum, self.weight_decay = lr, momentum, weight_decay
        self.buffers = [torch.zeros_like(p) for p in self.matrix]
        self.adamw = torch.optim.AdamW(self.other, lr=adamw_lr or lr, weight_decay=weight_decay) if self.other else None
        self.param_groups = [{"lr": lr, "params": self.matrix}] + (self.adamw.param_groups if self.adamw else [])
        self.base_lrs = [g["lr"] for g in self.param_groups]

    def zero_grad(self, set_to_none=True):
        for p in self.matrix:
            p.grad = None
        if self.adamw:
            self.adamw.zero_grad(set_to_none=set_to_none)

    def step(self):
        import torch
        with torch.no_grad():
            lr = self.param_groups[0]["lr"]
            for p, buf in zip(self.matrix, self.buffers):
                if p.grad is None:
                    continue
                buf.mul_(self.momentum).add_(p.grad)
                update = _newton_schulz(p.grad.add(buf, alpha=self.momentum))
                p.mul_(1 - lr * self.weight_decay)
                p.add_(update, alpha=-lr * max(1.0, p.size(0) / p.size(1)) ** 0.5)
        if self.adamw:
            self.adamw.step()

    def state_dict(self):
        return {"buffers": [b.cpu() for b in self.buffers], "adamw": self.adamw.state_dict() if self.adamw else None}

    def load_state_dict(self, sd):
        for b, saved in zip(self.buffers, sd["buffers"]):
            b.copy_(saved.to(b.device))
        if self.adamw and sd["adamw"]:
            self.adamw.load_state_dict(sd["adamw"])


# ------------------------------------------------------------------ model / data / evaluation
def _label_names(units):
    return {code: LANGUAGES.get(code, code) for code in sorted({u["stratum"] for u in units if u["stratum"] != "__canary__"})}


def _example_text(unit, task, labels):
    if task == "text_lid" and unit["stratum"] in labels:
        return f"Text: {unit['text']}\nLanguage: {labels[unit['stratum']]}"
    return unit["text"]


def _load_model(base, cfg, device):
    import torch
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(base["local_path"], local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(base["local_path"], dtype=torch.bfloat16, attn_implementation="sdpa", local_files_only=True)
    model.to(device)
    if cfg.get("gradient_checkpointing", True):  # measured on the H200: off = +35 % tokens/s for the 1.7B base within a bounded token budget
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    model.enable_input_require_grads()
    model.config.use_cache = False
    peft_model = get_peft_model(model, LoraConfig(r=cfg["lora_r"], lora_alpha=cfg["lora_alpha"], lora_dropout=cfg["lora_dropout"],
                                                  target_modules=cfg["target_modules"], bias="none", task_type="CAUSAL_LM"))
    return tokenizer, peft_model


def _tokenize(tokenizer, texts, max_len):
    enc = tokenizer([t + tokenizer.eos_token for t in texts], add_special_tokens=False, truncation=True, max_length=max_len)
    return enc["input_ids"]


WIDTH_STEPS = (16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512)


def _batches(ids, batch_size, seed, epoch, tokens_per_batch=0):
    """Length-sorted buckets. With a token budget every bucket is (indices, quantised width) with rows × width ≤ budget, so the run cycles
    through a handful of fixed tensor shapes — measured on the H200: per-step cuBLAS re-selection on ever-new shapes cost 3× the step time."""
    order = sorted(range(len(ids)), key=lambda i: len(ids[i]))
    if not tokens_per_batch:
        buckets = [(order[i:i + batch_size], None) for i in range(0, len(order), batch_size)]
    else:
        by_width = {}
        for i in order:
            width = next((w for w in WIDTH_STEPS if w >= len(ids[i])), len(ids[i]))
            by_width.setdefault(width, []).append(i)
        buckets = []
        for width, members in sorted(by_width.items()):
            rows = max(1, min(batch_size, tokens_per_batch // width))
            buckets.extend((members[i:i + rows], width) for i in range(0, len(members), rows))
    random.Random(f"{seed}:{epoch}").shuffle(buckets)
    return buckets


def _collate(ids, idx, pad, device, width=None):
    import torch
    longest = max(len(ids[i]) for i in idx)
    width = width or next((w for w in WIDTH_STEPS if w >= longest), longest)
    x = torch.full((len(idx), width), pad, dtype=torch.long)
    mask = torch.zeros((len(idx), width), dtype=torch.long)
    for r, i in enumerate(idx):
        x[r, :len(ids[i])] = torch.tensor(ids[i]); mask[r, :len(ids[i])] = 1
    labels = x.masked_fill(mask == 0, -100)
    return x.to(device), mask.to(device), labels.to(device)


def _per_unit_nll(model, tokenizer, ids, device, batch_size=16):
    """Mean next-token NLL and token accuracy per unit (teacher forced)."""
    import torch
    nll, acc = [None] * len(ids), [None] * len(ids)
    order = sorted(range(len(ids)), key=lambda i: len(ids[i]))
    for idx in [order[i:i + batch_size] for i in range(0, len(order), batch_size)]:
        x, mask, labels = _collate(ids, idx, tokenizer.pad_token_id, device)
        with torch.no_grad():
            logits = model(input_ids=x, attention_mask=mask).logits[:, :-1].float()
        target = labels[:, 1:]
        valid = (target != -100)
        lp = torch.log_softmax(logits, -1)
        tok = lp.gather(-1, target.clamp(min=0).unsqueeze(-1)).squeeze(-1)
        correct = (logits.argmax(-1) == target) & valid
        for r, i in enumerate(idx):
            n = int(valid[r].sum())
            nll[i] = float(-(tok[r] * valid[r]).sum() / max(1, n)); acc[i] = float(correct[r].sum() / max(1, n))
    return nll, acc


def _score_labels(model, tokenizer, prompts, labels, device, batch_size=16):
    """log p(label | prompt) for every label; returns [n][k] log-probs — the LID decision surface."""
    import torch
    scores = [[0.0] * len(labels) for _ in prompts]
    prompt_ids = tokenizer(prompts, add_special_tokens=False)["input_ids"]
    for k, label in enumerate(labels):
        label_ids = tokenizer(" " + label, add_special_tokens=False)["input_ids"]
        seqs = [p + label_ids for p in prompt_ids]
        order = sorted(range(len(seqs)), key=lambda i: len(seqs[i]))
        for idx in [order[i:i + batch_size] for i in range(0, len(order), batch_size)]:
            x, mask, _ = _collate(seqs, idx, tokenizer.pad_token_id, device)
            with torch.no_grad():
                lp = torch.log_softmax(model(input_ids=x, attention_mask=mask).logits[:, :-1].float(), -1)
            for r, i in enumerate(idx):
                start = len(prompt_ids[i]) - 1
                total = 0.0
                for j, t in enumerate(label_ids):
                    total += float(lp[r, start + j, t])
                scores[i][k] = total
    return scores


def evaluate(model, tokenizer, units, task, labels, device, cfg, tag):
    """Per-stratum measured results on a fixed, uncurated set: perplexity, (LID) accuracy with abstention, ECE."""
    import torch
    started = time.monotonic()
    texts = [_example_text(u, task, labels) for u in units]
    ids = _tokenize(tokenizer, texts, cfg["max_seq_len"])
    nll, tok_acc = _per_unit_nll(model, tokenizer, ids, device, cfg["eval_batch_size"])
    per = {}
    for u, n, a in zip(units, nll, tok_acc):
        row = per.setdefault(u["stratum"], {"units": 0, "nll": 0.0, "token_accuracy": 0.0})
        row["units"] += 1; row["nll"] += n; row["token_accuracy"] += a
    confidences, corrects = [], []
    if task == "text_lid":
        codes = list(labels)
        scores = _score_labels(model, tokenizer, [f"Text: {u['text']}\nLanguage:" for u in units], [labels[c] for c in codes], device, cfg["eval_batch_size"])
        for u, s in zip(units, scores):
            probs = torch.softmax(torch.tensor(s), -1)
            conf, pred = float(probs.max()), codes[int(probs.argmax())]
            row = per[u["stratum"]]
            row.setdefault("judged", 0); row.setdefault("correct", 0); row.setdefault("abstain", 0)
            if conf < ABSTAIN_CONFIDENCE:
                row["abstain"] += 1
            else:
                row["judged"] += 1; row["correct"] += int(pred == u["stratum"])
            confidences.append(conf); corrects.append(int(pred == u["stratum"]))
    for code, row in per.items():
        row["perplexity"] = round(math.exp(row["nll"] / row["units"]), 4); row["nll"] = round(row["nll"] / row["units"], 5)
        row["token_accuracy"] = round(row["token_accuracy"] / row["units"], 5)
        if "judged" in row:
            row["accuracy"] = round(row["correct"] / row["judged"], 5) if row["judged"] else None
            row["abstention_rate"] = round(row["abstain"] / row["units"], 5)
        else:
            row["accuracy"] = row["token_accuracy"]; row["abstention_rate"] = 0.0
    ece = None
    if confidences:
        bins = [[] for _ in range(10)]
        for c, y in zip(confidences, corrects):
            bins[min(9, int(c * 10))].append((c, y))
        ece = round(sum(abs(sum(c for c, _ in b) / len(b) - sum(y for _, y in b) / len(b)) * len(b) / len(confidences) for b in bins if b), 5)
    seconds = time.monotonic() - started
    return {"tag": tag, "units": len(units), "per_stratum": per, "mean_perplexity": round(math.exp(sum(nll) / max(1, len(nll))), 4),
            "macro_accuracy": round(sum(r["accuracy"] for r in per.values() if r["accuracy"] is not None) / max(1, sum(1 for r in per.values() if r["accuracy"] is not None)), 5),
            "min_stratum_accuracy": min((r["accuracy"] for r in per.values() if r["accuracy"] is not None), default=None),
            "ece": ece, "eval_seconds": round(seconds, 1), "seconds_per_unit_mean": round(seconds / max(1, len(units)), 5)}


def _sample(units, cap, seed):
    by = {}
    for u in units:
        by.setdefault(u["stratum"], []).append(u)
    out = []
    for stratum in sorted(by):
        rows = sorted(by[stratum], key=lambda u: u["id"]); random.Random(f"{seed}:{stratum}").shuffle(rows); out.extend(rows[:cap])
    return out


# ------------------------------------------------------------------ one training arm with checkpoint-resume
class InterruptForResumeProof(Exception):
    pass


def _digest_state(h, obj):
    if hasattr(obj, "detach"):
        h.update(obj.detach().cpu().float().numpy().tobytes())
    elif isinstance(obj, dict):
        for k in sorted(obj, key=str):
            h.update(str(k).encode()); _digest_state(h, obj[k])
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _digest_state(h, v)
    else:
        h.update(repr(obj).encode())


def _optimizer_digest(optimizer):
    h = hashlib.sha256(); _digest_state(h, optimizer.state_dict()); return h.hexdigest()


def _rng_digest():
    import numpy as np
    import torch
    h = hashlib.sha256()
    h.update(repr(random.getstate()).encode())
    np_state = np.random.get_state(); h.update(str(np_state[0]).encode()); h.update(np_state[1].tobytes()); h.update(repr(np_state[2:]).encode())
    h.update(torch.get_rng_state().numpy().tobytes())
    for s in torch.cuda.get_rng_state_all():
        h.update(s.numpy().tobytes())
    return h.hexdigest()


def _next_batch_digest(ids, cfg, epoch, batch_index):
    buckets = _batches(ids, cfg["batch_size"], cfg["seed"], epoch, cfg.get("tokens_per_batch", 0))
    return sha256_text(json.dumps(buckets[batch_index][0] if batch_index < len(buckets) else []))


RESUME_CARRIERS = ("weights", "optimizer", "scheduler", "data_offset", "rng")


def _carriers(model, optimizer, ids, cfg, step, epoch, batch_index):
    """BC Tier 1 five-carrier resume invariant (BC-1-GPU-INV-01/02): weights · optimizer · LR-scheduler step · data-pipeline offset · RNG."""
    return {"weights": _adapter_hash(model), "optimizer": _optimizer_digest(optimizer), "scheduler": {"step": step, "warmup_steps": cfg["warmup_steps"]},
            "data_offset": {"epoch": epoch, "batch_index": batch_index, "seed": cfg["seed"], "next_batch_sha256": _next_batch_digest(ids, cfg, epoch, batch_index)},
            "rng": _rng_digest()}


def _save_checkpoint(path, model, optimizer, step, epoch, batch_index, generator_seed, extra, ids=None, cfg=None):
    import numpy as np
    import torch
    from peft import get_peft_model_state_dict
    carriers = _carriers(model, optimizer, ids, cfg, step, epoch, batch_index) if ids is not None and cfg is not None else None
    state = {"adapter": {k: v.detach().cpu().float() for k, v in get_peft_model_state_dict(model).items()}, "optimizer": optimizer.state_dict(),
             "step": step, "epoch": epoch, "batch_index": batch_index, "generator_seed": generator_seed,
             "python_rng": random.getstate(), "numpy_rng": np.random.get_state(), "torch_rng": torch.get_rng_state(),
             "cuda_rng": torch.cuda.get_rng_state_all(), "carriers": carriers, **extra}
    tmp = path.with_suffix(".tmp"); torch.save(state, tmp); os.replace(tmp, path)
    return hashlib.sha256(b"".join(v.numpy().tobytes() for v in state["adapter"].values())).hexdigest()


def _load_checkpoint(path, model, optimizer, ids=None, cfg=None):
    """Restore all five carriers and prove it: a resume that cannot re-derive the saved carrier digests refuses (BC-1-GPU-INV-02)."""
    import numpy as np
    import torch
    from peft import set_peft_model_state_dict
    saved = torch.load(path, map_location="cpu", weights_only=False)
    set_peft_model_state_dict(model, saved["adapter"])
    optimizer.load_state_dict(saved["optimizer"])
    random.setstate(saved["python_rng"]); np.random.set_state(saved["numpy_rng"]); torch.set_rng_state(saved["torch_rng"])
    torch.cuda.set_rng_state_all(saved["cuda_rng"])
    parity = None
    if saved.get("carriers") and ids is not None and cfg is not None:
        live = _carriers(model, optimizer, ids, cfg, saved["step"], saved["epoch"], saved["batch_index"])
        parity = {k: live[k] == saved["carriers"][k] for k in RESUME_CARRIERS}
        if not all(parity.values()):
            raise ValueError("RESUME_CARRIER_MISMATCH:" + ",".join(k for k, ok in parity.items() if not ok))
    return saved, parity


def _adapter_hash(model):
    from peft import get_peft_model_state_dict
    return hashlib.sha256(b"".join(v.detach().cpu().float().numpy().tobytes() for v in get_peft_model_state_dict(model).values())).hexdigest()


def train_arm(cfg, base, train_units, eval_sets, task, labels, out_dir, state, tag, device="cuda"):
    """One governed LoRA arm: fixed data, recipe and budget; evaluates the base first, then the adapter."""
    import torch
    torch.manual_seed(cfg["seed"]); random.seed(cfg["seed"])
    tokenizer, model = _load_model(base, cfg, device)
    out_dir.mkdir(parents=True, exist_ok=True)
    eval_sets = {name: units for name, units in eval_sets.items() if units}
    texts = [_example_text(u, task, labels) for u in train_units]
    ids = _tokenize(tokenizer, texts, cfg["max_seq_len"])
    tokens_total = sum(len(i) for i in ids)
    with model.disable_adapter():
        model.eval()
        base_eval = {name: evaluate(model, tokenizer, units, task, labels, device, cfg, f"{tag}:base:{name}") for name, units in eval_sets.items()}
        model.train()
    params = [p for p in model.parameters() if p.requires_grad]
    if cfg["optimizer"] == "muon":
        optimizer = Muon(params, lr=cfg["muon_lr"], momentum=cfg["muon_momentum"], weight_decay=cfg["weight_decay"], adamw_lr=cfg["lr"])
    else:
        optimizer = torch.optim.AdamW(params, lr=cfg["lr"], weight_decay=cfg["weight_decay"], betas=(0.9, 0.95))
    steps_per_epoch = math.ceil(len(_batches(ids, cfg["batch_size"], cfg["seed"], 0, cfg.get("tokens_per_batch", 0))) / cfg["grad_accum"])
    total_steps = min(cfg["max_steps"], steps_per_epoch * cfg["epochs"]) if cfg.get("max_steps") else steps_per_epoch * cfg["epochs"]
    base_lrs = [g["lr"] for g in optimizer.param_groups]

    def set_lr(step):
        warm = cfg["warmup_steps"]
        scale = step / max(1, warm) if step < warm else 0.5 * (1 + math.cos(math.pi * (step - warm) / max(1, total_steps - warm)))
        for g, b in zip(optimizer.param_groups, base_lrs):
            g["lr"] = b * max(scale, 0.05)

    checkpoint = out_dir / "checkpoint.pt"
    cadence_receipts = out_dir / "checkpoint_cadence_receipt.jsonl"
    step, epoch, batch_index, resumed, curve, losses = 0, 0, 0, None, [], []
    if cfg.get("resume") and checkpoint.exists():
        saved, parity = _load_checkpoint(checkpoint, model, optimizer, ids, cfg)
        step, epoch, batch_index, curve = saved["step"], saved["epoch"], saved["batch_index"], saved.get("curve", [])
        resumed = {"from_step": step, "adapter_sha256": _adapter_hash(model), "carriers_restored": parity, "checkpoint_sha256": sha256_file(checkpoint)}
    elif cfg.get("resume"):
        raise ValueError("RESUME_CHECKPOINT_ABSENT:" + str(checkpoint))
    next_checkpoint_step = step + cfg["checkpoint_every"] if cfg["checkpoint_every"] else None
    durable_dir = Path(cfg["durable_checkpoint_dir"]) / out_dir.parent.name / out_dir.name if cfg.get("durable_checkpoint_dir") else None
    cadence = {"rule": cfg.get("checkpoint_cadence", "young_daly"), "rpo_seconds": RPO_GPU_COMPUTE_SECONDS, "mtbf_seconds": MTBF_BOOTSTRAP_SECONDS, "receipts": 0, "last": None}

    def checkpoint_now():
        """Write the checkpoint, replicate it to the durable tier if configured, then set the next boundary by Young/Daly τ ≈ √(2·C·MTBF), capped by the RPO."""
        t0 = time.monotonic()
        digest = _save_checkpoint(checkpoint, model, optimizer, step, epoch, batch_index, cfg["seed"], {"curve": curve, "tag": tag}, ids, cfg)
        write_seconds = time.monotonic() - t0
        replicate_seconds = None
        if durable_dir is not None:
            import shutil
            t1 = time.monotonic(); durable_dir.mkdir(parents=True, exist_ok=True)
            tmp = durable_dir / "checkpoint.pt.tmp"; shutil.copyfile(checkpoint, tmp); os.replace(tmp, durable_dir / "checkpoint.pt")
            replicate_seconds = time.monotonic() - t1
        cost = write_seconds + (replicate_seconds or 0.0)
        step_seconds = sum(step_times[-50:]) / max(1, len(step_times[-50:])) if step_times else None
        if cadence["rule"] == "young_daly" and step_seconds:
            tau = min(RPO_GPU_COMPUTE_SECONDS, math.sqrt(2 * max(cost, 1e-3) * MTBF_BOOTSTRAP_SECONDS))
            interval = max(1, int(tau / step_seconds))
        else:
            tau, interval = None, cfg["checkpoint_every"]
        receipt = {"at": now(), "step": step, "epoch": epoch, "checkpoint_adapter_sha256": digest, "write_seconds": round(write_seconds, 3), "replicate_seconds": None if replicate_seconds is None else round(replicate_seconds, 3),
                   "durable_copy": str(durable_dir / "checkpoint.pt") if durable_dir is not None else None, "step_seconds": None if step_seconds is None else round(step_seconds, 4),
                   "tau_seconds": None if tau is None else round(tau, 1), "next_checkpoint_step": step + interval, "rule": cadence["rule"], "rpo_seconds": RPO_GPU_COMPUTE_SECONDS, "mtbf_seconds": MTBF_BOOTSTRAP_SECONDS}
        with open(cadence_receipts, "a") as f:
            f.write(json.dumps(receipt) + "\n")
        cadence["receipts"] += 1; cadence["last"] = receipt
        return digest, step + interval

    started, trained_tokens, padded_tokens, step_times, gpu_seconds = time.monotonic(), 0, 0, [], 0.0
    interrupted = None
    torch.cuda.reset_peak_memory_stats()
    while step < total_steps:
        buckets = _batches(ids, cfg["batch_size"], cfg["seed"], epoch, cfg.get("tokens_per_batch", 0))
        while batch_index < len(buckets) and step < total_steps:
            t0 = time.monotonic()
            set_lr(step)
            for micro in range(cfg["grad_accum"]):
                if batch_index >= len(buckets):
                    break
                x, mask, y = _collate(ids, buckets[batch_index][0], tokenizer.pad_token_id, device, buckets[batch_index][1])
                loss = model(input_ids=x, attention_mask=mask, labels=y).loss / cfg["grad_accum"]
                if not torch.isfinite(loss):
                    raise ValueError("NONFINITE_LOSS")
                loss.backward(); losses.append(float(loss) * cfg["grad_accum"]); trained_tokens += int(mask.sum()); padded_tokens += x.numel(); batch_index += 1
            torch.nn.utils.clip_grad_norm_(params, cfg["max_grad_norm"])
            optimizer.step(); optimizer.zero_grad(set_to_none=True); step += 1
            step_times.append(time.monotonic() - t0)
            if step % 10 == 0 or step == 1:
                elapsed = time.monotonic() - started
                state.update(progress={"stage": f"training {tag}", "step": step, "total_steps": total_steps, "epoch": epoch + 1,
                                       "loss": round(sum(losses[-20:]) / len(losses[-20:]), 5), "tokens_per_second": round(trained_tokens / max(1e-6, elapsed), 1),
                                       "padded_tokens_per_step": round(padded_tokens / max(1, step)), "rows_last_step": len(buckets[batch_index - 1][0]),
                                       "recent_step_seconds": round(sum(step_times[-20:]) / len(step_times[-20:]), 3),
                                       "gpu_memory_gb": round(torch.cuda.max_memory_allocated() / 1e9, 2), "resumed": resumed, "elapsed_seconds": round(elapsed),
                                       "next_checkpoint_step": next_checkpoint_step, "last_checkpoint_step": (cadence["last"] or {}).get("step")})
            if next_checkpoint_step and step >= next_checkpoint_step:
                digest, next_checkpoint_step = checkpoint_now()
                if cfg.get("interrupt_after_steps") and step >= cfg["interrupt_after_steps"] and not resumed:
                    interrupted = {"at_step": step, "adapter_sha256_in_memory": _adapter_hash(model), "checkpoint_adapter_sha256": digest,
                                   "optimizer_state_sha256": _optimizer_digest(optimizer)}
                    raise InterruptForResumeProof(json.dumps(interrupted))
            if cfg["eval_every"] and step % cfg["eval_every"] == 0 and "dev" in eval_sets:
                model.eval(); dev = evaluate(model, tokenizer, eval_sets["dev"], task, labels, device, cfg, f"{tag}:dev@{step}"); model.train()
                curve.append({"step": step, "epoch": epoch + 1, "dev": {k: dev[k] for k in ("macro_accuracy", "min_stratum_accuracy", "mean_perplexity", "ece")}})
        if batch_index >= len(buckets):
            epoch += 1; batch_index = 0
    wall = time.monotonic() - started
    model.eval()
    final = {name: evaluate(model, tokenizer, units, task, labels, device, cfg, f"{tag}:adapter:{name}") for name, units in eval_sets.items()}
    adapter_dir = out_dir / "adapter"
    model.save_pretrained(str(adapter_dir))
    result = {"tag": tag, "base": {"registry_id": base["registry_id"], "weight_sha256": base["weight_sha256"]}, "recipe": {k: cfg[k] for k in RECIPE_KEYS if k in cfg},
              "train_units": len(train_units), "train_tokens": tokens_total, "steps": step, "epochs_completed": epoch, "total_steps_planned": total_steps,
              "wallclock_seconds": round(wall), "gpu_hours": round(wall / 3600, 4), "tokens_per_second": round(trained_tokens / max(1e-6, wall), 1),
              "padded_tokens_per_step": round(padded_tokens / max(1, step)), "padding_efficiency": round(trained_tokens / max(1, padded_tokens), 4),
              "gpu_max_memory_gb": round(torch.cuda.max_memory_allocated() / 1e9, 2), "final_loss": round(sum(losses[-20:]) / max(1, len(losses[-20:])), 5),
              "base_eval": base_eval, "adapter_eval": final, "dev_curve": curve, "resumed": resumed, "checkpoint_cadence": cadence,
              "adapter_sha256": _adapter_hash(model), "adapter_dir": str(adapter_dir), "device": torch.cuda.get_device_name(0)}
    return result, (model, tokenizer)


RECIPE_KEYS = ("optimizer", "lr", "muon_lr", "muon_momentum", "weight_decay", "epochs", "max_steps", "batch_size", "grad_accum", "max_seq_len", "tokens_per_batch", "gradient_checkpointing",
               "lora_r", "lora_alpha", "lora_dropout", "target_modules", "warmup_steps", "max_grad_norm", "seed", "checkpoint_every", "eval_every", "checkpoint_cadence", "durable_checkpoint_dir")
RECIPE_DEFAULTS = {"optimizer": "adamw", "lr": 2e-4, "muon_lr": 0.01, "muon_momentum": 0.95, "weight_decay": 0.01, "epochs": 1, "max_steps": 0,
                   "batch_size": 16, "grad_accum": 2, "max_seq_len": 384, "tokens_per_batch": 0, "gradient_checkpointing": True, "lora_r": 16, "lora_alpha": 32, "lora_dropout": 0.05,
                   "target_modules": ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"], "warmup_steps": 20,
                   "max_grad_norm": 1.0, "seed": 41, "checkpoint_every": 100, "eval_every": 0, "eval_batch_size": 16, "eval_cap_per_stratum": 400,
                   "checkpoint_cadence": "young_daly", "durable_checkpoint_dir": None}


def _recipe(control, **overrides):
    cfg = {**RECIPE_DEFAULTS, **{k: v for k, v in control.get("recipe", {}).items()}, **overrides}
    cfg["max_steps"] = cfg.get("max_steps") or 0
    return cfg


# ------------------------------------------------------------------ DAP-31 distance probe · DAP-37 pruning · MOAC card
def _lcs_ratio(a, b):
    """Longest common substring of two strings, normalised by the shorter length."""
    if not a or not b:
        return 0.0
    best, prev = 0, [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best / max(1, min(len(a), len(b)))


def distance_probe(model, tokenizer, train_units, held_units, canaries, cfg, device, out_dir):
    """DAP-31: no artefact egresses until it is measured to sit beyond a minimum distance from its training units."""
    import torch
    probe = cfg.get("distance_probe", {})
    samples, prefix_share, max_new = probe.get("samples", 120), probe.get("prefix_share", 0.4), probe.get("max_new_tokens", 48)
    memorised_ratio, verbatim_chars = probe.get("memorised_lcs_ratio", 0.75), probe.get("verbatim_chars_refuse", 100)
    tokenizer.padding_side = "left"

    def extraction(units, label):
        rows = sorted(units, key=lambda u: u["id"]); random.Random(f"probe:{label}").shuffle(rows); rows = rows[:samples]
        out = []
        for i in range(0, len(rows), cfg["eval_batch_size"]):
            chunk = rows[i:i + cfg["eval_batch_size"]]
            prompts = [u["text"][:max(8, int(len(u["text"]) * prefix_share))] for u in chunk]
            enc = tokenizer(prompts, return_tensors="pt", padding=True, add_special_tokens=False).to(device)
            with torch.no_grad():
                gen = model.generate(**enc, max_new_tokens=max_new, do_sample=False, pad_token_id=tokenizer.pad_token_id)
            for u, p, g in zip(chunk, prompts, gen):
                continuation = tokenizer.decode(g[enc["input_ids"].shape[1]:], skip_special_tokens=True)
                truth = u["text"][len(p):][:len(continuation) + 40]
                ratio = _lcs_ratio(_normalise(continuation), _normalise(truth))
                out.append({"id": u["id"], "lcs_ratio": round(ratio, 4), "verbatim_chars": int(ratio * min(len(_normalise(continuation)), len(_normalise(truth))))})
        share = sum(1 for r in out if r["lcs_ratio"] >= memorised_ratio) / max(1, len(out))
        return {"samples": len(out), "memorised_share": round(share, 4), "max_lcs_ratio": max((r["lcs_ratio"] for r in out), default=0.0),
                "max_verbatim_chars": max((r["verbatim_chars"] for r in out), default=0), "rows": out}

    train_probe = extraction([u for u in train_units if u["stratum"] != "__canary__"], "train")
    held_probe = extraction(held_units, "held")
    # Canary exposure (secret-sharer): rank of each inserted canary's likelihood among never-trained reference canaries.
    template = canaries["template"]
    ref_texts = [template.format(secret=s) for s in canaries["reference"]]
    ins_texts = [template.format(secret=c["secret"]) for c in canaries["inserted"]]
    tokenizer.padding_side = "right"
    nll_ref, _ = _per_unit_nll(model, tokenizer, _tokenize(tokenizer, ref_texts, 64), device, cfg["eval_batch_size"])
    nll_ins, _ = _per_unit_nll(model, tokenizer, _tokenize(tokenizer, ins_texts, 64), device, cfg["eval_batch_size"])
    exposures = []
    for c, n in zip(canaries["inserted"], nll_ins):
        rank = 1 + sum(1 for r in nll_ref if r <= n)
        exposures.append({"repeats": c["repeats"], "exposure_bits": round(math.log2(len(nll_ref) + 1) - math.log2(rank), 3), "rank": rank})
    by_repeat = {}
    for e in exposures:
        by_repeat.setdefault(e["repeats"], []).append(e["exposure_bits"])
    exposure_summary = {str(k): {"count": len(v), "mean": round(sum(v) / len(v), 3), "max": max(v)} for k, v in sorted(by_repeat.items())}
    max_bits = math.log2(len(nll_ref) + 1)
    extractable_floor = probe.get("extractable_exposure_bits", max_bits - 1.0)
    single_repeat_extractable = any(e["exposure_bits"] >= extractable_floor for e in exposures if e["repeats"] == 1)
    gap = train_probe["memorised_share"] - held_probe["memorised_share"]
    refusals = []
    if gap > probe.get("memorisation_gap_refuse", 0.05):
        refusals.append(f"memorisation gap {gap:.3f} exceeds {probe.get('memorisation_gap_refuse', 0.05)}")
    if train_probe["max_verbatim_chars"] >= verbatim_chars:
        refusals.append(f"verbatim reproduction of {train_probe['max_verbatim_chars']} chars >= {verbatim_chars}")
    if single_repeat_extractable:
        refusals.append("a once-seen canary is extractable (exposure at the top of the reference ranking)")
    result = {"method": "DAP-31 egress distance: greedy-continuation extraction on training vs held-out units + secret-sharer canary exposure",
              "train": {k: v for k, v in train_probe.items() if k != "rows"}, "held": {k: v for k, v in held_probe.items() if k != "rows"},
              "memorisation_gap": round(gap, 4), "canary_exposure_bits_by_repeats": exposure_summary, "canary_reference_count": len(nll_ref),
              "max_possible_exposure_bits": round(max_bits, 3), "extractable_exposure_floor_bits": round(extractable_floor, 3),
              "thresholds": {"memorised_lcs_ratio": memorised_ratio, "memorisation_gap_refuse": probe.get("memorisation_gap_refuse", 0.05),
                             "verbatim_chars_refuse": verbatim_chars, "class": "DEFAULT — disclosed, revisable on evidence"},
              "egress_permitted": not refusals, "refusals": refusals}
    (out_dir / "distance_probe_rows.json").write_text(json.dumps({"train": train_probe["rows"], "held": held_probe["rows"], "canaries": exposures}))
    return result


def prune_adapter(model, fraction):
    """DAP-37: magnitude-prune the LoRA delta; the pruned artefact is a new hash that must re-pass MOAC."""
    import torch
    zeroed, total = 0, 0
    with torch.no_grad():
        for name, p in model.named_parameters():
            if "lora_" in name and p.ndim == 2:
                k = int(p.numel() * fraction)
                if k:
                    threshold = p.abs().flatten().kthvalue(k).values
                    mask = p.abs() > threshold
                    zeroed += int((~mask).sum()); p.mul_(mask)
                total += p.numel()
    return {"fraction_requested": fraction, "weights_zeroed": zeroed, "adapter_weights": total, "sparsity": round(zeroed / max(1, total), 4)}


def moac_card(run_id, base_eval, adapter_eval, non_target_base, non_target_adapter, provenance_ok, gpu_seconds, eval_units, computed_at, outcome_floor):
    """Six MOAC criteria in the ModelAcceptanceCard_v0 shape; floors are the disclosed DEFAULTS, never curated.
    Per-stratum acceptance is the Outcome's recorded threshold plus no regression below the base (Docs 17–19; owner ruling 2026-09-30 1a);
    the +5-point M-a margin is the aggregate criterion (§26.1) and is not applied per stratum, where a fluent base makes it unreachable."""
    held_base, held = base_eval["held"], adapter_eval["held"]
    strata = [s for s in held["per_stratum"] if held["per_stratum"][s]["accuracy"] is not None]
    per_stratum_pass = {s: held["per_stratum"][s]["accuracy"] >= outcome_floor and held["per_stratum"][s]["accuracy"] >= (held_base["per_stratum"][s]["accuracy"] or 0) for s in strata}
    m_a = held["macro_accuracy"] - held_base["macro_accuracy"]
    regression = (non_target_adapter["mean_perplexity"] - non_target_base["mean_perplexity"]) / max(1e-9, non_target_base["mean_perplexity"])

    def crit(value, unit, method, floor, anchor):
        return {"measured_value": round(float(value), 6), "unit": unit, "method_of_measurement": method, "floor_value": floor, "canon_anchor": anchor}

    card = {"candidate_model_id": run_id, "evidence_source_kind": "uncurated_estate_sample", "evidence_purpose_id": f"m9-governed-training:{run_id}",
            "accuracy_uncurated": crit(held["macro_accuracy"], "accuracy_fraction", "Macro accuracy on the sealed, uncurated held-out set (group-disjoint), abstentions excluded from the judged count and reported separately.",
                                       round(held_base["macro_accuracy"] + M_A_IMPROVEMENT_DEFAULT, 6), "§26.1 · MOAC M-a improvement over base (+5 pts DEFAULT)"),
            "coverage_strata": crit(sum(per_stratum_pass.values()) / max(1, len(strata)), "fraction_of_strata_meeting_floor",
                                    f"Share of target strata whose held-out accuracy meets the Outcome's recorded per-stratum floor ({outcome_floor}) without regressing below the base. {PER_STRATUM_RULING}. gate_policy GATES release (A17.19b).",
                                    1.0, "§26.2 · per-stratum acceptance · Docs 17–19 threshold recorded on the Outcome"),
            "refusal_behaviour": crit(1.0 - regression, "one_minus_non_target_perplexity_regression", "Non-target held-out perplexity of the adapter relative to the base (MOAC M-b); reported abstention on the target set.",
                                      round(1.0 - M_B_REGRESSION_TOLERANCE, 6), "§26.3 · MOAC M-b no collateral regression (2 % DEFAULT)"),
            "provenance_integrity": crit(1.0 if provenance_ok else 0.0, "fraction", "Every training example resolves to a unit id in the sealed manifest; manifest sha verified at run open.", 1.0, "§26.4 · A17.16 ingredient manifest"),
            "cost_per_operation": crit(gpu_seconds / max(1, eval_units), "gpu_seconds_per_evaluated_unit", "Wall GPU seconds of the run divided by evaluated units (metering input; floor unset).", None, "§26.5"),
            "time_to_answer_p95": crit(held["seconds_per_unit_mean"], "seconds_per_unit_mean", "Mean evaluation latency per unit on the training host (p95 not yet instrumented; floor unset).", None, "§26.6"),
            "training_lineage_resolved": True, "training_lineage_note": "recipe + base weight sha + sealed corpus manifest sha recorded on the run receipt",
            "computed_at": computed_at}
    return card, {"m_a_improvement": round(m_a, 5), "m_b_non_target_regression": round(regression, 5), "per_stratum_pass": per_stratum_pass, "outcome_floor": outcome_floor,
                  "m_e_calibration_ece": held.get("ece"), "abstention_rate": {s: held["per_stratum"][s].get("abstention_rate") for s in strata}}


# ------------------------------------------------------------------ phases
def _base(control, registry_id):
    reg = json.loads((Path(control["root"]) / "base_registration.json").read_text())
    if registry_id not in reg:
        raise ValueError("BASE_NOT_ACQUIRED:" + registry_id)
    return {"registry_id": registry_id, **reg[registry_id]}


def _corpus_sets(control, cfg):
    root = Path(control["root"])
    units, manifest, canaries, manifest_sha = load_corpus(root, control["corpus_id"])
    excluded = set(control.get("excluded_unit_ids") or [])
    if excluded:  # rights withdrawn on a training dependency: the unit takes no part anywhere in the re-derivation (M9-T5)
        units = [u for u in units if u["id"] not in excluded]
    real = [u for u in units if u["stratum"] != "__canary__"]
    task = control.get("task", "text_lid" if manifest["kind"] == "transcript_text" else "text_lm")
    labels = _label_names(real)
    train = [u for u in units if u["split"] == "train"]
    eval_sets = {"dev": _sample([u for u in real if u["split"] == "dev"], cfg["eval_cap_per_stratum"], cfg["seed"]),
                 "held": _sample([u for u in real if u["split"] == "held"], cfg["eval_cap_per_stratum"], cfg["seed"])}
    archive = [u for u in real if u["split"] == "archive_test"]
    if archive:
        eval_sets["archive_test"] = _sample(archive, cfg["eval_cap_per_stratum"], cfg["seed"])
    non_target = []
    if control.get("non_target_corpus_id"):
        other, _, _, _ = load_corpus(root, control["non_target_corpus_id"])
        non_target = _sample([u for u in other if u["split"] == "held" and u["stratum"] != "__canary__"], cfg["eval_cap_per_stratum"], cfg["seed"])
    eval_sets["non_target"] = non_target or eval_sets["held"][:0]
    return units, manifest, canaries, manifest_sha, task, labels, train, eval_sets


def _fraction(train, fraction, seed):
    rows = sorted((u for u in train if u["stratum"] != "__canary__"), key=lambda u: u["id"]); random.Random(f"volume:{seed}").shuffle(rows)
    return rows[:max(1, int(len(rows) * fraction))] + [u for u in train if u["stratum"] == "__canary__"]


def _gpu_lock(control):
    lock = open(Path(control["root"]) / f"gpu_{control['gpu_index']}.lock", "w")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    os.environ["CUDA_VISIBLE_DEVICES"] = str(control["gpu_index"]); os.environ["HF_HUB_OFFLINE"] = "1"; os.environ["TRANSFORMERS_OFFLINE"] = "1"
    import torch
    torch.backends.cuda.matmul.allow_tf32 = True
    if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
        raise ValueError("M9_REQUIRES_ONE_RESERVED_VISIBLE_GPU")
    return lock


def _free(model_bundle):
    import gc
    import torch
    del model_bundle; gc.collect(); torch.cuda.empty_cache()


def _fit_curve(points):
    """acc = a + b·ln(volume) least squares; returns prediction at full volume with a ±2σ residual band."""
    xs = [math.log(v) for v, _ in points]; ys = [a for _, a in points]
    n = len(points)
    if n < 2:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    b = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / max(1e-12, sum((x - mx) ** 2 for x in xs))
    a = my - b * mx
    residual = math.sqrt(sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys)) / max(1, n - 2)) if n > 2 else 0.0
    pred = a + b * math.log(1.0)
    return {"a": round(a, 5), "b": round(b, 5), "predicted_full_volume": round(min(1.0, pred), 5),
            "interval_2sigma": [round(max(0.0, pred - 2 * residual), 5), round(min(1.0, pred + 2 * residual), 5)], "points": points}


def calibrate(control, state):
    """Mandatory first stage (§17.3): train at several data volumes per eligible base, fit the curve, quote with CI."""
    lock = _gpu_lock(control)
    try:
        cfg = _recipe(control, **control.get("calibration_recipe", {}))
        units, manifest, canaries, manifest_sha, task, labels, train, eval_sets = _corpus_sets(control, cfg)
        fractions = control.get("data_fractions", [0.125, 0.25, 0.5])
        out = Path(control["root"]) / "runs" / control["job_id"] / "calibration"
        runs, quotes = [], {}
        for registry_id in control["bases"]:
            base = _base(control, registry_id)
            cfg_b = {**cfg, **(control.get("base_recipes") or {}).get(registry_id, {})}  # measured per-base token budget / checkpointing
            points = {}
            for fraction in fractions:
                subset = _fraction(train, fraction, cfg["seed"])
                result, bundle = train_arm(cfg_b, base, subset, {"dev": eval_sets["dev"], "held": eval_sets["held"]}, task, labels,
                                           out / registry_id / f"v{fraction}", state, f"calibrate:{registry_id}:v{fraction}")
                _free(bundle)
                result.pop("dev_curve", None)
                runs.append({"base": registry_id, "fraction": fraction, **{k: result[k] for k in ("train_units", "train_tokens", "steps", "wallclock_seconds", "gpu_hours", "tokens_per_second", "gpu_max_memory_gb")},
                             "held": {s: (r["accuracy"], r["perplexity"]) for s, r in result["adapter_eval"]["held"]["per_stratum"].items()},
                             "held_macro_accuracy": result["adapter_eval"]["held"]["macro_accuracy"], "held_min_stratum": result["adapter_eval"]["held"]["min_stratum_accuracy"],
                             "base_macro_accuracy": result["base_eval"]["held"]["macro_accuracy"], "base_min_stratum": result["base_eval"]["held"]["min_stratum_accuracy"]})
                for s, r in result["adapter_eval"]["held"]["per_stratum"].items():
                    if r["accuracy"] is not None:
                        points.setdefault(s, []).append((fraction, r["accuracy"]))
                state.stage(f"calibration:{registry_id}:v{fraction}", {"held_macro": result["adapter_eval"]["held"]["macro_accuracy"], "gpu_hours": result["gpu_hours"]})
            curves = {s: _fit_curve(p) for s, p in points.items()}
            mine = [r for r in runs if r["base"] == registry_id]
            tps = [r["tokens_per_second"] for r in mine]
            mean_tps, sd_tps = sum(tps) / len(tps), (sum((t - sum(tps) / len(tps)) ** 2 for t in tps) / max(1, len(tps) - 1)) ** 0.5
            tokens_per_unit = sum(r["train_tokens"] for r in mine) / max(1, sum(r["train_units"] for r in mine))
            full_tokens = tokens_per_unit * len(train) * control.get("full_epochs", 2)
            quotes[registry_id] = {"curves": curves, "predicted_min_stratum_full": min((c["predicted_full_volume"] for c in curves.values() if c), default=None),
                                   "strata_predicted_to_clear": {s: c["predicted_full_volume"] >= (control.get("acceptance_floor", 0.90)) for s, c in curves.items() if c},
                                   "tokens_per_second": {"mean": round(mean_tps, 1), "sd": round(sd_tps, 1)},
                                   "full_run_gpu_hours_quote": {"estimate": round(full_tokens / max(1e-6, mean_tps) / 3600, 3),
                                                                "interval": [round(full_tokens / max(1e-6, mean_tps + 2 * sd_tps) / 3600, 3), round(full_tokens / max(1e-6, max(1.0, mean_tps - 2 * sd_tps)) / 3600, 3)],
                                                                "basis": f"{control.get('full_epochs', 2)} epochs over the full train split at the measured throughput; CI from ±2σ throughput"}}
        chosen = max(control["bases"], key=lambda b: ((quotes[b]["predicted_min_stratum_full"] or 0), -quotes[b]["full_run_gpu_hours_quote"]["estimate"]))
        milestones = [{"milestone": "corpus sealed", "done_condition": "manifest + test_set_seal on host before training", "owner": "training runner", "done": True},
                      {"milestone": "calibration curve", "done_condition": f"{len(fractions)} volumes × {len(control['bases'])} bases measured per stratum", "owner": "training runner", "done": True},
                      {"milestone": "optimizer parity", "done_condition": "two arms, identical conditions, M-a/M-b parity reported", "owner": "training runner", "done": False},
                      {"milestone": "full governed run", "done_condition": "adapter trained within the quoted GPU-hour band", "owner": "training runner", "done": False},
                      {"milestone": "MOAC on sealed held-out", "done_condition": "six criteria measured; per-stratum floors gate release", "owner": "admission ceremony", "done": False},
                      {"milestone": "DAP-31 egress distance", "done_condition": "extraction + canary probes within disclosed thresholds", "owner": "training runner", "done": False},
                      {"milestone": "DAP-37 pruned artefact", "done_condition": "pruned adapter re-measured as a new hash", "owner": "training runner", "done": False},
                      {"milestone": "registry admission", "done_condition": "admitted or refused on record; never auto-served", "owner": "admission ceremony", "done": False}]
        return {"corpus_id": control["corpus_id"], "manifest_sha256": manifest_sha, "task": task, "fractions": fractions, "runs": runs, "quotes": quotes,
                "base_selected_by_calibration": chosen, "selection_rule": "highest predicted minimum-stratum accuracy at full volume; ties → cheaper quote (A20.13)",
                "proposed_milestones": milestones, "recipe": {k: cfg[k] for k in RECIPE_KEYS if k in cfg}}
    finally:
        lock.close()


def compare_optimizers(control, state):
    """A17.5 two arms: baseline AdamW vs Muon, identical data, base, eval sets and budget, smallest valid stratum set."""
    lock = _gpu_lock(control)
    try:
        cfg = _recipe(control, **control.get("comparison_recipe", {}))
        units, manifest, canaries, manifest_sha, task, labels, train, eval_sets = _corpus_sets(control, cfg)
        subset = _fraction(train, control.get("comparison_fraction", 0.25), cfg["seed"])
        base = _base(control, control["base"])
        out = Path(control["root"]) / "runs" / control["job_id"] / "comparison"
        arms = {}
        for arm, optimizer in (("baseline", "adamw"), ("muon", "muon")):
            result, bundle = train_arm({**cfg, "optimizer": optimizer}, base, subset, {"dev": eval_sets["dev"], "held": eval_sets["held"], "non_target": eval_sets["non_target"]},
                                       task, labels, out / arm, state, f"compare:{arm}")
            _free(bundle)
            held, held_base = result["adapter_eval"]["held"], result["base_eval"]["held"]
            nt, nt_base = result["adapter_eval"].get("non_target"), result["base_eval"].get("non_target")
            regression = ((nt["mean_perplexity"] - nt_base["mean_perplexity"]) / nt_base["mean_perplexity"]) if nt else 0.0
            arms[arm] = {"optimizer": optimizer, "moac_m_a_improvement": round(held["macro_accuracy"] - held_base["macro_accuracy"], 5),
                         "moac_m_b_regression": round(regression, 5), "wallclock_seconds_to_convergence": result["wallclock_seconds"],
                         "gpu_hours_to_convergence": result["gpu_hours"], "moac_m_e_calibration": held.get("ece") if held.get("ece") is not None else 0.0,
                         "held_macro_accuracy": held["macro_accuracy"], "held_min_stratum": held["min_stratum_accuracy"], "final_loss": result["final_loss"],
                         "tokens_per_second": result["tokens_per_second"], "evaluation_samples_uncurated": True, "dev_curve": result["dev_curve"]}
            state.stage(f"comparison:{arm}", {k: arms[arm][k] for k in ("moac_m_a_improvement", "moac_m_b_regression", "gpu_hours_to_convergence")})
        b, m = arms["baseline"], arms["muon"]
        parity = m["moac_m_a_improvement"] >= b["moac_m_a_improvement"] - PARITY_TOLERANCE and m["moac_m_b_regression"] <= b["moac_m_b_regression"] + PARITY_TOLERANCE
        recommended = "adopted" if parity and m["gpu_hours_to_convergence"] <= b["gpu_hours_to_convergence"] and m["final_loss"] <= b["final_loss"] else "rejected"
        return {"corpus_id": control["corpus_id"], "manifest_sha256": manifest_sha, "base": control["base"], "comparison_fraction": control.get("comparison_fraction", 0.25),
                "train_units": len(subset), "arms": arms, "quality_parity": parity, "parity_tolerance": PARITY_TOLERANCE,
                "recommended_verdict": recommended, "recommendation_rule": "parity on M-a and M-b mandatory; adopt only if the candidate also converges in no more GPU-hours and to no higher loss",
                "recipe": {k: cfg[k] for k in RECIPE_KEYS if k in cfg}}
    finally:
        lock.close()


def train(control, state):
    """The governed run: sealed corpus → LoRA adapter → MOAC card → DAP-31 probe → DAP-37 pruned artefact → manifest."""
    lock = _gpu_lock(control)
    try:
        import torch
        cfg = _recipe(control)
        outcome_floor = control.get("acceptance_floor")
        if not isinstance(outcome_floor, (int, float)):
            raise ValueError("OUTCOME_PER_STRATUM_FLOOR_REQUIRED")  # Docs 17–19: an Outcome without a per-stratum acceptance threshold is rejected at definition
        units, manifest, canaries, manifest_sha, task, labels, train_units, eval_sets = _corpus_sets(control, cfg)
        if manifest_sha != sha256_text(json.dumps({k: v for k, v in manifest.items()}, sort_keys=True)):
            raise ValueError("CORPUS_MANIFEST_TAMPERED")
        base = _base(control, control["base"])
        run_job = control.get("resume_from_job_id") or control["job_id"]
        out = Path(control["root"]) / "runs" / run_job / "full"
        if control.get("resume_from_job_id"):
            cfg["resume"] = True  # physical process loss: the killed run's checkpoint on the host volume is the only continuation
        resume_proof = None
        try:
            result, bundle = train_arm(cfg, base, train_units, eval_sets, task, labels, out, state, "full")
        except InterruptForResumeProof as exc:
            interrupted = json.loads(str(exc))
            _free(None)
            state.event(f"interruption injected at step {interrupted['at_step']}; resuming from checkpoint")
            result, bundle = train_arm({**cfg, "resume": True}, base, train_units, eval_sets, task, labels, out, state, "full")
            resume_proof = {**interrupted, "resumed_adapter_sha256": result["resumed"]["adapter_sha256"],
                            "adapter_state_parity": result["resumed"]["adapter_sha256"] == interrupted["adapter_sha256_in_memory"],
                            "work_lost_steps": 0, "work_loss_bound_steps": cfg["checkpoint_every"], "resumed_from_step": result["resumed"]["from_step"], "kind": "in_process_exception"}
        if control.get("resume_from_job_id") and result.get("resumed"):
            resume_proof = {"kind": "physical_process_loss", "resumed_from_step": result["resumed"]["from_step"], "carriers_restored": result["resumed"]["carriers_restored"],
                            "checkpoint_sha256": result["resumed"]["checkpoint_sha256"], "resumed_adapter_sha256": result["resumed"]["adapter_sha256"], "killed_job_id": control["resume_from_job_id"]}
        model, tokenizer = bundle
        held_units = eval_sets["held"]
        nt_key = "non_target" if eval_sets.get("non_target") else "held"
        state.update(progress={"stage": "DAP-31 egress distance probe"})
        model.config.use_cache = True
        probe = distance_probe(model, tokenizer, train_units, held_units, canaries, cfg, "cuda", out)
        computed_at = now()
        card, moac_extra = moac_card(control["job_id"], result["base_eval"], result["adapter_eval"], result["base_eval"][nt_key],
                                     result["adapter_eval"][nt_key], True, result["wallclock_seconds"], len(held_units), computed_at, outcome_floor)
        state.update(progress={"stage": "DAP-37 pruning pass"})
        pruning = prune_adapter(model, control.get("prune_fraction", 0.3))
        model.eval()
        pruned_eval = {name: evaluate(model, tokenizer, us, task, labels, "cuda", cfg, f"pruned:{name}") for name, us in eval_sets.items() if us}
        pruned_dir = out / "pruned_adapter"; model.save_pretrained(str(pruned_dir))
        pruned_card, pruned_extra = moac_card(control["job_id"] + "-pruned", result["base_eval"], pruned_eval, result["base_eval"][nt_key],
                                              pruned_eval[nt_key], True, result["wallclock_seconds"], len(held_units), now(), outcome_floor)
        pruned_sha = _adapter_hash(model)
        training_manifest = {"artefact_id": control["job_id"], "corpus_id": control["corpus_id"], "corpus_manifest_sha256": manifest_sha, "rights_ref": manifest["rights_ref"],
                             "cited_units": sorted(u["id"] for u in train_units if u["stratum"] != "__canary__"), "was_sisa_sharded": False,
                             "excluded_unit_ids": sorted(control.get("excluded_unit_ids") or []), "rederived_from": control.get("rederived_from"),
                             "base": {"registry_id": base["registry_id"], "repo": base["repo"], "weight_sha256": base["weight_sha256"], "licence": base["licence_verified"]},
                             "recipe": result["recipe"], "guarantee": "provenance of ingredients only (A17.16); never provenance of assertions"}
        (out / "training_manifest.json").write_text(json.dumps(training_manifest, sort_keys=True))
        for name, payload in (("moac_card.json", card), ("moac_card_pruned.json", pruned_card), ("distance_probe.json", probe), ("recipe.json", result["recipe"])):
            (out / name).write_text(json.dumps(payload, indent=1))
        artefact_sha = tree_sha256(out / "adapter"); pruned_tree_sha = tree_sha256(pruned_dir)
        if pruned_tree_sha == artefact_sha:
            raise ValueError("PRUNED_ARTEFACT_HASH_COLLISION")
        _free(bundle)
        return {"corpus_id": control["corpus_id"], "task": task, "labels": labels, "manifest_sha256": manifest_sha, "corpus": {k: manifest[k] for k in ("units", "splits", "per_stratum", "test_set_seal", "rights_ref", "kind")},
                "training": {k: result[k] for k in ("train_units", "train_tokens", "steps", "epochs_completed", "total_steps_planned", "wallclock_seconds", "gpu_hours", "tokens_per_second", "gpu_max_memory_gb", "final_loss", "device", "recipe", "base")},
                "dev_curve": result.get("dev_curve", []), "base_eval": result["base_eval"], "adapter_eval": result["adapter_eval"],
                "moac": {"card": card, **moac_extra, "floors_class": f"DEFAULT (M-a +5 pts aggregate, M-b 2 %, per-stratum: Outcome floor {outcome_floor} + no regression below base) — disclosed, not curated"},
                "distance_probe": probe, "checkpoint": {"path": str(out / "checkpoint.pt"), "every_steps": cfg["checkpoint_every"], "cadence": result.get("checkpoint_cadence"), "rng_and_optimizer_saved": True, "resume_proof": resume_proof},
                "run_dir": str(out), "resume_from_job_id": control.get("resume_from_job_id"), "drill": bool(control.get("drill")),
                "pruning": {**pruning, "adapter_sha256": pruned_sha, "artefact_sha256": pruned_tree_sha, "eval": pruned_eval, "moac_card": pruned_card, **pruned_extra,
                            "anchor": "DAP-37: pruned artefact is a new hash; it must re-pass MOAC on its own numbers"},
                "artefact": {"path": str(out / "adapter"), "sha256": artefact_sha, "adapter_sha256": result["adapter_sha256"], "training_manifest_sha256": sha256_text((out / "training_manifest.json").read_text()),
                             "cited_units": len(training_manifest["cited_units"]), "custody": "tenant host only; nothing egresses without admission", "dp_sgd": {"applied": False, "reason": "optional arm per owner decision 3a; not commissioned in this run"}}}
    finally:
        lock.close()


def pipeline(control, state):
    """assemble → calibrate → compare optimizers → full run, one detached process; every stage result is retained."""
    stages = {}
    corpus = {**control, **control["assemble"]}
    stages["assemble"] = assemble(corpus, state); state.stage("assemble", {"units": stages["assemble"]["units"], "sha": stages["assemble"].get("manifest_sha256")})
    if control.get("non_target_assemble"):
        stages["assemble_non_target"] = assemble({**control, **control["non_target_assemble"]}, state)
    cal_control = {**control, **control["calibrate"], "corpus_id": corpus["corpus_id"]}
    stages["calibrate"] = calibrate(cal_control, state); state.stage("calibrate", {"base_selected": stages["calibrate"]["base_selected_by_calibration"]})
    base = stages["calibrate"]["base_selected_by_calibration"]
    cmp_control = {**control, **control["compare"], "corpus_id": corpus["corpus_id"], "base": base}
    stages["compare"] = compare_optimizers(cmp_control, state); state.stage("compare", {"verdict": stages["compare"]["recommended_verdict"]})
    optimizer = "muon" if stages["compare"]["recommended_verdict"] == "adopted" else "adamw"
    full_control = {**control, **control["train"], "corpus_id": corpus["corpus_id"], "base": base,
                    "acceptance_floor": control["train"].get("acceptance_floor", cal_control.get("acceptance_floor")),
                    "recipe": {**control.get("recipe", {}), **control["train"].get("recipe", {}), "optimizer": optimizer}}
    stages["train"] = train(full_control, state)
    return {"stages": stages, "base_selected": base, "optimizer_selected": optimizer}


# ------------------------------------------------------------------ M9.4 governed serving (registered artefact only · revocable · measured under load)
def _load_served(base, adapter_dir, device="cuda"):
    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(base["local_path"], local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(base["local_path"], dtype=torch.bfloat16, attn_implementation="sdpa", local_files_only=True).to(device)
    model = PeftModel.from_pretrained(model, str(adapter_dir), is_trainable=False)
    model.eval(); model.config.use_cache = False
    return tokenizer, model


def _percentiles(values):
    if not values:
        return None
    s = sorted(values)
    pick = lambda p: round(s[min(len(s) - 1, int(p * len(s)))], 4)
    return {"p50": pick(0.5), "p95": pick(0.95), "p99": pick(0.99), "max": round(s[-1], 4), "n": len(s)}


def serve(control, state):
    """Serve ONE registered artefact on the tenant host loopback: hash-verified at load, lineage on every answer, refusal the moment E1
    revokes the serving authority (revoked.json), stop on stop.json. The adapter hash is re-derived on health reads so load/precision
    pressure cannot silently alter the registered artefact (M9-T3)."""
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    import torch
    lock = _gpu_lock(control)
    try:
        root = Path(control["root"]); run_dir = Path(control["run_dir"])
        adapter_dir = run_dir / ("pruned_adapter" if control.get("variant") == "pruned" else "adapter")
        artefact_sha = tree_sha256(adapter_dir)
        if artefact_sha != control["artefact_sha256"]:
            raise ValueError("ARTEFACT_HASH_MISMATCH:registry=" + control["artefact_sha256"][:16] + ":host=" + artefact_sha[:16])
        manifest = json.loads((run_dir / "training_manifest.json").read_text())
        base = _base(control, manifest["base"]["registry_id"])
        if base["weight_sha256"] != manifest["base"]["weight_sha256"]:
            raise ValueError("BASE_WEIGHT_SHA_MISMATCH")
        labels = {code: LANGUAGES.get(code, code) for code in control["labels"]}
        codes = list(labels)
        state.update(progress={"stage": "loading registered artefact", "artefact_sha256": artefact_sha})
        tokenizer, model = _load_served(base, adapter_dir)
        loaded_sha = _adapter_hash(model)
        job_dir = Path(control["job_dir"]); revoked, stop = job_dir / "revoked.json", job_dir / "stop.json"
        authority = control["authority"]
        lineage = {"model_id": authority["model_id"], "artefact_sha256": artefact_sha, "registry_version": authority["registry_version"], "base": manifest["base"]["registry_id"],
                   "base_weight_sha256": manifest["base"]["weight_sha256"], "training_manifest_sha256": sha256_text((run_dir / "training_manifest.json").read_text()),
                   "corpus_manifest_sha256": manifest["corpus_manifest_sha256"], "cited_units": len(manifest["cited_units"]), "excluded_unit_ids": manifest.get("excluded_unit_ids", []),
                   "rederived_from": manifest.get("rederived_from"), "host": socket.gethostname(), "precision": "bfloat16 base · float32 adapter"}
        infer = threading.Lock()
        counters = {"served": 0, "refused": 0, "abstained": 0, "latency": [], "requests": 0}
        max_batch, max_chars, batch_size = int(control.get("max_batch", 64)), int(control.get("max_chars", 2000)), int(control.get("batch_size", 16))

        def classify(texts):
            with infer:
                scores = _score_labels(model, tokenizer, [f"Text: {t}\nLanguage:" for t in texts], [labels[c] for c in codes], "cuda", batch_size)
            out = []
            for s in scores:
                probs = torch.softmax(torch.tensor(s), -1); conf, pred = float(probs.max()), codes[int(probs.argmax())]
                out.append({"label": pred, "language": labels[pred], "confidence": round(conf, 5), "abstained": conf < ABSTAIN_CONFIDENCE})
            return out

        def revocation():
            try:
                return json.loads(revoked.read_text()) if revoked.exists() else None
            except ValueError:
                return {"reason": "revocation record unreadable; refusing by construction"}

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def _send(self, code, body):
                raw = json.dumps(body).encode()
                self.send_response(code); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(raw))); self.end_headers(); self.wfile.write(raw)

            def do_GET(self):
                if self.path != "/health":
                    return self._send(404, {"error": "not found"})
                rev = revocation()
                self._send(200, {"status": "revoked" if rev else "serving", "revocation": rev, **lineage, "loaded_adapter_sha256": loaded_sha, "adapter_sha256_now": _adapter_hash(model),
                                 "artefact_unaltered": _adapter_hash(model) == loaded_sha, "served_texts": counters["served"], "refused_requests": counters["refused"],
                                 "requests": counters["requests"], "abstained": counters["abstained"], "latency_seconds": _percentiles(counters["latency"][-2000:])})

            def do_POST(self):
                if self.path != "/classify":
                    return self._send(404, {"error": "not found"})
                counters["requests"] += 1
                try:
                    body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
                except ValueError:
                    return self._send(422, {"error": "body must be JSON"})
                rev = revocation()
                if rev:
                    counters["refused"] += 1
                    return self._send(403, {"refused": "SERVING_AUTHORITY_REVOKED", "revocation": rev, "model_id": lineage["model_id"]})
                texts = [str(t)[:max_chars] for t in (body.get("texts") or []) if str(t).strip()][:max_batch]
                if not texts:
                    return self._send(422, {"error": "texts required"})
                t0 = time.monotonic(); rows = classify(texts); dt = time.monotonic() - t0
                counters["served"] += len(texts); counters["abstained"] += sum(r["abstained"] for r in rows); counters["latency"].append(dt)
                self._send(200, {"results": rows, "lineage": lineage, "seconds": round(dt, 4)})

        server = ThreadingHTTPServer(("127.0.0.1", int(control["port"])), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        started = time.monotonic()
        state.update(progress={"stage": "serving", "port": control["port"], **lineage, "loaded_adapter_sha256": loaded_sha})
        state.stage("serving_started", {"port": control["port"], "artefact_sha256": artefact_sha, "loaded_adapter_sha256": loaded_sha})
        tick = 0
        while not stop.exists():
            time.sleep(2); tick += 1
            if tick % 15 == 0:
                state.update(progress={"stage": "serving", "port": control["port"], **lineage, "loaded_adapter_sha256": loaded_sha, "served_texts": counters["served"], "requests": counters["requests"],
                                       "refused_requests": counters["refused"], "revoked": revoked.exists(), "uptime_seconds": round(time.monotonic() - started)})
        server.shutdown()
        try:
            stop_reason = json.loads(stop.read_text()).get("reason")
        except ValueError:
            stop_reason = None
        return {**lineage, "loaded_adapter_sha256": loaded_sha, "adapter_sha256_at_stop": _adapter_hash(model), "artefact_unaltered": _adapter_hash(model) == loaded_sha,
                "requests": counters["requests"], "served_texts": counters["served"], "refused_requests": counters["refused"], "abstained": counters["abstained"],
                "latency_seconds": _percentiles(counters["latency"]), "uptime_seconds": round(time.monotonic() - started), "stop_reason": stop_reason, "revoked_at_stop": revocation()}
    finally:
        lock.close()


def load_test(control, state):
    """Measured quality under load (M9-T3/M9.4): sequential baseline labels on sealed held-out texts, then concurrent batched requests to the
    same loopback server; reports latency percentiles, throughput, label determinism versus the sequential baseline and artefact-hash constancy."""
    import threading
    import urllib.error
    import urllib.request
    root = Path(control["root"])
    units, _manifest, _c, _sha = load_corpus(root, control["corpus_id"])
    seed = control.get("seed", 41)
    held = _sample([u for u in units if u["split"] == "held" and u["stratum"] != "__canary__"], int(control.get("per_stratum", 30)), seed)
    url = f"http://127.0.0.1:{int(control['port'])}"

    def call(texts):
        req = urllib.request.Request(url + "/classify", data=json.dumps({"texts": texts}).encode(), headers={"Content-Type": "application/json"}, method="POST")
        t0 = time.monotonic()
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                body, code = json.loads(r.read()), r.status
        except urllib.error.HTTPError as e:
            body, code = json.loads(e.read() or b"{}"), e.code
        return code, body, time.monotonic() - t0

    state.update(progress={"stage": "sequential baseline", "units": len(held)})
    baseline, base_latency = {}, []
    for u in held:
        code, body, dt = call([u["text"]]); base_latency.append(dt)
        baseline[u["id"]] = body["results"][0]["label"] if code == 200 else None
    concurrency, per_thread, batch = int(control.get("concurrency", 8)), int(control.get("requests_per_thread", 20)), int(control.get("batch", 8))
    rows, guard = [], threading.Lock()

    def worker(k):
        rng = random.Random(f"{seed}:{k}")
        for _ in range(per_thread):
            picked = rng.sample(held, min(len(held), batch))
            code, body, dt = call([u["text"] for u in picked])
            pairs = [(u["id"], u["stratum"], r["label"]) for u, r in zip(picked, body.get("results", []))] if code == 200 else []
            with guard:
                rows.append({"code": code, "seconds": dt, "pairs": pairs, "sha": (body.get("lineage") or {}).get("artefact_sha256")})

    state.update(progress={"stage": "concurrent load", "concurrency": concurrency, "requests": concurrency * per_thread})
    threads = [threading.Thread(target=worker, args=(k,)) for k in range(concurrency)]
    t0 = time.monotonic()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    wall = time.monotonic() - t0
    ok = [r for r in rows if r["code"] == 200]
    pairs = [p for r in ok for p in r["pairs"]]
    mismatches = sum(1 for uid, _s, lab in pairs if baseline.get(uid) != lab)
    correct = sum(1 for _u, s, lab in pairs if s == lab)
    shas = sorted({r["sha"] for r in ok if r["sha"]})
    return {"port": int(control["port"]), "sample_units": len(held), "sequential": {"requests": len(held), "latency_seconds": _percentiles(base_latency),
                                                                                  "accuracy": round(sum(1 for u in held if baseline.get(u["id"]) == u["stratum"]) / max(1, len(held)), 5)},
            "load": {"concurrency": concurrency, "requests_per_thread": per_thread, "batch": batch, "requests": len(rows), "ok": len(ok), "errors": len(rows) - len(ok),
                     "wall_seconds": round(wall, 2), "texts_per_second": round(len(pairs) / max(1e-6, wall), 2), "latency_seconds": _percentiles([r["seconds"] for r in rows]),
                     "accuracy_under_load": round(correct / max(1, len(pairs)), 5)},
            "determinism": {"labels_compared": len(pairs), "label_mismatches_vs_sequential": mismatches, "identical": mismatches == 0},
            "artefact_sha256_constant": len(shas) == 1, "artefact_sha256_seen": shas, "error_codes": sorted({r["code"] for r in rows if r["code"] != 200})}


PHASES = {"acquire_bases": acquire_bases, "assemble": assemble, "calibrate": calibrate, "compare_optimizers": compare_optimizers, "train": train, "pipeline": pipeline,
          "serve": serve, "load_test": load_test}


def execute(control):
    state = State(control["job_dir"])
    state.update(phase=control["phase"], job_id=control["job_id"], hostname=socket.gethostname(), runtime_id=control["runtime_id"])
    receipt = {"protocol": "akki-m9-governed-training-v1", "job_id": control["job_id"], "phase": control["phase"], "runtime_id": control["runtime_id"],
               "hostname": socket.gethostname(), "started_at": state.doc["started_at"], "code_sha256": control["code_sha256"], "status": "failed"}
    try:
        if socket.gethostname() != control["hostname_expected"]:
            raise ValueError("HOST_IDENTITY_MISMATCH")
        if control['phase'] == 'lab_inspect':
            from services.training_lab.inspection_worker import inspect_corpus
            receipt['result'] = inspect_corpus(control, state)
        elif control['phase'] == 'lab_measure':
            from services.training_lab.measurement_worker import measure_corpus
            receipt['result'] = measure_corpus(control, state)
        elif control['phase'] == 'lab_train_music':
            os.environ['CUDA_VISIBLE_DEVICES'] = str(control['gpu_index'])
            from services.training_lab.music_detector_worker import train_music_detector
            receipt['result'] = train_music_detector(control, state)
        elif control['phase'] == 'lab_classify_estate':
            from services.training_lab.estate_language_worker import classify_estate
            receipt['result'] = classify_estate(control, state)
        elif control['phase'] == 'lab_text_lid':
            from services.training_lab.estate_language_worker import classify_text
            receipt['result'] = classify_text(control, state)
        elif control['phase'] == 'serve_reader':
            from services.training_runner.reader_worker import serve_reader
            receipt['result'] = serve_reader(control, state)
        elif control['phase'].startswith('malpha_'):
            os.environ['CUDA_VISIBLE_DEVICES'] = str(control['gpu_index'])
            from services.training_lab import malpha_worker as mw
            from services.training_lab import malpha_voice_worker as mv
            from services.training_lab.malpha_worker_audit import audit
            from services.training_lab.malpha_corpus_audit import audit as corpus_audit
            fn = {'malpha_aip_build': mw.aip_build, 'malpha_aip_requalify': mw.aip_requalify, 'malpha_aip_relabel': mw.aip_relabel, 'malpha_aip_reseal': mw.aip_reseal, 'malpha_internet_corpus': mw.internet_corpus, 'malpha_listener_train': mw.listener_train, 'malpha_evaluate': mw.evaluate_admission,
                  'malpha_story_text_train': mv.story_text_train, 'malpha_voice_train': mv.voice_train, 'malpha_baseline_render': mv.baseline_render, 'malpha_worker_audit': audit, 'malpha_corpus_audit': corpus_audit}[control['phase']]
            receipt['result'] = fn(control, state)
        else:
            receipt["result"] = PHASES[control["phase"]](control, state)
        receipt["status"] = "completed"
    except Exception as exc:
        receipt["error"] = {"type": type(exc).__name__, "message": str(exc)[:500], "trace": traceback.format_exc()[-3000:]}
        receipt["stages_completed"] = state.doc.get("stages")
    receipt["finished_at"] = now()
    body = json.dumps(receipt, sort_keys=True, default=str).encode()
    receipt["receipt_sha256"] = hashlib.sha256(body).hexdigest()
    (Path(control["job_dir"]) / "receipt.json").write_text(json.dumps(receipt, indent=1, default=str))
    state.update(status=receipt["status"], finished_at=receipt["finished_at"], receipt_sha256=receipt["receipt_sha256"])
    return receipt
