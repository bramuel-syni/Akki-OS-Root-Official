"""D12-03 diagnosis v2 · python-on-JUMP for clean JSON emission.

Fixes v1's bash-quoting-strip issue. Emits one clean JSON line per channel.
"""
from __future__ import annotations

import json, os, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, '/app/assessment_workspace/repos/Extraction-Akki/backend')
sys.path.insert(0, '/app/assessment_workspace/tools')
from services.secret_hygiene.custody_file import (
    assert_no_transcript_cat_on_custody,
    assert_no_transcript_openpyxl_iter_rows_on_custody,
    assert_no_transcript_set_x_with_password_var,
)
from d12_poc_live_probe import load_creds_silent


def main():
    creds = load_creds_silent()
    tmpdir = Path(tempfile.mkdtemp(prefix='d12_03v2_', dir='/tmp'))
    tmpdir.chmod(0o700)
    pw_file = tmpdir / '.sshpass_jump'
    pw_file.write_text(creds['jump_pw'] + '\n')
    os.chmod(pw_file, 0o600)

    # Remote python runs on JUMP: mount NAS, enumerate all channels + all
    # date dirs to pick lex-first available file per channel, ffprobe each.
    remote_python = '''
import json, os, subprocess, sys, tempfile

nas_pw = sys.stdin.readline().rstrip("\\n")

# Write cifs cred file
import tempfile as _tf
cred_fd, cred_path = _tf.mkstemp(prefix="cifs_cred_", suffix=".txt", dir="/tmp")
os.write(cred_fd, ("username=''' + creds['nas_user'] + '''" + "\\n" + "password=" + nas_pw + "\\n").encode())
os.close(cred_fd)
os.chmod(cred_path, 0o600)

# Mount
mnt = _tf.mkdtemp(prefix="nas_mnt_", dir="/tmp")
r = subprocess.run(["sudo", "mount", "-t", "cifs", "//10.10.55.55/OFFAIRRECS", mnt,
                    "-o", f"credentials={cred_path},vers=3.0,rsize=4194304,wsize=4194304,cache=loose,ro,uid=0"],
                   capture_output=True, timeout=30)
if r.returncode != 0:
    print(json.dumps({"mount_fail": r.stderr.decode()[-400:]}))
    subprocess.run(["shred", "-u", cred_path], capture_output=True)
    os.rmdir(mnt)
    sys.exit(2)

per_channel = []
try:
    record_dir = os.path.join(mnt, "Record")
    channels = sorted([c for c in os.listdir(record_dir) if c.startswith("channel")])
    for ch in channels:
        ch_dir = os.path.join(record_dir, ch)
        date_dirs = sorted([d for d in os.listdir(ch_dir) if d.startswith("20") and "_" in d], reverse=True)
        picked_file = None
        picked_date = None
        for dd in date_dirs:
            full_dd = os.path.join(ch_dir, dd)
            try:
                files = sorted([f for f in os.listdir(full_dd)
                                if any(f.lower().endswith(ext) for ext in
                                       (".mp4",".mp3",".wav",".m4a",".aac",".flac",".ogg",".ts",".mkv",".mov"))])
            except Exception:
                continue
            if files:
                picked_file = files[0]
                picked_date = dd
                break
        if not picked_file:
            per_channel.append({"channel": ch, "verdict": "NO_MEDIA_FILE_ACROSS_ANY_DATE_DIR",
                                "date_dirs_available": len(date_dirs)})
            continue
        file_path = os.path.join(ch_dir, picked_date, picked_file)
        file_size = os.path.getsize(file_path)
        # ffprobe (JSON output · clean)
        pr = subprocess.run(["ffprobe", "-v", "error",
                             "-show_entries",
                             "stream=index,codec_type,codec_name,duration,sample_rate,channels,bit_rate,width,height,nb_frames:format=duration,bit_rate,format_name,size",
                             "-of", "json", file_path],
                            capture_output=True, timeout=15)
        try:
            probe = json.loads(pr.stdout.decode("utf-8","replace"))
        except Exception as e:
            probe = {"parse_error": str(e), "stdout_tail": pr.stdout.decode("utf-8","replace")[-200:]}
        per_channel.append({"channel": ch, "date_dir": picked_date,
                            "file_basename": picked_file, "file_size": file_size,
                            "probe": probe})
    # Extra: count total date dirs per channel + first date dir
    for c in per_channel:
        pass  # already populated
finally:
    subprocess.run(["sudo", "umount", "-l", mnt], capture_output=True, timeout=15)
    subprocess.run(["shred", "-u", cred_path], capture_output=True)
    try: os.rmdir(mnt)
    except: pass

print(json.dumps({"per_channel_count": len(per_channel)}))
print("BEGIN_MATRIX")
print(json.dumps(per_channel))
print("END_MATRIX")
'''

    assert_no_transcript_cat_on_custody(remote_python)
    assert_no_transcript_openpyxl_iter_rows_on_custody(remote_python)
    assert_no_transcript_set_x_with_password_var(remote_python)

    # Write script to a JUMP-side tempfile, then invoke with NAS pw via stdin.
    script_local = tmpdir / 'jump_diag.py'
    script_local.write_text(remote_python)
    jump_script_path = f'/tmp/d12_03v2_{int(time.time())}.py'
    r = subprocess.run(['sshpass', '-f', str(pw_file), 'scp',
                        '-o', 'StrictHostKeyChecking=accept-new',
                        str(script_local),
                        f"{creds['jump_user']}@{creds['jump_host']}:{jump_script_path}"],
                       capture_output=True, timeout=30)
    if r.returncode != 0:
        pw_file.unlink()
        print(json.dumps({'scp_script_fail': r.returncode,
                          'stderr': r.stderr.decode('utf-8','replace')[-200:]}))
        return

    argv = ['sshpass', '-f', str(pw_file), 'ssh',
            '-o', 'StrictHostKeyChecking=accept-new',
            '-o', 'ConnectTimeout=15', '-o', 'ServerAliveInterval=30',
            f"{creds['jump_user']}@{creds['jump_host']}",
            f'python3 {jump_script_path}; rm -f {jump_script_path}']
    # NAS pw via stdin (python's sys.stdin.readline() reads it)
    t0 = time.time()
    r = subprocess.run(argv, input=(creds['nas_pw']+'\n').encode(),
                       capture_output=True, timeout=270)
    dt = time.time() - t0
    pw_file.unlink()

    out = r.stdout.decode('utf-8','replace')
    err = r.stderr.decode('utf-8','replace')
    print(json.dumps({'jump_scan_rc': r.returncode, 'dt_s': round(dt,3),
                      'stderr_lines': len(err.splitlines())}))

    # Extract matrix between BEGIN_MATRIX and END_MATRIX
    matrix = None
    if 'BEGIN_MATRIX' in out and 'END_MATRIX' in out:
        matrix_json = out.split('BEGIN_MATRIX')[1].split('END_MATRIX')[0].strip()
        try:
            matrix = json.loads(matrix_json)
        except Exception as e:
            print(json.dumps({'matrix_parse_error': str(e)}))
    if matrix is None:
        print(json.dumps({'no_matrix': True, 'stdout_tail': out[-800:]}))
        return

    # Analyze corpus
    audio_bearing = []
    audio_stream_present_but_empty = []
    video_only = []
    for c in matrix:
        probe = c.get('probe', {})
        if not isinstance(probe, dict) or 'streams' not in probe:
            continue
        streams = probe.get('streams', [])
        audio_streams = [s for s in streams if s.get('codec_type') == 'audio']
        video_streams = [s for s in streams if s.get('codec_type') == 'video']
        c['audio_track_count'] = len(audio_streams)
        c['video_track_count'] = len(video_streams)
        c['audio_summary'] = [{
            'codec': s.get('codec_name'),
            'sample_rate': s.get('sample_rate'),
            'channels': s.get('channels'),
            'duration_s': s.get('duration'),
            'bit_rate': s.get('bit_rate'),
            'nb_frames': s.get('nb_frames')} for s in audio_streams]
        c['video_summary'] = [{
            'codec': s.get('codec_name'),
            'width': s.get('width'),
            'height': s.get('height'),
            'duration_s': s.get('duration'),
            'bit_rate': s.get('bit_rate')} for s in video_streams]
        # Bucket
        if not audio_streams:
            video_only.append(c.get('channel'))
        else:
            # Interpret duration
            max_audio_duration = 0.0
            for a in audio_streams:
                try:
                    d = float(a.get('duration') or 0)
                    if d > max_audio_duration: max_audio_duration = d
                except Exception:
                    pass
            c['max_audio_duration_s'] = max_audio_duration
            if max_audio_duration < 1.0:
                audio_stream_present_but_empty.append(c.get('channel'))
            else:
                audio_bearing.append(c.get('channel'))

    summary = {
        'total_channels_probed': len(matrix),
        'audio_bearing_count': len(audio_bearing),
        'audio_bearing_channels': audio_bearing,
        'audio_stream_present_but_empty_count': len(audio_stream_present_but_empty),
        'audio_stream_present_but_empty_channels': audio_stream_present_but_empty,
        'video_only_count': len(video_only),
        'video_only_channels': video_only,
    }
    print(json.dumps({'summary': summary}, indent=2))

    # Bank corpus matrix receipt (updated)
    receipts_dir = Path('/app/assessment_workspace/phase0/d12_poc_receipts')
    ts = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    matrix_path = receipts_dir / f'{ts}_d12_03_channel_corpus_characterization_v2.json'
    matrix_path.write_text(json.dumps({
        'wave': 'W-D12-POC',
        'sub_wave': 'D12_03_CHANNEL_CORPUS_CHARACTERIZATION_v2',
        'sealed_at_utc': ts,
        'kind': 'd12_03_corpus_characterization',
        'poc_flag': 'POC-NOT-PRODUCTION',
        'summary': summary,
        'per_channel': matrix,
        'ffprobe_scan_dt_s': round(dt,3),
        'provenance_note': ('shape-only ffprobe · zero file bytes emitted · '
                            'position-redaction hard-lock preserved · '
                            'to be folded into W-CENSUS-RUNTIME-ORCHESTRATION as '
                            'measured census media_types/audio_bearing_share field '
                            'per owner directive 2026-09-15T~11:05Z'),
    }, indent=2))
    os.chmod(matrix_path, 0o644)
    print(json.dumps({'corpus_matrix_receipt_v2': str(matrix_path),
                      'receipt_bytes': matrix_path.stat().st_size}))


if __name__ == '__main__':
    main()
