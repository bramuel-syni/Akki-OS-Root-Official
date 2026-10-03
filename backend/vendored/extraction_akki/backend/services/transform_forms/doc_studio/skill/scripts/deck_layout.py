"""Deterministic pagination for evidence that outgrows the frozen slide zones.

Uses the same font metrics as QA. Nothing is discarded or made smaller to hide
overflow; continued tables, coverage and receipts receive another slide.
"""
from copy import deepcopy

from qa import _font, wrap_lines


def height(text, width, size, name):
    font, kind = _font(name, size)
    slack = 1.10 if kind == "serif" else 1.0
    return sum(wrap_lines(line, font, width * 72 / slack) for line in str(text).split("\n")) * size * 1.2 / 72


def _groups(items, heights, capacity, fixed=0, gap=0):
    group, measures, used = [], [], fixed
    for item, h in zip(items, heights):
        if group and used + h + gap > capacity:
            yield group, measures
            group, measures, used = [], [], fixed
        group.append(item)
        measures.append(h)
        used += h + gap
    if group:
        yield group, measures


def paginate(plan):
    slides, sizes, fonts = [], plan["sizes_pt"], plan["look"]["fonts"]
    for source in plan["slides"]:
        sl = deepcopy(source)
        table = sl.get("table")
        if sl["type"] == "table":
            z = sl["zones"]["table"]
            rows, columns = table["rows"], table["columns"]
            weights = [max(1.0, min(3.0, max(len(str(r[c])) for r in [columns] + rows) / 14)) for c in range(len(columns))]
            widths = [z["w"] * w / sum(weights) for w in weights]
            size = sizes["table"] - (1 if len(columns) > 4 else 0) - (1 if len(rows) > 6 else 0)
            def row_height(row, header=False):
                return max(0.34, max(height(value, widths[c] - 0.12, size,
                                           fonts["body"] if header or c < table["right_align_from"] else fonts["number"])
                                     for c, value in enumerate(row)) + 0.12)
            header_h = row_height(columns, True)
            heights = [row_height(row) for row in rows]
            offset = 0
            for page_rows, row_heights in _groups(rows, heights, z["h"], fixed=header_h):
                page = deepcopy(sl)
                page["table"].update(rows=page_rows, raw_rows=table["raw_rows"][offset:offset + len(page_rows)],
                                     rows_from=table["rows_from"] + offset, column_widths=widths,
                                     row_heights=[header_h] + row_heights, font_size=size)
                slides.append(page)
                offset += len(page_rows)
        elif sl["type"] == "coverage_limits":
            z = sl["zones"]["body"]
            cover_h = max(0.9, height("COVERS\n" + sl["coverage"]["covers"], z["w"], sizes["body"], fonts["body"]) + 0.08)
            width = (z["w"] - 0.4) / 3 - 0.16
            min_h = round(3 * sizes["table"] * 1.25 / 72 + 0.18, 2)
            gaps = sl["coverage"]["cannot_say"]
            heights = [max(min_h, max(height(g[k], width, sizes["table"], fonts["body"]) for k in ("gap", "reason", "closes_with")) + 0.2) for g in gaps]
            for page_gaps, row_heights in _groups(gaps, heights, z["h"] - cover_h - 0.55, gap=0.1):
                page = deepcopy(sl)
                page["coverage"].update(cannot_say=page_gaps, row_heights=row_heights, cover_height=cover_h)
                slides.append(page)
        elif sl["type"] == "appendix":
            z, size = sl["zones"]["body"], sizes["body"] - 1
            heights = [max(0.4, height(r["text"], z["w"] - 1, size, fonts["body"]) + 0.12) for r in sl["receipts"]]
            for receipts, row_heights in _groups(sl["receipts"], heights, z["h"], gap=0.15):
                page = deepcopy(sl)
                page.update(receipts=receipts, receipt_heights=row_heights)
                slides.append(page)
        else:
            slides.append(sl)
    for n, sl in enumerate(slides, 1):
        sl["n"] = n
    plan["slides"] = slides
    return plan