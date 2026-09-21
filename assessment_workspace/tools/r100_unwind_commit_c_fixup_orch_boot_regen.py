"""R-100-UNWIND Commit-C fixup: ORCH_BOOT R-6 boundary regen.

Wave R-100-UNWIND · self-reported §3.8 lapse cured. Follows R-99/R-100
Commit-C fixup precedent exactly (tools/r99_commit_c_fixup_orch_boot_regen.py
+ tools/r100_commit_c_fixup_orch_boot_regen.py).

- state_repo (heads_last_sealed.state_repo): advanced from R-100 Commit-B
  `e6a86c2c3f613def64cc854710837f03c468d89e` to R-100-UNWIND Commit-B
  `bf272c7ebe1c19545c9900fae8d41ff4d948bb53` (R-100-A OPERATIONAL CURE at
  `00827f7a` was a banking-only commit and did NOT bump this pointer).
- code_repo history: fresh entry for R-100-UNWIND Commit-A
  `42a0d3a04f13486b8929a59f8fd98d7f5a36d226` INSERTED at the top of the
  history (immediately after state_repo), preserving all prior code_repo
  entries in chronological order (R-100 Commit-A `39412d09...` remains
  as the next-most-recent entry).
- generated_at_utc + regeneration_reason: updated to R-100-UNWIND Commit-C
  fixup.

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R100_UNWIND_STATE_HEAD).

Standing bounds: zero push · zero remote · zero network.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R100_UNWIND_STATE_HEAD = "bf272c7ebe1c19545c9900fae8d41ff4d948bb53"
R100_UNWIND_CODE_HEAD = "42a0d3a04f13486b8929a59f8fd98d7f5a36d226"
R100_UNWIND_STATE_SEALED_AT = "2026-09-21T11:40:00Z"
R100_UNWIND_CODE_SEALED_AT = "2026-09-21T11:39:00Z"
NEW_UTC = "2026-09-21T11:45:00Z"
NEW_REGEN_REASON = (
    "r100-unwind-commit-c-fixup-r6-boundary-regen-advancing-state-repo-"
    "head-to-bf272c7e-cp-r100-unwind-commit-b-plus-new-code-repo-history-"
    "entry-for-r100-unwind-commit-a-42a0d3a-self-reported-so-3-8-lapse-"
    "cured-wrapper-services-enforce-principal-context-adapter-owning-with-"
    "block-protocol-sealed-context-py-restored-byte-identical-commit-"
    "4b3b5e0-sha256-ad0d9439-portal-requests-plus-portal-entitlement-"
    "repointed-to-wrapper-plus-sealed-bytes-sha-pin-test-structural-3-8-"
    "guard-plus-continuity-bundle-regen-3-bundles-pinned-in-state-pins-md"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R100_UNWIND_STATE_HEAD}
    sealed_at_utc: {R100_UNWIND_STATE_SEALED_AT}
    seal_kind: "R-100-UNWIND CP-R100-UNWIND · state Commit-B `{R100_UNWIND_STATE_HEAD}` · banks Commit-A `{R100_UNWIND_CODE_HEAD}` on programme/track-a · WAVE R-100-UNWIND · self-reported §3.8 lapse cured · owner directive verbatim this-session (2026-09-21T~11:00Z at UNWIND directive): 'Modifying the sealed PrincipalRequestContext class in services/request_context/context.py to add __enter__/__exit__ is an edit to a sealed class — SO §3.8 forbids it. Unwind to a wrapper: revert context.py byte-identically to its sealed state, author a context-manager adapter inside services/enforce/ that owns the protocol, re-point the R-100 portal routers to the wrapper, seal as a self-reported §3.8 lapse cured, regenerate the three continuity bundles, pin their sha256s in STATE/PINS.md, then hold at the R-91 horizon (no expedite).' Cure summary: (a) sealed backend/services/request_context/context.py restored byte-identical to Commit 4b3b5e0 (sha256 ad0d94399af44bd5f6fa57f9aa1371ede7ca526789e47db10b45dddc79c39cfb · verified via git show + diff IDENTICAL); (b) NEW backend/services/enforce/principal_context_adapter.py wrapper single public callable principal_context via @contextlib.contextmanager · enter sets _CURRENT_PRINCIPAL_ID.set-and-Token · exit resets Token in try/finally so both normal and exceptional exits clear propagation without leaking (semantic upgrade over the illegal cure which was no-op-on-exit) · yields the sealed PrincipalRequestContext carrier unchanged · PRIN-11 propagation-by-construction + PRIN-13 read-only-once-in-propagation both preserved verbatim on sealed carrier; (c) R-100 portal routers (portal_requests.py 5 handlers + portal_entitlement.py 4 handlers) re-pointed from services.request_context.enter_propagation to services.enforce.principal_context_adapter.principal_context (9 substitutions total · atomic sed); (d) NEW tests/invariants/test_principal_context_adapter.py with 5 tests (module-importable + enters-and-yields + exit-clears + exception-propagates-and-clears + sealed-bytes-sha256-pinned as SO §3.8 structural guard making any future in-place edit to context.py structurally detectable via sha-pin ad0d9439). Ratchet 5852 → 5857 (+5 MEASURED = targeted · no CCS2 correction) · new baseline_failures.json sha256 ee8569b871bb08537c4201b375c177d51b196f6d0583a9ac762b55d0e8c58671. AUTHENTIC RED-first cycle: drill_receipts/20260921T112718Z RED 5/5 right-reason + 20260921T112831Z GREEN 39/39 in 0.90s + BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep byte-identical stripped-sha256 27240fc197ca711f3712e61f086183683f71200e13320d3005d5445f39e463a4 IDENTICAL run1 (185.67s 5857 passed) + run2 (181.96s 5857 passed) + live curl matrix all 14 endpoints (5 R-99 canon-rules public 200 + 9 R-100 portal 200/202/404 with seeded JWT + 4 R-100 portal 401 without JWT · zero 500 · wrapper effective · sealed carrier untouched). Files banked at Commit-B: STATE/DECISIONS.md append (R-100-UNWIND section framed as self-reported §3.8 lapse cured + standing lesson banked) + notes/ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order (passed_floor 5852 → 5857) + phase0/spec_hunt_receipts/20260921T113000Z_r100_unwind_seal_report.md NEW consolidated seal report + tools/r100_unwind_pre_commit_a_ratchet_and_orch_boot_regen.py archived. Standing lesson banked verbatim: §3.8 does not admit expedient in-place edits; sealed classes needing new protocol surface land as adapters/wrappers in the appropriate services layer; pattern extends to any sealed file autopilot repeatedly reaches for (sha-pin test the first time §3.8 discipline is threatened). Sealed R-100 39412d09/e6a86c2c/0ae3713f + R-99 eb40fb67/58685080/2579f74f + R-98..R-88 seal chain all continue verbatim GREEN · sealed carriers PrincipalRequestContext + enter_propagation + current_principal_id + downstream_write + PrincipalContextAbsent + PrincipalContextRefusal all UNCHANGED · sealed ledger_actor_binding UNCHANGED. R-91 stays PARKED · horizon 2026-09-23T03:23:15Z UNCHANGED · current UTC 2026-09-21T~11:45Z < horizon (~39.6h out) · R-100-UNWIND seal completes cleanly inside window with zero ceremony-apply operations opened. Autopilot next Commit-C fixup this-turn advances state_head + inserts code_repo entry for R-100-UNWIND Commit-A 42a0d3a + executes Continuity Bundle regen (3 bundles) + STATE/PINS.md sha256 pins block → HOLD for R-91 horizon (NO EXPEDITE) → R-91 ε-APPLY at horizon → M1-to-date BUILD_JOURNAL closure state-only."
"""

NEW_R100_UNWIND_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R100_UNWIND_CODE_HEAD}
    sealed_at_utc: {R100_UNWIND_CODE_SEALED_AT}
    seal_kind: "R-100-UNWIND CP-R100-UNWIND · Commit-A `{R100_UNWIND_CODE_HEAD}` · code programme/track-a · WAVE R-100-UNWIND · self-reported §3.8 lapse cured on top of 320a752 (R-100-A OPERATIONAL CURE lapse commit stays in history · additive-only means this-Commit-A reverts the specific illegal file change and adds the wrapper · does NOT rewrite history). Owner directive verbatim this-session (2026-09-21T~11:00Z at UNWIND directive): 'Modifying the sealed PrincipalRequestContext class in services/request_context/context.py to add __enter__/__exit__ is an edit to a sealed class — SO §3.8 forbids it. Unwind to a wrapper: revert context.py byte-identically to its sealed state, author a context-manager adapter inside services/enforce/ that owns the protocol, re-point the R-100 portal routers to the wrapper, seal as a self-reported §3.8 lapse cured, regenerate the three continuity bundles, pin their sha256s in STATE/PINS.md, then hold at the R-91 horizon (no expedite).' Sealed backend/services/request_context/context.py restored byte-identical to Commit 4b3b5e0 (git show + diff IDENTICAL · sha256 ad0d94399af44bd5f6fa57f9aa1371ede7ca526789e47db10b45dddc79c39cfb) · NEW backend/services/enforce/principal_context_adapter.py wrapper (single public callable principal_context @contextlib.contextmanager · try/finally reset-Token so exit clears propagation on both normal AND exceptional exits without leaking · yields sealed PrincipalRequestContext carrier unchanged · PRIN-13 immutable-by-refusal preserved verbatim · docstring cites owner UNWIND ruling as §3.8 lapse cure) · portal_requests.py + portal_entitlement.py re-pointed to wrapper (9 substitutions · atomic sed) · NEW tests/invariants/test_principal_context_adapter.py with 5 tests (5 new · module-importable + enters-and-yields + exit-clears + exception-propagates-and-clears + sealed-bytes-sha256-pinned as SO §3.8 structural guard) · baseline_failures.json ratchet 5852 → 5857 both fields (measured = targeted · no CCS2 correction) · new baseline_failures.json sha256 ee8569b871bb08537c4201b375c177d51b196f6d0583a9ac762b55d0e8c58671 · SCOPE FROZEN SO §6.4 NOTHING-BEYOND (1 sealed-restore + 1 new wrapper + 1 new test module + 2 router re-points + 1 ratchet bump · zero other file change · zero implementation module edit outside this-wave) · sealed R-100 portal write surface + R-99 canon-rules HTTP router + R-96..R-98 canon vocabulary + R-88..R-95 seal chain all continue verbatim GREEN · additive-only per SO §3.8 · AUTHENTIC RED-first cycle drill_receipts/20260921T112718Z_r100_unwind_wrapper_RED_pre.log (5/5 fail right-reason ModuleNotFoundError services.enforce.principal_context_adapter tests 1-4 + AssertionError sealed-bytes-sha256-drift test 5 while illegal cure still present) → GREEN drill_receipts/20260921T112831Z_r100_unwind_wrapper_GREEN_post.log (39/39 pass 0.90s covering 5 new adapter + all 21 R-100 portal write surface + all 13 principal model v1) → deterministic BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep byte-identical stripped-sha256 27240fc197ca711f3712e61f086183683f71200e13320d3005d5445f39e463a4 IDENTICAL across run1 (185.67s 5857 passed) + run2 (181.96s 5857 passed) both 3 baseline-fails (subset · pod_shell mirror-drift · pending R-91 CEREMONY-OPEN horizon retirement) 1 skip 438 warnings · live curl matrix 20260921T113830Z all 14 endpoints working with cured wrapper (5 R-99 canon-rules public 200 + 9 R-100 portal 200/202/404 with seeded JWT + 4 R-100 portal 401 without JWT · zero 500 · CM wrapper effective · sealed carrier untouched · PRIN-11/PRIN-13 preserved) · Canon anchors verbatim: owner UNWIND directive this-session (2026-09-21T~11:00Z) + Principal Model Spec v1 §5 PRIN-11 propagation-by-construction + PRIN-13 read-only-once-in-propagation (both preserved verbatim on sealed carrier · wrapper owns only with-block protocol) + R-100 seal 39412d09/e6a86c2c/0ae3713f + R-100-A OPERATIONAL CURE at 320a752/00827f7a (this-lapse REVERTED-AND-BANKED · not rewritten in history · Commit-A here builds on top additively reverting the illegal in-place edit and adding the wrapper) + SO §2.5 verbatim-docstring + §3 tests-first + §3.3 3-Commit Seal + §3.8 additive-only (violated at 320a752 · cured this-wave · sealed-bytes sha-pin now structurally guards file against future in-place edits) + §6.4 NOTHING-BEYOND + §6.7 seal-report-boundary + M16-W3 corrected order · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · Structural §3.8 guard: test_context_py_sealed_bytes_sha256_pinned pins the sealed file's sha256 (ad0d9439...) making any future in-place edit structurally detectable · a repair-mechanism not a review-mechanism · Autopilot next Commit-B state master (banks this-Commit-A + regen tool + seal report + DECISIONS append) → Commit-C fixup (this-turn advances state_head + inserts code_repo entry + Continuity Bundle regen 3 bundles + STATE/PINS.md sha256 pins) → HOLD for R-91 horizon (NO EXPEDITE) → R-91 ε-APPLY at 2026-09-23T03:23:15Z → M1-to-date BUILD_JOURNAL closure state-only"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    if f"head: {R100_UNWIND_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-100-UNWIND Commit-B.")
    else:
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
        text = (
            text[: m.start()]
            + NEW_STATE_REPO_BLOCK
            + NEW_R100_UNWIND_CODE_REPO_BLOCK
            + text[m.end():]
        )

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
    print(f"heads_last_sealed.state_repo.head → {R100_UNWIND_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R100_UNWIND_CODE_HEAD}")


if __name__ == "__main__":
    main()
