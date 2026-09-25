"""Item-3 RMS census review extractor. Reads Mtafiti discovery receipts.
Excludes DigiCow. Computes coverage/composition/PII/quality/FK/cost answers."""
import json, collections, re

D = "/app/assessment_workspace/phase0/mtafiti_gpu_discovery/"
comp = json.load(open(D+"composition_census_latest.json"))
strat = json.load(open(D+"stratified_samples_20260918T110138Z.json"))
qual = json.load(open(D+"quality_profile_latest.json"))
wcb = json.load(open(D+"wave_close_bundle_latest.json"))
probe = json.load(open(D+"live_readonly_probe_latest.json"))

HOSTS = comp["hosts"]  # weego, ussd
NAME = {h: comp["per_host"][h]["label"] for h in HOSTS}
print("HOSTS:", [(h, NAME[h]) for h in HOSTS])

# ---- wave totals + cost ----
print("\n=== WAVE TOTALS ===", json.dumps(wcb["totals"]))
print("=== COST ===", json.dumps(wcb["cost_summary"]))

# ---- composition per host/schema + top tables + timestamps ----
role_hist = collections.Counter()
top_tables = []  # (rows, host, table)
no_ts_tables = collections.Counter(); ts_tables = collections.Counter(); tbl_total = collections.Counter()
per_db = collections.defaultdict(lambda: {"tables":0,"rows":0,"cols":0})
for h in HOSTS:
    ph = comp["per_host"][h]
    for role, n in ph["column_role_signals_summary"]["by_role"].items():
        role_hist[role] += n
    for tname, tv in ph["per_table"].items():
        rows = tv.get("row_count",0) or 0
        top_tables.append((rows, NAME[h], tname))
        db = tname.split(".")[0]
        per_db[(NAME[h],db)]["tables"] += 1
        per_db[(NAME[h],db)]["rows"] += rows
        per_db[(NAME[h],db)]["cols"] += tv.get("column_count",0) or 0
        cols = tv.get("columns",[])
        has_ts = any((c.get("data_type","") in ("timestamp","datetime","date")) for c in cols)
        tbl_total[NAME[h]] += 1
        if has_ts: ts_tables[NAME[h]] += 1
        else: no_ts_tables[NAME[h]] += 1

print("\n=== PER-DATABASE (schema · tables · columns · rows) ===")
for (host,db),v in sorted(per_db.items(), key=lambda x:-x[1]["rows"]):
    print(f"  {host:6s} {db:28s} tbl={v['tables']:4d} cols={v['cols']:6d} rows={v['rows']:,}")

print("\n=== TOP 20 TABLES BY ROWS (concentration) ===")
top_tables.sort(reverse=True)
grand = sum(r for r,_,_ in top_tables)
cum=0
for i,(rows,host,t) in enumerate(top_tables[:20],1):
    cum+=rows
    print(f"  {i:2d}. {host:6s} {t:45s} {rows:>13,}")
print(f"  --- top20 = {cum:,} of {grand:,} rows = {round(100*cum/grand,1)}% of counted rows ---")

print("\n=== TABLES WITH NO TIMESTAMP COLUMN (age unknowable) ===")
for h in HOSTS:
    n=NAME[h]; print(f"  {n}: {no_ts_tables[n]} of {tbl_total[n]} tables have NO timestamp ({round(100*no_ts_tables[n]/max(tbl_total[n],1))}%)")

print("\n=== COLUMN ROLE HISTOGRAM (aggregate, both hosts) ===")
for role,n in role_hist.most_common():
    print(f"  {role:22s} {n}")

# ---- PII (roles + stratified) ----
PII_ROLES = {"role.email","role.phone","role.address","role.dob","role.gender","role.password","role.name_person","role.ip","role.token","role.geo"}
print("\n=== PII SIGNAL SUMMARY (name-based roles) ===")
pii_total = sum(role_hist[r] for r in PII_ROLES)
print("  total PII-role columns:", pii_total, "->", {r.split('.')[1]:role_hist[r] for r in PII_ROLES if role_hist[r]})
for h in HOSTS:
    sh = strat["per_host"][h]
    print(f"  [{NAME[h]}] stratified pii_signals_summary:", json.dumps(sh.get("pii_signals_summary",{}))[:300])

# ---- FK graph: hubs + islands ----
print("\n=== FK CANDIDATE GRAPH (from stratified fk signals) ===")
indeg = collections.Counter(); outdeg = collections.Counter(); all_tables=set(); edges=0
for h in HOSTS:
    for t in comp["per_host"][h]["per_table"]:
        all_tables.add(f"{NAME[h]}:{t}")
    fk = strat["fk_candidate_signals_by_host"][h]
    samp = fk.get("sample",[]) if isinstance(fk,dict) else []
    print(f"  [{NAME[h]}] fk total={fk.get('total') if isinstance(fk,dict) else '?'} sample_len={len(samp)}")
    for s in samp:
        ref = s.get("source_ref","")
        m = re.match(r"([^.]+\.[^.]+)\.[^.]+->([^.]+\.[^.]+)", ref) or re.match(r"([^.]+\.[^.]+)\.[^.]+->([^.]+)", ref)
        if m:
            src=f"{NAME[h]}:{m.group(1)}"; tgt=f"{NAME[h]}:{m.group(2)}"
            outdeg[src]+=1; indeg[tgt]+=1; edges+=1
print(f"  edges parsed (from sample): {edges}")
print("  TOP HUBS (most incoming FK candidates):")
for t,c in indeg.most_common(10): print(f"     {t}  in={c}")
touched = set(indeg)|set(outdeg)
islands=[t for t in all_tables if t not in touched]
print(f"  ISLANDS (no FK candidate in or out, from sampled signals): {len(islands)} of {len(all_tables)} tables")
print("     e.g.", islands[:8])

# ---- Quality: dead columns ----
print("\n=== QUALITY PROFILE (dead columns) ===")
for h in HOSTS:
    qh = qual["per_host"][h]
    print(f"  [{NAME[h]}] quality totals:", json.dumps(qh.get("totals",{}))[:200])
    pc = qh.get("per_column",{})
    if isinstance(pc,dict):
        deadnull=[k for k,v in pc.items() if isinstance(v,dict) and (v.get("null_fraction",0)==1 or v.get("all_null"))]
        const=[k for k,v in pc.items() if isinstance(v,dict) and (v.get("distinct_count")==1 or v.get("constant"))]
        print(f"     per_column profiled={len(pc)} · all-null={len(deadnull)} · constant={len(const)}")
        # show one profiled column shape
        if pc: 
            k0=list(pc.keys())[0]; print("     sample col:", k0, json.dumps(pc[k0])[:200])

# ---- Coverage ----
print("\n=== COVERAGE (this run) ===")
for h in HOSTS:
    pp = probe["per_host"][h]
    print(f"  {NAME[h]} ({h}) connected={pp.get('connected')} errors={len(pp.get('errors',[]))}")
