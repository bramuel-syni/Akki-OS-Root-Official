#!/usr/bin/env python3
"""CP-CENSUS-RMS-STATION-LANGUAGE-AXIS pre-Commit-A ORCH_BOOT regen (ratchet-only).

Advances ratchet passed_floor 6224 -> 6232 and refreshes baseline_failures_sha256.
Heads stay at PHASE 4 (d-i) CP-DECK-ENGINE-DR-R4-OPENING sealed values pending
§3.3 CP-CENSUS-RMS-STATION-LANGUAGE-AXIS seal completion.
Syncs /app/frontend/public/audit/ORCH_BOOT.md byte-identically.

Additive per SO §3.8 · pre-Commit-A ratchet-only R-6 regen trigger.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ORCH_BOOT = Path("/app/assessment_workspace/notes/ORCH_BOOT.md")
AUDIT = Path("/app/frontend/public/audit/ORCH_BOOT.md")
BASELINE = Path(
    "/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/"
    "baseline_failures.json"
)

OLD_TIME = "2026-02-23T03:05:00Z"
NEW_TIME = "2026-02-23T03:35:00Z"
OLD_RATCHET = 6224
NEW_RATCHET = 6232
OLD_BASELINE_SHA = "66ae28aa7a7fbc2db40de200c26ffe0b9163239f6e58641bae6060eaacf6d61c"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    live_baseline_sha = _sha256(BASELINE)
    print(f"Live baseline_failures.json sha256: {live_baseline_sha}")

    body = ORCH_BOOT.read_text(encoding="utf-8")

    # generated_at_utc
    old_at = f"generated_at_utc: {OLD_TIME}"
    new_at = f"generated_at_utc: {NEW_TIME}"
    assert body.count(old_at) == 1, f"anchor not unique: {old_at!r}"
    body = body.replace(old_at, new_at)

    # generator line (single-line paren-enclosed) — anchor on the exact prior
    # PHASE 4 (d-i) prefix; replace whole line up to end of first ')'.
    old_gen_prefix = (
        "generator: main-agent Autopilot (PHASE 4 (d-i) - CP-DECK-ENGINE-DR-R4-OPENING - Commit-C fixup"
    )
    start = body.find(old_gen_prefix)
    assert start != -1, "generator prefix not found"
    end_paren = body.find(")\n", start)
    assert end_paren != -1
    end = end_paren + 1
    # NOTE: this scalar is a single-line YAML value — MUST NOT contain
    # any unquoted "key: value" colon-space patterns (YAML would parse
    # them as nested mapping). Bare single quotes are also unsafe when
    # they appear where YAML expects a flow scalar. We deliberately
    # substitute colons with slashes/dashes and remove stray quote chars.
    new_generator = (
        "generator: main-agent Autopilot (CP-CENSUS-RMS-STATION-LANGUAGE-AXIS "
        "pre-Commit-A - state master - owner-queued Task 3 scheduler fold-in "
        "verbatim (2026-02-23 mid-P4-d-i-seal) Audio - there are local "
        "language sample per station - each station represents local language "
        "- all research with title - eg inoro is kikuyu ramogi is luo etc. "
        "Update this. RMS = Royal Media Services (Kenya) - station identity "
        "is authoritative language metadata for audio - additive census-model "
        "service module services/rms_station_language_axis.py landed with "
        "16-station cited map (13 radio + 3 TV owner-anchored bindings "
        "Inooro/Ramogi verified verbatim) + owner HONESTY RULE verbatim + "
        "WHISPER_CORROBORATABLE_LANGUAGES frozenset Swahili + English + "
        "attribution_for_asset callable applying HONESTY RULE + OBS_BUCKET_"
        "TO_STATION cross-reference over 11 owner-named buckets + na7p4* "
        "series honest-gap - ratchet 6224 -> 6232 +8 canonical measured - "
        f"new baseline_failures.json sha256 `{live_baseline_sha}` - heads_"
        "last_sealed.code_repo.head + state_repo.head both stay at prior "
        "PHASE 4 (d-i) CP-DECK-ENGINE-DR-R4-OPENING Commit-A b68cc02fc + "
        "Commit-B 17ac82569 pending §3.3 CP-CENSUS-RMS-STATION-LANGUAGE-"
        "AXIS Commit-A/B/C seal - research receipt banked at phase0/rms_"
        "station_language_axis_research/receipt_20260223T032000Z.md with 8 "
        "root sources + 16 station-level citation records per owner all "
        "research with title directive - Sealed carriers UNCHANGED per "
        "SO §3.8 - Standing bounds unchanged)"
    )
    body = body[:start] + new_generator + body[end:]

    # regeneration_reason
    body = body.replace(
        "regeneration_reason: phase-4-d-i-cp-deck-engine-dr-r4-opening-commit-c-fixup-r-6-boundary-regen-advancing-state-head-22738f20-to-17ac8256-plus-code-head-419244cdb-to-b68cc02fc-plus-ratchet-6218-to-6224-plus-6-canonical-measured-dr-r4-deckspec-v0-shape-freeze-opening-slice-owner-queued-census-3-c-plus-razuna-newsvault-binding-verify-folded-to-scheduler",
        "regeneration_reason: r6-boundary-regen-pre-commit-a-at-cp-census-rms-station-language-axis-ratchet-only-6224-to-6232-plus-8-canonical-measured-owner-queued-task-3-fold-in-rms-station-language-metadata",
    )

    # ratchet block
    old_ratchet_block = (
        f"ratchet:\n"
        f"  passed_floor: {OLD_RATCHET}\n"
        f"  counts_at_baseline_passed: {OLD_RATCHET}\n"
        f"  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json\n"
        f"  baseline_failures_sha256: {OLD_BASELINE_SHA}\n"
    )
    new_ratchet_block = (
        f"ratchet:\n"
        f"  passed_floor: {NEW_RATCHET}\n"
        f"  counts_at_baseline_passed: {NEW_RATCHET}\n"
        f"  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json\n"
        f"  baseline_failures_sha256: {live_baseline_sha}\n"
    )
    assert old_ratchet_block in body, "ratchet block anchor not found"
    # last-key-wins in YAML - replace ALL 17 occurrences so the yaml.safe_load
    # in the invariant test sees the NEW ratchet across every duplicated block.
    body = body.replace(old_ratchet_block, new_ratchet_block)

    ORCH_BOOT.write_text(body, encoding="utf-8")
    AUDIT.write_text(body, encoding="utf-8")
    assert _sha256(ORCH_BOOT) == _sha256(AUDIT), "byte-identity check failed"

    # Verify YAML parses first block.
    import re, yaml
    m = re.search(r"```yaml\n(.*?)\n```", body, re.DOTALL)
    parsed = yaml.safe_load(m.group(1))
    assert parsed["ratchet"]["passed_floor"] == NEW_RATCHET
    assert parsed["ratchet"]["baseline_failures_sha256"] == live_baseline_sha
    print(f"OK: ORCH_BOOT advanced to ratchet={NEW_RATCHET}, baseline_sha={live_baseline_sha}")
    print(f"    notes sha256: {_sha256(ORCH_BOOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
