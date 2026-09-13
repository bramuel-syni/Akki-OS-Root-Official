READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M2-SW2 · W-RULES-SERVICE-CEREMONY — close (R-C1 RETIRED)

**Sub-wave slot:** 2 of the M2 block · Rules-Service stack #2 (of 4).
**UTC close:** 2026-09-13T18:51Z (EAT window IN).
**Canon anchors:** Doc-0 Attr-4 · Attr-9 rolled in · `Ratification_Record_v1` Table 2 R-1/R-2/R-3/R-4 · Canon-1 §4.10 · Canon-3 §22 · PHASE_C R-C1 retirement doctrine.
**track-a commit:** `f00da4a`.

## Ceremony mechanism landed

Rules-Service ceremony surface: `RuleFlipRequest` → `start_rule_flip()` → `attempt_apply_rule_flip()` with fail-closed on every gate (countdown / witness / signatory / business-type / registry-collision).  Wired to `services.rulings.default_class_constants` for R-1 countdown values.  Records a new rule to the singleton `RuleRegistry` (SW1) on successful ceremony completion — Canon-3 §22 additive.

## R-C1 · Governed retirement

- **Marker:** `R_C1_RULES_SERVICE_NOT_BUILT_FALLBACK_TRUE` on `contracts/asset_registry.py:53`.
- **Before:** `True` (flip-forbidden; Rules Service not built).
- **After:** `False` (Rules Service present; retirement backed by mechanism).
- **Enabling commits:**
  - `track-a:451ef2b` — W-M2-SW1 · `services/rules_service/rule_registry.py` (register scaffold).
  - `track-a:f00da4a` — W-M2-SW2 · `services/rules_service/ceremony.py` (change-control ceremony).
- **Retirement invariant:** `test_wm2_sw2_rules_service_ceremony.test_sw2_r_c1_retirement_backed_by_mechanism` asserts that when the marker is `False`, BOTH `rule_registry` and `ceremony` modules must be importable AND their key surfaces callable.  Silent re-flip in either direction is impossible without touching this test in the same commit.
- **Existing G3-CP-R2 R-C1 marker test updated in the same commit:** `test_wregext_g3_cp_r2_r_c1_marker_present` (renamed from `..._and_true`) now asserts `False` with the retirement lineage cited in the docstring — governance intent visible in the failing-hard test on any future silent flip.
- **`baseline_failures.json.ratchet_history`** entry appended with `marker_retired: "R-C1_RULES_SERVICE_NOT_BUILT_FALLBACK_TRUE"` + `enabling_commits` list.

## Discipline

- Mechanical RED: `phase0/m2_receipts/20260913T184700Z_M2_SW2_RED.log` (11 fails · right-reason `ModuleNotFoundError` pre-impl).
- Full-suite GREEN #1: `20260913T184900Z_M2_SW2_GREEN1.log` — `3651 passed · 1 skipped · 438 warnings · 115.67s`.
- Full-suite GREEN #2: `20260913T185100Z_M2_SW2_GREEN2.log` — `3651 passed · 1 skipped · 438 warnings · 116.71s` (byte-match).
- `BASELINE_GUARD=1` verify: floor honored at 3651 (117.10s).
- Rider 1: `20260913T185100Z_M2_SW2_PIPFREEZE.txt` (190 lines · zero delta).

## Ratchet

- Before: **3640** (SW1 close)
- After:  **3651** (+11)

## Two-commit local (no push)

- **track-a** · commit `f00da4a`.
- **master** · this commit.

## Outstanding DEFAULT-PENDING-OVERRIDE markers introduced by SW2

- `services.rules_service.ceremony.SECOND_SIGNATORY_ROLE_PENDING_OVERRIDE = "PENDING-OVERRIDE"` — Rules-Service R-2 (OPEN owner-input · `Ratification_Record_v1` Table 2).  Production ceremony awaits owner ruling on the named role.  Mechanism accepts any non-empty `second_signatory_id`; role name pending.

## Framing / not canon

Attr-9 (Change-Control) rolls INTO Rules-Service ceremonial per `BUILD_STATUS §2 row 4i`.  Discharged by SW2.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
