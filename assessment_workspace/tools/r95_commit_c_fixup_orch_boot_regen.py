"""R-95 Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Mirrors tools/r94_commit_c_fixup_orch_boot_regen.py precedent exactly.
- state_repo (heads_last_sealed.state_repo): replaced with R-95 Commit-B
  `bee3e32aad7ffa1942d6d08f25b39d0c4124e032` entry.
- code_repo history: fresh entry for R-95 Commit-A
  `c16edf2aee1996d542c03bfce372618b1bdc2893` INSERTED at the top of the
  history (immediately after state_repo), preserving all prior code_repo
  entries in chronological order (R-94 Commit-A `1115a332` remains as the
  next-most-recent entry).
- generated_at_utc + regeneration_reason: updated to R-95 Commit-C fixup.
- POD audit mirror: /app/frontend/public/audit/ORCH_BOOT.md byte-identically
  synced via shutil.copyfile (no remote calls).

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R95_STATE_HEAD).

Standing bounds: zero push · zero remote · zero network.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R95_STATE_HEAD = "bee3e32aad7ffa1942d6d08f25b39d0c4124e032"
R95_CODE_HEAD = "c16edf2aee1996d542c03bfce372618b1bdc2893"
R95_STATE_SEALED_AT = "2026-09-21T06:00:00Z"
R95_CODE_SEALED_AT = "2026-09-21T05:55:00Z"
NEW_UTC = "2026-09-21T06:05:00Z"
NEW_REGEN_REASON = (
    "r95-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-"
    "bee3e32a-cp-g5v5-doc5-b5-1-to-b5-5-second-sub-slice-commit-b-plus-new-"
    "code-repo-history-entry-for-r95-commit-a-c16edf2a-ruling-5-family-b-"
    "doc-5-m10-northena-part-b-b5-1-to-b5-5"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R95_STATE_HEAD}
    sealed_at_utc: {R95_STATE_SEALED_AT}
    seal_kind: "CP-G5V5-DOC5-B5-1-TO-B5-5 second sub-slice · Doc 5 M10 Northena Part B (B5.1..B5.5) · Promise #18 direction half Objective Preservation (Direction Half) · state Commit-B `{R95_STATE_HEAD}` · banks Commit-A `{R95_CODE_HEAD}` on programme/track-a · WAVE R-95 · Family B · Ruling 5 execution + owner ruling this-session verbatim (2026-09-21T~05:20Z: 'GO — R-95 Family B Part B (B5.1..B5.5 · Promise #18 · Ledger) confirmed as the next wave, plan verbatim as you stated it. ... Standing GO continues through the G5 family queue per SO §6 — seal reports at boundaries, no per-slice check-ins needed. Proceed.') · canon_ref resolves against v5 SRR sheet ONLY sha256 00072c58... (Ruling 5) · rule text governs (Ruling 3 erratum · source-column shape extended this-session) · Rule text extracted verbatim from fixtures/files_9_extracted/05_Direction_Scope_and_Focus_Part_1_Northena.docx sha256 f280356ec9957e14511b60b9561dd0f9ba3d009d9960a870657c0fe0c9ed7cdc (byte-verified at R-94) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · New backend module services/canon_doc5_northena/northena_b5_ledger.py (additive to R-94-sealed package · SO §3.8 additive-only) · 5 property invariants B5.1..B5.5 + 2 registry-shape tests + 4 pure-data-in grep-negative scanner tests = 11 total · 4 grep-negative scanners registered where rule text explicitly negates a pattern (B5.1 live_admission_edit + B5.2 downstream_lawful_basis_filter + B5.4 ledger_update_or_delete + B5.5 side_channel_typing_or_mutation) · B5.3 shape invariant (two admission paths · both write Ledger row · both freeze the same way) carried by property test only · no scanner because rule text does not negate a specific behavior pattern · DELTA +11 MEASURED (5727 → 5738 monotonic-up per CCS2 both fields bumped together · +11 new Doc 5 Part B tests · no v8 or other spontaneous transitions this-wave · targeted equalled measured · no CCS2 correction needed contrast R-94 which had +2 v8 transitions on top of +14 targeted · baseline_failures[] array NOT shrunk this-slice per R-91 CEREMONY-OPEN owner directive · atomic 5→0 retirement scheduled at R-91 apply-step operation 4) · pre-Commit-A ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order + byte-identical POD audit mirror sync (both sha256 c88088e118d30b8cc2fea24f4dbcaa5e85489a3f97a49f01a5a788367ad48108) · CCS2 lesson extended this-wave (hash-seed nondeterminism): first BASELINE_GUARD=1 sweep-pair 20260921T054100Z_run1 (182.76s · 5738 passed) + 20260921T054500Z_run2 (182.56s · 5738 passed) diverged in stripped-sha256 due to PYTHONHASHSEED random-per-process affecting pod_shell mirror-drift baseline-failed test's set-iteration order (pytest 5-item truncated set diff subset differs per run) → deterministic BASELINE_GUARD=1 double-sweep byte-identical stripped-sha256 c52c47da48fb555439c896c7c057e09294c9671dacf40efa83627f3f84b8ba23 IDENTICAL across drill_receipts/20260921T055000Z_run1 (183.52s · 5738 passed) + 20260921T055400Z_run2 (183.37s · 5738 passed) both under PYTHONHASHSEED=0 BASELINE_GUARD=1 · both 3 baseline-fails 1 skip 438 warnings against post-bump baseline_failures.json sha256 44ffe113 · CCS2 invariant surface (passed count · fail set membership · skipped count · warnings count) matches EXACTLY across all 4 sweeps · lesson recorded for R-96+: default to PYTHONHASHSEED=0 BASELINE_GUARD=1 for double-sweep receipts · HUNT-first evidence already banked at R-94 in phase0/spec_hunt_receipts/20260921T045000Z_g5v5_family_b_doc5_northena_hunt_data.json (SRR sha-pin 00072c58 verified · Doc 5 source .docx sha f280356e verified · 11 rows found at SRR rows 64-79 · this-slice covers 5 B5 rows 75-79 with verbatim docx paragraph indices 63-67) · R-88+ OWNER-RATIFICATION-PENDING RETIRED at a30db4f7 (not-restated) · Total-coverage guard (Guard #1 from R-88+) still GREEN across this slice's double-sweep · R-86 Property tests (Guard #2 from R-88+) still GREEN (annotation set unchanged this-slice) · Canon anchors verbatim: owner ruling this-session (2026-09-21T~05:20Z R-95 Family B Part B GO + standing-GO through G5 family queue · seal reports at boundaries · no per-slice check-ins · never force-halt mid-atom · frozen proposal doesn't expire at horizon it merely becomes applicable · canon-text precedence with supersession logging in DECISIONS.md) + owner ruling prior-session (2026-09-21T~03:53Z Family A GO + standing-GO through R-91 window) + owner Ruling 5 SRR-as-authority + owner Ruling 3 erratum + owner G5-v5 sequencing (2026-09-21T~01:00Z at a30db4f7 · Doc 1 M12 → Doc 5 M10 → DAP-1..38 → RBM+ROC · Tier A first · rows 1-565) + Master Requirements Registry v5 SRR rows 75-79 as authority (Ruling 5) + Doc 5 source .docx sha f280356e (byte-verified at R-94) + R-94 seal 1115a332/98963a11/Commit-C fixup (immediately-precedes · Family B first sub-slice · CP-G5V5-DOC5-A5-1-TO-A5-6 Part A · establishes Final[...]-constants + pure-data-in-scanner + grep-negative-ban-anchor pattern this wave inherits) + R-93 seal 36668e3/ee30ca98/de4f31bd (Family A · Doc 1 M12) + R-92 seal ceaa24f/19030610/e8f9f168 + R-91 Phase 1 seal 282ba19e + R-91 CEREMONY-OPEN a30db4f7 (APPLY horizon 2026-09-23T03:23:15Z unaffected by this slice · current UTC 2026-09-21T~06:00Z < horizon · ~45.4h out) + R-90/R-89/R-88 seal chain + prior R-85/R-86/R-87 seal chain + SO §2.5 verbatim-docstring + §3 tests-first + §3.3 3-Commit Seal + §3.8 additive-only + §3.10-α Final[str] closed-vocab + §6 autopilot governance (Ruling 5 scope · full SO §6 autonomy · measured ratchet not targeted · standing-GO through G5 family queue · no per-slice check-in) + §6.4 NOTHING-BEYOND + §6.7 seal-report-boundary + M16-W3 corrected order + CCS2 lesson (extended this-wave with hash-seed nondeterminism lesson) · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-C fixup this-turn (this-file R-6 regen advances state_repo.head to {R95_STATE_HEAD} + inserts code_repo entry for R95 Commit-A {R95_CODE_HEAD}) → G5-v5 Family C first sub-slice (DAP-1..38 lifecycle and principal model landing · Tier A first) per owner sequencing → R-91 CP-APP-JS-UNIFY Phase 2 stays CEREMONY-IN-FLIGHT · APPLY 2026-09-23T03:23:15Z"
"""

NEW_R95_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R95_CODE_HEAD}
    sealed_at_utc: {R95_CODE_SEALED_AT}
    seal_kind: "CP-G5V5-DOC5-B5-1-TO-B5-5 second sub-slice · Commit-A `{R95_CODE_HEAD}` · code programme/track-a · WAVE R-95 · Family B · Ruling 5 execution · Adds net-new backend module services/canon_doc5_northena/northena_b5_ledger.py + tests/invariants/test_g5v5_doc5_b5_1_to_b5_5.py · Registers B5.1..B5.5 canon vocabulary as load-bearing Final[...] constants (SRR row 75..79 statement text + source file:line + invariant Final[bool] flags derived from rule text · V7 authored strictly from rule text per Ruling 3 erratum · SRR Enforcement Class column empty for all 5 Doc 5 Part B rows) · 4 pure-data-in grep-negative scanners: scan_for_live_admission_edit (B5.1 · 5 patterns · rule text 'A changed intent is a new admission, never an edit of a live one') + scan_for_downstream_lawful_basis_filter (B5.2 · 5 patterns · rule text 'Purpose limitation is an admission property, not a downstream filter') + scan_for_ledger_update_or_delete (B5.4 · 6 patterns · rule text 'No update path and no delete path exists within the retention window' + 'Out-of-scope and refused items are recorded, never silently dropped') + scan_for_side_channel_typing_or_mutation (B5.5 · 5 patterns · rule text 'Typing it would harden it into a mutation surface' + 'Unit and audit stay in separate envelopes with separate lifecycles, joined by identity rather than embedded') · B5.3 shape invariant carried by property test only (no scanner because rule text asserts a shape invariant not a grep-negative pattern) · Top-level DOC5_B5_RULE_IDS 5-tuple + DOC5_B5_RULE_COUNT=5 · 11 tests total: 2 registry-shape + 5 property + 4 scanner · each carries SO §2.5 verbatim-docstring quoting rule text byte-verbatim · each property test asserts Final[...] annotation + value binding · scanner tests enforce clean-input-empty + each-watched-pattern-hits invariant byte-verbatim · DELTA +11 MEASURED (5727 → 5738 monotonic-up per CCS2 both fields bumped together · targeted equalled measured · no CCS2 correction needed · new baseline_failures.json sha256 44ffe113 was a1550d35 · new ORCH_BOOT.md sha256 c88088e1 both notes and POD audit mirror byte-identical) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · zero implementation module edit outside this-wave · zero sealed contract/writer/test file edit · sealed R-94 canon_doc5_northena.northena_a5_vocabulary + test_g5v5_doc5_a5_1_to_a5_6.py + __init__.py package marker all continue verbatim GREEN · sealed R-93 canon_doc1_chokepoint (R-93 SEALED) + R-92 security_function_policies (R-92 SEALED) + R-88..R-90 content_registry all continue verbatim GREEN · R-88+ OWNER-RATIFICATION-PENDING RETIRED at a30db4f7 (not restated) · AUTHENTIC RED-first cycle: RED at drill_receipts/20260921T053800Z_r95_family_b_doc5_b5_1_to_b5_5_RED_pre.log (11/11 fail collection right-reason ImportError cannot import name northena_b5_ledger from services.canon_doc5_northena) → GREEN at drill_receipts/20260921T053900Z_r95_family_b_doc5_b5_1_to_b5_5_GREEN_post.log (11/11 pass 0.71s) → first BASELINE_GUARD=1 sweep-pair drill_receipts/20260921T054100Z_run1 (182.76s · 5738 passed) + 20260921T054500Z_run2 (182.56s · 5738 passed) documenting CCS2 hash-seed nondeterminism finding on pod_shell mirror-drift assertion set-diff truncation → deterministic BASELINE_GUARD=1 double-sweep byte-identical stripped-sha256 c52c47da IDENTICAL across drill_receipts/20260921T055000Z_run1 + 20260921T055400Z_run2 both under PYTHONHASHSEED=0 BASELINE_GUARD=1 · both 5738 passed 3 baseline-fails 1 skip 438 warnings · pre-Commit-A ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order + byte-identical POD audit-mirror sync (tools/r95_pre_commit_a_ratchet_and_orch_boot_regen.py) · Canon anchors verbatim: owner ruling this-session (2026-09-21T~05:20Z R-95 Family B Part B GO + standing-GO through G5 family queue) + owner ruling prior-session (2026-09-21T~03:53Z Family A GO + standing-GO through R-91 window) + owner Ruling 5 SRR-as-authority + owner Ruling 3 erratum + owner G5-v5 sequencing (2026-09-21T~01:00Z at a30db4f7) + Master Requirements Registry v5 SRR rows 75-79 · Doc 5 B5.1..B5.5 · Northena canon · R-94 seal (immediately-precedes) · R-93/R-92/R-91 CEREMONY-OPEN a30db4f7 · prior seal chain R-85..R-90 + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + §6 autopilot governance + M16-W3 + CCS2 (extended this-wave with hash-seed nondeterminism lesson) · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-B state master → Commit-C fixup → G5-v5 Family C first sub-slice (DAP-1..38 lifecycle and principal model landing · Tier A first) queued"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    if f"head: {R95_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-95 Commit-B.")
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
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R95_CODE_REPO_BLOCK + text[m.end():]

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
    print(f"heads_last_sealed.state_repo.head → {R95_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R95_CODE_HEAD}")


if __name__ == "__main__":
    main()
