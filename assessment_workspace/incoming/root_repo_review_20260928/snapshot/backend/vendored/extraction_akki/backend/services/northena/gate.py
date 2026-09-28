"""services.northena.gate — Stage 2 (Doc 05 §A5.4).

Doc 05 §A5.4 verbatim: "Gate tests scope membership at every routing
decision — it checks whether a sub-objective is in the declared scope
set, and nothing else. Material outside scope is logged and dropped,
not followed. Being adjacent and available is not being in scope.
Ambiguous membership is a compilation defect resolved at Admit by the
reasoner, never a Gate-time judgement. No inferential path exists in Gate."
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from services.northena.ledger import record as ledger_record


async def route(
    *,
    run_id: str,
    trace_id: str,
    sub_objective: str,
    artifact_ref: Any,
    lawful_basis_ref: str,
    scope: Iterable[str],
    warm_index: Optional[Iterable[str]] = None,
) -> Dict[str, Any]:
    """Return `{decision, ledger_row, reason}`.

    decision ∈ {warm, fresh, refused}.
    Adjacency is not membership: only exact string equality against the
    declared scope set admits. Ambiguity is a compilation defect for Admit.
    """
    scope_set = set(scope)
    warm_set = set(warm_index or [])
    # Accept either a Pydantic LedgerArtifactRef or a dict shape.
    if isinstance(artifact_ref, dict):
        artifact_ref = LedgerArtifactRef(**artifact_ref)

    if sub_objective not in scope_set:
        row = LedgerRow.new(
            run_id=run_id, trace_id=trace_id,
            stage="gate", decision="refused", reason="out_of_scope",
            artifact_ref=artifact_ref,
            lawful_basis_ref=lawful_basis_ref,
            stamp_audit=None,
        )
        await ledger_record(row)
        return {
            "decision": "refused",
            "ledger_row": row.to_json(),
            "reason": "out_of_scope",
        }

    if sub_objective in warm_set:
        decision, reason = "warm", "in_scope_warm_serve"
    else:
        decision, reason = "fresh", "in_scope_fresh_extraction"

    row = LedgerRow.new(
        run_id=run_id, trace_id=trace_id,
        stage="gate", decision=decision, reason=reason,
        artifact_ref=artifact_ref,
        lawful_basis_ref=lawful_basis_ref,
        stamp_audit=None,
    )
    await ledger_record(row)
    return {"decision": decision, "ledger_row": row.to_json(), "reason": reason}
