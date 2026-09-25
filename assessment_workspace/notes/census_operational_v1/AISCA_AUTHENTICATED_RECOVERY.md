# Authenticated AISCA recovery — 2026-09-25

## Final read-only checkpoint —20:06Z

The alternative edit route was assessed AFTER network settled and the storage-loading message disappeared. On **akki-vm**, the SSH Public Key field is disabled/non-editable/empty. Its enabled adjacent icon opens a configuration VALUE VIEWER; the viewer's textarea is explicitly **readOnly=true**. No typing, attribute manipulation or update/save/deploy occurred. Thus an ordinary editable key-enrollment control was not established for this account/VM. The other VM's expanded key editor was not separately inspected; do not generalize that UI finding to all accounts or VMs.

Together with independently observed console XHR502 on BOTH hosts, this blocks the two inspected enrollment paths. Portal sign-in itself WORKS. AISCA needs to restore the existing-VM console or provide an approved in-place administrator enrollment route. No more portal credentials are needed to establish this finding.

Aggregate live receipt: `phase0/drill_receipts/census_operational_v1/execution_recovery/aisca_authenticated_recovery_20260925.json`. Prepared, NOT SENT provider brief: `AISCA_PROVIDER_RECOVERY_REQUEST.md`. No new application code in this portal slice; earlier103-test suite was NOT rerun or relabeled as these live checks. New browser observations are real, not mocked.

Read-only diagnostic corroborated the observed failure but not its cause. Its assertions about precise provider version/private-edge configuration are not adopted here without independently banked source evidence. Its generic namespace/cluster commands must not be run as though this tenant's topology were known. Any VM-recreation fallback is outside owner authority and explicitly rejected.

## Authority and credentials

Owner authorized an entirely new Akki SSH identity, then supplied an updated `Compute Creds.xlsx` (artifact prefix `z8ka7rig`). Restricted source custody `/app/backend/estate_keys/gpu_hosts/AISCA_portal_credentials_20260925T193725708878Z.xlsx`; sha256 `49376d19fe4bc6510cffb1af907f2e5cb4a87ff1f272af72a9cbef6f2ab83299`. This supersedes earlier reports of missing portal credentials. No email/password/key/token value is recorded here.

Portal `https://console.cpt.aiscafrica.org`. **One email/password sign-in succeeded**; no MFA observed. Do not ask the owner for these credentials again. Protected credential/session copies in the browser-tool environment are under `/tmp/akki_aisca_private` (directory0700/files0600), separate from the app pod. Workbook was TLS-fetched there and SHA-verified against intake before parsing. Session restoration requires cookies+localStorage, loading portal HOME, waiting for initialization, then navigating Virtual Machines. A deep-link attempt returned to sign-in; home-based restoration succeeds. Do not mistake that navigation artifact for invalid credentials or repeat login blindly.

## Verified existing resources and read-only actions

- `akki-vm` and `akki-vm-ii` both appear **Running** in `akki-workspace`. This is provider state, not a GPU diagnostic or source-execution success.
- Both list action menus: **Edit Configuration**, **View Metrics**, **Delete**. Only Edit Configuration was selected; it opens existing deployment details, not a submitted configuration mutation.
- Existing details show **Open console**, **Edit**, plus Start/Stop/Reboot/Migrate/Delete controls. No destructive/lifecycle control was selected.
- **Open console exists**, correcting the earlier unknown-console-availability boundary. It opens a same-origin console tab.
- `akki-vm-ii`: initial surface check showed no terminal; follow-up network observation at19:53Z confirmed an XHR HTTP502 before any login/terminal. No canvas/xterm/input available.
- `akki-vm`: independent check at19:55Z also returned XHR HTTP502 from a console-related endpoint, zero terminal elements. No console password, client key or command was sent on either host.
- This proves failure of the observed portal console launch flow; it does NOT establish the gateway, hypervisor or provider-service root cause.
- First Edit-button lookup used a button role, but the visible control is a LABEL; corrected text-based navigation at19:58Z opened the existing Edit Virtual Machine form. Do not record the earlier locator timeout as a provider failure.
- SSH Public Key field was seen present/empty/disabled in early edit previews, but asynchronous provider-storage loading was also observed. **Permanent immutability is NOT established**; wait for readiness before concluding the field cannot be changed. No field filled, no Save/Deploy submitted. Adjacent-control inspection climbed to too-broad a container and made no click; no claim of a disabled adjacent control.

## Privacy and receipts

Typed email/password, cookies, localStorage tokens and console token URLs were not printed in structured logs. The browser tool automatically captured a post-login screenshot showing the account identifier; it did not show a password or token. Subsequent captures explicitly redact account identifiers/IPs and obscure input/terminal content. Thus do not describe ALL initial images as identifier-free. Detailed redacted browser-operation JSON receipts remain in the browser environment; their observations are banked here and in a main-workspace aggregate report.

## Current boundary

No key generated, installed, activated or revoked. No VM stop/reboot/delete/recreate, no configuration submitted, no SSH/password policy change, no estate/source-data read. Existing SSH pins/key paths remain unchanged. T14 remains0/1.

Next: finish safe read-only assessment of whether the existing form supports a genuine in-place key change, without bypassing a disabled control or submitting a redeploy. Independently diagnose the console502 from evidence. If neither route is operational, AISCA must restore the existing-VM console/admin access or provide provider-assisted public-key enrollment. Do not replace VMs to fix SSH authorization. Private-key durable custody must be established before any replacement activation.