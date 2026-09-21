"""CP-PROD-DEPLOY-SELF-CONTAINMENT pre-Commit-A: ratchet bump 5857 → 5858 (+1)
+ ORCH_BOOT ratchet-only regen.

CP-PROD-DEPLOY-SELF-CONTAINMENT · code programme/track-a Commit-A adds
NEW mirror-invariant test tests/invariants/test_vendored_tree_mirrors_spine.py
enforcing byte-identity between the sealed sub-tree and the vendored twin
at /app/backend/vendored/extraction_akki/backend/. The vendor sync tool
itself (tools/prod_vendor_sync.py) lives on the state branch, outside the
code repo — so this-Commit-A is a single-file test addition on the code
side.

Owner directive verbatim this-session (2026-09-21T~11:45Z at CP-PROD-DEPLOY
directive):

    "VENDOR the runtime backend into /app/backend so the image is
    self-contained ... Build it with a deterministic sync TOOL (committed,
    receipted) — not a hand copy — so re-syncs at future seals are
    mechanical and drift-testable (a mirror invariant like the pod_shell
    pattern would be in-discipline)."

Delta +1 (5857 → 5858) MEASURED: 1 new test in
`tests/invariants/test_vendored_tree_mirrors_spine.py`
(::test_vendored_tree_byte_identical_mirror_of_spine).

Follows M16-W3 corrected order: ratchet bump + ORCH_BOOT ratchet-only regen
BEFORE Commit-A. Deterministic · idempotent · zero remote · zero network ·
zero subprocess · zero git ops · pure local Path.read_text + Path.write_text
+ shutil.copyfile.
"""
from __future__ import annotations
import hashlib, json, re, shutil
from pathlib import Path

STATE_ROOT = Path("/app/assessment_workspace")
NOTES_ORCH_BOOT = STATE_ROOT / "notes" / "ORCH_BOOT.md"
AUDIT_ORCH_BOOT = Path("/app/frontend/public/audit/ORCH_BOOT.md")
BASELINE_JSON = (
    STATE_ROOT / "repos" / "Extraction-Akki" / "backend" / "tests"
    / "invariants" / "baseline_failures.json"
)

PRIOR = 5857
NEW = 5858
DELTA = 1
NEW_UTC = "2026-09-21T12:00:00Z"

ENTRY = {
    "at_utc": "20260921T120000Z",
    "commit": "PENDING-CP-PROD-DEPLOY-SELF-CONTAINMENT-COMMIT-A",
    "cp": (
        "CP-PROD-DEPLOY-SELF-CONTAINMENT · code programme/track-a Commit-A "
        "adds NEW mirror-invariant test tests/invariants/test_vendored_"
        "tree_mirrors_spine.py enforcing byte-identity between the sealed "
        "runtime sub-tree and the vendored twin at /app/backend/vendored/"
        "extraction_akki/backend/ (owner UNWIND-adjacent CP-PROD-DEPLOY "
        "directive step 8: seal with the usual evidence + the production-"
        "simulation curl matrix)"
    ),
    "note": (
        "CP-PROD-DEPLOY-SELF-CONTAINMENT · owner directive verbatim "
        "this-session (2026-09-21T~11:45Z at CP-PROD-DEPLOY directive): "
        "'THE FAILURE (from rollout logs): backend pod crash-loops at "
        "startup — ModuleNotFoundError: No module named routers at "
        "/app/backend/server.py line 26 ... Root cause to verify: the "
        "production image packages ONLY /app/backend and /app/frontend; "
        "/app/assessment_workspace/** (where the real Extraction-Akki "
        "backend lives and from which the spine bridge sys.path-imports) "
        "does NOT exist in the container. The sandbox works because the "
        "workspace is present; production has no workspace. ... VENDOR "
        "the runtime backend into /app/backend so the image is self-"
        "contained: a committed sync of every package the spine bridge "
        "mounts (routers/, services/, contracts/, plus whatever they "
        "import — trace the closure) into /app/backend ... TWO-PATH "
        "RESOLUTION in /app/backend/server.py: if the live workspace "
        "path exists (sandbox), sys.path the live repo exactly as "
        "today (dev loop unchanged); else fall back to the vendored "
        "tree (production). Resolve paths relative to __file__, never "
        "cwd. No behavior change in the sandbox. ... a mirror invariant "
        "like the pod_shell pattern would be in-discipline.' Cure "
        "summary code-side: (a) NEW tests/invariants/test_vendored_"
        "tree_mirrors_spine.py enforces every runtime file in SPINE_"
        "BACKEND has a byte-identical vendored twin at /app/backend/"
        "vendored/extraction_akki/backend/ — pod_shell FE mirror pattern "
        "precedent · drift on either side flips the test RED before "
        "an image build · DEV-only guard (skips when either tree "
        "absent · production runtime has the vendored tree but not "
        "the spine tree; the dev loop has both so drift is caught). "
        "The mirror-invariant test imports its inclusion policy "
        "directly from tools/prod_vendor_sync.py so the two stay in "
        "lock-step: any change to INCLUDED_TOP_DIRS or INCLUDED_TOP_"
        "PY_FILES or EXCLUDE_* in the sync tool automatically drives "
        "the invariant. AUTHENTIC RED-first cycle: RED at drill_"
        "receipts/20260921T115554Z_cp_prod_deploy_mirror_invariant_"
        "RED_pre.log (1/1 fail right-reason 1-file-byte-diverged-"
        "config/__init__.py after synthetic 1-byte drift injection) "
        "→ GREEN at 20260921T115556Z_cp_prod_deploy_mirror_invariant_"
        "GREEN_post.log (1/1 pass 0.84s after drift restore). "
        "Production simulation curl matrix banked at 20260921T115632Z_"
        "cp_prod_deploy_production_simulation_curl_matrix.log — 14/14 "
        "endpoints operational under AKKI_FORCE_VENDORED=1 (workspace-"
        "masked · vendored-production resolution): 5 R-99 canon-rules "
        "200 + 9 R-100 portal 200/202/404 with seeded JWT + 4 R-100 "
        "portal 401 without JWT + openapi 200 · zero 500 · sealed "
        "spine tree absent from sys.path proves self-containment. "
        "The vendor sync tool tools/prod_vendor_sync.py + the two-"
        "path server.py edit + the vendored tree /app/backend/"
        "vendored/extraction_akki/backend/ + updated requirements.txt "
        "land on the state master branch (assessment_workspace) at "
        "Commit-B this-wave and on /app main at a companion FE-POD-"
        "PROD commit (three-repo discipline: code + state + /app main). "
        "Delta +1 MEASURED (5857 → 5858 · monotonic-up per CCS2 both "
        "fields bumped together · +1 new mirror-invariant test · no "
        "test flipped to fail · no v8 or other spontaneous transitions). "
        "R-100-UNWIND wrapper cure ships in the vendored image (self-"
        "reported §3.8 lapse cured landed at 42a0d3a/bf272c7e/7d7aec5a "
        "on 2026-09-21T11:30Z + Commit-C this-wave-precedes at "
        "7d7aec5a · vendored image built AFTER unwind seal so "
        "production ships the wrapper shape not the lapsed edit). "
        "Sealed R-100-UNWIND wrapper + R-100 portal write surface + "
        "R-99 canon-rules HTTP router + R-96..R-98 canon vocabulary "
        "+ R-88..R-95 seal chain all continue verbatim GREEN. Canon "
        "anchors verbatim: owner CP-PROD-DEPLOY directive this-session "
        "(2026-09-21T~11:45Z) + owner UNWIND directive (2026-09-21T~"
        "11:00Z at self-reported §3.8 lapse cured) + R-100-UNWIND "
        "seal 42a0d3a/bf272c7e/7d7aec5a (immediately-precedes on both "
        "branches) + R-100 seal 39412d09/e6a86c2c/0ae3713f + SO §2.5 "
        "verbatim-docstring + §3 tests-first + §3.3 3-Commit Seal + "
        "§3.8 additive-only + §6.4 NOTHING-BEYOND (scope = mirror "
        "invariant test + vendor sync tool + server.py two-path edit + "
        "vendored tree + requirements.txt closure + drill receipts · "
        "zero sealed edit outside additions) + §6.7 seal-report-"
        "boundary + M16-W3 corrected order. R-91 stays PARKED · "
        "horizon 2026-09-23T03:23:15Z UNCHANGED · current UTC "
        "2026-09-21T~12:00Z < horizon (~39.4h out) · CP-PROD-DEPLOY-"
        "SELF-CONTAINMENT seal completes cleanly inside window with "
        "zero ceremony-apply operations opened. Autopilot next: "
        "Commit-B state master (banks Commit-A + sync tool + vendored "
        "tree via /app main commit + DECISIONS append + ORCH_BOOT "
        "regen + seal report) → Commit-C fixup (R-6 boundary regen "
        "against Commit-B sha + Continuity Bundle regen 3 bundles + "
        "STATE/PINS.md sha256 pins) → HOLD for R-91 horizon (NO "
        "EXPEDITE) → R-91 ε-APPLY at horizon → M1-to-date BUILD_"
        "JOURNAL closure state-only. Standing bounds unchanged: zero "
        "push · zero remote configured on programme/track-a · terminal "
        "pytest only · no testing_agent (STRICTLY BANNED per SO §6) · "
        "additive-only §3.8 · three-repo discipline · ratchet monotonic-"
        "up floor 5858 · HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · "
        "R-25 tagged · Structural §3.8 guard on services/request_"
        "context/context.py sha-pin ad0d9439... (from R-100-UNWIND · "
        "still enforced)."
    ),
    "passed": NEW,
    "delta": DELTA,
    "specialist_dispatch_drift_carried_forward": 3,
}

REGEN_REASON = (
    "cp-prod-deploy-self-containment-pre-commit-a-ratchet-only-regen-"
    "advancing-passed-floor-5857-to-5858-plus-new-baseline-failures-"
    "sha256-under-m16-w3-corrected-order-vendor-runtime-backend-into-"
    "app-backend-for-self-contained-production-image-plus-two-path-"
    "resolution-in-server-py-plus-mirror-invariant-test-per-owner-"
    "cp-prod-deploy-directive-verbatim"
)


def bump_baseline() -> None:
    with BASELINE_JSON.open("r", encoding="utf-8") as fh:
        d = json.load(fh)
    assert d["counts_at_baseline"]["passed"] == PRIOR, (
        f"Prior mismatch: expected {PRIOR}, "
        f"got {d['counts_at_baseline']['passed']}"
    )
    assert d["invariants_enforced_when_baseline_guard_1"]["passed_floor"] == PRIOR
    d["counts_at_baseline"]["passed"] = NEW
    d["invariants_enforced_when_baseline_guard_1"]["passed_floor"] = NEW
    d["ratchet_history"].append(ENTRY)
    d["recorded_at_utc"] = NEW_UTC.replace("-", "").replace(":", "")
    with BASELINE_JSON.open("w", encoding="utf-8") as fh:
        json.dump(d, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def regen_orch_boot() -> str:
    text = NOTES_ORCH_BOOT.read_text(encoding="utf-8")
    sha = hashlib.sha256(BASELINE_JSON.read_bytes()).hexdigest()
    text = re.sub(r"^generated_at_utc:.*$", f"generated_at_utc: {NEW_UTC}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^regeneration_reason:.*$", f"regeneration_reason: {REGEN_REASON}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  passed_floor: \d+$", f"  passed_floor: {NEW}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  counts_at_baseline_passed: \d+$", f"  counts_at_baseline_passed: {NEW}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^  baseline_failures_sha256: [0-9a-f]+$", f"  baseline_failures_sha256: {sha}", text, count=1, flags=re.MULTILINE)
    NOTES_ORCH_BOOT.write_text(text, encoding="utf-8")
    shutil.copyfile(NOTES_ORCH_BOOT, AUDIT_ORCH_BOOT)
    return sha


if __name__ == "__main__":
    bump_baseline()
    sha = regen_orch_boot()
    print(f"baseline_failures.json sha256: {sha}")
    print(f"ratchet passed_floor: {NEW}")
    print(f"delta: +{DELTA}")
