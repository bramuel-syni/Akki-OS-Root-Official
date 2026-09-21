"""CP-PROD-DEPLOY-SELF-CONTAINMENT Commit-C fixup: ORCH_BOOT R-6 boundary regen.

Advances heads_last_sealed.state_repo.head from R-100-UNWIND Commit-B
`bf272c7ebe1c19545c9900fae8d41ff4d948bb53` to CP-PROD-DEPLOY Commit-B
`24661fedd61647c5e0a41fdce7389f56477243b2`.

Inserts NEW code_repo entry for CP-PROD-DEPLOY Commit-A
`283524d89dd337d79014b114d575ced7baab6dfc` at the top of the code_repo
history (preserving all prior entries).

Additive-only per SO §3.8 · deterministic · idempotent (skips re-application
if state_repo.head already equals CP_PROD_DEPLOY_STATE_HEAD).
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")

CPD_STATE_HEAD = "24661fedd61647c5e0a41fdce7389f56477243b2"
CPD_CODE_HEAD = "283524d89dd337d79014b114d575ced7baab6dfc"
CPD_APP_MAIN_HEAD = "25790c2c4ad82805c89d6ee17af12c220c5961f5"
CPD_STATE_SEALED_AT = "2026-09-21T12:20:00Z"
CPD_CODE_SEALED_AT = "2026-09-21T12:12:00Z"
CPD_APP_MAIN_SEALED_AT = "2026-09-21T12:13:00Z"
NEW_UTC = "2026-09-21T12:25:00Z"
NEW_REGEN_REASON = (
    "cp-prod-deploy-self-containment-commit-c-fixup-r6-boundary-regen-"
    "advancing-state-repo-head-to-24661fed-plus-new-code-repo-history-"
    "entry-for-cp-prod-deploy-commit-a-283524d8-plus-companion-app-main-"
    "commit-25790c2c-two-path-server-py-plus-vendored-tree-plus-"
    "requirements-closure-plus-mirror-invariant-test-per-owner-cp-prod-"
    "deploy-directive-verbatim-2026-09-21-11-45z-owner-explicit-"
    "authorization-during-r91-hold"
)


NEW_STATE_REPO_BLOCK = f"""heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: {CPD_STATE_HEAD}
    sealed_at_utc: {CPD_STATE_SEALED_AT}
    seal_kind: "CP-PROD-DEPLOY-SELF-CONTAINMENT · state Commit-B `{CPD_STATE_HEAD}` · banks Commit-A `{CPD_CODE_HEAD}` on programme/track-a + companion /app main commit `{CPD_APP_MAIN_HEAD}` landing two-path server.py + vendored tree + requirements closure · owner-directed production K8s deployment fix per owner directive verbatim this-session (2026-09-21T~11:45Z at CP-PROD-DEPLOY directive): 'NEW OWNER-PRIORITY WAVE — PRODUCTION DEPLOYMENT FIX. The owner attempted an Emergent production deploy (Kubernetes, containerized) and it failed. This work is authorized NOW during the R-91 hold (the hold bars the ε-apply, not owner-ordered work). R-91 still applies only at the horizon. THE FAILURE (from rollout logs): backend pod crash-loops at startup — ModuleNotFoundError: No module named routers at /app/backend/server.py line 26 (from routers import connect_gpu as connect_gpu_router). Root cause to verify: the production image packages ONLY /app/backend and /app/frontend; /app/assessment_workspace/** (where the real Extraction-Akki backend lives and from which the spine bridge sys.path-imports) does NOT exist in the container. The sandbox works because the workspace is present; production has no workspace. ... VENDOR the runtime backend into /app/backend so the image is self-contained: a committed sync of every package the spine bridge mounts (routers/, services/, contracts/, plus whatever they import — trace the closure) into /app/backend ... TWO-PATH RESOLUTION in /app/backend/server.py: if the live workspace path exists (sandbox), sys.path the live repo exactly as today (dev loop unchanged); else fall back to the vendored tree (production). Resolve paths relative to __file__, never cwd. No behavior change in the sandbox. ... a mirror invariant like the pod_shell pattern would be in-discipline.' R-100-UNWIND wrapper cure (self-reported §3.8 lapse cured at code 42a0d3a/state Commit-B bf272c7e/state Commit-C 7d7aec5a landed 2026-09-21T11:30-11:47Z) PRECEDES this-wave so vendored image ships wrapper shape (services/enforce/principal_context_adapter.py owning with-block protocol; sealed services/request_context/context.py restored byte-identical to Commit 4b3b5e0 sha256 ad0d9439...) not the lapsed edit. Cure summary: three-repo landing. Code programme/track-a Commit-A 283524d8: NEW backend/tests/invariants/test_vendored_tree_mirrors_spine.py enforcing byte-identity between sealed runtime sub-tree and vendored twin (imports inclusion policy from tools/prod_vendor_sync.py so single source of truth · pod_shell FE mirror precedent · DEV-only guard) + pod_shell/backend/server.py mirror sync of the two-path edit + backend/tests/invariants/baseline_failures.json ratchet 5857→5858 (+1 MEASURED). Production-image /app main commit 25790c2c: backend/server.py two-path spine bridge (SPINE_BACKEND if /app/assessment_workspace present else VENDORED_BACKEND fallback under ROOT_DIR/vendored/extraction_akki/backend · AKKI_FORCE_VENDORED=1 forces vendored branch for local prod simulation · fail loud RuntimeError if neither present · paths relative to __file__ never cwd) + Tigris env-discipline (WARN log line at import if _is_production_env=True and TIGRIS_* envs unset · no silent misconfig · MongoDB unchanged env-only fail-loud on missing MONGO_URL/DB_NAME) + backend/requirements.txt closure updates (httpx>=0.27.2 + openpyxl>=3.1.5 + Pillow>=10.0.0 generated from imports across routers/wizard_operator + services/service_1/webhook + services/synisense/shield/egress_firewall + services/rules_service + services/layer_a + services/data_source/synthetic_asset_gen) + backend/vendored/extraction_akki/backend/** 999-file byte-identical mirror (services/routers/contracts/data/config/drills/scripts/estate_keys + __init__.py/core.py · excluding tests/phase0/tools/__pycache__/*.pyc/tier_lock.v*.json runtime state) + backend/vendored/extraction_akki/MANIFEST.json (per-file sha256 + structural_sha256 379318b9f4e5e297fa7c7b90b5fa9e8244cf2e00f4b0cc81d94e6a016d9a14e8 + file_count 999). State master Commit-B this-repo: NEW tools/prod_vendor_sync.py deterministic sync tool + NEW tools/cp_prod_deploy_pre_commit_a_ratchet_and_orch_boot_regen.py + notes/ORCH_BOOT.md ratchet-only regen pre-Commit-A + STATE/DECISIONS.md append + phase0/spec_hunt_receipts/20260921T120000Z_cp_prod_deploy_seal_report.md consolidated seal report. Production simulation curl matrix at drill_receipts/20260921T115632Z: 14/14 endpoints operational under AKKI_FORCE_VENDORED=1 vendored-production resolution (5 R-99 canon-rules public 200 + 9 R-100 portal 200/202/404 with seeded JWT + 4 R-100 portal 401 without JWT + openapi 200 · zero 500 · sealed spine tree absent from sys.path proves self-containment). Deterministic BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep byte-identical stripped-sha256 23caeeb5ff3f71f6f5a3eeec8d117e0413d82c39fb03ad5918c05fc31853581a IDENTICAL across run1v3 (181.00s 5858 passed) + run2 (181.04s 5858 passed) · both 3 R-91-pending baseline-fails 1 skip 438 warnings against post-bump baseline_failures.json sha256 5266564f. Standing lesson banked: environment-differential deployment failures are structurally preventable via vendored-mirror + two-path bridge pattern. R-91 stays PARKED horizon 2026-09-23T03:23:15Z UNCHANGED · current UTC 2026-09-21T~12:20Z < horizon (~39.1h out) · CP-PROD-DEPLOY-SELF-CONTAINMENT seal completes cleanly inside window with zero ceremony-apply operations opened per owner explicit authorisation this-directive verbatim. Autopilot next Commit-C fixup this-turn advances state_head + inserts code_repo entries for 283524d8 code + 25790c2c app-main + executes Continuity Bundle regen (3 bundles) + STATE/PINS.md sha256 pins block → HOLD for R-91 horizon (NO EXPEDITE) → R-91 ε-APPLY at horizon → M1-to-date BUILD_JOURNAL closure state-only."
"""

NEW_CPD_CODE_REPO_BLOCK = f"""  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: {CPD_CODE_HEAD}
    sealed_at_utc: {CPD_CODE_SEALED_AT}
    seal_kind: "CP-PROD-DEPLOY-SELF-CONTAINMENT · Commit-A `{CPD_CODE_HEAD}` · code programme/track-a · WAVE CP-PROD-DEPLOY · owner directive verbatim this-session (2026-09-21T~11:45Z at CP-PROD-DEPLOY directive): production K8s image crash-loops at startup with ModuleNotFoundError No module named routers because the production image packages only /app/backend + /app/frontend and the sealed backend at /app/assessment_workspace/repos/Extraction-Akki/backend/ is absent · this-Commit-A code-side landing: NEW backend/tests/invariants/test_vendored_tree_mirrors_spine.py mirror-invariant test enforcing byte-identity between the sealed runtime sub-tree and the vendored twin at /app/backend/vendored/extraction_akki/backend/ (imports its inclusion policy directly from tools/prod_vendor_sync.py so single source of truth · pod_shell FE mirror precedent · DEV-only guard skipping when either tree absent · drift on either side flips test RED before an image build) + pod_shell/backend/server.py mirror sync of the two-path edit landing on /app main this-wave (companion commit 25790c2c) + backend/tests/invariants/baseline_failures.json ratchet 5857→5858 (+1 MEASURED · one new mirror-invariant test · zero test flipped to fail · no v8 or spontaneous transitions · new sha256 5266564fdfa09d6977b1684293864ef361754444cfb6178f4e3fdb1b5e6117cb) · AUTHENTIC RED-first cycle drill_receipts/20260921T115554Z_cp_prod_deploy_mirror_invariant_RED_pre.log (1/1 fail right-reason synthetic 1-byte drift on config/__init__.py) → GREEN drill_receipts/20260921T115556Z_cp_prod_deploy_mirror_invariant_GREEN_post.log (1/1 pass 0.84s post-drift-restore) → live production-simulation curl matrix drill_receipts/20260921T115632Z (14/14 endpoints operational under AKKI_FORCE_VENDORED=1 · 5 R-99 canon-rules public 200 + 9 R-100 portal 200/202/404 with seeded JWT + 4 R-100 portal 401 without JWT + openapi 200 · zero 500 · sealed spine tree absent from sys.path proves self-containment) → deterministic BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep byte-identical stripped-sha256 23caeeb5ff3f71f6f5a3eeec8d117e0413d82c39fb03ad5918c05fc31853581a IDENTICAL across drill_receipts/20260921T121132Z_run1v3 (181.00s 5858 passed) + 20260921T121507Z_run2 (181.04s 5858 passed) both 3 R-91-pending baseline-fails 1 skip 438 warnings · SCOPE FROZEN SO §6.4 NOTHING-BEYOND (1 new test file + 1 ratchet bump + 1 pod_shell mirror sync + 5 drill receipts · zero implementation module edit outside this-wave · zero sealed test file edit) · Sealed R-100-UNWIND 42a0d3a/bf272c7e/7d7aec5a wrapper cure PRECEDES this wave and ships in the vendored image so production ships the wrapper shape not the lapsed edit · sealed R-100 portal write surface + R-99 canon-rules HTTP router + R-96..R-98 canon vocabulary + R-88..R-95 seal chain all continue verbatim GREEN · additive-only per SO §3.8 · Canon anchors verbatim: owner CP-PROD-DEPLOY directive this-session (2026-09-21T~11:45Z) + owner UNWIND directive (2026-09-21T~11:00Z at self-reported §3.8 lapse cured) + R-100-UNWIND seal 42a0d3a/bf272c7e/7d7aec5a (immediately-precedes on programme/track-a + master) + R-100 seal 39412d09/e6a86c2c/0ae3713f + SO §2.5/§3/§3.3/§3.8 additive-only/§6.4 NOTHING-BEYOND/§6.7 seal-report-boundary + M16-W3 corrected order · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered · Autopilot next: Commit-B state master (banks this-Commit-A + companion app-main commit + sync tool + seal report + DECISIONS append + ORCH_BOOT regen) → Commit-C fixup (this-turn advances state_head + inserts code_repo entries + Continuity Bundle regen 3 bundles + STATE/PINS.md sha256 pins) → HOLD for R-91 horizon (NO EXPEDITE) → R-91 ε-APPLY at 2026-09-23T03:23:15Z → M1-to-date BUILD_JOURNAL closure state-only"
"""


def regen_orch_boot_commit_c() -> None:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    if f"head: {CPD_STATE_HEAD}" in text:
        print("Idempotent skip: state_repo.head already at CP-PROD-DEPLOY Commit-B.")
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
            + NEW_CPD_CODE_REPO_BLOCK
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
    print(f"heads_last_sealed.state_repo.head → {CPD_STATE_HEAD}")
    print(f"heads_last_sealed.code_repo (newest) → {CPD_CODE_HEAD}")


if __name__ == "__main__":
    main()
