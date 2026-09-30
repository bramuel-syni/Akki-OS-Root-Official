"""HTML review surface: calibration curves per stratum as inline SVG (no runtime), floors drawn, arms table, quote. Deterministic bytes."""
import html, json, math, sys
from pathlib import Path


def svg_curve(x, name, w=520, h=220):
    pts = x["points"]
    vols = [p["examples"] for p in pts]
    lo_v, hi_v = math.log2(vols[0]) - 0.3, math.log2(max(vols[-1] * 4, x["examples_to_floor"] or vols[-1])) + 0.3
    ys = [p["accuracy"] for p in pts] + [p["coverage"] for p in pts] + [x["accuracy_floor"], x["coverage_floor"], x["accuracy_floor"] - 0.25]
    lo_y, hi_y = min(ys) - 0.02, min(1.0, max(ys) + 0.02)
    X = lambda v: 50 + (math.log2(v) - lo_v) / (hi_v - lo_v) * (w - 70)  # noqa: E731
    Y = lambda a: 20 + (hi_y - a) / (hi_y - lo_y) * (h - 50)  # noqa: E731
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{html.escape(name)}">']
    out.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="var(--field)"/>')
    for a in (x["accuracy_floor"], x["coverage_floor"]):
        out.append(f'<line x1="50" y1="{Y(a):.1f}" x2="{w-20}" y2="{Y(a):.1f}" stroke="var(--rule)" stroke-dasharray="4 3"/>')
    out.append(f'<text x="{w-22}" y="{Y(x["accuracy_floor"])-3:.1f}" font-size="9" text-anchor="end" fill="var(--muted)">acc floor {x["accuracy_floor"]:.2f}</text>')
    out.append(f'<text x="{w-22}" y="{Y(x["coverage_floor"])-3:.1f}" font-size="9" text-anchor="end" fill="var(--muted)">cov floor {x["coverage_floor"]:.2f}</text>')
    for key, col in (("accuracy", "var(--accent)"), ("coverage", "var(--muted)")):
        path = " ".join(f'{"M" if i == 0 else "L"}{X(p["examples"]):.1f},{Y(p[key]):.1f}' for i, p in enumerate(pts))
        out.append(f'<path d="{path}" fill="none" stroke="{col}" stroke-width="2"/>')
        for p in pts:
            out.append(f'<circle cx="{X(p["examples"]):.1f}" cy="{Y(p[key]):.1f}" r="3" fill="{col}"/>')
    # projection to floor
    f = x["fit"]["accuracy"]
    if x["examples_to_accuracy_floor"]:
        v2 = x["examples_to_accuracy_floor"]
        out.append(f'<line x1="{X(vols[-1]):.1f}" y1="{Y(pts[-1]["accuracy"]):.1f}" x2="{X(v2):.1f}" y2="{Y(x["accuracy_floor"]):.1f}" stroke="var(--accent)" stroke-dasharray="2 3"/>')
        out.append(f'<text x="{X(v2):.1f}" y="{h-6}" font-size="9" text-anchor="middle" fill="var(--accent)">{v2:,} to floor</text>')
    for v in vols:
        out.append(f'<text x="{X(v):.1f}" y="{h-22}" font-size="9" text-anchor="middle" fill="var(--muted)">{v}</text>')
    out.append(f'<text x="8" y="{Y(hi_y-0.02):.1f}" font-size="9" fill="var(--muted)">{hi_y-0.02:.2f}</text><text x="8" y="{Y(lo_y+0.02):.1f}" font-size="9" fill="var(--muted)">{lo_y+0.02:.2f}</text>')
    out.append("</svg>")
    return "".join(out)


def render(plan, rec, out):
    e = html.escape
    cal = rec["stages"]["calibration"]
    cards = []
    for s, x in cal["per_stratum"].items():
        interval = x['ci'].get('reason') or str(x['ci'].get('low')) + '–' + str(x['ci'].get('high'))
        cards.append(f'<section class="card"><h3>{s} · {e(x["label"])} <span class="tag">{e(x["binding_dimension"] or "—")} binds</span></h3>{svg_curve(x, s)}'
                     f'<p>To accuracy floor: <b>{x["examples_to_accuracy_floor"]}</b> · to coverage floor: <b>{x["examples_to_coverage_floor"]}</b> · available {x["available_examples"]:,} · reachable: <b>{"yes" if x["reachable_within_available"] else "no"}</b> · Uncertainty: {e(interval)}</p></section>')
    for s in cal.get("strata_missing", []):
        cards.append(f'<section class="card missing"><h3>{s} · not evaluated</h3><p>Run interrupted before this stratum. Shown at full weight; not omitted.</p></section>')
    dgn = rec["stages"].get("diagnosis")
    if dgn:
        drows = "".join(f'<tr><td>{s}</td><td><b>{e(d["cause"])}</b></td><td>{e(str(d["evidence"]["slope_last_over_first"]))}</td><td>{d["evidence"]["train_heldout_gap"]}</td><td>{d["evidence"]["annotator_agreement"]}</td><td>{e(d["first_lever"] or "—")}</td></tr>' for s, d in dgn["per_stratum"].items())
        cards.append(f'<section class="card wide"><h3>Diagnosis</h3><table><tr><th>Stratum</th><th>Cause</th><th>Slope ratio</th><th>Gap</th><th>Agreement</th><th>First lever</th></tr>{drows}</table></section>')
    comp = rec["stages"]["comparison"]
    if "arms" in comp:
        rows = "".join(f'<tr><td>{a}</td><td>{e(x["config"])}</td><td class="n">{x["M_a_target_improvement"]:+.4f}</td><td class="n">{x["M_b_non_target_regression_max"]:.4f}</td><td class="n">{x["compute_to_convergence_gpu_hours"]}</td></tr>' for a, x in comp["arms"].items())
        comp_html = f'<h2>Two-arm comparison on {comp["stratum"]} at {comp["examples"]} · lever: {e(comp["lever"]["lever"] if comp.get("lever") else "—")}</h2><table><tr><th>Arm</th><th>Configuration</th><th>M-a</th><th>M-b max</th><th>Compute to convergence (GPU h)</th></tr>{rows}</table><p>Delta B−A {comp["delta_B_minus_A"]:+.4f} vs two-arm MDE {comp["mde_two_arm"]} · adoption evidence: <b>{e(comp["adoption_evidence"])}</b> · {e(comp["owner_verdict"])}</p>'
    else:
        comp_html = f'<h2>Two-arm comparison</h2><p>{e(comp["status"])}</p>'
    q = rec["stages"]["quote"]
    q_html = (f'<h2>Quote</h2><p><b>£{q["quote_gbp"]}</b> for {q["recommended_examples"]:,} examples · range £{q["ci_gbp"]["low"]}–£{q["ci_gbp"]["high"]} ({e(q["ci_gbp"]["kind"])}) · spent £{q["spent_so_far_gbp"]} · cap £{q["budget_cap_gbp"]} · within budget: <b>{q["within_budget"]}</b></p>'
              + (f'<p class="warn">Not reachable within available material: {", ".join(q["strata_not_reachable_within_available"])} — objective owner to rule.</p>' if q.get("strata_not_reachable_within_available") else "")) if "quote_gbp" in q else f'<h2>Quote</h2><p>{e(q["status"])}</p>'
    banner = f'<p class="stub">STUB RUN · {e(rec["evidential_weight"] or "")}</p>' if rec["backend"] == "stub" else ""
    if rec["status"] == "interrupted":
        banner += f'<p class="warn">INTERRUPTED after {rec["interruption"]["after"]} · missing {", ".join(rec["interruption"]["strata_missing"])}</p>'
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(plan["title"])} — review</title>
<style>:root{{--field:#fff;--structure:#1F2A44;--muted:#7F8C9A;--rule:#D8DEE5;--accent:#0E7C86;--hatch:#EAEEF2}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--field:#161a22;--structure:#e6e9ef;--muted:#98a2b3;--rule:#2b3340;--hatch:#1f2531}}}}
body{{margin:0;padding:24px;background:var(--field);color:var(--structure);font:14px/1.4 Calibri,Arial,sans-serif;max-width:1180px;margin:auto}}
h1{{font:600 22px Cambria,serif}} h2{{font:600 16px Cambria,serif;margin-top:28px}} h3{{font:600 14px Calibri;margin:0 0 6px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(520px,1fr));gap:18px}} .card{{border:1px solid var(--rule);padding:12px}} .card.wide{{grid-column:1/-1}} .card.missing{{background:repeating-linear-gradient(45deg,var(--hatch) 0 4px,var(--field) 4px 8px)}}
.tag{{font-size:11px;color:var(--muted);font-weight:400;margin-left:8px}} table{{border-collapse:collapse}} th,td{{padding:6px 10px;border-bottom:1px solid var(--rule);text-align:left}} td.n{{font-family:Consolas,monospace;text-align:right}}
.stub{{color:var(--accent);font-weight:600}} .warn{{color:#B4413E;font-weight:600}} .small{{color:var(--muted);font-size:12px}}</style></head><body>
<h1>{e(plan["title"])}</h1><p class="small">{e(plan["spec_id"])} · direction {e(plan["direction"])} · backend {e(rec["backend"])} · manifest {e(rec["manifest"]["manifest_hash"][:23])} · notebook head {e(rec.get("notebook", {}).get("head", "")[:23])}</p>
{banner}<h2>Calibration curves</h2><div class="grid">{"".join(cards)}</div>{comp_html}{q_html}
<p class="small">Review surface only; the delivered record is run-record.json and technical-report.md. Instrument: training-studio.</p></body></html>"""
    Path(out).write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    render(json.loads(Path(sys.argv[1]).read_text()), json.loads(Path(sys.argv[2]).read_text()), sys.argv[3])
    print(f"review -> {sys.argv[3]}")
