---
card_id: TENANT_SEPARATION
title: CP-TENANT-SEPARATION · two legal entities, two tenants, zero mixing
ratified_at_utc: 2026-09-22T03:25:00Z
ratified_by: owner ("TWO OWNER DELIVERIES" 2026-09-22T~03:2XZ · Part 2 · verbatim order · §6.8 · this order is the GO)
card_sha256: PENDING-PRE-FIRST-RED-TEST-COMPUTATION
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

## EXIT (owner verbatim · §9)

- The sweep receipt at zero violations.
- The isolation test IDs green in the ratchet.
- Both tenants' DAP surfaces reachable by their own principals only.
- The oversight screens rendering per §5.
- The two approving-authority forks in the queue.
- Seal per §3.3, full pre-seal sweep, and continue.

## BOUNDS (owner verbatim · §10)

- SO §3.3, §3.8, §3.10 as amended.
- §4 zero push.
- §4.1 §E.
- **No sealed-file edit — adapters and additive modules only.**
- **No cross-tenant data movement of any kind during the work, including for testing.**

## CANON ANCHORS

- Owner order verbatim 2026-09-22T~03:2XZ (this-card authority).
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
- **§6.8** "No GO exists" (this order is the GO).

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
