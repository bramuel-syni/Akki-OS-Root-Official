"""D12 POC live-run · Stage 4 · enumerate ≤3 audio files in NAS channel01.

Uses smbclient `ls` on JUMP-side. NAS pw via stdin, JUMP root pw via
sshpass -f. Only file-listing metadata returns; no bytes fetched yet.
Output is CP-A2 canonical-key shape for each file.
"""
from __future__ import annotations

import json, os, subprocess, sys, tempfile, time
from pathlib import Path

sys.path.insert(0, '/app/assessment_workspace/repos/Extraction-Akki/backend')
from services.secret_hygiene.custody_file import assert_no_transcript_cat_on_custody
sys.path.insert(0, str(Path(__file__).resolve().parent))
from d12_poc_live_probe import load_creds_silent, _redacted_verdict

CHANNEL = 'channel01'


def stage_4_enumerate_audio(creds: dict, tmpdir: Path) -> dict:
    stage = 'stage_4_enumerate_audio_in_' + CHANNEL
    pw_file = tmpdir / '.sshpass_jump'
    pw_file.write_text(creds['jump_pw'] + '\n')
    os.chmod(pw_file, 0o600)

    # smbclient -c "ls Record/channel01/*.*" via a here-doc; NAS pw via stdin.
    # Filter to audio-shaped extensions (.wav .mp3 .m4a .aac) and lexicographic order.
    remote_script = (
        'set -e; '
        'read -s NAS_PW; '
        'PASSWD="$NAS_PW" smbclient //10.10.55.55/OFFAIRRECS -U ' + creds['nas_user'] +
        ' -c "cd Record/' + CHANNEL + '; ls" 2>&1 | '
        'grep -iE "\\.(wav|mp3|m4a|aac|flac|ogg)\\b" | head -20; '
        'unset NAS_PW PASSWD; echo REMOTE_OK'
    )
    assert_no_transcript_cat_on_custody(remote_script)
    argv = [
        'sshpass', '-f', str(pw_file),
        'ssh', '-o', 'StrictHostKeyChecking=accept-new',
        '-o', 'ConnectTimeout=15',
        f"{creds['jump_user']}@{creds['jump_host']}",
        remote_script,
    ]
    t0 = time.time()
    r = subprocess.run(argv, input=(creds['nas_pw'] + '\n').encode(),
                       capture_output=True, timeout=90)
    dt = time.time() - t0
    pw_file.unlink()

    out = r.stdout.decode('utf-8', 'replace').strip()
    err = r.stderr.decode('utf-8', 'replace').strip()
    lines = [ln for ln in out.splitlines() if 'REMOTE_OK' not in ln and ln.strip()]

    # Parse each line via the sealed CP-A2 parser to get canonical keys
    from services.audio_poc.recording_inventory import (
        parse_smbclient_ls_line, RecordingKeyInvalid,
    )
    from services.audio_poc.recording_inventory import _PATH_REGEX

    parsed = []
    unparsable = 0
    for ln in lines:
        try:
            pr = parse_smbclient_ls_line(ln)
            if pr is not None:
                # pr is a (filename, size, mtime) tuple per the CP-A2 contract
                parsed.append({
                    'raw_line_shape': {'len': len(ln), 'sha256_12': __import__('hashlib').sha256(ln.encode()).hexdigest()[:12]},
                    'parsed': pr,
                })
            else:
                unparsable += 1
        except Exception:
            unparsable += 1

    # Pick lexicographically-first 3 by filename
    parsed.sort(key=lambda x: x['parsed'][0] if isinstance(x.get('parsed'), tuple) else str(x.get('parsed', '')))
    picked = parsed[:3]

    return {
        'stage': stage,
        'verdict': 'PASS' if r.returncode == 0 and picked else 'FAIL',
        'dt_seconds': round(dt, 3),
        'rc': r.returncode,
        'lines_matched': len(lines),
        'parsed_count': len(parsed),
        'unparsable_count': unparsable,
        'picked_count': len(picked),
        'picked': [
            {
                'filename': p['parsed'][0] if isinstance(p['parsed'], tuple) else str(p['parsed']),
                'size_bytes': p['parsed'][1] if isinstance(p['parsed'], tuple) and len(p['parsed'])>1 else None,
                'raw_line_shape': p['raw_line_shape'],
            } for p in picked
        ],
        'stderr_line_count': len(err.splitlines()) if err else 0,
    }


def main():
    tmpdir = Path(tempfile.mkdtemp(prefix='d12_poc_stage4_', dir='/tmp'))
    tmpdir.chmod(0o700)
    print(json.dumps({'tmpdir': str(tmpdir)}))
    try:
        creds = load_creds_silent()
        print(json.dumps({'creds_load': 'PASS', 'keys': sorted(creds.keys())}))
        v4 = stage_4_enumerate_audio(creds, tmpdir)
        print(json.dumps(v4))
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
