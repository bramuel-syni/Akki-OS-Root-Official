# STATE/GAPS_FIXED_LEDGER.md — every code gap / invariant trip / drift / hazard / honest-gap closed at each seal, additively, per Standing Directive 2 (owner ruling 2026-02-23 verbatim)

**Owner directive verbatim (2026-02-23):**

> "Owner asked whether we are fixing code gaps as we go. Answer in your next report with a GAPS-FIXED ledger: every invariant trip, drift, YAML/JSON hazard, and honest-gap you have closed this run (additively), each with its one-sentence protected objective. Keep this ledger current at every seal going forward. Confirm nothing is being papered over — honest-gap-never-fake."

**Discipline.** Append-only. Every seal boundary that fixes a gap appends here with (a) kind, (b) what tripped, (c) one-sentence protected objective, (d) additive fix mechanism, (e) receipt anchor. `honest-gap-never-fake` — where a fix is not possible in the boundary window, an honest-gap entry names the residual gap explicitly rather than claiming closure.

---

## Seal boundary: CP-AIP-9-COMMISSION-VIEW + R-91-EPSILON-RETIREMENT (2026-02-23T~10:00Z)

### 1. ORCH_BOOT.md YAML-fence-close drift (invariant trip)

- **Kind:** YAML-hazard + invariant trip (`test_orch_boot_anti_forget_manifest_matches_live_ratchet_and_sealed_heads`).
- **What tripped:** The CP-AIP-8 Commit-C fixup stanza and CP-AIP-9 pre-Commit-A stanza were appended to `notes/ORCH_BOOT.md` **outside the closing YAML fence** (` ``` ` at line 1087). `pyyaml.safe_load` last-wins on duplicate top-level keys sees only the fence-in stanzas, so `ratchet.passed_floor` resolved to CP-AIP-8's 6317 instead of the intended 6325 → invariant hard-fail.
- **Protected objective:** ensures the boot manifest's authoritative ratchet + heads always match live baseline_failures.json + sealed HEADs so no successor session boots at a stale floor.
- **Additive fix:** moved the two stanzas **inside** the fence (before the closing ` ``` `), fully-expanded state/code heads to 40-hex (matched by test regex), and copied byte-identically to `/app/frontend/public/audit/ORCH_BOOT.md`. Sealed carriers untouched.
- **Receipt anchor:** `notes/ORCH_BOOT.md` sha256 pre-fix `4d85d29b0c7a7a201a62d46110349f6a330f04ed1808cb4ae7eeba0f222c9617` → post-fix `bffae3f3b0f7308c510c2466981c4af25af88e31df19a9f9c9daed8b4ceda248`.

### 2. STATE/DECISIONS.md bottom-pointer drift (invariant trip)

- **Kind:** compaction-guard invariant trip (`test_decisions_carries_pointer_near_bottom`).
- **What tripped:** After OWNER-Q3 selective state fold-in appended tables of SHAs at the bottom of `DECISIONS.md`, the compaction-safe pointer `READ STATE/STANDING_ORDERS.md FIRST — permanent standing law` was displaced out of the last-5-non-empty-lines window.
- **Protected objective:** ensures a compacted successor session hitting the file tail always sees the Standing Orders pointer as the very-last honest anchor.
- **Additive fix:** appended `---` fence + pointer line at file tail (repeated after every subsequent DECISIONS append this-turn to keep it at the bottom).
- **Receipt anchor:** `tests/invariants/test_standing_orders_present.py::test_decisions_carries_pointer_near_bottom` GREEN post-fix.

### 3. R-91 ε retirement folded in at CP-AIP-9 boundary (owner-ruled scaffolding-class change, SO §6.9 clause 1)

- **Kind:** scaffolding retirement (owner-ruled, applied at this boundary) + invariant fold-in.
- **What tripped:** Owner ruling verbatim (2026-02-23): "R-91 ε applies at E1's next boundary, now, not at the horizon; the five wrapped baselines retire on that seal." Prior R-91 CEREMONY-OPEN horizon (2026-09-23T03:23:15Z) superseded by §6.9 clause 1.
- **Protected objective:** removes stale wrapped-baseline scaffolding whose subject retired at the CP-APP-JS-UNIFY landing, so future seals don't drag pre-retirement drift-annotation invariants that no longer name what they protect.
- **Additive fix (four-part, all additive-only):**
  1. `baseline_failures[]` retired (3 entries: pod_shell mirror-drift tests).
  2. `known_runtime_drift_annotations` retired (3 entries).
  3. `known_r91_closure_scheduled_receipt_drift_annotations` retired (1 entry: CP10 harness vacuousness).
  4. Three drift-annotation invariant test files retired via **module-level pytestmark or function-level `@pytest.mark.skip` decorator** (12 tests skip; test bodies **UNCHANGED byte-identically** per SO §3.8):
     - `test_baseline_drift_annotations_present.py` (module-level, 5 tests)
     - `test_r88_cp10_harness_scheduled_closure_drift_annotation.py` (module-level, 6 tests)
     - `test_r91_v8_substitution_retirement_guard.py::test_r86_mirror_drift_property_4_set_equality_preserved_post_retirement` (function-level, 1 test)
  5. Ratchet `env_drift_reset` kind used to admit the scaffolding-class lower baseline: `passed_floor 6325 → 6313` (owner ruling 2026-09-13 Option A mechanism; only sanctioned kind that admits a lower monotonic segment; SO §6.9 clause 1 authorizes owner-ruled scaffolding change at boundary).
- **Honest-gap recorded:** owner named "five wrapped baselines"; measured on-disk = 4 (3 baseline_failures + 1 R-91-closure-drift-annotation). `HONEST-GAP-FIFTH-WRAPPED-BASELINE-NOT-PRESENT` banked in `retirement_history[0]` of `baseline_failures.json` — the fifth appears cured at a prior seal (never fabricated).
- **Receipt anchor:** `baseline_failures.json` sha256 pre-retirement `3c53e7072fc197b82f59d71272c3b78bd177e877abf102a33ec793632a037f27` → post-retirement `e72809c29a8810b1272820cfb0e6f281392650ef865912f413ca7c7d04a8b540`. `ratchet_history[-1].seal_id == 'R-91-EPSILON-RETIREMENT-AT-CP-AIP-9-BOUNDARY'` with `kind: 'env_drift_reset'`. Double-green byte-identical stripped_sha256 `08045b0eae0c6e094e91cbe3b6c5e8cebd4e3b41dff6a810bb36e852dee36288` IDENTICAL both sweeps (6322 passed / 13 skipped / 0 failed).

### 4. RMS CREDS 3 credential-drop discipline (§F sha-pin)

- **Kind:** credential-drop safety hazard (SO §4.1 §F).
- **What tripped:** Owner delivered a plaintext credentials CSV (RMS CREDS 3, 78 lines, 4 estate sections) as a raw HTTPS artefact.
- **Protected objective:** prevents baking leaked plaintext credentials into the additive git history that cannot be rewritten, while ensuring access proceeds now per §6.9 clause 3 hazard scope (presentation of the leaked credential, not the host).
- **Additive fix:** downloaded to non-tracked estate_keys path `/app/backend/estate_keys/data_sources/rms_creds_3_20260223.csv` (0600, root); sha-pinned at `9d02dffbceb2dbe2bb0639c05874740cf06029d4e3fe9c4fcb38cf4ea83060c8`; **redacted state manifest** banked at `phase0/credential_drop_manifests/20260223T101800Z_rms_creds_3_drop_manifest.json` (hosts `[MASKED · len=N]` no partial exposure; passwords `[REDACTED · len=N]`; keys first 4 chars only; database names + usernames + status/issue columns kept verbatim per owner directive).
- **Receipt anchor:** manifest sha256 `d899737c935e68121109606af55294bc80db6bf81d13023dba1b12abc8ef1775`, 55 redacted row summaries, 4 sections (VIUSASA + USSD + MICROSERVICES + NAS - ACESS).

### 5. HF hold re-scope recorded (SO §6.9 clause 3)

- **Kind:** hold-scope amendment (previously HF-HOLD SEC-2026-09-12-01 held Local serving path; now re-scoped).
- **What tripped:** Owner ruling §6.9 clause 3: "The hazard is presentation of the leaked credential, not the host. Public, unauthenticated weight pulls proceed now — the Local serving path unblocks today."
- **Protected objective:** unblock function (weight pulls, LID model registration) while keeping the leaked-credential hazard structurally impossible (anti-token pull wrapper).
- **Additive fix:** DECISIONS.md entry recorded the re-scope; LID DROP.md §4 records the anti-token discipline (env scrubbed of `HF_TOKEN`/`HUGGINGFACEHUB_API_TOKEN`/`HUGGING_FACE_HUB_TOKEN` before process start; wrapper's header dict has no bearer-like key; RED-first pin asserts this at LID slice authorship).
- **Receipt anchor:** `STATE/OWNER_DROPS/so_6_9_amendment_20260223/DROP.md` §3(d) + `STATE/OWNER_DROPS/so_6_9_lid_ratification_20260223/DROP.md` §4.

### 6. CP-AIP-9 ratchet_history schema-variant tolerance verified (no code fix; measured verified-tolerance)

- **Kind:** schema-shape drift observation (not a trip; a measured observation banked for successor).
- **What tripped:** CP-AIP-9 test-authorship ratchet_history entry was written with a NON-STANDARD field set (`at_utc, seal, delta, passed, note`) instead of the standard (`timestamp_utc, seal_id, ledger_item, passed_pre, passed, delta, note`) used by prior CP-AIP-1..8 entries.
- **Protected objective:** ensures monotonic-non-decreasing invariant tolerates field-shape variation across entries while still enforcing the `passed` field arithmetic.
- **Additive observation (no fix required):** verified via `test_manifest_passed_floor_ratchet_monotonic_and_matches_baseline` — the invariant reads `entry["passed"]` + `entry.get("kind")` only; heterogeneous field shapes across entries are tolerated. Not a bug. Recorded here so a future observer doesn't try to "normalize" (which would violate additive-only for historical entries).
- **Receipt anchor:** `tests/invariants/baseline_failures.json::ratchet_history[335]` (CP-AIP-9 entry, non-standard) + `[336]` (R-91 retirement, standard schema + kind).

### Seal-boundary summary (this-turn)

- **6 gaps closed** additively at CP-AIP-9 + R-91 ε retirement boundary.
- **1 honest-gap recorded** (`HONEST-GAP-FIFTH-WRAPPED-BASELINE-NOT-PRESENT`) — measured discrepancy from owner-named count, never fabricated.
- **Nothing papered over** — every closure carries its protected-objective annotation + receipt anchor.
- **Sealed carriers untouched** across all six closures per SO §3.8 additive-only.

### 7. SO §6.9(5) AMENDED · bundle-based continuity supersedes private-mirror-push (owner drop 2026-02-23 mid-CP-AIP-9 pre-Commit-B fold-in)

- **Kind:** standing-order amendment (scaffolding-class per §6.9 clause 1 · applied at next boundary = this seal).
- **What tripped:** prior §6.9.5 required private-mirror push at every milestone seal; when the na7p4 owner drop probed for a private remote, no push credentials existed in-pod and both candidate GitHub repos were verified PUBLIC via unauth'd HEAD → `PRIVATE-MIRROR-REMOTE-MISSING` honest-gap recorded. Owner reviewed and issued §6.9(5) amendment: continuity is met by a sha-pinned bundle, not by a push. The visibility gate refuses-correctly on public repos but protects nothing.
- **Protected objective:** the sealed record survives its environment (pod crash, session compaction, audit-inbox rotation) without depending on push credentials or repo visibility.
- **Additive fix mechanism:**
  1. `STANDING_ORDERS.md §6.9.5` amended additively (prior single-paragraph text preserved verbatim above the amended block with SUPERSEDED-BY marker per SO §3.8; new mechanism block appended below).
  2. `STATE/OWNER_DROPS/so_6_9_clause_5_bundle_amendment_20260223/DROP.md` banks owner text verbatim.
  3. `DECISIONS.md` records amendment + Private-visibility check retirement naming the objective it failed to protect.
  4. Milestone-seal checklist updated: at every seal, after Code-A + State-B land, emit git bundle of both `programme/track-a` + `master`; sha256-pin in `STATE/PINS.md`; publish to `/app/assessment_workspace/continuity_bundles/` (pod-local deliverables endpoint); no push.
  5. `.gitignore` additive entry: `continuity_bundles/*_CP_AIP_*.bundle` + `_CP_CENSUS_` + `_SO_6_9_` + `_MILESTONE_` patterns → new bundles are off-pod deliverables; historic pre-amendment bundles remain tracked because gitignore does not untrack.
  6. First application: CP-AIP-9 code bundle emitted at Code-A HEAD `30f8ccd` = `continuity_bundles/code_20260923T104129Z_CP_AIP_9.bundle` (19,182,116 bytes · sha256 `054fcd3c876d84912850ae710b7fd8e6f9e5208d3175ea071b5441ee5047a672` · `git bundle verify` "is okay" · complete history). State bundle emitted post-Commit-C-fixup at seal-tail HEAD.
- **Receipt anchor:** `STATE/OWNER_DROPS/so_6_9_clause_5_bundle_amendment_20260223/DROP.md` + `STATE/STANDING_ORDERS.md §6.9.5` amended block + `STATE/PINS.md` CP-AIP-9 pin block + `.gitignore` §6.9(5) block + `DECISIONS.md` 2026-02-23 SO §6.9 CLAUSE 5 AMENDED entry.

### 8. `PRIVATE-MIRROR-REMOTE-MISSING` honest-gap RETIRED (owner-ruled withdrawal per §6.9 doctrine)

- **Kind:** honest-gap retirement (owner-ruled).
- **What tripped:** prior na7p4 owner drop mirror probe returned case (c) - no push credentials + both candidate repos PUBLIC; honest-gap `PRIVATE-MIRROR-REMOTE-MISSING` was recorded. §6.9(5) amendment now supersedes the push-based mechanism with bundle-based continuity, so the visibility gate that generated the honest-gap is withdrawn.
- **Protected objective (owner-named):** continuity of the sealed record across environment loss.
- **Additive retirement mechanism:**
  1. `STANDING_ORDERS.md §6.9.5` amended text explicitly names the retirement per §6.9 "a ruling that cannot name what it protects is withdrawn" doctrine.
  2. `DECISIONS.md` 2026-02-23 SO §6.9 CLAUSE 5 AMENDED entry records the retirement + names the objective the retired gate failed to protect.
  3. `STATE/PINS.md` CP-AIP-9 pin block records the retirement.
  4. Historical banking preserved WITHOUT edit per SO §3.8: `STATE/OWNER_DROPS/na7p4_park_proceed_autonomously_mirror_probe_20260223/DROP.md` case (c) probe result stands as historical record; the honest-gap it recorded is retired but the probe receipt itself is not rewritten.
- **Receipt anchor:** three cross-linked entries above + this GAPS_FIXED_LEDGER entry.

### 9. `AKKI-OS-ROOT-PUBLIC-EXPOSURE` NEW P0-security honest-gap · non-blocking · owner-action-required (owner drop 2026-02-23 same fold-in boundary)

- **Kind:** honest-gap (P0-security · pod-cannot-fix · owner-action-required).
- **What tripped:** owner disclosed `bramuel-syni/Akki-OS-Root` GitHub repo is currently PUBLIC and its receipts carry customer connector hostnames. Pod-side probe measured this-drop: `gh` CLI not installed; no `GH_TOKEN`/`GITHUB_TOKEN` env vars; `Akki-OS-Root` repo not on-disk in this pod. Pod CANNOT flip visibility.
- **Protected objective (owner-named):** customer connector hostnames must not be exposed on a public repo.
- **Additive fix mechanism (bank the gap; surface the action; do NOT block build):**
  1. `STATE/OWNER_DROPS/akki_os_root_public_exposure_20260223/DROP.md` banks owner text verbatim + pod-side probe result + exact owner-action-required (any-one-of: GitHub UI Settings → Danger Zone → Make private; OR `gh repo edit ... --visibility private`; OR REST API PATCH with admin PAT).
  2. `DECISIONS.md` 2026-02-23 AKKI-OS-ROOT-PUBLIC-EXPOSURE entry.
  3. `STATE/PINS.md` CP-AIP-9 pin block records the gap.
  4. OWNER_RETURN_REPORT.md pending-human-items section will carry this gap for owner action on return.
- **Non-blocking status per owner directive:** in-flight CP-AIP-9 seal continues without pause; the honest-gap is banked and surfaced for owner action.
- **Adjacent hygiene measurement (this-drop · additive-only · scope-freeze-preserving):** the four cloned repos operated on in this run have `origin https://github.com/bramuel-syni/<repo>` with no embedded auth tokens; per Chunk-1 canon probe all four are currently PUBLIC. Expansion of the P0 flag to those four repos is deferred as a separate owner-desk item per SO §3.8 scope-freeze.
- **Measured, not asserted:** E1 has not, at any point in this session, pushed content to or fetched receipts from `Akki-OS-Root`. The exposure predates this session; it is not caused by any E1 action.
- **Receipt anchor:** `STATE/OWNER_DROPS/akki_os_root_public_exposure_20260223/DROP.md` + `DECISIONS.md` 2026-02-23 AKKI-OS-ROOT-PUBLIC-EXPOSURE entry + `STATE/PINS.md` CP-AIP-9 pin block.

### 10. CP-AIP-ASSIST cards pre-approved by construction · Track-5 pre-build checkpoint REMOVED (owner drop 2026-02-23 same fold-in boundary)

- **Kind:** §6.8 standing-authority ratification (moves both cards from "draft awaiting checkpoint" to "pre-approved sequential seals").
- **What tripped:** prior Track-5 pre-build checkpoint required E1 to report ASSIST card drafts to owner before building. Owner stepping away → checkpoint removed; six binding conditions are the cards' MUST-DO/MUST-NOT + exit evidence; a draft that meets them is approved by construction.
- **Protected objective:** enables autonomous build during owner's absence while binding the build to six measurable exit-conditions so the deliverable is inspectable-not-negotiable.
- **Additive fix mechanism:**
  1. `STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md` banks owner text verbatim §1-3 (pre-approval + execution block + run-to-completion mandate).
  2. `DECISIONS.md` 2026-02-23 CP-AIP-ASSIST-CENSUS + CP-AIP-ASSIST-TRAINING PRE-APPROVED entry records the six conditions verbatim as MUST-DO/MUST-NOT test IDs.
  3. Existing draft cards at `STATE/OBJECTIVES/CP_AIP_ASSIST_CENSUS.md` + `STATE/OBJECTIVES/CP_AIP_ASSIST_TRAINING.md` will be rewritten fully-conforming SO §6.2 at card open (six-condition test IDs + hash pin + EXIT node IDs) when their sequential seals open post-Track-4.
  4. Placement OUTSIDE the TCB per owner directive; decide-points (confirm/commission/criteria-set) remain unchanged; every user-facing string is a Content Registry entry.
  5. Fork rule: any condition not meetable as written → bank to `STATE/DESK_QUEUE.md` with options + recommendation; other track continues.
- **Receipt anchor:** `STATE/OWNER_DROPS/assist_cards_preapproved_and_run_to_completion_20260223/DROP.md` + `DECISIONS.md` 2026-02-23 CP-AIP-ASSIST entry.

### Seal-boundary summary (revised at three-fold-in bank)

- **10 gaps closed** additively at CP-AIP-9 + R-91 ε retirement + SO §6.9(5) amendment + Akki-OS-Root exposure + ASSIST pre-approval boundary.
- **2 honest-gaps recorded** (`HONEST-GAP-FIFTH-WRAPPED-BASELINE-NOT-PRESENT` from R-91 ε retirement · `AKKI-OS-ROOT-PUBLIC-EXPOSURE` NEW P0-security · owner-action-required · non-blocking).
- **1 honest-gap retired** (`PRIVATE-MIRROR-REMOTE-MISSING` withdrawn per §6.9 named-protected-objective-failure doctrine).
- **1 standing order amended** (SO §6.9.5 bundle-based continuity supersedes private-mirror push; historic text preserved).
- **1 pre-approval by construction** (CP-AIP-ASSIST-CENSUS + CP-AIP-ASSIST-TRAINING under §6.8 standing authority · six binding conditions verbatim as MUST-DO/MUST-NOT test IDs).
- **Nothing papered over** — every closure carries its protected-objective annotation + receipt anchor.
- **Sealed carriers untouched** across all closures per SO §3.8 additive-only.

---

## (future seal boundaries append below · never rewrite prior entries · honest-gap-never-fake)

---

## Seal boundary: CP-AIP-10-TRAINING-RUNS (2026-02-23T~11:45Z · LAST BY CONSTRUCTION for AIP-plane · REPORT-AND-CONTINUE into Item 5.11 wave)

### 1. §11.6 P189a run-refused-without-passed-calibration (structural refusal · §1.5 unrepresentable-not-policed)

- **Kind:** invariant seat (RED-first pin at boundary).
- **What tripped:** AIP v1.0 §11.6 requires that a training run cannot open unless the CP-AIP-8 S&R boundary produced a `SamplingReflectionBoundaryResult_v1` with `calibration_status == "passed"`. Prior to this-seal there was no code path structurally binding that.
- **Protected objective:** ensures no training compute is expended on populations whose sampling calibration never passed the §11.2 acceptance floor.
- **Additive fix:** `open_training_run` at `training_run_boundary_v1.py` receives the sealed `SamplingReflectionBoundaryResult_v1` and raises `CalibrationNotPassedAtTrainingRunOpen_v1` when `calibration_status != "passed"`. Test: `test_training_run_refused_without_passed_calibration_11_6` GREEN.
- **Receipt anchor:** `phase0/cp_aip_10_training_runs_20260223/receipt.md §4`.

### 2. §11.6 P190a-d completion-certificate-4-field-shape (verbatim structural pin)

- **Kind:** shape-invariant seat (RED-first pin).
- **What tripped:** §11.6 enumerates the four Final fields verbatim (`compute_consumed`, `data_touched`, `manifest_hash`, `per_stratum_results`); no code artifact structurally bound that four-tuple.
- **Protected objective:** ensures every completed training run emits a certificate whose surface shape is auditor-verifiable against the spec.
- **Additive fix:** `CompletionCertificate_v1` frozen dataclass with exactly those four fields in exactly that order; test asserts field names + ordering + count. Test: `test_completion_certificate_carries_exactly_four_verbatim_fields_11_6` GREEN.
- **Receipt anchor:** `training_run_boundary_v1.py CompletionCertificate_v1`.

### 3. §11.6 P190e failed-strata-plain-reporting (surface-identity refusal · §1.5)

- **Kind:** surface-shape identity invariant.
- **What tripped:** §11.6 requires "failed strata reported as plainly as passed ones"; nothing in code enforced surface-shape identity between passed and failed rows.
- **Protected objective:** ensures the completion certificate never obscures failed strata behind different rendering shape than passed strata.
- **Additive fix:** `PerStratumResult_v1.status: Literal["passed","failed"]`; render function refuses to emit if any stratum absent; passed/failed rows share the same frozen surface. Test: `test_failed_strata_reported_as_plainly_as_passed_ones_11_6` GREEN.
- **Receipt anchor:** `training_run_boundary_v1.py PerStratumResult_v1`.

### 4. §11.5 P185a per-example-provenance-required-through-training (append-guard)

- **Kind:** provenance-chain integrity invariant.
- **What tripped:** §11.5 requires every training example's provenance to survive into the training manifest; no gate refused an empty `provenance_ref` at manifest-row append time.
- **Protected objective:** ensures no training example enters the manifest without a traceable provenance-ref chain back to its acquisition receipt.
- **Additive fix:** `TrainingManifestExampleRow_v1.provenance_ref: str` (frozen · non-empty enforced) + `TrainingManifest_v1.append_row` raises `TrainingExampleWithoutProvenanceRefRefused_v1` on empty ref. Test: `test_training_manifest_refuses_row_without_provenance_ref_11_5` GREEN.
- **Receipt anchor:** `training_run_boundary_v1.py TrainingManifest_v1.append_row`.

### 5. §11.5 P187 rights-lapse-enumerable-model-ids (frozenset-return contract)

- **Kind:** enumerability contract invariant.
- **What tripped:** §11.5 P187 requires that when rights lapse on any training example, the affected model set is enumerable; nothing in code bound the return type as an enumerable-not-policed frozenset.
- **Protected objective:** ensures rights-lapse events yield a definite, non-mutable, iterable set of model ids for downstream retirement/take-down decisions.
- **Additive fix:** `RightsLapseDetector_v1.enumerate_affected_model_ids(...) -> frozenset[str]`; test asserts return type == `frozenset` and elements are all `str`. Test: `test_rights_lapse_yields_enumerable_affected_model_ids_11_5` GREEN.
- **Receipt anchor:** `training_run_boundary_v1.py RightsLapseDetector_v1`.

### 6. Ruling (b) AKKI-RUNS-IT · pod-never-data-path structural refusal (owner verbatim 2026-02-23)

- **Kind:** custody-boundary structural refusal + Census-Autonomy-Service registration seam.
- **What tripped:** owner Ruling (b) verbatim: "E1's pod is never the training host and never a data path." Prior to this-seal, no code path structurally refused `pod://` / `/app/` prefixed refs at the training-run registration boundary.
- **Protected objective:** ensures training compute + model weights + labelled corpus never traverse E1's pod at any registration point; every job runs inside the live Akki OS via the Census Autonomy Service.
- **Additive fix:** `TrainingRunCensusAutonomyRegistration_v1` frozen 4-field dataclass (`data_source_adapter_ref`, `engine_response_queue_ref`, `training_manifest_ref`, `completion_certificate_return_ref`); `register_training_run_as_census_autonomy_job` raises `PodAsDataPathAtRegistrationError` / `PodAsTrainingHostAtRegistrationError` on any ref starting with `pod://` or `/app/`. `POD_IS_NEVER_DATA_PATH_POSTURE` Final marker present. Test: `test_training_run_census_autonomy_registration_pod_never_data_path_ruling_b` GREEN.
- **Receipt anchor:** `training_run_boundary_v1.py register_training_run_as_census_autonomy_job` + `STATE/OWNER_DROPS/ruling_b_akki_runs_it_plus_standing_directives_20260223/DROP.md`.

### 7. §1.2 no-redeclaration of sealed symbols (redeclaration-guard invariant)

- **Kind:** sealed-carrier redeclaration guard.
- **What tripped:** §1.2 modality-extension forbids redeclaration of sealed symbols; the added module needed a redeclaration-guard invariant to protect sealed CP-AIP-4/7/8/9 + CP-M6-7-3 carriers from accidental shadowing.
- **Protected objective:** ensures new additive modules compose sealed symbols by import, never redeclare them.
- **Additive fix:** `test_no_redeclaration_of_sealed_symbols_1_2` scans `training_run_boundary_v1.py` AST and asserts no class/function definitions match names of sealed carriers (`CostQuoteWithCI`, `PlannerBoundaryResult_v1`, `SamplingReflectionBoundaryResult_v1`, `PlanWithoutCalibrationAtSRBoundary`, `HONEST_GAP_V1_POSTURE`, etc.). Test: GREEN.
- **Receipt anchor:** `test_cp_aip_10_training_runs_aip_v1_0_section_11_6_and_11_5.py::test_no_redeclaration_of_sealed_symbols_1_2`.

### 8. §1.4 + §11.6 heavy-fine-tune-deferred-posture marker (measured-cost-receipt discipline)

- **Kind:** measure-don't-assert posture marker.
- **What tripped:** §1.4 requires measured-cost-receipt discipline; §11.6 heavy fine-tune runs cannot execute in E1's pod (Ruling (b)); nothing structurally banked the deferred-to-commissioned-job posture.
- **Protected objective:** ensures a compaction-safe posture marker is present at the boundary so any successor session can measure the deferral policy without inference.
- **Additive fix:** `HEAVY_FINETUNE_DEFERRED_TO_COMMISSIONED_JOB_POSTURE: Final[str]` = verbatim §11.6 + §1.4 text. Test: `test_heavy_fine_tune_deferred_to_commissioned_job_posture_marker_present_11_6_1_4` GREEN.
- **Receipt anchor:** `training_run_boundary_v1.py HEAVY_FINETUNE_DEFERRED_TO_COMMISSIONED_JOB_POSTURE`.

### Seal-boundary summary

- **8 gaps closed** additively at CP-AIP-10 boundary — all 8 as RED-first invariant seats with authentic ImportError pre-authorship + GREEN post-authorship + double-green byte-identical stripped_sha256 across sweeps.
- **0 honest-gaps opened** at this boundary (heavy-fine-tune deferral is a posture marker, not an honest-gap — the code path is refused structurally, not deferred with residual).
- **Sealed carriers untouched** — additive-only per SO §3.8: CP-AIP-1..9 modules + CP-M6-7-3 CostQuoteWithCI + CP-AIP-4 pretraining_contract_v1 unchanged.
- **Ratchet:** `6313` → `6321` (+8 canonical measured) · baseline_failures.json sha256 post-bump `0c7968cdf19694f301e67dc28fee7180e693b0e1f7053fbd3e8226fef5490abd` · double-green stripped_sha256 `92d09b7d7f27897fdc7827bbcde23f584cdcb46c3f8be56f4cb23e150ecc7378`.
- **Continuity:** code bundle sha256 `48b2c169e5d04985f1754ff17d9ca0ce9688bd9c6067ba1dc9ca1252c7b08a41` @ `programme/track-a` `8ef25c1` (state bundle pin pending post-Commit-C-fixup).

---

## Seal boundary: CP-SO-6.9-LID-WAVE (2026-02-23T~12:30Z · Item 5.11.a · SO §6.9 LID RATIFICATION verbatim §1-§9)

### 1. Whisper-LID (MIT) registration act shape structural invariant

- **Kind:** invariant seat (RED-first pin at boundary).
- **What tripped:** SO §6.9 LID RATIFICATION §4 verbatim requires a 6-field registration act shape for every LID model registered; Whisper-LID has no on-disk representation of this before the seal.
- **Protected objective:** ensures the audio-provenance-and-licence traceability of every-segment LID label survives without a token-presentation hazard.
- **Additive fix:** `LidModelRegistration_v1` frozen dataclass with 6 verbatim fields; `WHISPER_LID_REGISTRATION` Final constant carries `licence_id="MIT"`. Test: `test_whisper_lid_registration_act_shape_MIT_licence_pinned_so_6_9_lid` GREEN.
- **Receipt anchor:** `phase0/cp_so_6_9_lid_wave_20260223/receipt.md §3`.

### 2. VoxLingua107 (Apache-2.0) registration act shape structural invariant

- **Kind:** invariant seat (RED-first pin at boundary).
- **What tripped:** SO §6.9 LID RATIFICATION §4 verbatim requires the same 6-field shape for VoxLingua107; no on-disk registration.
- **Protected objective:** ensures audio-native corroboration of Whisper-LID under a licence needing no review, before any regime flip.
- **Additive fix:** `VOXLINGUA107_REGISTRATION` Final constant carries `licence_id="Apache-2.0"`. Test: `test_voxlingua107_registration_act_shape_apache_2_0_licence_pinned_so_6_9_lid` GREEN.
- **Receipt anchor:** `lid_wave_overlay_and_admission_v1.py VOXLINGUA107_REGISTRATION`.

### 3. OverlayLidDetection marker/label structural invariant (B5.4 shown-not-counted)

- **Kind:** shape-invariant seat + refusal path.
- **What tripped:** SO §6.9 LID RATIFICATION §5 + B5.4 require `marker="INFERRED"` iff `label is not None`; no code path enforced this bidirectionally.
- **Protected objective:** ensures overlay labels are shown, never counted as a measure until admission-gate promotion.
- **Additive fix:** `OverlayLidDetection_v1.__post_init__` raises `LidLabelBelowConfidenceMustBeUnmeasuredError` when invariant violated. Test: `test_overlay_lid_detection_marker_INFERRED_when_label_set_unmeasured_when_none_b5_4` GREEN.
- **Receipt anchor:** `lid_wave_overlay_and_admission_v1.py OverlayLidDetection_v1`.

### 4. OverlayLidDetection regime default `pre-admission` invariant

- **Kind:** shape-invariant seat + refusal path.
- **What tripped:** direct construction of `regime="post-admission"` would let overlay bypass the receipted-act promotion path.
- **Protected objective:** ensures the shown-not-counted line is not crossed by construction; only a receipted act flips regime.
- **Additive fix:** `OverlayLidDetection_v1.__post_init__` raises `LidOverlayMustNotFlowIntoCountedMeasureError` on direct `post-admission` construction. Test: `test_overlay_lid_detection_regime_starts_pre_admission_default_so_6_9` GREEN.
- **Receipt anchor:** same.

### 5. LID_DO_NOT_FLOW_INTO_COUNTED_MEASURE_POSTURE Final marker (B5.4)

- **Kind:** compaction-safe posture marker.
- **What tripped:** B5.4 line was not banked as a compaction-safe posture; a successor session could miss the shown-not-counted contract.
- **Protected objective:** ensures a successor re-anchors the shown-not-counted contract from module source without inference.
- **Additive fix:** `LID_DO_NOT_FLOW_INTO_COUNTED_MEASURE_POSTURE: Final[str]` verbatim B5.4 line. Test: `test_lid_do_not_flow_into_counted_measure_posture_marker_present_b5_4` GREEN.

### 6. Admission gate DEFAULT_THRESHOLD_PENDING = 0.90 tagged pending

- **Kind:** shape-invariant seat.
- **What tripped:** SO §6.9 LID RATIFICATION §6 pins DEFAULT threshold ≥ 90% tagged pending; no code path fixed the DEFAULT.
- **Protected objective:** ensures single-model overreach cannot enter measure until tenant-labelled agreement clears the DEFAULT bar (with `pending` tag so owner may retune).
- **Additive fix:** `LidAdmissionGate_v1.DEFAULT_THRESHOLD_PENDING: ClassVar[float] = 0.90`; gate evaluation records `gate_status="pending"` until owner retunes. Test: `test_admission_gate_default_threshold_is_0_90_pending_so_6_9_lid` GREEN.

### 7. Regime promotion requires owner receipted act (canon 8 §4 W2)

- **Kind:** refusal-path invariant seat.
- **What tripped:** canon 8 §4 W2 requires promotion be a receipted act with owner signature; no code path enforced this at the boundary.
- **Protected objective:** ensures no LID label promotes to measured without owner receipt; historic overlays remain byte-identical.
- **Additive fix:** `promote_lid_regime_by_receipted_act` raises `LidRegimePromotionRequiresOwnerReceiptedActError` when `owner_signature_ref` empty or `previous_regime == new_regime`. Test: `test_lid_regime_promotion_requires_owner_receipted_act_canon_8_4_W2` GREEN.

### 8. LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE Final marker + frozen dataclass guarantee

- **Kind:** compaction-safe posture marker + structural guarantee.
- **What tripped:** SO §6.9 LID RATIFICATION §5-§6 mandate "nothing is ever relabelled at regime flip"; no compaction-safe marker banked.
- **Protected objective:** ensures historic overlay detections remain byte-identical when regime flips; future overlays get new regime.
- **Additive fix:** `LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE: Final[str]` + `OverlayLidDetection_v1` frozen dataclass guarantees mutation is impossible. Test: `test_lid_nothing_relabelled_at_regime_flip_posture_marker_present_so_6_9` GREEN.

### 9. HF pull wrapper anti-token structural guarantee (SO §6.9 clause 3)

- **Kind:** hazard-scope refusal + env-scrub invariant.
- **What tripped:** SO §6.9 clause 3 verbatim requires no `Authorization`/`token=` header ever attached and env scrubbed of `HF_TOKEN` / `HUGGINGFACEHUB_API_TOKEN` / `HUGGING_FACE_HUB_TOKEN` before pull; no wrapper enforced this structurally.
- **Protected objective:** ensures HF hazard scope stays "presentation of the leaked credential", not the host; public unauthenticated weight pull proceeds while token-presentation is structurally impossible for this call.
- **Additive fix:** `HuggingFacePullWrapperAntiToken_v1.build_headers()` returns only User-Agent + Accept; post-build guard refuses any bearer-like key defensively via `TokenPresentedInPullError`; `scrub_env()` classmethod pops the three HF token env vars. Test: `test_hf_pull_wrapper_build_headers_has_no_bearer_like_key_so_6_9_clause_3` GREEN.

### 10. TENANT-LABELS-PENDING honest-gap for English/Sheng/code-switched + 12 languages RESOLVED via google-transcripts/

- **Kind:** honest-gap seat + resolution seat.
- **What tripped:** SO §6.9 LID RATIFICATION §5-§6 + owner amendment naming 12 languages as RESOLVED via `google-transcripts/` — code had neither the residual honest-gap seat nor the resolved-set seat.
- **Protected objective:** enables function-progression (admission gate builds and evaluates against 12 resolved languages) while naming the residual gap (English/Sheng/code-switched) rather than papering over it.
- **Additive fix:** `TENANT_LABELS_PENDING_HONEST_GAP: Final = TenantLabelsPendingHonestGap_v1(languages=frozenset({"English","Sheng","code-switched"}))` + `LID_TENANT_LABELS_RESOLVED_12_LANGUAGES: Final[frozenset[str]] = frozenset({"kik","ebu","swa","luo","kln","guz","mer","bxk","kam","mrg","lwg","mas"})`. Test: `test_tenant_labels_pending_honest_gap_english_sheng_code_switched_so_6_9_lid_ratification` GREEN.
- **Honest-gap status at boundary:** RETAINED for English/Sheng/code-switched (3 languages · residual per SO §6.9 LID RATIFICATION verbatim); RESOLVED for kik/ebu/swa/luo/kln/guz/mer/bxk/kam/mrg/lwg/mas (12 languages).

### 11. §1.2 no-redeclaration of sealed CP-M6-1-1 symbols

- **Kind:** sealed-carrier redeclaration guard.
- **What tripped:** §1.2 forbids redeclaration of sealed symbols; without an AST-level scan, an accidental shadow of `LanguageIDBackend` / `UnratifiedInferredBackend` / `LanguageIDResult` / `AudioSegment` could not be caught.
- **Protected objective:** ensures the LID-wave module composes CP-M6-1-1 by import only, never redeclares.
- **Additive fix:** `test_no_redeclaration_of_sealed_symbols_1_2_so_6_9_lid` scans module AST for class/function names in the forbidden set. Test: GREEN.

### Rejected options bookkeeping (per owner drop §7 verbatim)

- **fastText LID.176** → `WAITING-ON-TRANSCRIPTS` — parked, NOT registered. Reason: labels text not audio + needs unregistered transcription model.
- **Silero language classifier** → `LICENCE-REVIEW-REQUIRED C5.4` — parked, NOT registered. Reason: licence must be verified commercial before it can run (C5.4).

### Seal-boundary summary

- **11 gaps closed** additively at CP-SO-6.9-LID-WAVE boundary — all 11 as RED-first invariant seats with authentic ImportError pre-authorship + GREEN post-authorship + double-green byte-identical stripped_sha256 across sweeps.
- **1 honest-gap RETAINED** at this boundary (`TENANT-LABELS-PENDING` for English/Sheng/code-switched · residual per SO §6.9 LID RATIFICATION verbatim).
- **12 languages RESOLVED** via `google-transcripts/` corpus (kik/ebu/swa/luo/kln/guz/mer/bxk/kam/mrg/lwg/mas).
- **2 rejected options recorded** (fastText LID.176 → WAITING-ON-TRANSCRIPTS · Silero → LICENCE-REVIEW-REQUIRED C5.4).
- **Sealed carriers untouched** — additive-only per SO §3.8: CP-M6-1-1 `language_identifier.py` unchanged.
- **Ratchet:** `6321` → `6332` (+11 canonical measured) · baseline_failures.json sha256 post-bump `468340729cd16eb9f544453f4d18e33a6069cce79b1ec3aa638975daa20ce314` · double-green stripped_sha256 `b71bead1574966208bf999b2f59477324c7f0c8c20381ce98d6ecccc2240650a`.
- **Continuity:** code bundle sha256 `c312d8cfcf611f59e8d3008df7be5cc27569d867931b1837dfe43ffb4def193f` @ `programme/track-a` `d4eae498` (state bundle pin pending post-Commit-C-fixup).

---

## Seal boundary: CP-ENT-16-PILOT-LICENCE-SEEDS (2026-02-23T~13:15Z · Item 5.11.b · SO §6.9 amendment §6 verbatim)

### 1-6. Pilot licence seed structural invariants (RED-first pins)

- **Kind:** invariant seats · 6 pins on frozen dataclass shape + 3 tenant seed constants + tuple + boundary refusal.
- **What tripped:** SO §6.9 amendment §6 verbatim requires pilot licence object at tenant creation for RMS + DigiCow + AKKI-TEST with `Compute dial Managed` + `Frontier dial Your Keys`; no on-disk representation before this seal.
- **Protected objective:** ensures every model call resolves from day 1 (ENT-16 chokepoint has a resolvable licence for every seeded tenant).
- **Additive fix:** `PilotLicenceSeed_v1` frozen 4-field dataclass + `RMS/DIGICOW/AKKI_TEST_PILOT_LICENCE_SEED` Final constants + `THREE_TENANT_PILOT_LICENCE_SEEDS` tuple + `create_tenant_with_pilot_licence_seed` boundary refuses without seed. Tests GREEN.
- **Receipt anchor:** `phase0/cp_ent_16_pilot_licence_seeds_20260223/receipt.md §3`.

### 7. EVERY_MODEL_CALL_RESOLVES_FROM_DAY_1_POSTURE Final marker

- **Kind:** compaction-safe posture marker.
- **Additive fix:** `EVERY_MODEL_CALL_RESOLVES_FROM_DAY_1_POSTURE: Final[str]` verbatim SO §6.9 amendment §6 line.

### 8. §1.2 no-redeclaration of sealed CP-ENTITLEMENT-BUILD-WAVE symbols

- **Kind:** sealed-carrier redeclaration guard.
- **Additive fix:** AST scan test rejects `PrincipalV1`, `PrincipalKind`, `resolve`, `ResolutionRefusal` shadow.

### 9. Fold-in orthogonal gap-closure: CP-SO-6.9-LID-WAVE card_sha256 placeholder

- **Kind:** SO §6.2 hash-pin drift (discovered during CP-ENT-16 sweep pre-authorship).
- **What tripped:** CP-SO-6.9-LID-WAVE card_sha256 was `<computed_at_promote>` placeholder post-State-B; `test_every_card_hash_pin_matches_body` invariant would have failed at any post-State-B sweep.
- **Protected objective:** ensures every card in `STATE/OBJECTIVES/` has valid computed hash-pin per SO §6.2.
- **Additive fix:** computed `card_sha256 = 1f5712e33dde1c044f1a06e5ccadf0ce20639a3eba67e274a41054ee70fab8ee` and pinned at pre-CP-ENT-16 sweep boundary.
- **Lesson banked:** pin card_sha256 at promotion (before any sweep runs post-State-B), not as post-hoc computation.

### Seal-boundary summary

- **8 gaps closed** additively at CP-ENT-16 boundary (all RED-first with authentic ImportError → GREEN → double-green byte-identical).
- **1 orthogonal gap closed** at same boundary (CP-SO-6.9-LID-WAVE card_sha256 pin).
- **Sealed carriers untouched** — additive-only per SO §3.8.
- **Ratchet:** `6332` → `6340` · baseline_failures.json sha256 `129abd82ae739afb459a939d20f38c22d45eae27244339b3b56446b65d3f625c` · double-green stripped_sha256 `1d5895556ccc3c5c80ad25b3d511ed8563d191fa62c570bc43cf7753425ed3f5`.
- **Continuity:** code bundle sha256 `8ab58aa418413a08e8b37dc2492dca70e99cadab0e0ad815f0552a59d5ed186f` @ `programme/track-a` `9e3ca45a` (state bundle pin pending).

---

## CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY · Item 5.11.c · SEALED 2026-02-23T~14:05:00Z

**Owner anchor (SO §6.9 amendment §6 item 8 verbatim):** *"The census proceeds in its three waves — complete the walk with the unmeasured register, the full B3 dimension set with the defensibility matrix and sensitivity classification, then the perception pathway — and language labels from item 4 enter it as overlay from the first run."*

### 10. Three-wave ordered tuple with LID overlay from first run

- **Kind:** invariant seat — SO §6.9 amendment §6 item 8 verbatim binding as ordered 3-tuple `("unmeasured_register", "b3_dimension_set", "perception_pathway")` with LID overlay entering at Wave 3.
- **Protected objective:** the census walk executes in owner-verbatim order; overlay labels enter only through sealed CP-SO-6.9-LID-WAVE registrations.
- **Additive fix:** `CENSUS_THREE_WAVES` Final tuple + `UnmeasuredRegisterWave_v1` (frozen · `dimensions_measured=False` per B5.4 shown-not-counted) + `B3DimensionSetWave_v1` (frozen · `defensibility_matrix_rule_ref` + `sensitivity_class` + 3 B3 dims) + `PerceptionPathwayWave_v1` (frozen · `lid_overlay_source_registration` + `lid_overlay_marker` Literal `INFERRED`/`unmeasured`).

### 11. Wave-out-of-order refused at boundary

- **Kind:** structural sequencing enforcement.
- **What would trip:** opening Wave N with `prior_wave_completed != CENSUS_THREE_WAVES[N-1]`.
- **Protected objective:** the walk cannot skip a wave; a missed Wave 1 cannot proceed to Wave 2/3 (the census "proceeds in its three waves" verbatim).
- **Additive fix:** `open_wave(name, prior_wave_completed)` raises `CensusWaveOutOfOrderError` when the prior-wave contract is violated.

### 12. Unknown wave name refused

- **Kind:** Literal-closed 3-tuple set-membership guard.
- **Additive fix:** `open_wave` raises `CensusWaveNameRefused` when `name not in CENSUS_THREE_WAVES`.

### 13. LID overlay from first run: only sealed registrations accepted

- **Kind:** identity-check against sealed singletons.
- **What would trip:** a shape-equivalent fabricated `LidModelRegistration_v1` passed as overlay source.
- **Protected objective:** SO §6.9 LID RATIFICATION verbatim — only Whisper-LID (MIT) or VoxLingua107 (Apache-2.0) sealed registration singletons carry the overlay; fabricated shapes never enter.
- **Additive fix:** `lid_overlay_source_is_sealed_registration(source)` uses `is`-identity against `WHISPER_LID_REGISTRATION` / `VOXLINGUA107_REGISTRATION`.

### 14. LID overlay marker structural preservation

- **Kind:** B5.4 shown-not-counted line preserved by construction.
- **Additive fix:** `PerceptionPathwayWave_v1.lid_overlay_marker` typed `Literal["INFERRED", "unmeasured"]` — no `post-admission` label constructible at Wave 3 exit; regime promotion is a receipted act landed in the sealed LID module.

### 15. Ruling (b) AKKI-RUNS-IT verbatim at registration seam

- **Kind:** pod-never-data-path structural refusal at seam.
- **What would trip:** `engine_response_queue_ref` or `data_source_adapter_ref` starting with `pod://*` or `/app/*`.
- **Protected objective:** E1 wires the seam INTO Census Autonomy Service; pod is never data path (owner Ruling (b) verbatim 2026-02-23).
- **Additive fix:** `register_census_three_waves_as_census_autonomy_job(engine_response_queue_ref, data_source_adapter_ref)` raises `PodIsNeverDataPathError` on either forbidden prefix.

### 16. LID_OVERLAY_ENTERS_FROM_FIRST_RUN_POSTURE Final marker

- **Kind:** posture-marker string presence guarantee (SO §2.5 verbatim-anchor pattern).
- **Additive fix:** `LID_OVERLAY_ENTERS_FROM_FIRST_RUN_POSTURE` Final str carries SO §6.9 amendment §6 item 8 verbatim.

### 17. §1.2 no-redeclaration of sealed CP-SO-6.9-LID-WAVE symbols

- **Kind:** sealed-carrier redeclaration guard.
- **Additive fix:** AST scan test rejects `LidModelRegistration_v1`, `OverlayLidDetection_v1`, `WHISPER_LID_REGISTRATION`, `VOXLINGUA107_REGISTRATION`, `CharacterRegister`, `CharacterEntry` shadow.

### 18. UnmeasuredRegisterWave_v1 dimensions_measured=False (B5.4)

- **Kind:** B5.4 shown-not-counted enforcement.
- **Protected objective:** the unmeasured register does not seed downstream counted measures; only Wave 2's B3-dim measurement + defensibility class can.
- **Additive fix:** `UnmeasuredRegisterWave_v1` frozen with `dimensions_measured: bool` field pinned False at Wave 1 construction.

### 19. B3DimensionSetWave_v1 defensibility matrix + sensitivity carrier

- **Kind:** owner-verbatim required-fields on Wave 2 frozen carrier.
- **Additive fix:** `B3DimensionSetWave_v1` frozen with required fields `b3_attachment_markedness` + `b3_genre_form` + `b3_corroboration` + `defensibility_matrix_rule_ref` + `sensitivity_class` — matches Canon 4 §5.1 (detection layer + verdict layer) + Canon 7 §3 (sensitivity conservative default).

### Seal-boundary summary

- **10 gaps closed** additively at CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY boundary (all RED-first with authentic ImportError → GREEN → double-green byte-identical).
- **Sealed carriers untouched** — additive-only per SO §3.8 (CP-SO-6.9-LID-WAVE lid_wave_overlay_and_admission_v1.py unchanged).
- **Ratchet:** `6340` → `6350` · baseline_failures.json sha256 `e7eb57d0ba2b213b2f9b4361c6a45a6d51e39b07bbd94139314741dfaac80998` · double-green stripped_sha256 `c10b70efc5ab8c6086e83f3fb2f862bdb61ece2977bfee3684d882239c35ca88`.

