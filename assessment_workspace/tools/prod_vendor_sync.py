"""prod_vendor_sync.py · CP-PROD-DEPLOY-SELF-CONTAINMENT · deterministic vendor sync.

Owner directive verbatim this-session (2026-09-21T~11:45Z at CP-PROD-DEPLOY
directive):

    "VENDOR the runtime backend into /app/backend so the image is
    self-contained: a committed sync of every package the spine bridge
    mounts (routers/, services/, contracts/, plus whatever they import —
    trace the closure) into /app/backend (e.g. /app/backend/vendored/
    extraction_akki/ or flat, your call). Build it with a deterministic
    sync TOOL (committed, receipted) — not a hand copy — so re-syncs at
    future seals are mechanical and drift-testable (a mirror invariant
    like the pod_shell pattern would be in-discipline)."

What this tool does:
    Mirrors the RUNTIME portion of the sealed backend tree
    (/app/assessment_workspace/repos/Extraction-Akki/backend/) into
    /app/backend/vendored/extraction_akki/backend/ byte-identically.

    Included top-level dirs (runtime closure):
        services/  routers/  contracts/  data/  config/  drills/
        scripts/   estate_keys/
    Included top-level files: any *.py at backend root (currently none).

    Excluded (never vendored):
        tests/         (test-only surface; not needed at runtime)
        phase0/        (drill receipts, ~12 MB; not runtime)
        tools/         (tool scripts; not runtime)
        __pycache__/   (byte-compiled caches; regenerated per Python)
        .pytest_cache/ (test infrastructure)
        *.pyc          (byte-compiled cache files)
        .DS_Store, *.egg-info, .git*

Determinism:
    - File list is sorted (rglob + sort by relative path).
    - Idempotent: only writes when destination is missing OR content differs.
    - Emits a manifest with per-file sha256 for the mirror invariant test
      to consume: /app/backend/vendored/extraction_akki/MANIFEST.json.
    - Emits a summary receipt with total counts + top-level sha256 of
      the concatenated file-shas (structural hash for drift detection).

Zero remote · zero network · zero subprocess · zero git ops · pure local
Path.read_bytes + Path.write_bytes + hashlib.

Idempotency: safe to re-run at every seal boundary. If nothing changed
in the source tree, the vendored tree is untouched (mtime preserved
across writes-that-were-skipped).
"""

from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

SPINE_BACKEND = Path("/app/assessment_workspace/repos/Extraction-Akki/backend")
VENDORED_ROOT = Path("/app/backend/vendored/extraction_akki")
VENDORED_BACKEND = VENDORED_ROOT / "backend"
MANIFEST_PATH = VENDORED_ROOT / "MANIFEST.json"

# Top-level directories under SPINE_BACKEND that ARE vendored.
INCLUDED_TOP_DIRS = (
    "services",
    "routers",
    "contracts",
    "data",
    "config",
    "drills",
    "scripts",
    "estate_keys",
)

# Top-level *.py files under SPINE_BACKEND that ARE vendored. `server.py`
# is intentionally EXCLUDED — /app/backend/server.py is the entry point
# and vendoring the spine's server.py would create a shadow module name
# collision inside sys.path.
INCLUDED_TOP_PY_FILES = (
    "__init__.py",
    "core.py",
)

# Path substrings to skip anywhere in the tree.
EXCLUDE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".git",
}
EXCLUDE_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
}
EXCLUDE_FILE_NAMES = {
    ".DS_Store",
}
# Glob patterns (relative to SPINE_BACKEND) for auto-generated runtime state
# that lives inside the sealed tree BUT is not source-code. These files are
# untracked in the code repo (git status confirms) and would create false-
# positive drift for the mirror invariant on every re-sync.
EXCLUDE_REL_GLOBS = (
    "services/economics/tier_lock.v*.json",
)


def _iter_source_files() -> Iterable[Path]:
    """Yield every source-file path (absolute) under SPINE_BACKEND that
    passes the exclusion filters, sorted deterministically."""

    collected: list[Path] = []
    for name in INCLUDED_TOP_PY_FILES:
        p = SPINE_BACKEND / name
        if p.is_file():
            collected.append(p)
    for top in INCLUDED_TOP_DIRS:
        top_dir = SPINE_BACKEND / top
        if not top_dir.is_dir():
            continue
        for p in top_dir.rglob("*"):
            if not p.is_file():
                continue
            if any(part in EXCLUDE_DIR_NAMES for part in p.parts):
                continue
            if p.suffix in EXCLUDE_FILE_SUFFIXES:
                continue
            if p.name in EXCLUDE_FILE_NAMES:
                continue
            rel = p.relative_to(SPINE_BACKEND)
            if any(rel.match(g) for g in EXCLUDE_REL_GLOBS):
                continue
            collected.append(p)
    # Deterministic: relative-path sort.
    collected.sort(key=lambda p: str(p.relative_to(SPINE_BACKEND)))
    return collected


def _sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sync() -> dict:
    """Perform the mirror sync. Returns a summary dict."""

    if not SPINE_BACKEND.is_dir():
        raise SystemExit(
            f"SPINE_BACKEND missing: {SPINE_BACKEND} — cannot sync from an "
            "absent source tree. This tool must be run inside a sandbox "
            "where the workspace is present."
        )
    VENDORED_ROOT.mkdir(parents=True, exist_ok=True)

    files_written = 0
    files_skipped = 0
    files_removed = 0
    manifest: dict = {"files": {}}

    src_by_rel: dict[str, Path] = {}
    for src_abs in _iter_source_files():
        rel = str(src_abs.relative_to(SPINE_BACKEND))
        src_by_rel[rel] = src_abs

    for rel in sorted(src_by_rel):
        src_abs = src_by_rel[rel]
        dst_abs = VENDORED_BACKEND / rel
        dst_abs.parent.mkdir(parents=True, exist_ok=True)
        src_bytes = src_abs.read_bytes()
        file_sha = hashlib.sha256(src_bytes).hexdigest()
        manifest["files"][rel] = {
            "sha256": file_sha,
            "size_bytes": len(src_bytes),
        }
        if dst_abs.is_file() and dst_abs.read_bytes() == src_bytes:
            files_skipped += 1
            continue
        dst_abs.write_bytes(src_bytes)
        files_written += 1

    # Prune vendored files that no longer exist upstream (drift-cleanup).
    if VENDORED_BACKEND.is_dir():
        for vendored_abs in list(VENDORED_BACKEND.rglob("*")):
            if not vendored_abs.is_file():
                continue
            rel_v = str(vendored_abs.relative_to(VENDORED_BACKEND))
            if rel_v not in src_by_rel:
                vendored_abs.unlink()
                files_removed += 1
        # Prune empty dirs post-removal.
        for d in sorted(VENDORED_BACKEND.rglob("*"), reverse=True):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()

    # Structural top-level sha256: sha of the sorted (rel_path, sha256) pairs.
    structural_input = "\n".join(
        f"{rel}\t{manifest['files'][rel]['sha256']}"
        for rel in sorted(manifest["files"])
    )
    structural_sha256 = hashlib.sha256(structural_input.encode("utf-8")).hexdigest()

    manifest["structural_sha256"] = structural_sha256
    manifest["file_count"] = len(manifest["files"])
    manifest["generated_at_utc"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    manifest["source"] = {
        "spine_backend": str(SPINE_BACKEND),
        "included_top_dirs": list(INCLUDED_TOP_DIRS),
    }
    manifest["target"] = {
        "vendored_backend": str(VENDORED_BACKEND),
    }

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "file_count": manifest["file_count"],
        "files_written": files_written,
        "files_skipped": files_skipped,
        "files_removed": files_removed,
        "structural_sha256": structural_sha256,
    }


if __name__ == "__main__":
    summary = sync()
    print("prod_vendor_sync summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")
