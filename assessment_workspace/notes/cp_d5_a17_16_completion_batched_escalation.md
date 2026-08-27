# CP-D5 · Q3 · A17.16-completion — BATCHED ESCALATION

Date: 2026-08-27 (this session)
Branch: `programme/track-a`
CP: W11 D · CP-D5 · Debt Endgame · Q3 semantic fixes

## Situation

Manifest failing test (Q3 target from owner ruling Message 648):
- `backend/tests/invariants/test_phase_6_stage_b_economics.py::test_form_not_quotable_returns_form_not_offerable`

The test asserts (verbatim from source):
```
"""`callable_skill` and `knowledge_artifact` have null multipliers →
`form_not_offerable` refusal until §6.3/§6.4 lands."""
...
result = await _quote_service.issue_quote(request, "trc-form-null", warm_vs_fresh="fresh")
assert isinstance(result, AdmissionRefusal_v0)
assert result.reason == "form_not_offerable"
```

Current failure mode:
```
services/economics/quote_service.py:131
  → services/service_1/admission_refusal.py:125
    RuntimeError: admission_refusal_reasons.vN.json registry does not list
    reason='form_not_offerable' — construction blocked.
```

Root cause: `admission_refusal_reasons.v4.json` (landed at CP-D0 A17.16 ACCEPT, reconstructed at CP-D1 post-fix) moves `form_not_offerable` from `valid_reasons` to `struck_codes`. The v4 `landing_note` reads "Retains all v3 valid_reasons except form_not_offerable, which moves to struck_codes" (total-strike). The struck_codes[0].strike_rationale, by contrast, discusses ONLY the model-form doctrinal migration to `ModelFormOfferEnvelopeV0`.

`quote_service.py:131` still uses `form_not_offerable` for a SEMANTICALLY DISTINCT case: `callable_skill` / `knowledge_artifact` with null `output_form_multipliers` in the current price-model config bless (pending §6.3/§6.4 pricing landing). This is admission-time refusal, NOT the model-form doctrinal §6.5 case.

## Invariant conflict

Two ratified invariants directly contradict on the shape of `admission_refusal_reasons.v4.json`:

**Invariant A** — `tests/invariants/test_phase_6_stage_b_economics.py::test_form_not_quotable_returns_form_not_offerable`
- Currently: FAILING (in manifest as a Q3 target).
- Requires: `form_not_offerable` present in `valid_reasons` (so `admission_refusal.emit_form_not_offerable`'s guard passes for the null-multiplier case).
- Semantic anchor: v3 §6.3/§6.4 callable_skill / knowledge_artifact pending pricing.

**Invariant B** — `tests/invariants/test_a17_16_model_form_offer.py::test_admission_refusal_reasons_v4_strikes_form_not_offerable`
- Currently: PASSING (NOT in manifest; ratified at CP-D0).
- Requires (verbatim, lines 53-60):
  ```
  assert "form_not_offerable" not in valid, ...
  assert "form_not_offerable" in struck, ...
  ```
- Semantic anchor: v3 §6.5 model-form off-menu use of the reason.

## Two defensible readings

### Reading 1 — NARROW-STRIKE (v4 struke was over-executed)
- v3 spec_anchor for `form_not_offerable` was "v3 §6.5 (Model form off the offerable menu)" — narrow to model.
- The strike_rationale in v4 discusses ONLY the model-form migration path.
- The Phase 6 economics code had a SECOND, semantically-distinct use of the same reason string for the null-multiplier case at `quote_service.py:131`.
- Fix intent: Re-add `form_not_offerable` to `valid_reasons` with a **narrowed spec_anchor** scoped to null-multiplier (§6.3/§6.4 pending). Preserve the struck entry but rescope its strike to the model-form doctrinal case only.
- Cost: **Invariant B breaks** as currently authored (Invariant B's exact-string assertions do not permit the reason to be simultaneously in valid_reasons AND in struck_codes under a single canonical key). Owner ruling to amend the shape of Invariant B is required.

### Reading 2 — TOTAL-STRIKE (v4 is right, callable_skill / knowledge_artifact need their own offer envelopes)
- The v4 landing_note took the total-strike position deliberately.
- The A17.16 acceptance letter said the model-form OFFER-envelope pattern was the honest ceiling. Applied by extension: callable_skill / knowledge_artifact null-multiplier refusal is ALSO an over-cautious refusal that should route through a purpose-appropriate offer envelope (e.g., `CallableSkillPendingPricingOfferV0`, `KnowledgeArtifactPendingPricingOfferV0`) with an honest "pricing not yet landed" discriminator.
- Fix intent: Build the two new offer envelopes at §6.3/§6.4 landing scope; retire Invariant A as the null-multiplier path becomes an offer, not a refusal.
- Cost: This is a NEW BUILD (contracts + emit helpers + dispatch wiring), not a Q3 semantic fix. Belongs in Wave D CP or a §6.3/§6.4 lift, not CP-D5 Debt Endgame.

## What was tried this session (both reverted)

1. Applied Reading 1 in-place edit to `admission_refusal_reasons.v4.json`:
   - Re-added `form_not_offerable` to valid_reasons with narrowed spec_anchor.
   - Renamed struck_codes[0].reason to `"form_not_offerable (model-form doctrinal use ONLY)"` to permit both entries under a valid/struck partition.
   - RESULT: Invariant A GREEN, Invariant B RED (V1 guard violation — new-outside-manifest bad).
2. `git checkout HEAD -- backend/services/service_1/admission_refusal_reasons.v4.json` — reverted.

## Ask

Owner ruling on which reading is intended. Sub-choices for Reading 1 if selected:
- (1a) Amend Invariant B (`test_admission_refusal_reasons_v4_strikes_form_not_offerable`) to accept a partitioned reason string OR to accept the reason as struck-for-model-form-use even when the code appears in valid_reasons with a null-multiplier spec_anchor.
- (1b) Fork the reason string: keep `form_not_offerable` struck, add a NEW reason `form_pricing_not_landed` (or similar) for the null-multiplier case; update quote_service.py + admission_refusal.py to emit the new code. NOTE: owner's Message 648 amendment forbids inventing a new reason code, so this branch is disallowed unless owner explicitly authorises it.

For Reading 2:
- Confirm this is a §6.3/§6.4 build gap; Invariant A is retired at the §6.3/§6.4 landing CP, not CP-D5.
- In the meantime, `test_form_not_quotable_returns_form_not_offerable` stays in the manifest as an unfixed baseline_failure attributed to "§6.3/§6.4 pricing not landed" until the build closes it.

## Impact on CP-D5

- Q1 status: DONE (uncommitted-but-executed in working tree; will land in the CP-D5 close commit).
- Q3 Item 1 (AST-egress-gate): FIXED this session — `services/chokepoint/llm.py` added to `docs/mandates/shield_egress_exemptions.v0.json` citing Owner Order 2026-08-25 W5 §4 verbatim from the file docstring (commit a5be529).
- Q3 Item 2 (A17.16-completion / null-multiplier): **BATCHED ESCALATION — awaits owner ruling**. Manifest entry remains failing.
- Q3 sweep of the residual ~30 semantic defects: proceeding in parallel where owner-ruling is not required.

CP-D5 cannot close on Q3 completeness until this ruling lands. Q1 landing + AST-egress-gate fix + partial Q3 sweep can land in the interim; the manifest will retain the null-multiplier failure until the ruling arrives.
