"""Secret-hygiene guard for the Hugging Face access token.

This module ships:
  * Owner rotation ruling banked verbatim (module constant, wave-gated).
  * Active-token identity pinned by SHA256 (not by value).
  * Env-var-only loader (`load_hf_token_or_raise`).
  * Transcript-leak guard (`assert_no_transcript_leak_of_active_token`).
  * SEC rotation ledger frozen for the two HF SEC items.

Discipline: this module NEVER prints the token value.  It NEVER writes
the token value to any log/receipt/error message.  The guard functions
raise plain exception classes whose messages contain only labels.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


# Owner secret-hygiene rule (2026-09-14, verbatim; banked in
# STATE/DECISIONS.md · owner-channel ruling entry dated 2026-09-14T~13:00Z).
HF_TOKEN_ROTATION_RULING_VERBATIM: str = (
    "env-var injection only — same for ALL secrets from now on: "
    "env/askpass, never printed, never on a command line visible to ps."
)


# Active artefact — the rotated replacement received 2026-09-14T12:23:58Z.
# Identity pinned by SHA256; the file path is FYI-only for callers that
# use env-var injection (the normal path).
HF_TOKEN_ACTIVE_ARTEFACT: str = (
    "/app/backend/estate_keys/data_sources/hf_token_rotated_20260914.csv"
)
HF_TOKEN_ACTIVE_SHA256: str = (
    "3ea89c945d58b62b71fbda1089773af2ab0f62ebe86b67c97b7f4172326b19c5"
)


# Pre-rotation artefact — retained on disk for forensic evidence of
# SEC-2026-09-12-01 and to let a hardened loader raise
# `HFTokenNotRotatedError` if a stale caller points at the old path.
# NOT used at runtime by any loader in this module.
HF_TOKEN_PRE_ROTATION_ARTEFACT: str = (
    "/app/backend/estate_keys/data_sources/hf_token.csv"
)


# SEC state ledger — frozen tuple of dicts.  Records the current state
# of each HF-token SEC item at wave close.  See
# `notes/HF_TOKEN_ROTATION_LEDGER_20260914.md` and
# `notes/SEC_INCIDENTS_20260914.md` for full narrative.
SEC_ROTATION_LEDGER: tuple = (
    {
        "sec_id": "SEC-2026-09-12-01",
        "state": "OWNER-ROTATED-PENDING-CONFIRMATION",
        "class": "hf_token transcript leak",
        "filed": "2026-09-12",
        "rotated_by_owner_at_utc": "2026-09-14T12:23:58Z",
        "confirmation_gate": (
            "owner reply banking that leaked value is de-authorised on HF side"
        ),
    },
    {
        "sec_id": "SEC-2026-09-14-04",
        "state": "PENDING-SECOND-ROTATION",
        "class": "hf_token transcript leak (of the rotated replacement itself)",
        "filed": "2026-09-14",
        "cause": "head -1 on custody-root artefact during registration",
        "rotation_required_post_close": True,
    },
)


class HFTokenNotRotatedError(Exception):
    """Raised by a hardened loader when a caller points at the pre-rotation
    HF-token artefact path (SEC-2026-09-12-01 pre-rotation state).

    Declared for the fabric contract; runtime wiring to a file-path-
    refusing loader is a follow-on wave (see grounding brief §E.2).
    """


class HFTokenEnvVarMissing(Exception):
    """Raised by `load_hf_token_or_raise` when neither `HF_TOKEN` nor
    `HUGGING_FACE_HUB_TOKEN` is set in the process environment.

    Fail-closed by design: the loader does NOT fall back to reading
    the on-disk artefact into a string that could then be printed
    (that fallback is what led to SEC-2026-09-14-04).  Callers that
    see this exception must arrange env-var injection before retrying.
    """


def load_hf_token_or_raise() -> str:
    """Return the HF token from env-var injection.

    Order of resolution: `HF_TOKEN`, then `HUGGING_FACE_HUB_TOKEN`.
    If both are unset (or empty), raise `HFTokenEnvVarMissing`.  This
    function does NOT read the on-disk artefact and MUST NOT be
    modified to fall back to a file read.
    """
    value = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if not value:
        raise HFTokenEnvVarMissing(
            "HF token not found in env: set HF_TOKEN or HUGGING_FACE_HUB_TOKEN"
        )
    return value


# Module-private cache for the active token value.  Populated on first
# call to `assert_no_transcript_leak_of_active_token` by reading the
# custody-root artefact ONCE.  Never surfaced through any accessor;
# the guard's only external effect is raising `RuntimeError` on match.
_ACTIVE_TOKEN_CACHE: Optional[str] = None


def _read_active_token_from_custody() -> Optional[str]:
    """Read the active-artefact file into memory ONCE.

    Returns the stripped value or ``None`` if the file is missing or
    unreadable.  Never prints.  The returned string is stored in the
    module cache and used only by the substring check in
    `assert_no_transcript_leak_of_active_token`.
    """
    path = Path(HF_TOKEN_ACTIVE_ARTEFACT)
    if not path.is_file():
        return None
    try:
        return path.read_text().strip()
    except OSError:
        return None


def assert_no_transcript_leak_of_active_token(text: str) -> None:
    """Refuse if `text` contains the active HF-token value.

    Callers invoke this before emitting any log/receipt/print/error
    that might contain user- or context-supplied strings.  Raises
    `RuntimeError` (base class, matching the invariant contract)
    with a message that does NOT include the token value.

    If the on-disk artefact is missing (custody file removed or not
    yet dropped), the guard passes-through — a caller trying to leak
    a value that isn't on disk here is out of this wave's scope.
    """
    global _ACTIVE_TOKEN_CACHE
    if _ACTIVE_TOKEN_CACHE is None:
        _ACTIVE_TOKEN_CACHE = _read_active_token_from_custody()
    active = _ACTIVE_TOKEN_CACHE
    if active and active in text:
        raise RuntimeError(
            "secret leak refused: active HF-token value appears in the "
            "supplied text (SEC-2026-09-14-04 guard)"
        )
