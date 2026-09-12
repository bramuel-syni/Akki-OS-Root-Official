# W-MTAFITI-GPU-DISCOVERY — Grounding Brief

**Wave name:** `W-MTAFITI-GPU-DISCOVERY`
**Status:** OPENED 2026-09-09 · CP plan awaits owner sign-off · CP1 scaffolding staged (uncommitted)
**Precedent ruling:** 2026-09-09T~evening owner ruling banked in `STATE/DECISIONS.md` — "objective-generation blind, multi-objective facilitation" + "GPUs take precedence now"
**Discipline:** tests-first · thin-kernel · terminal `pytest` under `BASELINE_GUARD=1` · double-green byte-match to close each CP · two-commit pattern (track-a code + workspace STATE) · **NO PUSH** · no `testing_agent` · ratchet floor 3098 → grows per CP

---

## §A · Verbatim requirement quotes (Standing Condition 1, 2026-08-26 — no paraphrasing)

Every requirement in this wave binds to at least one of the quotes below. When a gating test is written, the quote appears verbatim in the test's docstring per Standing Condition 1.

### A.1 · The owner ruling itself (2026-09-09T~evening)

> **"The registry building function goes beyond the reading file names. Its should be 'objective generation' blind but can carry multiple objectives which it facilitates but not create new objectives. I think this is why it works hand in hand with Targeta and CIF to a clean more stable discover. It should do exactly what you have described as a mtafiti powered by GPUs."**

> **"On GPU availability, the previous run concluded and this should take precedence now."**

### A.2 · Canon 4 / RMS_Mtafiti_Specification (the discovery engine)

**RMS_Mtafiti_Specification.md §1 (lines 33-39) — verbatim:**
> "Mtafiti is the discovery engine. It censuses the estate exhaustively and writes the Registry: what exists, at what sensitivity, and how defensible each source is. **It is objective-blind — it measures the estate as it is, without reference to any particular objective — so that Targeta and Layer C read one measure that serves every objective.** It discovers and measures; it does not extract, target, or govern. It runs at estate standup and is maintained thereafter by a freshness mechanism."

**RMS_Mtafiti_Specification.md §4 · Detect versus Decide (lines 71-79) — verbatim:**
> "The inference overlay is learned, and the single rule that keeps learning from laundering authority into the measure is this: **the learned component produces detections, never verdicts.** It detects signals — a source-attachment marker is present, the genre-form is monologic, a claim recurs across the estate. The defensibility verdict — what a unit is permitted to assert — is assigned by the Qualification Matrix, a governed, versioned, inspectable taxonomy, by deterministic lookup. Learning detects; the governed Matrix decides; the declaration baseline floors; the V3 gate admits."

**Canon 4 §5 · C4-003 (Mtafiti Charter):**
> "Mtafiti measures WHAT THE ESTATE ACTUALLY CONTAINS, at whatever scale (whole org, department, archive, single file — Doc 1 §1.1)."

**Canon 4 §5 · C4-004 (Objective-blind):**
> "Mtafiti measures without reference to any objective. It measures the ESTATE, never the ANSWER. Reads for Watch tripwire coverage, never writes for them (Doc 9 §3)."

**Canon 4 §7 · C4-007 (Two-layer):**
> "Defensibility is produced in two layers: a DECLARATION layer (deterministic, per source, always available — the FLOOR) and an INFERENCE layer (signals detected in content — corroboration and contested status)."

**Canon 4 §7 · C4-008 (V3 gate):**
> "Inference contributes ONLY after its own accuracy has been proven on the tenant's own material. Until then, declaration STANDS ALONE."

**Canon 4 §7 · C4-009 (Verdict is not a model output):**
> "Neither layer decides what a measurement means. Meaning is a governed, versioned lookup — never a model's output."

**Canon 4 §10 · C4-013 (Repeatable):**
> "Every Mtafiti measurement is repeatable — same inputs, same time-boundary, same declaration set → same measured output."

### A.3 · Canon 4 / RMS_Targeta_Specification (the objective-carrier upstream)

**Canon 4 §11 · C4-014 (Targeta Charter):**
> "Targeta plans extraction — WHICH material, WHICH order, WHICH standards, WITHIN WHICH rights — against a frozen objective. Writes mining plans (Doc 9 §3). Readers = governing authority + auditors. Watch neither reads to steer nor writes."

**Canon 4 §11 · C4-015 (Objective-bound):**
> "Targeta operates ONLY on frozen objectives (Doc 3 §5). Never plans against an amending or drafting objective."

**Canon 4 §13 · C4-018 (Coverage figure):**
> "The coverage figure is a MEASURED anticipation drawn from Mtafiti composition, not a projection. It is stated as a RANGE, never a point estimate."

### A.4 · Canon 2 / CIF (the origination-port rule this refinement extends)

**Canon 2 §6 · C2-015 (Engine walls):**
> "A planner's learning never widens what an objective may reach; a critic detects and never decides. CIF operates inside these walls everywhere."

**Canon 2 §11 · C2-030 (Detection only):**
> "The faculty DETECTS. It NEVER adopts a frame on the strength of its own signature."

**Canon 2 §12 · C2-031 (Origination port — the constitutive rule):**
> "A new frame enters ONLY through the origination port: the coach, ground reality observed in deployment, or a genuinely outside reviewer. This seat is constitutionally load-bearing and permanent in every configuration."

### A.5 · Reading the refinement against the canon

The owner's "objective-generation blind" language and the canon quotes form a single consistent stack:

1. **CIF's C2-031** closes origination for new frames — origination is a constitutionally load-bearing SEAT that only the coach / ground reality / outside reviewer holds.
2. **CIF's C2-030** binds the faculty to DETECT-not-adopt on the strength of its own signature — self-certification is closed by construction (C2-037).
3. **Mtafiti-Spec §1** says mtafiti's registry serves "every objective" — so it CARRIES objectives; and mtafiti is "without reference to any particular objective" at measurement time — so it never BENDS its measurement to one.
4. **Mtafiti-Spec §4** binds the learned layer to DETECT-not-decide — model output cannot become a verdict.
5. **Targeta C4-014/C4-015** shows objectives arrive at Targeta already FROZEN — set upstream by CIF/coach. Targeta then reads mtafiti's registry to plan against them.

**The refinement therefore says:** the origination-port rule (C2-031) extends by construction from CIF to mtafiti. Mtafiti neither invents an objective (extension of C2-031) nor decides a verdict on its detections (§4). It accepts objectives supplied by Targeta/CIF and facilitates discovery under them, producing one measure that serves every objective (§1). Zero canon conflict; the refinement is a **codified extension**, not an amendment.

---

## §B · Scope guardrails (owner-issued, binding)

1. **DETECTION-ONLY enrichment set.** GPU workloads may only emit `DetectionSignal` typed objects. No verdicts (defensibility, sensitivity_class, same-entity, source-standing) may be written by the learned layer. Verdicts stay with the Qualification Matrix and governed lookups per Mtafiti-Spec §4.

2. **Adaptive sampling admitted ONLY in determinised form.** Pinned policy version + fixed seed → identical inputs must yield an identical walk. Preserves C4-013 repeatability. Online / path-dependent adaptive stays OUT pending a separate owner ruling.

3. **Objective handling.** Mtafiti accepts objectives from Targeta/CIF via a typed carrier (origin enum `TARGETA | CIF | COACH_ORIGINATION_PORT`). Any attempt by mtafiti internals to spawn a new objective must be refused with `ObjectiveOriginationForbidden`. Extension of C2-031 to the discovery engine.

4. **Interrupt discipline.** GPU-mtafiti is the primary GPU tenant NOW, but registers with `on_host_queue_dispatcher.py` as a **fill-only tenant** that yields immediately when a training campaign resumes. No new orchestration; reuses the existing dispatcher shape from W-WINDOW-FILL-RESTORE-2.

5. **Data fixtures.** Development and proof happen against the 2 currently-LIVE hosts (`Weego_and_marketing-analytics` at `159.138.162.146` and 3rd-party USSD host at `110.238.76.159`, ~1,213 tables across 20 schemas between them). **This is not "the census"** — per owner's "all-live-first, then census" directive, the full-estate run waits on the still-open credential/IAM ledger (§F below).

6. **Read-only SQL discipline unchanged.** Detectors execute `SELECT / SHOW / USE` only. No `INSERT / UPDATE / DELETE / CREATE / DROP / ALTER / GRANT` against any owner or third-party DB.

7. **HOLD scope.** This wave is the ONLY wave lifted from HOLD by the 2026-09-09T~evening ruling. Product-build HOLD on `W-REGISTRY-FULL-BUILD` CP10, `W-SOLVA-V2-LIFT`, `W-DAP-STACK`, `W-DOC0-GAP-CLOSURE`, `W-RULES-SERVICE-STACK` remains until owner rules otherwise.

---

## §C · Checkpoint breakdown (CP1..CP11)

Each CP is **reversible on its own**, tests-first, closes with `BASELINE_GUARD=1 python -m pytest tests/invariants/` double-green byte-match, bumps the ratchet, lands with a **two-commit pattern**: (1) code + tests on `programme/track-a` in `Extraction-Akki` repo; (2) STATE mirror on workspace `master`. **No push at any CP close.**

### CP1 — Wave scaffolding + brief invariant (RATCHET +1)

**Deliverables (workspace `master`):**
- This grounding brief (present file).
- STATE update: `DECISIONS.md` verbatim-owner-ruling entry (already banked 2026-09-09T~evening) + `HOLISTIC_PLAN.md §5` reconciliation (already banked) + `NEXT.md` precedence pointer.

**Deliverables (`programme/track-a` in Extraction-Akki):**
- `backend/tests/invariants/test_w_mtafiti_gpu_discovery_grounding_brief.py` — RED first, then GREEN:
  - Asserts brief exists at `notes/W_MTAFITI_GPU_DISCOVERY_grounding_brief.md`.
  - Asserts brief contains **exact** verbatim owner quote from 2026-09-09T~evening.
  - Asserts brief contains verbatim `RMS_Mtafiti_Specification.md §1 line 35-37` and `§4 line 71-79` substrings.
  - Asserts brief contains `C4-003`, `C4-004`, `C4-007`, `C4-008`, `C4-009`, `C4-013`, `C4-014`, `C4-015`, `C4-018`, `C2-015`, `C2-030`, `C2-031` row IDs.

**Ratchet expected:** 3098 → **3099**.

**Reversibility:** delete the invariant file + revert STATE appends. Zero infra impact.

### CP2 — Objective-carrier contract + origination-refusal invariant (RATCHET +2)

**Deliverables (`programme/track-a`):**
- `backend/contracts/mtafiti_objective_carrier.py` — Pydantic frozen model:
  ```
  class ObjectiveOrigin(str, Enum):
      TARGETA = "targeta"
      CIF = "cif"
      COACH_ORIGINATION_PORT = "coach_origination_port"
  class MtafitiObjectiveCarrier(BaseDocument):
      objective_id: str
      origin: ObjectiveOrigin        # frozen; must be one of the three
      frozen_at: datetime            # C4-015 "operates ONLY on frozen objectives"
      served_by: List[str]           # multi-objective carry
      # NO field named `originated_by_mtafiti` — that concept is refused
  ```
- `backend/services/mtafiti/objective_gate.py` — sole entrypoint that admits carriers into mtafiti; raises `ObjectiveOriginationForbidden` if any code path tries to construct a carrier with `origin` unset or with a mtafiti-internal origin.
- `backend/tests/invariants/test_mtafiti_refuses_to_originate_objective.py` — proves:
  - Constructing a carrier with no origin raises.
  - Constructing a carrier claiming mtafiti-internal origin raises.
  - Constructing carriers with the 3 legal origins succeeds and returns immutable objects.

**Ratchet expected:** 3099 → **3101**.

**Reversibility:** revert both files + the invariant. No downstream dependents in CP1.

### CP3 — `DetectionSignal` frozen contract + verdict-refusal invariant (RATCHET +2)

**Deliverables (`programme/track-a`):**
- `backend/contracts/mtafiti_detection_signal.py`:
  ```
  class EvidenceClass(str, Enum):
      FACT = "fact"
      INFERRED = "inferred"
      DETECTED = "detected"
      REPORTED = "reported"
      DECLARED = "declared"
  class DetectionSignal(BaseDocument):
      signal_name: str
      evidence_class: EvidenceClass
      confidence: float                    # 0..1 float; NOT a verdict
      source_ref: str
      detector_version: str                # pinned per Mtafiti-Spec §4 V3 gate
      seed: Optional[int]                  # if deterministic
      # FORBIDDEN: any field ending in _verdict, _decision, _class_authority
  ```
- `backend/tests/invariants/test_detection_signal_never_carries_verdict.py`:
  - Any DetectionSignal with a field name matching `*_verdict|*_decision|*_class_authority` fails Pydantic validation.
  - Proves DetectionSignal is frozen (immutable).
- `backend/tests/invariants/test_detection_signal_evidence_class_governs.py`:
  - `evidence_class` is one of the 5 canon evidence classes (Doc 5 §5 evidence-class taxonomy — quoted verbatim in test docstring).

**Ratchet expected:** 3101 → **3103**.

### CP4 — GPU dispatcher tenancy: fill-only tier registration (RATCHET +2)

**Deliverables (`programme/track-a`):**
- `backend/services/mtafiti/gpu_fill_tenant.py` — thin adapter that registers a mtafiti-gpu job with the existing `on_host_queue_dispatcher.py`. Adapter marks the job with tier `TENANT_TIER_FILL_ONLY` such that a training-tier job arriving preempts it immediately.
- `backend/tests/invariants/test_mtafiti_gpu_registers_as_fill_only_tenant.py`:
  - Proves mtafiti-gpu jobs cannot register at `TENANT_TIER_TRAINING` (raises).
  - Proves that when a training-tier job arrives in the dispatcher queue, an active mtafiti-gpu job's preempt signal fires within N seconds (mock timing, spec quote in docstring).
- `backend/tests/invariants/test_mtafiti_gpu_never_extends_dispatcher_orchestration.py`:
  - Asserts NO new orchestration modules were added (reuses only `queue_followon_launcher.py` + `on_host_queue_dispatcher.py`).

**Ratchet expected:** 3103 → **3105**.

### CP5 — PII / sensitive-data detector (RATCHET +2)

**Deliverables (`programme/track-a`):**
- `backend/services/mtafiti/detectors/pii_detector.py` — CPU-first (regex + small NER model, deterministic), GPU-optional (accelerated inference when the fill-only tenant is scheduled).
- Emits `DetectionSignal[]` — NEVER a `sensitivity_class` verdict.
- `backend/tests/invariants/test_pii_detector_emits_signals_not_verdicts.py` — proves detector output type ⊆ `DetectionSignal`; no field ever set to a `sensitivity_class` value.
- `backend/tests/invariants/test_pii_detector_deterministic_same_seed_same_output.py` — same seed + same input rows → byte-identical output (C4-013).

**Ratchet expected:** 3105 → **3107**.

### CP6 — Semantic column classifier (RATCHET +2)

**Deliverables (`programme/track-a`):**
- `backend/services/mtafiti/detectors/column_classifier.py` — classifies columns as one of {name, date, currency, geo, identifier, free-text, structured, blob, unknown}. Deterministic given seed.
- `backend/tests/invariants/test_column_classifier_emits_detections.py`.
- `backend/tests/invariants/test_column_classifier_deterministic.py`.

**Ratchet expected:** 3107 → **3109**.

### CP7 — Language detector + content-type profiler (RATCHET +2)

**Deliverables (`programme/track-a`):**
- `backend/services/mtafiti/detectors/language_detector.py` + `backend/services/mtafiti/detectors/content_type_profiler.py`.
- Emit language and format-conformance / null-density / cardinality signals — no verdicts.
- `backend/tests/invariants/test_language_detector_emits_signals.py`.
- `backend/tests/invariants/test_content_profiler_emits_signals.py`.

**Ratchet expected:** 3109 → **3111**.

### CP8 — Embedding detector (dedup / entity-resolution SIGNALS only) (RATCHET +3)

**Deliverables (`programme/track-a`):**
- `backend/services/mtafiti/detectors/embedding_detector.py` — sentence-transformer emits `(row_a, row_b, cosine)` triples as `DetectionSignal[]`. **Never** auto-labels pairs as "same entity" — that would DECIDE.
- `backend/tests/invariants/test_embedding_detector_emits_pairs_only.py`.
- `backend/tests/invariants/test_embedding_detector_no_threshold_autoclassify.py` — searches the module for any hard-coded threshold that assigns a same-entity verdict; asserts zero.
- `backend/tests/invariants/test_embedding_detector_deterministic.py`.

**Ratchet expected:** 3111 → **3114**.

### CP9 — Determinised adaptive walker (RATCHET +3)

**Deliverables (`programme/track-a`):**
- `backend/services/mtafiti/sampling/deterministic_adaptive_walker.py` — pinned RL/bandit policy + fixed seed → identical walk on identical inputs. No online learning during the walk.
- `backend/tests/invariants/test_adaptive_walker_same_seed_same_walk.py`.
- `backend/tests/invariants/test_adaptive_walker_different_data_different_walk.py` (guards against a degenerate "walker ignores its input" implementation).
- `backend/tests/invariants/test_adaptive_walker_refuses_online_learning.py` — asserts the walker cannot mutate its policy weights during a walk (C4-013 preservation + owner-ruled guard).

**Ratchet expected:** 3114 → **3117**.

### CP10 — Cross-table relationship + cross-estate corroboration detectors (RATCHET +2)

**Deliverables (`programme/track-a`):**
- `backend/services/mtafiti/detectors/relationship_candidate.py` — proposes implicit-FK candidates as SIGNALS; never commits them as canonical Registry rows.
- `backend/services/mtafiti/detectors/corroboration_detector.py` — surfaces "this entity recurs across N tables" as a SIGNAL; matches Canon 4 §7 spec-blessed language ("a claim recurs across the estate").
- `backend/tests/invariants/test_relationship_candidate_emits_signals_only.py`.
- `backend/tests/invariants/test_corroboration_detector_emits_signals_only.py`.

**Ratchet expected:** 3117 → **3119**.

### CP11 — Wave close · end-to-end integration on the 2 live hosts (RATCHET +3)

**Deliverables (`programme/track-a`):**
- Integration invariants that run the full detection pipeline (CP5-CP10) against the 2 currently-LIVE fixtures (Weego_and_marketing-analytics + 3rd-party USSD host), read-only SQL:
  - `test_mtafiti_gpu_e2e_writes_only_detection_signals.py` — no verdict rows written to Registry.
  - `test_mtafiti_gpu_e2e_walk_is_repeatable.py` — same seed → same walk across the two fixtures.
  - `test_mtafiti_gpu_e2e_yields_to_training_dispatcher.py` — training-tier arrival preempts the run mid-flight.
- **WPW draft** for wave close (short whitepaper, 5-section end-of-wave format per STANDING_ORDERS §2 refinement 2026-09-09T~13:15Z): progress made · how much to go · decisions taken · discoveries not envisioned · recommendations.
- **Ship-Manifest DoD**: `app/backend/server.py` and `pod_shell/backend/server.py` byte-identical (if this wave touches the router surface — likely NO for pure services; confirm at CP close).

**Ratchet expected:** 3119 → **3122** (subject to fixture behaviour; adjust at CP11 open).

**Wave close condition:** all 11 CPs double-green byte-match, ratchet at 3122 (target), grounding brief marked CLOSED with a wave-close entry in `DECISIONS.md`.

---

## §D · Test data — real fixtures, not synthetic

The wave develops against the 2 currently-LIVE hosts (per §B.5):

- **Weego_and_marketing-analytics** (159.138.162.146): `weego` (413 tables), `analytics` (28), `sql_demo` (1), `sql_trial1` (1) — DB user `bramuel@%` proven working.
- **3rd-party USSD host** (110.238.76.159): 16 non-system schemas / ~770 tables — DB user `bramuel@%` proven working.

Total dev fixture surface: ~1,213 tables across 20 schemas. Sufficient to prove all detectors and the adaptive walker at realistic scale without touching credentials we don't have.

**Fixture discipline:**
- No detection ever writes to the fixture DBs. Read-only SQL only.
- Detector output writes to the LOCAL registry contract (`backend/services/mtafiti/registry.py`), not into the source estate.
- Every fixture run is seeded; seed values banked in the test docstrings.

**Explicit non-scope:** the 10 currently-not-live hosts wait on §F below. This wave does NOT unblock any credentials or IAM grants — those are still on the owner-ledger.

---

## §E · Honest limits (STANDING_ORDERS §3)

1. **The GPU wave is authorised; product-build waves remain on HOLD.** CP10 of `W-REGISTRY-FULL-BUILD`, `W-SOLVA-V2-LIFT`, `W-DAP-STACK`, and `W-RULES-SERVICE-STACK` do not resume from this ruling.

2. **This wave builds the ENGINE, not the census.** Per owner's "all-live first, then census" directive, the full-estate census run is a subsequent wave and depends on §F unblocking.

3. **We cannot prove the detectors at census scale until §F unblocks.** The 2 live hosts are 2 tenants; the other 10 (containing large tables like `weego-replica`, `election-prod-db2`, `visitors-database-cluster`, `citizen-digital-dev-db-cluster`, `dbms-trf-req-database-3`, `rms-ai-pg`) are unreachable. If detector performance changes materially at estate scale, the wave will need a follow-on tuning CP.

4. **Ubuntu-release-upgrader is currently the top CPU process on both GPU hosts.** Cosmetic, but worth naming — the hosts have a pending apt task chewing 50-60% of one CPU. Does not affect GPU work; flagged so the owner knows the "idle" characterisation is CPU-live-but-GPU-idle.

5. **The STATE-file narrative and probed reality diverged.** Reconciled in `HOLISTIC_PLAN.md §5` this same session — the "77 campaigns running" language is retired. If any other STATE claims turn out to be similarly stale during this wave, they get reconciled the same way rather than papered over.

---

## §F · Still-open owner-ledger (unchanged by this wave)

These items gate full-estate reach and are NOT solved by W-MTAFITI-GPU-DISCOVERY:

1. **IAM grant on `BramwelMwalo`** for ECS/EVS/EIP/VPC-write in `af-south-1` (unlocks bastion provisioning — Part 8 Task 1 detail).
2. **DB password for `RDS-INTERACTIONS`** (network already open; only auth is missing).
3. **DB usernames + passwords for 5 unknown owner-tenant instances**: `election-prod-db2`, `visitors-database-cluster`, `dbms-trf-req-database-3`, `citizen-digital-dev-db-cluster`, and `rds-shikisha` (users `corporate`/`saa` known via API enum; passwords not).
4. **WEEGO primary DB password** (also unlocks `weego-replica-d536` via replica-inherited-users).
5. **PostgreSQL user + password for `rms-ai-pg`** + decision on second bastion in `ap-southeast-1` vs VPC peering vs defer.
6. **Third-party tenant coordination** for whitelisting our bastion EIP on SGs behind `203.123.86.10` and `159.138.164.93`.

**Effect on this wave:** none. This wave builds and proves the engine on the 2 live hosts. When §F unblocks (any subset), the engine runs against the additional hosts without engine changes; only the fixture list expands.

---

## §G · Commit protocol (STANDING_ORDERS §3)

- **Two-commit pattern per CP close**, both local, never pushed:
  - Commit 1: `programme/track-a` in `Extraction-Akki` repo — code + tests + any doc changes co-located with the code.
  - Commit 2: workspace `master` in `assessment_workspace` — STATE mirror + this brief updates + wave-close notes.
- **Commit messages** name the CP + spec_ids exercised + ratchet delta + ledgered receipts (path to `_scratch/` or `phase0/`).
- **NO PUSH** to any remote. Every close is local.

---

## §H · Wave close criteria

- All 11 CPs closed double-green byte-match, ratchet target 3122 (may adjust at CP11 open).
- WPW Tier-1 draft filed at wave close (5-section end-of-wave format).
- `DECISIONS.md` carries a WAVE-CLOSED entry with the final ratchet and the list of 21 new invariants.
- The full engine has been proven against the 2 live fixtures (Weego_and_marketing-analytics + 3rd-party USSD host).
- No verdict rows in the Registry from any GPU detector. No mtafiti-originated objectives in the carrier gate.
- Ship-Manifest DoD unaffected (confirm at CP11).

---

## §I · CP1 CLOSED · 2026-09-12T06:17Z

**Ratchet:** 3098 → **3164** (+66; 64 direct CP1 tests + 2 frozen-contract-parity self-heal via new snapshot files).

**Delta bundled per owner refinement this session:** four foundational governance invariants landed together — the user compressed CP1..CP3 + CP9-governance-surface into a single CP1 landing so the discovery engine has all bright-lines in place before any executor / detector scaffolding is touched.

**Invariant files (`programme/track-a`):**
- `backend/tests/invariants/test_mtafiti_gpu_discovery_objective_generation_blind.py` — 5 tests (C2-031 extension: origin ∈ {TARGETA, CIF, COACH_ORIGINATION_PORT}; carrier frozen; mtafiti-internal origin refused; module surface has no origination-suggesting symbol; schema forbids origination-authorship fields).
- `backend/tests/invariants/test_mtafiti_gpu_discovery_detect_not_decide.py` — 5 tests (DetectionSignal frozen with `extra="forbid"`; no verdict-shaped field names; 5-value evidence taxonomy pinned; confidence bounded [0,1]).
- `backend/tests/invariants/test_mtafiti_gpu_discovery_deterministic_adaptive_sampling.py` — 5 tests (constants pinned verbatim; same-input → byte-identical manifest_sha256; different-input → different manifest; manifest carries seed + policy_id; walker forbids online / stateful mutation).
- `backend/tests/invariants/test_mtafiti_gpu_discovery_readonly_sql_guard.py` — 49 tests (SELECT/SHOW/USE/DESCRIBE/DESC/EXPLAIN admitted; INSERT/UPDATE/DELETE/CREATE/DROP/ALTER/GRANT/REVOKE/TRUNCATE/REPLACE/RENAME/MERGE/CALL/EXECUTE/LOCK/UNLOCK/SET/COMMIT/ROLLBACK/BEGIN/START refused; multi-statement refused; empty/comment-only refused; comment-hidden writes still refused; refusal-by-construction).

**Kernel (`programme/track-a`):**
- `backend/contracts/mtafiti_objective_carrier.py` — ObjectiveOrigin enum · MtafitiObjectiveCarrier (frozen, extra="forbid") · ObjectiveOriginationForbidden · admit_carrier().
- `backend/contracts/mtafiti_detection_signal.py` — EvidenceClass enum · DetectionSignal (frozen, extra="forbid", closed schema).
- `backend/services/mtafiti/gpu_discovery_constants.py` — `MTAFITI_GPU_SAMPLING_SEED = 20260909` · `POLICY_ID = "mtafiti-gpu-discovery-v1"`.
- `backend/services/mtafiti/sampling/deterministic_adaptive_walker.py` — `deterministic_walk(inputs, sample_size)` emits pinned-policy manifest with canonical sha256.
- `backend/services/mtafiti/executor/readonly_sql_guard.py` — `refuse_if_write(sql)` + `WriteVerbRefused`.

**Frozen-contract-parity self-heal:**
- `backend/tests/invariants/mtafiti_objective_carrier.contract_snapshot.json` (new)
- `backend/tests/invariants/mtafiti_detection_signal.contract_snapshot.json` (new)
- `backend/tests/invariants/test_frozen_contract_snapshot_parity.py` — added 2 CONTRACT_TO_SNAPSHOT entries.

**Discipline receipts:**
- Harness refreshed pre-CP1 (real-Chromium, orphan_count=0): `phase0/harness_ground_truth/latest.json` at 2026-09-12T06:01:36Z; screenshot triples at `phase0/eyeball_proxies/20260912T060100Z_wave_g5_realchrome_pre_cp1_mtafiti_gpu_discovery_harness_refresh_{portal,registry,compute}.png`.
- Mechanical RED: `phase0/drill_receipts/20260912T060604Z_wave_mtafiti_gpu_discovery_cp1_RED_pre_impl.log` (64 failed / 3098 passed; right-reason ImportError against modules-not-yet-created).
- Double-green byte-match: `phase0/drill_receipts/20260912T061522Z_wave_mtafiti_gpu_discovery_cp1_close_run1.log` and `20260912T061711Z_..._run2.log` — both `3164 passed, 1 skipped, 438 warnings in 101.[23]s`, BASELINE_GUARD receipt `passed=3164 / baseline-failures-remaining=0 / quarantined=0 · status: OK`.

**Ratchet manifest:** `backend/tests/invariants/baseline_failures.json` bumped in tandem (counts.passed=3164 · passed_floor=3164 · ratchet_history entry appended).

**One decision-point surfaced and resolved autonomously (STANDING_ORDERS §2 DPO):** pre-CP1 baseline showed 3097/1 due to a 65.2h-old harness ground-truth receipt (threshold 48h). Owner precedent (DECISIONS 2026-09-08T~06:15Z STEP 5, verbatim: "refresh the harness, don't relax the threshold") was applied — the real-Chromium harness was re-run, ground-truth receipt refreshed against unchanged App.js. Then and only then did CP1 tests-first work begin. Full narrative in the wave-close DECISIONS entry.

**Wave-honest-limit (adds to §E):** none of CP2..CP11 has started. This CP1 hardens the GOVERNANCE walls of the engine; the DETECTORS (CP5-CP10) and the LIVE READ-ONLY SELECTs against Weego / USSD (CP3 / CP11) remain deferred. The read-only SQL guard is now green-and-committed; per owner ruling this session, "BOTH the read-only guard AND the PII redaction guard must be GREEN before CP3's first live SELECT" — PII redaction guard is CP2 opener.

**Next active step:** CP2 opener (PII redaction guard). CP2 owner-scope confirmation to be requested at CP2 open per owner comms doctrine (micro-sprint updates stay inside the sprint plan).

---
