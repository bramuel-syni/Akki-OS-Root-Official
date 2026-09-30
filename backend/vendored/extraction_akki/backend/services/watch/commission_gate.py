"""The Watch at the commission gates — the REAL protected boundaries (roadmap M2.1/M2.2).

Not a sibling engine (AIP §1.2): every crossing of an admitted commission gate is OBSERVED into an
append-only per-tenant feed; deterministic detectors read that feed and mint MachoVerdicts through
the existing `services.watch.macho` seam; Mkono maps them through the existing deterministic ladder
(`services.watch.mkono`); and the gate itself is the EFFECTOR — `contain` suspends the subject's
commissioning until its TTL, `shape` throttles it, `sever` (structural certainty only, via the
tripwire) holds until a dual-control release — writing an `effect` receipt every time it bites
(a persisted action is not proof of effect; a receipt is). Mark state is evaluated on every pass.
Expired containments reconcile once (`release` row + notice). Thresholds are seam DEFAULTS until a
ratified requirements version exists; every verdict names the version it was minted under.
Gate detectors are externally steerable by construction: they can never reach `sever`.
"""
import hashlib
import json
import os
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import HTTPException

PROTECTED_BOUNDARIES = {
    "training_lab.assessment": "POST /api/training/lab/runs",
    "training_lab.watch": "PUT /api/training/lab/watch",
    "census.commission": "POST /api/portal/census/run",
    "census.plan": "POST /api/portal/census/plan",
    "language_cognition.commission": "POST /api/portal/census/language-cognition/jobs",
    "language_cognition.cancel": "POST /api/portal/census/language-cognition/jobs/{job_id}/cancel",
    "estate_intelligence.commission": "POST /api/portal/census/estate-intelligence/jobs",
    "estate_intelligence.cancel": "POST /api/portal/census/estate-intelligence/jobs/{job_id}/cancel",
    "m9_training.commission": "POST /api/training/m9/jobs",
    "m9_training.cancel": "POST /api/training/m9/jobs/{job_id}/cancel",
    # M8/M9 completion (owner rulings 2026-09-30): admission re-adjudication, governed serving, interruption drills, rights withdrawal, continuity drills.
    "m9_training.readjudicate": "POST /api/training/m9/certificates/{job_id}/readjudicate",
    "m9_training.interrupt": "POST /api/training/m9/jobs/{job_id}/interrupt",
    "m9_training.drill_receipt": "POST /api/training/m9/drills/interruption",
    "m9_training.revoke_unit": "POST /api/training/m9/rights/revoke-unit",
    "m9_serving.start": "POST /api/training/m9/serving/{model_id}/start",
    "m9_serving.withdraw": "POST /api/training/m9/serving/{model_id}/withdraw",
    "m9_serving.stop": "POST /api/training/m9/serving/{model_id}/stop",
    "m9_serving.load_test": "POST /api/training/m9/serving/{model_id}/load-test",
    "continuity.ledger_archive": "POST /api/continuity/ledger/archive",
    "continuity.ledger_restore_drill": "POST /api/continuity/ledger/restore-drill",
    # M3 · a request becomes completed, delivered work: three more commission gates on the same inventory.
    "dap.commission": "POST /api/portal/commission/drafts/{draft_id}/freeze",
    "dap.approval": "POST /api/portal/approvals/{request_id}/decide",
    "dap.delivery": "POST /api/portal/requests/{request_id}/deliveries/{delivery_id}/retrieve",
}
DETECTORS = {
    "fast_violation": {"count": ("WATCH_GATE_FAST_REFUSALS", 3), "window_s": ("WATCH_GATE_FAST_WINDOW_S", 60),
                       "outcome": "refused", "intensity": "elevated"},
    "slow_play": {"count": ("WATCH_GATE_SLOW_REFUSALS", 8), "window_s": ("WATCH_GATE_SLOW_WINDOW_S", 86400),
                  "outcome": "refused", "intensity": "severe"},
    "permitted_but_misused": {"count": ("WATCH_GATE_DUPLICATE_ADMITS", 3), "window_s": ("WATCH_GATE_DUPLICATE_WINDOW_S", 600),
                              "outcome": "admitted", "same_digest": True, "intensity": "noted"},
}
SHAPE_WINDOW = ("WATCH_GATE_SHAPE_WINDOW_S", 600)
SHAPE_MIN_INTERVAL = ("WATCH_GATE_SHAPE_MIN_INTERVAL_S", 30)
RESPONDER = "mkono.commission_gate"
SEVER_MESSAGE = ("Your commissioning capability is severed by the Watch (action {action}). It holds rather than expires; "
                 "restoration requires a dual-control decision by your estate's operators. Reading your estate's records is unaffected.")


class GateUnobservable(RuntimeError):
    """R-26 posture applied to commission gates: a crossing that cannot be observed does not happen."""


def _param(spec):
    from services.watch import learning_loop
    ratified = learning_loop.ratified_value(spec[0])
    return int(ratified if ratified is not None else os.environ.get(spec[0], spec[1]))


def _dir():
    return Path(os.environ.get("WATCH_OBSERVATIONS_DIR", "/app/assessment_workspace/phase0/watch_observations"))


def _now():
    return datetime.now(timezone.utc)


def _iso(dt):
    return dt.isoformat().replace("+00:00", "Z")


def _parse(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def rows(tenant_id):
    path = _dir() / f"{tenant_id}.jsonl"
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def _append(tenant_id, row):
    try:
        _dir().mkdir(parents=True, exist_ok=True)
        with (_dir() / f"{tenant_id}.jsonl").open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, sort_keys=True) + "\n")
    except OSError as exc:
        raise GateUnobservable(f"observation_write_failed — {type(exc).__name__}") from exc


def subject_ref(principal_id):
    return f"principal:{principal_id}"


def _action(action_id):
    from services.watch.persistence import get_action
    return get_action(action_id)


def receipt_console(actor, surface="watch.state"):
    """Canon 8 §13: the console is watched — its sessions receipted. Not a detector input."""
    _append(actor["tenant_id"], {"kind": "console", "at": _iso(_now()), "tenant_id": actor["tenant_id"],
                                 "principal_id": actor["principal_id"], "surface": surface})


def reconcile_expired(tenant_id, now=None):
    """Every expired containment is released once (Canon 8 §18 auto-release integrity) and the
    subject is told what did not land (notify posture). Runs on every read and every crossing."""
    from services.watch import notices
    now = now or _now()
    all_rows = rows(tenant_id)
    released = {r["action_ref"] for r in all_rows if r["kind"] == "release"}
    out = []
    for row in all_rows:
        if row["kind"] != "detection" or row.get("action_class") != "contain" or row["action_id"] in released:
            continue
        action = _action(row["action_id"])
        if action is None:
            continue
        expires = _parse(action.issued_at) + timedelta(seconds=action.ttl_seconds)
        if now < expires:
            continue
        refused = sum(1 for r in all_rows if r["kind"] == "effect" and r["action_ref"] == action.action_id)
        _append(tenant_id, {"kind": "release", "at": _iso(now), "tenant_id": tenant_id, "principal_id": row["principal_id"],
                            "action_ref": action.action_id, "outcome": "expired_clean", "expired_at": _iso(expires), "reconciled_by": RESPONDER,
                            "attempts_not_landed": refused, "reconciliation": "notify",
                            "period_summary": "Commissioning suspended for the TTL; reads unaffected; released at expiry without extension."})
        notices.send(tenant_id, row["principal_id"], "release",
                     f"Your commissioning capability was suspended by the Watch from {action.issued_at} until {_iso(expires)} and has been released. "
                     f"{refused} commission attempt(s) in that period did not land and were not replayed; resubmit any you still need.",
                     {"action_ref": action.action_id}, now)
        released.add(action.action_id)
        out.append(action.action_id)
    return out


def active_effects(tenant_id, principal_id, now=None):
    """Live Mkono state for a subject, read from the record: active containments and shape windows."""
    now = now or _now()
    reconcile_expired(tenant_id, now)
    contain, shape = [], []
    for row in rows(tenant_id):
        if row["kind"] != "detection" or row["principal_id"] != principal_id:
            continue
        action = _action(row["action_id"])
        if action is None:
            continue
        issued = _parse(action.issued_at)
        if action.action_class == "contain":
            expires = issued + timedelta(seconds=action.ttl_seconds)
            if now < expires:
                contain.append({"action_id": action.action_id, "verdict_id": action.verdict_ref, "expires_at": _iso(expires)})
        elif action.action_class == "shape" and now < issued + timedelta(seconds=_param(SHAPE_WINDOW)):
            shape.append({"action_id": action.action_id, "verdict_id": action.verdict_ref, "until": _iso(issued + timedelta(seconds=_param(SHAPE_WINDOW)))})
    return {"contain": contain, "shape": shape}


def sever_state(tenant_id, principal_id):
    """Mark state evaluated on every pass (Canon 8 §10): an unreleased sever or a live mark on the
    subject holds the gate. Release exists only as a dual-control `release` row."""
    from services.watch.mark import read_marks
    from services.watch.persistence import read_actions
    subject = subject_ref(principal_id)
    released = {r["action_ref"] for r in rows(tenant_id) if r["kind"] == "release" and r["outcome"] == "released_by_dual_control"}
    demarked = {r.get("mark_ref") for r in rows(tenant_id) if r["kind"] == "release" and r["outcome"] == "released_by_dual_control"}
    sever = next((a for a in read_actions() if a.action_class == "sever" and a.subject_ref == subject and a.action_id not in released), None)
    mark = next((m for m in read_marks() if m.identity == subject and m.mark_id not in demarked), None)
    if sever is None and mark is None:
        return None
    return {"action_id": sever.action_id if sever else mark.action_ref, "mark_id": mark.mark_id if mark else None}


def release_sever(tenant_id, subject, refs, approvers, now=None):
    """The distinct release authority for severance: two operators, one record, real restoration."""
    from services.watch import notices
    now = now or _now()
    principal = subject.split(":", 1)[-1]
    _append(tenant_id, {"kind": "release", "at": _iso(now), "tenant_id": tenant_id, "principal_id": principal, "action_ref": refs["action_ref"],
                        "mark_ref": refs.get("mark_ref"), "outcome": "released_by_dual_control", "released_by": approvers, "reconciled_by": "decisions.dual_control",
                        "period_summary": "Severance released by two distinct estate operators; the mark stays on record as history, de-marked by this entry."})
    notices.send(tenant_id, principal, "release", "Two estate operators have released the Watch's severance on your commissioning capability. "
                 "Attempts made while severed did not land and were not replayed.", {"action_ref": refs["action_ref"]}, now)
    return {"protection_changed": True, "released_action": refs["action_ref"], "demarked": refs.get("mark_ref")}


def _enforce(actor, boundary, now):
    """The gate is the effector. sever → held until dual-control release; contain → commissioning
    suspended (reads intact); shape → friction: attempts spaced by SHAPE_MIN_INTERVAL."""
    tenant, principal = actor["tenant_id"], actor["principal_id"]
    held = sever_state(tenant, principal)
    if held:
        _append(tenant, {"kind": "effect", "at": _iso(now), "tenant_id": tenant, "principal_id": principal, "boundary": boundary,
                         "effect": "refused_by_sever", "action_ref": held["action_id"]})
        raise HTTPException(403, SEVER_MESSAGE.format(action=held["action_id"]))
    live = active_effects(tenant, principal, now)
    if live["contain"]:
        c = live["contain"][0]
        _append(tenant, {"kind": "effect", "at": _iso(now), "tenant_id": tenant, "principal_id": principal, "boundary": boundary,
                         "effect": "refused_by_containment", "action_ref": c["action_id"]})
        raise HTTPException(409, f"Your commissioning capability is suspended by the Watch until {c['expires_at']} "
                                 f"(action {c['action_id']}). Reading your estate's records is unaffected.")
    if live["shape"]:
        recent = [r for r in rows(tenant) if r["kind"] == "crossing" and r["principal_id"] == principal
                  and _parse(r["at"]) > now - timedelta(seconds=_param(SHAPE_MIN_INTERVAL))]
        if recent:
            s = live["shape"][0]
            _append(tenant, {"kind": "effect", "at": _iso(now), "tenant_id": tenant, "principal_id": principal, "boundary": boundary,
                             "effect": "throttled_by_shape", "action_ref": s["action_id"]})
            raise HTTPException(429, f"The Watch is applying friction to your commissions until {s['until']} "
                                     f"(action {s['action_id']}): wait {_param(SHAPE_MIN_INTERVAL)} s between commissions.")


def _detect(actor, boundary, digest, now):
    """Macho reads the feed; Mkono maps; the witness attests the digest; nothing here can reach sever."""
    from services.watch import learning_loop, witness_binding
    from services.watch.macho import MachoVerdict, mint_macho_verdict
    from services.watch.mkono import map_verdict_to_action, persist_action
    tenant, principal = actor["tenant_id"], actor["principal_id"]
    all_rows = rows(tenant)
    mine = [r for r in all_rows if r.get("principal_id") == principal]
    for name, spec in DETECTORS.items():
        window_start = now - timedelta(seconds=_param(spec["window_s"]))
        hits = [r for r in mine if r["kind"] == "crossing" and r["outcome"] == spec["outcome"] and _parse(r["at"]) >= window_start
                and (not spec.get("same_digest") or (r["digest"] == digest and r["boundary"] == boundary))]
        if len(hits) < _param(spec["count"]):
            continue
        if any(r["kind"] == "detection" and r["detector"] == name and _parse(r["at"]) >= window_start for r in mine):
            continue  # one verdict per detector per window
        verdict_id, action_id = f"mv_gate_{uuid.uuid4().hex[:12]}", f"ma_gate_{uuid.uuid4().hex[:12]}"
        evidence = (f"watch_observations://{tenant}/{principal}?detector={name}&boundary={boundary}&count={len(hits)}"
                    f"&threshold={_param(spec['count'])}&window_s={_param(spec['window_s'])}&{learning_loop.label()}")
        try:
            verdict = mint_macho_verdict(MachoVerdict(verdict_id=verdict_id, verdict_class="externally_steerable",
                                                      subject_ref=subject_ref(principal), evidence_ref=evidence,
                                                      asserted_at=_iso(now), intensity=spec["intensity"]))
            action = persist_action(map_verdict_to_action(verdict, action_id=action_id, issued_at=_iso(now)))
        except (ValueError, RuntimeError) as exc:
            _append(tenant, {"kind": "detection_error", "at": _iso(now), "tenant_id": tenant, "principal_id": principal,
                             "detector": name, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
            continue
        witness = None
        try:
            witness = witness_binding.attest_action(action.action_id, now).attestation_id
        except (ValueError, OSError) as exc:
            _append(tenant, {"kind": "witness_gap", "at": _iso(now), "tenant_id": tenant, "action_ref": action.action_id, "error": str(exc)[:200]})
        prior_release = any(r["kind"] == "release" and r["principal_id"] == principal for r in all_rows)
        _append(tenant, {"kind": "detection", "at": _iso(now), "tenant_id": tenant, "principal_id": principal, "detector": name,
                         "boundary": boundary, "verdict_id": verdict.verdict_id, "action_id": action.action_id,
                         "action_class": action.action_class, "ttl_seconds": action.ttl_seconds, "evidence_ref": evidence,
                         "witness_attestation": witness, "requirements": learning_loop.label(),
                         **({"anomaly": "contain_release_contain"} if action.action_class == "contain" and prior_release else {})})


def observe(actor, boundary, outcome, status, digest, now=None):
    now = now or _now()
    _append(actor["tenant_id"], {"kind": "crossing", "at": _iso(now), "tenant_id": actor["tenant_id"], "principal_id": actor["principal_id"],
                                 "boundary": boundary, "outcome": outcome, "status": status, "digest": digest})
    _detect(actor, boundary, digest, now)


@contextmanager
def crossing(actor, boundary, body):
    """Wrap one admitted-gate handler: enforce live Mkono state first, evaluate the tripwire, then
    observe the outcome (admitted or the handler's own refusal) before the response leaves."""
    from services.watch import tripwire
    if boundary not in PROTECTED_BOUNDARIES:
        raise ValueError(f"unknown protected boundary {boundary!r}")
    digest = hashlib.sha256(json.dumps(body or {}, sort_keys=True, default=str).encode()).hexdigest()
    now = _now()
    try:
        _enforce(actor, boundary, now)
        hit = tripwire.touched(actor["tenant_id"], body, now)
        if hit is not None:
            observe(actor, boundary, "refused", 403, digest, now)
            try:
                action = tripwire.convict(actor, boundary, digest, hit, now)
            except (ValueError, RuntimeError) as exc:
                _append(actor["tenant_id"], {"kind": "detection_error", "at": _iso(now), "tenant_id": actor["tenant_id"], "principal_id": actor["principal_id"],
                                             "detector": "mirage_incrimination", "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
                raise HTTPException(503, "The Watch could not complete the conviction record; nothing was commissioned.") from exc
            raise HTTPException(403, SEVER_MESSAGE.format(action=action.action_id))
    except GateUnobservable as exc:
        raise HTTPException(503, "The Watch could not observe this crossing; nothing was commissioned.") from exc
    try:
        yield
    except HTTPException as exc:
        try:
            observe(actor, boundary, "refused", exc.status_code, digest, now)
        except GateUnobservable:
            pass  # the refusal stands; the unobservable write is itself the failure posture
        raise
    try:
        observe(actor, boundary, "admitted", 202, digest, now)
    except GateUnobservable as exc:
        raise HTTPException(503, "The commission was accepted but the Watch could not observe it; treat it as not landed.") from exc


def owned_records(tenant_id):
    """Ownership evidence for the console: gate detections bind verdict/action/mark ids to the tenant,
    effect receipts prove the effector ran, release rows prove the honest expiry or the dual-control release."""
    all_rows = rows(tenant_id)
    detections = [r for r in all_rows if r["kind"] == "detection"]
    effects, releases = {}, {}
    for r in all_rows:
        if r["kind"] == "effect":
            effects.setdefault(r["action_ref"], []).append(r)
        elif r["kind"] == "release":
            releases[r["action_ref"]] = r
    return {"verdict_ids": {d["verdict_id"]: d for d in detections}, "action_ids": {d["action_id"]: d for d in detections},
            "mark_ids": {d["mark_id"]: d for d in detections if d.get("mark_id")},
            "effects": effects, "releases": releases,
            "counts": {"crossings": sum(1 for r in all_rows if r["kind"] == "crossing"),
                       "admitted": sum(1 for r in all_rows if r["kind"] == "crossing" and r["outcome"] == "admitted"),
                       "refusals": sum(1 for r in all_rows if r["kind"] == "crossing" and r["outcome"] == "refused"),
                       "detections": len(detections), "effects": sum(len(v) for v in effects.values()), "releases": len(releases),
                       "console": sum(1 for r in all_rows if r["kind"] == "console"),
                       "exceptions": sum(1 for r in all_rows if r["kind"] in ("detection_error", "witness_gap"))}}


def boundary_register():
    return [{"boundary": k, "route": v, "observed": True, "mark_check": True,
             "effector": "gate (sever → hold until dual-control release · contain → suspend commissioning · shape → throttle)"}
            for k, v in PROTECTED_BOUNDARIES.items()]
