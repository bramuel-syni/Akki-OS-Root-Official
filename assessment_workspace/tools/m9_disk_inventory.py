"""Read-only training-asset inventory of the admitted GPU hosts (M9.1 readiness). Metadata only; no estate bytes cross."""
import json
import os
import sys

sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
sys.path.insert(0, '/app/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from services.training_runner.ssh_seam import execute_remote_command, list_hosts  # noqa: E402

COMMAND = r'''
echo "== host"; hostname; uptime
echo "== gpus"; nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader 2>&1 | head -4
echo "== disks"; df -h / /mnt/volume_dkgjrkx /mnt/akki-storage-3388s 2>&1 | tail -n +1
echo "== volume top"; du -sh /mnt/volume_dkgjrkx/* 2>/dev/null | sort -rh | head -20
echo "== volume depth2"; find /mnt/volume_dkgjrkx -maxdepth 2 -mindepth 1 -type d 2>/dev/null | head -60
echo "== hf cache"; for d in ~/.cache/huggingface/hub /mnt/volume_dkgjrkx/hf_cache /mnt/volume_dkgjrkx/*/hf* /mnt/volume_dkgjrkx/*/.cache/huggingface/hub; do [ -d "$d" ] && echo "-- $d" && ls "$d" 2>/dev/null | head -40 && du -sh "$d" 2>/dev/null; done
echo "== journal"; ls -la ~/akki_journal 2>&1 | head -40; find ~/akki_journal -maxdepth 2 -name "*.json" 2>/dev/null | wc -l
echo "== sealed runs"; find ~/akki_journal /mnt/volume_dkgjrkx -maxdepth 4 \( -name "seal*.json" -o -name "final_seal*.json" -o -name "run_certificate*.json" -o -name "heartbeat.json" \) 2>/dev/null | head -60
echo "== adapters"; find ~/akki_journal /mnt/volume_dkgjrkx -maxdepth 5 \( -name "adapter_model.safetensors" -o -name "adapter_config.json" -o -name "*.pt" -o -name "*.safetensors" \) 2>/dev/null | head -40
echo "== corpora"; find ~ /mnt/volume_dkgjrkx -maxdepth 4 \( -name "*.jsonl" -o -name "*.parquet" \) -size +1M 2>/dev/null | head -40
echo "== python"; for py in /mnt/volume_dkgjrkx/akki-lc/venv/bin/python python3; do echo "-- $py"; $py - <<'PY' 2>&1 | head -20
import importlib
for m in ("torch","transformers","peft","accelerate","opacus","speechbrain","datasets","bitsandbytes","vllm","trl","deepspeed","flash_attn","torchaudio","faster_whisper","evaluate","sentencepiece"):
    try:
        mod=importlib.import_module(m); print(m, getattr(mod,"__version__","?"))
    except Exception as e:
        print(m, "MISSING")
PY
done
echo "== procs"; ps -eo pid,etime,pcpu,pmem,args --sort=-pcpu 2>/dev/null | grep -i "python\|train" | grep -v grep | head -10
'''

out = {}
for host in list_hosts():
    result = execute_remote_command(host, COMMAND, purpose='m9_training_asset_inventory_readonly', timeout=240)
    out[host] = {'rc': result.rc, 'receipt': result.receipt_id, 'stdout': result.stdout_redacted, 'stderr': result.stderr_redacted}
    print(f'##### {host} rc={result.rc} receipt={result.receipt_id}')
    print(result.stdout_redacted[-12000:])
    if result.stderr_redacted.strip():
        print('STDERR', result.stderr_redacted[-1500:])
target = os.environ.get('M9_INVENTORY_OUT', '/app/assessment_workspace/notes/m9_execution/HOST_TRAINING_ASSET_INVENTORY_20260929.json')
os.makedirs(os.path.dirname(target), exist_ok=True)
json.dump(out, open(target, 'w'), indent=1)
print('written', target)
