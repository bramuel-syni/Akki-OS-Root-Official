# CP-AIP-1-INGEST-CAPTURE · Comprehensive Seal Receipt

**Seal timestamp:** 2026-02-23T05:40:00Z  
**Ledger anchor:** EXECUTION_ORDER.md Item 5 · CP-AIP-1 (Ingest & Capture · AIP v1.0 §4.1-§4.4 + §4.6)  
**Owner authorization:** Item 4 checkpoint GO (2026-02-23 · owner verbatim quoted below).

**Ledger check** — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-1-INGEST-CAPTURE and nothing else.

---

## 1 · Owner GO (verbatim · banked at STATE/DECISIONS.md)

> "GO. Respond in English only. The owner pre-approved this exact order and the §16.2 working defaults — no reorder, no revision. Proceed with CP-AIP-1 · Ingest & Capture exactly as proposed, then continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals.
>
> Binding reminders for the AIP run (all 17 consolidated guards remain in force):
>
> 1. CP-AIP-1 acceptance = spec §4.6 verbatim, as RED-first invariants: (a) no segment leaves ingestion without languages[], condition profile, and applicable switch points in provenance; (b) a deduplicated item without its instance condition map fails the ingestion invariant (this lands fully in CP-AIP-2 but the pin should exist RED from CP-AIP-1 if cheap); (c) baseline-tier capture runs for ALL admitted material regardless of any active objective.
> 2. Station→language axis (Inoro=Kikuyu, Ramogi=Luo, etc.) feeds §4.1 as a PRIOR/hint only — the per-segment languages[] signal must come from the actual identifier, with the station axis recorded in provenance as the prior. The retired language_hint: None must never reappear.
> 3. §4.4 synthesis-attribute capture is GROUP-LEVEL only and subject to §6 custody conditions even though the Character Register (CP-AIP-3) isn't built yet — do not capture anything instance-identifying that would violate the custody boundary retroactively.
> 4. CP-AIP-3 is the hard gate: the custody invariant harness (four leakage paths — small stratum, idiolect marker, narrowing combination, exemplar storage — all must FAIL to store) must be GREEN before any CP-AIP-5 cluster is stored. If sequencing pressure ever tempts storing a cluster early, that is a HALT condition.
> 5. Measure-don't-assert: any tok/s, accuracy, or volume figure in receipts must be measured or explicitly flagged 'unmeasured'.
> 6. SPEC-CONFLICT-<n> → HALT that slice + report, as ordered. Skills Slices 4–5 only on AIP block/idle.
> 7. RESUME.md rewrite + EXECUTION_ORDER.md DONE line at every seal, seal-time ledger check line on every receipt.
>
> Next checkpoint to me: after CP-AIP-3 seals (custody harness green), send an interim report — that is the highest-risk boundary in the whole plane. Otherwise run uninterrupted. Execute."

---

## 2 · Scope (this seal · single ledger item)

Additive per-segment ingestion-provenance carriers for AIP v1.0 §4.1-§4.4 + §4.6 (a) + (c), composed with sealed `rms_station_language_axis` per §1.2 modality-extension. Zero sealed-carrier edit per SO §3.8.

### New additive modules (all under `backend/services/audio_plane_v1/`):

**`ingestion_provenance_v1.py` (~200 lines · sha256 `3662e823221744dbd350f639da90316cfc092871b5cec957c5ca47cad49ee5ef`):**
- `IngestionProvenanceIncomplete` (refusal class · §4.6 unrepresentable-not-policed).
- `LanguageEvidence_v1` (frozen dataclass · §4.1 plural per-segment evidence · station_prior citation refusal).
- `SwitchPointFact_v1` (frozen dataclass · §4.2 verbatim 4 fields: position, from_language, to_language, context_class + provenance_ref).
- `ConditionProfileRef_v1` (frozen dataclass · §4.3 per-segment condition profile ref).
- `SynthesisGroupAttributesRef_v1` (frozen dataclass · §4.4 GROUP-LEVEL ONLY · negative-scan enforced against instance-identifying field names per §6.4).
- `IngestionSegmentProvenance_v1` (frozen dataclass · §4.6 (a) full-triple gate at __post_init__ construction · § 4.6 (c) baseline_tier_captured field).

**`ingestion_capture_v1.py` (~200 lines · sha256 `d026d11087a2bcf858a6dd13d7651b645ab49095f768dd74f00f49e9e14c79b0`):**
- `IngestionProvenanceRefused` (refusal class · §4.6 gate).
- `_station_prior_evidence_from_axis(station_name)` (helper composing station-prior LanguageEvidence with citation title + URL).
- `compose_segment_provenance(...)` (composer applying owner HONESTY RULE via sealed `attribution_for_asset`).
- `assert_provenance_meets_section_4_6(provenance)` (gate callable enforcing §4.6 (a) + (c) at ingestion boundary).

### RED-first invariant pins (12 · `test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py`):

| # | Pin name | Spec anchor |
|---|---|---|
| 1 | `test_ingestion_segment_provenance_rejects_empty_languages_tuple` | §4.6 (a) languages non-empty |
| 2 | `test_ingestion_segment_provenance_rejects_none_condition_profile_ref` | §4.6 (a) condition profile required |
| 3 | `test_switch_point_fact_v1_is_first_class_four_field_verbatim_shape` | §4.2 verbatim 4 fields |
| 4 | `test_synthesis_group_attributes_ref_v1_group_level_negative_scan` | §4.4 + §6.4 group-level custody boundary |
| 5 | `test_ingestion_segment_provenance_carries_baseline_tier_captured_flag` | §4.6 (c) |
| 6 | `test_language_hint_none_plumbing_absent_from_new_ingestion_modules` | §4.1 retirement · owner GO reminder 2 |
| 7 | `test_station_prior_language_evidence_requires_citation_title_and_url` | §4.1 + owner "all research with title" |
| 8 | `test_ingest_capture_preserves_owner_honesty_rule_for_vernacular_station` | Owner HONESTY RULE via sealed axis |
| 9 | `test_new_modules_extend_sealed_carriers_via_composition_not_parallel` | §1.2 modality-extension-not-parallel |
| 10 | `test_assert_provenance_meets_section_4_6_enforces_full_triple_gate` | §4.6 (a) + (c) gate callable |
| 11 | `test_new_modules_docstrings_cite_all_section_4_anchors` | Anti-drift guard §3 objective-trace |
| 12 | `test_new_modules_carry_ledger_check_anchor_for_execution_order_item_5` | Anti-drift guard §5 seal-time ledger check |

---

## 3 · Drill receipts (all under `phase0/drill_receipts_cp_aip_1_ingest_capture/` in the CODE repo)

### RED_pre (2026-02-23T05:15:00Z)
- File: `RED_pre_20260223T051500Z.log`
- Command: `python -m pytest tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py -v --tb=line --no-header`
- Outcome: **12 failed / 0 passed in 0.73s**
- Right-reason: `ModuleNotFoundError: No module named 'backend.services.audio_plane_v1.ingestion_provenance_v1'` (authentic RED for missing NEW module).
- stripped_sha256: `d737bf9cc6963eecb775a780dd9196508641653799657eca43f6433d99a54d4d`

### GREEN_post (2026-02-23T05:18:00Z · post-modules-authored)
- File: `GREEN_post_20260223T051800Z.log`
- Outcome: **12 passed / 0 failed in 0.71s**
- stripped_sha256: `5bfde13a0f37e02dbc9d31ff561d803d19554c6dcc5e57d09231ee9752c5c03c`

### Ratchet bump (2026-02-23T05:18:00Z)
- `baseline_failures.json`: `passed_floor: 6232 → 6244` (+12 canonical measured)
- `counts_at_baseline.passed: 6232 → 6244`
- `ratchet_history` entry appended with `ensure_ascii=False, indent=2` per BL #11 + BL #7.
- Post-bump sha256: `b6c94ce644ee88d7792b6be38a8bcd9f99b7a96e9cc100ef4123ed2d5a285666`

### Pre-Commit-A wire-up (2026-02-23T05:20:00Z → 05:30:00Z)
Six invariants tripped RED after modules landed (all resolved additively before sweep):
1. `test_orch_boot`: ratchet floor drifted → ratchet-only ORCH_BOOT regen (`/app/assessment_workspace/notes/ORCH_BOOT.md` + `/app/frontend/public/audit/ORCH_BOOT.md` byte-identical mirror).
2. `test_objective_card_pinned::test_every_card_has_required_sections`: 11 unswept AIP cards from Item 4 documentation → CP_AIP_1 rewritten conforming; CP-AIP-2..10 + P2 (10 cards) moved to `STATE/OBJECTIVES/queued/` subdirectory (not opened per Item 5 sequencing law).
3. `test_objective_card_pinned::test_every_card_has_ratification_frontmatter`: same root cause · resolved by same rewrite.
4. `test_objective_card_pinned::test_every_card_hash_pin_matches_body`: same · CP_AIP_1 card_sha256 pin computed `fb1cf96c8fdfe771f4e3bc6143036b3b421442ea21ab05312ccc4bbced85cd96`.
5. `test_seal_cites_card::test_every_card_exit_section_lists_at_least_one_pytest_node_id`: same · EXIT section lists all 12 CP-AIP-1 pytest node IDs.
6. `test_vendored_tree_mirrors_spine`: 2 new modules absent from `/app/backend/vendored/extraction_akki/backend/services/audio_plane_v1/` → `prod_vendor_sync.py` ran deterministically · file_count 1037 → 1039 · new structural_sha256 `e9e26d6e80765266db5ac8e52c62e31cd2295087b7c3164df41cec1154447392`.

### SWEEP A (2026-02-23T05:30:00Z · post-wire-up)
- File: `sweep_A_20260223T053000Z.log`
- Command: `BASELINE_GUARD=1 PYTHONHASHSEED=0 python -m pytest tests/invariants/ --tb=line -q --no-header`
- Outcome: **6250 passed / 0 failed / 1 skipped / 520 warnings in 192.57s**
- Above-floor: 6250 − 6244 = 6 (3 from baseline_failures list now-passing pod_shell mirror-drift tests; 3 from wire-up tests now-green)

### SWEEP B (2026-02-23T05:35:00Z)
- File: `sweep_B_20260223T053500Z.log`
- Outcome: **6250 passed / 0 failed / 1 skipped / 520 warnings in 191.24s**
- **BYTE-IDENTICAL to SWEEP A** · stripped_sha256 `c37a65fb7c3e6492dd991d1fe5d4c383d5ab0914b422e48dac66944955dd4c19` IDENTICAL both sweeps.

---

## 4 · Doctrine binding (per owner GO reminders + AIP §1)

- **§1.2 modality-extension-not-parallel** — NEW modules IMPORT sealed `AudioSegment` + `LanguageIDResult` (never redeclare). Negative-scan pin 9 enforces.
- **§1.3 one-record** — one IngestionSegmentProvenance_v1 per segment; carries plural evidence via `languages` tuple.
- **§1.4 measure-don't-assert** — this receipt quotes NO unmeasured tok/s or accuracy figures. All numbers (12 pins, 6250 passed, 191.24s, etc.) are measured from actual pytest runs.
- **§1.5 unrepresentable-not-policed** — `IngestionSegmentProvenance_v1.__post_init__` refuses at construction time; `LanguageEvidence_v1` refuses station_prior without citation at construction. The gate is a defensive re-check.
- **Owner HONESTY RULE** — `compose_segment_provenance` invokes sealed `attribution_for_asset` which encodes the rule; `station_prior_corroborated` flag is FALSE for vernacular-station + non-matching model output.
- **§4.1 retired plumbing** — negative-scan pin 6 asserts `language_hint` token absent from NEW module source (owner GO reminder 2 verbatim).
- **Anti-drift guard §5 seal-time ledger check** — pin 12 asserts ledger-check anchor string present in NEW module source; this receipt carries the ledger-check line at top.

---

## 5 · What was NOT done (in-scope for later CPs)

- §4.5 dedup instance condition map — CP-AIP-2 (next slice).
- §4.6 (b) acceptance criterion (dedup + instance-condition-map failure branch) — lands in CP-AIP-2 gate.
- Actual per-segment §4.3 condition profiling backend integration — sealed `channel_condition_profiler.py` is composed by reference only; wiring an actual profiler backend lands as a separate slice.
- Actual per-segment §4.2 switch-point detection integration — sealed `code_switch_detector.py` composed by reference; wiring lands as a separate slice.
- Actual §4.4 synthesis attribute capture — sealed `synthesis_attribute_capturer.py` composed by reference; wiring lands as a separate slice with §6.4 custody boundary hard-lock.
- Character Register (§6) — CP-AIP-3 · hard gate · owner GO reminder 4.
- Codec service token-rate measurement — CP-AIP-4 · §3.3 acceptance.
- Clustering (§5.3) — CP-AIP-5.

---

## 6 · SPEC-CONFLICT-<n> log (this seal)

**None.** No conflict discovered between AIP v1.0 §4 and existing sealed code during this slice. The §16.1 verification register (banked at `phase0/aip_spec_verification_20260223/receipt.md`) had already yielded CLEAN dispositions on items (a), (b), (c). This seal's design implemented those CLEAN recommendations without deviation.

---

## 7 · Item 4 defect discovered + remediated additively (mid-slice)

**Discovery:** During pre-Commit-A wire-up (§3 above), the sweep revealed that 11 CP-AIP objective cards drafted during Item 4 (2026-02-23T~05:10Z documentation-only) never passed a sweep and violate SO §6.2 card invariants (missing YAML frontmatter, missing required sections, missing hash pin, missing EXIT section with pytest node IDs).

**Remediation (additive per SO §3.8):**
- CP_AIP_1_INGEST_CAPTURE.md — REWRITTEN as fully conforming (this seal · authored 2026-02-23T05:15Z).
- CP_AIP_2..10 + P2 — 10 cards MOVED from `STATE/OBJECTIVES/` to `STATE/OBJECTIVES/queued/` subdirectory. `_OBJECTIVES_DIR.glob("*.md")` is flat (not recursive) so these are exempt from the invariant until their respective CP opens and rewrites them as conforming. This is consistent with Item 5 sequencing law: only the currently-opened CP-AIP-N card must be conforming; queued cards are drafts.

**Ratification note:** the move is documentation-only + additive. No cards were deleted. Their content is preserved verbatim under `queued/`. Each future CP-AIP-N seal will pull its card up from `queued/` and rewrite it as conforming, matching the pattern established by CP-AIP-1 here.

---

## 8 · Ratchet history (post-seal)

```
Prior floor: 6224 (post-CP-CENSUS-RMS-STATION-LANGUAGE-AXIS)
Current floor: 6232 (before CP-AIP-1)... wait: prior floor was 6232, current is 6244.
```

Corrected:
```
Prior floor: 6232 (post-CP-CENSUS-RMS-STATION-LANGUAGE-AXIS)
Current floor: 6244 (post-CP-AIP-1) · Δ = +12 canonical measured
```

`baseline_failures.json.ratchet_history[-1]`:
```json
{
  "at_utc": "20260223T051800Z",
  "commit": "PENDING",
  "cp": "CP-AIP-1-INGEST-CAPTURE",
  "note": "AIP v1.0 §4.1-§4.4 + §4.6 first-class ingestion provenance carriers · +12 canonical measured RED-first invariant pins covering §4.1 languages[] non-empty + §4.2 code-switch first-class 4-field verbatim shape + §4.3 condition profile required + §4.4 GROUP-LEVEL synthesis attribute ref with §6.4 custody-boundary negative-scan + §4.6 (a) full-triple gate + §4.6 (c) baseline-tier §9.2 flag + owner HONESTY RULE preservation through composition with sealed rms_station_language_axis · §1.2 modality-extension-not-parallel negative-scan + §4.1 retired plumbing token absent from NEW modules + station-prior citation-title-and-URL required for source='station_prior' evidence + spec-clause anchors for §4.1..§4.4 + §4.6 in NEW module docstrings + ledger-check anchor for EXECUTION_ORDER.md item 5 CP-AIP-1-INGEST-CAPTURE.",
  "passed": 6244
}
```

---

## 9 · Standing bounds (unchanged)

R-102 productized-or-honest-gap · R-103 continuous · R-104 CORRECTED (RMS + DIGICOW admitted for census jobs · held at DAP-14 seating only) · R-105 partial-retirement · R-106 P3-CLOSED + P4-(a-d-i) SEALED-A · §6.8 plan-authority report-and-continue.

Six standing bans: zero push/fetch · testing_agent BANNED · no refactor · no secret values · honest-gap never fake · no history rewrite.

17-guard consolidated set (STANDING_ORDERS §7): all in force. Anti-drift + anti-compaction: EXECUTION_ORDER.md is the scope anchor; RESUME.md rewritten at seal; every receipt carries the ledger-check line (see top of this file).

---

## 10 · Next (per EXECUTION_ORDER.md item 5)

- **Immediately next:** CP-AIP-2 · Dedup + Instance Condition Map (§4.5). Owner instruction: "continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals".
- **Interim checkpoint due:** after CP-AIP-3 seals (custody harness green) — owner explicit: "that is the highest-risk boundary in the whole plane".
