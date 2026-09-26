# W0/W1 first autonomous slice — control-record authority, 2026-09-26

## Authorization
Owner: “This works, go autonomous, ill be stepping away and may not be in a position to respond. is ther a decion youd need from me except for the one you have listed above?”

This authorizes execution of the reviewed programme, not answers to held policy questions or renewed GPU access. Continue independent work; record newly discovered authority conflicts instead of guessing. Existing plan-only entries remain historical.

## Exact scope / six-field task contract

1. **Denominator:** two prospective control-event producers: Northena DAP held commissioning (`services/northena/portal_work.py::submit`) and skill-executor refusal (`services/portal_operational/skill_query.py::refuse_unadmitted`); two read-consumer families: request/work projection and entitlement projection. These are NOT all platform writers. Freeze their source hashes with acceptance evidence before modification.
2. **Procedure:** retain existing authenticated account/tenant resolution; bind its request-lifetime scope into a frozen, context-local carrier without editing sealed principal modules. Derive prospective writer actor from propagated context, never producer arguments. Require scope agreement, an active request lifetime, and matching payload attribution. Compose the existing canonical emitter/writer and verifier; reject broken chain/payload/shape before returning a successful projection or writing after an invalid prefix. Acknowledged records remain append-only. Separate command collision from integrity failure.
3. **Artifact:** additive guarded adapter/context carrier and producer/consumer imports; a verification JSON with exactly one member row for each of the four IDs in the pre-change snapshot, fields `member_id`, `outcome` (processed/refused/unmeasured), `reason`, `evidence_refs`; summary counts derived by grouping those outcomes. Include source-linked evidence, protected core-file hashes and unchanged original prototype files. No new endpoint, principal admission, credential, licence, price, operation approval or executor.
4. **Acceptance script:** `backend/tests/portal_operational/test_w1_control_record_contract_red.py` written and executed RED before runtime edits, with scoped supplemental checks where needed. First denominator check verifies the banked four-member source snapshot. Script hashes/results banked. Shared workspace access DOES NOT establish EX4 protected write isolation; this limitation remains open. Tests use synthetic local records for faults; live tests may commission held requests with existing credentials. No source/model/GPU calls or fixture grants in the real DB.
5. **Shortcut list:** (a) adding a wrapper but leaving producers on raw writer — detector: production-import assertions; (b) checking row hash but ignoring broken chain — detector: legacy counterexample plus guarded-prefix tests; (c) stamping an actor string without active propagation — detector: missing/mismatched/copied-expired context tests; (d) weakening sealed carriers or redesigning prototypes — detector: byte pins. Failure cases include corrupted/ill-formed/incomplete chains, command conflict, cancellation/concurrency and Ledger outage; never delete history or call an unbanked failure a receipt.
6. **Evidence:** pre-change member/source hashes, RED output and pinned test script, post-change member artifact/hash, repeated GREEN results, source/byte comparisons and actual API/browser receipts, plus explicitly bounded re-performance evidence. No EX4/R37 independence claim. Completion is limited to these two producers/two read families, not owner admission, full S32, global writer enforcement, independent witness/head rollback protection, all 509 semantic links or successful execution.

EX discipline used prospectively; adoption/status and EX4/R37 independent isolation remain held as listed. A checking process in this workspace is not claimed as a protected independent executor.

## Source/authority trace for this slice

- Principal specification B22/B23/B24: PRIN-11/12/13 require context-based attribution, absent-context refusal and immutable propagation; prior entries are not retroactively changed. The source's draft status is reconciled to the banked principal-wave seal in `STATE/DECISIONS.md:22741–22759` and the existing sealed propagation adapter. No new ratification inferred from tests.
- Canon 3 Governance Engines §6.2–6.3 (lines57–59): immutable freeze and idempotency prevent changed intent or duplicate commissioning; §9.3 (line92) requires append-only corrections, never destructive edits.
- S-6 requires authoritative evidence before the next gate. The canonical 17-field schema and existing verifier are reused; in-process verification here is not the independently placed verifier promised by its wider architecture.
- Existing D01/D02/D03/D10/D12 define identity/scoped request replay, authoritative failure and historical projections. This increment does not upgrade D04–D07's execution/approval/result claims.
- Namespace correction: Ledger code comments containing `BR-13/BR-14/BR-15` are not evidence for the separately named Governance Architecture rows BR-13.1 (Tier-3 eligibility), BR-14.1 (rights information point), BR-15.1 (agent-deploy outcomes). Use exact document-qualified identifiers, not number matching.

## Acceptance cases (tests first)

| ID | Required outcome |
|---|---|
| C01 | No trusted request context: prospective write refuses before DB access; no default actor |
| C02 | Caller actor argument or payload actor/tenant mismatch cannot override propagated principal/tenant |
| C03 | Same-scope nested context is safe; substitution of principal or tenant refuses; outer context survives |
| C04 | Two concurrent requests retain separate scopes; exceptions/cancellation clear context; a copied child context cannot write after request exit |
| C05 | Existing sealed context/adapter, 17-field schema, emitter/writer kernel and verifier stay byte-identical |
| C06 | Legitimate held request persists/replays; changed-body key conflict remains409; requests/work show same identity/history |
| C07 | Valid chain with unrelated tenant-local event types can be filtered without breaking sequence verification; no other tenant is returned |
| C08 | Missing/interleaved sequence, invalid genesis/link, tenant mismatch, malformed row or payload corruption fail closed even when selected individual row hashes look valid |
| C09 | A malformed/corrupted prefix blocks a new prospective append, not only its read projection |
| C10 | New event is detached from mutable caller payload; command identity is payload-hash-bound; a reused command cannot silently switch actor/run/event/intent |
| C11 | Real Mongo idempotent concurrency remains one event per command and one unbroken tenant chain; insert failure never acknowledges success |
| C12 | Existing anonymous/analyst/unknown skill and stop/retry/retrieval refusals remain; no new approval/licence/execution and no prototype changes |

## Architectural limits kept explicit

The trusted request carrier composes existing approved held-work membership. It is not a durable organisation-admission ceremony or a credential cache. Python context carriers are not a sandbox against arbitrary in-process code. All legacy writers and direct module invocation beyond the enumerated producers remain wider W1 work; an AST import invariant protects the migrated production call sites, not a universal network boundary.

Full-prefix verification is deliberately uncached for this bounded control-plane slice. Throughput/scaling is unmeasured; no CC floor claim. A self-consistent truncated/replaced chain needs an independent trusted head/witness to detect, which remains W6b. No record migration or purge is authorized.