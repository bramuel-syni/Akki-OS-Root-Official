"""Mongo durable queue: tenant-qualified idempotency and compare-and-set leases."""
import hashlib
import json
import os
import uuid
from datetime import datetime, timedelta, timezone
from functools import lru_cache

from pymongo import MongoClient, ReturnDocument
from pymongo.errors import DuplicateKeyError


def now():
    return datetime.now(timezone.utc).isoformat()


@lru_cache(maxsize=1)
def db():
    database = MongoClient(os.environ['MONGO_URL'])[os.environ['DB_NAME']]
    database.training_lab_runs.create_index([('tenant_id',1),('idempotency_key',1)],unique=True)
    database.training_lab_runs.create_index('run_id',unique=True)
    database.training_lab_runs.create_index([('tenant_id',1),('request.source_assessment',1)],unique=True,
        partialFilterExpression={'kind':'research_followup'})
    database.training_lab_runs.create_index([('status',1),('lease_until',1)])
    database.training_lab_webhooks.create_index('run_id',unique=True)
    database.training_lab_watch.create_index('tenant_id',unique=True)
    return database


def enqueue(tenant,actor,key,request,*,kind='assessment',evidence=None):
    fingerprint = hashlib.sha256(json.dumps(request,sort_keys=True).encode()).hexdigest()
    row = {'run_id':'lab-'+uuid.uuid4().hex[:16],'tenant_id':tenant,'actor':actor,'idempotency_key':key,
           'request_hash':fingerprint,'request':request,'kind':kind,'title':request.get('title','Training checkpoint review'),
           'status':'queued','created_at':now(),'updated_at':now(),'attempts':0,
           'training_authorized':False,'training_started':False,'model_admission':'not_requested'}
    if evidence is not None:
        row['evidence'] = evidence
    try:
        db().training_lab_runs.insert_one(dict(row))
        return row,True
    except DuplicateKeyError:
        old = db().training_lab_runs.find_one({'tenant_id':tenant,'idempotency_key':key},{'_id':0})
        if old is None:
            raise ValueError('A follow-up review already exists for this assessment')
        if old['request_hash'] != fingerprint:
            raise ValueError('Idempotency key already belongs to a different request')
        return old,False


def get(tenant,run_id):
    return db().training_lab_runs.find_one({'tenant_id':tenant,'run_id':run_id},{'_id':0})


def replay(tenant,key,request):
    row = db().training_lab_runs.find_one({'tenant_id':tenant,'idempotency_key':key},{'_id':0})
    if row and row['request_hash'] != hashlib.sha256(json.dumps(request,sort_keys=True).encode()).hexdigest():
        raise ValueError('Idempotency key already belongs to a different request')
    return row


def public(row):
    return {k:v for k,v in row.items() if k not in {'_id','actor','idempotency_key','request_hash','lease_token','lease_until'}}


def claim(tenant='RMS'):
    stamp = now()
    # A lost dispatch ACK is not safe to replay; reconcile rather than launch again.
    db().training_lab_runs.update_many({'tenant_id':tenant,'status':'dispatching','lease_until':{'$lt':stamp}},
        {'$set':{'status':'held','hold_reason':'Remote dispatch outcome uncertain; operator reconciliation required','updated_at':stamp}})
    db().training_lab_runs.update_many({'tenant_id':tenant,'status':'reviewing','lease_until':{'$lt':stamp}},
        {'$set':{'status':'held','hold_reason':'Review interrupted; no automatic repeated provider spend','updated_at':stamp}})
    token = uuid.uuid4().hex
    return db().training_lab_runs.find_one_and_update(
        {'tenant_id':tenant,'status':{'$in':['queued','inspecting']},'$or':[{'lease_until':{'$exists':False}},{'lease_until':{'$lt':stamp}}]},
        {'$set':{'lease_token':token,'lease_until':(datetime.now(timezone.utc)+timedelta(minutes=10)).isoformat()},'$inc':{'attempts':1}},
        projection={'_id':0},sort=[('created_at',1)],return_document=ReturnDocument.AFTER)


def update(row,**fields):
    fields['updated_at'] = now()
    result = db().training_lab_runs.update_one({'run_id':row['run_id'],'tenant_id':row['tenant_id'],'lease_token':row['lease_token']},{'$set':fields})
    if result.matched_count != 1:
        raise RuntimeError('Lab lease lost')
    row.update(fields)


def release(row):
    db().training_lab_runs.update_one({'run_id':row['run_id'],'lease_token':row['lease_token']},{'$unset':{'lease_until':'','lease_token':''}})