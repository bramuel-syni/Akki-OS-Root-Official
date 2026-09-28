"""W-CENSUS-RUNTIME-ORCHESTRATION · CP-CRO2 · estate_enumerator orchestrator.

Case-agnostic runtime orchestrator.  Walks a caller-provided estate target
list objective-blind, produces one `SourceCandidate` per target, classifies
sensitivity via CP-C1, and registers each via CP-C4
`register_source_candidate`.  A dependency-injected `probe_fn` allows the
caller to fold ffprobe (or any equivalent shape probe) results into the
new `media_types` + `audio_bearing_share` SourceRecord carriers (CP-CRO1
extension).

Discharge anchors (verbatim on single un-wrapped lines):

- Canon-4 §4 (canon/text/Akki_Canon_4_Operating_Engines.txt line 26):
      "The census walks the estate exhaustively and objective-blind, producing one candidate source record per discovered source. It enumerates and classifies; measurement follows separately. Each candidate carries the source reference, its region, the feed identity that keys the declaration baseline, and a deterministically classified sensitivity."

- Canon-4 §5.1 (canon/text/Akki_Canon_4_Operating_Engines.txt line 35):
      "An undeclared feed resolves to unknown, which is the conservative value — absence of a declaration never resolves upward."

- Owner scope-expansion directive verbatim (DECISIONS line 8640):
      "M8 #5 W-CENSUS-RUNTIME-ORCHESTRATION scope EXPANDS per owner ADDITION verbatim: fold ffprobe characterization into live NAS enumeration; new SourceRecord fields media_types + audio_bearing_share become measured census fields (Canon-4 §4.1 + §8 enrichments)."

Contract:

    enumerate_estate(*, run_id, freshness_stamp, targets,
                     probe_fn=None, feed_declaration_registry=None,
                     store) -> List[str]

Where:
    targets                    : Sequence[EstateTarget]
    probe_fn                   : Optional[Callable[[str], Tuple[Tuple[str, ...], Optional[float]]]]
                                 · called once per target with target.sample_ref
                                 · returns (media_types_tuple, audio_bearing_share)
                                 · caller wraps the actual ffprobe / equivalent shell-out
    feed_declaration_registry  : Optional mapping used by CP-C1's classify_sensitivity
                                 · None resolves each target's sensitivity to
                                   Canon-4 §5.1 conservative fallback (unknown)
    store                      : CP-C4 RegistryStore instance (mutated in-place;
                                 written records survive the return)

Returns: list of `record_id` (deterministic sha256-based ids) in target order.

Refusals:
    CensusTargetsEmptyError    on empty targets
    CensusTargetInvalidError   on non-EstateTarget element in targets

Case-agnostic — no executive-domain tokens in the module or in the returned
shapes.  Deterministic — same inputs + same probe_fn returns produce the
same list of record_ids.  Pure orchestration around CP-C1 + CP-C4 seams; no
LLM, no HTTP, no filesystem, no direct ffprobe invocation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple

from contracts.canon_census_source_candidate import SourceCandidate
from services.census_canon.source_candidate_classifier import (
    classify_sensitivity,
)
from services.census_canon.registry_write import (
    RegistryStore,
    register_source_candidate,
)


class CensusTargetsEmptyError(Exception):
    """Raised when `targets` is empty.  Canon-4 §4 says the census walks
    exhaustively; there is nothing to walk when targets is empty, so the
    orchestrator refuses at the boundary rather than emitting an empty
    result.
    """


class CensusTargetInvalidError(Exception):
    """Raised when a `targets` element is not an `EstateTarget` instance."""


@dataclass(frozen=True)
class EstateTarget:
    """A single estate target the orchestrator walks.

    Carriers (four; frozen; owner-ratified extension is a scope-expansion
    event):
      * ``source_reference`` — Canon-4 §4 identity carrier (canonical
        reference for the source).
      * ``region`` — Canon-4 §4 identity carrier.
      * ``feed_identity`` — Canon-4 §4 identity carrier · §5.1 declaration-
        baseline lookup key.
      * ``sample_ref`` — Optional caller-scoped hint the probe_fn uses to
        select a representative sample file for §4.1 probe measurement.
        `None` when no sample is available for probing (Unmeasured path).
    """

    source_reference: str
    region: str
    feed_identity: str
    sample_ref: Optional[str]


ProbeFn = Callable[[str], Tuple[Tuple[str, ...], Optional[float]]]


def _validate_targets(targets: Sequence[EstateTarget]) -> Tuple[EstateTarget, ...]:
    if not targets:
        raise CensusTargetsEmptyError(
            "census orchestrator: targets must be non-empty; got 0 targets"
        )
    coerced = tuple(targets)
    for i, t in enumerate(coerced):
        if not isinstance(t, EstateTarget):
            raise CensusTargetInvalidError(
                f"census orchestrator: targets[{i}] must be an EstateTarget; "
                f"got {type(t).__name__}"
            )
    return coerced


def enumerate_estate(
    *,
    run_id: str,
    freshness_stamp: str,
    targets: Sequence[EstateTarget],
    probe_fn: Optional[ProbeFn] = None,
    feed_declaration_registry: Optional[dict] = None,
    store: RegistryStore,
) -> List[str]:
    """Walk `targets` objective-blind, producing one SourceRecord per
    target via CP-C1 sensitivity + CP-C4 register_source_candidate.

    Optionally folds `probe_fn(sample_ref)` results into the two CP-CRO1
    §4.1 measurement carriers on the record.  When `probe_fn is None` OR
    `target.sample_ref is None`, no probe runs and the CP-CRO1 defaults
    apply (`media_types=()`, `audio_bearing_share=None` — Unmeasured).

    Returns the list of `record_id` values in target order.  Deterministic:
    same inputs (including same `probe_fn` returns) produce the same list
    of ids.

    Pure orchestration — no LLM, no HTTP, no filesystem, no ffprobe
    invocation (the probe_fn is caller-injected; the caller wraps any
    actual shell-out under `readonly_nas_guard`).
    """
    validated = _validate_targets(targets)

    record_ids: List[str] = []
    # CP-C1 classify_sensitivity requires a mapping; None → empty mapping
    # so absence-of-declaration resolves via §5.1 conservative fallback.
    declarations = feed_declaration_registry or {}
    for target in validated:
        # CP-C1 sensitivity classification (Canon-4 §5.1 conservative
        # fallback when the feed is absent from the registry).
        sensitivity = classify_sensitivity(
            feed_identity=target.feed_identity,
            feed_declaration_registry=declarations,
        )
        candidate = SourceCandidate(
            source_reference=target.source_reference,
            region=target.region,
            feed_identity=target.feed_identity,
            sensitivity=sensitivity,
        )

        # CP-CRO1 § 4.1 probe fold (optional).
        if probe_fn is not None and target.sample_ref is not None:
            media_types, audio_bearing_share = probe_fn(target.sample_ref)
        else:
            media_types = ()
            audio_bearing_share = None

        rid = register_source_candidate(
            store=store,
            candidate=candidate,
            run_id=run_id,
            freshness_stamp=freshness_stamp,
            defensibility_measure="rule/first-run/no-measurement-yet",
            media_types=media_types,
            audio_bearing_share=audio_bearing_share,
        )
        record_ids.append(rid)

    return record_ids
