# System Rules Registry · Inventory

**Source:** `canon/drops/20260907/extracted/files_11/System_Rules_Registry.xlsx` (sha256 `af591c0a…`)  
**Extracted:** `canon/drops/20260907/extracted/text/System_Rules_Registry.md`

## §A · Structure

3 sheets:
1. `System Rules Registry` — 287 rows (**286 rules + 1 header**), max_col=9
2. `Objectives` — 15 rows (**14 objectives + 1 header**)
3. `Legend` — 8 rows

**Registry columns:** Rule ID · Statement · Objective · Promise/Source Document · Doc · Status · Enforcement Class · Domain · Source (file:line)

## §B · Rule count reconciliation

- Doc 0 §3 G-4 claims **272 rules** tracked under rule_criteria_spec_v1 (as of 2026-09-01, Doc 0 draft v1).
- System Rules Registry v1 carries **286 rules** as of 2026-09-04 (Rules Service Spec date).
- Delta: **+14 rules** added between Doc 0 draft (2026-09-01) and Registry v1 (2026-09-04).

## §C · Sample first 20 rules (from extracted markdown, verbatim)

| Rule ID | Statement | Objective | Doc | Status | Domain |
|---|---|---|---|---|---|
| A5.1 | The single chokepoint | O1 Custody & Confidentiality | Doc 1 | CANON | SyniSense |
| A5.2 | The custody sequence | O1 Custody & Confidentiality | Doc 1 | CANON | SyniSense |
| A5.3 | The per-request envelope does not outlive the call | O1 Custody & Confidentiality | Doc 1 | CANON | SyniSense |
| A5.4 | Tenant-scoped entity resolution | O1 Custody & Confidentiality | Doc 1 | CANON | SyniSense |
| A5.5 | The outbound network is closed except at the crossing | O1 Custody & Confidentiality | Doc 1 | CANON | SyniSense |
| A5.6 | Structural impossibility, not policed prohibition | O1 Custody & Confidentiality | Doc 1 | CANON | SyniSense |
| A5.7 | The trust receipt | O1 Custody & Confidentiality | Doc 1 | CANON | SyniSense |
| A5.8 | Two custody pathways, both receipted, neither bypassing the other | O1 Custody & Confidentiality | Doc 1 | CANON | SyniSense |
| A5.9 | Grounding failure is a refusal, not a degraded answer | O1 Custody & Confidentiality | Doc 1 | CANON | SyniSense |
| A5.1 (Doc 2) | The list extends the tenant entity set consumed at the crossing | O1 Custody & Confidentiality | Doc 2 | CANON | SyniSense |
| A5.2 (Doc 2) | The objective-shaping loop produces a testable declaration | O1 Custody & Confidentiality | Doc 2 | PROPOSED | SyniSense |
| A5.3 (Doc 2) | Review shows reach against measured material only | O1 Custody & Confidentiality | Doc 2 | — (CANON-adjacent) | SyniSense |
| A5.4 (Doc 2) | Adding and removing are asymmetric, by governed ceremony | O1 Custody & Confidentiality | Doc 2 | CANON | SyniSense |
| A5.5 (Doc 2) | The whole list is itself a governed record | O1 Custody & Confidentiality | Doc 2 | CANON | SyniSense |
| B5.1 (Doc 1) | Extraction precedes de-identification in the fixed sequence | O1 Custody & Confidentiality | Doc 1 | RULED | SyniSense |
| B5.2 (Doc 1) | The extraction reads meaning, not just surface tokens | O1 Custody & Confidentiality | Doc 1 | — (CANON-adjacent) | SyniSense |
| B5.3 (Doc 1) | The captured objective is frozen, not editable | O1 Custody & Confidentiality | Doc 1 | CANON | SyniSense |
| B5.4 (Doc 1) | Declared and demonstrated intent are both recorded | O1 Custody & Confidentiality | Doc 1 | CANON | SyniSense |
| B5.5 (Doc 1) | Extraction failure is handled explicitly | O1 Custody & Confidentiality | Doc 1 | RULED | SyniSense |
| B5.1 (Doc 2) | Two items, split before assessment | O1 Custody & Confidentiality | Doc 2 | RULED | SyniSense |
| B5.2 (Doc 2) | Independent assessment, no cross-consultation | O1 Custody & Confidentiality | Doc 2 | RULED | SyniSense |
| B5.3 (Doc 2) | Re-association is a defined, guarded seam | O1 Custody & Confidentiality | Doc 2 | — (PROPOSED, per Doc 16 §7 discipline) | SyniSense |
| B5.4 (Doc 2) | The two files | O1 Custody & Confidentiality | Doc 2 | — | SyniSense |

## §D · Objectives sheet inventory

Sheet 2 `Objectives` has 15 rows (14 objectives + header). Structure preserved in `text/System_Rules_Registry.json`.

Named objectives referenced in Registry rules include (from sampling): **O1 Custody & Confidentiality · O2 Security & Intent** (others enumerated in full via the JSON extract).

## §E · Wave-honest limit

**Per-rule enumeration of all 286 rules is deferred.** The rule numbering scheme uses `<prefix><number>.<sub>` (e.g., A5.1, B5.1, etc.) with the same prefix appearing across multiple documents (e.g., A5.1 in Doc 1 and A5.1 in Doc 2 are distinct rules but share the compound ID). Full disambiguation requires the `Source (file:line)` column, which is preserved in the extract.

Structural inventory sufficient for this ingest wave:
- **286 system rules** total
- Statuses observed in sample: CANON · PROPOSED · RULED · — (CANON-adjacent or PROPOSED-per-discipline)
- Enforcement Class column exists but is UNPOPULATED in the sample (all blank) — this is itself a finding, since Doc 0 BA-4.3 requires a status from {CANON, RULED, DEFAULT, PROPOSED, OPEN} and Rules Service Spec RBM-4 requires a tier declared at authoring; Enforcement Class per rule_criteria_spec_v1 Axis 2 is distinct from the status field and its blankness across the observed sample suggests the Enforcement Class classification (per §8 STRUCTURAL / MECHANICAL / DISCRETIONARY) has not been populated yet for the loaded rules.

## §F · Gap surfaced by this inventory

**⚠ Registry-observed gap:** the `Enforcement Class` column is present but empty in the sampled rows. Doc 0 G-4 already flags "no assessment procedure on any of the 272 rules; no Statement of Applicability." This inventory extends that finding to: **enforcement class (structural/mechanical/discretionary per rule_criteria_spec_v1 §8) is also not populated** on the observed rules — which means RBM-6's conflict check ("MUST refuse any rule that would relax a system rule tagged STRUCTURAL or MECHANICAL") cannot fire against these rows until the classification is added. This is a Rules Service prerequisite, tracked in `GAPS_TO_WAVES.md`.
