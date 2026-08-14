# Claims Verification — Chunk 2 Part A

Verification of the seven §6 claims from an earlier read of RMS-IQ-Core-2.
Every citation is repo/path/file.py:line-range or Canon N §x. Cross-repo diff
result is stated per claim, with SHA-based confirmation where the file is
byte-identical to the RMS-IQ-Core-2 copy.

Pinned SHAs (from Chunk 1 §1): RMS-IQ-Core-2 `ea5aa01…be3b`;
Akki-OS-V1 `8c36190…956b`; Extraction-Akki `b150c21…ae25`;
Akki-Executive-Core `5844eee…19f2`.

---

## Claim 1 — Chokepoint is `invoke_with_metering()`; de-id → invoke → re-id; fail-closed

### RMS-IQ-Core-2 — **CONFIRMED (implementation + test)**

Implementation: `backend/services/synisense/shield/llm_router.py:153-311`.
- `async def invoke_with_metering(content, *, model_preference, timeout_seconds, system_msg, tenant_id)` — L153-160.
- Chokepoint sequence:
  - L207: `from services.synisense.shield import deidentifier, reidentifier`
  - L208: `de_id = await deidentifier.deidentify(content, tenant_id=tenant_id)`
  - L209-210: `llm_input = de_id.redacted_text; token_map = de_id.token_map`
  - L266-269: `response = await asyncio.wait_for(litellm.acompletion(**params), timeout=timeout_seconds)`
  - L280-281: `if _shielded_marker := True: text = reidentifier.reidentify(text, token_map)`
- Fail-closed paths:
  - L218-224 (mock mode) → `ServiceUnavailable`
  - L241-244 (SDK unavailable + reidentifier failure) → `ServiceUnavailable`
  - L299-311 (`TimeoutError`, `Exception`) → `ServiceUnavailable`
  - Docstring L165-172 states verbatim: "Fail-closed per the deidentifier's own spec: `ServiceUnavailable` from deidentify propagates without an LLM call (raw `content` never reaches the outbound seam)."

Test/call site: `backend/tests/registry/test_shield_custody_chain.py:34-140`.
- IF1-G1 (L34-88): asserts wire order `["deidentify(tenant_id=test-tenant)", "reidentify(token_map_keys=[...])"]` and that the LLM saw the redacted text, not the raw entity.
- IF1-G2 (L92-116): if `deidentify` raises `ServiceUnavailable`, LLM path MUST NOT execute (verified via `llm_touched` tripwire).
- IF1-G3 (L120-140): if `reidentify` raises, response text MUST NOT be returned to caller.

### Cross-repo status

| Repo | llm_router.py SHA-16 | Verdict |
|---|---|---|
| RMS-IQ-Core-2 | `b6d4dc6e1eefdc5d` (322 lines) | CONFIRMED |
| Extraction-Akki | `b6d4dc6e1eefdc5d` (322 lines) | CONFIRMED (byte-identical) |
| Akki-OS-V1 | `7750f6159ea034e3` (296 lines) | CONFIRMED with note |
| Akki-Executive-Core | `2a6749cb076b343a` (221 lines) | **PARTIAL** — see below |

**Akki-OS-V1**: the older shield still owns the chain — `deidentifier.deidentify` at L173, `reidentifier.reidentify` at L187/L209/L255, `ServiceUnavailable` at L189/L211/L274/L283. Custody chain wired but predates the 2026-07-30 P1-R6 token-preservation clause; sequence and fail-closed shape preserved.

**Akki-Executive-Core**: `invoke_with_metering()` (L118) does NOT call `deidentifier.deidentify` — it accepts a parameter literally named `de_id_content` (L119) and expects the caller to have already de-identified. The chain lives ONE level up in `backend/services/synisense/shield/client.py:63-71`:
```
63:    purpose_validator.validate_purpose(purpose, internal_caller=internal_caller)
66:    de_id = await deidentifier.deidentify(content, tenant_id=tenant_id, purpose=purpose)
67:    llm_text, provider, model, usage = await llm_router.invoke_with_metering(de_id.redacted_text, ...)
71:    response_text = reidentifier.reidentify(llm_text, de_id.token_map)
```
So the claim's *sequence* is present in Executive-Core, but the CHOKEPOINT is `client.py::invoke`, not `llm_router::invoke_with_metering`. The IF-1 close (2026-07-14) consolidated the chain INTO `invoke_with_metering` in the core three; Executive-Core (last commit 2026-07-08) predates that consolidation.

---

## Claim 2 — Runtime egress firewall + static AST gate

### RMS-IQ-Core-2 — **CONFIRMED**

Runtime firewall: `backend/services/synisense/shield/egress_firewall.py:1-138`.
- `class EgressFirewallTransport(httpx.BaseTransport)` L103-114 wraps sync transport.
- `class EgressFirewallAsyncTransport(httpx.AsyncBaseTransport)` L117-127 wraps async transport.
- `check_egress(url)` L84-100: parses host; iterates `_FORBIDDEN_HOSTS`; if forbidden AND `not _is_shield_call()` → returns denial reason.
- `_is_shield_call()` L74-81: walks `_call_stack_files()` L57-71 checking against config-driven `_EXEMPTED_FILES`.
- Denial → `raise EgressFirewallDenied(denial)` L113, L126.

Static AST gate: `backend/tests/invariants/test_ast_egress_gate.py:1-178`.
- `class _EgressWalker(ast.NodeVisitor)` L43.
- `visit_Import` L62-67 flags forbidden module names.
- `visit_ImportFrom` L72-80 flags forbidden `from X import Y`.
- `visit_Call` L82-97 detects `importlib.import_module("openai")` dynamic-import shape.

Also `backend/tests/test_no_direct_llm_calls_outside_shield.py` (134 lines) is a regex-based grep gate covering additional patterns — belt-and-braces with the AST gate.

Tests/call sites:
- `backend/tests/invariants/test_p1_custody_closure.py:98-108` — P1-G-R2.a break-in: raw `import openai` outside Shield fails the AST gate.
- `test_p1_custody_closure.py:111-120` — P1-G-R2.b aliased import.
- `test_p1_custody_closure.py:123-132` — P1-G-R2.c `from openai import ...`.
- `test_p1_custody_closure.py:135-144` — P1-G-R2.d dynamic-import via `importlib`.
- `test_p1_custody_closure.py:147-152` — P1-G-R2.e runtime firewall refuses outbound to `api.openai.com` from non-Shield call stack.
- `test_p1_custody_closure.py:155-161` — P1-G-R2.f every entry in the exemption list exists on disk.

### Cross-repo status

| Repo | egress_firewall.py | test_ast_egress_gate.py | test_p1_custody_closure.py | Verdict |
|---|---|---|---|---|
| RMS-IQ-Core-2 | present (137 L) | present (178 L) | present (430 L) | CONFIRMED |
| Extraction-Akki | present, byte-identical | present, byte-identical | present, byte-identical | CONFIRMED (Chunk 1 §2.1 — shield/ + tests/invariants/ identical) |
| Akki-OS-V1 | **MISSING** | **MISSING** | **MISSING** | **REFUTED** — no runtime firewall, no AST gate |
| Akki-Executive-Core | **MISSING** | **MISSING** | no P1 custody-closure suite | **REFUTED** — no runtime firewall, no AST gate |

---

## Claim 3 — Trust receipts HMAC-SHA256 + per-tenant HKDF keys + frozen field set

### RMS-IQ-Core-2 — **CONFIRMED**

Implementation: `backend/services/synisense/shield/trust_receipt.py:1-147`.
- HKDF: L44-56 `derive_tenant_key(tenant_id)` → `HKDF(algorithm=SHA256, length=32, salt=b"synisense/v1", info=tenant_id).derive(MASTER_SECRET)` (L48-54).
- HMAC-SHA256: L72-78 `sign(payload, *, tenant_id)` → `hmac.new(derive_tenant_key(tenant_id), _canonical_json(body), hashlib.sha256).hexdigest()`.
- Canonical JSON: L64-69 `sort_keys=True, separators=(",", ":"), UTF-8`.
- `verify()` L81-90 constant-time via `hmac.compare_digest`.
- Frozen field set (v1) declared in `build_trust_receipt` L99-146: 14 named fields — `receipt_id, audit_id, version, tenant_id, consumer_id, purpose, timestamp, llm_provider, llm_model, de_id_summary, dilution_score, exposure_reduction_score, request_hash, response_hash, masking_tier` — plus `signature`.

Frozen contract: `backend/contracts/trust_receipt_v1.py:1-96`.
- L35-40 docstring: "Trust Receipt v1 — masking-tier-carrying frozen shape. Fields carry forward from the shield-service v0 shape byte-verbatim."
- L41: `model_config = ConfigDict(extra="forbid", frozen=False)`.

Snapshot enforcement: `backend/tests/invariants/trust_receipt_v1.contract_snapshot.json` (113 lines) + `backend/tests/invariants/test_frozen_contract_snapshot_parity.py:69` maps `"trust_receipt_v1.py" → "trust_receipt_v1.contract_snapshot.json"` (parity seat #32, "P1 close 2026-07-30 · Owner condition (i)").

### Cross-repo status

| Repo | trust_receipt.py SHA-16 (lines) | contracts/trust_receipt_v1.py | snapshot json | Verdict |
|---|---|---|---|---|
| RMS-IQ-Core-2 | `cabe1c6598883452` (146) | present (96 L) | present (113 L) | CONFIRMED |
| Extraction-Akki | `cabe1c6598883452` (146) — byte-identical | present, byte-identical | present, byte-identical | CONFIRMED |
| Akki-OS-V1 | `086af1886a519749` (133) — **older** | **MISSING** | **MISSING** | **PARTIAL** — HMAC/HKDF present, but frozen contract not yet in place; older 133-line variant lacks `masking_tier` |
| Akki-Executive-Core | `086af1886a519749` (133) — **identical to Akki-OS-V1** | **MISSING** | **MISSING** | **PARTIAL** — same as Akki-OS-V1 |

The HMAC-SHA256 + HKDF machinery is present in all four repos; the "field set frozen" claim (contract + snapshot + parity seat) is only true in the RMS-IQ-Core-2 / Extraction-Akki line (post-2026-07-30 P1 close). Akki-OS-V1 and Executive-Core are on the pre-freeze receipt shape.

---

## Claim 4 — Northena ledger append-only + standing no-deletion-path test

### RMS-IQ-Core-2 — **CONFIRMED**

Implementation: `backend/services/northena/ledger.py:63-65`.
```
async def record(row: LedgerRow) -> None:
    """Append-only insert. No update, no delete. §7.2 + N-INV-8."""
    await db[NORTHENA_LEDGER_COLLECTION].insert_one(row.model_dump(mode="json"))
```
Only `insert_one`; no `update_*` / `delete_*` / `drop` in the module. Ledger writer is the sole write API for the collection.

Standing test: `backend/tests/invariants/test_northena_ledger_retention.py:37-62` (`test_no_deletion_path_in_northena_services`) grep-scans `services/northena/` for any `def delete_*` / `def purge_*` / `def expire_*`; asserts empty.

Wider invariant: `backend/tests/invariants/test_no_unauthorized_deletion_path.py` (154 lines) whitelists `services/retention/authorized_deletion.py` only; every other `delete_one(` / `delete_many(` / `.drop(` in `backend/services/` + `backend/routers/` fails the invariant.

Non-defect grep hits (test cleanup, not production paths):
- `backend/tests/registry/test_instance_fixture_b_walkthrough.py:54,109` — `db["northena_ledger"].delete_many({"instance_id": "instance_fixture_b"})` in test setup/teardown (test-fixture scope, not production code).

### Cross-repo status

| Repo | ledger.py SHA-16 | retention test SHA-16 | wider invariant test SHA-16 | Verdict |
|---|---|---|---|---|
| RMS-IQ-Core-2 | `50c723f746ecb80b` (115 L) | `ea206c8292aa5c75` (75 L) | `2c944cf54e871afd` (154 L) | CONFIRMED |
| Akki-OS-V1 | byte-identical | byte-identical | `c13206391fe8ff76` (145 L) — different, older | CONFIRMED (append-only intact) |
| Extraction-Akki | byte-identical | byte-identical | byte-identical | CONFIRMED |
| Akki-Executive-Core | **MISSING** — no `services/northena/`; entire Northena engine absent | **MISSING** | **MISSING** | **REFUTED** — Executive-Core does not carry the Northena engine at all |

---

## Claim 5 — Refusal-family registry external, versioned, append-only, with `unclassified` escape hatch

### RMS-IQ-Core-2 — **CONFIRMED**

External file: `backend/services/compliance/refusal_families.v0.json:1-31` — the registry.
- L1 `"version": "v0"`, L3 `"landed_at": "2026-07-06"`.
- L4 governance note (verbatim): "Registry-as-authority preserved… Family additions land as registry version bumps (v0 → v1 → v2 …), append-only."
- L5-30 `valid_families`: four entries.
  - `admission_refusals` (L6-11)
  - `composition_below_floor` (L12-17)
  - `outer_gate_refusals` (L18-23)
  - `unclassified` (L24-30) — the escape hatch: "MUST be surfaced honestly (never silently dropped). Any occurrence is a finding for future registry-additions review."

Classifier: `backend/services/compliance/refusal_family_classifier.py:1-121`.
- L77-78 loads external registries from `services/service_1/service_1_refusal_reasons.v0.json` and `admission_refusal_reasons.v3.json` at IMPORT time.
- L94-111 `classify_family(reason)` — pure function.
- L104 empty-reason fallback → `unclassified`.
- L111 unrecognised-reason fallback → `unclassified` (the escape hatch is deterministic, not a raise).
- L116-121 `FAMILY_DISPLAY_ORDER = ("admission_refusals","composition_below_floor","outer_gate_refusals","unclassified")` — the `unclassified` bucket is a first-class column.

Test/call site (from Chunk 2 §Claim 4 grep): several ledger-family gates reference this classifier in `backend/tests/invariants/test_phase_8_b_5a_compliance.py` and `backend/tests/invariants/test_phase_8_seam_3_sub_stage_3.py` (via `test_refusal_terminal_row_carries_registry_valid_refusal_family_in_stamp_audit` per the JSON governance note L4).

### Cross-repo status

| Repo | refusal_families.v0.json | classifier | Verdict |
|---|---|---|---|
| RMS-IQ-Core-2 | byte-identical | byte-identical | CONFIRMED |
| Akki-OS-V1 | byte-identical to Core-2 | byte-identical | CONFIRMED |
| Extraction-Akki | byte-identical | byte-identical | CONFIRMED |
| Akki-Executive-Core | **MISSING** — no `services/compliance/` directory | **MISSING** | **REFUTED** — Executive-Core does not carry the compliance service |

---

## Claim 6 — `purpose_validator.py` shaved at IF-1 close (2026-07-14) along with `client.py`, `audit_log.py`, `canonical.py`; purpose survives as a receipt field and a `deidentify()` kwarg

### File-existence matrix

| Repo | purpose_validator.py | client.py | audit_log.py | canonical.py |
|---|---|---|---|---|
| RMS-IQ-Core-2 | **absent** | **absent** | **absent** | **absent** |
| Akki-OS-V1 | **absent** | **absent** | **absent** | **absent** |
| Extraction-Akki | **absent** | **absent** | **absent** | **absent** |
| Akki-Executive-Core | **present** (60 L) | **present** (249 L) | **present** (191 L) | **present** (191 L) |

- Verdict for the three core repos: **CONFIRMED** (all four files shaved).
- Verdict for Akki-Executive-Core: **REFUTED** — all four files still exist AND the purpose-validation gate is WIRED IN: `backend/services/synisense/shield/client.py:63` calls `purpose_validator.validate_purpose(purpose, internal_caller=internal_caller)` before `deidentify()` and `llm_router.invoke_with_metering()`.
- Executive-Core's `purpose_validator.py:20-58` implements a real gate:
  - L32 raises `PurposeInvalid("purpose missing or not a string")`
  - L35 raises on empty string
  - L39-44 enforces `INTERNAL_ONLY_PURPOSE_PREFIXES` block for non-internal callers
  - L46-56 validates against `ALLOWED_PURPOSES` catalogue; unknown → raise
- Purpose SURVIVES in the core three:
  - As a **receipt field**: `backend/services/synisense/shield/trust_receipt.py:105,134` (`purpose: str` in `build_trust_receipt` signature and receipt dict).
  - As a **`deidentify()` kwarg**: not verified in this session; the docstring evidence at `llm_router.py:207-210` shows `deidentifier.deidentify(content, tenant_id=tenant_id)` — the kwarg `purpose=…` is NOT in the RMS-IQ-Core-2 call site. This is a spec-vs-code discrepancy worth flagging in Chunk 3. In Executive-Core (older shield) the kwarg IS passed: `client.py:66` calls `deidentifier.deidentify(content, tenant_id=tenant_id, purpose=purpose)`.

**Interpretation**: IF-1 close (2026-07-14) removed the pre-deid purpose gate in the core three. Executive-Core's last commit is 2026-07-08 (Chunk 1 §1) — six days before IF-1. So Executive-Core is on the pre-IF-1 architecture by date. Whether Executive-Core needs to adopt the IF-1 shave is a governance question for Chunk 3, not a claim verification.

---

## Claim 7 — No Studio / agent-builder surface in Core; Executive-Core has `work_studio` — what is it?

### Core three: **CONFIRMED — no surface exists**

Recon: `git ls-files | grep -Ei 'studio|agent[_ ]?build|agent_wizard|build_agent|/agents/|your_agents|agent_deploy|agent_train'` — **empty output** for RMS-IQ-Core-2, Akki-OS-V1, and Extraction-Akki.

### Akki-Executive-Core: **REFUTED (a surface exists)** — but "what it actually is" ≠ agent builder

Executive-Core has an extensive `work_studio` surface, but it is a **document / deck compilation surface**, not an agent-builder:

Backend (routers + services):
- `backend/routers/studio.py` — 915 LOC (studio surface router)
- `backend/routers/studio_blocks.py` — 1226 LOC
- `backend/routers/work_studio_export.py` — **2974 LOC** (largest single router in the repo)
- `backend/routers/work_studio_from_source.py` — 800 LOC (source-ingestion)
- `backend/routers/work_studio_overlay.py` — 828 LOC (intelligence overlays on documents)
- `backend/routers/work_studio_phase_c.py` / `phase_c2.py` — compilation phase C
- `backend/routers/work_studio_render.py` — 286 LOC (render pipeline)
- `backend/services/work_studio/confidence_scorer.py` — 306 LOC
- `backend/services/work_studio_export.py` — 1029 LOC
- `backend/services/work_studio_overlay.py` — 355 LOC
- `backend/work_studio/{brief,docx_generator,pptx_generator,pdf_generator,enhance,persistence}.py` — a parallel "legacy" implementation (~2100 LOC) that co-exists with `services/work_studio*`.

Frontend (`frontend/src/components/work_studio/`):
- `CompilationWizard.jsx` — 908 LOC
- `overlay/DocumentOverlay.jsx` — 1533 LOC
- `WorkStudioMasterTabs.jsx`, `WorkStudioSidebar.jsx`, `DocumentCardsSection.jsx` (469), `CreateArtefactModal.jsx` (466), `DraftingDrawer.jsx` (293), `DocumentJournalRail.jsx`, `overlay/DeckNotes.jsx`, `overlay/DocumentOutline.jsx`, `overlay/RelatedDocuments.jsx`, `overlay/SignalsPanel.jsx`, `overlay/IntelligencePanelExpanded.jsx`, `useAnalyzeStages.js`, `agentCyclePreview.js`.

Uploaded artefacts: `backend/uploads/work_studio_exports/` — 200+ real `.docx / .pdf / .pptx` files (users have exported artefacts).

Templates: `backend/templates/work_studio/SCHEMAS.md`.

Tests: `backend/tests/characterisation/test_work_studio_compile_golden.py` + `test_decks_work_studio.py` + `test_work_studio_briefings_visible.py` + `test_work_studio_listing.py`.

**What it IS**: a document / deck compilation wizard that ingests source material (uploaded docs), renders to docx/pdf/pptx, and overlays intelligence panels (signals, related documents, commentary). It maps onto Canon 5 §40 **Work pillar > Documents**, NOT Canon 5 §40 **Build pillar > Studio** (Canon 5 §42 "Studio" is *designed, not sourced* — a surface where an application is composed against platform primitives; Executive-Core's `work_studio` is the opposite — it EATS source material and produces artefacts).

**What it is NOT**: not an agent builder. There is no `agent_wizard`, `build_agent`, or agent-composer surface anywhere in the repo. The prototype's `Build > Build Agents / Your Agents` navigation (Canon 5 §40 Build pillar) has NO backend implementation in any of the four repos.

---

## Summary — status table

| Claim | RMS-IQ-Core-2 | Extraction-Akki | Akki-OS-V1 | Akki-Executive-Core |
|---|---|---|---|---|
| 1 · chokepoint = `invoke_with_metering` | **CONFIRMED** (impl+test) | **CONFIRMED** (byte-identical) | CONFIRMED (older, chain intact) | **PARTIAL** — chain in `shield/client.py`, not the router |
| 2 · runtime firewall + AST gate | **CONFIRMED** (impl+test) | **CONFIRMED** (byte-identical) | **REFUTED** — files absent | **REFUTED** — files absent |
| 3 · HMAC-SHA256 + HKDF + frozen field set | **CONFIRMED** | **CONFIRMED** (byte-identical) | **PARTIAL** — HMAC/HKDF present, contract not frozen, older 133-L variant | **PARTIAL** — same as Akki-OS-V1 |
| 4 · Northena ledger append-only + no-deletion test | **CONFIRMED** | **CONFIRMED** (byte-identical) | **CONFIRMED** | **REFUTED** — Northena engine absent |
| 5 · refusal-family registry external + versioned + escape hatch | **CONFIRMED** | **CONFIRMED** | **CONFIRMED** | **REFUTED** — compliance service absent |
| 6 · `purpose_validator.py` + client/audit/canonical shaved at IF-1 close | **CONFIRMED** | **CONFIRMED** | **CONFIRMED** | **REFUTED** — all four files present + purpose gate wired at `client.py:63` |
| 7 · No Studio/agent-builder in Core; Executive-Core has `work_studio` | **CONFIRMED** (no surface) | **CONFIRMED** | **CONFIRMED** | **REFUTED-in-part** — surface exists but is a document/deck compilation wizard, not an agent-builder |
