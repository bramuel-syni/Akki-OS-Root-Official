#!/usr/bin/env bash
# Waits for the in-flight NAS content pass to bank its receipt, restarts the census scheduler (new env: CENSUS_SAMPLE_STRATA_CAP),
# then commissions the OBS content_sample chains again so the readable buckets take the whole sample budget (owner: focus on what can be read).
set -u
STATE=/app/assessment_workspace/phase0/census_autonomy_state
WAIT_RUN="${1:-cr-061e8ff5e06f}"
DEADLINE_EPOCH="${2:-1790991768}"
log(){ echo "$(date -u +%FT%TZ) $*"; }
log "waiting for receipt of $WAIT_RUN (deadline $(date -u -d @$DEADLINE_EPOCH +%T))"
while ! ls "$STATE"/results/*_"$WAIT_RUN"_result.json >/dev/null 2>&1; do
  if [ "$(date +%s)" -gt $((DEADLINE_EPOCH + 180)) ]; then log "deadline passed without receipt; proceeding"; break; fi
  sleep 20
done
log "restarting census_scheduler"
sudo supervisorctl restart census_scheduler >/dev/null
sleep 15
API_URL=$(grep REACT_APP_BACKEND_URL /app/frontend/.env | cut -d '=' -f2)
TOKEN=$(curl -s -X POST "$API_URL/api/auth/login" -H "Content-Type: application/json" -d '{"email":"demo.operator@demo.rms.example.com","password":"demo-operator-pw"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
DAY=$(date -u +%Y%m%d)
for spec in "cr-bbf71c8d905a:akki-vm:obs-a" "cr-68be8ecf670a:akki-vm-ii:obs-b"; do
  IFS=: read -r SRC WORKER NAME <<<"$spec"
  REFS=$(python3 -c "import json;print(json.dumps(json.load(open('$STATE/dispatch/$SRC.json'))['source_refs']))")
  BODY=$(python3 -c "import json,sys;print(json.dumps({'source_ids':['rms_obs'],'worker_id':'$WORKER','measurement':'content_sample','idempotency_key':'estate-content-sample-$NAME-$DAY-readable','source_refs':json.loads(sys.argv[1])}))" "$REFS")
  log "commissioning $NAME on $WORKER"
  curl -s -X POST "$API_URL/api/portal/census/run" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "$BODY" | head -c 600; echo
done
log "done"
