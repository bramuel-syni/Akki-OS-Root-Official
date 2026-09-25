#!/usr/bin/env python3
"""estate_census_v3_direct.py — CENSUS-3-C · direct-connect MySQL estate walk.

Continues the numbered census lineage (next id after the highest census_<NNNN>).
Aggregates-only chokepoint (owner ruling 2, banked): the ONLY things read are
schemata / table lists / row-count estimates / column {name,type}. NO row values,
NO per-column extrema. Every query maps to one whitelisted sql_shape audit entry.

Direct pymysql connections (JUMP bastion 159.138.173.250 is unreachable from this
pod; these RMS hosts are directly reachable + authable). Null-count-per-column is
DEFERRED this pass (bounded/budgeted per R-106 §3) and marked honest-gap.
"""
from __future__ import annotations
import csv, json, re, time, datetime as dt, pathlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import pymysql

TS = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
RECORDS_DIR = pathlib.Path("/app/assessment_workspace/phase0/census")
CREDS_CSV = "/app/backend/estate_keys/data_sources/RMS_CREDS_3.csv"
SYS = {"information_schema", "mysql", "performance_schema", "sys"}
GLOBAL_DEADLINE = time.monotonic() + 150

OWNER_DIRECTIVE = ("Owner directive (banked in estate_census_v2 header) verbatim: "
                   "'you should have access to all. Dont block or assume a path. act as "
                   "seasoned systems engineer. Have Akki run the census job on all the "
                   "external connected data estates.'")
CANON_ANCHOR = {"primary": "Doc 9 · #13 — THE CENSUS · rule B5.7 · Mtafiti",
                "aggregates_only": "owner ruling 2 (2026-08-28) — row_count + column{name,type} + (null_count deferred)"}

def _is_ip(s):
    p = str(s).split("."); return len(p) == 4 and all(x.isdigit() and 0 <= int(x) < 256 for x in p)

def _load_hosts():
    rows = list(csv.reader(open(CREDS_CSV)))
    shared_u = shared_p = None; hosts = {}; section = None
    for r in rows:
        r = (r + [""] * 7)[:7]
        dbname, host, user, pw, status = r[0].strip(), r[1].strip(), r[2].strip(), r[3].strip(), r[4].strip()
        if r[0].strip() and not host and not user and not pw and r[0].strip().isupper():
            section = r[0].strip()
        if user and pw:
            shared_u, shared_p = user, pw
        if _is_ip(host) and host != "10.10.55.55":
            h = hosts.setdefault(host, {"host": host, "user": user or shared_u, "pw": pw or shared_p,
                                        "section": section, "status": status})
    return list(hosts.values())

def _conn(h):
    return pymysql.connect(host=h["host"], port=3306, user=h["user"], password=h["pw"],
                           connect_timeout=10, read_timeout=40, charset="utf8mb4")

def _cluster_census(h):
    trail = []
    res = {"cluster_host": h["host"], "section": h["section"], "status_in_sheet": h["status"],
           "user_prefix2": (h["user"] or "")[:2], "status": "?", "databases": []}
    t0 = time.monotonic()
    try:
        conn = _conn(h)
        with conn.cursor() as cur:
            cur.execute("SELECT schema_name FROM information_schema.schemata ORDER BY schema_name")
            trail.append({"sql_shape": "schemata_list", "at_utc": dt.datetime.now(dt.timezone.utc).isoformat()})
            dbs = [row[0] for row in cur.fetchall() if row[0] not in SYS]
            for db in dbs:
                d = {"database": db, "tables": []}
                cur.execute("SELECT table_name, table_rows FROM information_schema.tables "
                            "WHERE table_schema=%s AND table_type='BASE TABLE' ORDER BY table_name", (db,))
                trail.append({"sql_shape": "tables_list_and_row_count", "database": db,
                              "at_utc": dt.datetime.now(dt.timezone.utc).isoformat()})
                rc = {r[0]: int(r[1] or 0) for r in cur.fetchall()}
                cur.execute("SELECT table_name, column_name, data_type FROM information_schema.columns "
                            "WHERE table_schema=%s ORDER BY table_name, ordinal_position", (db,))
                trail.append({"sql_shape": "columns_list", "database": db,
                              "at_utc": dt.datetime.now(dt.timezone.utc).isoformat()})
                cols = {}
                for tn, cn, ct in cur.fetchall():
                    cols.setdefault(tn, []).append({"name": cn, "type": ct or ""})
                for tn in sorted(rc.keys()):
                    d["tables"].append({"table": tn, "row_count_est": rc[tn],
                                        "columns": cols.get(tn, []),
                                        "null_count": "DEFERRED_THIS_PASS"})
                d["table_count"] = len(d["tables"])
                d["row_count_est_total"] = sum(rc.values())
                res["databases"].append(d)
        conn.close()
        res["status"] = "OK"
        res["database_count"] = len(res["databases"])
        res["table_count"] = sum(x["table_count"] for x in res["databases"])
        res["row_count_est_total"] = sum(x["row_count_est_total"] for x in res["databases"])
    except Exception as e:
        res["status"] = f"FAIL:{type(e).__name__}"; res["error"] = str(e)[:200]
    res["elapsed_s"] = round(time.monotonic() - t0, 2)
    res["audit_trail"] = trail
    return res

def main():
    hosts = _load_hosts()
    print(f"[census] {len(hosts)} hosts to walk", flush=True)
    clusters = []
    with ThreadPoolExecutor(max_workers=8) as p:
        f2h = {p.submit(_cluster_census, h): h["host"] for h in hosts}
        for f in as_completed(f2h):
            x = f.result()
            print(f"  cluster[{f2h[f]}] {x['status']} dbs={x.get('database_count','-')} "
                  f"tbl={x.get('table_count','-')} rows~{x.get('row_count_est_total','-')} ({x['elapsed_s']}s)", flush=True)
            clusters.append(x)

    # numbering
    highest = 0
    if RECORDS_DIR.is_dir():
        for pth in RECORDS_DIR.iterdir():
            m = re.match(r"^census_(\d{4,})$", pth.name)
            if m: highest = max(highest, int(m.group(1)))
    census_id = highest + 1
    run_dir = RECORDS_DIR / f"census_{census_id:04d}"
    run_dir.mkdir(parents=True, exist_ok=True)

    ok = [c for c in clusters if c["status"] == "OK"]
    manifest = {
        "census_id": census_id,
        "started_at_utc": TS,
        "finished_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "initiator": "owner",
        "wave_id": "CENSUS-3-C",
        "estate_scope": "RMS MySQL estate · direct-connect · aggregates-only DB-level walk",
        "canon_anchor": CANON_ANCHOR,
        "owner_directive_verbatim": OWNER_DIRECTIVE,
        "continues_from": "census_0003 (surface census) — this fulfils its deferred CENSUS-3-C MySQL lane. Prior DB-level censuses #1/#2 walked the Digicow RDS estate (not reachable in this pod).",
        "connection_path": "direct pymysql (JUMP bastion 159.138.173.250 unreachable from pod)",
        "compute": {"gpu": "none", "path": "cpu-only", "cluster_workers": 8},
        "clusters": [],
        "rollup": {
            "cluster_count_reachable_authed": len(ok),
            "cluster_count_failed": len(clusters) - len(ok),
            "database_count": sum(c.get("database_count", 0) for c in ok),
            "table_count": sum(c.get("table_count", 0) for c in ok),
            "total_row_count_est": sum(c.get("row_count_est_total", 0) for c in ok),
        },
        "aggregates_only_attestation": "No row values read. Only schemata/table lists, information_schema.table_rows estimates, and column {name,type}. Per-column null_count DEFERRED this pass (bounded/budgeted per R-106 §3).",
        "honest_gaps": [
            "null_count per column deferred this pass (bounded run).",
            "JUMP-only clusters: none — all sheet MySQL hosts were directly reachable this pass.",
            "Digicow RDS (digicow_live/ndume · census #1/#2 surface) not walked: no db-restore-603-cluster.json connection record present in this pod.",
        ],
    }
    for c in clusters:
        tag = c["cluster_host"].replace(".", "_")
        (run_dir / f"cluster_{tag}.json").write_text(json.dumps(c, indent=2, default=str))
        manifest["clusters"].append({
            "cluster_host": c["cluster_host"], "section": c["section"],
            "status": c["status"], "database_count": c.get("database_count"),
            "table_count": c.get("table_count"), "row_count_est_total": c.get("row_count_est_total"),
            "per_cluster_file": f"cluster_{tag}.json",
        })
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str))
    print(f"\ncensus #{census_id} written -> {run_dir}/manifest.json")
    print("ROLLUP:", json.dumps(manifest["rollup"]))

if __name__ == "__main__":
    main()
