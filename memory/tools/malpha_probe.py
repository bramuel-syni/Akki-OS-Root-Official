"""Read-only probe of both GPU hosts for Mα: devices, corpus roots, installed packages, running processes."""
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
os.chdir('/app/backend/vendored/extraction_akki/backend')
from services.training_runner.ssh_seam import execute_remote_command  # noqa: E402

CMD = sys.argv[1] if len(sys.argv) > 1 else r'''hostname; nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader
echo __LC__; ls /mnt/volume_dkgjrkx/akki-lc | head -40
echo __LC_CORPUS__; ls /mnt/volume_dkgjrkx/akki-lc/corpus 2>/dev/null | head -30; du -sh /mnt/volume_dkgjrkx/akki-lc/corpus 2>/dev/null
echo __M9__; ls /mnt/volume_dkgjrkx/akki-m9; ls /mnt/volume_dkgjrkx/akki-m9/jobs 2>/dev/null | wc -l
echo __PIP__; /mnt/volume_dkgjrkx/akki-lc/venv/bin/pip list 2>/dev/null | grep -iE "^(torch|torchaudio|transformers|peft|accelerate|numpy|scipy|soundfile|librosa|faster|whisper|ctranslate|encodec|vocos|snac|descript|audiocraft|datasets|sentencepiece|tokenizers|opacus|bitsandbytes|vllm|flash|xformers|einops|safetensors|huggingface|jiwer|pyannote|speechbrain|nemo|xcodec|wavtokenizer|TTS|coqui|f5|phonemizer|espeak|g2p|unidecode|num2words|onnx|scikit|pandas|pyarrow) "
echo __DF__; df -h /mnt/volume_dkgjrkx | tail -1; free -g | head -2
echo __PS__; ps -eo pid,etime,pcpu,pmem,args | grep -E "python|vllm" | grep -v grep | cut -c1-160 | head -20
echo __HF__; ls /mnt/volume_dkgjrkx/akki-m9/hf_cache/hub 2>/dev/null | head -30; ls /mnt/volume_dkgjrkx/akki-lc/hf_cache/hub 2>/dev/null | head -30
'''
hosts = sys.argv[2].split(',') if len(sys.argv) > 2 else ('akki-vm', 'akki-vm-ii')
for h in hosts:
    r = execute_remote_command(h, CMD, purpose='malpha_probe', timeout=55)
    print('=====', h, 'rc', r.rc)
    print(r.stdout_redacted[:12000])
    if r.stderr_redacted.strip():
        print('ERR', r.stderr_redacted[:800])
