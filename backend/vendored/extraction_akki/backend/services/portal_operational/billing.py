"""Read-only period billing from the canonical ledger, never a second bill store.

Only linked measured events qualify. Integer credit contracts do not authorise
rounding: a fractional result is held rather than silently truncated to free use.
"""
import math
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pydantic import BaseModel, ConfigDict, Field
from contracts.dap import MeteredEvent
from services.entitlement_service_v1.catalog import CatalogRow
from services.entitlement_service_v1.licence import Licence
from services.ledger_writer.principal_control import read_events


def instant(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        raise ValueError('A timezone-aware period boundary is required.')
    return parsed


def debit(usage, row):
    if (not math.isfinite(usage.quantity) or usage.quantity < 0
            or row.status != 'listed'):
        raise ValueError('Invalid metered quantity/catalog state.')
    if row.access_class != 'reseller_frontier':
        return 0
    if usage.quantity_unit != 'tokens' or not math.isfinite(row.credit_rate):
        raise ValueError('Token units and an event-time rate are required.')
    quantity, rate = Decimal(str(usage.quantity)), Decimal(str(row.credit_rate))
    if quantity != quantity.to_integral_value():
        raise ValueError('A token count must be integral.')
    value = quantity * rate
    if not value.is_finite() or value != value.to_integral_value():
        raise ValueError('Fractional credits require an explicit rounding policy.')
    return int(value)


class LicenceInvoiceLine(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    ledger_ref: str
    execution_receipt_ref: str
    model_identifier: str
    access_class: str
    terms_id: str
    timestamp_iso: str
    quantity: float
    quantity_unit: str
    credits: int


class LicenceInvoiceView(BaseModel):
    model_config = ConfigDict(extra='forbid')
    status: str = 'unresolved'
    reason_code: str
    principal_id: str
    period_iso: str
    period_start: str | None = None
    period_end: str | None = None
    lines: list[LicenceInvoiceLine] = Field(default_factory=list)
    credits_total: int | None = None
    scope: str = 'principal'
    financial_invoice_issued: bool = False


def linked_usage(event, events):
    """Re-derive terms, quantities, owner and clock from the dispatch/meter chain."""
    p = event['payload']
    if p.get('evidence_mode') != 'measured' or not p.get('execution_receipt_ref'):
        raise ValueError('Unmeasured or unlinked usage cannot be billed.')
    usage = MeteredEvent.model_validate(p['metered_event'])
    row = CatalogRow.model_validate(p['catalog_row_at_event'])
    raw = next((e for e in events if e['row']['hash'] == p.get('raw_meter_hash')), None)
    if raw is None or raw['row']['resource_type'] != 'execution_flow' or raw['payload'].get('slot') != 'metered':
        raise ValueError('Canonical raw meter is missing.')
    meter = raw['payload']['data']
    dispatches = [e for e in events if e['row']['run_id'] == event['row']['run_id']
                  and e['row']['resource_type'] == 'execution_flow' and e['payload'].get('slot') == 'dispatch']
    if len(dispatches) != 1:
        raise ValueError('Canonical dispatch is missing or ambiguous.')
    dispatch = dispatches[0]
    snapshot = dispatch['payload']['data']['commercial_snapshot']
    original_row = CatalogRow.model_validate(snapshot['catalog_row'])
    licence = Licence.model_validate(snapshot['licence'])
    quantities = [q for q in meter['usage'] if q['unit'] == usage.quantity_unit]
    if (meter['evidence_mode'] != 'measured' or original_row != row
            or meter['worker_receipt_ref'] != p['execution_receipt_ref']
            or meter['terms_ref'] != usage.terms_id or licence.terms_identifier != usage.terms_id
            or licence.organisation_principal_id != p['organisation_principal_id']
            or snapshot['principal_id'] != usage.party_id or p.get('principal_id') != usage.party_id
            or raw['row']['run_id'] != event['row']['run_id']
            or len(quantities) != 1 or Decimal(quantities[0]['quantity']) != Decimal(str(usage.quantity))
            or instant(usage.timestamp_iso).timestamp() != raw['row']['at']['epoch_s']
            or not dispatch['row']['seq'] < raw['row']['seq'] < event['row']['seq']):
        raise ValueError('Meter/dispatch/event evidence does not reconcile.')
    return usage, row, debit(usage, row)


async def read_invoice(db, scope, period_iso):
    view = LicenceInvoiceView(principal_id=scope['principal_id'], period_iso=period_iso,
                              reason_code='ORGANISATION_UNRESOLVED')
    events = await read_events(db, {'row.tenant_id': scope['tenant_id']})
    try:
        members = [e['payload'] for e in events if e['row']['resource_type'] == 'principal_membership'
                   and e['payload'].get('principal_id') == scope['principal_id']]
        if not members or members[-1].get('status') != 'active' or not members[-1].get('admission_receipt_ref'):
            return view
        org = members[-1]['organisation_principal_id']
        periods = [e['payload'] for e in events if e['row']['resource_type'] == 'entitlement_licence'
                   and e['payload'].get('licence', {}).get('organisation_principal_id') == org
                   and e['payload'].get('period_iso') == period_iso and e['payload'].get('admission_receipt_ref')]
        view.reason_code = 'PERIOD_UNRESOLVED'
        if not periods:
            return view
        if len({(p['period_start'], p['period_end']) for p in periods}) != 1:
            raise ValueError('Period boundaries cannot change in place.')
        period = periods[-1]
        Licence.model_validate(period['licence'])
        start, end = instant(period['period_start']), instant(period['period_end'])
        if end <= start:
            raise ValueError('Invalid period interval.')
        view.period_start, view.period_end = start.isoformat(), end.isoformat()
        lines, seen = [], set()
        # A party view never discloses other seats' operation details, even in a pool.
        for event in events:
            p = event['payload']
            if (event['row']['resource_type'] != 'metered_event' or p.get('organisation_principal_id') != org
                    or p.get('metered_event', {}).get('party_id') != scope['principal_id']):
                continue
            timestamp = instant(p['metered_event']['timestamp_iso'])
            if not start <= timestamp < end:
                continue
            if timestamp > datetime.now(timezone.utc):
                raise ValueError('Future metering is not evidence of consumption.')
            usage, row, credits = linked_usage(event, events)
            identity = (p['raw_meter_hash'], usage.quantity_unit)
            if identity in seen:
                raise ValueError('Duplicate commercial usage identity.')
            seen.add(identity)
            lines.append(LicenceInvoiceLine(ledger_ref=event['row']['hash'], execution_receipt_ref=p['execution_receipt_ref'],
                model_identifier=row.model_identifier, access_class=row.access_class, terms_id=usage.terms_id,
                timestamp_iso=usage.timestamp_iso, quantity=usage.quantity, quantity_unit=usage.quantity_unit, credits=credits))
        view.lines, view.credits_total = lines, sum(line.credits for line in lines)
        view.status, view.reason_code = 'resolved', ''
    except (ValueError, TypeError, KeyError, OverflowError, InvalidOperation):
        view.status, view.reason_code = 'unresolved', 'BILLING_EVIDENCE_INVALID'
        view.lines, view.credits_total = [], None
    return view