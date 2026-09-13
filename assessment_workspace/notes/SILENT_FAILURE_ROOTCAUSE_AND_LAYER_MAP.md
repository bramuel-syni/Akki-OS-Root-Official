# Silent-Success Root Cause + Real-vs-Stub Layer Map (read-only)

**Task class:** DIAGNOSTIC · read-only · no build, no code commits, no push, ratchet 3251 untouched. **POC HOLD stays.**
**Directive received:** 2026-09-12T~13:50Z (owner).
**Executor:** track-a agent, re-grounded from `STATE/STANDING_ORDERS.md`, `STATE/DECISIONS.md`, `STATE/NEXT.md`.
**Retracted ChatGPT integration:** ignored (no OpenAI/ChatGPT reference in this document).

**Ground state:** ratchet floor **3251**; workspace `master` HEAD `760fe6c8` (prior spec deep extract); `programme/track-a` HEAD `77834d1`.

---

## Preface · a correction owed to the owner

The owner's diagnostic prompt says *"plan claimed 77 GPU campaigns running; both H200 hosts showed 0% for 14 days"*. Two clarifications before diagnosis, so the record is precise not defensive:

- **The "77 campaign runs" phrase is authored by the owner's 2026-09-08T~06:15Z directive** — banked verbatim in `notes/W_REGISTRY_FULL_BUILD_grounding_brief.md §C.3` + `§D.1` + `notes/MASTER_TRACEABILITY_AUDIT_20260909_UPDATE.md:140`: *"77 campaign runs visible in models roster"* — this refers to **surfacing sealed campaign records in the `/api/model_registry/models` roster PAYLOAD**, not to 77 currently-running GPU processes.
- **The prior "77 campaigns running" language was ALREADY retired.** `notes/W_MTAFITI_GPU_DISCOVERY_grounding_brief.md:290` records: *"The STATE-file narrative and probed reality diverged. Reconciled in `HOLISTIC_PLAN.md §5` this same session — the '77 campaigns running' language is retired."* — the earlier fork already caught the language and corrected it.
- **In `notes/AUDIO_AUTONOMOUS_JOURNEY_CAPABILITY_ASSESSMENT.md §F7.4` this session I wrote *"77 campaign runs visible in models roster"*** as accurate paraphrase of the roster-payload directive. Reading it in a plain-language pass, it can misread as "77 concurrent GPU campaigns" — that reading is wrong and I should have anticipated it. **The accurate number verified this session by live SSH: 21 real ACTIVITY_SUMMARY.md seals on `akki-vm` + 56 on `akki-vm-ii` = 77 sealed HISTORICAL runs across the two hosts; 0 currently running.** That 77 IS the owner's target enumeration surface, but it is NOT a runtime claim.
- **The "14 days" figure** — the last real trainer seal on either host is **2026-09-09 02:13Z (`akki-vm`) · 2026-09-08 23:55Z (`akki-vm-ii`)**. **Idle window is 3 days 10 hours as of this diagnostic (2026-09-12T12:15Z), not 14 days**, though the qualitative point stands: GPUs at $0-marginal Cassava lease have sat at 0% while `dispatcher_heartbeat.json` files remained fresh.

**The owner's diagnostic hypothesis stands.** The silent-success pattern is real and structural. What follows is the honest anatomy.

---

# PART 1 · ROOT CAUSE OF SILENT-SUCCESS

## 1.1 · The signal ledger — what the orchestration actually verifies

Every check, verbatim from `programme/track-a` HEAD `77834d1`:

### 1.1.a · `orchestrator_resilience/heartbeat.py` — pod-side heartbeat (line 91)

```python
def orchestrator_is_live(run_id: str, max_staleness_s: int = 600) -> bool:
    """Freshness check: return True iff a heartbeat exists AND its
    `at_utc` is within `max_staleness_s` seconds of now."""
```

**Field set of the heartbeat record** (line 62-69 verbatim):
```python
rec = {
    "run_id": run_id,
    "orchestrator_pid": int(orchestrator_pid),
    "at_utc": _iso_now(),
    "cycle_count": int(cycle_count),
    "on_host_status": dict(on_host_status),
    "next_poll_planned_utc": next_poll_planned_utc,
}
```
**No field for output progress. No `outputs_produced`, no `bytes_written`, no `checkpoint_step_delta`, no `gpu_utilization_pct`, no `loss_delta`, no `last_output_sha`.** The heartbeat is a *"point-in-time liveness record"* (docstring line 1) — it verifies the orchestrator's own pulse, nothing about what the orchestrator is orchestrating.

### 1.1.b · `orchestrator_resilience/watchdog.py::is_orchestrator_dead()` — pod-side death detector (line 53)

```python
def is_orchestrator_dead(run_id: str, max_staleness_s: int = 600) -> Tuple[bool, str]:
    """Death reasons (in order of check):
        no_heartbeat       — no heartbeat file exists
        stale_heartbeat    — heartbeat older than max_staleness_s
        pid_dead           — heartbeat's orchestrator_pid is not alive
    A heartbeat that is fresh AND whose pid is alive returns (False, "live")."""
```

**Three death signals: (a) no heartbeat file, (b) old timestamp, (c) dead PID.** All three are pure process-liveness. **The orchestrator can be "live" — fresh heartbeat + alive PID — while producing zero outputs.**

### 1.1.c · `orchestrator_resilience/orphan_detector.py::_looks_in_flight()` (line 52)

```python
def _looks_in_flight(run_dir: Path) -> bool:
    """A run dir looks in-flight if it has at least one launch record
    (`*_launch_burn.json` OR `*_launch_train.json`) AND at least one
    poll receipt (`*_nvidia_smi_poll_*s.json`)."""
```

**"Poll receipt" = an `nvidia-smi` output JSON.** A file recording `util=0, mem_used=0` still IS a poll receipt. The `_looks_in_flight` check does NOT open the file and does NOT read the util%. **A run that has never done any work — dispatcher polling nvidia-smi and dumping 0-values every 60s — passes as "in-flight" indefinitely.**

### 1.1.d · `orchestrator_resilience/adopt.py::can_adopt()` — orphan-adoption predicate (line 66)

```python
def can_adopt(orphan, max_poll_age_s: int = 900) -> Tuple[bool, str]:
    """(True, 'recent_poll_within_<n>s') if adoptable"""
```
Reasons for refusal (verbatim lines 83-95): `run_dir_missing` · `sealed` · `no_launch_record` · `no_polls` · `polls_stale_<n>s_gt_<threshold>`. **All five are FILE-EXISTENCE / TIMESTAMP checks. None read the poll receipts' util%. None verify progress.**

### 1.1.e · `campaign_infra/reconcile.py::adoptability_of_campaign_run()` (line 88)

Verdict field set (verbatim lines 105-112):
```python
verdict = {
    "run_id": run_id,
    "adoptable": False,
    "reason": "",
    "heartbeat_utc": None,
    "training_pid": None,
    "pid_alive": False,
}
```

Four verdict values (`still_running` · `restart_from_checkpoint` · `sealed` · `never_started`) — verbatim docstring lines 8-13. **The `sealed` verdict is based ENTIRELY on `_is_sealed()` (line 60):**

```python
def _is_sealed(run_dir: Path) -> bool:
    """Case-insensitive existence check for ACTIVITY_SUMMARY.md."""
    for entry in run_dir.iterdir():
        if entry.is_file() and entry.name.lower() == "activity_summary.md":
            return True
    return False
```

**Sealed = a markdown file exists with case-insensitive name `activity_summary.md`. Its contents are never read. Its length is never checked. Its `Kind:` field is never parsed.**

### 1.1.f · `campaign_infra/run_queue.py::execute_campaign()` (line 70)

The `trainer_fn` is **INJECTED** (docstring line 8-12):

> *"`trainer_fn` is a callable INJECTED by the caller (not a fixed dependency). This lets the invariant harness pass a fake trainer without touching real training code. In production, the caller wires a real trainer that respects checkpoint markers + on-host logging."*

The advance-to-next-run gate (line 120-136):
```python
trainer_fn(run_name=run_name, manifest_entry=run, host=host)
if not _is_run_sealed(campaign_id, run_name):
    # Trainer completed but did not seal. Write synthetic unfinished marker and refuse to advance.
    _hlog.write_run_summary(
        run_id=..., final_step=-1, final_loss=None,
        started_at_utc="unknown", completed_at_utc="unfinished",
    )
    raise CampaignPriorRunNotSealed(...)
```

**When the trainer returns without sealing, run_queue writes ITS OWN `ACTIVITY_SUMMARY.md` with `final_step=-1, final_loss=None, completed_at_utc="unfinished"`** — and then raises. But the ACTIVITY_SUMMARY.md file EXISTS. If a downstream consumer (models roster, reconciler) counts files, it counts this "unfinished" marker as sealed.

### 1.1.g · `tools/on_host_queue_dispatcher.py::_write_synthetic_dead_trainer_seal()` — the synthetic-seal escape (line 141)

**This is the smoking gun of the silent-success anatomy** (verbatim lines 99-116):

> *"When a dispatcher has just dispatched a trainer, the trainer PID must remain alive OR the trainer's own ACTIVITY_SUMMARY.md must appear. If neither is true for DEAD_TRAINER_POLL_THRESHOLD consecutive poll cycles, the dispatcher writes a synthetic 'kind=synthetic_dead_trainer_seal' seal at ~/akki_journal/<run_id>/ACTIVITY_SUMMARY.md and advances."*
> *"Rationale: crash-at-step-0 failures (CUDA OOM · disk-full checkpoint save · tokenizer download failure) can leave the trainer PID dead without ever writing a seal. The pre-fix dispatcher spun forever in `_wait_for_activity_summary`, leaving akki-vm idle for 16 hours on 2026-09-06 → 2026-09-07 across two lanes (~32 GPU-hours lost)."*

The synthetic seal body (verbatim lines 153-172):

```
# ACTIVITY SUMMARY · SYNTHETIC DEAD-TRAINER SEAL

**Kind:** synthetic_dead_trainer_seal
**Provenance:** programme.dispatcher_liveness_check
...
The trainer PID died without writing its own ACTIVITY_SUMMARY.md. Dispatcher observed the death for
{DEAD_TRAINER_POLL_THRESHOLD} consecutive polls and authored this synthetic seal so the queue can advance.
DO NOT bank this record into any baseline_record — the training run did not complete.
```

**The synthetic seal itself carries "DO NOT bank this record into any baseline_record — the training run did not complete."** — an explicit warning IN THE FILE.

**Grep this session for downstream code that filters synthetic seals:** `grep -rniE "(synthetic_dead_trainer_seal|Kind.*synthetic|kind == .synthetic|ignore.*synthetic)" backend tools` returned **six matches: five inside the writer itself + the invariant that verifies the writer fires. ZERO downstream consumers filter it out.** `_is_sealed()`, `_is_run_sealed()`, `_has_sealing_marker()`, `adoptability_of_campaign_run()`, and any roster payload aggregator ALL treat this file identically to a real trainer-authored seal.

### 1.1.h · `tools/on_host_watchdog.sh` — on-host cron watchdog (line 87)

The core check:
```bash
if kill -0 "${pid}" 2>/dev/null; then
    echo "on_host_watchdog: pid ${pid} alive for ${run_dir} · healthy · continue (no interference)"
    continue
fi
```

**Live-PID = "healthy · continue".** No progress check. No step-delta check. No loss-delta check. No GPU-util check. `kill -0` returns 0 for a process that has spent 16 hours doing nothing — and the watchdog logs "healthy".

## 1.2 · The full grep, negative-result findings

`grep -rniE "(gpu_util|utilization|progress_check|output_artifact|step_delta|loss_desc|starvation|idle_alarm|verify_progress|bytes_written)" backend/services/orchestrator_resilience backend/services/campaign_infra tools`

**Result: ZERO matches.**

There is **no code anywhere in the pod-side orchestration or the on-host dispatcher stack** that verifies:
- GPU utilization > 0 over any window.
- Poll receipt N+1 differs from poll receipt N (progress signal).
- Adapter weight file exists at wave close.
- Loss decreased between checkpoints.
- Queue emptiness raises an alarm (starvation signal).
- Time-since-last-real-seal exceeds an SLA (starvation signal).

## 1.3 · How a "campaigns running" claim can be emitted while GPUs sit idle — the exact chain

Reconstructed step by step from opened code:

1. **`campaign_infra.run_queue.execute_campaign`** is invoked with a manifest of N runs.
2. It iterates runs, calling `trainer_fn(run_name, manifest_entry, host)`. In production this is `production_trainer.default_trainer_fn` — which does real work (see §2.1 below).
3. `default_trainer_fn` (line 366-374) fires the trainer SSH command detached (`setsid nohup`) and returns immediately with a `run_receipt` handle. **It does NOT wait for the trainer to complete.**
4. `run_queue` then blocks on `_is_run_sealed(campaign_id, run_name)` — which is *"case-insensitive existence check for ACTIVITY_SUMMARY.md"* — poll-loop for the seal.
5. On-host, `on_host_queue_dispatcher.py::_wait_for_activity_summary()` also polls for the same file. If trainer_pid dies without a seal, it authors `synthetic_dead_trainer_seal` after `DEAD_TRAINER_POLL_THRESHOLD=3` polls (~3 min at 60s poll interval).
6. When the file appears — REAL or SYNTHETIC — `run_queue` advances to the next run. Every downstream aggregator (models roster, reconciler, adopt) reads the file's EXISTENCE, never its `Kind:` field.
7. **A campaign is `queue_completed.md`-marked when every run's directory has a `.md` seal.** A follow-on manifest chain (`--follow-on-queue-file` per `W-WINDOW-FILL-GUARANTEE 2026-09-06T~19:40Z`) launches the next dispatcher immediately after `queue_completed.md` lands.
8. **Follow-on chain drains, no new manifest exists → GPUs idle. Dispatchers stay alive (their heartbeat.json refresh loop runs).** From every liveness check's point of view the system is healthy: dispatchers heartbeating, watchdog reporting `pid alive · healthy · continue`. **From work's point of view, nothing has happened.**

## 1.4 · The exact gap that lets liveness-without-progress read as success

**One-line diagnosis:** the orchestration stack conflates **process liveness** with **work progress**, and the seal predicate `_is_sealed()` conflates **file existence** with **task completion**.

**Six specific code sites where the conflation lands** (all verbatim):

| # | File · line | Predicate | What it verifies | What it should also verify |
|---:|---|---|---|---|
| 1 | `heartbeat.py:91` | `orchestrator_is_live()` | `at_utc` freshness | progress delta (cycle_count-N > cycle_count-N-1 doesn't imply work) |
| 2 | `watchdog.py:32-50` | `pid_is_alive()` | POSIX signal-0 | GPU util > 0 over window |
| 3 | `orphan_detector.py:52` | `_looks_in_flight()` | launch + poll receipt files exist | poll receipt utilization > 0 |
| 4 | `reconcile.py:60` | `_is_sealed()` | activity_summary.md exists | `Kind:` field != synthetic_dead_trainer_seal |
| 5 | `run_queue.py:48` | `_is_run_sealed()` | activity_summary.md exists | same |
| 6 | `on_host_watchdog.sh:87` | `kill -0` | POSIX signal-0 | trainer log growing / step counter advancing / adapter file size increasing |

**Zero of the six read a byte of actual output.** Every one is a metadata / filesystem existence check.

## 1.5 · The specific instance the owner saw

Verified this session by live SSH probe 2026-09-12T~12:14Z (before this doc opened):

| Host | Dispatcher heartbeat | Card 0 util | Card 1 util | Last real seal | Idle for |
|---|---|---:|---:|---|---|
| `akki-vm` | fresh (dispatcher_pid alive, polling every 60s) | **0% / 0 MiB** | **0% / 0 MiB** | 2026-09-09 02:13Z (`shield-train-campaign-a-v21-A-3-7B-s5`) | **3d 10h** |
| `akki-vm-ii` | fresh (dispatcher_pid alive, polling every 60s) | **0% / 0 MiB** | **0% / 0 MiB** | 2026-09-08 23:55Z (`shield-train-campaign-b-v21-B-REF-3B-s7`) | **3d 12h** |

**77 sealed run dirs total** (21 on `akki-vm`, 56 on `akki-vm-ii`) — **0 synthetic-dead-trainer seals** across both hosts (grep verified). So the historical work WAS real trainer-authored. But since the follow-on chain drained on ~09-09, both dispatchers have been performing the ceremony of aliveness without a queue. Nothing in the stack raises an alarm on this.

**This IS the owner's silent-success pattern in its milder form.** The severe form is what would happen if a stub `trainer_fn` were injected (invariant-harness path) or if the crash-at-step-0 mode fires — in both cases a well-formed ACTIVITY_SUMMARY.md exists WITHOUT real work, and every downstream aggregator counts it as done.

---

# PART 2 · REAL vs STUB INVENTORY

Every audio + orchestration component classified by evidence from files opened this session.

## 2.1 · Orchestration (pod-side + on-host)

| Component | Class | Evidence |
|---|---|---|
| `campaign_infra/run_queue.py` — `execute_campaign` | **REAL orchestration wrapper** (trainer_fn INJECTED · invariant tests pass fake trainer, production wires real trainer) | line 8-12 docstring; line 73 `trainer_fn: Callable[..., Any]` parameter |
| `campaign_infra/production_trainer.py` — `default_trainer_fn` | **REAL production binding** (loads AWS creds from `/app/backend/estate_keys/data_sources/`, builds Aurora Data API executor, SSH-detach launches `on_host_trainer.py` on remote host) | line 266-374; lines 45-66 credential loader; lines 340-365 ssh_seam launch |
| `campaign_infra/manifest.py` | **REAL schema validator** | 107 lines · `validate_manifest()` enforces v0 shape |
| `campaign_infra/on_host_logging.py` — heartbeat/poll/summary writers | **REAL disk-writer primitives** | 144 lines, three writer functions with fsync semantics |
| `campaign_infra/checkpoint.py` | **HALF-REAL** — marker writer real, actual `.pt` tensor writer NOT IN THIS WAVE | line 12-14 docstring: *"Actual .pt tensor persistence is NOT in this wave (training-loop wave chartered separately)"* |
| `orchestrator_resilience/heartbeat.py` | **REAL liveness primitive** — but by design metadata-only | 135 lines; docstring line 10: *"observer, never a run participant"* |
| `orchestrator_resilience/watchdog.py::pid_is_alive` | **REAL** POSIX signal-0 check | line 32-50 |
| `orchestrator_resilience/orphan_detector.py::find_orphaned_runs` | **REAL** filesystem walker | line 64-107 |
| `orchestrator_resilience/adopt.py::can_adopt` | **REAL** predicate | line 66-95 |
| `orchestrator_resilience/adopt.py::mark_adopted` | **REAL** adoption ledger writer | line 115-148 |
| `orchestrator_resilience/resume.py::resume_from_receipts` | **REAL** — reads existing poll receipts to compute resume cursor | line 56-91; **but reads only filename `elapsed_s` — not the receipt's content** |
| `tools/on_host_queue_dispatcher.py` — dispatcher loop | **REAL** — launches real subprocesses; writes real heartbeats | 501 lines |
| `tools/on_host_queue_dispatcher.py::_write_synthetic_dead_trainer_seal` | **REAL WRITER of a HONEST-EMPTY placeholder** — writes `Kind: synthetic_dead_trainer_seal` .md carrying explicit "DO NOT bank" warning | line 141-183; but see §1.1.g gap |
| `tools/on_host_watchdog.sh` — cron restart-from-checkpoint | **REAL** — restarts dead trainers detached, writes `watchdog_restart_<utc>.json` ledger | 148 lines |
| `tools/queue_followon_launcher.py` — chained-dispatch launcher | **REAL** — respawns dispatchers on drained queues + dead PIDs | 395 lines; owner ruling 2026-09-08T~04:50Z item 4 (banked in DECISIONS) |
| `tools/on_host_trainer.py` — the actual LoRA fine-tuner | **REAL** — HuggingFace `AutoTokenizer.from_pretrained(trust_remote_code=True)` + `AutoModelForCausalLM.from_pretrained(torch_dtype=bf16)` + `LoraConfig` + `Trainer` + `resume_from_checkpoint` + adapter-sha256 walk | 20,939 bytes; docstring lines 1-40 name the exact HF classes used |

**On-host trainer verdict: REAL production training code.** The 77 sealed runs on the two hosts are 77 real HF LoRA runs against `Qwen/Qwen2.5-0.5B/1.5B/3B/7B` bases on `digicow_live` corpora.

## 2.2 · Audio pipeline (perception + layer_b)

| Component | Class | Evidence |
|---|---|---|
| `contracts/audio_segment_v0.py` | **REAL frozen wire contract** (Pydantic BaseModel, min_length=1 on both streams, extra=forbid, frozen=True) | 83 lines; parity map bump 66→67 |
| `contracts/perception_job_v0.py` | **REAL frozen contract #27** | 77 lines |
| `contracts/perception_result_v0.py` | **REAL frozen contract #28** with `purge_attestation` REQUIRED-not-optional | 79 lines |
| `contracts/signal_ring.py` | **REAL** v0 catalogue (6 audio dims) + validator | 68 lines |
| `contracts/extraction_params.py` | **REAL** v0 catalogue + validator + `is_deterministically_reproducible()` gate | 307 lines |
| `services/perception/eab_1_pipeline/a1_demux.py` | **WIRE-CONTRACT REAL · BACKEND ADAPTER MISSING** — 83 lines of deterministic envelope math; docstring lines 11-15: *"Real-world backend adapter is ffmpeg ... Backend adapter lives at `backend/services/perception/eab_1_pipeline/backends/` at deployment (NOT this atomic; the wire contract is what deploys)."* **`backends/` folder ABSENT on `programme/track-a` HEAD.** |
| `services/perception/eab_1_pipeline/a1_segmentation.py` | **REAL** deterministic segmenter (content-addressed batch_id) | 124 lines |
| `services/perception/eab_1_pipeline/a1_vad.py` | **WIRE-CONTRACT REAL · BACKEND ADAPTER MISSING** — Silero VAD wrapper docstring: *"consumer of the model registry pin"*; no real Silero inference call in this file | 141 lines |
| `services/perception/eab_1_pipeline/a1_dedup.py` | **REAL** (in-process content-address dedup using sha256) | 130 lines |
| `services/perception/eab_1_pipeline/a2_occurrence_writer.py` | **REAL emitter · with HARD-CODED `"language_hint":"en"`** at line 76 | 162 lines |
| `services/perception/eab_1_pipeline/a2_license_class.py` | **REAL** (three-class enum with fail-closed default) | 53 lines |
| `services/perception/eab_1_pipeline/a2_trace_walker.py` | **REAL** single-code-path resolver (FENCE 1) | 87 lines |
| `services/layer_b/asr/whisper_provider.py` (cloud) | **PLUMBING-STUB by construction** — routes through `services/synisense/shield/perception_router.py` which HAS A HONEST STUB PATH (line 86 · line 95 return `{synthetic_plumbing_only: True}`). Line 55 pass-through: `synthetic_plumbing_only=result.get("synthetic_plumbing_only", False)` — flag propagates. | 56 lines |
| `services/layer_b/asr/faster_whisper_provider.py` (local) | **REAL when `faster-whisper==1.2.1` importable AND model downloads succeed** — docstring lines 15-20: *"Until real Hour A arrives, the provider runs against the synthetic TTS audio with `synthetic_plumbing_only=True` set on the result"* — **but line 89 hard-codes `synthetic_plumbing_only=False` in the provider return, with comment *"provider doesn't know; caller stamps"*** — CALLER-COOPERATION required to stamp the flag. If caller forgets, real-vs-synthetic distinction is lost. | 90 lines |
| `services/layer_b/diarization/pyannote_provider.py` | **UN-RUNNABLE** — `pyannote.audio` NOT in `backend/requirements.txt`; `HUGGINGFACE_HUB_TOKEN` not in `.env`. Construction raises `ProviderUnavailable`. | 80 lines |
| `services/layer_b/vision/frame_perception_provider.py` | **PLUMBING-STUB via perception_router** — line 50: `synthetic_plumbing_only=result.get("synthetic_plumbing_only", False)` | grep-only |
| `services/synisense/shield/perception_router.py` | **HAS A HONEST STUB PATH** — docstring line 18: *"fall back to a deterministic `synthetic_plumbing_only=True` stub"*; two return paths (line 86, 95) both stamp `synthetic_plumbing_only: True` | grep-only |
| `services/perception/gpu_execution/audio_batching.py` | **SEAM-ONLY** — 33 lines; docstring line 28: *"For 9.2a fixture-mode: single chunk pass-through — faster-whisper's internal chunking handles longer audio. This function is a seam for 9.2b GPU-mode batching."* | 33 lines · effectively identity function |
| `services/perception/gpu_execution/model_loader.py` | **CI-FIXTURE-TIER** — `_hf_model_name()` map has ONE entry: `{"whisper-tiny": "tiny"}` (line 40). Multilingual whisper (medium, large, v3) requires a seed. | 46 lines |
| `services/perception/gpu_execution/cuda_runtime.py` | **REAL env-driven selector** with fail-hard-if-unset (Owner 9.2a-E2 α condition 1) | 52 lines |
| `services/perception/models_registry.v0.json` | **CI-fixture only** — sole seeded model is `whisper-tiny` per Ruling 9.2a-E1 α + seed-with-CI-fixture correction 2026-07-10 | verified last session |

## 2.3 · The owner's hypothesis, answered

Owner asked: *"were prior 'successes' running the ACTUAL components or just the plumbing/thinking of them?"*

**Split verdict:**

- **Text-training half (shield_train + campaign_infra + on_host_trainer.py):** **RAN THE ACTUAL COMPONENTS.** 77 real HF LoRA seals across two hosts, dispatchers-and-watchdogs proven in a 2026-09-06T110345Z runtime drill (`phase0/drill_receipts/20260906T110345Z_wave_orch_resilience_r2_runtime_drill/DRILL_REPORT.md` — banked in prior wave close). The `on_host_trainer.py` is 20,939 bytes of real HF training code. The `production_trainer.default_trainer_fn` loads real AWS credentials, invokes real Aurora Data API, SSHs a real detached subprocess.
- **Audio-perception half (perception + layer_b):** **RAN THE PLUMBING/THINKING** — the wire contracts + atomics are real (deterministic envelope math, sha256 canonical-IDs, batch-id computation, VAD probe reducer, dedup index) BUT the four backend adapters that touch real audio (`backends/ffmpeg_demux.py`, `backends/silero_vad.py`, `pyannote.audio` diarizer, ≥`whisper-medium` multilingual ASR) are all **MISSING or NEVER INVOKED** on `programme/track-a`. The Silero VAD wrapper's `registry_pin_reference()` returns a metadata dict — it does not load or invoke Silero. The whisper providers succeed at construction but their `transcribe()` either (a) routes through `perception_router` which returns `{synthetic_plumbing_only: True}` stubs, or (b) requires a `faster-whisper` model download on first use — a path that has not been exercised end-to-end on a real off-air recording.
- **Silent-success amplifier for audio**: `synthetic_plumbing_only` is a HONESTY flag that **requires caller cooperation to stamp True** — and downstream aggregators (models roster, ledger writers, MOAC readers) have **no invariant filter** on records where `synthetic_plumbing_only=True`. If a synthetic-plumbing run is stamped as a "perception result", it lands in the ledger with the same status as a real one unless the caller marked it. Grep this session: NO ledger-writer / roster-consumer / registry-writer filters on `synthetic_plumbing_only`. It is a passive metadata field.

**Conclusion for the owner's question:** the prior "successes" that surfaced as HF LoRA trainer seals across the two H200 hosts are REAL. Any prior claim of "audio work completed" would have been PLUMBING — the audio backend adapters have not been exercised end-to-end. **The two halves need very different re-trust strategies.**

---

# PART 3 · OWNER'S 6-LAYER MODEL → REAL COMPONENTS + WHAT "MILESTONE MET" ACTUALLY MEANS

For each layer: the mapped real component, its file path, maturity (REAL / PARTIAL / ABSENT), and — critically — **what "milestone met" is backed by in code today**.

### Layer 1 · Shape Objective — Objective Wizard / Targeta / CIF (Audio Plane §8)

| Component | Path | State |
|---|---|---|
| `MtafitiObjectiveCarrier` frozen contract | `contracts/mtafiti_objective_carrier.py` (created CP1 of W-MTAFITI-GPU-DISCOVERY) | **REAL** — refuses mtafiti-internal origin by construction; three-value `ObjectiveOrigin ∈ {TARGETA, CIF, COACH_ORIGINATION_PORT}` |
| Objective Wizard schema-compiler (`services/objective_wizard/*`) | — | **ABSENT** on `programme/track-a` (grepped this session) |
| CIF admission port (`services/cif/*`) | — | **ABSENT** on `programme/track-a` |
| Targeta package (`services/targeta/*`) | present in tree | **PARTIAL** (existence not deeply verified this session) |

**"Milestone met" for Layer 1 means:** — nothing. There is no `objective_shaped` milestone predicate. The frozen carrier can be constructed; that is a contract-shape assertion, not a milestone attestation. **Verdict: no artifact backs "objective shaped" today.**

### Layer 2 · Quality Definition Parameters — Target Outcome / Quality Matrix (Audio Plane §10, §11)

| Component | Path | State |
|---|---|---|
| `TargetOutcome` frozen contract (`contracts/target_outcome_v0.py`) | — | **ABSENT** |
| Quality Matrix instrumentation | `services/perception/execution_mode_telemetry.py` (1,665 bytes) + `phase0/baseline_lines/` slot | **PARTIAL** — telemetry emitter exists; per-class quality-matrix composer does not |
| MOAC six-criterion scorecard writer (`services/moac/scorecard.py`) | — | **ABSENT** |
| `transformation_quality_spec_v1.md` (22,775 bytes at `docs/requirements/`) | landed | **spec landed, code un-built** |

**"Milestone met" for Layer 2 means:** — nothing artifact-backed. Rung-1 emissions land as `baseline_lines/*.json` but no composer aggregates them into a single-deliverable acceptance verdict. **Verdict: no artifact backs "quality bar met" today.**

### Layer 3 · Success Strategy + QC — Critic Seam / release_gate / held-out / MOAC

| Component | Path | State |
|---|---|---|
| Held-out slice preflight | `services/shield_train/held_out.py` (banked W-Shield-Train-BUILD 2026-09-06) | **REAL** — `deterministic_20pct_tail_split(rows, seed=31337)` + `bank_held_out_slice_hash(...)` writes `banked_before_first_run_starts=True` sha256 preflight |
| PII redaction guard | `services/mtafiti/detectors/{pii_detector.py, pii_redaction_guard.py}` (CP2 W-MTAFITI-GPU-DISCOVERY) | **REAL** — deterministic salted-sha256 + `assert_no_raw_pii(data_view(receipt))` defence-in-depth |
| Read-only SQL guard | `services/mtafiti/executor/readonly_sql_guard.py` (CP1) | **REAL** — 20+ statement classes refused |
| Read-only media guard | — | **ABSENT** (POC dependency) |
| Release gate | `services/shield_train/release_gate.py` | **ABSENT** (POC dependency) |
| Critic Seam | `services/critic_seam/*` — spec landed at `docs/requirements/critic_seam_spec_v1_1.md` | **ABSENT — spec exists, code un-built** (WS-HARVEST-CRITIC-SEAM + WS-WIRE-CRITIC-INTO-ANSWERING per BUILD_STRATEGY.md) |
| MOAC scorecard writer | — | **ABSENT** |
| Double-green byte-match discipline | `BASELINE_GUARD=1 pytest` invocations | **REAL** — 17+ consecutive closes held byte-match |
| AU-3 six-element ledger completeness invariant | — | **PARTIAL** — writers exist; single gating invariant across ledger family absent |

**"Milestone met" for Layer 3 means:** for held-out preflight + PII + read-only-SQL + double-green: **REAL invariant tests fire on every CP close**. For Critic Seam + release_gate + MOAC: **no artifact — those milestones cannot fire because the code does not exist**.

### Layer 4 · Job Commission + Worker TOR — Commission (§13) / campaign_infra

| Component | Path | State |
|---|---|---|
| Commission View (§13 surface) | — | **ABSENT** (§13.1 declares no modality-specific UI; §13.4 forbids new-backend-machinery for it; no `services/commission_view/*`) |
| Campaign manifest schema (v0) | `services/campaign_infra/manifest.py` (107 lines) | **REAL** — validates 6 required run fields (run_name, model_size_class, corpus_variant, seed, hyperparams, held_out_slice_spec) |
| Campaign run queue | `services/campaign_infra/run_queue.py` (144 lines) | **REAL** — fcntl-lock, sequential dispatch, sealed-file gate |
| Milestone contract (§11.3 "milestone list") | — | **ABSENT** — the closest thing is the `manifest.runs[].run_name` list, but that is not a milestone-with-done-condition-and-owner shape |
| Worker JD / KPIs / handoff protocols | — | **ABSENT** — the only worker-side contract is the CLI arg list to `on_host_trainer.py` |
| On-host trainer worker | `tools/on_host_trainer.py` (20,939 bytes) | **REAL** — HF LoRA trainer with resume-from-checkpoint |
| Handoff between S-A / S-B (§17) | `contracts/handoff_contract.py` (3,740 bytes) | **REAL frozen contract** (existence verified, deep semantics not opened this session) |

**"Milestone met" for Layer 4 means:** a `ACTIVITY_SUMMARY.md` file exists in the run's directory (case-insensitive). **§1.1.e above — nothing about the file's contents is checked.** The `final_step` field is the trainer's self-declared step count; the `final_loss` field is self-declared; the `completed_at_utc` is self-declared. **No downstream code verifies these against the training log. No downstream code verifies the adapter .pt file exists at the location `on_host_trainer.py` claims to have written it.**

### Layer 5 · Supervision from OUTSIDE — Watch (Doc 8) / orchestrator-resilience

| Component | Path | State |
|---|---|---|
| Watch bundle (Macho / Mkono / Witness / Marks / Drills) | — | **ABSENT for audio domain** — `services/watch/*` chartered as Track-B open per BUILD_STRATEGY.md · `W-Watch-Foundation` wave not yet started · Canon 8 §1-§40 defines 72 requirement rows all un-implemented for audio |
| Orchestrator resilience r1+r2 | `services/orchestrator_resilience/{heartbeat,orphan_detector,resume,adopt,watchdog}.py` | **REAL** — runtime-drilled 2026-09-06T110345Z |
| **Progress-monitoring watchdog** (owner's Layer 5) | — | **ABSENT** — grep confirmed zero code checks `gpu_util`, `progress`, `output_artifact`, `step_delta`, `loss_desc`, `starvation`, `idle_alarm`, `verify_progress`, `bytes_written` anywhere in orch/campaign_infra/tools |
| Objective-drift monitor | — | **ABSENT** — no Watch mark exists for "trainer output no longer matches the frozen `MtafitiObjectiveCarrier`" |
| Quality-reshape monitor | — | **ABSENT** — no cross-CP invariant fires when a subsequent CP relaxes a rung-1 threshold |
| Resource-distortion monitor | — | **ABSENT** — no alarm fires when `gpu_util=0` for > SLA (SLA also un-authored) |
| Watch → CIF/coach escalation | — | **ABSENT** — Watch not yet wired to CIF |

**"Milestone met" for Layer 5 means:** **NOTHING WATCHES OUTPUTS FROM OUTSIDE TODAY.** The orchestrator_resilience watchdog is a **process-supervisor**, not a **work-supervisor**. It restarts dead PIDs; it does not audit whether the restarted PID does any work. The Watch (Doc 8) is designed to sense at the Layer 5 abstraction — but for the audio domain it is not built. **This is the biggest missing surface in the stack. The owner's diagnostic is correct: there is no outside-observer that verifies OUTPUTS EXIST AND MATCH THE OBJECTIVE.**

### Layer 6 · Human-in-the-Loop Streaming Milestone Review — §13.2 + front-end

| Component | Path | State |
|---|---|---|
| §13.2 milestone-ratification surface | — | **ABSENT** — §13.2 verbatim requires *"at Sampling & Reflection, the proposed milestone list is presented to the objective owner for agreement. Commission does not open until it is agreed."* No such UI or API endpoint exists |
| Front-end streaming | — | **ABSENT** — no live-status stream; owner reads STATE files + probes hosts via SSH |
| Owner-facing plain-language wave-close (5-section) | `notes/W_MTAFITI_GPU_DISCOVERY_wave_close.md` shape | **REAL as a document convention** — closed CPs bank a 5-section wave-close markdown; owner reads it after the fact, not during |

**"Milestone met" for Layer 6 means:** **owner reads a markdown file after the wave closes.** There is no runtime stream. There is no milestone-ratification gate that blocks CP opening on owner acknowledgment. The commission-opens-only-on-agreement discipline of §13.2 is asserted in the spec but has no code enforcement.

---

# PART 4 · AUDIO DATA-MODEL LAYERING — one file → N attribute streams

The owner's mental model: one audio file explodes into multiple attribute streams (volume, pitch, tone, unique identifiers, ...). Spec Audio Plane §1.1 authors this exactly:

> **"Segments are rows; the extractable layers — content, language, condition, prosody, occurrence, code-switch, music, group-level character — are columns; no schema exists until one is declared."**

**Spec's 8 columns (§1.1) mapped to code artifacts on `programme/track-a`:**

| # | Column (§1.1) | Owner's approx term | Contract / Signal Ring dim | State |
|---:|---|---|---|---|
| 1 | **content** | content / transcript / text | `AsrPerception.cues[].text` (`layer_b/contracts.py:37`) | **REAL as scalar, run through provider** |
| 2 | **language** | language identifier | Spec §4.1 requires `languages[]` + `confidences[]` per segment; `AsrPerception.language_hint: Optional[str]` is **single-scalar-optional** | **PARTIAL — shape wrong for spec** |
| 3 | **condition** | channel / environment | `AudioSegmentV0.condition_profile: str` (opaque scalar, `min_length=1`) | **PARTIAL — field exists, no detector** |
| 4 | **prosody** | pitch, tone, intonation | `signal_ring@v0["audio"]` dims: `prosody, vocal_emphasis, affect_valence, affect_arousal, speech_rate, pause_density` (6 dims) | **REAL as taxonomy · extractor un-built** |
| 5 | **occurrence** | dedup pointer / repeat log | `services/perception/eab_1_pipeline/a2_occurrence_writer.py::Occurrence` (`{canonical_id, station, timestamp_ms, batch_lineage}` locator) | **REAL** |
| 6 | **code-switch** | multi-language markers | Spec §4.2 requires `{position, from-language, to-language, context class}` — **no contract carries these fields** | **ABSENT** |
| 7 | **music** | music/speech split | `a1_vad.py::VADSegment.content_type ∈ {speech, music, ad, silence, tone, unknown}` | **REAL as tag · music-vs-speech separation UN-BUILT** (no demucs, no source-separation) |
| 8 | **group-level character** | Character Register (§5) | `services/character_register/*` | **ABSENT** — biggest §5-§7 gap |

**Owner-specific attributes that the SPEC forbids storing per-individual** (§6.1 · organic characteristics = biometric = NEVER registered):
- Vocal tract length · formant structure · glottal source · fundamental frequency range.

**Owner-specific attributes that spec authors as capturable at GROUP level (§4.4):**
- Pitch statistics · energy contours · duration patterns. Contract for these: **UN-BUILT** (§4.4 acceptance criteria fail: no per-segment pitch/energy/duration extractor exists).

**Attributes the owner might expect that spec is SILENT on:**
- **Volume** — no explicit spec column. Closest analog: `AudioSegmentV0.condition_profile` (subsumes SNR / bandwidth), or `signal_ring@v0["audio"]["vocal_emphasis"]` (louder-than-baseline signal). No dedicated volume field on any contract.
- **Speaker embeddings** — **STRUCTURALLY FORBIDDEN at per-utterance level by §6.2 bullet 4** (verbatim: *"Never stored audio; never per-utterance speaker embeddings. Embeddings used during clustering are destroyed after cluster assignment."*). `pyannote/embedding` model output is admissible ONLY as clustering input, discarded after cluster-assignment.
- **Named-person identifiers** — the spec's `named_persons` handling is via §6.4 idiolect rule (excluded from register) + Owner Ruling #5 (detect-yes, release-gated). No contract slot for "this segment names Person X".
- **Prosodic stream per segment** — spec §5.2 Character Register PROSODIC LAYER stores *"Intonation contours, stress, rate distributions, pause structure"* at group level. Per-segment prosody data (owner's likely mental model for "pitch stream" and "tone stream") is captured in `signal_ring@v0["audio"]` dims, but the extractor that fills those dims is un-built.

**One-line diagnosis for Layer 4 data-model:** the spec authors a **row-per-segment, N-column data model with 8 named columns**. The contract layer has slots for 3 of the 8 as first-class fields (content via ASR provider, occurrence via `Occurrence`, condition as opaque scalar). The other 5 are either (a) taxonomies on Signal Ring without extractors (prosody, music, part of condition), or (b) missing entirely (language on the segment contract, code-switch, group-level character). **Owner's "N attribute streams stored as a bundle" is architecturally correct per spec §1.1 — but the bundle is currently a stub. The frozen contract wire is there; the fillers of most columns are not.**

---

# PART 5 · SUMMARY IN 5 LINES OF PLAIN LANGUAGE

1. **The orchestration stack verifies process liveness + file existence, never work progress.** Six specific predicates (heartbeat freshness, PID-alive, launch-file present, poll-file present, ACTIVITY_SUMMARY.md present, seal filename case-insensitive) — every one is metadata. **Silent-success is design-inherent.**
2. **The text-training half of the platform (77 sealed HF LoRA runs across two H200 hosts) is REAL.** Trainers loaded real corpora, ran real HF training, wrote real adapter sha256s.
3. **The audio half is PLUMBING.** Frozen contracts real; atomics real; provider factories real; but the four backend adapters that touch real audio (ffmpeg demux, Silero VAD, pyannote diarization, whisper multilingual) are missing or never invoked. `synthetic_plumbing_only` is a caller-cooperation honesty flag with **no downstream filter**.
4. **Layers 1 · 2 · 6 have no artifact-backed milestone predicate today** — objective-shaped, quality-parameters-set, and milestone-ratified all fail to fire as invariants because their contracts and gates do not exist.
5. **Layer 5 (supervision from OUTSIDE) is the biggest single missing surface** — Watch for audio + progress-verification watchdog + starvation-alarm. This is what would have raised the alarm when `akki-vm` sat at 0% for 3d 10h with dispatcher heartbeats fresh.

---

# PART 6 · ATTESTATION

- **No product code touched.** No `services/**/*.py` edited or created. No pytest invoked. No testing_agent invoked. Ratchet floor **3251** untouched.
- **No push.** Local commit only, on workspace `master` (this document).
- **Retracted ChatGPT integration** — no OpenAI/ChatGPT reference anywhere.
- **POC HOLD in force** — `W-AUDIO-POC-3-STATIONS` CP0 does not open until owner ratifies the 3-station selection.
- **Every verbatim quote in this document was pulled from a file opened in this session.**
- **The correction owed to the owner about my own §F7.4 "77 campaign runs" phrasing** is on the record at the top of this document.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
