"""Language-cognition corrective recipe sweep (control plane only): queued arms over the two akki-vm H200s, every
submission through the authenticated `/api/portal/census/language-cognition/jobs` route (commission gate + Watch).

usage: lc_sweep.py <sweep.json>      (runs until every arm is terminal; safe to re-run — resumes from the sweep file)
Credentials from AKKI_M9_EMAIL / AKKI_M9_PASSWORD. Arm results are the banked run certificates; nothing is dispatched twice.
"""
import json
import os
import sys
import time

import requests

BASE = next(l.split("=", 1)[1].strip() for l in open("/app/frontend/.env") if l.startswith("REACT_APP_BACKEND_URL="))
EMAIL, PASSWORD = os.environ["AKKI_M9_EMAIL"], os.environ["AKKI_M9_PASSWORD"]
POLL = int(os.environ.get("LC_POLL_SECONDS", "180"))
TERMINAL = ("completed", "failed", "refused", "cancelled")
ROUTE = "/api/portal/census/language-cognition/jobs"


def headers():
    r = requests.post(f"{BASE}/api/auth/login", json={"email": EMAIL, "password": PASSWORD}, timeout=30)
    r.raise_for_status()
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def log(msg):
    print(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), msg, flush=True)


def save(path, doc):
    tmp = path + ".tmp"
    open(tmp, "w").write(json.dumps(doc, indent=1, default=str)); os.replace(tmp, path)


def submit(host, params):
    r = requests.post(f"{BASE}{ROUTE}", json={"phase": "train_corrective", "host": host, **params}, headers=headers(), timeout=180)
    if r.status_code != 202:
        raise RuntimeError(f"submit → {r.status_code}: {r.text[:400]}")
    return r.json()["job"]


def status(job_id):
    r = requests.get(f"{BASE}{ROUTE}/{job_id}", headers=headers(), timeout=240)
    r.raise_for_status()
    return r.json()["job"]


def summary(job):
    cert = job.get("run_certificate") or {}
    result = (job.get("receipt") or {}).get("result") or {}
    held = result.get("held_out") or {}
    probe = result.get("no_speaker_id_probe") or {}
    egress = probe.get("egress_surface") or {}
    guz = (probe.get("per_language") or {}).get("guz") or {}
    return {"verdict": cert.get("verdict"), "epsilon": (result.get("dp_sgd") or {}).get("epsilon"),
            "held_out": {c: (r.get("accuracy"), r.get("abstention_rate")) for c, r in held.get("per_language", {}).items() if r.get("windows")},
            "overall_accuracy_on_judged": held.get("overall_accuracy_on_judged"), "overall_abstention": held.get("overall_abstention_rate"),
            "archive_test_accuracy": (result.get("archive_test") or {}).get("overall_accuracy_on_judged"),
            "best_dev_epoch": (result.get("training") or {}).get("best_dev_epoch"), "steps": (result.get("training") or {}).get("steps"),
            "windows_per_second": (result.get("training") or {}).get("windows_per_second"), "elapsed_seconds": (result.get("training") or {}).get("elapsed_seconds"),
            "probe_guz": {name: (v.get("accuracy"), v.get("chance"), v.get("majority_baseline")) for name, v in guz.items()},
            "egress_at_chance_all_languages": egress.get("at_chance_all_languages"), "internal_at_chance": egress.get("internal_representations_at_chance"),
            "meets_default": (cert.get("sealed_contract_check") or {}).get("per_language_accuracy_default"),
            "artefact_sha256": cert.get("artefact_sha256")}


def main():
    path = sys.argv[1]
    doc = json.load(open(path))
    plan, arms = doc["plan"], doc["arms"]
    host, slots = plan["host"], list(plan["gpu_slots"])
    while True:
        busy = {a.get("gpu_index") for a in arms if a.get("job_id") and a.get("status") not in TERMINAL}
        for gpu in slots:
            if gpu in busy:
                continue
            queued = next((a for a in arms if not a.get("job_id")), None)
            if not queued:
                break
            params = {**plan["common"], **queued["params"], "gpu_index": gpu, "owner_order_ref": plan["owner_order_ref"]}
            job = submit(host, params)
            queued.update(job_id=job["job_id"], gpu_index=gpu, status=job["status"], submitted_at=job.get("submitted_at"), params_submitted=params)
            log(f"submitted arm {queued['name']} on {host} gpu{gpu} → {job['job_id']} ({job['status']})")
            busy.add(gpu); save(path, doc)
        live = [a for a in arms if a.get("job_id") and a.get("status") not in TERMINAL]
        if not live:
            log("all arms terminal"); save(path, doc); return
        for arm in live:
            job = status(arm["job_id"])
            arm.update(status=job["status"], reason=job.get("reason"), finished_at=job.get("finished_at"), process_alive=job.get("process_alive"))
            p = (job.get("remote_state") or {}).get("progress") or {}
            dev = p.get("latest_dev") or {}
            log(f"{arm['name']} {arm['job_id']} {job['status']} · {p.get('stage', '')} epoch {p.get('epoch', '')}/{p.get('epochs', '')} step {p.get('step', '')} "
                f"loss {p.get('loss', '')} w/s {p.get('windows_per_second', '')} gpu {p.get('gpu_memory_gb', '')} GB · dev ε {round(dev['epsilon'], 2) if dev.get('epsilon') else ''} "
                f"macro {round(dev['selection_score'][1], 3) if dev.get('selection_score') else ''}")
            if job["status"] in TERMINAL:
                arm["summary"] = summary(job)
                if job["status"] != "completed":
                    arm["error"] = ((job.get("receipt") or {}).get("error") or {}).get("message")
                log(f"{arm['name']} terminal: {json.dumps(arm['summary'], default=str)[:1500]}")
            save(path, doc)
        time.sleep(POLL)


if __name__ == "__main__":
    main()
