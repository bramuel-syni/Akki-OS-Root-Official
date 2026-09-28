"""services/solva_v2/critic_seam.py — CP-S7.

Canon-7 §44 · Critic Seam Tier 2.  Findings classed, cited, NEVER
blocking, NEVER editing.

Canon-7 §44.1 verbatim: 'A critic reading the author's rationale
inherits the author's frame, which is the blind-spot-sharing failure
this whole design exists to avoid.'

Structural discipline in this file:
  * CriticInvocation carries {artefact, canon, authorising_instrument,
    rubric} only.  No author-rationale, no worker-rationale, no
    reasoning-draft — enforced at the contract layer and by the
    CP-S7 negative-scan test on THIS FILE.
  * CriticFindings carries findings + citations only.  No blocks/edits.
"""
from __future__ import annotations

from contracts.solva_reasoning import CriticFindings, CriticInvocation


def invoke_critic(invocation: CriticInvocation) -> CriticFindings:
    """Thin-kernel critic: reads the four Canon-7 §44 fields and
    returns a findings envelope.  A future wave binds this to an
    independent-model-instance critic pass (Canon-7 §44.2).

    Zero fabrication here — this thin skeleton returns empty findings
    when the rubric is empty and a single 'unresolved' finding when
    the rubric is non-empty.  The invariant is the SHAPE (never
    blocking, never editing), not the semantic answer.
    """
    if not invocation.rubric.strip():
        return CriticFindings()
    return CriticFindings(
        findings=(f"Rubric received but Tier-2-binding pending: {invocation.rubric!r}",),
        citations=(invocation.canon,),
    )
