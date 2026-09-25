"""CP-CENSUS-OPERATIONAL-V1 RED-first tests. Synthetic fixtures, never estate I/O."""
import hashlib
import json
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

from services.census_autonomy.operational_scope import tenant_from_account, validate_submission
from services.mtafiti.census_projection import list_records
from services.census_autonomy.operational_validation import validate_output, classify_payload


def manifest(root, number, **values):
    path = root / f"census_{number:04d}" / "manifest.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"census_id": number, **values}))
    return path


def output(**values):
    base = {"protocol": "akki-census-aggregate-v1", "census_run_id": "cr-test",
            "tenant_id": "RMS", "source_id": "rms_mysql", "execution_location": "akki_host",
            "observed_at": "2026-09-25T12:00:00Z", "status": "complete",
            "database_count": 2, "table_count": 3, "row_count_estimate": 20,
            "worker_receipt_id": "worker-test", "source_rows_returned": 0}
    base.update(values)
    return base


def test_t03_membership_not_inferred_from_email():
    with pytest.raises(ValueError):
        tenant_from_account({"email": "demo.operator@demo.rms.example.com", "roles": ["operator"]})


def test_t03_explicit_rms_membership():
    assert tenant_from_account({"tenant_id": "RMS"}) == "RMS"


def test_t03_unknown_tenant_refused():
    with pytest.raises(ValueError):
        tenant_from_account({"tenant_id": "ANY"})


def test_t04_dynamic_newest_and_tenant_scope(tmp_path):
    manifest(tmp_path, 4, tenant_id="RMS", rollup={"table_count": 7, "total_row_count_est": 19})
    manifest(tmp_path, 8, tenant_id="DIGICOW", rollup={"table_count": 999})
    manifest(tmp_path, 9, tenant_id="RMS", rollup={"table_count": 9})
    rows = list_records(tmp_path, "RMS")
    assert [r["census_number"] for r in rows] == [9, 4]
    assert "999" not in json.dumps(rows)


def test_t04_untagged_unknown_record_is_not_owned(tmp_path):
    manifest(tmp_path, 55, rollup={"table_count": 888})
    assert list_records(tmp_path, "RMS") == []


def test_t05_estimate_does_not_become_count(tmp_path):
    p = manifest(tmp_path, 4, tenant_id="RMS", rollup={"total_row_count_est": 19})
    row = list_records(tmp_path, "RMS")[0]
    assert row["row_count_estimate"] == 19
    assert row["row_count_measured"] is None
    assert row["volume_bytes"] is None
    assert row["proof_sha256"] == hashlib.sha256(p.read_bytes()).hexdigest()


def test_t05_no_raw_audit_or_topology_leak(tmp_path):
    manifest(tmp_path, 4, tenant_id="RMS", audit_trail=[{"sql": "secret-table"}],
             clusters=[{"cluster_host": "10.2.3.4"}], password="secret")
    serialized = json.dumps(list_records(tmp_path, "RMS"))
    assert all(s not in serialized for s in ["10.2.3.4", "secret-table", '"password"'])


def test_t06_foreign_body_tenant_refused():
    with pytest.raises(ValueError):
        validate_submission({"tenant_id": "DIGICOW", "source_ids": ["rms_mysql"]}, "RMS", ["operator"])


def test_t06_analyst_cannot_launch():
    with pytest.raises(PermissionError):
        validate_submission({"source_ids": ["rms_mysql"]}, "RMS", ["ask_console_user"])


def test_t06_foreign_source_refused():
    with pytest.raises(ValueError):
        validate_submission({"source_ids": ["digicow_rds"]}, "RMS", ["operator"])


def test_t06_client_sql_and_credentials_refused():
    with pytest.raises(ValueError):
        validate_submission({"source_ids": ["rms_mysql"], "password": "x", "sql": "DROP TABLE x"}, "RMS", ["operator"])


def test_t08_placeholder_never_complete():
    assert classify_payload({"note": "Commit-A shape gate landed"}) == "UNVERIFIED"


def test_t08_matching_output_validates():
    assert validate_output(output(), "cr-test", "RMS", "rms_mysql")["table_count"] == 3


@pytest.mark.parametrize("change", [
    {"tenant_id": "DIGICOW"}, {"census_run_id": "cr-foreign"},
    {"table_count": -1}, {"table_count": True}, {"source_rows_returned": 1},
    {"execution_location": "pod"}, {"rows": [{"content": "forbidden"}]},
    {"worker_receipt_id": ""}, {"protocol": "demo"},
])
def test_t07_t08_invalid_receipt_refused(change):
    with pytest.raises(ValueError):
        validate_output(output(**change), "cr-test", "RMS", "rms_mysql")


def test_t08_mixed_source_result_not_complete():
    payload = {"protocol": "akki-census-aggregate-v1", "outcomes": [output(), {"status": "blocked"}],
               "registry_receipts": [{"receipt_id": "r1"}]}
    assert classify_payload(payload) == "PARTIAL"


def test_t08_no_registry_receipt_no_complete():
    assert classify_payload({"protocol": "akki-census-aggregate-v1", "outcomes": [output()]}) == "UNVERIFIED"