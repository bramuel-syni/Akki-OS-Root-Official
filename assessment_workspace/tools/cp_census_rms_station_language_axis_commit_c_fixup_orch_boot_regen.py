#!/usr/bin/env python3
"""CP-CENSUS-RMS-STATION-LANGUAGE-AXIS Commit-C fixup ORCH_BOOT regen.

Advances heads_last_sealed:
  state_repo.head 17ac82569a1e09e821bdc7f80a6344e986c35267 (P4-d-i Commit-B)
                -> a798827518604a37b90a221d9c5e40e3ba0fbc41 (this Commit-B)
  code_repo.head b68cc02fc3e40e86e38e706bdfbf8ed0cbf6aa73 (P4-d-i Commit-A)
                -> 832bdf25b681d717fdb0fb25b6710078392c8909 (this Commit-A)

Ratchet fields UNCHANGED (already at 6232 from pre-Commit-A regen).

Syncs /app/frontend/public/audit/ORCH_BOOT.md byte-identically.

BL #1 respected: any YAML scalar text uses dashes (`Proceed - X`), never
embedded colons.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ORCH_BOOT = Path("/app/assessment_workspace/notes/ORCH_BOOT.md")
AUDIT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

OLD_TIME = "2026-02-23T03:35:00Z"
NEW_TIME = "2026-02-23T03:55:00Z"

OLD_STATE_HEAD = "17ac82569a1e09e821bdc7f80a6344e986c35267"
NEW_STATE_HEAD = "a798827518604a37b90a221d9c5e40e3ba0fbc41"
OLD_CODE_HEAD = "b68cc02fc3e40e86e38e706bdfbf8ed0cbf6aa73"
NEW_CODE_HEAD = "832bdf25b681d717fdb0fb25b6710078392c8909"

OLD_STATE_SEALED_AT = "2026-02-23T03:00:00Z"
NEW_STATE_SEALED_AT = "2026-02-23T03:50:00Z"
OLD_CODE_SEALED_AT = "2026-02-23T02:50:00Z"
NEW_CODE_SEALED_AT = "2026-02-23T03:45:00Z"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    body = ORCH_BOOT.read_text(encoding="utf-8")

    # generated_at_utc
    old_at = f"generated_at_utc: {OLD_TIME}"
    new_at = f"generated_at_utc: {NEW_TIME}"
    assert body.count(old_at) == 1, f"anchor not unique: {old_at!r}"
    body = body.replace(old_at, new_at)

    # generator line — replace the prior pre-Commit-A generator paren-scalar
    # with the Commit-C fixup rewrite. BL #1 respected — no embedded colons.
    old_gen_prefix = (
        "generator: main-agent Autopilot (CP-CENSUS-RMS-STATION-LANGUAGE-AXIS "
        "pre-Commit-A"
    )
    start = body.find(old_gen_prefix)
    assert start != -1, "generator prefix not found"
    end_paren = body.find(")\n", start)
    assert end_paren != -1
    end = end_paren + 1
    new_generator = (
        "generator: main-agent Autopilot (CP-CENSUS-RMS-STATION-LANGUAGE-AXIS "
        "Commit-C fixup - state master - R-6 boundary regen advancing heads_"
        f"last_sealed.state_repo.head {OLD_STATE_HEAD} (P4-d-i Commit-B) -> "
        f"this-CP-CENSUS-RMS-STATION-LANGUAGE-AXIS Commit-B {NEW_STATE_HEAD} "
        f"[banks code Commit-A {NEW_CODE_HEAD} on programme/track-a + /app "
        f"main companion Commit-A 7b21450a74f35bd1bdc981e4619d7b7b8d14c736 - "
        "owner-queued Task 3 fold-in verbatim (2026-02-23 mid-P4-d-i-seal) "
        "Audio - there are local language sample per station - each station "
        "represents local language - all research with title - eg inoro is "
        "kikuyu ramogi is luo etc. Update this. RMS = Royal Media Services "
        "(Kenya) - station identity is authoritative language metadata for "
        "audio - NEW additive backend/services/rms_station_language_axis.py "
        "(~391 lines) with 16-station cited map (13 radio + 3 TV owner-"
        "anchored bindings Inooro/Ramogi FM+TV + Citizen TV verified "
        "verbatim) + owner HONESTY RULE verbatim + WHISPER_CORROBORATABLE_"
        "LANGUAGES frozenset Swahili + English + attribution_for_asset "
        "callable applying HONESTY RULE + OBS_BUCKET_TO_STATION over 11 "
        "owner-named buckets + na7p4* series honest-gap Final + NEW test_cp_"
        "census_rms_station_language_axis_phase_4_census_scheduler.py (8 "
        "RED-first structural pins) + baseline_failures.json ratchet 6224-"
        "to-6232 +8 canonical measured - Sealed carriers UNCHANGED per SO "
        "§3.8 - RED-first authentic ModuleNotFoundError right-reason - "
        "GREEN-post 8/8 pass 0.71s - Pre-Commit-A double-green byte-"
        "identical stripped_sha256 fb2624a016a2c95081fd86857d058ff58863b03c"
        "7e466b820ddf629b70940fe8 IDENTICAL sweep_A/B both 6238 passed 1 "
        "skipped 0 failed 520 warnings - baseline_failures.json sha256 "
        "73485dbfe9d85d83b47c581fd1bf7c95d90e7bffc382d90111d1351e1223f977 "
        "post-bump - research receipt banked at phase0/rms_station_"
        "language_axis_research/receipt_20260223T032000Z.md with 8 root "
        "sources + 16 station-level citation records per owner all "
        "research with title directive - owner credential-hold LIFT same-"
        "turn banked verbatim at STATE/DECISIONS.md top - HF-HOLD SEC-2026-"
        "09-12-01 LIFTED-BY-OWNER-ORDER DQ-06 RESOLVED-BY-OWNER-ORDER DQ-13 "
        "+ DQ-17 DEFERRED-POST-BUILD - AIP Spec v1.0 owner drop queued in "
        "DECISIONS.md for CP-AIP-SPEC-INGEST work block opening AFTER -2 "
        "collection-drift forensic + Order B + Order A audits] - advances "
        f"heads_last_sealed.code_repo.head {OLD_CODE_HEAD} (P4-d-i Commit-"
        f"A) -> this-wave Commit-A {NEW_CODE_HEAD} - Sealed carriers "
        "UNCHANGED per SO §3.8 - Standing bounds unchanged)"
    )
    body = body[:start] + new_generator + body[end:]

    # regeneration_reason
    body = body.replace(
        "regeneration_reason: r6-boundary-regen-pre-commit-a-at-cp-census-rms-station-language-axis-ratchet-only-6224-to-6232-plus-8-canonical-measured-owner-queued-task-3-fold-in-rms-station-language-metadata",
        f"regeneration_reason: r6-boundary-regen-post-commit-c-fixup-at-cp-census-rms-station-language-axis-advancing-state-head-17ac8256-to-a7988275-plus-code-head-b68cc02fc-to-832bdf25-plus-ratchet-6224-to-6232-plus-8-canonical-measured-owner-queued-task-3-rms-station-language-axis-fold-in",
    )

    # heads_last_sealed — state_repo block
    old_state_block = (
        f"  state_repo:\n"
        f"    workdir: /app/assessment_workspace\n"
        f"    branch: master\n"
        f"    head: {OLD_STATE_HEAD}\n"
        f"    sealed_at_utc: {OLD_STATE_SEALED_AT}\n"
        f'    seal_kind: "PHASE 4 (d-i) - CP-DECK-ENGINE-DR-R4-OPENING - state Commit-B'
    )
    new_state_prefix = (
        f"  state_repo:\n"
        f"    workdir: /app/assessment_workspace\n"
        f"    branch: master\n"
        f"    head: {NEW_STATE_HEAD}\n"
        f"    sealed_at_utc: {NEW_STATE_SEALED_AT}\n"
        f'    seal_kind: "CP-CENSUS-RMS-STATION-LANGUAGE-AXIS - state Commit-B'
    )
    assert old_state_block in body, "state_repo block anchor not found"
    body = body.replace(old_state_block, new_state_prefix)
    # Now find and rewrite the seal_kind scalar for state_repo up through
    # closing quote. Anchor on the prior full P4-d-i seal_kind - replace it
    # with the new CP-CENSUS-RMS-STATION-LANGUAGE-AXIS one.
    old_state_seal_kind_full = (
        '    seal_kind: "CP-CENSUS-RMS-STATION-LANGUAGE-AXIS - state Commit-B - '
        "banks code Commit-A b68cc02 + /app companion fb40d6f5 - Slice 1 of "
        "CP-DECK-ENGINE 14-DR-R chunked series OPENING - NEW backend/contracts/"
        "deck_spec_v0.py (SO 3.10-alpha closed-schema Pydantic BaseModel "
        "frozen=True + extra=forbid - Slice-1 minimum-viable fields deck_id + "
        "spec_version Literal v0 - DR_R4_SOURCE_RESTORE_HONEST_GAP Final "
        "naming deck_engine.md + RD-16 verbatim) + NEW deck_spec_v0.contract_"
        "snapshot.json + NEW test file (6 RED-first pins) + additive CONTRACT_"
        "TO_SNAPSHOT map entry - 6 RED-first pins - Sealed carriers UNCHANGED "
        "- CP-SKILLS-LAYER chunked series unchanged - server.py mirror pair "
        "unchanged (P4-d-i additive-only zero router surface Slice 1 contract "
        "shape only) - ratchet 6218-to-6224 +6 canonical - double-green byte-"
        "identical stripped_sha256 5998ae6832544cb698c861cf20c0b5699e6db8bfc4"
        "2c6c6b61cfe4b9b2d360fa IDENTICAL both 6230 passed - CP-DECK-ENGINE "
        "Slice 2 opens NEXT after seal (full field enumeration post deck_"
        "engine.md verbatim restore) - owner-queued CENSUS-3-C RMS text-column "
        "language-detection (CPU/SQL-only raised to next census-scheduler "
        "slot) + Razuna/Newsvault RMS-tenant binding-verify + OBS audio sweep "
        'inclusion (next census-pass gate) folded to scheduler queue mid-seal '
        'without interrupt"'
    )
    new_state_seal_kind_full = (
        f'    seal_kind: "CP-CENSUS-RMS-STATION-LANGUAGE-AXIS - state Commit-B - '
        f"banks code Commit-A {NEW_CODE_HEAD[:7]} + /app companion 7b21450a7 - "
        "owner-queued Task 3 fold-in verbatim - RMS = Royal Media Services "
        "(Kenya) - station identity is authoritative language metadata for "
        "audio - NEW backend/services/rms_station_language_axis.py 391 lines "
        "carrying OWNER_DIRECTIVE_VERBATIM + OWNER_HONESTY_RULE_VERBATIM + "
        "RMS_STATION_LANGUAGE_AXIS 16-station tuple (13 radio + 3 TV owner-"
        "anchored Inooro/Ramogi FM+TV + Citizen TV verbatim) + WHISPER_"
        "CORROBORATABLE_LANGUAGES frozenset Swahili + English + attribution_"
        "for_asset callable applying HONESTY RULE + OBS_BUCKET_TO_STATION 11 "
        "owner-named buckets + NA7P4_SERIES_HONEST_GAP Final + NEW test_cp_"
        "census_rms_station_language_axis_phase_4_census_scheduler.py 8 RED-"
        "first structural pins - Sealed carriers UNCHANGED - contracts.deck_"
        "spec_v0 P4-d-i unchanged - services.census_autonomy.tenant_"
        "admission_correction P4-c-v unchanged (this slice attributes station "
        "identity WITHIN RMS tenant already admitted at P4-c-v) - server.py "
        "mirror pair unchanged (metadata module only zero router surface) - "
        "ratchet 6224-to-6232 +8 canonical - double-green byte-identical "
        "stripped_sha256 fb2624a016a2c95081fd86857d058ff58863b03c7e466b820ddf6"
        "29b70940fe8 IDENTICAL both 6238 passed - owner credential-hold LIFT "
        "banked verbatim at DECISIONS.md top same-turn - AIP Spec v1.0 owner "
        "drop queued for CP-AIP-SPEC-INGEST post-audits - Task 1 CENSUS-3-C + "
        "Task 2 Razuna/Newsvault binding-verify remain scheduler-queued at "
        'next census-pass"'
    )
    assert old_state_seal_kind_full in body, "state seal_kind not matched"
    body = body.replace(old_state_seal_kind_full, new_state_seal_kind_full)

    # heads_last_sealed — code_repo block
    old_code_block = (
        f"  code_repo:\n"
        f"    workdir: /app/assessment_workspace/repos/Extraction-Akki\n"
        f"    branch: programme/track-a\n"
        f"    head: {OLD_CODE_HEAD}\n"
        f"    sealed_at_utc: {OLD_CODE_SEALED_AT}\n"
    )
    new_code_block = (
        f"  code_repo:\n"
        f"    workdir: /app/assessment_workspace/repos/Extraction-Akki\n"
        f"    branch: programme/track-a\n"
        f"    head: {NEW_CODE_HEAD}\n"
        f"    sealed_at_utc: {NEW_CODE_SEALED_AT}\n"
    )
    assert old_code_block in body, "code_repo block anchor not found"
    body = body.replace(old_code_block, new_code_block)

    # code_repo seal_kind — rewrite the prior P4-d-i one
    old_code_seal_kind_prefix = (
        '    seal_kind: "PHASE 4 (d-i) - CP-DECK-ENGINE-DR-R4-OPENING - Commit-A b68cc02'
    )
    start = body.find(old_code_seal_kind_prefix)
    assert start != -1, "code_repo seal_kind prefix not found"
    end_quote = body.find('"\n\n', start)
    assert end_quote != -1
    end = end_quote + 1
    new_code_seal_kind = (
        f'    seal_kind: "CP-CENSUS-RMS-STATION-LANGUAGE-AXIS - Commit-A '
        f"{NEW_CODE_HEAD[:7]} code programme/track-a - owner-queued Task 3 "
        "fold-in verbatim (2026-02-23 mid-P4-d-i-seal) - RMS = Royal Media "
        "Services (Kenya) - NEW backend/services/rms_station_language_axis.py "
        "(~391 lines - OWNER_DIRECTIVE_VERBATIM concat-guard proof BL #3 + "
        "OWNER_HONESTY_RULE_VERBATIM whisper-cannot-distinguish-vernaculars + "
        "RMS_STATION_LANGUAGE_AXIS Final tuple 16 station records 13 radio + "
        "3 TV each with station_name + language + whisper_can_corroborate + "
        "research_citation_title + research_citation_url + cross_reference_"
        "url + owner-anchored bindings Inooro FM = Kikuyu + Ramogi FM = Luo/"
        "Dholuo + Inooro TV = Kikuyu + Ramogi TV = Luo + Citizen TV = "
        "Kiswahili verified verbatim + WHISPER_CORROBORATABLE_LANGUAGES Final "
        "frozenset only Swahili + English + OBS_BUCKET_TO_STATION 11 owner-"
        "named buckets inoorotv + citizentv + citizen-vod + hot96backup + "
        "chamgei-backup + news-vault + rmsbroadcast + razuna.royalmedia + "
        "instore-radio-items + edailynew + skizaaudio + NA7P4_SERIES_HONEST_"
        "GAP Final str + attribution_for_asset callable applies HONESTY RULE "
        "vernacular-station-returns-unavailable + Swahili-station-model-"
        "Swahili-corroborated + English-station-model-English-corroborated + "
        "English-station-model-Kikuyu-unavailable) + NEW backend/tests/"
        "invariants/test_cp_census_rms_station_language_axis_phase_4_census_"
        "scheduler.py (8 RED-first structural pins - module presence + "
        "OWNER_DIRECTIVE_VERBATIM concat-guard + 16-station map length + "
        "owner-anchored bindings verbatim + every station carries citation "
        "title+url + MODEL_CORROBORATION_POLICY Final HONESTY RULE + WHISPER_"
        "CORROBORATABLE_LANGUAGES exact frozenset + attribution_for_asset "
        "callable across 4 scenarios + OBS_BUCKET_TO_STATION 11-bucket "
        "coverage + NA7P4_SERIES_HONEST_GAP present) + baseline_failures.json "
        "ratchet 6224-to-6232 +8 canonical measured schema-complete ratchet_"
        "history entry per BL #6 - BL #7 indent=2 - BL #11 ensure_ascii=False "
        "- Sealed carriers UNCHANGED per SO §3.8 - services.census_autonomy."
        "tenant_admission_correction P4-c-v CENSUS_ADMISSION_SOURCE_MAP "
        "unchanged - contracts.deck_spec_v0 P4-d-i unchanged - RED-first "
        "authentic ModuleNotFoundError right-reason - GREEN-post 8/8 pass "
        "0.71s - Pre-Commit-A double-green byte-identical stripped_sha256 "
        "fb2624a016a2c95081fd86857d058ff58863b03c7e466b820ddf629b70940fe8 "
        "IDENTICAL sweep_A/B both 6238 passed 1 skipped 0 failed 520 warnings "
        "~191s each - research receipt banked at phase0/rms_station_language_"
        "axis_research/receipt_20260223T032000Z.md - owner credential-hold "
        "LIFT this-turn same-session (HF-HOLD SEC-2026-09-12-01 LIFTED-BY-"
        "OWNER-ORDER + DQ-06 RESOLVED + DQ-13 + DQ-17 DEFERRED-POST-BUILD) "
        "banked verbatim at DECISIONS.md - AIP Spec v1.0 owner drop queued "
        'for CP-AIP-SPEC-INGEST work block opening after audits"'
    )
    body = body[:start] + new_code_seal_kind + body[end:]

    ORCH_BOOT.write_text(body, encoding="utf-8")
    AUDIT.write_text(body, encoding="utf-8")
    assert _sha256(ORCH_BOOT) == _sha256(AUDIT), "byte-identity check failed"

    print(f"OK: ORCH_BOOT Commit-C fixup advanced heads")
    print(f"    state_repo.head: {OLD_STATE_HEAD} -> {NEW_STATE_HEAD}")
    print(f"    code_repo.head:  {OLD_CODE_HEAD} -> {NEW_CODE_HEAD}")
    print(f"    notes sha256: {_sha256(ORCH_BOOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
