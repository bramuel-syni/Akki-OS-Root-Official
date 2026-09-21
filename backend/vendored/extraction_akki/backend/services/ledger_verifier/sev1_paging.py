"""services.ledger_verifier.sev1_paging — M10-W3 · SEV-1 security-group
paging primitive on chain break.

Owner Run Order 2026-09-18T~21:15Z (verbatim, banked in STATE/DECISIONS.md):
    "SEV-1 wire on chain break — security-group page + Watch signal
     recorded · evidence-never-action discipline"

B-M10-Q2 verbatim (2026-09-18T~12:30Z):
    "SEV-1 wiring: a chain break pages the security group per B.10
     and is additionally recorded as a Watch signal, never as an
     action — it's evidence, and it belongs in the certificate ground."

Contract:
  `Sev1Page` — frozen 5-field dataclass ·
    tenant_id · break_at_seq · head_seq · head_hash · paged_at_iso.
    No confidence/score/strength/probability field (M3 forward-compat).

  `raise_sev1_page(page, page_root, credential_handle)` — appends the
    page as a JSON line to
    `<page_root>/<verifier-namespace>/<tenant_id>/sev1_pages.jsonl`.
    Refuses under any `credential_handle != LEDGER_VERIFIER_CRED_HANDLE`
    (C3 gate reused from W2a).

  `list_pages_for_tenant(tenant_id, page_root, credential_handle)` —
    returns pages in append order. Same C3 gate.

Evidence-never-action discipline (Canon 8 §W1 eyes-never-act):
this module imports NO action-plane surface (no `services.watch.mkono`,
no `services.ledger_writer`). The SEV-1 wire is pure evidence.
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
class Sev1Page:
    """M3-forward-compat frozen record of a SEV-1 security-group page.

    Exactly five owner-ratified fields — adding a sixth (especially any
    confidence/score/strength/probability field) is a §3.3 seal event.
    """

    tenant_id: str
    break_at_seq: int
    head_seq: int
    head_hash: str
    paged_at_iso: str


def _c3_gate(credential_handle: str) -> None:
    if credential_handle != LEDGER_VERIFIER_CRED_HANDLE:
        raise SharedCredentialRefused(
            f"LEDGER-VERIFIER-C3-001: refused sev1_paging call with "
            f"credential_handle={credential_handle!r} — only the "
            f"verifier credential handle is admitted."
        )


def _page_path(*, page_root: Path, credential_handle: str, tenant_id: str) -> Path:
    tenant_dir = page_root / _handle_namespace(credential_handle) / tenant_id
    tenant_dir.mkdir(parents=True, exist_ok=True)
    return tenant_dir / "sev1_pages.jsonl"


def raise_sev1_page(
    *,
    page: Sev1Page,
    page_root: Path,
    credential_handle: str,
) -> None:
    """Append `page` to the per-tenant SEV-1 paging endpoint."""
    _c3_gate(credential_handle)
    path = _page_path(
        page_root=page_root,
        credential_handle=credential_handle,
        tenant_id=page.tenant_id,
    )
    line = json.dumps(asdict(page), sort_keys=True, separators=(",", ":"))
    with path.open("a") as fh:
        fh.write(line + "\n")


def list_pages_for_tenant(
    *,
    tenant_id: str,
    page_root: Path,
    credential_handle: str,
) -> List[Sev1Page]:
    """Return SEV-1 pages for a tenant in append order."""
    _c3_gate(credential_handle)
    path = _page_path(
        page_root=page_root,
        credential_handle=credential_handle,
        tenant_id=tenant_id,
    )
    if not path.exists():
        return []
    out: List[Sev1Page] = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        out.append(Sev1Page(**raw))
    return out


__all__ = [
    "Sev1Page",
    "raise_sev1_page",
    "list_pages_for_tenant",
]
