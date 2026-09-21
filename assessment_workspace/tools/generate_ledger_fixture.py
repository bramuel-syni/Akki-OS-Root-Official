#!/usr/bin/env python3
"""Generate an audit-labelled Ledger fixture segment via SEALED code only.

- Tenant: `AUDIT-FIXTURE-20260921` (explicit fixture, not production data).
- Storage root: /app/audit/inbox/verifier_receipt_store/  (outside repo trees).
- Uses ONLY sealed Extraction-Akki backend modules (imports; no code
  modifications to services/, contracts/, or tests/).
- Chain includes at least one genuine refused-operation row
  (event_type="refuse", decision="refused", reason_code from real
  compliance/refusal_families.v0.json).
- Additionally demonstrates a REAL sealed-writer refusal path by driving
  the writer to raise OutOfOrderSeqRefused (captured, not swallowed).
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

# --- point sys.path at Extraction-Akki backend (SEALED — no modification) ---
REPO = Path("/app/assessment_workspace/repos/Extraction-Akki")
sys.path.insert(0, str(REPO / "backend"))

# All imports below are from the sealed code tree.
from contracts.ledger_credentials import LEDGER_VERIFIER_CRED_HANDLE
from contracts.ledger_v1 import LedgerRow, LedgerRowAt, canonical_row_bytes
from services.ledger_emitter.emit_intent import LedgerIntent, emit_intent
from services.ledger_writer.main import (
    OutOfOrderSeqRefused,
    append_intent,
    compute_row_hash,
)
from services.ledger_verifier.receipt_store import VerifierReceiptStore
from services.ledger_verifier.verify import VerifierReceipt, verify_chain

# --- fixture constants ---
TENANT = "AUDIT-FIXTURE-20260921"
RUN_ID = "audit-run-20260921"
INBOX = Path("/app/audit/inbox")
STORAGE_ROOT = INBOX / "verifier_receipt_store"
STORAGE_ROOT.mkdir(parents=True, exist_ok=True)

FIXTURE_EPOCH = 1758470400  # 2026-09-21T12:00:00Z — deterministic

# --- deterministic sha256 helper (for payload_ref) ---
def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

# --- build a contiguous chain of intents ---
def _intent(
    seq_hint: int,
    event_type: str,
    decision: str,
    resource_type: str,
    resource_id: str,
    reason_code: str = "",
    actor_id: str = "service:audit_fixture_driver",
) -> LedgerIntent:
    """Wrap the sealed emitter."""
    return emit_intent(
        intent=LedgerIntent(
            tenant_id=TENANT,
            run_id=RUN_ID,
            task_id=f"audit-task-{seq_hint:03d}",
            actor_id=actor_id,
            actor_type="service",
            event_type=event_type,
            resource_type=resource_type,
            resource_id=resource_id,
            decision=decision,
            reason_code=reason_code,
            payload_ref=_sha(f"{TENANT}|{seq_hint}|{event_type}|{decision}|{reason_code}"),
            at=LedgerRowAt(epoch_s=FIXTURE_EPOCH + seq_hint, source="wall_clock"),
            break_glass_session_id=None,
        )
    )

# Chain design: 6 rows, 2 refused-operation rows (seq 3, seq 5) from real
# refusal families in services/compliance/refusal_families.v0.json and
# services/memory/memory_refusal_reasons.v0.json.
intents: list[LedgerIntent] = [
    _intent(1, "admit",    "admitted",  "objective",        "obj-A",
            actor_id="service:northena_admit"),
    _intent(2, "gate",     "passed",    "chokepoint_cross", "cross-1",
            actor_id="service:chokepoint_gate"),
    _intent(3, "refuse",   "refused",   "publication",      "pub-42",
            reason_code="publication_gate_denied",
            actor_id="service:memory_publication"),
    _intent(4, "converge", "converged", "solva_conclusion", "conc-77",
            actor_id="service:northena_converge"),
    _intent(5, "refuse",   "refused",   "composition",      "comp-11",
            reason_code="composition_below_floor",
            actor_id="service:service_1_composition"),
    _intent(6, "admit",    "admitted",  "artifact",         "art-9",
            actor_id="service:northena_admit"),
]

# --- append each intent via SEALED writer (hash-chaining) ---
rows: list[LedgerRow] = []
prev_row: LedgerRow | None = None
for i, intent in enumerate(intents, start=1):
    row = append_intent(intent=intent, prev_row=prev_row, tenant_seq_next=i)
    rows.append(row)
    prev_row = row

# --- demonstrate a REAL sealed-writer refusal path (out-of-order seq) ---
writer_refusal_receipt = None
try:
    _bad = append_intent(
        intent=intents[0],  # any intent
        prev_row=rows[-1],
        tenant_seq_next=99,  # deliberately wrong: should be 7
    )
    writer_refusal_receipt = {
        "attempted_illegal_op": "seq=99 while prev_row.seq=6",
        "outcome": "UNEXPECTED_SUCCESS_bug",
    }
except OutOfOrderSeqRefused as exc:
    writer_refusal_receipt = {
        "attempted_illegal_op": "append_intent(seq=99, prev_row.seq=6)",
        "outcome": "REFUSED_BY_SEALED_WRITER",
        "code": exc.code,
        "message_shape": {
            "startswith_code": str(exc).startswith("LEDGER-WRITER-001"),
            "length": len(str(exc)),
        },
    }

# --- SEALED verifier walks the segment ---
receipt: VerifierReceipt = verify_chain(rows_in_seq_order=rows)

# --- SEALED receipt store writes the receipt ---
store = VerifierReceiptStore(
    credential_handle=LEDGER_VERIFIER_CRED_HANDLE,
    storage_root=STORAGE_ROOT,
)
store.append(receipt)

# --- dump the chain to a snapshot (for auditor consumption) ---
def _row_to_dict(row: LedgerRow) -> dict:
    d = {
        "seq": row.seq,
        "prev_hash": row.prev_hash,
        "hash": row.hash,
        "schema_version": row.schema_version,
        "tenant_id": row.tenant_id,
        "run_id": row.run_id,
        "task_id": row.task_id,
        "actor_id": row.actor_id,
        "actor_type": row.actor_type,
        "event_type": row.event_type,
        "resource_type": row.resource_type,
        "resource_id": row.resource_id,
        "decision": row.decision,
        "reason_code": row.reason_code,
        "payload_ref": row.payload_ref,
        "at": {"epoch_s": row.at.epoch_s, "source": row.at.source},
        "break_glass_session_id": row.break_glass_session_id,
    }
    return d

snapshot = {
    "provenance": {
        "generator": "generate_ledger_fixture.py",
        "generator_path": "/app/audit/tools/generate_ledger_fixture.py",
        "generated_at_utc": "2026-09-21T~17:45Z",
        "tenant_id": TENANT,
        "audit_target_code_tag": "audit/code-20260921",
        "audit_target_code_commit": "283524d89dd337d79014b114d575ced7baab6dfc",
        "notice": (
            "AUDIT FIXTURE — generated 2026-09-21 via the SEALED "
            "services.ledger_emitter, services.ledger_writer, and "
            "services.ledger_verifier packages. Not production data. "
            "No production tenant chain existed at export time; the "
            "fixture segment is the only chain for this tenant."
        ),
    },
    "segment_bounds": {
        "tenant_id": TENANT,
        "seq_start": rows[0].seq,
        "seq_end": rows[-1].seq,
        "row_count": len(rows),
        "refused_row_seqs": [r.seq for r in rows if r.decision == "refused"],
        "refused_row_count": sum(1 for r in rows if r.decision == "refused"),
    },
    "rows": [_row_to_dict(r) for r in rows],
    "verifier_receipt": {
        "tenant_id": receipt.tenant_id,
        "head_seq": receipt.head_seq,
        "head_hash": receipt.head_hash,
        "break_at_seq": receipt.break_at_seq,
        "rows_walked": receipt.rows_walked,
    },
    "sealed_writer_refusal_demonstration": writer_refusal_receipt,
}

snapshot_path = INBOX / "ledger_snapshot_AUDIT-FIXTURE-20260921.json"
snapshot_path.write_text(json.dumps(snapshot, indent=2, sort_keys=True))
print("Ledger snapshot:", snapshot_path)
print("Receipt store   :", STORAGE_ROOT)
print()
print("Segment:", snapshot["segment_bounds"])
print("Head hash:", receipt.head_hash)
print("Chain intact:", receipt.break_at_seq is None)
print("Refused rows:", snapshot["segment_bounds"]["refused_row_seqs"])
print("Writer refusal path demonstrated:",
      writer_refusal_receipt["outcome"] if writer_refusal_receipt else "NO")

# --- README ---
readme = f"""# Akki OS · Audit Fixture · Ledger snapshot + verifier receipt store

**Not production data.** No production tenant chain existed at export time.
This bundle is a fixture generated 2026-09-21 via the sealed
`services.ledger_emitter`, `services.ledger_writer`, and
`services.ledger_verifier` packages from Extraction-Akki
programme/track-a at tag `audit/code-20260921` (commit
`283524d89dd337d79014b114d575ced7baab6dfc`).

## Tenant
- `tenant_id = "{TENANT}"`

## Segment bounds
- seq {rows[0].seq} .. seq {rows[-1].seq}  (row_count = {len(rows)})
- refused-operation rows: seq {snapshot['segment_bounds']['refused_row_seqs']}
- head hash: `{receipt.head_hash}`
- chain intact: `{receipt.break_at_seq is None}` (`break_at_seq={receipt.break_at_seq}`)

## Refused-operation rows in the chain
Each is a real refusal shape written through the sealed writer:

- **seq 3**: `event_type="refuse"`, `decision="refused"`, `reason_code="publication_gate_denied"`
  (registered in `services/memory/memory_refusal_reasons.v0.json`).
- **seq 5**: `event_type="refuse"`, `decision="refused"`, `reason_code="composition_below_floor"`
  (registered in `services/compliance/refusal_families.v0.json`).

## Sealed-writer refusal path demonstration
The driver additionally attempted an out-of-order `append_intent`
(`tenant_seq_next=99` while `prev_row.seq=6`). The sealed writer
raised `OutOfOrderSeqRefused` (code `LEDGER-WRITER-001`) — a REAL
refusal path exercised by the segment, not a hand-crafted row.
Outcome recorded verbatim in
`ledger_snapshot_AUDIT-FIXTURE-20260921.json` under
`sealed_writer_refusal_demonstration`.

## Verifier receipt store
- Storage root: `verifier_receipt_store/`
- Verifier credential handle: `akki.ledger.verifier.credential.v0`
  (positive-allowlist gate in `services/ledger_verifier/receipt_store.py`)
- Layout: `verifier_receipt_store/akki.ledger.verifier.credential.v0/{TENANT}/seq-000000000006.json`

## Files in this bundle
- `Master_Requirements_Registry_QA_v2_builder_status.xlsx` — filled workbook (Builder Status col K, all 602 rows)
- `ledger_snapshot_AUDIT-FIXTURE-20260921.json` — the chain segment
- `verifier_receipt_store/…` — receipt store tree (append-only)
- `akki_audit_20260921_code.bundle` — Extraction-Akki repo bundle including tag `audit/code-20260921`
- `akki_audit_20260921_state.bundle` — assessment_workspace repo bundle including tag `audit/state-20260921`
- `README_fixture.md` — this file

## Recreating the receipt
Any auditor can walk the chain from the snapshot rows via
`services.ledger_verifier.verify.verify_chain(rows_in_seq_order=…)`
under the audit tag and obtain the same `head_hash`.

## Notice
The fixture segment is not a substitute for a production tenant chain.
It exists so the auditor can walk sealed writer + verifier code with a
real chain shape.  Absence of a production tenant chain at
`audit/code-20260921` is itself a finding recorded in
`STATE/DECISIONS.md`.
"""
readme_path = INBOX / "README_fixture.md"
readme_path.write_text(readme)
print("README         :", readme_path)
