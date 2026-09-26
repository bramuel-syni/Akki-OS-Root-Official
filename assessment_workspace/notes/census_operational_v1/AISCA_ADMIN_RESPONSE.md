# AISCA administrator response — prepared, not sent

This message uses recorded observations from25September2026. No new portal/SSH
attempt or remediation was performed when preparing it. Provider root cause and
current service state are not independently established by this historical record.

## Copy-paste response

**Subject: Existing VM console access fails with HTTP502 — akki-vm / akki-vm-ii**

Hi,

We are trying to restore authorized, key-only SSH access to our two existing VMs
so the Akki service can execute its workloads there. We are not trying to create
replacement VMs or change their existing disks/workloads.

**Environment**
- Portal: https://console.cpt.aiscafrica.org
- Workspace: `akki-workspace`
- Existing VMs: `akki-vm` and `akki-vm-ii`
- Guest account shown in the portal: `ubuntu`

Portal sign-in succeeds, and both VMs were listed as Running. The failure occurs
after selecting **Virtual Machines → VM → Edit Configuration → Open console**.
The console opens in another tab, but its network request returns **HTTP502**
before any terminal or login prompt becomes available.

Recorded observations (UTC):

```text
2026-09-25 19:53  akki-vm-ii  Console request: HTTP502; no terminal/login prompt
2026-09-25 19:55  akki-vm     Console request: HTTP502; no terminal/login prompt
```

This is a summary of captured browser-network observations, not an AISCA server
stack trace. No console credentials or commands could be submitted. We cannot
identify the failing provider-side component from this response alone.

We also checked the alternative existing-VM key-update path on **akki-vm**.
After configuration loading completed, **SSH Public Key** was disabled/non-editable.
Its adjacent expanded value viewer also reported `readOnly=true`. This was
observed around20:04–20:06UTC. We did not modify or save any configuration. That
expanded key-editor check was not separately repeated on the second VM.

For context, Akki's local SSH identity safeguard currently reports:

```text
AKKI_EXECUTION_IDENTITY_NOT_VERIFIED
IDENTITY_PIN_MISMATCH
```

These are **Akki-side safety codes, not AISCA errors**. They mean the available
private-key identity does not match our admitted identity record, so the guarded
execution path refuses before attempting SSH. That is why we need a working
console or an administrator-assisted public-key enrollment route.

Could you please:
1. Investigate the console502responses for both VMs at the timestamps above,
   including console-service/gateway connectivity and account permissions.
2. Restore existing-VM console access, or provide the supported in-place procedure
   for enrolling our authorized replacement **public key** on both VMs.
3. Confirm the correct existing guest account and whether SSH-key editing is
   restricted for our portal account or unsupported for already-provisioned VMs.

Please preserve disks, running workloads, server host keys and unrelated SSH
authorizations. Do not recreate/redeploy, stop or reboot the VMs without separate
approval. We are not requesting password authentication to be enabled. A private
key should never be requested or transmitted; only a public key will be enrolled.

Thank you.

## Evidence attachments and their limits

The support_evidence directory holds copies of four original redacted portal
captures. They show the VM-details/Open-console control and the existing key form/
viewer. **They do not visually display HTTP502**, because the original automatic
capture remained on the parent portal page; the502was captured by network
observation in the aggregate JSON receipt. Do not label them screenshots of a
visible502error page and do not manufacture such an image.

- `01_akki-vm-ii_console_entry.jpeg`: parent details page/Open console.
- `02_akki-vm_console_entry.jpeg`: parent details page/Open console.
- `03_akki-vm_ssh_key_form.jpeg`: existing key-entry form.
- `04_akki-vm_ssh_key_viewer.jpeg`: expanded key-value viewer.
- `RECORDED_ERROR_SUMMARY.json`: sanitized factual observations for support.

Underlying receipts:
- `phase0/drill_receipts/census_operational_v1/execution_recovery/aisca_authenticated_recovery_20260925.json`
- `phase0/drill_receipts/census_operational_v1/execution_recovery/local_preflight_identity_refusal.json`

No support message has been sent. No provider-side or application fix is claimed.