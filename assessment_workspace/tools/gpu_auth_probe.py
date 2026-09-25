"""Read-only GPU auth probe. Prints ONLY structured results; never a secret value.

Tests, per host: (1) key auth via banked id_ed25519_akki_gpu, (2) password auth
via GPU_CREDS.xlsx. On key success runs `hostname` + `nvidia-smi`.
"""
import re
import openpyxl
import paramiko

XLSX = "/app/backend/estate_keys/gpu_hosts/GPU_CREDS.xlsx"
KEY = "/app/backend/estate_keys/gpu_hosts/id_ed25519_akki_gpu"

# --- parse the single-column key:value sheet -------------------------------
wb = openpyxl.load_workbook(XLSX, data_only=True)
fields = {}
for ws in wb.worksheets:
    for (val,) in ws.iter_rows(values_only=True):
        if not val:
            continue
        s = str(val)
        if ":" in s:
            k, _, v = s.partition(":")
            fields[k.strip().lower()] = v.strip()

# Identify creds. The sheet describes ONE host but we test both IPs.
username = fields.get("username") or fields.get("user") or "ubuntu"
password = fields.get("password") or fields.get("pass") or ""
port = int(fields.get("port") or 22)
sheet_host = fields.get("ip") or fields.get("host") or fields.get("public ip") or ""

print("PARSED_FIELDS_KEYS:", sorted(fields.keys()))
print("username:", username, "| port:", port, "| sheet_host:", sheet_host,
      "| password_present:", bool(password), "| password_len:", len(password))

def redact(t: str) -> str:
    if password and t:
        t = t.replace(password, "********")
    return t

HOSTS = [("akki-vm", "41.173.184.244"), ("akki-vm-ii", "41.173.184.247")]

def attempt(ip, method):
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    common = dict(hostname=ip, port=port, username=username, timeout=10,
                  allow_agent=False, look_for_keys=False, banner_timeout=10, auth_timeout=10)
    try:
        if method == "key":
            cli.connect(key_filename=KEY, **common)
        else:
            cli.connect(password=password, **common)
        # success — probe
        out = {}
        for label, cmd in [("hostname", "hostname"),
                           ("nvidia-smi", "nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>&1 | head -8"),
                           ("uname", "uname -a")]:
            _i, o, e = cli.exec_command(cmd, timeout=20)
            out[label] = redact((o.read() + e.read()).decode("utf-8", "replace").strip())
        cli.close()
        return {"ok": True, "probe": out}
    except Exception as ex:
        return {"ok": False, "err": f"{type(ex).__name__}: {redact(str(ex))}"}

for name, ip in HOSTS:
    print(f"\n===== {name} ({ip}) =====")
    for method in ("key", "password"):
        r = attempt(ip, method)
        if r["ok"]:
            print(f"  [{method}] SUCCESS")
            for k, v in r["probe"].items():
                print(f"      {k}: {v}")
        else:
            print(f"  [{method}] FAIL  {r['err']}")
