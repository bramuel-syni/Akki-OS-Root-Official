"""services.ledger_writer.writers — M10-W4 writer consolidation adapters.

Subpackage that carries the per-writer replay adapters folding legacy
per-service ledgers into the unified single-writer at
`services.ledger_writer.main.append_intent`. Ruled order per owner:
refusal → countersign → northena → deletion → memory.

Each writer adapter:
  * Canonicalises the legacy row shape (deterministic UTF-8 JSON).
  * Hash-anchors the legacy row via sha256_hex of the canonical bytes
    (payload_ref binding — this is the row-hash reproduction primitive).
  * Maps legacy fields to the unified 17-field `LedgerRow_v1` shape
    (zero rows lost).
  * Writes ONLY via `services.ledger_emitter.emit_intent.LedgerIntent` +
    `services.ledger_writer.main.append_intent` (the unified surface).
  * Does NOT import any legacy write function (legacy stores go
    read-only at cutover · owner mandate).

Canon 1 §62 verbatim: "no service keeps a local log constituting a
separate account of what happened." Canon 1 §71 verbatim: "When it
gains a new class of recorded event, the record gains a data class, not
a second ledger." The unified writer IS the single ledger; the legacy
per-service writers were the sibling-ledger anti-pattern the canon
forbids.
"""
