"""Read-only entitlement projections from receipted control-plane events.

No licence seeding, ceremony, price setting, or entitlement-specific balance.
Admission/ceremony producers must bank these records through the canonical writer.
Until they do, unresolved is the only truthful production response.
"""
from datetime import datetime, timezone
import math
from pydantic import BaseModel, ConfigDict, Field
from contracts.dap import MeteredEvent
from services.entitlement_service_v1.licence import Licence
from services.entitlement_service_v1.catalog import CatalogRow
from services.entitlement_service_v1.allowance import LicenceAllowanceState, derive_allowance_remaining
from services.entitlement_service_v1.chokepoint_resolver import _dial_admits_access_class
from services.ledger_writer.principal_control import read_events


class LicencePortalView(BaseModel):
    model_config = ConfigDict(extra="forbid")
    principal_id: str
    status: str = "unresolved"
    reason_code: str
    licence: Licence | None = None
    allowance_state: LicenceAllowanceState | None = None
    rows: list[CatalogRow] = Field(default_factory=list)
    badges: list[CatalogRow] = Field(default_factory=list)
    count: int = 0


def instant(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("A timezone-aware period boundary is required.")
    return parsed


async def read_view(db, scope):
    view = LicencePortalView(principal_id=scope["principal_id"], reason_code="ORGANISATION_UNRESOLVED")
    events = await read_events(db, {"row.tenant_id": scope["tenant_id"], "row.resource_type": {"$in": [
        "principal_membership", "entitlement_licence", "entitlement_catalog", "metered_event"]}})
    memberships = [e["payload"] for e in events if e["row"]["resource_type"] == "principal_membership"
                   and e["payload"].get("principal_id") == scope["principal_id"]]
    if not memberships:
        return view
    member = memberships[-1]
    if member.get("status") != "active" or not member.get("admission_receipt_ref"):
        return view
    org = member.get("organisation_principal_id")
    if not isinstance(org, str) or not org:
        return view
    licences = [e["payload"] for e in events if e["row"]["resource_type"] == "entitlement_licence"
                and e["payload"].get("licence", {}).get("organisation_principal_id") == org]
    view.reason_code = "LICENCE_UNRESOLVED"
    if not licences or not licences[-1].get("admission_receipt_ref"):
        return view
    try:
        record = licences[-1]
        licence = Licence.model_validate(record["licence"])
        view.licence = licence
        if licence.status != "active":
            view.status, view.reason_code = licence.status, f"LICENCE_{licence.status.upper()}"
            return view
        now = datetime.now(timezone.utc)
        if instant(licence.renewal_date) <= now:
            view.status, view.reason_code = "expired", "LICENCE_EXPIRED"
            return view
        start, end = instant(record["period_start"]), instant(record["period_end"])
        if not start <= now < end or not record.get("period_iso"):
            view.reason_code = "PERIOD_UNRESOLVED"
            return view
        catalog = {}
        for event in events:
            p = event["payload"]
            if event["row"]["resource_type"] == "entitlement_catalog" and p.get("ceremony_receipt_ref"):
                row = CatalogRow.model_validate(p["catalog_row"])
                catalog[(row.model_identifier, row.access_class)] = (row, p.get("organisation_principal_id"))
        admitted = [row for row, owner in catalog.values() if row.status == "listed"
                    and (row.access_class != "customer_model" or owner == org)
                    and _dial_admits_access_class(licence=licence, access_class=row.access_class)]
        view.rows, view.badges, view.count = admitted, admitted, len(admitted)
        debited = 0
        for event in events:
            p = event["payload"]
            if event["row"]["resource_type"] != "metered_event" or p.get("organisation_principal_id") != org:
                continue
            usage = MeteredEvent.model_validate(p["metered_event"])
            if not licence.pooled_credits_flag and usage.party_id != scope["principal_id"]:
                continue
            if not start <= instant(usage.timestamp_iso) < end:
                continue
            # An event-time catalog snapshot is hash-bound by the ledger. Never
            # apply today's rate to history or assume a missing rate is zero.
            row = CatalogRow.model_validate(p["catalog_row_at_event"])
            if usage.quantity < 0 or not math.isfinite(usage.quantity) or not p.get("execution_receipt_ref"):
                raise ValueError("Invalid metered event.")
            if row.access_class == "reseller_frontier" and usage.quantity_unit != "tokens":
                raise ValueError("Token metering required for reseller usage.")
            rate = row.credit_rate if row.access_class == "reseller_frontier" else 0
            if not math.isfinite(rate):
                raise ValueError("Invalid event-time rate.")
            # Rates belong to event-time rows, not to today's catalog or a
            # terms-only map: different models may share one licence terms ID.
            debited += derive_allowance_remaining(
                licence_terms_id=licence.terms_identifier, period_iso=record["period_iso"],
                credits_allowance=0, ledger_events=[usage],
                credit_rate_by_terms_id={usage.terms_id: rate},
            ).credits_debited
        allowance = licence.credits_per_seat_per_period * (licence.seat_count if licence.pooled_credits_flag else 1)
        view.allowance_state = LicenceAllowanceState(
            licence_terms_id=licence.terms_identifier, period_iso=record["period_iso"],
            credits_allowance=allowance, credits_debited=debited, credits_remaining=allowance - debited)
        view.status, view.reason_code = "resolved", ""
    except (ValueError, TypeError, KeyError, OverflowError):
        view.status, view.reason_code = "unresolved", "ENTITLEMENT_RECORD_INVALID"
        view.allowance_state, view.rows, view.badges, view.count = None, [], [], 0
    return view