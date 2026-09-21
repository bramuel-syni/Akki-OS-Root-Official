"""Training state rollup · REFERENCE-NOT-COPY. Reads three on-disk artifacts:
  * compiled Demand Tables under TRAINING_DEMAND_TABLE_DIR.
  * capacity ledger JSONL under TRAINING_CAPACITY_LEDGER_DIR.
  * test-set seals under TRAINING_TEST_SET_SEAL_DIR.

Renders a JSON dict suitable for the ``/api/training/state`` endpoint and
the ``/training`` React surface. Never returns secrets — the read paths
strip AWS credentials by construction (they were never written by the
underlying modules).
"""
from __future__ import annotations

from typing import Any, Dict, List

from services.training import capacity_ledger, demand_table, test_set_seal


def rollup() -> Dict[str, Any]:
    """Assemble the training-plane surface state."""
    tables = demand_table.read_all()
    cap_rows = capacity_ledger.read_all()
    seals = test_set_seal.read_all_seals()

    ship_state = "empty"
    if tables or cap_rows or seals:
        ship_state = "populated"

    # Reduce capacity to a per-stratum-and-scheme count · REFERENCE-NOT-COPY.
    cap_summary: List[Dict[str, Any]] = []
    for e in cap_rows:
        cap_summary.append({
            "scheme_id": e.scheme_id,
            "stratum": e.stratum,
            "level": e.level,
            "state": e.state,
            "provenance_count": len(e.provenance),
            "marginal_gain": e.marginal_gain,
            "written_at": e.written_at,
        })

    return {
        "ship_state": ship_state,
        "demand_tables": [
            {
                "objective_id": t["objective_id"],
                "compiled_at": t["compiled_at"],
                "schemes_count": len(t.get("schemes", [])),
                "strata_count": len(t.get("per_stratum", [])),
                "per_stratum": t.get("per_stratum", []),
                "schemes": t.get("schemes", []),
            }
            for t in tables
        ],
        "capacity_ledger_rows": len(cap_rows),
        "capacity_ledger": cap_summary,
        "test_set_seals": [
            {
                "seal_id": s.get("seal_id"),
                "objective_id": s.get("objective_id"),
                "source_id": s.get("source_id"),
                "target_table": s.get("target_table"),
                "strata": s.get("strata", []),
                "sample_size": s.get("sample_size"),
                "manifest_sha256": s.get("manifest_sha256"),
                "sealed_at": s.get("sealed_at"),
                "rds_link_verified_at": s.get("rds_link_verified_at"),
            }
            for s in seals
        ],
    }
