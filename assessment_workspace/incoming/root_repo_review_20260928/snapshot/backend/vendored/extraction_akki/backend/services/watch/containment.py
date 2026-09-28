"""services.watch.containment — Canon 8 §14-§18 containment fabric.

Structural writers for Containment_v0 + ContainmentReconciliation_v0.
Both records land on disk append-only (Canon 8 §43 correction-by-new-
entry-only).

start_containment requires a verdict on record (seam law · §6).
reconcile_containment requires the containment on record; one
reconciliation per containment (Canon 8 §18).
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from contracts.containment import Containment_v0, ContainmentReconciliation_v0
from services.watch.macho import load_verdicts


_DEFAULT_C_DIR = "/app/assessment_workspace/phase0/containments"
_DEFAULT_R_DIR = "/app/assessment_workspace/phase0/containment_reconciliations"


def _c_dir() -> Path:
    return Path(os.environ.get("CONTAINMENTS_DIR", _DEFAULT_C_DIR))


def _r_dir() -> Path:
    return Path(os.environ.get("CONTAINMENT_RECONCILIATIONS_DIR", _DEFAULT_R_DIR))


def _find_containment(containment_id: str) -> Optional[Containment_v0]:
    for c in load_containments():
        if c.containment_id == containment_id:
            return c
    return None


def _find_reconciliation_for(containment_id: str) -> Optional[ContainmentReconciliation_v0]:
    for r in load_reconciliations():
        if r.containment_id == containment_id:
            return r
    return None


def start_containment(payload: Dict[str, Any]) -> Containment_v0:
    """Mkono starts a bounded reversible containment. Requires the
    verdict on record (seam law · Canon 8 §6). Refuses overwrite."""
    c = Containment_v0(**payload)
    if not any(v.verdict_id == c.verdict_id for v in load_verdicts()):
        raise ValueError(
            f"verdict {c.verdict_id!r} not on record. Canon 8 §6 seam law: "
            f"Macho mints the verdict before Mkono contains."
        )
    d = _c_dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{c.containment_id}.json"
    if path.exists():
        raise ValueError(
            f"containment {c.containment_id!r} already on record. "
            f"Canon 8 §43: correction is by new entry only."
        )
    path.write_text(json.dumps(c.model_dump(), indent=2, ensure_ascii=False))
    return c


def load_containments() -> List[Containment_v0]:
    d = _c_dir()
    if not d.is_dir():
        return []
    return sorted(
        (Containment_v0(**json.loads(p.read_text()))
         for p in d.glob("cn_*.json")),
        key=lambda c: (c.started_at, c.containment_id),
    )


def reconcile_containment(payload: Dict[str, Any]) -> ContainmentReconciliation_v0:
    """Mkono writes a reconciliation at containment expiry. Refuses if
    the containment is not on record OR is already reconciled."""
    r = ContainmentReconciliation_v0(**payload)
    if _find_containment(r.containment_id) is None:
        raise ValueError(
            f"containment {r.containment_id!r} not on record. "
            f"Start the containment before reconciling."
        )
    if _find_reconciliation_for(r.containment_id) is not None:
        raise ValueError(
            f"containment {r.containment_id!r} already reconciled. "
            f"Canon 8 §43: correction is by new entry only."
        )
    d = _r_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{r.reconciliation_id}.json").write_text(
        json.dumps(r.model_dump(), indent=2, ensure_ascii=False)
    )
    return r


def load_reconciliations() -> List[ContainmentReconciliation_v0]:
    d = _r_dir()
    if not d.is_dir():
        return []
    return sorted(
        (ContainmentReconciliation_v0(**json.loads(p.read_text()))
         for p in d.glob("cr_*.json")),
        key=lambda r: (r.expired_at, r.reconciliation_id),
    )
