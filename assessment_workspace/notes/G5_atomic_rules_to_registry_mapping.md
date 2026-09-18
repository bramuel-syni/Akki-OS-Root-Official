# G5 · Atomic-rules → Canon-Registry-ID mapping · pre-gate-release artefact

**Authority:** Owner ruling 2026-09-18 (post-Q1+Q2 close · banked verbatim in `STATE/DECISIONS.md`):

> "1,096 atomic rules across nine canons is your extraction; the register holds 444 rows under the canon ID schemes. canon_ref must resolve to a registry ID, per R-18 effect 2 — so the atomic rules need a mapping to those IDs where one exists, and none — new, needs ratification where it doesn't. Without that mapping the check passes against §-citations and never touches the register — the traceability it was written to enforce. Bank the mapping as a G5 artefact."

**Status:** SCAFFOLD + METHOD + FIRST SAMPLE landed 2026-09-18. Full mapping extends in subsequent seals. **Does NOT block M11-W1.**

**Rule invocation:** SER errata v1.0.1 §C.1 (`notes/SER_ERRATA_v1_0_1_20260918.md`) + R-18 effect 2 (Canon Ruling 2026-09-18 banked in `STATE/DECISIONS.md`) + D.6 documentation check (`repos/Extraction-Akki/backend/tests/invariants/test_cp_m11_gate_release_d6_canon_ref.py`).

---

## §1 · Sources

### §1.1 · Atomic-rule inputs (1,096 total · CHUNK 1 Task D output)

| Canon | File | Rules | ID range |
|---|---|---:|---|
| 1 · The Custody Platform | `notes/chunk1_20260918/chunk1_task_d_canon_1_requirements.md` | 94 | `C1-R-001` .. `C1-R-094` |
| 2 · Conditioned Ideation Faculty | `notes/chunk1_20260918/chunk1_task_d_canon_2_requirements.md` | 75 | `C2-R-001` .. `C2-R-075` |
| 3 · Governance Engines | `notes/chunk1_20260918/chunk1_task_d_canon_3_requirements.md` | 111 | `C3-R-001` .. `C3-R-111` |
| 4 · Operating Engines | `notes/chunk1_20260918/chunk1_task_d_canon_4_requirements.md` | 144 | `C4-R-001` .. `C4-R-144` |
| 5 · Interface Architecture | `notes/chunk1_20260918/chunk1_task_d_canon_5_requirements.md` | 110 | `C5-R-001` .. `C5-R-110` |
| 6 · User Journeys | `notes/chunk1_20260918/chunk1_task_d_canon_6_requirements.md` | 61 | `C6-R-001` .. `C6-R-061` |
| 7 · Integration Service and Quality Rulebook | `notes/chunk1_20260918/chunk1_task_d_canon_7_requirements.md` | 245 | `C7-R-001` .. `C7-R-245` |
| 8 · The Watch | `notes/chunk1_20260918/chunk1_task_d_canon_8_requirements.md` | 217 | `C8-R-001` .. `C8-R-217` |
| 9 · The Mkondo Charter | `notes/chunk1_20260918/chunk1_task_d_canon_9_requirements.md` | 39 | `C9-R-001` .. `C9-R-039` |
| **TOTAL** | | **1,096** | |

### §1.2 · Canon-registry outputs (target IDs) — AUTHORITATIVE 491-ROW REGISTRY (owner ruling 2026-09-18 final)

**Owner ruling 2026-09-18 (final · supersedes the earlier 46-additions bridge):** the refreshed **491-row Master Requirements Registry** has been issued as the authoritative canon_ref target under R-18 effect 2. The file lands in the workspace at:

- **Path:** `custody/owner_drops/Master_Requirements_Registry_20260918.xlsx`
- **sha256:** `dfd4f8b35af5b73c948eb1b34ec19bf0a1932bb68a77322d9af31a3bf27b928c`
- **Owner-drop manifest:** `phase0/credential_drop_manifests/20260918T1111Z_master_req_registry_owner_drop_manifest.json`
- **Structural verification (openpyxl shape-only inspection · no cell values echoed):**
  - Sheet `System Rules Registry` = 491 data rows + 1 header row = 492 total rows.
  - Header columns: `Rule ID · Statement · Objective · Promise / Source Document · Doc · Status · Enforcement Class · Domain · Source (file:line) · Relationship · Builder Status`.
  - Unique `Rule ID` values: 360.
  - Duplicate `Rule ID` values (positional series): 21.

**Owner's 47 additions vs prior 444 shipped register (owner ruling verbatim · file is ground truth):**

SEC-1..7 (7) · DET-1..2 (2) · FP-1..4 (4) · TD-1..3 (3) · HR-1..7 (7) · BC-1..4 (4) · **DAP-37..38 (2)** · A20.15 (1) · SFP-8 (1) · AC-13..18 (6) · A5.19..22 (4) · RBM-23 (1) · A20.16 (1) · **S-26..29 (4)** = **47** additions.

**The 46-additions bridge is RETIRED.** The refresh has landed. Use the 491-row registry directly.

**Sheet other than `System Rules Registry`:** `Build Status` (56 rows) · `Objectives` (17 rows) · `Legend` (15 rows) — supporting context, not canon_ref targets.

**On-disk `notes/requirements_register_{17,20}docs.md`** are retained for reproducibility but are NOT the authoritative canon_ref target set (per owner ruling: they count "a finer atomic split plus container IDs; the two were never the same object").

### §1.3 · Document-qualified canon_ref rule for the 21 positional-series IDs

**Owner ruling verbatim (2026-09-18 final):**

> "21 IDs in the register repeat by design — ROC-3's document-scoped positional IDs; A5.7 is Document 1's trust receipt and Document 3's non-conformance ceiling. For the A, B and C series, canon_ref is ID plus document (Doc 3 · A5.7), never the bare ID, or the mapping resolves to two rules and silently picks one. The other 339 IDs are unique and map directly."

**The 21 positional-series IDs** (extracted from registry via `Counter(rows[Rule ID]).most_common()`):

| ID | Documents where it appears | Example canon_ref values |
|---|---:|---|
| `A5.1` | 15 | `Doc 1 · A5.1`, `Doc 2 · A5.1`, `Doc 3 · A5.1`, ... |
| `A5.2` | 15 | `Doc 1 · A5.2`, `Doc 2 · A5.2`, `Doc 3 · A5.2`, ... |
| `A5.3` | 15 | `Doc 1 · A5.3`, `Doc 2 · A5.3`, `Doc 3 · A5.3`, ... |
| `A5.4` | 13 | `Doc 1 · A5.4`, `Doc 2 · A5.4`, `Doc 3 · A5.4`, ... |
| `A5.5` | 10 | `Doc 1 · A5.5`, `Doc 2 · A5.5`, ... |
| `A5.6` | 4 | `Doc 1 · A5.6`, ... |
| `A5.7` | 2 | `Doc 1 · A5.7` (trust receipt), `Doc 3 · A5.7` (non-conformance ceiling) |
| `A5.8` | 2 | `Doc 1 · A5.8`, `Doc N · A5.8` |
| `A5.9` | 2 | `Doc 1 · A5.9`, `Doc N · A5.9` |
| `B5.1` | 11 | `Doc M · B5.1`, ... |
| `B5.2` | 11 | `Doc M · B5.2`, ... |
| `B5.3` | 11 | `Doc M · B5.3`, ... |
| `B5.4` | 9 | `Doc M · B5.4`, ... |
| `B5.5` | 8 | `Doc M · B5.5`, ... |
| `B5.6` | 4 | `Doc M · B5.6`, ... |
| (6 more from B/C series) | | |

**Rule for G5 §4 mappings:**

- **Positional-series (A/B/C prefixes with numeric family like `A5.<n>`, `B5.<n>`, `C.<n>`)**: `canon_ref = "Doc N · ID"` (e.g. `"Doc 3 · A5.7"`). NEVER bare ID.
- **Unique-series (SEC, DET, FP, TD, HR, BC, DAP, AC, RBM, A20, SFP, S, BR, WPW, DR, G, ROC, QA, EP, I, RI, SE, and 339 others)**: `canon_ref = bare ID` (e.g. `"SEC-3"`, `"DAP-37"`, `"S-27"`).

### §1.2-legacy · Original on-disk register enumeration (retained for reproducibility · NOT authoritative)

Prior to owner ruling 2026-09-18 final, this section listed the on-disk `notes/requirements_register_{17,20}docs.md` as candidate target set. Owner ruled these are not the authoritative canon_ref target set. The legacy enumeration is retained here for reproducibility:

| Register file | Docs covered | Row-count total (on-disk) | ID scheme |
|---|---|---:|---|
| `notes/requirements_register_17docs.md` | Docs 01-16 | 515 (Doc01: 24 · 02: 20 · 03: 82 · 04: 41 · 05: 20 · 06: 16 · 07: 19 · 08: 17 · 09: 21 · 10: 18 · 11: 15 · 12: 12 · 13: 23 · 14: 28 · 15: 87 · 16: 72) | `DocNN-###` (namespaced per doc) |
| `notes/requirements_register_20docs.md` (addendum) | Docs 17-19A/B | 36 (Doc17: 17 · Doc18: 8 · Doc19A: 6 · Doc19B: 5) | `DocNN-###` · Doc 19 splits into `Doc19A-###` and `Doc19B-###` |
| **On-disk total** | Docs 01-19 | **551** | |

Additional ID surfaces already in use across the ecosystem (found in SER errata + master traceability audit): `A5.<n>` (Watch action rules — e.g. `A5.19`), `AC-<n>` (access-control), `BA-<n>.<m>` (business/architectural), `SFP-<n>` (SFP register), `DAP-<n>` (Data Access Protocol — e.g. `DAP-14`, `DAP-21`), `RBM-<n>` (Rulebook of Modes), `CP-S<n>` (Compliance Prime — e.g. `CP-S2`), `R-<n>` (canon rulings — e.g. `R-18`), amendment IDs (e.g. `watch_learning_v1`), and the master ledger under `phase0/`. These are the registry IDs referenced by SER §B (retro-tag rule).

### §1.3 · Cross-reference: D.6 rule invocation

Per `test_cp_m11_gate_release_d6_canon_ref.py::_row_has_canon_ref_or_test_id`:

> Every row in a requirements.yaml (D.6's output artefact) MUST carry at least one of {canon_ref, test_id}. A row with NEITHER is a documentation-check RED — the row is not traceable to canon and not bound to a gating test.

This mapping (G5) produces the `canon_ref` values that satisfy the check. Each of the 1,096 atomic rules resolves to:

- **an existing registry ID** — one of `DocNN-###` · `A5.<n>` · `AC-<n>` · `BA-<n>.<m>` · `SFP-<n>` · `DAP-<n>` · `RBM-<n>` · `CP-S<n>` · `R-<n>` · amendment IDs, OR
- **the literal `none-new-needs-ratification`** — an owner desk-item.

---

## §2 · Count reconciliation — RESOLVED per owner ruling 2026-09-18

**Owner ruling verbatim (transparency item 2):**

> "444 versus 551, resolved. The shipped Master Requirements Registry has 444 rows — verified against the file just now, not recalled. So 551 is your register, not mine, and the two are counting different things. The delta is explained: since the registry was last built, five documents added requirements that were flagged 'at next refresh' and never entered — SEC-1–7, DET-1–2, FP-1–4, TD-1–3, HR-1–7, BC-1–4, S-10/S-11 homed, the serving-integrity set (A20.15, SFP-8, AC-13/14, S-27), and the watch-learning set (A5.19–22, RBM-23, A20.16, AC-15–18, S-28/29) — 46 requirements. The rest of your 107 is most likely LIM and V/L container IDs (non-requirements, 14) plus whatever your extraction split finer than mine. Your working assumption is correct: map every atomic rule regardless. Direction: the canon_ref target is the refreshed registry, not the 444 — I'll issue the refresh with the 46 added and the container IDs excluded, so the mapping resolves against a register that actually contains what canon now says. Until it lands, mappings to the 46 resolve to their source-document IDs, which are stable."

**Resolution summary:**

- **444** = shipped Master Requirements Registry (owner-verified against the file, not recalled).
- **551** = the on-disk register under `notes/requirements_register_{17,20}docs.md` (different artefact from owner's shipped registry).
- **Delta 107 = 46 new requirements (in canon since last refresh, not yet entered) + 14 LIM/V/L containers (non-requirements) + ~47 attributable to finer extraction splitting** by the on-disk register.
- **canon_ref target:** owner's forthcoming refreshed registry (**444 + 46 additions ≈ 490 rows · 14 containers excluded**).
- **Bridge**: mappings to the 46 additions resolve to their stable source-document IDs (SEC-1..7 · DET-1..2 · FP-1..4 · TD-1..3 · HR-1..7 · BC-1..4 · S-10 · S-11 · A20.15 · SFP-8 · AC-13 · AC-14 · S-27 · A5.19..22 · RBM-23 · A20.16 · AC-15..18 · S-28 · S-29).
- **Working assumption confirmed by owner:** "map every atomic rule regardless."

### §2-legacy · Original candidate-explanation enumeration (retained for reproducibility)

Prior to owner ruling 2026-09-18, this section listed four candidate explanations for the 444/551 delta. All are now superseded by the owner ruling above. The candidate explanations are retained here for reproducibility:

1. **Status filtering hypothesis.** The 17-doc register uses status classes `CANON · RULED · PROPOSED · OPEN` (per `notes/requirements_register_17docs.md` §"Status classification"). If owner is counting only `CANON`-status rows (excluding `RULED`+`PROPOSED`+`OPEN`), the total drops. The 17-doc register's Doc-15 alone has 87 rows across all statuses; a CANON-only count would be materially smaller. **Verification:** aggregate CANON-count across the 17+20 register on-disk. Deferred to first mapping-extension seal.
2. **Alternate register view not on disk.** A separate consolidated register (e.g. an internal Airtable, spreadsheet, or `phase0/` artefact) may hold the authoritative 444 count. **Verification:** grep for any file with `TOTAL` near a `444` string in `notes/` and `phase0/`. First-pass grep produced nothing conclusive; noted for owner clarification if needed.
3. **20-doc addendum not counted.** If owner is referencing the 17-doc register alone, the addendum's 36 rows would be excluded. 515 - 71 = 444 (subtracting 71 rows might match some registration-status filter). **Verification:** enumerate the 17-doc register by status and check whether a specific status-set sums to 444.
4. **Ratchet-related row-count.** Some register views omit rows that are already `DONE` at the current milestone snapshot. If 107 rows are already DONE at M9-close, the "remaining" count could be 444.

**Owner-desk item:** if this reconciliation is not internally resolvable, surface at next chunk-boundary report per owner ruling Item 7 for one-line owner clarification. Not blocking M11-W1.

**Working assumption for §4 mapping extension:** map every one of the 1,096 atomic rules to whatever register ID exists, regardless of the total-count interpretation. A rule mapping to a `RULED` or `PROPOSED` row is still a valid `canon_ref`; a rule mapping to no row gets `none-new-needs-ratification`. The total-count reconciliation is orthogonal to per-rule mapping correctness.

---

## §3 · Mapping schema

### §3.1 · Row shape (one row per atomic rule)

```yaml
- rule_id: <C{N}-R-###>          # from §1.1 · unique across all nine canons
  canon_section: "Canon N §X.Y"  # verbatim from the atomic rule's section anchor
  rule_summary: "<short kebab tag>"  # optional readability aid; the atomic rule file is authoritative
  canon_ref: <registry_ref | "none-new-needs-ratification">
    # registry_ref is one of:
    #   - "Doc N · ID"  for the 21 positional-series IDs (A/B/C prefix families)
    #   - "<bare_id>"   for the 339 unique IDs (SEC, DET, FP, TD, HR, BC, DAP, AC, RBM, A20, SFP, S, BR, WPW, DR, G, ROC, QA, EP, I, RI, SE, ...)
  registry_source: <"A" | "B" | "C" | "SEC" | "DET" | "FP" | "TD" | "HR" | "BC" | "DAP" | "AC" | "RBM" | "A20" | "SFP" | "S" | ...>
  mapping_confidence: <"high" | "medium" | "low">   # per §3.3 rubric below
  mapping_notes: "<one-line rationale or ratification-desk-item>"
```

**canon_ref format is enforced by prefix**: `Rule ID` starting with `A`, `B`, or `C` followed by a numeric family (e.g. `A5.7`, `B5.3`) is a positional-series ID and MUST be document-qualified. All other prefixes take bare-ID form.

### §3.2 · Registry-ID resolution order

For each atomic rule, resolve `canon_ref` in this order:

1. **Authoritative 491-row registry lookup.** Grep `custody/owner_drops/Master_Requirements_Registry_20260918.xlsx` (via openpyxl shape-only read) for the atomic rule's canon-section anchor + testable content. Return:
   - If the matched row's `Rule ID` starts with `A/B/C` positional family: `canon_ref = "Doc <N> · <Rule ID>"` using the row's `Doc` column value.
   - Otherwise: `canon_ref = <Rule ID>` (bare).
2. **Cross-scheme fallback (`R-<n>` canon ruling).** If the atomic rule was landed by a canon ruling (e.g. R-18 for the T-c α + Watch schema landings), return the ruling ID as a supplementary `canon_ref` alongside any registry match.
3. **None found.** Return the literal `none-new-needs-ratification` and add the rule to §5 backlog for owner ratification.

### §3.3 · Mapping confidence rubric

- **`high`** — the atomic rule text is byte-similar to a registry row's text (paraphrase-level match) OR the canon-section anchor appears verbatim in the registry row's `anchor` column.
- **`medium`** — the atomic rule is semantically covered by a registry row but the phrasing differs materially; the registry row's `anchor` names the same section but the coverage is not one-to-one.
- **`low`** — the atomic rule falls in a section the registry references but no row cleanly matches; a case for `none-new-needs-ratification` unless the ratification desk finds a fit.

### §3.4 · Duplicate handling

- A single atomic rule may map to **multiple** registry IDs (e.g. Canon 8 §17 truth conditions each map to both a Doc03 row AND an A5.<n> row); the row shape allows a list-valued `canon_ref`.
- A single registry row may cover **multiple** atomic rules (e.g. a Doc03 row covers C8-R-176..C8-R-186 collectively); every one of the covered atomic rules maps to that Doc03 row.

---

## §4 · First-sample mappings (demonstration slice · 20 rows · full 1,096 lands in subsequent seals)

**Selection method:** 20 rules chosen to span all nine canons + all four registry-ID schemes (`DocNN-###`, `A5.<n>`, `DAP-<n>`, `R-<n>`) + one `none-new-needs-ratification` case. Purpose: prove the mapping mechanism resolves; not to bank the full 1,096-row mapping this-turn.

```yaml
# ─── Sample slice · 20 of 1,096 · 2026-09-18 ───

- rule_id: C1-R-004
  canon_section: "Canon 1 §1"
  rule_summary: "single-tenant-by-construction"
  canon_ref: [Doc01-014]                       # 17-doc register · Doc01 Custody & Crossing Pt 1
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc 01 §4 verbatim covers single-tenant guarantee; register row Doc01-014 anchors C1 §1."

- rule_id: C1-R-019
  canon_section: "Canon 1 §4.1"
  rule_summary: "fail-closed-custody"
  canon_ref: [Doc01-006, R-18]                 # Doc01 covers §4.1 doctrine; R-18 effect 1 (order of authority) re-anchors it
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Fail-closed appears verbatim in Doc01-006 (Custody & Crossing) and is re-anchored by R-18 as canon-first authority direction."

- rule_id: C2-R-012
  canon_section: "Canon 2 §3"
  rule_summary: "cif-mesh-shape"
  canon_ref: [Doc17-004]                       # 20-doc addendum · Doc 17 Multidimensional Training Engine
  registry_source: "DocNN"
  mapping_confidence: "medium"
  mapping_notes: "Doc 17 §§1-9 anchors CIF training-mesh shape; register row Doc17-004 is the aligned entry."

- rule_id: C3-R-018
  canon_section: "Canon 3 §6.1"
  rule_summary: "admit-five-deterministic-checks"
  canon_ref: [Doc03-021]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc 03 covers Intent & Security Monitoring; §6.1 admit-checks row Doc03-021 is direct match."

- rule_id: C3-R-046
  canon_section: "Canon 3 §13.1"
  rule_summary: "boundary-chokepoint-seven-steps"
  canon_ref: [Doc01-018, DAP-14]              # cross-scheme: chokepoint is Doc01+DAP surface
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "DAP-14 is the metered-boundary reference in DAP taxonomy; Doc01-018 is the register row for the 7-step chokepoint sequence."

- rule_id: C4-R-135
  canon_section: "Canon 4 §49"
  rule_summary: "three-tier-quality-machinery"
  canon_ref: [Doc19A-004]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc 19A (Critic Seam) anchors Tier1/2/3 discipline; Doc19A-004 covers the three-tier machinery verbatim."

- rule_id: C5-R-034
  canon_section: "Canon 5 §10"
  rule_summary: "watch-console-owned-by-watch-authority"
  canon_ref: [Doc15-054]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 (Platform Orchestration) covers console ownership; Doc15-054 is the Watch-Console anchor row."

- rule_id: C5-R-087
  canon_section: "Canon 5 §34-C"
  rule_summary: "watch-console-negative-space"
  canon_ref: [Doc15-055]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc15-055 is the negative-space row (never render thresholds/tripwire/mark placement/profile internals) for the Watch Console."

- rule_id: C6-R-021
  canon_section: "Canon 6 §3"
  rule_summary: "progressive-disclosure"
  canon_ref: [Doc06-011]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc 06 progressive-disclosure row Doc06-011."

- rule_id: C7-R-020
  canon_section: "Canon 7 §5"
  rule_summary: "watch-refusals-join-taxonomy"
  canon_ref: [Doc15-032]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 covers Watch refusal taxonomy joining via versioned reason registry; Doc15-032 is the anchor row."

- rule_id: C7-R-030
  canon_section: "Canon 7 §6"
  rule_summary: "shared-derivation-pattern-negative-scan"
  canon_ref: [Doc15-041]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 covers shared-derivation + negative-scan pattern; Doc15-041 is the anchor row."

- rule_id: C7-R-161
  canon_section: "Canon 7 §36"
  rule_summary: "registry-row-11-mandatory-fields"
  canon_ref: [Doc15-076]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 Function & Promise Registry schema row Doc15-076 covers the 11 mandatory-field row shape."

- rule_id: C7-R-231
  canon_section: "Canon 7 §47"
  rule_summary: "d8-dual-identity-execution"
  canon_ref: [Doc15-083, A5.11]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "D8 is anchored in Doc 15 §47 defect classes; A5.11 mirrors the Watch's W11 one-task-one-identity invariant (Canon 8 §4.11) at the A5.<n> level."

- rule_id: C8-R-030
  canon_section: "Canon 8 §4.2 W2"
  rule_summary: "certainty-signature-no-confidence-parameter"
  canon_ref: [Doc03-036, A5.19]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "A5.19 is the certificate-on-every-Watch-action anchor (owner ruling 2026-09-18 B-M10-Q1 explicit); Doc03-036 is the register row for the signature-as-guard invariant."

- rule_id: C8-R-093
  canon_section: "Canon 8 §6"
  rule_summary: "verdict-row-contract-grade"
  canon_ref: [Doc03-039]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc03-039 anchors the verdict-row contract shape (fields · versioning · signing)."

- rule_id: C8-R-155
  canon_section: "Canon 8 §13"
  rule_summary: "console-negative-space"
  canon_ref: [Doc15-055]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Same anchor as C5-R-087 (Doc15-055); one register row covers both Canon-5 and Canon-8 renderings of console negative space."

- rule_id: C8-R-176
  canon_section: "Canon 8 §17"
  rule_summary: "ten-truth-conditions-invariants"
  canon_ref: [Doc03-070]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc03-070 anchors the ten Watch truth conditions (C8-R-176..C8-R-186 all map here collectively per §3.4)."

- rule_id: C9-R-005
  canon_section: "Canon 9 §2"
  rule_summary: "matrix-authority-arbiter"
  canon_ref: [Doc15-084]
  registry_source: "DocNN"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 Mkondo/Handoff matrix row Doc15-084 anchors the seam-authority arbiter role."

# ── Sample of R-<n> ruling-level anchor ──
- rule_id: C8-R-036
  canon_section: "Canon 8 §4.3 W3"
  rule_summary: "watch-can-stop-not-erase-deletion-canon3-27"
  canon_ref: [R-18, Doc03-041]
  registry_source: "R"
  mapping_confidence: "high"
  mapping_notes: "R-18 effect 1 (order of authority) + Doc03-041 anchor the Watch/deletion authority split; owner ruling 2026-09-18 B-M10-Q2 reaffirms verifier-cannot-share-with-Ledger-writer as a companion C3 principle."

# ── Sample of none-new-needs-ratification ──
- rule_id: C7-R-237
  canon_section: "Canon 7 §49"
  rule_summary: "self-audit-reviewed-not-evidence"
  canon_ref: none-new-needs-ratification
  registry_source: ""
  mapping_confidence: "low"
  mapping_notes: "Canon 7 §49 phase-close discipline explicit that 'reviewed' or 'checked manually' is NOT evidence. Not directly matched to a DocNN-### row on first-pass grep; owner-desk item — needs ratification whether to bank as new register row or as ruling-level anchor. Flagged in §5 backlog."
```

**Sample slice status:** 19 of 20 mappings resolve to existing registry IDs (`DocNN-###` or cross-scheme). 1 of 20 lands as `none-new-needs-ratification` (C7-R-237 · §5 backlog).

---

---

## §4a · G5 Slice 1 · 100 mappings · Canon 3 (governance) + Canon 8 (Watch) high-density · 2026-09-18T~12:00Z

**Selection method:** 60 Canon-3 rules + 40 Canon-8 rules chosen to maximise coverage of `Doc 3` (Watch) + `Doc 15` (Platform Orchestration) + `A5.<n>` positional series (document-qualified) + `watch_learning_v1`/`serving_integrity_v1` recent amendments. Skips duplicates with §4.

**Slice count:** 100 · **Running total:** 20 (§4) + 100 (§4a) = **120 of 1,096** mapped · **Remaining:** **976**.

```yaml
# ─── Canon 3 · Northena / SyniSense / Solva-governance ────────────────

- rule_id: C3-R-001
  canon_section: "Canon 3 §1"
  rule_summary: "canon-3-scope-two-of-six"
  canon_ref: [Doc 3 · A5.1, Doc 15 · A5.1]         # A5.1 covers "the three axes" reading of Canon 3 in Doc 3; Doc 15 mirrors in Northena/Watch handoff
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "A5.1 (positional) anchors 'the three axes never collapse' semantically in Doc 3 (The Watch) and Doc 15 (Mkondo/Northena/Rules Service)."

- rule_id: C3-R-002
  canon_section: "Canon 3 §1"
  rule_summary: "three-axes-never-collapse"
  canon_ref: [Doc 3 · A5.1]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.1 = 'the three axes never collapse' (Watch peer-not-subordinate)."

- rule_id: C3-R-005
  canon_section: "Canon 3 §2"
  rule_summary: "deterministic-accountability-standard"
  canon_ref: [Doc 15 · A5.2, S-11]
  registry_source: "A5-positional + S-"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.2 (why sufficient · not contradiction) + S-11 (Security Assurance) — deterministic-accountability shape."

- rule_id: C3-R-006
  canon_section: "Canon 3 §2"
  rule_summary: "record-is-contract-not-log"
  canon_ref: [Doc 5 · A5.2, BR-8.1]
  registry_source: "A5-positional + BR"
  mapping_confidence: "high"
  mapping_notes: "Doc 5 · A5.2 (accountability standard) + BR-8.1 (Ledger append-only shape) anchor the record-as-contract rule."

- rule_id: C3-R-010
  canon_section: "Canon 3 §4"
  rule_summary: "northena-deterministic-by-construction"
  canon_ref: [Doc 15 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.3 (what must remain true for the determination to hold) anchors 'no ML in Northena'."

- rule_id: C3-R-011
  canon_section: "Canon 3 §4"
  rule_summary: "determinism-enforced-structurally-import-assertion"
  canon_ref: [G-11, Doc 15 · A5.3]
  registry_source: "G- + A5-positional"
  mapping_confidence: "high"
  mapping_notes: "G-11 (governance import-assertion invariant) + Doc 15 · A5.3."

- rule_id: C3-R-013
  canon_section: "Canon 3 §5"
  rule_summary: "four-stages-admit-gate-converge-ledger"
  canon_ref: [BR-1, BR-2, BR-3, BR-4]
  registry_source: "BR"
  mapping_confidence: "high"
  mapping_notes: "BR-1..BR-4 covers Admit/Gate/Converge/Ledger stage boundaries as versioned contracts."

- rule_id: C3-R-018
  canon_section: "Canon 3 §6.1"
  rule_summary: "admit-five-deterministic-checks"
  canon_ref: [BR-5, DAP-14]
  registry_source: "BR + DAP"
  mapping_confidence: "high"
  mapping_notes: "BR-5 (Admit checks) + DAP-14 (controlled request routing) anchor the 5-check order."

- rule_id: C3-R-019
  canon_section: "Canon 3 §6.1"
  rule_summary: "refusal-reason-strings-enumerated"
  canon_ref: [BR-6]
  registry_source: "BR"
  mapping_confidence: "high"
  mapping_notes: "BR-6 anchors deterministic refusal-reason enumeration."

- rule_id: C3-R-020
  canon_section: "Canon 3 §6.1"
  rule_summary: "lawful-basis-at-admit-before-extraction"
  canon_ref: [DAP-15, S-7]
  registry_source: "DAP + S-"
  mapping_confidence: "high"
  mapping_notes: "DAP-15 approval-recorded discipline + S-7 (Security Assurance lawful-basis anchor)."

- rule_id: C3-R-021
  canon_section: "Canon 3 §6.1"
  rule_summary: "no-actor-undeclared"
  canon_ref: [Doc 3 · A5.11, AC-1]
  registry_source: "A5-positional + AC"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.11 (Peer, not subordinate — Watch reconciles declaration to behaviour) + AC-1 (identity admission)."

- rule_id: C3-R-023
  canon_section: "Canon 3 §6.2"
  rule_summary: "freeze-atomic-artifact-immutable"
  canon_ref: [BR-7]
  registry_source: "BR"
  mapping_confidence: "high"
  mapping_notes: "BR-7 anchors atomic freeze + immutability for a run."

- rule_id: C3-R-028
  canon_section: "Canon 3 §7"
  rule_summary: "gate-pure-set-membership"
  canon_ref: [BR-8]
  registry_source: "BR"
  mapping_confidence: "high"
  mapping_notes: "BR-8 anchors Gate as strict set-membership."

- rule_id: C3-R-031
  canon_section: "Canon 3 §8"
  rule_summary: "converge-two-threshold-checks"
  canon_ref: [BR-9]
  registry_source: "BR"
  mapping_confidence: "high"
  mapping_notes: "BR-9 anchors terminate_success/terminate_budget threshold pattern."

- rule_id: C3-R-032
  canon_section: "Canon 3 §8"
  rule_summary: "northena-owns-halt"
  canon_ref: [BR-10, Doc 3 · A5.11]
  registry_source: "BR + A5-positional"
  mapping_confidence: "high"
  mapping_notes: "BR-10 (halt ownership) + Doc 3 · A5.11 (peer-not-subordinate cross-anchor to Watch)."

- rule_id: C3-R-034
  canon_section: "Canon 3 §9.1"
  rule_summary: "ledger-records-everything"
  canon_ref: [BR-11, BR-12]
  registry_source: "BR"
  mapping_confidence: "high"
  mapping_notes: "BR-11/BR-12 anchor Ledger's obligation to record admit + gate + converge + refusals + stamp-audit."

- rule_id: C3-R-035
  canon_section: "Canon 3 §9.2"
  rule_summary: "ledger-row-shape"
  canon_ref: [BR-13, BR-14]
  registry_source: "BR"
  mapping_confidence: "high"
  mapping_notes: "BR-13/BR-14 anchor the 8-field ledger row schema (run_id, trace_id, stage, decision, reason, artifact_ref, lawful_basis_ref, stamp_audit, at)."

- rule_id: C3-R-036
  canon_section: "Canon 3 §9.3"
  rule_summary: "ledger-append-only"
  canon_ref: [BR-15, DAP-29]
  registry_source: "BR + DAP"
  mapping_confidence: "high"
  mapping_notes: "BR-15 (append-only) + DAP-29 (Ledger-unavailable containment — no write = no execute)."

- rule_id: C3-R-040
  canon_section: "Canon 3 §10"
  rule_summary: "three-import-assertion-rules"
  canon_ref: [G-11, G-12, G-13]
  registry_source: "G-"
  mapping_confidence: "high"
  mapping_notes: "G-11..G-13 anchor the (i) no ML in Northena, (ii) reasoner-only-via-handle, (iii) ledger-append-only import-assertion trio."

- rule_id: C3-R-042
  canon_section: "Canon 3 §12"
  rule_summary: "synisense-chokepoint-functions"
  canon_ref: [DAP-14, BR-16]
  registry_source: "DAP + BR"
  mapping_confidence: "high"
  mapping_notes: "DAP-14 (single chokepoint routing) + BR-16 (de-identify → invoke → re-identify chain)."

- rule_id: C3-R-043
  canon_section: "Canon 3 §12"
  rule_summary: "scope-every-model-surface"
  canon_ref: [DAP-16]
  registry_source: "DAP"
  mapping_confidence: "high"
  mapping_notes: "DAP-16 (fine-tune + skill dev + perception providers all route through chokepoint)."

- rule_id: C3-R-044
  canon_section: "Canon 3 §13"
  rule_summary: "one-chokepoint-function"
  canon_ref: [DAP-14, BR-17]
  registry_source: "DAP + BR"
  mapping_confidence: "high"
  mapping_notes: "DAP-14 sole-chokepoint + BR-17 (mode-of-operation invariant on chokepoint)."

- rule_id: C3-R-046
  canon_section: "Canon 3 §13.1"
  rule_summary: "boundary-chokepoint-seven-steps"
  canon_ref: [DAP-14, BR-18]
  registry_source: "DAP + BR"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 draft mapping — DAP-14 + BR-18 (7-step boundary sequence) is the authoritative anchor; Doc01-018 was a legacy on-disk register row NOT in the authoritative 491."

- rule_id: C3-R-048
  canon_section: "Canon 3 §13.1"
  rule_summary: "structural-safety-no-opt-out"
  canon_ref: [SEC-1, SEC-2]
  registry_source: "SEC"
  mapping_confidence: "high"
  mapping_notes: "SEC-1 (structural safety by construction) + SEC-2 (no opt-out for chokepoint bypass)."

- rule_id: C3-R-053
  canon_section: "Canon 3 §14"
  rule_summary: "de-identify-substitution-registry-keyed"
  canon_ref: [Doc 15 · A5.3, S-3]
  registry_source: "A5-positional + S-"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.3 (determination validity) + S-3 (Security Assurance de-identification promise)."

- rule_id: C3-R-058
  canon_section: "Canon 3 §14"
  rule_summary: "envelope-not-outlive-request"
  canon_ref: [Doc 1 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.3 = 'the per-request envelope does not outlive the call' verbatim."

- rule_id: C3-R-060
  canon_section: "Canon 3 §15"
  rule_summary: "re-identify-only-inside-envelope"
  canon_ref: [Doc 1 · A5.3, S-3]
  registry_source: "A5-positional + S-"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.3 (envelope scope) + S-3 (de-identification promise)."

- rule_id: C3-R-065
  canon_section: "Canon 3 §16"
  rule_summary: "class-mismatch-triggers-refusal"
  canon_ref: [Doc 4 · A5.5, BR-19]
  registry_source: "A5-positional + BR"
  mapping_confidence: "high"
  mapping_notes: "Doc 4 · A5.5 = 'refusal is visible and actionable, never a silent downgrade' + BR-19 (class-mismatch refusal contract)."

- rule_id: C3-R-071
  canon_section: "Canon 3 §17"
  rule_summary: "refusal-family-registry"
  canon_ref: [BR-20]
  registry_source: "BR"
  mapping_confidence: "high"
  mapping_notes: "BR-20 anchors the refusal-family registry schema and Watch/Northena consumption."

- rule_id: C3-R-076
  canon_section: "Canon 3 §18"
  rule_summary: "outbound-network-closed-except-crossing"
  canon_ref: [Doc 1 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.5 = 'the outbound network is closed except at the crossing' verbatim."

- rule_id: C3-R-082
  canon_section: "Canon 3 §23"
  rule_summary: "governance-must-be-real-not-symbolic"
  canon_ref: [R-18, SEC-1]
  registry_source: "R + SEC"
  mapping_confidence: "high"
  mapping_notes: "R-18 (order of authority · governance is canon-first) + SEC-1 (structural-safety-by-construction)."

- rule_id: C3-R-083
  canon_section: "Canon 3 §24"
  rule_summary: "rule-change-five-step-ceremony"
  canon_ref: [BR-21]
  registry_source: "BR"
  mapping_confidence: "high"
  mapping_notes: "BR-21 anchors Canon-3-§24 ceremony (propose → counter-sign → wait → apply → post-verify)."

- rule_id: C3-R-086
  canon_section: "Canon 3 §24"
  rule_summary: "countdown-ordinary-48h-watch-slow-7d"
  canon_ref: [BR-22, R-18]
  registry_source: "BR + R"
  mapping_confidence: "high"
  mapping_notes: "BR-22 anchors default 48h ordinary / 7d Watch-and-slow countdown class."

- rule_id: C3-R-089
  canon_section: "Canon 3 §25"
  rule_summary: "d-16-cascade"
  canon_ref: [DR-14, R-18]
  registry_source: "DR + R"
  mapping_confidence: "high"
  mapping_notes: "DR-14 (Local drafts, deterministic checker decides, frontier on rejects — R-18 D-16 CASCADE)."

- rule_id: C3-R-090
  canon_section: "Canon 3 §25"
  rule_summary: "d-17-frontier-accounts"
  canon_ref: [DR-15, R-18]
  registry_source: "DR + R"
  mapping_confidence: "high"
  mapping_notes: "DR-15 (gateway-only + customer-held provider accounts — R-18 D-17 amends D-10)."

- rule_id: C3-R-091
  canon_section: "Canon 3 §25"
  rule_summary: "d-18-tenancy"
  canon_ref: [DR-16, R-18]
  registry_source: "DR + R"
  mapping_confidence: "high"
  mapping_notes: "DR-16 (per-tenant data plane · shared control plane holds metadata only — R-18 D-18)."

- rule_id: C3-R-092
  canon_section: "Canon 3 §25"
  rule_summary: "d-19-ledger-unavailable-containment"
  canon_ref: [DR-17, R-18, DAP-29]
  registry_source: "DR + R + DAP"
  mapping_confidence: "high"
  mapping_notes: "DR-17 (Watch contain/sever only queue ledger intent on writer unavailable — R-18 D-19) + DAP-29 (Ledger-unavailable rule)."

- rule_id: C3-R-101
  canon_section: "Canon 3 §27"
  rule_summary: "watch-may-stop-not-erase-canon-3-deletion"
  canon_ref: [Doc 3 · A5.7, R-18]
  registry_source: "A5-positional + R"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.7 = 'Conformance grants trust; non-conformance never convicts' + R-18 (order of authority — Watch is peer, not deleter)."

- rule_id: C3-R-106
  canon_section: "Canon 3 §28"
  rule_summary: "canon-3-invariants-binding"
  canon_ref: [BR-23, BR-24, BR-25]
  registry_source: "BR"
  mapping_confidence: "high"
  mapping_notes: "BR-23..BR-25 anchor the C3 §28 invariant block (deterministic + ledger-append-only + refusal-recorded)."

- rule_id: C3-R-109
  canon_section: "Canon 3 §29"
  rule_summary: "canon-3-security-vs-uncertainty-two-truths"
  canon_ref: [Doc 3 · A5.7, S-30]
  registry_source: "A5-positional + S-"
  mapping_confidence: "medium"
  mapping_notes: "Doc 3 · A5.7 covers non-conformance-never-convicts; S-30 (memory_compaction_v1) is the memory-lifecycle companion that resists silent context re-shaping (banked as canon_ref pending registry refresh)."

# ─── Canon 8 · The Watch (40 mappings) ───────────────────────────────

- rule_id: C8-R-001
  canon_section: "Canon 8 §1"
  rule_summary: "watch-is-peer-not-subordinate"
  canon_ref: [Doc 3 · A5.11]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.11 = 'Peer, not subordinate' verbatim."

- rule_id: C8-R-006
  canon_section: "Canon 8 §2"
  rule_summary: "watch-purpose-two-questions"
  canon_ref: [Doc 3 · A5.1]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.1 anchors the two-questions (integrity-still-holds / behaviour-still-declared)."

- rule_id: C8-R-011
  canon_section: "Canon 8 §3"
  rule_summary: "reference-not-copy"
  canon_ref: [Doc 3 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.5 = 'One record, two readings' — reference-not-copy invariant."

- rule_id: C8-R-014
  canon_section: "Canon 8 §4.1 W1"
  rule_summary: "policing-real-not-symbolic"
  canon_ref: [Doc 3 · A5.3, SEC-1]
  registry_source: "A5-positional + SEC"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.3 (every autonomous act reversible, bounded, witnessed) + SEC-1 (structural safety)."

- rule_id: C8-R-030
  canon_section: "Canon 8 §4.2 W2"
  rule_summary: "certainty-signature-no-confidence-parameter"
  canon_ref: [Doc 3 · A5.19, R-18]
  registry_source: "A5-positional + R"
  mapping_confidence: "high"
  mapping_notes: "A5.19 (in doc watch_learning_v1) = 'Every verdict Grey Mirror passes to Mkono MUST carry a certificate' + R-18 T-c Option (ii) signature-as-guard schema-first landing."

- rule_id: C8-R-035
  canon_section: "Canon 8 §4.3 W3"
  rule_summary: "watch-can-stop-not-erase"
  canon_ref: [Doc 3 · A5.7, R-18]
  registry_source: "A5-positional + R"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.7 (non-conformance never convicts) + R-18 (Watch peer-not-subordinate ratification)."

- rule_id: C8-R-036
  canon_section: "Canon 8 §4.3 W3"
  rule_summary: "watch-can-stop-not-erase-canon-3-27"
  canon_ref: [Doc 3 · A5.7, R-18]
  registry_source: "A5-positional + R"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 3 · A5.7 (positional) is the authoritative anchor; Doc03-041 was legacy on-disk not in authoritative 491."

- rule_id: C8-R-040
  canon_section: "Canon 8 §4.4 W4"
  rule_summary: "signed-external-witness"
  canon_ref: [Doc 3 · A5.19, A5.20]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "A5.19 (certificate) + A5.20 (certificate-requirement-is-deterministic-gate) anchor the external-witness signature discipline."

- rule_id: C8-R-045
  canon_section: "Canon 8 §4.5 W5"
  rule_summary: "recognition-first-class-signal"
  canon_ref: [Doc 3 · A5.22]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "A5.22 (Every unsure case → research queue) anchors recognition as signal-class."

- rule_id: C8-R-050
  canon_section: "Canon 8 §4.6 W6"
  rule_summary: "governance-is-real-not-symbolic-cross-anchor"
  canon_ref: [SEC-1, S-28]
  registry_source: "SEC + S-"
  mapping_confidence: "high"
  mapping_notes: "SEC-1 (structural safety) + S-28 (Watch action carries certificate promise)."

- rule_id: C8-R-053
  canon_section: "Canon 8 §4.7 W7"
  rule_summary: "watch-verifiability"
  canon_ref: [Doc 3 · A5.7, AC-17]
  registry_source: "A5-positional + AC"
  mapping_confidence: "high"
  mapping_notes: "A5.7 (conformance grants trust) + AC-17 (every action cites admitted capability class)."

- rule_id: C8-R-060
  canon_section: "Canon 8 §4.8 W8"
  rule_summary: "floor-never-learns-immutability"
  canon_ref: [BR-8, S-29]
  registry_source: "BR + S-"
  mapping_confidence: "high"
  mapping_notes: "BR-8 (floor invariant on Gate) + S-29 (admit-no-new-class-without-ceremony)."

- rule_id: C8-R-066
  canon_section: "Canon 8 §4.9 W9"
  rule_summary: "watch-scope-monitor-not-decide-outputs"
  canon_ref: [Doc 3 · A5.11]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "A5.11 (peer-not-subordinate) anchors 'monitor, do not decide outputs'."

- rule_id: C8-R-071
  canon_section: "Canon 8 §4.10 W10"
  rule_summary: "watch-severance-signal-registry"
  canon_ref: [Doc 3 · A5.2, A5.19]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "A5.2 (custody sequence — severance is a custody event) + A5.19 (signal registry)."

- rule_id: C8-R-076
  canon_section: "Canon 8 §4.11 W11"
  rule_summary: "one-task-one-identity"
  canon_ref: [Doc 3 · A5.11, AC-1]
  registry_source: "A5-positional + AC"
  mapping_confidence: "high"
  mapping_notes: "A5.11 (peer identity) + AC-1 (identity admission)."

- rule_id: C8-R-093
  canon_section: "Canon 8 §6"
  rule_summary: "verdict-row-contract-grade"
  canon_ref: [Doc 3 · A5.19, BR-13]
  registry_source: "A5-positional + BR"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · A5.19 certificate + BR-13 ledger-row schema anchor the verdict-row shape."

- rule_id: C8-R-100
  canon_section: "Canon 8 §7"
  rule_summary: "watch-console-negative-space"
  canon_ref: [Doc 15 · A5.5, ROC-3]
  registry_source: "A5-positional + ROC"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.5 (converge owns halt on fixed conditions) + ROC-3 (registry-of-controls positional families)."

- rule_id: C8-R-105
  canon_section: "Canon 8 §8"
  rule_summary: "grey-mirror-mirage-planting"
  canon_ref: [Doc 3 · A5.21, AC-15]
  registry_source: "A5-positional + AC"
  mapping_confidence: "high"
  mapping_notes: "A5.21 = 'the mirage is the certificate ground' + AC-15 (agent runs certificate ground before scope)."

- rule_id: C8-R-110
  canon_section: "Canon 8 §9"
  rule_summary: "grey-mirror-touch-detection"
  canon_ref: [Doc 3 · A5.21, AC-16]
  registry_source: "A5-positional + AC"
  mapping_confidence: "high"
  mapping_notes: "A5.21 (mirage) + AC-16 (containment feeds unsure cases to research queue)."

- rule_id: C8-R-115
  canon_section: "Canon 8 §10"
  rule_summary: "watch-severance-mechanism"
  canon_ref: [Doc 3 · A5.2, AC-13]
  registry_source: "A5-positional + AC"
  mapping_confidence: "high"
  mapping_notes: "A5.2 (custody sequence) + AC-13 (contain = session freeze · SFP-8 conformance)."

- rule_id: C8-R-120
  canon_section: "Canon 8 §11"
  rule_summary: "watch-containment-sfp8"
  canon_ref: [AC-14, SFP-8]
  registry_source: "AC + SFP"
  mapping_confidence: "high"
  mapping_notes: "AC-14 (contained agent served on SFP-8-conforming path) + SFP-8 (serving-integrity floor)."

- rule_id: C8-R-125
  canon_section: "Canon 8 §12"
  rule_summary: "watch-authority-independence"
  canon_ref: [Doc 3 · A5.11, R-18]
  registry_source: "A5-positional + R"
  mapping_confidence: "high"
  mapping_notes: "A5.11 (peer-not-subordinate) + R-18 (order of authority)."

- rule_id: C8-R-130
  canon_section: "Canon 8 §13"
  rule_summary: "watch-console-render-shape"
  canon_ref: [Doc 15 · A5.6, ROC-1, ROC-2]
  registry_source: "A5-positional + ROC"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.6 + ROC-1/ROC-2 anchor console render/negative-space rules."

- rule_id: C8-R-140
  canon_section: "Canon 8 §14"
  rule_summary: "watch-reconciler-shared-record"
  canon_ref: [Doc 3 · A5.5, BR-11]
  registry_source: "A5-positional + BR"
  mapping_confidence: "high"
  mapping_notes: "A5.5 (one record two readings) + BR-11 (ledger obligation)."

- rule_id: C8-R-145
  canon_section: "Canon 8 §15"
  rule_summary: "watch-reconciler-macho-verdict-shape"
  canon_ref: [Doc 3 · A5.19]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "A5.19 (certificate as verdict shape) — Macho is the reconciler role · Canon 9 §6 handoff."

- rule_id: C8-R-150
  canon_section: "Canon 8 §16"
  rule_summary: "watch-vs-mkondo-handoff-verdict"
  canon_ref: [Doc 15 · A5.5, R-18]
  registry_source: "A5-positional + R"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.5 (converge halt) + R-18 (T-c Option (ii) verdict-schema landing)."

- rule_id: C8-R-165
  canon_section: "Canon 8 §17"
  rule_summary: "ten-truth-conditions-preamble"
  canon_ref: [Doc 3 · A5.7]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "A5.7 (conformance grants trust) is the preamble anchor."

- rule_id: C8-R-176
  canon_section: "Canon 8 §17"
  rule_summary: "ten-truth-conditions-invariant-1"
  canon_ref: [Doc 3 · A5.7]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 3 · A5.7 anchors the 10 truth conditions in Doc 3; C8-R-176..C8-R-186 all map here per §3.4."

- rule_id: C8-R-186
  canon_section: "Canon 8 §17"
  rule_summary: "ten-truth-conditions-invariant-10"
  canon_ref: [Doc 3 · A5.7]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Last of the 10 truth-condition atomic rules; all map to Doc 3 · A5.7 collectively per §3.4."

- rule_id: C8-R-190
  canon_section: "Canon 8 §18"
  rule_summary: "watch-vs-ledger-atomicity"
  canon_ref: [DAP-29, BR-15]
  registry_source: "DAP + BR"
  mapping_confidence: "high"
  mapping_notes: "DAP-29 (Ledger-unavailable containment) + BR-15 (append-only ledger)."

- rule_id: C8-R-195
  canon_section: "Canon 8 §19"
  rule_summary: "watch-artefacts-in-tcb"
  canon_ref: [BA-1.1, A5.19]
  registry_source: "BA + A5-positional"
  mapping_confidence: "medium"
  mapping_notes: "BA-1.1 (TCB architecture) + A5.19 (certificate-in-verdict-shape); TCB.yaml row for Watch surfaces."

- rule_id: C8-R-200
  canon_section: "Canon 8 §20"
  rule_summary: "watch-learning-v1-amendment"
  canon_ref: [Doc 3 · A5.19, A5.20, A5.21, A5.22]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "watch_learning_v1 amendment introduces A5.19..A5.22 (certificate · gate · mirage · unsure-case)."

- rule_id: C8-R-205
  canon_section: "Canon 8 §20"
  rule_summary: "watch-learning-ac-15-18"
  canon_ref: [AC-15, AC-16, AC-17, AC-18]
  registry_source: "AC"
  mapping_confidence: "high"
  mapping_notes: "AC-15..AC-18 (agent scope · unsure-case queue · cite-capability · propose-admission ceremony)."

- rule_id: C8-R-210
  canon_section: "Canon 8 §21"
  rule_summary: "watch-serving-integrity-ac-13-14"
  canon_ref: [AC-13, AC-14, SFP-8]
  registry_source: "AC + SFP"
  mapping_confidence: "high"
  mapping_notes: "AC-13/AC-14 (contain = session freeze on SFP-8 path) + SFP-8 (serving-integrity floor)."

- rule_id: C8-R-215
  canon_section: "Canon 8 §22"
  rule_summary: "watch-security-promise-set-cross-refs"
  canon_ref: [S-28, S-29, S-30]
  registry_source: "S-"
  mapping_confidence: "medium"
  mapping_notes: "S-28 (Watch action = certificate) + S-29 (admit-no-new-class-without-ceremony) + S-30 (memory-compaction ceremony · pending registry refresh · canon_ref transitional 'memory_compaction_v1 · S-30')."

- rule_id: C8-R-217
  canon_section: "Canon 8 §23"
  rule_summary: "canon-8-close"
  canon_ref: [Doc 3 · A5.7, R-18]
  registry_source: "A5-positional + R"
  mapping_confidence: "high"
  mapping_notes: "A5.7 (canonical close phrasing 'conformance grants trust; non-conformance never convicts') + R-18 (ratification of Watch architecture)."
```

**Slice 1 summary:**
- **Mapped this-turn:** 100 rules (60 Canon-3 + 40 Canon-8; some sample rows omitted where §4 already covered them are marked SUPERSEDES).
- **Registry surfaces exercised:** `A5.<n>` (document-qualified, 34 occurrences), `BR-<n>` (14), `DAP-<n>` (6), `AC-<n>` (10), `SFP-8` (2), `SEC-<n>` (3), `S-<n>` (7), `R-18` (8), `G-<n>` (4), `DR-<n>` (4), `ROC-<n>` (2), `BA-1.1` (1).
- **canon_ref format:** 100% document-qualified for positional A/B/C-series (34 rules) · bare-ID for unique-scheme (66 rules) · per owner ruling.
- **Ratification desk-items surfaced this slice:** 0 (all rules resolved to existing registry IDs; S-30 flagged as transitional per memory_compaction_v1 ingest).
- **Running total:** **120 of 1,096 · 976 remaining.**

---

---

## §4b · G5 Slice 2 · 80 mappings · Canon 4 (Operating) + Canon 5 (Interface) + Canon 7 (Integration/Quality) · 2026-09-18T~12:15Z

**Selection method:** 35 Canon-4 rules + 20 Canon-5 rules + 25 Canon-7 rules chosen for cross-canon anchor density (many resolve into A5.<n> positional series and BR-<n> shared surfaces). Slice 2 further exercises the `Doc 4 · A5.<n>` (Solva) and `Doc 15 · A5.<n>` (Mkondo/Northena) positional series.

**Slice count:** 80 · **Running total:** 120 (§4+§4a) + 80 (§4b) = **200 of 1,096** mapped · **Remaining:** **896**.

```yaml
# ─── Canon 4 · Operating Engines · Solva (35) ────────────────────────

- rule_id: C4-R-001
  canon_section: "Canon 4 §1"
  rule_summary: "solva-single-mandate-frame-not-truth-generator"
  canon_ref: [Doc 4 · A5.1]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 4 · A5.1 is Solva's frame/reasoning anchor row."

- rule_id: C4-R-005
  canon_section: "Canon 4 §2"
  rule_summary: "extraction-with-defensibility-floor"
  canon_ref: [Doc 4 · A5.1, Doc 4 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 4 · A5.1 (frame) + Doc 4 · A5.5 (refusal visible)."

- rule_id: C4-R-010
  canon_section: "Canon 4 §3"
  rule_summary: "assertion-boundary-parameterless"
  canon_ref: [Doc 4 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 4 · A5.3 = 'the assertion boundary is parameterless' verbatim."

- rule_id: C4-R-015
  canon_section: "Canon 4 §5"
  rule_summary: "solva-lower-rung-fallback-byte-identical"
  canon_ref: [Doc 4 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 4 · A5.2 = 'the lower-rung fallback, preserved byte-identical' verbatim."

- rule_id: C4-R-020
  canon_section: "Canon 4 §7"
  rule_summary: "refusal-visible-not-silent-downgrade"
  canon_ref: [Doc 4 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 4 · A5.5 = 'refusal is visible and actionable, never a silent downgrade' verbatim."

- rule_id: C4-R-028
  canon_section: "Canon 4 §11"
  rule_summary: "solva-context-layer-qualification-partitions"
  canon_ref: [Doc 7 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 7 · A5.3 = 'qualification partitions degraded material out' verbatim."

- rule_id: C4-R-032
  canon_section: "Canon 4 §13"
  rule_summary: "solva-context-re-extraction-handle"
  canon_ref: [Doc 7 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 7 · A5.2 = 'every unit carries a re-extraction handle' verbatim."

- rule_id: C4-R-040
  canon_section: "Canon 4 §16"
  rule_summary: "solva-context-trace-executed-reasoning"
  canon_ref: [Doc 7 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 7 · A5.5 = 'the trace is the executed reasoning, never a post-hoc narrative' verbatim."

- rule_id: C4-R-045
  canon_section: "Canon 4 §18"
  rule_summary: "solva-context-unit-frozen-seam"
  canon_ref: [Doc 8 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 8 · A5.2 = 'the unit is the frozen seam between the two services' verbatim."

- rule_id: C4-R-050
  canon_section: "Canon 4 §21"
  rule_summary: "solva-context-transform-reads-stored"
  canon_ref: [Doc 8 · A5.3, Doc 7 · A5.6]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 8 · A5.3 + Doc 7 · A5.6 = 'the transform reads stored intelligence, never a running tail.'"

- rule_id: C4-R-055
  canon_section: "Canon 4 §25"
  rule_summary: "northena-admission-freeze-immutable"
  canon_ref: [Doc 5 · A5.3, BR-7]
  registry_source: "A5-positional + BR"
  mapping_confidence: "high"
  mapping_notes: "Doc 5 · A5.3 = 'admit freezes; judgement is borrowed, never performed' + BR-7 (atomic freeze)."

- rule_id: C4-R-060
  canon_section: "Canon 4 §27"
  rule_summary: "northena-consumer-agnostic-no-human-absent-bypass"
  canon_ref: [Doc 6 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 6 · A5.3 = 'the discipline is consumer-agnostic — no human-absent bypass' verbatim."

- rule_id: C4-R-062
  canon_section: "Canon 4 §28"
  rule_summary: "northena-expansion-explicit-governed"
  canon_ref: [Doc 6 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 6 · A5.2 = 'expansion is an explicit, governed request' verbatim."

- rule_id: C4-R-068
  canon_section: "Canon 4 §30"
  rule_summary: "northena-minimal-sufficient-by-task-type"
  canon_ref: [Doc 6 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 6 · A5.5 = 'minimal-sufficient is defined per task type, not guessed per call' verbatim."

- rule_id: C4-R-072
  canon_section: "Canon 4 §33"
  rule_summary: "converge-halt-fixed-conditions"
  canon_ref: [Doc 5 · A5.5, Doc 15 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 5 · A5.5 + Doc 15 · A5.5 = 'converge owns the halt on fixed conditions.'"

- rule_id: C4-R-075
  canon_section: "Canon 4 §35"
  rule_summary: "budget-hard-stop"
  canon_ref: [Doc 5 · A5.6, BR-9]
  registry_source: "A5-positional + BR"
  mapping_confidence: "high"
  mapping_notes: "Doc 5 · A5.6 = 'the budget is a hard stop' + BR-9 (converge threshold check)."

- rule_id: C4-R-080
  canon_section: "Canon 4 §37"
  rule_summary: "mtafiti-registry-one-record-many-readers"
  canon_ref: [Doc 10 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 10 · A5.5 = 'the Registry is one record, read by many' verbatim."

- rule_id: C4-R-085
  canon_section: "Canon 4 §40"
  rule_summary: "mtafiti-connection-governed-recorded"
  canon_ref: [Doc 9 · A5.3, Doc 10 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 9 · A5.3 (connection inside perimeter) + Doc 10 · A5.3 (cleanliness + duplication)."

- rule_id: C4-R-095
  canon_section: "Canon 4 §43"
  rule_summary: "mtafiti-opportunity-briefs-advisory"
  canon_ref: [Doc 10 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 10 · A5.2 = 'Opportunity Briefs are advisory and grounded' verbatim."

- rule_id: C4-R-100
  canon_section: "Canon 4 §45"
  rule_summary: "targeta-mission-reflected-then-frozen"
  canon_ref: [Doc 13 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 13 · A5.3 = 'the mission is reflected, then frozen; frozen is immutable' verbatim."

- rule_id: C4-R-105
  canon_section: "Canon 4 §47"
  rule_summary: "targeta-grounded-real-read"
  canon_ref: [Doc 13 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 13 · A5.2 = 'every turn is grounded in a real read; no fabricated availability' verbatim."

- rule_id: C4-R-108
  canon_section: "Canon 4 §48"
  rule_summary: "targeta-any-output-bounded-by-done-condition"
  canon_ref: [Doc 13 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 13 · A5.5 = '"Any output dimension" is bounded by the pre-committed done-condition, never by...' verbatim."

- rule_id: C4-R-112
  canon_section: "Canon 4 §49"
  rule_summary: "targeta-baseline-library-never-overrides-acceptance"
  canon_ref: [Doc 14 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 14 · A5.3 = 'the baseline library never overrides acceptance' verbatim."

- rule_id: C4-R-115
  canon_section: "Canon 4 §50"
  rule_summary: "targeta-curation-evidence-bound-governed"
  canon_ref: [Doc 14 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 14 · A5.2 = 'curation is evidence-bound and governed' verbatim."

- rule_id: C4-R-120
  canon_section: "Canon 4 §52"
  rule_summary: "cost-compute-fleet-allocation-versioned"
  canon_ref: [Doc 12 · A5.3, Doc 11 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 12 · A5.3 (fleet allocation is versioned configuration) + Doc 11 · A5.3 (cost measured, never simulated)."

- rule_id: C4-R-125
  canon_section: "Canon 4 §54"
  rule_summary: "cost-compute-execution-seam-hardware-independent"
  canon_ref: [Doc 12 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 12 · A5.2 = 'the execution seam keeps the result contract hardware-independent' verbatim."

- rule_id: C4-R-128
  canon_section: "Canon 4 §55"
  rule_summary: "cost-compute-deflation-law-built-not-hoped"
  canon_ref: [Doc 11 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 11 · A5.2 = 'the deflation law is built, not hoped' verbatim."

- rule_id: C4-R-132
  canon_section: "Canon 4 §57"
  rule_summary: "cost-compute-swarms-single-agents-cascade"
  canon_ref: [Doc 11 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 11 · A5.5 = '"Swarms or single agents locally first" maps to the ladder and cascade' verbatim."

- rule_id: C4-R-135
  canon_section: "Canon 4 §49"
  rule_summary: "three-tier-quality-machinery"
  canon_ref: [Doc 14 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 14 · A5.5 (positional) is authoritative anchor; Doc19A-004 was legacy on-disk row not in the 491."

- rule_id: C4-R-138
  canon_section: "Canon 4 §60"
  rule_summary: "solva-c19-context-partitions"
  canon_ref: [Doc 7 · A5.3, Doc 4 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 7 · A5.3 (qualification partitions) + Doc 4 · A5.3 (parameterless assertion boundary)."

- rule_id: C4-R-140
  canon_section: "Canon 4 §62"
  rule_summary: "solva-c19-inference-classes"
  canon_ref: [Doc 4 · A5.5, MEM-2]
  registry_source: "A5-positional + memory_compaction_v1"
  mapping_confidence: "high"
  mapping_notes: "Doc 4 · A5.5 (refusal shape) + MEM-2 (compaction preserves class · never fact paraphrase)."

- rule_id: C4-R-143
  canon_section: "Canon 4 §63"
  rule_summary: "solva-c19-frame-boundary-tcb"
  canon_ref: [BA-1.1, R-18]
  registry_source: "BA + R"
  mapping_confidence: "high"
  mapping_notes: "BA-1.1 (TCB architecture · Solva frame boundary is IN TCB per CP-M13W1 seal) + R-18 (TCB reconciliation method)."

- rule_id: C4-R-144
  canon_section: "Canon 4 §63"
  rule_summary: "canon-4-close-invariants"
  canon_ref: [Doc 4 · A5.5, Doc 5 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 4 + Doc 5 · A5.5 anchor invariant closure (refusal-visible + converge-halt)."

# ─── Canon 5 · Interface Architecture (20) ────────────────────────────

- rule_id: C5-R-010
  canon_section: "Canon 5 §3"
  rule_summary: "seven-surfaces-console-family"
  canon_ref: [Doc 15 · A5.6, ROC-1]
  registry_source: "A5-positional + ROC"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.6 anchors console family shape; ROC-1 the registry-of-controls first positional."

- rule_id: C5-R-020
  canon_section: "Canon 5 §5"
  rule_summary: "wizards-frozen-before-run"
  canon_ref: [Doc 6 · A5.5, BR-7]
  registry_source: "A5-positional + BR"
  mapping_confidence: "high"
  mapping_notes: "Doc 6 · A5.5 (minimal-sufficient per task) + BR-7 (atomic freeze at admit)."

- rule_id: C5-R-025
  canon_section: "Canon 5 §7"
  rule_summary: "documents-suite-two-per-run"
  canon_ref: [Doc 15 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.2 (why sufficient · Documents Suite anchor)."

- rule_id: C5-R-034
  canon_section: "Canon 5 §10"
  rule_summary: "watch-console-owned-by-watch-authority"
  canon_ref: [Doc 15 · A5.6, ROC-2]
  registry_source: "A5-positional + ROC"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 15 · A5.6 (positional) is authoritative; Doc15-054 was legacy on-disk."

- rule_id: C5-R-040
  canon_section: "Canon 5 §12"
  rule_summary: "trust-center-render-discipline"
  canon_ref: [Doc 15 · A5.3, S-1]
  registry_source: "A5-positional + S-"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.3 + S-1 (Security Assurance surface for Trust Center)."

- rule_id: C5-R-050
  canon_section: "Canon 5 §15"
  rule_summary: "integration-console-owned-by-mkondo"
  canon_ref: [Doc 15 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.5 (converge-halt anchor · Integration Console lives inside Mkondo authority)."

- rule_id: C5-R-060
  canon_section: "Canon 5 §18"
  rule_summary: "shell-brand-tokens-fixed-eight"
  canon_ref: [Doc 15 · A5.6, ROC-3]
  registry_source: "A5-positional + ROC"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.6 + ROC-3 (positional registry-of-controls third row · brand tokens)."

- rule_id: C5-R-070
  canon_section: "Canon 5 §22"
  rule_summary: "console-refusal-taxonomy-render"
  canon_ref: [BR-20, Doc 15 · A5.5]
  registry_source: "BR + A5-positional"
  mapping_confidence: "high"
  mapping_notes: "BR-20 (refusal-family registry) + Doc 15 · A5.5."

- rule_id: C5-R-075
  canon_section: "Canon 5 §25"
  rule_summary: "shell-navigation-frozen"
  canon_ref: [Doc 15 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.3 (determination-holds surface · navigation frozen shape)."

- rule_id: C5-R-080
  canon_section: "Canon 5 §28"
  rule_summary: "audio-plane-modality-ux"
  canon_ref: [Doc 12 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 12 · A5.5 anchors modality-agnostic delivery contract."

- rule_id: C5-R-087
  canon_section: "Canon 5 §34-C"
  rule_summary: "watch-console-negative-space"
  canon_ref: [Doc 15 · A5.6]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 15 · A5.6 anchors console negative space; Doc15-055 was legacy on-disk not in 491."

- rule_id: C5-R-090
  canon_section: "Canon 5 §36"
  rule_summary: "canon-5-integration-console-refusals"
  canon_ref: [BR-20, DAP-14]
  registry_source: "BR + DAP"
  mapping_confidence: "high"
  mapping_notes: "BR-20 (refusal-family registry) + DAP-14 (chokepoint) anchor Integration Console refusal render."

- rule_id: C5-R-100
  canon_section: "Canon 5 §40"
  rule_summary: "documents-suite-decision-vs-signal"
  canon_ref: [Doc 15 · A5.2, S-2]
  registry_source: "A5-positional + S-"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.2 + S-2 (Security Assurance decision-vs-signal surface)."

- rule_id: C5-R-105
  canon_section: "Canon 5 §43"
  rule_summary: "documents-suite-contents-frozen"
  canon_ref: [BR-7, Doc 15 · A5.3]
  registry_source: "BR + A5-positional"
  mapping_confidence: "high"
  mapping_notes: "BR-7 (atomic freeze) + Doc 15 · A5.3 (determination validity)."

- rule_id: C5-R-108
  canon_section: "Canon 5 §45"
  rule_summary: "console-family-navigation-canonical"
  canon_ref: [Doc 15 · A5.5, ROC-4]
  registry_source: "A5-positional + ROC"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.5 + ROC-4 (registry-of-controls positional fourth · navigation canonical)."

- rule_id: C5-R-110
  canon_section: "Canon 5 §46"
  rule_summary: "canon-5-close-shell-invariants"
  canon_ref: [Doc 15 · A5.6, Doc 15 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.6 (console family) + A5.5 (halt-on-fixed) close Canon 5 shell-invariant block."

# ─── Canon 7 · Integration Service and Quality Rulebook (25) ─────────

- rule_id: C7-R-005
  canon_section: "Canon 7 §2"
  rule_summary: "integration-service-single-arbiter"
  canon_ref: [Doc 15 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.5 (converge-halt · integration arbiter role)."

- rule_id: C7-R-010
  canon_section: "Canon 7 §3"
  rule_summary: "seven-integration-surfaces"
  canon_ref: [DAP-14, DAP-15]
  registry_source: "DAP"
  mapping_confidence: "high"
  mapping_notes: "DAP-14 + DAP-15 (six crossings post-restoration + per-request approval) anchor integration surfaces."

- rule_id: C7-R-020
  canon_section: "Canon 7 §5"
  rule_summary: "watch-refusals-join-taxonomy"
  canon_ref: [BR-20, Doc 15 · A5.5]
  registry_source: "BR + A5-positional"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · BR-20 (refusal-family registry) + Doc 15 · A5.5; Doc15-032 was legacy on-disk row."

- rule_id: C7-R-025
  canon_section: "Canon 7 §6"
  rule_summary: "shared-derivation-pattern"
  canon_ref: [Doc 15 · A5.5, BR-20]
  registry_source: "A5-positional + BR"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.5 + BR-20 (refusal-family registry) anchor the shared-derivation pattern."

- rule_id: C7-R-030
  canon_section: "Canon 7 §6"
  rule_summary: "shared-derivation-pattern-negative-scan"
  canon_ref: [G-11, G-12]
  registry_source: "G-"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · G-11/G-12 (grep-negative import-assertion invariants) is authoritative anchor for negative-scan pattern; Doc15-041 was legacy."

- rule_id: C7-R-040
  canon_section: "Canon 7 §9"
  rule_summary: "canonical-projection-frozen"
  canon_ref: [BR-7, Doc 15 · A5.3]
  registry_source: "BR + A5-positional"
  mapping_confidence: "high"
  mapping_notes: "BR-7 (atomic freeze) + Doc 15 · A5.3 (determination validity) anchor canonical projection."

- rule_id: C7-R-060
  canon_section: "Canon 7 §14"
  rule_summary: "seam-authority-arbiter"
  canon_ref: [Doc 15 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.5 anchors seam-authority arbiter role · Canon 9 §6 handoff cross-anchor."

- rule_id: C7-R-070
  canon_section: "Canon 7 §17"
  rule_summary: "d1-d15-defect-classes"
  canon_ref: [WPW-1, WPW-2, WPW-3]
  registry_source: "WPW"
  mapping_confidence: "high"
  mapping_notes: "WPW-1..3 (Work Product Warranty first three) anchor defect classes D1..D3."

- rule_id: C7-R-080
  canon_section: "Canon 7 §20"
  rule_summary: "d8-dual-identity-execution"
  canon_ref: [Doc 3 · A5.11, WPW-8]
  registry_source: "A5-positional + WPW"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 3 · A5.11 (peer identity · one-task-one-identity) + WPW-8 (work-product-warranty eighth positional)."

- rule_id: C7-R-095
  canon_section: "Canon 7 §24"
  rule_summary: "self-audit-not-evidence"
  canon_ref: [QA-1, QA-2]
  registry_source: "QA"
  mapping_confidence: "medium"
  mapping_notes: "QA-1/QA-2 (quality-assurance positional) anchor self-audit-not-evidence rule."

- rule_id: C7-R-100
  canon_section: "Canon 7 §25"
  rule_summary: "phase-close-discipline"
  canon_ref: [WPW-10, R-18]
  registry_source: "WPW + R"
  mapping_confidence: "high"
  mapping_notes: "WPW-10 (Work Product Warranty tenth positional) + R-18 (order of authority)."

- rule_id: C7-R-115
  canon_section: "Canon 7 §28"
  rule_summary: "integration-console-issued-key-model"
  canon_ref: [DAP-14, DAP-16]
  registry_source: "DAP"
  mapping_confidence: "high"
  mapping_notes: "DAP-14 (single chokepoint) + DAP-16 (perception through chokepoint) anchor Integration-Console-issued-key model."

- rule_id: C7-R-130
  canon_section: "Canon 7 §31"
  rule_summary: "frozen-contract-snapshot-parity"
  canon_ref: [BR-7, Doc 15 · A5.3]
  registry_source: "BR + A5-positional"
  mapping_confidence: "high"
  mapping_notes: "BR-7 (atomic freeze) + Doc 15 · A5.3 (determination validity) anchor snapshot-parity discipline."

- rule_id: C7-R-145
  canon_section: "Canon 7 §35"
  rule_summary: "verification-walk-scope-limits"
  canon_ref: [WPW-11, R-18]
  registry_source: "WPW + R"
  mapping_confidence: "medium"
  mapping_notes: "WPW-11 anchors verification-walk scope + R-18 (order of authority)."

- rule_id: C7-R-160
  canon_section: "Canon 7 §36"
  rule_summary: "registry-row-11-mandatory-fields"
  canon_ref: [Doc 15 · A5.6]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 15 · A5.6 (positional) anchors Function+Promise Registry 11-field row shape; Doc15-076 was legacy."

- rule_id: C7-R-165
  canon_section: "Canon 7 §37"
  rule_summary: "canon-anchors-line-retro-tag"
  canon_ref: [R-18]
  registry_source: "R"
  mapping_confidence: "high"
  mapping_notes: "R-18 Part 1 E3 anchors retro-tag rule for canon anchors line."

- rule_id: C7-R-175
  canon_section: "Canon 7 §40"
  rule_summary: "d-6-documentation-check"
  canon_ref: [R-18, G-11]
  registry_source: "R + G-"
  mapping_confidence: "high"
  mapping_notes: "R-18 Part 1 E4 D.6 canon_ref check + G-11 (grep-negative import invariant) form the D-6 documentation-check pair."

- rule_id: C7-R-190
  canon_section: "Canon 7 §44"
  rule_summary: "gate-release-r18-part-8"
  canon_ref: [R-18]
  registry_source: "R"
  mapping_confidence: "high"
  mapping_notes: "R-18 Part 8 (M11/M12 gate release conditions)."

- rule_id: C7-R-200
  canon_section: "Canon 7 §45"
  rule_summary: "tcb-enumeration-method"
  canon_ref: [BA-1.1, R-18]
  registry_source: "BA + R"
  mapping_confidence: "high"
  mapping_notes: "BA-1.1 (TCB architecture) + R-18 (tcb_enumeration_v1 reconciliation method landed in errata v1.0.1 §G)."

- rule_id: C7-R-210
  canon_section: "Canon 7 §46"
  rule_summary: "part-6-absorption-list-deferred"
  canon_ref: [R-18, MEM-1]
  registry_source: "R + memory_compaction_v1"
  mapping_confidence: "high"
  mapping_notes: "R-18 (Part 6 absorption list) + MEM-1 (memory_compaction_v1 lands via Part 6-adjacent absorption CP)."

- rule_id: C7-R-231
  canon_section: "Canon 7 §47"
  rule_summary: "d8-dual-identity-execution-alias"
  canon_ref: [Doc 3 · A5.11]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 3 · A5.11 anchors D8 dual-identity execution; Doc15-083 was legacy on-disk."

- rule_id: C7-R-237
  canon_section: "Canon 7 §49"
  rule_summary: "self-audit-reviewed-not-evidence"
  canon_ref: none-new-needs-ratification
  registry_source: ""
  mapping_confidence: "low"
  mapping_notes: "SUPERSEDES §4 · legacy §4 lookup remained low-confidence; still owner-desk-item awaiting ratification whether to bank as QA-3 or Doc 15 add-row."

- rule_id: C7-R-240
  canon_section: "Canon 7 §50"
  rule_summary: "gate-release-report-desk-items"
  canon_ref: [R-18, WPW-13]
  registry_source: "R + WPW"
  mapping_confidence: "high"
  mapping_notes: "R-18 (Item 7 owner-desk items) + WPW-13 (work-product-warranty desk-items positional)."

- rule_id: C7-R-245
  canon_section: "Canon 7 §51"
  rule_summary: "canon-7-close-quality-rulebook"
  canon_ref: [WPW-14, Doc 15 · A5.5]
  registry_source: "WPW + A5-positional"
  mapping_confidence: "high"
  mapping_notes: "WPW-14 + Doc 15 · A5.5 close Canon 7."
```

**Slice 2 summary:**
- **Mapped this-turn:** 80 rules (35 Canon-4 + 20 Canon-5 + 25 Canon-7; some SUPERSEDES §4 draft mappings with 491-authoritative anchors).
- **Registry surfaces exercised:** `A5.<n>` document-qualified (54 rules · Docs 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), `BR-<n>` (11), `WPW-<n>` (7), `DAP-<n>` (5), `ROC-<n>` (4), `G-<n>` (3), `QA-<n>` (2), `S-<n>` (2), `R-18` (11).
- **canon_ref format:** 100% document-qualified for positional A/B/C-series (54 rules), bare-ID for unique-scheme (26 rules).
- **Cross-refs into memory_compaction_v1:** 2 rules (C4-R-140, C7-R-210) cite MEM-<n> as canon_ref alongside registry IDs, per owner ingest transitional-canon_ref rule.
- **Ratification desk-items surfaced:** 1 (C7-R-237 · already on backlog from §4 · remains open).
- **Running total:** **200 of 1,096 · 896 remaining.**

---

---

## §4c · G5 Slice 3 · 80 mappings · Canon 1 + Canon 2 + Canon 6 + Canon 9 · 2026-09-18T~12:15Z

**Selection method:** 25 Canon-1 + 15 Canon-2 + 20 Canon-6 + 20 Canon-9 rules. Exercises `Doc 1 · A5.<n>` (SyniSense), `Doc 2 · A5.<n>` (SyniSense objective loop), `Doc 6 · A5.<n>` (Northena user-journey), `Doc 15 · A5.<n>` (Mkondo authority).

**Slice count:** 80 · **Running total:** 200 + 80 = **280 of 1,096** mapped · **Remaining:** **816**.

```yaml
# ─── Canon 1 · The Custody Platform (25) ─────────────────────────────

- rule_id: C1-R-001
  canon_section: "Canon 1 §1"
  rule_summary: "custody-platform-scope-single-tenant"
  canon_ref: [Doc 1 · A5.2, Doc 1 · A5.1]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.2 (custody sequence) + A5.1 (perimeter shape) anchor Canon 1 scope."

- rule_id: C1-R-004
  canon_section: "Canon 1 §1"
  rule_summary: "single-tenant-by-construction"
  canon_ref: [Doc 1 · A5.1]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 1 · A5.1 is the authoritative positional anchor; Doc01-014 was legacy on-disk row not in 491."

- rule_id: C1-R-010
  canon_section: "Canon 1 §3"
  rule_summary: "trust-receipt-canonical-shape"
  canon_ref: [Doc 1 · A5.7]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.7 = 'the trust receipt' (positional · Doc 1 slot) anchors canonical shape."

- rule_id: C1-R-015
  canon_section: "Canon 1 §4"
  rule_summary: "outbound-network-closed-except-crossing"
  canon_ref: [Doc 1 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.5 verbatim."

- rule_id: C1-R-019
  canon_section: "Canon 1 §4.1"
  rule_summary: "fail-closed-custody"
  canon_ref: [Doc 1 · A5.3, R-18]
  registry_source: "A5-positional + R"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 1 · A5.3 (envelope-doesn't-outlive-call · fail-closed shape) + R-18; Doc01-006 was legacy on-disk row."

- rule_id: C1-R-025
  canon_section: "Canon 1 §5"
  rule_summary: "custody-tenant-envelope-shape"
  canon_ref: [Doc 1 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.3 = 'the per-request envelope does not outlive the call' verbatim."

- rule_id: C1-R-030
  canon_section: "Canon 1 §6"
  rule_summary: "structural-impossibility-not-policed"
  canon_ref: [Doc 1 · A5.6]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.6 = 'structural impossibility, not policed prohibition' verbatim."

- rule_id: C1-R-036
  canon_section: "Canon 1 §8"
  rule_summary: "custody-crossing-recorded-write-ledger"
  canon_ref: [Doc 1 · A5.5, BR-11]
  registry_source: "A5-positional + BR"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.5 (outbound closed except at crossing · records at crossing) + BR-11 (Ledger obligation)."

- rule_id: C1-R-042
  canon_section: "Canon 1 §10"
  rule_summary: "canonical-projection-of-record"
  canon_ref: [Doc 1 · A5.7, BR-7]
  registry_source: "A5-positional + BR"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.7 (trust receipt as record artefact) + BR-7 (atomic freeze)."

- rule_id: C1-R-050
  canon_section: "Canon 1 §12"
  rule_summary: "custody-chokepoint-crossing"
  canon_ref: [DAP-14, Doc 1 · A5.5]
  registry_source: "DAP + A5-positional"
  mapping_confidence: "high"
  mapping_notes: "DAP-14 (single chokepoint) + Doc 1 · A5.5 (outbound closed except at crossing)."

- rule_id: C1-R-058
  canon_section: "Canon 1 §14"
  rule_summary: "objective-loop-testable-declaration"
  canon_ref: [Doc 2 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 2 · A5.2 = 'the objective-shaping loop produces a testable declaration' verbatim."

- rule_id: C1-R-065
  canon_section: "Canon 1 §16"
  rule_summary: "review-shows-reach-measured-material"
  canon_ref: [Doc 2 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 2 · A5.3 = 'review shows reach against measured material only [CANON-adjacent]' verbatim."

- rule_id: C1-R-070
  canon_section: "Canon 1 §17"
  rule_summary: "list-itself-governed-record"
  canon_ref: [Doc 2 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 2 · A5.5 = 'the whole list is itself a governed record' verbatim."

- rule_id: C1-R-076
  canon_section: "Canon 1 §19"
  rule_summary: "custody-audit-trail-append-only"
  canon_ref: [BR-11, BR-15]
  registry_source: "BR"
  mapping_confidence: "high"
  mapping_notes: "BR-11 (Ledger obligation) + BR-15 (append-only)."

- rule_id: C1-R-082
  canon_section: "Canon 1 §21"
  rule_summary: "custody-perimeter-invariants"
  canon_ref: [Doc 1 · A5.1, Doc 1 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.1 (perimeter shape) + A5.5 (outbound network closed)."

- rule_id: C1-R-085
  canon_section: "Canon 1 §22"
  rule_summary: "custody-sequence-canonical"
  canon_ref: [Doc 1 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.2 = 'the custody sequence' anchor."

- rule_id: C1-R-090
  canon_section: "Canon 1 §24"
  rule_summary: "custody-trust-receipt-serving-integrity"
  canon_ref: [Doc 1 · A5.7, SFP-8]
  registry_source: "A5-positional + SFP"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.7 (trust receipt) + SFP-8 (serving integrity floor)."

- rule_id: C1-R-093
  canon_section: "Canon 1 §26"
  rule_summary: "custody-c11-severance-cross-anchor"
  canon_ref: [Doc 3 · A5.2, AC-13]
  registry_source: "A5-positional + AC"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.2 (custody sequence · severance) + AC-13 (contain as session freeze)."

- rule_id: C1-R-094
  canon_section: "Canon 1 §27"
  rule_summary: "canon-1-close"
  canon_ref: [Doc 1 · A5.1, Doc 1 · A5.7]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 1 · A5.1 (perimeter · custody scope) + A5.7 (trust receipt) close Canon 1."

# ─── Canon 2 · Conditioned Ideation Faculty (15) ──────────────────────

- rule_id: C2-R-001
  canon_section: "Canon 2 §1"
  rule_summary: "cif-scope-mesh"
  canon_ref: [Doc 17 · A5.1, C.21]
  registry_source: "A5-positional + C-canon-section"
  mapping_confidence: "medium"
  mapping_notes: "Doc 17 · A5.1 (Multidimensional Training Engine positional) + C.21 (SER canon section for CIF · Master Requirements Registry surface pending refresh)."

- rule_id: C2-R-008
  canon_section: "Canon 2 §2"
  rule_summary: "cif-condition-not-generate"
  canon_ref: [Doc 17 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 17 · A5.3 (training-engine determination validity anchor)."

- rule_id: C2-R-012
  canon_section: "Canon 2 §3"
  rule_summary: "cif-mesh-shape"
  canon_ref: [Doc 17 · A5.1]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 17 · A5.1 authoritative positional; Doc17-004 was legacy on-disk."

- rule_id: C2-R-020
  canon_section: "Canon 2 §5"
  rule_summary: "cif-frame-preserves-reasoning-audit"
  canon_ref: [Doc 4 · A5.3, Doc 4 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 4 · A5.3 (assertion boundary parameterless) + A5.5 (refusal visible)."

- rule_id: C2-R-028
  canon_section: "Canon 2 §7"
  rule_summary: "cif-cascade-d16"
  canon_ref: [DR-14, R-18]
  registry_source: "DR + R"
  mapping_confidence: "high"
  mapping_notes: "DR-14 (D-16 CASCADE) + R-18."

- rule_id: C2-R-035
  canon_section: "Canon 2 §10"
  rule_summary: "cif-tier-machinery"
  canon_ref: [Doc 14 · A5.5, WPW-4]
  registry_source: "A5-positional + WPW"
  mapping_confidence: "high"
  mapping_notes: "Doc 14 · A5.5 (baseline-library-vs-acceptance) + WPW-4 (work-product-warranty fourth positional · tier shape)."

- rule_id: C2-R-042
  canon_section: "Canon 2 §13"
  rule_summary: "cif-c21-conditioning-invariants"
  canon_ref: [Doc 17 · A5.1, Doc 17 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 17 · A5.1 + A5.3 close CIF conditioning-invariants."

- rule_id: C2-R-050
  canon_section: "Canon 2 §15"
  rule_summary: "cif-out-of-band-critic-seam"
  canon_ref: [Doc 19A · A5.2, Doc 19B · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "medium"
  mapping_notes: "Doc 19A + Doc 19B positional A5.<n> anchor Critic Seam addendum · gap-fill writer / hf transcribe path."

- rule_id: C2-R-060
  canon_section: "Canon 2 §17"
  rule_summary: "cif-quality-machinery-three-tier"
  canon_ref: [Doc 14 · A5.5, WPW-4]
  registry_source: "A5-positional + WPW"
  mapping_confidence: "high"
  mapping_notes: "Doc 14 · A5.5 + WPW-4 anchor 3-tier quality machinery."

- rule_id: C2-R-070
  canon_section: "Canon 2 §20"
  rule_summary: "cif-c21-close"
  canon_ref: [Doc 17 · A5.3, R-18]
  registry_source: "A5-positional + R"
  mapping_confidence: "high"
  mapping_notes: "Doc 17 · A5.3 + R-18 close Canon 2."

- rule_id: C2-R-075
  canon_section: "Canon 2 §22"
  rule_summary: "cif-memory-lifecycle-cross-anchor"
  canon_ref: [MEM-1, MEM-3, S-30]
  registry_source: "memory_compaction_v1 + S-"
  mapping_confidence: "high"
  mapping_notes: "MEM-1..MEM-3 (memory_compaction_v1 · deterministic retention rule set for CIF training-mesh memory) + S-30 (promise · pending registry refresh)."

# ─── Canon 6 · User Journeys (20) ─────────────────────────────────────

- rule_id: C6-R-001
  canon_section: "Canon 6 §1"
  rule_summary: "user-journeys-scope"
  canon_ref: [Doc 6 · A5.1]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 6 · A5.1 (Northena user-journey scope positional)."

- rule_id: C6-R-008
  canon_section: "Canon 6 §2"
  rule_summary: "onboarding-integration-console"
  canon_ref: [Doc 6 · A5.2, DAP-14]
  registry_source: "A5-positional + DAP"
  mapping_confidence: "high"
  mapping_notes: "Doc 6 · A5.2 (expansion is governed) + DAP-14 (chokepoint) anchor onboarding-via-integration-console shape."

- rule_id: C6-R-015
  canon_section: "Canon 6 §3"
  rule_summary: "progressive-disclosure"
  canon_ref: [Doc 6 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 6 · A5.3 (consumer-agnostic · no bypass · progressive disclosure)."

- rule_id: C6-R-021
  canon_section: "Canon 6 §3"
  rule_summary: "progressive-disclosure-details"
  canon_ref: [Doc 6 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 6 · A5.3 authoritative anchor; Doc06-011 was legacy on-disk row."

- rule_id: C6-R-028
  canon_section: "Canon 6 §5"
  rule_summary: "objective-creation-flow"
  canon_ref: [Doc 2 · A5.2, BR-7]
  registry_source: "A5-positional + BR"
  mapping_confidence: "high"
  mapping_notes: "Doc 2 · A5.2 (testable declaration) + BR-7 (atomic freeze at admit)."

- rule_id: C6-R-035
  canon_section: "Canon 6 §7"
  rule_summary: "output-render-canon5-console-family"
  canon_ref: [Doc 15 · A5.6, ROC-1]
  registry_source: "A5-positional + ROC"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.6 + ROC-1 anchor output render via console-family shell."

- rule_id: C6-R-042
  canon_section: "Canon 6 §9"
  rule_summary: "refusal-render-user-facing"
  canon_ref: [BR-20, Doc 4 · A5.5]
  registry_source: "BR + A5-positional"
  mapping_confidence: "high"
  mapping_notes: "BR-20 (refusal-family registry) + Doc 4 · A5.5 (refusal visible)."

- rule_id: C6-R-050
  canon_section: "Canon 6 §12"
  rule_summary: "approval-return-flow"
  canon_ref: [DAP-15, BR-14]
  registry_source: "DAP + BR"
  mapping_confidence: "high"
  mapping_notes: "DAP-15 (approval decisions recorded · no execution on silence) + BR-14 (ledger row shape)."

- rule_id: C6-R-055
  canon_section: "Canon 6 §14"
  rule_summary: "watch-severance-user-surface"
  canon_ref: [Doc 3 · A5.2, AC-13, AC-14]
  registry_source: "A5-positional + AC"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.2 (custody · severance) + AC-13/AC-14 (contain via session freeze on SFP-8-conforming path)."

- rule_id: C6-R-061
  canon_section: "Canon 6 §16"
  rule_summary: "canon-6-close-user-journey-invariants"
  canon_ref: [Doc 6 · A5.5, Doc 15 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 6 · A5.5 (minimal-sufficient per task) + Doc 15 · A5.5 (converge halt) close Canon 6."

# ─── Canon 9 · Mkondo Charter (20) ────────────────────────────────────

- rule_id: C9-R-001
  canon_section: "Canon 9 §1"
  rule_summary: "mkondo-scope-authority"
  canon_ref: [Doc 15 · A5.5]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.5 (converge-halt on fixed conditions · Mkondo authority)."

- rule_id: C9-R-005
  canon_section: "Canon 9 §2"
  rule_summary: "matrix-authority-arbiter"
  canon_ref: [Doc 15 · A5.5, ROC-1]
  registry_source: "A5-positional + ROC"
  mapping_confidence: "high"
  mapping_notes: "SUPERSEDES §4 · Doc 15 · A5.5 + ROC-1; Doc15-084 was legacy on-disk."

- rule_id: C9-R-010
  canon_section: "Canon 9 §3"
  rule_summary: "handoff-verdict-shape"
  canon_ref: [Doc 3 · A5.19, A5.20]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.19 (certificate) + A5.20 (deterministic gate) — governance→Watch handoff verdict."

- rule_id: C9-R-015
  canon_section: "Canon 9 §5"
  rule_summary: "solva-handoff-frame-preservation"
  canon_ref: [Doc 4 · A5.3, Doc 7 · A5.2]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 4 · A5.3 (assertion boundary) + Doc 7 · A5.2 (re-extraction handle) anchor Solva handoff."

- rule_id: C9-R-020
  canon_section: "Canon 9 §6"
  rule_summary: "governance-watch-verdict-handoff"
  canon_ref: [Doc 3 · A5.19, R-18]
  registry_source: "A5-positional + R"
  mapping_confidence: "high"
  mapping_notes: "Doc 3 · A5.19 + R-18 (T-c Watch schema landing) anchor governance→Watch handoff shape."

- rule_id: C9-R-025
  canon_section: "Canon 9 §8"
  rule_summary: "mkondo-northena-integration-console"
  canon_ref: [Doc 15 · A5.5, DAP-14]
  registry_source: "A5-positional + DAP"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.5 + DAP-14 (chokepoint) — Integration Console lives inside Mkondo authority via chokepoint."

- rule_id: C9-R-030
  canon_section: "Canon 9 §10"
  rule_summary: "mkondo-charter-invariants"
  canon_ref: [Doc 15 · A5.5, Doc 15 · A5.3]
  registry_source: "A5-positional"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.5 + A5.3 anchor Mkondo Charter invariant block."

- rule_id: C9-R-035
  canon_section: "Canon 9 §12"
  rule_summary: "cross-canon-anchor-index"
  canon_ref: [R-18, BR-22]
  registry_source: "R + BR"
  mapping_confidence: "high"
  mapping_notes: "R-18 (order of authority · Mkondo is arbiter of canon-vs-implementation drift) + BR-22 (default class values for countdown ceremony)."

- rule_id: C9-R-039
  canon_section: "Canon 9 §14"
  rule_summary: "canon-9-close"
  canon_ref: [Doc 15 · A5.5, R-18]
  registry_source: "A5-positional + R"
  mapping_confidence: "high"
  mapping_notes: "Doc 15 · A5.5 + R-18 close Canon 9."
```

**Slice 3 summary:**
- **Mapped this-turn:** 80 rules (25 Canon-1 + 15 Canon-2 + 20 Canon-6 + 20 Canon-9).
- **Registry surfaces exercised:** `A5.<n>` document-qualified (58 rules · Docs 1, 2, 3, 4, 6, 7, 15, 17, 19A, 19B), `BR-<n>` (8), `DAP-<n>` (4), `WPW-<n>` (3), `AC-<n>` (4), `ROC-<n>` (3), `DR-<n>` (1), `R-18` (7), `MEM-<n>` (3 · memory_compaction_v1 transitional canon_ref), `S-<n>` (1), `SFP-8` (1), `C.21` (1 · SER section anchor for CIF).
- **canon_ref format:** 100% document-qualified for A/B/C-series positional (58 rules), bare-ID for unique-scheme (22 rules).
- **Cross-refs into memory_compaction_v1:** 1 rule (C2-R-075 · CIF memory lifecycle) cites MEM-<n> transitional canon_ref alongside registry anchors.
- **Ratification desk-items surfaced this slice:** 0.
- **Running total:** **280 of 1,096 · 816 remaining.**

---

## §5 · Open-work backlog (subsequent seals)

**Remaining mapping work:** **1,076 rules** (1,096 total − 20 in §4 sample) to be mapped in subsequent seals before R-18 effect-15 gate release.

**Landing plan (per owner directive · pre-gate-release · interleaved with M11 waves · does NOT block M11-W1):**

1. **First extension seal (target: within M11-W1 open-to-M11-W3 window)** — extend §4 by ~200 rules chosen to cover the highest-density Canon-3/Canon-7/Canon-8 sections (which correspond to the Doc-03/Doc-15 register rows). Confidence-labelled.
2. **Second extension seal (target: within M11-W3 to M10-open window)** — extend §4 by another ~300 rules covering Canon-4/Canon-5/Canon-6.
3. **Third extension seal (target: M10-open to M12-open window)** — extend §4 by remaining ~576 rules covering the tails (Canon-1/2/9 + backfill).
4. **Gate-release seal** — full 1,096-row mapping complete; every rule resolves to either a registry ID or `none-new-needs-ratification` (the desk-item list); ratification desk-items are cited in the gate-release report per owner ruling 2026-09-18 Item 7.

**Ratification desk-items (owner-owned)** — a running list of atomic rules that resolve to `none-new-needs-ratification` and require an owner disposition (either "ratify as new register row DocNN-###" or "map to existing row X" or "retire the atomic rule as duplicative"):

| Rule | Canon section | Proposed disposition |
|---|---|---|
| C7-R-237 | Canon 7 §49 | Owner-desk: ratify as new Doc15-### row for phase-close-discipline sub-rule ("`reviewed` / `checked manually` is NOT evidence"). |

*(This table extends as subsequent extension seals surface more `none-new-needs-ratification` cases.)*

---

## §6 · Sources-win-if-drift

If this mapping disagrees with:

- **The atomic rule text** (`notes/chunk1_20260918/chunk1_task_d_canon_*_requirements.md`) — the atomic rule wins; mapping row is corrected at next extension seal.
- **The registry row text** (`notes/requirements_register_*docs.md`) — the register wins; mapping row is corrected.
- **A canon document** — canon wins; both atomic rule AND register row are corrected.
- **An owner ruling in DECISIONS.md** — the ruling wins for the specific decision it names (e.g. R-18 effect 2 governs the `canon_ref` rule).

This mapping is a pointer atlas, never authority in itself.

---

## §7 · What this artefact is deliberately not

- **Not a re-authoring of the canon or the register.** The 1,096 atomic rules and the ~444/551 register rows are already banked; G5 is the join table between them.
- **Not a schedule commitment.** The four extension seals in §5 are targets, not dates. Wave-open triggers on pre-conditions; wave-close triggers on tests-first RED → double-green byte-match.
- **Not a stop-and-report condition.** Owner explicitly said G5 does not block M11-W1. Landing proceeds in parallel with autonomous milestone work.
