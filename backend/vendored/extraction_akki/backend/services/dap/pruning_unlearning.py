"""W-M3-SW8 · W-PRUNING-UNLEARNING · Pruning_Unlearning_Amendment_v1.

Canon anchors (verbatim, `Pruning_Unlearning_Amendment_v1` · 2026-09-09):

* DAP-37: 'A fine-tuned artefact MAY be pruned ... A pruned artefact
  MUST re-pass MOAC's acceptance criteria ... A pruned artefact's
  hash differs from its pre-pruning hash; it is a new artefact for
  every purpose DAP-10 and DAP-31 govern.'

* DAP-38: 'When a unit's rights status changes to withdrawn ... every
  artefact whose training manifest cites that unit is identified via
  the registry ... and is either re-derived without the unit or
  recalled ... A unit's contribution to the estate release budget
  (DAP-35) is NOT refunded on unlearning.'

* R-12 OPEN: 'When the original training run was not sharded for
  isolated retraining, is re-derivation mandatory regardless of
  cost, or does recall alone satisfy DAP-38?'  Marker:
  PRUNING_UNLEARNING_R12_PENDING_OVERRIDE.

This module owns two contracts:

  1. DAP-37 hash-identity invariant.  A `PrunedArtefact` whose
     post-pruning hash equals its pre-pruning hash cannot be
     constructed; the type refuses at the constructor with
     `PruningHashCollision`.

  2. DAP-38 rights-withdrawal dispatch.  Given a withdrawn unit and a
     bundle of training manifests, the dispatcher returns one action
     per manifest that cites the unit: `re_derive` when the run was
     SISA-sharded, or `recall` otherwise (with the R-12 override
     marker attached so silent flips are impossible).

DAP-38 budget clause is encoded as an invariant function whose only
correct answer is `True` — refund is forbidden on unlearning.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple

from pydantic import BaseModel, ConfigDict


# R-12 marker — silent flip forbidden until owner rules.
PRUNING_UNLEARNING_R12_PENDING_OVERRIDE: str = "PENDING-OVERRIDE"


class PruningHashCollision(ValueError):
    """DAP-37: post-pruning hash must differ from pre-pruning hash."""


@dataclass(frozen=True)
class PrunedArtefact:
    """DAP-37 pruning record.

    Constructing a `PrunedArtefact` whose post-pruning hash equals its
    pre-pruning hash is a DAP-37 violation and raises
    `PruningHashCollision` directly (no wrapping).
    """

    pre_pruning_hash: str
    post_pruning_hash: str
    pruning_ratio: float
    pruning_method: str

    def __post_init__(self) -> None:
        if self.pre_pruning_hash == self.post_pruning_hash:
            raise PruningHashCollision(
                "DAP-37: pruned artefact hash equals pre-pruning hash"
            )


def assert_pruned_artefact_is_new(pa: PrunedArtefact) -> None:
    """DAP-37: assert `pa` is a new artefact (hash differs).

    Construction of `PrunedArtefact` already refuses collisions; this
    assertion is a downstream re-check so callers holding a value can
    fail closed if the type was ever bypassed.
    """
    if pa.pre_pruning_hash == pa.post_pruning_hash:
        raise PruningHashCollision(
            "DAP-37: pruned artefact hash equals pre-pruning hash"
        )


class TrainingManifest(BaseModel):
    """DAP-38 training manifest — cites the units used for training.

    `was_sisa_sharded` records whether the run was isolated-retrainable
    (SISA-style).  R-12 turns on this bit.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    artefact_id: str
    cited_units: Tuple[str, ...]
    was_sisa_sharded: bool


def handle_rights_withdrawal(
    *,
    withdrawn_unit: str,
    manifests: Iterable[TrainingManifest],
) -> dict:
    """DAP-38 dispatch: one action per manifest citing `withdrawn_unit`.

    Sharded artefact → `re_derive` (norm).
    Non-sharded artefact → `recall` with R-12 override marker attached.

    Returns a dict with an `actions` list.  Manifests that do not cite
    the withdrawn unit yield no action.
    """
    actions: List[dict] = []
    for m in manifests:
        if withdrawn_unit not in m.cited_units:
            continue
        if m.was_sisa_sharded:
            actions.append({
                "kind": "re_derive",
                "artefact_id": m.artefact_id,
                "withdrawn_unit": withdrawn_unit,
            })
        else:
            # R-12 unresolved: recall path is fully specified;
            # re-derivation path awaits owner ruling.  The marker
            # rides on the action so silent flips are impossible.
            actions.append({
                "kind": "recall",
                "artefact_id": m.artefact_id,
                "withdrawn_unit": withdrawn_unit,
                "r12_pending_override":
                    PRUNING_UNLEARNING_R12_PENDING_OVERRIDE,
            })
    return {"actions": actions}


def budget_refund_forbidden(*, unit_id: str) -> bool:
    """DAP-38 verbatim: 'A unit's contribution to the estate release
    budget (DAP-35) is NOT refunded on unlearning.'

    The function IS the invariant — its correct answer is `True` for
    every `unit_id`.  Refund is forbidden.
    """
    # `unit_id` is accepted for auditability of the call site; the
    # answer is unconditional.
    _ = unit_id
    return True
