"""Pull authoritative IDs/names for the sysadmin note. Read-only."""
import csv, json
from datetime import datetime, timezone

with open("/app/backend/estate_keys/data_sources/huawei_credentials.csv") as f:
    rows = list(csv.reader(f))
hdr = [h.lstrip("\ufeff").strip() for h in rows[0]]
d = dict(zip(hdr, rows[1]))
AK, SK = d["Access Key Id"], d["Secret Access Key"]

from huaweicloudsdkcore.auth.credentials import BasicCredentials, GlobalCredentials
from huaweicloudsdkcore.exceptions import exceptions as hw_ex
from huaweicloudsdkiam.v3 import (
    IamClient, KeystoneListProjectsRequest, KeystoneListAuthDomainsRequest,
)
from huaweicloudsdkiam.v3.region.iam_region import IamRegion
from huaweicloudsdkrds.v3 import RdsClient, ListInstancesRequest as RdsListInstancesRequest
from huaweicloudsdkrds.v3.region.rds_region import RdsRegion
from huaweicloudsdkvpc.v2 import (
    VpcClient, ShowVpcRequest, ShowSubnetRequest, ShowSecurityGroupRequest,
    ListSecurityGroupsRequest, ListVpcsRequest, ListSubnetsRequest,
)
from huaweicloudsdkvpc.v2.region.vpc_region import VpcRegion

OUT = {"ts": datetime.now(timezone.utc).isoformat()}

# 1) IAM: domain + af-south-1 project name/id
gcreds = GlobalCredentials(AK, SK)
iam = IamClient.new_builder().with_credentials(gcreds).with_region(IamRegion.value_of("ap-southeast-1")).build()
try:
    r = iam.keystone_list_auth_domains(KeystoneListAuthDomainsRequest())
    OUT["domain"] = {"id": r.domains[0].id, "name": r.domains[0].name, "enabled": r.domains[0].enabled} if r.domains else None
except hw_ex.ClientRequestException as e:
    OUT["domain_err"] = f"{e.status_code}:{e.error_code}"

try:
    r = iam.keystone_list_projects(KeystoneListProjectsRequest())
    OUT["projects"] = []
    for p in (r.projects or []):
        OUT["projects"].append({"id": p.id, "name": p.name, "domain_id": p.domain_id, "enabled": p.enabled})
        if p.name == "af-south-1":
            OUT["af_south_1_project"] = {"id": p.id, "name": p.name, "domain_id": p.domain_id, "enabled": p.enabled}
        if p.name == "ap-southeast-1":
            OUT["ap_southeast_1_project"] = {"id": p.id, "name": p.name, "domain_id": p.domain_id, "enabled": p.enabled}
except hw_ex.ClientRequestException as e:
    OUT["projects_err"] = f"{e.status_code}:{e.error_code}"

print(f"Domain: {OUT.get('domain')}")
print(f"af-south-1 project: {OUT.get('af_south_1_project')}")
print(f"ap-southeast-1 project: {OUT.get('ap_southeast_1_project')}")

# 2) VPC + subnet full names/CIDRs (af-south-1)
bcreds = BasicCredentials(AK, SK)
vpc = VpcClient.new_builder().with_credentials(bcreds).with_region(VpcRegion.value_of("af-south-1")).build()

RDS_VPC_ID = "de3ba6f7-d0e7-4228-8da2-19bd33a07ff2"
RDS_SUBNET_ID = "c7fef874-8aef-4b91-9d3b-7e84ce53104d"

try:
    r = vpc.show_vpc(ShowVpcRequest(vpc_id=RDS_VPC_ID))
    v = r.vpc
    OUT["rds_vpc"] = {"id": v.id, "name": v.name, "cidr": v.cidr, "status": v.status,
                      "enterprise_project_id": getattr(v, "enterprise_project_id", None),
                      "description": getattr(v, "description", None)}
    print(f"\nVPC: {OUT['rds_vpc']}")
except hw_ex.ClientRequestException as e:
    OUT["rds_vpc_err"] = f"{e.status_code}:{e.error_code}"

try:
    r = vpc.show_subnet(ShowSubnetRequest(subnet_id=RDS_SUBNET_ID))
    s = r.subnet
    OUT["rds_subnet"] = {"id": s.id, "name": s.name, "cidr": s.cidr, "gateway_ip": s.gateway_ip,
                         "status": s.status, "vpc_id": s.vpc_id,
                         "availability_zone": getattr(s, "availability_zone", None),
                         "primary_dns": s.primary_dns, "secondary_dns": s.secondary_dns}
    print(f"Subnet: {OUT['rds_subnet']}")
except hw_ex.ClientRequestException as e:
    OUT["rds_subnet_err"] = f"{e.status_code}:{e.error_code}"

# 2b) Also list ALL VPCs and subnets af-south-1 to see if there are others
try:
    r = vpc.list_vpcs(ListVpcsRequest(limit=100))
    OUT["all_af_south_1_vpcs"] = [{"id": v.id, "name": v.name, "cidr": v.cidr} for v in (r.vpcs or [])]
except Exception as e:
    pass

try:
    r = vpc.list_subnets(ListSubnetsRequest(limit=100))
    OUT["all_af_south_1_subnets"] = [{"id": s.id, "name": s.name, "cidr": s.cidr, "vpc_id": s.vpc_id, "gateway_ip": s.gateway_ip} for s in (r.subnets or [])]
except Exception as e:
    pass

# 3) RDS instances + their SG IDs (af-south-1 + ap-southeast-1)
rds_instances = []
for region in ("af-south-1", "ap-southeast-1"):
    rds = RdsClient.new_builder().with_credentials(bcreds).with_region(RdsRegion.value_of(region)).build()
    try:
        r = rds.list_instances(RdsListInstancesRequest())
        for i in (r.instances or []):
            rds_instances.append({
                "name": i.name, "id": i.id, "region": region,
                "engine": f"{i.datastore.type} {i.datastore.version}" if i.datastore else None,
                "port": i.port,
                "public_ips": i.public_ips,
                "private_ips": i.private_ips,
                "vpc_id": i.vpc_id,
                "subnet_id": i.subnet_id,
                "security_group_id": i.security_group_id,
                "az": getattr(i, "availability_zone", None) or getattr(i, "az_code", None),
            })
    except hw_ex.ClientRequestException as e:
        print(f"  RDS ERR {region}: {e.status_code}:{e.error_code}")
OUT["rds_instances"] = rds_instances

# 4) Resolve each unique SG ID -> name
unique_sgs = list({inst["security_group_id"] for inst in rds_instances if inst["security_group_id"]})
sg_details = {}
# Query af-south-1 first
for region in ("af-south-1", "ap-southeast-1"):
    v = VpcClient.new_builder().with_credentials(bcreds).with_region(VpcRegion.value_of(region)).build()
    for sg_id in unique_sgs:
        if sg_id in sg_details: continue
        try:
            r = v.show_security_group(ShowSecurityGroupRequest(security_group_id=sg_id))
            sg = r.security_group
            sg_details[sg_id] = {
                "id": sg.id,
                "name": sg.name,
                "description": sg.description,
                "vpc_id": getattr(sg, "vpc_id", None),
                "enterprise_project_id": getattr(sg, "enterprise_project_id", None),
                "region": region,
                "rule_count": len(sg.security_group_rules or []),
            }
        except hw_ex.ClientRequestException:
            continue
OUT["security_groups"] = sg_details

print(f"\nRDS instances: {len(rds_instances)}")
for inst in rds_instances:
    sg = sg_details.get(inst["security_group_id"])
    sg_name = sg["name"] if sg else "?"
    print(f"  {inst['name']:35s} region={inst['region']:16s} sg={inst['security_group_id']} [{sg_name}]")

with open("/app/assessment_workspace/tools/_scratch/sysadmin_note_facts.json", "w") as f:
    json.dump(OUT, f, indent=2, default=str)
print(f"\nSaved -> _scratch/sysadmin_note_facts.json")
