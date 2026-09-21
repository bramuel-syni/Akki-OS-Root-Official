"""M6 · Audio-Plane v1.0 · CP-M6-6-1 · Objective Wizard audio-variant compile-refusal + Rec-1-M6SW6 gate.

Discharge anchors (verbatim on single un-wrapped lines):

- Audio-Plane §8.4 P139 (V89 · compile-time rejection preamble):
      "The wizard cannot emit an artifact the downstream contracts would refuse. Rejected at compile, not warned:"

- Audio-Plane §8.4 P140 (V90 · rejection 1):
      "An Outcome without an existing test_set_ref."

- Audio-Plane §8.4 P141 (V91 · rejection 2):
      "An acceptance bar missing the per-stratum dimension."

- Audio-Plane §8.4 P142 (V92 · rejection 3):
      "A Collection Schema requiring a column whose capture violates the custody conditions of §6.2."

- Audio-Plane §8.1 P125 (V78 · Objective Wizard as shaping-wizard variant):
      "No business user hand-writes a Target Outcome. The Objective Wizard — a new variant of the existing shaping wizard, reusing its agent interface, guards, session persistence, and ledger sidecar — elicits an objective in plain language and compiles two governed artifacts:"

- Owner ruling 2026-09-15T~21:25Z verbatim (Rec-1-M6SW6 mandatory write-path gate):
      "Rec 1 RATIFIED — wire assert_cluster_carries_no_human_name into sub-wave 6's objective→cluster write path as a mandatory gate, not a downstream check. Make it an explicit invariant in the sub-wave 6 brief."

- Audio-Plane §5.3 P089 (V59 · clause 2 · discipline gate cross-referenced by Rec-1-M6SW6):
      "A cluster asserts that a distinct variant exists — not what it is called."

Wave-honest limits:
  - No LLM invocation.  No HTTP call.  No filesystem write.
  - Objective Wizard STUB territory only: `TargetOutcomeStub` is a
    STUB carrier — the full §10 TargetOutcome lands at sub-wave 7
    CP-M6-7-1.  The compile-refusal contract composes with the
    future full carrier without breaking (STUB has all fields the
    compile-refusal reads; full carrier is a superset).
  - `CollectionSchemaColumnStub.captures_custody_violating_field` is
    a MARKER field — sub-wave 6 does not re-import §6.2 conditions.
    A future CP wire may promote this marker to a live §6.2 check
    without breaking the sub-wave 6 refusal contract.
  - §3.1 P038 tokens-not-waveforms discipline preserved (no
    audio_bytes / waveform / samples / raw_audio / voiceprint /
    speaker_embedding carriers on any surface).
  - Synthetic-fixtures-only in tests.

Contract:

    AcceptanceBar — frozen 2-carrier:
      has_per_stratum_dimension · per_stratum_thresholds.

    TargetOutcomeStub — frozen 3-carrier:
      outcome_id · test_set_ref · acceptance_bar.

    CollectionSchemaColumnStub — frozen 3-carrier:
      column_name · captures_custody_violating_field · bound_cluster.

    compile_objective_artifact(*, outcome, columns) -> None
      Refuses at compile with one of four errors in this order
      (P036 receipt-before-result carrier discipline):
        1. `TargetOutcomeMissingTestSetRefError` (V90)
        2. `AcceptanceBarMissingPerStratumDimensionError` (V91)
        3. `CollectionSchemaCustodyViolationError` (V92)
        4. `CollectionSchemaClusterHumanNameLeakError` (Rec-1-M6SW6)
      First refusal wins; no partial success.

Refusals (4):
    TargetOutcomeMissingTestSetRefError ·
    AcceptanceBarMissingPerStratumDimensionError ·
    CollectionSchemaCustodyViolationError ·
    CollectionSchemaClusterHumanNameLeakError.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Tuple

from services.audio_plane_v1.cluster_stability import (
    ClusterHumanNameLeakError,
    assert_cluster_carries_no_human_name,
)


class TargetOutcomeMissingTestSetRefError(Exception):
    """Raised when a `TargetOutcomeStub` has `test_set_ref is None`.

    Audio-Plane §8.4 P140 verbatim: 'An Outcome without an existing
    test_set_ref.'  Cross-anchored to §10.1 P161 (LOAD-BEARING):
    'must exist before the Outcome is accepted.'"""


class AcceptanceBarMissingPerStratumDimensionError(Exception):
    """Raised when an `AcceptanceBar.has_per_stratum_dimension` is
    False (or the outcome has no acceptance_bar at all).

    Audio-Plane §8.4 P141 verbatim: 'An acceptance bar missing the
    per-stratum dimension.'  Cross-anchored to §10.2 P167: 'Acceptance
    is per stratum. A single global threshold hides the failure that
    matters'."""


class CollectionSchemaCustodyViolationError(Exception):
    """Raised when a `CollectionSchemaColumnStub.captures_custody_violating_field`
    is True.

    Audio-Plane §8.4 P142 verbatim: 'A Collection Schema requiring a
    column whose capture violates the custody conditions of §6.2.'
    Cross-anchored to §6.2 custody conditions (four-conjunctive
    conditions) enforced at CP-M6-3-3 register write-boundary."""


class CollectionSchemaClusterHumanNameLeakError(Exception):
    """Raised when a `CollectionSchemaColumnStub.bound_cluster` is
    non-None and carries a human-readable name via any attribute in
    `HUMAN_NAME_ATTRIBUTE_NAMES` (from CP-M6-5-3
    `services.audio_plane_v1.cluster_stability`).

    Owner ruling 2026-09-15T~21:25Z (Rec-1-M6SW6) verbatim:
    'wire assert_cluster_carries_no_human_name into sub-wave 6's
    objective→cluster write path as a mandatory gate, not a
    downstream check.'

    Cross-anchored to §5.3 P089 clause 2 verbatim: 'A cluster asserts
    that a distinct variant exists — not what it is called.'

    This is a WRITE-PATH invariant: the Objective Wizard cannot emit
    an artifact whose downstream data-plane contracts would surface a
    human-readable cluster name.  Any objective→cluster binding is
    refused at compile if the cluster carrier surfaces a human-readable
    name."""


@dataclass(frozen=True)
class AcceptanceBar:
    """Per-stratum acceptance bar carrier.

    §8.4 P141 verbatim: 'An acceptance bar missing the per-stratum
    dimension.'  §10.2 P167 verbatim: 'Acceptance is per stratum.'

    Two carriers:
      - `has_per_stratum_dimension` — True iff the acceptance bar
        has per-stratum thresholds (as opposed to a single global
        threshold).  False marks an acceptance bar that fails V91.
      - `per_stratum_thresholds` — immutable tuple of (stratum_id,
        accuracy, coverage) tuples.  §10.1 P159 verbatim: 'threshold
        per stratum; two-dimensional (accuracy, coverage)'.  Empty
        tuple when `has_per_stratum_dimension=False`.
    """

    has_per_stratum_dimension: bool
    per_stratum_thresholds: Tuple[Tuple[str, float, float], ...]


@dataclass(frozen=True)
class TargetOutcomeStub:
    """STUB Target Outcome carrier for CP-M6-6-1 compile-refusal
    territory.

    §8.1 P126 verbatim: 'TargetOutcome (§10) — handed to the Training
    Planner.'  This is a STUB — the full §10 TargetOutcome carrier
    lands at sub-wave 7 CP-M6-7-1 with all seven fields (task, domain,
    population, acceptance, gate_policy, test_set_ref, constraints).
    CP-M6-6-1 only needs the three fields the compile-refusal reads:
    outcome_id, test_set_ref, acceptance_bar.

    Three carriers:
      - `outcome_id` — opaque identifier.
      - `test_set_ref` — §10.1 P161 verbatim (LOAD-BEARING): 'must
        exist before the Outcome is accepted.'  None marks the V90
        refusal trigger.
      - `acceptance_bar` — `AcceptanceBar` or None.  None (or
        `has_per_stratum_dimension=False`) marks the V91 refusal
        trigger.
    """

    outcome_id: str
    test_set_ref: Optional[str]
    acceptance_bar: Optional[AcceptanceBar]


@dataclass(frozen=True)
class CollectionSchemaColumnStub:
    """STUB Collection Schema column carrier for CP-M6-6-1
    compile-refusal territory.

    §9.1 P148 verbatim: 'The declared data dictionary of a
    commission: what is extracted from the sound, for what purpose,
    at what quality bar.'  This is a STUB — the full §9
    CollectionSchemaColumn lands at CP-M6-6-2 (this same sub-wave)
    with the two-tier (baseline/objective) discipline.  CP-M6-6-1
    only needs the three fields the compile-refusal reads.

    Three carriers:
      - `column_name` — opaque column identifier.
      - `captures_custody_violating_field` — MARKER field.
        §8.4 P142 verbatim: 'A Collection Schema requiring a column
        whose capture violates the custody conditions of §6.2.'
        True marks the V92 refusal trigger.  Sub-wave 6 does not
        re-import §6.2 conditions — a future CP wire may promote
        this marker to a live §6.2 check (from CP-M6-3-3 register
        write-boundary) without breaking the sub-wave 6 refusal
        contract.
      - `bound_cluster` — Optional cluster-like object the column
        binds to.  None marks an unbound column (legitimate at
        qualify/graduate stage per §8.3 P135..P136).  Non-None
        triggers the Rec-1-M6SW6 gate against
        `assert_cluster_carries_no_human_name`.
    """

    column_name: str
    captures_custody_violating_field: bool
    bound_cluster: Optional[Any]


def compile_objective_artifact(
    *,
    outcome: TargetOutcomeStub,
    columns: Tuple[CollectionSchemaColumnStub, ...],
) -> None:
    """Compile the objective artifact; refuse at compile if any
    downstream-contract violation is present.

    §8.4 P139 verbatim preamble: 'The wizard cannot emit an artifact
    the downstream contracts would refuse. Rejected at compile, not
    warned:'

    Refusal ordering (P036 receipt-before-result carrier discipline):
      1. V90 — test_set_ref absent.
      2. V91 — acceptance bar missing per-stratum dimension.
      3. V92 — collection schema custody violation (per-column).
      4. Rec-1-M6SW6 — collection schema cluster human-name leak
         (per-column).

    First refusal wins; no partial success.  Returns None on pass.
    """
    # V90 · §8.4 P140: 'An Outcome without an existing test_set_ref.'
    if outcome.test_set_ref is None:
        raise TargetOutcomeMissingTestSetRefError(
            f"compile_objective_artifact: outcome "
            f"{outcome.outcome_id!r} has no test_set_ref; §8.4 P140 "
            f"verbatim: 'An Outcome without an existing test_set_ref.'"
        )

    # V91 · §8.4 P141: 'An acceptance bar missing the per-stratum
    # dimension.'
    if (
        outcome.acceptance_bar is None
        or not outcome.acceptance_bar.has_per_stratum_dimension
    ):
        raise AcceptanceBarMissingPerStratumDimensionError(
            f"compile_objective_artifact: outcome "
            f"{outcome.outcome_id!r} has no per-stratum acceptance "
            f"dimension; §8.4 P141 verbatim: 'An acceptance bar "
            f"missing the per-stratum dimension.'"
        )

    # V92 · §8.4 P142: 'A Collection Schema requiring a column whose
    # capture violates the custody conditions of §6.2.'
    for col in columns:
        if col.captures_custody_violating_field:
            raise CollectionSchemaCustodyViolationError(
                f"compile_objective_artifact: column "
                f"{col.column_name!r} captures a custody-violating "
                f"field; §8.4 P142 verbatim: 'A Collection Schema "
                f"requiring a column whose capture violates the "
                f"custody conditions of §6.2.'"
            )

    # Rec-1-M6SW6 · owner ruling 2026-09-15T~21:25Z: 'wire
    # assert_cluster_carries_no_human_name into sub-wave 6's
    # objective→cluster write path as a mandatory gate, not a
    # downstream check.'
    for col in columns:
        if col.bound_cluster is None:
            # Unbound column — legitimate at qualify/graduate stage
            # per §8.3 P135..P136.
            continue
        try:
            assert_cluster_carries_no_human_name(
                cluster=col.bound_cluster,
            )
        except ClusterHumanNameLeakError as exc:
            raise CollectionSchemaClusterHumanNameLeakError(
                f"compile_objective_artifact: column "
                f"{col.column_name!r} bound_cluster exposes a "
                f"human-readable name; §5.3 clause 2 verbatim: 'A "
                f"cluster asserts that a distinct variant exists — "
                f"not what it is called'; downstream: {exc}"
            ) from exc
    return None
