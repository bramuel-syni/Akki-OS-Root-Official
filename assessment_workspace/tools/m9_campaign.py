"""M9 governed campaign orchestrator (control plane only): calibrate ∥ compare → full governed run(s), all through the authenticated Akki API.

usage: m9_campaign.py <campaign.json>      (runs until every stage is terminal; safe to re-run — resumes from the campaign file)
Credentials from AKKI_M9_EMAIL / AKKI_M9_PASSWORD. Stage results are read from the banked job records; nothing is dispatched twice.
"""
import json
import os
import sys
import time

import requests

BASE = next(l.split("=", 1)[1].strip() for l in open("/app/frontend/.env") if l.startswith("REACT_APP_BACKEND_URL="))
EMAIL, PASSWORD = os.environ["AKKI_M9_EMAIL"], os.environ["AKKI_M9_PASSWORD"]
POLL = int(os.environ.get("M9_POLL_SECONDS", "120"))
TERMINAL = ("completed", "failed", "refused", "cancelled")


def headers():
    r = requests.post(f"{BASE}/api/auth/login", json={"email": EMAIL, "password": PASSWORD}, timeout=30)
    r.raise_for_status()
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def log(msg):
    print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), msg, flush=True)


def save(path, doc):
    tmp = path + ".tmp"
    open(tmp, "w").write(json.dumps(doc, indent=1, default=str)); os.replace(tmp, path)


def submit(phase, host, params):
    r = requests.post(f"{BASE}/api/training/m9/jobs", json={"phase": phase, "host": host, **params}, headers=headers(), timeout=180)
    if r.status_code != 202:
        raise RuntimeError(f"submit {phase} → {r.status_code}: {r.text[:400]}")
    job = r.json()["job"]
    log(f"submitted {phase} on {host} gpu{params.get('gpu_index')} → {job['job_id']} ({job['status']})")
    return job


def status(job_id):
    r = requests.get(f"{BASE}/api/training/m9/jobs/{job_id}", headers=headers(), timeout=240)
    r.raise_for_status()
    return r.json()["job"]


def wait(doc, path, keys):
    """Poll the named stages until terminal; progress lines are the worker's own state."""
    while True:
        pending = [k for k in keys if doc["stages"][k].get("status") not in TERMINAL]
        if not pending:
            return
        for k in pending:
            job = status(doc["stages"][k]["job_id"])
            doc["stages"][k].update(status=job["status"], reason=job.get("reason"), finished_at=job.get("finished_at"))
            progress = (job.get("remote_state") or {}).get("progress") or {}
            log(f"{k} {job['job_id']} {job['status']} · {progress.get('stage', '')} step {progress.get('step', '')}/{progress.get('total_steps', '')} "
                f"loss {progress.get('loss', '')} tok/s {progress.get('tokens_per_second', '')} padded/step {progress.get('padded_tokens_per_step', '')} gpu {progress.get('gpu_memory_gb', '')} GB")
            if job["status"] in TERMINAL:
                doc["stages"][k]["result_keys"] = sorted(((job.get("receipt") or {}).get("result") or {}).keys())
                if k == "calibrate" and job["status"] == "completed":
                    res = job["receipt"]["result"]
                    doc["stages"][k]["base_selected"] = res["base_selected_by_calibration"]
                    doc["stages"][k]["quotes"] = {b: {"predicted_min_stratum_full": q["predicted_min_stratum_full"], "gpu_hours": q["full_run_gpu_hours_quote"]} for b, q in res["quotes"].items()}
                if k == "compare" and job["status"] == "completed":
                    res = job["receipt"]["result"]
                    doc["stages"][k]["recommended_verdict"] = res["recommended_verdict"]
                    doc["stages"][k]["harness"] = job.get("optimizer_comparison")
                if k.startswith("train") and job.get("run_certificate"):
                    cert = job["run_certificate"]
                    doc["stages"][k]["certificate"] = {"moac": {kk: cert["moac"][kk] for kk in ("m_a_improvement", "m_b_non_target_regression", "m_e_calibration_ece")},
                                                       "per_stratum": {s: (r["accuracy"], r["base_accuracy"], r["meets_m_a"]) for s, r in cert["per_stratum"].items()},
                                                       "egress_permitted": cert["distance_probe"]["egress_permitted"], "refusals": cert["distance_probe"]["refusals"],
                                                       "admission": cert["admission"], "pruned": cert["pruned_artefact"].get("admission"),
                                                       "compute": {kk: cert["compute"][kk] for kk in ("steps", "epochs_completed", "wallclock_seconds", "gpu_hours", "tokens_per_second", "padded_tokens_per_step", "gpu_max_memory_gb", "final_loss")}}
                log(f"{k} terminal: {json.dumps(doc['stages'][k], default=str)[:1500]}")
            save(path, doc)
        time.sleep(POLL)


def main():
    path = sys.argv[1]
    doc = json.load(open(path))
    doc.setdefault("stages", {})
    plan = doc["plan"]
    host = plan["host"]
    # Stage 1 — mandatory calibration (§17.3) on one GPU, A17.5 optimizer comparison on the other: independent, parallel.
    if "calibrate" not in doc["stages"]:
        doc["stages"]["calibrate"] = {"job_id": submit("calibrate", host, plan["calibrate"])["job_id"], "status": "running"}; save(path, doc)
    if "compare" not in doc["stages"]:
        doc["stages"]["compare"] = {"job_id": submit("compare_optimizers", host, plan["compare"])["job_id"], "status": "running"}; save(path, doc)
    wait(doc, path, ["calibrate", "compare"])
    cal, cmp_ = doc["stages"]["calibrate"], doc["stages"]["compare"]
    if cal["status"] != "completed":
        log("calibration did not complete; the full run is NOT commissioned without its quote (§17.3)"); return
    base = cal["base_selected"]
    optimizer = "muon" if cmp_.get("recommended_verdict") == "adopted" else "adamw"
    log(f"base selected by calibration: {base}; optimizer by A17.5 harness: {optimizer} (comparison {cmp_.get('status')}, verdict {cmp_.get('recommended_verdict')})")
    # Stage 2 — the governed full run on the selected base; the runner-up base trains on the other GPU as a measured alternative
    # (max utilisation per owner order; each artefact must pass MOAC/DAP-31 on its own numbers, nothing is served).
    if "train_selected" not in doc["stages"]:
        params = json.loads(json.dumps(plan["train"][base])); params["recipe"]["optimizer"] = optimizer; params["base"] = base; params["gpu_index"] = 0
        doc["stages"]["train_selected"] = {"job_id": submit("train", host, params)["job_id"], "status": "running", "base": base, "optimizer": optimizer}; save(path, doc)
    others = [b for b in plan["calibrate"]["bases"] if b != base and b in plan["train"]]
    if plan.get("train_runner_up", True) and others and "train_runner_up" not in doc["stages"]:
        params = json.loads(json.dumps(plan["train"][others[0]])); params["recipe"]["optimizer"] = optimizer; params["base"] = others[0]; params["gpu_index"] = 1
        doc["stages"]["train_runner_up"] = {"job_id": submit("train", host, params)["job_id"], "status": "running", "base": others[0], "optimizer": optimizer}; save(path, doc)
    wait(doc, path, [k for k in doc["stages"] if k.startswith("train")])
    doc["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()); save(path, doc)
    log("campaign terminal")


if __name__ == "__main__":
    main()
