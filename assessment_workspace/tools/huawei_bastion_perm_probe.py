"""Probe ECS/EIP/VPC create permissions on the AK/SK BEFORE any actual create.
Strategy: read operations first (no side effects). If reads are 403, create will be too.
No POST/PUT/DELETE calls in this probe.
"""
import csv, json
from datetime import datetime, timezone

with open("/app/backend/estate_keys/data_sources/huawei_credentials.csv") as f:
    rows = list(csv.reader(f))
hdr = [h.lstrip("\ufeff").strip() for h in rows[0]]
d = dict(zip(hdr, rows[1]))
AK, SK = d["Access Key Id"], d["Secret Access Key"]

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions as hw_ex
from huaweicloudsdkecs.v2 import EcsClient, ListServersDetailsRequest, ListFlavorsRequest
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion
from huaweicloudsdkvpc.v2 import VpcClient
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion
from huaweicloudsdkvpc.v2 import (
    ListVpcsRequest, ListSubnetsRequest, ListSecurityGroupsRequest,
    ShowVpcRequest, ShowSubnetRequest,
)

region = "af-south-1"
creds = BasicCredentials(AK, SK)

results = {"ts": datetime.now(timezone.utc).isoformat(), "region": region, "probes": []}

def probe(name, fn):
    r = {"name": name, "ok": False, "code": None, "error_msg": None, "sample": None}
    try:
        resp = fn()
        r["ok"] = True
        # Capture a tiny sample without leaking data
        if hasattr(resp, "servers"):
            r["sample"] = f"servers_count={len(resp.servers or [])}"
        elif hasattr(resp, "vpcs"):
            r["sample"] = f"vpcs_count={len(resp.vpcs or [])}"
            r["vpcs"] = [{"id": v.id, "name": v.name, "cidr": v.cidr} for v in (resp.vpcs or [])]
        elif hasattr(resp, "subnets"):
            r["sample"] = f"subnets_count={len(resp.subnets or [])}"
            r["subnets"] = [{"id": s.id, "name": s.name, "cidr": s.cidr, "vpc_id": s.vpc_id} for s in (resp.subnets or [])]
        elif hasattr(resp, "security_groups"):
            r["sample"] = f"sgs_count={len(resp.security_groups or [])}"
            r["sgs"] = [{"id": s.id, "name": s.name} for s in (resp.security_groups or [])[:20]]
        elif hasattr(resp, "flavors"):
            r["sample"] = f"flavors_count={len(resp.flavors or [])}"
    except hw_ex.ClientRequestException as e:
        r["code"] = f"{e.status_code}:{e.error_code}"
        r["error_msg"] = (getattr(e, "error_msg", "") or "")[:200]
    except Exception as e:
        r["code"] = type(e).__name__
        r["error_msg"] = str(e)[:200]
    results["probes"].append(r)
    return r

# 1. ECS reads
ecs_client = EcsClient.new_builder().with_credentials(creds).with_region(EcsRegion.value_of(region)).build()
r1 = probe("ecs:cloudServers:list (ListServersDetails)", lambda: ecs_client.list_servers_details(ListServersDetailsRequest(limit=1)))
r2 = probe("ecs:cloudServerFlavors:get (ListFlavors)", lambda: ecs_client.list_flavors(ListFlavorsRequest()))

# 2. VPC reads
vpc_client = VpcClient.new_builder().with_credentials(creds).with_region(VpcRegion.value_of(region)).build()
r3 = probe("vpc:vpcs:list (ListVpcs)", lambda: vpc_client.list_vpcs(ListVpcsRequest(limit=100)))
r4 = probe("vpc:subnets:list (ListSubnets)", lambda: vpc_client.list_subnets(ListSubnetsRequest(limit=100)))
r5 = probe("vpc:securityGroups:list (ListSecurityGroups)", lambda: vpc_client.list_security_groups(ListSecurityGroupsRequest(limit=100)))

# 3. Direct show on the known RDS VPC + subnet (confirms IDs the owner referenced)
RDS_VPC_ID = "de3ba6f7-d0e7-4228-8da2-19bd33a07ff2"
RDS_SUBNET_ID = "c7fef874-8aef-4b91-9d3b-7e84ce53104d"
r6 = probe(f"vpc:vpcs:show (ShowVpc {RDS_VPC_ID[:8]}...)",
           lambda: vpc_client.show_vpc(ShowVpcRequest(vpc_id=RDS_VPC_ID)))
r7 = probe(f"vpc:subnets:show (ShowSubnet {RDS_SUBNET_ID[:8]}...)",
           lambda: vpc_client.show_subnet(ShowSubnetRequest(subnet_id=RDS_SUBNET_ID)))

# Print pretty summary
print("=== ECS / VPC / SG permission probe (READ-ONLY) ===\n")
for r in results["probes"]:
    status = "OK   " if r["ok"] else "DENY "
    print(f"  [{status}] {r['name']:60s}  {r.get('sample') or r.get('code') or ''}  {(r.get('error_msg') or '')[:80]}")

with open("/app/assessment_workspace/tools/_scratch/perm_probe.json","w") as f:
    json.dump(results, f, indent=2, default=str)

# Verdict
any_ecs = any(r["ok"] for r in results["probes"][:2])
any_vpc = any(r["ok"] for r in results["probes"][2:])
print()
print(f"ECS reads: {'ALLOWED' if any_ecs else 'DENIED'}")
print(f"VPC reads: {'ALLOWED' if any_vpc else 'DENIED'}")
print()
print("If ECS reads are DENIED, create will be denied too — STOP HERE and report.")
