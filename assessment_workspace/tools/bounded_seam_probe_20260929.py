"""Bounded live probe of the deep worker over the pull seam. Same bundle, same
seams, short budget. Usage: python bounded_seam_probe_20260929.py <source> <runtime> <seconds>
Returns the sanitized worker receipt; no source bytes or credentials are printed."""
import hashlib, json, os, re, shlex, sys, time
from pathlib import Path
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')
from services.census_autonomy.deep_bundle import build_bundle, BOOTSTRAP
from services.census_autonomy.deep_dispatch import connector_for, pull_seam_hop, JUMP_GOVERNED_SOURCES
from services.census_autonomy.jump_dispatch import _connect_jump, _jump_config
from services.census_autonomy.remote_dispatch import _connect

source, runtime, seconds = sys.argv[1], sys.argv[2], int(sys.argv[3])
started = time.time(); deadline = started + seconds
config = connector_for('cr-000000000000', 'RMS', source, 'probe')
if len(sys.argv) > 4: config['parallelism'] = int(sys.argv[4])
if runtime != 'non_gpu_jump' and source in JUMP_GOVERNED_SOURCES: config['pull_via'] = pull_seam_hop()
if runtime == 'non_gpu_jump':
    client = _connect_jump(_jump_config(), 20); expected = os.environ['CENSUS_JUMP_HOSTNAME']
else:
    client, host_config = _connect(runtime, 20); expected = host_config.hostname_expected
print(f'connected {runtime} in {time.time()-started:.1f}s', flush=True)
bundle, code_hash = build_bundle()
remaining = int(deadline - time.time()); margin = min(45, max(2, remaining // 4))
control = {'bundle': bundle, 'code_sha256': code_hash, 'census_run_id': 'cr-000000000000', 'tenant_id': 'RMS',
           'source_id': source, 'runtime_id': runtime, 'hostname_expected': expected,
           'lawful_basis_sha256': 'probe', 'max_seconds': remaining - margin, 'connector': config}
channel = client.get_transport().open_session(timeout=15); channel.settimeout(remaining)
channel.exec_command(shlex.quote(os.environ['CENSUS_REMOTE_PYTHON']) + ' -c ' + shlex.quote(BOOTSTRAP))
channel.sendall(json.dumps(control).encode()); channel.shutdown_write()
output = bytearray(); diagnostic = bytearray(); timed_out = False
while True:
    if channel.recv_ready(): output.extend(channel.recv(65536))
    if channel.recv_stderr_ready(): diagnostic.extend(channel.recv_stderr(65536))
    if channel.exit_status_ready() and not channel.recv_ready() and not channel.recv_stderr_ready(): break
    if time.time() >= deadline + 30: timed_out = True; channel.close(); break
    time.sleep(.05)
wall = time.time() - started
code = None if timed_out else channel.recv_exit_status(); client.close()
text = diagnostic.decode(errors='replace')
text = re.sub(r'(password|secret|Password|Secret)[^\s,]*', r'\1=REDACTED', text)
print(f'exit={code} timed_out={timed_out} wall={wall:.1f}s stdout={len(output)}B stderr={len(diagnostic)}B', flush=True)
if diagnostic: print('--- stderr tail ---'); print(text[-2500:])
summary = {'at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'source': source, 'runtime': runtime,
           'budget_seconds': seconds, 'wall_seconds': round(wall, 1), 'exit_code': code, 'timed_out': timed_out,
           'stdout_bytes': len(output), 'stderr_sha256': hashlib.sha256(diagnostic).hexdigest(),
           'error_classes': re.findall(r'^([A-Za-z]+(?:Error|Exception)):', text, re.M)}
if output and code == 0:
    value = json.loads(output)
    worker = value.get('worker', {})
    summary.update(status=value.get('status'), reason_code=value.get('reason_code'), worker_wall=worker.get('wall_seconds'),
                   hostname=worker.get('telemetry', {}).get('hostname'), pull_seam=worker.get('pull_seam'),
                   sources=[{k: s.get(k) for k in ('label', 'status', 'reason_code', 'file_count', 'object_count', 'volume_bytes',
                                                   'directories_complete', 'directories_pending', 'epoch', 'runs_in_epoch', 'progress_this_run', 'resumable', 'checkpoint_sha256', 'pages', 'errors', 'media_samples', 'enumeration')}
                            for s in value.get('sources', [])])
print(json.dumps(summary, indent=1, default=str))
out = Path('/app/assessment_workspace/notes/m1_execution/logs'); out.mkdir(exist_ok=True)
(out / f'bounded_probe_{source}_{runtime}_{summary["at_utc"].replace(":", "")}.json').write_text(json.dumps(summary, indent=2, default=str))
