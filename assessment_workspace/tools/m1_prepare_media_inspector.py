"""Prepare the media inspector on the existing jump runtime, never on NAS."""
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')
sys.path.insert(0,'/app/backend/vendored/extraction_akki/backend')
from services.census_autonomy.jump_dispatch import _connect_jump,_jump_config

client=_connect_jump(_jump_config(),15)
try:
    _,out,err=client.exec_command("sudo -n sh -c 'apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg'",timeout=240)
    out.read(); errors=err.read(); code=out.channel.recv_exit_status()
    result={'runtime_id':'non_gpu_jump','tool':'ffprobe','exit_code':code,'status':'installed' if code==0 else 'blocked'}
    Path('/app/assessment_workspace/notes/m1_execution/MEDIA_PREPARATION.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result))
finally:
    client.close()