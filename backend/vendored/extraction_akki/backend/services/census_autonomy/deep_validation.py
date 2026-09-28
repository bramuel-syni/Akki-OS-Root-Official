"""Evidence validation for the additive deep-measurement protocol, not legacy success."""
import json
from datetime import datetime

def validate_deep(value,run_id,tenant,source):
    expected={'census_run_id':run_id,'tenant_id':tenant,'source_id':source,'source_rows_returned':0}
    if any(value.get(k)!=v for k,v in expected.items()) or type(value.get('source_rows_returned')) is not int:
        raise ValueError('Commission scope mismatch')
    if value.get('status') not in {'complete','partial','blocked'}: raise ValueError('Unknown deep outcome')
    if datetime.fromisoformat(value['observed_at']).tzinfo is None: raise ValueError('Timestamp lacks timezone')
    if value['status']!='blocked':
        worker=value.get('worker',{})
        if value.get('execution_location')!='akki_host' or worker.get('transport_verified') is not True:
            raise ValueError('Actual external transport proof required')
        if not worker.get('server_key_sha256') or not worker.get('code_sha256') or not worker.get('runtime_id'):
            raise ValueError('Worker identity incomplete')
        if not value.get('sources') or not value.get('worker_receipt_id'): raise ValueError('Source measurements absent')
        if value['status']=='complete' and any(s.get('status')!='complete' for s in value['sources']):
            raise ValueError('Partial source coverage cannot be COMPLETE')
        for key in ('database_count','table_count','row_count_estimate'):
            if type(value.get(key)) is not int or value[key]<0: raise ValueError('Invalid totals')
    elif not value.get('reason_code'): raise ValueError('Blocked reason required')
    def scan(node):
        if isinstance(node,dict):
            if set(node)&{'password','aws_secret_access_key','access_key_id','secret_access_key','raw_rows','sample_values','row_values'}:
                raise ValueError('Source content or credential field refused')
            for v in node.values(): scan(v)
        elif isinstance(node,list):
            for v in node: scan(v)
    scan(value)
    if len(json.dumps(value))>12*1024*1024: raise ValueError('Receipt exceeds store limit')
    return dict(value)