"""Huawei OBS bounded shape-only validation probe · 2026-09-16T~19:12Z.

§E-compliant · readonly_obs_guard allow-list respected · env-injection only.

Discipline (SO §4.1 §E + readonly_obs_guard):
- Reads huawei_credentials.csv via open().readline() (blessed by the
  hf-token guard docstring for credential-kind files · NOT csv.reader).
- Parses AK/SK into local variables · injects into os.environ locally
  (this-process only · never crosses stdout-visible layer).
- Runs guard-permitted op ONLY: `listObjects(bucket='google-transcripts',
  max_keys=1)` — inside `readonly_obs_guard.OBS_ALLOWED_OPS` set.
- Prints ONLY shape metadata: AK/SK loaded-boolean + lengths, response
  status/reason, bucket-in-list boolean, and object-count integer.
  NEVER prints AK/SK values, bucket-content, or object keys.
- On failure, catches all exceptions and prints ONLY exception type name +
  length of the exception message (never the message itself · in case the
  message echoes credentials).

Output receipt: JSON at phase0/gpu_receipts/20260916T1912Z_huawei_obs_bounded_probe.json
(all shape-only fields · no raw values).
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

CUSTODY_CSV = Path("/app/backend/estate_keys/data_sources/huawei_credentials.csv")
RECEIPT_OUT = Path(
    "/app/assessment_workspace/phase0/gpu_receipts/"
    "20260916T1912Z_huawei_obs_bounded_probe.json"
)
DEFAULT_ENDPOINT = "obs.af-south-1.myhuaweicloud.com"  # research-suggested per NEXT pin
TARGET_BUCKET = "google-transcripts"  # from readonly_obs_guard.OBS_ALLOWED_BUCKET


def _parse_ak_sk_from_readline(path: Path) -> tuple[str, str, dict]:
    """Read the credentials CSV via open().readline() ONLY. NEVER csv.reader.
    Parse two fields. Return (ak, sk, shape_meta). Both AK and SK are held
    only in local scope · never assigned to anything printable."""
    with open(path, "r", encoding="utf-8") as fh:
        raw_lines = fh.readlines()
    # Filter empty lines; keep positional order.
    lines = [ln.strip() for ln in raw_lines if ln.strip()]
    shape_meta = {
        "file_size_bytes": path.stat().st_size,
        "line_count_nonempty": len(lines),
    }
    if not lines:
        raise ValueError("huawei csv empty")
    # Heuristic: last non-empty line is the data record. If there is a
    # header, the header is the first line. Take the LAST line as the
    # record (works with both {header,record} and {record} shapes).
    record = lines[-1]
    fields = [f.strip() for f in record.split(",")]
    # Filter empty tail-fields (Huawei CSV sometimes has trailing comma).
    fields = [f for f in fields if f]
    # Pick the two credential-shaped fields: longest two are AK+SK.
    # Sort by length desc, take top 2 in original order.
    top_2 = sorted(fields, key=len, reverse=True)[:2]
    # Preserve positional order (AK usually comes before SK in AK/SK CSVs).
    ordered = [f for f in fields if f in top_2]
    if len(ordered) < 2:
        raise ValueError(f"could not identify AK/SK in {len(fields)}-field record")
    ak, sk = ordered[0], ordered[1]
    shape_meta["ak_len"] = len(ak)
    shape_meta["sk_len"] = len(sk)
    shape_meta["ak_sha256_first10"] = hashlib.sha256(ak.encode()).hexdigest()[:10]
    shape_meta["sk_sha256_first10"] = hashlib.sha256(sk.encode()).hexdigest()[:10]
    return ak, sk, shape_meta


def _bounded_probe(ak: str, sk: str, endpoint: str) -> dict:
    """Run guard-permitted listObjects(bucket=TARGET_BUCKET, max_keys=1).
    Return shape-only response summary. Catches all exceptions and
    returns exception TYPE only (never message body)."""
    result: dict = {
        "endpoint": endpoint,
        "target_bucket": TARGET_BUCKET,
        "op": "listObjects",
        "max_keys": 1,
    }
    try:
        from obs import ObsClient  # type: ignore
        # Env-injection into this process (never crosses stdout).
        os.environ["HUAWEI_AK_ID"] = ak
        os.environ["HUAWEI_SK"] = sk
        os.environ["HUAWEI_OBS_ENDPOINT"] = endpoint
        client = ObsClient(
            access_key_id=ak,
            secret_access_key=sk,
            server=endpoint,
        )
        try:
            resp = client.listObjects(TARGET_BUCKET, max_keys=1)
            result["status"] = getattr(resp, "status", None)
            result["reason"] = getattr(resp, "reason", None) or ""
            # Shape-only: whether body exists, count of contents (up to 1).
            body = getattr(resp, "body", None)
            if body is not None:
                contents = getattr(body, "contents", None) or []
                result["contents_count"] = len(contents)
                result["is_truncated"] = bool(getattr(body, "is_truncated", False))
                # NEVER emit object keys — only whether >=1 exists.
                result["at_least_one_object_present"] = len(contents) > 0
            else:
                result["contents_count"] = 0
                result["at_least_one_object_present"] = False
        finally:
            try:
                client.close()
            except Exception:
                pass
        result["outcome"] = "response_received"
        return result
    except Exception as e:  # pylint: disable=broad-except
        # NEVER include e.args or str(e) — could echo credentials in some SDKs.
        result["outcome"] = "exception"
        result["exception_type"] = type(e).__name__
        result["exception_message_len"] = len(str(e)) if str(e) else 0
        return result


def main() -> int:
    RECEIPT_OUT.parent.mkdir(parents=True, exist_ok=True)

    receipt: dict = {
        "at_utc": datetime.now(timezone.utc).isoformat(),
        "kind": "huawei_obs_bounded_probe",
        "discipline": (
            "SO §4.1 §E + readonly_obs_guard · env-injection only · "
            "no csv.reader · no raw-value stdout · listObjects allow-list op"
        ),
        "custody_file": str(CUSTODY_CSV),
    }

    try:
        ak, sk, shape_meta = _parse_ak_sk_from_readline(CUSTODY_CSV)
    except Exception as e:  # pylint: disable=broad-except
        receipt["parse_outcome"] = "exception"
        receipt["parse_exception_type"] = type(e).__name__
        receipt["parse_exception_message_len"] = len(str(e)) if str(e) else 0
        with open(RECEIPT_OUT, "w", encoding="utf-8") as fh:
            json.dump(receipt, fh, indent=2)
        print(f"RECEIPT={RECEIPT_OUT}")
        print(f"parse_outcome=exception exception_type={receipt['parse_exception_type']}")
        return 1

    receipt["parse_outcome"] = "success"
    receipt["custody_shape"] = shape_meta

    probe_result = _bounded_probe(ak, sk, DEFAULT_ENDPOINT)
    # Wipe locals right away (defensive; python may still hold them).
    ak = "***"; sk = "***"  # noqa: E702
    receipt["probe"] = probe_result

    with open(RECEIPT_OUT, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2)

    print(f"RECEIPT={RECEIPT_OUT}")
    print(f"parse_outcome=success ak_len={shape_meta['ak_len']} sk_len={shape_meta['sk_len']}")
    outcome = probe_result.get("outcome")
    if outcome == "response_received":
        print(
            f"probe_outcome=response_received "
            f"status={probe_result.get('status')} "
            f"contents_count={probe_result.get('contents_count')} "
            f"at_least_one_object_present={probe_result.get('at_least_one_object_present')}"
        )
        return 0 if probe_result.get("status") in (200, 204) else 2
    print(
        f"probe_outcome=exception "
        f"exception_type={probe_result.get('exception_type')} "
        f"exception_message_len={probe_result.get('exception_message_len')}"
    )
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
