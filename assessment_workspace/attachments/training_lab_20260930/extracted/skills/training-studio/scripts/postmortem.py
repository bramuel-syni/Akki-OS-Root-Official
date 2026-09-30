"""Postmortem: score a prior run's predictions against actuals, per lens. This is how priors become house-observed and lenses become weighted.
  python scripts/postmortem.py <prior_run_record.json> <actuals.json> <out.json>
actuals.json: {"per_stratum": {"ST1": {"examples_used": n, "accuracy": a, "coverage": c}, ...}, "comparison_winner": "A"|"B", "first_production_failure": "...", "value_realised_gbp": {...}}"""
import json, sys
from pathlib import Path


def score(prior, act):
    out = {"professor": [], "researcher": [], "industry": [], "entrepreneur": []}
    cal = prior["stages"]["calibration"]["per_stratum"]
    for s, x in cal.items():
        a = act["per_stratum"].get(s)
        if not a:
            continue
        pred = x["examples_to_floor"]
        hit = a["accuracy"] >= x["accuracy_floor"] and a["coverage"] >= x["coverage_floor"]
        out["professor"].append({"stratum": s, "predicted_examples_to_floor": pred, "examples_used": a["examples_used"], "floor_met": hit,
                                 "prediction_ok": (pred is not None and hit and a["examples_used"] <= pred * 1.25) or (pred is None and not hit)})
    comp = prior["stages"].get("comparison", {})
    if comp.get("arms"):
        predicted = "B" if comp["delta_B_minus_A"] > 0 else "A"
        out["researcher"].append({"lever": comp["lever"]["lever"] if comp.get("lever") else None, "predicted_winner": predicted, "actual_winner": act.get("comparison_winner"),
                                  "prediction_ok": predicted == act.get("comparison_winner"), "was_detectable": comp["delta_detectable"]})
    op = prior.get("operational_plan", {})
    if op:
        fails = act.get("first_production_failure")
        out["industry"].append({"monitored_signals": [m["signal"] for m in op["monitors"].values()], "first_production_failure": fails,
                                "prediction_ok": bool(fails) and any(k in (fails or "") for k in ("coverage", "drift", "capture"))})
    vc = prior.get("value_case", {})
    for s, v in vc.get("per_stratum", {}).items():
        r = act.get("value_realised_gbp", {}).get(s)
        if r is not None:
            out["entrepreneur"].append({"stratum": s, "predicted_value": v["value_gbp"], "realised": r, "prediction_ok": abs(r - v["value_gbp"]) <= 0.3 * v["value_gbp"]})
    hit_rate = {k: (round(sum(1 for e in v if e["prediction_ok"]) / len(v), 2) if v else None) for k, v in out.items()}
    return {"per_lens": out, "hit_rate": hit_rate, "note": "hit rates per lens feed lens weighting over commissions (cif_spec §10 hit-rate); a lever whose predicted effect is confirmed becomes house-observed with this record as receipt"}


if __name__ == "__main__":
    prior, act = json.loads(Path(sys.argv[1]).read_text()), json.loads(Path(sys.argv[2]).read_text())
    res = score(prior, act)
    Path(sys.argv[3]).write_text(json.dumps(res, indent=2) + "\n")
    print(json.dumps(res["hit_rate"]))
