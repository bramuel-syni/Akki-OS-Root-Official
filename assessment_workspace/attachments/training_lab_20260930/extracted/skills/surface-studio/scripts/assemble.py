"""surface-studio produce: the frozen content record (one entry per block, with class, receipts and walk targets) and the page preview."""
import html, json, sys
from pathlib import Path


def load(p):
    return json.loads(Path(p).read_text())


def content_record(plan):
    return {
        "cache_key": plan["cache_key"], "page": plan["page"], "role": plan["role"], "voice": plan["voice"], "page_state_ref": plan["page_state_ref"], "as_of": plan["as_of"],
        "direction": plan["direction"], "build_stamp": plan["build_stamp"], "source": plan["source"], "stub": plan["stub"], "servable": not plan["stub"],
        "unavailable_sources": plan["unavailable_sources"],
        "blocks": [{"id": b["id"], "move": b["move"], "kind": b.get("kind"), "title": b["title"], "text": b["text"], "classes": b["classes"], "receipts": b["receipts"], "walk": b["walk"], "degraded": b.get("degraded", False), "missing_sources": b.get("missing_sources", [])} for b in plan["blocks"]],
        "silence_surfaced": any(b["move"] == "silence" for b in plan["blocks"]),
        "note": "Frozen copy for this page state, role and voice. Regenerated only when the cache key changes (#19 warm-serve). Instrument: surface-studio.",
    }


def preview(plan, rec):
    e = html.escape
    cards = []
    for b in rec["blocks"]:
        kind = f' <span class="kind">{e(b["kind"])}</span>' if b.get("kind") else ""
        cls = " ".join(f'<span class="chip">{e(c)}</span>' for c in b["classes"]) or '<span class="chip">observed</span>'
        walks = "".join(f'<li><a href="#receipt-{e(w["receipt"])}">{e(plan["walk_affordance"])}</a> {e(w["ref"])} · {e(w["receipt"])}: {e(w["resolves_to"])}</li>' for w in b["walk"])
        cards.append(f'<article class="block {e(b["move"])}"><header><span class="move">{e(b["move"])}</span>{kind}<h2>{e(b["title"])}</h2></header><p>{e(b["text"])}</p><footer>{cls}<details><summary>Receipts ({len(b["walk"])})</summary><ul>{walks}</ul></details></footer></article>')
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(plan["page"])} · {e(plan["role"])} — preview</title>
<style>:root{{--field:#fff;--structure:#1F2A44;--muted:#7F8C9A;--rule:#D8DEE5;--accent:#0E7C86;--hatch:#EAEEF2;--warn:#B4413E}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--field:#161a22;--structure:#e6e9ef;--muted:#98a2b3;--rule:#2b3340;--hatch:#1f2531}}}}
body{{margin:0;background:var(--field);color:var(--structure);font:15px/1.45 Calibri,Arial,sans-serif}} main{{max-width:880px;margin:auto;padding:24px}}
h1{{font:600 20px Cambria,serif;margin:0}} .meta{{color:var(--muted);font-size:12px;margin:4px 0 20px}}
.block{{border:1px solid var(--rule);padding:14px 16px;margin:0 0 14px}} .block.silence{{background:repeating-linear-gradient(45deg,var(--hatch) 0 4px,var(--field) 4px 8px)}}
.block.trigger{{border-left:4px solid var(--accent)}} .move{{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}} .kind{{font-size:11px;color:var(--accent);margin-left:8px}}
h2{{font:600 16px Cambria,serif;margin:4px 0 6px}} p{{margin:0 0 8px}} .chip{{font:11px Consolas,monospace;border:1px solid var(--rule);padding:1px 6px;margin-right:6px}}
.banner{{color:var(--warn);font-weight:600;border:1px solid var(--warn);padding:6px 10px;margin:0 0 12px}} details{{margin-top:6px;font-size:12px;color:var(--muted)}} a{{color:var(--accent)}} ul{{margin:4px 0 0;padding-left:16px}}</style></head><body><main>
{'<p class="banner">STUB PAGE STATE — not servable; preview only.</p>' if plan["stub"] else ''}{('<p class="banner">Sources unavailable at ' + e(plan["as_of"]) + ': ' + e(", ".join(plan["unavailable_sources"])) + '</p>') if plan["unavailable_sources"] else ''}<h1>{e(plan["page"])} · {e(plan["tenant"])}</h1><div class="meta">role {e(plan["role"])} · voice {e(plan["voice"])} · as of {e(plan["as_of"])} · direction {e(plan["direction"])} · cache {e(plan["cache_key"][:23])}</div>
{"".join(cards)}
<p class="meta">Preview only. The frozen copy is content-record.json. Every figure carries its class and a receipt; unmeasured territory is hatched, not blank.</p></main></body></html>"""


if __name__ == "__main__":
    plan = load(sys.argv[1])
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    rec = content_record(plan)
    (out / "content-record.json").write_text(json.dumps(rec, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    (out / "preview.html").write_text(preview(plan, rec), encoding="utf-8")
    print(f"assembled {len(rec['blocks'])} blocks -> {out}")
