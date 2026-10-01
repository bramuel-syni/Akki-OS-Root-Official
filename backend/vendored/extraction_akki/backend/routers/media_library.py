"""Private media library. Metadata in Mongo, objects only in managed storage."""
import asyncio
import hashlib
import os
import tempfile
import uuid
from datetime import datetime,timedelta,timezone
from urllib.parse import quote

from fastapi import APIRouter,Depends,Header,HTTPException,Request
from fastapi.responses import StreamingResponse
from pymongo import ReturnDocument

from services.enforce.census_identity import census_identity
from services.watch import commission_gate
from services.training_lab import store as lab
from services.media_library import contracts as c,store,storage,formats,assessment

router=APIRouter(prefix='/api/media',tags=['file-media-storage'])
_transfers=asyncio.Semaphore(4)


def operator(actor):
    if not {'operator','master_admin'}.intersection(actor['roles']):
        raise HTTPException(403,'An admitted operator is required')


def row_for(actor,file_id):
    row=store.get(actor['tenant_id'],file_id)
    if not row: raise HTTPException(404,'File not found')
    return row


def live(row):
    if row['is_deleted']: raise HTTPException(410,'This file is archived')
    if row['rights_status']=='withdrawn': raise HTTPException(403,'Access is held because rights were withdrawn')
    if row['status']!='available': raise HTTPException(409,'This file has not finished uploading')


def unavailable(exc):
    messages={402:'Storage access is suspended',403:'Storage access is unavailable',439:'The storage provider quota is reached',404:'Stored file could not be retrieved'}
    return HTTPException(503,messages.get(exc.status,'Storage is temporarily unavailable. Please retry later.'))


@router.get('/config',response_model=c.Envelope)
def config(actor=Depends(census_identity)):
    ready,error=storage.ready()
    quota=store.db().media_quota.find_one({'tenant_id':actor['tenant_id']},{'_id':0}) or {}
    return {'tenant_id':actor['tenant_id'],'storage_ready':ready,'storage_error':error,
            'max_file_bytes':int(os.environ['MEDIA_MAX_FILE_BYTES']),'max_text_bytes':int(os.environ['MEDIA_MAX_TEXT_BYTES']),
            'max_batch_files':int(os.environ['MEDIA_MAX_BATCH_FILES']),'extensions':list(formats.FORMATS),
            'reserved_bytes':quota.get('reserved_bytes',0),'allowance_bytes':int(os.environ['MEDIA_TENANT_MAX_BYTES']),
            'hard_delete_supported':False,'direct_upload_supported':False,
            'retention_notice':'Archiving removes access in Akki. Stored bytes and previously downloaded copies are not erased.'}


@router.get('/files',response_model=c.Envelope)
def files(actor=Depends(census_identity)):
    rows=list(store.db().media_files.find({'tenant_id':actor['tenant_id']},{'_id':0}).sort('created_at',-1).limit(1001))
    return {'tenant_id':actor['tenant_id'],'files':[store.public(row) for row in rows[:1000]],'truncated':len(rows)>1000}


@router.post('/uploads',status_code=201,response_model=c.Envelope)
def prepare(body:c.Upload,idempotency_key:str=Header(...,min_length=8,max_length=100),actor=Depends(census_identity)):
    operator(actor)
    try:
        info=formats.describe(body.filename,body.size_bytes)
    except ValueError as exc: raise HTTPException(422,str(exc)) from exc
    try:
        old,digest=store.replay(actor['tenant_id'],idempotency_key,body.model_dump())
    except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    if old: return {'tenant_id':actor['tenant_id'],'file':store.public(old),'created':False}
    with commission_gate.crossing(actor,'media.upload',{'upload_key':idempotency_key,'filename':body.filename,'size_bytes':body.size_bytes}):
        try: row,new=store.create(actor,idempotency_key,body.model_dump(),info,digest)
        except ValueError as exc: raise HTTPException(409,str(exc)) from exc
        if new: store.audit(actor,'upload_reserved',row['file_id'],row['revision'])
    return {'tenant_id':actor['tenant_id'],'file':store.public(row),'created':new}


@router.put('/files/{file_id}/content',response_model=c.Envelope)
async def content(file_id:str,request:Request,actor=Depends(census_identity)):
    operator(actor); row=row_for(actor,file_id)
    if row['is_deleted']: raise HTTPException(410,'This file is archived')
    if row['status']=='available': return {'tenant_id':actor['tenant_id'],'file':store.public(row),'replayed':True}
    length=request.headers.get('content-length')
    if length is not None:
        try: valid=int(length)==row['size_bytes']
        except ValueError: valid=False
        if not valid: raise HTTPException(413,'Uploaded size does not match the reserved file')
    stamp=lab.now(); lease=uuid.uuid4().hex
    claimed=store.db().media_files.find_one_and_update({'tenant_id':actor['tenant_id'],'file_id':file_id,'is_deleted':False,
        '$or':[{'status':{'$in':['awaiting_upload','upload_failed']}},{'status':'uploading','upload_lease_until':{'$lt':stamp}}]},
        {'$set':{'status':'uploading','upload_token':lease,'upload_lease_until':(datetime.now(timezone.utc)+timedelta(minutes=10)).isoformat()}},
        projection={'_id':0},return_document=ReturnDocument.AFTER)
    if not claimed: raise HTTPException(409,'This upload is already in progress')
    query={'tenant_id':actor['tenant_id'],'file_id':file_id,'upload_token':lease}
    try:
        async with _transfers:
            with tempfile.SpooledTemporaryFile(max_size=1024*1024,mode='w+b') as temp:
                count=0; digest=hashlib.sha256()
                async for chunk in request.stream():
                    count+=len(chunk)
                    if count>row['size_bytes']: raise HTTPException(413,'The upload is larger than declared')
                    digest.update(chunk); temp.write(chunk)
                if count!=row['size_bytes'] or digest.hexdigest()!=row['sha256']:
                    raise HTTPException(422,'File size or checksum changed. Choose the original file and retry.')
                try: validation=formats.validate(temp,row['extension'])
                except ValueError as exc: raise HTTPException(422,str(exc)) from exc
                result=await asyncio.to_thread(storage.put,row['storage_path'],temp,row['content_type'])
                if int(result['size'])!=count: raise HTTPException(502,'Storage did not confirm the expected file size')
        saved=store.db().media_files.find_one_and_update(query,{'$set':{'status':'available','storage_path':result['path'],
            'format_validation':validation,'stored_at':lab.now(),'updated_at':lab.now()},'$unset':{'upload_token':'','upload_lease_until':''}},
            projection={'_id':0},return_document=ReturnDocument.AFTER)
        if not saved: raise HTTPException(409,'Upload state changed; refresh the library')
        store.audit(actor,'stored',file_id,saved['revision'],{'sha256':row['sha256'],'bytes':count})
        return {'tenant_id':actor['tenant_id'],'file':store.public(saved),'replayed':False}
    except BaseException as exc:
        store.db().media_files.update_one(query,{'$set':{'status':'upload_failed','updated_at':lab.now()},'$unset':{'upload_token':'','upload_lease_until':''}})
        if isinstance(exc,storage.StorageError): raise unavailable(exc) from exc
        raise


@router.get('/files/{file_id}/download')
def download(file_id:str,actor=Depends(census_identity)):
    row=row_for(actor,file_id); live(row)
    try: response=storage.download(row['storage_path'])
    except storage.StorageError as exc: raise unavailable(exc) from exc
    def stream():
        try:
            for chunk in response.iter_content(65536):
                if chunk: yield chunk
        finally: response.close()
    return StreamingResponse(stream(),media_type=row['content_type'],headers={
        'Content-Disposition':"attachment; filename*=UTF-8''"+quote(row['filename'],safe=''),
        'X-Content-Type-Options':'nosniff','Cache-Control':'private, no-store','Content-Length':str(row['size_bytes'])})


@router.patch('/files/{file_id}',response_model=c.Envelope)
def metadata(file_id:str,body:c.Metadata,actor=Depends(census_identity)):
    operator(actor); row=row_for(actor,file_id)
    if row['is_deleted']: raise HTTPException(410,'Archived metadata is read-only')
    if row['status']!='available': raise HTTPException(409,'Finish uploading before editing metadata')
    fields=body.model_dump(exclude={'revision'})
    if fields['rights_status']!='declared': fields['training_permission_confirmed']=False
    with commission_gate.crossing(actor,'media.metadata',{'file_id':file_id,**body.model_dump()}):
        updated=store.db().media_files.find_one_and_update({'tenant_id':actor['tenant_id'],'file_id':file_id,'is_deleted':False,'revision':body.revision},
            {'$set':{**fields,'updated_at':lab.now()},'$inc':{'revision':1}},projection={'_id':0},return_document=ReturnDocument.AFTER)
        if not updated: raise HTTPException(409,'File details changed. Refresh before saving again.')
        store.audit(actor,'metadata_updated',file_id,updated['revision'],{'rights_status':fields['rights_status']})
    return {'tenant_id':actor['tenant_id'],'file':store.public(updated)}


@router.post('/files/{file_id}/archive',response_model=c.Envelope)
def archive(file_id:str,body:c.Archive,actor=Depends(census_identity)):
    operator(actor); row=row_for(actor,file_id)
    if row['is_deleted']: return {'tenant_id':actor['tenant_id'],'file':store.public(row)}
    with commission_gate.crossing(actor,'media.archive',{'file_id':file_id,'revision':body.revision}):
        updated=store.db().media_files.find_one_and_update({'tenant_id':actor['tenant_id'],'file_id':file_id,'revision':body.revision,'status':{'$ne':'uploading'}},
            {'$set':{'is_deleted':True,'status':'archived','archived_at':lab.now(),'updated_at':lab.now()},'$inc':{'revision':1}},
            projection={'_id':0},return_document=ReturnDocument.AFTER)
        if not updated: raise HTTPException(409,'File changed or is uploading. Refresh before archiving.')
        store.audit(actor,'archived_access_revoked',file_id,updated['revision'],{'physical_deletion':False})
    return {'tenant_id':actor['tenant_id'],'file':store.public(updated)}


@router.post('/assessments',status_code=201,response_model=c.Envelope)
def assess(body:c.Selection,idempotency_key:str=Header(...,min_length=8,max_length=100),actor=Depends(census_identity)):
    operator(actor)
    if actor['tenant_id']!='RMS': raise HTTPException(403,'Training-lab dataset assessments are currently RMS-scoped')
    data={'title':body.title,'file_ids':sorted(set(body.file_ids)),'model_reviews':False}
    try: old=lab.replay(actor['tenant_id'],idempotency_key,data)
    except ValueError as exc: raise HTTPException(409,str(exc)) from exc
    if old: return {'tenant_id':actor['tenant_id'],'run':lab.public(old),'created':False}
    rows=[row_for(actor,key) for key in data['file_ids']]
    for row in rows: live(row)
    report=assessment.snapshot(rows)
    with commission_gate.crossing(actor,'media.assess',data):
        run,new=lab.enqueue(actor['tenant_id'],actor['principal_id'],idempotency_key,data,kind='dataset_readiness',dataset_assessment=report)
    return {'tenant_id':actor['tenant_id'],'run':lab.public(run),'created':new}


@router.get('/assessments',response_model=c.Envelope)
def assessments(actor=Depends(census_identity)):
    rows=lab.db().training_lab_runs.find({'tenant_id':actor['tenant_id'],'kind':'dataset_readiness'},{'_id':0}).sort('created_at',-1).limit(20)
    return {'tenant_id':actor['tenant_id'],'runs':[lab.public(row) for row in rows]}