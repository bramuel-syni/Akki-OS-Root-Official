"""Execution cursor over the EXISTING census queue; results stay with its sealed writer."""
import fcntl
import hashlib
import json
import os
import re
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from services.census_autonomy import engine


def now():
    return datetime.now(timezone.utc).isoformat()


def cursor_dir():
    p = engine.CENSUS_STATE_DIR / "dispatch"
    p.mkdir(parents=True, exist_ok=True)
    return p


@contextmanager
def lock(key, blocking=True):
    name = hashlib.sha256(key.encode()).hexdigest()
    with (cursor_dir() / f"{name}.lock").open("a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
        except BlockingIOError:
            yield False
            return
        try:
            yield True
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def save(doc):
    if not re.fullmatch(r"cr-[a-f0-9]{12}", doc["census_run_id"]):
        raise ValueError("Invalid run identifier")
    doc['updated_at']=now()
    from services.census_autonomy.registry_durability import preserve_cursor
    preserve_cursor(doc)
    path = cursor_dir() / (doc["census_run_id"] + ".json")
    temp = path.with_suffix(f".{os.getpid()}.tmp")
    with temp.open("w") as handle:
        json.dump(doc, handle, sort_keys=True)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def runs(tenant):
    from services.census_autonomy.registry_durability import restore_cursors
    restore_cursors(tenant,cursor_dir())
    values = []
    for path in cursor_dir().glob("cr-*.json"):
        try:
            row = json.loads(path.read_text())
            if row.get("tenant_id") == tenant:
                values.append(row)
        except (OSError, ValueError):
            continue
    return sorted(values, key=lambda r: r.get("created_at", ""), reverse=True)


def get(run_id, tenant):
    if not re.fullmatch(r'cr-[a-f0-9]{12}',run_id): return None
    path=cursor_dir()/(run_id+'.json')
    try: row=json.loads(path.read_text())
    except (OSError,ValueError): return None
    return row if row.get('tenant_id')==tenant else None


def enqueue(tenant, principal, sources, key, lawful_ref, worker_id=None, source_refs=None, measurement=None):
    if not re.fullmatch(r"[a-zA-Z0-9_-]{16,100}", key):
        raise ValueError("A valid idempotency key is required.")
    identity=[tenant, principal, sorted(sources)]
    if worker_id: identity.append(worker_id)
    if source_refs: identity.append(sorted(source_refs))
    if measurement: identity.append('measurement='+measurement)
    fingerprint = hashlib.sha256(json.dumps(identity, separators=(",", ":")).encode()).hexdigest()
    with lock(f"submit:{tenant}:{principal}:{key}"):
        for row in runs(tenant):
            if row.get("principal_id") == principal and row.get("idempotency_key") == key:
                if row["fingerprint"] != fingerprint:
                    raise ValueError("This submission key already belongs to a different source selection.")
                return row, False
        descriptor = {"version": "operational-v1", "source_ids": sources, "principal_id": principal,
                      "idempotency_key": key, "fingerprint": fingerprint,
                      "lawful_basis_sha256": hashlib.sha256(Path(lawful_ref).read_bytes()).hexdigest()}
        if source_refs: descriptor['source_refs']=source_refs
        if measurement: descriptor['measurement']=measurement
        # Recover a crash after the canonical enqueue but before the dispatch cursor write.
        job = next((j for j in engine.get_pending_scheduled_runs()
                    if j.get("tenant_id") == tenant and j.get("connect_source_descriptor") == descriptor), None)
        run_id = job["census_run_id"] if job else engine.enqueue_on_demand_run(tenant, descriptor, lawful_ref)
        doc = {"census_run_id": run_id, "tenant_id": tenant, "principal_id": principal,
               "source_ids": sources, "idempotency_key": key, "fingerprint": fingerprint,
               "status": "PENDING", "stage": "queued", "created_at": now(), "outcomes": [],
               "lawful_basis_admit_ref": lawful_ref, "worker_id": worker_id, "source_refs":source_refs, "measurement": measurement}
        doc['job_descriptor']=next((job for job in engine.get_pending_scheduled_runs() if job['census_run_id']==run_id),None)
        save(doc)
        return doc, True