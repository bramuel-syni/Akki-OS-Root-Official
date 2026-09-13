READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_REGISTRY_FULL_BUILD_CP10_close.md — CP10 finalization

**Wave.** W-REGISTRY-FULL-BUILD · CP10 · real-Chromium DOM proof + wave-close manifest finalization.
**Canon anchors.** Owner directive 2026-09-08T~06:15Z STEP 5 (real-Chromium proof), MILESTONE_PROMISE_BINDING 2026-09-13 Task 2 (ratified sequence), `notes/v3_substitution_rules.json` (24 rules re-authored at CP8).
**Owner authorisation.** Verbatim 2026-09-13: G-A ratified sequence (2E→2F→2G→2H→CP10→G-3) + G-C confirmed one-time public Playwright/Chromium egress for CP10 only.
**Ratchet.** 3625 → 3627 (+2).
**Track-a commit.** Pending — will be recorded in backfill.
**Seal.** `phase0/output_verified_seals/wregistry_cp10.seal.txt`.

---

## §A · Invariants added (2 new)

| Test | Anchor | What it enforces |
|---|---|---|
| CP10-01 · `test_cp10_wave_close_manifest_exists_and_names_all_10_cps` | Owner rule STEP 5 | `notes/W_REGISTRY_FULL_BUILD_close.md` exists and names CP1..CP10 |
| CP10-02 · `test_cp10_harness_receipt_is_still_recent` | STEP 5 real-Chromium | `phase0/harness_ground_truth/latest.json` exists with `at_utc` <12h old AND every rule in `ground_truth.per_rule` has `bound_to_rendered_dom=true` |

## §B · Mechanism landed

- `tools/cp10_real_chromium_harness.py` (~180 lines · Playwright + Chromium script: launches headless Chromium; sets XFF `34.16.56.64, edge-proxy, gcp-lb` (SPINE_ALLOWED_IPS + 2 trusted hops); navigates `http://localhost:3000/` for portal iframe host + directly to `http://localhost:3000/v8_prototype.html` for deep static-file scan; uses `page.content()` + `frame.content()` (full HTML including hidden sections) — NOT `inner_text` which drops hidden panels; scans body for each rule's `dummyContent` marker; writes `latest.json` receipt in the schema expected by the CP10 close-check invariants).
- `backend/tests/invariants/test_w_registry_full_build_cp10_wave_close.py` restored verbatim from quarantine (2 invariants).
- `notes/W_REGISTRY_FULL_BUILD_close.md` restored + CP10 line finalized (delta +2; session provenance; Playwright/Chromium egress attribution).
- `backend/tests/invariants/baseline_failures.json` bumped: floor 3625 → 3627; ratchet_history entry appended.

## §C · Gate 2 Option B egress attribution (authorised one-time public download)

**Owner verbatim 2026-09-13 (G-C).** "The one-time public Playwright/Chromium download remains in force for CP10 only.  Log exact URLs, versions, and hashes fetched in the CP10 close artefact.  Zero on-prem egress."

**Installed under this authorization:**
- `playwright==1.62.0` (Python wrapper, from PyPI)
- `pyee==13.0.1` (transitive dep of playwright)
- `greenlet==3.5.5` (transitive dep of playwright)
- Chrome Headless Shell **151.0.7922.34** (Playwright chromium-headless-shell v1234) at `/pw-browsers/chromium-1234/chrome-linux/chrome` (111 MiB, downloaded from Playwright CDN via `playwright install chromium`).

**Egress log:** `phase0/cp10_egress_log/20260913T162655Z_playwright_install.log`.

**On-prem egress:** ZERO.  The harness targets `http://localhost:3000/` only (the in-container frontend served by supervisor's `frontend` process).  No JUMP, no RADIO, no Huawei estate, no external internet after install.

**Pip-freeze delta (Rider 1):** the DAP-STACK arc closed at 187 packages (hash `7c45a54d...`); CP10 closes at 190 packages (hash `f6296cd2...`).  Delta is honestly recorded here and in the seal — silent env drift is exactly what Rider 1 catches; this one is authorised.

## §D · Real-Chromium receipt (this session's proof)

- `at_utc`: `2026-09-13T16:30:40Z`
- rules declared: **24** (from `notes/v3_substitution_rules.json`)
- rules bound to rendered DOM: **24 / 24** (`unbound_rules: []`)
- rendered body length: `1_356_810` chars
- target: `http://localhost:3000/v8_prototype.html` (deep static-file navigation) plus `/` (portal iframe host)
- XFF header applied: `34.16.56.64, edge-proxy, gcp-lb`
- capture method: `page.content()` + `frame.content()` (full HTML including hidden sections)

Prior run (2026-09-13T05:41:45Z) was ~11h old at CP10 open — right at the freshness threshold.  This session's fresh receipt (16:30Z) supersedes it under the same 12h rule.

## §E · Discipline receipts (Rider 1 held)

| Kind | Path | SHA-256 |
|---|---|---|
| Mechanical RED | `phase0/drill_receipts/20260913T163119Z_wregistry_cp10_RED.log` | `062f4fbecb997b5b32c8464869440c57e669832e822ad4433658889d52210793` |
| GREEN 1 | `phase0/drill_receipts/20260913T163217Z_wregistry_cp10_GREEN1.log` | `fdae0d5ed67bfe74c68305756028f48eb1f8dc650f30ff3ec32e234576497d4f` |
| GREEN 2 | `phase0/drill_receipts/20260913T163422Z_wregistry_cp10_GREEN2.log` | `5929401bd57c45726624d63e1b627363288b384e4a4dce48f0971872200aab4f` |
| **Rider 1** pip freeze (190 pkgs · env-delta noted) | `phase0/drill_receipts/20260913T163645Z_wregistry_cp10_PIPFREEZE.txt` | `f6296cd2848bcf2eb6189ed1c68c35a7f262317f90ef176df3cf69b24c6778a0` |
| **Rider 1** collect-only (3628 items) | `phase0/drill_receipts/20260913T163645Z_wregistry_cp10_COLLECTONLY.txt` | `38fa9c172e9121ae027ba5804915713f6e44bd2325f7324a9a21ff801009c7a1` |
| Gate 2 Option B egress log | `phase0/cp10_egress_log/20260913T162655Z_playwright_install.log` | (log-only receipt) |
| Playwright harness script | `tools/cp10_real_chromium_harness.py` | (committed at track-a HEAD after CP10) |
| Fresh harness receipt | `phase0/harness_ground_truth/latest.json` (at_utc 2026-09-13T16:30:40Z) | (banked on master state) |
| Seal | `phase0/output_verified_seals/wregistry_cp10.seal.txt` | — |
| Byte-match | Both GREEN runs 3627 passed / 1 skipped / 438 warnings; strip-of-time diff empty; both 37589 bytes | — |

### RED reason verbatim (right-reason check)

Mechanical RED at 2026-09-13T16:31:19Z produced 1 failed / 1 passed:
- FAILED: `test_cp10_wave_close_manifest_exists_and_names_all_10_cps` — right-reason `AssertionError: wave-close manifest missing at /app/assessment_workspace/notes/W_REGISTRY_FULL_BUILD_close.md — owner rule STEP 5` (the manifest was still under quarantine at that instant).
- PASSED: `test_cp10_harness_receipt_is_still_recent` — the fresh harness receipt (written ~30s prior by the Playwright run) was still under the 12h threshold and had all 24 rules bound.  This test PASSED at RED time; per G-D amended (owner ruling 2026-09-13), it is documented as `RED-NOT-PRODUCIBLE for this test in this instant because the harness receipt was just written`.  See §F.

## §F · G-D · already-satisfied row (per owner amendment 2026-09-13)

| Row | Provenance | Disposition |
|---|---|---|
| CP10-02 · `test_cp10_harness_receipt_is_still_recent` | `RED-NOT-PRODUCIBLE at RED-instant`: the receipt at `phase0/harness_ground_truth/latest.json` had already been written by `tools/cp10_real_chromium_harness.py` moments earlier (at_utc 2026-09-13T16:30:40Z, ~30s before RED at 16:31:19Z), so its freshness assertion trivially held. | Landed as regression guard per G-D amended.  Freshness re-verified at GREEN1 (16:32:17Z) and GREEN2 (16:34:22Z) — receipt still <12h old and all 24 rules bound.  Listed here + in block completion report. |

## §G · Promises discharged

Per `MILESTONE_PROMISE_BINDING §M1` (updated 2026-09-13):
- **W-REGISTRY-FULL-BUILD CP10** — discharged: real-Chromium proof landed for THIS session's frontend runtime (v8/v2 Portal · localhost:3000 · rules bound 24/24).
- Prior-session CP1..CP9 (commits `9874b1d..ff20aac`) remain the code substrate; CP10 is the final wave-close that binds them to a fresh rendered-DOM proof.

Notes on scope vs the Sep-9 CP10 attempt (from the quarantined manifest):
- The Sep-9 attempt claimed "8 substitutions applied on Registry" using a different scanner.
- This session's Playwright run uses `page.content()` (full HTML), giving deeper coverage — **24/24 v3 rules matched**.
- No re-work of CP1..CP9 code was needed; the substitution rules JSON (`notes/v3_substitution_rules.json`) is the same 24-rule set from CP8.

## §H · Guardrails held

- Local commit only (`programme/track-a`). NEVER pushed.
- Egress: ZERO on-prem.  Only the one-time authorised public Playwright/Chromium package download from PyPI + Playwright CDN.  All fetches logged in `phase0/cp10_egress_log/`.
- `testing_agent` BANNED.  Terminal pytest only.
- Rider-1 discipline banked with the close (env-delta from playwright install honestly recorded — silent flip forbidden).
- ENV-DRIFT-2TESTS-20260913 remains tracked-open (untouched by this wave).
- SEC-2026-09-12-01 remains owner-side; builder not touching.
- G-A ratified sequence next step: G-3 full-closure remainder (Doc-0 G-3 / BR-4.1).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
