"""services.northena.admit — Stage 1 (Doc 05 §A5.3 + §B5.1 + §B5.2).

Doc 05 canon (verbatim):
  §A5.3 · Admit freezes; judgement is borrowed via opaque handle
          (Solva depth governor), never performed by Northena.
  §B5.1 · The freeze is atomic; the artifact is IMMUTABLE for the run;
          a changed intent is a NEW admission, never an edit.
  §B5.2 · Lawful basis is enforced at Admit, before any extraction;
          five deterministic validity checks in order; a failure at
          any point refuses admission and writes the reason, and no
          downstream stage runs.

Adapted from Akki-OS-V1/backend/services/northena/admit.py:
  - FrozenArtifact / AdmitOffender / AdmitValidation shape reproduced verbatim.
  - Persistence rewritten to phase0/ JSON (matches this estate's pattern).
  - Solva boundary is admit_assist_stub (Solver lands in W5).
  - Every frozen artifact carries `judgement_provenance` — drawn-not-blank
    for downstream surfaces.
"""
from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from services.northena import admit_assist_stub
from services.northena.ledger import record as ledger_record


_REQUIRED_KEYS = (
    "artifact_type", "artifact_id", "artifact_version",
    "lawful_basis", "scope",
)

_DEFAULT_ADMITS_DIR = "/app/assessment_workspace/phase0/northena_admits"


def _admits_dir() -> Path:
    return Path(os.environ.get("NORTHENA_ADMITS_DIR", _DEFAULT_ADMITS_DIR))


# ---------------------------------------------------------------------------
# Structured-offender shape — verbatim from donor.
# ---------------------------------------------------------------------------

@dataclass
class AdmitOffender:
    validator: str
    field_path: str
    explanation: str


@dataclass
class AdmitValidation:
    offenders: List[AdmitOffender] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.offenders

    def refusal_reason(self) -> str:
        return ";".join(f"{o.validator}:{o.field_path}={o.explanation}"
                        for o in self.offenders)


def _validate_completeness(raw_intent: Dict[str, Any]) -> AdmitValidation:
    v = AdmitValidation()
    missing = [k for k in _REQUIRED_KEYS if not raw_intent.get(k)]
    if missing:
        v.offenders.append(AdmitOffender(
            validator="required_fields",
            field_path=",".join(missing),
            explanation="missing_required_fields",
        ))
    # Lawful basis is called out separately by §B5.2.
    if not str(raw_intent.get("lawful_basis", "")).strip():
        # If lawful_basis was also missing from required, this is a
        # duplicate offender that names the specific field; that's
        # per §B5.2 which insists lawful basis be refused BY NAME.
        if "lawful_basis" not in ",".join(o.field_path for o in v.offenders):
            v.offenders.append(AdmitOffender(
                validator="lawful_basis",
                field_path="lawful_basis",
                explanation="missing_lawful_basis",
            ))
    return v


# ---------------------------------------------------------------------------
# FrozenArtifact — immutable dict wrapper (§B5.1 · N-INV-4).
# ---------------------------------------------------------------------------

class FrozenArtifact:
    """Immutable dict wrapper.

    Doc 05 §B5.1 · A changed intent is a NEW admission, never an edit.
    Structurally: __setitem__ / __delitem__ raise TypeError.
    """

    __slots__ = ("_data",)

    def __init__(self, data: Dict[str, Any]) -> None:
        object.__setattr__(self, "_data", dict(data))

    def __getitem__(self, k): return self._data[k]

    def __setitem__(self, k, v):
        raise TypeError(
            "FrozenArtifact is immutable (Doc 05 §B5.1) — a changed intent "
            "is a new admission, never an edit of a live one."
        )

    def __delitem__(self, k):
        raise TypeError("FrozenArtifact is immutable (Doc 05 §B5.1)")

    def __contains__(self, k): return k in self._data

    def get(self, k, d=None): return self._data.get(k, d)

    def keys(self): return self._data.keys()

    def to_dict(self) -> Dict[str, Any]: return dict(self._data)

    def artifact_ref(self) -> LedgerArtifactRef:
        return LedgerArtifactRef(
            artifact_type=self._data["artifact_type"],
            artifact_id=self._data["artifact_id"],
            version=self._data["artifact_version"],
        )


# ---------------------------------------------------------------------------
# compile_and_freeze — the Admit entry point.
# ---------------------------------------------------------------------------

async def compile_and_freeze(
    raw_intent: Dict[str, Any],
    *,
    run_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    registry: Optional[admit_assist_stub.RegistryStub] = None,
) -> Dict[str, Any]:
    """Return `{decision, frozen_artifact?, ledger_row, reason, run_id, trace_id}`.

    Deterministic. Every path (accept + refuse) writes a Ledger row.
    Admitted runs additionally write a phase0/northena_admits/adm-<hex>.json
    frozen-artifact record for later reference-not-copy join.
    """
    run_id = run_id or f"run-{uuid.uuid4().hex[:12]}"
    trace_id = trace_id or f"trc-{uuid.uuid4().hex[:12]}"
    registry = registry or admit_assist_stub.RegistryStub()

    # §B5.2 · Completeness first — deterministic; offender list, not booleans.
    val = _validate_completeness(raw_intent)
    if not val.ok:
        row = await _refuse(run_id, trace_id, raw_intent, reason=val.refusal_reason())
        return {
            "decision": "refused",
            "ledger_row": row.to_json(),
            "reason": row.reason,
            "frozen_artifact": None,
            "run_id": run_id,
            "trace_id": trace_id,
        }

    # §A5.3 · Scope resolves through Solva stub — Northena freezes the return.
    resolved, resolve_prov = admit_assist_stub.resolve_scope(
        list(raw_intent.get("scope") or []), registry
    )
    if not resolved:
        row = await _refuse(run_id, trace_id, raw_intent, reason="scope_unresolved")
        return {
            "decision": "refused",
            "ledger_row": row.to_json(),
            "reason": row.reason,
            "frozen_artifact": None,
            "run_id": run_id,
            "trace_id": trace_id,
        }

    floor, floor_prov = admit_assist_stub.defensibility_floor(
        raw_intent.get("defensibility_floor"),
    )
    depth, depth_prov = admit_assist_stub.preservation_depth(
        raw_intent.get("preservation_depth"),
    )

    frozen_data: Dict[str, Any] = {
        **raw_intent,
        "scope": list(resolved),
        "defensibility_floor": floor,
        "preservation_depth": depth,
        "run_id": run_id,
        "trace_id": trace_id,
        "frozen_at_iso": datetime.now(timezone.utc)
                                .isoformat().replace("+00:00", "Z"),
        "judgement_provenance": {
            "resolve_scope": resolve_prov,
            "defensibility_floor": floor_prov,
            "preservation_depth": depth_prov,
        },
    }
    frozen = FrozenArtifact(frozen_data)

    row = LedgerRow.new(
        run_id=run_id,
        trace_id=trace_id,
        stage="admit",
        decision="admitted",
        reason="admitted",
        artifact_ref=frozen.artifact_ref(),
        lawful_basis_ref=str(raw_intent["lawful_basis"]),
        stamp_audit=None,
    )
    await ledger_record(row)

    # phase0/northena_admits · one JSON per admission for read-side use.
    _write_admit_record(run_id=run_id, trace_id=trace_id,
                        frozen_data=frozen_data, ledger_row=row)

    return {
        "decision": "admitted",
        "frozen_artifact": frozen_data,
        "ledger_row": row.to_json(),
        "reason": "admitted",
        "run_id": run_id,
        "trace_id": trace_id,
    }


async def _refuse(
    run_id: str, trace_id: str, raw_intent: Dict[str, Any], *, reason: str,
) -> LedgerRow:
    row = LedgerRow.new(
        run_id=run_id, trace_id=trace_id,
        stage="admit", decision="refused", reason=reason,
        artifact_ref=LedgerArtifactRef(
            artifact_type=(raw_intent.get("artifact_type")
                           if raw_intent.get("artifact_type") in
                              {"portfolio_mandate", "objective_request",
                               "thinklab_objective"}
                           else "objective_request"),
            artifact_id=raw_intent.get("artifact_id") or "unresolved",
            version=raw_intent.get("artifact_version") or "unknown",
        ),
        lawful_basis_ref=str(raw_intent.get("lawful_basis") or ""),
        stamp_audit=None,
    )
    await ledger_record(row)
    return row


def _write_admit_record(
    *, run_id: str, trace_id: str,
    frozen_data: Dict[str, Any], ledger_row: LedgerRow,
) -> None:
    d = _admits_dir()
    d.mkdir(parents=True, exist_ok=True)
    adm_id = f"adm-{uuid.uuid4().hex[:12]}"
    (d / f"{adm_id}.json").write_text(json.dumps({
        "admit_id": adm_id,
        "run_id": run_id,
        "trace_id": trace_id,
        "frozen_artifact": frozen_data,
        "ledger_row_id": ledger_row.row_id,
    }, indent=2, sort_keys=True))
