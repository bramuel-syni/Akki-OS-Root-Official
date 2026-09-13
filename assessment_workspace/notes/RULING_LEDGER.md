# RULING_LEDGER.md — owner rulings ledger (STEP 3 close, owner directive 2026-09-08T~06:15Z)

**Created:** 2026-09-09
**Owner directives banked:** 2026-09-08T~06:15Z (STEP 3) · 2026-09-09T~11:40Z (proceed straight through) · 2026-09-13 (M0-open C3 batch-ratification; see `notes/RATIFICATION_C3_BATCH_20260913.md`)
**Ratchet floor at creation:** 3017 · **at latest reconcile 2026-09-13:** 3562

## Purpose

Every owner ruling banked verbatim in `STATE/DECISIONS.md` gets its human-readable
status row here. This ledger is the source of truth for "what's ratified, what's
default, what's coupled, what's still owner-open" — mirrored from the DECISIONS
verbatim bank without paraphrasing the ruling itself.

Categories:
- **RATIFIED** — owner explicitly approved the proposed value; binding immediately.
- **DEFAULT** — owner set a working value with `DEFAULT-class · revisable on evidence` posture; wired now, may change on later ruling.
- **COUPLED** — must be ruled together with a named companion; solo ruling forbidden.
- **OPEN** — genuinely awaiting owner input; **not** an ambiguity reflected back — a concrete decision the owner has said he wants to make himself.

---

## RATIFIED (17 = original 5 + C3-batch flip of 12)

**Original 5** (2026-09-08 · unchanged):

| # | Ruling | Owner text (verbatim from DECISIONS.md 2026-09-08T~06:15Z) |
|--:|---|---|
| 1 | Rules-Service **R-4** taxonomy | Ratified as proposed. |
| 2 | DAP **R-1** controlled-unit definition | Ratified as proposed. |
| 3 | Agent-Containment **R-1** capability-ceiling list | Ratified as proposed (the four ceilings: no self-replication, no unauthorised resource acquisition, no unauthorised credential escalation, no self-access to oversight). |
| 4 | Rules-Service **R-3** witness | Same witness the Watch already uses (C3). |
| 5 | Agent-Containment **R-2** scope-ratifying authority | Syni.ai for early deployments. |

**C3-batch flip 2026-09-13** (owner verbatim: *"3 - Approved"* · see `notes/RATIFICATION_C3_BATCH_20260913.md`):

| # | Ruling | Value (flipped DEFAULT → RATIFIED) |
|--:|---|---|
| 6 | Rules-Service **R-1** countdown | 48h system-ordinary / 7 days system-TCB |
| 7 | DAP **R-4** API-key lifetime | 90-day rotation |
| 8 | DAP **R-5** AI-labs taxonomy | Separate external-party entry |
| 9 | Security **R-10** recommendation window | 24h (A5.16) |
| 10 | Security **R-8** approach | Baseline-period |
| 11 | Security **R-9** approach | Baseline-period |
| 12 | Security **R-11** approach | Baseline-period |
| 13 | Agent-Containment **R-3** sample rate | Baseline-period |
| 14 | Pruning **R-12** default | Re-derivation |
| 15 | Doc-0 **R-1** TCB test | Resolved-by-use; deterministic ∧ protection-critical (`tcb_enumeration_v1`) |
| 16 | Doc-0 **R-3** Watch TCB membership | Mkono IN · Grey Mirror OUT |
| 17 | Doc-0 **R-5** deployment model | Dedicated infrastructure per tenant (`trust_domains_v1`) |
| + | Serving-Integrity **R-13** validation cadence | Monthly + per-engine-version + per-artefact-version (folded under C3 en-masse) |

## DEFAULT (0 remaining after C3 batch)

All prior DEFAULT rows flipped to RATIFIED per C3 batch 2026-09-13. New DEFAULT rows would appear here as future owner rulings land with DEFAULT-class posture.

## COUPLED (1)

| # | Ruling | Coupling clause (verbatim) |
|--:|---|---|
| 1 | DAP **R-3** per-party ceilings | MUST NOT be ruled alone — allocation against Security **R-7** estate release budget; rule together. |

## OPEN (7 — genuine owner decisions; +2 reconcile from `Ratification_Record_v1` + Serving-Integrity Amendment + 2A env-drift-tracked-unknown)

| # | Ruling | What owner has explicitly reserved for himself |
|--:|---|---|
| 1 | Security **R-7** | Estate release budget number (**highest priority** — gates DAP R-3, DAP-6, SFP-6) |
| 2 | DAP **R-6** | Pricing model |
| 3 | WPW **R-2** | External-release signatory |
| 4 | DAP named approving authority (DAP **R-2**) | Person/role identity |
| 5 | Rules-Service **R-2** | Second-signatory named role (reconciled from `Ratification_Record_v1` Section 2 R-2; not previously in RULING_LEDGER; added M0 2026-09-13) |
| 6 | Serving-Integrity Amendment **R-14** | Colibri engine admission — deliberately unruled; gated by appliance benchmark + TCB-tier admission ceremony (added M0 2026-09-13) |
| 7 | **ENV-DRIFT-2TESTS-20260913** | 2 tests present in close-time env (recorded 3562 floor) but not collected in current sandbox at HEAD `e2ae44b0`. Preflight rebased floor to 3560 per owner Option A ruling 2026-09-13. Closed when close-time env info surfaces (e.g. per-test collect-only log from the close-time sandbox). Tracked, not lost. |

---

## Rollup (post C3-batch 2026-09-13)

| Class | Count |
|---|--:|
| RATIFIED | 17 (+1 SIA R-13) |
| DEFAULT (wired tests-first) | 0 (all flipped in C3) |
| COUPLED (blocked until companion) | 1 (DAP R-3 · Sec R-7) |
| OPEN (owner-reserved) | 6 |
| **Total tracked** | **25** |

## Also HELD (not counted in rollup; tracked for owner reference)

- **DPO-S2 reflection contract** — HELD per owner C5 disposition 2026-09-13 · reflection.run() raises NotImplementedError · 3-5 candidates in `notes/DPO_S2_REFLECTION_CANDIDATES_20260913.md` awaiting owner selection.
- **S-7 "Learn"** — HELD per Amendment 1 (spec gap) · owner-context package at `notes/S7_CONTEXT_PACKAGE_20260913.md` (4 options).
- **Amendment 8 scope-statement (eradication / communication / evidence custody)** — HOLD per owner C1 disposition 2026-09-13 · parked, no milestone assigned.

## Rule (banked)

DEFAULT-class values are **wired into `backend/services/rulings/default_class_constants.py`
tests-first**: every value in that module is frozen by an invariant test that
docstring-quotes the owner ruling verbatim. If the owner overrides a DEFAULT
later, the invariant is amended in the same commit that flips the value. A
DEFAULT value is never silently changed.

**Read `STATE/STANDING_ORDERS.md` first — permanent standing law.**
