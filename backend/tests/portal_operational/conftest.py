"""portal_operational test runtime path bootstrap (RED contract suite)."""

import sys
from pathlib import Path


runtime = Path(__file__).resolve().parents[2] / "vendored" / "extraction_akki" / "backend"
if not runtime.is_dir():
    raise RuntimeError("The vendored runtime source is missing; cannot run portal_operational tests.")
sys.path.insert(0, str(runtime))
