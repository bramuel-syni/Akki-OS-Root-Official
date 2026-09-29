"""Background poller: one bounded status RPC every N seconds until the job closes; appends to a log."""
import json
import subprocess
import sys
import time

job_id, interval, log = sys.argv[1], int(sys.argv[2]), sys.argv[3]
while True:
    out = subprocess.run([sys.executable, "/app/assessment_workspace/tools/m2_language_cognition_run.py", "refresh", job_id],
                         capture_output=True, text=True, timeout=110, check=False).stdout
    try:
        doc = json.loads(out)
    except ValueError:
        doc = {"raw": out[-300:]}
    with open(log, "a") as f:
        f.write(json.dumps({"at": time.strftime("%H:%M:%S"), "status": doc.get("status"), "progress": doc.get("progress"), "error": doc.get("error")}) + "\n")
    if doc.get("status") in ("completed", "failed", "refused"):
        break
    time.sleep(interval)
