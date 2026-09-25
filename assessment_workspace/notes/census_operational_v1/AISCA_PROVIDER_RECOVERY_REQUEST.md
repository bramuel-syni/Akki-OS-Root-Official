# AISCA recovery request — prepared, NOT SENT

## Subject
Existing VM console launch returns HTTP502 — akki-vm / akki-vm-ii

## Observed issue

We can authenticate to `https://console.cpt.aiscafrica.org` and view both existing VMs, **akki-vm** and **akki-vm-ii**, in **akki-workspace**. Both are listed as **Running**.

Opening each VM through **Edit Configuration → Open console** opens a console tab, but its console request returns **HTTP502 before a terminal or login prompt is available**:

- akki-vm-ii: 2026-09-25 approximately19:53 UTC.
- akki-vm: 2026-09-25 approximately19:55 UTC.

For akki-vm, the existing **SSH Public Key** field remains disabled after configuration loading settles; its expanded value editor is read-only. No values were entered or saved.

## Requested provider action

Please restore the console-access path for these **existing VMs**, verifying the console service, gateway connectivity, account permissions and applicable VM management components. The client-side observations do not establish which provider component caused the502.

Alternatively, provide an approved administrator-assisted procedure to append an owner-authorized replacement SSH public key to the exact existing VM account on both machines. The new identity is authorized but has not yet been generated or installed; enrollment/custody will be coordinated once the working route is established.

## Preservation requirements

- **Do not delete, recreate, redeploy, restart or stop either VM** as part of this request without separate explicit authorization.
- Preserve VM disks, running workloads, existing server host keys and unrelated SSH authorizations.
- Do not re-enable SSH password authentication.
- Retain the old Akki authorized key until the replacement has passed pinned-key authentication checks on both VMs.
- Do not request or transmit the replacement private key; only the public key is enrollable.

We have made no VM configuration/lifecycle changes and sent no console credentials or shell commands. No source/estate database has been queried through the recovery client.

## Evidence reference

`assessment_workspace/phase0/drill_receipts/census_operational_v1/execution_recovery/aisca_authenticated_recovery_20260925.json`

This brief has been prepared only. No support ticket/email has been sent and no provider intervention is claimed.