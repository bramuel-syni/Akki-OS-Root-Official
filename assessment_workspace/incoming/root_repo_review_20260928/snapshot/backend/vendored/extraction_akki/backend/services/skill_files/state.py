"""Skill Files state rollup · REFERENCE-NOT-COPY."""
from __future__ import annotations

from typing import Any, Dict, List

from services.skill_files import persistence


def rollup() -> Dict[str, Any]:
    rows = persistence.read_all()
    return {
        "ship_state": "populated" if rows else "empty",
        "count": len(rows),
        "skills": [
            {
                "skill_id": r.skill_id,
                "adapter_id": r.adapter_id,
                "training_run_id": r.training_run_id,
                "moac_card_id": r.moac_card_id,
                "recipe_version": r.recipe_version,
                "chain_length": len(r.provenance_chain),
                "provisioned_at": r.provisioned_at,
                "chain": [
                    {
                        "step_id": s.step_id,
                        "kind": s.kind,
                        "label": s.label,
                        "at": s.at,
                        "artifact_ref": s.artifact_ref,
                    }
                    for s in r.provenance_chain
                ],
            }
            for r in rows
        ],
    }
