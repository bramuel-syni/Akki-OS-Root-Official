"""parser.py — deterministic pattern-only paste parser.

HARD RULES (Owner Simplification Ruling 2026-08-14 · DECISIONS.md §492-508):
  * No LLM SDK, no HTTP client, no external process, no answering-side shield.
  * No socket, no subprocess. Pure in-process regex/string logic.
  * Anything richer (semantic disambiguation, entity extraction) is refused
    by design — the owner will paste again or use the manual fallback fields.

Supported paste shapes:
  * ``Label: value`` — colon delimiter, whitespace-tolerant.
  * ``Label = value`` — equals delimiter, whitespace-tolerant.

Label matching is case-insensitive against a fixed synonym table (see
``LABEL_SYNONYMS`` below). Unmapped label lines fall through into ``extras``
so the caller can render them for owner review; they never silently map onto
a known field.

Compute-kind shape is the AISCA Output panel (screenshot in
``fixtures/AISCA_GPU_Access_Guide.pdf`` Fig 9-10): Host Name / Username /
Password / Public IP / Private IP / OS / Ephemeral Storage.
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Field taxonomy per kind
# ---------------------------------------------------------------------------

SUPPORTED_KINDS: Tuple[str, ...] = ("compute", "data-source", "llm", "trained-model")

# Canonical field name -> list of accepted label synonyms (case-insensitive).
# Order matters only for auto-detect scoring (see _score_kind).
FIELD_SYNONYMS: Dict[str, Dict[str, List[str]]] = {
    "compute": {
        "host_name": ["host name", "hostname", "host", "vm name", "machine name"],
        "username": ["username", "user name", "user", "login"],
        "password": ["password", "pass", "pwd"],
        "public_ip": ["public ip", "public ip address", "external ip", "ip", "ip address"],
        "private_ip": ["private ip", "private ip address", "internal ip"],
        "os": ["os", "operating system", "image"],
        "ephemeral_storage": ["ephemeral storage", "storage", "disk"],
        "deploy_date": ["deploy date", "deployment date", "deployed", "created"],
    },
    "data-source": {
        "source_name": ["source name", "dataset name", "name"],
        "endpoint": ["endpoint", "url", "uri"],
        "username": ["username", "user"],
        "password": ["password", "pass"],
        "notes": ["notes", "note", "description"],
        # Owner Ruling 2026-08-18 · FL-P2-23 · Aurora RDS Data API shape
        "aws_access_key_id": ["aws access key id", "access key id", "access key", "aws_access_key_id"],
        "aws_secret_access_key": ["aws secret access key", "secret access key", "aws_secret_access_key", "secret key"],
        "region": ["region", "aws region"],
        "cluster_arn": ["cluster arn", "resource arn", "db cluster arn", "cluster_arn"],
        "secret_arn": ["secret arn", "secrets manager arn", "secret_arn"],
        "database": ["database", "database name", "db name", "schema"],
    },
    "llm": {
        "provider": ["provider", "vendor"],
        "model": ["model", "model name", "engine"],
        "endpoint": ["endpoint", "url", "uri"],
        "api_key": ["api key", "apikey", "key", "token", "password"],
    },
    "trained-model": {
        "model_name": ["model name", "name"],
        "checkpoint_uri": ["checkpoint uri", "checkpoint", "artifact uri", "uri"],
        "sha256": ["sha256", "hash", "digest"],
        "provenance": ["provenance", "trained by", "author"],
    },
}


# Required fields per kind — used to compute the "missing" report.
REQUIRED_FIELDS: Dict[str, Tuple[str, ...]] = {
    "compute": ("host_name", "username", "password", "public_ip"),
    # Owner Ruling 2026-08-18 · FL-P2-23 · Aurora RDS Data API shape.
    # Data API needs at minimum: region + cluster_arn + secret_arn. The
    # aws_* IAM key/secret can be supplied for SigV4, but the secret_arn is
    # what the Data API actually reads for the DB user credentials.
    "data-source": ("region", "cluster_arn", "secret_arn"),
    "llm": ("provider", "model"),
    "trained-model": ("model_name", "checkpoint_uri"),
}


# ---------------------------------------------------------------------------
# Line-level regex — deliberately conservative. Accepts either `:` or `=` as
# the separator. Value captures the remainder of the line (whitespace
# stripped).
# ---------------------------------------------------------------------------

_LINE_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9 _\-/]{0,63})\s*[:=]\s*(.+?)\s*$")


def _label_to_canonical(label: str, kind: str) -> Optional[str]:
    """Return the canonical field key for a raw label, or None if unmapped.

    Case-insensitive. Extra internal whitespace collapses to single spaces.
    """
    norm = re.sub(r"\s+", " ", label.strip().lower())
    for canonical, synonyms in FIELD_SYNONYMS[kind].items():
        if norm in synonyms:
            return canonical
    return None


def _score_kind(text: str) -> str:
    """Deterministic auto-detect: count matched labels per kind, pick winner.

    Ties break to "compute" (the AISCA path is the operative one right now
    per owner ruling — this is not a judgement call, it is a documented tie
    break).
    """
    counts: Dict[str, int] = {k: 0 for k in SUPPORTED_KINDS}
    for raw_line in text.splitlines():
        m = _LINE_RE.match(raw_line)
        if not m:
            continue
        label = m.group(1)
        for kind in SUPPORTED_KINDS:
            if _label_to_canonical(label, kind) is not None:
                counts[kind] += 1

    # Tie-break: compute wins ties (documented above).
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], 0 if kv[0] == "compute" else 1))
    winner, top = ordered[0]
    if top == 0:
        # No labels matched anywhere — still default to compute so the missing
        # report lists compute's required fields; caller can override.
        return "compute"
    return winner


def parse(text: str, hint_kind: Optional[str] = None) -> Dict[str, object]:
    """Parse a paste blob into structured fields.

    Args:
      text: The raw paste. May contain non-label lines (banners, comments);
        they are ignored.
      hint_kind: If given and in SUPPORTED_KINDS, forces the kind. If None
        or unknown, auto-detects.

    Returns:
      Dict with:
        * ``kind`` (str) — resolved kind.
        * ``fields`` (Dict[str, str]) — canonical field key -> value. Absent
          fields are simply not present. NB: this dict includes ``password``
          when the paste contained one — callers rendering this to the wire
          must strip it (see router.py).
        * ``missing`` (List[str]) — required fields for the kind that were
          not present in the paste.
        * ``extras`` (Dict[str, str]) — label lines whose label did not map
          to any canonical field for the chosen kind. Rendered read-only.
    """
    if hint_kind is not None and hint_kind not in SUPPORTED_KINDS:
        hint_kind = None
    kind = hint_kind or _score_kind(text)

    fields: Dict[str, str] = {}
    extras: Dict[str, str] = {}

    for raw_line in text.splitlines():
        m = _LINE_RE.match(raw_line)
        if not m:
            continue
        raw_label, raw_value = m.group(1), m.group(2)
        value = raw_value.strip()
        if value == "":
            continue
        canonical = _label_to_canonical(raw_label, kind)
        if canonical is None:
            # Preserve the last-seen extra for a given label (do not silently
            # overwrite a canonical field with an unmapped one).
            extras[raw_label.strip()] = value
            continue
        # First occurrence wins for canonical fields — paste shape from the
        # AISCA panel never repeats labels.
        fields.setdefault(canonical, value)

    required = REQUIRED_FIELDS.get(kind, ())
    missing = [f for f in required if f not in fields]

    return {
        "kind": kind,
        "fields": fields,
        "missing": missing,
        "extras": extras,
    }
