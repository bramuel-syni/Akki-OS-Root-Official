# R-85 HUNT · BlockedKind three-vs-four/five reconciliation receipt

**Timestamp**: 2026-09-20T~17:50Z
**Wave**: CP-PARTY-HALTED-ADDITIVE-SUB-WAVE (R-85 · pre-Commit-A HUNT)
**Purpose**: Reconcile owner's "existing four kinds" phrasing against sealed `BlockedKind` enum (3 members) and journey v2's "five kinds" text before touching `blocked_kinds.py`.
**Owner directive verbatim** (this-session): "Superseding-rename is NOT an available reading (the owner ruled 'one new block_kind value... no change to the existing kinds' — party_halted is additive, never a rename). If suspended is absent or the mapping is unclear: bank FORK-BLK-KINDS, stop on that half only, proceed with the party_halted additive build as ruled."

## Facts established this-hunt

### F1 · Sealed enum members (byte-verified at commit `6af89e3` on `programme/track-a`)

`repos/Extraction-Akki/backend/services/dap_lifecycle/blocked_kinds.py` lines 31-36:

```python
class BlockedKind(enum.Enum):
    """The 3 kinds of Blocked · request / check / estate."""

    request = "request"
    check = "check"
    estate = "estate"
```

**Count**: 3 members. Docstring literally states "The 3 kinds".

### F2 · Journey v2 (owner drop `20260920T1600Z`, ingested at `CP-CONTENT-REGISTRY-INGEST-DROP` `6d910bbe`)

- **§2 line 30**: "**Five kinds**, and the drawer states which: `request`, `check`, `estate`, `suspended`, and `party_halted`."
- **§11 line 207**: "**`Blocked` has five kinds**, not one flat state: `request`, `check`, `estate`, `suspended`, and `party_halted`, both added later."
- **§Whatchanged line 239**: "**Added a fourth `Blocked` kind, `suspended`**, for DAP-27's owner-suspension path. It doesn't share the other three kinds' shape: no reason field, and its progress-indicator treatment depends on `blocked_from_status`."
- **§Whatchanged line 240**: "**Added a fifth `Blocked` kind, `party_halted`**, for a party stopping their own `Executing` request. Not a scope extension of `Withdrawn` — [...] Closest in shape to `suspended`, but party-triggered rather than owner-triggered."
- **§Whatchanged line 241**: "**Partial compute on a halt is billed, prorated, entirely on the backend.** No DAP-21 receipt — that rule holds everywhere, unchanged. [...] Scoped to party-initiated halts only, not `check` or owner-triggered `suspended`."
- **§11 line 404 (Data payload for Blocked drawer)**: "`block_kind` (`request` / `check` / `estate` / `suspended` / `party_halted`), `blocked_from_status` (`in_approval` / `executing` / `ready` — populated only when `block_kind` is `suspended`; always `executing` when `block_kind` is `party_halted`, so not separately tracked), `block_reason` (party-facing, recorded once; absent for `estate`, `suspended`, and `party_halted`), `block_ref` (absent for `estate` only), `blocked_at_stage` [...], `blocked_by` (individual user — `party_halted` only, same name-disclosure rule as `Withdrawn`'s `withdrawn_by`), plus the sign-off fields below."

### F3 · `suspended` structural presence at lifecycle layer (NOT as BlockedKind member)

Grep in `services/dap_lifecycle/`:

- `services/dap_lifecycle/escrow.py` — Q5 RULED module (owner R-78) · "Output held in escrow on suspension · Ready-on-lift · termination destruction = receipted Ledger event retaining artefact hash".
- `services/dap_lifecycle/fail_closed.py::q5_suspension_from_ready()` (line 104) — returns escrow-entry summary with `"escrowed": True, "ready_on_lift": True, "termination_destroys_but_retains_hash": True`.
- `services/dap_lifecycle/suspension_notices.py` — R-78 minimal-disclosure notices (org admin + affected submitters only, per DAP-27).
- Zero `BlockedKind.suspended` enum member anywhere in codebase (grep-negative confirmed).

### F4 · `party_halted` structural absence

Grep in `services/`, `contracts/`, `tests/`:

```
$ grep -rn "party_halted\|party.halt\|halt.party" services/ tests/ 2>/dev/null
(zero results)
```

Genuinely absent. No prior mention in any module or test.

## Reconciliation

### Mapping question (FORK-BLK-KINDS)

The three-vs-four/five discrepancy resolves to a **mapping ambiguity** on `suspended` — journey v2 introduces `suspended` as the fourth `BlockedKind` enum member (Block-drawer surface layer), but the existing code has `suspended` semantics scattered across escrow.py + suspension_notices.py + fail_closed.py::q5_suspension_from_ready() (lifecycle module tree layer).

Two candidate readings, both unable to satisfy owner "one new block_kind value... no change to the existing kinds":

- **Reading A · Q5-module-tree-satisfies-BlockedKind.suspended**: If the existing escrow + suspension_notices + q5_suspension_from_ready are treated as the "fourth kind" that owner references, then journey v2's `suspended` line 239 is already satisfied structurally, and only `party_halted` needs adding — matching owner's "one new block_kind value". Under this reading, an enum-layer `BlockedKind.suspended` addition would be a **surfacing rename** (moving the concept from module-tree layer to enum layer), which owner explicitly forbids.
- **Reading B · BlockedKind.suspended-absent-and-required-first**: If `BlockedKind.suspended` is understood at the enum layer (matching journey v2 line 404 data payload where `block_kind` is one of five string values `request / check / estate / suspended / party_halted`), then adding BOTH `BlockedKind.suspended` AND `BlockedKind.party_halted` this-wave contradicts owner "one new block_kind value". Under this reading, `BlockedKind.suspended` would need its own separate wave (call it R-84-follow-on-BLK-SUSPENDED or R-85.5) before or alongside `party_halted`.

Neither reading is unilaterally resolvable without owner ruling.

### Owner instruction applied verbatim

> "If suspended is absent or the mapping is unclear: bank FORK-BLK-KINDS, stop on that half only, proceed with the party_halted additive build as ruled."

**Disposition**: `suspended` **IS present at lifecycle-module-tree layer** (F3) but **ABSENT at BlockedKind enum layer** (F1). The mapping between journey v2's "fourth `Blocked` kind, `suspended`" and the existing Q5 module tree is **UNCLEAR** (Reading A vs Reading B not resolvable without owner). Therefore: **BANK FORK-BLK-KINDS · STOP-ON-THAT-HALF-ONLY · PROCEED party_halted-additive as ruled**.

## FORK-BLK-KINDS banked mid-wave

**FORK-BLK-KINDS · OPEN**: How does journey v2's "fourth `Blocked` kind, `suspended`" reconcile with the sealed 3-member `BlockedKind` enum?

Options for owner ruling:

1. **A · Q5-module-tree-satisfies-BlockedKind.suspended**: Ratify current code state · journey v2 line 239 is factually satisfied by escrow.py + suspension_notices.py + q5_suspension_from_ready() as a shape-different-but-semantically-equivalent-fourth-kind · no enum edit · journey v2 phrasing stands as spec-level-narrative-not-code-shape.
2. **B · BlockedKind.suspended-lands-before-party_halted**: Sequence a separate additive sub-wave (R-84-follow-on) to land `BlockedKind.suspended` enum member + wire escrow/suspension_notices into the surface_gate_fault() dispatch path · then R-85 lands `BlockedKind.party_halted`.
3. **C · BlockedKind.suspended-AND-BlockedKind.party_halted-both-land-at-R-85**: Owner ratifies two-additions-this-wave as exception to "one new block_kind value" phrasing, treating that phrasing as approximate rather than binding · this-wave lands both.
4. **D · Something else** the owner has in mind that this desk hasn't enumerated.

**Status**: STOP-ON-THAT-HALF-ONLY (per owner directive verbatim) · this-desk does not unilaterally resolve · proceed with party_halted-additive-only build this-wave as ruled.

## R-85 party_halted-additive build proceeds

Per owner directive verbatim ("proceed with the party_halted additive build as ruled"):

- **Additive**: one new `BlockedKind.party_halted` enum member (F1 has 3 · this-wave lands 4th at enum layer).
- **Additive**: one new `blocked_by` field on Blocked-drawer payload (per journey v2 line 404 · "individual user — `party_halted` only").
- **Additive test**: TC-BLK-24 "partial-compute-billed-backend-only" (per journey v2 line 241 · no DAP-21 receipt · billed prorated backend only).
- **NOT touching** existing `BlockedKind.{request,check,estate}` values or their shape.
- **NOT adding** `BlockedKind.suspended` at enum layer (blocked on FORK-BLK-KINDS).
- **NOT touching** existing Q5 escrow/suspension_notices/q5_suspension_from_ready module tree.

Contract-surface-ready flag will be raised in R-85 Commit-A seal report to trigger FE-specialist dispatch for extraction-journey conformance pass on `party_halted` drawer surfaces (per journey v2 §11 lines 387/392-399 · frozen indicator + `You stopped this while it was running.` copy line + `Copy into a new request` present + `blocked_by` name shown + Sign-off carries over unchanged).

## Canon anchors verbatim

- `extraction_request_approval_journey_v2.md` (owner drop `20260920T1600Z` · custody-tracked at `CP-CONTENT-REGISTRY-INGEST-DROP` `6d910bbe`) §2 line 30 + §11 line 207 + §Whatchanged lines 239-241 + §11 line 404 (Data payload).
- `services/dap_lifecycle/blocked_kinds.py` (sealed at `CP-DAP-LIFECYCLE-BACKEND-WAVE` · code_repo head at wave-open).
- `services/dap_lifecycle/escrow.py` + `suspension_notices.py` + `fail_closed.py::q5_suspension_from_ready()` (sealed at `CP-Q-UNLOCK-SUB-WAVE` `c0f5e6d5/6fc1a99b/d5b0522f`).
- FORK-CON-INGEST-3 owner ruling verbatim (banked at STATE/DECISIONS.md R-83 SEALED · 2026-09-20T~16:45Z): "APPROVED, net-new ADDITIVE `party_halted` sub-wave — one new block_kind value + one new blocked_by field + frontend copy spec + TC-BLK-24 partial-compute-billed-backend-only".
- Owner directive this-session verbatim: "party_halted is additive, never a rename. If suspended is absent or the mapping is unclear: bank FORK-BLK-KINDS, stop on that half only, proceed with the party_halted additive build as ruled."
- SO §3.8 additive-only · SO §2.5 verbatim-docstring · SO §3.10-α option alpha structural guarantee.
