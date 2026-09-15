READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL · Grounding Brief · Paired Wave (M8 #3+#4)

**Wave charter trigger.** DECISIONS 2026-09-14T~15:30Z W-DATA-SUITE-V2-LIFT close report §Δ (verbatim, line 7810):

> "`W-DATA-SUITE-ANALYZE-WORKSPACE-REAL` + `W-DATA-SUITE-DEEP-DIVE-REAL` — replace engine skeletons with case-agnostic real mechanism (paired wave)."

And DECISIONS 2026-08-27T~02:35Z Owner M8 sequencing verbatim (line 8319):

> "Then M8 unblocked quick hardening (small waves, high value): W-TESTS-FIRST-GUARD-INVARIANT → W-EXPORT-ARTEFACT-RENDER → W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL (paired) → W-CENSUS-RUNTIME-ORCHESTRATION → W-AUDIO-PROD-MODEL-SELECT"

Owner GO chain confirmation (2026-09-15T~16:20Z verbatim): *"After the audit lands, resume: paired W-DATA-SUITE-ANALYZE-WORKSPACE-REAL + W-DEEP-DIVE-REAL → W-CENSUS-RUNTIME-ORCHESTRATION (expanded) → M6 open (Path α/β flagged) → M7 open."*

---

## §A · Verbatim discharge anchors

### A.1 · CP-D8 wave-honest limit (verbatim, DECISIONS line 7802)

> "E.2 Negative-scan scoped to `analyze_workspace/` + `analysis_lifecycle.py` + `workbook_analyzer/` donor paths only."

Discharge in this paired wave: word-boundary case-insensitive executive-domain negative-scan re-runs across the two engine modules AND their new tests. Any donor-token surfaces → HALT.

### A.2 · CP-D8 skeleton disposition (verbatim, DECISIONS line 7778)

> "Landed `services/data_suite_v2/engines/{__init__.py, analyze_workspace_engine.py, deep_dive_engine.py}`: two engine skeletons expose `run(*args, **kwargs)` that raises `NotImplementedError` with `HALT` in the message per Solva-V2 CP-S8 precedent. ... No LLM/HTTP/DB donor plumbing was lifted (grounding brief §E.4)."

Discharge in this paired wave: replace the HALT `run()` with real case-agnostic mechanisms. Still no LLM/HTTP/DB plumbing — the real mechanisms are pure functions of typed inputs that produce the CP-D4 tab-artefact shapes.

### A.3 · CP-D4 analyze-tab contracts (already-landed law)

> `ANALYZE_TAB_KINDS = frozenset({"rapid", "deep_dive", "sources"})` closed 3-value set (line 7714). `AnalyzeRapid` [session_id, tab_kind="rapid", unit_ref_count]. `AnalyzeDeepDive` [session_id, tab_kind="deep_dive", synthesis_sha256_hex] — carries a **hash only, no raw synthesis text/body/content**. `AnalyzeSources` [session_id, tab_kind="sources", unit_refs: Sequence[str]] — carries **UnitRefs only, no raw content/body/text**. Each `__post_init__` enforces its own `tab_kind` label at construction; `AnalyzeTabInvalid` on mismatch.

Discharge in this paired wave: `analyze_workspace_engine.run(...)` returns `Tuple[AnalyzeRapid, AnalyzeSources]`; `deep_dive_engine.run(...)` returns `AnalyzeDeepDive` with a deterministic `synthesis_sha256_hex`.

### A.4 · Canon-4 §22 (verbatim, `canon/text/Akki_Canon_4_Operating_Engines.txt` line 118)

> "The function returns unit references only. It carries no class decision. A load-bearing function that returned a class would have collapsed the two faculties into one — Solva chooses the units; it does not choose what those units imply."

Discharge in this paired wave: `AnalyzeSources.unit_refs` is a straight pass-through of the caller-provided source refs; the engines emit no class decision, no interpretation, no synthesis content — only shape.

### A.5 · Pull Seam P1 (context anchor)

> "The Pull Seam is the model-facing seam; source data does not cross; only derivatives cross."

Discharge in this paired wave: `AnalyzeDeepDive` carries `synthesis_sha256_hex` (a derivative-shape hash), never the synthesis text. The deep-dive engine computes a deterministic hash over a canonical serialization of the workspace's shape; the synthesis body itself is never materialised in this mechanism.

---

## §B · CP breakdown (2-CP paired wave)

| CP | Deliverable | File(s) |
|----|-------------|---------|
| CP-DASWR1 | `services/data_suite_v2/engines/analyze_workspace_engine.py :: run(*, session_id, source_refs) -> Tuple[AnalyzeRapid, AnalyzeSources]`. Pure function: no LLM, no HTTP, no storage. Case-agnostic: no executive-domain tokens in module + tests. Refusals: `WorkspaceInvalidError` on empty/non-string `session_id`; `WorkspaceEmptyError` on empty `source_refs`; `WorkspaceInvalidError` on non-string element in `source_refs`. Shared exception classes land in `engines/__init__.py`. | `services/data_suite_v2/engines/__init__.py` (+errors) · `services/data_suite_v2/engines/analyze_workspace_engine.py` (real run) · `tests/invariants/test_wdaswr_cp_daswr1_analyze_workspace_engine.py` |
| CP-DDDR1 | `services/data_suite_v2/engines/deep_dive_engine.py :: run(*, session_id, source_refs, prior_notes=()) -> AnalyzeDeepDive`. Pure function: no LLM, no HTTP, no storage. Case-agnostic. `synthesis_sha256_hex` = `sha256` of a canonical UTF-8 serialization of `(session_id, sorted(source_refs), prior_notes)` — deterministic across calls; different inputs → different hash. Refusals: same shape as CP-DASWR1 for `session_id` / `source_refs`; `WorkspaceInvalidError` on non-string element in `prior_notes`. | `services/data_suite_v2/engines/deep_dive_engine.py` (real run) · `tests/invariants/test_wdddr_cp_dddr1_deep_dive_engine.py` |

**Estimated ratchet delta:** +10 invariants (target: **4083 → 4093**).

---

## §C · Invariants gated (right-reason ImportError / HALT-message REDs before mechanism)

### C.1 · CP-DASWR1 (5 invariants)

1. **Module fabric.** `services.data_suite_v2.engines` exports `WorkspaceEmptyError` + `WorkspaceInvalidError`. `services.data_suite_v2.engines.analyze_workspace_engine.run` is callable and does NOT raise `NotImplementedError` on valid inputs.
2. **Empty `session_id` refuses.** `session_id=""` propagates `WorkspaceInvalidError` mentioning `session_id`.
3. **Empty `source_refs` refuses.** `source_refs=()` propagates `WorkspaceEmptyError` mentioning `source_refs`.
4. **Return shape.** Valid inputs return `Tuple[AnalyzeRapid, AnalyzeSources]` with `AnalyzeRapid.tab_kind="rapid"`, `AnalyzeRapid.unit_ref_count == len(source_refs)`, `AnalyzeSources.tab_kind="sources"`, `AnalyzeSources.unit_refs == tuple(source_refs)`.
5. **Deterministic pure function.** Two byte-identical calls produce byte-identical `(AnalyzeRapid, AnalyzeSources)` dataclass tuples. No LLM/HTTP/storage side-effects.

### C.2 · CP-DDDR1 (5 invariants)

1. **Module fabric.** `services.data_suite_v2.engines.deep_dive_engine.run` is callable and does NOT raise `NotImplementedError` on valid inputs.
2. **Empty `session_id` refuses.** Same shape as CP-DASWR1 #2.
3. **Empty `source_refs` refuses.** Same shape as CP-DASWR1 #3.
4. **Return shape.** Valid inputs return `AnalyzeDeepDive` with `tab_kind="deep_dive"` and `synthesis_sha256_hex` matching `^[0-9a-f]{64}$` (64 lowercase hex chars). Carrier is hash-only per Canon-4 §22 · Pull Seam P1.
5. **Deterministic + input-sensitive.** Same inputs → same `synthesis_sha256_hex`; changing any single input element (session_id · a source_ref · a prior_note) → different `synthesis_sha256_hex`. Zero-collision on the tested input pairs.

---

## §D · Wave-honest limits (declared at open)

1. **E.1** No LLM invocation. No HTTP call. No filesystem write. No database read. The engines are pure functions of typed inputs.
2. **E.2** The synthesis body itself is NOT materialised. `AnalyzeDeepDive` carries `synthesis_sha256_hex` as a derivative-shape carrier per Canon-4 §22 + Pull Seam P1. Producing a real synthesis body is a follow-on wave that must route through the release gate + P036 receipt-before-result (would be CP-DDDR2+ if the owner ever authorises it).
3. **E.3** Case-agnostic. Word-boundary case-insensitive executive-domain negative-scan across the two engine modules AND their tests. Any donor-token surfaces → HALT this wave.
4. **E.4** `prior_notes` is an OPTIONAL sequence of pre-existing notes to fold into the deep-dive hash; default empty tuple. Not required for the shape contract.
5. **E.5** `source_refs` is a caller-provided Sequence[str] of unit-ref labels. This wave does NOT enforce a particular unit-ref format; a follow-on wave may add a shape guard.
6. **E.6** No mutation of caller inputs. Both engines take Sequence inputs and treat them as immutable; the tuple(...) coercion is defensive but harmless.

---

## §E · Commit protocol

- **CP-DASWR1 (Commit A on track-a):** code + tests + `baseline_failures.json` bump 4083 → 4088.
- **CP-DDDR1 (Commit B on track-a):** code + tests + `baseline_failures.json` bump 4088 → 4093.
- **Wave-close (Commit C on master):** state — DECISIONS entry + NEXT refresh + composite seal + drill receipts + riders + boundary probe #14.
- **Seal:** `phase0/output_verified_seals/w_data_suite_analyze_workspace_deep_dive_real.seal.txt` (`Kind: w_data_suite_analyze_workspace_deep_dive_real`).
- **NEVER push.**

---

## §F · Decision points / stop conditions

Wave HALTS with a decision-point note if:
- Word-boundary executive-domain negative-scan surfaces a donor token in either engine module or either test file.
- Baseline ratchet regression at CP-DASWR1 or CP-DDDR1 double-green.
- Any file entering the ratchet path leaks credential-shaped content (custody-cat guard fires).

Otherwise wave proceeds per owner directive.

---

## §G · Boundary-hygiene probe cadence

Per DECISIONS 2026-09-15T~09:50Z Effect 4 verbatim: *"Keep the CD/Visitors re-probe loop running at boundaries while egress is open."* Probes fire at each CP boundary (CP-DASWR1 seal + CP-DDDR1 seal + wave-close). Probe #13 already fired at estate-contact-audit close (CD+Visitors BOTH FAIL 6.007s/6.003s). Standing retry loop continues.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
