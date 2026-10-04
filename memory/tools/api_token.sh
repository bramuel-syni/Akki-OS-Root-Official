#!/bin/bash
# usage: source /app/memory/tools/api_token.sh [email] [password]  → sets API and TOKEN
API=$(grep REACT_APP_BACKEND_URL /app/frontend/.env | cut -d= -f2)
EMAIL=${1:-demo.operator@demo.rms.example.com}
PASS=${2:-demo-operator-pw}
TOKEN=$(curl -s -X POST "$API/api/auth/login" -H "Content-Type: application/json" -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}" | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
export API TOKEN
