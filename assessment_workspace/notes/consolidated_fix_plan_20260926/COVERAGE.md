# Fix-plan coverage index — 2026-09-26

**Planning allocation only.** All 56 assessment families are listed with their banked row counts; all S-1–S-35 and D01–D12 have routes. A family can touch several packages. W0 is a source/authority dependency for every family; W1's mandatory controls apply wherever relevant. This does not claim row-level semantic closure, executable tests or delivered promises. W0 must finish the exact row/obligation-to-closure joins before implementation claims.

Source: `../full_requirements_gap_20260926/FAMILY_COVERAGE_56.json` and the requirement/promise JSON matrices. Package meanings: W0 trace/authority; W1 identity/custody/effective writes; W2 source/registry; W3 DAP outcome; W4 grounded context/memory; W5a commercial prerequisites; W5b DQ/commercial breadth; W6a required operational gates; W6b Watch/governance/resilience breadth; W7a lineage prerequisite; W7b training/serving/withdrawal; W8 media/skills/rendering; W9a early measurement/journey baseline; W9b surfaces/release proof.

## 1. All 56 requirement families

| Family (literal Doc key) | Rows | Lead / contributing work packages |
|---|---:|---|
| Doc 1 | 14 | W1, W4 |
| Doc 2 | 11 | W1, W4 |
| Doc 15 | 12 | W1, W3, W6a, W6b |
| Doc 3 | 19 | W6a, W6b, W1 |
| Doc 4 | 15 | W4, W6a, W6b |
| Doc 5 | 11 | W4, W7b |
| Doc 6 | 5 | W4 |
| Doc 7 | 6 | W4, W7a |
| Doc 8 | 9 | W2, W3, W4 |
| Doc 9 | 17 | W2, W5b |
| Doc 10 | 5 | W2, W5b, W9b |
| Doc 12 | 10 | W2, W3, W5a, W7b |
| Doc 11 | 16 | W5a, W5b, W7b, W9b |
| Doc 13 | 11 | W7b, W5b |
| Doc 14 | 9 | W7b |
| WPW spec | 18 | W7b, W8, W9b |
| Doc 17 | 23 | W7b, W8 |
| Doc 20 | 14 | W7b, W8 |
| SV extension | 11 | W0 source hold, W8, W7b |
| Doc 19 | 17 | W0, W9a, W9b; EP1–4 adoption held, EP5 nonclaim |
| Deck Engine spec | 14 | W8, W9b; W0 source hold for DR-R10/13 |
| Doc 18 | 8 | W3, W4, W8; A18.6 conditional async disposition |
| ROC spec | 11 | W0 source hold, W1, W6b |
| Rules Service spec | 27 | W1, W6b, W5b |
| DAP Backend spec | 30 | W3, W5a, W5b, W6a, W7b, W8, W9b |
| Amendment T-1/W-1 | 1 | W6a, W4, W8 |
| Amendment W-2 | 1 | W6a, W6b, W4 |
| Amendment W-3 | 1 | W6a, W6b |
| Amendment W-4 | 2 | W1, W6a, W6b |
| Amendment T-1 | 1 | W6a, W7b, W8 |
| Amendment T-2 | 1 | W7b |
| Amendment W-1 | 1 | W6a, W3, W8 |
| Amendment W-7 | 1 | W6a, W7b |
| Amendment W-8 | 1 | W7b, W6a |
| Governance Architecture | 41 | W1, W3, W4, W6a, W6b, W7b, W9b |
| Governance Architecture — gap register | 13 | W0, W1, W6b; historic diagnoses revalidated, not assumed current absence |
| Security Assurance Set | 25 | W1, W6a, W6b; individual S1–25 assignments below |
| Agent Containment spec | 12 | W1, W6a, W6b, W7b |
| security_architecture_v1 | 7 | W1, W6a, W6b, W7b |
| determinism_inventory_v1 | 2 | W0, W2, W5b, W7b |
| failure_posture_v1 | 4 | W1, W6a, W6b |
| trust_domains_v1 | 3 | W1, W2, W6b |
| handoff_registry_v1 | 7 | W1, W2, W3, W4, W7b |
| business_continuity_v1 | 4 | W6b, W0 owner RPO/site-loss decisions |
| Pruning & Unlearning Amendment | 2 | W7a, W7b, W8 |
| serving_integrity_v1 | 4 | W7b, W9b |
| watch_learning_v1 | 10 | W6a, W6b, W7b |
| Security Assurance Promise Set | 4 | W7a, W7b, W6b; S26–29 below |
| entitlement_service_v1 | 49 | W5a, W5b, W3, W4, W9b |
| memory_compaction_v1 | 11 | W4, W7a, W7b |
| principal_model_v1 | 13 | W1, W5a, W6b |
| content_registry_v1 | 31 | W9a, W9b, W3, W4, W8 |
| security_function_policies_v1 | 7 | W0 atomization, W1, W4, W6a, W6b, W7b |
| execution_standard_v1 | 15 | W0 and each execution package; W9a, W9b independent evidence |
| data_cleanliness_v1 | 15 | W5b, W2, W4, W7b, W8 |
| context_and_capability_v1 | 16 | W1, W4, W5a, W6b, W9a, W9b |

Declared total: **56 families / 648 rows**. These counts describe coverage of the planning inventory only.

## 2. All 35 assurance promises (not product-promise #N)

The literal promise text, bound and falsification scenario remain in `PROMISE_GAPS_35.json` / `PROMISES_LINE_BY_LINE.md`; the descriptions below are routing labels, not rewritten promises.

| Promise | Planning label | Lead / contributing gates |
|---|---|---|
| S-1 | Every actor/input/action observed | W1, W6a, W6b |
| S-2 | Three attack-shape detection mechanisms | W6b |
| S-3 | Suspicion versus evidence-authorized response | W6a, W6b |
| S-4 | Ladder and cumulative blast/friction ceilings | W6a, W6b |
| S-5 | Reversible TTL action, atomic attestation, peer counter-sign | W1, W6b |
| S-6 | Authoritative record before next gate | W1, W6a |
| S-7 | Watch Learning amendment, no self-ratification | W6b, W7b |
| S-8 | Demonstrated standing response rails | W6a, W6b |
| S-9 | Mirage replay or explicit non-landed work | W6b, W3 |
| S-10 | 3,600-second independent Ledger continuity | W6b |
| S-11 | 72-hour qualifying breach notification | W6b |
| S-12 | Independent custody fail-close | W1, W6a, W6b |
| S-13 | Macho judgement/Mkono action separation | W1, W6a, W6b |
| S-14 | Closed authentic sever signals | W6a, W6b |
| S-15 | Conformance loss cannot convict | W6a, W6b |
| S-16 | Deterministic floors, delayed two-signature ceremony | W1, W6b |
| S-17 | Watch cannot delete; separate erasure authority | W6b, W7a, W7b |
| S-18 | Tenant-keyed nonexportable profiles | W1, W6b, W9b |
| S-19 | Independent liveness and tamper witness | W6b |
| S-20 | Exactly one immutable task authority | W1 |
| S-21 | Isolated mirage with truthful internal records | W6b |
| S-22 | All component-output inspection and ADVISORY tags | W6a, W4, W8 |
| S-23 | Party/mandate/coordination cumulative conduct | W1, W6a, W6b |
| S-24 | Finding-raiser budget/drift, no volume-to-sever | W6a, W6b |
| S-25 | Lifetime estate release ceiling | W6a, W7a, W7b |
| S-26 | Descendant recall/re-derivation, no privacy refund | W7a, W7b, W4, W8 |
| S-27 | Actual registered model/engine serving integrity | W7b, W9b |
| S-28 | Evidence certificates and ratified vocabulary | W6a, W6b |
| S-29 | Admitted capability class, no learner ratification | W1, W6a, W7b |
| S-30 | Receipted anchored compaction and disclosed loss | W4, W7a |
| S-31 | Admitted licence/routes, one Ledger, truthful usage | W5a, W5b, W3, W4 |
| S-32 | Every producer authenticated and admitted | W1 |
| S-33 | Registered content, measured fields, ruled salience | W9a, W9b, W3, W4, W8 |
| S-34 | Check-bound per-record cleanliness and eligibility | W5b, W2, W4, W7b, W8 |
| S-35 | Context/custody loss and actual governance cost | W4, W6b, W9a, W9b |

S30–35 have their own assurance rows even though the master registry's assurance-named families list only S1–29; their component-family coverage must not be confused with absence of promises.

## 3. Original DAP acceptance: retain progress, finish residuals

| ID | Banked status | Residual work routed to |
|---|---|---|
| D01 | Verified scoped slice | W1 all-producer admission/scope; regression at W3 |
| D02 | Verified | Preserve immutable submission/replay; W3 regression |
| D03 | Partial | W1 effective commits; W3 approval/terminal command concurrency |
| D04 | Open | W5a actual authority/terms; W3 independent recorded approval, party privacy |
| D05 | Partial | W3 executor-backed stop, same-scope valid-approval retry bounded at three |
| D06 | Partial | W2 admitted real source/executor; W3 real operation dispatch |
| D07 | Partial | W3 artifact/rights/hash retrieval; W4/W8 grounded skill/transformed outputs |
| D08 | Partial | W3 actual success/action history parity; W9b remaining journeys |
| D09 | Partial | W5a real membership/licence/catalog/ceremony producers; W5b breadth |
| D10 | Partial | W5a/W3 actual metering; W5b pricing/period/rollover/concurrency |
| D11 | Verified changed views | Preserve prototype hashes/test IDs; W9b entire applicable surface coverage |
| D12 | Verified scoped slice | Repeat appropriate tests/receipts per new package; real positive work distinct from mocks |

T14 remains the separate **real Census source-success gate**, not an extra DAP test or a platform percentage. No status above has been advanced by planning.

## 4. Owner-facing report areas A–L

| Gap-report area | Routed work |
|---|---|
| A Custody, confidentiality, identity | W1, W6a |
| B Northena request/work/result | W3, W5a, W2 |
| C Ledger and effective governance | W1, W6b |
| D Estate, Census, Mtafiti | W2, W5b |
| E Solva and truthful grounding | W4, W5b, W6a |
| F Context/warm/memory | W4, W7a, W9a/W9b |
| G Targeta/CIF/training/serving | W7b, W5b, W6b |
| H Audio/voice/multimodal | W8, W7b, W5b |
| I Watch/containment/resilience | W6a, W6b, W1 |
| J Entitlement/commercial truth | W5a, W5b, W3 |
| K Content/prototypes/reports/decks/skills | W9a/W9b, W8, W3, W4 |
| L EX/DQ/CC | W0/all execution contracts; W5b; W1/W4/W6b/W9a/W9b |

The full report's separately named Rules/Trust Domain and Learning Withdrawal boundaries are covered by W1/W6b and W7a/W7b/W4/W8 respectively. Supplemental Canon and inherited limitations stay in W0; no family or promise is declared complete merely by having an assigned package.