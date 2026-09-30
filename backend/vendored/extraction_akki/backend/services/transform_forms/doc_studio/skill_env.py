"""doc-studio v1.1 skill runtime binding: the installed skill's scripts are importable, and its tool paths come from the
environment (DOC_STUDIO_TOOLS_DIR, owner condition A). Nothing in the skill directory is edited beyond that one line."""
from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL_DIR = HERE / "skill"
SCRIPTS_DIR = SKILL_DIR / "scripts"
TOOLS_DIR = Path(os.environ.get("DOC_STUDIO_TOOLS_DIR") or (HERE / "tools"))
os.environ.setdefault("DOC_STUDIO_TOOLS_DIR", str(TOOLS_DIR))
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


def skill_module(name: str):
    """Import one of the skill's scripts (studio, validate, freeze, revise, build, qa, render_*) by name."""
    return importlib.import_module(name)


def build_env() -> dict:
    env = dict(os.environ)
    env["DOC_STUDIO_TOOLS_DIR"] = str(TOOLS_DIR)
    env.setdefault("MPLBACKEND", "Agg")
    return env
