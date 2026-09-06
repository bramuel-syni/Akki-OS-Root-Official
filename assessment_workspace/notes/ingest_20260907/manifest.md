# Ingest Manifest · 2026-09-07 Canon Drop

**Authored:** 2026-09-06T~17:35Z during operator interrupt (read-only ingest wave). No production code written. Live campaign v2 dispatchers on akki-vm and akki-vm-ii undisturbed (heartbeats freshness verified before and after ingest — see §Live Campaign Health).

## §A · Raw artefact bank

All raw bytes banked verbatim at `canon/drops/20260907/raw/`. Extracted text/JSON at `canon/drops/20260907/extracted/text/`. Extracted text is DERIVED — raw file is authoritative.

| # | File | sha256 | size | banked path | origin URL |
|---|---|---|---|---|---|
| 1 | `doc0_governance_architecture.docx` | `4fe658f20c8d422e7f9cd7a762963e05c12bb46e09e8361e6d5abb80b2a7da2d` | 49,884 | `canon/drops/20260907/raw/doc0_governance_architecture.docx` | https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/p7opwxpy_Akki_Governance_Architecture_v1%20%281%29.docx |
| 2 | `security_assurance_promise_set.xlsx` | `f824056dff929fc20c195dd923cb6816e84db3941a9e1f18ce53edce51128f45` | 15,669 | `canon/drops/20260907/raw/security_assurance_promise_set.xlsx` | https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/9x8wkh5r_Security_Assurance_Promise_Set.xlsx |
| 3 | `files_11.zip` | `67a53666384ac6fb39c7a325e246a6503cc60b7d9bacc83281dbfc8263c79aa4` | 66,281 | `canon/drops/20260907/raw/files_11.zip` | https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/g0h03gfl_files%20%2811%29.zip |
| 4 | `files_12.zip` | `95c78a5d4f8c01c4c4679a09cfba571b00393865fa98f3232bc4b61f5f917a60` | 26,429 | `canon/drops/20260907/raw/files_12.zip` | https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/k5pv9lwq_files%20%2812%29.zip |
| 5 | `files_13.zip` | `001cc4851b6dfcc5b63d8b7e3c542c80c45ba2e5eb4058a16e536642b4085a32` | 37,731 | `canon/drops/20260907/raw/files_13.zip` | https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/m9zamqye_files%20%2813%29.zip |

## §B · Unzipped inventory (per zip)

### files_11.zip · 3 files
| File | sha256 | size |
|---|---|---|
| `Rules_Service_Spec_v1.docx` | `9652fb47f10c9fd238a3ec26731f7b8331b22a0e066554ca9d703294fe9f6ae1` | 17,521 |
| `Rule_Book_Library_v1.xlsx` | `fc5c1a9caeae1c75908250f299f9c16788df42e88b8840f99d94b19e98742ad6` | 16,806 |
| `System_Rules_Registry.xlsx` | `af591c0ac76cfeb5d758efec7ab7faac98439ec34aba0e97ead5437afffb3557` | 35,796 |

### files_12.zip · 2 files
| File | sha256 | size | Note |
|---|---|---|---|
| `Security_Assurance_Promise_Set.xlsx` | `f824056dff929fc20c195dd923cb6816e84db3941a9e1f18ce53edce51128f45` | (same bytes as artefact 2) | **DUPLICATE** — byte-identical to top-level xlsx |
| `Security_Promise_Set_Amendments.docx` | `0adc3ff5222316110c8a3f09ff82da0f9d2b90da9e21a0f7cbbe5bc15cf65c42` | 13,387 | 8 amendments dated 3 September 2026 |

### files_13.zip · 2 files
| File | sha256 | size | Note |
|---|---|---|---|
| `Security_Assurance_Promise_Set.xlsx` | `f824056dff929fc20c195dd923cb6816e84db3941a9e1f18ce53edce51128f45` | (same bytes as artefact 2) | **DUPLICATE (2×)** — byte-identical to top-level xlsx and files_12 xlsx |
| `Security_Amendments_Trojan_Whisper.docx` | `20b459da0103c15126e25ea949bed34f767ab0a381c6ebc42fa875cd0a48bf65` | 24,635 | 10 amendments · 4 new promises · 5 rulings · dated 5 September 2026 |

**Observation:** The Security Assurance Promise Set xlsx is present in three of the five artefacts (top-level, files_12, files_13). All three copies are byte-identical (md5 `f15ab77d994271c92470977b5f373f81` × 3). The two amendments docs (files_12 and files_13) update the SAME xlsx — the xlsx itself does not carry the amendments; the amendment documents amend it.

## §C · Extraction outputs

| Source | Extraction target | Format | Row/paragraph count |
|---|---|---|---|
| doc0_governance_architecture.docx | `text/doc0_governance_architecture.txt` | txt | 465 paragraphs · 4 tables |
| security_assurance_promise_set.xlsx | `text/security_assurance_promise_set.md` + `.json` | md + json | 2 sheets · 27 rows (Security Assurance Set) + 7 (Legend) |
| Rules_Service_Spec_v1.docx | `text/Rules_Service_Spec_v1.txt` | txt | 57 paragraphs · 5 tables |
| Rule_Book_Library_v1.xlsx | `text/Rule_Book_Library_v1.md` + `.json` | md + json | 8 sheets (Index, Profiles, RB-PDP, RB-AIG, RB-FIN, RB-HLT, RB-MED, RB-RES) |
| System_Rules_Registry.xlsx | `text/System_Rules_Registry.md` + `.json` | md + json | 3 sheets · 287 rules in Registry + 15 Objectives + 8 Legend |
| Security_Promise_Set_Amendments.docx | `text/Security_Promise_Set_Amendments.txt` | txt | 43 paragraphs · 1 table |
| Security_Amendments_Trojan_Whisper.docx | `text/Security_Amendments_Trojan_Whisper.txt` | txt | 109 paragraphs · 3 tables |

Extraction script: `tools/extract_canon_drops_20260907.py` (python-docx 1.2.0 + openpyxl 3.1.5).

## §D · Live campaign health (probed WITHOUT interference · 2026-09-06T17:32Z)

**akki-vm** (dispatcher_pid 194861 · A-0-0p5B-v2 trainer 194863 running):
- Heartbeat `at_utc: 2026-09-06T17:32:30.904390Z` (fresh)
- `queue_progress: {index: 0, total: 4}` — still on A-0-0p5B-v2 (first entry)
- 3 trainer processes (parent + 2 workers), consistent with A-0-v1 architecture

**akki-vm-ii** (dispatcher_pid 177780 · B1-v1 trainer 154018 running):
- Heartbeat `at_utc: 2026-09-06T17:32:12.652220Z` (fresh)
- `queue_progress: {index: 0, total: 7}` — still on B-REF-3B-v2 (waiting behind B1-v1 seal)
- B1-v1 progress: step 700/963 at 17:28:25Z · loss 0.1466 · wallclock 11576s ≈ 3h 13m elapsed
- ETA B1-v1 seal ~18:00-18:10Z (263 steps × ~15-20s/step + 3 min held-out eval)

Both dispatchers healthy · both trainers alive · no interference from ingest.

## §E · Line-by-line extraction notes (produced this ingest wave)

- `notes/ingest_20260907/canon_doc0_governance_architecture_requirements.md` — 12 attributes (BA-1.1..12.3 + TA-1.1..12.3), 16 components (BR-1.1..16.2), 13 gaps (G-1..G-13), 4 rulings (R-1, R-2, R-3, R-5)
- `notes/ingest_20260907/canon_security_promise_set_requirements.md` — S-1..S-25 verbatim (25 promises, of which S-22..S-25 are new from Trojan/Whisper amendments)
- `notes/ingest_20260907/canon_security_amendments_requirements.md` — Promise Set 8 amendments (2026-09-03) + Trojan/Whisper 10 amendments (2026-09-05): T-1, T-2, W-1..W-8 + rulings R-7..R-11
- `notes/ingest_20260907/canon_rules_service_spec_v1_requirements.md` — invariants I-1..I-5, requirements RBM-1..RBM-22, business-type taxonomy v1, rulings R-1..R-4
- `notes/ingest_20260907/canon_rule_book_library_v1_inventory.md` — 6 rule books (RB-PDP FULL, RB-AIG FULL, others SKELETON) + 8 profiles
- `notes/ingest_20260907/canon_system_rules_registry_inventory.md` — 287-row registry inventory (per-rule enumeration deferred; structural inventory only)
- `notes/ingest_20260907/DOC0_LIVE_BUILD_DELTA.md` — Doc 0 Part 2 status vs actual programme build
- `notes/ingest_20260907/GAPS_TO_WAVES.md` — G-1..G-13 + Absent-status promises + T/W amendments mapped to LIFT/ADAPT/BUILD wave charters (NOT fired)
- `notes/ingest_20260907/OWNER_RULINGS_ONESHOT.md` — Consolidated ruling questions
