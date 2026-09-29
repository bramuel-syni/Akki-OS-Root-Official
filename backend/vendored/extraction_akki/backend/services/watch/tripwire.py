"""Tripwires at the commission gates (Canon 8 §11 'Sarabi degrades into a tripwire, never a hole';
§12 mirage isolation; §10 the mark).

Mkono plants a decoy descriptor one-way (only its hash is on record — §32.4 construction hidden).
An actor who presents that descriptor at a protected gate has touched what no legitimate path
advertises: a `mirage_incrimination` signal from the closed six-member registry, a
structural-certainty verdict, a `sever` that holds rather than expires, and a mark binding every
dimension the gate can observe. The mirage store is measured disjoint from every production
store before a decoy is planted; the measurement is recorded, not asserted."""
import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

PLANTER = "mkono.commission_gate.tripwire"


def _iso(dt):
    return dt.isoformat().replace("+00:00", "Z")


def _parse(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def _hash(text):
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _production_dirs():
    from services.watch import commission_gate, mark, persistence, sever_signals
    from services.watch.mirage import _m_dir, _t_dir
    return {"observations": commission_gate._dir(), "verdicts": persistence._verdicts_dir(), "actions": persistence._actions_dir(),
            "sever_signals": sever_signals._dir(), "marks": mark._dir(), "mirages": _m_dir(), "mirage_touches": _t_dir()}


def isolation_check():
    """Measured: the isolated mirage store shares no path with any production Watch store."""
    from services.watch.mirage_artifacts import _dir as mirage_dir, _is_same_or_subpath
    target = Path(mirage_dir()).resolve()
    overlaps = [name for name, path in _production_dirs().items()
                if _is_same_or_subpath(target, Path(path).resolve()) or _is_same_or_subpath(Path(path).resolve(), target)]
    return {"passed": not overlaps, "overlaps": overlaps, "stores_compared": len(_production_dirs()), "mirage_store": str(target)}


def plant(tenant_id, decoy_ref, ttl_seconds, planted_by_principal, now=None):
    from services.watch import commission_gate
    from services.watch.mirage import plant_mirage
    from services.watch.mirage_artifacts import write_mirage_artifact
    now = now or datetime.now(timezone.utc)
    check = isolation_check()
    if not check["passed"]:
        raise RuntimeError(f"Mirage store overlaps production stores {check['overlaps']}; nothing was planted.")
    mirage_id = f"mr_gate_{uuid.uuid4().hex[:12]}"
    mirage = plant_mirage({"mirage_id": mirage_id, "planted_at": _iso(now), "expires_at": _iso(now + timedelta(seconds=int(ttl_seconds))),
                           "mirage_class": "decoy_artefact", "planted_by": PLANTER, "opaque_ref": _hash(decoy_ref),
                           "planting_note": "Decoy source descriptor for the commission gates; presenting it is a structural finding. Placement not recorded here."})
    write_mirage_artifact({"artifact_id": f"mir_{mirage_id}", "mirage_session_id": mirage_id, "is_synthetic": True,
                           "synthetic_provenance": f"tripwire:{mirage_id}:planted_by:{PLANTER}", "production_store_leak_check": "passed",
                           "outward_lie_only": True, "created_at": _iso(now)})
    commission_gate._append(tenant_id, {"kind": "mirage_planted", "at": _iso(now), "tenant_id": tenant_id, "principal_id": planted_by_principal,
                                        "mirage_id": mirage_id, "expires_at": mirage.expires_at, "isolation_check": check})
    return {"mirage_id": mirage_id, "expires_at": mirage.expires_at, "isolation_check": check}


def _candidates(body):
    out = []
    for key, value in (body or {}).items():
        if isinstance(value, str):
            out.append(value)
        elif isinstance(value, list):
            out.extend(v for v in value if isinstance(v, str))
        elif isinstance(value, dict):
            out.extend(v for v in value.values() if isinstance(v, str))
    return out


def touched(tenant_id, body, now=None):
    from services.watch import commission_gate
    from services.watch.mirage import load_mirages
    now = now or datetime.now(timezone.utc)
    planted = {r["mirage_id"] for r in commission_gate.rows(tenant_id) if r["kind"] == "mirage_planted"}
    live = {m.opaque_ref: m for m in load_mirages() if m.mirage_id in planted and _parse(m.expires_at) > now}
    for candidate in _candidates(body):
        hit = live.get(_hash(candidate))
        if hit:
            return hit
    return None


def convict(actor, boundary, digest, mirage, now):
    """Touch → signal → structural verdict → sever → mark → witness → record → decision → notice."""
    from contracts.sever_certainty_signal_v0 import SeverCertaintySignalV0
    from services.watch import commission_gate, decisions, notices, witness_binding
    from services.watch.macho import MachoVerdict, mint_macho_verdict
    from services.watch.mark import mint_mark
    from services.watch.mirage import record_touch
    from services.watch.mkono import map_verdict_to_action, persist_action
    from services.watch.sever_signals import append_sever_signal
    tenant, principal = actor["tenant_id"], actor["principal_id"]
    subject = commission_gate.subject_ref(principal)
    tag = uuid.uuid4().hex[:12]
    touch = record_touch({"touch_id": f"mt_gate_{tag}", "mirage_id": mirage.mirage_id, "touched_at": _iso(now), "actor_ref": subject,
                          "touch_kind": "guilty_use", "evidence_note": f"Decoy descriptor presented at {boundary}; crossing digest sha256:{digest[:16]}."})
    signal = append_sever_signal(SeverCertaintySignalV0(signal_id=f"sig_mirage_{tag}", signal_kind="mirage_incrimination", asserted_by=PLANTER,
                                                        asserted_at=_iso(now), evidence_ref=f"mirage_touch:{touch.touch_id}"))
    verdict = mint_macho_verdict(MachoVerdict(verdict_id=f"mv_gate_{tag}", verdict_class="structural_certainty", subject_ref=subject,
                                              evidence_ref=f"sever_signal:{signal.signal_id}", asserted_at=_iso(now),
                                              sever_certainty_signal_id=signal.signal_id))
    action = persist_action(map_verdict_to_action(verdict, action_id=f"ma_gate_{tag}", issued_at=_iso(now)))
    recent = [r["digest"] for r in commission_gate.rows(tenant) if r["kind"] == "crossing" and r["principal_id"] == principal][-8:]
    mark = mint_mark(mark_id=f"mark_gate_{tag}", verdict_ref=verdict.verdict_id, action_ref=action.action_id, identity=subject,
                     credentials=actor.get("session_ref") or "unresolved", session_id=actor.get("session_ref") or "unresolved",
                     device_fingerprint=actor.get("device_ref") or "unresolved",
                     behavioural_signature=_hash(json.dumps(recent + [digest])), content_hashes=[f"sha256:{digest}", mirage.opaque_ref],
                     minted_at=_iso(now))
    witness = None
    try:
        witness = witness_binding.attest_action(action.action_id, now).attestation_id
    except (ValueError, OSError) as exc:
        commission_gate._append(tenant, {"kind": "witness_gap", "at": _iso(now), "tenant_id": tenant, "action_ref": action.action_id, "error": str(exc)[:200]})
    commission_gate._append(tenant, {"kind": "detection", "at": _iso(now), "tenant_id": tenant, "principal_id": principal, "detector": "mirage_incrimination",
                                     "boundary": boundary, "verdict_id": verdict.verdict_id, "action_id": action.action_id, "action_class": "sever",
                                     "ttl_seconds": None, "mark_id": mark.mark_id, "touch_id": touch.touch_id, "signal_id": signal.signal_id,
                                     "witness_attestation": witness, "evidence_ref": verdict.evidence_ref})
    commission_gate._append(tenant, {"kind": "effect", "at": _iso(now), "tenant_id": tenant, "principal_id": principal, "boundary": boundary,
                                     "effect": "refused_by_sever", "action_ref": action.action_id})
    decisions.open_decision(tenant, "demark_release", subject, {"action_ref": action.action_id, "mark_ref": mark.mark_id, "verdict_ref": verdict.verdict_id},
                            "mkono.commission_gate", f"Severed on structural certainty · {subject}", now)
    notices.send(tenant, principal, "sever", "The Watch has severed your commissioning capability. It holds rather than expires; "
                 "restoration requires a dual-control decision by your estate's operators. Reading your estate's records is unaffected.",
                 {"action_ref": action.action_id}, now)
    return action
