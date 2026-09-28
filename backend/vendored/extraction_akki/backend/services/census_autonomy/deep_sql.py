"""External-only adapter of existing composition, profile and detection kernels.

Samples remain in this worker's memory. Returned material is schema metadata and
aggregate measurements, never source rows. Large-table full scans are not issued.
"""
import hashlib
import json
import time
from collections import Counter
from services.mtafiti.composition_census import run_composition_census
from services.mtafiti.quality_profiler import run_quality_profile
from services.mtafiti.relationship_signals import detect_relationship_signals
from services.mtafiti.probes.live_readonly_probe import ExecutorResult
from services.mtafiti.executor.readonly_sql_guard import refuse_if_write
from services.mtafiti.detectors.pii_detector import detect_pii

def identifier(value):
    return '`'+str(value).replace('`','``')+'`'

def inspect_connection(config, deadline, database=None):
    connection=None
    sample={'rows':0,'pii_rows':0,'incomplete_rows':0,'duplicate_rows':0,'languages':{},'table_samples':[]}
    try:
        if config['driver']=='rds_data':
            import boto3
            from botocore.config import Config
            sdk=boto3.client('rds-data',region_name=config['region'],aws_access_key_id=config['aws_access_key_id'],aws_secret_access_key=config['aws_secret_access_key'],config=Config(connect_timeout=10,read_timeout=30,retries={'max_attempts':1}))
            def query(sql):
                value=sdk.execute_statement(resourceArn=config['cluster_arn'],secretArn=config['secret_arn'],database=database,sql=sql,includeResultMetadata=True)
                rows=[[None if cell.get('isNull') else next(iter(cell.values())) for cell in row] for row in value.get('records',[])]
                return rows,[v.get('name','') for v in value.get('columnMetadata',[])]
        else:
            import pymysql
            connection=pymysql.connect(host=config['host'],port=int(config['port']),user=config['user'],password=config['password'],connect_timeout=8,read_timeout=15,write_timeout=8,charset='utf8mb4',autocommit=True)
            def query(sql):
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    return list(cursor.fetchall()),[c[0] for c in cursor.description or []]
        def executor(sql):
            if time.time()>=deadline: return ExecutorResult(error='BUDGET_EXHAUSTED')
            try:
                guarded=refuse_if_write(sql)
                # No table-wide COUNT or uncontrolled statement may escape this wrapper.
                if not ('information_schema' in guarded.lower() or guarded.upper()=='SHOW DATABASES' or ' LIMIT ' in guarded.upper()):
                    return ExecutorResult(error='READ_OUTSIDE_BOUNDED_METHOD')
                rows,columns=query(guarded)
                if 'information_schema' not in guarded.lower() and guarded.upper().startswith('SELECT '):
                    observe(rows,columns,sample)
                return ExecutorResult(rows=rows,columns=columns,row_count=len(rows))
            except Exception as exc:
                return ExecutorResult(error=type(exc).__name__)
        composition=run_composition_census(host='external-worker-source',port=0,user='custody-reference',label=config['label'],sql_executor=executor,schemas=[database] if database else None)
        if not composition['connected']: raise RuntimeError('CONNECTION_UNAVAILABLE')
        tables=composition['per_table']
        profile=run_quality_profile(host='external-worker-source',port=0,user='custody-reference',label=config['label'],sql_executor=executor,per_table=tables)
        # Clear SQL/error diagnostics; only aggregate field results cross the seam.
        for value in (composition,profile):
            for key in ('host','port','user','sql_trace'): value.pop(key,None)
            value['errors']=[{'stage':str(e.get('stage','')),'code':'MEASUREMENT_NOT_COMPLETED'} for e in value.get('errors',[])]
        links=[s.model_dump(mode='json') for s in detect_relationship_signals(tables)]
        structure={k:v['columns'] for k,v in sorted(tables.items())}
        totals=composition['totals']
        return {'status':'complete' if not composition['errors'] and not profile['errors'] else 'partial',
                'database_count':totals['schemas'],'table_count':totals['tables'],'column_count':totals['columns'],
                'row_count_estimate':totals['rows'],'volume_bytes':sum(v.get('data_length_bytes') or 0 for v in tables.values()),
                'structure_sha256':hashlib.sha256(json.dumps(structure,sort_keys=True).encode()).hexdigest(),
                'composition':composition,'profile':profile,'sample':sample,'relationships':links,
                'enumeration':'metadata_full' if not composition['errors'] else 'partial',
                'content_measurement':'sampled','row_count_measured':None,
                'method':'Existing Mtafiti composition CP4 + deterministic bounded CP5 profile; MySQL estimates, no full table scan'}
    finally:
        if connection: connection.close()

def observe(rows,columns,result):
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed=0
    fingerprints=set(); languages=Counter(result['languages'])
    incomplete=pii=duplicates=0
    for row in rows:
        mapped=dict(zip(columns,row))
        # Null occurrence is a measurement, NOT a claim that nullable fields violate policy.
        incomplete+=any(v is None for v in row)
        pii+=bool(detect_pii(mapped))
        digest=hashlib.sha256(json.dumps(row,default=str,sort_keys=True).encode()).digest()
        duplicates+=digest in fingerprints; fingerprints.add(digest)
        text=' '.join(v for v in row if isinstance(v,str) and len(v)>30)
        if text:
            try: languages[detect(text[:2000])]+=1
            except Exception: languages['undetermined']+=1
    result['rows']+=len(rows); result['pii_rows']+=pii
    result['incomplete_rows']+=incomplete; result['duplicate_rows']+=duplicates
    result['languages']=dict(languages)
    result['table_samples'].append({'rows':len(rows),'pii_rows':pii,'null_bearing_rows':incomplete,'duplicate_rows':duplicates})

def run(config,deadline):
    connections=config['connections'] if config['driver']=='mysql_metadata' else [dict(config,label=db,database=db) for db in config['databases']]
    outputs=[]
    for connection in connections:
        identity=hashlib.sha256((config['source_id']+'|'+connection['label']).encode()).hexdigest()[:24]
        if config.get('source_refs') and 'source_'+identity not in config['source_refs']: continue
        entry={'source_ref':'source_'+identity,'label':connection['label'],'kind':'mysql','status':'blocked'}
        if time.time()>=deadline:
            entry['reason_code']='BUDGET_EXHAUSTED'
        else:
            try: entry.update(inspect_connection({**connection,'driver':config['driver']},deadline,connection.get('database')))
            except Exception as exc:
                code=exc.args[0] if getattr(exc,'args',[]) and type(exc.args[0]) is int else None
                entry['reason_code']={1045:'AUTHENTICATION_FAILED',1044:'DATABASE_PERMISSION_DENIED',1142:'DATABASE_PERMISSION_DENIED',2003:'SOURCE_UNREACHABLE',2013:'SOURCE_TIMEOUT'}.get(code,type(exc).__name__)
                if code is not None: entry['provider_error_code']=code
        outputs.append(entry)
    return outputs