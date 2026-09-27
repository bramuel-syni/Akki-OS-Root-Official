"""execution_components runtime bootstrap for RED-first component-binding contract tests."""

import sys
from pathlib import Path


runtime = Path(__file__).resolve().parents[2] / "vendored" / "extraction_akki" / "backend"
if not runtime.is_dir():
    raise RuntimeError("The vendored runtime source is missing; cannot run execution_components tests.")
if str(runtime) not in sys.path:
    sys.path.insert(0, str(runtime))
