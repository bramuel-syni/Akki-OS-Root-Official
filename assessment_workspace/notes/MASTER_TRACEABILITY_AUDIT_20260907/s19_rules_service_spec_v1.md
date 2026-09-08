# S19 · Rules Service Spec v1 · Detail Classification

**Source:** `canon/drops/20260907/extracted/files_11/Rules_Service_Spec_v1.docx` (sha256 `9652fb47…`) · extracted at `canon/drops/20260907/extracted/text/Rules_Service_Spec_v1.txt` · verbatim in `notes/ingest_20260907/canon_rules_service_spec_v1_requirements.md`. **Draft v1 · 4 September 2026 · every requirement PROPOSED until ratified.**

**Row inventory: 31** = 5 invariants (I-1..I-5) + 22 normative requirements (RBM-1..RBM-22) + 4 rulings-parked (R-1..R-4). Plus supporting: 10 business-type taxonomy entries (§E) + 7 build acceptance tests A1-A7 (§F) — these are downstream of the 31 rows.

## §A · Invariants I-1..I-5

Doc 0 mapping: Rules Service Spec closes 4 Doc 0 gaps directly per §1 verbatim: **G-2** (Rule Registry as standing artefact), **G-4** (assessment procedures per rule), **G-5** (named PAP per checkpoint), **G-9** (documented change-control procedure).

| Row ID | Invariant (verbatim) | This audit classification | Code path / donor / gap |
|---|---|---|---|
| RS-I-1 | No rule is in force that has not completed the ceremony for its tier | NEW | Ceremony code absent · charter W-RULES-SERVICE-CEREMONY (master §E.2) |
| RS-I-2 | Every in-force rule is in Registry with every field ROC-10 requires | NEW | System Rules Registry Enforcement Class + Assessment Procedure columns empty; missing-reference M-4 (ROC-10) |
| RS-I-3 | No customer rule relaxes a system rule STRUCTURAL or MECHANICAL | NEW | Enforcement Class unpopulated; RBM-6 check un-firable |
| RS-I-4 | Every state change written to Ledger append-only BEFORE change takes effect | PARTIAL | Ledger append exists; "before" precondition NEW · same facet as S-6 |
| RS-I-5 | Rules Service's own rules change only through its own ceremony (administers, not edits) | NEW | Self-governance mechanism NEW · RBM-21 test A4 |

## §B · Normative Requirements RBM-1..RBM-22

### B.1 · Authoring (RBM-1..RBM-4)

| Row ID | Requirement (compressed verbatim) | Classification | Code / donor / gap |
|---|---|---|---|
| RS-RBM-1 | Rule authored in plain language + MUST carry all 9 fields (ID · origination + citation · owning subsystem · enforcement class · domain · tier · assessment procedure · status=PROPOSED) at creation. Authoring MUST refuse missing field. | NEW | Authoring endpoint NEW · frontend surface NEW · rule schema NEW |
| RS-RBM-2 | Drafting assistance MAY propose text/classification/tier/procedure but every proposal marked as assisted and MUST be human-confirmed before PROPOSED (assistant never ratifies). [Att 10] | NEW | Assisted-authoring wire NEW · Doc 0 Att 10 seam prerequisite |
| RS-RBM-3 | Mnemonic prefix MUST be reserved through Rules Service before first use. Collision refused at reservation + recorded. [ROC-6] | NEW | Prefix-reservation service NEW · missing-reference M-6 (ROC-6) |
| RS-RBM-4 | Rule's tier declared at authoring; TCB-tier if governs TCB component, else system-ordinary; tenant rules = customer tier | NEW | Tier declaration NEW · depends on W-TCB-ENUMERATION (Doc 0 §1 BA-1.3) |

### B.2 · Impact Analysis (RBM-5, RBM-6)

| Row ID | Requirement (compressed) | Classification | Code / donor / gap |
|---|---|---|---|
| RS-RBM-5 | Before countersign, Rules Service MUST produce impact record: for amendment/retirement, every rule/checkpoint/component/profile citing/depending on the rule; for new rule, every checkpoint/component it would constrain | NEW | Impact record schema + traversal NEW · [NIST CM-3] |
| RS-RBM-6 | For every customer + adopted rule-book rule, MUST check against system rule set + MUST refuse any that would relax STRUCTURAL/MECHANICAL. Refusal names the system rule. | NEW | Conflict-check gate NEW · depends on W-286-RULE-ENUMERATION-CLASSIFY (Enforcement Class population) · missing-reference M-3 |

### B.3 · Ceremony (RBM-7..RBM-11)

| Row ID | Requirement | Classification | Code / donor / gap |
|---|---|---|---|
| RS-RBM-7 | System-ordinary + customer ceremony: propose → impact → countersign by second named authority → cancellable countdown → apply → re-verify. Countdown length ruled per tier (§9 R-1). | NEW | Ceremony state machine NEW · owner R-1 pending |
| RS-RBM-8 | System-TCB ceremony: as RBM-7 + platform's slowest countdown + external witness holding no credentials over governed component. [Doc 3 A5.8, A5.11; Doc 0 BR-7.3] | NEW | External-witness protocol NEW · owner R-3 pending |
| RS-RBM-9 | Either signatory MAY cancel before countdown expires. Cancellation recorded (identity + reason). Cancelled ceremony returns rule to PROPOSED (not deleted). | NEW | Cancellation path NEW |
| RS-RBM-10 | Apply MUST be atomic (status CANON + Registry entry + Ledger record + version stamp) OR none. Partial apply = failure leaving prior state intact. [Doc 15 #27] | NEW | Atomic apply transaction NEW · test A6 in §F |
| RS-RBM-11 | Re-verify MUST run rule's assessment procedure after apply + record result. Failed re-verify raises finding routed to countersigning authority (no silent rollback). | NEW | Re-verify path NEW |

### B.4 · Amend, Retire (RBM-12, RBM-13)

| Row ID | Requirement | Classification | Code / donor / gap |
|---|---|---|---|
| RS-RBM-12 | Amendment = new version through full ceremony. Prior version retained, never overwritten. [ROC-11] | NEW | Version-history storage NEW · missing-reference M-5 (ROC-11) |
| RS-RBM-13 | Retirement through ceremony. Retired rule remains in Registry, status RETIRED, history intact. Where rule's terms require, retirement produces destruction attestation. [Doc 15 #27] | NEW | Retirement + destruction attestation NEW |

### B.5 · Library, profiles, adoption (RBM-14..RBM-17)

| Row ID | Requirement | Classification | Code / donor / gap |
|---|---|---|---|
| RS-RBM-14 | Library holds rule books; each versioned + cites source standard/regulation by clause + holds every rule per RBM-1. Rule book with uncited rule not admissible. | REUSE | Rule Book Library v1 catalog exists (S20); admission gate NEW |
| RS-RBM-15 | Profile = named bundle of rule books recommended for one business type. Profiles versioned + change through system-ordinary ceremony. Business-type taxonomy = ruled versioned list (§7). | NEW | 10 business-type profiles catalog in §E; profile-versioning + adoption NEW |
| RS-RBM-16 | At onboarding, business type selected from taxonomy + MUST present matching profile's rule books as recommendation. Unmatched → base bundle + recorded finding. [Component 14 Connect Wizard] | PARTIAL | Connect Wizard exists (DONE 21 rows); rule-book presentation NEW |
| RS-RBM-17 | Adoption instantiates rule book's rules as customer rules through customer-tier ceremony after RBM-6 conflict check. Recommendation never auto-applied; tenant's accountable person = proposer. | NEW | Adoption endpoint NEW |

### B.6 · Registry, Assessment (RBM-18..RBM-20)

| Row ID | Requirement | Classification | Code / donor / gap |
|---|---|---|---|
| RS-RBM-18 | Registry = authoritative store · every field per ROC-10 · append-only per ROC-11 · Ledger custody | REUSE | Existing System Rules Registry XLSX (286 rules) as donor material; needs ROC-10 field completion (M-4) |
| RS-RBM-19 | Rules Service MUST run any rule's assessment procedure on demand + on stated schedule + record each result. SoA = Registry view, not separate document. | PARTIAL | 3004 invariant tests are runnable-on-demand; 286-rule catalog has no assessment procedure column filled |
| RS-RBM-20 | Every Registry query resolves by rule ID/objective/promise/tier/status/enforcement class/domain/rule book/profile/tenant | NEW | Query API NEW |

### B.7 · Self-Governance and Audit (RBM-21, RBM-22)

| Row ID | Requirement | Classification | Code / donor / gap |
|---|---|---|---|
| RS-RBM-21 | Rules Service's own RBM-* rules are system-TCB tier. No code path alters an RBM-* rule outside RBM-8. [I-5] | NEW | Self-governance invariant NEW |
| RS-RBM-22 | Every Rules Service action writes AU-3 audit record to Ledger (event type + time + component + source + outcome incl. failure + principal identity). [Doc 0 Att 8] | NEW | AU-3 audit-record schema NEW · same as Doc 0 Att 8 requirements · G-8 dependency |

## §C · Rulings Parked R-1..R-4

Owner has 4 open rulings; none block RBM-1..22 authoring/impact/registry/library workflows.

| Row ID | Ruling required | Default (DEFAULT-PENDING-OVERRIDE) | Blocker impact if unresolved |
|---|---|---|---|
| RS-R-1 | Countdown lengths per tier (system-TCB · system-ordinary · customer) | TCB=72h · ordinary=24h · customer=1h | Ceremony can't apply without a value |
| RS-R-2 | Second signatory for system-ordinary rules (role + current holder) | DPO or COO named by owner | RBM-7 gate can't fire |
| RS-R-3 | External witness for system-TCB rules (Watch's witness or separate) | Same as Watch's witness (matches BR-7.3) | RBM-8 gate can't fire |
| RS-R-4 | Ratify v1 business-type taxonomy as standing list | Ratify as v1 | RBM-15/16 static-list gate uses draft only |

## §D · Position vs Architecture

Rules Service adds to Doc 0 Part 2 as **third non-engine subsystem** (alongside Watch + Ledger). Doc 0 language "six engines plus two" becomes "six engines plus three" on ratification. **Effect on Doc 0 §Standing:** Doc 0 amendment triggered — must be banked as a Doc 0 amendment ceremony.

## §E · Business-Type Taxonomy v1 (10 entries)

Not counted as separate rows in the 31 above; treated as a versioned list per RBM-15/16.

10 profiles: Healthcare (hospital/clinic) · Media (broadcaster) · Media (content acq/prod) · Financial (bank) · Financial (insurer) · Agriculture · University · Telecom · Government · Other-not-listed (base bundle + finding).

Each maps to 2-3 rule books; agri/telecom/gov have skeleton-only rule books (RB-FIN partial; RB-HLT/RB-MED/RB-RES per S20).

## §F · Build Acceptance Tests A1-A7 (§8, Table 4)

Not counted as separate rows; each is the test that closes an RBM group:

- **A1** No-force-without-ceremony (RBM-7 + RBM-10 + RBM-21)
- **A2** Conflict-check refuses relaxing customer rule (RBM-6)
- **A3** Append-only Registry (RBM-18)
- **A4** Self-governance (RBM-21)
- **A5** Recommendation per taxonomy (RBM-15/16)
- **A6** Atomic apply (RBM-10)
- **A7** Audit completeness AU-3 (RBM-22)

Each A-test becomes a green invariant proposal in the sprint roadmap pass criteria.

## §G · S19 rollup

| Bucket | Rows | % of 31 |
|---|--:|---:|
| DONE | 0 | 0.0% |
| PARTIAL | 3 | 9.7% |
| REUSE | 6 | 19.4% |
| NEW | 22 | 71.0% |
| Rulings-parked | 4 (already in NEW above) | — |

**Interpretation:** Rules Service is the largest single NEW-scan block (22 of 31 rows NEW = 71%). It is also the primary unlock for W-286-RULE-ENUMERATION-CLASSIFY (E.2), W-CHANGE-CONTROL-CEREMONY (E.4), and every ceremony-dependent rule change. Effort: **XL** (bootstrap) + **L** (ceremony) + **XL** (286-rule enumeration) = ~4 sprints of foundation work per calibration factor 1.60×.

**Missing-reference dependencies:** M-1 (`rule_criteria_spec_v1 §4`), M-2 (§6), M-3 (§8), M-4 (ROC-10), M-5 (ROC-11), M-6 (ROC-6). Six references cited by Rules Service Spec that we don't hold; the spec itself is admissible without them (they're rule ID scheme + storage + enforcement axis specs), but the acceptance tests A1-A7 require these before running.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
