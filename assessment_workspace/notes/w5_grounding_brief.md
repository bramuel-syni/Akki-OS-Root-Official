# W5 · Solva · Shrinkage · Memory + LLM crossing LIVE — grounding brief

**Owner Order 2026-08-25 · "W5 go" with LLM rulings** (verbatim in `STATE/DECISIONS.md`).
**Owner ruling 2026-08-25 · plan confirmation with four sharpenings** (metering fields · connection-scoped egress allowlist · `.json` custody · CP3 honesty + model provenance).
**Owner correction 2026-08-25 · canon vocabulary is Solva — not "Solver"** (backend package · purpose IDs · receipt kinds · surface copy all say Solva).
Scope class **L (≤2500 LOC)**.

## 1. Register rows targeted by W5

**Total: 93 rows** across Doc 04 (41) + Doc 06 (16) + Doc 07 (19) + Doc 08 (17) + CA1-002/003/010 (already merged into their docs).

### Doc 04 · Reasoning · Solva · 41 rows
- **Doc04-001** ← C4-003 · Evidence gate refuses claims beyond source (Promise #8) · **REUSABLE → target: DONE-lite (deterministic gate + shield-fallback path in place; full evidence-grounding requires source layer W6+)**.
- **Doc04-014** ← C4-029 · Structured refusal (Evidence · Coverage · Contradiction) — v7 refusal card copy VERBATIM · **PARTIAL → target: DONE**.
- **Doc04-041 · CA1-010** · Session-scoped lowered standard with logged expiry · **BUILD → target: PARTIAL** (stub the config surface; enforce logged expiry on the receipt).
- Frame audit + situation class + candidate generation + triangulation + tension + probability weighting + synthesis + refusal — the 7 Solva reasoning modules from Executive-Final donor (~30 REUSABLE rows).

### Doc 06 · Progressive Disclosure · 16 rows
- **Doc06-001** ← C4-042 · Minimal-sufficient context per step (Promise #17) · **REUSABLE → target: PARTIAL** (context selection remains ThinkLab-scoped; the "audit line" is CA1-002).
- **Doc06-016 · CA1-002** · Audit line names how many available source units were served · **BUILD → target: DONE-lite** (rendered on the reasoning receipt).

### Doc 07 · Shrinkage · 19 rows
- **Doc07-001** ← C2-020 · Five-ring normalised unit (Promise #19) · **REUSABLE → target: DEFERRED** (five-ring perception layer needs its own wave; W5 declares the boundary).
- **Doc07-019 · CA1-003** · Densification stat + per-turn warm/fresh tag · **BUILD → target: PARTIAL** (warm/fresh tag renders on gate rows; densification stat = honest gap).

### Doc 08 · Memory & Retrieval · 17 rows
- **Doc08-001** ← C2-032 · Model reads distilled memory, not raw DB (Promise #20) · **REUSABLE → target: DEFERRED** (memory layer isolated to W6+ under Cost Ledger + retention discipline).
- **Doc08-006** ← C2-036 · Targeted fresh-fetch for what memory doesn't hold (Promise #21) · **REUSABLE → target: DEFERRED**.

**Realistic W5 close row-count**: ~15 rows to DONE-lite / PARTIAL; the remaining ~78 deferred to W6+ with honest gaps named.

## 2. Real crossings landing this wave

Adds **third real outbound path** to the estate:
- **(x3) Emergent LLM** — HTTPS out via `emergentintegrations.llm.chat.LlmChat` to `api.emergent.host` (universal provider fan-out). Region: `platform-managed`. Verb: `stream_message` (default). Every invoke transits `services.chokepoint.llm.invoke()`. Registered as connected LLM in registry_facts. **Egress allowlist gains `api.emergent.host` at W5 open — this is a real connection.**

Existing paths continue under W3 discipline:
- (x1) RDS Data API HTTPS via boto3 (eu-west-1) · structure_only tier.
- (x2) Compute-seam SSH via paramiko (region_not_on_record) · attested_command tier.

**Provider hosts stay OFF the allowlist until connected** (owner ruling · plan confirmation §3): `api.anthropic.com`, `api.openai.com`, `generativelanguage.googleapis.com` are refused as crossing endpoints until a key of that provider has been pasted, verified via the chokepoint, and its `data_connection_records/llm_<provider>_*.json` record is on disk.

## 3. Six mechanisms in W5 scope

### (a) LLM chokepoint (`services.chokepoint.llm`)
- Single `invoke(*, purpose, prompt, masking_tier, tenant_id, actor, model, provider, ...)` function.
- SOLE importer of `emergentintegrations` (or any provider SDK).
- Extends W3's `register_crossing()` to write per-call receipts with **metering** (owner sharpening §1): `payload_shape` carries `model_id` · `provider` · `tokens_in` · `tokens_out` · `latency_ms` (wall-clock at boundary, NOT provider-reported). Absent metering → refuse the receipt write.
- Failure modes: `PurposeInvalid` (422 refusal), `MaskingTierRefused`, `LLMShieldFailure` (upstream provider error — surface renders refusal, does NOT canned-response).
- **Reuse**: **ADAPT** `Akki-Executive-Final/backend/services/synisense/shield/purpose_validator.py` (60 LOC donor) → `services/chokepoint/llm_purpose_gate.py`; **BUILD** the invoke wrapper itself using the Emergent integrations playbook shape.

### (b) Emergent Universal LLM registration
- `services.registry_facts` extends `_llms()` to enumerate the emergent-universal connection when `EMERGENT_LLM_KEY` is present.
- Provider = "emergent"; models = the playbook admissible list (subset carried at connected_at).
- Custody = env-var only; never rendered on any surface; every crossing verifies the key is on record before invoking.

### (c) Solva (adapted from Executive-Final donor)
- **Reuse**: **ADAPT** `Akki-Executive-Final/backend/services/solva/reasoning/` (subpackage: `frame_audit_engine.py`, `candidate_generation.py`, `refusal_logic.py`) → `services/solva/` (minimal — frame_audit + candidate_generation + synthesis for W5; triangulation + tension + probability_weighting deferred to W6+ under Grey Mirror).
- Every stage calls `services.chokepoint.llm.invoke(purpose=...)` with a distinct purpose string.
- ALLOWED_PURPOSES entries this wave: `solva.frame_audit`, `solva.candidate_generation`, `solva.synthesis`, `thinklab.direct_answer`, `chat.governed_answer`, `llm.connect_verify`.
- **CP3 honesty binding** (owner sharpening §4): if any stage returns a Doc 04 refusal verdict (`evidence_insufficient` / `out_of_scope` / `high_stakes_low_evidence` / `purpose_refused` / `masking_tier_refused`), surface renders the refusal string VERBATIM — never a smoothed answer (A8-Q3).

### (d) ThinkLab reasoning wire-through
- The dormant reasoning panel from W4 → live reasoning stages. On admission, kick off `solva.frame_audit(direction_statement)` → render verdict; then `solva.candidate_generation` → render 3 candidates; then `solva.synthesis` → render coach-voice paragraph.
- Each stage renders its receipt identity (rcp-<hex>) AND its **model provenance** — model_id + provider pulled from the receipt (owner sharpening §4) — REFERENCE-NOT-COPY.
- No canned fallbacks: on shield refusal, refusal card renders the reason.
- If receipt lacks model_id (should not happen after CP2), render `model provenance unavailable` and refuse the reasoning body display.

### (e) Chat surface
- Minimal v7-exact chat page at `/chat`. One-question / one-answer form; purpose = `chat.governed_answer`.
- On submit, renders the answer + its crossing receipt (model · purpose · tier · tokens_in · tokens_out · latency_ms · at).
- Answer body carries model provenance line ("Answered by <model_id> via <provider>") from the receipt.

### (f) Reasoning Shield surface
- Extends `/shield` with a second sub-region: reasoning receipts (filtered on `kind == "solva_synthesis"` OR `kind == "chat_governed_answer"`). Renders purpose · tokens_in · tokens_out · latency_ms · model_id · masking_tier · at_iso · attributed_actor per row.

## 4. Connect drawer-chat LLM chip (owner-mandated build)
- Extend `ConnectDrawerChat.jsx`: "An LLM" chip prompts a paste; deterministic parser recognises Anthropic `sk-ant-`, OpenAI `sk-`, Gemini shapes; key lands in `estate_keys/llm_<provider>_<connection_id>.json` custody (**`.json` shape per owner sharpening §3**, consistent with `estate_keys/aws_<source_id>.json` from W1 — mode 0600, gitignored, NEVER in responses).
- Connection verified with a minimal governed call (`purpose = llm.connect_verify` — **verification itself transits the chokepoint** per owner sharpening §2). NOT wired to reasoning yet — verification is a one-shot round-trip.
- **Chat renders `•••• captured` from the FIRST parse turn** — the key never round-trips to the client after paste (owner sharpening §3).
- **Egress allowlist for the provider host is added ONLY on successful verify** (owner sharpening §2) — a ledger row records the allowlist change like any other governed value.

## 5. Reuse pulls cited

| Pull | Source | Destination |
|------|--------|-------------|
| **ADAPT** `Akki-Executive-Final/backend/services/synisense/shield/purpose_validator.py` (60 LOC) | Purpose-gate ADAPT | `services/chokepoint/llm_purpose_gate.py` |
| **ADAPT** `Akki-Executive-Final/backend/services/solva/reasoning/frame_audit_engine.py` + `candidate_generation.py` + `refusal_logic.py` | Solva ADAPT | `services/solva/reasoning.py` |
| **ADAPT** `Akki-Executive-Final/backend/services/solva/models.py` record shapes (FrameAuditRecord, CandidateRecord, Layer3Record) | Contract ADAPT | `contracts/solva_records.py` |
| **v7 fabric** — Chat sub-tree (offsets ~410000+) | Chat surface | `pod_shell/frontend/src/components/Chat.jsx` |
| **v7 fabric** — Reasoning Shield extension of Trust Center | Shield extension | Inline extension of `DataShield.jsx` |
| **Integration playbook** — Emergent Universal LLM | Invoke shape | `services/chokepoint/llm.py` |

## 6. Persistence

- LLM crossing receipts: `phase0/crossing_receipts/rcp-<hex>.json` (existing W3 shape) with additional `payload_shape` fields per owner sharpening §1: `model_id`, `provider`, `tokens_in`, `tokens_out`, `latency_ms`, plus stage-specific fields (e.g., `stage`, `direction_ref`).
- Solva reasoning artefacts: `phase0/solva_runs/run-<hex>.json` — carries stage results (each references its receipt by identity).
- Emergent-universal LLM record: `phase0/data_connection_records/data_source_emergent_universal_20260825T....json` (matches Data API / VM connection record pattern).
- Provider-key custody (BYO LLM): `estate_keys/llm_<provider>_<connection_id>.json` — mode 0600, gitignored, NEVER returned in responses.

## 7. Scope class L (≤2500 LOC) accounting

Estimates:
- Backend chokepoint.llm + purpose gate + models: ~250 LOC.
- Backend solva (minimal): ~350 LOC.
- Backend chat + reasoning shield endpoints: ~150 LOC.
- Backend registry_facts extension for emergent: ~60 LOC.
- Backend Connect LLM chip endpoint (paste parser + verify + custody): ~150 LOC.
- Backend tests: ~700 LOC (metering + provenance + purpose gate + AST + honesty + custody).
- Frontend Chat.jsx: ~250 LOC.
- Frontend DataShield.jsx extension (reasoning receipts + provenance): ~150 LOC.
- Frontend ThinkLab reasoning wire (with provenance line): ~250 LOC.
- Frontend ConnectDrawerChat LLM chip: ~150 LOC.
- Frontend tests: ~200 LOC.
- **Estimate total: ~2660 LOC** — 6% ABOVE **L (≤2500)**. Stop-and-report cap if drifting past 2500; owner correction of Solva vocabulary does not add LOC (rename is line-for-line).
- **Mitigation:** if drifting past 2500, checkpoint-commit at CP3 close and report before CP4 opens. Data Suite defers to W6 as owner's stated fallback.

## 8. Checkpoint commit plan

- Checkpoint 1 · Ruling + brief (this) → committed.
- Checkpoint 2 · LLM chokepoint + purpose gate + Emergent registration + AST update + tests-first + green.
- Checkpoint 3 · Solver adapted + ThinkLab reasoning wire + tests + screenshot.
- Checkpoint 4 · Chat surface + Reasoning Shield extension + Connect LLM chip + screenshots.
- Checkpoint 5 · Wave close: STATE + dashboard + final green.
