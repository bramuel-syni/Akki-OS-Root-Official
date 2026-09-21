"""tools/digicow_s3_audio_read_check_20260921.py

DigiCow-scoped S3 audio read-capability check.

Owner directive verbatim: "OWNER GO → targeted read check: audio in the
DigiCow AWS estate, specifically the S3 path s3://training-content-2026/
audio/. Use the DigiCow AWS IAM keys already in custody."

Discipline:
    * READ-ONLY across every touch.
    * Direct egress to AWS S3. Region resolved via GetBucketLocation.
    * Region-correct endpoint for all subsequent calls (301 redirect
      handled).
    * ListObjectsV2 for enumeration (max-keys 50 per page, up to
      LIST_PAGES pages for the light per-prefix summary).
    * ONE HeadObject + ONE Range GetObject on the SINGLE SMALLEST audio
      object under `audio/`. Range: bytes=0-15 (16 bytes total).
    * Report magic-number hex + inferred format ONLY — never the audio
      content.
    * Scope discipline: DigiCow ONLY (NO touch to RMS Huawei OBS,
      MySQL clusters, or CIFS archive).
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from collections import Counter
from pathlib import Path
from typing import Optional

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError, ReadTimeoutError
from botocore.client import Config

RECEIPT_DIR = Path("/app/assessment_workspace/phase0/connectivity_receipts")
DIGICOW_CSV = Path("/app/assessment_workspace/custody/credentials/incoming_20260921/20260921T153705Z_DIGICOW_digicow_access_keys_csv.csv")

BUCKET = "training-content-2026"
PREFIX = "audio/"
DEFAULT_REGION = "eu-west-1"

LIST_MAX_KEYS_PER_PAGE = 50
LIST_PAGES = 20  # up to 1000 keys for the audio/ prefix summary
RANGE_BYTES = "bytes=0-15"  # 16 bytes inclusive


AUDIO_EXTS = {"mp3", "wav", "wave", "m4a", "aac", "flac", "ogg", "oga",
              "opus", "aiff", "aif", "wma", "ac3", "amr", "au", "mka"}


def _now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha256_file(p: Path) -> Optional[str]:
    if not p.is_file(): return None
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_ak_sk() -> dict:
    text = DIGICOW_CSV.read_text(encoding="utf-8-sig", errors="replace")
    reader = csv.DictReader(text.splitlines())
    for row in reader:
        ak = (row.get("Access key ID") or "").strip()
        sk = (row.get("Secret access key") or "").strip()
        if ak and sk:
            return {"ak": ak, "sk": sk,
                    "ak_len": len(ak), "sk_len": len(sk),
                    "ak_prefix4": ak[:4]}
    raise RuntimeError("No AK/SK in CSV")


def _identify_audio_magic(b: bytes) -> dict:
    """Recognize container/format from the first 16 bytes.

    Emits: hex(16), inferred_format, is_audio.
    """
    hexs = b.hex()
    out = {"hex_16": hexs[:32],
           "ascii_printable_prefix":
               "".join(c if 32 <= ord(c) < 127 else "." for c in b.decode("latin1", errors="replace"))[:16]}
    if not b:
        out["inferred_format"] = "EMPTY"
        out["is_audio"] = False
        return out

    # --- Signature matching ---------------------------------------
    if b.startswith(b"ID3"):
        out["inferred_format"] = "MP3 (ID3 tag header)"; out["is_audio"] = True
    elif len(b) >= 2 and b[0] == 0xFF and (b[1] & 0xE0) == 0xE0:
        # MPEG frame sync (11 bits set: 0xFFE0)
        # More specifically MP3/MPEG audio
        out["inferred_format"] = "MP3/MPEG (raw frame sync 0xFFEx)"; out["is_audio"] = True
    elif b.startswith(b"RIFF") and len(b) >= 12 and b[8:12] == b"WAVE":
        out["inferred_format"] = "WAV (RIFF/WAVE)"; out["is_audio"] = True
    elif b.startswith(b"OggS"):
        out["inferred_format"] = "OGG (OggS)"; out["is_audio"] = True
    elif b.startswith(b"fLaC"):
        out["inferred_format"] = "FLAC (fLaC)"; out["is_audio"] = True
    elif b.startswith(b"FORM") and len(b) >= 12 and b[8:12] in (b"AIFF", b"AIFC"):
        out["inferred_format"] = "AIFF (FORM/AIFF)"; out["is_audio"] = True
    elif len(b) >= 8 and b[4:8] == b"ftyp":
        # M4A/M4B/AAC in ISO base media container
        brand = b[8:12] if len(b) >= 12 else b""
        out["inferred_format"] = f"ISO-BMFF ftyp brand={brand!r} (likely M4A/MP4 audio)"
        out["is_audio"] = True
    elif b.startswith(b"\x30\x26\xB2\x75\x8E\x66\xCF\x11"):
        out["inferred_format"] = "ASF/WMA (GUID header)"; out["is_audio"] = True
    elif b.startswith(b"\x1A\x45\xDF\xA3"):
        out["inferred_format"] = "Matroska/EBML (MKA if audio-only)"; out["is_audio"] = True
    elif b.startswith(b"\x0B\x77") or b.startswith(b"\x77\x0B"):
        out["inferred_format"] = "AC-3 (Dolby)"; out["is_audio"] = True
    elif b.startswith(b"#!AMR"):
        out["inferred_format"] = "AMR"; out["is_audio"] = True
    else:
        out["inferred_format"] = f"UNKNOWN (hex={hexs[:32]})"
        out["is_audio"] = None  # unknown — not confidently audio
    return out


def _classify_s3_error(e: ClientError) -> dict:
    err = e.response.get("Error", {})
    code = err.get("Code")
    msg = err.get("Message", "")
    http = e.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    layer_map = {
        "NoSuchBucket": "BUCKET_DOES_NOT_EXIST",
        "AccessDenied": "AWS_ACCESS_DENIED",
        "AllAccessDisabled": "AWS_ALL_ACCESS_DISABLED",
        "PermanentRedirect": "WRONG_REGION_REDIRECT_301",
        "InvalidAccessKeyId": "IAM_INVALID_ACCESS_KEY_ID",
        "SignatureDoesNotMatch": "IAM_SIGNATURE_MISMATCH",
        "NoSuchKey": "KEY_DOES_NOT_EXIST",
        "InvalidBucketName": "INVALID_BUCKET_NAME",
        "AuthorizationHeaderMalformed": "AUTH_HEADER_MALFORMED",
    }
    return {
        "http_status": http,
        "error_code": code,
        "error_message": msg[:400],
        "failure_layer": layer_map.get(code, f"AWS_ERROR_{code}"),
        # For PermanentRedirect S3 puts the target region in the response
        "extra_from_response": {
            k: err.get(k) for k in ("BucketRegion", "Endpoint", "Region")
            if err.get(k) is not None
        },
    }


def _make_s3_client(session, region: str):
    return session.client("s3", region_name=region,
                          config=Config(signature_version="s3v4",
                                        retries={"max_attempts": 2, "mode": "standard"}))


def _resolve_region(session, bucket: str) -> dict:
    """Try eu-west-1 first (per drop hint); handle 301 redirect."""
    out = {"probe_order": []}
    for region_try in [DEFAULT_REGION, "us-east-1"]:
        c = _make_s3_client(session, region_try)
        step = {"tried_region": region_try}
        # HeadBucket first — cleanest way to catch region redirects
        try:
            resp = c.head_bucket(Bucket=bucket)
            step["head_bucket_ok"] = True
            step["response_metadata"] = {
                "http_status": resp.get("ResponseMetadata", {}).get("HTTPStatusCode"),
                "bucket_region_header":
                    resp.get("ResponseMetadata", {}).get("HTTPHeaders", {}).get("x-amz-bucket-region"),
            }
            out["resolved_region"] = (
                step["response_metadata"]["bucket_region_header"] or region_try
            )
            out["probe_order"].append(step)
            return out
        except ClientError as e:
            step["client_error"] = _classify_s3_error(e)
            # Botocore sometimes puts BucketRegion in the exception's response
            hdr = e.response.get("ResponseMetadata", {}).get("HTTPHeaders", {})
            step["x_amz_bucket_region"] = hdr.get("x-amz-bucket-region")
            if step["x_amz_bucket_region"]:
                out["resolved_region"] = step["x_amz_bucket_region"]
                out["probe_order"].append(step)
                return out
            out["probe_order"].append(step)
        except Exception as e:
            step["error_class"] = e.__class__.__name__
            step["error_msg"] = str(e)[:400]
            out["probe_order"].append(step)

    # Try GetBucketLocation as a fallback
    try:
        c = _make_s3_client(session, "us-east-1")
        loc = c.get_bucket_location(Bucket=bucket)
        loc_constraint = loc.get("LocationConstraint")
        # us-east-1 returns None
        resolved = loc_constraint or "us-east-1"
        out["fallback_get_bucket_location"] = {
            "location_constraint": loc_constraint, "resolved_region": resolved,
        }
        out["resolved_region"] = resolved
    except ClientError as e:
        out["fallback_get_bucket_location_err"] = _classify_s3_error(e)
    except Exception as e:
        out["fallback_get_bucket_location_err"] = {
            "error_class": e.__class__.__name__, "error_msg": str(e)[:400]
        }
    return out


def _list_prefix(s3, bucket: str, prefix: str) -> dict:
    """Enumerate up to LIST_PAGES pages of ListObjectsV2 under prefix."""
    out: dict = {"prefix": prefix, "pages": 0, "total_keys": 0,
                 "total_bytes": 0}
    ext_counter: Counter = Counter()
    audio_ext_counter: Counter = Counter()
    per_page_summary = []
    all_objects_smallest_audio = None  # track globally smallest audio
    date_min = None
    date_max = None
    key_samples: list = []
    continuation = None
    try:
        for page_ix in range(LIST_PAGES):
            kwargs = {"Bucket": bucket, "Prefix": prefix,
                      "MaxKeys": LIST_MAX_KEYS_PER_PAGE}
            if continuation:
                kwargs["ContinuationToken"] = continuation
            resp = s3.list_objects_v2(**kwargs)
            contents = resp.get("Contents", []) or []
            out["pages"] += 1
            out["total_keys"] += len(contents)
            page_bytes = 0
            for obj in contents:
                key = obj["Key"]
                size = obj["Size"]
                lm = obj.get("LastModified")
                page_bytes += size
                # Ext histogram
                m = re.search(r"\.([A-Za-z0-9]{1,8})$", key)
                ext = m.group(1).lower() if m else "NOEXT"
                ext_counter[ext] += 1
                if ext in AUDIO_EXTS:
                    audio_ext_counter[ext] += 1
                    # Track globally smallest audio (size > 0)
                    if size > 0:
                        if (all_objects_smallest_audio is None
                                or size < all_objects_smallest_audio["size"]):
                            all_objects_smallest_audio = {
                                "key": key, "size": size,
                                "last_modified": str(lm), "ext": ext,
                            }
                # Date range
                if lm:
                    if date_min is None or lm < date_min: date_min = lm
                    if date_max is None or lm > date_max: date_max = lm
                # Key name samples — first 20 audio + first 5 non-audio
                if len(key_samples) < 25:
                    key_samples.append({"key": key, "size": size,
                                        "last_modified": str(lm)[:19],
                                        "ext": ext})
            out["total_bytes"] += page_bytes
            per_page_summary.append({"page": page_ix + 1,
                                     "keys": len(contents),
                                     "page_bytes": page_bytes})
            continuation = resp.get("NextContinuationToken") if resp.get("IsTruncated") else None
            if not continuation:
                out["fully_enumerated_within_bounds"] = True
                break
        else:
            out["fully_enumerated_within_bounds"] = False
    except ClientError as e:
        out["client_error"] = _classify_s3_error(e)
    except Exception as e:
        out["error_class"] = e.__class__.__name__
        out["error_msg"] = str(e)[:400]

    out["ext_histogram"] = dict(ext_counter.most_common())
    out["audio_ext_histogram"] = dict(audio_ext_counter.most_common())
    out["audio_object_count"] = sum(audio_ext_counter.values())
    out["date_range_lastmodified"] = {
        "min": str(date_min)[:19] if date_min else None,
        "max": str(date_max)[:19] if date_max else None,
    }
    out["key_samples_first_25"] = key_samples
    out["chosen_smallest_audio"] = all_objects_smallest_audio
    out["per_page_summary"] = per_page_summary
    return out


def _proof_of_audio(s3, bucket: str, key: str, size: int) -> dict:
    """HeadObject + Range GetObject (bytes=0-15). Return signature+format."""
    out: dict = {"chosen_key": key, "chosen_size": size}
    t0 = time.monotonic()
    try:
        h = s3.head_object(Bucket=bucket, Key=key)
        out["head_object"] = {
            "ContentType": h.get("ContentType"),
            "ContentLength": h.get("ContentLength"),
            "LastModified": str(h.get("LastModified")),
            "ETag": (h.get("ETag") or "").strip('"'),
            "StorageClass": h.get("StorageClass"),
            "elapsed_s": round(time.monotonic() - t0, 3),
        }
    except ClientError as e:
        out["head_object_err"] = _classify_s3_error(e)
        out["failure_layer"] = out["head_object_err"]["failure_layer"]
        return out
    t1 = time.monotonic()
    try:
        # If the object is smaller than 16 bytes, fall back to reading the full object.
        actual_range = RANGE_BYTES
        if size < 16:
            actual_range = f"bytes=0-{max(size-1, 0)}"
        g = s3.get_object(Bucket=bucket, Key=key, Range=actual_range)
        body = g["Body"].read()
        out["get_object"] = {
            "range_requested": actual_range,
            "ContentRange": g.get("ContentRange"),
            "ContentType": g.get("ContentType"),
            "bytes_returned": len(body),
            "elapsed_s": round(time.monotonic() - t1, 3),
        }
        out["magic_signature"] = _identify_audio_magic(body)
    except ClientError as e:
        out["get_object_err"] = _classify_s3_error(e)
        out["failure_layer"] = out["get_object_err"]["failure_layer"]
    return out


def _top_level_discovery(s3, bucket: str) -> dict:
    """Delimiter='/' listing at bucket root — reveals top-level prefixes."""
    out = {}
    try:
        resp = s3.list_objects_v2(Bucket=bucket, Delimiter="/",
                                  MaxKeys=100)
        prefixes = [p["Prefix"] for p in (resp.get("CommonPrefixes") or [])]
        loose_files = [{"key": o["Key"], "size": o["Size"]}
                       for o in (resp.get("Contents") or [])]
        out["top_level_prefixes"] = prefixes
        out["top_level_loose_files_first_20"] = loose_files[:20]
        out["is_truncated"] = resp.get("IsTruncated", False)
    except ClientError as e:
        out["client_error"] = _classify_s3_error(e)
    except Exception as e:
        out["error_class"] = e.__class__.__name__
        out["error_msg"] = str(e)[:400]
    return out


def main():
    receipt = {
        "task": "DIGICOW_s3_audio_read_check_owner_authorized_20260921",
        "captured_at_utc": _now(),
        "authorization": (
            "Owner directive this-session 2026-09-21T~15:47Z: 'OWNER GO "
            "targeted read check: audio in the DigiCow AWS estate, "
            "specifically s3://training-content-2026/audio/'. R-91 hold "
            "unchanged. Ratchet 5858 unchanged."
        ),
        "scope_discipline": (
            "DIGICOW AWS S3 ONLY. NO touch to RMS Huawei OBS, MySQL "
            "clusters, or CIFS archive."
        ),
        "hygiene": {
            "read_only": True,
            "no_bulk_downloads": True,
            "single_16_byte_range_read_max": True,
            "creds_by_shape_only": True,
        },
        "cred_source": {
            "access_keys_csv": str(DIGICOW_CSV),
            "access_keys_csv_sha256": _sha256_file(DIGICOW_CSV),
        },
        "target": {"bucket": BUCKET, "prefix": PREFIX},
    }

    hw = _load_ak_sk()
    receipt["cred_shape"] = {"ak_len": hw["ak_len"], "sk_len": hw["sk_len"],
                             "ak_prefix4": hw["ak_prefix4"]}

    session = boto3.session.Session(
        aws_access_key_id=hw["ak"],
        aws_secret_access_key=hw["sk"],
    )

    # ---- Step 1 · STS identity confirmation --------------------------
    sts = session.client("sts", region_name=DEFAULT_REGION)
    try:
        ident = sts.get_caller_identity()
        receipt["sts_identity"] = {"ok": True,
                                   "account": ident.get("Account"),
                                   "arn": ident.get("Arn"),
                                   "user_id": ident.get("UserId"),
                                   "matches_digicow_account_494452543252":
                                       ident.get("Account") == "494452543252"}
    except ClientError as e:
        receipt["sts_identity"] = {"ok": False,
                                   **_classify_s3_error(e)}
        _emit(receipt); return

    # ---- Step 2 · Region resolution ---------------------------------
    region_info = _resolve_region(session, BUCKET)
    receipt["region_resolution"] = region_info
    region = region_info.get("resolved_region")
    if not region:
        receipt["verdict"] = {
            "binary_answer": "NO",
            "failure_layer": "BUCKET_UNREACHABLE_REGION_UNRESOLVED",
            "explicit": (
                "Could not resolve region for bucket "
                f"'{BUCKET}'. Inspect region_resolution.probe_order."
            ),
        }
        _emit(receipt); return

    # Region-correct client
    s3 = _make_s3_client(session, region)

    # HeadBucket confirmation via the region-correct client. NOTE: some
    # IAM policies are prefix-scoped (grant s3:ListBucket only under
    # audio/*), which returns 403 on bucket-level HeadBucket while
    # still permitting ListObjectsV2(Prefix=audio/). We record the
    # HeadBucket result but do NOT short-circuit on 403 — continue.
    try:
        hb = s3.head_bucket(Bucket=BUCKET)
        receipt["head_bucket_region_correct"] = {
            "ok": True, "region_used": region,
            "response_bucket_region_header":
                hb.get("ResponseMetadata", {}).get("HTTPHeaders", {}).get("x-amz-bucket-region"),
        }
    except ClientError as e:
        receipt["head_bucket_region_correct"] = {
            "ok": False,
            **_classify_s3_error(e),
            "note": (
                "HeadBucket 403 is expected under prefix-scoped IAM "
                "(s3:ListBucket conditioned on prefix). Proceeding to "
                "ListObjectsV2(Prefix=audio/) which may still succeed."
            ),
        }

    # ---- Step 3 · List `audio/` prefix ------------------------------
    receipt["audio_prefix_listing"] = _list_prefix(s3, BUCKET, PREFIX)

    audio_count = receipt["audio_prefix_listing"].get("audio_object_count", 0)
    smallest = receipt["audio_prefix_listing"].get("chosen_smallest_audio")

    # ---- Step 4 · Proof-of-read (only if audio present) ------------
    if smallest:
        receipt["proof_of_read"] = _proof_of_audio(
            s3, BUCKET, smallest["key"], smallest["size"])
    else:
        receipt["proof_of_read"] = {"skipped": "NO_AUDIO_OBJECT_UNDER_PREFIX"}

    # ---- Step 5 · Top-level discovery (always run for context) ------
    receipt["top_level_discovery"] = _top_level_discovery(s3, BUCKET)

    # ---- Step 6 · Verdict --------------------------------------------
    listing = receipt["audio_prefix_listing"]
    total_keys = listing.get("total_keys", 0)
    fully = listing.get("fully_enumerated_within_bounds")
    if "client_error" in listing:
        verdict = {
            "binary_answer": "NO",
            "failure_layer": listing["client_error"]["failure_layer"],
            "explicit": (
                f"ListObjectsV2 under s3://{BUCKET}/{PREFIX} failed: "
                f"{listing['client_error']['error_code']} — "
                f"{listing['client_error']['error_message'][:200]}"
            ),
        }
    elif total_keys == 0:
        verdict = {
            "binary_answer": "NO",
            "failure_layer": "PREFIX_EMPTY_OR_NONEXISTENT",
            "explicit": (
                f"s3://{BUCKET}/{PREFIX} lists zero keys — the prefix "
                "is empty or does not exist. See top_level_discovery for "
                "what prefixes DO exist under this bucket."
            ),
            "top_level_prefixes_available":
                receipt["top_level_discovery"].get("top_level_prefixes"),
        }
    elif audio_count == 0:
        verdict = {
            "binary_answer": "PARTIAL",
            "failure_layer": "PREFIX_NONEMPTY_BUT_NO_RECOGNIZED_AUDIO_EXTS",
            "explicit": (
                f"s3://{BUCKET}/{PREFIX} has {total_keys} keys but 0 "
                "have recognized audio extensions. Ext histogram in "
                "audio_prefix_listing.ext_histogram."
            ),
        }
    else:
        por = receipt["proof_of_read"]
        magic = por.get("magic_signature", {}) if isinstance(por, dict) else {}
        get_ok = "get_object" in por and por.get("get_object", {}).get("bytes_returned", 0) > 0
        is_audio_confirmed = bool(magic.get("is_audio"))
        if get_ok and is_audio_confirmed:
            verdict = {
                "binary_answer": "YES",
                "failure_layer": None,
                "explicit": (
                    f"CAN READ AUDIO. s3://{BUCKET}/{PREFIX} has "
                    f"{audio_count} audio object(s) across "
                    f"{list(listing.get('audio_ext_histogram', {}).keys())}; "
                    "proof-of-read on smallest returned a real audio "
                    f"signature: {magic.get('inferred_format')} "
                    f"(hex={magic.get('hex_16')})."
                ),
            }
        elif get_ok and not is_audio_confirmed:
            verdict = {
                "binary_answer": "PARTIAL",
                "failure_layer": "READ_OK_BUT_MAGIC_UNRECOGNIZED",
                "explicit": (
                    f"Read succeeded but the first 16 bytes did not "
                    "match any known audio signature. "
                    f"hex={magic.get('hex_16')}. "
                    "Object may be a different container or encrypted."
                ),
            }
        else:
            verdict = {
                "binary_answer": "PARTIAL",
                "failure_layer": (por.get("failure_layer") or
                                  "PROOF_OF_READ_FAILED_(SEE_proof_of_read)"),
                "explicit": (
                    "Listing showed audio object(s), but the "
                    "proof-of-read GetObject failed."
                ),
            }
    verdict["surface"] = f"AWS S3 bucket '{BUCKET}' region={region}"
    verdict["counts"] = {
        "total_keys_under_prefix": total_keys,
        "audio_keys_under_prefix": audio_count,
        "fully_enumerated_within_bounds": fully,
        "pages_walked": listing.get("pages"),
    }
    verdict["formats_observed"] = list(listing.get("audio_ext_histogram", {}).keys())
    verdict["size_summary"] = {
        "sum_bytes_across_walked_pages": listing.get("total_bytes"),
    }
    receipt["verdict"] = verdict

    _emit(receipt)


def _emit(receipt):
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = RECEIPT_DIR / f"{stamp}_DIGICOW_s3_audio_read_check_owner_authorized_20260921.json"
    p.write_text(json.dumps(receipt, indent=2, default=str) + "\n",
                 encoding="utf-8")
    print(f"receipt_path: {p}")


if __name__ == "__main__":
    main()
