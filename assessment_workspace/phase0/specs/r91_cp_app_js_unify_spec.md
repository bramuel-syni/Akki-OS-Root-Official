# R-91 · CP-APP-JS-UNIFY · FE Specialist Landing Spec

**Wave:** R-91 CP-APP-JS-UNIFY (SCHEDULED · Phase 1 opening banked with this spec)
**Authored:** 2026-09-20T23:58:00Z · main-agent Autopilot (SO §6)
**Authority chain:** R-91 closure card `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` (ratified 2026-09-20T21:55:00Z) · owner Ruling 1 (2026-09-20T~19:00Z) · owner D-ruling on CP10 (2026-09-20T~21:55Z) · owner A-extension covering v8-cascade artifacts (2026-09-20T~22:05Z) · owner Phase 1 approval (2026-09-21T~00:00Z, current session).
**HUNT receipt binding:** `phase0/spec_hunt_receipts/20260920T235800Z_r91_cp_app_js_unify_hunt_receipt.md` (§1-§16 · read as ground truth for every claim in this spec).

---

## 0 · Preamble · what this spec is and is not

**This spec is** the byte-identity landing blueprint the FE specialist implements on `pod_shell/frontend/**` inside `/app/assessment_workspace/repos/Extraction-Akki/`. It pins the mirror direction, the file inventory the specialist must materialise, the two-half exit criteria (mirror-drift half + CP10 non-vacuous half), the retirement plan for 5 baseline entries, and the discipline the specialist inherits from the Standing Order.

**This spec is not** the specialist's tactical choice of *where* to restore the V8 substitution engine (Option A/B/C surfaced in HUNT §10). The owner explicitly authorised the specialist to resolve that architectural question at landing ("R-91 resolves it either way"). This spec presents the option surface and states each option's cost, without picking.

**This spec is not** authorised to be amended after Phase 1 opening lands without an owner ruling, per SO §6.4 NOTHING-BEYOND. If the specialist discovers a scope constraint at implementation time (e.g., a fourth option or a constraint on an existing option), the specialist stops and reports rather than adapts.

**Non-goals of Phase 2:**
- No refactor of any existing test file (additive-only; existing invariants continue verbatim GREEN).
- No editing of any sealed contract/writer under `backend/services/` or `backend/contracts/`.
- No new baseline entry authored during Phase 2 (the 5 wrapped entries retire; no substitute failures may enter the baseline in the same commit).
- No downward ratchet shrink (SO §3 forbids silent rebaselining; the baseline set shrinks under set-equality-preserving retirement, but `passed_floor` and `counts_at_baseline.passed` never go down).
- No push to any remote (`programme/track-a` and `master` have no remotes configured; this stays true).
- No use of `testing_agent` — terminal `pytest` only.

---

## 1 · Unification direction (STRICT · from R-91 closure card MUST NOT)

**Verbatim from the closure card:**
> Edit `/app/frontend/**` during this wave — the unification direction is `/app/frontend/**` (specialist head) → `pod_shell/frontend/**` (repo mirror), NEVER the other way.

**Operationalisation for the FE specialist:**
- `/app/frontend/**` is the AUTHORITATIVE HEAD. Its App.js (sha `282650cbb514ea5cdfacef2d5ca0ac14f040d2809c1107af98fcd0f8799c6374`) and its `pages/**` (9 `.jsx` files per HUNT §5) are the target the pod_shell mirror catches up to.
- `pod_shell/frontend/**` is the MIRROR that must catch up. Specifically:
  - `pod_shell/frontend/src/App.js` (currently sha `ef20409b38425c15e6acea6226ff197742b805bc008a17bc2dbf450361e4ff5a`, 1084 lines · V8-shell-port snapshot) must be replaced byte-identically with `/app/frontend/src/App.js` content — with the specific caveat below for the CP10 half.
  - `pod_shell/frontend/src/pages/**` (currently empty per HUNT §5) must be materialised byte-identical to `/app/frontend/src/pages/**` (9 `.jsx` files).

**Caveat: the CP10 non-vacuous half depends on Option A/B/C (§3 below).** If the specialist selects Option A (restore V8 engine into `/app/frontend/src/App.js` or into `/app/frontend/src/pages/os/OSPrototype.jsx`), that IS an edit of `/app/frontend/**`. The R-91 closure card's MUST NOT clause is about the *mirror direction of the byte-identity copy*, not about whether the target file that gets mirrored can be edited to include a restored engine. The specialist must reconcile this in the landing note and cite the owner D-ruling authorising CP10 "either way" resolution.

**Repo touched by specialist landing:** `/app/assessment_workspace/repos/Extraction-Akki/pod_shell/frontend/**` (primary) + `/app/frontend/**` if Option A/B chosen (secondary, per the caveat above).

**Repo not touched:** any file under `/app/assessment_workspace/repos/Extraction-Akki/backend/**` (tests + services + contracts stay verbatim); any file under `/app/assessment_workspace/repos/Extraction-Akki/frontend/**` (the 154-line retired AkkiV4Shell tree at sha `e381de86…` is unrelated per HUNT §1).

---

## 2 · Mirror-drift half · exact byte-identity contract

### 2.1 App.js byte-identity

**Target:** `sha256(/app/frontend/src/App.js) == sha256(pod_shell/frontend/src/App.js)`.

**Baseline before landing:**
- `/app/frontend/src/App.js` — sha256 `282650cbb514ea5cdfacef2d5ca0ac14f040d2809c1107af98fcd0f8799c6374` · 71 lines · DAP Portal + OS Prototype v2.
- `pod_shell/frontend/src/App.js` — sha256 `ef20409b38425c15e6acea6226ff197742b805bc008a17bc2dbf450361e4ff5a` · 1084 lines · V8-shell-port (pre-`dc48d5313`).

**Action after landing (Option A/B path):** If Option A picks `/app/frontend/src/App.js` as the substitution-engine host, the runtime file's SHA changes (say to `NEW_APP_JS_SHA`); then pod_shell's `src/App.js` must be updated to match `NEW_APP_JS_SHA`. If Option A picks `pages/os/OSPrototype.jsx` as the host, the runtime `src/App.js` sha stays at `282650cb…` and the pod_shell mirror lands at that value. If Option B (public/v8_prototype.html) is picked, App.js is untouched; pod_shell `src/App.js` lands at `282650cb…`.

**Test coverage that flips green:**
- `tests/invariants/test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell` (baseline entry #1).
- `tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js` (baseline entry #4).

### 2.2 pages/** byte-identity

**Target:** For every file `p` under `/app/frontend/src/pages/**`, `sha256(p) == sha256(pod_shell/frontend/src/pages/{relpath(p)})`, AND the file-set of `/app/frontend/src/pages/**` equals the file-set of `pod_shell/frontend/src/pages/**`.

**Files the specialist must materialise under `pod_shell/frontend/src/pages/`** (from HUNT §5 inventory):

| Relpath | Source sha (from `/app/frontend/src/pages/{relpath}`) · to be measured at landing |
|---|---|
| `dap/AvailableResources.jsx` | (specialist measures + reports at landing) |
| `dap/ConnectResources.jsx` | ← |
| `dap/DAPLanding.jsx` | ← |
| `dap/DAPLayout.jsx` | ← |
| `dap/DataEstates.jsx` | ← |
| `dap/DataGovernance.jsx` | ← |
| `dap/ExtractModes.jsx` | ← |
| `dap/RequestLifecycle.jsx` | ← |
| `os/OSPrototype.jsx` | (if Option A restores engine here, sha changes at both sites; specialist reports pre- and post-landing shas) |

**Extra files under `/app/frontend/src/` referenced by pages** (e.g., `src/hooks/useAuth.js` if imported by `pages/dap/DAPLayout.jsx`, `src/lib/apiClient.js` if imported): the specialist must inventory all such transitive-reference files and materialise them byte-identical under `pod_shell/frontend/src/`. HUNT §7 notes that neither tree currently carries `src/apiClient.js`; if `src/lib/apiClient.js` exists at runtime, the mirror invariant for `apiClient.js` remains vacuous (path-check for `src/apiClient.js`), but the specialist should still mirror `src/lib/**` files that runtime pages reference so the app boots at pod_shell.

**Test coverage that flips green:**
- `tests/invariants/test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir` (baseline entry #5).

### 2.3 Additive-only discipline against pod_shell/frontend/src/components/

**Do not delete** any file under `pod_shell/frontend/src/components/` (17 `.jsx` per HUNT §6 · legacy pod donor material retained per Wave G4). The corresponding directory at `/app/frontend/src/components/` also carries 17 `.jsx` byte-identical files (currently GREEN under `test_runtime_frontend_components_match_repo_pod_shell`); mirror direction from runtime to pod_shell must NOT introduce a new file that then has no runtime peer (would REGRESS the components mirror invariant).

If the specialist introduces a NEW component to support the DAP Portal that lives under `/app/frontend/src/components/`, it must be mirrored byte-identical under `pod_shell/frontend/src/components/` in the same commit.

### 2.4 Same-commit annotation retirement (R-86 Property 4 · non-negotiable)

At the moment the 3 mirror-drift entries flip GREEN:
- Their 3 keys under `baseline_failures.json.baseline_failures` are removed.
- Their 3 keys under `baseline_failures.json.known_runtime_drift_annotations` are removed (same commit).
- `counts_at_baseline.passed` bumps by ≥3.
- `passed_floor` bumps by ≥3 (matching the delta · CCS2 lesson: never split).
- New `ratchet_history` entry appended with `at_utc`, `cp`, `delta`, `passed`, `receipts` fields.

Violation: retiring baseline entries without retiring their annotations (or vice versa) fires `test_baseline_drift_annotations_present.py::test_annotation_count_equals_mirror_drift_baseline_entry_count` RED.

---

## 3 · CP10 non-vacuous half · option surface + exit criteria

### 3.1 Owner authority to resolve

Owner D-ruling verbatim (2026-09-20T~21:55Z · re CP10 discrepancy):
> "State the discrepancy in the receipt as found; R-91 resolves it either way."

Owner A-extension verbatim (2026-09-20T~22:05Z · re v8-cascade artifacts):
> "Same root cause (dc48d5313), same closure (R-91), same reasoning that covered artifact 4 covers artifacts 5 and 6."

**Reading:** The specialist has explicit owner authority to select any resolution path that produces a non-vacuous harness receipt at Phase 2 seal, provided the resolution is banked verbatim in the landing note and the option's cost is stated honestly.

### 3.2 Option A · Restore engine into React tree

**Where:** `/app/frontend/src/App.js` (add `V8_SUBSTITUTIONS` array + `window.V8_SUBSTITUTIONS_DUMMIES` exposure + `applySubstitutions()` + MutationObserver + iframe-content mutation) OR `/app/frontend/src/pages/os/OSPrototype.jsx` (same set, scoped to the OS Prototype route's iframe).

**Byte cost:**
- Edits `/app/frontend/src/App.js` (~1000 net-new lines from pod_shell/App.js · L58-L889 substitution engine block, ported verbatim OR reduced to what OSPrototype needs).
- Then mirrored byte-identical into `pod_shell/frontend/src/App.js` (or `pod_shell/frontend/src/pages/os/OSPrototype.jsx`).

**Interaction with R-91 MUST NOT clause:** the MUST NOT explicitly targets the *direction of the byte-identity copy* (specialist head → repo mirror). Restoring the engine into the runtime head file that then flows to the repo mirror is compatible with the MUST NOT (the runtime remains authoritative; the pod_shell copies from it). If the specialist reads the MUST NOT more strictly (no touches to `/app/frontend/**` at all this wave), Option A is unavailable — but the CP10 half's D-ruling authority ("either way") overrides that stricter reading.

**Exit criteria pinned:**
- `window.V8_SUBSTITUTIONS_DUMMIES` is exposed by the runtime React app (verified by opening a browser at the app root and evaluating `window.V8_SUBSTITUTIONS_DUMMIES.length`; the harness at `tools/wave_g5_realchrome_verification_harness.py` reads this global).
- Post-landing harness run regenerates `phase0/harness_ground_truth/latest.json` with `dummies_declared > 0`, `marked_slots_count > 0`, `per_rule` non-empty, every rule `bound_to_rendered_dom == True`, `registry-aside-hero-sentence.matched_by_marker == True`.
- 2 v8-cascade baseline entries retire. 2 keys under `known_r91_closure_scheduled_receipt_drift_annotations` retire in the same commit as the baseline removals.

### 3.3 Option B · Embed engine inside `/app/frontend/public/v8_prototype.html`

**Where:** the static HTML iframe source itself gains a `<script>` block declaring `V8_SUBSTITUTIONS`, exposing `window.V8_SUBSTITUTIONS_DUMMIES` inside the iframe's document context, and driving substitutions inside that same context. Requires an ancillary edit to `tools/wave_g5_realchrome_verification_harness.py` to read the iframe's `contentWindow.V8_SUBSTITUTIONS_DUMMIES` rather than the outer `window`.

**Byte cost:**
- Edits `/app/frontend/public/v8_prototype.html` (adds substitution engine as inlined script).
- Edits `tools/wave_g5_realchrome_verification_harness.py` (retargets to iframe context).
- Mirrors both edits into `pod_shell/frontend/public/v8_prototype.html` and — if the tools/ path is repo-scoped — into repo-side tools/. NOTE: `tools/` lives in `/app/assessment_workspace/tools/`, which is the STATE repo (workspace); its mirroring discipline is separate.

**Exit criteria pinned:** same three test greens as Option A, plus verified harness retargeting produces the expected non-vacuous output.

### 3.4 Option C · Retire the invariant contract

**Where:** owner ruling that the DAP Portal architecture legitimately deprecates the V8 substitution engine (this option is NOT currently backed by any owner ruling — the current annotation umbrella presumes closure-by-restoration).

**Byte cost:**
- New owner ruling banked in `STATE/DECISIONS.md`.
- Retirement of `tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py` entirely (delete file) OR its rebless as vacuous under a documented rationale.
- Retirement of `test_r88_cp10_harness_scheduled_closure_drift_annotation.py::test_harness_receipt_is_non_vacuous_when_card_status_is_sealed` OR its rebless with the DAP-Portal-final rationale.
- Retirement of `known_r91_closure_scheduled_receipt_drift_annotations` field OR its rebless.

**Interaction with SO §3:** Option C is closure-by-test-retirement, which historically fires SO §3's silent-rebaselining alarms. It requires explicit owner ruling and receipt banking. This option is presented for completeness; do not proceed without owner directive.

### 3.5 Recommendation to the specialist (non-binding · advisory)

Option A is the shortest path to Phase 2 seal and requires no invariant retirement or harness retargeting. Option A is compatible with the owner D-ruling and the R-91 closure card MUST NOT under the direction-of-copy reading. The specialist should default to Option A absent a specific tactical reason to prefer B or C. If a specific reason emerges, the specialist stops and reports rather than adapts.

---

## 4 · Phase 2 acceptance protocol · terminal `pytest` only

### 4.1 Post-landing verification subset

After the specialist lands the byte-identity + engine-restoration edits, run this verification subset from `/app/assessment_workspace/repos/Extraction-Akki/backend/` via terminal `pytest`:

```
pytest tests/invariants/test_ship_manifest_dod.py -v
pytest tests/invariants/test_wave_g_pod_shell_frontend_mirror.py -v
pytest tests/invariants/test_v8_substitution_rules_bind_to_rendered_dom.py -v
pytest tests/invariants/test_baseline_drift_annotations_present.py -v
pytest tests/invariants/test_r88_cp10_harness_scheduled_closure_drift_annotation.py -v
pytest tests/invariants/test_w_registry_full_build_cp10_wave_close.py -v
```

Expected: all six modules GREEN. The 5 wrapped baseline entries flip from RED (via `baseline_failures.json` wrapping) to GREEN (via actual pass).

### 4.2 Full BASELINE_GUARD=1 double-sweep byte-identical gate

After the verification subset is GREEN, run the full sweep twice with `BASELINE_GUARD=1` and confirm stripped-sha256 equality (per SO §3.3 + M16-W3 corrected order):

```
BASELINE_GUARD=1 pytest > /app/assessment_workspace/phase0/drill_receipts/<utc>_r91_close_run1.log
BASELINE_GUARD=1 pytest > /app/assessment_workspace/phase0/drill_receipts/<utc>_r91_close_run2.log
python3 tools/strip_baseline_guard_log.py <run1.log> > run1.stripped
python3 tools/strip_baseline_guard_log.py <run2.log> > run2.stripped
sha256sum run1.stripped run2.stripped   # both must match
```

Expected: `run1.stripped` and `run2.stripped` sha256 identical. `passed` count ≥ 5695 + 5 = 5700 (baseline retirement floor) plus any additional new tests the specialist authors. `failed` count 0 (baseline set shrunk to empty). `skipped` count 1 (unchanged from the legacy conditional skip).

### 4.3 Ratchet update (CCS2-aligned)

Post-landing edit to `backend/tests/invariants/baseline_failures.json`:
- `baseline_failures` array: remove 5 entries → empty array `[]`.
- `known_runtime_drift_annotations`: remove 3 keys → empty object `{}`.
- `known_r91_closure_scheduled_receipt_drift_annotations`: remove 3 keys (the 2 baseline entries plus the non-baseline "still-recent" guard entry) → empty object `{}` OR retain the "still-recent" guard entry only, per specialist's Option A/B choice.
- `counts_at_baseline.passed`: `5695` → `5695 + Δ` where `Δ ≥ 5`.
- `counts_at_baseline.failed`: `5` → `0`.
- `invariants_enforced_when_baseline_guard_1.passed_floor`: `5695` → same as `counts_at_baseline.passed` post-landing.
- Append to `ratchet_history` (M16-W3 corrected order · same commit as the code lands):
  ```json
  {
    "at_utc": "<utc>",
    "cp": "R-91 CP-APP-JS-UNIFY Phase 2 · mirror-drift half + CP10 non-vacuous half retirement",
    "delta": <int ≥ 5>,
    "passed": <int ≥ 5700>,
    "receipts": [ "phase0/drill_receipts/<utc>_r91_close_run1.log", "phase0/drill_receipts/<utc>_r91_close_run2.log" ]
  }
  ```
- Regenerate `notes/ORCH_BOOT.md` ratchet-only pre-Commit-A per M16-W3 corrected order.
- Sync byte-identically to `/app/frontend/public/audit/ORCH_BOOT.md` (POD audit mirror).

### 4.4 Regenerate harness ground-truth receipt

Run `tools/wave_g5_realchrome_verification_harness.py` post-landing to regenerate `/app/assessment_workspace/phase0/harness_ground_truth/latest.json`. Assert receipt is non-vacuous (`dummies_declared > 0`, `marked_slots_count > 0`, `per_rule` non-empty, `orphan_count == 0`).

### 4.5 3-Commit Seal (Phase 2 close)

Follow the R-92 3-Commit Seal precedent verbatim (per `STATE/DECISIONS.md 2026-09-20T23:33:00Z` R-92 seal report):

- **Commit-A** on `programme/track-a` in `/app/assessment_workspace/repos/Extraction-Akki`: pod_shell mirror byte-identity + baseline retirement + engine restoration (Option A/B).
- **Commit-B** on `master` in `/app/assessment_workspace`: state banking (STATE/DECISIONS.md R-91 seal report + STATE/NEXT.md R-91 SEALED marker + STATE/PINS.md R-91-PHASE-2-PINS block + pre-Commit-A ORCH_BOOT ratchet regen + tools/r91_pre_commit_a_orch_boot_regen.py NEW + drill_receipts × 4 + harness_ground_truth/latest.json regen).
- **Commit-C** fixup on `master`: R-6 boundary regen advancing `heads_last_sealed.state_repo.head` to Commit-B SHA + new code_repo history entry for Commit-A SHA + STATE/NEXT.md R-91 SEALED marker flip + POD audit mirror byte-identical sync.

### 4.6 Standing bounds carried into Phase 2

Verbatim from the R-92 seal report (unchanged):
- Zero push · zero remote configured on `programme/track-a`.
- Terminal `pytest` only · no `testing_agent`.
- Additive-only per SO §3.8 · three-repo discipline · ratchet monotonic-up.
- R-88+ OWNER-RATIFICATION-PENDING block carries forward unchanged.
- HF-HOLD SEC-2026-09-12-01 remains OPEN · R-24 remains UNLISTED · R-25 defaults tagged.

---

## 5 · Retirement plan · 5 baseline entries flip GREEN at Phase 2 seal

| # | Test nodeid | Field | Retires when | Post-landing outcome |
|---|---|---|---|---|
| 1 | `test_ship_manifest_dod::test_runtime_frontend_app_matches_repo_pod_shell` | `known_runtime_drift_annotations` | `sha256(/app/frontend/src/App.js) == sha256(pod_shell/frontend/src/App.js)` | GREEN |
| 2 | `test_wave_g_pod_shell_frontend_mirror::test_app_frontend_App_js_mirrors_pod_shell_App_js` | `known_runtime_drift_annotations` | same as #1 | GREEN |
| 3 | `test_wave_g_pod_shell_frontend_mirror::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir` | `known_runtime_drift_annotations` | all 9 files under pod_shell/frontend/src/pages/ byte-identical peers of runtime | GREEN |
| 4 | `test_v8_substitution_rules_bind_to_rendered_dom::test_every_v8_substitution_rule_binds_to_harness_rendered_dom` | `known_r91_closure_scheduled_receipt_drift_annotations` | harness ground-truth per_rule non-empty AND every rule bound | GREEN |
| 5 | `test_v8_substitution_rules_bind_to_rendered_dom::test_slot1_registry_aside_marker_present` | `known_r91_closure_scheduled_receipt_drift_annotations` | ground-truth `registry-aside-hero-sentence.matched_by_marker == True` | GREEN |

Baseline set: `5 → 0`. Two annotation fields become empty `{}` (or retain only the "still-recent" guard for the third field under Option A depending on architectural choice).

---

## 6 · Discipline invariants that MUST continue GREEN through Phase 1 AND Phase 2

R-86 (5 tests · `test_baseline_drift_annotations_present.py`):
- test_every_mirror_drift_baseline_entry_has_an_annotation
- test_every_annotation_has_the_required_8_field_shape
- test_annotation_closure_card_paths_resolve_to_real_files
- test_annotation_count_equals_mirror_drift_baseline_entry_count *(this is the SET-EQUALITY GUARD that forces same-commit retirement of annotations + baseline entries)*
- test_every_annotation_names_cp_app_js_unify_as_closure_wave

R-88+ (6 tests · `test_r88_cp10_harness_scheduled_closure_drift_annotation.py`):
- test_cp10_harness_scheduled_closure_annotation_present
- test_cp10_annotation_has_required_8_field_shape
- test_cp10_annotation_closure_wave_is_cp_app_js_unify_r91
- test_cp10_annotation_closure_card_path_resolves_to_real_file
- test_cp10_annotation_closure_card_line_present_in_closure_card
- test_harness_receipt_is_non_vacuous_when_card_status_is_sealed *(this GUARD fires RED the moment the R-91 milestone flips to SEALED if the harness is still vacuous · Option A/B must produce non-vacuous BEFORE the milestone flips)*

---

## 7 · Files inventoried this-Phase (Phase 1 outputs)

Under `/app/assessment_workspace/`:
- `phase0/spec_hunt_receipts/20260920T235800Z_r91_cp_app_js_unify_hunt_receipt.md` — HUNT receipt (binding for every claim in this spec).
- `phase0/specs/r91_cp_app_js_unify_spec.md` — this file.
- `notes/FE_DISPATCH_READY_R91.md` — dispatch-ready flag pointer note.
- `STATE/DECISIONS.md` — R-91 Phase 1 opening banking appended.
- `STATE/NEXT.md` — R-91 Phase 1 IN-FLIGHT marker appended.
- `STATE/PINS.md` — R-91-PHASE-1-PINS block appended.

Files NOT touched (Phase 1 discipline):
- `programme/track-a` HEAD stays at `ceaa24f41c8156c31e408b47fa8a59b3b265e6ac` (R-92 Commit-A).
- `/app/frontend/**` — untouched by Phase 1 (Phase 2 may edit per Option A/B per §3).
- `notes/ORCH_BOOT.md` — untouched (ratchet stays `5695 pass / 5 fail / 1 skip · floor 5695`).
- The R-91 closure card `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` — contract unchanged (Phase 1 confirms; does not amend).
- Any file under `backend/**` (tests + services + contracts stay verbatim).

---

## 8 · Handoff protocol

1. **Owner dispatches this spec verbatim to the FE specialist.** The `FE-DISPATCH-READY` flag at `notes/FE_DISPATCH_READY_R91.md` announces the spec is complete and Phase 1 is landed on `master`.
2. **The FE specialist:**
   - Reads `STATE/STANDING_ORDERS.md` first (permanent law).
   - Reads this spec + the HUNT receipt + the R-91 closure card.
   - Selects Option A/B/C (recommendation: A) and lands the byte-identity + engine-restoration on `pod_shell/frontend/**` (and `/app/frontend/**` if Option A/B).
   - Regenerates the harness ground-truth receipt.
   - Updates `baseline_failures.json` per §4.3.
   - Regenerates `notes/ORCH_BOOT.md` (ratchet-only pre-Commit-A per M16-W3).
   - Executes the 3-Commit Seal per §4.5.
   - Reports back to the owner with the seal report and drill receipts.
3. **Owner verifies:** double-sweep byte-identical stripped-sha256 match + all 5 baseline entries retired + harness receipt non-vacuous + R-86/R-88+ property tests all GREEN.
4. **Phase 2 seal fires.** R-91 marker flips SCHEDULED → SEALED in `STATE/NEXT.md` + R-91 milestone_status flips to SEALED in the closure card. R-88+ guard `test_harness_receipt_is_non_vacuous_when_card_status_is_sealed` verifies non-vacuous at the moment of the flip.

---

## 9 · Failure modes the specialist should watch for

- **Half-mirror:** Retiring 3 mirror-drift entries WITHOUT restoring CP10 non-vacuous. Fires the R-88+ guard RED at the moment the R-91 milestone flips SEALED. Do not attempt a partial seal.
- **Same-commit annotation-vs-baseline set mismatch:** Retiring baseline entries without retiring their annotations (or vice versa) fires R-86 Property 4 RED. Both must retire together.
- **Silent rebaselining:** Bumping `passed_floor` up without a matching `counts_at_baseline.passed` bump (or vice versa) fires the M16-W3 / CCS2 guard. Both counters move together.
- **Downward shrink:** Any decrease in `passed_floor` fires SO §3 stop-condition.
- **Non-additive edit:** Modifying a sealed contract/writer/test file fires SO §3.8 stop-condition.
- **Component tree mirror regression:** Introducing a component under one tree without mirroring to the other fires `test_runtime_frontend_components_match_repo_pod_shell` RED. Any new component must land in BOTH trees byte-identical in the same commit.
- **Harness receipt still vacuous post-landing:** Option A/B not restoring `window.V8_SUBSTITUTIONS_DUMMIES` at a location the harness reads → harness regenerates as still-vacuous → v8-cascade tests stay RED → R-91 cannot seal. Verify harness reads the correct global BEFORE the seal.

---

## 10 · Anchors + citations

- Owner Ruling 1 (2026-09-20T~19:00Z) — banked at `STATE/DECISIONS.md` OWNER RULINGS anchor.
- Owner D-ruling on CP10 (2026-09-20T~21:55Z) — banked in R-88+ Commit-B pending.
- Owner A-extension covering v8-cascade artifacts (2026-09-20T~22:05Z) — banked in R-88+ Commit-B pending.
- Owner Phase 1 approval (2026-09-21T~00:00Z, current session) — will be banked at Phase 1 Commit-A on `master` (this-turn).
- R-91 closure card `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` (ratified 2026-09-20T21:55:00Z · sha256 `667f744606020f205aac2d292e61fb5945ac0443430c5c7522473675fb929b61`).
- R-86 seal `2eca0e58d1d9773d1b781abe570c3e015e0c98f2` (schedules R-91 slot + establishes the annotation pattern).
- R-88+ seal `db90089d/79d5d38d/0cbfc23b` (extends annotation umbrella to CP10 fourth artifact + owner A-extension for artifacts 5, 6).
- R-92 seal `ceaa24f/19030610/e8f9f168` (immediately-precedes · this-Phase-1 opens directly against R-92 Commit-C head).
- HUNT receipt `phase0/spec_hunt_receipts/20260920T235800Z_r91_cp_app_js_unify_hunt_receipt.md`.
- Standing Order §2.5 verbatim-docstring · §3 tests-first · §3.3 3-Commit Seal · §3.8 additive-only · §6.2 objective-card discipline · §6.4 NOTHING-BEYOND · §6.7 seal-report-boundary.
- M16-W3 corrected order (ORCH_BOOT ratchet regen pre-Commit-A) · CCS2 lesson (both counters bump together).

**END OF SPEC.**
