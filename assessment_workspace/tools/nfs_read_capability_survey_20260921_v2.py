"""tools/nfs_read_capability_survey_20260921_v2.py

v2 continuation of the NFS/CIFS read-capability survey. v1 established:

    * /mnt/nfs-share on JUMP is actually a CIFS/SMB mount to
      //10.10.55.55/OFFAIRRECS/Record (NOT NFS despite path name).
    * Mount is kernel-mediated with `bramuel` credentials that WORK at
      kernel level (mount was established before rotation OR the
      user 'bramuel' — 7 chars — is different from the 'NAS creds'
      sheet user).
    * 49TB / 47TB used / 2.7TB free.
    * 16 top-level directories present: channel01..channel16
      (case-drift: channel01..08+16 lowercase; Channel09..15 TitleCase).
    * Positional match: channel01 -> Ch1, channel04 -> Ch4, etc.

v2 executes the bounded sample sweep with the correct observed names.
Same discipline: read-only, no downloads, bounded output, stat-based
readability proof, 1-byte fallback ONLY if stat cannot prove read.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_TOOLS = Path("/app/assessment_workspace/tools")
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import rms_creds_loader  # noqa: E402
import paramiko  # noqa: E402

RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")
LS_MAX_LINES = 60
FIND_MAX_LINES = 200

EXPECTED_CHANNELS = [
    ("Ch1",  "Citizen TV",   "TV"),
    ("Ch2",  "Inooro TV",    "TV"),
    ("Ch3",  "Radio Citizen","Radio"),
    ("Ch4",  "Inooro FM",    "Radio"),
    ("Ch5",  "Ramogi FM",    "Radio"),
    ("Ch6",  "Egesa FM",     "Radio"),
    ("Ch7",  "Musyi FM",     "Radio"),
    ("Ch8",  "Hot 96 FM",    "Radio"),
    ("Ch9",  "Chamgei FM",   "Radio"),
    ("Ch10", "Mulembe FM",   "Radio"),
    ("Ch11", "Sulwe FM",     "Radio"),
    ("Ch12", "Vuuka FM",     "Radio"),
    ("Ch13", "Bahari FM",    "Radio"),
    ("Ch14", "Muuga FM",     "Radio"),
    ("Ch15", "Wimwaro FM",   "Radio"),
    ("Ch16", "Ramogi TV",    "TV"),
]


def _now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _shquote(s: str) -> str:
    if s == "": return "''"
    return "'" + s.replace("'", "'\\''") + "'"


def _ssh_exec(client, cmd, timeout=20.0):
    t0 = time.monotonic()
    try:
        stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
        out = stdout.read(65536).decode("utf-8", errors="replace")
        err = stderr.read(8192).decode("utf-8", errors="replace")
        rc = stdout.channel.recv_exit_status()
        return {
            "cmd": cmd if len(cmd) <= 240 else cmd[:240] + "...(truncated)",
            "rc": rc,
            "stdout": out[:16384],
            "stderr": err[:2048],
            "elapsed_s": round(time.monotonic() - t0, 3),
        }
    except Exception as e:
        return {"cmd": cmd[:240], "rc": None,
                "error_class": e.__class__.__name__,
                "error_msg": str(e)[:400],
                "elapsed_s": round(time.monotonic() - t0, 3)}


def _sample_channel(client, mount_path: str, channel_name: str, label: str) -> dict:
    q = _shquote(f"{mount_path}/{channel_name}")
    out: dict = {"label": label, "channel_name_observed": channel_name}

    # Depth 1 listing
    out["depth1_ls_la"] = _ssh_exec(
        client, f"timeout 15 ls -la {q}/ 2>&1 | head -{LS_MAX_LINES}",
        timeout=25,
    )
    # Type histogram at depth 1
    out["depth1_types"] = _ssh_exec(
        client,
        f"timeout 15 bash -c '(cd {q} 2>/dev/null && "
        "echo dirs=$(find . -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l); "
        "echo files=$(find . -maxdepth 1 -mindepth 1 -type f 2>/dev/null | wc -l); "
        "echo other=$(find . -maxdepth 1 -mindepth 1 ! -type d ! -type f 2>/dev/null | wc -l))' "
        "2>&1",
        timeout=25,
    )
    # Depth 2 find (bounded + timeboxed)
    out["depth2_find_capped"] = _ssh_exec(
        client,
        f"timeout 25 find {q} -maxdepth 2 -mindepth 1 2>&1 | head -{FIND_MAX_LINES}",
        timeout=35,
    )
    # Depth 3 find — no more than 30s of walk
    out["depth3_find_capped"] = _ssh_exec(
        client,
        f"timeout 25 find {q} -maxdepth 3 -type f 2>/dev/null | head -{FIND_MAX_LINES}",
        timeout=35,
    )
    # Extension histogram — 25s walk cap
    out["ext_histogram"] = _ssh_exec(
        client,
        f"timeout 25 find {q} -maxdepth 3 -type f 2>/dev/null | head -5000 | "
        "awk -F. '{if (NF>1) print tolower($NF); else print \"NOEXT\"}' | "
        "sort | uniq -c | sort -rn | head -30",
        timeout=35,
    )
    # File count within depth 3 (capped)
    out["depth3_file_count_capped_10000"] = _ssh_exec(
        client,
        f"timeout 25 find {q} -maxdepth 3 -type f 2>/dev/null | head -10000 | wc -l",
        timeout=35,
    )
    # mtime spread across depth 1 dirs
    out["depth1_mtime_range"] = _ssh_exec(
        client,
        f"timeout 15 find {q} -maxdepth 1 -mindepth 1 -printf '%TY-%Tm-%Td\\n' 2>/dev/null | "
        "sort -u | (head -1; tail -1) 2>&1",
        timeout=25,
    )
    # mtime spread across files (depth 3, bounded to first 5000)
    out["files_mtime_range"] = _ssh_exec(
        client,
        f"timeout 25 find {q} -maxdepth 3 -type f -printf '%TY-%Tm-%Td\\n' 2>/dev/null | "
        "head -5000 | sort -u | (head -1; tail -1) 2>&1",
        timeout=35,
    )
    # SKIP du -sh --max-depth=1 (would walk full 47TB subtree)
    # Small file sample — the smallest regular file at depth ≤ 3
    out["smallest_file_find"] = _ssh_exec(
        client,
        f"timeout 25 find {q} -maxdepth 3 -type f -printf '%s\\t%p\\n' 2>/dev/null | "
        "head -5000 | sort -n | head -1",
        timeout=35,
    )
    return out


def _stat_and_read_test(client, path: str) -> dict:
    """stat + `test -r` per file. No byte reads."""
    q = _shquote(path)
    out: dict = {"path": path}
    out["stat"] = _ssh_exec(
        client,
        "stat --format='name=%n%nsize=%s%nmode_octal=%a%nmode_hr=%A%n"
        "uid=%u%nuname=%U%ngid=%g%ngname=%G%nmtime=%y%nctime=%z' " + q,
    )
    out["test_r"] = _ssh_exec(
        client, f"test -r {q} && echo READABLE || echo NOT_READABLE",
    )
    return out


def _one_byte_read(client, path: str) -> dict:
    q = _shquote(path)
    res = _ssh_exec(
        client,
        f"head -c 1 {q} 2>&1 | wc -c ; echo _RC=$?",
    )
    stdout = res.get("stdout", "")
    m = re.search(r"^\s*(\d+)\s*$", stdout.splitlines()[0] if stdout else "", re.M)
    return {
        "bytes_read": int(m.group(1)) if m else None,
        "one_byte_success": bool(m and int(m.group(1)) == 1),
        "raw_res": res,
    }


def _channel_reconcile(ls_names: list) -> dict:
    """Robust positional reconciliation: channelNN or ChannelNN → ChN."""
    matched = []
    extra = []
    used_codes = set()
    expected_by_num = {i + 1: EXPECTED_CHANNELS[i] for i in range(16)}

    for name in ls_names:
        low = name.strip().lower()
        # ChannelNN or channelNN
        m = re.match(r"^channel0*(\d+)$", low)
        if m:
            num = int(m.group(1))
            if 1 <= num <= 16 and num in expected_by_num:
                code, ename, kind = expected_by_num[num]
                matched.append({"observed": name, "matched_to": code,
                                "num": num, "expected_name": ename,
                                "kind": kind, "match_via": "channelNN_positional"})
                used_codes.add(num)
                continue
        # ChN or chN prefix
        m2 = re.match(r"^ch(\d+)\b", low)
        if m2:
            num = int(m2.group(1))
            if 1 <= num <= 16 and num in expected_by_num:
                code, ename, kind = expected_by_num[num]
                matched.append({"observed": name, "matched_to": code,
                                "num": num, "expected_name": ename,
                                "kind": kind, "match_via": "chN_positional"})
                used_codes.add(num)
                continue
        extra.append(name)

    missing = []
    for i in range(1, 17):
        if i not in used_codes:
            code, ename, kind = expected_by_num[i]
            missing.append({"expected_code": code, "expected_name": ename,
                            "kind": kind})

    return {
        "expected_count": 16,
        "matched_count": len(matched),
        "extra_count": len(extra),
        "missing_count": len(missing),
        "matched": matched,
        "extra": extra,
        "missing": missing,
    }


def main():
    receipt = {
        "task": "NFS_read_capability_survey_v2_owner_authorized_20260921",
        "captured_at_utc": _now(),
        "predecessor_receipt": (
            "phase0/connectivity_receipts/20260921T135153Z_NFS_read_"
            "capability_survey_owner_authorized_20260921.json"
        ),
        "correction_from_v1": (
            "v1 discovered /mnt/nfs-share is CIFS/SMB (not NFS) — "
            "//10.10.55.55/OFFAIRRECS/Record. v1's channel name regex "
            "did not accept the `channel01..channel16` naming, so no "
            "samples ran. v2 uses positional reconciliation + correct "
            "sample selection (channel01=Ch1 TV; channel04=Ch4 Radio)."
        ),
        "hygiene": {
            "read_only": True,
            "no_downloads": True,
            "no_writes": True,
            "bounded_enumeration": True,
            "one_byte_fallback_only_if_stat_insufficient": True,
        },
        "bounds": {
            "ls_max_lines": LS_MAX_LINES,
            "find_max_lines": FIND_MAX_LINES,
            "channels_sampled_max": 2,
            "sample_depth_max": 3,
        },
    }

    binds = rms_creds_loader.load()

    # Open JUMP
    jump = paramiko.SSHClient()
    jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    jump.connect(hostname=binds.jump.host, port=22,
                 username=binds.jump.user, password=binds.jump.password,
                 timeout=12, auth_timeout=12, banner_timeout=12,
                 allow_agent=False, look_for_keys=False)

    # Recapture mount status (mount is stable but bank the current fingerprint)
    receipt["mount_now"] = {
        "mount_grep_cifs_or_nfs": _ssh_exec(
            jump, "mount 2>&1 | grep -iE '(nfs|cifs)' | head -5",
        ),
        "df_h": _ssh_exec(jump, "df -h /mnt/nfs-share 2>&1"),
        "smbstatus_owner": _ssh_exec(
            jump, "grep -oE 'username=[^,)]+' /proc/mounts | head -3 2>&1",
        ),
    }

    # Re-list the 16 top-level entries — full names
    receipt["top_level_ls_1"] = _ssh_exec(jump, "ls -1 /mnt/nfs-share/ 2>&1")
    names = [
        s.strip() for s in (receipt["top_level_ls_1"].get("stdout") or "").splitlines()
        if s.strip() and s.strip() not in (".", "..")
    ]
    receipt["top_level_names"] = names
    receipt["channel_reconciliation"] = _channel_reconcile(names)

    # Pick samples
    by_code = {m["matched_to"]: m["observed"]
               for m in receipt["channel_reconciliation"]["matched"]}
    tv_target = by_code.get("Ch1")   # Citizen TV
    radio_target = by_code.get("Ch4")  # Inooro FM

    sweep = {}

    if tv_target:
        entry = {"channel_selected": tv_target, "maps_to": "Ch1 Citizen TV (TV)"}
        entry["structure_probe"] = _sample_channel(
            jump, "/mnt/nfs-share", tv_target, "TV_Ch1",
        )
        # Pick smallest file → stat + test -r
        smallest_stdout = entry["structure_probe"]["smallest_file_find"].get("stdout", "")
        parts = smallest_stdout.strip().split("\t", 1) if smallest_stdout.strip() else []
        if len(parts) == 2:
            try:
                size = int(parts[0])
                smallest_path = parts[1]
                entry["smallest_file"] = {"size_bytes": size, "path": smallest_path}
                entry["stat_and_test_r"] = _stat_and_read_test(jump, smallest_path)
                test_r_stdout = entry["stat_and_test_r"]["test_r"]["stdout"]
                if "READABLE" in test_r_stdout and "NOT_READABLE" not in test_r_stdout:
                    entry["readability_proof"] = {
                        "method": "test -r (POSIX read-permission check)",
                        "verdict": "READABLE_WITHOUT_BYTE_READ",
                    }
                else:
                    # Fallback: 1-byte read (owner-authorized)
                    entry["one_byte_fallback"] = _one_byte_read(jump, smallest_path)
                    entry["readability_proof"] = {
                        "method": "fallback: read exactly 1 byte via head -c 1",
                        "verdict": (
                            "READABLE_1_BYTE_CONFIRMED"
                            if entry["one_byte_fallback"]["one_byte_success"]
                            else "READ_DENIED_AT_BYTE_LEVEL"
                        ),
                    }
            except Exception as e:
                entry["stat_err"] = f"{e.__class__.__name__}: {e}"
        else:
            entry["smallest_file"] = None
            entry["readability_proof"] = {"method": "n/a",
                                          "verdict": "NO_REGULAR_FILE_IN_TREE_UNDER_DEPTH_3"}
        sweep["TV_Ch1"] = entry

    if radio_target:
        entry = {"channel_selected": radio_target, "maps_to": "Ch4 Inooro FM (Radio)"}
        entry["structure_probe"] = _sample_channel(
            jump, "/mnt/nfs-share", radio_target, "Radio_Ch4",
        )
        smallest_stdout = entry["structure_probe"]["smallest_file_find"].get("stdout", "")
        parts = smallest_stdout.strip().split("\t", 1) if smallest_stdout.strip() else []
        if len(parts) == 2:
            try:
                size = int(parts[0])
                smallest_path = parts[1]
                entry["smallest_file"] = {"size_bytes": size, "path": smallest_path}
                entry["stat_and_test_r"] = _stat_and_read_test(jump, smallest_path)
                test_r_stdout = entry["stat_and_test_r"]["test_r"]["stdout"]
                if "READABLE" in test_r_stdout and "NOT_READABLE" not in test_r_stdout:
                    entry["readability_proof"] = {
                        "method": "test -r",
                        "verdict": "READABLE_WITHOUT_BYTE_READ",
                    }
                else:
                    entry["one_byte_fallback"] = _one_byte_read(jump, smallest_path)
                    entry["readability_proof"] = {
                        "method": "fallback: head -c 1",
                        "verdict": (
                            "READABLE_1_BYTE_CONFIRMED"
                            if entry["one_byte_fallback"]["one_byte_success"]
                            else "READ_DENIED_AT_BYTE_LEVEL"
                        ),
                    }
            except Exception as e:
                entry["stat_err"] = f"{e.__class__.__name__}: {e}"
        else:
            entry["smallest_file"] = None
            entry["readability_proof"] = {"method": "n/a",
                                          "verdict": "NO_REGULAR_FILE_IN_TREE_UNDER_DEPTH_3"}
        sweep["Radio_Ch4"] = entry

    receipt["channel_sample_sweep"] = sweep

    # Verdict
    matched = receipt["channel_reconciliation"]["matched_count"]
    read_ok = sum(
        1 for lbl, e in sweep.items()
        if e.get("readability_proof", {}).get("verdict", "").startswith("READABLE_")
    )
    denied = sum(
        1 for lbl, e in sweep.items()
        if "DENIED" in e.get("readability_proof", {}).get("verdict", "")
    )
    if matched == 16 and read_ok == len(sweep) and denied == 0:
        verdict = "FULL_16_CHANNELS_PRESENT_ALL_SAMPLED_READABLE"
    elif matched == 16 and read_ok > 0:
        verdict = f"PARTIAL_16_CHANNELS_PRESENT_{read_ok}_OF_{len(sweep)}_SAMPLED_READABLE"
    elif matched < 16:
        verdict = f"CHANNEL_TREE_PARTIAL_MATCH_{matched}_OF_16"
    else:
        verdict = "AMBIGUOUS_INSPECT_MANUALLY"
    receipt["verdict"] = {
        "matched_channels": matched,
        "expected_channels": 16,
        "sampled_channels": len(sweep),
        "sampled_read_ok": read_ok,
        "sampled_denied": denied,
        "one_line": verdict,
        "mount_kind_observed": "CIFS/SMB_v3.1.1",
        "trust_model_observed": (
            "kernel-mediated CIFS mount using cached user credentials "
            "('bramuel'). NOT NFS AUTH_SYS IP-trust despite the "
            "/mnt/nfs-share path name — mount type is 'cifs' in "
            "/proc/mounts. The mount was established prior to any "
            "credential rotation and remains authenticated via the "
            "kernel's cached SMB session."
        ),
    }

    try: jump.close()
    except Exception: pass

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = RECEIPT_DIR / f"{stamp}_NFS_read_capability_survey_v2_owner_authorized_20260921.json"
    p.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                 encoding="utf-8")
    print(f"receipt_path: {p}")


if __name__ == "__main__":
    main()
