"""D12-01 breakthrough close-out · JUMP-staged file → pod → akki-vm → transcribe."""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, '/app/assessment_workspace/repos/Extraction-Akki/backend')
sys.path.insert(0, '/app/assessment_workspace/tools')
from services.secret_hygiene.custody_file import assert_no_transcript_cat_on_custody
from d12_poc_live_probe import load_creds_silent


def load_gpu_env():
    env = {}
    for ln in open('/app/backend/.env').read().splitlines():
        if not ln or ln.startswith('#') or '=' not in ln: continue
        k, v = ln.split('=', 1); env[k.strip()] = v.strip()
    return env


def main():
    # Find the most-recent JUMP-staged file from Approach A
    matrix_dir = Path('/app/assessment_workspace/phase0/d12_poc_receipts')
    matrices = sorted(matrix_dir.glob('*_d12_01_throughput_matrix.json'))
    if not matrices:
        print(json.dumps({'error': 'no throughput matrix found'}))
        return
    d = json.loads(matrices[-1].read_text())
    a = d['results'].get('approach_a_full_details', {})
    if a.get('verdict') != 'PASS':
        print(json.dumps({'error': 'approach_a did not pass', 'verdict': a.get('verdict')}))
        return

    jump_staged_path = a['staged_file_on_jump']
    bytes_expected = a['bytes_transferred']

    creds = load_creds_silent()
    gpu_env = load_gpu_env()

    tmpdir = Path(tempfile.mkdtemp(prefix='d12_bt_', dir='/tmp'))
    tmpdir.chmod(0o700)

    try:
        pw_file = tmpdir / '.sshpass_jump'
        pw_file.write_text(creds['jump_pw'] + '\n')
        os.chmod(pw_file, 0o600)

        # Verify JUMP-staged file still exists
        check_cmd = f'stat -c %s {jump_staged_path} 2>/dev/null || echo MISSING'
        r = subprocess.run(['sshpass', '-f', str(pw_file), 'ssh',
                            '-o', 'StrictHostKeyChecking=accept-new',
                            f"{creds['jump_user']}@{creds['jump_host']}",
                            check_cmd], capture_output=True, timeout=20)
        check_out = r.stdout.decode('utf-8','replace').strip()
        if 'MISSING' in check_out:
            print(json.dumps({'error': 'JUMP-staged file missing', 'path': jump_staged_path}))
            return
        print(json.dumps({'stage_a_reuse': 'PASS', 'jump_bytes': check_out}))

        # Stage 6a · scp JUMP -> pod
        pod_file = tmpdir / 'channel01_2026_09_14_00_00_00.mp4'
        argv = ['sshpass', '-f', str(pw_file), 'scp',
                '-o', 'StrictHostKeyChecking=accept-new',
                f"{creds['jump_user']}@{creds['jump_host']}:{jump_staged_path}",
                str(pod_file)]
        t0 = time.time()
        r = subprocess.run(argv, capture_output=True, timeout=180)
        dt_jump_to_pod = time.time() - t0
        if r.returncode != 0 or not pod_file.exists():
            print(json.dumps({'error': 'scp jump->pod failed', 'rc': r.returncode}))
            return
        pod_bytes = pod_file.stat().st_size
        pod_sha = hashlib.sha256(pod_file.read_bytes()).hexdigest()
        print(json.dumps({'stage_6a_jump_to_pod': 'PASS',
                          'dt_s': round(dt_jump_to_pod,3),
                          'bytes': pod_bytes, 'sha256': pod_sha,
                          'kb_per_s': round(pod_bytes / dt_jump_to_pod / 1024, 1)}))

        # Cleanup JUMP-staged file
        cleanup_cmd = f'shred -u {jump_staged_path} 2>/dev/null || rm -f {jump_staged_path}'
        subprocess.run(['sshpass', '-f', str(pw_file), 'ssh',
                        '-o', 'StrictHostKeyChecking=accept-new',
                        f"{creds['jump_user']}@{creds['jump_host']}",
                        cleanup_cmd], capture_output=True, timeout=15)
        pw_file.unlink()

        # Stage 6b · scp pod -> akki-vm
        gpu_tmpdir = f'/tmp/d12_bt_{int(time.time())}'
        subprocess.run(['ssh', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
                        '-p', gpu_env['AKKI_VM_PORT'],
                        '-o', 'StrictHostKeyChecking=accept-new',
                        f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}",
                        f'mkdir -p {gpu_tmpdir} && chmod 700 {gpu_tmpdir}'],
                       capture_output=True, timeout=30)
        gpu_dest = f'{gpu_tmpdir}/{pod_file.name}'
        argv = ['scp', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
                '-o', 'StrictHostKeyChecking=accept-new',
                '-P', gpu_env['AKKI_VM_PORT'],
                str(pod_file), f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}:{gpu_dest}"]
        t0 = time.time()
        r = subprocess.run(argv, capture_output=True, timeout=180)
        dt_pod_to_gpu = time.time() - t0
        if r.returncode != 0:
            print(json.dumps({'error': 'scp pod->gpu failed', 'rc': r.returncode}))
            return
        print(json.dumps({'stage_6b_pod_to_gpu': 'PASS',
                          'dt_s': round(dt_pod_to_gpu,3),
                          'kb_per_s': round(pod_bytes / dt_pod_to_gpu / 1024, 1)}))

        # Stage 7 · faster-whisper transcribe on akki-vm (never emit transcript text)
        remote_python = f'''
import json, time, os
from faster_whisper import WhisperModel
t0 = time.time()
try:
    model = WhisperModel("tiny", device="cuda", compute_type="int8")
    device_used = "cuda"
except Exception:
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    device_used = "cpu"
t_load = time.time() - t0
t1 = time.time()
segments_iter, info = model.transcribe(r"{gpu_dest}", beam_size=1)
segments = list(segments_iter)
t_infer = time.time() - t1
seg_count = len(segments)
word_count_approx = 0
avg_lp = 0.0
for s in segments:
    if s.text: word_count_approx += len(s.text.split())
    if hasattr(s, "avg_logprob") and s.avg_logprob is not None:
        avg_lp += s.avg_logprob
if seg_count:
    avg_lp /= seg_count
receipt = {{
    "poc_flag": "POC-NOT-PRODUCTION",
    "input_bytes": {pod_bytes},
    "input_sha256": "{pod_sha}",
    "wall_clock_load_s": round(t_load, 3),
    "wall_clock_transcribe_s": round(t_infer, 3),
    "device_used": device_used,
    "segment_count": seg_count,
    "word_count_approx": word_count_approx,
    "language_hint": info.language if hasattr(info, "language") else None,
    "language_probability": round(info.language_probability, 4) if hasattr(info, "language_probability") else None,
    "audio_duration_s": round(info.duration, 2) if hasattr(info, "duration") else None,
    "avg_logprob": round(avg_lp, 4) if seg_count else None,
    "gpu_host": os.uname().nodename,
}}
print(json.dumps(receipt))
'''
        argv = ['ssh', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
                '-p', gpu_env['AKKI_VM_PORT'],
                '-o', 'StrictHostKeyChecking=accept-new',
                '-o', 'ServerAliveInterval=30',
                f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}",
                'python3 -']
        t0 = time.time()
        r = subprocess.run(argv, input=remote_python.encode(),
                           capture_output=True, timeout=280)
        dt_transcribe_end_to_end = time.time() - t0
        out = r.stdout.decode('utf-8','replace').strip()
        err = r.stderr.decode('utf-8','replace').strip()
        if r.returncode != 0:
            print(json.dumps({'error': 'transcribe failed', 'rc': r.returncode,
                              'stderr_tail': err[-500:]}))
            return
        # Parse the last JSON line
        receipt = None
        for ln in reversed(out.splitlines()):
            if ln.strip().startswith('{'):
                receipt = json.loads(ln)
                break
        if not receipt:
            print(json.dumps({'error': 'no receipt json', 'stdout_tail': out[-500:]}))
            return

        # Bank full pipeline receipt
        receipts_dir = Path('/app/assessment_workspace/phase0/d12_poc_receipts')
        ts = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
        out_path = receipts_dir / f'{ts}_channel01_2026_09_14_00_00_00_D12_BREAKTHROUGH.json'
        combined = {
            'wave': 'W-D12-POC',
            'sub_wave': 'CP-D12P1_LIVE_BREAKTHROUGH_D12_01_APPROACH_A',
            'sealed_at_utc': ts,
            'kind': 'd12_poc_receipt',
            'poc_flag': 'POC-NOT-PRODUCTION',
            'blocker_d12_01_status': 'CLOSED_VIA_APPROACH_A_MOUNT_CIFS_SMB3_RSIZE_4M',
            'input_canonical_key': {
                'station': 'channel01', 'date_utc': '20260914', 'slot': '0000',
                'filename_stem': 'channel01_2026_09_14_00_00_00',
            },
            'input_sha256': pod_sha,
            'input_bytes': pod_bytes,
            'model_id': 'faster-whisper:tiny',
            'model_version': 'ctranslate2',
            'compute_type': 'int8',
            'beam_size': 1,
            'legs': {
                'nas_to_jump_via_mount_cifs': {
                    'dt_s': a['dt_measured_on_jump_s'],
                    'kb_per_s': a['kb_per_second'],
                    'bytes': a['bytes_transferred'],
                    'params': 'vers=3.0,rsize=4M,wsize=4M,cache=loose,ro',
                },
                'jump_to_pod_scp': {'dt_s': round(dt_jump_to_pod,3),
                                    'kb_per_s': round(pod_bytes/dt_jump_to_pod/1024,1)},
                'pod_to_gpu_scp': {'dt_s': round(dt_pod_to_gpu,3),
                                   'kb_per_s': round(pod_bytes/dt_pod_to_gpu/1024,1)},
                'gpu_transcribe_end_to_end': {'dt_s': round(dt_transcribe_end_to_end,3)},
            },
            'transcription_receipt': receipt,
            'provenance_note': ('raw transcript body NEVER emitted · '
                                'release-gate admission deferred per owner Option-A 2026-09-15T~09:50Z · '
                                'blocker D12-01 CLOSED this run via mount.cifs SMB3.0 rsize=4M'),
        }
        out_path.write_text(json.dumps(combined, indent=2))
        os.chmod(out_path, 0o644)
        print(json.dumps({'stage_8_receipt_banked': str(out_path),
                          'receipt_bytes': out_path.stat().st_size,
                          'end_to_end_dt_s': round(dt_transcribe_end_to_end,3),
                          'receipt_summary': {k: receipt[k] for k in [
                              'wall_clock_transcribe_s', 'device_used',
                              'segment_count', 'word_count_approx', 'language_hint',
                              'language_probability', 'audio_duration_s', 'avg_logprob',
                          ]}}))

        # GPU cleanup
        subprocess.run(['ssh', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
                        '-p', gpu_env['AKKI_VM_PORT'],
                        '-o', 'StrictHostKeyChecking=accept-new',
                        f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}",
                        f'shred -u {gpu_dest} 2>/dev/null && rmdir {gpu_tmpdir} 2>/dev/null || rm -rf {gpu_tmpdir}'],
                       capture_output=True, timeout=30)

    finally:
        try: del creds
        except NameError: pass
        for p in tmpdir.iterdir():
            try: p.unlink()
            except OSError: pass
        try: tmpdir.rmdir()
        except OSError: pass


if __name__ == '__main__':
    main()
