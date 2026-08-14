# aisca_sop_extraction.md

**Source:** `fixtures/AISCA_GPU_Access_Guide.pdf` · sha256 `0f6b6e0f692494e18a65df655fddf48f45839005dc7aa6b988239b8f90e157f3` · 535,169 bytes · owner-supplied 2026-08-14.
**Document title (extracted):** *AISCA – GPU Access*.
**Version/date on document:** not specified.
**Scope (extracted):** Section 1 only — *"Creating a Virtual Machine (Developer Hub)"*. Provisioning + network setup + credential handoff. No sections on operations, restart semantics, deprovisioning, HSS management post-creation, or hardening.

---

## 1 · Verbatim / near-verbatim SOP items (in order)

Numbering matches figure sequence in the PDF.

| # | Step | Preconditions / Must | Warnings / Do-Not | Config values in step |
|---|---|---|---|---|
| SOP-1 | Open the Services menu (grid icon, top left) and select Developer Hub. | — | — | — |
| SOP-2 | In Developer Hub, under Compute in the left sidebar, select Virtual Machines. | — | — | — |
| SOP-3 | On the Virtual Machines page, click `+ New Virtual Machine`. | — | — | — |
| SOP-4 | In the Virtual Machines Catalog, click `Read Me` to review the resource's specs, then click `Select` to choose that SKU. | — | — | **SKU shown in Read Me (Figure 9):** `1× H200` · `20 vCPU` · `240 GB RAM` · `3 TB local ephemeral` · `75 GB root disk (High Speed Storage)`. |
| SOP-5 | Enter required info: Name, Workspace, (attach High Speed Storage). | HSS must EXIST as a resource before it can be attached at VM creation: *"No High Speed Storage options available — Create a High Speed Storage first to see options here."* | — | HSS attach dropdown is populated ONLY from pre-existing HSS resources. |
| SOP-6 | Under Network Details, set `Assign Public IP = true`, and add a Security Group rule allowing SSH from the customer's IP address(es). | *"This is an important step since access is primarily through SSH."* | — | `Assign Public IP: true` · Security Group rule: Source=`<customer IP>/32`, Rule Type=`allow`, Application=`ssh` (three entries pattern). |
| SOP-7 | Confirm VM Details (OS, GPU/CPU count, memory, boot disk, ephemeral storage) and Billing Details (Contract Term), then deploy. | — | — | `OS: Ubuntu 24.04` · `GPU Count: 1` · `CPU Count: 20` · `Memory: 240 GB` · `Boot Disk: 75 GB` · `Ephemeral Storage: 3 TB` · `Contract Term: On Demand`. |
| SOP-8 | Share the Public IP, Username, and Password with your team after provisioning completes. | *"Once deployed, the Output section shows the Host Name, Username, Password, Public IP, Private IP, OS, and Ephemeral Storage."* | — | Output panel discloses: Public IP, Private IP, Username, **Password**, OS `ubuntu24.04`, Ephemeral Storage. |

## 2 · Silences in the SOP (explicit absences — do-not-invent)

The PDF's Section 1 is silent on:

- Restart / reboot behaviour; nothing on what survives a routine restart.
- Deprovisioning; nothing on ephemeral wipe as a loss event.
- HSS attach after VM creation (SOP is silent; only shows attach-at-creation flow).
- SSH key installation, `authorized_keys`, or key-only auth switch.
- `PasswordAuthentication no` configuration in `sshd_config` or equivalent.
- External probe to confirm password auth is dead.
- Bootstrap credential retirement.
- Any acceptance / verification test (no `nvidia-smi` check, no `df -h` HSS check, no mount survives-restart check).
- Multi-GPU / NVLink SKUs (only the 1×H200 SKU is documented in Figure 9).
- 4× H200 · 84 vCPU · 948 GB RAM · 12 TB ephemeral SKU (not present).
- ~30 TB HSS volume (not present as a size figure).

Recorded per Build Order 01 discipline: absence is a finding, not a blank.

---

## 3 · Reconciliation against Build Order 01 §6 — CONFLICTS FOUND

Order §6 bindings, item-by-item, checked against SOP text:

| Binding (Order §6) | SOP status | Reconciliation | Grade |
|---|---|---|---|
| VM = **4× H200 NVLink · 84 vCPU · 948 GB RAM · 12 TB local ephemeral · Ubuntu 24.04** via AISCA Rafay console. | SOP Read Me (Figure 9) documents ONLY `1× H200 · 20 vCPU · 240 GB RAM · 3 TB ephemeral`. Ubuntu 24.04 matches. | The SOP as-written cannot produce the Order-§6 environment. Either a different Catalog SKU exists that isn't in this PDF, OR the 4×H200 SKU must be created through a channel not covered by this SOP, OR the Order §6 environment is unavailable in this Catalog. | **CONFLICT A — HARD** · ESCALATED per Q2(a). |
| **~30 TB persistent HSS volume** shared to org; HSS cannot be attached after VM creation, selection at creation is the go/no-go. | SOP documents `75 GB root disk HSS` at the VM level; no ~30 TB volume figure. HSS attach flow is pre-created-then-selected-at-creation (compatible with "at-creation is the go/no-go" if post-creation attach truly does not exist). | The Order's ~30 TB size does not appear in SOP; owner asserts this size is available. Order's post-creation-attach prohibition is compatible with the SOP's silence but not confirmed by it. | AMBIGUOUS — flagged for owner confirmation whether the ~30 TB HSS is a separate provisioning path from Figure 10 or an inline resize. |
| **Key-only SSH; password auth disabled and confirmed dead by external probe; bootstrap credentials retired.** | SOP step SOP-8 hands over Public IP + Username + **Password** as the connection artifact. SOP contains no step to install SSH keys, disable password auth, or probe. | Order's own credential-hardening clause is the reconciliation. The SOP is INCOMPLETE, not doctrinally opposite: the SOP terminates at bootstrap-credential handoff; the Order carries the hardening past that point. Still: the SOP as-written invites a password-auth-live path unless the Order's hardening steps are added inline. | **CONFLICT B — PROCEDURAL** · ESCALATED per Q2(a) — owner must confirm the hardening steps are inserted between SOP-8 and any data movement, or accept that this Guide is insufficient for governance. |
| **Allowlist pinned to owner egress IPs /32.** | SOP-6 says allow SSH from `<customer IP>/32`. | Compatible: matches Order §6 verbatim. | AGREES. |
| **Vendor answers on record: routine restart does NOT wipe ephemeral (deprovisioning is the loss event).** | SOP silent on restart / deprovisioning. | Vendor answer is off-document (owner recorded in Order §6). SOP does not contradict. | COMPATIBLE (silent). |
| **Pre-flight: HSS visible ~30 TB, smaller = stop-and-escalate.** | SOP silent on pre-flight; no acceptance/verification step in Section 1. | Order §6's Phase-0 `acceptance.sh` is the pre-flight; SOP does not cover it. | COMPATIBLE (silent). |
| **Acceptance before any data moves, ledgered as commissioning record: HSS mounted ~30 TB writable; write-test survives one deliberate restart; nvidia-smi shows 4× H200 NVLink active; ephemeral present scratch-only; password auth probed dead.** | SOP silent on all five checks. | Same as above: Order §6's `acceptance.sh` covers this. | COMPATIBLE (silent) — but the `acceptance.sh` presumes the 4×H200 NVLink SKU which is CONFLICT A. |

**Overall reconciliation result: TWO conflicts (A HARD, B PROCEDURAL), one AMBIGUOUS, four COMPATIBLE-BUT-SILENT. Escalated per Q2(a); no owner-favoured interpretation applied.**

---

## 4 · Concrete owner-side questions raised by the reconciliation

Q-SOP-1 (blocks Phase-0 start): The SOP Catalog documents a `1× H200 · 20 vCPU · 240 GB RAM · 3 TB ephemeral` SKU. Order §6 mandates `4× H200 NVLink · 84 vCPU · 948 GB RAM · 12 TB ephemeral`. What is the provisioning path for the Order-§6 SKU? Is there a Catalog entry not shown in this PDF, or is a different channel required?

Q-SOP-2 (blocks Phase-0 start): Is the ~30 TB HSS created through the same Figure 10 attach flow (create-HSS-first-then-attach-at-VM-creation), or through a separate provisioning path? Confirm the "cannot attach after VM creation" vendor answer that appears in Order §6 (SOP is silent).

Q-SOP-3 (blocks first data movement): The SOP-8 handoff artifact is Public-IP + Username + **Password**. Are the Order §6 hardening steps (install SSH keys · disable password auth · external probe · retire bootstrap credentials) executed by owner-side hands before the compute seam gains admission, or by the compute seam through `acceptance.sh`? If the latter, `acceptance.sh` must extend to cover them — currently it does not.

Q-SOP-4 (informational): Vendor answers on restart/deprovisioning that Order §6 cites are not in the SOP. Are they in a companion document, a support ticket, or verbal channel? Recorded here as an external-source pin for future audits.

---

## 5 · Effect on Phase 0 / Phase 3 materials — HELD PENDING OWNER RULING

**Frozen until conflicts A + B are ruled:**

- `phase0/acceptance.sh` remains at its current shape (probes for 4×H200 NVLink · ~30 TB HSS · restart survives · password-dead) — DO NOT modify to accommodate the 1×H200 SKU; owner has not ruled that fallback is acceptable.
- `phase0/commissioning_checklist.md` — the SKU line stays at the Order §6 spec.
- Phase-3 runbook is unwritten (Phase-3 opens only after Phase-2 slice results). No SOP-derived text lands there until Q-SOP-1..Q-SOP-3 are ruled.

**Cleared for continuation:**

- Fixture-processing cycle for the v7 brief (interface stream) — proceeds; the SOP conflicts do not touch interface DoDs.
- Corrections to BUILD_STRATEGY.md HEAD (§10.F, XL count, five-consoles) — proceeds; these are document defects unrelated to the SOP.

## 6 · Re-open condition

- If the SOP is re-uploaded in a later version showing the 4×H200 SKU or the ~30 TB HSS path or the hardening steps, this file re-extracts and the conflict rows above re-grade.
- If owner rules that the current SOP is authoritative and Order §6 SKU/hardening bindings relax: append a "SOP-A supersession" row and update `acceptance.sh` accordingly.
- Q-SOP-1..Q-SOP-4 are also logged in `notes/fidelity_ledger.md` as new rows FL-P2-03 and FL-P2-04 (see ledger for exact row shape).
