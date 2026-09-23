# CP-AIP-4-CODEC-SERVICE · objective card · 2026-02-23T05:05:00Z

**Spec anchor:** AIP v1.0 §3 · Build Sequence #4.

**Status:** ⚪ **QUEUED** (opens after CP-AIP-3 completes · unsupervised codec pretraining can run in parallel with labelled work per §15 verbatim).

## Rationale for position (spec §15 verbatim)

> *"Unsupervised pretraining starts on unlabelled audio while labelled work proceeds elsewhere."*

## Scope

Full `perception/audio_codec/` service per §3.2 with:

- **Registration** at `services/perception/model_registry.py` via additive v0→v1 bump per its append-only doctrine.
- **Census-visible** posture per §3.2 verbatim.
- **In-perimeter tenant compute** per §3.2 verbatim.
- **Output**: `{content_tokens[], character_stream, codec_version}` — already sealed at `services/perception/audio_codec/artefact.py:CodecArtefact` (CP-M6-4-2).
- **Target token rate** 50-100 tokens/second of audio (§3.2 · measured before serve per §3.3).
- **Unsupervised pretraining** on unlabelled estate audio under standard commissioned-job contract (§3.2).

## §3.3 acceptance criteria (become RED-first pytest invariants)

1. **Round-trip fidelity measured and recorded per codec version BEFORE that version serves any commission.**
2. **A downstream artifact lacking `codec_version` in provenance is REJECTED at the registry boundary.** — sealed at CP-M6-4-2 · reinforce via new test surface.
3. **An unsupported-condition input produces a refusal with a stated reason and NO output artifact** — fail-closed per §1.5.

## §16.2 open decision (banked as PENDING-OWNER-CONFIRMATION)

**Codec choice** — deferred per owner: `"Sampling & Reflection answers it once built (§11.2)"`. Working default: existing open codec (name TBD post-CP-AIP-8) vs estate-specific — decision lands at Sampling & Reflection completion.

## §16.2 open decision working defaults

- **HF-HOLD SEC-2026-09-12-01 LIFTED** this-session (owner 2026-02-23T03:15Z) — HF-hosted codec bases are permitted; local/cached fallback via `local_files_only=True` remains as offline path.

## New additive modules (proposed shape)

- `services/perception/audio_codec/pretrain.py` — commissioned-job pretraining harness.
- `services/perception/audio_codec/round_trip_fidelity.py` — per-version fidelity measurement.
- `services/perception/audio_codec/unsupported_condition_refusal.py` — fail-closed with stated reason.
- `services/perception/audio_codec/models_registry_v1_bump.py` — additive v0→v1 registration.
- Test file: `tests/invariants/test_cp_aip_4_codec_service_aip_v1_0_section_3.py` (≥5 RED-first pins per §3.3).

## Sealed carriers to NOT edit

- `services/perception/audio_codec/artefact.py` (CP-M6-4-2 sealed).
- `services/perception/audio_codec/service.py` (CP-M6-4-1 sealed).
- `services/perception/audio_codec/census_visibility.py` (sealed).
- `services/perception/audio_codec/perimeter_boundary.py` (sealed).
- `services/perception/model_registry.py` (extended additively per its own append-only doctrine).
- `services/perception/models_registry.v0.json` (v0→v1 additive bump lands new file).

## Ledger check

> **Ledger check — this seal implements EXECUTION_ORDER.md item 5 CP-AIP-4-CODEC-SERVICE and nothing else.**

**Additive-only §3.8 · RED-first · 5-commit seal · BASELINE_GUARD.**
