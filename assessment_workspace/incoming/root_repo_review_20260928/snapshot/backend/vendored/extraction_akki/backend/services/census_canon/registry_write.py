"""W-CENSUS-CANON-ALIGN · CP-C4 · Append-only registry write path.

W-CENSUS-RUNTIME-ORCHESTRATION · CP-CRO1 extension (sealed 2026-09-15T~17:xxZ):
`SourceRecord` extended from 10 → 12 carriers with two §4.1 measurement
fields (`media_types`, `audio_bearing_share`) per owner scope-expansion
directive 2026-09-15T~11:05Z (DECISIONS line 8640).  Both fields are
Optional-default so pre-CRO1 writes still succeed unchanged.

Canon anchors (verbatim quotes carried by this docstring per the
Verbatim-canon standing rule · DECISIONS.md 2026-09-15T~01:40Z):

Canon-4 §4.1 (canon/text/Akki_Canon_4_Operating_Engines.txt:28):
    "Per source and per stratum: volume, media types, languages, era
     distribution, quality strata, the share already verified, the share
     carrying personal data, the share licensed for external use — and,
     explicitly, what has not been measured."

Canon-4 §8 (canon/text/Akki_Canon_4_Operating_Engines.txt:51):
    "One record per source, carrying existence, sensitivity, the
     defensibility measure, and a freshness stamp. This is the interface targeting and convergence both read."

Master Requirements Registry Doc-10 A5.5 (canon/drops/20260910/extracted/text/Master_Requirements_Registry.md:155):
    "The Registry is one record, read by many"

Wave-honest-limit E.5 (notes/wave_census_canon_align_grounding_brief.md):
    "Registry-write is append-only. No update path this wave. A source-
     record correction lands as a new record with a link to the superseded
     record (Canon-3 §9.3 append-only ledger spirit precedent from CP-D5)."

Wave-honest-limit E.1 (notes/wave_census_canon_align_grounding_brief.md):
    "First-run shape acceptable for B5.6 (freshness). Full structural-delta
     freshness mechanism is out-of-scope this wave; a `freshness_stamp`
     field on the source record + a `next_recheck_hint` field are the
     first-run shape."

Design (bindings):

  * `SourceRecord` — frozen dataclass.  Canon §8 explicitly names four
    carrier concepts.  `existence` is encoded implicitly by presence in the
    `RegistryStore` (there is no `existence: bool` field; the record
    presence-in-store IS its existence).  `sensitivity`,
    `defensibility_measure`, `freshness_stamp` are explicit fields.
    Identity carriers from `SourceCandidate` (source_reference / region /
    feed_identity) + CP-C3 linkage (`census_run_id`) + `record_id` +
    correction-chain link (`supersedes_record_id`) + first-run freshness
    hint (`next_recheck_hint`) form the CP-C4 10 carriers.  CP-CRO1 adds
    `media_types` (Tuple[str, ...] default empty tuple) +
    `audio_bearing_share` (Optional[float] default None) as §4.1 media-
    type + quality-strata measurement carriers.
  * `RegistryStore` — in-memory dict of {record_id: SourceRecord}.  The
    store is append-only by construction: `write` refuses to overwrite an
    existing record_id (idempotent on identical writes; distinct
    supersession writes land with a distinct id).  No update / delete API
    exposed.
  * `register_source_candidate(...)` — the write path.  Returns a
    deterministic record_id (sha256 over canonical JSON of the input
    tuple), so identical writes are idempotent and correction writes
    (with `supersedes_record_id` set) land under a distinct id.  CP-CRO1
    extends the input tuple to include `media_types` +
    `audio_bearing_share`, so records with different probe data get
    distinct ids (§4.1 measurement participates in identity).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, Optional, Sequence, Tuple

from contracts.canon_census_source_candidate import (
    Sensitivity,
    SourceCandidate,
)


@dataclass(frozen=True)
class SourceRecord:
    """A written registry record per Canon-4 §8 verbatim (CP-CRO1 12-carrier
    shape).

    Twelve carriers total:
      * ``record_id`` — deterministic id produced by
        ``register_source_candidate``.
      * ``source_reference`` / ``region`` / ``feed_identity`` — identity
        carriers lifted from the `SourceCandidate` (CP-C1).
      * ``sensitivity`` — the CP-C1 `Sensitivity` value (Canon-4 §8 field).
      * ``defensibility_measure`` — rule reference string (Canon-4 §8
        field).  First-run shape; full defensibility engine is a later wave.
      * ``freshness_stamp`` — ISO 8601 timestamp of the write (Canon-4 §8
        field).
      * ``next_recheck_hint`` — optional next-recheck hint (E.1 first-run
        shape, `None` for records with no scheduled recheck).
      * ``census_run_id`` — CP-C3 `CensusRunId` that produced this write.
      * ``supersedes_record_id`` — E.5 correction-chain link; `None` for
        original records, set for correction records.
      * ``media_types`` — Canon-4 §4.1 P28 media-types measurement carrier
        (CP-CRO1).  Tuple of media-type descriptor strings (e.g.
        ``("audio/aac",)`` or ``("video/h264+aac-null",)``).  Default empty
        tuple = Unmeasured per §4.1 P29 "Unmeasured is a first-class
        value".
      * ``audio_bearing_share`` — Canon-4 §4.1 quality-strata measurement
        for the audio-bearing fraction (CP-CRO1).  ``None`` = Unmeasured;
        float in [0.0, 1.0] when measured.
    """

    record_id: str
    source_reference: str
    region: str
    feed_identity: str
    sensitivity: Sensitivity
    defensibility_measure: str
    freshness_stamp: str
    next_recheck_hint: Optional[str]
    census_run_id: str
    supersedes_record_id: Optional[str]
    # CP-CRO1 § 4.1 additions:
    media_types: Tuple[str, ...] = ()
    audio_bearing_share: Optional[float] = None


class RegistryStore:
    """Append-only in-memory registry store.

    Public API is deliberately narrow: `write` (append-only), `read`
    (retrieve by id), `count` (size), `has` (membership).  No update, no
    delete.  Corrections come in as NEW records with `supersedes_record_id`
    pointing back to the superseded record (see `register_source_candidate`
    below).
    """

    def __init__(self) -> None:
        self._records: Dict[str, SourceRecord] = {}

    def write(self, record: SourceRecord) -> None:
        """Idempotent append.  Writing a record whose id already exists in
        the store is a no-op iff the incoming record is byte-identical to
        the stored one; a byte-DIFFERENT record under the same id would
        indicate a determinism failure in `register_source_candidate` and
        MUST NOT overwrite the stored value.
        """
        existing = self._records.get(record.record_id)
        if existing is None:
            self._records[record.record_id] = record
            return
        if existing == record:
            return  # idempotent no-op
        raise RegistryDeterminismFailure(
            f"Registry write refused: record_id={record.record_id!r} already "
            f"present with different content.  Determinism of "
            f"`register_source_candidate` is violated.  "
            f"E.5 append-only invariant preserved."
        )

    def read(self, record_id: str) -> SourceRecord:
        return self._records[record_id]

    def has(self, record_id: str) -> bool:
        return record_id in self._records

    def count(self) -> int:
        return len(self._records)


class RegistryDeterminismFailure(Exception):
    """Raised when a write would overwrite an existing record with byte-
    different content — indicates the record_id gen is not deterministic.
    Preserves the E.5 append-only invariant by refusing rather than
    overwriting.
    """


def _compute_record_id(
    *,
    candidate: SourceCandidate,
    run_id: str,
    freshness_stamp: str,
    defensibility_measure: str,
    next_recheck_hint: Optional[str],
    supersedes_record_id: Optional[str],
    media_types: Tuple[str, ...],
    audio_bearing_share: Optional[float],
) -> str:
    """Deterministic record-id gen (CP-CRO1 extended tuple).

    Canonicalises the input tuple into a stable JSON form and hashes with
    sha256.  Same inputs → same record_id (idempotent); any input change →
    distinct id (correction records with `supersedes_record_id` set differ
    from originals even when candidate + run + freshness_stamp match — the
    supersession field is part of the input tuple).

    CP-CRO1: `media_types` + `audio_bearing_share` participate in the
    hash, so records with different probe data get distinct ids (§4.1
    measurement participates in record identity).
    """
    payload = {
        "source_reference": candidate.source_reference,
        "region": candidate.region,
        "feed_identity": candidate.feed_identity,
        "sensitivity_class_label": candidate.sensitivity.class_label,
        "sensitivity_is_undeclared": candidate.sensitivity.is_undeclared,
        "sensitivity_rule_reference": candidate.sensitivity.rule_reference,
        "run_id": run_id,
        "freshness_stamp": freshness_stamp,
        "defensibility_measure": defensibility_measure,
        "next_recheck_hint": next_recheck_hint,
        "supersedes_record_id": supersedes_record_id,
        # CP-CRO1 additions:
        "media_types": list(media_types),
        "audio_bearing_share": audio_bearing_share,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"rec_{digest}"


def register_source_candidate(
    *,
    store: RegistryStore,
    candidate: SourceCandidate,
    run_id: str,
    freshness_stamp: str,
    defensibility_measure: str,
    next_recheck_hint: Optional[str] = None,
    supersedes_record_id: Optional[str] = None,
    media_types: Sequence[str] = (),
    audio_bearing_share: Optional[float] = None,
) -> str:
    """Register a `SourceCandidate` into the registry store.

    Returns the deterministic `record_id`.  Writing the same input tuple
    twice is idempotent (no duplicate entry, no mutation).  A correction
    write passes `supersedes_record_id` pointing back to the original;
    the correction lands under a distinct id and both records remain
    retrievable.

    CP-CRO1: optional `media_types` (Sequence[str] · coerced to Tuple[str,
    ...]) + `audio_bearing_share` (Optional[float]) kwargs land on the
    written record's §4.1 measurement carriers.
    """
    media_types_t: Tuple[str, ...] = tuple(media_types)
    record_id = _compute_record_id(
        candidate=candidate,
        run_id=run_id,
        freshness_stamp=freshness_stamp,
        defensibility_measure=defensibility_measure,
        next_recheck_hint=next_recheck_hint,
        supersedes_record_id=supersedes_record_id,
        media_types=media_types_t,
        audio_bearing_share=audio_bearing_share,
    )
    record = SourceRecord(
        record_id=record_id,
        source_reference=candidate.source_reference,
        region=candidate.region,
        feed_identity=candidate.feed_identity,
        sensitivity=candidate.sensitivity,
        defensibility_measure=defensibility_measure,
        freshness_stamp=freshness_stamp,
        next_recheck_hint=next_recheck_hint,
        census_run_id=run_id,
        supersedes_record_id=supersedes_record_id,
        media_types=media_types_t,
        audio_bearing_share=audio_bearing_share,
    )
    store.write(record)
    return record_id
