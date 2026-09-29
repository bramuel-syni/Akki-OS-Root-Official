"""M2 operator tool — commission / refresh language-cognition phases through the control plane (same path
as `POST /api/portal/census/language-cognition/jobs`). Usage:
    python m2_language_cognition_run.py submit <phase> '<json params>'
    python m2_language_cognition_run.py refresh <job_id>
    python m2_language_cognition_run.py list
"""
import json
import os
import sys

sys.path.insert(0, "/app/backend/vendored/extraction_akki/backend")
from dotenv import load_dotenv  # noqa: E402

load_dotenv("/app/backend/.env")
from services.audio_plane_v1 import language_cognition_dispatch as lc  # noqa: E402
from services.census_autonomy.operational_runner import admission_path  # noqa: E402

PRINCIPAL = os.environ.get("M2_OPERATOR_PRINCIPAL", "demo.operator@demo.rms.example.com")


def _brief(job):
    keep = {k: job.get(k) for k in ("job_id", "phase", "status", "reason", "submitted_at", "finished_at", "process_alive")}
    keep["progress"] = (job.get("remote_state") or {}).get("progress")
    if job.get("receipt") and job["receipt"].get("error"):
        keep["error"] = {k: job["receipt"]["error"][k] for k in ("type", "message")}
        keep["trace_tail"] = job["receipt"]["error"]["trace"][-1200:]
    keep["log_tail"] = (job.get("worker_log_tail") or "")[-600:]
    return keep


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "submit":
        params = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        path, _ = admission_path()
        job = lc.submit(sys.argv[2], params, PRINCIPAL, str(path), timeout=int(os.environ.get("M2_SUBMIT_TIMEOUT", "90")))
        print(json.dumps(_brief(job), indent=1, default=str))
    elif command == "refresh":
        print(json.dumps(_brief(lc.refresh(sys.argv[2])), indent=1, default=str))
    elif command == "list":
        for job in lc.list_jobs():
            print(job["job_id"], job["phase"], job["status"], job.get("submitted_at"))
