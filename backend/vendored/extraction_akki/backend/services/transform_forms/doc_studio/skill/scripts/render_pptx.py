"""Render a resolved deck plan to .pptx with python-pptx.

This file makes no design decisions. Colours, fonts, sizes and zones all come
from the plan. Keep it that way: any judgment added here escapes the frozen
specification and breaks repeatability.
"""
import sys
from pathlib import Path

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

sys.path.insert(0, str(Path(__file__).parent))
from studio import load  # noqa: E402


def rgb(h):
    return RGBColor.from_string(h)


class Deck:
    def __init__(self, plan):
        self.p = plan
        self.look = plan["look"]
        self.pal = self.look["palette"]
        self.fonts = self.look["fonts"]
        self.sz = plan["sizes_pt"]
        self.prs = Presentation()
        self.prs.slide_width = Inches(plan["slide_w"])
        self.prs.slide_height = Inches(plan["slide_h"])
        self.blank = self.prs.slide_layouts[6]

    # -- primitives ---------------------------------------------------------
    def slide(self, field=None):
        s = self.prs.slides.add_slide(self.blank)
        bg = s.background.fill
        bg.solid()
        bg.fore_color.rgb = rgb(field or self.pal["field"])
        return s

    def text(self, s, z, txt, size, font=None, color=None, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False):
        tb = s.shapes.add_textbox(Inches(z["x"]), Inches(z["y"]), Inches(z["w"]), Inches(z["h"]))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = anchor
        lines = txt if isinstance(txt, list) else [txt]
        for i, line in enumerate(lines):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = align
            run = para.add_run()
            run.text = line
            f = run.font
            f.size = Pt(size)
            f.name = font or self.fonts["body"]
            f.bold = bold
            f.italic = italic
            f.color.rgb = rgb(color or self.pal["structure"])
        return tb

    def rule(self, s, x, y, w, color=None, weight=0.75):
        ln = s.shapes.add_connector(1, Inches(x), Inches(y), Inches(x + w), Inches(y))
        ln.line.color.rgb = rgb(color or self.pal["rule"])
        ln.line.width = Pt(weight)
        return ln

    def furniture(self, s, n):
        fz = self.p["furniture_zones"]
        fu = self.p["furniture"]
        muted = self.pal["muted"]
        self.text(s, fz["doc_id"], fu.get("deck_id", self.p["spec_id"]), self.sz["small"], color=muted, anchor=MSO_ANCHOR.BOTTOM)
        self.text(s, fz["confidentiality"], fu.get("confidentiality", ""), self.sz["small"], color=muted, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM)
        self.text(s, fz["page_no"], str(n), self.sz["small"], font=self.fonts["number"], color=muted, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.BOTTOM)

    def header(self, s, sl):
        z = sl["zones"]
        self.text(s, z["kicker"], sl["kicker"].upper(), self.sz["kicker"], color=self.pal["muted"], bold=True)
        self.text(s, z["title"], sl["title"], self.sz["title"], font=self.fonts["title"], anchor=MSO_ANCHOR.TOP)

    def badge_and_receipt(self, s, z_receipt, cls, receipt_text, receipt_ids):
        line = f"[{cls}]  Receipt {', '.join(receipt_ids)}: {receipt_text}"
        self.text(s, z_receipt, line, self.sz["small"], font=self.fonts["number"], color=self.pal["muted"], anchor=MSO_ANCHOR.BOTTOM)

    # -- slide types ---------------------------------------------------------
    def cover(self, sl):
        s = self.slide()
        z = sl["zones"]
        self.text(s, z["title"], sl["title"], self.sz["cover_title"], font=self.fonts["title"], anchor=MSO_ANCHOR.BOTTOM)
        self.text(s, z["subtitle"], sl["subtitle"], self.sz["cover_sub"], color=self.pal["muted"])
        self.text(s, z["org"], f'{sl["org"]}  ·  {self.p["furniture"].get("confidentiality", "")}', self.sz["small"], color=self.pal["muted"])
        return s

    def exec_summary(self, sl):
        s = self.slide()
        self.header(s, sl)
        z = sl["zones"]["body"]
        n = len(sl["scqa"])
        rowh = z["h"] / n
        for i, (label, body) in enumerate(sl["scqa"]):
            y = z["y"] + i * rowh
            self.text(s, {"x": z["x"], "y": y, "w": 1.6, "h": rowh - 0.15}, label.upper(), self.sz["kicker"], bold=True,
                      color=self.pal["accent"] if label == "Answer" else self.pal["muted"])
            self.text(s, {"x": z["x"] + 1.8, "y": y, "w": z["w"] - 1.8, "h": rowh - 0.15}, body, self.sz["body"])
            if i < n - 1:
                self.rule(s, z["x"], y + rowh - 0.08, z["w"])
        self.furniture(s, sl["n"])
        return s

    def section(self, sl):
        inverted = self.look["divider_treatment"] == "inverted-field"
        s = self.slide(self.pal["structure"] if inverted else None)
        z = sl["zones"]
        fg = self.pal["field"] if inverted else self.pal["accent"]
        self.text(s, z["number"], f'{sl["number"]:02d}', self.sz["section_number"], font=self.fonts["number"], color=fg, anchor=MSO_ANCHOR.MIDDLE)
        self.text(s, z["title"], sl["title"], self.sz["section_title"], font=self.fonts["title"],
                  color=self.pal["field"] if inverted else self.pal["structure"], anchor=MSO_ANCHOR.MIDDLE)
        return s

    def chart(self, s, z, ex):
        cd = CategoryChartData()
        cd.categories = ex["categories"]
        for name, vals in ex["values"].items():
            cd.add_series(name, vals)
        ctype = {"bar": XL_CHART_TYPE.COLUMN_CLUSTERED, "line": XL_CHART_TYPE.LINE_MARKERS, "stacked_bar": XL_CHART_TYPE.COLUMN_STACKED}[ex["plate"]]
        gf = s.shapes.add_chart(ctype, Inches(z["x"]), Inches(z["y"]), Inches(z["w"]), Inches(z["h"]), cd)
        ch = gf.chart
        ch.has_legend = len(ex["values"]) > 1
        if ch.has_legend:
            ch.legend.position = XL_LEGEND_POSITION.BOTTOM
            ch.legend.include_in_layout = False
        ch.font.name = self.fonts["body"]
        ch.font.size = Pt(self.sz["small"] + 1)
        ch.font.color.rgb = rgb(self.pal["muted"])
        numfmt = {"pct": "0.0%", "gbp": "£0.00", "num": "#,##0.0"}[ex["y_format"]]
        va = ch.value_axis
        va.has_major_gridlines = True
        va.major_gridlines.format.line.color.rgb = rgb(self.pal["rule"])
        va.format.line.fill.background()
        va.tick_labels.number_format = numfmt
        va.tick_labels.number_format_is_linked = False
        va.tick_labels.font.name = self.fonts["number"]
        ca = ch.category_axis
        ca.format.line.color.rgb = rgb(self.pal["rule"])
        ca.has_major_gridlines = False
        plot = ch.plots[0]
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.number_format = numfmt
        dl.number_format_is_linked = False
        dl.font.name = self.fonts["number"]
        dl.font.size = Pt(self.sz["small"] + 1)
        dl.font.color.rgb = rgb(self.pal["structure"])
        dl.position = XL_LABEL_POSITION.OUTSIDE_END if ex["plate"] != "line" else XL_LABEL_POSITION.ABOVE
        if ex["plate"] != "line":
            plot.gap_width = 80
        for i, ser in enumerate(plot.series):
            col = self.pal["accent"] if i == 0 else self.pal["muted"]
            if ex["plate"] == "line":
                ser.format.line.color.rgb = rgb(col)
                ser.format.line.width = Pt(2.25)
                ser.smooth = False
                ser.marker.format.fill.solid()
                ser.marker.format.fill.fore_color.rgb = rgb(col)
                ser.marker.format.line.color.rgb = rgb(col)
            else:
                ser.format.fill.solid()
                ser.format.fill.fore_color.rgb = rgb(col)
        return gf

    def assertion_exhibit(self, sl):
        s = self.slide()
        self.header(s, sl)
        z = sl["zones"]
        ex = sl["exhibit"]
        if ex["backend"] in ("native", "native-stacked"):
            self.chart(s, z["exhibit"], ex)
        else:
            raise NotImplementedError(f"backend {ex['backend']} for {ex['plate']} in pptx")
        if ex["so_what"]:
            self.text(s, z["so_what"], ex["so_what"], self.sz["body"], color=self.pal["accent"], italic=True, anchor=MSO_ANCHOR.BOTTOM)
        self.badge_and_receipt(s, z["receipt"], ex["class"], ex["receipt_text"], [ex["receipt"]])
        self.furniture(s, sl["n"])
        return s

    def assertion_points(self, sl):
        s = self.slide()
        self.header(s, sl)
        z = sl["zones"]["points"]
        n = len(sl["points"])
        rowh = min(1.3, z["h"] / n)
        for i, ptxt in enumerate(sl["points"]):
            y = z["y"] + i * rowh
            self.text(s, {"x": z["x"], "y": y, "w": 0.7, "h": rowh}, f"{i+1:02d}", self.sz["title"], font=self.fonts["number"], color=self.pal["accent"])
            self.text(s, {"x": z["x"] + 0.9, "y": y + 0.08, "w": z["w"] - 0.9, "h": rowh - 0.1}, ptxt, self.sz["body"])
            self.rule(s, z["x"], y + rowh - 0.12, z["w"])
        self.furniture(s, sl["n"])
        return s

    def comparison(self, sl):
        s = self.slide()
        self.header(s, sl)
        z = sl["zones"]["table"]
        t = sl["table"]
        ncol = len(t["columns"]) + 1
        nrow = len(t["rows"]) + 1
        shape = s.shapes.add_table(nrow, ncol, Inches(z["x"]), Inches(z["y"]), Inches(z["w"]), Inches(min(z["h"], 0.5 * nrow)))
        tbl = shape.table
        tbl.first_row = True
        label_w = z["w"] * 0.28
        tbl.columns[0].width = Inches(label_w)
        for c in range(1, ncol):
            tbl.columns[c].width = Inches((z["w"] - label_w) / (ncol - 1))

        def cell(r, c, txt, bold=False, font=None, color=None, align=PP_ALIGN.LEFT, fill=None):
            ce = tbl.cell(r, c)
            ce.fill.solid()
            ce.fill.fore_color.rgb = rgb(fill or self.pal["field"])
            ce.margin_left = ce.margin_right = Inches(0.08)
            tf = ce.text_frame
            tf.word_wrap = True
            para = tf.paragraphs[0]
            para.alignment = align
            run = para.add_run()
            run.text = txt
            run.font.size = Pt(self.sz["table"])
            run.font.bold = bold
            run.font.name = font or self.fonts["body"]
            run.font.color.rgb = rgb(color or self.pal["structure"])

        cell(0, 0, "", fill=self.pal["hatch"])
        for c, name in enumerate(t["columns"], start=1):
            cell(0, c, name, bold=True, fill=self.pal["hatch"])
        for r, row in enumerate(t["rows"], start=1):
            cell(r, 0, row["label"], color=self.pal["muted"])
            for c, v in enumerate(row["cells"], start=1):
                cell(r, c, v, font=self.fonts["number"], align=PP_ALIGN.RIGHT)
        if t["so_what"]:
            self.text(s, sl["zones"]["so_what"], t["so_what"], self.sz["body"], color=self.pal["accent"], italic=True, anchor=MSO_ANCHOR.BOTTOM)
        self.badge_and_receipt(s, sl["zones"]["receipt"], t["class"], t["receipt_text"], t["receipts"])
        self.furniture(s, sl["n"])
        return s

    def table(self, sl):
        """v1.3 evidence table: exact locations, decisions, per-language rows — text columns left, numeric columns right."""
        s = self.slide()
        self.header(s, sl)
        z = sl["zones"]["table"]
        t = sl["table"]
        ncol, nrow = len(t["columns"]), len(t["rows"]) + 1
        shape = s.shapes.add_table(nrow, ncol, Inches(z["x"]), Inches(z["y"]), Inches(z["w"]), Inches(min(z["h"], 0.42 * nrow)))
        tbl = shape.table
        tbl.first_row = True
        weights = [max(1.0, min(3.0, max(len(str(r[c])) for r in [t["columns"]] + t["rows"]) / 14)) for c in range(ncol)]
        total = sum(weights)
        for c in range(ncol):
            tbl.columns[c].width = Inches(z["w"] * weights[c] / total)
        size = self.sz["table"] - (1 if ncol > 4 else 0) - (1 if nrow > 7 else 0)

        def cell(r, c, txt, bold=False, font=None, color=None, align=PP_ALIGN.LEFT, fill=None):
            ce = tbl.cell(r, c)
            ce.fill.solid()
            ce.fill.fore_color.rgb = rgb(fill or self.pal["field"])
            ce.margin_left = ce.margin_right = Inches(0.06)
            ce.margin_top = ce.margin_bottom = Inches(0.03)
            tf = ce.text_frame
            tf.word_wrap = True
            para = tf.paragraphs[0]
            para.alignment = align
            run = para.add_run()
            run.text = txt
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.name = font or self.fonts["body"]
            run.font.color.rgb = rgb(color or self.pal["structure"])

        for c, name in enumerate(t["columns"]):
            cell(0, c, name, bold=True, fill=self.pal["hatch"])
        for r, row in enumerate(t["rows"], start=1):
            for c, v in enumerate(row):
                numeric = c >= t["right_align_from"]
                cell(r, c, v, font=self.fonts["number"] if numeric else None, align=PP_ALIGN.RIGHT if numeric else PP_ALIGN.LEFT)
        if t["so_what"]:
            self.text(s, sl["zones"]["so_what"], t["so_what"], self.sz["body"], color=self.pal["accent"], italic=True, anchor=MSO_ANCHOR.BOTTOM)
        self.badge_and_receipt(s, sl["zones"]["receipt"], t["class"], t["receipt_text"], t["receipts"])
        self.furniture(s, sl["n"])
        return s

    def glossary(self, sl):
        """v1.3 plain-English terms: the term in the number column's place, its meaning beside it."""
        s = self.slide()
        self.header(s, sl)
        z = sl["zones"]["points"]
        n = max(1, len(sl["terms"]))
        rowh = min(1.3, z["h"] / n)
        termw = min(2.6, z["w"] * 0.28)
        for i, term in enumerate(sl["terms"]):
            y = z["y"] + i * rowh
            self.text(s, {"x": z["x"], "y": y + 0.06, "w": termw, "h": rowh - 0.1}, term["term"], self.sz["body"], bold=True, color=self.pal["accent"])
            self.text(s, {"x": z["x"] + termw + 0.2, "y": y + 0.06, "w": z["w"] - termw - 0.2, "h": rowh - 0.1}, term["meaning"], self.sz["body"] - 1)
            self.rule(s, z["x"], y + rowh - 0.08, z["w"])
        self.furniture(s, sl["n"])
        return s

    def coverage_limits(self, sl):
        s = self.slide()
        self.header(s, sl)
        z = sl["zones"]["body"]
        cov = sl["coverage"]
        self.text(s, {"x": z["x"], "y": z["y"], "w": z["w"], "h": 0.9}, ["COVERS", cov["covers"]], self.sz["body"])
        y = z["y"] + 1.0
        colw = (z["w"] - 0.4) / 3
        for i, h in enumerate(["CANNOT SAY", "WHY", "WHAT WOULD CLOSE IT"]):
            self.text(s, {"x": z["x"] + i * (colw + 0.2), "y": y, "w": colw, "h": 0.3}, h, self.sz["kicker"], bold=True, color=self.pal["muted"])
        self.rule(s, z["x"], y + 0.32, z["w"], color=self.pal["structure"])
        y += 0.45
        ts = self.sz["table"]
        row_h = round(3 * ts * 1.25 / 72 + 0.18, 2)  # room for three wrapped lines at the table size
        for gap in cov["cannot_say"]:
            box = s.shapes.add_shape(1, Inches(z["x"]), Inches(y), Inches(z["w"]), Inches(row_h))
            box.fill.patterned()
            box.fill.fore_color.rgb = rgb(self.pal["hatch"])
            box.fill.back_color.rgb = rgb(self.pal["field"])
            box.line.fill.background()
            for i, key in enumerate(["gap", "reason", "closes_with"]):
                self.text(s, {"x": z["x"] + i * (colw + 0.2) + 0.08, "y": y + 0.08, "w": colw - 0.16, "h": row_h - 0.14}, gap[key], ts)
            y += row_h + 0.1
        self.furniture(s, sl["n"])
        return s

    def hero(self, sl):
        s = self.slide(self.pal["structure"])
        z = sl["zones"]
        if sl.get("kicker"):
            self.text(s, z["kicker"], sl["kicker"].upper(), self.sz["kicker"], color=self.pal["accent"], bold=True)
        self.text(s, z["statement"], sl["statement"], self.sz["hero"], font=self.fonts["title"], color=self.pal["field"], anchor=MSO_ANCHOR.MIDDLE)
        return s

    def closing(self, sl):
        s = self.slide(self.pal["structure"])
        z = sl["zones"]
        self.text(s, z["statement"], sl["statement"], self.sz["closing"], font=self.fonts["title"], color=self.pal["field"], anchor=MSO_ANCHOR.MIDDLE)
        if sl.get("sub"):
            self.text(s, z["sub"], sl["sub"], self.sz["body"], color=self.pal["muted"])
        return s

    def big_number(self, sl):
        s = self.slide()
        z = sl["zones"]
        ex = sl["exhibit"]
        self.text(s, z["kicker"], sl["kicker"].upper(), self.sz["kicker"], color=self.pal["muted"], bold=True, align=PP_ALIGN.CENTER)
        self.text(s, z["number"], sl["number"], self.sz["big_number"], font=self.fonts["number"], color=self.pal["accent"], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        self.text(s, z["label"], sl["label"], self.sz["body"], align=PP_ALIGN.CENTER)
        if ex["so_what"]:
            self.text(s, z["so_what"], ex["so_what"], self.sz["body"], color=self.pal["muted"], italic=True, align=PP_ALIGN.CENTER)
        self.badge_and_receipt(s, z["receipt"], ex["class"], ex["receipt_text"], [ex["receipt"]])
        self.furniture(s, sl["n"])
        return s

    def appendix(self, sl):
        s = self.slide()
        self.header(s, sl)
        z = sl["zones"]["body"]
        y = z["y"]
        size = self.sz["body"] - 1
        chars_per_line = max(40, int((z["w"] - 1.0) * 72 / (size * 0.5)))
        for r in sl["receipts"]:
            lines = max(1, -(-len(r["text"]) // chars_per_line))
            h = max(0.4, round(lines * size * 1.2 / 72 + 0.12, 2))
            self.text(s, {"x": z["x"], "y": y, "w": 0.9, "h": h}, r["id"], self.sz["body"], font=self.fonts["number"], color=self.pal["accent"], bold=True)
            self.text(s, {"x": z["x"] + 1.0, "y": y, "w": z["w"] - 1.0, "h": h}, r["text"], size)
            self.rule(s, z["x"], y + h + 0.02, z["w"])
            y += h + 0.15
        self.furniture(s, sl["n"])
        return s

    def render(self, out):
        for sl in self.p["slides"]:
            getattr(self, sl["type"])(sl)
        cp = self.prs.core_properties
        cp.title = self.p["title"]
        cp.author = "doc-studio"
        cp.last_modified_by = "doc-studio"
        cp.revision = 1
        self.prs.save(out)
        return out


if __name__ == "__main__":
    plan = load(sys.argv[1])
    Path(sys.argv[2]).parent.mkdir(parents=True, exist_ok=True)
    Deck(plan).render(sys.argv[2])
    print(f"pptx -> {sys.argv[2]}")
