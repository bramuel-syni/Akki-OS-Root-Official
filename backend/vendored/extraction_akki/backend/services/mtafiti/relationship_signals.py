"""Relationship-Signals Detector — CP6 kernel (name-based scaffold).

Emits `DetectionSignal` for FK-candidate name matches within a schema:
a column `<name>_id` in table `X` for which a table `<name>` exists in
the same schema → emit `signal.fk_candidate` with source_ref pointing
to `X.<name>_id → <name>.id` (candidate — never a verdict).

Owner ruling verbatim:
    "The learned component produces detections, never verdicts."

This is a NAME-BASED scaffold. GPU-embedding relationship signals are
the follow-on when the GPU dispatcher lands (deferred per honest-limit).
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

from contracts.mtafiti_detection_signal import DetectionSignal, EvidenceClass


_DETECTOR_VERSION = "fk-candidate-v0.1"


def detect_relationship_signals(per_table: Dict[str, Dict[str, Any]]) -> List[DetectionSignal]:
    """Return DetectionSignal per FK-candidate found in the census.

    per_table: {"schema.table": {columns: [{column_name, ...}, ...]}} — CP4 census output.
    """
    # Build set of table basenames per schema for O(1) lookup.
    tables_by_schema: Dict[str, set] = {}
    for key in per_table:
        sch, tbl = key.split(".", 1)
        tables_by_schema.setdefault(sch, set()).add(tbl)

    signals: List[DetectionSignal] = []
    for key, info in per_table.items():
        sch, tbl = key.split(".", 1)
        peer_tables = tables_by_schema.get(sch, set())
        for col in info.get("columns", []):
            name = col.get("column_name", "")
            m = re.match(r"^(.+)_id$", name)
            if not m:
                continue
            candidate = m.group(1)
            # Match if peer table basename equals candidate (exact) or plural (s / es)
            targets: List[str] = []
            if candidate in peer_tables:
                targets.append(candidate)
            if (candidate + "s") in peer_tables:
                targets.append(candidate + "s")
            if (candidate + "es") in peer_tables:
                targets.append(candidate + "es")
            # De-dup
            targets = list(dict.fromkeys(targets))
            for tgt in targets:
                signals.append(
                    DetectionSignal(
                        signal_name="signal.fk_candidate",
                        evidence_class=EvidenceClass.DETECTED,
                        confidence=0.85 if tgt == candidate else 0.65,
                        source_ref=f"{sch}.{tbl}.{name}->{sch}.{tgt}",
                        detector_version=_DETECTOR_VERSION,
                    )
                )
    return signals
