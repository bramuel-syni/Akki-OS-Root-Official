# AIP Spec v1.0 · §16.1 Verification Register Receipts · 2026-02-23T05:00:00Z

**Owner drop context**: AIP Spec v1.0 supersedes Audio Capability Spec v1.0 + Addendum v1.1.2. Single build reference for the audio plane.

**Method**: read-only investigation against current sealed code at HEAD `832bdf25b681d717fdb0fb25b6710078392c8909` (CP-CENSUS-RMS-STATION-LANGUAGE-AXIS · Commit-A · programme/track-a). No code change this-pass — investigation only.

**Ledger check** — this receipt implements EXECUTION_ORDER.md item 4 sub-step §16.1 and nothing else.

---

## §16.1 (a) — Perception router contract (§3.2)

**Question:** *Where does model registration occur, and does the router carry a second output stream per segment or does the character stream need its own artifact type?*

### Findings

**Model registration location**: `backend/services/perception/model_registry.py`.

- Provides `current_registry_version()`, `load_registry(kind)`, `attest_model(model_id)`, and `register_model(model_id, entry)`.
- Uses **additive versioning**: `models_registry.v(N).json` → `models_registry.v(N+1).json` (append-only per SO §3.8).
- Currently at v0 (`models_registry.v0.json`) seeded with `whisper-tiny` CI fixture (weights_sha256 pinned, MIT-licensed).
- Owner ruling 9.2a-E1 α verbatim carrier at module docstring: production models land additively at 9.2b via v0→v1 registry bump.

**Router surface**: `backend/services/synisense/shield/perception_router.py`.

- Currently extends Shield to ASR / vision modalities with a **single per-segment output stream** (line 85 reads `"language_hint": None`).
- Mints a **perception trust receipt** per call (via `trust_receipt.build_trust_receipt` cousin pattern).
- Falls back to deterministic `synthetic_plumbing_only=True` stub when live provider absent.
- **~200 LoC budget guard** at module top (Rule 2). Router is a lean seam, not a stream-multiplexer.

**§3.2 P047 codec output shape** already lands at `services/perception/audio_codec/artefact.py`:

```
CodecArtefact — frozen 3-carrier dataclass:
  content_tokens · character_stream · codec_version
```

The **character_stream field is already a first-class carrier** on the codec artefact, sealed at CP-M6-4-2. It has its own place in the output shape — it is NOT routed through a second per-segment stream in the router.

### Recommendation

**No new artifact type is needed for the character stream** — it is already a first-class field on `CodecArtefact` (§3.2 P047 verbatim). What IS needed:

1. **Perception router extension** (§3.2 P045 path `perception/audio_codec/`): a service registration for `audio_codec` in `perception/model_registry.py` (v0→v1 bump) so the codec is census-visible per §3.2 verbatim `"registered like any other perception model; census-visible; runs in-perimeter on tenant compute"`.
2. **Router downstream routing rule** (additive): when a codec produces its 2-stream output, the router must persist BOTH `content_tokens` (routing to ASR/NER path) AND `character_stream` (routing to Character Register write path). Neither may be dropped as noise.
3. **Character stream is already representable** — no new artifact type. The router's SINGLE output-stream shape at line 85 of `perception_router.py` is the **content-side** default; a new sibling helper (e.g., `perception_router.route_character_stream(...)`) can be added additively without editing the sealed content router path.

### Sealed carriers unchanged

- `services/perception/model_registry.py` unchanged (v0→v1 bump is additive per its own append-only doctrine).
- `services/perception/audio_codec/artefact.py` unchanged (already sealed with correct shape).
- `services/synisense/shield/perception_router.py` unchanged (SO §3.8 — extension goes to a new sibling helper).

**Rating**: **CLEAN — no artifact-type refactor needed. CP-AIP-4-CODEC-SERVICE can build additively on the existing seals.**

---

## §16.1 (b) — Ingestion segment boundaries (§4.1)

**Question:** *Confirm the exact unit a language label attaches to in current ingestion.*

### Findings

Current ingestion segment structures (grep-verified this-pass):

| Module | Class | Purpose | Language field |
|---|---|---|---|
| `services/perception/eab_1_pipeline/a1_vad.py:27` | `VADSegment` | Voice-activity detection output | — (VAD is pre-language) |
| `services/perception/eab_1_pipeline/a1_segmentation.py:37` | `BatchSegment` | Batch segmentation | — |
| `services/audio_plane_v1/language_identifier.py:70` | **`AudioSegment`** | **Canonical audio segment for language ID** | **canonical carrier** |
| `services/audio_plane_v1/corpus_deliverable_v1.py:68` | `CorpusSegment_v1` | Downstream corpus row | — (composes AudioSegment upstream) |
| `services/audio_plane_v1/corpus_deliverable_v1_derivative.py:106` | `DerivativeSegment_v1` | Post-processed derivative | — |

**Canonical unit that a language label attaches to**: `services/audio_plane_v1/language_identifier.py:AudioSegment`.

The current `language_identifier.identify_language_per_segment(*, segments: Sequence[AudioSegment], ...) -> Tuple[AudioSegment, ...]` (line 158-159) is the canonical function per §4.1. `AudioSegment` is the unit.

**`language_hint` retirement status** (§4.1 P per verbatim *"The current plumbing value (language_hint: None) is retired."*):

- Still present as a field/plumbing value in:
  - `services/perception/diarization_worker.py:192` (`"language_hint": None`)
  - `services/synisense/shield/perception_router.py:85` (`"language_hint": None`)
  - `services/perception/asr_worker.py:236` (`"language_hint": "en"` — hardcoded)
  - `services/layer_b/contracts.py:43` (`language_hint: Optional[str] = None`)
  - `services/layer_b/asr/whisper_provider.py:36,51` (self._params dict + result read)
  - `services/data_source/synthetic.py:66` (synthetic fixture)
  - `services/d12_poc/receipt_contract.py:85,106` (receipt contract fields)

**Retirement work required** (for CP-AIP-1-INGEST-CAPTURE):

- Each `language_hint` plumbing site above must be additively wrapped by a new `languages_from_axis(segment, station_id) -> Tuple[str, ...]` helper that reads:
  - Station-prior from the just-sealed `services.rms_station_language_axis.RMS_STATION_LANGUAGE_AXIS` (this-session · Task 3).
  - Live segment-level language identifier output from `audio_plane_v1.language_identifier`.
- The wrapper adjudicates per the just-sealed HONESTY RULE (`attribution_for_asset`) — vernacular-station returns `model_corroboration=unavailable`; Swahili/English corroborated only when model matches AND whisper-corroboratable.
- **Sealed sites are NEVER edited** — new wrappers added, callers repointed as additive callers per SO §3.8.

### Recommendation

**Language label attaches to `services/audio_plane_v1/language_identifier.AudioSegment` — this is the canonical unit** per §4.1.

**Station-axis feed** (§4.1 verbatim `"routes downstream model selection ... written into provenance"`):

- New `services/audio_plane_v1/language_identifier_with_station_prior.py` (additive) wraps `identify_language_per_segment` with a station-prior + HONESTY RULE adjudicator using the just-sealed `RMS_STATION_LANGUAGE_AXIS` + `attribution_for_asset`.
- `languages[]` field on `AudioSegment` composes: station-prior (cited via research_citation_title/url) + model-detected + code-switch points per §4.1.

### Sealed carriers unchanged

- `services/audio_plane_v1/language_identifier.py` unchanged.
- `services/audio_plane_v1/corpus_deliverable_v1.py` unchanged.
- All 7 sites carrying `language_hint` plumbing unchanged (wrapped, not edited).

**Rating**: **CLEAN — canonical unit is `AudioSegment`. Wrapper approach for station-axis feed is fully additive.**

---

## §16.1 (c) — Wizard B-2/B-3 landing state (§8.5)

**Question:** *Assess extending existing shaping-wizard state machine with an objective variant OR standing a sibling machine on shared agent interface + ledger sidecar.*

### Findings

Current wizard state (grep-verified this-pass):

- **`services/wizard/operator_state_machine.py`** — B-2/B-3 landing exists (line 182: `Phase 7 Stage B-2 Condition A(i) landing (Owner ruling, 2026-07-04)`; line 93: `numeric content sharpens at B-3 admission handoff`).
- **`contracts/wizard_commit_state.py:WizardCommitState_v0`** — frozen carrier with `variant: Literal["operator", "buyer"]` (per `router_shims.py` line 52).
- **Existing wizard sub-modules**:
  - `agent_interface.py` — LLM-facing interface.
  - `admission_handoff.py` — handoff to downstream admission.
  - `connect_llm_router.py` — LLM routing seam.
  - `milestones.py` — milestone recorder.
  - `operator_state_machine.py` — main state machine (operator variant · buyer variant deprecated per `router_shims.py:19-23` byte-identical parity).
  - `router_shims.py` — B-2/B-3 router shim during evolution period.
  - `session_persistence.py` — Mongo persistence.
  - `source_tagging.py` — source-tagging seam.
  - `turn_ledger.py` — session-stamp ledger sidecar.

Existing wizard state machine ALREADY carries:

- Agent interface (agent_interface.py).
- Session persistence (session_persistence.py).
- Ledger sidecar (turn_ledger.py).
- Variant Literal on committed state (`WizardCommitState_v0.variant`).

### Recommendation

**Extend the existing state machine with an objective variant** — do NOT stand up a sibling machine.

Rationale:

1. **§1.2 modality-extension-not-parallel discipline** — AIP explicitly forbids sibling services. The Objective Wizard must be a variant of the existing shaping wizard, not a parallel machine.
2. **Existing seams are exactly the ones AIP §8.5 calls for**: agent interface, guards, session persistence, ledger sidecar. Sibling would duplicate all four.
3. **`WizardCommitState_v0.variant` Literal is already the extension point** — adding `"objective"` as a third Literal member (additively) is the minimal wire change. Frozen contract byte-identity is preserved by additive-append to a `Literal[...]` per Pydantic 2.13 emission semantics (verified pattern from prior contract snapshots).
4. **B-2/B-3 state transitions already exist** — the operator state machine's B-2 condition A(i) landing (line 182) and B-3 admission handoff (line 93) are the exact transitions the objective variant needs to reuse.

**Minimal build shape** for CP-AIP-6-OBJECTIVE-WIZARD:

- Additive `services/wizard/objective_state_machine.py` (new sibling FILE, shared machine — implements `state.variant == "objective"` branches).
- Additive `contracts/wizard_objective_commit_state_v0.py` (per §8.1: outputs `{TargetOutcome, CollectionSchema}`) — extension of `WizardCommitState_v0` shape, not replacement.
- Additive `contracts/target_outcome_v0.py` (§10.1 seven-field schema).
- Additive `contracts/collection_schema_v0.py` (§9 baseline + objective tier).
- Additive `services/wizard/objective_compile.py` (§8.4 compile-time rejections).
- Reuses `agent_interface.py`, `turn_ledger.py`, `session_persistence.py`, `admission_handoff.py` **byte-identically**.

### Sealed carriers unchanged

- `services/wizard/operator_state_machine.py` unchanged.
- `services/wizard/agent_interface.py` unchanged.
- `services/wizard/turn_ledger.py` unchanged.
- `services/wizard/session_persistence.py` unchanged.
- `contracts/wizard_commit_state.py` unchanged (extended via new sibling contract, not edited).

**Rating**: **CLEAN — extend existing state machine with additive objective variant + new contracts. Sibling machine explicitly rejected per §1.2.**

---

## Summary of §16.1 recommendations

| Item | Verdict | Recommendation | Sealed impact |
|---|---|---|---|
| (a) Perception router contract | CLEAN | codec is registered like any other perception model at `perception/model_registry.py` (v0→v1 additive bump); `character_stream` is already first-class on `CodecArtefact` — no new artifact type. Add sibling router helper (`route_character_stream`) additively. | Zero sealed edits. |
| (b) Ingestion segment boundaries | CLEAN | Canonical unit is `services/audio_plane_v1/language_identifier.AudioSegment`. Add sibling `language_identifier_with_station_prior.py` wrapper that fuses this-session's `RMS_STATION_LANGUAGE_AXIS` + `attribution_for_asset` HONESTY RULE. `language_hint` plumbing at 7 sites is wrapped, not edited. | Zero sealed edits. |
| (c) Wizard B-2/B-3 landing | CLEAN | Extend existing state machine with additive `objective` variant on `WizardCommitState_v0.variant` Literal + new sibling contracts (`target_outcome_v0`, `collection_schema_v0`, `wizard_objective_commit_state_v0`). Sibling machine explicitly rejected per §1.2. | Zero sealed edits. |

**All three §16.1 items yield CLEAN recommendations** — CP-AIP-1..10 slices can build additively on the existing sealed architecture without any refactor.

**No SPEC-CONFLICT-<n> logged** — spec and sealed code align on doctrine (§1.2 modality extension, §1.5 unrepresentable-not-policed, §3.8 additive-only).

---

## Files banked this receipt

- `phase0/aip_spec_verification_20260223/receipt.md` (this file).
- `STATE/OBJECTIVES/CP_AIP_*.md` (10 objective cards + P2 parked · next tool call).

**Additive-only §3.8** · zero code change · zero test change · zero ratchet movement · investigation + recommendations only.
