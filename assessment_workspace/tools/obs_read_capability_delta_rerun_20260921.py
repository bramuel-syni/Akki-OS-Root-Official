"""tools/obs_read_capability_delta_rerun_20260921.py

Delta re-run of Section D · OBS only, after SDK parameter fix in the
main sweep tool (listObjects uses `max_keys=`, not `maxKeys=`). Section B
(MySQL) already succeeded cleanly and is untouched.

Emits a supplement receipt banked alongside the main sweep receipt.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_TOOLS = Path("/app/assessment_workspace/tools")
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")
HUAWEI_CRED_CANDIDATES = [
    Path("/app/backend/estate_keys/data_sources/huawei_credentials_2_20260916.csv"),
    Path("/app/backend/estate_keys/data_sources/huawei_credentials.csv"),
]

BUCKET_SAMPLE = [
    ("2024offairrecs",         "af-south-1"),
    ("cal-docs",               "af-south-1"),
    ("chamgei-backup",         "af-south-1"),
    ("apr252017",              "tr-west-1"),
    ("feb272017",              "tr-west-1"),
    ("librarydirectupload2",   "tr-west-1"),
    ("citizen-vod",            "ap-southeast-3"),
    ("iso-rms-storage",        "ap-southeast-3"),
    ("rms-ai",                 "ap-southeast-1"),
]

RMS_AI_LIST_KEYS_FOR_SMALLEST = 20


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha256_file(p: Path) -> Optional[str]:
    if not p.is_file(): return None
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_ak_sk():
    for p in HUAWEI_CRED_CANDIDATES:
        if not p.is_file(): continue
        text = p.read_text(encoding="utf-8-sig", errors="replace")
        reader = csv.DictReader(text.splitlines())
        for row in reader:
            ak = (row.get("Access Key Id") or "").strip()
            sk = (row.get("Secret Access Key") or "").strip()
            if ak and sk:
                return {"path": str(p), "sha256": _sha256_file(p),
                        "ak_len": len(ak), "sk_len": len(sk),
                        "ak_prefix4": ak[:4],
                        "user_name": (row.get("User Name") or "").strip(),
                        "ak": ak, "sk": sk}
    return None


def _probe(client_factory, bucket, region, max_keys=5):
    endpoint = f"obs.{region}.myhuaweicloud.com"
    out = {"bucket": bucket, "region_assumed": region, "endpoint": endpoint}
    c = client_factory(endpoint)
    try:
        t0 = time.monotonic()
        head = c.headBucket(bucket)
        out["head_bucket"] = {"status": head.status,
                              "elapsed_s": round(time.monotonic() - t0, 3)}
        t1 = time.monotonic()
        lst = c.listObjects(bucket, max_keys=max_keys)
        lo = {"status": lst.status,
              "elapsed_s": round(time.monotonic() - t1, 3)}
        if lst.status < 300:
            body = lst.body
            lo["is_truncated"] = getattr(body, "is_truncated", None)
            contents = getattr(body, "contents", None) or []
            lo["count_returned"] = len(contents)
            lo["sample"] = [
                {"key": o.key,
                 "size_bytes": o.size,
                 "etag": (o.etag or "").strip('"'),
                 "last_modified": str(getattr(o, "lastModified", None))}
                for o in contents[:max_keys]
            ]
        else:
            lo["errorCode"] = getattr(lst, "errorCode", None)
            lo["errorMessage"] = getattr(lst, "errorMessage", None)
        out["list_objects"] = lo
    except Exception as e:
        out["error_class"] = e.__class__.__name__
        out["error_msg"] = str(e)[:300]
    finally:
        try: c.close()
        except Exception: pass
    return out


def _proof_of_read(client_factory):
    result = {"bucket": "rms-ai", "region": "ap-southeast-1"}
    endpoint = "obs.ap-southeast-1.myhuaweicloud.com"
    c = client_factory(endpoint)
    try:
        lst = c.listObjects("rms-ai", max_keys=RMS_AI_LIST_KEYS_FOR_SMALLEST)
        result["list_step"] = {"status": lst.status}
        if lst.status >= 300:
            result["failure_layer"] = f"LIST_HTTP_{lst.status}"
            return result
        contents = list(getattr(lst.body, "contents", None) or [])
        result["list_step"]["count_returned"] = len(contents)
        if not contents:
            result["failure_layer"] = "BUCKET_EMPTY_WITHIN_FIRST_N"
            return result
        smallest = min(contents, key=lambda o: o.size)
        result["chosen_object"] = {
            "key": smallest.key, "size_bytes": smallest.size,
            "etag": (smallest.etag or "").strip('"'),
            "last_modified": str(getattr(smallest, "lastModified", None)),
        }
        t = time.monotonic()
        resp = c.getObject("rms-ai", smallest.key, loadStreamInMemory=True)
        if resp.status >= 300:
            result["get_object"] = {"status": resp.status,
                                    "errorCode": getattr(resp, "errorCode", None),
                                    "elapsed_s": round(time.monotonic() - t, 3)}
            result["failure_layer"] = f"GET_HTTP_{resp.status}"
            return result
        buf = resp.body.buffer
        get_out = {
            "status": resp.status,
            "elapsed_s": round(time.monotonic() - t, 3),
            "content_length": len(buf),
            "sha256": _sha256_bytes(buf),
        }
        # headers
        try:
            hdrs = {k.lower(): v for k, v in (resp.header or [])}
            get_out["content_type"] = hdrs.get("content-type")
            get_out["etag_from_header"] = (hdrs.get("etag") or "").strip('"')
        except Exception:
            pass
        result["get_object"] = get_out
        # explicit drop of bytes
        del buf
    except Exception as e:
        result["error_class"] = e.__class__.__name__
        result["error_msg"] = str(e)[:300]
    finally:
        try: c.close()
        except Exception: pass
    return result


def main():
    hw = _load_ak_sk()
    from obs import ObsClient

    def mk(endpoint):
        return ObsClient(
            access_key_id=hw["ak"],
            secret_access_key=hw["sk"],
            server=endpoint,
            timeout=15,
        )

    receipt = {
        "task": "obs_read_capability_delta_rerun_20260921",
        "captured_at_utc": _now(),
        "predecessor_receipt": "phase0/connectivity_receipts/20260921T133821Z_FULL_ESTATE_read_capability_sweep_owner_authorized_20260921.json",
        "reason": (
            "Main sweep's OBS section failed with `TypeError: ObsClient."
            "listObjects() got an unexpected keyword argument 'maxKeys'` "
            "(SDK expects snake_case `max_keys=`). This delta re-runs "
            "ONLY Section D (OBS) with the corrected parameter name. "
            "MySQL + JUMP sizing + NAS remain unchanged and cited."
        ),
        "hygiene": {
            "read_only": True,
            "bytes_hashed_then_dropped": True,
            "creds_by_shape_only": True,
        },
        "credential_shape": {
            "path": hw["path"], "sha256": hw["sha256"],
            "ak_len": hw["ak_len"], "sk_len": hw["sk_len"],
            "ak_prefix4": hw["ak_prefix4"],
            "user_name_shape": {"len": len(hw["user_name"] or "")},
        },
    }

    per_bucket = []
    for bucket, region in BUCKET_SAMPLE:
        per_bucket.append(_probe(mk, bucket, region, max_keys=5))
    receipt["per_bucket_results"] = per_bucket

    receipt["proof_of_read_rms_ai"] = _proof_of_read(mk)

    # Region rollup
    rollup = {}
    for res in per_bucket:
        reg = res.get("region_assumed", "?")
        slot = rollup.setdefault(reg, {"buckets_probed": 0,
                                       "head_2xx": 0, "head_other": 0,
                                       "list_2xx": 0, "list_other": 0,
                                       "objects_visible_in_sample": 0,
                                       "bucket_names_readable": []})
        slot["buckets_probed"] += 1
        h = res.get("head_bucket", {}).get("status")
        if h and h < 300: slot["head_2xx"] += 1
        else: slot["head_other"] += 1
        lo = res.get("list_objects", {})
        if lo.get("status") and lo["status"] < 300:
            slot["list_2xx"] += 1
            slot["objects_visible_in_sample"] += lo.get("count_returned", 0) or 0
            slot["bucket_names_readable"].append(res["bucket"])
        else:
            slot["list_other"] += 1
    receipt["region_rollup"] = rollup

    # Explicit answer
    porr = receipt["proof_of_read_rms_ai"]
    por_ok = "get_object" in porr and porr["get_object"].get("status", 500) < 300
    receipt["explicit_answer"] = {
        "all_9_buckets_HeadBucket_2xx": all(
            b.get("head_bucket", {}).get("status") == 200 for b in per_bucket),
        "list_objects_success_regions": [
            reg for reg, s in rollup.items() if s.get("list_2xx", 0) > 0
        ],
        "list_objects_failure_regions": [
            reg for reg, s in rollup.items() if s.get("list_2xx", 0) == 0
        ],
        "get_object_rms_ai_proof_ok": por_ok,
        "get_object_details": porr.get("get_object") if por_ok else None,
        "verdict": (
            "CAN_READ_OBS_OBJECTS_END_TO_END" if por_ok else
            "PARTIAL_HEADS_OK_LIST_OR_GET_FAILED"
        ),
    }

    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = RECEIPT_DIR / f"{stamp}_OBS_read_capability_delta_rerun_20260921.json"
    p.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                 encoding="utf-8")
    print(f"receipt_path: {p}")


if __name__ == "__main__":
    main()
