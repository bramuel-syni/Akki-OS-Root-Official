# AISCA access guide — evidence and replacement boundary

## Owner screenshots / extra credentials reconciliation —19:32Z

The four supplied images show Figures5–12: Developer Hub navigation, VM catalog/new VM, SSH Public Key, source-IP SSH rules, VM details and redacted/masked deployment output. These images were considered; they confirm the documented provisioning flow, not an authenticated existing-VM console session.

Owner also stated more portal credentials were added. Current asset retrieval returned11 files including four new guide screenshots, with no separate new portal-credential file visible. Both prior GPU workbook URLs were privately re-fetched and compared: hashes unchanged, neither workbook contains an email-shaped value or portal label. Relevant environment key-name scan found no portal settings. No credential values printed or sent. Banked `portal_credential_reconciliation_20260925T193250671302Z.json`. Needed: location/filename of the intended new portal credential attachment, or reattachment if upload not present. This is not another request for the known provider URL or replacement authorization.

## Subsequent owner-supplied portal — verified19:21Z

Owner supplied `https://console.cpt.aiscafrica.org`. Browser returned HTTP200/title AISCA with an email-first login screen (Email, Remember me, Continue). No email entered or login attempted. Initial public crawler failure was superseded by successful browser access. Public-entry receipt `phase0/drill_receipts/census_operational_v1/execution_recovery/aisca_portal_public_entry_20260925T1921Z.json`.

Provider/URL are now KNOWN. Portal sign-in credentials, authentication method after email, account privileges, VM console/gateway availability remain UNVERIFIED. Need authorized portal account access or owner-operated authenticated console; do not use the VM workbook or app demo account as guessed portal credentials. Earlier missing-URL statements below describe the PDF alone, not the current owner-supplied information.

Date: 2026-09-25. Owner supplied `AISCA_GPU_Access_Guide (1).pdf` saying "Here is the integration guide" after authorizing an entirely new Akki SSH identity.

## Intake

Original retained in restricted mode0600 custody because screenshots include example connection credential fields. Path and SHA in `phase0/drill_receipts/census_operational_v1/execution_recovery/aisca_access_guide_intake_20260925T191908049373Z.json`. Original SHA256 `0f6b6e0f692494e18a65df655fddf48f45839005dc7aa6b988239b8f90e157f3`. No raw credentials, IPs, personal addresses or credential-bearing links extracted to this note.

## What the owner's guide documents

- Pages1–2: AISCA and the **Rafay Console** are the provider/platform context.
- Pages3–4: Developer Hub / Virtual Machines SKU selection and **NEW VM provisioning**. The illustrated new-VM form includes an **SSH Public Key** field.
- Pages4–5: Public IP assignment and security-group allowance for customer SSH traffic.
- Page6: VM deployment outputs include host, username, password, IP, OS and ephemeral-storage fields. Values are deliberately not reproduced.

## What it does not establish

Targeted extraction found **no explicit readable portal/login base URL**, console/admin login credentials, API key, existing-VM key-update action, existing-VM Console/Serial Console menu, or serial-console recovery procedure. The guide does not document how changes to the new-VM SSH key input affect an already-running guest. Do not infer that re-running Deploy updates authorized_keys safely. Backup/persistence policy is not specified.

This identifies the provider; it does not yet provide an authenticated installation channel.

## Independently checked Rafay documentation

Source: https://docs.rafay.co/releasenotes/2026/gpupaas/v3.1-40/ — **03 Jul2026**, VM SKU / Serial Console Support.

Rafay documents serial-console support for VMs for out-of-band recovery. It explicitly requires a gateway deployed on a machine in the data center with network connectivity to the server hosting the VMs. **AISCA's installed version, gateway availability, user permissions and console availability have NOT been verified.** General capability is not proof of this tenant's access. No generic Rafay login URL is substituted for the unknown AISCA portal URL.

## Safe next action

Obtain the actual AISCA/Rafay portal URL and an authorized existing-VM console/admin route (owner can run a public-key enrollment bundle, or AISCA administrator can perform it). Check serial console on **existing akki-vm / akki-vm-ii**, not new machine creation. If unavailable, provider-assisted public-key enrollment/recovery is required. New identity is already authorized; do not ask again for replacement permission.

Once route/custody is established: stage fresh key separately, enroll public key, verify new-key authentication with unchanged host pins on both hosts, activate, then remove only the superseded Akki public key. Preserve unrelated keys, VM disks, running workloads and original UI. Do not delete/redeploy VMs, enable passwords, alter security groups speculatively or revoke old access first.

No key generated/installed/removed, host disconnected/restarted/recreated, or source data read during guide assessment. No application code changed. Existing live evidence remains: both pinned hosts advertise publickey only; user authentication/T14 remain unverified/blocked. This document review is not a functional test pass or increased platform-completion percentage.