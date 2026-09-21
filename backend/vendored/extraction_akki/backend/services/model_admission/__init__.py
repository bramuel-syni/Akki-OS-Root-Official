"""services.model_admission — Model Admission ceremony (W7 CP4).

Canon 4 §26 (six-criterion MOAC) + §27 (uncurated evidence) + §28
(rights lineage required to ship) + Owner Ruling 2026-08-25T23:30Z
(W7 GO · Q2 disposition on uncurated-sample source).

Ceremony fires: MOAC card + rights-lineage-resolved → admitted (+ registry
bump). MOAC card missing / lineage unresolved / floor missed / estate
sample without named purpose → refused with a stated reason. Every fire
writes a record to phase0/model_admission_records/.

CA1-011 (Doc13-023) SPLIT (Orchestrator ruling 2026-08-25T23:15Z):
  W7 lands the outcome-side named seam
  `services.watch.route_recheck_failure` — the Watch-routed enforcement
  binds to it at W9. NOT faked in W7.
"""
from services.model_admission.ceremony import (
    AdmissionOutcome,
    run_admission,
)

__all__ = ["AdmissionOutcome", "run_admission"]
