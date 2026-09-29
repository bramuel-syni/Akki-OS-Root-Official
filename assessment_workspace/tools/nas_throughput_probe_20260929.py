"""Read-only NAS throughput probe on the jump host. Prints timings/counts only; no filenames."""
import shlex, sys, time
sys.path.insert(0, '/app/backend/vendored/extraction_akki/backend')
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')
from services.census_autonomy.jump_dispatch import _connect_jump, _jump_config

PROBE = r'''
set -u
R=/mnt/nfs-share
echo NPROC=$(nproc) LOAD="$(cut -d' ' -f1-3 /proc/loadavg)"
echo FSTAB=$(grep -c nfs-share /etc/fstab 2>/dev/null) CREDFILE=$(grep -o 'credentials=[^ ,]*' /etc/fstab 2>/dev/null | wc -l)
D=$(ls -d $R/channel07/*/ 2>/dev/null | sed -n '100p')
echo DIR_INDEX=100
s=$(date +%s.%N); n=$(ls "$D" | wc -l); e=$(date +%s.%N); echo "LS_ONLY entries=$n sec=$(echo "$e-$s"|bc)"
s=$(date +%s.%N); n=$(ls -l "$D" | wc -l); e=$(date +%s.%N); echo "LS_STAT entries=$n sec=$(echo "$e-$s"|bc)"
s=$(date +%s.%N); n=$(find "$D" -type f -printf '%s\n' | wc -l); e=$(date +%s.%N); echo "FIND_PRINTF entries=$n sec=$(echo "$e-$s"|bc)"
D2=$(ls -d $R/channel07/*/ 2>/dev/null | sed -n '101p')
s=$(date +%s.%N); n=$(/opt/akki-census/bin/python - "$D2" <<'PY'
import os,sys,time
c=0
with os.scandir(sys.argv[1]) as it:
    for e in it:
        if e.is_file(follow_symlinks=False): e.stat(follow_symlinks=False); c+=1
print(c)
PY
); e=$(date +%s.%N); echo "PY_SCANDIR_STAT entries=$n sec=$(echo "$e-$s"|bc)"
D3=$(ls -d $R/channel07/*/ 2>/dev/null | sed -n '102p')
s=$(date +%s.%N); n=$(/opt/akki-census/bin/python - "$D3" <<'PY'
import os,sys
c=0
with os.scandir(sys.argv[1]) as it:
    for e in it:
        if e.is_file(follow_symlinks=False): c+=1
print(c)
PY
); e=$(date +%s.%N); echo "PY_SCANDIR_ONLY entries=$n sec=$(echo "$e-$s"|bc)"
D4=$(ls -d $R/channel07/*/ 2>/dev/null | sed -n '103p')
s=$(date +%s.%N); n=$(ls -l --time-style=+%s "$D4" | awk 'NR>1{s+=$5;c++}END{print c}'); e=$(date +%s.%N); echo "LS_L_AWK entries=$n sec=$(echo "$e-$s"|bc)"
echo CHANNEL01_SUBDIRS=$(ls $R/channel01 | wc -l)
D5=$(ls -d $R/channel01/*/ 2>/dev/null | sed -n '50p'); echo CHANNEL01_D50_ENTRIES=$(ls "$D5" | wc -l) SUBDIRS=$(find "$D5" -maxdepth 1 -type d | wc -l)
echo SMBCLIENT_VERSION=$(smbclient --version 2>/dev/null | head -1)
'''
client = _connect_jump(_jump_config(), 20)
_, out, err = client.exec_command('bash -c ' + shlex.quote(PROBE), timeout=170)
print(out.read().decode(errors='replace')); print('ERR:', err.read().decode(errors='replace')[-800:])
client.close()
