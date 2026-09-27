# Existing-provider binding contract — non-GPU continuation

This is a typed interface implemented for an EXISTING admitted service, not a
claim that a service endpoint exists or has been installed. Nothing activates
without the owner-estate's actual provider and signed authority.

## Callable query ingress
1. Client/native query ingress retains question/corpus bytes within the owning
   runtime. The Akki portal intent banks only query SHA256 and provisioning SHA256.
2. Owning native plan references its actual query handle and the emitted query ID,
   exact provisioning/corpus/grant/floor/objective hash from skill_request().
3. Existing signed plan/approval/allocation/worker flow admits execution. Native
   worker records registered answer artifact, measured usage and skill_response
   observation. Independent source/anchor producer signs each anchor commitment.
4. Akki verifies metadata and returns admitted references, never answer bytes.
   A separate custody handoff can deliver the result directly to the client.

Observation skill_response: context_sha256=request.digest(); grounding contains
actual query_ref, answer_sha256, anchors and context disclosure. claim_sha256 is
the Canon digest of {request_sha256, artifact: Artifact JSON, grounding: JSON}.
Refusal observation must be current, native, request-bound OUT_OF_SCOPE and cite
the intent receipt, with claim_sha256 of its structured Refusal payload.

## Custody provider
Compose `CustodyBinding` into `NativeRuntime(custody=...)`. Receipts must be the
same NativeReceipts object as the rest of the native runtime. Explicit fields:
native custodian principal, exact allowed HTTPS origins, maximum grant duration,
metadata timeout. No wildcard domain matching or generic file-download proxy.

Async methods:
- `prepare(DeliveryDescriptor, current Authority) -> ProviderState`
- `status(DeliveryDescriptor, current Authority) -> ProviderState`

ProviderState contains signed native grant/completion receipts, and optionally an
opaque SecretStr capability URL. It contains no source/answer bytes. The provider
must honour stable delivery_id/descriptor binding and current authorization at
actual redemption; issuing any static/unrevocable object URL is not this contract.

The signed Observation category is delivery_grant or delivery_completion;
context_sha256=DeliveryDescriptor.digest(), claim_sha256=digest(DeliveryProof JSON).
DeliveryProof covers requester/artifact SHA+size/delivery ID, native event ID,
current-rights-at-redemption declaration and workspace_touched_bytes=false.
Grant adds exact allowed origin and SHA256 of the returned capability URL.
Completion adds original grant receipt, redemption/completion times, actually
delivered byte count and observed SHA256. All phases must be measured, not MOCKED.

The caller checks signatures/mandates/scope/bounds independently and records only
receipt references/metadata. No URL in Ledger. Pending/timeouts remain unverified;
completed must be exact-byte/hash receipted. Completed historical evidence can be
reconciled after capability expiry, never used to resurrect the capability.

Current application has no bound native provider. Test providers do not satisfy
this requirement and must not be installed in its active composition. No GPU
interaction belongs to this work.