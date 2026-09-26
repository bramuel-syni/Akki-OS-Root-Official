# Engineer-to-engineer SSH handoff — recorded evidence, prepared not sent

## Subject: SSH authentication failure on Akki GPU VMs — public-key identity recovery

Hi,

I am trying to establish an SSH session as `ubuntu` from Akki's execution
environment to the existing GPU VMs, so we can run the Akki workloads there.

| VM | Address | Port | Account |
|---|---|---|---|
|akki-vm|41.173.184.244|22|ubuntu|
|akki-vm-ii|41.173.184.247|22|ubuntu|

**Where the connection fails:** the recorded checks reached both SSH servers.
The server-key pins matched, but no authenticated session/shell was established.
The servers advertise `publickey` authentication only.

Earlier OpenSSH attempts recorded:

```text
Permission denied (publickey).
```

Earlier Python/Paramiko attempts recorded a rejected password-authentication
method (`BadAuthenticationType`, allowed methods `['publickey']`) and a
key-authentication failure:

```text
Authentication failed
```

The latest banked method-only checks, on25September2026, were:

```text
18:57:52 UTC  akki-vm
  Server host-key pin matched: true
  Advertised authentication methods: publickey
  Authenticated: false
  Diagnostic result: AUTH_NONE_REJECTED

18:57:54 UTC  akki-vm-ii
  Server host-key pin matched: true
  Advertised authentication methods: publickey
  Authenticated: false
  Diagnostic result: AUTH_NONE_REJECTED
```

Those last two checks deliberately used `auth_none` to discover supported
methods: **no password or private-key authentication was attempted in that probe**.
`AUTH_NONE_REJECTED` is the diagnostic's label, not a verbatim sshd log. It confirms
that passwords are not an offered recovery method; it does not prove which
client keys are currently authorized.

**Client-side finding:** the private key available in our environment derives a
different public-key fingerprint from our previously admitted SSH client identity:

```text
Previously admitted CLIENT public-key fingerprint:
SHA256:M3Dre1A1I1ZQFo0FDsfzbWPwn5z+oxmZ02y1eZwFy1A

Available CLIENT key fingerprint at the recorded local check:
SHA256:dtmtQPKdrqRioj5sas2RCucpKpP97F5c0/0tPHTux2o
```

These are client-key fingerprints, not the VMs' server host-key fingerprints.
Our guarded worker refuses this identity mismatch before attempting another SSH
connection. We have not inspected either server's current `authorized_keys`, so
we are not asserting which key is presently installed there.

**Please help with the authentication identity rather than GPU diagnostics:**
1. Confirm `ubuntu` is the correct account and check sshd's authentication logs
   for the recorded connection attempts.
2. Confirm the authorized public-key fingerprint(s) for that account on both
   VMs, especially whether the previously admitted fingerprint above remains.
3. If the matching private key cannot be recovered through our authorized
   custody/backup, provide an approved administrator-assisted route to enroll
   our authorized replacement **public key** on both existing VMs.

Please preserve disks/workloads, server host keys and unrelated authorized keys.
Do not enable password login or revoke the existing Akki key before replacement
authentication has been verified. No private key should be requested or sent.

The observed blocker is SSH authentication/access identity, **not an observed
GPU/CUDA failure or a TCP timeout**. GPU health and workload execution remain
untested because we have not obtained a shell.

## Evidence limits and sources (not a new terminal transcript)

- Prepared from recorded24–25September checks. No new connection attempt,
  configuration change or remediation was made for this handoff.
- OpenSSH/Paramiko error strings are preserved in the banked aggregate receipt
  `phase0/connectivity_receipts/20260925T014858Z_CENSUS_LIVE_AND_GPU_DOOR_EVIDENCE.json`.
  This handoff does NOT adopt that old receipt's unsupported inference that the
  current key is absent from `authorized_keys`, nor its password-enablement advice.
- Latest per-host method results are in
  `phase0/drill_receipts/census_operational_v1/execution_recovery/auth_none_owner_compute_workbook/`.
- Client identity comparison: `notes/census_operational_v1/EXECUTION_RECOVERY.md:57–61`.
- No SSH terminal-error screenshot has been recovered. Do not represent the
  portal screenshots as SSH-client screenshots or manufacture one from these notes.