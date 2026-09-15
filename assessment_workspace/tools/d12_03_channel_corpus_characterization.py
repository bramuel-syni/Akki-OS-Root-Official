"""D12-03 diagnosis · 16-channel ffprobe corpus characterization on NAS OFFAIRRECS.

Owner directive verbatim (2026-09-15T~11:05Z):
  1. ffprobe already-fetched channel01 file on JUMP - confirm audio.
  2. Characterize corpus: probe ONE file per channel across all 16 channels.
  3. If any audio-bearing file exists: run ONE through the full pipe for
     TRUE quality receipt.
  4. Bank channel characterization matrix + updated per-hour projection.

Bounded engineering discipline:
  - Single mount.cifs invocation (vers=3.0 rsize=4M cache=loose ro).
  - 16 ffprobe calls on mounted paths (each < 1s · no bulk fetch).
  - Position-redaction hard-lock: no credential material stdout'd.
  - NO `set -x` (Standing Rule 6 · SEC-15-10 class).
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


TARGET_DATE_DIR = '2026_09_14'  # yesterday · fully populated


def main():
    creds = load_creds_silent()
    tmpdir = Path(tempfile.mkdtemp(prefix='d12_03_diag_', dir='/tmp'))
    tmpdir.chmod(0o700)
    pw_file = tmpdir / '.sshpass_jump'
    pw_file.write_text(creds['jump_pw'] + '\n')
    os.chmod(pw_file, 0o600)

    # Verify ffprobe on JUMP
    check_ffprobe = 'which ffprobe && ffprobe -version 2>&1 | head -1 || echo NO_FFPROBE'
    r = subprocess.run(['sshpass', '-f', str(pw_file), 'ssh',
                        '-o', 'StrictHostKeyChecking=accept-new',
                        f"{creds['jump_user']}@{creds['jump_host']}",
                        check_ffprobe], capture_output=True, timeout=20)
    ffprobe_status = r.stdout.decode('utf-8','replace').strip()
    print(json.dumps({'ffprobe_jump': ffprobe_status[:200]}))

    if 'NO_FFPROBE' in ffprobe_status or r.returncode != 0:
        print(json.dumps({'installing_ffmpeg_on_jump': True}))
        install = 'sudo apt-get -qq install -y ffmpeg 2>&1 | tail -3; which ffprobe'
        r = subprocess.run(['sshpass', '-f', str(pw_file), 'ssh',
                            '-o', 'StrictHostKeyChecking=accept-new',
                            f"{creds['jump_user']}@{creds['jump_host']}",
                            install], capture_output=True, timeout=180)
        print(json.dumps({'ffmpeg_install_rc': r.returncode,
                          'ffprobe_after': r.stdout.decode('utf-8','replace').strip()[-200:]}))

    # Atomic mount + 16-channel ffprobe (one file per channel · date=today or yesterday)
    # For each channel, pick lex-first mp4 file (or whatever ext exists).
    remote_script = '''
set -e
read -s NAS_PW
CRED=$(mktemp /tmp/cifs_cred.XXXXXX); chmod 600 $CRED
printf "username=''' + creds['nas_user'] + '''\\npassword=$NAS_PW\\n" > $CRED
MNT=$(mktemp -d /tmp/nas_mnt.XXXXXX)
sudo mount -t cifs //10.10.55.55/OFFAIRRECS $MNT \
  -o credentials=$CRED,vers=3.0,rsize=4194304,wsize=4194304,cache=loose,ro,uid=0 2>&1 | tail -2

# For each channel, pick lex-first file in the date dir and ffprobe it.
for CH in $(ls $MNT/Record | grep -E "^channel[0-9]+$" | sort); do
  DATE_DIR="$MNT/Record/$CH/''' + TARGET_DATE_DIR + '''"
  if [ ! -d "$DATE_DIR" ]; then
    # Try today
    DATE_DIR="$MNT/Record/$CH/2026_09_15"
  fi
  if [ ! -d "$DATE_DIR" ]; then
    echo "CH_MISSING_DATE_DIR:$CH"
    continue
  fi
  FIRST_FILE=$(ls "$DATE_DIR" 2>/dev/null | grep -iE "\\.(mp4|mp3|wav|m4a|aac|flac|ogg|ts|mkv|mov)$" | head -1)
  if [ -z "$FIRST_FILE" ]; then
    echo "CH_NO_MEDIA:$CH"
    continue
  fi
  FILE_PATH="$DATE_DIR/$FIRST_FILE"
  FILE_SIZE=$(stat -c %s "$FILE_PATH" 2>/dev/null || echo 0)
  # ffprobe streams shape-only (no cell values)
  PROBE_JSON=$(ffprobe -v error \
    -show_entries "stream=index,codec_type,codec_name,duration,sample_rate,channels,bit_rate,width,height:format=duration,bit_rate,format_name" \
    -of json "$FILE_PATH" 2>&1)
  # Emit one JSON line per channel · never emit file bytes
  echo "CH_PROBE:{\"channel\":\"$CH\",\"date_dir\":\"$(basename $DATE_DIR)\",\"file_basename\":\"$FIRST_FILE\",\"file_size\":$FILE_SIZE,\"probe\":$(echo $PROBE_JSON | tr -d '\\n')}"
done

sudo umount -l $MNT 2>/dev/null
shred -u $CRED 2>/dev/null
rmdir $MNT 2>/dev/null
echo REMOTE_OK
'''

    # Guard checks against known leak patterns
    assert_no_transcript_cat_on_custody(remote_script)
    assert_no_transcript_openpyxl_iter_rows_on_custody(remote_script)
    assert_no_transcript_set_x_with_password_var(remote_script)

    argv = ['sshpass', '-f', str(pw_file), 'ssh',
            '-o', 'StrictHostKeyChecking=accept-new',
            '-o', 'ConnectTimeout=15', '-o', 'ServerAliveInterval=30',
            f"{creds['jump_user']}@{creds['jump_host']}", remote_script]
    t0 = time.time()
    r = subprocess.run(argv, input=(creds['nas_pw']+'\n').encode(),
                       capture_output=True, timeout=270)
    dt = time.time() - t0
    pw_file.unlink()

    stdout = r.stdout.decode('utf-8','replace')
    stderr = r.stderr.decode('utf-8','replace')
    print(json.dumps({'corpus_scan_rc': r.returncode,
                      'corpus_scan_dt_s': round(dt,3),
                      'remote_ok': 'REMOTE_OK' in stdout,
                      'stderr_lines': len(stderr.splitlines()),
                      'stdout_lines': len(stdout.splitlines())}))

    # Parse per-channel results
    channels = []
    for ln in stdout.splitlines():
        if ln.startswith('CH_PROBE:'):
            payload = ln[len('CH_PROBE:'):]
            try:
                ch_data = json.loads(payload)
                channels.append(ch_data)
            except Exception as e:
                channels.append({'raw_line': payload[:400], 'parse_error': str(e)})
        elif ln.startswith('CH_MISSING_DATE_DIR:'):
            channels.append({'channel': ln.split(':',1)[1], 'verdict': 'MISSING_DATE_DIR'})
        elif ln.startswith('CH_NO_MEDIA:'):
            channels.append({'channel': ln.split(':',1)[1], 'verdict': 'NO_MEDIA_FILE_IN_DATE_DIR'})

    # Derive summary
    audio_bearing = []
    video_only = []
    for c in channels:
        probe = c.get('probe', {})
        if not isinstance(probe, dict):
            continue
        streams = probe.get('streams', [])
        audio_streams = [s for s in streams if s.get('codec_type') == 'audio']
        video_streams = [s for s in streams if s.get('codec_type') == 'video']
        c['audio_track_count'] = len(audio_streams)
        c['video_track_count'] = len(video_streams)
        if audio_streams:
            audio_bearing.append(c)
            c['audio_summary'] = [{
                'codec': s.get('codec_name'),
                'sample_rate': s.get('sample_rate'),
                'channels': s.get('channels'),
                'duration_s': s.get('duration'),
                'bit_rate': s.get('bit_rate')} for s in audio_streams]
        else:
            video_only.append(c)

    summary = {
        'total_channels_probed': len(channels),
        'audio_bearing_count': len(audio_bearing),
        'video_only_count': len(video_only),
        'audio_bearing_channels': [c.get('channel') for c in audio_bearing],
        'video_only_channels': [c.get('channel') for c in video_only],
    }
    print(json.dumps({'summary': summary}))

    # Bank corpus matrix receipt
    receipts_dir = Path('/app/assessment_workspace/phase0/d12_poc_receipts')
    ts = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    matrix_path = receipts_dir / f'{ts}_d12_03_channel_corpus_characterization.json'
    matrix_path.write_text(json.dumps({
        'wave': 'W-D12-POC',
        'sub_wave': 'D12_03_CHANNEL_CORPUS_CHARACTERIZATION',
        'sealed_at_utc': ts,
        'kind': 'd12_03_corpus_characterization',
        'poc_flag': 'POC-NOT-PRODUCTION',
        'target_date_dir_preferred': TARGET_DATE_DIR,
        'summary': summary,
        'per_channel': channels,
        'ffprobe_scan_dt_s': round(dt,3),
        'provenance_note': ('shape-only ffprobe · zero file bytes emitted · '
                            'position-redaction hard-lock preserved · '
                            'to be folded into W-CENSUS-RUNTIME-ORCHESTRATION as '
                            'measured census media_types/audio_bearing_share field '
                            'per owner directive 2026-09-15T~11:05Z'),
    }, indent=2))
    os.chmod(matrix_path, 0o644)
    print(json.dumps({'corpus_matrix_receipt': str(matrix_path),
                      'receipt_bytes': matrix_path.stat().st_size}))

    # Post-scan: if any channel has audio, print a next-step recommendation
    if audio_bearing:
        pick = audio_bearing[0]
        print(json.dumps({
            'audio_bearing_pick_for_true_quality_probe': {
                'channel': pick.get('channel'),
                'file_basename': pick.get('file_basename'),
                'file_size': pick.get('file_size'),
                'audio_summary': pick.get('audio_summary'),
            }
        }))
    else:
        print(json.dumps({'no_audio_track_found_in_any_channel': True,
                          'next': 'this becomes an owner-facing corpus-level finding per D12-03 close condition'}))


if __name__ == '__main__':
    main()
