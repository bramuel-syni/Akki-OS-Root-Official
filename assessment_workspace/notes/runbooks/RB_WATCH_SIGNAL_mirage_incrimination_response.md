# RB_WATCH_SIGNAL_mirage_incrimination_response

**Runbook code:** `WATCH_SIGNAL_MIRAGE_INCRIMINATION` — Watch signal of kind `mirage_incrimination` reached the enforcer.
**Canon anchor:** Canon 3 §B.10 · Canon 8 §W1 (eyes-never-act) · Canon 8 §Line 31 verbatim (closed six-signal registry · `mirage_incrimination` is member 6 of 6).
**Sealed anchor:** `SeverCertaintySignalV0.signal_kind == "mirage_incrimination"` (contracts/sever_certainty_signal_v0.py · SEVER_CERTAINTY_SIGNALS closed 6-tuple).

## TRIGGER

A signal of kind `mirage_incrimination` is appended via `services.watch.sever_signals.append_sever_signal` when a caller acts against a Watch-placed mirage — a deliberately-shaped false artefact whose existence is known only to Watch (e.g., a mirage data row that appears to be an attractive target but does not appear in any legitimate query path). Acting against the mirage — reading it, writing to it, acknowledging it — is structural evidence of following false leads no legitimate caller could know to follow.

## EVIDENCE

- **On-record signal:** the `SeverCertaintySignalV0` record with `signal_kind = "mirage_incrimination"`, mirage id, caller identity, action shape, and time.
- **Mirage placement ledger:** Watch's internal record of the mirage's placement and its intended attractiveness profile; mirage placement is scope-bounded to Watch per Canon 8 §W10 watcher-watched-from-outside.
- **Caller path trace:** the OTel `traced_call` spans (M13-W3 wrapper) that carried the caller from its declared scope to the mirage; the trace shows the deviation from any legitimate query path.
- **Enforcer intake log:** the enforcer's record of receiving the signal.

## VERIFY

1. Confirm the `SeverCertaintySignalV0` record parses and its `signal_kind` matches `mirage_incrimination` exactly.
2. Confirm the mirage id referenced exists on the Watch mirage ledger and is not retired.
3. Confirm the caller's action shape against the mirage was a positive touch (read · write · acknowledge) — a passive query that returned the mirage in a result set without follow-up action is a separate signal class.
4. Confirm the caller's trace shows the deviation from any legitimate query path; a caller who was routed to the mirage by a legitimate mechanism is a mirage-placement bug, not a mirage_incrimination candidate.

## DECIDE

The Watch on-call lead reviews the mirage-incrimination context and decides:
- **Option A** · the caller is unauthenticated or externally exposed — treat as a live intrusion incident and open SEC-<YYYY-MM-DD-NN>; page the security-group.
- **Option B** · the caller is an authenticated internal actor whose scope does not include the mirage's location — treat as an insider-drift incident and open an investigation ticket; the caller identity registry is reviewed.
- **Option C** · route to owner-desk if the mirage-placement contract is under review; a mirage that a legitimate mechanism could reach is a placement bug and the fork banks the two options (retire the mirage · tighten the mechanism).

## ACT

The Watch on-call lead is the authority for every action here. Each step is operator-issued.

1. The Watch on-call lead files the incident or investigation ticket per DECIDE.
2. If DECIDE chose Option A, the Watch on-call lead pages the security-group via the SEV-1 paging endpoint and coordinates the intrusion response with the incident lead. Every step is human-issued.
3. The Watch on-call lead reviews the mirage placement to decide whether the mirage should be retired (a touched mirage's incrimination value is spent for the specific attacker profile that touched it).
4. The Watch on-call lead does NOT sever the caller on the strength of a single `mirage_incrimination` signal; the aggregation the enforcer performs is the sever authority, not the runbook.

## RECORD

- The signal_id + mirage id + caller identity + action shape + decision option + operator handle are recorded on the incident or investigation ticket.
- The mirage retirement decision (retire · keep · relocate) is recorded on the Watch mirage ledger with a rationale.
- If DECIDE chose Option C (fork), the fork banking is recorded on STATE/DECISIONS.md per §6.3.

## POSTMORTEM

Within 5 working days of incident close:
- The mirage-incrimination event is written up under `docs/postmortems/SEC-<YYYY-MM-DD-NN>.md` (or the investigation ticket summary for Option B).
- The attacker's or drifter's path to the mirage is enumerated and reviewed against the platform's caller-scope discipline.
- The trace evidence carried by the OTel wrapper is cross-referenced with the caller's declared scope; scope-vs-actual drift patterns are enumerated.
- The runbook is reviewed for gaps; any missed distinction between authorised passive query and unauthorised positive touch is extended.
