# RB_SEV1_CHAIN_BREAK_ledger_chain_break

**Runbook code:** `SEV1_CHAIN_BREAK` — ledger chain break paged via SEV-1 wire.
**Canon anchor:** Canon 3 §B.10 · Canon 8 §W1 (eyes-never-act) · owner run order 2026-09-18T~21:15Z verbatim.
**Sealed anchor:** `services.ledger_verifier.sev1_wire.wire_sev1_on_chain_break` (M10-W3 · Commit-A sealed at owner-verbatim run order landing).

## TRIGGER

`services.ledger_verifier.sev1_wire.wire_sev1_on_chain_break` fires when a `VerifierReceipt` presents `break_at_seq is not None`. The wire atomically emits one `Sev1Page` to the paging endpoint AND one `LedgerChainBreakSignal` to the Watch evidence store — never one without the other, never either if the chain is intact.

## EVIDENCE

- **On-record paging document:** the `Sev1Page` record persisted under the paging root; carries `tenant_id`, `break_at_seq`, `head_seq`, `head_hash`, `paged_at_iso`.
- **On-record Watch signal:** the `LedgerChainBreakSignal` record persisted under the watch root; carries the same tenant + break-seq + head fields as the page.
- **Verifier receipt (source):** the receipt whose `break_at_seq` triggered the wire; retained in the verifier's own append-only receipt store.
- **Ratchet + baseline_failures.json entries:** M10-W3 seal at Commit-A recorded verbatim.

## VERIFY

1. Confirm the `Sev1Page` and `LedgerChainBreakSignal` records both exist under their respective roots and carry identical `tenant_id` + `break_at_seq` + `head_seq` + `head_hash` + `at_iso` fields.
2. Confirm the paging endpoint's on-call rotation acknowledged receipt of the page.
3. Confirm no `Sev1Page` exists on record with `break_at_seq is None` (evidence-never-fabricated per Canon 8 §W1).
4. Confirm the `credential_handle` recorded on the wire call equals `LEDGER_VERIFIER_CRED_HANDLE` — a page raised under any shared credential is a C3 credential-separation violation and escalates to a separate incident.

## DECIDE

The on-call security lead reviews the verifier receipt against the paging window's tenant scope and decides:
- **Option A** · scope the break to the affected tenant, notify the tenant owner via the pilot-tenant contact ledger, and open a chain-restore incident.
- **Option B** · escalate to the platform-wide owner-desk on-call if the break spans more than one tenant.
- **Option C** · if the receipt's `break_at_seq` matches a known-good pre-rotation cutover point, mark the page as expected-cutover-noise and record the reconciliation in RECORD.

## ACT

The on-call security lead is the authority for every action here. This runbook is evidence-shaped; no step below is triggered as a mechanism.

1. The on-call security lead acknowledges the page via the paging endpoint console.
2. The on-call security lead notifies the tenant owner or platform owner-desk per the DECIDE choice, using the pilot-tenant contact ledger or the owner-desk paging endpoint. All notifications are operator-issued.
3. The on-call security lead files a chain-restore incident, referencing the `VerifierReceipt` id, the `Sev1Page` record id, and the `LedgerChainBreakSignal` record id.
4. The on-call security lead pauses new writes to the affected tenant's ledger until the chain-restore incident owner clears the block. The pause is a human-issued step at the write-authority console.

## RECORD

- The chain-restore incident id + `VerifierReceipt` id + `Sev1Page` record id + `LedgerChainBreakSignal` record id are recorded in the SEC incident ledger under a new SEC-<YYYY-MM-DD-NN> entry.
- The decision option (A · B · C) taken from DECIDE is recorded with the operator handle and a one-line rationale.
- The pause-of-writes window (start · end) is recorded on the tenant's operational ledger.

## POSTMORTEM

Within 5 working days of the page:
- Root cause of the chain break is written up under `docs/postmortems/SEC-<YYYY-MM-DD-NN>.md`.
- The `break_at_seq` position is compared to the tenant's write cadence to identify whether the break is upstream (write side) or downstream (verifier side).
- If the break is upstream, a fork is banked at STATE/DECISIONS.md offering options to strengthen the write-side chain integrity check; the fork routes to owner-desk per §6.3.
- If the break is downstream and the verifier receipt store shows corruption, a separate SEC incident is opened for the verifier's credential + storage.
- The runbook is reviewed for gaps and either kept as-is or extended in a follow-on additive seal.
