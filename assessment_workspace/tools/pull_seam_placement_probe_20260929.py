"""Read-only placement probe: where is the NAS reachable from, per the pull seam.

Uses only the existing governed seams (jump_dispatch._connect_jump, remote_dispatch._connect).
No secrets printed; no file contents read; TCP reachability + mount facts only.
"""
import json, os, sys, shlex, time
from pathlib import Path
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')
from services.census_autonomy.jump_dispatch import _connect_jump, _jump_config
from services.census_autonomy.remote_dispatch import _connect

PROBE = r'''
echo HOST=$(hostname)
echo MOUNT_NFS_SHARE=$(mountpoint -q /mnt/nfs-share && echo yes || echo no)
mount | grep -iE 'nfs-share|cifs|nfs' | sed -E 's/(username|password|user|pass)=[^,]*/\1=REDACTED/g' | head -3
echo CHANNEL_DIRS=$(ls -1 /mnt/nfs-share 2>/dev/null | wc -l)
echo SMBCLIENT=$(command -v smbclient >/dev/null && echo yes || echo no)
echo FFPROBE=$(command -v ffprobe >/dev/null && echo yes || echo no)
echo MYSQL=$(command -v mysql >/dev/null && echo yes || echo no)
echo CENSUS_PY=$(test -x /opt/akki-census/bin/python && echo yes || echo no)
for t in 10.10.55.55:445 10.10.55.55:2049 159.138.173.250:22; do
  h=${t%%:*}; p=${t##*:}
  if timeout 4 bash -c "exec 3<>/dev/tcp/$h/$p" 2>/dev/null; then echo TCP_$t=open; else echo TCP_$t=closed; fi
done
'''

def run(client, label):
    _, out, err = client.exec_command('bash -c ' + shlex.quote(PROBE), timeout=40)
    text = out.read().decode(errors='replace'); err.read()
    print(f'== {label}'); print(text.strip())
    return text

facts = {}
for runtime in ['non_gpu_jump', 'akki-vm']:
    client = None
    try:
        if runtime == 'non_gpu_jump':
            client = _connect_jump(_jump_config(), 20)
        else:
            client, _cfg = _connect(runtime, 20)
        facts[runtime] = run(client, runtime)
    except Exception as exc:
        facts[runtime] = f'UNREACHABLE {type(exc).__name__}'
        print(f'== {runtime}: {type(exc).__name__}')
    finally:
        if client: client.close()

out = Path('/app/assessment_workspace/notes/m1_execution/PULL_SEAM_PLACEMENT_PROBE_20260929.json')
out.write_text(json.dumps({'at_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'facts': facts}, indent=2))
print('receipt:', out)
