"""External NAS/object inventory: enumerate metadata; inspect admitted bounded media.

No source filename, object body or media is returned to the E1 control plane.
"""
import hashlib
import json
import os
import shutil
import subprocess
import time
from collections import Counter
from pathlib import Path

def source_ref(group,label):
    return 'source_'+hashlib.sha256((group+'|'+label).encode()).hexdigest()[:24]

def nas(config,deadline):
    root=Path(config['root']).resolve(strict=True)
    # The root is the already mounted, owner-supplied NAS path on the jump worker.
    if not os.path.ismount(root):
        raise ValueError('NAS_NOT_AN_EXTERNAL_MOUNT')
    result=[]
    for channel in sorted(root.iterdir()):
        if not channel.is_dir() or channel.is_symlink(): continue
        label=channel.name
        if config.get('source_refs') and source_ref(config['source_id'],label) not in config['source_refs']: continue
        entry={'source_ref':source_ref(config['source_id'],label),'label':label,'kind':'nas','status':'complete',
               'file_count':0,'volume_bytes':0,'formats':{},'date_min':None,'date_max':None,
               'media_samples':0,'media_duration_seconds':0,'media_failures':0,'skipped_symlinks':0,'errors':0,
               'enumeration':'full','content_measurement':'sampled','row_count_estimate':0,'database_count':0,'table_count':0}
        formats=Counter(); samples=[]
        def onerror(_): entry['errors']+=1
        for directory,dirs,files in os.walk(channel,followlinks=False,onerror=onerror):
            if time.time()>=deadline:
                entry.update(status='partial',enumeration='partial',reason_code='BUDGET_EXHAUSTED'); break
            dirs[:]=sorted(d for d in dirs if not Path(directory,d).is_symlink())
            for filename in sorted(files):
                path=Path(directory,filename)
                try:
                    if path.is_symlink(): entry['skipped_symlinks']+=1; continue
                    stat=path.stat(); entry['file_count']+=1; entry['volume_bytes']+=stat.st_size
                    formats[path.suffix.lower() or 'no_extension']+=1
                    stamp=stat.st_mtime
                    entry['date_min']=min(entry['date_min'],stamp) if entry['date_min'] is not None else stamp
                    entry['date_max']=max(entry['date_max'],stamp) if entry['date_max'] is not None else stamp
                    # Reservoir selection is deterministic by path hash, without exporting it.
                    key=hashlib.sha256(str(path.relative_to(root)).encode()).hexdigest()
                    if path.suffix.lower() in ('.mp4','.mp3','.wav','.mkv','.m4a'):
                        samples.append((key,path)); samples=sorted(samples,key=lambda x:x[0])[:3]
                except OSError: entry['errors']+=1
        entry['formats']=dict(formats)
        entry['media_unmeasured']=0
        for _,path in samples:
            if time.time()>=deadline or not shutil.which('ffprobe'): break
            try:
                p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_name,codec_type,sample_rate','-of','json',str(path)],capture_output=True,text=True,timeout=min(15,max(1,deadline-time.time())))
                if p.returncode:
                    if any(text in p.stderr.lower() for text in ['invalid data','moov atom not found','end of file']): entry['media_failures']+=1
                    else: entry['media_unmeasured']+=1
                    continue
                probe=json.loads(p.stdout); entry['media_samples']+=1
                entry['media_duration_seconds']+=float(probe.get('format',{}).get('duration',0))
                entry.setdefault('codecs',[]).extend(s.get('codec_name') for s in probe.get('streams',[]) if s.get('codec_name'))
            except Exception: entry['media_unmeasured']+=1
        if samples and not shutil.which('ffprobe'):
            entry.update(status='partial',reason_code='MEDIA_INSPECTOR_UNAVAILABLE')
        entry['content_measurement']='sampled' if entry['media_samples'] or entry['media_failures'] else 'unmeasured'
        if entry['errors']: entry.update(status='partial',enumeration='partial')
        entry['method']='External read-only directory/stat enumeration; path-hash-pinned sample of up to three media per channel, ffprobe; duration covers inspected sample only'
        result.append(entry)
    if not result: raise ValueError('NAS_NO_CHANNELS_OBSERVED')
    return result

def objects(config,deadline):
    import boto3
    from botocore.config import Config
    sdk=boto3.client('s3',endpoint_url=config['endpoint'],region_name=config['region'],aws_access_key_id=config['access_key_id'],aws_secret_access_key=config['secret_access_key'],config=Config(signature_version='s3v4',connect_timeout=10,read_timeout=20,retries={'max_attempts':1}))
    buckets=sdk.list_buckets()['Buckets']; result=[]
    for bucket in buckets:
        if config.get('source_refs') and source_ref(config['source_id'],bucket['Name']) not in config['source_refs']: continue
        label=bucket['Name']; entry={'source_ref':source_ref(config['source_id'],label),'label':label,'kind':'object_store','status':'complete',
              'object_count':0,'volume_bytes':0,'formats':{},'date_min':None,'date_max':None,'pages':0,'duplicate_candidates':0,
              'enumeration':'full','content_measurement':'unmeasured','database_count':0,'table_count':0,'row_count_estimate':0}
        token=None; formats=Counter(); fingerprints=set()
        try:
            while True:
                if time.time()>=deadline: raise TimeoutError()
                kwargs={'Bucket':label,'MaxKeys':1000}
                if token: kwargs['ContinuationToken']=token
                page=sdk.list_objects_v2(**kwargs); entry['pages']+=1
                for item in page.get('Contents',[]):
                    entry['object_count']+=1; entry['volume_bytes']+=item['Size']
                    formats[Path(item['Key']).suffix.lower() or 'no_extension']+=1
                    stamp=item['LastModified'].isoformat()
                    entry['date_min']=min(entry['date_min'],stamp) if entry['date_min'] else stamp
                    entry['date_max']=max(entry['date_max'],stamp) if entry['date_max'] else stamp
                    key=(item.get('ETag'),item['Size'])
                    entry['duplicate_candidates']+=key in fingerprints; fingerprints.add(key)
                if not page.get('IsTruncated'): break
                following=page.get('NextContinuationToken')
                if not following or following==token: raise ValueError('NON_ADVANCING_PAGE')
                token=following
        except Exception as exc:
            entry.update(status='partial' if entry['pages'] else 'blocked',enumeration='partial',reason_code=type(exc).__name__)
        entry['formats']=dict(formats)
        entry['method']='External S3-compatible ListObjectsV2, all returned pages; ETag+size candidates are not proven byte duplicates; no object bodies read'
        result.append(entry)
    return result