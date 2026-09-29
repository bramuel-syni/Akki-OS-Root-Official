"""M3 guard — negative scan: no tenant name in M3 code, M3 configuration or any KindProfile.

    python m3_tenant_name_scan.py            → exit 0 when clean, 1 on any hit

Scope: the M3 modules (estate_admission, extraction_runtime, work_orders, commissioning, the commissioning
router, the native-runtime factory), every field of every registered KindProfile, and the .env keys M3 added.
Tenant names, estate legal names, bucket names and host slugs are data: they live in admission files and on
the ledger, never in these files. Pre-existing M1 .env keys that carry a tenant token are reported separately
as a standing finding (outside the M3 scope, not hidden).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import dotenv_values  # noqa: E402

BACKEND = Path('/app/backend/vendored/extraction_akki/backend')
M3_PATHS = [BACKEND / 'services/estate_admission', BACKEND / 'services/extraction_runtime', BACKEND / 'services/work_orders',
            BACKEND / 'services/commissioning', BACKEND / 'routers/commissioning.py']
M3_ENV_KEYS = ('AKKI_ESTATE_CUSTODY_DIR', 'AKKI_NATIVE_RUNTIME_FACTORY', 'AKKI_NATIVE_RUNTIME_TIMEOUT_SECONDS', 'AKKI_CUSTODY_MAX_GRANT_SECONDS')
TOKENS = [r'\bRMS\b', r'\bDIGICOW\b', r'\bDigiCow\b', r'\bAKKI-TEST\b', r'\bAUDIT-FIXTURE', r'royalmedia', r'Royal Media',
          r'\bakki-vm\b', r'\bakki-vm-ii\b', r'datauploadroyalmedia', r'\brms_mysql\b', r'\brms_obs\b', r'\brms_nas\b',
          r'\bdigicow_rds\b', r'\bdigicow_s3\b', r'demo\.(operator|master_admin|dpo|analyst)']
PATTERN = re.compile('|'.join(TOKENS))


def scan_text(label, text):
    hits = []
    for number, line in enumerate(text.splitlines(), 1):
        match = PATTERN.search(line)
        if match:
            hits.append({'where': f'{label}:{number}', 'token': match.group(0), 'line': line.strip()[:160]})
    return hits


def main():
    hits = []
    for path in M3_PATHS:
        files = [path] if path.is_file() else sorted(path.rglob('*.py'))
        for file in files:
            hits.extend(scan_text(str(file.relative_to(BACKEND)), file.read_text()))
    from services.work_orders import kind_profiles
    for kind, profile in kind_profiles.REGISTRY.items():
        hits.extend(scan_text(f'KindProfile[{kind}]', json.dumps(profile.__dict__, sort_keys=True, default=str)))
    env = dotenv_values('/app/backend/.env')
    for key in M3_ENV_KEYS:
        hits.extend(scan_text(f'.env:{key}', f'{key}={env.get(key, "")}'))
    legacy = [k for k, v in env.items() if k not in M3_ENV_KEYS and PATTERN.search(f'{k}={v or ""}')]
    report = {'clean': not hits, 'hits': hits, 'scanned': [str(p.relative_to(BACKEND)) for p in M3_PATHS] + ['KindProfile registry', '.env (M3 keys)'],
              'kinds_scanned': sorted(kind_profiles.REGISTRY), 'standing_finding_pre_m3_env_keys': legacy}
    print(json.dumps(report, indent=1))
    return 0 if not hits else 1


if __name__ == '__main__':
    sys.exit(main())
