"""Standing frames for the direction (CIF) stage — owner ruling 2026-09-30 (3): routine commissions run under a confirmed frame
with operator-authored verdicts; non-routine commissions take candidate directions from CIF's ideas endpoint (not mounted here).
A frame names its family/voice and the standing candidate assemblies drawn from references/taxonomy.md; the producer instantiates
the verdict with brief-grounded rationale and a manifest generated from the brief (manifest_template.py)."""
from __future__ import annotations

from typing import Any, Dict, Optional

FRAMES: Dict[str, Dict[str, Any]] = {
    "FR-strategy-decide-v1": {
        "frame_id": "FR-strategy-decide-v1", "family": "strategy", "objective": "decide", "voice": "strategy-house",
        "confirmed_under": "owner ruling 2026-09-30 (3): operator-authored verdicts under standing frames for routine commissions",
        "routine_when": {"purpose.kind": "decide", "brand.house": "house-neutral"},
        "candidates": [
            {"idea_id": "D1", "name": "Evidence-led", "verdict": "adopt",
             "assembly": {"narrative": "recommendation-and-evidence", "compositions": ["cover", "exec_summary", "section", "assertion_exhibit", "assertion_points", "comparison", "coverage_limits", "appendix"],
                          "treatment": "restrained", "density": "sparse", "imagery": "none"},
             "rationale": "Audience priorities are {priorities}; every slide must carry a receipted exhibit.{read_ahead}"},
            {"idea_id": "D2", "name": "Future-state", "verdict": "defer",
             "assembly": {"narrative": "vision-then-journey", "compositions": ["cover", "hero", "big_number", "assertion_exhibit", "closing"], "treatment": "expressive", "density": "medium", "imagery": "abstract"},
             "conditions": "Re-enter when the purpose is to persuade or inspire a programme or all-hands audience rather than to decide."},
            {"idea_id": "D3", "name": "Human-centred", "verdict": "reject",
             "assembly": {"narrative": "stakeholder-journey", "compositions": ["cover", "persona", "journey", "benefits", "evidence"], "treatment": "warm", "density": "medium", "imagery": "photographic"},
             "rationale": "No stakeholder research exists in the content model; the direction would require evidence that does not exist."},
        ],
    },
}


def frame_for(brief: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """The standing frame whose routine conditions the brief meets, or None (non-routine → CIF ideas endpoint, not mounted)."""
    for frame in FRAMES.values():
        if all(_get(brief, path) == value for path, value in frame["routine_when"].items()):
            return frame
    return None


def _get(doc: Dict[str, Any], dotted: str):
    cur: Any = doc
    for key in dotted.split("."):
        cur = cur.get(key) if isinstance(cur, dict) else None
    return cur


def verdict_from_frame(frame: Dict[str, Any], brief: Dict[str, Any], verdict_id: str, manifest: list, confirmed_by: str, confirmed_at: str) -> Dict[str, Any]:
    read_ahead = " Read-ahead use means exhibits must be self-explaining." if brief["setting"].get("read_unattended") else ""
    fill = {"priorities": ", ".join(brief["audience"].get("priorities") or []) or "not stated", "read_ahead": read_ahead}
    candidates = []
    for c in frame["candidates"]:
        cand = {"idea_id": c["idea_id"], "name": c["name"], "assembly": c["assembly"], "verdict": c["verdict"]}
        if "rationale" in c:
            cand["rationale"] = c["rationale"].format(**fill)
        if "conditions" in c:
            cand["conditions"] = c["conditions"]
        candidates.append(cand)
    adopted = next(c["idea_id"] for c in candidates if c["verdict"] == "adopt")
    return {"verdict_id": verdict_id, "brief_ref": brief["brief_id"],
            "goal": f"Select a direction that lets {brief['audience']['who']} {brief['purpose']['kind']} from this pack: {brief['purpose']['statement']}",
            "frame_ref": frame["frame_id"], "candidates": candidates, "adopted": adopted, "manifest": manifest,
            "confirmed_by": confirmed_by, "confirmed_at": confirmed_at}
