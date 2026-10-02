"""Content pass of the deep census (owner order 2026-10-02: "run the census … for the entire estate. No short cuts. read every thing").

Every media object in the commissioned scope is read byte for byte on the admitted GPU host, verified against the listing (size, ETag),
decoded in full and judged on every consecutive two-second window with the admitted music detector and the current audio language
model — no sampling, no per-file second or window cap. The only bound is the engine's bounded run: the durable inventory, the
per-object rows and the access verdicts live on the host volume, so successive runs resume until every readable object is read.
Only aggregates return in the receipt; keys, bytes and rows never leave the host. Objects the key cannot read are counted and
reported as such — that is the byte-level truth of what can be accessed, not a gap papered over.
"""
import hashlib
import json
import os
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

AUDIO = ('.mp3', '.wav', '.flac', '.ogg', '.oga', '.m4a', '.aac', '.wma', '.amr', '.opus', '.aif', '.aiff')
VIDEO = ('.mp4', '.mkv', '.mov', '.avi', '.mxf', '.ts', '.m2ts', '.wmv', '.flv', '.webm', '.mpg', '.mpeg', '.3gp', '.m4v', '.mts', '.vob')
MEDIA = AUDIO + VIDEO
SR = 16000
WIN = 2 * SR
STOP_MARGIN_S = 240          # devices stop this long before the worker deadline so rows flush, aggregates build and the receipt is written
INVENTORY_SHARE = 0.35       # at most this share of a run goes to listing before reading starts; listing resumes next run
PROBE_OBJECTS = 6            # spread objects probed with one-byte range reads before a bucket is declared unreadable
PREFIX_LIMIT = 60
# Transport failures are retried on the next run; permission, state and decode failures are the object's recorded truth.
RETRY_ERRORS = {'ReadTimeoutError', 'ConnectTimeoutError', 'ConnectionError', 'EndpointConnectionError', 'ConnectionClosedError', 'IncompleteReadError',
                'SSLError', 'ProtocolError', 'ResponseStreamingError', 'TimeoutError', 'OSError', 'IOError', 'EOFError', 'SSHException', 'socket.timeout',
                'InternalError', 'ServiceUnavailable', 'SlowDown', 'RequestTimeout', 'Throttling', '503'}

DEVICE_MAIN = '''import sys, json
sys.path.insert(0, sys.argv[1])
from services.census_autonomy.deep_content import run_device
run_device(json.load(sys.stdin), sys.argv[2], int(sys.argv[3]))
'''


def now():
    return datetime.now(timezone.utc).isoformat()


def ref_of(source, key):
    return hashlib.sha256(f'{source}|{key}'.encode()).hexdigest()[:16]


def kind_of(key):
    low = key.lower()
    return 'audio' if low.endswith(AUDIO) else 'video' if low.endswith(VIDEO) else None


def _label_dir(root, source_id, label):
    path = Path(root).expanduser() / source_id / hashlib.sha256(label.encode()).hexdigest()[:24]
    path.mkdir(parents=True, exist_ok=True)
    return path


def _read_json(path, default):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return default


def _write_json(path, value):
    tmp = Path(str(path) + f'.{os.getpid()}.tmp')
    tmp.write_text(json.dumps(value, sort_keys=True, default=str))
    os.replace(tmp, path)


def _gpus():
    try:
        p = subprocess.run(['nvidia-smi', '--query-gpu=index', '--format=csv,noheader'], capture_output=True, text=True, timeout=20)
        return [int(x) for x in p.stdout.split()] if p.returncode == 0 else []
    except Exception:
        return []


def _sdk(config):
    import boto3
    from botocore.config import Config
    return boto3.client('s3', endpoint_url=config['endpoint'], region_name=config['region'], aws_access_key_id=config['access_key_id'],
                        aws_secret_access_key=config['secret_access_key'],
                        config=Config(signature_version='s3v4', connect_timeout=10, read_timeout=120, retries={'max_attempts': 3}, max_pool_connections=64))


# ----------------------------------------------------------------------------------------------------------------- inventories
def _inventory_obs(sdk, label, folder, stop_at):
    """Every key in the bucket, resumable by continuation token; the inventory is the full enumeration of this run as well."""
    meta = _read_json(folder / 'inventory.json', {'complete': False, 'token': None, 'objects': 0, 'bytes': 0, 'pages': 0, 'formats': {}, 'date_min': None, 'date_max': None, 'started_at': now()})
    if meta['complete']:
        return meta
    with (folder / 'inventory.tsv').open('a') as out:
        while time.time() < stop_at:
            kwargs = {'Bucket': label, 'MaxKeys': 1000}
            if meta['token']:
                kwargs['ContinuationToken'] = meta['token']
            try:
                page = sdk.list_objects_v2(**kwargs)
            except Exception as exc:
                meta['list_error'] = type(exc).__name__
                break
            meta['pages'] += 1
            for item in page.get('Contents', []):
                stamp = item['LastModified'].isoformat()
                out.write('\t'.join([item['Key'].replace('\t', ' ').replace('\n', ' '), str(item['Size']), (item.get('ETag') or '').strip('"'), stamp, item.get('StorageClass') or '']) + '\n')
                meta['objects'] += 1
                meta['bytes'] += item['Size']
                suffix = Path(item['Key']).suffix.lower() or 'no_extension'
                meta['formats'][suffix] = meta['formats'].get(suffix, 0) + 1
                meta['date_min'] = min(meta['date_min'], stamp) if meta['date_min'] else stamp
                meta['date_max'] = max(meta['date_max'], stamp) if meta['date_max'] else stamp
            out.flush()
            if not page.get('IsTruncated'):
                meta.update(complete=True, token=None, completed_at=now())
                break
            following = page.get('NextContinuationToken')
            if not following or following == meta['token']:
                meta['list_error'] = 'NON_ADVANCING_PAGE'
                break
            meta['token'] = following
            if meta['pages'] % 20 == 0:
                _write_json(folder / 'inventory.json', meta)
    _write_json(folder / 'inventory.json', meta)
    return meta


def _sftp_client(hop):
    import paramiko
    client = paramiko.SSHClient()
    with tempfile.NamedTemporaryFile('w', suffix='.known_hosts', delete=False) as handle:
        handle.write(hop['known_hosts'])
        known = handle.name
    try:
        client.load_host_keys(known)
        client.set_missing_host_key_policy(paramiko.RejectPolicy())
        client.connect(hop['host'], int(hop['port']), username=hop['user'], password=hop['password'], look_for_keys=False, allow_agent=False, timeout=20, auth_timeout=20, banner_timeout=20)
        client.get_transport().set_keepalive(30)
    finally:
        os.unlink(known)
    return client, client.open_sftp()


def _inventory_nas(sftp, root, label, folder, stop_at):
    """Every file under one share, walked through the jump host's SFTP; the pending-directory frontier resumes across runs."""
    import stat as st
    meta = _read_json(folder / 'inventory.json', {'complete': False, 'pending': [f'{root}/{label}'], 'objects': 0, 'bytes': 0, 'directories': 0, 'formats': {}, 'date_min': None, 'date_max': None, 'errors': 0, 'started_at': now()})
    if meta['complete']:
        return meta
    last_flush = time.time()
    with (folder / 'inventory.tsv').open('a') as out:
        while meta['pending'] and time.time() < stop_at:
            directory = meta['pending'][-1]
            try:
                entries = sftp.listdir_attr(directory)
            except (IOError, OSError):
                meta['errors'] += 1
                meta['pending'].pop()
                continue
            children = []
            for entry in entries:
                if st.S_ISLNK(entry.st_mode):
                    continue
                path = f'{directory}/{entry.filename}'
                if st.S_ISDIR(entry.st_mode):
                    children.append(path)
                    continue
                stamp = datetime.fromtimestamp(entry.st_mtime or 0, tz=timezone.utc).isoformat()
                out.write('\t'.join([path[len(root) + 1:].replace('\t', ' ').replace('\n', ' '), str(entry.st_size or 0), '', stamp, 'nas']) + '\n')
                meta['objects'] += 1
                meta['bytes'] += entry.st_size or 0
                suffix = Path(entry.filename).suffix.lower() or 'no_extension'
                meta['formats'][suffix] = meta['formats'].get(suffix, 0) + 1
                meta['date_min'] = min(meta['date_min'], stamp) if meta['date_min'] else stamp
                meta['date_max'] = max(meta['date_max'], stamp) if meta['date_max'] else stamp
            out.flush()
            meta['pending'].pop()
            meta['pending'].extend(children)
            meta['directories'] += 1
            if time.time() - last_flush > 30:
                _write_json(folder / 'inventory.json', meta)
                last_flush = time.time()
        if not meta['pending']:
            meta.update(complete=True, completed_at=now())
    _write_json(folder / 'inventory.json', meta)
    return meta


def _media_items(folder):
    """Media rows of the inventory: (key, size, etag, modified, storage_class, kind); audio first, then video, deterministic order."""
    items = []
    try:
        with (folder / 'inventory.tsv').open() as handle:
            for line in handle:
                parts = line.rstrip('\n').split('\t')
                if len(parts) < 5:
                    continue
                kind = kind_of(parts[0])
                if kind:
                    items.append((parts[0], int(parts[1]), parts[2], parts[3], parts[4], kind))
    except OSError:
        return []
    items.sort(key=lambda it: (it[5] != 'audio', it[0]))
    return items


def _duplicate_candidates(folder, meta):
    if meta.get('duplicate_candidates') is not None:
        return meta['duplicate_candidates']
    seen, candidates = set(), 0
    try:
        with (folder / 'inventory.tsv').open() as handle:
            for line in handle:
                parts = line.rstrip('\n').split('\t')
                if len(parts) < 3 or not parts[2]:
                    continue
                digest = hashlib.sha256(f'{parts[2]}|{parts[1]}'.encode()).digest()[:16]
                candidates += digest in seen
                seen.add(digest)
    except OSError:
        pass
    meta['duplicate_candidates'] = candidates
    _write_json(folder / 'inventory.json', meta)
    return candidates


def _rows(folder):
    """Every retained row of a bucket/share, one per object: a successful read supersedes an earlier failure; a transport failure is
    not final and the object is read again on the next run."""
    by_ref = {}
    for path in sorted(folder.glob('rows_*.jsonl')):
        try:
            with path.open() as handle:
                for line in handle:
                    try:
                        row = json.loads(line)
                    except ValueError:
                        continue
                    previous = by_ref.get(row['ref'])
                    if previous is None or previous.get('error') or not row.get('error'):
                        by_ref[row['ref']] = row
        except OSError:
            continue
    return by_ref


def _done_refs(folder):
    return {ref for ref, row in _rows(folder).items() if not (row.get('error') in RETRY_ERRORS)}


def _probe_access(sdk, label, items, folder):
    """Spread one-byte range reads decide whether the key may read this bucket's bodies at all; the verdict is kept with the inventory."""
    verdict = _read_json(folder / 'access.json', None)
    if verdict and verdict.get('items') == len(items):
        return verdict
    picks = [items[int(i * (len(items) - 1) / max(1, PROBE_OBJECTS - 1))] for i in range(min(PROBE_OBJECTS, len(items)))] if items else []
    outcomes = Counter()
    for key, size, *_ in picks:
        try:
            body = sdk.get_object(Bucket=label, Key=key, Range='bytes=0-0')['Body']
            body.read()
            outcomes['readable'] += 1
        except Exception as exc:
            name = type(exc).__name__
            code = (getattr(exc, 'response', {}) or {}).get('Error', {}).get('Code') or name
            outcomes[code] += 1
    if not picks:
        state = 'no_media'
    elif outcomes.get('readable'):
        state = 'readable'
    elif all(code == 'InvalidObjectState' for code in outcomes):
        state = 'archived'
    else:
        state = 'denied'
    verdict = {'state': state, 'probed': dict(outcomes), 'items': len(items), 'at': now()}
    _write_json(folder / 'access.json', verdict)
    return verdict


# ----------------------------------------------------------------------------------------------------------------- aggregation
def _aggregate(folder, items, access, meta, label, source_kind, run_seconds, devices, this_run_rows):
    by_ref = _rows(folder)
    rows = list(by_ref.values())
    read = [r for r in rows if not r.get('error')]
    failed = [r for r in rows if r.get('error')]
    media_bytes = sum(it[1] for it in items)
    pending = [it for it in items if ref_of(label, it[0]) not in by_ref or by_ref[ref_of(label, it[0])].get('error') in RETRY_ERRORS]
    languages, files_top, prefixes, formats, codecs, rates, channels = Counter(), Counter(), {}, Counter(), Counter(), Counter(), Counter()
    windows = silence = music = speech = abstained = judged = 0
    seconds = 0.0
    confidence_sum, confidence_n, clipped_sum, clipped_n, level_sum, level_n = 0.0, 0, 0.0, 0, 0.0, 0
    bytes_read = bytes_verified = 0
    for r in read:
        bytes_read += r['bytes_read']
        bytes_verified += r['bytes_read'] if r.get('size_match') and r.get('etag_match') in (True, None) else 0
        seconds += r['duration_s']
        windows += r['windows']; silence += r['silence_windows']; music += r['music_windows']; speech += r['speech_windows']
        abstained += r['abstained']; judged += r['judged']
        languages.update(r.get('by_language') or {})
        if r.get('top_language'):
            files_top[r['top_language']] += 1
        formats[r['ext']] += 1
        if r.get('codec'):
            codecs[r['codec']] += 1
        if r.get('sample_rate'):
            rates[str(r['sample_rate'])] += 1
        if r.get('channels'):
            channels[str(r['channels'])] += 1
        if r.get('mean_confidence') is not None:
            confidence_sum += r['mean_confidence'] * max(1, r['judged'] + r['abstained']); confidence_n += max(1, r['judged'] + r['abstained'])
        if r.get('clipped_share') is not None:
            clipped_sum += r['clipped_share'] * r['windows']; clipped_n += r['windows']
        if r.get('level_dbfs') is not None:
            level_sum += r['level_dbfs'] * r['windows']; level_n += r['windows']
        p = prefixes.setdefault(r['prefix'], {'prefix': r['prefix'], 'objects': 0, 'bytes_read': 0, 'hours_decoded': 0.0, 'hours_speech': 0.0, 'hours_music': 0.0, 'languages': Counter()})
        p['objects'] += 1; p['bytes_read'] += r['bytes_read']; p['hours_decoded'] += r['duration_s'] / 3600
        p['hours_speech'] += r['speech_windows'] * 2 / 3600; p['hours_music'] += r['music_windows'] * 2 / 3600
        p['languages'].update(r.get('by_language') or {})
    prefix_rows = sorted(prefixes.values(), key=lambda p: -p['bytes_read'])
    other = prefix_rows[PREFIX_LIMIT:]
    prefix_rows = prefix_rows[:PREFIX_LIMIT]
    if other:
        merged = {'prefix': f'({len(other)} further folders)', 'objects': sum(p['objects'] for p in other), 'bytes_read': sum(p['bytes_read'] for p in other),
                  'hours_decoded': sum(p['hours_decoded'] for p in other), 'hours_speech': sum(p['hours_speech'] for p in other), 'hours_music': sum(p['hours_music'] for p in other), 'languages': Counter()}
        for p in other:
            merged['languages'].update(p['languages'])
        prefix_rows.append(merged)
    for p in prefix_rows:
        top = p['languages'].most_common(1)
        p['top_language'] = top[0][0] if top else None
        p['hours_by_language'] = {k: round(v * 2 / 3600, 3) for k, v in p['languages'].most_common(8)}
        del p['languages']
        for k in ('hours_decoded', 'hours_speech', 'hours_music'):
            p[k] = round(p[k], 3)
    errors = Counter(r['error'] for r in failed)
    denied_bytes = sum(r['size'] for r in failed if r['error'] in ('AccessDenied', 'Forbidden'))
    archived_bytes = sum(r['size'] for r in failed if r['error'] == 'InvalidObjectState')
    if access['state'] in ('denied', 'archived'):
        measurement = access['state']
    elif not meta.get('complete') or pending:
        measurement = 'partial'
    else:
        measurement = 'full'
    gpu_seconds = sum(d.get('elapsed_s', 0) for d in devices)
    audio_hours_this_run = sum(r['duration_s'] for r in this_run_rows) / 3600
    bytes_this_run = sum(r['bytes_read'] for r in this_run_rows)
    return {
        'measurement': measurement, 'access': access['state'], 'access_probe': access.get('probed'), 'inventory_complete': bool(meta.get('complete')),
        'media_objects': len(items), 'media_bytes': media_bytes, 'media_audio_objects': sum(1 for it in items if it[5] == 'audio'), 'media_video_objects': sum(1 for it in items if it[5] == 'video'),
        'objects_read': len(read), 'bytes_read': bytes_read, 'bytes_verified': bytes_verified, 'objects_failed': len(failed), 'failures': dict(errors),
        'objects_denied': sum(1 for r in failed if r['error'] in ('AccessDenied', 'Forbidden')) if access['state'] != 'denied' else len(items),
        'bytes_denied': denied_bytes if access['state'] != 'denied' else media_bytes,
        'objects_archived': sum(1 for r in failed if r['error'] == 'InvalidObjectState') if access['state'] != 'archived' else len(items),
        'bytes_archived': archived_bytes if access['state'] != 'archived' else media_bytes,
        'objects_pending': len(pending) if access['state'] == 'readable' else 0, 'bytes_pending': sum(it[1] for it in pending) if access['state'] == 'readable' else 0,
        'audio_seconds': round(seconds, 1), 'hours_decoded': round(seconds / 3600, 3), 'windows': windows, 'silence_windows': silence, 'music_windows': music, 'speech_windows': speech,
        'abstained_windows': abstained, 'judged_windows': judged, 'hours_music': round(music * 2 / 3600, 3), 'hours_speech': round(speech * 2 / 3600, 3), 'hours_silence': round(silence * 2 / 3600, 3),
        'hours_by_language': {k: round(v * 2 / 3600, 3) for k, v in languages.most_common()}, 'files_top_language': dict(files_top.most_common()),
        'mean_confidence': round(confidence_sum / confidence_n, 4) if confidence_n else None,
        'quality': {'clipped_share': round(clipped_sum / clipped_n, 5) if clipped_n else None, 'level_dbfs_mean': round(level_sum / level_n, 2) if level_n else None,
                    'sample_rates': dict(rates.most_common(6)), 'codecs': dict(codecs.most_common(8)), 'channels': dict(channels.most_common(4)), 'formats_read': dict(formats.most_common())},
        'prefixes': prefix_rows,
        'this_run': {'objects_read': len(this_run_rows), 'bytes_read': bytes_this_run, 'audio_hours': round(audio_hours_this_run, 3), 'run_seconds': round(run_seconds, 1),
                     'mb_per_s': round(bytes_this_run / max(1e-6, run_seconds) / 1e6, 2), 'audio_hours_per_hour': round(audio_hours_this_run / max(1e-6, run_seconds / 3600), 1), 'gpu_seconds': gpu_seconds},
        'source_kind': source_kind,
    }


def _detections(source_id, label, summary, content):
    """Mtafiti contract: the GPU layer emits detections, never verdicts. Byte facts are facts; model readings are detected measures
    pinned to the admitted artefact that produced them. What counts as 'clean' or 'eligible' is decided downstream, not here."""
    from contracts.mtafiti_detection_signal import DetectionSignal, EvidenceClass
    from services.census_autonomy.deep_files import source_ref
    ref = source_ref(source_id, label)
    audio_version = f"audio-language:{(content.get('audio_model_sha256') or 'unpinned')[:16]}"
    music_version = f"music-detector:{(content.get('music_model_sha256') or 'unpinned')[:16]}"
    signals = []
    for name in ('media_bytes', 'bytes_read', 'bytes_verified', 'bytes_denied', 'bytes_archived', 'bytes_pending', 'objects_read', 'objects_denied', 'objects_archived'):
        signals.append(DetectionSignal(signal_name=f'content.{name}={summary[name]}', evidence_class=EvidenceClass.FACT, confidence=1.0, source_ref=ref, detector_version='byte-read:sha256+size+etag'))
    judged = summary['windows'] - summary['silence_windows']
    if judged:
        conf = summary['mean_confidence'] if summary['mean_confidence'] is not None else 0.0
        signals.append(DetectionSignal(signal_name=f"media_composition.music_share={summary['music_windows'] / judged:.4f}", evidence_class=EvidenceClass.DETECTED, confidence=1.0, source_ref=ref, detector_version=music_version))
        signals.append(DetectionSignal(signal_name=f"media_composition.speech_share={summary['speech_windows'] / judged:.4f}", evidence_class=EvidenceClass.DETECTED, confidence=1.0, source_ref=ref, detector_version=music_version))
        signals.append(DetectionSignal(signal_name=f"media_composition.silence_share={summary['silence_windows'] / max(1, summary['windows']):.4f}", evidence_class=EvidenceClass.FACT, confidence=1.0, source_ref=ref, detector_version='rms-threshold:1e-4'))
        if summary['judged_windows']:
            signals.append(DetectionSignal(signal_name=f"language.abstained_share={summary['abstained_windows'] / max(1, summary['speech_windows']):.4f}", evidence_class=EvidenceClass.DETECTED, confidence=min(1.0, max(0.0, conf)), source_ref=ref, detector_version=audio_version))
            for code, hours in list(summary['hours_by_language'].items())[:12]:
                share = hours * 1800 / summary['judged_windows']
                signals.append(DetectionSignal(signal_name=f'language.{code}.speech_hours={hours}', evidence_class=EvidenceClass.DETECTED, confidence=min(1.0, max(0.0, conf)), source_ref=ref, detector_version=audio_version))
                signals.append(DetectionSignal(signal_name=f'language.{code}.judged_share={share:.4f}', evidence_class=EvidenceClass.DETECTED, confidence=min(1.0, max(0.0, conf)), source_ref=ref, detector_version=audio_version))
    return [s.model_dump(mode='json') for s in signals]


# ----------------------------------------------------------------------------------------------------------------- orchestration
def _spawn_devices(content, hop, obs, folder_map, queues, stop_at, run_dir, bundle):
    procs = {}
    for index, work in queues.items():
        control = {'queue': work, 'stop_at': stop_at, 'run_dir': str(run_dir), 'content': {k: v for k, v in content.items() if k not in ('state_dir',)},
                   'obs': obs, 'hop': hop, 'folders': folder_map, 'device': index}
        log = open(run_dir / f'device_{index}.log', 'ab')
        proc = subprocess.Popen([content['gpu_python'], '-c', DEVICE_MAIN, bundle, str(run_dir), str(index)],
                                stdin=subprocess.PIPE, stdout=log, stderr=subprocess.STDOUT,
                                env={**os.environ, 'CUDA_VISIBLE_DEVICES': str(index), 'OMP_NUM_THREADS': '8', 'HF_HUB_OFFLINE': '1', 'TOKENIZERS_PARALLELISM': 'false'})
        proc.stdin.write(json.dumps(control).encode()); proc.stdin.close()
        procs[index] = proc
    return procs


def _wait_devices(procs, stop_at, run_dir, progress):
    while any(p.poll() is None for p in procs.values()):
        time.sleep(10)
        progress(run_dir)
        if time.time() > stop_at + 60:
            for p in procs.values():
                if p.poll() is None:
                    p.kill()
    return [_read_json(run_dir / f'progress_{i}.json', {'device': i, 'exit_code': p.returncode}) | {'exit_code': p.returncode} for i, p in procs.items()]


def _balance(items, devices):
    queues, load = {d: [] for d in devices}, {d: 0 for d in devices}
    for item in sorted(items, key=lambda it: -it['size']):
        target = min(load, key=load.get)
        queues[target].append(item); load[target] += item['size']
    for work in queues.values():
        work.sort(key=lambda it: (it['kind'] != 'audio', it['label'], it['key']))
    return queues


def content_pass(config, labels, deadline, source_kind, root=None, hop=None):
    """Inventory → access verdict → read everything pending on every GPU of this host until the run's stop time → aggregate."""
    content = config['content']
    started = time.time()
    stop_at = deadline - STOP_MARGIN_S
    devices = _gpus()
    if not devices:
        raise ValueError('NO_GPU_VISIBLE')
    state_root = Path(content['state_dir']).expanduser()
    (state_root / config['source_id']).mkdir(parents=True, exist_ok=True)
    import fcntl
    guard = (state_root / config['source_id'] / '.content.lock').open('a')
    try:
        fcntl.flock(guard, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise ValueError('ENUMERATION_ALREADY_RUNNING')  # a previous pass on this source is still reading; the engine defers and re-enters
    try:
        return _content_pass(config, labels, deadline, source_kind, root, hop, content, started, stop_at, devices, state_root)
    finally:
        fcntl.flock(guard, fcntl.LOCK_UN); guard.close()


def _content_pass(config, labels, deadline, source_kind, root, hop, content, started, stop_at, devices, state_root):
    run_dir = Path(content['scratch_dir']).expanduser() / f"run-{config['source_id']}-{int(started)}"
    run_dir.mkdir(parents=True, exist_ok=True)
    for stale in Path(content['scratch_dir']).expanduser().glob(f"run-{config['source_id']}-*"):
        if stale != run_dir:
            shutil.rmtree(stale, ignore_errors=True)
    sdk = _sdk(config) if source_kind == 'object_store' else None
    sftp_client = sftp = None
    if source_kind == 'nas':
        sftp_client, sftp = _sftp_client(hop)
    folders = {label: _label_dir(state_root, config['source_id'], label) for label in labels}
    metas, accesses, items_by_label = {}, {}, {}
    # Listing takes a bounded share of each run; the frontier resumes next run and reading starts with whatever is inventoried.
    inventory_stop = min(stop_at, started + (deadline - started) * INVENTORY_SHARE)
    for label in sorted(labels, key=lambda l: (_read_json(folders[l] / 'inventory.json', {}).get('complete') is not True, labels.index(l))):
        metas[label] = _inventory_obs(sdk, label, folders[label], inventory_stop) if source_kind == 'object_store' else _inventory_nas(sftp, root, label, folders[label], inventory_stop)
        items_by_label[label] = _media_items(folders[label])
        accesses[label] = _probe_access(sdk, label, items_by_label[label], folders[label]) if source_kind == 'object_store' else {'state': 'readable' if items_by_label[label] else 'no_media', 'probed': None, 'items': len(items_by_label[label]), 'at': now()}
    work = []
    for label in labels:
        if accesses[label]['state'] != 'readable':
            continue
        done = _done_refs(folders[label])
        for key, size, etag, modified, storage_class, kind in items_by_label[label]:
            ref = ref_of(label, key)
            if ref not in done:
                work.append({'label': label, 'key': key, 'size': size, 'etag': etag, 'modified': modified, 'storage_class': storage_class, 'kind': kind, 'ref': ref})
    queues = _balance(work, devices) if work and time.time() < stop_at - 60 else {}
    bundle = next(p for p in sys.path if p.endswith('worker.zip'))
    obs = {k: config[k] for k in ('endpoint', 'region', 'access_key_id', 'secret_access_key')} if source_kind == 'object_store' else None
    folder_map = {label: str(folders[label]) for label in labels}
    before = {label: _done_refs(folders[label]) for label in labels}
    device_reports = []
    if queues:
        for index, items in queues.items():
            (run_dir / f'queue_{index}.json').write_text(json.dumps(items))
        procs = _spawn_devices(content, hop if source_kind == 'nas' else None, obs, folder_map, {i: str(run_dir / f'queue_{i}.json') for i in queues}, stop_at, run_dir, bundle)
        device_reports = _wait_devices(procs, stop_at, run_dir, lambda d: None)
    if sftp_client:
        sftp_client.close()
    run_seconds = time.time() - started
    entries = []
    for label in labels:
        meta, items, access = metas[label], items_by_label[label], accesses[label]
        new_rows = [row for ref, row in _rows(folders[label]).items() if ref not in before[label] and not row.get('error')]
        summary = _aggregate(folders[label], items, access, meta, label, source_kind, run_seconds, device_reports, new_rows)
        summary['models'] = {'audio_language': {'artefact_dir': Path(content['audio_model_dir']).name, 'sha256': content.get('audio_model_sha256')},
                             'music_detector': {'artefact_path': Path(content['music_model_path']).parent.name, 'sha256': content.get('music_model_sha256')}}
        summary['detections'] = _detections(config['source_id'], label, summary, content)
        summary['devices'] = len(devices)
        summary['device_reports'] = device_reports
        complete = meta.get('complete') and summary['measurement'] in ('full', 'denied', 'archived', 'no_media')
        entry = {'label': label, 'kind': source_kind, 'status': 'complete' if complete else 'partial',
                 ('object_count' if source_kind == 'object_store' else 'file_count'): meta['objects'], 'volume_bytes': meta['bytes'], 'formats': dict(meta.get('formats') or {}),
                 'date_min': meta.get('date_min'), 'date_max': meta.get('date_max'), 'pages': meta.get('pages'), 'directories_complete': meta.get('directories'), 'directories_pending': len(meta.get('pending') or []),
                 'duplicate_candidates': _duplicate_candidates(folders[label], meta) if source_kind == 'object_store' and meta.get('complete') else None,
                 'enumeration': 'full' if meta.get('complete') else 'partial', 'content_measurement': summary['measurement'], 'content': summary,
                 'database_count': 0, 'table_count': 0, 'row_count_estimate': 0, 'epoch': 1, 'runs_in_epoch': None, 'resumable': True,
                 'media_samples': summary['objects_read'], 'media_duration_seconds': summary['audio_seconds'], 'media_failures': summary['objects_failed'],
                 'method': ('Full-content census on the admitted GPU host: every key listed (resumable inventory on the host volume), every media object read byte for byte '
                            'and verified against the listing, decoded in full and judged on every consecutive two-second window by the admitted music detector and the '
                            'current audio language model on every GPU of the host; per-object rows stay on the host; aggregates only in this receipt; successive bounded '
                            'runs resume until every readable object is read. Objects the key cannot read are counted as denied or archived, never estimated.')}
        if not complete:
            entry['reason_code'] = 'BUDGET_EXHAUSTED' if not meta.get('list_error') else meta['list_error']
        if summary['measurement'] == 'denied':
            entry['content_reason_code'] = 'CONTENT_GET_DENIED'
        elif summary['measurement'] == 'archived':
            entry['content_reason_code'] = 'CONTENT_ARCHIVED_RESTORE_REQUIRED'
        entries.append(entry)
    logs = state_root / config['source_id'] / 'logs'
    logs.mkdir(parents=True, exist_ok=True)
    for log in run_dir.glob('device_*.log'):
        shutil.copy(log, logs / f"{int(started)}_{log.name}")
    for old in sorted(logs.glob('*.log'))[:-24]:
        old.unlink(missing_ok=True)
    shutil.rmtree(run_dir, ignore_errors=True)
    return entries


def _ordered(config, labels, source_id):
    """Audio-rich stores first (retained enumeration's audio-file counts, supplied by the control plane), then the commissioned order."""
    from services.census_autonomy.deep_files import source_ref
    priority = {label: i for i, label in enumerate((config.get('content') or {}).get('priority_labels') or [])}
    order = {ref: i for i, ref in enumerate(config.get('source_refs') or [])}
    return sorted(labels, key=lambda l: (priority.get(l, 1 << 30), order.get(source_ref(source_id, l), 1 << 30), l))


def objects_full(config, deadline):
    sdk = _sdk(config)
    from services.census_autonomy.deep_files import source_ref
    buckets = [b['Name'] for b in sdk.list_buckets()['Buckets'] if not config.get('source_refs') or source_ref(config['source_id'], b['Name']) in config['source_refs']]
    if not buckets:
        raise ValueError('OBS_NO_BUCKETS_IN_SCOPE')
    return content_pass(config, _ordered(config, buckets, config['source_id']), deadline, 'object_store')


def nas_full(config, deadline):
    from services.census_autonomy.deep_files import source_ref
    hop = config['pull_via']
    client, sftp = _sftp_client(hop)
    try:
        import stat as st
        root = config['root'].rstrip('/')
        channels = sorted(e.filename for e in sftp.listdir_attr(root) if st.S_ISDIR(e.st_mode) and not st.S_ISLNK(e.st_mode)
                          and (not config.get('source_refs') or source_ref(config['source_id'], e.filename) in config['source_refs']))
    finally:
        client.close()
    if not channels:
        raise ValueError('NAS_NO_CHANNELS_OBSERVED')
    return content_pass(config, _ordered(config, channels, config['source_id']), deadline, 'nas', root=root, hop=hop)


# ----------------------------------------------------------------------------------------------------------------- GPU device reader
def _ffprobe(path):
    try:
        p = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,bit_rate,format_name:stream=codec_type,codec_name,sample_rate,channels', '-of', 'json', str(path)],
                           capture_output=True, text=True, timeout=120)
        probe = json.loads(p.stdout or '{}')
    except Exception:
        return {}
    audio = next((s for s in probe.get('streams', []) if s.get('codec_type') == 'audio'), {})
    fmt = probe.get('format', {})
    return {'codec': audio.get('codec_name'), 'sample_rate': int(audio['sample_rate']) if audio.get('sample_rate') else None, 'channels': audio.get('channels'),
            'container': fmt.get('format_name'), 'container_duration_s': round(float(fmt['duration']), 2) if fmt.get('duration') else None,
            'bit_rate': int(fmt['bit_rate']) if fmt.get('bit_rate') else None, 'audio_streams': sum(1 for s in probe.get('streams', []) if s.get('codec_type') == 'audio'),
            'video_streams': sum(1 for s in probe.get('streams', []) if s.get('codec_type') == 'video')}


def _download_obs(sdk, item, path):
    sha, md5, n = hashlib.sha256(), hashlib.md5(), 0
    body = sdk.get_object(Bucket=item['label'], Key=item['key'])['Body']
    with open(path, 'wb') as out:
        for chunk in iter(lambda: body.read(1 << 20), b''):
            out.write(chunk); sha.update(chunk); md5.update(chunk); n += len(chunk)
    return n, sha.hexdigest(), md5.hexdigest()


def _download_nas(sftp, root, item, path):
    sha, n = hashlib.sha256(), 0
    with sftp.open(f"{root}/{item['key']}", 'rb') as src, open(path, 'wb') as out:
        src.prefetch()
        for chunk in iter(lambda: src.read(1 << 20), b''):
            out.write(chunk); sha.update(chunk); n += len(chunk)
    return n, sha.hexdigest(), None


def _judge(models, pcm, device, batch, stats):
    """Every consecutive two-second window of this block: music probability, language label and confidence, level and clipping."""
    import numpy as np
    import torch
    count = pcm.shape[0] // WIN
    if count == 0:
        return
    windows = pcm[:count * WIN].reshape(count, WIN)
    rms = np.sqrt((windows ** 2).mean(1))
    loud = rms > 1e-4
    stats['windows'] += count
    stats['silence'] += int((~loud).sum())
    stats['clipped'] += int((np.abs(windows) >= 0.99).sum())
    stats['samples'] += int(windows.size)
    if loud.any():
        stats['level_sum'] += float((20 * np.log10(rms[loud])).sum()); stats['level_n'] += int(loud.sum())
    windows = windows[loud]
    classes, threshold, music_threshold = models['classes'], models['threshold'], models['music_threshold']
    with torch.no_grad():
        for i in range(0, len(windows), batch):
            chunk = torch.from_numpy(np.ascontiguousarray(windows[i:i + batch])).to(device)
            pcm16 = (chunk * 32767.0).to(torch.int16)
            with torch.autocast('cuda', dtype=torch.bfloat16):
                enc = models['encoder'](input_features=models['featurizer'](pcm16)).last_hidden_state.mean(1)
            probs = torch.softmax(models['language_head'](models['project'](enc.float())), dim=-1)
            conf, idx = probs.max(dim=-1)
            music_p = torch.sigmoid(models['music'](models['music_featurizer'](chunk)).squeeze(1))
            is_music = music_p >= music_threshold
            judged = (~is_music) & (conf >= threshold)
            stats['music'] += int(is_music.sum())
            stats['abstained'] += int(((~is_music) & (conf < threshold)).sum())
            stats['conf_sum'] += float(conf[~is_music].sum()); stats['conf_n'] += int((~is_music).sum())
            for label in idx[judged].tolist():
                stats['by_language'][classes[label]] += 1


def _read_item(models, item, path, control, device):
    """Decode the whole object as 16 kHz mono through ffmpeg in bounded blocks; judge every window; nothing is skipped."""
    import numpy as np
    stats = {'windows': 0, 'silence': 0, 'music': 0, 'abstained': 0, 'by_language': Counter(), 'conf_sum': 0.0, 'conf_n': 0, 'clipped': 0, 'samples': 0, 'level_sum': 0.0, 'level_n': 0}
    block = int(control['content'].get('block_windows', 2048)) * WIN
    cmd = ['ffmpeg', '-v', 'error', '-nostdin', '-i', str(path), '-vn', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-']
    errlog = tempfile.TemporaryFile()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=errlog)
    carry = b''
    total_samples = 0
    err = ''
    try:
        while True:
            raw = proc.stdout.read(block * 4)
            if not raw:
                break
            raw = carry + raw
            usable = (len(raw) // (WIN * 4)) * WIN * 4
            carry = raw[usable:]
            if usable:
                pcm = np.frombuffer(raw[:usable], dtype=np.float32)
                total_samples += pcm.shape[0]
                _judge(models, pcm, device, int(control['content'].get('batch_size', 256)), stats)
            if time.time() > control['stop_at'] + 30:
                proc.kill(); raise TimeoutError('RUN_STOP')
        total_samples += len(carry) // 4
        proc.wait(timeout=60)
        errlog.seek(0); err = errlog.read().decode(errors='replace')[-300:]
    finally:
        if proc.poll() is None:
            proc.kill()
        errlog.close()
    if total_samples == 0:
        raise ValueError('DECODE_FAILED:' + (err.strip().splitlines() or ['no audio stream decoded'])[-1][:120])
    judged = sum(stats['by_language'].values())
    top = stats['by_language'].most_common(1)
    return {'duration_s': round(total_samples / SR, 2), 'windows': stats['windows'], 'tail_seconds': round((len(carry) // 4) / SR, 3), 'silence_windows': stats['silence'],
            'music_windows': stats['music'], 'speech_windows': stats['windows'] - stats['silence'] - stats['music'], 'abstained': stats['abstained'], 'judged': judged,
            'by_language': dict(stats['by_language']), 'top_language': top[0][0] if top else None, 'top_share': round(top[0][1] / judged, 4) if judged else None,
            'mean_confidence': round(stats['conf_sum'] / stats['conf_n'], 4) if stats['conf_n'] else None,
            'music_share': round(stats['music'] / max(1, stats['windows'] - stats['silence']), 4),
            'clipped_share': round(stats['clipped'] / stats['samples'], 6) if stats['samples'] else None,
            'level_dbfs': round(stats['level_sum'] / stats['level_n'], 2) if stats['level_n'] else None, 'decoder_note': err.strip()[-120:] or None}


def run_device(control, run_dir, index):
    """One GPU: downloader threads keep the scratch volume fed, the main thread decodes and judges; rows append per object."""
    import torch
    from services.training_lab.estate_language_worker import _load_models
    torch.backends.cuda.matmul.allow_tf32 = True
    run_dir = Path(run_dir)
    queue_items = json.loads(Path(control['queue']).read_text())
    stop_at = float(control['stop_at'])
    scratch = run_dir / f'scratch_{index}'
    scratch.mkdir(parents=True, exist_ok=True)
    started = time.time()
    progress = {'device': index, 'files': 0, 'of': len(queue_items), 'bytes': 0, 'audio_seconds': 0.0, 'windows': 0, 'errors': 0, 'elapsed_s': 0, 'stage': 'loading models'}
    (run_dir / f'progress_{index}.json').write_text(json.dumps(progress))
    device = 'cuda'
    models = _load_models({'lab_corpus_root': control['content']['lab_corpus_root'], 'audio_model_dir': control['content']['audio_model_dir'], 'music_model_path': control['content']['music_model_path']}, device)
    inflight_limit = int(control['content'].get('prefetch_bytes', 4 << 30))
    ready, inflight, lock = queue.Queue(), [0], threading.Lock()
    workers = int(control['content'].get('download_workers', 6))
    sdk = _sdk(control['obs']) if control.get('obs') else None
    hop = control.get('hop')
    root = control['content'].get('nas_root')
    cursor = [0]

    def downloader():
        sftp_client = sftp = None
        if hop:
            sftp_client, sftp = _sftp_client(hop)
        try:
            while time.time() < stop_at:
                with lock:
                    if cursor[0] >= len(queue_items):
                        return
                    item = queue_items[cursor[0]]; cursor[0] += 1
                while inflight[0] > inflight_limit and time.time() < stop_at:
                    time.sleep(0.5)
                path = scratch / f"{item['ref']}{Path(item['key']).suffix.lower()[:8]}"
                try:
                    n, sha, md5 = _download_obs(sdk, item, path) if sdk else _download_nas(sftp, root, item, path)
                    with lock:
                        inflight[0] += n
                    ready.put((item, path, n, sha, md5, None))
                except Exception as exc:
                    code = (getattr(exc, 'response', {}) or {}).get('Error', {}).get('Code') if hasattr(exc, 'response') else None
                    try:
                        path.unlink()
                    except OSError:
                        pass
                    ready.put((item, None, 0, None, None, (code or type(exc).__name__)[:60]))
        finally:
            if sftp_client:
                sftp_client.close()
            ready.put(None)

    threads = [threading.Thread(target=downloader, daemon=True) for _ in range(workers)]
    for t in threads:
        t.start()
    finished = 0
    progress['stage'] = 'reading'
    handles = {}
    try:
        while finished < len(threads):
            got = ready.get()
            if got is None:
                finished += 1
                continue
            item, path, n, sha, md5, error = got
            row = {'ref': item['ref'], 'label': item['label'], 'prefix': item['key'].split('/')[0] if '/' in item['key'] else '(root)', 'ext': Path(item['key']).suffix.lower(),
                   'kind': item['kind'], 'size': item['size'], 'storage_class': item['storage_class'], 'modified': item['modified'][:10], 'device': index, 'read_at': now(),
                   'bytes_read': n, 'sha256': sha, 'size_match': (n == item['size']) if path else False, 'etag_match': (md5 == item['etag']) if (md5 and item['etag'] and '-' not in item['etag']) else None}
            if error:
                row['error'] = error
            else:
                try:
                    row.update(_ffprobe(path))
                    row.update(_read_item(models, item, path, control, device))
                except TimeoutError:
                    row = None
                except Exception as exc:
                    row['error'] = (str(exc)[:80] if str(exc).startswith('DECODE_FAILED') else type(exc).__name__)[:80]
                finally:
                    with lock:
                        inflight[0] -= n
                    try:
                        path.unlink()
                    except OSError:
                        pass
            if row is None:
                continue
            handle = handles.get(item['label'])
            if handle is None:
                handle = handles[item['label']] = (Path(control['folders'][item['label']]) / f'rows_{index}.jsonl').open('a')
            handle.write(json.dumps(row, sort_keys=True) + '\n'); handle.flush()
            progress['files'] += 1; progress['bytes'] += n; progress['errors'] += 1 if row.get('error') else 0
            progress['audio_seconds'] = round(progress['audio_seconds'] + (row.get('duration_s') or 0), 1); progress['windows'] += row.get('windows') or 0
            progress['elapsed_s'] = int(time.time() - started); progress['gpu_peak_gb'] = round(torch.cuda.max_memory_allocated() / 2 ** 30, 2)
            progress['mb_per_s'] = round(progress['bytes'] / max(1e-6, time.time() - started) / 1e6, 2)
            progress['audio_hours_per_hour'] = round(progress['audio_seconds'] / 3600 / max(1e-6, (time.time() - started) / 3600), 1)
            (run_dir / f'progress_{index}.json').write_text(json.dumps(progress))
    finally:
        for handle in handles.values():
            handle.close()
    progress.update(stage='stopped at the run boundary' if cursor[0] < len(queue_items) or time.time() >= stop_at else 'queue complete', elapsed_s=int(time.time() - started), finished=True,
                    not_reached=len(queue_items) - progress['files'])
    (run_dir / f'progress_{index}.json').write_text(json.dumps(progress))
    shutil.rmtree(scratch, ignore_errors=True)
