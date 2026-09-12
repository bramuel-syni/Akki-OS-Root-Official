"""Split multi-SG bindings on RDS and resolve every unique SG name in af-south-1 + ap-southeast-1."""
import csv, json
with open("/app/backend/estate_keys/data_sources/huawei_credentials.csv") as f:
    rows = list(csv.reader(f))
hdr = [h.lstrip("\ufeff").strip() for h in rows[0]]
d = dict(zip(hdr, rows[1]))
AK, SK = d["Access Key Id"], d["Secret Access Key"]

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions as hw_ex
from huaweicloudsdkrds.v3 import RdsClient, ListInstancesRequest
from huaweicloudsdkrds.v3.region.rds_region import RdsRegion
from huaweicloudsdkvpc.v2 import VpcClient, ShowSecurityGroupRequest, ListVpcsRequest
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion

bcreds = BasicCredentials(AK, SK)

# Refetch af-south-1 RDS with SG-split
rds = RdsClient.new_builder().with_credentials(bcreds).with_region(RdsRegion.value_of("af-south-1")).build()
resp = rds.list_instances(ListInstancesRequest())
per_inst = []
all_sg_ids = set()
for i in (resp.instances or []):
    sgs = [s.strip() for s in (i.security_group_id or "").split(",") if s.strip()]
    all_sg_ids.update(sgs)
    per_inst.append({"name": i.name, "id": i.id, "security_groups": sgs,
                     "public_ips": i.public_ips, "private_ips": i.private_ips,
                     "engine": f"{i.datastore.type} {i.datastore.version}"})

print(f"af-south-1 RDS instances: {len(per_inst)}")
print(f"Unique SG IDs across af-south-1 RDS: {len(all_sg_ids)}\n")

# Resolve every SG name via af-south-1 VPC show
vpc = VpcClient.new_builder().with_credentials(bcreds).with_region(VpcRegion.value_of("af-south-1")).build()
sg_map = {}
for sg_id in all_sg_ids:
    try:
        r = vpc.show_security_group(ShowSecurityGroupRequest(security_group_id=sg_id))
        sg = r.security_group
        # Extract inbound rules on port 3306/5432
        inbound_3306 = []
        inbound_5432 = []
        inbound_22 = []
        inbound_all = []
        for rule in (sg.security_group_rules or []):
            if rule.direction == "ingress":
                pmin = getattr(rule, "port_range_min", None) or getattr(rule, "multiport", None)
                pmax = getattr(rule, "port_range_max", None)
                rem = getattr(rule, "remote_ip_prefix", None) or getattr(rule, "remote_group_id", None)
                proto = getattr(rule, "protocol", None)
                summary = f"proto={proto} port={pmin}-{pmax} remote={rem}"
                inbound_all.append(summary)
                port_str = str(pmin) if pmin else ""
                if "3306" in port_str: inbound_3306.append(summary)
                if "5432" in port_str: inbound_5432.append(summary)
                if port_str == "22": inbound_22.append(summary)
        sg_map[sg_id] = {
            "id": sg.id, "name": sg.name, "description": sg.description,
            "rule_count": len(sg.security_group_rules or []),
            "ingress_3306": inbound_3306,
            "ingress_5432": inbound_5432,
            "ingress_22":   inbound_22,
            "ingress_total": len(inbound_all),
            "ingress_sample": inbound_all[:6],
        }
        print(f"SG {sg_id[:8]}…  name='{sg.name}'  rules={len(sg.security_group_rules or [])}  ingress_3306={len(inbound_3306)}  ingress_5432={len(inbound_5432)}")
    except hw_ex.ClientRequestException as e:
        print(f"SG {sg_id[:8]}…  ERR {e.status_code}:{e.error_code}")
        sg_map[sg_id] = {"err": f"{e.status_code}:{e.error_code}"}

print("\n=== Per-instance SG binding with resolved names ===")
for inst in per_inst:
    print(f"\n  {inst['name']:35s} ({inst['engine']})")
    print(f"    public: {inst['public_ips']}  private: {inst['private_ips']}")
    for sg_id in inst["security_groups"]:
        m = sg_map.get(sg_id, {})
        print(f"    SG {sg_id}  name='{m.get('name','?')}'  rules={m.get('rule_count','?')}  3306-ingress={len(m.get('ingress_3306',[]))} rules")

# Save
with open("/app/assessment_workspace/tools/_scratch/sysadmin_sg_map.json","w") as f:
    json.dump({"instances": per_inst, "sg_map": sg_map}, f, indent=2, default=str)
