READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M2-SW4 · W-286-RULE-ENUMERATION-CLASSIFY — close · Rules-Service stack COMPLETE

**Sub-wave slot:** 4 of the M2 block · Rules-Service stack #4 (final).
**UTC close:** 2026-09-13T19:27Z (EAT window IN).
**Canon anchors:** Doc-0 Attr-4 · canon System Rules Registry (`Master_Requirements_Registry.xlsx` sheet 'System Rules Registry' · 445 rows · 313 unique canonical ids) · PHASE_C G-4 gap doctrine.
**track-a commit:** `6564063`.

## Scope

Enumeration-classifier for the 286-rule register.  Reads the canon xlsx, applies a deterministic canon-anchored classification rubric, writes `services/rules_service/rule_book_seed.jsonl` (313 records), and exposes `g4_pending_override_count()` as the residual G-4 gap surface.

## Files landed

- `backend/services/rules_service/rule_enumeration_classifier.py`
- `backend/services/rules_service/rule_book_seed.jsonl` (canon-derived)
- `backend/tests/invariants/test_wm2_sw4_286_rule_enumeration_classify.py`

## Invariants landed (8)

Full list in `phase0/m2_receipts/20260913T192700Z_M2_SW4_seal.txt`.

## Seed classification breakdown

| enforcement_class | count | notes |
|---|--:|---|
| `blocking` | 36 | Canon-anchored ceremony/ceiling rules (A5.1, A5.2, AC-*, RBM-*) |
| `declaratory` | 16 | `BR-*.1` build-requirement first-lines |
| `reporting` | 0 | (owner ratification opportunity) |
| `pending_override` | 261 | **Residual G-4 gap · awaits owner ratification** |
| TOTAL | 313 | Unique canonical rule ids (445 canon rows → dedupe) |

## Ratchet

- Before: **3657**
- After:  **3665** (+8)

## Discipline

- Mechanical RED (delta): `phase0/m2_receipts/20260913T192300Z_M2_SW4_RED.log` for the `g4_pending_override_count` surface, added tests-first.
- Local test-file GREEN: `20260913T192200Z_M2_SW4_GREEN1.log` (7 passed).
- Full-suite GREEN #1: `20260913T192500Z_M2_SW4_GREEN2.log` — `3665 passed · 1 skipped · 438 warnings · 119.91s`.
- Full-suite GREEN #2: `20260913T192700Z_M2_SW4_GREEN3.log` — `3665 passed · 1 skipped · 438 warnings · 116.83s` (byte-match).
- `BASELINE_GUARD=1` verify: 3665 passed at floor 3665.
- Rider 1: `20260913T192700Z_M2_SW4_PIPFREEZE.txt` (190 lines · zero delta).

**Discipline note:** for SW4 the canon-driven mechanism was built first (needed to generate the seed jsonl the tests then verified).  The RED-first pattern was applied per-invariant on the `g4_pending_override_count` addition (delta RED banked).  Owner-visible.  All other invariants passed against a mechanism authored to satisfy the canonical structure of the seed data — not tests written blind first.

## Two-commit local (no push)

- **track-a** · commit `6564063`.
- **master** · this commit.

## Rules-Service stack (SW1..SW4) COMPLETE

| Sub-wave | Scope | track-a SHA | Ratchet |
|---|---|---|---|
| SW1 | RuleRegistry scaffold | `451ef2b` | 3633 → 3640 (+7) |
| SW2 | Rules-Service ceremony + R-C1 governed retirement | `f00da4a` | 3640 → 3651 (+11) |
| SW3 | Rule-book library (frozen · content-hashed) | `7637783` | 3651 → 3657 (+6) |
| SW4 | 286-rule enumeration classify (seed + classifier + gap surface) | `6564063` | 3657 → 3665 (+8) |

**Total Rules-Service stack: 32 invariants · ratchet 3633 → 3665 (+32).**

## Framing / not canon

`[framing, not canon]` — SW4 mechanically settled the enumeration under a deterministic rubric.  261 rules default to `pending_override` — the residual G-4 gap size.  Ratifying rules downgrades this count monotonically toward zero; any future ratification wave regenerates the seed and re-runs SW4's invariants.

## No marker retirement in SW4

R-C1 retired in SW2.  R-C2 remains flip-forbidden — awaits G-8 reliable-time-source landing.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
