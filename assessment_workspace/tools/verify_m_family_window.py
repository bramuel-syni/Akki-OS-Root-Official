"""Parameterized M-family wave-window verifier (POST-7 M5 · POST-8 M6).

Usage:
    python3 tools/verify_m_family_window.py <milestone_id>

Supported milestone_ids: M5, M6.
"""

from __future__ import annotations
import json, os, re, subprocess, sys
from pathlib import Path

REPO = Path("/app/assessment_workspace/repos/Extraction-Akki")
BACKEND = REPO / "backend"

CASE_AGNOSTIC_KERNELS = [
    "services/work_supervisor",
    "services/capability_registry.py",
    "services/resource_registry",
    "services/output_verified_seal",
]

BANNED_TOKENS = ["kill", "terminate", "refuse_dispatch", "unregister"]

MILESTONES = {
    "M5": {
        "cp_number": 7,
        "open_commit": "24928de",  # W-AUDIO-POC CP-A1
        "close_commit": "7cccbe8",  # W-D12-POC CP-D12P1
        "next_family_open_commit": "e02dd4d",  # W-M8-TESTS-FIRST-GUARD-INVARIANT
        "description": "M5 · Data-Suite-v2 lift + Audio-POC + Census-run + Release-gate + D12 POC (compound milestone · 6 named sub-waves + 1 supplement)",
        "sub_waves": [
            ("W-AUDIO-POC", ["24928de","84bc5e6","815500a","4b7ca3a","6243a24","dc498fd"]),
            ("W-DATA-SUITE-V2-LIFT", ["ed0265f","6df2a40","2b002df","cdcab77","aebec40","7202916","3dc0d63","6549c31"]),
            ("W-CENSUS-CANON-ALIGN", ["c45d0c3","112de26","e2a710c","5fcee76","d552c31","0053b16"]),
            ("W-RELEASE-GATE-PILOT-LIFT", ["e8a40b8","d28d2d0","440b995","4c4500a","ee45e69","7a5f431"]),
            ("W-CENSUS-SUPPLEMENT-AUDIO-INVENTORY-MOUNT", ["4308620"]),
            ("W-D12-POC", ["7cccbe8"]),
        ],
    },
    "M6": {
        "cp_number": 8,
        "open_commit": "b105aa0",  # CP-M6-1-1
        "close_commit": "7b45a89",  # CP-M6-9-2 (last M6 commit before CP-M7-W1-POST-1)
        "next_family_open_commit": "2c7a8f0",  # CP-M7-W1-POST-1
        "description": "M6 · Audio Plane v1 Production Build (9 sub-waves · SW1..SW9)",
        "sub_waves": [
            # Enumerated at runtime via git log
        ],
    },
}


def sh(cmd, cwd=REPO):
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True).stdout


def enumerate_window_files(open_commit: str, close_commit: str, path_glob: str) -> list[tuple[str, str, str]]:
    """Returns list of (commit, path, when_iso) for first-added files in window."""
    r = subprocess.run(
        ["git","log","--diff-filter=A","--name-only","--format=%H|%cI",f"{open_commit}^..{close_commit}","--",path_glob],
        cwd=str(REPO), capture_output=True, text=True,
    )
    out = []
    current_commit = None
    current_when = None
    for line in r.stdout.split("\n"):
        if "|" in line and re.match(r"^[0-9a-f]{40}\|", line):
            current_commit, current_when = line.split("|", 1)
        elif line.strip() and not line.startswith("---"):
            if "pycache" in line or line.endswith(".pyc"):
                continue
            out.append((current_commit[:7], line, current_when))
    return out


def run_pytest_file_scoped(test_files: list[str]) -> dict:
    env = {k: v for k, v in os.environ.items() if k != "BASELINE_GUARD"}
    r = subprocess.run(
        ["python", "-m", "pytest", "-q", *test_files],
        cwd=str(BACKEND), capture_output=True, text=True, env=env,
    )
    m = re.search(r"(\d+) passed[^\n]*in ([\d.]+)s", r.stdout)
    return {
        "cmd": "python -m pytest -q <{}> file-scoped".format(len(test_files)),
        "returncode": r.returncode,
        "passed": int(m.group(1)) if m else None,
        "duration_s": float(m.group(2)) if m else None,
        "tail": r.stdout.strip().split("\n")[-3:],
    }


def check_c3_no_kernel_leak(commits: list[str]) -> dict:
    per = []
    for c in commits:
        files = sh(["git","show","--name-only","--format=",c]).strip().split("\n")
        touched = [f for f in files if any(k in f for k in CASE_AGNOSTIC_KERNELS)]
        per.append({"commit": c, "kernel_touches": touched})
    total = sum(len(x["kernel_touches"]) for x in per)
    return {"kernels_probed": CASE_AGNOSTIC_KERNELS, "per_commit": per, "total_kernel_touches": total, "clean": total == 0}


def check_c4_within_window(modules: list[tuple[str,str,str]], open_c: str, close_c: str) -> dict:
    per = []
    for commit, path, when in modules:
        in_window = sh(["git","log","-1","--format=%h|%cI",f"{open_c}^..{close_c}","--",path]).strip()
        post_window = sh(["git","log","--format=%h|%cI|%s",f"{close_c}..HEAD","--",path]).strip()
        per.append({
            "sw_commit": commit, "path": path, "added_when": when,
            "in_window_last_touched": in_window,
            "post_window_modifications": post_window.split("\n") if post_window else [],
        })
    return {"per_module": per, "post_window_modification_count": sum(1 for m in per if m["post_window_modifications"] and m["post_window_modifications"][0])}


def check_c6_no_banned_tokens(modules: list[tuple[str,str,str]]) -> dict:
    per = []
    for commit, path, when in modules:
        full = REPO / path
        if not full.exists():
            per.append({"path": path, "exists": False, "hits": []})
            continue
        text = full.read_text()
        hits = []
        for tok in BANNED_TOKENS:
            for m in re.finditer(rf"^\s*def\s+({tok}\w*|_?{tok}\w*)\s*\(", text, flags=re.MULTILINE):
                hits.append({"token": tok, "context": m.group(0).strip()})
            for m in re.finditer(rf"^\s*class\s+(\w*{tok}\w*)\s*[\(:]", text, flags=re.MULTILINE):
                hits.append({"token": tok, "context": m.group(0).strip()})
        per.append({"path": path, "exists": True, "hits": hits})
    total = sum(len(x["hits"]) for x in per)
    return {"banned_tokens": BANNED_TOKENS, "per_module": per, "total_hits_on_public_surface": total, "clean": total == 0}


def enumerate_window_commits(open_c: str, close_c: str) -> list[dict]:
    r = subprocess.run(
        ["git","log","--format=%h|%cI|%s",f"{open_c}^..{close_c}","--reverse"],
        cwd=str(REPO), capture_output=True, text=True,
    )
    out = []
    for line in r.stdout.strip().split("\n"):
        parts = line.split("|", 2)
        if len(parts) == 3:
            out.append({"commit": parts[0], "when": parts[1], "subject": parts[2]})
    return out


def main(milestone_id: str):
    if milestone_id not in MILESTONES:
        print(f"Unknown milestone: {milestone_id}", file=sys.stderr)
        sys.exit(1)
    ms = MILESTONES[milestone_id]

    # Enumerate window commits + modules + tests
    commits = enumerate_window_commits(ms["open_commit"], ms["close_commit"])
    modules = enumerate_window_files(ms["open_commit"], ms["close_commit"], "backend/services/")
    test_files_full = enumerate_window_files(ms["open_commit"], ms["close_commit"], "backend/tests/invariants/")
    test_paths = [p.replace("backend/", "", 1) for _, p, _ in test_files_full]

    # Prefix modules with backend/
    modules_full = [(c, p if p.startswith("backend/") else f"backend/{p}", w) for c, p, w in modules]

    print(f"== {milestone_id} · {ms['description']} ==")
    print(f"  window: {ms['open_commit']}..{ms['close_commit']} · next-open: {ms['next_family_open_commit']}")
    print(f"  commits enumerated: {len(commits)}")
    print(f"  services/ modules first-added: {len(modules_full)}")
    print(f"  tests/invariants/ files first-added: {len(test_paths)}")

    # C.2 · invariants pass
    c2 = run_pytest_file_scoped(test_paths)
    print(f"C.2 · {c2['passed']} passed in {c2['duration_s']}s · rc={c2['returncode']}")

    # C.3 · no kernel leak
    c3 = check_c3_no_kernel_leak([c["commit"] for c in commits])
    print(f"C.3 · clean={c3['clean']} · total_kernel_touches={c3['total_kernel_touches']}")

    # C.4 · within-window last-touched
    c4 = check_c4_within_window(modules_full, ms["open_commit"], ms["close_commit"])
    print(f"C.4 · post-window-modification count: {c4['post_window_modification_count']}")

    # C.6 · no banned tokens
    c6 = check_c6_no_banned_tokens(modules_full)
    print(f"C.6 · clean={c6['clean']} · total_hits={c6['total_hits_on_public_surface']}")

    verdict = "clean" if (c2["returncode"] == 0 and c3["clean"] and c6["clean"]) else "dirty"

    receipt = {
        "cp": f"CP-M7-W1-POST-{ms['cp_number']}-VERIFICATION",
        "type": "verification_walk",
        "wave_window": milestone_id,
        "description": ms["description"],
        "so_ref": "SO §4.2 wave-window commit enumeration + clause 6 cross-wave modification handling",
        "window_open_commit": ms["open_commit"],
        "window_close_commit": ms["close_commit"],
        "window_next_family_open_commit": ms["next_family_open_commit"],
        "commits_enumerated": commits,
        "modules_enumerated": modules_full,
        "tests_enumerated": test_paths,
        "commit_count": len(commits),
        "module_count": len(modules_full),
        "test_count": len(test_paths),
        "sub_waves_declared": ms.get("sub_waves"),
        "c2_invariants": c2,
        "c3_no_kernel_leak": c3,
        "c4_within_window": c4,
        "c6_no_banned_tokens": c6,
        "verdict": verdict,
        "path_taken": "Path α" if verdict == "clean" else "Path β",
        "ratchet_delta": 0,
        "wave_window_now_fully_verified": verdict == "clean",
    }
    out = Path(f"/app/assessment_workspace/phase0/m7_w1_post_{ms['cp_number']}_verification/verification_receipt_20260916.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True, default=str))
    print(f"\n== RECEIPT WRITTEN ==\n{out}\nverdict={verdict} path={receipt['path_taken']}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "M5")
