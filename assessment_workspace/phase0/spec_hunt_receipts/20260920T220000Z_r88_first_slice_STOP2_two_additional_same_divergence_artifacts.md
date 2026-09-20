# STOP-CONDITION #2 · R-88+ First Slice · Two Additional Same-Divergence Artifacts Discovered Post-Cure

- **Recorded UTC**: 2026-09-20T22:00:00Z
- **Wave**: R-88+ · CP-CONTENT-REGISTRY-WAVE first slice
- **Trigger**: BASELINE_GUARD=1 sweep 1 after applying owner D-ruling
- **Finding kind**: Cascade discovery — cure #2 (necessary for CP10 staleness) unmasked 2 additional previously-passing tests that also depend on non-empty `per_rule`

## Context

Owner D-ruling this session (2026-09-20T~21:55Z verbatim) ratified applying
Ruling 1's annotation pattern to a **fourth** artifact of the same divergence:

- Artifacts 1-3: pod_shell mirror-drift baseline entries (R-86 annotations)
- Artifact 4: `test_cp10_harness_receipt_is_still_recent` vacuous-pass (R-88+ D-ruling annotation)

Owner ruling framed this as "a fourth artifact"; his ruling was applied and
BASELINE_GUARD=1 sweep 1 was executed to measure.

## What sweep 1 revealed

**Sweep 1 result**: 5666 passed / 5 failed / 1 skipped (after ORCH_BOOT regen in-scope fix).

Baseline expected 3 failures. Actual 5. The 2 unexpected NEW failures are
BOTH derivative of the same `dc48d5313` V8 substitution-engine retirement:

| Test node id | Why now failing |
|--------------|------------------|
| `tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom` | Reads `phase0/harness_ground_truth/latest.json`, asserts `per_rule` non-empty. Was passing when receipt was 09:19Z (37 rules). Now empty. |
| `tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present` | Same file; asserts `registry-aside-hero-sentence` rule present in `per_rule`. Was passing when receipt was 09:19Z. Now missing. |

## Root cause is IDENTICAL to CP10 artifact

Both tests are direct victims of the same fact pattern the owner already ruled:
- Commit `dc48d53131be2a36b36aabab83048cbbb779cfa2` on `main` at 2026-09-20T14:21:07Z
  removed `V8_SUBSTITUTIONS_DUMMIES` from the React tree.
- Any harness re-run against the rebuilt frontend produces an empty `per_rule`.
- Any test that reads `per_rule` content (rather than only its shape) flips
  from GREEN to RED at that receipt.

**The 2 v8 tests were passing at R-87 pre-Commit-A sweep** (drill_receipts
`20260920T203618Z_run1` and `20260920T204257Z_run2` · both counted 5651 pass /
3 fail). At that moment the 09:19Z receipt was still ~11h 20m old — under
12h — so it was authoritative and had 37 rules. The 12h threshold was
crossed at ~21:19Z. Refresh became mandatory. Refresh exposed the retirement.

## Boundary check

- These 2 tests were NOT in prior `baseline_failures[]` (verified in-session:
  `python3 -c "import json; ...` returns `NOT in baseline` for both).
- They are NOT modifications my R-88+ wave introduced (my wave is
  backend-only + additive-only per SO §3.8).
- They surfaced as an unavoidable consequence of curing `test_cp10_harness_
  receipt_is_still_recent` per your D-ruling.

## Why I stop instead of extending the annotation umbrella myself

Your D-ruling text described the CP10 test as **"a fourth artifact"** —
counting precisely: 3 pod_shell mirror-drift + 1 CP10 = 4. You did not
know at ruling-time that curing CP10 would surface 5th and 6th artifacts
of the identical divergence. Adding these to `baseline_failures[]` +
annotation umbrella is a **material extension** of your ruling — a step
the discipline requires you ratify, not extrapolate.

## The math (nothing has been committed to the ratchet)

- Prior floor at R-87 seal: 5651 pass / 3 fail / 1 skip = 5655 total.
- R-88+ additions this session: +11 CON-1..11 + 6 R-88+ annotation-guard = +17 (all pass).
- After curing V8 engine retirement side-effect: 2 previously-passing tests flip to fail.
- Sweep 1 measurement: **5666 pass / 5 fail / 1 skip = 5672 total** (5666 = 5651 + 17 − 2).
- If we accept the 2 v8 tests into baseline_failures[]:
    - counts_at_baseline.failed: 3 → 5
    - counts_at_baseline.passed: 5668 → 5666 (measured)
    - passed_floor: 5668 → 5666 (measured)
    - ratchet_history[-1].passed: 5668 → 5666 (measured)
    - baseline_failures[] length: 3 → 5 (must also update the manifest count to match)
- If we roll back the receipt to 09:19Z: CP10 test relapses to stale (12h+ old).
- If we do neither: sweep cannot pass, R-88+ Commit-A cannot open.

## Options for owner ruling (I do not choose)

- **(A) Extend the annotation umbrella**. Add both v8 test nodeids to
  `baseline_failures[]` AND to `known_r91_closure_scheduled_receipt_drift_annotations`
  with the same 8-field shape citing `dc48d5313` and R-91 closure.
  Update `counts_at_baseline.failed` 3→5, ratchet to measured 5666.
  The R-91 verification exit-criterion line already reads
  "non-vacuous receipt (dummies_declared > 0, marked_slots > 0, per_rule
  non-empty)" — which byte-for-byte covers what both these tests need to
  flip back to GREEN. No additional card edit required.
- **(B) Different annotation strategy** (owner specifies).
- **(C) Roll back the receipt** (breaks CP10 staleness — I flag this as
  a losing move but present it for completeness).
- **(D) Something else the owner specifies.**

## Historical note (per owner directive · flag as-found)

The specialist's original build report for `dc48d5313` claimed the
substitution engine was "migrated into pages/os/OSPrototype.jsx". In-session
verification:
- `grep -rn "V8_SUBSTITUTIONS" /app/frontend/src/ /app/frontend/public/`
  returns **zero matches**.
- `grep -rn "V8_SUBSTITUTIONS" /app/frontend/public/v8_prototype.html`
  (checked implicitly by the harness observing dummies still visible in
  the iframe DOM) — the dummies remain because the static prototype
  preserves its baseline copy, but no substitution engine is wired to
  overwrite them.

Conclusion (subject to R-91 wave-close verification): either the migration
was into the iframe'd static HTML (not the React tree the harness reads)
or the migration was never landed. R-91 resolves it either way.

## State (nothing committed)

- `programme/track-a` HEAD unchanged: `200c2c637`.
- Un-banked working-tree changes on `programme/track-a`:
    - `backend/tests/invariants/baseline_failures.json` (ratchet + new annotation)
    - `backend/tests/invariants/test_r88_cp10_harness_scheduled_closure_drift_annotation.py` (new · 6 property tests)
- `master` HEAD unchanged: `61d2f15c`.
- Un-banked working-tree changes on `master`:
    - `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` (extended: MUST DO #6 + new EXIT block + new ANCHORs + recomputed card_sha256=`667f744606020f205aac2d292e61fb5945ac0443430c5c7522473675fb929b61`)
    - `notes/ORCH_BOOT.md` + `/app/frontend/public/audit/ORCH_BOOT.md` (ratchet-only regen `bf04d20d...` — both byte-identical)
    - `phase0/harness_ground_truth/latest.json` (fresh 21:43Z receipt with declared=0/marked=0)
- Sweep 1 receipt: `phase0/drill_receipts/20260920T215753Z_r88_first_slice_BASELINE_GUARD1_sweep1.log`
- Red-first receipt for R-88+ annotation guard: `phase0/drill_receipts/*_r88_first_slice_annotation_guard_RED_pre.log`
- Green post-cure receipt: `phase0/drill_receipts/*_r88_first_slice_annotation_GREEN_post.log`
- Prior stop-condition receipt: `phase0/spec_hunt_receipts/20260920T214836Z_r88_first_slice_STOP_harness_subject_retired.md`

Please rule on A/B/C/D and I resume.
