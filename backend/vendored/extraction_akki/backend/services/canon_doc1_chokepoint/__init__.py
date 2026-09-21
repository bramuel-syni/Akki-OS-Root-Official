"""services.canon_doc1_chokepoint · G5-v5 Family A first sub-slice · Doc 1 M12 chokepoint canon vocabulary.

Landed under WAVE R-93 (G5-v5 second slice · Family A first sub-slice · A5.1..A5.9 authoring)
inside the R-91 CEREMONY-OPEN countdown window (2026-09-21T03:23:15Z → 2026-09-23T03:23:15Z).
This package is a net-new SO §3.8 additive addition; no sealed module is edited.

Ruling 5 authority (v5 SRR sheet only · sha256 `00072c58…` · rows R2..R10). The
package registers `Final[...]` canon vocabulary for the 9 CANON rules of
Document 1 Section 5 (chokepoint · M12 milestone). Sealed M12 code at
`services/chokepoint/*` carries substantive enforcement of A5.1/A5.5/A5.6 but
registers zero `Final[...]` vocabulary; this package adds the vocabulary
layer that lets tests bind against SRR rows directly (canon_ref-bites-on-live-code).

Standing bounds inherited (unchanged): additive-only per SO §3.8 · closed-vocab
per SO §3.10-α · zero external I/O · deterministic · terminal pytest only ·
no testing_agent · three-repo discipline · ratchet measured-monotonic-up
floor 5695 (bumps at pre-Commit-A per M16-W3 corrected order).
"""

from services.canon_doc1_chokepoint.chokepoint_vocabulary import (
    DOC1_A5_RULE_IDS,
    DOC1_A5_RULE_COUNT,
    DOC1_A5_ROW_SHARED_METADATA,
    scan_for_non_chokepoint_model_invocation,
    scan_for_envelope_persistence,
    scan_for_outbound_network_outside_crossing,
    scan_for_credential_at_receipt,
    scan_for_degraded_answer_on_grounding_failure,
)

__all__ = [
    "DOC1_A5_RULE_IDS",
    "DOC1_A5_RULE_COUNT",
    "DOC1_A5_ROW_SHARED_METADATA",
    "scan_for_non_chokepoint_model_invocation",
    "scan_for_envelope_persistence",
    "scan_for_outbound_network_outside_crossing",
    "scan_for_credential_at_receipt",
    "scan_for_degraded_answer_on_grounding_failure",
]
