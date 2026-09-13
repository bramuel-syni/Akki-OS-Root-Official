READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_REGISTRY_EXTENSION_G3_close.md — wave close manifest

**Wave:** `W-REGISTRY-EXTENSION-G3` `[framing, not canon]` — owner ruling Option A (2026-09-13).
**Closes:** Doc-0 §STATUS AS OF row G-3 mechanical half (Mtafiti asset-inventory extension: `Component 4 BR-4.1 STATUS "Not Met"` → mechanism now landed).
**Prior-wave lineage untouched:** `W-REGISTRY-FULL-BUILD` (2026-09-09, CP1..CP9 closed at ratchet 3100, CP10 on owner HOLD with its close test shelved-untracked). Zero rename or edit of prior-wave code, tests, or state.
**Wave opened:** 2026-09-13 · ratchet floor 3503 (post-W1c).
**Wave closed:** 2026-09-13 · ratchet floor **3531** (+28 invariants).
**Output seal:** `phase0/output_verified_seals/registry_extension_g3.seal.txt` · `Kind: registry_extension_g3` · sha256 `0ba27118e7301aac02f2c71d96dcefc40d2b93b0b8225219c268b0a1af5954bc`.

---

## §A · CP roll-up (6 CPs · +28 invariants · 0 push)

| CP | Delta | Focus | Grounding test |
|--:|--:|---|---|
| CP-R1 | 5 | Extended asset-class schema: `AssetClass` (5 canon kinds: source·model·artifact·receipt·rule), `NamedOwner` (Doc-0 BA-3.1 owner_id+owner_class+mandate_source), `AssetRegistryRecord` reusing `FreshnessStamp` per Canon-1 §4.6 extension-not-sibling doctrine. `extra="forbid"` throughout. | `test_wregext_g3_cp_r1_asset_class_schema.py` |
| CP-R2 | 4 | Typed queryable `CustodyClass` (4-value enum, DPO-1 declared), refuses free-text at validation, `find_by_custody_class(custody_class: CustodyClass)` typed. R-C1 marker `R_C1_RULES_SERVICE_NOT_BUILT_FALLBACK_TRUE=True` asserted; silent flip forbidden by test. | `test_wregext_g3_cp_r2_typed_custody_class.py` |
| CP-R3 | 4 | Doc-0 TA-3.1 finite-named-class-list surface: `list_registered_classes()` returns dict of 4 immutable tuples (principals · assets · operations · custody_classes) with strict enum parity checks and non-empty invariant. | `test_wregext_g3_cp_r3_class_enumeration.py` |
| CP-R4 | 4 | Canon-3 §22 four-class governance-value taxonomy: `GovernanceValueClass` enum + `classify_governance_value(name)`. Unknown value refused (KeyError) not defaulted. Each wave-added function classified. | `test_wregext_g3_cp_r4_governance_taxonomy.py` |
| CP-R5 | 5 | Canon-7 §35-40 F&P Registry 11-field row: `FunctionPromiseRow` schema + `notes/function_promise_registry.jsonl` seed (4 rows for wave functions). Redundancy + Orphans standing queries wired. Gaps deferred (DPO-3). | `test_wregext_g3_cp_r5_fp_registry.py` |
| CP-R6 | 5 | Canon-9 §3 single-writer + Canon-3 §9.3 append-only: `write_asset_record()` idempotent (sha256-content receipt_id), no update/delete paths, negative-scan across `services/` for second-writer defect. `WriteReceipt.au_3b_defensible=False` (R-C2 marker) asserted invariant. | `test_wregext_g3_cp_r6_ledger_visibility.py` |
| Snapshot parity | 1 | `asset_registry.py` added to `CONTRACT_TO_SNAPSHOT` (headline `AssetRegistryRecord`) + `function_promise_row.contract_snapshot.json` added to `CONTRACT_TO_SNAPSHOT_SECONDARIES`. Bijection + parity tests pick up +1 invariant on next run. | `test_frozen_contract_snapshot_parity.py` |

## §B · What was built

Two mechanism files (new), one seed file (new), one snapshot-parity edit (existing test file), and six grounding-test files (new).

**Code (Commit A, `programme/track-a`):**
- `backend/contracts/asset_registry.py` (new · 155 lines) — headline `AssetRegistryRecord` + secondary `FunctionPromiseRow` + supporting models (`NamedOwner`, enums) + `ASSET_REGISTRY_COLLECTION` constant + `R_C1_RULES_SERVICE_NOT_BUILT_FALLBACK_TRUE` marker.
- `backend/services/mtafiti/asset_registry_writer.py` (new · ~150 lines) — canonical `write_asset_record()` + `WriteReceipt` (R-C2 carrier) + `find_by_custody_class()` + `list_registered_classes()` + `classify_governance_value()` + `_GOVERNANCE_TAXONOMY` map.
- `backend/tests/invariants/test_wregext_g3_cp_r1_asset_class_schema.py` (new)
- `backend/tests/invariants/test_wregext_g3_cp_r2_typed_custody_class.py` (new)
- `backend/tests/invariants/test_wregext_g3_cp_r3_class_enumeration.py` (new)
- `backend/tests/invariants/test_wregext_g3_cp_r4_governance_taxonomy.py` (new)
- `backend/tests/invariants/test_wregext_g3_cp_r5_fp_registry.py` (new)
- `backend/tests/invariants/test_wregext_g3_cp_r6_ledger_visibility.py` (new)
- `backend/tests/invariants/test_frozen_contract_snapshot_parity.py` (edited · +2 lines: headline + secondary registration).
- `backend/tests/invariants/asset_registry_record.contract_snapshot.json` (new · 3964 bytes).
- `backend/tests/invariants/function_promise_row.contract_snapshot.json` (new · 2167 bytes).
- `backend/tests/invariants/baseline_failures.json` (edited: `passed_floor` 3503→3531; `counts_at_baseline.passed` 3503→3531; `ratchet_history` +1 entry).

**State (Commit B, `master`):**
- `notes/W_REGISTRY_EXTENSION_G3_grounding_brief.md` (new · wave open).
- `notes/W_REGISTRY_EXTENSION_G3_close.md` (this file).
- `notes/function_promise_registry.jsonl` (new · 4 rows).
- `notes/PHASE_C_SYSTEMATIC_BUILD_PLAN.md` (edited · rename to new label).
- `notes/SYSTEM_OBJECTIVES_AND_PROMISES_CHARTER.md` (edited · one annotation).
- `notes/PRECHECK_BASTION_20260913.md` (edited · three references).
- `phase0/drill_receipts/20260913T102054Z_wregext_g3_RED_pre_impl.log` (RED banked).
- `phase0/drill_receipts/20260913T102544Z_wregext_g3_GREEN1.log` (GREEN #1).
- `phase0/drill_receipts/20260913T102820Z_wregext_g3_GREEN2.log` (GREEN #2).
- `phase0/output_verified_seals/registry_extension_g3.seal.txt` (output_verified_seal per SO §3.1).

## §C · Honest limits (declared, SO §3 no-silence)

- **DPO-1 · CustodyClass enum values.** `{open, sensitive, controlled, forbidden}` was chosen consistent with Canon-3 §22.1 "sensitivity classification Mtafiti assigns during census, specified in Document 4". Document 4's exact enum was not opened first-hand in this wave; owner may rule a different N-value set at any subsequent CP boundary — migration is a schema swap at that point.
- **DPO-3 · F&P Gaps standing query deferred.** Redundancy and Orphans run; Gaps requires a whole-journey Canon-6 catalog which is out of thin-kernel scope. Deferred to a subsequent wave.
- **R-C1 · Rules Service unbuilt** — carried on `contracts.asset_registry.R_C1_RULES_SERVICE_NOT_BUILT_FALLBACK_TRUE=True`. Meaning: controlled-unit determination this wave uses custody class alone (DAP-Spec §8 dependency verbatim). Silent flip forbidden by CP-R2 invariant `test_wregext_g3_cp_r2_r_c1_marker_present_and_true`.
- **R-C2 · Reliable time source unbuilt** — carried on `WriteReceipt.au_3b_defensible=False`. Meaning: timestamps in this wave's ledger writes are not defensible under AU-3(b) until Doc-0 G-8 (`Security_Promise_Set_Amendments.docx Amendment 3`) closes. Silent flip forbidden by CP-R6 invariant `test_wregext_g3_cp_r6_r_c2_marker_false_at_wave_open`.
- **In-memory registry.** `_REGISTRY: Dict[str, AssetRegistryRecord]` in `services/mtafiti/asset_registry_writer.py` is a thin-kernel append-only map; downstream persistence is a later wave's concern. This does not affect the invariants asserted here (idempotency, append-only, single writer, typed custody class, etc.) — they hold at the language and receipt layer.

## §D · Ratchet trace (this wave)

- Wave opened at floor **3503** (post-W1c).
- Mechanical RED at 27 right-reason failures (ModuleNotFoundError + missing-file), banked `20260913T102054Z_wregext_g3_RED_pre_impl.log`.
- GREEN #1: **3531 passed, 1 skipped, 438 warnings in 110.90s** · BASELINE_GUARD receipt `status: OK · subset · quarantine · ratchet all pass`.
- GREEN #2: **3531 passed, 1 skipped, 438 warnings in 111.12s** · BASELINE_GUARD receipt `status: OK`.
- Byte-match on pass count: TRUE (3531 · 3531).
- Ratchet bumped 3503 → **3531** (+28) in `backend/tests/invariants/baseline_failures.json`.

## §E · Discipline held

- **BASELINE_GUARD=1** tests-first: RED banked before mechanism.
- **Double-green byte-match** at close.
- **`output_verified_seal Kind: registry_extension_g3`** written; not `registry_full_build` (owner label discipline).
- **Zero track-a churn to prior-wave code**: `services/w_registry_full_build/*`, `pod_shell/backend/server.py`, prior invariant suite (`test_w_registry_full_build_*`), prior state artefacts (`notes/W_REGISTRY_FULL_BUILD_*`, `STATE/HOLISTIC_PLAN.md`, `STATE/DECISIONS.md`, `STATE/NEXT.md`) all untouched.
- **Two-commit pattern**: Commit A (code, `programme/track-a`) + Commit B (state, `master`). NEVER push.
- **testing_agent BANNED** — verification terminal pytest only.
- **No egress. No Radio traffic.** T4 / timezone / host-key verification still held for owner ruling; no probe fired.

## §F · What this wave does NOT open

- **CP10 of prior W-REGISTRY-FULL-BUILD** — still on owner HOLD.
- **W-SOLVA-V2-LIFT** — sequenced next per standing owner ruling 2026-09-06T~19:20Z + this session's Phase C plan §D.
- **W-DAP-STACK** — sequenced behind Solva; carries R-C1 and R-C2 the moment it opens.
- **W-JOURNEY-ASSISTANT** — candidate wave surfaced by the journey audit, NOT ruled in by owner. Not folded.
- **Doc-0 G-3 general triad formalisation half** — documentary, not mechanical. Deferred.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
