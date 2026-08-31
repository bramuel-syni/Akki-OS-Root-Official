"""Masking function for the ussd_question_response training extract.

Authority: owner ruling 6 · 2026-08-31 (verbatim in DECISIONS.md).
    "MASKING DISCIPLINE (owner-bypass covers the missing pipeline BUILD, not
    the PII rules): identifiers stripped (phone numbers, farmer IDs, names,
    session IDs), all PII-classified columns excluded (occupation boolean
    stays out per its ruling), response-sanitizer banned fields
    (`farmer_mobile_no`, `farmer_answer`) excluded, plus a regex scrub pass
    over free text for phone-number/ID patterns before anything leaves the
    seam. Unclassified columns: cautious-default — exclude unless clearly
    non-PII structural/text content. Log the exact include/exclude decision
    per column in the data statement."

The `ussd_question_response` table has 13 columns.  This module records the
column include/exclude decision as a static, per-column DECISION_LEDGER (so
the decision is auditable + testable), and provides a `mask_row_free_text`
function that regex-scrubs Kenyan phone-number patterns + 7–10-digit
ID-shaped numerals from free text.

Discipline:
  - No PII in this module's output (rows post-mask carry only text tokens
    with phone/ID patterns replaced by [PHONE]/[ID]).
  - Cautious default: unclassified column = EXCLUDED (per owner ruling 6).
  - Every excluded column carries a `reason` field for the data statement.
"""
from __future__ import annotations

import re
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
# Per-column decision ledger for ussd_question_response
# (schema is stable per Census #1 · 2026-08-31)
# ---------------------------------------------------------------------------

DECISION_LEDGER: Dict[str, Tuple[str, str]] = {
    # column_name: (decision, reason_verbatim)
    "id":                ("EXCLUDE", "row primary key identifier — quasi-identifier, cautious-default"),
    "ussd_user_id":      ("EXCLUDE", "identifier linking to ussd_users PII table — strip"),
    "mobile_number":     ("EXCLUDE", "direct PII (Kenyan phone number) — strip"),
    "training_code":     ("EXCLUDE", "code identifier — cautious-default"),
    "post_id":           ("EXCLUDE", "identifier — cautious-default"),
    "question_id":       ("EXCLUDE", "identifier — cautious-default"),
    "option_id":         ("EXCLUDE", "identifier — cautious-default"),
    "option_string":     ("INCLUDE", "response text — training material; free-text regex-scrubbed"),
    "created_at":        ("EXCLUDE", "metadata timestamp — not training-relevant, cautious-default"),
    "question_string":   ("INCLUDE", "prompt text — training material; free-text regex-scrubbed"),
    "value_chain":       ("INCLUDE", "structural category (e.g. 'dairy', 'poultry') — non-PII"),
    "number_of_animals": ("EXCLUDE", "quasi-identifier revealing farm scale — cautious-default"),
    "forage_area":       ("EXCLUDE", "quasi-identifier revealing farm scale — cautious-default"),
}


INCLUDED_COLUMNS: List[str] = [c for c, (d, _) in DECISION_LEDGER.items() if d == "INCLUDE"]
EXCLUDED_COLUMNS: List[str] = [c for c, (d, _) in DECISION_LEDGER.items() if d == "EXCLUDE"]


# ---------------------------------------------------------------------------
# Free-text scrub patterns
# ---------------------------------------------------------------------------

# Kenyan phone-number patterns (all common variants).
# Numbers are 10 digits total starting with 07XX or 01XX, or 12 digits
# starting with +254 7XX / +254 1XX. Separators (space, dash) may appear
# between any two adjacent digits after the prefix.
#
# Approach: match a 2-digit anchor prefix (07/01 or 254 7/1) then require
# 8 more digits with optional single separators between them.
_PHONE_PATTERNS = [
    # +254 or 254 + (7|1) + 8 more digits with optional separators anywhere.
    re.compile(r"\+?254[\s\-]*[17](?:[\s\-]*\d){8,9}"),
    # 07XX or 01XX prefix (10 total digits) with optional separators.
    re.compile(r"(?<!\d)0[\s\-]*[17](?:[\s\-]*\d){8,9}"),
]

# Kenyan national-ID and misc identifiers: bare 7–10 digit numerics
# NOT adjacent to letters/dashes-as-model (avoids matching "H200", dates).
# Use a lookaround pattern.
_ID_PATTERN = re.compile(r"(?<![\d\w])\d{7,10}(?![\d\w])")


def mask_free_text(s: str) -> str:
    """Scrub Kenyan phone-number patterns and 7–10 digit ID-shaped numerics
    from ``s``. Returns the scrubbed string. Order matters (phone first,
    otherwise the ID regex swallows partial matches).
    """
    if s is None:
        return ""
    if not isinstance(s, str):
        s = str(s)
    out = s
    for p in _PHONE_PATTERNS:
        out = p.sub("[PHONE]", out)
    out = _ID_PATTERN.sub("[ID]", out)
    return out


def mask_row(row: Dict[str, object]) -> Dict[str, str]:
    """Apply the DECISION_LEDGER to a single raw row.
    - Rejects rows containing keys not in DECISION_LEDGER (raises).
    - Returns a new dict with ONLY the included columns; each value is
      regex-scrubbed via mask_free_text().
    """
    unknown = set(row.keys()) - set(DECISION_LEDGER.keys())
    if unknown:
        raise ValueError(
            f"cautious-default refuses unclassified columns: {sorted(unknown)}"
        )
    masked = {}
    for col in INCLUDED_COLUMNS:
        v = row.get(col)
        masked[col] = mask_free_text("" if v is None else str(v))
    return masked


def build_training_text(masked: Dict[str, str]) -> str:
    """Compose one training example text from a masked row.
    Format:
      "Category: <value_chain>\nQuestion: <question_string>\nAnswer: <option_string>"
    Kept simple + explicit so the corpus shape is inspectable at eyeball.
    """
    q = (masked.get("question_string") or "").strip()
    a = (masked.get("option_string") or "").strip()
    c = (masked.get("value_chain") or "").strip()
    if not q or not a:
        return ""
    parts = []
    if c:
        parts.append(f"Category: {c}")
    parts.append(f"Question: {q}")
    parts.append(f"Answer: {a}")
    return "\n".join(parts)
