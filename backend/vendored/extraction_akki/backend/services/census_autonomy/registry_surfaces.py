"""Registry consumers of retained evidence, never estate readers."""
from services.census_autonomy.registry_durability import evidence_rows

def source_summary(source):
    summary={k:v for k,v in source.items() if k not in {'composition','profile','relationships'}}
    if source.get('sample'):
        summary['sample']={k:v for k,v in source['sample'].items() if k!='table_samples'}
    summary['relationship_count']=len(source.get('relationships',[]))
    summary['details_available']=True
    return summary

def record_summary(record):
    return {**run_summary(record),'source_details':[source_summary(s) for s in record.get('source_details',[])]}

def run_summary(row):
    return {**row,'outcomes':[{**o,'sources':[source_summary(s) for s in o.get('sources',[])]} for o in row.get('outcomes',[])]}

def inventory(tenant,records):
    sources={}; workers={}
    for record in records:
        for source in record.get('source_details',[]):
            key=source['source_ref']
            if key not in sources:
                sources[key]={**source,'record_id':record['record_id'],'proof_ref':record.get('proof_ref'),
                              'sensitivity':'unmeasured','rights_status':'Census authority only; further use is not established'}
            elif sources[key].get('status')=='blocked' and source.get('status') in ('complete','partial') and 'last_good' not in sources[key]:
                sources[key]['last_good']={'record_id':record['record_id'],'observed_at':source['observed_at'],
                                          'volume_bytes':source.get('volume_bytes'),'proof_ref':record.get('proof_ref')}
                sources[key]['freshness']='stale; latest measurement failed'
        for worker in record.get('workers',[]):
            workers.setdefault(worker['runtime_id'],{**worker,'record_id':record['record_id']})
    for evidence in sorted(evidence_rows(tenant,'worker_inventory'),key=lambda e:e['observed_at'],reverse=True):
        workers.setdefault(evidence['worker']['runtime_id'],evidence['worker'])
    from services.model_registry.registry import current_registry_version
    version,registered=current_registry_version()
    models=[]
    for key,value in registered.items():
        # The registry is an inventory, not a blanket operational admission.
        if value.get('tenant_id') not in (None,tenant): continue
        models.append({'model_id':key,'name':value.get('display_name') or key,'registry_version':version,
                       'provider':value.get('provider'),'licence':value.get('license') or value.get('licence'),
                       'model_hash':value.get('sha256') or value.get('model_hash'),
                       'provenance':value.get('provenance'),'status':'Registered; runtime qualification not established here'})
    return {'source_details':list(sources.values()),'compute_resources':list(workers.values()),'llm_backends':models}

def conversations(tenant,run_id=None):
    import json
    from services.census_autonomy.response_required_queue import RESPONSE_REQUIRED_DIR
    items={}; metadata={}
    for path in RESPONSE_REQUIRED_DIR.glob('*.json'):
        try: value=json.loads(path.read_text())
        except (OSError,ValueError): continue
        if value.get('tenant_id')==tenant and (not run_id or value.get('census_run_id')==run_id): items[value['item_id']]=value
    for evidence in evidence_rows(tenant,'census_response'):
        value=evidence['item']
        metadata.setdefault(value['item_id'],{}).update({k:evidence[k] for k in ('source_id','host_label','reason_code') if k in evidence})
        if (not run_id or value.get('census_run_id')==run_id):
            current=items.get(value['item_id'])
            if not current or value['state']!='PENDING': items[value['item_id']]=value
    from services.census_autonomy.census_dq_producer import _field
    projected=[]
    for value in items.values():
        text=value.get('reason_text','')
        extra={'source_id':_field(text,'source=') or 'unrecorded','host_label':_field(text,'host=') or 'Source scope',
               'reason_code':_field(text,'census_reason=') or value.get('refusal_code'),**metadata.get(value['item_id'],{})}
        projected.append({**value,**extra,'message':text,'resolved_by':value.get('resolver_id')})
    return sorted(projected,key=lambda r:r.get('banked_at_utc',''))