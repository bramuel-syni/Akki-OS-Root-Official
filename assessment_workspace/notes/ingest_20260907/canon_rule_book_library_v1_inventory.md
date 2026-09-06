# Rule Book Library v1 · Inventory

**Source:** `canon/drops/20260907/extracted/files_11/Rule_Book_Library_v1.xlsx` (sha256 `fc5c1a9c…`)  
**Extracted:** `canon/drops/20260907/extracted/text/Rule_Book_Library_v1.md`

## §A · Structure

8 sheets:
1. `Index` — 10 rows · rule book catalog with status
2. `Profiles` — 13 rows · profile-to-book mapping (mirrors Rules Service Spec §7 taxonomy)
3. `RB-PDP` — 12 rows · Personal Data Protection rule book (FULL)
4. `RB-AIG` — 11 rows · AI-System Governance rule book (FULL)
5. `RB-FIN` — 11 rows · Financial Services rule book (SKELETON)
6. `RB-HLT` — 10 rows · Healthcare rule book (SKELETON)
7. `RB-MED` — 10 rows · Media/Archive rule book (SKELETON)
8. `RB-RES` — 10 rows · Research/Academic rule book (SKELETON)

## §B · Index (verbatim status)

Each rule book is atomic (one regulatory domain). Status: **FULL** = every rule written, cited, and checked against source text. **SKELETON** = sources named, sections and expected rule count set, rules not yet written.

| Book ID | Rule book | Source standards/regulations | Free to verify? | Sections | Expected rules | v1 status |
|---|---|---|---|---|---|---|
| RB-PDP | Personal Data Protection | Kenya DPA 2019 (primary) · Data Protection (General) Regulations 2021 · GDPR (EU) 2016/679 as international reference · POPIA (ZA) and NDPA 2023 (NG) noted as regional variants | Yes — all | Lawful basis & consent · Data-subject rights · Sensitive-category data · Cross-border transfer · Retention & erasure · Breach notification (72h) · Automated decisions (s.35/Art.22) · DPO & accountability | 18–22 | **FULL — next** |
| RB-AIG | AI-System Governance | EU AI Act 2024/1689 (Arts. 9–15 high-risk, Art. 14 oversight) · ISO/IEC 42001:2023 (paywalled) · NIST AI RMF 1.0 · ISO/IEC TR 5469:2024 (paywalled) | EU AI Act, NIST: yes · ISO: paywalled | Risk classification · Data & training governance · Human oversight (5 capabilities) · Transparency & record-keeping · Accuracy, robustness, cybersecurity · Post-market monitoring · Determinism boundary (platform-native) | 16–20 | **FULL — next** |
| RB-FIN | Financial Services | (sources listed in sheet, SKELETON only) | — | — | — | **SKELETON** |
| RB-HLT | Healthcare | — | — | — | — | **SKELETON** |
| RB-MED | Media/Archive Rights | — | — | — | — | **SKELETON** |
| RB-RES | Research/Academic | — | — | — | — | **SKELETON** |

**FULL count:** 2 of 6 (RB-PDP, RB-AIG).  
**SKELETON count:** 4 of 6.

## §C · Profiles (mapping to business type)

Sheet `Profiles` (13 rows) mirrors Rules Service Spec §7 Table 3. See `canon_rules_service_spec_v1_requirements.md` §E for the full mapping.

## §D · Detail sheets

Sheet content per rule book (RB-PDP, RB-AIG, RB-FIN, RB-HLT, RB-MED, RB-RES) is preserved verbatim in `canon/drops/20260907/extracted/text/Rule_Book_Library_v1.md`. Per-rule enumeration is deferred to when the Rules Service is fired (thin-kernel: not fired now).

Two FULL rulebooks are seeded and ready for ratification-through-ceremony pending Rules Service Spec §9 R-1..R-4 rulings.

## §E · Wave-honest limit

Per-rule enumeration of RB-PDP (18-22 rules) and RB-AIG (16-20 rules) not reproduced here. Verbatim rows preserved in the extracted markdown and JSON at `canon/drops/20260907/extracted/text/Rule_Book_Library_v1.{md,json}` — 118 lines total. Reproduce here on demand when authoring a Rules Service adoption wave.
