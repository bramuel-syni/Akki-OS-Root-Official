"""doc-studio core: resolve specs into a frozen, literal build plan.

Everything a renderer needs is computed here once: text with references
substituted, numbers formatted, palette and type pair chosen by seed within the
voice's compatibility rules, layout zones converted from grid units to inches,
and the backend for every exhibit chosen from the plate policy. Renderers read
the resolved plan and nothing else, which is what makes rebuilds repeatable.
"""
import ast, hashlib, json, os, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKEN = re.compile(r"\{([A-Za-z_][A-Za-z0-9_.:]*)\}")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def dump(obj, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")


# ----------------------------------------------------------------------------
# Number formatting: one place, so every output agrees.
# ----------------------------------------------------------------------------
def fmt_value(v, unit, places=None):
    if unit == "GBPm":
        return f"£{v:,.1f}m"
    if unit == "GBP":
        return f"£{v:,.2f}"
    if unit == "pct":
        return f"{v*100:.{1 if places is None else places}f}%"
    if unit == "pp":
        return f"{v*100:.1f}pp"
    if unit == "m":
        return f"{v:,.1f}m"
    if unit in ("FTE",):
        return f"{int(round(v)):,}"
    if unit == "months":
        return f"{v:g}"
    if unit == "years":
        return f"{v:.1f}"
    if isinstance(v, float):
        return f"{v:,.1f}"
    return str(v)


def fmt_by_style(v, style):
    if style == "num1":
        return f"{v:,.1f}"
    if style == "int":
        return f"{int(round(v)):,}"
    if style == "pct":
        return f"{v*100:.1f}%"
    return str(v)


# ----------------------------------------------------------------------------
# Calculation evaluator: arithmetic only, names resolved from the content model.
# ----------------------------------------------------------------------------
class _Eval(ast.NodeVisitor):
    def __init__(self, names):
        self.names = names

    def visit_Expression(self, n):
        return self.visit(n.body)

    def visit_BinOp(self, n):
        a, b = self.visit(n.left), self.visit(n.right)
        if isinstance(n.op, ast.Add):
            return a + b
        if isinstance(n.op, ast.Sub):
            return a - b
        if isinstance(n.op, ast.Mult):
            return a * b
        if isinstance(n.op, ast.Div):
            return a / b
        raise ValueError("operator not allowed")

    def visit_UnaryOp(self, n):
        v = self.visit(n.operand)
        return -v if isinstance(n.op, ast.USub) else v

    def visit_Constant(self, n):
        return n.value

    def visit_Name(self, n):
        return self.names[n.id]

    def visit_Attribute(self, n):
        base = self.visit(n.value)
        return base[n.attr]

    def generic_visit(self, n):
        raise ValueError(f"not allowed in formula: {type(n).__name__}")


def evaluate(formula, names):
    return _Eval(names).visit(ast.parse(formula, mode="eval"))


class Content:
    """Read-side of the content model with reference resolution."""

    def __init__(self, data):
        self.d = data
        self.facts = data["facts"]
        self.series = data.get("series", {})
        self.options = data.get("options", {})
        self.calcs = data.get("calculations", {})
        self.claims = data.get("claims", {})
        self.receipts = data["receipts"]

    def fact_names(self):
        return {k: v["value"] for k, v in self.facts.items()}

    def calc(self, kid, option=None):
        k = self.calcs[kid]
        names = self.fact_names()
        if option is not None:
            names["option"] = self.options[option]
        return evaluate(k["formula"], names), k.get("unit")

    def resolve_token(self, tok):
        if tok.startswith("content."):
            return str(self.d[tok.split(".", 1)[1]])
        if tok in self.facts:
            f = self.facts[tok]
            return fmt_value(f["value"], f["unit"])
        if tok in self.calcs:
            v, unit = self.calc(tok)
            return fmt_value(v, unit)
        if tok in self.claims:
            return self.text(self.claims[tok]["text"])
        m = re.fullmatch(r"(K\d+):(min|max)", tok)
        if m:
            k = self.calcs[m.group(1)]
            vals = [self.calc(m.group(1), option=o)[0] for o in k["inputs"] if o in self.options]
            return fmt_value((min if m.group(2) == "min" else max)(vals), k.get("unit"))
        m = re.fullmatch(r"([A-Z]\d+):([A-Z]\d+):ratio", tok)
        if m:
            a, b = self.facts[m.group(1)]["value"], self.facts[m.group(2)]["value"]
            return f"{a/b*100:.0f}%"
        if "." in tok:
            oid, field = tok.split(".", 1)
            if oid in self.options:
                v = self.options[oid][field]
                return f"{v:,}" if isinstance(v, (int, float)) else str(v)
        raise KeyError(f"unresolvable reference {{{tok}}}")

    def text(self, s):
        if not isinstance(s, str):
            return s
        return TOKEN.sub(lambda m: self.resolve_token(m.group(1)), s)

    def receipt_for(self, rid):
        return self.receipts[rid]["resolves_to"]

    def claim_receipts(self, cid):
        out = []
        for sid in self.claims[cid].get("supports", []):
            src = self.facts.get(sid) or self.series.get(sid) or self.options.get(sid)
            if src and src.get("receipt") and src["receipt"] not in out:
                out.append(src["receipt"])
        return out


# ----------------------------------------------------------------------------
# Seeded selection inside the curated variation space.
# ----------------------------------------------------------------------------
def _idx(seed, axis, n):
    h = hashlib.sha256(f"{seed}:{axis}".encode()).hexdigest()
    return int(h[:8], 16) % n


def choose_look(theme, voice, brief, seed):
    vs = theme["variation_space"]
    comp = voice["compatibility"]
    palettes = [p for p in vs["palettes"] if p in comp["allowed_palettes"]]
    pairs = [p for p in vs["type_pairs"] if p in comp["allowed_type_pairs"]]
    covers = list(vs["cover_compositions"])
    dividers = list(vs["divider_treatments"])

    pi = _idx(seed, "palette", len(palettes))
    ti = _idx(seed, "type_pair", len(pairs))
    ci = _idx(seed, "cover", len(covers))
    di = _idx(seed, "divider", len(dividers))
    steps = []
    for _ in range(len(palettes) * len(pairs) * len(covers)):
        cand = {"palette": palettes[pi], "type_pair": pairs[ti], "cover": covers[ci]}
        veto = next((v for v in comp.get("veto", []) if all(cand.get(k) == v[k] for k in v if k != "why")), None)
        if veto is None:
            break
        steps.append({"vetoed": dict(cand), "why": veto["why"]})
        ti = (ti + 1) % len(pairs)  # step the cheapest axis first, deterministically
        if len(steps) % len(pairs) == 0:
            ci = (ci + 1) % len(covers)
    look = {
        "palette_id": palettes[pi], "palette": dict(vs["palettes"][palettes[pi]]),
        "type_pair_id": pairs[ti], "fonts": {**vs["type_pairs"][pairs[ti]], "number": theme["constant"]["type_roles"]["number"]},
        "cover_composition": covers[ci], "divider_treatment": dividers[di],
        "veto_steps": steps,
    }
    if brief["setting"].get("printed") and comp.get("printed_requires_field"):
        look["palette"]["field"] = comp["printed_requires_field"]
        look["printed_override"] = "field forced to printable white (M3)"
    return look


# ----------------------------------------------------------------------------
# Grid → inches.
# ----------------------------------------------------------------------------
def zone_inches(grid, z):
    W, H = grid["slide_w"], grid["slide_h"]
    mx, my, g = grid["margin_x"], grid["margin_y"], grid["gutter"]
    cw = (W - 2 * mx - g * (grid["cols"] - 1)) / grid["cols"]
    rh = (H - 2 * my) / grid["rows"]
    x = mx + z["col"] * (cw + g)
    w = z["span"] * cw + (z["span"] - 1) * g
    y = my + z["row"] * rh
    h = z["rspan"] * rh
    return {"x": round(x, 3), "y": round(y, 3), "w": round(w, 3), "h": round(h, 3)}


# ----------------------------------------------------------------------------
# Exhibit resolution shared by all formats.
# ----------------------------------------------------------------------------
def resolve_exhibit(ex, content, voice, fmt):
    plate = ex["plate"]
    pol = voice["plate_policy"][plate]
    s = content.series[ex["series_ref"]]
    return {
        "plate": plate, "backend": pol[fmt], "editable": pol["editable"],
        "label": s["label"], "categories": s["categories"], "values": s["values"],
        "unit": s["unit"], "class": s["class"], "receipt": s["receipt"],
        "receipt_text": content.receipt_for(s["receipt"]),
        "y_format": ex.get("y_format", "num"),
        "so_what": content.text(ex.get("so_what", "")),
        "caption": content.text(ex.get("caption", "")),
    }


def resolve_option_table(spec, content):
    cols = spec["columns"]
    rows = []
    for r in spec["rows"]:
        cells = []
        for oid in cols:
            if "field" in r:
                v = content.options[oid][r["field"]]
            else:
                v, _ = content.calc(r["calc"], option=oid)
            cells.append(fmt_by_style(v, r["format"]))
        rows.append({"label": r["label"], "cells": cells})
    receipts = sorted({content.options[o]["receipt"] for o in cols})
    classes = sorted({content.options[o]["class"] for o in cols})
    return {
        "columns": [content.options[o]["name"] for o in cols], "rows": rows,
        "receipts": receipts, "receipt_text": "; ".join(content.receipt_for(r) for r in receipts),
        "class": "/".join(classes), "so_what": content.text(spec.get("so_what", "")),
        "caption": content.text(spec.get("caption", "")),
    }


def coverage_block(content):
    c = content.d["coverage"]
    return {"covers": c["covers"], "cannot_say": c["cannot_say"]}


# ----------------------------------------------------------------------------
# Resolvers per spec type.
# ----------------------------------------------------------------------------
def _common(spec, content, brief, verdict, theme, voice):
    look = choose_look(theme, voice, brief, spec["seed"])
    return {
        "spec_id": spec["spec_id"], "spec_type": spec["spec_type"],
        "content_ref": spec["content_ref"], "brief_ref": spec["brief_ref"], "verdict_ref": spec["verdict_ref"],
        "direction": verdict["adopted"], "manifest_ids": [m["id"] for m in verdict["manifest"]],
        "voice": voice["voice_id"], "family": voice["family"], "seed": spec["seed"],
        "build_stamp": spec["build_stamp"], "look": look, "sizes_pt": voice["sizes_pt"],
        "title": content.text(content.d["title"]), "organisation": content.d["organisation"],
        "furniture": spec.get("furniture", {}),
    }


def resolve_deck(spec, content, brief, verdict, theme, voice):
    out = _common(spec, content, brief, verdict, theme, voice)
    grid = voice["grid"]
    out["slide_w"], out["slide_h"] = grid["slide_w"], grid["slide_h"]
    out["furniture_zones"] = {k: zone_inches(grid, z) for k, z in voice["layouts"]["furniture"].items()}
    slides = []
    for i, s in enumerate(spec["slides"], start=1):
        t = s["type"]
        zones = {k: zone_inches(grid, z) for k, z in voice["layouts"][t].items()}
        r = {"n": i, "type": t, "zones": zones}
        if t == "cover":
            r.update(title=content.text(s["title"]), subtitle=content.text(s["subtitle"]), org=content.text(s["org"]))
        elif t == "exec_summary":
            r.update(kicker=s["kicker"], title=content.text(s["title"]),
                     scqa=[("Situation", content.text(s["situation"])), ("Complication", content.text(s["complication"])),
                           ("Question", content.text(s["question"])), ("Answer", content.text(s["answer"]))])
        elif t == "section":
            r.update(number=s["number"], title=content.text(s["title"]))
        elif t == "assertion_exhibit":
            r.update(kicker=s["kicker"], title=content.text(s["title"]), exhibit=resolve_exhibit(s["exhibit"], content, voice, "pptx"))
        elif t == "assertion_points":
            r.update(kicker=s["kicker"], title=content.text(s["title"]), points=[content.text(p) for p in s["points"]])
        elif t == "comparison":
            r.update(kicker=s["kicker"], title=content.text(s["title"]), table=resolve_option_table(s, content))
        elif t == "coverage_limits":
            r.update(kicker="Coverage and limits", title=voice["structural"].get("coverage_title", "What this pack covers, what it cannot say, and what would close each gap"), coverage=coverage_block(content))
        elif t == "hero":
            r.update(kicker=s.get("kicker", ""), statement=content.text(s["statement"]))
            r["title"] = r["statement"]
        elif t == "closing":
            r.update(statement=content.text(s["statement"]), sub=content.text(s.get("sub", "")))
            r["title"] = r["statement"]
        elif t == "big_number":
            f = content.facts[s["fact_ref"]]
            r.update(kicker=s.get("kicker", ""), number=fmt_value(f["value"], f["unit"]), label=content.text(s["label"]),
                     exhibit={"plate": "big_number", "backend": voice["plate_policy"]["big_number"]["pptx"], "editable": True,
                              "class": f["class"], "receipt": f["receipt"], "receipt_text": content.receipt_for(f["receipt"]),
                              "so_what": content.text(s.get("so_what", ""))})
            r["title"] = r["label"]
        elif t == "appendix":
            r.update(kicker="Appendix", title="Exhibit index with receipts",
                     receipts=[{"id": k, "text": v["resolves_to"]} for k, v in sorted(content.receipts.items())])
        else:
            raise ValueError(f"unknown slide type {t}")
        r["title_chars"] = len(r.get("title", ""))
        slides.append(r)
    out["slides"] = slides
    return out


def resolve_paper(spec, content, brief, verdict, theme, voice):
    out = _common(spec, content, brief, verdict, theme, voice)
    out["subtitle"] = content.text(spec["subtitle"])
    secs = []
    for sec in spec["sections"]:
        blocks = []
        for b in sec["blocks"]:
            if "para" in b:
                blocks.append({"kind": "para", "text": content.text(b["para"])})
            elif "figure" in b:
                blocks.append({"kind": "figure", **resolve_exhibit(b["figure"], content, voice, "docx")})
            elif "table" in b:
                ex = resolve_exhibit({"plate": "bar", **b["table"]}, content, voice, "docx")
                blocks.append({"kind": "table", **ex})
            elif "options_table" in b:
                blocks.append({"kind": "options_table", **resolve_option_table(b["options_table"], content)})
            elif "coverage_limits" in b:
                blocks.append({"kind": "coverage", **coverage_block(content)})
            elif "receipts" in b:
                blocks.append({"kind": "receipts", "receipts": [{"id": k, "text": v["resolves_to"]} for k, v in sorted(content.receipts.items())]})
        secs.append({"heading": content.text(sec["heading"]), "blocks": blocks})
    out["sections"] = secs
    return out


def resolve_workbook(spec, content, brief, verdict, theme, voice):
    out = _common(spec, content, brief, verdict, theme, voice)
    sheets = []
    for sh in spec["sheets"]:
        r = {"name": sh["name"], "kind": sh["kind"]}
        if sh["kind"] == "inputs":
            r["facts"] = [{"id": fid, **content.facts[fid], "receipt_text": content.receipt_for(content.facts[fid]["receipt"])} for fid in sh["facts"]]
        elif sh["kind"] == "options_model":
            r["options"] = [{"id": oid, **content.options[oid], "receipt_text": content.receipt_for(content.options[oid]["receipt"])} for oid in sh["options"]]
            r["derived"] = sh["derived"]
        elif sh["kind"] == "series":
            r["series"] = [{"id": sid, **content.series[sid], "receipt_text": content.receipt_for(content.series[sid]["receipt"])} for sid in sh["series"]]
        sheets.append(r)
    out["sheets"] = sheets
    return out


RESOLVERS = {"deck": resolve_deck, "paper": resolve_paper, "workbook": resolve_workbook}


def resolve(spec_path, fixture_dir, out_dir):
    fixture_dir, out_dir = Path(fixture_dir), Path(out_dir)
    spec = load(spec_path)
    content_data = load(fixture_dir / "content.json")
    brief = load(fixture_dir / "brief.json")
    verdict = load(fixture_dir / "verdict.json")
    voice = load(ROOT / "voices" / f"{spec['voice']}.json")
    theme = load(ROOT / "themes" / f"{brief['brand']['house']}.json")
    cref = f"{content_data['content_id']}@{content_data['version']}"
    assert spec["content_ref"] == cref, f"spec points at {spec['content_ref']}, content is {cref}"
    assert verdict["verdict_id"] == spec["verdict_ref"], "spec/verdict mismatch"
    assert verdict["brief_ref"] == brief["brief_id"], "verdict/brief mismatch"
    content = Content(content_data)
    plan = RESOLVERS[spec["spec_type"]](spec, content, brief, verdict, theme, voice)
    plan["inputs_sha256"] = {
        p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in [Path(spec_path), fixture_dir / "content.json", fixture_dir / "brief.json", fixture_dir / "verdict.json",
                  ROOT / "voices" / f"{spec['voice']}.json", ROOT / "themes" / f"{brief['brand']['house']}.json"]
    }
    out = out_dir / f"{spec['spec_type']}.resolved.json"
    dump(plan, out)
    return out, plan


if __name__ == "__main__":
    import sys
    p, plan = resolve(sys.argv[1], sys.argv[2], sys.argv[3])
    print(f"resolved -> {p}  look={plan['look']['palette_id']}/{plan['look']['type_pair_id']}/{plan['look']['cover_composition']}")
