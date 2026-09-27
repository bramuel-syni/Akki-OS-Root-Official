# Native execution component binding — verified 2026-09-27

## Bounded architecture result

The execution spine now composes native Akki principal/licence/catalogue resolution,
canonical Mtafiti registration, and actual-usage publication to the existing
entitlement consumer. These are implementations, not success-returning placeholders.
Independent operation decisions, remote workers and independent artifact inspection
remain server-owned provider interfaces; none has been faked into production.

| Member | Native implementation / evidence | Remaining boundary |
|---|---|---|
| Authority adapter | Propagated context → principal/parent organisation → typed LicencePortalView → existing entitlement resolver → exact operation decision and immutable commercial snapshot | Actual principal/admission/approval producers must supply real records; a licence alone never approves work |
| Registry adapter | Typed inspection → immutable content+metadata version → durable registration envelope → existing canonical writer; replay/recovery and current retrieval checks | Independent byte/rights/custody inspection is an upstream port, not performed on estate bytes by E1 |
| Usage handoff | Canonical raw-meter/dispatch binding → native MeteredEvent and captured catalogue rate → native entitlement projection; stable replay IDs | No invoice/payment activation; non-model consumption is not assigned an invented model price |
| Server composition | Frozen typed binding bundle, exact kind/engine matching, server app-state injection, default held operation | No public adapter/admission registration and no real provider bindings activated |

### Implementation files

New under the vendored backend:
- `services/northena/execution_component_models.py`
- `services/northena/execution_authority.py`
- `services/northena/execution_usage.py`
- `services/northena/execution_bindings.py`
- `services/mtafiti/execution_record_models.py`
- `services/mtafiti/execution_registry.py`

Existing unsealed composition, coordinator/completion/journal, portal execution
route and entitlement projection were connected to these adapters. The old
`view['licence_admitted']` mismatch was removed: actual typed fields are used.
The sealed principal, licence/catalogue, canonical registry/Ledger and prototype
files were not edited. No new dependencies, credentials, real admissions or keys.

## Important semantics

- Current principal/org/licence/operation scope and expiry checked; unknown is held.
- Snapshot catalogue/terms before dispatch; changed terms before the effect refuse.
  Historical usage uses its captured rate, not whatever is listed at read time.
- Canonical registration occurs only AFTER its authoritative Ledger envelope. If
  cache projection fails, the persisted version can be rehydrated. No history deletion
  or new registry collection/writer. Retrieval checks the current inspector again.
- `record.freshness_stamp` identifies the asset version, not the latest inspection
  invocation time. An inspection receipt may change while the version is unchanged;
  changed owner/custody/identity/metadata is not silently substituted into an old version.
- Metered quantity must be finite and representable by the existing MeteredEvent;
  every unit is checked before financial publication. Unknown usage is not zero.
  AU-3(b) remains false. MOCKED consumption is refused by the publisher and explicitly
  unverified usage cannot silently become an entitlement debit.
- Source non-model usage gets an explicit consumption-only handoff: no fabricated
  model-credit entry and no assertion that all non-model services are free.
- ENT-22 is preserved: **tokens × per-token credit_rate**. The synthetic historical
  test uses `1000 × 0.002 = 2`; changing the current rate to0.02 does not reprice it.
  No “per1000” pricing field or changed arithmetic was added; reseller R24 stays held.

## Verified evidence

**143 passed / 0 failed / 0 skipped** across execution_components, execution_spine
and portal_operational. JUnit: `test_reports/pytest/pytest_iteration31_components_spine_portal.xml`.

Three new native positive integration tests specifically exercise:
1. REAL Coordinator, LedgerJournal, ComponentAuthority/native entitlement reader and
   resolver, CanonicalRegistry/native writer, LedgerUsagePublisher and EngineAdapter
   in one complete source-kind control flow, including rights-checked retrieval.
2. Registry commit failure before publication, projection failure after commit,
   reconstruction/retry without another registry envelope, and changed owner,
   custody or artifact refusal.
3. Native historical usage projection, idempotent debit, preserved dispatch-time
   pricing after rerating, MOCKED usage refusal, and handoff-failure recovery without
   duplicate financial entries. Actual ComponentAuthority still rejects reseller dispatch.

The earlier140-pass run covered regressions and fixture migrations but did NOT yet
contain these three native integration tests; it is not presented as the same proof.

All positive upstream principal/licence/decision/worker/inspection inputs here are
**SYNTHETIC / MOCKED**, with **FAKE isolated storage**. Some fixtures use measured-shaped
schema values to exercise strict production acceptance; their provenance remains
MOCKED and **live element verification is false**. No grants, model charges, approvals
or source results were seeded into production. Actual API regression creates only
legitimate HELD control requests. No source/GPU/SSH/model/provider operation ran.

Main hash recheck verified16 unchanged protected/reference files, including native
schemas/kernels and literal prototypes. Iteration28's manifest also included four
intentionally mutable integration files; their changes are recorded as authorized,
not misrepresented as protected-file preservation. See the final evidence JSON.

Two old test fixtures were migrated, not the runtime relaxed: an obsolete fake dict
was replaced by typed licence/context data; a bare object was replaced by a request
with app.state for the existing foreign-principal404 test. Assertions retained their
original admission/ownership protection. Original failing reports remain banked.

## Next / nonclaims

Next: bind actual admitted operation-decision and worker/inspection producers, expand
typed skill/training/evaluation compositions with these native adapters, and continue
custody/handoff, DQ and commercial architectural closure. Keep missing elements
separate from assembly/testing; no additional owner decision is needed for independent
already-authoritative work.

Production still has no successful external bindings: execution requests remain
truthfully held; callable query remains refused without admitted execution. This
does not close T14, full principal/owner admission, all Mtafiti consumers, pooled
capacity/seat/period concurrency, all DQ, W6 witnessing, full Mongo failover or actual
source/model/hardware performance. Full-prefix verification remains uncached; no
best-throughput/SLO claim is inferred from pytest time. No full-platform percentage.

Later enhancement: expose these same receipt-linked unmet prerequisites in the
existing request drawer without changing its owner prototype.