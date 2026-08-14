#!/usr/bin/env python3
"""Strict file-count-by-type per requested spec: py/js/jsx/ts/tsx/other.
Also test file count (paths containing /tests/ or /test/ or matching *_test.py/*.test.js/etc.).
"""
import subprocess
from pathlib import Path
from collections import defaultdict

REPOS = ["RMS-IQ-Core-2", "Akki-OS-V1", "Extraction-Akki", "Akki-Executive-Core"]
BASE = Path("/app/assessment_workspace/repos")
BUCKETS = ["py", "js", "jsx", "ts", "tsx"]

def git_ls(repo):
    r = subprocess.run(["git", "ls-files"], cwd=str(BASE / repo),
                       capture_output=True, text=True, check=True)
    return [ln for ln in r.stdout.splitlines() if ln]

import re
test_re = re.compile(r'(^|/)(tests?)(/|$)|(_test\.|_spec\.|\.test\.|\.spec\.)')

print("| Repo | py | js | jsx | ts | tsx | other | test files | total |")
print("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
for repo in REPOS:
    files = git_ls(repo)
    buckets = defaultdict(int)
    tests = 0
    for f in files:
        ext = f.rsplit(".", 1)[-1].lower() if "." in f.rsplit("/", 1)[-1] else "_noext"
        if ext in BUCKETS:
            buckets[ext] += 1
        else:
            buckets["other"] += 1
        if test_re.search(f):
            tests += 1
    total = sum(buckets.values())
    row = f"| {repo} | {buckets['py']} | {buckets['js']} | {buckets['jsx']} | {buckets['ts']} | {buckets['tsx']} | {buckets['other']} | {tests} | {total} |"
    print(row)
