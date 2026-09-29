"""Offline tests of the language-cognition worker's pure parsers and rules (the shipped bundle code).
No estate bytes, no GPU: synthetic layouts only."""
import json
import tarfile

import numpy as np
import pytest

from services.audio_plane_v1 import language_cognition_worker as w


class _Sdk:
    def __init__(self, pages):
        self.pages = pages

    def list_objects_v2(self, **kwargs):
        page = self.pages[kwargs.get("ContinuationToken", 0)]
        nxt = kwargs.get("ContinuationToken", 0) + 1
        return {"Contents": page, "IsTruncated": nxt < len(self.pages), "NextContinuationToken": nxt}


def test_list_objects_skips_prefix_marker_objects_and_paginates():
    sdk = _Sdk([[{"Key": "datasets/kik/S1", "Size": 0}, {"Key": "datasets/kik/S1/audio/1.wav", "Size": 10}],
                [{"Key": "datasets/kik/", "Size": 0}, {"Key": "datasets/kik/S1.tar.xz", "Size": 5}, {"Key": "datasets/kik/manifest.tsv", "Size": 0}]])
    objects, markers = w.list_objects(sdk, "b", "datasets/")
    assert objects == [("datasets/kik/S1/audio/1.wav", 10), ("datasets/kik/S1.tar.xz", 5), ("datasets/kik/manifest.tsv", 0)]
    assert markers == 2


def test_classify_objects_reads_session_layout_archives_and_pairing():
    objects = [("datasets/kik/S1/audio/1.wav", 100), ("datasets/kik/S1/transcript/1.txt", 5), ("datasets/kik/S1/metadata/1.tsv", 3),
               ("datasets/kik/S1.tar.xz", 40), ("datasets/kik/S2.tar.xz", 40), ("datasets/kik/manifest.tsv", 1), ("datasets/kik/S3/audio/9.wav", 7),
               ("datasets/validation/kik.xlsx", 2)]
    per = w.classify_objects(objects)
    kik = per["kik"]
    assert kik["audio"] == {"objects": 2, "bytes": 107, "extensions": {".wav": 2}}
    assert kik["archives"] == {"objects": 2, "bytes": 80} and kik["manifests"] == 1
    assert kik["session_count"] == 2 and kik["archive_only_sessions"] == 1
    assert kik["pairing"] == {"matched_pairs": 1, "audio_without_transcript": 1, "transcript_without_audio": 0}
    assert per["_unclassified"] == {"objects": 1, "bytes": 2, "sample_keys": ["datasets/validation/kik.xlsx"]}


def test_read_segments_and_metadata(tmp_path):
    t = tmp_path / "1.txt"
    t.write_text("0.0\t3.5\tSpeaker_1_f\thello\nbad\tline\n4.0\tx\tSpeaker_2_m\tno\n4.0\t6.0\tSpeaker_2_m\tworld\ttrailing\n")
    assert w.read_segments(t) == [(0.0, 3.5, "Speaker_1_f", "hello"), (4.0, 6.0, "Speaker_2_m", "world")]
    m = tmp_path / "1.tsv"
    m.write_text("VENDOR_NAME\tPROJECT_NAME\tSPEAKER_ID\tLOCALE\tGENDER\tAGE\tDEVICE\tENVIRONMENT\tYEAR\nrms\t2022\tSpeaker_1_f\tkik_ke\tfemale\t\t\t\t\n")
    assert w.read_metadata(m) == {"Speaker_1_f": {"gender": "female", "age": None, "device": None, "environment": None, "locale": "kik_ke"}}
    assert w.read_metadata(tmp_path / "missing.tsv") == {}


def test_speech_windows_stay_inside_speech_and_carry_speaker():
    segs = [(0.0, 5.0, "A", ""), (10.0, 12.5, "B", ""), (20.0, 21.0, "C", "")]
    out = w.speech_windows(segs, 30 * w.SAMPLE_RATE, 100)
    starts = [(s / w.SAMPLE_RATE, spk) for s, spk in out]
    assert starts == [(0.0, "A"), (2.0, "A"), (10.0, "B")]           # 1 s segment yields no 2 s window
    capped = w.speech_windows(segs, 30 * w.SAMPLE_RATE, 2, seed=1)
    assert len(capped) == 2 and capped == sorted(capped)
    assert w.speech_windows(segs, 3 * w.SAMPLE_RATE, 10) == [(0, "A")]  # audio shorter than the transcript


def test_span_rule_hysteresis_and_min_span():
    seq = [(0.0, "kik", 0.9), (2.0, "kik", 0.9), (4.0, "swa", 0.8), (6.0, "kik", 0.9), (8.0, "kik", 0.9),
           (10.0, "swa", 0.8), (12.0, "swa", 0.8), (14.0, "swa", 0.8)]
    result = w.spans(seq)
    assert result == [{"start": 0.0, "end": 12.0, "label": "kik"}, {"start": 10.0, "end": 16.0, "label": "swa"}]
    assert w.spans([(0.0, "kik", 0.9)], min_span=2.5) == [{"start": 0.0, "end": 2.0, "label": "unmeasured"}]
    assert (w.MIN_SPAN_SECONDS, w.HYSTERESIS_WINDOWS) == (0.5, 2)


def test_split_by_presenter_holds_out_whole_presenters_and_archive_sessions():
    items = [("kik", "kik:1", "folder")] * 30 + [("kik", "kik:2", "folder")] * 30 + [("kik", "kik:3", "folder")] * 40 \
        + [("kik", "kik:9", "archive")] * 10 + [("swa", "swa:1", "folder")] * 5
    assignment, summary = w.split_by_presenter(items)
    by_presenter = {}
    for n, (code, presenter, origin) in enumerate(items):
        by_presenter.setdefault(presenter, set()).add(assignment[n])
    assert all(len(v) == 1 for v in by_presenter.values())              # no presenter straddles train/held
    assert by_presenter["kik:9"] == {"archive_test"}
    assert summary["kik"]["presenters_held"] >= 1 and summary["kik"]["presenters_train"] >= 1
    assert summary["kik"]["windows_train"] + summary["kik"]["windows_held"] == 100 and summary["kik"]["windows_archive_test"] == 10
    assert summary["swa"] == {"presenters_train": 1, "presenters_held": 0, "windows_train": 5, "windows_held": 0, "windows_archive_test": 0,
                              "meets_presenter_minimum_n": False}


def test_speaker_crops_take_longest_segments_only():
    audio = np.zeros(60 * w.SAMPLE_RATE, dtype=np.float32)
    segs = [(0.0, 1.0, "A", ""), (2.0, 6.0, "A", ""), (10.0, 12.0, "A", ""), (20.0, 30.0, "B", "")]
    crops = w.speaker_crops(segs, audio, per_speaker=1)
    assert set(crops) == {"A", "B"} and crops["A"][0].shape[0] == 3 * w.SAMPLE_RATE
    assert len(w.speaker_crops(segs, audio, per_speaker=5)["A"]) == 2      # the 1 s segment is below min_seconds


def test_cluster_presenters_links_similar_voices():
    pytest.importorskip("scipy")
    a = np.array([1.0, 0.0, 0.0]); b = np.array([0.98, 0.2, 0.0]); c = np.array([0.0, 1.0, 0.0])
    labels = w.cluster_presenters([a / np.linalg.norm(a), b / np.linalg.norm(b), c], threshold=0.45)
    assert labels[0] == labels[1] != labels[2]
    assert w.cluster_presenters([a], 0.45) == [1]


def _session(root, code, session, ids, transcript=True):
    for i in ids:
        (root / code / session / "audio").mkdir(parents=True, exist_ok=True)
        (root / code / session / "audio" / f"{i}.wav").write_bytes(b"RIFF")
        if transcript:
            (root / code / session / "transcript").mkdir(exist_ok=True)
            (root / code / session / "transcript" / f"{i}.txt").write_text("0.0\t4.0\tSpeaker_1_m\thi\n")


def test_extract_archives_unpacks_archive_only_sessions_and_indexes_origin(tmp_path):
    corpus = tmp_path / "corpus" / "datasets"
    _session(corpus, "kik", "S_folder", ["1"])
    staging = tmp_path / "build" / "S_archive"
    _session(tmp_path / "build", "", "S_archive", ["2"])
    with tarfile.open(corpus / "kik" / "S_archive.tar.xz", "w:xz") as tar:
        for child in ("audio", "transcript"):
            tar.add(staging / child, arcname=child)
    with tarfile.open(corpus / "kik" / "S_folder.tar.xz", "w:xz") as tar:
        tar.add(corpus / "kik" / "S_folder" / "audio", arcname="audio")
    report = w.extract_archives(tmp_path, state=None, parallelism=2)
    assert report["extracted_this_run"] == 1 and report["failed_count"] == 0
    assert (corpus / "kik" / "S_archive" / "audio" / "2.wav").exists()
    index = json.loads((tmp_path / "sessions_index.json").read_text())
    assert index == {"kik/S_archive": "archive", "kik/S_folder": "folder+archive"}
    assert report["session_origins"] == {"archive": 1, "folder+archive": 1}
    assert w._corpus_files(tmp_path, origins_allowed={"archive"}) == {"kik": [corpus / "kik" / "S_archive" / "audio" / "2.wav"]}
    assert w.extract_archives(tmp_path, state=None)["extracted_this_run"] == 0   # idempotent


def test_measure_staged_reads_corpus_as_database(tmp_path):
    corpus = tmp_path / "corpus" / "datasets"
    _session(corpus, "kik", "S1", ["1", "2"])
    _session(corpus, "swa", "S9", ["5"], transcript=False)
    (corpus / "kik" / "S1" / "metadata").mkdir()
    (corpus / "kik" / "S1" / "metadata" / "1.tsv").write_text("VENDOR_NAME\tSPEAKER_ID\tGENDER\tAGE\tDEVICE\tENVIRONMENT\nrms\tSpeaker_1_m\tmale\t\t\t\n")
    out = w.measure_staged(tmp_path)
    kik = out["kik"]
    assert kik["audio_files"] == 2 and kik["unreadable_audio"] == 2 and kik["segments"] == 2 and kik["speech_hours"] == round(8 / 3600, 2)
    assert kik["session_local_speaker_ids"] == 1 and kik["speakers_with_gender_suffix"] == 2
    assert kik["metadata_gender"] == {"male": 1} and kik["metadata_condition_cells_filled"] == 0
    assert out["swa"]["transcribed_files"] == 0
    files = [json.loads(l) for l in (tmp_path / "corpus_db" / "files.jsonl").read_text().splitlines()]
    segs = [json.loads(l) for l in (tmp_path / "corpus_db" / "segments.jsonl").read_text().splitlines()]
    assert len(files) == 3 and len(segs) == 2 and segs[0]["code_switch"] == "unlabelled" and "text" not in segs[0]
    assert files[0]["metadata"] == {"Speaker_1_m": {"gender": "male", "age": None, "device": None, "environment": None, "locale": None}}
    assert files[0]["audio"] is None and files[0]["declared_suffix"] == ".wav"
