"""Live SQL reach — Path A. Read-only. Credential-from-CSV per owner directive."""
import csv, hashlib, json, sys
from datetime import datetime, timezone

CRED = "/app/backend/estate_keys/data_sources/db_credentials.csv"

def now(): return datetime.now(timezone.utc).isoformat()

# The CSV has a "banner-row-per-group" shape. Parse it structurally.
def parse_targets(path):
    """Returns list of {group, dbname, host, user, password} for rows that have host+user+password."""
    with open(path, "r", newline="") as f:
        rows = list(csv.reader(f))
    targets = []
    current_group = None
    header_seen = False
    for row in rows:
        cells = [c.strip() for c in row]
        non_empty = [c for c in cells if c]
        if len(non_empty) == 1:
            current_group = non_empty[0]
            header_seen = False
            continue
        if not header_seen and len(cells) >= 4 and cells[0].upper() == "DATABASE NAME":
            header_seen = True
            continue
        if len(cells) >= 4 and cells[0] and cells[1] and cells[2] and cells[3]:
            targets.append({
                "group": current_group,
                "dbname": cells[0], "host": cells[1],
                "user": cells[2], "password": cells[3],
            })
    return targets

def probe(t):
    import pymysql
    result = {"group": t["group"], "dbname": t["dbname"], "host": t["host"], "user": t["user"],
              "pw_fp": "sha256_8=" + hashlib.sha256(t["password"].encode()).hexdigest()[:8],
              "connected": False, "steps": []}
    try:
        conn = pymysql.connect(
            host=t["host"], port=3306, user=t["user"], password=t["password"],
            connect_timeout=8, read_timeout=8,
        )
        result["connected"] = True
        with conn.cursor() as cur:
            # 1. SELECT 1
            cur.execute("SELECT 1;")
            r = cur.fetchone()
            result["steps"].append({"sql": "SELECT 1;", "row": list(r)})
            # 2. VERSION
            cur.execute("SELECT VERSION();")
            r = cur.fetchone()
            result["steps"].append({"sql": "SELECT VERSION();", "row": list(r)})
            # 3. CURRENT_USER
            cur.execute("SELECT CURRENT_USER(), USER(), @@hostname, @@version_comment;")
            r = cur.fetchone()
            result["steps"].append({"sql": "SELECT CURRENT_USER(), USER(), @@hostname, @@version_comment;", "row": list(r)})
            # 4. SHOW DATABASES
            cur.execute("SHOW DATABASES;")
            dbs = [row[0] for row in cur.fetchall()]
            result["databases"] = dbs
            result["steps"].append({"sql": "SHOW DATABASES;", "count": len(dbs), "sample": dbs[:40]})
            # 5. Try USE target dbname
            db_tables = {}
            try:
                cur.execute(f"USE `{t['dbname']}`;")
                result["use_target_ok"] = True
                cur.execute("SHOW TABLES;")
                tbls = [row[0] for row in cur.fetchall()]
                result["target_db"] = t["dbname"]
                result["target_tables_count"] = len(tbls)
                result["target_tables_sample"] = tbls[:30]
                # Count rows on up to 5 tables
                for tb in tbls[:5]:
                    try:
                        cur.execute(f"SELECT COUNT(*) FROM `{tb}`;")
                        cnt = cur.fetchone()[0]
                        db_tables[tb] = {"row_count": cnt}
                    except Exception as e:
                        db_tables[tb] = {"error": str(e)[:120]}
                # SELECT LIMIT 5 on the first table with any rows
                for tb in tbls[:5]:
                    if db_tables.get(tb, {}).get("row_count", 0) > 0:
                        try:
                            cur.execute(f"SELECT * FROM `{tb}` LIMIT 5;")
                            cols = [d[0] for d in cur.description]
                            sample_rows = cur.fetchall()
                            # Redact any col that looks like sensitive PII
                            sensitive_hints = ("phone","msisdn","email","password","pwd","token","secret",
                                              "otp","ssn","dob","dob_","idnumber","id_number","national_id",
                                              "surname","firstname","lastname","fullname","address","account","card","cvv","pin","iban")
                            def redact(colname, val):
                                if val is None: return None
                                lc = colname.lower()
                                if any(h in lc for h in sensitive_hints):
                                    s = str(val)
                                    return f"<REDACTED len={len(s)}>"
                                s = str(val)
                                # If a value looks like an email, phone, or long token — redact regardless
                                if "@" in s and "." in s:
                                    return "<REDACTED-email>"
                                if s.startswith("+") and s[1:].replace(" ","").isdigit() and len(s) > 8:
                                    return "<REDACTED-phone>"
                                return s if len(s) < 80 else s[:60] + f"…(+{len(s)-60})"
                            redacted_rows = [
                                {cols[i]: redact(cols[i], row[i]) for i in range(len(cols))}
                                for row in sample_rows
                            ]
                            result["target_sample_query"] = {
                                "sql": f"SELECT * FROM `{tb}` LIMIT 5;",
                                "columns": cols,
                                "rows_redacted": redacted_rows,
                            }
                            break
                        except Exception as e:
                            result["target_sample_error"] = f"{tb}: {str(e)[:160]}"
                result["target_table_row_counts"] = db_tables
            except pymysql.err.Error as e:
                result["use_target_ok"] = False
                result["use_target_err"] = f"{e.args[0]}:{str(e.args[1])[:160]}" if len(e.args) > 1 else str(e)[:200]
        conn.close()
    except pymysql.err.OperationalError as e:
        result["error"] = {"type": "OperationalError", "code": e.args[0] if e.args else None,
                          "message": (str(e.args[1]) if len(e.args) > 1 else str(e))[:250]}
    except Exception as e:
        result["error"] = {"type": type(e).__name__, "message": str(e)[:250]}
    return result

def main():
    targets = parse_targets(CRED)
    out = {"started_at": now(), "target_count": len(targets), "results": []}
    for t in targets:
        print(f"\n== {t['group']} / {t['dbname']} @ {t['host']} as {t['user']} ==", flush=True)
        r = probe(t)
        # print sanitised summary
        if r["connected"]:
            print(f"  CONNECTED ok=True databases_n={len(r.get('databases',[]))} use_target={r.get('use_target_ok')} tables_in_target={r.get('target_tables_count')}")
            for s in r["steps"][:3]:
                print(f"    {s['sql']} -> {s.get('row') or s.get('sample')}")
            print(f"    target_row_counts: {r.get('target_table_row_counts')}")
        else:
            print(f"  NOT CONNECTED err={r.get('error')}")
        out["results"].append(r)
    out["finished_at"] = now()
    with open("/app/assessment_workspace/tools/_scratch/live_sql_results.json", "w") as f:
        # Strip password field before persisting
        safe = json.loads(json.dumps(out, default=str))
        for row in safe["results"]:
            row.pop("password", None)
        json.dump(safe, f, indent=2, default=str)

if __name__ == "__main__":
    main()
