# RB_WATCH_SIGNAL_attestation_failure_response

**Runbook code:** `WATCH_SIGNAL_ATTESTATION_FAILURE` — Watch signal of kind `attestation_failure` reached the enforcer.
**Canon anchor:** Canon 3 §B.10 · Canon 8 §W1 (eyes-never-act) · Canon 8 §Line 31 verbatim (closed six-signal registry · `attestation_failure` is member 2 of 6).
**Sealed anchor:** `SeverCertaintySignalV0.signal_kind == "attestation_failure"` (contracts/sever_certainty_signal_v0.py · SEVER_CERTAINTY_SIGNALS closed 6-tuple).

## TRIGGER

A signal of kind `attestation_failure` is appended via `services.watch.sever_signals.append_sever_signal` when a service that should have produced a valid attestation (signed structural claim about its own state) produces one that fails signature verification or is missing. The signature is the guard per Canon 8 §Line 31: absence or invalidity of a required attestation is structural evidence, not curated content.

## EVIDENCE

- **On-record signal:** the `SeverCertaintySignalV0` record with `signal_kind = "attestation_failure"`, tenant + service scope, and the raw attestation fact (signature verification result · missing-attestation flag).
- **Expected-attestation source:** the sealed registry of services required to attest (Watch keeps this list; it does not accept an attestation from a service outside the list per Canon 8 §W9 no-actor-enters-undeclared).
- **Rotation lineage cross-reference:** if the attestation failure is signature-related, the KMS `KeyLineageRecord` for the attesting service's tenant at the attestation time is cross-referenced.
- **Enforcer intake log:** the enforcer's record of receiving the signal (evidence-then-decide per §B.10).

## VERIFY

1. Confirm the `SeverCertaintySignalV0` record parses and its `signal_kind` matches `attestation_failure` exactly.
2. Confirm the attesting service was on the sealed expected-attestation registry at the failure time.
3. Confirm the signature verification result is reproducible: given the recorded signature + expected public key + attested payload, the verify call fails deterministically.
4. Confirm the KMS `KeyLineageRecord` for the service's tenant at attestation time does not show a mid-attestation rotation (an attestation that spans a rotation is a separate incident class).

## DECIDE

The Watch on-call lead reviews the attestation failure context and decides:
- **Option A** · the failure is corroborated by another sever-certainty signal within the same tenant + service scope inside a 60-second window — treat as a live incident and open SEC-<YYYY-MM-DD-NN>, page the security-group.
- **Option B** · the failure is isolated and matches a known-benign class (e.g., clock skew tolerated by the attestation contract) — file a low-severity investigation ticket and monitor for repeat occurrences.
- **Option C** · route to owner-desk if the attestation failure appears against a service whose expected-attestation contract has been amended recently but the amendment is not yet ratified; a partial contract change is a fork banked with two options.

## ACT

The Watch on-call lead is the authority for every action here. Each step is operator-issued.

1. The Watch on-call lead files the incident or investigation ticket per DECIDE.
2. If DECIDE chose Option A, the Watch on-call lead pages the security-group via the SEV-1 paging endpoint (the same wire M10-W3 sealed for chain break) and coordinates containment scope with the incident lead. Every step is human-issued.
3. The Watch on-call lead marks the attesting service as under review on the operational ledger; new attestations from that service are queued but not admitted until the incident lead clears the review flag.
4. The Watch on-call lead does NOT sever the service on the strength of a single `attestation_failure` signal; the aggregation the enforcer performs is the sever authority, not the runbook.

## RECORD

- The signal_id + service scope + tenant scope + decision option + operator handle are recorded on the incident or investigation ticket.
- The review flag on the attesting service is recorded on the operational ledger with a rationale.
- If DECIDE chose Option C (fork), the fork banking is recorded on STATE/DECISIONS.md per §6.3.
- The pilot-tenant contact ledger is updated so the tenant owner learns of the review flag from the platform.

## POSTMORTEM

Within 5 working days of incident close:
- The attestation failure is written up under `docs/postmortems/SEC-<YYYY-MM-DD-NN>.md`.
- Root cause is classified as (a) key drift · (b) contract drift · (c) service compromise · (d) clock/skew · (e) other.
- If root cause is (a), the KMS on-demand rotation runbook is cross-referenced; if the runbook was not invoked at the attestation time, the gap is written up.
- The runbook is reviewed against the failure's evidence set; gaps that would have distinguished the root cause classes earlier are extended in a follow-on additive seal.
