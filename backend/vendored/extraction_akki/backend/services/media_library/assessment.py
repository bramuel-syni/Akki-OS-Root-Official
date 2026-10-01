"""Metadata readiness only; no media decoding, model calls or training dispatch."""
from services.media_library import store


def snapshot(rows):
    checks=[]
    for row in rows:
        issues=[]
        if row['rights_status']!='declared': issues.append('Training rights need review' if row['rights_status']=='pending' else 'Training rights withdrawn')
        if row['kind']=='audio' and (row['event_label']=='unknown' or row['label_status']!='human_reviewed'):
            issues.append('Speech/music labels need human review')
        if row['kind']=='labels': issues.append('Label taxonomy and file alignment need verification')
        checks.append({'file_id':row['file_id'],'title':row['title'],'revision':row['revision'],'kind':row['kind'],
                       'issues':issues,'rights_independently_verified':False,'quality':'not_measured'})
    return {'scope':'uploaded_file_metadata_only','files':checks,'file_count':len(rows),
            'total_bytes':sum(row['size_bytes'] for row in rows),
            'audio_files':sum(row['kind']=='audio' for row in rows),
            'status':'held_before_retraining','training_started':False,
            'blockers':['Independently verify rights and annotations','Measure audio quality and duration on an authorized worker',
                        'Approve the evaluation contract and training recipe'],
            'duration_seconds':None,'music_detection_performed':False}


def validity(row):
    stale=[]
    for item in row.get('dataset_assessment',{}).get('files',[]):
        current=store.get(row['tenant_id'],item['file_id'])
        if not current or current['is_deleted'] or current['status']!='available' or current['revision']!=item['revision'] or current['rights_status']=='withdrawn':
            stale.append(item['file_id'])
    return {'stale':bool(stale),'changed_files':len(stale),'training_authorized':False}