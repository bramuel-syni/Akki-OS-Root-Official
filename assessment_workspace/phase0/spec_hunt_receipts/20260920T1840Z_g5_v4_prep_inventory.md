# G5-v4 prep · read-only inventory of Master Requirements Registry v4

**Timestamp**: 2026-09-20T~18:40Z
**Scope**: Read-only structural inventory of `custody/owner_drops/20260920T1600Z/Master_Requirements_Registry_v4.xlsx` compared to `custody/owner_drops/20260920T1300Z/Master_Requirements_Registry_v3.xlsx`.
**NON-authority**: v3 remains the ratified authority per prior seals (R-81 CP-ENTITLEMENT-WAVE-SETUP anchor). v4 ratification is HELD by owner. This receipt records the structural delta ONLY; it does not treat v4 as ratified.
**Trigger**: Owner directive verbatim this-session — "If autopilot has clean non-held work (e.g., G5 prep that doesn't commit against v4, or open M13+ card items), proceed per SO §6".

## File-level facts (byte-verified)

### v3 · Master_Requirements_Registry_v3.xlsx (custody `owner_drops/20260920T1300Z/`)

- `file_size`: **78732 bytes**
- `sha256`: `79d4456224392ac6e936739ca80e8ba39d782b8d6af9d7bc2245d2a798c94a51` — matches R-81 seal narrative anchor (`79d44562...` cited at CP-ENTITLEMENT-WAVE-SETUP Commit-A `fc8b5c0` seal message verbatim).
- `sheet_count`: 4
- Sheets (data rows only):
    - `Build Status`: 44 rows × 4 cols
    - `System Rules Registry`: 564 rows × 11 cols (header row + 564 data rows)
    - `Objectives`: 14 rows × 3 cols
    - `Legend`: 7 rows × 2 cols
- TOTAL: 629 data rows across 4 sheets

### v4 · Master_Requirements_Registry_v4.xlsx (custody `owner_drops/20260920T1600Z/`)

- `file_size`: **83411 bytes**
- `sha256`: `72160287dcc4bddc5b921ab391d020bfda0f19e48dbffd122b70f45b6fead588`
- `sheet_count`: 4 (identical to v3)
- Sheets (data rows only):
    - `Build Status`: 44 rows × 4 cols — **unchanged from v3**
    - `System Rules Registry`: 595 rows × 11 cols — **+31 rows from v3**
    - `Objectives`: 14 rows × 3 cols — **unchanged from v3**
    - `Legend`: 7 rows × 2 cols — **unchanged from v3**
- TOTAL: 660 data rows (delta +31)

## v3 → v4 delta (structural · pure-additive)

| Aspect | v3 | v4 | Delta |
|---|---|---|---|
| Sheet count | 4 | 4 | 0 |
| System Rules Registry unique rule IDs | 433 | 464 | **+31** |
| System Rules Registry data rows | 564 | 595 | +31 |
| Net-new rules | — | 31 | **+31** |
| Removed rules | — | 0 | 0 |
| Edited rules (id-shared but statement changed) | — | 0 | **0** |
| Build Status data rows | 44 | 44 | 0 |
| Objectives data rows | 14 | 14 | 0 |
| Legend data rows | 7 | 7 | 0 |

**Delta shape**: **pure-additive** — every v3 rule ID persists in v4 with byte-identical statement text; v4 adds 31 new rows without editing or removing any prior rule. This is the structural shape that permits ratification-as-additive-superset (owner ruling still required for authority transfer).

## The 31 net-new v4 rules (byte-verified · full enumeration)

All 31 net-new rules share the prefix `CON-` (Content Registry doctrine). Zero net-new rules outside this prefix.

| Rule ID | v4 row | Statement (first ~80 chars · byte-verbatim) |
|---|---|---|
| CON-1 | 566 | Every string that reaches a surface belongs to exactly one content entry and exa... |
| CON-2 | 567 | Fixed entries render their text verbatim. The text is a contract; changing it is... |
| CON-3 | 568 | Templated entries render only from named dependencies that resolve to verified f... |
| CON-4 | 569 | Every Templated entry carries an honest-gap variant for each dependency that may... |
| CON-5 | 570 | Generated entries carry a class ceiling of inference or advisory and never fact... |
| CON-6 | 571 | A number on any surface comes from a Templated dependency or a Fixed string. A G... |
| CON-7 | 572 | Which surfaces may carry Generated entries at all is a ruled list (R-32). A surf... |
| CON-8 | 573 | A content entry carries: entry identifier; surface; class; objective — one sente... |
| CON-9 | 574 | A slot entry carries: slot identifier; surface; ordered candidate list; ranking ... |
| CON-10 | 575 | The registry is read-only to every component except the ceremony engine. Templat... |
| CON-11 | 576 | An objective is mandatory on every entry. An entry whose objective cannot be sta... |
| CON-12 | 577 | Rendering is a pure function of (entry, entry version, dependency values). For F... |
| CON-13 | 578 | A learned component MAY propose a new template, a new candidate, or a re-orderin... |
| CON-14 | 579 | The resolver fails closed. A missing dependency renders the honest-gap variant; ... |
| CON-15 | 580 | Every candidate on a slot is assigned one salience class at render time, by the ... |
| CON-16 | 581 | The hook is the eligible candidate with the lowest salience class. Ties resolve ... |
| CON-17 | 582 | An ineligible candidate — any dependency null — is never the hook while an eligi... |
| CON-18 | 583 | No engagement measure — views, dwell, clicks, replies — and no learned signal en... |
| CON-19 | 584 | A hook holds until a candidate of a lower class becomes eligible or the hook's o... |
| CON-20 | 585 | Choosing a hook writes a content receipt carrying the salience trace: every cand... |
| CON-21 | 586 | A hook is advisory. It directs attention; it never gates an action, and a compon... |
| CON-22 | 587 | A chat answer, a recommendation body, or a notification body is a Generated entr... |
| CON-23 | 588 | A displayed Generated string is stored as an artefact by hash with: class, ancho... |
| CON-24 | 589 | A Generated string that would state a fact the anchors do not support is refused... |
| CON-25 | 590 | A Templated string is not stored as text. Its content receipt records template v... |
| CON-26 | 591 | A Generated string is stored per CON-23. A Fixed string is stored once, as the c... |
| CON-27 | 592 | Erasure reaches Generated artefacts. When a unit's rights are withdrawn, every G... |
| CON-28 | 593 | Retention of Generated artefacts follows a ruled default (R-35) and is subject t... |
| CON-29 | 594 | A Templated entry re-renders when any dependency changes. Dependency changes are... |
| CON-30 | 595 | A schedule exists only for an entry with a dependency that emits no event. The s... |
| CON-31 | 596 | If a trigger source is unreachable, the last rendered string displays with a vis... |

## Cross-check against prior sprint-order narrative

- **CP-CONTENT-REGISTRY-INGEST-DROP** `6d910bbe` ingested the Content Registry doctrine bundle at 2026-09-20T~16:00Z alongside journey v2 in the same drop `20260920T1600Z`. This receipt confirms that ingestion produced 31 CON-* rules landing in v4's registry.
- **STILL HELD (owner "do not open")** at R-83/R-84/R-85 seals: "R-32 generated-surfaces list + Content Registry wave open · G5 against 595-row v4 ratification". This receipt corroborates the 595-row figure (v4 `System Rules Registry`) and confirms the delta is 31 CON-* rules exactly.
- **R-32 anchor**: CON-7 references `R-32` verbatim ("Which surfaces may carry Generated entries at all is a ruled list (R-32)"). CON-28 references `R-35` verbatim ("Retention of Generated artefacts follows a ruled default (R-35)..."). Both R-numbered rules would be net-new in the paired Rules section of v4 — but the `System Rules Registry` sheet holds the CON-* content and the R-N ruling-register is elsewhere (Objectives or a paired v4 doc); this prep does not trace R-32/R-35 to their source registers.
- **CON-18 grep-negative anchor**: "No engagement measure — views, dwell, clicks, replies — and no learned signal enters the hook resolver" — this is a structural-impossibility candidate for a G5-v4 invariant (grep-negative on hook resolver imports of engagement-measure identifiers).

## Prep-only disposition (per owner "does not commit against v4")

This receipt records the structural v3→v4 delta as a factual inventory. It does NOT:
- Ratify v4 as authority (owner ratification still HELD).
- Extract CON-* rule statements into an atomic-rules markdown (that is the G5-v4 wave's Commit-A work · not prep).
- Author any invariant test against v4 (that is the G5-v4 wave's Commit-A work · not prep).
- Edit any sealed module or test file.

Once owner ratifies v4 as authority, the G5-v4 wave's Commit-A can proceed with:
1. Extract atomic-rule markdown at `notes/master_requirements_registry_v4_atomic_rules.md` from CON-1..31 (byte-verbatim statement extraction · SO §2.5 discipline).
2. Author paired grep-negative invariants + property tests for each CON-N per SO §3.10-α closed-schema pattern.
3. Bump baseline ratchet by +31 (one test per CON-N as MVP · or +N-per-testable-invariant if some CON-N need multiple grep-negatives).
4. Ratchet 5640 → 5671 (or higher · TBD).

## Canon anchors

- `custody/owner_drops/20260920T1300Z/Master_Requirements_Registry_v3.xlsx` (v3 · ratified authority · sha256 `79d44562...`).
- `custody/owner_drops/20260920T1600Z/Master_Requirements_Registry_v4.xlsx` (v4 · ratification HELD · sha256 `72160287...`).
- CP-CONTENT-REGISTRY-INGEST-DROP seal `6d910bbe` (v4 + journey v2 ingestion boundary).
- CP-ENTITLEMENT-WAVE-SETUP seal `fc8b5c0/c3cc7451/16c9d912` (v3 anchor at prior wave).
- Owner directive this-session verbatim ("G5 prep that doesn't commit against v4").
- SO §6.2 objective-card discipline (G5-v4 objective card would be authored at wave open · pre-authorised drafting per SO §6.2).
- SO §6.4 NOTHING-BEYOND (this receipt is prep-only · nothing beyond structural inventory).
- SO §3.8 additive-only (v3→v4 delta shape is pure-additive · compatible with additive-only landing on v4 ratification).

## Standing bounds preserved

zero push · terminal `pytest` only · no `testing_agent` · additive-only §3.8 · three-repo discipline · ratchet monotonic-up (unchanged at 5640 · this receipt does not edit `baseline_failures.json`).
