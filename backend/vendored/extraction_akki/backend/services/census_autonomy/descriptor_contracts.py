"""The supplied Draft 2020-12 contracts, validated without inventing admission."""
import hashlib
import json
import os
from functools import lru_cache
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
from services.census_autonomy.operational_scope import sources_for
from services.census_autonomy.registry_durability import collection,evidence_rows
from services.census_autonomy.operational_store import now
from services.mtafiti.asset_registry_writer import append_census_evidence

ROOT=Path(__file__).resolve().parents[2]/'contracts'/'connection_descriptors_v1'
KINDS={'source','query','worker','inspection','custody','admission_record'}

@lru_cache(maxsize=None)
def validator(kind):
    if kind not in KINDS: raise ValueError('Unknown descriptor contract')
    filename='admission_record.schema.json' if kind=='admission_record' else f'{kind}_descriptor.schema.json'
    schema=json.loads((ROOT/filename).read_text()); Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema,format_checker=FormatChecker())

def validate_descriptor(kind,value):
    errors=sorted(validator(kind).iter_errors(value),key=lambda e:str(list(e.path)))
    if errors: raise ValueError('; '.join(f'{".".join(map(str,e.path))}: {e.message}' for e in errors[:5]))
    return value

def bind_existing(tenant,source_id,name,principal):
    if source_id not in sources_for(tenant): raise ValueError('Source outside tenant scope')
    if not isinstance(name,str) or not 1<=len(name.strip())<=160: raise ValueError('Name must be 1–160 characters')
    collection()
    existing=next((x for x in evidence_rows(tenant,'source_descriptor') if x['source_group']==source_id),None)
    if existing: return existing,False
    kinds={'rms_mysql':'mysql','rms_nas':'nas_nfs','rms_obs':'object_store','digicow_rds':'http_api','digicow_s3':'object_store'}
    ports=json.loads(os.environ['CENSUS_DESCRIPTOR_PORTS'])
    value={'descriptor_id':'src_'+hashlib.sha256((tenant+'|'+source_id).encode()).hexdigest()[:16],
           'descriptor_class':'source','tenant_id':tenant,'estate_id':tenant,'version':1,
           'recorded_by_principal_id':principal,'recorded_at':now(),'supersedes':None,
           'read_only':True,'status':'declared','verification_receipt_ref':None,'kind':kinds[source_id],
           'endpoint':{'host_ref':'cust://estate/'+source_id,'port':ports[source_id],'database_or_bucket':'registry:'+source_id},
           'scope':{'schemas_or_prefixes':['registry:'+source_id],'excluded':[]},
           'credential_ref':'cust://estate/'+source_id,'custody_class_default':'controlled','connector_registry_id':source_id}
    value['pinned_hash']=hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    validate_descriptor('source',value)
    evidence={'kind':'source_descriptor','descriptor':value,'source_group':source_id,'name':name.strip(),'recorded_by':principal,
              'admission_status':'Existing operational census scope; native signed descriptor admission is not inferred.'}
    append_census_evidence('source-descriptor:'+tenant+':'+value['descriptor_id'],tenant,evidence)
    return evidence,True