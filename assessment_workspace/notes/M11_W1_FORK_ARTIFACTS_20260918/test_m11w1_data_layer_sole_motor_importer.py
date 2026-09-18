"""tests/invariants/test_m11w1_data_layer_sole_motor_importer.py

M11-W1 · SOLE MOTOR IMPORTER discipline (AST-based, wave-open baseline).

Canon anchor (verbatim):
  v1.0 B.2 · "Primary datastore is Mongo, one database per tenant, all
  access via `services.data.repository` — the sole Motor importer."
  R-18 Tension (a) Option C · SO §3.8 amended in-place: "M11-W1 lands
  `services/data/repository.py` as the sole Motor importer.  Adapters at
  `services/enforce/<entity>_gate.py` (W3+) call the paired M9 refuser
  first, then a Repository op."

Wave-open reality (banked at M11-W1 open · 2026-09-18):
  There are 12 pre-existing motor importers in the tree (from earlier
  waves M2-M9 that predate the B.2 "sole importer" rule).  The wave-open
  discipline is a **whitelist**: those 12 files are grandfathered as
  legacy importers; the sole *new* motor importer permitted from this
  wave forward is `services/data/repository.py`.  Later M11 waves
  (W3-W10) migrate the grandfathered files off direct motor imports
  onto Repository; the whitelist below shrinks monotonically.

  Any NEW motor importer added after M11-W1 wave-open (i.e. any file
  outside the whitelist below that imports motor.motor_asyncio or motor
  in any form) is a violation.

Test IDs (3):
  1. test_m11w1_data_repository_is_a_motor_importer
     (positive assertion: services/data/repository.py IS in the tree
      and does import motor.motor_asyncio — the sole *new* importer).
  2. test_m11w1_no_new_motor_importers_outside_grandfathered_or_data
     (AST negative scan: every file importing motor is either
      grandfathered OR is services/data/repository.py).
  3. test_m11w1_enforce_gate_is_sole_dual_importer_surface
     (Branch C rule: only files under services/enforce/*_gate.py may
      dual-import services.data.repository AND a
      services.platform_control_plane.* module in the same file.  W1
      lands the CHECK; W3+ lands the actual enforce files.)
"""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

# --- Repository / path constants --------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[3]  # .../repos/Extraction-Akki
BACKEND = REPO_ROOT / "backend"
DATA_REPOSITORY_PATH = BACKEND / "services" / "data" / "repository.py"

# --- Grandfathered legacy importers · banked at M11-W1 open · 2026-09-18 ---
# Path strings are relative to REPO_ROOT for stability.
GRANDFATHERED_LEGACY_MOTOR_IMPORTERS = frozenset({
    "backend/core.py",
    "backend/routers/s2_onboard.py",
    "backend/services/transform_forms/callable_skill_persistence.py",
    "backend/services/census_dimensions/dimensions_service.py",
    "backend/services/multi_instance/scoped_accessor.py",
    "backend/tests/registry/test_instance_fixture_b_walkthrough.py",
    "backend/tests/registry/test_instance_isolation.py",
    "backend/tests/conftest.py",
    "backend/tests/invariants/test_census_dimensions.py",
    "backend/tests/invariants/conftest.py",
})

# --- The sole new motor importer permitted by B.2 from M11-W1 forward ------
SOLE_NEW_MOTOR_IMPORTER = "backend/services/data/repository.py"

# --- Motor module prefixes checked as HARD ---------------------------------
_MOTOR_MODULE_PREFIXES = ("motor.motor_asyncio", "motor.core", "motor")


def _file_imports_motor(pyfile: Path) -> bool:
    """AST scan · returns True iff pyfile has any Import or ImportFrom
    node touching a `motor.*` module."""
    try:
        src = pyfile.read_text()
    except (OSError, UnicodeDecodeError):
        return False
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if any(alias.name == p or alias.name.startswith(p + ".")
                       for p in _MOTOR_MODULE_PREFIXES):
                    return True
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if any(mod == p or mod.startswith(p + ".")
                   for p in _MOTOR_MODULE_PREFIXES):
                return True
    return False


def _all_python_files_under_backend():
    """Yields every .py file under backend/, skipping __pycache__."""
    for p in BACKEND.rglob("*.py"):
        if "__pycache__" in p.parts:
            continue
        yield p


# --- Test 1: services/data/repository.py IS a motor importer ---------------

def test_m11w1_data_repository_is_a_motor_importer():
    """B.2 · the sole *new* importer must exist and must actually import motor."""
    assert DATA_REPOSITORY_PATH.exists(), (
        "M11-W1: services/data/repository.py must exist as the sole new "
        "Motor importer (v1.0 B.2)."
    )
    assert _file_imports_motor(DATA_REPOSITORY_PATH), (
        "M11-W1: services/data/repository.py must actually import "
        "motor.motor_asyncio; it is the sole new motor importer."
    )


# --- Test 2: no new motor importers outside grandfathered or data ---------

def test_m11w1_no_new_motor_importers_outside_grandfathered_or_data():
    """R-18 Tension (a) Option C: every file importing motor is either
    grandfathered legacy (whitelist) OR the sole new importer at
    services/data/repository.py.  Any other motor importer fails."""
    offenders = []
    for pyfile in _all_python_files_under_backend():
        try:
            rel = str(pyfile.relative_to(REPO_ROOT)).replace("\\", "/")
        except ValueError:
            continue
        if not _file_imports_motor(pyfile):
            continue
        if rel == SOLE_NEW_MOTOR_IMPORTER:
            continue
        if rel in GRANDFATHERED_LEGACY_MOTOR_IMPORTERS:
            continue
        offenders.append(rel)
    assert not offenders, (
        f"M11-W1: found {len(offenders)} NEW motor importer(s) outside "
        f"the wave-open whitelist ({SOLE_NEW_MOTOR_IMPORTER} + "
        f"{len(GRANDFATHERED_LEGACY_MOTOR_IMPORTERS)} grandfathered).  "
        f"Any new motor import must land inside services/data/repository.py; "
        f"grandfathered legacy files may only shrink, never grow."
    )


# --- Test 3: enforce/*_gate.py is sole dual-importer surface --------------

def _file_dual_imports_repo_and_pcp(pyfile: Path):
    """Returns True iff pyfile imports BOTH services.data.repository AND
    a services.platform_control_plane.* module in the same file."""
    try:
        src = pyfile.read_text()
    except (OSError, UnicodeDecodeError):
        return False
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    imports_repo = False
    imports_pcp = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod == "services.data.repository" or mod.startswith(
                "services.data.repository."
            ):
                imports_repo = True
            if mod == "services.platform_control_plane" or mod.startswith(
                "services.platform_control_plane."
            ):
                imports_pcp = True
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if (alias.name == "services.data.repository"
                        or alias.name.startswith("services.data.repository.")):
                    imports_repo = True
                if (alias.name == "services.platform_control_plane"
                        or alias.name.startswith(
                            "services.platform_control_plane.")):
                    imports_pcp = True
    return imports_repo and imports_pcp


def test_m11w1_enforce_gate_is_sole_dual_importer_surface():
    """Branch C rule: only `backend/services/enforce/**/*.py` may
    dual-import services.data.repository AND a
    services.platform_control_plane.* module in the same file.  Any
    other file that dual-imports is a violation."""
    offenders = []
    for pyfile in _all_python_files_under_backend():
        try:
            rel = str(pyfile.relative_to(REPO_ROOT)).replace("\\", "/")
        except ValueError:
            continue
        if not _file_dual_imports_repo_and_pcp(pyfile):
            continue
        # Permitted: any file under backend/services/enforce/
        if rel.startswith("backend/services/enforce/"):
            continue
        # Permitted: the tests that exercise the rule itself may exist
        # under backend/tests/ — they don't dual-import; nothing under
        # tests/ is expected here, so no test-directory exception is
        # granted (keeps the rule sharp).
        offenders.append(rel)
    assert not offenders, (
        f"M11-W1 Branch C: found {len(offenders)} file(s) outside "
        f"backend/services/enforce/ that dual-import "
        f"services.data.repository AND services.platform_control_plane.*.  "
        f"Only enforce/*_gate.py adapters may hold both imports."
    )
