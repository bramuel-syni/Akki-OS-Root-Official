# Model consumers, eligibility and acknowledged handoff — 2026-09-27

Owner: continue autonomous architecture-first programme. No new live admissions,
credentials, source/model/GPU calls, receiver impersonation or prototype changes.

## Exact five-member denominator
1. Native skill descriptor → governed result-handle flow.
2. Native training descriptor → registered artifact flow.
3. Native evaluation descriptor → registered report flow.
4. Purpose-bound input-eligibility receipts consumed before effect and release.
5. Native Mkondo handoff + receiver acknowledgement + separately committed send.

## Known authority / non-decisions

- Reuse native licence/catalogue, principal, asset registry and usage adapters.
- Skill corpus/floor remain bound to the provisioning contract; quality eligibility
  is not fact truth and never upgrades a response class.
- Training/evaluation use their existing corpus/model/MOAC/held-out descriptors;
  no seventh criterion, adopted threshold, real experiment or quality score invented.
- DQ integration is a CONSUMER receipt gate, not a new classifier. A server-owned
  admitted quality producer must supply effective policy, pack and snapshot refs for
  the exact request and purpose. Unknown, expired, denied or unassessed inputs hold.
  No unresolved stratum/exception table is answered in code. Source population
  inspection is not labelled Clean merely because this consumer gate does not apply.
- Canon15§33/CA1-009: use frozen HandoffContract_v0 before crossing; preserve native
  Mkondo distinct-author/receiver check and native register/attest persistence.
- Sender task/principal remains unchanged. Receiver has a DISTINCT admitted
  principal and a deterministic distinct receiver-task reference. This is metadata
  naming/acknowledgement, not E1 creating a receiver identity or executing as it.
- Existing native emitter's returned intent is not durable by itself. Bank the
  handoff envelope through the canonical Ledger BEFORE native file projection,
  and bank verified receiver ACK before any effectful send.

## Architecture changes

1. Add strict purpose-bound eligibility receipt and sidecar delivery/receiver-ACK
   schemas; no fields added to frozen Canon contracts, Request or WorkerResult.
2. Bind optional quality/handoff producers through server-owned ExecutionBindings;
   production composition always installs the appropriate fail-closed gates. Missing
   providers hold affected work. No browser/API registration or caller policy flags.
3. Explicit finite metadata RPC timeout required when these producers are bound.
   No polling loops/background scheduler. Concrete providers remain separate elements.
4. Pin quality policy/pack/snapshot identity in the same Ledger; renew current
   verification receipts without silently changing the admitted input basis.
5. Receiver selection/mandate must bind exact request/scope/authority/shape/fence,
   be current, and resolve an admitted distinct principal. Use deterministic handoff
   and receiver-task IDs, never a caller-selected target identity.
6. Use explicit HANDOFF_CONTRACTS_DIR configuration before calling existing file
   persistence; do not inherit its hardcoded fallback. Tests isolate it to temporary
   metadata directories. No production .env/config changes or file migration.
7. Separate durable dispatch RESERVATION from a unique send-commit slot. Failures
   before send commitment can be retried after fresh gates. Once send is committed,
   ambiguous outcomes use stable-key status; never blindly resubmit. Legacy dispatch
   rows that predate this protocol and lack a protocol marker remain conservative
   status-only, not presumed unsent.
8. Cancellation competes on that SAME send slot; if cancellation wins before send,
   there is no worker effect. A receiver's metadata ACK is not execution or usage.
9. A versioned metadata-only delivery packet carries the frozen request/authority,
   native handoff, receiver task, committed ACK/send refs, and eligibility receipt
   ref where required. A server adapter must explicitly support this delivery RPC;
   no silent fallback to the old unqualified submit callback.
10. Bind returned executor identity to the admitted receiver. Preserve current-rights,
    input eligibility and artifact revalidation before publication/retrieval; actual
    already-consumed usage remains recorded even when output becomes ineligible.

## Acceptance / shortcuts

Positive tests use REAL builders, coordinator, canonical Ledger kernels, native
principal/licence/catalogue adapters, Mtafiti writer, usage consumer and Mkondo
contract/registry/persistence. Upstream observations/decisions and storage are
SYNTHETIC/MOCKED/FAKE, including any measured-shaped schema fixtures. Never call
these live execution, owner confirmation, signatures, model quality or performance.

Tests first, then runtime:
- Complete all three model kinds, using real provisioning/training descriptor
  contracts where available, correct class floor and real native catalogue/usage.
- Fresh eligible vs denied/not-assessed/expired/changed input basis, no class lift;
  deny queued dispatch or release after withdrawal without fabricating zeros.
- Contract/authored-by/source actor/receiver/shape/scope/fence/expiry mismatch;
  unknown/suspended/dual-hatted receiver; no receiver context spoofing in E1.
- Native handoff file appears only after durable envelope; ACK only after receiver
  verification; send only after ACK and its own durable claim. No false acknowledgement.
- Failure/restart before handoff, native projection, ACK commit and send commit;
  known-pre-send recovery vs post-send uncertainty; duplicate/concurrent advance and
  cancel races; at most one initial effectful submit per operation key.
- Malformed/expired/mismatched ACK or a worker returning another executor refuses.
- Mutable eligibility/receiver basis cannot silently widen a pinned objective;
  current expiry/revocation still checked despite previously banked receipts.
- Existing143 regressions retained. Old native positive fixtures may need explicit
  synthetic handshake inputs; do not relax gates or change sealed schemas to pass.
- Protected hashes and literal UI remain unchanged. No credentials/accounts created.

## Completion artifact and bounds

Bank five-member test/evidence mapping, RED/GREEN scripts/output, mode labels and
protected-file hashes. Shared-workspace checking is not EX4/R37 isolation. This slice
does not implement live receiver credential/mandate verification, continuous
mid-work enforcement, full delegated-ledger consumption across actors, all DQ
classification, real skill answers/training or full Mkondo coverage. Those remain
explicit element/architecture follow-ups; no global promise completion claim.