READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# MILESTONE_PROMISE_BINDING · delta 2026-09-13T19:10Z — Watch Learning Amendment fold-in

**Base document:** `notes/MILESTONE_PROMISE_BINDING_20260913.md` (unchanged; this file is an APPEND-only delta).
**Trigger:** owner drop #2 · Security_Assurance_Promise_Set v3 (sha `51d52ebd...`) + Watch_Learning_Amendment_v1 (sha `eb8a0bec...`).
**Ratchet:** unchanged (document lane).  No code change.

## §Δ1 · Promise-set count

| Field | Before | After |
|---|---|---|
| Total S-Set chartered promises | S-1..S-27 (27) | **S-1..S-29 (29)** |
| Spec-gap items in S-Set | S-7 gap (Amendment 1 reclassified) | **none — S-7 spec-closed 2026-09-13 by Watch Learning Amendment L-2, L-4** |
| New items | — | **S-28** (verdict certificate) · **S-29** (capability admission ceremony) |
| Open owner-input rulings introduced | — | **R-15** (initial cert library seed) · **R-16** (ratifier + cadence) · **R-17** (class granularity + initial register) |

Authoritative Promise-Set version from this drop forward: **v3** (`51d52ebd7acf4ef9d47eaf4634c1970e087cc71d021bc56763c3064f07f86f30`).

## §Δ2 · S-7 status change (owner-relevant)

- **Was:** Amendment 1 (Security_Promise_Set_Amendments) reclassified S-7 as a specification gap.  Tracked as an OPEN-C2 item.
- **Now:** Watch Learning Amendment v1 CLOSES S-7 at spec level via L-2 (A5.20 + RBM-23) and L-4 (A5.22 research loop).  Not built.

## §Δ3 · Milestone binding impact (owner constraint 2026-09-13: no plan changes; new requirements ride EXISTING wave homes)

### M2 (Rules-Service + Doc-0 attributes) — no plan change
Additive-compatible; no in-flight sub-wave invalidated.  Detailed matrix in `notes/canon_grey_mirror_requirements.md` §5.  Notable:

- **W-M2-SW1 (CLOSED)** — generic RuleRegistry accepts new rule class `RBM-23` without schema change.  No re-work.
- **W-M2-SW2 (CLOSED)** — `system_tcb` business-type already in v1 taxonomy; RBM-23's RBM-8 ceremony is the same countdown/witness/second-signatory ceremony SW2 landed.  No re-work.
- **W-M2-SW3 (IN FLIGHT)** — rule-book library is generic; a future seed jsonl can carry RBM-23 rows.  No plan change.
- **W-M2-SW4 W-286-RULE-ENUMERATION-CLASSIFY** (in M2 plan; not yet opened) — natural home for RBM-23 as an added rule row, filed alongside the remaining 272 rules.  No plan change.
- **W-DOC0-ATTR7-BASELINE (in M2 plan; imminent)** — L-3 mirage-as-certificate-ground concept touches admission time; wave scope unchanged, add a limit-marker in ATTR7 close note when it lands.
- **W-DOC0-ATTR8-AUDIT-AU3 (in M2 plan; imminent)** — certificate records are AU-3 subjects (Doc-0 §8); additive AU-3 subject class in the linter.  No plan change.
- **W-SFP-8-SERVING-INTEGRITY (in M2 plan; imminent)** — DAP-32+ extended orthogonally by L-3; SFP-8 declared-dependency marker unchanged.  No plan change.

### M3 (Watch 62-row + Registry CP10 + Pruning + Agent-Containment) — no plan change

Per `MILESTONE_PROMISE_BINDING_20260913 §M3`, M3 owns the Watch stack (W-WATCH-STACK Wave C · 62 rows) and Agent-Containment (W-AGENT-CONTAINMENT AC-1..AC-12).  New Watch-Learning-Amendment requirements ride these EXISTING waves — no new waves:

| New requirement | Existing home wave in M3 | Notes |
|---|---|---|
| A5.19 verdict certificate schema | W-WATCH-STACK · Doc-3 A2 seam row | Enriches, not replaces |
| A5.20 certificate-requirement rule class | W-WATCH-STACK · Doc-3 A5 row | Deterministic gate |
| A5.21 mirage as certificate ground | W-WATCH-STACK · mirage subsystem row | Extends mirage row |
| A5.22 unsure-case research queue | W-WATCH-STACK · S-13 detection-vs-decide seam | Extends verdict handoff |
| A20.16 capability-class register | W-WATCH-STACK · Doc-20 companion row | Doc-20 adjacency |
| AC-15 pre-scope certificate ground | W-AGENT-CONTAINMENT | New AC row in existing wave |
| AC-16 containment feeds research queue | W-AGENT-CONTAINMENT | New AC row in existing wave |
| AC-17 per-action citation + first-exercise floor | W-AGENT-CONTAINMENT | New AC row in existing wave |
| AC-18 learner proposes, never ratifies | W-AGENT-CONTAINMENT | New AC row in existing wave |
| DAP-32+ per-requirement provocation | W-DAP-STACK 2H (**CLOSED · M1**) | `[flag]` — extension on closed wave; documentary-only unless owner rules otherwise |

`[framing, not canon]` — Doc-3 62-row baseline naturally grows when Doc-3 grows; wave count unchanged.  M3 is not re-planned.

### M4/M5 — no direct impact

No M4/M5 wave is invalidated; no plan changes.

## §Δ4 · WHEN DONE, THESE PROMISES HOLD (append in place — no plan change)

Add to `MILESTONE_PROMISE_BINDING_20260913.md §M3 WHEN DONE, THESE PROMISES HOLD` when it is next refreshed (owner constraint: EXISTING milestone home, NOT a new wave):

- **`Promise S-28`** — `Absent → new`.  Discharged **inside W-WATCH-STACK + W-AGENT-CONTAINMENT** by: L-1 (A5.19 certificate schema on Doc-3 A2 seam row) + L-2 (A5.20/RBM-23 on Doc-3 A5 row) + L-3 (A5.21 on mirage row) + L-4 (A5.22 on S-13 seam).  Landed at spec 2026-09-13, **not built**; W-WATCH-STACK builds when M3 opens.
- **`Promise S-29`** — `Absent → new`.  Discharged **inside W-WATCH-STACK + W-AGENT-CONTAINMENT** by: L-5 (A20.16 on Doc-20 row + AC-17 + AC-18 in W-AGENT-CONTAINMENT).  Landed at spec 2026-09-13, **not built**.
- **`Promise S-7`** — `Gap → spec-closed`.  Discharged at SPEC level by Watch Learning Amendment L-2 + L-4.  Built inside W-WATCH-STACK (M3) when M3 opens.  Not built.

**Existing §M3 `S-7` row (line 287) should be updated in place** from `NOT discharged by M3 per Amendment 1` to `discharged inside W-WATCH-STACK per Watch Learning Amendment L-2/L-4 (spec-closed 2026-09-13; not built)`.

## §Δ5 · Amendments explicitly discharged this drop

- **Watch Learning Amendment L-1..L-5** (2026-09-13) — spec text landed; no wave built yet.  Requirement rows filed against existing W-WATCH-STACK (M3) and W-AGENT-CONTAINMENT (M3) waves.  R-15/R-16/R-17 remain OPEN owner-input rulings; land in `RULING_LEDGER.md` (documentary, not a wave).

## §Δ6 · No plan change · no M2 halt-to-owner triggered

Owner constraint 2026-09-13 applied: **do NOT alter the plan; do NOT create new waves; do NOT resequence.**  Every new requirement filed against an existing M0..M5 wave home per the mapping in §Δ3.  Load-bearing check ran against every in-flight and imminent M2 sub-wave; all changes are ADDITIVE.  M2 continues unchanged.

## §Δ7 · Flags surfaced for owner visibility (do NOT reopen)

- **`[flag]` W-DAP-STACK 2H is CLOSED (M1 · already banked).**  L-3's DAP-32+ extension (per-requirement provocation scenarios) sits inside the CLOSED 2H scope.  Documentary-only unless owner rules to (a) open a documentary follow-on close-note against 2H, or (b) fold at build-time when the certificate mechanism is landed elsewhere in M3.
- **`[flag]` W-M2-SW1 + W-M2-SW2 CLOSED accept RBM-23 additively.**  Filing RBM-23 into the register happens naturally at W-M2-SW4 (W-286-RULE-ENUMERATION-CLASSIFY) when SW4 opens.
- **`[flag]` W-AGENT-CONTAINMENT scope defined as AC-1..AC-12.**  Four new AC rows (AC-15..AC-18) land inside the same wave — Doc-3 canonical scope naturally grows.  No new wave needed.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
