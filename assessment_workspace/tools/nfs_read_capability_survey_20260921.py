"""tools/nfs_read_capability_survey_20260921.py

Owner directive verbatim this-session (2026-09-21T~13:55Z):

    "OWNER GO → NFS READ-CAPABILITY SURVEY. The owner supplied a new
    access path: NFS export at `/mnt/nfs-share`, expected to hold
    broadcast content organized by 16 RMS channels/stations."

Discipline:
    * READ-ONLY across every touch.
    * Vantage: JUMP first (LAN-trusted; NFS commonly IP-based trust).
    * Existing mount preferred; if a probe-mount is required, use
      `mount -o ro,nolock,soft,timeo=50` and `umount` at end.
    * NO file byte reads unless `stat` alone cannot prove readability;
      in that case, read exactly ONE byte from the smallest sampled
      file (owner-authorized fallback).
    * Bounded enumeration — sample 2 channels (1 TV, 1 Radio) at
      depth ≤3; cap `ls`/`find` output.
    * Distinguish 4 failure classes: no-export / mount-denied /
      perm-denied / stale-handle.
    * Zero downloads. Zero writes. Never modify existing mounts.

Emits: phase0/connectivity_receipts/20260921T{HHMMSS}Z_NFS_read_
capability_survey_owner_authorized_20260921.json
"""

from __future__ import annotations

import hashlib
import json
import re
import socket
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_TOOLS = Path("/app/assessment_workspace/tools")
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import rms_creds_loader  # noqa: E402
import paramiko  # noqa: E402

RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")

# Owner-provided expected channel map — treat as reference, verify vs reality.
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

# Sample plan: 1 TV, 1 Radio (Ch1 Citizen TV + Ch4 Inooro FM). Pick
# fallbacks if not present.
SAMPLE_TV_PRIMARY = "Ch1"
SAMPLE_RADIO_PRIMARY = "Ch4"

# Output caps
LS_MAX_LINES = 60
FIND_MAX_LINES = 200
STAT_MAX_LINES = 40


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_file(p: Path) -> Optional[str]:
    if not p.is_file(): return None
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _ssh_exec(client, cmd, timeout=20.0):
    """Run cmd on remote; capture rc/stdout/stderr timeboxed."""
    t0 = time.monotonic()
    try:
        stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout,
                                                    get_pty=False)
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
        return {
            "cmd": cmd if len(cmd) <= 240 else cmd[:240] + "...(truncated)",
            "rc": None,
            "error_class": e.__class__.__name__,
            "error_msg": str(e)[:400],
            "elapsed_s": round(time.monotonic() - t0, 3),
        }


def _who_am_i(client) -> dict:
    """Fingerprint the JUMP identity we're running under."""
    return {
        "whoami":  _ssh_exec(client, "whoami"),
        "id":      _ssh_exec(client, "id"),
        "hostname":_ssh_exec(client, "hostname"),
        "uname":   _ssh_exec(client, "uname -a"),
    }


def _mount_snapshot(client) -> dict:
    """Read-only capture of the mount table + /mnt/nfs-share status."""
    return {
        "mount_grep_nfs":     _ssh_exec(client, "mount 2>&1 | grep -i nfs || echo _NO_NFS_MOUNT"),
        "proc_mounts_nfs":    _ssh_exec(client, "grep -i nfs /proc/mounts 2>&1 || echo _NO_NFS_IN_PROC_MOUNTS"),
        "df_mnt_nfs_share":   _ssh_exec(client, "df -h /mnt/nfs-share 2>&1"),
        "ls_slash_mnt":       _ssh_exec(client, "ls -la /mnt/ 2>&1 | head -20"),
        "ls_mnt_nfs_share":   _ssh_exec(client, "ls -la /mnt/nfs-share/ 2>&1 | head -{}".format(LS_MAX_LINES)),
        "stat_mnt_nfs_share": _ssh_exec(client, "stat /mnt/nfs-share 2>&1"),
    }


def _showmount_probes(client, servers: list) -> dict:
    """Try `showmount -e <server>` against candidate NFS servers.

    Note: some NFS servers hide showmount by default (NFSv4). Missing
    export list ≠ no export; still worth capturing.
    """
    out = {}
    for label, host in servers:
        # rpcinfo first for portmap presence
        out[f"rpcinfo_{label}_{host}"] = _ssh_exec(
            client, f"rpcinfo -p {host} 2>&1 | head -30",
        )
        out[f"showmount_e_{label}_{host}"] = _ssh_exec(
            client, f"showmount -e {host} 2>&1",
        )
        # NFSv4 pseudo-fs discovery — attempt a temp ro-mount at nothing
        # and inspect. Skipped here; only run explicit mount if directed.
    return out


def _classify_showmount(res: dict) -> str:
    """Read failure layer from showmount stdout+stderr."""
    if res is None: return "NOT_PROBED"
    combined = ((res.get("stdout") or "") + " " + (res.get("stderr") or "")).lower()
    if "export list for" in combined:
        return "EXPORTS_LISTED"
    if "no route to host" in combined:
        return "NO_ROUTE"
    if "connection refused" in combined:
        return "TCP_REFUSED"
    if "clnt_create" in combined and "rpc" in combined:
        return "RPC_UNAVAILABLE_(maybe_NFSv4_only_or_portmap_off)"
    if "access denied" in combined or "permission denied" in combined:
        return "ACL_DENIED"
    if res.get("rc") == 0 and combined.strip():
        return "OK_MAYBE_EMPTY"
    return "UNKNOWN"


def _enumerate_top_level(client, mount_path: str) -> dict:
    """Enumerate top-level of the NFS mount and reconcile with owner map."""
    out: dict = {"mount_path": mount_path}
    # ls -la
    out["ls_la_root"] = _ssh_exec(
        client, f"ls -la {mount_path}/ 2>&1 | head -{LS_MAX_LINES}",
    )
    # Just names — one-per-line, no dotfiles
    out["ls_1_root"] = _ssh_exec(
        client, f"ls -1 {mount_path}/ 2>&1 | head -{LS_MAX_LINES}",
    )
    # Directory count vs file count at top level
    out["top_level_counts"] = _ssh_exec(
        client,
        f"(cd {mount_path} 2>/dev/null && "
        "find . -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l; "
        "find . -maxdepth 1 -mindepth 1 -type f 2>/dev/null | wc -l) "
        "2>&1",
    )
    return out


def _reconcile_channels(top_ls_lines: list) -> dict:
    """Match observed top-level entries against the 16 expected channels.

    Emits: matched, extra, missing.
    """
    expected_by_prefix = {}
    for code, name, kind in EXPECTED_CHANNELS:
        expected_by_prefix[code.lower()] = (code, name, kind)

    matched = []
    extra = []
    used_codes = set()

    for line in top_ls_lines:
        line = line.strip()
        if not line or line in (".", ".."):
            continue
        low = line.lower()
        # match Ch<N> prefix with optional space/dash/underscore
        m = re.match(r"^(ch\d+)\b", low)
        code_hit = None
        if m:
            code_hit = m.group(1)
        else:
            # try softer match: look for any ch<n>
            m2 = re.search(r"\bch\d+\b", low)
            if m2: code_hit = m2.group(0)
        if code_hit and code_hit in expected_by_prefix:
            code, name, kind = expected_by_prefix[code_hit]
            matched.append({"observed": line, "matched_to": code, "name": name, "kind": kind})
            used_codes.add(code_hit)
        else:
            # Maybe name-based match (e.g. "Citizen TV")
            name_match = None
            for code, name, kind in EXPECTED_CHANNELS:
                if name.lower() in low or low in name.lower():
                    name_match = (code, name, kind)
                    break
            if name_match:
                code, name, kind = name_match
                matched.append({"observed": line, "matched_to": code,
                                "name": name, "kind": kind,
                                "match_via": "name"})
                used_codes.add(code.lower())
            else:
                extra.append(line)

    missing = []
    for code, name, kind in EXPECTED_CHANNELS:
        if code.lower() not in used_codes:
            missing.append({"expected_code": code, "expected_name": name, "kind": kind})

    return {
        "expected_count": len(EXPECTED_CHANNELS),
        "matched_count": len(matched),
        "extra_count": len(extra),
        "missing_count": len(missing),
        "matched": matched,
        "extra": extra,
        "missing": missing,
    }


def _parse_ls_names(ls_stdout: str) -> list:
    """Extract non-empty non-dotdot names from `ls -1` output."""
    return [
        ln.strip()
        for ln in (ls_stdout or "").splitlines()
        if ln.strip() and ln.strip() not in (".", "..")
    ]


def _sample_channel(client, mount_path: str, channel_observed_name: str,
                    label: str) -> dict:
    """Descend 2-3 levels into one channel; sample file naming + shape.

    Bounded: ls at each level capped at LS_MAX_LINES; find -maxdepth 3
    capped at FIND_MAX_LINES lines.
    """
    q = _shquote(f"{mount_path}/{channel_observed_name}")
    out: dict = {"label": label, "channel_name_observed": channel_observed_name}
    # Depth 1 listing
    out["depth1_ls_la"] = _ssh_exec(
        client, f"ls -la {q}/ 2>&1 | head -{LS_MAX_LINES}",
    )
    # File type histogram at depth 1
    out["depth1_types"] = _ssh_exec(
        client,
        f"(cd {q} 2>/dev/null && "
        "echo dirs=$(find . -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l); "
        "echo files=$(find . -maxdepth 1 -mindepth 1 -type f 2>/dev/null | wc -l); "
        "echo other=$(find . -maxdepth 1 -mindepth 1 ! -type d ! -type f 2>/dev/null | wc -l)"
        ") 2>&1",
    )
    # Depth 2 sample — one representative subdir + inside listing
    out["depth2_find_sample"] = _ssh_exec(
        client,
        f"find {q} -maxdepth 2 -mindepth 1 2>&1 | head -{FIND_MAX_LINES}",
    )
    # File extension histogram (bounded)
    out["depth2_ext_histogram"] = _ssh_exec(
        client,
        f"find {q} -maxdepth 3 -type f 2>/dev/null | "
        "awk -F. '{if (NF>1) print tolower($NF); else print \"NOEXT\"}' | "
        f"sort | uniq -c | sort -rn | head -30",
    )
    # Depth 3 find — VERY bounded (200 lines)
    out["depth3_find_capped"] = _ssh_exec(
        client,
        f"find {q} -maxdepth 3 -type f 2>/dev/null | head -{FIND_MAX_LINES}",
    )
    # mtime range at depth 1
    out["depth1_mtime_range"] = _ssh_exec(
        client,
        f"find {q} -maxdepth 1 -mindepth 1 -printf '%TY-%Tm-%Td\\n' 2>/dev/null | "
        "sort -u | (head -1; tail -1) 2>&1",
    )
    # Size / mtime spread across depth 2 (bounded)
    out["depth2_size_mtime_sample"] = _ssh_exec(
        client,
        f"find {q} -maxdepth 3 -type f -printf '%s\\t%TY-%Tm-%Td\\t%p\\n' 2>/dev/null | "
        "head -30 2>&1",
    )
    return out


def _shquote(s: str) -> str:
    """Single-quote shell-quote."""
    if s == "": return "''"
    return "'" + s.replace("'", "'\\''") + "'"


def _smallest_file_stat(client, mount_path: str, channel_name: str) -> dict:
    """Find the smallest regular file in the channel tree (depth <=3),
    stat it, and return a metadata-only view. No byte reads unless
    explicitly authorized by fallback path."""
    q = _shquote(f"{mount_path}/{channel_name}")
    # Get smallest file's path + size, capped by find -maxdepth 3.
    out: dict = {"channel": channel_name}
    find_cmd = (
        f"find {q} -maxdepth 3 -type f -printf '%s\\t%p\\n' 2>/dev/null | "
        "sort -n | head -1 2>&1"
    )
    res = _ssh_exec(client, find_cmd)
    out["find_smallest"] = res
    line = (res.get("stdout") or "").strip().splitlines()
    if not line:
        out["smallest_file"] = None
        out["notes"] = "NO_FILES_UNDER_DEPTH_3_OR_EMPTY_TREE"
        return out
    parts = line[0].split("\t", 1)
    if len(parts) != 2:
        out["smallest_file"] = None
        out["notes"] = "COULD_NOT_PARSE_FIND_OUTPUT"
        return out
    try:
        size = int(parts[0])
    except Exception:
        size = None
    smallest_path = parts[1]
    out["smallest_file"] = {"size_bytes": size, "path": smallest_path}
    # stat proves readability without opening bytes
    stat_res = _ssh_exec(
        client,
        "stat --format='name=%n%nsize=%s%nmode_octal=%a%nmode_hr=%A%n"
        "uid=%u%ngid=%g%nmtime=%y%nctime=%z%natime=%x' "
        + _shquote(smallest_path),
    )
    out["stat_result"] = stat_res
    # Read access test: `test -r <file>` — proves the mount UID can
    # read it WITHOUT actually reading bytes.
    test_r = _ssh_exec(
        client, f"test -r {_shquote(smallest_path)} && echo READABLE || echo NOT_READABLE",
    )
    out["test_r"] = test_r
    return out


def _one_byte_fallback(client, path: str) -> dict:
    """OWNER-AUTHORIZED FALLBACK: read exactly ONE byte from a file.
    Returns success/failure — never the byte value itself."""
    q = _shquote(path)
    cmd = f"head -c 1 {q} 2>&1 | wc -c ; echo _RC=$?"
    res = _ssh_exec(client, cmd)
    out = {
        "cmd_shape": "head -c 1 | wc -c",
        "rc_line_present": "_RC=" in (res.get("stdout") or ""),
        "raw_res": res,
    }
    m = re.search(r"^\s*(\d+)\s*$", (res.get("stdout") or "").splitlines()[0] if res.get("stdout") else "", re.M)
    if m:
        out["bytes_read"] = int(m.group(1))
        out["one_byte_success"] = int(m.group(1)) == 1
    else:
        out["bytes_read"] = None
        out["one_byte_success"] = False
    return out


def _classify_verdict(top: dict, channel_sweep: dict) -> dict:
    """Compute the binary readability verdict + failure layer."""
    reconciled = top.get("channel_reconciliation", {})
    matched = reconciled.get("matched_count", 0)
    expected = reconciled.get("expected_count", 0)
    denied = 0
    read_ok = 0
    for _, res in channel_sweep.items():
        stat = res.get("smallest_file_probe", {})
        if stat.get("test_r", {}).get("stdout", "").strip().endswith("READABLE"):
            read_ok += 1
        elif "NOT_READABLE" in (stat.get("test_r", {}).get("stdout") or ""):
            denied += 1
    v = {
        "matched_channels": matched,
        "expected_channels": expected,
        "sampled_channels": len(channel_sweep),
        "sampled_read_ok": read_ok,
        "sampled_denied": denied,
    }
    if matched == 0:
        v["verdict"] = "NO_CHANNEL_MATCH_TREE_STRUCTURE_UNEXPECTED"
    elif read_ok == len(channel_sweep) and matched == expected:
        v["verdict"] = "FULL_16_CHANNELS_PRESENT_SAMPLED_READ_OK"
    elif read_ok == len(channel_sweep) and matched < expected:
        v["verdict"] = "PARTIAL_TREE_SAMPLES_READ_OK_MATCHED_%d_OF_%d" % (matched, expected)
    elif read_ok > 0 and denied > 0:
        v["verdict"] = "MIXED_SOME_READABLE_SOME_DENIED_IN_SAMPLE"
    elif denied == len(channel_sweep):
        v["verdict"] = "MOUNTED_BUT_PERM_DENIED_ACROSS_SAMPLES"
    else:
        v["verdict"] = "AMBIGUOUS_SEE_PER_CHANNEL_DETAILS"
    return v


def main():
    receipt: dict = {
        "task": "NFS_read_capability_survey_owner_authorized_20260921",
        "captured_at_utc": _now(),
        "authorization": (
            "Owner GO this-session 2026-09-21T~13:55Z: 'NFS READ-CAPABILITY "
            "SURVEY. The owner supplied a new access path: NFS export at "
            "/mnt/nfs-share, expected to hold broadcast content organized "
            "by 16 RMS channels/stations.' R-91 hold unchanged. Ratchet "
            "5858 unchanged. Survey-only, no seal."
        ),
        "hygiene": {
            "read_only": True,
            "no_downloads": True,
            "no_writes": True,
            "one_byte_fallback_only_if_stat_insufficient": True,
            "bounded_enumeration": True,
            "existing_mount_never_modified": True,
        },
        "bounds": {
            "ls_max_lines": LS_MAX_LINES,
            "find_max_lines": FIND_MAX_LINES,
            "stat_max_lines": STAT_MAX_LINES,
            "channels_sampled_max": 2,
            "sample_depth_max": 3,
        },
        "reference_owner_provided_channel_map": [
            {"code": c, "name": n, "kind": k} for c, n, k in EXPECTED_CHANNELS
        ],
    }

    binds = rms_creds_loader.load()
    receipt["cred_shape"] = {"jump": binds.jump.describe()}

    # Open JUMP
    jump = paramiko.SSHClient()
    jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        t0 = time.monotonic()
        jump.connect(hostname=binds.jump.host, port=22,
                     username=binds.jump.user, password=binds.jump.password,
                     timeout=12, auth_timeout=12, banner_timeout=12,
                     allow_agent=False, look_for_keys=False)
        receipt["jump_open"] = {"ok": True,
                                "elapsed_s": round(time.monotonic() - t0, 3)}
        # Host key un-drift assertion (record only)
        hk = jump.get_transport().get_remote_server_key()
        import base64 as _b64
        receipt["jump_open"]["remote_host_key_type"] = hk.get_name()
        receipt["jump_open"]["remote_host_key_sha256_b64"] = _b64.b64encode(
            hashlib.sha256(hk.asbytes()).digest()
        ).decode("ascii").rstrip("=")
    except Exception as e:
        receipt["jump_open"] = {"ok": False,
                                "error_class": e.__class__.__name__,
                                "error_msg": str(e)[:400]}
        _emit(receipt); return

    # ---- Vantage identity + mount snapshot ---------------------------
    receipt["jump_identity"] = _who_am_i(jump)
    receipt["mount_snapshot"] = _mount_snapshot(jump)

    # Decide vantage: mounted vs need-to-probe
    ls_root = receipt["mount_snapshot"]["ls_mnt_nfs_share"]
    mount_grep = receipt["mount_snapshot"]["mount_grep_nfs"]
    ls_stdout = ls_root.get("stdout") or ""
    mount_grep_stdout = mount_grep.get("stdout") or ""

    already_mounted = ("nfs" in mount_grep_stdout.lower()
                       and "/mnt/nfs-share" in mount_grep_stdout)
    # Also: if `ls -la /mnt/nfs-share` returned real entries (not just "..")
    # even when mount grep didn't spot it explicitly, treat as mounted.
    has_real_entries = False
    for ln in ls_stdout.splitlines():
        s = ln.strip()
        if not s: continue
        # skip total/. and ..
        if s.startswith("total ") or s.endswith(" .") or s.endswith(" .."):
            continue
        # Real entry lines start with permissions block (drwxr-xr-x etc.)
        if re.match(r"^[dl\-][rwx\-]{9}", s):
            has_real_entries = True
            break
    mounted_effective = already_mounted or has_real_entries
    receipt["vantage_decision"] = {
        "already_mounted_via_mount_grep": already_mounted,
        "has_real_entries_via_ls": has_real_entries,
        "vantage_used": (
            "existing_mount_at_/mnt/nfs-share" if mounted_effective
            else "no_existing_mount_probe_via_showmount"
        ),
    }

    if mounted_effective:
        # Direct enumeration path
        mount_path = "/mnt/nfs-share"
        receipt["enumeration_top_level"] = _enumerate_top_level(jump, mount_path)
        ls_names_stdout = receipt["enumeration_top_level"]["ls_1_root"].get("stdout", "")
        top_names = _parse_ls_names(ls_names_stdout)
        receipt["enumeration_top_level"]["channel_reconciliation"] = _reconcile_channels(top_names)

        # Sample 2 channels: 1 TV (Ch1) + 1 Radio (Ch4).
        matched = receipt["enumeration_top_level"]["channel_reconciliation"]["matched"]
        by_code = {m["matched_to"]: m["observed"] for m in matched}

        sample_targets: list = []
        # TV pick
        tv_target = by_code.get(SAMPLE_TV_PRIMARY)
        if not tv_target:
            # Fallback: any TV kind
            for m in matched:
                if m["kind"] == "TV":
                    tv_target = m["observed"]; break
        if tv_target:
            sample_targets.append(("TV_sample_" + SAMPLE_TV_PRIMARY, tv_target))

        # Radio pick
        radio_target = by_code.get(SAMPLE_RADIO_PRIMARY)
        if not radio_target:
            for m in matched:
                if m["kind"] == "Radio":
                    radio_target = m["observed"]; break
        if radio_target:
            sample_targets.append(("Radio_sample_" + SAMPLE_RADIO_PRIMARY, radio_target))

        channel_sweep: dict = {}
        for label, ch_name in sample_targets:
            entry: dict = {"channel_selected_for_sample": ch_name}
            entry["structure_probe"] = _sample_channel(jump, mount_path, ch_name, label)
            entry["smallest_file_probe"] = _smallest_file_stat(jump, mount_path, ch_name)
            # If stat couldn't prove readability, invoke owner-authorized
            # 1-byte fallback on the SAME file (still no byte value banked).
            test_r_stdout = entry["smallest_file_probe"].get("test_r", {}).get("stdout", "")
            if ("NOT_READABLE" in test_r_stdout
                and entry["smallest_file_probe"].get("smallest_file")):
                path = entry["smallest_file_probe"]["smallest_file"]["path"]
                entry["one_byte_fallback"] = _one_byte_fallback(jump, path)
            channel_sweep[label] = entry
        receipt["channel_sweep"] = channel_sweep

        # Verdict
        receipt["verdict"] = _classify_verdict(
            receipt["enumeration_top_level"], channel_sweep,
        )

    else:
        # Discover path — showmount against candidates
        candidates = [("NAS", "10.10.55.55")]
        for c in binds.mysql_clusters:
            if c.host and c.host != "HOST":
                candidates.append(("mysql_" + (c.section or "?"), c.host))
        receipt["export_discovery"] = _showmount_probes(jump, candidates)
        # Per-server classification
        classifications = {}
        for k, res in receipt["export_discovery"].items():
            if k.startswith("showmount_e_"):
                classifications[k] = _classify_showmount(res)
        receipt["export_discovery_classifications"] = classifications

        # If ANY export listed successfully, we could optionally attempt a
        # probe mount — but per owner discipline, only do so if it's
        # non-invasive. Here we do NOT auto-mount; we report and stop,
        # letting the owner decide whether to proceed. This is the
        # "least-invasive path" instruction verbatim.
        exports_visible = any(v == "EXPORTS_LISTED" for v in classifications.values())
        receipt["exports_visible_via_showmount"] = exports_visible
        receipt["verdict"] = {
            "matched_channels": 0,
            "expected_channels": len(EXPECTED_CHANNELS),
            "sampled_channels": 0,
            "verdict": (
                "NO_EXISTING_NFS_MOUNT_ON_JUMP_AND_NO_AUTO_MOUNT_"
                "PERFORMED_(exports_visible={})".format(exports_visible)
            ),
        }

    # Teardown
    try: jump.close()
    except Exception: pass

    _emit(receipt)


def _emit(receipt: dict) -> None:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = RECEIPT_DIR / f"{stamp}_NFS_read_capability_survey_owner_authorized_20260921.json"
    p.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                 encoding="utf-8")
    print(f"receipt_path: {p}")


if __name__ == "__main__":
    main()
