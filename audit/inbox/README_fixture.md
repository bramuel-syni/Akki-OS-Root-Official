# Akki OS · Audit Fixture · Ledger snapshot + verifier receipt store

**Not production data.** No production tenant chain existed at export time.
This bundle is a fixture generated 2026-09-21 via the sealed
`services.ledger_emitter`, `services.ledger_writer`, and
`services.ledger_verifier` packages from Extraction-Akki
programme/track-a at tag `audit/code-20260921` (commit
`283524d89dd337d79014b114d575ced7baab6dfc`).

## Tenant
- `tenant_id = "AUDIT-FIXTURE-20260921"`

## Segment bounds
- seq 1 .. seq 6  (row_count = 6)
- refused-operation rows: seq [3, 5]
- head hash: `548b3d9bafcaec19ace23bc92520f03617dddde915c75d2120285f67ca7d78a0`
- chain intact: `True` (`break_at_seq=None`)

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
- Layout: `verifier_receipt_store/akki.ledger.verifier.credential.v0/AUDIT-FIXTURE-20260921/seq-000000000006.json`

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
