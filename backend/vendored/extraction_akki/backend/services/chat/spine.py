"""Qualified-memory spine (M4-T1 / M5 seam): verified artefacts → bounded whole-unit read → scoped working set.

The answerer never walks an estate. It reads sealed, independently inspected, rights-bearing qualified units
through the admitted runtime that holds them (mode `unit_select`), holds them only for the turn, and records
references — never content — in the requester's plane-scoped working set.
"""
import asyncio
import hashlib
import os

from core import db
from services.activation.receipts import RESOURCE as RECEIPTS
from services.estate_admission.records import latest
from services.estate_admission.runtimes import runtime_by_id
from services.extraction_runtime import objects, remote
from services.extraction_runtime.adapter import CALL_SECONDS, object_store_secrets
from services.extraction_runtime.structured_records_worker import unit_terms
from services.ledger_writer.principal_control import read_events
from services.memory import plane_registry, working_set
from services.memory.plane_registry import MEMORY_PLANE_COLLECTION
from services.memory.scoped_accessor import for_plane
from services.northena.execution_journal import LedgerJournal
from services.northena.execution_models import Held
from services.portal_operational.execution_records import events_for, snapshot
from services.work_orders import packaging


def _int_env(name, default):
    try:
        return int(os.environ.get(name) or default)
    except ValueError:
        return default


# [SLOT] bounded candidate retrieval per artefact; measured, not committed to in advance.
MAX_CANDIDATES = _int_env('AKKI_ANSWER_MAX_CANDIDATES', 48)
MAX_NEIGHBOURS = _int_env('AKKI_ANSWER_MAX_NEIGHBOURS', 12)


def unit_ref(tenant, request_id, unit_id):
    return f"akki://unit/{tenant}/{request_id}/{unit_id}"


def question_terms(text):
    return sorted(unit_terms(text))


def _active_rights(events):
    """unit_ref → rights receipt hash for receipts whose latest status is active and not revoked."""
    active, by_hash = {}, {}
    for e in events:
        receipt = e['payload'].get('receipt') or {}
        claims = receipt.get('claims') or {}
        if receipt.get('kind') == 'observation' and claims.get('category') == 'rights':
            rights = claims.get('rights') or {}
            by_hash[e['row']['hash']] = rights.get('unit_ref')
            if rights.get('status') == 'active':
                active[rights['unit_ref']] = e['row']['hash']
            else:
                active.pop(rights.get('unit_ref'), None)
        elif receipt.get('kind') == 'revocation':
            target = by_hash.get(claims.get('target_ref'))
            if target and active.get(target) == claims.get('target_ref'):
                active.pop(target, None)
    return active


async def verified_artefacts(db_, scope):
    """Every sealed artefact the requester may see that is complete, independently verified, terminal `ready`
    and carries current rights. Metadata only; no bytes."""
    events = await events_for(db_, scope)
    by_run = {}
    for e in events:
        by_run.setdefault(e['row']['run_id'], []).append(e)
    rights = _active_rights(await read_events(db_, {'row.tenant_id': scope['tenant_id'], 'row.resource_type': RECEIPTS}))
    out = []
    for items in by_run.values():
        try:
            request = snapshot(items, scope)
        except ValueError:
            continue
        if request is None:
            continue
        rows = await LedgerJournal(db_).read(request)
        registry = next((r for r in rows if r['slot'] == 'registry'), None)
        terminal = next((r for r in reversed(rows) if r['slot'] == 'terminal'), None)
        if registry is None or terminal is None or terminal['data'].get('phase') != 'ready':
            continue
        sealed = await objects.lookup(db_, request)
        if not sealed or not sealed.get('object') or sealed.get('state') != 'complete':
            continue
        order, _ = await packaging.load(db_, request)
        selection = (order or {}).get('selection') or {}
        for artifact in sealed.get('artifacts', []):
            if artifact['ref'] not in rights:
                continue
            out.append({'artifact_ref': artifact['ref'], 'sha256': artifact['sha256'], 'size_bytes': artifact['size_bytes'],
                        'class_label': artifact.get('class_label'), 'request_id': request.request_id,
                        'runtime_id': sealed['runtime_id'], 'object': sealed['object'],
                        'region': f"{selection.get('database')}.{selection.get('table')}", 'source_id': selection.get('source_id'),
                        'columns': list(selection.get('columns') or []), 'units': (sealed.get('quality') or {}).get('qualified_units'),
                        'rights_receipt_ref': rights[artifact['ref']], 'inspection_ref': registry['data'].get('inspection_ref'),
                        'terminal_reason': terminal['data'].get('reason_code'), 'scope_refs': list(request.scope_refs)})
    return sorted(out, key=lambda a: (a['region'], a['request_id']))


def qualified_set_ref(artefacts):
    """One hash naming the exact qualified set an answer was allowed to read."""
    body = '|'.join(f"{a['artifact_ref']}:{a['sha256']}:{a['rights_receipt_ref']}" for a in artefacts)
    return hashlib.sha256(body.encode()).hexdigest()


async def read_candidates(db_, scope, artefacts, terms, pinned=()):
    """Bounded whole-unit read from the qualified store on the admitted runtime. Zero source reads."""
    if not artefacts:
        return {'candidates': [], 'calls': 0, 'qualified_bytes_read': 0, 'matched_total': 0, 'units_total': 0, 'failures': []}
    custody = await latest(db_, scope['tenant_id'], 'custody_descriptor', 'default')
    if custody is None:
        raise Held('CUSTODY_DESCRIPTOR_UNRESOLVED')
    secrets = {'object_store': object_store_secrets(scope['tenant_id'], custody['payload']['record'])}

    async def one(artefact):
        descriptor = await runtime_by_id(db_, scope['tenant_id'], artefact['runtime_id'])
        control = {'mode': 'unit_select', 'tenant_id': scope['tenant_id'], 'request_id': artefact['request_id'],
                   'artifact': {'key': artefact['object']['key'], 'sha256': artefact['sha256'], 'size_bytes': artefact['size_bytes']},
                   'terms': list(terms), 'unit_ids': [p for p in pinned if p.startswith(unit_ref(scope['tenant_id'], artefact['request_id'], ''))],
                   'max_candidates': MAX_CANDIDATES, 'max_neighbours': MAX_NEIGHBOURS, 'secrets': secrets}
        control['unit_ids'] = [u.rsplit('/', 1)[-1] for u in control['unit_ids']]
        try:
            value = await remote.call_async(descriptor, control, deadline_seconds=CALL_SECONDS)
        except (Held, TimeoutError, OSError) as exc:
            return artefact, {'status': 'failed', 'reason_code': getattr(exc, 'reason_code', type(exc).__name__)}
        return artefact, value

    results = await asyncio.gather(*(one(a) for a in artefacts))
    candidates, failures, bytes_read, matched_total, units_total = [], [], 0, 0, 0
    for artefact, value in results:
        if value.get('status') != 'complete':
            failures.append({'artifact_ref': artefact['artifact_ref'], 'reason_code': value.get('reason_code', 'RUNTIME_CALL_FAILED')})
            continue
        bytes_read += value.get('bytes_read', 0)
        matched_total += value.get('matched_total', 0)
        units_total += value.get('units_total', 0)
        for c in value['candidates']:
            unit = c['unit']
            candidates.append({'ref': unit_ref(scope['tenant_id'], artefact['request_id'], unit['unit_id']), 'unit_id': unit['unit_id'],
                               'unit': unit, 'position': c['position'], 'overlap': c['overlap'], 'kind': c['kind'],
                               'rel_keys': c.get('rel_keys', []), 'content_sha256': c['content_sha256'],
                               'region': artefact['region'], 'artifact_ref': artefact['artifact_ref'], 'request_id': artefact['request_id'],
                               'class_label': (unit.get('defensibility') or {}).get('defensibility_class', 'utterance'),
                               'reextraction_ref': f"akki://reextract/{scope['tenant_id']}/{artefact['request_id']}/{unit['unit_id']}"})
    return {'candidates': candidates, 'calls': len(results), 'qualified_bytes_read': bytes_read, 'matched_total': matched_total,
            'units_total': units_total, 'failures': failures}


async def chat_plane(scope):
    """One memory plane per requester per application; isolation by construction (scoped accessor)."""
    key = f"chat:{scope['tenant_id']}:{scope['principal_id']}"
    doc = await db[MEMORY_PLANE_COLLECTION].find_one({'issued_to_integration_key': key, 'tenant_id': scope['tenant_id'], 'state': 'active'})
    plane_id = doc['plane_id'] if doc else (await plane_registry.issue_plane(
        integration_key=key, tenant_id=scope['tenant_id'], retrieval_scope=f"tenant:{scope['tenant_id']}:qualified_units")).plane_id
    return await for_plane(plane_id=plane_id, integration_key=key)


async def touch_working_set(accessor, refs):
    """Record use of the served references; report hits (already hot) and misses; evict past the cap."""
    existing = {e['ref'] for e in await accessor.list_working_set()}
    hits = [r for r in refs if r in existing]
    for ref in refs:
        await working_set.record_use(accessor=accessor, ref=ref)
    evicted = await working_set.evict_by_halflife(accessor=accessor)
    return {'plane_id': accessor.plane_id, 'hits': len(hits), 'misses': len(refs) - len(hits), 'hot_refs_before': len(existing),
            'hot_refs_after': len(existing | set(refs)) - evicted, 'evicted': evicted}
