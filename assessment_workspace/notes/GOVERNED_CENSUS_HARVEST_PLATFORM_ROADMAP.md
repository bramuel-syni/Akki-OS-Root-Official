# Governed Census + Harvest Platform — Roadmap (read-only)

**Task class:** DESIGN REFRAME · read-only · no pipeline build, no code commits, no push, ratchet 3251 untouched. **POC/build HOLD until owner ratifies this reframe.**
**Directive received:** 2026-09-12T~15:00Z (owner) — *"build as a GENERIC, SCALABLE SYSTEM (a platform), NOT structured to this specific case ... there is 'what the system should be' and separately 'mounting THIS job onto the system.'"*
**Executor:** track-a agent, re-grounded from `STATE/STANDING_ORDERS.md`, `STATE/DECISIONS.md`, `STATE/NEXT.md`, and prior notes in the audio programme thread.
**Retracted ChatGPT integration:** ignored (no OpenAI/ChatGPT reference anywhere).
**Integrity mandate:** verify against spec + repo; correct owner where technical specifics are wrong.

**Ground state:** ratchet floor **3251**; workspace `master` HEAD `df24d0a8`; `programme/track-a` HEAD `77834d1`; this file supersedes `notes/AUDIO_PROGRAMME_ROADMAP.md` which is deleted in the same commit.

---

## Design reframe — anchored to spec, not new opinion

The owner's reframe is not a departure from spec; it is a **direct read of spec §1.2 anti-proliferation + §1.1 recursion + Canon 4 §5 estate-scale invariance**. Verbatim from the sources:

**Audio Plane §1.2 (`canon/text/Audio_Intelligence_Plane.md` line ~50 area)**:
> *"The audio plane introduces no sibling services. Mtafiti gains an audio modality; Northena gains audio data classes; the wizard gains an objective variant; Targeta gains a training object. Anything in this document that reads as a parallel to an existing service is rule proliferation and must be collapsed into the existing service before build."*

**Audio Plane §1.1 recursion**:
> *"The archive is an estate; a programme is an estate; a single file is an estate. Segments are rows; the extractable layers ... are columns; no schema exists until one is declared. Census, admission, registry, and record apply at every scale."*

**Canon 4 `C4-003 §5 Charter` (Mtafiti)**:
> *"Mtafiti measures WHAT THE ESTATE ACTUALLY CONTAINS, at whatever scale (whole org, department, archive, single file — Doc 1 §1.1)."*

**Consequence:** the platform builds **estate-agnostic + modality-agnostic** primitives. A job (audio census on 16 Kenyan stations OR text training on Aurora DBs OR an image-taxonomy census on an S3 bucket) is a **mounting artifact** — a `JobManifest` that binds the platform's registered planes to a concrete instance. **Nothing case-specific may live in the platform code path.** This is the spec's own anti-proliferation discipline pushed one level up.

---

# PART A · THE GENERIC PLATFORM (case-agnostic)

## A.0 · The ten planes

The platform is a composition of ten pluggable planes. Every plane has (i) a **contract** (frozen wire), (ii) a **registry** or interface, and (iii) an **implementation set** — multiple, swappable, each satisfying the contract. A `JobManifest` (§A.11) binds selections from each plane.

| # | Plane | Purpose | Current state on `programme/track-a` |
|---:|---|---|---|
| A.1 | **Resource Plane** | Register + schedule + supervise compute resources | PARTIAL (host-specific tools/campaign_infra) |
| A.2 | **Source Plane** | Connector interface + read-only guard per source type | PARTIAL (readonly_sql_guard only) |
| A.3 | **Capability Registry** | Register pluggable processing capabilities | PARTIAL (`layer_b.factory` for ASR/diarization/vision) |
| A.4 | **Objective Plane (L1)** | Frozen objective carrier + wizard-compile port | PARTIAL (carrier landed, wizard absent) |
| A.5 | **Outcome + Quality Plane (L2)** | TargetOutcome + Quality Matrix schemas | ABSENT (schemas un-authored as frozen contracts) |
| A.6 | **Success + QC Plane (L3)** | Composable gate framework | PARTIAL (5 individual gates, no framework) |
| A.7 | **Commission + Worker Plane (L4)** | Worker orchestration + JD/KPI/milestone/handoff | PARTIAL (LORA-trainer-specific) |
| A.8 | **Supervision Plane (L5)** | Domain-agnostic work-supervisor | ABSENT (progress-signal watchdog un-built) |
| A.9 | **HITL Plane (L6)** | Milestone-stream + ratification API | ABSENT |
| A.10 | **Governance Plane** | Rulebook · release gate · AU-3 · determinism boundary · IP/consent/DP chokepoints | PARTIAL (§C7 rulebook landed, release-gate module absent) |

**Cross-plane invariants** (banked in the STANDING ORDERS the platform inherits + one new order per W0 · one per W1):

- Determinism boundary — §8.3 · §11.1 · `extraction_params@v0 temperature=0`.
- Detect-autonomously / decide-only-with-owner-ruling — Ruling #5 pattern.
- Absence-is-a-finding — Canon 4 §41 `C4-057`.
- One-record law — Canon 9 `C9-005`.
- Alive != done — **new W0 STANDING ORDER, this reframe.**
- No run without progress signal — **new W1 STANDING ORDER, this reframe.**

---

## A.1 · Resource Plane

### Contract

```python
class ComputeResource(BaseModel):
    """A registered compute resource, indexed by capability class."""
    model_config = ConfigDict(extra="forbid", frozen=True)
    resource_id: str                                  # e.g. "host:akki-vm:gpu:0"
    resource_class: Literal["gpu", "cpu", "tpu", "cluster"]
    capability_tags: List[str]                        # e.g. ["nvidia:h200","vram:80gb","cuda:12.4"]
    max_concurrent_workers: int
    ssh_seam_ref: Optional[str] = None                # governed access channel
    cost_class: Literal["billed_hourly", "leased_flat", "spot"]
    registered_at: str                                # ISO-8601 UTC
```

### Interface

```
list_resources() -> List[ComputeResource]
select_by_capability(required_tags: Set[str]) -> List[ComputeResource]
schedule_worker(worker: Worker, resource_id: str) -> ScheduleReceipt
supervise_resource(resource_id: str) -> ProgressSignal
```

### Current state

- **Extant primitives (reusable):** `services/orchestrator_resilience/{heartbeat, orphan_detector, adopt, watchdog, resume}.py` — resource-supervision primitives, runtime-drilled 2026-09-06. `tools/{on_host_queue_dispatcher.py, on_host_watchdog.sh, queue_followon_launcher.py}` — dispatcher-per-lane pattern.
- **Extant frozen contracts (reusable):** `PerceptionJob_v0` (with `modality ∈ {AUDIO, VIDEO}` — CPU-only is TEXT per V1-I1); `PerceptionResult_v0` (with `Telemetry.gpu_hours + broadcast_hours + unit_yield + per_modality`).
- **Missing platform layer:** the registry itself. There is no `services/resource_registry/*` today; hosts are bound by `AKKI_VM_HOST` / `AKKI_VM_II_HOST` env vars, not by capability query. **W1 platform wave introduces the registry.**

### What the plane does NOT include

- Not "Cassava H200". Not "akki-vm". Not "80 GB VRAM". These are **values in a specific `ComputeResource` instance**, not code paths.

---

## A.2 · Source Plane

### Contract — connector interface (any estate type)

```python
class SourceConnector(Protocol):
    """One connector per source type. All implementations enforce read-only guard."""
    connector_id: str                                  # e.g. "connector:rds", "connector:synology-filestation"
    source_class: Literal["rdbms", "object_store", "nas", "http_stream", "message_queue"]

    def list(self, path: str, **kwargs) -> List[SourceEntry]: ...
    def read(self, entry: SourceEntry, **kwargs) -> bytes | Iterator[bytes]: ...
    def stream(self, entry: SourceEntry, chunk_size: int) -> Iterator[bytes]: ...
    def read_only_guard(self, operation: str) -> None: ...   # refuses non-{list, read, stream}
    def admit(self, admit_row: AdmitRow) -> AdmitReceipt: ... # Northena admit crossing
```

### Implementations (registered, swappable)

| Implementation | Backing seam | State |
|---|---|---|
| **RDBMS · Aurora Data API** | `services/connect/rds_data_submit` (exempted boto3 seam) | **REAL** — proven in 77 shield_train seals |
| **RDBMS · direct MySQL/PG** | `services/mtafiti/live_readonly_probe.py` (Huawei RDS drills) | **REAL** — proven in W-MTAFITI-GPU-DISCOVERY |
| **Object store · S3 / OBS / GCS** | boto3/OBS SDK behind connector interface | **ABSENT** — pattern established, not implemented |
| **NAS · Synology FileStation** | HTTP-based FileStation API `/webapi/entry.cgi?api=SYNO.FileStation.List` | **ABSENT** — needed for THIS job (see Part B) |
| **NAS · SMB / NFS** | pysmb / nfsclient behind connector interface | **ABSENT** |
| **HTTP stream** | requests / httpx with size + type guards | **ABSENT** |

### Read-only guard — GENERIC pattern

`services/mtafiti/executor/readonly_sql_guard.py` (extant CP1 of W-MTAFITI-GPU-DISCOVERY · 20+ statement classes refused) is the archetype. Every connector implementation implements a `read_only_guard(operation)` that refuses everything outside `{list, read, stream, status}` (spec §C4-013 §10 Repeatable is the anchor: same inputs → same measured output requires no side-effects).

**Owner correction owed:** in the prior audio-programme roadmap I named the missing NAS guard as `readonly_media_guard.py`. Under the reframe, this is one implementation of the generic `read_only_guard()` — not its own separate service. The right shape is `services/source_plane/connectors/synology_filestation.py::SynologyFileStationConnector.read_only_guard`.

---

## A.3 · Capability Registry

### Contract — a Capability is a pluggable processor

```python
class Capability(BaseModel):
    """A registered processing capability, invoked per-segment or per-record."""
    model_config = ConfigDict(extra="forbid", frozen=True)
    capability_id: str                                # e.g. "asr:sunbird-51-african"
    capability_class: Literal[
        "vad", "lid", "asr", "diarization", "speaker_embedding",
        "music_detect", "music_separation", "quality_score",
        "pii_detect", "column_classify", "ner", "de_identify",
        "translation", "vision_ocr", "vision_tagger",
        # extensible — add class only via ceremony
    ]
    input_contract_ref: str                           # frozen input contract
    output_contract_ref: str                          # frozen output contract
    determinism: Literal["deterministic", "seeded_nondeterministic", "nondeterministic"]
    resource_class_required: Literal["gpu", "cpu", "either"]
    model_ref: Optional[str] = None                   # e.g. "hf:facebook/mms-lid-4017"
    library_deps: List[str]                           # deps that must be installed
    provider_ref: str                                 # dotted path to callable class
    fail_shape: Literal["fail_closed", "provider_unavailable", "refusal_family"]
```

### Interface

```
register(capability: Capability) -> RegisterReceipt
select_by_class(cls: str, requirements: Dict) -> List[Capability]
invoke(capability_id: str, input: Any) -> Any                 # deterministic → determinism_pin honoured
availability_probe() -> Dict[str, bool]                        # per capability, buildable-now vs missing dep
```

### Current state

- **Extant primitive:** `services/layer_b/factory.py` (`_ASR_REGISTRY`, `_DIARIZATION_REGISTRY`, `_VISION_REGISTRY` — dotted-path registries with env-var selection). `available_providers()` docstring line 66-85 verbatim: *"A provider is 'available' iff its class can be constructed without raising ProviderUnavailable. This lets the system surface honestly flag which providers are wired but un-installed."*
- **Missing platform layer:** the framework is ASR/diarization/vision-specific. **W1 platform wave generalises `layer_b.factory` into `services/capability_registry/*` with the extensible `capability_class` enum + registration flow.**

### What the plane does NOT include

- Not "MMS-LID-4017". Not "Sunbird". Not "HTDemucs". These are **specific `Capability` instances** registered via `register(...)`. The platform code path knows only `capability_class="lid"`; the JobManifest binds `capability_id="lid:mms-4017"` for THIS job.

---

## A.4 · Objective Plane (L1)

### Contract

```python
class MtafitiObjectiveCarrier(BaseModel):
    """EXTANT frozen contract (CP1 W-MTAFITI-GPU-DISCOVERY).
       Refuses mtafiti-internal origin by construction."""
    origin: Literal["TARGETA", "CIF", "COACH_ORIGINATION_PORT"]
    ...
```

### Interface (per Audio Plane §8 — schema compiler)

```
compile(commission_prose: str, coach_ratified: bool) -> Tuple[MtafitiObjectiveCarrier, CollectionSchema]
```

### Current state

- **Extant:** `contracts/mtafiti_objective_carrier.py` (REAL, CP1 origin).
- **Missing:** `services/objective_wizard/*` — Audio Plane §8.4 says the wizard **refuses at compile-time** on `(a) Outcome without existing test_set_ref, (b) acceptance bar missing per-stratum dimension, (c) schema requiring column that violates §6.2 custody`.

### Platform vs job

- Platform: the carrier contract + compiler port + rejection classes.
- Job: the concrete NL commission + its compiled TargetOutcome + CollectionSchema — data, not code.

---

## A.5 · Outcome + Quality Plane (L2)

### Contract (per Audio Plane §10.1 verbatim schema — this reframe formalises it)

```python
class TargetOutcome_v0(BaseModel):
    """Audio Plane §10.1 schema, generalised across modalities."""
    model_config = ConfigDict(extra="forbid", frozen=True)
    task: str                                          # operational · falsifiable
    domain: str
    population: PopulationSpec                          # per §10.2 register-strata-defined
    acceptance: List[StratumAcceptance]                 # per-stratum · 2D · accuracy × coverage
    gate_policy: Literal["missed_stratum_gates_release", "ships_documented"]
    test_set_ref: str                                   # must exist at freeze time
    constraints: OutcomeConstraints                      # latency_p95_ms · compute_budget · deployment_target
```

```python
class StratumAcceptance(BaseModel):
    stratum_id: str
    accuracy_metric: str                                # e.g. "WER", "CER", "F1", "MCC"
    accuracy_threshold: float
    coverage_metric: str                                # e.g. "hours", "count", "distinct_speakers"
    coverage_threshold: float
    evidence_class: Literal["measured", "projected", "aspirational"]  # §10.1 evidence classing
```

### Current state

- **Missing frozen contract** — `contracts/target_outcome_v0.py` is absent.
- **Extant instrumentation:** `services/perception/execution_mode_telemetry.py` emits per-CP rung-1 telemetry to `phase0/baseline_lines/`.

### Platform vs job

- Platform: the schema + the writer that composes rung-1 telemetry into a MOAC scorecard.
- Job: the concrete `task="build music-free non-English speech corpus"` + specific stratum thresholds — **data, not code.**

**Key spec discipline:** thresholds are **evidence-classed** (measured / projected / aspirational). Per Audio Plane §11.2: *"Data requirements for low-resource fine-tuning are empirical; no analytical answer exists"* — thresholds land at CP2 of any job after Sampling & Reflection returns real numbers, not before.

---

## A.6 · Success + QC Plane (L3) — the composable gate framework

### Contract — a Gate is a pluggable admission predicate

```python
class Gate(BaseModel):
    gate_id: str                                       # e.g. "gate:held_out_preflight"
    gate_class: Literal[
        "held_out_preflight", "pii_redaction", "readonly_source",
        "critic_seam", "release_gate", "au3_completeness",
        "output_verified_seal",                          # NEW · from W0
        "progress_signal",                               # NEW · from W1
        "double_green_ratchet",
    ]
    admit_predicate: Callable[[Artifact, Ruling], AdmissionVerdict]
    refusal_class: str                                  # ties to memory_refusal_reasons.v0.json
    order_hint: int                                     # gates compose in ascending order
```

### Interface

```
compose_pipeline(gates: List[Gate]) -> AdmissionPipeline
admit(artifact: Artifact, pipeline: AdmissionPipeline) -> AdmissionVerdict
```

### Current state

- **Extant gates (already registered as primitives, un-registered as a framework):**
  - `services/shield_train/held_out.py::bank_held_out_slice_hash` — held-out preflight.
  - `services/mtafiti/detectors/pii_redaction_guard.py::assert_no_raw_pii` — PII redaction.
  - `services/mtafiti/executor/readonly_sql_guard.py` — RDBMS read-only.
  - `services/shield_train/*::MaskingTierNotAdmitted` — masking-tier HARD GATE.
  - Double-green `BASELINE_GUARD=1` — STANDING_ORDERS §3.
- **Missing gates (deliverables of W0 + W1):**
  - `output_verified_seal(run_dir) = is_real_seal(md_path) AND artifact_gate_passed(run_dir)` — **W0.**
  - `progress_signal(run_id, poll_window_s)` — **W1.**
  - `critic_seam(*)` — `docs/requirements/critic_seam_spec_v1_1.md` landed; code absent.
  - `release_gate(artifact, four_verdicts)` — Ruling #5 chokepoint.
- **Missing framework:** a `services/gate_framework/*` composition service that runs an admission pipeline against an Artifact.

### Platform vs job

- Platform: the Gate contract, the composition framework, the extant primitives, W0's new `output_verified_seal`, W1's `progress_signal`.
- Job: the specific list of gates + their thresholds (SNR ≥ 25 dB, MOS ≥ 3.0) — data.

---

## A.7 · Commission + Worker Plane (L4)

### Contract — Commission and Worker

```python
class CommissionSpec(BaseModel):
    """The declarative artifact that turns an Objective into a plan."""
    commission_id: str
    objective_carrier_ref: str                          # frozen from L1
    outcome_ref: str                                    # frozen from L2
    milestones: List[Milestone]                         # per §11.3
    worker_lanes: List[WorkerLane]
    handoff_contract_ref: str                           # per Canon 4 §17 seam contract
    started_at: str

class Milestone(BaseModel):
    milestone_id: str
    done_condition: DoneCondition                        # artifact-existence + gate-pass composite
    owner: str                                           # human owner
    status: Literal["done", "on_track", "behind", "missed"]  # §13.2 verbatim vocabulary
    depends_on: List[str]                                # ordering

class WorkerLane(BaseModel):
    lane_id: str
    resource_id: str                                     # from Resource Plane (A.1)
    capability_pipeline: List[str]                       # capability_ids from Capability Registry (A.3)
    kpi_thresholds: Dict[str, float]                     # gate thresholds from L3

class WorkerJD(BaseModel):
    """Worker Job Description — what a lane executes."""
    jd_id: str
    lane_ref: str
    inputs: List[str]
    outputs: List[str]
    determinism_pin: bool
    resource_requirement_tags: List[str]
    escalation_hooks: List[EscalationHook]
```

### Current state

- **Extant:** `services/campaign_infra/manifest.py::CampaignManifest` (LORA-training-specific 6-field schema) + `run_queue.py` + `production_trainer.py` + `on_host_trainer.py`.
- **Missing:** the generic CommissionSpec/Milestone/WorkerLane/WorkerJD contracts. The current campaign manifest is a **LORA-trainer specialisation of the abstract commission** — the reframe promotes the abstract to platform-primary + demotes LORA to a specific WorkerJD.

### Platform vs job

- Platform: the four contracts above + the generic run-queue + the injected `worker_fn` seam (already the shape of `execute_campaign(trainer_fn=...)`).
- Job: the concrete milestone list + lane bindings + KPI thresholds — data.

---

## A.8 · Supervision Plane (L5) — the OUTSIDE work-supervisor

### Contract

> **⚠ SUPERSEDED SHAPE (aspirational · authored 2026-09-11) ⚠**
>
> The 9-field `ProgressSignal` shape below (`run_id · resource_id · at_utc · gpu_util_pct_rolling_avg · output_artifact_growth_bytes · checkpoint_step_delta · loss_delta_last_n_steps · verdict Literal["PROGRESSING", "STALLED", "ZERO_UTIL_ALARM", "OUTPUT_STARVATION_ALARM"]`) plus the 3-field `StarvationAlarm` with closed-enum `reason` are **SUPERSEDED** by the actual W1 close (2026-09-13T06:33:22Z · commit `fe01e5e`).
>
> **Owner CP-breakdown correction verbatim (2026-09-13 · W1 CP approval):**
>
> > "CORRECTION — job_kind must stay CASE-AGNOSTIC ... Do NOT lock a closed 5-value audio-harvest enum into the platform JobManifest at CP1 — that leaks the audio case into generic platform code. Instead make job_kind reference an OPEN, registry-backed kind: a capability/job-kind REGISTRY that jobs register into."
>
> The same correction binds ALL W1-family platform kernels: closed-value enums (`verdict Literal[...]` · `reason Literal[...]`) that name specific-case verdict spaces leak the case into generic platform code and are BANNED. Under that correction, the W1 kernel deliberately ships **case-agnostic minimal** primitives:
>
> **Canonical W1 `ProgressSignal` (5 fields, frozen dataclass):**
> `job_id: str · at_utc: str (ISO Z) · magnitude: float (opaque scalar; downstream interprets) · output_bytes: int (cumulative) · output_path: str (or "" if no artifact)`.
>
> **Canonical W1 `HaltVerdict` (5 fields, frozen dataclass):**
> `job_id: str · reason: str ∈ {starvation_no_signal, starvation_stale_signal, starvation_output_flatline} · at_utc: str · last_progress_at_utc: str · message: str`.
>
> The three closed-enum reason strings on `HaltVerdict.reason` describe STARVATION MODES (universal across every commissioned run · not case-specific verdict spaces). This preserves case-agnostic discipline while giving callers a structured refusal.
>
> **Canonical W1 `StarvationAlarm(RuntimeError)`:** named exception class for wrapping-boundary use. Not a dataclass; not a data return value. The public watchdog returns `HaltVerdict` (data); callers may raise `StarvationAlarm` at their own boundary if desired.
>
> **Canonical W1 primitive interface** (`services/work_supervisor/runtime_supervisor.py`):
>
> - `record_progress(sig: ProgressSignal, *, ring_root: Path) -> Path` — writer; returns the ring file path.
> - `load_progress(job_id: str, *, ring_root: Path) -> List[ProgressSignal]` — reader; returns list sorted by at_utc.
> - `output_verification_watchdog(job_id, *, sla_seconds, ring_root, now_utc, output_path=None) -> HaltVerdict | None` — readiness gate; returns HaltVerdict on first starvation hit, None on healthy.
>
> **Zero-influence contract** (verbatim `runtime_supervisor.py` docstring lines 19-21): the watchdog READS progress signals + optionally STATs the named output artifact. It never kills any process. A HALT verdict is DATA (a returned dataclass); callers act on it. Observation and mutation remain separate.
>
> **Wave-honest limit** (verbatim SO §3.2 clause 4): the W1 watchdog measures BYTE growth, not semantic growth. A run that writes zeros steadily would pass the flatline check. Semantic watchdogs (per-kind output shape validators) are Part-B concerns.
>
> The aspirational 9-field `ProgressSignal` + 3-field `StarvationAlarm` shapes below are retained here as historical reference of what the pre-correction plan looked like; they are NOT the platform kernel's schema. Reading the shapes below as required platform-kernel schemas misreads what actually landed under the 2026-09-13 case-agnostic correction.

**Aspirational shapes (SUPERSEDED — kept for historical reference · not a build target):**

```python
class ProgressSignal(BaseModel):
    """[SUPERSEDED — see above · not the platform kernel schema.]"""
    run_id: str
    resource_id: str                                    # supervisor watches ANY resource
    at_utc: str
    gpu_util_pct_rolling_avg: Optional[float]           # None if resource_class != gpu
    output_artifact_growth_bytes: int
    checkpoint_step_delta: int
    loss_delta_last_n_steps: Optional[float]
    verdict: Literal["PROGRESSING", "STALLED", "ZERO_UTIL_ALARM", "OUTPUT_STARVATION_ALARM"]

class StarvationAlarm(BaseModel):
    """[SUPERSEDED — the canonical class is an exception, not a dataclass.]"""
    lane_id: str
    since_utc: str
    reason: Literal["queue_drained", "trainer_dead", "zero_util_over_sla"]
```

### Interface

```
subscribe(resource_id: str, poll_interval_s: int) -> None
signal(resource_id: str) -> ProgressSignal
alarm_write(alarm: StarvationAlarm) -> AlarmReceipt
escalate(mark: WatchMark) -> None                        # to Canon 8 Macho if Watch bundle lands
```

### Current state

- **Extant primitive:** `services/orchestrator_resilience/*` — process-level supervision (heartbeat freshness · PID liveness · orphan adoption). **These check PROCESS ALIVENESS, not WORK PROGRESS** (per `notes/SILENT_FAILURE_ROOTCAUSE_AND_LAYER_MAP.md §1`).
- **Missing:** `services/work_supervisor/*` — the OUTPUT-verifying supplement. **This is W1's deliverable.**

### Standing law introduced by W1

**New STANDING ORDER — "No run without progress signal":**

> *"Every registered WorkerLane MUST emit a ProgressSignal on each supervisor poll cycle. A lane whose supervisor signals `ZERO_UTIL_ALARM` for N consecutive polls (SLA-default 3 at 60 s intervals = 3 min) HALTS via MARK write to the Supervision Plane. Queue-drained lanes emit `StarvationAlarm` within SLA-default 15 min. A dispatcher heartbeat is not evidence of work; only a ProgressSignal with `verdict=PROGRESSING` is."*

---

## A.9 · HITL Plane (L6)

### Contract

```python
class MilestoneStream(Protocol):
    def subscribe(job_id: str, since_utc: str) -> Iterator[MilestoneEvent]: ...
    def ratify(milestone_id: str, coach_id: str, ratified_at: str) -> RatificationReceipt: ...
    def dispute(milestone_id: str, coach_id: str, reason: str) -> DisputeReceipt: ...
```

### Current state

- **Missing:** no `services/hitl/*` on `programme/track-a`. Owner reads STATE files + probes hosts via SSH.
- **Extant convention:** the 5-section wave-close markdown pattern is the informal L6 surface today.

### Ratification gate — from Audio Plane §13.2 verbatim

> *"At Sampling & Reflection, the proposed milestone list is presented to the objective owner for agreement. **Commission does not open until it is agreed.**"*

The platform L6 API enforces this by construction: `CommissionSpec.status = OPENED` requires `MilestoneStream.ratify(...)` receipts for every milestone in the list.

### Platform vs job

- Platform: the stream + ratify + dispute API + the ratification-gate predicate.
- Job: the specific milestones + specific coach IDs — data.

---

## A.10 · Governance Plane

### The plane's contracts + primitives (extant + new)

| # | Primitive | Path | State |
|---:|---|---|---|
| 1 | Rulebook (Canon 7 D-01..D-26 defect classes) | `notes/canon_7_requirements.md` | authored |
| 2 | Refusal-family registry | `services/memory/memory_refusal_reasons.v0.json` | REAL |
| 3 | Owner-ruling banking discipline (STANDING_ORDERS §2) | `STATE/DECISIONS.md` | REAL |
| 4 | Determinism boundary (`extraction_params@v0` temperature=0) | `contracts/extraction_params.py` | REAL |
| 5 | AU-3 six-element ledger (BA-8.1) | `services/northena/ledger.py` writer; gating invariant absent | PARTIAL |
| 6 | Release gate (four verdicts) | absent | NEW · W-DELIVERABLE-GOVERNANCE wave |
| 7 | Custody boundary primitives (§6.2 forbid) | absent (Character Register) | ABSENT |
| 8 | Data-protection chokepoint (KDPA-verdict field) | absent | NEW · same wave as (6) |
| 9 | IP/consent chokepoint (`licence_class`) | `services/perception/eab_1_pipeline/a2_license_class.py` (three-class enum) | REAL |
| 10 | Cross-border transfer chokepoint (§48/§51) | absent | NEW |

### Release gate — GENERIC contract

```python
class ReleaseGateVerdicts(BaseModel):
    """Four-verdict primitive. Any deliverable release requires ALL four ADMISSIBLE."""
    kdpa_verdict: Literal["PENDING", "ADMISSIBLE_CONSENT", "ADMISSIBLE_LEGITIMATE_INTEREST",
                          "ADMISSIBLE_DPIA_APPROVED", "REFUSED"] = "PENDING"
    named_persons_verdict: Literal["PENDING", "DE_IDENTIFIED_PASS", "REDACTED_PASS", "REFUSED"] = "PENDING"
    transfer_basis: Literal["PENDING", "SCC", "ADEQUACY", "RESEARCH_CARVE_OUT_51", "CONSENT", "REFUSED"] = "PENDING"
    licence_class: str                                   # from A.9 primitive #9

def admit_release(artifact: Artifact, tier: ReleaseTier, verdicts: ReleaseGateVerdicts) -> AdmissionVerdict:
    """Refuses tiers {biometric_embedding, named_identity, speaker_labeled_audio,
                     audio_speech_no_speaker, audio_speech_with_speaker} until owner ruling."""
```

### Retention primitive — GENERIC (this is the reframe's answer to the storage/purge question)

```python
class RetentionPolicy(BaseModel):
    """Applied per Artifact class. The plane supports THREE distinct retention regimes."""
    artifact_class: str
    regime: Literal[
        "SOURCE_UNTOUCHED",      # source estate never modified — a1_demux discipline
        "WORKER_SCRATCH_PURGED", # V1-D1 purge_attestation REQUIRED
        "REGISTER_DESCRIPTIVE",  # §6.2 four conditions — never audio, never per-utterance embedding
        "DELIVERABLE_GOVERNED",  # C4-022 §16 frozen unit contract — governed retain-exception
    ]
    ttl_days: Optional[int] = None                       # None = indefinite under governance
    release_gate_verdicts_required: bool = True          # if regime = DELIVERABLE_GOVERNED
```

**This IS the platform-level answer to §6.2 vs sale-of-corpus.** The plane supports FOUR distinct retention regimes, each with its own governance surface. Any Artifact class binds to exactly one regime. **The measurement plane's purge default (regime 2) does NOT preclude the deliverable plane's governed retention (regime 4)** — they are ORTHOGONAL under the plane's architecture. See §C below for the full clause verification + this-job answer.

---

## A.11 · JobManifest — the MOUNTING schema

The declarative artifact that mounts a specific job onto the platform. **This is the case-specific artifact — everything else in Part A is case-agnostic.**

> **⚠ SUPERSEDED SHAPE (aspirational · authored 2026-09-11) ⚠**
>
> The 15-field shape below (job_class · mounted_at · mounted_by · objective_carrier_ref · target_outcome_ref · source_bindings · resource_bindings · capability_pipeline · gate_composition · commission_spec_ref · supervision_config · hitl_config · retention_policy_ref · owner_rulings · release_gate_verdicts_current · manifest_sha256) is **SUPERSEDED** by the actual W1 close (2026-09-13T06:33:22Z · commit `fe01e5e`).
>
> **Owner CP-breakdown correction verbatim (2026-09-13 · W1 CP approval):**
>
> > "CORRECTION — job_kind must stay CASE-AGNOSTIC ... Do NOT lock a closed 5-value audio-harvest enum into the platform JobManifest at CP1 — that leaks the audio case into generic platform code. Instead make job_kind reference an OPEN, registry-backed kind: a capability/job-kind REGISTRY that jobs register into."
>
> Under that correction, the W1 JobManifest kernel deliberately ships **v0** with a **10-field case-agnostic surface** — `manifest_version=0 · job_id · job_kind (registry-backed) · submitter · submitted_at_utc · scope (opaque dict) · output_contract (dict) · depends_on (list[str]) · dispatch_intent · precondition_seals (list[{run_dir, expected_kind}])` — and pushes all case-specific plane bindings into the `scope: dict` opaque field where downstream job waves (W2+) attach them WITHOUT the platform kernel adopting any case-specific field.
>
> The aspirational 15-field shape below is retained here as the **case-specific expansion** a mounting job's YAML instance may carry inside its `scope: dict` — it is NOT the platform kernel's schema. Reading the shape below as a required platform-kernel schema misreads what actually landed.
>
> **Canonical W1 platform kernel:** `services/work_supervisor/job_manifest.py::JobManifest` (v0 · 10 fields).
> **Canonical parse:** `services/work_supervisor/job_manifest.py::parse_job_manifest(payload: dict) -> JobManifest`.
> **Canonical failure:** `JobManifestInvalid(ValueError)`.
> **Canonical kind registration:** `services/work_supervisor/kind_registry.py::register_kind(name)` + `is_registered(name)`. Sole platform-side seed: `platform.generic`. Case-specific kinds register at their own case wave.

**Aspirational 15-field shape (SUPERSEDED — kept for historical reference · not a build target):**

```python
class JobManifest(BaseModel):
    """[SUPERSEDED — see above · not the platform kernel schema.]
    Binds platform planes to a specific job instance. Frozen at mount time."""
    model_config = ConfigDict(extra="forbid", frozen=True)

    # Identity
    job_id: str
    job_class: str                                       # e.g. "audio-census", "text-training", "image-taxonomy"
    mounted_at: str                                      # ISO-8601 UTC
    mounted_by: str                                      # coach or origination port ref

    # A.4 Objective Plane
    objective_carrier_ref: str                           # frozen MtafitiObjectiveCarrier instance

    # A.5 Outcome + Quality Plane
    target_outcome_ref: str                              # frozen TargetOutcome instance

    # A.2 Source Plane
    source_bindings: List[SourceBinding]                 # {connector_id, source_path, credentials_ref}

    # A.1 Resource Plane
    resource_bindings: List[ResourceBinding]             # {resource_id, lane_assignments}

    # A.3 Capability Registry
    capability_pipeline: List[CapabilityBinding]         # ordered list of {capability_id, invocation_params}

    # A.6 Success + QC Plane
    gate_composition: List[GateBinding]                  # ordered gates for admit_release

    # A.7 Commission + Worker Plane
    commission_spec_ref: str                             # frozen CommissionSpec instance

    # A.8 Supervision Plane
    supervision_config: SupervisionConfig                 # SLA thresholds for progress + starvation

    # A.9 HITL Plane
    hitl_config: HitlConfig                              # ratification-gate coach list + poll interval

    # A.10 Governance Plane
    retention_policy_ref: str                             # frozen RetentionPolicy instance
    owner_rulings: List[OwnerRulingRef]                   # verbatim-banked rulings applicable to this job
    release_gate_verdicts_current: ReleaseGateVerdicts    # PENDING at mount; updated as rulings arrive

    # Freeze contract
    manifest_sha256: str                                  # content-address of this manifest
```

**A JobManifest is IMMUTABLE once mounted.** A change to any binding is a **new job** (§10.2 verbatim discipline: *"A change is a NEW run, not a mutation"*).

---

## A.12 · PLATFORM build waves — W0 · W1

**These are the platform's own build waves.** They apply to ANY future job (audio census · text training · image taxonomy · anything else). They do NOT require the audio-specific mount to exist.

### W0 · Integrity fix — silent-success defect (S-class · PLATFORM)

Fixes six specific code sites where the platform conflates process-liveness with work-progress. Full anatomy in `notes/SILENT_FAILURE_ROOTCAUSE_AND_LAYER_MAP.md §1`. Delivers:

- Parse `Kind:` field in every seal predicate.
- Introduce `output_verified_seal(run_dir)` composite predicate.
- **New STANDING ORDER: "Alive != done."** — appended to STANDING_ORDERS.md.

### W1 · Work-supervisor + Resource Registry + Capability Registry generalisation (M-class · PLATFORM)

> **⚠ ACTUAL-VS-ASPIRATIONAL SCOPE RECONCILIATION (banked 2026-09-16T~05:15Z per owner ruling) ⚠**
>
> The five-item deliverable list below (authored 2026-09-11) is the aspirational W1 scope. The **actual W1 close** landed 2026-09-13T06:33:22Z (commit `fe01e5e` · ratchet 3282→3392) delivered ONE of the five items in ratified case-agnostic-simplified form:
>
> - **DELIVERED at W1 close:** `services/work_supervisor/{runtime_supervisor, supervisor, governance, job_manifest, kind_registry}.py` — case-agnostic under the 2026-09-13 verbatim owner correction ("job_kind must stay CASE-AGNOSTIC ... Do NOT lock a closed 5-value enum into the platform"). See §A.8 SUPERSEDED reconciliation for canonical shapes. STANDING ORDER §3.2 "NO RUN WITHOUT A PROGRESS SIGNAL" appended to STANDING_ORDERS.md.
> - **DELIVERED at W1b close (2026-09-13T06:59:30Z · commit `53645935` · 26 minutes after W1 close · ratchet 3392 → 3492 · +100):** `services/capability_registry.py` (case-agnostic capability registry · compose-not-modify with `services/layer_b/factory.py` · frozen by 15 W1b CP4 invariants at `tests/invariants/test_w1b_cp4_capability_registry.py`) + `services/governance_plane/retention_policy.py` (RetentionPolicy primitive) + `services/source_plane/connector.py` (SourceConnector Protocol) + `services/source_plane/synology_file_station.py` (interface-only) + `services/audio_plane_v1/attribute_stream_bundle.py` (generic AttributeStreamBundle_v0) + L2/L4 contract shells. **This W1b close was OVERLOOKED by the M7 W1 verification receipt (this-shift · 2026-09-16T~04:15Z)** — the receipt covered only W1 close (commit `fe01e5e` at 06:33Z), missing W1b 26 minutes later. Surfaced as a wave-honest gap in the CP-M7-W1-POST-2 verification walk (2026-09-16T~06:00Z · Path α clean).
> - **NOT DELIVERED at W1 close but DELIVERED at CP-M7-W1-POST-1 (this shift · 2026-09-16T~05:45Z · track-a `2c7a8f0c` · master `51555512` · ratchet 4358 → 4384 · +26):** `services/resource_registry/{__init__, registry}.py` (case-agnostic Resource Registry · scope boundary registry-surface-only per owner ruling 2026-09-16T~05:10Z).
> - **CAPABILITY REGISTRY ratified at CP-M7-W1-POST-2 (this shift · 2026-09-16T~06:00Z · verification walk · Path α clean · zero-delta):** pre-existing W1b `services/capability_registry.py` verified to satisfy owner ruling INTENT (case-agnostic + compose-not-modify). No new mechanism landed; ratchet unchanged 4384.
> - **STILL UNVERIFIED (candidate CP-M7-W1-POST-3-VERIFICATION):** the other 5 W1b deliverables — RetentionPolicy + SourceConnector Protocol + Synology FileStation + AttributeStreamBundle_v0 + L2/L4 shells — remain unverified as of this shift. Owner-desk item.
>
> **W1 close did NOT under-deliver by mistake.** It delivered the CORRECTED case-agnostic-minimal scope under the 2026-09-13 verbatim owner correction. Reading the aspirational 5-item list below as a completed-vs-shipped checklist misreads the correction; the correction narrowed W1's kernel scope while leaving `resource_registry` + `capability_registry` for the same case-agnostic pattern in a later CP.
>
> **W-M7-W0-VERIFICATION** (Path α clean · 2026-09-16T~04:00Z) verified the §3.1 primitive is enforced.
> **W-M7-W1-VERIFICATION** (Path α clean · 2026-09-16T~04:15Z) verified the §3.2 kernel is enforced and unchanged since W1 close.
> **CP-M7-W1-POST-1** (this shift) lands `services/resource_registry/*`.
> **CP-M7-W1-POST-2** (this shift) lands `services/capability_registry/*` via compose-not-modify delegation to `services/layer_b/factory.py`.

**Aspirational W1 deliverable list (historical reference · reconciled above):**

- `services/work_supervisor/{progress_signal, output_verification_watchdog, starvation_alarm}.py` (per §A.8).
- `services/resource_registry/*` (per §A.1).
- Generalise `services/layer_b/factory.py` → `services/capability_registry/*` (per §A.3).
- Extend `services/source_plane/connectors/*` with the NAS/S3/HTTP interface (per §A.2).
- **New STANDING ORDER: "No run without progress signal."** — appended to STANDING_ORDERS.md.
- Governance-Plane primitives: generic `ReleaseGateVerdicts` + `RetentionPolicy` contracts + `release_gate.py` module (per §A.10).

**Both waves land ZERO case-specific code.** They introduce reusable planes any future mount consumes.

---

# PART B · THIS JOB MOUNTED (the audio census as ONE instance)

**Job class:** `audio-census`. Bound to the platform via a `JobManifest`. Everything below is CONFIG/DATA on top of Part A's plane implementations.

## B.1 · Job identity

- **`job_id`**: `audio-census-rms-16-stations-non-english-music-free-v1`.
- **`job_class`**: `audio-census`.
- **`mounted_by`**: owner via TARGETA origination.
- **Objective in plain language (frozen at mount):** *"Build a non-English, music-free, quality-graded speech corpus from off-air recordings of 16 Kenyan RMS stations, extracting maximum context internally, releasing to a research lab under KDPA + owner Ruling #5 verdicts."*

## B.2 · The concrete JobManifest — bindings

### B.2.1 · Source bindings (A.2)

```yaml
source_bindings:
  - source_binding_id: "src:synology:rms-nairobi"
    connector_id: "connector:synology-filestation"
    source_path: "http://10.10.55.55:5000"
    credentials_ref: "custody:/app/backend/estate_keys/data_sources/synology-rms.json"  # 0600, git-ignored
    licence_class: "owner_full_rights"   # per Owner Ruling #2 (2026-09-12T~12:00Z)
    reachability_status: "BLOCKED_NEEDS_BASTION_OR_VPN"
```

### B.2.2 · Resource bindings (A.1)

```yaml
resource_bindings:
  - resource_id: "host:akki-vm:gpu:0"
    capability_tags: ["nvidia:h200","vram:80gb","cuda:12.4"]
    lane_assignment: "heavy-asr-lane"     # Sunbird whisper + MMS-1B-all + pyannote-3.3.2 + HTDemucs
  - resource_id: "host:akki-vm:gpu:1"
    lane_assignment: "light-perception-lane"  # MMS-LID-4017 + PANNs + WavLM + SQUIM/DNSMOS
  - resource_id: "host:akki-vm-ii:gpu:0"
    lane_assignment: "heavy-asr-lane"       # mirror for parallel-station processing
  - resource_id: "host:akki-vm-ii:gpu:1"
    lane_assignment: "light-perception-lane"
```

### B.2.3 · Capability pipeline (A.3)

```yaml
capability_pipeline:
  - {capability_id: "vad:silero", invocation_params: {threshold: 0.5, min_speech_ms: 250}}
  - {capability_id: "lid:facebook/mms-lid-4017", invocation_params: {segment_boundary: "post-vad-speech"}}
  - {capability_id: "music_detect:panns-cnn14", invocation_params: {music_class_threshold: 0.5}}
  - {capability_id: "music_separation:htdemucs_ft", invocation_params: {two_stems: "vocals", trigger_if: "music_prob>0.5"}}
  - {capability_id: "asr:sunbird/faster-whisper-51-african-languages",
     invocation_params: {temperature: 0, beam_size: 5},
     routing: "top1_lang ∈ sunbird_supported_51"}
  - {capability_id: "asr:facebook/mms-1b-all",
     invocation_params: {temperature: 0},
     routing: "top1_lang ∉ sunbird_supported_51 OR top1_confidence < 0.60"}
  - {capability_id: "diarization:pyannote/speaker-diarization-3.1", invocation_params: {min_speakers: 1, max_speakers: 8}}
  - {capability_id: "speaker_embedding:microsoft/wavlm-base-plus-sv",
     invocation_params: {retention_regime: "REGISTER_DESCRIPTIVE"}  # destroy after cluster-assign
    }
  - {capability_id: "quality_score:torchaudio-squim+dnsmos", invocation_params: {mos_metric: "MOS_SIG"}}
```

**All capability_id values above must be REGISTERED into the Capability Registry (A.3) before this manifest can be mounted.**

### B.2.4 · Target Outcome (A.5)

```yaml
target_outcome:
  task: "produce_music_free_non_english_speech_corpus"
  domain: "kenyan_vernacular_broadcast_audio"
  population:
    strata:
      - {stratum_id: "kikuyu-kik", accent_cluster: "central-mt-kenya", condition: "off-air-broadcast"}
      - {stratum_id: "dholuo-luo", accent_cluster: "nyanza", condition: "off-air-broadcast"}
      - {stratum_id: "kamba-kam",  accent_cluster: "eastern",  condition: "off-air-broadcast"}
      # Extendable per W-scale wave for stations 4-16
  acceptance:
    - {stratum_id: "kikuyu-kik", accuracy_metric: "WER", accuracy_threshold: 0.209,  # Sunbird published baseline
       coverage_metric: "hours",  coverage_threshold: 10.0,        # POC W3 target
       evidence_class: "measured"}
    - {stratum_id: "dholuo-luo", accuracy_metric: "WER", accuracy_threshold: 0.226,
       coverage_metric: "hours",  coverage_threshold: 10.0,
       evidence_class: "measured"}
    - {stratum_id: "kamba-kam",  accuracy_metric: "WER", accuracy_threshold: null,   # SEE NOTE
       coverage_metric: "hours",  coverage_threshold: 10.0,
       evidence_class: "projected"}                                                   # measured at CP2
  gate_policy: "missed_stratum_gates_release"    # fail-loud/HALT
  test_set_ref: "audio-poc-heldout-v1"           # created at W2 CP1 via deterministic_20pct_tail_split
  constraints:
    latency_p95_ms: null                         # POC: not a real-time job
    compute_budget_gpu_hours: 40                 # est per §2.1 · updates at Sampling & Reflection
    deployment_target: "batch_offline"
```

**IMPORTANT NOTE on `kamba-kam` acceptance_threshold=null:** Sunbird's 51-African-language whisper **DOES NOT cover Kamba** (`kam`) — verified this session against the Sunbird HF model card. The Kamba fallback ASR path is `facebook/mms-1b-all` which supports 1,162 languages. **The Kamba WER threshold is `null` at mount because it must be MEASURED at CP2 via Sampling & Reflection** (§11.2 discipline: *"train at three to four data volumes, evaluate per stratum against the test set, fit the scaling curve, extrapolate to the acceptance threshold"*). Sunbird published Kikuyu/Luo WERs (0.209/0.226) enter as `evidence_class:measured`; Kamba enters as `evidence_class:projected`.

### B.2.5 · Gate composition (A.6)

```yaml
gate_composition:
  - {gate_id: "gate:readonly_source", order_hint: 10}          # Synology FileStation List/Read/Status only
  - {gate_id: "gate:pii_redaction", order_hint: 20}            # PII in transcripts
  - {gate_id: "gate:output_verified_seal", order_hint: 25}     # W0 primitive
  - {gate_id: "gate:progress_signal", order_hint: 26}          # W1 primitive
  - {gate_id: "gate:held_out_preflight", order_hint: 30}
  - {gate_id: "gate:critic_seam", order_hint: 40}              # ASR + diarization worker outputs
  - {gate_id: "gate:quality_score_floor",                       # SNR/MOS/LUFS floors
     order_hint: 50,
     params: {snr_reject_db: 15.0, snr_flag_db: 25.0, mos_reject: 2.5, mos_accept: 3.0, lufs_target: -23.0}}
  - {gate_id: "gate:non_english_filter", order_hint: 60,
     params: {reject_language: "eng", min_top1_confidence: 0.60}}
  - {gate_id: "gate:music_free_filter", order_hint: 70,
     params: {music_prob_max: 0.5, vocals_snr_min_db: 15.0}}
  - {gate_id: "gate:release_gate", order_hint: 999,
     params: {refused_tiers: ["biometric_embedding","named_identity","speaker_labeled_audio"]}}
```

### B.2.6 · Retention policy (A.10)

```yaml
retention_policy:
  bindings:
    - {artifact_class: "source-audio-file", regime: "SOURCE_UNTOUCHED"}
    - {artifact_class: "worker-scratch-audio", regime: "WORKER_SCRATCH_PURGED",
       purge_attestation_required: true}
    - {artifact_class: "speaker-embedding-per-utterance", regime: "REGISTER_DESCRIPTIVE",
       destroy_after_cluster_assign: true}
    - {artifact_class: "character-register-entry", regime: "REGISTER_DESCRIPTIVE",
       stored_form: ["centroids","distributions","frequencies"]}
    - {artifact_class: "corpus-deliverable-transcript", regime: "DELIVERABLE_GOVERNED",
       release_gate_verdicts_required: true}
    - {artifact_class: "corpus-deliverable-audio-segment-bytes",
       regime: "DELIVERABLE_GOVERNED_PATH_A_PENDING_OWNER_RULING",   # SEE §C
       release_gate_verdicts_required: true,
       licence_class_extension: "owner_full_rights_speech_corpus"}
```

### B.2.7 · Owner rulings (A.10)

```yaml
owner_rulings:
  - {ruling_id: "audio-poc-addendum-2026-09-12", banked_at: "2026-09-12T~12:00Z"}
release_gate_verdicts_current:
  kdpa_verdict: "PENDING"                                # Ruling #5 sub-verdict pending
  named_persons_verdict: "PENDING"                       # Ruling #5 sub-verdict pending
  transfer_basis: "PENDING"                              # §48/§51 to be determined
  licence_class: "owner_full_rights"                     # Ruling #2 (2026-09-12) — clears copyright layer
```

## B.3 · Job build waves — W2 · W3

**These are the AUDIO-JOB waves, not platform waves.** They EXECUTE the mounted job on the platform primitives Part A delivered.

### W2 · Mount + run vertical slice ONE station (L-class · JOB)

**Prerequisites (external):**
- W0 platform wave closed.
- W1 platform wave closed.
- NAS network path opened.
- HF token in `backend/.env`.
- `requirements.txt` deps added.
- Owner-ratified 3-station selection with Kamba MMS-fallback path.
- Owner ruling on RetentionPolicy for `corpus-deliverable-audio-segment-bytes` (see §C.2).

**Scope (L-class):**

- CP2.1 · Mount the JobManifest v1 (single station: Inooro FM).
- CP2.2 · Instantiate the eight capability_ids in the Capability Registry (register + availability_probe).
- CP2.3 · NAS reachability preflight + Source-Plane's `SynologyFileStationConnector.list()` + composition census (per-file inventory).
- CP2.4 · Stage ONE 30-min file to `akki-vm` via `connector.stream()` under the read-only guard.
- CP2.5 · Fire the capability pipeline (parallel per §1.7 attribute-stream design). L5 supervisor watches OUTPUTS.
- CP2.6 · Compose `AudioAttributeStreamBundle_v0`. Fire gate composition. Emit MOAC scorecard.
- CP2.7 · L6 milestone ratification — first live-runtime L6 use.
- CP2.8 · Wave close.

### W3 · Scale to 3 stations (M-class · JOB)

Replicate W2 on Inooro + Ramogi + Musyi with hybrid-ASR routing.

### Later job waves

- W4 · Scale to 16 stations.
- W5 · Character Register wave (§5-§7 invention layer).
- W6 · DAP sale surface (R-6/R-7 bindings).
- W7 · WPW Tier-2 draft-on-settle emitter.
- W8 · Release-gate ADMISSIBLE lift (Ruling #5 verdicts).
- W9 · Owner-ruling A/B/C for audio-bytes-retention (see §C).

**Every one of these is DATA on top of the platform — no case-specific PLATFORM code changes.**

---

# PART C · STORAGE / PURGE VERIFICATION AT PLATFORM LEVEL

## C.1 · The platform's Governance Plane supports the retain-exception BY CONSTRUCTION

The reframe unlocks a cleaner answer than the prior single-job framing. **The platform's `RetentionPolicy` primitive (A.10) has FOUR distinct regimes**, and each Artifact class binds to exactly one. This is not an ad-hoc exception — it is the plane's shape.

**Verbatim spec anchors, verified this session:**

**Audio Plane §6.1 · §6.2 · §6.3 — "Register Custody Boundary"** (scoped to the CHARACTER REGISTER):
> *"Only learned characteristics may be registered."*
> *"Stored as description, not exemplar. Centroids, distributions, frequencies. **Never stored audio; never per-utterance speaker embeddings.** Embeddings used during clustering are destroyed after cluster assignment. Provenance points to material, not to speaker identity."*
> *"**The register write path** exposes no field through which an instance-level representation can be stored: the schema cannot represent a voiceprint. Unrepresentable, not policed (§1.5)."*

→ Binds artifact_class `character-register-entry` to regime `REGISTER_DESCRIPTIVE` (§A.10 primitive #7).

**`PerceptionResult_v0.PurgeAttestation` (`contracts/perception_result_v0.py:54`):**
> *"purged: bool ... **'True iff worker-side raw AV was purged.'**"*

→ Binds artifact_class `worker-scratch-audio` to regime `WORKER_SCRATCH_PURGED`.

**`a1_demux.py` docstring:**
> *"Source objects are never modified or deleted; restructured audio is a derived artifact with lineage to the source object."*

→ Binds artifact_class `source-audio-file` to regime `SOURCE_UNTOUCHED`.

**Canon 4 `C4-022 §16` — S-A terminus:**
> *"S-A ends in a **FROZEN UNIT CONTRACT** — the deliverable's contents, licence label, privacy attestation, quality card, proof trail bound together and receipted."*

**Canon 4 `C4-057 §41` — contents attestation:**
> *"Every dataset/brief/feed carries a CONTENTS attestation — what the deliverable contains and what it does not. What it does NOT contain is stated as explicitly as what it does. Absence is a first-class fact."*

**Audio Plane §7.3 — sellable artifact:**
> *"The certificate is a first-class sellable artifact."*

→ These clauses **author a deliverable-plane** distinct from the register and the worker-scratch. The deliverable is content-agnostic; whether it carries audio bytes vs pointers vs transcripts is set by the RetentionPolicy binding for its artifact class, subject to the release gate.

**Audio Plane §1.2 anti-proliferation:**
> *"Anything in this document that reads as a parallel to an existing service is rule proliferation and must be collapsed into the existing service before build."*

→ The four retention regimes live under ONE `RetentionPolicy` service, not four sibling services.

**Platform-level answer to the storage/purge question:**

The **Governance Plane (A.10) SUPPORTS a governed "retain deliverable" exception distinct from the measurement plane's purge default BY CONSTRUCTION** — the four `regime` values on the `RetentionPolicy` primitive make this the natural expression. The spec authors the shape at §6 (register), `PurgeAttestation` (worker), `a1_demux` (source), and `C4-022 §16` (deliverable); the platform names each and binds Artifact classes to them.

**What §6.2 forbids:** audio bytes in the `character-register-entry` artifact class. **Nothing else.**
**What `PurgeAttestation` forbids:** audio bytes in the `worker-scratch-audio` artifact class. **Nothing else.**
**What the deliverable-plane clauses say:** the `corpus-deliverable-*` artifact class MAY carry ANY contents provided the contents-attestation is stated (`C4-057`) and the release gate ADMITS.

## C.2 · **This job — is retain-for-sale allowed / forbidden / needs ruling?**

**VERDICT for THIS job: NEEDS OWNER RULING before W2.**

**Reasoning:**

1. The platform's architecture SUPPORTS the retain-deliverable regime (C.1 established).
2. The specific ARTIFACT CLASS proposed for this job is `corpus-deliverable-audio-segment-bytes` — bytes of music-free non-English speech spans.
3. The spec does NOT preemptively bless nor preemptively forbid this specific artifact class. It authors the shape at §6 (forbidden in register), `PurgeAttestation` (forbidden in worker), `C4-022` (deliverable allowed with contents-attestation) — but the deliverable plane's specific instantiation for audio-segment bytes is **SILENT**.
4. Three sub-questions the owner must resolve:
   - **`kdpa_verdict`** — KDPA §44 sensitive-personal-data status for voice biometrics. Options: `ADMISSIBLE_CONSENT` (per-broadcast consent obtained), `ADMISSIBLE_LEGITIMATE_INTEREST`, `ADMISSIBLE_DPIA_APPROVED`, or `REFUSED`.
   - **`named_persons_verdict`** — Constitution §31 + Children Act 2022 §54 + Judiciary Recording Rules. Options: `DE_IDENTIFIED_PASS`, `REDACTED_PASS`, or `REFUSED`.
   - **`transfer_basis`** — KDPA §48 cross-border. Options: `SCC`, `ADEQUACY`, `RESEARCH_CARVE_OUT_51`, `CONSENT`, or `REFUSED`.

Ruling #2 (2026-09-12) already CLEARED the copyright layer (`licence_class = owner_full_rights`). The three verdicts above are the remaining chokepoints.

### Three concrete paths (unchanged from prior roadmap, now framed as owner-choose)

**Path A · GOVERNED AUDIO-BYTES RETENTION** — audio_class `corpus-deliverable-audio-segment-bytes` binds to `regime=DELIVERABLE_GOVERNED` with a new `licence_class_extension=owner_full_rights_speech_corpus`. Release gate refuses tiers `{audio_speech_no_speaker, audio_speech_with_speaker, biometric_embedding, named_identity}` by default; Ruling #5 verdicts lift. **Highest lab fidelity; highest governance surface.**

**Path B · POINTER-ONLY DELIVERABLE** — corpus is `{source-file-pointer, segment_offsets_ms, transcript}` triples. Audio bytes stay on the source estate. `regime=SOURCE_UNTOUCHED` for audio, `regime=DELIVERABLE_GOVERNED` for the manifest. **Safest; risks lab-value collapse if lab needs offline audio.**

**Path C · DEFER** — W2/W3 build with `pointer_or_bytes` schema; audio-bytes retention lands in W9 after Ruling #5 arrives. Corpus is transcript-only through W3.

**Default if no ruling by W2 CP0: Path C.**

## C.3 · Platform primitive NEW under W1: the `RetentionPolicy` module

`services/governance_plane/retention_policy.py` (new, W1) — enforces artifact-class ↔ regime binding by construction. Any Artifact instance carries a `retention_policy_ref` field pointing to its bound RetentionPolicy; write-to-storage refuses if the artifact's actual bytes violate the regime (e.g. an artifact of class `character-register-entry` refuses to accept an audio-bytes payload). **This IS the §1.5 unrepresentable pattern extended to the deliverable plane.**

---

# PART D · CORRECTIONS + VERIFICATIONS FROM THE OWNER'S REFRAME MESSAGE

For clarity, everywhere I disagreed with, modified, or clarified the reframe:

1. **Owner's list of "any host (GPU/CPU) registers by capability".** Verified alignment with `PerceptionJob_v0.modality ∈ {AUDIO, VIDEO}` + V1-I1 comment *"TEXT never routes to GPU (V1-I1)"*. The platform's resource-class enum extends the modality logic upward. ✅
2. **Owner's "readonly_media_guard" language.** Under the reframe this is a specific `SynologyFileStationConnector.read_only_guard`, not a sibling service. §A.2 records this correction.
3. **Owner's "release gate" as generic primitive.** Verified alignment with §A.10 `ReleaseGateVerdicts` — the four-verdict shape (kdpa + named_persons + transfer_basis + licence_class) is derivable from banked Ruling #5 + §V governance-chokepoint list. ✅
4. **Owner's "retain deliverable" governed exception.** Verified as one of four RetentionPolicy regimes. §C.1 establishes the platform supports it by construction; §C.2 says THIS job's binding requires an owner ruling. ✅
5. **Owner's premise "Everything case-specific lives HERE as config/data, not in Part A code".** Verified against §1.2 anti-proliferation. The JobManifest schema in §A.11 is the mounting surface; every case-specific field lives on the JobManifest instance, not in platform code. ✅
6. **Musyi/Kamba correction retained.** Not related to reframe; recorded in Part B `target_outcome.acceptance[kamba-kam]` as `evidence_class: projected`. ✅
7. **My prior "W-AUDIO-POC-3-STATIONS" naming** is now retired — the reframe replaces it with the job-manifest identity `audio-census-rms-16-stations-non-english-music-free-v1`. Waves W0/W1 are platform (no case-name); W2/W3 are mount-and-run of this specific manifest. ✅

---

# PART E · SEQUENCING UNDER THE REFRAME

## E.1 · NAS-free platform work (can start today)

| Item | Wave | Blocks |
|---|---|---|
| W0 integrity fix (Parts A.6 · A.10) | W0 · PLATFORM | Nothing external |
| W1 work-supervisor + resource-registry + capability-registry generalisation + governance-plane primitives (Parts A.1 · A.3 · A.8 · A.10) | W1 · PLATFORM | Nothing external |
| STANDING_ORDERS appends ("alive != done", "no run without progress signal") | W0 + W1 | Owner ratifies STANDING ORDER wording |
| TargetOutcome frozen contract (A.5) | W1 | Nothing external |
| CommissionSpec + Milestone + WorkerLane + WorkerJD contracts (A.7) | W1 | Nothing external |
| ReleaseGateVerdicts + RetentionPolicy primitives (A.10) | W1 | Nothing external |
| Source-Plane connector interface + Synology + S3 implementations (A.2) | W1 | Nothing external for interface; NAS reachability blocks the runtime probe |
| Capability Registry generalisation (A.3) | W1 | Nothing external |
| AudioAttributeStreamBundle_v0 contract (Part B artifact class) | W1 | Nothing external |
| Model + dep install on GPU hosts (owner-authorised) | W1-adjacent | HF token; owner authorisation |
| Dry-run on fixture audio (`fixture_a_silence.wav`, `fixture_b_tone.wav`) | W1 close proof | Nothing external — proves platform plumbing without real content |

## E.2 · BLOCKED-ON-OWNER / EXTERNAL

| Item | Wave | Blocker |
|---|---|---|
| Mount the audio-census JobManifest | W2 CP1 | Owner ratifies manifest |
| NAS reachability | W2 CP3 | Sysadmin bastion / VPN |
| Real audio stage | W2 CP4 | NAS reach + NAS credential landing |
| 3-station selection ratification | W2 CP1 | Owner |
| RetentionPolicy binding for `corpus-deliverable-audio-segment-bytes` | W2 CP1 | Owner ruling (Path A / B / C) |
| Release-gate verdicts lift | W8 (post-POC) | Ruling #5 sub-verdicts |
| DAP R-6 pricing + R-7 disclosure budget | W6 | Owner rulings |
| Watch-for-audio | W-Watch-Foundation (Track-B) | Separate charter |

---

# PART F · ATTESTATION

- **No product code touched.** No `services/**/*.py` edited or created. No pytest invoked. No testing_agent invoked. Ratchet floor **3251** untouched.
- **No push.** Local commit only, on workspace `master` (this document supersedes the prior `AUDIO_PROGRAMME_ROADMAP.md` which is deleted in the same commit).
- **Retracted ChatGPT integration** — no OpenAI/ChatGPT reference anywhere in this document.
- **POC/build HOLD in force** — no job manifest is mounted; no capability is registered; no wave has opened.
- **Every technical claim in this document was verified against a file opened in this session or a prior session's banked note.** Spec §-anchors verbatim.
- **Platform-vs-job separation held.** Part A carries zero case-specific values. Part B is a `JobManifest` yaml instance on top of Part A.
- **Storage/purge answered at PLATFORM level** (§C.1: supports by construction via four-regime `RetentionPolicy`) **AND at this-job level** (§C.2: NEEDS OWNER RULING for `corpus-deliverable-audio-segment-bytes` regime binding, three sub-verdicts open).
- **Standing orders proposed for W0 and W1.** Awaiting owner ratification of wording before authoring into `STANDING_ORDERS.md`.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
