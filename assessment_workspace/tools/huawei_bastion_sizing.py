"""Re-probe hosts named in db_credentials_2.csv + list af-south-1 ECS flavors for bastion sizing."""
import csv, socket, time, json, hashlib
from datetime import datetime, timezone

with open("/app/backend/estate_keys/data_sources/huawei_credentials.csv") as f:
    rows = list(csv.reader(f))
hdr = [h.lstrip("\ufeff").strip() for h in rows[0]]
d = dict(zip(hdr, rows[1]))
AK, SK = d["Access Key Id"], d["Secret Access Key"]

# --- Task 1a: fresh TCP + greet check on the 4 hosts named in db_credentials_2.csv ---
targets = [
    ("159.138.162.146", "Weego_and_marketing-analytics"),
    ("159.138.164.124", "citizen-digital-dev-db-cluster"),
    ("110.238.75.83",   "visitors-database-cluster"),
    ("203.123.83.144",  "rds-shikisha"),
]

def tcp(host, port=3306, timeout=8.0):
    r = {"tcp_ok": False, "err": None, "latency_ms": None, "mysql_version": None}
    t0 = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            r["tcp_ok"] = True
            r["latency_ms"] = round((time.time()-t0)*1000, 1)
            s.settimeout(3.0)
            try:
                data = s.recv(4096)
                if data and len(data) > 5 and data[4] == 0x0a:
                    i = 5; end = data.find(b"\x00", i)
                    r["mysql_version"] = data[i:end].decode("latin-1","replace")
            except socket.timeout:
                pass
    except Exception as e:
        r["err"] = f"{type(e).__name__}:{str(e)[:100]}"
        r["latency_ms"] = round((time.time()-t0)*1000, 1)
    return r

print("=== TASK 1a: TCP+greet on the 4 hosts named in db_credentials_2.csv ===")
tcp_out = {}
for host, name in targets:
    r = tcp(host)
    tcp_out[host] = {"name": name, **r}
    print(f"  {host:20s} [{name:35s}]  tcp={r['tcp_ok']:5}  lat={r['latency_ms']}ms  ver={r['mysql_version']}  err={r['err']}")

# --- Task 2: list ECS flavors in af-south-1 ---
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions as hw_ex
from huaweicloudsdkecs.v2 import EcsClient, ListFlavorsRequest
from huaweicloudsdkecs.v2.region.ecs_region import EcsRegion

print("\n=== TASK 2a: ECS flavors visible in af-south-1 ===")
creds = BasicCredentials(AK, SK)
client = EcsClient.new_builder().with_credentials(creds).with_region(EcsRegion.value_of("af-south-1")).build()

flavors = []
try:
    resp = client.list_flavors(ListFlavorsRequest(availability_zone=None))
    for f in (resp.flavors or []):
        # Filter to small-to-medium: <=4 vCPU, <=8 GB
        try:
            vcpu = int(f.vcpus)
            ram_mb = int(f.ram)
        except Exception:
            continue
        if vcpu <= 4 and ram_mb <= 8192:
            flavors.append({
                "id": f.id,
                "name": f.name,
                "vcpus": vcpu,
                "ram_gb": round(ram_mb / 1024, 1),
                "disk": f.disk,
            })
    print(f"  total small flavors returned (≤4 vCPU, ≤8 GB): {len(flavors)}")
    # Show family breakdown
    from collections import Counter
    families = Counter(f["id"].split(".")[0] for f in flavors)
    print(f"  families: {dict(families)}")
    # Show recommended candidates: s-series (general), t-series (burstable), kc/kai (Kunpeng ARM)
    print("\n  === Bastion-candidate flavors (1-2 vCPU, 2-4 GB) ===")
    cands = [f for f in flavors if f["vcpus"] in (1,2) and f["ram_gb"] in (1.0, 2.0, 4.0)]
    for f in sorted(cands, key=lambda x: (x["vcpus"], x["ram_gb"], x["id"])):
        print(f"    {f['id']:30s}  {f['vcpus']}vCPU / {f['ram_gb']}GB  disk={f['disk']}")
except hw_ex.ClientRequestException as e:
    print(f"  ERR: {e.status_code}:{e.error_code}:{e.error_msg[:150]}")

with open("/app/assessment_workspace/tools/_scratch/ecs_flavors_af_south_1.json","w") as f:
    json.dump({"flavors_small": flavors, "tcp_reprobe": tcp_out, "ts": datetime.now(timezone.utc).isoformat()}, f, indent=2, default=str)
print("\nSaved -> _scratch/ecs_flavors_af_south_1.json")
