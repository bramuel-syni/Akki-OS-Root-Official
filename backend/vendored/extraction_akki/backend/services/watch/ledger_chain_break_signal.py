"""services.watch.ledger_chain_break_signal — M10-W3 · Watch evidence
surface for a ledger chain break.

Owner Run Order 2026-09-18T~21:15Z (verbatim, banked in STATE/DECISIONS.md):
    "SEV-1 wire on chain break — security-group page + Watch signal
     recorded · evidence-never-action discipline"

B-M10-Q2 verbatim (2026-09-18T~12:30Z):
    "SEV-1 wiring: a chain break pages the security group per B.10
     and is additionally recorded as a Watch signal, never as an
     action — it's evidence, and it belongs in the certificate ground."

DISTINCT from `services.watch.sever_signals`:
  * `sever_signals` holds the closed six-kind sever-certainty registry
    (canary touch · attestation failure · mark hit · witness-write
    attempt · floor violation · mirage incrimination) per Canon 8
    §Line 31. Widening the six-kind grammar is banned by canon.
  * A ledger chain break is NOT one of the six sever-certainty kinds.
    It is operational-integrity evidence recorded on the Watch side
    (Macho half · the eyes) so that the security authority holds the
    same walkable record the governing authority does. It never
    unlocks maximum autonomous force; it never mints a Mark; it never
    triggers Mkono. It is pure evidence in the certificate ground.

Contract:
  `LedgerChainBreakSignal` — frozen 5-field dataclass ·
    tenant_id · break_at_seq · head_seq · head_hash · observed_at_iso.
    No confidence/score/strength/probability field (M3 forward-compat).

  `record_chain_break_signal(signal, watch_root, credential_handle)` —
    appends the signal as a JSON line to
    `<watch_root>/<verifier-namespace>/<tenant_id>/chain_break_signals.jsonl`.
    Refuses under any `credential_handle != LEDGER_VERIFIER_CRED_HANDLE`
    (C3 gate reused from W2a — the emitter is the verifier, which is
    also the surface holding the evidence on the Watch side).

  `list_chain_break_signals_for_tenant(tenant_id, watch_root, credential_handle)` —
    returns signals in append order. Same C3 gate.

Evidence-never-action discipline (Canon 8 §W1 eyes-never-act):
this module imports NO action-plane surface (no `services.watch.mkono`,
no `services.ledger_writer`). The Watch chain-break signal is pure
Macho, pure eyes, zero hand.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

from contracts.ledger_credentials import LEDGER_VERIFIER_CRED_HANDLE
from services.ledger_verifier.receipt_store import SharedCredentialRefused


_HANDLE_SAFE_RE = re.compile(r"[^A-Za-z0-9._-]")


def _handle_namespace(handle: str) -> str:
    return _HANDLE_SAFE_RE.sub("_", handle)


@dataclass(frozen=True)
class LedgerChainBreakSignal:
    """M3-forward-compat frozen record of a Watch-observed ledger chain
    break.

    Exactly five owner-ratified fields — adding a sixth (especially any
    confidence/score/strength/probability field) is a §3.3 seal event.

    NOT a sever-certainty registry entry (Canon 8 §Line 31 six-kind
    closed grammar is preserved). This is operational-integrity
    evidence: it never unlocks maximum autonomous force.
    """

    tenant_id: str
    break_at_seq: int
    head_seq: int
    head_hash: str
    observed_at_iso: str


def _c3_gate(credential_handle: str) -> None:
    if credential_handle != LEDGER_VERIFIER_CRED_HANDLE:
        raise SharedCredentialRefused(
            f"LEDGER-VERIFIER-C3-001: refused chain_break_signal call "
            f"with credential_handle={credential_handle!r} — only the "
            f"verifier credential handle is admitted."
        )


def _signal_path(*, watch_root: Path, credential_handle: str, tenant_id: str) -> Path:
    tenant_dir = watch_root / _handle_namespace(credential_handle) / tenant_id
    tenant_dir.mkdir(parents=True, exist_ok=True)
    return tenant_dir / "chain_break_signals.jsonl"


def record_chain_break_signal(
    *,
    signal: LedgerChainBreakSignal,
    watch_root: Path,
    credential_handle: str,
) -> None:
    """Append `signal` to the per-tenant Watch chain-break evidence store."""
    _c3_gate(credential_handle)
    path = _signal_path(
        watch_root=watch_root,
        credential_handle=credential_handle,
        tenant_id=signal.tenant_id,
    )
    line = json.dumps(asdict(signal), sort_keys=True, separators=(",", ":"))
    with path.open("a") as fh:
        fh.write(line + "\n")


def list_chain_break_signals_for_tenant(
    *,
    tenant_id: str,
    watch_root: Path,
    credential_handle: str,
) -> List[LedgerChainBreakSignal]:
    """Return Watch chain-break signals for a tenant in append order."""
    _c3_gate(credential_handle)
    path = _signal_path(
        watch_root=watch_root,
        credential_handle=credential_handle,
        tenant_id=tenant_id,
    )
    if not path.exists():
        return []
    out: List[LedgerChainBreakSignal] = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        out.append(LedgerChainBreakSignal(**raw))
    return out


__all__ = [
    "LedgerChainBreakSignal",
    "record_chain_break_signal",
    "list_chain_break_signals_for_tenant",
]
