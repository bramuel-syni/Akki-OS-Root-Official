"""NAS content census (CENSUS-3-E) via existing CIFS mount on JUMP.
Metadata-only, bounded: per-channel day-dir count + date range + one sampled day
(file count + bytes). No downloads. Writes receipt + prints summary."""
from __future__ import annotations
import paramiko
import base64
import json
import datetime as dt
import pathlib

JUMP = {"host": "159.138.173.250", "port": 22, "user": "root", "password": "76Nkr9P4Jv77"}
SEC = [JUMP["password"]]
TS = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def red(t):
    for s in SEC:
        if s and t:
            t = t.replace(s, "********")
    return t


REMOTE = r"""
cd /mnt/nfs-share || exit 1
DF=$(df -B1 /mnt/nfs-share 2>/dev/null | tail -1)
echo "DF|$DF"
for ch in */; do
  ch=${ch%/}
  days=$(ls -1 "$ch" 2>/dev/null | grep -E '^[0-9]{4}_[0-9]{2}_[0-9]{2}$' | sort)
  n=$(printf '%s\n' "$days" | grep -c .)
  mn=$(printf '%s\n' "$days" | head -1)
  mx=$(printf '%s\n' "$days" | tail -1)
  nf=0; by=0; ext=""
  if [ -n "$mx" ]; then
    nf=$(ls -1 "$ch/$mx" 2>/dev/null | grep -c '\.mp4$')
    by=$(timeout 40 du -sb "$ch/$mx" 2>/dev/null | cut -f1)
    ext=$(ls -1 "$ch/$mx" 2>/dev/null | sed -n 's/.*\.//p' | sort | uniq -c | sort -rn | head -4 | tr '\n' ',')
  fi
  echo "CH|$ch|$n|$mn|$mx|$nf|$by|$ext"
done
"""

cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(JUMP["host"], JUMP["port"], username=JUMP["user"], password=JUMP["password"],
            timeout=12, look_for_keys=False, allow_agent=False, banner_timeout=12)
b64 = base64.b64encode(REMOTE.encode()).decode()
_i, o, e = cli.exec_command(f"echo {b64} | base64 -d | bash", timeout=180)
out = red(o.read().decode("utf-8", "replace"))
err = red(e.read().decode("utf-8", "replace"))
cli.close()

channels = []
df = None
for line in out.splitlines():
    if line.startswith("DF|"):
        df = line[3:].strip()
    elif line.startswith("CH|"):
        p = (line.split("|") + [""] * 8)[:8]
        _, ch, n, mn, mx, nf, by, ext = p
        channels.append({
            "channel": ch, "day_dir_count": int(n or 0),
            "date_min": mn, "date_max": mx,
            "sampled_day": mx, "sampled_day_mp4_count": int(nf or 0),
            "sampled_day_bytes": int(by or 0),
            "sampled_day_ext_hist": ext.strip(","),
        })

# aggregates
total_days = sum(c["day_dir_count"] for c in channels)
dmins = [c["date_min"] for c in channels if c["date_min"]]
dmaxs = [c["date_max"] for c in channels if c["date_max"]]
est_total_bytes = sum(c["day_dir_count"] * c["sampled_day_bytes"] for c in channels)

manifest = {
    "receipt_kind": "NAS_CONTENT_CENSUS",
    "wave_id": "CENSUS-3-E",
    "at_utc": TS,
    "access_path": "existing CIFS mount on JUMP bastion · //10.10.55.55/OFFAIRRECS/Record -> /mnt/nfs-share (username=bramuel)",
    "df_raw": df,
    "content_kind": "off-air broadcast recording · 16 channels · YYYY_MM_DD day folders · 5-minute .mp4 segments (channelNN_YYYY_MM_DD_HH_MM_SS.mp4)",
    "channels": channels,
    "rollup": {
        "channel_count": len(channels),
        "total_day_dirs": total_days,
        "date_range_min": min(dmins) if dmins else None,
        "date_range_max": max(dmaxs) if dmaxs else None,
        "estimated_total_bytes_from_daily_sample": est_total_bytes,
        "estimated_total_tb_from_daily_sample": round(est_total_bytes / (1024**4), 2),
        "authoritative_used_from_df": df,
    },
    "discipline": "metadata-only · no file bytes downloaded · bounded (one sampled day per channel for size; day-dir counts + date ranges measured fully)",
    "honest_gap": "Per-channel total bytes are ESTIMATES (day_dir_count x one-sampled-day size). df 'Used' is the authoritative share total. Full per-file du over 44TB deferred (bounded run).",
}

out_dir = pathlib.Path("/app/assessment_workspace/phase0/census_v3/nas")
out_dir.mkdir(parents=True, exist_ok=True)
recp = out_dir / f"{TS}_CENSUS3E_NAS_content.json"
recp.write_text(json.dumps(manifest, indent=2))

print("== NAS CONTENT CENSUS (CENSUS-3-E) ==")
print("df:", df)
print(f"channels: {len(channels)} · total day-dirs: {total_days} · "
      f"date range: {manifest['rollup']['date_range_min']} .. {manifest['rollup']['date_range_max']}")
print(f"estimated total (daily-sample extrapolation): {manifest['rollup']['estimated_total_tb_from_daily_sample']} TB "
      f"(authoritative df Used is the real figure)")
print("\nper channel:")
for c in channels:
    gb = round(c["sampled_day_bytes"] / (1024**3), 2)
    print(f"  {c['channel']:10s} days={c['day_dir_count']:4d}  range={c['date_min']}..{c['date_max']}  "
          f"sample[{c['sampled_day']}]={c['sampled_day_mp4_count']} mp4 / {gb} GB")
print("\nreceipt:", recp)
if err.strip():
    print("stderr:", err.strip()[:300])
