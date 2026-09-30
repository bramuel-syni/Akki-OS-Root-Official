"""Mechanical QA on rendered files. Blockers only; judgment stays with the reviewer.

Checks:
- pptx/docx: the office validators from the pptx and docx skills (schema, rels, charts)
- pptx: text-fit estimate per text box from font metrics (Liberation metrics match
  Arial/Calibri-class widths closely enough to catch real overflow; serif titles are
  given 10% slack, as the pptx skill advises)
- xlsx: zero formula errors after recalc, and every Checks!D cell reads OK
"""
import json
import subprocess
import sys
from pathlib import Path

from openpyxl import load_workbook
from PIL import ImageFont
from pptx import Presentation
from pptx.util import Emu

SKILLS = Path("/mnt/skills/public")
FONT_FILES = {
    "sans": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "serif": "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "mono": "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
}
SERIF = {"Cambria", "Bookman Old Style", "Century Schoolbook", "Times New Roman", "Georgia"}
MONO = {"Courier New", "Consolas"}


def _font(name, size_pt):
    kind = "serif" if name in SERIF else "mono" if name in MONO else "sans"
    return ImageFont.truetype(FONT_FILES[kind], int(size_pt * 10)), kind


def wrap_lines(text, font, width_pt):
    """Greedy word wrap, the way PowerPoint breaks lines: words never split."""
    lines, cur = 1, 0.0
    space = font.getlength(" ") / 10
    for word in text.split():
        wl = font.getlength(word) / 10
        if cur == 0:
            cur = wl
        elif cur + space + wl <= width_pt:
            cur += space + wl
        else:
            lines += 1
            cur = wl
    return lines


def text_fit(pptx_path):
    """Estimate whether each text box's content fits its frame; returns blockers."""
    prs = Presentation(pptx_path)
    out = []
    for n, slide in enumerate(prs.slides, start=1):
        for sh in slide.shapes:
            if not sh.has_text_frame or sh.width is None:
                continue
            tf = sh.text_frame
            w_in = Emu(sh.width).inches
            h_in = Emu(sh.height).inches
            need_in = 0.0
            for para in tf.paragraphs:
                runs = [r for r in para.runs if r.text]
                if not runs:
                    continue
                size = runs[0].font.size.pt if runs[0].font.size else 14
                name = runs[0].font.name or "Calibri"
                font, kind = _font(name, size)
                text = "".join(r.text for r in runs)
                slack = 1.10 if kind == "serif" else 1.0
                lines = wrap_lines(text, font, w_in * 72 / slack)
                need_in += lines * size * 1.2 / 72
            if need_in > h_in * 1.05 and need_in - h_in > 0.12:
                out.append(f"slide {n}: text needs ~{need_in:.2f}in but box is {h_in:.2f}in: \"{tf.text[:50]}\"")
    return out


def office_validate(path, kind):
    script = SKILLS / kind / "scripts" / "office" / "validate.py"
    r = subprocess.run([sys.executable, str(script), str(path)], capture_output=True, text=True)
    ok = "PASSED" in r.stdout or r.returncode == 0
    return [] if ok else [f"{kind} validator: {r.stdout.strip()[-400:]}"]


def workbook_gate(path):
    out = []
    wb = load_workbook(path, data_only=True)
    if "Checks" not in wb.sheetnames:
        return ["xlsx: no Checks sheet"]
    ws = wb["Checks"]
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] and row[2] is not None and row[3] != "OK":
            out.append(f"xlsx Checks: {row[0]} -> {row[3]} (workbook {row[1]} vs content {row[2]})")
    for wsn in wb.sheetnames:
        for row in wb[wsn].iter_rows(values_only=True):
            for v in row:
                if isinstance(v, str) and v.startswith("#"):
                    out.append(f"xlsx {wsn}: formula error {v}")
    return out


def main(out_dir, recalc_json=None):
    out_dir = Path(out_dir)
    blockers = []
    for p in sorted(out_dir.iterdir()):
        if p.suffix == ".pptx":
            blockers += office_validate(p, "pptx")
            blockers += text_fit(p)
        elif p.suffix == ".docx":
            blockers += office_validate(p, "docx")
        elif p.suffix == ".xlsx":
            blockers += workbook_gate(p)
    releasable = {p.name: True for p in out_dir.iterdir() if p.suffix in (".pptx", ".docx", ".xlsx", ".html")}
    if recalc_json:
        rc = json.loads(Path(recalc_json).read_text())
        if rc.get("backend") == "stub" or rc.get("status") == "unavailable":
            for k in releasable:
                if k.endswith(".xlsx"):
                    releasable[k] = False
            blockers.append("xlsx: recalc backend stub (LibreOffice unavailable); workbook not releasable until recalculated")
        elif rc.get("status") != "success":
            blockers.append(f"recalc: {rc}")
    report = {"blockers": blockers, "releasable": releasable, "status": "FAIL" if blockers else "PASS"}
    (out_dir / "qa-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
