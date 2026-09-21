"""R-100-UNWIND pre-Commit-A: ratchet bump 5852 → 5857 (+5) + ORCH_BOOT regen.

R-100-UNWIND · self-reported §3.8 lapse cured · authors NEW wrapper
`services/enforce/principal_context_adapter.py` owning the `with ...:`
context-manager protocol, restores `services/request_context/context.py`
byte-identical to its authored form at Commit 4b3b5e0 (sha256
ad0d94399af44bd5f6fa57f9aa1371ede7ca526789e47db10b45dddc79c39cfb), and
re-points the R-100 portal routers (portal_requests.py + portal_entitlement.py)
to import `principal_context` from the wrapper.

Owner ruling this-session verbatim (2026-09-21T~11:00Z at the UNWIND directive):

    "Modifying the sealed PrincipalRequestContext class in
    services/request_context/context.py to add __enter__/__exit__ is
    an edit to a sealed class — SO §3.8 forbids it. Unwind to a wrapper:
    revert context.py byte-identically to its sealed state, author a
    context-manager adapter inside services/enforce/ that owns the
    protocol, re-point the R-100 portal routers to the wrapper, seal
    as a self-reported §3.8 lapse cured, regenerate the three continuity
    bundles, pin their sha256s in STATE/PINS.md, then hold at the R-91
    horizon (no expedite)."

Delta +5 (5852 → 5857) MEASURED: 5 new tests in
`tests/invariants/test_principal_context_adapter.py`:
  1. test_principal_context_adapter_module_importable
  2. test_principal_context_wrapper_enters_and_yields_request_context
  3. test_principal_context_wrapper_exit_clears_propagation
  4. test_principal_context_wrapper_exception_propagates_and_clears
  5. test_context_py_sealed_bytes_sha256_pinned (SO §3.8 structural
     guard · sha-pin of the sealed file · makes the specific §3.8
     lapse structurally non-repeatable on this file)

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

PRIOR = 5852
NEW = 5857
DELTA = 5
NEW_UTC = "2026-09-21T11:30:00Z"

ENTRY = {
    "at_utc": "20260921T113000Z",
    "commit": "PENDING-CP-R100-UNWIND-COMMIT-A",
    "cp": (
        "CP-R100-UNWIND · WAVE R-100-UNWIND · self-reported §3.8 lapse "
        "cured · authors NEW wrapper services/enforce/principal_context_"
        "adapter.py owning the with-block protocol · restores sealed "
        "services/request_context/context.py byte-identical to Commit "
        "4b3b5e0 · re-points R-100 portal routers (portal_requests.py + "
        "portal_entitlement.py) to import principal_context from the "
        "wrapper · additive-only per SO §3.8"
    ),
    "note": (
        "R-100-UNWIND · self-reported §3.8 lapse cured · owner directive "
        "verbatim this-session (2026-09-21T~11:00Z): 'Modifying the "
        "sealed PrincipalRequestContext class in services/request_"
        "context/context.py to add __enter__/__exit__ is an edit to a "
        "sealed class — SO §3.8 forbids it. Unwind to a wrapper: "
        "revert context.py byte-identically to its sealed state, "
        "author a context-manager adapter inside services/enforce/ "
        "that owns the protocol, re-point the R-100 portal routers "
        "to the wrapper, seal as a self-reported §3.8 lapse cured, "
        "regenerate the three continuity bundles, pin their sha256s "
        "in STATE/PINS.md, then hold at the R-91 horizon (no "
        "expedite).' Cure relocation, not new invariant surface. "
        "Additive-only per SO §3.8: 1 new file "
        "services/enforce/principal_context_adapter.py (single module · "
        "single public callable `principal_context` context-manager · "
        "@contextlib.contextmanager over PRIN-11 propagation entry · "
        "enter sets ContextVar via the sealed module's _CURRENT_PRINCIPAL_ID "
        "via saved Token · exit resets that Token in try/finally so both "
        "normal and exceptional exits clear propagation without leaking · "
        "yields the sealed PrincipalRequestContext carrier unchanged) + "
        "1 new test file tests/invariants/test_principal_context_adapter.py "
        "with 5 tests (module-importable + enters-and-yields + exit-clears "
        "+ exception-propagates-and-clears + sealed-bytes-sha256-pinned). "
        "Sealed file services/request_context/context.py restored byte-"
        "identical to Commit 4b3b5e0 · sha256 ad0d94399af44bd5f6fa57f9aa"
        "1371ede7ca526789e47db10b45dddc79c39cfb (verified via `git show` "
        "extraction + diff shows IDENTICAL). Router edits are pure two-"
        "line substitutions in each of portal_requests.py + portal_"
        "entitlement.py: (a) import line changed from `from services."
        "request_context import enter_propagation` to `from services."
        "enforce.principal_context_adapter import principal_context`; "
        "(b) inside each handler `with enter_propagation(identity."
        "user_id):` replaced by `with principal_context(identity.user_"
        "id):` (5 handlers in portal_requests.py + 4 handlers in "
        "portal_entitlement.py = 9 substitutions total · sed -i "
        "atomic). Delta +5 MEASURED (5852 → 5857 · monotonic-up per "
        "CCS2 both fields bumped together · +5 new adapter tests · no "
        "test flipped to fail · no v8 or other spontaneous transitions). "
        "AUTHENTIC RED-first cycle: RED at drill_receipts/20260921T112718Z"
        "_r100_unwind_wrapper_RED_pre.log (5/5 fail right-reason "
        "ModuleNotFoundError services.enforce.principal_context_adapter "
        "for tests 1-4 + AssertionError sealed-bytes-sha256-drift for "
        "test 5 while illegal cure still present) → GREEN at drill_"
        "receipts/20260921T112831Z_r100_unwind_wrapper_GREEN_post.log "
        "(39/39 pass 0.90s covering 5 new adapter tests + all 21 R-100 "
        "portal write surface tests still GREEN after router re-point "
        "+ all 13 principal model v1 tests still GREEN with sealed "
        "context.py restored). Sealed R-100 portal write surface + "
        "sealed R-99 canon-rules HTTP router + sealed R-96..R-98 canon "
        "vocabulary + sealed R-88..R-95 seal chain all continue "
        "verbatim GREEN · additive-only per SO §3.8. Canon anchors "
        "verbatim: owner UNWIND directive this-session (2026-09-21T~11:00Z) "
        "+ Principal Model Spec v1 §5 PRIN-11 propagation-by-construction "
        "+ PRIN-13 read-only-once-in-propagation (both preserved verbatim: "
        "sealed carrier unchanged; wrapper owns only the with-block "
        "protocol) + R-100 seal 39412d09/e6a86c2c/0ae3713f (immediately-"
        "precedes on programme/track-a + master respectively) + R-100-A "
        "post-seal OPERATIONAL CURE at 320a752/00827f7a (this-lapse "
        "REVERTED-AND-BANKED · not rewritten in history · additive-only "
        "means the UNWIND lands as a new Commit-A on top of 320a752 "
        "reverting the illegal file change and adding the wrapper) + "
        "SO §2.5 verbatim-docstring + §3 tests-first + §3.3 3-Commit "
        "Seal + §3.8 additive-only (violated at 320a752 · cured "
        "this-wave · sealed-bytes sha-pin now structurally guards the "
        "file against future in-place edits) + §6.4 NOTHING-BEYOND "
        "(scope = wrapper + tests + sealed-file restore + router "
        "repoint · zero other file change) + §6.7 seal-report-boundary. "
        "Stop-conditions #1/#2/#3 NOT triggered. R-91 stays PARKED · "
        "horizon 2026-09-23T03:23:15Z UNCHANGED · current UTC ~11:30Z "
        "< horizon (~40h out) · R-100-UNWIND seal completes cleanly "
        "inside window with zero ceremony-apply operations opened. "
        "Autopilot next: Commit-B state master (bank DECISIONS.md "
        "entry framed as self-reported §3.8 lapse cured + drill "
        "receipts + this seal report) → Commit-C fixup (ORCH_BOOT "
        "R-6 boundary regen against Commit-B sha) → regenerate all "
        "three continuity bundles (code programme/track-a + state "
        "master + FE /app main) + pin sha256s in STATE/PINS.md → "
        "HOLD for R-91 horizon (NO EXPEDITE) → at horizon 2026-09-23T"
        "03:23:15Z execute R-91 ε-apply (mirror CURRENT /app/frontend/"
        "src/App.js byte-identically to pod_shell/frontend/src/App.js) "
        "→ M1-to-date BUILD_JOURNAL closure state-only. Standing bounds "
        "unchanged: zero push · zero remote configured on programme/"
        "track-a · terminal pytest only · no testing_agent (STRICTLY "
        "BANNED per SO §6) · additive-only §3.8 · three-repo discipline "
        "· ratchet monotonic-up floor 5857 · HF-HOLD SEC-2026-09-12-01 "
        "· R-24 UNLISTED · R-25 tagged."
    ),
    "passed": NEW,
    "delta": DELTA,
    "specialist_dispatch_drift_carried_forward": 3,
}

REGEN_REASON = (
    "r100-unwind-pre-commit-a-ratchet-only-regen-cp-r100-unwind-"
    "advancing-passed-floor-5852-to-5857-plus-new-baseline-failures-"
    "sha256-under-m16-w3-corrected-order-self-reported-so-3-8-lapse-"
    "cured-wrapper-services-enforce-principal-context-adapter-owning-"
    "with-block-protocol-sealed-context-py-restored-byte-identical-"
    "commit-4b3b5e0-sha256-ad0d9439-portal-requests-plus-portal-"
    "entitlement-repointed-to-wrapper-plus-sealed-bytes-sha-pin-test"
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
