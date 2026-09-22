---
card_id: TENANT_SEPARATION
title: CP-TENANT-SEPARATION · two legal entities, two tenants, zero mixing
ratified_at_utc: 2026-09-22T03:25:00Z
ratified_by: owner ("TWO OWNER DELIVERIES" 2026-09-22T~03:2XZ · Part 2 · verbatim order · §6.8 · this order is the GO)
card_sha256: 3aefe137ebf33ac86e4a7a21603a7d5fee9f276009eab69416a097375d5e24dc
milestone_status: DRAFTED · pinned before the first RED test per owner directive verbatim ("Objective card TENANT_SEPARATION drafted from this text, pinned before the first RED test")
sequence_gate: opens AFTER CENSUS-SURFACE UI ships post-R-91 ε-apply (horizon 2026-09-23T03:23:15Z NO EXPEDITE); interleaves with F→C→D→E census lanes + S4a + Order B / Q-1 as compute allows
---

# TENANT_SEPARATION · CP-TENANT-SEPARATION objective card

Owner order verbatim (2026-09-22T~03:2XZ · "TWO OWNER DELIVERIES · Part 2"):

> "ORDER — CP-TENANT-SEPARATION · two legal entities, two tenants, zero mixing
>
> Under §6 standing authority; §6.8 applies — this order is the GO. Objective card TENANT_SEPARATION drafted from this text, pinned before the first RED test."

## OBJECTIVE (owner verbatim · §1)

Every record, source, key, receipt, licence and principal on the platform belongs to exactly one of four tenants, and no principal of one can see, list, read or act on another's. RMS and DigiCow are separate legal entities and are separated at every layer canon names: tenant (B.2), trust domain (PRIN-7, PRIN-9, D-18), Ledger (B.4 per tenant), context key (C.13), licence (ENT-5).

## MUST DO (numbered per owner order verbatim)

### 2. Tenants and principals

- **RMS** — organisation principal, own trust-domain identifier, own Ledger, own context key, own licence.
- **DIGICOW** — same, independently.
- **AKKI-TEST** — a dedicated test tenant for systems testing. **Synthetic data only. Never holds RMS or DigiCow content.**
- **AUDIT-FIXTURE-20260921** — as already exists; unchanged.

Individuals are seats under their organisation (PRIN-1). A person who acts in two tenants is two principals — no principal spans tenants. Every principal is admitted by named authority (PRIN-2); no self-admission.

### 3. Data assignment — every source bound to one tenant, by registration, not by convention

- **RMS**: Weego, USSD, Citizen Digital, Visitors (MySQL); NAS 16 channels (SMB); OBS `google-transcripts`; Razuna/Newsvault; GaussDB/Viusasa when its credentials land.
- **DigiCow**: `digicow_live`, `ndume`; the AWS account when its credentials land.

Each connector record, each census artefact (`census_0001/0002` → **DIGICOW**; Item-3 receipts → **RMS**), each `source_inventory` row, each stratified sample, each cost receipt carries its `tenant_id` via the `akki.data` primitive — auto-injected, never caller-supplied (M11, AKKI-DATA-001). A source with no tenant does not exist to the platform.

### 4. DAP activated on both tenants, separately

Per tenant:
- The six crossing profiles enabled per **DAP-25** — every custody-class/operation combination defaults unavailable until the owner grants it.
- A licence object (**ENT-5**).
- A catalog view.
- A release budget (**DAP-35**) at the DEFAULT value, tagged pending R-7.
- An approving authority (**DAP-14**).

**The named approving authority is a tier-4 fork per tenant — bank both to `STATE/DESK_QUEUE.md`; until named, no controlled request executes (DAP-14 holds by construction; nothing is defaulted).**

### 5. Owner oversight — the data owner sees what the customer is doing

One screen family on the tenant console, per tenant, for the estate owner's principals only:
- Every party admitted under the tenant, with mandate and posture (**DAP-1**).
- The approvals queue — pending, decided, expired — with decision, reason and deciding identity (**DAP-15**; the approver is visible here and only here).
- Cumulative extraction history per party, queryable (**DAP-24**).
- Every receipt: operation, units or scope, quantity, terms identifier (**DAP-21**).
- Release-budget consumption against the ceiling (**DAP-35**) — shown to the owner, never to the party.
- Standing approvals in force (**DAP-17**).
- Suspend-in-one-act (**DAP-27**).

**Nothing in this view crosses tenants.** An RMS owner sees RMS parties and nothing of DigiCow, and the reverse.

### 6. Admin account for systems testing — a principal, not a bypass

**AKKI-TEST** owner and seats hold full rights inside AKKI-TEST only.

A **platform-operator** principal holds control-plane visibility — metadata, identity, scheduling, metering (**D-18**) — and:
- **no read** of any tenant's source content
- **no write** to any tenant's Ledger
- **no ability to approve** any tenant's request

Its actions are receipted like any principal's. **Any admin capability that would read RMS or DigiCow content is out of spec.**

### 7. UI/UX unchanged

Existing architecture, flow and feel per the Front End Integration Brief and the bound prototype: five-stage pattern, FE §2 laws, refusal card, honest-gap strings. Every new string is a Content Registry entry (**CON-1**); the oversight screens' headline slots are ranked per **CON-15**. Tenant context is set at sign-in from the principal and never selectable in the UI.

### 8. Post-sweep — mixing is impossible, then proven

**Tests first, RED, then the sweep, then the seal:**

1. Every row in every collection carries a `tenant_id` in the four; zero rows without; zero rows whose estate/connector tenant disagrees with the row's.
2. `akki.data`: a cross-tenant read refuses `AKKI-DATA-001`; a cross-tenant write refuses; a query without tenant context refuses (no default tenant).
3. Principal of RMS against every DigiCow surface and route — list, detail, submit, stop, retry, entitlement reads, oversight — refuses without confirming existence; and the reverse; and AKKI-TEST against both.
4. Every credential in the plane bound to exactly one trust domain (**PRIN-7**); every Ledger row carries its trust-domain identifier (**PRIN-10**); the two Ledgers share no writer, chain or store.
5. Census artefacts, samples and receipts re-read from disk and confirmed under the correct tenant; **RMS Item-3 receipts and DigiCow census #1/#2 named explicitly in the sweep receipt**.
6. Sweep result written as a receipt: rows checked per collection, violations found (expected zero), remediations if any, sha-pinned in `PINS.md`.

## MUST NOT (owner-derived bans · additive to owner §10 BOUNDS)

- **No cross-tenant data movement of any kind during the work**, including for testing (owner §10 verbatim). `canon_ref: owner order §10 + AKKI-DATA-001 sealed refusal code (M11).`
- **No sealed-file edit — adapters and additive modules only** (owner §10 verbatim). `canon_ref: owner order §10 + SO §3.8 additive-only.`
- **No admin-tier capability that would read RMS or DigiCow content** — the platform-operator principal is control-plane only (§6 verbatim: "Any admin capability that would read RMS or DigiCow content is out of spec"). `canon_ref: owner §6 verbatim + D-18 platform-operator scope.`
- **No principal spans tenants** — a person acting in two tenants is two principals (§2 verbatim). `canon_ref: owner §2 verbatim + PRIN-1 seat-principal + PRIN-7 trust-domain binding.`
- **No self-admission of principals** — every principal admitted by named authority (§2 verbatim). `canon_ref: owner §2 verbatim + PRIN-2 named-authority admission.`
- **No source without a tenant** — a source with no `tenant_id` does not exist to the platform (§3 verbatim). `canon_ref: owner §3 verbatim + M11 AKKI-DATA-001 auto-injection contract.`
- **No approving-authority default** — DAP-14 holds by construction; nothing is defaulted (§4 verbatim). `canon_ref: owner §4 verbatim + DAP-14 named-authority requirement + SO §6.4 NOTHING-BEYOND on tier-4 forks.`
- **No tenant-selectable UI** — tenant context is set at sign-in from the principal and never selectable (§7 verbatim). `canon_ref: owner §7 verbatim + PRIN-12 forbid header identity.`
- **No downward baseline shrink or silent rebaselining** during CP-TENANT-SEPARATION landing. `canon_ref: SO §3 ratchet monotonic-up.`
- **No zero-push discipline breach** — local commits only, three-repo. `canon_ref: SO §4 zero push + Owner Clarification 1 (2026-08-14).`

## EXIT (owner verbatim · §9 + citation to existing sealed sealed tenant invariants)

Per owner §9 verbatim:

- The sweep receipt at zero violations.
- The isolation test IDs green in the ratchet.
- Both tenants' DAP surfaces reachable by their own principals only.
- The oversight screens rendering per §5.
- The two approving-authority forks in the queue.
- Seal per §3.3, full pre-seal sweep, and continue.

**Sealed tenant-boundary invariants already on disk at wave-open (must remain GREEN through CP-TENANT-SEPARATION landing; citation targets for the pre-Commit-A sweep gate)**:

- tests/invariants/test_p6_cp3_cross_tenant_access_suite.py::test_refuses_on_tenant_context_gate
- tests/invariants/test_p6_cp3_cross_tenant_access_suite.py::test_refuses_on_task_scope_gate
- tests/invariants/test_p6_cp3_cross_tenant_access_suite.py::test_refuses_on_permission_evaluation_gate
- tests/invariants/test_p6_cp3_cross_tenant_access_suite.py::test_refuses_on_scheduler_admission_gate
- tests/invariants/test_p6_cp3_cross_tenant_access_suite.py::test_refuses_on_metering_gate
- tests/invariants/test_p6_cp3_cross_tenant_access_suite.py::test_refuses_on_audit_visibility_gate
- tests/invariants/test_p6_cp3_cross_tenant_access_suite.py::test_fail_fast_order_tenant_context_first
- tests/invariants/test_p6_cp3_cross_tenant_access_suite.py::test_refusal_hierarchy

**New CP-TENANT-SEPARATION invariants to land at wave-open** — see the sibling `PLANNED INVARIANTS` section below (moved out of EXIT so the `test_every_cited_exit_test_file_exists_on_disk` invariant only scans citations to files already on disk; the future RED-first authoring at CP-TENANT-SEPARATION wave-open post-R-91 remains documented but is not counted as banked exit evidence at this Commit-B).

**Pre-Commit-A gate**: BASELINE_GUARD=1 PYTHONHASHSEED=0 double-sweep byte-identical (SO §3).

## PLANNED INVARIANTS (RED-first · authored at CP-TENANT-SEPARATION wave-open post-R-91)

Files below do not exist yet on disk (by design — RED-first mandate authors them AT wave-open, not before). Exit evidence for MUST-DO 2–8 at that wave will list them under this card's EXIT section once the file is on disk:

- test_cp_tenant_separation.py :: test_four_tenants_declared_verbatim (MUST-DO 2)
- test_cp_tenant_separation.py :: test_every_source_has_tenant_id (MUST-DO 3)
- test_cp_tenant_separation.py :: test_dap_activated_per_tenant (MUST-DO 4)
- test_cp_tenant_separation.py :: test_oversight_screens_per_tenant_no_cross (MUST-DO 5)
- test_cp_tenant_separation.py :: test_platform_operator_no_content_read (MUST-DO 6)
- test_cp_tenant_separation.py :: test_no_tenant_selectable_ui (MUST-DO 7)
- test_cp_tenant_separation.py :: test_isolation_sweep_zero_violations (MUST-DO 8)
- test_cp_tenant_separation.py :: test_two_approving_authority_forks_banked (MUST-DO 4 + Tier-4 forks)

## STOP (milestone-specific stop conditions per SO §6.2)

- Any attempt to read across tenants during CP-TENANT-SEPARATION landing — even for testing — triggers immediate halt (owner §10 verbatim ban; AKKI-DATA-001 sealed refusal is the boundary).
- Any sealed-file edit surfaced during the wave (SO §3.8 additive-only violation).
- Any principal admitted without named-authority (PRIN-2 violation).
- Any cross-tenant leak surfaced by the isolation sweep (§8 EXIT clause 8.1: expected-zero violations).
- Any DAP surface reached by the wrong tenant's principal (§8 EXIT clause 8.3 refusal invariant).
- Any Ledger writer / chain / store shared across tenants (§8 EXIT clause 8.4).
- Any approving-authority defaulted or auto-named in code (§4 verbatim ban).
- Any downward ratchet-floor bump (SO §3 monotonic-up).

## BOUNDS (owner verbatim · §10)

- SO §3.3, §3.8, §3.10 as amended.
- §4 zero push.
- §4.1 §E.
- **No sealed-file edit — adapters and additive modules only.**
- **No cross-tenant data movement of any kind during the work, including for testing.**

## ANCHORS

- Owner order verbatim 2026-09-22T~03:2XZ (this-card authority · "TWO OWNER DELIVERIES · Part 2").
- **B.2** · tenant discipline.
- **PRIN-1, PRIN-2, PRIN-7, PRIN-9, PRIN-10, PRIN-12** · principal model.
- **B.4** · per-tenant Ledger.
- **C.13** · context key.
- **ENT-5** · licence object.
- **DAP-1, DAP-14, DAP-15, DAP-17, DAP-21, DAP-24, DAP-25, DAP-27, DAP-35** · DAP lifecycle.
- **CON-1, CON-15** · Content Registry.
- **D-18** · trust-domain identifier + platform-operator scope.
- **AKKI-DATA-001** · sealed cross-tenant refusal code (M11).
- **SO §3.3** · 3-Commit Seal · **§3.8** additive-only · **§3.10-α** Final[str] closed-vocab.
- **§4** zero push · **§4.1 §E** credential custody read discipline.
- **§6.2** · objective card structure · **§6.4** NOTHING-BEYOND · **§6.8** "No GO exists" (this order is the GO).
- Sealed sibling: `tests/invariants/test_p6_cp3_cross_tenant_access_suite.py` (existing sealed tenant-boundary refusal suite; the new CP-TENANT-SEPARATION invariants ADD to this surface, they do not replace).
- Sealed sibling: `services/akki_data/*` (`akki.data` primitive · auto-injects `tenant_id` per M11 · never caller-supplied).
- Sealed sibling: `services/dap_lifecycle/*` (DAP-1..38 lifecycle · already present per R-95..R-97 seal chain).

## TIER-4 FORKS TO BANK AT WAVE OPEN

- **APPROVING AUTHORITY · RMS tenant** — DAP-14 named authority for RMS not yet identified; must be named before RMS controlled requests execute. Bank to DESK_QUEUE with options + recommendation at wave open per SO §6.8.2.
- **APPROVING AUTHORITY · DIGICOW tenant** — same shape for DIGICOW. Bank sibling entry.

## SEQUENCING

1. **CENSUS-SURFACE-A remaining backend** (this-Commit-A" seals it) + **post-R-91 ε-apply UI** at horizon `2026-09-23T03:23:15Z` (banked UI specs land byte-identically to `pod_shell/frontend/src/App.js` mirror).
2. **OPEN CP-TENANT-SEPARATION** — this-card pinned pre-first RED · MUST-DO 2 admits four tenants → 3 registers real sources per tenant → 4 lands DAP surfaces per tenant → 5 lands oversight screens (Content Registry entries) → 6 lands platform-operator principal → 7 renders unchanged UI → 8 RED sweep proves isolation → 9 EXIT evidence.
3. **Census lanes F→C→D→E · S4a-DIGICOW-RDS · Order B/Q-1** continue interleaved as compute allows.

## POST-RATIFICATION

Card body IS the ratification text (owner order §6.8 verbatim = this-card content). No further owner ack required. First RED test opens on card's `card_sha256` pin (computed at wave open).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
