"""Direct-connect reachability + auth probe across RMS_CREDS_3 MySQL hosts.
Read-only. Structured output only; password never printed."""
import csv, socket, time
import pymysql

CSV = "/app/backend/estate_keys/data_sources/RMS_CREDS_3.csv"

def _is_ip(s):
    p = str(s).split(".")
    return len(p) == 4 and all(x.isdigit() and 0 <= int(x) < 256 for x in p)

# Parse: collect IP rows + inherited shared cred (single shared cred in this sheet).
rows = list(csv.reader(open(CSV)))
shared_user = shared_pw = None
hosts = {}  # ip -> {user,pw,dbs:set,section}
section = None
for r in rows:
    r = (r + [""] * 7)[:7]
    dbname, host, user, pw, status = r[0].strip(), r[1].strip(), r[2].strip(), r[3].strip(), r[4].strip()
    if user and pw:
        shared_user, shared_pw = user, pw
    if _is_ip(host) and host != "10.10.55.55":
        h = hosts.setdefault(host, {"user": user or shared_user, "pw": pw or shared_pw, "dbs": set(), "status": status})
        if dbname:
            h["dbs"].add(dbname)

secrets = {shared_pw} | {h["pw"] for h in hosts.values() if h["pw"]}
def red(t):
    for s in secrets:
        if s and t: t = t.replace(s, "********")
    return t

print("HOSTS_TO_PROBE:", [(ip, h["user"], "pw_len=%d" % len(h["pw"] or ""), "declared=%d" % len(h["dbs"]), h["status"]) for ip, h in hosts.items()])

SYS = {"information_schema", "mysql", "performance_schema", "sys"}
for ip, h in hosts.items():
    print(f"\n===== {ip} (status_in_sheet={h['status']!r}) =====")
    # TCP first
    s = socket.socket(); s.settimeout(6)
    try:
        s.connect((ip, 3306)); s.close(); tcp = "OPEN"
    except Exception as e:
        print(f"  tcp/3306 UNREACHABLE {type(e).__name__}"); continue
    print(f"  tcp/3306 {tcp}")
    # Auth
    t0 = time.monotonic()
    try:
        conn = pymysql.connect(host=ip, port=3306, user=h["user"], password=h["pw"],
                               connect_timeout=10, read_timeout=25)
        with conn.cursor() as cur:
            cur.execute("SHOW DATABASES")
            dbs = [row[0] for row in cur.fetchall()]
            userdbs = [d for d in dbs if d not in SYS]
            # aggregate table count across user dbs (aggregates-only, no row values)
            tcount = {}
            for d in userdbs:
                cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s", (d,))
                tcount[d] = cur.fetchone()[0]
        conn.close()
        print(f"  AUTH_OK ({round(time.monotonic()-t0,2)}s) · user_dbs={len(userdbs)} · dbs={userdbs}")
        print(f"  table_counts={tcount}")
    except Exception as e:
        print(f"  AUTH_FAIL ({round(time.monotonic()-t0,2)}s) {type(e).__name__}: {red(str(e))[:200]}")
