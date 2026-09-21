"""services.response_sanitizer — Wave E CP-E7 shared response-boundary
sanitizer.

Owner ruling (Wave E scope §7 verbatim, 2026-08-27T~12:10Z):
    "Security/PII pass on the DigiCow paths: verify PII posture (the
     corpus contains farmer PII — ussd_users 2.28M rows), confirm the
     response-boundary sanitizer covers every new Wave E surface, and
     receipt the check."

The `sanitize` function strips banned fields (secrets + PII) from a
response dict before it leaves the pod boundary. Callers apply it to
any dict shape that could carry a leak (record from disk, model_dump
of a contract, third-party payload).

Banned-set composition:
  * `SECRET_BANNED_FIELDS` — canon-Watch discipline (Doc 8):
    password, secret, signing_material, aws_secret_access_key.
  * `DIGICOW_PII_BANNED_FIELDS` — measured from the DigiCow live
    connection record (phase0/data_connection_records/data_source_
    digicow_live_20260819T152513Z_FINAL.json). Owner declared
    ussd_users 2.28M rows carry farmer PII.
  * `_raw` suffix — any key ending with `_raw` is considered
    dye-tagged and stripped.
"""
from __future__ import annotations

from typing import Any, Dict


SECRET_BANNED_FIELDS = {
    "password", "secret", "signing_material", "aws_secret_access_key",
}

# Wave E CP-E7 · DigiCow PII column names measured from the connection
# record at phase0/data_connection_records/data_source_digicow_live_
# 20260819T152513Z_FINAL.json (ussd_users table).
#
# Wave-G5c-CLASSIFICATION-OCCUPATION · owner Ruling #2 (2026-08-28T~15:40Z,
# banked in STATE/DECISIONS.md) adds `occupation` to this set under the
# conservative-default policy for quasi-identifiers. See
# `pii_classification_registry.v0.json` alongside for the classification
# entry including the declassification path (exists but CLOSED until a
# documented linkage-risk assessment plus DPO sign-off).
DIGICOW_PII_BANNED_FIELDS = {
    "farmer_mobile_no",
    "farmer_answer",
    "occupation",
}

PII_BANNED_FIELDS = DIGICOW_PII_BANNED_FIELDS  # public alias

BANNED_FIELDS = SECRET_BANNED_FIELDS | DIGICOW_PII_BANNED_FIELDS


def sanitize(d: Dict[str, Any]) -> Dict[str, Any]:
    """Strip banned fields and any `_raw`-suffixed keys from a
    response body. Non-dict inputs are returned unchanged (list of
    dicts callers should map through this function themselves)."""
    if not isinstance(d, dict):
        return d
    return {
        k: v for k, v in d.items()
        if k not in BANNED_FIELDS and not k.endswith("_raw")
    }
