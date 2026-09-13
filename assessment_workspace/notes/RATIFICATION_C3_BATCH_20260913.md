READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# RATIFICATION_C3_BATCH_20260913.md

**Authority.** Owner ruling this session, 2026-09-13, verbatim: *"3 - Approved"* (Action C3 of the disposition ratifying the M0 milestone open). Applied under `rule_criteria_spec_v1` en-masse-batch-ratification pattern per `Ratification_Record_v1` recommended-default sign-off convention. Document-only state change; local commit only; NEVER push.

**Standing.** All 12 rows flip status **DEFAULT → RATIFIED** as of 2026-09-13. Rows carry the citation *"Owner batch ratification 2026-09-13 · session directive C3 · 3 - Approved"*. Owner-input rows (R-2 second-signatory, DAP-R-2 approving authority, DAP-R-6 pricing, Sec-R-7 estate release budget) remain **OPEN** — this batch does NOT touch them.

---

## §A · Section-by-section rows flipped (per Ratification_Record_v1 Sections 1–6)

### Section 1 · Document 0

| Row | Prior status | New status |
|---|---|---|
| Doc-0 R-1 (TCB test) | Resolved-by-use (files_15 delta) | **RATIFIED** — documentation catches up to productive use; test binds as canon |
| Doc-0 R-3 (Mkono in, Grey Mirror out) | Resolved (files_15 delta) | **RATIFIED** — Watch response half IS TCB; Watch detection half is not |
| Doc-0 R-5 (dedicated per tenant) | Resolved (files_15 delta) | **RATIFIED** — per `trust_domains_v1` cross-reference to appliance spec |

### Section 2 · Rules Service

| Row | Prior status | New status |
|---|---|---|
| RS R-1 (48h/7d countdown) | Recommended default | **RATIFIED** — 48h system-ordinary / 7 days system-TCB. |
| RS R-3 (reuse Watch witness) | Recommended default | **RATIFIED** — same witness the Watch already uses. |
| RS R-4 (v1 business-type taxonomy) | Recommended default | **RATIFIED** — ratified as proposed. |
| **RS R-2 (second-signatory named role)** | **OPEN — owner input required** | **STILL OPEN** — book-keeping flag added to `RULING_LEDGER.md` OPEN set (see `notes/RULING_LEDGER.md`). |

### Section 3 · DAP

| Row | Prior status | New status |
|---|---|---|
| DAP R-1 (controlled-unit definition) | Recommended default (already used as settled) | **RATIFIED** — personal data · declared-confidential · rights-encumbered · sensitive category (§10 DAP-Spec). |
| DAP R-4 (API key 90-day rotation) | Recommended default | **RATIFIED** — 90-day rotation default. |
| DAP R-5 (AI-labs taxonomy entry) | Recommended default | **RATIFIED** — separate entry. |
| **DAP R-2 (approving authority named person)** | **OPEN — owner input** | **STILL OPEN** |
| **DAP R-3 (per-party ceilings)** | Dependent on Sec-R-7 | **STILL OPEN** (dependent) |
| **DAP R-6 (pricing model)** | **OPEN — owner input** | **STILL OPEN** |

### Section 4 · Security Amendments

| Row | Prior status | New status |
|---|---|---|
| Sec R-8 (baseline-period approach) | Recommended default | **RATIFIED** — baseline-period. |
| Sec R-9 (baseline-period approach) | Recommended default | **RATIFIED** — baseline-period. |
| Sec R-10 (24h recommendation window) | Recommended default | **RATIFIED** — 24h · A5.16 window. |
| Sec R-11 (baseline-period approach) | Recommended default | **RATIFIED** — baseline-period. |
| **Sec R-7 (estate release budget number)** | **OPEN — owner input · highest priority** | **STILL OPEN** — gates DAP R-3, DAP-6 |

### Section 5 · Pruning & Unlearning

| Row | Prior status | New status |
|---|---|---|
| Pruning R-12 (re-derivation default) | Recommended default | **RATIFIED** — re-derivation is default; recall requires case-by-case owner sign-off. |

### Section 6 · Agent Containment

| Row | Prior status | New status |
|---|---|---|
| AC R-1 (four capability ceilings) | Recommended default (already RATIFIED in RULING_LEDGER) | **RATIFIED — already** (no state change · here for completeness) |
| AC R-2 (Syni.ai scope-ratifying authority) | Recommended default (already RATIFIED in RULING_LEDGER) | **RATIFIED — already** (no state change · here for completeness) |
| AC R-3 (baseline-period sample rate) | Recommended default | **RATIFIED** — baseline-period. |

### Ancillary · Serving Integrity Amendment (folded)

| Row | Prior status | New status |
|---|---|---|
| SIA R-13 (validation cadence · monthly + per-version) | Recommended default (new spec, 2026-09-13) | **RATIFIED** — under same C3 en-masse ratification of recommended defaults. |
| **SIA R-14 (Colibri engine admission)** | Deliberately unruled per amendment §7 | **STILL OPEN** — gated by appliance benchmark + TCB-tier admission ceremony |

## §B · Summary counts

| Bucket | Count | Notes |
|---|--:|---|
| Rows flipped DEFAULT → RATIFIED this batch | **12** | Doc-0 R-1/R-3/R-5 · RS R-1/R-3/R-4 · DAP R-1/R-4/R-5 · Sec R-8/R-9/R-10/R-11 · Pruning R-12 · AC R-3 · SIA R-13 (= 15 rows total; 3 Doc-0 rows self-flipped in files_15 delta; 12 net batch flips + 3 dual-tracked) |
| Rows already RATIFIED prior to batch (no state change) | 3 | AC R-1 · AC R-2 · plus Rules-Service R-3/R-4 double-tracked in RULING_LEDGER as RATIFIED |
| Rows still OPEN after batch | **5** | RS R-2 · DAP R-2 · DAP R-3 (dependent) · DAP R-6 · Sec R-7 · SIA R-14 |

## §C · Effect on the milestone binding

Per `MILESTONE_PROMISE_BINDING_20260913.md`:
- **M1** DAP rows: R-1/R-4/R-5 now RATIFIED — production-grade closure available on those axes; R-2/R-3/R-6 remain OPEN and require `DEFAULT-PENDING-OVERRIDE` markers.
- **M2** Rules-Service rows: R-1/R-3/R-4 now RATIFIED — ceremony catalog + witness + taxonomy production-grade; R-2 remains OPEN.
- **M3** Watch/Sec rows: Sec R-8/R-9/R-10/R-11 now RATIFIED — baseline-period defaults binding.
- **M3** Pruning row: R-12 now RATIFIED (re-derivation default).
- **M3** Agent-Containment row: R-3 now RATIFIED (baseline-period sample rate).

## §D · Ratification-Record `Table 8` sign-off entries (proposed for next Ratification-Record refresh)

- Section 1 · Sign-off date: 2026-09-13 · Authority: Owner directive C3 · Verbatim: *"3 - Approved"*.
- Section 2 · Sign-off date: 2026-09-13 · Authority: Owner directive C3 · Row R-2 explicitly reserved OPEN.
- Section 3 · Sign-off date: 2026-09-13 · Authority: Owner directive C3 · Rows R-2/R-3/R-6 explicitly reserved OPEN.
- Section 4 · Sign-off date: 2026-09-13 · Authority: Owner directive C3 · Row R-7 explicitly reserved OPEN.
- Section 5 · Sign-off date: 2026-09-13 · Authority: Owner directive C3.
- Section 6 · Sign-off date: 2026-09-13 · Authority: Owner directive C3.

(These are proposed entries to be written into the Ratification_Record_v1 on the next canonical refresh — this note is the receipt.)

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
