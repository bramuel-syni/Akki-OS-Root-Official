"""R-99 Commit-C fixup: ORCH_BOOT R-6 boundary regen (heads_last_sealed advance).

Mirrors tools/r98_commit_c_fixup_orch_boot_regen.py precedent exactly.

- state_repo (heads_last_sealed.state_repo): replaced with R-99 Commit-B
  `58685080caafe967111ea1af6e3f665e1b5518c5` entry (was R-98 Commit-B
  `deff9e58d0380d8052cd60785dd6766e6a9a2326`).
- code_repo history: fresh entry for R-99 Commit-A
  `eb40fb67ea83c18cb35f51956b3b4b19c07ecbed` INSERTED at the top of the
  history (immediately after state_repo), preserving all prior code_repo
  entries in chronological order (R-98 Commit-A `38eeef6c4844c56e91900a83355c140f76733148`
  remains as the next-most-recent entry).
- generated_at_utc + regeneration_reason: updated to R-99 Commit-C fixup.

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals R99_STATE_HEAD).

Standing bounds: zero push · zero remote · zero network.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

R99_STATE_HEAD = "58685080caafe967111ea1af6e3f665e1b5518c5"
R99_CODE_HEAD = "eb40fb67ea83c18cb35f51956b3b4b19c07ecbed"
R99_STATE_SEALED_AT = "2026-09-21T07:37:00Z"
R99_CODE_SEALED_AT = "2026-09-21T07:33:35Z"
NEW_UTC = "2026-09-21T07:40:00Z"
NEW_REGEN_REASON = (
    "r99-commit-c-fixup-r6-boundary-regen-advancing-state-repo-head-to-"
    "58685080-cp-lifecycle-entitlement-http-surface-commit-b-plus-new-"
    "code-repo-history-entry-for-r99-commit-a-eb40fb67-additive-read-only-"
    "router-canon-rules-registry-exposing-sealed-r-96-to-r-98-canon-"
    "vocabularies-dap-1-to-38-plus-rbm-1-to-23-plus-roc-1-to-11-plus-"
    "rbm-8-ceremony-mechanic-r-91-live-evidence-receipt-completion-"
    "sprint-step-4-of-6"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {R99_STATE_HEAD}
    sealed_at_utc: {R99_STATE_SEALED_AT}
    seal_kind: "R-99 CP-LIFECYCLE-ENTITLEMENT-HTTP-SURFACE · state Commit-B `{R99_STATE_HEAD}` · banks Commit-A `{R99_CODE_HEAD}` on programme/track-a · WAVE R-99 · additive READ-ONLY canon-rules HTTP router surface · COMPLETION SPRINT step 4 of 6 (2026-09-21T~06:10Z verbatim: 'LIFECYCLE/ENTITLEMENT HTTP SURFACE · additive routers only') + user step-4-a directive verbatim (2026-09-21T~07:10Z: 'flag FE-WIRING-READY immediately with the dispatch-ready endpoint list + auth + sample payloads — I send the FE specialist to wire the portal write-path screens against the live surface while you continue') + user R-91 HOLD-AND-PROCEED directive (2026-09-21T~07:10Z: 'never skip the ceremony') · pre-Commit-A ratchet 5822 → 5831 + notes/ORCH_BOOT.md ratchet-only regen per M16-W3 corrected order + tools/r99_pre_commit_a_ratchet_and_orch_boot_regen.py + STATE hygiene fixes (M12b_W1.md pin recomputed 0bc8b267→f3aedc9e · ENTITLEMENT.md pin recomputed 46f4a6e7→a214881e · NEXT.md POINTER_LINE appended at tail restoring test_next_carries_pointer_near_bottom invariant) + phase0/spec_hunt_receipts/20260921T073500Z_r99_canon_rules_registry_seal_report.md NEW with FE-WIRING-READY handoff artifact (endpoint list · auth · sample payloads verbatim from live sweep run1 · FE consumption invariant SO §6.6). FE-WIRING-READY flag RAISED at this Commit-B for FE specialist dispatch. R-99 seal completes cleanly inside R-91 window with zero ceremony-apply operations opened (current UTC 2026-09-21T~07:35Z < horizon 2026-09-23T03:23:15Z · ~43.6h out). Autopilot next Commit-C fixup this-turn advances state_head + inserts code_repo entry for R-99 Commit-A eb40fb67 → per user's corrected sequence: (a) FE-WIRING-READY dispatch → (b) OPEN-CARD SWEEP fad511a7 already banked on master (verified from git log) → (c) residual G5 Tier B / consolidated owner-list scan → (d) R-91 ε-apply at first boundary after horizon → (e) M1-to-date BUILD_JOURNAL closure state-only as final act (COMPLETION SPRINT step 6)."
"""

NEW_R99_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {R99_CODE_HEAD}
    sealed_at_utc: {R99_CODE_SEALED_AT}
    seal_kind: "R-99 CP-LIFECYCLE-ENTITLEMENT-HTTP-SURFACE · Commit-A `{R99_CODE_HEAD}` · code programme/track-a · WAVE R-99 · additive READ-ONLY router exposing sealed R-96..R-98 canon rule vocabularies (DAP-1..38 + RBM-1..23 + ROC-1..11) as GET /api/canon/rules/{{dap,dap/{{rule_id}},rbm,roc,rbm-8-ceremony-mechanic}} · COMPLETION SPRINT step 4 of 6 · Adds NEW backend router routers/canon_rules_registry.py (197 lines · APIRouter prefix=/api/canon/rules · 5 GET endpoints · closed-vocab reflection over sealed Final[...] constants via identity import · zero sealed edit) + NEW test tests/invariants/test_r99_canon_rules_registry_router_surface.py (180 lines · 9 tests: 2 router-surface + 3 DAP + 1 RBM + 1 ROC + 1 RBM-8 ceremony-mechanic + 1 OpenAPI discoverability · SO §2.5 verbatim-docstring) + additive server.py mount (4 lines · 1 comment + 1 import + 1 blank + 1 include_router) + additive backend/tests/invariants/known_unwired.py 1 new entry keyed routers.canon_rules_registry with Doc04/Doc05/Doc12 SRR canon citations + FE-WIRING-READY remediation R-tag + baseline_failures.json ratchet 5822 → 5831 both fields + new ratchet_history entry documenting this-wave · DELTA +9 MEASURED (targeted equalled measured · no CCS2 correction needed) · new baseline_failures.json sha256 070c57c4cf8618554a7857f8e14a0e2555ae4d8593df6953b1693080c3e8361f was df3325f7bc82f49060ed097ce0755bb4c3ed3aa46147ea799a14e293a96674cd · new ORCH_BOOT.md sha256 1bbdb2de1506de23d1f5887828e950460d1cb9a6cd267d98097170f71cf127e9 both notes and POD audit mirror byte-identical · SCOPE FROZEN SO §6.4 NOTHING-BEYOND · zero implementation module edit outside this-wave · Sealed R-98 canon_rules_service.rbm_roc_vocabulary + R-97 canon_dap_lifecycle.dap_tier_b_vocabulary + R-96 dap_tier_a_vocabulary + R-95..R-88 seal chain all continue verbatim GREEN · additive-only per SO §3.8 · AUTHENTIC RED-first: initial RED at drill_receipts/20260921T072500Z_r99_canon_rules_registry_RED_pre.log (test_r99_openapi_json_lists_canon_rules_paths 1/9 fail right-reason 404 from /openapi.json before path corrected to /api/openapi.json per FastAPI openapi_url configuration server.py:52) → GREEN at 20260921T071500Z_r99_canon_rules_registry_GREEN_post.log (10/10 pass 0.84s incl test_orch_boot) → deterministic BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep byte-identical canonicalised-sha256 0eac2d7684e21020fe5bc351759cf282b981896fc6c7eaf9525e76cadb6e885a IDENTICAL run1 (5831 passed · 184.65s · 3 baseline-fails · 1 skip · 438 warnings) + run2 (5831 passed · 185.01s · same) both against post-bump baseline_failures.json sha256 070c57c4 · CCS2 invariant surface matches exactly across both deterministic-seed sweeps · CCS2 lesson extension: strip_baseline_guard_log.py does not currently strip shell-appended RUN[12]_EXIT= marker lines · this-wave canonicalises via inline post-strip filter · extension deferred to hygiene wave · RBM-8 ceremony-mechanic invariants encoded at R-98 Commit-A 38eeef6c NOW SURFACED byte-verbatim at /api/canon/rules/rbm-8-ceremony-mechanic HTTP endpoint (FE portal write-path R-91-countdown surface must consume byte-verbatim per SO §6.6) · FE-WIRING-READY flag raised via Commit-B seal report handoff artifact · Canon anchors verbatim: COMPLETION SPRINT step 4 + user step-4-a FE-WIRING-READY + user R-91 HOLD-AND-PROCEED + owner R-91 NO-EXPEDITE (RBM-8/SER C.5 I-4) + owner RBM-8 ceremony directive + owner Ruling 5 SRR-as-authority + owner Ruling 3 erratum + Master Requirements Registry v5 SRR sheet · R-98 seal chain (38eeef6c/deff9e58/35e2fda7 + a6be791) + R-97/R-96 Family C seals + R-95..R-88 seal chain + OPEN-CARD SWEEP state-only commit fad511a7 · SO §2.5/§3/§3.3/§3.8/§3.10-α/§6/§6.2/§6.4/§6.6/§6.7 · M16-W3 corrected order · CCS2 lesson extended this-wave · Autopilot next: Commit-B state master (banks this-Commit-A + regen tool + STATE hygiene fixes + seal report) → Commit-C fixup (this-turn advances state_head + inserts code_repo entry) → FE-WIRING-READY dispatch → residual scan → R-91 ε-apply at horizon → M1-to-date BUILD_JOURNAL closure"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    if f"head: {R99_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at R-99 Commit-B.")
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
        text = text[: m.start()] + NEW_STATE_REPO_BLOCK + NEW_R99_CODE_REPO_BLOCK + text[m.end():]

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
    print(f"heads_last_sealed.state_repo.head → {R99_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {R99_CODE_HEAD}")


if __name__ == "__main__":
    main()
