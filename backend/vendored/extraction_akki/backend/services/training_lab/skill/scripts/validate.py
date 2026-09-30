"""training-studio validate: schemas + blockers before the run; lints on the record after.
Blockers are measurable (RV shape). Review items are routed (QA shape). Outcome set: pass | finding-not-blocking | blocked."""
import json, re, sys
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).parent))
import manifest as mf  # noqa: E402
import notebook as nbk  # noqa: E402
TOKEN = re.compile(r"\{[^}]+\}")


def load(p):
    return json.loads(Path(p).read_text())


def retyped(spec):
    """Literal numbers in a run plan where references belong (volumes, thresholds, budgets)."""
    out = []
    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("spec_id", "seed", "build_stamp", "objective_ref", "brief_ref", "verdict_ref", "id", "stage", "arm", "optimizer"):
                    continue
                walk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            out.append(f"{path}: literal {o}; thresholds, volumes and budgets come from the objective, brief or policy by reference")
    walk(spec, "plan")
    return out


def pre(fx):
    fx = Path(fx)
    blockers, review = [], []
    obj, brief, verdict, plan = load(fx / "objective.json"), load(fx / "brief.json"), load(fx / "verdict.json"), load(fx / "plan.json")
    for kind, d in (("objective", obj), ("brief", brief), ("verdict", verdict), ("plan", plan)):
        jsonschema.validate(d, load(ROOT / "schemas" / f"{kind}.schema.json"))
    # A17 §17.3: target rejected at definition without strata + 2D acceptance + existing test set
    for s, d in obj["population"]["strata"].items():
        if not d.get("test_set_ref") or d["test_set_ref"] not in obj["receipts"]:
            blockers.append(f"stratum {s}: no resolvable test_set_ref (target rejected at definition)")
        acc = obj["acceptance"]["per_stratum"].get(s)
        if not acc or "accuracy_floor" not in acc or "coverage_floor" not in acc:
            blockers.append(f"stratum {s}: acceptance is not two-dimensional")
    # C.20 manifest: 100% classed with lawful basis and hash
    policy = load(ROOT / "policies" / "run-policy.json")
    for mid, m in obj["materials"].items():
        for f in policy["manifest"]["required_fields"]:
            if not m.get(f):
                blockers.append(f"material {mid}: missing {f}")
        if m.get("lawful_basis") and m["lawful_basis"] not in policy["manifest"]["lawful_bases"]:
            blockers.append(f"material {mid}: lawful_basis '{m['lawful_basis']}' not recognised")
        if m.get("receipt") and m["receipt"] not in obj["receipts"]:
            blockers.append(f"material {mid}: receipt {m['receipt']} does not resolve")
    # A17.20: manifest counts must match the per-example index
    idx = fx / policy["manifest"]["index_file"]
    if not idx.exists():
        blockers.append(f"materials index {policy['manifest']['index_file']} missing; per-example provenance is required (A17.20)")
    else:
        blockers += mf.check_counts(obj["materials"], mf.load_index(idx))
    # A17.2: recipe seat ships empty unless evidence is attached
    if plan["recipe"].get("state") != "empty" and not plan["recipe"].get("comparison_ref"):
        blockers.append("recipe seat filled without an attached measured comparison (A17.2/A17.4)")
    # verdict integrity
    if verdict["adopted"] not in {c["idea_id"] for c in verdict["candidates"] if c["verdict"] == "adopt"}:
        blockers.append("verdict: adopted id is not an adopted candidate")
    if not verdict.get("confirmed_by"):
        blockers.append("verdict: no confirmer")
    # no decision fields anywhere in inputs
    blob = json.dumps(plan) + json.dumps(verdict)
    if re.search(r'"(accepted|admitted|released|approved)"\s*:\s*true', blob):
        blockers.append("input carries a decision field; skills do not decide")
    blockers += retyped(plan)
    if obj["base_model"].get("role") == "ci-fixture-only":
        review.append("base model is the CI fixture (A17.10); production base is named after census (A17.11)")
    review.append("Are ST3/ST4 floors achievable within available material, or is the objective owner accepting a documented miss?")
    return blockers, review


def post(record_path, plan_path):
    r, plan = load(record_path), load(plan_path)
    blockers, review = [], []
    if r["status"] == "refused":
        blockers.append(f"run refused: {r['reason']}")
        return blockers, review
    if r["backend"] == "stub" and (not r.get("stub") or r["status"] not in ("stub", "interrupted")):
        blockers.append("stub run must carry stub=true and a status of stub or interrupted")
    nbp = Path(record_path).parent / "notebook.jsonl"
    ok, at = nbk.verify(nbp) if nbp.exists() else (False, None)
    if not ok:
        blockers.append(f"notebook chain broken or missing (seq {at})")
    if r["manifest"]["classed_pct"] < 100 or not r["manifest"]["lawful_basis_present"]:
        blockers.append("manifest not 100% classed with lawful basis")
    if re.search(r'"(accepted|adopted|admitted|released)"\s*:\s*true', json.dumps(r)):
        blockers.append("run record carries a decision; the runner may not decide")
    cal = r["stages"]["calibration"]["per_stratum"]
    if r["status"] == "interrupted":
        it = r["interruption"]
        if not it.get("partial_ruling_ref"):
            blockers.append(f"interrupted after {it['after']}: strata missing {it['strata_missing']}; report blocked until the objective owner's partial ruling is referenced (partial_ruling_ref)")
        else:
            review.append(f"partial run reported under ruling {it['partial_ruling_ref']}; strata missing {it['strata_missing']}")
        return blockers, review
    for s in plan["strata"]:
        if s not in cal:
            blockers.append(f"stratum {s} missing from calibration report (failed strata reported as plainly as passed)")
        else:
            for k in ("examples_to_accuracy_floor", "examples_to_coverage_floor", "binding_dimension"):
                if k not in cal[s]:
                    blockers.append(f"stratum {s}: {k} not evaluated (acceptance is two-dimensional)")
    comp = r["stages"]["comparison"]
    for arm in comp["arms"].values():
        for k in ("M_a_target_improvement", "M_b_non_target_regression_max", "compute_to_convergence_gpu_hours"):
            if k not in arm:
                blockers.append(f"comparison arm {arm.get('optimizer')}: {k} not reported (A17.6)")
    if "owner_verdict" not in comp or "pending" not in str(comp["owner_verdict"]):
        blockers.append("comparison verdict is not left to the Owner seat (A17.6)")
    q = r["stages"]["quote"]
    if q["quote_gbp"] and ("low" not in q["ci_gbp"] or q["ci_gbp"].get("kind") not in ("statistical", "indicative-band")):
        blockers.append("quote lacks a range (A17.20: never a point estimate)")
    if q["ci_gbp"].get("kind") == "indicative-band" and q["ci_gbp"].get("class") != "estimated":
        blockers.append("indicative band must carry class estimated")
    for k in ("M_b_A_within_objective", "M_b_B_within_objective"):
        if k not in comp["parity"]:
            blockers.append(f"comparison does not test {k} against objective.non_target_regression_max")
    if not q["within_budget"] and not q.get("over_cap_action"):
        blockers.append("over-cap quote without routing to a named person (#11)")
    if q["strata_not_reachable_within_available"]:
        review.append(f"strata not reachable within available material: {q['strata_not_reachable_within_available']}; objective owner to rule on documented miss vs more material")
    return blockers, review


if __name__ == "__main__":
    fx, out = Path(sys.argv[1]), Path(sys.argv[2])
    b, rv = pre(fx)
    rec = out / "out" / "run-record.json"
    if rec.exists():
        b2, r2 = post(rec, out / "resolved" / "run_plan.resolved.json")
        b, rv = b + b2, rv + r2
    report = {"outcome": "blocked" if b else ("finding-not-blocking" if rv else "pass"), "blockers": b, "review": rv}
    (out / "validate-report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    sys.exit(1 if b else 0)
