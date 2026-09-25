"""Census on what is connected RIGHT NOW (exhaustive-across-reachable, Canon-4 §5.1).
Connected: Razuna/Newsvault MySQL (159.138.173.58) + NAS via JUMP CIFS.
Aggregates-only. Banks a reachable-now census receipt + unmeasured register."""
import csv, json, socket, datetime as dt, pathlib, collections, re
import pymysql, paramiko

TS = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
SYS = {"information_schema","mysql","performance_schema","sys"}

# --- parse RMS creds (per-host inheritance, same loader that authed Razuna) ---
rows=list(csv.reader(open('/app/backend/estate_keys/data_sources/RMS_CREDS_3.csv')))
def is_ip(s):
    p=str(s).split("."); return len(p)==4 and all(x.isdigit() and 0<=int(x)<256 for x in p)
su=sp=None; hosts={}
for r in rows:
    r=(r+['']*7)[:7]; dbn,h,u,p=r[0].strip(),r[1].strip(),r[2].strip(),r[3].strip()
    if u and p: su,sp=u,p
    if is_ip(h) and h!="10.10.55.55":
        hosts.setdefault(h,{"user":u or su,"pw":p or sp})
RAZ=hosts["159.138.173.58"]
JP="76Nkr9P4Jv77"
SEC=[RAZ["pw"], JP]
def red(t):
    for s in SEC:
        if s and t: t=t.replace(s,"********")
    return t

# --- PII/role heuristic on column names ---
ROLE_PAT = [
 ("email", r"email|e_mail"), ("phone", r"phone|msisdn|mobile|tel|contact_no"),
 ("name_person", r"first_name|last_name|fullname|full_name|surname|username|name$"),
 ("dob", r"dob|date_of_birth|birth"), ("national_id", r"national_id|id_no|idnumber|passport|nid"),
 ("address", r"address|street|city|county|postal|location"), ("amount", r"amount|price|cost|balance|total|fee|charge"),
 ("timestamp", r"created_at|updated_at|_at$|timestamp|_date|date_|datetime"), ("password", r"password|passwd|pwd|secret|token|api_key"),
 ("geo", r"lat|lng|longitude|latitude|geo"), ("ip", r"ip_address|ipaddr"),
]
def roles_for(col):
    c=col.lower(); out=set()
    for role,pat in ROLE_PAT:
        if re.search(pat,c): out.add(role)
    return out

# --- walk Razuna/Newsvault NOW ---
result={"receipt_kind":"REACHABLE_NOW_CENSUS","at_utc":TS,
        "posture":"Canon-4 §5.1 exhaustive-across-reachable + Doc-9 A5.4 first-class unmeasured",
        "connected_surfaces":[], "unmeasured_register":[]}
mysql_report={"host":"159.138.173.58","label":"Razuna/Newsvault","databases":[]}
role_hist=collections.Counter(); top=[]; no_ts=0; tbl_n=0
try:
    c=pymysql.connect(host="159.138.173.58",port=3306,user=RAZ["user"],password=RAZ["pw"],connect_timeout=8,read_timeout=30)
    with c.cursor() as cur:
        cur.execute("SELECT schema_name FROM information_schema.schemata")
        dbs=[r[0] for r in cur.fetchall() if r[0] not in SYS]
        for db in dbs:
            cur.execute("SELECT table_name, table_rows FROM information_schema.tables WHERE table_schema=%s AND table_type='BASE TABLE'",(db,))
            rc={r[0]:int(r[1] or 0) for r in cur.fetchall()}
            cur.execute("SELECT table_name,column_name,data_type FROM information_schema.columns WHERE table_schema=%s ORDER BY table_name,ordinal_position",(db,))
            cols=collections.defaultdict(list)
            for tn,cn,ctype in cur.fetchall(): cols[tn].append((cn,ctype))
            dbrec={"database":db,"table_count":len(rc),"row_count_est":sum(rc.values()),"column_count":sum(len(v) for v in cols.values())}
            for tn in rc:
                tbl_n+=1; top.append((rc[tn],db,tn))
                has_ts=False
                for cn,ctype in cols.get(tn,[]):
                    for role in roles_for(cn): role_hist[role]+=1
                    if ctype in ("timestamp","datetime","date"): has_ts=True
                if not has_ts: no_ts+=1
            mysql_report["databases"].append(dbrec)
    c.close()
    mysql_report["status"]="CONNECTED"
    mysql_report["totals"]={"databases":len(mysql_report["databases"]),
        "tables":sum(d["table_count"] for d in mysql_report["databases"]),
        "columns":sum(d["column_count"] for d in mysql_report["databases"]),
        "rows_est":sum(d["row_count_est"] for d in mysql_report["databases"])}
    mysql_report["column_role_signals"]=dict(role_hist)
    mysql_report["tables_without_timestamp"]=no_ts
    top.sort(reverse=True)
    mysql_report["top_tables_by_rows"]=[{"db":d,"table":t,"rows_est":r} for r,d,t in top[:10]]
    result["connected_surfaces"].append(mysql_report)
except Exception as e:
    result["connected_surfaces"].append({"host":"159.138.173.58","status":f"FAIL:{type(e).__name__}","error":red(str(e))[:120]})

# --- confirm NAS still connected via JUMP CIFS ---
nas={"surface":"NAS //10.10.55.55/OFFAIRRECS/Record via JUMP CIFS mount"}
try:
    cli=paramiko.SSHClient(); cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cli.connect("159.138.173.250",22,username="root",password=JP,timeout=10,look_for_keys=False,allow_agent=False)
    _i,o,_=cli.exec_command("df -B1 /mnt/nfs-share 2>/dev/null | tail -1; echo '---'; ls -1 /mnt/nfs-share 2>/dev/null | grep -ic channel",timeout=20)
    out=o.read().decode().strip(); cli.close()
    df_line=out.split("---")[0].strip(); chans=out.split("---")[-1].strip()
    nas["status"]="CONNECTED"; nas["df"]=red(df_line); nas["channel_dirs"]=chans
    nas["note"]="structural census already banked: CENSUS-3-E 20260925T021101Z (47.3TB, 16 channels)"
except Exception as e:
    nas["status"]=f"FAIL:{type(e).__name__}"; nas["error"]=red(str(e))[:120]
result["connected_surfaces"].append(nas)

# --- unmeasured register (live-verified 03:45Z) ---
result["unmeasured_register"]=[
 {"surface":"USSD 110.238.76.159 + WEEGO 159.138.162.146","reason":"TCP open but MySQL auth DENIED for bramuel@current-source-IP (credential rotated / grant not for this IP)","class":"credential"},
 {"surface":"VIUSASA 203.123.86.10, MICROSERVICES 159.138.164.93, CD 159.138.164.124, visitors 110.238.75.83, Shikisha 203.123.83.144","reason":"TCP timeout — security-group does not allow this pod's ephemeral egress IP 35.193.209.116","class":"network_acl"},
 {"surface":"citizen_digital 159.138.164.103 (Item-3 host)","reason":"TCP timeout via pod; SG not open for source IP","class":"network_acl"},
 {"surface":"GPU hosts akki-vm / akki-vm-ii","reason":"SSH publickey-only; our key not authorized; password refused","class":"host_auth"},
 {"surface":"Huawei OBS (106 buckets)","reason":"no OBS credentials present in this pod env; content also IAM-gated (GetObject 403 on 74/106)","class":"credential+iam"},
]

out_dir=pathlib.Path("/app/assessment_workspace/phase0/connectivity_receipts")
recp=out_dir/f"{TS}_REACHABLE_NOW_CENSUS.json"
recp.write_text(json.dumps(result,indent=2,default=str))

# --- print ---
print("=== CENSUS ON WHAT IS CONNECTED (",TS,") ===")
for s in result["connected_surfaces"]:
    if s.get("status")=="CONNECTED" and "totals" in s:
        t=s["totals"]; print(f"\n[MySQL {s['label']} {s['host']}] CONNECTED")
        print(f"  databases={t['databases']} tables={t['tables']} columns={t['columns']} rows_est={t['rows_est']:,}")
        print(f"  tables_without_timestamp={s['tables_without_timestamp']}  role_signals={s['column_role_signals']}")
        print("  top tables:", [(x['table'],x['rows_est']) for x in s['top_tables_by_rows'][:5]])
    elif s.get("surface","").startswith("NAS"):
        print(f"\n[NAS] {s.get('status')} · {s.get('df','')}  channel_dirs={s.get('channel_dirs','')}")
    else:
        print("\n[surface]", s.get("host"), s.get("status"), s.get("error",""))
print("\n=== UNMEASURED REGISTER (first-class, live 03:45Z) ===")
for u in result["unmeasured_register"]:
    print(f"  [{u['class']}] {u['surface']}\n      -> {u['reason']}")
print("\nreceipt:", recp)
