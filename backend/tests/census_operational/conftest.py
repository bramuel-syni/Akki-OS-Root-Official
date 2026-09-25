"""Resolve this slice's runtime package without changing production import paths."""
import sys
from pathlib import Path

runtime = Path(__file__).resolve().parents[2] / 'vendored' / 'extraction_akki' / 'backend'
if not runtime.is_dir():
    raise RuntimeError('The census runtime source is missing; cannot substitute another snapshot.')
sys.path.insert(0, str(runtime))