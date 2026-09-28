"""services.ledger_verifier.receipt_store — M10-W2a · append-only receipt store.

Owner Run Order 2026-09-18T~21:15Z (verbatim, banked in STATE/DECISIONS.md):
    "Verifier under credentials the writer does not hold; its own
     append-only receipt store ..."

Owner ruling anchor B-M10-Q2 (2026-09-18T~12:30Z verbatim):
    "verifier writes its receipts to its own append-only store under
     credentials the Ledger writer does NOT hold (C3 principle:
     verifier cannot share anything with the thing it verifies)".

Contract:
  `VerifierReceiptStore(credential_handle, storage_root)` :
    * Constructor refuses (raises `SharedCredentialRefused`) unless
      `credential_handle == LEDGER_VERIFIER_CRED_HANDLE`.  Positive
      allowlist — any other handle (writer's or arbitrary third-party)
      is refused.
    * Persistence directory is scoped by the verifier credential
      handle (namespace isolation from any writer path).
    * APPEND-ONLY: only `append(receipt)`, `read(...)`, and
      `list_for_tenant(...)` are exposed.  No `update`, no `delete`
      attributes are defined — attempting either raises `AttributeError`
      at attribute-access time (Python's default behaviour when the
      method is not defined).
    * Re-appending an existing (tenant_id, head_seq) pair raises
      `VerifierReceiptOverwriteRefused` (LEDGER-VERIFIER-STORE-001).

Persistence shape:
  <storage_root>/<verifier-namespaced-dir>/<tenant_id>/seq-<head_seq>.json
  Each file is a JSON dict of the VerifierReceipt fields.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict
from pathlib import Path
from typing import List

from contracts.ledger_credentials import (
    LEDGER_VERIFIER_CRED_HANDLE,
)
from services.ledger_verifier.verify import VerifierReceipt


# ---------------------------------------------------------------------------
# Refusal types
# ---------------------------------------------------------------------------


class LedgerVerifierRefusalError(Exception):
    """Root of ledger-verifier receipt-store refusals."""

    code: str = ""


class SharedCredentialRefused(LedgerVerifierRefusalError):
    """LEDGER-VERIFIER-C3-001 · construction with a non-verifier credential handle."""

    code: str = "LEDGER-VERIFIER-C3-001"


class VerifierReceiptOverwriteRefused(LedgerVerifierRefusalError):
    """LEDGER-VERIFIER-STORE-001 · append of an already-present (tenant_id, head_seq)."""

    code: str = "LEDGER-VERIFIER-STORE-001"


# ---------------------------------------------------------------------------
# Namespace helper
# ---------------------------------------------------------------------------


_HANDLE_SAFE_RE = re.compile(r"[^A-Za-z0-9._-]")


def _handle_namespace(handle: str) -> str:
    """Filesystem-safe namespace derived from a credential handle.

    Preserves the handle string so `test_verifier_receipt_store_persistence_path_scoped_to_verifier_credential_handle`
    can locate the namespace by substring match.
    """
    # Replace only characters that are actively unsafe on disk; keep dots
    # so the handle remains substring-recognisable.
    return _HANDLE_SAFE_RE.sub("_", handle)


# ---------------------------------------------------------------------------
# VerifierReceiptStore
# ---------------------------------------------------------------------------


class VerifierReceiptStore:
    """Append-only receipt store for `VerifierReceipt` records.

    See module docstring for the C3 credential-separation contract.
    """

    def __init__(self, *, credential_handle: str, storage_root: Path) -> None:
        # Positive allowlist: only LEDGER_VERIFIER_CRED_HANDLE is admitted.
        # The writer's credential handle (and every other handle) is
        # refused by this single check — the C3 gate is a positive
        # allowlist, not a negative check against a named writer handle.
        # (Importing LEDGER_WRITER_CRED_HANDLE here would violate the
        # C3 AST invariant `test_ledger_verifier_does_not_import_writer_credential_handle`.)
        if credential_handle != LEDGER_VERIFIER_CRED_HANDLE:
            raise SharedCredentialRefused(
                f"LEDGER-VERIFIER-C3-001: refused construction with "
                f"credential_handle={credential_handle!r} — only the "
                f"verifier credential handle is admitted; the C3 gate "
                f"is a positive allowlist, not a negative check."
            )

        self._credential_handle = credential_handle
        self._storage_root = Path(storage_root)
        self._namespace = _handle_namespace(credential_handle)
        self._store_dir = self._storage_root / self._namespace
        self._store_dir.mkdir(parents=True, exist_ok=True)

    # No `update` method defined.
    # No `delete` method defined.
    # Both `hasattr(store, "update")` and `hasattr(store, "delete")`
    # therefore return False (append-only by construction).

    def _receipt_path(self, *, tenant_id: str, head_seq: int) -> Path:
        tenant_dir = self._store_dir / tenant_id
        tenant_dir.mkdir(parents=True, exist_ok=True)
        return tenant_dir / f"seq-{head_seq:012d}.json"

    def append(self, receipt: VerifierReceipt) -> None:
        """Append a receipt.  Refuses re-append of an existing
        (tenant_id, head_seq)."""
        path = self._receipt_path(
            tenant_id=receipt.tenant_id, head_seq=receipt.head_seq
        )
        if path.exists():
            raise VerifierReceiptOverwriteRefused(
                f"LEDGER-VERIFIER-STORE-001: refused overwrite of receipt at "
                f"tenant_id={receipt.tenant_id!r} head_seq={receipt.head_seq} — "
                f"the verifier store is APPEND-ONLY (B-M10-Q2 verbatim)."
            )
        path.write_text(
            json.dumps(asdict(receipt), sort_keys=True, separators=(",", ":"))
        )

    def read(self, *, tenant_id: str, head_seq: int) -> VerifierReceipt:
        """Read a specific receipt by (tenant_id, head_seq)."""
        path = self._receipt_path(tenant_id=tenant_id, head_seq=head_seq)
        raw = json.loads(path.read_text())
        return VerifierReceipt(**raw)

    def list_for_tenant(self, *, tenant_id: str) -> List[VerifierReceipt]:
        """Return receipts for a tenant in append order (ascending head_seq)."""
        tenant_dir = self._store_dir / tenant_id
        if not tenant_dir.is_dir():
            return []
        out: List[VerifierReceipt] = []
        for f in sorted(tenant_dir.glob("seq-*.json")):
            raw = json.loads(f.read_text())
            out.append(VerifierReceipt(**raw))
        return out


__all__ = [
    "SharedCredentialRefused",
    "VerifierReceiptOverwriteRefused",
    "VerifierReceiptStore",
    "LedgerVerifierRefusalError",
]
