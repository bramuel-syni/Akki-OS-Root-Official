"""R-98 Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Mirrors tools/r95_commit_c_fixup_orch_boot_regen.py precedent exactly.

- state_repo (heads_last_sealed.state_repo): replaced with R-98 Commit-B
  `deff9e58d0380d8052cd60785dd6766e6a9a2326` entry (was R-97 Commit-B
  `d233975da6ec82cab8d5a116fedb99025176c15c`).
- code_repo history: fresh entry for R-98 Commit-A
  `38eeef6c4844c56e91900a83355c140f76733148` INSERTED at the top of the
  history (immediately after state_repo), preserving all prior code_repo
  entries in chronological order (R-97 Commit-A `c98fe5c5` remains as the
  next-most-recent entry).
- generated_at_utc + regeneration_reason: updated to R-98 Commit-C fixup.

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R98_STATE_HEAD).

Standing bounds: zero push · zero remote · zero network.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R98_STATE_HEAD = "deff9e58d0380d8052cd60785dd6766e6a9a2326"
R98_CODE_HEAD = "38eeef6c4844c56e91900a83355c140f76733148"
R98_STATE_SEALED_AT = "2026-09-21T07:10:00Z"
R98_CODE_SEALED_AT = "2026-09-21T07:08:00Z"
NEW_UTC = "2026-09-21T07:15:00Z"
NEW_REGEN_REASON = (
    "r98-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-"
    "deff9e58-cp-g5v5-family-d-rbm-roc-commit-b-plus-new-code-repo-history-"
    "entry-for-r98-commit-a-38eeef6c-ruling-5-family-d-rbm-1-to-22-tier-a-"
    "rulebook-engine-spec-v1-rbm-23-tier-b-watch-learning-v1-roc-1-to-11-"
    "tier-a-rule-criteria-spec-v1-plus-rbm-8-ceremony-mechanic-invariants"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R98_STATE_HEAD}
    sealed_at_utc: {R98_STATE_SEALED_AT}
    seal_kind: "R-98 CP-G5V5-FAMILY-D-RBM-ROC · state Commit-B `{R98_STATE_HEAD}` · banks Commit-A `{R98_CODE_HEAD}` on programme/track-a · WAVE R-98 · Family D · RBM-1..23 + ROC-1..11 Rules Service · 34 rules · 40 tests · Ruling 5 · under COMPLETION SPRINT DIRECTIVE step 2 of 6 (2026-09-21T~06:10Z) + R-91 NO-EXPEDITE (2026-09-21T~06:15Z: horizon 2026-09-23T03:23:15Z UNCHANGED · RBM-8/SER C.5 I-4 Family D cross-refs) + owner this-session RBM-8 ceremony directive (2026-09-21T~06:35Z: 'ceremony windows are rigid, no shortening path exists in code, R-91 window is the live evidence receipt') · RBM Tier A rows 288..309 promise=rulebook_engine_spec_v1 domain=Rules Service · RBM Tier B row 483 promise=watch_learning_v1 domain=O2 Security & Intent · ROC Tier A rows 277..287 promise=rule_criteria_spec_v1 domain=Rules Service PROPOSED (pending ratification) · RBM-8 authored to encode ceremony-mechanic invariants (RBM_8_CEREMONY_WINDOW_IS_RIGID + RBM_8_NO_SHORTENING_PATH_IN_CODE + RBM_8_R91_LIVE_EVIDENCE_HORIZON_UTC=2026-09-23T03:23:15Z + RBM_8_R91_IS_LIVE_EVIDENCE_RECEIPT) + scan_for_ceremony_shortening_path 5-pattern grep-negative scanner · Delta +40 measured · ratchet 5782 → 5822 · baseline sha df3325f7 · deterministic double-green stripped-sha256 33d59d5a IDENTICAL · Family D CLOSED at this Commit-A · autopilot next Commit-C fixup this-turn → COMPLETION SPRINT step 3 OPEN-CARD SWEEP → step 4 LIFECYCLE/ENTITLEMENT HTTP SURFACE → step 5 R-91 ε-APPLY at horizon → step 6 FINAL CLOSURE REPORT"
"""

NEW_R98_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R98_CODE_HEAD}
    sealed_at_utc: {R98_CODE_SEALED_AT}
    seal_kind: "R-98 CP-G5V5-FAMILY-D-RBM-ROC · Commit-A `{R98_CODE_HEAD}` · code programme/track-a · WAVE R-98 · Family D · RBM-1..23 + ROC-1..11 Rules Service · Adds NEW backend package services/canon_rules_service/__init__.py + services/canon_rules_service/rbm_roc_vocabulary.py registering 34 Final[...] {{ID}}_STATEMENT + {{ID}}_SRR_ROW pairs byte-verbatim (RBM Tier A 22 rows 288..309 promise=rulebook_engine_spec_v1 domain=Rules Service + RBM Tier B 1 row 483 promise=watch_learning_v1 domain=O2 Security & Intent + ROC Tier A 11 rows 277..287 promise=rule_criteria_spec_v1 domain=Rules Service PROPOSED (pending ratification)) + RBM_RULE_IDS 23-tuple + RBM_TIER_A/B splits + ROC_RULE_IDS 11-tuple + registry metadata dicts + ROC-7 status axis 5-tuple + ROC-8 enforcement-class axis 5-tuple + RBM-8 CEREMONY MECHANIC invariants (owner-cited): RBM_8_IS_R91_CEREMONY_ANCHOR + RBM_8_CEREMONY_WINDOW_IS_RIGID + RBM_8_NO_SHORTENING_PATH_IN_CODE + RBM_8_R91_LIVE_EVIDENCE_HORIZON_UTC=`2026-09-23T03:23:15Z` + RBM_8_R91_IS_LIVE_EVIDENCE_RECEIPT + RBM_8_CEREMONY_SHORTENING_WATCHED_PATTERNS 5-tuple + scan_for_ceremony_shortening_path pure-data-in grep-negative scanner (5 patterns: shorten_ceremony_countdown/expedite_ceremony_apply/waive_ceremony_countdown/bypass_ceremony_horizon/fast_forward_ceremony) · Adds NEW test tests/invariants/test_g5v5_family_d_rbm_roc.py 40 tests (4 registry-shape + 22 RBM Tier A + 1 RBM Tier B + 11 ROC Tier A + 1 extended RBM-8 ceremony-mechanic + 2 RBM-8 scanner) · SO §2.5 verbatim-docstring · SRR-status=PROPOSED preserved verbatim · DELTA +40 MEASURED · targeted equalled measured · Sealed R-97 canon_dap_lifecycle.dap_tier_b_vocabulary + R-96 dap_tier_a_vocabulary + R-95..R-88 seal chain all continue verbatim GREEN · additive-only per SO §3.8 · AUTHENTIC RED-first: RED at drill_receipts/20260921T064000Z_r98_family_d_rbm_roc_RED_pre.log (3/40 fail right-reason AttributeError on RBM_8_CEREMONY_WINDOW_IS_RIGID + scan_for_ceremony_shortening_path + RBM_8_CEREMONY_SHORTENING_WATCHED_PATTERNS · 37/40 pass since base 34-rule vocabulary was scaffolded pre-owner-directive · RED window authentic for incremental owner-directive symbols) → GREEN at 20260921T064500Z_r98_family_d_rbm_roc_GREEN_post.log (40/40 pass 0.78s) → deterministic BASELINE_GUARD=1 double-sweep byte-identical stripped-sha256 33d59d5a IDENTICAL run1 (5822 passed · 184.28s) + run2 (5822 passed · 184.94s) both PYTHONHASHSEED=0 · both 3 baseline-fails (pod_shell mirror-drift ×3 from R-88+ carrying forward) 1 skip 438 warnings · new baseline_failures.json sha256 df3325f7 was a2a28fcf · new ORCH_BOOT.md sha256 15982ed8 both notes and POD audit mirror byte-identical · Canon anchors verbatim: owner COMPLETION SPRINT (2026-09-21T~06:10Z six-step directive) + owner R-91 NO-EXPEDITE (2026-09-21T~06:15Z RBM-8/SER C.5 I-4 citations) + owner this-session RBM-8 ceremony directive (2026-09-21T~06:35Z ceremony-window-rigid) + owner G5-v5 sequencing (2026-09-21T~01:00Z at a30db4f7) + owner Ruling 5 SRR-as-authority + owner Ruling 3 erratum + Master Requirements Registry v5 SRR rows 277..287 + 288..309 + 483 · R-97 seal (immediately-precedes · Family C fully closed) · prior seal chain R-96/R-95/R-94/R-93/R-92/R-91/R-90/R-89/R-88/R-87/R-86/R-85 · SO §2.5/§3/§3.3/§3.8/§3.10-α/§6/§6.4/§6.6/§6.7 · M16-W3 corrected order · CCS2 lesson (with hash-seed determinism · PYTHONHASHSEED=0 required) · Autopilot next: Commit-B state master → Commit-C fixup (this-turn advances state_head + inserts code_repo entry) → COMPLETION SPRINT step 3 OPEN-CARD SWEEP → step 4 LIFECYCLE/ENTITLEMENT HTTP SURFACE additive routers → step 5 R-91 ε-APPLY at horizon → step 6 FINAL CLOSURE REPORT"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    if f"head: {R98_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-98 Commit-B.")
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
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R98_CODE_REPO_BLOCK + text[m.end():]

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
    print(f"heads_last_sealed.state_repo.head → {R98_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R98_CODE_HEAD}")


if __name__ == "__main__":
    main()
