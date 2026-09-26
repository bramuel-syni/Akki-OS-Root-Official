# DAP operational continuation — 2026-09-25

Owner approved P0 request/work/entitlement continuation; GPU recovery remains PARKED.
Reproduced pre-existing RED tests: 16 failed, 1 passed. Receipt:
`phase0/drill_receipts/dap_operational_v1/RED_resume.log`.

## Evidence-led design
- `northena/ledger.py` is a legacy filesystem writer with a best-effort Mongo
  mirror that swallows errors. Its sealed body is NOT changed or represented as
  an atomic Mongo writer. New Northena request coordination composes the current
  `ledger_emitter.emit_intent` and `ledger_writer.main.append_intent`.
- Add a persistence adapter inside ledger_writer: one insert-only Mongo envelope
  atomically contains the exact 17-field canonical row and hash-bound payload.
  Unique tenant sequence and command identity prevent forks/duplicate commands.
  No mutable request state store: reads project the immutable events.
- No owner-admitted licence/organisation binding or operational approval was
  established by the previous inventory. Do not manufacture either. Persist
  submitted→routing and a reason-coded routing hold; do NOT invent an illegal
  Routing→Blocked edge or claim execution. Metered consumption is absent until
  an actual governed operation consumes something under established terms.
- Entitlement reads consume canonical licence/catalog/rate Ledger payloads,
  resolve organisation membership server-side, and derive allowance per call.
  Missing/corrupt records remain unresolved, never a fabricated zero/free grant.
- Stop/retry/retrieval fail closed against actual record state and prerequisites.
  Approval authority, successful dispatch, output retrieval and billing remain
  separately unverified until their real admitted upstream records exist.
- No source-data queries, GPU connections, authentication/account changes,
  prototype source edits, new licence seeds or synthetic outputs.

Verification: existing RED contracts, concurrent replay/collision, hash-chain and
ledger-failure checks, scoped entitlement positive/negative fixture tests, API
persistence and existing census regressions. Isolated fixtures must be labelled
MOCKED/TEST-ONLY, not real grants or executor proof. D01–D12 remain the acceptance
baseline; record partial cases rather than imply the whole platform is complete.