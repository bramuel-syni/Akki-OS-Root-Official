"""RDS API deeper probe — list users, DB names, backup config, and instance detail (endpoint FQDN)."""
import json, csv
CRED = "/app/backend/estate_keys/data_sources/huawei_credentials.csv"
with open(CRED) as f:
    rows = list(csv.reader(f))
hdr = [h.lstrip("\ufeff").strip() for h in rows[0]]
d = dict(zip(hdr, rows[1]))
AK, SK = d["Access Key Id"], d["Secret Access Key"]

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions as hw_ex
from huaweicloudsdkrds.v3 import (
    RdsClient, ListInstancesRequest, ListDatabasesRequest,
    ListDbUsersRequest, ShowBackupPolicyRequest, ShowDomainNameRequest,
    ShowAuditlogPolicyRequest,
)
from huaweicloudsdkrds.v3.region.rds_region import RdsRegion

targets = [
    ("af-south-1", "012de8d88d734339a2f50278128e0062in01", "RDS-INTERACTIONS"),
    ("af-south-1", "f5f29903117245469acd1c9abeeac2acin01", "Weego_and_marketing-analytics"),
    ("af-south-1", "87629ec62e2e492a8f3aa70b8c492df1in01", "rds-shikisha"),
    ("af-south-1", "01a1ecfa0fe14679bc8ab80f8b9b8b24in01", "weego-replica-d536"),
    ("ap-southeast-1", "2ce731854be043aaaaa9363d0a1b6585in03", "rms-ai-pg"),
]

def call(client, fn, *a, **kw):
    try:
        return {"ok": True, "resp": fn(*a, **kw)}
    except hw_ex.ClientRequestException as e:
        return {"ok": False, "err": f"{e.status_code}:{e.error_code}:{getattr(e,'error_msg','')[:200]}"}
    except Exception as e:
        return {"ok": False, "err": f"{type(e).__name__}:{str(e)[:200]}"}

out = {}
for region, iid, name in targets:
    print(f"\n== {name} ({iid}) @ {region} ==")
    creds = BasicCredentials(AK, SK)
    client = RdsClient.new_builder().with_credentials(creds).with_region(RdsRegion.value_of(region)).build()

    # 1. instance detail via ListInstances(id=iid)
    r = call(client, client.list_instances, ListInstancesRequest(id=iid))
    entry = {"instance_detail": None, "databases": None, "db_users": None, "backup_policy": None, "audit_policy": None, "endpoints": None}
    if r["ok"] and (r["resp"].instances or []):
        inst = r["resp"].instances[0]
        entry["instance_detail"] = {
            "name": inst.name, "status": inst.status,
            "engine": (inst.datastore.type + " " + inst.datastore.version) if inst.datastore else None,
            "port": inst.port,
            "private_dns_names": getattr(inst, "private_dns_names", None),
            "public_ips": inst.public_ips,
            "private_ips": inst.private_ips,
            "vpc_id": inst.vpc_id, "subnet_id": inst.subnet_id, "security_group_id": inst.security_group_id,
            "db_user_name": getattr(inst, "db_user_name", None),
            "flavor": inst.flavor_ref,
            "created": inst.created,
            "az": getattr(inst, "availability_zone", None) or getattr(inst, "az_code", None),
            "az_code_ha": getattr(inst, "az_code_ha", None),
        }
        print(f"  detail_ok: engine={entry['instance_detail']['engine']} db_root_user={entry['instance_detail']['db_user_name']}")
        print(f"    private_dns={entry['instance_detail']['private_dns_names']}")
    else:
        print(f"  detail_err: {r.get('err','no instances returned')}")
        entry["instance_detail_err"] = r.get("err")

    # 1b. public endpoint FQDN
    r = call(client, client.show_domain_name, ShowDomainNameRequest(instance_id=iid, dns_type="public"))
    if r["ok"]:
        entry["endpoints"] = {"public_fqdn": r["resp"].public_domain_name if hasattr(r["resp"], "public_domain_name") else None}
        print(f"  public_fqdn: {entry['endpoints']}")
    else:
        print(f"  fqdn_err: {r['err']}")

    # 2. databases (MySQL) — PG uses different endpoints
    is_mysql = "mysql" in (entry.get("instance_detail") or {}).get("engine", "").lower() if entry.get("instance_detail") else True
    if is_mysql:
        r = call(client, client.list_databases, ListDatabasesRequest(instance_id=iid, page=1, limit=100))
        if r["ok"]:
            dbs = [{"name": db.name, "charset": db.character_set} for db in (r["resp"].databases or [])]
            entry["databases"] = dbs
            print(f"  databases_ok: n={len(dbs)}: {[d['name'] for d in dbs[:12]]}{'...' if len(dbs)>12 else ''}")
        else:
            print(f"  databases_err: {r['err']}")
            entry["databases_err"] = r["err"]

        r = call(client, client.list_db_users, ListDbUsersRequest(instance_id=iid, page=1, limit=100))
        if r["ok"]:
            users = [u.name for u in (r["resp"].users or [])]
            entry["db_users"] = users
            print(f"  db_users_ok: n={len(users)}: {users[:12]}{'...' if len(users)>12 else ''}")
        else:
            print(f"  db_users_err: {r['err']}")
            entry["db_users_err"] = r["err"]

    # 3. backup policy
    r = call(client, client.show_backup_policy, ShowBackupPolicyRequest(instance_id=iid))
    if r["ok"]:
        bp = r["resp"].backup_policy
        entry["backup_policy"] = {
            "keep_days": bp.keep_days, "start_time": bp.start_time, "period": bp.period,
        }
        print(f"  backup_ok: keep_days={bp.keep_days} start={bp.start_time} period={bp.period}")
    else:
        print(f"  backup_err: {r['err']}")

    out[name] = entry

with open("/app/assessment_workspace/tools/_scratch/rds_deep.json", "w") as f:
    json.dump(out, f, indent=2, default=str)

print("\nSaved -> _scratch/rds_deep.json")
