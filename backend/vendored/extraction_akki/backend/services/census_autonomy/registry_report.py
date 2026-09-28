"""Evidence-bearing report projection. Never manufactures missing measurements."""
from datetime import datetime

ROWS = [
 ('coverage','data_held','Data held','Everything kept across the sources in this census.','bytes'),
 ('coverage','sources_full','Sources read in full','Sources whose declared reading scope completed, with nothing skipped.','sources'),
 ('coverage','share_measured','Share measured','The share directly measured here; sampled content is distinguished from a full read.','percent'),
 ('coverage','not_read','Not read','Declared sources or regions that could not be read in this census.','sources'),
 ('condition','duplicates','Duplicates','Repeated content confirmed by the stated check, not merely similar keys.','percent'),
 ('condition','degraded','Degraded','Inspected media that failed the stated decode or structural check.','percent'),
 ('condition','incomplete','Incomplete records','Required-field or relationship failures, where those checks were performed.','percent'),
 ('condition','stale','Stale','Data outside its adopted source freshness window.','percent'),
 ('condition','schema_drift','Schema drift','Sources whose measured structure differs from a comparable prior census.','sources'),
 ('readiness','verified','Share verified','Independently corroborated evidence, not simply a passed quality check.','percent'),
 ('readiness','pii','Share carrying PII','Assessed rows with detected personal-information markers; sample basis remains explicit.','percent'),
 ('readiness','usable','Usable today','Measured, clean, non-duplicated material with the applicable rights.','percent'),
 ('readiness','opportunities','Things worth building','Supported advisory briefs grounded in this census.','briefs'),
]

def enrich_record(record,doc,payload):
    from services.census_autonomy import operational_store as store
    cursor=store.get(doc['census_run_id'],record['tenant_id']) or {}
    sources=[]; workers=[]
    for outcome in payload['outcomes']:
        for row in outcome.get('sources',[]):
            sources.append({**row,'source_id':outcome['source_id'],'observed_at':outcome['observed_at'],
                            'worker_id':outcome.get('worker',{}).get('runtime_id')})
        if outcome.get('worker'): workers.append(outcome['worker'])
    record.update(initiated_by=payload.get('principal_id'),started_at=cursor.get('started_at'),
                  source_refs=cursor.get('source_refs'),
                  source_ids=cursor.get('source_ids') or [o['source_id'] for o in payload['outcomes']],
                  source_details=sources,workers=workers,worker_id=cursor.get('worker_id'),
                  coverage={'declared':len(sources) or len(payload['outcomes']),
                            'completed':sum(s['status']=='complete' for s in sources),
                            'partial':sum(s['status']=='partial' for s in sources),
                            'blocked':sum(s['status']=='blocked' for s in sources)})
    if workers:
        record.update(scope='External deep census: enumerated metadata and declared sampled checks',
            volume_bytes=sum(s.get('volume_bytes',0) for s in sources),
            limitations=['Row totals from MySQL statistics are estimates, not full table scans.',
                         'Content-quality and PII measures describe only their assessed sample.',
                         'Unperformed checks, verification, purpose-specific rights and new model capability remain unmeasured.'])
    try: record['duration_seconds']=(datetime.fromisoformat(record['finished_at'])-datetime.fromisoformat(record['started_at'])).total_seconds()
    except (TypeError,ValueError,KeyError): record['duration_seconds']=None
    record['report']=report_for(record)
    return record

def report_for(record,previous=None):
    sources=record.get('source_details',[])
    sampled=sum(s.get('sample',{}).get('rows',0) for s in sources)
    pii=sum(s.get('sample',{}).get('pii_rows',0) for s in sources)
    media=sum(s.get('media_samples',0)+s.get('media_failures',0) for s in sources)
    media_failures=sum(s.get('media_failures',0) for s in sources)
    complete=sum(s.get('enumeration')=='full' and s.get('content_measurement')=='full' for s in sources)
    measured_bytes=sum(s.get('volume_bytes',0) for s in sources if s.get('status') in ('complete','partial'))
    source_identity=sorted(s['source_ref'] for s in sources)
    prior_identity=sorted(s['source_ref'] for s in (previous or {}).get('source_details',[]))
    comparable=bool(previous and source_identity and source_identity==prior_identity)
    old={s['source_ref']:s for s in (previous or {}).get('source_details',[])}
    structured=[s for s in sources if s.get('structure_sha256') and old.get(s['source_ref'],{}).get('structure_sha256')]
    drift=sum(s['structure_sha256']!=old[s['source_ref']]['structure_sha256'] for s in structured) if comparable and structured else None
    values={'data_held':measured_bytes if sources else record.get('volume_bytes'),
            'sources_full':complete if sources else None,'not_read':sum(s['status']=='blocked' for s in sources) if sources else None,
            'degraded':round(100*media_failures/media,2) if media else None,
            'pii':round(100*pii/sampled,2) if sampled else None,'schema_drift':drift}
    metrics={}
    for group,key,label,description,unit in ROWS:
        value=values.get(key)
        status='sampled' if key in ('pii','degraded') and value is not None else 'measured' if value is not None else 'unmeasured'
        note='No applicable measured result is retained for this figure.'
        if key=='data_held' and value is not None: note='Observed database allocation/object/file bytes; partial sources cover enumerated regions only.'
        elif key=='sources_full' and sources: note='Full metadata enumeration is not a full content read. Sampled SQL and media are not counted here.'
        elif key=='pii' and sampled: note=f'{pii} of {sampled} assessed rows; existing deterministic PII detector; not extrapolated to the estate.'
        elif key=='degraded' and media: note=f'{media_failures} failures among {media} attempted media probes; not an estate-wide rate.'
        elif key=='not_read' and sources: note='Blocked source count; inspect partial regions separately in Discovery Details. Unread bytes are not inferred.'
        elif key=='schema_drift' and drift is not None: note=f'{len(structured)} comparable structural signatures checked.'
        prior_metric=(previous or {}).get('report',{}).get('metrics',{}).get(key,{})
        delta=value-prior_metric['value'] if comparable and value is not None and prior_metric.get('value') is not None and status==prior_metric.get('status') else None
        metrics[key]={'key':key,'group':group,'label':label,'description':description,'unit':unit,'value':value,
                      'status':status,'method':note,'measured_at':record.get('finished_at'),
                      'population':sampled if key=='pii' else media if key=='degraded' else len(sources),
                      'record_id':record['record_id'],'previous_record_id':previous['record_id'] if comparable else None,'delta':delta}
    return {'metrics':metrics,'groups':[{'key':g,'label':g.title(),'rows':[metrics[k] for group,k,*_ in ROWS if group==g]} for g in ('coverage','condition','readiness')],
            'condition_distribution':None,'condition_note':'A mutually exclusive condition distribution has not been measured. Unknown is not clean or zero.',
            'previous_record_id':previous['record_id'] if comparable else None}

def attach_reports(records):
    # Pin comparisons to the previous comparable scope, not any convenient record.
    for index in range(len(records)-1,-1,-1):
        record=records[index]
        identity=sorted(s['source_ref'] for s in record.get('source_details',[]))
        prior=next((r for r in records[index+1:] if identity and sorted(s['source_ref'] for s in r.get('source_details',[]))==identity),None)
        record['report']=report_for(record,prior)
    return records