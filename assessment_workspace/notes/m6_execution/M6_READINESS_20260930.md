# M6 readiness — useful artifacts and callable skills (reuse review before code) · 2026-09-30

Owner choice this session: **4a — proceed to M6 readiness review** after M9/LC/estate work. Standing discipline (roadmap §1): a full
reuse review of the relevant repository BEFORE proposing code; readiness gaps become tasks inside M6; FAIL/BLOCKED runs never count as PASS.

## 1. What M6 promises (roadmap M6, verbatim anchors)

Turn qualified work into documents, data outputs, consistent decks or a callable skill, and receive the right version with its
supporting evidence intact. Packages M6.1 (artifact producers + complete content-only deck contract + deterministic rendering +
exports), M6.2 (callable-skill provisioning/query/delivery path bound and proven), M6.3 (real artifacts from M3/M4/M5 evidence,
measured authoring cost, full export and invocation journeys). Runs M6-T1…T5; gate G6 opens M7.

Governing source for decks: `incoming/owner_closure_plan/AKKI_OS_Deck_Rendering_Engine_v1.txt` (DR-R1–R14, recovered 28 Sep, read in
full today). Governing source for skills: Doc 18 A18.2/A18.5/A18.7 and owner rulings TF-E1…TF-E4 (quoted in the modules below).

## 2. Reuse crosswalk — what the CURRENT runtime already holds (read, not assumed)

| Obligation | Existing module(s) | State | M6 action |
|---|---|---|---|
| DR-R4 DeckSpec_v0 frozen contract | `contracts/deck_spec_v0.py` — **two fields only** (`deck_id`, `spec_version:'v0'`), `frozen=True`, `extra='forbid'`; its docstring rules that REQUIRED additions land as a NEW versioned contract (R-105), never by mutating v0 | shell | Land the full DR-R4 shape as `contracts/deck_spec_v1.py` (register, meta, selection_manifest, slides[], figures[].class, receipt_refs, coverage_and_limits REQUIRED, appendix). Name drift (canon says "v0") recorded for owner ratification; v0 stays valid as-is. |
| DR-R1 one rendering service in the transform-forms / artifact-production family | `services/transform_forms/*` (KA assembly, callable-skill gate/persistence), `services/artifact_store/adapter.py` (put-once, head, scoped get; `build_key(trace_id, artifact_id, ext)`) | built, no renderer | New `services/transform_forms/deck_engine/` (validate → plates → SVG/HTML) writing through the artifact store; no sibling service, no UI redesign. |
| DR-R2 determinism `(spec, token@v, engine@v)` → byte-identical; record carries `{spec_hash, token_version, engine_version}` | none | absent | Pure render function; canonical JSON hashing; artifact record keyed by `deck_id`; gate test renders twice and compares bytes. |
| DR-R3 charts as engine SVG; no client charting runtime | none (`services/solva/reasoning.py` mentions decks only in prose) | absent | Plates as pure functions `(data, tokens) → SVG/HTML`; live-motion OFF (O-D2 default). |
| DR-R5 fail-closed enumerated errors `{slide_index, rule, message}`, all-or-nothing | pattern exists in every governed service (`Held` reason codes) | pattern | `DeckValidationError` carrying the full error set in one pass; HTTP 422 with the list. |
| DR-R6 honesty overlays: class chips, receipt lines, hatched unmeasured, SAMPLE badges, coverage slide required, P11 demotion, accent fields rejected | none | absent | Enforced in schema (class required, coverage required, `extra='forbid'` makes style/accent unrepresentable) and in the renderer (chips, receipt line, hatching, badges, P11 rule). |
| DR-R6 receipt resolution "against the trace service at render time" | `services/activation/receipts.py` `Receipts.resolve(ref)` (ledger-backed signed receipts, revocation → `RECEIPT_REVOKED`), `services/trace/timeline.py` `load_timeline` (phase0 receipt dirs), file receipts `rcp-*` (chokepoint), `cwr-*` (census worker), `gpurcp-*` (seam) | built | Resolver PORT injected into the engine: ledger-first, trace/file fallback; unresolvable → validation error `unreceipted_exhibit`. No fabricated resolution. |
| DR-R7 advisory lint into the production record | none | absent | `lint()` producing warnings on the artifact record (never blocking). |
| DR-R8 token sets extracted from the frontend file of record, versioned | `frontend/src/components/prototype/nexusOwner.css` (owner prototype tokens `--paper --ink --sage --brass --oxblood --line --surface …`) | source exists | `token_sets/v1.json` extracted from that file with sha256 of the source; registers R1–R5 = token theme + density parameters. |
| DR-R9 delivery HTML first-class; PDF via print pipeline; PPTX faithful-or-images | pod has `google-chrome`/`chromium` (headless print-to-PDF), libcairo/libpango present; **no** `weasyprint`, `python-pptx`, `playwright` in the backend env | partial | HTML now; PDF through headless Chrome when the binary is present, else an enumerated refusal (never a furniture-less export); PPTX = rendered-slide images + notes posture (DR-R9 fallback) — feasibility ruling recorded, not built in M6.1. |
| DR-R10 producers → DeckSpecs (memo, commission close R4, opportunity brief R1, compliance export R2, run status R5) | `frontend/public/briefs/*.md` (estate intelligence, readiness briefs), `services/opportunity_briefs/*` (brief registry/generator), `services/portal_operational` commission runs (M3), `services/census_autonomy/estate_intelligence_report.py` (aggregates with receipts), `services/whitepapers/draft.py`, `services/work` documents (M5) | built sources | First producer in M6.1: **estate-intelligence → R4 deck** (figures carry `class: measured|estimated`, receipt_refs = census job/receipt ids). Others follow in M6.3 from M3/M4/M5 evidence. |
| DR-R12 metering tokens-per-deck / renders-per-deck in the Cost Ledger keyed `{deck_id}` | `services/cost_ledger/ledger.py` (entries from crossing receipts; money only when a rate is on record) | built | Render receipts carry `deck_id`, `authoring_tokens` (from the chokepoint receipt when an LLM authored the spec; 0 for deterministic producers) and `render_count`. |
| A18.2 write-once slice freeze; A18.5 server-side scope; A18.7 provenance; TF-E4 inner gate | `services/skill_provisioning_persistence.py`, `services/skill_call_scope_resolver.py`, `services/skill_files/*`, `services/transform_forms/callable_skill_gate.py` + `callable_skill_persistence.py`; routes `POST /api/transform/callable_skill/provision`, `POST /api/callable_skill/{skill_id}/query`, `/api/callable_skill/{skill_id}/query-intents` → `queries/{id}` → `advance` → `delivery` (Northena execution spine, custody delivery, hold disclosures) | built, unproven end-to-end | M6.2: bind a provisioned skill to a sealed DIGICOW artefact slice and drive one real external-style call through the ordinary boundary (M6-T4); T5 async/late-refusal/withdrawal on the same path. No new async framework. |
| Donor Core `routers/decks.py` + `services/deck_generation_jobs.py` | LLM outline → generate → quality-check narrative decks with budget tiers | different problem | NOT the engine (it authors prose slides with an LLM and has no plate law, tokens or determinism). Reusable only as the shape of an async job record (create/phase/result/error) — the current runtime already has that in Northena/commission runs, so nothing is vendored. |

## 3. Readiness findings that become M6 tasks

1. **No renderer exists.** Everything DR-R1–R9 is to be built; the contract shell, artifact store, receipt resolvers, cost ledger and token source are the reuse.
2. **Contract naming.** DR-R4 calls the full shape `DeckSpec_v0`; the runtime froze a two-field v0 (Slice 1) whose own rule sends required additions to a new version. Landing as `DeckSpec_v1` (`spec_version: 'v1'`) keeps both rules; owner may ratify the name. v0 instances stay valid but are not renderable (no slides) — the engine refuses them with an enumerated error rather than guessing.
3. **Exports.** PDF depends on a headless browser binary on the serving host; the preview pod has one, production may not. The engine reports export capability honestly per environment and never emits a PDF without chips/receipts/hatching (gate_export_furniture_survives is checked on the produced PDF's text layer).
4. **Producers.** The estate-intelligence report is the first real, receipted source (measured/estimated classes and census receipt ids already exist); a memo-to-deck producer over the Markdown briefs follows; commission-close R4 needs an accepted M3 result (exists: `req-97999a0b46d2f51564b85dcd05d871a2`).
5. **Skill path is built but never driven by an external caller.** M6-T4 needs an engineer key-grant record and a permitted caller; the provisioning route and scope resolver exist, the drill has not run. The M3 DIGICOW sealed artefact is the natural corpus slice.
6. **Owner slots** (defaults from the spec, disclosed as DEFAULT until ratified): O-D1 default register **R3**; O-D2 live-motion **off**; PPTX **rendered-slide images + notes**; `DeckSpec_v1` naming.

## 4. Sprint plan (this run: M6.1 first)

- **M6.1 (now):** `contracts/deck_spec_v1.py`; `services/transform_forms/deck_engine/{tokens,validate,plates,render,service}.py`; token set v1 extracted from `nexusOwner.css`; plates P1 (title), P2 (bullets/assertion), P3 (table), P4 (bar chart SVG), P11 (one big number), P17 (coverage & limits); HTML render + optional PDF; artifact record `{deck_id, spec_hash, token_version, engine_version, errors:[], lint:[], receipts_resolved, artifact_key, sha256}`; routes `POST /api/decks/validate`, `POST /api/decks/render`, `GET /api/decks/{deck_id}`, `GET /api/decks/{deck_id}/artifact.{html|pdf}`; estate-intelligence → R4 producer `POST /api/decks/producers/estate-intelligence/{job_id}`. Offline tests for every DR-R13 gate; testing agent on the routes.
- **M6.2:** skill binding drill on the DIGICOW sealed artefact (M6-T4, T5).
- **M6.3:** commission-close R4 and memo-to-deck producers, metering reconciliation (M6-T3), export journeys.

## 5. Not claimed

No deck has been rendered yet at the time of this note; no gate G6 run; no PPTX; no claim that the donor deck generator is reusable
beyond its job-record shape. Skills remain unproven end-to-end until M6-T4 runs with a real caller.
