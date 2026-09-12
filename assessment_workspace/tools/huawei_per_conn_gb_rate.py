"""Per-connection $/GB probe for the 2 live Huawei DB connections. Read-only."""
import csv, json
from datetime import datetime, timezone

# Load HW AK/SK
with open("/app/backend/estate_keys/data_sources/huawei_credentials.csv") as f:
    rows = list(csv.reader(f))
hdr = [h.lstrip("\ufeff").strip() for h in rows[0]]
d = dict(zip(hdr, rows[1]))
AK, SK = d["Access Key Id"], d["Secret Access Key"]

# Load bramuel DB pw
with open("/app/backend/estate_keys/data_sources/db_credentials.csv") as f:
    for r in csv.reader(f):
        if len(r) >= 4 and r[1] == "110.238.76.159":
            BRAM_USER, BRAM_PW = r[2], r[3]
            break

RESULTS = {"ts": datetime.now(timezone.utc).isoformat()}

# 1) EIP config for 159.138.162.146 (Weego)
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkeip.v2 import EipClient, ListPublicipsRequest, ListBandwidthsRequest, ShowPublicipRequest
from huaweicloudsdkeip.v2.region.eip_region import EipRegion

creds = BasicCredentials(AK, SK)
eip = EipClient.new_builder().with_credentials(creds).with_region(EipRegion.value_of("af-south-1")).build()

pips = []
resp = eip.list_publicips(ListPublicipsRequest(limit=500))
for p in (resp.publicips or []):
    if p.public_ip_address == "159.138.162.146":
        pip_row = {
            "public_ip": p.public_ip_address,
            "publicip_id": p.id,
            "type": p.type,
            "status": p.status,
            "bandwidth_id": p.bandwidth_id,
            "bandwidth_size": p.bandwidth_size,
            "bandwidth_share_type": p.bandwidth_share_type,
            "port_id": p.port_id,
            "tenant_id": p.tenant_id,
            "create_time": p.create_time,
        }
        pips.append(pip_row)

print(f"[Weego 159.138.162.146] EIP records: {len(pips)}")
for pip in pips:
    print(f"  publicip_id={pip['publicip_id']}")
    print(f"  bandwidth_id={pip['bandwidth_id']}")
    print(f"  bandwidth_size={pip['bandwidth_size']} Mbit/s")
    print(f"  bandwidth_share_type={pip['bandwidth_share_type']}")
    print(f"  tenant_id={pip['tenant_id']}")

# Get the bandwidth's charge_mode
if pips:
    resp = eip.list_bandwidths(ListBandwidthsRequest(limit=500))
    for bw in (resp.bandwidths or []):
        if bw.id == pips[0]["bandwidth_id"]:
            pips[0]["bandwidth_charge_mode"] = bw.charge_mode
            pips[0]["bandwidth_name"] = bw.name
            pips[0]["bandwidth_size_final"] = bw.size
            print(f"  bandwidth.charge_mode={bw.charge_mode}  (traffic=pay-per-GB · bandwidth=fixed Mbps)")
            print(f"  bandwidth.name={bw.name}")

RESULTS["weego_eip"] = pips[0] if pips else None

# 2) Data volume on each live connection
import pymysql

def data_volume(host, user, pw):
    """SELECT information_schema data_length + index_length on all non-system schemas."""
    conn = pymysql.connect(host=host, port=3306, user=user, password=pw, connect_timeout=8, read_timeout=20)
    out = {"per_db": [], "total_data_gb": 0, "total_index_gb": 0, "total_gb": 0}
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_schema,
                   COUNT(*) AS tables,
                   ROUND(SUM(data_length)/1024/1024/1024, 4)   AS data_gb,
                   ROUND(SUM(index_length)/1024/1024/1024, 4)  AS index_gb,
                   ROUND(SUM(data_length+index_length)/1024/1024/1024, 4) AS total_gb
              FROM information_schema.TABLES
             WHERE table_schema NOT IN ('information_schema','mysql','performance_schema','sys')
             GROUP BY table_schema
             ORDER BY total_gb DESC;
        """)
        for row in cur.fetchall():
            db, tn, data_gb, idx_gb, total_gb = row
            out["per_db"].append({"db": db, "tables": tn, "data_gb": float(data_gb or 0),
                                  "index_gb": float(idx_gb or 0), "total_gb": float(total_gb or 0)})
            out["total_data_gb"] += float(data_gb or 0)
            out["total_index_gb"] += float(idx_gb or 0)
            out["total_gb"] += float(total_gb or 0)
    conn.close()
    return out

print("\n=== Data volumes ===")
print("\n[A] Weego_and_marketing-analytics @ 159.138.162.146")
weego_vol = data_volume("159.138.162.146", BRAM_USER, BRAM_PW)
for e in weego_vol["per_db"]:
    print(f"    {e['db']:30s}  tables={e['tables']:4d}  data={e['data_gb']:.3f} GB  idx={e['index_gb']:.3f} GB  total={e['total_gb']:.3f} GB")
print(f"    TOTAL: data={weego_vol['total_data_gb']:.3f} GB  idx={weego_vol['total_index_gb']:.3f} GB  total={weego_vol['total_gb']:.3f} GB")
RESULTS["weego_data_volume"] = weego_vol

print("\n[B] 3rd-party USSD host @ 110.238.76.159")
ussd_vol = data_volume("110.238.76.159", BRAM_USER, BRAM_PW)
for e in ussd_vol["per_db"]:
    print(f"    {e['db']:30s}  tables={e['tables']:4d}  data={e['data_gb']:.3f} GB  idx={e['index_gb']:.3f} GB  total={e['total_gb']:.3f} GB")
print(f"    TOTAL: data={ussd_vol['total_data_gb']:.3f} GB  idx={ussd_vol['total_index_gb']:.3f} GB  total={ussd_vol['total_gb']:.3f} GB")
RESULTS["ussd_data_volume"] = ussd_vol

with open("/app/assessment_workspace/tools/_scratch/per_conn_gb_rate.json","w") as f:
    json.dump(RESULTS, f, indent=2, default=str)
print("\nSaved -> _scratch/per_conn_gb_rate.json")
