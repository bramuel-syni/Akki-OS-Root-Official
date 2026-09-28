"""services.cif.detection · CIF learned faculty · OUT TCB · Doc-9 §BR-9.4.

Canon anchors verbatim:
- **BR-9.4** (Doc-9): the CIF detection faculty MAY propose; only
  the deterministic acceptance point (M16-W3, IN TCB) acts.  The
  detection module is a learned pattern-matching surface authoring
  `CIFProposal_v0` instances.
- **AC-18** proposes-never-ratifies: this module authors proposals
  and does NOT decide.  Its outputs carry zero ratification-
  adjacent field (enforced at shape level in the sealed M16-W1
  contract `contracts.cif_proposal_v0.CIFProposal_v0`).
- **Canon 8 §W11** one-task-one-identity: structural role
  separation.  This module MUST NOT import TCB-adjacent surfaces
  (`services.watch`, `services.ledger_emitter`,
  `services.data.repository`, `motor`, `services.cif.acceptance_point`);
  it MUST NOT expose any mutation/decision function whose name
  starts with a banned prefix (`insert_`, `update_`, `delete_`,
  `upsert_`, `replace_`, `modify_`, `drop_`, `persist_`, `emit_`,
  `ratify_`, `admit_`, `accept_`, `decide_`, `sign_`).  The only
  authoring verb exposed is `author_proposal`.
- **`services/doc0_attributes/tcb.py`** (sealed W-M2-SW7 · R-3
  ratification 2026-09-09) classifies `component_id == "cif.detection"`
  as OUT TCB per Doc-0 Attr-1 CIF TCB placement.
- **M16-W1 sealed**: outputs are identity instances of
  `contracts.cif_proposal_v0.CIFProposal_v0` (sealed 6-field tuple ·
  frozen · extra=forbid · kind Literal closed 2-tuple · SO §3.10-α
  closed-schema discipline).
- **SO §3.8** thin-kernel additive-only: new module in
  `services/cif/`; sealed modules not edited.

Downstream wiring (M16-W3 · M16-W4 · M16-W5):
- Every `CIFProposal_v0` authored here MUST pass through the M16-W3
  deterministic single-experiment acceptance point (BR-9.2) before
  affecting anything downstream.
- On acceptance the M16-W4 output router binds `kind == "capability"`
  proposals to the sealed L-5 capability register
  (`services.capability_registry.register_capability`, A20.16) and
  `kind == "research_loop_item"` proposals to the L-4 research loop
  sink (A5.22).
- CIF holds via M16-W5 `services.cif.halt` (DET-1) independently of
  the Targeta run it feeds.
"""
from __future__ import annotations

from typing import Tuple

from contracts.cif_proposal_v0 import CIFProposal_v0

__all__ = ("author_proposal",)


def author_proposal(
    *,
    proposal_id: str,
    proposed_at: str,
    kind: str,
    payload: str,
    citations: Tuple[str, ...] = (),
    proposed_by: str = "cif.detection",
) -> CIFProposal_v0:
    """Author a `CIFProposal_v0` instance from a CIF detection call.

    The learned pattern-matching surface fills the closed 6-field
    tuple of the sealed M16-W1 contract and returns a frozen
    pydantic instance.  Shape drift is caught at construction time
    by the sealed model (regex on `proposal_id`, Literal on
    `kind`, `extra="forbid"`, `frozen=True`).

    Per **AC-18** (proposes-never-ratifies) this function has no
    decision surface: it does not decide whether the proposal is
    accepted, does not persist, does not sign, does not emit
    ledger intents.  The M16-W3 deterministic acceptance point
    (IN TCB) is the sole surface that acts on the proposal
    downstream.

    Parameters
    ----------
    proposal_id
        Regex-constrained id (``^cif_[a-z0-9_-]+$`` per M16-W1).
    proposed_at
        ISO UTC timestamp (``min_length=1``).
    kind
        Closed 2-tuple ``Literal["capability", "research_loop_item"]``
        binding downstream routing to L-5 A20.16 (capability register)
        or L-4 A5.22 (research loop).  A third value is refused at
        construction time by pydantic per SO §3.10-α.
    payload
        Opaque JSON-serialised string (``min_length=1``) per DAP-7
        Option-D structural bytes-in pattern.  The detection module
        does NOT introspect the payload; downstream consumers do.
    citations
        Evidence citations (closed tuple).  Empty tuple by default.
    proposed_by
        Component id of the proposing surface.  Defaults to
        ``"cif.detection"`` per BR-9.4.  Consumers may override for
        test scaffolding; sealed R-3 ratification 2026-09-09 places
        ``cif.detection`` OUT TCB.

    Returns
    -------
    CIFProposal_v0
        Identity instance of the sealed M16-W1 model (not a shadow /
        re-declaration / subclass).
    """
    return CIFProposal_v0(
        proposal_id=proposal_id,
        proposed_at=proposed_at,
        proposed_by=proposed_by,
        kind=kind,
        payload=payload,
        citations=citations,
    )
