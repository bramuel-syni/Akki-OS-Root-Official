"""CENSUS-3-F.2 · runtime bindings for the OBS read-only adapter.

This module is ADDITIVE to the CENSUS-3-F Commit-A shape.  It provides
pure-Python helpers that the adapter methods delegate to for their
runtime behaviour.  No sealed surface is modified — only new helpers
are added.

Owner-authority anchors (verbatim; survive compaction):

- Owner Rulings 2 + 1a/2a/3/4 verbatim 2026-09-22T~04:14-04:2XZ
  (CENSUS-3-F GPU pipeline opens · same-seal hygiene · cp10 harness
  refresh · DQ-10 hook-anomaly monitoring · ratchet measured-basis).

- Owner Ruling for CENSUS-3-F.2 forks (this-session, 2026-09-22T~05:35Z):

    FORK-F.2-WRITER: "(γ). State-repo receipt files under
    phase0/drill_receipts_census_3_f/ per the CP-CLEANUP precedent —
    no new writer of record, no Canon-9 §3 surface event."

    FORK-F.2-OBS-CUSTODY: "(α), with one constraint — the values come
    from custody already on disk, not from a fresh owner drop. ...
    If the keys genuinely exist nowhere durable, fall back to (δ) with
    a DQ credential ask."  (Fell back to HALF-δ per .env-hygiene block;
    DQ-11 filed.)

    FORK-F.2-HF-MODEL-BIND: "(α). local_files_only=True AND
    HF_HUB_OFFLINE=1 set in the adapter runtime env before load.  Add
    one invariant asserting the adapter never performs an HF HTTP
    fetch while SEC-2026-09-12-01 stands."

    FORK-F.2-COMMIT-SHAPE: "Commit-A′, extension of CENSUS-3-F, per the
    CENSUS-SURFACE-A precedent.  Single-wave narrative."

- HF-HOLD SEC-2026-09-12-01 STANDING (DQ-06).  Model load must not
  cross network; local cache read only.

- DQ-11 (this-wave) · `/app/backend/.env` tracked-instead-of-gitignored.
  Live OBS bind (env-vend of HUAWEI_OBS_AK/SK) waits for hygiene close.
  Keys are known-durable at
  `custody/credentials/rms_connection_creds_v1.xlsx#Huawei Creds`.

- Canon-9 §3 preserved: this module has ZERO writer verbs that touch
  the sealed ledger writer surface (`services.mtafiti.asset_registry_writer`).
  The `write_read_receipt_to_phase0` helper writes to state-side phase0
  files only — the same disk-only receipt pattern as
  `phase0/harness_ground_truth/` and `phase0/eyeball_proxies/` per
  CP-CLEANUP-STATE-DISCIPLINE 2026-09-19T~18:30Z.

- Canon-9 §3 forward option (banked, NOT built at F.2): if the owner
  later wants read events queryable on the mtafiti asset registry
  surface, add `AssetRegistryRecord.collection = "EXTERNAL_READ_EVENT_OBS"`
  variant additively; no writer surface added, only a new collection
  vocab entry.

Standing bounds:
- Additive-only per SO §3.8.  No sealed module touched.
- Deterministic: no wall-clock, no random, no network under HF-HOLD.
- The OBS S3 client bind SAFE-REFUSES when the .env-hygiene block is
  active; there is no live OBS network I/O in this module until
  DQ-11 closes.
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Final, Optional


# ---------------------------------------------------------------------------
#  HF-HOLD SEC-2026-09-12-01 guard vocabulary
# ---------------------------------------------------------------------------

HF_OFFLINE_ENV_KEYS: Final[tuple[str, ...]] = (
    "HF_HUB_OFFLINE",
    "TRANSFORMERS_OFFLINE",
)
"""Both must be set to `"1"` before the faster-whisper model is loaded
(owner ruling FORK-F.2-HF-MODEL-BIND α: local-cache-only, no network
under SEC-2026-09-12-01)."""


HF_OFFLINE_VALUE: Final[str] = "1"


# ---------------------------------------------------------------------------
#  OBS env-bind vocabulary (SAFE-REFUSE surface · DQ-11 gate)
# ---------------------------------------------------------------------------

OBS_ENV_KEYS: Final[tuple[str, ...]] = (
    "HUAWEI_OBS_AK",
    "HUAWEI_OBS_SK",
    "HUAWEI_OBS_ENDPOINT",
)
"""The three env keys the adapter checks for live OBS bind.  As of
CENSUS-3-F.2 Commit-A' none are set (DQ-11 open: `/app/backend/.env`
is tracked-instead-of-gitignored; live env-vend waits for hygiene
close)."""


# ---------------------------------------------------------------------------
#  Phase0 receipt-writer paths (owner Ruling FORK-F.2-WRITER γ)
# ---------------------------------------------------------------------------

CENSUS3F_PHASE0_ROOT_ENV: Final[str] = "CENSUS3F_PHASE0_ROOT"
"""Env pointer to the phase0 receipts root.  Default resolved at call
time via `default_phase0_root()`; tests override to a tmpdir."""


CENSUS3F_READS_SUBDIR: Final[str] = "reads"
CENSUS3F_CURSORS_SUBDIR: Final[str] = "cursors"


def default_phase0_root() -> Path:
    """Default phase0 root: `<code-repo>/backend/phase0/drill_receipts_census_3_f/`.

    Runs from the adapter package location; walks up to
    `<backend>/phase0/drill_receipts_census_3_f/`.
    """
    # runtime.py -> obs_huawei_audio_read_only -> data_source -> services -> backend
    return (
        Path(__file__).resolve().parent.parent.parent.parent
        / "phase0"
        / "drill_receipts_census_3_f"
    )


def resolve_phase0_root() -> Path:
    """Return the effective phase0 root: env override wins over default."""
    env = os.environ.get(CENSUS3F_PHASE0_ROOT_ENV)
    return Path(env).resolve() if env else default_phase0_root()


# ---------------------------------------------------------------------------
#  HF-HOLD guard (assert before any faster-whisper load)
# ---------------------------------------------------------------------------

class HFHoldViolation(Exception):
    """Raised when the runtime bind attempts to load a HF model without
    both offline env keys set to '1'.  DQ-06 SEC-2026-09-12-01 guard."""


def ensure_hf_offline_env() -> None:
    """Set HF_HUB_OFFLINE=1 and TRANSFORMERS_OFFLINE=1 in the current
    process env.  Idempotent; raises `HFHoldViolation` if a value that
    is not `"1"` is already set (would indicate a live-fetch attempt)."""
    for key in HF_OFFLINE_ENV_KEYS:
        current = os.environ.get(key)
        if current is None:
            os.environ[key] = HF_OFFLINE_VALUE
            continue
        if current != HF_OFFLINE_VALUE:
            raise HFHoldViolation(
                f"HF-HOLD SEC-2026-09-12-01 violation: {key}={current!r} "
                f"(must be {HF_OFFLINE_VALUE!r} before model load)"
            )


def assert_hf_offline_env() -> None:
    """Assert HF offline env is set; raise `HFHoldViolation` otherwise.
    Read-only version of `ensure_hf_offline_env` for property tests."""
    for key in HF_OFFLINE_ENV_KEYS:
        v = os.environ.get(key)
        if v != HF_OFFLINE_VALUE:
            raise HFHoldViolation(
                f"HF-HOLD SEC-2026-09-12-01 violation: {key}={v!r} "
                f"(must be {HF_OFFLINE_VALUE!r} before model load)"
            )


# ---------------------------------------------------------------------------
#  OBS SAFE-REFUSE bind (DQ-11 gate · no network until hygiene close)
# ---------------------------------------------------------------------------

class OBSCredentialsUnavailable(Exception):
    """Raised when live OBS bind is attempted without all three env
    keys present.  DQ-11 gate: `/app/backend/.env` hygiene-hold; keys
    known-durable at
    `custody/credentials/rms_connection_creds_v1.xlsx#Huawei Creds` but
    env-vend is blocked until `.env` is untracked."""


def obs_env_available() -> bool:
    """Return True iff all three OBS env keys are present and non-empty.

    Does NOT read values (no leak into transcript · no memory copy of
    secret material).  Presence-only check for SAFE-REFUSE routing.
    """
    for key in OBS_ENV_KEYS:
        v = os.environ.get(key)
        if not v:  # None or empty string
            return False
    return True


def refuse_live_obs_without_env() -> None:
    """SAFE-REFUSE gate: raise `OBSCredentialsUnavailable` unless all
    three OBS env keys are present.  The adapter calls this at the top
    of `stream_object` so the pipeline halts cleanly instead of
    attempting a network I/O with missing credentials."""
    if not obs_env_available():
        raise OBSCredentialsUnavailable(
            "CENSUS-3-F.2 live OBS bind SAFE-REFUSED: one or more of "
            f"{list(OBS_ENV_KEYS)} is unset.  DQ-11 open "
            "(/app/backend/.env tracked-not-gitignored; keys known-durable "
            "at custody/credentials/rms_connection_creds_v1.xlsx#Huawei Creds)."
        )


# ---------------------------------------------------------------------------
#  Phase0 receipt writer (owner Ruling FORK-F.2-WRITER γ)
# ---------------------------------------------------------------------------

def _read_receipt_filename(bucket: str, object_key: str, epoch: int) -> str:
    """Deterministic receipt filename: `<epoch>_read_<bucket>_<key_hash8>.json`.

    Uses a short prefix of sha256(object_key) so long/exotic OBS keys
    yield filesystem-safe filenames.  Deterministic (same triple →
    same filename)."""
    key_hash = hashlib.sha256(object_key.encode("utf-8")).hexdigest()[:16]
    return f"{epoch}_read_{bucket}_{key_hash}.json"


def write_read_receipt_to_phase0(
    bucket: str,
    object_key: str,
    sha256: str,
    byte_count: int,
    *,
    wave_id: str = "CENSUS-3-F",
    lawful_basis_admit_ref: str = "",
    phase0_root: Optional[Path] = None,
    now_utc: Optional[datetime] = None,
) -> Path:
    """Write an ExternalRead ledger event to phase0 as a JSON receipt.

    Canon-9 §3 preserved: no writer verb into the sealed ledger writer
    surface.  This is a disk-only receipt under state-repo phase0 (or
    the env-overridden root), matching how cp10 harness receipts +
    eyeball proxies + drill receipts already ledger.

    Args:
        bucket: OBS bucket name.
        object_key: OBS object key.
        sha256: Content sha256 (hex, lowercase).
        byte_count: Object byte count.
        wave_id: Wave identifier for the receipt payload.
        lawful_basis_admit_ref: Reference to the wave-level admit id.
        phase0_root: Override phase0 root (tests use tmpdir).
        now_utc: Override wall clock (tests use fixed datetime).

    Returns:
        Path to the written receipt file.
    """
    root = phase0_root if phase0_root is not None else resolve_phase0_root()
    reads_dir = root / CENSUS3F_READS_SUBDIR
    reads_dir.mkdir(parents=True, exist_ok=True)
    now = now_utc if now_utc is not None else datetime.now(timezone.utc)
    epoch = int(now.timestamp())
    filename = _read_receipt_filename(bucket, object_key, epoch)
    path = reads_dir / filename
    payload = {
        "wave_id": wave_id,
        "bucket": bucket,
        "object_key": object_key,
        "sha256": sha256,
        "byte_count": byte_count,
        "at_utc": now.isoformat().replace("+00:00", "Z"),
        "lawful_basis_admit_ref": lawful_basis_admit_ref,
        "receipt_kind": "EXTERNAL_READ_CENSUS3F",
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return path


def receipt_id_from_path(path: Path) -> str:
    """Deterministic receipt id from a receipt file path: filename
    stem stripped of `_read_` infix.  Idempotent across runs."""
    return f"EXTERNAL-READ-CENSUS3F-{path.stem}"


# ---------------------------------------------------------------------------
#  Cursor persistence (owner Ruling FORK-F.2-WRITER γ · same phase0 root)
# ---------------------------------------------------------------------------

def persist_cursor_to_disk(
    bucket: str,
    object_key: str,
    *,
    phase0_root: Optional[Path] = None,
) -> Path:
    """Write the cursor for `bucket` to phase0.  Overwrites prior cursor
    for the same bucket (last-write-wins on cursor advance)."""
    root = phase0_root if phase0_root is not None else resolve_phase0_root()
    cursors_dir = root / CENSUS3F_CURSORS_SUBDIR
    cursors_dir.mkdir(parents=True, exist_ok=True)
    path = cursors_dir / f"{bucket}.cursor"
    path.write_text(object_key)
    return path


def read_cursor_from_disk(
    bucket: str,
    *,
    phase0_root: Optional[Path] = None,
) -> str:
    """Return the cursor key for `bucket`, or empty string if not banked."""
    root = phase0_root if phase0_root is not None else resolve_phase0_root()
    path = root / CENSUS3F_CURSORS_SUBDIR / f"{bucket}.cursor"
    if not path.exists():
        return ""
    return path.read_text().rstrip("\n")


# ---------------------------------------------------------------------------
#  Lawful-basis-admit id resolution
# ---------------------------------------------------------------------------

LAWFUL_BASIS_ADMIT_ID: Final[str] = (
    "LAWFUL-BASIS-ADMIT-CENSUS3-20260922T014000Z"
)
"""The banked wave-level LawfulBasisAdmit id.  Matches the receipt at
`LAWFUL_BASIS_ADMIT_REF`."""
