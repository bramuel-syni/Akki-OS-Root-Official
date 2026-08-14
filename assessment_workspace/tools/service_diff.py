#!/usr/bin/env python3
"""For each backend/services/<svc> present in 2+ repos, compute:
  - file count per repo
  - total lines per repo (counting text files only)
  - last commit date affecting that path (git log -1 --format=%cI -- <path>)
  - diff summary vs a chosen 'anchor' repo (the one with the most files for that service):
        * IDENTICAL: same file set AND every file byte-identical
        * SUPERSET_OF_ANCHOR: has every anchor file identical + extras
        * DIVERGED: at least one file differs (content or path set)
Also list services present in EXACTLY ONE repo.
"""
import subprocess
import hashlib
from pathlib import Path
from collections import defaultdict

REPOS = ["RMS-IQ-Core-2", "Akki-OS-V1", "Extraction-Akki", "Akki-Executive-Core"]
BASE = Path("/app/assessment_workspace/repos")

def git_ls(repo):
    r = subprocess.run(["git", "ls-files"], cwd=str(BASE / repo),
                       capture_output=True, text=True, check=True)
    return [ln for ln in r.stdout.splitlines() if ln]

def git_last_commit_date(repo, path):
    r = subprocess.run(
        ["git", "log", "-1", "--format=%cI", "--", path],
        cwd=str(BASE / repo), capture_output=True, text=True, check=True)
    return r.stdout.strip() or "n/a"

def count_lines(path):
    try:
        return sum(1 for _ in open(path, "rb"))
    except Exception:
        return 0

def sha256_file(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while True:
                b = f.read(65536)
                if not b: break
                h.update(b)
        return h.hexdigest()
    except Exception:
        return "ERROR"

# Build services map per repo (service -> [rel paths])
services_by_repo = {}
for repo in REPOS:
    files = git_ls(repo)
    svc_map = defaultdict(list)
    for f in files:
        parts = f.split("/")
        if len(parts) >= 3 and parts[0] == "backend" and parts[1] == "services":
            svc_map[parts[2]].append(f)
    services_by_repo[repo] = dict(svc_map)

# All service names ever seen
all_names = set()
for m in services_by_repo.values():
    all_names.update(m.keys())

# Determine which are shared
shared = sorted([n for n in all_names
                 if sum(1 for r in REPOS if n in services_by_repo[r]) >= 2])

# For each shared service compute measurements
print("# Cross-repo service delta measurements\n")
print("Legend: files/lines/last-commit per repo. Diff status computed against 'anchor' = repo with most files.\n")

for name in shared:
    print(f"\n## service: `{name}`\n")
    present_in = [r for r in REPOS if name in services_by_repo[r]]

    # Compute stats per repo
    stats = {}
    file_sets = {}
    hash_maps = {}
    for repo in present_in:
        rel_paths = sorted(services_by_repo[repo][name])
        total_files = len(rel_paths)
        total_lines = 0
        hashes = {}
        for rel in rel_paths:
            full = BASE / repo / rel
            total_lines += count_lines(full)
            hashes[rel] = sha256_file(full)
        last_date = git_last_commit_date(repo, f"backend/services/{name}/")
        # But git log with dir may return empty; try without slash
        if not last_date or last_date == "n/a":
            last_date = git_last_commit_date(repo, f"backend/services/{name}")
        stats[repo] = (total_files, total_lines, last_date)
        file_sets[repo] = set(rel_paths)
        hash_maps[repo] = hashes

    # Table row
    print("| Repo | files | lines | last commit date (this path) |")
    print("|---|---:|---:|---|")
    for repo in present_in:
        f, l, d = stats[repo]
        print(f"| {repo} | {f} | {l} | {d} |")

    # Determine anchor = repo with most files
    anchor = max(present_in, key=lambda r: stats[r][0])
    print(f"\nAnchor for comparison: **{anchor}** ({stats[anchor][0]} files)")

    # Compare each other repo to anchor by relative path (strip repo, keep 'backend/services/...')
    # We need to compare by same rel-path AND by content
    anchor_paths = file_sets[anchor]
    anchor_hashes = hash_maps[anchor]

    diff_lines = []
    for repo in present_in:
        if repo == anchor:
            continue
        rp = file_sets[repo]
        rh = hash_maps[repo]
        # missing = in anchor not in repo; extra = in repo not in anchor
        missing = sorted(anchor_paths - rp)
        extra = sorted(rp - anchor_paths)
        common = anchor_paths & rp
        content_diff = [p for p in sorted(common) if anchor_hashes[p] != rh[p]]

        if not missing and not extra and not content_diff:
            status = "IDENTICAL to anchor"
        elif not missing and not content_diff and extra:
            status = f"SUPERSET_OF_ANCHOR (adds {len(extra)} files)"
        elif not extra and not content_diff and missing:
            status = f"SUBSET_OF_ANCHOR (missing {len(missing)} files)"
        else:
            status = f"DIVERGED (missing_here={len(missing)}, extra_here={len(extra)}, content_diff={len(content_diff)})"

        diff_lines.append(f"- **{repo} vs {anchor}**: {status}")
        if missing:
            diff_lines.append(f"    - files IN {anchor} MISSING FROM {repo}: {len(missing)}")
            for p in missing[:5]:
                diff_lines.append(f"        - {p}")
            if len(missing) > 5:
                diff_lines.append(f"        - ... +{len(missing)-5} more")
        if extra:
            diff_lines.append(f"    - files IN {repo} MISSING FROM {anchor}: {len(extra)}")
            for p in extra[:5]:
                diff_lines.append(f"        - {p}")
            if len(extra) > 5:
                diff_lines.append(f"        - ... +{len(extra)-5} more")
        if content_diff:
            diff_lines.append(f"    - files with SAME PATH BUT DIFFERENT CONTENT: {len(content_diff)}")
            for p in content_diff[:5]:
                diff_lines.append(f"        - {p}")
            if len(content_diff) > 5:
                diff_lines.append(f"        - ... +{len(content_diff)-5} more")

    print()
    for ln in diff_lines:
        print(ln)
    # Note absent repos
    absent = [r for r in REPOS if r not in present_in]
    if absent:
        print(f"\nAbsent in: {', '.join(absent)}")
