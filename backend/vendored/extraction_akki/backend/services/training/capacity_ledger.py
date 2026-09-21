"""Capacity Ledger · Doc 17 §4.2 + Incremental Training Capacity Briefing §5.3.

Ships the MINIMUM per Owner CP3 deprioritization:
  * record shape + append + read.
  * provenance-required day-one (§5.3 · 'the one field that cannot be retrofitted').
  * state grammar: building | held | saturated.

DEFERRED:
  * marginal-gain writer from calibration probe.
  * saturation derivation from marginal-gain history.
  * cross-commission substrate transfer.

Persistence: append-only JSONL under the workspace phase0/. No new
frozen Pydantic contract — governed non-frozen shape, pattern from
``services.connect.sources_store``.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Literal, Optional


CapacityState = Literal["building", "held", "saturated"]
ALLOWED_STATES = ("building", "held", "saturated")


@dataclass(frozen=True)
class CapacityEntry:
    """§4.2 shape · provenance is REQUIRED (§5.3)."""
    scheme_id: str
    stratum: str  # per-stratum id or "global"
    level: float  # measured 0.0..1.0
    provenance: List[str]  # commission ids that built it · REQUIRED
    marginal_gain: Optional[float]  # nullable at CP3 · fills at calibration probe
    state: CapacityState
    written_at: str  # ISO-8601 UTC


# ---------------------------------------------------------------------------
# Persistence · JSONL append-only under workspace phase0/.
# ---------------------------------------------------------------------------

_LEDGER_DIR: Optional[Path] = None


def _default_dir() -> Path:
    p = os.environ.get(
        "TRAINING_CAPACITY_LEDGER_DIR",
        "/app/assessment_workspace/phase0/training/capacity_ledger",
    )
    return Path(p)


def _configure_for_tests(dir_: Path) -> None:
    """Test hook · pins the persistence dir for a test."""
    global _LEDGER_DIR
    _LEDGER_DIR = Path(dir_)
    _LEDGER_DIR.mkdir(parents=True, exist_ok=True)


def _active_dir() -> Path:
    if _LEDGER_DIR is not None:
        return _LEDGER_DIR
    d = _default_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d


def _ledger_file() -> Path:
    return _active_dir() / "capacity_ledger.jsonl"


# ---------------------------------------------------------------------------
# Append + read.
# ---------------------------------------------------------------------------

def append(
    scheme_id: str,
    stratum: str,
    level: float,
    provenance: List[str],
    marginal_gain: Optional[float],
    state: str,
) -> CapacityEntry:
    """Append a capacity row · rejects empty provenance and out-of-grammar state."""
    if not provenance:
        raise ValueError(
            "capacity_ledger.append: provenance is required (§5.3 · the one "
            "field that cannot be retrofitted)."
        )
    if state not in ALLOWED_STATES:
        raise ValueError(
            f"capacity_ledger.append: state {state!r} not in grammar "
            f"{ALLOWED_STATES} (§4.2)."
        )
    entry = CapacityEntry(
        scheme_id=scheme_id,
        stratum=stratum,
        level=float(level),
        provenance=list(provenance),
        marginal_gain=marginal_gain,
        state=state,  # type: ignore[arg-type]
        written_at=datetime.now(timezone.utc).isoformat(),
    )
    _ledger_file().parent.mkdir(parents=True, exist_ok=True)
    with _ledger_file().open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(asdict(entry), sort_keys=True))
        fh.write("\n")
    return entry


def read_all() -> List[CapacityEntry]:
    """REFERENCE-NOT-COPY read · reads the JSONL from disk each call."""
    f = _ledger_file()
    if not f.exists():
        return []
    out: List[CapacityEntry] = []
    for line in f.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
            out.append(CapacityEntry(
                scheme_id=row["scheme_id"],
                stratum=row["stratum"],
                level=row["level"],
                provenance=list(row["provenance"]),
                marginal_gain=row.get("marginal_gain"),
                state=row["state"],
                written_at=row["written_at"],
            ))
        except (json.JSONDecodeError, KeyError):
            continue
    return out


def row_count() -> int:
    return len(read_all())
