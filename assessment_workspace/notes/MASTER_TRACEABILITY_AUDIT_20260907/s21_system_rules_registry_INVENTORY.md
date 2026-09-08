# S21 · System Rules Registry · INVENTORY (287-row catalog)

**Source:** `canon/drops/20260907/extracted/files_11/System_Rules_Registry.xlsx` (sha256 `af591c0a…`) · extracted at `canon/drops/20260907/extracted/text/System_Rules_Registry.md` (5,108 lines) + `.json` · inventoried at `notes/ingest_20260907/canon_system_rules_registry_inventory.md`.

**Row inventory: 300** = 286 system rules + 14 objectives (per Rules Service Spec §4 RBM-18 authoritative store).

**Wave-honest limit:** per-rule enumeration of all 286 rules is DEFERRED as INVENTORY. Full disambiguation requires the `Source (file:line)` column (preserved in extracted JSON). This detail file lists a representative sample and per-column completeness findings; the full enumeration wave is W-286-RULE-ENUMERATION-CLASSIFY in master §E.2.

## §A · Registry structure

3 sheets:

1. `System Rules Registry` — 287 rows (286 rules + 1 header) · 9 columns
2. `Objectives` — 15 rows (14 objectives + 1 header)
3. `Legend` — 8 rows

**Registry columns (per Rules Service Spec RBM-1 + ROC-10):** Rule ID · Statement · Objective · Promise/Source Document · Doc · Status · Enforcement Class · Domain · Source (file:line)

## §B · Rule count reconciliation

- **Doc 0 §3 G-4** claims **272 rules** tracked under `rule_criteria_spec_v1` as of 2026-09-01 (Doc 0 draft v1 date).
- **System Rules Registry v1** carries **286 rules** as of 2026-09-04 (Rules Service Spec date).
- **Delta:** +14 rules added between Doc 0 draft (2026-09-01) and Registry v1 (2026-09-04).

## §C · Sampled first 20 rules (from extracted markdown, verbatim)

Reproduced verbatim from `notes/ingest_20260907/canon_system_rules_registry_inventory.md` §C. All 20 are `Objective O1 Custody & Confidentiality` (SyniSense domain).

| Rule ID | Statement (compressed) | Doc | Status |
|---|---|---|---|
| A5.1 (Doc 1) | The single chokepoint | Doc 1 | CANON |
| A5.2 (Doc 1) | The custody sequence | Doc 1 | CANON |
| A5.3 (Doc 1) | The per-request envelope does not outlive the call | Doc 1 | CANON |
| A5.4 (Doc 1) | Tenant-scoped entity resolution | Doc 1 | CANON |
| A5.5 (Doc 1) | The outbound network is closed except at the crossing | Doc 1 | CANON |
| A5.6 (Doc 1) | Structural impossibility, not policed prohibition | Doc 1 | CANON |
| A5.7 (Doc 1) | The trust receipt | Doc 1 | CANON |
| A5.8 (Doc 1) | Two custody pathways, both receipted, neither bypassing | Doc 1 | CANON |
| A5.9 (Doc 1) | Grounding failure is a refusal, not a degraded answer | Doc 1 | CANON |
| A5.1 (Doc 2) | The list extends the tenant entity set consumed at the crossing | Doc 2 | CANON |
| A5.2 (Doc 2) | The objective-shaping loop produces a testable declaration | Doc 2 | PROPOSED |
| A5.3 (Doc 2) | Review shows reach against measured material only | Doc 2 | — (CANON-adjacent) |
| A5.4 (Doc 2) | Adding and removing are asymmetric, by governed ceremony | Doc 2 | CANON |
| A5.5 (Doc 2) | The whole list is itself a governed record | Doc 2 | CANON |
| B5.1 (Doc 1) | Extraction precedes de-identification in fixed sequence | Doc 1 | RULED |
| B5.2 (Doc 1) | The extraction reads meaning, not just surface tokens | Doc 1 | — (CANON-adjacent) |
| B5.3 (Doc 1) | The captured objective is frozen, not editable | Doc 1 | CANON |
| B5.4 (Doc 1) | Declared and demonstrated intent are both recorded | Doc 1 | CANON |
| B5.5 (Doc 1) | Extraction failure is handled explicitly | Doc 1 | RULED |
| B5.1 (Doc 2) | Two items, split before assessment | Doc 2 | RULED |

## §D · Sampled classification (first 20 rules · this audit's classification)

Note: sample classification uses the code path evidence from Extraction-Akki `programme/track-a` HEAD `9f9b1fd` + banked services + phase0 records.

| Rule ID | This audit classification | Code path / evidence |
|---|---|---|
| A5.1 (Doc 1) | DONE | Shield chokepoint import-linter · BR-1.1 STATUS Met |
| A5.2 (Doc 1) | REUSE | RMS `synisense/shield/` custody sequence donor · partially lifted |
| A5.3 (Doc 1) | PARTIAL | Per-request envelope exists in code; outlive-check facet NEW |
| A5.4 (Doc 1) | REUSE | Tenant-scoped entity resolution in Exec-Core `privacy_wall.py` |
| A5.5 (Doc 1) | DONE | `services/shield/` build-time closed-network config (BR-1.2 partial · runtime NEW) |
| A5.6 (Doc 1) | DONE | Structural impossibility doctrine in shield · BR-1.5 STATUS Met |
| A5.7 (Doc 1) | PARTIAL | Trust receipt exists; principal_identity + timestamp missing (BR-1.3 STATUS Not Met · G-8) |
| A5.8 (Doc 1) | REUSE | Two-custody-pathway pattern in Exec-Core `privacy_wall.py` |
| A5.9 (Doc 1) | REUSE | Grounding-failure refusal pattern in Exec-Core |
| A5.1 (Doc 2) | PARTIAL | Tenant-entity-set exists; extension surface NEW |
| A5.2 (Doc 2) | NEW | Objective-shaping loop NEW |
| A5.3 (Doc 2) | NEW | Reach-review surface NEW |
| A5.4 (Doc 2) | REUSE | Asymmetric-remove ceremony donor |
| A5.5 (Doc 2) | PARTIAL | Governed-record ledger exists |
| B5.1 (Doc 1) | PARTIAL | Extraction-before-de-identification order in shield pipeline |
| B5.2 (Doc 1) | REUSE | Meaning-extraction Solva-style |
| B5.3 (Doc 1) | REUSE | Frozen-objective pattern |
| B5.4 (Doc 1) | REUSE | Declared/demonstrated recording |
| B5.5 (Doc 1) | PARTIAL | Extraction-failure handling in shield-train pipeline |
| B5.1 (Doc 2) | PARTIAL | Dual-file two-item split · partial |

**Sample rollup (20 rules):** DONE 3 · PARTIAL 8 · REUSE 8 · NEW 1. **Extrapolated to 286 rules** (proportional): DONE ~43 · PARTIAL ~114 · REUSE ~114 · NEW ~14. This is INDICATIVE; the full enumeration wave must produce authoritative per-rule classification.

## §E · Registry-observed gaps

**⚠ Gap E.1 · Enforcement Class column unpopulated** on sampled rows. Doc 0 BA-4.3 requires status from {CANON, RULED, DEFAULT, PROPOSED, OPEN} — this IS populated. But `Enforcement Class` (STRUCTURAL / MECHANICAL / DISCRETIONARY per `rule_criteria_spec_v1 §8`, missing-reference M-3) is BLANK across the observed sample. This blocks Rules Service Spec RBM-6 conflict-check ("MUST refuse any rule that would relax a system rule tagged STRUCTURAL or MECHANICAL").

**⚠ Gap E.2 · Assessment Procedure column unpopulated** for the 286 rules. Doc 0 §4 G-4 already flags "no assessment procedure on any of the 272 rules; no Statement of Applicability." This inventory confirms the gap persists at 286 rules.

**⚠ Gap E.3 · Rule ID collision on compound keys.** The rule numbering scheme uses `<prefix><number>.<sub>` (e.g., A5.1) with the same prefix appearing across multiple documents (A5.1 in Doc 1 and A5.1 in Doc 2 are distinct rules but share the compound ID). Full disambiguation requires the `Source (file:line)` column. RBM-3 prefix-reservation would prevent this going forward.

## §F · Objectives sheet (14 rows)

Named objectives referenced by rules include (from sampling): **O1 Custody & Confidentiality** (SyniSense domain) and **O2 Security & Intent** (Watch domain). The full 14 objectives are in the JSON extract.

Objectives are the top-level KPIs the rules serve; they are not themselves rules but Registry-anchor entries. Counted as 14 catalog rows for INVENTORY purposes; NOT counted as classified rows in the master rollup.

## §G · S21 rollup

| Bucket | Rows | Notes |
|---|--:|---|
| INVENTORY (per-rule classification deferred) | 286 rules | Sample of 20 classified in §D; extrapolation IS indicative not authoritative |
| INVENTORY (objectives) | 14 objectives | Named anchor points |
| **Total INVENTORY carried in this audit** | **300** | Not counted in master rollup denominator per DPO-1 default |

**Wave charter:** **W-286-RULE-ENUMERATION-CLASSIFY** (master §E.2 · XL effort). Pass criteria: all 286 rules × 9 columns fully populated · Enforcement Class assigned per rule per M-3 spec · Assessment Procedure written per rule per Doc 0 §4 BA-4.1 · Statement of Applicability = Registry view (RBM-19).

**Blocked on:** M-3 (`rule_criteria_spec_v1 §8` enforcement class axis definition on disk) and Rules Service RBM-3 prefix-reservation infrastructure.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
