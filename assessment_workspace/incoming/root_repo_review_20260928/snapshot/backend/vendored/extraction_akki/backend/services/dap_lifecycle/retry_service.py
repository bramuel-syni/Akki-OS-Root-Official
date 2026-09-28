"""DAP Request Lifecycle · Q1 Retry service.

Owner ruling verbatim (STATE/DECISIONS.md R-78 · 2026-09-20T~13:00Z):
    "Q1 retry-for-check-only, reusing the surviving approval — approve.
    Conditions: the frozen objective is hash-identical, the same units,
    the approval unexpired; the retry re-runs every gate from the failed
    stage forward, not the failed check alone; the request keeps its id
    with an attempt counter; each attempt is receipted; attempts are
    bounded (DEFAULT 3) — an unbounded retry is a probe."

Additive-only per SO §3.8.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple


RETRY_MAX_ATTEMPTS_DEFAULT: int = 3


class RetryRefused(Exception):
    """Retry did not meet the owner-ratified conditions."""


def attempt_retry(
    *,
    request_id: str,
    current_block_kind: str,
    original_approval_id: str,
    original_approval_unexpired: bool,
    submitted_objective_hash: str,
    stored_objective_hash: str,
    submitted_units: Tuple[str, ...],
    stored_units: Tuple[str, ...],
    current_attempt: int,
    failed_stage: Optional[str] = None,
) -> Dict[str, Any]:
    """Attempt a retry per owner R-78 conditions.

    Refuses if:
        - The current block is not `check` kind (retry-for-check-only).
        - The submitted objective hash differs from the stored one.
        - The units differ.
        - The approval has expired.
        - current_attempt >= RETRY_MAX_ATTEMPTS_DEFAULT (bounded 3).

    Returns the retry-admitted outcome otherwise.
    """
    # Owner verbatim: retry-for-check-only. Block-kind must be `check`.
    if current_block_kind != "check":
        raise RetryRefused(
            f"DAP-LIFECYCLE-Q1 · retry-for-check-only · request {request_id} "
            f"blocked kind is {current_block_kind!r} · not_check_kind · fail-closed"
        )
    if submitted_objective_hash != stored_objective_hash:
        raise RetryRefused(
            f"DAP-LIFECYCLE-Q1 · request {request_id} · objective_hash_mismatch "
            f"submitted={submitted_objective_hash!r} stored={stored_objective_hash!r} · fail-closed"
        )
    if tuple(submitted_units) != tuple(stored_units):
        raise RetryRefused(
            f"DAP-LIFECYCLE-Q1 · request {request_id} · units_mismatch "
            f"submitted={submitted_units!r} stored={stored_units!r} · fail-closed"
        )
    if not original_approval_unexpired:
        raise RetryRefused(
            f"DAP-LIFECYCLE-Q1 · request {request_id} · approval_expired "
            f"(approval_id={original_approval_id!r}) · fail-closed"
        )
    if current_attempt >= RETRY_MAX_ATTEMPTS_DEFAULT:
        raise RetryRefused(
            f"DAP-LIFECYCLE-Q1 · request {request_id} · bounded max_attempts "
            f"{RETRY_MAX_ATTEMPTS_DEFAULT} reached (attempt={current_attempt}) · "
            "unbounded retry is a probe · fail-closed"
        )

    return {
        "request_id": request_id,   # id preserved · owner verbatim "keeps its id"
        "next_attempt_number": current_attempt + 1,
        "receipted": True,
        "reuses_original_approval": True,
        "original_approval_id": original_approval_id,
        # Owner verbatim: "the retry re-runs every gate from the failed stage forward,
        # not the failed check alone".
        "reruns_gates_from_stage": failed_stage,
        "reruns_only_the_failed_check_alone": False,
    }
