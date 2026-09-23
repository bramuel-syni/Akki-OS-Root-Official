#!/usr/bin/env python3
"""CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY pre-Commit-A ratchet + ORCH_BOOT regen.

Bumps baseline_failures.json passed_floor 6340 -> 6350 (+10 canonical measured)
and refreshes ORCH_BOOT.md top ```yaml``` fenced block to match (both copies
byte-identical). Heads_last_sealed values stay UNCHANGED at the CP-ENT-16 seal
values until this-CP's own Commit-A + Commit-B land at the seal chain.

Additive per SO §3.8. BL #11 respected (ensure_ascii=False). BL #7 (indent=2).
BL #6 (ratchet_history entry passed = new floor).
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


BASELINE = Path(
    "/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/"
    "baseline_failures.json"
)
ORCH_BOOT_NOTES = Path("/app/assessment_workspace/notes/ORCH_BOOT.md")
ORCH_BOOT_AUDIT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

OLD_FLOOR = 6340
NEW_FLOOR = 6350
SEAL_ID = "CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY-20260223"
LEDGER_ITEM = "STATE/OBJECTIVES/CP_CENSUS_THREE_WAVES_20260223.md"

# Heads stay UNCHANGED at CP-ENT-16 seal.
STATE_HEAD_OLD = "6256dbf7774c6885a6044502492c34ce33a75049"
CODE_HEAD_OLD = "9e3ca45a9c6382732f52970966df800311eada17"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    d = json.loads(BASELINE.read_text())
    old_floor = d["invariants_enforced_when_baseline_guard_1"]["passed_floor"]
    assert old_floor == OLD_FLOOR, f"expected old_floor {OLD_FLOOR}; got {old_floor}"

    d["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = NEW_FLOOR
    d["counts_at_baseline"]["passed"] = NEW_FLOOR
    d["recorded_at_utc"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    d["ratchet_history"].append({
        "timestamp_utc": "2026-02-23T13:55:00Z",
        "seal_id": SEAL_ID,
        "ledger_item": LEDGER_ITEM,
        "passed_pre": OLD_FLOOR,
        "passed": NEW_FLOOR,
        "delta": NEW_FLOOR - OLD_FLOOR,
        "note": (
            "CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY · Item 5.11.c of "
            "EXECUTION_ORDER.md · SO §6.9 amendment §6 item 8 verbatim: "
            "'The census proceeds in its three waves — complete the walk "
            "with the unmeasured register, the full B3 dimension set with "
            "the defensibility matrix and sensitivity classification, then "
            "the perception pathway — and language labels from item 4 "
            "enter it as overlay from the first run.' 10 RED-first "
            "canonical measured invariant pins on 3-wave census orchestration "
            "boundary: CENSUS_THREE_WAVES ordered 3-tuple (unmeasured_register "
            "+ b3_dimension_set + perception_pathway) + UnmeasuredRegisterWave_v1 "
            "frozen dimensions_measured=False (B5.4 shown-not-counted line) + "
            "B3DimensionSetWave_v1 frozen carrying b3_attachment_markedness + "
            "b3_genre_form + b3_corroboration + defensibility_matrix_rule_ref "
            "(Canon 4 §5.1 qmatrix rule) + sensitivity_class (Canon 4 §5.1 + "
            "Canon 7 §3 conservative default) + PerceptionPathwayWave_v1 frozen "
            "lid_overlay_source_registration + lid_overlay_marker Literal "
            "INFERRED/unmeasured + CensusWaveOutOfOrderError structural sequencing "
            "(Wave 2 refuses without Wave 1 completed; Wave 3 refuses without "
            "Wave 2 completed) + CensusWaveNameRefused Literal-closed 3-tuple + "
            "lid_overlay_source_is_sealed_registration identity-check against "
            "sealed CP-SO-6.9-LID-WAVE WHISPER_LID_REGISTRATION + "
            "VOXLINGUA107_REGISTRATION (fabricated shape-equivalent objects "
            "refused) + register_census_three_waves_as_census_autonomy_job "
            "refuses pod://* + /app/* prefixed refs (Ruling (b) AKKI-RUNS-IT "
            "verbatim: pod is never data path) + "
            "LID_OVERLAY_ENTERS_FROM_FIRST_RUN_POSTURE Final marker citing "
            "SO §6.9 amendment §6 item 8 verbatim + "
            "POD_IS_NEVER_DATA_PATH_POSTURE_THREE_WAVES Final marker citing "
            "Ruling (b) verbatim + §1.2 no-redeclaration of sealed "
            "CP-SO-6.9-LID-WAVE symbols (LidModelRegistration_v1 + "
            "OverlayLidDetection_v1 + WHISPER_LID_REGISTRATION + "
            "VOXLINGUA107_REGISTRATION) + §1.2 no-redeclaration of sealed "
            "CP-M6-3-1 CharacterRegister/CharacterEntry. §1.2 modality-extension "
            "composing sealed CP-SO-6.9-LID-WAVE lid_wave_overlay_and_admission_v1. "
            "1 NEW additive module backend/services/audio_plane_v1/"
            "census_three_waves_v1.py (~230 lines). Sealed CP-SO-6.9-LID-WAVE "
            "carrier UNCHANGED per SO §3.8 additive-only."
        ),
    })

    BASELINE.write_text(
        json.dumps(d, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    new_baseline_sha = _sha256(BASELINE)
    print(f"NEW baseline_failures.json sha256: {new_baseline_sha}")

    # Regen ORCH_BOOT.md top ```yaml``` fenced block: bump passed_floor +
    # baseline_failures_sha256 + counts_at_baseline_passed. Heads UNCHANGED.
    body = ORCH_BOOT_NOTES.read_text(encoding="utf-8")

    def _regen_first_yaml_block(body_text: str) -> str:
        fence_re = re.compile(r"(```yaml\s*\n)(.*?)(\n```)", re.DOTALL)
        m = fence_re.search(body_text)
        assert m, "no fenced yaml block found"
        inner = m.group(2)
        # Bump passed_floor + counts_at_baseline_passed + baseline_failures_sha256.
        inner = re.sub(
            r"(\bpassed_floor:\s*)\d+",
            rf"\g<1>{NEW_FLOOR}",
            inner,
            count=1,
        )
        inner = re.sub(
            r"(\bcounts_at_baseline_passed:\s*)\d+",
            rf"\g<1>{NEW_FLOOR}",
            inner,
            count=1,
        )
        inner = re.sub(
            r"(\bbaseline_failures_sha256:\s*)[0-9a-f]{64}",
            rf"\g<1>{new_baseline_sha}",
            inner,
            count=1,
        )
        # Bump generated_at_utc.
        new_time = "2026-02-23T13:55:00Z"
        inner = re.sub(
            r"(\bgenerated_at_utc:\s*)\S+",
            rf"\g<1>{new_time}",
            inner,
            count=1,
        )
        # Bump generator + regeneration_reason to reflect this-CP.
        inner = re.sub(
            r'\bgenerator:\s*".*?"',
            (
                'generator: "main-agent Autopilot '
                "(CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY pre-Commit-A ratchet-only "
                "ORCH_BOOT regen · advancing ratchet.passed_floor 6340 -> 6350 + "
                "baseline_failures.json sha256 to post-bump value · "
                "heads_last_sealed UNCHANGED at last CP-ENT-16-PILOT-LICENCE-SEEDS "
                "state Commit-B 6256dbf7 + code Commit-A 9e3ca45a · this-CP heads "
                'advance at Commit-C fixup post-Commit-B)"'
            ),
            inner,
            count=1,
            flags=re.DOTALL,
        )
        inner = re.sub(
            r"\bregeneration_reason:\s*\S+",
            (
                "regeneration_reason: pre-commit-a-cp-census-three-waves-"
                "with-lid-overlay-ratchet-only-regen-6340-to-6350-plus-10-"
                "canonical-measured-so-6-9-amendment-6-item-8-three-wave-"
                "census-orchestration-boundary-plus-lid-overlay-from-first-run"
            ),
            inner,
            count=1,
        )
        return body_text[:m.start(2)] + inner + body_text[m.end(2):]

    body_new = _regen_first_yaml_block(body)
    ORCH_BOOT_NOTES.write_text(body_new, encoding="utf-8")
    ORCH_BOOT_AUDIT.write_text(body_new, encoding="utf-8")
    notes_sha = _sha256(ORCH_BOOT_NOTES)
    audit_sha = _sha256(ORCH_BOOT_AUDIT)
    assert notes_sha == audit_sha, "byte-identity check failed"
    print(f"ORCH_BOOT.md notes+audit byte-identical sha256: {notes_sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
