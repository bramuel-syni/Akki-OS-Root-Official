"""services.mkondo · Mkondo registry package.

Canon 15 §33 · CA1-009 · Canon 8 §W11 (one-task-one-identity) · Canon 1 §62
(single-writer ledger).

Structural role separation: this package admits and persists hand-offs.
It does NOT sign hand-offs (signing stays at M14-W4 · Watch signature
primitive is the sole signer).

SO §3.8 thin-kernel additive-only: this package extends the estate via
a new module surface; sealed pre-M14 modules
(`contracts.handoff_contract`, `services.handoff.contracts`,
`services.ledger_emitter.emit_intent`) are consumed, not edited.
"""
