READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_security_assurance_promise_set_v2_delta.md

**Source (NEW).** `canon/drops/20260913/raw/Security_Assurance_Promise_Set_v2.xlsx` sha256 `72a4e7620c959a8d0dd36c73ed5c712689ed8f0663630803b79a43f0db453088` · 17,480 B · owner-attached 2026-09-13.
**Prior version.** `canon/drops/20260909/extracted/files_14/Security_Assurance_Promise_Set.xlsx` sha256 `8c7a3b7205db0166852ceffc879e2461053ee4af61eedbdb02c253e2deb0010d` · 16,864 B (files_14 · 2026-09-09).

## §A · Row-level diff verdict

**Structural changes to sheet `Security Assurance Set`:** +1 row (28 → 29 rows). **New row = R28 · S-27**. NO existing S-1..S-26 rows or the composite #6 row changed by any cell. NO deletions. NO reordering.

**Structural changes to sheet `Legend`:** 1 cell diff (R2 col B) — scope range widened from *"S-1–S-26"* to *"S-1–S-27"*. NO other cells changed.

## §B · New row · S-27 (verbatim)

| Field | Value |
|---|---|
| # | **S-27** |
| Doc | V-1–V-4 · Serving Integrity Amendment (13 Sep 2026) |
| Promise | *"The system will serve exactly the model it registered — pressure may make it slower, never different — and will say on the record which engine, its own or a provider's, produced every answer."* |
| Standard | A5.8 (no silent recalibration, rules layer) · SEC-1/SEC-2 load-time integrity pattern · FDP_ACC.1 form (SFP-8) · invariants under Attribute 11 FP-2 posture |
| Impl. status | Absent → new |
| Bound / Ruling | R-13 (validation cadence, DEFAULT-class) open; floor explicitly **not imposable** on the frontier gateway tier — receipt records boundary |
| Where it lives | Serving Integrity Amendment V-1 (A20.15, SFP-8), V-2 (gate conformance), V-4 (receipt fields); TCB entry and failure-posture entries added |
| System features | (a) Artefact hash verified against register before first token; (b) Token-exact reproduction check on demand + schedule; (c) Response envelope carries provider + model-version fields for frontier crossings; (d) Failure = fail-closed refuse-to-serve |
| User requirements | *"User can (estate owner) trust that the model tested is the model running, under any load / User can (any consumer) see which engine — Akki-controlled or provider — produced any answer."* |

## §C · Impact on `MILESTONE_PROMISE_BINDING_20260913.md`

**Material update required** (interim addendum banked at `notes/MILESTONE_PROMISE_BINDING_20260913.md §M3-ADDENDUM` — see that file).

Summary:
- **M3** Watch composite `#6 · S-1..S-21` grows to `#6 · S-1..S-21 + S-22..S-27` (S-22..S-25 already carried; S-26 already carried via Pruning; S-27 is new).
- Milestone-level binding for S-27:
  - **M2** wires TCB entry (serving-integrity gate IN; engine bulk OUT) + FP entry (hash-mismatch → fail-closed refuse-to-serve) + SFP-8.
  - **M1** wires DAP-31+/DAP-32+ conformance dependency markers.
  - **M3** wires AC-13 + AC-14 alongside AC-1..AC-12.
  - **M4** wires A5.7+ receipt-fields extension composed with DAP-20 assistance-chat.
  - **M5** wires TGT+ (Targeta acceptance evaluations SFP-8-conforming) as dependency.

## §D · Not a blocker for the Registry+DAP block

Reasoning:
- DAP-Spec §9 A1..A10 acceptance criteria unchanged by the v2 xlsx.
- SFP-8 conformance is a **serving-path dependency**, not a §9 pass criterion — M1 rows can land tests-first with declared dependency markers where DAP-31/DAP-32 semantics require SFP-8 (owner C5 disposition: reflection stays HALTed; declared dependency, not guess).
- The v2 xlsx changes NO existing binding — only adds S-27.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
