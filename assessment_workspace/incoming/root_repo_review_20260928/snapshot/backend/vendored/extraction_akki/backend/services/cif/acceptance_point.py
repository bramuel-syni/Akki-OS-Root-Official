"""services.cif.acceptance_point — M16-W3 · Doc-9 BR-9.2 deterministic
single-experiment acceptance point (IN TCB per sealed
services.doc0_attributes.tcb R-3 2026-09-09).

**Structural placement.**  Per BR-9.2 and sealed
`services.doc0_attributes.tcb::_TCB_ENTRIES` R-3 ratification
2026-09-09, the component_id ``cif.acceptance_point`` is
classified **IN** TCB (reason: "BR-9.2 CIF single-experiment
acceptance point (Doc-9)").  This module is the only surface that
acts on a CIF proposal; the M16-W2 detection module authors
proposals but never decides.  Routing to L-4 (research loop
A5.22) and L-5 (capability register A20.16) is delegated to
M16-W4 as a **mechanical consequence** of the verdict returned
here; this module has zero routing surface.

**Deterministic-rung-1 machinery.**  Per Canon 4 §22, a
deterministic acceptance check is rung-1 machinery — **not** a
second model's judgement.  The predicate takes no LLM client, no
learned faculty, and no non-deterministic randomness source at
top-level.  AST-scan invariants enforce this structurally
(``tests/invariants/test_m16_w3_cif_acceptance_point.py`` test 3).

**Fail-closed trust boundary.**  Per AC-18 and Canon 8 §W11 the
acceptance point is the trust boundary — non-``CIFProposal_v0``
inputs return ``False`` (never raise).  Callers may not rely on
exception-based rejection.

**Single-experiment gate.**  Per BR-9.2 the acceptance predicate
implements a single deterministic experiment.  The chosen
experiment is: **the proposal must carry at least one citation**
(closed ``Tuple[str, ...]`` from ``CIFProposal_v0``).  This binds
AC-18 (proposes-never-ratifies) at the acceptance boundary: an
un-cited proposal fails the single-experiment gate.  Everything
else is refused; nothing beyond that per SO §6.4 NOTHING-BEYOND
clause.

**Type identity check.**  Per SO §3.10-α closed-schema discipline
the module uses ``type(proposal) is CIFProposal_v0`` (not
``isinstance``) so no shadow class and no subclass masquerade can
pass the boundary.

**Additive-only per SO §3.8.**  Sealed
``contracts/cif_proposal_v0.py`` (M16-W1) is consumed by identity
import.  Sealed ``services/doc0_attributes/tcb.py`` (W-M2-SW7)
is consumed structurally by the invariant test — this module does
not import it, so a bad edit to ``tcb.py`` cannot leak into the
acceptance path.

Canon anchors verbatim:
- **BR-9.2** (Doc-9): CIF single-experiment acceptance point · IN
  TCB · the ONLY surface that acts on a CIF proposal downstream.
- **AC-18**: proposes-never-ratifies · the acceptance point is
  the ONLY surface that decides whether a CIF proposal advances.
- **Canon 4 §22**: deterministic acceptance check is rung-1
  machinery · NOT a second model's judgement.
- **Canon 8 §W11**: one-task-one-identity · structural role
  separation preserved — this module neither authors nor routes.
- **``tcb_enumeration_v1``** canon drop 2026-09-09 +
  ``Ratification_Record_v1`` R-3: banks
  ``cif.acceptance_point → IN`` verbatim (cited by test 2).
- **M16-W1 sealed** ``CIFProposal_v0``: consumed by identity
  import; type identity check via ``type() is`` per SO §3.10-α.
- **SO §3.8**: thin-kernel additive-only.
- **SO §3.10-α**: closed-schema discipline (no shadow · no
  subclass).
- **SO §6.4 NOTHING-BEYOND**: no other surface in this module.
- **SO §6.7**: batch-ratification-at-preceding-seal.

Card citation: STATE/OBJECTIVES/M16.md MUST-DO 3 · EXIT-W3.
"""
from __future__ import annotations

from contracts.cif_proposal_v0 import CIFProposal_v0


def is_accepted(proposal: CIFProposal_v0) -> bool:
    """Return ``True`` iff *proposal* passes the CIF
    single-experiment acceptance gate (BR-9.2).

    The gate:
      1. ``type(proposal) is CIFProposal_v0`` (SO §3.10-α closed
         schema identity check — no shadow / no subclass /
         no dict / no None).
      2. ``len(proposal.citations) >= 1`` (AC-18 evidence-backed
         proposes-never-ratifies · un-cited proposals fail).

    Returns ``False`` on any deviation.  Never raises: the
    predicate IS the trust boundary (AC-18 + Canon 8 §W11).

    Determinism: no wall-clock read · no randomness source · no
    hidden state · same proposal instance yields the same verdict
    across arbitrarily many repeated calls (Canon 4 §22 rung-1
    machinery).
    """
    if type(proposal) is not CIFProposal_v0:
        return False
    return len(proposal.citations) >= 1


__all__ = ["is_accepted"]
