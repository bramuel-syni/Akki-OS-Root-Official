"""Read-Only SQL Guard — CP1 kernel.

Owner CP1 refinement this session (verbatim):
    "The executor may only emit SELECT/SHOW/USE/DESCRIBE; any
     INSERT/UPDATE/DELETE/CREATE/DROP/ALTER/GRANT/TRUNCATE is refused
     by construction (RED if a write verb reaches the wire). This is a
     core safety invariant and MUST be green before any live touch."

Canon binding · Mtafiti-Spec §1:
    "It [Mtafiti] discovers and measures; it does not extract, target,
    or govern."

Contract:
  `refuse_if_write(sql: str) -> str`  →  normalised SQL if admitted,
  or raises `WriteVerbRefused` if the statement is not exclusively
  read-only.

Refuse-by-construction. The guard is a single-statement guard; multi-
statement submissions (semicolon-injection) are refused even if the
lead statement is read-only.
"""
from __future__ import annotations

import re


class WriteVerbRefused(Exception):
    """Raised when a SQL string is not exclusively read-only.

    Caused by:
      - A lead verb outside the read-only allow-list.
      - A multi-statement submission (any semicolon in the sanitised
        body other than a single trailing one).
      - Empty / whitespace-only / comment-only input.
    """


_ALLOWED_LEAD = frozenset({"SELECT", "SHOW", "USE", "DESCRIBE", "DESC", "EXPLAIN"})

# SQL comment stripping (line comments and block comments).
_COMMENT_RX = re.compile(r"(--[^\n]*|/\*.*?\*/)", re.DOTALL)


def _strip_comments(sql: str) -> str:
    return _COMMENT_RX.sub(" ", sql)


def refuse_if_write(sql: str) -> str:
    """Refuse-by-construction: raise WriteVerbRefused unless `sql` is
    exclusively read-only. Otherwise return the normalised statement.
    """
    if not isinstance(sql, str):
        raise WriteVerbRefused(
            f"sql must be a string; got {type(sql).__name__!r}"
        )

    cleaned = _strip_comments(sql).strip()
    if not cleaned:
        raise WriteVerbRefused(
            "SQL is empty / whitespace / comment-only after sanitisation."
        )

    # Allow exactly one trailing semicolon; reject anything else.
    core = cleaned.rstrip().rstrip(";").rstrip()
    if not core:
        raise WriteVerbRefused(
            "SQL has no statement body after removing trailing semicolons."
        )
    if ";" in core:
        raise WriteVerbRefused(
            "multi-statement submission refused; single statement only."
        )

    lead_token = core.split(None, 1)[0].upper()
    if lead_token not in _ALLOWED_LEAD:
        raise WriteVerbRefused(
            f"lead verb {lead_token!r} is not read-only; "
            f"allowed = {sorted(_ALLOWED_LEAD)!r}"
        )

    return core
