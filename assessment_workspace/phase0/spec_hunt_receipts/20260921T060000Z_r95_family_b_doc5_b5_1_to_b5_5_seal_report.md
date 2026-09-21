# R-95 · CP-G5V5-DOC5-B5-1-TO-B5-5 · Family B second sub-slice · Seal report

**Wave**: R-95 · CP-G5V5-DOC5-B5-1-TO-B5-5 second sub-slice
**Family**: B (Doc 5 M10 Northena)
**Scope**: SRR rows 75..79 · B5.1..B5.5 · Promise #18 direction half "Objective Preservation (Direction Half)" · all CANON · all Domain=Northena
**Authority**: v5 Master Requirements Registry · SRR sheet · sha-pinned custody workbook sha256 `00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`
**Rule text source**: `fixtures/files_9_extracted/05_Direction_Scope_and_Focus_Part_1_Northena.docx` sha256 `f280356ec9957e14511b60b9561dd0f9ba3d009d9960a870657c0fe0c9ed7cdc` (byte-verified at R-94)
**Owner ruling this-session (verbatim)** — 2026-09-21T~05:20Z:

> "GO — R-95 Family B Part B (B5.1..B5.5 · Promise #18 · Ledger) confirmed as
> the next wave, plan verbatim as you stated it. ... Standing GO continues
> through the G5 family queue per SO §6 — seal reports at boundaries, no
> per-slice check-ins needed. Proceed."

---

## 3-Commit Seal complete

| Position | Repo | Branch | SHA | Timestamp |
|---|---|---|---|---|
| **Commit-A** | Extraction-Akki (CODE) | `programme/track-a` | `c16edf2aee1996d542c03bfce372618b1bdc2893` | 2026-09-21T05:55:00Z |
| **Commit-B** | assessment_workspace (STATE) | `master` | (this-append pending) | 2026-09-21T06:00:00Z |
| **Commit-C fixup** | assessment_workspace (STATE) | `master` | (post-Commit-B pending) | 2026-09-21T06:05:00Z |

---

## Rules registered (verbatim from SRR rows 75..79)

- **B5.1** (row 75) · `The freeze is atomic; the artifact is immutable for the run` [CANON] · docx paragraph index 63
- **B5.2** (row 76) · `Lawful basis is enforced at Admit, before any extraction` [CANON] · docx paragraph index 64
- **B5.3** (row 77) · `Two admission paths, both freezing the same way` [CANON] · docx paragraph index 65
- **B5.4** (row 78) · `The Ledger writer exposes append only` [CANON] · docx paragraph index 66
- **B5.5** (row 79) · `The stamp-audit side-channel is deliberately permissive` [CANON] · docx paragraph index 67

---

## Grep-negative scanners registered (4 · one per rule that explicitly negates a behavior)

- **B5.1** · `scan_for_live_admission_edit` — 5 patterns · rule text "A changed intent is a new admission, never an edit of a live one"
- **B5.2** · `scan_for_downstream_lawful_basis_filter` — 5 patterns · rule text "Purpose limitation is an admission property, not a downstream filter"
- **B5.4** · `scan_for_ledger_update_or_delete` — 6 patterns · rule text "No update path and no delete path exists within the retention window" + "Out-of-scope and refused items are recorded, never silently dropped"
- **B5.5** · `scan_for_side_channel_typing_or_mutation` — 5 patterns · rule text "Typing it would harden it into a mutation surface" + "Unit and audit stay in separate envelopes with separate lifecycles, joined by identity rather than embedded"

**B5.3** carries a shape invariant (two admission paths · both write Ledger row · both freeze the same way) via property test only; no grep-negative scanner because the rule text does not negate a specific behavior pattern.

---

## Delta measured

**+11 MEASURED** (5727 → 5738 · monotonic-up per CCS2 both fields bumped together):
- **+11** new Doc 5 Part B tests (2 registry-shape + 5 property + 4 grep-negative scanner)
- No v8 or other spontaneous transitions this-wave (contrast R-94 which had +2 v8 transitions on top of +14 targeted)

`baseline_failures[]` array NOT shrunk this-slice per R-91 CEREMONY-OPEN owner directive verbatim ("all 5 wrapped baseline failures stay wrapped through Phase 1 and retire ONLY in Phase 2 after the FE landing"). Atomic 5→0 retirement remains scheduled at R-91 apply-step operation 4.

- New `baseline_failures.json` sha256: `44ffe1138a5cc52cbaf9e2bd90ecc078024267a835a840975e031e3a8e7a5c51` (was `a1550d35ec976c70ce7b4ca9b683e00e5b3f6c7cdda2594bd21b121b64b25014` at R-94 seal)
- New `notes/ORCH_BOOT.md` sha256: `c88088e118d30b8cc2fea24f4dbcaa5e85489a3f97a49f01a5a788367ad48108` (byte-identical POD audit mirror sync)

---

## Authentic RED-first cycle

- **RED-pre**: `backend/phase0/drill_receipts/20260921T053800Z_r95_family_b_doc5_b5_1_to_b5_5_RED_pre.log` (11/11 fail collection right-reason `ImportError: cannot import name 'northena_b5_ledger' from 'services.canon_doc5_northena'` module absent)
- **GREEN-post**: `backend/phase0/drill_receipts/20260921T053900Z_r95_family_b_doc5_b5_1_to_b5_5_GREEN_post.log` (11/11 pass 0.71s all B5.1..B5.5)
- **First BASELINE_GUARD=1 sweep-pair (non-deterministic seed · CCS2 hash-seed nondeterminism lesson):**
  - `backend/phase0/drill_receipts/20260921T054100Z_..._run1.log` (182.76s · 5738 passed · 3 baseline-fails · 1 skip · 438 warnings)
  - `backend/phase0/drill_receipts/20260921T054500Z_..._run2.log` (182.56s · 5738 passed · 3 baseline-fails · 1 skip · 438 warnings)
  - Stripped-sha256 DIVERGED: `748c7ff7...` vs `483c1230...` due to `PYTHONHASHSEED` random-per-process affecting the `pod_shell mirror-drift` baseline-failed test's set-iteration order — pytest emits 5-item truncated set diff whose subset shows different items per run.
  - **CCS2 lesson extended this-wave**: force `PYTHONHASHSEED=0` for reproducible byte-identical BASELINE_GUARD=1 double-sweep receipts when any baseline-failed test emits set-iteration-order-dependent assertion output. Recorded for future waves.
- **BASELINE_GUARD=1 deterministic double-sweep byte-identical**: stripped-sha256 `c52c47da48fb555439c896c7c057e09294c9671dacf40efa83627f3f84b8ba23` IDENTICAL across:
  - `backend/phase0/drill_receipts/20260921T055000Z_..._run1.log` (183.52s · 5738 passed · 3 baseline-fails · 1 skip · 438 warnings)
  - `backend/phase0/drill_receipts/20260921T055400Z_..._run2.log` (183.37s · 5738 passed · 3 baseline-fails · 1 skip · 438 warnings)
- Both against post-bump `baseline_failures.json` sha256 `44ffe113...`
- Both under `PYTHONHASHSEED=0 BASELINE_GUARD=1`
- **CCS2 invariant surface (passed count · fail set membership · skipped count · warnings count) matches EXACTLY across all 4 sweeps** (2 non-deterministic-seed + 2 deterministic-seed) — the invariant is stable; only the incidental assertion detail of a baseline-annotated failing test was hash-seed-dependent.

---

## CCS2 measured-not-targeted principle preserved

Pre-Commit-A ratchet bump was set to floor 5738 (targeted +11 for 11 new tests). First sweep measured 5738 (+11 exact). Second/third/fourth sweeps confirmed 5738 (+11). **No CCS2 correction needed** — targeted equalled measured this-wave (contrast R-94 which required 5725→5727 correction pre-double-sweep).

---

## HUNT-first evidence

Already banked at R-94 · unchanged this-wave · covers this-slice rows 75-79:
- `phase0/spec_hunt_receipts/20260921T045000Z_g5v5_family_b_doc5_northena_hunt_data.json` (SRR sha-pin `00072c58` verified · Doc 5 source `.docx` sha `f280356e` verified · 11 rows found at SRR rows 64-79 · this-slice covers 5 B5 rows 75-79 with verbatim docx paragraph indices 63-67 · Part A A5 rows 64-69 sealed at R-94)

---

## Files at Commit-A (9 tracked · code repo `programme/track-a` @ `c16edf2aee1996d542c03bfce372618b1bdc2893`)

1. `backend/services/canon_doc5_northena/northena_b5_ledger.py` (NEW · 305 lines · Final[...] canon vocabulary + 4 scanners for B5.1..B5.5)
2. `backend/tests/invariants/test_g5v5_doc5_b5_1_to_b5_5.py` (NEW · 268 lines · 11 tests)
3. `backend/tests/invariants/baseline_failures.json` (additive: `counts.passed` 5727→5738, `passed_floor` 5727→5738, `ratchet_history` append, `recorded_at_utc` bump to `20260921T054000Z`)
4. `backend/phase0/drill_receipts/20260921T053800Z_..._RED_pre.log` (NEW)
5. `backend/phase0/drill_receipts/20260921T053900Z_..._GREEN_post.log` (NEW)
6. `backend/phase0/drill_receipts/20260921T054100Z_..._BASELINE_GUARD1_run1.log` (NEW · non-deterministic-seed first pair)
7. `backend/phase0/drill_receipts/20260921T054500Z_..._BASELINE_GUARD1_run2.log` (NEW · non-deterministic-seed first pair)
8. `backend/phase0/drill_receipts/20260921T055000Z_..._BASELINE_GUARD1_run1.log` (NEW · deterministic double-green pair · `PYTHONHASHSEED=0`)
9. `backend/phase0/drill_receipts/20260921T055400Z_..._BASELINE_GUARD1_run2.log` (NEW · deterministic double-green pair · `PYTHONHASHSEED=0`)

---

## Files at Commit-B (this-append · state master)

- `STATE/DECISIONS.md` (this-append · seal-report banking · R-95 opening + Commit-A SHA banked)
- `STATE/NEXT.md` (this-append · R-95 marker ⏳ IN-FLIGHT · Family C queued next)
- `notes/ORCH_BOOT.md` (already ratchet-only regen'd pre-Commit-A · sha `c88088e118d30b8cc2fea24f4dbcaa5e85489a3f97a49f01a5a788367ad48108`)
- `/app/frontend/public/audit/ORCH_BOOT.md` (POD audit mirror byte-identical sync at same sha)
- `tools/r95_pre_commit_a_ratchet_and_orch_boot_regen.py` (NEW · deterministic idempotent regen tool mirrors R-94 precedent exactly · zero remote / zero network / zero subprocess / zero git ops · pure local `Path.read_text` + `Path.write_text` + `shutil.copyfile`)
- `phase0/spec_hunt_receipts/20260921T060000Z_r95_family_b_doc5_b5_1_to_b5_5_seal_report.md` (this file · NEW)

---

## Baseline failures at this Commit-B (3 failing / 5 in array · all annotated)

Runtime-failing (3 · all mirror-drift · unchanged from R-94):
- `test_ship_manifest_dod::test_runtime_frontend_app_matches_repo_pod_shell`
- `test_wave_g_pod_shell_frontend_mirror::test_app_frontend_App_js_mirrors_pod_shell_App_js`
- `test_wave_g_pod_shell_frontend_mirror::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir`

Runtime-passing but still in `baseline_failures[]` per R-91 CEREMONY-OPEN directive (2 · v8 cascade · unchanged from R-94):
- `test_v8_substitution_rules_bind_to_rendered_dom::test_every_v8_substitution_rule_binds_to_harness_rendered_dom`
- `test_v8_substitution_rules_bind_to_rendered_dom::test_slot1_registry_aside_marker_present`

Total-coverage guard (Guard #1 from R-88+) verified GREEN across all 4 sweeps. R-86 Property tests (Guard #2 from R-88+) still GREEN (annotation set unchanged this-slice). R-88+ OWNER-RATIFICATION-PENDING RETIRED at `a30db4f7`.

---

## R-91 CP-APP-JS-UNIFY Phase 2 ceremony window

- Countdown horizon: `2026-09-23T03:23:15Z` (unchanged since ceremony-open at `a30db4f7`)
- Current UTC at Commit-B: `2026-09-21T~06:00Z` (< horizon · ~45.4h out)
- **Result**: R-91 stays parked. R-95 Commit-A + Commit-B complete cleanly inside window with zero ceremony-apply operations opened.
- Proposal `notes/proposals/PROPOSAL_r91_r86_property_tests_amendment_20260921.md` unchanged this-slice.

---

## Canon anchors verbatim

- owner ruling this-session (2026-09-21T~05:20Z R-95 Family B Part B GO + standing-GO through G5 family queue per SO §6 · seal reports at boundaries · no per-slice check-ins needed)
- owner ruling prior-session (2026-09-21T~03:53Z Family A GO + standing-GO through R-91 window)
- owner G5-v5 sequencing (2026-09-21T~01:00Z at `a30db4f7`)
- owner Ruling 5 SRR-as-authority (2026-09-20T~19:00Z · v5 workbook sha `00072c58...`)
- owner Ruling 3 erratum (class column HINT · rule text governs · source-column shape extended this-session)
- v5 SRR workbook rows 75..79 as authority (Ruling 5)
- Doc 5 source `.docx` sha `f280356ec9957e14511b60b9561dd0f9ba3d009d9960a870657c0fe0c9ed7cdc` (byte-verified at R-94)
- **R-94 seal `1115a332`/`98963a11`/Commit-C fixup (immediately-precedes · Family B first sub-slice · CP-G5V5-DOC5-A5-1-TO-A5-6 Part A · establishes Final[...]-constants + pure-data-in-scanner + grep-negative-ban-anchor pattern this wave inherits)**
- R-93 seal `36668e3`/`ee30ca98`/`de4f31bd` (Family A · Doc 1 M12 chokepoint)
- R-92 seal `ceaa24f`/`19030610`/`e8f9f168`
- R-91 Phase 1 seal `282ba19e` + R-91 CEREMONY-OPEN `a30db4f7`
- R-90/R-89/R-88 seal chain + prior R-85/R-86/R-87 seal chain
- SO §2.5/§3/§3.3/§3.8/§3.10-α/§6/§6.4/§6.7 + M16-W3 corrected order + CCS2 lesson (extended this-wave with hash-seed nondeterminism lesson)

---

## Stop-conditions this-commit

- Stop-conditions #1/#2/#3 NOT triggered this-slice.
- SO §6.4 pre-ruling NOT triggered.
- MEM-R-053 CROWN BAN NOT triggered.
- No push · zero remote configured on `programme/track-a` · **no `testing_agent`** (STRICTLY BANNED per SO §6).

---

## Autopilot next

**Commit-C fixup** (state master · R-6 boundary regen advancing `heads_last_sealed.state_repo.head` to this Commit-B SHA + new code_repo history entry for `c16edf2` · R-95 second-sub-slice marker flips ⏳ IN-FLIGHT → ✅ SEALED · POD audit mirror byte-identical sync reconfirmed).

**Then G5-v5 Family C first sub-slice** (DAP-1..38 lifecycle and principal model landing · Tier A first) per owner sequencing.

---

## Standing bounds unchanged

zero push · zero remote configured · terminal `pytest` only · **no `testing_agent`** (STRICTLY BANNED per SO §6) · additive-only §3.8 (with ceremonied R-91 amendment as SINGLE authorized exception at horizon) · three-repo discipline · ratchet measured-monotonic-up **5738** floor · HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged · R-88+ OWNER-RATIFICATION-PENDING RETIRED at `a30db4f7`.

**End of R-95 · Family B second sub-slice · Doc 5 B5.1..B5.5 · Commit-A + Commit-B seal-report.**
