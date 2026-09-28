"""services.baseline_line — CA1-004 baseline line records.

Doc 14 §32 + CA1-004 (Addendum §1): baseline line names licence-verified
starting model per training run. Attest against model_registry at
record time (unregistered starting model hard-fails).
"""
from services.baseline_line.records import (
    load_baseline_lines,
    record_baseline_line,
)

__all__ = ["record_baseline_line", "load_baseline_lines"]
