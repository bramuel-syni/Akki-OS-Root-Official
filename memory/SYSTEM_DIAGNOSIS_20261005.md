# Akki — full system diagnosis (M1–M10 · five promises · Mα 31 jobs) — 5 October 2026

Owner order (verbatim, OWNER_ORDERS §10): "this was meant to be a full system diagnosis — not just for M alpha. M1–M10 as well. I need a deep assessment of the issues I raise and execution plan for orders I've given."

Status of this document: diagnosis only. No code, job, policy or model was changed to produce it. Live reads at 09:45–09:52 UTC on 5 Oct: three Mα GPU jobs running (listener it.5 `m9j-2bc0eea34925`, story_text it.9 `m9j-dade36472f5e`, story_voice it.10 `m9j-82202771c7fd`), witness pass `wp-3ab3a63a4464` at 09:45:01 consistent, cron ticks at 09:45 received, `malpha_review_tasks` 1,502 tasks / 0 annotated, nothing admitted. Companion: `EXECUTION_PLAN_20261005.md`.

Sources read for this diagnosis: Doc 1 Chokepoint (B35–B98), Doc 2 Confidentiality & Dual-File (B12–B87), Doc 11 Cost/Local-first (B16–B45, B62–B64), Audio Plane Spec §§1,5–7, Canon 4 Solva faculties as implemented, `M1_M10_STATUS_20261003.md`, `FIVE_PROMISES_CANON_ASSESSMENT_20261004.md`, `M_ALPHA_PLAN.md`, `M_ALPHA_EXECUTION_LOG.md`, `REQUIREMENTS_RECONCILIATION.md`, the live crossing code (`chokepoint/llm.py`, `synisense/shield/*`, `solva/*`, `solva_v2/*`), `training_lab/malpha*.py`, `training_runner/m9_serving.py`, `audio_plane_v1/character_register_write_boundary_v1.py`, `skill/scripts/backend.py`.

---

## PART A — The issues the owner raised, assessed one by one

### A1. "Jumpy; still interpreting an assumptive position on the requirements"

**Finding — substantiated.** Four mechanisms produced it:

1. **Compaction handoffs became the authority.** Each fork starts from an assistant-written summary. This fork's own handoff still said "Mocked: Hostility / Input-seat scorer" after the reconciliation had already corrected it, and still carried the "regex tighten → paid replay → MA-19" plan the owner had rejected. Agents plan from the summary in their first message instead of from canon.
2. **Questions already answered in canon were asked back.** Of the four decisions requested in the prior turn, two were prescribed: contained compute inside the perimeter (Doc 1 A5.5 "Compute does not leave the perimeter … models the organisation hosts … run inside"; Doc 11 A5.1 four-rung ladder, local before frontier) and reasoning-not-scanning for categories (Doc 2 A3 B21; Doc 1 B5.2 B83). Asking them signalled the canon had not been read.
3. **Plans proposed before the clause was located.** The first message of the prior fork proposed a regex tightening as a fix for a capability the canon says must be reasoning.
4. **No mechanical check** that a work item cites a resolving source before it is executed. `AGENTS.md` (5 Oct) states the rule; nothing enforces it.

**Root cause:** authority drift — assistant artefacts (handoffs, prior plans, green tests) treated as owner authority. Fix is procedural + mechanical (Plan WP-00).

### A2. "Shield had already been built (SyniSense + Solva + context preservation). You were only to enhance the LLM capability within SyniSense."

**What exists and is the owner of the crossing (verified in code):**
- `chokepoint/llm.py::invoke` — the sole external invocation (Doc 1 A5.1), fixed custody sequence de-identify → invoke → re-identify (A5.2), request-local token map (A5.3), tenant entity set (A5.4), endpoint allowlist (A5.5), trust receipt (A5.7), purpose gate, masking tiers, credential scrub, Watch input-seat emit.
- `synisense/shield/`: `deidentifier.py` (regex + tenant entities + installed local spaCy NER), `reidentifier.py`, `egress_firewall.py`, `masking_tier.py`, `trust_receipt.py`, `perception_router.py` (audio/vision custody pathway, A5.8), `task_separation.py` (owner Mα §2 data/task separation), `semantic_register.py` + `register_gate.py` (added 4 Oct under MA-04).
- `synisense/shield/llm_router.py`, `brief_synthesizer.py`, `fluency_synthesizer.py` — the original "LLM capability within SyniSense". **Excised by owner order W5 §4 (2026-08-25)**; now HARVESTED-BUT-DEAD, refused by the AST sole-importer gate. The only live LLM path inside SyniSense is the chokepoint.
- Solva: `solva_v2/*` deterministic faculties (load-bearing units, assertion boundary, intent audit, trace); `solva/reasoning.py` three-stage reasoning — **which calls the external model through the chokepoint**.
- Context preservation (Docs 7–8): memory plane / compaction / re-extraction handles — present, not touched by Mα.

**Where MA-04 drifted (the cause of the LLMShieldFailure loop):**
- Doc 2 A3 B21: categories are "recognised through the reasoning layer, not only by literal or pattern match". MA-04 implemented `semantic_register.classify` as cue-word + capitalisation regex and placed it, enforced, in front of every crossing (`register_gate.gate` inside `invoke`). It scans; it does not read. Plain words in JSON schemas ("project", "internal", "token accounting") were classified as secrets → legitimate planner/reviewer crossings refused → regex patched per failure. That loop is the indiscipline the owner named.
- Doc 1 B5.1–B5.5 (intent/meaning/objective extracted **before** redaction, by Solva, frozen, declared-vs-demonstrated, refuse-or-ask) is **not wired** in the inspected crossing. `solva_v2.intent_audit` exists as a record type; nothing at the crossing produces the objective artefact or consumes it downstream.
- **The structural gap underneath both:** the platform has **no contained text-reasoning rung**. Doc 11 A5.1 prescribes a four-rung ladder with local rungs before the frontier rung; Doc 1 B5.2 requires Solva to read the whole question; Mode B forbids the external model from seeing originals. Today the only LLM Solva can reach is the external one. Every "semantic" need was therefore pushed either into regex (Shield categories, hostility rules, `task_separation.REVEAL_CUES`) or to the frontier model. `m9_serving.py` exists as an estate-host loopback serving seam but exposes only `/classify` for admitted adapters. Registered Qwen3 bases exist on both hosts (`base_registration.json`), used only for training.

**Assessment of the enhancement actually ordered (owner §8 items 2 and 4):** provide SyniSense with an estate-owned contained reader (owner's example: latest self-hosted Qwen working with a superior NER) so that, inside the perimeter and before redaction, Solva reads the whole item, produces the frozen objective, recognises Category-3 declarations, and reconstructs the safe item; Category-1 and Category-2 stay deterministic (regex, exact values, patterns, qualified NER); the cue-regex is demoted to the DPO "Generate" step (where cues are useful for drafting declarations), not an enforcer at the crossing. The chokepoint remains the sole external invocation and verifies the sealed safe artefact (mark twice, Doc 16 §7). This is an enhancement of the existing boundary, not a rebuild. Plan WP-01…WP-06.

### A3. The confidentiality register vs. the owner's three categories

| Owner category | Canon mechanism | Current code | Gap |
|---|---|---|---|
| **Cat 1** conventional identifiers (PII/HII/BII/payment) | Doc 1 A3 B21 identifiers removed before crossing; A5.4 recogniser + tenant set must cover what actually occurs; A6 B56 recognition completeness is load-bearing | `deidentifier.py`: regex (Luhn cards, phones, e-mail, IDs) + installed spaCy English NER (transformer→small fallback, offline-only since 5 Oct) + `register` `personal_data` patterns | NER is English-only, breadth/quality unmeasured on estate material; HII/BII coverage not evidenced; no multilingual recogniser; no measured FP/FN |
| **Cat 2** owner-named content, bulk via workbook to a Confidentiality Vault Manager | Doc 2 A3 exact values + patterns; A4 Generate→Review→Edit→Adopt(pending)→Approve(live); A5.1 ONE tenant entity set; A5.4 removal by counter-signed ceremony with countdown (C3 defaults 48 h / 7 d recorded); A5.5 full provenance | `semantic_register.author()` writes **directly into force** ("the DPO act IS the adoption"); `remove()` is immediate; `tenant_entities.py` reads a **separate static catalogue JSON** (presenters/stations/programmes/advertisers) — two stores; no workbook intake route (`/api/shield/register*` has propose/adopt/author/enforcement/delete only) | Lifecycle contradicts A4/A5.1/A5.4; two entity stores violate A6 "one set, one source"; no vault/workbook path |
| **Cat 3** descriptive privileged meaning (contracts, BRDs, audit reports — parties, IP, trade secret, value, status) | Doc 2 A3 category → reasoning-layer recogniser; A5.2 shaping loop yields a testable declaration bound to that recogniser; A5.3 reach shown against measured material | Cue-word regex (`classify` contextual kind) | Not the capability; false positives on ordinary words; no measured reach; no contained reader |

### A4. "Placement — Shield should happen outside LLM processing"

**Reading of the order (interpretation, recorded, not an owner quote):** estate-side protection is a discrete stage that completes and is receipted **before** any external task model processes the item. Today de-identification, register classification and hostility scoring execute *inside* `invoke()` as part of the LLM call. Canon still requires the sole invocation to enforce custody (Doc 1 A5.2/A5.6), so the compliant shape is: Shield stage → sealed safe artefact (safe text, placeholders held locally, frozen objective, receipt) → chokepoint verifies the seal and refuses unsealed payloads (mark twice) → external call. Moving checks out while leaving a bypass would violate, not satisfy, the order. The contained reader is part of Shield (Solva inside the perimeter), not "LLM processing" in the owner's sense.

**Audio (owner: worker converts audio to a spectrum database with biometric content scrapped/modified without harming training quality; derived data not stored with the biometric information):**
- AIP §6: organic/anatomical characteristics (vocal tract length, formant structure, glottal source, F0 range) are biometric and **never registered**; register entries are acquired, shared across ≥N speakers, stored as description not exemplar; embeddings destroyed after clustering; schema cannot represent a voiceprint; invariant harness must fail to store four leakage paths.
- **What `malpha_worker.py` does:** persists per-segment rows with `FEATURES` including `f0_mean_hz`, `f0_std_semitones`, `f0_range_hz` (organic), a 16 kHz PCM store per language, and Mimi codec codes (acoustic codebooks 1–7 carry speaker character); `character_register(rows)` returns percentiles of **every** feature including the organic ones, with no group-size, idiolect or combination check.
- **Existing canon-built boundary bypassed:** `audio_plane_v1/character_register_write_boundary_v1.py::write_character_entry` already refuses SmallStratum, IdiolectMarker, NarrowingCombination, ExemplarStorage and NonLearned entries, with `leakage_path_harness.py`. `training_lab/malpha*.py` imports none of it. This is the concrete instance of "rebuilding instead of enhancing" in the audio plane.
- Codec tokens, group percentiles and the voice identity output gate (`malpha_voice_worker`, max-cosine < 0.40) prove nothing about the **input** derived store. The owner's "3 basis points" is an illustrative thought; any transform must be qualified by speaker-linkage tests (verification EER on the derived data vs. source) and per-language utility tests (listener dev P/R, codec reconstruction, text/voice dev metrics) before adoption. Plan WP-07/WP-08.

### A5. "Design first for all registered requirements, guardrails and ratifications"

Agreed and applied: `EXECUTION_PLAN_20261005.md` is written as requirement → existing owner → mechanism → test → pass for every open row across M1–M10, the five promises and the 31 Mα jobs. Ratification sources indexed in `REQUIREMENTS_RECONCILIATION.md` (C3 batch 13 Sep; pending-ledger flips 15 Sep; Ratification_Record_v1). No settled row is reopened.

### A6. "Clear disc-recorded rule: operate from issued requirements; evolve/ratify on disk; anchor the agent to read before inventing"

`/app/AGENTS.md` records the rule (5 Oct). Gap: nothing mechanical detects drift. WP-00 adds the minimum guardrail: every plan work package carries `Sources:` paths that a test resolves on disk; owner-order files are append-only (section hashes checked); the diagnosis/plan are the first files named in `AGENTS.md`. This is a detector, not a proof that future agents comply.

---

## PART B — Root causes across the whole system (why progress has been slow)

| # | Root cause | Evidence | Where it bites |
|---|---|---|---|
| RC-1 | **Authority drift** — handoffs/plans/green tests treated as requirements | A1 above; handoff "Mocked scorer" after correction; questions asked that canon answers | Every milestone; Shield most visibly |
| RC-2 | **Regex where canon prescribes reasoning** | `semantic_register.classify` contextual cues; `register_gate.HOSTILITY_RULES`; `task_separation.REVEAL_CUES`; `dry_run.py` literal category names | P5 Shield, MA-03/04/05 |
| RC-3 | **No contained inference rung** | `m9_serving` `/classify` only; `solva/reasoning.py` → external; Doc 11 ladder's local rungs for text reasoning never built | P5, P3 (lowest-sufficient-rung routing), P1 (supervisor reasoning), cost deflation |
| RC-4 | **Control-plane continuity** — dispatcher lives in the preview pod cron; pod pauses stop iteration | 21:31→02:26 UTC outage 4–5 Oct, ≈12 GPU-h idle; recurrence risk every pause | P1 autonomous training, owner's "lost unattended GPU time" |
| RC-5 | **Scaffold/capability conflation** | `RealBackend` NotImplemented; `perception/audio_codec/service.py` descriptor-only; `/api/healthz*` unmounted; `m9/capabilities` says audio dormant while Wanga/music admitted; estate reads use Wanga head for all languages | M9, M1, P1, status truth |
| RC-6 | **Independent verification not in place** | 0 native annotations → no listener admission possible; voice/story gates are automated proxies; tests with MOCKED fixtures | MA-14/17, M9, M10 |
| RC-7 | **Governance lifecycle shortcuts** | register adopt-into-force and immediate removal; two entity stores; M7 checker effective before Ledger emission (`checker/state_machine.py:202–208` vs `routers/checker.py:139–152`) | P5, M7 |
| RC-8 | **Sibling implementations instead of extending owners** | `malpha_worker.character_register` vs `audio_plane_v1` write boundary; Mα split/seal logic vs existing collection-schema seams | AIP compliance, maintenance, trust |
| RC-9 | **Economics unmeasured** | no GPU rate card; cost ledger partial (26,107 calls, USD 0.35 partial); principal bill empty; routes `/api/principal/billing/*` 404 in current mount | P3 "fraction of the cost", MA-30, M7 |

---

## PART C — Status by milestone (M1–M10), refreshed 5 Oct

Percentages are the 3 Oct engineering estimates; "Δ since" lists what actually changed. Nothing here is an acceptance score. Since 3 Oct all engineering went to the estate forecast pack and Mα; **no M2–M8 work occurred.**

| M | Estimate | Working (verified) | Open (unchanged unless Δ) | Δ since 3 Oct |
|---|---|---|---|---|
| M1 Registry/deep census | ~85% | Registry, OBS/NAS/SQL intelligence, tiered content census, whole-estate Monte Carlo forecast pack delivered and tested (iter 82) | Measured share ~8.5%; refused-bucket grant; 13-class language register arithmetic assumes 7 classes; forecast caps codes at 12; completion semantics (NAS complete vs 0/16 sources) incoherent; `calibrate()` not a 0–100 score nor wired | Forecast pack delivered 3 Oct; forecast not yet shown in UI; `/api/estate/intelligence/report` path 404 under current mount — verify the live route name before UI binding |
| M2 Watch/Grey Mirror | ~85% | Witness fresh: `placed=true`, 206 passes, last consistent pass 09:45:01 UTC; input-seat deterministic rule detector now scores payload text | Learned/calibrated detection; new-boundary coverage; benign-traffic evidence; freshness acceptance (RC-4) | Freshness finding of 3 Oct resolved for today; recurs whenever the pod pauses |
| M3 Request→delivery | ~70% | DIGICOW extraction, artefact, history, cancellation | Ordinary commissioning/approval/delivery journey, confirmed recipient retrieval, late-rights/recovery; `CUSTODY_GRANT_ORIGIN_UNRULED` still logged at startup for DIGICOW shared_filesystem | none |
| M4 Answers/context | ~75% | Governed multi-turn chat, durable sessions, 200-task evaluation (161/200) | Two-path quality comparison, severe-context/withdrawal, fresh-request continuation | none |
| M5 Memory/collaboration | ~55% **paused** | Sessions/compaction, task/goal/board foundations | Owner pause stands | none |
| M6 Documents/skills | ~85% | DOCX/PPTX/XLSX deterministic builds, QA, downloads, frontier author/review pipeline; estate packs v3–v7 | Grounded callable skill (held by ruling), independent-review closure (`author.compose` can retain disagreement), public `/downloads/` audience vs client custody, legacy install-manifest drift, pre-existing `test_eval1_pptx_hash` failure | none |
| M7 Tenants/rules/commercials | ~45% | Tenant-scoped access, entitlement/usage foundations, cost-ledger rate register with governed authoring (MA-30) | Checker atomicity (effective-before-Ledger), Rules Updates page unwired, licence/catalogue ceremony, provider-key custody, nonempty reconciled bill; billing routes not mounted at the paths previously documented | Rate register added 4 Oct; still empty except a flagged placeholder |
| M8 Recovery | nondeferred scope recorded complete | Interruption/checkpoint restore and countersigned Ledger restore receipts | Owner-deferred site restore and real notification delivery; cross-service failure matrix | none |
| M9 Training/media/models | text-only scope complete; expanded scope incomplete | Admitted 8B text-LID adapters; Wanga-only and music admissions; native signed autopilot; Mα lanes running with supervisor (Solva+CIF) lineage | 13-class dataset/worker/report; generic `RealBackend`; admission-to-consumer routing (Wanga head used for all languages); `m9/capabilities` projection stale; LID serving unloaded since 4 Oct | Mα added real AIP database, Mimi codec qualification, v3 cluster-level seal with verified independence, native-review panel, supervisor; **no model admitted**; two sibling implementations (RC-8) |
| M10 Integrated product + UI | UI partial; independent acceptance ~10% | HTML-bound major screens; Your Agents now renders ARMI overview (16 identities) and routing/rate cards | Six cross-product journeys on one identified build; owner visual acceptance | ARMI surface progressed 4 Oct (was "not available" on 3 Oct) |

---

## PART D — Five promises, refreshed (engineering estimates ±10, not acceptance)

| Promise | 4 Oct | Now | What moved / what blocks |
|---|---|---|---|
| P1 Governed multi-dimensional training | 50% | ~55% | Real AIP database, codec, sealed splits, supervisor and uncapped metering exist and run; blocks: no admission (0 native labels), `RealBackend` unimplemented, non-audio rows (MA-19) not started, 13-class LID unrestored, control-plane continuity (RC-4), audio derived-store privacy unproven (A4) |
| P2 CaaS | 45% | ~50% | Metered CaaS lane and rate freezing (MA-30); blocks: no external principal/app journey (MA-27), no domain offers proven (MA-28), empty bill |
| P3 Right model + excellent affordable output | 50% | ~55% | Measured routing trial `rt-9e6a2c92e8` (MA-08); blocks: no contained rung → ladder's local rungs absent; no blind output comparison (MA-24/25); cost all-in unknown |
| P4 ARMI | 35% | ~50% | Overview/profile/attribution/routing surfaces (MA-29); blocks: onboarding→assign→complete→suspend lifecycle, N2 score contract, Watch W13 separation evidenced |
| P5 Shield control | 40% | **40%** | Register + gate added but are regex (A2/A3); offline NER loader hardened; blocks: contained reader, pre-redaction objective, canonical lifecycle, one entity set, dual-file seam, workbook vault, multilingual NER, independent leak/utility suite. **No increase awarded for MA-04 as built.** |

---

## PART E — Mα 31 jobs, state at 09:52 UTC 5 Oct

States per `M_ALPHA_PLAN.md` §1 vocabulary. "running" claims carry native job IDs above.

| Job | State | Note |
|---|---|---|
| MA-01 traceability | implementing | OWNER_ORDERS, PLAN, RECONCILIATION, this diagnosis; machine check pending (WP-00) |
| MA-02 hardware/rates/uncapped authority | verified_pass (authority) / failed (rates) | `uncapped_until_billing` represented; **no GPU rate card** — money stays unknown |
| MA-03 data/task separation | ready_for_test (narrow) | `task_separation.py` works with regex reconstruction; needs contained reconstruction + full outbound inspection suite |
| MA-04 register exact/pattern/contextual + lifecycle | **failed** | Regex contextual recogniser; lifecycle contradicts Doc 2 A4/A5; two entity stores |
| MA-05 hostility/provenance + sole route | implementing | Deterministic rule detector on payload; learned detection and bypass proof open |
| MA-06 general training commission/worker | implementing | Mα lanes real; generic `RealBackend` NotImplemented; `validate_definition` admits only transcript_text |
| MA-07 durable scheduling | implementing / **blocked** | Lineage-pair validation fixed 5 Oct; continuity across pod pause unsolved (RC-4) |
| MA-08 measured routing | ready_for_test | Trial run; adoption is an operator act; writer/reviewer task sets missing |
| MA-09 audio file → queryable datasets | ready_for_test | AIP db v1 88,850 segments; lineage replay test pending |
| MA-10 real codec | ready_for_test | Mimi 100 tok/s measured; `perception/audio_codec/service.py` still descriptor-only — two implementations |
| MA-11 discoverable spectrum + Character Register | **failed** | Organic features persisted and aggregated; existing write boundary bypassed (A4) |
| MA-12 Outcome/sealed sets | verified_pass (v3 seal, independence verified) | dev remains session-holdout (disclosed) |
| MA-13 calibration 3–4 volumes | planned | not started |
| MA-14 storyteller | running (it.9 text / it.10 voice) | fidelity 0.85/0.81/1.0; identity gate failing all three languages; no native ratings |
| MA-15 invented identity | running | gate < 0.40 unmet (max cosine 0.57–0.61) |
| MA-16 spectral-guided learning comparison | planned | no same-base controlled comparison yet |
| MA-17 listener | running (it.5) | best dev P/R kik 0.94/0.58 · kam 0.83/0.46 · swa 0.66/0.78; recall is the gap; sealed read locked on 0 annotations |
| MA-18 13-language LID | blocked | serving unloaded since 4 Oct; 13-class prerequisites per M1_M10 §A |
| MA-19 non-audio coverage | planned | not started |
| MA-20 callable skills | planned | not started |
| MA-21 WPW Tier 1 | implementing | notebooks attached at commissioning; completeness replay test pending |
| MA-22 WPW Tier 2 | implementing | `malpha_tier2_reports` exists; nine-section skeleton check pending |
| MA-23 WPW Tier 3 | decision_pending | R1/R2/R3 recorded parked |
| MA-24 decks / MA-25 reports | planned | quality references recovered; no blind comparison |
| MA-26 maker-quality interaction | implementing | Train Models shows live runs; full ordinary-user paths unverified |
| MA-27 CaaS customer / MA-28 domain offers | planned | not started |
| MA-29 ARMI | implementing | surfaces exist; lifecycle not proven |
| MA-30 economics | implementing | metering real; rates absent |
| MA-31 independent closure | planned | — |

---

## PART F — Owner actions and decisions genuinely outstanding (not restatements of canon)

| ID | Decision / action | Why it cannot be taken autonomously |
|---|---|---|
| D1 | Control-plane continuity: (a) deploy the control plane so the dispatcher is always-on, or (b) authorise a host-side lane-continuation worker under the same recipe ladder | Infrastructure/placement choice; (b) is a new scheduler the handoff forbade without authority |
| D2 | Nominate native Kikuyu/Kamba/Kiswahili listeners (two per segment) and let me create reviewer identities | Human judgment the system must not fabricate; no listener admission without it |
| D3 | Supply GPU and model rate facts (or authorise using the provider's published list price as a disclosed placeholder) | Money must not be invented |
| D4 | Mode B vs CC1 entity-knowledge unmasked exception: disable, or retain as separately disclosed mode | Existing owner-approved policy; changing it needs the owner |
| D5 | WPW Tier 3 R1 threshold / R2 signatory / R3 novelty | Recorded parked in canon |
| D6 | 13-class LID: English and Maa handling | Ontology decision recorded open in M1_M10 §A |
| D7 | GPU placement for the contained reader: co-reside on akki-vm-ii GPU1 beside the resident 52.7 GB workload (no eviction; measured fit) vs wait for a lane to free | Capacity assignment; default proposed = co-reside after measured fit |

Everything else in the execution plan proceeds under existing authority.
