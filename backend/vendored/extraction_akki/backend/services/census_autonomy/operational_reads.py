"""One read model for native OS, DAP, and legacy census aliases."""
import hashlib
import json
import os
from pathlib import Path

from services.census_autonomy import engine, operational_store as store
from services.census_autonomy.operational_validation import classify_payload, validate_output
from services.mtafiti.census_projection import list_records
from services.mtafiti.census_result_adapter import restore_registered


def records(tenant):
    from services.census_autonomy.registry_durability import restore_results
    restore_results(tenant)
    values = list_records(Path(os.environ["CENSUS_RECORDS_DIR"]), tenant)
    for path in (engine.CENSUS_STATE_DIR / engine.RESULTS_SUBDIR).glob("*.json"):
        try:
            raw = path.read_bytes()
            doc = json.loads(raw)
            if doc.get("tenant_id") != tenant:
                continue
            payload = doc.get("payload", {})
            state = classify_payload(payload)
            if state not in {"COMPLETE", "PARTIAL"}:
                continue
            good = [validate_output(o, doc["census_run_id"], tenant, o["source_id"])
                    for o in payload["outcomes"] if o.get("status") in {"complete", "partial"}]
            restore_registered(payload)
            record={"record_id": doc["census_run_id"], "census_number": None, "tenant_id": tenant,
                           "status": state, "scope": "Bounded metadata inventory", "execution_verified": True,
                           "finished_at": doc["completed_at_utc"], "database_count": sum(o["database_count"] for o in good),
                           "table_count": sum(o["table_count"] for o in good),
                           "row_count_estimate": sum(o["row_count_estimate"] for o in good),
                           "row_count_measured": None, "volume_bytes": None, "quality_percent": None,
                           "licensed_percent": None, "outcomes": payload["outcomes"],
                           "proof_ref": f"census_autonomy_state/results/{path.name}",
                           "proof_sha256": hashlib.sha256(raw).hexdigest(),
                           "limitations": ["Metadata only; source content, quality and external rights were not assessed."]}
            from services.census_autonomy.registry_report import enrich_record
            values.append(enrich_record(record,doc,payload))
        except (OSError, ValueError, KeyError, TypeError):
            continue
    from services.census_autonomy.registry_report import attach_reports
    return attach_reports(sorted(values, key=lambda v: v.get("finished_at") or "", reverse=True))


def run_view(row):
    if not row:
        return None
    public = {k: v for k, v in row.items() if k not in {"idempotency_key", "fingerprint", "lawful_basis_admit_ref", "source_hosts"}}
    if row.get("status") == "COMPLETE":
        try:
            name = row["proof_ref"].rsplit("/", 1)[-1]
            evidence = engine.CENSUS_STATE_DIR / engine.RESULTS_SUBDIR / name
            raw = evidence.read_bytes()
            payload = json.loads(raw)["payload"]
            if hashlib.sha256(raw).hexdigest() != row["proof_sha256"] or classify_payload(payload) != "COMPLETE":
                raise ValueError("Completion evidence mismatch")
        except (KeyError, OSError, ValueError):
            public.update(status="REFUSED", stage="unverified", reason_code="COMPLETION_EVIDENCE_UNAVAILABLE")
    import time
    if row.get("stage") == "executing" and time.time() > row.get("deadline", 0):
        public.update(stage="interrupted", status="REFUSED", reason_code="EXECUTION_DEADLINE_PASSED")
    return public


def run_state(run_id, tenant):
    row = store.get(run_id, tenant)
    if row:
        return run_view(row)
    # Older COMPLETE receipts are preserved, but no longer represented as executed work.
    for path in (engine.CENSUS_STATE_DIR / engine.RESULTS_SUBDIR).glob("*.json"):
        try:
            doc = json.loads(path.read_text())
            if doc.get("census_run_id") == run_id and doc.get("tenant_id") == tenant:
                return {"census_run_id": run_id, "tenant_id": tenant, "status": "REFUSED", "stage": "unverified",
                        "reason_code": "LEGACY_COMPLETION_HAS_NO_VERIFIED_EXECUTION", "outcomes": []}
        except (OSError, ValueError):
            continue
    return None