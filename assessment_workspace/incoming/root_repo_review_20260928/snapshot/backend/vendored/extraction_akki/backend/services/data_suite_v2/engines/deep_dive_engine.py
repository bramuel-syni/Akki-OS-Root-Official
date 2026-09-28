"""W-DEEP-DIVE-REAL · CP-DDDR1 · Real deep-dive engine.

Replaces the CP-D8 HALT-skeleton with a real case-agnostic mechanism that
produces the CP-D4 `AnalyzeDeepDive` shape from typed workspace inputs.
Pure function — no LLM, no HTTP, no storage.

Contract:

    run(*, session_id: str, source_refs: Sequence[str],
        prior_notes: Sequence[str] = ()) -> AnalyzeDeepDive

The `synthesis_sha256_hex` carried in the returned `AnalyzeDeepDive` is
computed deterministically from a canonical UTF-8 serialization of the
workspace shape.  Canon-4 §22 + Pull Seam P1: the synthesis body itself is
NEVER materialised in this mechanism — the carrier is a hash-only
derivative-shape.

Refusals (same shape as CP-DASWR1):
- `session_id` empty or non-string             → `WorkspaceInvalidError`
- `source_refs` empty                          → `WorkspaceEmptyError`
- any element of `source_refs` non-string      → `WorkspaceInvalidError`
- any element of `prior_notes` non-string      → `WorkspaceInvalidError`

Canonical serialization (bytes hashed for `synthesis_sha256_hex`):

    b"session_id=" + session_id.encode('utf-8') + b"\\n"
    + b"source_refs=" + b"\\x1f".join(r.encode('utf-8') for r in sorted(source_refs)) + b"\\n"
    + b"prior_notes=" + b"\\x1f".join(n.encode('utf-8') for n in prior_notes) + b"\\n"

`source_refs` are sorted (order-invariant contract — the workspace is a
set of units per Canon-4 §22, not a sequence).  `prior_notes` preserve
caller order (notes are time-ordered evidence carriers).  `\\x1f` (ASCII
UNIT SEPARATOR) is used as an intra-field delimiter so no legal UTF-8
character in a ref/note can collide with the separator.
"""
from __future__ import annotations

import hashlib
from typing import Sequence

from services.data_suite_v2.analyze_tabs import AnalyzeDeepDive
from services.data_suite_v2.engines import (
    WorkspaceEmptyError,
    WorkspaceInvalidError,
)


_UNIT_SEP = b"\x1f"


def _validate_session_id(session_id: str) -> None:
    if not isinstance(session_id, str) or not session_id:
        raise WorkspaceInvalidError(
            f"workspace shape: session_id must be a non-empty string; "
            f"got {session_id!r}"
        )


def _validate_source_refs(source_refs: Sequence[str]) -> tuple:
    if not source_refs:
        raise WorkspaceEmptyError(
            "workspace shape: source_refs must be non-empty; got 0 refs"
        )
    coerced = tuple(source_refs)
    for i, ref in enumerate(coerced):
        if not isinstance(ref, str):
            raise WorkspaceInvalidError(
                f"workspace shape: source_refs[{i}] must be a string; "
                f"got {type(ref).__name__}"
            )
    return coerced


def _validate_prior_notes(prior_notes: Sequence[str]) -> tuple:
    coerced = tuple(prior_notes)
    for i, note in enumerate(coerced):
        if not isinstance(note, str):
            raise WorkspaceInvalidError(
                f"workspace shape: prior_notes[{i}] must be a string; "
                f"got {type(note).__name__}"
            )
    return coerced


def _canonical_bytes(
    session_id: str,
    source_refs: tuple,
    prior_notes: tuple,
) -> bytes:
    """Canonical UTF-8 serialization of the workspace shape for hashing.

    Order-invariant on `source_refs` (sorted).  Order-preserving on
    `prior_notes` (caller-ordered).  ASCII UNIT SEPARATOR (0x1f) as intra-
    field delimiter.  No legal UTF-8 character in a ref or note can collide
    with the separator.
    """
    parts = [
        b"session_id=" + session_id.encode("utf-8") + b"\n",
        b"source_refs="
        + _UNIT_SEP.join(r.encode("utf-8") for r in sorted(source_refs))
        + b"\n",
        b"prior_notes="
        + _UNIT_SEP.join(n.encode("utf-8") for n in prior_notes)
        + b"\n",
    ]
    return b"".join(parts)


def run(
    *,
    session_id: str,
    source_refs: Sequence[str],
    prior_notes: Sequence[str] = (),
) -> AnalyzeDeepDive:
    """Compose an `AnalyzeDeepDive` hash-only carrier from a workspace.

    Pure function of typed inputs.  No LLM/HTTP/storage side-effects.  Case-
    agnostic — no executive-domain tokens in the module or in the returned
    shape.  See module docstring for refusals and discharge anchors.
    """
    _validate_session_id(session_id)
    refs = _validate_source_refs(source_refs)
    notes = _validate_prior_notes(prior_notes)

    body = _canonical_bytes(session_id, refs, notes)
    synthesis_sha256_hex = hashlib.sha256(body).hexdigest()

    return AnalyzeDeepDive(
        session_id=session_id,
        tab_kind="deep_dive",
        synthesis_sha256_hex=synthesis_sha256_hex,
    )
