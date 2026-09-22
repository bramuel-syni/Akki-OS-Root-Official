#!/usr/bin/env python3
"""estate_census_v2.py — Census-2 executor via JUMP + local pool.
Canon anchor: Doc 9 · #13 · rule B5.7 (Mtafiti, pending_override).
"""
from __future__ import annotations
import argparse, datetime as dt, json, os, subprocess, sys, tempfile, time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from pathlib import Path

TS = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
OWNER_DIRECTIVE = ("Owner directive 2026-09-21T~19:35Z: 'you should have access to all. "
                   "Dont block or assume a path. act as seasoned systems engineer. "
                   "Have Akki [run] the census job on all the external connected data "
                   "estates, powered by the GPUs — apportion work for full utilization. "
                   "include audio, non music.'")
CANON_ANCHOR = {"primary": "Doc 9 · #13 — THE CENSUS · rule B5.7 · Mtafiti · pending_override",
                "secondary": ["A17.10 · Doc 17 · Targeta · pending_override",
                              "mtafiti.asset_registry_writer.write_asset_record (Canon-9 §3)"]}

FRESH_XLSX = "/app/audit/scratch/creds_20260921_redrop/RMS_CREDS.xlsx"
FRESH_SHA = "3311dae2d142f3a651431325d68f72a011598054a39c0d7b3976c757410cc545"
JUMP = {"host": "159.138.173.250", "port": 22, "user": "root", "password": "76Nkr9P4Jv77"}
NAS = {"host": "10.10.55.55", "user": "Bramwel", "password": "r:ZY5_j{"}
DIGICOW_CSV = "/app/assessment_workspace/custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_digicow_access_keys_csv.csv"
DIGICOW_XLSX = "/app/assessment_workspace/custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_digicow_xlsx.xlsx"
BUCKET, PREFIX = "training-content-2026", "audio/"
MYSQL_CLUSTERS: list[dict] = []

def _load_fresh_creds():
    global MYSQL_CLUSTERS
    from openpyxl import load_workbook
    def _ip(s):
        try:
            p = str(s).split(".")
            return len(p) == 4 and all(x.isdigit() and 0 <= int(x) < 256 for x in p)
        except (ValueError, TypeError): return False
    wb = load_workbook(FRESH_XLSX, data_only=True); ws = wb["Sheet1"]
    hosts = {}
    # Two-pass: pass 1 collects section-header credentials (rows where
    # col A is a section label AND col C/D populated), pass 2 assigns
    # them to member DB rows that share the cluster host.
    section_creds = None  # (user, pwd) inherited by member rows
    for r in range(3, ws.max_row+1):
        row = [ws.cell(row=r, column=c).value for c in range(1, ws.max_column+1)]
        while len(row) < 4: row.append(None)
        dbname, host, user, pwd = row[:4]
        # If this looks like a cluster-header row (user+pwd populated, host may be IP or placeholder)
        if user and pwd and host:
            section_creds = (str(user), str(pwd))
            if _ip(host):
                key = str(host)
                hosts.setdefault(key, {"host": key, "user": str(user), "password": str(pwd), "databases": []})
                if dbname: hosts[key]["databases"].append(str(dbname))
        elif host and _ip(host) and section_creds:
            # Member row inheriting from the enclosing section
            key = str(host)
            u, p = section_creds
            hosts.setdefault(key, {"host": key, "user": u, "password": p, "databases": []})
            if dbname: hosts[key]["databases"].append(str(dbname))
        elif dbname and not host and not user and not pwd:
            # Continuation row: same cluster as previous
            # Append to the most recently seen host (last inserted)
            if hosts:
                last_key = list(hosts.keys())[-1]
                hosts[last_key]["databases"].append(str(dbname))
    MYSQL_CLUSTERS = list(hosts.values())

def _cred_shape():
    return {"fresh_xlsx_sha256": FRESH_SHA,
            "mysql_clusters": [{"host": c["host"], "user_len": len(c["user"]), "user_prefix2": c["user"][:2],
                                "password_len": len(c["password"]), "declared_dbs": len(c["databases"])}
                               for c in MYSQL_CLUSTERS],
            "jump": {"host": JUMP["host"], "user_len": len(JUMP["user"]), "password_len": len(JUMP["password"])},
            "nas": {"host": NAS["host"], "user_len": len(NAS["user"]), "password_len": len(NAS["password"])}}

def _ssh_exec(sql, host, user, pwd, db="", timeout=45):
    import paramiko
    s = paramiko.SSHClient(); s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(JUMP["host"], JUMP["port"], username=JUMP["user"], password=JUMP["password"],
              timeout=8, look_for_keys=False, allow_agent=False, banner_timeout=8)
    try:
        db_a = f"-D {db}" if db else ""
        # Escape the password for single-quoted bash string.
        pwd_esc = pwd.replace("'", "'\\''")
        # bash process substitution keeps pwd out of ps args and off cmd line.
        cmd = (f"bash -c \"mysql --defaults-extra-file=<(printf '[client]\\npassword=%s\\n' '{pwd_esc}') "
               f"--column-names=false --batch -N -h {host} -P 3306 -u {user} {db_a} -e \\\"{sql}\\\"\"")
        _, o, e = s.exec_command(cmd, timeout=timeout)
        rc = o.channel.recv_exit_status()
        rows = [l.split("\t") for l in o.read().decode('utf-8','replace').splitlines() if l]
        return rc, rows, e.read().decode('utf-8','replace')
    finally:
        s.close()

def _to_int(x):
    try: return int(x)
    except (ValueError, TypeError): return x

def _cluster_census(c):
    host, user, pwd = c["host"], c["user"], c["password"]
    res = {"host": host, "user_prefix2": user[:2], "declared_databases": c["databases"], "status": "?"}
    t0 = time.monotonic()
    try:
        rc, rows, err = _ssh_exec("SHOW DATABASES", host, user, pwd)
        if rc != 0:
            res["status"] = "AUTH_FAIL"; res["error"] = err.strip()[:300]; res["elapsed_s"] = round(time.monotonic()-t0,3); return res
        SYS = {"information_schema","mysql","performance_schema","sys"}
        actual = [r[0] for r in rows]
        res["actual_databases"] = actual
        per_db = {}
        for db in actual:
            if db in SYS: continue
            d = {}
            rc, r, _ = _ssh_exec(
                "SELECT COUNT(*),COALESCE(SUM(data_length+index_length),0),COALESCE(SUM(table_rows),0),MIN(create_time),MAX(update_time) "
                f"FROM information_schema.tables WHERE table_schema='{db}'", host, user, pwd)
            if rc == 0 and r:
                nt, bt, ro, mc, mu = r[0][:5]
                d["n_tables"] = _to_int(nt); d["bytes"] = _to_int(bt); d["rows_est"] = _to_int(ro)
                d["freshness"] = {"min_create": mc, "max_update": mu}
            rc, r, _ = _ssh_exec(
                "SELECT table_name,engine,table_rows,(data_length+index_length),update_time "
                f"FROM information_schema.tables WHERE table_schema='{db}' "
                "ORDER BY (data_length+index_length) DESC LIMIT 10", host, user, pwd)
            if rc == 0:
                d["top10"] = [{"t": x[0], "eng": x[1], "rows": _to_int(x[2]), "b": _to_int(x[3]),
                               "upd": x[4] if len(x)>4 else None} for x in r]
            rc, r, _ = _ssh_exec(f"SELECT engine,COUNT(*) FROM information_schema.tables WHERE table_schema='{db}' GROUP BY engine",
                                 host, user, pwd)
            if rc == 0:
                d["engines"] = {x[0]: _to_int(x[1]) for x in r if x[0]}
            rc, r, _ = _ssh_exec(f"SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='{db}'",
                                 host, user, pwd)
            if rc == 0 and r: d["columns"] = _to_int(r[0][0])
            per_db[db] = d
        res["per_database"] = per_db
        res["status"] = "OK"
    except Exception as e:
        res["status"] = f"PROBE_FAIL:{type(e).__name__}"
        res["error"] = str(e)[:300]
    res["elapsed_s"] = round(time.monotonic()-t0, 3)
    return res

def _census_all_mysql():
    r = []
    with ThreadPoolExecutor(max_workers=8) as p:
        f2h = {p.submit(_cluster_census, c): c["host"] for c in MYSQL_CLUSTERS}
        for f in as_completed(f2h):
            x = f.result()
            print(f"  mysql[{f2h[f]}] → {x['status']} ({x['elapsed_s']}s)", flush=True)
            r.append(x)
    return r

def _rds_census():
    from openpyxl import load_workbook
    lines = Path(DIGICOW_CSV).read_text(encoding="utf-8-sig").splitlines()
    hdr = [h.strip() for h in lines[0].split(",")]; row = [c.strip() for c in lines[1].split(",")]
    cr = {h.lower().replace(" ","_"): v for h,v in zip(hdr,row)}
    ak, sk = cr["access_key_id"], cr["secret_access_key"]
    wb = load_workbook(DIGICOW_XLSX, data_only=True); ws = wb["Sheet1"]
    ca = sa = None
    for r in range(1, ws.max_row+1):
        v = ws.cell(row=r, column=1).value
        if not v: continue
        s = str(v).strip(); low = s.lower()
        if low.startswith("cluster arn:"): ca = s[len("cluster arn:"):].strip()
        elif low.startswith("secret arn:"): sa = s[len("secret arn:"):].strip()
    import boto3
    c = boto3.client("rds-data", region_name="eu-west-1", aws_access_key_id=ak, aws_secret_access_key=sk)
    def _n(f):
        if f.get("isNull"): return 0
        for k in ("longValue","doubleValue"):
            if k in f: return f[k]
        if "stringValue" in f:
            try: return int(f["stringValue"])
            except (ValueError, TypeError):
                try: return float(f["stringValue"])
                except (ValueError, TypeError): return f["stringValue"]
        return None
    out = {}
    for db in ("digicow_live","ndume"):
        d = {}
        r = c.execute_statement(resourceArn=ca, secretArn=sa, database=db,
            sql="SELECT COUNT(*),COALESCE(SUM(data_length+index_length),0),COALESCE(SUM(table_rows),0),MIN(create_time),MAX(update_time) "
                f"FROM information_schema.tables WHERE table_schema='{db}'")
        f = r.get("records",[[]])[0]
        d["n_tables"] = _n(f[0]); d["bytes"] = _n(f[1]); d["rows_est"] = _n(f[2])
        d["freshness"] = {"min_create": _n(f[3]), "max_update": _n(f[4])}
        r = c.execute_statement(resourceArn=ca, secretArn=sa, database=db,
            sql=f"SELECT table_name,engine,table_rows,(data_length+index_length),update_time FROM information_schema.tables WHERE table_schema='{db}' ORDER BY (data_length+index_length) DESC LIMIT 10")
        d["top10"] = [{"t":_n(x[0]),"eng":_n(x[1]),"rows":_n(x[2]),"b":_n(x[3]),"upd":_n(x[4])} for x in r.get("records",[])]
        r = c.execute_statement(resourceArn=ca, secretArn=sa, database=db,
            sql=f"SELECT engine,COUNT(*) FROM information_schema.tables WHERE table_schema='{db}' GROUP BY engine")
        d["engines"] = {_n(x[0]): _n(x[1]) for x in r.get("records",[])}
        r = c.execute_statement(resourceArn=ca, secretArn=sa, database=db,
            sql=f"SELECT COUNT(*) FROM information_schema.columns WHERE table_schema='{db}'")
        d["columns"] = _n(r.get("records",[[]])[0][0]) if r.get("records") else None
        out[db] = d
    return {"surface": "digicow_rds", "region": "eu-west-1", "status": "OK", "databases": out}

def _s3_boto():
    lines = Path(DIGICOW_CSV).read_text(encoding="utf-8-sig").splitlines()
    hdr = [h.strip() for h in lines[0].split(",")]; row = [c.strip() for c in lines[1].split(",")]
    cr = {h.lower().replace(" ","_"): v for h,v in zip(hdr,row)}
    import boto3
    return boto3.client("s3", region_name="eu-west-1",
                        aws_access_key_id=cr["access_key_id"],
                        aws_secret_access_key=cr["secret_access_key"])

def _list_audio():
    s3 = _s3_boto()
    p = s3.get_paginator("list_objects_v2")
    out = []
    for pg in p.paginate(Bucket=BUCKET, Prefix=PREFIX):
        for o in pg.get("Contents", []):
            out.append({"key": o["Key"], "size": o["Size"], "last_modified": o["LastModified"].isoformat()})
    return out

def _classify(pcm, sr):
    """Speech-vs-music heuristic from PCM bytes (numpy-only; no scipy)."""
    import numpy as np
    x = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
    if len(x) < sr:
        return {"label": "TOO_SHORT", "dur_s": round(len(x)/sr,3)}
    frame = int(0.025*sr); hop = int(0.010*sr); hop = max(1, hop)
    n = max(1, (len(x)-frame)//hop)
    zcr = np.zeros(n, dtype=np.float32); eng = np.zeros(n, dtype=np.float32)
    for i in range(n):
        fr = x[i*hop:i*hop+frame]
        zcr[i] = np.sum(np.diff(np.signbit(fr))) / max(1, len(fr))
        eng[i] = float(np.sqrt(np.mean(fr*fr)))
    mask = eng < 0.01
    silence = float(np.mean(mask))
    # Build sample-level mask matching x's length
    sample_mask = np.repeat(eng >= 0.01, hop)
    if len(sample_mask) < len(x):
        # pad with False (silence) at the tail
        sample_mask = np.concatenate([sample_mask, np.zeros(len(x) - len(sample_mask), dtype=bool)])
    elif len(sample_mask) > len(x):
        sample_mask = sample_mask[:len(x)]
    active = x[sample_mask] if len(eng) else x
    if len(active) < sr//2:
        return {"label": "MOSTLY_SILENCE", "silence": round(silence,4), "dur_s": round(len(x)/sr,3)}
    # Welch-like PSD via numpy: windowed segments, Hann window, rfft, average
    seglen = min(1024, len(active))
    hopseg = seglen // 2
    win = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(seglen) / (seglen - 1))
    win = win.astype(np.float32)
    winnorm = float(np.sum(win * win))
    psd_accum = np.zeros(seglen // 2 + 1, dtype=np.float32)
    nseg = 0
    for start in range(0, len(active) - seglen + 1, hopseg):
        seg = active[start:start + seglen] * win
        spec = np.fft.rfft(seg)
        psd_accum += (spec.real ** 2 + spec.imag ** 2) / (sr * winnorm)
        nseg += 1
    if nseg == 0:
        return {"label": "MOSTLY_SILENCE", "silence": round(silence,4), "dur_s": round(len(x)/sr,3)}
    psd = np.maximum(psd_accum / nseg, 1e-12)
    flat = float(np.exp(np.mean(np.log(psd))) / np.mean(psd))
    zm = float(np.mean(zcr[~mask])) if np.any(~mask) else 0.0
    zs = float(np.std(zcr[~mask])) if np.any(~mask) else 0.0
    if flat > 0.35:                        label = "music_or_noise"
    elif zs > 0.05 and 0.02 < zm < 0.15:   label = "speech"
    elif flat < 0.10 and zm < 0.05:        label = "music"
    else:                                  label = "speech_probable" if zs > 0.03 else "music_probable"
    return {"label": label, "zcr_mean": round(zm,4), "zcr_std": round(zs,4),
            "flatness": round(flat,4), "silence": round(silence,4), "dur_s": round(len(x)/sr,3)}

def _one_audio(rec):
    key, size = rec["key"], rec["size"]
    r = {"key": key, "size": size, "last_modified": rec["last_modified"]}
    t0 = time.monotonic()
    try:
        s3 = _s3_boto()
        end = min(size-1, 524287)
        obj = s3.get_object(Bucket=BUCKET, Key=key, Range=f"bytes=0-{end}")
        data = obj["Body"].read()
    except Exception as e:
        r["status"] = f"S3_FAIL:{type(e).__name__}"; r["error"] = str(e)[:200]; return r
    ext = key.rsplit(".",1)[-1] if "." in key else "bin"
    with tempfile.NamedTemporaryFile(suffix="."+ext, delete=False) as tf:
        tf.write(data); tmp = tf.name
    try:
        p = subprocess.run(["ffprobe","-v","quiet","-print_format","json","-show_format","-show_streams",tmp],
                           capture_output=True, text=True, timeout=15)
        if p.returncode == 0 and p.stdout:
            probe = json.loads(p.stdout)
            fmt = probe.get("format",{})
            aud = [s for s in probe.get("streams",[]) if s.get("codec_type")=="audio"]
            vid = [s for s in probe.get("streams",[]) if s.get("codec_type")=="video"]
            r["ffprobe"] = {"fmt": fmt.get("format_name"),
                "dur_s": float(fmt.get("duration",0) or 0),
                "bitrate": int(fmt.get("bit_rate",0) or 0),
                "n_audio": len(aud), "n_video": len(vid),
                "codecs": [s.get("codec_name") for s in aud],
                "sr": [int(s.get("sample_rate",0) or 0) for s in aud],
                "ch": [int(s.get("channels",0) or 0) for s in aud]}
            if aud and r["ffprobe"]["dur_s"] > 0.5:
                d = subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-nostdin",
                                    "-i",tmp,"-t","5","-ac","1","-ar","8000","-f","s16le","pipe:1"],
                                   capture_output=True, timeout=20)
                if d.returncode == 0 and d.stdout:
                    r["cls"] = _classify(d.stdout, 8000)
                else:
                    r["cls"] = {"label": "DECODE_FAIL"}
            else:
                r["cls"] = {"label": "NO_AUDIO"}
            r["status"] = "OK"
        else:
            r["status"] = "FFPROBE_FAIL"; r["err"] = p.stderr[:200]
    finally:
        os.unlink(tmp)
    r["elapsed_s"] = round(time.monotonic()-t0, 3)
    return r

def _s3_audio_census():
    objs = _list_audio()
    print(f"  s3 audio: {len(objs)} objects", flush=True)
    results = []; t0 = time.monotonic()
    with ProcessPoolExecutor(max_workers=8) as pool:
        for i, r in enumerate(pool.map(_one_audio, objs, chunksize=8), 1):
            results.append(r)
            if i % 100 == 0:
                elapsed = time.monotonic() - t0
                rate = i/elapsed if elapsed else 0
                eta = (len(objs)-i)/rate if rate else 0
                print(f"    ... {i}/{len(objs)} rate={rate:.1f}/s eta={eta:.0f}s", flush=True)
    labels = {}; speech_h = music_h = total_h = 0.0
    codec_ct = {}; ext_ct = {}; decode_fail = 0; s3_fail = 0
    for r in results:
        ext = r["key"].rsplit(".",1)[-1].lower() if "." in r["key"] else "(none)"
        ext_ct[ext] = ext_ct.get(ext, 0) + 1
        if r.get("status") != "OK":
            if r.get("status","").startswith("S3_"): s3_fail += 1
            continue
        f = r.get("ffprobe", {}); cs = r.get("cls", {})
        lab = cs.get("label","?"); labels[lab] = labels.get(lab, 0) + 1
        dh = f.get("dur_s", 0)/3600.0; total_h += dh
        if lab in ("speech","speech_probable"): speech_h += dh
        elif lab in ("music","music_probable","music_or_noise"): music_h += dh
        for cx in f.get("codecs", []):
            if cx: codec_ct[cx] = codec_ct.get(cx, 0) + 1
        if cs.get("label") == "DECODE_FAIL": decode_fail += 1
    return {"surface": "digicow_s3_audio", "status": "OK",
            "bucket": BUCKET, "prefix": PREFIX,
            "total_objects": len(results),
            "elapsed_s": round(time.monotonic()-t0, 2),
            "aggregate": {"labels": labels, "speech_h": round(speech_h,2),
                          "music_h": round(music_h,2), "total_h": round(total_h,2),
                          "codecs": codec_ct, "extensions": ext_ct,
                          "decode_fail": decode_fail, "s3_fail": s3_fail},
            "per_file": results}

def _nas_probe():
    import paramiko
    s = paramiko.SSHClient(); s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        s.connect(JUMP["host"], 22, username=JUMP["user"], password=JUMP["password"],
                  timeout=8, look_for_keys=False, allow_agent=False, banner_timeout=8)
        probes = {}
        for port, label in [(5000,"dsm_http"),(5001,"dsm_https"),(445,"smb"),(139,"nb"),(22,"ssh"),(2049,"nfs")]:
            _, o, _ = s.exec_command(f"timeout 3 bash -c 'echo > /dev/tcp/{NAS['host']}/{port}' && echo OPEN || echo CLOSED", timeout=6)
            probes[label] = o.read().decode().strip()
        _, o, _ = s.exec_command("which smbclient nmap", timeout=3)
        tools = o.read().decode().strip()
        s.close()
        return {"surface": "nas_cifs", "status": "PROBED", "port_probes_from_jump": probes,
                "jump_tools": tools,
                "note": "Deep NAS walk deferred behind budget this pass."}
    except Exception as e:
        return {"surface": "nas_cifs", "status": f"JUMP_ERR:{type(e).__name__}", "err": str(e)[:200]}

def _obs_retry():
    return {"surface": "huawei_obs", "status": "DEFERRED_THIS_PASS",
            "reason": "Fresh drop has no new OBS AK/SK; retry against banked HPUA keys deferred (recorded)",
            "desk_queue_ref": "DQ-05 (unchanged this pass)"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface", default="all",
                    choices=["all","mysql","rds","s3_audio","nas","obs"])
    ap.add_argument("--out-json", default=None); ap.add_argument("--out-md", default=None)
    args = ap.parse_args()
    _load_fresh_creds()
    c = {"census_ts_utc": TS, "canon_anchor": CANON_ANCHOR,
         "owner_directive_verbatim": OWNER_DIRECTIVE,
         "compute": {"cpu_cores": 8, "gpu": "none", "mem_gb": 31,
                     "mysql_workers": 8, "s3_audio_workers": 8, "rds_workers": 1},
         "cred_shape": _cred_shape(), "surfaces": {}}
    print(f"[census-2] fresh creds sha256: {FRESH_SHA}", flush=True)
    print(f"[census-2] {len(MYSQL_CLUSTERS)} mysql clusters detected", flush=True)

    if args.surface in ("all","mysql"):
        print("[census-2] mysql pool starting...", flush=True)
        c["surfaces"]["mysql"] = _census_all_mysql()
    if args.surface in ("all","rds"):
        print("[census-2] rds...", flush=True)
        try: c["surfaces"]["digicow_rds"] = _rds_census()
        except Exception as e: c["surfaces"]["digicow_rds"] = {"status": f"FAIL:{type(e).__name__}", "err": str(e)[:200]}
    if args.surface in ("all","s3_audio"):
        print("[census-2] s3 audio pool starting...", flush=True)
        try: c["surfaces"]["digicow_s3_audio"] = _s3_audio_census()
        except Exception as e: c["surfaces"]["digicow_s3_audio"] = {"status": f"FAIL:{type(e).__name__}", "err": str(e)[:200]}
    if args.surface in ("all","nas"):
        print("[census-2] nas probe...", flush=True)
        c["surfaces"]["nas_cifs"] = _nas_probe()
    if args.surface in ("all","obs"):
        print("[census-2] obs retry...", flush=True)
        c["surfaces"]["huawei_obs"] = _obs_retry()

    out_json = Path(args.out_json or f"/app/assessment_workspace/phase0/connectivity_receipts/{TS}_ESTATE_CENSUS_v2.json")
    out_md = Path(args.out_md or f"/app/assessment_workspace/STATE/notes/ESTATE_CENSUS_v2_{TS}.md")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(c, indent=2, default=str))
    md = [f"# ESTATE_CENSUS_v2 · {TS}", "",
          f"**Canon anchor**: {CANON_ANCHOR['primary']}", "",
          f"**Owner directive**: {OWNER_DIRECTIVE}", "",
          "## Compute", f"- CPU cores: 8 · GPU: none · RAM: 31 GB", "",
          "## Cred shape (SHAPE-ONLY)", "```json", json.dumps(c["cred_shape"], indent=2), "```", "",
          "## Surfaces"]
    for name, s in c["surfaces"].items():
        md.append(f"### {name}")
        md.append("```json")
        if isinstance(s, dict) and "per_file" in s:
            md.append(json.dumps({k: v for k,v in s.items() if k != "per_file"}, indent=2, default=str))
        else:
            md.append(json.dumps(s, indent=2, default=str))
        md.append("```"); md.append("")
    out_md.write_text("\n".join(md))
    print(f"\ncensus JSON: {out_json}\ncensus MD  : {out_md}")

if __name__ == "__main__":
    main()
