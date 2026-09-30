"""Re-adjudicate a banked M9 run certificate under the owner-ruled per-stratum criterion (2026-09-30 · 1a).

Nothing is retrained and no floor is lowered: the certificate's measured per-stratum accuracies are re-read against the
Outcome's recorded threshold (Docs 17–19: acceptance is a per-stratum threshold recorded on the Outcome at definition time)
plus a no-regression-below-base condition. The original refusal stays on file; the new admission record cites the ruling
(Canon 8 §43 · correction by new entry only). Admission still runs the unchanged ceremony (contract → purpose → lineage → floors).
"""
import copy
import json
import os
from pathlib import Path

from services.training_runner import m9_dispatch as m9

RULING_REF = m9.OWNER_RULING_20260930


def _dir():
    path = m9._jobs_dir() / "readjudications"
    path.mkdir(parents=True, exist_ok=True)
    return path


def per_stratum_verdict(per_stratum, outcome_floor):
    rows = {}
    for stratum, r in per_stratum.items():
        acc, base = r.get("accuracy"), r.get("base_accuracy") or 0.0
        if acc is None:
            continue
        rows[stratum] = {"accuracy": acc, "base_accuracy": base, "meets_outcome_floor": acc >= outcome_floor, "no_regression_below_base": acc >= base,
                         "passes": acc >= outcome_floor and acc >= base}
    coverage = sum(1 for r in rows.values() if r["passes"]) / max(1, len(rows))
    return rows, coverage


def _variant_inputs(job, run, cert, variant):
    if variant == "full":
        return (copy.deepcopy(cert["moac"]["card"]), cert["per_stratum"], job["job_id"], cert["artefact_sha256"], run["artefact"]["path"], cert.get("admission"))
    held = run["pruning"]["eval"]["held"]["per_stratum"]
    per = {s: {"accuracy": r["accuracy"], "base_accuracy": run["base_eval"]["held"]["per_stratum"][s]["accuracy"]} for s, r in held.items()}
    return (copy.deepcopy(run["pruning"]["moac_card"]), per, job["job_id"] + "-pruned", run["pruning"]["artefact_sha256"],
            str(Path(run["artefact"]["path"]).parent / "pruned_adapter"), (cert.get("pruned_artefact") or {}).get("admission"))


def readjudicate(job_id, outcome_floor, floor_source, variant="full", actor=None):
    from services.model_admission import ceremony
    job = m9.load_job(job_id)
    if not job or not job.get("run_certificate") or not job.get("receipt"):
        raise ValueError("NO_BANKED_CERTIFICATE_FOR:" + str(job_id))
    if variant not in ("full", "pruned"):
        raise ValueError("VARIANT_MUST_BE_full_OR_pruned")
    cert = job["run_certificate"]
    run = job["receipt"]["result"]
    run = run["stages"]["train"] if job["phase"] == "pipeline" else run
    card, per, model_id, artefact_sha, adapter_dir, original = _variant_inputs(job, run, cert, variant)
    rows, coverage = per_stratum_verdict(per, outcome_floor)
    record = {"job_id": job_id, "model_id": model_id, "variant": variant, "ruling_ref": RULING_REF, "outcome_floor": outcome_floor, "floor_source": floor_source,
              "actor": actor, "per_stratum": rows, "coverage_strata": round(coverage, 6), "original_admission": original, "artefact_sha256": artefact_sha, "at": m9.now()}
    if not run["distance_probe"]["egress_permitted"]:
        record["readjudicated"] = {"outcome": "refused", "reason": "dap31_egress_refused", "refusal_note": "; ".join(run["distance_probe"]["refusals"])}
    else:
        card["coverage_strata"] = {"measured_value": round(coverage, 6), "unit": "fraction_of_strata_meeting_floor",
                                   "method_of_measurement": (f"Share of target strata whose held-out accuracy meets the Outcome's recorded per-stratum floor ({outcome_floor}; source: {floor_source}) "
                                                             f"without regressing below the base. {RULING_REF}. gate_policy GATES release (A17.19b). Re-adjudicated from the banked certificate; no retraining."),
                                   "floor_value": 1.0, "canon_anchor": "§26.2 · per-stratum acceptance · Docs 17–19 threshold recorded on the Outcome"}
        card["computed_at"] = m9.now()
        entry = m9.adapter_registry_entry(job, run, model_id, artefact_sha, adapter_dir, RULING_REF)
        entry["readjudication_ref"] = f"{job_id}:{variant}:{record['at']}"
        outcome = ceremony.run_admission(card, entry)
        record["readjudicated"] = {"outcome": outcome.outcome, "reason": outcome.reason, "refusal_note": outcome.refusal_note, "registry_version_after": outcome.registry_version_after,
                                   "record_ref": outcome.record_ref, "computed_at": outcome.computed_at}
        record["moac_card"] = card
        if outcome.outcome == "admitted":
            record["whitepaper"] = _whitepaper(job, run, model_id, record)
    (_dir() / f"{model_id}_{record['at'].replace(':', '')}.json").write_text(json.dumps(record, indent=1, default=str))
    target = cert if variant == "full" else cert.setdefault("pruned_artefact", {})
    target.setdefault("readjudications", []).append({k: record[k] for k in ("ruling_ref", "outcome_floor", "floor_source", "coverage_strata", "readjudicated", "at")})
    target["admission_current"] = record["readjudicated"]
    if variant == "full":
        cert["per_stratum"] = {s: {**r, "meets_outcome_floor_no_regression": rows.get(s, {}).get("passes")} for s, r in cert["per_stratum"].items()}
    (m9._jobs_dir() / f"run_certificate_{job_id}.json").write_text(json.dumps(cert, indent=1, default=str))
    m9.save_job(job)
    return record


def _whitepaper(job, run, model_id, record):
    """Doc 14 §33: a new whitepaper draft cites the admission now on record; the earlier draft (citing the refusal) is retained."""
    try:
        from services.whitepapers import draft as _wp
        safe = model_id.replace("-", "_").lower()
        wp = _wp.draft_whitepaper({"whitepaper_id": f"wp_{safe}_readj_{record['at'][:10].replace('-', '')}", "run_ref": job["job_id"], "drafted_at": m9.now(), "drafted_by": "m9_readjudication",
                                   "cites_model_admission_id": model_id, "cites_baseline_line_id": f"bl_{job['job_id'].replace('-', '_')}",
                                   "summary_note": (f"M9 governed run {job['job_id']} ({record['variant']} artefact) re-adjudicated under {RULING_REF}: coverage_strata {record['coverage_strata']:.4f} "
                                                    f"against the Outcome floor {record['outcome_floor']}; MOAC M-a {run['moac']['m_a_improvement']:+.4f}, M-b {run['moac']['m_b_non_target_regression']:+.4f}; "
                                                    f"admission {record['readjudicated']['outcome']}, registry v{record['readjudicated']['registry_version_after']}."), "retention_class": "standard"})
        return {"drafted": True, "whitepaper_id": getattr(wp, "whitepaper_id", None) or (wp.get("whitepaper_id") if isinstance(wp, dict) else None)}
    except Exception as exc:
        return {"drafted": False, "reason": f"{type(exc).__name__}: {str(exc)[:300]}"}


def list_records():
    out = []
    for path in sorted(_dir().glob("*.json")):
        try:
            out.append(json.loads(path.read_text()))
        except (OSError, ValueError):
            continue
    return out
