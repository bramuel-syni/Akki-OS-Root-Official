"""NAS SMB enumeration via JUMP — learn workgroup + sweep auth variants."""
import paramiko, time, base64, itertools

JUMP = {"host": "159.138.173.250", "port": 22, "user": "root", "password": "76Nkr9P4Jv77"}
NAS = {"host": "10.10.55.55", "pw": "r:ZY5_j{"}
SECRETS = [JUMP["password"], NAS["pw"]]
def red(t):
    for s in SECRETS:
        if s and t: t = t.replace(s, "********")
    return t

cli = paramiko.SSHClient(); cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(JUMP["host"], JUMP["port"], username=JUMP["user"], password=JUMP["password"],
            timeout=12, look_for_keys=False, allow_agent=False, banner_timeout=12)
def run(cmd, timeout=45):
    _i,o,e = cli.exec_command(cmd, timeout=timeout)
    out=o.read().decode("utf-8","replace"); err=e.read().decode("utf-8","replace")
    return o.channel.recv_exit_status(), red(out), red(err)

print("== anonymous probe (learn server/workgroup) ==")
rc,o,e = run(f"smbclient -L //{NAS['host']} -N 2>&1")
print(f"rc={rc}")
print("\n".join("  "+l for l in (o or e).splitlines() if l.strip())[:0] or "  "+ (o or e).strip()[:800])

# discover workgroup token if present
discovered = []
for l in (o or "").splitlines():
    ls=l.strip()
    if ls.lower().startswith("workgroup") or "Domain=" in l:
        discovered.append(l.strip())
print("discovered:", discovered)

def authfile(user, domain):
    body=f"username = {user}\npassword = {NAS['pw']}\ndomain = {domain}\n"
    b64=base64.b64encode(body.encode()).decode()
    path="/tmp/.na_%d"%(time.time()*1000)
    run(f"umask 077; echo {b64}|base64 -d > {path}")
    return path

print("\n== auth variant sweep ==")
users = ["Bramwel","bramwel","BRAMWEL"]
domains = ["", "WORKGROUP"]
dialects = ["", "-m SMB2", "-m NT1"]
winner = None
for user, domain, dial in itertools.product(users, domains, dialects):
    ap = authfile(user, domain)
    rc,o,e = run(f"smbclient -L //{NAS['host']} -A {ap} {dial} 2>&1", timeout=30)
    run(f"rm -f {ap}")
    tag=f"user={user} domain={domain or '(empty)'} dial={dial or 'default'}"
    if rc==0 and ("Sharename" in o or "Disk" in o):
        print(f"  SUCCESS  {tag}")
        winner=(user,domain,dial,o); break
    else:
        msg=(o or e).strip().splitlines()
        m=next((x for x in msg if "NT_STATUS" in x or "failed" in x.lower()), (msg[0] if msg else ""))
        print(f"  fail     {tag} :: {m[:80]}")

if winner:
    user,domain,dial,listing = winner
    print("\n== SHARES ==")
    print("\n".join("  "+l for l in listing.splitlines() if l.strip()))
    ap = authfile(user, domain)
    shares=[]
    for l in listing.splitlines():
        p=l.split()
        if len(p)>=2 and p[1]=="Disk":
            shares.append(p[0])
        elif len(p)>=2 and p[1] in ("Disk","IPC","Printer"):
            pass
    # smbclient -L columns: Sharename Type Comment ; Disk in col2
    shares=[l.split()[0] for l in listing.splitlines() if len(l.split())>=2 and l.split()[1]=="Disk" and not l.split()[0].endswith("$")]
    print("\ndisk shares:", shares)
    for sh in shares[:20]:
        rc,o,e = run(f"smbclient //{NAS['host']}/{sh} -A {ap} {dial} -c 'ls' 2>&1", timeout=40)
        lines=[l for l in (o or e).splitlines() if l.strip()]
        print(f"\n-- //{NAS['host']}/{sh} (top-level) rc={rc}, {len(lines)} entries --")
        print("\n".join("   "+l for l in lines[:40]))
    run(f"rm -f {ap}")
else:
    print("\nNo auth variant succeeded — will report LOGON_FAILURE with the variants tried.")
cli.close()
