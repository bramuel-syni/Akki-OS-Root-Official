"""contracts.ledger_credentials — M10-W2a · frozen credential-handle constants.

Owner Run Order 2026-09-18T~21:15Z (verbatim, banked in STATE/DECISIONS.md):
    "Verifier under credentials the writer does not hold; its own
     append-only receipt store ..."

Owner ruling anchor B-M10-Q2 (2026-09-18T~12:30Z verbatim):
    "verifier writes its receipts to its own append-only store under
     credentials the Ledger writer does NOT hold (C3 principle:
     verifier cannot share anything with the thing it verifies)".

C3 principle: the ledger writer and the ledger verifier hold DISJOINT
credential handles.  No module holds both.  Sharing is refused
structurally by construction — the two handles are distinct string
constants living in this file, and the verifier's receipt store
refuses to construct if handed the writer's handle.

Adding, renaming, or otherwise altering either handle is a §3.3 seal
event requiring an Owner ruling recorded in STATE/DECISIONS.md.  Zero
alias, zero shim, zero back-compat overload: the two handles are
independent strings.
"""
from __future__ import annotations

from typing import Final


LEDGER_WRITER_CRED_HANDLE: Final[str] = "akki.ledger.writer.credential.v0"
"""The credential handle the Ledger writer holds.  Only
``services.ledger_writer.*`` may reference this constant.  The verifier
must NEVER import this constant (AST-enforced by
``test_ledger_verifier_does_not_import_writer_credential_handle``)."""


LEDGER_VERIFIER_CRED_HANDLE: Final[str] = "akki.ledger.verifier.credential.v0"
"""The credential handle the Ledger verifier holds.  Only
``services.ledger_verifier.*`` may reference this constant.  The
writer must NEVER import this constant (AST-enforced by
``test_ledger_writer_does_not_import_verifier_credential_handle``)."""


__all__ = [
    "LEDGER_WRITER_CRED_HANDLE",
    "LEDGER_VERIFIER_CRED_HANDLE",
]
