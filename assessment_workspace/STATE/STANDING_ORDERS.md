READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# STANDING_ORDERS.md — Permanent standing law

**This file is the single source of standing discipline for every session — fresh, forked, or compaction-restarted. Read it before anything else. Do not paraphrase, do not skip, do not treat as history. Edits require an explicit owner ruling banked in `STATE/DECISIONS.md`.**

---

## 1. SESSION BOOT PROTOCOL

The CHUNK-1 problem statement is a **STALE bootstrap brief**. Never re-run it. Never re-clone the repos. Never wipe `/app/assessment_workspace/`. Never scaffold a new FastAPI/React/Expo app in `/app/backend` or `/app/frontend`.

Boot sequence (in order, no shortcuts):

1. Read this file top to bottom.
2. Read the last 300 lines of `STATE/DECISIONS.md` AND `STATE/NEXT.md`.
3. Verify repo HEADs match `STATE/PINS.md`; verify ratchet floor from `repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json` — `counts_at_baseline.passed` and `invariants_enforced_when_baseline_guard_1.passed_floor` must match.
4. Resume the in-flight work order named at the top of `STATE/NEXT.md`. Do not open speculative work.

---

## 2. ENGAGEMENT DISCIPLINE

**Mission-framed reporting (owner ruling 2026-09-08T~05:15Z, verbatim):**

> "The analysis is never the subject. The subject should be the mission at all times - what are we building, what are the verified gaps surfaced and what are the missing requirements - output is lets generate xxx to close the gap, build and ensuring its works."

**Communication doctrine refinement (owner ruling 2026-09-09T~13:15Z, verbatim, superseding cadence rules below):**

> "It is to be applied once you have run analysis and you need to take a decision especially when on autonomous mode or you want to recommend a way forward. On updates, give an update of progress made, how much to go, decisions you have taken, discoveries made that were not envisioned at planning, recommendations to make experience better inline with the mission and this is only at the end of a large building sprint/wave - eg Solva building. for micro sprints, keep progress updates within the sprint plan."

**Two report formats — pick by trigger:**

- **DECISION-POINT format** (autonomous-mode calls, recommendations, plan compilations) — four sections, plain product language:
  1. What we are building — one-paragraph mission synthesis from the full requirement base.
  2. Verified gaps — honest gap list with updated percentages.
  3. Missing requirements — remaining M-items in plain words.
  4. Generate-to-close plan — "to close gap N we generate/build X, proven working by Y".

- **END-OF-WAVE format** (owner-facing at large wave close only — Registry-Full-Build, Solva-Lift, DAP waves, etc.) — five sections, plain product language:
  1. Progress made.
  2. How much to go.
  3. Decisions taken.
  4. Discoveries not envisioned at planning.
  5. Recommendations to make the experience better, in line with the mission.

**Micro-sprint (CP-level) updates** stay INSIDE the sprint plan / grounding brief · never owner-facing as separate reports. Commit messages + DECISIONS entries + `STATE/NEXT.md` step markers carry the CP-level record. Owner sees the wave-close roll-up, not CP-by-CP narration.

Analysis appears only as evidence behind those sections. No REQ-ID walls in top-level narrative. No engineering vocabulary on the surface.

Owner-facing output is **metrics first**: requirement → status → evidence path → %. Plain language. No machine jargon. No assumed emphasis. No filler.

Requirements are **never flattened**. Sub-clauses stay distinct. Every requirement quoted verbatim in the gating test's docstring and in the wave grounding brief. If the verbatim quote is not in the test, the test does not gate the row.

Ambiguity is **never reflected back as an open question**. State the specific ambiguity, apply ONE stated default with rationale, mark it `DEFAULT-PENDING-OVERRIDE`. The owner overrides on the next turn if the default is wrong.

Every owner ruling is banked **verbatim** in `STATE/DECISIONS.md` **before** any action is taken on it.

---

## 3. BUILD DISCIPLINE

- **Tests-first, mechanical RED.** No code lands without a drill receipt showing the tests failing for the right reason on the pre-implementation tree. RED receipt banked under `phase0/drill_receipts/`.
- **Double-green byte-match to close.** `BASELINE_GUARD=1 python -m pytest` under the repo root, run twice back-to-back, byte-identical tally. Both receipts banked.
- **Ratchet floor monotonic-up.** `baseline_failures.json` `counts_at_baseline.passed` and `invariants_enforced_when_baseline_guard_1.passed_floor` bump in tandem; `ratchet_history` entry appended.
- **Two-commit pattern.**
  - **Commit A (code):** `repos/Extraction-Akki/` on branch `programme/track-a`.
  - **Commit B (state):** `/app/assessment_workspace/` on branch `master` — STATE, notes, phase0 receipts, canon drops, prototypes.
- **Never push.** Local commits are the record.
- **Terminal pytest only.** The `testing_agent` and every other test-orchestrating subagent is BANNED by owner. Curl / python3 -c are allowed for spot checks.
- **No refactor.** Thin-kernel discipline — do only what the current wave scopes.
- **Grounding brief before every wave.** File in `notes/`, verbatim owner quote in §A, wave-honest-limits in §E, commit protocol in §F.

### 3.1 ALIVE IS NOT DONE — silent-success ban (W0 integrity fix, 2026-09-13)

**Standing order (verbatim, banked by owner directive "BUILD GO" 2026-09-13 · CP0.a→W0 close):**

> **ALIVE IS NOT DONE.** The existence of a heartbeat, a running PID,
> a directory on disk, or a filename in that directory is NOT proof of
> completion. Completion requires an OUTPUT ARTIFACT — a seal file
> whose contents, when parsed, prove the specific real work-kind that
> just finished. A seal read that does not parse `Kind:` and refuse
> non-real kinds silently promotes stubs, synthetic fixtures, and
> unfinished runs to success. This is banned.

**Binding contract on every seal read:**

1. Every sealing check in the codebase MUST route through
   `services.output_verified_seal.is_real_seal(run_dir)` (or the
   sibling `parse_seal` primitive when the caller needs the parsed
   payload). Bare filename-existence checks against `ACTIVITY_SUMMARY.md`
   are banned. Refactoring around the primitive is not optional.

2. A "real seal" is a file that (a) exists at the canonical
   `ACTIVITY_SUMMARY.md` path (case-insensitive), (b) carries a
   `Kind:` line in its body, and (c) whose `Kind:` value names a
   real-work kind — NOT `stub`, `synthetic`, `unfinished`,
   `test_fixture`, or the empty string.

3. Every seal write MUST route through
   `services.output_verified_seal.output_verified_seal(run_dir,
   kind=..., body=...)`. The writer emits `Kind: <value>` as a first-
   class field in the body. A write without a kind is refused
   (`ValueError`).

4. Silent-success attack surface enumerated at W0 open (2026-09-13 ·
   6 code sites, all refactored in this wave):
     - `services/campaign_infra/reconcile.py::_is_sealed`
     - `services/campaign_infra/run_queue.py::_is_run_sealed`
     - `services/orchestrator_resilience/orphan_detector.py::_has_sealing_marker`
     - `services/orchestrator_resilience/adopt.py::can_adopt`
       (direct `.exists()` on line 85)
     - `services/orchestrator_resilience/watchdog.py` (via
       `_od._has_sealing_marker` on line 126)
     - `services/campaign_infra/on_host_logging.py::write_run_summary`
       (writer side — emits `Kind:` on every write)

5. Invariant `test_output_verified_seal.py` freezes this contract.
   Adding a new seal read/write in the codebase without routing
   through `output_verified_seal` is a right-reason RED failure
   under BASELINE_GUARD=1.

### 3.2 NO RUN WITHOUT A PROGRESS SIGNAL — runtime silent-no-progress ban (W1 CP2b, 2026-09-13)

**Standing order (verbatim, banked by owner directive "W1 CP breakdown approval" 2026-09-13):**

> **NO RUN WITHOUT A PROGRESS SIGNAL** — every commissioned run must
> emit a progress signal within its SLA or the supervisor raises a
> starvation alarm and HALTS the run.

**Binding contract on every commissioned run:**

1. Every dispatch surface in the codebase MUST bind its run_id to
   the `services.work_supervisor.runtime_supervisor` progress-ring:
   the running trainer/harvester/extractor emits `ProgressSignal`
   records at least once per SLA window via
   `runtime_supervisor.record_progress(sig, ring_root=…)`.

2. Before treating a run as still-in-flight, callers MUST invoke
   `runtime_supervisor.output_verification_watchdog(job_id,
   sla_seconds=…, ring_root=…, now_utc=…)`. A returned
   `HaltVerdict` binds the caller to STOP dispatching further work
   on that run and surface the verdict.

3. Halt reasons are closed-enum data (`starvation_no_signal` /
   `starvation_stale_signal` / `starvation_output_flatline`). A
   HALT verdict is DATA — the runtime supervisor NEVER kills any
   process. Callers act on the verdict; observation and mutation
   remain separate (zero-influence discipline preserved).

4. Wave-honest limit: the W1 watchdog measures BYTE growth, not
   semantic growth. A run that writes zeros steadily would pass
   the flatline check. Semantic watchdogs (per-kind output shape
   validators) are Part-B concerns.

5. Invariant `test_w1_cp2b_runtime_supervisor.py` freezes this
   contract. Any dispatch surface added later that does NOT bind
   to the progress ring is a right-reason RED under BASELINE_GUARD=1.

### 3.3 NO SEAL WITHOUT BOTH SHAs — post-seal receipt rule (2026-09-15)

**Standing order (verbatim, banked by owner directive "Discovery-1 ratification" 2026-09-15T~20:35Z · CP-M6-4-2 partial-seal reconciliation precedent · owner authorization in DECISIONS.md same date):**

> "No CP may be reported 'sealed' in any summary or handoff unless BOTH commit SHAs (track-a Commit A + master Commit B) are recorded in the seal/DECISIONS entry."

**Owner §A authorization (verbatim, same channel, same date):**

> "Your Discovery-1 recommendation is RATIFIED under the owner's standing 'requisite guardrails' mandate — it strengthens discipline with zero scope impact. Amend STANDING_ORDERS with the one-line post-seal receipt rule: 'No CP may be reported "sealed" in any summary or handoff unless BOTH commit SHAs (track-a Commit A + master Commit B) are recorded in the seal/DECISIONS entry.' Bank the amendment with this message as §A authorization."

**Binding contract on every CP seal:**

1. Every CP seal file MUST carry at seal completion:
   - `Track-a HEAD at seal:` — the actual `programme/track-a` Commit A SHA (never `TBD`).
   - `Master HEAD:` — the actual `master` Commit B SHA (never `TBD`).
2. Every DECISIONS.md CP entry MUST carry both SHAs at CP close.
3. Every NEXT.md CURRENT AS OF pin MUST carry the track-a SHA at CP close (master SHA discoverable via state repo `git log`).
4. Handoff / status summaries that claim a CP is "sealed" MUST include both SHAs, or the CP MUST NOT be reported sealed.
5. This closes the partial-seal drift class the CP-M6-4-2 reconciliation exposed (mechanism + tests + receipts + ratchet-bump present, both commits absent, seal file absent — the CP was NOT actually sealed but was reported as such in the handoff summary).

**Enforcement:** at seal-check time the reader compares the seal-file `Track-a HEAD at seal:` value against `git log --oneline -1 programme/track-a` in the code repo AND the seal-file `Master HEAD:` value against `git log --oneline -1 master` in the state repo. Any `TBD` or missing SHA is a right-reason RED under §3.3.

**Rationale.** ALIVE IS NOT DONE (§3.1) closes the seal-file-missing class. NO RUN WITHOUT A PROGRESS SIGNAL (§3.2) closes the runtime-silent class. §3.3 closes the seal-claimed-but-commit-absent class: the last honesty gap in the tests-first → RED → GREEN → SEAL → COMMITS discipline chain.

---

## 4. RUNTIME LAW

- **Literal design adoption.** Prototype HTML is byte-identical; interpretation is banned. Substitution rules bind to rendered DOM only. A rule that matches nothing is a RED right-reason failure — it does not silently degrade.
- **No engineering vocabulary on product surfaces.** No "endpoint", "PID", "manifest", "ratchet", "invariant", "seam", "hash" on any owner-facing surface. Refusals and empty states speak plain product language ("not measured", "not yet extracted", etc.).
- **Pod runtime must mirror the repo.** Built-but-not-shipped is a failure class. If the pod's `/app/backend` or `/app/frontend` diverges from `repos/Extraction-Akki/pod_shell/*`, that is a RED-worthy finding named in the next wave's grounding brief.
- **PII / credential custody.**
  - AWS RDS Data API credentials: `/app/backend/estate_keys/data_sources/db-restore-603-cluster.json` (mode 0600).
  - GPU host SSH private key: `/app/backend/estate_keys/gpu_hosts/id_ed25519_akki_gpu` (mode 0600).
  - Host IPs and usernames: `/app/backend/.env` (`AKKI_VM_HOST`, `AKKI_VM_II_HOST`, `AKKI_VM_USERNAME`, `AKKI_VM_II_USERNAME`, etc.).
  - Never committed. Never returned in responses. Never logged. Never in test docstrings. Redacted everywhere.
- **Owner Clarification 1 (2026-08-14):** no push, ever. Local commits are the record.

---

### 4.1 §E · CREDENTIAL CUSTODY READ DISCIPLINE — Redaction Hardening Option 1 (owner ruling 2026-09-15T~22:30Z)

**Ratified same turn as SEC incident `sec_incident_jump_cred_leak_20260915T222935Z` (JUMP root pw leaked to agent-tool STDOUT via a bad sed redaction).**

**Rule.** Custody files under `CUSTODY_PATH_PREFIXES` (currently `/app/backend/estate_keys/`) may only be read through one of two disciplines:

1. **Shape-only helper** — `services.secret_hygiene.custody_file.read_custody_metadata(*, path)` returns a frozen `CustodyFileMetadata` carrier whose per-field entries expose ONLY `field_name` + `value_length_bytes` + `value_sha256`. The helper structurally cannot return raw column values: the returned dataclass has no value-bearing attribute.

2. **Env-injection into the target process** — any consumer needing the actual secret binds it directly into the target process's environment (`MYSQL_PWD`, `sshpass -e`, `Authorization: Bearer $TOKEN`, AWS SDK credential providers) so that the value never crosses a stdout-visible layer. The injecting shell script itself must not fall foul of §3.3 or the existing `assert_no_transcript_set_x_with_password_var` guard.

**Any direct read outside these two paths is a SEC-class violation.** Direct reads specifically include, but are not limited to: `cat`/`head`/`tail`/`less`/`more`/`bat`/`view`/`type` against a custody path (caught at authoring-time by `assert_no_transcript_cat_on_custody`); `csv.reader(open(...))` + `print(...)` co-occurrence (caught by `assert_no_transcript_csv_header_emit_on_custody`); `openpyxl.load_workbook(...)` + `print(...)` co-occurrence (caught by `assert_no_transcript_openpyxl_iter_rows_on_custody`); shell tracing (`set -x`, `bash -x`, `-o xtrace`) co-occurring with a credential-shaped env var (caught by `assert_no_transcript_set_x_with_password_var`); and — as of this ruling — any pattern that reads a custody file's bytes through the agent-tool STDOUT surface even with a redaction filter unless the redaction is proven structurally-safe by the shape-only helper.

**Scope this CP (CP-SW6-HYG-1):** JSON custody support. CSV / xlsx / raw-key formats refuse with `CustodyFileFormatUnsupportedError` — extension is a follow-on CP when a specific schema is standardised.

**Option 2 (encrypt-at-rest) was DECLINED same turn** — key custody would live on the same pod, adding ceremony without a real trust-boundary gain at pilot stage. Revisit at BC-build time.

**Enforcement.** At any future CP that adds custody surfaces, the CP's grounding brief must state one of: (i) the surface is read only via `read_custody_metadata` + env-injection, or (ii) an owner ruling explicitly ratifies a scoped exception. Silent direct reads land as SEC incidents with the same discipline as this session's `sec_incident_jump_cred_leak_20260915T222935Z`.

---

## 5. GPU OBLIGATIONS

- **Full-consumption guarantee** while a campaign window is open. All 4 GPUs across the two hosts (`akki-vm`, `akki-vm-ii`) run at high utilization until the window closes. Idle lanes are an **interrupt-priority** condition that outranks documentation and audit work.
- **Never kill a training run mid-flight.** Reconcile via `campaign_infra.reconcile` reading `~/akki_journal/` on the hosts. Ownership passes through the run's ACTIVITY_SUMMARY.md seal, never via SIGKILL.
- **Idle-lane restoration** uses the banked machinery in `tools/queue_followon_launcher.py` + `tools/on_host_queue_dispatcher.py` + the pd × ctx logits cap invariants; do not improvise.
- **Custody paths for GPU operations:**
  - `/app/backend/estate_keys/gpu_hosts/id_ed25519_akki_gpu` — SSH private key (mode 0600).
  - `/app/backend/estate_keys/data_sources/` — data-source custody files.
  - `/app/backend/.env` — `AKKI_VM_HOST`, `AKKI_VM_PORT`, `AKKI_VM_USERNAME`, `AKKI_VM_SSH_PRIVATE_KEY_PATH` and the `AKKI_VM_II_*` twin set.
  - Verify credential-chain audit at wave open per DECISIONS entry 2026-09-06T~14:20Z.
- **Fallback-burn records** live in `phase0/gpu_burn/` and `phase0/gpu_fill_burns/`; never mixed into `shield-train/*` or `baseline_lines/*`.

---

## 6. CURRENT AUTHORITATIVE ARTIFACTS

Read alongside this file; do not paraphrase.

- `notes/MASTER_TRACEABILITY_AUDIT_20260907.md` — master requirement-vs-code reconciliation · **landed 2026-09-08T~04:40Z** · per-source detail files under `notes/MASTER_TRACEABILITY_AUDIT_20260907/` (S15 Doc 0 · S16 Security Promise Set · S17/S18 Security Amendments · S19 Rules Service Spec · S20 Rule Book Library · S21 System Rules Registry INVENTORY · S22 WPW · S23 v2 Prototype surfaces · S24 Donor Akki-OS-V1 · S25/S26 Donor Executive-Core/Final · S27 Donor RMS-IQ-Core-2 salvage · S28 BUILD_JOURNAL claims-to-verify) · authoritative once owner accepts.
- `notes/TRUE_STATE_OF_CODE.md` — accepted 2026-09-06T~19:20Z.
- `notes/SURFACE_AUDIT_v2_prototype_20260907.md` — 47-surface audit against the v2 prototype.
- `STATE/SPRINT_PLAN.md` — chartered follow-on waves.
- `STATE/WPW_CHARTER.md` — Whitepaper Wizard v1 scope.
- `notes/ingest_20260907/` — Doc 0 governance architecture + Security Promise Set + Rules Service Spec + System Rules Registry inventories.
- `canon/text/` and `canon/drops/20260907/extracted/` — extracted canon and drop text.
- `canon/prototypes/20260907_v2_standalone/` — v2 prototype (binding design source).
- `phase0/campaign_drafts/CAMPAIGN_OBJECTIVES.md` + `CAMPAIGN_MANIFEST_TABLES.md` + `CAMPAIGN_V2_WINDOW_FILL_MATH.md` — campaign design + math.
- `phase0/campaign_drafts/REATTACH_RUNBOOK.md` — session pickup after context loss; references this file.
- `phase0/campaign_drafts/campaign_*_v21_lane*_queue_manifest.json` — active campaign queue manifests.
- `repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json` — ratchet floor + `ratchet_history`.
- `STATE/PINS.md` — repo pinned HEAD SHAs, custody paths, protected env vars.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
