"""services.northena.converge — Stage 3 (Doc 05 §A5.5).

Doc 05 §A5.5 verbatim: "Converge decides termination on two conditions
fixed in the frozen artifact, both threshold checks: done-condition met
terminates as success; budget exhausted terminates on budget; neither
continues. There is no learned stopping."

Precedence: done-condition beats budget (success is truthful over
budget-exhausted when both hit).

Restored 2026-08-27 (pre-CP-D0 defect fix, owner ruling): the three
stamp-audit absorbers `absorb_solva_trace`, `absorb_outer_gate_receipt`,
and `absorb_v2_refusal` were removed at W4 commit 7bea87d ("will be
re-adapted in W5 when Solver + trace-lens surfaces land"). W5 landed
Solva but did not re-adapt these helpers, leaving 1 collection error
+ 8 runtime failures on the ratified invariant suite and orphaning
three v0 seams advertised in services/system_state.py. Semantics
preserved byte-for-byte from 7bea87d^; only the LedgerRow constructor
call is ported to LedgerRow.new(...) (LedgerRow.at now auto-populates
via `default_factory=lambda: datetime.now(timezone.utc)` — same UTC-
aware value the pre-deletion versions computed explicitly).
"""
from __future__ import annotations

from typing import Any, Dict

from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from services.northena.ledger import record as ledger_record


async def check(
    *,
    run_id: str,
    trace_id: str,
    artifact_ref: Any,
    lawful_basis_ref: str,
    done_condition_met: bool,
    budget_exhausted: bool,
) -> Dict[str, Any]:
    if isinstance(artifact_ref, dict):
        artifact_ref = LedgerArtifactRef(**artifact_ref)

    if done_condition_met:
        decision, reason = "terminate_success", "done_condition_met"
    elif budget_exhausted:
        decision, reason = "terminate_budget", "budget_exhausted"
    else:
        decision, reason = "continue", "neither_threshold_met"

    row = LedgerRow.new(
        run_id=run_id, trace_id=trace_id,
        stage="converge", decision=decision, reason=reason,
        artifact_ref=artifact_ref,
        lawful_basis_ref=lawful_basis_ref,
        stamp_audit=None,
    )
    await ledger_record(row)
    return {"decision": decision, "ledger_row": row.to_json(), "reason": reason}


async def absorb_solva_trace(
    *,
    run_id: str,
    trace_id: str,
    trace_dict: Dict,
    artifact_ref: LedgerArtifactRef,
    lawful_basis_ref: str,
) -> LedgerRow:
    """G3 seam — Solva SolvaTrace lands in a converge-stage ledger row.

    Solva spec §13: "Solva → Ledger (via stamp-audit): Refusal/decision
    audit; absorbed by Northena." The seam is `LedgerRow.stamp_audit:
    Optional[Dict]` — no frozen-contract mutation. Northena still owns
    the halt (N-INV-6); this helper is the write-side of that ownership
    when Solva provides the convergence-time judgment.

    Decision derives from the trace's conclusion kind:
      * assertion → terminate_success
      * refusal   → terminate_budget (Solva refused below floor; Northena
                    records the halt as a budget-style terminate with the
                    Solva reason preserved in `stamp_audit`).
    """
    conclusion = trace_dict.get("conclusion") or {}
    kind = conclusion.get("kind")
    if kind == "assertion":
        decision = "terminate_success"
        reason = f"solva_assertion_class={conclusion.get('klass')}"
    elif kind == "refusal":
        decision = "terminate_budget"
        reason = f"solva_refusal_{conclusion.get('reason', 'unknown')}"
    else:
        raise ValueError(f"absorb_solva_trace: unrecognised conclusion.kind={kind!r}")
    row = LedgerRow.new(
        run_id=run_id, trace_id=trace_id,
        stage="converge",
        decision=decision,
        reason=reason,
        artifact_ref=artifact_ref, lawful_basis_ref=lawful_basis_ref,
        stamp_audit=trace_dict,
    )
    await ledger_record(row)
    return row


async def absorb_outer_gate_receipt(
    *,
    run_id: str,
    trace_id: str,
    receipt_dict: Dict,
    artifact_ref: LedgerArtifactRef,
    lawful_basis_ref: str,
) -> LedgerRow:
    """G6 seam — outer-gate irreversibility receipt lands in a gate-stage row.

    Product v2.1 §22.1 records "each Gate decision and reason". V2 gates
    the outer-gate file-out (§29.1), so a successful outer-gate transform
    maps to `stage="gate", decision="fresh"` — fresh (anonymised) egress
    was produced. The full receipt lands in `stamp_audit` as a permissive
    Dict; NO NEW FIELD is added to northena_ledger_row@v0.
    """
    row = LedgerRow.new(
        run_id=run_id, trace_id=trace_id,
        stage="gate",
        decision="fresh",
        reason=(
            f"outer_gate_transform_applied:"
            f"{receipt_dict.get('transform_version', 'unknown')}"
        ),
        artifact_ref=artifact_ref, lawful_basis_ref=lawful_basis_ref,
        stamp_audit={"outer_gate_receipt": receipt_dict},
    )
    await ledger_record(row)
    return row


async def absorb_v2_refusal(
    *,
    run_id: str,
    trace_id: str,
    refusal_dict: Dict,
    artifact_ref: LedgerArtifactRef,
    lawful_basis_ref: str,
) -> LedgerRow:
    """G6 seam — V2 refusal envelope lands in a gate-stage row.

    Product v2.1 §29.1 "V2 gates the outer-gate file-out"; §22.1 "every
    refusal" records refusals. V2 refusal maps to `stage="gate",
    decision="refused"`. Full envelope in `stamp_audit` as permissive Dict;
    NO NEW FIELD on northena_ledger_row@v0.
    """
    reason_code = refusal_dict.get("reason_code", "unknown")
    row = LedgerRow.new(
        run_id=run_id, trace_id=trace_id,
        stage="gate",
        decision="refused",
        reason=f"v2_refused:{reason_code}",
        artifact_ref=artifact_ref, lawful_basis_ref=lawful_basis_ref,
        stamp_audit={"v2_refusal": refusal_dict},
    )
    await ledger_record(row)
    return row
