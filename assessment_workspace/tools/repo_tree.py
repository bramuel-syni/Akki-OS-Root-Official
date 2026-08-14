#!/usr/bin/env python3
"""Produce a depth-2 directory tree summary for each repo, plus per-service dir listings."""
import subprocess
from pathlib import Path
from collections import defaultdict

REPOS = ["RMS-IQ-Core-2", "Akki-OS-V1", "Extraction-Akki", "Akki-Executive-Core"]
BASE = Path("/app/assessment_workspace/repos")

def git_ls_files(repo):
    r = subprocess.run(["git", "ls-files"], cwd=str(BASE / repo),
                       capture_output=True, text=True, check=True)
    return [ln for ln in r.stdout.splitlines() if ln]

for repo in REPOS:
    print(f"\n===== {repo} =====")
    files = git_ls_files(repo)
    top = defaultdict(int)
    lvl2 = defaultdict(int)
    for f in files:
        parts = f.split("/")
        if len(parts) == 1:
            top[parts[0]] += 1
        else:
            top[parts[0] + "/"] += 1
            if len(parts) >= 2:
                lvl2[parts[0] + "/" + parts[1] + "/"] += 1
    print(f"total files: {len(files)}")
    print("\n-- level 1 --")
    for k in sorted(top):
        print(f"  {k:<40} {top[k]} entries")
    print("\n-- level 2 (top 60 by file count) --")
    for k, v in sorted(lvl2.items(), key=lambda x: -x[1])[:60]:
        print(f"  {k:<60} {v} files")
