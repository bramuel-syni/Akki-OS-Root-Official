"""W-D12-POC · CP-D12P1 · Receipt-contract module for transcription pipe-proof.

Owner directive verbatim (DECISIONS 2026-09-15T~03:55Z Effect 6):
    "After the census completes: run the transcription pipe-proof with the
     canon CI fixture (whisper-tiny + faster-whisper) on a SMALL BOUNDED
     set of real NAS files (single-digit count), on the GPU hosts, all
     outputs labeled POC-NOT-PRODUCTION in provenance, receipts banked.
     Production model selection still follows census activation per
     §A17.11 — the POC does not pre-empt it."

Owner Option-A ratification verbatim (DECISIONS 2026-09-15T~09:50Z):
    "Option A — ratified. Proceed with the D12 POC now: bounded single-
     digit NAS files, GPU hosts, POC-NOT-PRODUCTION provenance, raw
     transcription receipts banked under phase0/d12_poc_receipts/,
     release-gate admission explicitly deferred."

Design (bindings):

  * D12 POC outputs are labeled `POC-NOT-PRODUCTION` regardless of stage
    outcome (success or refused).  Owner directive is verbatim on this.
  * The receipt NEVER carries transcript text.  The receipt is a shape
    fingerprint (input canonical key + input sha256 + wall-clock + model
    id + segment count + word-count approximation + language hint) —
    NOT the content.  This preserves the position-redaction hard-lock
    for arbitrary bounded NAS files whose sensitivity is `unknown` per
    CP-CSAIM1 (Canon-4 §5.1 conservative fallback) until the audio-plane
    feed_declaration_registry publishes their declarations (owner-desk
    item DECISIONS 2026-09-15T~09:50Z Effect 2).
  * The receipt-assembler is a pure DATA function (no I/O, no side-
    effects); the live run wraps it.  This keeps the invariants
    deterministic-testable without any GPU/NAS runtime dependency.
  * Model + compute-type + beam-size are canonical tokens frozen in this
    module.  Silent rename fires an invariant.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


# Canonical tokens frozen at module scope.  Silent renames fire invariants.
POC_NOT_PRODUCTION_FLAG: str = "POC-NOT-PRODUCTION"
D12_MODEL_ID: str = "faster-whisper:tiny"
D12_MODEL_VERSION: str = "ctranslate2"
D12_COMPUTE_TYPE: str = "int8"
D12_BEAM_SIZE: int = 1


@dataclass(frozen=True)
class D12InputCanonicalKey:
    """CP-A2 recording_inventory canonical key shape, re-frozen here for
    D12 receipt assembly.  Kept as an independent dataclass rather than a
    direct import of `services.audio_poc.recording_inventory.RecordingKey`
    so this module can produce a receipt for OBS-sourced audio too (once
    OBS-to-bytes plumbing lands) without a cross-package coupling.
    """
    station: str
    date_utc: str
    slot: str
    filename_stem: str


@dataclass(frozen=True)
class D12PocReceipt:
    """The shape of a D12 POC receipt.

    Field-name discipline:
      - Every field is a shape / fingerprint / provenance field.
      - Zero fields carry transcript text, segment content, utterance
        strings, or any other transcript body form.
      - `poc_flag` is always `POC-NOT-PRODUCTION` (owner directive verbatim).
    """
    poc_flag: str
    input_canonical_key: D12InputCanonicalKey
    input_sha256: str
    input_bytes: int
    model_id: str
    model_version: str
    compute_type: str
    beam_size: int
    wall_clock_seconds: float
    segment_count: int
    word_count_approx: int
    language_hint: Optional[str]
    avg_confidence: Optional[float]
    gpu_host: str
    gpu_model: str
    provenance_note: str


_PROVENANCE_NOTE: str = (
    "raw transcript body NEVER emitted · "
    "release-gate admission deferred per owner Option-A 2026-09-15T~09:50Z"
)


def assemble_d12_poc_receipt(
    *,
    input_canonical_key: D12InputCanonicalKey,
    input_sha256: str,
    input_bytes: int,
    wall_clock_seconds: float,
    segment_count: int,
    word_count_approx: int,
    language_hint: Optional[str],
    avg_confidence: Optional[float],
    gpu_host: str,
    gpu_model: str,
) -> D12PocReceipt:
    """Assemble a D12 POC receipt.

    Callers supply the operational fields (input bytes / sha256 / wall
    clock / per-run stats / gpu identity).  Model + compute-type + beam-
    size + poc_flag come from module-frozen constants.  The receipt
    never carries transcript text under any code path (see
    `D12PocReceipt` docstring).
    """
    return D12PocReceipt(
        poc_flag=POC_NOT_PRODUCTION_FLAG,
        input_canonical_key=input_canonical_key,
        input_sha256=input_sha256,
        input_bytes=input_bytes,
        model_id=D12_MODEL_ID,
        model_version=D12_MODEL_VERSION,
        compute_type=D12_COMPUTE_TYPE,
        beam_size=D12_BEAM_SIZE,
        wall_clock_seconds=wall_clock_seconds,
        segment_count=segment_count,
        word_count_approx=word_count_approx,
        language_hint=language_hint,
        avg_confidence=avg_confidence,
        gpu_host=gpu_host,
        gpu_model=gpu_model,
        provenance_note=_PROVENANCE_NOTE,
    )


# Frozen set of fields the receipt is ALLOWED to carry.  A silent
# addition of a text-carrying field (`transcript`, `segments_text`,
# etc.) fires the strict-subset invariant.
D12_POC_RECEIPT_ALLOWED_FIELDS: frozenset = frozenset({
    "poc_flag",
    "input_canonical_key",
    "input_sha256",
    "input_bytes",
    "model_id",
    "model_version",
    "compute_type",
    "beam_size",
    "wall_clock_seconds",
    "segment_count",
    "word_count_approx",
    "language_hint",
    "avg_confidence",
    "gpu_host",
    "gpu_model",
    "provenance_note",
})


# Fields the receipt MUST NOT carry, ever (transcript body enumeration).
# The `never_carries_transcript_text_field` invariant asserts this set is
# disjoint from `D12_POC_RECEIPT_ALLOWED_FIELDS`.
D12_POC_RECEIPT_FORBIDDEN_TEXT_FIELDS: frozenset = frozenset({
    "text",
    "transcript",
    "transcript_text",
    "segments_text",
    "utterance_text",
    "body",
    "content",
    "segments",  # segments-with-text-inside also forbidden; only counts allowed
})
