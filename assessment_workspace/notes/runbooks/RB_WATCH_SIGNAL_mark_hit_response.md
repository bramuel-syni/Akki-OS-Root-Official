# RB_WATCH_SIGNAL_mark_hit_response

**Runbook code:** `WATCH_SIGNAL_MARK_HIT` — Watch signal of kind `mark_hit` reached the enforcer.
**Canon anchor:** Canon 3 §B.10 · Canon 8 §W1 (eyes-never-act) · Canon 8 §Line 31 verbatim (closed six-signal registry · `mark_hit` is member 3 of 6).
**Sealed anchor:** `SeverCertaintySignalV0.signal_kind == "mark_hit"` (contracts/sever_certainty_signal_v0.py · SEVER_CERTAINTY_SIGNALS closed 6-tuple).

## TRIGGER

A signal of kind `mark_hit` is appended via `services.watch.sever_signals.append_sever_signal` when an outsider touches a Watch-placed mark — a marker Watch has embedded in a location or artefact only Watch knows to be a marker. Unlike a canary (a tripwire object whose whole purpose is to be touched), a mark is an internal identifier whose presence is not disclosed; touching it is structural evidence of unauthorised inspection.

## EVIDENCE

- **On-record signal:** the `SeverCertaintySignalV0` record with `signal_kind = "mark_hit"`, mark id, tenant scope, and the touch context (which caller · which resource · at what time).
- **Mark placement ledger:** Watch's internal record of the mark's placement — the placement itself is scope-bounded to Watch trust boundary per Canon 8 §W10 watcher-watched-from-outside.
- **Caller context:** the caller identity that touched the mark; cross-referenced with the caller's declared scope per Canon 8 §W9 no-actor-enters-undeclared.
- **Enforcer intake log:** the enforcer's record of receiving the signal.

## VERIFY

1. Confirm the `SeverCertaintySignalV0` record parses and its `signal_kind` matches `mark_hit` exactly.
2. Confirm the mark id referenced exists on the Watch mark ledger and is not retired.
3. Confirm the caller identity that touched the mark was on-record at the touch time and was operating within its declared scope.
4. Confirm the mark is not itself a canary (canaries are separate; a canary's touch fires `canary_touch`, not `mark_hit`).

## DECIDE

The Watch on-call lead reviews the mark hit context and decides:
- **Option A** · the caller had no declared read-right on the resource that carried the mark — treat as a scope violation and open SEC-<YYYY-MM-DD-NN>; page the security-group.
- **Option B** · the caller had read-right but the mark's location was outside the declared purpose of the read — treat as a purpose-drift incident and open an investigation ticket.
- **Option C** · route to owner-desk if the mark's placement is under active review or the caller is a Watch-tier service whose mark-hit would indicate a Watch internal drift.

## ACT

The Watch on-call lead is the authority for every action here. Each step is operator-issued.

1. The Watch on-call lead files the incident or investigation ticket per DECIDE.
2. If DECIDE chose Option A, the Watch on-call lead notifies the tenant owner and coordinates with the incident lead on the caller's blast radius. Every step is operator-issued.
3. The Watch on-call lead reviews the mark placement to decide whether the mark should be retired (a hit mark's signalling value is spent).
4. The Watch on-call lead does NOT sever the caller on the strength of a single `mark_hit` signal; enforcement of a sever is the enforcer's authority under aggregation, not the runbook.

## RECORD

- The signal_id + mark id + caller identity + tenant scope + decision option + operator handle are recorded on the incident or investigation ticket.
- The mark retirement decision (retire · keep · relocate) is recorded on the Watch mark ledger with a rationale.
- If DECIDE chose Option C (fork), the fork banking is recorded on STATE/DECISIONS.md per §6.3.

## POSTMORTEM

Within 5 working days of incident close:
- The mark hit is written up in the Watch signal log summary.
- The caller's declared scope is reviewed against the mark's location; scope-drift patterns are enumerated on the tenant's operational ledger.
- If the mark placement disclosure gap is what enabled the hit, a fork is banked at STATE/DECISIONS.md offering options to tighten mark-placement scope discipline.
- The runbook is reviewed for gaps; any missed distinction between mark_hit and mark-adjacent-noise is extended.
