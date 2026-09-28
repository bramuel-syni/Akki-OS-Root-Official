"""CP-AIP-4-CODEC-SERVICE · AIP v1.0 §3.3 (c) unsupported-condition fail-closed refusal.

Ledger check - this seal implements EXECUTION_ORDER.md item 5 CP-AIP-4-CODEC-SERVICE and nothing else.

Spec anchor (AIP v1.0):
- §3.1 P037 verbatim: 'The audio codec fails closed; it never silently
  degrades. The character stream is retained and routed, never
  discarded.'
- §3.3 (c) verbatim: 'An unsupported-condition input produces a refusal
  with a stated reason and no output artifact.'
- §1.5 unrepresentable-not-policed: the refusal path is structural -
  the callable raises before any artifact-shaped return value flows.

Design:
- `SupportedConditionProfileRegistry_v1` frozen dataclass carries the
  set of supported condition-profile names for a given codec version
  + a provenance ref pointing to the material behind the support set.
- `UnsupportedCodecConditionRefused` raised on any input whose declared
  condition is outside the supported set. Refusal message MUST carry
  the offending condition name AND the codec version (owner directive
  §3.3 (c) 'stated reason').
- No output artifact ever flows on the refusal path. On the acceptance
  path the callable returns None (no artifact-shaped value either -
  artifact construction is downstream).

Sealed carriers UNCHANGED per SO §3.8:
- backend/services/perception/audio_codec/service.py (CP-M6-4-1).
- backend/services/perception/audio_codec/artefact.py (CP-M6-4-2).

Wave-honest limits:
- No LLM invocation. No HTTP call. No filesystem write.
- Case-agnostic; no executive-domain tokens.
- §3.1 P038 tokens-not-waveforms: no audio-byte carriers here either.
"""
from __future__ import annotations

import dataclasses
from typing import FrozenSet


class UnsupportedCodecConditionRefused(Exception):
    """§3.3 (c) verbatim refusal · fail-closed on unsupported condition
    input. Carries the offending condition name + codec version in
    the message so the stated reason is retrievable by callers
    (owner directive verbatim: 'stated reason')."""


@dataclasses.dataclass(frozen=True)
class SupportedConditionProfileRegistry_v1:
    """§3.3 (c) supported-condition registry for a given codec version.

    Three carriers:
      - `codec_version` — the codec version this registry applies to
        (matches sealed CP-M6-4-2 `codec_version` field).
      - `supported_conditions` — immutable frozenset of condition-
        profile names admitted by this codec version.
      - `provenance_ref` — reference to the material / receipt that
        established the support set (§6.2 P098 verbatim 'provenance
        points to material').
    """

    codec_version: str
    supported_conditions: FrozenSet[str]
    provenance_ref: str


def assert_condition_supported(
    *,
    codec_version: str,
    declared_condition: str,
    registry: SupportedConditionProfileRegistry_v1,
) -> None:
    """§3.3 (c) verbatim: 'An unsupported-condition input produces a
    refusal with a stated reason and no output artifact.'

    Refuses `UnsupportedCodecConditionRefused` when `declared_condition`
    is outside `registry.supported_conditions`. Returns None on
    acceptance (no artifact-shaped value flows either - artifact
    construction is downstream).

    Also refuses if `codec_version` does not match the registry's
    codec_version - the registry pin is per-version by construction.
    """
    if codec_version != registry.codec_version:
        raise UnsupportedCodecConditionRefused(
            f"§3.3 (c) codec version mismatch: request codec_version="
            f"{codec_version!r} vs registry codec_version="
            f"{registry.codec_version!r}. Support registries are "
            f"per-version by construction."
        )
    if declared_condition not in registry.supported_conditions:
        raise UnsupportedCodecConditionRefused(
            f"§3.3 (c) verbatim: codec version {codec_version!r} refuses "
            f"unsupported condition {declared_condition!r}. Supported "
            f"conditions per registry: {sorted(registry.supported_conditions)!r}. "
            f"Registry provenance: {registry.provenance_ref!r}. Stated "
            f"reason: declared_condition is outside the supported set for "
            f"this codec version - fail-closed per §3.1 P037. NO output "
            f"artifact produced."
        )
    return None
