"""services.service_1.model_form_offer · W11 D · CP-D0 · A17.16 ACCEPT.

Emits the ModelFormOfferEnvelopeV0 at the dispatch seam that
previously fired emit_form_not_offerable. Owner-verbatim rationale
carried through as the envelope's ingredients_guarantee field.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from contracts.model_form_offer_envelope_v0 import (
    ModelFormOfferEnvelopeV0,
    INGREDIENTS_ONLY_GUARANTEE_VERBATIM,
)


# Closed set of stronger claims the envelope refuses. Each entry is
# a claim the platform CANNOT honestly make about a trained model —
# per A17.16 owner reasoning: 'claiming provenance of assertions
# would be overclaiming something training structurally cannot
# support.'
_FORBIDDEN_STRONGER_CLAIMS: List[str] = [
    "assertion_provenance",
    "training_causation_claim",
    "output_veracity_guarantee",
    "per_utterance_speaker_identity",
]


def emit_model_form_offer(*, trace_id: str) -> ModelFormOfferEnvelopeV0:
    """Build the A17.16 ACCEPT offer envelope. Called from the
    dispatch entry-point when output.form == OutputForm.MODEL.

    Replaces the prior emit_form_not_offerable in the MODEL branch;
    the AdmissionRefusal_v0 registry v4 marks form_not_offerable as
    struck under the same landing."""
    return ModelFormOfferEnvelopeV0(
        trace_id=trace_id,
        output_form="model",
        offered_at=datetime.now(timezone.utc).isoformat(),
        ingredients_guarantee=INGREDIENTS_ONLY_GUARANTEE_VERBATIM,
        forbidden_stronger_claims=list(_FORBIDDEN_STRONGER_CLAIMS),
    )
