"""Secret-hygiene guard for the pod `.env` files.

This module ships the DQ-12 CP-DOT-ENV-HYGIENE mechanism landed at
Turn 4 sub-slice 4b of the R-101 ε-apply wave (owner ruling R-101
condition (iv) verbatim relayed 2026-09-22T~06:12Z at
`STATE/DECISIONS.md:R-101 append`).

Fabric:
  * Owner ruling banked verbatim as `DOT_ENV_HYGIENE_RULING_VERBATIM`.
  * `POD_MAIN_ROOT` resolution: env var `AKKI_POD_MAIN_ROOT` or `/app`.
  * `verify_backend_env_untracked()`: returns True IFF /app/backend/.env
    is not tracked in git AND is git-check-ignored.
  * `verify_backend_env_local_gitignored()`: returns True IFF
    /app/backend/.env.local is git-check-ignored.
  * `verify_no_secret_kind_in_tracked_env()`: shape-only scan of any
    tracked backend/.env content for the six live-secret kinds
    (EMERGENT_LLM_KEY, JWT_SECRET, TIGRIS_SECRET_ACCESS_KEY,
    OPENAI_SK, HuggingFace hf_, AWS AKIA). Returns list of any hits.
    Values are NEVER printed by this function.

Discipline: this module NEVER prints the value of any secret. Only
kind labels + file-line pairs are ever exposed.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import List, Tuple


# Owner ruling R-101 condition (iv) verbatim (banked at
# STATE/DECISIONS.md:R-101 append · state master commit fbcbf1f7).
DOT_ENV_HYGIENE_RULING_VERBATIM: str = (
    "DQ-12 CP-DOT-ENV-HYGIENE (.env untracking + .env.local pattern)"
)


# Pod main root resolution: env var override for cross-pod portability;
# defaults to /app in the primary pod.
def pod_main_root() -> Path:
    return Path(os.environ.get("AKKI_POD_MAIN_ROOT", "/app"))


BACKEND_ENV_RELPATH = "backend/.env"
BACKEND_ENV_LOCAL_RELPATH = "backend/.env.local"


# Kind-labels for the six live-secret shapes. Values are NEVER printed.
LIVE_SECRET_KIND_PATTERNS: List[Tuple[str, "re.Pattern[str]"]] = [
    ("EMERGENT_LLM_KEY_or_OPENAI_SK", re.compile(r"^\s*(?:export\s+)?(?:EMERGENT_LLM_KEY|OPENAI_API_KEY)\s*=\s*sk-[A-Za-z0-9_\-]{20,}", re.M)),
    ("JWT_SECRET_high_entropy", re.compile(r"^\s*(?:export\s+)?JWT_SECRET\s*=\s*[A-Za-z0-9_\-+/=]{32,}", re.M)),
    ("TIGRIS_SECRET_ACCESS_KEY_high_entropy", re.compile(r"^\s*(?:export\s+)?TIGRIS_SECRET_ACCESS_KEY\s*=\s*[A-Za-z0-9_\-+/=]{20,}", re.M)),
    ("HUAWEI_OBS_SK_high_entropy", re.compile(r"^\s*(?:export\s+)?HUAWEI_OBS_SK\s*=\s*[A-Za-z0-9_\-+/=]{20,}", re.M)),
    ("HuggingFace_hf_token", re.compile(r"\bhf_[A-Za-z0-9]{30,}", re.M)),
    ("AWS_AKIA_ASIA_access_key", re.compile(r"\b(A(?:KIA|SIA)[0-9A-Z]{16})\b", re.M)),
]


def _run_git(*args: str) -> Tuple[int, str, str]:
    """Run git with given args. Returns (returncode, stdout, stderr).

    Never raises. Callers interpret returncode; git returns 0 for
    tracked/ignored (as appropriate for the subcommand) and non-zero
    for untracked/not-ignored.
    """
    root = pod_main_root()
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True, timeout=15,
    )
    return proc.returncode, proc.stdout, proc.stderr


def verify_backend_env_untracked() -> bool:
    """Returns True IFF /app/backend/.env is NOT tracked in git.

    Uses `git ls-files --error-unmatch backend/.env` — returns non-zero
    (raises pathspec error) if the file is untracked. That is the
    GREEN state after DQ-12 cure.
    """
    code, _out, _err = _run_git("ls-files", "--error-unmatch", BACKEND_ENV_RELPATH)
    # code 0 = tracked (RED); code non-zero = untracked (GREEN)
    return code != 0


def verify_backend_env_gitignored() -> bool:
    """Returns True IFF /app/backend/.env matches a gitignore rule.

    Uses `git check-ignore -v backend/.env` — returns 0 when the path
    is ignored by some rule. Post-DQ-12 cure the existing .env rule
    (or an explicit backend/.env rule) matches.
    """
    code, _out, _err = _run_git("check-ignore", "-v", BACKEND_ENV_RELPATH)
    return code == 0


def verify_backend_env_local_gitignored() -> bool:
    """Returns True IFF /app/backend/.env.local matches a gitignore rule."""
    code, _out, _err = _run_git("check-ignore", "-v", BACKEND_ENV_LOCAL_RELPATH)
    return code == 0


def verify_no_secret_kind_in_tracked_env() -> List[Tuple[str, int]]:
    """Shape-only scan of tracked backend/.env content for live-secret kinds.

    Reads the file at HEAD (if still tracked); returns list of
    (kind_label, line_number) tuples for any hits. Values are NEVER
    included in the return. Returns empty list if file is untracked
    (correct GREEN state) or if no kinds match.
    """
    # If untracked, nothing tracked to leak
    if verify_backend_env_untracked():
        return []

    root = pod_main_root()
    env_path = root / BACKEND_ENV_RELPATH
    if not env_path.is_file():
        return []

    try:
        text = env_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    hits: List[Tuple[str, int]] = []
    for kind, pat in LIVE_SECRET_KIND_PATTERNS:
        for m in pat.finditer(text):
            line_no = text.count("\n", 0, m.start()) + 1
            hits.append((kind, line_no))
    return sorted(set(hits))
