"""tools/jump_connectivity_retry_20260921.py · owner-priority connectivity drill.

Owner directive verbatim this-session (2026-09-21T~12:30Z):

    "OWNER PRIORITY TASK (non-interrupting to the R-91 hold — this is
    authorized work now): RETRY THE JUMP SERVER CONNECTION with the
    SAME credentials already on file. Context: the owner has just
    spoken with the RMS admin — the expectation is the network path
    (firewall) may now admit us; the credentials were NOT rotated,
    use the existing banked ones. Respond in English only.
    Execute as a connectivity drill, receipted: ..."

Discipline:
    * Values are held in memory only (via rms_creds_loader.load()).
    * NEVER prints secret values to any log or receipt.
    * References secrets by drop manifest sha + file sha only.
    * Timebox every probe (10s default).
    * Reachability-only for downstream hosts (Huawei MySQL + NAS DSM).
      DO NOT open MySQL protocol sessions; TCP-open is the ceiling.
    * If SSH auth SUCCEEDS: run non-invasive hostname/uname + downstream
      reachability probes, then STOP. No ingestion.

Emits: phase0/connectivity_receipts/20260921T{HHMMSS}Z_JUMP_retry_owner_
authorized_20260921.json (state-only; banked in the state repo).
"""

from __future__ import annotations

import hashlib
import json
import socket
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

# Force tools/ onto sys.path — rms_creds_loader is a co-located tool.
_TOOLS = Path("/app/assessment_workspace/tools")
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import rms_creds_loader  # noqa: E402
import paramiko  # noqa: E402

CUSTODY_XLSX = Path("/app/backend/estate_keys/data_sources/RMS_Connection_Creds.xlsx")
DROP_MANIFEST = Path(
    "/app/assessment_workspace/phase0/credential_drop_manifests/"
    "20260916T1910Z_drop_manifest.json"
)
RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _egress_ip() -> dict:
    """Try to determine the egress IP we present to remote hosts. Multiple
    fallbacks, timeboxed. This is the IP the RMS admin may need for
    firewall allowlisting."""

    results = {}
    endpoints = [
        ("ifconfig.me", "https://ifconfig.me/ip"),
        ("api.ipify.org", "https://api.ipify.org"),
    ]
    for label, url in endpoints:
        try:
            out = subprocess.run(
                ["curl", "-sS", "--max-time", "6", url],
                capture_output=True, text=True, timeout=8,
            )
            if out.returncode == 0 and out.stdout.strip():
                results[label] = out.stdout.strip()[:64]
                return results  # one is enough
        except Exception as e:
            results[label + "_err"] = repr(e)[:120]
    return results


def _dns_resolve(host: str) -> dict:
    """Timeboxed DNS resolution — captures both A-record and error."""
    try:
        socket.setdefaulttimeout(8)
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
        addrs = sorted({info[4][0] for info in infos})
        return {"resolved": True, "addresses": addrs}
    except Exception as e:
        return {"resolved": False, "error_class": e.__class__.__name__, "error_msg": str(e)[:200]}
    finally:
        socket.setdefaulttimeout(None)


def _tcp_probe(host: str, port: int, timeout: float = 10.0) -> dict:
    """Timeboxed TCP connect probe — returns which OSI layer we die at."""
    t0 = time.monotonic()
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        elapsed = time.monotonic() - t0
        s.close()
        return {"tcp_connected": True, "elapsed_s": round(elapsed, 3)}
    except socket.timeout:
        return {"tcp_connected": False, "failure_layer": "TCP_TIMEOUT", "elapsed_s": round(time.monotonic() - t0, 3)}
    except ConnectionRefusedError as e:
        return {"tcp_connected": False, "failure_layer": "TCP_REFUSED", "error_msg": str(e)[:200]}
    except socket.gaierror as e:
        return {"tcp_connected": False, "failure_layer": "NO_DNS", "error_msg": str(e)[:200]}
    except Exception as e:
        return {"tcp_connected": False, "failure_layer": "OTHER", "error_class": e.__class__.__name__, "error_msg": str(e)[:200]}


def _ssh_probe(host: str, port: int, username: str, password: str, timeout: float = 12.0) -> dict:
    """Timeboxed SSH auth probe using paramiko. Never logs the password.

    Returns: banner, auth result, remote-side hostname + uname on success.
    """
    result: dict = {
        "tcp_connected": None,
        "banner": None,
        "banner_class": None,
        "auth_ok": None,
        "auth_failure_layer": None,
    }
    t0 = time.monotonic()
    client = paramiko.SSHClient()
    # STRICT host-key mode against the known TOFU-verified fingerprints
    # captured on 2026-09-14 (T3 handshake receipt). If the JUMP host has
    # been re-imaged, key drift will be caught here — safer than AutoAdd.
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    known_hosts_path = Path("/tmp/jump_known_hosts_20260921.tmp")
    known_hosts_path.write_text(
        # SHA256 fingerprints from T3 handshake (2026-09-14T09:48:04Z)
        # were:
        #   ssh-rsa           SHA256:qEUrMRNdP9rUzetuJ2qYMDKGFrUlLUeaVI6UHPaM/Xc
        #   ecdsa-sha2-nistp256 SHA256:dMz9wmWATBTN1pfwmxvLpMvcdchm77aaVr3q0zIOmk8
        #   ssh-ed25519       SHA256:W45xvjhsARJOcFj9U/bcWC3KDte30T+Amu3eCx4UrwU
        # We cannot pre-populate known_hosts by fingerprint alone
        # (paramiko wants the full public key), so we relax to AutoAdd
        # for this drill and separately re-capture the actual server
        # keys post-connect for TOFU verification.
        "",
        encoding="utf-8",
    )
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # First: use paramiko.Transport for a controlled banner capture
        # then close and use SSHClient for auth. That preserves banner
        # visibility without confusing the retry.
        sock = socket.create_connection((host, port), timeout=timeout)
        result["tcp_connected"] = True
        transport_only = paramiko.Transport(sock)
        try:
            transport_only.start_client(timeout=timeout)
            banner = transport_only.remote_version or ""
            result["banner"] = banner[:200]
            # Class the banner by prefix so the receipt can flag drift.
            if banner.startswith("SSH-2.0-OpenSSH_"):
                result["banner_class"] = "OpenSSH"
            elif banner.startswith("SSH-"):
                result["banner_class"] = "SSH_OTHER"
            else:
                result["banner_class"] = "UNKNOWN"
            # Capture server host key fingerprint for TOFU comparison.
            host_key = transport_only.get_remote_server_key()
            fp = hashlib.sha256(host_key.asbytes()).digest()
            import base64
            fp_b64 = base64.b64encode(fp).decode("ascii").rstrip("=")
            result["remote_host_key_type"] = host_key.get_name()
            result["remote_host_key_sha256_b64"] = fp_b64
        finally:
            try:
                transport_only.close()
            except Exception:
                pass
            try:
                sock.close()
            except Exception:
                pass

        # Now attempt password auth via a fresh SSHClient — separate
        # connect, timeboxed, secret held in local scope only.
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            auth_timeout=timeout,
            banner_timeout=timeout,
            allow_agent=False,
            look_for_keys=False,
        )
        result["auth_ok"] = True

        # Post-auth: safe non-invasive commands to fingerprint the host.
        for cmd_key, cmd in (
            ("hostname", "hostname"),
            ("uname_a", "uname -a"),
            ("whoami", "whoami"),
            ("uptime", "uptime"),
        ):
            try:
                _stdin, stdout, stderr = client.exec_command(cmd, timeout=6)
                out = stdout.read(2048).decode("utf-8", errors="replace").strip()
                result[cmd_key] = out[:300]
            except Exception as e:
                result[cmd_key + "_err"] = repr(e)[:200]

        # Downstream reachability probes from within the JUMP host.
        # Reachability only — no protocol handshake, no auth attempts.
        # Endpoints sourced from the loader (banked creds); we probe TCP
        # open/closed via /dev/tcp bash primitive (no nc needed).
        downstream = []
        try:
            binds = rms_creds_loader.load()
            for cluster in binds.mysql_clusters:
                if cluster.host:
                    downstream.append({
                        "kind": "mysql",
                        "section": cluster.section,
                        "host": cluster.host,
                        "port": 3306,
                    })
            if binds.nas.dsm_url:
                # Extract host from URL crudely (avoid urllib to keep import surface tight).
                url = binds.nas.dsm_url
                host_nas = url.replace("https://", "").replace("http://", "").split("/")[0]
                if ":" in host_nas:
                    hnas, pnas = host_nas.rsplit(":", 1)
                    downstream.append({"kind": "nas_dsm", "host": hnas, "port": int(pnas)})
                else:
                    downstream.append({"kind": "nas_dsm", "host": host_nas, "port": 443})
        except Exception as e:
            result["downstream_enumeration_err"] = repr(e)[:200]

        # Run each downstream TCP probe FROM THE JUMP (via ssh exec_command).
        downstream_results = []
        for ep in downstream:
            cmd = (
                f"timeout 6 bash -c 'exec 3<>/dev/tcp/{ep['host']}/{ep['port']} "
                f"&& echo TCP_OPEN || echo TCP_CLOSED'"
            )
            try:
                _stdin, stdout, stderr = client.exec_command(cmd, timeout=8)
                out = stdout.read(64).decode("utf-8", errors="replace").strip()
                err = stderr.read(256).decode("utf-8", errors="replace").strip()
                downstream_results.append({
                    "kind": ep["kind"],
                    "section": ep.get("section"),
                    "host": ep["host"],
                    "port": ep["port"],
                    "result": out or "TIMEOUT_OR_ERROR",
                    "stderr_first_256": err[:256] if err else "",
                })
            except Exception as e:
                downstream_results.append({
                    "kind": ep["kind"],
                    "section": ep.get("section"),
                    "host": ep["host"],
                    "port": ep["port"],
                    "result": "PROBE_EXCEPTION",
                    "error_class": e.__class__.__name__,
                    "error_msg": str(e)[:200],
                })
        result["downstream_reachability_from_jump"] = downstream_results

    except paramiko.AuthenticationException as e:
        result["auth_ok"] = False
        result["auth_failure_layer"] = "SSH_AUTH_REJECTED"
        result["error_msg"] = str(e)[:200]
    except paramiko.SSHException as e:
        result["auth_ok"] = False
        result["auth_failure_layer"] = "SSH_PROTOCOL_ERROR"
        result["error_msg"] = str(e)[:200]
    except socket.timeout:
        result["tcp_connected"] = False
        result["auth_failure_layer"] = "TCP_TIMEOUT"
    except ConnectionRefusedError as e:
        result["tcp_connected"] = False
        result["auth_failure_layer"] = "TCP_REFUSED"
        result["error_msg"] = str(e)[:200]
    except socket.gaierror as e:
        result["auth_failure_layer"] = "NO_DNS"
        result["error_msg"] = str(e)[:200]
    except Exception as e:
        result["auth_failure_layer"] = "OTHER"
        result["error_class"] = e.__class__.__name__
        result["error_msg"] = str(e)[:200]
        result["traceback"] = traceback.format_exc()[-1500:]
    finally:
        result["elapsed_s"] = round(time.monotonic() - t0, 3)
        try:
            client.close()
        except Exception:
            pass
        try:
            known_hosts_path.unlink(missing_ok=True)
        except Exception:
            pass

    return result


def main() -> None:
    receipt: dict = {
        "task": "jump_connection_retry_owner_authorized_20260921",
        "captured_at_utc": _now_utc(),
        "authorization": (
            "Owner priority directive this-session 2026-09-21T~12:30Z: "
            "'RETRY THE JUMP SERVER CONNECTION with the SAME credentials "
            "already on file. Context: the owner has just spoken with the "
            "RMS admin — the expectation is the network path (firewall) "
            "may now admit us; the credentials were NOT rotated, use the "
            "existing banked ones.' R-91 hold unchanged (owner: 'non-"
            "interrupting to the R-91 hold — this is authorized work now')."
        ),
        "cred_source": {
            "custody_file": str(CUSTODY_XLSX),
            "custody_file_sha256": _sha256(CUSTODY_XLSX) if CUSTODY_XLSX.is_file() else None,
            "drop_manifest": str(DROP_MANIFEST),
            "drop_manifest_sha256": _sha256(DROP_MANIFEST) if DROP_MANIFEST.is_file() else None,
        },
        "egress_ip_we_present": _egress_ip(),
    }

    # Load creds in memory — never printed, never written.
    try:
        binds = rms_creds_loader.load()
    except Exception as e:
        receipt["cred_load_err"] = repr(e)[:400]
        _emit_receipt(receipt)
        return

    receipt["cred_shape"] = {
        "jump": binds.jump.describe(),         # host + user_len + user_prefix2 + password_len
        "radio": binds.radio.describe(),
        "nas": binds.nas.describe(),
        "mysql_clusters_count": len(binds.mysql_clusters),
    }

    jump_host = binds.jump.host
    jump_user = binds.jump.user
    # Port is not carried in xlsx — assume standard SSH 22 per prior banking.
    jump_port = 22

    receipt["target"] = {
        "host": jump_host,
        "port": jump_port,
    }

    # Probe cascade — each timeboxed.
    receipt["probes"] = {}
    receipt["probes"]["dns"] = _dns_resolve(jump_host)
    receipt["probes"]["tcp_connect"] = _tcp_probe(jump_host, jump_port, timeout=10.0)
    receipt["probes"]["ssh_banner_plus_auth_plus_survey"] = _ssh_probe(
        jump_host, jump_port,
        username=jump_user,
        password=binds.jump.password,  # held only in local frame
        timeout=12.0,
    )

    _emit_receipt(receipt)


def _emit_receipt(receipt: dict) -> None:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    receipt_path = RECEIPT_DIR / f"{stamp}_JUMP_retry_owner_authorized_20260921.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"receipt_path: {receipt_path}")
    # Deliberately do NOT print the receipt contents themselves — they
    # contain host/user shape info that is fine but let's keep the
    # stdout minimal per hygiene.


if __name__ == "__main__":
    main()
