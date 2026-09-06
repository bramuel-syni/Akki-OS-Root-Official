"""Audit every service directory across all 4 repos, produce LOC +
last-commit-date matrix per (service, repo). Read-only."""
import subprocess, os, sys, json, pathlib

REPOS = [
    "/app/assessment_workspace/repos/RMS-IQ-Core-2",
    "/app/assessment_workspace/repos/Akki-OS-V1",
    "/app/assessment_workspace/repos/Akki-Executive-Core",
    "/app/assessment_workspace/repos/Extraction-Akki",
]

def sh(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, shell=True)
    return r.stdout.strip()

def get_services(repo):
    svc_dir = os.path.join(repo, "backend", "services")
    if not os.path.isdir(svc_dir):
        return []
    out = []
    for name in sorted(os.listdir(svc_dir)):
        if name.startswith("__") or name.startswith("."):
            continue
        p = os.path.join(svc_dir, name)
        if os.path.isdir(p):
            out.append(name)
    return out

def loc(repo, svc):
    p = os.path.join(repo, "backend", "services", svc)
    r = subprocess.run(
        f"find {p} -name '*.py' -exec cat {{}} + 2>/dev/null | wc -l",
        capture_output=True, text=True, shell=True)
    try: return int(r.stdout.strip())
    except: return 0

def last_commit(repo, svc):
    return sh(f"git log -1 --format=%cs -- backend/services/{svc}", repo)

def file_count(repo, svc):
    p = os.path.join(repo, "backend", "services", svc)
    r = subprocess.run(f"find {p} -name '*.py' | wc -l",
                       capture_output=True, text=True, shell=True)
    try: return int(r.stdout.strip())
    except: return 0

matrix = {}  # svc_name -> {repo_short: (loc, last_commit, file_count)}
repo_shorts = {}
for repo in REPOS:
    short = os.path.basename(repo)
    repo_shorts[repo] = short
    for svc in get_services(repo):
        matrix.setdefault(svc, {})
        matrix[svc][short] = (loc(repo, svc), last_commit(repo, svc),
                              file_count(repo, svc))

print(f"Total unique service names: {len(matrix)}")
out = {"generated_at_utc": "2026-09-06T19:00:00Z",
       "repos": [os.path.basename(r) for r in REPOS],
       "repo_heads": {os.path.basename(r): sh("git rev-parse --short HEAD", r) for r in REPOS},
       "services": {}}
for svc, per_repo in sorted(matrix.items()):
    out["services"][svc] = {}
    for short in [os.path.basename(r) for r in REPOS]:
        if short in per_repo:
            l, lc, fc = per_repo[short]
            out["services"][svc][short] = {"loc": l, "last_commit": lc, "files": fc}
        else:
            out["services"][svc][short] = None

pathlib.Path("/app/assessment_workspace/notes/TRUE_STATE_matrix.json").write_text(
    json.dumps(out, indent=2))
print(f"Wrote /app/assessment_workspace/notes/TRUE_STATE_matrix.json")
print(f"Services x repo count:")
for short in out["repos"]:
    n = sum(1 for s in matrix.values() if short in s)
    print(f"  {short}: {n} services")
