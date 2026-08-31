"""RED-then-GREEN tests for the ussd_question_response masking module.

Contract enforced (per owner ruling 6 · 2026-08-31 · verbatim in DECISIONS.md):
  - Kenyan phone-number patterns scrubbed to [PHONE].
  - 7-10 digit ID-shaped numerals scrubbed to [ID].
  - Unclassified columns → cautious-default REFUSAL (raises).
  - Only INCLUDED columns pass through mask_row.
  - Data-statement column decisions are auditable + stable.
"""
import pytest

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mask import (
    DECISION_LEDGER,
    INCLUDED_COLUMNS,
    EXCLUDED_COLUMNS,
    mask_free_text,
    mask_row,
    build_training_text,
)


# --- DECISION_LEDGER covers all 13 columns of ussd_question_response ---

def test_decision_ledger_covers_all_13_columns_of_ussd_question_response():
    # Verbatim column set from Census #1 (2026-08-31, digicow_live)
    expected = {
        "id", "ussd_user_id", "mobile_number", "training_code", "post_id",
        "question_id", "option_id", "option_string", "created_at",
        "question_string", "value_chain", "number_of_animals", "forage_area",
    }
    assert set(DECISION_LEDGER.keys()) == expected


def test_only_three_columns_included():
    # question_string, option_string, value_chain
    assert set(INCLUDED_COLUMNS) == {"question_string", "option_string", "value_chain"}


def test_pii_columns_are_excluded():
    # Every column with "id", "mobile", "code", quasi-identifiers → EXCLUDE
    for col in ("mobile_number", "ussd_user_id", "post_id", "question_id",
                "option_id", "id", "training_code", "number_of_animals",
                "forage_area", "created_at"):
        assert DECISION_LEDGER[col][0] == "EXCLUDE"


def test_every_decision_has_a_reason():
    for col, (decision, reason) in DECISION_LEDGER.items():
        assert decision in ("INCLUDE", "EXCLUDE")
        assert isinstance(reason, str) and len(reason) > 5


# --- Phone-number scrubbing (Kenyan patterns) ---

@pytest.mark.parametrize("s", [
    "call me 0712345678 please",
    "reach at +254712345678 asap",
    "phone: 254712345678",
    "07 12 345 678",
    "+254 712 345 678",
    "+254-712-345-678",
    "0102345678",
    "+254102345678",
    "2547 12 345 678",
])
def test_phone_numbers_get_scrubbed(s):
    out = mask_free_text(s)
    assert "[PHONE]" in out
    # Verify no phone-digit-shaped substring remains
    for target in ["712345678", "102345678"]:
        assert target not in out, f"digits leaked: {out!r}"


# --- ID-shaped numeric scrubbing ---

def test_id_shaped_numerics_get_scrubbed():
    # 7–10 digit standalone numerics
    for s in ("id 12345678 here", "reference 1234567890", "farmer 9876543"):
        out = mask_free_text(s)
        assert "[ID]" in out


def test_short_numerics_are_not_scrubbed():
    # Fewer than 7 digits should pass through untouched (e.g. counts,
    # small numbers). Cautious-default is on COLUMN admission; free-text
    # numerics below 7 digits are training signal (e.g. "3 cows").
    assert mask_free_text("I have 3 cows") == "I have 3 cows"
    assert mask_free_text("$1.5 per litre") == "$1.5 per litre"
    assert mask_free_text("100 kg") == "100 kg"


def test_alphanumeric_codes_not_falsely_scrubbed():
    # Model designators / farm codes with letters shouldn't be regarded
    # as phone/ID numerics.
    assert "[PHONE]" not in mask_free_text("F123456789")
    assert "[ID]" not in mask_free_text("F1234567")


# --- Row-level masking ---

def _sample_raw_row():
    return {
        "id": 42,
        "ussd_user_id": 100,
        "mobile_number": "+254712345678",
        "training_code": "T-001",
        "post_id": 5,
        "question_id": 7,
        "option_id": 3,
        "option_string": "milk twice daily, call 0712345678 for support",
        "created_at": "2025-01-15 10:30:00",
        "question_string": "How often should I milk my cow?",
        "value_chain": "dairy",
        "number_of_animals": "3",
        "forage_area": "0.5",
    }


def test_mask_row_returns_only_included_columns():
    masked = mask_row(_sample_raw_row())
    assert set(masked.keys()) == set(INCLUDED_COLUMNS)


def test_mask_row_scrubs_free_text():
    masked = mask_row(_sample_raw_row())
    # option_string had a phone number embedded
    assert "0712345678" not in masked["option_string"]
    assert "[PHONE]" in masked["option_string"]


def test_mask_row_never_returns_pii_columns():
    masked = mask_row(_sample_raw_row())
    for banned in ("mobile_number", "ussd_user_id", "id", "created_at"):
        assert banned not in masked


def test_mask_row_refuses_unclassified_columns():
    row = _sample_raw_row()
    row["unclassified_new_column"] = "surprise"
    with pytest.raises(ValueError, match="cautious-default"):
        mask_row(row)


# --- Training text composition ---

def test_build_training_text_shape():
    masked = mask_row(_sample_raw_row())
    txt = build_training_text(masked)
    assert txt.startswith("Category: dairy")
    assert "Question: How often should I milk my cow?" in txt
    assert "[PHONE]" in txt or "Answer:" in txt


def test_build_training_text_skips_when_empty_qa():
    assert build_training_text({"question_string": "", "option_string": "x"}) == ""
    assert build_training_text({"question_string": "x", "option_string": ""}) == ""


# --- Regression: masking never re-introduces raw digits ---

def test_masking_output_carries_no_full_phone_digits():
    # After masking, no 10-digit Kenyan-shaped run should survive.
    import re
    s = "customer 0712345678 called from +254712345678 about farmer 12345678"
    out = mask_free_text(s)
    for pat in [r"0712345678", r"254712345678", r"12345678"]:
        assert re.search(pat, out) is None, f"pattern {pat!r} leaked: {out!r}"
