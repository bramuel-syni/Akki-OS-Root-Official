"""tools/huawei_obs_access_retry_20260921.py · owner-priority OBS access drill.

Owner directive verbatim this-session (2026-09-21T~12:55Z):

    "OWNER QUESTION → receipted drill (authorized now, non-interrupting
    to the R-91 hold): DO WE HAVE HUAWEI OBS (object storage) ACCESS
    with any banked access keys? ... INVENTORY: scan the banked
    credential sources — estate_keys/data_sources/RMS_Connection_Creds.
    xlsx (sha d778eb1e...), any other custody drops/manifests — for
    Huawei Cloud access keys (AK/SK pairs), OBS endpoints, bucket
    names, region identifiers, or console credentials. ... If AK/SK
    found: probe OBS read-only via signed REST ... Probes, timeboxed
    10s each, in order: (a) ListBuckets — enumerate what the key can
    see; (b) for each visible bucket: HeadBucket + GetBucketLocation
    + a ListObjects with max-keys=5 (names/sizes only). NO object
    downloads, NO writes, NO ACL changes. ... Failure-layer everything
    like the JUMP matrix: no-keys-on-file / DNS / TCP / TLS /
    403-invalid-key / 403-no-permission / 200. A 403 with a valid
    signature is an IAM-policy finding, not a network finding —
    distinguish them. ... STOP after the survey — no object data
    leaves the estate without a separate owner GO."

Discipline (SO §4.1 §E + readonly_obs_guard):
    * AK/SK held in memory only via readline() + shape derivation.
    * NEVER prints AK/SK values, NEVER writes them to log or receipt.
    * References secrets by drop + sha + field-shape only (ak_len,
      sk_len, ak_sha256_first10, sk_sha256_first10).
    * Probes timeboxed 10s each · wall-time capped.
    * ListObjects capped at max_keys=5 per bucket · names/sizes only.
    * NO GetObject · NO PutObject · NO DeleteObject · NO ACL change.
    * Failure-layer classification distinguishes network from IAM:
      NO_KEYS_ON_FILE / DNS_FAIL / TCP_FAIL / TLS_FAIL /
      HTTP_403_INVALID_SIGNATURE / HTTP_403_PERMISSION_DENIED /
      HTTP_2XX_OK / OTHER.

Emits: phase0/connectivity_receipts/20260921T{HHMMSS}Z_HUAWEI_OBS_access_retry_owner_authorized.json
"""
from __future__ import annotations

import hashlib
import json
import os
import socket
import subprocess
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

CUSTODY_CSV = Path("/app/backend/estate_keys/data_sources/huawei_credentials.csv")
CUSTODY_CSV_ALT = Path("/app/backend/estate_keys/data_sources/huawei_credentials_2_20260916.csv")
DROP_MANIFEST = Path(
    "/app/assessment_workspace/phase0/credential_drop_manifests/"
    "20260916T1910Z_drop_manifest.json"
)
RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")
MASTER_ENDPOINT = "obs.ap-southeast-1.myhuaweicloud.com"  # proven at T7 20260914

# Per-call timebox (seconds).
PER_CALL_TIMEOUT_S = 10.0
# Wall-time cap for the per-bucket triple sweep (seconds).
WALL_TIME_CAP_S = 300.0


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _egress_ip() -> dict:
    """Try to determine the egress IP presented to remote hosts."""
    for label, url in (
        ("ifconfig.me", "https://ifconfig.me/ip"),
        ("api.ipify.org", "https://api.ipify.org"),
    ):
        try:
            out = subprocess.run(
                ["curl", "-sS", "--max-time", "6", url],
                capture_output=True, text=True, timeout=8,
            )
            if out.returncode == 0 and out.stdout.strip():
                return {label: out.stdout.strip()[:64]}
        except Exception:
            continue
    return {"error": "no_endpoint_returned"}


def _tcp_probe(host: str, port: int, timeout: float = 10.0) -> dict:
    """Timeboxed TCP connect probe."""
    t0 = time.monotonic()
    try:
        s = socket.create_connection((host, port), timeout=timeout)
        elapsed = time.monotonic() - t0
        s.close()
        return {"tcp_connected": True, "elapsed_s": round(elapsed, 3)}
    except socket.timeout:
        return {"tcp_connected": False, "failure_layer": "TCP_TIMEOUT"}
    except ConnectionRefusedError:
        return {"tcp_connected": False, "failure_layer": "TCP_REFUSED"}
    except socket.gaierror as e:
        return {"tcp_connected": False, "failure_layer": "DNS_FAIL", "error_msg": str(e)[:200]}
    except Exception as e:
        return {"tcp_connected": False, "failure_layer": "OTHER", "error_class": e.__class__.__name__, "error_msg": str(e)[:200]}


def _tls_probe(host: str, port: int, timeout: float = 10.0) -> dict:
    """Timeboxed TLS handshake probe to distinguish TLS-level failures."""
    import ssl
    t0 = time.monotonic()
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ss:
                cert = ss.getpeercert()
                return {
                    "tls_ok": True,
                    "elapsed_s": round(time.monotonic() - t0, 3),
                    "cert_subject_cn": next(
                        (v for k, v in [x for sub in (cert.get("subject") or []) for x in sub] if k == "commonName"),
                        None,
                    ),
                    "issuer_cn": next(
                        (v for k, v in [x for sub in (cert.get("issuer") or []) for x in sub] if k == "commonName"),
                        None,
                    ),
                    "not_after": cert.get("notAfter"),
                }
    except Exception as e:
        return {"tls_ok": False, "failure_layer": "TLS_FAIL",
                "error_class": e.__class__.__name__, "error_msg": str(e)[:200]}


def _parse_ak_sk(path: Path) -> tuple[str, str, dict]:
    """Read the credentials CSV via readline() only · returns (ak, sk, shape)."""
    with path.open("r", encoding="utf-8") as fh:
        raw = fh.readlines()
    lines = [ln.strip() for ln in raw if ln.strip()]
    shape = {"file_size_bytes": path.stat().st_size, "line_count_nonempty": len(lines)}
    if not lines:
        raise ValueError("csv empty")
    record = lines[-1]
    fields = [f.strip() for f in record.split(",")]
    fields = [f for f in fields if f]
    if len(fields) < 2:
        raise ValueError(f"cannot identify AK/SK in {len(fields)}-field record")
    # Positional-order preserved sort by length desc, take top 2.
    top_2 = sorted(fields, key=len, reverse=True)[:2]
    ordered = [f for f in fields if f in top_2]
    if len(ordered) < 2:
        raise ValueError("cannot identify two credential-shaped fields")
    ak, sk = ordered[0], ordered[1]
    shape.update({
        "ak_len": len(ak),
        "sk_len": len(sk),
        "ak_sha256_first10": hashlib.sha256(ak.encode()).hexdigest()[:10],
        "sk_sha256_first10": hashlib.sha256(sk.encode()).hexdigest()[:10],
        "ak_prefix2": ak[:2],  # Huawei AKs typically start with alnum · low-entropy hint
    })
    return ak, sk, shape


def _classify_obs_response(status: Optional[int], reason: Optional[str], errCode: Optional[str]) -> str:
    """Classify an OBS SDK response into a failure layer name."""
    if status is None:
        return "NO_HTTP_RESPONSE"
    if 200 <= status < 300:
        return "HTTP_2XX_OK"
    if status == 403:
        # Huawei error codes: SignatureDoesNotMatch = invalid signature/AK
        # AccessDenied = IAM policy denies operation.
        code = (errCode or "").strip()
        if code in ("SignatureDoesNotMatch", "InvalidAccessKeyId"):
            return "HTTP_403_INVALID_SIGNATURE"
        if code in ("AccessDenied", "AllAccessDisabled"):
            return "HTTP_403_PERMISSION_DENIED"
        return f"HTTP_403_UNCLASSIFIED_{code}" if code else "HTTP_403"
    if status == 404:
        return "HTTP_404"
    if status == 301 or status == 307:
        return f"HTTP_{status}_REDIRECT"
    if 400 <= status < 500:
        return f"HTTP_4XX_{status}"
    if 500 <= status < 600:
        return f"HTTP_5XX_{status}"
    return f"HTTP_{status}"


def _run_probe(ak: str, sk: str, master_endpoint: str, wall_cap: float) -> dict:
    """Run the full OBS survey: TCP/TLS to endpoint + ListBuckets + per-bucket
    HeadBucket + GetBucketLocation + ListObjects(max_keys=5). Returns matrix."""
    from obs import ObsClient

    result: dict = {
        "master_endpoint": master_endpoint,
        "tcp": _tcp_probe(master_endpoint, 443, timeout=PER_CALL_TIMEOUT_S),
        "tls": _tls_probe(master_endpoint, 443, timeout=PER_CALL_TIMEOUT_S),
    }
    if not result["tcp"].get("tcp_connected") or not result["tls"].get("tls_ok"):
        result["survey_aborted"] = "network-layer failure — see tcp/tls fields"
        return result

    # Env-inject (this-process only).
    os.environ["HUAWEI_AK_ID"] = ak
    os.environ["HUAWEI_SK"] = sk

    client = ObsClient(access_key_id=ak, secret_access_key=sk, server=master_endpoint)

    # 1) ListBuckets
    lb_t0 = time.monotonic()
    try:
        lb_resp = client.listBuckets()
    except Exception as e:
        result["list_buckets"] = {
            "outcome": "exception",
            "exception_type": e.__class__.__name__,
            "elapsed_s": round(time.monotonic() - lb_t0, 3),
        }
        client.close()
        return result

    lb_status = getattr(lb_resp, "status", None)
    lb_err_code = getattr(lb_resp, "errorCode", None)
    lb_body = getattr(lb_resp, "body", None)
    lb_buckets = list(getattr(lb_body, "buckets", None) or []) if lb_body else []
    lb_owner_id = getattr(lb_body, "owner", None) if lb_body else None
    result["list_buckets"] = {
        "outcome": "response_received",
        "status": lb_status,
        "reason": (getattr(lb_resp, "reason", None) or "")[:120],
        "errorCode": lb_err_code,
        "errorMessage_len": len(getattr(lb_resp, "errorMessage", None) or ""),
        "failure_layer": _classify_obs_response(lb_status, getattr(lb_resp, "reason", None), lb_err_code),
        "elapsed_s": round(time.monotonic() - lb_t0, 3),
        "n_buckets": len(lb_buckets),
        "owner_id_present": bool(lb_owner_id),
    }

    if lb_status is None or lb_status >= 400:
        client.close()
        return result

    # 2) Per-bucket: HeadBucket + GetBucketLocation + ListObjects(max_keys=5)
    per_bucket_matrix: list = []
    wall_t0 = time.monotonic()
    _region_client_cache: dict = {master_endpoint: client}

    for bkt in lb_buckets:
        if time.monotonic() - wall_t0 > wall_cap:
            per_bucket_matrix.append({
                "bucket": getattr(bkt, "name", "unknown"),
                "wall_time_cap_reached": True,
            })
            break

        bname = getattr(bkt, "name", "") or ""
        bkt_region_from_lb = (getattr(bkt, "location", "") or "").strip()
        row: dict = {
            "bucket": bname,
            "create_date": getattr(bkt, "create_date", "") or "",
            "location_from_listbuckets": bkt_region_from_lb,
        }

        # Route each per-bucket call to that bucket's home-region endpoint
        # if listBuckets told us where it lives; else fall back to master.
        if bkt_region_from_lb:
            region_endpoint = f"obs.{bkt_region_from_lb}.myhuaweicloud.com"
        else:
            region_endpoint = master_endpoint
        row["region_endpoint_used"] = region_endpoint

        # Build / cache per-region client (lazy · one per region).
        rc = _region_client_cache.get(region_endpoint)
        if rc is None:
            rc = ObsClient(access_key_id=ak, secret_access_key=sk, server=region_endpoint)
            _region_client_cache[region_endpoint] = rc
        per_bucket_client = rc

        # HeadBucket
        try:
            hb_t0 = time.monotonic()
            hb = per_bucket_client.headBucket(bname)
            hb_status = getattr(hb, "status", None)
            hb_err = getattr(hb, "errorCode", None)
            row["head_bucket"] = {
                "status": hb_status,
                "errorCode": hb_err,
                "failure_layer": _classify_obs_response(hb_status, None, hb_err),
                "elapsed_s": round(time.monotonic() - hb_t0, 3),
            }
        except Exception as e:
            row["head_bucket"] = {"outcome": "exception", "exception_type": e.__class__.__name__}

        # GetBucketLocation
        try:
            loc_t0 = time.monotonic()
            loc = per_bucket_client.getBucketLocation(bname)
            loc_status = getattr(loc, "status", None)
            loc_body = getattr(loc, "body", None)
            loc_region = getattr(loc_body, "location", "") if loc_body else ""
            row["get_bucket_location"] = {
                "status": loc_status,
                "region": loc_region,
                "failure_layer": _classify_obs_response(loc_status, None, getattr(loc, "errorCode", None)),
                "elapsed_s": round(time.monotonic() - loc_t0, 3),
            }
        except Exception as e:
            row["get_bucket_location"] = {"outcome": "exception", "exception_type": e.__class__.__name__}

        # ListObjects (max_keys=5, shape only)
        try:
            lo_t0 = time.monotonic()
            lo = per_bucket_client.listObjects(bname, max_keys=5)
            lo_status = getattr(lo, "status", None)
            lo_err = getattr(lo, "errorCode", None)
            lo_body = getattr(lo, "body", None)
            objs = list(getattr(lo_body, "contents", None) or []) if lo_body else []
            sample = [
                {
                    "key_len": len(getattr(o, "key", "") or ""),
                    "key_sha256_first10": hashlib.sha256((getattr(o, "key", "") or "").encode()).hexdigest()[:10],
                    "size_bytes": getattr(o, "size", None),
                }
                for o in objs
            ]
            row["list_objects"] = {
                "status": lo_status,
                "errorCode": lo_err,
                "failure_layer": _classify_obs_response(lo_status, None, lo_err),
                "elapsed_s": round(time.monotonic() - lo_t0, 3),
                "region_endpoint_used": region_endpoint,
                "count_returned_capped_5": len(objs),
                "is_truncated": bool(getattr(lo_body, "is_truncated", False)) if lo_body else False,
                "sample_shape_only_no_names": sample,
            }
        except Exception as e:
            row["list_objects"] = {"outcome": "exception", "exception_type": e.__class__.__name__}

        per_bucket_matrix.append(row)

    # Close all cached region clients.
    for rc in _region_client_cache.values():
        try:
            rc.close()
        except Exception:
            pass

    result["per_bucket"] = per_bucket_matrix
    result["per_bucket_wall_elapsed_s"] = round(time.monotonic() - wall_t0, 3)
    result["region_endpoints_used"] = sorted(_region_client_cache.keys())

    try:
        client.close()
    except Exception:
        pass

    # Summary counts
    n_ok_head = sum(1 for r in per_bucket_matrix if (r.get("head_bucket") or {}).get("failure_layer") == "HTTP_2XX_OK")
    n_ok_loc = sum(1 for r in per_bucket_matrix if (r.get("get_bucket_location") or {}).get("failure_layer") == "HTTP_2XX_OK")
    n_ok_lo = sum(1 for r in per_bucket_matrix if (r.get("list_objects") or {}).get("failure_layer") == "HTTP_2XX_OK")
    n_403_iam = sum(1 for r in per_bucket_matrix if (r.get("list_objects") or {}).get("failure_layer") == "HTTP_403_PERMISSION_DENIED")
    n_403_sig = sum(1 for r in per_bucket_matrix if (r.get("list_objects") or {}).get("failure_layer") == "HTTP_403_INVALID_SIGNATURE")
    result["summary"] = {
        "n_buckets_seen": len(lb_buckets),
        "n_buckets_probed": len(per_bucket_matrix),
        "n_head_2xx": n_ok_head,
        "n_location_2xx": n_ok_loc,
        "n_listobjects_2xx": n_ok_lo,
        "n_listobjects_403_iam": n_403_iam,
        "n_listobjects_403_signature": n_403_sig,
    }
    return result


def main() -> None:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    receipt: dict = {
        "task": "huawei_obs_access_retry_owner_authorized_20260921",
        "captured_at_utc": _now_utc(),
        "authorization": (
            "Owner priority directive this-session 2026-09-21T~12:55Z: "
            "'OWNER QUESTION → receipted drill (authorized now, non-"
            "interrupting to the R-91 hold): DO WE HAVE HUAWEI OBS "
            "(object storage) ACCESS with any banked access keys? ... "
            "Probes, timeboxed 10s each, in order: (a) ListBuckets; "
            "(b) for each visible bucket: HeadBucket + GetBucketLocation "
            "+ a ListObjects with max-keys=5 ... NO object downloads, "
            "NO writes, NO ACL changes. ... STOP after the survey.' "
            "R-91 hold unchanged."
        ),
        "cred_source": {
            "custody_file": str(CUSTODY_CSV),
            "custody_file_sha256": _sha256(CUSTODY_CSV) if CUSTODY_CSV.is_file() else None,
            "alt_custody_file": str(CUSTODY_CSV_ALT),
            "alt_custody_file_sha256": _sha256(CUSTODY_CSV_ALT) if CUSTODY_CSV_ALT.is_file() else None,
            "byte_identical_alt": (
                CUSTODY_CSV.is_file() and CUSTODY_CSV_ALT.is_file() and
                _sha256(CUSTODY_CSV) == _sha256(CUSTODY_CSV_ALT)
            ),
            "drop_manifest_sha256": _sha256(DROP_MANIFEST) if DROP_MANIFEST.is_file() else None,
        },
        "egress_ip_we_present": _egress_ip(),
        "master_endpoint": MASTER_ENDPOINT,
    }

    if not CUSTODY_CSV.is_file():
        receipt["outcome"] = "NO_KEYS_ON_FILE"
        _emit(receipt)
        return

    try:
        ak, sk, shape = _parse_ak_sk(CUSTODY_CSV)
    except Exception as e:
        receipt["outcome"] = "PARSE_FAIL"
        receipt["parse_exception_type"] = e.__class__.__name__
        receipt["parse_exception_message_len"] = len(str(e)) if str(e) else 0
        _emit(receipt)
        return

    receipt["cred_shape"] = shape

    try:
        probe = _run_probe(ak, sk, MASTER_ENDPOINT, WALL_TIME_CAP_S)
    except Exception as e:
        receipt["outcome"] = "PROBE_EXCEPTION"
        receipt["probe_exception_type"] = e.__class__.__name__
        receipt["probe_traceback"] = traceback.format_exc()[-1500:]
        # Wipe locals.
        ak = "***"; sk = "***"  # noqa: E702
        _emit(receipt)
        return

    # Wipe locals.
    ak = "***"; sk = "***"  # noqa: E702
    receipt["probe"] = probe
    receipt["outcome"] = "SURVEY_COMPLETE"
    _emit(receipt)


def _emit(receipt: dict) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = RECEIPT_DIR / f"{stamp}_HUAWEI_OBS_access_retry_owner_authorized.json"
    path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"receipt_path: {path}")


if __name__ == "__main__":
    main()
