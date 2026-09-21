"""tools/digicow_cifs_deeper_20260921.py

Follow-up CIFS-only search for 'digicow'. The first pass used a pipeline
`find ... | head` which masked find's exit code, so we couldn't tell
whether find completed or hit the outer 25s timeout. This pass:
    - preserves find's rc via `set -o pipefail` OR just no pipeline
    - limits type=d (directories only — a 'digicow' channel/folder would
      manifest as a directory name)
    - extends the timeout to 90s
    - runs depth 3 first; if that completes, tries depth 4 with tighter
      time budget
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

import rms_creds_loader_v2 as L2  # noqa: E402
import paramiko  # noqa: E402

RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")


def _now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ssh_exec(client, cmd, timeout=100.0):
    t0 = time.monotonic()
    try:
        stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
        out = stdout.read(65536).decode("utf-8", errors="replace")
        err = stderr.read(8192).decode("utf-8", errors="replace")
        rc = stdout.channel.recv_exit_status()
        return {"cmd": cmd if len(cmd) <= 240 else cmd[:240]+"...",
                "rc": rc, "stdout": out[:16384],
                "stderr": err[:2048],
                "elapsed_s": round(time.monotonic() - t0, 3)}
    except Exception as e:
        return {"cmd": cmd[:240], "rc": None,
                "error_class": e.__class__.__name__,
                "error_msg": str(e)[:400],
                "elapsed_s": round(time.monotonic() - t0, 3)}


def main():
    receipt = {
        "task": "DIGICOW_cifs_deeper_search_20260921",
        "captured_at_utc": _now(),
        "predecessor": ("phase0/connectivity_receipts/20260921T145515Z_"
                        "DIGICOW_targeted_read_check_owner_authorized_"
                        "20260921.json"),
        "reason": (
            "The prior CIFS search used `find ... | head` and returned "
            "rc=0 in 26.3s — pipeline rc masking made it ambiguous "
            "whether find completed or timed out on the 47 TiB tree. "
            "This pass preserves find's rc + targets directory names "
            "only + extends the timeout."
        ),
        "hygiene": {"read_only": True, "no_downloads": True,
                    "structural_names_ok_to_emit": True},
    }

    binds = L2.load()
    jump = paramiko.SSHClient()
    jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    jump.connect(hostname=binds.jump.host, port=22,
                 username=binds.jump.user, password=binds.jump.password,
                 timeout=12, auth_timeout=12, banner_timeout=12,
                 allow_agent=False, look_for_keys=False)

    # Sanity: still mounted?
    receipt["mount_now"] = _ssh_exec(
        jump, "mount 2>&1 | grep -iE '(cifs|nfs)' | head -3", timeout=10)

    # Pass A · directory names ONLY, depth 3, TRUE find rc.
    # Using `bash -c "set -o pipefail; ..."` to preserve find's rc into
    # the pipeline result. Also writing find's output to a temp on JUMP
    # so we can inspect stderr separately.
    receipt["pass_A_dirnames_depth3"] = _ssh_exec(
        jump,
        "bash -c 'set -o pipefail; "
        "timeout 90 find /mnt/nfs-share -maxdepth 3 -type d -iname \"*digicow*\" "
        "2>/tmp/digicow_stderr.log ; echo _RC=$?' 2>&1",
        timeout=110,
    )
    receipt["pass_A_stderr_sample"] = _ssh_exec(
        jump, "tail -20 /tmp/digicow_stderr.log 2>&1; rm -f /tmp/digicow_stderr.log", timeout=10)

    # Pass B · CASE-INSENSITIVE, non-type-restricted, depth 3, find rc.
    receipt["pass_B_any_type_depth3"] = _ssh_exec(
        jump,
        "bash -c 'timeout 90 find /mnt/nfs-share -maxdepth 3 -iname \"*digicow*\" "
        "2>/dev/null ; echo _RC=$?' 2>&1",
        timeout=110,
    )

    # Pass C · The 16 top-level channel dirs — count subdirs at depth 2
    # to gauge tree width (so we know whether Pass A's 90s window was
    # enough).
    receipt["pass_C_tree_width"] = _ssh_exec(
        jump,
        "bash -c 'for i in $(seq -w 1 16); do "
        "d=/mnt/nfs-share/channel$i; "
        "if [ -d $d ]; then "
        "  n=$(timeout 15 find $d -maxdepth 1 -mindepth 1 -type d 2>/dev/null | wc -l); "
        "  echo channel$i depth1_dirs=$n; "
        "fi; done'",
        timeout=200,
    )

    # Pass D · Search inside `/mnt/nfs-share/channelXX/*/` at depth 2
    # explicitly (sometimes CIFS list caches differ per subtree).
    receipt["pass_D_per_channel_depth2"] = _ssh_exec(
        jump,
        "bash -c 'timeout 90 find /mnt/nfs-share -maxdepth 4 -type d -iname \"*digicow*\" "
        "2>/dev/null ; echo _RC=$?' 2>&1",
        timeout=110,
    )

    # ---- Verdict per pass -------------------------------------------
    def _parse_rc_and_hits(r):
        stdout = r.get("stdout") or ""
        m = re.search(r"_RC=(\d+)", stdout)
        rc = int(m.group(1)) if m else None
        hits = [ln.strip() for ln in stdout.splitlines()
                if ln.strip() and not ln.strip().startswith("_RC=")]
        return {"find_rc": rc,
                "find_rc_hint": {124: "TIMEOUT", 0: "COMPLETED_NO_MATCHES_OR_MATCHES",
                                 141: "SIGPIPE"}.get(rc, f"OTHER"),
                "hit_count": len(hits),
                "hits": hits[:50],
                "elapsed_s": r.get("elapsed_s")}
    receipt["verdict_per_pass"] = {
        "pass_A_dirnames_depth3": _parse_rc_and_hits(receipt["pass_A_dirnames_depth3"]),
        "pass_B_any_type_depth3": _parse_rc_and_hits(receipt["pass_B_any_type_depth3"]),
        "pass_D_dirnames_depth4": _parse_rc_and_hits(receipt["pass_D_per_channel_depth2"]),
    }

    # Overall
    total_hits = sum(v["hit_count"] for v in receipt["verdict_per_pass"].values())
    all_completed = all(
        v["find_rc"] == 0 for v in receipt["verdict_per_pass"].values()
        if v["find_rc"] is not None
    )
    any_timeout = any(
        v["find_rc"] == 124 for v in receipt["verdict_per_pass"].values()
    )
    receipt["overall"] = {
        "total_hits_across_passes": total_hits,
        "all_completed_cleanly": all_completed,
        "any_pass_timed_out": any_timeout,
        "conclusion": (
            "DIGICOW_NOT_FOUND_IN_CIFS_MOUNT_TO_DEPTH_4"
            if total_hits == 0 and all_completed else
            "DIGICOW_NOT_FOUND_BUT_SOME_PASS_INCOMPLETE"
            if total_hits == 0 and any_timeout else
            "DIGICOW_FOUND"
        ),
    }

    try: jump.close()
    except Exception: pass

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = RECEIPT_DIR / f"{stamp}_DIGICOW_cifs_deeper_search_20260921.json"
    p.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                 encoding="utf-8")
    print(f"receipt_path: {p}")


if __name__ == "__main__":
    main()
