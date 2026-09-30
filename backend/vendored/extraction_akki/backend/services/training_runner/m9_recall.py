"""M9-T5 · retained learning and withdrawal: revoke a training dependency (one sealed corpus unit) and account for every descendant.

The unit's membership in each admitted adapter's ingredient manifest is checked ON THE HOST (unit ids only cross the seam; no content).
Every descendant is recalled by a new registry entry, its live serving authority is revoked and the refusal is proven, and a lawful
re-derivation (the same recipe with the unit excluded everywhere) is commissioned so the capability is recovered without the withdrawn
right. Spent GPU budget is not refunded; nothing is deleted; the recalled artefact stays under host custody as evidence.
"""
import json
import shlex
import uuid

from services.model_registry.registry import annotate_model, trained_adapters
from services.training_runner import m9_dispatch as m9
from services.training_runner import m9_serving as serving


def _dir():
    path = m9._jobs_dir() / "revocations"
    path.mkdir(parents=True, exist_ok=True)
    return path


def descendants_of_unit(unit_id):
    """Ask each custody host which admitted/served adapters cite the unit — read from the training manifests, never inferred."""
    from services.training_runner.ssh_seam import execute_remote_command
    by_host = {}
    for model_id, e in trained_adapters().items():
        if e.get("status") in ("recalled",):
            continue
        by_host.setdefault(e["host"], []).append((model_id, e["run_dir"] + "/training_manifest.json"))
    out = []
    for host, rows in by_host.items():
        script = ("import json,sys\nrows=json.loads(sys.argv[1]);u=sys.argv[2]\nres=[]\nfor mid,p in rows:\n"
                  "  try:\n    m=json.load(open(p));res.append({'model_id':mid,'cites':u in set(m['cited_units']),'cited_units':len(m['cited_units']),'excluded':m.get('excluded_unit_ids',[])})\n"
                  "  except Exception as e:\n    res.append({'model_id':mid,'error':type(e).__name__})\nprint(json.dumps(res))")
        command = f"{shlex.quote(m9._remote_python())} -c {shlex.quote(script)} {shlex.quote(json.dumps(rows))} {shlex.quote(unit_id)}"
        result = execute_remote_command(host, command, purpose=f"m9_descendants:{unit_id[:24]}", timeout=60)
        try:
            found = json.loads(result.stdout_redacted.strip())
        except ValueError:
            found = [{"model_id": mid, "error": "HOST_READ_FAILED:" + result.stderr_redacted[:120]} for mid, _ in rows]
        for row in found:
            row["host"] = host
        out.extend(found)
    return out


def revoke_unit(unit_id, reason, principal_id, lawful_ref, rederive=True, gpu_index=0):
    if not unit_id or len(unit_id) > 200:
        raise ValueError("UNIT_ID_REQUIRED")
    revocation_id = "rvk-" + uuid.uuid4().hex[:12]
    at = m9.now()
    descendants = descendants_of_unit(unit_id)
    record = {"revocation_id": revocation_id, "unit_id": unit_id, "reason": reason, "by": principal_id, "at": at, "descendants_checked": descendants, "recalled": [], "rederivations": [],
              "privacy_budget_refunded": False, "evidence_deleted": False}
    pseudo = {"job_id": revocation_id, "northena_run_id": f"run-{uuid.uuid4().hex[:12]}", "northena_trace_id": f"trc-{uuid.uuid4().hex[:12]}",
              "governing_artifact_ref": {"artifact_type": "objective_request", "artifact_id": "M9-TRAINING-RIGHTS-WITHDRAWAL", "version": revocation_id}, "lawful_basis_ref": str(lawful_ref)}
    m9._ledger(pseudo, "admit", "admitted", f"m9_training_unit_revoked:{unit_id[:60]}", {"reason": reason[:120], "by": principal_id})
    record["ledger_rows"] = pseudo.get("ledger_rows")
    adapters = trained_adapters()
    for row in descendants:
        if not row.get("cites"):
            continue
        model_id = row["model_id"]
        entry = adapters[model_id]
        recall = {"model_id": model_id, "previous_status": entry.get("status"), "at": m9.now()}
        if (entry.get("serving") or {}).get("status") == "running":
            recall["serving_withdrawal"] = serving.withdraw(model_id, f"training dependency revoked ({revocation_id}): {reason}", principal_id, new_status="recalled")
        else:
            recall["registry_version_after"] = annotate_model(model_id, {"status": "recalled", "recall": {"revocation_id": revocation_id, "unit_id": unit_id, "reason": reason, "at": recall["at"], "by": principal_id}},
                                                             authority_source=f"M9-T5 recall by {principal_id}: unit {unit_id} revoked ({revocation_id})")
        if "serving_withdrawal" in recall:
            recall["registry_version_after"] = annotate_model(model_id, {"recall": {"revocation_id": revocation_id, "unit_id": unit_id, "reason": reason, "at": recall["at"], "by": principal_id}},
                                                             authority_source=f"M9-T5 recall record for {model_id} ({revocation_id})")
        record["recalled"].append(recall)
        if rederive and entry.get("variant", "full") == "full":
            record["rederivations"].append(_rederive(entry, unit_id, revocation_id, principal_id, lawful_ref, gpu_index))
    record["descendant_count"] = sum(1 for r in descendants if r.get("cites"))
    (_dir() / f"{revocation_id}.json").write_text(json.dumps(record, indent=1, default=str))
    return record


def _rederive(entry, unit_id, revocation_id, principal_id, lawful_ref, gpu_index):
    """Lawful re-derivation: same base, recipe and sealed corpus with the revoked unit excluded everywhere; a new artefact that must re-pass admission."""
    source = m9.load_job(entry["training_job_id"])
    params = dict((source or {}).get("params") or {})
    recipe = {k: v for k, v in (params.get("recipe") or {}).items() if k not in ("interrupt_after_steps",)}
    params.update({"recipe": recipe, "base": entry["base"]["registry_id"], "corpus_id": entry["corpus_id"], "gpu_index": gpu_index,
                   "excluded_unit_ids": sorted(set(entry.get("excluded_unit_ids") or []) | {unit_id}), "rederived_from": entry["model_id"], "revocation_id": revocation_id,
                   "acceptance_floor": params.get("acceptance_floor", (source or {}).get("run_certificate", {}).get("outcome_floor") or 0.9)})
    try:
        job = m9.submit("train", params, entry["host"], principal_id, lawful_ref, timeout=90)
        return {"from_model_id": entry["model_id"], "job_id": job["job_id"], "status": job["status"], "reason": job.get("reason"), "excluded_unit_ids": params["excluded_unit_ids"]}
    except Exception as exc:
        return {"from_model_id": entry["model_id"], "status": "refused", "reason": f"{type(exc).__name__}: {str(exc)[:200]}"}


def list_records():
    out = []
    for path in sorted(_dir().glob("rvk-*.json")):
        try:
            out.append(json.loads(path.read_text()))
        except (OSError, ValueError):
            continue
    return out
