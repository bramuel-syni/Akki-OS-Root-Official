"""CP-LID-OVERLAY-ABSTENTION-AND-ESTATE-FILTER · additive fix module

Owner correction 2026-02-24 verbatim (P0 fidelity defect · false-positive
language labels): "The LID overlay produced Maori ('mi') and Arabic ('ar')
labels. The owner confirms there is NO Maori or Arabic in this data. These
are FALSE POSITIVES — a real accuracy defect. VERIFY the abstention rule is
live: a window below the confidence threshold MUST record unmeasured, NEVER
a label. If it isn't enforced, that is the bug — fix it (additive) with a
RED-first pin. CONSTRAIN honestly: consider an estate-language allow-list
prior (the 12 corpus languages + English/Sheng/Swahili — the languages
actually present) so labels outside it are flagged low-confidence/unmeasured
rather than asserted. Do NOT hard-suppress — record the raw model output but
mark out-of-estate labels as suspected-false-positive."

Spec anchors (verbatim):
- CP-SO-6.9-LID-WAVE §5 (B5.4 shown-not-counted line).
- CP-SO-6.9-LID-WAVE §6 admission gate DEFAULT threshold ≥ 0.90.
- CP-AIP-LANGUAGE-COGNITION MUST-DO §5 (Canon 5 §5.3): "A window below the
  confidence threshold is unmeasured, NEVER labelled."
- CP-AIP-LANGUAGE-COGNITION MUST-NOT §4: "Below-confidence windows are
  unmeasured, NEVER labelled with any language."
- SO §6.9 LID RATIFICATION §5 markers-over-refusal: raw output preserved
  alongside filtered result (anti-loss); out-of-estate labels are FLAGGED
  suspected-false-positive, not hard-suppressed.
- §1.2 modality-extension composes sealed OverlayLidDetection_v1 +
  LidAdmissionGate_v1 by identity; no redeclaration.

Additive-only per SO §3.8. Sealed lid_wave_overlay_and_admission_v1.py
UNCHANGED. Nothing here alters existing symbols; every sealed symbol is
imported and re-exported by identity for composition.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, Tuple

# --- §1.2 compose sealed symbols by identity (no redeclaration) ---------------
from .lid_wave_overlay_and_admission_v1 import (
    LidAdmissionGate_v1,
    LidLabelBelowConfidenceMustBeUnmeasuredError,
    LID_TENANT_LABELS_RESOLVED_12_LANGUAGES,
    OverlayLidDetection_v1,
)

__all__ = [
    # Estate allow-list (owner correction 2026-02-24)
    "ESTATE_LANGUAGE_ALLOWLIST_v1",
    "LID_ABSTENTION_DEFAULT_THRESHOLD",
    "LID_ABSTENTION_REASONS",
    # Additive filtered-sample carrier
    "LidOverlayFilteredSample_v1",
    # Boundary callable
    "apply_abstention_and_estate_filter",
    # Composed sealed symbols (identity re-export)
    "OverlayLidDetection_v1",
    "LidAdmissionGate_v1",
    "LidLabelBelowConfidenceMustBeUnmeasuredError",
    "LID_TENANT_LABELS_RESOLVED_12_LANGUAGES",
    # Posture markers (§6.9 desk discipline)
    "LID_ESTATE_ALLOWLIST_PRIOR_POSTURE",
    "LID_ABSTENTION_ENFORCED_AT_WRITER_BOUNDARY_POSTURE",
    "LID_RAW_OUTPUT_PRESERVED_ANTI_LOSS_POSTURE",
]


# --- Estate language allow-list (owner correction 2026-02-24 verbatim) --------
#
# 12 google-transcripts labelled corpus codes (from sealed
# LID_TENANT_LABELS_RESOLVED_12_LANGUAGES) + English (en) + Sheng (sheng).
# Swahili appears as "swa" in the 12-corpus tuple; the display name "Swahili"
# from LANGUAGE_COGNITION_TARGET_LANGUAGES is the same language — the ISO code
# is authoritative for filter equality.
ESTATE_LANGUAGE_ALLOWLIST_v1: Final[frozenset[str]] = frozenset(
    LID_TENANT_LABELS_RESOLVED_12_LANGUAGES | {"en", "sheng"}
)


# --- Default threshold (composition-by-identity with sealed admission gate) ---
LID_ABSTENTION_DEFAULT_THRESHOLD: Final[float] = LidAdmissionGate_v1.DEFAULT_THRESHOLD_PENDING


# --- Abstention reason enum (verbatim 3-tuple · owner correction 2026-02-24) --
LID_ABSTENTION_REASONS: Final[Tuple[str, str, str]] = (
    "ok",
    "below_confidence",
    "out_of_estate_suspected_false_positive",
)


# --- Additive frozen carrier: filtered sample + raw output ANTI-LOSS ----------
@dataclass(frozen=True)
class LidOverlayFilteredSample_v1:
    """Filtered LID overlay sample carrying BOTH the sealed
    OverlayLidDetection_v1 (after abstention + estate-filter applied) AND
    the raw model output (raw_label, raw_confidence) — anti-loss discipline
    per owner correction 2026-02-24 verbatim.

    4-field shape verbatim (order):
    - overlay: sealed OverlayLidDetection_v1 (label=None if abstained; label set
      only if in-estate + confidence ≥ threshold).
    - raw_label: the raw model output label BEFORE filtering (str; preserved).
    - raw_confidence: the raw model output confidence BEFORE filtering (float).
    - abstention_reason: Literal[LID_ABSTENTION_REASONS] verbatim.

    Frozen: nothing relabelled at regime flip per SO §6.9 LID RATIFICATION §5-§6.
    """
    overlay: OverlayLidDetection_v1
    raw_label: str
    raw_confidence: float
    abstention_reason: Literal[
        "ok",
        "below_confidence",
        "out_of_estate_suspected_false_positive",
    ]


# --- Boundary callable — apply abstention + estate-filter (single writer path) -
def apply_abstention_and_estate_filter(
    *,
    segment_ref: str,
    model_entry: str,
    raw_label: str,
    raw_confidence: float,
    execution_mode: Literal["cpu", "cuda"],
    detected_at_utc: str,
    threshold: float = LID_ABSTENTION_DEFAULT_THRESHOLD,
) -> LidOverlayFilteredSample_v1:
    """Apply confidence-abstention + estate-allow-list-filter to a raw LID
    model output and return the sealed OverlayLidDetection_v1 alongside the
    raw output (anti-loss).

    Rules (owner correction 2026-02-24 verbatim):
    1. If raw_confidence < threshold → label=None, marker='unmeasured',
       abstention_reason='below_confidence'.
    2. Else if raw_label NOT in ESTATE_LANGUAGE_ALLOWLIST_v1 → label=None,
       marker='unmeasured', abstention_reason='out_of_estate_suspected_false_positive'.
    3. Else → label=raw_label, marker='INFERRED', abstention_reason='ok'.

    Case-insensitive on raw_label: normalized to lowercase for allow-list
    comparison; original raw_label preserved verbatim in the filtered carrier.

    Composes sealed OverlayLidDetection_v1 by identity — the sealed
    LidLabelBelowConfidenceMustBeUnmeasuredError structural invariant remains
    the ultimate guard on the (label, marker) pair.

    Raw model output is ALWAYS preserved on LidOverlayFilteredSample_v1
    (raw_label + raw_confidence fields) — no lossy drop, per owner correction
    verbatim: 'Do NOT hard-suppress — record the raw model output.'
    """
    normalized = raw_label.strip().lower()

    if raw_confidence < threshold:
        overlay_label = None
        overlay_marker = "unmeasured"
        reason = "below_confidence"
    elif normalized not in ESTATE_LANGUAGE_ALLOWLIST_v1:
        overlay_label = None
        overlay_marker = "unmeasured"
        reason = "out_of_estate_suspected_false_positive"
    else:
        overlay_label = normalized
        overlay_marker = "INFERRED"
        reason = "ok"

    overlay = OverlayLidDetection_v1(
        segment_ref=segment_ref,
        model_entry=model_entry,
        label=overlay_label,
        confidence=raw_confidence,
        execution_mode=execution_mode,
        regime="pre-admission",
        marker=overlay_marker,  # type: ignore[arg-type]
        disagreement_with_other_model=None,
        detected_at_utc=detected_at_utc,
    )
    return LidOverlayFilteredSample_v1(
        overlay=overlay,
        raw_label=raw_label,
        raw_confidence=raw_confidence,
        abstention_reason=reason,  # type: ignore[arg-type]
    )


# --- Posture markers (§6.9 desk discipline) -----------------------------------
LID_ESTATE_ALLOWLIST_PRIOR_POSTURE: Final[str] = (
    "Owner correction 2026-02-24 verbatim: 'consider an estate-language "
    "allow-list prior (the 12 corpus languages + English/Sheng/Swahili — the "
    "languages actually present) so labels outside it are flagged "
    "low-confidence/unmeasured rather than asserted.' The prior is applied "
    "as a structural filter at the LID overlay writer boundary; raw model "
    "output is preserved alongside (anti-loss)."
)

LID_ABSTENTION_ENFORCED_AT_WRITER_BOUNDARY_POSTURE: Final[str] = (
    "Owner correction 2026-02-24 verbatim: 'VERIFY the abstention rule is "
    "live: a window below the confidence threshold MUST record unmeasured, "
    "NEVER a label.' The abstention rule is enforced at the LID overlay "
    "writer boundary (apply_abstention_and_estate_filter) — the raw model "
    "output NEVER flows into the OverlayLidDetection_v1 label field unless "
    "it clears both threshold AND estate allow-list."
)

LID_RAW_OUTPUT_PRESERVED_ANTI_LOSS_POSTURE: Final[str] = (
    "Owner correction 2026-02-24 verbatim: 'Do NOT hard-suppress — record "
    "the raw model output but mark out-of-estate labels as "
    "suspected-false-positive.' Anti-loss is guaranteed by "
    "LidOverlayFilteredSample_v1 carrying raw_label + raw_confidence on "
    "every filter output; the filtered sealed overlay + the raw output "
    "coexist on the frozen carrier."
)
