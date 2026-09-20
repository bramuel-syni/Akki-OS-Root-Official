# CP-REGISTRY-V5-INGEST-AND-VERIFY · custody ingest + openpyxl authoritative verification

**Timestamp**: 2026-09-20T~19:45Z
**Trigger**: Owner directive verbatim this-session — "RULING 5 UNBLOCKED — the v5 registry file has landed. [...] Ingest per standard custody discipline: download to owner_drops with timestamped path, sha256-pin, manifest entry, then authoritative openpyxl verification: (a) System Rules Registry data row count = 602 exact, (b) delta vs v4 (`72160287…`) is EXACTLY SFP-1 through SFP-7, all Tier A, zero removals, zero edits to the 595 shared rows — byte-identical statements, (c) CON-1..31 unchanged vs v4. [...] If the delta is anything other than exactly those seven rows, STOP-AND-REPORT before G5 opens."
**Disposition**: **STOP-AND-REPORT triggered.** All 3 owner-mandated checks PASS. Two net-new SHEETS discovered beyond owner's scope-description. G5-v5 does **NOT** open until owner ruling on the net-new sheets.

## Custody drop metadata

- **URL**: `https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/a84gf1c1_Master_Requirements_Registry%20%285%29.xlsx`
- **Drop path**: `custody/owner_drops/20260920T1900Z/Master_Requirements_Registry_v5.xlsx`
- **Downloaded via**: `curl -sSL` at 2026-09-20T~19:44Z
- **file size**: **115,136 bytes**
- **sha256**: **`00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`**
- **v4 predecessor sha256** (custody `owner_drops/20260920T1600Z/Master_Requirements_Registry_v4.xlsx`): `72160287dcc4bddc5b921ab391d020bfda0f19e48dbffd122b70f45b6fead588`

## Owner-mandated verification checks · all PASS

### (a) System Rules Registry data row count = 602 exact · ✅ PASS

`openpyxl` inspection of the `System Rules Registry` sheet:
- v4: 595 data rows (11 cols)
- v5: **602 data rows** (11 cols)
- Expected v5: 602
- Result: **exactly 602 · PASS**

Row-count is measured on non-empty rows (any cell in the row has non-empty content). Unique Rule ID count = 471 in v5 (464 v4 + 7 SFP additions); the 131-row difference between data-rows (602) and unique-IDs (471) is the same 131-row gap that already existed in v4 (595 data rows − 464 unique IDs = 131) — i.e., structural section-header / spacer / continuation rows in the sheet that carry no Rule ID in col-0. This is a v4-inherited artefact, not a v5-introduced structural change.

### (b) delta = exactly SFP-1 through SFP-7 (all Tier A, zero removals, zero edits) · ✅ PASS

- **Net-new rule IDs**: `{'SFP-1', 'SFP-2', 'SFP-3', 'SFP-4', 'SFP-5', 'SFP-6', 'SFP-7'}` — **exactly 7 · matches owner spec byte-precisely**
- **Removed rule IDs**: **∅ · zero removals**
- **Edited rule IDs** (any of the 464 v4-shared rules whose full-row tuple differs between v4 and v5): **∅ · zero edits**
- **Byte-identical statement discipline**: all 464 v4-shared rules preserved bytewise (per-row full-tuple equality across all 11 cols)

**Rule-name verification (byte-verbatim against owner's independent sanity pass)**:

| Rule ID | Statement head (v5 SRR col-1 · first ~30 chars) | Owner-stated name | Match |
|---|---|---|---|
| SFP-1 | `\| Assertion Floor \| Subjects:` | Assertion Floor | ✅ |
| SFP-2 | `\| Certainty-to-Evidence Binding \|` | Certainty-to-Evidence Binding | ✅ |
| SFP-3 | `\| Acceptance Floor \| Subjects:` | Acceptance Floor | ✅ |
| SFP-4 | `\| Custody Floor \| Subjects:` | Custody Floor | ✅ |
| SFP-5 | `\| Non-Conformance Ceiling \|` | Non-Conformance Ceiling | ✅ |
| SFP-6 | `\| Release Budget \| Subjects:` | Release Budget | ✅ |
| SFP-7 | `\| Reproduction Ceiling \|` | Reproduction Ceiling | ✅ |

**Tier A verification**: All 7 SFP-1..7 rows in the NEW `QA Verification` sheet (col 6 "Sampling tier") carry **"A — 100%"** verbatim. Note: the "Tier A" designation lives in the NEW `QA Verification` sheet, not in the `System Rules Registry` sheet's 11-col header (which has `Rule ID · Statement · Objective · Promise/Source Document · Doc · Status · Enforcement Class · Domain · Source · Relationship · Builder Status` — no explicit "Tier" column). SFP-1..7 SRR-rows all show `Status = 'PROPOSED'`, `Domain = 'O14 Governance Architecture'`, `Doc = 'security_function_policies_v1'`, `Source = 'Security_Function_Policies_v1.docx'`, `Relationship = 'Added at refresh 20 Sep 2026 (c) — surfaced by the audit-sta...'`.

### (c) CON-1..31 byte-identical vs v4 · ✅ PASS

Full-row tuple equality check across all 11 SRR columns for each of the 31 CON-N rules:

- **CON drifts**: **0** — all 31 CON-1 through CON-31 rows byte-identical between v4 and v5.

## STOP-AND-REPORT · net-new SHEETS discovered beyond owner scope

**Owner's scope-description** was strictly "delta vs v4 is EXACTLY SFP-1 through SFP-7 [...] all Tier A, zero removals, zero edits to the 595 shared rows — byte-identical statements". This describes the RULE-LEVEL delta inside the `System Rules Registry` sheet only.

**Discovered STRUCTURAL delta beyond owner's scope**: **v5 introduces 2 NET-NEW SHEETS** not present in v4:

### Net-new sheet #1 · `QA Verification` (602 data rows · 10 cols)

- **Header**: `Rule ID · Doc · Status · Primary verification class · Secondary class · Evidence required (primary) · Sampling tier · Auditor verdict · Evidence examined (ref) · Finding ref`
- **Purpose (inferred from content)**: audit-tooling companion sheet mapping every one of the 602 `System Rules Registry` rules (identified by `Rule ID` col-0) to its QA verification classification. First data row: `('A5.1', 'Doc 1', 'CANON', 'V7 — Document & design inspection', '', 'Specification text against implementation description; prove', 'A — 100%', '', '', '')`.
- **Coverage**: one row per SRR rule (602 rows · full coverage).
- **Not authoritative for rule content**: this sheet is a METADATA COMPANION to `System Rules Registry`. The rule ID is the join key; the rule TEXT lives in `System Rules Registry`.

### Net-new sheet #2 · `QA Legend` (9 data rows · 4 cols)

- **Header**: `Class · Name · Evidence standard · Derivation pattern (first match, in this order)`
- **Purpose (inferred from content)**: legend defining the verification classes V1..V9 (or similar) referenced by the `QA Verification` sheet's `Primary verification class` + `Secondary class` columns.
- **Sample rows**:
    - `('V1', 'Test evidence', 'Golden-input, byte-identical output; RED-first test ID; ratchet manife...', 'determinist|byte-identical|golden|hash|signature|signed|repr...')`
    - `('V2', 'Structural evidence', 'Negative-scan or AST rule present, named, and green in CI; s...', 'MUST NOT|must not|no code path|exactly one|only .* may|never...')`
    - `('V3', 'Record evidence', 'Ledger rows inspected; hash-chain verifier receipt; refused ...', 'receipt|[Ll]edger|recorded|metered event|written before|appe...')`
    - `('V4', 'Governance-record evidence', 'DECISIONS.md entry; ceremony record with tier, countersign, ...', 'ceremony|countersign|ratif|ruling|witness|DECISIONS|canon_re...')`
    - `('V5', 'Failure-injection demonstration', 'Dependency made unreachable or check made to error; observed...', 'fail[- ]closed|refuse|refusal|unreachable|cannot complete|er...')`
    - ... and 4 more rows (V6-V9)
- **Not authoritative for rule content**: this sheet defines an out-of-band verification-classification vocabulary that maps into the `QA Verification` sheet columns.

### This-desk analysis (report-only · not a unilateral ruling)

The 2 net-new sheets appear to be **audit-tooling companions** that expand the workbook's SCOPE from "just the ratified rule text" to "ratified rule text + per-rule QA verification classification + legend for the classification vocabulary". Under a **narrow reading** of owner's directive (delta scoped to System Rules Registry sheet only), the 3 owner-mandated checks all PASS and G5-v5 could open. Under a **broad reading** (delta = entire workbook structural shape), the 2 net-new sheets are unanticipated structural drift and require owner ruling.

Per owner's verbatim "**STOP-AND-REPORT before G5 opens**" and per SO §11 stop-condition #2 (canon-vs-scope-description conflict), this-desk **STOPS on G5-v5 open** and reports both readings for owner ruling.

**Suggested owner-ruling readings** (this-desk hands-off pending owner):

1. **Reading N · Narrow** — 3 owner-mandated checks all PASS; the 2 net-new sheets are audit-tooling companions that do NOT change the ratified rule content of `System Rules Registry`; G5-v5 opens against `System Rules Registry` sheet only (602 rows · SFP-1..7 in first slice); QA Verification + QA Legend sheets are registered as informational-only companions with no G5-invariant claims made against them at this-wave.
2. **Reading B · Broad-with-companion-integration** — the QA Verification sheet is load-bearing (it names the verification class + sampling tier per rule, which G5 should honour); G5-v5 opens against BOTH sheets, with per-rule invariants that CITE the QA Verification classification (e.g., V1-classified rules get RED-first tests, V2-classified rules get AST-scan invariants) and align sampling tier to test-authoring intensity (A/100% = full-invariant, other tiers = sampled).
3. **Reading H · Halt-and-re-drop** — owner did not mention these sheets and may have intended a different file; owner re-uploads a v5 file WITHOUT the QA sheets or explicitly ratifies their inclusion.
4. **Reading D · Owner-alternative** — something this-desk hasn't enumerated.

**This-desk lean (if forced to choose · non-authoritative)**: Reading N is the safest step forward (G5-v5 opens against the SRR sheet only per the ratified authority). Reading B is attractive if the QA Verification classification is intended to shape test authorship; but it doubles the G5 scope and is not what owner described as "SFP-1..7 land in the FIRST slice". Reading H is only necessary if owner explicitly wants the audit sheets stripped.

## Canon anchors

- `custody/owner_drops/20260920T1900Z/Master_Requirements_Registry_v5.xlsx` (v5 · sha256 `00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d` · 115,136 bytes · **NOT-YET-RATIFIED** pending net-new-sheets ruling).
- `custody/owner_drops/20260920T1600Z/Master_Requirements_Registry_v4.xlsx` (v4 · sha256 `72160287dcc4bddc5b921ab391d020bfda0f19e48dbffd122b70f45b6fead588` · was never ratified per Ruling 5 verbatim).
- `custody/owner_drops/20260920T1300Z/Master_Requirements_Registry_v3.xlsx` (v3 · sha256 `79d4456224392ac6e936739ca80e8ba39d782b8d6af9d7bc2245d2a798c94a51` · **currently ratified authority** until Ruling 5 v5 ratification lands).
- Owner directive Ruling 5 verbatim (this-session · 2026-09-20T~19:00Z + v5-unblock 2026-09-20T~19:40Z).
- CP-CONTENT-REGISTRY-INGEST-DROP seal `6d910bbe` (predecessor · ingested Content Registry Spec + journey v2 alongside v4).
- CP-G5-V4-PREP-INVENTORY receipt `phase0/spec_hunt_receipts/20260920T1840Z_g5_v4_prep_inventory.md` (v4 prep · superseded by this v5 verification).
- SO §11 stop-conditions (#2 canon-vs-scope conflict + owner-explicit STOP-AND-REPORT before G5 opens).
- SO §6.4 NOTHING-BEYOND (this-wave banks ingestion + verification only · does NOT open G5-v5 · does NOT extract atomic rules · does NOT author invariants).

## Standing bounds preserved

zero push · terminal `pytest` only · no `testing_agent` · additive-only §3.8 · three-repo discipline · ratchet monotonic-up (unchanged at 5640 · this receipt does not edit any test surface or `baseline_failures.json`).

## Disposition

- **v5 file custody-tracked** at drop path with sha256-pin.
- **3 owner-mandated content checks PASS** (row count 602 · SFP-1..7 delta · CON-1..31 byte-identical).
- **2 net-new sheets flagged** for owner ruling (QA Verification + QA Legend).
- **G5-v5 does NOT open** pending owner ruling on net-new sheets.
- **Sprint order unchanged**: R-86 CP-APP-JS-UNIFY-SCHEDULE-AND-DRIFT-ANNOTATE (Ruling 1 · in-flight) → R-87 CP-BLOCKED-VOCABULARY-CORRECTION (Ruling 2) → R-88+ CP-CONTENT-REGISTRY-WAVE (Ruling 4) → R-XX G5-v5 wave (Ruling 5) when net-new-sheets ruling lands.
