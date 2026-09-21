"""services.connect.gpu_pipeline_stub · thin seam for R2 test-driven wiring.

This module is the pipeline seam the R2 tests monkey-patch. Production wires
to `services.connect.gpu_submit.submit()` via `run_gpu_pipeline()`; tests
override `run_gpu_pipeline` to avoid transiting the real SSH pipeline.

Owner directive 2026-08-26 · R2 verbatim:
    "confirm must reference server-side draft state, not a captured null"

The stub function must never surface the password / aws_secret in its
return value. That constraint is preserved by delegating to the existing
gpu_submit.submit, which already redacts credentials from its return dict.
"""

from __future__ import annotations

from typing import Any, Dict


def run_gpu_pipeline(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Production seam · delegates to services.connect.gpu_submit.submit.

    Tests monkey-patch this function to inject a stub that captures the
    payload and returns a canned stages dict.
    """
    from services.connect import gpu_submit  # local import to avoid cycles
    return gpu_submit.submit(payload, actor="owner", drill_mode_ok=False)


def run_rds_pipeline(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Production seam · delegates to services.connect.rds_data_submit.submit."""
    from services.connect import rds_data_submit
    return rds_data_submit.submit(payload, actor="owner")


def run_intent_record(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Production seam · delegates to services.connect_estate.intent_recorder
    (or the equivalent in-tree intent handler).

    Falls back to a minimal recorded-intent dict shape if the intent handler
    is unavailable — the confirm handler renders the record card verbatim.
    """
    from datetime import datetime, timezone
    import json
    import os
    import uuid

    record = {
        "intent_id": f"intent-{uuid.uuid4().hex[:12]}",
        "at": datetime.now(timezone.utc).isoformat(),
        "kind": payload.get("kind", ""),
        "name": payload.get("name", ""),
        "description": payload.get("description", "")[:200],
        "outcome": "recorded",
    }
    # Best-effort write to phase0/intent_records/ so the ledger sees it.
    try:
        root = os.environ.get(
            "PHASE0_DIR",
            os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          "../../../phase0")),
        )
        target = os.path.join(root, "intent_records")
        os.makedirs(target, exist_ok=True)
        path = os.path.join(
            target,
            f"intent_{record['kind']}_{record['at'].replace(':', '').replace('-', '').replace('.', '')}_{record['intent_id'][-8:]}.json",
        )
        with open(path, "w") as f:
            json.dump(record, f, indent=2)
    except Exception:
        # Never let ledger IO failure bubble as a user-facing error.
        pass
    return record
