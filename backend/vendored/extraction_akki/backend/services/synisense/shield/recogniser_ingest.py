"""Receipted ingestion of a Category-1 recogniser onto an estate host (WP-A6).

Model ingestion is a registration ACT, not a runtime download (BUILD_PLAN_V2 §0 build hygiene): one explicit, receipted act per model —
performed through the SSH seam by a named principal under a lawful reference — installs the GLiNER2 library into the host worker
environment, fetches one pinned revision into the estate's local cache, hashes every weight file, records the licence declared by the
model card, and writes the entry into `base_registration.json` beside the Qwen bases. The serving process (reader worker) loads the
recogniser from that local path only, with HF offline flags and the egress guard; nothing at request time can reach the network."""
import json
import os
import shlex

from services.model_registry.registry import current_registry_version, register_model
from services.training_runner import m9_dispatch as m9
from services.training_runner.ssh_seam import execute_remote_command

CANDIDATES = {
    # research lead (BUILD_PLAN_V2 §4): schema-conditioned GLiNER2 family, Apache-2.0; qualification decides the primary, never this table
    'gliner2-pii-multi': {'repo': 'fastino/gliner2-privacy-filter-PII-multi', 'kind': 'pii', 'languages_claimed': ['en', 'fr', 'es', 'de', 'it', 'pt', 'nl']},
    'gliner2-multi-v1': {'repo': 'fastino/gliner2-multi-v1', 'kind': 'general', 'languages_claimed': ['multilingual (model card)']},
}
LIBRARY = 'gliner2[local]'
LIBRARY_VERSION = '2.0.0'

_REMOTE = r'''
import hashlib, json, os, sys, re
root, repo, key, revision = sys.argv[1:5]
os.environ['HF_HOME'] = root + '/hf_cache'
from huggingface_hub import snapshot_download
path = snapshot_download(repo, revision=revision or None, cache_dir=root + '/hf_cache/hub', local_files_only=False)
digest, weights, size = hashlib.sha256(), [], 0
for dirpath, _, files in os.walk(path):
    for f in sorted(files):
        if f.endswith(('.safetensors', '.bin', '.pt')):
            p = os.path.join(dirpath, f); weights.append(f); size += os.path.getsize(os.path.realpath(p))
            h = hashlib.sha256()
            with open(p, 'rb') as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b''): h.update(chunk)
            digest.update(f.encode()); digest.update(h.digest())
card = open(os.path.join(path, 'README.md'), encoding='utf-8', errors='replace').read() if os.path.exists(os.path.join(path, 'README.md')) else ''
m = re.search(r'^license:\s*([\w.\-]+)', card, re.M); licence = (m.group(1).strip().lower() if m else 'undeclared')
rev = os.path.basename(path)
reg_path = root + '/base_registration.json'
reg = json.load(open(reg_path)) if os.path.exists(reg_path) else {}
entry = {'repo': repo, 'revision': rev, 'licence_verified': licence, 'weight_sha256': digest.hexdigest(), 'weight_bytes': size, 'weight_files': weights, 'local_path': path, 'role': 'category1_recogniser',
         'library': 'gliner2', 'ingested_at': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(), 'ingestion': 'receipted registration act (WP-A6); no runtime download'}
reg[key] = entry
json.dump(reg, open(reg_path, 'w'), indent=1)
print(json.dumps(entry))
'''


def ingest(host, key, principal_id, lawful_ref, revision='', timeout=900):
    """One receipted act: library into the worker venv, pinned snapshot into the estate cache, hash + licence into base_registration.json, registry entry."""
    cand = CANDIDATES[key]
    py = os.environ['M9_REMOTE_PYTHON']; root = os.environ['M9_REMOTE_ROOT']
    install = execute_remote_command(host, f"{shlex.quote(py)} -m pip install -q {shlex.quote(LIBRARY + '==' + LIBRARY_VERSION)} 2>&1 | tail -3; {shlex.quote(py)} -c 'import gliner2, sys; print(gliner2.__version__ if hasattr(gliner2, \"__version__\") else \"installed\")'",
                                     purpose=f'wp_a6_ingest_library:{key}', timeout=timeout)
    if install.rc != 0: raise RuntimeError(f'library install failed on {host}: {install.stderr_redacted[:300]} {install.stdout_redacted[-300:]}')
    fetch = execute_remote_command(host, f"{shlex.quote(py)} -c {shlex.quote(_REMOTE)} {shlex.quote(root)} {shlex.quote(cand['repo'])} {shlex.quote(key)} {shlex.quote(revision)}", purpose=f'wp_a6_ingest_snapshot:{key}', timeout=timeout)
    if fetch.rc != 0: raise RuntimeError(f'snapshot ingestion failed on {host}: {fetch.stderr_redacted[-400:]}')
    entry = json.loads(fetch.stdout_redacted.strip().splitlines()[-1])
    if not entry['licence_verified'].startswith('apache'): raise RuntimeError(f"licence {entry['licence_verified']!r} declared by the model card is not a verified permissive licence; the entry is recorded on the host but NOT registered for use")
    model_id = f'recogniser-{key}'
    n, models = current_registry_version()
    if model_id not in models:
        register_model(model_id, {'role': 'category1_recogniser', 'base': key, 'base_repo': entry['repo'], 'base_revision': entry['revision'], 'licence_verified': entry['licence_verified'], 'weight_sha256': entry['weight_sha256'], 'weight_bytes': entry['weight_bytes'],
                                  'host': host, 'kind': cand['kind'], 'languages_claimed': cand['languages_claimed'], 'library': f'gliner2=={LIBRARY_VERSION}', 'provenance': 'receipted ingestion act (WP-A6); served offline from the local path by the reader worker; no runtime download',
                                  'ingestion_receipt_ids': [install.receipt_id, fetch.receipt_id], 'registered_by': principal_id, 'lawful_ref': lawful_ref, 'registered_at': m9.now(), 'status': 'registered_unqualified',
                                  'qualification': None, 'owner_ruling_ref': 'OWNER_ORDERS §12 (Wave A autonomous) · BUILD_PLAN_V2 WP-A6'})
    return {'model_id': model_id, 'entry': entry, 'receipts': [install.receipt_id, fetch.receipt_id], 'library_install_tail': install.stdout_redacted[-200:]}


if __name__ == '__main__':
    import sys
    from dotenv import load_dotenv
    load_dotenv('/app/backend/.env')
    host, key, principal = sys.argv[1], sys.argv[2], sys.argv[3]
    print(json.dumps(ingest(host, key, principal, 'OWNER_ORDERS §12 Wave A autonomous · BUILD_PLAN_V2 WP-A6'), indent=1, default=str))
