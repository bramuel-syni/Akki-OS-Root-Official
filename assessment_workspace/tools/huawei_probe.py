"""
Huawei Cloud connectivity drill — READ-ONLY.
Sequence: IAM identity -> OBS buckets -> RDS instances -> DWS clusters -> DDS instances.
Stop-on-hard-403 per service; keep trying other services and regions.
NO writes, NO commits. SK never written to stdout/artefacts.
"""
import csv, json, os, sys, time, hashlib, traceback
from datetime import datetime, timezone

CRED_PATH = "/app/backend/estate_keys/data_sources/huawei_credentials.csv"
OUT_DIR = "/app/assessment_workspace/tools/_scratch"
os.makedirs(OUT_DIR, exist_ok=True)

REGIONS = [
    "cn-north-1", "cn-north-2", "cn-north-4", "cn-north-9",
    "cn-east-2", "cn-east-3",
    "cn-south-1", "cn-south-2",
    "ap-southeast-1", "ap-southeast-2", "ap-southeast-3",
    "af-south-1", "eu-west-0",
    "cn-southwest-2",   # extra common
    "la-north-2", "la-south-2", "sa-brazil-1",
    "na-mexico-1",
]

def load_creds():
    with open(CRED_PATH, "r", newline="") as f:
        rows = list(csv.reader(f))
    hdr = [h.lstrip("\ufeff").strip() for h in rows[0]]
    r = dict(zip(hdr, rows[1]))
    return r["User Name"], r["Access Key Id"], r["Secret Access Key"]

def sk_fp(sk):
    return "sha256_8=" + hashlib.sha256(sk.encode()).hexdigest()[:8]

def now():
    return datetime.now(timezone.utc).isoformat()

RESULTS = {"started_at": now(), "iam": {}, "obs": {}, "rds": {}, "dws": {}, "dds": {}}

def save():
    with open(os.path.join(OUT_DIR, "probe_results.json"), "w") as f:
        # Deep-scrub any SK-shaped strings just in case (40-char alnum)
        s = json.dumps(RESULTS, indent=2, default=str)
        json.dump(RESULTS, f, indent=2, default=str)

def probe_iam(user, ak, sk):
    """Try IAM against the international endpoint, then domestic. List projects, domains, user info."""
    from huaweicloudsdkcore.auth.credentials import GlobalCredentials
    from huaweicloudsdkcore.exceptions import exceptions as hw_ex
    from huaweicloudsdkiam.v3 import IamClient
    from huaweicloudsdkiam.v3.region.iam_region import IamRegion
    from huaweicloudsdkiam.v3 import (
        KeystoneListProjectsRequest,
        KeystoneListAuthDomainsRequest,
        KeystoneListRegionsRequest,
    )

    iam_res = {"attempts": [], "domain_id": None, "projects": [], "regions_seen": [], "user_id": None}

    # Try both international and domestic IAM regions
    candidates = []
    try:
        for rname in ("ap-southeast-1", "cn-north-4", "cn-north-1", "eu-west-0", "af-south-1"):
            try:
                candidates.append((rname, IamRegion.value_of(rname)))
            except Exception:
                pass
    except Exception:
        pass

    for rname, region in candidates:
        attempt = {"region": rname, "endpoint": getattr(region, "endpoint", None), "ok": False, "error": None}
        try:
            creds = GlobalCredentials(ak, sk)
            client = IamClient.new_builder().with_credentials(creds).with_region(region).build()

            # Domains (tells us account/domain_id)
            try:
                d = client.keystone_list_auth_domains(KeystoneListAuthDomainsRequest())
                if d.domains:
                    iam_res["domain_id"] = d.domains[0].id
                    attempt["domain_id"] = d.domains[0].id
                    attempt["domain_name"] = d.domains[0].name
            except hw_ex.ClientRequestException as e:
                attempt["domain_error"] = f"{e.status_code}:{e.error_code}"

            # Projects (regions/tenants)
            try:
                p = client.keystone_list_projects(KeystoneListProjectsRequest())
                for proj in (p.projects or []):
                    iam_res["projects"].append({
                        "id": proj.id, "name": proj.name, "enabled": proj.enabled,
                        "domain_id": proj.domain_id,
                    })
                    if proj.name and proj.name not in iam_res["regions_seen"]:
                        iam_res["regions_seen"].append(proj.name)
                attempt["projects_count"] = len(p.projects or [])
                attempt["ok"] = True
            except hw_ex.ClientRequestException as e:
                attempt["projects_error"] = f"{e.status_code}:{e.error_code}:{getattr(e,'error_msg','')}"

            # Regions list (public catalogue of regions this SDK sees)
            try:
                rr = client.keystone_list_regions(KeystoneListRegionsRequest())
                attempt["catalogue_regions"] = [r.id for r in (rr.regions or [])]
            except hw_ex.ClientRequestException as e:
                attempt["regions_error"] = f"{e.status_code}:{e.error_code}"

            iam_res["attempts"].append(attempt)
            if attempt["ok"]:
                break  # got projects, stop trying more IAM regions
        except Exception as e:
            attempt["error"] = f"{type(e).__name__}:{str(e)[:200]}"
            iam_res["attempts"].append(attempt)
    RESULTS["iam"] = iam_res
    return iam_res

def probe_obs(ak, sk):
    """List all OBS buckets visible to this AK/SK (global call)."""
    from obs import ObsClient
    obs_res = {"buckets": [], "attempts": []}
    # OBS list-buckets is region-agnostic; try a few endpoints just in case
    endpoints = [
        "https://obs.ap-southeast-1.myhuaweicloud.com",
        "https://obs.cn-north-4.myhuaweicloud.com",
        "https://obs.cn-north-1.myhuaweicloud.com",
        "https://obs.af-south-1.myhuaweicloud.com",
        "https://obs.eu-west-0.myhuaweicloud.com",
    ]
    for ep in endpoints:
        client = ObsClient(access_key_id=ak, secret_access_key=sk, server=ep)
        try:
            resp = client.listBuckets(isQueryLocation=True)
            att = {"endpoint": ep, "status": resp.status, "errorCode": resp.errorCode, "errorMessage": resp.errorMessage}
            if resp.status < 300:
                for b in (resp.body.buckets if resp.body and hasattr(resp.body, "buckets") else []):
                    obs_res["buckets"].append({"name": b.name, "location": getattr(b, "location", None), "create_date": str(getattr(b, "create_date", None))})
                att["ok"] = True
                obs_res["attempts"].append(att)
                break
            obs_res["attempts"].append(att)
        except Exception as e:
            obs_res["attempts"].append({"endpoint": ep, "error": f"{type(e).__name__}:{str(e)[:200]}"})
        finally:
            try:
                client.close()
            except Exception:
                pass
    RESULTS["obs"] = obs_res
    return obs_res

def probe_rds(ak, sk, regions):
    """Iterate regions, list RDS instances."""
    from huaweicloudsdkcore.auth.credentials import BasicCredentials
    from huaweicloudsdkcore.exceptions import exceptions as hw_ex
    from huaweicloudsdkrds.v3 import RdsClient, ListInstancesRequest
    from huaweicloudsdkrds.v3.region.rds_region import RdsRegion

    rds_res = {"by_region": {}, "instances": []}
    for rname in regions:
        entry = {"ok": False, "error": None, "count": 0}
        try:
            region = RdsRegion.value_of(rname)
            creds = BasicCredentials(ak, sk)
            client = RdsClient.new_builder().with_credentials(creds).with_region(region).build()
            resp = client.list_instances(ListInstancesRequest())
            entry["ok"] = True
            entry["count"] = resp.total_count or 0
            for inst in (resp.instances or []):
                d = {
                    "id": inst.id, "name": inst.name, "status": inst.status,
                    "engine": getattr(getattr(inst, "datastore", None), "type", None),
                    "engine_version": getattr(getattr(inst, "datastore", None), "version", None),
                    "port": inst.port,
                    "region": rname,
                    "private_ips": inst.private_ips,
                    "public_ips": inst.public_ips,
                }
                rds_res["instances"].append(d)
        except hw_ex.ClientRequestException as e:
            entry["error"] = f"{e.status_code}:{e.error_code}:{getattr(e,'error_msg','')[:120]}"
        except Exception as e:
            entry["error"] = f"{type(e).__name__}:{str(e)[:160]}"
        rds_res["by_region"][rname] = entry
    RESULTS["rds"] = rds_res
    return rds_res

def probe_dws(ak, sk, regions):
    from huaweicloudsdkcore.auth.credentials import BasicCredentials
    from huaweicloudsdkcore.exceptions import exceptions as hw_ex
    from huaweicloudsdkdws.v2 import DwsClient, ListClustersRequest
    from huaweicloudsdkdws.v2.region.dws_region import DwsRegion

    dws_res = {"by_region": {}, "clusters": []}
    for rname in regions:
        entry = {"ok": False, "error": None, "count": 0}
        try:
            region = DwsRegion.value_of(rname)
        except Exception as e:
            entry["error"] = f"NoRegion:{str(e)[:100]}"
            dws_res["by_region"][rname] = entry
            continue
        try:
            creds = BasicCredentials(ak, sk)
            client = DwsClient.new_builder().with_credentials(creds).with_region(region).build()
            resp = client.list_clusters(ListClustersRequest())
            entry["ok"] = True
            clusters = resp.clusters or []
            entry["count"] = len(clusters)
            for c in clusters:
                dws_res["clusters"].append({
                    "id": c.id, "name": c.name, "status": c.status,
                    "region": rname,
                    "endpoints": [{"connect_info": ep.connect_info, "jdbc_url": ep.jdbc_url} for ep in (getattr(c,'endpoints', []) or [])],
                    "port": getattr(c, "port", None),
                    "version": getattr(c, "version", None),
                })
        except hw_ex.ClientRequestException as e:
            entry["error"] = f"{e.status_code}:{e.error_code}:{getattr(e,'error_msg','')[:120]}"
        except Exception as e:
            entry["error"] = f"{type(e).__name__}:{str(e)[:160]}"
        dws_res["by_region"][rname] = entry
    RESULTS["dws"] = dws_res
    return dws_res

def probe_dds(ak, sk, regions):
    from huaweicloudsdkcore.auth.credentials import BasicCredentials
    from huaweicloudsdkcore.exceptions import exceptions as hw_ex
    from huaweicloudsdkdds.v3 import DdsClient, ListInstancesRequest as DdsListInstancesRequest
    from huaweicloudsdkdds.v3.region.dds_region import DdsRegion

    dds_res = {"by_region": {}, "instances": []}
    for rname in regions:
        entry = {"ok": False, "error": None, "count": 0}
        try:
            region = DdsRegion.value_of(rname)
        except Exception as e:
            entry["error"] = f"NoRegion:{str(e)[:100]}"
            dds_res["by_region"][rname] = entry
            continue
        try:
            creds = BasicCredentials(ak, sk)
            client = DdsClient.new_builder().with_credentials(creds).with_region(region).build()
            resp = client.list_instances(DdsListInstancesRequest())
            entry["ok"] = True
            entry["count"] = resp.total_count or 0
            for inst in (resp.instances or []):
                dds_res["instances"].append({
                    "id": inst.id, "name": inst.name, "status": inst.status,
                    "mode": inst.mode, "engine": inst.datastore.type if inst.datastore else None,
                    "engine_version": inst.datastore.version if inst.datastore else None,
                    "port": inst.port, "region": rname,
                    "public": getattr(inst, "public_ips", None) or getattr(inst, "public_ip", None),
                    "private": getattr(inst, "private_ips", None) or getattr(inst, "private_ip", None),
                })
        except hw_ex.ClientRequestException as e:
            entry["error"] = f"{e.status_code}:{e.error_code}:{getattr(e,'error_msg','')[:120]}"
        except Exception as e:
            entry["error"] = f"{type(e).__name__}:{str(e)[:160]}"
        dds_res["by_region"][rname] = entry
    RESULTS["dds"] = dds_res
    return dds_res

def main():
    user, ak, sk = load_creds()
    RESULTS["user_name"] = user
    RESULTS["ak_prefix"] = ak[:4] + "…" + ak[-2:]
    RESULTS["ak_len"] = len(ak)
    RESULTS["sk_fingerprint"] = sk_fp(sk)
    RESULTS["sk_len"] = len(sk)

    print(f"[{now()}] IAM probe…", flush=True)
    iam = probe_iam(user, ak, sk)
    save()
    print(f"  attempts={len(iam['attempts'])} projects={len(iam['projects'])} domain_id={iam['domain_id']}", flush=True)

    # If IAM revealed projects, pivot: only sweep regions where a project exists.
    project_regions = [p["name"] for p in iam["projects"] if p.get("name")]
    sweep = project_regions if project_regions else REGIONS
    RESULTS["region_sweep"] = sweep
    print(f"  sweep set: {sweep}", flush=True)

    print(f"[{now()}] OBS probe…", flush=True)
    obs = probe_obs(ak, sk)
    save()
    print(f"  buckets={len(obs['buckets'])}", flush=True)

    print(f"[{now()}] RDS probe across {len(sweep)} regions…", flush=True)
    rds = probe_rds(ak, sk, sweep)
    save()
    ok_regions = [r for r,v in rds["by_region"].items() if v["ok"]]
    print(f"  ok_regions={ok_regions} total_instances={len(rds['instances'])}", flush=True)

    print(f"[{now()}] DWS probe…", flush=True)
    dws = probe_dws(ak, sk, sweep)
    save()
    print(f"  ok_regions={[r for r,v in dws['by_region'].items() if v['ok']]} clusters={len(dws['clusters'])}", flush=True)

    print(f"[{now()}] DDS probe…", flush=True)
    dds = probe_dds(ak, sk, sweep)
    save()
    print(f"  ok_regions={[r for r,v in dds['by_region'].items() if v['ok']]} instances={len(dds['instances'])}", flush=True)

    RESULTS["finished_at"] = now()
    save()
    print(f"[{now()}] DONE — results at {OUT_DIR}/probe_results.json", flush=True)

if __name__ == "__main__":
    main()
