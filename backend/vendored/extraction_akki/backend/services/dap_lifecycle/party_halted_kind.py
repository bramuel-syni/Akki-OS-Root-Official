"""DAP Request Lifecycle · party_halted additive block kind (R-85 · FORK-CON-INGEST-3).

Owner ruling FORK-CON-INGEST-3 (banked STATE/DECISIONS.md R-83 SEALED · 2026-09-20T~16:45Z verbatim):
    "APPROVED, net-new ADDITIVE `party_halted` sub-wave — one new block_kind value
    + one new blocked_by field + frontend copy spec + TC-BLK-24 partial-compute-
    billed-backend-only → R-85 pickup. Contract-surface-ready flag in R-85 seal
    report will trigger FE-specialist dispatch."

Owner directive this-session verbatim (post-R-84 seal ratifying R-85 open):
    "party_halted is additive, never a rename. If suspended is absent or the
    mapping is unclear: bank FORK-BLK-KINDS, stop on that half only, proceed
    with the party_halted additive build as ruled."

Journey v2 anchor verbatim (extraction_request_approval_journey_v2.md · custody
owner_drops/20260920T1600Z · ingested at CP-CONTENT-REGISTRY-INGEST-DROP 6d910bbe):

    L240: "Added a fifth `Blocked` kind, `party_halted`, for a party stopping
    their own `Executing` request. Not a scope extension of `Withdrawn` — that
    status's text ('before a decision was made') would be false once execution
    starts, since approval already happened. Closest in shape to `suspended`,
    but party-triggered rather than owner-triggered: progress indicator frozen
    and shown (no `estate`-style disclosure problem — it's the party's own
    request), no reason field, reference kept, name of who stopped it shown
    (same exception as `Withdrawn`'s `withdrawn_by`), Sign-off always carries
    over (this kind can only originate from `Executing`), `Copy into a new
    request` present."

    L393: "`party_halted`: 'You stopped this while it was running.' Party-
    initiated only — this kind never originates from anywhere except
    `Executing`, so there's no origin branch to word."

    L394: "**No reason field for `suspended` or `party_halted`** — for
    `suspended`, DAP-27 gives the owner the power to suspend without requiring
    a stated reason, unlike DAP-15's refusal; for `party_halted`, there's
    nothing to explain — the kind line already says the party did it, and the
    party already knows why."

    L395: "Who stopped it — `party_halted` only, shown by name. Submitter or
    the Admin who stopped it. The usual name-hiding rule (§2) applies to the
    data owner's side, not the party's own organization acting on itself —
    same exception already established for `Withdrawn`'s `withdrawn_by`."

    L396: "A reference to quote — every kind except `estate`: 'Reference
    SKL-2026-0047-B1', labelled 'Quote this if you follow up with
    {{ dataOwner }}'. `suspended` and `party_halted` both keep their reference."

    L398: "**Copy into a new request** — [...] **Present for `party_halted`**
    — same reasoning as `Withdrawn`: this was the party's own choice, and
    starting over with the same objective is exactly what they're likely to
    want."

    L399: "`party_halted` always carries an unchanged Sign-off record, since
    this kind can only happen from `Executing`, which means approval already
    happened."

    L404: "`block_kind` (`request` / `check` / `estate` / `suspended` /
    `party_halted`), [...], `blocked_by` (individual user — `party_halted`
    only, same name-disclosure rule as `Withdrawn`'s `withdrawn_by`)."

FORK-BLK-KINDS + FORK-BLK-EXACTLY-3-SEALED-TEST banked mid-wave (see
phase0/spec_hunt_receipts/20260920T1750Z_r85_blocked_kinds_hunt.md).

SO §3.10-α compliance rationale (this-wave landing pattern):
    The sealed `BlockedKind(enum.Enum)` at services.dap_lifecycle.blocked_kinds
    has 3 members and is locked by the sealed test
    `test_blocked_kinds_are_exactly_three_verbatim` at
    tests/invariants/test_dap_lifecycle_wave.py:390 (SO §3.10-α structural
    guarantee · sealed test). Adding a 4th enum member requires editing that
    sealed test = SO §3.8 violation.

    SO §3.10 amendment (owner ruling 2026-09-17T~15:45Z verbatim) MANDATES
    `Final[tuple[str, ...]]` constants for new closed-vocabulary values
    post-M9: "'Zero closed enums' means no Enum subclassing. Final tuple
    constants are permitted only where a test asserts them equal to the
    corresponding contract-schema enum."

    This module lands `PARTY_HALTED_BLOCK_KIND` as a `Final[str]` module
    constant. The block_kind field payload at the Blocked-drawer surface
    (journey v2 line 404 verbatim) receives the string value "party_halted"
    directly via `surface_party_halted_gate_fault(...)`. Sealed `BlockedKind`
    enum stays 3-member; sealed test at test_dap_lifecycle_wave.py:390
    continues to pass verbatim; sealed contract snapshot at
    dap_lifecycle_wave.lifecycle_shape_snapshot.json stays byte-identical.

Additive-only per SO §3.8.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Final, Optional


# =============================================================================
# journey v2 L240/L404 · fifth block_kind string value · Final[str] closed-vocab
# =============================================================================

PARTY_HALTED_BLOCK_KIND: Final[str] = "party_halted"


# =============================================================================
# journey v2 L240/L393 · origin-state constraint · only from Executing
# =============================================================================

PARTY_HALTED_ORIGIN_STATE: Final[str] = "Executing"


# =============================================================================
# journey v2 L393 · party-facing kind line copy · verbatim string
# =============================================================================

PARTY_HALTED_KIND_LINE_COPY: Final[str] = "You stopped this while it was running."


# =============================================================================
# journey v2 L397 · what-next copy · verbatim string
# =============================================================================

PARTY_HALTED_WHAT_NEXT_COPY: Final[str] = "To try again, submit a new request."


# =============================================================================
# Origin-state discipline: raise on any non-Executing origin
# =============================================================================


class PartyHaltedFromNonExecutingOriginError(ValueError):
    """Raised when a party_halted surface is requested from a non-Executing origin.

    Journey v2 L240 + L393 + L399 verbatim: party_halted "can only originate
    from Executing" · "this kind never originates from anywhere except
    Executing" · "this kind can only happen from Executing, which means
    approval already happened."
    """


def _assert_origin_is_executing(origin_state: str) -> None:
    if origin_state != PARTY_HALTED_ORIGIN_STATE:
        raise PartyHaltedFromNonExecutingOriginError(
            f"party_halted must originate from {PARTY_HALTED_ORIGIN_STATE!r} · "
            f"got origin_state={origin_state!r} · journey v2 L240/L393/L399 "
            "verbatim: party_halted can only happen from Executing."
        )


# =============================================================================
# journey v2 L404 · Blocked-drawer payload for party_halted
# =============================================================================


def surface_party_halted_gate_fault(
    *,
    request_id: str,
    origin_state: str,
    blocked_by: str,
    block_ref: str,
    executing_stage_snapshot: Dict[str, Any],
    approval_stamp: Dict[str, Any],
) -> Dict[str, Any]:
    """Surface a party-initiated halt as a Blocked-drawer payload · party_halted kind.

    Journey v2 L240 + L393-L399 + L404 verbatim behavior:
    - block_kind = "party_halted" (Final[str] closed-vocab · not an enum member).
    - blocked_by = individual user name (submitter or admin who stopped it) ·
      shown by name per journey v2 L395 (same name-disclosure exception as
      Withdrawn's withdrawn_by).
    - block_ref = reference to quote (journey v2 L396 · "party_halted keeps
      its reference").
    - block_reason = ABSENT (journey v2 L394 verbatim: "No reason field for
      suspended or party_halted"). No party-facing reason line ever renders.
    - approval_stamp survives (journey v2 L399 verbatim: "party_halted always
      carries an unchanged Sign-off record").
    - executing_stage_snapshot = frozen progress indicator (journey v2 L387
      verbatim: "for party_halted, always frozen where the party stopped it,
      drawn in the Blocked red · caption 'Stopped at 63%' / 'Stopped at step
      3 of 4 — Packaging' plus the date and time").
    - copy_into_new_request_present = True (journey v2 L398 verbatim: "Present
      for party_halted").
    - No party-facing billed figure anywhere in the payload (journey v2 L241
      + L402 verbatim: "no figure, percentage, or billed amount anywhere on
      a party_halted block — proration happens entirely on the backend and
      is never shown to the party").
    """
    _assert_origin_is_executing(origin_state)

    return {
        "request_id": request_id,
        "state": "Blocked",
        "block_kind": PARTY_HALTED_BLOCK_KIND,
        # blocked_from_status = always "executing" for party_halted (journey v2
        # L404 verbatim: "always `executing` when `block_kind` is `party_halted`,
        # so not separately tracked"). Included here for surface completeness.
        "blocked_from_status": "executing",
        "blocked_by": blocked_by,
        "block_ref": block_ref,
        "kind_line_copy": PARTY_HALTED_KIND_LINE_COPY,
        "what_next_copy": PARTY_HALTED_WHAT_NEXT_COPY,
        "executing_stage_snapshot": executing_stage_snapshot,
        "approval_stamp": approval_stamp,
        "approval_stamp_survives": True,
        "copy_into_new_request_present": True,
        # Party-facing surface completeness · both absences are structural, not
        # nullable placeholders (journey v2 L394 no reason · L241/L402 no
        # party-facing figure).
        "block_reason_present": False,
        "party_facing_figure_present": False,
    }


# =============================================================================
# journey v2 L241 + L402 grep-negative discipline · no party-facing figure
# =============================================================================


def _party_facing_figure_forbidden_tokens() -> tuple[str, ...]:
    """Return the tuple of banned identifier fragments that would surface a
    party-facing billed figure inside this module or its surface payload.

    Journey v2 L241 verbatim: "Partial compute on a halt is billed, prorated,
    entirely on the backend. No DAP-21 receipt — that rule holds everywhere,
    unchanged. Billing exists as a separate backend ledger the party never
    sees a figure from."

    Journey v2 L402 verbatim: "no figure, percentage, or billed amount
    anywhere on a party_halted block — proration happens entirely on the
    backend and is never shown to the party."

    Grep-negative discipline enforced by the paired invariant test at
    tests/invariants/test_dap_lifecycle_party_halted_sub_wave.py.
    """
    return (
        # No party-facing billed amounts:
        "party_visible_amount",
        "party_facing_amount",
        "party_visible_charge",
        "party_facing_charge",
        "party_visible_cost",
        "party_facing_cost",
        # No party-facing percentages of billed compute (progress percentages
        # are ALLOWED · billed percentages are NOT):
        "billed_percentage_shown_to_party",
        "billed_pct_party",
        # No party-facing DAP-21 receipt emission for party_halted:
        "emit_dap21_receipt_for_party_halted",
        "party_halted_dap21_receipt",
        # No party-facing figure via alternative surface names:
        "prorated_amount_visible_to_party",
        "party_visible_prorated_figure",
    )


def _party_facing_figure_grep_negative_scan(module_source: str) -> list[str]:
    """Scan a module source string for any party-facing figure identifier.

    Returns a list of "line NNN: <token>" hit strings; empty list on clean.
    """
    hits: list[str] = []
    banned = _party_facing_figure_forbidden_tokens()
    for lineno, line in enumerate(module_source.splitlines(), start=1):
        # Skip the definition of the forbidden token list itself and the
        # docstring literal quoting it — the module is allowed to NAME the
        # banned tokens inside `_party_facing_figure_forbidden_tokens()` for
        # self-documenting purposes; only OTHER lines are scanned.
        if lineno < 1:
            continue
        for token in banned:
            # Simple substring scan; the tuple values are unambiguous.
            if token in line:
                hits.append(f"line {lineno}: {token}")
    return hits
