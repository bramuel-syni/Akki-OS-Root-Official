"""services.handoff.contracts — R/W of handoff records.

Records: phase0/handoff_contracts/*.json (or HANDOFF_CONTRACTS_DIR).
Append-only; each handoff_id authored once.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from contracts.handoff_contract import HandoffContract_v0


_DEFAULT_DIR = "/app/assessment_workspace/phase0/handoff_contracts"


def _dir() -> Path:
    return Path(os.environ.get("HANDOFF_CONTRACTS_DIR", _DEFAULT_DIR))


def register_handoff(payload: Dict[str, Any]) -> HandoffContract_v0:
    """Author + persist a HandoffContract_v0. Refuses duplicate handoff_id.

    Raises pydantic ValidationError on shape drift; ValueError on
    duplicate handoff_id (load-bearing conflict).
    """
    contract = HandoffContract_v0(**payload)
    d = _dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{contract.handoff_id}.json"
    if path.exists():
        raise ValueError(
            f"handoff {contract.handoff_id!r} already on record at {path}. "
            f"CA1-009 discipline: each handoff_id authored once; overwrites "
            f"are load-bearing conflicts and refused."
        )
    path.write_text(json.dumps(contract.model_dump(), indent=2, ensure_ascii=False))
    return contract


def load_handoffs() -> List[HandoffContract_v0]:
    d = _dir()
    if not d.is_dir():
        return []
    out: List[HandoffContract_v0] = []
    for p in sorted(d.glob("ho_*.json")):
        out.append(HandoffContract_v0(**json.loads(p.read_text())))
    return out


def attest_handoff(handoff_id: str) -> HandoffContract_v0:
    """Hard-fail if `handoff_id` not on record. Called at cross-time
    by any service crossing governed work between apps."""
    for contract in load_handoffs():
        if contract.handoff_id == handoff_id:
            return contract
    raise ValueError(
        f"handoff {handoff_id!r} not on record. CA1-009 discipline: "
        f"any cross-app crossing must be expressed in a HandoffContract_v0 "
        f"before it ships. Author the contract via register_handoff() first."
    )
