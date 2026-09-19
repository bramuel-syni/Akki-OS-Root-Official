# RB_WATCH_SIGNAL_witness_write_attempt_response

**Runbook code:** `WATCH_SIGNAL_WITNESS_WRITE_ATTEMPT` — Watch signal of kind `witness_write_attempt` reached the enforcer.
**Canon anchor:** Canon 3 §B.10 · Canon 8 §W1 (eyes-never-act) · Canon 8 §Line 31 verbatim (closed six-signal registry · `witness_write_attempt` is member 4 of 6).
**Sealed anchor:** `SeverCertaintySignalV0.signal_kind == "witness_write_attempt"` (contracts/sever_certainty_signal_v0.py · SEVER_CERTAINTY_SIGNALS closed 6-tuple).

## TRIGGER

A signal of kind `witness_write_attempt` is appended via `services.watch.sever_signals.append_sever_signal` when a caller attempts to write to the witness ledger — a store whose contract is read-only from every caller outside the Watch peer set. The witness ledger's write authority is scope-bound per Canon 8 §W11 one-task-one-identity; an attempt to write from a caller outside that identity is structural evidence of a role conflation attempt.

## EVIDENCE

- **On-record signal:** the `SeverCertaintySignalV0` record with `signal_kind = "witness_write_attempt"`, caller identity, target witness path, and the raw refused-write shape.
- **Refused-write record:** the witness ledger's write authority rejected the attempt at the trust-boundary gate; the refusal itself is a peer-not-subordinate record per Canon 8 §W12.
- **Caller identity registry:** the sealed registry of which callers hold which write scopes; an entry outside the witness-writer scope attempting to write is structural evidence.
- **Enforcer intake log:** the enforcer's record of receiving the signal.

## VERIFY

1. Confirm the `SeverCertaintySignalV0` record parses and its `signal_kind` matches `witness_write_attempt` exactly.
2. Confirm the caller identity that attempted the write does NOT hold the witness-writer scope in the sealed caller identity registry.
3. Confirm the target path was the witness ledger's write endpoint at the attempt time (a write attempt against a different ledger is a different signal class).
4. Confirm the refusal record exists at the witness ledger's refusal store and matches the attempt time.

## DECIDE

The Watch on-call lead reviews the witness-write-attempt context and decides:
- **Option A** · the caller is a legitimate service that recently had its scope amended and the amendment left the scope map inconsistent — treat as a scope-map incident and open an investigation ticket; the caller identity registry is reviewed against the amendment.
- **Option B** · the caller identity is unknown or externally exposed — treat as an intrusion candidate and open SEC-<YYYY-MM-DD-NN>; page the security-group.
- **Option C** · route to owner-desk if the write attempt targets a witness ledger whose scope contract is under active amendment.

## ACT

The Watch on-call lead is the authority for every action here. Each step is operator-issued.

1. The Watch on-call lead files the incident or investigation ticket per DECIDE.
2. If DECIDE chose Option B, the Watch on-call lead pages the security-group via the SEV-1 paging endpoint and coordinates the intrusion response with the incident lead. Every step is human-issued.
3. The Watch on-call lead does NOT modify the caller identity registry on the strength of a single signal; scope map corrections are ratified at a §3.3 seal boundary, never mid-incident by the runbook.
4. The Watch on-call lead reviews the refused-write shape to check whether the attempt was well-formed enough to have succeeded under an incorrect scope map; a well-formed refused attempt is a stronger intrusion signal than a malformed one.

## RECORD

- The signal_id + caller identity + target path + decision option + operator handle are recorded on the incident or investigation ticket.
- The refused-write shape is included on the incident ticket as evidence.
- If DECIDE chose Option C (fork), the fork banking is recorded on STATE/DECISIONS.md per §6.3.
- The caller identity registry's audit trail is annotated with the review flag.

## POSTMORTEM

Within 5 working days of incident close:
- The witness-write attempt is written up under `docs/postmortems/SEC-<YYYY-MM-DD-NN>.md` (or the investigation ticket summary for Option A).
- Root cause is classified as (a) scope-map inconsistency · (b) intrusion · (c) caller-identity drift · (d) other.
- If root cause is (a), the scope-map amendment process is reviewed and a fork is banked at STATE/DECISIONS.md if the amendment discipline is at fault.
- The runbook is reviewed for gaps; any missed distinction between root cause classes is extended.
