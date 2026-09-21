# OPEN-CARD SWEEP · COMPLETION SPRINT step 3 · consolidated owner-line list

**Sweep at UTC**: 2026-09-21T07:20:00Z
**Sprint step**: 3 of 6 · immediately-post R-98 seal (Family D closed)
**Scope**: every card under `STATE/OBJECTIVES/` (10 cards)
**Method**: read each card's front-matter status + trace history in `STATE/DECISIONS.md` git log for seal chains

---

## Card status matrix (10 cards)

| Card | Front-matter says | Verified from banking history | Verdict |
| --- | --- | --- | --- |
| `M10_W2_W3.md` | `milestone_status: SEALED` | M10-W2/W3 SEALED (Milestone 1) | ✅ CLOSED |
| `M10_W4.md` | `milestone_status: CLOSED · W4a+W4b+W4c+W4d+W4e all sealed` | Milestone 2 all 5 sub-waves sealed | ✅ CLOSED |
| `M12b_W1.md` | `milestone_status: UPCOMING · gated on M10-W4 close, W1f confirmation banked, Canon-8 G5 rules mapped` | **MILESTONE 3 OPENER SEALED at CP-M12b-W1-CALLER-FLIP-VERDICT-SCHEMA-ED25519 Commit-A `60cc61e1` / Commit-B `179df4e4ea822ce7ac63c955a43ff8d91890fb55` (2026-09-19T~04:20Z · all 4 MUST-DOs landed with double-green byte-identical proof · gates i/ii/iii cleared · ratchet 5238 → 5279 +41)** — front-matter stale | ⚠️ **CLOSABLE · closes with this-sweep additive status-append** (front-matter untouched · card_sha256 unchanged per SO §3.8 additive-only) |
| `M13.md` | `milestone_status: CLOSED · all 5 sub-waves W1-W5 sealed` | Milestone 4 all 5 sub-waves closed at CP-M13-W5-B10-RUNBOOKS 2026-09-19T~06:10Z | ✅ CLOSED |
| `M14.md` | `milestone_status: CLOSED · sealed at CP-M14-W5-SEAL-INTEGRATION` | Milestone 5 all 5 sub-waves closed 2026-09-19T~08:55Z | ✅ CLOSED |
| `M15.md` | `milestone_status: CLOSED · all 5 sub-waves W1..W5 sealed` | Milestone 6 all 5 sub-waves closed 2026-09-19T~10:29Z | ✅ CLOSED |
| `M16.md` | `milestone_status: CLOSED · 5 sub-waves W1..W5 all sealed` | Milestone 7 CIF all 5 sub-waves closed 2026-09-19T~12:31Z | ✅ CLOSED |
| `M17.md` | `milestone_status: CLOSED (post-fork sub-wave W6 · fork closed by Option-i landed)` | Milestone 8 all 6 sub-waves (W1..W5 + W6 fork-closure) sealed | ✅ CLOSED |
| `ENTITLEMENT.md` | `wave_status: OPEN · WAVE R-81 · CP-ENTITLEMENT-WAVE-SETUP · sub-wave 1 of 2` | **R-81 SETUP SEALED at Commit-A `fc8b5c0` / Commit-B `c3cc7451` / Commit-C `16c9d912` (21 property tests · ratchet 5621) AND R-82 BUILD SEALED at Commit-A `c4bf7094d4c6553973f78bc2104b70134167ffe0` / Commit-B `eff17295f4d98248ead46c7102ba0e0f1adac424` / Commit-C `7d1e66a9` (2026-09-20T~16:11Z · 7 new modules in services/entitlement_service_v1/ · Phase-2 structural enforcement active · zero baseline shrink)** — front-matter stale | ⚠️ **CLOSABLE · closes with this-sweep additive status-append** (front-matter untouched per SO §3.8) |
| `CP_APP_JS_UNIFY.md` | `milestone_status: SCHEDULED (not-open-ended) · slot R-91 · closure trigger for the three pod_shell mirror-drift baseline entries + CP10 harness receipt vacuous-pass restoration` | R-91 Phase 1 SEALED at `282ba19e`; R-91 CEREMONY-OPEN banked at `a30db4f7` (2026-09-21T~01:00Z) · APPLY horizon **`2026-09-23T03:23:15Z` NO EXPEDITE** per owner ruling 2026-09-21T~06:15Z verbatim | ⏳ **RIGHTLY OPEN · cannot close until horizon** (RBM-8 ceremony-mechanic anchor enforces this in code as of R-98 seal · SO §6.6 "a countdown cut short is what FAIL looks like") |

---

## Consolidated owner-line list (no halt — reporting-only)

**Closable-with-status-append this sweep (2 cards):**

1. **`M12b_W1.md`** — front-matter says UPCOMING; MILESTONE 3 OPENER actually SEALED at `179df4e4` (2026-09-19T~04:20Z). Status-append lands additively (SO §3.8) at bottom of card noting seal chain; front-matter `card_sha256: 0bc8b267…` untouched (§6.2 discipline: milestone_status stays on-card as ratified; gate-satisfaction recorded in DECISIONS + NEXT + seal notes, not in-card). No `card_sha256` re-pin needed.

2. **`ENTITLEMENT.md`** — front-matter says OPEN · WAVE R-81 sub-wave 1 of 2; both R-81 setup (`fc8b5c0/c3cc7451/16c9d912`) and R-82 build (`c4bf7094/eff17295/7d1e66a9`) SEALED (2026-09-20T~15:00Z + 2026-09-20T~16:11Z). Status-append lands additively at bottom of card noting both seal chains; front-matter `card_sha256: 46f4a6e7…` untouched (this is pinned in R-82 test evidence at `test_wave_setup_spec_docx_source_sha256_byte_verified`; must not change).

**Legitimately open (1 card):**

3. **`CP_APP_JS_UNIFY.md`** — R-91 CEREMONY-OPEN parked · frozen horizon `2026-09-23T03:23:15Z` · NO EXPEDITE ruling verbatim in code at RBM-8 sub-invariants (`RBM_8_R91_LIVE_EVIDENCE_HORIZON_UTC="2026-09-23T03:23:15Z"` · `RBM_8_R91_IS_LIVE_EVIDENCE_RECEIPT=True`). Closes atomically at horizon per owner-ruled 10-operation apply-step at COMPLETION SPRINT step 5.

**All other 7 cards (M10_W2_W3, M10_W4, M13, M14, M15, M16, M17):** CLOSED. Nothing to do.

---

## Actions taken this sweep

Two status-appends land additively at the bottom of `M12b_W1.md` and `ENTITLEMENT.md` per SO §3.8 (additive-only · zero front-matter edit · zero `card_sha256` change). Each append cites the actual seal chain SHAs and dates for anti-forget reference. The card headers remain unchanged per §6.2 discipline (milestone_status ratified value stays on-card; retroactive corrections land in appended sections).

## R-91 posture at this sweep

R-91 CP-APP-JS-UNIFY Phase 2 remains **PARKED** at frozen horizon `2026-09-23T03:23:15Z` (~44.1h out at sweep time). RBM-8 encoded in code as of R-98 seal (`38eeef6c` on programme/track-a) as the ceremony-mechanic anchor: **ceremony windows are rigid** (`RBM_8_CEREMONY_WINDOW_IS_RIGID: Final[bool] = True`), **no shortening path exists in code** (`RBM_8_NO_SHORTENING_PATH_IN_CODE: Final[bool] = True` + `scan_for_ceremony_shortening_path` 5-pattern grep-negative scanner), and **R-91 window is the live evidence receipt** (`RBM_8_R91_LIVE_EVIDENCE_HORIZON_UTC="2026-09-23T03:23:15Z"` + `RBM_8_R91_IS_LIVE_EVIDENCE_RECEIPT: Final[bool] = True`).

---

## Autopilot next per COMPLETION SPRINT sequence

Step 4 · **LIFECYCLE/ENTITLEMENT HTTP SURFACE** — additive routers only, RED-first invariants on routers, expose `/api/openapi.json`, flag `FE-WIRING-READY` with endpoint list + auth requirements + sample payloads → Step 5 · **R-91 ε-APPLY** at horizon `2026-09-23T03:23:15Z` NO EXPEDITE → Step 6 · **FINAL CLOSURE REPORT**.
