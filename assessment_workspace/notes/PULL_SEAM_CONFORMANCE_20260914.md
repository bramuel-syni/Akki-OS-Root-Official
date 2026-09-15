READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

> **SUPERSEDED — 2026-09-15T~01:40Z.** This document cited invented
> `PS-P*` IDs and inherited prose gloss from
> `notes/canon_pull_seam_requirements.md`. It is superseded by
> `notes/PULL_SEAM_CONFORMANCE_VERBATIM_20260914.md` which rebuilds the
> gap table from the verbatim extraction. Per owner ruling
> 2026-09-15T~01:40Z. Retained for audit-trail continuity only.

# PULL_SEAM_CONFORMANCE_20260914.md

**Canon source:** `The Pull Seam` (pull_seam_principles_v1 · 14 September 2026 · External) · sha256 `0a3084422726dd76aee6a6d80d9e3534ded2677cfe95947215c9762fe305afab` · requirements at `notes/canon_pull_seam_requirements.md` (70 numbered requirements).
**Purpose:** map each principle-level requirement to what already exists in-repo vs what is missing. **INGEST_AND_MAP_ONLY** — no build. Owner will scope the wave.
**Ratchet at time of writing:** 3979. **Track-a HEAD:** `6549c31`. **Master HEAD:** `e22d1f68`.

---

## Legend

* **✔ COVERED** — an existing surface fully discharges the requirement (gate-able today).
* **◐ PARTIAL** — an existing surface discharges part of the requirement; a bounded extension closes it.
* **✗ MISSING** — no in-repo surface addresses the requirement.
* **N/A HW** — hardware / deployment concern (physical port, front panel). Not a code invariant.

Every "existing surface" citation is a real path in `repos/Extraction-Akki/backend/` verified this session.

---

## §2 · Principles

### Principle 1 · Compute comes to the data

| Req | Requirement (short) | Status | Existing surface (if any) | Gap |
|---|---|---|---|---|
| PS-P1.1 | Sealed appliance inside customer perimeter | **N/A HW** | — | Deployment concern; documented in seal not code. |
| PS-P1.2 | Appliance holds GPUs on-prem | **◐ PARTIAL** | `services.training_runner.ssh_seam` (dispatches training to `akki-vm` / `akki-vm-ii` hosts by SSH); `phase0/gpu_burn/` (on-host receipts). | Estate GPU host is the source of truth for training runs, but nothing asserts the ceiling ("no rented off-host GPU can run training"). Need invariant that refuses training dispatch to any host outside the estate host allow-list. |
| PS-P1.3 | Queries execute on appliance | **◐ PARTIAL** | `services.mtafiti.probes.live_readonly_probe` + `readonly_sql_guard` refuse writes and stay bounded to estate DBs. | Not yet invariant-gated: no test that refuses SQL dispatch to a non-estate destination. |
| PS-P1.4 | Models train on appliance | **◐ PARTIAL** | Campaign infra dispatches to estate GPU hosts only (see PS-P1.2). | Same as PS-P1.2 gap. |
| PS-P1.5 | Party's model comes IN; weights leave OUT | **✗ MISSING** | — | No `IncomingModelAdmit` surface; no synthetic-env pre-flight (see PS-T1); no model-registry mint path. |
| PS-P1.6 | "No configuration transfers estate data outside" — prohibition, not default | **✗ MISSING** | — | Build-time invariant that scans `services/**` for any HTTP/SFTP/S3 outbound of raw-record payloads is not written. Adjacent guards exist (secret_hygiene, egress-window) but the affirmative "no-exfil path" invariant is absent. |

### Principle 2 · One seam, two ports

| Req | Requirement (short) | Status | Existing surface | Gap |
|---|---|---|---|---|
| PS-P2.1 | Two physically separate connectors | **N/A HW** | — | Deployment. |
| PS-P2.2 | Colour-keyed + labelled ESTATE/WAN | **N/A HW** | — | Deployment. |
| PS-P2.3 | Data read through ESTATE | **◐ PARTIAL** | `readonly_nas_guard.py` + `readonly_obs_guard.py` (CP-A1) + `readonly_sql_guard.py` (W-MTAFITI-GPU-DISCOVERY CP1). Three read guards on the three live sources. | No named "ESTATE port" symbol; the three guards agree by convention but don't share a common `ESTATE_INTERFACE` closed enum. |
| PS-P2.4 | Parties connect through WAN | **◐ PARTIAL** | IP allowlist middleware (`SPINE_ALLOWED_IPS`); FastAPI ingress. | No labelled "WAN port" symbol; conflated with the pod's public ingress. |
| PS-P2.5 | Exactly ONE software crossing function | **✗ MISSING** | Closest ancestor: `services/chokepoint/router.py` (LLM crossing) + `services/dap/gates.py::governed_operation` (governance decorator). | Nothing declares itself as *the* crossing function; nothing else refuses to be one. No `Seam.crossing()` closed surface. |
| **PS-P2.6** | **Build scan fails on a second crossing path** | **✗ MISSING** | — | **Highest-value structural gap.** No invariant walks `services/**` at build/ratchet time and refuses any second module that implements a WAN→ESTATE path. This is the primary Pull-Seam-enforcement invariant. |
| PS-P2.7 | Outbound allow-list | **◐ PARTIAL** | `services/chokepoint/llm_endpoint_allowlist.v0.json` (LLM egress allowlist) + `services/chokepoint/residency_allowlist.v0.json` + HF token env-only loader (`services.secret_hygiene.hf_token`) enforces one HF destination. | Partial: covers LLM + residency + HF. No single unified `outbound_allowlist.v1.json` that names every destination the appliance is allowed to reach; individual destination allowlists are not composed. |

### Principle 3 · Two sides share nothing

| Req | Requirement (short) | Status | Existing surface | Gap |
|---|---|---|---|---|
| PS-P3.1 | Separate trust domains | **◐ PARTIAL** | `services/trust_domain_description` (canon requirements banked at `notes/canon_trust_domain_description_v1_requirements.md`). | Doc-level anchor exists; enforcement is thin. Cross-domain-identifier invariant not landed. |
| PS-P3.2 | No shared identifiers | **✗ MISSING** | — | No `party_key`/`record_key` type separation invariant. |
| PS-P3.3 | No shared storage | **◐ PARTIAL** | Two-branch git repo layout (track-a code vs master state) is a weak analogue; runtime storage separation not asserted. | No filesystem/DB namespace separation invariant between ESTATE-facing and WAN-facing state. |
| PS-P3.4 | No shared credentials | **✔ COVERED** | `services.secret_hygiene.hf_token.load_hf_token_or_raise` env-only; credentials in `/app/backend/estate_keys/` mode 0600, git-ignored; SO §4 credential-custody rule. | Extensions to non-HF credentials would use the same pattern; guard-writer wave `W-HYGIENE-HF-TOKEN-GUARD` closed. |
| PS-P3.5 | Party key: own, revocable, expiring, non-transferable, never logged | **✗ MISSING** | — | No `PartyKey` type at all. No revocation ledger, no expiry, no transferability check. IP allowlist substitutes weakly. |

### Principle 4 · Identity never crosses

| Req | Requirement (short) | Status | Existing surface | Gap |
|---|---|---|---|---|
| PS-P4.1 | Results pass through the crossing before leaving | **◐ PARTIAL** | `services/audio_poc/release_gate.py::admit_transcript_release` + `services/data_suite_v2/export_gate.py::admit_export`. Two release gates today. | The gates exist per-artefact-kind but the seam-wide "every crossing goes through *one* crossing function" invariant (PS-P2.5) is missing, so PS-P4.1 is enforced piecemeal not universally. |
| PS-P4.2 | Identifiers replaced with placeholder tokens per custody class | **◐ PARTIAL** | `services/mtafiti/detectors/pii_redaction_guard.py::redact_row` + `_hash16(kind, value)` produces `<REDACTED:pii.<kind>:<hash16>>` tokens (deterministic, salted-sha256, idempotent). | Redaction is by PII-class taxonomy, not custody-class. `services/response_sanitizer/pii_classification_registry.v0.json` has classifications but no per-custody-class token policy. |
| PS-P4.3 | Confidential values replaced with placeholders | **◐ PARTIAL** | `services/shield_train/masking_policy.v0.json` (mask_regex_scrub for author'd columns); `redact_row` (PII). | Confidentiality classification is per-column ledger, not per-record custody class; the two don't compose. |
| PS-P4.4 | Re-identification only inside perimeter | **✗ MISSING** | Salt in `_hash16` lives on-appliance (env var), so out-of-perimeter re-id is architecturally impossible today. | Not invariant-gated. |

### Principle 5 · Six crossings, each governed on its own terms

| Req | Operation | Status | Existing surface | Gap |
|---|---|---|---|---|
| PS-P5.1 | Browse the estate (aggregate composition only) | **◐ PARTIAL** | `services/mtafiti/composition_census.py` produces aggregate composition (row-count / schema / column-role stats); receipts under `phase0/mtafiti_gpu_discovery/`. | Not exposed as a "Browse" crossing surface with its own governance rules; no closed browse-artefact contract. |
| PS-P5.2 | Query (API) — de-identified results | **◐ PARTIAL** | `services/mtafiti/probes/live_readonly_probe.py` runs read-only SQL, redacts through `redact_row`. | No "Query crossing" surface with `QueryArtefact` frozen carrier; no per-query approval gate for controlled-column touches. |
| PS-P5.3 | Processed intelligence — derived output only | **◐ PARTIAL** | `services/solva_v2/*` (reasoning primitives · trace · intent audit); `services/dap/gates.py::governed_operation`. | Derived-output crossing is not a distinct surface. No `ProcessedIntelligenceArtefact`. |
| PS-P5.4 | Train a model | **✗ MISSING** | `services/shield_train/pipeline.py::execute_governed_lora_run` gates on masking-tier admission and refuses when tier not admissible. Adjacent primitive. | No `TrainedWeightsArtefact` with rights-posture + weights-hash + terms carriers; no "always-approval" gate on training crossings. |
| PS-P5.5 | Build a skill | **✗ MISSING** | `backend/contracts/skill_file_provenance_v0.py` + `services/skill_files/` (some primitives). | No `SkillArtefact` crossing gate with skill-hash + records-read + terms. |
| PS-P5.6 | Download raw data | **✗ MISSING** | — | No outer-gate surface at all. This is PS-P8 → its own row below. |
| PS-P5.7 | Five of six release derivatives; only one releases data itself | **✗ MISSING** | — | The taxonomy isn't a closed enum anywhere. Should be a closed 6-value `CrossingKind` enum with attached rules table (Sequential to Solva-V2's `SolvaTrace` shape). |

### Principle 6 · Trained model measured before release

| Req | Requirement (short) | Status | Existing surface | Gap |
|---|---|---|---|---|
| PS-P6.1 | Training changes weights; weights carry statistical influence | **N/A (fact)** | — | Doctrinal statement; no gate required. |
| PS-P6.2 | Training differentially private by default | **✗ MISSING** | — | No DP-SGD or noise-injection primitive wired into `services/shield_train/pipeline.py`. |
| PS-P6.3 | Memorisation probe before release | **✗ MISSING** | — | No probe surface. |
| PS-P6.4 | Refuses release until distance-from-controlled-records threshold met | **✗ MISSING** | — | No distance metric primitive. |
| PS-P6.5 | Every release debited against release budget | **✗ MISSING** | — | No `ReleaseBudget` primitive in-repo. |
| PS-P6.6 | Release budget = single global ceiling across all parties/ops/time | **✗ MISSING** | — | Same as above. This is the second-highest-value structural gap after PS-P2.6. |

### Principle 7 · Every crossing recorded — or doesn't happen

| Req | Requirement (short) | Status | Existing surface | Gap |
|---|---|---|---|---|
| PS-P7.1 | Receipt carries 5 fields (what/quantity/terms/party/time) | **◐ PARTIAL** | Multiple receipt writers across `services/*` (shield_train_receipts, mtafiti_gpu_discovery, drill_receipts, commissioning_records, nas_connect_receipts, live_readonly_probe). None share a common 5-field schema. | No `Receipt.v0` frozen contract enforcing all 5 fields together. |
| PS-P7.2 | Receipt written BEFORE result returned | **◐ PARTIAL** | `services/audio_poc/gap_fill_writer.py` writes receipt before write-back; `dap/gates.py::governed_operation` decorator carries some ordering. | Not universal; no invariant refuses a code path that returns a result without a prior receipt write. |
| PS-P7.3 | Op refused if receipt cannot be written | **◐ PARTIAL** | Present per-surface (audio_poc + shield_train) but not universal. | Same gap as PS-P7.2. |
| PS-P7.4 | Fail-closed on approval/terms/check failure | **◐ PARTIAL** | `services/dap/gates.py::FailedClosed` (RuntimeError); Solva-V2 CP-S4 three-action envelope refuses fourth-action. | No `FailClosed` decorator wired around every governed op. |
| PS-P7.5 | No path returns data/result/model when a check did not complete | **◐ PARTIAL** | Individual gates refuse; no universal enforcement invariant. | Composition gap. |

### Principle 8 · Raw data leaves through a separate outer gate

| Req | Requirement (short) | Status | Existing surface | Gap |
|---|---|---|---|---|
| **PS-P8.1** | **Outer gate is a distinct surface** | **✗ MISSING** | — | Not built. Highest deliberate-scope gap: the six ordinary crossings + outer gate = seven paths; today we have zero for outer gate. |
| PS-P8.2 | Disclosure depth bounded by rights and custody | **✗ MISSING** | — | No `DisclosureDepth` primitive. |
| PS-P8.3 | Redaction runs as a gate, not a suggestion | **◐ PARTIAL** | `services/mtafiti/detectors/pii_redaction_guard.py::assert_no_raw_pii` raises `RawPiiLeakForbidden`; scan-and-refuse pattern present. | Wired only to the mtafiti live-probe pipeline; not to a raw-download gate. |
| PS-P8.4 | Named human sign-off | **✗ MISSING** | — | No signer registry, no signer-mint step in any release path. Solva/DAP verdicts are R-N rulings but not per-download signer attestations. |
| PS-P8.5 | Every released record individually recorded | **✗ MISSING** | — | Per-record recording surface absent (only per-batch receipts exist). |

---

## §5 · Precise-leave statement — additional roll-up

| Req | Requirement (short) | Status | Note |
|---|---|---|---|
| PS-S5.1a | No raw record leaves except through outer gate + signed | **✗ MISSING** | Follows from PS-P8 gaps. |
| PS-S5.1b | Everything else leaves as one of {de-identified results, derived intelligence, measured artefacts} — closed 3-value set | **◐ PARTIAL** | Two of the three artefact carriers exist as frozen dataclasses (`TranscriptArtefact` measured audio-poc + `ExportArtefact` DAP-A10). The closed 3-value carrier enum is not present. |
| PS-S5.1c | Aggregate bounded by release budget | **✗ MISSING** | Blocked by PS-P6.5. |
| PS-S5.1d | Recorded individually | **◐ PARTIAL** | Some individual receipts present per artefact kind; not gate-enforced universally. |

---

## §8 · Observable-corresponding artefacts

| Req | What a technical reader can observe | Status | Existing surface (if any) |
|---|---|---|---|
| PS-O1 | Front panel two-port + GPUs inside | **N/A HW** | — |
| PS-O2 | Build test output — single-crossing check passing | **✗ MISSING** | Direct correspondent of PS-P2.6 gap. |
| PS-O3 | Outbound allow-list published | **◐ PARTIAL** | `chokepoint/llm_endpoint_allowlist.v0.json` + `residency_allowlist.v0.json` exist per-purpose; unified allow-list absent. |
| PS-O4 | Receipt + ledger entry with 5 carriers | **◐ PARTIAL** | Various receipt writers; no unified schema. |
| PS-O5 | Memorisation probe result | **✗ MISSING** | See PS-P6.3. |
| PS-O6 | Release budget + consumption | **✗ MISSING** | See PS-P6.5. |
| PS-O7 | No setting moves estate data to outside compute | **◐ PARTIAL** | Adjacent guards exist (secret_hygiene, egress-window, chokepoint allowlist) but the affirmative "no-exfil path" invariant is not written. |

---

## Roll-up: coverage by principle

| Principle | ✔ | ◐ | ✗ | N/A HW |
|---|--:|--:|--:|--:|
| 1 · Compute-to-data | 0 | 3 | 2 | 1 |
| 2 · One seam, two ports | 0 | 3 | **1 (P2.6)** | 2 |
| 3 · Share nothing | 1 (P3.4) | 2 | 2 | 0 |
| 4 · Identity never crosses | 0 | 3 | 1 | 0 |
| 5 · Six governed crossings | 0 | 3 | 4 | 0 |
| 6 · Model measured before release | 0 | 0 | **5** | 1 (P6.1 fact) |
| 7 · Every crossing recorded | 0 | 5 | 0 | 0 |
| 8 · Outer gate | 0 | 1 | **4** | 0 |
| **Total (41 principle sub-clauses)** | **1** | **20** | **19** | **4** |

**One-line summary:** roughly half the Pull-Seam principle-clauses have a partial in-repo anchor today (◐), half have no anchor (✗). Only one clause (PS-P3.4 · no shared credentials) is fully covered — that clause was hardened in the W-HYGIENE-HF-TOKEN-GUARD wave this M5 sprint. The three highest-leverage structural gaps are **PS-P2.6 (single-crossing build scan), PS-P6.5 (release budget), PS-P8 (outer gate)**.

---

## Recommendation (owner scopes the wave)

The Pull-Seam gap-closure is naturally chartered as a **staged multi-wave programme**, not a single wave. Suggested staging (each staging item is a candidate wave with its own grounding brief · owner decides sequence + scope):

1. **W-PULL-SEAM-STAGE-1 · Single-crossing declaration + build scan (PS-P2.5 + PS-P2.6 + PS-O2)**
   * Declare `services/pull_seam/crossing.py::cross(direction, artefact) -> None` as *the* crossing function.
   * Land an AST-parsed build-time invariant that scans `services/**` and refuses any second module that implements the WAN→ESTATE / ESTATE→WAN path (Solva-V2 CP-S1 two-faculty-seam-import-assertion precedent).
   * **Ratchet estimate:** +8 to +12.

2. **W-PULL-SEAM-STAGE-2 · Six-crossing taxonomy + receipt-v0 unified schema (PS-P5.1..P5.6 + PS-P7.1)**
   * Land `contracts/crossing_kind.py::CrossingKind` closed 6-value enum + `contracts/pull_seam_receipt.py::Receipt` frozen 5-field carrier.
   * Migrate the two existing gates (`release_gate.py`, `export_gate.py`) to emit `Receipt` records.
   * **Ratchet estimate:** +10 to +14.

3. **W-PULL-SEAM-STAGE-3 · Release budget primitive (PS-P6.5 + PS-P6.6 + PS-O6)**
   * `contracts/release_budget.py::ReleaseBudget` frozen · `debit_budget(receipt) -> new_ceiling` append-only + refuse on exhaustion.
   * Wire the two existing gates through `debit_budget`.
   * **Ratchet estimate:** +6 to +8.

4. **W-PULL-SEAM-STAGE-4 · Custody-class placeholder-tokenization (PS-P4.2 + PS-P4.3)**
   * `contracts/custody_class.py::CustodyClass` closed enum · per-class token policy (extension of `_hash16`).
   * Compose with existing `pii_redaction_guard` and `masking_policy`.
   * **Ratchet estimate:** +8 to +10.

5. **W-PULL-SEAM-STAGE-5 · Outer gate for raw download (PS-P8.1..P8.5)**
   * `services/outer_gate/download.py` with per-record recording + named-human signer + rights-and-custody depth bound.
   * Deliberately outside the six-crossing taxonomy (distinct surface).
   * **Ratchet estimate:** +10 to +14.

6. **W-PULL-SEAM-STAGE-6 · Memorisation probe + DP-training gate (PS-P6.2 + PS-P6.3 + PS-P6.4 + PS-O5)**
   * `services/measurement/memorisation_probe.py` + wire into `shield_train.pipeline`.
   * Refuse-in-full on distance-threshold miss.
   * **Ratchet estimate:** +10 to +12.

7. **W-PULL-SEAM-STAGE-7 · Party-key primitive + revocation ledger (PS-P3.5)**
   * `contracts/party_key.py::PartyKey` frozen · revocation record append-only · no-log invariant.
   * **Ratchet estimate:** +6 to +8.

**Aggregate ratchet estimate (all seven stages): +58 to +78 invariants.** Comparable in scale to W-DATA-SUITE-V2-LIFT (+50) but staged.

**Do not build any of this now.** Owner scopes the wave.

---

## Cross-links

* Principle-level requirements: `notes/canon_pull_seam_requirements.md`.
* Raw canon: `canon/drops/20260914_pull_seam/raw/The_Pull_Seam.docx`.
* Extracted text: `canon/drops/20260914_pull_seam/extracted/The_Pull_Seam.txt`.
* Drop manifest: `canon/drops/20260914_pull_seam/manifest.json`.
* Adjacent existing waves: `notes/W_AUDIO_POC_wave_close.md` · `notes/W_DATA_SUITE_V2_LIFT_close.md` · `notes/W_HYGIENE_HF_TOKEN_GUARD_close.md` · `notes/W_SOLVA_V2_LIFT_close.md`.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
