"""Use the existing execution spine; no in-pod query, source read or answer generation."""
import asyncio
from services.northena.execution_bindings import build_coordinator
from services.northena.execution_models import Held
from services.portal_operational import query_intents, query_plans, query_evidence
from services.portal_operational.hold_reasons import public_reason


async def advance(db, scope, skill_id, query_id, provisioning, runtime):
    rows = await query_intents.events(db, scope, skill_id, query_id)
    intent = rows[0]
    try:
        request = await query_plans.resolve(runtime, scope, intent, provisioning)
        coordinator = build_coordinator(db, runtime.bindings)
        await coordinator.authority.authorize(request, 'retrieve')
        refusal = await asyncio.wait_for(query_evidence.refusal(runtime.receipts, request, intent), runtime.evidence_timeout_seconds)
        if refusal is not None:
            recorded = await coordinator.journal.read(request)
            if any(r['slot'] in {'registry', 'terminal'} and r['data'].get('phase', 'ready') == 'ready' for r in recorded):
                raise Held('SKILL_OUTCOME_CONFLICT')
            view = refusal
        else:
            result = await coordinator.advance(request)
            if not result.execution_verified:
                code = public_reason(result.reason_code).code
                view = {'outcome': 'running' if result.phase == 'running' else 'held', 'reason_code': code,
                        'execution_verified': False, 'delivery_verified': False}
            else:
                view = await asyncio.wait_for(query_evidence.grounding(runtime, coordinator, request), runtime.evidence_timeout_seconds)
                await coordinator.release_gates(request, 'retrieve')
    except Held as exc:
        code = public_reason(exc.reason_code).code
        view = {'outcome': 'held', 'reason_code': code, 'execution_verified': False, 'delivery_verified': False}
    except (TimeoutError, ConnectionError, OSError):
        view = {'outcome': 'held', 'reason_code': 'SKILL_NATIVE_VERIFICATION_UNAVAILABLE', 'execution_verified': False, 'delivery_verified': False}
    except (ValueError, KeyError, TypeError):
        view = {'outcome': 'held', 'reason_code': 'SKILL_NATIVE_EVIDENCE_INVALID', 'execution_verified': False, 'delivery_verified': False}
    await query_intents.record_view(db, scope, intent, view)
    return query_intents.status(await query_intents.events(db, scope, skill_id, query_id))


async def current_status(db, scope, skill_id, query_id, provisioning, runtime):
    """GET never executes a workload; prior verification is not a current release grant."""
    rows = await query_intents.events(db, scope, skill_id, query_id)
    query_intents.require_current_provisioning(rows[0], provisioning)
    historical = query_intents.status(rows)
    if historical['outcome'] not in {'ready', 'refused'}:
        return historical
    try:
        request = await query_plans.resolve(runtime, scope, rows[0], provisioning)
        coordinator = build_coordinator(db, runtime.bindings)
        await coordinator.authority.authorize(request, 'retrieve')
        if historical['outcome'] == 'refused':
            checked = await asyncio.wait_for(query_evidence.refusal(runtime.receipts, request, rows[0]), runtime.evidence_timeout_seconds)
            if checked is None:
                raise Held('SKILL_REFUSAL_NOT_PROVED')
        else:
            result = await coordinator.retrieve(request)
            if not result.execution_verified:
                raise Held(result.reason_code)
            checked = await asyncio.wait_for(query_evidence.grounding(runtime, coordinator, request), runtime.evidence_timeout_seconds)
        return {**historical, **checked}
    except Held as exc:
        code = public_reason(exc.reason_code).code
    except (TimeoutError, ConnectionError, OSError):
        code = 'SKILL_NATIVE_VERIFICATION_UNAVAILABLE'
    except (ValueError, KeyError, TypeError):
        code = 'SKILL_NATIVE_EVIDENCE_INVALID'
    return {k: v for k, v in historical.items() if k in {'query_id', 'skill_id', 'query_sha256', 'intent_receipt_ref', 'history'}} | {
        'outcome': 'held', 'reason_code': code, 'execution_verified': False, 'delivery_verified': False}