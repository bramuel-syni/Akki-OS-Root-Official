"""CP-AIP-4-CODEC-SERVICE · AIP v1.0 §3.2 P045 additive v0→v1 audio-codec registration.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-4-CODEC-SERVICE and nothing else.

Spec anchor (AIP v1.0):
- §3.2 P045 verbatim: 'perception/audio_codec/ - registered like any
  other perception model; census-visible; runs in-perimeter on
  tenant compute.'
- §16.1 (a) CLEAN verdict: model registration lives at
  `backend/services/perception/model_registry.py` with an append-only
  additive v(N)→v(N+1) doctrine. This module exposes the ENTRY-BUILDER
  callable; the actual v0→v1 bump is performed at deploy time via the
  sealed `register_model` API (not invoked at test time - SO §3.8
  additive-only).
- §1.2 modality-extension: imports sealed
  `AUDIO_CODEC_SERVICE_PATH` from CP-M6-4-1 verbatim; no parallel
  redeclaration.
- §16.2 codec-choice DEFERRED per owner ('Sampling & Reflection §11.2
  answers it once built'). This entry names the audio_codec service
  seat; specific codec base is a Sampling & Reflection decision.

Design:
- `AUDIO_CODEC_MODEL_ID` Final str: the entry-key under which the
  audio-codec service is registered in the perception models registry.
- `build_audio_codec_registry_entry()` returns the entry payload dict
  shape expected by sealed `register_model` at v0→v1 bump time.

Sealed carriers UNCHANGED per SO §3.8:
- backend/services/perception/audio_codec/service.py (CP-M6-4-1 ·
  AUDIO_CODEC_SERVICE_PATH imported).
- backend/services/perception/model_registry.py (extended additively
  via its own append-only doctrine - NOT edited here).
- backend/services/perception/models_registry.v0.json (v0 seed
  UNCHANGED - v0→v1 bump lands new file at deploy time).

Wave-honest limits:
- No LLM invocation. No HTTP call. No filesystem write (test time).
- Case-agnostic; no executive-domain tokens.
"""
from __future__ import annotations

from typing import Any, Dict, Final

from backend.services.perception.audio_codec.service import (
    AUDIO_CODEC_SERVICE_PATH,
    build_service_descriptor,
)


AUDIO_CODEC_MODEL_ID: Final[str] = "audio_codec_service_v0"


def build_audio_codec_registry_entry() -> Dict[str, Any]:
    """Return the entry payload dict for v0→v1 registration of the
    audio-codec service in the perception models registry.

    §3.2 P045 verbatim: 'perception/audio_codec/ - registered like any
    other perception model; census-visible; runs in-perimeter on
    tenant compute.'

    Shape mirrors the sealed v0 fixture-entry shape (model_id + role +
    origin + license) plus the audio-codec-specific §3.2 P045 flags
    (`service_path` verbatim + `census_visible` true + `in_perimeter`
    true) so the entry is discoverable both as a perception model AND
    as the audio-codec service seat.

    §16.2 codec-choice is DEFERRED - `codec_base_choice_pending` names
    the deferred decision so audit trails can locate it.
    """
    descriptor = build_service_descriptor()
    return {
        "model_id": AUDIO_CODEC_MODEL_ID,
        "family": "audio_codec_service",
        "role": "audio_perception_codec_service",
        "service_path": AUDIO_CODEC_SERVICE_PATH,
        "census_visible": True,
        "in_perimeter": True,
        "token_rate_target": list(descriptor.token_rate_target),
        "pretraining_contract": descriptor.pretraining_contract,
        "codec_base_choice_pending": (
            "§16.2 codec-choice DEFERRED per owner ruling. Sampling & "
            "Reflection §11.2 answers this once built."
        ),
        "authority_source": (
            "AIP v1.0 §3.2 P045 verbatim + §16.1 (a) CLEAN receipt "
            "(2026-02-23T05:00:00Z · state repo phase0/"
            "aip_spec_verification_20260223/receipt.md) + CP-AIP-4 "
            "seal (2026-02-23)."
        ),
    }
