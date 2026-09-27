# New GPU connection diagnostic — 2026-09-27

## Scope
User: “I have no idea what these are - have we completed all the other items.
Try and run the GPU connection”. One read-only diagnostic per existing configured
host, preserving client admission and server pins; no workloads, key changes,
configuration changes, new targets or ongoing retry authorisation.

## Observed 17:33:52–17:33:56 UTC
| Check | akki-vm | akki-vm-ii |
|---|---|---|
| TCP/SSH server reached | Yes | Yes |
| Saved server identity matched | Yes | Yes |
| Local client admission | IDENTITY_PIN_MISMATCH | IDENTITY_PIN_MISMATCH |
| Actual public-key authentication calls | 0 | 0 |
| Authentication-method discovery | auth_none → publickey | auth_none → publickey |
| Authenticated session | No | No |
| Channels / commands / workload | 0 / 0 / none | 0 / 0 / none |

The admitted client key and the configured available key do not agree. The
existing guard was preserved. This check did NOT offer the mismatched key to
the remote server; therefore it must not be reported as a fresh key rejection.
Network reachability is not successful login and not GPU hardware health.

Protected files unchanged: backend.env, key file, known_hosts, execution_identity.py,
remote_dispatch.py. No credentials or accounts were created/modified. New files are
the diagnostic tool and evidence only; no application feature was changed.

## Sources
- `/app/test_reports/iteration_46.json`
- `/app/assessment_workspace/phase0/drill_receipts/20260927T173352Z_gpu_connection_diag_once/intent.json`
- Same directory `result.json`, including before/after protected-file hashes.
- `/app/assessment_workspace/tools/gpu_connection_diag_once.py` (reviewed after run;
  no implicit authority to rerun; reads existing config, verifies pins before auth).

## Interpretation and corrections to diagnostic recommendations
Report46's suggestion to “refresh/realign” admitted receipt fingerprints must NOT
be interpreted as permission to pin the currently mismatched key. That would hide
the custody mismatch without demonstrating remote authorisation.

Offline RCA repeated older assertions that either/both client keys are absent or
unauthorised in remote authorized_keys. Those claims are NOT established. No remote
authorized_keys or sshd policy was inspected. Historical26Sep actual key-auth
rejections do not identify the exact server-side reason or establish the original
key's current status. Keep those observations separate from today's guarded test.

## Safe next step and programme status
Recover the originally admitted access through its existing runtime/key custody or
the responsible administrator. Do not generate a third key, rotate identities,
rewrite pins, disable checks, overwrite working original-runtime credentials or
ask for a private key in chat. Any replacement admission is a distinct authorised
operation with remote verification, not an automatic repair.

Control-plane engineering, recovery safeguards and hold-reason UI are tested
(last full run565backend/7frontend). Genuine source-to-registry/retrieval, grounded
skill and training/independent-evaluation proofs, live certificates and physical
cross-host qualification remain incomplete. Lab proofs are SYNTHETIC/MOCKED.
Not all remaining work is inherently GPU-dependent. Original live-pod health was
not checked by this local-workspace diagnostic.