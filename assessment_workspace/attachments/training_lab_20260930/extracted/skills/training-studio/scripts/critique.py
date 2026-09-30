"""Objective critique: the four lenses run their question sets against the objective before any direction is chosen.

Arithmetic parts are computed (MDE per stratum; value per stratum; cost from priors); judgment parts are authored under the lens question sets and recorded with their class. Output: critique-table.json and critique.md. Only the professor's MDE finding is a blocker; everything else routes to the objective owner.
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import stats  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def load(p):
    return json.loads(Path(p).read_text())


def run(obj, brief):
    priors, levers, cmap = load(ROOT / "policies/priors.json"), load(ROOT / "policies/levers.json")["levers"], load(ROOT / "policies/cause-map.json")
    fam = priors["task_families"][obj["task_family"]]
    conf = priors["evaluation"]["confidence"]
    rows, blockers = [], []
    strata = obj["population"]["strata"]
    # --- professor: MDE per stratum, sealed set, seeds
    for s, d in strata.items():
        base, floor = obj["baseline"]["per_stratum"][s], obj["acceptance"]["per_stratum"][s]["accuracy_floor"]
        m = stats.mde(base, d["test_n"], conf)
        gap = floor - base
        detectable = gap >= m
        lever = levers["eval.enlarge_test"]
        need_n = int((d["test_n"] * (m / gap) ** 2) + 1) if gap > 0 else None
        rows.append({"lens": "professor", "stratum": s, "objection": f"gap to floor {gap*100:.1f}pp vs MDE {m*100:.1f}pp at test_n={d['test_n']}", "class": "fact",
                     "severity": "blocker" if not detectable else "note", "lever": None if detectable else lever["name"],
                     "lever_detail": None if detectable else f"raise sealed test set to ≥{need_n} items for {s} (currently {d['test_n']}); cost: labelling {need_n - d['test_n']} items",
                     "resolves_with": None if detectable else "objective owner funds test-set enlargement, or accepts that the floor cannot be verified on this stratum (documented)"})
        if not detectable:
            blockers.append(f"{s}: floor unverifiable — gap {gap*100:.1f}pp < MDE {m*100:.1f}pp at test_n={d['test_n']} (professor); enlarge the sealed set to ≥{need_n}")
    rows.append({"lens": "professor", "stratum": "all", "objection": f"single-seed calibration unless budget allows ≥{priors['evaluation']['min_seeds_for_distribution_comparison']} seeds; numbers will be marked single-seed", "class": "recalled", "severity": "note", "lever": None, "lever_detail": None, "resolves_with": "budget for seeds, or accept single-seed labelling"})
    if obj.get("test_set_custody", {}).get("seen_by_training_decisions", None) is None:
        rows.append({"lens": "professor", "stratum": "all", "objection": "test set custody not stated: who has seen it, has it been used to choose anything", "class": "inferred", "severity": "note", "lever": None, "lever_detail": None, "resolves_with": "add test_set_custody to the objective"})
    # --- entrepreneur: value per stratum, kill criteria, phased path
    value_rows = []
    for s, d in strata.items():
        v = obj.get("value", {}).get("per_stratum", {}).get(s)
        base, floor = obj["baseline"]["per_stratum"][s], obj["acceptance"]["per_stratum"][s]["accuracy_floor"]
        per_point = fam.get("examples_per_point_from_baseline_0.6_0.8") or fam.get("examples_per_point_from_baseline_0.6_0.9") or [50, 200]
        need = stats.examples_to_floor_from_prior(base, floor, per_point, 60000)
        gpu = obj["cost"]["gpu_hour_gbp"]
        cost = [round(n / 1000 * 3 * 1.2 * gpu, 0) for n in need]
        value_rows.append({"stratum": s, "value_gbp": v["gbp"] if v else None, "value_basis": v["basis"] if v else "not stated", "prior_examples_to_floor": need, "prior_cost_gbp": cost,
                           "ratio": (round(v["gbp"] / max(cost[1], 1), 1) if v else None), "class": "estimated"})
    ranked = sorted([r for r in value_rows if r["ratio"] is not None], key=lambda r: -r["ratio"])
    rows.append({"lens": "entrepreneur", "stratum": "all", "objection": "phased path by value/cost: " + (" > ".join(f"{r['stratum']} ({r['ratio']}×)" for r in ranked) if ranked else "value per stratum not stated; cannot rank"), "class": "estimated", "severity": "note",
                 "lever": "phase by value", "lever_detail": "clear the highest-ratio stratum first; its saving funds the next", "resolves_with": "objective owner confirms the value basis per stratum"})
    total_prior_cost = sum(r["prior_cost_gbp"][1] for r in value_rows)
    cap = brief["constraints"]["budget_cap_gbp"]
    rows.append({"lens": "entrepreneur", "stratum": "all", "objection": f"prior full-run cost upper bound £{total_prior_cost:,.0f} vs cap £{cap:,}: {'within' if total_prior_cost <= cap else 'OVER — phase or raise cap'}", "class": "estimated", "severity": "note" if total_prior_cost <= cap else "escalate",
                 "lever": "stop-loss", "lever_detail": "stop after calibration if the binding stratum's curve projects beyond available material or beyond the phase budget", "resolves_with": "owner agrees the stop-loss before calibration"})
    # --- industry: capture condition, monitor, owner
    prod = obj.get("production", {})
    for s, d in strata.items():
        cc = prod.get("capture_condition", {}).get(s)
        mon = prod.get("monitor", {}).get(s)
        if not cc:
            rows.append({"lens": "industry", "stratum": s, "objection": "production capture condition not stated; calibration material may not match production", "class": "inferred", "severity": "escalate", "lever": levers["data.restratify"]["name"], "lever_detail": "state capture condition per stratum; re-stratify if it differs from the register axis", "resolves_with": "objective owner states production conditions"})
        if not mon:
            rows.append({"lens": "industry", "stratum": s, "objection": "no production monitor for the coverage floor", "class": "fact", "severity": "escalate", "lever": "monitor per stratum", "lever_detail": "coverage rate and confidence distribution, weekly; trigger below floor two weeks running", "resolves_with": "owner names the monitor and the seat"})
    if not prod.get("owner_seat"):
        rows.append({"lens": "industry", "stratum": "all", "objection": "no owner seat after admission", "class": "fact", "severity": "escalate", "lever": "name the seat", "lever_detail": "the artefact is a liability until owned", "resolves_with": "owner names the seat"})
    # --- researcher: comparison follows the cause; prior; counterfactual
    rows.append({"lens": "researcher", "stratum": "all", "objection": f"literature prior for {obj['task_family']}: b∈{fam['power_law']['exponent_b']}, seed SD {fam['seed_sd']} ({fam['class']}); the recipe-seat comparison will be chosen from the diagnosed cause (cause map), not defaulted to the optimizer", "class": "recalled", "severity": "note", "lever": "comparison follows cause", "lever_detail": cmap["comparison_rule"], "resolves_with": "diagnosis after calibration"})
    return {"blockers": blockers, "rows": rows, "value_table": value_rows, "confidence": conf}


def to_md(ct):
    L = ["# Objective critique (four lenses)\n", "| Lens | Stratum | Objection | Class | Severity | Proposed lever | Resolves with |", "|---|---|---|---|---|---|---|"]
    for r in ct["rows"]:
        L.append(f"| {r['lens']} | {r['stratum']} | {r['objection']} | {r['class']} | {r['severity']} | {r['lever'] or '—'}{(': ' + r['lever_detail']) if r['lever_detail'] else ''} | {r['resolves_with'] or '—'} |")
    L.append("\n## Value table (entrepreneur)\n\n| Stratum | Value £ | Basis | Prior examples to floor | Prior cost £ | Ratio |\n|---|---|---|---|---|---|")
    for v in ct["value_table"]:
        L.append(f"| {v['stratum']} | {v['value_gbp'] if v['value_gbp'] is not None else '—'} | {v['value_basis']} | {v['prior_examples_to_floor'][0]:,}–{v['prior_examples_to_floor'][1]:,} | {v['prior_cost_gbp'][0]:,.0f}–{v['prior_cost_gbp'][1]:,.0f} | {v['ratio'] if v['ratio'] is not None else '—'} |")
    L.append("\nOnly the professor's MDE finding blocks; every other row routes to the objective owner, who may overrule on the record. All expected effects are priors with a class.")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    fx, out = Path(sys.argv[1]), Path(sys.argv[2])
    ct = run(load(fx / "objective.json"), load(fx / "brief.json"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "critique-table.json").write_text(json.dumps(ct, indent=2, sort_keys=True) + "\n")
    (out / "critique.md").write_text(to_md(ct))
    print(json.dumps({"blockers": ct["blockers"], "rows": len(ct["rows"])}, indent=2))
