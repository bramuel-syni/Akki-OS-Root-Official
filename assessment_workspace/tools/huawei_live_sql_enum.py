"""Enumerate the 20 databases visible on 110.238.76.159 as bramuel (read-only)."""
import csv, json, pymysql, hashlib
from datetime import datetime, timezone

CRED = "/app/backend/estate_keys/data_sources/db_credentials.csv"

def load_pw():
    with open(CRED) as f:
        rows = list(csv.reader(f))
    for r in rows:
        if len(r) >= 4 and r[1] == "110.238.76.159":
            return r[2], r[3]
    raise RuntimeError("host not found in CSV")

USER, PW = load_pw()
HOST = "110.238.76.159"

conn = pymysql.connect(host=HOST, port=3306, user=USER, password=PW, connect_timeout=8, read_timeout=15)
result = {"host": HOST, "user": USER, "pw_fp": "sha256_8=" + hashlib.sha256(PW.encode()).hexdigest()[:8],
          "ts": datetime.now(timezone.utc).isoformat(), "databases": {}}

with conn.cursor() as cur:
    cur.execute("SHOW DATABASES;")
    all_dbs = [r[0] for r in cur.fetchall()]

    # System DBs to note but skip deep-enum
    system_dbs = {"information_schema","mysql","performance_schema","sys"}
    print(f"All databases visible ({len(all_dbs)}):")
    for db in all_dbs:
        mark = " (system)" if db in system_dbs else ""
        print(f"  - {db}{mark}")
    print()

    for db in all_dbs:
        entry = {"tables_count": None, "tables_sample": None, "table_row_counts": {},
                 "system": db in system_dbs, "error": None}
        try:
            cur.execute(f"USE `{db}`;")
            cur.execute("SHOW TABLES;")
            tables = [r[0] for r in cur.fetchall()]
            entry["tables_count"] = len(tables)
            entry["tables_sample"] = tables[:30]
            # Skip row counts on system DBs and on empty schemas
            if not entry["system"] and tables:
                for tb in tables[:8]:  # first 8 tables per db
                    try:
                        cur.execute(f"SELECT COUNT(*) FROM `{tb}`;")
                        entry["table_row_counts"][tb] = cur.fetchone()[0]
                    except Exception as e:
                        entry["table_row_counts"][tb] = f"<err:{str(e)[:80]}>"
        except pymysql.err.Error as e:
            entry["error"] = f"{e.args[0]}:{str(e.args[1])[:120]}" if len(e.args) > 1 else str(e)[:200]
        result["databases"][db] = entry
        summary = f"tables={entry['tables_count']} rc={dict(list(entry['table_row_counts'].items())[:5])}" \
                  if entry["tables_count"] is not None else f"err={entry['error']}"
        print(f"  {db}: {summary}")

    # Pick one non-system, non-empty table, show columns + 1 redacted row
    print("\n=== One representative table proof (redacted) ===")
    for db, e in result["databases"].items():
        if e["system"] or not e["tables_count"]: continue
        # find a table with rows
        cand = None
        for tb, cnt in e["table_row_counts"].items():
            if isinstance(cnt, int) and cnt > 0:
                cand = tb; break
        if cand:
            cur.execute(f"USE `{db}`;")
            cur.execute(f"SELECT * FROM `{cand}` LIMIT 3;")
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            SENS = ("phone","msisdn","email","password","pwd","token","secret","otp","ssn","dob",
                    "idnumber","id_number","national_id","surname","firstname","lastname","fullname",
                    "address","account","card","cvv","pin","iban","user","name","username","hash",
                    "mobile","tel","contact","salt","key","auth")
            def redact(colname, val):
                if val is None: return None
                lc = colname.lower()
                if any(h in lc for h in SENS):
                    s = str(val); return f"<REDACTED len={len(s)}>"
                s = str(val)
                if "@" in s and "." in s and " " not in s: return "<REDACTED-email>"
                if s.startswith("+") and len(s) > 8: return "<REDACTED-phone>"
                if len(s) > 60: return s[:60] + f"…(+{len(s)-60})"
                return s
            red_rows = [{cols[i]: redact(cols[i], row[i]) for i in range(len(cols))} for row in rows]
            result["proof_query"] = {"db": db, "table": cand, "columns": cols, "rows_redacted": red_rows}
            print(f"  db={db} table={cand}")
            print(f"  columns: {cols}")
            for rr in red_rows:
                print(f"  row: {rr}")
            break

conn.close()

with open("/app/assessment_workspace/tools/_scratch/live_sql_enum.json", "w") as f:
    json.dump(result, f, indent=2, default=str)
print("\nSaved -> _scratch/live_sql_enum.json")
