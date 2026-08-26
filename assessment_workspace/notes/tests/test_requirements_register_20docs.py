"""W11 CP7 · register expansion 17-doc → 20-doc invariants.

Owner Ruling 2026-08-19 §6 · additive-only correction discipline:
the 17-doc register is preserved verbatim; Docs 17, 18, 19 are appended
as a new file `notes/requirements_register_20docs.md` layered on top.
This test file lives at:
  workspace-root/notes/tests/  (docs-level, not backend/tests)

The invariant is a docs-shape assertion, executable by `python3 -m pytest`
against the workspace notes dir, so it counts alongside the CP2/CP3 cohort
without needing an import of any backend module.

Expected shape (from W11 reassessment §2):
  * Doc17-001..017    · 17 rows (11 CANON + 6 OPEN)
  * Doc18-001..008    · 8 rows (6 CANON + 1 PROPOSED + 1 OPEN)
  * Doc19A-001..006   · 6 rows (Critic Seam QA-1..QA-6 · all CANON)
  * Doc19B-001..005   · 5 rows (EP-1..EP-5 · 4 PROPOSED + 1 OPEN)
  * Grand total: 36 new rows.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest


REGISTER_20DOCS = Path(__file__).resolve().parents[2] / \
    "notes" / "requirements_register_20docs.md"


def _read_register() -> str:
    assert REGISTER_20DOCS.exists(), (
        f"CP7 register file missing at {REGISTER_20DOCS}"
    )
    return REGISTER_20DOCS.read_text(encoding="utf-8")


def _extract_row_ids(text: str, prefix: str) -> set:
    """Return the set of unique row IDs matching '**{prefix}-###**' in bold."""
    pat = re.compile(rf"\*\*({re.escape(prefix)}-\d+[a-z]?)\*\*")
    return set(pat.findall(text))


def test_register_file_exists():
    """CP7 file lands additively at notes/requirements_register_20docs.md."""
    assert REGISTER_20DOCS.exists()


def test_doc17_rows_count_17():
    """Doc 17 · Multidimensional Training Engine · 17 rows."""
    rows = _extract_row_ids(_read_register(), "Doc17")
    assert len(rows) == 17, (
        f"Doc17 row count drift · expected 17 · got {len(rows)}: {sorted(rows)}"
    )


def test_doc18_rows_count_8():
    """Doc 18 · Callable Skill Files · 8 rows."""
    rows = _extract_row_ids(_read_register(), "Doc18")
    assert len(rows) == 8, (
        f"Doc18 row count drift · expected 8 · got {len(rows)}: {sorted(rows)}"
    )


def test_doc19a_rows_count_6():
    """Doc 19 Part A · Critic Seam QA-1..QA-6 · 6 rows."""
    rows = _extract_row_ids(_read_register(), "Doc19A")
    assert len(rows) == 6, (
        f"Doc19A row count drift · expected 6 · got {len(rows)}: {sorted(rows)}"
    )


def test_doc19b_rows_count_5():
    """Doc 19 Part B · Evidence Protocol EP-1..EP-5 · 5 rows."""
    rows = _extract_row_ids(_read_register(), "Doc19B")
    assert len(rows) == 5, (
        f"Doc19B row count drift · expected 5 · got {len(rows)}: {sorted(rows)}"
    )


def test_total_new_rows_36():
    """Total across Docs 17 + 18 + 19A + 19B is 36 new rows."""
    text = _read_register()
    total = (
        len(_extract_row_ids(text, "Doc17"))
        + len(_extract_row_ids(text, "Doc18"))
        + len(_extract_row_ids(text, "Doc19A"))
        + len(_extract_row_ids(text, "Doc19B"))
    )
    assert total == 36, f"CP7 total row drift · expected 36 · got {total}"


def test_register_denominator_551():
    """Register grows from 515 → 551 (§7 of w11_reassessment)."""
    text = _read_register()
    assert "515" in text, "prior denominator (515) must be cited in the delta table"
    assert "551" in text, "new denominator (551) must be named in the CP7 landing"


def test_additive_only_preservation_statement():
    """Owner Ruling 2026-08-19 §6 · additive-only correction discipline."""
    text = _read_register().lower()
    assert "additive" in text, (
        "CP7 landing must cite the additive-only correction discipline"
    )


def test_owner_ruling_status_per_doc_present():
    """Each new doc carries a status classification per row."""
    text = _read_register()
    for status in ("CANON", "PROPOSED", "OPEN"):
        assert status in text, (
            f"status class {status!r} missing from register"
        )


def test_carrying_phase_pointers_present():
    """R4 registry rows land only with their carrying phases — the register
    names them (CP2, CP3, CP4, CP5, CP8) so the register-to-code seam is
    auditable."""
    text = _read_register()
    for cp in ("CP2", "CP3"):
        assert cp in text, f"carrying-phase pointer {cp!r} missing"


def test_donor_lift_source_named_for_doc19a():
    """Doc 19A CritIc Seam is a verbatim LIFT from Akki-OS-V1; the register
    must cite the donor path so downstream audit can trace the LIFT."""
    text = _read_register()
    assert "Akki-OS-V1" in text and "critic_pass" in text, (
        "Doc 19A must cite the Akki-OS-V1/critic_pass donor path"
    )


def test_digicow_freshness_note_present():
    """The register cites the DigiCow test-set seal succeeding on the fresh
    2026-08-26 verification (interleave commit 3e99be2)."""
    text = _read_register()
    assert "digicow" in text.lower(), "DigiCow anchor must be cited"
    assert "2026-08-26" in text, (
        "the successful-seal date (fresh verification) must be named"
    )
