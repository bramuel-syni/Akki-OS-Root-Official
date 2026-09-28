"""services.canon_rules_service · G5-v5 Family D Rules Service (RBM + ROC).

Registers `Final[...]` load-bearing vocabulary for Family D:

- RBM-1..RBM-22 (SRR rows 288..309) · promise `rulebook_engine_spec_v1` · domain `Rules Service` · Tier A rule-book machinery
- RBM-23 (SRR row 483) · promise `watch_learning_v1` · domain `O2 Security & Intent` · Tier B Certificate requirements amendment
- ROC-1..ROC-11 (SRR rows 277..287) · promise `rule_criteria_spec_v1` · domain `Rules Service` · Tier A rule criteria/registry axes

All 34 rows carry status `PROPOSED` (RBM) or `PROPOSED (pending ratification)` (ROC)
on the SRR sheet — landed under owner G5-v5 sequencing directive
(2026-09-21T~01:00Z at `a30db4f7`) that named `RBM + ROC (Rules Service)` as
the queue after DAP-1..38 + COMPLETION SPRINT directive (2026-09-21T~06:10Z)
re-affirmed continuation.

## Owner cross-references at authoring boundary (2026-09-21T~06:15Z NO-EXPEDITE ruling)

- **RBM-8** is the ceremony rule the owner cited as the mechanic governing
  R-91's frozen horizon: "System-TCB ceremony: as RBM-7 plus slowest
  countdown and external witness with no credentials over the component."
- SER C.5 I-4 is the Tier A audit-standard check the owner cited alongside
  RBM-8 (not part of Family D scope · noted for cross-reference).

Standing bounds: additive-only per SO §3.8 · closed-vocab per SO §3.10-α ·
zero external I/O · deterministic.
"""
