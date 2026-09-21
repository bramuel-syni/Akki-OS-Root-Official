# R-93 · CP-G5V5-DOC1-A5-1-TO-A5-9 first sub-slice · SEAL REPORT

**Emitted**: 2026-09-21T04:47:00Z
**Wave**: R-93 · G5-v5 Family A · Doc 1 M12 chokepoint · A5.1..A5.9
**Ruling**: Ruling 5 execution (SRR-as-authority · v5 workbook sha `00072c58...`)
**Status**: ✅ SEALED · 3-Commit Seal COMPLETE
**Owner ruling this-session verbatim** (2026-09-21T~03:53Z): "GO — Family A first sub-slice HUNT-and-authoring, exactly per your posture plan ... Standing GO extends through the R-91 window: Family A → Family B (Doc 5 Northena) → DAP-1..38 → RBM + ROC, Tier A before Tier B per the owner's sequencing, sub-slice sizes at your discretion for clean seals, no per-slice check-ins needed (SO §6 governs)."

---

## 3-Commit Seal

| Position | Repo | Branch | SHA | Timestamp |
|---|---|---|---|---|
| **Commit-A** | Extraction-Akki (CODE) | `programme/track-a` | `36668e371bd4c99d0a0ee3ffde706b1bf4a34af3` | 2026-09-21T04:00:00Z |
| **Commit-B** | assessment_workspace (STATE) | `master` | `ee30ca980a1e61c45db858444a91894fa7e65513` | 2026-09-21T04:15:00Z |
| **Commit-C fixup** | assessment_workspace (STATE) | `master` | `de4f31bd27f8595ad0ea3851111efadef7132e54` | 2026-09-21T04:45:00Z |

---

## Delta measured

**+16** monotonic-up per CCS2 (5695 → 5711 both `counts_at_baseline.passed` and `invariants_enforced_when_baseline_guard_1.passed_floor` bumped together).

Component breakdown:
- +2 registry-shape tests (`DOC1_A5_RULE_IDS` 9-tuple · shared row metadata)
- +9 property tests (one per A5.1..A5.9 · SRR row R2..R10 · verbatim rule text)
- +5 grep-negative scanner tests (A5.1, A5.3, A5.5, A5.7, A5.9)

No test flipped fail→pass this-slice · no test flipped pass→fail this-slice.

---

## Files landed

### Commit-A (code · programme/track-a)

- `backend/services/canon_doc1_chokepoint/__init__.py` (NEW · SO §2.5 verbatim-docstring package marker)
- `backend/services/canon_doc1_chokepoint/chokepoint_vocabulary.py` (NEW · registers `DOC1_A5_RULE_IDS`, `DOC1_A5_RULE_COUNT`, per-rule `Final[...]` bindings for statement + source + invariant flags, 5 pure-data-in grep-negative scanners)
- `backend/tests/invariants/test_g5v5_doc1_a5_1_to_a5_9.py` (NEW · 425 lines · 16 tests · SO §2.5 verbatim-docstring discipline)
- `backend/tests/invariants/baseline_failures.json` (additive: counts+floor 5695→5711, ratchet_history append, `recorded_at_utc` bump)

### Commit-B (state · master)

- `STATE/DECISIONS.md` (seal-report banking · owner ruling verbatim · 5 binding conditions · sequencing verbatim · canon anchors)
- `STATE/NEXT.md` (R-93 marker ⏳ IN-FLIGHT · sprint queue post-R-93)
- `STATE/PINS.md` (R-93-FIRST-SUB-SLICE-PINS block)
- `notes/ORCH_BOOT.md` (pre-Commit-A ratchet-only regen · `passed_floor` 5695→5711 · new baseline sha `870eac9a`)
- `/app/frontend/public/audit/ORCH_BOOT.md` (POD audit mirror byte-identical sync)
- `tools/r93_pre_commit_a_ratchet_and_orch_boot_regen.py` (NEW)
- `phase0/spec_hunt_receipts/20260921T033330Z_g5v5_family_a_doc1_m12_chokepoint_hunt_data.json` (NEW)
- `phase0/spec_hunt_receipts/20260921T033330Z_g5v5_family_a_doc1_m12_chokepoint_hunt_receipt.md` (NEW)
- `phase0/spec_hunt_receipts/20260921T034200Z_g5v5_family_a_doc1_source_doc_false_negative_correction_addendum.md` (NEW · falsifies prior fork's `.md`-missing misreport)
- `phase0/spec_hunt_receipts/20260921T034500Z_g5v5_family_a_doc1_a5_1_to_a5_9_authoring_hunt_data.json` (NEW)
- Multiple drill receipts in `backend/phase0/drill_receipts/` (RED-pre + GREEN-post + double-sweep run1 + run2)

### Commit-C fixup (state · master · this-seal)

- `notes/ORCH_BOOT.md` (R-6 boundary regen: state_repo.head `ee30ca98` + new code_repo entry for `36668e3` · new sha `9c234e2534a97f745fdf91bbbcb8b07d50f7622cb9bd89481177d4a6b2679d29`)
- `/app/frontend/public/audit/ORCH_BOOT.md` (POD audit mirror byte-identical)
- `tools/r93_commit_c_fixup_orch_boot_regen.py` (NEW · mirrors R-92 precedent exactly)
- `STATE/DECISIONS.md` (Commit-C banking with R-6 regen evidence + `ee30ca98` full-40 + short banking)
- `STATE/NEXT.md` (R-93 marker ✅ SEALED · sprint queue post-R-93)

---

## Byte-identity evidence

**Pre-Commit-A double-green BASELINE_GUARD=1 sweep** (banked at Commit-B):
- run1: stripped-sha256 `ee3e1fb7...` · 5711 passed · 5 baseline-fails · 1 skip · 438 warnings
- run2: stripped-sha256 `ee3e1fb7...` (IDENTICAL) · 5711 passed · 5 baseline-fails · 1 skip · 438 warnings
- baseline_failures.json sha256: `870eac9a06f25cbf2b5591b9084bbb9c4a1555719ac183f9c8dfd44700cf18b1`

**Pre-Commit-C verify subset** (banked at Commit-C):
- 36/36 GREEN in 0.99s at `backend/phase0/drill_receipts/20260921T044000Z_r93_pre_commit_c_verify_subset.log`

**Post-seal verify subset** (this-receipt):
- 36/36 GREEN in 0.98s at `backend/phase0/drill_receipts/20260921T044600Z_r93_post_seal_verify_subset.log`
- Test breakdown: R-93 wave 16/16 + `test_orch_boot` 1/1 + baseline manifest 12/12 + R-86 property tests 5/5 + R-88 total-coverage guards 2/2

**Post-fixup ORCH_BOOT byte-identity**:
- `notes/ORCH_BOOT.md`: sha256 `9c234e2534a97f745fdf91bbbcb8b07d50f7622cb9bd89481177d4a6b2679d29`
- `/app/frontend/public/audit/ORCH_BOOT.md`: sha256 `9c234e2534a97f745fdf91bbbcb8b07d50f7622cb9bd89481177d4a6b2679d29`
- IDENTICAL ✅

---

## Ratchet state at seal

| Field | Value |
|---|---|
| `passed_floor` | **5711** |
| `counts_at_baseline.passed` | **5711** |
| `counts_at_baseline.failed` | 5 (unchanged from R-88+) |
| `counts_at_baseline.skipped` | 1 |
| `baseline_failures.json` sha256 | `870eac9a06f25cbf2b5591b9084bbb9c4a1555719ac183f9c8dfd44700cf18b1` |
| `notes/ORCH_BOOT.md` sha256 | `9c234e2534a97f745fdf91bbbcb8b07d50f7622cb9bd89481177d4a6b2679d29` |
| `heads_last_sealed.state_repo.head` | `ee30ca980a1e61c45db858444a91894fa7e65513` |
| `heads_last_sealed.code_repo.head` (newest) | `36668e371bd4c99d0a0ee3ffde706b1bf4a34af3` |

---

## Baseline failures (5 · all annotated · covered by exactly one annotation field · Total-coverage guard GREEN)

Unchanged from R-88+/R-89/R-90/R-92 carry-forward. All 5 wrap the same `dc48d5313` App.js divergence with `CP-APP-JS-UNIFY` scheduled closure at R-91:

3 pod_shell mirror-drift (annotated under `known_runtime_drift_annotations`):
- `test_ship_manifest_dod::test_runtime_frontend_app_matches_repo_pod_shell`
- `test_wave_g_pod_shell_frontend_mirror::test_app_frontend_App_js_mirrors_pod_shell_App_js`
- `test_wave_g_pod_shell_frontend_mirror::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir`

2 v8 cascade (annotated under `known_r91_closure_scheduled_receipt_drift_annotations`):
- `test_v8_substitution_rules_bind_to_rendered_dom::test_every_v8_substitution_rule_binds_to_harness_rendered_dom`
- `test_v8_substitution_rules_bind_to_rendered_dom::test_slot1_registry_aside_marker_present`

R-86 Property tests all GREEN (annotation set unchanged this-slice · disjoint-field discipline preserved).

---

## R-91 CP-APP-JS-UNIFY Phase 2 ceremony window

- Countdown horizon: `2026-09-23T03:23:15Z` (unchanged since ceremony-open at `a30db4f7`)
- Current UTC: `2026-09-21T04:33:41Z` (verified via `date -u -Iseconds`)
- **Result**: `current < horizon` → R-91 stays parked. R-93 seal completes cleanly inside window with zero ceremony-apply operations opened.
- Proposal `notes/proposals/PROPOSAL_r91_r86_property_tests_amendment_20260921.md` unchanged this-slice.
- R-91 apply-step post-apply (per proposal §6): baseline set 5→0 · `known_runtime_drift_annotations` 3→0 · `known_r91_closure_scheduled_receipt_drift_annotations` 3→1 (retain cp10-still-recent) · `counts.passed` 5711 → 5716 measured (3 remaining baselines transitioning fail→pass · revised from proposal §6's 5700 prediction).

---

## R-88+ OWNER-RATIFICATION-PENDING

RETIRED at state commit `a30db4f7` (R-91 CEREMONY-OPEN · D+A ratification banked verbatim per owner ruling this-session 2026-09-21T~01:00Z). Not restated this-Commit-C.

---

## Standing bounds unchanged

- zero push · zero remote configured on `programme/track-a`
- terminal `pytest` only · **no `testing_agent`** (STRICTLY BANNED per SO §6 Long Autonomous Run Protocol)
- additive-only §3.8 (with ceremonied R-91 amendment as SINGLE authorized exception at horizon)
- three-repo discipline (`programme/track-a` CODE · `master` STATE · `main` frontend POD audit mirror)
- ratchet measured-monotonic-up floor **5711**
- HF-HOLD SEC-2026-09-12-01 remains OPEN
- R-24 remains UNLISTED
- R-25 defaults tagged

---

## Autopilot next: G5-v5 Family B (Doc 5 M10 Northena) sub-slice HUNT-and-authoring

Per owner G5-v5 second slice sequencing verbatim (2026-09-21T~01:00Z at `a30db4f7`): "Document 1 (chokepoint, M12) and Document 5 (the Ledger, M10) first; then DAP-1 through DAP-38 (lifecycle and principal model landing); then RBM and ROC (Rules Service). Tier B rows in each family trail their Tier A. Sequence rows 1–565 accordingly."

Per owner standing-GO through R-91 window verbatim (2026-09-21T~03:53Z): "Standing GO extends through the R-91 window: Family A → Family B (Doc 5 Northena) → DAP-1..38 → RBM + ROC, Tier A before Tier B per the owner's sequencing, sub-slice sizes at your discretion for clean seals, no per-slice check-ins needed (SO §6 governs)."

**Immediate next actions** (autonomous · no owner check-in):
1. HUNT-first: extract Doc 5 M10 Northena rule text from `fixtures/files_9_extracted/05_Direction_Scope_and_Focus_Part_1_Northena.docx` byte-verified + v5 SRR workbook (`00072c58…`) Tier A rows for M10.
2. Sub-slice size at autopilot discretion for clean seals.
3. Author new `services/canon_doc5_northena/` package + property/scanner tests per Family A pattern.
4. RED-first → GREEN → measured ratchet → double-green byte-identical → 3-Commit Seal.

---

**End of R-93 seal-report. G5-v5 Family A first sub-slice CLOSED. Family B opens next.**
