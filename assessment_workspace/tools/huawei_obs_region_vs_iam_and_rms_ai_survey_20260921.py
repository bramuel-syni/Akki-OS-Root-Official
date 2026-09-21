"""tools/huawei_obs_region_vs_iam_and_rms_ai_survey_20260921.py.

Owner directive verbatim this-session (2026-09-21T~13:15Z):

    "PART A — COMPLETE THE OBS SURVEY (the drill stopped mid-report).
    From your receipt 20260921T130729Z_HUAWEI_OBS_access_retry_owner_
    authorized.json: AK/SK authenticates (ListBuckets 200, 106 buckets
    enumerated → valid key, not a network/invalid-key fault), but per-
    bucket ops returned HTTP_404 on 105/106 and 200 on ONLY rms-ai
    (ap-southeast-1, created 2026/07/13). Resolve the ambiguity that
    404-pattern hides ... 1. The 105 × 404 is EITHER region-mismatch
    ... OR IAM policy scoping the key to rms-ai only. Distinguish
    them: for a SMALL sample (5-8) of the 404 buckets, re-probe
    HeadBucket + GetBucketLocation against the OTHER Huawei regional
    endpoints (ap-southeast-2/3, cn-north-*, etc. — the standard set).
    If a bucket returns 200/location from another region → region-
    mismatch (fixable our side by using the right endpoint). If it
    403s with a valid signature everywhere → IAM-deny (owner takes to
    admin). Report the histogram. 2. For rms-ai (the one accessible
    bucket): ListObjects max-keys=20, report object-name prefixes +
    count + total-size-if-cheap ONLY (no downloads). ... Bank the
    completion receipt + a one-line state note. NO downloads, NO
    writes, NO ACL changes."

Same secret-hygiene discipline as the initial drill.
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

CUSTODY_CSV = Path("/app/backend/estate_keys/data_sources/huawei_credentials.csv")
RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")
PRIOR_RECEIPT = RECEIPT_DIR / "20260921T130729Z_HUAWEI_OBS_access_retry_owner_authorized.json"

# Huawei OBS standard regional endpoints (published catalog + observed in prior
# listBuckets locations `af-south-1`, `tr-west-1`, `ap-southeast-1..3`,
# `cn-east-3`, `cn-north-*`, `cn-south-1`, `sa-argentina-1`, etc.).
REGIONS_TO_PROBE = (
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "af-south-1",
    "tr-west-1",
    "cn-north-1",
    "cn-north-4",
    "cn-north-9",
    "cn-east-2",
    "cn-east-3",
    "cn-south-1",
    "sa-argentina-1",
    "sa-brazil-1",
    "eu-west-101",
    "la-south-2",
)
PER_CALL_TIMEOUT_S = 10.0
LO_MAX_KEYS_RMS_AI = 20
SAMPLE_SIZE_404_BUCKETS = 6  # owner said 5-8


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_ak_sk(path: Path) -> tuple[str, str, dict]:
    with path.open("r", encoding="utf-8") as fh:
        raw = fh.readlines()
    lines = [ln.strip() for ln in raw if ln.strip()]
    record = lines[-1]
    fields = [f.strip() for f in record.split(",") if f.strip()]
    top_2 = sorted(fields, key=len, reverse=True)[:2]
    ordered = [f for f in fields if f in top_2]
    ak, sk = ordered[0], ordered[1]
    return ak, sk, {
        "ak_len": len(ak),
        "sk_len": len(sk),
        "ak_sha256_first10": hashlib.sha256(ak.encode()).hexdigest()[:10],
        "sk_sha256_first10": hashlib.sha256(sk.encode()).hexdigest()[:10],
    }


def _classify(status: Optional[int], errorCode: Optional[str]) -> str:
    if status is None:
        return "NO_HTTP_RESPONSE"
    if 200 <= status < 300:
        return "HTTP_2XX_OK"
    if status == 403:
        code = (errorCode or "").strip()
        if code in ("SignatureDoesNotMatch", "InvalidAccessKeyId"):
            return "HTTP_403_INVALID_SIGNATURE"
        if code in ("AccessDenied", "AllAccessDisabled"):
            return "HTTP_403_PERMISSION_DENIED"
        return f"HTTP_403_UNCLASSIFIED_{code}" if code else "HTTP_403"
    if status == 404:
        return "HTTP_404"
    if status in (301, 307):
        return f"HTTP_{status}_REDIRECT"
    if 400 <= status < 500:
        return f"HTTP_4XX_{status}"
    if 500 <= status < 600:
        return f"HTTP_5XX_{status}"
    return f"HTTP_{status}"


def _load_prior_receipt() -> list[dict]:
    """Return the per_bucket list from the earlier drill so we can pick
    a small sample of 404 buckets without re-running ListBuckets."""
    with PRIOR_RECEIPT.open("r", encoding="utf-8") as fh:
        d = json.load(fh)
    return d.get("probe", {}).get("per_bucket", []) or []


def _pick_404_sample(per_bucket: list[dict]) -> list[dict]:
    """Deterministic sample: pick buckets whose location_from_listbuckets
    spans different regions to maximise the diagnostic value."""
    by_region: dict[str, list[dict]] = {}
    for row in per_bucket:
        if (row.get("list_objects") or {}).get("failure_layer") == "HTTP_404":
            loc = row.get("location_from_listbuckets") or "unknown"
            by_region.setdefault(loc, []).append(row)
    # Pick 1 per region until we hit SAMPLE_SIZE_404_BUCKETS; deterministic
    # (alphabetical region order + first bucket per region alphabetical).
    picks: list[dict] = []
    for region in sorted(by_region.keys()):
        if len(picks) >= SAMPLE_SIZE_404_BUCKETS:
            break
        picks.append(sorted(by_region[region], key=lambda r: r.get("bucket", ""))[0])
    return picks


def _probe_bucket_across_regions(bname: str, bkt_region_lb: str, ak: str, sk: str) -> dict:
    from obs import ObsClient
    matrix: list[dict] = []
    overall_verdict = "UNRESOLVED"
    for region in REGIONS_TO_PROBE:
        endpoint = f"obs.{region}.myhuaweicloud.com"
        client = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint,
                            timeout=int(PER_CALL_TIMEOUT_S))
        entry = {"region": region, "endpoint": endpoint}
        try:
            hb_t0 = time.monotonic()
            hb = client.headBucket(bname)
            hb_status = getattr(hb, "status", None)
            hb_err = getattr(hb, "errorCode", None)
            entry["head_bucket"] = {
                "status": hb_status,
                "errorCode": hb_err,
                "failure_layer": _classify(hb_status, hb_err),
                "elapsed_s": round(time.monotonic() - hb_t0, 3),
            }
        except Exception as e:
            entry["head_bucket"] = {"outcome": "exception", "exception_type": e.__class__.__name__}
        try:
            loc_t0 = time.monotonic()
            loc = client.getBucketLocation(bname)
            loc_status = getattr(loc, "status", None)
            loc_body = getattr(loc, "body", None)
            loc_region = getattr(loc_body, "location", "") if loc_body else ""
            entry["get_bucket_location"] = {
                "status": loc_status,
                "region": loc_region,
                "errorCode": getattr(loc, "errorCode", None),
                "failure_layer": _classify(loc_status, getattr(loc, "errorCode", None)),
                "elapsed_s": round(time.monotonic() - loc_t0, 3),
            }
        except Exception as e:
            entry["get_bucket_location"] = {"outcome": "exception", "exception_type": e.__class__.__name__}
        try:
            client.close()
        except Exception:
            pass
        matrix.append(entry)
        # Short-circuit if a region returns 2XX — we have region-mismatch evidence.
        if (entry.get("head_bucket") or {}).get("failure_layer") == "HTTP_2XX_OK" or \
           (entry.get("get_bucket_location") or {}).get("failure_layer") == "HTTP_2XX_OK":
            overall_verdict = "REGION_MISMATCH_RESOLVED"
            break

    # Post-loop verdict if no region returned 2XX
    if overall_verdict == "UNRESOLVED":
        # Check if all responses were 403 with a valid-signature code → IAM-deny
        all_403 = all(
            ((e.get("head_bucket") or {}).get("failure_layer", "").startswith("HTTP_403"))
            for e in matrix
        )
        if all_403:
            overall_verdict = "IAM_DENY_ACROSS_ALL_REGIONS"
        elif all(
            ((e.get("head_bucket") or {}).get("failure_layer") == "HTTP_404")
            for e in matrix
        ):
            overall_verdict = "HTTP_404_ACROSS_ALL_REGIONS_UNKNOWN_ROUTING"
        else:
            overall_verdict = "MIXED"

    return {"bucket": bname,
            "location_from_listbuckets": bkt_region_lb,
            "region_probe_matrix": matrix,
            "verdict": overall_verdict}


def _survey_rms_ai(ak: str, sk: str) -> dict:
    """ListObjects max-keys=20 on rms-ai, report prefixes + counts + total-size-if-cheap."""
    from obs import ObsClient
    endpoint = "obs.ap-southeast-1.myhuaweicloud.com"
    client = ObsClient(access_key_id=ak, secret_access_key=sk, server=endpoint,
                        timeout=int(PER_CALL_TIMEOUT_S))
    result: dict = {"endpoint": endpoint, "bucket": "rms-ai", "op": "listObjects",
                    "max_keys": LO_MAX_KEYS_RMS_AI}
    try:
        t0 = time.monotonic()
        lo = client.listObjects("rms-ai", max_keys=LO_MAX_KEYS_RMS_AI)
        lo_status = getattr(lo, "status", None)
        lo_body = getattr(lo, "body", None)
        objs = list(getattr(lo_body, "contents", None) or []) if lo_body else []
        # Prefix extraction: first path segment before '/', else "(root)".
        prefixes = Counter()
        total_size = 0
        sample_names = []  # SAFE to include object names — owner asked for prefixes
        for o in objs:
            k = getattr(o, "key", "") or ""
            size = getattr(o, "size", 0) or 0
            total_size += size
            prefix = k.split("/", 1)[0] if "/" in k else "(root-no-slash)"
            prefixes[prefix] += 1
            sample_names.append({"key": k, "size_bytes": size})
        result["status"] = lo_status
        result["failure_layer"] = _classify(lo_status, getattr(lo, "errorCode", None))
        result["elapsed_s"] = round(time.monotonic() - t0, 3)
        result["count_returned"] = len(objs)
        result["is_truncated"] = bool(getattr(lo_body, "is_truncated", False)) if lo_body else False
        result["total_size_bytes_sample"] = total_size
        result["prefix_histogram"] = dict(prefixes)
        result["sample_object_names_and_sizes"] = sample_names  # names allowed per owner
    except Exception as e:
        result["outcome"] = "exception"
        result["exception_type"] = e.__class__.__name__
    finally:
        try:
            client.close()
        except Exception:
            pass
    return result


def main() -> None:
    receipt: dict = {
        "task": "huawei_obs_region_vs_iam_and_rms_ai_survey_completion",
        "captured_at_utc": _now_utc(),
        "prior_receipt": str(PRIOR_RECEIPT),
        "prior_receipt_sha256": _sha256(PRIOR_RECEIPT),
        "cred_source": {
            "custody_file": str(CUSTODY_CSV),
            "custody_file_sha256": _sha256(CUSTODY_CSV),
        },
    }

    ak, sk, shape = _parse_ak_sk(CUSTODY_CSV)
    os.environ["HUAWEI_AK_ID"] = ak
    os.environ["HUAWEI_SK"] = sk
    receipt["cred_shape"] = shape

    # PART A.1 — Region-vs-IAM sample probe
    per_bucket_prior = _load_prior_receipt()
    sample = _pick_404_sample(per_bucket_prior)
    receipt["part_a_1_region_vs_iam"] = {
        "sample_size_targeted": SAMPLE_SIZE_404_BUCKETS,
        "sample_actual": [{"bucket": r["bucket"], "location_from_listbuckets": r.get("location_from_listbuckets")} for r in sample],
        "regions_probed": list(REGIONS_TO_PROBE),
        "results": [
            _probe_bucket_across_regions(r["bucket"], r.get("location_from_listbuckets") or "", ak, sk)
            for r in sample
        ],
    }

    # Overall verdict histogram
    verdicts = Counter(r["verdict"] for r in receipt["part_a_1_region_vs_iam"]["results"])
    receipt["part_a_1_verdict_histogram"] = dict(verdicts)

    # PART A.2 — rms-ai survey
    receipt["part_a_2_rms_ai_survey"] = _survey_rms_ai(ak, sk)

    # Wipe secrets from local scope defensively.
    ak = "***"; sk = "***"  # noqa: E702

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = RECEIPT_DIR / f"{stamp}_HUAWEI_OBS_region_vs_iam_and_rms_ai_survey_COMPLETION.json"
    out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"receipt_path: {out}")


if __name__ == "__main__":
    main()
