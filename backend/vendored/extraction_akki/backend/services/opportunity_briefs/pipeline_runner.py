"""services.opportunity_briefs.pipeline_runner
==============================================

W11 R4.5 · owner directive 2026-08-26 verbatim:

    "opportunity-briefs endpoint calls the generator/selector pipeline"

This module is the thin runner that stitches selector → generator →
brief_registry (in-memory) → Mongo persistence. The GET endpoint that
serves the frontend then reads both stores.

The runner is called by the new POST /api/registry/opportunity_briefs/
regenerate endpoint in routers/registry.py. It is invoked with a
census_dimensions map (owner-supplied · not census-derived at this
stage per the register's OB-R1 sequencing) and a registry_read_texts
map (also caller-supplied for now; when the Registry read API is
populated post-9.2b, the runner will source these from Registry).
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from services.opportunity_briefs.brief_selector import (
    SliceCandidate, enumerate_candidates,
)
from services.opportunity_briefs.generator import generate_one_brief
from services.opportunity_briefs.brief_registry import registry


async def run_pipeline(
    *,
    census_dimensions: Dict[str, List[str]],
    registry_read_texts: Dict[str, str],
    census_ref: str,
    regeneration_reason: str = "manual_regenerate",
    max_combined_order: int = 2,
    max_briefs: int = 10,
) -> Dict[str, Any]:
    """Run the full pipeline: enumerate candidates → generate one brief per
    candidate up to max_briefs → return telemetry summary.

    Returns:
      {
        "invoked": True,
        "at_iso": ISO-8601 UTC,
        "census_ref": <census_ref>,
        "candidates_enumerated": <int>,
        "briefs_written": <int>,
        "briefs_rejected": <int>,
        "results": [<telemetry_dict>, ...],
      }
    """
    candidates: List[SliceCandidate] = enumerate_candidates(
        census_dimensions,
        max_combined_order=max_combined_order,
    )
    written = 0
    rejected = 0
    results: List[Dict[str, Any]] = []

    for cand in candidates[:max_briefs]:
        brief_row, telem = await generate_one_brief(
            scope=cand.scope,
            contributing_slices=list(cand.contributing_slices),
            registry_read_texts=registry_read_texts,
            census_ref=census_ref,
            regeneration_reason=regeneration_reason,
        )
        if brief_row is not None:
            written += 1
        else:
            rejected += 1
        results.append(telem)

    return {
        "invoked": True,
        "at_iso": datetime.now(timezone.utc).isoformat(),
        "census_ref": census_ref,
        "candidates_enumerated": len(candidates),
        "briefs_written": written,
        "briefs_rejected": rejected,
        "results": results,
    }


def list_briefs_from_registry() -> List[Dict[str, Any]]:
    """Read all rows from the in-memory brief registry. The GET
    /api/registry/opportunity_briefs endpoint merges these with the
    Mongo `opportunity_briefs` collection so the frontend sees any
    briefs produced by the runner in-process."""
    reg = registry()
    if hasattr(reg, "_rows"):
        return [dict(row) for row in reg._rows.values()]  # pragma: no cover
    return []
