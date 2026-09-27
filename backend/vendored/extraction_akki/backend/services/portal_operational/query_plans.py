import asyncio
import json
from services.activation.receipts import RESOURCE
from services.activation.record_shapes import Plan
from services.northena.execution_builders import skill_request
from services.northena.execution_models import Held


async def resolve(runtime, scope, intent, provisioning):
    if runtime is None:
        raise Held('SKILL_EXECUTOR_UNADMITTED')
    from services.portal_operational.query_intents import require_current_provisioning
    require_current_provisioning(intent, provisioning)
    async def lookup():
        receipts = runtime.receipts
        events = await receipts.events()
        plans = [e for e in events if e['row']['resource_type'] == RESOURCE
                 and e['payload'].get('receipt', {}).get('kind') == 'plan'
                 and e['payload']['receipt'].get('claims', {}).get('request', {}).get('request_id') == intent['row']['run_id']]
        if len(plans) != 1:
            raise Held('SKILL_NATIVE_PLAN_REQUIRED')
        receipt = await receipts.resolve(plans[0]['row']['hash'], kind='plan', events=events)
        plan = Plan.model_validate_json(json.dumps(receipt.claims))
        request = plan.request
        if not request.input_refs:
            raise Held('SKILL_NATIVE_PLAN_MISMATCH')
        expected = skill_request(provisioning, request_id=intent['row']['run_id'],
            tenant_id=scope['tenant_id'], principal_id=scope['principal_id'], query_ref=request.input_refs[-1],
            query_sha256=intent['payload']['query_sha256'], deadline_epoch=request.deadline_epoch)
        if request != expected or receipt.request_sha256 != request.digest():
            raise Held('SKILL_NATIVE_PLAN_MISMATCH')
        return request
    try:
        return await asyncio.wait_for(lookup(), runtime.evidence_timeout_seconds)
    except (TimeoutError, ConnectionError, OSError):
        raise Held('SKILL_PLAN_LOOKUP_UNAVAILABLE') from None
    except (ValueError, KeyError, TypeError, AttributeError):
        raise Held('SKILL_NATIVE_PLAN_INVALID') from None