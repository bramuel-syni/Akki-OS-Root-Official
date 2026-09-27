# Fresh direct connection from the new owner workbook

## Owner instruction and scope
Owner explicitly requested rebuilding the connection seam from newly supplied
`GPU CREDs.xlsx`, without historical CLIENT-key/approval comparisons, rotation or
administrative/key changes. Owner clarified that connection takes priority and
retained historical records must not influence it. Historical evidence retained
only for audit, never consulted by the active direct connector.

## Supplied connection specification
The new workbook supplies2 targets, each with hostname, public IP, username and
password. It supplies NO private key. Endpoint/account/password are read only
from this new workbook. SSH port22 and timeout8s are explicit non-secret connector
configuration, not recovered client credentials. Workbook custody is mode0600,
git-ignored, never copied into application/source/logs/public API responses.
Custody reference is recorded privately in `/app/memory/test_credentials.md`.

## Fresh seam and active routing
`services/gpu_direct/{workbook,connection,config}.py` implements the new path:
- Reads exact new password values, no key load/generation/agent/discovery.
- Connects to the workbook IP/account with one `auth_password(..., fallback=False)`.
- Verifies the SERVER endpoint using existing server known-hosts only. Server keys
  do not supply or compare any CLIENT credential and passed in both real attempts.
- Returns safe stage outcomes; no raw credential or provider exception text.
- Does not consult `verify_identity`, prior client-key files, old client identity
  receipts, principal admission or activation approvals to establish SSH login.

Following the real test, active application configuration was set explicitly:
`AKKI_GPU_CONNECTION_MODE=direct_workbook`, new workbook path, SSH port and timeout.
Both the legacy training-runner connection entrypoint and census `_connect` now
dispatch to the direct connector. Active host inventory/credential metadata also
come from the workbook. Failed direct auth never falls back to old client keys.
Missing/corrupt workbook fails without reverting to old credentials. Backend was
restarted for the explicit non-secret configuration change. No credentials or
server accounts were rotated. Existing initial env keys/audit records remain
preserved but old client settings are not read by the selected connection path.

## REAL connection result — 2026-09-27 17:47:10–17:47:14 UTC
One password attempt per target, no retry, no remote channels or commands:

| Target | Reached SSH server | Server identity verified | Actual password calls | Reply | Authenticated |
|---|---|---|---:|---|---|
| akki-vm-ii | Yes | Yes |1|DIRECT_PASSWORD_METHOD_NOT_ALLOWED; allowed_methods=[publickey]|No|
| akki-vm | Yes | Yes |1|DIRECT_PASSWORD_METHOD_NOT_ALLOWED; allowed_methods=[publickey]|No|

This is a real remote authentication-method rejection, NOT a local historical
client-key mismatch. It does not establish that the supplied password is incorrect;
password authentication was not accepted by these SSH listeners. No current client
key's authorisation or GPU hardware condition was tested. The server's actual sshd
configuration/authorized_keys were not inspected or changed. No key-auth fallback.

## Evidence
- `/app/test_reports/iteration_47.json`
- `phase0/drill_receipts/20260927T174710Z_gpu_direct_workbook/{intent,result}.json`
- Live one-off launcher `tools/gpu_direct_workbook_once.py` (do not re-run under
  consumed authorisation). Connection code does not import legacy identity guard.
-6 initial offline tests plus7 active-entrypoint tests passed:13total; dummy
  transports are MOCKED. They prove code selection/sanitisation, not live auth.
- Full backend result: **578 passed,2 pre-existing explicitly gated custody drills
  skipped,0 failures/errors** in116.234s:
  `test_reports/pytest/gpu_direct_full_regression.{xml,log}`.
  No additional GPU network calls occur in regression tests. Network-blocked
  configured inventory check shows direct mode, password login and no client-key
  path for both targets. Restarted application returns401 for anonymous access to
  authenticated activation-profile route as expected.

The live receipt's protected-hash equality describes that diagnostic's before/after
period. The subsequent explicit .env/entrypoint change is documented above; do not
mistakenly claim that no local configuration was changed during the entire task.

## What is and is not complete
Fresh direct seam implemented and selected; login is NOT successful. GPU connection
still precedes workloads. No proof, workload, source/model read or certificate ran.
No server rotation, password-enablement, agent use or previous client admission.

Next input should be the GPU provider's actual **Connect** instructions (SSH command
or connection screenshot with secrets hidden). The workbook supplies passwords but
the reached SSH listeners advertise publickey. Determine whether those passwords
are meant for a browser console or whether the provider's SSH instructions specify
a key. Do not ask for private keys in chat, invent credentials, enable server
password login, or change account policy as an automatic fix. Do not conclude the
original working runtime is affected by this separate workspace's result.