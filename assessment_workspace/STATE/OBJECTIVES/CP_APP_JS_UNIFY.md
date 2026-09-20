---
card_id: CP_APP_JS_UNIFY
title: Scheduled Wave · App.js + Frontend Byte-Identity Unification · slot R-91
ratified_at_utc: 2026-09-20T20:05:00Z
ratified_by: R-86 Commit-A · owner Ruling 1 (2026-09-20T~19:00Z) + follow-up ratification of R-91 slot (2026-09-20T~19:54Z)
card_sha256: 800d836d08e0cff31a3a06458142331cb19dd8698ebbf26855923c2a891b1d3c
milestone_status: SCHEDULED (not-open-ended) · slot R-91 · closure trigger for the three pod_shell mirror-drift baseline entries
---

# CP-APP-JS-UNIFY · Scheduled Wave · Slot R-91 · Closure Trigger for pod_shell Mirror-Drift Baseline Entries

## OBJECTIVE

Unify `/app/frontend/**` with `pod_shell/frontend/**` to byte-identity across App.js + design/ + pages/ + hooks/ + apiClient.js + public/index.html (extended-scope per Wave G Step 1), so the three pod_shell mirror-drift baseline entries retire atomically at wave landing and the FE specialist and repo mirror rejoin one head.

## MUST DO

1. **Byte-identity of `/app/frontend/src/App.js` with `pod_shell/frontend/src/App.js`** — the App.js file is the single authoritative surface after specialist FE conformance passes; unification replays specialist commits `d0a2ea9b` + `9b6b170b` + `14173772` + `3fbfb75c` + `f090e8305` + `d0e36a51e` into `pod_shell/frontend/` so the two trees byte-match. `canon_ref: Wave G Step 1 pod_shell mirror discipline (test_wave_g_pod_shell_frontend_mirror.py) + Ruling 1 verbatim ("Coexistence with a closure date is discipline; without one it's drift with a ruling attached").`
2. **Byte-identity of `/app/frontend/src/pages/**/*.jsx` peers** — every `.jsx` file under `/app/frontend/src/pages/` has a byte-identical counterpart at `pod_shell/frontend/src/pages/`. Includes the specialist-authored `pages/dap/RequestLifecycle.jsx` and any other net-new pages. `canon_ref: Wave G Step 1 extended-scope mirror + specialist commit chain.`
3. **Full runtime-frontend mirror at extended-scope** — `test_runtime_frontend_app_matches_repo_pod_shell` GREEN across App.js + design/ + pages/ + hooks/ + apiClient.js + public/index.html (extended-scope per Wave G Step 1). `canon_ref: test_ship_manifest_dod.py DoD (a)+(b)+(c) + SO §3.3 3-Commit Seal.`
4. **Baseline retirement of the three mirror-drift entries** — the three entries below are removed from `baseline_failures.json.baseline_failures` in the same commit their annotations retire from `known_runtime_drift_annotations`. `canon_ref: R-86 invariant test_annotation_count_equals_mirror_drift_baseline_entry_count (fires immediately if the sets diverge).`
5. **Ratchet monotonic-up under BASELINE_GUARD=1 double-sweep** — new passed_floor equals the old floor plus the count of tests that flip green (the three mirror-drift tests) plus any new tests authored in-wave, minus none (never a shrink). `canon_ref: SO §3 no-silent-rebaselining + M16-W3 corrected order + CCS2 lesson.`

## MUST NOT

- Retire annotations from `known_runtime_drift_annotations` without also retiring the corresponding baseline entries in the same commit (R-86 invariant enforces set equality). `canon_ref: R-86 test_annotation_count_equals_mirror_drift_baseline_entry_count.`
- Edit `/app/frontend/**` during this wave — the unification direction is `/app/frontend/**` (specialist head) → `pod_shell/frontend/**` (repo mirror), NEVER the other way. `canon_ref: Ruling 1 mirror-half closure design + specialist dispatch chain authority.`
- Silently rebaseline (bumping floor downward or leaving floor while removing failing entries). `canon_ref: SO §3.`
- Ship non-additive edits to sealed contracts/writers/tests. `canon_ref: SO §3.8 additive-only.`
- Open the wave before slot R-91 (the definite slot the sprint queue records). `canon_ref: Ruling 1(b) verbatim + CP-REGISTRY-V5-RATIFICATION-AND-COUNT-ERRATUM banking at 1250c39a.`

## EXIT

**R-86 authored invariants (GREEN at R-86 Commit-A · continue verbatim GREEN through this wave landing):**
- tests/invariants/test_baseline_drift_annotations_present.py::test_every_mirror_drift_baseline_entry_has_an_annotation
- tests/invariants/test_baseline_drift_annotations_present.py::test_every_annotation_has_the_required_8_field_shape
- tests/invariants/test_baseline_drift_annotations_present.py::test_annotation_closure_card_paths_resolve_to_real_files
- tests/invariants/test_baseline_drift_annotations_present.py::test_annotation_count_equals_mirror_drift_baseline_entry_count
- tests/invariants/test_baseline_drift_annotations_present.py::test_every_annotation_names_cp_app_js_unify_as_closure_wave

**The three mirror-drift entries that flip green at this wave landing (retire from baseline_failures + retire from annotations in the SAME commit):**
- tests/invariants/test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell
- tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js
- tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir

**BASELINE_GUARD=1 double-sweep byte-identical pre-Commit-A gate (in-slot at R-91).**

## STOP

- Any editing of `/app/frontend/**` during this wave (unification direction is repo mirror ← specialist head; reversing is a fork not a merge).
- Any un-annotated pod_shell mirror-drift entry appearing in `baseline_failures` at wave open (R-86 invariant would flag it; unification cannot proceed under phantom drift).
- Any downward baseline shrink or silent rebaselining (SO §3 stop).
- Specialist FE dispatch still landing new writes to `/app/frontend/**` at wave open (must be quiesced first; double-writing burns work — see the "Why now" rationale in the R-86 seal report).

## ANCHORS

- `tests/invariants/test_baseline_drift_annotations_present.py` (R-86-landed · 5 property tests · enforce the annotation ↔ closure-card chain).
- `tests/invariants/test_ship_manifest_dod.py` (Wave G Step 1 · extended-scope mirror invariant).
- `tests/invariants/test_wave_g_pod_shell_frontend_mirror.py` (Wave G Step 1 · App.js + pages/ byte-identity invariants).
- Specialist commit chain `d0a2ea9b` + `9b6b170b` + `14173772` + `3fbfb75c` + `f090e8305` + `d0e36a51e` (authoritative FE head).
- CP-REGISTRY-V5-RATIFICATION-AND-COUNT-ERRATUM banking at `1250c39a` (bank of R-91 slot).
- Owner Ruling 1 verbatim (2026-09-20T~19:00Z · banked at STATE/DECISIONS.md OWNER RULINGS anchor).
- SO §3.3 3-Commit Seal · SO §3.8 additive-only · SO §6.2 objective-card discipline · SO §6.4 NOTHING-BEYOND · SO §6.7 seal-report-boundary.
