---
card_id: CP_AIP_1_INGEST_CAPTURE
title: AIP v1.0 §4.1-§4.4 + §4.6 · first-class ingestion provenance carriers · Item 5 CP-AIP-1
ratified_at_utc: 2026-02-23T05:15:00Z
ratified_by: Owner GO at Item 4 checkpoint (2026-02-23 · post-CP-AIP-SPEC-INGEST · verbatim 'GO. Respond in English only. The owner pre-approved this exact order and the §16.2 working defaults - no reorder, no revision. Proceed with CP-AIP-1 · Ingest & Capture exactly as proposed').
card_sha256: fb1cf96c8fdfe771f4e3bc6143036b3b421442ea21ab05312ccc4bbced85cd96
milestone_status: OPEN (Item 5 CP-AIP-1 · in-flight for this seal)
---

# CP-AIP-1-INGEST-CAPTURE · AIP v1.0 §4.1-§4.4 + §4.6 First-Class Ingestion Provenance

## OBJECTIVE

Land the additive per-segment ingestion-provenance carriers required by AIP v1.0 §4.1-§4.4 and enforced by §4.6 acceptance criteria (a) + (c), composed via `services/rms_station_language_axis.py` station-prior + owner HONESTY RULE, without editing any sealed carrier per SO §3.8 additive-only. `canon_ref: AIP v1.0 §4.1-§4.6 + §1.2 modality-extension-not-parallel + §1.5 unrepresentable-not-policed + owner GO verbatim 2026-02-23 post-Item-4-checkpoint.`

Everything downstream (§5 clustering, §6 character register, §8 objective wizard, §10 planner, §11 sampling+milestones, §13 commission view) consumes the shapes this CP lands. Per AIP §15 verbatim: "Everything downstream consumes these; only cheap at first ingestion. Deferral cost is a full re-pass over the estate."

## MUST DO

1. **§4.1 languages[] plural + station-prior discipline** — the new `LanguageEvidence_v1` carrier expresses `languages[]` plural via a Tuple of evidence entries with `source ∈ {"detected", "station_prior", "code_switch"}`. The per-segment `languages[]` signal comes from the actual identifier; station axis is recorded in provenance as the prior. Retired plumbing value `language_hint: None` MUST NEVER reappear in NEW modules — negative-scan enforced. `canon_ref: AIP §4.1 verbatim + owner GO reminder 2 verbatim.`

2. **§4.2 code-switch points as first-class facts** — `SwitchPointFact_v1` frozen dataclass carries the four §4.2 verbatim fields (position, from-language, to-language, context class) plus a provenance_ref binding the fact to its originating segment/position. Facts, not preprocessing metadata. `canon_ref: AIP §4.2 verbatim.`

3. **§4.3 condition profile required at ingestion** — `ConditionProfileRef_v1` binds a per-segment condition profile (studio / field / telephone band caller-defined open str) to a segment via a reference-shape carrier; audio bytes never cross the shape per pull-seam discipline. `canon_ref: AIP §4.3 verbatim.`

4. **§4.4 GROUP-LEVEL synthesis attribute capture with §6.4 custody-boundary** — `SynthesisGroupAttributesRef_v1` declares GROUP-LEVEL fields only (pitch_statistics_ref, energy_contour_ref, duration_pattern_ref, custody_boundary_class); negative-scan bans any instance-identifying field name (idiolect_marker, speaker_id, character_id, voiceprint, biometric_embedding, exemplar). §6.4 custody boundary unrepresentable-by-construction on the group-level ref shape per §1.5. `canon_ref: AIP §4.4 + §6.4 + owner GO reminder 3 verbatim.`

5. **§4.6 full-triple gate at ingestion boundary** — `assert_provenance_meets_section_4_6` callable in `ingestion_capture_v1.py` refuses provenance missing any of §4.6 (a) required carriers (empty languages tuple, None condition_profile_ref) and refuses §4.6 (c) admitted material with `baseline_tier_captured=False`. §4.6 (b) dedup instance-condition-map branch lands in CP-AIP-2 per owner directive. `canon_ref: AIP §4.6 verbatim + §1.5 unrepresentable-not-policed.`

6. **§4.1 station-prior citation discipline** — every LanguageEvidence with `source="station_prior"` MUST carry non-empty `research_citation_title` AND `research_citation_url`; construction refuses either missing per owner "all research with title" directive banked in CP-CENSUS-RMS-STATION-LANGUAGE-AXIS. `canon_ref: owner directive verbatim (CP-CENSUS this-session · sealed carrier) + AIP §4.1.`

7. **Owner HONESTY RULE preserved through composition** — `compose_segment_provenance` invokes sealed `attribution_for_asset` from `rms_station_language_axis` to compute `station_prior_corroborated` flag; NEVER records model-output as station corroboration for a vernacular station (Kikuyu/Dholuo/Kalenjin/Kamba/etc.). `canon_ref: sealed MODEL_CORROBORATION_POLICY constant in rms_station_language_axis.py line 68 verbatim.`

8. **§1.2 modality-extension-not-parallel** — NEW modules import sealed `AudioSegment` + `LanguageIDResult` symbols via composition; MUST NOT redeclare any sealed carrier symbol. Negative-scan enforced. `canon_ref: AIP §1.2 verbatim.`

9. **RED-first pytest invariants + double-green ratchet** — 12 canonical measured RED-first pins under `test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py`; RED_pre 12/12 failed → GREEN_post 12/12 passed; BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep byte-identical; ratchet floor 6232 → 6244. `canon_ref: SO §3 RED-first + §3.3 5-Commit-Seal.`

10. **5-commit seal on dual branches + /app companion** — Code Commit-A on `programme/track-a` (in `/app/assessment_workspace/repos/Extraction-Akki`) + /app Commit-A companion on `main` (vendored twin sync of NEW modules + MANIFEST bump + ORCH_BOOT regen + gitlink) + State Commit-B on `master` (drill receipts + DECISIONS + RESUME rewrite + EXECUTION_ORDER DONE line) + State Commit-C fixup on `master` (R-6 boundary regen) + /app Commit-C companion on `main` (ORCH_BOOT post-fixup mirror sync). `canon_ref: SO §3.3 5-Commit-Seal + SO §7 guard 6.`

## MUST NOT

- Edit any sealed §4.1-§4.5 carrier (`language_identifier.py`, `channel_condition_profiler.py`, `code_switch_detector.py`, `synthesis_attribute_capturer.py`, `instance_condition_map.py`) or the sealed `rms_station_language_axis.py`. `canon_ref: SO §3.8 additive-only.`

- Redeclare sealed AudioSegment / LanguageIDResult / LanguageIDBackend symbols in the NEW modules (parallel-machinery ban). `canon_ref: AIP §1.2 verbatim.`

- Land any instance-identifying field name on the §4.4 group-level ref (idiolect_marker, speaker_id, character_id, voiceprint, biometric_embedding, exemplar, individual_identifier). `canon_ref: AIP §4.4 + §6.4 + owner GO reminder 3.`

- Reintroduce retired plumbing token `language_hint` in any NEW module. `canon_ref: AIP §4.1 + owner GO reminder 2.`

- Present model output as confirming a language whisper can't reliably detect (Kikuyu/Dholuo/Kalenjin/Kamba/etc.) for a vernacular RMS station. `canon_ref: sealed MODEL_CORROBORATION_POLICY verbatim + owner HONESTY RULE.`

- Quote unmeasured tok/s or accuracy figures in the seal receipt. Numbers land in Sampling & Reflection (§11.2 · CP-AIP-8). `canon_ref: AIP §1.4 measure-don't-assert.`

- Bypass RED-first doctrine (test author BEFORE module implementation). `canon_ref: SO §3.`

- Sprawl beyond the ledger item — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-1-INGEST-CAPTURE and nothing else. `canon_ref: SO §7 guard 5 + STATE/EXECUTION_ORDER.md anti-drift §5 verbatim.`

## EXIT

**12 RED-first invariants (RED_pre 12/12 failed · GREEN_post 12/12 passed · authored under this seal · continue verbatim GREEN post-Commit-A):**

- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_ingestion_segment_provenance_rejects_empty_languages_tuple
- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_ingestion_segment_provenance_rejects_none_condition_profile_ref
- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_switch_point_fact_v1_is_first_class_four_field_verbatim_shape
- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_synthesis_group_attributes_ref_v1_group_level_negative_scan
- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_ingestion_segment_provenance_carries_baseline_tier_captured_flag
- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_language_hint_none_plumbing_absent_from_new_ingestion_modules
- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_station_prior_language_evidence_requires_citation_title_and_url
- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_ingest_capture_preserves_owner_honesty_rule_for_vernacular_station
- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_new_modules_extend_sealed_carriers_via_composition_not_parallel
- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_assert_provenance_meets_section_4_6_enforces_full_triple_gate
- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_new_modules_docstrings_cite_all_section_4_anchors
- tests/invariants/test_cp_aip_1_ingest_capture_aip_v1_0_section_4.py::test_new_modules_carry_ledger_check_anchor_for_execution_order_item_5

**Baseline ratchet monotonic-up under BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep:**
- passed_floor 6232 → 6244 (+12 canonical measured)
- baseline_failures list unchanged (still the 3 pod_shell mirror-drift entries)
- both sweeps byte-identical stripped_sha256 (to be pinned in the Commit-A receipt per BL #11)

## STOP

Stop at 5-commit seal landing. Do NOT proceed into CP-AIP-2 in the same seal — CP-AIP-2 is a separate slice per EXECUTION_ORDER.md item 5 sequencing law (each CP-AIP-N gets its own 5-commit seal).

Do NOT cross into CP-AIP-3 territory (character register + custody harness) — that is the hard-gate slice per owner GO reminder 4 and MUST be a distinct seal.

Do NOT open any CP-AIP-2..10 card in this seal — those cards remain in `STATE/OBJECTIVES/queued/` until their respective CP opens.

If a SPEC-CONFLICT is discovered between the code being written and AIP v1.0 §4, HALT the slice, log it in DECISIONS.md as SPEC-CONFLICT-<n>, and report — do not improvise. `canon_ref: STATE/EXECUTION_ORDER.md anti-drift standing guard §3 verbatim.`

## ANCHORS

**Spec anchors (AIP v1.0):**
- §4.1 language identification (V44 verbatim on line 98 of `Audio_Intelligence_Plane.md`).
- §4.2 code-switch points as facts (V45 verbatim on line 110).
- §4.3 condition profiling (V46 verbatim on line 114).
- §4.4 synthesis-relevant attribute capture (V49 verbatim on line 118).
- §4.6 acceptance criteria (V52 verbatim on line 124).
- §1.2 modality extension, not parallel machinery.
- §1.5 unrepresentable, not policed.
- §15 build sequence: "Ingestion capture - language ID, code-switch points, condition profile, synthesis attributes (§4.1-§4.4)".

**Owner directives (verbatim · banked at STATE/DECISIONS.md):**
- HONESTY RULE (CP-CENSUS this-session): 'whisper-class models do NOT reliably distinguish Kikuyu/Luo/Kalenjin/Kamba etc. - where the model cant corroborate, the attribution is station-prior (cited), model-corroboration: unavailable - never present model output as confirming a language it cant detect. Where model says Swahili/English it corroborates those stations only.'
- All research with title (CP-CENSUS this-session): 'all research with title'.
- Item 4 GO (2026-02-23 · post-checkpoint): 'GO... Proceed with CP-AIP-1 · Ingest & Capture exactly as proposed'.
- GO reminders 1..7 (2026-02-23 · verbatim in the GO message): (1) §4.6 verbatim acceptance; (2) station-prior discipline + retired plumbing never reappears; (3) §4.4 GROUP-LEVEL + §6 custody; (4) CP-AIP-3 hard gate; (5) measure-don't-assert; (6) SPEC-CONFLICT halt; (7) RESUME + EXECUTION_ORDER + ledger-check line.

**Sealed carriers composed (UNCHANGED per SO §3.8):**
- `backend/services/audio_plane_v1/language_identifier.py` (CP-M6-1-1)
- `backend/services/audio_plane_v1/channel_condition_profiler.py` (CP-M6-1-3)
- `backend/services/audio_plane_v1/code_switch_detector.py` (CP-M6-1-2)
- `backend/services/audio_plane_v1/synthesis_attribute_capturer.py` (CP-M6-1-4)
- `backend/services/audio_plane_v1/instance_condition_map.py` (CP-M6-2-1 · §4.5)
- `backend/services/rms_station_language_axis.py` (CP-CENSUS-RMS-STATION-LANGUAGE-AXIS)

**New additive modules landed by this seal:**
- `backend/services/audio_plane_v1/ingestion_provenance_v1.py` (~200 lines · 5 carrier dataclasses + 1 refusal class).
- `backend/services/audio_plane_v1/ingestion_capture_v1.py` (~200 lines · station-prior composer + §4.6 gate).

**Standing Orders anchors:**
- SO §3 RED-first doctrine.
- SO §3.3 5-Commit Seal protocol.
- SO §3.8 additive-only.
- SO §4 product-language discipline.
- SO §6.2 objective-card shape + hash-pin invariants.
- SO §7 consolidated 17-guard set.
- STATE/EXECUTION_ORDER.md anti-drift §3 objective-trace guard + §5 seal-time ledger-check line.

**Ledger check:** this seal implements EXECUTION_ORDER.md item 5 CP-AIP-1-INGEST-CAPTURE and nothing else.
