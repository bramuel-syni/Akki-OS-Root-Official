"""DR-R1/R2 pure rendering: render(spec, token_set@version, engine@version) → HTML bytes. No clock, no randomness, no LLM,
no field from the spec is read as style. The same (spec, token_version, engine_version) tuple yields byte-identical output."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from typing import Any, Dict, List

from contracts.deck_spec_v1 import DeckSpec_v1, Slide
from services.transform_forms.deck_engine import plates
from services.transform_forms.deck_engine.plates import esc
from services.transform_forms.deck_engine.tokens import REGISTERS, TOKEN_SETS

ENGINE_VERSION = "1.0.0"
TOKEN_VERSION = "v1"
FURNITURE_MARKERS = ("measured", "estimated", "sample", "Receipts:", "Covered basis")


def spec_hash(deck: DeckSpec_v1) -> str:
    canonical = json.dumps(deck.model_dump(by_alias=True, mode="json"), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _css(tokens, reg) -> str:
    c, f = tokens["colour"], tokens["font"]
    return f"""
:root{{--paper:{c['paper']};--surface:{c['surface']};--line:{c['line']};--ink:{c['ink']};--ink2:{c['ink2']};--ink3:{c['ink3']};--sage:{c['sage']};--brass:{c['brass']};--oxblood:{c['oxblood']}}}
html,body{{margin:0;background:var(--paper);color:var(--ink);font-family:{f['body']};font-size:{reg['body_px']}px;line-height:1.35}}
.deck-head{{padding:28px 48px;border-bottom:{tokens['divider']}}}
.deck-head h1{{font-family:{f['head']};font-size:{reg['title_px'] + 6}px;margin:0 0 6px;font-weight:600}}
.deck-head .meta{{color:var(--ink3);font-size:{reg['kicker_px'] + 1}px}}
.deck-head .meta span+span:before{{content:" · "}}
.slide{{position:relative;width:{reg['slide_w']}px;min-height:{reg['slide_h']}px;box-sizing:border-box;padding:40px 48px 64px;margin:24px auto;background:var(--surface);border:{tokens['divider']};page-break-after:always;break-after:page}}
.kicker{{font-family:{f['mono']};font-size:{reg['kicker_px']}px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink3);margin:0 0 8px}}
.slide h2{{font-family:{f['head']};font-size:{reg['title_px']}px;line-height:1.15;margin:0 0 20px;font-weight:600;max-width:{reg['title_chars_per_line'] * 0.6}em}}
.so-what{{color:var(--ink2);margin:16px 0 0;font-size:{reg['body_px']}px}}
.figures{{display:flex;flex-wrap:wrap;gap:18px 32px;margin:12px 0}}
.figure .fig-value{{font-family:{f['head']};font-size:{reg['title_px']}px}}
.figure .fig-label{{display:block;color:var(--ink3);font-size:{reg['kicker_px'] + 1}px}}
.unit{{color:var(--ink3)}}
.chip{{display:inline-block;font-family:{f['mono']};font-size:{reg['kicker_px'] - 1}px;letter-spacing:.06em;text-transform:uppercase;border:1px solid;border-radius:2px;padding:1px 6px;vertical-align:middle;margin-left:6px}}
.badge-sample{{position:absolute;top:18px;right:24px;font-family:{f['mono']};font-size:{reg['kicker_px']}px;letter-spacing:.1em;color:{c['oxblood']};border:1px solid {c['oxblood']};padding:2px 8px;text-transform:uppercase}}
.receipts{{position:absolute;left:48px;right:48px;bottom:18px;font-family:{f['mono']};font-size:{reg['kicker_px']}px;color:var(--ink3);border-top:{tokens['divider']};padding-top:6px}}
.plate-table{{border-collapse:collapse;width:100%;font-size:{reg['body_px'] - 1}px}}
.plate-table th,.plate-table td{{text-align:left;padding:8px 10px;border-bottom:{tokens['divider']};vertical-align:top}}
.plate-table th{{color:var(--ink3);font-weight:500;font-size:{reg['kicker_px'] + 1}px;text-transform:uppercase;letter-spacing:.05em}}
.plate-table caption{{text-align:left;color:var(--ink3);font-size:{reg['kicker_px'] + 1}px;padding-bottom:6px}}
.bullets{{margin:0;padding-left:1.1em}} .bullets li{{margin:0 0 10px}}
.big-number b{{font-family:{f['head']};display:block;line-height:1}} .big-number.demoted b{{color:var(--ink2)}}
.demoted-note{{color:var(--ink3);font-size:{reg['kicker_px'] + 1}px;margin:8px 0 0}}
.hatch-caption{{display:block;color:var(--ink3);font-size:{reg['kicker_px']}px}}
.basis{{font-size:{reg['body_px'] - 1}px}} .limits .reason{{font-family:{f['mono']};font-size:{reg['kicker_px'] + 1}px}}
.notes{{display:none}}
.record{{width:{reg['slide_w']}px;margin:8px auto 40px;font-family:{f['mono']};font-size:{reg['kicker_px']}px;color:var(--ink3)}}
@media print{{html,body{{background:#fff}} .slide{{margin:0;border:0;page-break-after:always}} .record{{page-break-before:always}}}}
"""


def _slide_html(index: int, slide: Slide, model, tokens, reg, deck: DeckSpec_v1) -> str:
    body = ""
    if slide.plate == "P2":
        body = plates.p2(model, tokens, reg)
    elif slide.plate == "P3":
        body = plates.p3(model, tokens, reg)
    elif slide.plate == "P4":
        body = plates.p4(model, tokens, reg)
    elif slide.plate == "P5":
        body = plates.p5(model, tokens, reg)
    elif slide.plate == "P11":
        body = plates.p11(slide, tokens, reg)
    elif slide.plate == "P17" or slide.type == "coverage":
        body = plates.p17(deck.coverage_and_limits, tokens, reg)
    figures = "" if slide.plate == "P11" else ('<div class="figures">' + "".join(plates.figure_html(f, tokens) for f in slide.figures) + "</div>" if slide.figures else "")
    refs = list(slide.receipt_refs) + [r for f in slide.figures for r in f.receipt_refs if r not in slide.receipt_refs]
    receipts = f'<footer class="receipts">Receipts: {" · ".join(esc(r) for r in dict.fromkeys(refs))}</footer>' if refs else ""
    sample = '<span class="badge-sample">Sample</span>' if (deck.meta.sample_deck or any(f.class_ == "sample" for f in slide.figures)) else ""
    kicker = f'<p class="kicker">{esc(slide.kicker)}</p>' if slide.kicker else ""
    so_what = f'<p class="so-what">{esc(slide.so_what)}</p>' if slide.so_what else ""
    notes = f'<aside class="notes">{esc(slide.notes)}</aside>' if slide.notes else ""
    return (f'<section class="slide slide-{esc(slide.type)}" data-index="{index}" data-plate="{esc(slide.plate or "")}">{sample}{kicker}'
            f'<h2>{esc(slide.title)}</h2>{body}{figures}{so_what}{notes}{receipts}</section>')


def render_html(deck: DeckSpec_v1, plate_models: Dict[int, Any]) -> bytes:
    tokens, reg = TOKEN_SETS[TOKEN_VERSION], REGISTERS[deck.register_]
    slides = list(deck.slides) + list(deck.appendix.extra_slides)
    sample_badge = '<span class="badge-sample">Sample deck</span>' if deck.meta.sample_deck else ""
    parts = [f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{esc(deck.meta.title)}</title><style>{_css(tokens, reg)}</style></head><body>',
             f'<header class="deck-head">{sample_badge}<h1>{esc(deck.meta.title)}</h1>'
             f'<p class="meta"><span>{esc(deck.meta.audience_line)}</span><span>{esc(deck.meta.date)}</span><span>register {esc(deck.register_)} — {esc(reg["name"])}</span>'
             f'<span>rights posture {esc(deck.meta.rights_posture_ref)}</span></p></header>']
    parts += [_slide_html(i, s, plate_models.get(i), tokens, reg, deck) for i, s in enumerate(slides)]
    if not any(s.type == "coverage" or s.plate == "P17" for s in slides):
        parts.append(f'<section class="slide slide-coverage" data-index="{len(slides)}" data-plate="P17"><p class="kicker">Coverage and limits</p>'
                     f'<h2>What this deck covers, and what it does not</h2>{plates.p17(deck.coverage_and_limits, tokens, reg)}</section>')
    if deck.appendix.exhibit_index_auto:
        rows = "".join(f'<tr><td>{i + 1}</td><td>{esc(s.title)}</td><td>{esc(s.plate or "")}</td><td>{esc(" · ".join(dict.fromkeys(list(s.receipt_refs) + [r for f in s.figures for r in f.receipt_refs])))}</td></tr>'
                       for i, s in enumerate(slides) if s.figures or s.plate in ("P3", "P4", "P5", "P11"))
        parts.append(f'<section class="slide slide-appendix" data-plate=""><p class="kicker">Appendix</p><h2>Exhibit index</h2>'
                     f'<table class="plate-table"><thead><tr><th>#</th><th>Exhibit</th><th>Plate</th><th>Receipts</th></tr></thead><tbody>{rows}</tbody></table></section>')
    parts.append(f'<p class="record">spec {spec_hash(deck)} · tokens {TOKEN_VERSION} · engine {ENGINE_VERSION} · selection: {esc(deck.selection_manifest.register_why)}'
                 + "".join(f' · override {esc(o.field)}={esc(o.value)} ({esc(o.why)})' for o in deck.selection_manifest.overrides) + "</p></body></html>")
    return "".join(parts).encode("utf-8")


def pdf_capability() -> Dict[str, Any]:
    binary = os.environ.get("AKKI_DECK_PDF_BROWSER") or shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    return {"available": bool(binary), "binary": binary, "method": "headless browser print pipeline from the same HTML (DR-R9)"}


def render_pdf(html_bytes: bytes, timeout: int = 60) -> bytes:
    cap = pdf_capability()
    if not cap["available"]:
        raise RuntimeError("PDF_EXPORT_UNAVAILABLE: no headless browser on this host; HTML remains the artifact of record")
    with tempfile.TemporaryDirectory() as tmp:
        src, out = os.path.join(tmp, "deck.html"), os.path.join(tmp, "deck.pdf")
        with open(src, "wb") as fh:
            fh.write(html_bytes)
        cmd = [cap["binary"], "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out}", f"file://{src}"]
        subprocess.run(cmd, check=True, timeout=timeout, capture_output=True)
        with open(out, "rb") as fh:
            return fh.read()


def furniture_survives(pdf_bytes: bytes, expected: List[str]) -> Dict[str, Any]:
    """gate_export_furniture_survives: the export's text layer must still carry the chips, receipt lines and coverage basis."""
    try:
        from pypdf import PdfReader
        import io
        text = "\n".join((page.extract_text() or "") for page in PdfReader(io.BytesIO(pdf_bytes)).pages)
    except Exception as exc:  # noqa: BLE001 — reported, never hidden
        return {"checked": False, "reason": f"text layer unreadable: {type(exc).__name__}"}
    missing = [m for m in expected if m.lower() not in text.lower()]
    return {"checked": True, "survives": not missing, "missing": missing, "pages": text.count("\f") + 1 if text else 0}
