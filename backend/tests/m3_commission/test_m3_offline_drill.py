"""M3 offline drill: ceremony → runtime attestation (worker executed in-process, real Ed25519) →
draft → feasibility (sizing) → freeze (requester scope group + interim stand-in) → approved plan →
class-matched dispatch → admit_limits ack → write-verb refusal receipt. SYNTHETIC tenant on a fake
ledger; no SSH, no estate bytes. Nothing here is a live gate proof.
"""
import asyncio
import json
import sys
import time
from contextlib import contextmanager

import pytest

sys.path.insert(0, "/app/backend/vendored/extraction_akki/backend")
sys.path.insert(0, "/app/backend/tests/activation_controls")
sys.path.insert(0, "/app/backend/tests/portal_operational")

import test_native_control_ledger as native_helpers  # noqa: E402
from test_w1_control_record_contract_red import _FakeDb  # noqa: E402

from services.activation.approvals import approved_plan  # noqa: E402
from services.activation.record_shapes import Quantity, quantities  # noqa: E402
from services.activation.reservations import Reservations  # noqa: E402
from services.activation.runtime_limits import RuntimeEnvelope  # noqa: E402
from services.commissioning import approvals as approvals_api, commission, shaping  # noqa: E402
from services.enforce.control_scope import bind_control_scope  # noqa: E402
from services.enforce.principal_context_adapter import principal_context  # noqa: E402
from services.estate_admission import ceremony, runtimes, signing  # noqa: E402
from services.estate_admission.resolver import LedgerAdmittedSigners, ledger_principal_lookup  # noqa: E402
from services.extraction_runtime import remote, structured_records_worker as worker  # noqa: E402
from services.northena.execution_models import Held  # noqa: E402
from services.portal_operational.entitlements import read_view  # noqa: E402
from services.work_orders import kind_profiles, sizing  # noqa: E402

TENANT = "tenant-SYNTHETIC-m3"
UNIT = "synthetic_source"
REQUESTER, BUDGET_HOLDER, DPO = "principal-requester", "principal-budget", "principal-dpo"


@contextmanager
def scope(principal, tenant=TENANT):
    with principal_context(principal), bind_control_scope({"principal_id": principal, "tenant_id": tenant}):
        yield {"principal_id": principal, "tenant_id": tenant, "roles": ["operator"]}


def run(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:  # another test on this worker closed its loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@pytest.fixture
def db():
    return _FakeDb(ledger_v1_control_events=native_helpers.ConcurrentCollection())


@pytest.fixture
def custody(tmp_path, monkeypatch):
    monkeypatch.setenv("AKKI_ESTATE_CUSTODY_DIR", str(tmp_path / "custody"))
    return tmp_path


@pytest.fixture
def in_process_runtime(tmp_path, monkeypatch):
    """The admitted seam is replaced by executing the worker module here, in a temp state dir per runtime.
    Signatures, envelopes and protocol are the real worker code; only the transport is absent."""
    calls = []

    def call(descriptor, control, *, deadline_seconds):
        calls.append((descriptor["runtime_id"], control["mode"]))
        payload = {**control, "runtime_id": descriptor["runtime_id"], "state_dir": str(tmp_path / descriptor["runtime_id"]),
                   "signer_id": descriptor["principal_id"], "key_id": descriptor["key_id"], "bundle": "", "code_sha256": ""}
        return worker.execute(payload)

    async def call_async(descriptor, control, *, deadline_seconds):
        return call(descriptor, control, deadline_seconds=deadline_seconds)

    monkeypatch.setattr(remote, "call_async", call_async)
    gpu = {"cpu_cores": 36, "gpu_count": 2, "memory_gb": 460, "compute_classes": ["cpu", "gpu"], "accounting": ["cpu_seconds"]}
    cpu = {"cpu_cores": 4, "gpu_count": 0, "memory_gb": 16, "compute_classes": ["cpu"], "accounting": ["cpu_seconds"]}
    observed = {"rt-gpu-a": gpu, "rt-gpu-b": gpu, "rt-cpu": cpu}
    original = worker._capacity_observed
    monkeypatch.setattr(worker, "_capacity_observed", lambda: original())
    real_attest = worker.attest

    def attest(control):
        value = real_attest(control)
        value["capacity_observed"] = observed[control["runtime_id"]]
        return value
    monkeypatch.setitem(worker.MODES, "attest", attest)
    return calls


def descriptor(rid, roles, reach_direct=(UNIT,)):
    return {"runtime_id": rid, "roles": roles, "transport": {"kind": "ssh_seam", "host_slug": rid}, "python": "python3",
            "state_dir": "~/.akki-extraction", "kinds": ["source"],
            "enforced_dimensions": ["spend", "wall_clock", "scanned_records", "returned_records", "bytes_read", "active_compute"],
            "reach": {"direct": list(reach_direct), "pull_seam": []}}


ALLOCATION = [{"dimension": "spend", "unit": "USD", "quantity": "0"}, {"dimension": "wall_clock", "unit": "seconds", "quantity": "2592000"},
              {"dimension": "scanned_records", "unit": "records", "quantity": "50000000"},
              {"dimension": "returned_records", "unit": "records", "quantity": "10000000"},
              {"dimension": "bytes_read", "unit": "bytes", "quantity": "5000000000000"},
              {"dimension": "active_compute", "unit": "cpu_seconds", "quantity": "10000000"},
              {"dimension": "active_compute", "unit": "gpu_seconds", "quantity": "1000000"}]
LICENCE = {"plan_identifier": "pilot.synthetic", "seat_count": 3, "compute_dial": "managed", "frontier_dial": "your_keys",
           "credits_per_seat_per_period": 0, "pooled_credits_flag": True, "seat_soft_limit": 3, "organisation_ceiling": 100,
           "period": "month", "renewal_date": "2027-09-01T00:00:00+00:00", "status": "active", "terms_identifier": "TERMS-SYNTHETIC-v0"}
DIALS = ({"custody_floor": "v0", "approving_authority": "v0", "external_crossing": "v0", "disclosure_counterparties": "v0"},
         {"crossing_decision_table": "v0", "acceptance_standard": "v0", "cleanliness_pack": "v0"}, 1)


async def perform_ceremony(db, tmp_path, *, seated, stand_in):
    units = [UNIT]
    org_id = ceremony.opaque("org", TENANT, "Synthetic estate")
    with scope(org_id):
        await ceremony.admit_organisation(db, TENANT, "Synthetic estate", "test owner")
        agents = {}
        for scope_name, key_id, perms in (("northena:planner", "northena-planner", ["activation:plan"]),
                                          ("estate:allocator", "estate-allocator", ["activation:allocation"]),
                                          ("estate:rights-authority", "estate-rights-authority",
                                           ["activation:observation:anchor", "activation:observation:rights"])):
            pid = ceremony.opaque("agent", TENANT, scope_name)
            await ceremony.admit_member(db, TENANT, org_id, pid, scope_name, "test owner", kind="agent", autonomy_scope=scope_name)
            await ceremony.admit_custody_signer(db, TENANT, pid, key_id, perms, units)
            agents[scope_name] = (pid, key_id)
    refs = {}
    for pid, seats in ((REQUESTER, ["scope.requester"]), (BUDGET_HOLDER, ["scope.requester", "expenditure.estate"]),
                       (DPO, ["scope.requester", "extraction.controlled"])):
        with scope(org_id):
            aref = await ceremony.admit_member(db, TENANT, org_id, pid, pid, "test owner")
            await ceremony.admit_custody_signer(db, TENANT, pid, "approver-" + pid, ["activation:approval:" + s for s in seats], units)
        refs[pid] = await ceremony.bank_membership(db, TENANT, pid, org_id, aref)
    with scope(org_id):
        groups = [{"group": "expenditure.estate", "purpose": "expenditure", "quorum": 1, "members": [BUDGET_HOLDER] if seated else []},
                  {"group": "extraction.controlled", "purpose": "extraction", "quorum": 1, "members": [DPO] if seated else []}]
        stand = await ceremony.admit_stand_in(db, TENANT, org_id, "test owner", [g["group"] for g in groups if not g["members"]],
                                              units, "synthetic stand-in basis") if stand_in else None
        await ceremony.set_approval_groups(db, TENANT, groups, stand)
        start, end, iso = ceremony.period_bounds()
        await ceremony.bank_licence(db, TENANT, {**LICENCE, "organisation_principal_id": org_id}, refs[REQUESTER], start, end, iso)
        await ceremony.set_dials(db, TENANT, *DIALS)
        await ceremony.bank_allocation(db, TENANT, *agents["estate:allocator"], ALLOCATION, LICENCE["terms_identifier"], units)
        lawful = tmp_path / "lawful.json"
        lawful.write_text(json.dumps({"lawful_basis": "SYNTHETIC"}))
        await ceremony.bank_rights(db, TENANT, *agents["estate:rights-authority"], units, str(lawful))
        admitted = {}
        for rid, roles in (("rt-gpu-a", ["worker"]), ("rt-gpu-b", ["inspector", "custodian"]), ("rt-cpu", ["worker"])):
            admitted[rid] = await ceremony.admit_runtime(db, TENANT, descriptor(rid, roles), units)
    return org_id, agents, admitted


SYNTHETIC_TABLE = {"census_run_id": "cr-SYNTHETIC", "observed_at": "2026-09-29T00:00:00+00:00", "source_ref": "source_" + "0" * 24,
                   "label": "synthetic", "database": "app", "table": "categories", "row_count": 40, "column_count": 3,
                   "columns": ["id", "name", "kind"], "column_types": {"id": "int", "name": "varchar", "kind": "varchar"},
                   "role_signals": [], "primary_key": "id", "personal_columns": [], "data_length_bytes": 4096}


@pytest.fixture
def censused(monkeypatch):
    from services.commissioning import census_profile, feasibility
    monkeypatch.setitem(feasibility.SOURCE_TENANTS, UNIT, TENANT)

    async def tables_for(tenant, source_id):
        return [SYNTHETIC_TABLE] if source_id == UNIT and tenant == TENANT else None
    monkeypatch.setattr(feasibility, "tables_for", tables_for)
    monkeypatch.setattr(census_profile, "tables_for", tables_for)


# ------------------------------------------------------------------------------------------ kind profiles & sizing

def test_every_registered_kind_names_a_compute_class_and_split():
    table = kind_profiles.routable()
    assert set(table) == set(kind_profiles.REGISTRY) and len(table) >= 11
    for kind, row in table.items():
        assert row["compute_class"] in kind_profiles.COMPUTE_CLASSES
        assert set(row["scaling"]) == ({"cpu", "gpu"} if row["compute_class"] == "mixed" else {row["compute_class"]})
    census = kind_profiles.CENSUS_DEEP
    assert census.scaling == {"cpu": "scanned_records", "gpu": "media_duration"}
    assert kind_profiles.CENSUS_STRUCTURAL_WALK.compute_class == "cpu" and kind_profiles.CENSUS_PERCEPTION_TRANSCRIBE.compute_class == "gpu"
    assert kind_profiles.TRAINING_FINE_TUNE.compute_class == "gpu" and kind_profiles.REPORT_RUN.compute_class == "cpu"


def test_kind_without_compute_class_or_split_is_not_routable():
    base = kind_profiles.STRUCTURED_RECORDS.__dict__
    with pytest.raises(ValueError, match="KIND_NOT_ROUTABLE_WITHOUT_COMPUTE_CLASS"):
        kind_profiles.KindProfile(**{**base, "job_kind": "x", "compute_class": ""})
    with pytest.raises(ValueError, match="KIND_COMPUTE_SPLIT_UNNAMED"):
        kind_profiles.KindProfile(**{**base, "job_kind": "x", "compute_class": "mixed"})


def test_sizing_from_prior_then_from_record_and_census_split_drops_gpu_without_media():
    profile = kind_profiles.STRUCTURED_RECORDS
    bounds = {**profile.default_bounds, "max_records": 500}
    prior = sizing.size(profile, bounds)
    assert prior["classes"]["cpu"]["scaling_unit"] == "scanned_records" and prior["classes"]["cpu"]["scale"] == 1000
    assert prior["classes"]["cpu"]["estimate_seconds"] == pytest.approx(20 + 1000 * 0.002)
    assert prior["classes"]["cpu"]["reservation_seconds"] == 66 and prior["needs"] == {"cpu_cores": 1, "gpu_count": 0, "memory_gb": 1}
    measured = sizing.size(profile, bounds, {"cpu": {"seconds_per_unit": 0.01, "runs": 3}})
    assert measured["classes"]["cpu"]["rate_basis"].startswith("measured record (3")
    assert measured["classes"]["cpu"]["estimate_seconds"] == pytest.approx(20 + 1000 * 0.01)
    deep = kind_profiles.CENSUS_DEEP
    both = sizing.size(deep, {**deep.default_bounds})
    assert set(both["classes"]) == {"cpu", "gpu"} and both["needs"]["gpu_count"] == 1
    no_media = sizing.size(deep, {**deep.default_bounds, "max_media_seconds": 0})
    assert set(no_media["classes"]) == {"cpu"} and no_media["needs"]["gpu_count"] == 0
    limits = deep.limits(deep.default_bounds, both)
    assert [(q["dimension"], q["unit"]) for q in limits if q["dimension"] == "active_compute"] == \
        [("active_compute", "cpu_seconds"), ("active_compute", "gpu_seconds")]
    quantities([Quantity(**q) for q in limits])
    with pytest.raises(ValueError):
        quantities([Quantity(dimension="spend", unit="USD", quantity="1"), Quantity(dimension="spend", unit="EUR", quantity="1")])


# ------------------------------------------------------------------------------------------ ceremony, attestation, selection

def test_ceremony_attests_runtimes_and_resolves_membership_licence_and_signers(db, custody, in_process_runtime):
    org_id, agents, admitted = run(perform_ceremony(db, custody, seated=True, stand_in=False))
    with scope(REQUESTER) as s:
        view = run(read_view(db, s))
        assert view.status == "resolved" and view.licence.terms_identifier == "TERMS-SYNTHETIC-v0"
        principal = run(ledger_principal_lookup(db)(REQUESTER))
        assert principal.parent_organisation_id == org_id
        planner_pid, planner_key = agents["northena:planner"]
        signer = run(LedgerAdmittedSigners(db).resolve(TENANT, planner_pid, planner_key))
        assert signer.permissions == ("activation:plan",) and signer.public_key_hex == signing.ensure_key(TENANT, planner_key)
        table = run(runtimes.admitted_runtimes(db, TENANT))
        assert table["rt-gpu-a"]["compute_classes"] == ["cpu", "gpu"] and table["rt-cpu"]["capacity"]["gpu_count"] == 0
        assert table["rt-gpu-a"]["key_id"].startswith("rk-") and table["rt-gpu-a"]["principal_id"] == "runtime:rt-gpu-a"
        receipts = ceremony.receipts_for(db)
        worker_receipt = run(receipts.resolve(admitted["rt-gpu-a"][1], kind="worker"))
        assert worker_receipt.signer_id == "runtime:rt-gpu-a" and worker_receipt.claims["runtime_id"] == "rt-gpu-a"
        assert ("rt-gpu-a", "attest") in in_process_runtime and ("rt-gpu-a", "sign_worker") in in_process_runtime
        # Re-running the signer admission with the same key and mandate is idempotent.
    with scope(org_id):
        before = len(db["ledger_v1_control_events"].docs)
        run(ceremony.admit_custody_signer(db, TENANT, agents["northena:planner"][0], "northena-planner", ["activation:plan"], [UNIT]))
        assert len(db["ledger_v1_control_events"].docs) == before


def test_dispatch_is_class_matched_with_headroom(db, custody, in_process_runtime):
    run(perform_ceremony(db, custody, seated=True, stand_in=False))
    cpu_job = sizing.size(kind_profiles.STRUCTURED_RECORDS, kind_profiles.STRUCTURED_RECORDS.default_bounds)
    gpu_job = sizing.size(kind_profiles.CENSUS_PERCEPTION_TRANSCRIBE, kind_profiles.CENSUS_PERCEPTION_TRANSCRIBE.default_bounds)
    with scope(REQUESTER):
        chosen, basis = run(runtimes.select(db, TENANT, "worker", "source", (UNIT,), sizing=cpu_job))
        assert chosen["runtime_id"] == "rt-cpu" and "exact class match ['cpu']" in basis
        chosen, basis = run(runtimes.select(db, TENANT, "worker", "source", (UNIT,), sizing=gpu_job))
        assert chosen["runtime_id"] == "rt-gpu-a" and "rt-cpu: classes ['cpu'] lack ['gpu']" in basis
        big = {**cpu_job, "needs": {"cpu_cores": 8, "gpu_count": 0, "memory_gb": 1}}
        chosen, basis = run(runtimes.select(db, TENANT, "worker", "source", (UNIT,), sizing=big))
        assert chosen["runtime_id"] == "rt-gpu-a" and "rt-cpu: no headroom" in basis
        with pytest.raises(Held, match="ADMITTED_RUNTIME_UNAVAILABLE_FOR_WORKER"):
            run(runtimes.select(db, TENANT, "worker", "source", (UNIT,), exclude=("rt-cpu", "rt-gpu-a"), sizing=cpu_job))


# ------------------------------------------------------------------------------------------ draft → feasibility → freeze

def draft_body(**kw):
    return shaping.DraftBody(objective_text="Extract the smallest clean table for the pilot.", operation="browse_estate", units=[UNIT], **kw)


def test_freeze_with_interim_stand_in_yields_an_approved_plan_and_sized_reservation(db, custody, in_process_runtime, censused):
    run(perform_ceremony(db, custody, seated=False, stand_in=True))
    with scope(REQUESTER) as s:
        view = run(shaping.save(db, s, draft_body()))
        assert view["feasibility"]["verdict"] == "warm" and view["freeze_ready"] is True
        assert view["feasibility"]["sizing"]["classes"]["cpu"]["reservation_seconds"] == 66
        seating = {g["purpose"]: g["seating"] for g in view["routing"]["groups"]}
        assert seating == {"scope": "requester_operator_standing", "expenditure": "interim_pilot_stand_in"}
        assert any(a["field"] == "compute" for a in view["assumed"]) and view["quote"]["total"] == "0"
        frozen = run(commission.commission(db, s, view["draft_id"], "idempotency-key-0001"))
        assert frozen["state"] == "commissioned" and frozen["stand_ins"][0]["group"] == "expenditure.estate"
        assert {a["by"] for a in frozen["approvals_signed"]} == {"requester", "interim_pilot_stand_in"}
        assert frozen["dispatch_intent"] == "runtime:rt-cpu"
        request = run(_frozen_request(db, s, frozen))
        receipts = ceremony.receipts_for(db)
        plan, plan_ref, approval_refs, expiry, _ = run(approved_plan(receipts, request))
        assert {g.group for g in plan.groups} == {"scope.requester", "expenditure.estate"} and len(approval_refs) == 2
        assert {(q.dimension, q.unit) for q in plan.limits} >= {("active_compute", "cpu_seconds"), ("scanned_records", "records")}
        reservation = run(Reservations(receipts).reserve(plan, plan_ref))
        assert reservation and run(Reservations(receipts).reserve(plan, plan_ref)) == reservation
        # Freeze is idempotent: the same draft cannot be commissioned twice and the plan stays unique.
        with pytest.raises(Exception):
            run(commission.commission(db, s, view["draft_id"], "idempotency-key-0001"))
        routing = run(approvals_api.routing(db, s, request.request_id))
        assert routing["state"] == "approved"


def test_freeze_with_seated_groups_waits_for_the_seated_approver_and_refusal_keeps_the_job(db, custody, in_process_runtime, censused):
    run(perform_ceremony(db, custody, seated=True, stand_in=False))
    with scope(REQUESTER) as s:
        view = run(shaping.save(db, s, draft_body()))
        assert view["routing"]["requires_other_approver"] is True
        frozen = run(commission.commission(db, s, view["draft_id"], "idempotency-key-0002"))
        request = run(_frozen_request(db, s, frozen))
        receipts = ceremony.receipts_for(db)
        with pytest.raises(Held, match="APPROVAL_GROUP_PENDING"):
            run(approved_plan(receipts, request))
    with scope(BUDGET_HOLDER) as b:
        queue = run(approvals_api.queue(db, b))
        assert [r["request_id"] for r in queue] == [request.request_id] and queue[0]["pending_for_you"] == ["expenditure.estate"]
        decided = run(approvals_api.decide(db, b, request.request_id, "expenditure.estate", "approved", "budget holder approves"))
        assert decided["state"] == "approved"
    with scope(REQUESTER):
        plan, *_ = run(approved_plan(ceremony.receipts_for(db), request))
        assert plan.request == request
    with scope(DPO) as d:
        with pytest.raises(Exception):  # not a seated member of the expenditure group
            run(approvals_api.decide(db, d, request.request_id, "expenditure.estate", "approved", "x"))


def test_feasibility_refuses_unknown_scope_and_uncensused_table(db, custody, censused):
    with scope(REQUESTER) as s:
        other = run(shaping.save(db, s, shaping.DraftBody(objective_text="x", operation="download_raw_data", units=[UNIT])))
        assert other["feasibility"]["verdict"] == "refuse" and other["feasibility"]["reason_code"] == "OPERATION_NOT_COMMISSIONABLE_HERE"
        wrong = run(shaping.save(db, s, draft_body(reach=shaping.Reach(database="app", table="missing"))))
        assert wrong["feasibility"]["verdict"] == "unknown" and wrong["feasibility"]["reason_code"] == "TABLE_NOT_CENSUSED"
        assert wrong["freeze_ready"] is False


async def _frozen_request(db, s, frozen):
    from services.northena.execution_models import Request
    from services.ledger_writer.mongo_control import digest
    return Request(request_id=frozen["request_id"], tenant_id=TENANT, principal_id=s["principal_id"], kind="source", engine="mtafiti",
                   objective_sha256=digest(frozen["envelope"]["objective_text"]), input_refs=("akki://source/" + UNIT,),
                   scope_refs=(UNIT,), deadline_epoch=frozen["deadline_epoch"])


# ------------------------------------------------------------------------------------------ worker modes (in-process)

def test_worker_admits_limits_signs_runtime_ack_refuses_unmeasurable_gpu_and_refuses_write_verbs(db, custody, in_process_runtime, tmp_path):
    run(perform_ceremony(db, custody, seated=False, stand_in=True))
    with scope(REQUESTER):
        table = run(runtimes.admitted_runtimes(db, TENANT))
    d = table["rt-cpu"]
    now = int(time.time())
    limits = [{"dimension": "spend", "unit": "USD", "quantity": "0"}, {"dimension": "wall_clock", "unit": "seconds", "quantity": "900"},
              {"dimension": "scanned_records", "unit": "records", "quantity": "1000"}, {"dimension": "returned_records", "unit": "records", "quantity": "500"},
              {"dimension": "bytes_read", "unit": "bytes", "quantity": "1000000"}, {"dimension": "active_compute", "unit": "cpu_seconds", "quantity": "66"}]
    envelope = RuntimeEnvelope(protocol="akki.runtime.limits/1", request_sha256="a" * 64, plan_ref="b" * 64, reservation_ref="c" * 64,
                               runtime_id="rt-cpu", operation_key="op-1", fence=3, limits=tuple(Quantity(**q) for q in limits),
                               starts_epoch=now - 1, stop_work_by_epoch=now + 800, terminate_by_epoch=now + 860)
    base = {"tenant_id": TENANT, "request_sha256": "a" * 64, "operation_key": "op-1", "fence": 3, "scope_refs": [UNIT], "job_kind": "k"}
    ack = run(remote.call_async(d, {**base, "mode": "admit_limits", "envelope": envelope.model_dump(mode="json")}, deadline_seconds=5))
    assert ack["status"] == "acknowledged"
    with scope(REQUESTER):
        receipts = ceremony.receipts_for(db)
        ref = run(receipts.record(signing.runtime_receipt(ack["receipt"])))
        recorded = run(receipts.resolve(ref, kind="observation", request_sha256="a" * 64))
        from services.ledger_writer.mongo_control import digest
        assert recorded.claims["category"] == "runtime" and recorded.claims["claim_sha256"] == digest(envelope.model_dump(mode="json"))
    gpu_limits = limits + [{"dimension": "active_compute", "unit": "gpu_seconds", "quantity": "10"}]
    gpu_env = envelope.model_copy(update={"limits": tuple(Quantity(**q) for q in gpu_limits)}).model_dump(mode="json")
    refused = run(remote.call_async(d, {**base, "mode": "admit_limits", "operation_key": "op-2", "envelope": gpu_env}, deadline_seconds=5))
    assert refused["status"] == "refused" and refused["reason_code"] == "RUNTIME_ACCOUNTING_UNAVAILABLE:gpu_seconds"
    write = run(remote.call_async(d, {**base, "mode": "write_attempt", "sql": "DELETE FROM app.categories WHERE id = 1", "sign": True}, deadline_seconds=5))
    assert write["status"] == "refused" and write["reason_code"] == "WRITE_VERB_REFUSED"
    with scope(REQUESTER):
        ref = run(ceremony.receipts_for(db).record(signing.runtime_receipt(write["receipt"])))
        assert run(ceremony.receipts_for(db).resolve(ref, kind="observation")).claims["category"] == "refusal"
    status = run(remote.call_async(d, {**base, "mode": "status"}, deadline_seconds=5))
    assert status["state"] == "unknown" and status["reason_code"] == "JOB_NOT_SUBMITTED"
    limiter = worker.Limiter(envelope.model_dump(mode="json"))
    limiter.before_batch({("scanned_records", "records"): 10, ("bytes_read", "bytes"): 5000})
    measured = {(q["dimension"], q["unit"]): q["quantity"] for q in limiter.quantities(7)}
    assert set(measured) == {(q["dimension"], q["unit"]) for q in limits} and measured[("returned_records", "records")] == "7"
    assert float(measured[("active_compute", "cpu_seconds")]) >= 0


# ------------------------------------------------------------------------------------------ rights follow lineage

def test_verified_artifact_receives_rights_along_worker_signed_lineage_and_withdrawn_parent_holds(db, custody, in_process_runtime, tmp_path):
    from services.extraction_runtime import derived_rights, worker_identity
    from services.non_gpu_governance.gate import NativeGovernance
    from services.non_gpu_governance.lineage import Rights
    from services.northena.execution_journal import LedgerJournal
    from services.northena.execution_models import Artifact, Request
    from services.ledger_writer.mongo_control import digest
    _, agents, _ = run(perform_ceremony(db, custody, seated=False, stand_in=True))
    request = Request(request_id="req-lineage", tenant_id=TENANT, principal_id=REQUESTER, kind="source", engine="mtafiti",
                      objective_sha256="a" * 64, input_refs=("akki://source/" + UNIT,), scope_refs=(UNIT,),
                      deadline_epoch=int(time.time()) + 3600)
    artifact = Artifact(ref="akki://artifact/" + TENANT + "/req-lineage/qualified-units", sha256="b" * 64, size_bytes=2,
                        tenant_id=TENANT, class_label="utterance")
    lineage = {"version": "akki.lineage.metadata/1", "artifact_ref": artifact.ref, "artifact_sha256": artifact.sha256,
               "parents": list(request.input_refs)}
    with scope(REQUESTER):
        receipts = ceremony.receipts_for(db)
        d = run(runtimes.admitted_runtimes(db, TENANT))["rt-cpu"]
        signed = worker_identity.receipt(str(tmp_path / "rt-cpu"), tenant_id=TENANT, signer_id=d["principal_id"], key_id=d["key_id"],
                                         kind="observation", scope_refs=[UNIT], request_sha256=request.digest(),
                                         claims=worker_identity.observation("lineage", request.digest(), lineage, typed={"lineage": lineage}))
        run(receipts.record(signing.runtime_receipt(signed)))
        gate = NativeGovernance(receipts, LedgerJournal(db))
        events = run(receipts.events())
        run(gate.rights.check(request, request.input_refs, events))  # sources alone: the ceremony's rights suffice
        # Without the extension the artefact itself has no current rights.
        with pytest.raises(Held, match="NATIVE_RIGHTS_PROOF_REQUIRED"):
            run(gate.rights.check(request, request.input_refs + (artifact.ref,), events, artifacts=(artifact,)))
        wrong = artifact.model_copy(update={"sha256": "c" * 64})
        with pytest.raises(Held, match="ARTIFACT_LINEAGE_REQUIRED"):
            run(derived_rights.extend(db, receipts, request, (wrong,), events))
        refs = run(derived_rights.extend(db, receipts, request, (artifact,), events))
        events = run(receipts.events())
        assert refs == {artifact.ref: derived_rights.existing(events, artifact.ref)}
        recorded = run(receipts.resolve(refs[artifact.ref], kind="observation"))
        assert recorded.signer_id == agents["estate:rights-authority"][0] and recorded.claims["rights"]["reason_code"] == derived_rights.REASON
        assert request.input_refs[0] in run(gate.rights.check(request, request.input_refs + (artifact.ref,), events, artifacts=(artifact,)))
        # Idempotent: a second pass reuses the proof; nothing is re-signed.
        before = len(db["ledger_v1_control_events"].docs)
        assert run(derived_rights.extend(db, receipts, request, (artifact,), events)) == refs
        assert len(db["ledger_v1_control_events"].docs) == before
        # A withdrawn source holds the descendant; the extension cannot revive it.
        pid, key_id = agents["estate:rights-authority"]
        anchor = run(receipts.resolve(recorded.claims["rights"]["policy_ref"], kind="observation"))
        withdrawn = Rights(version="akki.rights.metadata/1", unit_ref=request.input_refs[0], status="withdrawn",
                           policy_ref=anchor_ref_of(recorded), reason_code="SYNTHETIC_WITHDRAWAL")
        claim = {"category": "rights", "context_sha256": request.digest(), "evidence_mode": "measured",
                 "claim_sha256": digest(withdrawn.model_dump(mode="json")), "rights": withdrawn.model_dump(mode="json")}
        run(receipts.record(signing.sign_receipt(TENANT, pid, key_id, "observation", claim, scope_refs=anchor.scope_refs)))
        with pytest.raises(Held, match="DESCENDANT_RIGHTS_WITHDRAWN"):
            run(derived_rights.extend(db, receipts, request, (artifact,), run(receipts.events())))


def anchor_ref_of(rights_receipt):
    return rights_receipt.claims["rights"]["policy_ref"]
