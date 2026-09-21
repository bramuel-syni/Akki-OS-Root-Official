"""services/solva_v2/engines/__init__.py — CP-S8.

Case-agnostic donor-lift skeletons.  Owner directive (2026-09-13):
lift the donor pool from Akki-Executive-Core, but STRIP all
executive-domain tokens.  Where a donor construct's case-agnostic
form is ambiguous, HALT.

HALTed constructs (declared in
notes/W_SOLVA_V2_LIFT_grounding_brief.md §C, not lifted):
  * DPO-S1 donor refusal categories {clean, jailbreak_attempt,
    out_of_scope, distress_flag, extraction_marker} — different
    refusal shape from Canon-4 §24's three actions.
  * DPO-S2 donor reflection LOCKED_QUESTIONS — executive-domain
    'diagnosis' vocabulary; case-agnostic reflection question set
    is an owner decision.
  * Sector-tag triangulation — domain-specific.
"""
