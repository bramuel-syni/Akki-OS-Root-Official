"""Validate specs before resolving, and lint the resolved plans.

Two kinds of finding, kept apart on purpose:
- BLOCKER: measurable, fails the build. No judgment involved.
- REVIEW:  a question for the editorial/visual reviewer. Never fails the build.
"""
import json
import re
import sys
from pathlib import Path

import jsonschema

sys.path.insert(0, str(Path(__file__).parent))
from studio import ROOT, TOKEN, load  # noqa: E402

DIGITS = re.compile(r"(?<![A-Za-z{])\b\d[\d,]*\.?\d*\b(?![}\d])")
ALLOWED_LITERAL_NUMBERS = re.compile(r"^(FY\d\d|BP-\d{4}-\d\d|\d{1,2} (January|February|March|April|May|June|July|August|September|October|November|December) \d{4}|Q\d-\d{4}|\d{4}-\d\d-\d\d|v\d+|20\d\d|\d+ sites?|\d+ non-executive|\d+ executive)$")


def schema_check(kind, data):
    schema = load(ROOT / "schemas" / f"{kind}.schema.json")
    jsonschema.validate(data, schema)


def retyped_numbers(spec):
    """Numbers typed into a spec instead of referenced are the commonest way outputs drift apart."""
    found = []

    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("seed", "build_stamp", "spec_id", "content_ref", "brief_ref", "verdict_ref", "format", "field", "calc", "plate", "y_format", "formula", "number", "deck_id", "paper_id", "table_ref", "rows_from", "rows_to"):
                    continue
                walk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")
        elif isinstance(o, str):
            stripped = TOKEN.sub("", o)
            stripped = re.sub(r"^\d+\.\s", "", stripped)  # leading section ordinal
            for m in DIGITS.finditer(stripped):
                ctx = stripped[max(0, m.start() - 12): m.end() + 12]
                if any(ALLOWED_LITERAL_NUMBERS.match(chunk.strip(" ,.;")) for chunk in re.findall(r"[^,;]+", ctx)):
                    continue
                if re.search(r"(FY|BP-|Q\d-|v)\d", ctx) or re.search(r"\d{4}", m.group()) or re.search(r"\d+ (sites?|non-executive|executive|October|minutes)", ctx):
                    continue
                found.append(f"{path}: literal number '{m.group()}' in \"{o[:60]}\"")
    walk(spec, spec.get("spec_type", "spec"))
    return found


def lint_plan(plan, voice):
    blockers, review = [], []
    st = voice["structural"]
    if plan["spec_type"] == "deck":
        types = [s["type"] for s in plan["slides"]]
        for req in st["requires"]:
            if req not in types:
                blockers.append(f"voice requires a '{req}' slide; none present")
        for s in plan["slides"]:
            t = s.get("title", "")
            if s["type"] not in ("cover", "section", "closing", "big_number", "table", "glossary") and len(t) > st["title_max_chars"]:
                blockers.append(f"slide {s['n']}: title {len(t)} chars > {st['title_max_chars']}")
            ex = s.get("exhibit") or s.get("table")
            if ex:
                if not ex.get("receipt") and not ex.get("receipts"):
                    blockers.append(f"slide {s['n']}: exhibit has no receipt")
                if not ex.get("class"):
                    blockers.append(f"slide {s['n']}: figure class missing")
                if st.get("so_what_required_on_exhibits") and not ex.get("so_what"):
                    blockers.append(f"slide {s['n']}: exhibit has no so-what")
            if s["type"] == "comparison" and st.get("no_winner_marked"):
                if any(w in json.dumps(s).lower() for w in ("recommended", "preferred", "winner", "✓")):
                    blockers.append(f"slide {s['n']}: comparison marks a winner; this voice presents options without one")
            if s["type"] not in ("cover", "section") and s["type"] != "exec_summary" and t and not re.search(r"[a-z]", t[:1]):
                pass
            if s["type"] == "table" and (len(s["table"]["rows"]) > 9 or len(s["table"]["columns"]) > 7):
                blockers.append(f"slide {s['n']}: evidence table {s['table']['id']} has {len(s['table']['rows'])} rows × {len(s['table']['columns'])} columns; paginate to ≤ 9 rows × 7 columns per slide")
            if s["type"] == "glossary" and len(s["terms"]) > 6:
                blockers.append(f"slide {s['n']}: glossary slide carries {len(s['terms'])} terms; paginate to ≤ 6 per slide")
            if s["type"] in ("assertion_exhibit", "assertion_points", "comparison"):
                if not re.search(r"\s(is|are|was|were|has|have|cost|costs|grew|fell|runs|stays|means|carry|carries|outrun|outruns|outrunning)\b", t):
                    review.append(f"slide {s['n']}: is the title a full-sentence assertion? \"{t}\"")
            words = len(json.dumps({k: v for k, v in s.items() if k in ("title", "points", "scqa", "exhibit", "table")}).split())
            if words > st["words_per_slide_max"] * 2.2:
                review.append(f"slide {s['n']}: dense ({words} tokens); consider splitting")
        review.append("Read only the titles in order: do they tell the whole story?")
        review.append("Does each exhibit prove its title, or merely decorate it?")
    if plan["spec_type"] == "paper":
        for sec in plan["sections"]:
            for b in sec["blocks"]:
                if b["kind"] in ("figure", "table", "options_table", "rows_table"):
                    if not (b.get("receipt") or b.get("receipts")):
                        blockers.append(f"paper section '{sec['heading']}': exhibit without receipt")
        review.append("Does the paper read as an argument when read unattended, without the deck?")
    if plan["spec_type"] == "workbook":
        review.append("Are the yellow key assumptions the ones the board would want to change?")
    return blockers, review


def main(fixture_dir, resolved_dir):
    fixture_dir, resolved_dir = Path(fixture_dir), Path(resolved_dir)
    blockers, review = [], []
    for kind, fn in (("content", "content.json"), ("brief", "brief.json"), ("verdict", "verdict.json")):
        schema_check(kind, load(fixture_dir / fn))
    verdict = load(fixture_dir / "verdict.json")
    if verdict["adopted"] not in {c["idea_id"] for c in verdict["candidates"] if c["verdict"] == "adopt"}:
        blockers.append("verdict: adopted direction is not a candidate with verdict=adopt")
    if not verdict.get("confirmed_by"):
        blockers.append("verdict: no confirmer recorded (CIF coach seat)")
    for spec_file in sorted(fixture_dir.glob("*.json")):
        spec = load(spec_file)
        if "spec_type" not in spec:
            continue
        schema_check(spec["spec_type"], spec)
        blockers += retyped_numbers(spec)
        plan_path = resolved_dir / f"{spec['spec_type']}.resolved.json"
        if plan_path.exists():
            voice = load(ROOT / "voices" / f"{spec['voice']}.json")
            b, r = lint_plan(load(plan_path), voice)
            blockers += b
            review += r
    report = {"blockers": blockers, "review": review, "status": "FAIL" if blockers else "PASS"}
    (resolved_dir / "validate-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
