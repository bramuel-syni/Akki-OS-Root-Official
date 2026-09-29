"""External NAS/object inventory: enumerate metadata; inspect admitted bounded media.

No source filename, object body or media is returned to the E1 control plane.
Measured limits (jump host, CIFS, 57ms RTT, 1 vCPU): about one hundred directory
entries per second regardless of thread count, so a whole share cannot be walked in
one bounded job. Enumeration is therefore resumable: a durable frontier (directory
paths / continuation tokens) is kept on the admitted worker only, units of work are
committed only when fully scanned, and every run reports cumulative totals plus the
progress it made. E1 receives counts, hashes and pending-unit numbers, never paths.
"""
import fcntl
import hashlib
import json
import os
import queue
import shutil
import subprocess
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

MEDIA_SUFFIXES=('.mp4','.mp3','.wav','.mkv','.m4a')
CHECKPOINT_SECONDS=30

def source_ref(group,label):
    return 'source_'+hashlib.sha256((group+'|'+label).encode()).hexdigest()[:24]

def now():
    from datetime import datetime,timezone
    return datetime.now(timezone.utc).isoformat()

class Checkpoint:
    """Durable enumeration frontier on the admitted worker; the file never leaves it."""
    def __init__(self,config,scope_key):
        base=config.get('state_dir')
        self.path=None; self.handle=None; self.state=None
        if not base: return
        key=hashlib.sha256(json.dumps([config['source_id'],scope_key,sorted(config.get('source_refs') or [])]).encode()).hexdigest()[:16]
        self.path=Path(os.path.expanduser(base))/config['source_id']/f'{key}.json'
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.handle=open(self.path.with_suffix('.lock'),'a')
        try: fcntl.flock(self.handle,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: raise ValueError('ENUMERATION_ALREADY_RUNNING')
        if self.path.exists():
            try: self.state=json.loads(self.path.read_text())
            except ValueError: self.state=None
    def write(self,state):
        if not self.path: return None
        temp=self.path.with_suffix(f'.{os.getpid()}.tmp')
        raw=json.dumps(state,sort_keys=True,default=str).encode()
        temp.write_bytes(raw); os.replace(temp,self.path)
        return hashlib.sha256(raw).hexdigest()
    def close(self):
        if self.handle:
            fcntl.flock(self.handle,fcntl.LOCK_UN); self.handle.close()

def new_acc():
    return {'file_count':0,'volume_bytes':0,'formats':{},'date_min':None,'date_max':None,
            'samples':[],'skipped_symlinks':0,'errors':0,'directories_complete':0}

def merge_acc(target,acc):
    for key in ('file_count','volume_bytes','skipped_symlinks','errors','directories_complete'): target[key]+=acc[key]
    for suffix,count in acc['formats'].items(): target['formats'][suffix]=target['formats'].get(suffix,0)+count
    target['samples']=sorted([*map(tuple,target['samples']),*acc['samples']])[:3]
    for bound,pick in (('date_min',min),('date_max',max)):
        if acc[bound] is not None: target[bound]=acc[bound] if target[bound] is None else pick(target[bound],acc[bound])

def scan_directory(directory,root,deadline,stop):
    """One unit of work: returns (acc, child_directories) or None when interrupted."""
    acc=new_acc(); children=[]
    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                if stop.is_set() or time.time()>=deadline: stop.set(); return None
                try:
                    if entry.is_symlink(): acc['skipped_symlinks']+=1; continue
                    if entry.is_dir(follow_symlinks=False): children.append(entry.path); continue
                    stat=entry.stat(follow_symlinks=False)
                    acc['file_count']+=1; acc['volume_bytes']+=stat.st_size
                    suffix=os.path.splitext(entry.name)[1].lower()
                    acc['formats'][suffix or 'no_extension']=acc['formats'].get(suffix or 'no_extension',0)+1
                    stamp=stat.st_mtime
                    acc['date_min']=stamp if acc['date_min'] is None else min(acc['date_min'],stamp)
                    acc['date_max']=stamp if acc['date_max'] is None else max(acc['date_max'],stamp)
                    if suffix in MEDIA_SUFFIXES:
                        # Reservoir selection is deterministic by path hash, without exporting it.
                        key=hashlib.sha256(os.path.relpath(entry.path,root).encode()).hexdigest()
                        acc['samples']=sorted([*acc['samples'],(key,entry.path)])[:3]
                except OSError: acc['errors']+=1
    except OSError: acc['errors']+=1
    acc['directories_complete']=1
    return acc,children

class Frontier:
    """Shared queue plus committed per-channel sums; commit happens only for fully scanned directories."""
    def __init__(self,channels,frontier):
        self.lock=threading.Lock(); self.pending=queue.Queue(); self.channels=channels
        self.open={(label,path) for label,path in frontier}; self.progress=0
        for label,path in frontier: self.pending.put((label,path))
    def commit(self,label,path,acc,children):
        with self.lock:
            self.open.discard((label,path)); merge_acc(self.channels[label],acc); self.progress+=1
            for child in children: self.open.add((label,child)); self.pending.put((label,child))
    def snapshot(self):
        with self.lock: return sorted(self.open),json.loads(json.dumps(self.channels))
    def drain(self,root,deadline,stop):
        while True:
            try: label,path=self.pending.get(timeout=.2)
            except queue.Empty:
                if self.pending.unfinished_tasks==0: return
                continue
            try:
                if not stop.is_set():
                    scanned=scan_directory(path,root,deadline,stop)
                    if scanned: self.commit(label,path,*scanned)
            finally: self.pending.task_done()

def inspect_media(entry,samples,deadline):
    entry['media_unmeasured']=0
    if samples and not shutil.which('ffprobe'):
        entry.update(status='partial',reason_code='MEDIA_INSPECTOR_UNAVAILABLE'); return
    for _,path in samples:
        if time.time()>=deadline: entry['media_unmeasured']+=1; continue
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
    entry['content_measurement']='sampled' if entry['media_samples'] or entry['media_failures'] else 'unmeasured'

def nas(config,deadline):
    root=Path(config['root']).resolve(strict=True)
    # The root is the already mounted, owner-supplied NAS path on the jump worker.
    if not os.path.ismount(root):
        raise ValueError('NAS_NOT_AN_EXTERNAL_MOUNT')
    # Measured on the jump host: directory query throughput does not scale with threads on one CIFS session.
    workers=int(config.get('parallelism',2))
    channels=[c for c in sorted(root.iterdir()) if c.is_dir() and not c.is_symlink()
              and (not config.get('source_refs') or source_ref(config['source_id'],c.name) in config['source_refs'])]
    if not channels: raise ValueError('NAS_NO_CHANNELS_OBSERVED')
    checkpoint=Checkpoint(config,str(root))
    try:
        state=checkpoint.state
        if not state or state.get('complete') or state.get('root')!=str(root):
            previous={'epoch':state['epoch'],'completed_at':state['completed_at'],'file_count':sum(c['file_count'] for c in state['channels'].values()),
                      'volume_bytes':sum(c['volume_bytes'] for c in state['channels'].values())} if state and state.get('complete') else None
            state={'version':1,'source_id':config['source_id'],'root':str(root),'epoch':(state or {}).get('epoch',0)+1,'epoch_started_at':now(),
                   'runs':0,'channels':{},'frontier':[],'complete':False,'completed_at':None,'previous_epoch':previous}
        for channel in channels:
            if channel.name not in state['channels']:
                state['channels'][channel.name]=new_acc(); state['frontier'].append([channel.name,str(channel)])
        state['runs']+=1
        frontier=Frontier(state['channels'],state['frontier']); stop=threading.Event()
        # Enumeration yields a slice of the budget to bounded media inspection (≤3 probes per channel, ≤15s each).
        enumeration_deadline=deadline-min(60,max(0,(deadline-time.time())*.05))
        def persist():
            state['frontier'],state['channels']=frontier.snapshot()
            return checkpoint.write(state)
        def keeper():
            while not stop.wait(CHECKPOINT_SECONDS): persist()
        keeper_thread=threading.Thread(target=keeper,daemon=True); keeper_thread.start()
        try:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                for _ in pool.map(lambda _:frontier.drain(str(root),enumeration_deadline,stop),range(workers)): pass
        finally:
            stop.set(); keeper_thread.join(timeout=5)
        pending=Counter(label for label,_ in frontier.open)
        state['complete']=not frontier.open
        state['completed_at']=now() if state['complete'] else None
        digest=persist()
    finally:
        checkpoint.close()
    result=[]
    for channel in channels:
        label=channel.name; acc=state['channels'][label]
        entry={'source_ref':source_ref(config['source_id'],label),'label':label,'kind':'nas','status':'complete',
               'file_count':acc['file_count'],'volume_bytes':acc['volume_bytes'],'formats':dict(acc['formats']),
               'date_min':acc['date_min'],'date_max':acc['date_max'],
               'media_samples':0,'media_duration_seconds':0,'media_failures':0,'skipped_symlinks':acc['skipped_symlinks'],'errors':acc['errors'],
               'directories_complete':acc['directories_complete'],'directories_pending':pending.get(label,0),
               'enumeration':'full','content_measurement':'sampled','row_count_estimate':0,'database_count':0,'table_count':0,
               'epoch':state['epoch'],'epoch_started_at':state['epoch_started_at'],'runs_in_epoch':state['runs'],
               'progress_this_run':frontier.progress,'resumable':checkpoint.path is not None,'checkpoint_sha256':digest,
               'previous_epoch':state.get('previous_epoch')}
        if pending.get(label): entry.update(status='partial',enumeration='partial',reason_code='BUDGET_EXHAUSTED')
        inspect_media(entry,[tuple(s) for s in acc['samples']],deadline)
        if entry['errors']: entry.update(status='partial',enumeration='partial')
        entry['method']=(f'External read-only directory/stat enumeration on the admitted mount, {workers} bounded concurrent walkers over a shared '
                         'queue; directories are committed only when fully scanned and the frontier is checkpointed on the worker so successive '
                         'bounded runs resume until the share is complete; path-hash-pinned sample of up to three media per channel, ffprobe; '
                         'duration covers inspected sample only')
        result.append(entry)
    return result

class BucketState:
    """Continuation token plus compact fingerprints, persisted on the worker."""
    def __init__(self,checkpoint,label,saved):
        self.saved=saved or {'object_count':0,'volume_bytes':0,'formats':{},'date_min':None,'date_max':None,'pages':0,
                             'duplicate_candidates':0,'token':None,'complete':False,'fingerprints':0}
        self.fingerprints=set(); self.path=None; self.buffer=bytearray()
        if checkpoint.path:
            self.path=checkpoint.path.with_name(f'{checkpoint.path.stem}-{hashlib.sha256(label.encode()).hexdigest()[:24]}.fp')
            if self.path.exists():
                raw=self.path.read_bytes()[:self.saved['fingerprints']*16]
                self.fingerprints={raw[i:i+16] for i in range(0,len(raw),16)}
                self.path.write_bytes(raw)
    def flush(self):
        if self.path and self.buffer:
            with self.path.open('ab') as handle: handle.write(self.buffer)
            self.saved['fingerprints']+=len(self.buffer)//16; self.buffer=bytearray()

def objects(config,deadline):
    import boto3
    from botocore.config import Config
    workers=int(config.get('parallelism',16))
    sdk=boto3.client('s3',endpoint_url=config['endpoint'],region_name=config['region'],aws_access_key_id=config['access_key_id'],aws_secret_access_key=config['secret_access_key'],config=Config(signature_version='s3v4',connect_timeout=10,read_timeout=20,retries={'max_attempts':1},max_pool_connections=max(16,workers)))
    buckets=[b for b in sdk.list_buckets()['Buckets'] if not config.get('source_refs') or source_ref(config['source_id'],b['Name']) in config['source_refs']]
    checkpoint=Checkpoint(config,config['endpoint'])
    try:
        state=checkpoint.state
        if not state or state.get('complete'):
            state={'version':1,'source_id':config['source_id'],'endpoint':config['endpoint'],'epoch':(state or {}).get('epoch',0)+1,
                   'epoch_started_at':now(),'runs':0,'buckets':{},'complete':False,'completed_at':None}
            if checkpoint.path:
                for stale in checkpoint.path.parent.glob(f'{checkpoint.path.stem}-*.fp'): stale.unlink()
        state['runs']+=1
        lock=threading.Lock(); stop=threading.Event(); progress=[0]
        states={b['Name']:BucketState(checkpoint,b['Name'],state['buckets'].get(b['Name'])) for b in buckets}
        def persist():
            with lock:
                for bucket in states.values(): bucket.flush()
                state['buckets']={label:bucket.saved for label,bucket in states.items()}
                return checkpoint.write(state)
        def keeper():
            while not stop.wait(CHECKPOINT_SECONDS): persist()
        keeper_thread=threading.Thread(target=keeper,daemon=True); keeper_thread.start()
        def inventory(bucket):
            label=bucket['Name']; entry=states[label].saved; fingerprints=states[label].fingerprints; reason=None
            if entry['complete']: return label,None
            try:
                while True:
                    if time.time()>=deadline: raise TimeoutError()
                    kwargs={'Bucket':label,'MaxKeys':1000}
                    if entry['token']: kwargs['ContinuationToken']=entry['token']
                    page=sdk.list_objects_v2(**kwargs)
                    with lock:
                        entry['pages']+=1; progress[0]+=1
                        for item in page.get('Contents',[]):
                            entry['object_count']+=1; entry['volume_bytes']+=item['Size']
                            suffix=Path(item['Key']).suffix.lower() or 'no_extension'
                            entry['formats'][suffix]=entry['formats'].get(suffix,0)+1
                            stamp=item['LastModified'].isoformat()
                            entry['date_min']=min(entry['date_min'],stamp) if entry['date_min'] else stamp
                            entry['date_max']=max(entry['date_max'],stamp) if entry['date_max'] else stamp
                            key=hashlib.sha256(f"{item.get('ETag')}|{item['Size']}".encode()).digest()[:16]
                            entry['duplicate_candidates']+=key in fingerprints; fingerprints.add(key); states[label].buffer.extend(key)
                        if not page.get('IsTruncated'): entry['complete']=True; entry['token']=None; break
                        following=page.get('NextContinuationToken')
                        if not following or following==entry['token']: raise ValueError('NON_ADVANCING_PAGE')
                        entry['token']=following
            except Exception as exc:
                reason='BUDGET_EXHAUSTED' if isinstance(exc,TimeoutError) else type(exc).__name__
            return label,reason
        try:
            with ThreadPoolExecutor(max_workers=max(1,min(workers,len(buckets) or 1))) as pool:
                reasons=dict(pool.map(inventory,buckets))
        finally:
            stop.set(); keeper_thread.join(timeout=5)
        state['complete']=bool(buckets) and all(states[b['Name']].saved['complete'] for b in buckets)
        state['completed_at']=now() if state['complete'] else None
        digest=persist()
    finally:
        checkpoint.close()
    result=[]
    for bucket in buckets:
        label=bucket['Name']; saved=states[label].saved; reason=reasons.get(label)
        entry={'source_ref':source_ref(config['source_id'],label),'label':label,'kind':'object_store',
               'status':'complete' if saved['complete'] else 'partial' if saved['pages'] else 'blocked',
               'object_count':saved['object_count'],'volume_bytes':saved['volume_bytes'],'formats':dict(saved['formats']),
               'date_min':saved['date_min'],'date_max':saved['date_max'],'pages':saved['pages'],'duplicate_candidates':saved['duplicate_candidates'],
               'enumeration':'full' if saved['complete'] else 'partial','content_measurement':'unmeasured','database_count':0,'table_count':0,'row_count_estimate':0,
               'epoch':state['epoch'],'epoch_started_at':state['epoch_started_at'],'runs_in_epoch':state['runs'],
               'progress_this_run':progress[0],'resumable':checkpoint.path is not None and reason in (None,'BUDGET_EXHAUSTED'),'checkpoint_sha256':digest}
        if reason: entry['reason_code']=reason
        entry['method']=(f'External S3-compatible ListObjectsV2, all returned pages, {workers} bounded concurrent bucket listings; continuation '
                         'tokens and page sums are checkpointed on the worker so successive bounded runs resume; ETag+size candidates are not '
                         'proven byte duplicates; no object bodies read')
        result.append(entry)
    return result
