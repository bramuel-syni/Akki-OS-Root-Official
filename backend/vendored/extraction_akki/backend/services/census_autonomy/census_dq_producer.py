"""Live census DQ producer — turns REAL per-host census outcomes into
actionable response-required items surfaced in the portal UI.

This runs off the genuine census detail manifests banked by the non-GPU /
jump dispatchers (never a synthetic fixture). Content-registry asset records
are already written live per completed source by
`services.mtafiti.census_result_adapter.register_outcome`; this producer adds
the honest data-quality signal: every connection the real census could NOT read
is banked as an owner-answerable unblock action (grant, network path, credential).
"""
import glob
import json
import os

from services.census_autonomy import operational_store as store
from services.census_autonomy.response_required_queue import bank_response_required_item


def _action_for(reason_code, label):
    r = (reason_code or "").lower()
    if "1045" in r or "access denied" in r or "credential" in r:
        return (f"Grant read (SELECT + PROCESS) to the census account on '{label}' "
                f"for the estate census route's source IP, then re-run the census.")
    if "timeout" in r or "unavailable" in r or "unreachable" in r or "1049" in r:
        return (f"Open the network/firewall path to '{label}' from the census route "
                f"(or route it via the jump server), then re-run the census.")
    if "database_bound_exceeded" in r:
        return (f"'{label}' exposes more databases than the census bound; raise the "
                f"bound or scope the source, then re-run.")
    return f"Investigate '{label}' census read failure ({reason_code}); then re-run."


def emit_from_run(census_run_id, tenant_id):
    """Bank one response-required item per connection the real census could not
    read. Returns the list of banked item_ids. Idempotent per (run, host)."""
    banked = []
    existing = _existing_signatures(tenant_id)
    pattern = str(store.cursor_dir() / f"transport-{census_run_id}-*.json")
    for path in sorted(glob.glob(pattern)):
        try:
            detail = json.loads(open(path).read())
        except (OSError, ValueError):
            continue
        source = detail.get("source_id", "")
        for conn in detail.get("connections", []) or []:
            if conn.get("status") == "complete":
                continue
            label = conn.get("label") or conn.get("host_fingerprint") or "unknown"
            signature = f"{census_run_id}|{source}|{label}"
            if signature in existing:
                continue
            action = _action_for(conn.get("reason_code"), label)
            reason_text = (f"[UNBLOCK action_class=host_reachability] {action}\n"
                           f"source={source} host={label} "
                           f"census_reason={conn.get('reason_code')}")
            banked.append(bank_response_required_item(
                census_run_id=census_run_id, tenant_id=tenant_id,
                reason_text=reason_text, refusal_code="BLOCKED_SURFACE_UNREACHABLE",
                decision_timestamp_utc=store.now()))
    return banked


def _existing_signatures(tenant_id):
    """Signatures already banked, so re-runs of the same census don't duplicate."""
    from services.census_autonomy.response_required_queue import list_pending_response_required_items
    sigs = set()
    try:
        for item in list_pending_response_required_items():
            if item.get("tenant_id") != tenant_id:
                continue
            text = item.get("reason_text", "")
            run = item.get("census_run_id", "")
            src = _field(text, "source=")
            host = _field(text, "host=")
            if src and host:
                sigs.add(f"{run}|{src}|{host}")
    except Exception:  # noqa: BLE001
        pass
    return sigs


def _field(text, key):
    idx = text.find(key)
    if idx < 0:
        return ""
    rest = text[idx + len(key):]
    return rest.split()[0] if rest.split() else ""
