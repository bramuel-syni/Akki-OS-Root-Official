"""Ship reviewed code, never source data, to the existing external executors."""
import base64
import hashlib
import io
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULES = [
    'contracts/mtafiti_detection_signal.py',
    'services/mtafiti/composition_census.py',
    'services/mtafiti/quality_profiler.py',
    'services/mtafiti/relationship_signals.py',
    'services/mtafiti/gpu_discovery_constants.py',
    'services/mtafiti/probes/live_readonly_probe.py',
    'services/mtafiti/executor/readonly_sql_guard.py',
    'services/mtafiti/detectors/pii_detector.py',
    'services/mtafiti/detectors/pii_redaction_guard.py',
    'services/mtafiti/sampling/deterministic_adaptive_walker.py',
    'services/census_autonomy/deep_worker.py',
    'services/census_autonomy/deep_sql.py',
    'services/census_autonomy/deep_files.py',
]

def build_bundle():
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED) as archive:
        directories=set()
        for name in MODULES:
            for parent in Path(name).parents:
                if str(parent)!='.': directories.add(str(parent))
            entry=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0))
            archive.writestr(entry,(ROOT/name).read_bytes())
        for directory in sorted(directories):
            archive.writestr(zipfile.ZipInfo(directory+'/__init__.py',date_time=(2026,1,1,0,0,0)),b'')
    raw=buffer.getvalue()
    return base64.b64encode(raw).decode(),hashlib.sha256(raw).hexdigest()

# stdin carries credentials only inside the encrypted existing SSH channel. It is
# consumed in memory. Only the code ZIP is written to the remote temporary folder.
BOOTSTRAP = '''import sys,json,base64,tempfile,pathlib,hashlib,runpy
p=json.load(sys.stdin)
b=base64.b64decode(p.pop('bundle'))
if hashlib.sha256(b).hexdigest()!=p['code_sha256']: raise ValueError('CODE_HASH_MISMATCH')
with tempfile.TemporaryDirectory(prefix='akki-census-code-') as d:
 z=pathlib.Path(d)/'worker.zip'; z.write_bytes(b); sys.path.insert(0,str(z))
 from services.census_autonomy.deep_worker import execute
 print(json.dumps(execute(p),sort_keys=True,default=str),flush=True)
'''