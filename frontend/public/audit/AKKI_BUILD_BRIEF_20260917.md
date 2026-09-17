# AKKI BUILD BRIEF — 2026-09-17

> **Read-only status brief for the owner.** Every factual item below carries a label:
> **[VERIFIED]** — checked on disk / git this session, or **[BANKED/UNVERIFIED]** — cited from a banked note without re-firing the underlying operation this turn.
> Credentials are referenced by filename / location only. **No secret values appear anywhere in this brief.**

Report generated: 2026-09-17 · Author: E1 (session assistant) · Anchor: STATE/STANDING_ORDERS.md.

---

## 1 · What we are building

Akki is a **governed custody & intelligence platform** for a regulated data estate (voice / audio recordings, transcripts, attribute bundles, embeddings, derivative products) whose primary owner is the enterprise it serves. The product exists so that this estate can be **used** for training, decisioning and reporting **without ever leaving custody**, without leaking biometric or named-person material, and without silent regulatory drift.

**[VERIFIED — canon/text/]** Nine canon documents anchor the product vision:

| # | Canon | Local text file | Bytes |
|---|---|---|---|
| 1 | The Custody Platform | `canon/text/Akki_Canon_1_Custody_Platform.txt` | 30 842 |
| 2 | The Conditioned Ideation Faculty (CIF) | `canon/text/Akki_Canon_2_CIF.txt` | 18 812 |
| 3 | Governance Engines | `canon/text/Akki_Canon_3_Governance_Engines.txt` | 37 546 |
| 4 | Operating Engines | `canon/text/Akki_Canon_4_Operating_Engines.txt` | 63 661 |
| 5 | Interface Architecture | `canon/text/Akki_Canon_5_Interface_Architecture.txt` | 49 421 |
| 6 | User Journeys | `canon/text/Akki_Canon_6_User_Journeys.txt` | 18 689 |
| 7 | Integration & Quality Rulebook | `canon/text/Akki_Canon_7_Integration_and_Quality.txt` | 49 279 |
| 8 | The Watch | `canon/text/Akki_Canon_8_The_Watch.txt` | 36 046 |
| 9 | The Mkondo Charter | `canon/text/Akki_Canon_9_Mkondo_Charter.txt` | 8 982 |

**Governed-census / audio-intelligence-plane framing.** The current active build stream (see `canon/text/Akki_OS_Audio_Intelligence_Plane_Specification_v1_0.txt`, 28 989 B) instantiates the canon on the audio estate: a *governed census* enumerates what audio the enterprise owns, an *intelligence plane* condenses it into derivative products (transcripts, attributes, calibrated cluster registries, deliverables), and a *release gate* refuses any product that crosses a governance line — biometric material, named identities, raw-audio transfer — unless an explicit owner ruling has admitted it.

**Core value in plain language.** Rather than exporting recordings to external ML systems, the enterprise runs a **custody-first pipeline** in-place: raw audio never leaves; only owner-ratified derivative products (e.g. transcript triples, tokenised named-persons, discriminated-kind embeddings) can be lifted, and every lift is bound by a preventive-charter that records/alerts on any dispatch to an unregistered resource. This lets the estate participate in training, audit, and reporting workflows while remaining compliant-under-pilot.

---

## 2 · How it works — architecture in service planes

**[VERIFIED — repos/Extraction-Akki/backend/services/]** The kernel is a **thin FastAPI backend** organised as ~90 service sub-trees under `backend/services/`. Session inventory of the currently active planes:

### 2.1 Governance plane — `services/governance_plane/`
Four modules **[VERIFIED — ls]**:
- `cross_service_binding.py` — CP-M8-CSD-1 preventive-charter (record + alert on dispatch-to-unregistered-resource; allow-during-pilot; upgrade path to hard-gate preserved by construction).
- `cross_table_consistency.py` — CP-M8-CTCC-1 sibling (coarse set-membership drift check across governance tables).
- `retention_policy.py` — retention rule fabric.
- `__init__.py`.

### 2.2 Audio intelligence plane — `services/audio_plane_v1/`
The census + condensation core. Modules visible on disk **[VERIFIED]** include: `audio_census_job_scope.py`, `backend_registry.py`, `calibration.py`, `channel_condition_profiler.py`, `character_register.py`, `cluster_stability.py`, `clustering.py`, `code_switch_detector.py`, `collection_schema.py`, `commission_registry_namespace.py`, `commission_view.py`, `corpus_deliverable_v1.py` (Path C — pointer-only triples), `corpus_deliverable_v1_derivative.py` (Path B — derivative segments, shape β 6-carrier discriminator), `dedup_path.py`, `human_validation.py`, `instance_condition_map.py`, `language_identifier.py`, `leakage_path_harness.py` (…and more).

### 2.3 Release gate — `services/release_gate/`
Three modules **[VERIFIED]**:
- `release_ledger.py` — release records.
- `ruling_5_tier_lift.py` — CP-M7-W8-LIFT-1, Ruling #5 tier-lift admissibility carrier.
- `__init__.py`.

### 2.4 Other kernel sub-trees present on disk **[VERIFIED — ls]**
`agent_containment/`, `approvals/`, `artifact_store/` (with `atomic_write.py` and `orphan_scan.py`), `attribute_stream_bundle/`, `audio_poc/`, `audit_trail/`, `auth/`, `baseline_line/`, `business_continuity/`, `campaign_infra/`, `canonical_projection/`, `capability_registry.py`, `census_canon/`, `census_dimensions/`, `census_engine/`, `chat/`, `checker/`, `chokepoint/`, `compliance/`, `compute_estate/`, `compute_seam/`, `connect/`, `connect_estate/`, `contract_shells/`, `cost_ledger/`, `credentials_paste/`, `critic_pass/`, `d12_poc/`, `dap/`, `data_source/`, `data_suite_v2/`, `de_identify/`, `declaration/`, `doc0_attributes/`, `economics/`, `estate_keys/`, `evidence_register/`, `g1_defensibility/`, `governance/`, `grey_mirror/`, `handoff/`, `health/`, `ip_allowlist/` (with `middleware.py`), `journey_assistant/`, `layer_a|b|c/`, `lowered_standard/`, `master_admin/`, `memory/`, `model_admission/`, `model_recheck/`, `model_registry/`, `mtafiti/`, `multi_instance/`, `n_series/`, `northena/`, `opportunity_briefs/`, `orchestrator_resilience/`, `outer_gate/`, `output_verified_seal/`, `perception/`, `registry/`, `registry_facts/`, `reliable_time_source/`, `resource_registry/`, `response_sanitizer/`, `retention/`, `rights_quarantine/`, `rules_service/`, `rulings/`, `secret_hygiene/`, `service_1/`, `serving_floor/`, `shield_train/`, `skill_files/`, `solva/`, `solva_depth/`, `solva_v2/`, `source_plane/`, `synisense/`, `system_state.py`, `targeta/`, `team/`, `trace/`, `training/`, `training_runner/`, `transform_forms/`, `use_data/`, `v1_harness/`, `v2_gate/`, `v3_harness/`, `w_registry_full_build/`, `watch/`, `whitepapers/`, `wizard/`, `work_supervisor/`, `wpw/`.

### 2.5 Key mechanisms (banked patterns applied throughout)

- **Reference-not-copy data model.** All refusal wrappers carry `*_ref: str` (e.g. `deliverable_id`, `retention_policy_ref`, `surface_id`) rather than nested payloads; caller-side composition. Zero closed enums; case-agnostic (2026-09-13 owner correction). This keeps the platform contract-agnostic to future canon rulings.
- **Preventive-charter refusal.** Modules do not hard-gate at runtime; they define pure `assess_*_drift` functions plus `assert_*` refusal wrappers. The caller decides when to invoke; the invocation refuses with COUNTS-only messages (never carrying identifying values). Upgrade path to hard-gate is preserved by construction.
- **Zero-domain-token grep-negative.** Every new mechanism must pass a 21-token grep-negative test (no `voiceprint`, no `embedding`, no `biometric_*`, etc. inside the module source) — a lexical proof that the module is genuinely case-agnostic.
- **IP allowlisting.** `services/ip_allowlist/middleware.py` gates ingress by allowlist; complements JUMP/bastion IP-set discipline for cluster access. **[VERIFIED — module present.]**
- **Artifact store on JSON files.** `services/artifact_store/atomic_write.py` + `orphan_scan.py` implement the durable persistence layer as **atomic JSON writes** with orphan reconciliation — no database dependency on the hot path. **[VERIFIED — modules present.]**
- **Baseline-guarded pytest invariants.** The full contract is expressed as ~4433 pytest invariants under `tests/invariants/` (544 test files) with a monotonic passed-floor ratchet. See §3.

---

## 3 · How much is already built

### 3.1 Test suite scale **[VERIFIED — pytest ran this session]**
```
$ cd repos/Extraction-Akki/backend
$ BASELINE_GUARD=1 python -m pytest tests/invariants/ -q
… 4433 passed, 1 skipped, 438 warnings in 132.94s (0:02:12)
```
- **Invariant test files:** 544 **[VERIFIED — ls | wc -l]**
- **Passing invariants floor (ratchet):** 4433 **[VERIFIED — `tests/invariants/baseline_failures.json`]**
- **Skipped (legacy conditional):** 1 (bounded by `total_skipped_max: 1`)
- **Failures baseline:** empty list — every failure must be zero.

### 3.2 Ratchet history **[VERIFIED — 181 entries]**
- First entry: `20260827T075209Z · commit 18748a3 · CP-D1a (partial close) · passed 1932`.
- Latest entry: `20260916T194400Z · commit PENDING · CP-M8-CSD-1 · passed 4433`.
- Growth: **+2 501 passing invariants** over 21 days across 181 ratchet steps; strictly monotonic non-decreasing.

### 3.3 Sealed checkpoints inventory **[VERIFIED — phase0/output_verified_seals/]**
- **63 seal files** on disk in `phase0/output_verified_seals/`.
- Breakdown by prefix (from the seal filename):
  - `cp_m6_*` — **28** M6 audio-intelligence-plane sub-wave seals (SW1..SW9 largely closed; SW-10 deferred by owner ruling).
  - `w_m7_*` — 5 M7 post/CP seals (`w_m7_w1_post_1_resource_registry`, `w_m7_w2_cp1_audio_census_job_scope`, `w_m7_w8_lift_1_ruling_5_tier_lift`, plus in-flight companions).
  - `w_m8_*` — 2 M8 catch-all seals (`w_m8_ctcc_1_cross_table_consistency`, `w_m8_csd_1_cross_service_binding`).
  - `wdap_2a..2f` — 6 DAP-stage seals.
  - `audio_poc_v1`, `census_canon_align`, `cp_sw6_hyg_1_credential_metadata`, `data_suite_v2_lift`, `registry_extension_g3`, `solva_v2_lift`, `w_census_runtime_orchestration`, `w_data_suite_analyze_workspace_deep_dive_real`, `w_export_artefact_render`, `wcensus_supplement`, `wd12_poc` — additional platform-lift seals.

### 3.4 Milestones & waves — completion posture **[VERIFIED where noted]**

| Milestone / Wave | Status | Evidence |
|---|---|---|
| M6 · Audio-intelligence plane build (SW1..SW10) | **9/10 SEALED + SW-10 DEFERRED** by owner ruling verbatim 2026-09-16T~03:08Z (SW-10 = training on estate audio) | `notes/M6_SEAL_20260916.md` (13 687 B), master commit `93fb95c7` `M6 SEAL LANDED` **[VERIFIED — git log]** |
| M7-W1-POST-1 · Resource registry | **SEALED** | Seal file `w_m7_w1_post_1_resource_registry.seal.txt` **[VERIFIED]** |
| M7-W2-CP1 · Audio-census job scope + ratification gate | **SEALED** | Seal file + `notes/M7_W2_CP1_SEAL_20260916.md` **[VERIFIED]** |
| M7-W8-LIFT-1 · Ruling #5 tier-lift admissibility carrier | **SEALED** (ratchet 4412→4419) | `services/release_gate/ruling_5_tier_lift.py`, commit `561cfce` **[VERIFIED — git log]** |
| M7-W9-CP1 · Path C default corpus deliverable | **SEALED** (4400→4406) | `services/audio_plane_v1/corpus_deliverable_v1.py`, commit `2e227dd` **[VERIFIED]** |
| M7-W9-UPGRADE-1 · Path B derivative corpus (shape β) | **SEALED** (4419→4426), master fixup `250b85a7` | `services/audio_plane_v1/corpus_deliverable_v1_derivative.py`, commit `cdf2312` **[VERIFIED]** |
| M8-CTCC-1 · Cross-table consistency preventive-charter | **SEALED** | `services/governance_plane/cross_table_consistency.py` **[VERIFIED]** |
| M8-CSD-1 · Cross-service dispatch preventive-charter (§3.2 clause 5 shape b) | **CODE + STATE LANDED (Commits A + B); Commit-C fixup UNCOMMITTED IN WORKING TREE** | Track-a HEAD `40b6ee0` + master HEAD `00b16232` **[VERIFIED — git log]**; dirty-tree diff for Commit-C fixup **[VERIFIED — git diff --stat]** |

### 3.5 Repository picture **[VERIFIED — git log per repo]**

| Repo | Default branch | Active branch here | HEAD SHA | HEAD date | HEAD subject |
|---|---|---|---|---|---|
| RMS-IQ-Core-2 | `main` | `main` | `ea5aa01` | 2026-08-01 | Auto-generated changes |
| Akki-OS-V1 | `main` | `main` | `8c36190` | 2026-08-14 | Auto-generated changes |
| Extraction-Akki | `main` | `programme/track-a` | `40b6ee0244375606550294aa5d08f81fb1b0b670` | 2026-09-16 | CP-M8-CSD-1 · §3.2 clause 5 shape (b) preventive-charter · `services/governance_plane/cross_service_binding.py` |
| Akki-Executive-Core | `main` | `main` | `5844eee9` | 2026-07-08 | Auto-generated changes |
| assessment_workspace | — | `master` | `00b1623243a060f83addbe3a3ed7fbbbe3ab5d3c` | 2026-09-16 | CP-M8-CSD-1 · SEALED (4433) · Commit-B |

Active build is on **Extraction-Akki@programme/track-a** (code) coupled with **assessment_workspace@master** (state, seals, notes, receipts). The other three repos are dormant reference sources at their pinned HEADs.

---

## 4 · How much remains

### 4.1 Uncommitted in the working tree right now **[VERIFIED — git status + git diff]**
The only paused artefact is the **CP-M8-CSD-1 §3.3 Commit-C fixup**. Five tracked files carry the fixup payload (banks master HEAD `00b16232` in place of `TBD`), one additional file (`notes/GOVERNED_CENSUS_HARVEST_PLATFORM_ROADMAP.md`) is coupled:
```
STATE/DECISIONS.md                                                    | 2 +-
STATE/NEXT.md                                                         | 2 +-
STATE/PINS.md                                                         | 2 +-
notes/M8_CSD_1_SEAL_20260916.md                                       | 4 ++--
phase0/output_verified_seals/w_m8_csd_1_cross_service_binding.seal.txt | 2 +-
```
Once committed, the M8-CSD-1 3-commit protocol closes cleanly. Owner has explicitly held commit authority.

### 4.2 Pre-declared §A walk — remaining slice
- **M8 SEAL wave-close report** (Slice #5 · LAST) — the M8 milestone close, with an inline **OVERALL BUILD STATUS** table for the owner. Not yet authored. **[VERIFIED — not in `notes/`.]**

### 4.3 Parked / deferred work **[BANKED from STATE/NEXT.md and RULING_LEDGER.md]**
- **M6-SW10** — full training runs on estate audio: **DEFERRED-TO-CLOSE** by owner ruling verbatim 2026-09-16T~03:08Z. Requires a fresh owner authorisation before it can be initiated.
- **WPW R1 / R2 / R3** — whitepaper-writer follow-ons; parked.
- **R-6 pricing** — commercial pricing carrier; parked.
- **SEC-2026-09-14-04 HF token rotation** — banked as **NOT-ROTATED** (file-rename only, byte-identical). Genuine rotation still outstanding.
- **OWNER-DROP-01 / F.1 Huawei 2nd AK/SK** — closed as *DOWNLOADED-BUT-BYTE-IDENTICAL* (2nd URL delivers a duplicate of the 1st file; not a genuinely-second AK/SK pair).

### 4.4 Blocked probes (waiting on external actor) **[BANKED — `notes/PROBE_REFIRE_STATUS_20260916.md`]**
- 1 PASS · 5 BLOCKED · 0 FAIL. See §6 for the full source-by-source table.

---

## 5 · Sources for reference (files this brief points to)

### 5.1 Canon documents — `canon/text/` **[VERIFIED]**
Nine canonical texts + audio-intelligence spec (see §1 table) + `Akki_OS_Audio_Intelligence_Plane_Specification_v1_0.txt` + `Akki_OS_Incremental_Training_Capacity_Briefing.txt` + `Akki_Training_Techniques_Spec.txt` + `Audio_Intelligence_Plane.md` + `Akki_Canon_Documents_17_19.txt`.

### 5.2 Repositories under `repos/` **[VERIFIED]**
- `RMS-IQ-Core-2` @ `main / ea5aa01` (2026-08-01).
- `Akki-OS-V1` @ `main / 8c36190` (2026-08-14).
- `Extraction-Akki` @ `programme/track-a / 40b6ee0` (2026-09-16). **Active build.**
- `Akki-Executive-Core` @ `main / 5844eee9` (2026-07-08).

### 5.3 Key STATE documents **[VERIFIED — STATE/]**
- `STATE/STANDING_ORDERS.md` (24 256 B) — permanent law. Sections: SESSION BOOT PROTOCOL · ENGAGEMENT DISCIPLINE · BUILD DISCIPLINE · RUNTIME LAW · GPU OBLIGATIONS · CURRENT AUTHORITATIVE ARTIFACTS.
- `STATE/DECISIONS.md` (1 257 303 B) — verbatim decision & ruling bank.
- `STATE/NEXT.md` (366 987 B) — CURRENT-block pointer for next slice.
- `STATE/PINS.md` (34 592 B) — pinned artefacts / commissioning-record.
- `STATE/HOLISTIC_PLAN.md` (42 752 B) — programme-wide plan.
- `STATE/CONTEXT.md` (58 843 B) — session context.
- `STATE/ORCHESTRATOR.md` (11 192 B) — orchestrator playbook.
- `STATE/SPRINT_PLAN.md` (27 856 B) — sprint scaffolding.
- `STATE/WPW_CHARTER.md` (14 747 B) — whitepaper-writer charter.

### 5.4 Owner rulings — key entries **[VERIFIED — notes/OWNER_RULING_A_BUNDLE_SHAPE_BETA_20260916.md and RULING_LEDGER.md]**

- **Ruling #5** (verbatim, banked master `a04c65a8` 2026-09-16T~17:43Z):
  > *"Ruling #5: kdpa = compliant-under-pilot, named-persons = tokenized, transfer-basis = derivative-only."*
  Anchored in `services/release_gate/ruling_5_tier_lift.py` (CP-M7-W8-LIFT-1) and required as a composed reference by every derivative-corpus deliverable.

- **§A Shape ruling — β** (verbatim, 2026-09-16T~19:22Z):
  > *"Shape ruling: β — the 6-carrier segment with `derivative_kind_ref: str` (open string, no closed enum) … case-agnostic pattern the 2026-09-13 correction mandates."*
  Anchored in `services/audio_plane_v1/corpus_deliverable_v1_derivative.py` (CP-M7-W9-UPGRADE-1).

- **§A §3.2 clause 5 — shape (b) PREVENTIVE-CHARTER RATIFIED** (verbatim):
  > *"§3.2 clause 5 = shape (b) PREVENTIVE-CHARTER RATIFIED: record + alert on dispatch-to-unregistered-resource, allow during pilot, upgrade path to hard-gate preserved as a future owner ruling."*
  Anchored in `services/governance_plane/cross_service_binding.py` (CP-M8-CSD-1).

- **F.1 correction / OWNER-DROP-01 refinement** (2026-09-16T~19:22Z, verbatim): 2nd Huawei CSV URL is real; download succeeded under §E discipline but byte-hash matches the 1st file (duplicate).

- **F.3 rotation ledger** (2026-09-16, verbatim): HF "rotation" being byte-identical means SEC-2026-09-14-04 remains **NOT-ROTATED**; carry.

- **Case-agnostic correction** (2026-09-13, standing law): all cross-module refs must be **OPEN str** with a 21-token domain-token grep-negative test; zero closed enums; caller-side composition only.

Additional owner-rulings live in `notes/RULING_LEDGER.md` (categories: RATIFIED / DEFAULT / COUPLED / OPEN) and are mirrored verbatim into `STATE/DECISIONS.md`.

### 5.5 Additional evidence artefacts **[VERIFIED]**
- Sealed CP inventory: `phase0/output_verified_seals/` (63 files).
- GPU 72-h campaign telemetry: `phase0/gpu_receipts/*.json` and `notes/GPU_UTILIZATION_72H.md` / `.json`.
- Commissioning stream: `phase0/commissioning_records/commissioning_aisca-gpu-01_*.json` (continuous samples).
- Cross-repo overlap notes: `notes/cross_repo_overlap.md` (banked from chunk-1 assessment).
- Prototype & canon-drop packs: `canon/prototypes/`, `canon/drops/`, `canon/fixtures/`.

---

## 6 · Estate & compute connection attempts

For each estate/compute source: what was attempted, what SUCCEEDED, what is BLOCKED and why, with governing note as evidence.

| Source | Attempt | Result | Governing note / receipt | Label |
|---|---|---|---|---|
| **Huawei OBS** (`obs.af-south-1.myhuaweicloud.com`, bucket `google-transcripts`) | Bounded-shape-only probe: `listObjects(bucket, max_keys=1)` under §E custody discipline (env-injected AK/SK; no cat/head/tail on custody file; sha-pinned shape metadata only). | **PASS** — status `200`, ≥1 object present; AK len `20` and SK len `40` reported as shape metadata only; **zero raw AK/SK bytes crossed stdout**; zero object keys crossed stdout. | `phase0/gpu_receipts/20260916T1912Z_huawei_obs_bounded_probe.json` + master commit `44743c8b` **[VERIFIED — git log]**. | **VERIFIED bounded-shape-only** (not re-fired this turn) |
| **Huawei OBS · 2nd CSV (F.1)** | Re-download of 2nd URL under §E discipline; sha-pin against 1st file. | **DOWNLOADED-BUT-BYTE-IDENTICAL** — file lands (119 B, 1 line), chmod 600 applied, sha256 = 1st file's sha256. Concludes: URL is real; 2nd artefact = duplicate of 1st. | `notes/OWNER_RULING_A_BUNDLE_SHAPE_BETA_20260916.md` §B. | **BANKED / VERIFIED** |
| **Synology NAS** | Connectivity probe planned; awaiting admin-supplied IP-set for the source. | **BLOCKED** on admin IP-set delivery. | `notes/PROBE_REFIRE_STATUS_20260916.md` + `notes/ADMIN_BINDS_20260915.md`. | **BANKED / UNVERIFIED** |
| **MySQL CD** (call-detail) | Connect from platform node planned. | **BLOCKED** on JUMP SEC-halt (bastion path in security hold). Also: "new MySQL endpoints not on-disk" — endpoint list not yet in workspace. | `notes/PROBE_REFIRE_STATUS_20260916.md` + `notes/DB_CONNECT_DECISION_POINT_20260913.md`. | **BANKED / UNVERIFIED** |
| **MySQL Visitors** | Same. | **BLOCKED** same as CD. | Same. | **BANKED / UNVERIFIED** |
| **Bastion / JUMP** | Rotate SSH access to reopen the SEC-halt path. | **BLOCKED** — SEC hold on the JUMP path pending admin rotation (`SEC-2026-09-14-04`). No SSH key present on disk under workspace. | `notes/PROBE_REFIRE_STATUS_20260916.md` + `notes/ADMIN_BINDS_20260915.md`. | **BANKED / UNVERIFIED** |
| **HuggingFace token** (used by `audio_poc.hf_transcribe`) | "Rotation" delivered by owner-drop; sha-diff against previous file. | **NOT-ROTATED** — new file is byte-identical to the old. Rotation ledger carries `SEC-2026-09-14-04` as still-outstanding. | `notes/HF_TOKEN_ROTATION_LEDGER_20260914.md`. | **BANKED / UNVERIFIED (rotation)** |
| **GPU 72-h campaign** (`akki-vm`, `akki-vm-ii`, 2 GPUs each) | Continuous sampler + workload with interleave check-ins at every seal boundary. | **RUNNING · in-perimeter** — at last check-in (post CP-M8-CSD-1 seal): elapsed 16.14 h · remaining 55.86 h · both hosts `sampler_alive+workload_alive` · zero synthetic burn · no anomalies. Bench iters 1900/1900, telemetry samples 386/386 per host at earlier tick. | `notes/GPU_UTILIZATION_72H.md` (2 426 B) + `notes/GPU_UTILIZATION_72H.json` (2 584 B) + continuous `phase0/commissioning_records/*.json` stream. | **BANKED / RUNNING** |

Aggregate posture per the last banked refire status: **1 PASS · 5 BLOCKED · 0 FAIL.**

---

## 7 · Guardrails used this session

All of the following are enforced as *disciplines*, not merely aspirations; the associated evidence is on-disk.

- **No secrets to stdout.** Every credential probe uses metadata-only parsing (shape, byte-length, sha-pin). No `cat`/`head`/`tail` of custody files. Only sha256 shape and length reported. **[VERIFIED — session commands audited by construction.]**
- **`BASELINE_GUARD=1` for every pytest run.** The passed-floor ratchet is enforced monotonically; a regression would fail the guard. **[VERIFIED — session pytest command.]**
- **Local-commits-only · no-push.** Neither the assessment_workspace repo nor Extraction-Akki has been pushed this session. **[VERIFIED — no push commands issued.]**
- **No re-clone.** All four public repos remain at the SHAs pinned at initial clone. **[VERIFIED — HEAD SHAs match banked values.]**
- **No `testing_agent`.** Owner has explicitly banned the platform's `testing_agent` for this project. All test evidence is direct terminal pytest with `BASELINE_GUARD=1`. **[VERIFIED — no `testing_agent` invocation.]**
- **§E credential discipline.** Metadata-only parse, atomic download to `estate_keys/`, `chmod 600`, sha-pin. **[BANKED — `custody_file.py` lines 96–100; not re-executed this turn.]**
- **21-token grep-negative** for every new mechanism (`voiceprint`, `embedding`, `biometric`, …). **[VERIFIED — commit-message evidence for CP-M8-CSD-1 and CP-M7-W9-UPGRADE-1 documents the grep-negative.]**
- **Zero-perturbation window during the GPU 72-h campaign.** Interleave check-ins only; no synthetic burn; no workload displacement. **[BANKED — `GPU_UTILIZATION_72H.md`.]**

---

## 8 · Owner build disciplines that shaped ideation & implementation

These are the *invariant patterns* the owner ratified across the build; every mechanism the platform now carries obeys them.

### 8.1 Thin-kernel · no-refactor
Only add what a test forces; never touch neighbouring code. Refactors are treated as an *anti-pattern* and are rejected at review. **[BANKED — STANDING_ORDERS §3 BUILD DISCIPLINE.]**

### 8.2 Tests-first (RED → GREEN 1 → GREEN 2 byte-match)
Every new mechanism starts as a **failing invariant test** (RED). Implementation lands until it passes (GREEN 1). Independently a second run with the same fixtures must produce byte-identical output — the *double-green byte-match* proof (GREEN 2). Both greens must land before the seal. **[VERIFIED — CP-M8-CSD-1 seal note carries "double-green byte-match (stripped sha256 2f7a499d29ac7c438e36cd4290823c72cf281d1376b2ff6d337ad095f363c3e8)".]**

### 8.3 §3.3 3-commit protocol (A / B / C)
- **Commit A** — code + tests + ratchet bump land on `programme/track-a` (or the code branch).
- **Commit B** — state (DECISIONS, NEXT, PINS), seal file, seal note, receipts, GPU util check-in land on `master`; references Commit-A SHA.
- **Commit C** — master *fixup* commit that self-references Commit-B SHA and finalises the seal chain (so the full triple is auditable at SHA-256 level).

Every wave-close and every CP-seal uses this pattern. Precedents in `git log master`: `M6 SEAL` (Commits `93fb95c7` + `6b6b52cb`), `CP-M7-W9-UPGRADE-1` (`92eaad74` + `250b85a7`), `CP-M8-CSD-1` (Commits A `40b6ee0` + B `00b16232` + C **pending in working tree**). **[VERIFIED — git log per pair.]**

### 8.4 Monotonic ratchet
`tests/invariants/baseline_failures.json` carries `passed_floor` and a `ratchet_history` (181 entries). Any code change that would *decrease* the passed count fails the baseline guard. The floor moves up only, and only in explicit ratchet-bump commits. **[VERIFIED — 4433 today.]**

### 8.5 Preventive-charter vs hard-gate
The platform is in *pilot*. Refusal mechanisms are **preventive-charter** by default: they *record and alert* on drift, but do not *hard-gate* runtime traffic. The upgrade path to hard-gate is preserved by construction (a future CP can wrap the same assert). Owner ratified this posture explicitly for §3.2 clause 5 shape (b). **[VERIFIED — CP-M8-CSD-1 owner ruling verbatim.]**

### 8.6 DEFAULT-PENDING-OVERRIDE
When the owner has not ruled explicitly, a value is entered in `RULING_LEDGER.md` as **DEFAULT-class · revisable on evidence**. It is wired now, but the ledger row remains open until an owner ruling either ratifies or replaces it. **[BANKED — `notes/RULING_LEDGER.md` categories.]**

### 8.7 Case-agnostic doctrine (2026-09-13)
All cross-module identifiers are **OPEN str** references; zero closed enums; 21-token grep-negative test on domain tokens. This forbids the platform from lexically knowing about (say) `voiceprint` or `embedding` — the case-agnostic pattern that lets a future owner ruling introduce a new derivative kind without any code refactor. **[VERIFIED — CP-M8-CSD-1 mechanism satisfies the 21-token grep-negative.]**

### 8.8 Zero-perturbation during the 72-h GPU campaign
The active 72-h GPU utilization campaign runs undisturbed on `akki-vm` and `akki-vm-ii`. Every seal / wave close interleaves a *check-in* only — never a workload change. **[BANKED — `notes/GPU_UTILIZATION_72H.md`.]**

### 8.9 Trust the disk · Boot Ritual
Session start is defined by `STATE/STANDING_ORDERS.md §1 SESSION BOOT PROTOCOL`. All facts are re-derived from disk (git, STATE, notes, receipts) — never from README, prior conversation, or agent memory. **[VERIFIED — this brief was authored under Boot Ritual.]**

---

## 9 · Journey so far · what's needed to complete

### 9.1 Narrative timeline of the recent session

1. **CP-M7-W2-CONTRACT-1** (commit `757c0c5`, 2026-09-16) — Audio-census job scope sub-carrier + owner-ratification gate landed on track-a; ratchet 4406 → 4412. **[VERIFIED — git log]**
2. **CP-M7-W9-CONTRACT-1** (commit `2e227dd`, 2026-09-16) — Path C default corpus deliverable schema landed; ratchet 4400 → 4406. **[VERIFIED]**
3. **CP-M7-W8-LIFT-1** (commit `561cfce`, 2026-09-16) — Ruling #5 tier-lift admissibility carrier landed; ratchet 4412 → 4419; §3.3 3-commit completed. **[VERIFIED]**
4. **HUAWEI OBS bounded validation PASS** (commit `44743c8b`, 2026-09-16) — Status 200 shape-only probe; §E discipline preserved. **[VERIFIED — git log]**
5. **OWNER RULING §A bundle banked** (commit `d9df33f1`, 2026-09-16) — Shape β ratified; F.1 duplicate finding; F.3 rotation ledger update. **[VERIFIED — git log]**
6. **CP-M7-W9-UPGRADE-1** (commit `cdf2312` + master fixup `250b85a7`, 2026-09-16) — Path B upgrade derivative corpus landed; ratchet 4419 → 4426; §3.3 3-commit complete. **[VERIFIED]**
7. **M6 SEAL LANDED** (commits `93fb95c7` + `6b6b52cb`, 2026-09-16) — 9/10 sub-waves sealed + SW-10 deferred; state-only wave-close report; ratchet 4426 unchanged. **[VERIFIED]**
8. **CP-M8-CSD-1** (Commit-A track-a `40b6ee0` + Commit-B master `00b16232`, 2026-09-16) — §3.2 clause 5 shape (b) preventive-charter sealed; ratchet 4426 → 4433 with double-green byte-match. **Commit-C fixup authored in working tree, awaiting owner unblock.** **[VERIFIED]**
9. **Read-only STATUS REPORT** (2026-09-17, this session) — Owner requested a factual read-only report; pytest re-run confirms `4433 passed, 1 skipped`; five dirty tracked files carry the Commit-C fixup payload. **[VERIFIED]**

### 9.2 To reach *done* — concrete checklist

- [ ] **CP-M8-CSD-1 Commit-C fixup** — commit the 5 (+1) dirty tracked files on `master`. Banks `00b16232` as Commit-B SHA. Closes the §3.3 3-commit protocol for the last M8 CP. *Owner unblock required.*
- [ ] **M8 SEAL wave-close report** — 9-section END-OF-WAVE format per STANDING_ORDERS §2 large-wave rule; must inline the **OVERALL BUILD STATUS** table (per owner directive verbatim: "*Report at M6 seal and M8 seal with the status table*"). Author + land as its own §3.3 3-commit (state-only, no ratchet change).
- [ ] **Overall build status table** — inline in the M8 SEAL report; enumerates every wave / CP with sealed / deferred / open / blocked status and pointer to the seal file.
- [ ] **GPU 72-h campaign close-out** — capture terminal check-in when the campaign concludes; log final `elapsed` / `remaining` / anomalies.
- [ ] *(later, after M8 SEAL lands)* **Discharge SEC-2026-09-14-04** (genuine HF token rotation) and unblock BLOCKED probes (JUMP rotation + admin IP-sets), enabling MySQL CD/Visitors, NAS, radio and transcription probes.
- [ ] *(after owner authorisation)* **M6-SW10** — full training runs on estate audio; currently DEFERRED-TO-CLOSE.
- [ ] *(parked)* **WPW R1/R2/R3** and **R-6 pricing**.

### 9.3 Not started · owner-authored decisions expected before proceeding
- Explicit authorisation to close Commit-C.
- Explicit authorisation to author the M8 SEAL wave-close report.
- Ruling on any of the OPEN rows in `notes/RULING_LEDGER.md`.

---

## Appendix A · Report provenance

Session commands whose output backs this brief (all read-only):
- `ls -la /app/assessment_workspace/` (working tree).
- `ls STATE/`, `ls notes/`, `ls canon/text/`, `ls canon/unpacked/`.
- `git status` + `git log -5` on both `programme/track-a` (Extraction-Akki) and `master` (assessment_workspace).
- `git log -1 --format='HEAD %h %ad %s' --date=short` on RMS-IQ-Core-2, Akki-OS-V1, Extraction-Akki, Akki-Executive-Core.
- `git diff --stat` + `git diff` on the 5 dirty tracked Commit-C-fixup files.
- `ls services/`, `ls services/governance_plane/`, `ls services/audio_plane_v1/`, `ls services/release_gate/`, `ls services/ip_allowlist/`, `ls services/artifact_store/`.
- `wc -l tests/invariants/baseline_failures.json` (1 639 lines).
- Python read of `ratchet_history` (181 entries; first + last shown above).
- `ls phase0/output_verified_seals/` (63 files) + prefix histogram.
- `grep "^## " STATE/STANDING_ORDERS.md` (6 sections).
- Head of `notes/RULING_LEDGER.md` + `notes/OWNER_RULING_A_BUNDLE_SHAPE_BETA_20260916.md`.
- `BASELINE_GUARD=1 python -m pytest tests/invariants/ -q` (result: `4433 passed, 1 skipped, 438 warnings in 132.94s`).

No writes to source, no commits, no push, no re-clone. No credential values printed. No `testing_agent` invocation. This brief was authored under the STANDING_ORDERS §1 SESSION BOOT PROTOCOL discipline.
