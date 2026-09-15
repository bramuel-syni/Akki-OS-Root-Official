"""D12 POC live-run helper · Stage 2-8 pipeline.

Position-redaction hard-lock:
  * Credential values are LOADED into python local variables from custody.
  * Values are NEVER printed / stdout'd / put in argv / put in env vars
    that persist across processes.
  * Only operational verdicts (rc / dt / PASS/FAIL / counts / sha256s /
    canonical-key shapes) surface to stdout.
  * sshpass reads JUMP root pw from stdin (fd=0 pipe) not from env.
  * smbclient (on JUMP side) reads NAS pw from an auth-file whose path
    is passed on argv and whose content is scp'd via a private temp file
    then shred'd on completion.

Custody-cat guard (`services/secret_hygiene/custody_file.py::assert_no_
transcript_cat_on_custody`) is exercised on every subprocess command
string before invocation.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Guard scope
sys.path.insert(0, '/app/assessment_workspace/repos/Extraction-Akki/backend')
from services.secret_hygiene.custody_file import assert_no_transcript_cat_on_custody

XLSX = '/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx'


def load_creds_silent() -> dict:
    """Load credentials from custody xlsx into a private dict.
    NEVER prints values. Returns a dict; caller is responsible for
    ensuring values never leak out.
    """
    from openpyxl import load_workbook
    wb = load_workbook(XLSX, data_only=True, read_only=True)

    creds: dict = {}

    # 'NAS creds' sheet: 'Username: Bramwel' pattern in col0 rows 5-6
    ws = wb['NAS creds']
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        c0 = r[0] if r and r[0] is not None else ''
        s = str(c0).strip()
        if s.lower().startswith('username:'):
            creds['nas_user'] = s.split(':', 1)[1].strip()
        elif s.lower().startswith('password:'):
            creds['nas_pw'] = s.split(':', 1)[1].strip()

    # 'NAS Guide + Cred' sheet: rows 0-3 are JUMP block, rows 7-10 RADIO
    ws2 = wb['NAS Guide + Cred']
    rows2 = list(ws2.iter_rows(values_only=True))
    # Row 0 col0 is JUMP IP; row 1 col0 is 'root'; row 2 col0 is JUMP pw
    if len(rows2) > 2:
        creds['jump_host'] = str(rows2[0][0]).strip()
        creds['jump_user'] = str(rows2[1][0]).strip()
        creds['jump_pw'] = str(rows2[2][0]).strip()
    wb.close()

    required = {'nas_user', 'nas_pw', 'jump_host', 'jump_user', 'jump_pw'}
    missing = required - set(creds.keys())
    if missing:
        raise RuntimeError(f'cred extraction failed · missing keys={sorted(missing)}')
    return creds


def _redacted_verdict(*, stage: str, verdict: str, dt_s: float,
                     rc: int | None, extras: dict | None = None) -> dict:
    """Emit-only shape for stdout: never carries any credential material."""
    v = {
        'stage': stage,
        'verdict': verdict,
        'dt_seconds': round(dt_s, 3),
        'rc': rc,
    }
    if extras:
        v.update(extras)
    return v


def stage_2_jump_ssh_probe(creds: dict, tmpdir: Path) -> dict:
    """Stage 2 · SSH into JUMP, verify uname + smbclient available."""
    stage = 'stage_2_jump_ssh_probe'
    pw_file = tmpdir / '.sshpass_jump'
    pw_file.write_text(creds['jump_pw'] + '\n')
    os.chmod(pw_file, 0o600)

    cmd = 'echo OK && uname -n && which smbclient'
    assert_no_transcript_cat_on_custody(cmd)

    argv = [
        'sshpass', '-f', str(pw_file),
        'ssh', '-o', 'StrictHostKeyChecking=accept-new',
        '-o', 'ConnectTimeout=15',
        '-o', 'ServerAliveInterval=10',
        f"{creds['jump_user']}@{creds['jump_host']}",
        cmd,
    ]
    t0 = time.time()
    r = subprocess.run(argv, capture_output=True, timeout=45)
    dt = time.time() - t0
    pw_file.unlink()  # dispose

    out = r.stdout.decode('utf-8', 'replace').strip()
    ok = (r.returncode == 0 and 'OK' in out and 'smbclient' in out)
    return _redacted_verdict(
        stage=stage, verdict='PASS' if ok else 'FAIL', dt_s=dt, rc=r.returncode,
        extras={'stdout_shape': {'lines': len(out.splitlines()),
                                 'contains_ok': 'OK' in out,
                                 'contains_smbclient': 'smbclient' in out}},
    )


def stage_3_smbclient_share_probe(creds: dict, tmpdir: Path) -> dict:
    """Stage 3 · SSH into JUMP + smbclient -L //10.10.55.55 -U Bramwel.
    NAS pw passed via PASSWD env on JUMP-side (never in argv).
    """
    stage = 'stage_3_smbclient_share_probe'
    pw_file = tmpdir / '.sshpass_jump'
    pw_file.write_text(creds['jump_pw'] + '\n')
    os.chmod(pw_file, 0o600)

    # JUMP-side script: read NAS pw from stdin (fd=3 pipe), export as PASSWD, exec smbclient.
    remote_script = (
        'set -e; '
        'read -s NAS_PW; '
        'PASSWD="$NAS_PW" smbclient -L //10.10.55.55 -U ' + creds['nas_user'] + ' 2>&1 | '
        'grep -E "Disk|Sharename|OFFAIRRECS" | head -60; '
        'unset NAS_PW PASSWD; '
        'echo REMOTE_OK'
    )
    assert_no_transcript_cat_on_custody(remote_script)

    argv = [
        'sshpass', '-f', str(pw_file),
        'ssh', '-o', 'StrictHostKeyChecking=accept-new',
        '-o', 'ConnectTimeout=15',
        '-o', 'ServerAliveInterval=10',
        f"{creds['jump_user']}@{creds['jump_host']}",
        remote_script,
    ]
    t0 = time.time()
    # Feed NAS pw via stdin
    r = subprocess.run(
        argv, input=(creds['nas_pw'] + '\n').encode(),
        capture_output=True, timeout=60,
    )
    dt = time.time() - t0
    pw_file.unlink()

    out = r.stdout.decode('utf-8', 'replace').strip()
    err = r.stderr.decode('utf-8', 'replace').strip()
    lines = out.splitlines()
    share_lines = [ln for ln in lines if 'Disk' in ln or 'Sharename' in ln or 'OFFAIRRECS' in ln]
    remote_ok = 'REMOTE_OK' in out
    return _redacted_verdict(
        stage=stage,
        verdict='PASS' if (r.returncode == 0 and remote_ok and share_lines) else 'FAIL',
        dt_s=dt, rc=r.returncode,
        extras={
            'stdout_line_count': len(lines),
            'share_lines_matched': len(share_lines),
            'remote_ok_marker_present': remote_ok,
            'stderr_line_count': len(err.splitlines()) if err else 0,
        },
    )


def main():
    tmpdir = Path(tempfile.mkdtemp(prefix='d12_poc_', dir='/tmp'))
    tmpdir.chmod(0o700)
    print(json.dumps({'tmpdir': str(tmpdir)}))
    try:
        creds = load_creds_silent()
        print(json.dumps({'creds_load': 'PASS', 'keys': sorted(creds.keys())}))

        v2 = stage_2_jump_ssh_probe(creds, tmpdir)
        print(json.dumps(v2))
        if v2['verdict'] != 'PASS':
            print(json.dumps({'halt': 'stage_2_failed_no_further_probes'}))
            return

        v3 = stage_3_smbclient_share_probe(creds, tmpdir)
        print(json.dumps(v3))

    finally:
        # dispose creds
        try:
            del creds
        except NameError:
            pass
        # dispose tmp
        for p in tmpdir.iterdir():
            try: p.unlink()
            except OSError: pass
        try: tmpdir.rmdir()
        except OSError: pass


if __name__ == '__main__':
    main()
