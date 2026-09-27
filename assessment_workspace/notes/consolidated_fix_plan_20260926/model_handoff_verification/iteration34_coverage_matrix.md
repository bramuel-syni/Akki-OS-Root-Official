## Iteration34 Supplemental Model-Handoff Coverage Matrix

- Suite: `/app/backend/tests/model_handoff/test_model_handoff_supplemental_iteration34.py`
- Result: **50 passed / 1 failed** (51 behavioral cases)
- JUnit: `/app/test_reports/pytest/pytest_model_handoff_iteration34_supplemental.xml`

### Covered acceptance themes
- Gate presence + fail-closed: missing eligibility/handoff/delivery RPC holds
- Finite timeout enforcement: invalid timeout values rejected
- Producer timeout paths: eligibility/receiver/ack bounded timeout holds
- Eligibility integrity: request/input/scope/purpose/expiry/disposition mismatches
- Eligibility basis pinning: policy basis change between reserve/send held
- Withdrawal effects by phase: send/verify/publish/retrieve not-ready behavior; metered usage persistence post-effect
- Receiver binding integrity: strict cross-field mismatch rejection
- Suspended receiver principal hold behavior
- ACK integrity: malformed/mutated ACK blocks send
- Contract mutation defense: authored_by mutation rejected by packet cross-validation
- Executor identity enforcement: delivery/status/cancel receiver mismatch holds
- Post-send timeout recovery: unknown first pass then status-only recovery without resend
- Native projection conflict refusal
- Concurrency interleaving: advance/advance one send slot; advance/cancel cancel-wins no submit
- Legacy dispatch (no protocol marker): submit not retried
- No class lift: defensibility floor enforcement

### Open failing case
- `test_unknown_receiver_lookup_refusal_is_held`
  - Expected: held `PRINCIPAL_NOT_ADMITTED`
  - Actual: uncaught `PrincipalRefusal` (RuntimeError subclass) escapes from `ComponentAuthority.principal`
  - Impact: unknown native principal lookup can bubble exception instead of canonical hold.
