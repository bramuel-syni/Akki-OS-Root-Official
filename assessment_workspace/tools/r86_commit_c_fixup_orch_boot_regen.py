"""R-86 Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Precedent shape:
- state_repo (lines 47-52): replaced with R-86 Commit-B `1525ddd0…` entry.
- code_repo history: fresh entry for R-86 Commit-A `2eca0e58…` INSERTED at
  the top of the history (immediately after state_repo), preserving all
  prior code_repo entries in chronological order.
- generated_at_utc + regeneration_reason: updated to Commit-C fixup.
- POD audit mirror: byte-identically synced.

Additive: heads_last_sealed history is append-only for code_repo entries;
state_repo is a single current-head slot that advances at each Commit-C.

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R86_STATE_HEAD).
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R86_STATE_HEAD = "1525ddd0f0a00d85c9c4e114e2f77362175158d6"
R86_CODE_HEAD = "2eca0e58d1d9773d1b781abe570c3e015e0c98f2"
R86_STATE_SEALED_AT = "2026-09-20T20:12:00Z"
R86_CODE_SEALED_AT = "2026-09-20T20:07:00Z"
NEW_UTC = "2026-09-20T20:18:00Z"
NEW_REGEN_REASON = (
    "r86-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-1525ddd0-"
    "cp-app-js-unify-schedule-and-drift-annotate-commit-b-plus-new-code-repo-history-"
    "entry-for-r86-commit-a-2eca0e58"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R86_STATE_HEAD}
    sealed_at_utc: {R86_STATE_SEALED_AT}
    seal_kind: "CP-APP-JS-UNIFY-SCHEDULE-AND-DRIFT-ANNOTATE · state Commit-B `{R86_STATE_HEAD}` · banks Commit-A `{R86_CODE_HEAD}` on programme/track-a · WAVE R-86 · Ruling 1 mirror-half closure sealed · CP-APP-JS-UNIFY confirmed at slot R-91 · 2026-09-20T~20:12Z · owner Ruling 1 verbatim (2026-09-20T~19:00Z · 'Coexistence with a closure date is discipline; without one it's drift with a ruling attached') + follow-up R-91 slot ratification 2026-09-20T~19:54Z (banked at 1250c39a) · DELTA +5 measured (5640 → 5645 monotonic-up per CCS2 lesson both fields bumped together · new baseline_failures.json sha256 ccb45068bf19a1f95f20b6e15bcd7c7993571c714a0d5e316e93a8175f8972ea was 284a18c3cbd3bb74dd8a436342301f760d47b6e5a2df4c0ba8681e21825b7438) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND (1 new test module tests/invariants/test_baseline_drift_annotations_present.py + 1 additive top-level baseline_failures.json field known_runtime_drift_annotations mapping 3 pod_shell mirror-drift entries · 1 additive ratchet bump + ratchet_history append · 1 new scheduled-slot card STATE/OBJECTIVES/CP_APP_JS_UNIFY.md 6-section+YAML-frontmatter+hash-pin card_sha256 800d836d08e0cff31a3a06458142331cb19dd8698ebbf26855923c2a891b1d3c · 1 pre-Commit-A ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order via tools/r86_pre_commit_a_orch_boot_regen_and_card_pin.py · 1 new tool · 1 STATE/PINS.md commissioning_record pointer refresh R-29-BOOT housekeeping-pickup) · zero implementation module edit · zero sealed contract/writer/test file edit · zero baseline shrink · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 b709ed74305ca67da6743fa737363c48f8990a40b9619ea7efc9a0e8f9d12931 IDENTICAL across drill_receipts/20260920T200944Z_run1 (180.20s · 5645 passed) + 20260920T201305Z_run2 (183.22s · 5645 passed) both 3 baseline-fails 1 skip 438 warnings against post-bump baseline_failures.json sha256 ccb45068 · Files (6 tracked): STATE/OBJECTIVES/CP_APP_JS_UNIFY.md NEW + notes/ORCH_BOOT.md updated + tools/r86_pre_commit_a_orch_boot_regen_and_card_pin.py NEW + STATE/PINS.md refresh + STATE/DECISIONS.md this-append + STATE/NEXT.md this-append · FE COORDINATION seal FULLY CLOSED at this-wave (byte-verify half at d0a2ea9b + mirror-drift half at this-commit) · Canon anchors verbatim: owner Ruling 1 this-session (2026-09-20T~19:00Z · DECISIONS.md line 20421 OWNER RULINGS anchor + reaffirmed at 1250c39a) + R-91 slot ratification 2026-09-20T~19:54Z + Wave G Step 1 pod_shell mirror discipline + specialist commit chain 3fbfb75c/f090e8305/d0e36a51e + CP-ENT-43-BYTE-VERIFY-CLOSURE d0a2ea9b + CP-LIFECYCLE-STRINGS-BYTE-VERIFY 9b6b170b + CP-LIFECYCLE-STRINGS-BYTE-VERIFY-CLOSURE 14173772 + SO §2.5/§3/§3.3/§3.8/§6.2/§6.4/§6.7 + M16-W3 corrected order + CCS2 lesson + CP-PARTY-HALTED-ADDITIVE-SUB-WAVE seal 11afc4f/0cd4c9b8 (R-85 immediately-precedes) + CP-REGISTRY-V5-RATIFICATION-AND-COUNT-ERRATUM banking at 1250c39a (v5 RATIFIED + count-fix erratum cites 0e7a07b0 + G5-v5 unblocked + sequencing confirmed with R-91 slot · this-wave anchor) · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-C fixup this-turn (this-file R-6 regen advances state_repo.head to {R86_STATE_HEAD} + inserts code_repo entry for R86 Commit-A {R86_CODE_HEAD} + R-86 marker flips ✅ SEALED at Commit-C in STATE/NEXT.md) → R-87 CP-BLOCKED-VOCABULARY-CORRECTION opens"
"""

NEW_R86_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R86_CODE_HEAD}
    sealed_at_utc: {R86_CODE_SEALED_AT}
    seal_kind: "CP-APP-JS-UNIFY-SCHEDULE-AND-DRIFT-ANNOTATE · Commit-A `{R86_CODE_HEAD}` · code programme/track-a · WAVE R-86 · Ruling 1 mirror-half closure + CP-APP-JS-UNIFY scheduled at slot R-91 · 2026-09-20T~20:07Z · owner verbatim ('Coexistence with a closure date is discipline; without one it's drift with a ruling attached') · 5 NEW property invariants at tests/invariants/test_baseline_drift_annotations_present.py enforcing (1) coverage every pod_shell mirror-drift baseline entry has annotation + (2) 8-field shape (drift_kind reason owner_ruling_ref owner_ruling_verbatim_short closure_wave closure_wave_slot closure_card_path closure_card_line) + (3) closure_card_path resolves under STATE repo root + (4) annotation count == mirror-drift baseline set + (5) closure_wave == CP-APP-JS-UNIFY verbatim · NEW top-level known_runtime_drift_annotations field in baseline_failures.json mapping the 3 pod_shell mirror-drift baseline entries (test_ship_manifest_dod::test_runtime_frontend_app_matches_repo_pod_shell + test_wave_g_pod_shell_frontend_mirror::test_app_frontend_App_js_mirrors_pod_shell_App_js + test_wave_g_pod_shell_frontend_mirror::test_app_frontend_pages_dir_mirrors_pod_shell_pages_dir) to closure_wave=CP-APP-JS-UNIFY closure_wave_slot=R-91 closure_card_path=STATE/OBJECTIVES/CP_APP_JS_UNIFY.md closure_card_line='unify /app/frontend/** ↔ pod_shell/frontend/** byte-identity' · DELTA +5 measured (5640 → 5645 monotonic-up per CCS2 lesson · new baseline sha ccb45068bf19a1f95f20b6e15bcd7c7993571c714a0d5e316e93a8175f8972ea was 284a18c3cbd3bb74dd8a436342301f760d47b6e5a2df4c0ba8681e21825b7438) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · Files added (1 NEW additive-only per SO §3.8): backend/tests/invariants/test_baseline_drift_annotations_present.py (~230 lines · 5 property tests with SO §2.5 verbatim-docstring discipline) · Files edited (additive-only): backend/tests/invariants/baseline_failures.json (passed_floor + counts_at_baseline.passed 5640 → 5645 + known_runtime_drift_annotations NEW top-level field + ratchet_history append per M16-W3 corrected order) · AUTHENTIC RED-first cycle: RED at drill_receipts/20260920T200147Z (5/5 fail right-reason · annotations dict absent + closure card absent from STATE/OBJECTIVES/) → GREEN at 20260920T200233Z (5/5 pass 0.69s post-annotations + post-card) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 b709ed74305ca67da6743fa737363c48f8990a40b9619ea7efc9a0e8f9d12931 IDENTICAL across drill_receipts/20260920T200944Z_run1 (180.20s) + 20260920T201305Z_run2 (183.22s) both 5645 pass · 3 baseline-fails · 1 skip · 438 warnings · specialist-drift .jsx redacted per prior reconciliation pattern · sealed contracts NOT edited · sealed writers NOT edited · sealed test files NOT edited · Canon anchors verbatim: owner Ruling 1 this-session 2026-09-20T~19:00Z + R-91 slot ratification 2026-09-20T~19:54Z (banked at 1250c39a) + Wave G Step 1 pod_shell mirror discipline (test_ship_manifest_dod + test_wave_g_pod_shell_frontend_mirror) + specialist commit chain 3fbfb75c/f090e8305/d0e36a51e + CP-ENT-43-BYTE-VERIFY-CLOSURE d0a2ea9b + CP-LIFECYCLE-STRINGS-BYTE-VERIFY 9b6b170b + CP-LIFECYCLE-STRINGS-BYTE-VERIFY-CLOSURE 14173772 + SO §2.5/§3/§3.3/§3.8/§6.2/§6.4/§6.7 + M16-W3 corrected order + CCS2 lesson + CP-PARTY-HALTED-ADDITIVE-SUB-WAVE seal 11afc4f/0cd4c9b8 (R-85 immediately-precedes) + CP-REGISTRY-V5-RATIFICATION-AND-COUNT-ERRATUM banking at 1250c39a (v5 RATIFIED + count-fix erratum cites 0e7a07b0 + G5-v5 unblocked + sequencing confirmed with R-91 slot · this-wave anchor) · CONTRACT-SURFACE-READY FLAG unchanged · FE COORDINATION seal FULLY CLOSED at this-wave · autopilot next Commit-B state master → Commit-C fixup → R-87 CP-BLOCKED-VOCABULARY-CORRECTION"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")

    # Idempotency guard: if state_repo.head already equals R86_STATE_HEAD, skip.
    if f"head: {R86_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-86 Commit-B.")
    else:
        # Replace state_repo section + insert new code_repo entry at top of history.
        # Pattern: match from 'heads_last_sealed:' through end of first state_repo entry
        # (up to but NOT including the first '  code_repo:' line).
        state_repo_regex = re.compile(
            r"heads_last_sealed:\n"
            r"  state_repo:\n"
            r"    workdir: /app/assessment_workspace\n"
            r"    branch: master\n"
            r"    head: [0-9a-f]{40}\n"
            r"    sealed_at_utc: [^\n]+\n"
            r'    seal_kind: "[^\n]+"\n',
            re.DOTALL,
        )
        m = state_repo_regex.search(text)
        if not m:
            raise SystemExit("Could not locate heads_last_sealed.state_repo block")
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R86_CODE_REPO_BLOCK + text[m.end():]

    # Update generated_at_utc + regeneration_reason
    text = re.sub(
        r"^generated_at_utc:.*$",
        f"generated_at_utc: {NEW_UTC}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^regeneration_reason:.*$",
        f"regeneration_reason: {NEW_REGEN_REASON}",
        text,
        count=1,
        flags=re.MULTILINE,
    )

    NOTES_ORCH_BOOT.write_text(text, encoding="utf-8")
    shutil.copyfile(NOTES_ORCH_BOOT, AUDIT_ORCH_BOOT)


def main() -> None:
    regen_orch_boot_commit_c()
    print(f"heads_last_sealed.state_repo.head → {R86_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R86_CODE_HEAD}")
    print(f"regenerated: {NOTES_ORCH_BOOT}")
    print(f"mirrored:    {AUDIT_ORCH_BOOT}")


if __name__ == "__main__":
    main()
