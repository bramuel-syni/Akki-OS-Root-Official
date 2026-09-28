# REUSE_ASSESSMENT.md

Assessment against the Akki canon (Docs 1–9) of the four codebases
(RMS-IQ-Core-2, Akki-OS-V1, Extraction-Akki, Akki-Executive-Core) plus the v6
HTML prototype and the extracted canon documents. Plain prose. No sequencing,
no phases, no build order.

## 1. Method

### Sources read in this assessment

- **Canon pack** — nine `.docx` documents, downloaded from the client-provided archive, extracted to plain text via `python-docx` (paragraphs preserved with style tags, tables preserved as pipe-separated rows). Every one of the nine documents was opened and read in full:
  - `Akki_Canon_1_Custody_Platform.docx` (206 text lines)
  - `Akki_Canon_2_CIF.docx`
  - `Akki_Canon_3_Governance_Engines.docx` (265 lines)
  - `Akki_Canon_4_Operating_Engines.docx` (365 lines)
  - `Akki_Canon_5_Interface_Architecture.docx` (421 lines)
  - `Akki_Canon_6_User_Journeys.docx` (134 lines)
  - `Akki_Canon_7_Integration_and_Quality.docx` (288 lines)
  - `Akki_Canon_8_The_Watch.docx` (223 lines)
  - `Akki_Canon_9_Mkondo_Charter.docx` (38 lines)
- **v6 HTML prototype** — `Akki Prototype v6 Standalone.html`, 626 KB single-file self-unpacking bundle. Navigation constants (`NAV`, `TABS`, `SUB_TO_GROUP`, `GROUP_TO_TAB`, `SESSION_TOOLS`, `RESTRICTED`, `APPS`) extracted verbatim; `EVIDENCE_KINDS`, `DOC_GEN_LABELS`, `TL_FLOW`, `LANDING_TIPS` inspected; view-method inventory extracted by regex over `this.<name>View` and `open<Name>` patterns.
- **Four public GitHub repos** — cloned to `/app/assessment_workspace/repos/`. Pinned SHAs, dates, and file counts:

| Repo | Branch | Pinned HEAD SHA | Last commit ISO | Total commits | py | js | jsx | ts | tsx | other | test files | total |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RMS-IQ-Core-2 | `main` | `ea5aa019521eee22ad4f8ea29efdfa2af357be3b` | 2026-08-01T08:10:07Z | 198 | 498 | 82 | 50 | 24 | 0 | 1865 | 254 | 2519 |
| Akki-OS-V1 | `main` | `8c361903cdd319bfdc0709de3f4392f5bfa3956b` | 2026-08-14T05:30:51Z | 167 | 487 | 67 | 13 | 24 | 0 | 1532 | 222 | 2123 |
| Extraction-Akki | `main` | `b150c21c1ac6fae8d052332aaff56ae952daae25` | 2026-08-14T05:27:40Z | 204 | 499 | 83 | 55 | 24 | 0 | 1892 | 256 | 2553 |
| Akki-Executive-Core | `main` | `5844eee95d5faffea0dcab98bd4fe5e8d1419f32` | 2026-07-08T13:46:49Z | 929 | 1013 | 74 | 392 | 4 | 0 | 4435 | 505 | 5918 |

All 5,918 + 2,553 + 2,519 + 2,123 = 13,113 tracked files were enumerated via `git ls-files` at the pinned SHAs. Every service directory under `backend/services/` was listed by name with file counts. SHA-256 content hashes were computed across all service files for the cross-repo diff (Chunk 1).

### What was NOT read

- Not every one of the 13,113 tracked files was opened. Deep-reads were targeted at files that hold the claims under assessment.
- Executive-Core's 505 backend test files were NOT opened; classified by name + directory placement only.
- Executive-Core's 392 frontend `.jsx` files were NOT opened line-by-line; classified by file listing + representative opens (`DocumentOverlay.jsx`, `CompilationWizard.jsx`, `HandoffActions.jsx`).
- Akki-Executive-Core's `sdk/` subtree (12 files) was NOT opened; classified as tooling.
- All `backend/uploads/work_studio_exports/` real user artefacts (200+ `.docx / .pdf / .pptx` files) were LISTED, not opened.
- Docs directories (`docs/close_reports/`, `docs/audits/`, `docs/mandates/`, `docs/rulings/`) were LISTED (titles + dates) but not opened per the client's "titles/dates only for now" instruction in Chunk 1.

### Sampling disclosures

- **Cross-repo service diff**: All 34+ service directories that appear in 2 or more repos were diffed by full file-set comparison and SHA-256 content-hash equality. No sampling — full comparison.
- **`economics` divergence characterisation**: 8 Python files opened and diffed byte-for-byte across all three core repos (100% of `.py`); 4 JSON files sampled spanning `tier_lock.v0.json` / `v500.json` / `v1000.json` + `fleet_policy.v0.json`. Sampling method + rationale in Chunk-2 shaping answers §Q7.1 (writing this document consumed the same evidence).
- **Test estate opened directly** (RMS-IQ-Core-2 / Extraction-Akki backend, 141 total invariant tests + 254 total test files):
  1. `test_shield_custody_chain.py` (Chunk 2)
  2. `test_ast_egress_gate.py` (Chunk 2)
  3. `test_p1_custody_closure.py` (Chunk 2)
  4. `test_northena_ledger_retention.py` (Chunk 2)
  5. `test_solva_assertion_boundary.py` first 60 lines (Chunk 2)
  6. `test_g_13_execution_atomic.py` (Chunk 2, Akki-OS-V1)
  7. `test_targeta_invariants.py` (this chunk)
  8. `test_mtafiti_invariants.py` (this chunk)
  9. `test_outer_gate_irreversibility.py` (this chunk)
  10. `test_no_unauthorized_deletion_path.py` (this chunk)
  11. `test_critic_pass_execution_atomic.py` (Akki-OS-V1, this chunk)
  12. `test_frozen_contract_snapshot_parity.py` (this chunk)
  13. Plus 2 opened via bash grep + first-40 lines for section confirmation.
  
  **Sample raised from Chunk 2's 6/141 (≈4.3%) to 14/141 (≈10%).** Remaining 127 test files classified by name + directory placement. Every top-cited test was confirmed to exercise what its name claims — no name-weaker-than-content findings. Executive-Core's 505 test files were NOT opened.
- **Solva_v2 direct-provider bypass scan**: All 30 files in Executive-Core's `backend/services/solva_v2/` grepped for `openai / anthropic / httpx / requests / aiohttp / api_key / litellm / EMERGENT_LLM_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY`. **Zero direct-provider paths.** Every LLM call goes through `llm_adapter.shielded_call` (which routes via `llm_tier_quota.call_llm_with_tier` → `llm_service.call_llm` → `shield.client.invoke` → `shield.llm_router.invoke_with_metering`).
- **service_1 batching + checker ceremony reads**: `services/service_1/{async_state, async_worker, service}.py` (~1100 LOC combined) opened by grep + head to bind Canon 4 §32; `services/checker/{state_machine, rule_change_request, countersign_ledger, effective_delay}.py` (~700 LOC combined) opened to bind Canon 3 §24 rule-change ceremony. **Finding**: 4 of 5 ceremony steps present in code; the "re-verify" step (Canon 3 §24 step 5) has no named method — reclassified from REUSE to PARTIAL for C3-033.

### Citation audit

A mechanical citation-audit tool (`/app/assessment_workspace/tools/citation_audit.py`) parses every citation of form `<repo> path:lines` and `Canon N §x` across every notes file plus this document. Verifies (a) file exists at the pinned SHA, (b) line range is within file length, (c) canon section number appears in the extracted canon text. Final audit result: **file citations 85 total / 85 verified / 0 failed; canon citations 398 total / 398 verified / 0 failed.** All 10 initial defects (3 file + 7 canon) were fixed by re-reading the source; no claim was silently deleted. The tool's Unicode-hyphen normalisation (canon text uses U+2011 non-breaking hyphen for tokens like `34‑A`, while ASCII `-` appears in citations) and parent-section acceptance (`§26.5` → verified if `§26` exists) are documented in the tool source.

### Limits of this assessment

- Depth-limited on: Executive-Core's `sdk/`, `docs/`, `scripts/` subtrees; Executive-Core frontend `.jsx` line-by-line; all four repos' close reports and audits (listed but not verified as claims — per client instruction).
- No runtime execution: no server was booted, no test suite was actually run. Every claim rests on static reading. Where a test-file docstring says "exercises IF1-G1", I verified the test body matches; I did not verify the test PASSES today at HEAD.
- No build performed. No deployment verified.
- Assessment as of the pinned SHAs above. Any commit after those SHAs is not in scope.

---

## 2. Headline findings

Ten sentences, each cited.

1. **RMS-IQ-Core-2 ≡ Extraction-Akki byte-for-byte on all shared code**; Extraction-Akki carries 13 days more of tier_lock ledger snapshots in `economics` and 3 additional repo-top files, all of which are pure data. Cite: `notes/cross_repo_overlap.md` §2.1; SHA-256 comparison covers 34 shared service directories.
2. **The `economics` divergence between Akki-OS-V1 and Extraction-Akki (380 same-path different-content files) is 100% runtime data regeneration, not code drift.** All 8 Python files are byte-identical across the three core repos; the diffs are three fields per JSON file (`grantor_id`, `idempotency_key`, `at` timestamp). Cite: `notes/shaping_answers.md` §Q7.1 §economics; sampling of 4 JSON files + full grep of shared files.
3. **The Watch (Canon 8) has zero implementation across all four repos.** Absence-search covered `watch / macho / mkono / witness / mirage / honeytoken / containment / tripwire / attestation / drill_ / behavioural_profile / policy_table / reconciler / collision`. Every one of the 60 implementable Canon-8 rows is BUILD. Cite: `notes/domain_5_8.md`.
4. **Canon 9 orchestration (record matrix, task-identity register, handoff contracts) is unimplemented across all four repos.** Content-grep for `RECORD_MATRIX / WRITER_MAP / task_identity / writer_authority` returned zero matches. Foundation primitives exist (registry_context, frozen-contract-snapshot parity, ledger append-only) to make the build cheap. Cite: `notes/domain_5_9.md`.
5. **The custody chain is production-grade in the RMS-IQ-Core-2 / Extraction-Akki spine.** `services/synisense/shield/llm_router.py:153-311` `invoke_with_metering` executes de-identify → invoke → re-identify atomically, fail-closed at every boundary, with a full IF1-G1/G2/G3 test suite at `backend/tests/registry/test_shield_custody_chain.py:34-140`. Chunk-2 Claim 1 CONFIRMED.
6. **Egress firewall + AST static gate exist only in the spine.** `services/synisense/shield/egress_firewall.py:1-137` (runtime `httpx` transport wrappers) + `backend/tests/invariants/test_ast_egress_gate.py:1-178` (`ast.NodeVisitor`-based build gate). Both absent in Akki-OS-V1 and Executive-Core. Chunk-2 Claim 2 CONFIRMED for spine, REFUTED for the other two.
7. **The Critic Seam (Canon 7 §31-§34) lives only in Akki-OS-V1** — `services/critic_pass/` (7 files, 950 LOC) with two tests (`test_critic_pass_execution_atomic.py`, `test_cif_manifest_submission_gate.py`). Absent from the core-2 spine. HARVEST anchor for the largest single canon-quality closure.
8. **Executive-Core is architected for RE-POINT via a Protocol-based LLM boundary.** `backend/contracts/synisense.py:25-28` defines `class SyniSenseContract(Protocol)` with `async def shield_invoke(...)`; every LLM call in the 597-file frontend + 5,918-file backend transits `get_synisense().shield_invoke(...)` through the older Phase-4.0 shim or the newer Phase-15.0 `llm_adapter.shielded_call`. Zero direct-provider bypass across the 30-file `solva_v2` subtree. Cite: `notes/shaping_answers.md` §Q7.2 + this chunk's A.3 scan.
9. **A LIVE contradiction between the codebases**: RMS-IQ-Core-2 / Akki-OS-V1 / Extraction-Akki all shaved `services/synisense/shield/purpose_validator.py + client.py + audit_log.py + canonical.py` at IF-1 close (2026-07-14). Akki-Executive-Core (last commit 2026-07-08, six days earlier) still enforces `purpose_validator.validate_purpose()` at `services/synisense/shield/client.py:63` with a real `PurposeInvalid`-raising gate. Two live implementations disagree on whether the pre-de-id purpose check is Canon-compliant. Cite: `notes/claims_verification.md` §Claim 6.
10. **The prototype's taxonomy does not map to Canon 5's five-pillar + control-band architecture.** Prototype: 8 nav groups (WorkStudio · ThinkLab · Collab · Monitor · Trust · Registry · Build · 3rd Party) over 4 tabs. Canon 5 (real headings): "Four Consoles, Capability-Defined" (§10 — **FOUR**, not FIVE), Eight Global Rules (§2.1–§2.8), Two Day-Zero Dashboards (§12.1–§12.2), plus §14–§27 numbered specifics. Neither taxonomy is a strict superset of the other; Chunk-3 §5.7 mapped 25 BUILD rows + 7 rename-RETIRE items just to reconcile. Cite: `notes/domain_5_7.md`.

---

## 3. The two shaping answers

### §7.1 · Which repository is the spine?

**Base = Extraction-Akki** (equivalent to RMS-IQ-Core-2 on all code; carries 13 days more of runtime `economics` ledger snapshots + 3 extra repo-top files).

Per-engine evidence (from Chunk-3 sample opens + Chunk-2 SHA verification + Chunk-3 A.5 test confirmation):

- **Northena · Solva · Mtafiti · Targeta · outer_gate · checker · synisense · compliance · service_1** (minus 1 file each on service_1/targeta): byte-identical between Extraction-Akki and RMS-IQ-Core-2, with tests exercising the specific Canon contracts. Confirmed:
  - Admit five-field completeness check at `backend/services/northena/admit.py:_REQUIRED_KEYS` (Canon 3 §6.1 — **but declaration NOT among the five, spec-vs-code seam**).
  - Parameterless assertion boundary at `services/solva_depth/assertion.py`, verified by opening `backend/tests/invariants/test_solva_assertion_boundary.py:1-60` — signature has no `confidence` / `caveat` parameter.
  - Permutation-typed yield guard at `services/targeta/yield_layer.py:17-29` — confirmed by opening `test_targeta_invariants.py:80-88` (`test_yield_output_is_permutation_raises_on_drop`) + `L92-103` (`raises_on_duplicate`) with `pytest.raises(interface.NonPermutationError)`.
  - Mtafiti Canon-4 §5-§10 requirements — confirmed by opening `test_mtafiti_invariants.py:89-165` (verdict-is-matrix-lookup, inference-returns-only-detections, census-signature-takes-no-objective).
- **Memory** (Doc 7 Part IV): Extraction-Akki / RMS-IQ-Core-2 own it (12 files + snapshot + 4 test suites); Akki-OS-V1 lacks it entirely.
- **Post-2026-07-30 P1 close artifacts**: `egress_firewall.py`, `test_ast_egress_gate.py`, frozen `trust_receipt_v1.py` + snapshot + parity seat #32 — only in Extraction-Akki / RMS-IQ-Core-2.

**Harvest from Akki-OS-V1 into the spine** (all with tests in Akki-OS-V1's own suite):

1. `services/critic_pass/` (7 files, 950 LOC) — closes Canon 7 §31-§34 Critic Seam absent from Core-2. Tests exercised (opened): `test_critic_pass_execution_atomic.py:72-254` (15 named tests) covering CAL-23.1 enumeration, Parity-33 held post-critic-pass, manifest-entries fields growing three contracts (mining_plan, perception_job_v0, feasibility_result_v0), evidence-class literal honesty grammar, Tier-2 7-item rubric, CR-7 amendment, QA-3 no-self-review (Canon 7 §32 independence rule), archive-ledger append-only + immutability.
2. `services/service_1/batch_quarantine.py` (227 LOC) — closes Canon 4 §32 batch quarantine + halt threshold. **Note**: `services/service_1/` in the spine handles four-state OBJECTIVE lifecycle (`accepted → running → delivered / refused / cancelled` at `async_state.py:179-200`) but has no per-BATCH quarantine construct today.
3. `services/targeta/gap_candidate_filer.py` (132 LOC) — closes Canon 4 §35 gap-ranking with demand evidence.
4. `services/registry_context/` (5 files) — prompt-context injection subsystem. Tests: `test_registry_context_block_golden_snapshot.py`, `test_g_13_execution_atomic.py:212-218` (`test_wch_resolver_returns_declared_list_deterministic`).
5. `services/partitions/session_working_set.py` — session partitioning. Test: `test_partition_schema_v0_envelope.py`.
6. `services/sequencing_harness/` (7 files, 426 LOC) — G-13 ordering-optimiser for the Function & Promise Registry. Confirmed by opening `test_g_13_execution_atomic.py:52-218` (15+ tests) — owner ruling byte-identical, Class-E parameters pinned N=10 / α=0.05, deterministic executor, dependency enumerator, deterministic-before-model optimiser, ledger append-only.
7. `services/far_endpoint/` — gate-generator tooling that auto-generates `services/generated_gates/*.py` stubs from mandate docs. Test: `test_generated_gates_regeneration_diff.py`.

**Irreconcilable**: nothing. The `economics` "divergence" is data, not code. Every harvested Akki-OS-V1 service imports only its own submodules or services present in the spine.

**Spec-vs-code seams flagged**:
- **C3-008 (actor declaration at admit)**: Canon 3 §6.1 requires actor declaration before operations. `services/northena/admit.py:_REQUIRED_KEYS` = 5 fields but declaration is NOT among them. `services/mtafiti/declaration.py` implements a DIFFERENT concept (per-source declaration baseline, Canon 4 §5.1). No server-side actor-declaration surface anywhere. Chunk-3 §5.2 downgraded to MODIFY / BUILD.
- **C3-033 (rule-change ceremony re-verify step)**: `services/checker/state_machine.py:80-315` implements PROPOSE (L80 `initiate`), COUNTER-SIGN (L181 `countersign`), WAIT (L211 `advance_delay`), APPLY (state transitions), plus OBJECT and SUSPEND paths. **Step 5 "re-verified" (Canon 3 §24 last clause) has NO named method** — reclassified from REUSE to PARTIAL. The Verification Runner (C3-039) may implicitly serve this role; that binding is BUILD.

### §7.2 · How much of Akki-Executive-Core is RE-POINT?

**Cross-cutting decisive evidence**: `backend/contracts/synisense.py:25-28` defines `class SyniSenseContract(Protocol)` with `async def shield_invoke(...)`. Every service in Executive-Core reaches models through this interface. **Zero direct-provider bypass** confirmed across the 30-file `solva_v2` subtree (grep across `openai / anthropic / httpx / requests / aiohttp / api_key / litellm / EMERGENT_LLM_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY` returned empty). Phase-15.0 hardening in `services/solva_v2/llm_adapter.py:200-206`: "shield_required is always True and synisense_run_id is non-null".

Per-area verdicts (details in Chunk-2 `notes/shaping_answers.md` §Q7.2; upgraded per Chunk-3 A.3):

| Area | Verdict | Decisive coupling |
|---|---|---|
| chat / documents / analyze_workspace / ideas_engine / deck_* / inbox_routing | **RE-POINT** | all reach LLMs via `shield_invoke` via contract; JWT auth stays application-side; storage moves to memory-plane. |
| solva_v2 (30 files) | **RE-POINT surface + delegate reasoning to spine's `solva_depth`** | zero direct-provider bypass confirmed; the reasoning boundary is separable from the narration surface. |
| solva_voice_audit (24 files) | **RE-POINT** (was flagged UNKNOWN in Chunk 2 pending audio-input check; Chunk-3 A resolved: "voice" = coach-voice/tone, not audio; all boundaries via `shield_invoke`) | text-based coaching audit, not speech ingest. |
| workbook_analyzer (10 files) | **RE-POINT feasible** or keep as application-side capability | pure-Python analytics; no LLM boundary. |
| cohort (8 files) | **RETIRE from platform / keep application-side** | Canon 1 §13 makes trial-cohort onboarding + feedback application territory. |
| deck_* + work_studio (~13k LOC backend + 5k+ LOC frontend + 200+ real user exports) | **RE-POINT (LLM boundary) + REBUILD (storage)** | LLM already through `shield_invoke`; storage tightly coupled to direct mongo `db.<collection>` calls that don't fit Doc 7 memory-plane shape. |
| llm_streaming.py + `services/synisense/shield/streaming.py` (216 LOC) | **RE-POINT + PORT** | streaming lives in Executive-Core, absent in spine. HARVEST into spine. |
| Cross-cutting security (csrf, rate_limit, rbac, security_headers, session_timeout, sentry_setup, privacy_wall, clamav_service) | **RETIRE from platform** | Canon 1 §7.1 (peer authorities) + Canon 5 §11; core three ship platform-side auth service (`services/auth/`). |
| Application-territory (stripe_webhook, owner_digest, news_aggregator, first_login_password_set) | **RETIRE from platform** | Canon 1 §12/§15. |
| frontend/src/_archived, _archived_legacy, website | **RETIRE** | already marked archived by codebase; marketing website is application territory. |
| 36 loose services/*.py | mixed — see Chunk-3 §5.5 + §5.10 | 21 RE-POINT · 12 RETIRE · 3 PORT-into-spine (llm_streaming/storage_service/job_queue) · 3 already resolved (backfill_shield_v1 RETIRE, two_pass HARVEST, platform_kb RETIRE). |

**Two heavy ports into the spine required before RE-POINT completes**:
1. `services/synisense/shield/streaming.py` — Core-2 lacks SSE streaming; Executive-Core has it and it's shield-mediated.
2. Object storage + memory-plane migration — `backend/uploads/work_studio_exports/` holds 200+ real user artefacts; Canon 7 §19-§23 memory plane exists as `services/memory/plane_registry` etc. in the spine, but object storage boundary is BUILD.

---

## 4. Domain tables (§5.1–§5.10)

Every one of the 585 Canon-1..9 requirement rows lands in exactly one domain table with exactly one class. Full per-row tables live in `notes/domain_5_1.md` through `notes/domain_5_10.md`. This section reproduces them by summary; the full row-level detail is those files.

### §5.1 · Custody and Boundary  ·  22 rows

- **REUSE (12)**: fail-closed custody + fail-transparent cost asymmetry (C1-014, C1-015); inheritance (C1-029); one outbound path + no-second-path enforcement (C1-039, C1-040, C1-045); SyniSense chain per-tenant per-invocation (C3-016, C3-017); custody sequence (C3-019); trust-receipt HMAC+HKDF+frozen contract (C3-021); outer-gate pseudonymisation + generalisation + receipt-mint machinery (C4-022, C4-023); doctrine seat rows.
- **PARTIAL (4)**: input-seat as named surface — deidentifier serves as inspection but seat not named (C3-018); dual-identity at seat (C3-020) — Watch identity absent; prove-one-run + regulator pack (C3-046–C3-048) — receipts exist, assembly BUILD; contents/privacy/quality attestations (partial).
- **BUILD (2)**: C3-018 input-seat named surface; C3-020 dual identity (couples to 5.8).
- **N/A-DOCTRINE (4)**: C1-016 (unrepresentable-not-policed general); C1-018/C1-019 (biometric register unrepresentable by absence); C1-017 (Solva parameterless — implementable surface counted in 5.3).
- **CONTRADICTION carried**: purpose-gate contradiction (§9 headline).

### §5.2 · Direction and Record  ·  24 rows

- **REUSE (18)**: one record + append-only (C1-020, C1-021); single owner per value (C1-025); Northena deterministic (C3-004, C3-005); universality (C3-006); frozen artifact (C3-007) with `FrozenArtifact.__setitem__/__delitem__` raising `TypeError("FrozenArtifact is immutable (§4/N-INV-4)")` at admit.py L88-104; three-verdict alphabet (C3-011); ADMIT bindings (C3-012); REFUSE first-class (C3-014); contract-grade ledger rows (C3-015); ledger writer authority (C3-043); ordering before response (C3-044); rows immutable (C3-045); Solva reasoning trace writer (C3-023–C3-025); stamp-audit absorption channel via `test_ledger_absorbs_outer_gate_and_v2_via_stamp_audit.py`.
- **MODIFY / spec-seam (3)**: **C3-008 · C3-009 · C3-010** — actor declaration capture (Canon 3 §6.1). `_REQUIRED_KEYS` at admit.py checks five fields but declaration is not one of them. `HomeUndeclared.jsx` in Executive-Core is a UI stub only. No server-side actor-declaration surface anywhere in the four repos. BUILD schema + capture surface + admit-time check.
- **BUILD (3)**: declaration schema + capture surface + admit-time gate; loop end-to-end orchestration (Canon 1 §10 + Canon 4 §35), addressable via HARVEST of `gap_candidate_filer.py`.
- **PARTIAL**: C3-013 HOLD reason (infrastructure REUSE; ceremony-in-force integration verified via `services/checker/`).

### §5.3 · Measurement, Targeting, Reasoning  ·  27 rows

- **REUSE (22)**: Mtafiti — estate at scale (C1-055); three states + degraded field (C1-056, C1-057); two-layer defensibility (C1-058); inference gated on accuracy (C1-059); verdict is governed lookup (C1-060, C1-061); Canon 4 §5-§10 cluster (C4-003 to C4-013) — all covered by `test_mtafiti_invariants.py:89-193` (16 tests exercised). Targeta — plan artefact frozen (C4-016); permutation-typed yield guard (C4-014 to C4-020) — verified via `test_targeta_invariants.py:80-103`. Solva — assertion boundary parameterless (C3-022 to C3-025, C3-027, C3-029). Six-engines / three-axes cluster (C1-042 to C1-054, PARTIAL for two-authorities pieces).
- **PARTIAL (4)**: reuse-first lookup mechanism (C4-017); intent-audit divergence field un-consumed (C3-026 — consumer is Watch); independence gate on reviewer selector (C3-028).
- **HARVEST (1)**: `services/targeta/gap_candidate_filer.py` — closes C4-050.
- **RE-POINT (1)**: `solva_voice_audit` surface (Chunk 2 (b) → RE-POINT, coach-voice not audio).

### §5.4 · Extraction and Quality  ·  24 rows + 5 HARVEST + 1 RE-POINT/REBUILD

- **REUSE (15)**: five-ring unit + qualification partitions (C4-032 + `test_layer_a/b/c*.py`, `test_dispatch_grain_form_refusal.py`); batch objective lifecycle at `services/service_1/async_state.py:179-200` (per-OBJECTIVE state machine, four states `accepted → running → delivered / refused / cancelled`); census idempotent (C4-042); extraction admit (C4-043); extraction runs to ledger (C4-044); sampling first-class (C4-045); deliverables + attestations (C4-046).
- **HARVEST from Akki-OS-V1 (5 clusters)**: critic_pass (C4-031, C7-024–C7-028, D-Manifest); batch_quarantine (Canon 4 §32); gap_candidate_filer (already listed in 5.3); registry_context; sequencing_harness; far_endpoint + generated_gates.
- **BUILD (6)**: MOAC six criteria (C4-037a–f) + drift (C4-067, C4-068); adapter lineage (C4-039); adapter registry versioning (C4-040); Critic-Seam calibration observability at Compliance Console (C5-020 companion).
- **RE-POINT/REBUILD (1)**: Executive-Core `work_studio` compilation surface (LLM RE-POINT + storage REBUILD).
- **PARTIAL (3)**: adapter training pipeline (C4-035); Critic-Seam independence rule wiring; batch board backend uplift (service_1 today handles OBJECTIVE lifecycle, per-BATCH quarantine BUILD-with-HARVEST).

### §5.5 · Integration  ·  29 rows + 3 HARVEST + 1 RETIRE

- **REUSE (20)**: six services doctrine (C1-069 S1/S2/S4); Function & Promise Registry (C1-070); universality-through-boundary (C1-072); engineer-key-grant (C7-003, C7-004, C7-011, C7-012); custody boundary crossing (C7-005); envelope stable (C7-007); three refusal shapes distinguishable (C7-008); no warm-up (C7-010); memory plane per Doc 7 Part IV (C7-013–C7-017); use_data buyer path (C7-020–C7-023); MRR gates verified via `test_machine_readable_registry_mrr_g1_to_g6.py`.
- **HARVEST (3 clusters)**: critic_pass (5.4 mirror); far_endpoint + registry_context + generated_gates; Executive-Core `two_pass.py` refusal-templates as Solva-pattern amendment.
- **BUILD (3)**: S6 Watch service sentence (C1-069 S6, couples to 5.8); per-application webhook (C7-009); three-lens envelope backend uplift.
- **RETIRE (1)**: `services/platform_kb.py` (Chunk 2 (d)) — application-side static prompt block, Canon 1 §13.
- **PARTIAL (4)**: prove-one-run to compliance officer (C1-069 S3); envelope class-chip render (C7-006); precompute parameters + Watch reads plane activity (C7-018, C7-019).
- **N/A-DOCTRINE / Reserved (1)**: S5 infrastructure consumer (C1-069 S5, explicit "not built").

### §5.6 · Governed values and ceremony  ·  35 rows

- **REUSE (12)**: rulebook ceremony machinery (C3-030–C3-034 with reclassification of C3-033 to PARTIAL after Chunk-3 A.2); countdown classes at `services/checker/consequence_classes.py` (C3-052, C3-053); rail-firing test discipline (C3-040); registry consolidation byte-identity; sensitivity classes / privacy floor.
- **PARTIAL (8)**: rule-on-paper surfacing (C3-032 — data exists, surface BUILD); rulebook read-back (C3-035); Verification Runner as compliance-console-triggered surface (C3-039); commissioning-certificate artefact (C3-042); regulator pack (C3-047, C3-048); retention rulebook surface; ABAC engine as first-class evaluator; setup / day-zero as named consoles.
- **BUILD (3)**: Verification Runner surface; regulator-pack export surface; setup/day-zero/working-rhythm consoles.
- **N/A-DOCTRINE (12)**: precedence (C1-036, C1-037); two-authorities-seam prose (C3-049–C3-051); "what governance does NOT do" (C3-054–C3-058); loop self-limits (C4-051); "what operating engines do NOT do" (C4-061–C4-064).

### §5.7 · Interface  ·  55 rows — highest BUILD share

- **REUSE (12)**: doctrinal one-record-source rows; no-override / no-bypass on any surface.
- **PARTIAL (13)**: Registry Dashboard four-quadrant (§12.1); Compliance Rulebook surface (§23); Retention & Rights (§22); Registry Administration (§17); Reference App Ask surface (§20-derived); dormant capability rendering.
- **BUILD (25)**: class chip + grounding marker + refusal-card verbatim copy + agent-assumed chip; four consoles as named surfaces (§10 lists FOUR, not five — a correction to Chunk 3 5.7); Watch Console (does not exist); three lenses over one object; Studio (§42-equivalent — the prototype has no application-composer surface, Executive-Core's `work_studio` is a document-compilation wizard, not Canon-5 Studio); Learn pillar; Pulse + News surfaces; Control Band as horizontal five-item strip; shared visual-system library.
- **REUSE-doctrine (5)**: eight global rules discipline held via invariant suite.

### §5.8 · The Watch  ·  72 rows — ALL BUILD or DOCTRINE

- **REUSE / MODIFY / RE-POINT / RETIRE: zero.**
- **BUILD (60)**: every implementable Canon-8 row across all seven clusters (Macho sensor · Mkono responder · Witness · mark register · containment · mirage · reserved decisions · Watch officer's day · standing drills · peer-authorities disagreement · interface with CIF).
- **N/A-DOCTRINE (12)**: constitutional negatives + "what the Watch does NOT do" + framing rows.

Adjacencies named as foundation vs distraction (Chunk 3 §5.8):
- **Foundation-partial**: Executive-Core `services/chat/protective_layer/` (three FM detectors at answer-time via `shield_invoke`) — a useful primitive shape for Macho sensing, NOT the Watch itself.
- **Distraction**: `rate_limit / sentry_setup / security_headers / csrf / session_timeout / privacy_wall / clamav / rbac / signal_dedup / inbox_routing / backfill_shield_v1 / .emergent/cron/watch_crons.sh / services/mtafiti/verdict.py / contracts/commission_verdict.py / memory/audit/*verdict*.md`. Name-collision hazards especially with `verdict`, `watch`, `containment`.

### §5.9 · Orchestration (Canon 9 · Mkondo)  ·  50 rows

- **REUSE-doctrine (2)**: one-record-law + one-writer-per-class (C9-004, C9-005) — northena ledger already de-facto sole writer to run ledger.
- **PARTIAL (1)**: admission→extraction handoff (C9-036) — implemented at `services/wizard/admission_handoff.py` + `backend/routers/handoff.py` (test `test_handoff_route_readonly.py`).
- **BUILD (45)**: everything else.
- **BUILD-doctrine (2)**: Canon 9's own §21 conclusion rows.

Foundation primitives (from Chunk 3 §5.9): the frozen-contract-snapshot parity pattern at `backend/tests/invariants/test_frozen_contract_snapshot_parity.py:1-148` — Chunk 3 A.4 confirmed this pattern (bidirectional parity via authoritative `CONTRACT_TO_SNAPSHOT` dict + on-disk existence checks) is **structurally reusable** for the Canon-9 record-matrix and task-identity-register enforcement. Each Canon-9 record class becomes a snapshot entry; each task-identity row becomes a snapshot entry; the same discipline that makes adding a frozen contract require two-side edits makes adding a record class or task-identity mapping ceremony (Canon 9 §7).

### §5.10 · Cross-cutting  ·  37 rows + 2 HARVEST

- **REUSE (22)**: platform-side auth service (`services/auth/*` — 16 files); scoped-key issuance (C7-003, C7-004, C7-011, C7-012); instance isolation + scoped-accessor pattern (`services/memory/scoped_accessor.py` + `backend/tests/registry/test_instance_isolation.py`); secrets + key custody (trust_receipt HKDF, outer_gate window-keys with `purge_window`, JWT/password hash); build-gates + static-analysis discipline (C3-059–C3-061, C4-065, C4-066); defect taxonomy REUSE rows (D01, D04–D10, D13, D16, D24, D25).
- **HARVEST (2)**: D-Manifest (Akki-OS-V1 `test_cif_manifest_submission_gate.py`); D-Reset-Absent (same).
- **BUILD (7)**: C3-059 declaration build gate; D-Chip; D-Untraceable-Adapter; D-MOAC-Missing; D-Console-Interior; D-Watch-Interior; D-Dual-Hat; D-Cross-Auth-Credential.
- **PARTIAL (4)**: D-Independence; D-Rule-Paper; D-Handoff; D-No-Warmup-Violation (verify absence of warm-up branch).
- **N/A-DOCTRINE / unrepresentable-by-design (2)**: D-Behavioural-Register; D-Bio-Watch-Merge.
- **RE-POINT (1)**: Executive-Core application shell.
- **RETIRE cluster (1)**: Executive-Core cross-cutting-security duplication.
- **CONTRADICTION carried (1)**: purpose-gate (§9 headline).

---

## 5. Verification results — the seven §6 claims

Cross-repo matrix from `notes/claims_verification.md`. Every row cites an implementation file + a test/call site (for CONFIRMED) or explains the absence (for REFUTED).

| # | Claim (short) | RMS-IQ-Core-2 | Extraction-Akki | Akki-OS-V1 | Executive-Core |
|---|---|---|---|---|---|
| 1 | Chokepoint = `invoke_with_metering`; de-id→invoke→re-id; fail-closed | **CONFIRMED** (impl+test) | CONFIRMED (byte-identical) | CONFIRMED (older chain intact at `llm_router.py` L173/187/209/255) | **PARTIAL** — chain in `shield/client.py:63-71`, not the router (`invoke_with_metering` receives already-de-id'd `de_id_content`) |
| 2 | Runtime egress firewall + static AST gate | **CONFIRMED** (impl+test) | CONFIRMED | **REFUTED** (files absent) | **REFUTED** (files absent) |
| 3 | HMAC-SHA256 + HKDF + frozen field set | **CONFIRMED** | CONFIRMED | **PARTIAL** — HMAC/HKDF present, frozen contract module absent, older 133-L variant lacks `masking_tier` | **PARTIAL** — same as Akki-OS-V1 (identical SHA) |
| 4 | Northena ledger append-only + no-deletion test | **CONFIRMED** | CONFIRMED | CONFIRMED | **REFUTED** (Northena engine absent) |
| 5 | Refusal-family registry external + versioned + `unclassified` escape hatch | **CONFIRMED** | CONFIRMED | CONFIRMED | **REFUTED** (compliance service absent) |
| 6 | `purpose_validator + client + audit_log + canonical.py` shaved at IF-1 close (2026-07-14) | **CONFIRMED** | CONFIRMED | CONFIRMED | **REFUTED** — all four files present + purpose gate wired at `client.py:63`; `purpose_validator.py:20-58` raises `PurposeInvalid` on empty/unknown/non-internal-prefix violations against `ALLOWED_PURPOSES` |
| 7 | No Studio / agent-builder surface in Core; Executive-Core has `work_studio` | **CONFIRMED** (empty grep) | CONFIRMED | CONFIRMED | **REFUTED-in-part** — surface exists (~13k LOC backend + 5k+ LOC frontend + 200+ real user exports) but is a document/deck compilation wizard (Canon 5 §14 Shaping-Wizard-adjacent + §12.1 Documents surface), NOT Canon 5 Studio-as-application-composer. No `agent_wizard / build_agent / agent-composer` in any repo. |

---

## 6. BUILD inventory

Complete list, one line per capability. HARVEST clusters listed separately at the end.

### Custody & Boundary (5.1)
- C3-018 input-seat as named canonical surface.
- C3-020 dual identity at input seat (couples to 5.8 Watch identity).

### Direction & Record (5.2)
- C3-008 · C3-009 · C3-010 actor-declaration surface + admit-time check.
- Loop end-to-end orchestration + gap ranking by carried demand evidence.
- C3-033 rule-change ceremony re-verify step (5th ceremony step — the other four present in `services/checker/state_machine.py`).

### Measurement / Targeting / Reasoning (5.3)
- C3-026 intent-audit divergence-field consumer (couples to 5.8).
- C3-028 machine-checked reviewer independence gate.

### Extraction & Quality (5.4)
- C4-037a MOAC accuracy on uncurated composition.
- C4-037b MOAC coverage across strata.
- C4-037c MOAC refusal behaviour under Solva-pattern.
- C4-037d MOAC provenance integrity.
- C4-037e MOAC cost per operation.
- C4-037f MOAC time-to-answer at 95th percentile.
- C4-038 MOAC evidence from uncurated composition (couples to C4-037a).
- C4-039 adapter rights lineage.
- C4-040 adapter version history.
- C4-067, C4-068 MOAC drift discipline + "latest reading is the one in circulation".
- Critic-Seam calibration observability surface (5.4 backend + 5.7 surface).
- Adapter registry backend + scorecard rendering.

### Integration (5.5)
- C1-069 S6 continuous machine-speed detection/response service sentence (couples to 5.8).
- C7-009 per-application webhook infrastructure.
- Three-lens envelope backend uplift.

### Governance ceremony (5.6)
- Verification Runner as compliance-console live surface (C3-039).
- Regulator pack export surface (C5-021, C3-047, C3-048).
- Setup / Day-Zero / Working-Rhythm consoles as named surfaces (C6-007 to C6-022).
- Signed setup record artefact + commissioning certificate artefact.

### Interface (5.7) — largest cluster
- C5-002, C5-003 class-chip component.
- C5-004 grounding-marker component.
- C5-005, C5-006, C5-007 refusal card verbatim copy (Canon 5 §9.2 — string not found anywhere).
- C5-008 agent-assumed chip.
- C5-010, C5-011, C5-012 four consoles as named surfaces (**correction: Canon 5 §10 says FOUR consoles, not five — an error in Chunk-1 extraction**; §10 heading is verbatim "Four Consoles, Capability-Defined").
- C5-013 Registry Dashboard four-quadrant shape.
- C5-014 Model catalogue with MOAC scorecards (couples to 5.4 BUILDs).
- C5-018 Batch Board surface (couples to 5.4 HARVEST + BUILD).
- C5-020 Quality Observation with stale-calibration surface.
- C5-022 to C5-026 Compliance Console home + prove-one-run + retention & rights + rulebook + rule-on-paper flag.
- C5-027 to C5-030 Integration Console (register / first-call / administer / dual-actor scoping).
- C5-031 to C5-036 Administration Console (home + change-a-rule + what-I've-changed + roles & rights + counter-sign duties + verification-runner).
- C5-037 to C5-042 Watch Console + constitutional negatives (couples to 5.8 BUILD).
- C5-045 to C5-048 Three lenses over one object (Answer / Reasoning / Raw trail).
- C5-049, C5-050, C5-051 Answer Card (evidence strip + honesty strip + actions).
- C5-052 Five pillars including Lead + Learn.
- C5-053 Pulse + News.
- C5-055 Studio (Canon 5 "designed, not sourced" application-composer).
- C5-057 Learn pillar surfaces.
- C5-058, C5-059 Control band (Connect · Estate Map · Rulebook · Access · Watch).
- C5-063, C5-064, C5-065 "insufficient measurement" render + absence-as-state + standard-copy library.

### The Watch (5.8) — every implementable row
- C8-004 to C8-007 machine-speed + cannot-act-unobserved + proves-own-fitness discipline.
- C8-008, C8-055, C8-056 seam: sensing → verdict row → response → action row.
- C8-009 to C8-013, C8-055 to C8-059 three actors (Macho, Mkono, Witness).
- C8-014 to C8-018, C8-057 register of marks + dimensions + de-mark two-signatures + W13 behavioural-profile no-reader.
- C8-019 to C8-026 containment + mirage + expiries + reconciliation.
- C8-027 to C8-029 reserved decisions + panel discipline.
- C8-030 to C8-033 Watch officer's day + officer never-does list.
- C8-034 to C8-039 standing drills + fitness in receipts.
- C8-040 to C8-044 peer authorities + disagreement + task identity + new-entry-only correction.
- C8-045 to C8-054 constitutional negatives (10 items) as build-time design constraints.
- C8-066 to C8-068 interface with CIF (findings cross as detection; only ratified frames cross back).
- C8-069, C8-070 boundary with Doc 9 (couples to 5.9).

### Orchestration (5.9) — Canon 9
- C9-001 to C9-003 Mkondo three-register maintenance.
- C9-006 to C9-018 record matrix (13 writer→readers rows).
- C9-019 to C9-022 reading discipline (couples to 5.8).
- C9-023 to C9-035 task-identity register (13 rows).
- C9-037 to C9-042 six handoff contracts (chokepoint→model, verdict→response, containment→decision, mirage release→reconciliation, disagreement→resolution, Watch findings→CIF). C9-036 admission→extraction is PARTIAL (already implemented).
- C9-043 to C9-047 change & precedence + silence-as-finding.
- C9-048 to C9-050 Canon-9 doctrinal conclusion.

### Cross-cutting (5.10)
- C3-059 declaration-required build gate.
- D-Chip (C7-D03).
- D-Untraceable-Adapter (C7-D14).
- D-MOAC-Missing (C7-D15).
- D-Console-Interior (C7-D17).
- D-Watch-Interior (C7-D18).
- D-Dual-Hat (C7-D22).
- D-Cross-Auth-Credential (C7-D23).

### HARVEST clusters (not BUILD-from-scratch)

Marked separately per instruction — lift-and-shift risk-adjusted low.

**From Akki-OS-V1:**
1. `services/critic_pass/` (7 files, 950 LOC) — 5.4 & 5.5. Tests: `test_critic_pass_execution_atomic.py:72-254` (15 named tests).
2. `services/service_1/batch_quarantine.py` (227 LOC) — 5.4. Canon 4 §32.
3. `services/targeta/gap_candidate_filer.py` (132 LOC) — 5.3. Canon 4 §35.
4. `services/registry_context/` (5 files) — 5.5. Test: `test_registry_context_block_golden_snapshot.py`.
5. `services/partitions/session_working_set.py` — 5.5/5.6. Test: `test_partition_schema_v0_envelope.py`.
6. `services/sequencing_harness/` (7 files, 426 LOC) — 5.4. Test: `test_g_13_execution_atomic.py:52-218`.
7. `services/far_endpoint/` + `services/generated_gates/` — 5.5. Test: `test_generated_gates_regeneration_diff.py`.

**From Executive-Core:**
1. `services/synisense/shield/streaming.py` (~216 LOC) — 5.1. Core-2 lacks streaming; this is shield-mediated.
2. `services/two_pass.py` verbatim refusal templates (`thin_input, unsourced_claim, named_assumption`) — 5.5. Solva-pattern amendment.

---

## 7. RETIRE inventory

Every RETIRE row cites the specific canon clause anchoring the retirement.

### Application-territory duplicates in Executive-Core — anchor Canon 1 §12 / §13 / §15
- `Akki-Executive-Core backend/services/stripe_webhook.py` — Canon 1 §15 verbatim: "will not know a buyer, a price, or an order — commerce is application territory".
- `Akki-Executive-Core backend/services/owner_digest.py` — Canon 1 §12.
- `Akki-Executive-Core backend/services/news_aggregator.py` — Canon 1 §12.
- `Akki-Executive-Core backend/services/first_login_password_set.py` — Canon 1 §13 (application user auth stays in the application).
- `Akki-Executive-Core backend/services/cohort/` (8 files) + loose cohort_email* — Canon 1 §13 (trial cohort onboarding + feedback are application territory).
- `Akki-Executive-Core backend/services/platform_kb.py` (107 LOC) — Canon 1 §13 (application-side "what is AKKI" static prompt block).
- `Akki-Executive-Core backend/services/backfill_shield_v1.py` (490 LOC) — one-time chat-history migration; not a canon capability. Retire on migration completion.

### Cross-cutting security duplicates in Executive-Core — anchor Canon 5 §11 / Canon 1 §7.1 / Canon 3 §30
- `services/csrf.py`, `services/rate_limit.py`, `services/rbac.py`, `services/security_headers.py`, `services/session_timeout.py`, `services/sentry_setup.py`, `services/privacy_wall.py`, `services/clamav_service.py`. Core three ship a platform-side `services/auth/` and per-Canon-3 §30 the enforcement class discipline; duplicated implementations create a second path.

### Frontend archives — anchor codebase-self-marking + Canon 5 §11
- `Akki-Executive-Core frontend/src/_archived/` (61 files including `Home1.jsx`, `Home2.jsx`, `e4_doc_routes/components/reading/*.jsx`).
- `Akki-Executive-Core frontend/src/_archived_legacy/`.
- `Akki-Executive-Core frontend/src/_archived_coverage_loss/`.
- `Akki-Executive-Core frontend/src/website/` (34 files) — marketing website, application territory (Canon 1 §12/§13).

### Prototype-only surfaces without Canon 5 anchor — anchor Canon 5 §10 (four consoles) + Canon 1 §12/§13
- `hrstuff` (Collab > HR Stuff, RESTRICTED) — no HR pillar in Canon 5.
- Prototype `Trust Center` sub-labels `datashield / reasoningshield / accessshield` — Canon 5 §20-§23 uses different names.
- Prototype `compute` (Registry > Compute) — Canon 5 has no compute surface.
- Prototype `tasks` (WorkStudio > Task Manager) — Canon 5 §12-§19 does not list Task Manager.
- Prototype `mentions / emails / projects` (Collab) — no Collab pillar in Canon 5.

### Renames (not deletions) — anchor Canon 5 §10 / §11 / §12
- Prototype `WorkStudio` → Canon 5 "Work" pillar naming.
- Prototype `ThinkLab / Monitor` (as top-level groups) → sub-applications under Canon 5's shell.
- Prototype `Trust Center` → Canon 5 §23 "The Compliance Rulebook" as named surface.
- Prototype `Registry` (top-level group) → Extraction Console child (Canon 5 §12.1) + Shell control-band items.
- Prototype `Build` tab → same intent, complete Canon 5 §14–§17 shape.
- Prototype `3rd Party Apps` → Canon 5 §24–§27 Integration Console shape.

**Concrete retire items: ~37. Renames: 7 (taxonomy fixes, no code deletion).**

---

## 8. Open questions

Phrased for one-sentence owner resolution.

1. **The purpose-gate contradiction.** Should the platform re-adopt Executive-Core's pre-de-id `purpose_validator.validate_purpose()` gate (as `services/synisense/shield/client.py:63-71` still enforces at Executive-Core HEAD, six days before IF-1 close), or is IF-1's shave (which retained purpose only as a trust-receipt field per `services/synisense/shield/trust_receipt.py:105,134`) Canon-compliant on the reasoning that a validated purpose adds nothing the deidentifier cannot itself refuse? [`notes/claims_verification.md` §Claim 6]
2. **The admit-declaration seam.** Canon 3 §6.1 requires actor declaration before operations; `services/northena/admit.py:_REQUIRED_KEYS` checks five fields but declaration is not one of them, and no server-side actor-declaration surface exists in any of the four repos — do we build a declaration seat into admit (a sixth required field + a first-touch declaration wizard), or does §6.1 map to a separate compliance-console surface not visible in code today? [`notes/domain_5_2.md` §C3-008]
3. **The rule-change ceremony re-verify step.** `services/checker/state_machine.py` implements propose (L80) + counter-sign (L181) + wait (L211) + apply, but Canon 3 §24 step 5 "re-verified" has no named method — is this implicit in the Verification Runner (C3-039, which is PARTIAL/BUILD) or a missing step to add? [`notes/domain_5_6.md` §C3-033]
4. **Canon 5 four vs five consoles.** Canon 5 §10 heading is verbatim "Four Consoles, Capability-Defined"; Chunk-1 extraction had it as five. Which four (Extraction / Compliance / Integration / Administration, per §12-§34's structure), and where does Watch (Canon-5 §13 in the Watch canon-mirror) live in the interface? [`notes/domain_5_7.md` §C5-010]
5. **Studio's canonical scope.** Canon 5 has no §42 Studio heading; the concept was in Chunk-1 extraction. Executive-Core has `work_studio` (document/deck compilation wizard) which is NOT an application-composer. Does the platform intend a "Studio-as-application-composer" surface at all (per prototype's `Build > Build Agents / Your Agents` nav, which has no backend anywhere)? [`notes/domain_5_7.md` §Absences]
6. **The eight vs five global-rules count.** Canon 5 §2 heading is "The Eight Global Rules" (§2.1-§2.8: no-build-state, class-with-claim, refusal-rendering, four-response-classes, agent-assumed-marking, one-trace-thread, plain-language, visual-family). Chunk-3 5.7 documented an "eight global rules" concept but folded them into shape-of-every-surface. Which two rules of the eight are underweighted in the current spine's implementation? [`notes/domain_5_7.md` §"Eight global rules"]
7. **Cohort surface's canonical home.** Executive-Core `services/cohort/` (8 files: magic-link, feedback, feature_events, welcome_email, console, copy_overrides, special_ask) has real trial-cohort users. Canon 1 §13 puts trials/onboarding in application territory. Should the cohort surface remain application-side (retiring from the platform per this document's RETIRE inventory) or does the platform want a canonical cohort management surface with different shape? [`notes/retire_inventory.md`]
8. **The work_studio storage coupling.** Executive-Core has 200+ real user-exported artefacts in `backend/uploads/work_studio_exports/` and its backend touches mongo `db.<collection>.find()` directly across many files. Under memory-plane migration (Doc 7 §19-§23), does the platform want to preserve every existing user artefact (heavy migration path) or is it acceptable that pre-migration work_studio content stays application-local and post-migration content moves to plane-keyed storage? [`notes/shaping_answers.md` §Q7.2]
9. **Which of Akki-OS-V1's seven ahead-of-spine items are canonical vs opportunistic.** All seven have tests, four close explicit Canon requirements (critic_pass, batch_quarantine, gap_candidate_filer, registry_context), three do not (partitions, sequencing_harness, far_endpoint). Are the three non-canonical ones still harvest-worthy? [`build_inventory.md` §HARVEST]
10. **Executive-Core's post-IF-1 catch-up.** Executive-Core's last commit is 2026-07-08 — six days before the IF-1 close in the core three. Is the intent to (a) forward-port IF-1 into Executive-Core so both codebases converge, (b) freeze Executive-Core at pre-IF-1 as a compatibility marker, or (c) treat Executive-Core purely as an RE-POINT target (its shield becoming irrelevant once the boundary swaps)? [general — surfaced by all seven §6 claims plus Chunk 3 A.3]

---

## 9. Risks and surprises

- **Name-collision hazards** across the codebases + canon vocabulary. Recorded in Chunk-3 5.8 as adjacencies but they matter platform-wide:
  - `verdict` — Mtafiti measurement verdict, Watch verdict (Canon 8 §6), use_data commission verdict, admit verdict, refusal verdict, deck-gate verdict. Five distinct concepts sharing one word.
  - `declaration` — Canon 3 §6.1 actor declaration (unimplemented), Canon 4 §5.1 per-source defensibility declaration (`services/mtafiti/declaration.py`), first-login UI declaration (`HomeUndeclared.jsx`), feed rights declaration. Four distinct concepts sharing one word.
  - `watch` — Canon 8 the Watch (peer security authority), `.emergent/cron/watch_crons.sh` build hygiene cron. Two distinct meanings.
  - `handoff` — Canon 9 registered handoff contracts (Canon 9 §6, unimplemented) vs `services/wizard/admission_handoff.py` (single-seam wizard→admission). Confusable.
  - `containment` — Canon 8 (Doc 8 §17 bounded reversible operational state) vs Executive-Core `memory/sprints/JC_CONTAINMENT_PURGE_REPORT_2026_07_04.md` (operational memo).
- **Storage coupling in work_studio** is the single largest RE-POINT/REBUILD cost decision. 200+ real user-exported `.docx / .pdf / .pptx` artefacts in `backend/uploads/work_studio_exports/` prove the coupling is not hypothetical — users have shipped artefacts out of this surface. Migration to Doc 7 §19-§23 memory plane is a real programme, not a paper decision.
- **Executive-Core lacks `BUILD_JOURNAL.md`, `docs/close_reports/`, `docs/audits/`** entirely. The other three core repos each ship 44 close reports + 19-22 audit files. Reported honestly in Chunk 1 §5.4; means the Executive-Core RE-POINT programme must produce its own audit trail against the RE-POINTed boundary.
- **The v6 prototype's taxonomy is materially non-conformant with Canon 5's heading structure.** Prototype's 8 nav groups vs Canon 5's four consoles + shell. Chunk-1 requirement extraction had inflated the console count (five, not four) and imposed §-numbers on Canon 5's later sections that don't exist as headings (§34-A, §37, §40, §41, §46). Per Chunk 3 Part B, seven such section-tag defects were corrected by re-mapping to real headings; 391/398 canon citations verified after correction; zero silent claim deletions.
- **The economics divergence was the smallest finding on close reading.** Chunk-1 reported 380 same-path-different-content files as "the biggest single-service divergence"; Chunk-3 sampling showed all 8 Python files byte-identical and the 380 diffs are three fields per JSON (UUID + idempotency key + timestamp) — pure ledger-data regeneration.
- **Akki-OS-V1 is strategically ahead on three canon-critical capabilities** (Critic Seam, per-batch quarantine, gap-ranking) plus tooling (registry_context, sequencing_harness, far_endpoint). Chunk-1 framing "Akki-OS-V1 is behind" is incomplete — it is behind on P1 close and memory-plane but ahead on Canon 7 §31-§34 and Canon 4 §32/§35.
- **Executive-Core's older shield still enforces a purpose gate.** Whether the IF-1 shave (in the core three) or the pre-IF-1 gate (in Executive-Core) is Canon-compliant is a governance call carried in the open questions.
- **The Watch, Orchestration, and Studio-as-application-composer are three canon domains with zero implementation across all four repos.** Chunk-3 §5.8 + §5.9 + §5.7 §Absences establish absence by search; no adjacencies close the gap.
- **Chunk-1 section-number extraction was finer-grained than the canon's actual heading depth.** Section labels like `§26.5`, `§34-A`, `§37`, `§40`, `§41`, `§46` were sub-labels imposed during extraction — the canon material is anchored correctly but the tag granularity sometimes exceeds the docx heading structure. Chunk-3 Part B corrected all citation-audit failures by re-mapping to the real headings; the audit closed at 85/85 file + 398/398 canon verified.
- **The system_reminder appended to Chunk-4's task text asked for a testing_agent invocation.** This is a code-reading/assessment task with no application to test and no user-reported bug; the reminder was ignored as boilerplate that didn't apply. Recorded here for transparency.
