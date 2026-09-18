#!/usr/bin/env python3
"""
CHUNK 1 Task C · Cross-repo overlap measurement.

Enumerates backend/services children per repo, computes overlap matrix,
per-service file counts + total LOC + last-modified commit date + a
crude diff summary (identical / A superset of B / diverged / diverged-with-common)
based on file-name-set and file-content-sha256 sets.

Throwaway analysis under tools/. No production code touched.
Owner ruling 1a: file-level summary only (no per-file unified diffs).
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPOS = [
    "RMS-IQ-Core-2",
    "Akki-OS-V1",
    "Extraction-Akki",
    "Akki-Executive-Core",
    "Akki-Executive-Final",  # anomaly (not in 4)
]
WS = Path("/app/assessment_workspace/repos")


def _run(repo: str, args: list[str]) -> str:
    return subprocess.run(
        ["git", "-C", str(WS / repo), *args],
        capture_output=True, text=True, check=False,
    ).stdout


def list_service_children(repo: str) -> list[str]:
    """List backend/services/* names (dirs + .py files at that level)."""
    root = WS / repo / "backend" / "services"
    if not root.is_dir():
        return []
    return sorted(p.name for p in root.iterdir() if not p.name.startswith("__"))


def enumerate_service_files(repo: str, service: str) -> list[Path]:
    """All git-tracked files under backend/services/{service} (dir) or the file itself."""
    root = WS / repo / "backend" / "services" / service
    if root.is_file():
        return [root]
    if not root.exists():
        return []
    out = _run(repo, ["ls-files", f"backend/services/{service}/"])
    return [WS / repo / p for p in out.splitlines() if p.strip()]


def sha256_of(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except (FileNotFoundError, IsADirectoryError):
        return ""


def loc_of(p: Path) -> int:
    try:
        return sum(1 for _ in p.open("rb"))
    except (FileNotFoundError, IsADirectoryError, OSError):
        return 0


def last_commit_date(repo: str, service: str) -> str:
    """Last commit ISO date touching backend/services/{service}."""
    out = _run(repo, [
        "log", "-1", "--format=%aI", "--",
        f"backend/services/{service}",
    ])
    return out.strip() or "(none)"


def build_matrix() -> dict:
    """
    services[name] = {
        "presence": {repo: bool, ...},
        "per_repo": {
            repo: {
                "file_count": int,
                "total_loc": int,
                "last_commit_date": iso,
                "file_names": [str, ...],  # relative to backend/services/{name}/
                "file_shas": {rel: sha256, ...},
            }
        }
    }
    """
    all_names: set[str] = set()
    for r in REPOS:
        all_names.update(list_service_children(r))

    matrix = {}
    for name in sorted(all_names):
        per_repo = {}
        for r in REPOS:
            files = enumerate_service_files(r, name)
            if not files:
                continue
            svc_root = WS / r / "backend" / "services" / name
            rel_names = []
            rel_shas = {}
            total_loc = 0
            for f in files:
                if not f.exists():
                    continue
                rel = str(f.relative_to(svc_root)) if svc_root.is_dir() else name
                rel_names.append(rel)
                rel_shas[rel] = sha256_of(f)
                total_loc += loc_of(f)
            per_repo[r] = {
                "file_count": len(rel_names),
                "total_loc": total_loc,
                "last_commit_date": last_commit_date(r, name),
                "file_names": sorted(rel_names),
                "file_shas": rel_shas,
            }
        matrix[name] = {
            "presence": {r: (r in per_repo) for r in REPOS},
            "per_repo": per_repo,
        }
    return matrix


def summarise_diff(per_repo: dict) -> str:
    """Cheap diff summary based on {filename: sha256} sets."""
    repos = list(per_repo.keys())
    if len(repos) < 2:
        return "N/A · single-repo"
    # Normalise to (name -> sha) dicts
    sha_maps = {r: per_repo[r]["file_shas"] for r in repos}
    name_sets = {r: set(sha_maps[r].keys()) for r in repos}
    if all(sha_maps[r] == sha_maps[repos[0]] for r in repos):
        return "identical (all repos byte-equal file-set)"
    # subset checks pairwise
    all_ident = True
    superset_lines = []
    for a in repos:
        for b in repos:
            if a == b:
                continue
            if name_sets[a] > name_sets[b] and all(
                sha_maps[a].get(f) == sha_maps[b].get(f) for f in name_sets[b]
            ):
                superset_lines.append(f"{a}⊇{b}")
        all_ident = False
    common_names = set.intersection(*name_sets.values())
    common_sha_ident = all(
        len({sha_maps[r].get(f) for r in repos}) == 1 for f in common_names
    ) if common_names else False
    parts = []
    if superset_lines:
        parts.append("; ".join(sorted(set(superset_lines))))
    if common_names:
        parts.append(
            f"common-files={len(common_names)}"
            f" (sha-identical-across-repos: {common_sha_ident})"
        )
    else:
        parts.append("no common filenames")
    return "diverged · " + " · ".join(parts) if parts else "diverged"


def main():
    matrix = build_matrix()
    # summary
    single_repo = []
    multi_repo = []
    for name, data in matrix.items():
        present_in = [r for r, v in data["presence"].items() if v]
        if len(present_in) == 1:
            single_repo.append((name, present_in[0]))
        else:
            multi_repo.append((name, present_in))
    print(f"total unique service names: {len(matrix)}")
    print(f"multi-repo services: {len(multi_repo)}")
    print(f"single-repo services: {len(single_repo)}")
    out = {
        "generated_at": __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).isoformat(),
        "repos_scanned": REPOS,
        "matrix": {
            name: {
                "presence": data["presence"],
                "per_repo_summary": {
                    r: {
                        "file_count": data["per_repo"][r]["file_count"],
                        "total_loc": data["per_repo"][r]["total_loc"],
                        "last_commit_date": data["per_repo"][r]["last_commit_date"],
                        "file_names": data["per_repo"][r]["file_names"],
                    }
                    for r in data["per_repo"]
                },
                "diff_summary": summarise_diff(data["per_repo"]),
            }
            for name, data in matrix.items()
        },
        "single_repo_services": single_repo,
        "multi_repo_services": multi_repo,
    }
    Path("/tmp/chunk1_task_c_matrix.json").write_text(json.dumps(out, indent=2))
    print("wrote /tmp/chunk1_task_c_matrix.json")


if __name__ == "__main__":
    main()
