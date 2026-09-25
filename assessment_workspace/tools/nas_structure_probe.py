"""Access NAS via existing CIFS mount on JUMP. Quick structure probe."""
import paramiko
JUMP = {"host":"159.138.173.250","port":22,"user":"root","password":"76Nkr9P4Jv77"}
SEC=[JUMP["password"]]
def red(t):
    for s in SEC:
        if s and t: t=t.replace(s,"********")
    return t
cli=paramiko.SSHClient(); cli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cli.connect(JUMP["host"],JUMP["port"],username=JUMP["user"],password=JUMP["password"],
            timeout=12,look_for_keys=False,allow_agent=False,banner_timeout=12)
def run(cmd,t=40):
    _i,o,e=cli.exec_command(cmd,timeout=t)
    return o.channel.recv_exit_status(), red(o.read().decode('utf-8','replace')), red(e.read().decode('utf-8','replace'))

print("== mount + df =="); 
for c in ["mount | grep -i 10.10.55.55 || echo NO_MOUNT",
          "df -h /mnt/nfs-share 2>&1",
          "ls -1 /mnt/nfs-share/ 2>&1"]:
    rc,o,e=run(c); print(f"$ {c}\n{(o or e).strip()}\n")

print("== structure of first channels (what's inside a channel dir?) ==")
for ch in ["channel01","Channel09"]:
    rc,o,e=run(f"ls -la /mnt/nfs-share/{ch}/ 2>&1 | head -20")
    print(f"-- {ch} --\n{(o or e).strip()}\n")
    rc,o,e=run(f"timeout 20 find /mnt/nfs-share/{ch} -maxdepth 3 2>/dev/null | head -30")
    print(f"-- find {ch} (maxdepth3, head30) --\n{o.strip()}\n")
cli.close()
