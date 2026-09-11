"""
Live DB reach test — TCP + protocol handshake only. No credentials will be attempted with real usernames.
- MySQL: read the initial handshake packet (server sends unprompted; proves DB is alive).
- Optionally attempt a login with a garbage user to confirm auth-path returns AccessDenied.
- PostgreSQL: attempt startup with a bogus user; expect an authentication_failed / role does not exist.
Read-only, no writes.
"""
import json, socket, struct, time, sys
from datetime import datetime, timezone

RESULTS_IN = "/app/assessment_workspace/tools/_scratch/probe_results.json"
OUT = "/app/assessment_workspace/tools/_scratch/dbreach_results.json"

def now(): return datetime.now(timezone.utc).isoformat()

def tcp_reach(host, port, timeout=6.0):
    r = {"host": host, "port": port, "tcp_ok": False, "error": None, "latency_ms": None}
    t0 = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            r["tcp_ok"] = True
            r["latency_ms"] = round((time.time() - t0) * 1000, 1)
            s.settimeout(3.0)
            try:
                data = s.recv(4096)
                r["handshake_bytes"] = len(data) if data else 0
                r["handshake_prefix_hex"] = data[:64].hex() if data else None
                # MySQL greeting parse
                if data and len(data) > 5 and data[4] == 0x0a:  # protocol v10
                    # skip 3-byte length + 1-byte seq id + 1-byte protocol
                    i = 5
                    end = data.find(b"\x00", i)
                    version = data[i:end].decode("latin-1", "replace")
                    r["mysql_protocol"] = 10
                    r["mysql_version"] = version
                    r["mysql_greeting_parsed"] = True
            except socket.timeout:
                r["handshake_bytes"] = 0
                r["handshake_note"] = "server didn't send greeting within 3s"
    except Exception as e:
        r["error"] = f"{type(e).__name__}:{str(e)[:120]}"
        r["latency_ms"] = round((time.time() - t0) * 1000, 1)
    return r

def mysql_login_probe(host, port, user="rms_probe_readonly", password="not-a-real-password-check-auth-path"):
    """Try to log in — we EXPECT failure. The error code tells us the DB is alive & auth-gated."""
    import pymysql
    r = {"host": host, "port": port, "user_tried": user, "outcome": None, "sqlstate": None, "code": None}
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password, connect_timeout=6, read_timeout=6)
        # If somehow it connects (should NOT), just close.
        conn.close()
        r["outcome"] = "UNEXPECTED_SUCCESS"
    except pymysql.err.OperationalError as e:
        code = e.args[0] if e.args else None
        msg = str(e.args[1]) if len(e.args) > 1 else str(e)
        r["outcome"] = "OPERATIONAL_ERROR"
        r["code"] = code
        r["message"] = msg[:200]
        # 1045 = Access denied for user (auth path alive, wrong creds)
        # 1130 = Host not allowed to connect (whitelist blocked)
        # 2003 = Can't connect (network/host)
    except Exception as e:
        r["outcome"] = type(e).__name__
        r["message"] = str(e)[:200]
    return r

def pg_login_probe(host, port, user="rms_probe_readonly", database="postgres"):
    import psycopg2
    r = {"host": host, "port": port, "user_tried": user, "database": database, "outcome": None}
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password="not-a-real-password", dbname=database, connect_timeout=6)
        conn.close()
        r["outcome"] = "UNEXPECTED_SUCCESS"
    except psycopg2.OperationalError as e:
        r["outcome"] = "OPERATIONAL_ERROR"
        r["message"] = str(e)[:250]
    except Exception as e:
        r["outcome"] = type(e).__name__
        r["message"] = str(e)[:200]
    return r

def main():
    with open(RESULTS_IN) as f:
        prev = json.load(f)
    results = {"started_at": now(), "targets": []}
    for inst in prev["rds"]["instances"]:
        target = {"name": inst["name"], "region": inst["region"], "engine": inst["engine"],
                  "engine_version": inst["engine_version"], "port": inst["port"],
                  "private_ips": inst["private_ips"], "public_ips": inst["public_ips"]}
        target["probes"] = []
        endpoints = list(inst["public_ips"] or [])
        # Also probe private IP (will 99% fail from this container, but proves it)
        for pip in (inst["private_ips"] or []):
            endpoints.append(pip)
        for ep in endpoints:
            tcp = tcp_reach(ep, inst["port"])
            probe = {"endpoint": ep, "tcp": tcp}
            if tcp["tcp_ok"]:
                if (inst["engine"] or "").lower().startswith("mysql"):
                    probe["auth"] = mysql_login_probe(ep, inst["port"])
                elif (inst["engine"] or "").lower().startswith("postgres"):
                    probe["auth"] = pg_login_probe(ep, inst["port"])
            target["probes"].append(probe)
        results["targets"].append(target)
    results["finished_at"] = now()
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    # Pretty summary to stdout
    for t in results["targets"]:
        print(f"\n== {t['name']} ({t['engine']} {t['engine_version']}) region={t['region']} port={t['port']} ==")
        for p in t["probes"]:
            tcp = p["tcp"]
            auth = p.get("auth", {})
            print(f"  endpoint {p['endpoint']}: tcp_ok={tcp['tcp_ok']} lat={tcp.get('latency_ms')}ms err={tcp.get('error')}")
            if tcp["tcp_ok"]:
                print(f"    handshake={tcp.get('handshake_bytes')}B mysql_version={tcp.get('mysql_version')}")
                print(f"    auth: outcome={auth.get('outcome')} code={auth.get('code')} msg={auth.get('message','')[:160]}")

if __name__ == "__main__":
    main()
