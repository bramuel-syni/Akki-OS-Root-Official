"""W-CENSUS-SUPPLEMENT-AUDIO-INVENTORY-MOUNT · CP-CSAIM1.

Mounts the two audio-plane connectors (NAS 16ch + OBS google-transcripts)
into the CP-C4 census `RegistryStore` as first-class `SourceRecord`s,
discharging the no-live-scan-tool unmeasured-with-reason entries the
Item-3 census run banked for these two connectors at
`notes/ITEM_3_CENSUS_RUN_20260915.md` §D rows 3-4.

Owner directive verbatim (course-correction 2026-09-15T~08:37Z clause a):
    "(a) census supplement for NAS+OBS via the sealed audio_poc
     inventories mounted into the census registry (do not defer to M8)"

Grounding brief: notes/wave_census_supplement_grounding_brief.md

Canon anchors (verbatim, per Verbatim-canon standing rule):

Canon-4 §4 (canon/text/Akki_Canon_4_Operating_Engines.txt:26):
    "The census walks the estate exhaustively and objective-blind,
     producing one candidate source record per discovered source. It
     enumerates and classifies; measurement follows separately. Each
     candidate carries the source reference, its region, the feed
     identity that keys the declaration baseline, and a deterministically
     classified sensitivity."

Canon-4 §5.1 (line 35, verbatim conservative-fallback clause):
    "An undeclared feed resolves to unknown, which is the conservative
     value - absence of a declaration never resolves upward."

Canon-4 §8 (canon/text/Akki_Canon_4_Operating_Engines.txt:51):
    "One record per source, carrying existence, sensitivity, the
     defensibility measure, and a freshness stamp. This is the interface
     targeting and convergence both read."

W-AUDIO-POC seal (phase0/output_verified_seals/audio_poc_v1.seal.txt ·
Sealed-at-utc 2026-09-14T13:58:45Z · Kind `audio_poc_wave_close`):
    CP-A2 (13 invariants) landed the recording_inventory contract
    (services/audio_poc/recording_inventory.py). CP-A3 (13 invariants)
    landed the transcript_inventory contract
    (services/audio_poc/transcript_inventory.py). Both are the "sealed
    audio_poc inventories" the owner names in directive clause (a).
    They carry the parse + canonical-key + snapshot-fingerprint contracts
    that a live SMB/OBS scan tool will feed once M8
    W-CENSUS-RUNTIME-ORCHESTRATION wires it in.

Design:

  * The two SourceRecords written by this supplement are placeholders
    marking the two audio-plane connectors as registered-but-unenumerated.
    Their `defensibility_measure` field points to the sealed CP-A2/A3
    contract modules + the audio_poc_v1 wave seal, per wave-honest-limit
    E.1 (first-run shape).
  * `next_recheck_hint` on both records points to M8
    W-CENSUS-RUNTIME-ORCHESTRATION, the follow-on wave that lands live
    SMB/OBS enumeration.  Post-M8, correction records with
    `supersedes_record_id` set will land per CP-C4 E.5 append-only
    discipline (Canon-3 §9.3 spirit).
  * Sensitivity classification uses the CP-C1 classifier with an empty
    feed_declaration_registry -> Canon-4 §5.1 conservative fallback
    ("unknown", is_undeclared=True) for both connectors.
"""

from __future__ import annotations

from contracts.canon_census_source_candidate import SourceCandidate

from services.census_canon.registry_write import (
    RegistryStore,
    register_source_candidate,
)
from services.census_canon.source_candidate_classifier import (
    classify_sensitivity,
)


# Canonical feed_identity tokens (Canon-4 §4 "feed identity that keys the
# declaration baseline").  Byte-identical strings; renames must be tracked
# in a delta grounding brief.
NAS_FEED_IDENTITY: str = "audio_nas_offairrecs_16ch"
OBS_FEED_IDENTITY: str = "obs_google_transcripts_bucket"

# Canonical source_reference shapes (Canon-4 §4 "source reference").  Match
# the parse regex shapes of the sealed CP-A2/A3 contracts:
#   * NAS: services/audio_poc/recording_inventory.py:26-28 _PATH_REGEX
#     canonical shape "/OFFAIRRECS/Record/channel<NN>/<YYYYMMDD>_<HHMM>_
#     <stem>.<ext>"
#   * OBS: services/audio_poc/transcript_inventory.py:20-22 _OBS_KEY_REGEX
#     canonical shape "<station>/<YYYYMMDD>/<YYYYMMDD>_<HHMM>_<stem>.json"
# The trailing template placeholders (channel_dir / channel / date / key)
# stay templated because this supplement is the registration point, not the
# scan point -- concrete per-file source_references land when the live
# scanner runs (M8 W-CENSUS-RUNTIME-ORCHESTRATION).
NAS_SOURCE_REFERENCE: str = "nas://OFFAIRRECS/Record/{channel_dir}"
OBS_SOURCE_REFERENCE: str = "obs://google-transcripts/{channel}/{date}/{key}"

# Region tag for the audio plane (Canon-4 §4 "region" carrier +
# Audio-Plane-v1 §1.2 no-parallel-machinery: NAS + OBS share one region).
NAS_REGION: str = "estate.audio_plane"
OBS_REGION: str = "estate.audio_plane"

# Defensibility measure (Canon-4 §8 field, first-run shape per
# grounding-brief §E.1).  Pointers to the sealed CP-A2 / CP-A3 contracts +
# the audio_poc_v1 wave seal.
NAS_DEFENSIBILITY_MEASURE: str = (
    "sealed_cp_a2_recording_inventory@audio_poc_v1.seal"
)
OBS_DEFENSIBILITY_MEASURE: str = (
    "sealed_cp_a3_transcript_inventory@audio_poc_v1.seal"
)

# next_recheck_hint points to the follow-on wave that lands live
# enumeration (DECISIONS 2026-09-15T~04:12Z §Δ5).
NEXT_RECHECK_HINT_M8: str = "M8·W-CENSUS-RUNTIME-ORCHESTRATION"


def mount_audio_inventory_into_census(
    *,
    store: RegistryStore,
    run_id: str,
    freshness_stamp: str,
) -> tuple[str, str]:
    """Mount NAS + OBS into `store` as two `SourceRecord`s under `run_id`.

    Args:
      store: the CP-C4 `RegistryStore` to append into.
      run_id: caller-supplied `CensusRunId` (produced by CP-C3
        `generate_census_run_id`) that this supplement writes under.
      freshness_stamp: ISO 8601 timestamp for the write's freshness
        (Canon-4 §8 freshness carrier).

    Returns:
      Tuple `(nas_record_id, obs_record_id)`.  Both start with `"rec_"`
      and are deterministic over the input tuple: calling this function
      twice with identical (store's prior state included) inputs returns
      the same two ids and leaves `store.count()` unchanged (E.5
      append-only + CP-C4 idempotency).

    Notes:
      Sensitivity for both connectors resolves via the Canon-4 §5.1
      conservative fallback -- the feed_declaration_registry is empty
      because audio-plane sensitivity declarations have not yet been
      published (owner-desk item, tracked at DECISIONS 2026-09-15T~04:12Z
      §Δ6).  Post-declaration, correction records with
      `supersedes_record_id` set will land per E.5.
    """
    empty_registry: dict[str, str] = {}

    nas_candidate = SourceCandidate(
        source_reference=NAS_SOURCE_REFERENCE,
        region=NAS_REGION,
        feed_identity=NAS_FEED_IDENTITY,
        sensitivity=classify_sensitivity(
            feed_identity=NAS_FEED_IDENTITY,
            feed_declaration_registry=empty_registry,
        ),
    )
    obs_candidate = SourceCandidate(
        source_reference=OBS_SOURCE_REFERENCE,
        region=OBS_REGION,
        feed_identity=OBS_FEED_IDENTITY,
        sensitivity=classify_sensitivity(
            feed_identity=OBS_FEED_IDENTITY,
            feed_declaration_registry=empty_registry,
        ),
    )

    nas_record_id = register_source_candidate(
        store=store,
        candidate=nas_candidate,
        run_id=run_id,
        freshness_stamp=freshness_stamp,
        defensibility_measure=NAS_DEFENSIBILITY_MEASURE,
        next_recheck_hint=NEXT_RECHECK_HINT_M8,
        supersedes_record_id=None,
    )
    obs_record_id = register_source_candidate(
        store=store,
        candidate=obs_candidate,
        run_id=run_id,
        freshness_stamp=freshness_stamp,
        defensibility_measure=OBS_DEFENSIBILITY_MEASURE,
        next_recheck_hint=NEXT_RECHECK_HINT_M8,
        supersedes_record_id=None,
    )
    return nas_record_id, obs_record_id
