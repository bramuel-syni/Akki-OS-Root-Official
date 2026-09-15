"""D12-01 attack matrix · 5-approach engineering probe.

Owner directive verbatim (2026-09-15T~10:30Z):
  (a) mount.cifs on JUMP with SMB3.x dialect + rsize=4M + cache=loose · RO · fetch ONE · measure
  (b) smbclient iosize/buffer tuning
  (c) staged fetch NAS→JUMP-disk→akki-vm · measure legs separately
  (d) parallel/segmented ranged reads if share tolerates
  (e) precise NAS admin ask if all fail

Bank throughput matrix. Position-redaction hard-lock throughout.
"""
from __future__ import annotations
import json, os, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, '/app/assessment_workspace/repos/Extraction-Akki/backend')
sys.path.insert(0, '/app/assessment_workspace/tools')
from services.secret_hygiene.custody_file import assert_no_transcript_cat_on_custody
from d12_poc_live_probe import load_creds_silent


TARGET_PATH = 'Record/channel01/2026_09_14/channel01_2026_09_14_00_00_00.mp4'
TARGET_BASENAME = 'channel01_2026_09_14_00_00_00.mp4'


def _ssh_jump(creds, pw_file: Path, remote_cmd: str, timeout: int = 240, nas_pw_stdin: bool = False):
    assert_no_transcript_cat_on_custody(remote_cmd)
    argv = ['sshpass', '-f', str(pw_file), 'ssh',
            '-o', 'StrictHostKeyChecking=accept-new',
            '-o', 'ConnectTimeout=15',
            f"{creds['jump_user']}@{creds['jump_host']}",
            remote_cmd]
    input_bytes = (creds['nas_pw'] + '\n').encode() if nas_pw_stdin else None
    t0 = time.time()
    r = subprocess.run(argv, input=input_bytes, capture_output=True, timeout=timeout)
    return time.time() - t0, r


def approach_a_mount_cifs(creds, tmpdir: Path) -> dict:
    """mount.cifs read-only · SMB3.0 · rsize=4M · cache=loose · fetch ONE file · measure."""
    approach = 'a_mount_cifs_smb3_rsize4M'
    pw_file = tmpdir / '.sshpass_jump'
    pw_file.write_text(creds['jump_pw'] + '\n')
    os.chmod(pw_file, 0o600)

    # Write NAS pw to a temp credentials file on JUMP side (via stdin heredoc)
    # cifs credentials file format: "username=X\npassword=Y\n"
    setup_cmd = (
        'set -e; '
        'sudo -n true 2>/dev/null || { echo NO_SUDO; exit 1; }; '
        'read -s NAS_PW; '
        'CRED=$(mktemp /tmp/cifs_cred.XXXXXX); chmod 600 $CRED; '
        f'printf "username={creds["nas_user"]}\\npassword=$NAS_PW\\n" > $CRED; '
        'MNT=$(mktemp -d /tmp/nas_mnt.XXXXXX); '
        'echo MNT=$MNT; echo CRED=$CRED'
    )
    dt, r = _ssh_jump(creds, pw_file, setup_cmd, timeout=30, nas_pw_stdin=True)
    if r.returncode != 0:
        pw_file.unlink()
        return {'approach': approach, 'verdict': 'SETUP_FAIL',
                'sub_step': 'mktemp_cred', 'rc': r.returncode,
                'stderr_tail': r.stderr.decode('utf-8','replace')[-300:]}
    setup_out = r.stdout.decode('utf-8','replace')
    if 'NO_SUDO' in setup_out:
        pw_file.unlink()
        return {'approach': approach, 'verdict': 'NO_SUDO_ON_JUMP',
                'sub_step': 'sudo_precheck',
                'note': 'mount.cifs requires root; sudo -n not available for JUMP user'}
    mnt = [ln.split('=',1)[1] for ln in setup_out.splitlines() if ln.startswith('MNT=')][0]
    cred = [ln.split('=',1)[1] for ln in setup_out.splitlines() if ln.startswith('CRED=')][0]

    # Mount
    mount_cmd = (
        f'sudo mount -t cifs //10.10.55.55/OFFAIRRECS {mnt} '
        f'-o credentials={cred},vers=3.0,rsize=4194304,wsize=4194304,'
        f'cache=loose,ro,uid=0 2>&1 | tail -5; '
        f'mount | grep {mnt} | head -1 || echo NOT_MOUNTED'
    )
    dt_mount, r = _ssh_jump(creds, pw_file, mount_cmd, timeout=45)
    mount_out = r.stdout.decode('utf-8','replace')
    if 'NOT_MOUNTED' in mount_out:
        cleanup = f'sudo umount -l {mnt} 2>/dev/null; shred -u {cred} 2>/dev/null; rmdir {mnt}'
        _ssh_jump(creds, pw_file, cleanup, timeout=15)
        pw_file.unlink()
        return {'approach': approach, 'verdict': 'MOUNT_FAIL',
                'dt_mount_s': round(dt_mount,3),
                'stdout_tail': mount_out[-400:]}

    # Fetch: cp mounted file to JUMP local · timed
    dest_local = f'/tmp/d12_a_test_{int(time.time())}.mp4'
    fetch_cmd = (
        f'set -e; '
        f'START=$(date +%s.%N); '
        f'timeout 300 cp {mnt}/{TARGET_PATH} {dest_local} 2>&1 | head -3; '
        f'END=$(date +%s.%N); '
        f'BYTES=$(stat -c %s {dest_local} 2>/dev/null || echo 0); '
        f'echo BYTES=$BYTES; '
        f'echo DT_S=$(python3 -c "print(round($END-$START,3))")'
    )
    dt_fetch, r = _ssh_jump(creds, pw_file, fetch_cmd, timeout=310)
    fetch_out = r.stdout.decode('utf-8','replace')
    fetch_err = r.stderr.decode('utf-8','replace')

    # Parse BYTES + DT_S
    bytes_transferred = 0
    dt_measured = None
    for ln in fetch_out.splitlines():
        if ln.startswith('BYTES='):
            try: bytes_transferred = int(ln.split('=',1)[1])
            except: pass
        elif ln.startswith('DT_S='):
            try: dt_measured = float(ln.split('=',1)[1])
            except: pass

    # sha256 the fetched file on JUMP side (safe · non-secret)
    sha_cmd = f'sha256sum {dest_local} 2>/dev/null | head -1 || echo NO_FILE'
    dt_sha, r_sha = _ssh_jump(creds, pw_file, sha_cmd, timeout=30)
    sha_line = r_sha.stdout.decode('utf-8','replace').strip()

    # Cleanup: unmount, shred cred, rm dest
    cleanup_cmd = (
        f'sudo umount -l {mnt} 2>/dev/null; '
        f'shred -u {cred} 2>/dev/null; '
        f'rmdir {mnt} 2>/dev/null; '
        f'stat -c %s {dest_local} 2>/dev/null || echo GONE; '
        f'test -f {dest_local} && ls -la {dest_local} || true'
        # Keep the file on JUMP for potential Approach C staging - don't delete yet
    )
    _ssh_jump(creds, pw_file, cleanup_cmd, timeout=30)

    pw_file.unlink()

    kb_per_s = None
    if dt_measured and dt_measured > 0 and bytes_transferred > 0:
        kb_per_s = bytes_transferred / dt_measured / 1024

    verdict = 'PASS' if (bytes_transferred >= 79000000 and dt_measured and dt_measured < 300) else \
              'PARTIAL' if bytes_transferred > 0 else 'FAIL'

    return {
        'approach': approach,
        'verdict': verdict,
        'dt_setup_s': round(dt,3),
        'dt_mount_s': round(dt_mount,3),
        'dt_fetch_s': round(dt_fetch,3),
        'dt_measured_on_jump_s': dt_measured,
        'bytes_transferred': bytes_transferred,
        'kb_per_second': round(kb_per_s, 1) if kb_per_s else None,
        'sha256_line': sha_line[:80],  # sha256sum output shape
        'staged_file_on_jump': dest_local,  # kept for Approach C if this passes
        'fetch_stdout_tail': fetch_out[-400:],
        'fetch_stderr_tail': fetch_err[-200:] if fetch_err else '',
    }


def main():
    tmpdir = Path(tempfile.mkdtemp(prefix='d12_matrix_', dir='/tmp'))
    tmpdir.chmod(0o700)
    print(json.dumps({'tmpdir': str(tmpdir)}))
    try:
        creds = load_creds_silent()
        print(json.dumps({'creds_load': 'PASS'}))

        results = {}

        # Approach A
        v_a = approach_a_mount_cifs(creds, tmpdir)
        results['approach_a'] = v_a
        print(json.dumps({'approach_a_summary': {
            'verdict': v_a['verdict'],
            'bytes_transferred': v_a.get('bytes_transferred'),
            'kb_per_second': v_a.get('kb_per_second'),
            'dt_measured_on_jump_s': v_a.get('dt_measured_on_jump_s'),
        }}))

        # If A passed with full file: save the JUMP-side path for Approach C staging
        results['approach_a_full_details'] = v_a

    finally:
        try: del creds
        except NameError: pass
        for p in tmpdir.iterdir():
            try: p.unlink()
            except OSError: pass
        try: tmpdir.rmdir()
        except OSError: pass

    # Bank the throughput matrix
    matrix_dir = Path('/app/assessment_workspace/phase0/d12_poc_receipts')
    matrix_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    matrix_path = matrix_dir / f'{ts}_d12_01_throughput_matrix.json'
    matrix_path.write_text(json.dumps({
        'kind': 'd12_01_throughput_matrix',
        'sealed_at_utc': ts,
        'approaches_tested_this_run': ['a'],
        'results': results,
    }, indent=2))
    os.chmod(matrix_path, 0o644)
    print(json.dumps({'matrix_receipt_banked': str(matrix_path)}))


if __name__ == '__main__':
    main()
