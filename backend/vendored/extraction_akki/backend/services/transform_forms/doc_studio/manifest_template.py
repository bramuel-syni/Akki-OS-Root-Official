"""Verdict manifest template (owner condition B): every commission's manifest is generated from that commission's brief —
never copied from a fixture. Each entry names the brief field it rests on (`source`), so revise.py's strike detection
watches exactly the assumptions this commission depends on. Classes follow references/directions.md (fact / recalled / inferred)."""
from __future__ import annotations

from typing import Any, Dict, List

TEMPLATE: List[Dict[str, Any]] = [
    {"id": "M1", "class": "fact", "source": "brief.purpose, brief.audience", "flips": ["density", "narrative", "exhibit_per_slide"],
     "assumption": "Audience is {audience.who}; the pack must let them {purpose.kind}"},
    {"id": "M2", "class": "fact", "source": "brief.setting.read_unattended",
     "when_true": {"assumption": "Pack is read unattended before it is presented", "flips": ["so_what_lines", "self_explaining_exhibits", "docx_output"]},
     "when_false": {"assumption": "Pack is presented live and not read unattended", "flips": ["so_what_brevity", "no_paper_output"]}},
    {"id": "M3", "class": "fact", "source": "brief.setting.printed",
     "when_true": {"assumption": "Pack will be printed", "flips": ["palette_field", "full_bleed_disallowed"]},
     "when_false": {"assumption": "Pack is screen-only", "flips": ["full_bleed_allowed"]}},
    {"id": "M4", "class": "recalled", "source": "brief.audience.knowledge", "flips": ["jargon_policy", "glossary_in_appendix"],
     "assumption": "Audience knowledge is {audience.knowledge}"},
    {"id": "M5", "class": "fact", "source": "brief.audience.priorities", "flips": ["exhibit_selection", "slide_order"],
     "assumption": "Audience priorities are {audience.priorities}"},
    {"id": "M6", "class": "inferred", "source": "house policy: findings not directives", "flips": ["comparison_plate_no_winner"],
     "assumption": "Every option is shown without a recommended winner", "only_if_options": True},
]


def _lookup(brief: Dict[str, Any], dotted: str) -> str:
    cur: Any = brief
    for key in dotted.split("."):
        cur = cur.get(key) if isinstance(cur, dict) else None
    return ", ".join(str(x) for x in cur) if isinstance(cur, list) else ("not stated" if cur in (None, "") else str(cur))


def _fill(text: str, brief: Dict[str, Any]) -> str:
    out, i = "", 0
    while True:
        start = text.find("{", i)
        if start < 0:
            return out + text[i:]
        end = text.find("}", start)
        out += text[i:start] + _lookup(brief, text[start + 1:end])
        i = end + 1


def manifest_from_brief(brief: Dict[str, Any], has_options: bool) -> List[Dict[str, Any]]:
    entries = []
    for t in TEMPLATE:
        if t.get("only_if_options") and not has_options:
            continue
        if "when_true" in t:
            field = t["source"].replace("brief.", "")
            branch = t["when_true"] if _lookup(brief, field) == "True" else t["when_false"]
            entries.append({"id": t["id"], "assumption": branch["assumption"], "class": t["class"], "source": t["source"], "flips": branch["flips"]})
        else:
            entries.append({"id": t["id"], "assumption": _fill(t["assumption"], brief), "class": t["class"], "source": t["source"], "flips": t["flips"]})
    return entries
