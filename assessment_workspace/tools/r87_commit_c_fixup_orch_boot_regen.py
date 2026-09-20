"""R-87 Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Precedent shape (mirrors tools/r86_commit_c_fixup_orch_boot_regen.py):
- state_repo (lines 47-52 of ORCH_BOOT.md): replaced with R-87 Commit-B
  `b4526572…` entry.
- code_repo history: fresh entry for R-87 Commit-A `200c2c63…` INSERTED at
  the top of the history (immediately after state_repo), preserving all
  prior code_repo entries in chronological order.
- generated_at_utc + regeneration_reason: updated to R-87 Commit-C fixup.
- POD audit mirror: /app/frontend/public/audit/ORCH_BOOT.md byte-identically
  synced via shutil.copyfile (no remote calls).

Additive: heads_last_sealed history is append-only for code_repo entries;
state_repo is a single current-head slot that advances at each Commit-C.

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R87_STATE_HEAD).

Standing bounds: zero push · zero remote · zero network. This script performs
local filesystem operations only (Path.read_text, Path.write_text,
shutil.copyfile).
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R87_STATE_HEAD = "b452657228e7038cb3c59834c7921dae332b391b"
R87_CODE_HEAD = "200c2c637277f1f12dee342dc68cdf7a7ebed463"
R87_STATE_SEALED_AT = "2026-09-20T20:47:00Z"
R87_CODE_SEALED_AT = "2026-09-20T20:43:00Z"
NEW_UTC = "2026-09-20T20:50:00Z"
NEW_REGEN_REASON = (
    "r87-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-b4526572-"
    "cp-blocked-vocabulary-correction-commit-b-plus-new-code-repo-history-"
    "entry-for-r87-commit-a-200c2c63"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R87_STATE_HEAD}
    sealed_at_utc: {R87_STATE_SEALED_AT}
    seal_kind: "CP-BLOCKED-VOCABULARY-CORRECTION · state Commit-B `{R87_STATE_HEAD}` · banks Commit-A `{R87_CODE_HEAD}` on programme/track-a · WAVE R-87 · Ruling 2 mirror-half landed · FE-FIX-READY FLAGGED · 2026-09-20T~20:47Z · owner Ruling 2 verbatim (2026-09-20T~19:00Z · 'suspension is a state of the principal (DAP-27, PRIN-1), not a fourth reason a request is blocked — a different axis, different object. Sealed enum stays at three. party_halted lives as its own state via the Q5 module tree and its vocab constant, and it NEVER renders in the Blocked reason grammar — no estate copy, no kind label. Correct the wording at source everywhere non-sealed: it is three Blocked kinds plus Interrupted plus party_halted — NOT five Blocked kinds. Vocabulary is load-bearing for the substitution rules now — register the corrected count/grammar so the wrong phrasing is RED where feasible') + R-87-open reinforcement 2026-09-20T~20:30Z verbatim ((a) corrected vocabulary + (b) register in substitution-rule set + (c) sealed erratum non-sealed source-fix + (d) FE-FIX-READY spec with EXACT badge/legend/drawer grammar) · DELTA +6 measured (5645 → 5651 monotonic-up per CCS2 lesson both fields bumped together · new baseline_failures.json sha256 c0af7a314841e78af4507149539e3f59892ace811bf15a5afce527878b65bbb7 was ccb45068bf19a1f95f20b6e15bcd7c7993571c714a0d5e316e93a8175f8972ea) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND (1 new backend module services/dap_lifecycle/blocked_vocabulary.py + 1 new test module tests/invariants/test_blocked_vocabulary_correction.py + 1 additive ratchet bump + 1 FE-FIX-READY spec notes/FE_FIX_READY_R87_blocked_vocabulary_correction.md + 1 non-sealed fork-note fix in place + 3 erratum entries citing sealed R-85 files in DECISIONS.md + 1 pre-Commit-A ORCH_BOOT ratchet-only regen + 1 new regen tool + 1 STATE/PINS.md housekeeping-pickup) · zero implementation module edit · zero sealed contract/writer/test file edit · zero baseline shrink · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 e1a887e05d52e4cc0c28759e0ce3efe289846963eaedea8405e8d0f8b18d1e73 IDENTICAL across drill_receipts/20260920T203618Z_run1 (181.67s · 5651 passed) + 20260920T204257Z_run2 (181.99s · 5651 passed) both 3 baseline-fails 1 skip 438 warnings against post-bump baseline_failures.json sha256 c0af7a31 · Files (7 tracked): notes/FE_FIX_READY_R87_blocked_vocabulary_correction.md NEW (sha256 44f2824fcf2109fca5d0716cf5df349f5131504addb7812e605acba9658afb42) + notes/dap_extraction_journey_v2_open_forks_20260920.md (Ruling 2(c) in-place correction) + notes/ORCH_BOOT.md (ratchet-only regen sha256 a6e07e58…) + tools/r87_pre_commit_a_orch_boot_regen.py NEW + STATE/PINS.md refresh + STATE/DECISIONS.md this-append + STATE/NEXT.md this-append · POD audit mirror /app/frontend/public/audit/FE_FIX_READY_R87_blocked_vocabulary_correction.md byte-identically synced at this-Commit-B (sha256 44f2824f identical) · POD audit mirror /app/frontend/public/audit/ORCH_BOOT.md byte-identically synced pre-Commit-A (sha256 a6e07e58 identical) · Canon anchors verbatim: owner Ruling 2 this-session (2026-09-20T~19:00Z · DECISIONS.md line 20421 OWNER RULINGS anchor + reaffirmed at 1250c39a + R-86 Commit-C e40047f4) + owner R-87-open reinforcement (2026-09-20T~20:30Z verbatim this-chat) + sealed BlockedKind enum at services/dap_lifecycle/blocked_kinds.py (3 members request/check/estate) + journey v1 §11 L201 'Blocked has three kinds, not one flat state: request, check, estate' + DAP-27 principal-state + PRIN-1 principal-context binding + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + CP-APP-JS-UNIFY-SCHEDULE-AND-DRIFT-ANNOTATE seal 2eca0e58/1525ddd0/e40047f4 (R-86 immediately-precedes) + CP-PARTY-HALTED-ADDITIVE-SUB-WAVE seal 11afc4f/0cd4c9b8 (R-85 · this-wave erratum targets) + CP-REGISTRY-V5-RATIFICATION-AND-COUNT-ERRATUM 1250c39a · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-C fixup this-turn (this-file R-6 regen advances state_repo.head to {R87_STATE_HEAD} + inserts code_repo entry for R87 Commit-A {R87_CODE_HEAD} + R-87 marker flips ⏳ IN-FLIGHT → ✅ SEALED at Commit-C in STATE/NEXT.md) → R-88+ CP-CONTENT-REGISTRY-WAVE opens (Ruling 4 · CON-1..31 · 7-category grep-negative bans + R-32 surface-list binding on Generated-class)"
"""

NEW_R87_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R87_CODE_HEAD}
    sealed_at_utc: {R87_CODE_SEALED_AT}
    seal_kind: "CP-BLOCKED-VOCABULARY-CORRECTION · Commit-A `{R87_CODE_HEAD}` · code programme/track-a · WAVE R-87 · Ruling 2 execution · 2026-09-20T~20:43Z · owner Ruling 2 verbatim (2026-09-20T~19:00Z · 'suspension is a state of the principal (DAP-27, PRIN-1), not a fourth reason a request is blocked — a different axis, different object. Sealed enum stays at three. party_halted lives as its own state via the Q5 module tree and its vocab constant, and it NEVER renders in the Blocked reason grammar — no estate copy, no kind label. Correct the wording at source everywhere non-sealed: it is three Blocked kinds plus Interrupted plus party_halted — NOT five Blocked kinds. Vocabulary is load-bearing for the substitution rules now — register the corrected count/grammar so the wrong phrasing is RED where feasible') · 1 NEW backend module services/dap_lifecycle/blocked_vocabulary.py registering Final[int] BLOCKED_KINDS_COUNT=3 + Final[tuple[str, ...]] BLOCKED_KINDS_TUPLE=('request', 'check', 'estate') byte-verbatim match sealed BlockedKind enum + Final[bool] SUSPENDED_IS_PRINCIPAL_STATE_NOT_BLOCKED_KIND=True (DAP-27/PRIN-1 axis-binding) + Final[bool] PARTY_HALTED_IS_OWN_RAIL_STATE_NOT_BLOCKED_KIND=True (Q5 module tree axis-binding) + Final[str] CORRECTED_COMPOSITION_PHRASE='three Blocked kinds plus Interrupted plus party_halted' + Final[tuple[str, ...]] WRONG_COUNT_PHRASES canonical 4-variant list ('five Blocked kinds' + '5 Blocked kinds' + 'Blocked has five kinds' + 'five kinds of Blocked') + pure-data-in grep_negative_wrong_count_phrases(text) scanner returning (line_no matched_phrase) hit list · 1 NEW test module tests/invariants/test_blocked_vocabulary_correction.py with 6 property tests (Final[int] count-binding + BLOCKED_KINDS_TUPLE byte-match sealed enum + Final[bool] axis-bindings + WRONG_COUNT_PHRASES 4-variant grep-negative substrate + module docstring Ruling-2 verbatim 4-quote presence check) · DELTA +6 measured (5645 → 5651 monotonic-up per CCS2 lesson both fields bumped · new baseline_failures.json sha256 c0af7a314841e78af4507149539e3f59892ace811bf15a5afce527878b65bbb7 was ccb45068bf19a1f95f20b6e15bcd7c7993571c714a0d5e316e93a8175f8972ea) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND (1 new backend module + 1 new test module + additive ratchet bump · FE-FIX-READY spec + fork-note fix + erratum land at Commit-B) · zero implementation module edit outside this-wave · zero sealed contract/writer/test file edit · sealed BlockedKind enum NOT edited (consumed via identity import + tuple-match assertion) · sealed party_halted_kind.py + party_halt_billing.py + test_dap_lifecycle_party_halted_sub_wave.py NOT edited (their SO §2.5 verbatim-docstring quotes of journey v2 'five kinds' phrasing inherit Ruling-2 erratum citation banked at Commit-B) · sealed suspension_notices.py NOT edited (Q5-sealed principal-state surface stays authoritative) · AUTHENTIC RED-first cycle: RED at drill_receipts/20260920T203041Z_cp_r87_blocked_vocabulary_correction_RED_pre.log (6/6 fail right-reason ImportError blocked_vocabulary module absent) → GREEN at 20260920T203133Z_GREEN_post + 20260920T203211Z_GREEN_post2 (6/6 pass 0.71s post-module + post-docstring-fix) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 e1a887e05d52e4cc0c28759e0ce3efe289846963eaedea8405e8d0f8b18d1e73 IDENTICAL across drill_receipts/20260920T203618Z_run1 (181.67s · 5651 passed) + 20260920T204257Z_run2 (181.99s · 5651 passed) both 3 baseline-fails (specialist-dispatch mirror-drift · pre-CP-APP-JS-UNIFY R-91) 1 skip 438 warnings · pre-Commit-A ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order + byte-identical POD audit-mirror sync (tools/r87_pre_commit_a_orch_boot_regen.py + notes/ORCH_BOOT.md + /app/frontend/public/audit/ORCH_BOOT.md both sha256 a6e07e5842263757a4a453628b7096e2ecb962e5f5caae905d998db4959aa610) · Canon anchors verbatim: owner Ruling 2 this-session (2026-09-20T~19:00Z · STATE/DECISIONS.md line 20421 OWNER RULINGS anchor + re-affirmed at 1250c39a + R-86 Commit-C e40047f4) + sealed BlockedKind enum at services/dap_lifecycle/blocked_kinds.py (3 members request/check/estate) + journey v1 §11 L201 'Blocked has three kinds, not one flat state: request, check, estate' + DAP-27 principal-state + PRIN-1 principal-context binding + CP-APP-JS-UNIFY-SCHEDULE-AND-DRIFT-ANNOTATE seal 2eca0e58/1525ddd0/e40047f4 (R-86 immediately-precedes) + CP-PARTY-HALTED-ADDITIVE-SUB-WAVE seal 11afc4f/0cd4c9b8 (R-85) + CP-REGISTRY-V5-RATIFICATION-AND-COUNT-ERRATUM 1250c39a + SO §2.5 verbatim-docstring + §3 tests-first + §3.3 3-Commit Seal + §3.8 additive-only + §3.10-α Final[str] closed-vocab + §6.2 objective-card + §6.4 NOTHING-BEYOND + §6.7 seal-report-boundary + M16-W3 corrected order + CCS2 lesson · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · FE-FIX-READY spec authored at Commit-B (notes/FE_FIX_READY_R87_blocked_vocabulary_correction.md sha256 44f2824fcf2109fca5d0716cf5df349f5131504addb7812e605acba9658afb42 · byte-precise before/after for 3 FE surfaces StatusBadge.jsx + lifecycleStrings.js + RequestLifecycle.jsx · 10 acceptance criteria) · specialist merge-back acceptance criteria (10 checks · grep-negative on Blocked·suspended + Blocked·party_halted + 5-kind phrasing + BLOCK_KIND_SUSPENDED/BLOCK_WHATNEXT_SUSPENDED exports · STATUS_META 12-key exact set + lifecycleStrings.js export delta = -4 · RequestLifecycle.jsx zero suspended blockKind occurrences · party_halted own drawer + Blocked drawer three-kind scoping · behaviour of request/check/estate rails unchanged pre/post) · autopilot next Commit-B state master → Commit-C fixup → R-88+ CP-CONTENT-REGISTRY-WAVE opens (Ruling 4 · CON-1..31 · 7-category grep-negative bans + R-32 surface-list binding on Generated-class)"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")

    # Idempotency guard: if state_repo.head already equals R87_STATE_HEAD, skip.
    if f"head: {R87_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-87 Commit-B.")
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
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R87_CODE_REPO_BLOCK + text[m.end():]

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
    print(f"heads_last_sealed.state_repo.head → {R87_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R87_CODE_HEAD}")
    print(f"regenerated: {NOTES_ORCH_BOOT}")
    print(f"mirrored:    {AUDIT_ORCH_BOOT}")


if __name__ == "__main__":
    main()
