"""W-AUDIO-POC · CP-A5 · Gap-fill receipt emission + gated write-back.

Two responsibilities:

1. `emit_gap_fill_receipt(gft, receipts_dir)` — writes a deterministic
   shape-only JSON receipt (no raw text) to a canonical path.

2. `write_gap_transcript_or_refuse(gft, transcript_bytes, verdicts,
   receipts_dir)` — runs release-gate refusal + transcript-leak guard
   BEFORE any OBS PutObject would be attempted.  On admit, returns a
   marker dict describing where OBS PutObject would land.  Actual OBS
   PutObject is upstream OS-boundary code guarded by `readonly_obs_guard`;
   this function's contract is admit-or-refuse.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Mapping

from services.audio_poc.hf_transcribe import GapFillTranscript
from services.audio_poc.release_gate import (
    TranscriptArtefact,
    admit_transcript_release,
    SAFE_TRANSCRIPT_TIER,
)
from services.secret_hygiene.hf_token import (
    assert_no_transcript_leak_of_active_token,
)


class WriteBackRefused(Exception):
    """Raised when the release-gate refuses the transcript."""


def _receipt_filename(gft: GapFillTranscript) -> str:
    return (
        f"{gft.recording_station}_"
        f"{gft.recording_date_utc}_"
        f"{gft.recording_slot}_"
        f"{gft.recording_filename_stem}.gap_fill.json"
    )


def _canonical_receipt_bytes(gft: GapFillTranscript) -> bytes:
    payload = asdict(gft)
    return json.dumps(
        payload,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def emit_gap_fill_receipt(
    gft: GapFillTranscript,
    receipts_dir: Path,
) -> Path:
    """Write a deterministic shape-only receipt for a gap-fill result.

    Receipt content is `asdict(gft)` → canonical-JSON.  The transcript
    text is NEVER carried in the receipt.  The transcript-leak guard
    is applied to the serialised bytes as a belt-and-braces check.
    """
    receipts_dir.mkdir(parents=True, exist_ok=True)
    body = _canonical_receipt_bytes(gft)
    assert_no_transcript_leak_of_active_token(body.decode("utf-8"))
    p = receipts_dir / _receipt_filename(gft)
    p.write_bytes(body)
    return p


def write_gap_transcript_or_refuse(
    gft: GapFillTranscript,
    transcript_bytes: bytes,
    verdicts: Mapping[str, str],
    receipts_dir: Path,
) -> dict:
    """Refuse or admit a transcript write-back to OBS.

    Applies the transcript-leak guard to `transcript_bytes` FIRST
    (raises RuntimeError before any release-gate call if the active
    token value leaks into the transcript body).  Then constructs a
    `TranscriptArtefact` and invokes `admit_transcript_release`; on
    refusal, raises `WriteBackRefused`.  On admit, emits the shape-
    only receipt and returns a marker dict.
    """
    # Belt-and-braces: refuse if the transcript body contains the
    # active token (would be a transcript-side leak).
    try:
        assert_no_transcript_leak_of_active_token(
            transcript_bytes.decode("utf-8", errors="replace")
        )
    except RuntimeError:
        raise  # bubble up unchanged; guard message does not echo value

    artefact = TranscriptArtefact(
        tier=SAFE_TRANSCRIPT_TIER,
        kdpa_verdict=verdicts.get("kdpa_verdict", "PENDING"),
        named_persons_verdict=verdicts.get("named_persons_verdict", "PENDING"),
        transfer_basis=verdicts.get("transfer_basis", "PENDING"),
        licence_class=verdicts.get("licence_class", "PENDING"),
    )
    try:
        admit_transcript_release(artefact)
    except Exception as e:
        raise WriteBackRefused(
            f"transcript write-back refused: {type(e).__name__}"
        ) from None

    # Admitted.  Emit the receipt.  Actual OBS PutObject would be
    # invoked upstream through readonly_obs_guard's companion writer;
    # this function returns a marker describing the destination.
    receipt_path = emit_gap_fill_receipt(gft, receipts_dir)
    obs_key = (
        f"{gft.recording_station}/"
        f"{gft.recording_date_utc}/"
        f"{gft.recording_filename_stem}.json"
    )
    return {
        "admitted": True,
        "receipt_path": str(receipt_path),
        "obs_key": obs_key,
    }
