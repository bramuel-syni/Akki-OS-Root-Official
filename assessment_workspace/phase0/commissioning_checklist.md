# Phase 0 · Commissioning Checklist

**Source:** Build Order 01 §6 (owner channel, 2026-08-14, verbatim in `STATE/DECISIONS.md`).
**Owner:** human-executed on the AISCA Rafay console + VM. Not scriptable from this pod.
**Deliverable:** commissioning record ledgered per §6 acceptance list.

---

## Pre-flight (must pass before any provisioning)

- [ ] AISCA Rafay console shows the HSS volume visible at ~30 TB.
      **STOP AND ESCALATE if smaller.** Do NOT adapt.

## Provisioning (per SOP + Build Order §6 bindings)

Create the VM with **all four** at creation time (post-creation attach is not possible for HSS):

- [ ] GPU: **4× H200 NVLink**.
- [ ] HSS: attached at creation, target ~30 TB.
- [ ] Public IP: **true** (SSH allowlist enforcement on our end).
- [ ] Ubuntu 24.04 image per SOP.

Once provisioned, receive the host IP + VM user name. Provide our egress IP to
AISCA console operators for allowlist:

- [ ] Egress IP from `backend/tools/report_egress_ip.sh` (current: **34.16.56.64**)
      added as `/32` to VM SSH allowlist. **Only allowlist us.**

## Credential hardening (before any data moves)

- [ ] SSH key-only. Root/bootstrap passwords retired (probe from outside to
      confirm dead — see below).
- [ ] `PasswordAuthentication no` in `/etc/ssh/sshd_config` and confirmed by
      `sshd -T | grep passwordauth`.
- [ ] Private key delivered to us under named custody — placed at
      `SSH_PRIVATE_KEY_PATH` in `backend/.env` (NEVER commit; NEVER in STATE/).
- [ ] `VM_HOST`, `VM_USER`, `SSH_ALLOWLIST_EGRESS_IPS` set in `backend/.env`.
- [ ] External probe from a machine NOT on the allowlist returns:
      `Permission denied (publickey)` — password auth confirmed dead.

## Acceptance (per Build Order §6 verbatim — six checks)

Run `backend/tools/run_acceptance_via_seam.py` from this pod after credentials
land. It executes each check THROUGH the compute seam (governed handoff,
ledgered, receipt-stamped):

- [ ] `hss.check` — HSS mounted at ~30 TB.
- [ ] `hss.writable` — write test file survives.
- [ ] Deliberate restart via Rafay console. Re-run `hss.writable` post-restart —
      the test file must STILL be present (routine restart does NOT wipe HSS or
      ephemeral per vendor answer on record).
- [ ] `gpu.nvidia_smi` — reports **4× H200**.
- [ ] `gpu.nvlink` — NVLink topology active (NOT absent).
- [ ] `ephemeral.present` — ephemeral disk visible + marked scratch-only.
- [ ] `sshd.no_password` — `PasswordAuthentication no` confirmed.

Escalate-and-stop, never adapt, on:
- HSS absent / undersized.
- NVLink absent.
- Password auth still live.
- Ephemeral persistence claim contradicted by restart test.

## VM as declared infrastructure actor

The compute seam refuses to execute if the VM is not declared. `run_acceptance_via_seam.py`
captures the declaration before executing:

```python
ActorDeclaration(
    actor_id="infrastructure.vm.<host>",
    actor_kind="infrastructure",
    objective="Archive processing and speech-model training.",
    capabilities=["compute", "hss_storage", "gpu_training"],
    risks=["bulk_data_custody", "external_location"],
    scope=["archive.ingestion", "training.speech_kenyan"],
    lawful_basis="build_order_01_2026-08-14",
)
```

## Deliverable at Phase-0 exit

- Signed commissioning record JSON in `phase0/commissioning_records/<UTC>.json`.
- Restart-survival evidence (write-test present pre/post restart).
- Two-week checkpoint deadline pinned in `STATE/PINS.md`.

## Blocked-until

The following remain BLOCKED until this checklist is fully green and the
attachments (reference screenshot + v7 brief + AISCA GPU Access Guide PDF)
land in the workspace:

- Phase 2 slice run (archive-source hashing, admission, transfer to HSS).
- A4 operating surface (needs fixtures).
- Track-B console items (needs fixtures).
- Watch Console §6 verbatim consumption (needs v7 brief §6).

Nothing else in Phase 1 A0/A1 blocks on this.
