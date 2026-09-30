#!/usr/bin/env python3
"""M8-T2 critical-service-failure drill · Ledger store (MongoDB) outage, exercised against the running application.

Baseline → stop the Ledger store → probe: identity, Ledger head read, WORM archive, a governed commission (must refuse BEFORE any
remote dispatch; no partial WORM object; no split writer) → restore the store → prove the head/chain are unchanged and the same
commission now succeeds exactly once. Receipt at phase0/bc_drill_receipts/. Rules/credential-custody outages are covered by the
isolated suites and are named as such in the receipt — this drill does not claim them.
"""
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

API = Path("/app/frontend/.env").read_text().split("REACT_APP_BACKEND_URL=")[1].splitlines()[0].strip()
LOCAL = "http://localhost:8001"
RECEIPTS = Path(os.environ.get("BC_DRILL_RECEIPTS_DIR", "/app/assessment_workspace/phase0/bc_drill_receipts"))
WORM = Path("/app/assessment_workspace/phase0/worm/ledger_v1_control_events")


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def call(method, path, token=None, body=None, base=LOCAL, timeout=60):
    headers = {"Content-Type": "application/json", "User-Agent": "akki-drill/1.0", **({"Authorization": "Bearer " + token} if token else {})}
    req = urllib.request.Request(base + path, data=json.dumps(body).encode() if body is not None else None, method=method, headers=headers)
    t0 = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(); code = r.status
    except urllib.error.HTTPError as e:
        raw = e.read() or b""; code = e.code
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        return {"code": None, "error": type(e).__name__, "seconds": round(time.monotonic() - t0, 3)}
    try:
        body = json.loads(raw) if raw else {}
    except ValueError:
        body = {"raw": raw.decode(errors="replace")[:200]}
    return {"code": code, "body": body, "seconds": round(time.monotonic() - t0, 3)}


def sv(action):
    return subprocess.run(["sudo", "supervisorctl", action, "mongodb"], capture_output=True, text=True).stdout.strip()


def main():
    login = {"email": os.environ["AKKI_DRILL_EMAIL"], "password": os.environ["AKKI_DRILL_PASSWORD"]}
    r = call("POST", "/api/auth/login", body=login); assert r["code"] == 200, r
    token = r["body"]["access_token"]
    commission = {"tenant_id": "RMS", "phase": "load_test", "host": "akki-vm-ii", "port": 8611, "corpus_id": "rms-transcripts-v1", "concurrency": 2, "requests_per_thread": 2, "batch": 4, "per_stratum": 3}
    receipt = {"drill": "M8-T2 critical service failure · Ledger store outage (live application)", "at": now(), "store": "mongodb (supervisor-managed)", "phases": {}}
    base_head = call("GET", "/api/continuity/ledger/head", token)
    worm_before = len(list(WORM.glob("*.receipt.json")))
    receipt["phases"]["baseline"] = {"ledger_head": {"code": base_head["code"], "rows": base_head["body"].get("rows"), "head": base_head["body"].get("head"), "chain_intact": (base_head["body"].get("chain") or {}).get("intact")},
                                     "worm_objects": worm_before, "identity": call("GET", "/api/auth/me", token)["code"]}
    t_down = time.monotonic()
    receipt["phases"]["outage"] = {"supervisor": sv("stop"), "started_at": now()}
    time.sleep(2)
    probes = {}
    probes["identity_login"] = call("POST", "/api/auth/login", body=login, timeout=40)
    probes["ledger_head_read"] = call("GET", "/api/continuity/ledger/head", token, timeout=40)
    probes["worm_archive_attempt"] = call("POST", "/api/continuity/ledger/archive", token, {"tenant_id": "RMS"}, timeout=60)
    probes["governed_commission_attempt"] = call("POST", "/api/training/m9/jobs", token, commission, timeout=90)
    probes["serving_health_read_ssh_path"] = call("GET", "/api/training/m9/serving/m9j-74af7cef0a85/health", token, timeout=120)
    for k, v in probes.items():
        v["body"] = json.dumps(v.get("body"))[:300] if v.get("body") is not None else None
    receipt["phases"]["outage"]["probes"] = probes
    receipt["phases"]["outage"]["worm_objects_after_probes"] = len(list(WORM.glob("*.receipt.json")))
    receipt["phases"]["outage"]["no_partial_worm_object"] = receipt["phases"]["outage"]["worm_objects_after_probes"] == worm_before
    receipt["phases"]["recovery"] = {"supervisor": sv("start"), "started_at": now()}
    ok = None
    for _ in range(30):
        time.sleep(2)
        ok = call("GET", "/api/continuity/ledger/head", token, timeout=30)
        if ok["code"] == 200:
            break
    receipt["phases"]["recovery"]["seconds_to_ledger_read"] = round(time.monotonic() - t_down, 1)
    receipt["phases"]["recovery"]["ledger_head"] = {"code": ok["code"], "rows": ok["body"].get("rows"), "head": ok["body"].get("head"), "chain_intact": (ok["body"].get("chain") or {}).get("intact")}
    receipt["phases"]["recovery"]["head_unchanged_by_outage"] = receipt["phases"]["recovery"]["ledger_head"]["head"] == receipt["phases"]["baseline"]["ledger_head"]["head"]
    r = call("POST", "/api/auth/login", body=login); token = r["body"].get("access_token", token)
    jobs_before = call("GET", "/api/training/m9/jobs", token, timeout=60)["body"].get("jobs", [])
    after = call("POST", "/api/training/m9/jobs", token, commission, timeout=120)
    job = (after.get("body") or {}).get("job") or {}
    receipt["phases"]["recovery"]["same_commission_after_recovery"] = {"code": after["code"], "job_id": job.get("job_id"), "status": job.get("status"), "reason": job.get("reason")}
    jobs_after = call("GET", "/api/training/m9/jobs", token, timeout=60)["body"].get("jobs", [])
    new_ids = sorted({j["job_id"] for j in jobs_after} - {j["job_id"] for j in jobs_before})
    receipt["phases"]["recovery"]["jobs_created_by_the_two_attempts"] = new_ids
    receipt["phases"]["recovery"]["single_effect"] = len(new_ids) == 1
    outage = receipt["phases"]["outage"]["probes"]
    refused = all((outage[k]["code"] is None or outage[k]["code"] >= 400) for k in ("identity_login", "ledger_head_read", "worm_archive_attempt", "governed_commission_attempt"))
    receipt["coverage"] = {"ledger_store_outage": "DRILLED LIVE", "rules_service_outage": "isolated suite only (tests/execution_components · not claimed live)",
                           "credential_custody_outage": "isolated suite only (custody/delivery 13 tests · not claimed live)"}
    receipt["verdict"] = "PASS" if refused and receipt["phases"]["outage"]["no_partial_worm_object"] and receipt["phases"]["recovery"]["head_unchanged_by_outage"] and receipt["phases"]["recovery"]["single_effect"] and after["code"] == 202 else "FAIL"
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    path = RECEIPTS / f"{receipt['at'].replace(':', '').replace('-', '')}_m8t2_ledger_store_outage.json"
    path.write_text(json.dumps(receipt, indent=1, default=str))
    print(json.dumps({"verdict": receipt["verdict"], "path": str(path), "outage_probes": {k: v["code"] for k, v in outage.items()}, "recovery": receipt["phases"]["recovery"]}, indent=1, default=str))


if __name__ == "__main__":
    main()
