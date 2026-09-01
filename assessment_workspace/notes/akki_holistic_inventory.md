# Akki holistic inventory — engines, gates, rules

**Authority:** owner question, 2026-08-31, verbatim: *"On full implementation how many rules, gates, engines does akki holistically have"*. Bounded read-only accounting task; time-box ~20–30 min; sourced only from on-disk artefacts (canon docs at `canon/text/`, REUSE_ASSESSMENT.md, STATE/DECISIONS.md, STATE/SPRINT_PLAN.md, backend/services/, backend/tests/invariants/, chokepoint allowlists, App.js V8_SUBSTITUTIONS, baseline_failures.json).

**Working definitions (as Akki uses them):**

- **Engine** — a distinct functional service that operates on the platform's real workloads (measures, decides, reasons, gates, records, or governs). The canon names six "engines" per se (Northena, SyniSense, Solva, Mtafiti, Targeta, Watch); the code tree carries these plus every service module that runs alongside them (compute estate, census engine, training runner, chokepoint, audit trail, etc.). "Engine" in this inventory covers both.
- **Gate** — an enforcement or refusal point where a request/crossing/render is either admitted or refused against a declared rule. Includes governed chokepoints (data crossings, masking tiers), route guards (MUST_BE_LIVE_ROUTES), IP allowlist, redaction/sanitizer, compliance controls (CA1-N*), and product-side substitution gates on the UI surface.
- **Rule** — an artefact that fixes what a gate refuses/admits, or what an engine may/may not do. Owner rulings (banked verbatim in DECISIONS.md), policy artefacts (masking tiers, endpoint allowlists, PII classifications, continuity policy), UI substitution rules, and invariant tests as the mechanical enforcement layer that makes rules refuse-on-break.

---

## Compact summary table

| Category | BUILT NOW (on disk) | CHARTERED (in flight) | CANON-DECLARED not yet chartered | Total at full implementation (estimate) |
|---|---:|---:|---:|---:|
| **ENGINES** — service modules | **69** | **4** (new engines inside 4 open charters) | **~10** (major canon surfaces without a charter) | **~83** |
| **GATES** — enforcement/refusal points | **~90** (see breakdown) | **~10** (Shield-Train row_extractor/masked_transport + WPW eligibility gates) | **~30–50** (per-column PII gates × 233 tables + full CA1 grid + verification-pack gates) | **~140–160** |
| **RULES** — governance + tests | **2703 invariants** + **20 UI substitutions** + **~20 policy artefacts** + **87 DECISIONS.md anchored sections** (~24 numbered owner rulings) | **~10 policy artefacts** (masking policy, per-column PII expansion, WPW eligibility policy) | **~1500–2500** (per-column PII classifications for 233-table estate; verification pack rules; regulator pack rules) | **~4500–5500** invariants + **~3000** policy rules |

**Total** at full implementation ≈ **~83 engines, ~140–160 gates, ~7500–8500 rules** (invariants + policy artefacts + rulings combined).

---

## 1 · ENGINES — the count, split three ways

### 1.1 · BUILT NOW · 69 service modules on disk

Enumerated from `backend/services/*/` on `programme/track-a` HEAD 37164e8 (non-`__pycache__` directories):

**Canon-named engines (6/6 present, all partial or full):**
`northena` · `synisense` · `solva` (+ `solva_depth`) · `mtafiti` · `targeta` · `watch`

**Governance / custody / receipt machinery (Doc 3 §13–§32):**
`chokepoint` (with `masking_tier`, `residency`, `llm_endpoint_allowlist`, `llm_purpose_gate`, `llm`, `router`, `dry_run`) · `outer_gate` · `audit_trail` · `model_registry` · `model_admission` · `model_recheck` · `evidence_register` · `retention` · `rights_quarantine` · `compliance` · `response_sanitizer` · `governance` · `master_admin` · `handoff` · `team` · `approvals` · `checker` · `baseline_line` · `cost_ledger` · `n_series` · `estate_keys` · `declaration` · `layer_a` / `layer_b` / `layer_c` · `lowered_standard`

**Operating / extraction machinery (Doc 4 §1–§Economics):**
`census_engine` (+ `census_dimensions`) · `compute_estate` · `compute_seam` · `training` · `training_runner` (with `ssh_seam.py`) · `perception` · `grey_mirror` · `memory` · `trace` · `data_source` · `connect` (+ `connect_estate`) · `registry` (+ `registry_facts`) · `transform_forms` · `use_data` · `canonical_projection` · `critic_pass` · `opportunity_briefs` · `economics` · `g1_defensibility`

**Product-side / user-facing services:**
`chat` · `wizard` · `whitepapers` · `skill_files` · `multi_instance`

**Infrastructure services (not engines per canon, but present):**
`auth` · `health` · `ip_allowlist` · `artifact_store` · `credentials_paste` · `service_1` (integration-console stub) · `v1_harness` · `v2_gate` · `v3_harness`

### 1.2 · CHARTERED (in flight per STATE/SPRINT_PLAN.md) — 4 new engine bodies inside 4 open charters

- **W-TxtTrain-v2** — improved LoRA text training run (owner-authorized 2026-08-31T~21:20Z "run a longer one" go-ahead). No new engine · extends existing `training_runner` and `tools/text_train_pipeline`.
- **W-Shield-Train** — shielded-training pipeline. Introduces ~3 new service modules: `chokepoint/row_extractor` (row-bearing SQL executor · Doc 02 §A5.2), `training_runner/masked_transport` (masked-file transport with sha256 gate), `training_runner/lora_full` (unstub `execute_lora_train_real`).
- **W-Audio-P2** — audio archive Phase 2 admission ceremony (manifest hash → representative slice → HSS → GPU smoke). Extends existing audio_plane; may add a dedicated admission surface.
- **W-WPW-v1** — Whitepaper Wizard v1 Tiers 1+2. Extends existing `whitepapers` and `wizard`; adds notebook + technical-report generators. Tier 3 blocked on Rulings R1/R2/R3.

Two more charters already **CLOSED** tonight (banked in SPRINT_PLAN.md):
- **W-G5c-close** · retirement + keypair-hardening (CLOSED 20260831T2033Z · floor 2680→2692)
- **W-G5c-COMPUTE-v2** · 11 tile-value substitutions on Compute Connected (CLOSED 20260831T2131Z · floor 2692→2703)

### 1.3 · CANON-DECLARED not yet chartered — ~10 major surfaces

Reading through Canon 3 (Governance Engines), Canon 4 (Operating Engines), Canon 5 (Interface Architecture), and Canon 8 (The Watch):

- **DRE / Decks** — mentioned as standing arrival in STATE/NEXT.md ("Decks/Documents build GO, owner-sequenced post-plan"). Spec ingested; charter awaits owner GO.
- **Trust Center** (Doc 3 §29) — partial via `governance` + `team`; no dedicated Trust Center service assembling verification packs / regulator packs.
- **Verification Packs** (Doc 3 §31) — no dedicated pack-generator engine.
- **Regulator Pack** (Doc 3 §32) — no dedicated regulator-facing pack service.
- **Integration Console** (Doc 5 §26 "Administer" + Application Registration) — `service_1` is a stub for A17.16 wire path only.
- **Commercial Applications console** (Doc 5 §38) — declared as consumer surface; no service yet.
- **Control Band console** (Doc 5 §41) — mapped to canon-declared consoles; no dedicated service.
- **Ask reference application** (Doc 5 §37) — declared as reference app consuming platform through Integration Console; no dedicated service.
- **Full Model Ladder** (Doc 3 §17) — partial via `model_admission` + `model_registry` + `model_recheck`; ladder-crossing sequencer not authored.
- **Full extraction stack** (Doc 4 §"remaining machinery") — extraction stack is scaffolded across `use_data`, `canonical_projection`, `transform_forms`, `layer_a/b/c`, `critic_pass`; end-to-end assembly under one governor pending.

### 1.4 · Engine totals

- BUILT NOW · **69**
- CHARTERED new engine bodies · **~4**
- CANON-declared major surfaces without charter · **~10**
- **Full-implementation estimate · ~83 engines/services**

---

## 2 · GATES — enforcement/refusal points

### 2.1 · Governed chokepoints (Doc 3 §13 · Doc 01 §A5.2 custody sequence)

- **Masking-tier allowlist** — `backend/services/chokepoint/masking_tier_allowlist.v0.json`. **8 tiers declared · 5 admitted · 3 not-yet-admitted**:
  - Admitted: `structure_only`, `attested_command`, `receipt_only`, `llm_prompt_governed_text`, `llm_reasoning_context`.
  - Not-admitted (row-bearing, awaits prerequisites): `t1_full_mask`, `t2_partial`, `t3_category`.
- **LLM endpoint allowlist** — `chokepoint/llm_endpoint_allowlist.v0.json`. Positive-allowlist gate over which endpoints may be called via the LLM crossing.
- **LLM purpose gate** — `chokepoint/llm_purpose_gate.py`. Refuses LLM crossings whose declared purpose is not in the allowlist.
- **Residency allowlist** — `chokepoint/residency_allowlist.v0.json`. Refuses crossings that would land data outside declared residency.
- **Custody sequence gate** — `chokepoint/router.py` orchestrates the four-step custody per Doc 01 §A5.2.

**Chokepoint sub-gate count: 5 declared + 8 masking tiers = 13 discrete gate rules.**

### 2.2 · Route table drift guard (Ship-Manifest DoD extension)

- **MUST_BE_LIVE_ROUTES** — `backend/tests/invariants/test_ship_manifest_dod_route_table_drift.py`. **41 entries** currently. Each entry gates: "route path shipped in a CP-close receipt must be reachable through the pod's live openapi". Adding a route here is a conscious act (no dynamic derivation); a CP that ships a wire path MUST add its route here in the same commit.

### 2.3 · IP allowlist middleware (source-IP admission)

- **`services/ip_allowlist/middleware.py`** — 1 middleware, 2 layers (SPINE + OWNER), 2 modes (`strict` fail-closed default vs `permissive` demo mode). Every decision logged via `ip_allowlist_decision` INFO line (nothing silent).

### 2.4 · Response sanitizer / PII redaction

- **`services/response_sanitizer/`** — 1 sanitizer + **1 PII classification** currently authored (`digicow_live.ussd_users.occupation` per Ruling #2, 2026-08-28 · conservative_default_quasi_identifier).
- Declassification path is CLOSED (unlock requires `linkage_risk_assessment` + `dpo_signoff`).

### 2.5 · Compliance controls (CA1-N* series)

- **14 controls** anchored in DECISIONS.md + NEXT.md: `CA1-001` through `CA1-009` (audit-trail Overview surface controls) + `CA1-N1` through `CA1-N5` (retention / residency / erasure / continuity / RTO).
- Current status: CA1-001/002/003 BUILT (audit_trail Overview surface CLOSED Wave F), CA1-N5 RTO=3600s DEFAULT-class RATIFIED (Ruling #1, 2026-08-28), CA1-N1/N4 remain VERIFICATION-class.

### 2.6 · UI substitution gates (product-facing render gates)

- **`V8_SUBSTITUTIONS`** in `pod_shell/frontend/src/App.js`. **20 rules** currently: 9 legacy (registry hero sentence, census header/byline, 3 tile pairs) + 11 compute-v2 (compute-v2-clusters/gpus value/byline, capacity/committed/free/jobs/workflows/utilisation, runs-receipted).
- Each rule is a substitution gate: if the rule's dummy is present in the rendered DOM and its anchor context matches, the substitution engine replaces the dummy with either a live-values fragment (from `/api/*`) or an honest-empty fragment (never with echoed prototype numbers · `theatre-vs-honesty` invariant).
- **Rule-must-match-rendered-DOM invariant** (owner Ruling A, Wave-G5b): every rule must be provably bound to real DOM; orphan rules (no marker, no dummy in body) are RED, not silent no-ops. Enforced by `capture_ground_truth()` in the real-Chromium harness.

### 2.7 · Eligibility gates (WPW · declared, not yet built)

Per **W-WPW-v1** charter (SPRINT_PLAN.md): novelty gate, exceptional-preservation gate, dual-judge concurrence gate. All declared in canon (Doc 19 whitepaper section), not yet coded.

### 2.8 · Gate totals

| Kind | Count |
|---|---:|
| Chokepoint sub-gates + masking tiers | **13** |
| MUST_BE_LIVE_ROUTES entries | **41** |
| IP allowlist middleware (1 middleware × 2 layers × 2 modes) | **1** |
| Response sanitizer / PII classification gates | **1 sanitizer + 1 classification** = **2** |
| Compliance controls CA1-N* + CA1-00X | **14** |
| UI substitution gates (V8_SUBSTITUTIONS) | **20** |
| Eligibility gates (WPW declared, not built) | **~3** |
| **BUILT NOW total** | **~90** |
| **CHARTERED** (Shield-Train row_extractor + masked_transport + LLM chokepoint completion + WPW eligibility) | **~10** |
| **Not-yet-chartered** (per-column PII across ~233 tables × avg ~10-20 cols/table + verification pack gates + regulator gates + Doc 10 evidence-record backfill) | **~30–50** |
| **Full-implementation estimate** | **~140–160 gates** |

---

## 3 · RULES — what the gates enforce

### 3.1 · Owner rulings (banked verbatim in DECISIONS.md)

- **87 anchored `## ` sections** in `STATE/DECISIONS.md` (append-only log).
- Of these, **~24 are numbered "Ruling N" / "Owner Ruling N" / "Owner ruling N"** shape — the direct owner rulings the four-test discipline binds (Ruling 1, 2, 3 · Owner Ruling on FL-P2-03/04 · Owner Ruling on Console-Access · Owner Stop-Order · Owner Fixture Drop · Owner Course-Correction · Owner Simplification · Owner rulings 3–8 across the tonight thread, etc.).
- Remaining anchored sections capture wave-closes, orchestrator rulings, standing rules, and interleave decisions — all binding under Ruling 1's discipline ("an unlogged ruling is treated as not having lawfully happened").

### 3.2 · Governance / policy rules encoded as artefacts

| Artefact | Location | Entries |
|---|---|---:|
| Masking-tier allowlist | `services/chokepoint/masking_tier_allowlist.v0.json` | 8 tiers |
| LLM endpoint allowlist | `services/chokepoint/llm_endpoint_allowlist.v0.json` | 1 file |
| Residency allowlist | `services/chokepoint/residency_allowlist.v0.json` | 1 file |
| Continuity policy | `services/watch/continuity_policy.v0.json` | 12 keys (RTO=3600s DEFAULT + cadence + ruling refs) |
| PII classification registry | `services/response_sanitizer/pii_classification_registry.v0.json` | **1 classification** (`digicow_live.ussd_users.occupation` per Ruling #2) |
| DIGICOW_PII_BANNED_FIELDS | `services/response_sanitizer/` | small set (occupation now included) |

**Currently authored: ~20 policy-artefact rules.** At full implementation, the PII classification registry alone needs a per-column decision across the estate's **233 tables** (Census #1 count). Assuming avg ~10–20 columns/table, that's **~2,300–4,600 per-column classifications** at full coverage. Plus verification-pack rules and regulator-pack rules.

### 3.3 · UI substitution rules (mechanical rules that keep the product surface honest)

- **20 rules** in `V8_SUBSTITUTIONS` (App.js).
- Each rule: `{name, kind, dummyContent, anchorAncestorText, renderFragments}` — declarative rule that binds prototype dummies to live/honest-empty renders.
- Residuals in queue: **-r1** chart-caption substitution + **-r2** tile-note substitution (banked as scope, not bugs).

### 3.4 · Invariant tests as the mechanical rule-enforcement layer

- **246 test files** in `backend/tests/invariants/`.
- **2,703 tests currently passing at the ratchet floor** (as of 20260831T213000Z close of W-G5c-COMPUTE-v2, banked in `baseline_failures.json.counts_at_baseline.passed = 2703`).
- Ratchet trajectory (from `ratchet_history` in same manifest): 1,830 (Wave D CP-D0) → 2,041 (CP-D5) → 2,066 (CP-D6) → 2,119 (Wave D endgame) → 2,169 (Wave E) → 2,355 (Wave F) → 2,463 (Wave G2) → 2,566 (Wave G4) → 2,594 (Wave G5b) → 2,611 (Wave-G5b close) → 2,636 (Wave-G5c-CENSUS) → 2,649 (COMPUTE-BACKEND) → 2,669 (RULINGS-1-2-5) → 2,680 (COMPUTE-FRONTEND) → 2,692 (W-G5c-close) → **2,703 (W-G5c-COMPUTE-v2-close · tonight)**.
- Extrapolating the average +15–25 delta per wave × the count of remaining chartered + canon-declared work → **full implementation likely lands ~4,500–5,500 invariants**.

### 3.5 · Rule totals

| Kind | BUILT NOW | Full-implementation estimate |
|---|---:|---:|
| Owner rulings anchored in DECISIONS.md | 87 (~24 numbered) | 87 (append-only; grows with owner rulings landing) |
| Policy artefacts (masking tiers, allowlists, PII, continuity, sanitizer) | ~20 entries across 6 files | ~3,000 (dominated by per-column PII across the 233-table estate) |
| UI substitution rules (V8_SUBSTITUTIONS) | 20 | ~40–60 (add -r1 chart captions + -r2 tile notes + other consoles) |
| Invariant tests (mechanical rule enforcement) | 2,703 | ~4,500–5,500 |
| **Total rules** | **~2,830** | **~7,500–8,500** |

---

## 4 · Honest caveat on precision

**Exact on-disk counts (verified this session · from `backend/services/`, `backend/tests/invariants/`, `chokepoint/*.v0.json`, App.js V8_SUBSTITUTIONS, `baseline_failures.json`, DECISIONS.md `grep`):**
- Service modules: **69** · invariant test files: **246** · invariants passing at floor: **2,703** · MUST_BE_LIVE_ROUTES: **41** · masking tiers: **8** (5 admitted / 3 not) · UI substitution rules: **20** · PII classifications authored: **1** · CA1 controls: **14** · DECISIONS.md anchored sections: **87** (numbered owner rulings ≈ **24**) · Census #1 estate: **2 databases · 233 tables · 5,909,421 rows** (per Census #1 receipt at `phase0/census/census_0001/`).

**Estimated (not directly countable in a single artefact):**
- Canon-declared engines "not yet chartered" — extracted by reading Canon 3/4/5/8 headings and cross-referencing against `backend/services/`; the canon does not enumerate a single canonical list of all engines/machinery in one place. My count of ~10 major surfaces without a charter is a working estimate, not a canon-verified total.
- PII classifications at full implementation — estimated at **~2,300–4,600** by multiplying Census #1's 233-table count by an average of 10–20 columns per table; the exact column count per table exists in Census #1 per-database records at `phase0/census/census_0001/*.json` but wasn't summed to a single scalar for this note (would take a follow-on ~5 min pass).
- Full-implementation invariant volume — extrapolated from ratchet-history delta averages; not a canon-declared target.

**Not on disk (known-missing):**
- **Doc 10** is referenced in DECISIONS.md ("Doc 10 evidence-record backfill decision") but **is NOT present in `canon/text/`** (only Docs 1–9 + 17–19 are). Any engines/gates/rules Doc 10 declares are absent from this inventory. Owner may confirm whether Doc 10 exists elsewhere or is deferred.
- Whitepaper Wizard v1 spec (`canon/fixtures/whitepaper_wizard_spec_v1/`) is a *fixtures* input, not a canon document; specific rule counts for WPW eligibility gates are declared in the WPW_CHARTER.md (which I authored) rather than in canon text.

---

**Maintenance:** this note is the single-page owner-readable snapshot. Live counts drift as waves close; regenerate at each wave-close by re-running the small scripts under `tools/inventory/` (charter for follow-on if the owner wants an auto-refreshing version). Until then, this document is a manual point-in-time snapshot at 2026-08-31T~21:35Z (post W-G5c-COMPUTE-v2-close, floor 2703).
