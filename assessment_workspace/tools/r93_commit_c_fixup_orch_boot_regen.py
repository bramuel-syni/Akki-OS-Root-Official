"""R-93 Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Mirrors tools/r92_commit_c_fixup_orch_boot_regen.py precedent exactly.
- state_repo (heads_last_sealed.state_repo): replaced with R-93 Commit-B
  `ee30ca980a1e61c45db858444a91894fa7e65513` entry.
- code_repo history: fresh entry for R-93 Commit-A
  `36668e371bd4c99d0a0ee3ffde706b1bf4a34af3` INSERTED at the top of the
  history (immediately after state_repo), preserving all prior code_repo
  entries in chronological order.
- generated_at_utc + regeneration_reason: updated to R-93 Commit-C fixup.
- POD audit mirror: /app/frontend/public/audit/ORCH_BOOT.md byte-identically
  synced via shutil.copyfile (no remote calls).

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R93_STATE_HEAD).

Standing bounds: zero push · zero remote · zero network.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R93_STATE_HEAD = "ee30ca980a1e61c45db858444a91894fa7e65513"
R93_CODE_HEAD = "36668e371bd4c99d0a0ee3ffde706b1bf4a34af3"
R93_STATE_SEALED_AT = "2026-09-21T04:15:00Z"
R93_CODE_SEALED_AT = "2026-09-21T04:00:00Z"
NEW_UTC = "2026-09-21T04:45:00Z"
NEW_REGEN_REASON = (
    "r93-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-"
    "ee30ca98-cp-g5v5-doc1-a5-1-to-a5-9-first-sub-slice-commit-b-plus-new-"
    "code-repo-history-entry-for-r93-commit-a-36668e3-ruling-5-family-a-"
    "doc-1-m12-chokepoint-a5-1-to-a5-9"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R93_STATE_HEAD}
    sealed_at_utc: {R93_STATE_SEALED_AT}
    seal_kind: "CP-G5V5-DOC1-A5-1-TO-A5-9 first sub-slice · Doc 1 M12 chokepoint (A5.1..A5.9) · state Commit-B `{R93_STATE_HEAD}` · banks Commit-A `{R93_CODE_HEAD}` on programme/track-a · WAVE R-93 · Family A · Ruling 5 execution + owner ruling this-session verbatim (2026-09-21T~03:53Z: 'GO — Family A first sub-slice HUNT-and-authoring, exactly per your posture plan ... Standing GO extends through the R-91 window: Family A → Family B (Doc 5 Northena) → DAP-1..38 → RBM + ROC, Tier A before Tier B per the owner's sequencing, sub-slice sizes at your discretion for clean seals, no per-slice check-ins needed (SO §6 governs)') · canon_ref resolves against v5 SRR sheet ONLY sha256 00072c58... (Ruling 5) · rule text governs (Ruling 3 erratum · source-column shape extended this-session) · Rule text extracted verbatim from fixtures/files_9_extracted/01_Custody_and_the_Crossing_Part_1_The_Chokepoint.docx sha256 a33588298100c6224366623e64ac8632b48294649e57ad43cf67ee6730f97844 (source-doc block CLEARED at state commit afd0f3c7 · falsified prior fork's `.md`-missing misreport by direct extraction · correction addendum banked at spec_hunt_receipts/20260921T034200Z_g5v5_family_a_doc1_source_doc_false_negative_correction_addendum.md) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND (state-side additive banking only: DECISIONS append + NEXT append + PINS append with R-93-FIRST-SUB-SLICE-PINS block + ORCH_BOOT already ratchet-only regen'd pre-Commit-A · 2 new tools (pre-commit-a ratchet+regen + this Commit-C fixup) · 2 HUNT receipts + 4 drill receipts · zero card edit this-slice · zero implementation module edit outside this-wave · zero sealed contract/writer/test file edit) · New backend package services/canon_doc1_chokepoint/ (net-new · SO §3.8 additive-only) · 9 property invariants A5.1..A5.9 + 2 registry-shape tests + 5 pure-data-in grep-negative scanner tests = 16 total · 5 grep-negative scanners registered where rule text explicitly negates a pattern (A5.1 non_chokepoint_model_invocation + A5.3 envelope_persistence + A5.5 outbound_network_outside_crossing + A5.7 credential_at_receipt + A5.9 degraded_answer_on_grounding_failure) · No scanner for A5.2/A5.4/A5.6/A5.8 per owner directive 'grep-negative bans where the rule text states them' (invariants asserted without negating specific patterns · SFP-1..7 precedent) · DELTA +16 MEASURED (5695 → 5711 monotonic-up per CCS2 both fields bumped together · no test flipped to fail · CCS2-aligned across counts.passed/passed_floor/ratchet_history[-1].passed) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 ee3e1fb7... IDENTICAL across run1+run2 both 5711 passed / 5 baseline-fails (3 mirror-drift + 2 v8 cascade all from R-88+ carrying forward · covered by exactly one annotation field under total-coverage guard verified this-slice) / 1 skip against post-bump baseline_failures.json sha256 870eac9a06f25cbf2b5591b9084bbb9c4a1555719ac183f9c8dfd44700cf18b1 · notes/ORCH_BOOT.md pre-Commit-A ratchet-only regen + byte-identical POD audit mirror sync (both sha256 0fade309efb9fbb98b42e72fc24225debf8c05fce68302faa0e3750f454e265f) · HUNT-first via python-docx extraction + openpyxl SRR sha-pin verification banked at phase0/spec_hunt_receipts/20260921T034500Z_g5v5_family_a_doc1_a5_1_to_a5_9_authoring_hunt_data.json · sha-pin verified against v5 workbook 00072c58 before any row was read · R-88+ OWNER-RATIFICATION-PENDING RETIRED at a30db4f7 (D+A ratification banked · not restated this-slice) · Total-coverage guard (Guard #1 from R-88+) still GREEN across this slice's double-sweep · R-86 Property tests (Guard #2 from R-88+) still GREEN (annotation set unchanged this-slice) · Canon anchors verbatim: owner ruling this-session (2026-09-21T~03:53Z Family A GO) + owner Ruling 5 SRR-as-authority (2026-09-20T~19:00Z · v5 workbook sha 00072c58...) + owner Ruling 3 erratum (class column HINT · rule text governs) + owner G5-v5 second slice sequencing (2026-09-21T~01:00Z at a30db4f7: Doc 1 M12 → Doc 5 M10 → DAP-1..38 → RBM+ROC · Tier A first · rows 1-565) + Master Requirements Registry v5 SRR sheet rows R2..R10 as authority (Ruling 5) + R-92 seal ceaa24f/19030610/e8f9f168 (immediately-precedes · CP-G5V5-SFP-1-7 first slice · establishes Final[...]-constants + pure-data-in-scanner + grep-negative-ban-anchor pattern this wave inherits) + R-91 Phase 1 seal 282ba19e + R-91 CEREMONY-OPEN seal a30db4f7 (D+A ratification + G5-v5 sequencing · APPLY 2026-09-23T03:23:15Z unaffected by this slice) + R-90 seal 457d947/19bfd333/44d2ae74 (CLOSES Ruling-4 scope) + R-89 seal 49e2a338/76c530f0/f2638177 + R-88 seal db90089d/79d5d38d/0cbfc23b + prior seal chain R-85/R-86/R-87 + SO §2.5 verbatim-docstring + §3 tests-first + §3.3 3-Commit Seal + §3.8 additive-only + §3.10-α Final[...] closed-vocab + §6 autopilot governance (Ruling 5 scope · full SO §6 autonomy · measured ratchet not targeted) + §6.4 NOTHING-BEYOND + §6.7 seal-report-boundary + M16-W3 corrected order + CCS2 lesson · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-C fixup this-turn (this-file R-6 regen advances state_repo.head to {R93_STATE_HEAD} + inserts code_repo entry for R93 Commit-A {R93_CODE_HEAD}) → G5-v5 Family B (Doc 5 Northena) HUNT-and-authoring queued next per owner sequencing (2026-09-21T~01:00Z verbatim + 2026-09-21T~03:53Z standing GO through R-91 window) → R-91 CP-APP-JS-UNIFY Phase 2 stays CEREMONY-IN-FLIGHT · APPLY 2026-09-23T03:23:15Z"
"""

NEW_R93_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R93_CODE_HEAD}
    sealed_at_utc: {R93_CODE_SEALED_AT}
    seal_kind: "CP-G5V5-DOC1-A5-1-TO-A5-9 first sub-slice · Commit-A `{R93_CODE_HEAD}` · code programme/track-a · WAVE R-93 · Family A · Ruling 5 execution · Adds net-new backend package services/canon_doc1_chokepoint/__init__.py + services/canon_doc1_chokepoint/chokepoint_vocabulary.py + tests/invariants/test_g5v5_doc1_a5_1_to_a5_9.py · Registers A5.1..A5.9 canon vocabulary as load-bearing Final[...] constants (SRR row R2..R10 statement text + source file:line + invariant Final[bool] flags derived from rule text · V7 authored from rule text per Ruling 3 erratum extended source-column shape this-session) · 5 pure-data-in grep-negative scanners: scan_for_non_chokepoint_model_invocation (A5.1 · 5 patterns · rule text 'fails the build if any module other than the chokepoint function imports or invokes the model client') + scan_for_envelope_persistence (A5.3 · 5 patterns · rule text 'never persisted to disk as a standing record, never shared between requests, and never available to any consumer after the call completes') + scan_for_outbound_network_outside_crossing (A5.5 · 5 patterns · rule text 'No other module in the platform holds outbound network capability' + build gate) + scan_for_credential_at_receipt (A5.7 · 5 patterns · rule text 'the credential used to reach the model is never logged or included') + scan_for_degraded_answer_on_grounding_failure (A5.9 · 5 patterns · rule text 'refusal, not a weaker answer offered anyway') · No scanner for A5.2/A5.4/A5.6/A5.8 (rule text asserts invariants without negating specific patterns · SFP-1..7 precedent) · Top-level DOC1_A5_RULE_IDS 9-tuple + DOC1_A5_RULE_COUNT=9 · 16 tests total: 2 registry-shape tests + 9 property tests + 5 grep-negative scanner tests · each carries SO §2.5 verbatim-docstring quoting rule text byte-verbatim · each property test asserts Final[...] annotation + value binding · scanner tests enforce clean-input-empty + each-watched-pattern-hits invariant byte-verbatim · DELTA +16 MEASURED (5695 → 5711 monotonic-up per CCS2 both fields bumped together · new baseline_failures.json sha256 870eac9a was 4e7caa47 · new ORCH_BOOT.md sha256 0fade309 both notes and POD audit mirror byte-identical) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · zero implementation module edit outside this-wave · zero sealed contract/writer/test file edit · sealed M12 code (services/chokepoint/*) NOT edited · sealed M12 tests NOT edited · services/security_function_policies/* NOT edited (R-92 GREEN carries forward) · services/content_registry/* NOT edited (R-88..R-90 GREEN carries forward) · R-88+ OWNER-RATIFICATION-PENDING RETIRED at a30db4f7 (not-restated) · AUTHENTIC RED-first cycle: source-doc false-negative correction FIRST (prior fork misreported `.md` files missing · falsified by python-docx text extraction at 01_Custody_and_the_Crossing_Part_1_The_Chokepoint.docx byte-verified · correction banked at state commit afd0f3c7) → HUNT extraction of A5.1..A5.9 rule text byte-verbatim → author vocabulary Final[...] bindings → RED sweep (16/16 fail right-reason ModuleNotFoundError services.canon_doc1_chokepoint) → GREEN sweep (16/16 pass) → pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 ee3e1fb7 IDENTICAL run1+run2 both 5711 passed 5 baseline-fails 1 skip · pre-Commit-A ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order + byte-identical POD audit-mirror sync (tools/r93_pre_commit_a_ratchet_and_orch_boot_regen.py both sha256 0fade309) · Canon anchors verbatim: owner ruling this-session (2026-09-21T~03:53Z Family A GO) + owner Ruling 5 SRR-as-authority + owner Ruling 3 erratum + owner G5-v5 sequencing (2026-09-21T~01:00Z at a30db4f7 · Doc 1 M12 first) + Master Requirements Registry v5 SRR rows R2..R10 · Doc 1 A5.1..A5.9 · Custody-and-the-Crossing-Part-1-The-Chokepoint canon · R-92 seal (immediately-precedes) · R-91 Phase 1 seal 282ba19e · R-91 CEREMONY-OPEN a30db4f7 (D+A ratified · G5-v5 sequencing banked · APPLY 2026-09-23T03:23:15Z) · prior seal chain R-85/R-86/R-87/R-88/R-89/R-90 + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + §6 autopilot governance + M16-W3 + CCS2 · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-B state master → Commit-C fixup → G5-v5 Family B (Doc 5 Northena) sub-slice HUNT-and-authoring queued"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    if f"head: {R93_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-93 Commit-B.")
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
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R93_CODE_REPO_BLOCK + text[m.end():]

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
    print(f"heads_last_sealed.state_repo.head → {R93_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R93_CODE_HEAD}")


if __name__ == "__main__":
    main()
