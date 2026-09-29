"""Binding of the existing witness fabric (Canon 8 §16) to the commission-gate record.

The record witness holds no Watch or governance credentials: it only reads on-record action
files, attests their digests, and runs the standing break-in test through the production writer
(which must refuse). Placement is honest: it runs in the application pod, not yet in a separate
deployment — that gap is declared on the identity and on the console."""
import uuid
from datetime import datetime, timezone

WITNESS_ID = "wi_gate_record_witness"
NOTE = ("Record witness for commission-gate actions. Holds no Watch credentials and no governance "
        "credentials; performs read-only digest attestation and the standing break-in test. Placement: "
        "application pod, not yet a separate deployment (declared gap).")


def _iso(dt):
    return dt.isoformat().replace("+00:00", "Z")


def ensure_identity(now=None):
    from services.watch.witness import load_identities, register_identity
    for w in load_identities():
        if w.witness_id == WITNESS_ID:
            return w
    now = now or datetime.now(timezone.utc)
    return register_identity({"witness_id": WITNESS_ID, "registered_at": _iso(now),
                              "signing_material_ref": "witness_binding:sha256-digest-attestation",
                              "independent_of_authorities": True, "registration_note": NOTE})


def attest_action(action_id, now=None):
    from services.watch.witness import attest_watch_action
    now = now or datetime.now(timezone.utc)
    ensure_identity(now)
    return attest_watch_action(attestation_id=f"wa_gate_{uuid.uuid4().hex[:12]}", witness_id=WITNESS_ID,
                               watch_action_id=action_id, attested_at=_iso(now),
                               attestation_note="Digest of the on-record gate action at mint time; later drift against it is tamper.")


def break_in(action_id, now=None):
    from services.watch.witness import run_standing_break_in_test
    now = now or datetime.now(timezone.utc)
    ensure_identity(now)
    return run_standing_break_in_test(break_in_id=f"bit_gate_{uuid.uuid4().hex[:12]}", witness_id=WITNESS_ID,
                                      target_action_id=action_id, at_iso=_iso(now))


def attestations_for(action_ids):
    from services.watch.witness import load_attestations
    wanted = {f"action:{a}" for a in action_ids}
    return [a for a in load_attestations() if a.subject_kind == "watch_action" and a.subject_ref in wanted]


def summary():
    from services.watch.witness import load_alarms, load_attestations, load_identities
    identity = next((w for w in load_identities() if w.witness_id == WITNESS_ID), None)
    return {"identity": identity.witness_id if identity else None, "placement": "application pod (not a separate deployment)",
            "attestations": sum(1 for a in load_attestations() if a.subject_kind == "watch_action"),
            "tamper_alarms": len(load_alarms()), "note": NOTE}
