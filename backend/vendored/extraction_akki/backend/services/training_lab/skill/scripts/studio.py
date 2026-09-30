"""training-studio resolve: plan + objective + brief + verdict + policy → frozen resolved plan.

No judgment lives here. Volumes, arms, costs and strata come from the policy
and the objective by reference; the runner executes what this writes.
"""
import hashlib, json, math, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKEN = re.compile(r"\{([A-Za-z_][A-Za-z0-9_.:\[\]*]*)\}")


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def dump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(o, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def smallest_valid_stratum(obj, policy):
    """Smallest stratum whose test_n supports a valid evaluation (A17.5): the smallest with test_n ≥ policy floor."""
    floor = policy["calibration"]["small_stratum_floor_examples"] // 3
    ok = [(s, d["test_n"]) for s, d in obj["population"]["strata"].items() if d["test_n"] >= floor]
    return min(ok, key=lambda x: x[1])[0]


def resolve(fixture_dir, out_dir):
    fx, out = Path(fixture_dir), Path(out_dir)
    plan, obj, brief, verdict = load(fx / "plan.json"), load(fx / "objective.json"), load(fx / "brief.json"), load(fx / "verdict.json")
    policy = load(ROOT / "policies" / "run-policy.json")
    oref = f"{obj['objective_id']}@{obj['version']}"
    assert plan["objective_ref"] == oref == brief["objective_ref"], "objective_ref mismatch"
    assert plan["verdict_ref"] == verdict["verdict_id"] and verdict["brief_ref"] == brief["brief_id"], "verdict/brief mismatch"
    cal = policy["calibration"]
    strata = obj["population"]["strata"]
    gpu = obj["cost"]["gpu_hour_gbp"]
    # calibration cost, deterministic from policy + objective
    cal_hours = 0.0
    for s in strata:
        for v in cal["volumes"]:
            cal_hours += v / 1000 * cal["epochs_per_volume"] * cal["gpu_hours_per_1000_examples_epoch"] + cal["eval_gpu_hours_per_stratum"]
    comp_stratum = smallest_valid_stratum(obj, policy)
    comp_hours = 2 * (cal["volumes"][-1] / 1000 * cal["epochs_per_volume"] * cal["gpu_hours_per_1000_examples_epoch"] + cal["eval_gpu_hours_per_stratum"])
    resolved = {
        "spec_id": plan["spec_id"], "objective_ref": oref, "brief_ref": brief["brief_id"], "verdict_ref": verdict["verdict_id"],
        "direction": verdict["adopted"], "manifest_ids": [m["id"] for m in verdict["manifest"]],
        "backend": plan["backend"], "seed": plan["seed"], "build_stamp": plan["build_stamp"],
        "title": obj["title"], "task": obj["task"], "modality": obj["modality"],
        "base_model": obj["base_model"], "recipe": plan["recipe"],
        "strata": {s: {**d, "baseline_accuracy": obj["baseline"]["per_stratum"][s], "baseline_coverage": obj["baseline"]["coverage"][s],
                       "accuracy_floor": obj["acceptance"]["per_stratum"][s]["accuracy_floor"], "coverage_floor": obj["acceptance"]["per_stratum"][s]["coverage_floor"],
                       "gap_pp": round((obj["acceptance"]["per_stratum"][s]["accuracy_floor"] - obj["baseline"]["per_stratum"][s]) * 100, 1),
                       "available_examples": sum(m["examples"] for m in obj["materials"].values() if m["stratum"] == s)} for s, d in strata.items()},
        "gate_policy": brief["constraints"]["gate_policy"], "non_target_regression_max": obj["acceptance"]["non_target_regression_max"],
        "materials": obj["materials"], "receipts": obj["receipts"],
        "calibration": {"volumes": cal["volumes"], "epochs": cal["epochs_per_volume"], "selection": cal["selection"], "gpu_hours": round(cal_hours, 3), "cost_gbp": round(cal_hours * gpu, 2)},
        "comparison": {"stratum": comp_stratum, "arms": policy["comparison"]["candidates"], "parity_tolerance": policy["comparison"]["parity_tolerance"],
                       "gpu_hours": round(comp_hours, 3), "cost_gbp": round(comp_hours * gpu, 2), "compute_is_gating": policy["comparison"]["compute_is_gating"]},
        "budget_cap_gbp": brief["constraints"]["budget_cap_gbp"], "gpu_hour_gbp": gpu,
        "quote_policy": policy["quote"], "scaling_fit": policy["scaling_fit"], "reproducibility": policy["reproducibility"],
        "full_run": policy["full_run"], "interruption": policy["interruption"],
        "rates": {"gpu_hours_per_1000_examples_epoch": cal["gpu_hours_per_1000_examples_epoch"], "eval_gpu_hours_per_stratum": cal["eval_gpu_hours_per_stratum"]},
        "materials_index": str(fx / policy["manifest"]["index_file"]), "manifest_policy": policy["manifest"], "notebook_policy": policy["notebook"],
        "moac_pack_policy": policy["moac_pack"], "completion_certificate_policy": policy["completion_certificate"],
        "collection_schema": obj["collection_schema"], "baseline_ref": obj["baseline"]["run_ref"],
        "task_family": obj["task_family"], "modality_key": obj["modality_key"], "annotator_agreement": {k: v for k, v in obj["annotator_agreement"].items() if k.startswith("ST")},
        "value": obj["value"], "production": obj["production"], "test_set_custody": obj["test_set_custody"],
        "milestones": plan["milestones"], "report_skeleton": policy["report"]["skeleton"], "coverage": obj["coverage"],
        "stub_policy": policy["stub"] if plan["backend"] == "stub" else None,
        "inputs_sha256": {p.name: sha(p) for p in [fx / "plan.json", fx / "objective.json", fx / "brief.json", fx / "verdict.json", ROOT / "policies" / "run-policy.json", ROOT / "policies" / "levers.json", ROOT / "policies" / "priors.json", ROOT / "policies" / "cause-map.json"]},
    }
    dump(resolved, out / "run_plan.resolved.json")
    return resolved


if __name__ == "__main__":
    r = resolve(sys.argv[1], sys.argv[2])
    print(f"resolved: comparison on {r['comparison']['stratum']}, calibration £{r['calibration']['cost_gbp']}, cap £{r['budget_cap_gbp']}")
