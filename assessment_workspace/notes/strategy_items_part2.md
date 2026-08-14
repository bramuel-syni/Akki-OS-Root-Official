# strategy_items_part2.md — BUILD_STRATEGY Part 2

**Chunk 4, Part 2.** All BUILD items with no canon-compliant donor code (i.e., must be built from paper canon). Every item covers 1+ canon requirement rows; the union of coverage across Part-1 + Part-2 = every non-doctrine canon row (mechanical audit produces zero gaps).

**Scope of this file:** 50 items — bundled by canonical mechanism per Orchestrator Ruling B ("not one mega-item per canon"). The Watch's 60 rows fan out to 15 mechanism-scoped items; Canon 9's 45 rows to 6; Canon 2 CIF's 30+ rows to 6.

**Ruling-1 transition linkage:** `WS-BUILD-DECL` and `WS-BUILD-WATCH-RECONCILER` carry the demonstrated-firing precondition for `WS-CONTRADICTION-PURPOSE-GATE` strip.

**Ruling-B new items:** `WS-BUILD-STREAMING-PORT` and `WS-BUILD-OBJECT-STORAGE-PORT` promoted from folded dependencies to standalone items (multiple items gate on them; FL-P1-03 stays open pending owner ratification).

**Parity-seat linkage:** Every item creating a NEW contract cites `WS-WIRE-PARITY-EXTENSION` (Part 1) as a dependency — no new contract lands without a parity-seat entry.

Estimation discipline and field template — see `strategy_items_part1.md` §top. Not repeated.

**Cross-cutting doctrinal frame** applies to every item (Canon 9 record matrix + task identity + Canon 4 §32 quality matrix + Canon 3 §31 verification packs + Ruling 1 four-test discipline). Fields that cannot be filled honestly → `notes/fidelity_ledger.md`.

---

# A. Custody & Boundary (Canon 1 §12, §6.1, §7.1)

## WS-BUILD-DECL

1. **WHAT.** Actor-declaration seat + admit-time check + supersession. Rows C3-008, C3-009, C3-010, C3-059. Component: new `services/declaration/` (writer + surface). Contract: `Declaration.v0` (frozen). Record class: `Actor.Declaration` (Canon 9 §6 — writer = declaration seat; readers = admit + Watch + Compliance Console). Task identity: `declaration.capture` and `declaration.check.per_admit`.
2. **CANON CLAUSES.** Canon 3 §6 (Admit — declarations captured before operations); Canon 3 §33 (governance orchestration end-to-end); Canon 6 §3 (setup declarations); Ruling 1 (declaration check is a Watch-reconciler-paired precondition for `WS-CONTRADICTION-PURPOSE-GATE` strip).
3. **DEFINITION OF DONE.** Every `northena/admit.compile_and_freeze` call requires an in-force declaration; declarations captured at setup morning (Canon 6 §3) and re-captured on scope change (supersession event). Admit-time check refuses on missing/expired/scope-mismatched declaration; refusal ledgered via `WS-WIRE-CUSTODY-DECL`. `WS-CONTRADICTION-PURPOSE-GATE` strip prerequisite (a) demonstrates firing via a drill: a declaration-scoped refusal is observable in the ledger and rendered by the refusal card.
4. **QUALITY EVIDENCE.** Contract test (Declaration.v0 shape) + drill (a full admit-refusal cycle with a scoped-mismatched actor). Uncurated sample: every admission in a drill week carries a declaration id or refusal reason. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-WIRE-CUSTODY-DECL` (Part 1), `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION` (new contract). Ruling-1 pair with `WS-BUILD-WATCH-RECONCILER`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components (declaration seat + admit hook + surface), new register/console surface (declaration seat is a first-class register), 3 integration surfaces (admit, ledger writer, Watch reader).
7. **REVERSAL COST.** High. Declaration records are append-only; a wrong shape freezes forever. Reversal = new supersession entry with revised shape; existing records stay. Ruling-1 gate to strip depends on this firing — a wrong build blocks the strip lawfully.

## WS-BUILD-INPUT-SEAT

1. **WHAT.** Canonical input-seat surface distinct from de-identifier. Row C3-018. Component: new `services/input_seat/` (per Canon 3 §12 seat, not tenant_entities de-identification). Contract: `Input.Envelope.v0`. Record class: `Input.Seat.Verdict` (Canon 9 §6 — writer = input seat; readers = admit + Watch). Task identity: `input_seat.admit.per_call`.
2. **CANON CLAUSES.** Canon 3 §12 (input seat); Canon 3 §33 (governance orchestration); Canon 1 §6 (fail-closed custody).
3. **DEFINITION OF DONE.** Every incoming payload passes through the input seat before de-identification; seat writes a verdict row per call (admit/refuse/quarantine). Existing `tenant_entities.py` becomes a downstream stage, not the seat itself. Verification: drill with a shaped-input fixture produces a seat verdict + downstream ledger row.
4. **QUALITY EVIDENCE.** Contract test (envelope shape) + drill. Uncurated sample: one drill day of live traffic; seat verdict count = incoming call count. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: new authority (input seat is a Canon-3 §12 authoritative surface).
7. **REVERSAL COST.** High. Input-seat verdicts are ledgered; reversal removes the seat and re-exposes payload to un-gated code paths (Canon 3 §12 violation). Ledger stays.

## WS-BUILD-INPUT-SEAT-DUAL

1. **WHAT.** Dual identity at input seat: governance identity at admit; Watch identity when sensing. Row C3-020. Component: extension of `services/input_seat/` (per WS-BUILD-INPUT-SEAT) with dual identity resolver. Contract: `Input.Seat.Identity.v0`. Record class: uses task-identity register (Canon 9 §8-§35). Task identity: `input_seat.identity_resolve.per_call`.
2. **CANON CLAUSES.** Canon 3 §12 (input seat dual role); Canon 9 §8-§35 (task identity register); Canon 8 §4.11 W11 (one task, one identity).
3. **DEFINITION OF DONE.** Every input-seat verdict carries exactly one task identity (governance OR Watch, never both — Canon 8 §4.11 W11). Task-identity register (WS-BUILD-TASK-IDENTITY-REGISTER) contains the mapping. Verification: AST discipline check (mirror `test_ast_egress_gate.py`) fires on any dual-identity assignment.
4. **QUALITY EVIDENCE.** Invariant class (AST-scoped one-identity gate). Uncurated sample: full drill day; dual-identity assignments = 0. Calibration under Canon 8 §4.11.
5. **DEPENDENCIES.** `WS-BUILD-INPUT-SEAT`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 1 component (extension), 1 new/changed contract (identity shape), 2 integration surfaces.
7. **REVERSAL COST.** Medium. Dual-identity slip is a Canon 8 W11 violation; reversal disables the resolver, task-identity register keeps prior records.

---

# B. Extraction Quality (Canon 4 §26, §32)

## WS-BUILD-MOAC-SCORECARD

1. **WHAT.** MOAC six-criteria scorecard + measurement pipeline + drift + latest-reading-in-circulation. Rows C4-037a..f, C4-038, C4-039, C4-040, C4-067, C4-068, C7-D14, C7-D15. Component: new `services/moac/` (scorecard + drift monitor). Contract: `MOAC.Scorecard.v0` (frozen). Record class: `MOAC.Scorecard` (Canon 9 §6 — writer = MOAC engine; readers = Extraction Console + Compliance Console). Task identity: `moac.score.per_adapter_version`.
2. **CANON CLAUSES.** Canon 4 §26 (MOAC anchor); Canon 4 §32 (quality matrix); Canon 5 §14 (Model Catalogue surface pair).
3. **DEFINITION OF DONE.** Every adapter version carries a MOAC scorecard (6 criteria + uncurated-sample provenance + rights lineage + version history). Drift measured continuously; the latest reading is the one shown in circulation (Canon 4 §50). Adapter without a scorecard fails admission (D-MOAC-Missing per C7-D15). Verification: drill with a shape-defect fixture on any of 6 criteria produces the correct card decoration.
4. **QUALITY EVIDENCE.** Contract test (scorecard shape) + drill class (6 defect fixtures, one per criterion). Uncurated sample: 20 adapter versions across a drill month; scorecard coverage = 100%. Calibration under Canon 4 §32.
5. **DEPENDENCIES.** `WS-BUILD-ADAPTER-REGISTRY`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components (scorecard + drift + surface hook), new register/console (Model Catalogue tile pair), 2 integration surfaces.
7. **REVERSAL COST.** High. Scorecards ledgered; reversal removes MOAC gate — Canon 4 §26 violation. Records stay.

## WS-BUILD-ADAPTER-REGISTRY

1. **WHAT.** Adapter registry surface + no-model-for-class rendering. Rows C4-034, C4-035, C4-036. Component: `services/adapter_registry/` (registry writer + surface data). Contract: `Adapter.Registration.v0`. Record class: `Adapter.Registration` (Canon 9 §6). Task identity: `adapter.register.per_version`.
2. **CANON CLAUSES.** Canon 4 §34-§36 (adapter surface); Canon 5 §14 (Model Catalogue read-back).
3. **DEFINITION OF DONE.** Every adapter used in extraction is registered with version, MOAC scorecard reference, rights lineage. Missing model for a class renders as its own state (no silent fall-back). Verification: drill with an unregistered adapter fails admission.
4. **QUALITY EVIDENCE.** Contract test (registration shape). Uncurated sample: full adapter set over a drill week. Calibration under Canon 4 §35.
5. **DEPENDENCIES.** `WS-BUILD-MOAC-SCORECARD`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 2 components, 1 new contract, 2 integration surfaces.
7. **REVERSAL COST.** Medium.

---

# C. Ports (Ruling B new items)

## WS-BUILD-STREAMING-PORT

1. **WHAT.** Streaming port at the spine — anchors harvested `synisense/shield/streaming.py` (`WS-HARVEST-STREAMING` in Part 1) as a first-class port that answering surfaces call. Component: `services/synisense/shield/streaming.py` (post-harvest) + port shim. Contract: `Streaming.Frame.v0` (frozen — mirror of memory_plane_v0.contract_snapshot.json shape). Record class: `Streaming.Frame.Envelope` (Canon 9 §6). Task identity: `streaming.frame.per_session`.
2. **CANON CLAUSES.** Canon 1 §7.1 (Shield boundary); Canon 3 §12 (input seat — frames transit); Canon 7 §19 (plane activity envelope).
3. **DEFINITION OF DONE.** Every streamed answer session passes frames through this port; the port's shape is frozen under parity seat. Every RE-POINTed surface (`WS-REPOINT-ANSWERING-SURFACES`, Part 1) that streams calls this port. Verification: streaming drill (100 frames across sessions) shows envelope shape byte-identical to snapshot.
4. **QUALITY EVIDENCE.** Invariant class (frame-envelope). Uncurated sample: one drill day of streamed responses. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-HARVEST-STREAMING` (Part 1), `WS-WIRE-PARITY-EXTENSION`, gates `WS-REPOINT-ANSWERING-SURFACES` completion.
6. **CREDIT COST CLASS.** L. Justification: new register/console surface (port as a first-class integration surface).
7. **REVERSAL COST.** Medium. Streaming disabled; RE-POINT surfaces fall back to non-streamed responses.

## WS-BUILD-OBJECT-STORAGE-PORT

1. **WHAT.** Object-storage port at the spine — provides per-application object storage per Canon 7 §19-§23 memory-plane discipline. Component: `services/object_storage/` (port + plane-keyed writer + revocation). Contract: `ObjectStorage.Blob.v0` (frozen). Record class: `ObjectStorage.Blob.Reference` (Canon 9 §6). Task identity: `storage.blob.per_object`. **PROPOSAL (per Ruling B): this lands as an XL BUILD item; FL-P1-03 stays OPEN pending owner ratification.**
2. **CANON CLAUSES.** Canon 7 §19-§23 (per-application memory plane with plane-keyed storage); Canon 1 §12 (six-services boundary — storage as a service); Canon 9 §6 (record classes at storage boundary).
3. **DEFINITION OF DONE.** Every blob write/read is plane-keyed via task-identity + application-scope. Blob metadata (id, plane, application, uploaded-by, retention-class) lives in ledger. Revocation cascades per Canon 3 §26-§27. Verification: drill with per-application isolation fixture — cross-application read returns refusal.
4. **QUALITY EVIDENCE.** Invariant class (plane-key discipline test) + drill class (cross-application isolation). Uncurated sample: full drill week of blob operations; cross-application leak count = 0. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`. **Gates `WS-REBUILD-WORK-STUDIO-STORAGE`** (Part 1 — the 200+ export migration.)
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** New engine/authority (object-storage service does not exist at the spine today); estate-wide (every application will eventually store artefacts); its API shape is a new frozen contract that irreversibly defines how work_studio + future artefact-creating applications write. XL bar met on the new-engine axis alone; also meets estate-wide-wiring axis independently.
7. **REVERSAL COST.** VERY HIGH. Once blobs exist, they cannot be un-stored trivially; reversal = keep the blob store but stop writing new blobs; downstream applications lose the artefacts they wrote. Reader-migration reversibility is the canonical case (see `WS-REBUILD-WORK-STUDIO-STORAGE`).

---

# D. Integration (Canon 7)

## WS-BUILD-WEBHOOK

1. **WHAT.** Per-application webhook infrastructure for compliance-record notifications. Rows C7-009, C6-042. Component: `services/webhook/` (subscription registry + delivery + signing). Contract: `Webhook.Envelope.v0`. Record class: `Webhook.Delivery` (Canon 9 §6). Task identity: `webhook.deliver.per_event`.
2. **CANON CLAUSES.** Canon 7 §9 (webhook infrastructure); Canon 6 §11 (commissioning notifications); Canon 3 §33 (governance orchestration).
3. **DEFINITION OF DONE.** Applications register webhook subscriptions per compliance-record class; every write to a subscribed class fans out via signed deliveries. Delivery retries follow Canon 7 §9 discipline; failed deliveries ledgered.
4. **QUALITY EVIDENCE.** Contract test (envelope shape) + drill. Uncurated sample: 100 webhook deliveries across a drill week; retry rate + delivery hash. Calibration under Canon 7 §9.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 2 components, 1 new contract, 2 integration surfaces.
7. **REVERSAL COST.** Low. Reversal disables webhook delivery; applications poll instead.

## WS-BUILD-PLANE-PRECOMPUTE

1. **WHAT.** Per-application memory-plane precompute per Canon 7 §19-§23. Row C7-018. Component: `services/plane_precompute/` (background job runner over memory planes). Contract: `PlanePrecompute.Task.v0`. Record class: `Plane.Precompute` (Canon 9 §6). Task identity: `plane.precompute.per_job`.
2. **CANON CLAUSES.** Canon 7 §19-§23 (memory plane precompute); Canon 3 §33 (governance orchestration).
3. **DEFINITION OF DONE.** Precompute jobs run within per-application task identity; job metadata + result hash ledgered; Watch reads job activity envelope (via `WS-WIRE-WATCH-PLANE-ACTIVITY`, Part 1) without reading content.
4. **QUALITY EVIDENCE.** Contract test (task shape) + invariant (no content crosses the Watch reader boundary). Uncurated sample: full drill week of precompute jobs. Calibration under Canon 7 §19 + Canon 8 §4.13 W13.
5. **DEPENDENCIES.** `WS-BUILD-OBJECT-STORAGE-PORT`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-WATCH-PLANE-ACTIVITY`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3 components (job runner + plane reader + Watch envelope), new register (job class), 3 integration surfaces.
7. **REVERSAL COST.** Medium.

---

# E. Governance Ceremony (Canon 3 §24, §31, §33; Canon 6)

## WS-BUILD-VERIFICATION-RUNNER

1. **WHAT.** Compliance-Console-triggered live verification runner. Rows C3-039, C3-040, C3-041, C3-042. Component: `services/verification_runner/` (pack loader + executor + result writer). Contract: `Verification.Pack.v0` + `Verification.Result.v0`. Record class: `Verification.Run` (Canon 9 §6). Task identity: `verification.run.per_pack`.
2. **CANON CLAUSES.** Canon 3 §31 (verification packs); Canon 3 §33 (Compliance Console read-back); Canon 6 §11-§13 (commissioning verification).
3. **DEFINITION OF DONE.** Compliance owner triggers a verification pack from the Administration Console (`WS-HARVEST-CONSOLE-ADMINISTRATION`, Part 1); pack loads named tests from `tests/invariants/`; results write to ledger. Also invoked by `WS-BUILD-CEREMONY-REVERIFY` (Part 1) as the 5th step. Verification: drill runs one pack end-to-end.
4. **QUALITY EVIDENCE.** Contract test (pack + result shapes) + drill (compliance owner runs a pack). Uncurated sample: full pack catalogue across a drill week. Calibration under Canon 3 §31.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-CEREMONY-REVERIFY` (Part 1), `WS-HARVEST-CONSOLE-ADMINISTRATION` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3 components (runner + pack registry + result writer), new register/console (verification-runner surface), 3 integration surfaces.
7. **REVERSAL COST.** Medium.

## WS-BUILD-PROVE-ONE-RUN

1. **WHAT.** Canon 3 §33 "prove one run" export pack as single action. Rows C3-046, C3-047, C3-048. Component: `services/prove_one_run/` (pack compiler over ledger). Contract: `ProveOneRun.Pack.v0` (frozen). Record class: `ProveOneRun.Pack` (Canon 9 §6). Task identity: `prove_one_run.compile.per_run`.
2. **CANON CLAUSES.** Canon 3 §33 (prove-one-run + regulator pack); Canon 5 §21 (Prove-one-run panel; also §22-§23 Compliance Home).
3. **DEFINITION OF DONE.** For any run id, a single compile call emits a pack containing: admit row, declaration in force, rule versions consulted, retrieved evidence with hashes, trust receipts of outbound calls, verdicts, refusal receipts. Pack verifies offline by receipt signatures. Surface: rendered via `WS-MODIFY-PROVE-ONE-RUN-EXPORT` (Part 1) tile.
4. **QUALITY EVIDENCE.** Contract test (pack shape) + drill (offline verification of an exported pack). Uncurated sample: 20 exported packs across a drill week; offline-verify pass rate = 100%. Calibration under Canon 3 §33.
5. **DEPENDENCIES.** `WS-WIRE-LEDGER-MATRIX` (Part 1), `WS-BUILD-RECORD-MATRIX`, `WS-MODIFY-PROVE-ONE-RUN-EXPORT` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3 components (compiler + hasher + surface), new register (pack class), 3 integration surfaces (ledger reader, hash writer, surface).
7. **REVERSAL COST.** Medium. Packs signed and delivered stay; reversal disables new compilation.

## WS-BUILD-SETUP-CONSOLE

1. **WHAT.** Setup surface + signed setup record artefact. Rows C6-007..C6-012. Component: `services/setup_console/` (setup flow + record writer). Contract: `Setup.Record.v0`. Record class: `Setup.Record` (Canon 9 §6). Task identity: `setup.commit.per_actor`.
2. **CANON CLAUSES.** Canon 6 §3 (setup declarations); Canon 6 §7 (signed setup record).
3. **DEFINITION OF DONE.** Setup flow captures actor identity, declarations, initial connectors, initial policies; produces a signed setup record. Record ledgered; parity-seat frozen. Verification: drill runs a full setup end-to-end and produces a valid signed record.
4. **QUALITY EVIDENCE.** Contract test + drill. Uncurated sample: 5 setup runs across drills. Calibration under Canon 6 §3.
5. **DEPENDENCIES.** `WS-BUILD-DECL`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`, `WS-HARVEST-CONSOLE-INTEGRATION` (Part 1 — setup pages).
6. **CREDIT COST CLASS.** L. Justification: 3 components (flow + record + surface), new register, 3 integration surfaces.
7. **REVERSAL COST.** Medium.

## WS-BUILD-DAY-ZERO

1. **WHAT.** Estate map + commissioning certificate + Verification-Runner packs + Watch drills — the Day-Zero bundle. Rows C6-013..C6-022. Component: `services/day_zero/` (orchestrator over setup + estate scan + verification + drills). Contract: `Commissioning.Certificate.v0`. Record class: `Commissioning.Certificate` (Canon 9 §6). Task identity: `day_zero.commission.per_instance`.
2. **CANON CLAUSES.** Canon 6 §11-§13 (commissioning certificate); Canon 8 §5 W-drills (Watch fitness on day zero).
3. **DEFINITION OF DONE.** Day-zero orchestration produces: estate map + commissioning certificate signed by all seat-holders + Watch drill fitness receipt + Verification-Runner packs for all standing invariants. Certificate ledgered.
4. **QUALITY EVIDENCE.** Contract test + drill (full day-zero simulation on a fixture instance). Uncurated sample: every day-zero produces the four artefacts. Calibration under Canon 6 §11.
5. **DEPENDENCIES.** `WS-BUILD-SETUP-CONSOLE`, `WS-BUILD-VERIFICATION-RUNNER`, `WS-BUILD-WATCH-DRILL-HARNESS`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components, new register (commissioning certificate).
7. **REVERSAL COST.** Medium.

## WS-BUILD-RULEBOOK-SURFACE

1. **WHAT.** Compliance Rulebook read-back surface. Rows C3-030..C3-032, C3-034, C3-035, C7-D12. Component: `services/rulebook/` (read-back writer + surface data). Contract: `Rulebook.Rule.v0`. Record class: `Rulebook.Rule` (Canon 9 §6). Task identity: `rulebook.read_back.per_rule`.
2. **CANON CLAUSES.** Canon 3 §25 (rulebook); Canon 5 §25 (rulebook read-back at Compliance Home); Canon 7 §D12 defect (rule-on-paper flag).
3. **DEFINITION OF DONE.** Every governance rule visible in the rulebook shows: current text, effective date, ceremony trail (proposed→countersigned→waited→applied→re-verified via `WS-BUILD-CEREMONY-REVERIFY`), rule-on-paper flag if not yet applied. Surface rendered by `WS-HARVEST-CONSOLE-COMPLIANCE` (Part 1).
4. **QUALITY EVIDENCE.** Contract test (rule shape) + inventory audit (every rule has ceremony trail). Uncurated sample: full rulebook over drill week. Calibration under Canon 3 §25.
5. **DEPENDENCIES.** `WS-BUILD-CEREMONY-REVERIFY` (Part 1), `WS-BUILD-RECORD-MATRIX`, `WS-HARVEST-CONSOLE-COMPLIANCE` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3 components (rule writer + ceremony reader + surface data), new register.
7. **REVERSAL COST.** Medium.

---

# F. Interface BUILD (Canon 5, no Extraction-Akki donor)

Each of these tiles either has no existing page in the Extraction-Akki frontend (`WS-BUILD-*`) OR carries copy that must be built verbatim from canon (`WS-BUILD-REFUSAL-CARD-COPY`). Every tile appears as a BUILD-marked open slot inside the harvested console tile-groups (Part 1). All carry `FIXTURE PENDING: reference screenshot for tile-grid-plus-detail-card grammar`.

## WS-BUILD-CONSOLE-EXTRACTION-MODEL-CATALOGUE

1. **WHAT.** Extraction Console Model Catalogue tile — MOAC scorecard render per adapter version. Row C5-014. Component: new frontend tile + backend data provider. Contract: `Model.Catalogue.Row.v0`. Record class: `MOAC.Scorecard` (reader). Task identity: `catalogue.render.per_adapter`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 5 §14 (Model Catalogue); Canon 4 §26 (MOAC).
3. **DEFINITION OF DONE.** Tile renders every adapter version with its MOAC scorecard, drift indicator, uncurated-sample provenance, rights lineage. Row without a scorecard renders as its own state.
4. **QUALITY EVIDENCE.** Inventory audit (tile row-count = adapter-version-count). Calibration under Canon 5 §14.
5. **DEPENDENCIES.** `WS-BUILD-MOAC-SCORECARD`, `WS-BUILD-ADAPTER-REGISTRY`, `WS-HARVEST-CONSOLE-EXTRACTION` (Part 1 — the parent tile-group), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 1-2 components, 1 new contract (row shape), 2 integration surfaces.
7. **REVERSAL COST.** Low.

## WS-BUILD-BATCH-BOARD-SURFACE

1. **WHAT.** Batch Board surface with quarantined batches. Row C5-018. Component: frontend tile + backend data feed from `WS-HARVEST-BATCH-QUARANTINE` (Part 1). Contract: `Batch.Board.Row.v0`. Record class: `Batch.QuarantineDecision` (reader). Task identity: `batch_board.render.per_batch`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 4 §34.1 Batch Board; Canon 5 §17 Extraction Console.
3. **DEFINITION OF DONE.** Tile renders every batch with quarantine verdict + reason; quarantined batches highlighted; un-quarantined batches show pass state. No content leaks (Canon 4 §34.1 discipline).
4. **QUALITY EVIDENCE.** Inventory audit + invariant (no content leak). Calibration under Canon 4 §34.1.
5. **DEPENDENCIES.** `WS-HARVEST-BATCH-QUARANTINE` (Part 1), `WS-HARVEST-CONSOLE-EXTRACTION` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M. Justification: 1-2 components, 1 new contract, 2 integration surfaces.
7. **REVERSAL COST.** Low.

## WS-BUILD-QUALITY-OBSERVATION

1. **WHAT.** Quality Observation tile with Critic-Seam calibration stale surface. Row C5-020. Component: frontend tile + backend Critic-Seam calibration state reader. Contract: `Quality.Observation.Panel.v0`. Record class: `Critic.Verdict` (reader). Task identity: `quality_observation.render.per_check`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 5 §18 (Quality Observation); Canon 7 §33 (Critic Seam calibration); Canon 4 §32 (quality matrix).
3. **DEFINITION OF DONE.** Tile renders Critic Seam calibration status per adapter class; stale-calibration surface highlighted; drift alarms per Canon 4 §32.
4. **QUALITY EVIDENCE.** Inventory audit + calibration-stale drill. Calibration under Canon 4 §32.
5. **DEPENDENCIES.** `WS-HARVEST-CRITIC-SEAM` (Part 1), `WS-WIRE-CRITIC-INTO-ANSWERING` (Part 1), `WS-HARVEST-CONSOLE-EXTRACTION` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

## WS-BUILD-AGENT-ASSUMED-CHIP

1. **WHAT.** Agent-assumed chip render (chip that flags claims produced by the agent's own inference vs quoted evidence). Row C5-008. Component: new frontend chip component. Contract: `Agent.Assumed.Chip.v0`. Record class: none (surface-only). Task identity: `agent_assumed.render.per_claim`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 5 §2.5 (Agent-assumed marking); Canon 5 §9.3 (Agent-assumed chip component).
3. **DEFINITION OF DONE.** Every claim carrying agent-derived (not-quoted) inference renders with the agent-assumed chip. Existing test `gate1_class_inseparable.test.js` extends to require chip presence.
4. **QUALITY EVIDENCE.** Invariant test (chip-presence per agent-derived claim). Uncurated sample: 100 answer envelopes; agent-assumed classifier accuracy per calibration. Calibration under Canon 5 §2.5.
5. **DEPENDENCIES.** `WS-HARVEST-CLASS-CHIP-LIBRARY` (Part 1), `WS-BUILD-ANSWER-CARD`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** S.
7. **REVERSAL COST.** Very low.

## WS-BUILD-REFUSAL-CARD-COPY

1. **WHAT.** Verbatim Canon 5 §9.2 refusal card COPY authored + registered in the refusal-family taxonomy (extends `services/memory/memory_refusal_reasons.v0.json`). Rows C5-005, C5-006, C5-007, C7-D03. Component: taxonomy JSON extension + copy authoring. Contract: refusal-reason JSON snapshot (extends existing frozen shape via `WS-WIRE-PARITY-EXTENSION`). Record class: `Refusal.Reason` (writer). Task identity: `refusal.copy.per_family`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 5 §9.2 (verbatim refusal card copy); Canon 1 §7.1 (refusal recorded); Canon 3 §17 (refusal shapes catalogued).
3. **DEFINITION OF DONE.** Every canon-listed refusal family has a verbatim copy entry in the taxonomy JSON. `WS-HARVEST-REFUSAL-CARD` (Part 1 — the render) reads these entries. Copy is byte-identical to Canon 5 §9.2 text.
4. **QUALITY EVIDENCE.** Invariant test (byte-identical copy render) + inventory audit (every family has a copy entry). Calibration under Canon 5 §9.2.
5. **DEPENDENCIES.** `WS-HARVEST-REFUSAL-CARD` (Part 1), `WS-WIRE-REFUSAL-FAMILY` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** S. Justification: 1 component (JSON extension), 0 new contracts (extends existing), 1 integration surface.
7. **REVERSAL COST.** Very low.

## WS-BUILD-THREE-LENSES

1. **WHAT.** Three lenses (Answer / Reasoning / Raw trail) over one object. Rows C5-045..C5-048, C7-006 (envelope class-chip render). Component: new frontend tile with three panels + backend three-panel data provider. Contract: `Three.Lenses.Envelope.v0`. Record class: `Answer.Envelope` (Canon 9 §6). Task identity: `answer.three_lenses.render.per_object`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 5 §37.1 (three lenses); Canon 5 §2 (class chip inseparable per lens).
3. **DEFINITION OF DONE.** Every answer surface renders three lenses over the same object; class chip present in every lens; refusal card can appear in any lens.
4. **QUALITY EVIDENCE.** Invariant test (three-panel + class-chip presence) + drill (10 answer sessions rendered across three lenses).
5. **DEPENDENCIES.** `WS-HARVEST-CLASS-CHIP-LIBRARY` (Part 1), `WS-BUILD-ANSWER-CARD`, `WS-REPOINT-ANSWERING-SURFACES` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

## WS-BUILD-ANSWER-CARD

1. **WHAT.** Answer card (evidence strip + honesty strip + actions). Rows C5-049, C5-050, C5-051. Component: new frontend card + backend data provider. Contract: `Answer.Card.v0`. Record class: `Answer.Envelope` (reader). Task identity: `answer_card.render.per_answer`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 5 §37 (Ask surface); Canon 5 §37.4 (machine form / answer envelope).
3. **DEFINITION OF DONE.** Every answer renders as an answer card with evidence + honesty + actions strips. Card is source-of-truth for the answer envelope.
4. **QUALITY EVIDENCE.** Invariant test (card shape). Uncurated sample: 100 answers across drill week. Calibration under Canon 5 §37.
5. **DEPENDENCIES.** `WS-HARVEST-CLASS-CHIP-LIBRARY` (Part 1), `WS-HARVEST-REFUSAL-CARD` (Part 1), `WS-REPOINT-ANSWERING-SURFACES` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

## WS-BUILD-FIVE-PILLARS

1. **WHAT.** Five-pillar router (Canon 5 §40): Ask · Work · Lead · Learn · Build + 3rd Party. Row C5-052. Component: new frontend router + pillar-registry backend. Contract: `Pillar.Registration.v0`. Record class: none (surface + registration). Task identity: `pillar.router.per_navigation`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 5 §40 (five pillars); FL-OQ-04 (four-vs-five console taxonomy — pillars are distinct from consoles).
3. **DEFINITION OF DONE.** Every user surfaces routes through one of the five pillars; Canon-5 conformance audit = 100%.
4. **QUALITY EVIDENCE.** Inventory audit (surface-list → pillar-list). Calibration under Canon 5 §40.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR` (Part 1), `WS-BUILD-CONTROL-BAND`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: new register/console surface (five-pillar taxonomy).
7. **REVERSAL COST.** Medium (pillar taxonomy touches every surface's placement).

## WS-BUILD-PULSE-NEWS

1. **WHAT.** Pulse + News apps for the Lead pillar. Row C5-053. Component: new Lead-pillar applications. Contract: `Pulse.Post.v0`, `News.Item.v0`. Record class: `Pulse.Post`, `News.Item` (Canon 9 §6). Task identity: `pulse.compose.per_post`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 5 §40 (Lead pillar apps); Canon 5 §43 (Pulse + News).
3. **DEFINITION OF DONE.** Two Lead-pillar apps render as tiles inside the Lead pillar router; Pulse is workspace-internal, News aggregates canon-tagged updates.
4. **QUALITY EVIDENCE.** Contract test + inventory audit.
5. **DEPENDENCIES.** `WS-BUILD-FIVE-PILLARS`, `WS-HARVEST-SHELL-GRAMMAR` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

## WS-BUILD-STUDIO

1. **WHAT.** Studio — application composer surface for the Build pillar. Rows C5-055, C5-060. Component: new Build-pillar application. Contract: `Studio.Composition.v0`. Record class: `Studio.Composition`. Task identity: `studio.compose.per_app`. **FIXTURE PENDING + FL-OQ-05 pending.**
2. **CANON CLAUSES.** Canon 5 §42 (designed, not sourced); Canon 5 §43 Studio (per row extraction; scope resolution pending FL-OQ-05).
3. **DEFINITION OF DONE.** _Partial pending FL-OQ-05_: Studio surfaces expose app composition primitives per Canon 5 §42; scope of "compose" — does it include storage-plane assignment? — governed by owner ruling.
4. **QUALITY EVIDENCE.** Contract test + drill (one Studio-composed app end-to-end).
5. **DEPENDENCIES.** `WS-BUILD-FIVE-PILLARS`, `WS-BUILD-OBJECT-STORAGE-PORT`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`. Scope-gated by FL-OQ-05.
6. **CREDIT COST CLASS.** L (baseline scope) → XL if scope expands to storage-plane composition. Reclassify on FL-OQ-05 ruling.
7. **REVERSAL COST.** Medium-high depending on scope.

## WS-BUILD-LEARN-PILLAR

1. **WHAT.** Learn-pillar surfaces (Canon 5 §40 fifth pillar). Row C5-057. Component: new Learn-pillar applications. Contract: `Learn.Module.v0`. Record class: `Learn.Module.Interaction`. Task identity: `learn.module.per_interaction`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 5 §40 (five pillars — Learn); Canon 5 §43 (Learn surfaces).
3. **DEFINITION OF DONE.** Learn tiles render under Learn pillar; interactions ledgered per Canon 9 §6 without content leaking.
4. **QUALITY EVIDENCE.** Contract test + inventory audit.
5. **DEPENDENCIES.** `WS-BUILD-FIVE-PILLARS`, `WS-HARVEST-SHELL-GRAMMAR` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

## WS-BUILD-REFERENCE-APP

1. **WHAT.** Reference App (Ask) — the canonical Ask app surface. Rows C5-043, C5-044, C6-038..C6-043. Component: new Ask pillar-application. Contract: `Ask.Session.v0`. Record class: `Ask.Session`. Task identity: `ask.session.per_actor`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 5 §37 (Ask); Canon 5 §43-§44 (Reference App); Canon 6 §5-§7 (working-rhythm).
3. **DEFINITION OF DONE.** Ask app renders three-lenses (`WS-BUILD-THREE-LENSES`) over answer envelope; agent-assumed chip present per Canon 5 §2.5; refusal card renders verbatim per Canon 5 §9.2.
4. **QUALITY EVIDENCE.** Drill (10 Ask sessions across various shapes). Calibration under Canon 5 §37.
5. **DEPENDENCIES.** `WS-BUILD-THREE-LENSES`, `WS-BUILD-ANSWER-CARD`, `WS-BUILD-AGENT-ASSUMED-CHIP`, `WS-HARVEST-REFUSAL-CARD` (Part 1), `WS-REPOINT-ANSWERING-SURFACES` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components, new register (Ask session class).
7. **REVERSAL COST.** Medium.

## WS-BUILD-CONTROL-BAND

1. **WHAT.** Control Band (Connect / Estate Map / Rulebook / Access / Watch). Rows C5-058, C5-059. Component: new frontend control-band component + wiring to five sub-tiles. Contract: `Control.Band.Row.v0`. Record class: none (surface). Task identity: `control_band.render.per_user`. **FIXTURE PENDING.**
2. **CANON CLAUSES.** Canon 5 §41 (Control Band).
3. **DEFINITION OF DONE.** Every user surface renders the Control Band with five items; each item links to the corresponding Canon-5 console tile.
4. **QUALITY EVIDENCE.** Inventory audit (control-band item count = 5). Calibration under Canon 5 §41.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR` (Part 1), `WS-BUILD-FIVE-PILLARS`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Low.

---

# G. Watch (Canon 8, 60 rows → 15 mechanism-scoped items)

## WS-BUILD-WATCH-FOUNDATION

1. **WHAT.** Watch foundational discipline: machine-speed + cannot-act-unobserved + proves-own-fitness + sensing→verdict→response→action seam. Rows C8-004..C8-008. Component: `services/watch/foundation.py` + shared discipline module. Contract: `Watch.Attestation.v0`. Record class: `Watch.Attestation` (Canon 9 §6). Task identity: `watch.attestation.per_cycle`.
2. **CANON CLAUSES.** Canon 8 §1-§4 (What the Watch Is); Canon 8 §4.14 W14 (Self-proving); Canon 8 §5 (Macho — Eyes).
3. **DEFINITION OF DONE.** Machine-speed operative parameter measured continuously (Canon 8 §18); no Watch action executes without a receipt landing atomically (Canon 8 §4); fitness attested per cycle by drill receipts.
4. **QUALITY EVIDENCE.** Invariant class (machine-speed bound, receipt-atomicity gate). Uncurated sample: full drill week; violations = 0. Calibration under Canon 8 §18.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** New authority — the Watch is a Canon-1 §7.1 peer authority to governance. Its foundational discipline (machine-speed, cannot-act-unobserved, proves-own-fitness) is estate-wide (crosses every request path). XL bar met on both new-authority AND estate-wide-wiring axes.
7. **REVERSAL COST.** Very high — Watch attestations append-only; a bad build ledgers unreliable attestations forever.

## WS-BUILD-WATCH-ACTORS

1. **WHAT.** Macho (sensor) + Mkono (responder) + Witness — three Watch actors bundled per Canon 8 §6 seam. Rows C8-009..C8-013, C8-055..C8-057, C8-059. Component: `services/watch/macho/`, `services/watch/mkono/`, `services/watch/witness/`. Contracts: `Watch.Verdict.v0` (Macho), `Watch.Action.v0` (Mkono), `Watch.Attestation.v0` (Witness). Record classes: `Watch.Verdict`, `Watch.Action`, `Watch.Attestation` (Canon 9 §6). Task identities: `watch.macho.sense`, `watch.mkono.respond`, `watch.witness.attest`.
2. **CANON CLAUSES.** Canon 8 §5 (Macho); Canon 8 §7 (Mkono); Canon 8 §16 (Witness); Canon 8 §21 seam.
3. **DEFINITION OF DONE.** Each actor writes only its own record class (Macho writes verdicts; Mkono writes actions; Witness writes attestations); actors read shared record. Verification: drill fires three-actor cycle end-to-end.
4. **QUALITY EVIDENCE.** Invariant class (writer-role exclusivity per Canon 9 §6). Uncurated sample: full drill week. Calibration under Canon 8 §5-§7.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-FOUNDATION`, `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** Three new authorities in one item (Macho, Mkono, Witness — each a Canon-8 named actor with its own record class); estate-wide (every request path passes through Macho); qualifies XL on both axes.
7. **REVERSAL COST.** Very high — actor verdicts/actions append-only.

## WS-BUILD-WATCH-RECONCILER

1. **WHAT.** Watch reconciler — Macho verdict × Mkono action × Governance record reconciliation loop per Canon 8 §14-§15. Component: `services/watch/reconciler.py`. Contract: `Watch.Reconciliation.v0`. Record class: `Watch.Reconciliation` (Canon 9 §6). Task identity: `watch.reconciler.per_cycle`. **Ruling-1 linkage: this item's DEMONSTRATED FIRING is the second precondition for `WS-CONTRADICTION-PURPOSE-GATE` strip.**
2. **CANON CLAUSES.** Canon 8 §14-§15 (With the Governing Authority + Disagreement); Canon 9 §6 (record matrix — reconciliation handoff `governance→Watch verdict`); Ruling 1 (transition condition).
3. **DEFINITION OF DONE.** Reconciler runs on every cycle; produces a `Watch.Reconciliation` record with fields (governance-verdict-id, watch-verdict-id, agree|disagree, disagreement-reason-if-any). **Ruling-1 demonstrated-firing evidence:** one drill produces a shared-record reconciliation event with an observable reconciliation row, cross-cited to the ledger. This satisfies precondition (b) for the purpose-gate strip.
4. **QUALITY EVIDENCE.** Invariant class (reconciliation-per-cycle gate) + drill class (shared-record fixture producing reconciliation event). Uncurated sample: every cycle produces one reconciliation record. Calibration under Canon 8 §14-§15.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-DECL` (Ruling-1 paired precondition), `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-HANDOFF-REGISTRY`, `WS-WIRE-PARITY-EXTENSION`. **Gates:** `WS-CONTRADICTION-PURPOSE-GATE` strip lawfulness.
6. **CREDIT COST CLASS.** L. Justification: 2 components (reconciler + handoff), 1 new contract, 3 integration surfaces (Macho reader + governance reader + reconciliation writer).
7. **REVERSAL COST.** Very high — Ruling-1 strip cannot proceed lawfully without this firing. Reconciliation records append-only.

## WS-BUILD-WATCH-MARK-REGISTRY

1. **WHAT.** Watch Mark Register — writer, dimensions, de-mark two-signature discipline. Rows C8-014..C8-018. Component: `services/watch/mark_registry/`. Contract: `Watch.Mark.v0`. Record class: `Watch.Mark` (Canon 9 §6). Task identity: `watch.mark.per_placement`.
2. **CANON CLAUSES.** Canon 8 §10 (The Mark); Canon 9 §6 (mark record class).
3. **DEFINITION OF DONE.** Every mark placement writes a `Watch.Mark` row with dimensions; de-mark requires two signatures (Canon 8 §10 discipline); marks never rendered on public surfaces (Canon 8 §4.13 W13).
4. **QUALITY EVIDENCE.** Invariant class (two-signature de-mark gate + no-render W13). Uncurated sample: full drill week of mark placements. Calibration under Canon 8 §10.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 2 components + new register.
7. **REVERSAL COST.** Very high — marks append-only.

## WS-BUILD-WATCH-CONTAINMENT

1. **WHAT.** Containment machinery — bounded, reversible, witnessed acts per Canon 8 §4.3 W3; expiries + reconciliation on release. Rows C8-019..C8-026. Component: `services/watch/containment/`. Contract: `Watch.Containment.v0` + `Watch.Containment.Release.v0`. Record class: `Watch.Containment` (Canon 9 §6). Task identity: `watch.contain.per_target`.
2. **CANON CLAUSES.** Canon 8 §4.3 W3 (reversible + bounded + witnessed); Canon 8 §8 (Four Layers of Constraint); Canon 8 §17 (expiry discipline).
3. **DEFINITION OF DONE.** Every containment is bounded (has explicit scope + duration); reversible (release possible); witnessed (Witness attestation recorded). Expiries do NOT auto-extend (Canon 8 §21 W-negative). On release, reconciliation record (`WS-BUILD-WATCH-RECONCILER`) fires.
4. **QUALITY EVIDENCE.** Invariant class (bounded-scope + no-auto-extend gates) + drill (containment lifecycle end-to-end). Calibration under Canon 8 §17.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-RECONCILER`, `WS-BUILD-WATCH-ATTESTATION-WITNESS`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

## WS-BUILD-WATCH-MIRAGE

1. **WHAT.** Sarabi — the misdirection arm. Rows C8-020..C8-021, C8-036 (drill: planted credential touched + severance executed). Component: `services/watch/sarabi/mirage.py`. Contract: `Watch.Mirage.v0`. Record class: `Watch.Mirage.Placement` (Canon 9 §6). Task identity: `watch.mirage.per_placement`.
2. **CANON CLAUSES.** Canon 8 §11 (Sarabi — Misdirection Arm); Canon 8 §12 (Duties Deception Carries).
3. **DEFINITION OF DONE.** Mirages placed as planted credentials/paths; touch triggers containment. Mirage placement + touch events ledgered. No surface renders mirage construction (Canon 8 §21 W-negative — enforced via AST discipline check).
4. **QUALITY EVIDENCE.** Invariant class (no-mirage-render AST gate) + drill (planted-credential-touched fixture). Calibration under Canon 8 §11.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-CONTAINMENT`, `WS-BUILD-WATCH-MARK-REGISTRY`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** High.

## WS-BUILD-WATCH-SIGNATURE-STORE

1. **WHAT.** Behavioural profile / signature store — no-reader W13 discipline. Rows C8-018, C8-058, C8-064, C8-045 (constitutional negative). Component: `services/watch/signature_store/`. Contract: `Watch.Signature.v0`. Record class: `Watch.Signature` (Canon 9 §6 — writer = signature substrate, readers = NO surface, ever, per W13). Task identity: `watch.signature.per_actor`.
2. **CANON CLAUSES.** Canon 8 §4.13 W13 (profile is armory, not inventory); Canon 8 §9 (Signature).
3. **DEFINITION OF DONE.** Signatures written; NO surface reads (AST discipline check across all surfaces). Behavioural profile internals never rendered anywhere. Export blocked (Canon 8 §21 W-negative).
4. **QUALITY EVIDENCE.** Invariant class (AST no-reader gate). Uncurated sample: full codebase AST scan; reader count = 0. Calibration under Canon 8 §4.13.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high (any leak is a Canon 8 W13 violation; leaked signatures cannot be un-leaked).

## WS-BUILD-WATCH-DECISIONS-PANEL

1. **WHAT.** Reserved decisions + panel discipline. Rows C8-027..C8-029, C8-050 (no reserved-decision executed by machine). Component: `services/watch/reserved_decisions/`. Contract: `Watch.Reserved.Decision.v0`. Record class: `Watch.Reserved.Decision` (Canon 9 §6). Task identity: `watch.reserved_decision.per_case`.
2. **CANON CLAUSES.** Canon 8 §13 (Watch Console); Canon 8 §19 (Quality Parameters).
3. **DEFINITION OF DONE.** Reserved decisions never executed by machine (Canon 8 §21 W-negative); require Watch-officer signature (Canon 8 §13). Panel renders inside Watch Console (`WS-BUILD-CONSOLE-WATCH`).
4. **QUALITY EVIDENCE.** Invariant class (no-machine-execution gate) + drill. Calibration under Canon 8 §19.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-CONSOLE-WATCH`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

## WS-BUILD-WATCH-DAY

1. **WHAT.** Watch officer's day — what officer reads/does/NEVER does. Rows C8-030..C8-033. Component: Watch-officer-day flow inside Watch Console. Contract: `Watch.Officer.Session.v0`. Record class: `Watch.Officer.Session` (Canon 9 §6). Task identity: `watch.officer.session.per_shift`.
2. **CANON CLAUSES.** Canon 8 §21 (What This Canon Comes Down To — officer discipline).
3. **DEFINITION OF DONE.** Watch officer's session ledgered; officer reads state band + record + under-watch panel + decisions panel; officer NEVER tunes thresholds (Canon 8 §21 W-negative — no threshold visible for tuning).
4. **QUALITY EVIDENCE.** Invariant class (no-threshold-render AST gate) + drill (officer day walk-through). Calibration under Canon 8 §21.
5. **DEPENDENCIES.** `WS-BUILD-CONSOLE-WATCH`, `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-DECISIONS-PANEL`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Medium.

## WS-BUILD-WATCH-DRILL-HARNESS

1. **WHAT.** Watch drill harness — standing drills + fitness in receipts. Rows C8-034..C8-039. Component: `services/watch/drills/` (drill runner + fitness computer). Contract: `Watch.Drill.Receipt.v0`. Record class: `Watch.Drill.Receipt` (Canon 9 §6). Task identity: `watch.drill.per_run`.
2. **CANON CLAUSES.** Canon 8 §5 W-drills; Canon 8 §19 Quality Parameters (fitness); Canon 8 §4.14 W14 (self-proving).
3. **DEFINITION OF DONE.** Drills run on fixed cadence; each produces a receipt (Canon 9 §3 attestation shape). Fitness stated only via receipts (Canon 8 §21 no self-attestation). Verification: drill week produces receipts for every scheduled drill class.
4. **QUALITY EVIDENCE.** Contract test (receipt shape) + drill week. Uncurated sample: every scheduled drill in a week. Calibration under Canon 8 §19.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-MIRAGE`, `WS-BUILD-WATCH-CONTAINMENT`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

## WS-BUILD-WATCH-AUTHORITY-PEERAGE

1. **WHAT.** Watch × Governance peerage — disagreement + task identity + new-entry-only correction. Rows C8-040..C8-044. Component: `services/watch/peerage/`. Contract: `Watch.Disagreement.v0`. Record class: `Watch.Disagreement` (Canon 9 §6). Task identity: `watch.peerage.disagree.per_event`.
2. **CANON CLAUSES.** Canon 8 §14-§15 (peerage + disagreement); Canon 8 §4.12 W12 (peer, not subordinate); Canon 8 §4.11 W11 (one task, one identity).
3. **DEFINITION OF DONE.** Neither authority commands the other. Disagreements ledgered; correction is by new entry only (Canon 8 §21 no in-place amend). Task identity discipline enforced per W11.
4. **QUALITY EVIDENCE.** Invariant class (no-command AST gate + new-entry-only invariant). Calibration under Canon 8 §14-§15.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-RECONCILER`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

## WS-BUILD-WATCH-RECORD-CLASSES

1. **WHAT.** All Watch record classes writers — verdict/action/marks/behavioural-profiles/attestation writer discipline. Rows C8-055..C8-059. Component: matrix entries in `WS-BUILD-RECORD-MATRIX` for every Watch class. Contract: matrix rows for verdict, action, mark, signature, attestation. Task identity: `watch.record.per_write`.
2. **CANON CLAUSES.** Canon 9 §6-§18 (record matrix); Canon 8 §21-§59 (Watch record classes).
3. **DEFINITION OF DONE.** Every Watch record class has an exclusive writer entry in the Record Matrix; readers explicitly enumerated per class (including the empty reader-list for behavioural profiles per W13).
4. **QUALITY EVIDENCE.** Matrix inventory audit. Calibration under Canon 9 §6.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-SIGNATURE-STORE`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Very high.

## WS-BUILD-WATCH-TO-CIF

1. **WHAT.** Watch findings crossing to CIF as detection input; only ratified frames cross back. Rows C2-014, C8-066..C8-068. Component: `services/watch/to_cif/`. Contract: `Watch.CIF.Handoff.v0`. Record class: `Watch.CIF.Handoff` (Canon 9 §6). Task identity: `watch.to_cif.per_finding`.
2. **CANON CLAUSES.** Canon 2 §6 (engine walls — CIF origination port); Canon 8 §21 (Watch/CIF interface); Canon 9 §6 handoff `Watch findings→CIF`.
3. **DEFINITION OF DONE.** Watch findings arrive at CIF as detection input under CIF's origination port. Nothing crosses back except ratified frames through the coach seat. Watch drills operate under CIF's permanent bound (Watch may never certify CIF).
4. **QUALITY EVIDENCE.** Contract test (handoff shape) + drill (Watch finding → CIF detection). Calibration under Canon 2 §6.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-CIF-COACH-SEAT`, `WS-CIF-DETECTION`, `WS-BUILD-HANDOFF-REGISTRY`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** High.

## WS-BUILD-WATCH-ATTESTATION-WITNESS

1. **WHAT.** Witness attestation infrastructure — the third actor. Rows C8-016 (Witness), C8-059 (writer). Component: `services/watch/witness/`. Contract: `Watch.Witness.Attestation.v0`. Record class: `Watch.Witness.Attestation` (Canon 9 §6). Task identity: `watch.witness.attest.per_event`.
2. **CANON CLAUSES.** Canon 8 §16 (The Witness); Canon 8 §4.10 W10 (the watcher is watched from outside).
3. **DEFINITION OF DONE.** Every containment + reserved-decision + Watch-officer session carries a Witness attestation. Attestations are the only evidence Watch may cite for its own fitness (Canon 8 §21).
4. **QUALITY EVIDENCE.** Invariant class (attestation-per-Watch-act gate). Calibration under Canon 8 §16.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-CONTAINMENT`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Very high.

## WS-BUILD-S6-WATCH-SERVICE

1. **WHAT.** Canon 1 §12 S6 — continuous machine-speed detection/response Watch service sentence. Row C1-069. Component: `services/watch/service.py` (top-level Canon-1 six-services entry point wiring). Contract: `Watch.Service.Registration.v0`. Record class: N/A. Task identity: `watch.service.per_instance`.
2. **CANON CLAUSES.** Canon 1 §12 (six services); Canon 8 §1 (What the Watch Is).
3. **DEFINITION OF DONE.** Watch appears as the sixth service at the platform boundary; every application crossing the boundary passes Watch scrutiny (Canon 1 §7.1 peer authority). Verification: platform-boundary audit shows six services live.
4. **QUALITY EVIDENCE.** Inventory audit (six-services listing) + drill. Calibration under Canon 1 §12.
5. **DEPENDENCIES.** `WS-BUILD-WATCH-FOUNDATION`, `WS-BUILD-WATCH-ACTORS`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Very high.

## WS-BUILD-CONSOLE-WATCH

1. **WHAT.** Watch Console as the fourth tile-group under the Admin surface's tile-grid-plus-detail-card grammar per Instruction 02. Tiles (four, verbatim from Canon 8 §13): `State` · `Record` · `Under Watch` · `Decisions`. Component: new frontend Watch-Console + backend data feeds. Contract: `Watch.Console.Tile.v0`. Record class: consumes Watch record classes (reader only). Task identity: sessions run under Watch identity per Canon 9. **FIXTURE PENDING: reference screenshot.**
2. **CANON CLAUSES.** Canon 8 §13 (Watch Console — four panels); Canon 5 §10 (four consoles + Watch as fourth group per Instruction 02); Ruling 3 (Instruction 02).
3. **DEFINITION OF DONE.** Watch Console renders as a fourth tile-group with EXACTLY four tiles named `State`, `Record`, `Under Watch`, `Decisions`. **Watch-officer role-gated** (only watch-officer role sees the group). **Sessions run under Watch identity per Canon 9 (Task Identity Register).** **NEVER nested under Trust Center or any Compliance-Console tile — placement invariant test asserts this.** Verification: role-audit + placement-audit.
4. **QUALITY EVIDENCE.** Inventory audit (four-tile invariant + placement invariant + role-gate) + drill (watch-officer session end-to-end). Calibration under Canon 8 §13 + Instruction 02.
5. **DEPENDENCIES.** `WS-HARVEST-SHELL-GRAMMAR` (Part 1), `WS-BUILD-WATCH-ACTORS`, `WS-BUILD-WATCH-MARK-REGISTRY`, `WS-BUILD-WATCH-DECISIONS-PANEL`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-WIRE-PARITY-EXTENSION`. Reference screenshot pending (FL-P1-14).
6. **CREDIT COST CLASS.** L. Justification: 3+ components (4 tiles), new register/console (Watch tile-group), 3 integration surfaces (shell + Watch record classes + role-gate).
7. **REVERSAL COST.** Very high — placement change post-launch would break Instruction 02 explicit constraint; Watch-officer credentials outside the group is a Canon 8 §21 W-negative violation.

---

# H. Mkondo Charter (Canon 9, 45 rows → 6 items)

## WS-BUILD-MKONDO-CHARTER

1. **WHAT.** Structure-only orchestration service — Mkondo maintains three registers, answers-here-not-memory. Rows C9-001..C9-003, C9-043..C9-047 (change + precedence + silence-as-finding). Component: `services/mkondo/charter.py`. Contract: `Mkondo.Charter.v0`. Record class: N/A (Mkondo is the registrar for others). Task identity: `mkondo.charter.per_change`.
2. **CANON CLAUSES.** Canon 9 §1-§3 (Mkondo Charter); Canon 9 §4-§8 (precedence, silence-as-finding, change).
3. **DEFINITION OF DONE.** Mkondo owns three registers (record matrix, task-identity, handoffs); every register access goes through Mkondo. Structure-only — Mkondo answers questions ABOUT records but NEVER holds the records themselves.
4. **QUALITY EVIDENCE.** Invariant class (structure-only gate) + inventory audit. Calibration under Canon 9 §3.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-BUILD-HANDOFF-REGISTRY`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components (three registers coordinated), new engine/authority (Mkondo is a Canon-9 first-class authority), 3 integration surfaces.
7. **REVERSAL COST.** Very high — Mkondo is the register-of-registers; removing it means the three registers lose their shared discipline.

## WS-BUILD-RECORD-MATRIX

1. **WHAT.** Record matrix — 13 writer→readers rows. Rows C9-006..C9-018. Component: `services/mkondo/record_matrix/` (matrix definition + enforcement). Contract: `Record.Matrix.Entry.v0`. Record class: `Record.Matrix.Entry` (writer = Mkondo). Task identity: `matrix.entry.per_class`.
2. **CANON CLAUSES.** Canon 9 §6-§18 (record matrix — 13 rows).
3. **DEFINITION OF DONE.** All 13 record classes have matrix entries: writer role, reader-list, contract shape. AST discipline check enforces writer-role exclusivity and reader-list scoping. Verification: every service in the spine that writes a matrix-tracked class is the sole writer per matrix; every reader is in the reader-list.
4. **QUALITY EVIDENCE.** Invariant class (AST-scoped writer + reader gates). Uncurated sample: full codebase AST scan. Calibration under Canon 9 §6.
5. **DEPENDENCIES.** `WS-BUILD-MKONDO-CHARTER`, `WS-WIRE-LEDGER-MATRIX` (Part 1 — anchors ledger writer), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** Estate-wide wiring — every writer / reader across the entire spine is subject to matrix discipline; introduces 13 new contracts simultaneously; matrix is the substrate for all Canon-9 governance. Meets XL bar on estate-wide axis alone; also meets multi-new-contract axis.
7. **REVERSAL COST.** Very high — matrix defines the entire records governance; removal reverts to ad-hoc ownership. Records written stay.

## WS-BUILD-READING-DISCIPLINE

1. **WHAT.** Reading discipline — matrix reader-list enforcement across Compliance Console + Watch Console. Rows C9-019..C9-022. Component: `services/mkondo/reading_discipline/`. Contract: enforced via record-matrix reader-list. Record class: N/A. Task identity: `matrix.read.per_call`.
2. **CANON CLAUSES.** Canon 9 §7 (reading discipline); Canon 9 §8 (matrix reader-list scoping).
3. **DEFINITION OF DONE.** Every read of a matrix-tracked class goes through the matrix reader path; unauthorized reads refuse with a Canon 9 §7 refusal. Compliance Console reads only its scoped classes; Watch Console reads only its scoped classes.
4. **QUALITY EVIDENCE.** Invariant class (matrix-reader gate). Uncurated sample: one drill week of console reads. Calibration under Canon 9 §7.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-HARVEST-CONSOLE-COMPLIANCE` (Part 1), `WS-BUILD-CONSOLE-WATCH`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

## WS-BUILD-TASK-IDENTITY-REGISTER

1. **WHAT.** Task-identity register — 13 entries. Rows C9-023..C9-035, C7-D22. Component: `services/mkondo/task_identity/`. Contract: `Task.Identity.Registration.v0`. Record class: `Task.Identity` (writer = Mkondo). Task identity: `task_identity.register.per_task`.
2. **CANON CLAUSES.** Canon 9 §5 (task identity); Canon 8 §4.11 W11 (one task, one identity); Canon 7 §D22 (D-Dual-Hat defect).
3. **DEFINITION OF DONE.** Every runtime task carries exactly one registered task identity. Dual-hat tasks refuse (D-Dual-Hat defect). Verification: AST scan confirms every service call site is task-identity-tagged.
4. **QUALITY EVIDENCE.** Invariant class (task-identity-per-call gate + no-dual-hat gate). Calibration under Canon 8 §4.11 + Canon 9 §5.
5. **DEPENDENCIES.** `WS-BUILD-MKONDO-CHARTER`, `WS-BUILD-INPUT-SEAT-DUAL`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** XL. **One-paragraph defence:** Estate-wide — every task-taking call site across the spine registers here; 13 new contract entries land simultaneously; task identity is the substrate for W11 discipline (one of the fourteen Canon-8 doctrines). Both estate-wide-wiring and multi-new-contract axes meet XL.
7. **REVERSAL COST.** Very high.

## WS-BUILD-CREDENTIAL-SCOPE-STRUCTURAL

1. **WHAT.** Structural credential-scope discipline — no credential spans both authorities. Row C7-D23 (D-Cross-Auth-Credential defect). Component: `services/mkondo/credential_scope/`. Contract: `Credential.Scope.v0`. Record class: `Credential.Scope` (writer = Mkondo). Task identity: `credential.scope.per_grant`.
2. **CANON CLAUSES.** Canon 8 §21 W-negative (no credential scope spans both authorities); Canon 9 §5 (task identity); Canon 7 §D23.
3. **DEFINITION OF DONE.** Every credential grant carries a scope; cross-authority scope refuses (D-Cross-Auth-Credential). Verification: AST scan of grants + credential-inventory audit shows dual-scope count = 0.
4. **QUALITY EVIDENCE.** Invariant class (no-dual-scope gate). Calibration under Canon 8 §21.
5. **DEPENDENCIES.** `WS-BUILD-TASK-IDENTITY-REGISTER`, `WS-BUILD-MKONDO-CHARTER`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** Very high.

## WS-BUILD-HANDOFF-REGISTRY

1. **WHAT.** Six handoff contracts (chokepoint→model, verdict→response, containment→decision, mirage-release→reconciliation, disagreement→resolution, Watch findings→CIF). Rows C9-037..C9-042, C7-D21. Component: `services/mkondo/handoff_registry/`. Contract: `Handoff.Contract.v0` (frozen shape with parameter subclasses per handoff type). Record class: `Handoff.Contract` (Canon 9 §6). Task identity: `handoff.per_type`.
2. **CANON CLAUSES.** Canon 9 §6 (handoff contracts); Canon 7 §D21 (D-Handoff-Missing).
3. **DEFINITION OF DONE.** All six handoffs registered; every call across a Canon-9 seam uses a registered handoff shape; unregistered handoffs refuse. Verification: seam-audit shows six live handoffs.
4. **QUALITY EVIDENCE.** Invariant class (handoff-shape gate at every seam). Calibration under Canon 9 §6.
5. **DEPENDENCIES.** `WS-BUILD-MKONDO-CHARTER`, `WS-WIRE-ADMISSION-HANDOFF` (Part 1 — registers the existing admission handoff), `WS-BUILD-WATCH-RECONCILER`, `WS-BUILD-WATCH-TO-CIF`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 2 components + 6 new contracts (handoff shapes) — meets L on register axis.
7. **REVERSAL COST.** Very high.

---

# I. Conditioned Ideation Faculty (Canon 2, ~30 rows → 6 items)

## WS-CIF-COACH-SEAT

1. **WHAT.** Coach seat + origination port — the ONLY seat that adopts frames. Rows C2-009, C2-031. Component: `services/cif/coach_seat/`. Contract: `Coach.Seat.Adoption.v0`. Record class: `Coach.Seat.Adoption` (writer = coach seat). Task identity: `coach.adopt.per_frame`.
2. **CANON CLAUSES.** Canon 2 §12 (coach seat + origination port constitutional load-bearing).
3. **DEFINITION OF DONE.** Only the coach seat adopts frames (no other origination surface); frame adoptions ledgered; frame origin evidenced.
4. **QUALITY EVIDENCE.** Invariant class (single-origination-port AST gate). Calibration under Canon 2 §12.
5. **DEPENDENCIES.** `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-SOLVA-CIF` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: new authority (coach seat) + 1 new contract.
7. **REVERSAL COST.** Very high — Canon 2 §12 constitutional load-bearing.

## WS-CIF-ARCHIVE

1. **WHAT.** CIF living archive — four-state discipline + silence-is-a-data-state + rejection-names-condition + rent + zero-inherited-credibility + paper-first. Rows C2-019..C2-023. Component: `services/cif/archive/`. Contract: `Archive.Entry.v0` (frozen 4-state). Record class: `Archive.Entry` (writer = archive). Task identity: `cif.archive.per_entry`.
2. **CANON CLAUSES.** Canon 2 §10-§13 (Living Archive discipline).
3. **DEFINITION OF DONE.** Archive entries in exactly one of four states {proposed, provisionally-adopted, adopted, rejected}; silence is data-state (Canon 2); rejection names condition; entries pay rent (Canon 2 §11); zero inherited credibility from parent artefacts; paper-first before compute (Canon 2 §13).
4. **QUALITY EVIDENCE.** Invariant class (4-state + rent gates). Calibration under Canon 2 §10.
5. **DEPENDENCIES.** `WS-CIF-COACH-SEAT`, `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

## WS-CIF-DETECTION

1. **WHAT.** Frame-signature detection (cascade / absorption / misfit). Rows C2-029, C2-030. Component: `services/cif/detection/`. Contract: `Frame.Signature.Detection.v0`. Record class: `Frame.Signature.Detection`. Task identity: `cif.detect.per_signal`.
2. **CANON CLAUSES.** Canon 2 §15-§16 (detection modes).
3. **DEFINITION OF DONE.** Signals arriving at CIF are classified into one of the three detection modes; detection events ledgered.
4. **QUALITY EVIDENCE.** Contract test + drill (three-mode fixture). Calibration under Canon 2 §15.
5. **DEPENDENCIES.** `WS-CIF-COACH-SEAT`, `WS-BUILD-WATCH-TO-CIF` (Watch findings feed detection), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** M.
7. **REVERSAL COST.** High.

## WS-CIF-METABOLISATION

1. **WHAT.** Four-step frame-adoption sweep + build check. Rows C2-032, C2-033. Component: `services/cif/metabolisation/`. Contract: `Metabolisation.Step.v0`. Record class: `Metabolisation.Step`. Task identity: `cif.metabolise.per_frame`.
2. **CANON CLAUSES.** Canon 2 §17 (metabolisation sweep).
3. **DEFINITION OF DONE.** Every frame adoption traverses all four metabolisation steps; build check fires at closure; incomplete metabolisation refuses.
4. **QUALITY EVIDENCE.** Invariant class (four-step gate) + drill. Calibration under Canon 2 §17.
5. **DEPENDENCIES.** `WS-CIF-ARCHIVE`, `WS-CIF-DETECTION`, `WS-WIRE-SOLVA-CIF` (Part 1), `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** Very high.

## WS-CIF-MONITORING

1. **WHAT.** Condition watchers + cascade detection + adversarial elicitation. Rows C2-034..C2-036. Component: `services/cif/monitoring/`. Contract: `Cif.Condition.Watch.v0`. Record class: `Cif.Condition.Watch`. Task identity: `cif.monitor.per_condition`.
2. **CANON CLAUSES.** Canon 2 §18 (monitoring); Canon 8 §5 (Watch to CIF handoff).
3. **DEFINITION OF DONE.** Condition watchers active; cascades detected pre-emptively; adversarial elicitation runs on schedule; findings ledgered.
4. **QUALITY EVIDENCE.** Contract test + drill (adversarial elicitation fixture). Calibration under Canon 2 §18.
5. **DEPENDENCIES.** `WS-CIF-DETECTION`, `WS-BUILD-WATCH-TO-CIF`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L.
7. **REVERSAL COST.** High.

## WS-CIF-PARAMETERS

1. **WHAT.** CIF operative + quality parameters. Rows C2-040..C2-051 (manifest coverage, archive completeness, escalation latency, metabolisation execution, rent collection, promise metric, manifest hit-rate, provisional honesty, metabolisation closure, overhead ceiling, false-escalation rate, defaults). Component: `services/cif/parameters/`. Contract: `Cif.Parameter.Reading.v0`. Record class: `Cif.Parameter.Reading`. Task identity: `cif.parameter.per_cycle`.
2. **CANON CLAUSES.** Canon 2 §19 (Operative Parameters); Canon 2 §20 (Quality Parameters).
3. **DEFINITION OF DONE.** Every parameter measured continuously; latest reading is the one shown; drift monitored. Verification: parameter dashboard shows all 12 parameters within Canon 2 §19 bounds during a drill week.
4. **QUALITY EVIDENCE.** Contract test + inventory audit (12 parameters live). Calibration under Canon 2 §19-§20.
5. **DEPENDENCIES.** `WS-CIF-*` (all preceding CIF items), `WS-BUILD-RECORD-MATRIX`, `WS-WIRE-PARITY-EXTENSION`.
6. **CREDIT COST CLASS.** L. Justification: 3+ components (parameters + measurement + rendering), new register.
7. **REVERSAL COST.** High.

---

# Part-2 item count summary

| Group | Count | Items |
|---|---:|---|
| A. Custody & Boundary | 3 | WS-BUILD-DECL, WS-BUILD-INPUT-SEAT, WS-BUILD-INPUT-SEAT-DUAL |
| B. Extraction Quality | 2 | WS-BUILD-MOAC-SCORECARD, WS-BUILD-ADAPTER-REGISTRY |
| C. Ports (Ruling B new) | 2 | WS-BUILD-STREAMING-PORT, WS-BUILD-OBJECT-STORAGE-PORT |
| D. Integration | 2 | WS-BUILD-WEBHOOK, WS-BUILD-PLANE-PRECOMPUTE |
| E. Governance Ceremony | 5 | WS-BUILD-VERIFICATION-RUNNER, WS-BUILD-PROVE-ONE-RUN, WS-BUILD-SETUP-CONSOLE, WS-BUILD-DAY-ZERO, WS-BUILD-RULEBOOK-SURFACE |
| F. Interface BUILD (no donor) | 13 | Model-Catalogue, Batch-Board, Quality-Obs, Agent-Chip, Refusal-Card-Copy, Three-Lenses, Answer-Card, Five-Pillars, Pulse-News, Studio, Learn-Pillar, Reference-App, Control-Band |
| G. Watch | 16 | Foundation, Actors, Reconciler, Mark-Registry, Containment, Mirage, Signature-Store, Decisions-Panel, Watch-Day, Drill-Harness, Authority-Peerage, Record-Classes, To-CIF, Attestation-Witness, S6-Watch-Service, Console-Watch |
| H. Mkondo | 6 | Charter, Record-Matrix, Reading-Discipline, Task-Identity-Register, Credential-Scope-Structural, Handoff-Registry |
| I. CIF | 6 | Coach-Seat, Archive, Detection, Metabolisation, Monitoring, Parameters |
| **Total** | **55** | |

**Reconciliation with row_to_item_index.md counts.** The initial count of 42 Part-2 items (55 - 13 interface reclassifications) has expanded to 55 because Ruling B mandated bundling by canonical MECHANISM rather than one-mega-item-per-canon. Watch expanded from ~10 items to 16; Ports promoted from folded dependencies to 2 standalone items (Streaming, Object-Storage). Grand total now: 47 Part 1 + 55 Part 2 = **102 work items**.

**New contracts + Parity-seat linkage.** Every item in this file with a `Contract:` line lists `WS-WIRE-PARITY-EXTENSION` as a dependency — enforced during the completeness audit.

**Ruling-1 transition linkage verified in:** `WS-BUILD-DECL` (precondition a) and `WS-BUILD-WATCH-RECONCILER` (precondition b). Both name `WS-CONTRADICTION-PURPOSE-GATE` as the item they lawfully permit to strip once both fire.

**Fidelity ledger entries opened in this file:** FL-P1-03 (Object Storage Port placement — resolved with PROPOSAL, ledger stays OPEN pending owner ratification); FL-OQ-05 (Studio scope reclassification — L → XL if storage-plane composition).
