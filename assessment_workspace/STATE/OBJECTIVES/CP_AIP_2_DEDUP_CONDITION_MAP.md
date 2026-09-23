---
card_id: CP_AIP_2_DEDUP_CONDITION_MAP
title: AIP v1.0 §4.5 + §4.6 (b) · dedup instance-condition-map provenance carriers · Item 5.2 CP-AIP-2
ratified_at_utc: 2026-02-23T06:00:00Z
ratified_by: Owner GO at Item 4 checkpoint (2026-02-23 · verbatim 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals').
card_sha256: b5b86c6a5aefba1a86f95cfd1b9d7894ceb9e4d88bc5f193808767b875e006b6
milestone_status: OPEN (Item 5.2 CP-AIP-2 · in-flight for this seal)
---

# CP-AIP-2-DEDUP-CONDITION-MAP · AIP v1.0 §4.5 + §4.6 (b) Dedup Instance-Condition-Map Provenance

## OBJECTIVE

Land the additive dedup-instance provenance carriers extending CP-AIP-1 (via §1.2 modality-extension) with sealed CP-M6-2-1 `InstanceConditionMap` composition, enforcing AIP v1.0 §4.5 (dedup as augmentation · one canonical extraction stored · variant set → robustness stratum at zero acquisition cost) and §4.6 (b) acceptance criterion (a deduplicated item without its instance condition map fails the ingestion invariant test). Zero sealed-carrier edit per SO §3.8. `canon_ref: AIP v1.0 §4.5 + §4.6 (b) + §1.2 modality-extension + §1.5 unrepresentable-not-policed.`

CP-AIP-1 previously deferred §4.6 (b) to this slice per owner GO reminder 1 (b) verbatim. This seal closes that deferral.

## MUST DO

1. **§4.5 InstanceConditionMap composition (not redeclaration)** — the NEW `DedupInstanceProvenance_v1` wraps the sealed `InstanceConditionMap` (CP-M6-2-1) via an `instance_condition_map` field. §1.2 modality-extension via import; no parallel redeclaration. `canon_ref: AIP §4.5 verbatim + §1.2.`

2. **§4.5 canonical-vs-variant Literal type** — `DedupInstanceProvenance_v1.dedup_role` is typed as `Literal["canonical", "variant"]` encoding §4.5 verbatim "One canonical extraction is stored; the variant set enters training curricula" distinction structurally. `canon_ref: AIP §4.5 verbatim.`

3. **§4.5 RobustnessStratumTag_v1 with zero_acquisition_cost=True** — `RobustnessStratumTag_v1` frozen dataclass carries §4.5 verbatim provenance ('designated robustness stratum at zero acquisition cost'). Construction refuses `zero_acquisition_cost=False` per §1.5 unrepresentable-not-policed. `canon_ref: AIP §4.5 verbatim.`

4. **§4.6 (b) gate callable using sealed helper** — `assert_dedup_provenance_meets_section_4_6_b(item)` invokes sealed `dedup_item_has_instance_condition_map(item)` from CP-M6-2-1 to enforce §4.6 (b) verbatim. Uses sealed helper rather than redoing the check parallel-fashion. `canon_ref: AIP §4.6 (b) verbatim + §1.2.`

5. **CP-AIP-1 base_provenance composition** — `DedupInstanceProvenance_v1.base_provenance` is typed as sealed `IngestionSegmentProvenance_v1` (CP-AIP-1 · sealed this-session). §1.2 composition, not redeclaration. `canon_ref: AIP §1.2 + CP-AIP-1 seal record.`

6. **10 RED-first pytest invariants** — RED_pre 10/10 failed → GREEN_post 10/10 passed. Each pin cites the exact §4.5 or §4.6 (b) or §1.2 spec anchor it enforces. `canon_ref: SO §3 RED-first + Anti-drift standing guard §3.`

7. **Ratchet floor 6244 → 6254** — +10 canonical measured pins · `ensure_ascii=False, indent=2` per BL #11 + BL #7 · ratchet_history entry appended. `canon_ref: SO §3 no-silent-rebaselining + BL #6/7/11.`

8. **5-commit seal on dual branches + /app companion** — same shape as CP-AIP-1 seal. Terminal `pytest` only. BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green byte-identical stripped_sha256. `canon_ref: SO §3.3 5-Commit-Seal + SO §7 guard 6.`

## MUST NOT

- Edit any sealed §4.5 carrier (`instance_condition_map.py`, `dedup_path.py`) or the CP-AIP-1 sealed carriers (`ingestion_provenance_v1.py`, `ingestion_capture_v1.py`). `canon_ref: SO §3.8 additive-only.`

- Redeclare sealed `InstanceConditionMap`, `InstanceConditionVariant`, `IngestionSegmentProvenance_v1`, or `LanguageEvidence_v1` (parallel-machinery ban). `canon_ref: AIP §1.2 verbatim.`

- Reimplement the §4.6 (b) attribute-existence check parallel-fashion — MUST invoke sealed `dedup_item_has_instance_condition_map(item)`. `canon_ref: AIP §1.2 + BL #4.`

- Accept `zero_acquisition_cost=False` on a `RobustnessStratumTag_v1` (§4.5 verbatim requires zero acquisition cost). `canon_ref: AIP §4.5 verbatim + §1.5.`

- Quote unmeasured tok/s or accuracy figures in the seal receipt. `canon_ref: AIP §1.4 measure-don't-assert.`

- Sprawl beyond the ledger item — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-2-DEDUP-CONDITION-MAP and nothing else. `canon_ref: SO §7 guard 5.`

## EXIT

**10 RED-first invariants (RED_pre 10/10 failed · GREEN_post 10/10 passed · authored under this seal · continue verbatim GREEN post-Commit-A):**

- tests/invariants/test_cp_aip_2_dedup_condition_map_aip_v1_0_section_4_5.py::test_dedup_instance_provenance_requires_non_empty_variants
- tests/invariants/test_cp_aip_2_dedup_condition_map_aip_v1_0_section_4_5.py::test_dedup_instance_provenance_dedup_role_is_canonical_or_variant
- tests/invariants/test_cp_aip_2_dedup_condition_map_aip_v1_0_section_4_5.py::test_robustness_stratum_tag_carries_zero_acquisition_cost_flag
- tests/invariants/test_cp_aip_2_dedup_condition_map_aip_v1_0_section_4_5.py::test_assert_dedup_provenance_gate_refuses_missing_instance_condition_map
- tests/invariants/test_cp_aip_2_dedup_condition_map_aip_v1_0_section_4_5.py::test_assert_dedup_provenance_gate_accepts_wellformed_item
- tests/invariants/test_cp_aip_2_dedup_condition_map_aip_v1_0_section_4_5.py::test_dedup_capture_composes_sealed_instance_condition_map_constructor
- tests/invariants/test_cp_aip_2_dedup_condition_map_aip_v1_0_section_4_5.py::test_new_modules_do_not_redeclare_sealed_dedup_carriers
- tests/invariants/test_cp_aip_2_dedup_condition_map_aip_v1_0_section_4_5.py::test_assert_gate_uses_sealed_dedup_item_helper
- tests/invariants/test_cp_aip_2_dedup_condition_map_aip_v1_0_section_4_5.py::test_dedup_instance_provenance_composes_cp_aip_1_ingestion_provenance
- tests/invariants/test_cp_aip_2_dedup_condition_map_aip_v1_0_section_4_5.py::test_new_modules_cite_section_4_5_and_ledger_check_anchor

**Baseline ratchet monotonic-up under BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep:**
- passed_floor 6244 → 6254 (+10 canonical measured)
- baseline_failures list unchanged
- both sweeps byte-identical stripped_sha256 (to be pinned in the Commit-A receipt)

## STOP

Stop at 5-commit seal landing. Do NOT proceed into CP-AIP-3 in the same seal — CP-AIP-3 is the HARD GATE per owner GO reminder 4 and requires a distinct seal AND an interim owner report post-close.

If a SPEC-CONFLICT is discovered between the code being written and AIP v1.0 §4.5 / §4.6 (b), HALT the slice, log it in DECISIONS.md as SPEC-CONFLICT-<n>, and report. `canon_ref: STATE/EXECUTION_ORDER.md anti-drift §3.`

## ANCHORS

**Spec anchors (AIP v1.0):**
- §4.5 dedup as augmentation (V50 verbatim on line 122 of `Audio_Intelligence_Plane.md`).
- §4.6 (b) acceptance criterion (V52 verbatim on line 128).
- §15 P230 build sequence: 'Dedup instance condition map (§4.5) — Contract change to existing machinery; near-zero new detection work.'
- §1.2 modality extension, not parallel machinery.
- §1.5 unrepresentable, not policed.

**Owner directives (verbatim):**
- Item 4 GO (2026-02-23): 'continue sequentially CP-AIP-2 → CP-AIP-10 without pausing between seals'.
- GO reminder 1 (b) verbatim: 'a deduplicated item without its instance condition map fails the ingestion invariant (this lands fully in CP-AIP-2 but the pin should exist RED from CP-AIP-1 if cheap)'.

**Sealed carriers composed (UNCHANGED per SO §3.8):**
- `backend/services/audio_plane_v1/instance_condition_map.py` (CP-M6-2-1 · §4.5 schema + constructor + gate helper).
- `backend/services/audio_plane_v1/dedup_path.py` (CP-M6-2-2 · sealed).
- `backend/services/audio_plane_v1/ingestion_provenance_v1.py` (CP-AIP-1 · sealed this-session).
- `backend/services/audio_plane_v1/ingestion_capture_v1.py` (CP-AIP-1 · sealed this-session).

**New additive modules landed by this seal:**
- `backend/services/audio_plane_v1/dedup_instance_provenance_v1.py` (~110 lines · RobustnessStratumTag_v1 + DedupInstanceProvenance_v1 + DedupInstanceProvenanceIncomplete refusal · §1.5 __post_init__ gates).
- `backend/services/audio_plane_v1/dedup_capture_v1.py` (~95 lines · compose_dedup_instance_provenance composer + assert_dedup_provenance_meets_section_4_6_b gate callable + DedupInstanceProvenanceRefused refusal class).

**Standing Orders anchors:**
- SO §3 RED-first · SO §3.3 5-Commit Seal · SO §3.8 additive-only · SO §4 product-language · SO §6.2 objective-card shape + hash-pin · SO §7 17-guard consolidated set · STATE/EXECUTION_ORDER.md anti-drift §3 + §5.

**Ledger check:** this seal implements EXECUTION_ORDER.md item 5 CP-AIP-2-DEDUP-CONDITION-MAP and nothing else.
