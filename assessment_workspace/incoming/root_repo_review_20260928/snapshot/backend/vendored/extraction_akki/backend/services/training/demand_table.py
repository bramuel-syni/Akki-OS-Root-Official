"""Demand Table compile · Doc 17 §4.1 + Incremental Training Capacity Briefing §3.

Governs:
  * §3.3 · B — coordination breadth · positive integer per stratum.
  * §3.4 · I — interference flag · binary at introduction (0 or 1).
  * §3.5 · E = B + I · computed once at compile · model-independent.
  * §4.1 · admissibility · every scheme carries a named_failure.

Persistence discipline mirrors ``services.connect.sources_store``:
governed non-frozen JSON under a workspace directory. No new Pydantic
contract lands with CP3 · Parity 59 is preserved.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


# ---------------------------------------------------------------------------
# Configuration · workspace path for persisted compiled demand tables.
# ---------------------------------------------------------------------------

_DEMAND_TABLE_DIR: Optional[Path] = None


def _default_dir() -> Path:
    """Default persistence dir · overridable by env for tests."""
    p = os.environ.get(
        "TRAINING_DEMAND_TABLE_DIR",
        "/app/assessment_workspace/phase0/training/demand_tables",
    )
    return Path(p)


def _configure_for_tests(dir_: Path) -> None:
    """Test hook · pins the persistence dir for a test's tmp_path scope."""
    global _DEMAND_TABLE_DIR
    _DEMAND_TABLE_DIR = Path(dir_)
    _DEMAND_TABLE_DIR.mkdir(parents=True, exist_ok=True)


def _active_dir() -> Path:
    if _DEMAND_TABLE_DIR is not None:
        return _DEMAND_TABLE_DIR
    d = _default_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d


# ---------------------------------------------------------------------------
# Shapes · §4.1 admissibility · §3.3-3.5 binding rules.
# ---------------------------------------------------------------------------

class UnnamedFailureError(ValueError):
    """§4.1 verbatim: 'A scheme enters the table only with its named failure ·
    the concrete thing that breaks without it. Robustness is not admissible.'"""


@dataclass(frozen=True)
class Scheme:
    """A named, reusable capability a model either holds or does not (§3.1)."""
    id: str
    named_failure: str


@dataclass(frozen=True)
class StratumDemand:
    """§3.3 (B) + §3.4 (I) per stratum · E derived (§3.5)."""
    stratum_id: str
    B: int
    I: int

    def __post_init__(self) -> None:
        # §3.3: B is a coordination breadth · positive.
        if self.B <= 0:
            raise ValueError(
                f"stratum {self.stratum_id!r} · B must be positive (§3.3); got {self.B}"
            )
        # §3.4: I is binary at introduction. Weighted I requires calibration.
        if self.I not in (0, 1):
            raise ValueError(
                f"stratum {self.stratum_id!r} · I is binary at introduction (§3.4); got {self.I}"
            )

    @property
    def E(self) -> int:
        """§3.5: E = B + I."""
        return self.B + self.I


@dataclass(frozen=True)
class DemandTable:
    """The demand travels with the objective · model-independent · computed once."""
    objective_id: str
    schemes: List[Scheme]
    per_stratum: List[StratumDemand]
    compiled_at: str  # ISO-8601 UTC

    def per_stratum_with_E(self) -> List[StratumDemand]:
        """Convenience · returns the per-stratum list; E is a property of each row."""
        return list(self.per_stratum)


# ---------------------------------------------------------------------------
# Compile · admissibility + derivation.
# ---------------------------------------------------------------------------

def compile(
    objective_id: str,
    schemes: List[Scheme],
    per_stratum: List[StratumDemand],
) -> DemandTable:
    """§4.1 admissibility + §3.5 derivation. Compile stage rejects unnamed-failure
    schemes as it rejects an objective with no test set."""
    for s in schemes:
        if not s.named_failure or not s.named_failure.strip():
            raise UnnamedFailureError(
                f"scheme {s.id!r} has no named_failure. §4.1: a scheme enters "
                f"the table only with its named failure."
            )
    return DemandTable(
        objective_id=objective_id,
        schemes=list(schemes),
        per_stratum=list(per_stratum),
        compiled_at=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# Persistence · stamp a compiled DemandTable to disk + read.
# ---------------------------------------------------------------------------

def stamp(table: DemandTable) -> Path:
    """Persist the compiled demand table under the active dir. Idempotent per
    objective_id — the latest stamp overwrites the file for that objective."""
    safe = table.objective_id.replace("/", "_").replace(":", "_")
    p = _active_dir() / f"{safe}.json"
    payload = {
        "objective_id": table.objective_id,
        "schemes": [asdict(s) for s in table.schemes],
        "per_stratum": [
            {"stratum_id": r.stratum_id, "B": r.B, "I": r.I, "E": r.E}
            for r in table.per_stratum
        ],
        "compiled_at": table.compiled_at,
    }
    p.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return p


def read_all() -> List[dict]:
    """Return every persisted demand table as dicts · REFERENCE-NOT-COPY."""
    d = _active_dir()
    out: List[dict] = []
    for p in sorted(d.glob("*.json")):
        try:
            out.append(json.loads(p.read_text()))
        except (json.JSONDecodeError, OSError):
            continue
    return out
