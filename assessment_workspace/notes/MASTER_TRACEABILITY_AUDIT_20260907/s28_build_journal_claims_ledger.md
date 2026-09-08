# S28 · BUILD_JOURNAL claims + close_reports + audits · Claims-to-Verify Ledger

**Binding rule:** per owner directive and STANDING_ORDERS §3, journals and close reports are **claims to verify against code**, not authoritative findings. This detail file catalogs the claims WITHOUT emitting findings from them; each entry becomes a follow-on verification task in the sprint roadmap.

## §A · BUILD_JOURNAL inventory

| Repo | Path | Lines | Character |
|---|---|--:|---|
| Extraction-Akki | `BUILD_JOURNAL.md` | **2,195** | Append-only build journal · every gate open/close · contract freeze/re-bless · Rule-2 flag · V-gate runs |
| Akki-OS-V1 | `BUILD_JOURNAL.md` | **1,792** | Same shape as Extraction-Akki |
| RMS-IQ-Core-2 | `BUILD_JOURNAL.md` | **2,195** | Byte-similar to Extraction-Akki (shared history from spine split) |
| Akki-Executive-Core | (none) | — | Executive workstream uses `docs/MEMO_DECISIONS.md` + `docs/BUILD_PHASES.md` instead |
| Akki-Executive-Final | (none) | — | Same as Core |

**Total BUILD_JOURNAL lines to verify: 6,182** across 3 repos.

## §B · close_reports inventory (per repo)

| Repo | Path | Count | Notes |
|---|---|--:|---|
| Extraction-Akki | `docs/close_reports/` | **44 files** | Titles include: `8_ext.md`, `9_2a.md`, `answer_fluency.md`, `artifact_store.md`, `census_dimensions.md`, `commercial_cut_2026_07_06.md`, `eab_1.md`, `fixture_refresh.md`, `g2_registry_maintenance.md`, `g3_operating_values_v1_1.md`, and 34 more |
| Akki-OS-V1 | `docs/close_reports/` | **44 files** | Overlaps with Extraction-Akki + adds `change_order_2026_07_25.md`, `critic_pass.md`, `eab_2.md` |
| RMS-IQ-Core-2 | `docs/close_reports/` | **44 files** | Same titles as Extraction-Akki (spine-shared history) |

**Total close_reports: 132 files** (with byte-identical duplicates across spine-linked repos; unique conceptual reports ≈ 44–47).

## §C · audits inventory (per repo)

| Repo | Path | Count | Notes |
|---|---|--:|---|
| Extraction-Akki | `docs/audits/` | **14 files** | Titles include: `deviation_audit_v1.md`, `enforcement_check_count_derivation_2026-07-30.md`, `engine_conformance_v1.md`, `g3_precondition/` subdir, `g3_solva_conformance_v1.md`, `g4_mtafiti_conformance_v1.md`, `g4_service_1_v1_conformance_v1.md`, `g4_targeta_conformance_v1.md`, `g5a_conformance_v1.md`, `g5b_conformance_v1.md`, and 4 more |
| Akki-OS-V1 | `docs/audits/` | **17 files** | Extraction-Akki set + `g6_conformance_v1.md` + additional Akki-OS specific |
| RMS-IQ-Core-2 | `docs/audits/` | **14 files** | Same as Extraction-Akki |

**Total audit files: 45** (with duplicates; unique conceptual audits ≈ 17–18).

## §D · Categorization by verification cost

| Category | Count | Verification approach |
|---|--:|---|
| **BUILD_JOURNAL entries** (append-only, dated, per-close attributes) | ~6,182 lines / ~500 close entries | Each entry claims a code state at a SHA. Verification: `git show <SHA> -- <path>` per claim. Prohibitive at full scale. **Approach:** verify only the last N wave-close entries against current HEAD; older entries retained as historical claims. |
| **close_reports/** | ~44 unique reports | Each report claims a wave outcome + LOC + green tests. Verification: cross-check against current test suite + ratchet_history. **Approach:** spot-check last 5 close reports against ratchet_history.json entries; older reports retained as historical claims. |
| **audits/ conformance reports** | ~17 unique conformance reports (g3/g4/g5a/g5b/g6/etc.) | Each claims engine conformance at a specific gate. Verification: re-run the conformance test suite. **Approach:** spot-check `engine_conformance_v1.md` + `g5b_conformance_v1.md` (most recent) against current invariants. |

## §E · Coverage-ledger note

Per master §F Δ10, this catalog is what the audit added; per binding rule, **NO findings emitted from these claims**. If the owner rules that BUILD_JOURNAL claims should be treated as authoritative (or partially so), the sprint roadmap grows a new item **W-VERIFY-BUILD-JOURNAL-CLAIMS** with L effort (spot-check last 20 close entries + all g-conformance audits).

## §F · S28 rollup

| Bucket | Rows | Notes |
|---|--:|---|
| Claims-to-verify (not classified) | ~700 (500 journal entries + 132 close reports + 45 audits + duplicates) | See §D for verification approach |
| DONE / PARTIAL / REUSE / NEW | 0 | Per binding rule, no findings emitted from journals |

**Wave charter:** **W-VERIFY-BUILD-JOURNAL-CLAIMS** (deferred; L effort) — spot-check the last 20 wave-close entries + all g-conformance audits against current HEAD `9f9b1fd`. Confirm ratchet_history.json entries match close_reports.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
