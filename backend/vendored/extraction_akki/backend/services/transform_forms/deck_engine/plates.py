"""Plates are pure functions (data, tokens, register) → HTML/SVG fragments implementing plate law (DR-R3, DR-R6, DR-R8).
No LLM, no client-side charting runtime, no style field read from the spec. Every plate data schema is closed (extra='forbid'),
so accent/highlight/colour fields are unrepresentable (findings-never-selection). Null values need the explicit unmeasured marker."""
from __future__ import annotations

import html
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from contracts.deck_spec_v1 import FigureClass

Scalar = Union[int, float, str]


class _Closed(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class Unmeasured(_Closed):
    value: None = None
    unmeasured: bool = Field(..., description="must be true — the explicit marker that makes a blank honest (DR-R6)")
    caption: str = Field(..., min_length=1)


Cell = Union[Scalar, Unmeasured, None]


class P2Data(_Closed):  # assertion + supporting points
    bullets: List[str] = Field(..., min_length=1, max_length=6)


class P3Data(_Closed):  # table
    columns: List[str] = Field(..., min_length=1)
    rows: List[List[Cell]] = Field(..., min_length=1)
    unit: Optional[str] = None


class Bar(_Closed):
    label: str
    value: Union[int, float, None]
    unmeasured: bool = False
    caption: Optional[str] = None
    class_: FigureClass = Field(..., alias="class")
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)


class P4Data(_Closed):  # horizontal bars from plate law
    series: List[Bar] = Field(..., min_length=1, max_length=12)
    unit: Optional[str] = None


class P5Data(_Closed):  # comparison: options × criteria; no accent field can exist
    options: List[str] = Field(..., min_length=2)
    criteria: List[str] = Field(..., min_length=1)
    cells: List[List[Cell]] = Field(..., min_length=1)


class P17Data(_Closed):  # coverage & limits carries no data of its own; the spec's coverage_and_limits renders here
    pass


PLATE_SCHEMAS = {"P1": None, "P2": P2Data, "P3": P3Data, "P4": P4Data, "P5": P5Data, "P11": None, "P17": P17Data}
IMPLEMENTED = tuple(PLATE_SCHEMAS)


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def parse_plate_data(plate: str, data: Optional[Dict[str, Any]]):
    """Returns (model_or_None, errors[]) with rule ids per DR-R5."""
    if plate not in PLATE_SCHEMAS:
        return None, [{"rule": "plate_not_implemented", "message": f"plate {plate} has no renderer in engine v1 (implemented: {', '.join(IMPLEMENTED)})"}]
    schema = PLATE_SCHEMAS[plate]
    if schema is None:
        if data:
            return None, [{"rule": "plate_takes_no_data", "message": f"plate {plate} renders from figures/meta only; data must be absent"}]
        return None, []
    try:
        model = schema.model_validate(data or {})
    except ValidationError as exc:
        errors = []
        for e in exc.errors():
            loc = ".".join(str(p) for p in e["loc"])
            rule = "style_unrepresentable" if e["type"] == "extra_forbidden" else "plate_schema_invalid"
            errors.append({"rule": rule, "message": f"{plate}.{loc}: {e['msg']}"})
        return None, errors
    return model, blank_errors(plate, model)


def blank_errors(plate: str, model) -> List[Dict[str, str]]:
    """gate_no_silent_blank: a null cell/value without the unmeasured marker refuses."""
    errors = []
    grids = []
    if isinstance(model, P3Data):
        grids.append(("rows", model.rows))
    if isinstance(model, P5Data):
        grids.append(("cells", model.cells))
    for name, grid in grids:
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell is None:
                    errors.append({"rule": "no_silent_blank", "message": f"{plate}.{name}[{r}][{c}] is null without an unmeasured marker"})
                elif isinstance(cell, Unmeasured) and not cell.unmeasured:
                    errors.append({"rule": "no_silent_blank", "message": f"{plate}.{name}[{r}][{c}] marker must be unmeasured=true"})
    if isinstance(model, P4Data):
        for i, bar in enumerate(model.series):
            if bar.value is None and not bar.unmeasured:
                errors.append({"rule": "no_silent_blank", "message": f"{plate}.series[{i}] ({bar.label}) is null without unmeasured=true"})
            if bar.unmeasured and not bar.caption:
                errors.append({"rule": "no_silent_blank", "message": f"{plate}.series[{i}] ({bar.label}) unmeasured needs a caption"})
    return errors


# ----------------------------------------------------------------------------- rendering fragments

def chip(cls: str, tokens) -> str:
    colour = tokens["colour"][tokens["status"][cls]]
    return f'<span class="chip chip-{cls}" style="color:{colour};border-color:{colour}">{esc(cls)}</span>'


def hatched(caption: str, tokens, width: str = "100%", height: str = "1.4em") -> str:
    stroke, gap = tokens["hatch"]["stroke"], tokens["hatch"]["gap"]
    return (f'<span class="hatch" title="{esc(caption)}" style="display:inline-block;width:{width};height:{height};vertical-align:middle;'
            f'background:repeating-linear-gradient(135deg,{stroke} 0 1px,transparent 1px {gap}px)"></span><small class="hatch-caption">{esc(caption)}</small>')


def cell_html(cell: Cell, tokens) -> str:
    if isinstance(cell, Unmeasured):
        return hatched(cell.caption, tokens)
    return esc(cell)


def figure_html(figure, tokens) -> str:
    value = "—" if figure.value is None else f"{figure.value:,}" if isinstance(figure.value, (int, float)) and not isinstance(figure.value, bool) else str(figure.value)
    unit = f' <span class="unit">{esc(figure.unit)}</span>' if figure.unit else ""
    label = f'<span class="fig-label">{esc(figure.label)}</span>' if figure.label else ""
    return f'<div class="figure">{label}<b class="fig-value">{esc(value)}</b>{unit} {chip(figure.class_, tokens)}</div>'


def p2(model: P2Data, tokens, reg) -> str:
    return '<ul class="bullets">' + "".join(f"<li>{esc(b)}</li>" for b in model.bullets) + "</ul>"


def p3(model: P3Data, tokens, reg) -> str:
    head = "".join(f"<th>{esc(c)}</th>" for c in model.columns)
    body = "".join("<tr>" + "".join(f"<td>{cell_html(c, tokens)}</td>" for c in row) + "</tr>" for row in model.rows)
    unit = f'<caption>{esc(model.unit)}</caption>' if model.unit else ""
    return f'<table class="plate-table">{unit}<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def p4(model: P4Data, tokens, reg) -> str:
    w, row_h, label_w = 1040, 34, 260
    values = [b.value for b in model.series if b.value is not None]
    vmax = max([abs(v) for v in values] + [1])
    h = row_h * len(model.series) + 12
    parts = [f'<svg class="plate-svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="bar chart">',
             f'<defs><pattern id="hatch" patternUnits="userSpaceOnUse" width="{tokens["hatch"]["gap"]}" height="{tokens["hatch"]["gap"]}" patternTransform="rotate(45)">'
             f'<line x1="0" y1="0" x2="0" y2="{tokens["hatch"]["gap"]}" stroke="{tokens["hatch"]["stroke"]}" stroke-width="1"/></pattern></defs>']
    for i, bar in enumerate(model.series):
        y = 6 + i * row_h
        colour = tokens["colour"][tokens["status"][bar.class_]]
        parts.append(f'<text x="0" y="{y + 22}" font-family="{tokens["font"]["body"]}" font-size="{reg["body_px"] - 2}" fill="{tokens["colour"]["ink"]}">{esc(bar.label)}</text>')
        if bar.value is None:
            parts.append(f'<rect x="{label_w}" y="{y + 6}" width="{w - label_w - 200}" height="{row_h - 14}" fill="url(#hatch)" stroke="{tokens["hatch"]["stroke"]}"/>'
                         f'<text x="{w - 190}" y="{y + 22}" font-size="{reg["kicker_px"]}" fill="{tokens["colour"]["ink3"]}">{esc(bar.caption)}</text>')
        else:
            length = round((abs(bar.value) / vmax) * (w - label_w - 200), 2)
            parts.append(f'<rect x="{label_w}" y="{y + 6}" width="{length}" height="{row_h - 14}" fill="{colour}"/>'
                         f'<text x="{label_w + length + 8}" y="{y + 22}" font-size="{reg["body_px"] - 2}" fill="{tokens["colour"]["ink2"]}">{esc(f"{bar.value:,}")}{esc(" " + model.unit if model.unit else "")}</text>'
                         f'<text x="{w - 70}" y="{y + 22}" font-size="{reg["kicker_px"]}" fill="{colour}">{esc(bar.class_)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def p5(model: P5Data, tokens, reg) -> str:
    head = "<th></th>" + "".join(f"<th>{esc(o)}</th>" for o in model.options)
    body = "".join(f"<tr><th scope=\"row\">{esc(crit)}</th>" + "".join(f"<td>{cell_html(c, tokens)}</td>" for c in row) + "</tr>"
                   for crit, row in zip(model.criteria, model.cells))
    return f'<table class="plate-table plate-compare"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def p11(slide, tokens, reg) -> str:
    """One big number. class: estimated at landmark size is refused and demoted mechanically (DR-R6)."""
    fig = slide.figures[0]
    demoted = fig.class_ != "measured"
    size = reg["title_px"] + (18 if not demoted else 0)
    note = '<p class="demoted-note">Demoted: only a measured figure renders at landmark size.</p>' if demoted else ""
    value = "—" if fig.value is None else f"{fig.value:,}" if isinstance(fig.value, (int, float)) and not isinstance(fig.value, bool) else str(fig.value)
    return (f'<div class="big-number{" demoted" if demoted else ""}"><b style="font-size:{size}px">{esc(value)}</b>'
            f'<span class="unit">{esc(fig.unit or "")}</span> {chip(fig.class_, tokens)}{note}</div>')


def p17(coverage, tokens, reg) -> str:
    rows = "".join(f'<tr><td class="reason">{esc(l.reason)}</td><td>{esc(l.statement)}</td><td>{esc(l.closing_condition)}</td></tr>' for l in coverage.limits) \
        or '<tr><td colspan="3">No limits declared beyond the covered basis.</td></tr>'
    return (f'<p class="basis">Covered basis: <code>{esc(coverage.covered_basis_ref)}</code></p>'
            f'<table class="plate-table limits"><thead><tr><th>Reason</th><th>Statement</th><th>Closing condition</th></tr></thead><tbody>{rows}</tbody></table>')
