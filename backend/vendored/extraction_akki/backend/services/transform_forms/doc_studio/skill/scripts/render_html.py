"""Render a resolved deck plan to a single self-contained HTML review page.

Same zones (converted to percentages of the slide), same palette and fonts as
the pptx path, so the review surface and the delivered file are held to one
specification. Charts are inline SVG from the shared chart module.
"""
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from charts import chart_svg  # noqa: E402
from studio import load  # noqa: E402


def esc(s):
    return html.escape(str(s))


def render(plan, out):
    W, H = plan["slide_w"], plan["slide_h"]
    pal, fonts, sz = plan["look"]["palette"], plan["look"]["fonts"], plan["sizes_pt"]

    def zone(z, extra=""):
        return f'style="left:{z["x"]/W*100:.2f}%;top:{z["y"]/H*100:.2f}%;width:{z["w"]/W*100:.2f}%;height:{z["h"]/H*100:.2f}%;{extra}"'

    def box(z, cls, inner, extra=""):
        return f'<div class="z {cls}" {zone(z, extra)}>{inner}</div>'

    fz = plan["furniture_zones"]
    fu = plan["furniture"]

    def furniture(n):
        return (box(fz["doc_id"], "small", esc(fu.get("deck_id", plan["spec_id"])), "display:flex;align-items:flex-end")
                + box(fz["confidentiality"], "small", esc(fu.get("confidentiality", "")), "display:flex;align-items:flex-end;justify-content:center")
                + box(fz["page_no"], "small mono", str(n), "display:flex;align-items:flex-end;justify-content:flex-end"))

    def header(sl):
        z = sl["zones"]
        return box(z["kicker"], "kicker", esc(sl["kicker"]).upper()) + box(z["title"], "title", esc(sl["title"]))

    def receipt(z, cls, ids, text):
        return box(z, "small mono", esc(f"[{cls}]  Receipt {', '.join(ids)}: {text}"), "display:flex;align-items:flex-end")

    slides = []
    for sl in plan["slides"]:
        t, z = sl["type"], sl["zones"]
        parts, bg = [], pal["field"]
        if t == "cover":
            parts += [box(z["title"], "title cover", esc(sl["title"]), "display:flex;align-items:flex-end"),
                      box(z["subtitle"], "body muted", esc(sl["subtitle"])),
                      box(z["org"], "small", esc(f'{sl["org"]}  ·  {fu.get("confidentiality", "")}'))]
        elif t == "exec_summary":
            parts.append(header(sl))
            rows = "".join(f'<div class="scqa"><div class="kicker{" accent" if l == "Answer" else ""}">{l.upper()}</div><div class="body">{esc(b)}</div></div>' for l, b in sl["scqa"])
            parts.append(box(z["body"], "", rows))
            parts.append(furniture(sl["n"]))
        elif t == "section":
            inv = plan["look"]["divider_treatment"] == "inverted-field"
            bg = pal["structure"] if inv else pal["field"]
            fg = pal["field"] if inv else pal["accent"]
            parts += [box(z["number"], "mono", f'{sl["number"]:02d}', f"font-size:{sz['section_number']}pt;color:#{fg};display:flex;align-items:center"),
                      box(z["title"], "title", esc(sl["title"]), f"font-size:{sz['section_title']}pt;color:#{pal['field'] if inv else pal['structure']};display:flex;align-items:center")]
        elif t == "assertion_exhibit":
            ex = sl["exhibit"]
            parts += [header(sl), box(z["exhibit"], "chart", chart_svg(ex, pal, fonts))]
            if ex["so_what"]:
                parts.append(box(z["so_what"], "body accent italic", esc(ex["so_what"]), "display:flex;align-items:flex-end"))
            parts += [receipt(z["receipt"], ex["class"], [ex["receipt"]], ex["receipt_text"]), furniture(sl["n"])]
        elif t == "assertion_points":
            parts.append(header(sl))
            pts = "".join(f'<div class="pt"><div class="mono accent num">{i+1:02d}</div><div class="body">{esc(p)}</div></div>' for i, p in enumerate(sl["points"]))
            parts += [box(z["points"], "", pts), furniture(sl["n"])]
        elif t == "comparison":
            tb = sl["table"]
            head = "<tr><th></th>" + "".join(f"<th>{esc(c)}</th>" for c in tb["columns"]) + "</tr>"
            body = "".join("<tr><td class='muted'>" + esc(r["label"]) + "</td>" + "".join(f"<td class='mono r'>{esc(c)}</td>" for c in r["cells"]) + "</tr>" for r in tb["rows"])
            parts += [header(sl), box(z["table"], "", f"<table>{head}{body}</table>")]
            if tb["so_what"]:
                parts.append(box(z["so_what"], "body accent italic", esc(tb["so_what"]), "display:flex;align-items:flex-end"))
            parts += [receipt(z["receipt"], tb["class"], tb["receipts"], tb["receipt_text"]), furniture(sl["n"])]
        elif t == "coverage_limits":
            cov = sl["coverage"]
            rows = "".join(f'<tr class="hatch"><td>{esc(g["gap"])}</td><td>{esc(g["reason"])}</td><td>{esc(g["closes_with"])}</td></tr>' for g in cov["cannot_say"])
            inner = f'<div class="kicker">COVERS</div><div class="body">{esc(cov["covers"])}</div><table class="cov"><tr><th>CANNOT SAY</th><th>WHY</th><th>WHAT WOULD CLOSE IT</th></tr>{rows}</table>'
            parts += [header(sl), box(z["body"], "", inner), furniture(sl["n"])]
        elif t == "hero":
            bg = pal["structure"]
            if sl.get("kicker"):
                parts.append(box(z["kicker"], "kicker", esc(sl["kicker"]).upper(), f"color:#{pal['accent']}"))
            parts.append(box(z["statement"], "title", esc(sl["statement"]), f"font-size:{sz['hero']/14:.3f}em;color:#{pal['field']};display:flex;align-items:center"))
        elif t == "closing":
            bg = pal["structure"]
            parts.append(box(z["statement"], "title", esc(sl["statement"]), f"font-size:{sz['closing']/14:.3f}em;color:#{pal['field']};display:flex;align-items:center"))
            if sl.get("sub"):
                parts.append(box(z["sub"], "body muted", esc(sl["sub"])))
        elif t == "big_number":
            ex = sl["exhibit"]
            parts += [box(z["kicker"], "kicker", esc(sl["kicker"]).upper(), "text-align:center"),
                      box(z["number"], "mono accent", esc(sl["number"]), f"font-size:{sz['big_number']/14:.3f}em;display:flex;align-items:center;justify-content:center"),
                      box(z["label"], "body", esc(sl["label"]), "text-align:center")]
            if ex["so_what"]:
                parts.append(box(z["so_what"], "body muted italic", esc(ex["so_what"]), "text-align:center"))
            parts += [receipt(z["receipt"], ex["class"], [ex["receipt"]], ex["receipt_text"]), furniture(sl["n"])]
        elif t == "appendix":
            rows = "".join(f'<div class="pt"><div class="mono accent" style="width:7%">{esc(r["id"])}</div><div class="body">{esc(r["text"])}</div></div>' for r in sl["receipts"])
            parts += [header(sl), box(z["body"], "", rows), furniture(sl["n"])]
        elif t == "table":
            tb = sl["table"]
            head = "<tr>" + "".join(f"<th>{esc(c)}</th>" for c in tb["columns"]) + "</tr>"
            body = "".join("<tr>" + "".join(f"<td class='{'mono r' if c >= tb['right_align_from'] else ''}'>{esc(v)}</td>" for c, v in enumerate(row)) + "</tr>" for row in tb["rows"])
            parts += [header(sl), box(z["table"], "", f"<table>{head}{body}</table>")]
            if tb["so_what"]:
                parts.append(box(z["so_what"], "body accent italic", esc(tb["so_what"]), "display:flex;align-items:flex-end"))
            parts += [receipt(z["receipt"], tb["class"], tb["receipts"], tb["receipt_text"]), furniture(sl["n"])]
        elif t == "glossary":
            terms = "".join(f'<div class="pt"><div class="accent" style="width:26%;font-weight:700">{esc(g["term"])}</div><div class="body">{esc(g["meaning"])}</div></div>' for g in sl["terms"])
            parts += [header(sl), box(z["points"], "", terms), furniture(sl["n"])]
        slides.append(f'<section class="slide" style="background:#{bg}">{"".join(parts)}</section>')

    css = f"""
:root{{--field:#{pal['field']};--structure:#{pal['structure']};--muted:#{pal['muted']};--rule:#{pal['rule']};--accent:#{pal['accent']};--hatch:#{pal['hatch']}}}
body{{margin:0;background:#2b2b2b;font-family:'{fonts['body']}',Calibri,Arial,sans-serif;color:var(--structure)}}
.slide{{position:relative;width:min(96vw,1280px);aspect-ratio:{W}/{H};margin:24px auto;box-shadow:0 2px 12px #0006;font-size:calc(min(96vw,1280px)/{W}*0.0139*14)}}
.z{{position:absolute;box-sizing:border-box;overflow:hidden}}
.kicker{{font-size:{sz['kicker']/14:.3f}em;font-weight:700;color:var(--muted);letter-spacing:.04em}}
.title{{font-family:'{fonts['title']}',Cambria,serif;font-size:{sz['title']/14:.3f}em;line-height:1.15}}
.title.cover{{font-size:{sz['cover_title']/14:.3f}em}}
.body{{font-size:1em;line-height:1.3}} .small{{font-size:{sz['small']/14:.3f}em;color:var(--muted)}}
.mono{{font-family:'{fonts['number']}',monospace}} .muted{{color:var(--muted)}} .accent{{color:var(--accent)}} .italic{{font-style:italic}}
.scqa{{display:grid;grid-template-columns:14% 1fr;gap:0 1em;border-bottom:1px solid var(--rule);padding:.5em 0}}
.scqa:last-child{{border:0}} .kicker.accent{{color:var(--accent)}}
.pt{{display:flex;gap:1em;align-items:flex-start;border-bottom:1px solid var(--rule);padding:.6em 0}} .pt .num{{font-size:{sz['title']/14:.3f}em;line-height:1}}
table{{border-collapse:collapse;width:100%;font-size:.95em}} th{{background:var(--hatch);text-align:left;padding:.4em .6em;font-weight:700}}
td{{padding:.4em .6em;border-bottom:1px solid var(--rule)}} td.r{{text-align:right}}
table.cov{{margin-top:.8em}} tr.hatch td{{background:repeating-linear-gradient(45deg,var(--hatch) 0 4px,var(--field) 4px 8px)}}
.chart svg{{width:100%;height:100%}}
"""
    manifest = f"<p style='color:#bbb;font:12px monospace;text-align:center'>{esc(plan['spec_id'])} · direction {esc(plan['direction'])} · {esc(plan['voice'])} · look {esc(plan['look']['palette_id'])}/{esc(plan['look']['type_pair_id'])}/{esc(plan['look']['cover_composition'])} · seed {esc(plan['seed'])}</p>"
    doc = f"<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{esc(plan['title'])} — review</title><style>{css}</style></head><body>{manifest}{''.join(slides)}</body></html>"
    Path(out).write_text(doc, encoding="utf-8")
    return out


if __name__ == "__main__":
    plan = load(sys.argv[1])
    Path(sys.argv[2]).parent.mkdir(parents=True, exist_ok=True)
    render(plan, sys.argv[2])
    print(f"html -> {sys.argv[2]}")
