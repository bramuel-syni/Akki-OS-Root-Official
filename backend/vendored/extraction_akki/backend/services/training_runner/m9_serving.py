"""M9.4 governed serving control plane. Only an artefact the registry holds as admitted may be loaded; the host verifies the
tree hash before serving; every answer carries lineage; E1 can revoke the serving authority (the host refuses from the next
request) and stop the server. Load tests run on the host against the loopback server. E1 relays bounded requests only —
corpora and weights never leave the tenant host."""
import base64
import json
import os
import shlex
from pathlib import Path

from services.model_registry.registry import annotate_model, attest_model, current_registry_version
from services.training_runner import m9_dispatch as m9

PORT_BASE = 8611
MAX_TEXTS, MAX_CHARS = 16, 2000


def _dir():
    path = m9._jobs_dir() / "serving"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _remote(host, command, purpose, timeout=60):
    from services.training_runner.ssh_seam import execute_remote_command
    return execute_remote_command(host, command, purpose=purpose, timeout=timeout)


def _entry(model_id):
    entry = attest_model(model_id)
    if entry.get("role") != "trained_adapter":
        raise ValueError("NOT_A_TRAINED_ADAPTER:" + model_id)
    return entry


def _serving_job(entry):
    job_id = ((entry.get("serving") or {}).get("job_id"))
    return m9.refresh(job_id) if job_id else None


def _port_for(model_id):
    used = {int((e.get("serving") or {}).get("port") or 0) for e in _all_adapters().values() if (e.get("serving") or {}).get("status") == "running"}
    port = PORT_BASE
    while port in used:
        port += 1
    return port


def _all_adapters():
    from services.model_registry.registry import trained_adapters
    return trained_adapters()


def start(model_id, principal_id, lawful_ref, gpu_index=1, host=None):
    entry = _entry(model_id)
    if entry.get("status") != "admitted":
        raise ValueError(f"MODEL_NOT_ADMITTED_FOR_SERVING:{model_id}:status={entry.get('status')}")
    current = _serving_job(entry)
    if current and current["status"] == "running":
        return current
    n, _ = current_registry_version()
    port = _port_for(model_id)
    params = {"run_dir": entry["run_dir"], "variant": entry.get("variant", "full"), "artefact_sha256": entry["artefact_sha256"], "labels": list(entry["labels"]), "port": port,
              "gpu_index": gpu_index, "max_batch": 64, "max_chars": MAX_CHARS,
              "authority": {"model_id": model_id, "registry_version": n, "artefact_sha256": entry["artefact_sha256"], "admitted_at": entry.get("connected_at"), "granted_by": principal_id, "granted_at": m9.now(),
                            "owner_ruling_ref": entry.get("owner_ruling_ref")}}
    job = m9.submit("serve", params, host or entry["host"], principal_id, lawful_ref, timeout=90)
    annotate_model(model_id, {"serving": {"job_id": job["job_id"], "host": job["host"], "port": port, "gpu_index": gpu_index, "started_at": m9.now(), "status": job["status"], "started_by": principal_id}},
                   authority_source=f"M9.4 governed serving start by {principal_id} · registry v{n} admission · {entry.get('owner_ruling_ref')}")
    return job


def health(model_id):
    entry = _entry(model_id)
    job = _serving_job(entry)
    if not job:
        return {"model_id": model_id, "status": "not_serving", "registry_status": entry.get("status")}
    if job["status"] != "running":
        return {"model_id": model_id, "status": "not_serving", "job": {k: job.get(k) for k in ("job_id", "status", "reason", "finished_at")}, "registry_status": entry.get("status"), "summary": job.get("serving_summary")}
    port = int(entry["serving"]["port"])
    result = _remote(job["host"], f"curl -s -m 60 http://127.0.0.1:{port}/health", purpose=f"m9_serving_health:{model_id}", timeout=75)
    try:
        body = json.loads(result.stdout_redacted.strip())
    except ValueError:
        body = {"error": "no response from the loopback server", "stderr": result.stderr_redacted[:200]}
    return {"model_id": model_id, "status": body.get("status", "unreachable"), "job_id": job["job_id"], "host": job["host"], "port": port, "health": body, "registry_status": entry.get("status")}


def classify(model_id, texts):
    entry = _entry(model_id)
    job = _serving_job(entry)
    if not job or job["status"] != "running":
        raise ValueError("MODEL_NOT_SERVING:" + model_id)
    clean = [str(t)[:MAX_CHARS] for t in texts if str(t).strip()][:MAX_TEXTS]
    if not clean:
        raise ValueError("TEXTS_REQUIRED")
    payload = base64.b64encode(json.dumps({"texts": clean}).encode()).decode()
    port = int(entry["serving"]["port"])
    command = f"echo {payload} | base64 -d | curl -s -m 120 -o /tmp/.akki_cls_$$ -w '%{{http_code}}' -X POST -H 'Content-Type: application/json' --data-binary @- http://127.0.0.1:{port}/classify; echo; cat /tmp/.akki_cls_$$; rm -f /tmp/.akki_cls_$$"
    result = _remote(job["host"], command, purpose=f"m9_serving_classify:{model_id}", timeout=150)
    code, _, body_text = result.stdout_redacted.strip().partition("\n")
    try:
        body = json.loads(body_text.strip())
    except ValueError:
        body = {"error": "unreadable response", "raw": body_text[:200]}
    return {"model_id": model_id, "http_status": int(code) if code.strip().isdigit() else None, "response": body, "receipt_id": result.receipt_id}


def _write_marker(job, name, payload):
    raw = base64.b64encode(json.dumps(payload).encode()).decode()
    path = shlex.quote(job["remote"]["job_dir"] + "/" + name)
    result = _remote(job["host"], f"echo {raw} | base64 -d > {path}.tmp && mv {path}.tmp {path} && cat {path}", purpose=f"m9_serving_marker:{name}:{job['job_id']}", timeout=45)
    if result.rc != 0:
        raise OSError("MARKER_WRITE_FAILED:" + result.stderr_redacted[:200])
    return result.receipt_id


def withdraw(model_id, reason, principal_id, new_status="withdrawn"):
    """Scope withdrawal (M9-T3/T5): revoke the serving authority on the host, prove the very next request is refused, then record the
    registry status by new entry. Nothing is deleted; the artefact stays on the host under custody."""
    entry = _entry(model_id)
    job = _serving_job(entry)
    record = {"model_id": model_id, "reason": reason, "by": principal_id, "at": m9.now(), "previous_status": entry.get("status")}
    if job and job["status"] == "running":
        record["revocation_receipt_id"] = _write_marker(job, "revoked.json", {"reason": reason, "by": principal_id, "at": record["at"], "model_id": model_id})
        probe = classify_raw(job, int(entry["serving"]["port"]), ["kuna habari gani leo"])
        record["post_revocation_probe"] = probe
        record["refused_after_revocation"] = probe.get("http_status") == 403 and (probe.get("response") or {}).get("refused") == "SERVING_AUTHORITY_REVOKED"
        health_now = health(model_id)
        record["health_after_revocation"] = health_now.get("health")
    else:
        record["post_revocation_probe"] = None
        record["refused_after_revocation"] = None
        record["note"] = "no live serving job; registry status withdrawn only"
    n = annotate_model(model_id, {"status": new_status, "serving": {**(entry.get("serving") or {}), "status": "revoked", "revoked_at": record["at"], "revoked_reason": reason},
                                  "withdrawal": {k: record[k] for k in ("reason", "by", "at", "refused_after_revocation")}},
                       authority_source=f"M9 scope withdrawal by {principal_id}: {reason}")
    record["registry_version_after"] = n
    (_dir() / f"withdraw_{model_id}_{record['at'].replace(':', '')}.json").write_text(json.dumps(record, indent=1, default=str))
    return record


def classify_raw(job, port, texts):
    payload = base64.b64encode(json.dumps({"texts": texts}).encode()).decode()
    command = f"echo {payload} | base64 -d | curl -s -m 120 -o /tmp/.akki_cls_$$ -w '%{{http_code}}' -X POST -H 'Content-Type: application/json' --data-binary @- http://127.0.0.1:{port}/classify; echo; cat /tmp/.akki_cls_$$; rm -f /tmp/.akki_cls_$$"
    result = _remote(job["host"], command, purpose=f"m9_serving_probe:{job['job_id']}", timeout=150)
    code, _, body_text = result.stdout_redacted.strip().partition("\n")
    try:
        body = json.loads(body_text.strip())
    except ValueError:
        body = {"error": "unreadable response", "raw": body_text[:200]}
    return {"http_status": int(code) if code.strip().isdigit() else None, "response": body, "receipt_id": result.receipt_id}


def stop(model_id, reason, principal_id):
    entry = _entry(model_id)
    job = _serving_job(entry)
    if not job or job["status"] != "running":
        return {"model_id": model_id, "status": "not_serving"}
    receipt = _write_marker(job, "stop.json", {"reason": reason, "by": principal_id, "at": m9.now()})
    import time
    for _ in range(20):
        time.sleep(3)
        job = m9.refresh(job["job_id"])
        if job["status"] != "running":
            break
    annotate_model(model_id, {"serving": {**entry["serving"], "status": job["status"], "stopped_at": m9.now(), "stop_reason": reason}}, authority_source=f"M9.4 serving stop by {principal_id}: {reason}")
    return {"model_id": model_id, "job": {k: job.get(k) for k in ("job_id", "status", "finished_at")}, "summary": job.get("serving_summary"), "stop_receipt_id": receipt}


def load_test(model_id, principal_id, lawful_ref, concurrency=8, requests_per_thread=20, batch=8, per_stratum=30):
    entry = _entry(model_id)
    job = _serving_job(entry)
    if not job or job["status"] != "running":
        raise ValueError("MODEL_NOT_SERVING:" + model_id)
    params = {"port": int(entry["serving"]["port"]), "corpus_id": entry["corpus_id"], "concurrency": int(concurrency), "requests_per_thread": int(requests_per_thread), "batch": int(batch),
              "per_stratum": int(per_stratum), "model_id": model_id, "serving_job_id": job["job_id"]}
    return m9.submit("load_test", params, job["host"], principal_id, lawful_ref, timeout=90)


def models_view():
    adapters = _all_adapters()
    n, _ = current_registry_version()
    rows = []
    for model_id, e in adapters.items():
        rows.append({"model_id": model_id, "status": e.get("status"), "variant": e.get("variant"), "base": e.get("base"), "artefact_sha256": e.get("artefact_sha256"), "host": e.get("host"),
                     "training_job_id": e.get("training_job_id"), "recipe_version": e.get("recipe_version"), "cited_units": e.get("cited_units"), "excluded_unit_ids": e.get("excluded_unit_ids"),
                     "rederived_from": e.get("rederived_from"), "connected_at": e.get("connected_at"), "re_check_due_at": e.get("re_check_due_at"), "serving": e.get("serving"), "recall": e.get("recall"),
                     "withdrawal": e.get("withdrawal"), "owner_ruling_ref": e.get("owner_ruling_ref")})
    return {"registry_version": f"v{n}", "trained_adapters": sorted(rows, key=lambda r: r.get("connected_at") or "", reverse=True)}
