READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# MILESTONE_PROMISE_BINDING_20260913.md

**M3-ADDENDUM (added 2026-09-13 · M0 close) — Serving Integrity Amendment v1 + Security Assurance Promise Set v2 delta:**

Two new canon artefacts landed 2026-09-13 (owner-attached · see `notes/canon_serving_integrity_amendment_v1_requirements.md` + `notes/canon_security_assurance_promise_set_v2_delta.md`). Material updates to the binding:

- **S-27** (new · V-1..V-4 composite) — Watch composite-promise cluster grows from `#6 · S-1..S-21` to `#6 · S-1..S-21 + S-22..S-27`. S-22..S-25 already carried; S-26 already carried via Pruning; **S-27 is new and lands in M3**.
- **S-28** (new 2026-09-13 · Watch Learning Amendment v1 L-1..L-4) — verdict certificate; discharged **inside W-WATCH-STACK** (M3).  Spec-closed; not built.
- **S-29** (new 2026-09-13 · Watch Learning Amendment v1 L-5) — capability admission ceremony; discharged **inside W-WATCH-STACK + W-AGENT-CONTAINMENT** (M3).  Spec-closed; not built.
- **S-7 status flip** (2026-09-13 · Watch Learning Amendment v1 L-2 + L-4) — was "Absent → gap" per Amendment 1; now **"Absent → new (spec-closed, 13 Sep 2026)"**.  Discharged **inside W-WATCH-STACK** (M3).  Not built.  Open owner-input rulings: R-15, R-16.
- **Open rulings introduced by Watch Learning Amendment v1**: **R-15** (initial certificate library seed) · **R-16** (ratifier role + research cadence) · **R-17** (capability-class granularity).  Filed in `RULING_LEDGER.md` (documentary; no wave).
- **AC-13 (session freeze)** + **AC-14 (contained-agent SFP-8 serving)** — Agent-Containment set grows from AC-1..AC-12 to AC-1..AC-14; both land in M3 W-AGENT-CONTAINMENT.
- **A20.15 · SFP-8 · Serving Floor** — SFP-8 discharges in M2 W-DOC0-ATTR7-BASELINE + W-RULES-SERVICE-CEREMONY (was 7 SFP rows, now 8). TCB row `serving-integrity gate` lands in M2 W-DOC0-ATTR1-TCB. FP row `hash-mismatch → fail-closed refuse-to-serve` lands in M2 W-DOC0-ATTR11.
- **DAP-31+ / DAP-32+ · gate-conformance** — DAP-31 (reproduction probe) and DAP-32 (admission-integrity probe) both grow a conformance clause requiring SFP-8-conforming serving path. Land in M1 as **declared dependency markers** (per owner C5 disposition · reflection HALTed · declared dependency, not guess). M1 acceptance criteria A1..A10 unaffected in scope — SFP-8 is a serving-path dependency, not a §9 pass criterion.
- **A5.7+ · frontier-crossing receipt fields** — Existing A5.7 (already amended to include principal identity + timestamp per Security_Promise_Set_Amendments Amendment 3) grows to also record provider + provider-stated model version for frontier crossings. Discharges in M4 (composed with DAP-20 assistance-chat receipt surface).
- **TGT+ · Targeta acceptance evaluations SFP-8-conforming** — MOAC verdict + yield-wall per-stratum measurements land on SFP-8-conforming serving only. Discharges in M5 W-DATA-SUITE-v2-LIFT as dependency.
- **R-13 · validation cadence** — RATIFIED per C3 batch 2026-09-13 (monthly + per-engine-version + per-artefact-version). No milestone-level scope change.
- **R-14 · Colibri engine admission** — deliberately unruled; added to RULING_LEDGER OPEN set. Not assigned to any milestone; gated by appliance benchmark + TCB-tier admission ceremony.

**Not a blocker for the Registry+DAP block.** DAP-Spec §9 A1..A10 pass criteria unchanged; SFP-8 conformance is a serving-path dependency; M1 rows carry declared dependency markers per C5.

**Updated §END coverage-count for M3:** 1 composite (`#6`) + **21 → 26 S-rows** (S-1..S-21 + S-24 + S-26 + new S-27; plus S-22/S-23/S-25 partial remainders) + **12 → 14 AC** + 1 RBM + 1 CP-close + 1 doctrine.

**Updated §END coverage-count for M2:** 12 Attributes + 3 Rules-R + 3 Promise-# + 2 Amendments + 2 doctrines + **1 new SFP-8** + TCB serving-integrity-gate row + FP hash-mismatch row.

---

**Purpose.** Unambiguous milestone ↔ work ↔ promise binding for the owner-ratified M0–M5 spine. Every promise ID is drawn verbatim from an on-disk catalog. Read-only, document-only. `[framing, not canon]` tags mark my interpretation.

**Standing.** ROLE OVERRIDE · Phase-1 Canon Assessment · NO production code · NO scaffolding touched · local commit only, NEVER push · NO egress · HALT after delivery. SO §1 boot honoured; SO §2 DECISION-POINT / END-OF-WAVE reporting doctrine respected.

**Date.** 2026-09-13.

**Ratchet floor.** 3562 (`baseline_failures.json`; untouched).

---

## §0 Authoritative promise catalogs on disk (source of every ID cited below)

I bind ONLY to the catalogs enumerated here. Every ID quoted in §M0–M5 traces back to one of these files.

| Catalog | Source path on disk | ID space |
|---|---|---|
| **Security Assurance Promise Set** (26-row) | `canon/drops/20260909/extracted/files_14/Security_Assurance_Promise_Set.xlsx` sheet "Security Assurance Set", 28 rows × 9 cols | `#6` (composite) + **`S-1 … S-26`** |
| **Security Promise Set Amendments** (8 amendments applied on top) | `canon/drops/20260907/extracted/text/Security_Promise_Set_Amendments.txt` (also `.../files_12/Security_Promise_Set_Amendments.docx`) | **Amendment 1 … Amendment 8**; adjust status of S-7 (gap), S-10/S-11 (doc-home), S-14/S-15 standard, S-2/S-4/S-5/S-19 bounds, upgrades the Watch to full Reference-Monitor instantiation, adds A5.9 to Attr-11, adds scope-statement request |
| **Canon-8 A5.x structural properties** (referenced by the S-rows) | `canon/unpacked/Akki_Canon_8_The_Watch.docx` Part II §A5 | **`A5.1 … A5.21`** (representative refs from S-set: `A5.1 A5.2 A5.3 A5.5 A5.6 A5.7 A5.8 A5.9 A5.10 A5.11 A5.12 A5.13 A5.14 A5.16 A5.17*(new) A5.18*(new)`); `[framing, not canon]` A5.4 has been relocated to Doc-0 Attr-9 per Amendment 3 and is no longer an A5 promise |
| **DAP-Spec §9 Build Acceptance Criteria** | `canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` line 122-131 | **`A1 A2 A3 A4 A5 A6 A7 A8 A9 A10`** (DAP build-acceptance, distinct from Canon-8 A5.x) |
| **DAP-Spec functional rows** | same file, lines 30+ | **`DAP-1 … DAP-38`** (referenced by S-22..S-25 as targets: `DAP-33 DAP-34 DAP-35 DAP-36 DAP-37 DAP-38`) |
| **Agent Swarm Containment** promises | `canon/drops/20260910/extracted/text/Agent_Swarm_Containment_Governance_Model_v1.txt` lines 26-45 | **`AC-1 … AC-12`** (+ non-claims `LIM-1 … LIM-5` per `notes/NON_CLAIMS_REGISTER.md`) |
| **Canon-1 numbered promise references** (indirect: Canon-1 §12 = "Six Services" as **six canonical sentences**, unnumbered in Canon-1 itself; the **`Promise #N` numbering** is used across `Doc-0 Governance Architecture v1`, `Handoff_Generalisation_v1`, `Master_Requirements_Registry`, and `notes/canon_1_requirements.md`) | `canon/drops/20260909/extracted/text/Akki_Governance_Architecture_v1.txt` (Doc-0) references at least: **Promise #4** (retained-file custody classes), **Promise #7** (detection-latency), **Promise #12** (census/connection), **Promise #22** (MOAC · "every criterion or no service"), **Promise #25** (outer gate · raw-data download), **Promise #27** (full ceremony · SFP), **Promise #29** ("learning may detect, never decide"), **Promise #32** (Northena's objective freeze / registered handoff contract) | **`Promise #4 · #7 · #12 · #22 · #25 · #27 · #29 · #32 …`** (numbering originates outside Canon-1's body; the numbering is authoritative in Doc-0 and `Master_Requirements_Registry`) |
| **Ruled-value defaults** (Wave E) | `notes/RULING_LEDGER.md` (5 RATIFIED, 9 DEFAULT, 1 COUPLED, 4 OPEN) + `Ratification_Record_v1.docx` (drop 09-10) | **`R-1 … R-12`** across (Rules-Service, DAP, Security, Agent-Containment, Pruning), **`CA1-N2` (72-hour breach)**, **`CA1-N5` (RTO 3600s)**, **`RBM-2`, `RBM-20`** (rulebook items) |
| **SYSTEM_OBJECTIVES_AND_PROMISES_CHARTER (session synthesis)** | `notes/SYSTEM_OBJECTIVES_AND_PROMISES_CHARTER.md` §2 | **`P1 … P12`** + **`P-SO-1 P-SO-2`** (standing-order-derived operational law). The charter states verbatim: *"The promises are numbered P1–P12 for reference in this charter only; canon does not carry that numbering."* So P1–P12 are traceability handles, not canonical promise IDs. |
| **Function & Promise Registry** (per Canon-7 §35–§40; live registry) | `notes/function_promise_registry.jsonl` (4 rows so far; W-REGISTRY-EXTENSION-G3 seed) | live per-function rows carrying `function_id`, `governor`, `mandate`, `promise`, `service_trace`, `enforcement` |

**`[framing, not canon]` on enumeration accuracy:**
- Canon-1 §12 states "Six sentences state what the platform promises" but does NOT number them 1–6 in Canon-1's body; the register is Part VI per §5 Precedence, but §11 "Governing Rule" + §12 "Six Services" is the register body.
- The **`Promise #N`** numbering (e.g. #4, #22, #27, #29, #32) is used systematically in Doc-0 and Master_Requirements_Registry; that is the authoritative numbering space I bind to below.
- Where I need a promise ID that has no on-disk enumeration, I write the canon-clause anchor (e.g. `Canon-1 §4.1 "Fail-closed custody" doctrine`) rather than invent an ID. Doctrines (`Canon-1 §4.1 … §4.12`) are the higher-precedence rank per Canon-1 §5.

---

## §M0 · Canon-delta extractions + supersession of Aug-14 REUSE / BUILD_STRATEGY

**Owner-ratified shape (confirmed against disk):** ✅ matches.

### BUILDING
- **Canon-delta extractions** — up to 10 new `notes/canon_<slug>_requirements.md` files per Stage-P1 order of `notes/LEVERAGE_AND_GAP_INVENTORY_20260913.md §G.2`.
- **Superseded deliverables** — dated successors to `REUSE_ASSESSMENT.md` (2026-08-14, 53,479 B) and `BUILD_STRATEGY.md` (2026-08-14, 250,939 B) as `REUSE_ASSESSMENT_20260913.md` / `BUILD_STRATEGY_20260913.md` (Q2 DEFAULT-PENDING-OVERRIDE: supersession, preserve Aug-14 originals).
- **Book-keeping refresh** (deferred per Q5 DEFAULT-PENDING-OVERRIDE) — `STATE/NEXT.md` `## Current step marker` block + `STATE/PINS.md` canon-pin block. NOT executed in Phase-1 per default.

### LIFTING
- **Nothing lifted** (M0 is document-only extraction · no donor code).

### KEEPING (unchanged, cited leverage)
- **All 559 rows** of `notes/canon_1..9_requirements.md` (2026-08-14) — canon-pack hashes byte-identical to fresh download; extractions valid. Evidence: this session's hash verification in `notes/LEVERAGE_AND_GAP_INVENTORY_20260913.md §3.2`.
- **`notes/canon_addendum_1_requirements.md`** (Aug 27) — source unchanged; valid.
- **`notes/canon_agent_containment_spec_v1_requirements.md`** (Sep 9) — source sha `2824796d06` unchanged; valid.
- **Ratchet floor 3562** — untouched (M0 writes no code, no invariants).
- **All 449 phase0 drill_receipts** — untouched.
- **All 84 backend services** — untouched.

### WHEN DONE, THESE PROMISES HOLD

M0 discharges NO canonical runtime promise. It discharges an **engagement-discipline obligation** carried in `STANDING_ORDERS §2 Engagement Discipline` (verbatim):

> "Requirements are **never flattened**. Sub-clauses stay distinct. Every requirement quoted verbatim in the gating test's docstring and in the wave grounding brief. If the verbatim quote is not in the test, the test does not gate the row."

and Canon-1 §4.11 doctrine (verbatim):

> "**Canon before ruling** — No decision proceeds from memory or summary where the governing document exists. Unread canon is read before ruling."

**PROCESS that proves M0 discharge:**
- Every un-extracted doc listed in `LEVERAGE_AND_GAP_INVENTORY §F.1` (20 docx/xlsx) has either a `canon_*_requirements.md` file OR a documented reason for deferral in the same note.
- Superseded `REUSE_ASSESSMENT_20260913.md` and `BUILD_STRATEGY_20260913.md` cite the M0-produced row-level extractions as their bibliography (SO §2: "quote spec verbatim per the audit rebase rule").
- `notes/citation_audit.py` (per PINS.md) runs clean over M0 deliverables (previous baseline: `104/104 file · 1778/1778 canon · 0 failed`).
- **This is a book-keeping promise, not a runtime promise.** No S-*, DAP-*, AC-*, or `Promise #N` is discharged by M0.

---

## §M1 · W-DAP-STACK · DAP-1..DAP-30 (admission · trust · crossing · approval · metering)

**Owner-ratified shape (confirmed against disk):** ✅ matches `PHASE_C_SYSTEMATIC_BUILD_PLAN.md §W-DAP-STACK`, `LEVERAGE_AND_GAP_INVENTORY §E.2`.

### BUILDING (new mechanisms · wave IDs)

Per `PHASE_C_SYSTEMATIC_BUILD_PLAN.md §W-DAP-STACK` sub-wave lineup:

- **W-DAP-STACK 2A** — External-party principal + admission (DAP-1, DAP-2, DAP-3, DAP-4, DAP-5, DAP-13). **LEVERAGES the existing untracked scaffolding** at `backend/contracts/dap.py` (288 lines), `backend/services/dap/admission.py` (101 lines), `backend/tests/invariants/test_wdap_2a_external_party_principal_and_admission.py` (174 lines). **DO NOT rescaffold**.
- **W-DAP-STACK 2B** — Trust-domain separation + browse (DAP-6, DAP-7, DAP-8-partial).
- **W-DAP-STACK 2C** — Approval routing + controlled operations (DAP-11, DAP-14, DAP-15, DAP-16, DAP-17). **R-C1 marker: `controlled_determination_basis = custody_class_fallback` flip-forbidden** (per PHASE_C plan).
- **W-DAP-STACK 2D** — Objective freeze + assistance chat boundary (DAP-18, DAP-19, DAP-20, DAP-24).
- **W-DAP-STACK 2E** — Metering + cumulative disclosure budget (DAP-21, DAP-22-partial, DAP-25, DAP-26). **R-C2 marker: `au_3b_defensible=False` flip-forbidden**.
- **W-DAP-STACK 2F** — Suspension + revocation (DAP-27, DAP-28, DAP-29).
- **W-DAP-STACK 2G** — Coalition joint evaluation (DAP-34, DAP-35).
- **W-DAP-STACK 2H** — Component boundary + composition close (DAP-30, DAP-31, DAP-32).

### LIFTING (donor code)

- **Nothing new lifted** in M1. The stack composes existing platform primitives:
  - Chokepoint discipline reused from **`services/chokepoint`** (1,403 LOC / 35 tests) — already banked.
  - Shield-Train's admission chokepoint pattern reused (W-Shield-Train-Admission close, ratchet 2894).
  - Solva-V2 assertion floor reused from **`services/solva_v2`** (W-SOLVA-V2-LIFT close, ratchet 3562) — DAP-8 crosses via Solva's assertion boundary per PHASE_C plan §347.

### KEEPING (banked, unchanged)

| Asset | Evidence |
|---|---|
| Solva-V2 seam (assertion boundary, critic seam, intent audit, trace, reasoning faculty) | `backend/services/solva_v2/` · commit `7f6d235a` · ratchet 3562 |
| W1 platform substrate (work_supervisor, job_manifest, kind_registry, governance, runtime_supervisor) | `backend/services/work_supervisor/` · commit `fe01e5e` · ratchet 3392 |
| W1b platform primitives (attribute_stream_bundle, capability_registry, retention_policy) | `backend/services/attribute_stream_bundle/` + `services/capability_registry.py` · commit `5364593` · ratchet 3492 |
| W1c integration proof (spine walk trace) | `phase0/integration_proofs/w1c_integration_proof_trace.md` · commit `e1712a1` · ratchet 3503 |
| W-REGISTRY-EXTENSION-G3 (typed custody class, class enumeration, F&P Registry row) | `backend/services/registry/` + `backend/services/registry_facts/` · commit `33edf56b` · ratchet 3531 |
| W-REGISTRY-FULL-BUILD CP1..CP9 (22 routes + payload contracts + real-data wires + v3 substitution rules) | `backend/services/w_registry_full_build/routers.py` (14,585 B) · commits `318e7cd` → `3a5584c` · ratchet 3098 |
| Rulings wired: DAP R-1 (RATIFIED) + DAP R-4 (DEFAULT 90-day) + DAP R-5 (DEFAULT AI-labs entry) | `backend/services/rulings/default_class_constants.py` · per `RULING_LEDGER.md` |
| Existing untracked DAP 2A scaffolding | `backend/contracts/dap.py` + `backend/services/dap/` + `backend/tests/invariants/test_wdap_2a_*.py` (untracked; landed via mechanical-RED at 2A open) |

### WHEN DONE, THESE PROMISES HOLD

DAP-Spec explicitly binds the following in §9 Build Acceptance Criteria (verbatim from `DAP_Backend_Spec_v1.txt` lines 122-131):

- **`A1` · Compute-to-data** (verbatim): *"attempt, by every available configuration, to move estate data to compute outside the perimeter for a fine-tune job → No configuration permits it; every attempt refused and recorded."* → discharged by **W-DAP-STACK 2H** (component boundary close) via chokepoint refuse-if-egress + Canon-1 §4.1 fail-closed doctrine.
- **`A2` · Browse boundary** (verbatim): *"request unit contents through every browse path, including malformed and crafted requests → Aggregates only returned; no path yields a unit's contents or a sample."* → discharged by **W-DAP-STACK 2B** (browse boundary) via Mtafiti census progressive-disclosure + DAP-6/DAP-7.
- **`A3` · Approval gate** (verbatim): *"submit a controlled request; make the approval service unreachable mid-flight → Request does not execute; expires unexecuted; refusal recorded."* → discharged by **W-DAP-STACK 2C** (approval routing) via DAP-14/DAP-15/DAP-16 + R-C1 fallback + fail-closed refusal.
- **`A4` · Metering completeness** (verbatim): *"run one job of each of the six operations → Six metered events, each with all required fields, each written before its result returned."* → discharged by **W-DAP-STACK 2E** (metering).
- **`A5` · Slow-play detection** (verbatim): *"issue a scripted sequence of individually-permitted requests whose aggregate exceeds entitlement → Detected against cumulative history and raised, not evaluated per request."* → discharged by **W-DAP-STACK 2E** (cumulative disclosure) + **W-DAP-STACK 2G** (coalition joint evaluation).
- **`A6` · Objective freeze** (verbatim): *"attempt to widen a commissioned job's scope through the assistance chat after commission → Refused; a wider scope requires a new job."* → discharged by **W-DAP-STACK 2D** (objective freeze · DAP-18/DAP-20).
- **`A7` · Suspension** (verbatim): *"suspend a party with jobs in flight → All in-flight jobs stop; each recorded as stopped; no job silently completes."* → discharged by **W-DAP-STACK 2F** (DAP-27).
- **`A8` · Trust-domain separation** (verbatim): *"attempt to resolve an estate unit identifier from the party's domain outside a permitted operation → No resolution; attempt recorded."* → discharged by **W-DAP-STACK 2B** (trust-domain separation · DAP-7).
- **`A9` · Key hygiene** (verbatim): *"inspect every record written during a full session → No key material in any record, including receipts and metered events."* → discharged by **W-DAP-STACK 2A** (DAP-13 key issuance discipline).
- **`A10` · Artefact egress** (verbatim): *"complete a fine-tune on controlled units → Weights carry rights posture, hash, derivation from controlled units, and terms cited."* → **partially discharges A10; remainder in M5** (Data-Suite / artefact egress against `services/targeta`).

**Additional canon promises discharged (or partially discharged) by M1:**

- **`Promise #4` · Retained-file custody classes** — Doc-0 STATUS: *"Partial — custody classes are distinguished in practice (A5.3 vs. Promise #4's retained files) but not confirmed as a typed, queryable attribute. See G-3."* Since W-REGISTRY-EXTENSION-G3 already delivered typed queryable `CustodyClass` (KEEPING above), Promise #4 was **partially discharged by G-3**; M1's DAP-1/DAP-2 consume this typed attribute at the DAP admission surface, discharging the remaining "external-party retained-file" dimension. **Remainder** on internal-only retained files: Rules Service (M2).
- **`Promise #22` · MOAC · "every criterion or no service"** — Doc-0 STATUS: *"Met — MOAC, Promise #22: 'every criterion or no service.'"* MOAC itself is banked; M1's DAP-14 (controlled-unit determination) is the DAP-side application of MOAC per DAP-Spec §5. **Reads MOAC, does not re-implement it.**
- **`Promise #25` · Outer gate** — Doc-0 STATUS: *"Met — 'no human may confer eligibility,' consistent with Promise #22's design."* M1's DAP-11 (Download raw data) explicitly cites Promise #25 per DAP-Spec §4 table row 6: *"Outer gate (Promise #25) — not the ordinary crossing."* → **Reads Promise #25, does not re-implement it; M1's DAP-11 gates the crossing.**
- **`Canon-1 §4.1 Fail-closed custody doctrine`** — verbatim: *"If a custody control cannot execute, the operation does not happen."* → discharged structurally across M1 waves 2A/2C/2H (chokepoint refuse-if patterns).
- **`Canon-1 §4.9 Provenance is not optional`** — verbatim: *"A fact that cannot name its source cannot be stored."* → discharged by M1 metering (2E) writing every crossing to the Ledger before result return.
- **`Canon-1 §4.11 Canon before ruling`** — discharged by M1 grounding briefs quoting DAP-Spec §9 verbatim in every gating test docstring (per SO §2 CONDITION 1).

**Promise IDs from the S-set that M1 touches or composes (bounded by Doc-3 scope):**
- **`S-22` (DAP-33)** — *"The system will inspect what leaves, not only who sends it — every output leaving DAP passes a deterministic output gate."* → **partially discharged by M1** (deterministic gate at every component boundary via chokepoint); **remainder in M3** (Watch's reproduction probe + output-gate hardening).
- **`S-23` (DAP-34)** — *"The system will treat a coalition as one actor …"* → **partially discharged by M1** (2G coalition joint evaluation); **remainder in M3** (Watch coordination-signature threshold R-11 · baseline-period-deferred).
- **`S-25` (DAP-35, DAP-36)** — *"The system will bound what the estate releases in total — across all parties, all operations, all time."* → **partially discharged by M1** (2E metering + cumulative disclosure accumulator); **BLOCKED on OPEN owner ruling Security R-7 estate release budget number**. Under R-C1/R-C2 markers, M1 lands the mechanism tests-first with `RELEASE_BUDGET_NUMBER = DEFAULT-PENDING-OVERRIDE`; production-grade close awaits R-7.

**PROCESS that proves M1 discharge** (per SO §3):
- Mechanical RED banked at `phase0/drill_receipts/<ts>_wdap_2a_RED_pre_impl.log` for each sub-wave.
- Double-green byte-match: `BASELINE_GUARD=1 python -m pytest tests/invariants/` × 2 back-to-back.
- Grounding brief per sub-wave in `notes/W_DAP_STACK_2A_grounding_brief.md` etc., verbatim DAP-Spec quotes in every test docstring (SO §2 Condition 1).
- Two-commit local pattern preserved.

---

## §M2 · Rules-Service mechanism + 6 remaining Doc-0 attribute waves

**Owner-ratified shape (confirmed against disk):** ✅ matches `BUILD_STATUS_PERCENT_20260909 §2 rows 4a..4l, row 5`.

### BUILDING

Per `LEVERAGE_AND_GAP_INVENTORY §G.2` Stage-P2 items 5-6 + `BUILD_STATUS_PERCENT §2 row 5` and rows 4a..4l:

- **W-RULE-REGISTRY-BOOTSTRAP** — 286-rule register scaffold (Attr-4 Controls first slice).
- **W-RULES-SERVICE-CEREMONY** — countdown + witness + second-signatory ceremony (Rules-Service R-1..R-4). **R-2 second-signatory named role is OPEN owner-input row per `Ratification_Record_v1` Table 2**.
- **W-RULE-BOOK-LIBRARY** — rule-book library service.
- **W-286-RULE-ENUMERATION-CLASSIFY** — enforcement-class assignment for the remaining 272 rules (G-4 gap).
- **W-DOC0-ATTR1-TCB** — `GET /api/tcb/current` + ledger-on-modify. `tcb_enumeration_v1` BANKED as spec.
- **W-DOC0-ATTR2-SUBSYSTEMS** — declared_interface field + linter (Doc-0 BR-2.1).
- **W-DOC0-ATTR3-TRIAD** — principals/assets/operations catalogs + op→checkpoint mapping (BA-3.3).
- **W-DOC0-ATTR6-REFERENCE-MONITOR** — interface-traverse linter.
- **W-DOC0-ATTR7-BASELINE** — refusal-on-failure invariant + unlowerable-by-measured.
- **W-DOC0-ATTR8-AUDIT-AU3** — six-element AU-3 contract linter globally.
- **W-DOC0-ATTR10-DETERMINISM** — component classification catalog + EU AI Act Art. 14 capabilities a-e. `determinism_inventory_v1` BANKED as spec.
- **W-COHERENCE-BR-11** — contradiction-refusal invariant.
- **W-DOC0-ATTR12-GOVERNANCE-CEREMONY** — fan-in of Attr 1..11.

`[framing, not canon]`: Attr-4 (Controls) and Attr-9 (Change-Control) roll INTO Rules-Service waves (per `BUILD_STATUS §2 row 4d, 4i` verbatim). DO NOT open them as independent waves.

### LIFTING

- **Nothing new lifted** in M2. Rules-Service reads existing OpVal-v1.1 machinery from `services/rulings/` (137 LOC, 3 tests).

### KEEPING

| Asset | Evidence |
|---|---|
| 5 RATIFIED rulings (Rules-Service R-3/R-4, DAP R-1, Agent-Containment R-1/R-2) | `RULING_LEDGER.md` + `backend/services/rulings/default_class_constants.py` |
| 9 DEFAULT-class rulings (Rules-Service R-1, DAP R-4/R-5, Security R-8/R-9/R-10/R-11, Agent-Containment R-3, Pruning R-12) | same |
| `spec_id_index.json` — `rule_criteria_spec_v1` BANKED-DERIVED (ROC-1 ratification 2026-09-09) | `notes/spec_id_index.json` + DECISIONS.md 2026-09-09T~11:40Z |
| G-3 Registry extension (asset-class schema, typed CustodyClass, class enumeration, four-class governance-value taxonomy, F&P Registry 11-field row, ledger-scoped visibility) | `backend/services/registry_facts/` + `backend/services/w_registry_full_build/` · commit `33edf56b` · ratchet 3531 |
| System_Rules_Registry 286 rules INVENTORY | `canon/drops/20260910/extracted/files_15/Master_Requirements_Registry.xlsx` sheet "System Rules Registry" (445 rows) |

### WHEN DONE, THESE PROMISES HOLD

- **`Promise #22` · MOAC "every criterion or no service"** — **fully discharged** by M2's Rules-Service mechanism once Attr-4 Controls (rule-flip ceremony) is in force with the 286-rule enforcement-class fully populated.
- **`Promise #27` · full ceremony** — Doc-0 STATUS: *"Met — Promise #27's full ceremony."* M2 makes ceremony production-grade (R-2 second-signatory named role required).
- **`Promise #29` · "learning may detect, never decide"** — Doc-0 STATUS: *"Met by doctrine … not yet recorded as an applied instance of a published TCB test, because the test itself is not yet published. See G-1, G-10."* → **fully discharged** by M2's W-DOC0-ATTR1-TCB (TCB test published) + W-DOC0-ATTR6-REFERENCE-MONITOR.
- **`Doc-0 Attribute 1` (TCB)** — discharged by W-DOC0-ATTR1-TCB.
- **`Doc-0 Attribute 2` (Subsystem Declaration)** — discharged by W-DOC0-ATTR2-SUBSYSTEMS.
- **`Doc-0 Attribute 3` (Governed Triad · BA-3.3 "every operation maps to exactly one checkpoint")** — discharged by W-DOC0-ATTR3-TRIAD; also **partially discharges Promise #32 handoff generalisation**; remainder in M4 (assistant/journey surfaces).
- **`Doc-0 Attribute 4` (Controls / Rule Registry)** — discharged by W-RULE-REGISTRY-BOOTSTRAP + W-286-RULE-ENUMERATION-CLASSIFY.
- **`Doc-0 Attribute 5` (Checkpoint discipline)** — already ~30% via W-Shield-Train + Registry-Full-Build; **fully discharged by M2** once Rules-Service PDP/PEP/PIP catalog is complete.
- **`Doc-0 Attribute 6` (Reference Monitor)** — discharged by W-DOC0-ATTR6-REFERENCE-MONITOR. **Note per Security_Promise_Set_Amendments Amendment 6**: *"The Watch Upgraded to a Full Reference Monitor Instance … Upgraded to a full Reference Monitor instantiation. Document 3 demonstrates all three defining properties directly."* → the Watch already is a Reference Monitor; Attr-6 fulfilment here means **the second Reference Monitor instance** for the governance side.
- **`Doc-0 Attribute 7` (Mandatory Baseline Ceremony)** — discharged by W-DOC0-ATTR7-BASELINE.
- **`Doc-0 Attribute 8` (Audit Record AU-3)** — discharged by W-DOC0-ATTR8-AUDIT-AU3.
- **`Doc-0 Attribute 9` (Change-Control Ceremony)** — rolled into Rules-Service ceremonial; discharged by W-RULES-SERVICE-CEREMONY.
- **`Doc-0 Attribute 10` (Determinism Boundary)** — discharged by W-DOC0-ATTR10-DETERMINISM.
- **`Doc-0 Attribute 11` (Coherence Enforcement)** — discharged by W-COHERENCE-BR-11. **Note per Security_Promise_Set_Amendments Amendment 7**: A5.9 added to Attr-11 (fail-closed independent of Watch).
- **`Doc-0 Attribute 12` (Governance Ceremony)** — discharged by W-DOC0-ATTR12-GOVERNANCE-CEREMONY.
- **`Canon-1 §4.10 Verdicts are never curated`** — enforced by Rules-Service change-control ceremony (Amendment path only).
- **`Canon-1 §4.11 Canon before ruling`** — enforced structurally by ROC-1 BANKED-DERIVED + rule-firing against on-disk rule set.

**Amendments explicitly discharged in M2:**
- **Amendment 1** (S-7 marked as gap) — carried as a scope-honest limit; M2 does NOT close the spec gap (that requires Doc-3 §A1/A5 amendment ceremony, not M2 mechanism).
- **Amendment 6** (Watch upgraded to full Reference Monitor) — cross-referenced by W-DOC0-ATTR6-REFERENCE-MONITOR to require the governance-side second RM instance (G-6 open for MOAC / distance-gate / format-gate).
- **Amendment 7** (A5.9 added to Attr-11) — discharged by W-COHERENCE-BR-11 asserting Watch-independent fail-closed posture.

**Ruled-values wired at M2 close** (per RULING_LEDGER):
- Rules-Service R-1 = 48h system-ordinary / 7 days system-TCB (DEFAULT wired).
- Rules-Service R-3 = same witness the Watch uses (RATIFIED).
- Rules-Service R-4 = v1 business-type taxonomy (RATIFIED).
- Rules-Service R-2 = OPEN (second-signatory named role) — production-grade close awaits owner input.

**PROCESS that proves M2 discharge** (per SO §3):
- Mechanical RED per wave; double-green byte-match; grounding brief per wave; verbatim canon quotes in every test docstring; two-commit local.

---

## §M3 · Watch (Doc-03 62 BUILD rows) + Registry CP10 DOM proof + Pruning + Agent-Containment

**Owner-ratified shape (confirmed against disk):** ✅ matches `BUILD_STATUS_PERCENT_20260909 §2 rows 1, 7, 8, 9`.

### BUILDING

Per `LEVERAGE_AND_GAP_INVENTORY §G.2` Stage-P2 items 4, 7, 8, 9:

- **W-REGISTRY-FULL-BUILD CP10** — real-Chromium DOM proof + wave-close manifest. **Owner-HOLD lift required.**
- **W-WATCH-STACK (Wave C · 62 rows)** — bait · containment ladder · quarantine copies · external witness signing + tamper alarms · mirage planting / touch detection / severance · Doc03-078 Watch exemption.
- **W-PRUNING-UNLEARNING** — retirement ceremony end-to-end.
- **W-AGENT-CONTAINMENT (AC-1..AC-12)** — mechanism build.

### LIFTING

- **Nothing new lifted** in M3. Watch stack iterates on existing scaffolding.

### KEEPING

| Asset | Evidence |
|---|---|
| Watch scaffolding (15 files, 2,787 LOC, 54 tests) | `backend/services/watch/{containment,continuity,fitness,macho,mark,mirage,mirage_artifacts,mkono,persistence,route_recheck_failure,route_staleness_flag,router,sever_signals,witness}.py` |
| Grey-Mirror scaffolding | `backend/services/grey_mirror/` (2 files, 91 LOC, 2 tests) |
| Rights-Quarantine | `backend/services/rights_quarantine/` (3 files, 262 LOC, 3 tests) |
| Shield-Train pipeline (build+admission+run) | `backend/services/shield_train/` (6 files, 1,120 LOC, 17 tests) · ratchet 2924 |
| Registry CP10 wave-close test file (shelved-untracked, drafted 2026-09-09) | `backend/tests/invariants/test_w_registry_full_build_cp10_wave_close.py` |
| 3 Agent-Containment rulings wired: AC R-1 (RATIFIED · 4 capability ceilings), AC R-2 (RATIFIED · Syni.ai scope-ratifying authority), AC R-3 (DEFAULT · baseline-period sample rate) | `backend/services/rulings/default_class_constants.py` |
| Pruning R-12 ruling wired (DEFAULT · re-derivation) | same |
| `NON_CLAIMS_REGISTER.md` LIM-1..5 (never counted as met requirements) | `notes/NON_CLAIMS_REGISTER.md` |

### WHEN DONE, THESE PROMISES HOLD

**Watch — Security_Assurance_Promise_Set** (verbatim S-row promise, `.xlsx` col 3):

- **`#6` · Watch composite** — *"The platform continuously watches everything happening across the estate and the boundary … "* → **fully discharged by W-WATCH-STACK** (composite over S-1..S-21).
- **`S-1` · Totality of sight** (A3, A6 truth-condition 1) — *"observe every actor, input, and action across the estate and the boundary"* → discharged by W-WATCH-STACK Macho + Totality subsystems.
- **`S-2` · Detect three shapes** (A3 · Promise #7 link) — *"detect the machine-speed attack, the slow play beneath every threshold, and the recruited insider whose behaviour drifts"* → discharged by W-WATCH-STACK three-detection-paths + intent reconciliation.
- **`S-3` · Refinement paths** (A5.6 + C1) — *"route probabilistic suspicion to friction, a narrowed envelope, or the mirage"* → discharged by W-WATCH-STACK mirage entry + narrowed envelope.
- **`S-4` · Four-rung action ladder** (A5.14) — *"annotate, shape, contain, sever — bounded by blast-budget share and friction ceiling"* → discharged by W-WATCH-STACK ladder mechanism.
- **`S-5` · Reversible/bounded/witnessed** (A5.3) — *"every autonomous act reversible, bounded, and witnessed"* → discharged by W-WATCH-STACK TTL + atomic act-and-attest + peer countersignature.
- **`S-6` · One record, two readings** (A3 · A5.5) — *"write every verdict, action, attestation, and mark to the one authoritative ledger"* → **partially discharged by M3**; **remainder** discharged by M2 W-DOC0-ATTR8-AUDIT-AU3 global AU-3 linter.
- **`S-7` · Learning** — **spec-closed 2026-09-13** by Watch Learning Amendment v1 (L-2 + L-4).  Discharged **inside W-WATCH-STACK** (mechanism: certificate-requirement library at Doc-3 A5 seam + A5.22 research loop).  Not built.  Open owner-input rulings: **R-15** (initial library seed), **R-16** (ratifier + cadence).  Supersedes Amendment 1's "Absent → gap" status.
- **`S-8` · Standing drill cadence** (A5.13 · A3) — *"exercise every response rail on a standing drill cadence"* → discharged by W-WATCH-STACK drill loops + receipts.
- **`S-9` · Mirage reconciliation** (C1) — *"on release from the mirage, replay the actor's mirage-period work"* → discharged by W-WATCH-STACK reconciliation-mode mechanism (R-3 baseline-period-deferred value).
- **`S-10` · Ledger continuity RTO 3,600s** (Wave E · CA1-N5) — discharged by W-WATCH-STACK Part-D-proposed recovery mechanism (Amendment 2 gives it a document home).
- **`S-11` · Breach notification 72h** (Wave E · CA1-N2) — discharged by W-WATCH-STACK Part-D-proposed notification mechanism (Amendment 2).
- **`S-12` · Fail-closed independent of Watch** (A5.9) — **already partially discharged by W-Shield-Train + Registry-Full-Build**; M3 finalises the invariant.
- **`S-13` · Detection never decides / response never judges** (A5.1 · C2 verdict seam) — discharged by W-WATCH-STACK Macho/Mkono split.
- **`S-14` · Maximum-autonomous-force gated by closed six-signal registry** (A5.2) — discharged by W-WATCH-STACK sever-signals registry.
- **`S-15` · Non-conformance never convicts** (A5.7) — discharged by W-WATCH-STACK conformance mechanism.
- **`S-16` · Ruled deterministic floor beneath adaptive layers** (A5.8) — discharged by W-WATCH-STACK floor mechanism.
- **`S-17` · No destroy in the Watch** (A3 · A5.3) — discharged by W-WATCH-STACK persistence.
- **`S-18` · Non-exportable tenant-keyed behavioural profile** (A5.12) — discharged by W-WATCH-STACK profile store.
- **`S-19` · Own liveness attested by no-credential witness** (A5.9 · C3) — discharged by W-WATCH-STACK witness + break-in test.
- **`S-20` · One authority one identity** (A5.10 · A5.11 · single-crossing) — discharged by W-WATCH-STACK task-identity mechanism.
- **`S-21` · Mirage deceives outward only** (A5.5 · C1) — discharged by W-WATCH-STACK mirage outward-only invariant.

**DAP-side reference-monitor amendments carried by M3:**
- **`S-22` · Output-inspection deterministic gate** (proposed A5.15 · DAP-33) — **remainder** from M1 discharged by M3's Watch reproduction-probe (R-8 baseline-period-deferred) + boundary gate.
- **`S-23` · Coalition as one actor** (Doc-0 Attr-3 · proposed A5.18 · DAP-34) — **remainder** from M1 discharged by M3's coordination-signature threshold (R-11 baseline-period-deferred).
- **`S-24` · Raiser held to same conformance as target** (proposed A5.17) — discharged by M3's Class-D/Class-A finding mechanism + lineage collapse.
- **`S-25` · Estate-level release budget** (DAP-35 · DAP-36 · Doc-0 Attr-7) — **remainder** from M1 discharged by M3's estate-level accumulator; **BLOCKED on Security R-7 owner-input**.

**Pruning promises:**
- **`S-26` · Remove a unit's influence when withdrawn** (DAP-37 · DAP-38 · Pruning & Unlearning Amendment) — discharged by W-PRUNING-UNLEARNING (T-3, T-4 tags per S-26 col 8). R-12 default (re-derivation) already wired; recall requires owner sign-off per DEFAULT posture.
- **`RBM-20`** (Registry query for pruning) — discharged by W-PRUNING-UNLEARNING Registry-query implementation.

**Registry CP10:**
- **CP10 wave-close** — completes W-REGISTRY-FULL-BUILD; strictly speaking discharges the CP10-scoped wave close only, not a canon promise (the wave itself already carries `Promise #12` fulfilment per Doc-0 STATUS: *"census and connection are specified (Promise #12); a published class list was not located"*). CP10 delivers the missing class-list surface as DOM proof. `[framing, not canon]`

**Agent Swarm Containment:**
- **`AC-1` · Four capability ceilings** (verbatim: no self-replication · no unauthorised resource acquisition · no unauthorised credential escalation · no self-access to oversight) — **rulings landed**; **mechanism discharged by W-AGENT-CONTAINMENT**.
- **`AC-2` · Task-scope starts at minimum · expands only on record+ratification** — discharged.
- **`AC-3` · Every scope expansion logged** — discharged.
- **`AC-4` · Graduated response for novel-in-pattern actions** — discharged (reuses Watch A5.14 pattern per AC-11).
- **`AC-5` · Bounded sample of novel actions to independent review** — discharged. `R-3` = baseline-period-deferred (DEFAULT).
- **`AC-6` · Second independently-scoped evaluator for ambiguity** — discharged.
- **`AC-7` · Oversight mechanism structurally separate** (general form of AC-1(d)) — discharged.
- **`AC-8` · Liveness attested by no-credential component** — **partially discharged**; **`LIM-4` limits**: "confirmed only for actors operating inside Akki's own six engines. Extending it to an arbitrary external agent's action space is a per-deployment engineering task." So AC-8 fully discharged for internal actors; external per-deployment.
- **`AC-9` · Intervention without agent cooperation** — discharged.
- **`AC-10` · Aggregate ceiling across coordinated agents** (reuses A5.18/DAP-34/DAP-35 pattern) — discharged; composed against M1 2G + M3 estate-accumulator.
- **`AC-11` · Ladder mechanism (annotate/shape/contain/sever · blast budget · reversible · time-limited)** (reuses A5.3 · A5.14) — discharged.
- **`AC-12` · Every containment-relevant event on Ledger before completion** — discharged.

**Explicit non-claims held (never discharged, never counted):**
- `LIM-1`: no claim on condition-3 detection-of-novel-danger.
- `LIM-2`: no claim on defending unaffiliated public assets.
- `LIM-3`: no claim on independent audit / red-team / operational track record.
- `LIM-4`: AC-8 external-agent scope is per-deployment.
- `LIM-5`: no shipped tool-vocabulary or task-scope for a specific agent.

**PROCESS that proves M3 discharge:**
- Mechanical RED per wave; double-green byte-match; grounding brief per wave; verbatim canon quotes in every test docstring; two-commit local.
- Watch drill cadence (S-8) proven by drill receipts written to `phase0/drill_receipts/`.
- Own-liveness attestation receipts written to `phase0/witness_attestations/` and `phase0/watch_verdicts/`.

---

## §M4 · Assistant surfaces (Shaping Wizard · Connect Wizard · DAP-20 boundary · Journey handoff)

**Owner-ratified shape (confirmed against disk):** ✅ matches `notes/JOURNEY_AND_ASSISTANT_AUDIT_20260913.md` + `LEVERAGE_AND_GAP_INVENTORY §E.4`.

### BUILDING

- **W-JOURNEY-ASSISTANT** (candidate wave) — owner-charter pending. Comprises:
  - Setup guided sequence (Canon-6 §3) hardening.
  - Connect Wizard (Doc-0 §14 · BR-14.1) surfacing.
  - Shaping / Commission Wizard (Canon-5 §14 · Canon-6 §6) chat+draft-rail surface.
  - DAP assistance chat (DAP-Spec DAP-20) — bounded operator surface for external parties.
  - Registered-handoff contract generalisation (Doc-0 §BR-6.1 · G-13) — Promise #32 remainder.

### LIFTING

- **Nothing new lifted** in M4. Composes existing wizard/chat surfaces.

### KEEPING

| Asset | Evidence |
|---|---|
| Solva refusal envelope (three actions: accept-as-stated · narrow-objective · lower-standard) | `backend/services/solva_v2/` W-SOLVA-V2-LIFT close · CP-S4 · commit `7f6d235a` · ratchet 3562 |
| DAP-20 boundary (assistance chat MUST NOT approve/widen-scope/decide-gate) | landed via M1 W-DAP-STACK 2D · DAP-18/DAP-20 |
| A5.16 Recommendation window (24h · DEFAULT · Security R-10) | wired at `backend/services/rulings/default_class_constants.py` `SECURITY_RECOMMENDATION_WINDOW_HOURS = 24` |
| Existing `services/wizard/` (10 files · 1,258 LOC · 14 tests) | Setup guided sequence + Connect Wizard chrome |
| `services/chat/` (2 files · 99 LOC · 4 tests) | Chat surface primitive |
| `services/credentials_paste/` (3 files · 294 LOC · 6 tests) | Data-source connect flow |
| `services/critic_pass/` (8 files · 1,035 LOC · 4 tests) | Canon-7 §44 Tier-2 critic mechanism (already wired at M1 via 2A-2H) |

### WHEN DONE, THESE PROMISES HOLD

- **`Promise #32` · Registered handoff contract per crossing** — Doc-0 STATUS: *"Partial — Promise #32 is itself marked Partial in canon: 'one concrete instance … no generalised registered handoff contract per crossing.' See G-13."* → **fully discharged by M4** via the generalised handoff-contract mechanism (composed on M2 W-DOC0-ATTR3-TRIAD BA-3.3 op→checkpoint mapping).
- **`Doc-0 BR-6.1 STATUS`** (verbatim from Doc-0): *"Partial — Promise #32 is itself marked Partial in canon: 'one concrete instance … no generalised registered handoff contract per crossing.' See G-13."* → discharged with M4 close.
- **`Canon-5 §14 Commission — The Shaping Wizard`** (verbatim, `notes/JOURNEY_AND_ASSISTANT_AUDIT §1.2`): *"Layout: a chat pane on one side, an objective draft rail on the other … The operator states intent; the agent asks for mandatory fields and never proposes on them. An estate-check chip renders inline before any feasibility-dependent question is asked … Every turn is grounded in a real estate read; no fabricated availability, ever, under any circumstance."* → discharged by M4 Shaping Wizard build.
- **`Canon-6 §3 Setup guided sequence`** — *"guided sequence captures … each explained in one plain sentence with a recommended default …"* → discharged by M4.
- **`Canon-6 §6 Commissioning`** — *"turns a need into governed work in five steps … all shown before any commitment"* → discharged by M4.
- **`Canon-6 §12 What Every Journey Above Has in Common`** (verbatim, `notes/JOURNEY_AND_ASSISTANT_AUDIT §1.4`): *"Three verdicts, never more. Every step in every journey above resolves to answered, held, or refused — never a fourth outcome invented to smooth over an awkward moment."* → discharged structurally by every M4 wizard sending its verdicts through the Solva refusal envelope (KEEPING above).
- **`DAP-Spec DAP-20`** (verbatim from `DAP_Backend_Spec_v1.txt`): *"The portal's assistance chat MAY help a party shape an objective, identify relevant scope, or understand terms, before commission. It MUST NOT approve, widen scope after commission, or decide any gate. It proposes; the gates decide."* → **verified during M4 close** (already landed at M1; M4 confirms the assistance-chat surface honours the boundary).
- **`Canon-1 §4.6 Extension not proliferation`** — *"New capability extends an existing component."* → structural bind on M4 (adds wizard modality, not sibling registry).

**PROCESS that proves M4 discharge:**
- Mechanical RED banked; double-green byte-match; grounding brief `notes/W_JOURNEY_ASSISTANT_grounding_brief.md` quoting Canon-6 §3/§6/§12 + Canon-5 §14 + DAP-20 verbatim in every test docstring.
- Playwright end-to-end proof of Shaping Wizard chat+draft-rail flow (per Registry CP10 pattern) — receipts to `phase0/drill_receipts/screenshots/`.
- Handoff-contract instances written to a new `phase0/handoff_records/` dir (name TBD at wave open).

**M4 discharges no S-* row or DAP-A* build criterion directly; those are runtime security/DAP promises, not journey promises.**

---

## §M5 · Data-Suite-v2 (donor lift) + Audio-POC (build)

**Owner-ratified shape (confirmed against disk):** ✅ matches `BUILD_STATUS_PERCENT_20260909 §2 row 10` + W2 BLOCKED per DECISIONS.md 2026-09-13 W1c-close.

### BUILDING

- **W-AUDIO-POC** — first real-audio job under the W1/W1b/W1c substrate (per `notes/W_AUDIO_POC_SCOPING_20260912.md` and `AUDIO_INTELLIGENCE_PLANE_SPEC_DEEP_EXTRACT.md`). **BLOCKED on three owner operational rulings** (per DECISIONS 2026-09-13 W1c-close item 9): Path A/B/C storage ruling · NAS network path · 3-station confirm.

### LIFTING

- **`W-DATA-SUITE-v2-LIFT`** — 3 surfaces (per BUILD_STATUS §2 row 10).
- **`W-TRUST-SURFACE-v2`** — 2 surfaces.
- **`W-EXECUTIVE-SUITE-v2-LIFT`** — 7 surfaces.
- **Donor sources:**
  - **`repos/Akki-Executive-Core/backend/services/`** — 17 top-level dirs incl. `analysis_lifecycle.py`, `analyze_workspace/`, `cohort/`, `deck_generation_jobs.py`, `documents/`, `ideas_engine/`, `inbox_routing/`, `monitor/`, `open_questions/`, `platform_kb.py`, `solva/`, `solva_v2/`, `solva_voice_audit/`, `synisense/`, `tasks/`, `tasks_initiatives/`, `work_studio/`, `workbook_analyzer/` (candidates for Executive-Suite-v2 lift).
  - **`repos/Akki-Executive-Final/backend/services/`** — 15 top-level dirs; sibling of Executive-Core (Q3 DEFAULT-PENDING-OVERRIDE: excluded unless owner overrides).
- **Lift discipline** — case-agnostic-only per W-SOLVA-V2-LIFT CP-S8 precedent (executive-domain negative-scan · word-boundary).

### KEEPING

| Asset | Evidence |
|---|---|
| W2 audio scoping | `notes/W_AUDIO_POC_SCOPING_20260912.md` (40,584 B) |
| Audio-Plane spec deep extract | `notes/AUDIO_INTELLIGENCE_PLANE_SPEC_DEEP_EXTRACT.md` (102,393 B) |
| Audio journey capability audit | `notes/AUDIO_AUTONOMOUS_JOURNEY_CAPABILITY_ASSESSMENT.md` (74,550 B) |
| W-Audio-Census Addendum ruling (Ruling #2 · copyright layer · `licence_class:owner_full_rights`) | DECISIONS.md 2026-09-12T~12:00Z + `services/perception/eab_1_pipeline/a2_license_class.py` |
| All existing Data-Suite / Trust / Executive-Suite surface prototypes | `notes/prototype_inventory_v8.md` (57,275 B) + `notes/SURFACE_AUDIT_v2_prototype_20260907.md` (41,898 B) |

### WHEN DONE, THESE PROMISES HOLD

- **DAP-Spec `A10` · Artefact egress remainder** from M1 → **fully discharged by M5** W-DATA-SUITE-v2-LIFT: weights carry rights posture, hash, derivation from controlled units, and terms cited.
- **`Audio-Plane §1.2 no parallel machinery`** — enforced structurally by W-AUDIO-POC composing existing platform primitives.
- **`Canon-1 §4.6 Extension not proliferation`** — enforced structurally.
- **`Promise #12` · Census and connection** (Doc-0 STATUS: partial) — **fully discharged by M5** via Audio-POC extending Mtafiti census with audio modality (Canon-1 §4.6 extension, not sibling registry).

**BLOCKED items (not discharged until owner unblocks):**
- Storage Path A/B/C ruling for audio artefacts.
- NAS network path.
- 3-station confirm.
- Six other Audio-related open governance chokepoints per Audio-Census scoping doc §V.5: KDPA biometric, KDPA named-individuals, cross-border §48, purpose-limitation §51, DAP R-6 pricing, DAP R-7 disclosure budget.

**PROCESS that proves M5 discharge** (when unblocked):
- Case-agnostic lift discipline (executive-domain negative-scan per W-SOLVA-V2-LIFT CP-S8).
- Audio-POC ratchet-bumping close under BASELINE_GUARD=1 with real audio job's every crossing metered.

---

## §COV · COVERAGE-GAP CROSS-CHECK

**Promise catalog entries NOT discharged by any milestone above:**

| Promise ID | Source | Why not discharged | Owner scope question |
|---|---|---|---|
| **`S-7`** · "Learn" — **spec-closed 2026-09-13 by Watch Learning Amendment v1 (L-2 + L-4)** | Security_Assurance_Promise_Set **v3** (sha `51d52ebd...`) + Watch_Learning_Amendment_v1 (sha `eb8a0bec...`) | Was "Absent → gap" per Amendment 1; now `Absent → new (spec-closed, 13 Sep 2026)`.  Mechanism: certificate-requirement library + research loop.  Discharged INSIDE **W-WATCH-STACK** (M3) — no new wave.  Open owner-input rulings: R-15, R-16. | Owner: no plan change; row updated in place per 2026-09-13 owner constraint. |
| **`LIM-1..5`** · agent_containment_spec non-claims | NON_CLAIMS_REGISTER.md | Non-claims by design. Never discharged. Rows are here for owner awareness only. | — |
| **`Amendment 8`** · scope statement for eradication / communication / evidence custody | Security_Promise_Set_Amendments.txt | Amendment 8: *"Recommend an explicit scope statement in Document 3, resolving one of two ways: (a) name these three as deliberately out of the Watch's scope … with that function identified; or (b) declare them open gaps."* No milestone opens a new function for eradication / external communication / evidence custody. | Owner ruling required: is this M3 scope creep, a new milestone, or explicitly out-of-scope? |
| **`Doc-0 Attribute 12 · Governance Ceremony`** | Doc-0 governance architecture | Listed in M2's BUILDING but explicitly fan-in on Attributes 1-11 so cannot close until all others land. | Owner-confirm: Attr-12 close = the M2 end-of-milestone gate, not a standalone. |
| **`DAP R-6`** pricing model | RULING_LEDGER.md OPEN #2 | Genuinely open commercial owner-input. Neither M1 nor M5 discharges it as a mechanism; but its ABSENCE does not block M1 acceptance criteria A1..A10 — R-6 gates DAP-22 pricing/billing wave. | Owner ruling required to close DAP-22 to production grade. |
| **`WPW R-2`** external-release signatory | RULING_LEDGER.md OPEN #3 | WPW Tier 3 remains blocked. **Not in any milestone above.** | Owner scope question: does WPW Tier 3 enter M2 (Rules-Service ceremonial) or a separate M-milestone? Currently unassigned. |
| **`DAP R-2`** approving-authority named person | Ratification_Record_v1 Section 3 R-2 | OPEN owner-input. M1's DAP-14/DAP-15 approval routing lands mechanism tests-first with `APPROVING_AUTHORITY = DEFAULT-PENDING-OVERRIDE`. | Owner ruling required for production-grade close. |
| **`Rules-Service R-2`** second-signatory named role | Ratification_Record_v1 Section 2 R-2 | OPEN owner-input. Present in Ratification_Record but **NOT in RULING_LEDGER's 4-OPEN** (book-keeping gap already flagged in `LEVERAGE_AND_GAP_INVENTORY §D.2`). | Owner ruling required. |
| **`DPO-S2`** reflection contract | `notes/DPO_S2_REFLECTION_CANDIDATES_20260913.md` | Semantic engine gap. Not a canonical promise ID but blocks Solva-V2 reflection close. **Not assigned to any milestone above** because owner must select one of 3-5 candidates first. | Owner ruling required: which candidate, and does the close land as a Solva-V2 follow-on or as an M2 sub-wave? |

**Total un-covered promise/ruling items: 9** (of which 2 are non-claims by design and 4 are owner-input openings; 3 need scope decisions).

---

## §ORPH · ORPHAN-WORK CROSS-CHECK

**Milestone work that discharges NO catalogued promise:**

| Work item | Milestone | Nature | Scope question |
|---|---|---|---|
| **`STATE/NEXT.md` + `STATE/PINS.md` book-keeping refresh** | M0 (deferred per Q5) | Operational hygiene | Not a promise-discharge item. Confirm deferral is acceptable. |
| **`REUSE_ASSESSMENT_20260913.md` / `BUILD_STRATEGY_20260913.md` supersession** | M0 | Assessment-doc lineage | Discharges the SO §2 engagement-discipline meta-promise, not a canonical runtime promise. |
| **`Doc-0 G-8` fix** (Reliable-time-source control) | Not assigned to M0..M5 | R-C2 marker in PHASE_C plan | Currently carried as a wave-honest LIMIT across M1 (au_3b_defensible=False). Owner scope question: is G-8 a separate M-milestone, or a sub-wave inside M2? Doc-0 STATUS says *"Spec-closed. Not built."* |
| **`G-3` full closure remainder** (general triad formalisation + Mtafiti full asset-inventory extension) | Not assigned to M0..M5 | Doc-0 Part 3 Gap Register row | *W-REGISTRY-EXTENSION-G3 closed the mechanical half.* The remainder — Mtafiti-side asset-inventory generalisation — falls into no current milestone. Owner scope question: M2 Attr-3 or a separate wave? |
| **`W-MTAFITI-GPU-EMBEDDINGS`** + **`W-MTAFITI-DEEP-SWEEP`** follow-ons (enumerated in NEXT.md 2026-09-12T~07:35Z) | Not assigned to M0..M5 | Follow-on to closed W-MTAFITI-GPU-DISCOVERY | Owner scope question: are these deferred, or are they M5-adjacent? Neither maps to a Promise ID. |
| **`Sysadmin follow-up` on 9 SG-blocked hosts** (enumerated in NEXT.md 2026-09-12T~07:35Z) | Not assigned | Environmental / discovery surface | Not a promise-discharge item. |

**Total orphan work items: 6** (of which 2 are M0 book-keeping, 4 are follow-on/gap items that need owner scope rulings to place in a milestone).

---

## §CONFIRM · Shape correction against disk

The owner-proposed BUILD/LIFT/KEEP shape checked against disk:

- **M0 building canon-delta extractions + superseded reuse/strategy delta; keeping Aug-14 corpus + 3562 baseline.** ✅ **Confirmed**. Add: also carries the STATE/NEXT.md + STATE/PINS.md book-keeping-refresh option (deferred per Q5).
- **M1 building DAP-1..30 (admission/trust/crossing/approval/metering); lifting nothing new; keeping Solva-V2 seam + W1/W1b/W1c substrate + landing existing untracked 2A scaffolding (NOT rebuild).** ✅ **Confirmed**. Add: also keeps W-REGISTRY-FULL-BUILD CP1..CP9 (routes/payload contracts) and W-REGISTRY-EXTENSION-G3 (typed CustodyClass) as prerequisites.
- **M2 building Rules-Service mechanism + 6 remaining Doc-0 attribute waves; keeping ratified rulings + G-3 registry extension.** ⚠️ **Confirmed with correction**: it is not 6 remaining Doc-0 attribute waves — it is **all 7 remaining attribute waves** (Attr 1, 2, 3, 6, 7, 8, 10, 11, 12 = 9 attributes to land, of which Attr 4 rolls into Rules-Service and Attr 5 is already ~30%; Attr 9 rolls into Rules-Service change-control ceremonial). Correct count = **7 independent Doc-0 attribute waves + 4 Rules-Service sub-waves** = 11 sub-waves in M2. See §M2 BUILDING above for the full list.
- **M3 building Watch 62-row mechanism + Registry CP10 DOM proof + Pruning + Agent-Containment; keeping existing Watch/CP10 scaffolding.** ✅ **Confirmed**.
- **M4 building assistant surfaces; keeping Solva refusal envelope + DAP-20 boundary + A5.16 provenance from M1.** ⚠️ **Confirmed with two clarifications**: (a) A5.16 is the **Watch recommendation window ruling (Security R-10 = 24h · DEFAULT)**, not a "provenance" clause; it belongs in the KEEPING list of M4 as an already-wired ruling constant. (b) Provenance-per-form (Charter P8) is a distinct promise carried by Canon-4 (Solva assertion floor) and Canon-8 (record matrix) — it is **kept unchanged from M1's W-SOLVA-V2-LIFT** rather than lifted into M4.
- **M5 lifting Data-Suite-v2 donor + building Audio-POC; blocked on owner operational rulings.** ✅ **Confirmed**.

---

## §END · Summary of discharged-promise coverage

| Milestone | Count of promise IDs discharged | Ownership |
|---|--:|---|
| **M0** | 0 canon promises · discharges SO §2 engagement discipline + Canon-1 §4.11 doctrine | book-keeping |
| **M1** | DAP-A1, A2, A3, A4, A5, A6, A7, A8, A9 (full); A10 (partial); DAP-33/34/35 (partial); Promise #4 partial; Promise #22, #25 (consumed); doctrines §4.1, §4.9, §4.11 | 10 DAP-A + 3 partial S + 2 Promise-# + 3 doctrines |
| **M2** | Doc-0 Attr 1, 2, 3, 4, 5 (complete), 6, 7, 8, 9, 10, 11, 12; Rules-Service ceremony R-1/R-3/R-4; Promise #22 (fully), #27, #29; Amendments 6, 7; doctrines §4.10, §4.11 | 12 Attributes + 3 Rules-R + 3 Promise-# + 2 Amendments + 2 doctrines |
| **M3** | Watch composite #6 + S-1..S-21 (S-7 now spec-closed per Watch Learning Amendment v1); S-10/S-11 (Amendment 2); S-22/S-23/S-25 (partial remainders); S-24, S-26; **S-27 (Voice Amendment)**; **S-28, S-29 (Watch Learning Amendment L-1..L-5 · new 2026-09-13)**; AC-1..AC-12 + **AC-15..AC-18 (Watch Learning Amendment · additive to existing W-AGENT-CONTAINMENT)**; RBM-20 + **RBM-23 (Watch Learning Amendment · additive rule class)**; Registry CP10 (wave close); doctrine §4.1 | 1 composite + 23 S + 3 partial-S + 16 AC + 2 RBM + 1 CP-close + 1 doctrine |
| **M4** | Promise #32 (fully); Canon-5 §14; Canon-6 §3 / §6 / §12; DAP-20 boundary verified; doctrine §4.6 | 1 Promise-# + 4 canon sections + 1 doctrine |
| **M5** | DAP-A10 (remainder); Promise #12 (fully); Audio-Plane §1.2; doctrine §4.6 | 1 DAP-A remainder + 1 Promise-# + 1 canon section + 1 doctrine |

**Coverage gap total**: 9 (2 non-claims by design · 4 owner-input openings · 3 scope decisions).

**Orphan-work total**: 6 (2 M0 book-keeping · 4 follow-on/gap items needing owner scope rulings).

---

## HALT

**No build, no scaffolding, no extraction opens on the strength of this note.** Awaiting owner ratification of:

1. **§CONFIRM corrections** — accept the two clarifications (M2 = 11 sub-waves total; M4 A5.16 = ruling, not provenance-clause).
2. **§COV coverage-gap dispositions** — 9 items each require an explicit owner ruling (spec-fix vs defer vs owner-input).
3. **§ORPH orphan-work placements** — 6 items each need placement in a milestone or explicit deferral.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
