#!/usr/bin/env python3
"""
Broad hygiene sweep · 2026-09-22 · Turn 3 of R-101 sequence
============================================================

Sweeps every tracked file in every git repo present on disk for live secret
material. SHAPE-ONLY output — no values printed, ever.

Repos swept:
    /app (pod main)
    /app/assessment_workspace (state master)
    /app/assessment_workspace/repos/Extraction-Akki (code programme/track-a)
    /app/assessment_workspace/repos/RMS-IQ-Core-2
    /app/assessment_workspace/repos/Akki-OS-V1
    /app/assessment_workspace/repos/Akki-Executive-Core
    /app/assessment_workspace/repos/Akki-Executive-Final

Output: repo → file:line → kind-of-secret label. NO VALUE PRINTED.
"""
import subprocess
import re
import os
import json
from collections import defaultdict, Counter

REPOS = [
    ('/app', 'main'),
    ('/app/assessment_workspace', 'master'),
    ('/app/assessment_workspace/repos/Extraction-Akki', 'programme/track-a'),
    ('/app/assessment_workspace/repos/RMS-IQ-Core-2', 'main'),
    ('/app/assessment_workspace/repos/Akki-OS-V1', 'main'),
    ('/app/assessment_workspace/repos/Akki-Executive-Core', 'main'),
    ('/app/assessment_workspace/repos/Akki-Executive-Final', 'main'),
]

# Patterns to detect. Ordering matters — most specific first.
# Each pattern must match ONLY the shape/key, never capture the value we print.
PATTERNS = [
    ('AWS_ACCESS_KEY_AKIA_ASIA', re.compile(r'\b(A(?:KIA|SIA)[0-9A-Z]{16})\b')),
    ('OPENAI_API_KEY_shape', re.compile(r'\bsk-[A-Za-z0-9_\-]{20,}')),
    ('HUGGINGFACE_TOKEN_hf', re.compile(r'\bhf_[A-Za-z0-9]{30,}')),
    ('GITHUB_TOKEN_ghp_gho_ghu_ghs_ghr', re.compile(r'\bgh[pousr]_[A-Za-z0-9]{30,}')),
    ('GOOGLE_API_KEY_AIza', re.compile(r'\bAIza[0-9A-Za-z_\-]{35}\b')),
    ('SLACK_TOKEN_xox', re.compile(r'\bxox[baprs]-[A-Za-z0-9\-]{10,}')),
    ('STRIPE_KEY_sk_live_or_rk_live', re.compile(r'\b(?:sk|rk)_live_[A-Za-z0-9]{20,}')),
    ('PRIVATE_KEY_PEM_BEGIN', re.compile(r'-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED |)PRIVATE KEY-----')),
    ('MONGODB_URI_WITH_CREDS', re.compile(r'mongodb(?:\+srv)?://[^:\s"\'/]+:[^@\s"\']+@')),
    ('POSTGRESQL_URI_WITH_CREDS', re.compile(r'postgres(?:ql)?://[^:\s"\'/]+:[^@\s"\']+@')),
    ('MYSQL_URI_WITH_CREDS', re.compile(r'mysql://[^:\s"\'/]+:[^@\s"\']+@')),
    ('BEARER_TOKEN_INLINE', re.compile(r'Bearer\s+[A-Za-z0-9\-_\.]{20,}')),
    ('ENV_ASSIGN_EMERGENT_LLM_KEY', re.compile(r'^\s*(?:export\s+)?EMERGENT_LLM_KEY\s*=\s*[^\s#][^\s]+', re.M)),
    ('ENV_ASSIGN_JWT_SECRET', re.compile(r'^\s*(?:export\s+)?JWT_SECRET\s*=\s*[^\s#][^\s]+', re.M)),
    ('ENV_ASSIGN_HUAWEI_OBS_AK', re.compile(r'^\s*(?:export\s+)?HUAWEI_OBS_AK\s*=\s*[^\s#][^\s]+', re.M)),
    ('ENV_ASSIGN_HUAWEI_OBS_SK', re.compile(r'^\s*(?:export\s+)?HUAWEI_OBS_SK\s*=\s*[^\s#][^\s]+', re.M)),
    ('ENV_ASSIGN_ANY_ACCESS_KEY', re.compile(r'^\s*(?:export\s+)?(?:AWS_ACCESS_KEY|ACCESS_KEY_ID|OSS_ACCESS_KEY)[A-Z_]*\s*=\s*[^\s#][^\s]+', re.M)),
    ('ENV_ASSIGN_ANY_SECRET_KEY', re.compile(r'^\s*(?:export\s+)?(?:AWS_SECRET_ACCESS_KEY|SECRET_ACCESS_KEY|OSS_SECRET_KEY|SECRET_KEY)[A-Z_]*\s*=\s*[^\s#][^\s]+', re.M)),
    ('ENV_ASSIGN_API_KEY_generic', re.compile(r'^\s*(?:export\s+)?[A-Z][A-Z0-9_]*(?:API_KEY|APIKEY|_TOKEN|_KEY|_SECRET|PASSWORD|PASSWD|PWD)\s*=\s*[^\s#][^\s]{16,}', re.M)),
    ('SSH_AUTHORIZED_KEY_BODY', re.compile(r'(?:ssh-rsa|ssh-ed25519|ecdsa-sha2-\S+)\s+[A-Za-z0-9+/=]{40,}')),
    ('PASSWORD_ASSIGN_INLINE', re.compile(r'\b(?:password|passwd|pwd)\s*[:=]\s*["\']?[^"\'\s#]{8,}["\']?', re.I)),
]

# Skip patterns to reduce false-positive noise. These are files where these
# patterns are known-fixture / test-vector / documentation.
SKIP_PATH_FRAGMENTS = [
    '/test_', '/tests/', '/testing/', '/__pycache__/',
    '/node_modules/', '/.venv/', '/venv/',
    '/dist/', '/build/', '/.git/',
    '.min.js', '.min.css', '.map',
    'package-lock.json', 'yarn.lock', 'poetry.lock',
    '.snap',
    '/fixture', '/fixtures/',
    '/vendored/', '/vendor/',
]

# Files worth full inspection (even if patterns above are broad)
FOCUS_EXTS = ('.env', '.env.local', '.env.production', '.env.staging', '.env.dev',
              '.yaml', '.yml', '.json', '.py', '.js', '.ts', '.jsx', '.tsx',
              '.md', '.txt', '.sh', '.toml', '.ini', '.cfg', '.conf',
              '.tf', '.tfvars', '.dockerfile', 'Dockerfile',
              '.ipynb', '.pem', '.key', '.crt', '.rc')


def should_skip(path):
    for frag in SKIP_PATH_FRAGMENTS:
        if frag in path:
            return True
    return False


def is_binary(data):
    return b'\x00' in data[:4096]


def sweep_repo(repo_root, branch):
    print(f"\n===REPO {repo_root} · branch={branch}===")
    try:
        files = subprocess.check_output(
            ['git', '-C', repo_root, 'ls-files'],
            timeout=60
        ).decode('utf-8', errors='ignore').splitlines()
    except Exception as e:
        print(f"  SKIP (git ls-files failed): {e}")
        return {'files_swept': 0, 'files_hit': 0, 'hits': []}

    print(f"  tracked_files_total: {len(files)}")

    files_swept = 0
    files_hit = 0
    hits = []
    kind_counter = Counter()

    for fp in files:
        if should_skip(fp):
            continue

        # Only sweep files with focus extensions OR files that are top-of-tree config
        base = os.path.basename(fp)
        _, ext = os.path.splitext(base)
        matches_focus = (ext in FOCUS_EXTS
                         or base in ('Dockerfile', 'Makefile', 'docker-compose.yml', 'docker-compose.yaml')
                         or base.startswith('.env')
                         or base.endswith('rc'))
        if not matches_focus:
            continue

        abs_path = os.path.join(repo_root, fp)
        if not os.path.isfile(abs_path):
            continue

        # Read file bytes
        try:
            with open(abs_path, 'rb') as fh:
                data = fh.read(2 * 1024 * 1024)  # cap at 2 MB
        except Exception:
            continue

        if is_binary(data):
            continue

        try:
            text = data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = data.decode('latin-1')
            except Exception:
                continue

        files_swept += 1
        file_hits = []
        for kind, pat in PATTERNS:
            for m in pat.finditer(text):
                # find line number
                line_no = text.count('\n', 0, m.start()) + 1
                file_hits.append((line_no, kind))
                kind_counter[kind] += 1

        if file_hits:
            files_hit += 1
            # dedupe by (line_no, kind)
            file_hits_ded = sorted(set(file_hits))
            for ln, kind in file_hits_ded:
                hits.append({'file': fp, 'line': ln, 'kind': kind})

    print(f"  files_swept: {files_swept}")
    print(f"  files_with_hit: {files_hit}")
    print(f"  total_hits: {len(hits)}")
    if kind_counter:
        print(f"  by_kind:")
        for k, c in sorted(kind_counter.items(), key=lambda x: -x[1]):
            print(f"    {k}: {c}")

    return {
        'repo': repo_root,
        'branch': branch,
        'tracked_files_total': len(files),
        'files_swept': files_swept,
        'files_with_hit': files_hit,
        'total_hits': len(hits),
        'by_kind': dict(kind_counter),
        'hits': hits,
    }


def main():
    all_results = []
    for repo, branch in REPOS:
        if not (os.path.isdir(os.path.join(repo, '.git')) or os.path.isfile(os.path.join(repo, '.git'))):
            print(f"SKIP {repo} (no .git)")
            continue
        result = sweep_repo(repo, branch)
        all_results.append(result)

    # Emit summary
    print("\n\n============ AGGREGATE SUMMARY ============")
    total_files_swept = sum(r['files_swept'] for r in all_results)
    total_files_hit = sum(r['files_with_hit'] for r in all_results)
    total_hits = sum(r['total_hits'] for r in all_results)
    print(f"repos_swept: {len(all_results)}")
    print(f"total_files_swept: {total_files_swept}")
    print(f"total_files_with_hit: {total_files_hit}")
    print(f"total_hits: {total_hits}")

    agg_kind = Counter()
    for r in all_results:
        for k, v in r['by_kind'].items():
            agg_kind[k] += v
    print("aggregate_by_kind:")
    for k, c in sorted(agg_kind.items(), key=lambda x: -x[1]):
        print(f"  {k}: {c}")

    # Write JSON receipt
    out_path = '/app/assessment_workspace/phase0/hygiene_receipts/20260922T063000Z_broad_sweep_hits.json'
    with open(out_path, 'w') as fh:
        json.dump({
            'sweep_utc': '2026-09-22T06:30:00Z',
            'repos': all_results,
            'aggregate': {
                'repos_swept': len(all_results),
                'total_files_swept': total_files_swept,
                'total_files_with_hit': total_files_hit,
                'total_hits': total_hits,
                'by_kind': dict(agg_kind),
            },
        }, fh, indent=2)
    print(f"\nJSON receipt at: {out_path}")


if __name__ == '__main__':
    main()
