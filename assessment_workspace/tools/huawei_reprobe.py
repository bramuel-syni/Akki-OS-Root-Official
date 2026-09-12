"""Post-whitelist reachability sweep — read-only.
Retest previously-blocked public MySQL endpoints across:
 (a) the 2 SG-blocked hosts from db_credentials.csv (203.123.86.10, 159.138.164.93)
 (b) the 5 SG-blocked af-south-1 RDS EIPs from the AK/SK RDS inventory
 (c) sanity: the 2 previously-reachable hosts (should still be up)
For each: TCP+handshake, then attempt auth ONLY with the bramuel credential (from db_credentials.csv).
"""
import csv, socket, time, json, hashlib
from datetime import datetime, timezone

CRED_DB = "/app/backend/estate_keys/data_sources/db_credentials.csv"

with open(CRED_DB) as f:
    rows = list(csv.reader(f))
BRAM_USER, BRAM_PW = None, None
for r in rows:
    if len(r) >= 4 and r[1] == "110.238.76.159":  # reference row with creds
        BRAM_USER, BRAM_PW = r[2], r[3]
        break

TARGETS = [
    # (host, port, prior_state, name, source, try_bramuel_creds)
    # DB creds CSV — bramuel creds are the natural attempt
    ("203.123.86.10",  3306, "was TCP-blocked",       "VIUSASA host",                     "db_creds_csv",   True),
    ("159.138.164.93", 3306, "was TCP-blocked",       "MICROSERVICES host",               "db_creds_csv",   True),
    ("110.238.76.159", 3306, "was reachable+authed",  "USSD host (sanity)",               "db_creds_csv",   True),
    # AK/SK RDS EIPs
    ("159.138.162.220",3306, "was reachable (auth)",  "RDS-INTERACTIONS",                 "aksk_rds",       True),
    ("159.138.162.146",3306, "was reachable (auth)",  "Weego_and_marketing-analytics",    "aksk_rds",       True),
    ("203.123.83.144", 3306, "was TCP-blocked",       "rds-shikisha",                     "aksk_rds",       True),
    ("110.238.77.61",  3306, "was TCP-blocked",       "election-prod-db2",                "aksk_rds",       True),
    ("110.238.75.83",  3306, "was TCP-blocked",       "visitors-database-cluster",        "aksk_rds",       True),
    ("159.138.175.179",3306, "was TCP-blocked",       "dbms-trf-req-database-3",          "aksk_rds",       True),
    ("159.138.164.124",3306, "was TCP-blocked",       "citizen-digital-dev-db-cluster",   "aksk_rds",       True),
]

def tcp_probe(host, port, timeout=8.0):
    r = {"tcp_ok": False, "err": None, "latency_ms": None, "mysql_version": None, "handshake_bytes": 0}
    t0 = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            r["tcp_ok"] = True
            r["latency_ms"] = round((time.time()-t0)*1000, 1)
            s.settimeout(3.0)
            try:
                data = s.recv(4096)
                r["handshake_bytes"] = len(data) if data else 0
                if data and len(data) > 5 and data[4] == 0x0a:
                    i = 5; end = data.find(b"\x00", i)
                    r["mysql_version"] = data[i:end].decode("latin-1","replace")
            except socket.timeout:
                pass
    except Exception as e:
        r["err"] = f"{type(e).__name__}:{str(e)[:120]}"
        r["latency_ms"] = round((time.time()-t0)*1000, 1)
    return r

def mysql_auth(host, port, user, password):
    import pymysql
    r = {"outcome": None, "code": None, "message": None, "databases": None, "server_user": None}
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password,
                               connect_timeout=8, read_timeout=10)
        r["outcome"] = "CONNECTED"
        with conn.cursor() as cur:
            cur.execute("SELECT USER(), CURRENT_USER(), VERSION();")
            u, cu, ver = cur.fetchone()
            r["server_user"] = u; r["current_user"] = cu; r["version"] = ver
            cur.execute("SHOW DATABASES;")
            dbs = [row[0] for row in cur.fetchall()]
            r["databases"] = dbs
            r["databases_count"] = len(dbs)
            # For non-system DBs, count tables per DB (up to 8) — read-only
            sys_dbs = {"information_schema","mysql","performance_schema","sys"}
            per_db = {}
            for db in dbs:
                if db in sys_dbs:
                    per_db[db] = {"system": True}
                    continue
                try:
                    cur.execute(f"USE `{db}`;")
                    cur.execute("SHOW TABLES;")
                    tbls = [t[0] for t in cur.fetchall()]
                    per_db[db] = {"tables_count": len(tbls), "tables_sample": tbls[:8]}
                except Exception as e:
                    per_db[db] = {"error": str(e)[:120]}
            r["per_db"] = per_db
        conn.close()
    except pymysql.err.OperationalError as e:
        r["outcome"] = "AUTH_ERROR" if (e.args and e.args[0] == 1045) else "OP_ERROR"
        r["code"] = e.args[0] if e.args else None
        r["message"] = (str(e.args[1]) if len(e.args) > 1 else str(e))[:200]
    except Exception as e:
        r["outcome"] = type(e).__name__
        r["message"] = str(e)[:200]
    return r

results = {"ts": datetime.now(timezone.utc).isoformat(),
           "creds_fp": "sha256_8=" + hashlib.sha256(BRAM_PW.encode()).hexdigest()[:8],
           "creds_user": BRAM_USER,
           "hosts": []}

for host, port, prior, name, source, try_auth in TARGETS:
    print(f"\n== {host}:{port}  [{name}]  prior: {prior} ==", flush=True)
    entry = {"host": host, "port": port, "name": name, "source": source, "prior_state": prior}
    tcp = tcp_probe(host, port)
    entry["tcp"] = tcp
    print(f"  TCP: ok={tcp['tcp_ok']} lat={tcp['latency_ms']}ms handshake={tcp['handshake_bytes']}B version={tcp['mysql_version']} err={tcp['err']}")
    if tcp["tcp_ok"] and try_auth:
        auth = mysql_auth(host, port, BRAM_USER, BRAM_PW)
        entry["auth"] = auth
        print(f"  AUTH bramuel: outcome={auth['outcome']} code={auth.get('code')} "
              f"databases_count={auth.get('databases_count')} msg={(auth.get('message') or '')[:120]}")
        if auth["outcome"] == "CONNECTED":
            print(f"    server_user={auth['server_user']} version={auth['version']}")
            print(f"    databases: {auth['databases']}")
            sys_dbs = {"information_schema","mysql","performance_schema","sys"}
            for db, info in auth["per_db"].items():
                if info.get("system"): continue
                if "error" in info: print(f"      {db}: ERROR {info['error']}")
                else: print(f"      {db}: tables={info['tables_count']}  sample={info['tables_sample'][:5]}")
    results["hosts"].append(entry)

with open("/app/assessment_workspace/tools/_scratch/reprobe_results.json", "w") as f:
    json.dump(results, f, indent=2, default=str)
print("\nSaved -> _scratch/reprobe_results.json")
