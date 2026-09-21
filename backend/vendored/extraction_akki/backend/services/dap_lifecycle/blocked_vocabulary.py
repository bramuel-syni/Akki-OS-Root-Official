"""R-87 · CP-BLOCKED-VOCABULARY-CORRECTION · load-bearing vocabulary registration.

Owner Ruling 2 verbatim (banked in STATE/DECISIONS.md OWNER RULINGS
anchor line 20421 · 2026-09-20T~19:00Z · re-affirmed at CP-APP-JS-UNIFY-
SCHEDULE-AND-DRIFT-ANNOTATE Commit-C `e40047f4`):

    "RULING 2 — FORK-BLK-KINDS: OPTION A RATIFIED, with a load-bearing vocabulary correction. Owner verbatim: suspension 'is a state of the principal (DAP-27, PRIN-1), not a fourth reason a request is blocked — a different axis, different object.' Sealed enum stays at three. party_halted lives as its own state via the Q5 module tree and its vocab constant, and it NEVER renders in the Blocked reason grammar — no estate copy, no kind label. Correct the wording at source everywhere non-sealed: it is 'three Blocked kinds plus Interrupted plus party_halted' — NOT 'five Blocked kinds.' Vocabulary is load-bearing for the substitution rules now — register the corrected count/grammar so the wrong phrasing is RED where feasible."

R-87 wave scope (SO §6.4 NOTHING-BEYOND): this module registers the
corrected vocabulary as Final[...] constants so downstream authors
(FE-FIX-READY spec consumer + backend surface authors + auditors) have
a single source of truth and the wrong phrasing is RED at the
vocabulary layer.

## What is registered

- `BLOCKED_KINDS_COUNT: Final[int] = 3` — canonical count. Never five.
- `BLOCKED_KINDS_TUPLE: Final[tuple[str, ...]] = ("request", "check",
  "estate")` — byte-verbatim match with the sealed `BlockedKind` enum.
- `SUSPENDED_IS_PRINCIPAL_STATE_NOT_BLOCKED_KIND: Final[bool] = True` ·
  DAP-27 + PRIN-1 axis-binding.
- `PARTY_HALTED_IS_OWN_RAIL_STATE_NOT_BLOCKED_KIND: Final[bool] = True` ·
  Q5 module tree axis-binding.
- `WRONG_COUNT_PHRASES: Final[tuple[str, ...]]` — canonical list of
  nonconformant phrasings the FE-FIX-READY spec + grep-negative sweeps
  consume.
- `grep_negative_wrong_count_phrases(text: str)` — pure-data-in scanner.

## What is NOT touched (additive-only per SO §3.8)

- Sealed `BlockedKind` enum at `services/dap_lifecycle/blocked_kinds.py`
  (3 members: request/check/estate) — read via identity import only.
- Sealed `services/dap_lifecycle/party_halted_kind.py` (R-85) — its
  SO §2.5 verbatim quotes of journey v2's "five kinds" phrasing inherit
  the Ruling-2 erratum citation banked in this-wave's Commit-B.
- Sealed `services/dap_lifecycle/party_halt_billing.py` (R-85) — same
  erratum treatment.
- Sealed `services/dap_lifecycle/suspension_notices.py` (Q5-sealed
  at CP-Q-UNLOCK-SUB-WAVE) — this IS the surface where suspended
  renders (principal-state axis · separate from Blocked reason grammar).

## Axis discipline (Ruling 2 verbatim)

    "three Blocked kinds plus Interrupted plus party_halted"

Read as an ordered composition:
- Three Blocked kinds — sealed `BlockedKind` enum · request/check/estate.
- Plus Interrupted — separate rail state (platform fault) · own axis.
- Plus party_halted — separate rail state (party stopped executing
  request) · own axis via Q5 module tree at
  `services/dap_lifecycle/party_halted_kind.py`.

Suspended is a fourth axis (principal-state, DAP-27/PRIN-1) surfaced
only via `services/dap_lifecycle/suspension_notices.py` — it is NOT a
Blocked reason and NEVER renders as a Blocked-kind label.

Canon anchors:
- Owner Ruling 2 verbatim (STATE/DECISIONS.md line 20421 anchor).
- Sealed `BlockedKind` at `services/dap_lifecycle/blocked_kinds.py`.
- Journey v1 §11 L201 "Blocked has three kinds, not one flat state:
  request, check, estate" (authoritative for the 3-kind grammar).
- DAP-27 principal-state + PRIN-1 principal-context binding.
- SO §2.5 verbatim-docstring · §3 tests-first · §3.3 3-Commit Seal ·
  §3.8 additive-only · §3.10-α Final[str] closed-vocab pattern.
- CP-APP-JS-UNIFY-SCHEDULE-AND-DRIFT-ANNOTATE seal `2eca0e58` /
  `1525ddd0` / `e40047f4` (R-86 immediately-precedes).
- CP-PARTY-HALTED-ADDITIVE-SUB-WAVE seal `11afc4f` / `0cd4c9b8` (R-85
  precedes · sealed party_halted surfaces inherit Ruling-2 erratum).
- CP-REGISTRY-V5-RATIFICATION-AND-COUNT-ERRATUM `1250c39a` (registry v5
  ratified · G5-v5 unblocked · Ruling-3-erratum-shape count-fix cites
  `0e7a07b0`).
"""

from __future__ import annotations

from typing import Final, List, Tuple


# ---------- Load-bearing count / grammar registration ----------

#: Ruling 2 count-binding · three Blocked kinds, never five.
BLOCKED_KINDS_COUNT: Final[int] = 3

#: Ruling 2 grammar-binding · byte-verbatim match with the sealed
#: BlockedKind enum member set. Any drift is a Canon 3 §24 4-step
#: rule-change ceremony territory, not a code edit.
BLOCKED_KINDS_TUPLE: Final[Tuple[str, ...]] = ("request", "check", "estate")


# ---------- Axis-binding Final[bool] flags ----------

#: Ruling 2 axis-binding · suspension "is a state of the principal
#: (DAP-27, PRIN-1), not a fourth reason a request is blocked — a
#: different axis, different object." NEVER renders in Blocked reason
#: grammar; surfaces only via services/dap_lifecycle/suspension_notices.py.
SUSPENDED_IS_PRINCIPAL_STATE_NOT_BLOCKED_KIND: Final[bool] = True

#: Ruling 2 axis-binding · "party_halted lives as its own state via the
#: Q5 module tree and its vocab constant, and it NEVER renders in the
#: Blocked reason grammar — no estate copy, no kind label."
PARTY_HALTED_IS_OWN_RAIL_STATE_NOT_BLOCKED_KIND: Final[bool] = True


# ---------- Corrected composition phrase ----------

#: Ruling 2 corrected-phrase · Final[str] closed-vocab per SO §3.10-α.
#: "three Blocked kinds plus Interrupted plus party_halted" — NEVER
#: "five Blocked kinds." Consumed verbatim by FE-FIX-READY spec.
CORRECTED_COMPOSITION_PHRASE: Final[str] = (
    "three Blocked kinds plus Interrupted plus party_halted"
)


# ---------- Wrong-phrase registration (grep-negative substrate) ----------

#: Ruling 2(b) verbatim: "register the corrected count/grammar so the
#: wrong phrasing is RED where feasible." Canonical nonconformant
#: phrasings that FE-FIX-READY spec + grep-negative sweeps consume.
#: Byte-verbatim tokens (case-sensitive as authored). Ordering is stable
#: per Final[tuple] discipline.
WRONG_COUNT_PHRASES: Final[Tuple[str, ...]] = (
    "five Blocked kinds",
    "5 Blocked kinds",
    "Blocked has five kinds",
    "five kinds of Blocked",
)


def grep_negative_wrong_count_phrases(text: str) -> List[Tuple[int, str]]:
    """Pure-data-in scanner returning a list of (line_no, matched_phrase)
    hits for a given text buffer.

    Callers (FE-FIX-READY spec consumers · non-sealed backend authors ·
    reviewers) pass a file body and receive the hit list · empty list =
    clean · non-empty list = nonconformant.

    Signature is intentionally pure-data-in: no filesystem access, no
    logging, no side effects. Line numbers are 1-based to match editor
    conventions.
    """
    hits: List[Tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for phrase in WRONG_COUNT_PHRASES:
            if phrase in line:
                hits.append((lineno, phrase))
    return hits
