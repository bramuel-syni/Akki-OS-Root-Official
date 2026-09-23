"""CP-SO-6.9-LID-WAVE · lid_wave_overlay_and_admission_v1 · additive §1.2 modality-extension.

Whisper-LID (MIT) + VoxLingua107 (Apache-2.0) registration acts + OverlayLidDetection_v1
shape + admission gate DEFAULT ≥ 90% scored against google-transcripts labelled corpus +
regime promotion by receipted act (canon 8 §4 W2) + anti-token HF pull wrapper +
TENANT-LABELS-PENDING honest-gap for English/Sheng/code-switched.

Spec anchors (verbatim on single un-wrapped lines):
- SO §6.9 LID RATIFICATION 2026-02-23 verbatim (STATE/OWNER_DROPS/so_6_9_lid_ratification_20260223/DROP.md).
- Audio-Plane v1.0 §4.1 N1: "A lightweight offline language identifier (CPU-viable, in-perimeter) runs at segment level during ingestion."
- B5.4 shown-not-counted: overlay detections MUST NOT flow into any counted measure until regime flips by receipted act.
- Canon 8 §4 W2: promotion is a receipted act with owner signature.
- §1.2 modality-extension composes sealed CP-M6-1-1 LanguageIDBackend at services/audio_plane_v1/language_identifier.py; no redeclaration.
- §6.9 clause 3: anti-token pull hazard scope; no Authorization/token header ever attached; env scrubbed of HF_TOKEN/HUGGINGFACEHUB_API_TOKEN/HUGGING_FACE_HUB_TOKEN.

Additive-only per SO §3.8. Sealed CP-M6-1-1 language_identifier.py UNCHANGED.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import ClassVar, Final, Literal, Optional


# --- Refusal exceptions ---------------------------------------------------------

class LidWaveBoundaryRefused(Exception):
    """Base for all LID-wave boundary refusals."""


class LidLabelBelowConfidenceMustBeUnmeasuredError(LidWaveBoundaryRefused):
    """OverlayLidDetection marker structural invariant violated.

    Enforces SO §6.9 LID §5 + B5.4:
    - marker == "INFERRED" iff label is not None
    - marker == "unmeasured" iff label is None
    """


class LidOverlayMustNotFlowIntoCountedMeasureError(LidWaveBoundaryRefused):
    """OverlayLidDetection regime=post-admission requires a companion receipted act.

    Enforces SO §6.9 LID §5 + B5.4 shown-not-counted line: the regime cannot start at
    post-admission at construction; a receipted-act promotion must exist first.
    """


class LidRegimePromotionRequiresOwnerReceiptedActError(LidWaveBoundaryRefused):
    """Regime promotion requires an owner_signature_ref (canon 8 §4 W2) and a real flip."""


class TokenPresentedInPullError(LidWaveBoundaryRefused):
    """Anti-token pull wrapper refused: bearer-like header key detected."""


# --- Registration act (both models) -------------------------------------------

@dataclass(frozen=True)
class LidModelRegistration_v1:
    """LID model registration act per SO §6.9 LID §4 verbatim.

    6-field shape (order-verbatim):
    - model_entry: canonical identifier used in overlay detection records.
    - weight_sha256: pinned weight-file hash (pull provenance verifies this later).
    - licence_id: Literal["MIT","Apache-2.0"] (SO §6.9 LID ratified two licences).
    - licence_file_path: on-disk path to the recorded licence file.
    - pull_provenance_ref: opaque handle to the pull URL + response headers + timestamp record.
    - execution_mode: Literal["cpu","cuda"] measured at run time.
    """
    model_entry: str
    weight_sha256: str
    licence_id: Literal["MIT", "Apache-2.0"]
    licence_file_path: str
    pull_provenance_ref: str
    execution_mode: Literal["cpu", "cuda"]


# Whisper LID (MIT) — canonical registration act
WHISPER_LID_REGISTRATION: Final[LidModelRegistration_v1] = LidModelRegistration_v1(
    model_entry="whisper-lid-v1-mit",
    weight_sha256="[weight-sha256-pinned-at-track-4-pull]",
    licence_id="MIT",
    licence_file_path="phase0/lid_registration_20260223/licences/whisper_lid_MIT.txt",
    pull_provenance_ref="phase0/lid_registration_20260223/pull_provenance/whisper_lid.json",
    execution_mode="cpu",
)


# SpeechBrain VoxLingua107 (Apache-2.0) — canonical registration act
VOXLINGUA107_REGISTRATION: Final[LidModelRegistration_v1] = LidModelRegistration_v1(
    model_entry="speechbrain-voxlingua107-apache-2-0",
    weight_sha256="[weight-sha256-pinned-at-track-4-pull]",
    licence_id="Apache-2.0",
    licence_file_path="phase0/lid_registration_20260223/licences/voxlingua107_APACHE_2_0.txt",
    pull_provenance_ref="phase0/lid_registration_20260223/pull_provenance/voxlingua107.json",
    execution_mode="cpu",
)


# --- Overlay detection record -------------------------------------------------

@dataclass(frozen=True)
class OverlayLidDetection_v1:
    """Overlay LID detection per SO §6.9 LID §5 verbatim.

    Structural invariants (enforced in __post_init__):
    - marker == "INFERRED" iff label is not None; marker == "unmeasured" iff label is None.
    - regime == "pre-admission" at construction; "post-admission" refused (must be produced by
      a receipted-act promotion path, not by direct construction).
    - disagreement_with_other_model is signal for the gate; do not resolve.

    Frozen: nothing ever relabelled per SO §6.9 LID §5 + §6 verbatim.
    """
    segment_ref: str
    model_entry: str
    label: Optional[str]
    confidence: float
    execution_mode: Literal["cpu", "cuda"]
    regime: Literal["pre-admission", "post-admission"]
    marker: Literal["INFERRED", "unmeasured"]
    disagreement_with_other_model: Optional[bool]
    detected_at_utc: str

    def __post_init__(self) -> None:
        # Marker/label invariant (B5.4 shown-not-counted line)
        if self.label is not None and self.marker != "INFERRED":
            raise LidLabelBelowConfidenceMustBeUnmeasuredError(
                f"OverlayLidDetection with label={self.label!r} must have marker='INFERRED'; got {self.marker!r}"
            )
        if self.label is None and self.marker != "unmeasured":
            raise LidLabelBelowConfidenceMustBeUnmeasuredError(
                f"OverlayLidDetection with label=None must have marker='unmeasured'; got {self.marker!r}"
            )
        # Regime invariant (shown-not-counted): direct construction with post-admission refused.
        if self.regime == "post-admission":
            raise LidOverlayMustNotFlowIntoCountedMeasureError(
                "OverlayLidDetection cannot be constructed with regime='post-admission' directly; "
                "post-admission overlays are produced only by the receipted-act promotion path "
                "per SO §6.9 LID §6 + canon 8 §4 W2."
            )


# --- Admission gate -----------------------------------------------------------

@dataclass(frozen=True)
class LidAdmissionGate_v1:
    """LID admission gate evaluation per SO §6.9 LID §6 verbatim.

    DEFAULT_THRESHOLD_PENDING = 0.90 (owner may retune before promotion).
    gate_status Literal["pending","cleared","below_threshold"].
    Score against google-transcripts/datasets/{kik,ebu,swa,luo,kln,guz,mer,bxk,kam,mrg,lwg,mas}/{audio,transcript}
    (12-language labelled corpus per SO §6.9 LID RATIFICATION amendment; TENANT-LABELS-PENDING resolved
    for these 12; English/Sheng/code-switched retain honest-gap per TenantLabelsPendingHonestGap_v1).
    """
    DEFAULT_THRESHOLD_PENDING: ClassVar[float] = 0.90

    model_entry: str
    tenant_labelled_sample_ref: str
    threshold: float
    segment_level_agreement: float
    gate_status: Literal["pending", "cleared", "below_threshold"]
    evaluated_at_utc: str


# --- Regime promotion (receipted act; canon 8 §4 W2) --------------------------

@dataclass(frozen=True)
class LidRegimePromotionByReceiptedAct_v1:
    """Regime promotion carrier per canon 8 §4 W2 verbatim.

    Nothing is relabelled at flip — this is a forward-looking regime change for future overlay
    detections. Historic overlays remain byte-identical (frozen carrier guarantee).
    """
    model_entry: str
    owner_signature_ref: str
    previous_regime: Literal["pre-admission", "post-admission"]
    new_regime: Literal["pre-admission", "post-admission"]
    effective_at_utc: str


def promote_lid_regime_by_receipted_act(
    *,
    model_entry: str,
    owner_signature_ref: str,
    previous_regime: str,
    new_regime: str,
    effective_at_utc: str,
) -> LidRegimePromotionByReceiptedAct_v1:
    """Promote LID model regime per canon 8 §4 W2 receipted-act discipline.

    Refuses when owner_signature_ref is empty (no receipted-act) or previous_regime == new_regime
    (no real flip). Returns frozen carrier bearing the receipt evidence.
    """
    if not owner_signature_ref:
        raise LidRegimePromotionRequiresOwnerReceiptedActError(
            "Regime promotion requires a non-empty owner_signature_ref (canon 8 §4 W2 receipted act)."
        )
    if previous_regime == new_regime:
        raise LidRegimePromotionRequiresOwnerReceiptedActError(
            f"Regime promotion requires a real flip; previous_regime={previous_regime!r} == "
            f"new_regime={new_regime!r} is not a promotion."
        )
    return LidRegimePromotionByReceiptedAct_v1(
        model_entry=model_entry,
        owner_signature_ref=owner_signature_ref,
        previous_regime=previous_regime,  # type: ignore[arg-type]
        new_regime=new_regime,  # type: ignore[arg-type]
        effective_at_utc=effective_at_utc,
    )


# --- Tenant labels honest-gap -------------------------------------------------

@dataclass(frozen=True)
class TenantLabelsPendingHonestGap_v1:
    """SO §6.9 LID RATIFICATION honest-gap residual per §5-§6 verbatim.

    12 languages RESOLVED via google-transcripts/ corpus (kik/ebu/swa/luo/kln/guz/mer/bxk/kam/mrg/lwg/mas).
    English/Sheng/code-switched retain honest-gap — no tenant-labelled sample yet; gate machinery
    lands and evaluates honest-gap per §6.9 desk discipline.
    """
    languages: frozenset[str]


TENANT_LABELS_PENDING_HONEST_GAP: Final[TenantLabelsPendingHonestGap_v1] = TenantLabelsPendingHonestGap_v1(
    languages=frozenset({"English", "Sheng", "code-switched"}),
)


LID_TENANT_LABELS_RESOLVED_12_LANGUAGES: Final[frozenset[str]] = frozenset({
    "kik", "ebu", "swa", "luo", "kln", "guz", "mer", "bxk", "kam", "mrg", "lwg", "mas",
})


# --- Anti-token HF pull wrapper (SO §6.9 clause 3) ----------------------------

_HF_TOKEN_ENV_KEYS: Final[tuple[str, ...]] = (
    "HF_TOKEN",
    "HUGGINGFACEHUB_API_TOKEN",
    "HUGGING_FACE_HUB_TOKEN",
)


class HuggingFacePullWrapperAntiToken_v1:
    """HF pull wrapper structurally guaranteed to present no bearer-like header.

    Per SO §6.9 clause 3 verbatim: "no Authorization/token= header ever attached; env scrubbed
    of HF_TOKEN/HUGGINGFACEHUB_API_TOKEN/HUGGING_FACE_HUB_TOKEN before the process starts."

    Public unauthenticated weight pulls are permitted per SO §6.9(3); do NOT present any old/leaked
    HF token; pull anonymously.
    """

    @staticmethod
    def scrub_env() -> None:
        """Remove HF-token env vars from os.environ before any pull path invokes an HTTP client."""
        for k in _HF_TOKEN_ENV_KEYS:
            os.environ.pop(k, None)

    def build_headers(self) -> dict[str, str]:
        """Return a header dict guaranteed to have no bearer-like key.

        Only User-Agent + Accept are set. Env is scrubbed before headers are built.
        """
        HuggingFacePullWrapperAntiToken_v1.scrub_env()
        headers: dict[str, str] = {
            "User-Agent": "akki-lid-anonymous-pull/1.0",
            "Accept": "application/octet-stream",
        }
        # Post-build guard: refuse any bearer-like key defensively.
        banned = {"authorization", "bearer", "token"}
        for k in list(headers.keys()):
            kl = k.lower()
            for b in banned:
                if b in kl:
                    raise TokenPresentedInPullError(
                        f"Anti-token pull wrapper detected bearer-like header key '{k}' (contains '{b}')."
                    )
        return headers


# --- Final posture markers (§6.9 desk discipline) -----------------------------

LID_DO_NOT_FLOW_INTO_COUNTED_MEASURE_POSTURE: Final[str] = (
    "SO §6.9 LID RATIFICATION §5 verbatim: overlay LID detections MUST NOT flow into any "
    "counted measure until the admission gate clears by receipted act; overlay detections are "
    "shown, not counted (B5.4 shown-not-counted line)."
)

LID_HF_PULL_WRAPPER_ANTI_TOKEN_POSTURE: Final[str] = (
    "SO §6.9 clause 3 verbatim: no Authorization/token= header ever attached; env scrubbed of "
    "HF_TOKEN/HUGGINGFACEHUB_API_TOKEN/HUGGING_FACE_HUB_TOKEN before the process starts. Public "
    "unauthenticated weight pulls proceed; presentation of the leaked credential is structurally "
    "impossible for this call."
)

LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE: Final[str] = (
    "SO §6.9 LID RATIFICATION §5-§6 verbatim: nothing is ever relabelled at regime flip; "
    "promotion changes regime, not labels. Historic overlay detections remain byte-identical "
    "(frozen carrier guarantee). Post-admission overlays are produced only by the receipted-act "
    "promotion path per canon 8 §4 W2."
)


__all__ = [
    "LidWaveBoundaryRefused",
    "LidLabelBelowConfidenceMustBeUnmeasuredError",
    "LidOverlayMustNotFlowIntoCountedMeasureError",
    "LidRegimePromotionRequiresOwnerReceiptedActError",
    "TokenPresentedInPullError",
    "LidModelRegistration_v1",
    "WHISPER_LID_REGISTRATION",
    "VOXLINGUA107_REGISTRATION",
    "OverlayLidDetection_v1",
    "LidAdmissionGate_v1",
    "LidRegimePromotionByReceiptedAct_v1",
    "promote_lid_regime_by_receipted_act",
    "TenantLabelsPendingHonestGap_v1",
    "TENANT_LABELS_PENDING_HONEST_GAP",
    "LID_TENANT_LABELS_RESOLVED_12_LANGUAGES",
    "HuggingFacePullWrapperAntiToken_v1",
    "LID_DO_NOT_FLOW_INTO_COUNTED_MEASURE_POSTURE",
    "LID_HF_PULL_WRAPPER_ANTI_TOKEN_POSTURE",
    "LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE",
]
