"""M2-T1 Watch Commission-gate live drill. Prints observations for report."""
import os, time, json, sys, requests

BASE = os.environ.get("REACT_APP_BACKEND_URL", "https://pensive-goodall-6.preview.emergentagent.com").rstrip("/")
ANALYST = ("demo.analyst@demo.rms.example.com", "demo-analyst-pw")
OPERATOR = ("demo.operator@demo.rms.example.com", "demo-operator-pw")

def login(email, pw):
    r = requests.post(f"{BASE}/api/auth/login", json={"email": email, "password": pw}, timeout=20)
    print(f"LOGIN {email} -> {r.status_code}")
    r.raise_for_status()
    return r.json()["access_token"]

def h(tok): return {"Authorization": f"Bearer {tok}"}

report = {"steps": [], "verdict_ids": [], "action_ids": [], "timestamps": []}

analyst_tok = login(*ANALYST)
operator_tok = login(*OPERATOR)

# Step A: 3 back-to-back POSTs -> expect 3x 403
print("\n=== Step A: 3 refusals ===")
step_a = []
for i in range(3):
    r = requests.post(f"{BASE}/api/portal/census/language-cognition/jobs",
                      json={"phase": "nope"}, headers=h(analyst_tok), timeout=20)
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print(f"  A{i+1}: {r.status_code} {r.text[:180]}")
    step_a.append({"status": r.status_code, "ts": ts, "body_snippet": r.text[:200]})
    time.sleep(1)
report["steps"].append({"step": "A", "results": step_a})

# Step B: within 30s of the 3rd
print("\n=== Step B: throttle -> 429 ===")
r = requests.post(f"{BASE}/api/portal/census/language-cognition/jobs",
                  json={"phase": "nope"}, headers=h(analyst_tok), timeout=20)
ts_b = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
body = r.text
print(f"  B: {r.status_code} {body[:300]}")
action_id = None
if r.status_code == 429:
    try:
        detail = r.json().get("detail","")
        if isinstance(detail, dict):
            detail_str = json.dumps(detail)
        else:
            detail_str = str(detail)
        import re
        m = re.search(r"ma_gate_[a-zA-Z0-9_\-]+", detail_str)
        if m: action_id = m.group(0)
        friction_ok = "friction" in detail_str.lower()
        print(f"  friction-in-detail: {friction_ok}, action_id: {action_id}")
    except Exception as e:
        print(f"  parse err: {e}")
report["steps"].append({"step": "B", "status": r.status_code, "ts": ts_b, "action_id": action_id, "body": body[:400]})
if action_id: report["action_ids"].append(action_id)

# Operator watch/state after B
print("\n=== Post-B: operator GET watch/state ===")
r = requests.get(f"{BASE}/api/portal/watch/state", headers=h(operator_tok), timeout=20)
print(f"  status: {r.status_code}")
state = r.json() if r.status_code == 200 else {}
counts = state.get("counts", {})
pb = state.get("protected_boundaries", [])
records = state.get("records", [])
print(f"  counts: {counts}")
print(f"  protected_boundaries: {pb}")
print(f"  record kinds: {[(x.get('kind'), x.get('title'), x.get('detector'), x.get('boundary'), x.get('state'), x.get('effect_verified')) for x in records][:10]}")

verdict_row = next((x for x in records if x.get("kind")=="verdict" and x.get("detector")=="fast_violation" and x.get("boundary")=="language_cognition.commission"), None)
action_row = next((x for x in records if x.get("kind")=="action" and x.get("title")=="shape" and x.get("state")=="In effect"), None)
raw = json.dumps(state)
password_leak = "password" in raw.lower() or "secret" in raw.lower()
print(f"  verdict_row present: {bool(verdict_row)}; shape action In effect verified: {action_row}; password leak: {password_leak}")

report["steps"].append({
    "step": "post_B_operator_watch_state",
    "counts": counts,
    "protected_boundaries": pb,
    "verdict_row": verdict_row,
    "shape_action_row": action_row,
    "password_or_secret_in_body": password_leak,
    "num_records": len(records),
})
if verdict_row: report["verdict_ids"].append(verdict_row.get("id"))
if action_row: report["action_ids"].append(action_row.get("id"))

# Step C: slow-play -> contain. Need 8 refusals in 24h. We have (existing 1) + 3 (step A) = 4.
# Need 4 more, spaced >=32s. Between each, must be 403 (not 429). Wait 32s after step B first.
print("\n=== Step C: slow-play, spaced >=32s until 8th refusal + contain ===")
time.sleep(32)
step_c = []
contained_at = None
for i in range(6):  # allow a couple extra attempts
    r = requests.post(f"{BASE}/api/portal/census/language-cognition/jobs",
                      json={"phase": "nope"}, headers=h(analyst_tok), timeout=20)
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    print(f"  C{i+1}: {r.status_code} {r.text[:220]}")
    step_c.append({"status": r.status_code, "ts": ts, "body": r.text[:250]})
    if r.status_code == 409:
        contained_at = ts
        break
    time.sleep(33)
report["steps"].append({"step": "C", "results": step_c, "contained_at": contained_at})

# One more post to confirm 409 contain
print("\n=== Post-C: next attempt must be 409 ===")
r = requests.post(f"{BASE}/api/portal/census/language-cognition/jobs",
                  json={"phase": "nope"}, headers=h(analyst_tok), timeout=20)
body = r.text
print(f"  status: {r.status_code} body: {body[:300]}")
contain_ok = r.status_code == 409 and "suspended by the Watch until" in body and "unaffected" in body
report["steps"].append({"step": "post_C_contain_check", "status": r.status_code, "body": body[:400], "contain_ok": contain_ok})

# reads unaffected for analyst
r1 = requests.get(f"{BASE}/api/portal/census/language-cognition/jobs", headers=h(analyst_tok), timeout=20)
r2 = requests.get(f"{BASE}/api/portal/census/overview", headers=h(analyst_tok), timeout=20)
print(f"  analyst GET jobs: {r1.status_code}; GET overview: {r2.status_code}")
report["steps"].append({"step": "analyst_reads_after_contain", "jobs_status": r1.status_code, "overview_status": r2.status_code})

# operator watch after C
print("\n=== Post-C: operator watch/state ===")
r = requests.get(f"{BASE}/api/portal/watch/state", headers=h(operator_tok), timeout=20)
state2 = r.json() if r.status_code == 200 else {}
counts2 = state2.get("counts", {})
recs2 = state2.get("records", [])
contain_row = next((x for x in recs2 if x.get("kind")=="action" and x.get("title")=="contain" and x.get("state")=="In effect"), None)
print(f"  counts: {counts2}")
print(f"  contain action row: {contain_row}")
report["steps"].append({"step": "post_C_operator_watch_state", "counts": counts2, "contain_action_row": contain_row})
if contain_row: report["action_ids"].append(contain_row.get("id"))

# Legacy watch/state
print("\n=== Legacy /api/watch/state ===")
r = requests.get(f"{BASE}/api/watch/state", timeout=20)
print(f"  status: {r.status_code}")
legacy = r.json() if r.status_code == 200 else {}
entries = (legacy.get("verdicts") or {}).get("entries") or []
gate_verdicts = [e for e in entries if str(e.get("id","")).startswith("mv_gate_")]
externally = [e for e in gate_verdicts if e.get("verdict_class")=="externally_steerable"]
sever_present = any(e.get("action_class")=="sever" for e in entries)
print(f"  gate verdicts: {len(gate_verdicts)}; externally_steerable: {len(externally)}; any sever: {sever_present}")
report["steps"].append({"step": "legacy_watch_state", "status": r.status_code,
                        "gate_verdict_count": len(gate_verdicts),
                        "externally_steerable_count": len(externally),
                        "sever_present": sever_present})

# M2-T2: operator benign reads
print("\n=== M2-T2: operator benign reads ===")
before = counts2.get("gate_crossings", 0)
r_ov = requests.get(f"{BASE}/api/portal/census/overview", headers=h(operator_tok), timeout=20)
r_lj = requests.get(f"{BASE}/api/portal/census/language-cognition/jobs", headers=h(operator_tok), timeout=20)
r_lj1 = requests.get(f"{BASE}/api/portal/census/language-cognition/jobs/lcj-f96c86a16312", headers=h(operator_tok), timeout=20)
print(f"  overview:{r_ov.status_code} jobs:{r_lj.status_code} one:{r_lj1.status_code}")
r_state3 = requests.get(f"{BASE}/api/portal/watch/state", headers=h(operator_tok), timeout=20)
after = r_state3.json().get("counts",{}).get("gate_crossings", 0) if r_state3.status_code==200 else -1
print(f"  crossings before:{before} after reads:{after}")
report["steps"].append({"step": "operator_benign_reads",
                        "overview": r_ov.status_code, "jobs": r_lj.status_code, "one_job": r_lj1.status_code,
                        "crossings_before": before, "crossings_after": after})

# Exactly one operator POST -> 422 as refused crossing
print("\n=== One operator POST {phase:nope} -> 422 refusal ===")
r_op_post = requests.post(f"{BASE}/api/portal/census/language-cognition/jobs",
                          json={"phase": "nope"}, headers=h(operator_tok), timeout=20)
print(f"  operator POST: {r_op_post.status_code} {r_op_post.text[:200]}")
r_state4 = requests.get(f"{BASE}/api/portal/watch/state", headers=h(operator_tok), timeout=20)
counts_final = r_state4.json().get("counts",{}) if r_state4.status_code==200 else {}
print(f"  final counts: {counts_final}")
report["steps"].append({"step": "operator_one_post_and_final_counts",
                        "operator_post_status": r_op_post.status_code,
                        "final_counts": counts_final})

# dump raw records for evidence
report["final_state_records_summary"] = [
    {"kind": x.get("kind"), "id": x.get("id"), "title": x.get("title"),
     "detector": x.get("detector"), "boundary": x.get("boundary"),
     "state": x.get("state"), "effect_verified": x.get("effect_verified"),
     "effects": x.get("effects"), "actor": x.get("actor")}
    for x in (r_state4.json().get("records", []) if r_state4.status_code==200 else [])
][:40]

with open("/app/test_reports/iteration_62_drill_output.json", "w") as f:
    json.dump(report, f, indent=2, default=str)
print("\nDONE. Wrote /app/test_reports/iteration_62_drill_output.json")
