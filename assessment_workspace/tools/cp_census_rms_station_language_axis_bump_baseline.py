"""CP-CENSUS-RMS-STATION-LANGUAGE-AXIS · ratchet floor bump.

Bumps baseline_failures.json passed_floor 6224 -> 6232 (+8 canonical
measured) reflecting the 8 RED-first structural pins landed by
test_cp_census_rms_station_language_axis_phase_4_census_scheduler.py.

BL #11 respected: json.dumps writes with ensure_ascii=False.
BL #7 respected: indent=2 preserved.
BL #6 respected: ratchet_history entry `passed` field equals the NEW
post-seal floor (6232).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


BASELINE_PATH = (
    Path(__file__).resolve().parents[1]
    / "repos"
    / "Extraction-Akki"
    / "backend"
    / "tests"
    / "invariants"
    / "baseline_failures.json"
)


def main() -> None:
    d = json.loads(BASELINE_PATH.read_text())

    old_floor = d["invariants_enforced_when_baseline_guard_1"]["passed_floor"]
    new_floor = 6232
    assert old_floor == 6224, (
        f"expected old_floor 6224 · got {old_floor}"
    )

    d["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = new_floor
    d["counts_at_baseline"]["passed"] = new_floor
    d["recorded_at_utc"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )

    history_entry = {
        "at_utc": d["recorded_at_utc"],
        "from_floor": old_floor,
        "to_floor": new_floor,
        "delta": new_floor - old_floor,
        "passed": new_floor,
        "cp": (
            "CP-CENSUS-RMS-STATION-LANGUAGE-AXIS · PHASE 4 CENSUS-SCHEDULER "
            "· owner-queued Task 3 fold-in verbatim (RMS = Royal Media "
            "Services Kenya · station identity is authoritative language "
            "metadata for audio) · additive census-model service module "
            "services/rms_station_language_axis.py landed with 16-station "
            "cited map + owner HONESTY RULE verbatim + WHISPER_"
            "CORROBORATABLE_LANGUAGES == frozenset({Swahili, English}) "
            "+ attribution_for_asset product callable applying HONESTY "
            "RULE + OBS_BUCKET_TO_STATION cross-reference · 8 RED-first "
            "structural pins at tests/invariants/test_cp_census_rms_"
            "station_language_axis_phase_4_census_scheduler.py"
        ),
        "note": (
            "8 RED-first pins landed additively per SO §3.8 · module "
            "presence + owner directive verbatim marker (BL #3 concat "
            "guard) · full 16-station map (13 radio + 3 TV) with per-"
            "station research_citation_title + research_citation_url · "
            "owner-anchored bindings (Inooro/Ramogi FM+TV) verified "
            "verbatim · MODEL_CORROBORATION_POLICY Final constant "
            "carrying owner HONESTY RULE verbatim · WHISPER_CORROBORATABLE_"
            "LANGUAGES frozenset({Swahili, English}) · attribution_for_"
            "asset callable applies HONESTY RULE (vernacular station "
            "returns model_corroboration='unavailable' regardless of "
            "model output · Swahili/English station corroborated only "
            "when model output matches AND is whisper-corroboratable) · "
            "OBS_BUCKET_TO_STATION covers 11 owner-named buckets · "
            "na7p4* series honest-gap. Research receipt banked at "
            "phase0/rms_station_language_axis_research/"
            "receipt_20260223T032000Z.md with 8 root sources + 16 "
            "station-level citation records per owner's 'all research "
            "with title' directive. Sealed carriers UNCHANGED per "
            "SO §3.8: services.census_autonomy.tenant_admission_"
            "correction (P4-c-v CENSUS_ADMISSION_SOURCE_MAP unchanged - "
            "this slice attributes station identity WITHIN the RMS "
            "tenant already admitted at P4-c-v). RED-pre 8 "
            "ModuleNotFoundError right-reason · GREEN-post 8/8 pass "
            "0.71s."
        ),
    }
    d.setdefault("ratchet_history", []).append(history_entry)

    BASELINE_PATH.write_text(
        json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    )
    print(f"baseline_failures.json bumped {old_floor} -> {new_floor}")


if __name__ == "__main__":
    main()
