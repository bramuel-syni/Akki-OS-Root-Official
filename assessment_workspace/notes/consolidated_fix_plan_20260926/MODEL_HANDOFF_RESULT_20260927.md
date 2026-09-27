# Model-handoff architecture result — 2026-09-27

## Scope and result

Owner-approved continuation of the architecture-first Akki programme. Implemented
the five-member slice in `MODEL_HANDOFF_CONTRACT_20260927.md`: native skill,
training and evaluation compositions; purpose-bound eligibility consumption;
acknowledged Mkondo handoff followed by a separate durable send claim.

**GREEN: 227 passed / 0 failed / 0 skipped, twice**, once with two pytest workers
and once serially. This comprises **84 model-handoff cases + 143 prior scoped
regressions**, not 227 platform promises or live operational journeys. Nine pinned
files remain hash-identical, including both literal owner prototypes. No frontend
code, environment, dependencies, credentials, admissions or GPU configuration changed.

## Implemented chain

- Native builders freeze exact skill provisioning/corpus/floor or training and
  evaluation descriptors. Existing principal, licence, catalogue, Mtafiti and
  usage producers/consumers remain the governing components.
- `northena/execution_eligibility.py` consumes strict current receipts from a
  server-owned producer; exact request, input order, scope, purpose, policy,
  rule-pack and snapshot basis is pinned. Ineligible, unassessed, unknown,
  expired, changed or MOCKED evidence holds. It does not classify data or
  invent DQ thresholds, model quality or fact truth.
- `mkondo/execution_delivery.py` defines frozen receiver binding, ACK and
  metadata-only delivery sidecars; frozen Canon contracts are unchanged.
  Deterministic distinct receiver-task IDs do not create receiver identities.
- `mkondo/execution_handoff.py` resolves an existing distinct admitted receiver,
  binds scope/authority/operation/shape/mandate/fence, banks the canonical
  envelope, then uses native Mkondo admit/register/attest. The receiver ACK
  must bind the actual contract digest before it is banked.
- `mkondo/execution_projection.py` requires explicit HANDOFF_CONTRACTS_DIR;
  native projection remains subordinate to the canonical envelope. Local file
  projection is locked, replay-attested, never silently overwritten. Missing or
  conflicting projection holds. It does not turn the native emitted intent
  into a second durable ledger authority.
- `northena/execution_send.py` separates reservation from the atomic send slot.
  Known-pre-send failures retry fresh gates. Cancellation competes on the same
  slot. Once send is committed, uncertainty is status-only: even a crash BEFORE
  invoking delivery must not cause a blind resubmit. The worker must support
  stable operation-key reconciliation; this is NOT exactly-once network delivery.
- `EngineAdapter.submit_delivery` requires an explicit bounded delivery callback,
  cross-validates the packet and binds returned executor identity to the receiver.
  No legacy submit fallback for production model handoffs. Source-kind work is
  not labelled Clean or charged an invented model price.
- Publication and retrieval recheck rights, eligibility, receiver basis and native
  artifact evidence. Post-effect output holds preserve measured-shaped actual
  usage receipts from the fixture under dispatch-time commercial terms.
- Production assembly installs fail-closed gates. Optional direct-core fixtures
  remain an isolated architecture seam, not public or production gate bypasses.
- Narrow consumer fix: exact native `PrincipalRefusal` becomes
  `Held("PRINCIPAL_NOT_ADMITTED")`; unrelated RuntimeError still propagates.
  No login/token/password/admission rule or sealed principal-store change.

## Evidence and corrections

Evidence directory: `model_handoff_verification/`.

1. Iteration32: original RED 1 pass / 9 fail; original test body retained in
   `iteration32_original_tests.py.txt`. Initial runtime attempt: 66 pass / 6 fail.
2. Iteration33: positive fixtures corrected, not runtime weakened: model catalogue
   selection, explicit admitted receivers, deterministic shape/task IDs, actual
   contract digest, eligibility, finite timeout and explicit delivery RPC. Missing
   eligibility retained as a negative. Legacy ambiguity fixture now returns
   unknown rather than complete-with-missing-commercial-snapshot. Old exact
   3-field binding assertion updated to approved 6-field extension. 153 pass.
3. Iteration34: 51 additional gate/withdrawal/mismatch/timeout tests; 50 pass,
   one real native unknown-principal exception escaped. Exact exception mapping
   corrected and retested; then all204 passed.
4. Iteration35: new restart suite initially 15 pass / 7 fail. Its diagnosis of
   repeated delivery was **incorrect**: `DeliveryAwareRpc.delivery` incremented
   the counter and called its parent, which incremented the SAME counter again.
   Original file retained as `iteration35_original_restart_tests.py.txt`.
   Corrected the helper, preserving assertions of exactly one initial invocation;
   no production resubmit logic was weakened. Added after-send-commit/before-RPC
   crash case, proving zero delivery and persistent unknown/status-only recovery.
5. Final: model suite84 + baseline143 =227, all pass twice. Original reports32–35
   and failing JUnit artifacts remain unchanged; final evidence supersedes their
   current defect status, not their historical observations.

Final artifacts:
- `/app/test_reports/pytest/pytest_model_handoff_final_20260927.xml`
- `/app/test_reports/pytest/pytest_model_handoff_final_serial_20260927.xml`
- `model_handoff_verification/final_green_20260927.log`
- `model_handoff_verification/final_green_serial_20260927.log`
- `model_handoff_verification/FINAL_MODEL_HANDOFF_EVIDENCE_20260927.json`

Python compilation and diff whitespace checks pass. Existing multipart dependency
deprecation warning remains; no new dependency was installed. Unchanged DAP shell
loaded at the current preview URL in a desktop smoke test; this is not new visual
acceptance or full UI testing.

## Five-member test mapping

All following tests reside in `/app/backend/tests/model_handoff/`:

| Member | Behavioral evidence |
|---|---|
| Native skill | `test_model_handoff_red_contract.py::test_native_skill_training_eval_trajectories_with_eligibility_and_handoff_outbox[_skill_request]` |
| Native training | Same test, `[_training_request]` |
| Native evaluation | Same test, `[_evaluation_request]` |
| Eligibility consumer | `test_model_handoff_supplemental_iteration34.py::test_invalid_eligibility_receipts_hold`; `test_withdrawal_phase_blocks_readiness_and_preserves_usage_post_effect`; `test_model_handoff_restart.py::test_changed_pinned_pack_snapshot_basis_blocks_send` |
| Acknowledged outbox | `test_mkondo_handoff_explicit_dir_and_pre_send_ack_projection_order`; restart suite `test_restart_fail_once_durable_recovery_paths`, both projection recovery tests, `test_cancel_wins_between_rows_check_and_send_insert`, `test_duplicate_advance_barrier_exactly_one_delivery_no_legacy_submit` |

Additional negatives cover unknown/suspended/dual-hatted receivers, wrong executor,
ACK bindings, expiry, missing providers, finite timeouts, changed receiver mandate,
projection corruption, class-floor refusal and legacy status-only behavior.

## Limits and next work

**Upstream decisions, eligibility, receiver/ACK, worker and inspector inputs are
SYNTHETIC/MOCKED; positive ledger storage is FAKE.** Measured-shaped fixture schemas
are not live measurements, signatures, admissions, owner grants or model execution.
Native canonical kernels, registry/usage consumers and Mkondo file projection are
real code exercised with those fixtures. Actual portal API regressions only verify
existing held/auth/scope/replay behavior, not successful source/model execution.

Production decision, eligibility, receiver/ACK, worker and independent inspection
providers are still unbound; callable answers/training/evaluation are not live.
No source/provider/model/GPU/SSH calls. AISCA remains parked. No credential changes.
No multi-host storage/failover or hardware-performance guarantees. Local file locking
does not prove shared-volume cross-host behavior. Remote mandate verification,
receiver-side receipt lookup/fencing/idempotency, full delegated-actor ledger
consumption and continuous mid-work revocation remain separate element work.
No whole Mkondo/DQ/W1/DAP/T14/platform completion claim.

Next P0: extend admitted producer/custody joins and prepare the bounded
source→registry→metered verified result→rights-gated retrieval acceptance path;
activate only with actual admitted evidence, never by turning fixtures into grants.
P1: grounded warm-answer path with context-loss disclosure and broader DQ/entitlement
consumer coverage. P2: real experiments, audio/serving/withdrawal/transformed-output
journeys. Owner EX/DQ/CC rulings and AISCA holds remain in force.

Potential enhancement: show receipt-linked unmet prerequisites in the existing
request drawer, preserving the owner's original markup and visual design.