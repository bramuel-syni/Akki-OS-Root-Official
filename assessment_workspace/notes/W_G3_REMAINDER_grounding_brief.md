READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_G3_REMAINDER_grounding_brief.md — wave-open grounding brief

**Wave.** `W-G3-REMAINDER` — Mtafiti-side asset-inventory generalisation (Doc-0 G-3 full-closure remainder).
**Framing.** `[framing, not canon]` — per session block-plan Task 3.
**Owner authorisation.** Verbatim 2026-09-13: G-A ratified sequence "2E → 2F → 2G → 2H → CP10 → G-3 remainder, exactly as stated."
**Predecessor.** `W-REGISTRY-EXTENSION-G3` (2026-09-13 · commit `33edf56` · ratchet 3531) closed the *mechanical half* — Mtafiti asset-inventory extension at schema + single-writer + typed-custody-class + class-enumeration grade. THIS wave closes the *generalisation half* remainder: making the asset inventory a first-class, complete surface across ALL 5 `AssetClass` kinds, per BR-4.1 verbatim target.
**Deferred (documentary half).** Doc-0 G-3 general triad formalisation remains documentary and out of this wave.

---

## §A · Canon anchors bound by this wave

- **Doc-0 §STATUS AS OF row G-3** verbatim: *"dap_backend_spec_v1 DAP-1/DAP-2 (external-party case only) | Partial — general triad formalisation and Mtafiti's full asset-inventory extension remain open."*  ← this wave attacks the *"Mtafiti's full asset-inventory extension"* clause.
- **Doc-0 Component 4 BR-4.1 STATUS** verbatim: *"Not Met — current coverage is estate sources only (Promises #12, #13).  See G-3."*  ← this wave lifts BR-4.1 STATUS from "estate sources only" to "all 5 AssetClass kinds discoverable through one surface."
- **Doc-0 Attribute 3 §TA-3.1** verbatim: *"A finite, named list of principal classes, asset classes, and operations exists and can be produced on request."*  ← already asserted at kernel grade by `list_registered_classes()`; this wave adds *"and every record of every asset class is retrievable through it."*
- **Canon-9 §3 (record matrix)** verbatim: *"A second writer to any class is a defect on sight; a reader not listed does not read."*  ← this wave asserts the single-writer invariant STILL HOLDS on the generalised query surface (no new writer path, only new reader paths).
- **Canon-1 §4.6 (extension not sibling)** — new query surface composes OVER `services.mtafiti.asset_registry_writer` without modifying it; no new registry, no sibling.

## §B · Predecessor-wave discipline preserved (`W-REGISTRY-EXTENSION-G3` §E)

The G-3 mechanical half's close manifest recorded verbatim: *"Zero track-a churn to prior-wave code."*  This wave PRESERVES that discipline by:
- NOT modifying `backend/services/mtafiti/asset_registry_writer.py` (predecessor mechanism).
- NOT modifying `backend/contracts/asset_registry.py` (predecessor schema).
- ADDING a NEW module `backend/services/mtafiti/asset_inventory.py` that COMPOSES over the predecessor by importing its symbols.

## §C · Invariants planned (this wave)

| Row | Anchor | What it will assert |
|---|---|---|
| GS-01 · module fabric | Canon-1 §4.6 | `services.mtafiti.asset_inventory` importable with `list_all_assets`, `count_by_class`, `enumerate_classes_always_five`, `cross_class_governance_query`, `single_writer_still_holds` |
| GS-02 · BR-4.1 · all 5 classes covered | Doc-0 BR-4.1 | One record per each of the 5 `AssetClass` kinds → `count_by_class()` returns all 5 keys with correct counts; NO class is missing |
| GS-03 · BR-4.1 · no asset hidden | Doc-0 BR-4.1 | Every written record retrievable via `list_all_assets()`; no filter-by-default; every `receipt_id` returned matches the corresponding writer receipt |
| GS-04 · TA-3.1 · enum stable at zero | Doc-0 TA-3.1 | With an EMPTY inventory, `enumerate_classes_always_five()` still returns all 5 asset-class names — a finite, named list is producible even with 0 records |
| GS-05 · BR-4.1 · cross-class governance query | Doc-0 BR-4.1 + Canon-3 §22.1 | `cross_class_governance_query(custody_class, asset_class, owner_class)` composes the three filters correctly; each individual filter is honored |
| GS-06 · Canon-9 §3 · single writer preserved | Canon-9 §3 verbatim | The generalised surface exposes readers only; a negative-scan `single_writer_still_holds()` returns True (no `write_*`/`append_*`/`update_*` names on the inventory module's public surface) |

## §D · What this wave will NOT do

- Will NOT open a second writer to any class.
- Will NOT modify the predecessor `asset_registry_writer.py` or its contracts.
- Will NOT lift the R-C1 or R-C2 markers (still flip-forbidden).
- Will NOT resolve Doc-0 G-3 general-triad-formalisation documentary half — that stays deferred.
- Will NOT extend BR-4.1 STATUS past "generalised across the 5 AssetClass kinds already in schema"; if BR-4.1 needs more classes later, that is a separate wave.

## §E · Ratchet + discipline

- Ratchet floor at wave open: **3627** (post-CP10).
- Expected +6 invariants → floor **3633** on close.
- BASELINE_GUARD=1 tests-first; mechanical RED, then GREEN1, GREEN2, Rider 1 (pip freeze + collect-only), seal, close.md, two-commit local pattern.
- `testing_agent` BANNED. Local commit only, NEVER pushed.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
