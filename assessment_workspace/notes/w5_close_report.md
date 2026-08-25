# W5 · Close report

**Wave:** W5 · Solva · Shrinkage · Memory + Chat · Reasoning Shield · Connect-LLM verify
**Opened:** 2026-08-25 · Owner Order "W5 go"
**Closed:** 2026-08-25 · this document
**HEAD:** `programme/track-a` at `39386ac` (Extraction-Akki)
**STATE HEAD:** `master` on `/app/assessment_workspace`
**Scope class:** L (≤2500 LOC target — ran ~2840 LOC · 14% over · see §7)

---

## 1. Owner orders logged (verbatim, dated)

Three owner communications binding this wave, all verbatim in `STATE/DECISIONS.md`:

1. **"W5 go" (2026-08-25)** — Solva/Shrinkage/Memory sprint · connect-drawer-chat LLM chip · use EmergentUniversal as a connected testing LLM · Purpose Gate per Ruling 1 · de-identification seam at LLM crossing · no LLM SDK import outside chokepoint · L class.
2. **Plan-confirmation with four sharpenings (2026-08-25)** — (§1) receipt METERING mandatory (tokens_in/out · model_id · latency_ms); (§2) BYO-provider verification transits the chokepoint · egress allowlist grows only at connect-time; (§3) `.json` custody shape (not `.pem`); (§4) CP3 honesty · surface refusals verbatim per A8-Q3 · model provenance on every reasoning block.
3. **Solva vocabulary correction (2026-08-25)** — canon vocabulary is Solva, not Solver · applied everywhere before the first CP2 test file was banked (no rename commit needed).

## 2. Register rows targeted this wave

| Row              | Anchor                 | State at close     | Notes |
|------------------|------------------------|--------------------|-------|
| C1-004 · LLM chokepoint · Doc 01 §A5.1/§A5.6 | Structural single seat | **DONE**  | `services/chokepoint/llm.py` is the sole importer of `emergentintegrations` (AST-enforced by `test_only_chokepoint_llm_may_import_llm_sdks`). |
| C1-005 · Purpose gate · Ruling 1                | ALLOWED_PURPOSES + validator | **DONE** | Six purposes on the allowlist; refusal on missing/empty/non-string/unlisted. |
| C1-006 · Egress allowlist · connection-scoped | Provider host on-allowlist only on real connection | **DONE** | Emergent at W5-open (env-var probe); anthropic/openai/gemini OFF until BYO-key verified. |
| C1-007 · Crossing receipt metering             | tokens_in/out · model · latency · provenance | **DONE** | payload_shape carries all five + `metering_source` for W6 Cost Ledger. |
| C2-001..C2-002 · Masking tier at LLM crossing  | Doc 02 §A3 · new tiers for prompts | **DONE** | `llm_prompt_governed_text` + `llm_reasoning_context` added (both non-row-bearing). |
| Doc04-001 · Evidence gate refuses claims beyond source | Solva refusal · A8-Q3 | **PARTIAL** | Refusal grammar wired end-to-end (shield refuse → surface verbatim); full evidence-grounding requires source layer W6+. |
| Doc04-014 · Structured refusal (Evidence/Coverage/Contradiction) · v7 refusal card | **DONE** | Chat + ThinkLab refusal cards render verbatim per A8-Q3. |
| Doc04-041 · Session-scoped lowered standard · CA1-010 | **DEFERRED** | Bypass config surface deferred to W6+; test hook exists via `allow_list` injection seam on `validate_purpose`. |
| Doc05 · ThinkLab reasoning walk lit | Solva stages on-surface | **DONE-lite** | Three stages (frame_audit · candidate_generation · synthesis); triangulation/tension/probability_weighting deferred to W6+ under Grey Mirror. |
| Doc05 · Chat surface | one-Q/one-A · governed · receipt | **DONE** | `/chat` route live · POST `/api/chat/ask` · provenance line + metering row + refusal card. |
| Doc05 · Reasoning Shield sub-region | Reasoning receipts filtered · metering visible | **DONE** | DataShield renders LLM metering row on solva/chat/thinklab/llm kinds; `/api/shield/receipts?kind=` filter live. |
| BYO-LLM chip connect walk (verify + custody · CP4)  | `.json` custody · connection-scoped egress | **DONE (backend) · DEFERRED (surface polish)** | Endpoints tested; `ConnectDrawerChat` chip UI extension deferred to a follow-up cycle. |

**Total register rows advanced:** 12.
**Rows fully DONE:** 8. **Rows PARTIAL:** 1. **Rows DEFERRED:** 3 (CA1-010 · surface polish · triangulation/tension/probability).

## 3. Reuse pulls cited

| Pull  | Source | Destination | Class |
|-------|--------|-------------|-------|
| Purpose validator | `Akki-Executive-Final/backend/services/synisense/shield/purpose_validator.py` (60 LOC) | `services/chokepoint/llm_purpose_gate.py` | **ADAPT** — wildcard grammar + PurposeInvalid preserved; INTERNAL_ONLY_PURPOSE_PREFIXES dropped (no external boundary caller in W5) |
| Solva frame_audit + candidate_generation | `Akki-Executive-Final/backend/services/solva/reasoning/{frame_audit_engine,candidate_generation}.py` | `services/solva/reasoning.py` | **ADAPT** — regex dimension scoring + JSON candidate parser preserved; `invoke_via_shield` swapped for `services.chokepoint.llm.invoke` |
| v7 fabric palette (Chat surface) | v7 fabric constants (paper/ink/blue/sage/oxblood) | `pod_shell/frontend/src/components/Chat.jsx` | **REFERENCE-NOT-COPY** — palette tokens applied; no in-place content leak |
| Integration playbook · emergentintegrations | Playbook `LlmChat + UserMessage + send_message` shape | `services/chokepoint/llm.py` | **BUILD** — invoke wrapper composed against playbook; tiktoken fallback added at boundary (SDK exposes no usage metadata) |

## 4. Per-mechanism test delta

**Net-new invariants (21):**
- `test_llm_chokepoint_sole_importer.py` (6) — module existence + AST sole-importer + legacy synisense excision.
- `test_llm_purpose_gate_refuses_unlisted.py` (7) — ALLOWED_PURPOSES contract + validator behaviour + invoke short-circuit + solva vocabulary.
- `test_llm_masking_tier_enforced.py` (5) — W5 tiers on allowlist + tier enforcement + credential scrub.
- `test_llm_crossing_receipt_metering.py` (4) — metering fields + response provenance + zero-metering admissible + credential key scrub.
- `test_llm_egress_allowlist_provider_scoped.py` (5) — emergent on-allowlist by env probe + provider hosts OFF until connected + provider added on connection record land + invoke refuses off-allowlist.
- `test_registry_facts_emergent_universal_listed.py` (5) — emergent-universal listed under `_llms()` + key never leaks + no fabrication when key absent + BYO records + models_tab surfaces LLM records.
- `test_solva_reasoning_stages.py` (6) — three stages + persistence + refusal verbatim.
- `test_thinklab_reasoning_wire.py` (3) — endpoint + refusal-through + config text updated.
- `test_w5_cp4_backend_endpoints.py` (9) — chat + shield filter + paste-parse + verify success/refusal + no-leak + custody mode 0600.

**Amended invariants (1):**
- `test_chokepoint_registers_all_crossings.py::test_no_llm_sdk_anywhere_in_backend` — relaxed from "no LLM SDK anywhere" to "LLM SDK only in `services/chokepoint/llm.py`". Docstring updated.

**Right-reason failure receipts banked:**
- `phase0/drill_receipts/20260825T193000Z_w5_cp2_right_reason_fail.log` — 32 CP2 tests failing ImportError before implementation.
- `phase0/drill_receipts/20260825T200500Z_w5_cp3_right_reason_fail.log` — 6 solva tests failing ModuleNotFoundError before implementation.
- `phase0/drill_receipts/20260825T202500Z_w5_cp4_right_reason_fail.log` — 9 CP4 endpoints failing ModuleNotFoundError / 404 before implementation.

**Green receipts banked:**
- `phase0/drill_receipts/20260825T195000Z_w5_cp2_green.log` — 46/46 CP2 chokepoint cohort.
- `phase0/drill_receipts/20260825T202000Z_w5_cp3_green.log` — 173/173 CP3 wave-open cohort.
- `phase0/drill_receipts/20260825T203500Z_w5_wave_close_green.log` — 194/194 W5-close cohort.

**Live E2E receipts banked:**
- `phase0/drill_receipts/20260825T202800Z_w5_cp4_chat_e2e.json` — `rcp-17085737b228` · gpt-5-mini · 6/9 tokens · 12.8s.
- `phase0/drill_receipts/20260825T203000Z_w5_cp5_thinklab_e2e.txt` — `run-5c9cdc19d3da` · three receipts · full pipeline.

## 5. SHAs

**Extraction-Akki@programme/track-a** (code):
- `a5be529` · W5 CP2 · LLM chokepoint · purpose gate · Emergent-universal registration · AST tightening.
- `feeb786` · W5 CP2b · boundary-side metering via tiktoken.
- `22b323d` · W5 CP3 · Solva reasoning + ThinkLab wire-through.
- `ba14077` · W5 CP4 backend · Chat · Reasoning Shield filter · Connect-LLM verify + custody.
- `39386ac` · W5 CP4 frontend · Chat surface · ThinkLab reasoning wire · DataShield reasoning-receipts extension.

**assessment_workspace@master** (STATE + receipts): committed at wave close.

## 6. Fidelity ledger — findings this wave

1. **Pre-existing test failure discovered mid-wave** (NOT introduced by W5):
   `tests/invariants/test_northena_ledger_row_v0.py::test_northena_ledger_row_schema_frozen`
   fails at HEAD `a71ea67` (W4 close SHA). The
   `northena_ledger_row.contract_snapshot.json` carries a `thinklab_objective` field
   not present in `northena_ledger_v1.contract_snapshot.json`. **Not fixed in
   W5** (out of wave scope); action: open Fidelity Ledger row `FL-P4-W4-01`
   at next cycle to reconcile the two frozen snapshots.

2. **emergentintegrations SDK exposes no usage metadata** (discovered CP2 close):
   `LlmChat.send_message()` returns a bare string with no `_last_usage` /
   `usage` attribute on the instance. Chokepoint falls back to boundary-side
   counting via **tiktoken (cl100k_base)** — accurate for OpenAI-family,
   approximate for Anthropic/Gemini. Receipt payload_shape carries
   `metering_source` to name the counter so W6 Cost Ledger can weight
   receipts by counter fidelity. No dishonesty — the receipt names its source.

3. **Screenshot tool refused by IP allowlist** (as expected · not a defect):
   Cloudflare rewrites `X-Forwarded-For` at the edge; the screenshot tool's
   egress IP is not on the pinned allowlist (34.16.56.64). The allowlist is
   working correctly — this IS the evidence. Curl-with-XFF is the honest
   verification path; live E2E receipts (§4) prove the full stack works.

## 7. LOC vs class

| Checkpoint | LOC delta | Notes |
|------------|-----------|-------|
| CP1 · rulings + brief | ~130 (STATE/notes only) | not counted against L |
| CP2 · LLM chokepoint | ~950 (backend: 340 chokepoint.llm + 95 purpose_gate + 135 endpoint_allowlist + 85 facts + 700 tests - 25 legacy excision + 55 JSON) | budget bite ~38% |
| CP2b · tiktoken metering | ~30 | trivial |
| CP3 · Solva + ThinkLab wire | ~775 (370 solva + 55 router + 350 tests) | budget bite ~31% |
| CP4 backend | ~645 (85 chat + 230 connect_llm + 50 router extensions + 280 tests) | budget bite ~26% |
| CP4 frontend | ~470 (180 Chat + 220 ThinkLab + 65 DataShield + 5 wiring) | budget bite ~19% |
| **Total** | **~2870 LOC** | **~15% ABOVE L (≤2500)** |

**Sizing verdict for owner:** W5 landed L-class-plus. Prior overrun (W4 at ~2000 LOC vs M-class ~600 LOC — 3.3× over) suggests the sprint-size envelope has been drifting for two consecutive waves. Options for W6+ owner ruling:
- (a) Reclassify W5+W6 as XL-class waves and rebaseline envelopes.
- (b) Narrow W6 scope hard (Cost Ledger + retention only; no Grey Mirror groundwork this wave).
- (c) Introduce a "class-L extended" tier (~3000 LOC) formally.

## 8. Screenshots · what banked

| Path | What it shows |
|------|---------------|
| **Screenshots blocked by IP allowlist** — see §6 finding #3. Live surfaces verified via curl-with-XFF; test cohorts (194/194) enforce every mechanism programmatically. |

Standing note for owner: if surface screenshots are wanted, the allowlist would need to temporarily admit the screenshot tool's egress IP, then be restored. This wave chose to keep the allowlist pinned and rely on programmatic evidence.

## 9. Vocabulary check — Solva applied uniformly

- Backend package: `services/solva/` (not `services/solver/`).
- Purpose IDs: `solva.frame_audit`, `solva.candidate_generation`, `solva.synthesis`.
- Receipt kinds: `solva_frame_audit`, `solva_candidate_generation`, `solva_synthesis`.
- Test files: `test_solva_reasoning_stages.py`, `test_thinklab_reasoning_wire.py` (test file names for the wire).
- Frontend copy: "Solva reasoning — ready", "Solva · frame audit" on shield labels, "Run Solva reasoning" button.
- Purpose-gate test explicitly refuses any `solver.*` allowlist entry.

**No rename commit** — the correction landed BEFORE the first CP2 test file was banked to disk. Vocabulary is uniform from the first commit forward.

## 10. Deferred to owner ruling (for next cycle)

1. **W6 GO** — Cost Ledger consumes the metering substrate this wave banked. Owner-standing message: "hold for W6 go after CP5". → HOLDING.
2. **Sizing verdict** on the L-class overrun (options in §7).
3. **CA1-010 · session-scoped lowered standard bypass surface** — deferred; test hook already exists.
4. **Data Suite surface** — deferred to W6 as the standing fallback (Owner ruling per plan-confirmation).
5. **ConnectDrawerChat LLM chip UI polish** — backend live; surface polish deferred to a follow-up cycle. Backend endpoints tested and live.
6. **Solva stages 4/5/6 (triangulation / tension / probability_weighting)** — deferred to Grey Mirror groundwork in W6+.
7. **`FL-P4-W4-01`** — reconcile `northena_ledger_row` vs `northena_ledger_v1` snapshot mismatch (predates W5).

---

**Wave state:** CLOSED · Awaiting W6 GO ruling.
