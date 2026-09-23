# CP-ENT-16-PILOT-LICENCE-SEEDS · comprehensive receipt · Item 5.11.b

**Seal boundary:** 2026-02-23T~13:15Z · **SO §6.9 amendment §6 verbatim + Ruling (b) AKKI-RUNS-IT verbatim** · §1.2 modality-extension composing sealed CP-ENTITLEMENT-BUILD-WAVE (R-82) `chokepoint_resolver.py` · **RUN-TO-COMPLETION mandate ACTIVE**.

## §1 — What sealed

Three pilot licence seed objects landed structurally at the entitlement-service boundary: `RMS_PILOT_LICENCE_SEED`, `DIGICOW_PILOT_LICENCE_SEED`, `AKKI_TEST_PILOT_LICENCE_SEED` — each frozen with `compute_dial="Managed"` + `frontier_dial="Your Keys"` per SO §6.9 amendment §6 verbatim. Tenant creation seam `create_tenant_with_pilot_licence_seed` refuses without a pilot licence seed present (`TenantCreationRefusedWithoutPilotLicenceSeedError`).

## §2 — Ratchet

| Stage | passed | delta |
|---|---:|---:|
| Pre-authorship (post-CP-SO-6.9-LID-WAVE) | 6332 | — |
| Post-CP-ENT-16 RED-first authorship | 6340 | +8 canonical measured |

`baseline_failures.json` sha256 post-bump: `129abd82ae739afb459a939d20f38c22d45eae27244339b3b56446b65d3f625c`.

## §3 — Modules added

`backend/services/entitlement_service_v1/pilot_licence_seeds_v1.py` (~135 lines · `PilotLicenceSeed_v1` + 3 seed constants + `THREE_TENANT_PILOT_LICENCE_SEEDS` tuple + `create_tenant_with_pilot_licence_seed` + `EVERY_MODEL_CALL_RESOLVES_FROM_DAY_1_POSTURE` Final marker + `TenantCreationRefusedWithoutPilotLicenceSeedError`).

## §4 — Test authorship

- **RED_pre:** 8/8 failed 0.73s (authentic `ImportError` right-reason).
- **GREEN_post:** 8/8 passed 0.71s.
- Test file: `backend/tests/invariants/test_cp_ent_16_pilot_licence_seeds_rms_digicow_akki_test.py`.

## §5 — Double-green byte-identity

- **stripped_sha256:** `1d5895556ccc3c5c80ad25b3d511ed8563d191fa62c570bc43cf7753425ed3f5` IDENTICAL sweep_A (~199s) + sweep_B (~199s) both 6349 passed / 13 skipped / 0 failed / 520 warnings.

## §6 — Objective card

`STATE/OBJECTIVES/CP_ENT_16_PILOT_LICENCE_SEEDS_20260223.md` (promoted from `queued/` · `card_sha256: b50a64f0443e1260c94487aa80ac2495ff27478e487271d8fdf3e0058d0cc31d`).

## §7 — Continuity bundles (SO §6.9(5) AMENDED · 4th application)

- **Code bundle:** `continuity_bundles/code_20260923T125822Z_CP_ENT_16.bundle` · 18.4 MiB · sha256 `8ab58aa418413a08e8b37dc2492dca70e99cadab0e0ad815f0552a59d5ed186f` @ `programme/track-a` `9e3ca45a`.
- **State bundle:** PENDING post-Commit-C-fixup.

## §8 — Fold-in gap closure at this boundary (orthogonal · card-pin drift)

- **Kind:** SO §6.2 hash-pin drift in CP_SO_6_9_LID_WAVE_20260223.md (card had `<computed_at_promote>` placeholder after State-B promotion; would have failed `test_every_card_hash_pin_matches_body` invariant if not caught).
- **Additive fix:** at pre-CP-ENT-16 sweep boundary, computed `card_sha256 = 1f5712e33dde1c044f1a06e5ccadf0ce20639a3eba67e274a41054ee70fab8ee` and pinned it. Discovered during CP-ENT-16 sweep_A pre-authorship failure; resolved additively.
- **Lesson:** future State-B commits MUST pin the card_sha256 before the card moves from `queued/` to `STATE/OBJECTIVES/` (or immediately after promotion, before any sweep). Banked as LESSON at RESUME rewrite.
- **Receipt anchor:** `STATE/OBJECTIVES/CP_SO_6_9_LID_WAVE_20260223.md` line 6.

## §9 — 5-commit seal chain (in flight)

| # | Commit | SHA | Branch |
|---|---|---|---|
| 1 | Code Commit-A | `9e3ca45a9c6382732f52970966df800311eada17` | `programme/track-a` |
| 2 | /app companion A | `2c88897f357072696b08ed4236ef80bcf4db9a84` | `main` |
| 3 | State Commit-B | *(this bank)* | `master` |

## §10 — Ledger check

**This seal implements Item 5.11.b of `EXECUTION_ORDER.md` and nothing else.** Additive-only. No sealed carrier edit. Fold-in orthogonal fix for CP-SO-6.9-LID-WAVE card_sha256 placeholder banked at same boundary per §6.9 desk discipline.
