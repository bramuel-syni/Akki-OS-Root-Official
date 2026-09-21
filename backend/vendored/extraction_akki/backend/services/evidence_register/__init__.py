"""services.evidence_register · Doc 19B §19B.4-6 · EP-1 evidence register.

EP-1 verbatim (grounding brief lines 41-42):
    'EP-1 [PROPOSED] Build the register first — cheapest piece, and it
     immediately hardens the custody-recall and Model Acceptance sites
     above.'

§19B.6 verbatim (line 246):
    'No figure reaches an external document without a resolvable
     register row — stated as absolute in the proposal, not
     aspirational.'

The register is a two-store package:
  * register.py           · evidence_register JSONL write-once by figure_id.
  * claims_validation.py  · A-4 companion ledger (EP-3 · never a build gate).
  * router.py             · HTTP surface (both stores empty at ship).
"""
