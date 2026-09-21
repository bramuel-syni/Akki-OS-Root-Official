# R-91 CP-APP-JS-UNIFY · HUNT Receipt · Phase 1

**Generated:** 2026-09-20T23:58:00Z
**Wave:** R-91 CP-APP-JS-UNIFY (SCHEDULED · Phase 1 opening this-turn)
**Author:** main-agent Autopilot (SO §6 · in-session file inspection only · no README/prior-knowledge quoting)
**Purpose:** Ground-truth measurement receipt captured before authoring the unify spec. All facts below come from files opened in this session; no interpretation of "which architecture is best" — that is deferred to the FE specialist landing per owner D-ruling (2026-09-20T~21:55Z: "R-91 resolves it either way").
**Precedent:** `phase0/spec_hunt_receipts/20260920T232424Z_g5v5_sfp_1_7_hunt_receipt.md` (R-92 · SRR-authority-binding pattern).

---

## 0 · Owner directives that scope this HUNT

Owner Ruling 1 verbatim (2026-09-20T~19:00Z · banked at STATE/DECISIONS.md OWNER RULINGS anchor):
> "Coexistence with a closure date is discipline; without one it's drift with a ruling attached."

Owner D-ruling verbatim (2026-09-20T~21:55Z · re CP10 harness vacuousness · banked in R-88+ Commit-B pending):
> "THE SUBJECT IS NOT RETIRED — IT IS DISPLACED BY AN ALREADY-RULED DIVERGENCE WITH A SCHEDULED CLOSURE. Your root cause (`dc48d5313` App.js rebuild removing the V8 substitution engine/iframe host) is the SAME fact pattern the owner ruled at Ruling 1: coexistence, documented, with closure trigger CP-APP-JS-UNIFY at slot R-91. [...] the specialist's original build report claimed the substitution engine was 'migrated into pages/os/OSPrototype.jsx' — your grep shows zero V8_SUBSTITUTIONS matches in /app/frontend/src, so either the migration was into the iframe'd static HTML (not the React tree the harness reads) or the claim was inaccurate. State the discrepancy in the receipt as found; R-91 resolves it either way."

Owner ruling this-session verbatim (2026-09-21T~00:00Z · re Phase 1 opening):
> "Plan APPROVED with both defaults confirmed and one label correction. Q1: (a) — state-only Phase 1 seal; `programme/track-a` code branch untouched until the FE specialist lands. [...] Q2: Confirmed — all 5 wrapped baseline failures stay wrapped through Phase 1 and retire ONLY in Phase 2 after the FE landing, byte-identity verify, and non-vacuous CP10 receipt regeneration. [...] LABEL CORRECTION: `pod_shell/frontend/src/App.js` (sha `ef20409b…`) is the V8-shell-port; `/app/frontend/src/App.js` (sha `282650cb…` at dc48d5313, since evolved through `b33d19a8d`) is the DAP Portal + OS Prototype. [...] Proceed with the HUNT → spec → state-only Commit → FE-DISPATCH-READY flag."

Owner correction verbatim (same session · re label direction inherited by earlier plan):
> The earlier plan naming "frontend/src/App.js (V8 shell) vs pod_shell/frontend/src/App.js (DAP Portal routes)" is BACKWARDS. Corrected labels captured below (§1) and inherited by the spec header.

Standing bounds carried into Phase 1:
- Zero push · zero remote configured on `programme/track-a` · terminal `pytest` only · **`testing_agent` STRICTLY BANNED**.
- Additive-only per SO §3.8 · three-repo discipline · ratchet monotonic-up floor **5695** · R-88+ OWNER-RATIFICATION-PENDING carries forward.
- **Unification direction (R-91 closure card MUST NOT · verbatim):** "Edit `/app/frontend/**` during this wave — the unification direction is `/app/frontend/**` (specialist head) → `pod_shell/frontend/**` (repo mirror), NEVER the other way." → the specialist writes to `pod_shell/frontend/**`; my Phase 1 touches nothing on `programme/track-a` and nothing on `/app/frontend/**`.

---

## 1 · App.js measurements · three variants exist, each with distinct SHA

Measured this session via `sha256sum` + `wc -l`. Labels corrected per owner verbatim above.

| Path | SHA256 | Lines | Role (owner-verified) |
|---|---|---|---|
| `/app/frontend/src/App.js` | `282650cbb514ea5cdfacef2d5ca0ac14f040d2809c1107af98fcd0f8799c6374` | 71 | **DAP Portal + OS Prototype** (Track 1 `/dap/*` + Track 2 `/`) · runtime authoritative · lineage: `dc48d5313` (2026-09-20T14:21:07Z) → since evolved through `b33d19a8d` |
| `/app/assessment_workspace/repos/Extraction-Akki/pod_shell/frontend/src/App.js` | `ef20409b38425c15e6acea6226ff197742b805bc008a17bc2dbf450361e4ff5a` | 1084 | **V8-shell-port** · pod-shell mirror at pre-`dc48d5313` snapshot · hosts the V8 substitution engine + `window.V8_SUBSTITUTIONS_DUMMIES` + PortalIframe |
| `/app/assessment_workspace/repos/Extraction-Akki/frontend/src/App.js` | `e381de86a593ef90681cb391bbdf60a1a8cbb40a71c0e7d95e14e2aa334ededd` | 154 | Retired **AkkiV4Shell** · repo `frontend/src/` tree · declared stale by Fidelity Batch B1 note (2026-08-01) · NOT part of runtime mirror (`test_ship_manifest_dod` compares runtime `/app/frontend/**` vs `pod_shell/frontend/**` only) |

Absence-as-finding: no fourth App.js variant on disk under the four cloned repos.

## 2 · `/app/frontend/src/App.js` · module anatomy (verbatim landmarks)

Opened in-session · lines 1-71 verbatim. Key structural facts:

- L1: `import "@/App.css";`
- L2: `import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";`
- L4-L15: comment block "── DAP Portal (Track 1) ──" + "── OS Prototype v2 (Track 2) ──"
- L5-L12: **8 DAP page imports** via `@/pages/dap/*`: `DAPLayout`, `DAPLanding`, `AvailableResources`, `DataGovernance`, `RequestLifecycle`, `DataEstates`, `ExtractModes`, `ConnectResources`
- L15: `import OSPrototype from "@/pages/os/OSPrototype";`
- L17-L27: module docstring stating "Two tracks mounted under the same React router: Track 1 — `/dap/*` : The Data Access Portal (full build) · Track 2 — `/` : The OS Prototype v2 (iframe-wrapped standalone HTML) [...] The OS Prototype route preserves the existing iframe approach from prior waves (PortalIframe / v8_prototype.html), ensuring backward compatibility with the substitution engine and all existing harness probes."
- L29-L68: `function App()` returning `<BrowserRouter>` with:
  - L35: `<Route path="/" element={<OSPrototype />} />`
  - L38-L61: `<Route path="/dap" element={<DAPLayout />}>` with 7 nested routes:
    - `index` → `DAPLanding`
    - `extract/:mode` → `ExtractModes`
    - `resources/:tab` → `AvailableResources`
    - `governance/:tab` → `DataGovernance`
    - `connect/:tab` → `ConnectResources`
    - `requests` → `RequestLifecycle`
    - `estates/:estateId` → `DataEstates`
    - `*` (within DAP) → `Navigate to="/dap"`
  - L64: `<Route path="*" element={<OSPrototype />} />` (fallback)
- L71: `export default App;`

Absence-as-finding: **zero `V8_SUBSTITUTIONS`, zero `window.V8_SUBSTITUTIONS_DUMMIES`, zero `applySubstitutions`, zero `MutationObserver` in `/app/frontend/src/App.js`**. The React tree does not host the substitution engine.

## 3 · `/app/frontend/src/pages/os/OSPrototype.jsx` · module anatomy

Opened in-session · lines 1-105 verbatim. Key facts:

- 105-line React component wrapping `/v8_prototype.html` in an `<iframe>` sized to `100vw × 100vh` with `data-testid="v8-prototype-iframe"`.
- Fetches on iframe `load` event: `${backend}/api/registry/facts`, `${backend}/api/census/latest`, `${backend}/api/compute/estate`.
- Populates a `liveValues` local — but does NOT apply those values to the iframe's DOM.
- L77-L80 docstring verbatim: *"The iframe is the prototype HTML which has its own dc-runtime · Substitutions are applied by the original applySubstitutions in App.js · Since this is now separate, we still let the iframe render its own content"* — explicit acknowledgment that the substitution mechanism was left behind at the split.
- L92-L93 outer `<div>` carries `data-testid="os-prototype"` + `data-substitution-applied={substitutionsApplied}` (attribute is set once to `1` in `onLoad`, not tied to real substitution work).

Cross-check: **the harness ground-truth invariant reads `window.V8_SUBSTITUTIONS_DUMMIES` (exposed by App.js at pod_shell) · this global is not set anywhere in `/app/frontend/src/`.** Grep-negative confirmed.

## 4 · `pod_shell/frontend/src/App.js` · module anatomy (1084 lines · sampled landmarks)

Opened in-session at L1-150 verbatim + `grep -n` over full file:

- L1-3: imports (`@/App.css`, `useEffect/useRef/useState`, `BrowserRouter/Routes/Route` — note: NO `Navigate`, NO `@/pages/*` imports).
- L5-52: Wave G4 module docstring (verbatim owner corrections; V8 LITERAL adoption + owner Wave G3 REJECT corrections; retirement of 14 legacy pod component imports).
- L58-68: helper phrase functions `_sourcesPhrase(sources)` + `_tablesPhrase(tables)`.
- L93-687: **`const V8_SUBSTITUTIONS = [...]`** array · **37 named rules** total (`grep -c '^    name:' pod_shell/frontend/src/App.js` = 38 including the `.map()` template literal at L690):
  - Registry surface (9 rules): `registry-aside-hero-sentence` (styled-element-anchor, slot #1) · `registry-census-header/-byline` (slot #2 pair) · `tile-total-held-value/-label` · `tile-share-measured-value/-label` · `tile-opportunities-value/-label` (6 topline tiles).
  - Compute-v2 surface (11 rules): `compute-v2-clusters-value/-byline` · `-gpus-value/-byline` · `-capacity-value` · `-committed-value` · `-free-value` · `-jobs-waiting-value` · `-workflows-month-value` · `-utilisation-value` · `-runs-receipted-value`.
  - Compute-residuals-r1 chart surface (14 rules): `-chart-caption-door/-week/-state` (3 captions) + `-bar-door-{train,extract,export,measure,prove}` (5 door bars) + `-bar-week-{1,2,3,4}` (4 week bars) + `-bar-state-{committed,free}` (2 state bars).
  - Compute-residuals-r2 note surface (3 rules): `-note-capacity/-committed/-free`.
- **L690: `window.V8_SUBSTITUTIONS_DUMMIES = V8_SUBSTITUTIONS.map((r) => ({ name: r.name, ... }));`** — the harness contract point (per `test_v8_substitution_rules_bind_to_rendered_dom.py::_load_ground_truth`).
- L698-732: DOM walk helpers `_findAncestorContainingText`, `_findAncestorWithSlot`.
- L734-889: `function applySubstitutions(doc, vals)` — the substitution engine (element-anchor + text-node + styled-element-anchor + tile-value modes with MutationObserver re-application).
- L891-1066: `function PortalIframe()` — iframe host wrapping `/v8_prototype.html`, MutationObserver over `iframe.contentDocument.body`, 3 fetches (`/api/registry/facts`, `/api/census/latest`, `/api/compute/estate`), `data-substitution-applied` counter on outer div.
- L1071-1082: `function App()` — `<BrowserRouter><Routes><Route path="/" element={<PortalIframe />} /><Route path="*" element={<PortalIframe />} /></Routes></BrowserRouter>`.

Absence-as-finding: **zero `/dap/*` routes, zero `Navigate`, zero `@/pages/*` imports in `pod_shell/frontend/src/App.js`.** This tree is the pre-`dc48d5313` V8-shell-port snapshot.

## 5 · pages/ tree inventory (test_wave_g_pod_shell_frontend_mirror::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir)

Measured this session via `find [tree]/src/pages -type f | sort`:

| Tree | Path | File count | Manifest |
|---|---|---|---|
| Runtime (authoritative) | `/app/frontend/src/pages/` | **9** | `dap/AvailableResources.jsx`, `dap/ConnectResources.jsx`, `dap/DAPLanding.jsx`, `dap/DAPLayout.jsx`, `dap/DataEstates.jsx`, `dap/DataGovernance.jsx`, `dap/ExtractModes.jsx`, `dap/RequestLifecycle.jsx`, `os/OSPrototype.jsx` |
| Pod-shell (mirror) | `/app/assessment_workspace/repos/Extraction-Akki/pod_shell/frontend/src/pages/` | **0** | (directory absent or empty · `find` returned no entries) |
| Repo stale (unrelated) | `/app/assessment_workspace/repos/Extraction-Akki/frontend/src/pages/` | 40+ | AkkiV4Shell + retired v4 tree · not scanned by the mirror invariant |

**Byte-identity delta:** pod-shell mirror is 9 files short (all 9 in `/app/frontend/src/pages/` have no counterpart). The FE specialist landing must materialise 9 files under `pod_shell/frontend/src/pages/` byte-identical to their `/app/frontend/src/pages/` counterparts.

## 6 · components/ tree inventory (currently GREEN under `test_runtime_frontend_components_match_repo_pod_shell`)

Measured this session · both trees carry **17 `.jsx` files** with identical filenames + identical byte sizes + identical mtimes (Sep 19 21:29 at pod_shell · Aug 25-27 at runtime):

`AuditTrail.jsx`, `Chat.jsx`, `ClassBadge.jsx`, `CommissionWizard.jsx`, `ConnectDrawerChat.jsx`, `ConnectWizard.jsx`, `CostLedger.jsx`, `DataShield.jsx`, `EvidenceRegister.jsx`, `Governance.jsx`, `GreyMirror.jsx`, `ModelEcosystem.jsx`, `RefusalCard.jsx`, `Registry.jsx`, `SkillFiles.jsx`, `ThinkLab.jsx`, `Training.jsx`.

Neither pod_shell/App.js nor `/app/frontend/src/App.js` imports any of these 17 components at present (verified via `grep`); they are dead donor material per Wave G4 owner correction "14 legacy pod component imports removed from App.js" — retained on disk under both trees to preserve additive-only discipline.

## 7 · public/index.html + design/ + hooks/ + apiClient.js mirror surface (Wave G Step 1 extended scope)

Measured surfaces required by `test_wave_g_pod_shell_frontend_mirror.py`:

- `public/index.html` — status this-session: NOT INDEPENDENTLY VERIFIED here (Wave G Step 1 note claims both trees restored byte-identical at 2026-08-28 with the amended-close addendum). Falls under the mirror invariant test `test_app_frontend_public_index_html_mirrors_pod_shell` which is currently GREEN (not in the 5 baseline failures set).
- `design/` — vacuously green per test docstring: "Currently both trees are empty of design/ files, so this check is vacuously green."
- `hooks/use-toast.js` — restored at 2026-08-28 Wave G Step 1 (both trees byte-identical per that seal note); GREEN today (not in the 5 baseline failures set).
- `apiClient.js` — absent from both trees this session (the DAP Portal uses `@/lib/apiClient` — under `src/lib/`, not `src/`); vacuous per test docstring.

## 8 · Baseline failure map (5 wrapped entries · closure_wave=CP-APP-JS-UNIFY · closure_wave_slot=R-91)

Read verbatim this session from `repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json`. All 5 wrapped in **two disjoint annotation fields** (both fields written to preserve R-86 Property-4 set-equality invariant · pod_shell_mirror_drift entries vs cp10 v8-engine-retirement entries do not collide).

**Field `known_runtime_drift_annotations` (R-86 · 3 entries · drift_kind = `pod_shell_mirror_drift`):**

| # | Test nodeid | Entry retires when |
|---|---|---|
| 1 | `test_ship_manifest_dod.py::test_runtime_frontend_app_matches_repo_pod_shell` | `sha256(/app/frontend/src/App.js) == sha256(pod_shell/frontend/src/App.js)` |
| 2 | `test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_App_js_mirrors_pod_shell_App_js` | Same byte-identity as #1 (test-file duplicate coverage) |
| 3 | `test_wave_g_pod_shell_frontend_mirror.py::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir` | Every `.jsx/.js` file under `/app/frontend/src/pages/**` has a byte-identical peer under `pod_shell/frontend/src/pages/**` |

**Field `known_r91_closure_scheduled_receipt_drift_annotations` (R-88+ A-extension · 2 baseline entries + 1 non-baseline guard):**

| # | Test nodeid | Entry retires when | In baseline set? |
|---|---|---|---|
| 4 | `test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom` | Harness ground-truth `per_rule` non-empty AND every rule has `bound_to_rendered_dom == True` | YES |
| 5 | `test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present` | Ground-truth entry for `registry-aside-hero-sentence` has `matched_by_marker == True` | YES |
| 6 (guard) | `test_w_registry_full_build_cp10_wave_close.py::test_cp10_harness_receipt_is_still_recent` | Not currently in baseline_failures set (still GREEN today · annotated only) — will remain GREEN if harness receipt refreshes within its freshness window at Phase 2 close | NO (annotation-only) |

Culpable commit (both fields' `reason` field verbatim): `dc48d53131be2a36b36aabab83048cbbb779cfa2` on `main` at 2026-09-20T14:21:07Z ("feat(frontend): DAP Portal full build + OS Prototype v2 React surfaces") — replaced the substantive V8 substitution engine that lived in `/app/frontend/src/App.js` with a slim iframe-wrapper shell for the DAP Portal.

## 9 · R-86 + R-88+ property invariants that continue GREEN through Phase 1

Reading from the closure card `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` EXIT section (verified against test files opened this session):

R-86 authored invariants (5 tests · GREEN through Phase 1 & Phase 2):
- `test_baseline_drift_annotations_present.py::test_every_mirror_drift_baseline_entry_has_an_annotation`
- `test_baseline_drift_annotations_present.py::test_every_annotation_has_the_required_8_field_shape`
- `test_baseline_drift_annotations_present.py::test_annotation_closure_card_paths_resolve_to_real_files`
- `test_baseline_drift_annotations_present.py::test_annotation_count_equals_mirror_drift_baseline_entry_count`
- `test_baseline_drift_annotations_present.py::test_every_annotation_names_cp_app_js_unify_as_closure_wave`

R-88+ additive invariants (6 tests · GREEN through Phase 1 & Phase 2):
- `test_r88_cp10_harness_scheduled_closure_drift_annotation.py::test_cp10_harness_scheduled_closure_annotation_present`
- `test_r88_cp10_harness_scheduled_closure_drift_annotation.py::test_cp10_annotation_has_required_8_field_shape`
- `test_r88_cp10_harness_scheduled_closure_drift_annotation.py::test_cp10_annotation_closure_wave_is_cp_app_js_unify_r91`
- `test_r88_cp10_harness_scheduled_closure_drift_annotation.py::test_cp10_annotation_closure_card_path_resolves_to_real_file`
- `test_r88_cp10_harness_scheduled_closure_drift_annotation.py::test_cp10_annotation_closure_card_line_present_in_closure_card`
- `test_r88_cp10_harness_scheduled_closure_drift_annotation.py::test_harness_receipt_is_non_vacuous_when_card_status_is_sealed` — **fires RED if R-91 closure card `milestone_status` flips to SEALED without harness receipt regenerated non-vacuous**.

Set-equality guard (R-86 Property 4): the 3 keys of `known_runtime_drift_annotations` must equal the 3 `pod_shell_mirror_drift` baseline entries · this-Phase-1 does NOT alter either set · GREEN carries forward.

## 10 · CP10 harness architectural discrepancy (found · stated · not resolved this Phase)

Per owner D-ruling verbatim (§0 above): "State the discrepancy in the receipt as found; R-91 resolves it either way." Statement of the discrepancy:

**Observed:** The React tree under `/app/frontend/src/` contains ZERO `V8_SUBSTITUTIONS` matches. The `OSPrototype.jsx` iframe wrapper's own docstring at lines 77-80 confirms substitutions were left behind at the DAP Portal split.

**Consequence:** A pure byte-identity mirror-copy of `/app/frontend/**` into `pod_shell/frontend/**` — the discipline the R-91 closure card MUST NOT clause enforces — will produce a `pod_shell/App.js` that ALSO carries zero `V8_SUBSTITUTIONS`, and the harness will continue to report `dummies_declared=0 · marked_slots=0 · per_rule=[]`. The 3 mirror-drift baseline entries would retire (byte-identity restored), but the 2 v8-cascade baseline entries would remain RED (harness still vacuous) — AND the R-88+ guard `test_harness_receipt_is_non_vacuous_when_card_status_is_sealed` would fire RED the moment the R-91 milestone_status flips.

**Architectural resolution options (surface only · this HUNT does not choose):**
- **Option A · Restore engine into React tree** — the substitution engine (`V8_SUBSTITUTIONS` array + `window.V8_SUBSTITUTIONS_DUMMIES` exposure + `applySubstitutions()` + MutationObserver + iframe-content mutation) is re-authored into `/app/frontend/src/App.js` OR `/app/frontend/src/pages/os/OSPrototype.jsx` at the specialist landing. This is an EDIT of `/app/frontend/**` — MUST NOT clause of the closure card literally forbids editing `/app/frontend/**` during this wave for the mirror-drift half; the CP10 half is textually a separate artifact of the same wave (owner D-ruling explicitly authorises R-91 to resolve CP10 "either way"). Reading: the MUST NOT applies to the mirror direction of copying, not to authoring the substitution engine into a target file that ends up mirrored one-to-one.
- **Option B · Embed engine inside `/app/frontend/public/v8_prototype.html`** — the static HTML iframe source itself gains a `<script>` block declaring `window.V8_SUBSTITUTIONS_DUMMIES` and applying substitutions inside its own document context; the harness would need retargeting to read `iframe.contentWindow.V8_SUBSTITUTIONS_DUMMIES` rather than the outer `window`. Also edits `/app/frontend/**` (the `public/` subtree) and edits the harness.
- **Option C · Evolve the invariant contract** — declare that the DAP Portal architecture legitimately retires the V8 substitution engine, retire `test_v8_substitution_rules_bind_to_rendered_dom.py` from the baseline and from `test_r88_cp10_harness_scheduled_closure_drift_annotation.py::test_harness_receipt_is_non_vacuous_when_card_status_is_sealed` via an owner ruling to that effect. This retires tests rather than restoring capability. Owner has NOT ruled this option; the current annotation umbrella (R-88+ D-ruling + A-extension) presumes closure-by-restoration, not closure-by-retirement.

**This HUNT states the discrepancy · the FE specialist proposes and lands the resolution · the owner adjudicates at seal-verify.**

## 11 · Byte-identity target after FE specialist landing (Phase 2 exit criterion)

For the pod_shell mirror-drift half to close:
- `sha256(/app/frontend/src/App.js) == sha256(pod_shell/frontend/src/App.js)`.
- For every `p` under `/app/frontend/src/pages/**` (currently 9 `.jsx` files enumerated §5), `sha256(p) == sha256(pod_shell/frontend/src/pages/{relpath})` and both sets equal.
- `test_ship_manifest_dod::test_runtime_frontend_app_matches_repo_pod_shell` GREEN.
- `test_wave_g_pod_shell_frontend_mirror::test_app_frontend_App_js_mirrors_pod_shell_App_js` GREEN.
- `test_wave_g_pod_shell_frontend_mirror::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir` GREEN.
- Same-commit retirement of the 3 keys under `known_runtime_drift_annotations` alongside their removal from the `baseline_failures` array (R-86 Property 4 enforces set equality).

For the CP10 non-vacuous half to close (either the same commit or a paired commit depending on Option A/B/C picked):
- `phase0/harness_ground_truth/latest.json` regenerated post-landing with `dummies_declared > 0`, `marked_slots_count > 0`, `per_rule` non-empty, AND every rule `bound_to_rendered_dom == True`, AND the `registry-aside-hero-sentence` entry has `matched_by_marker == True`.
- `test_v8_substitution_rules_bind_to_rendered_dom.py::test_every_v8_substitution_rule_binds_to_harness_rendered_dom` GREEN.
- `test_v8_substitution_rules_bind_to_rendered_dom.py::test_slot1_registry_aside_marker_present` GREEN.
- Retirement of the 2 v8-cascade keys under `known_r91_closure_scheduled_receipt_drift_annotations`.
- R-88+ guard `test_harness_receipt_is_non_vacuous_when_card_status_is_sealed` transitions from "vacuous permitted while SCHEDULED" to "non-vacuous required at SEALED" — both branches GREEN post-landing.

Baseline shrink at Phase 2 landing: **5 → 0** (both fields retire together with matching set-equality removals · R-86 Property 4 + R-88+ annotation invariants remain GREEN).

Ratchet at Phase 2 landing: `5695` → `5695 + Δ` where `Δ ≥ 5` (the 5 wrapped tests flip to pass) + any additional passing tests authored in the wave (e.g. FE-specialist regression tests). Baseline set shrinks (permitted per set-equality invariants operating over the joint retirement). Both `counts_at_baseline.passed` and `passed_floor` bump together (CCS2 lesson).

## 12 · Endpoints the merged App.js OR its restored substitution engine must fetch (current pod_shell + OSPrototype semantics · verified in-session)

Both `pod_shell/App.js::PortalIframe` (L949, L978, L1009) and `/app/frontend/src/pages/os/OSPrototype.jsx` (L34, L49, L70) fetch these three backend endpoints in `useEffect` on iframe `load` event:

- `${REACT_APP_BACKEND_URL}/api/registry/facts` — provides `data_sources` list with per-source `table_count`; drives `estateSources` / `estateTables` live values on slot #1.
- `${REACT_APP_BACKEND_URL}/api/census/latest` — provides `census.rollup.database_count` / `census.rollup.table_count` + `census.census_id` + `census.finished_at_utc`; drives Registry census header/byline slot #2 + overrides estate counts when higher-quality.
- `${REACT_APP_BACKEND_URL}/api/compute/estate` — provides `hosts` list; drives 11 compute-v2 tile substitutions + 17 compute-residuals-r1/r2 rules.

Both use `process.env.REACT_APP_BACKEND_URL || ""` prefix · both wrap fetches in `try/catch(_)` silent-fail · both consume the response body's specific shape without additional error handling.

## 13 · Standing invariants that MUST continue GREEN through Phase 1 (state-only opening)

Since Phase 1 modifies **only** state files under `/app/assessment_workspace/{phase0/,notes/,STATE/}` and does **not** touch `baseline_failures.json`, `notes/ORCH_BOOT.md`, the R-91 closure card, or any test file:

- All 5 baseline entries stay wrapped (owner Q2 verbatim: "all 5 wrapped baseline failures stay wrapped through Phase 1 and retire ONLY in Phase 2").
- Ratchet stays `5695 pass / 5 fail / 1 skip · floor 5695`.
- `baseline_failures.json` sha256 stays `4e7caa47f437b7fe15731bd9f6eb1cbf3f202d3f09b2db495b6c8be668125694`.
- `notes/ORCH_BOOT.md` stays sha256 `0c67f0e639bfd7edf58f925c349761d8917808b0af3add11fc8ebcf64577df0f` (no ratchet delta · no head advance until Phase 2 code lands).
- The R-91 closure card `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` `milestone_status` stays SCHEDULED (not yet SEALED).
- R-86 property tests + R-88+ property tests remain GREEN (annotation sets unchanged).

## 14 · What Phase 1 lands

Files added this-Phase (all under `/app/assessment_workspace/`):
- `phase0/spec_hunt_receipts/20260920T235800Z_r91_cp_app_js_unify_hunt_receipt.md` — this file.
- `phase0/specs/r91_cp_app_js_unify_spec.md` — FE specialist landing blueprint (Phase 1 authored).
- `notes/FE_DISPATCH_READY_R91.md` — dispatch-ready flag pointer.

STATE files appended (single Phase 1 opening commit on `master`):
- `STATE/DECISIONS.md` — R-91 Phase 1 opening banking + FE-DISPATCH-READY flag raised.
- `STATE/NEXT.md` — R-91 Phase 1 IN-FLIGHT marker + queue update.
- `STATE/PINS.md` — R-91-PHASE-1-PINS block.

Files NOT touched this-Phase:
- Any file under `/app/assessment_workspace/repos/Extraction-Akki/**` (code branch fully untouched).
- Any file under `/app/frontend/**` (specialist-authoritative tree untouched).
- `notes/ORCH_BOOT.md` (no ratchet delta · no head advance).
- `/app/frontend/public/audit/ORCH_BOOT.md` (POD audit mirror untouched).
- The R-91 closure card at `STATE/OBJECTIVES/CP_APP_JS_UNIFY.md` (contract unchanged · this Phase confirms it, does not amend it).

## 15 · Discipline verification against Standing Order §6 stop-conditions

- **SO §6.4 pre-ruling NOT triggered:** Phase 1 authoring is inside the ratified R-91 slot scope (Ruling 1 + R-91 schedule + R-88+ A-extension); no material extension beyond that scope.
- **Stop-conditions #1/#2/#3 NOT triggered:** no sealed-file edit · no cross-repo mirror hole invention · no drop-schema uncorroborated ingest.
- **MEM-R-053 CROWN BAN NOT triggered:** no user-mode operation on the crown.
- **§3 tests-first discipline:** state-only opening — no code delta means no RED-GREEN cycle at Phase 1; the RED-GREEN cycle is Phase 2's discipline (FE specialist lands byte-identity code → mirror invariants flip green → CP10 harness regenerates → v8-cascade tests flip green → 3-Commit Seal fires).
- **§3.8 additive-only:** all Phase 1 files are net-new adds; STATE appends are additive (comment-anchor delimited); no edits below prior anchors.
- **CCS2 lesson:** ratchet stays byte-identical this-Phase (no counter advance possible without a code delta).

## 16 · Deliverable pointers for the FE specialist dispatch

- **Spec:** `/app/assessment_workspace/phase0/specs/r91_cp_app_js_unify_spec.md` (this-Phase authored).
- **Hunt receipt (this file):** `/app/assessment_workspace/phase0/spec_hunt_receipts/20260920T235800Z_r91_cp_app_js_unify_hunt_receipt.md`.
- **Closure card (contract · unchanged this-Phase):** `/app/assessment_workspace/STATE/OBJECTIVES/CP_APP_JS_UNIFY.md`.
- **Standing Order (permanent law):** `/app/assessment_workspace/STATE/STANDING_ORDERS.md`.
- **Baseline manifest (read-only for FE specialist):** `/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json`.
- **Harness ground-truth path (regenerated at Phase 2 close):** `/app/assessment_workspace/phase0/harness_ground_truth/latest.json`.

**END OF HUNT RECEIPT.**
