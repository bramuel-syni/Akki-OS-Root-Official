# Non-GPU skill queries and custody delivery — 2026-09-27

## Scope
User: “Proceed with everything else except GPU”, then “Proceed”. No GPU/SSH
connection, credential change, runtime rotation or workload was performed. GPU
connector test files were excluded from this non-GPU regression; both existing
authorisation-gated custody/production drills remain skipped. Frontend prototype,
styles, frozen Canon interfaces and existing login/accounts remain unchanged.

## Native query flow implemented
`services/portal_operational/query_{intents,plans,evidence,execution}.py` and
`routers/skill_queries.py` extend the existing callable-skill gates, not replace
them. The original scope/Keygrant/owner/floor/crossing gate runs first.

- Idempotent, tenant/principal/skill-bound question intents on the existing Ledger.
  Only the question hash and exact provisioning hash persist; no raw questions
  or generated answer/source bytes are persisted or forwarded by this flow.
- Existing signed native plan must match the exact question, provisioning, corpus,
  caller, engine, floor, scope and deadline through the existing skill_request
  builder. The owning estate must already hold the actual query/corpus; this
  workspace does not create data handles or generate an answer locally.
- Execution uses the existing coordinator and approval/limit/handoff gates.
  Ready requires signed worker answer metadata plus independently signed anchors,
  matching registered answer hash/class, context-loss disclosure and floor.
- A genuine native OUT_OF_SCOPE refusal must be signed by the admitted worker and
  cite this intent. Missing executor/approval is a HELD state, not a fabricated
  out-of-scope proof. Contradictory answer/refusal outcomes are held.
- Status/replay checks current provisioning. An older ready view cannot expose
  artifact references after a different corpus/provisioning or lost native access.
  HTTP release rechecks the original skill gate after awaiting native operations.
- Existing `/api/callable_skill/{id}/query` uses this flow only with a configured
  native runtime and explicit Idempotency-Key. Unconfigured legacy route remains
  a receipted409, never fabricated answer text.

New APIs: POST `/api/callable_skill/{id}/query-intents`; GET
`/.../queries/{query_id}`; POST `.../advance`; POST `.../delivery`; GET
`.../deliveries/{delivery_id}`.

## Native custody handoff implemented
`services/custody_delivery` and `routers/custody_delivery.py` implement a
metadata-only native port. NativeRuntime optionally binds an existing custody
provider through the SAME admitted receipt source; no storage client, identity
store, endpoint, credential or provider is fabricated.

- Before a grant: current result/rights/registry validation, frozen descriptor,
  idempotent intent and single dispatch. Concurrency/uncertainty reconciles the
  same delivery ID through status; it does not redispatch blindly.
- Provider supplies an authenticated signed grant and opaque capability. Exact
  approved HTTPS origin, recipient/tenant/request/artifact/hash/size, explicit
  expiry and authority window are checked. No public/static S3 fallback.
- Capability URLs exist only transiently and in an explicit authenticated
  no-store/no-referrer response. Never stored in Ledger/history or logged. The
  workspace never fetches, streams or redirects source bytes; actual retrieval
  must be browser/client-to-admitted-custody service.
- Issuing a link does NOT mark delivery verified. Only the signed terminal
  completion with exact measured bytes/hash and legal redemption chronology does.
  The native gateway must enforce current rights at redemption; none is deployed
  by this change. Tests cannot prove that unconfigured service's enforcement.
- Expired URLs cannot be issued again. A current signed completion can prove an
  earlier legal redemption after link expiry; fresh rights still gate reads.
  Modified provider evidence, missing signature, bad recipient/count/hash/origin,
  expiry during final rights check and withdrawn grants fail closed.
- Recorded handoff/grant/uncertainty/completion joins existing DAP/OS work history
  through canonical receipt references, with no URL exposure. Result-level
  delivery_verified requires coverage of ALL expected artifacts; partial delivery
  remains explicitly partial. Existing result-response allowlist is unchanged.

Source APIs: POST `/api/portal/requests/{id}/delivery`; GET
`/api/portal/requests/{id}/deliveries/{delivery_id}`. The owned DAP request and
frozen native execution descriptor are both required. Work history is already
rendered by the existing prototype; no new panels/layout/buttons were added.

## Test evidence and corrections
- Independent report48 added18 signed/fake-provider cases and confirmed original
  protected contracts. Its first broad run accidentally skipped15 live API tests
  because the preview environment variable wasn't exported. It is NOT the final
  regression result; main reran with current frontend.env URL exported.
- Main added expiry, capability privacy, race, wrong-recipient/count/hash, current
  provisioning, multi-session isolation, HTTP and work-history/partial-result
  tests. The final suite is `test_reports/pytest/non_gpu_verified.{xml,log}`.
- FINAL: **602 non-GPU tests passed,2 original explicitly gated custody drills
  skipped,0 failures/errors**,64.635seconds.13 unchanged GPU connector tests were
  excluded because this batch explicitly excludes GPU work.
- All7 frontend tests pass; unchanged external desktop shell smoke passed. Final
  desktop1920×800/mobile390×844 verification used an existing1083-character
  objective among971 request records; no horizontal overflow at either width.
  Scoped Python lint passes. Only pre-existing third-party deprecation warnings.
- One result-response allowlist regression was caught and fixed by retaining the
  original four keys. Additional receipt references belong in work history, not
  extra result-response fields. No baseline assertion was weakened.
- API fixture failures reflected missing owned DAP records and wrong fixture
  skill IDs; fixtures were corrected, not ownership/provisioning checks. Synthetic
  expiry clocks were kept behind actual Ledger recording time, not future-dated.

## Current actual status, not lab status
Authenticated live GET `/api/portal/activation/runtime` returned200 with:
configured=false, custody_delivery_bound=false, skill_query_execution_bound=false,
worker_paths_bound=[], execution_authorized=false, live_proof_verified=false.
Anonymous new query/delivery endpoints returned401. This is real API evidence,
not proof of a source read, answer, delivery or workload.

All positive custody/grounding/admission/effect examples in this batch use
SYNTHETIC/MOCKED native providers and in-memory keys. Signature math and Ledger
contracts are real; source/answer bytes and actual custody endpoints were NOT
used. No real non-GPU A/B proof or live certificate was issued. No actual provider
transport was installed because none is configured/recovered in this workspace.

## Remaining work
Bind the existing admitted non-GPU execution/custody/query-ingress services and
recover their actual signed controls. Then run genuine bounded source→registry→
delivery and grounded-skill/refusal proofs, with independently observed counts,
usage and delivery before certificate issuance. Native provisioning and physical
cross-host qualification remain pending actual interfaces/authority. GPU is
explicitly parked under the user's latest instruction. Do not substitute tests,
Tigris credentials, in-pod processing or old demo records for live qualification.