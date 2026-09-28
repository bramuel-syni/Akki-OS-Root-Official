"""M6 · Audio-Plane v1.0 · CP-M6-3-2 · §6.3 P100 four-leakage-path harness.

Harness framework for the §6.3 P100 invariant.  Concrete write-path
refusal logic lands in CP-M6-3-3; §6.4 read-path scope enforcement
lands in CP-M6-3-4.

Discharge anchor (verbatim on single un-wrapped line):

- Audio-Plane §6.3 P100 (V66 · four-leakage-path invariant):
      "The register write path exposes no field through which an instance-level representation can be stored: the schema cannot represent a voiceprint. Unrepresentable, not policed (§1.5). An automated invariant test attempts each known leakage path (small stratum, idiolect marker, narrowing combination, exemplar storage) and must fail to store all of them on every change to the register code."

Owner ruling 2026-09-15T~19:07Z verbatim:
    "the §6.3 P100 four-leakage-path harness is a canon-mandated
    PROTECTIVE mechanism — it builds the refusal guarantees that make
    identity leakage structurally impossible... it does not touch,
    ingest, or expose any biometric data..."

HALT-trigger (verbatim):
    "all harness tests use SYNTHETIC fixtures only... If at ANY point
    in sub-wave 3 (or later: clustering §5.3, voice verification §7) a
    mechanism would require REAL estate voice/biometric material to
    validate, HALT there."

Wave-honest limits:
  - SYNTHETIC FIXTURES ONLY (all provenance_material_ref values carry
    'synthetic' marker).
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Case-agnostic; no executive-domain tokens.

Contract:

    LEAKAGE_PATHS: Tuple[str, ...] — §6.3 P100 verbatim four-tuple in
        verbatim order (small_stratum, idiolect_marker,
        narrowing_combination, exemplar_storage).

    LeakageScenario — 3-carrier frozen dataclass (path_name +
        rationale + attempt_entry).

    LeakageRefusalError — base exception class; concrete subclasses
        land in CP-M6-3-3.

    HarnessAcceptedForbiddenError — raised when a scenario is NOT
        refused (§6.3 P100 invariant fire).

    HarnessRefusalTypeError — raised when a scenario is refused with
        the WRONG exception type (must subclass LeakageRefusalError).

    build_leakage_scenarios() -> Tuple[LeakageScenario, ...] — the
        canonical four synthetic scenarios.

    run_leakage_path_harness(*, write_callable) -> None — runs all
        four scenarios; asserts each is refused with LeakageRefusalError.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Tuple

from services.audio_plane_v1.character_register import (
    CharacterEntry,
    construct_character_entry,
)


LEAKAGE_PATHS: Tuple[str, ...] = (
    "small_stratum",
    "idiolect_marker",
    "narrowing_combination",
    "exemplar_storage",
)


class LeakageRefusalError(Exception):
    """Base class for write-path refusals of leakage-path attempts.

    Concrete subclasses (one per LEAKAGE_PATH, or a shared
    RegisterWriteRefusedError, etc.) land in CP-M6-3-3.  The harness
    contract only requires that any leakage refusal subclass this
    class — so downstream reporting can classify it as a protective
    refusal rather than an accidental failure."""


class HarnessAcceptedForbiddenError(Exception):
    """Raised by `run_leakage_path_harness` when a leakage-path scenario
    is NOT refused by the write callable.  This is the §6.3 P100
    invariant fire — the harness has caught a real leakage-path
    breach in the register code.  Message identifies the accepted
    `path_name` so remediation can target the specific breach."""


class HarnessRefusalTypeError(Exception):
    """Raised by `run_leakage_path_harness` when the write callable
    refuses with the WRONG exception type (i.e., not a subclass of
    `LeakageRefusalError`).  Enforces refusal-type discipline: leakage
    refusals must be classifiable as such by downstream reporting."""


@dataclass(frozen=True)
class LeakageScenario:
    """A single synthetic leakage-path scenario per §6.3 P100.

    Three carriers:
      - `path_name` — one of `LEAKAGE_PATHS`.
      - `rationale` — verbatim §6 canon-anchor label identifying the
        rule violated by this scenario.
      - `attempt_entry` — a schema-valid `CharacterEntry` that the
        write-path MUST refuse.  §5.2 layer validation passes at
        construction time (CP-M6-3-1); the refusal happens at the
        WRITE-PATH (CP-M6-3-3).

    All `attempt_entry.provenance_material_ref` values MUST carry
    the 'synthetic' marker per owner-ratified HALT-trigger.
    """

    path_name: str
    rationale: str
    attempt_entry: CharacterEntry


def build_leakage_scenarios() -> Tuple[LeakageScenario, ...]:
    """Return the canonical four synthetic scenarios per §6.3 P100.

    Order matches `LEAKAGE_PATHS` (verbatim §6.3 P100 order).  Every
    scenario's `attempt_entry` is SYNTHETIC — no real-estate biometric
    material referenced.
    """
    return (
        LeakageScenario(
            path_name="small_stratum",
            rationale=(
                "§6.2 P096 cond-2: 'Shared. Observed across at least N "
                "distinct speakers.' A single-speaker stratum violates "
                "this condition."
            ),
            attempt_entry=construct_character_entry(
                attribute_name="synthetic_hyper_narrow_variant_alpha",
                layer="phonetic",
                description=(0.5,),
                provenance_material_ref="mat://synthetic/small_stratum",
                occurrence_count=1,
                n_distinct_speakers=1,  # violation: N < any reasonable threshold
                is_learned=True,
            ),
        ),
        LeakageScenario(
            path_name="idiolect_marker",
            rationale=(
                "§6.4 P102 verbatim: 'Habitual fillers, characteristic "
                "phrasings, and idiosyncratically pronounced words are "
                "learned but individuating. They fail condition 2 or 3 "
                "and are excluded.'"
            ),
            attempt_entry=construct_character_entry(
                attribute_name="synthetic_idiolect_habitual_filler_pattern",
                layer="phonetic",
                description=(0.7, 0.65, 0.72),
                provenance_material_ref="mat://synthetic/idiolect",
                occurrence_count=100,
                n_distinct_speakers=1,  # individuating · violates cond-2 via idiolect
                is_learned=True,
            ),
        ),
        LeakageScenario(
            path_name="narrowing_combination",
            rationale=(
                "§6.2 P097 cond-3: 'Non-reconstructive in combination. "
                "Tested against attribute combinations, not attributes in "
                "isolation: language + region + age band + one "
                "distinctive feature can reach a single person even when "
                "each attribute is group-level.'"
            ),
            attempt_entry=construct_character_entry(
                attribute_name=(
                    "synthetic_narrowing_combo::lang_x::region_y::"
                    "age_band_z::distinctive_feature_q"
                ),
                layer="phonetic",
                description=(0.9, 0.8, 0.7, 0.6, 0.5),
                provenance_material_ref="mat://synthetic/narrowing_combo",
                occurrence_count=3,
                n_distinct_speakers=2,  # not tiny in isolation · but combo re-identifies
                is_learned=True,
            ),
        ),
        LeakageScenario(
            path_name="exemplar_storage",
            rationale=(
                "§6.2 P098 cond-4: 'Stored as description, not exemplar. "
                "Centroids, distributions, frequencies. Never stored "
                "audio; never per-utterance speaker embeddings. "
                "Embeddings used during clustering are destroyed after "
                "cluster assignment.'"
            ),
            attempt_entry=construct_character_entry(
                attribute_name=(
                    "synthetic_exemplar_dense_512d_utterance_embedding"
                ),
                layer="phonetic",
                # Exemplar-like dense vector (deterministic synthetic
                # fixture; no real embedding).
                description=tuple(0.1 for _ in range(512)),
                provenance_material_ref="mat://synthetic/exemplar",
                occurrence_count=1,
                n_distinct_speakers=1,  # per-utterance · exemplar
                is_learned=True,
            ),
        ),
    )


def run_leakage_path_harness(
    *,
    write_callable: Callable[[CharacterEntry], None],
) -> None:
    """Run the §6.3 P100 four-leakage-path invariant against
    `write_callable`.

    For each scenario in `build_leakage_scenarios()`:
      - Submit `scenario.attempt_entry` to `write_callable`.
      - If the callable raises `LeakageRefusalError` (or any subclass) —
        the leakage is refused; continue.
      - If the callable raises any OTHER exception type — raise
        `HarnessRefusalTypeError` (refusal-type discipline breach).
      - If the callable returns normally — raise
        `HarnessAcceptedForbiddenError` naming the accepted `path_name`
        (this is the §6.3 P100 invariant fire).
    """
    for scenario in build_leakage_scenarios():
        try:
            write_callable(scenario.attempt_entry)
        except LeakageRefusalError:
            continue
        except Exception as exc:
            raise HarnessRefusalTypeError(
                f"Leakage-path {scenario.path_name!r} refused with wrong "
                f"exception type: expected LeakageRefusalError subclass, "
                f"got {type(exc).__name__}: {exc}"
            ) from exc
        else:
            # No exception raised → forbidden pattern was accepted → §6.3 P100 fire.
            raise HarnessAcceptedForbiddenError(
                f"§6.3 P100 invariant FIRE: leakage-path "
                f"{scenario.path_name!r} was NOT refused. "
                f"Rationale: {scenario.rationale}"
            )
