"""D12 POC live-run · Stages 5-8 (fetch → scp → install → transcribe → receipt).

Single-file pipeline for BOUNDED POC scope (single-digit=1 file per owner
directive · file cap 100 MB per grounding-brief §E.4 refinement).

Position-redaction hard-lock: credentials live in-process only, never
in argv / env-leak / print. All operational stdout is structured JSON.
"""
from __future__ import annotations

import hashlib, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, '/app/assessment_workspace/repos/Extraction-Akki/backend')
sys.path.insert(0, '/app/assessment_workspace/tools')
from services.secret_hygiene.custody_file import assert_no_transcript_cat_on_custody
from d12_poc_live_probe import load_creds_silent

TARGET_DATE_DIR = '2026_09_14'  # yesterday · fully populated per stage-4b probe
TARGET_FILENAME = 'channel01_2026_09_14_00_00_00.mp4'  # first slot · lex-smallest
FILE_CAP_BYTES = 100 * 1024 * 1024  # E.4 refined: 100 MB per file

# GPU host from env
def load_gpu_env():
    env = {}
    for ln in open('/app/backend/.env').read().splitlines():
        if not ln or ln.startswith('#') or '=' not in ln: continue
        k, v = ln.split('=', 1)
        env[k.strip()] = v.strip()
    return env


def stage_5_fetch_nas_to_pod(creds: dict, tmpdir: Path) -> dict:
    """Pod-side: sshpass -> jump -> smbclient 'get <path>' into pod tmp."""
    stage = 'stage_5_fetch_nas_to_pod'
    pw_file = tmpdir / '.sshpass_jump'
    pw_file.write_text(creds['jump_pw'] + '\n')
    os.chmod(pw_file, 0o600)

    # Fetch to JUMP-local /tmp first (smbclient runs on JUMP), then scp back to pod.
    # Use a size cap check before smbclient get.
    jump_tmpfile = f'/tmp/d12_poc_nas_{int(time.time())}.mp4'
    remote_script = (
        'set -e; read -s NAS_PW; '
        'PASSWD="$NAS_PW" smbclient //10.10.55.55/OFFAIRRECS -U ' + creds['nas_user'] +
        ' -t 300 --socket-options="TCP_NODELAY IPTOS_LOWDELAY SO_KEEPALIVE"'
        ' --max-protocol=SMB2 -m SMB2'
        ' -c "cd Record/channel01/' + TARGET_DATE_DIR + '; get ' + TARGET_FILENAME + ' ' + jump_tmpfile + '"' +
        ' 2>&1 | tail -3; '
        'echo BYTES_ON_JUMP=$(stat -c %s ' + jump_tmpfile + ' 2>/dev/null || echo 0); '
        'unset NAS_PW PASSWD; echo REMOTE_OK'
    )
    assert_no_transcript_cat_on_custody(remote_script)
    argv = ['sshpass', '-f', str(pw_file), 'ssh', '-o', 'StrictHostKeyChecking=accept-new',
            '-o', 'ConnectTimeout=15', f"{creds['jump_user']}@{creds['jump_host']}", remote_script]
    t0 = time.time()
    r = subprocess.run(argv, input=(creds['nas_pw']+'\n').encode(),
                       capture_output=True, timeout=180)
    dt_fetch_on_jump = time.time() - t0

    if r.returncode != 0 or 'REMOTE_OK' not in r.stdout.decode('utf-8','replace'):
        pw_file.unlink()
        return {'stage': stage, 'verdict': 'FAIL',
                'sub_step': 'jump_side_smbclient_get',
                'dt_seconds': round(dt_fetch_on_jump,3), 'rc': r.returncode,
                'stderr_shape': {'lines': len(r.stderr.decode('utf-8','replace').splitlines())}}

    # scp JUMP:tmpfile -> pod:tmpdir/<filename>
    pod_local = tmpdir / TARGET_FILENAME
    argv_scp = ['sshpass', '-f', str(pw_file), 'scp',
                '-o', 'StrictHostKeyChecking=accept-new',
                '-o', 'ConnectTimeout=15',
                f"{creds['jump_user']}@{creds['jump_host']}:{jump_tmpfile}",
                str(pod_local)]
    t1 = time.time()
    r2 = subprocess.run(argv_scp, capture_output=True, timeout=300)
    dt_scp = time.time() - t1
    # Cleanup JUMP tmpfile
    argv_cleanup = ['sshpass', '-f', str(pw_file), 'ssh',
                    '-o', 'StrictHostKeyChecking=accept-new',
                    f"{creds['jump_user']}@{creds['jump_host']}",
                    f'shred -u {jump_tmpfile} 2>/dev/null || rm -f {jump_tmpfile}']
    subprocess.run(argv_cleanup, capture_output=True, timeout=30)
    pw_file.unlink()

    if r2.returncode != 0 or not pod_local.exists():
        return {'stage': stage, 'verdict': 'FAIL',
                'sub_step': 'scp_jump_to_pod',
                'dt_seconds': round(dt_scp,3), 'rc': r2.returncode}

    size = pod_local.stat().st_size
    if size > FILE_CAP_BYTES:
        pod_local.unlink()
        return {'stage': stage, 'verdict': 'REFUSED_BOUNDED_CAP',
                'dt_seconds': round(dt_fetch_on_jump+dt_scp,3),
                'file_bytes': size, 'cap_bytes': FILE_CAP_BYTES}

    sha = hashlib.sha256(pod_local.read_bytes()).hexdigest()
    return {'stage': stage, 'verdict': 'PASS',
            'dt_fetch_on_jump_s': round(dt_fetch_on_jump,3),
            'dt_scp_to_pod_s': round(dt_scp,3),
            'dt_total_s': round(dt_fetch_on_jump+dt_scp,3),
            'pod_path': str(pod_local),
            'file_bytes': size, 'sha256': sha}


def stage_6_scp_pod_to_gpu(pod_file: Path, gpu_env: dict, gpu_tmpdir: str) -> dict:
    stage = 'stage_6_scp_pod_to_gpu'
    dest = f"{gpu_tmpdir}/{pod_file.name}"
    argv = ['scp', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
            '-o', 'StrictHostKeyChecking=accept-new',
            '-P', gpu_env['AKKI_VM_PORT'],
            str(pod_file),
            f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}:{dest}"]
    t0 = time.time()
    r = subprocess.run(argv, capture_output=True, timeout=300)
    dt = time.time() - t0
    return {'stage': stage, 'verdict': 'PASS' if r.returncode == 0 else 'FAIL',
            'dt_seconds': round(dt,3), 'rc': r.returncode,
            'dest_path': dest,
            'stderr_shape': {'lines': len(r.stderr.decode('utf-8','replace').splitlines())}}


def stage_7_install_and_transcribe_on_gpu(gpu_env: dict, gpu_file_path: str,
                                          input_sha256: str, input_bytes: int) -> dict:
    """SSH into akki-vm · pip install faster-whisper (--user) if missing ·
    transcribe · emit only receipt-shape JSON (NEVER transcript body).
    """
    stage = 'stage_7_install_and_transcribe_on_gpu'
    # Remote python script - reads whisper-tiny, transcribes, outputs receipt JSON.
    remote_python = f'''
import json, time, os, sys
try:
    from faster_whisper import WhisperModel
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages",
                    "--user", "--quiet", "faster-whisper"], check=True)
    from faster_whisper import WhisperModel
t0 = time.time()
try:
    model = WhisperModel("tiny", device="cuda", compute_type="int8")
except Exception as e:
    # Fallback to cpu int8 if cuda backend fails
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
t_load = time.time() - t0
t1 = time.time()
segments_iter, info = model.transcribe(r"{gpu_file_path}", beam_size=1)
segments = list(segments_iter)
t_infer = time.time() - t1
# Aggregate WITHOUT emitting text body
seg_count = len(segments)
word_count_approx = 0
avg_conf = 0.0
for s in segments:
    # length-only count of whitespace-delimited tokens
    if s.text:
        word_count_approx += len(s.text.split())
    if hasattr(s, "avg_logprob") and s.avg_logprob is not None:
        avg_conf += s.avg_logprob
if seg_count > 0:
    avg_conf /= seg_count
receipt = {{
    "gpu_side_receipt_kind": "d12_poc_transcription_run",
    "poc_flag": "POC-NOT-PRODUCTION",
    "input_bytes": {input_bytes},
    "input_sha256": "{input_sha256}",
    "wall_clock_load_s": round(t_load, 3),
    "wall_clock_transcribe_s": round(t_infer, 3),
    "segment_count": seg_count,
    "word_count_approx": word_count_approx,
    "language_hint": info.language if hasattr(info, "language") else None,
    "language_probability": round(info.language_probability, 4) if hasattr(info, "language_probability") else None,
    "duration_s": round(info.duration, 2) if hasattr(info, "duration") else None,
    "avg_confidence": round(avg_conf, 4) if seg_count else None,
    "gpu_host": os.uname().nodename,
}}
print(json.dumps(receipt))
'''

    # Write remote python to a heredoc-safe form
    argv = ['ssh', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
            '-o', 'StrictHostKeyChecking=accept-new',
            '-p', gpu_env['AKKI_VM_PORT'],
            '-o', 'ServerAliveInterval=30',
            f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}",
            'python3 -']
    t0 = time.time()
    r = subprocess.run(argv, input=remote_python.encode(),
                       capture_output=True, timeout=900)
    dt = time.time() - t0
    out = r.stdout.decode('utf-8','replace').strip()
    err = r.stderr.decode('utf-8','replace').strip()
    if r.returncode != 0:
        return {'stage': stage, 'verdict': 'FAIL',
                'dt_seconds': round(dt,3), 'rc': r.returncode,
                'stderr_shape': {'lines': len(err.splitlines()),
                                 'tail_100chars': err[-500:] if err else ''}}
    try:
        # Only the last valid-JSON line is the receipt
        for ln in reversed(out.splitlines()):
            if ln.strip().startswith('{'):
                receipt = json.loads(ln)
                break
        else:
            raise ValueError('no JSON receipt line')
    except Exception as e:
        return {'stage': stage, 'verdict': 'FAIL',
                'sub_step': 'json_parse',
                'dt_seconds': round(dt,3), 'rc': r.returncode,
                'stdout_tail_500chars': out[-500:]}
    return {'stage': stage, 'verdict': 'PASS',
            'dt_end_to_end_s': round(dt,3),
            'receipt': receipt}


def main():
    tmpdir = Path(tempfile.mkdtemp(prefix='d12_poc_full_', dir='/tmp'))
    tmpdir.chmod(0o700)
    print(json.dumps({'tmpdir': str(tmpdir)}))
    try:
        creds = load_creds_silent()
        gpu_env = load_gpu_env()

        # Stage 5 · fetch NAS bytes to pod
        v5 = stage_5_fetch_nas_to_pod(creds, tmpdir)
        print(json.dumps(v5))
        if v5['verdict'] != 'PASS':
            print(json.dumps({'halt': 'stage_5_fail'}))
            return
        pod_file = Path(v5['pod_path'])

        # Stage 6 · scp pod -> gpu
        gpu_tmpdir = f'/tmp/d12_poc_{int(time.time())}'
        subprocess.run(['ssh', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
                        '-p', gpu_env['AKKI_VM_PORT'],
                        '-o', 'StrictHostKeyChecking=accept-new',
                        f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}",
                        f'mkdir -p {gpu_tmpdir} && chmod 700 {gpu_tmpdir}'],
                       capture_output=True, timeout=30)
        v6 = stage_6_scp_pod_to_gpu(pod_file, gpu_env, gpu_tmpdir)
        print(json.dumps(v6))
        if v6['verdict'] != 'PASS':
            print(json.dumps({'halt': 'stage_6_fail'}))
            return

        # Stage 7 · install faster-whisper + transcribe on GPU
        gpu_file_path = f"{gpu_tmpdir}/{pod_file.name}"
        v7 = stage_7_install_and_transcribe_on_gpu(
            gpu_env, gpu_file_path,
            input_sha256=v5['sha256'], input_bytes=v5['file_bytes'],
        )
        print(json.dumps(v7))

        # Stage 8 · bank pod-side receipt
        receipt_dir = Path('/app/assessment_workspace/phase0/d12_poc_receipts')
        receipt_dir.mkdir(parents=True, exist_ok=True)
        ts = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
        key_short = pod_file.stem[:32]
        out_path = receipt_dir / f'{ts}_{key_short}.json'
        combined = {
            'wave': 'W-D12-POC',
            'sub_wave': 'CP-D12P1_LIVE_RUN',
            'sealed_at_utc': ts,
            'kind': 'd12_poc_receipt',
            'poc_flag': 'POC-NOT-PRODUCTION',
            'input_canonical_key': {
                'station': 'channel01',
                'date_utc': TARGET_DATE_DIR.replace('_', ''),
                'slot': '0000',
                'filename_stem': pod_file.stem,
            },
            'input_sha256': v5['sha256'],
            'input_bytes': v5['file_bytes'],
            'model_id': 'faster-whisper:tiny',
            'model_version': 'ctranslate2',
            'compute_type': 'int8',
            'beam_size': 1,
            'live_run_stages': {'stage_5': v5, 'stage_6': v6, 'stage_7': v7},
            'provenance_note': ('raw transcript body NEVER emitted · '
                                'release-gate admission deferred per owner '
                                'Option-A 2026-09-15T~09:50Z'),
        }
        out_path.write_text(json.dumps(combined, indent=2))
        os.chmod(out_path, 0o644)
        print(json.dumps({'stage_8': {'verdict': 'PASS',
                                       'receipt_path': str(out_path),
                                       'receipt_bytes': out_path.stat().st_size}}))

        # Cleanup GPU-side tmpdir
        subprocess.run(['ssh', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
                        '-p', gpu_env['AKKI_VM_PORT'],
                        '-o', 'StrictHostKeyChecking=accept-new',
                        f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}",
                        f'shred -u {gpu_file_path} 2>/dev/null && rmdir {gpu_tmpdir} 2>/dev/null || rm -rf {gpu_tmpdir}'],
                       capture_output=True, timeout=30)

    finally:
        try: del creds
        except NameError: pass
        # Pod-side cleanup
        for p in tmpdir.iterdir():
            try: p.unlink()
            except OSError: pass
        try: tmpdir.rmdir()
        except OSError: pass


if __name__ == '__main__':
    main()
