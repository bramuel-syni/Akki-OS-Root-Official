#!/bin/bash
# M7 · W-M7-UTILIZATION-72H · nvidia-smi telemetry sampler.
# Runs on GPU host under ~/akki_util_72h/sampler.sh (staged via base64 + ssh_seam).
# Every 5 minutes: nvidia-smi query → append one JSONL row per GPU to
# ~/akki_util_72h/telemetry.jsonl.  72-hour wall-clock; exit 0 at end.
# On SIGTERM: exit cleanly.
set -eu

OUT_DIR="$HOME/akki_util_72h"
JSONL="$OUT_DIR/telemetry.jsonl"
STATUS="$OUT_DIR/sampler_status.json"
mkdir -p "$OUT_DIR"

WALL_CLOCK_S=$((72*3600))
SAMPLE_INTERVAL_S=300  # 5 minutes

START_TS=$(date -u +%s)
HOSTNAME=$(hostname)

trap 'exit 0' TERM INT

cat > "$STATUS" <<EOF
{"state":"running","start_utc":"$(date -u +%Y-%m-%dT%H:%M:%SZ)","host":"$HOSTNAME","pid":$$,"sample_interval_s":$SAMPLE_INTERVAL_S,"wall_clock_s":$WALL_CLOCK_S}
EOF

while :; do
  NOW_TS=$(date -u +%s)
  ELAPSED=$((NOW_TS - START_TS))
  if [ $ELAPSED -ge $WALL_CLOCK_S ]; then
    break
  fi
  TS_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  # nvidia-smi: index,name,util.gpu,util.mem,mem.used,power.draw,temperature.gpu
  nvidia-smi --query-gpu=index,name,utilization.gpu,utilization.memory,memory.used,memory.total,power.draw,temperature.gpu,clocks.sm,clocks.mem \
             --format=csv,noheader,nounits \
    | while IFS=',' read -r idx name util_gpu util_mem mem_used mem_total power temp clk_sm clk_mem; do
        # Trim whitespace
        idx=$(echo "$idx" | xargs); name=$(echo "$name" | xargs)
        util_gpu=$(echo "$util_gpu" | xargs); util_mem=$(echo "$util_mem" | xargs)
        mem_used=$(echo "$mem_used" | xargs); mem_total=$(echo "$mem_total" | xargs)
        power=$(echo "$power" | xargs); temp=$(echo "$temp" | xargs)
        clk_sm=$(echo "$clk_sm" | xargs); clk_mem=$(echo "$clk_mem" | xargs)
        # Emit one JSONL row per GPU
        printf '{"ts_utc":"%s","host":"%s","gpu_index":%s,"gpu_name":"%s","utilization_gpu_pct":%s,"utilization_mem_pct":%s,"memory_used_mib":%s,"memory_total_mib":%s,"power_w":%s,"temperature_c":%s,"clock_sm_mhz":%s,"clock_mem_mhz":%s,"elapsed_s":%s}\n' \
          "$TS_UTC" "$HOSTNAME" "$idx" "$name" "$util_gpu" "$util_mem" "$mem_used" "$mem_total" "$power" "$temp" "$clk_sm" "$clk_mem" "$ELAPSED" \
          >> "$JSONL"
      done
  sleep $SAMPLE_INTERVAL_S
done

cat > "$STATUS" <<EOF
{"state":"finished","start_utc":"$(date -u -d @$START_TS +%Y-%m-%dT%H:%M:%SZ)","end_utc":"$(date -u +%Y-%m-%dT%H:%M:%SZ)","host":"$HOSTNAME","pid":$$}
EOF
