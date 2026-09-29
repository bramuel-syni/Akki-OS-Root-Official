#!/bin/bash
# usage: source /tmp/akki_env.sh; login digicow|rms|rmsadmin|analyst  → sets TOKEN, H, J, API
API=$(grep REACT_APP_BACKEND_URL /app/frontend/.env | cut -d= -f2)
J='Content-Type: application/json'
login() {
  case "$1" in
    digicow) E=demo.operator@demo.digicow.example.com; P=demo-digicow-operator-pw;;
    rms) E=demo.operator@demo.rms.example.com; P=demo-operator-pw;;
    rmsadmin) E=demo.master_admin@demo.rms.example.com; P=demo-master-admin-pw;;
    analyst) E=demo.analyst@demo.rms.example.com; P=demo-analyst-pw;;
  esac
  TOKEN=$(curl -s -X POST "$API/api/auth/login" -H "$J" -d "{\"email\":\"$E\",\"password\":\"$P\"}" | python3 -c "import sys,json;d=json.load(sys.stdin);print(d.get('access_token') or d.get('token'))")
  H="Authorization: Bearer $TOKEN"
}
