#!/usr/bin/env python3
"""Enumerate backend/services/ subdirectories per repo and identify cross-repo overlap.
Also for each repo, list what exists under docs/close_reports and docs/audits (titles only).
"""
import subprocess
from pathlib import Path
from collections import defaultdict

REPOS = ["RMS-IQ-Core-2", "Akki-OS-V1", "Extraction-Akki", "Akki-Executive-Core"]
BASE = Path("/app/assessment_workspace/repos")

def git_ls(repo):
    r = subprocess.run(["git", "ls-files"], cwd=str(BASE / repo),
                       capture_output=True, text=True, check=True)
    return [ln for ln in r.stdout.splitlines() if ln]

# ---------- 1. services/ subdirs per repo ----------
services_by_repo = {}   # repo -> {service_name: [file paths]}
for repo in REPOS:
    files = git_ls(repo)
    svc_map = defaultdict(list)
    for f in files:
        # backend/services/<svc>/... or in Akki-Executive-Core sometimes different
        parts = f.split("/")
        if len(parts) >= 3 and parts[0] == "backend" and parts[1] == "services":
            svc = parts[2]
            svc_map[svc].append(f)
    services_by_repo[repo] = dict(svc_map)

# ---------- 2. print full service listing per repo ----------
print("======================================================")
print(" backend/services/ SUBDIRECTORY LISTING PER REPO")
print("======================================================")
for repo in REPOS:
    svc_map = services_by_repo[repo]
    total_files = sum(len(v) for v in svc_map.values())
    print(f"\n----- {repo}: {len(svc_map)} service dirs, {total_files} files under backend/services/ -----")
    for svc in sorted(svc_map):
        n = len(svc_map[svc])
        print(f"  {svc:<45} {n} files")

# ---------- 3. cross-repo overlap of service names ----------
print("\n\n======================================================")
print(" CROSS-REPO SERVICE-NAME OVERLAP")
print("======================================================")
all_names = set()
for m in services_by_repo.values():
    all_names.update(m.keys())

def presence_row(name):
    row = []
    for r in REPOS:
        if name in services_by_repo[r]:
            row.append(str(len(services_by_repo[r][name])))
        else:
            row.append("—")
    return row

# services in 2+ repos
print(f"\n{'service':<45} " + " ".join(f"{r[:18]:<18}" for r in REPOS))
in_2plus = []
single = []
for name in sorted(all_names):
    present = sum(1 for r in REPOS if name in services_by_repo[r])
    if present >= 2:
        in_2plus.append(name)
    else:
        single.append(name)

print("\n-- Services present in 2 or more repos --")
print(f"{'service':<45} " + " ".join(f"{r[:18]:<18}" for r in REPOS))
for name in in_2plus:
    counts = presence_row(name)
    print(f"{name:<45} " + " ".join(f"{c:<18}" for c in counts))

print("\n-- Services present in EXACTLY ONE repo --")
for name in single:
    for r in REPOS:
        if name in services_by_repo[r]:
            print(f"  ONLY in {r:<22}  service={name}  ({len(services_by_repo[r][name])} files)")

# ---------- 4. docs/close_reports & docs/audits listing per repo ----------
print("\n\n======================================================")
print(" docs/close_reports, docs/audits, BUILD_JOURNAL PRESENCE PER REPO")
print("======================================================")
for repo in REPOS:
    files = git_ls(repo)
    bj = [f for f in files if f == "BUILD_JOURNAL.md"]
    close = sorted(f for f in files if f.startswith("docs/close_reports/"))
    audits = sorted(f for f in files if f.startswith("docs/audits/"))
    print(f"\n----- {repo} -----")
    print(f"  BUILD_JOURNAL.md:  {'present' if bj else 'MISSING'}")
    print(f"  docs/close_reports/: {len(close)} files")
    for f in close:
        print(f"    {f}")
    print(f"  docs/audits/: {len(audits)} files")
    for f in audits:
        print(f"    {f}")
