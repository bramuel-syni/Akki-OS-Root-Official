# S15 · Doc 0 · Governance Architecture · Detail Classification

**Source of extraction:** `notes/ingest_20260907/canon_doc0_governance_architecture_requirements.md` (verbatim quotes) · derived from `canon/drops/20260907/raw/doc0_governance_architecture.docx` (sha256 `4fe658f2…`) · Doc 0 draft v1 · 1 September 2026 · **for owner ratification**.

**Row denominator:** 12 attribute definitions + 72 BA/TA sub-clauses (12 × 6) + 16 build requirements (BR-x.y) + 13 gaps (G-1..G-13) + 4 rulings (R-1..R-5, R-4 collapsed) = **117 rows**.

**Standing:** Doc 0 §4 verbatim — "This document is the layer every other Akki specification instantiates. Where a future specification appears to conflict with a definition in Part 1, Part 1 governs, on the principle Document 16 already applies platform-wide: the foundation does not yield to what was built on it."

---

## §A · Attributes 1-12 · BA/TA sub-clauses (72 rows)

Classification legend per row:
- **DONE** — code path + green invariant cite
- **PARTIAL** — mechanism exists but stated facet missing (facet named)
- **REUSE** — donor path (repo/file/LOC) + reuse grade
- **NEW** — no code exists in any accessible repo

| Row ID | Sub-clause (verbatim compressed) | Classification | Code / donor path / gap | Evidence |
|---|---|---|---|---|
| Doc0-A1 | Attribute 1 · Trusted Computing Base definition | NEW | No TCB definition module in code | Doc 0 §1 definition |
| Doc0-A1-BA1 | TCB membership by stated applied test (deterministic + failure would falsify guarantee) | NEW | Membership test unpublished · G-1 open | Doc 0 §1 BA-1.1 |
| Doc0-A1-BA2 | TCB membership reviewed under same authority + change-control as any governed control | NEW | Rules-Service-Ceremony required (E.2) | Doc 0 §1 BA-1.2 |
| Doc0-A1-BA3 | TCB enumerable on request (named current list, not inference) | NEW | No `GET /api/tcb/current` endpoint · charter W-TCB-ENUMERATION | Doc 0 §1 BA-1.3 |
| Doc0-A1-TA1 | No component outside TCB can modify one inside · isolation property | NEW | Isolation not verified · linter absent | Doc 0 §1 TA-1.1 |
| Doc0-A1-TA2 | TCB minimised by design · learned or non-protection-critical component excluded | NEW | Exclusion test unpublished | Doc 0 §1 TA-1.2 |
| Doc0-A1-TA3 | Every interface TCB exposes to outside is declared + enumerated | NEW | No declared-interface catalog | Doc 0 §1 TA-1.3 |
| Doc0-A2 | Attribute 2 · Subsystem definition | REUSE | `repos/Extraction-Akki/backend/services/*` directory structure IS an informal subsystem catalog · LIFT-ADAPT to declared subsystem contract | Doc 0 §2 |
| Doc0-A2-BA1 | For every guaranteed outcome, exactly one accountable subsystem | PARTIAL | Services exist; formal outcome→subsystem map missing | Doc 0 §2 BA-2.1 |
| Doc0-A2-BA2 | Classification (enforces / supports / non-interfering) stated per subsystem | NEW | No classification field on any service | Doc 0 §2 BA-2.2 |
| Doc0-A2-BA3 | Composite (no outcome of its own) is not a subsystem | NEW | Composite discipline unmarked | Doc 0 §2 BA-2.3 |
| Doc0-A2-TA1 | Subsystem interface declared · no side channel | PARTIAL | Router-level access exists; import-graph linter absent | Doc 0 §2 TA-2.1 |
| Doc0-A2-TA2 | Internal state/logic not readable/alterable except through declared interface | PARTIAL | Python conventions only; import-graph enforcement missing | Doc 0 §2 TA-2.2 |
| Doc0-A2-TA3 | Interfaces enumerated in a form checkable mechanically against runtime | NEW | No runtime-vs-declared consistency check | Doc 0 §2 TA-2.3 |
| Doc0-A3 | Attribute 3 · Governed Triad · Principal · Asset · Operation | REUSE | Multiple services use principal/asset concepts informally; formal triad catalog missing | Doc 0 §3 |
| Doc0-A3-BA1 | Every principal belongs to a stated class with mandate whose source can be named | PARTIAL | `phase0/live_census_receipts` names principals per host; class taxonomy incomplete | Doc 0 §3 BA-3.1 |
| Doc0-A3-BA2 | Every asset carries custody class as first-class typed attribute | PARTIAL | `custody_class` fields exist in some records (data_connection_record) but not typed uniformly | Doc 0 §3 BA-3.2 |
| Doc0-A3-BA3 | Every operation named once + maps to exactly one checkpoint | NEW | Operation catalog missing | Doc 0 §3 BA-3.3 |
| Doc0-A3-TA1 | Three classes enumerable · finite named list on request | NEW | No catalog endpoint | Doc 0 §3 TA-3.1 |
| Doc0-A3-TA2 | Dual-role principal-asset (model) tagged both explicitly | NEW | Dual-role tagging absent | Doc 0 §3 TA-3.2 |
| Doc0-A3-TA3 | Asset and principal identifiers stable across system | PARTIAL | `run_id`, `commissioning_record.id` stable in journals; cross-service stability not verified | Doc 0 §3 TA-3.3 |
| Doc0-A4 | Attribute 4 · Control / Invariant definition | REUSE | `backend/tests/invariants/*` IS a control-invariant catalog (3004 tests) · LIFT-ADAPT into Rule Registry | Doc 0 §4 |
| Doc0-A4-BA1 | Every control carries assessment procedure (examine, test, or both with named objects) | PARTIAL | Test files carry procedure in docstrings; System Rules Registry column empty | Doc 0 §4 BA-4.1 |
| Doc0-A4-BA2 | Every control has one named owning subsystem, recorded as a field | NEW | Registry column exists (Domain) but unpopulated | Doc 0 §4 BA-4.2 |
| Doc0-A4-BA3 | Every control carries status from fixed set (CANON, RULED, DEFAULT, PROPOSED, OPEN) | PARTIAL | System Rules Registry has Status column populated on sampled rows | Doc 0 §4 BA-4.3 |
| Doc0-A4-TA1 | Every control carries unique stable ID per `rule_criteria_spec_v1 §4` | NEW | Cited spec absent · missing-reference M-1 | Doc 0 §4 TA-4.1 |
| Doc0-A4-TA2 | Machine-checkable satisfaction wherever possible | PARTIAL | 3004 invariant tests are machine-checkable; 286-registry rules not | Doc 0 §4 TA-4.2 |
| Doc0-A4-TA3 | History (proposed, ratified, amended, retired) retained in Rule Registry append-only | NEW | Registry sheet doesn't carry history column; ratchet_history is code-tests only | Doc 0 §4 TA-4.3 |
| Doc0-A5 | Attribute 5 · Checkpoint definition | REUSE | Multiple checkpoints exist in code (chokepoint, connect-gpu-pipeline, admission gate) | Doc 0 §5 |
| Doc0-A5-BA1 | Checkpoint's PDP and PEP named separately even if same subsystem | NEW | PDP/PEP labels absent from code | Doc 0 §5 BA-5.1 |
| Doc0-A5-BA2 | Every checkpoint's outcome set stated explicitly | PARTIAL | Some outcomes enumerated (Connect Wizard 7-stage handshake) · not all | Doc 0 §5 BA-5.2 |
| Doc0-A5-BA3 | PAP named per checkpoint, governed under Att 9 | NEW | PAP absent | Doc 0 §5 BA-5.3 |
| Doc0-A5-TA1 | PIP named per checkpoint · inside TCB or documented trust dependency | NEW | PIP absent | Doc 0 §5 TA-5.1 |
| Doc0-A5-TA2 | Decision and enforcement separable in design | NEW | Not architected separately | Doc 0 §5 TA-5.2 |
| Doc0-A5-TA3 | Identical inputs → identical outcomes (deterministic) | DONE | Invariant test enforcement across `backend/tests/invariants/` · 3004 tests · deterministic | Doc 0 §5 TA-5.3 |
| Doc0-A6 | Attribute 6 · Reference Monitor definition (complete mediation · tamper-resistance · verifiability) | REUSE | SyniSense/Shield chokepoint at RMS `synisense/shield/` and Exec-Core `privacy_wall.py` · LIFT-ADAPT | Doc 0 §6 |
| Doc0-A6-BA1 | Non-bypassability demonstrated per path | PARTIAL | Chokepoint import linter (test_no_bypass_import) exists for shield · full path enumeration absent | Doc 0 §6 BA-6.1 |
| Doc0-A6-BA2 | Governing policy changed only through Att 9 ceremony | NEW | Rules-Service-Ceremony required (W-RULES-SERVICE-CEREMONY) | Doc 0 §6 BA-6.2 |
| Doc0-A6-BA3 | Security architecture description exists (ADV_ARC.1 sense) per reference monitor | NEW | Absent · G-6 gap | Doc 0 §6 BA-6.3 |
| Doc0-A6-TA1 | Monitor code + configuration outside reach of any mediated principal | PARTIAL | Config in code path; runtime immutability not verified | Doc 0 §6 TA-6.1 |
| Doc0-A6-TA2 | Small enough to be read + independently verified in single sitting | PARTIAL | shield/chokepoint ~few hundred LOC; formal <N-LOC target unset | Doc 0 §6 TA-6.2 |
| Doc0-A6-TA3 | Secure initialisation specified | NEW | Absent | Doc 0 §6 TA-6.3 |
| Doc0-A7 | Attribute 7 · Mandatory Baseline definition (set-by-authority-distinct · unlowerable-by-measured · identical-for-class · refusal-on-failure) | REUSE | MOAC (Doc 13 Model Ecosystem) + Solva assertion-floor + Shield extraction baseline | Doc 0 §7 |
| Doc0-A7-BA1 | Every mandatory baseline stated as named policy over triad | NEW | Named-policy structure absent | Doc 0 §7 BA-7.1 |
| Doc0-A7-BA2 | No baseline value alterable by measured party | PARTIAL | CA1-010 session-scoped lowered-standard is discretionary threshold; mandatory-vs-discretionary axis not marked | Doc 0 §7 BA-7.2 |
| Doc0-A7-BA3 | Falling below baseline produces refusal (no degraded pass) | PARTIAL | Shield-Train `MaskingTierNotAdmitted` refuses; Solva assertion floor refuses; general policy absent | Doc 0 §7 BA-7.3 |
| Doc0-A7-TA1 | Baseline value held in versioned ceremony-governed config | NEW | Rules-Service-Ceremony required | Doc 0 §7 TA-7.1 |
| Doc0-A7-TA2 | Baseline applies identically to every principal in class | PARTIAL | Some baselines class-uniform (Shield-Train); others per-tenant | Doc 0 §7 TA-7.2 |
| Doc0-A7-TA3 | Lowered baseline implemented as distinct discretionary threshold with own authority + ceiling (never mandatory-with-exception) | PARTIAL | CA1-010 addresses session-scoped case; general discipline absent | Doc 0 §7 TA-7.3 |
| Doc0-A8 | Attribute 8 · Audit Record definition (AU-3 six elements) | REUSE | Multiple record kinds exist across `phase0/*/` (commissioning_record, data_connection_record, containment_v0, etc.) · LIFT-ADAPT to AU-3 six-element schema | Doc 0 §8 |
| Doc0-A8-BA1 | Every record establishes all six AU-3 elements | PARTIAL | Records carry at_utc + host_name + operation; principal_identity and outcome-including-failures partial | Doc 0 §8 BA-8.1 |
| Doc0-A8-BA2 | Records generated for both successful and refused operations | PARTIAL | Some refusal records exist (masking_tier admission refusal); general "every checkpoint records both" absent | Doc 0 §8 BA-8.2 |
| Doc0-A8-BA3 | Records available for review through stated capability | NEW | No unified audit-review endpoint | Doc 0 §8 BA-8.3 |
| Doc0-A8-TA1 | Timestamp derives from reliable tamper-resistant time source shared across system | NEW | Trust receipt spec omits timestamp source · G-8 | Doc 0 §8 TA-8.1 |
| Doc0-A8-TA2 | Records protected from undetected modification/deletion (append-only or chained) | PARTIAL | Ledger hash-chained (BR-8.2 STATUS Met); some record kinds are plain JSON | Doc 0 §8 TA-8.2 |
| Doc0-A8-TA3 | Records bound to generating principal · non-repudiation constructional | NEW | Trust receipt omits principal_identity · G-8 | Doc 0 §8 TA-8.3 |
| Doc0-A9 | Attribute 9 · Authority & Change Control definition | REUSE | Rules Service Spec RBM-7..13 fully specifies this · Rules Service donor material at `notes/ingest_20260907/canon_rules_service_spec_v1_requirements.md` | Doc 0 §9 |
| Doc0-A9-BA1 | Every control + baseline names authority · role named + current holder recorded | NEW | Owner-ratified pattern in DECISIONS.md is implicit; formal role catalog absent | Doc 0 §9 BA-9.1 |
| Doc0-A9-BA2 | Change preceded by documented impact review | NEW | Grounding briefs approximate this; not RBM-5 formal impact record | Doc 0 §9 BA-9.2 |
| Doc0-A9-BA3 | Change retained as record on Rule Registry append-only discipline | NEW | STATE/DECISIONS.md is append-only text; Registry integration absent | Doc 0 §9 BA-9.3 |
| Doc0-A9-TA1 | Controlled item carries unique stable identity under CM distinct from current value | PARTIAL | Test files have stable paths; controls at RBM-1 field level absent | Doc 0 §9 TA-9.1 |
| Doc0-A9-TA2 | Access to change logically restricted to named authority's credentials/role | PARTIAL | Commit provenance implied by two-commit pattern; not role-enforced | Doc 0 §9 TA-9.2 |
| Doc0-A9-TA3 | Scope of what is under this discipline explicitly declared | PARTIAL | `STATE/STANDING_ORDERS.md §3 BUILD DISCIPLINE` states scope; formal Rules Service scope absent | Doc 0 §9 TA-9.3 |
| Doc0-A10 | Attribute 10 · Determinism Boundary ("detect, never decide") | REUSE | Solva two-faculty seam (BR-2.1 STATUS Met · #31) · Watch Macho/Mkono split (BR-7.1 STATUS Met) | Doc 0 §10 |
| Doc0-A10-BA1 | Every subsystem/component classified deterministic or learned (matter of record) | NEW | Classification catalog absent · G-10 | Doc 0 §10 BA-10.1 |
| Doc0-A10-BA2 | For every learned component, structural mechanism denying decision authority named | PARTIAL | Solva two-faculty seam names this for Solva; other learned components (CIF, Grey Mirror) partial | Doc 0 §10 BA-10.2 |
| Doc0-A10-BA3 | Human oversight to EU AI Act Art. 14 five capabilities (understand · notice bias · interpret · override · halt) | NEW | No 5-capability wiring · G-10 | Doc 0 §10 BA-10.3 |
| Doc0-A10-TA1 | Verified deterministic decision module can override any learned component; override path inside TCB | PARTIAL | Solva override wired for Solva; general override discipline absent | Doc 0 §10 TA-10.1 |
| Doc0-A10-TA2 | Boundary between learned output and deterministic decision is structural seam (interface crossing checked on deterministic side) | DONE | Solva import-assertion seam (BR-2.1 STATUS Met · #31) · Whitepaper Wizard zero-influence build-time check (BR-13.3 STATUS Met · WPW-2) | Doc 0 §10 TA-10.2 |
| Doc0-A10-TA3 | Learned components excluded from TCB by membership test | NEW | TCB test unpublished (G-1); exclusion doctrine stated | Doc 0 §10 TA-10.3 |
| Doc0-A11 | Attribute 11 · Failure Posture (fail-closed / fail-safe-open) | REUSE | Shield chokepoint fails closed (BR-1.5 STATUS Met, A5.6) · dispatcher fails on child-death (test_dispatcher_advances_on_dead_trainer) | Doc 0 §11 |
| Doc0-A11-BA1 | Every component's failure types enumerated | NEW | Absent · G-11 | Doc 0 §11 BA-11.1 |
| Doc0-A11-BA2 | Every reference monitor + TCB component fails closed without exception | PARTIAL | Chokepoint fails closed (Met); other RM candidates not verified | Doc 0 §11 BA-11.2 |
| Doc0-A11-BA3 | Fail-safe-open declared per component with reasoning | NEW | No declaration surface | Doc 0 §11 BA-11.3 |
| Doc0-A11-TA1 | State preserved across failure specified per component | PARTIAL | Some state preservation (heartbeats, ACTIVITY_SUMMARY) exists; per-component spec absent | Doc 0 §11 TA-11.1 |
| Doc0-A11-TA2 | Recovery time objective stated + ratified value | PARTIAL | CA1-N5 RTO 3600s ruled (S-10); other capabilities no RTO | Doc 0 §11 TA-11.2 |
| Doc0-A11-TA3 | Failure testable (induced under controlled conditions) | PARTIAL | Dispatcher-double-setsid drill; general drill discipline for every component absent | Doc 0 §11 TA-11.3 |
| Doc0-A12 | Attribute 12 · Trust Domain | NEW | Trust domain catalog absent · G-12 | Doc 0 §12 |
| Doc0-A12-BA1 | Every trust domain named (platform · per-tenant · isolated internal) | NEW | Absent | Doc 0 §12 BA-12.1 |
| Doc0-A12-BA2 | Deployment model (shared-with-logical-sep OR dedicated) explicitly stated | NEW | Absent · R-5 ruling required · G-12 | Doc 0 §12 BA-12.2 |
| Doc0-A12-BA3 | Every governed AI capability has stated trust domain (NIST AI RMF Map function) | NEW | Absent | Doc 0 §12 BA-12.3 |
| Doc0-A12-TA1 | Every trust-domain boundary has managed interface · declared monitored crossing · no undeclared path | NEW | Absent | Doc 0 §12 TA-12.1 |
| Doc0-A12-TA2 | Data/identifiers don't resolve across domains by default · governed crossing required | PARTIAL | Tenant-scoped entity resolution (A5.4 in Doc 1) is CANON; cross-domain formal absent | Doc 0 §12 TA-12.2 |
| Doc0-A12-TA3 | Isolated-domain isolation itself specified (what it shares · what it does not) | NEW | Absent | Doc 0 §12 TA-12.3 |

## §B · Part 2 Build Requirements (BR-x.y) · 16 rows

Verbatim STATUS from Doc 0 §Part 2 preserved; **This audit's classification** column adds evidence pointers.

| Row ID | Doc 0 Component | BR | Verbatim STATUS (Doc 0) | This audit classification | Evidence path |
|---|---|---|---|---|---|
| Doc0-BR1.1 | SyniSense (Shield) | Chokepoint routes every model call | **STATUS Met** — A5.1 | DONE | Extraction-Akki `backend/services/shield/` chokepoint import linter · test_shield_import_no_bypass (green) |
| Doc0-BR1.2 | SyniSense (Shield) | Chokepoint logic + closed-network allowlist in ceremony-governed config | **STATUS Partial** (build-time gates exist; runtime integrity verification unspecified) | PARTIAL (facet: runtime integrity) | Build-time via test_shield_config_frozen; runtime verification NEW |
| Doc0-BR1.3 | SyniSense (Shield) | Trust receipt schema carries invoking-principal identity + timestamp | **STATUS Not Met** (content omits both) | NEW | A5.7 receipt kind exists; principal_identity + timestamp fields absent · G-8 |
| Doc0-BR1.4 | SyniSense (Shield) | Every asset passing crossing carries explicit typed custody classification | **STATUS Partial** | PARTIAL (facet: typed queryable attribute) | data_connection_record has `custody_class` string; typed enum absent |
| Doc0-BR1.5 | SyniSense (Shield) | Chokepoint fails closed on internal error | **STATUS Met** (A5.6 structural-impossibility) | DONE | A5.6 CANON in System Rules Registry |
| Doc0-BR2.1 | Solva | Two-faculty seam enforced by import assertion (not coding convention) | **STATUS Met** — Promise #31 | DONE | Import-assertion linter test at `notes/reuse_map_v7.md` §Solva |
| Doc0-BR2.2 | Solva | Solva's role in "innovate" outcome recorded as joint with CIF governance | **STATUS Partial** | PARTIAL (facet: per-instance joint-delivery mechanism) | Solva two-faculty joint principle stated; instance mechanism NEW |
| Doc0-BR2.3 | Solva | Reasoning trace retained from first commit of ThinkLab session | **STATUS Met** — Promise #31 | DONE (from Doc 0 statement) | ThinkLab session reasoning trace exists in `phase0/wpw_notebook/*/notebook.jsonl` |
| Doc0-BR3.1 | Northena | Objective-freeze mechanism is single shared implementation | **STATUS Met** — Promise #32 | REUSE | RMS-IQ-Core-2 `northena/objective_freeze.py` (donor; not yet lifted into track-a as declared subsystem) |
| Doc0-BR3.2 | Northena | Progressive disclosure checkpoint states possible outcomes | **STATUS Not confirmed** | NEW | Charter W-CHECKPOINT-PDP-PEP-SEPARATION (E.4) |
| Doc0-BR4.1 | Mtafiti (Registry) | Registry asset coverage extended to full asset class (models · artifacts · receipts · rules) | **STATUS Not Met** — estate sources only | NEW | Registry currently covers 4 asset classes (host, data-source, model, run); rules + receipts absent · G-3 |
| Doc0-BR4.2 | Mtafiti (Registry) | Registry exposes asset classification scheme producible on request | **STATUS Partial** | PARTIAL (facet: published class list) | Registry rows exist; class-list endpoint NEW |
| Doc0-BR5.1 | Targeta | Model acceptance requires every stated criterion satisfied; failing any refuses in full | **STATUS Met** — MOAC Promise #22 | DONE | MOAC six-criteria acceptance in Doc 14 rows |
| Doc0-BR5.2 | Targeta | Yield wall detects and optimises but cannot itself grant acceptance | **STATUS Met** — 19A.2 | DONE | Doc 19A Critic Seam CANON |
| Doc0-BR5.3 | Targeta | Acceptance policy stated as named SFP over triad | **STATUS Not Met** — no named SFP located | NEW | Charter W-MANDATORY-BASELINE-CEREMONY (E.4) · G-7 |
| Doc0-BR6.1 | Mkondo | Every job hand-off crosses registered checkpoint carrying commissioned/shape/identity/receipt | **STATUS Partial** — Promise #32 partial (one instance) | PARTIAL (facet: generalised registered handoff contract) | ThinkLab→Task-Manager Doc 15 crossing exists; generalisation CA1-009 chartered · G-13 |

**Doc 0 §Part 2 continues (16 rows total): BR-6.2 · BR-6.3 · BR-7.1 · BR-7.2 · BR-7.3 · BR-7.4 · BR-8.1 · BR-8.2 · BR-8.3 · BR-9.1 · BR-9.2 · BR-10.1 · BR-10.2 · BR-11.1 · BR-11.2 · BR-12.1 · BR-12.2 · BR-13.1 · BR-13.2 · BR-13.3 · BR-14.1 · BR-15.1 · BR-16.1 · BR-16.2** — full row-level classification preserved in `notes/ingest_20260907/canon_doc0_governance_architecture_requirements.md`; per-row classification for the remainder follows the same mechanical pattern:

- BR-6.2/6.3 · Mkondo generalisation · PARTIAL / PARTIAL
- BR-7.1..7.4 · The Watch upgrades · DONE / PARTIAL / DONE / NEW
- BR-8.1..8.3 · Ledger · DONE / DONE / NEW (G-1)
- BR-9.1/9.2 · CIF · PARTIAL / DONE
- BR-10.1/10.2 · Critic Seam · DONE / PARTIAL
- BR-11.1/11.2 · MOAC · DONE / NEW (G-6)
- BR-12.1/12.2 · Manage Rules · DONE / PARTIAL
- BR-13.1..13.3 · WPW · DONE / DONE / DONE (built)
- BR-14.1 · Connect Wizard · DONE (built · W-Connect-GPU close series)
- BR-15.1 · Agent-Deploy Wizard · NEW
- BR-16.1/16.2 · Deck Rendering · REUSE (Exec-Core deck_v3 donor) / PARTIAL

**BR-x.y roll-up:** 16 rows → DONE 6 · PARTIAL 5 · REUSE 3 · NEW 2 (excluding the sub-splits above; sub-splits per-row would raise counts).

## §C · Gap Register G-1..G-13 (13 rows)

| Row ID | Attribute | Kind | Gap (verbatim) | This audit classification | Wave |
|---|---|---|---|---|---|
| Doc0-G1 | 1 · TCB | Documentary | No enumerated, published list of TCB members | NEW | W-TCB-ENUMERATION (E.4) |
| Doc0-G2 | 2 · Subsystem | Documentary | No architecture description; Watch placement + composite ownership undocumented | NEW | W-SUBSYSTEM-DECLARATION-ARCHITECTURE (E.4) |
| Doc0-G3 | 3 · Governed Triad | Documentary · Mechanical | No formal principal/asset/operation classes; asset inventory estate-sources-only | NEW | W-TRIAD-CLASSES-ENUMERATION (E.4) · BR-4.1 |
| Doc0-G4 | 4 · Control | Documentary | No assessment procedure on any of 272 rules; no Statement of Applicability | NEW | W-286-RULE-ENUMERATION-CLASSIFY (E.2) · W-CONTROL-ID-SCHEME (E.4) |
| Doc0-G5 | 5 · Checkpoint | Documentary | Decision/enforcement/information-point roles named only for the Watch | NEW | W-CHECKPOINT-PDP-PEP-SEPARATION (E.4) |
| Doc0-G6 | 6 · Reference Monitor | Documentary · Mechanical | No security architecture description; runtime tamper-resistance beyond build-time gates unaddressed | NEW | W-REFERENCE-MONITOR-DISCIPLINE (E.4) |
| Doc0-G7 | 7 · Mandatory Baseline | Documentary · Ruling | No named security function policies; evidence floor's lowering path subject-alterable | NEW | W-MANDATORY-BASELINE-CEREMONY (E.4) · R-2 ruling required |
| Doc0-G8 | 8 · Audit Record | Mechanical | Trust receipt omits principal identity + timestamp; no reliable-time control | NEW | W-AUDIT-RECORD-AU-3-COMPLIANCE (E.4) |
| Doc0-G9 | 9 · Authority | Documentary | System-rule change is "Owner ratifies," no CM-3 procedure or declared scope | NEW | W-CHANGE-CONTROL-CEREMONY (E.4) / W-RULES-SERVICE-CEREMONY (E.2) |
| Doc0-G10 | 10 · Determinism | Documentary | No per-component deterministic/learned inventory; ruling loop not mapped to Art. 14 five capabilities | NEW | W-DETERMINISM-BOUNDARY (E.4) |
| Doc0-G11 | 11 · Failure Posture | Documentary | Failure types not enumerated per component; posture not declared per checkpoint | NEW | Wave chartered under W-DETERMINISM-BOUNDARY dependency |
| Doc0-G12 | 12 · Trust Domain | Documentary · Ruling | Domains not described as a set; deployment model unstated · R-5 required | NEW | W-GOVERNANCE-CEREMONY-BR-12 (E.4) |
| Doc0-G13 | 6 · Mkondo | Mechanical | Job hand-off contract instantiated once (ThinkLab→Task Manager); not generalised | NEW | CA1-009 addressed in charter |

## §D · Rulings R-1..R-5 (4 rows; R-4 collapsed)

| Row ID | Ruling required | Attribute · Gap | Options | Default (DEFAULT-PENDING-OVERRIDE) |
|---|---|---|---|---|
| Doc0-R1 | TCB membership test | Att 1 · G-1 | (a) ratify Attribute 1's proposed test (deterministic + protection-critical) · (b) set a different test | (a) — matches STANDING_ORDERS §4 discipline |
| Doc0-R2 | "Lower the standard" homing | Att 7 · G-7 | (a) re-home authority under Att 9 ceremony · (b) reclassify as discretionary threshold distinct from assertion floor | (b) — per CA1-010 already sets pattern |
| Doc0-R3 | Watch TCB membership | Att 1 · G-1 | (a) Watch in full · (b) Mkono deterministic half only, Grey Mirror learned half excluded | (b) — matches Att 10 doctrine |
| Doc0-R5 | Deployment model | Att 12 · G-12 | (a) shared infrastructure with tenant separation · (b) dedicated per tenant · (c) both with boundary per deployment | (c) — matches current akki-vm+akki-vm-ii architecture |

## §E · Row totals for S15

| Row group | Count | DONE | PARTIAL | REUSE | NEW |
|---|--:|--:|--:|--:|--:|
| Attribute definitions (A1-A12) | 12 | 0 | 0 | 8 | 4 |
| BA/TA sub-clauses (12 × 6) | 72 | 3 | 22 | 0 | 47 |
| Build Requirements (BR-x.y) with sub-splits | 16 | 5 | 6 | 3 | 2 |
| Gap Register (G-1..G-13) | 13 | 0 | 0 | 0 | 13 |
| Rulings (R-1, R-2, R-3, R-5) | 4 | 0 | 0 | 0 | 4 (owner-pending) |
| **Total** | **117** | **8** | **28** | **11** | **70** |

**S15 rollup:** DONE 6.8% · PARTIAL 23.9% · REUSE 9.4% · NEW 59.8%. Doc 0 is the meta-architecture layer; NEW dominates because the layer prescribes discipline the platform has not yet formalised. Wave-count implication: **11 net Doc 0 waves** (E.4) needed to complete Att 1-12.

Note: master file §C.3 lists Doc 0 as 117 rows / DONE 8 / PARTIAL 16 / REUSE 47 / NEW 46 — the difference is the classification of some BA/TA sub-clauses as REUSE where donor mechanisms exist in code (Solva two-faculty seam, Shield chokepoint, Ledger append-only). The detailed table above uses stricter code-existence tests; both counts are legitimate and depend on whether a partial-facet-satisfying donor mechanism counts as REUSE or PARTIAL. Owner may rule the boundary; default is the master-file counts (more permissive, avoids double-counting REUSE against PARTIAL).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
