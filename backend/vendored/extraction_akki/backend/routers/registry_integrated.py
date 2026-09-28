"""M1 tenant-scoped consumers of the existing census and Registry lifecycle."""
import json
from fastapi import APIRouter,Body,Depends,HTTPException
from pydantic import BaseModel,ConfigDict
from services.enforce.census_identity import census_identity
from services.census_autonomy import operational_reads as reads,operational_store as store
from services.census_autonomy.registry_surfaces import inventory,conversations

router=APIRouter(tags=['integrated-registry'])
class Envelope(BaseModel):
    model_config=ConfigDict(extra='allow')
    tenant_id:str

@router.get('/api/portal/census/descriptors',response_model=Envelope)
def descriptors(actor=Depends(census_identity)):
    from services.census_autonomy.registry_durability import evidence_rows
    return {'tenant_id':actor['tenant_id'],'descriptors':evidence_rows(actor['tenant_id'],'source_descriptor')}

@router.post('/api/portal/census/connections',response_model=Envelope)
def connect(body:dict=Body(...),actor=Depends(census_identity)):
    if not {'operator','master_admin'}.intersection(actor['roles']): raise HTTPException(403,'An estate operator is required.')
    if set(body)-{'source_id','name'}: raise HTTPException(422,'Connection uses existing credential custody; do not submit raw credentials.')
    from services.census_autonomy.descriptor_contracts import bind_existing
    try: descriptor,created=bind_existing(actor['tenant_id'],body.get('source_id'),body.get('name'),actor['principal_id'])
    except ValueError as exc: raise HTTPException(422,str(exc)) from exc
    return {'tenant_id':actor['tenant_id'],'connection':descriptor,'created':created,'status':'DECLARED',
            'next_action':'Commission the read-only census to measure access. Declaration is not a successful connection or native admission.'}

@router.get('/api/portal/census/sources',response_model=Envelope)
def sources(actor=Depends(census_identity)):
    from services.census_autonomy.registry_surfaces import source_summary
    return {'tenant_id':actor['tenant_id'],'sources':[source_summary(s) for s in inventory(actor['tenant_id'],reads.records(actor['tenant_id']))['source_details']]}

@router.get('/api/portal/census/sources/{source_ref}',response_model=Envelope)
def source(source_ref:str,actor=Depends(census_identity)):
    item=next((s for s in inventory(actor['tenant_id'],reads.records(actor['tenant_id']))['source_details'] if s['source_ref']==source_ref),None)
    if not item: raise HTTPException(404,'No such source in your tenant.')
    return {'tenant_id':actor['tenant_id'],'source':item}

@router.get('/api/portal/census/compute',response_model=Envelope)
def compute(actor=Depends(census_identity)):
    return {'tenant_id':actor['tenant_id'],'workers':inventory(actor['tenant_id'],reads.records(actor['tenant_id']))['compute_resources']}

@router.post('/api/portal/census/compute/refresh',response_model=Envelope)
def refresh_compute(actor=Depends(census_identity)):
    if not {'operator','master_admin'}.intersection(actor['roles']): raise HTTPException(403,'An estate operator is required.')
    from services.census_autonomy.worker_inventory import refresh
    return {'tenant_id':actor['tenant_id'],'workers':refresh(actor['tenant_id'])}

@router.get('/api/portal/census/conversations',response_model=Envelope)
def conversation_list(actor=Depends(census_identity)):
    return {'tenant_id':actor['tenant_id'],'items':conversations(actor['tenant_id'])}

@router.post('/api/portal/census/conversations/reconcile',response_model=Envelope)
def reconcile_conversations(actor=Depends(census_identity)):
    if not {'operator','master_admin'}.intersection(actor['roles']): raise HTTPException(403,'An estate operator is required.')
    from services.census_autonomy.deep_response import publish
    from services.census_autonomy.operational_runner import admission_path
    _,digest=admission_path()
    created=[]
    for run in store.runs(actor['tenant_id']):
        if run.get('outcomes'): created.extend(publish(run,digest))
    return {'tenant_id':actor['tenant_id'],'created':len(created),'items':conversations(actor['tenant_id'])}

@router.post('/api/portal/census/conversations/{item_id}/resolve',response_model=Envelope)
def resolve(item_id:str,body:dict=Body(...),actor=Depends(census_identity)):
    if not {'operator','master_admin'}.intersection(actor['roles']): raise HTTPException(403,'An estate operator is required.')
    item=next((i for i in conversations(actor['tenant_id']) if i['item_id']==item_id),None)
    if not item: raise HTTPException(404,'No such response item in your tenant.')
    text=body.get('resolution_text'); state=body.get('state')
    if set(body)-{'resolution_text','state'} or not isinstance(text,str) or not 1<=len(text.strip())<=2000 or state not in {'RESOLVED_ACCEPTED','RESOLVED_REJECTED'}:
        raise HTTPException(422,'Provide a resolution and its accepted/rejected disposition.')
    from services.census_autonomy.response_required_queue import resolve_response_required_item
    with store.lock('response:'+item_id):
        current=next(i for i in conversations(actor['tenant_id']) if i['item_id']==item_id)
        if current['state']!='PENDING':
            if current['resolution_text']!=text.strip() or current['state']!=state:
                raise HTTPException(409,'This response was already resolved; its history cannot be rewritten.')
            resolved=current
        else:
            resolved=resolve_response_required_item(item_id=item_id,resolver_id=actor['principal_id'],resolution_text=text.strip(),resolved_state=state)
            from services.census_autonomy.registry_durability import collection
            from services.mtafiti.asset_registry_writer import append_census_evidence
            collection(); append_census_evidence('census-response:'+actor['tenant_id']+':'+item_id,actor['tenant_id'],{'kind':'census_response','item':resolved})
    return {'tenant_id':actor['tenant_id'],'item':resolved,'resume_status':'Recorded. A terminal historical run is preserved; commission a successor to verify the changed source.'}