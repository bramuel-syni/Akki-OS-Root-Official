"""training-studio produce: execute the resolved run plan through a trainer backend.

Stages: manifest → notebook open → calibration (per stratum, per volume) →
two-arm comparison → quote → full (planned, never executed here) → MOAC pack
request → certificate template. The runner never writes a verdict (A17.6).
Interruption after a stratum writes a partial record; the report is blocked
until the objective owner's partial ruling is referenced.
"""
import hashlib, json, math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import backend as be  # noqa: E402
import diagnosis as dg  # noqa: E402
import manifest as mf  # noqa: E402
import stats as st  # noqa: E402
from notebook import Notebook  # noqa: E402


def load(p):
    return json.loads(Path(p).read_text())


def dump(o, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(o, indent=2, sort_keys=True) + "\n")


def fit_log_linear(points):
    xs = [math.log2(v) for v, _ in points]
    ys = [a for _, a in points]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx if sxx else 0.0
    intercept = my - slope * mx
    return slope, intercept, [y - (intercept + slope * x) for x, y in zip(xs, ys)]


def examples_to_reach(slope, intercept, floor, cap):
    if slope <= 0:
        return None
    return int(min(cap, 2 ** ((floor - intercept) / slope)))


def bootstrap_ci(points, floor, cap, seed, level, draws=200):
    slope, intercept, resid = fit_log_linear(points)
    ests = []
    for i in range(draws):
        pts = []
        for j, (v, a) in enumerate(points):
            k = int(hashlib.sha256(f"{seed}:{i}:{j}".encode()).hexdigest()[:4], 16) % len(resid)
            pts.append((v, a - resid[j] + resid[k]))
        s2, i2, _ = fit_log_linear(pts)
        e = examples_to_reach(s2, i2, floor, cap)
        ests.append(e if e is not None else cap)
    ests.sort()
    return ests[int((1 - level) / 2 * draws)], ests[int((1 + level) / 2 * draws) - 1]


def run(plan, out_dir, interrupt_after=None):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    bk = be.make(plan)  # raises with the contract for backend=real
    seed, sf, cap = plan["seed"], plan["scaling_fit"], plan["scaling_fit"]["extrapolation_cap_examples"]
    nb = Notebook(plan["build_stamp"], seed)
    nb.add("commissioning_reflection", "observed", plan["verdict_ref"], {"direction": plan["direction"], "manifest_ids": plan["manifest_ids"], "goal_ref": "verdict.goal"})
    nb.add("cif_ideation", "observed", plan["verdict_ref"], {"mirrored_by_reference": True, "adopted": plan["direction"]})
    nb.add("baseline_record", "measured", plan["baseline_ref"], {s: {"accuracy": d["baseline_accuracy"], "coverage": d["baseline_coverage"]} for s, d in plan["strata"].items()})

    # --- manifest (A17.20): every example's provenance, or no run
    index_rows = mf.load_index(plan["materials_index"])
    man, man_rows = mf.build(plan, index_rows)
    if man["refused"]:
        nb.add("anomaly", "observed", "manifest", {"refused": len(man["refused"])})
        nb.write(out / "notebook.jsonl")
        rec = {"spec_id": plan["spec_id"], "objective_ref": plan["objective_ref"], "verdict_ref": plan["verdict_ref"], "backend": bk.name, "stub": bk.name == "stub",
               "execution_mode": bk.name, "status": "refused", "reason": f"manifest refused {len(man['refused'])} examples; a partial manifest is not a manifest", "manifest": man, "stages": {}, "volatile": {}}
        dump(rec, out / "run-record.json")
        return rec
    Path(out / "training-manifest.jsonl").write_text("\n".join(json.dumps(r, sort_keys=True) for r in man_rows) + "\n")
    nb.add("checkpoint", "measured", man["manifest_hash"], {"stage": "manifest", "examples": man["examples"], "classed_pct": man["classed_pct"]})

    record = {
        "spec_id": plan["spec_id"], "objective_ref": plan["objective_ref"], "verdict_ref": plan["verdict_ref"],
        "backend": bk.name, "stub": bk.name == "stub", "execution_mode": bk.name, "status": "stub" if bk.name == "stub" else "running",
        "evidential_weight": bk.evidential_weight, "seed": seed, "build_stamp": plan["build_stamp"],
        "recipe": plan["recipe"], "manifest": man, "collection_schema_ref": "objective.collection_schema", "stages": {},
    }

    # --- calibration
    cal = {"volumes": plan["calibration"]["volumes"], "estimated_cost_gbp": plan["calibration"]["cost_gbp"], "actual_gpu_hours": 0.0, "per_stratum": {}, "strata_evaluated": [], "strata_missing": []}
    for s, d in plan["strata"].items():
        pts, cpts, tr, hrs = [], [], [], 0.0
        for v in plan["calibration"]["volumes"]:
            r = bk.calibrate(s, v, f"{man['manifest_hash']}#{s}@{v}")
            pts.append((v, r["accuracy"])); cpts.append((v, r["coverage"])); hrs += r["gpu_hours"]
            tr.append(r["train_accuracy"])
            nb.add("checkpoint", "measured", r["checkpoint_ref"], {"stratum": s, "examples": v, "accuracy": r["accuracy"], "train_accuracy": r["train_accuracy"], "coverage": r["coverage"], "gpu_hours": r["gpu_hours"]})
            if r["accuracy"] >= d["accuracy_floor"] and r["coverage"] >= d["coverage_floor"]:
                nb.add("criterion_transition", "measured", r["checkpoint_ref"], {"stratum": s, "examples": v, "transition": "both floors met at this volume"})
        cal["actual_gpu_hours"] = round(cal["actual_gpu_hours"] + hrs, 3)
        a_slope, a_int, _ = fit_log_linear(pts)
        c_slope, c_int, _ = fit_log_linear(cpts)
        need_acc, need_cov = examples_to_reach(a_slope, a_int, d["accuracy_floor"], cap), examples_to_reach(c_slope, c_int, d["coverage_floor"], cap)
        need = None if (need_acc is None or need_cov is None) else max(need_acc, need_cov)
        binding = None if need is None else ("coverage" if need_cov > need_acc else "accuracy")
        if len(pts) >= sf["min_points_for_ci"]:
            lo, hi = bootstrap_ci(pts, d["accuracy_floor"], cap, seed, sf["ci_level"])
            clo, chi = bootstrap_ci(cpts, d["coverage_floor"], cap, seed + ":cov", sf["ci_level"])
            ci = {"kind": "statistical", "level": sf["ci_level"], "low": max(lo, clo), "high": max(hi, chi)}
        else:
            ci = {"kind": "not-reported", "reason": f"{len(pts)} calibration points < {sf['min_points_for_ci']} (policy.scaling_fit.min_points_for_ci)"}
        cal["per_stratum"][s] = {
            "label": d["label"], "points": [{"examples": v, "accuracy": a, "train_accuracy": t, "coverage": c} for (v, a), (_, c), t in zip(pts, cpts, tr)],
            "mde_vs_floor": round(st.mde(d["baseline_accuracy"], d["test_n"], sf.get("ci_level", 0.9)), 4), "undetectable": (d["accuracy_floor"] - d["baseline_accuracy"]) < st.mde(d["baseline_accuracy"], d["test_n"], sf.get("ci_level", 0.9)),
            "seeds": 1, "single_seed": True,
            "fit": {"accuracy": {"form": "log-linear", "slope_per_log2": round(a_slope, 5), "intercept": round(a_int, 5)}, "coverage": {"form": "log-linear", "slope_per_log2": round(c_slope, 5), "intercept": round(c_int, 5)}},
            "accuracy_floor": d["accuracy_floor"], "coverage_floor": d["coverage_floor"],
            "examples_to_accuracy_floor": need_acc, "examples_to_coverage_floor": need_cov, "binding_dimension": binding, "examples_to_floor": need, "ci": ci,
            "available_examples": d["available_examples"], "reachable_within_available": (need is not None and need <= d["available_examples"]),
        }
        cal["strata_evaluated"].append(s)
        if interrupt_after is not None and s == interrupt_after:
            cal["strata_missing"] = [x for x in plan["strata"] if x not in cal["strata_evaluated"]]
            break
    cal["actual_cost_gbp"] = round(cal["actual_gpu_hours"] * plan["gpu_hour_gbp"], 2)
    nb.add("cost_checkpoint", "measured", "calibration", {"estimated_gbp": cal["estimated_cost_gbp"], "actual_gbp": cal["actual_cost_gbp"], "variance_gbp": round(cal["actual_cost_gbp"] - cal["estimated_cost_gbp"], 2)})
    record["stages"]["calibration"] = cal

    if cal["strata_missing"]:
        nb.add("anomaly", "observed", "calibration", {"interrupted_after": interrupt_after, "strata_missing": cal["strata_missing"]})
        record.update(status="interrupted", interruption={"after": interrupt_after, "strata_evaluated": cal["strata_evaluated"], "strata_missing": cal["strata_missing"],
                                                           "report_allowed": plan["interruption"]["report_allowed"], "partial_ruling_ref": None, "retained": plan["interruption"]["retain"]})
        record["stages"]["comparison"] = {"status": "not run: calibration interrupted"}
        record["stages"]["quote"] = {"status": "not quoted: calibration incomplete", "recommended_examples": None, "within_budget": None, "ci_gbp": {}, "strata_not_reachable_within_available": []}
        record["stages"]["full"] = {"status": "not planned: calibration incomplete"}
        record["milestones"] = [{**m, "state": "open"} for m in plan["milestones"]]
        record["moac_pack_request"] = {"kind": "none", "note": "no pack until calibration completes"}
        record["notebook"] = {"entries": len(nb.entries), "head": nb.write(out / "notebook.jsonl")}
        record["volatile"] = {"run_id": "stub-" + hashlib.sha256((seed + plan["build_stamp"] + "int").encode()).hexdigest()[:12], "note": "volatile fields are excluded from the content hash"}
        dump(record, out / "run-record.json")
        return record

    # --- diagnosis (professor names the cause; researcher picks the comparison from it)
    diag = dg.diagnose(plan, cal, {"annotator_agreement": plan["annotator_agreement"]})
    binding = max(cal["per_stratum"], key=lambda s: (cal["per_stratum"][s]["examples_to_floor"] or 0))
    comp_design = dg.choose_comparison(diag, binding, plan)
    record["stages"]["diagnosis"] = {"per_stratum": diag, "binding_stratum": binding, "comparison_design": comp_design}
    for s, d in diag.items():
        nb.add("criterion_transition", "observed", "diagnosis", {"stratum": s, "cause": d["cause"], "first_lever": d["first_lever"]})
    # --- comparison: on the smallest valid stratum (A17.5), testing the lever the diagnosis chose (with vs without)
    cs, v = plan["comparison"]["stratum"], plan["calibration"]["volumes"][-1]
    arm_specs = [{"arm": "A", "config": comp_design["arms"][0]["config"] if comp_design else "incumbent"}, {"arm": "B", "config": comp_design["arms"][1]["config"] if comp_design else "candidate", "expected_effect": comp_design["expected_effect"] if comp_design else None}]
    arms_raw = bk.compare(cs, v, arm_specs, f"{man['manifest_hash']}#{cs}@{v}")
    arms = {}
    mde2 = round(st.mde_two_arm(plan["strata"][cs]["baseline_accuracy"], plan["strata"][cs]["test_n"], sf.get("ci_level", 0.9)), 4)
    for arm, r in arms_raw.items():
        non_target = {s: bk.calibrate(s, v, f"{man['manifest_hash']}#{s}@{v}", arm=arm)["accuracy"] - plan["strata"][s]["baseline_accuracy"] for s in plan["strata"] if s != cs}
        arms[arm] = {"config": r["config"], "target_stratum": cs, "M_a_target_improvement": round(r["accuracy"] - plan["strata"][cs]["baseline_accuracy"], 4),
                     "M_b_non_target_regression_max": round(-min(min(non_target.values()), 0), 4), "coverage": r["coverage"], "compute_to_convergence_gpu_hours": r["compute_to_convergence_gpu_hours"], "seeds": 1}
        nb.add("checkpoint", "measured", r["checkpoint_ref"], {"stage": "comparison", "arm": arm, **{k: arms[arm][k] for k in ("config", "M_a_target_improvement", "M_b_non_target_regression_max", "compute_to_convergence_gpu_hours")}})
    tol, ntr = plan["comparison"]["parity_tolerance"], plan["non_target_regression_max"]
    parity = {"M_a": arms["B"]["M_a_target_improvement"] >= arms["A"]["M_a_target_improvement"] - tol,
              "M_b_A_within_objective": arms["A"]["M_b_non_target_regression_max"] <= ntr, "M_b_B_within_objective": arms["B"]["M_b_non_target_regression_max"] <= ntr}
    delta = arms["B"]["M_a_target_improvement"] - arms["A"]["M_a_target_improvement"]
    record["stages"]["comparison"] = {"stratum": cs, "examples": v, "lever": comp_design, "identical": ["data", "base_model", "eval_set", "compute_cap"], "arms": arms, "parity_tolerance": tol, "non_target_regression_max": ntr,
                                      "delta_B_minus_A": round(delta, 4), "mde_two_arm": mde2, "delta_detectable": abs(delta) >= mde2, "single_seed": True,
                                      "parity": parity, "eligible_for_adoption": all(parity.values()) and abs(delta) >= mde2,
                                      "adoption_evidence": ("sufficient: parity holds and delta exceeds the two-arm MDE" if all(parity.values()) and abs(delta) >= mde2 else
                                                            f"insufficient: delta {delta:+.4f} below two-arm MDE {mde2} at test_n={plan['strata'][cs]['test_n']}; the recipe seat stays empty until the comparison is repeated with more test items or seeds" if all(parity.values()) else "insufficient: parity fails"),
                                      "compute_is_gating": plan["comparison"]["compute_is_gating"],
                                      "owner_verdict": "pending Owner ruling on the measured results (A17.6); no threshold pre-exists the evidence", "cost_gbp": plan["comparison"]["cost_gbp"]}

    # --- quote
    per = {s: min(x["examples_to_floor"], x["available_examples"]) for s, x in cal["per_stratum"].items() if x["examples_to_floor"] is not None}
    rec_examples = sum(per.values()) if per else None
    fr = plan["full_run"]
    def cost_for(n):
        h = n / 1000 * fr["epochs"] * fr["gpu_hours_per_1000_examples_epoch"] + len(plan["strata"]) * fr["eval_gpu_hours_per_stratum"]
        return h, h * plan["gpu_hour_gbp"] * (1 + plan["quote_policy"]["contingency"])
    hours, quote = cost_for(rec_examples or 0)
    quote = round(quote, 2)
    spent = cal["actual_cost_gbp"] + plan["comparison"]["cost_gbp"]
    within = spent + quote <= plan["budget_cap_gbp"]
    if all(x["ci"]["kind"] == "statistical" for x in cal["per_stratum"].values()):
        lo_n = sum(min(x["ci"]["low"], x["available_examples"]) for x in cal["per_stratum"].values())
        hi_n = sum(min(x["ci"]["high"], x["available_examples"]) for x in cal["per_stratum"].values())
        ci_gbp = {"kind": "statistical", "level": sf["ci_level"], "low": round(cost_for(lo_n)[1], 2), "high": round(cost_for(hi_n)[1], 2)}
    else:
        band = plan["quote_policy"]["indicative_band"]
        ci_gbp = {"kind": "indicative-band", "class": plan["quote_policy"]["indicative_band_class"], "band": band, "low": round(quote * (1 - band), 2), "high": round(quote * (1 + band), 2),
                  "reason": "statistical CI not available at this number of calibration points; band is a policy assumption, not a measurement"}
    record["stages"]["quote"] = {"recommended_examples": rec_examples, "recommended_per_stratum": per, "epochs": fr["epochs"], "gpu_hours": round(hours, 2), "quote_gbp": quote, "ci_gbp": ci_gbp,
                                 "spent_so_far_gbp": round(spent, 2), "budget_cap_gbp": plan["budget_cap_gbp"], "within_budget": within,
                                 "over_cap_action": plan["quote_policy"]["over_cap_action"] if not within else None,
                                 "strata_not_reachable_within_available": [s for s, x in cal["per_stratum"].items() if not x["reachable_within_available"]]}
    nb.add("cost_checkpoint", "estimated", "quote", {"quote_gbp": quote, "range": ci_gbp, "within_budget": within})
    record["stages"]["full"] = {"status": "awaiting Owner ruling and objective-owner milestone agreement", "conditional_on": ["comparison.owner_verdict recorded", "quote.within_budget", "MS3 done"],
                                "gate_policy": plan["gate_policy"], "note": "not executed in this build; the backend's full() is never called before the ruling"}
    record["milestones"] = [{**m, "state": "done" if m["id"] in ("MS1", "MS2", "MS3") else "open"} for m in plan["milestones"]]
    prod = plan["production"]
    record["operational_plan"] = {"lens": "industry", "owner_seat": prod["owner_seat"], "rollback": prod["rollback"], "retrain_cadence": prod["retrain_cadence"],
                                  "monitors": {s: {"signal": prod["monitor"].get(s), "capture_condition": prod["capture_condition"].get(s), "coverage_floor": plan["strata"][s]["coverage_floor"], "window": "weekly", "trigger": "below floor two weeks running"} for s in plan["strata"]}, "class": prod["class"], "receipt": prod["receipt"]}
    vals = plan["value"]["per_stratum"]
    record["value_case"] = {"lens": "entrepreneur", "per_stratum": {s: {"value_gbp": vals[s]["gbp"], "basis": vals[s]["basis"], "quoted_cost_gbp": round(cost_for(per.get(s, 0))[1], 2) if per.get(s) else None,
                                                                    "ratio": (round(vals[s]["gbp"] / max(cost_for(per[s])[1], 1), 1) if per.get(s) else None), "reachable": cal["per_stratum"][s]["reachable_within_available"]} for s in plan["strata"]},
                            "phased_path": sorted([s for s in plan["strata"] if per.get(s)], key=lambda s: -(vals[s]["gbp"] / max(cost_for(per[s])[1], 1))),
                            "kill_criteria": ["binding stratum unreachable within available material and no lever with expected effect ≥ gap", "quote exceeds cap after phasing", "diagnosis = leakage"], "class": plan["value"]["class"], "receipt": plan["value"]["receipt"]}

    # --- MOAC pack request keyed to criteria; evidence only, never a verdict
    ev = {"M-a": {"evidence": "comparison.arms[*].M_a_target_improvement", "status": "measured at calibration scale; full-run value pending"},
          "M-b": {"evidence": "comparison.arms[*].M_b_non_target_regression_max vs objective ceiling " + str(ntr), "status": "measured at calibration scale; full-run value pending"},
          "M-d": {"evidence": "recipe_version pending Owner ruling; base_model " + plan["base_model"]["registry_ref"] + "; rights lineage per manifest " + man["manifest_hash"], "status": "partial: recipe_version not yet assigned"},
          "C8-held-out": {"evidence": "sealed test set " + plan["receipts"]["R02"]["resolves_to"], "status": "evidence pending full run"},
          "C8-repro": {"evidence": plan["reproducibility"]["contract"] + "; tolerance ±" + str(plan["reproducibility"]["tolerance_accuracy"]), "status": "policy stated; second-run evidence pending"},
          "C8-provenance": {"evidence": f"manifest {man['manifest_hash']}: {man['examples']} examples, {man['classed_pct']}% classed, lawful basis present={man['lawful_basis_present']}", "status": "met at manifest"},
          "C8-admission": {"evidence": "admission pre-check runs on the artefact (C.6)", "status": "evidence pending artefact"}}
    record["moac_pack_request"] = {"kind": "request", "for": "full run artefact when produced", "criteria_set_ref": "MOAC criteria set version fixed in the frozen objective (C.8 I-1)",
                                   "criteria": [{**c, **ev.get(c["id"], {})} for c in plan["moac_pack_policy"]["criteria"]], "note": plan["moac_pack_policy"]["note"] + " Acceptance is MOAC's; no human in the path (#22)."}
    record["completion_certificate"] = {"status": "not issued: full run not executed (policy.completion_certificate.issued_when)",
                                        "template": {f: None for f in plan["completion_certificate_policy"]["fields"]} | {"manifest_hash": man["manifest_hash"], "backend": bk.name, "execution_mode": bk.name, "objective_ref": plan["objective_ref"]}}
    record["notebook"] = {"entries": len(nb.entries), "head": nb.write(out / "notebook.jsonl")}
    record["volatile"] = {"run_id": "stub-" + hashlib.sha256((seed + plan["build_stamp"]).encode()).hexdigest()[:12], "note": "volatile fields are excluded from the content hash"}
    dump(record, out / "run-record.json")
    return record


if __name__ == "__main__":
    ia = sys.argv[3] if len(sys.argv) > 3 else None
    r = run(load(sys.argv[1]), sys.argv[2], interrupt_after=ia)
    print(f"{r['backend']} run: status={r['status']}", (f"quote £{r['stages']['quote']['quote_gbp']}" if r['status'] == 'stub' else ""))
