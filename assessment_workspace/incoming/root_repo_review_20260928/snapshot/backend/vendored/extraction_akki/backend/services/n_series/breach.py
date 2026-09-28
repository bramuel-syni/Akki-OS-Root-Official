"""services.n_series.breach — CA1-N2 breach notification enforcement.

Wave E · CP-E2 (2026-08-27T~13:35Z) · Owner ruling verbatim:
    "CA1-N2 breach notification: recipients = DPO + the Watch's existing
     external witness; window = 72 hours (canon-grounded Kenya DPA/GDPR);
     channel = enforcement-view record PLUS real-time alert to both
     recipients; threshold = a hard line ACTUALLY CROSSED — map onto
     the existing Watch event grammar (containment failure / actual
     exfiltration / unreceipted crossing). Contained/shaped events are
     the Watch working and MUST NOT trigger notification — encode that
     as an invariant, not a comment."

Enforcement:
  * policy config `breach_policy.v0.json` resolves the four sentinels;
    payload sentinels still refuse (caller must pick resolved values);
  * recipient_witness_id MUST be a registered WitnessIdentity_v0 with
    independent_of_authorities=True;
  * recipient_dpo_id MUST be non-empty;
  * source_watch_action_class in {annotate, shape, contain} REFUSES
    (contained/shaped events are the Watch working — owner invariant);
  * notify_deadline_utc computed as triggered_at + 72h if not supplied;
  * real-time alert file drops written to
    BREACH_ALERTS_DIR/{recipient_id}/{notification_id}.json for BOTH
    the DPO and the witness — channel = ledger row PLUS real-time
    alert per owner ruling.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List

from contracts.breach_notification import (
    OWNER_POLICY_PENDING,
    BreachNotification_v0,
)
from services.watch.witness import load_identities


_DEFAULT_DIR = "/app/assessment_workspace/phase0/breach_notifications"
_DEFAULT_ALERTS_DIR = "/app/assessment_workspace/phase0/breach_alerts"
_POLICY_PATH = Path(__file__).with_name("breach_policy.v0.json")

_NON_NOTIFIABLE = {"annotate", "shape", "contain"}


def _dir() -> Path:
    return Path(os.environ.get("BREACH_NOTIFICATIONS_DIR", _DEFAULT_DIR))


def _alerts_dir() -> Path:
    return Path(os.environ.get("BREACH_ALERTS_DIR", _DEFAULT_ALERTS_DIR))


def load_policy() -> Dict[str, Any]:
    """Load the CA1-N2 policy config. Owner-supplied resolved values."""
    return json.loads(_POLICY_PATH.read_text())


def _witness_or_refuse(witness_id: str) -> None:
    """Refuse if the recipient witness is not registered OR not
    canonically independent (Canon 8 §9)."""
    for w in load_identities():
        if w.witness_id == witness_id:
            if w.independent_of_authorities is not True:
                raise ValueError(
                    f"CA1-N2 · recipient witness {witness_id!r} on "
                    f"record but `independent_of_authorities` is not "
                    f"True — Canon 8 §9 verbatim invariant violated. "
                    f"On-disk record tampered; refuse to notify."
                )
            return
    raise ValueError(
        f"CA1-N2 · witness {witness_id!r} not on record. Register the "
        f"witness identity (POST /api/watch/witness/identity) before "
        f"firing a breach notification."
    )


def _compute_deadline_utc(triggered_at: str, hours: int) -> str:
    """triggered_at ISO-8601 UTC → deadline ISO-8601 UTC + hours."""
    dt = datetime.fromisoformat(triggered_at.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    deadline = dt + timedelta(hours=hours)
    return deadline.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_realtime_alerts(n: BreachNotification_v0) -> List[str]:
    """Ledger row PLUS real-time alert channel (owner ruling verbatim).
    Writes two file drops: one for DPO, one for witness. Returns the
    absolute paths written."""
    d = _alerts_dir()
    receipts: List[str] = []
    for recipient_id, role in (
        (n.recipient_dpo_id, "dpo"),
        (n.recipient_witness_id, "external_witness"),
    ):
        rd = d / recipient_id
        rd.mkdir(parents=True, exist_ok=True)
        path = rd / f"{n.notification_id}.json"
        payload = {
            "notification_id": n.notification_id,
            "recipient_id": recipient_id,
            "recipient_role": role,
            "triggered_at": n.triggered_at,
            "notify_deadline_utc": n.notify_deadline_utc,
            "trigger_event_class": n.trigger_event_class,
            "breach_summary": n.breach_summary,
            "source_watch_action_class": n.source_watch_action_class,
            "policy_ref": "services/n_series/breach_policy.v0.json",
        }
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        receipts.append(str(path))
    return receipts


def fire_breach_notification(payload: Dict[str, Any]) -> BreachNotification_v0:
    """CA1-N2 · fire a breach notification with full enforcement.

    Refuses on:
      * any of q1..q4 still at OWNER_POLICY_PENDING (caller must adopt
        the resolved policy values from breach_policy.v0.json);
      * source_watch_action_class in {annotate, shape, contain} (owner
        invariant: contained/shaped events are the Watch working and
        MUST NOT trigger notification);
      * recipient_dpo_id empty OR recipient_witness_id not registered
        as an independent WitnessIdentity_v0;
      * overwrite of an existing notification_id.
    Auto-computes notify_deadline_utc if payload omits it.
    Writes real-time alerts to BOTH recipients on success.
    """
    payload = dict(payload)  # local mutation only

    # DPO required (owner ruling: DPO + witness).
    if not payload.get("recipient_dpo_id"):
        raise ValueError(
            "CA1-N2 · recipient_dpo_id is required · owner ruling "
            "'DPO + the Watch's existing external witness'."
        )

    # Watch-event-grammar invariant BEFORE contract validation so the
    # refusal message names the ruling.
    src = payload.get("source_watch_action_class", "")
    if src in _NON_NOTIFIABLE:
        raise ValueError(
            f"CA1-N2 · source_watch_action_class={src!r} is a "
            f"contained/shaped event · the Watch working as intended · "
            f"NOT a breach per owner ruling verbatim: 'contained/shaped "
            f"events are the Watch working and MUST NOT trigger "
            f"notification — encode that as an invariant, not a "
            f"comment.'"
        )

    # 72h deadline auto-compute if absent.
    policy = load_policy()
    if not payload.get("notify_deadline_utc"):
        payload["notify_deadline_utc"] = _compute_deadline_utc(
            payload["triggered_at"], policy.get("window_hours", 72),
        )

    # Contract validation.
    n = BreachNotification_v0(**payload)

    # Sentinel refusal — caller must adopt resolved policy values.
    pending = [
        f for f in ("q1_trigger_scope", "q2_notification_routing",
                    "q3_actor_masking", "q4_cadence")
        if getattr(n, f) == OWNER_POLICY_PENDING
    ]
    if pending:
        raise ValueError(
            f"CA1-N2 · policy fields still {OWNER_POLICY_PENDING!r}: "
            f"{pending}. Adopt the resolved values from "
            f"services/n_series/breach_policy.v0.json before firing."
        )

    # Witness registered + independent (defence-in-depth).
    _witness_or_refuse(n.recipient_witness_id)

    # Real-time alert file drops (BOTH recipients).
    receipts = _write_realtime_alerts(n)

    # Ledger record. Rebuild with alert_channel_receipts populated.
    n = BreachNotification_v0(**{
        **n.model_dump(),
        "alert_channel_receipts": receipts,
    })

    d = _dir()
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{n.notification_id}.json"
    if path.exists():
        raise ValueError(
            f"CA1-N2 · notification {n.notification_id!r} already on "
            f"record. Canon 8 §43: correction is by new entry only."
        )
    path.write_text(json.dumps(n.model_dump(), indent=2, ensure_ascii=False))
    return n


def load_breach_notifications() -> List[BreachNotification_v0]:
    d = _dir()
    if not d.is_dir():
        return []
    return [
        BreachNotification_v0(**json.loads(p.read_text()))
        for p in sorted(d.glob("bn_*.json"))
    ]
