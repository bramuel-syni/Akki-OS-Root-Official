"""services.governance_plane — governance-plane primitives.

Contents:
  retention_policy.py            — W1b · CP1 · RetentionPolicy + four regimes + check_write_admissible
  cross_table_consistency.py     — M8 · CP-M8-CTCC-1 · preventive refusal contract for cross-table identifier reconstruction
"""
from __future__ import annotations

from .cross_table_consistency import (
    EmittedColumnRef,
    IdentifierClass,
    assess_reconstruction_risk,
    assert_no_cross_table_identifier_reconstruction,
    CrossTableIdentifierReconstructionRefused,
)

__all__ = [
    "EmittedColumnRef",
    "IdentifierClass",
    "assess_reconstruction_risk",
    "assert_no_cross_table_identifier_reconstruction",
    "CrossTableIdentifierReconstructionRefused",
]
