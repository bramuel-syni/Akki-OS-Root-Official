# Native binding requirements — no new identity store or credentials

All paths below are relative to `backend/vendored/extraction_akki/backend`.
This specifies what the owning engine/admission bridge must supply; it is NOT a
request to replace keys, invent owner approvals, or use E1 as the runtime.

## Admission and signer provenance
`services.activation.receipts.NativeReceipts` requires a server-owned async
`admitted_keys.resolve(tenant_id, principal_id, key_id) -> AdmittedSigner`.
The result must be derived from actual existing native admission/mandate/key
provenance records, with tenant/principal/key, admitted public key, admission
reference, scoped permissions, validity and current revocation. Existing
PrincipalV1/ControlScope remain the principal and request boundaries. The current
in-process principal store and mere possession of a key file do not supply this
bridge. No resolver or trust root has been installed in the current app.

Permissions are explicit record purposes: `activation:plan`, `:allocation`,
`:worker`, `:approval:<group>`, `:observation:<category>`, `:revocation`,
`:certificate`. Worker records attest capabilities of an ALREADY admitted worker;
they do not create a principal or authorize unknown infrastructure. Native workers
sign their own enforcement/usage observations under admitted scoped mandates.

`SignedReceipt` defines exact versioned, domain-separated canonical signing bytes;
signature public keys never come from a client body. HTTP relaying principal is
recorded separately from the cryptographically verified native producer. All live
signatures must be produced by the existing admitted owner/engine, not E1.

## Runtime and native ports
- `BoundedEngineAdapter` extends, rather than modifies, original EngineAdapter.
  Supply async submit/status/cancel, model delivery where needed, and
  `admit_limits_rpc(request, operation_key, fence, RuntimeEnvelope) -> SignedReceipt`.
- The admitted worker must independently enforce dimension/unit ceilings, zero
  spend where adopted, start/stop/terminate deadlines, stable operation identity and
  fence. The exported cooperative RuntimeLimiter is not a hard supervisor. Its
  deployment and actual termination must be evidenced by the owning runtime.
- Bind existing eligibility, Mkondo handoff/receiver and native artifact inspector
  APIs. Inspectors and models return metadata/custody references; actual bytes stay
  within the admitted source/worker/registry/retrieval paths, never E1.
- `native_activation_bindings(...)` in `services.activation.composition` produces
  receipts, evidence verifier and ExecutionBindings. Owning application startup
  must bind them to `app.state.activation_receipts`, `activation_evidence`,
  `execution_bindings`, with explicit `activation_evidence_timeout_seconds`.
  No placeholder configuration is automatically installed.

## Records needed before effects
Signed adopted allocation, worker attestation and immutable Plan with frozen
request/terms/scope/purposes, all independent required approval groups, exact four
dial and three policy versions, actual snapshot/script commitments and dimensional
ceilings. Each group approval must reference this plan and its current mandate.
No assumed20 GPU-hours or USD0 allocation is minted from chat/history.

For C, the protected split and exact six native MOAC criterion mapping/thresholds
must be adopted before training. Evaluation consumes the recorded training artifact
under a separate native request and independently admitted producer; release is a
separate signed decision. For B, require actual signed anchor commitments and a
genuine out-of-scope refusal, not the legacy `SKILL_EXECUTOR_UNADMITTED` refusal.

## Proof/issuance boundary
Frozen schema field mappings are `inputs.dial_versions` and `inputs.policy_versions`;
there is no `policy_and_dials` field. Signed certificate seals bind the canonical
document excluding only `issuer.signature`, which carries the native seal receipt
reference. All additional claim/backlink/reference rules are executable in
`native_evidence.py` and `native_joins.py`.

APIs `/receipts`, `/readiness`, `/reservations/settle`, `/certificates/issue` are real
metadata routes. Current app bindings remain absent, so they cannot manufacture
grants/live certificates. Complete real Path A→B→C proof remains required; test
keys, fake ledger positives or isolated Mongo test reservations cannot satisfy it.