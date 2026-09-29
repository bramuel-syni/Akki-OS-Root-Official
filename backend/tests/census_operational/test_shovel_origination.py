"""Shovel origination: Targeta orders, the shovel cuts, Northena banks, CIF proposes.
Offline: engine surfaces run for real; the census store and ledger writer are stubbed."""
import contextlib
import json

import pytest

from contracts.northena_ledger import LedgerArtifactRef
from services.census_autonomy import census_scoop_origination as shovel
from services.targeta import core as targeta_core, gate as targeta_gate, plan as targeta_plan

TIB = shovel.TIB
REF = LedgerArtifactRef(artifact_type="objective_request", artifact_id="census-shovel:RMS", version="snap-test")


def _region(ref, source_id, label, volume, status="partial", enumeration="partial", **extra):
    return {"source_ref": ref, "source_id": source_id, "label": label, "kind": extra.pop("kind", "nas"),
            "volume_bytes": volume, "status": status, "enumeration": enumeration, **extra}


@pytest.fixture
def estate(monkeypatch):
    regions = [
        _region("source_" + "a" * 24, "rms_nas", "channel01", 7 * TIB),                       # oversized, pending
        _region("source_" + "b" * 24, "rms_nas", "channel02", 600 * 1024 ** 3),                # fits with c
        _region("source_" + "c" * 24, "rms_nas", "channel03", 300 * 1024 ** 3),
        _region("source_" + "d" * 24, "rms_nas", "channel04", 500 * 1024 ** 3),                # spills to next scoop
        _region("source_" + "e" * 24, "rms_mysql", "iebc", 2 * 1024 ** 3, "complete", "metadata_full", kind="mysql"),  # consumed
        _region("source_" + "f" * 24, "rms_mysql", "artists_app", None, "blocked", None, kind="mysql"),              # declared only
    ]
    monkeypatch.setattr(shovel, "inventory", lambda tenant, records: {"source_details": regions})
    monkeypatch.setattr(shovel.operational_reads, "records", lambda tenant: [])
    monkeypatch.setattr(shovel, "_inflight_sources", lambda tenant: set())
    monkeypatch.setenv("CENSUS_SCHEDULER_MAX_INFLIGHT", "3")
    monkeypatch.setenv("CENSUS_JOB_MAX_SECONDS", "3600")
    return regions


def test_live_full_source_pass_collapses_to_one_adoptable_target(estate, monkeypatch):
    monkeypatch.setattr(shovel, "_inflight_sources", lambda tenant: {"rms_nas", "rms_obs"})
    rows, _ = shovel.registry_rows("RMS")
    nas = [r for r in rows if r["region"] == "rms_nas"]
    assert len(nas) == 1 and nas[0]["source_ref"] == "rms_nas:inflight" and nas[0]["status"] == "inflight"
    assert nas[0]["volume_bytes"] == sum(r["volume_bytes"] for r in estate if r["source_id"] == "rms_nas" and r["status"] != "complete")
    assert nas[0]["defensibility_class"] == "fact"
    assert next(r for r in rows if r["region"] == "rms_obs")["status"] == "inflight"
    mining, scoops = _plan_from(rows)
    live = next(s for s in scoops if s["source_id"] == "rms_nas")
    assert live["kind"] == "discovery" and live["source_refs"] is None and live["volume_bytes"] == nas[0]["volume_bytes"]


def _plan_from(rows, target=TIB, shape="rms_mysql rms_obs rms_nas"):
    eligible = targeta_core.eligible_and_rank(rows, shovel.FLOOR, shape)
    ordered, version = targeta_gate.compose_ordering(eligible, thresholds=None)
    mining = targeta_plan.build_plan(ordered=ordered, core_baseline=eligible, floor=shovel.FLOOR, mode="per_run",
                                     governing_artifact_ref=REF, registry_snapshot_ref="snap-test", yield_layer_version=version)
    return mining, shovel._cut_scoops(mining.ordered_targets, rows, target)


def test_registry_rows_classify_pending_consumed_and_unmeasured(estate):
    rows, consumed = shovel.registry_rows("RMS")
    by_ref = {r["source_ref"]: r for r in rows}
    assert [c["label"] for c in consumed] == ["iebc"]
    assert by_ref["source_" + "a" * 24]["defensibility_class"] == "fact"          # measured region
    assert by_ref["source_" + "f" * 24]["defensibility_class"] == "utterance"     # declared, unmeasured
    assert by_ref["rms_obs:unmeasured"]["status"] == "unmeasured"                 # admitted source, no region yet
    assert by_ref["rms_obs:unmeasured"]["region"] == "rms_obs"


def test_targeta_order_is_deterministic_and_plan_id_reproducible(estate):
    rows, _ = shovel.registry_rows("RMS")
    mining_a, scoops_a = _plan_from(rows)
    mining_b, scoops_b = _plan_from(list(reversed(rows)))
    assert mining_a.plan_id == mining_b.plan_id
    assert mining_a.yield_layer_version == "core-only"
    assert [s["source_refs"] for s in scoops_a] == [s["source_refs"] for s in scoops_b]
    # Measured (fact) targets rank ahead of declared-only (utterance) ones; ties by source_ref.
    classes = [next(r for r in rows if r["source_ref"] == t.source_ref)["defensibility_class"] for t in mining_a.ordered_targets]
    assert classes == sorted(classes, key=lambda c: 0 if c == "fact" else 1)


def test_shovel_cuts_one_tib_scoops_in_targeta_order(estate):
    rows, _ = shovel.registry_rows("RMS")
    mining, scoops = _plan_from(rows)
    order = [t.source_ref for t in mining.ordered_targets]
    walked = [ref for s in scoops for ref in (s["source_refs"] or [f"{s['source_id']}:unmeasured"])]
    assert walked == order                                                        # no second ranking
    oversized = [s for s in scoops if s["oversized"]]
    assert len(oversized) == 1 and oversized[0]["source_refs"] == ["source_" + "a" * 24]
    assert all(s["volume_bytes"] <= TIB for s in scoops if not s["oversized"])
    by_ref = {r["source_ref"]: r for r in rows}
    assert all(by_ref[r["source_ref"]]["region"] == s["source_id"] for s in scoops for r in s["regions"])  # one source per scoop
    discovery = [s for s in scoops if s["kind"] == "discovery"]
    assert [s["source_id"] for s in discovery] == ["rms_obs"] and discovery[0]["source_refs"] is None
    assert [s["sequence"] for s in scoops] == list(range(len(scoops)))
    assert all(s["state"] == "queued" for s in scoops)


def test_objective_shape_conditions_targeta_order(estate):
    rows, _ = shovel.registry_rows("RMS")
    mining, _ = _plan_from(rows, shape="rms_mysql")
    assert mining.ordered_targets[0].region == "rms_mysql"                        # relevance 1.0 first


@pytest.fixture
def stubbed_store(monkeypatch, tmp_path):
    saved, ledger, enqueued = {}, [], []
    monkeypatch.setattr(shovel.store, "cursor_dir", lambda: tmp_path)
    monkeypatch.setattr(shovel.store, "save", lambda doc: saved.__setitem__(doc["census_run_id"], dict(doc)))
    monkeypatch.setattr(shovel.store, "get", lambda run_id, tenant: saved.get(run_id))
    monkeypatch.setattr(shovel.store, "runs", lambda tenant: list(saved.values()))
    monkeypatch.setattr(shovel.store, "lock", lambda key, blocking=True: contextlib.nullcontext(True))
    monkeypatch.setattr(shovel.store, "now", lambda: "2026-09-29T00:00:00+00:00")

    def enqueue(tenant, principal, sources, key, lawful_ref, worker_id=None, source_refs=None):
        enqueued.append(key)
        row = {"census_run_id": "cr-" + f"{len(enqueued):012x}", "tenant_id": tenant, "principal_id": principal,
               "source_ids": sources, "idempotency_key": key, "status": "PENDING", "outcomes": [],
               "lawful_basis_admit_ref": lawful_ref, "worker_id": worker_id, "source_refs": source_refs}
        saved[row["census_run_id"]] = row
        return row, True
    monkeypatch.setattr(shovel.store, "enqueue", enqueue)

    async def record(row):
        ledger.append(row)
    monkeypatch.setattr(shovel, "ledger_record", record)
    return {"saved": saved, "ledger": ledger, "enqueued": enqueued}


def _saved_plan(rows, scoops, mining):
    plan = {"plan_id": mining.plan_id, "tenant_id": "RMS", "principal_id": "p1", "state": "active", "worker_id": "akki-vm",
            "target_bytes": TIB, "created_at": "2026-09-29T00:00:00+00:00", "northena_run_id": "run-test",
            "northena_trace_id": "trc-test", "governing_artifact_ref": REF.model_dump(mode="json"),
            "lawful_basis_ref": "/tmp/admit.json", "ledger_rows": [{"row_id": "led-admit", "stage": "admit", "decision": "admitted", "reason": "admitted"}],
            "registry_snapshot_ref": "snap-test", "scoops": scoops, "cif_proposals": []}
    shovel.save_plan(plan)
    return plan


def test_commission_and_advance_walk_the_order_through_northena(estate, stubbed_store):
    rows, _ = shovel.registry_rows("RMS")
    mining, scoops = _plan_from(rows)
    plan = _saved_plan(rows, scoops, mining)
    row, fresh = shovel.commission_scoop(plan, 0, "p1", "/tmp/admit.json")
    assert fresh and row["scoop_plan_id"] == mining.plan_id and row["scoop_index"] == 0
    assert row["source_ids"] == [scoops[0]["source_id"]] and row["source_refs"] == scoops[0]["source_refs"]
    assert stubbed_store["enqueued"] == [f"{mining.plan_id}-scoop000"]
    # Scoop 0 finishes with coverage; the plan banks it and commissions scoop 1.
    row.update(status="PARTIAL", proof_ref="results/x.json",
               outcomes=[{"source_id": row["source_ids"][0], "status": "partial", "sources": [{"file_count": 1200}]}])
    stubbed_store["saved"][row["census_run_id"]] = row
    nxt = shovel.advance_plan(row)
    reloaded = shovel.load_plan("RMS", mining.plan_id)
    assert reloaded["scoops"][0]["state"] == "banked" and reloaded["scoops"][0]["progress_units"] == 1200
    assert reloaded["scoops"][1]["state"] == "commissioned" and reloaded["scoops"][1]["census_run_id"] == nxt
    converge = [r for r in stubbed_store["ledger"] if r.stage == "converge"]
    assert [r.decision for r in converge] == ["continue"] and converge[0].reason.startswith("scoop_000_banked:PARTIAL")
    # Re-advancing the same finished run is a no-op (already banked).
    assert shovel.advance_plan(row) is None


def test_flatline_halt_proposes_through_cif_and_moves_on(estate, stubbed_store):
    rows, _ = shovel.registry_rows("RMS")
    mining, scoops = _plan_from(rows)
    plan = _saved_plan(rows, scoops, mining)
    row, _ = shovel.commission_scoop(plan, 0, "p1", "/tmp/admit.json")
    row.update(status="PARTIAL", scope_halt={"reason": "starvation_output_flatline", "message": "no growth", "at_utc": "t"},
               outcomes=[{"source_id": row["source_ids"][0], "status": "partial", "sources": [{"file_count": 5}]}])
    stubbed_store["saved"][row["census_run_id"]] = row
    shovel.advance_plan(row)
    reloaded = shovel.load_plan("RMS", mining.plan_id)
    assert reloaded["scoops"][0]["state"] == "halted"
    proposal = reloaded["cif_proposals"][0]
    assert proposal["note"] == "scope_starved_flatline" and proposal["accepted"] is True
    assert proposal["routed"] == "research_loop_appended" and row["census_run_id"] in proposal["citations"]
    assert reloaded["scoops"][1]["state"] == "commissioned"
    from services.cif.output_routing import get_research_loop_items
    assert any(p.proposal_id == proposal["proposal_id"] for p in get_research_loop_items())


def test_plan_terminates_budget_without_progress_and_success_with_progress(estate, stubbed_store, monkeypatch):
    rows, _ = shovel.registry_rows("RMS")
    mining, scoops = _plan_from(rows)
    plan = _saved_plan(rows, scoops[-1:], mining)             # single-scoop plan
    row, _ = shovel.commission_scoop(plan, 0, "p1", "/tmp/admit.json")
    row.update(status="REFUSED", outcomes=[{"source_id": row["source_ids"][0], "status": "blocked", "reason_code": "EXECUTION_NOT_VERIFIED"}])
    stubbed_store["saved"][row["census_run_id"]] = row
    assert shovel.advance_plan(row) is None
    reloaded = shovel.load_plan("RMS", mining.plan_id)
    assert reloaded["state"] == "terminated"
    assert stubbed_store["ledger"][-1].decision == "terminate_budget"
    # With progress the plan terminates successfully and asks for a successor over what remains.
    calls = []
    monkeypatch.setattr(shovel, "originate_successor", lambda p: calls.append(p["plan_id"]))
    plan2 = dict(plan, plan_id="plan_second", state="active", scoops=[dict(s, state="queued") for s in scoops[-1:]], ledger_rows=[], cif_proposals=[])
    shovel.save_plan(plan2)
    row2, _ = shovel.commission_scoop(plan2, 0, "p1", "/tmp/admit.json")
    row2.update(status="COMPLETE", outcomes=[{"source_id": row2["source_ids"][0], "status": "complete", "sources": [{"table_count": 9}]}])
    stubbed_store["saved"][row2["census_run_id"]] = row2
    shovel.advance_plan(row2)
    assert stubbed_store["ledger"][-1].decision == "terminate_success" and calls == ["plan_second"]


def test_inflight_same_scope_run_is_adopted_not_duplicated(estate, stubbed_store):
    rows, _ = shovel.registry_rows("RMS")
    mining, scoops = _plan_from(rows)
    plan = _saved_plan(rows, scoops, mining)
    first = scoops[0]
    stubbed_store["saved"]["cr-aaaaaaaaaaaa"] = {"census_run_id": "cr-aaaaaaaaaaaa", "tenant_id": "RMS", "status": "PENDING",
                                                 "source_ids": [first["source_id"]], "source_refs": first["source_refs"], "outcomes": []}
    row, fresh = shovel.commission_scoop(plan, 0, "p1", "/tmp/admit.json")
    assert row["census_run_id"] == "cr-aaaaaaaaaaaa" and fresh is False and stubbed_store["enqueued"] == []
    assert row["scoop_plan_id"] == mining.plan_id
    assert shovel.load_plan("RMS", mining.plan_id)["scoops"][0]["adopted_inflight"] is True


def test_reconcile_advances_a_finished_but_unadvanced_scoop(estate, stubbed_store):
    rows, _ = shovel.registry_rows("RMS")
    mining, scoops = _plan_from(rows)
    plan = _saved_plan(rows, scoops, mining)
    row, _ = shovel.commission_scoop(plan, 0, "p1", "/tmp/admit.json")
    row.update(status="REFUSED", outcomes=[{"source_id": row["source_ids"][0], "status": "blocked", "reason_code": "BLOCKED"}])
    stubbed_store["saved"][row["census_run_id"]] = row
    active = shovel.active_plan("RMS")
    assert active["scoops"][0]["state"] == "banked" and active["scoops"][1]["state"] == "commissioned"


def test_saved_plan_roundtrip_and_snapshot_ref_stable(estate, stubbed_store):
    rows, consumed = shovel.registry_rows("RMS")
    assert shovel._snapshot_ref(rows, consumed) == shovel._snapshot_ref(list(rows), list(consumed))
    mining, scoops = _plan_from(rows)
    plan = _saved_plan(rows, scoops, mining)
    assert json.loads(shovel._plan_path("RMS", mining.plan_id).read_text())["plan_id"] == mining.plan_id
    assert shovel.load_plan("RMS", "plan_missing") is None
