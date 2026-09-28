"""Secret-hygiene guards.

Runtime invariants that refuse to let credential material round-trip
into any log/receipt/print/error message.  Landed as its own hygiene/
hardening wave (W-HYGIENE-HF-TOKEN-GUARD, 2026-09-14) against the
same-class transcript-leak recurrence enumerated in
`notes/SEC_INCIDENTS_20260914.md`.
"""
