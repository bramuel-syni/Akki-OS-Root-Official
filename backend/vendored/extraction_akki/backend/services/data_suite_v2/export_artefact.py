"""W-DATA-SUITE-V2-LIFT · CP-D6 · Export-artefact contract (DAP-Spec §A10).

Frozen carrier for the four DAP-A10 export required-fields:
rights_posture · derivation_hash · derivation_unit_refs · terms_cited.

Refusal is at the release gate (see `export_gate.py`), not at construction —
callers may hold an incomplete ExportArtefact in flight; the gate is where
DAP-A10 fires.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class ExportArtefact:
    rights_posture: str
    derivation_hash: str
    derivation_unit_refs: Sequence[str]
    terms_cited: Sequence[str]
