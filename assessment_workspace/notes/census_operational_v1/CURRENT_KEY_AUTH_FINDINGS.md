# Current-key SSH diagnostic — real result, 2026-09-26

## Owner authorization and exact scope
Owner explicitly approved one actual public-key authentication attempt per GPU
host, bypassing ONLY Akki's local client-fingerprint equality check. Existing
private-key custody and admitted-receipt integrity checks were retained, as were
pinned server host-key checks. No passwords/agent/key search/fallback, retries,
channels, shell commands, source queries, key/configuration or VM changes.

The authorization was consumed by the two attempts below. This is not permission
to reconnect automatically or to change either client or server identities.

## Actual results

| Host | Started UTC | TCP | Pinned server key | Actual public-key auth calls | Outcome |
|---|---|---|---|---:|---|
|akki-vm|2026-09-26 10:34:17.022|Connected|Matched|1|AuthenticationException: `Authentication failed.`|
|akki-vm-ii|2026-09-26 10:34:19.047|Connected|Matched|1|AuthenticationException: `Authentication failed.`|

Both finished by10:34:21.049UTC. Neither authenticated. No session channel or
remote command was opened/executed. These are real authentication attempts, not
the older auth_none discovery and not mocked outcomes.

The same existing client key was offered to each configured `ubuntu` account:

```
SHA256:dtmtQPKdrqRioj5sas2RCucpKpP97F5c0/0tPHTux2o
```

The previously admitted client fingerprint remains different:

```
SHA256:M3Dre1A1I1ZQFo0FDsfzbWPwn5z+oxmZ02y1eZwFy1A
```

Actual connection code in `assessment_workspace/tools/current_key_auth_once.py:108`:

```python
next_methods = transport.auth_publickey(config.username, key)
```

At this line the server's key had already been verified. The diagnostic does
not call `execution_identity.verify_identity`; it deliberately allows the
recorded client-fingerprint mismatch for this approved one-off test.

## What is established, and what is not

- The local fingerprint equality guard is **not the sole blocker**: actual SSH
  authentication still failed when that comparison was bypassed.
- This does NOT prove an AISCA defect or establish the contents/permissions of
  `authorized_keys`. The remaining problem may still be our key custody/configuration,
  account authorization, or another server-side authentication policy.
- GPU/CUDA/workload health was NOT tested. A shell was not obtained.
- No application or environment file changed. No keys were generated or changed.
- The correct next recovery is to restore an actually authorized client identity
  or coordinate enrollment of an authorized replacement public key. Merely deleting
  the local guard cannot make the server accept this credential.

## Independent verification

`test_reports/iteration_14.json` independently checked the diagnostic logic and
the REAL live receipts without another network call. Its offline transport tests
are explicitly **MOCKED**:12passed,1local-environment check skipped,0failed.

The main follow-up loaded existing configuration and reran exactly that suite
with outgoing socket connections explicitly blocked: **13passed,0skipped**.
This removed the runner-environment limitation without SSH retries or app changes.
These checks validate the diagnostic/receipt interpretation, not a credential fix.

Evidence:
- `CURRENT_KEY_AUTH_LIVE_RESULT.json`: combined real result.
- `phase0/drill_receipts/census_operational_v1/execution_recovery/current_key_auth_owner_authorized_v1/`: exclusive intents + per-host results.
- `current_key_auth_verification/`: offline tests/JUnit and configured recheck.

## Administrator-facing update

“On26September2026 at10:34:17–10:34:21UTC we bypassed only our local client-key
admission comparison and made one real key-only SSH authentication attempt as
ubuntu on each existing VM. TCP and pinned server identity checks passed. Both
actual calls to Paramiko Transport.auth_publickey returned AuthenticationException:
‘Authentication failed.’ The offered client fingerprint was
SHA256:dtmtQPKdrqRioj5sas2RCucpKpP97F5c0/0tPHTux2o. Please check sshd authentication
logs and the approved public-key/account authorization for those attempts. We
have not inspected authorized_keys or changed anything on the VMs.”

No support message was sent. SSH access remains unresolved; no fix is claimed.