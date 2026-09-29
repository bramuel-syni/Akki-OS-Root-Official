"""Census shovel origination through the designed engines — no bespoke planner.

Northena ADMITS the census objective and freezes it (Doc 05 §B5.1/§B5.2); Targeta
RANKS the retained estate regions deterministically into a reproducible MiningPlan
(mandate §9/§17 #8; yield seam closed); the shovel CUTS that ordered target list
into ~1 TiB scoops commissioned one at a time on the external worker; Northena's
ledger records gate/converge for every scoop; Solva's critic seam attaches
non-blocking findings; CIF PROPOSES (never ratifies) research-loop items when a
region exceeds one scoop or a scope starves. E1 plans; no estate bytes touch E1.
"""
import asyncio
import hashlib
import json
import math
import os
import threading
from datetime import datetime, timezone

from contracts.five_rings import DefensibilityClass
from contracts.northena_ledger import LedgerArtifactRef, LedgerRow
from services.census_autonomy import operational_reads, operational_store as store
from services.census_autonomy.operational_scope import SOURCE_TENANTS, sources_for
from services.census_autonomy.registry_surfaces import inventory
from services.northena import admit as northena_admit
from services.northena.ledger import record as ledger_record
from services.targeta import core as targeta_core, gate as targeta_gate, plan as targeta_plan

TIB = 1024 ** 4
FLOOR = DefensibilityClass.UTTERANCE
CONSUMED = {"full", "metadata_full"}


_LOOP = None


def _loop():
    """Coroutines (Northena ledger, Targeta persist) run on the loop Motor is bound to:
    the app loop when it is running, else one dedicated loop thread per process."""
    global _LOOP
    from core import client
    bound = getattr(client, "_io_loop", None)
    if bound is not None and bound.is_running():
        return bound
    if _LOOP is None:
        _LOOP = asyncio.new_event_loop()
        threading.Thread(target=_LOOP.run_forever, name="census-shovel-loop", daemon=True).start()
    return _LOOP


def _run(coro):
    return asyncio.run_coroutine_threadsafe(coro, _loop()).result(timeout=120)


def _now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _capacity():
    return {"concurrent_workers": int(os.environ["CENSUS_SCHEDULER_MAX_INFLIGHT"]),
            "pass_seconds": int(os.environ["CENSUS_JOB_MAX_SECONDS"]),
            "nas_dirs_per_sec": float(os.environ.get("CENSUS_NAS_DIRS_PER_SEC", "0.4")),
            "obs_objects_per_sec": float(os.environ.get("CENSUS_OBS_OBJECTS_PER_SEC", "850"))}


def _inflight_sources(tenant):
    """Sources whose unowned full-source pass (or its continuation) is still PENDING."""
    return {row["source_ids"][0] for row in store.runs(tenant)
            if row.get("status") == "PENDING" and not row.get("scoop_plan_id")
            and len(row.get("source_ids") or []) == 1 and not row.get("source_refs")}


def registry_rows(tenant):
    """Targeta's Registry read: retained regions still to consume + unmeasured sources.
    A measured region is `fact` (census measured it); a declared-only region is
    `utterance` (the owner said it exists; nothing measured yet). Consumed regions
    are not targets of a consume-fully objective (a re-census is a new admission).
    A source whose full-source pass is still in flight is one target: the shovel adopts
    that live chain rather than cutting the same regions again beside it."""
    regions = inventory(tenant, operational_reads.records(tenant))["source_details"]
    inflight = _inflight_sources(tenant)
    rows, consumed, seen, live = [], [], set(), {}
    for region in regions:
        seen.add(region["source_id"])
        pending = region.get("status") != "complete" or region.get("enumeration") not in CONSUMED
        row = {"source_ref": region["source_ref"], "region": region["source_id"], "label": region.get("label"),
               "kind": region.get("kind"), "status": region.get("status"), "enumeration": region.get("enumeration"),
               "volume_bytes": int(region.get("volume_bytes") or 0), "directories_pending": region.get("directories_pending"),
               "object_count": region.get("object_count"),
               "defensibility_class": "fact" if region.get("volume_bytes") else "utterance"}
        if not pending:
            consumed.append(row)
        elif region["source_id"] in inflight:
            live.setdefault(region["source_id"], []).append(row)
        else:
            rows.append(row)
    for source_id, parts in sorted(live.items()):
        volume = sum(p["volume_bytes"] for p in parts)
        rows.append({"source_ref": f"{source_id}:inflight", "region": source_id, "label": f"{len(parts)} regions in one live full-source pass",
                     "kind": parts[0]["kind"], "status": "inflight", "enumeration": "partial", "volume_bytes": volume,
                     "directories_pending": sum(p.get("directories_pending") or 0 for p in parts) or None,
                     "object_count": sum(p.get("object_count") or 0 for p in parts) or None,
                     "defensibility_class": "fact" if volume else "utterance"})
    for source_id in sorted(set(sources_for(tenant)) - seen):
        rows.append({"source_ref": f"{source_id}:unmeasured", "region": source_id, "label": None, "kind": None,
                     "status": "inflight" if source_id in inflight else "unmeasured", "enumeration": None, "volume_bytes": 0,
                     "directories_pending": None, "object_count": None, "defensibility_class": "utterance"})
    return rows, consumed


def _snapshot_ref(rows, consumed):
    payload = json.dumps([rows, consumed], sort_keys=True, default=str)
    return "snap-" + hashlib.sha256(payload.encode()).hexdigest()[:16]


def _cut_scoops(ordered, rows, target):
    """The shovel: walk Targeta's order and cut consecutive same-source targets into
    ~target-byte scoops. Unmeasured sources are discovery scoops (full-source
    resumable pass); a region larger than one scoop is its own multi-pass scoop."""
    by_ref = {r["source_ref"]: r for r in rows}
    scoops, current = [], None

    def flush():
        nonlocal current
        if current:
            scoops.append(current)
        current = None

    for target_location in ordered:
        row = by_ref[target_location.source_ref]
        if row["status"] in ("unmeasured", "inflight"):
            flush()
            scoops.append({"kind": "discovery", "source_id": row["region"], "regions": [row], "volume_bytes": row["volume_bytes"],
                           "oversized": False,
                           "note": ("Adopt the live full-source pass until its epoch completes." if row["status"] == "inflight"
                                    else "Measure region sizes first (resumable full-source pass).")})
            continue
        if row["volume_bytes"] >= target:
            flush()
            scoops.append({"kind": "region", "source_id": row["region"], "regions": [row],
                           "volume_bytes": row["volume_bytes"], "oversized": True})
            continue
        if current and (current["source_id"] != row["region"] or current["volume_bytes"] + row["volume_bytes"] > target):
            flush()
        if current is None:
            current = {"kind": "region", "source_id": row["region"], "regions": [], "volume_bytes": 0, "oversized": False}
        current["regions"].append(row)
        current["volume_bytes"] += row["volume_bytes"]
    flush()
    cap = _capacity()
    for index, scoop in enumerate(scoops):
        scoop["sequence"] = index
        scoop["source_refs"] = None if scoop["kind"] == "discovery" else [r["source_ref"] for r in scoop["regions"]]
        scoop["estimated_passes"] = None if scoop["kind"] == "discovery" else _estimate_passes(scoop, cap)
        scoop["regions"] = [{k: r.get(k) for k in ("source_ref", "label", "status", "volume_bytes", "defensibility_class")}
                            for r in scoop["regions"]]
        scoop["state"] = "queued"
    return scoops


def _estimate_passes(scoop, cap):
    seconds = 0.0
    for region in scoop["regions"]:
        if region.get("kind") == "object_store":
            units = region.get("object_count") or 0
            rate = cap["obs_objects_per_sec"]
        else:
            units = region.get("directories_pending") or 0
            rate = cap["nas_dirs_per_sec"]
        seconds += units / max(rate, 1.0)
    return max(1, math.ceil(seconds / cap["pass_seconds"])) if seconds else 1


def _ledger(plan, stage, decision, reason, stamp_audit=None):
    row = LedgerRow.new(run_id=plan["northena_run_id"], trace_id=plan["northena_trace_id"], stage=stage,
                        decision=decision, reason=reason, artifact_ref=LedgerArtifactRef(**plan["governing_artifact_ref"]),
                        lawful_basis_ref=plan["lawful_basis_ref"], stamp_audit=stamp_audit)
    _run(ledger_record(row))
    plan.setdefault("ledger_rows", []).append({"row_id": row.row_id, "stage": stage, "decision": decision, "reason": reason})
    return row


def _critic(plan_id, run_id):
    from contracts.solva_reasoning import CriticInvocation
    from services.solva_v2.critic_seam import invoke_critic
    findings = invoke_critic(CriticInvocation(
        artefact=plan_id, canon="Doc 05 §B5.1; Targeta §17 #8; harvest recursion: census applies at every scale",
        authorising_instrument=run_id,
        rubric="Does the scoop order consume the admitted estate fully, one bounded pass per scoop, without a second ranking?"))
    return findings.model_dump(mode="json")


def _cif_propose(plan, kind_note, payload, citations):
    """CIF authors; the deterministic acceptance point decides; routing is a
    mechanical consequence of that verdict (BR-9.2, AC-18)."""
    from services.cif.detection import author_proposal
    from services.cif.acceptance_point import is_accepted
    from services.cif.output_routing import RoutingRefused, route_accepted_proposal
    proposal_id = "cif_" + hashlib.sha256(json.dumps([plan["plan_id"], kind_note, payload], sort_keys=True, default=str)
                                          .encode()).hexdigest()[:16]
    proposal = author_proposal(proposal_id=proposal_id, proposed_at=_now(), kind="research_loop_item",
                               payload=json.dumps({"note": kind_note, **payload}, default=str), citations=tuple(citations))
    accepted = is_accepted(proposal)
    routed = None
    if accepted:
        try:
            routed = route_accepted_proposal(proposal, accepted)
        except RoutingRefused as exc:
            routed = f"refused:{exc}"
    plan.setdefault("cif_proposals", []).append({"proposal_id": proposal_id, "note": kind_note, "accepted": accepted,
                                                 "routed": routed, "citations": list(citations), "at": _now()})


def originate(tenant, principal_id, lawful_ref, worker_id=None, target_bytes=None, objective_shape=None):
    """Admit → rank → cut → gate. Returns the saved shovel plan (scoop 0 not yet commissioned)."""
    if tenant not in SOURCE_TENANTS.values():
        raise ValueError("Unknown tenant for census planning.")
    target = int(target_bytes or os.environ.get("CENSUS_SCOOP_TARGET_BYTES", TIB))
    sources = sources_for(tenant)
    shape = objective_shape or " ".join(sources)
    rows, consumed = registry_rows(tenant)
    snapshot = _snapshot_ref(rows, consumed)
    admission = _run(northena_admit.compile_and_freeze({
        "artifact_type": "objective_request", "artifact_id": f"census-shovel:{tenant}", "artifact_version": snapshot,
        "lawful_basis": str(lawful_ref), "scope": sources, "defensibility_floor": FLOOR.value,
        "objective": "Consume the admitted estate fully in ordered scoops, one bounded pass at a time.",
        "tenant_id": tenant, "principal_id": principal_id, "worker_id": worker_id, "scoop_target_bytes": target,
        "objective_shape": shape}))
    if admission["decision"] != "admitted":
        return {"plan_id": None, "tenant_id": tenant, "state": "refused", "reason": admission["reason"],
                "northena_run_id": admission["run_id"], "ledger_rows": [admission["ledger_row"]["row_id"]]}
    frozen = northena_admit.FrozenArtifact(admission["frozen_artifact"])
    artifact_ref = frozen.artifact_ref()
    eligible = targeta_core.eligible_and_rank(rows, FLOOR, shape)
    ordered, yield_version = targeta_gate.compose_ordering(eligible, thresholds=None)
    mining = targeta_plan.build_plan(ordered=ordered, core_baseline=eligible, floor=FLOOR, mode="per_run",
                                     governing_artifact_ref=artifact_ref, registry_snapshot_ref=snapshot,
                                     yield_layer_version=yield_version)
    _run(targeta_plan.persist(mining))
    scoops = _cut_scoops(mining.ordered_targets, rows, target)
    plan = {"plan_id": mining.plan_id, "tenant_id": tenant, "principal_id": principal_id, "state": "active",
            "worker_id": worker_id or os.environ["CENSUS_PRIMARY_WORKER"], "target_bytes": target,
            "objective_shape": shape, "created_at": store.now(), "capacity": _capacity(),
            "northena_run_id": admission["run_id"], "northena_trace_id": admission["trace_id"],
            "governing_artifact_ref": artifact_ref.model_dump(mode="json"), "lawful_basis_ref": str(lawful_ref),
            "ledger_rows": [{"row_id": admission["ledger_row"]["row_id"], "stage": "admit", "decision": "admitted", "reason": "admitted"}],
            "mining_plan": mining.model_dump(mode="json"), "registry_snapshot_ref": snapshot,
            "targets_pending": len(rows), "regions_consumed": len(consumed),
            "estate_measured_bytes": sum(r["volume_bytes"] for r in rows), "scoop_count": len(scoops),
            "cadence": _cadence(scoops, target), "scoops": scoops, "cif_proposals": []}
    plan["solva_critic"] = _critic(mining.plan_id, admission["run_id"])
    if not scoops:
        _ledger(plan, "gate", "refused", "no_pending_targets:estate_consumed")
        _ledger(plan, "converge", "terminate_success", f"census_estate_consumed:regions={len(consumed)}")
        plan["state"] = "terminated"
    else:
        _ledger(plan, "gate", "warm", f"targeta_plan_built:{mining.plan_id}",
                {"scoops": len(scoops), "targets": len(rows), "yield_layer_version": yield_version,
                 "solva_critic": plan["solva_critic"]})
        for scoop in scoops:
            if scoop["oversized"]:
                region = scoop["regions"][0]
                _cif_propose(plan, "region_exceeds_one_scoop",
                             {"source_ref": region["source_ref"], "label": region["label"], "volume_bytes": region["volume_bytes"],
                              "scoop_target_bytes": target, "idea": "split this region into sub-regions so one scoop is one pass"},
                             [region["source_ref"], plan["ledger_rows"][-1]["row_id"]])
    save_plan(plan)
    return plan


def _cadence(scoops, target):
    cap = _capacity()
    sized = [s for s in scoops if s["kind"] != "discovery"]
    passes = sum(s.get("estimated_passes") or 0 for s in sized)
    return {"scoop_target": f"{target / TIB:.2f} TiB per scoop, one at a time",
            "discovery_scoops": len(scoops) - len(sized), "sized_scoops": len(sized),
            "oversized_scoops": sum(1 for s in sized if s["oversized"]), "estimated_total_passes": passes,
            "estimated_wall_hours_at_current_capacity": round(passes * cap["pass_seconds"] / max(cap["concurrent_workers"], 1) / 3600.0, 1),
            "principle": "Shovel: Targeta orders, complete one scoop, bank it, move to the next; resumable enumeration walks any scoop larger than one pass."}


def _plan_path(tenant, plan_id):
    return store.cursor_dir() / f"scoopplan-{tenant}-{plan_id}.json"


def save_plan(plan):
    path = _plan_path(plan["tenant_id"], plan["plan_id"])
    path.write_text(json.dumps(plan, indent=2, default=str))
    return path


def load_plan(tenant, plan_id):
    try:
        return json.loads(_plan_path(tenant, plan_id).read_text())
    except (OSError, ValueError):
        return None


def active_plan(tenant):
    plans = []
    for path in store.cursor_dir().glob(f"scoopplan-{tenant}-*.json"):
        try:
            plans.append(json.loads(path.read_text()))
        except (OSError, ValueError):
            continue
    live = [p for p in plans if p.get("state") == "active"]
    return reconcile(max(live, key=lambda p: p.get("created_at", ""))) if live else None


def reconcile(plan):
    """Self-heal: a commissioned scoop whose run (or its continuation chain) already
    ended without advancing the plan (e.g. scheduler restart) is advanced now."""
    for scoop in plan["scoops"]:
        if scoop.get("state") != "commissioned" or not scoop.get("census_run_id"):
            continue
        row = store.get(scoop["census_run_id"], plan["tenant_id"])
        while row and row.get("continuation_run_id"):
            row = store.get(row["continuation_run_id"], plan["tenant_id"])
        if row and row.get("status") != "PENDING":
            advance_plan(row)
            return load_plan(plan["tenant_id"], plan["plan_id"]) or plan
    return plan


def _inflight_for(scoop, tenant):
    """An unowned PENDING run already doing exactly this scoop's work (reuse, not duplicate)."""
    refs = scoop["source_refs"] or None
    for row in store.runs(tenant):
        if (row.get("status") == "PENDING" and row.get("source_ids") == [scoop["source_id"]]
                and (row.get("source_refs") or None) == refs and not row.get("scoop_plan_id")):
            return row
    return None


def _tag(plan, index, row, adopted=False):
    row.update(scoop_plan_id=plan["plan_id"], scoop_index=index, northena_run_id=plan["northena_run_id"])
    store.save(row)
    plan["scoops"][index].update(state="commissioned", census_run_id=row["census_run_id"], adopted_inflight=adopted)
    save_plan(plan)
    return row


def commission_scoop(plan, index, principal_id, lawful_ref):
    """Commission one scoop as a tenant census on the external worker, tagged with its
    plan position; an in-flight run over the same scope is adopted instead of duplicated."""
    scoop = plan["scoops"][index]
    inflight = _inflight_for(scoop, plan["tenant_id"])
    if inflight:
        return _tag(plan, index, inflight, adopted=True), False
    key = f"{plan['plan_id']}-scoop{index:03d}"
    row, fresh = store.enqueue(plan["tenant_id"], principal_id, [scoop["source_id"]], key, lawful_ref,
                               plan["worker_id"], scoop["source_refs"])
    return _tag(plan, index, row), fresh


def _progress(current):
    total = 0
    for outcome in current.get("outcomes", []):
        for s in outcome.get("sources", []):
            total += (s.get("file_count") or 0) + (s.get("object_count") or 0) + (s.get("table_count") or 0)
    return total


def _already_running(current):
    return any(o.get("reason_code") == "ENUMERATION_ALREADY_RUNNING" for o in current.get("outcomes", []))


def advance_plan(current):
    """After a scoop's pass finishes without self-continuation: bank it in Northena's
    ledger, let CIF propose on starvation, commission the next scoop, and terminate
    the plan (success, or budget when nothing progressed) when the order is walked."""
    plan_id = current.get("scoop_plan_id")
    if plan_id is None or current.get("continuation_run_id"):
        return None
    with store.lock(f"shovel:{plan_id}"):
        plan = load_plan(current["tenant_id"], plan_id)
        if not plan or plan.get("state") != "active":
            return None
        index = current.get("scoop_index") or 0
        scoop = plan["scoops"][index]
        if scoop.get("state") != "commissioned" or scoop.get("census_run_id") != current["census_run_id"]:
            return None
        return _advance(plan, index, current)


def _advance(plan, index, current):
    scoop = plan["scoops"][index]
    if _already_running(current):
        inflight = _inflight_for(scoop, plan["tenant_id"])
        if inflight:
            return _tag(plan, index, inflight, adopted=True)["census_run_id"]
    halt = current.get("scope_halt")
    progress = _progress(current)
    scoop.update(state="halted" if halt else "banked", status=current.get("status"), progress_units=progress,
                 census_run_id=current["census_run_id"], proof_ref=current.get("proof_ref"),
                 reason_codes=sorted({o.get("reason_code") for o in current.get("outcomes", []) if o.get("reason_code")}))
    if halt:
        _ledger(plan, "converge", "continue", f"scoop_{index:03d}_halted:{halt['reason']}", {"scope_halt": halt})
        _cif_propose(plan, "scope_starved_flatline",
                     {"scoop_index": index, "source_id": scoop["source_id"], "source_refs": scoop["source_refs"],
                      "census_run_id": current["census_run_id"], "halt": halt,
                      "idea": "re-examine mount/session ceiling or narrow the scope before re-scooping"},
                     [current["census_run_id"], current.get("proof_ref") or plan["ledger_rows"][-1]["row_id"]])
    else:
        _ledger(plan, "converge", "continue", f"scoop_{index:03d}_banked:{current.get('status')}:units={progress}")
    nxt = index + 1
    if nxt < len(plan["scoops"]):
        save_plan(plan)
        row, _ = commission_scoop(plan, nxt, plan["principal_id"], plan["lawful_basis_ref"])
        return row["census_run_id"]
    progressed = any(s.get("progress_units") for s in plan["scoops"])
    plan["state"] = "terminated"
    if progressed:
        _ledger(plan, "converge", "terminate_success", f"shovel_walked:scoops={len(plan['scoops'])}")
    else:
        _ledger(plan, "converge", "terminate_budget", "no_progress_signal:owner_dependency_banked")
    save_plan(plan)
    if progressed:
        return originate_successor(plan)
    return None


def originate_successor(plan):
    """A walked plan that made progress re-plans what still remains (living artifact).
    An unchanged Registry snapshot means nothing new to shovel: no successor."""
    from services.census_autonomy.operational_runner import admission_path
    rows, consumed = registry_rows(plan["tenant_id"])
    if not rows or _snapshot_ref(rows, consumed) == plan["registry_snapshot_ref"]:
        return None
    path, _ = admission_path()
    successor = originate(plan["tenant_id"], plan["principal_id"], str(path), plan["worker_id"], plan["target_bytes"],
                          plan.get("objective_shape"))
    plan["successor_plan_id"] = successor.get("plan_id")
    save_plan(plan)
    if successor.get("state") == "active" and successor["scoops"]:
        row, _ = commission_scoop(successor, 0, plan["principal_id"], str(path))
        return row["census_run_id"]
    return None
