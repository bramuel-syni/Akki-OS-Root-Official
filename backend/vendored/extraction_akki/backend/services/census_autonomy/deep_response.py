"""Connect genuine failed source observations to the existing response queue."""
import json
from services.census_autonomy import operational_store as store
from services.census_autonomy.registry_surfaces import conversations
from services.census_autonomy.census_dq_producer import _action_for
from services.census_autonomy.response_required_queue import bank_response_required_item,RESPONSE_REQUIRED_DIR
from services.census_autonomy.registry_durability import collection
from services.mtafiti.asset_registry_writer import append_census_evidence

def publish(run,lawful_hash):
    from services.mtafiti.asset_registry_writer import persistence_enabled
    if not persistence_enabled(): return []
    collection()
    with store.lock('responses:'+run['census_run_id']):
        known={(v['source_id'],v['host_label']) for v in conversations(run['tenant_id'],run['census_run_id'])}
        added=[]
        for outcome in run.get('outcomes',[]):
            failed=[s for s in outcome.get('sources',[]) if s['status']=='blocked']
            # A bucket the key may list but not read is an owner-answerable gap of the full-content census, banked once per bucket.
            failed+=[{**s,'reason_code':s['content_reason_code']} for s in outcome.get('sources',[]) if s.get('content_reason_code') and s['status']!='blocked']
            if outcome['status']=='blocked' and not failed:
                failed=[{'label':outcome['source_id'],'reason_code':outcome.get('reason_code','WORKER_UNAVAILABLE')}]
            failures=[{'host_label':s['label'],'reason_code':s.get('reason_code','SOURCE_CHECK_INCOMPLETE')} for s in failed if (outcome['source_id'],s['label']) not in known]
            if not failures: continue
            for failure in failures:
                reason=_action_for(failure['reason_code'],failure['host_label'])
                identity=bank_response_required_item(census_run_id=run['census_run_id'],tenant_id=run['tenant_id'],
                    reason_text=reason,refusal_code='BLOCKED_SURFACE_UNREACHABLE',decision_timestamp_utc=store.now())
                item=json.loads((RESPONSE_REQUIRED_DIR/(identity+'.json')).read_text())
                evidence={'kind':'census_response','item':item,'source_id':outcome['source_id'],
                          'host_label':failure['host_label'],'reason_code':failure['reason_code'],'lawful_basis_sha256':lawful_hash}
                append_census_evidence('census-response-origin:'+run['tenant_id']+':'+identity,run['tenant_id'],evidence)
                added.append(item)
        return added