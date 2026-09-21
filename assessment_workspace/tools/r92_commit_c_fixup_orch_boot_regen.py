"""R-92 Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Mirrors tools/r90_commit_c_fixup_orch_boot_regen.py precedent exactly.
- state_repo (heads_last_sealed.state_repo): replaced with R-92 Commit-B
  `19030610d7e80072cfec498a72180f3304dd4f59` entry.
- code_repo history: fresh entry for R-92 Commit-A
  `ceaa24f41c8156c31e408b47fa8a59b3b265e6ac` INSERTED at the top of the
  history (immediately after state_repo), preserving all prior code_repo
  entries in chronological order.
- generated_at_utc + regeneration_reason: updated to R-92 Commit-C fixup.
- POD audit mirror: /app/frontend/public/audit/ORCH_BOOT.md byte-identically
  synced via shutil.copyfile (no remote calls).

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R92_STATE_HEAD).

Standing bounds: zero push · zero remote · zero network.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R92_STATE_HEAD = "19030610d7e80072cfec498a72180f3304dd4f59"
R92_CODE_HEAD = "ceaa24f41c8156c31e408b47fa8a59b3b265e6ac"
R92_STATE_SEALED_AT = "2026-09-20T23:36:00Z"
R92_CODE_SEALED_AT = "2026-09-20T23:33:00Z"
NEW_UTC = "2026-09-20T23:40:00Z"
NEW_REGEN_REASON = (
    "r92-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-19030610-"
    "cp-g5v5-sfp-1-7-first-slice-commit-b-plus-new-code-repo-history-entry-for-"
    "r92-commit-a-ceaa24f-ruling-5-security-function-policies"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R92_STATE_HEAD}
    sealed_at_utc: {R92_STATE_SEALED_AT}
    seal_kind: "CP-G5V5-SFP-1-7 first slice · Security Function Policies (SFP-1..SFP-7) · state Commit-B `{R92_STATE_HEAD}` · banks Commit-A `{R92_CODE_HEAD}` on programme/track-a · WAVE R-92 · Ruling 5 execution + owner ruling this-session verbatim (2026-09-20T~23:12Z: 'Then open G5-v5 SFP-1..7 first slice per the queue and my prior directives (canon_ref = v5 SRR only, class column bounded hint, rule text governs, measured ratchet above 5688, full SO §6 autonomy). Proceed.') · canon_ref resolves against v5 SRR sheet ONLY sha256 00072c58... · rule text governs · V7 authored from rule text (SRR Enforcement Class empty for all 7 SFP rows per Ruling 3 erratum) · Straight-shot additive slice within Ruling 5 scope · No new stop-conditions · No card edit · New backend package services/security_function_policies/ (net-new · SO §3.8 additive-only) · 7 property invariants SFP-1..SFP-7 · 4 pure-data-in grep-negative scanners registered where rule text explicitly negates a behavior (SFP-1 unanchorable-softening + SFP-2 confidence-score-as-severance-input + SFP-3 partial-acceptance + SFP-5 conformance-as-conviction-ground) · No scanner for SFP-4/SFP-6/SFP-7 per owner directive 'grep-negative bans where the rule text states them' · DELTA +7 MEASURED (5688 → 5695 monotonic-up per CCS2 both fields bumped together · no test flipped to fail · CCS2-aligned across counts.passed/passed_floor/ratchet_history[-1].passed) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 dc89bbdf5d63f96f8b6bc543f4e3809a67df1a7f2bf63d3a47fd2c7b3dfd8c9d IDENTICAL across drill_receipts/20260920T233100Z_run1 (181.30s · 5695 passed) + 20260920T233500Z_run2 (182.62s · 5695 passed) both 5 baseline-fails (3 mirror-drift + 2 v8 cascade all from R-88+ carrying forward · covered by exactly one annotation field under total-coverage guard verified this-slice) 1 skip 438 warnings against post-bump baseline_failures.json sha256 4e7caa47f437b7fe15731bd9f6eb1cbf3f202d3f09b2db495b6c8be668125694 · notes/ORCH_BOOT.md pre-Commit-A ratchet-only regen + byte-identical POD audit mirror sync (both sha256 127e1671e76b0f684c185abedbc52ba6321dce7e97603aec77b888a3f063fa68) · HUNT-first via tools/g5v5_sfp_1_7_hunt.py at phase0/spec_hunt_receipts/20260920T232424Z_g5v5_sfp_1_7_hunt_data.json + human-readable md receipt · sha-pin verified against v5 workbook 00072c58 before any row was read · 7/7 SFP rows found at SRR rows 597-603 · Files (12 tracked at Commit-B): STATE/DECISIONS.md this-append + STATE/NEXT.md this-append + STATE/PINS.md this-append + notes/ORCH_BOOT.md ratchet regen + tools/r92_pre_commit_a_orch_boot_regen.py NEW + tools/g5v5_sfp_1_7_hunt.py NEW + phase0/spec_hunt_receipts/*.json + *.md NEW + phase0/drill_receipts/*.log NEW × 4 · No card edit required for R-92 · R-88+ OWNER-RATIFICATION-PENDING block carries forward unchanged · Total-coverage guard (Guard #1 from R-88+) still GREEN across this slice's double-sweep · R-86 Property tests (Guard #2 from R-88+) still GREEN · Canon anchors verbatim: owner ruling this-session (2026-09-20T~23:12Z) + owner Ruling 5 SRR-as-authority + owner Ruling 3 erratum (class column HINT · rule text governs) + Master Requirements Registry v5 SRR rows 597-603 + R-90 seal 457d947/19bfd333/44d2ae74 (immediately-precedes · CLOSES Ruling-4 scope) + R-89 seal 49e2a338/76c530f0/f2638177 + R-88 seal db90089d/79d5d38d/0cbfc23b + prior seal chain R-85/R-86/R-87 + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + §6 autopilot governance + M16-W3 + CCS2 · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-C fixup this-turn (this-file R-6 regen advances state_repo.head to {R92_STATE_HEAD} + inserts code_repo entry for R92 Commit-A {R92_CODE_HEAD}) → G5-v5 subsequent slices queued → R-91 CP-APP-JS-UNIFY stays at scheduled slot"
"""

NEW_R92_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R92_CODE_HEAD}
    sealed_at_utc: {R92_CODE_SEALED_AT}
    seal_kind: "CP-G5V5-SFP-1-7 first slice · Commit-A `{R92_CODE_HEAD}` · code programme/track-a · WAVE R-92 · Ruling 5 execution · Adds net-new backend package services/security_function_policies/__init__.py + services/security_function_policies/sfp_vocabulary.py + tests/invariants/test_g5v5_sfp_1_7.py · Registers SFP-1..SFP-7 vocabulary as load-bearing Final[...] constants (name + subjects + objects + operations verb tuple + rule text + citation tuple + invariant Final[bool] flags derived from rule text · V7 authored from rule text per Ruling 3 erratum · SRR Enforcement Class column empty for all 7 SFP rows) · 4 pure-data-in grep-negative scanners: scan_for_unanchorable_softening (SFP-1 · 5 patterns · rule text 'refused, not weakened') + scan_for_confidence_score_as_severance_input (SFP-2 · 4 patterns · rule text 'no confidence score, however high, is an eligible input') + scan_for_partial_acceptance (SFP-3 · 5 patterns · rule text 'no partial acceptance') + scan_for_conformance_as_conviction_ground (SFP-5 · 4 patterns · rule text 'never, by itself, grounds for conviction') · No scanner for SFP-4/SFP-6/SFP-7 (rule text asserts invariants without negating specific patterns) · Top-level SFP_RULE_IDS 7-tuple + SFP_RULE_COUNT=7 · 7 property tests · each carries SO §2.5 verbatim-docstring quoting the SRR row's pipe-delimited statement byte-verbatim · each asserts Final[...] annotation + value binding · scanner tests enforce clean-input-empty + each-watched-pattern-hits invariant byte-verbatim · DELTA +7 MEASURED (5688 → 5695 monotonic-up per CCS2 both fields bumped together · new baseline_failures.json sha256 4e7caa47 was 37eaae80 · new ORCH_BOOT.md sha256 127e1671 both notes and POD audit mirror byte-identical) · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · zero implementation module edit outside this-wave · zero sealed contract/writer/test file edit · R-88..R-90 CON-1..31 module + tests + all 7 grep-negative bans continue verbatim GREEN · R-88+ OWNER-RATIFICATION-PENDING block carries forward unchanged · AUTHENTIC RED-first cycle: RED at drill_receipts/20260920T232700Z_g5v5_sfp_1_7_RED_pre.log (7/7 fail right-reason ModuleNotFoundError services.security_function_policies) → GREEN at drill_receipts/20260920T232900Z_g5v5_sfp_1_7_GREEN_post.log (7/7 pass 0.73s) → BASELINE_GUARD=1 double-sweep byte-identical stripped-sha256 dc89bbdf IDENTICAL run1 (5695 passed) + run2 (5695 passed) both 5 baseline-fails 1 skip 438 warnings · pre-Commit-A ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order + byte-identical POD audit-mirror sync (tools/r92_pre_commit_a_orch_boot_regen.py) · Canon anchors verbatim: owner ruling this-session (2026-09-20T~23:12Z) + owner Ruling 5 SRR-as-authority + owner Ruling 3 erratum + Master Requirements Registry v5 SRR rows 597-603 + R-90 seal (immediately-precedes) + prior seal chain R-85/R-86/R-87/R-88/R-89 + SO §2.5/§3/§3.3/§3.8/§3.10-α/§6.2/§6.4/§6.7 + §6 autopilot governance + M16-W3 + CCS2 · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · autopilot next Commit-B state master → Commit-C fixup → G5-v5 subsequent slices queued"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    if f"head: {R92_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-92 Commit-B.")
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
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R92_CODE_REPO_BLOCK + text[m.end():]

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
    print(f"heads_last_sealed.state_repo.head → {R92_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R92_CODE_HEAD}")


if __name__ == "__main__":
    main()
