"""Phase 8 Stage B-1 — wizard router shim (Owner E3 ratified).
Commercial-cut 2026-07-06 — buyer helpers extracted to salvage.

Owner ruling verbatim (Phase 8 Stage B-1 dispatch, E3):
    "Land services/wizard/router_shims.py at B-1. It's the §0.2 debt with
     this slot as named receiver; deferring reschedules it into exactly
     the period (B-2/B-3 router evolution) where duplication drifts.
     Grep-negative gate parametrised over the triad symbols."

Post-commercial-cut posture (BCR v1.4 §12, 2026-07-06):
  * The two BUYER-ONLY helpers `summarise_dual_deltas` and
    `compose_objective_request_from_frozen_state_with_proposals`
    relocated verbatim to `/app/salvage/commercial_cut_2026_07_06/
    backend/wizard/router_shims_buyer_helpers.py` per BCR v1.4 §12.2
    (code preservation, mandatory).
  * The OPERATOR-ONLY helper `compose_objective_request_from_frozen_state`
    stays in the extractor build tree.
  * Frozen contracts `WizardCommitState_v0` + `ObjectiveRequest_v2`
    remain byte-identical. `WizardCommitState_v0.variant` Literal still
    accepts `"buyer"` (orphan-in-place per PRES-3); the composer's
    buyer branch is retained as no-live-consumer dead code that never
    fires post-cut (variant will only be "operator" from the operator
    wizard). This keeps `WizardCommitState_v0` byte-identical parity 26.

Grep-negative gate (updated post-cut): the operator router does not
locally define the operator-remaining triad symbol
`compose_objective_request_from_frozen_state`.
"""
from __future__ import annotations

from typing import Any, Dict

from contracts.objective_request_v2 import ObjectiveRequest_v2
from contracts.wizard_commit_state import WizardCommitState_v0


def _get_committed(wizard_state: WizardCommitState_v0, field_name: str, default: Any) -> Any:
    """Read a committed value from the frozen state; fallback to default."""
    cv = wizard_state.committed_values.get(field_name)
    if cv is None:
        return default
    return cv.value


def compose_objective_request_from_frozen_state(
    wizard_state: WizardCommitState_v0,
) -> ObjectiveRequest_v2:
    """Mint an `ObjectiveRequest_v2` from a frozen wizard state.

    Preconditions:
      * `wizard_state.committed_at is not None` (state is frozen).
      * `wizard_state.variant in ("operator", "buyer")` — post-cut only
        "operator" is a live producer; `"buyer"` remains an orphan
        variant value per PRES-3 (frozen contract byte-identical).

    Postconditions:
      * Returned envelope carries `commissioner = f"wizard-{variant}-{session_id}"`.
      * Deterministic `idempotency_key = f"handoff-{session_id}"`.
      * Buyer variant only: `envelope.floor_feasibility["dual_delta_summary"]`
        is initialised (empty dict). Post-cut this branch is dead code
        (no live buyer producer) but retained to preserve the composer's
        byte-identical semantics for orphan-in-place validity checks.
      * No mutation of `wizard_state` — pure function.
    """
    if wizard_state.committed_at is None:
        raise ValueError(
            "compose_objective_request_from_frozen_state requires a FROZEN "
            "wizard state (committed_at must be set). Handoff on an unfrozen "
            "session is refused at the router layer with `wizard_not_frozen`."
        )

    reach_value = _get_committed(
        wizard_state, "reach", {"scope_refs": [], "exclusions": [], "depth": "default"}
    )
    if not isinstance(reach_value, dict):
        reach_value = {"scope_refs": [str(reach_value)], "exclusions": [], "depth": "default"}
    reach_block = {
        "scope_refs": list(reach_value.get("scope_refs", []) or []),
        "exclusions": list(reach_value.get("exclusions", []) or []),
        "depth": reach_value.get("depth", "default"),
    }

    output_standard = _get_committed(
        wizard_state, "output.standard",
        {"minimum_class": "utterance", "minimum_scores": {}},
    )
    if not isinstance(output_standard, dict):
        output_standard = {"minimum_class": str(output_standard), "minimum_scores": {}}
    output_block = {
        "form": _get_committed(wizard_state, "output.form", "composed_conclusion"),
        "consumer": _get_committed(wizard_state, "output.consumer", "person"),
        "grain": _get_committed(wizard_state, "output.grain", "synthesized_whole"),
        "standard": output_standard,
    }

    floor_feasibility_raw = _get_committed(wizard_state, "envelope.floor_feasibility", {})
    if not isinstance(floor_feasibility_raw, dict):
        floor_feasibility_raw = {}
    floor_feasibility_out: Dict[str, Any] = dict(floor_feasibility_raw)
    # Orphan-in-place: buyer branch retained but no live producer post-cut.
    if wizard_state.variant == "buyer":
        floor_feasibility_out.setdefault("dual_delta_summary", {})

    availability_snapshot = _get_committed(wizard_state, "envelope.availability_snapshot", {})
    if not isinstance(availability_snapshot, dict):
        availability_snapshot = {}

    envelope_block = {
        "lawful_basis": _get_committed(wizard_state, "envelope.lawful_basis", "legitimate_interest"),
        "done_condition": _get_committed(wizard_state, "envelope.done_condition", "standing_floor"),
        "budget": _get_committed(wizard_state, "envelope.budget", "default"),
        "scope_ceiling": _get_committed(wizard_state, "envelope.scope_ceiling", "estate"),
        "availability_snapshot": availability_snapshot,
        "floor_feasibility": floor_feasibility_out,
        "commissioner": f"wizard-{wizard_state.variant}-{wizard_state.session_id}",
        "committed_at": wizard_state.committed_at,
    }

    payload = {
        "entry": "external_request",
        "reach": reach_block,
        "output": output_block,
        "envelope": envelope_block,
        "shaping": None,
        "commercial": None,
        "idempotency_key": f"handoff-{wizard_state.session_id}",
    }
    return ObjectiveRequest_v2.model_validate(payload)
