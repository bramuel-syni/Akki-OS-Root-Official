"""Probe NEW rotated GPU passwords from GPU_Creds_2.csv. Structured output only."""
import csv, re
import paramiko

CSV = "/app/backend/estate_keys/gpu_hosts/GPU_Creds_2.csv"

# parse blocks: each host block has Hostname/Username/Password/Public IP lines
rows = [r[0].strip() for r in csv.reader(open(CSV)) if r and r[0].strip()]
hosts = []
cur = {}
for line in rows:
    if ":" in line:
        k, _, v = line.partition(":")
        k = k.strip().lower(); v = v.strip()
        if k == "hostname":
            if cur:
                hosts.append(cur)
            cur = {"hostname": v}
        else:
            cur[k] = v
if cur:
    hosts.append(cur)

secrets = [h.get("password", "") for h in hosts if h.get("password")]
def redact(t):
    for s in secrets:
        if s and t:
            t = t.replace(s, "********")
    return t

print("HOSTS_PARSED:", [(h.get("hostname"), h.get("public ip"), h.get("username"),
                          "pw_len=%d" % len(h.get("password", ""))) for h in hosts])

def try_pw(ip, user, pw):
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        cli.connect(hostname=ip, port=22, username=user, password=pw, timeout=12,
                    allow_agent=False, look_for_keys=False, banner_timeout=12, auth_timeout=12)
        out = {}
        for lbl, cmd in [("hostname", "hostname"),
                         ("nvidia-smi", "nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader 2>&1 | head -8"),
                         ("uname", "uname -a")]:
            _i, o, e = cli.exec_command(cmd, timeout=25)
            out[lbl] = redact((o.read() + e.read()).decode("utf-8", "replace").strip())
        cli.close()
        return True, out
    except Exception as ex:
        return False, f"{type(ex).__name__}: {redact(str(ex))}"

for h in hosts:
    ip = h.get("public ip"); user = h.get("username", "ubuntu"); pw = h.get("password", "")
    print(f"\n===== {h.get('hostname')} ({ip}) =====")
    ok, res = try_pw(ip, user, pw)
    if ok:
        print("  [password] SUCCESS")
        for k, v in res.items():
            print(f"      {k}: {v}")
    else:
        print(f"  [password] FAIL  {res}")
