"""services.ledger_verifier.publication — M10-W2b · head-hash publication to
the tenant receipt endpoint (B.4).

Owner Run Order 2026-09-18T~21:15Z (verbatim, banked in STATE/DECISIONS.md):
    "head hash published to the tenant receipt endpoint"

Canon anchors:
  * v1.0 B.4 · "Publishes head hash to the tenant's receipt endpoint".
  * B-M10-Q2 verbatim: verifier writes its receipts to its own
    append-only store; publication is the tenant-facing analogue.
  * M3 forward-compat (owner run order 2026-09-18T~21:15Z): the M3
    verdict schema at M12b-W1 will carry {requirement_id,
    data_points[], observation_refs[]} and "no confidence, score,
    strength or probability field, enforced by a signature-as-guard
    test". HeadHashPublication is a certificate-like record and
    respects the same discipline preemptively at W2b (see the
    matching invariant test).

Contract:
  `HeadHashPublication` :
    frozen 5-field dataclass — tenant_id · head_seq · head_hash ·
    published_at_iso · verifier_receipt_signature. No score field,
    no confidence field, no strength field, no probability field.

  `publish_head_hash(publication, endpoint_root, credential_handle)` :
    Refuses (raises `SharedCredentialRefused`) unless
    `credential_handle == LEDGER_VERIFIER_CRED_HANDLE`. Appends
    `publication` as a JSON line to
    `<endpoint_root>/<verifier-namespace>/<tenant_id>/receipts.jsonl`.
    Append-only (no truncation, no rewrite).

  `list_publications_for_tenant(tenant_id, endpoint_root, credential_handle)` :
    Same C3 gate. Returns publications in append order.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, fields as dc_fields
from pathlib import Path
from typing import List

from contracts.ledger_credentials import LEDGER_VERIFIER_CRED_HANDLE
from services.ledger_verifier.receipt_store import SharedCredentialRefused


_HANDLE_SAFE_RE = re.compile(r"[^A-Za-z0-9._-]")


def _handle_namespace(handle: str) -> str:
    return _HANDLE_SAFE_RE.sub("_", handle)


@dataclass(frozen=True)
class HeadHashPublication:
    """M3-forward-compat frozen record for head-hash publication.

    Exactly five owner-ratified fields — adding a sixth (especially
    any confidence/score/strength/probability field) is a §3.3 seal
    event requiring an Owner ruling.
    """

    tenant_id: str
    head_seq: int
    head_hash: str
    published_at_iso: str
    verifier_receipt_signature: str


def _c3_gate(credential_handle: str) -> None:
    """Positive allowlist reused from W2a's C3 gate."""
    if credential_handle != LEDGER_VERIFIER_CRED_HANDLE:
        raise SharedCredentialRefused(
            f"LEDGER-VERIFIER-C3-001: refused publication call with "
            f"credential_handle={credential_handle!r} — only the "
            f"verifier credential handle is admitted."
        )


def _endpoint_path(
    *, endpoint_root: Path, credential_handle: str, tenant_id: str
) -> Path:
    tenant_dir = endpoint_root / _handle_namespace(credential_handle) / tenant_id
    tenant_dir.mkdir(parents=True, exist_ok=True)
    return tenant_dir / "receipts.jsonl"


def publish_head_hash(
    *,
    publication: HeadHashPublication,
    endpoint_root: Path,
    credential_handle: str,
) -> None:
    """Append `publication` to the tenant receipt endpoint.

    Refuses under any non-verifier credential handle (C3 gate).
    """
    _c3_gate(credential_handle)
    path = _endpoint_path(
        endpoint_root=endpoint_root,
        credential_handle=credential_handle,
        tenant_id=publication.tenant_id,
    )
    line = json.dumps(asdict(publication), sort_keys=True, separators=(",", ":"))
    with path.open("a") as fh:
        fh.write(line + "\n")


def list_publications_for_tenant(
    *,
    tenant_id: str,
    endpoint_root: Path,
    credential_handle: str,
) -> List[HeadHashPublication]:
    """Return publications for a tenant in append order."""
    _c3_gate(credential_handle)
    path = _endpoint_path(
        endpoint_root=endpoint_root,
        credential_handle=credential_handle,
        tenant_id=tenant_id,
    )
    if not path.exists():
        return []
    out: List[HeadHashPublication] = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        raw = json.loads(line)
        out.append(HeadHashPublication(**raw))
    return out


__all__ = [
    "HeadHashPublication",
    "publish_head_hash",
    "list_publications_for_tenant",
]
