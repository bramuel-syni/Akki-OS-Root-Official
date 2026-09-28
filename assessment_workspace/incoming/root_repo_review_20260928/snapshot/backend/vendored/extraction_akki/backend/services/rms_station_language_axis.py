"""CP-CENSUS-RMS-STATION-LANGUAGE-AXIS · additive census-model service.

Owner directive verbatim (2026-02-23 · mid-P4-d-i-seal · this-turn):
    'Audio - there are local language sample per station - each station represents local language - all research with title - eg inoro is kikuyu, ramogi is luo, etc. Update this.'

Owner-provided meaning verbatim (same message):
    'Meaning: RMS is Royal Media Services (Kenya) - each station broadcasts
     in a specific local language, so STATION IDENTITY is authoritative
     language metadata for its audio.'

Owner-directed 4-sub-task execution plan verbatim (banked at
STATE/DECISIONS.md 2026-02-23T03:12:00Z entry):
    1. RESEARCH the full RMS station-language map with cited sources (web
       search, titles/links banked in the receipt - the owner asked for
       'all research with title'). Known anchors the owner gave:
       Inooro = Kikuyu, Ramogi = Luo (Dholuo).
    2. CROSS-REFERENCE the map against estate identifiers: the NAS 16
       off-air channels, OBS buckets (inoorotv, citizentv, citizen-vod,
       hot96backup, chamgei-backup, news-vault, rmsbroadcast,
       razuna.royalmedia, instore-radio-items, edailynew, skizaaudio, the
       na7p4* series when unblocked), and any station fields in the MySQL
       dbs. Bank a station-language-sources(assets) mapping table.
    3. FOLD INTO the census language axis: per-asset expected_language
       from station attribution becomes a first-class field alongside
       model-detected language.
    4. HONESTY RULE (non-negotiable · owner-verbatim):
       whisper-class models do NOT reliably distinguish
       Kikuyu/Luo/Kalenjin/Kamba etc. - where the model cant corroborate,
       the attribution is 'station-prior (cited), model-corroboration:
       unavailable' - never present model output as confirming a language
       it cant detect. Where model says Swahili/English it corroborates
       those stations only.

Research receipt with full per-station citation title + URL banked at
`phase0/rms_station_language_axis_research/receipt_20260223T032000Z.md`
carrying 8 root sources + 16 station-level citation records per owner's
*all research with title* directive.

Sealed carriers UNCHANGED per SO §3.8:
- `services.census_autonomy.tenant_admission_correction` (P4-c-v ·
  CENSUS_ADMISSION_SOURCE_MAP unchanged; this module attributes station
  identity WITHIN the RMS tenant already admitted at P4-c-v).
"""
from __future__ import annotations

from typing import Dict, Final, Tuple


# -----------------------------------------------------------------------------
# OWNER DIRECTIVE + HONESTY RULE (verbatim · non-negotiable)
# -----------------------------------------------------------------------------

# Banked verbatim from the owner message received 2026-02-23 mid-P4-d-i-seal.
OWNER_DIRECTIVE_VERBATIM: Final[str] = (
    "Audio - there are local language sample per station - each station "
    "represents local language - all research with title - eg inoro is "
    "kikuyu, ramogi is luo, etc. Update this."
)

# Owner-provided meaning banked verbatim (same message).
OWNER_MEANING_VERBATIM: Final[str] = (
    "Meaning: RMS is Royal Media Services (Kenya) - each station "
    "broadcasts in a specific local language, so STATION IDENTITY is "
    "authoritative language metadata for its audio."
)

# Owner HONESTY RULE (non-negotiable) banked verbatim.
MODEL_CORROBORATION_POLICY: Final[str] = (
    "OWNER HONESTY RULE (non-negotiable) verbatim: whisper-class models "
    "do NOT reliably distinguish Kikuyu/Luo/Kalenjin/Kamba etc. - where "
    "the model cant corroborate, the attribution is 'station-prior "
    "(cited), model-corroboration: unavailable' - never present model "
    "output as confirming a language it cant detect. Where model says "
    "Swahili/English it corroborates those stations only."
)


# -----------------------------------------------------------------------------
# WHISPER-CORROBORATABLE LANGUAGE SET (frozen · exactly {Swahili, English})
# -----------------------------------------------------------------------------

# Per owner HONESTY RULE closing clause: 'Where model says Swahili/English
# it corroborates those stations only.' The frozenset is the disk-verifiable
# closure of that clause.
WHISPER_CORROBORATABLE_LANGUAGES: Final[frozenset[str]] = frozenset({
    "Swahili",
    "English",
})


# -----------------------------------------------------------------------------
# RMS STATION -> LANGUAGE MAP (16 stations · 13 radio + 3 TV · cited)
# -----------------------------------------------------------------------------

# Each record carries the source-title + URL per owner's *all research with
# title* directive. Full 8-source root anchor + per-station citation table
# banked at phase0/rms_station_language_axis_research/receipt_20260223T032000Z.md.
_StationRecord = Dict[str, object]  # frozen-by-immutable-tuple-of-dicts pattern

RMS_STATION_LANGUAGE_MAP: Final[Tuple[_StationRecord, ...]] = (
    # --- Radio (13 stations per royalmedia.co.ke/radio/) ---
    {
        "station_name": "Radio Citizen",
        "modality": "radio",
        "primary_language": "Swahili",
        "secondary_languages": (),
        "slogan": "Chemchemi ya Ukweli",
        "whisper_can_corroborate": True,
        "research_citation_title": "Radio Citizen - radio.co.ke listen",
        "research_citation_url": "https://radio.co.ke/listen/radio-citizen/",
        "cross_reference_url": "https://royalmedia.co.ke/our-programming/",
    },
    {
        "station_name": "Hot 96",
        "modality": "radio",
        "primary_language": "English",
        "secondary_languages": ("Swahili",),  # Kenyanese urban blend
        "whisper_can_corroborate": True,
        "research_citation_title": "Hot 96 - Royal Media Services brand",
        "research_citation_url": "https://royalmedia.co.ke/brands/hot96/",
        "cross_reference_url": "https://royalmedia.co.ke/our-programming/",
    },
    {
        "station_name": "Inooro FM",
        "modality": "radio",
        "primary_language": "Kikuyu",
        "secondary_languages": (),
        "whisper_can_corroborate": False,
        "research_citation_title": "Inooro FM - Royal Media Services brand",
        "research_citation_url": "https://royalmedia.co.ke/brands/inooro-fm/",
        "cross_reference_url": "https://royalmedia.co.ke/our-programming/",
    },
    {
        "station_name": "Ramogi FM",
        "modality": "radio",
        "primary_language": "Dholuo",
        "secondary_languages": (),
        "whisper_can_corroborate": False,
        "research_citation_title": "Ramogi FM - Royal Media Services brand",
        "research_citation_url": "https://royalmedia.co.ke/brands/ramogi-fm/",
        "cross_reference_url": "https://royalmedia.co.ke/our-programming/",
    },
    {
        "station_name": "Chamgei FM",
        "modality": "radio",
        "primary_language": "Kalenjin",
        "secondary_languages": (),
        "whisper_can_corroborate": False,
        "research_citation_title": "Royal Media Services - Our Programming",
        "research_citation_url": "https://royalmedia.co.ke/our-programming/",
        "cross_reference_url": "https://allbusiness.africa/business/royal-media-services",
    },
    {
        "station_name": "Musyi FM",
        "modality": "radio",
        "primary_language": "Kamba",
        "secondary_languages": (),
        "whisper_can_corroborate": False,
        "research_citation_title": "Musyi FM - Royal Media Services brand",
        "research_citation_url": "https://royalmedia.co.ke/brands/musyi-fm/",
        "cross_reference_url": "https://royalmedia.co.ke/our-programming/",
    },
    {
        "station_name": "Muuga FM",
        "modality": "radio",
        "primary_language": "Kimeru",
        "secondary_languages": (),
        "whisper_can_corroborate": False,
        "research_citation_title": "Royal Media Services - Our Programming",
        "research_citation_url": "https://royalmedia.co.ke/our-programming/",
        "cross_reference_url": "https://allbusiness.africa/business/royal-media-services",
    },
    {
        "station_name": "Mulembe FM",
        "modality": "radio",
        "primary_language": "Luhya",
        "secondary_languages": (),
        "whisper_can_corroborate": False,
        "research_citation_title": "Royal Media Services - Our Programming",
        "research_citation_url": "https://royalmedia.co.ke/our-programming/",
        "cross_reference_url": "https://allbusiness.africa/business/royal-media-services",
    },
    {
        "station_name": "Egesa FM",
        "modality": "radio",
        "primary_language": "Ekegusii",
        "secondary_languages": (),
        "whisper_can_corroborate": False,
        "research_citation_title": "Egesa FM - Royal Media Services brand",
        "research_citation_url": "https://royalmedia.co.ke/brands/egesa-fm/",
        "cross_reference_url": "https://royalmedia.co.ke/our-programming/",
    },
    {
        "station_name": "Bahari FM",
        "modality": "radio",
        "primary_language": "Swahili",  # Kiswahili cha Kijomba - coastal Swahili
        "secondary_languages": ("Taita", "Giriama", "Digo"),  # Mijikenda variants
        "whisper_can_corroborate": True,  # coastal Swahili is Swahili variant
        "research_citation_title": "Bahari FM - Royal Media Services brand",
        "research_citation_url": "https://royalmedia.co.ke/brands/bahari-fm/",
        "cross_reference_url": "https://radio.co.ke/listen/bahari-fm/",
    },
    {
        "station_name": "Sulwe FM",
        "modality": "radio",
        "primary_language": "Bukusu",  # Luhya-Bukusu
        "secondary_languages": ("Wanga", "Kabras", "Tachoni", "Banyala", "Batura", "Bakhayo", "Bagisu"),
        "whisper_can_corroborate": False,
        "research_citation_title": "Sulwe FM - Royal Media Services brand",
        "research_citation_url": "https://royalmedia.co.ke/brands/sulwe-fm/",
        "cross_reference_url": "https://royalmedia.co.ke/radio/",
    },
    {
        "station_name": "Wimwaro FM",
        "modality": "radio",
        "primary_language": "Kiembu",  # Embu
        "secondary_languages": (),
        "whisper_can_corroborate": False,
        "research_citation_title": "Wimwaro FM - Royal Media Services brand",
        "research_citation_url": "https://royalmedia.co.ke/brands/wimwaro-fm/",
        "cross_reference_url": "https://royalmedia.co.ke/radio/",
    },
    {
        "station_name": "Vuuka FM",
        "modality": "radio",
        "primary_language": "Maragoli",  # Luhya-Maragoli
        "secondary_languages": (),
        "whisper_can_corroborate": False,
        "research_citation_title": "Vuuka FM - Royal Media Services brand",
        "research_citation_url": "https://royalmedia.co.ke/brands/vuuka-fm/",
        "cross_reference_url": "https://royalmedia.co.ke/radio/",
    },

    # --- TV (3 stations per royalmedia.co.ke/our-programming/) ---
    {
        "station_name": "Citizen TV",
        "modality": "tv",
        "primary_language": "English",  # National English + Swahili flagship
        "secondary_languages": ("Swahili",),
        "whisper_can_corroborate": True,
        "research_citation_title": "Citizen TV - Royal Media Services brand",
        "research_citation_url": "https://royalmedia.co.ke/brands/citizen-tv/",
        "cross_reference_url": "https://royalmedia.co.ke/our-programming/",
    },
    {
        "station_name": "Inooro TV",
        "modality": "tv",
        "primary_language": "Kikuyu",
        "secondary_languages": (),
        "whisper_can_corroborate": False,
        "research_citation_title": "Inooro TV - Royal Media Services brand",
        "research_citation_url": "https://royalmedia.co.ke/brands/inooro-tv/",
        "cross_reference_url": "https://royalmedia.co.ke/our-programming/",
    },
    {
        "station_name": "Ramogi TV",
        "modality": "tv",
        "primary_language": "Dholuo",
        "secondary_languages": (),
        "whisper_can_corroborate": False,
        "research_citation_title": "Royal Media Services - Our Programming",
        "research_citation_url": "https://royalmedia.co.ke/our-programming/",
        "cross_reference_url": "https://royalmedia.co.ke/radio/",
    },
)


# -----------------------------------------------------------------------------
# OBS BUCKET -> STATION CROSS-REFERENCE (owner CROSS-REFERENCE directive)
# -----------------------------------------------------------------------------

# Owner directive verbatim (2. CROSS-REFERENCE) names 11 buckets. The na7p4*
# series is honest-gap (*when unblocked*). Each mapping is a station-name
# attribution or a mixed-multi-station attribution when the bucket is an
# RMS-wide archive.
OBS_BUCKET_TO_STATION: Final[Dict[str, str]] = {
    "inoorotv":              "Inooro TV",
    "citizentv":             "Citizen TV",
    "citizen-vod":           "Citizen TV",  # video-on-demand archive
    "hot96backup":           "Hot 96",
    "chamgei-backup":        "Chamgei FM",
    "news-vault":            "Citizen TV",  # RMS newsroom archive - Citizen TV primary
    "rmsbroadcast":          "MIXED_ALL_16",  # RMS-wide broadcast archive - per-asset lookup required
    "razuna.royalmedia":     "MIXED_ALL_16",  # Razuna DAM all-station - per-asset lookup required
    "instore-radio-items":   "Radio Citizen",  # commercial store items
    "edailynew":             "Citizen TV",  # E-daily newsroom archive
    "skizaaudio":            "Radio Citizen",  # Skiza SMS-tunes platform hosting Radio Citizen
}


# Owner honest-gap: na7p4* series is *when unblocked* per owner directive.
# The mapping requires content-inspection when the block clears.
NA7P4_SERIES_HONEST_GAP: Final[str] = (
    "na7p4* series buckets are honest-gap - owner directive verbatim "
    "'when unblocked' - station attribution requires content-inspection "
    "when the block clears. Deferred to sub-slice at next scheduler pass."
)


# -----------------------------------------------------------------------------
# PRODUCT-LANGUAGE CALLABLES (SO §4)
# -----------------------------------------------------------------------------

def _lookup_station(station_name: str) -> _StationRecord | None:
    """Look up a station record by name · returns None if unknown."""
    for record in RMS_STATION_LANGUAGE_MAP:
        if record["station_name"] == station_name:
            return record
    return None


def station_to_language(station_name: str) -> str | None:
    """Return the primary language for a station · None if station unknown.

    Product-language callable per SO §4. Returned language is the
    station-attributed prior; corroboration policy separate via
    `attribution_for_asset`.
    """
    record = _lookup_station(station_name)
    if record is None:
        return None
    return record["primary_language"]  # type: ignore[return-value]


def is_language_whisper_corroboratable(language: str) -> bool:
    """Return True iff whisper-class model output for `language` is a
    reliable corroboration signal per owner HONESTY RULE.

    Only Swahili + English return True. All vernacular Kenyan languages
    (Kikuyu, Dholuo/Luo, Kalenjin, Kamba, Kimeru, Luhya, Ekegusii/Kisii,
    Bukusu, Kiembu, Maragoli, Mijikenda variants) return False.
    """
    return language in WHISPER_CORROBORATABLE_LANGUAGES


def attribution_for_asset(
    station_name: str,
    model_detected_language: str,
) -> Dict[str, object]:
    """Apply owner HONESTY RULE to produce an attribution record for an
    asset with a known station-prior + a whisper-class model-output.

    Returned schema:
      { 'station_prior': <str>,           # station-attributed primary language
        'model_corroboration': <str>,     # model output ONLY IF whisper can
                                          # detect the station-prior AND
                                          # model output matches; else
                                          # 'unavailable'
        'corroborated': <bool>,           # True iff both station-prior
                                          # AND model-output are in
                                          # WHISPER_CORROBORATABLE_LANGUAGES
                                          # AND match. Else False.
      }

    Owner HONESTY RULE (non-negotiable): model output is NEVER recorded as
    corroboration for a language whisper cant reliably detect.
    """
    record = _lookup_station(station_name)
    if record is None:
        return {
            "station_prior": "unknown_station",
            "model_corroboration": "unavailable",
            "corroborated": False,
        }
    station_lang: str = record["primary_language"]  # type: ignore[assignment]

    # Case 1: station is whisper-corroboratable (Swahili/English) AND
    # model output matches AND model output is itself whisper-corroboratable.
    if (
        station_lang in WHISPER_CORROBORATABLE_LANGUAGES
        and model_detected_language in WHISPER_CORROBORATABLE_LANGUAGES
        and model_detected_language == station_lang
    ):
        return {
            "station_prior": station_lang,
            "model_corroboration": model_detected_language,
            "corroborated": True,
        }

    # Case 2: station is vernacular (Kikuyu/Luo/Kalenjin/etc.) — HONESTY RULE
    # forbids recording model output as corroboration. Model output is
    # noise; attribution rests on cited station-prior only.
    #
    # Case 3: station is whisper-corroboratable but model claims a
    # whisper-unreliable language — model output is not credible on that
    # claim; attribution rests on cited station-prior only.
    return {
        "station_prior": station_lang,
        "model_corroboration": "unavailable",
        "corroborated": False,
    }
