"""services.ledger_verifier.cadence — M10-W2b · cadence scheduler primitive.

Owner Run Order 2026-09-18T~21:15Z (verbatim, banked in STATE/DECISIONS.md):
    "nightly plus on-demand"

B-M10-Q2 verbatim (2026-09-18T~12:30Z):
    "Cadence: nightly per tenant + on-demand (R-18 effect 12)."

Closed intent alphabet (per SO §3.10-α · owner ruling 2026-09-17T~13:26Z ·
tuple[str] admitted · `enum.Enum` still banned):
    CADENCE_INTENT_ALPHABET = ("nightly", "on_demand")

Contract:
  `record_run_intent(tenant_id, intent_kind, at_iso, journal_root,
                     credential_handle)` :
      Refuses on non-verifier credential handle (C3 gate reused from
      W2a) → `SharedCredentialRefused`.
      Refuses on `intent_kind not in CADENCE_INTENT_ALPHABET` →
      `UnknownCadenceIntentRefused` (`LEDGER-VERIFIER-CADENCE-001`).
      Appends a `CadenceIntent` record to the per-tenant journal.

  `list_intents_for_tenant(tenant_id, journal_root, credential_handle)` :
      Same C3 gate. Returns intents in append order.

Intent journaling is the WHEN-was-a-verify-scheduled surface.  The
actual verifier walk (`verify_chain()`) is called separately; cadence
does NOT invoke the verifier — it only records intents.  This
preserves W2a's discipline (each module has one job) and lets the
scheduling side be tested independently of the verifier's semantics.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Final, List, Tuple

from contracts.ledger_credentials import LEDGER_VERIFIER_CRED_HANDLE
from services.ledger_verifier.receipt_store import (
    LedgerVerifierRefusalError,
    SharedCredentialRefused,
)


CADENCE_INTENT_ALPHABET: Final[Tuple[str, str]] = ("nightly", "on_demand")


class UnknownCadenceIntentRefused(LedgerVerifierRefusalError):
    """LEDGER-VERIFIER-CADENCE-001 · intent_kind not on closed alphabet."""

    code: str = "LEDGER-VERIFIER-CADENCE-001"


@dataclass(frozen=True)
class CadenceIntent:
    """Frozen record of a scheduled verifier run intent."""

    tenant_id: str
    intent_kind: str  # one of CADENCE_INTENT_ALPHABET
    at_iso: str


_HANDLE_SAFE_RE = re.compile(r"[^A-Za-z0-9._-]")


def _handle_namespace(handle: str) -> str:
    return _HANDLE_SAFE_RE.sub("_", handle)


def _c3_gate(credential_handle: str) -> None:
    if credential_handle != LEDGER_VERIFIER_CRED_HANDLE:
        raise SharedCredentialRefused(
            f"LEDGER-VERIFIER-C3-001: refused cadence call with "
            f"credential_handle={credential_handle!r} — only the "
            f"verifier credential handle is admitted."
        )


def _intent_path(
    *, journal_root: Path, credential_handle: str, tenant_id: str
) -> Path:
    tenant_dir = journal_root / _handle_namespace(credential_handle) / tenant_id
    tenant_dir.mkdir(parents=True, exist_ok=True)
    return tenant_dir / "intents.jsonl"


def record_run_intent(
    *,
    tenant_id: str,
    intent_kind: str,
    at_iso: str,
    journal_root: Path,
    credential_handle: str,
) -> None:
    """Append a `CadenceIntent` to the per-tenant journal.

    Refuses on non-verifier credential handle (C3).
    Refuses on `intent_kind not in CADENCE_INTENT_ALPHABET`.
    """
    _c3_gate(credential_handle)
    if intent_kind not in CADENCE_INTENT_ALPHABET:
        raise UnknownCadenceIntentRefused(
            f"LEDGER-VERIFIER-CADENCE-001: intent_kind={intent_kind!r} "
            f"not in closed alphabet {CADENCE_INTENT_ALPHABET!r}. Owner "
            "run order verbatim: 'nightly plus on-demand'."
        )
    path = _intent_path(
        journal_root=journal_root,
        credential_handle=credential_handle,
        tenant_id=tenant_id,
    )
    intent = CadenceIntent(
        tenant_id=tenant_id, intent_kind=intent_kind, at_iso=at_iso
    )
    line = json.dumps(asdict(intent), sort_keys=True, separators=(",", ":"))
    with path.open("a") as fh:
        fh.write(line + "\n")


def list_intents_for_tenant(
    *,
    tenant_id: str,
    journal_root: Path,
    credential_handle: str,
) -> List[CadenceIntent]:
    """Return recorded intents for a tenant in append order."""
    _c3_gate(credential_handle)
    path = _intent_path(
        journal_root=journal_root,
        credential_handle=credential_handle,
        tenant_id=tenant_id,
    )
    if not path.exists():
        return []
    out: List[CadenceIntent] = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        out.append(CadenceIntent(**raw))
    return out


__all__ = [
    "CADENCE_INTENT_ALPHABET",
    "CadenceIntent",
    "UnknownCadenceIntentRefused",
    "record_run_intent",
    "list_intents_for_tenant",
]
