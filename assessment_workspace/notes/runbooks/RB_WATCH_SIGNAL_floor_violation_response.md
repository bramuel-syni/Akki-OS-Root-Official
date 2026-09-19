# RB_WATCH_SIGNAL_floor_violation_response

**Runbook code:** `WATCH_SIGNAL_FLOOR_VIOLATION` — Watch signal of kind `floor_violation` reached the enforcer.
**Canon anchor:** Canon 3 §B.10 · Canon 8 §W1 (eyes-never-act) · Canon 8 §Line 31 verbatim (closed six-signal registry · `floor_violation` is member 5 of 6) · Canon 8 §W8 (the-floor-never-learns).

## TRIGGER

A signal of kind `floor_violation` is appended via `services.watch.sever_signals.append_sever_signal` when a floor invariant of the Watch is violated. The floor is the set of invariants Watch never lets slip below — the-floor-never-learns per Canon 8 §W8 means the floor's threshold is fixed at ratification and cannot be lowered by any adaptive mechanism. A violation is structural evidence that either the sealed floor is wrong (owner-desk fork) or the platform has drifted below it (containment).

## EVIDENCE

- **On-record signal:** the `SeverCertaintySignalV0` record with `signal_kind = "floor_violation"`, the floor invariant id, the observed value, and the ratified floor threshold.
- **Ratified floor registry:** the sealed store of floor invariants and their thresholds; the threshold cited on the signal MUST match the ratified value exactly (a mismatch is a separate incident class).
- **Observed value trail:** the metric or state observation that dropped below the floor; the trail is retained in the observability plane (M13-W3 OTel wrapper `services.observability.otel_tracer.traced_call` may carry the observation as span attribute).
- **Enforcer intake log:** the enforcer's record of receiving the signal.

## VERIFY

1. Confirm the `SeverCertaintySignalV0` record parses and its `signal_kind` matches `floor_violation` exactly.
2. Confirm the floor invariant id referenced exists on the ratified floor registry and is not retired.
3. Confirm the observed value on the signal is genuinely below the ratified threshold (compute the comparison at incident review time to catch any measurement drift).
4. Confirm the observation source is on the sealed observability plane (an unofficial source is a separate signal class).

## DECIDE

The Watch on-call lead reviews the floor violation context and decides:
- **Option A** · the observed value is a transient dip below the floor and returned above the threshold within a bounded window — treat as a transient investigation ticket, review the observability plane's window.
- **Option B** · the observed value is sustained below the floor — treat as a live incident and open SEC-<YYYY-MM-DD-NN>; page the security-group; pause new writes to the affected surface until the floor is restored.
- **Option C** · route to owner-desk if the sealed floor threshold itself is suspected wrong; changing a floor is a canon-vs-lower-layer decision per §6.4 rule 3 and MUST go to owner-desk with a fork banked.

## ACT

The Watch on-call lead is the authority for every action here. Each step is operator-issued.

1. The Watch on-call lead files the incident or investigation ticket per DECIDE.
2. If DECIDE chose Option B, the Watch on-call lead pauses new writes to the affected surface via the write-authority console (the pause is human-issued at the console; the runbook does not run the pause).
3. The Watch on-call lead does NOT lower the floor threshold on the strength of any signal; the floor never learns per Canon 8 §W8 — threshold changes require an owner-desk ceremony.
4. The Watch on-call lead reviews the observed value trail against the ratified threshold and files the delta on the incident ticket as evidence of the drift magnitude.

## RECORD

- The signal_id + floor invariant id + observed value + ratified threshold + decision option + operator handle are recorded on the incident or investigation ticket.
- The pause-of-writes window (if any) is recorded on the affected surface's operational ledger with start · end · operator handle.
- If DECIDE chose Option C (fork), the fork banking is recorded on STATE/DECISIONS.md per §6.3 and routed to owner-desk.

## POSTMORTEM

Within 5 working days of incident close:
- The floor violation is written up under `docs/postmortems/SEC-<YYYY-MM-DD-NN>.md` (or the investigation ticket summary for Option A).
- The elapsed time from violation onset to violation-cleared is measured; sustained violations beyond a bounded window are separately reported to owner-desk regardless of the runbook's DECIDE choice.
- If the sealed floor threshold is suspected wrong, an owner-desk fork is banked at STATE/DECISIONS.md; the fork is never resolved by the runbook.
- The runbook is reviewed for gaps; any missed transient-vs-sustained distinction is extended.
