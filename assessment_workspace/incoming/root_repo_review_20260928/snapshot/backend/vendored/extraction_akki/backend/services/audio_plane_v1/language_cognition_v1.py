"""CP-AIP-LANGUAGE-COGNITION · language_cognition_v1 · additive Targeta training-run.

Ledger check - this seal implements Item 5.12 of EXECUTION_ORDER.md
CP-AIP-LANGUAGE-COGNITION (SPEC ENHANCEMENT · owner order 2026-02-23T~16:07Z
verbatim · SO §6.8 standing authority) and nothing else. Additive-only per
SO §3.8. Sealed CP-SO-6.9-LID-WAVE + CP-CENSUS-THREE-WAVES + CP-ENT-16 +
CP-TENANT-SEPARATION + CP-TRACK-4-AUTONOMY-WIRING + CP-AIP-ASSIST-CENSUS +
CP-AIP-ASSIST-TRAINING + CP-AIP-10-TRAINING-RUNS UNCHANGED. Terminal
pytest only. RED-first mechanical.

Owner directive verbatim (SO §6.8 standing authority + owner drop
2026-02-23 `STATE/OWNER_DROPS/language_cognition_20260223/DROP.md`):

    "A model that identifies the language of speech in the RMS archive by
    its acoustic and phonotactic signature — including Kikuyu, Luo, Sheng,
    Swahili and English, and including code-switched speech where several
    occur in one utterance — producing per-span labels grounded to the
    second, so the census can measure language distribution as fact rather
    than mark it unmeasured."

Ruling (b) AKKI-RUNS-IT verbatim 2026-02-23: E1 wires the seam INTO
Census Autonomy Service; pod is never data path. Training compute + model
weights + labelled corpus NEVER leave Akki's boundary.

§1.2 modality-extension composing sealed CP-SO-6.9-LID-WAVE +
CP-TRACK-4-AUTONOMY-WIRING + CP-AIP-ASSIST-CENSUS by identity — never
redeclare sealed symbols.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional, Tuple

# §1.2 modality-extension: compose sealed CP-SO-6.9-LID-WAVE by identity.
from backend.services.audio_plane_v1.lid_wave_overlay_and_admission_v1 import (
    LidModelRegistration_v1 as _LidModelRegistration_v1,
    WHISPER_LID_REGISTRATION as _WHISPER_LID_REGISTRATION,
    VOXLINGUA107_REGISTRATION as _VOXLINGUA107_REGISTRATION,
    promote_lid_regime_by_receipted_act as _promote_lid_regime_by_receipted_act,
    LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE as _LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE,
)

# §1.2 modality-extension: compose sealed CP-TRACK-4-AUTONOMY-WIRING by identity.
from backend.services.census_autonomy.track_4_autonomy_wiring_v1 import (
    TRACK_4_JOB_KINDS as _TRACK_4_JOB_KINDS,
    PodIsNeverDataPathAtTrack4Error as _PodIsNeverDataPathAtTrack4Error,
    POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4 as _POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4,
    E1_STEPS_BACK_AFTER_WIRING_POSTURE as _E1_STEPS_BACK_AFTER_WIRING_POSTURE,
)


# ---------------------------------------------------------------------------
# Sealed anchors composed by identity (§1.2 no-redeclaration)
# ---------------------------------------------------------------------------

WHISPER_LID_REGISTRATION_TRAINING_BASE_ANCHOR: Final[_LidModelRegistration_v1] = _WHISPER_LID_REGISTRATION
VOXLINGUA107_REGISTRATION_TRAINING_BASE_ANCHOR: Final[_LidModelRegistration_v1] = _VOXLINGUA107_REGISTRATION
PROMOTE_LID_REGIME_BY_RECEIPTED_ACT_COMPOSED_BY_IDENTITY = _promote_lid_regime_by_receipted_act
TRACK_4_JOB_KINDS_ANCHOR = _TRACK_4_JOB_KINDS


# ---------------------------------------------------------------------------
# Refusal hierarchy — base + specialised subclasses per MUST-NOT §§1-9
# ---------------------------------------------------------------------------


class LanguageCognitionBoundaryRefused(Exception):
    """Base refusal for language-cognition boundary violations."""


class CleanMonolingualOnlyRefused(LanguageCognitionBoundaryRefused):
    """MUST-NOT §1: 'Clean-monolingual alone is a MUST-NOT for the final
    model.' Owner verbatim. Commission refused when has_code_switched_material
    is False."""


class SpeakerOverlapRefused(LanguageCognitionBoundaryRefused):
    """MUST-NOT §2: 'Speaker overlap between train and test splits' refused
    (Canon 4 §5.5 + DAP-31)."""


class SpeakerIdentifiableArtefactRefused(LanguageCognitionBoundaryRefused):
    """MUST-NOT §3: artefact that identifies presenters above chance refused
    (DAP-31 biometric class · Canon 8)."""


class BelowConfidenceLabelRefused(LanguageCognitionBoundaryRefused):
    """MUST-NOT §4: labelling a below-confidence window refused (Canon 5 §5.3).
    Below-confidence windows are `unmeasured`, NEVER labelled."""


class RelabellingAtRegimeFlipRefused(LanguageCognitionBoundaryRefused):
    """MUST-NOT §5: relabelling prior overlay labels at regime flip refused
    (Canon 5 §B5.4 + Canon 8 §W2). Nothing is relabelled retrospectively."""


class PodAsDataPathRefused(_PodIsNeverDataPathAtTrack4Error):
    """MUST-NOT §6: pod as data path or training host refused (Ruling (b)
    verbatim). Extends sealed CP-TRACK-4 base by identity — pod://* + /app/*
    prefixed refs refused at every boundary."""


class SilentMoacThresholdChangeRefused(LanguageCognitionBoundaryRefused):
    """MUST-NOT §8: silent MOAC threshold change refused (owner verbatim
    'MOAC criteria owner-set'). Threshold changes require a new owner-set
    frozen criteria contract."""


class MockTrainingRunRefused(LanguageCognitionBoundaryRefused):
    """MUST-NOT §9: mock training-run execution refused (owner drop
    §Execution-reach verbatim: 'commissioned-job contract with honest-gap on
    execution, never a mock')."""


# ---------------------------------------------------------------------------
# Frozen carriers — MUST-DO §§1-11 shape
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LanguageCognitionFeatureBasis_v1:
    """MUST-DO §1 (Canon 4 §5.4): feature basis for language cognition —
    signature not prosody alone. Phonotactic + spectral structure are the
    PRIMARY signals; prosody/pitch/dynamics are SECONDARY features. The
    card names the feature basis so the model is evaluated on what it
    should be learning.
    """
    primary_features: Tuple[str, ...]
    secondary_features: Tuple[str, ...]
    canon_reference: str


LANGUAGE_COGNITION_FEATURE_BASIS: Final[LanguageCognitionFeatureBasis_v1] = LanguageCognitionFeatureBasis_v1(
    primary_features=("phonotactic", "spectral"),
    secondary_features=("prosody", "pitch", "dynamics"),
    canon_reference="Canon 4 §5.4 feature-basis declaration + Doc 20 training-base posture",
)


@dataclass(frozen=True)
class LanguageCognitionTrainingBaseRegistration_v1:
    """MUST-DO §8 (Doc 20 · owner drop §Sequence): Extends sealed
    CP-SO-6.9-LID-WAVE LID registrations with training-base posture (hash +
    licence + LoRA-adapter declaration). The sealed carrier is composed by
    identity in the `sealed_lid_registration` field — no redeclaration.
    """
    sealed_lid_registration: _LidModelRegistration_v1
    training_base_posture_hash: str
    licence_id_pinned: str
    lora_adapter_declaration: str


@dataclass(frozen=True)
class SpeakerDisjointSplitContract_v1:
    """MUST-DO §3 (Canon 4 §5.5 + DAP-31): minimum N distinct presenters per
    language; train/test splits share NO speaker. This is the criterion that
    separates learning a language from learning a voice. N DEFAULT 20 is a
    FORK to DESK_QUEUE (DQ-21) tagged pending.
    """
    presenter_minimum_n: int
    presenter_minimum_n_tagged_pending: bool  # FORK DQ-21
    share_no_speaker: bool


SPEAKER_DISJOINT_SPLIT_CONTRACT_DEFAULT: Final[SpeakerDisjointSplitContract_v1] = SpeakerDisjointSplitContract_v1(
    presenter_minimum_n=20,
    presenter_minimum_n_tagged_pending=True,
    share_no_speaker=True,
)


@dataclass(frozen=True)
class NoSpeakerIdMoacProbe_v1:
    """MUST-DO §4 (DAP-31 applied to voices · Canon 8 biometric class):
    A speaker-identification probe against the artefact MUST fail to exceed
    chance on held-out presenters. A voice is biometric personal data; an
    artefact that could return 'this is presenter X' does not leave the
    training run.
    """
    held_out_presenter_set_ref: str
    chance_level_threshold: float
    probe_passed: bool


@dataclass(frozen=True)
class WindowAndSpanRule_v1:
    """MUST-DO §5 (Canon 5 §5.3 + owner drop §Window-and-span):
    Classification per one-to-two-second window; deterministic span rule
    (minimum span duration + hysteresis on label change). Each span carries
    start/end seconds. Below-confidence = `unmeasured` NEVER labelled.
    """
    window_seconds_min: float
    window_seconds_max: float
    min_span_duration_seconds: float
    hysteresis_frames: int
    below_confidence_marker: str


WINDOW_AND_SPAN_RULE_DEFAULT: Final[WindowAndSpanRule_v1] = WindowAndSpanRule_v1(
    window_seconds_min=1.0,
    window_seconds_max=2.0,
    min_span_duration_seconds=0.5,
    hysteresis_frames=2,
    below_confidence_marker="unmeasured",
)


@dataclass(frozen=True)
class LanguageCognitionMoacContract_v1:
    """MUST-DO §6 (owner drop §MOAC-criteria) verbatim:
    - Per-language accuracy on speaker-disjoint real material — DEFAULT
      ≥ 90% (FORK DQ-22).
    - Code-switch span accuracy — boundary within a ruled tolerance AND
      label correct — DEFAULT ≥ 85% (FORK DQ-23).
    - No-speaker-identification probe passed.
    - Abstention rate REPORTED, not hidden.
    """
    per_language_accuracy_default: float
    per_language_accuracy_tagged_pending: bool  # FORK DQ-22
    code_switch_span_accuracy_default: float
    code_switch_span_accuracy_tagged_pending: bool  # FORK DQ-23
    no_speaker_id_probe_passed: bool
    abstention_rate_reported: bool


LANGUAGE_COGNITION_MOAC_CONTRACT_DEFAULT: Final[LanguageCognitionMoacContract_v1] = LanguageCognitionMoacContract_v1(
    per_language_accuracy_default=0.90,
    per_language_accuracy_tagged_pending=True,
    code_switch_span_accuracy_default=0.85,
    code_switch_span_accuracy_tagged_pending=True,
    no_speaker_id_probe_passed=True,
    abstention_rate_reported=True,
)


@dataclass(frozen=True)
class B5_4_AdmissionReceiptedAct_v1:
    """MUST-DO §7 (Canon 5 §B5.4 + Canon 8 §W2): On MOAC pass, model's
    labels promote from OVERLAY to MEASURE by a receipted act; regime flag
    changes; NOTHING is relabelled. Composes sealed CP-SO-6.9-LID-WAVE
    `promote_lid_regime_by_receipted_act` by identity via
    `PROMOTE_LID_REGIME_BY_RECEIPTED_ACT_COMPOSED_BY_IDENTITY`.
    """
    receipt_ref: str
    moac_pass_ref: str
    admitted_at_utc: str
    prior_overlay_labels_untouched: bool


@dataclass(frozen=True)
class RmsCustodyRightsPosture_v1:
    """MUST-DO §9 (Canon 8 §3 + pilot licence §8.3 + DP-SGD default):
    Labelled corpus is tenant data — RMS custody class applies; training
    inside the perimeter (E1 pod NEVER data path per Ruling (b) verbatim);
    artefact belongs to RMS under pilot terms unless elected otherwise
    (§8.3); DP-SGD default applies unless the owner opts out recorded.
    DP opt-out is a FORK to DESK_QUEUE (DQ-24).
    """
    custody_class: str
    in_perimeter_training: bool
    artefact_ownership_ref: str
    dp_sgd_default: bool
    dp_opt_out_ref: Optional[str]
    dp_opt_out_tagged_pending: bool  # FORK DQ-24


RMS_CUSTODY_RIGHTS_POSTURE_DEFAULT: Final[RmsCustodyRightsPosture_v1] = RmsCustodyRightsPosture_v1(
    custody_class="RMS_TENANT",
    in_perimeter_training=True,
    artefact_ownership_ref="pilot_licence_ref://8.3",
    dp_sgd_default=True,
    dp_opt_out_ref=None,
    dp_opt_out_tagged_pending=True,
)


@dataclass(frozen=True)
class LanguageCognitionCorpusAssemblyPosture_v1:
    """MUST-DO §10 (owner drop §Sequence · §coupling): corpus assembly
    runs UNDER THE CENSUS ASSISTANT'S DIALOGUE. The assistant proposes
    corpus slices; the owner/tenant confirms; gates decide. Composes sealed
    CP-AIP-ASSIST-CENSUS `bank_confirmed_assistant_turn` +
    `render_content_registry_entry` by identity via the corpus-seam module.
    """
    assistant_module_ref: str
    workflow_kind: str


LANGUAGE_COGNITION_CORPUS_ASSEMBLY_POSTURE: Final[LanguageCognitionCorpusAssemblyPosture_v1] = (
    LanguageCognitionCorpusAssemblyPosture_v1(
        assistant_module_ref="backend.services.census_autonomy.assist_census_v1",
        workflow_kind="propose_confirm_gate_decide",
    )
)


# ---------------------------------------------------------------------------
# Posture markers (Final str · owner/canon verbatim)
# ---------------------------------------------------------------------------


SIGNATURE_NOT_PROSODY_ALONE_POSTURE: Final[str] = (
    "CP-AIP-LANGUAGE-COGNITION MUST-DO §1 verbatim (Canon 4 §5.4 feature-"
    "basis declaration + Doc 20 training-base posture): 'The model MUST "
    "learn phonotactic and spectral structure as PRIMARY signal; prosody, "
    "pitch and dynamics are SECONDARY features. The card names the feature "
    "basis so the model is evaluated on what it should be learning.' "
    "Signature not prosody alone."
)


CLEAN_MONOLINGUAL_ALONE_MUST_NOT_POSTURE: Final[str] = (
    "CP-AIP-LANGUAGE-COGNITION MUST-NOT §1 owner verbatim: 'Clean-"
    "monolingual alone is a MUST-NOT for the final model.' The final "
    "model refuses commission if the labelled training set carries NO "
    "code-switched material per span."
)


NO_SPEAKER_ID_MOAC_POSTURE: Final[str] = (
    "CP-AIP-LANGUAGE-COGNITION MUST-DO §4 verbatim (DAP-31 logic applied "
    "to voices · Canon 8 §Personal-data biometric class): 'A speaker-"
    "identification probe against the artefact MUST fail to exceed chance "
    "on held-out presenters. A voice is biometric personal data; an "
    "artefact that could return this is presenter X does not leave the "
    "training run. This is a MOAC criterion — not a hope.'"
)


BELOW_CONFIDENCE_UNMEASURED_NEVER_LABELLED_POSTURE: Final[str] = (
    "CP-AIP-LANGUAGE-COGNITION MUST-DO §5 verbatim (Canon 5 §5.3 · owner "
    "drop §Window-and-span): 'Classification per one-to-two-second window; "
    "deterministic span rule (minimum span duration + hysteresis on label "
    "change) turns windows into language spans. Each span carries its "
    "start and end second (C5.3). A window below the confidence threshold "
    "is unmeasured, NEVER labelled.'"
)


NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE: Final[str] = (
    "CP-AIP-LANGUAGE-COGNITION MUST-DO §7 verbatim (Canon 5 §B5.4 + "
    "Canon 8 §W2 · retagged scope of sealed CP-SO-6.9-LID-WAVE "
    "LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE for language-cognition "
    "artefact): 'On MOAC pass, the model's labels promote from OVERLAY to "
    "MEASURE by a receipted act; regime flag changes; NOTHING is "
    "relabelled.' Sealed anchor: "
    + _LID_NOTHING_RELABELLED_AT_REGIME_FLIP_POSTURE
)


POD_NEVER_DATA_PATH_POSTURE_LANGUAGE_COGNITION: Final[str] = (
    "CP-AIP-LANGUAGE-COGNITION MUST-NOT §6 verbatim (Ruling (b) AKKI-RUNS-"
    "IT 2026-02-23): 'E1's pod is NEVER the training host and NEVER a "
    "data path. Training compute + labelled corpus NEVER leave Akki's "
    "boundary. Registration of training-base MUST refuse pod://* and "
    "/app/* prefixed refs.' Sealed anchor: "
    + _POD_IS_NEVER_DATA_PATH_POSTURE_TRACK_4
)


E1_WIRES_AND_STEPS_BACK_POSTURE_LANGUAGE_COGNITION: Final[str] = (
    "CP-AIP-LANGUAGE-COGNITION MUST-DO §11 verbatim (Ruling (b) verbatim "
    "+ owner drop §Execution-reach): 'Training run executes inside the "
    "Akki perimeter as a commissioned job per Track-4 wiring. Akki runs "
    "it; E1 wires and STEPS BACK.' Sealed anchor: "
    + _E1_STEPS_BACK_AFTER_WIRING_POSTURE
)


TRAINING_ARTEFACT_NEVER_LEAVES_PERIMETER_POSTURE: Final[str] = (
    "CP-AIP-LANGUAGE-COGNITION MUST-DO §9 verbatim (Canon 8 §3 + pilot "
    "licence §8.3): 'Labelled corpus is tenant data — RMS custody class "
    "applies; training inside the perimeter; artefact belongs to RMS "
    "under pilot terms unless elected otherwise; DP-SGD default applies "
    "unless the owner opts out recorded.' Training artefact NEVER leaves "
    "the perimeter."
)


LANGUAGE_COGNITION_SIX_PLUS_ONE_BINDING_POSTURE: Final[Tuple[str, ...]] = (
    "MUST-DO §1: feature basis — signature not prosody alone.",
    "MUST-DO §2: baseline clean named presenter speech + labelled code-switched material per span.",
    "MUST-DO §3: speaker-disjoint splits N≥20 DEFAULT tagged pending.",
    "MUST-DO §4: no-speaker-ID MOAC probe chance-level on held-out presenters.",
    "MUST-DO §5: 1-2s window + deterministic span rule + below-confidence unmeasured.",
    "MUST-DO §6: MOAC ≥90% per-language + ≥85% code-switch-span + no-speaker-ID pass + abstention reported.",
    "MUST-DO §7: B5.4 admission by receipted act, nothing relabelled.",
    "MUST-DO §8: Doc 20 training-base registration extends sealed LID registrations.",
    "MUST-DO §9: RMS custody + in-perimeter training + DP-SGD default.",
    "MUST-DO §10: corpus assembly under census-assistant dialogue.",
    "MUST-DO §11: training run commissioned as Track-4 autonomy job.",
    "MUST-DO §12: sequence — register base → assemble → commission → train → MOAC → admit → promote.",
)


# ---------------------------------------------------------------------------
# Boundary callable — commission_language_cognition_training_run
# ---------------------------------------------------------------------------


def commission_language_cognition_training_run(
    *,
    has_code_switched_material: bool,
    speaker_disjoint_split_ref: str,
    base_registration_ref: str,
    moac_contract_ref: str,
    corpus_assembly_ref: str,
) -> str:
    """Commission a language-cognition Targeta training run.

    Refuses:
    - `has_code_switched_material is False` → `CleanMonolingualOnlyRefused`
      (MUST-NOT §1 owner verbatim).
    - any ref starting with `pod://` or `/app/` → `PodAsDataPathRefused`
      (MUST-NOT §6 Ruling (b) verbatim).

    On success, returns a commission handle string composed of the four
    refs. The actual training run executes as a commissioned Track-4 job
    kind `training_runs` (composed by identity via TRACK_4_JOB_KINDS_ANCHOR).
    E1 wires and STEPS BACK.
    """
    for ref, name in (
        (speaker_disjoint_split_ref, "speaker_disjoint_split_ref"),
        (base_registration_ref, "base_registration_ref"),
        (moac_contract_ref, "moac_contract_ref"),
        (corpus_assembly_ref, "corpus_assembly_ref"),
    ):
        if isinstance(ref, str) and (ref.startswith("pod://") or ref.startswith("/app/")):
            raise PodAsDataPathRefused(
                f"Ruling (b) verbatim: pod is never data path. "
                f"{name}={ref!r} refused at language-cognition commission boundary."
            )
    if not has_code_switched_material:
        raise CleanMonolingualOnlyRefused(
            "MUST-NOT §1 owner verbatim: 'Clean-monolingual alone is a "
            "MUST-NOT for the final model.' Commission refused because "
            "has_code_switched_material is False; the training set MUST "
            "carry labelled code-switched material per span."
        )
    # Success handle — composition of the four refs (opaque)
    return (
        f"lc_training_run://"
        f"{base_registration_ref}|"
        f"{speaker_disjoint_split_ref}|"
        f"{moac_contract_ref}|"
        f"{corpus_assembly_ref}"
    )
