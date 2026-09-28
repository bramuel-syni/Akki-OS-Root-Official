"""Durable custody/hydration adapter to the existing canonical Registry writer."""
import hashlib
import json
import os
from functools import lru_cache
from pathlib import Path
from pymongo import MongoClient
from contracts.asset_registry import ASSET_REGISTRY_COLLECTION
from services.mtafiti import asset_registry_writer as writer
from services.census_autonomy import engine

@lru_cache(maxsize=1)
def collection():
    client=MongoClient(os.environ['MONGO_URL'],serverSelectionTimeoutMS=5000)
    value=client[os.environ['DB_NAME']][ASSET_REGISTRY_COLLECTION]
    writer.configure_persistence(value)
    return value

def preserve_result(path):
    collection()
    doc=json.loads(Path(path).read_text())
    return writer.append_census_evidence('census-result:'+doc['tenant_id']+':'+doc['census_run_id'],doc['tenant_id'],
                                         {'kind':'census_result','filename':Path(path).name,'result':doc,'raw_json':Path(path).read_text()})

def restore_results(tenant):
    root=engine.CENSUS_STATE_DIR/engine.RESULTS_SUBDIR; root.mkdir(parents=True,exist_ok=True)
    for summary in collection().find({'tenant_id':tenant,'census_evidence.kind':'census_result'},
          {'_id':0,'asset_ref':1,'census_evidence.filename':1}):
        name=summary['census_evidence']['filename']
        if Path(name).name!=name: raise ValueError('Invalid retained result name')
        if (root/name).exists(): continue
        document=next(iter(collection().find({'asset_ref':summary['asset_ref']},{'_id':0})))
        evidence=document['census_evidence']
        digest=hashlib.sha256(json.dumps(evidence,sort_keys=True,default=str).encode()).hexdigest()
        if digest!=document['evidence_sha256']: raise ValueError('Durable census evidence mismatch')
        if json.loads(evidence['raw_json']).get('tenant_id')!=tenant: raise ValueError('Retained result tenant mismatch')
        name=evidence['filename']
        if Path(name).name!=name: raise ValueError('Invalid retained result name')
        path=root/name
        if not path.exists():
            temporary=path.with_suffix('.restore.tmp')
            temporary.write_text(evidence['raw_json'])
            temporary.replace(path)

def evidence_rows(tenant,kind):
    rows=[]
    for doc in collection().find({'tenant_id':tenant,'census_evidence.kind':kind},{'_id':0,'census_evidence':1,'evidence_sha256':1}):
        digest=hashlib.sha256(json.dumps(doc['census_evidence'],sort_keys=True,default=str).encode()).hexdigest()
        if digest!=doc.get('evidence_sha256'): raise ValueError('Registry evidence integrity check failed')
        rows.append(doc['census_evidence'])
    return rows


def preserve_cursor(doc):
    if not writer.persistence_enabled(): return
    digest=hashlib.sha256(json.dumps(doc,sort_keys=True,default=str).encode()).hexdigest()
    writer.append_census_evidence('census-cursor:'+doc['tenant_id']+':'+doc['census_run_id']+':'+digest,
                                 doc['tenant_id'],{'kind':'census_cursor','cursor':doc})


def restore_cursors(tenant,root):
    if not writer.persistence_enabled(): return
    seen=set()
    docs=collection().find({'tenant_id':tenant,'census_evidence.kind':'census_cursor'},
                           {'_id':0,'asset_ref':1,'census_evidence.cursor.census_run_id':1,'census_evidence.cursor.updated_at':1}).sort('census_evidence.cursor.updated_at',-1)
    for summary in docs:
        run_id=summary['census_evidence']['cursor']['census_run_id']
        if run_id in seen: continue
        seen.add(run_id)
        import re
        if not re.fullmatch(r'cr-[a-f0-9]{12}',run_id): raise ValueError('Invalid retained cursor identity')
        path=root/(run_id+'.json')
        if path.exists(): continue
        document=next(iter(collection().find({'asset_ref':summary['asset_ref']},{'_id':0})))
        evidence=document['census_evidence']; cursor=evidence['cursor']
        if hashlib.sha256(json.dumps(evidence,sort_keys=True,default=str).encode()).hexdigest()!=document['evidence_sha256']:
            raise ValueError('Cursor custody hash mismatch')
        temporary=path.with_suffix('.restore.tmp');temporary.write_text(json.dumps(cursor,sort_keys=True));temporary.replace(path)
        # Restore the existing queue reference, never invent a second work item.
        job=cursor.get('job_descriptor')
        if cursor['status']=='PENDING' and job:
            target=engine._pending_job_path(run_id)
            if not target.exists(): target.write_text(json.dumps(job,indent=2))