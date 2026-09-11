"""Billing config probe — RDS charge_info + EIP bandwidth billing + data volume estimate.
Read-only. No writes. No commits.
"""
import csv, json, hashlib, pymysql
from datetime import datetime, timezone

CRED_HW = "/app/backend/estate_keys/data_sources/huawei_credentials.csv"
CRED_DB = "/app/backend/estate_keys/data_sources/db_credentials.csv"

with open(CRED_HW) as f:
    rows = list(csv.reader(f))
hdr = [h.lstrip("\ufeff").strip() for h in rows[0]]
d = dict(zip(hdr, rows[1]))
AK, SK = d["Access Key Id"], d["Secret Access Key"]

from huaweicloudsdkcore.auth.credentials import BasicCredentials, GlobalCredentials
from huaweicloudsdkcore.exceptions import exceptions as hw_ex
from huaweicloudsdkrds.v3 import RdsClient, ListInstancesRequest as RdsListInstancesRequest
from huaweicloudsdkrds.v3.region.rds_region import RdsRegion
from huaweicloudsdkeip.v2 import EipClient, ListPublicipsRequest, ListBandwidthsRequest
from huaweicloudsdkeip.v2.region.eip_region import EipRegion

RESULTS = {"ts": datetime.now(timezone.utc).isoformat(), "domain_id": "3f9d29266af74046bfb637cabb995c39"}

# --- Part 1: RDS charge_info per known-active regions ---
print("=== RDS charge_info (2 regions with known instances) ===")
rds_summary = []
for region in ("af-south-1", "ap-southeast-1"):
    print(f"\n[{region}]")
    creds = BasicCredentials(AK, SK)
    client = RdsClient.new_builder().with_credentials(creds).with_region(RdsRegion.value_of(region)).build()
    try:
        resp = client.list_instances(RdsListInstancesRequest())
        for inst in (resp.instances or []):
            ci = getattr(inst, "charge_info", None)
            row = {
                "name": inst.name, "id": inst.id, "region": region,
                "engine": f"{inst.datastore.type} {inst.datastore.version}" if inst.datastore else None,
                "flavor": inst.flavor_ref,
                "charge_mode": getattr(ci, "charge_mode", None) if ci else None,
                "period_type": getattr(ci, "period_type", None) if ci else None,
                "period_num": getattr(ci, "period_num", None) if ci else None,
                "is_auto_renew": getattr(ci, "is_auto_renew", None) if ci else None,
                "public_ips": inst.public_ips,
                "private_ips": inst.private_ips,
                "created": inst.created,
            }
            rds_summary.append(row)
            print(f"  {inst.name:40s}  flavor={inst.flavor_ref:30s} charge_mode={row['charge_mode']} period={row['period_type']} public_ips={inst.public_ips}")
    except hw_ex.ClientRequestException as e:
        print(f"  ERR: {e.status_code}:{e.error_code}:{e.error_msg}")

RESULTS["rds"] = rds_summary

# --- Part 2: EIP billing per region + per public IP ---
print("\n\n=== EIP billing (list_publicips + list_bandwidths) ===")
eip_summary = {"by_region": {}, "our_target_ips": {}}
target_ips = set()
for r in rds_summary:
    for ip in (r["public_ips"] or []):
        target_ips.add(ip)
target_ips.update({"110.238.76.159", "203.123.86.10", "159.138.164.93"})  # from DB creds CSV

for region in ("af-south-1", "ap-southeast-1"):
    print(f"\n[{region}]")
    try:
        eregion = EipRegion.value_of(region)
    except Exception as e:
        print(f"  no EIP region: {e}")
        continue
    creds = BasicCredentials(AK, SK)
    eclient = EipClient.new_builder().with_credentials(creds).with_region(eregion).build()

    # 2a. list publicips
    try:
        resp = eclient.list_publicips(ListPublicipsRequest(limit=500))
        pips = resp.publicips or []
        eip_summary["by_region"][region] = {"publicip_count": len(pips), "publicips_matched_targets": []}
        print(f"  publicips: {len(pips)}")
        for pip in pips:
            ipaddr = pip.public_ip_address
            if ipaddr in target_ips:
                pip_row = {
                    "public_ip": ipaddr,
                    "id": pip.id,
                    "type": pip.type,
                    "status": pip.status,
                    "bandwidth_id": pip.bandwidth_id,
                    "bandwidth_size": pip.bandwidth_size,
                    "bandwidth_share_type": pip.bandwidth_share_type,
                    "port_id": pip.port_id,
                    "tenant_id": pip.tenant_id,
                    "profile": getattr(pip, "profile", None),
                    "create_time": pip.create_time,
                }
                eip_summary["our_target_ips"][ipaddr] = pip_row
                eip_summary["by_region"][region]["publicips_matched_targets"].append(ipaddr)
                print(f"    MATCH target {ipaddr}: bw_id={pip.bandwidth_id} bw_size={pip.bandwidth_size}Mbps share_type={pip.bandwidth_share_type}")
    except hw_ex.ClientRequestException as e:
        print(f"  publicips ERR: {e.status_code}:{e.error_code}:{e.error_msg[:120]}")

    # 2b. list bandwidths
    try:
        resp = eclient.list_bandwidths(ListBandwidthsRequest(limit=500))
        bws = resp.bandwidths or []
        eip_summary["by_region"][region]["bandwidth_count"] = len(bws)
        # index by id
        bw_by_id = {bw.id: bw for bw in bws}
        # attach billing details for our target IPs
        for ip, row in eip_summary["our_target_ips"].items():
            bw = bw_by_id.get(row.get("bandwidth_id"))
            if bw:
                row["bandwidth_charge_mode"] = getattr(bw, "charge_mode", None)  # "bandwidth" | "traffic"
                row["bandwidth_billing_info"] = getattr(bw, "billing_info", None)
                row["bandwidth_name"] = bw.name
                row["bandwidth_size_final"] = bw.size
                row["bandwidth_publicip_info"] = [p.publicip_address for p in (bw.publicip_info or [])] if getattr(bw, "publicip_info", None) else None
                print(f"    bw for {ip}: charge_mode={row['bandwidth_charge_mode']} size={bw.size}Mbps billing_info={row['bandwidth_billing_info']}")
    except hw_ex.ClientRequestException as e:
        print(f"  bandwidths ERR: {e.status_code}:{e.error_code}:{e.error_msg[:120]}")

RESULTS["eip"] = eip_summary

# --- Part 3: Data volume estimate on the ONE reachable live host ---
print("\n\n=== Data volume (information_schema on 110.238.76.159) ===")
# get pw
with open(CRED_DB) as f:
    for r in csv.reader(f):
        if len(r) >= 4 and r[1] == "110.238.76.159":
            USER, PW = r[2], r[3]
            break
conn = pymysql.connect(host="110.238.76.159", port=3306, user=USER, password=PW, connect_timeout=10, read_timeout=30)
with conn.cursor() as cur:
    # total per schema
    cur.execute("""
        SELECT table_schema,
               COUNT(*) AS tables,
               ROUND(SUM(data_length)/1024/1024, 1)   AS data_mb,
               ROUND(SUM(index_length)/1024/1024, 1)  AS index_mb,
               ROUND(SUM(data_length+index_length)/1024/1024, 1) AS total_mb,
               ROUND(SUM(data_length+index_length)/1024/1024/1024, 3) AS total_gb
          FROM information_schema.TABLES
         WHERE table_schema NOT IN ('information_schema','mysql','performance_schema','sys')
         GROUP BY table_schema
         ORDER BY total_mb DESC;
    """)
    per_db = []
    total_gb = 0.0
    for row in cur.fetchall():
        db, tbl_n, data_mb, index_mb, total_mb, total_gb_row = row
        per_db.append({"db": db, "tables": tbl_n, "data_mb": float(data_mb or 0),
                       "index_mb": float(index_mb or 0), "total_mb": float(total_mb or 0),
                       "total_gb": float(total_gb_row or 0)})
        total_gb += float(total_gb_row or 0)
        print(f"  {db:30s} tables={tbl_n:4d}  data={data_mb} MB  idx={index_mb} MB  total={total_mb} MB ({total_gb_row} GB)")
    print(f"\n  GRAND TOTAL: {total_gb:.3f} GB across {len(per_db)} databases on this host")

    # global row count estimate (approximate — from information_schema, not authoritative)
    cur.execute("""
        SELECT SUM(table_rows) FROM information_schema.TABLES
         WHERE table_schema NOT IN ('information_schema','mysql','performance_schema','sys');
    """)
    row_est = cur.fetchone()[0]
    print(f"  Approx row count (information_schema.table_rows, an estimate): {row_est:,}")

conn.close()
RESULTS["data_volume"] = {"host": "110.238.76.159", "per_db": per_db, "total_gb": total_gb, "row_count_estimate": int(row_est or 0)}

with open("/app/assessment_workspace/tools/_scratch/billing_probe.json", "w") as f:
    json.dump(RESULTS, f, indent=2, default=str)
print("\nSaved -> _scratch/billing_probe.json")
