"""Access NAS 10.10.55.55 via JUMP bastion. Metadata-only enumeration.
Structured output; passwords never printed."""
import paramiko, time, shlex

JUMP = {"host": "159.138.173.250", "port": 22, "user": "root", "password": "76Nkr9P4Jv77"}
NAS = {"host": "10.10.55.55", "user": "Bramwel", "password": "r:ZY5_j{", "domain": "WORKGROUP"}

SECRETS = [JUMP["password"], NAS["password"]]
def red(t):
    for s in SECRETS:
        if s and t: t = t.replace(s, "********")
    return t

cli = paramiko.SSHClient(); cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(JUMP["host"], JUMP["port"], username=JUMP["user"], password=JUMP["password"],
            timeout=12, look_for_keys=False, allow_agent=False, banner_timeout=12, auth_timeout=12)
print("JUMP AUTH OK ->", JUMP["host"])

def run(cmd, timeout=40):
    _i, o, e = cli.exec_command(cmd, timeout=timeout)
    out = o.read().decode("utf-8", "replace"); err = e.read().decode("utf-8", "replace")
    rc = o.channel.recv_exit_status()
    return rc, red(out), red(err)

# 1) NAS port probe from jump
print("\n== NAS port probe (from jump) ==")
for port, label in [(5000,"dsm_http"),(5001,"dsm_https"),(445,"smb"),(139,"nb"),(2049,"nfs"),(22,"ssh"),(3306,"mysql")]:
    rc, o, _ = run(f"timeout 3 bash -c 'echo > /dev/tcp/{NAS['host']}/{port}' && echo OPEN || echo CLOSED", timeout=8)
    print(f"  {label:10s} {NAS['host']}:{port} -> {o.strip()}")

# 2) tooling on jump
print("\n== jump tooling ==")
rc, o, _ = run("for t in smbclient showmount mount.cifs nmap; do printf '%-10s ' $t; (command -v $t || echo MISSING); done")
print(o.strip())

# 3) create temp smb auth file on jump (keeps pw off ps args), enumerate shares
authpath = "/tmp/.nasauth_%d" % int(time.time())
authbody = f"username = {NAS['user']}\npassword = {NAS['password']}\ndomain = {NAS['domain']}\n"
# write via python on jump to avoid echo leaking to ps; use base64 to avoid quoting issues
import base64
b64 = base64.b64encode(authbody.encode()).decode()
run(f"umask 077; echo {b64} | base64 -d > {authpath}")

print("\n== SMB share list (smbclient -L) ==")
for extra in ["-m SMB3", "-m SMB2", ""]:
    rc, o, e = run(f"smbclient -L //{NAS['host']} -A {authpath} {extra} 2>&1", timeout=40)
    if rc == 0 and ("Sharename" in o or "Disk" in o):
        print(f"  [{extra or 'default'}] OK:\n" + "\n".join("    "+l for l in o.splitlines() if l.strip()))
        break
    else:
        print(f"  [{extra or 'default'}] rc={rc} :: {(o or e).strip()[:200]}")

# 4) NFS exports
print("\n== NFS exports (showmount -e) ==")
rc, o, e = run(f"showmount -e {NAS['host']} 2>&1", timeout=20)
print(f"  rc={rc} :: {(o or e).strip()[:400]}")

# cleanup
run(f"shred -u {authpath} 2>/dev/null || rm -f {authpath}")
cli.close()
print("\nDONE (auth file shredded).")
