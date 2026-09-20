# STOP-CONDITION · R-88+ First Slice · Harness Subject Retired

- **Recorded UTC**: 2026-09-20T21:48:36Z
- **Wave**: R-88+ · CP-CONTENT-REGISTRY-WAVE first slice (CON-1..CON-11)
- **Trigger**: BASELINE_GUARD=1 sweep 1 cure attempt — test_cp10_harness_receipt_is_still_recent
- **Finding kind**: Silent-rebaseline risk (owner rule "no silent rebaseline")

## What I did (per owner steer this session)

1. Cured test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline
   by fixing my own un-banked working-tree malformed ratchet_history append
   IN PLACE (schema keys utc / wave / to_floor / reason → canonical
   at_utc / commit / cp / passed / note). Result: **GREEN**. Ratchet count
   MEASURED at 5662 (5651 + 11 CON-1..11 invariants). No rebaseline of
   the count itself.

2. To cure test_cp10_harness_receipt_is_still_recent, I applied the
   existing-precedent ceremony: re-ran
   tools/wave_g5_realchrome_verification_harness.py --label r88_first_slice_harness_refresh_20260920T214213Z.
   Per-run receipt at
   phase0/harness_ground_truth/run_r88_first_slice_harness_refresh_20260920T214213Z_1789940636.json.
   Test **now passes** (freshness 0h old · zero unbound rules) — BUT it passes VACUOUSLY.

## Silent-rebaseline evidence (why I stop)

| Receipt at_utc         | Label                                                | dummies_declared | marked_slots_count | body_len |
|------------------------|------------------------------------------------------|------------------|---------------------|----------|
| 2026-09-16T03:55:59Z   | run                                                  | 37               | 29                  | 608177   |
| 2026-09-16T16:26:53Z   | run                                                  | 37               | 29                  | 608177   |
| 2026-09-17T04:30:41Z   | run                                                  | 37               | 29                  | 608177   |
| 2026-09-18T01:59:48Z   | run                                                  | 37               | 29                  | 608177   |
| 2026-09-19T02:04:35Z   | run                                                  | 37               | 29                  | 608177   |
| 2026-09-19T14:25:16Z   | m17w3_refresh                                        | 37               | 29                  | 608177   |
| 2026-09-20T09:19:52Z   | staleness_ceremony_20260920_sweep_refresh            | 37               | 29                  | 608177   |
| **2026-09-20T21:43:56Z** | **r88_first_slice_harness_refresh_20260920T214213Z** | **0**            | **0**               | **608128** |

## Root cause (verified with file inspection, not README speculation)

Commit **dc48d53131be2a36b36aabab83048cbbb779cfa2** on branch `main` at
2026-09-20T14:21:07Z ("feat(frontend): DAP Portal full build + OS Prototype
v2 React surfaces") replaced the substantive V8 substitution engine that
previously lived in /app/frontend/src/App.js with a slim iframe-wrapper
shell for the DAP Portal.

Evidence:

- `wc -c /app/frontend/src/App.js` = 2691 bytes (pre-rebuild it was
  substantially larger and contained the substitution engine).
- `grep -rn "V8_SUBSTITUTIONS" /app/frontend/src/ /app/frontend/public/`
  returns **zero matches**.
- Harness DIAG at 21:43:14 confirms `"hasWindowSubstitutions": false`,
  `"hasApplySubstitutions": false`, and `"hostFound": false` — the
  `[data-testid="v8-portal-iframe-host"]` element that the harness and
  the substitution engine both required is absent from the rebuilt App.js.
- The iframe itself still loads `http://localhost:3000/v8_prototype.html`
  (1.26 MB static prototype file preserved), so the DOM body_len is still
  ~608k. But the substitution engine that used to inject "Not yet measured"
  / "awaiting first census" / etc. is retired.

## Why this is a stop-condition (not proceed-as-vacuous-green)

- The test body has TWO clauses: (a) `age_h < 12`, (b) no unbound rules.
  Clause (b) becomes vacuously satisfied when the receipt's `per_rule`
  array is empty — which is the current state.
- The test was authored (owner directive verbatim, banked in the test
  docstring): *"real-Chromium proof, floor 3006 (fix/refresh stale
  harness-receipt invariant first — refresh the harness, don't relax the
  threshold)"*. The SPIRIT is "the substitution engine has been proven to
  bind to rendered DOM". An empty per_rule is not a binding proof — it is
  absence of the subject.
- Accepting this vacuous pass as GREEN and sealing Commit-A would bake
  the {declared=0, marked=0} shape into the R-88+ closure record,
  effectively rebaselining the harness receipt without an explicit owner
  ruling.

## Boundary check — this is not my R-88+ wave's fault

- R-88+ first-slice code-only changes on `programme/track-a` HEAD
  200c2c637 (sealed R-87 Commit-A) are backend-only:
    - services/content_registry/__init__.py (new)
    - services/content_registry/content_registry_vocabulary.py (new)
    - tests/invariants/test_content_registry_v1_section_2_and_3.py (new)
    - tests/invariants/baseline_failures.json (schema-cured additive append + ratchet 5651→5662)
- The frontend rebuild landed on `main` (branch: main, commit dc48d5313,
  2026-09-20T14:21:07Z), 7+ hours BEFORE my R-88+ first-slice implementation
  started at ~2026-09-20T21:20Z.

## Options for owner (per owner's binding rule: I do not choose ordering, phases, or build order)

Options A / B / C / D — I do not recommend one; I present the fact and
await ruling.

- (A) **Retire the test.** The substitution engine is retired; the test's
      subject no longer exists. Additive retirement receipt on `master`
      with citation of dc48d5313. Ratchet re-measured.
- (B) **Restore the substitution engine on the new DAP Portal architecture.**
      Out-of-scope for R-88+; would open a dedicated FE wave (Ruling ? ·
      scheduled slot).
- (C) **Accept vacuous pass.** Explicit owner ruling to permit the empty
      per_rule as steady-state under the retired subject. Ratchet
      re-measured; annotation added on the receipt shape.
- (D) **Something else the owner specifies.**

## No changes made outside my un-banked working tree

- Cure #1 (schema fix on ratchet_history[-1]): PERSISTED in
  tests/invariants/baseline_failures.json (was already my un-banked
  working-tree edit; the fix stays because it also un-breaks the
  monotonic-ratchet test).
- Cure #2 (harness re-run): PERSISTED in
  phase0/harness_ground_truth/latest.json +
  phase0/harness_ground_truth/run_r88_first_slice_harness_refresh_20260920T214213Z_1789940636.json.
  The previous per-run reference receipts (Sep 16 through Sep 20 09:19Z)
  are untouched and still available for byte-comparison.
- No `git add` / `git commit` / `git push` executed. R-88+ first-slice
  Commit-A remains UN-OPENED pending owner ruling on Option A/B/C/D.

## Anchors and files

- Failing tests reproduction receipt: phase0/drill_receipts/20260920T214119Z_r88_pre_cure_two_reds_reproduction.log
- Harness re-run stdout: phase0/drill_receipts/20260920T214213Z_r88_harness_refresh_stdout.log
- Harness re-run structured log: phase0/eyeball_proxies/20260920T214213Z_wave_g5_realchrome_r88_first_slice_harness_refresh_20260920T214213Z.log
- Reference receipt (last full-green): phase0/harness_ground_truth/run_staleness_ceremony_20260920_sweep_refresh_1789895992.json
- Current receipt (vacuous-green): phase0/harness_ground_truth/latest.json
- Culpable commit on `main`: dc48d53131be2a36b36aabab83048cbbb779cfa2 (2026-09-20T14:21:07Z)
- HEAD on `programme/track-a` (unchanged during this session): 200c2c637277f1f12dee342dc68cdf7a7ebed463
