# S20 · Rule Book Library v1 · Detail Classification

**Source:** `canon/drops/20260907/extracted/files_11/Rule_Book_Library_v1.xlsx` (sha256 `fc5c1a9c…`) · extracted at `canon/drops/20260907/extracted/text/Rule_Book_Library_v1.md` (118 lines) · inventoried at `notes/ingest_20260907/canon_rule_book_library_v1_inventory.md`.

**Row inventory: 14 catalog entries** = 6 rule books + 8 profiles. Per-rule enumeration (~120 rules across FULL books) is deferred as INVENTORY per thin-kernel discipline.

## §A · Rule Books (6 rows)

| Row ID | Book ID | Rule book | Source standards | v1 status | Classification |
|---|---|---|---|---|---|
| RBL-1 | RB-PDP | Personal Data Protection | Kenya DPA 2019 · GDPR (EU) 2016/679 · POPIA (ZA) · NDPA 2023 (NG) · Data Protection (General) Regulations 2021 | **FULL** (18-22 rules) | REUSE (donor: extracted markdown 118 lines) |
| RBL-2 | RB-AIG | AI-System Governance | EU AI Act 2024/1689 (Arts. 9-15, Art. 14) · ISO/IEC 42001:2023 (paywalled) · NIST AI RMF 1.0 · ISO/IEC TR 5469:2024 (paywalled) | **FULL** (16-20 rules) | REUSE (donor: extracted markdown 118 lines) |
| RBL-3 | RB-FIN | Financial Services | Sources listed in sheet | **SKELETON** | NEW (per-rule authoring required) |
| RBL-4 | RB-HLT | Healthcare | — | **SKELETON** | NEW (per-rule authoring required) |
| RBL-5 | RB-MED | Media/Archive Rights | — | **SKELETON** | NEW (per-rule authoring required) |
| RBL-6 | RB-RES | Research/Academic | — | **SKELETON** | NEW (per-rule authoring required) |

## §B · Profiles (8 rows) — mirror Rules Service Spec §7

Business-type-to-rulebook mapping. Not counted as separate rows in NEW-scan (already tracked in S19 §E business-type taxonomy · 10 profiles). This detail file lists them once more for completeness:

| Row ID | Business type | Profile books (recommended) | Classification |
|---|---|---|---|
| RBL-P1 | Healthcare — hospital/clinic | RB-HLT + RB-PDP + RB-AIG | REUSE (Health book skeleton needs full write) |
| RBL-P2 | Media — broadcaster | RB-MED + RB-PDP + RB-AIG | REUSE |
| RBL-P3 | Media — content acquisition/production | RB-MED (licensing emphasis) + RB-PDP + RB-AIG | REUSE |
| RBL-P4 | Financial services — bank | RB-FIN + RB-PDP + RB-AIG | REUSE |
| RBL-P5 | Financial services — insurer | RB-FIN (insurance regulator variant) + RB-PDP + RB-AIG | REUSE |
| RBL-P6 | Agriculture / agri-tech | RB-PDP + RB-AIG + (agri book: skeleton only) | REUSE / NEW (agri) |
| RBL-P7 | University / research | RB-RES + RB-PDP + RB-AIG | REUSE |
| RBL-P8 | Telecommunications | RB-PDP + RB-AIG + (telecom book: skeleton only) | REUSE / NEW (telecom) |

Note: 2 additional profiles in Rules Service Spec §E (Government/public + Other/not-listed) share pattern.

## §C · S20 rollup

**Total catalog rows: 14** (6 books + 8 profiles).

| Bucket | Rows | % of 14 |
|---|--:|---:|
| DONE | 0 | 0.0% |
| PARTIAL | 0 | 0.0% |
| REUSE | 8 (RBL-1, RBL-2 + 6 profile mappings) | 57.1% |
| NEW | 6 (4 SKELETON books + 2 unmentioned profile-supporting books noted at profile-level) | 42.9% |

**Interpretation:** Rule Book Library v1 is a **content donor** — the two FULL books (RB-PDP + RB-AIG) provide ~40 rules of Personal Data Protection + AI-System Governance discipline. Adoption gated on Rules Service ceremony (RBM-14 admits book if every rule cited; RBM-17 instantiates through customer-tier ceremony). This is a **REUSE-heavy source** — the rule content is authored; the CEREMONY to admit it is NEW (see S19 rollup).

**Per-rule enumeration** (~120 rules in the FULL books) is deferred to when Rules Service is fired. Wave charter: **W-RULE-BOOK-LIBRARY** in master §E.2 (M effort for RB-PDP + RB-AIG only; L effort for all 6 books).

**Wave-honest limit:** the 4 SKELETON books (RB-FIN, RB-HLT, RB-MED, RB-RES) require external-standard citation authoring. Sources are named in the sheet but bodies are empty. Not blocking — the two FULL books satisfy the base bundle path (RBM-16 base bundle = Personal Data Protection + AI-System Governance).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
