# W-M6-OBJECTIVE-WIZARD-COLLECTION-SCHEMA · Wave close

**Wave sealed at UTC:** 2026-09-15T~22:59Z
**Milestone:** M6 · Sub-wave 6 (§8 + §9 + §12.1 + Rec-3-M6SW6 + Redaction Hardening Option 1 hygiene)
**Track-a HEAD at wave close:** `053d3f1` (last CP mechanism · hygiene) · **Master HEAD:** `df98f8f6` (last CP fixup · landed under STANDING_ORDERS §3.3 · NO SEAL WITHOUT BOTH SHAs rule satisfied across all 5 seals)
**Ratchet delta:** 4240 → 4288 (+48) across five CPs (4 sub-wave 6 §15 CPs + 1 hygiene CP)

---

## §A · What we built

Sub-wave 6 discharged **§8 Objective Wizard compile-refusal + §9 Collection Schema type + §12.1 P195 per-commission registry namespace + Rec-3-M6SW6 backend registry surface** — the four §15 walk items packaged as CP-M6-6-1..4.  On top of that, one hygiene CP (CP-SW6-HYG-1) landed the Redaction Hardening Option 1 helper + STANDING_ORDERS §4.1 §E clause + version-controlled probe tool, discharging the SEC incident that surfaced mid-walk.

### CP-M6-6-1 · Objective Wizard compile-refusal + Rec-1-M6SW6 gate (§8.4 P139..P142 verbatim)

Landed `services/audio_plane_v1/objective_wizard.py` — compile-time refusal contract per §8.4 P139..P142 verbatim + Rec-1-M6SW6 write-path gate composing CP-M6-5-3 `assert_cluster_carries_no_human_name`.

- `AcceptanceBar` (frozen 2-carrier) · `TargetOutcomeStub` (frozen 3-carrier · STUB territory) · `CollectionSchemaColumnStub` (frozen 3-carrier · custody-marker + bound_cluster).
- `compile_objective_artifact(*, outcome, columns) -> None` — 4-refusal contract in P036 receipt-before-result order: test_set_ref → per_stratum_dimension → custody_violation → cluster_human_name_leak (first refusal wins; no partial success).
- Refusals (4): `TargetOutcomeMissingTestSetRefError` (V90) · `AcceptanceBarMissingPerStratumDimensionError` (V91) · `CollectionSchemaCustodyViolationError` (V92) · `CollectionSchemaClusterHumanNameLeakError` (Rec-1-M6SW6).

Ratchet 4240 → 4254 (+14).  Seal: `cp_m6_6_1_objective_wizard_compile_refusal.seal.txt`.  Track-a `6802806` · master `c98a113a` (Commit C-fixup `b5595ffa`).

### CP-M6-6-2 · Collection Schema type (§9 P148..P152 verbatim)

Landed `services/audio_plane_v1/collection_schema.py` — two-tier schema type per §9.1 P148 + §9.2 P150 + §9.3 P152 verbatim.

- `BASELINE_TIER_CONTENTS_V1_0` (frozen 5-tuple in verbatim canonical order per §9.2 P150) · `SCHEMA_TIER_VALUES` (frozenset {baseline, objective}).
- `CollectionSchemaColumn` (frozen 4-carrier: column_name + tier + quality_bar + provenance_ref; refuses invalid tier at `__post_init__`).
- `CollectionSchema` (frozen 3-carrier: schema_id + commission_id + columns).
- `construct_collection_schema` — refuses `BaselineTierIncompleteError` on missing v1.0 baseline; refuses `ObjectiveTierProvenanceMissingError` on objective-tier `None` provenance per §9.3 P152 (propose-qualify-graduate).
- Refusals (3): `SchemaTierInvalidError` · `BaselineTierIncompleteError` · `ObjectiveTierProvenanceMissingError`.
- §9.2 P150 baseline seam-governance held: `BASELINE_TIER_CONTENTS_V1_0` module-level frozen 5-tuple · extension owner-ratification-only (same discipline as `HUMAN_NAME_ATTRIBUTE_NAMES`).

Ratchet 4254 → 4263 (+9).  Seal: `cp_m6_6_2_collection_schema.seal.txt`.  Track-a `7c856fa` · master `d9766459` (Commit C-fixup `0bd45c50`).

### CP-M6-6-3 · Per-commission registry namespace (§12.1 P195 verbatim)

Landed `services/audio_plane_v1/commission_registry_namespace.py` — per-commission scoped registry namespace with sealed-not-deleted discipline per §12.1 P195 verbatim.

- `NAMESPACE_STATE_VALUES` (frozenset {open, sealed}) · `COLUMN_COLLECTION_STATE_VALUES` (frozenset {declared_not_yet_collected, collected} — declared-but-not-yet-collected as first-class state per §12.1 P195 verbatim).
- `NamespaceColumnEntry` (frozen 3-carrier) · `NamespaceStratumCoverageEntry` (frozen 2-carrier) · `CommissionRegistryNamespace` (frozen 6-carrier: commission_id + state + collection_schema_versioned_ref + column_entries + stratum_coverage_entries + sealed_at_utc).
- `open_namespace` · `record_declared_column` (refuses `NamespaceSealedError`) · `record_column_collected` (refuses `NamespaceSealedError` + `NamespaceColumnUnknownError`) · `seal_namespace` (refuses `NamespaceAlreadySealedError`; preserves entries per sealed-not-deleted).
- Sealed-not-deleted anchored: entries remain populated and queryable after seal per §12.1 P195 verbatim ("*sealed, not deleted: it is the record of what was collected and why, and the next objective's wizard session queries prior schemas and coverage so the second project starts from the first project's map.*").

Ratchet 4263 → 4274 (+11).  Seal: `cp_m6_6_3_commission_registry_namespace.seal.txt`.  Track-a `75447ac` · master `ea823aa3` (Commit C-fixup `c1ed5bc6`).

### CP-M6-6-4 · Ratified-vs-INFERRED backend registry surface (Rec-3-M6SW6 verbatim · CLOSES SUB-WAVE 6)

Landed `services/audio_plane_v1/backend_registry.py` — read-only registry surface enumerating every pluggable audio-plane seam with status ∈ {ratified, inferred_pending_ratification}, closed-set refusal on unknown status, deterministic output per Rec-3-M6SW6.

- `BACKEND_RATIFICATION_STATES` (frozenset {ratified, inferred_pending_ratification} · D10 vocabulary verbatim).
- `RegisteredBackendEntry` (frozen 5-carrier: seam_name + backend_name + ratification_state + canon_anchor + ratified_at_utc:Optional[str]).
- `BackendRegistrySurface` (frozen 1-carrier: entries tuple).
- `register_backend` — refuses `BackendRatificationStateInvalidError` on state ∉ closed set; refuses `BackendRatifiedButMissingRatifiedAtError` on `ratified` + `None` timestamp per §P036 receipt-before-result.
- `list_ratified_backends` + `list_inferred_backends` — insertion-order filters · deterministic output.
- `assert_seam_has_ratified_backend` — refuses `SeamHasNoRatifiedBackendError` when no ratified backend for the given seam; load-bearing gate for future live-invocation paths.
- Refusals (3): V123 · V124 · V125.

**M6-seal-story deliverable populated:** `phase0/backend_ratification_snapshot.json` — 5 seams enumerated (language_identifier · code_switch_detector · channel_condition_profiler · synthesis_attribute_capturer · clustering); all 5 in state `inferred_pending_ratification`; 0 ratified.  Codec service (CP-M6-4-1..4-4) excluded per shape mismatch (SERVICE not pluggable-backend seam; documented in `codec_note`).

Ratchet 4274 → 4282 (+8).  Seal: `cp_m6_6_4_backend_registry.seal.txt`.  Track-a `b4f5a6b` · master `75fa22d3` (Commit C-fixup `cfe9b789`).

### CP-SW6-HYG-1 · Credential metadata shape helper (Redaction Hardening Option 1 hygiene · out-of-walk)

Extended `services/secret_hygiene/custody_file.py` (append-only under `# Part-C extension` header · no refactor of existing functions) with positive-shape `read_custody_metadata` helper per owner ruling 2026-09-15T~22:30Z Redaction Hardening Option 1 (ratified same turn as SEC incident `sec_incident_jump_cred_leak_20260915T222935Z`).

- `CustodyFieldMetadata` (frozen 3-carrier: field_name + value_length_bytes + value_sha256 · structurally cannot carry a raw value — closed attribute set enforced by dataclass shape).
- `CustodyFileMetadata` (frozen 2-carrier: path + fields tuple).
- `read_custody_metadata(*, path)` — JSON custody read · raw values held only in private local scope · never assigned to any returned attribute.
- `NonCustodyPathRefused` (refuses paths outside `CUSTODY_PATH_PREFIXES`).
- `CustodyFileFormatUnsupportedError` (refuses non-JSON extensions this CP; CSV/xlsx/raw-key follow-on).

**Companion artefacts:**
- `STATE/STANDING_ORDERS.md §4.1 §E CREDENTIAL CUSTODY READ DISCIPLINE` clause landed — two-path rule (helper OR env-injection) authoritative from this seal forward.
- `/app/assessment_workspace/tools/boundary_probe_cd_visitors.py` version-controlled — 293-line probe tool using helper + env-injection · dry-run + opt-in-CSV modes · never echoes creds · shape-only receipts.

Ratchet 4282 → 4288 (+6).  Seal: `cp_sw6_hyg_1_credential_metadata.seal.txt`.  Track-a `053d3f1` · master `76a8476e` (Commit C-fixup `df98f8f6`).

---

## §B · Discharge summary vs canon

| Canon anchor | Verbatim clause discharged | CP | Mechanism |
|---|---|---|---|
| §8.4 P139..P142 | Compile-time refusal contract (4 refusals) | CP-M6-6-1 | `objective_wizard.py::compile_objective_artifact` |
| Rec-1-M6SW6 | Write-path gate composing `assert_cluster_carries_no_human_name` | CP-M6-6-1 | `CollectionSchemaClusterHumanNameLeakError` refusal |
| §9.1 P148 | Two-tier schema (baseline + objective) | CP-M6-6-2 | `SCHEMA_TIER_VALUES` |
| §9.2 P150 | v1.0 baseline five-item canonical order | CP-M6-6-2 | `BASELINE_TIER_CONTENTS_V1_0` |
| §9.3 P152 | Propose–qualify–graduate for objective columns | CP-M6-6-2 | `ObjectiveTierProvenanceMissingError` refusal |
| §12.1 P195 | Per-commission scoped namespace + declared-not-yet-collected first-class + sealed-not-deleted | CP-M6-6-3 | `commission_registry_namespace.py` (whole module) |
| Rec-3-M6SW6 | Ratified-vs-INFERRED backend registry surface | CP-M6-6-4 | `backend_registry.py` (whole module) |
| Owner ruling 2026-09-15T~22:30Z | Redaction Hardening Option 1 (helper + STANDING_ORDERS §E clause + probe tool) | CP-SW6-HYG-1 | `custody_file.py` Part-C extension + STANDING_ORDERS §4.1 §E + `tools/boundary_probe_cd_visitors.py` |

---

## §C · Composition · No-refactor across the wave

**No-refactor**: no modifications to any prior audio-plane module across the wave.  Every CP was additive.  §3.1 P038 tokens-not-waveforms discipline preserved on every new API surface.  §5.3 clause 2 "not what it is called" discipline preserved (CP-M6-6-1's Rec-1-M6SW6 gate composes with, and does not modify, CP-M6-5-3's `assert_cluster_carries_no_human_name`).

**Composition surface at wave close:**

- CP-M6-6-1 `CollectionSchemaColumnStub` is a STUB carrier (custody-marker + bound_cluster).  CP-M6-6-2 `CollectionSchemaColumn` is the full §9 carrier.  Both coexist without collision — CP-M6-6-1's compile-refusal uses the STUB shape (structural typing); CP-M6-6-2 introduces the runtime-tier carrier.
- CP-M6-6-3 `CommissionRegistryNamespace.collection_schema_versioned_ref` is a reference to a CP-M6-6-2 `CollectionSchema`.  Composition is by string reference, not by class coupling — case-agnostic per D10.
- CP-M6-6-4 `RegisteredBackendEntry.seam_name` names any of the CP-M6-1-1..1-4 or CP-M6-5-1 seams; population is externally driven at composition points, seams do not self-register.
- CP-SW6-HYG-1 `read_custody_metadata` composes with the existing guard trio (`assert_no_transcript_cat_on_custody`, `assert_no_transcript_csv_header_emit_on_custody`, `assert_no_transcript_openpyxl_iter_rows_on_custody`, `assert_no_transcript_set_x_with_password_var`) — guards refuse violating source-text patterns at authoring-time; helper provides the safe surface those refusals point toward.

---

## §D · Discipline receipts across the wave

Every CP walked §3.3: RED → mechanism → targeted green → ratchet bump → double-green byte-match → rider → seal → 3-commit close.  Byte-match stripped-sha256 recorded on every seal.  Ratchet monotonic-up throughout.  No test regressed.  Zero refactor.

| CP | RED log | Byte-match sha256 | Rider drift | Track-a | Master |
|---|---|---|---|---|---|
| CP-M6-6-1 | `20260915T213905Z` | `ab14ba54…` | zero | `6802806` | `c98a113a` |
| CP-M6-6-2 | `20260915T215523Z` | `71d78288…` | zero | `7c856fa` | `d9766459` |
| CP-M6-6-3 | `20260915T220901Z` | `d01332ef…` | zero | `75447ac` | `ea823aa3` |
| CP-M6-6-4 | `20260915T223452Z` | `9a2fb1a5…` | zero | `b4f5a6b` | `75fa22d3` |
| CP-SW6-HYG-1 | `20260915T224949Z` | `583ac87d…` | zero | `053d3f1` | `76a8476e` |

---

## §E · Boundary probes across the wave

- **Probes #48..#53** fired FAIL (CD + Visitors both 6.00-6.006s ETIMEDOUT).  Consistent with admin bind pending on CD/Visitors SGs.  Bank at `phase0/boundary_probes/probe_{48..53}_*.json`.
- **Probe #54 NOTE-SKIPPED** per SEC incident `sec_incident_jump_cred_leak_20260915T222935Z` + owner ruling Path β (probes observe not gate).  Bank at `probe_54_20260915T223210Z.json` · commit `0546bca9`.
- **Probe #55 NOT FIRED** — probe loop remains suspended pending JUMP custody rotation to JSON per SEC discipline.  Tool is version-controlled and ready to fire once rotation lands.

**Cumulative PASS count across probes #1–#54: 0.**  Admin binds for CD + Visitors remain owner-desk (SG-open + credential-scope discipline).

---

## §F · SEC incident this wave

**Incident**: mid-walk (immediately after CP-M6-6-3 seal), an attempt to probe #54 involved a bash read of the JUMP custody CSV.  My sed redaction pattern was wrong (masked right-of-comma; CSV holds sensitive values in column-0 left-of-comma per `step3_reachability_probe.py::load_jump`), causing the cleartext JUMP root password to render in one bash-tool STDOUT line of this session's transcript.

**Containment**:
- Halted probe firing immediately.
- Halted CP-M6-6-4 walk temporarily until owner ratification.
- Banked receipt at `phase0/security_incidents/sec_incident_jump_cred_leak_20260915T222935Z.json` (commit `75bf8e1f`).
- Banked note at `notes/SEC_INCIDENT_JUMP_CRED_LEAK_20260915.md`.
- The cleartext value was NOT written to any on-disk file, commit message, log, or receipt.  The leak is bounded to the agent-tool STDOUT captured in the current session's transcript.

**Owner rulings that landed same turn**:
1. **Path β**: probe #54 NOTE-SKIPPED; proceed to CP-M6-6-4; close sub-wave 6 on its seal.  Ratified.
2. **Option 1 (procedural + mechanical helper)**: land `credential_metadata`-style helper + STANDING_ORDERS §E clause + invariant tests.  Ratified.  Option 2 (encrypt-at-rest) DECLINED for now.
3. **Probe tool close**: version-control `tools/boundary_probe_cd_visitors.py` using the new helper + env-injection.  Ratified.

All three rulings are discharged in CP-SW6-HYG-1.

**Owner-desk items remaining** (unchanged after this wave):
- JUMP root credential rotation at `159.138.173.250`.
- Ratification of this SEC incident in `STATE/DECISIONS.md` at next owner turn.
- Admin SG binds for CD + Visitors (was already owner-desk; unchanged).

---

## §G · Sub-wave 6 DoD review

- ✓ CP-M6-6-1 sealed under §3.3 (both SHAs banked · `6802806` + `c98a113a`).
- ✓ CP-M6-6-2 sealed under §3.3 (both SHAs banked · `7c856fa` + `d9766459`).
- ✓ CP-M6-6-3 sealed under §3.3 (both SHAs banked · `75447ac` + `ea823aa3`).
- ✓ CP-M6-6-4 sealed under §3.3 (both SHAs banked · `b4f5a6b` + `75fa22d3`).
- ✓ CP-SW6-HYG-1 sealed under §3.3 (both SHAs banked · `053d3f1` + `76a8476e`) — hygiene CP out-of-walk.
- ✓ Wave-close report authored (this document).
- ✓ `phase0/backend_ratification_snapshot.json` populated at CP-M6-6-4 seal.
- ⚠ Ratchet delta actual: +42 for the four §15 walk CPs (target-band was +34..+38 · came in slightly higher due to parametric expansion at CP-M6-6-1: 14 vs target 10).  Plus +6 for the hygiene CP = **+48 total**.
- ⚠ Boundary probes #50..#57 target: #50, #51, #52, #53 fired FAIL; #54 NOTE-SKIPPED; #55..#57 SUSPENDED pending helper + tool landing + JUMP custody rotation.
- ✓ Word-boundary executive-domain negative-scan CLEAN on every seal.
- ✓ Word-boundary audio-material negative-scan CLEAN on every new module.
- ✓ §3.1 P038 tokens-not-waveforms discipline preserved on every new API surface.
- ✓ HALT boundary held — no CP required real estate voice/biometric material.

---

## §H · What I recommend to owner at wave close

1. **Ratify SEC incident** in `STATE/DECISIONS.md` at next owner turn.  Ledger has the receipt at `phase0/security_incidents/sec_incident_jump_cred_leak_20260915T222935Z.json`; ratification is a doctrine-level sign-off, not a code change.
2. **Rotate JUMP root credential** at `159.138.173.250` via sysadmin desk.  Coordinate with the migration of `/app/backend/estate_keys/bastion/jump_server_radio_system.csv` to a JSON custody format (e.g. `jump_server_radio_system.json` with `{"ip": ..., "user": ..., "password": ...}`) so the probe tool's JSON-custody branch replaces the opt-in-CSV branch as the default.
3. **Admin SG binds for CD + Visitors** remain owner-desk.  Once bound, boundary probes will start firing PASS and the probe tool receipts will be non-empty.
4. **Sub-wave 7 opening**: I can proceed autonomously with W-M6-TARGET-OUTCOME-PLANNER (§10 + §11.1 + §11.4) or await your ratification of this wave close.  Per your last direction ("continue the M6 §15 walk autonomously"), I will proceed unless directed otherwise.

---

## §I · Onward

**Sub-wave 7 · W-M6-TARGET-OUTCOME-PLANNER** — §10 + §11.1 + §11.4.  First CP: CP-M6-7-1 · full §10 `TargetOutcome` carrier (composes with CP-M6-6-1's `TargetOutcomeStub` — the STUB becomes deprecated once the full carrier lands, but old references remain callable during transition).

**Sub-wave 8 · calibration + acceptance** — §11.2 + §11.3.

**Sub-wave 9 · Commission View surface** — §13.

**Sub-wave 10 · §11.6 full training runs on real estate data** — **very likely HALT-to-owner at sub-wave open** per user direction.  Real estate voice/biometric material triggers M6 §E.5 HALT boundary; I will flag this early in the sub-wave 10 grounding brief.

Post-M6: M7 opens (W0..W9 · ALREADY RATIFIED per earlier owner turn).
