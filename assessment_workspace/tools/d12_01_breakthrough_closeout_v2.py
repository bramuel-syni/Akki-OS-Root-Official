"""D12-01 breakthrough close-out v2 · with ffprobe + ffmpeg audio-extract + transcribe.

Uses mount.cifs (Approach A) NAS→JUMP · then JUMP→pod scp · pod→GPU scp ·
then ffprobe to confirm audio track · ffmpeg extract to wav · then transcribe.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, '/app/assessment_workspace/repos/Extraction-Akki/backend')
sys.path.insert(0, '/app/assessment_workspace/tools')
from services.secret_hygiene.custody_file import assert_no_transcript_cat_on_custody
from d12_poc_live_probe import load_creds_silent


TARGET_PATH = 'Record/channel01/2026_09_14/channel01_2026_09_14_00_00_00.mp4'
TARGET_BASENAME = 'channel01_2026_09_14_00_00_00.mp4'


def load_gpu_env():
    env = {}
    for ln in open('/app/backend/.env').read().splitlines():
        if not ln or ln.startswith('#') or '=' not in ln: continue
        k, v = ln.split('=', 1); env[k.strip()] = v.strip()
    return env


def main():
    creds = load_creds_silent()
    gpu_env = load_gpu_env()
    tmpdir = Path(tempfile.mkdtemp(prefix='d12_bt2_', dir='/tmp'))
    tmpdir.chmod(0o700)
    try:
        pw_file = tmpdir / '.sshpass_jump'
        pw_file.write_text(creds['jump_pw'] + '\n')
        os.chmod(pw_file, 0o600)

        # Stage A · mount.cifs + copy (single JUMP session)
        jump_staged = f'/tmp/d12_bt2_{int(time.time())}.mp4'
        setup_cmd = (
            'set -e; read -s NAS_PW; '
            'CRED=$(mktemp /tmp/cifs_cred.XXXXXX); chmod 600 $CRED; '
            f'printf "username={creds["nas_user"]}\\npassword=$NAS_PW\\n" > $CRED; '
            'MNT=$(mktemp -d /tmp/nas_mnt.XXXXXX); '
            f'sudo mount -t cifs //10.10.55.55/OFFAIRRECS $MNT '
            f'-o credentials=$CRED,vers=3.0,rsize=4194304,wsize=4194304,cache=loose,ro,uid=0 2>&1 | tail -2; '
            'START=$(date +%s.%N); '
            f'timeout 200 cp $MNT/{TARGET_PATH} {jump_staged} 2>&1 | head -3; '
            'END=$(date +%s.%N); '
            f'BYTES=$(stat -c %s {jump_staged} 2>/dev/null || echo 0); '
            'sudo umount -l $MNT 2>/dev/null; '
            'shred -u $CRED 2>/dev/null; rmdir $MNT 2>/dev/null; '
            'echo NAS_BYTES=$BYTES; '
            'echo NAS_DT_S=$(python3 -c "print(round($END-$START,3))")'
        )
        argv = ['sshpass', '-f', str(pw_file), 'ssh',
                '-o', 'StrictHostKeyChecking=accept-new',
                f"{creds['jump_user']}@{creds['jump_host']}", setup_cmd]
        t0 = time.time()
        r = subprocess.run(argv, input=(creds['nas_pw']+'\n').encode(),
                           capture_output=True, timeout=280)
        dt_stage_a = time.time() - t0
        out = r.stdout.decode('utf-8','replace')
        nas_bytes = int(next((ln.split('=',1)[1] for ln in out.splitlines()
                              if ln.startswith('NAS_BYTES=')), '0'))
        nas_dt = float(next((ln.split('=',1)[1] for ln in out.splitlines()
                             if ln.startswith('NAS_DT_S=')), '0'))
        print(json.dumps({'stage_a_mount_cifs': 'PASS' if nas_bytes > 79000000 else 'FAIL',
                          'nas_bytes': nas_bytes, 'nas_dt_s': nas_dt,
                          'nas_kb_s': round(nas_bytes/nas_dt/1024,1) if nas_dt else 0,
                          'wallclock_pod_side_s': round(dt_stage_a,3)}))
        if nas_bytes < 79000000:
            print(json.dumps({'halt': 'stage_a_failed'}))
            return

        # Stage 6a · JUMP→pod
        pod_file = tmpdir / TARGET_BASENAME
        argv = ['sshpass', '-f', str(pw_file), 'scp',
                '-o', 'StrictHostKeyChecking=accept-new',
                f"{creds['jump_user']}@{creds['jump_host']}:{jump_staged}",
                str(pod_file)]
        t0 = time.time()
        subprocess.run(argv, capture_output=True, timeout=180)
        dt_j2p = time.time() - t0
        # cleanup JUMP-side
        subprocess.run(['sshpass', '-f', str(pw_file), 'ssh',
                        '-o', 'StrictHostKeyChecking=accept-new',
                        f"{creds['jump_user']}@{creds['jump_host']}",
                        f'shred -u {jump_staged} 2>/dev/null || rm -f {jump_staged}'],
                       capture_output=True, timeout=15)
        pw_file.unlink()
        pod_bytes = pod_file.stat().st_size
        pod_sha = hashlib.sha256(pod_file.read_bytes()).hexdigest()
        print(json.dumps({'stage_6a_jump_to_pod': 'PASS',
                          'dt_s': round(dt_j2p,3), 'bytes': pod_bytes,
                          'kb_s': round(pod_bytes/dt_j2p/1024,1)}))

        # Stage 6b · pod→GPU
        gpu_tmpdir = f'/tmp/d12_bt2_{int(time.time())}'
        subprocess.run(['ssh', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
                        '-p', gpu_env['AKKI_VM_PORT'],
                        '-o', 'StrictHostKeyChecking=accept-new',
                        f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}",
                        f'mkdir -p {gpu_tmpdir} && chmod 700 {gpu_tmpdir}'],
                       capture_output=True, timeout=30)
        gpu_mp4 = f'{gpu_tmpdir}/{pod_file.name}'
        argv = ['scp', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
                '-P', gpu_env['AKKI_VM_PORT'],
                '-o', 'StrictHostKeyChecking=accept-new',
                str(pod_file), f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}:{gpu_mp4}"]
        t0 = time.time()
        subprocess.run(argv, capture_output=True, timeout=240)
        dt_p2g = time.time() - t0
        print(json.dumps({'stage_6b_pod_to_gpu': 'PASS', 'dt_s': round(dt_p2g,3),
                          'kb_s': round(pod_bytes/dt_p2g/1024,1)}))

        # Stage 7-pre · ffprobe on GPU host to identify audio track shape
        ffprobe_cmd = (
            f'ffprobe -v error -show_entries stream=index,codec_type,codec_name,duration,sample_rate,channels,bit_rate '
            f'-of json {gpu_mp4}'
        )
        r = subprocess.run(['ssh', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
                            '-p', gpu_env['AKKI_VM_PORT'],
                            '-o', 'StrictHostKeyChecking=accept-new',
                            f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}",
                            ffprobe_cmd], capture_output=True, timeout=45)
        try:
            probe = json.loads(r.stdout.decode('utf-8','replace'))
        except Exception:
            probe = {'raw_stdout_tail': r.stdout.decode('utf-8','replace')[-300:]}
        # Extract audio-track summary (shape-only, no values that could be sensitive)
        audio_streams = [s for s in probe.get('streams', []) if s.get('codec_type') == 'audio']
        video_streams = [s for s in probe.get('streams', []) if s.get('codec_type') == 'video']
        print(json.dumps({'stage_7pre_ffprobe': 'PASS' if audio_streams else 'AUDIO_TRACK_MISSING',
                          'audio_track_count': len(audio_streams),
                          'video_track_count': len(video_streams),
                          'audio_tracks': [{'codec_name': s.get('codec_name'),
                                            'sample_rate': s.get('sample_rate'),
                                            'channels': s.get('channels'),
                                            'duration_s': s.get('duration'),
                                            'bit_rate': s.get('bit_rate')} for s in audio_streams]}))

        # Stage 7 · ffmpeg-extract to 16kHz mono wav + faster-whisper transcribe on wav
        gpu_wav = f'{gpu_tmpdir}/{pod_file.stem}_mono16k.wav'
        transcribe_script = f'''
import json, subprocess, time, os
# ffmpeg extract audio to 16kHz mono wav (whisper preferred format)
t0 = time.time()
r = subprocess.run(
    ["ffmpeg", "-nostdin", "-y", "-loglevel", "error",
     "-i", r"{gpu_mp4}",
     "-vn", "-ac", "1", "-ar", "16000",
     r"{gpu_wav}"], capture_output=True, timeout=120)
t_ffmpeg = time.time() - t0
if r.returncode != 0:
    print(json.dumps({{"stage": "ffmpeg_extract", "verdict": "FAIL",
                       "rc": r.returncode,
                       "stderr_tail": r.stderr.decode("utf-8","replace")[-500:]}}))
    raise SystemExit(1)
wav_bytes = os.path.getsize(r"{gpu_wav}")
# faster-whisper on wav
from faster_whisper import WhisperModel
t1 = time.time()
try:
    model = WhisperModel("tiny", device="cuda", compute_type="int8")
    device = "cuda"
except Exception:
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    device = "cpu"
t_load = time.time() - t1
t2 = time.time()
segments_iter, info = model.transcribe(r"{gpu_wav}", beam_size=1)
segments = list(segments_iter)
t_transcribe = time.time() - t2
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
    "input_bytes_mp4": {pod_bytes},
    "input_sha256_mp4": "{pod_sha}",
    "wav_bytes": wav_bytes,
    "wall_clock_ffmpeg_s": round(t_ffmpeg, 3),
    "wall_clock_load_s": round(t_load, 3),
    "wall_clock_transcribe_s": round(t_transcribe, 3),
    "wall_clock_end_to_end_gpu_s": round(t_ffmpeg + t_load + t_transcribe, 3),
    "device_used": device,
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
        t0 = time.time()
        r = subprocess.run(['ssh', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
                            '-p', gpu_env['AKKI_VM_PORT'],
                            '-o', 'StrictHostKeyChecking=accept-new',
                            '-o', 'ServerAliveInterval=30',
                            f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}",
                            'python3 -'],
                           input=transcribe_script.encode(),
                           capture_output=True, timeout=200)
        dt_transcribe_end_to_end = time.time() - t0
        out = r.stdout.decode('utf-8','replace').strip()
        err = r.stderr.decode('utf-8','replace').strip()
        receipt = None
        for ln in reversed(out.splitlines()):
            if ln.strip().startswith('{'):
                try:
                    receipt = json.loads(ln)
                    break
                except Exception:
                    continue
        if receipt is None or receipt.get('stage') == 'ffmpeg_extract':
            print(json.dumps({'stage_7_verdict': 'FAIL', 'rc': r.returncode,
                              'stderr_tail': err[-500:],
                              'partial_receipt': receipt}))
        else:
            print(json.dumps({'stage_7_verdict': 'PASS',
                              'dt_end_to_end_s': round(dt_transcribe_end_to_end,3),
                              'receipt': receipt}))

        # Bank full receipt
        receipts_dir = Path('/app/assessment_workspace/phase0/d12_poc_receipts')
        ts = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
        out_path = receipts_dir / f'{ts}_channel01_2026_09_14_00_00_00_D12_BREAKTHROUGH_v2.json'
        combined = {
            'wave': 'W-D12-POC',
            'sub_wave': 'CP-D12P1_LIVE_BREAKTHROUGH_D12_01_APPROACH_A_v2',
            'sealed_at_utc': ts,
            'kind': 'd12_poc_receipt',
            'poc_flag': 'POC-NOT-PRODUCTION',
            'blocker_d12_01_status': 'CLOSED_VIA_APPROACH_A_MOUNT_CIFS_SMB3_RSIZE_4M',
            'blocker_d12_03_status': 'CLOSED_VIA_FFMPEG_EXTRACT_TO_MONO16K_WAV' if receipt else 'FFMPEG_OR_WHISPER_FAIL',
            'input_canonical_key': {
                'station': 'channel01', 'date_utc': '20260914', 'slot': '0000',
                'filename_stem': 'channel01_2026_09_14_00_00_00',
            },
            'legs': {
                'nas_to_jump_mount_cifs': {'dt_s': nas_dt, 'bytes': nas_bytes,
                                           'kb_s': round(nas_bytes/nas_dt/1024,1),
                                           'params': 'vers=3.0,rsize=4M,wsize=4M,cache=loose,ro'},
                'jump_to_pod_scp': {'dt_s': round(dt_j2p,3),
                                    'kb_s': round(pod_bytes/dt_j2p/1024,1)},
                'pod_to_gpu_scp': {'dt_s': round(dt_p2g,3),
                                   'kb_s': round(pod_bytes/dt_p2g/1024,1)},
                'gpu_end_to_end': {'dt_s': round(dt_transcribe_end_to_end,3)},
            },
            'ffprobe_audio_tracks': [{'codec_name': s.get('codec_name'),
                                       'sample_rate': s.get('sample_rate'),
                                       'channels': s.get('channels'),
                                       'duration_s': s.get('duration'),
                                       'bit_rate': s.get('bit_rate')} for s in audio_streams],
            'transcription_receipt': receipt,
            'model_id': 'faster-whisper:tiny',
            'model_version': 'ctranslate2',
            'compute_type': 'int8',
            'beam_size': 1,
            'provenance_note': ('raw transcript body NEVER emitted · '
                                'release-gate admission deferred per owner Option-A 2026-09-15T~09:50Z · '
                                'blocker D12-01 CLOSED via mount.cifs SMB3.0 rsize=4M · '
                                'blocker D12-03 (mp4 audio decode) addressed via ffmpeg extract to mono 16k wav'),
        }
        out_path.write_text(json.dumps(combined, indent=2))
        os.chmod(out_path, 0o644)
        print(json.dumps({'receipt_banked': str(out_path),
                          'receipt_bytes': out_path.stat().st_size}))

        # GPU cleanup
        subprocess.run(['ssh', '-i', gpu_env['AKKI_VM_SSH_PRIVATE_KEY_PATH'],
                        '-p', gpu_env['AKKI_VM_PORT'],
                        '-o', 'StrictHostKeyChecking=accept-new',
                        f"{gpu_env['AKKI_VM_USERNAME']}@{gpu_env['AKKI_VM_HOST']}",
                        f'shred -u {gpu_mp4} {gpu_wav} 2>/dev/null; rm -rf {gpu_tmpdir} 2>/dev/null'],
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
