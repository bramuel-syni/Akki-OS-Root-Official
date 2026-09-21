"""R-94 Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Mirrors tools/r93_commit_c_fixup_orch_boot_regen.py precedent exactly.
- state_repo (heads_last_sealed.state_repo): replaced with R-94 Commit-B
  `98963a11bc5720516ca04ee5943fa96b912ab827` entry.
- code_repo history: fresh entry for R-94 Commit-A
  `1115a332b42072c6ea010e07c2163bcb65991ca4` INSERTED at the top of the
  history (immediately after state_repo), preserving all prior code_repo
  entries in chronological order.
- generated_at_utc + regeneration_reason: updated to R-94 Commit-C fixup.
- POD audit mirror: /app/frontend/public/audit/ORCH_BOOT.md byte-identically
  synced via shutil.copyfile (no remote calls).

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R94_STATE_HEAD).

Standing bounds: zero push · zero remote · zero network.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R94_STATE_HEAD = "98963a11bc5720516ca04ee5943fa96b912ab827"
R94_CODE_HEAD = "1115a332b42072c6ea010e07c2163bcb65991ca4"
R94_STATE_SEALED_AT = "2026-09-21T05:20:00Z"
R94_CODE_SEALED_AT = "2026-09-21T05:15:00Z"
NEW_UTC = "2026-09-21T05:30:00Z"
NEW_REGEN_REASON = (
    "r94-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-"
    "98963a11-cp-g5v5-doc5-a5-1-to-a5-6-first-sub-slice-commit-b-plus-new-"
    "code-repo-history-entry-for-r94-commit-a-1115a332-ruling-5-family-b-"
    "doc-5-m10-northena-part-a-a5-1-to-a5-6"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R94_STATE_HEAD}
    sealed_at_utc: {R94_STATE_SEALED_AT}
    seal_kind: "CP-G5V5-DOC5-A5-1-TO-A5-6 first sub-slice · Doc 5 M10 Northena Part A (A5.1..A5.6) · Promise #16 Focus maintained under massive context · state Commit-B `{R94_STATE_HEAD}` · banks Commit-A `{R94_CODE_HEAD}` on programme/track-a · WAVE R-94 · Family B · Ruling 5 execution + owner ruling this-session verbatim (2026-09-21T~03:53Z: 'GO — Family A first sub-slice HUNT-and-authoring, exactly per your posture plan ... Standing GO extends through the R-91 window: Family A → Family B (Doc 5 Northena) → DAP-1..38 → RBM + ROC, Tier A before Tier B per the owner's sequencing, sub-slice sizes at your discretion for clean seals, no per-slice check-ins needed (SO §6 governs)') · canon_ref resolves against v5 SRR sheet ONLY sha256 00072c58... (Ruling 5) · rule text governs (Ruling 3 erratum · source-column shape extended this-session) · Rule text extracted verbatim from fixtures/files_9_extracted/05_Direction_Scope_and_Focus_Part_1_Northena.docx sha256 f280356ec9957e14511b60b9561dd0f9ba3d009d9960a870657c0fe0c9ed7cdc · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · New backend package services/canon_doc5_northena/ (net-new · SO §3.8 additive-only) · 6 property invariants A5.1..A5.6 + 2 registry-shape tests + 6 pure-data-in grep-negative scanner tests = 14 total · 6 grep-negative scanners registered where rule text explicitly negates a pattern (A5.1 northena_ml_import + A5.2 score_based_admission_rationale + A5.3 northena_governor_internals_or_inference + A5.4 gate_inferential_path + A5.5 learned_stopping_or_extra_halt_owner + A5.6 executor_owned_budget_ceiling) · DELTA +16 MEASURED (5711 → 5727 monotonic-up per CCS2 both fields bumped together · +14 new Doc 5 Part A tests · +2 v8 tests spontaneously transitioning fail→pass from R-88+ baseline set carrying forward · CCS2 measured-not-targeted correction 5725→5727 landed pre-double-sweep · baseline_failures[] array NOT shrunk this-slice per R-91 CEREMONY-OPEN owner directive · atomic 5→0 retirement scheduled at R-91 apply-step operation 4) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 7b394b139e6496e67b8b4e9cb453a48bc18259b300dcecbe6dfc4527f49515c2 IDENTICAL across drill_receipts/20260921T050600Z_run1 (182.81s · 5727 passed) + 20260921T051000Z_run2 (183.60s · 5727 passed) both 3 baseline-fails (3 pod_shell mirror-drift · 2 v8 cascade tests now passing outside failing set · covered by exactly one annotation field under total-coverage guard verified this-slice) 1 skip 438 warnings against post-bump baseline_failures.json sha256 a1550d35ec976c70ce7b4ca9b683e00e5b3f6c7cdda2594bd21b121b64b25014 · notes/ORCH_BOOT.md pre-Commit-A ratchet-only regen + byte-identical POD audit mirror sync (both sha256 c47cb387d7c26a4dfc75281bdec5e5ab7ac537bf083fee7e45af5625d3d71243) · HUNT-first via python-docx extraction + openpyxl SRR sha-pin verification banked at phase0/spec_hunt_receipts/20260921T045000Z_g5v5_family_b_doc5_northena_hunt_data.json (v5 workbook sha-pin 00072c58 verified · Doc 5 source .docx sha f280356e verified · 11 rows found at SRR rows 64-79 · this-slice covers 6 A5 rows 64-69 · Part B B5 rows 75-79 queued next) · R-88+ OWNER-RATIFICATION-PENDING RETIRED at a30db4f7 (not-restated) · Total-coverage guard (Guard #1 from R-88+) still GREEN across this slice's double-sweep · R-86 Property tests (Guard #2 from R-88+) still GREEN (annotation set unchanged this-slice) · Canon anchors verbatim: owner ruling this-session (2026-09-21T~03:53Z Family A GO + standing-GO through R-91 window) + owner Ruling 5 SRR-as-authority + owner Ruling 3 erratum + owner G5-v5 sequencing (2026-09-21T~01:00Z at a30db4f7 · Doc 1 M12 → Doc 5 M10 → DAP-1..38 → RBM+ROC · Tier A first · rows 1-565) + Master Requirements Registry v5 SRR rows 64-69 as authority (Ruling 5) + Doc 5 source .docx sha f280356e (byte-verified this-wave) + R-93 seal 36668e3/ee30ca98/de4f31bd (immediately-precedes · Family A · CP-G5V5-DOC1-A5-1-TO-A5-9 first sub-slice · establishes Final[...]-constants + pure-data-in-scanner + grep-negative-ban-anchor pattern this wave inherits) + R-92 seal ceaa24f/19030610/e8f9f168 + R-91 Phase 1 seal 282ba19e + R-91 CEREMONY-OPEN a30db4f7 (APPLY horizon 2026-09-23T03:23:15Z unaffected by this slice) + R-90/R-89/R-88 seal chain + prior R-85/R-86/R-87 seal chain + SO §2.5 verbatim-docstring + §3 tests-first + §3.3 3-Commit Seal + §3.8 additive-only + §3.10-α Final[str] closed-vocab + §6 autopilot governance (Ruling 5 scope · full SO §6 autonomy · measured ratchet not targeted · standing-GO through R-91 window · no per-slice check-in) + §6.4 NOTHING-BEYOND + §6.7 seal-report-boundary + M16-W3 corrected order + CCS2 lesson · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-C fixup this-turn (this-file R-6 regen advances state_repo.head to {R94_STATE_HEAD} + inserts code_repo entry for R94 Commit-A {R94_CODE_HEAD}) → G5-v5 Family B second sub-slice (Doc 5 Part B · B5.1..B5.5 · Promise #18 direction half · Objective Preservation · Ledger append-only writer · SRR rows 75..79) HUNT-and-authoring per owner sequencing → R-91 CP-APP-JS-UNIFY Phase 2 stays CEREMONY-IN-FLIGHT · APPLY 2026-09-23T03:23:15Z"
"""

NEW_R94_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R94_CODE_HEAD}
    sealed_at_utc: {R94_CODE_SEALED_AT}
    seal_kind: "CP-G5V5-DOC5-A5-1-TO-A5-6 first sub-slice · Commit-A `{R94_CODE_HEAD}` · code programme/track-a · WAVE R-94 · Family B · Ruling 5 execution · Adds net-new backend package services/canon_doc5_northena/__init__.py + services/canon_doc5_northena/northena_a5_vocabulary.py + tests/invariants/test_g5v5_doc5_a5_1_to_a5_6.py · Registers A5.1..A5.6 canon vocabulary as load-bearing Final[...] constants (SRR row 64..69 statement text + source file:line + invariant Final[bool] flags derived from rule text · V7 authored strictly from rule text per Ruling 3 erratum · SRR Enforcement Class column empty for all 6 Doc 5 Part A rows) · 6 pure-data-in grep-negative scanners: scan_for_northena_ml_import (A5.1 · 5 patterns · rule text 'No Northena module imports a machine-learning library or a learned component') + scan_for_score_based_admission_rationale (A5.2 · 5 patterns · rule text names 'Admitted because the model scored it highly enough' as unauditable outcome) + scan_for_northena_governor_internals_or_inference (A5.3 · 5 patterns · rule text 'Northena never reads that governor's internals and never performs inference itself') + scan_for_gate_inferential_path (A5.4 · 5 patterns · rule text 'No inferential path exists in Gate') + scan_for_learned_stopping_or_extra_halt_owner (A5.5 · 5 patterns · rule text 'There is no learned stopping' + 'stop decision and record belong to Northena alone') + scan_for_executor_owned_budget_ceiling (A5.6 · 5 patterns · rule text 'enforced by the governor rather than by the executor that could be tempted to keep going') · Top-level DOC5_A5_RULE_IDS 6-tuple + DOC5_A5_RULE_COUNT=6 · 14 tests total: 2 registry-shape + 6 property + 6 scanner · each carries SO §2.5 verbatim-docstring quoting rule text byte-verbatim · each property test asserts Final[...] annotation + value binding · scanner tests enforce clean-input-empty + each-watched-pattern-hits invariant byte-verbatim · DELTA +16 MEASURED (5711 → 5727 monotonic-up per CCS2 both fields bumped together · new baseline_failures.json sha256 a1550d35 was 870eac9a · new ORCH_BOOT.md sha256 c47cb387 both notes and POD audit mirror byte-identical) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · zero implementation module edit outside this-wave · zero sealed contract/writer/test file edit · sealed canon_doc1_chokepoint (R-93 SEALED) + security_function_policies (R-92 SEALED) + content_registry (R-88..R-90 SEALED) all continue verbatim GREEN · R-88+ OWNER-RATIFICATION-PENDING RETIRED at a30db4f7 (not restated) · AUTHENTIC RED-first cycle: RED at drill_receipts/20260921T045700Z_r94_family_b_doc5_a5_1_to_a5_6_RED_pre.log (14/14 fail collection right-reason ImportError services.canon_doc5_northena.northena_a5_vocabulary module absent) → GREEN at drill_receipts/20260921T045500Z_r94_family_b_doc5_a5_1_to_a5_6_GREEN_post.log (14/14 pass 0.69s) → BASELINE_GUARD=1 double-sweep byte-identical stripped-sha256 7b394b13 IDENTICAL run1 (5727 passed) + run2 (5727 passed) both 3 baseline-fails 1 skip 438 warnings · pre-Commit-A ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order + byte-identical POD audit-mirror sync (tools/r94_pre_commit_a_ratchet_and_orch_boot_regen.py) · Canon anchors verbatim: owner ruling this-session (2026-09-21T~03:53Z Family A GO + standing-GO through R-91 window) + owner Ruling 5 SRR-as-authority + owner Ruling 3 erratum + owner G5-v5 sequencing (2026-09-21T~01:00Z at a30db4f7) + Master Requirements Registry v5 SRR rows 64-69 · Doc 5 A5.1..A5.6 · Northena canon · R-93 seal (immediately-precedes) · R-91 CEREMONY-OPEN a30db4f7 · prior seal chain R-85/R-86/R-87/R-88/R-89/R-90/R-92 + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + §6 autopilot governance + M16-W3 + CCS2 · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-B state master → Commit-C fixup → G5-v5 Family B second sub-slice (Doc 5 Part B · B5.1..B5.5) queued"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    if f"head: {R94_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-94 Commit-B.")
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
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R94_CODE_REPO_BLOCK + text[m.end():]

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
    print(f"heads_last_sealed.state_repo.head → {R94_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R94_CODE_HEAD}")


if __name__ == "__main__":
    main()
