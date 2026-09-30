"""training-studio report: technical report on the WPW-8 skeleton, from the run record only (WPW-13).
Every figure carries its class and receipt (WPW-9). Where the record is silent the report says so."""
import json, sys
from pathlib import Path


def load(p):
    return json.loads(Path(p).read_text())


def pct(v):
    return f"{v*100:.1f}%"


def render(plan, rec):
    L = []
    w = rec["evidential_weight"]
    L.append(f"# Technical report: {plan['title']}\n")
    L.append(f"Run `{plan['spec_id']}` · objective `{plan['objective_ref']}` · direction {plan['direction']} · backend **{rec['backend']}** · status **{rec['status']}**\n")
    if rec["backend"] == "stub":
        L.append(f"> STUB RUN. {w}\n")
    if rec["status"] == "interrupted":
        it = rec["interruption"]
        L.append(f"> INTERRUPTED after {it['after']}. Strata evaluated: {', '.join(it['strata_evaluated'])}. Strata missing: {', '.join(it['strata_missing'])}. Reported under partial ruling {it.get('partial_ruling_ref')}. The partial record is retained (WPW-7).\n")
    L.append("## 1. Problem and objective\n")
    L.append(f"{plan['task']} on {plan['modality']}; {len(plan['strata'])} declared population strata. Acceptance is two-dimensional per stratum (accuracy × coverage); gate policy: **{plan['gate_policy']}**.\n")
    L.append("| Stratum | Share | Baseline acc. | Floor acc. | Gap (pp) | Floor cov. | Available examples |\n|---|---|---|---|---|---|---|")
    for s, d in plan["strata"].items():
        L.append(f"| {s} {d['label']} | {pct(d['share'])} | {pct(d['baseline_accuracy'])} | {pct(d['accuracy_floor'])} | {d['gap_pp']} | {pct(d['coverage_floor'])} | {d['available_examples']:,} |")
    L.append(f"\n[measured] Receipt R01, R03: {plan['receipts']['R01']['resolves_to']}; {plan['receipts']['R03']['resolves_to']}\n")
    L.append("## 2. Data statement\n")
    L.append("| Material | Stratum | Examples | Class | Lawful basis | Hash |\n|---|---|---|---|---|---|")
    for mid, m in plan["materials"].items():
        L.append(f"| {mid} {m['source']} | {m['stratum']} | {m['examples']:,} | {m['class']} | {m['lawful_basis']} | `{m['hash']}` |")
    man = rec["manifest"]
    L.append(f"\nTraining manifest `{man['manifest_hash']}`: {man['examples']:,} examples, {man['classed_pct']}% classed, lawful basis present: {man['lawful_basis_present']}, refused: {len(man['refused'])}. Per-example provenance in `training-manifest.jsonl` (A17.20). Selection: {man['selection_rule']}.\n")
    L.append("| Stratum | Examples | By class | By lawful basis |\n|---|---|---|---|")
    for s, c in man["per_stratum"].items():
        L.append(f"| {s} | {c['total']:,} | {', '.join(f'{k} {v:,}' for k, v in c['by_class'].items())} | {', '.join(f'{k} {v:,}' for k, v in c['by_basis'].items())} |")
    cs = plan["collection_schema"]
    L.append(f"\nCollection schema (unit: {cs['unit']}): fields {', '.join(cs['fields'])}; quality gates {json.dumps(cs['quality_gates'])}; labelling: {cs['labelling_protocol']}; admission: {cs['admission']}. [{cs['class']}] Receipt {cs['receipt']}: {plan['receipts'][cs['receipt']]['resolves_to']}\n")
    L.append(f"[measured] Receipt R04: {plan['receipts']['R04']['resolves_to']}\n")
    L.append("## 3. Baseline record\n")
    L.append(f"Baseline run {plan['receipts']['R03']['resolves_to']} on the sealed test set ({plan['receipts']['R02']['resolves_to']}). Base model: `{plan['base_model']['registry_ref']}`, role: {plan['base_model']['role']}; production selection {plan['base_model']['production_selection']}.\n")
    L.append("## 3b. Objective critique (four lenses)\n")
    L.append("Full table in `critique.md`. Escalations to the objective owner are listed there; the adopted verdict records which objections were accepted and which overruled.\n")
    L.append("## 4. Method\n")
    L.append(f"Adopted direction {plan['direction']} under the recorded verdict `{plan['verdict_ref']}`. Recipe seat: **{plan['recipe']['state']}** ({plan['recipe']['training_params_ref']}). Calibration at {plan['calibration']['volumes']} examples per stratum, {plan['calibration']['epochs']} epochs each; two-arm optimizer comparison on the smallest valid stratum ({plan['comparison']['stratum']}).\n")
    L.append("## 5. Setup and reproducibility\n")
    calst = rec["stages"]["calibration"]
    L.append(f"Execution mode: {rec['execution_mode']}. Reproducibility contract: {plan['reproducibility']['contract']} (accuracy ±{plan['reproducibility']['tolerance_accuracy']}, coverage ±{plan['reproducibility']['tolerance_coverage']}); canon: {plan['reproducibility']['canon']}. Seed `{plan['seed']}`. Calibration cost: estimated £{calst['estimated_cost_gbp']} [estimated, R05], actual £{calst.get('actual_cost_gbp', '—')} ({calst['actual_gpu_hours']} GPU h) [{'stub' if rec['backend']=='stub' else 'measured'}]; comparison cost £{plan['comparison']['cost_gbp']} [estimated, R05].\n")
    L.append("## 6. Results on held-out material\n")
    cal = rec["stages"]["calibration"]["per_stratum"]
    vols = plan['calibration']['volumes']
    L.append("| Stratum | " + " | ".join(f"acc @{v}" for v in vols) + " | " + " | ".join(f"cov @{v}" for v in vols) + " | To acc. floor | To cov. floor | Binding | CI | Reachable |\n|---|" + "---|" * (2 * len(vols) + 5))
    for s, x in cal.items():
        ci = f"{x['ci']['low']}–{x['ci']['high']} (prior sensitivity, not CI)" if x["ci"]["kind"] == "prior-sensitivity" else x['ci'].get('reason','not reported')
        L.append(f"| {s} | " + " | ".join(pct(p["accuracy"]) for p in x["points"]) + " | " + " | ".join(pct(p["coverage"]) for p in x["points"]) + f" | {x['examples_to_accuracy_floor'] if x['examples_to_accuracy_floor'] is not None else 'not on this curve'} | {x['examples_to_coverage_floor'] if x['examples_to_coverage_floor'] is not None else 'not on this curve'} | {x['binding_dimension']} | {ci} | {'yes' if x['reachable_within_available'] else 'no'} |")
    missing = rec["stages"]["calibration"].get("strata_missing", [])
    for s in missing:
        L.append(f"| {s} | " + " | ".join("—" for _ in range(2 * len(vols))) + " | not evaluated | not evaluated | — | — | unknown |")
    L.append(f"\n[{ 'stub' if rec['backend']=='stub' else 'measured'}] Evaluated on {plan['receipts']['R02']['resolves_to']}. Failed strata are reported as plainly as passed ones.\n")
    dgn = rec["stages"].get("diagnosis")
    if not dgn:
        L.append("### Diagnosis per stratum\n\nNot run: calibration incomplete.\n")
    if dgn:
        L.append("### Diagnosis per stratum (professor names the cause; researcher picks the lever)\n")
        L.append("| Stratum | Cause | Test | Curve slope ratio | Train/held-out gap | Annotator agreement | First lever | Expected effect (class) |\n|---|---|---|---|---|---|---|---|")
        for s, d in dgn["per_stratum"].items():
            ee = d["expected_effect"]
            ee_txt = (f"{ee['low']}–{ee['high']} {ee['metric']} ({ee['class']})" if ee and ee.get("low") is not None else (f"— ({ee['class']})" if ee else "—"))
            L.append(f"| {s} | **{d['cause']}** | {d['test']} | {d['evidence']['slope_last_over_first']} | {d['evidence']['train_heldout_gap']} | {d['evidence']['annotator_agreement']} | {d['first_lever']} | {ee_txt} |")
        L.append(f"\nBinding stratum: {dgn['binding_stratum']}. Comparison design: {dgn['comparison_design']['rationale'] if dgn['comparison_design'] else 'none'}.\n")
    comp = rec["stages"]["comparison"]
    if "arms" not in comp:
        L.append(f"### Two-arm comparison\n\n{comp['status']}.\n")
    q = rec["stages"]["quote"]
    if "quote_gbp" not in q:
        L.append(f"### Quote\n\n{q['status']}.\n")
    if "arms" in comp:
      L.append(f"### Two-arm comparison on {comp['stratum']} at {comp['examples']} examples — lever: {comp['lever']['lever'] if comp.get('lever') else '—'} (single-seed)\n")
      L.append("| Arm | Configuration | M-a target improvement | M-b non-target regression (max) | Coverage | Compute to convergence (GPU h) |\n|---|---|---|---|---|---|")
      for a, x in comp["arms"].items():
        L.append(f"| {a} | {x['config']} | {x['M_a_target_improvement']:+.4f} | {x['M_b_non_target_regression_max']:.4f} | {pct(x['coverage'])} | {x['compute_to_convergence_gpu_hours']} |")
      L.append(f"\nDelta B−A {comp['delta_B_minus_A']:+.4f} vs two-arm MDE {comp['mde_two_arm']}: {'detectable' if comp['delta_detectable'] else 'NOT detectable'}. Adoption evidence: **{comp['adoption_evidence']}**.")
      pr = comp["parity"]
      L.append(f"\nEligibility: M-a parity within {comp['parity_tolerance']}: {pr['M_a']}; M-b within objective ceiling {comp['non_target_regression_max']}: arm A {pr['M_b_A_within_objective']}, arm B {pr['M_b_B_within_objective']}. Eligible for adoption: **{comp['eligible_for_adoption']}**. Compute is reported, not gating. **Verdict: {comp['owner_verdict']}.**\n")
    if "quote_gbp" in q:
      L.append("### Quote for the full run\n" if q['quote_scope']=='full_run' else "### Partial estimate — not a full-run quote\n\nSome strata require more labelled examples than are available. Their uncapped forecasts remain in the run record; no full run is recommended.\n")
      rng = q["ci_gbp"]
      rng_txt = f"{rng['level']*100:.0f}% CI £{rng['low']}–£{rng['high']}" if rng["kind"] == "statistical" else f"indicative band ±{rng['band']*100:.0f}% £{rng['low']}–£{rng['high']} [estimated: {rng['reason']}]"
      L.append(f"Recommended examples: {q['recommended_examples']:,} ({', '.join(f'{s}: {n:,}' for s, n in q['recommended_per_stratum'].items())}); {q['epochs']} epochs; {q['gpu_hours']} GPU h. **Quote £{q['quote_gbp']}** ({rng_txt}), spent so far £{q['spent_so_far_gbp']}, cap £{q['budget_cap_gbp']}, within budget: {q['within_budget']}." + (f" Over-cap action: {q['over_cap_action']}." if q['over_cap_action'] else "") + "\n")
    if not rec.get("operational_plan"):
        L.append("\n### Operational plan (industry lens)\n\nNot produced: run incomplete.\n")
    if not rec.get("value_case"):
        L.append("\n### Value case (entrepreneur lens)\n\nNot produced: run incomplete.\n")
    if rec.get("operational_plan"):
        op = rec["operational_plan"]
        L.append("\n### Operational plan (industry lens)\n")
        L.append(f"Owner seat: {op['owner_seat']}. Rollback: {op['rollback']}. Retrain cadence: {op['retrain_cadence']}. [{op['class']}] Receipt {op['receipt']}\n")
        L.append("| Stratum | Capture condition | Monitor | Coverage floor | Window | Trigger |\n|---|---|---|---|---|---|")
        for s, m in op["monitors"].items():
            L.append(f"| {s} | {m['capture_condition']} | {m['signal']} | {pct(m['coverage_floor'])} | not calibrated | {m['status']} |")
    if rec.get("value_case"):
        vc = rec["value_case"]
        L.append("\n### Value case (entrepreneur lens)\n")
        L.append("| Stratum | Value £/yr | Basis | Quoted cost £ | Ratio | Reachable |\n|---|---|---|---|---|---|")
        for s, v in vc["per_stratum"].items():
            L.append(f"| {s} | {v['value_gbp']:,} | {v['basis']} | {v['quoted_cost_gbp'] if v['quoted_cost_gbp'] is not None else '—'} | {v['ratio'] if v['ratio'] is not None else '—'} | {'yes' if v['reachable'] else 'no'} |")
        L.append(f"\nPhased path by value/cost: {' → '.join(vc['phased_path'])}. Kill criteria: {'; '.join(vc['kill_criteria'])}. [{vc['class']}] Receipt {vc['receipt']}\n")
    L.append("## 7. Ablations\n\nNone run. The record is silent on ablations.\n")
    L.append("## 8. Limitations (four lenses)\n")
    cal_ = rec["stages"]["calibration"]["per_stratum"]
    L.append(f"- **Statistical (professor):** all calibration numbers are single-seed; CIs {'reported' if all(x['ci']['kind']=='statistical' for x in cal_.values()) else 'not reported at this number of points'}; MDE vs floor per stratum: " + ", ".join(f"{s} {x['mde_vs_floor']*100:.1f}pp" for s, x in cal_.items()) + ". What would change the conclusion: a second seed disagreeing beyond the prior seed SD.")
    if "arms" in comp:
        L.append(f"- **Methodological (researcher):** one comparison, one lever ({comp['lever']['lever'] if comp.get('lever') else '—'}); no ablations; delta {'below' if not comp['delta_detectable'] else 'above'} two-arm MDE. What would change it: a repeat with ≥3 seeds or a larger sealed set on {comp['stratum']}.")
    if rec.get("operational_plan"):
        L.append(f"- **Operational (industry):** calibration material may not match production capture on every stratum (see capture conditions); monitors are proposed, not yet live. What would change it: a production drift signal in the first month.")
    if rec.get("value_case"):
        L.append(f"- **Economic (entrepreneur):** value figures are the owner's estimates [{rec['value_case']['class']}]; costs are quotes at prior rates. What would change it: the binding stratum's curve projecting beyond available material.")
    for g in plan["coverage"]["cannot_say"]:
        L.append(f"- **{g['gap']}**: {g['reason']}; closes with {g['closes_with']}.")
    if q.get("strata_not_reachable_within_available"):
        L.append(f"- Strata not reachable within available material: {', '.join(q['strata_not_reachable_within_available'])}.")
    L.append("\n## 9. Negative results\n\nNone recorded in this run. A refused run's record is retained (WPW-7).\n")
    L.append("## Milestones\n")
    for m in rec["milestones"]:
        L.append(f"- {m['id']} [{m['state']}] {m['done_when']} — owner: {m['owner']}")
    L.append("\n## MOAC pack request\n")
    mp = rec["moac_pack_request"]
    if mp.get("criteria"):
        L.append("| Criterion | Source | Evidence | Status |\n|---|---|---|---|")
        for c in mp["criteria"]:
            L.append(f"| {c['id']} {c['name']} | {c['source']} | {c['evidence']} | {c['status']} |")
        L.append(f"\n{mp['note']}\n")
    else:
        L.append(f"{mp['note']}\n")
    if rec.get("completion_certificate"):
        L.append(f"\n## Completion certificate\n\n{rec['completion_certificate']['status']}. Template fields: {', '.join(rec['completion_certificate']['template'].keys())}.\n")
    if rec.get("notebook"):
        L.append(f"\n## Notebook\n\n{rec['notebook']['entries']} entries, hash-chained, head `{rec['notebook']['head']}` (`notebook.jsonl`, WPW-3/4). Human contributions and CIF events are recorded by reference; correlation only.\n")
    L.append("---\n*Instrument: training-studio (WPW-17). Authors are humans; this report names none until the objective owner signs.*\n")
    return "\n".join(L)


if __name__ == "__main__":
    out = Path(sys.argv[3])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(load(sys.argv[1]), load(sys.argv[2])))
    print(f"report -> {out}")
