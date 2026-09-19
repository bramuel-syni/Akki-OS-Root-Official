# RB_WATCH_SIGNAL_canary_touch_response

**Runbook code:** `WATCH_SIGNAL_CANARY_TOUCH` — Watch signal of kind `canary_touch` reached the enforcer.
**Canon anchor:** Canon 3 §B.10 · Canon 8 §W1 (eyes-never-act) · Canon 8 §Line 31 verbatim (closed six-signal registry · `canary_touch` is member 1 of 6).
**Sealed anchor:** `SeverCertaintySignalV0.signal_kind == "canary_touch"` (contracts/sever_certainty_signal_v0.py · SEVER_CERTAINTY_SIGNALS closed 6-tuple).

## TRIGGER

A signal of kind `canary_touch` (an outsider touched a placed canary — an object designed only for tripwire purposes) is appended via `services.watch.sever_signals.append_sever_signal`. The Watch's sever-certainty registry admits this signal because it is one of the six kinds that no outsider can fabricate at will (a canary's placement is a Watch internal fact, so a touch on it is structural evidence, not curated).

## EVIDENCE

- **On-record signal:** the `SeverCertaintySignalV0` record in the closed-six registry, carrying `signal_id`, `signal_kind = "canary_touch"`, tenant scope, and the raw touch fact.
- **Canary placement ledger:** the internal Watch record of when and where the canary was placed; the touch's spatial + temporal coincidence with a placed canary is what makes this evidence structural.
- **Enforcer's Watch-signal intake log:** the enforcer records receipt of the signal without acting on it directly (evidence-then-decide per §B.10).
- **Correlated timeline:** any other signals of the six-kind grammar within the same tenant scope in a bounded window before or after the canary touch.

## VERIFY

1. Confirm the `SeverCertaintySignalV0` record parses and its `signal_kind` field matches the closed-registry member `canary_touch` exactly.
2. Confirm the canary placement referenced by the signal exists on the Watch canary ledger and is not itself retired.
3. Confirm the signal_id is write-once — a duplicate raises `WriteOnceViolation` at the store level; if any duplicate is on record, the incident escalates.
4. Confirm the signal reached the enforcer's intake log (Watch is peer-not-subordinate per Canon 8 §W12 — the enforcer receives the signal as data, never as command).

## DECIDE

The Watch on-call lead reviews the canary touch context and decides:
- **Option A** · the canary touch is corroborated by a mark_hit or witness_write_attempt signal within the same tenant scope inside a 60-second window — treat as a live incident and open SEC-<YYYY-MM-DD-NN>.
- **Option B** · the canary touch is isolated (no correlated signal within 60 seconds) — treat as a probe candidate and open a low-severity investigation ticket.
- **Option C** · route to owner-desk if the canary touch aligns with a scheduled test or drill; test-noise on a canary is a fork banked because it exposes canary placement to the drill scope.

## ACT

The Watch on-call lead is the authority for every action here. Each step is operator-issued.

1. The Watch on-call lead files the incident or investigation ticket per DECIDE.
2. If DECIDE chose Option A, the Watch on-call lead notifies the tenant owner via the pilot-tenant contact ledger and coordinates with the incident lead on containment scope. Every notification is human-issued.
3. The Watch on-call lead does NOT trigger a sever action on the strength of a single `canary_touch` signal — Canon 8 §W1 discipline; a sever action requires the aggregation the enforcer performs when the closed-six registry accumulates evidence of a certain shape.
4. The Watch on-call lead reviews the canary's placement to decide whether the canary should be retired (a touched canary loses its tripwire value); retirement is filed at the Watch canary ledger by the operator, not by the sever_signals module.

## RECORD

- The `SeverCertaintySignalV0.signal_id` + tenant_id + placement id + decision option (A · B · C) + operator handle are recorded on the incident or investigation ticket.
- The canary retirement decision (retire · keep · replace) is recorded on the Watch canary ledger with a rationale.
- If DECIDE chose Option C (fork), the fork banking is recorded on STATE/DECISIONS.md per §6.3.

## POSTMORTEM

Within 5 working days of incident close (or 30 days for low-severity investigation tickets):
- The canary touch is written up in the Watch signal log summary.
- If the touch was a real probe, the probe's attack surface is enumerated and reviewed against the platform's tenant isolation posture.
- If the touch was drill noise, the drill scope is reviewed against Watch canary placement disclosure; a follow-on additive seal may extend the drill isolation.
- The runbook is reviewed for gaps; any missed correlation window is extended.
