"""Independent watchdog — offline proofs of the host-side judgement, run with the EXACT script E1 installs on the
custody host, under a temporary HOME with a throwaway Ed25519 key. No SSH, no estate, no Mongo write.

Proves: a consistent statement is signed `consistent`; a rewritten Ledger head, a rewritten historical hash, a
truncated feed and a rewritten feed prefix are each signed as `divergence` with the finding named; a gap beyond
twice the agreed interval is signed `silence`; E1's signature verification accepts the host's record and rejects
a record altered after signing; the host chain is append-only across passes.
"""
import base64
import hashlib
import json
import os
import subprocess
import sys
import time

import pytest

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')

from services.watch import independent_witness as iw  # noqa: E402


@pytest.fixture
def host(tmp_path):
    home = tmp_path / 'home'
    d = home / '.akki_witness'
    d.mkdir(parents=True)
    subprocess.run(['openssl', 'genpkey', '-algorithm', 'ed25519', '-out', str(d / 'ed25519.pem')], check=True, capture_output=True)
    script = d / 'watch_witness.py'
    script.write_text(iw.SCRIPT, encoding='utf-8')
    env = {**os.environ, 'HOME': str(home)}

    def run(*args):
        out = subprocess.run([sys.executable, str(script), *args], env=env, capture_output=True, text=True)
        assert out.returncode == 0, out.stderr
        return json.loads(out.stdout.strip().splitlines()[-1])
    return run


def statement(seq=10, head='h10', at_prev=None, rows=5, prefix_rows=None, prefix_sha=None, whole='w5', when=None):
    return {'at': when or time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'interval_s': 900,
            'tenants': {'T': {'ledger': {'seq': seq, 'hash': head}, 'ledger_hash_at': at_prev or {},
                              'feed': {'rows': rows, 'sha256': whole, 'prefix_rows': prefix_rows, 'prefix_sha256': prefix_sha}}}, 'actions': 3}


def judge(run, stmt):
    return run('judge', base64.b64encode(json.dumps(stmt, sort_keys=True, separators=(',', ':')).encode()).decode())


def test_first_pass_is_consistent_and_verifiable(host):
    assert host('last') == {}
    entry = judge(host, statement())
    record = entry['record']
    assert record['verdict'] == 'consistent' and record['findings'] == [] and record['witness_seq'] == 1 and record['prev_record_sha256'] is None
    assert record['script_sha256'] == iw.SCRIPT_SHA256
    assert iw._verify(entry)  # E1-side Ed25519 verification against the host's public key
    tampered = {**entry, 'record': {**record, 'verdict': 'divergence'}}
    with pytest.raises(Exception):
        iw._verify(tampered)
    assert host('last')['witness_seq'] == 1


def test_growth_with_matching_history_is_consistent(host):
    judge(host, statement(seq=10, head='h10', rows=5, whole='w5'))
    entry = judge(host, statement(seq=12, head='h12', at_prev={'10': 'h10'}, rows=7, prefix_rows=5, prefix_sha='w5', whole='w7'))
    assert entry['record']['verdict'] == 'consistent' and entry['record']['witness_seq'] == 2 and entry['record']['prev_record_sha256']


@pytest.mark.parametrize('mutation, kind', [
    (dict(seq=10, head='h10-changed', at_prev={'10': 'h10-changed'}), 'ledger_head_rewritten'),
    (dict(seq=12, head='h12', at_prev={'10': 'other'}), 'ledger_history_rewritten'),
    (dict(seq=9, head='h9', at_prev={}), 'ledger_head_regressed'),
    (dict(seq=12, head='h12', at_prev={'10': 'h10'}, rows=3, whole='w3'), 'feed_truncated'),
    (dict(seq=12, head='h12', at_prev={'10': 'h10'}, rows=7, prefix_rows=5, prefix_sha='not-w5', whole='w7'), 'feed_rewritten'),
])
def test_rewrites_and_truncation_are_signed_as_divergence(host, mutation, kind):
    judge(host, statement(seq=10, head='h10', rows=5, whole='w5'))
    entry = judge(host, statement(**mutation))
    assert entry['record']['verdict'] == 'divergence'
    assert kind in [f['kind'] for f in entry['record']['findings']]
    assert iw._verify(entry)


def test_silence_beyond_twice_the_interval_is_signed(host, tmp_path):
    first = judge(host, statement())
    chain = tmp_path / 'home' / '.akki_witness' / 'watch_chain.jsonl'
    lines = chain.read_text().splitlines()
    old = json.loads(lines[-1])
    old['record']['epoch'] -= 5000  # the host's own clock says the last pass was 5000 s ago
    chain.write_text('\n'.join(lines[:-1] + [json.dumps(old, sort_keys=True)]) + '\n')
    entry = judge(host, statement(seq=10, head='h10', at_prev={'10': 'h10'}, rows=5, prefix_rows=5, prefix_sha='w5', whole='w5'))
    assert entry['record']['verdict'] == 'silence' and entry['record']['findings'][0]['kind'] == 'silence' and entry['record']['gap_s'] > 1800
    assert first['record']['witness_seq'] == 1 and entry['record']['witness_seq'] == 2


def test_e1_feed_digest_prefix_matches_host_contract(tmp_path, monkeypatch):
    monkeypatch.setenv('WATCH_OBSERVATIONS_DIR', str(tmp_path))
    (tmp_path / 'T.jsonl').write_text('{"a":1}\n{"a":2}\n{"a":3}\n')
    whole = iw._feed_digests('T', None)
    assert whole['rows'] == 3 and whole['prefix_sha256'] is None
    (tmp_path / 'T.jsonl').write_text('{"a":1}\n{"a":2}\n{"a":3}\n{"a":4}\n')
    later = iw._feed_digests('T', 3)
    assert later['rows'] == 4 and later['prefix_rows'] == 3 and later['prefix_sha256'] == whole['sha256']
    assert hashlib.sha256('{"a":1}\n{"a":2}\n{"a":3}'.encode()).hexdigest() == whole['sha256']
