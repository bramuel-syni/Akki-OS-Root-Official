"""Projections for the four constitutional Watch panels (Canon 8 §13) from the same records.

Negative space is honoured: no thresholds, bands or trip points; no decoy placement; no profile
internals (marks are shown as subject + minted_at + standing, never their dimensions)."""
from datetime import datetime, timedelta, timezone

from services.watch import commission_gate, decisions, learning_loop, notices, witness_binding


def _parse(text):
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def _iso(dt):
    return dt.isoformat().replace("+00:00", "Z")


def tiles(rows, items, now):
    hour = now - timedelta(hours=1)
    crossings = [r for r in rows if r["kind"] == "crossing"]
    open_items = [d for d in items.values() if d["state"] == "open"]
    return {
        "waiting": {"value": len(open_items), "note": "Reserved decisions open on the panel", "lines": [d["title"] for d in open_items[:3]]},
        "actors": {"value": len({r["principal_id"] for r in crossings}), "note": "Distinct principals seen at the gates",
                   "lines": [f"{len({r['principal_id'] for r in rows if r['kind'] == 'detection'})} with a verdict on record"]},
        "sessions": {"value": len({r["principal_id"] for r in rows if r["kind"] == "console" and _parse(r["at"]) >= hour}),
                     "note": "Console sessions receipted in the last hour", "lines": [f"{sum(1 for r in rows if r['kind'] == 'console')} console reads receipted in total"]},
        "allowed": {"value": sum(1 for r in crossings if r["outcome"] == "admitted"), "note": "Crossings the gates admitted", "lines": []},
        "refused": {"value": sum(1 for r in crossings if r["outcome"] == "refused"), "note": "Crossings the handlers or the Watch refused",
                    "lines": [f"{sum(1 for r in rows if r['kind'] == 'effect')} refusals were Watch effects"]},
        "flagged": {"value": sum(1 for r in rows if r["kind"] == "detection"), "note": "Detector verdicts minted",
                    "lines": [f"{n}: {sum(1 for r in rows if r['kind'] == 'detection' and r['detector'] == n)}" for n in [*commission_gate.DETECTORS, "mirage_incrimination"]]},
        "checks": {"value": witness_binding.summary()["attestations"] + sum(1 for r in rows if r["kind"] == "break_in" and r.get("immutability_measurement") == "passed"),
                   "note": "Witness digest attestations and break-in tests that measured immutability", "lines": []},
        "exceptions": {"value": sum(1 for r in rows if r["kind"] in ("detection_error", "witness_gap")) + sum(1 for r in rows if r["kind"] == "break_in" and r.get("immutability_measurement") != "passed") + witness_binding.summary()["tamper_alarms"],
                       "note": "Record, witness or conviction failures — each one is an incident, not a logging miss", "lines": []},
        "recovery": {"value": sum(1 for r in rows if r["kind"] == "release"), "note": "Releases: expired clean or dual-control",
                     "lines": [f"{sum(1 for r in rows if r['kind'] == 'release' and r['outcome'] == 'expired_clean')} expired clean · "
                               f"{sum(1 for r in rows if r['kind'] == 'release' and r['outcome'] == 'released_by_dual_control')} released by dual control"]},
    }


def charts(rows):
    crossings = [r for r in rows if r["kind"] == "crossing"]
    detections = [r for r in rows if r["kind"] == "detection"]
    activity = [{"label": b, "value": sum(1 for r in crossings if r["boundary"] == b)} for b in commission_gate.PROTECTED_BOUNDARIES]
    responses = [{"label": c, "value": sum(1 for r in detections if r["action_class"] == c)} for c in ("annotate", "shape", "contain", "sever")]
    return {"activity": activity, "responses": responses}


def patterns(rows, now):
    days = [(now - timedelta(days=8 - i)).date() for i in range(9)]
    out = []
    for principal in sorted({r["principal_id"] for r in rows if r["kind"] == "crossing" and r["outcome"] == "refused"}):
        mine = [r for r in rows if r.get("principal_id") == principal]
        curve = [sum(1 for r in mine if r["kind"] == "crossing" and r["outcome"] == "refused" and _parse(r["at"]).date() == d) for d in days]
        detections = [r for r in mine if r["kind"] == "detection"]
        if not sum(curve) and not detections:
            continue
        out.append({"subject_ref": commission_gate.subject_ref(principal), "principal_id": principal, "curve": curve,
                    "refusals_9d": sum(curve), "effects": sum(1 for r in mine if r["kind"] == "effect"),
                    "last_detector": detections[-1]["detector"] if detections else None,
                    "redeclaration_requested": any(r["kind"] == "redeclaration_requested" for r in mine)})
    return out


def mirage(rows, now):
    planted = [r for r in rows if r["kind"] == "mirage_planted"]
    live = [r for r in planted if _parse(r["expires_at"]) > now]
    touches = [r for r in rows if r["kind"] == "detection" and r.get("detector") == "mirage_incrimination"]
    checks = [r["isolation_check"] for r in planted]
    passed = all(c.get("passed") for c in checks) if checks else None
    return {"planted": len(planted), "live": len(live), "touches": len(touches), "isolation_passed": passed,
            "findings": ([f"Isolation measured against {checks[-1]['stores_compared']} production stores: {'disjoint' if passed else 'OVERLAP'}"] if checks else
                         ["No decoy has been planted for this tenant; isolation is measured at planting."])
            + [f"{len(live)} decoy(s) live, {len(planted) - len(live)} expired; construction and placement are not shown here",
               f"{len(touches)} touch(es), each a structural conviction with its own mark and sever"]
            + ["Entry into the mirage above containment is not autonomous: the owner has not ruled the entry threshold (highest bar holds)."]}


def marked(tenant_id, rows):
    from services.watch.mark import read_marks
    owned = {d["mark_id"]: d for d in rows if d["kind"] == "detection" and d.get("mark_id")}
    demarked = {r.get("mark_ref") for r in rows if r["kind"] == "release" and r["outcome"] == "released_by_dual_control"}
    return [{"mark_id": m.mark_id, "subject_ref": m.identity, "minted_at": m.minted_at, "action_ref": m.action_ref,
             "standing": "de-marked by dual control" if m.mark_id in demarked else "held",
             "dimensions_bound": 6, "notice_sent": bool(notices.by_ref(tenant_id, "action_ref", m.action_ref))}
            for m in read_marks() if m.mark_id in owned]


def panel(tenant_id, items):
    out = []
    for d in sorted(items.values(), key=lambda d: (d["state"] != "open", -d["blast"], d["opened_at"])):
        left = [f"Verdict {d['refs'].get('verdict_ref') or d['refs'].get('proposal_id') or '—'}", f"Action {d['refs'].get('action_ref') or 'none (requirement)'}",
                f"Mark {d['refs'].get('mark_ref') or 'none'}", f"Opened by {d['opened_by']} at {d['opened_at']}"]
        right = ([f"Grounding seam {d['refs'].get('grounding_seam_id')}", f"Routing {d['refs'].get('routing')}", f"Citations {len(d['refs'].get('citations', []))}"]
                 if d["klass"] == "requirement_ratification" else
                 [f"Subject {d['subject_ref']}", "Governance admitted this principal to the tenant; the Watch holds the gate", "Neither authority overrules the other alone"])
        out.append({**{k: d[k] for k in ("decision_id", "klass", "subject_ref", "opened_at", "opened_by", "title", "state", "blast", "approvers", "approvals_needed", "acknowledged_by")},
                    "declined": d["declined"], "executed": d["executed"], "watch_record": left, "governance_record": right, "refs": d["refs"]})
    return out


def record_walks(tenant_id, gate, rows):
    """Every acted row carries its evidence walk: signal → verdict → policy row → action → outcome → witness."""
    attest = {a.subject_ref.split(":", 1)[1]: a.attestation_id for a in witness_binding.attestations_for(gate["action_ids"].keys())}
    walks = {}
    for action_id, d in gate["action_ids"].items():
        effects = gate["effects"].get(action_id, [])
        release = gate["releases"].get(action_id)
        witness = attest.get(action_id) or d.get("witness_attestation")
        walk = {"signal": f"{d['detector']} at {d['boundary']}", "verdict": f"{d['verdict_id']} · {'structural_certainty' if d['action_class'] == 'sever' else 'externally_steerable'}",
                "policy": f"Mkono ladder → {d['action_class']}" + (f" · TTL {d['ttl_seconds']} s" if d.get("ttl_seconds") else " · holds") + f" · {d.get('requirements', 'thresholds=DEFAULT_PENDING_OWNER_RULING')}",
                "action": action_id, "outcome": f"{len(effects)} effect receipt(s)" + (f" · released {release['outcome']}" if release else ""),
                "witness": witness or None}
        walks[action_id] = walks[d["verdict_id"]] = {**walk, "complete": all(walk.values())}
    return walks


def budgets(rows, now):
    """Canon 8 §7/§19 gauges, measured from the feed: friction = share of crossings by innocents (later
    released clean) that met Watch friction; blast = share of active principals under an autonomous
    action in the rolling hour. Ceilings are DEFAULT class pending ruling."""
    hour = now - timedelta(hours=1)
    crossings = [r for r in rows if r["kind"] == "crossing"]
    innocents = {r["principal_id"] for r in rows if r["kind"] == "release" and r["outcome"] == "expired_clean"}
    friction_hits = sum(1 for r in rows if r["kind"] == "effect" and r["principal_id"] in innocents)
    active = {r["principal_id"] for r in crossings if _parse(r["at"]) >= hour}
    acted = {r["principal_id"] for r in rows if r["kind"] == "detection" and r["action_class"] != "annotate" and _parse(r["at"]) >= hour}
    return {"friction": {"share": round(friction_hits / len(crossings), 4) if crossings else 0.0, "hits": friction_hits, "of": len(crossings),
                         "ceiling": "≤ 0.5% weekly (DEFAULT)", "note": "effects felt by principals later released clean, over all crossings"},
            "blast": {"share": round(len(acted & active) / len(active), 4) if active else 0.0, "acted": len(acted & active), "of": len(active),
                      "ceiling": "≤ 5% of active actors per hour (DEFAULT · dual-control)", "note": "principals under an autonomous shape/contain/sever this hour"}}


def learning(rows):
    steps = [r for r in rows if r["kind"] == "learning"]
    live = learning_loop.current()
    return {"requirements_version": live["version"] if live else None, "label": learning_loop.label(),
            "ratified_at": live["ratified_at"] if live else None, "steps": steps[-6:]}
