"""CP-AIP-4-CODEC-SERVICE · AIP v1.0 §3.3 (a) round-trip fidelity measurement per codec version.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-4-CODEC-SERVICE and nothing else.

Spec anchor (AIP v1.0):
- §3.3 (a) verbatim: 'Round-trip fidelity measured and recorded per
  codec version before that version serves any commission.'
- §1.4 measure-don't-assert: every claim is either measured at run-time
  OR explicitly flagged as unmeasured. This module records MEASURED
  values only; the acceptance gate refuses codec versions with no
  measurement record on file.
- §1.5 unrepresentable-not-policed: incomplete measurement records are
  refused at construction (frozen dataclass __post_init__ gate).

Design:
- `RoundTripFidelityMeasurement_v1` frozen dataclass carries the
  measured fidelity record with mandatory `measurement_method` +
  `provenance_material_ref` (both non-empty at construction time).
- Persistence: append-only JSONL at a governed seam path (default
  `phase0/audio_codec_fidelity/measurements.jsonl` under the workspace
  root; overridable via storage_root parameter for test isolation).
- `assert_codec_version_ready_to_serve` refuses with
  `MissingFidelityMeasurementError` when no measurement exists for the
  requested codec version.

Sealed carriers UNCHANGED per SO §3.8:
- backend/services/perception/audio_codec/artefact.py (CP-M6-4-2).
- backend/services/perception/audio_codec/service.py (CP-M6-4-1).

Wave-honest limits:
- No LLM invocation. No HTTP call. Filesystem WRITE limited to the
  governed measurement-JSONL path (append-only) - measurement is an
  audit-trail act by nature, not an out-of-perimeter side effect.
- No audio bytes / waveforms / samples carriers (§3.1 P038 tokens-not-
  waveforms).
- Case-agnostic; no executive-domain tokens.
"""
from __future__ import annotations

import dataclasses
import json
import threading
from pathlib import Path
from typing import Any, Dict, Optional


class FidelityMeasurementIncomplete(Exception):
    """§1.5 unrepresentable-not-policed refusal · fidelity record
    missing a required carrier (measurement_method or
    provenance_material_ref). Structural gate at construction time."""


class MissingFidelityMeasurementError(Exception):
    """§3.3 (a) verbatim refusal · a codec version cannot serve any
    commission until a round-trip fidelity measurement has been
    recorded for that version. §1.4 measure-don't-assert."""


@dataclasses.dataclass(frozen=True)
class RoundTripFidelityMeasurement_v1:
    """§3.3 (a) fidelity measurement record.

    Six carriers:
      - `codec_version` — the codec version this measurement pertains
        to (matches sealed CP-M6-4-2 `codec_version` field).
      - `measured_at_utc` — ISO-8601 UTC timestamp when the measurement
        was taken.
      - `sample_count` — number of samples the round-trip was run over.
      - `bit_error_rate` — measured BER (or equivalent fidelity metric)
        as a float in [0, 1].
      - `measurement_method` — verbatim descriptor of HOW the fidelity
        was measured (e.g. `"synthetic_ber_over_512_frame_reconstruction"`).
        Non-empty at construction (§1.5).
      - `provenance_material_ref` — reference to the material used for
        the measurement (§6.2 P098 verbatim 'provenance points to
        material'). Non-empty at construction (§1.5).
    """

    codec_version: str
    measured_at_utc: str
    sample_count: int
    bit_error_rate: float
    measurement_method: str
    provenance_material_ref: str

    def __post_init__(self) -> None:  # noqa: D401
        if not self.codec_version:
            raise FidelityMeasurementIncomplete(
                "RoundTripFidelityMeasurement_v1: codec_version must be "
                "non-empty (§1.5 unrepresentable-not-policed)"
            )
        if not self.measurement_method:
            raise FidelityMeasurementIncomplete(
                "RoundTripFidelityMeasurement_v1: measurement_method "
                "must be non-empty (§1.4 measure-don't-assert · every "
                "record identifies HOW it was measured)"
            )
        if not self.provenance_material_ref:
            raise FidelityMeasurementIncomplete(
                "RoundTripFidelityMeasurement_v1: provenance_material_ref "
                "must be non-empty (§6.2 P098 verbatim 'provenance "
                "points to material')"
            )


def _default_measurements_path() -> Path:
    return (
        Path("/app/assessment_workspace/phase0/audio_codec_fidelity/measurements.jsonl")
    )


_write_lock = threading.Lock()


def record_fidelity_measurement(
    *,
    measurement: RoundTripFidelityMeasurement_v1,
    storage_root: Optional[Path] = None,
) -> Path:
    """Append a fidelity measurement record to the governed JSONL seam.

    Append-only. Creates the parent directory if absent. Returns the
    absolute path of the JSONL file written to. §1.4 measure-don't-
    assert: every recorded value MUST come from an actual measurement
    run - this function does NOT synthesise measurement values.
    """
    target = storage_root if storage_root is not None else _default_measurements_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(dataclasses.asdict(measurement), ensure_ascii=False, sort_keys=True)
    with _write_lock:
        with target.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    return target


def load_measurement(
    *,
    codec_version: str,
    storage_root: Optional[Path] = None,
) -> Optional[RoundTripFidelityMeasurement_v1]:
    """Load the most-recent fidelity measurement for a given codec
    version. Returns None if none is found.

    §3.3 (a) verbatim: 'measured and recorded per codec version'.
    """
    target = storage_root if storage_root is not None else _default_measurements_path()
    if not target.exists():
        return None
    last_match: Optional[RoundTripFidelityMeasurement_v1] = None
    with target.open("r", encoding="utf-8") as fh:
        for raw in fh:
            raw = raw.strip()
            if not raw:
                continue
            data: Dict[str, Any] = json.loads(raw)
            if data.get("codec_version") == codec_version:
                last_match = RoundTripFidelityMeasurement_v1(
                    codec_version=data["codec_version"],
                    measured_at_utc=data["measured_at_utc"],
                    sample_count=int(data["sample_count"]),
                    bit_error_rate=float(data["bit_error_rate"]),
                    measurement_method=data["measurement_method"],
                    provenance_material_ref=data["provenance_material_ref"],
                )
    return last_match


def assert_codec_version_ready_to_serve(
    *,
    codec_version: str,
    storage_root: Optional[Path] = None,
) -> None:
    """§3.3 (a) verbatim: 'Round-trip fidelity measured and recorded
    per codec version before that version serves any commission.'

    Refuses with `MissingFidelityMeasurementError` if no measurement
    record exists for `codec_version`. §1.4 measure-don't-assert.
    """
    record = load_measurement(codec_version=codec_version, storage_root=storage_root)
    if record is None:
        raise MissingFidelityMeasurementError(
            f"§3.3 (a) verbatim: codec version {codec_version!r} has no "
            f"round-trip fidelity measurement on file. No serve permitted "
            f"until a MEASURED record is banked at "
            f"{(storage_root or _default_measurements_path())!s}. §1.4 "
            f"measure-don't-assert."
        )
    return None
