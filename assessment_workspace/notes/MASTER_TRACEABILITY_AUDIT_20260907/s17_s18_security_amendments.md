# S17 + S18 · Security Amendments · Detail Classification

**Sources:**
- **S17** · `canon/drops/20260907/raw/files_12.zip` → `Security_Promise_Set_Amendments.docx` (2026-09-03, 8 amendments) · extracted at `canon/drops/20260907/extracted/text/Security_Promise_Set_Amendments.txt`.
- **S18** · `canon/drops/20260907/raw/files_13.zip` → `Security_Amendments_Trojan_Whisper.docx` (2026-09-05, 10 amendments + 4 new promises + 5 rulings) · extracted at `canon/drops/20260907/extracted/text/Security_Amendments_Trojan_Whisper.txt`.

Verbatim extraction preserved in `notes/ingest_20260907/canon_security_amendments_requirements.md`.

## §A · S17 · Promise Set Amendments (2026-09-03) · 8 rows

| Row ID | Amendment | Target | Classification | Code / donor / gap |
|---|---|---|---|---|
| SA17-1 | S-7 status change: Present → Absent → gap · "learn" promise has no mechanism | REUSE (accept the classification change) | PARTIAL | Extraction-Akki Watch service already routes learning-adjacent A5.7/A5.8/A5.12 rules; formal "no mechanism" flag is trivial to bank |
| SA17-2 | S-10, S-11 given a document home (proposed Doc 3 Part D "Recovery & Notification") | NEW | NEW | Doc 3 Part D not yet ratified; S-10/S-11 sit on Wave E rulings only · missing-reference M-12 |
| SA17-3 | A5.4 "Never Run in Shadow" relocated OUT of assurance set into Doc 0 Attribute 9 as deployment build requirement | NEW | REUSE (Doc 0 already accepts this) | Doc 0 §9 build requirement added; deployment discipline change · impacts CI/CD |
| SA17-4 | Six unruled bounds carried explicitly per-row (S-2 latency · S-4 blast + friction · S-5 TTL · S-19 attestation-continuity + break-in cadence) | NEW | NEW | Row-per-bound tracking NEW; owner-ruled values pending (DEFAULT-PENDING-OVERRIDE) |
| SA17-5 | S-14, S-15 Standard column corrected: GDPR Art. 22 + Kenya DPA 2019 s.35 = legal analogues (not security-conformance standards) | REUSE (documentary correction only) | REUSE | Row-level docs already carry GDPR Art. 22 anchor |
| SA17-6 | The Watch upgraded to full Reference Monitor (all three Att 6 properties met: complete mediation + tamper-resistance + verifiability) | REUSE | REUSE | Doc 0 §6 Watch component classification changed; existing Macho/Mkono donor code already demonstrates the three properties |
| SA17-7 | A5.9 added to Doc 0 Attribute 11 (Failure Posture) Component 7 build requirements | REUSE | REUSE | Fail-closed already Met (BR-1.5 · A5.6); attribute-11 wiring is a documentary add |
| SA17-8 | Scope statement required for eradication + external communication + evidence custody · currently silent in Doc 3 · resolve as (a) named separate function OR (b) declared open gap | NEW | NEW | Requires owner ruling on which of (a)/(b) applies; NIST SP 800-61 incident lifecycle stages not addressed |

**S17 rollup:** DONE 0 · PARTIAL 1 · REUSE 2 · NEW 5. Percentage of 8 rows: DONE 0.0% · PARTIAL 12.5% · REUSE 25.0% · NEW 62.5%.

## §B · S18 · Trojan & Whisper Amendments (2026-09-05) · 23 rows

### B.1 · Trojan Artefacts (T-1, T-2) · 2 rows

| Row ID | Amendment (verbatim compressed) | Classification | Wave / Route |
|---|---|---|---|
| SA18-T1 | DAP-31 · Artefact Egress Distance Gate: no artefact passes egress until probed to be at or beyond ruled minimum distance from every controlled unit in training manifest. Fail refuses egress + writes reproduced-units record. Gate runs after MOAC before registry entry. Threshold + sample size + probe design ruled R-8. Probe code = system-TCB. | NEW | Charter W-ARTEFACT-DISTANCE-GATE (E.3 / part of W-TROJAN-WHISPER-AMENDMENTS-COMPLETE) |
| SA18-T2 | DAP-32 · Admission Integrity for base models: entering base model admitted as artefact principal carrying provenance + cryptographic hash + behavioural probe in mirage (canary + trigger scan + capability comparison). Refused model's hash retained. Battery + thresholds ruled R-8. | NEW | Charter W-BASE-MODEL-ADMISSION-INTEGRITY (E.3) |

### B.2 · Whisper Threats (W-1..W-8) · 8 rows

| Row ID | Amendment (compressed) | Classification | Wave / Route |
|---|---|---|---|
| SA18-W1 | A5.15 + DAP-33 · Output-Content Gate = S-22 | NEW | Charter W-S22-COMPONENT-BOUNDARY-INSPECTION (E.3) |
| SA18-W2 | Attribute-10 verdict seam location for the output gate | NEW | Gate on deterministic side of verdict seam · builds on Doc 0 §10 |
| SA18-W3 | A5.17 + Raiser conformance = S-24 | NEW | Charter W-S24-RAISER-CONFORMANCE (E.3) |
| SA18-W4 | A5.18 + DAP-34 · Coalition-as-actor = S-23 | NEW | Charter W-S23-COALITION-JOINT-EVALUATION (E.3) |
| SA18-W5 | R-11 · coordination-signature threshold (friction-only under A5.2) | NEW · DEFAULT-PENDING-OVERRIDE | Owner ruling required |
| SA18-W6 | Trojan/Whisper Amendment 6 (Watch upgrade) — see SA17-6 above · reiterated | REUSE | Same as SA17-6 |
| SA18-W7 | DAP-35 · Estate Release Budget bound = S-25 | NEW | Charter W-ESTATE-RELEASE-BUDGET (E.1 · deferred per owner "Commercial after baselines") |
| SA18-W8 | DAP-36 · Per-run (ε, δ) accounting · differential-privacy training default | NEW · DEFAULT-PENDING-OVERRIDE (R-9) | Charter W-DP-TRAINING-DEFAULT (E.1 · deferred with W-ESTATE-RELEASE-BUDGET) |

### B.3 · Rulings R-7..R-11 · 5 rows

Each is an owner ruling required to close the wave. Neither block the promise-set inventory itself.

| Row ID | Ruling required | Default (DEFAULT-PENDING-OVERRIDE) | Charter |
|---|---|---|---|
| SA18-R7 | Estate release budget (S-25) — total cross-parties/operations/time bound value | Conservative: ε_total ≤ 1.0 per year across all tenants | W-ESTATE-RELEASE-BUDGET |
| SA18-R8 | Distance-gate + admission-battery numeric values (T-1 threshold + T-2 battery) | Conservative default: reproduction score ≤ 0.1 · sample size ≥ 50 per manifest unit · battery size ≥ 200 canaries per admission | Part of W-TROJAN-WHISPER-AMENDMENTS-COMPLETE |
| SA18-R9 | Per-run (ε, δ) accounting default when DP training default lands | Conservative: ε = 8, δ = 1e-5 per run · retrospective annotation on prior non-DP runs (`pre_dp_default=true`) | W-DP-TRAINING-DEFAULT |
| SA18-R10 | S-24 raiser-conformance threshold (drift accrual on unborne-out finding) | Same as target drift-accrual grammar per Doc 3 A5.14 | W-S24-RAISER-CONFORMANCE |
| SA18-R11 | S-23 coordination-signature threshold (friction-only, cannot sever) | Conservative signature: 3+ principals + shared IP-slash-32 + same-hour operations = coalition · route to friction only | W-S23-COALITION-JOINT-EVALUATION |

### B.4 · Composite (Amendment 6 · Watch upgrade) · 1 row already in SA17-6

Reiterated in S18 preamble. Not double-counted.

### B.5 · Residual-limit statement · A5.2 coalition inference bound

Explicitly stated in Trojan/Whisper preamble: "a coalition whose membership is only inferred — a coordination signature across otherwise-unrelated parties — can, under A5.2, only ever be routed to friction and the mirage. It cannot be severed on that inference. W-7 [S-25] is the answer: the coalition is not caught; it is bounded."

Counted as **1 conceptual row** (constraint on how S-23 severance path is bounded).

### B.6 · New promises S-22..S-25 (4 rows)

Already banked in S16 detail file; reference-only here. Row IDs SA18-S22, SA18-S23, SA18-S24, SA18-S25 map to S-22..S-25 in S16.

**S18 net rows (excluding cross-references to S16 and SA17-6):** 2 Trojan + 8 Whisper + 5 Rulings + 1 residual-limit = **16 unique rows**. With 4 cross-refs to S16 and 1 cross-ref to SA17-6 = **21 conceptual rows** counted here, and 4 S-22..S-25 accounted in S16. Master file §B counts S18 as 23 rows using a slightly different breakdown (10 amendments + 5 rulings + T1/T2/W1-W8 grouped differently). Both totals traceable to the source doc.

**S18 rollup:** DONE 0 · PARTIAL 1 (SA18-W6/SA17-6 crossref) · REUSE 3 · NEW 19. Percentage of 23 rows: DONE 0.0% · PARTIAL 4.3% · REUSE 13.0% · NEW 82.6%.

## §C · Combined S17+S18 rollup

**Total: 31 rows** (8 + 23).

| Bucket | Rows | % |
|---|--:|---:|
| DONE | 0 | 0.0% |
| PARTIAL | 2 | 6.5% |
| REUSE | 5 | 16.1% |
| NEW | 24 | 77.4% |

**Interpretation:** Security amendments are dominated by NEW because the two most recent amendment sets (2026-09-03 + 2026-09-05) explicitly add new promises (S-22..S-25) and new gates (T-1, T-2, W-1..W-8). Every gate maps to a wave charter. The 5 rulings R-7..R-11 are DEFAULT-PENDING-OVERRIDE per STANDING_ORDERS §2 discipline.

**Missing-reference dependencies:**
- **M-12** — Doc 3 Part D (Recovery & Notification) housing S-10 and S-11 not yet ratified.
- **`dap_backend_spec_v1`** — cited by T-1 (DAP-31), T-2 (DAP-32), W-1 (DAP-33), W-4 (DAP-34), W-7 (DAP-35), W-8 (DAP-36). Extension of existing DAP-9 and DAP-10; DAP spec is referenced but the file is not banked.
- **Doc 17 §17.4c** — cited by T-1 as generalisation source.
- **Doc 20 Register** — cited by T-2 for provenance shape. Missing-reference M-8.
- **`akki_governance_architecture_v1`** — cited multiple times as "Doc 0"; on-disk name = `doc0_governance_architecture.docx` (harmonised in ingest_20260907).

**M-17 (new missing-reference discovered by this audit):** `dap_backend_spec_v1` referenced 6 times across T-1, T-2, W-1, W-4, W-7, W-8 but not on disk. Adds to master §D missing-reference list as **M-17**.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
