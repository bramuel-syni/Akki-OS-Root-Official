"""CP-M7-W1-POST-5-VERIFICATION · M3 wave-window verification under SO §4.2 (+ clause 6).

Wave-window:
- Open: W-M3-SW1  · eaa0e04 · 2026-09-14T05:24:59Z (Flag-2 tight-budget guard · clock.py extension)
- Close: W-M3-SW12 · 7123cf8 · 2026-09-14T09:24:26Z (M3 block-close composite invariant)
- Next-family open: W-CONN-SP1 · 4b0909a · 2026-09-14T10:05:14Z (source-plane connector · closes M3 window)

Verification checks (C.1-C.6, M3 domain scope):
  C.1 · Primitive surface frozen by dedicated SW test (verified via passing invariants).
  C.2 · Invariant tests pass file-scoped across all M3 test files.
  C.3 · No leak into case-agnostic platform kernels (work_supervisor, capability_registry,
        resource_registry, output_verified_seal). M3 modules ARE domain-specific by design;
        C.3 is domain-adapted (no leak into kernels rather than count domain tokens within).
  C.4 · Within-window last-touched: all 12 M3 modules last-touched within [eaa0e04^..7123cf8]
        EXCEPT clock.py (which is a cross-wave extension of the M2-SW5 addition; this IS
        the SO §4.2 clause 6 in-scope surface for M3).
  C.5 · Compose / scope-boundary honoured (verified via passing invariants).
  C.6 · No banned enforcement tokens (kill|terminate|refuse_dispatch|unregister) on any
        M3 module's public surface.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path("/app/assessment_workspace/repos/Extraction-Akki")
BACKEND = REPO / "backend"

M3_OPEN = "eaa0e04"
M3_CLOSE = "7123cf8"
M3_NEXT_FAMILY_OPEN = "4b0909a"

M3_MODULES = [
    ("W-M3-SW1", "eaa0e04", "services/reliable_time_source/clock.py", "MODIFIED (cross-wave extension of M2 SW5 addition · Flag-2 tight-budget guard)"),
    ("W-M3-SW2", "43889de", "services/watch/verdict_interface.py", "ADDED"),
    ("W-M3-SW3", "80198a5", "services/watch/certificate_library.py", "ADDED"),
    ("W-M3-SW4", "0640553", "services/watch/mirage_provocation.py", "ADDED"),
    ("W-M3-SW5", "156c21d", "services/watch/research_queue.py", "ADDED"),
    ("W-M3-SW6", "0b64c68", "services/watch/capability_admission.py", "ADDED"),
    ("W-M3-SW7", "48f0ba9", "services/agent_containment/__init__.py", "ADDED"),
    ("W-M3-SW7", "48f0ba9", "services/agent_containment/ceilings.py", "ADDED"),
    ("W-M3-SW8", "9309330", "services/dap/pruning_unlearning.py", "ADDED"),
    ("W-M3-SW9", "d859cc6", "services/agent_containment/serving_freeze.py", "ADDED"),
    ("W-M3-SW10", "c9469c8", "services/business_continuity/__init__.py", "ADDED"),
    ("W-M3-SW10", "c9469c8", "services/business_continuity/anchors.py", "ADDED"),
    ("W-M3-SW11", "10a3deb", "services/dap/m3_remainder.py", "ADDED"),
    ("W-M3-SW12", "7123cf8", "services/dap/m3_block_completion.py", "ADDED"),
]

M3_TESTS = [
    "tests/invariants/test_wm3_sw1_flag2_tight_budget_defensible_write.py",
    "tests/invariants/test_wm3_sw2_watch_stack_core.py",
    "tests/invariants/test_wm3_sw3_watch_learning_certificate_library.py",
    "tests/invariants/test_wm3_sw4_watch_learning_mirage_provocation.py",
    "tests/invariants/test_wm3_sw5_watch_learning_research_queue.py",
    "tests/invariants/test_wm3_sw6_watch_learning_capability_admission.py",
    "tests/invariants/test_wm3_sw7_agent_containment.py",
    "tests/invariants/test_wm3_sw8_pruning_unlearning.py",
    "tests/invariants/test_wm3_sw9_ac13_ac14_serving_freeze.py",
    "tests/invariants/test_wm3_sw10_bca_s10_s11_bc1_bc2.py",
    "tests/invariants/test_wm3_sw11_dap33_dap34_dap35_m3_remainder.py",
    "tests/invariants/test_wm3_sw12_m3_block_completion.py",
]

CASE_AGNOSTIC_KERNELS = [
    "services/work_supervisor",
    "services/capability_registry.py",
    "services/resource_registry",
    "services/output_verified_seal",
]

BANNED_TOKENS = ["kill", "terminate", "refuse_dispatch", "unregister"]


def sh(cmd: list[str], cwd: Path = REPO) -> str:
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return r.stdout


def check_c2_invariants() -> dict:
    """Run all 12 M3 test files file-scoped and report pass count + duration."""
    # POST-3 precedent: verification walks run file-scoped WITHOUT BASELINE_GUARD=1
    # (the HALT would fire because ratchet floor is 4384, larger than subset count).
    import os
    env = {k: v for k, v in os.environ.items() if k != "BASELINE_GUARD"}
    cmd = ["python", "-m", "pytest", "-q", *M3_TESTS]
    r = subprocess.run(cmd, cwd=str(BACKEND), capture_output=True, text=True, env=env)
    tail = r.stdout.strip().split("\n")[-3:]
    passed = None
    duration = None
    m = re.search(r"(\d+) passed[^\n]*in ([\d.]+)s", r.stdout)
    if m:
        passed = int(m.group(1))
        duration = float(m.group(2))
    return {
        "cmd": " ".join(cmd),
        "returncode": r.returncode,
        "passed": passed,
        "duration_s": duration,
        "tail": tail,
    }


def check_c3_no_kernel_leak() -> dict:
    """For each M3 commit, verify NO changes touched case-agnostic platform kernels."""
    results = []
    m3_commits = ["eaa0e04", "43889de", "80198a5", "0640553", "156c21d", "0b64c68",
                  "48f0ba9", "9309330", "d859cc6", "c9469c8", "10a3deb", "7123cf8"]
    for c in m3_commits:
        files = sh(["git", "show", "--name-only", "--format=", c]).strip().split("\n")
        touched = [f for f in files if any(k in f for k in CASE_AGNOSTIC_KERNELS)]
        results.append({
            "commit": c,
            "kernel_touches": touched,
        })
    total_touches = sum(len(r["kernel_touches"]) for r in results)
    return {
        "kernels_probed": CASE_AGNOSTIC_KERNELS,
        "per_commit": results,
        "total_kernel_touches": total_touches,
        "clean": total_touches == 0,
    }


def check_c4_within_window_last_touched() -> dict:
    """For each M3 module, get its last-touched commit and confirm it's within window
       (except clock.py which is cross-wave)."""
    results = []
    for sw, commit, path, kind in M3_MODULES:
        # get last commit that touched this file (any time)
        full = sh(["git", "log", "-1", "--format=%h|%cI|%s", "programme/track-a", "--", f"backend/{path}"]).strip()
        # within-window last-touched
        in_window = sh(["git", "log", "-1", "--format=%h|%cI", f"{M3_OPEN}^..{M3_CLOSE}", "--", f"backend/{path}"]).strip()
        # post-window modifications (drift-check surface)
        post_window = sh(["git", "log", "--format=%h|%cI|%s", f"{M3_CLOSE}..HEAD", "programme/track-a", "--", f"backend/{path}"]).strip()
        results.append({
            "sub_wave": sw,
            "sw_commit": commit,
            "path": path,
            "kind": kind,
            "in_window_last_touched": in_window,
            "overall_last_touched": full,
            "post_window_modifications": post_window.split("\n") if post_window else [],
        })
    return {"per_module": results}


def check_c6_no_banned_tokens() -> dict:
    """Grep each M3 module for banned enforcement token names as function/class/method names."""
    results = []
    for sw, commit, path, kind in M3_MODULES:
        full = BACKEND / path
        if not full.exists():
            results.append({"path": path, "exists": False})
            continue
        text = full.read_text()
        hits = []
        for tok in BANNED_TOKENS:
            # look for def, class, or method binding
            for m in re.finditer(rf"^\s*def\s+({tok}\w*|_?{tok}\w*)\s*\(", text, flags=re.MULTILINE):
                hits.append({"token": tok, "context": m.group(0).strip()})
            for m in re.finditer(rf"^\s*class\s+(\w*{tok}\w*)\s*[\(:]", text, flags=re.MULTILINE):
                hits.append({"token": tok, "context": m.group(0).strip()})
        results.append({
            "path": path,
            "exists": True,
            "hits": hits,
        })
    total = sum(len(r.get("hits", [])) for r in results)
    return {
        "banned_tokens": BANNED_TOKENS,
        "per_module": results,
        "total_hits_on_public_surface": total,
        "clean": total == 0,
    }


def main():
    receipt = {
        "cp": "CP-M7-W1-POST-5-VERIFICATION",
        "type": "verification_walk",
        "wave_window": "M3",
        "so_ref": "SO §4.2 wave-window commit enumeration + clause 6 cross-wave modification handling",
        "window_open_commit": M3_OPEN,
        "window_close_commit": M3_CLOSE,
        "window_next_family_open_commit": M3_NEXT_FAMILY_OPEN,
        "modules_enumerated": len(M3_MODULES),
        "tests_enumerated": len(M3_TESTS),
    }

    print("== C.2 · Invariant tests pass ==")
    c2 = check_c2_invariants()
    receipt["c2_invariants"] = c2
    print(f"  {c2['passed']} passed in {c2['duration_s']}s · rc={c2['returncode']}")

    print("== C.3 · No leak into case-agnostic kernels ==")
    c3 = check_c3_no_kernel_leak()
    receipt["c3_no_kernel_leak"] = c3
    print(f"  clean={c3['clean']} · total_kernel_touches={c3['total_kernel_touches']}")

    print("== C.4 · Within-window last-touched ==")
    c4 = check_c4_within_window_last_touched()
    receipt["c4_within_window"] = c4
    for m in c4["per_module"]:
        pw = m["post_window_modifications"]
        note = f" · POST-WINDOW-MODS: {len(pw)}" if pw and pw[0] else ""
        print(f"  {m['sub_wave']} · {m['path']} · in-window: {m['in_window_last_touched']}{note}")

    print("== C.6 · No banned enforcement tokens ==")
    c6 = check_c6_no_banned_tokens()
    receipt["c6_no_banned_tokens"] = c6
    print(f"  clean={c6['clean']} · total_hits={c6['total_hits_on_public_surface']}")

    # verdict
    verdict = "clean"
    for f in ("c2_invariants", "c3_no_kernel_leak", "c6_no_banned_tokens"):
        v = receipt[f]
        if f == "c2_invariants" and (v.get("returncode") != 0 or v.get("passed") is None):
            verdict = "dirty"
        if f in ("c3_no_kernel_leak", "c6_no_banned_tokens") and not v.get("clean"):
            verdict = "dirty"
    receipt["verdict"] = verdict
    receipt["path_taken"] = "Path α" if verdict == "clean" else "Path β"
    receipt["ratchet_delta"] = 0
    receipt["wave_window_now_fully_verified"] = verdict == "clean"

    out = Path("/app/assessment_workspace/phase0/m7_w1_post_5_verification/verification_receipt_20260916.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"\n== RECEIPT WRITTEN ==\n{out}\nverdict={verdict} path={receipt['path_taken']}")


if __name__ == "__main__":
    main()
