import hashlib
import os
import uuid
from functools import lru_cache

from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError
from services.training_lab import store as lab


@lru_cache(maxsize=1)
def db():
    database=lab.db()
    database.media_files.create_index([('tenant_id',1),('upload_key',1)],unique=True)
    database.media_files.create_index('file_id',unique=True)
    database.media_files.create_index([('tenant_id',1),('created_at',-1)])
    database.media_quota.create_index('tenant_id',unique=True)
    return database


def public(row):
    return {k:v for k,v in row.items() if k not in {'_id','storage_path','upload_key','request_hash','uploaded_by','upload_lease_until','upload_token'}}


def get(tenant,file_id):
    return db().media_files.find_one({'tenant_id':tenant,'file_id':file_id},{'_id':0})


def replay(tenant,key,body):
    import json
    digest=hashlib.sha256(json.dumps(body,sort_keys=True).encode()).hexdigest()
    row=db().media_files.find_one({'tenant_id':tenant,'upload_key':key},{'_id':0})
    if row and row['request_hash']!=digest: raise ValueError('This upload key belongs to a different file')
    return row,digest


def create(actor,key,body,info,digest):
    tenant=actor['tenant_id']; size=body['size_bytes']; database=db()
    database.media_quota.update_one({'tenant_id':tenant},{'$setOnInsert':{'reserved_bytes':0}},upsert=True)
    quota=database.media_quota.find_one_and_update({'tenant_id':tenant,'reserved_bytes':{'$lte':int(os.environ['MEDIA_TENANT_MAX_BYTES'])-size}},
        {'$inc':{'reserved_bytes':size}},projection={'_id':0},return_document=ReturnDocument.AFTER)
    if quota is None: raise ValueError('The media storage allowance is reached, including archived files')
    file_id=uuid.uuid4().hex
    namespace=hashlib.sha256(tenant.encode()).hexdigest()[:24]
    row={**info,'file_id':file_id,'tenant_id':tenant,'upload_key':key,'request_hash':digest,
         'storage_path':f"{os.environ['MEDIA_STORAGE_APP']}/{namespace}/{file_id}{info['extension']}",
         'size_bytes':size,'sha256':body['sha256'],'status':'awaiting_upload','is_deleted':False,'revision':1,
         'created_at':lab.now(),'updated_at':lab.now(),'uploaded_by':actor['principal_id'],
         'storage_permission_confirmed':True,'language':'','event_label':'unknown','label_status':'unreviewed',
         'rights_status':'pending','rights_basis':'','rights_reference':'','training_permission_confirmed':False,
         'rights_independently_verified':False}
    try: database.media_files.insert_one(dict(row))
    except Exception as exc:
        database.media_quota.update_one({'tenant_id':tenant},{'$inc':{'reserved_bytes':-size}})
        if isinstance(exc,DuplicateKeyError):
            return replay(tenant,key,body)[0],False
        raise
    return row,True


def audit(actor,action,file_id,revision,details=None):
    db().media_events.insert_one({'tenant_id':actor['tenant_id'],'actor':actor['principal_id'],
        'action':action,'file_id':file_id,'revision':revision,'at':lab.now(),'details':details or {}})