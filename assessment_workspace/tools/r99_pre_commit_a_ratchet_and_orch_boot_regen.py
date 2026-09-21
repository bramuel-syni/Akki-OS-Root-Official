"""R-99 pre-Commit-A: ratchet bump 5822 → 5831 (+9) + ORCH_BOOT ratchet-only regen.

Wave R-99 · COMPLETION SPRINT step 4 of 6 · CP-LIFECYCLE-ENTITLEMENT-HTTP-SURFACE.

Additive-only per SO §3.8: authors a NEW read-only HTTP router
`routers/canon_rules_registry.py` exposing sealed R-96..R-98 canonical rule
vocabularies (DAP-1..38 + RBM-1..23 + ROC-1..11) as `GET /api/canon/rules/*`
endpoints. RBM-8 endpoint surfaces R-91 live-evidence-receipt byte-verbatim
from sealed vocabulary (owner directive 2026-09-21T~06:35Z: "ceremony
windows are rigid, no shortening path exists in code, R-91 window is the
live evidence receipt"). FE surfaces displaying an R-91 ceremony countdown
MUST consume this endpoint verbatim.

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

PRIOR = 5822
NEW = 5831
DELTA = 9
NEW_UTC = "2026-09-21T07:15:00Z"

ENTRY = {
    "at_utc": "20260921T071500Z",
    "commit": "PENDING-CP-LIFECYCLE-ENTITLEMENT-HTTP-SURFACE-COMMIT-A",
    "cp": (
        "CP-LIFECYCLE-ENTITLEMENT-HTTP-SURFACE · WAVE R-99 · additive read-only "
        "HTTP router exposing sealed canon rule vocabularies (DAP-1..38 + "
        "RBM-1..23 + ROC-1..11) · COMPLETION SPRINT step 4 of 6"
    ),
    "note": (
        "R-99 COMPLETION SPRINT step 4 of 6 · additive-only per SO §3.8 · "
        "authors NEW router routers/canon_rules_registry.py mounting under "
        "/api/canon/rules prefix + 5 READ-ONLY GET endpoints: "
        "(1) GET /api/canon/rules/dap materialises 38-rule closed DAP "
        "registry from sealed services.canon_dap_lifecycle.dap_tier_a_"
        "vocabulary + dap_tier_b_vocabulary (Tier A DAP-1..30 + Tier B "
        "DAP-31..38) · (2) GET /api/canon/rules/dap/{rule_id} returns "
        "single rule (404 on unknown ID) · (3) GET /api/canon/rules/rbm "
        "materialises 23-rule RBM registry (Tier A 22 + Tier B 1) · "
        "(4) GET /api/canon/rules/roc materialises 11-rule ROC registry · "
        "(5) GET /api/canon/rules/rbm-8-ceremony-mechanic surfaces R-91 "
        "live-evidence-receipt byte-verbatim: RBM_8_CEREMONY_WINDOW_IS_"
        "RIGID + RBM_8_NO_SHORTENING_PATH_IN_CODE + RBM_8_R91_LIVE_"
        "EVIDENCE_HORIZON_UTC=2026-09-23T03:23:15Z + RBM_8_R91_IS_LIVE_"
        "EVIDENCE_RECEIPT + 5-pattern watched grep-negative tuple + owner "
        "directive verbatim 2026-09-21T~06:35Z. Additive server.py mount "
        "(2 new lines: 1 import + 1 include_router · router carries "
        "prefix=/api/canon/rules) · Adds NEW test module tests/invariants/"
        "test_r99_canon_rules_registry_router_surface.py with 9 tests: "
        "2 router-surface (importable + prefix) + 3 DAP endpoint "
        "(38-rule registry + single-by-id + 404-on-unknown) + 1 RBM "
        "endpoint (23-rule registry) + 1 ROC endpoint (11-rule registry) + "
        "1 RBM-8 ceremony-mechanic endpoint (R-91 live evidence receipt) + "
        "1 OpenAPI discoverability (all 5 paths in /api/openapi.json). "
        "SCOPE FROZEN SO §6.4 NOTHING-BEYOND. zero implementation module "
        "edit outside this-wave. Sealed R-98 canon_rules_service.rbm_roc_"
        "vocabulary + R-97 canon_dap_lifecycle.dap_tier_b_vocabulary + "
        "R-96 dap_tier_a_vocabulary + prior seal chain R-95..R-88 all "
        "continue verbatim GREEN · additive-only per SO §3.8 · router "
        "consumes sealed vocabulary via identity import + closed-vocab "
        "reflection (getattr over Final[...] constants keyed by RULE_IDS "
        "tuples · zero sealed edit). Delta +9 targeted (5822 → 5831 · "
        "monotonic-up per CCS2 both fields bumped together · no test "
        "flipped to fail). CCS2 measured-not-targeted correction applied "
        "pre-double-sweep if a different delta is measured. R-91 stays "
        "PARKED · horizon 2026-09-23T03:23:15Z UNCHANGED · current UTC "
        "2026-09-21T~07:15Z < horizon (~44.1h out) · R-99 seal completes "
        "cleanly inside window with zero ceremony-apply operations "
        "opened. Owner directives verbatim: COMPLETION SPRINT step 4 "
        "(2026-09-21T~06:10Z: 'LIFECYCLE/ENTITLEMENT HTTP SURFACE · "
        "additive routers only') + R-91 NO-EXPEDITE (2026-09-21T~06:15Z: "
        "'the countdown that cannot be shortened is the ceremony ... "
        "waiving it because the sweep already proved green is exactly "
        "the argument every future shortcut would make') + RBM-8 "
        "ceremony directive (2026-09-21T~06:35Z: 'ceremony windows are "
        "rigid, no shortening path exists in code, and the R-91 window "
        "you are currently honoring is the live evidence receipt'). This "
        "wave FE-WIRING-READY: dispatch-ready endpoint list + auth "
        "requirements + sample payloads land in Commit-B seal report."
    ),
    "passed": NEW,
    "delta": DELTA,
    "specialist_dispatch_drift_carried_forward": 3,
}

REGEN_REASON = (
    "r99-pre-commit-a-ratchet-only-regen-cp-lifecycle-entitlement-http-"
    "surface-advancing-passed-floor-5822-to-5831-plus-new-baseline-"
    "failures-sha256-under-m16-w3-corrected-order-additive-router-"
    "canon-rules-registry-exposing-sealed-dap-rbm-roc-plus-rbm-8-"
    "ceremony-mechanic-endpoint-r91-live-evidence-receipt-completion-"
    "sprint-step-4-of-6"
)


def bump_baseline() -> None:
    with BASELINE_JSON.open("r", encoding="utf-8") as fh:
        d = json.load(fh)
    assert d["counts_at_baseline"]["passed"] == PRIOR, f"Prior mismatch: expected {PRIOR}, got {d['counts_at_baseline']['passed']}"
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
