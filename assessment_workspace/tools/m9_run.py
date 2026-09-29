"""Operator tool: commission / read M9 governed-training jobs through the authenticated Akki API (never a bypass).

usage: m9_run.py submit <phase> <host> <params.json>   ·   m9_run.py status <job_id>   ·   m9_run.py list   ·   m9_run.py cancel <job_id> <reason>
Credentials come from AKKI_M9_EMAIL / AKKI_M9_PASSWORD (RMS operator seat), never from this file.
"""
import json
import os
import sys

import requests

BASE = next(l.split("=", 1)[1].strip() for l in open("/app/frontend/.env") if l.startswith("REACT_APP_BACKEND_URL="))
EMAIL, PASSWORD = os.environ["AKKI_M9_EMAIL"], os.environ["AKKI_M9_PASSWORD"]


def headers():
    r = requests.post(f"{BASE}/api/auth/login", json={"email": EMAIL, "password": PASSWORD}, timeout=30)
    r.raise_for_status()
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def main():
    cmd = sys.argv[1]
    h = headers()
    if cmd == "submit":
        phase, host, params = sys.argv[2], sys.argv[3], json.load(open(sys.argv[4]))
        r = requests.post(f"{BASE}/api/training/m9/jobs", json={"phase": phase, "host": host, **params}, headers=h, timeout=120)
        print(r.status_code); print(json.dumps(r.json(), indent=1, default=str)[:3000])
    elif cmd == "status":
        r = requests.get(f"{BASE}/api/training/m9/jobs/{sys.argv[2]}", headers=h, timeout=180)
        job = r.json().get("job", r.json())
        brief = {k: job.get(k) for k in ("job_id", "phase", "host", "status", "reason", "started_at", "finished_at", "process_alive")}
        brief["progress"] = (job.get("remote_state") or {}).get("progress")
        brief["stages"] = list(((job.get("remote_state") or {}).get("stages") or {}).keys())
        if job.get("receipt") and job["receipt"].get("error"):
            brief["error"] = job["receipt"]["error"]
        print(r.status_code); print(json.dumps(brief, indent=1, default=str))
        if len(sys.argv) > 3 and sys.argv[3] == "full":
            print(json.dumps(job, indent=1, default=str)[:int(os.environ.get("M9_PRINT", "12000"))])
    elif cmd == "list":
        r = requests.get(f"{BASE}/api/training/m9/jobs", headers=h, timeout=60)
        for j in r.json()["jobs"]:
            print(j["job_id"], j["phase"], j["host"], j["status"], j.get("submitted_at", "")[:19], (j.get("reason") or "")[:80])
    elif cmd == "cancel":
        r = requests.post(f"{BASE}/api/training/m9/jobs/{sys.argv[2]}/cancel", json={"reason": sys.argv[3]}, headers=h, timeout=90)
        print(r.status_code, json.dumps(r.json(), default=str)[:600])


if __name__ == "__main__":
    main()
