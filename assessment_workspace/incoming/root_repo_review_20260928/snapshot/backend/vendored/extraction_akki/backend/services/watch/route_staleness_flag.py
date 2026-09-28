"""services.watch.route_staleness_flag — CA1-012 Watch staleness route.

Canon addendum: "Extend the Watch's existing self-flagging of stale
baits (Doc 3) to rulebook re-certification and training baselines:
anything adopted from an external standard carries a staleness check
against that standard's own revision history, using the same
flagging mechanism."

W9 CP3 delivers the generic staleness route function. Callers pass
(record_kind, record_id, external_standard_ref, last_seen_at,
current_revision_iso). If current > last_seen, the seam fires a
verdict + action pair (Canon 8 §32.5 atomic act-and-attest).
Idempotent per (record_kind, record_id).

Scope enforced (CA1-012 verbatim): record_kind must be one of
'baseline_line' or 'rulebook_rule'. Unknown kinds raise ValueError.

Sensor + responder names:
  * sensor    = 'macho.staleness_watcher'
  * responder = 'mkono.staleness_responder'
"""
from __future__ import annotations

from typing import Any, Dict, Literal

from services.watch.macho import mint_verdict, load_verdicts
from services.watch.mkono import act_on_verdict, load_actions


_ALLOWED_KINDS = ("baseline_line", "rulebook_rule")


def _existing_pair(record_kind: str, record_id: str) -> Dict[str, Any]:
    subject_ref = f"{record_kind}:{record_id}"
    for v in load_verdicts():
        if (
            v.signal_class == "baseline_standard_stale"
            and v.subject_ref == subject_ref
        ):
            for a in load_actions():
                if a.verdict_id == v.verdict_id:
                    return {
                        "fired": True,
                        "state": "stale",
                        "verdict_id": v.verdict_id,
                        "action_id": a.action_id,
                    }
            return {
                "fired": True,
                "state": "stale",
                "verdict_id": v.verdict_id,
                "action_id": None,
            }
    return {}


def route_staleness_flag(
    record_kind: str,
    record_id: str,
    external_standard_ref: str,
    last_seen_at: str,
    current_revision_iso: str,
) -> Dict[str, Any]:
    """CA1-012 Watch staleness route. See module docstring."""
    if record_kind not in _ALLOWED_KINDS:
        raise ValueError(
            f"record_kind {record_kind!r} not in allowed set "
            f"{_ALLOWED_KINDS!r}. CA1-012 scope: rulebook_rule OR "
            f"baseline_line only."
        )
    if current_revision_iso <= last_seen_at:
        return {"fired": False, "state": "up_to_date"}

    existing = _existing_pair(record_kind, record_id)
    if existing:
        return existing

    # Sanitize record_id for id suffix (dots and hyphens are common;
    # verdict/action ids are lowercase per contract pattern).
    sfx = (
        f"{record_kind}_{record_id.replace('.', '_').replace('-', '_')}"
    ).lower()
    verdict_id = f"vd_stale_{sfx}"
    action_id = f"ax_stale_{sfx}"

    v = mint_verdict({
        "verdict_id": verdict_id,
        "at_iso": current_revision_iso,
        "sensor": "macho.staleness_watcher",
        "signal_class": "baseline_standard_stale",
        "severity": "attention",
        "subject_kind": "artifact",
        "subject_ref": f"{record_kind}:{record_id}",
        "evidence_note": (
            f"Record {record_kind}:{record_id!r} carries external "
            f"standard {external_standard_ref!r} last seen at "
            f"{last_seen_at!r}; current revision {current_revision_iso!r} "
            f"has revised since. CA1-012 staleness."
        ),
    })
    a = act_on_verdict({
        "action_id": action_id,
        "at_iso": current_revision_iso,
        "verdict_id": v.verdict_id,
        "action_class": "mark_minted",
        "responder": "mkono.staleness_responder",
        "acted_on_ref": f"{record_kind}:{record_id}",
        "outcome_note": (
            f"Staleness mark minted on {record_kind}:{record_id!r} "
            f"against external standard {external_standard_ref!r}. "
            f"Re-certification required before further reliance."
        ),
    })
    return {
        "fired": True,
        "state": "stale",
        "verdict_id": v.verdict_id,
        "action_id": a.action_id,
    }
