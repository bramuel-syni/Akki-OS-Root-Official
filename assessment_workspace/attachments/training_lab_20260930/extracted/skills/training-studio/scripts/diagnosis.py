"""Diagnosis after calibration: name the cause per stratum with the test that supports it; pick the recipe-seat comparison from the cause map."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(p):
    return json.loads(Path(p).read_text())


def diagnose(plan, cal, obj_extra):
    cmap, levers, priors = load(ROOT / "policies/cause-map.json")["causes"], load(ROOT / "policies/levers.json")["levers"], load(ROOT / "policies/priors.json")
    fam = priors["task_families"][plan["task_family"]]
    seed_sd = sum(fam["seed_sd"]) / 2
    out = {}
    for s, x in cal["per_stratum"].items():
        pts = x["points"]
        accs = [p["accuracy"] for p in pts]
        first = accs[1] - accs[0] if len(accs) > 1 else 0
        last = accs[-1] - accs[-2] if len(accs) > 2 else first
        gap = sum(p.get("train_accuracy", p["accuracy"]) - p["accuracy"] for p in pts) / len(pts)
        agree = obj_extra.get("annotator_agreement", {}).get(s)
        tests = {"slope_last_over_first": round(last / first, 2) if first else None, "train_heldout_gap": round(gap, 4), "annotator_agreement": agree, "seed_sd_prior": seed_sd,
                 "leakage_check": obj_extra.get("leakage_check", {}).get(s, "not run")}
        if tests["leakage_check"] == "found":
            cause = "leakage"
        elif not x["reachable_within_available"] and x.get("undetectable"):
            cause = "undetectable"
        elif agree is not None and agree < priors["evaluation"]["annotator_agreement_floor"]:
            cause = "label-noise-limited"
        elif gap > 2 * seed_sd:
            cause = "overfit"
        elif first and last / first > 0.5:
            cause = "data-limited"
        elif first and last / first < 0.25:
            cause = "method-limited"
        else:
            cause = "data-limited"
        cands = [lid for lid in cmap[cause]["levers"] if levers[lid]["modality"] in (plan["modality_key"], "any")]
        out[s] = {"cause": cause, "test": cmap[cause]["test"], "evidence": tests, "levers_in_order": cands,
                  "first_lever": (levers[cands[0]]["name"] if cands else None), "expected_effect": (levers[cands[0]]["expected_effect"] if cands else None)}
    return out


def choose_comparison(diag, binding_stratum, plan):
    levers = load(ROOT / "policies/levers.json")["levers"]
    d = diag[binding_stratum]
    if not d["levers_in_order"]:
        return None
    lid = d["levers_in_order"][0]
    lv = levers[lid]
    return {"lever_id": lid, "lever": lv["name"], "cause": d["cause"], "arms": [{"arm": "A", "config": f"without {lv['name']}"}, {"arm": "B", "config": f"with {lv['name']}"}],
            "expected_effect": lv["expected_effect"], "rationale": f"binding stratum {binding_stratum} diagnosed {d['cause']}; highest-expected-effect admissible lever for that cause (cause map order)"}
