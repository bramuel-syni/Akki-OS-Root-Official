"""Reviewed extraction-runtime code shipped to an admitted runtime; never data, never secrets on disk."""
from functools import lru_cache
from services.census_autonomy.deep_bundle import build_bundle

MODULES = [
    'contracts/mtafiti_detection_signal.py',
    'services/mtafiti/executor/readonly_sql_guard.py',
    'services/mtafiti/detectors/pii_detector.py',
    'services/mtafiti/gpu_discovery_constants.py',
    'services/mtafiti/detectors/pii_redaction_guard.py',
    'services/extraction_runtime/worker_identity.py',
    'services/extraction_runtime/units.py',
    'services/extraction_runtime/inner_hop.py',
    'services/extraction_runtime/structured_records_worker.py',
    'services/extraction_runtime/skill_worker.py',
]


@lru_cache(maxsize=1)
def bundle():
    """(base64 zip, sha256). Cached per process; the hash is part of every receipt."""
    return build_bundle(MODULES)
