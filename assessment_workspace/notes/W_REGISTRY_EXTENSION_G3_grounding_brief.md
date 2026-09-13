READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_REGISTRY_EXTENSION_G3_grounding_brief.md — wave open

**Wave label:** `W-REGISTRY-EXTENSION-G3` `[framing, not canon]` — owner ruling 2026-09-13 (Option A: rename this cycle to avoid namespace collision with the prior `W-REGISTRY-FULL-BUILD` wave of 2026-09-09, which sits CP1..CP9 closed at ratchet 3098 and CP10 on owner HOLD; nothing in this wave touches that lineage).

**Wave opens:** 2026-09-13 · ratchet floor **3503** (post-W1c, banked).

**Canon closure claim:** Doc-0 §STATUS AS OF row `G-3 | dap_backend_spec_v1 DAP-1/DAP-2 (external-party case only) | Partial — general triad formalisation and Mtafiti's full asset-inventory extension remain open` — this wave closes the **Mtafiti asset-inventory extension** half; the "general triad formalisation" half remains a documentary wave, out of scope here.

**Owner directive** (verbatim, this session): "Open the wave with the banked Phase C §W-REGISTRY scope — CP-R1..CP-R6 ... schema extension on top of the existing `contracts/mtafiti_registry.py` shape ... models/artifacts/receipts/rules with named owner; typed queryable custody class; class enumeration; four-class governance-value taxonomy per Canon-3 §22/§22.1 ABAC over Mtafiti sensitivity; F&P Registry rent per Canon-7 §35-40; ledger-scoped visibility."

---

## §A · Canon anchors (first-hand, this session)

- **Doc-0 Attribute 3 §BA-3.1**: "Every principal belongs to a stated class — human role, application, or subsystem acting under its own authority — and carries a mandate whose source can be named."
- **Doc-0 Attribute 3 §TA-3.1**: "A finite, named list of principal classes, asset classes, and operations exists and can be produced on request."
- **Doc-0 Component 4 BR-4.1 STATUS**: "Not Met — current coverage is estate sources only (Promises #12, #13). See G-3."
- **Canon-3 §22 (Four Classes)** verbatim: "Every governed value in the platform is exactly one of these classes, and moves between them by change of nature, not by opinion." — Rails · Rules · Engine settings · Registries.
- **Canon-3 §22.1 (Entitlement rules as ABAC)** verbatim: "The content side is already built: the sensitivity classification Mtafiti assigns during census, specified in Document 4, is exactly the resource attribute this match runs against. No new classification exists; entitlement reads the one already there."
- **Canon-7 §35-40 (Function & Promise Registry)**: every named function registers with 11 fields; three standing queries (Redundancy / Orphans / Gaps) run on every registry change. §37 verbatim: "No gate without a promise. No promise without a service trace. No journey step without enforcement. New functions register before they land."
- **Canon-9 §3 (Record matrix)** verbatim: "A second writer to any class is a defect on sight; a reader not listed does not read." Mtafiti is the single writer for Census and registry records.

## §B · CP-R1..CP-R6 · thin-kernel design

Each CP lands with grounding tests **before/with** the mechanism (STANDING_ORDERS §3 tests-first).

| CP | Focus | Mechanism sites | Grounding invariants |
|--:|---|---|--:|
| CP-R1 | Extended asset-class schema on top of existing `MtafitiRegistryRecord` (Mandate §13 shape untouched). New: `AssetClass` enum (source·model·artifact·receipt·rule), `NamedOwner`, `AssetRegistryRecord`. | `contracts/asset_registry.py` | 5 |
| CP-R2 | Typed, queryable `custody_class` field per `Doc-0 BR-1.4`. Enum-bounded, `extra=forbid`, refuses free-text. R-C1 marker declared explicitly. | in `contracts/asset_registry.py` (same file) | 4 |
| CP-R3 | Class enumeration surface (Doc-0 TA-3.1) — finite named list of principal classes, asset classes, operations, custody classes; producible on request. | `services/mtafiti/asset_registry_writer.py::list_registered_classes()` | 4 |
| CP-R4 | Four-class governance-value taxonomy binding (Canon-3 §22): `GovernanceValueClass` enum + `classify_governance_value()` returning exactly one class per named value; unknown value refused. | `services/mtafiti/asset_registry_writer.py::classify_governance_value()` | 4 |
| CP-R5 | Function & Promise Registry population (Canon-7 §35-40): 11-field `FunctionPromiseRow` schema + jsonl seed for the functions this wave introduces + standing queries (Redundancy, Orphans). Gaps standing query deferred (needs whole-journey enumeration, out of thin-kernel scope; deferred to a subsequent wave with a canon-6-driven catalog). | `contracts/asset_registry.py` (FunctionPromiseRow) + `notes/function_promise_registry.jsonl` | 5 |
| CP-R6 | Ledger-scoped visibility (Canon-9 §3): asset registry writes go through Mtafiti's canonical `write_asset_record()`; negative-scan test asserts no second writer imports the collection name. R-C2 marker declared explicitly on the writer's return receipt. | `services/mtafiti/asset_registry_writer.py::write_asset_record()` | 5 |
| Snapshot parity | `AssetRegistryRecord` and `FunctionPromiseRow` schemas snapshotted; parity registered in `CONTRACT_TO_SNAPSHOT`. | `tests/invariants/*.contract_snapshot.json` (2 new files) | 2 |

**Target invariants added: ~29.** Ratchet target 3503 → ~3532.

## §C · R-C1 and R-C2 carriage (named constraints, not silently absorbed)

- **R-C1 · Rules Service unbuilt** — carried on `AssetRegistryRecord.custody_class` as a class-level marker `R_C1_RULES_SERVICE_NOT_BUILT_FALLBACK_TRUE = True`. Meaning: controlled-unit determination in this wave uses custody class alone (DAP-Spec §8 dependency table verbatim: "Until the Rules Service is built, controlled status is determined by custody class alone."). This marker is invariant-asserted so it cannot be silently flipped without a test.
- **R-C2 · Reliable time source unbuilt** — carried on the writer's return receipt `WriteReceipt.au_3b_defensible: bool = False`. Meaning: timestamps in this wave's ledger writes are not defensible under AU-3(b) until Doc-0 G-8 (`Security_Promise_Set_Amendments.docx Amendment 3`) closes. Invariant-asserted; cannot be silently flipped.

## §D · Out of scope for this wave (explicit)

- **`W-JOURNEY-ASSISTANT`** — the candidate wave surfaced in `notes/JOURNEY_AND_ASSISTANT_AUDIT_20260913.md` §5. NOT ruled in by owner. NOT folded here.
- **G-3's general triad formalisation half** — documentary, not mechanical. Deferred.
- **Gaps standing query on Function & Promise Registry** — requires a whole-journey Canon-6 catalog. Deferred; only Redundancy + Orphans run in CP-R5.
- **Radio-side network egress** — T4 held pending owner timezone ruling. No traffic in this wave.
- **Rewriting `MtafitiRegistryRecord`** — the existing shape is untouched. Extension is by *addition* of `AssetRegistryRecord`.

## §E · Wave-honest limits (declared before close, STANDING_ORDERS §3)

- **DPO-1 · Custody class enum values.** The `CustodyClass` enum in CP-R2 uses the four-value set `{open, sensitive, controlled, forbidden}` — a common-sense classification the plan reads as *DPA-sensitivity-shaped* consistent with Canon-3 §22.1 ("sensitivity classification Mtafiti assigns during census"). Canon-4 (Document 4) specifies the exact sensitivity taxonomy Mtafiti writes; Document 4's precise enum was not opened first-hand in this session's grounding pass. Owner may rule a different four-value or N-value set at any subsequent CP boundary; migration is a schema swap at that point.
- **DPO-2 · F&P schema completeness.** The 11-field row shape is derived from Canon-7 §35-40's stated fields (function_id, governor, mandate, promise, service_trace, surface, enforcement, cost, dependencies, ladder_rung, owner). If Canon-7 elsewhere adds a twelfth field, migration required at next CP boundary.
- **DPO-3 · Standing-query Gaps deferred.** Redundancy and Orphans run; Gaps deferred until Canon-6 journey catalog is enumerated.
- **R-C1 carriage** as declared in §C above (custody-class-only fallback).
- **R-C2 carriage** as declared in §C above (AU-3(b) non-defensibility).

## §F · Discipline standing

- **BASELINE_GUARD=1 tests-first.** RED banked at `phase0/drill_receipts/YYYYMMDDTHHMMSSZ_wregext_g3_RED_pre_impl.log` before any mechanism lands.
- **Double-green byte-match** at close: `cd backend && BASELINE_GUARD=1 python -m pytest tests/invariants/` twice consecutively.
- **`output_verified_seal`** at close: `Kind: registry_extension_g3` (new label; not `registry_full_build`).
- **Two-commit pattern**: Commit A (code) on `programme/track-a`; Commit B (state) on `master`. NEVER push.
- **testing_agent BANNED.**
- **No egress. No Radio traffic.**

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
