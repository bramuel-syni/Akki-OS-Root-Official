"""services.ledger_verifier.sev1_wire — M10-W3 · orchestrator that wires
a `VerifierReceipt` with `break_at_seq is not None` to BOTH:
  (a) `raise_sev1_page()` on the SEV-1 security-group paging endpoint;
  (b) `record_chain_break_signal()` on the Watch chain-break evidence
      store.

Owner Run Order 2026-09-18T~21:15Z verbatim, banked in
STATE/DECISIONS.md, tests-first requirement:

    "SEV-1 wire on chain break — security-group page + Watch signal
     recorded · evidence-never-action discipline.
     Tests-first requirement: deliberately-broken chain produces BOTH
     the paging AND the Watch signal; any shared credential fails a
     dedicated test."

B-M10-Q2 verbatim (2026-09-18T~12:30Z):
    "SEV-1 wiring: a chain break pages the security group per B.10
     and is additionally recorded as a Watch signal, never as an
     action — it's evidence, and it belongs in the certificate ground."

Discipline (structurally enforced by the invariant test suite):
  * **Evidence-never-fabricated (Canon 8 §W1 eyes-never-act):** if
    `receipt.break_at_seq is None` (intact chain), this helper writes
    NEITHER a page NOR a Watch signal. Absence of signal is not a
    signal.
  * **Evidence-never-action:** this module imports NO action-plane
    surface. It does not touch `services.watch.mkono` (the hand) and
    does not touch `services.ledger_writer` (the write authority).
  * **C3 credential separation:** the wire refuses under any
    `credential_handle != LEDGER_VERIFIER_CRED_HANDLE` (positive gate
    reused from W2a). Any shared credential fails a dedicated test
    per the owner's tests-first requirement.

Contract:
  `wire_sev1_on_chain_break(receipt, page_root, watch_root, at_iso,
                            credential_handle)` — if
      `receipt.break_at_seq is not None`, atomically emit one
      `Sev1Page` and one `LedgerChainBreakSignal` (both records carry
      the same `tenant_id`, `break_at_seq`, `head_seq`, `head_hash`,
      and `at_iso`). If `receipt.break_at_seq is None`, do nothing.
"""
from __future__ import annotations

from pathlib import Path

from contracts.ledger_credentials import LEDGER_VERIFIER_CRED_HANDLE
from services.ledger_verifier.receipt_store import SharedCredentialRefused
from services.ledger_verifier.sev1_paging import Sev1Page, raise_sev1_page
from services.ledger_verifier.verify import VerifierReceipt
from services.watch.ledger_chain_break_signal import (
    LedgerChainBreakSignal,
    record_chain_break_signal,
)


def _c3_gate(credential_handle: str) -> None:
    if credential_handle != LEDGER_VERIFIER_CRED_HANDLE:
        raise SharedCredentialRefused(
            f"LEDGER-VERIFIER-C3-001: refused sev1_wire call with "
            f"credential_handle={credential_handle!r} — only the "
            f"verifier credential handle is admitted."
        )


def wire_sev1_on_chain_break(
    *,
    receipt: VerifierReceipt,
    page_root: Path,
    watch_root: Path,
    at_iso: str,
    credential_handle: str,
) -> None:
    """Wire a verifier receipt into the SEV-1 paging + Watch evidence
    surfaces.

    Chain intact (`receipt.break_at_seq is None`) → no-op (evidence-never-
    fabricated).

    Chain broken (`receipt.break_at_seq is not None`) → atomic emit of
    one `Sev1Page` (to the paging endpoint) AND one
    `LedgerChainBreakSignal` (to the Watch evidence store).
    """
    # C3 gate FIRST — any shared credential must fail before the module
    # inspects the receipt shape at all.
    _c3_gate(credential_handle)

    if receipt.break_at_seq is None:
        return

    page = Sev1Page(
        tenant_id=receipt.tenant_id,
        break_at_seq=receipt.break_at_seq,
        head_seq=receipt.head_seq,
        head_hash=receipt.head_hash,
        paged_at_iso=at_iso,
    )
    raise_sev1_page(
        page=page,
        page_root=page_root,
        credential_handle=credential_handle,
    )

    signal = LedgerChainBreakSignal(
        tenant_id=receipt.tenant_id,
        break_at_seq=receipt.break_at_seq,
        head_seq=receipt.head_seq,
        head_hash=receipt.head_hash,
        observed_at_iso=at_iso,
    )
    record_chain_break_signal(
        signal=signal,
        watch_root=watch_root,
        credential_handle=credential_handle,
    )


__all__ = ["wire_sev1_on_chain_break"]
