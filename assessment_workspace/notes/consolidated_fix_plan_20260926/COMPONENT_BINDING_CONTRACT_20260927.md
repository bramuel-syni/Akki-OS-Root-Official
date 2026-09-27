# Execution component binding — next architecture slice, 2026-09-27

Owner: continue under the confirmed architecture-first/autonomous programme.
No new policy decision, admission, provider credentials or GPU access is implied.

## Four-member denominator
1. Principal/licence/catalogue authority adapter.
2. Canonical Mtafiti artifact registration adapter.
3. Actual-usage handoff to the existing entitlement read consumer.
4. Trusted server-side composition and public held-boundary regression.

## Existing components and concrete changes

- Fix `ExistingAuthorityBoundary`: `read_view` returns `LicencePortalView`, not a
  dictionary with `licence_admitted`. Use the actual typed status/licence fields.
- Resolve the actual propagated principal through the sealed principal store;
  require active parent organisation and agreement with the licence. Compose the
  existing entitlement `resolve` pure function for model-bound operations.
- Independent operation approval remains a server-owned decision producer port;
  a licence is not approval. Its typed decision must bind the exact request, phase,
  engine, scope, expiry and terms. No client-supplied actor, approval or model binding.
- Snapshot commercial terms/catalogue BEFORE durable dispatch; retain them for
  measured history. Current suspension/withdrawal still gates release/retrieval.
  Reseller R24 stays held; synthetic historical pricing tests do not ratify it.
- Independent artifact inspector supplies typed manifest/custody/owner evidence.
  Compose existing `AssetRegistryRecord`, deterministic canonical receipt ID and
  `write_asset_record`; do not create another registry writer/store or infer custody.
  Persist the exact registration envelope on the SAME Ledger before updating the
  canonical registry projection. Immutable content+metadata-version refs prevent
  overwriting a prior registered version. Rehydrate after commit/projection failure.
- Publish model usage as actual `MeteredEvent` plus captured catalogue snapshot,
  organisation and execution receipt reference through the canonical Ledger. Stable
  command IDs prevent duplicate debits. Unknown usage is not zero; MOCKED observations
  never become production balance entries. Preserve AU-3(b)=false. Non-model source
  usage remains explicit execution consumption, not fabricated model pricing/credits.
- Add a frozen server-owned binding bundle consumed by composition/app state. No
  HTTP registration/approval endpoint and no production successful test doubles.

## Acceptance before implementation

Use REAL coordinator/journal, native entitlement projection/resolver, canonical
registry writer and native MeteredEvent consumer against isolated FAKE storage.
Principal/approval/inspector/worker observations are synthetic test fixtures, not
live authority. Where measured-shaped fixtures are required to test production
refusal/consumption code, the test artifact must still label their source MOCKED.

Required cases:
- Typed unresolved view returns a held reason, not TypeError. Missing/mismatched/
  suspended principal/org/licence refuses; individual/agent parent checked outside
  sealed pure resolver. Local/Your Keys not subjected to reseller-only holds.
- Exact operation decision and declared catalogue required for model operations;
  malicious/widened/expired/terms-mismatched decisions cannot dispatch.
- Dispatch snapshot immutable; rerating afterwards cannot reprice prior usage.
- Registry commit failure leaves no canonical in-memory publication; projection
  failure after commit replays and restores without a second authoritative record.
- Manifest owner/custody/class/identity/evidence mode checked; no class/custody
  inferred from file type or completion flag. Forbidden and mismatched entries refuse.
- Raw usage is receipted before bridge; bridge failure holds publication and retry
  cannot duplicate a debit. Multiple units, invalid/unknown quantities, missing price,
  conflicting command and MOCKED observations are safely accounted for/refused.
- Current rights/registry validation at retrieval; canonical field contracts and
  byte-pinned principal/registry/entitlement kernels remain unchanged.
- Server bundle may be supplied only by trusted app composition; request body/header
  cannot install a decision producer/executor. Default application remains held.
- Existing execution_spine and portal suites remain green; original UI untouched.

## Six-field discipline / closure boundary

Denominator above; procedure is native component composition with all refusal/race/
replay boundaries; artifact is four-member acceptance/evidence table with native vs
synthetic labels; RED-first script pinned; shortcuts detected by field/type and
commit-order tests; evidence includes GREEN regressions and protected file hashes.
EX4/R37 isolation not asserted from a shared workspace. No all-platform/live-element
claim, no source/model/SSH activity, no fees/admissions fabricated. Full replica
failover, seat/reservation concurrency, rollover and independent root producers
remain wider programme work. No benchmark/optimal-performance claim is inferred.