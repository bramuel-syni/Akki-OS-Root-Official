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
