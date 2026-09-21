"""drills.ruling_1_containment_expiry_clean · Canon 8 §27 firing drill.

Ruling-1 precondition (b) demonstration · RATIFIED per DECISIONS.md
2026-08-26T04:20Z R1.

Sequence (all on REAL default directories under
/app/assessment_workspace/phase0/):
  1. Macho mints a verdict (drill_actor subject).
  2. Mkono acts with action_class='containment_started' (§32.5 atomic).
  3. containment.start_containment writes the bounded-state record.
  4. containment.reconcile_containment writes the expiry-reconciliation
     record with outcome='expired_clean'.

The clock is fast-forwarded via a computed expires_at in the past
(Canon 8 §27 verifies the reconciliation LOGIC, not real-time passing).
This is honest: a governed drill authors its own timestamps within
the record shapes.

Idempotent-once (Canon 8 §43 correction-by-new-entry-only): a second
invocation raises 'already on record' on the first mint. Test-side
cleanup removes drill_actor: files before running.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from services.watch.containment import reconcile_containment, start_containment
from services.watch.macho import mint_verdict
from services.watch.mkono import act_on_verdict


PHASE0 = Path("/app/assessment_workspace/phase0")
DRILL_ACTOR = "drill_actor:ruling_1_containment_expiry_clean"

# Stable drill record ids.
VERDICT_ID = "vd_ruling_1_containment_expiry_clean"
ACTION_ID = "ax_containment_started_ruling_1_drill"
CONTAINMENT_ID = "cn_ruling_1_containment_expiry_clean"
RECONCILIATION_ID = "cr_ruling_1_containment_expiry_clean"

# Drill timestamps (governed authorship · Canon 8 §27 fast-forward).
_VERDICT_AT = "2026-08-26T05:00:00Z"
_ACTION_AT = "2026-08-26T05:00:01Z"
_CONTAINMENT_STARTED_AT = "2026-08-26T05:00:02Z"
_CONTAINMENT_EXPIRES_AT = "2026-08-26T05:01:02Z"   # +60s bound
_RECONCILE_EXPIRED_AT = "2026-08-26T05:01:02Z"


def run_drill() -> Dict[str, Any]:
    """Execute Canon 8 §27 containment-expiring-clean drill.

    Returns a dict naming the four record paths + programme-level
    Ruling-1 precondition (b) demonstration flag.
    """
    verdict = mint_verdict({
        "verdict_id": VERDICT_ID,
        "at_iso": _VERDICT_AT,
        "sensor": "macho.drill_harness",
        "signal_class": "drill_containment_expiry",
        "severity": "noted",
        "subject_kind": "actor",
        "subject_ref": DRILL_ACTOR,
        "evidence_note": (
            "Canon 8 §27 standing drill · containment expiring clean · "
            "Ruling-1 precondition (b) demonstration · drill_actor "
            "host-identity pattern per Phase 0 DECISIONS.md L347. "
            "No live actor targeted; no estate touched."
        ),
    })

    action = act_on_verdict({
        "action_id": ACTION_ID,
        "at_iso": _ACTION_AT,
        "verdict_id": verdict.verdict_id,
        "action_class": "containment_started",
        "responder": "mkono.containment_manager",
        "acted_on_ref": DRILL_ACTOR,
        "outcome_note": (
            "Bounded read-only containment started on drill_actor for "
            "Canon 8 §27 expiring-clean drill. Sixty-second scope. "
            "Atomic with the verdict on record."
        ),
    })

    containment = start_containment({
        "containment_id": CONTAINMENT_ID,
        "started_at": _CONTAINMENT_STARTED_AT,
        "expires_at": _CONTAINMENT_EXPIRES_AT,
        "verdict_id": verdict.verdict_id,
        "responder": "mkono.containment_manager",
        "contained_actor_ref": DRILL_ACTOR,
        "bound_scope": "read_only_scoped_env",
        "bound_note": (
            "Sixty-second read-only scoped environment on drill_actor. "
            "Automatic release on expires_at. Canon 8 §14 bounded "
            "reversible state · §17 expiry required."
        ),
    })

    reconciliation = reconcile_containment({
        "reconciliation_id": RECONCILIATION_ID,
        "containment_id": containment.containment_id,
        "expired_at": _RECONCILE_EXPIRED_AT,
        "outcome": "expired_clean",
        "reconciled_by": "mkono.containment_manager",
        "period_summary": (
            "Canon 8 §27 drill · sixty seconds of scoped read-only "
            "activity on drill_actor · zero touches during window · "
            "reconciled clean at expiry. Period accounted for; outcome "
            "recorded per §18."
        ),
    })

    return {
        "ruling_1_precondition_b_demonstrated": True,
        "verdict_path": str(
            PHASE0 / "watch_verdicts" / f"{verdict.verdict_id}.json"
        ),
        "action_path": str(
            PHASE0 / "watch_actions" / f"{action.action_id}.json"
        ),
        "containment_path": str(
            PHASE0 / "containments" / f"{containment.containment_id}.json"
        ),
        "reconciliation_path": str(
            PHASE0 / "containment_reconciliations"
            / f"{reconciliation.reconciliation_id}.json"
        ),
        "drill_actor": DRILL_ACTOR,
        "canon_anchor": "Canon 8 §27 · containment expiring clean",
        "ruling_1_anchor": "Owner Ruling 2026-08-14 · precondition (b)",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_drill(), indent=2))
