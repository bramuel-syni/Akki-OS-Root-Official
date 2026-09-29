"""The Watch at the commission gates — the first REAL protected boundaries (roadmap M2.1/M2.2).

Not a sibling engine (AIP §1.2): every crossing of an admitted commission gate is OBSERVED into an
append-only per-tenant feed; deterministic detectors read that feed and mint MachoVerdicts through
the existing `services.watch.macho` seam; Mkono maps them through the existing deterministic ladder
(`services.watch.mkono`); and the gate itself is the EFFECTOR — a `contain` action suspends the
subject's commissioning capability until its TTL, a `shape` action throttles it — writing an
`effect` receipt every time it bites (a persisted action is not proof of effect; a receipt is).
Expired containments reconcile once (`release` row, `expired_clean`). Every threshold is a seam
DEFAULT pending owner ruling and is named on the verdict's evidence_ref. Detectors here are
externally steerable by construction: they can never reach `sever`.
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
    "census.commission": "POST /api/portal/census/run",
    "census.plan": "POST /api/portal/census/plan",
    "language_cognition.commission": "POST /api/portal/census/language-cognition/jobs",
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


class GateUnobservable(RuntimeError):
    """R-26 posture applied to commission gates: a crossing that cannot be observed does not happen."""


def _param(spec):
    return int(os.environ.get(spec[0], spec[1]))


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


def active_effects(tenant_id, principal_id, now=None):
    """Live Mkono state for a subject read from the record: active containments (issued_at+ttl) and
    shape windows. Expired containments are reconciled here, once, as `release` rows (Canon 8 §18)."""
    now = now or _now()
    all_rows = rows(tenant_id)
    released = {r["action_ref"] for r in all_rows if r["kind"] == "release"}
    contain, shape = [], []
    for row in all_rows:
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
            elif action.action_id not in released:
                _append(tenant_id, {"kind": "release", "at": _iso(now), "tenant_id": tenant_id, "principal_id": principal_id,
                                    "action_ref": action.action_id, "outcome": "expired_clean", "expired_at": _iso(expires),
                                    "reconciled_by": RESPONDER,
                                    "period_summary": "Commissioning suspended for the TTL; reads unaffected; released at expiry without extension."})
                released.add(action.action_id)
        elif action.action_class == "shape" and now < issued + timedelta(seconds=_param(SHAPE_WINDOW)):
            shape.append({"action_id": action.action_id, "verdict_id": action.verdict_ref, "until": _iso(issued + timedelta(seconds=_param(SHAPE_WINDOW)))})
    return {"contain": contain, "shape": shape}


def _enforce(actor, boundary, now):
    """The gate is the effector. contain → commissioning suspended (reads intact); shape → friction:
    the subject's commission attempts (admitted or refused) are spaced by SHAPE_MIN_INTERVAL."""
    tenant, principal = actor["tenant_id"], actor["principal_id"]
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
    """Macho reads the feed; Mkono maps; nothing here can reach sever (externally steerable by grammar)."""
    from services.watch.macho import MachoVerdict, mint_macho_verdict
    from services.watch.mkono import map_verdict_to_action, persist_action
    tenant, principal = actor["tenant_id"], actor["principal_id"]
    all_rows = rows(tenant)
    mine = [r for r in all_rows if r["principal_id"] == principal]
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
                    f"&threshold={_param(spec['count'])}&window_s={_param(spec['window_s'])}&thresholds=DEFAULT_PENDING_OWNER_RULING")
        try:
            verdict = mint_macho_verdict(MachoVerdict(verdict_id=verdict_id, verdict_class="externally_steerable",
                                                      subject_ref=subject_ref(principal), evidence_ref=evidence,
                                                      asserted_at=_iso(now), intensity=spec["intensity"]))
            action = persist_action(map_verdict_to_action(verdict, action_id=action_id, issued_at=_iso(now)))
        except (ValueError, RuntimeError) as exc:
            _append(tenant, {"kind": "detection_error", "at": _iso(now), "tenant_id": tenant, "principal_id": principal,
                             "detector": name, "error": f"{type(exc).__name__}: {str(exc)[:200]}"})
            continue
        _append(tenant, {"kind": "detection", "at": _iso(now), "tenant_id": tenant, "principal_id": principal, "detector": name,
                         "boundary": boundary, "verdict_id": verdict.verdict_id, "action_id": action.action_id,
                         "action_class": action.action_class, "ttl_seconds": action.ttl_seconds, "evidence_ref": evidence})


def observe(actor, boundary, outcome, status, digest, now=None):
    now = now or _now()
    _append(actor["tenant_id"], {"kind": "crossing", "at": _iso(now), "tenant_id": actor["tenant_id"], "principal_id": actor["principal_id"],
                                 "boundary": boundary, "outcome": outcome, "status": status, "digest": digest})
    _detect(actor, boundary, digest, now)


@contextmanager
def crossing(actor, boundary, body):
    """Wrap one admitted-gate handler: enforce live Mkono state first, then observe the outcome
    (admitted or the handler's own refusal) into the feed before the response leaves."""
    if boundary not in PROTECTED_BOUNDARIES:
        raise ValueError(f"unknown protected boundary {boundary!r}")
    digest = hashlib.sha256(json.dumps(body or {}, sort_keys=True, default=str).encode()).hexdigest()
    now = _now()
    try:
        _enforce(actor, boundary, now)
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
    """Ownership evidence for the console: gate detections bind verdict/action ids to the tenant,
    effect receipts prove the effector ran, release rows prove the honest expiry."""
    all_rows = rows(tenant_id)
    detections = [r for r in all_rows if r["kind"] == "detection"]
    effects, releases = {}, {}
    for r in all_rows:
        if r["kind"] == "effect":
            effects.setdefault(r["action_ref"], []).append(r)
        elif r["kind"] == "release":
            releases[r["action_ref"]] = r
    return {"verdict_ids": {d["verdict_id"]: d for d in detections}, "action_ids": {d["action_id"]: d for d in detections},
            "effects": effects, "releases": releases,
            "counts": {"crossings": sum(1 for r in all_rows if r["kind"] == "crossing"),
                       "refusals": sum(1 for r in all_rows if r["kind"] == "crossing" and r["outcome"] == "refused"),
                       "detections": len(detections), "effects": sum(len(v) for v in effects.values()), "releases": len(releases)}}


def boundary_register():
    return [{"boundary": k, "route": v, "observed": True, "effector": "gate (contain → suspend commissioning · shape → throttle)"}
            for k, v in PROTECTED_BOUNDARIES.items()]
