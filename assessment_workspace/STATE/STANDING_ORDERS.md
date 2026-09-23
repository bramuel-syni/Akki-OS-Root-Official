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

### 2.1 ORDER OF AUTHORITY (R-18 · owner ruling 2026-09-18 · binding on M11, M12 and every subsequent wave)

**Order of authority, fixed** (higher amends lower; lower NEVER amends higher; every conflict resolves upward):

1. **(a) Canon** — Ratified canon rules carrying IDs: Documents 0–20 and amendments through `watch_learning_v1`. In build artefacts the word "Canon" means **(a) only**.
2. **(b) Standing Orders** — this file. Derives from canon; never overrides it.
3. **(c) System Engineering Reference (SER)** — the engineering derivation of canon, not a replacement for it. Where SER and canon conflict, canon prevails and the SER is corrected. In build artefacts and PR titles the SER is cited as `SER §x`, **never as "Canon"**.
4. **(d) Contract schemas** — `contracts/*.schema.json` and adjacent contract-versioned artefacts. Bind code shape and vocabularies; derived from canon and SER.
5. **(e) Code** — the tree at `backend/**`, `services/**`, `tools/**`, `tests/**`. Bottom of the ladder; never amends anything above it.

**Traceability enforcement**: every SER Part B and Part C section carries a "Canon anchors" line naming the rule IDs it derives from. Requirement rows in D.6 `requirements.yaml` gain `canon_ref` (existing registry ID, or `none-new-needs-ratification`); a requirement with neither `canon_ref` nor `test_id` fails the documentation check. D.6's "this document supersedes that count" line is struck: the SER **extends and cross-references** the register, it does not supersede it.

**Rationale**. R-18 restores the single line of authority to canon and eliminates the risk that a lower-layer derivation (SER, schema, or code) silently amends a higher-layer rule. Every ruling below this line in the SO derives from canon; every SER section from now on must show its canon anchor line-by-line.

---

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

### 3.8 THIN-KERNEL / NO-REFACTOR — additive-only discipline (Owner ruling 2026-09-17 · Tension (a) = Option C · thin adapter layer)

**Standing order (verbatim · owner ruling relayed 2026-09-17T~15:45Z on the M11 gate ask):**

> "Tension (a) RULING = Option C (hybrid adapter layer `services/enforce/<entity>_gate.py`; §3.8 held verbatim, no M9 changes). Conditions: AST sole-importer enforced BOTH directions (M9 refuser importable only from `services/enforce/`; `akki.data.repo` importable only from `services/enforce/` and `akki.data`; any router importing a refuser or the repo directly fails CI; routers reach persistence only via `Depends(<entity>_gate)`); every adapter calls the refuser BEFORE any repo write, fails CLOSED on refusal, and emits a ledger intent for BOTH refusal and acceptance. Exit evidence at M12: AST rule in CI; P-07 refusal parity across all 36 entities; B.2 tenant-mismatch write test (AKKI-DATA-001) passing through every adapter."

**Binding contract:**

1. **Additive-only.** No CP may modify a sealed module. Every new capability lands as a new file, a new class, or a new function on a NEW package path — never as an edit to an existing sealed carrier.
2. **Sole-importer AST invariants (both directions).** `akki_arch` invariants MUST enforce, at CI:
   - M9 refusers (`platform_control_plane.<module>.assert_*`, `refuse_*`, etc.) are importable ONLY from `backend/services/enforce/**/*.py` and from paired-tests directories.
   - `akki.data.repository.Repository` and its factories are importable ONLY from `backend/services/enforce/**/*.py` and `backend/services/data/**/*.py` and from paired-tests directories.
   - Any router / handler / service outside `services/enforce/` that imports a refuser or the repository directly is a HARD RED at CI.
3. **Router persistence path.** Routers reach persistence ONLY via `Depends(<entity>_gate)` where `<entity>_gate` lives under `services/enforce/`. The gate function calls the M9 refuser first; only on refuser-pass may the gate invoke the repository.
4. **Fail-CLOSED on refusal.** If the M9 refuser rejects (raises a refusal or returns a REFUSED verdict), the adapter MUST NOT call the repository. It MUST emit a ledger intent tagged `refuser_verdict=REFUSED` and propagate the refusal to the caller.
5. **Ledger intent parity.** Every adapter emits a ledger intent for BOTH refuser-REFUSED and refuser-ACCEPTED paths (parity is the invariant — asymmetric emission is a RED).
6. **Exit evidence at M12 seal:** (i) the `akki_arch` AST rule enforcing (2) is on and green in CI; (ii) `P-07` refusal-parity acceptance test passes for all 36 M9 entities; (iii) `B.2` tenant-mismatch write test refuses with `AKKI-DATA-001` when invoked through every adapter.
7. **`allowed_import_targets` exception mechanism.** The M13-W1 precedent (Ruling · 2026-09-17T~13:30Z Binding-effect 4) established that shared-primitive cross-imports may be resolved by whitelisting specific import targets in the `akki_arch` rule's `allowed_import_targets:` list rather than by refactor. This mechanism is available for §3.8 to preserve verbatim status. Any new use of `allowed_import_targets` must be surfaced in the seal note.

**Interaction with prior wording.** Prior SO §4.2 line "SO §3 (no refactor / thin-kernel discipline)" now formally resolves to this §3.8. The clause replaces no earlier text; it names what was previously referenced only in aggregate.

---

### 3.10 ZERO CLOSED ENUM TYPE — technical reading amended (Owner ruling 2026-09-17 · Tension (b) = Option α)

**Amendment text (verbatim · owner ruling relayed 2026-09-17T~15:45Z):**

> "'Zero closed enums' means no Enum subclassing. Final tuple constants are permitted only where a test asserts them equal to the corresponding contract-schema enum."

**Amendment conditions (verbatim · same channel):**

> "The authoritative closed set is the enum in the akki-contracts JSON Schema for that contract version (B.3), NOT the Python tuple; every fixed-vocabulary `Final[tuple[str, ...]]` carries a test asserting equality with the schema enum; vocabulary changes are contract-version changes."

**Binding contract:**

1. **Banned constructs.** No `from enum import Enum, IntEnum, StrEnum, Flag, IntFlag` in any P1–P6 M9 module, TCB package, or downstream service. No `class X(Enum): ...`. No `class X(str, Enum): ...`. No `IntEnum`, `Flag`, `IntFlag`. Existing wording "zero closed enum type" resolves to this exact ban surface.
2. **Permitted constructs.** `Final[tuple[str, ...]]` (or `Final[tuple[Literal[...], ...]]`) module-level constants ARE permitted. Existing on-disk practice (`ACTION_CLASSES`, `PILOT_TENANT_KEYS = ("RMS", "DigiCow", "BDO", "Trinity")`, etc.) is retroactively ratified.
3. **Authoritative source.** For every fixed-vocabulary constant, the AUTHORITY is the corresponding JSON Schema enum in `contracts/*.schema.json` (or the akki-contracts contract-version bound to that surface). The Python tuple is a MIRROR of the schema enum; it is not the source of truth.
4. **Mandatory equality test.** For every `Final[tuple[str, ...]]` closed-vocabulary constant, a paired test MUST assert `tuple(sorted(PY_CONST)) == tuple(sorted(SCHEMA_ENUM))`. Failure is a right-reason RED. Suggested test-ID pattern: `test_<constant_name>_matches_contract_schema_enum`.
5. **Vocabulary changes are contract-version changes.** Adding or removing a value from a closed vocabulary is a CONTRACT-VERSION change (B.3). It cannot land as a code-only PR. The schema version bump + the code mirror-update must land together; the equality test at step 4 keeps them synchronized by construction.
6. **Retro-conformance.** M9 already-frozen closed vocabularies (Watch verdict actions, permission verbs, capability ceilings, pilot tenant keys, etc.) are grandfathered as-is at M9 seal snapshot. Their equality tests will be authored under `M12b-W1` alongside the schema-enum landing. Where the schema enum does not yet exist, the M12b wave authors it; the equality test forces the two to agree.

**Interaction with existing invariants.** Existing M9 grep-negative invariants (21-token grep-negative on module sources, "zero closed enum type" in every M9 seal note) continue in force. This amendment does NOT loosen them; it clarifies that they target `enum.Enum` subclassing, not fixed-vocabulary tuples.

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

### 4.2 VERIFICATION-WALK SCOPE DISCIPLINE — wave-window commit enumeration (owner ruling 2026-09-16T~06:15Z)

**Ratified same turn as CP-M7-W1-POST-2 close (2026-09-16T~06:00Z), which surfaced the discipline gap.**

**Rule.** When a wave-close is being verified (e.g. M7-open W0/W1 verification walks, or any future milestone-open verification walk), the verification MUST enumerate **every commit within the wave-window**, not just the canonically-named wave-close commit.

**Concrete this-shift precedent (why the rule exists).** The M7 W1 verification receipt (2026-09-16T~04:15Z · `phase0/m7_w1_verification/verification_receipt_20260916.json`) enumerated only the 5 W1-close modules last-touched by commit `fe01e5e` (W1 close 2026-09-13T06:33:22Z). It missed the W1b close 26 minutes later (`53645935` at 06:59:30Z · ratchet 3392 → 3492 · +100) that shipped 6 additional platform primitives (`services/capability_registry.py`, `services/governance_plane/retention_policy.py`, `services/source_plane/connector.py`, `services/source_plane/synology_file_station.py`, `services/audio_plane_v1/attribute_stream_bundle.py`, plus L2/L4 contract shells). The gap was surfaced by CP-M7-W1-POST-2's tests-first RED drill (`test_capability_registry_module_importable PASSED` at RED · a pre-existing module was importing), and rescued the walk from rule-proliferation.

**Enforcement mechanics for every future verification walk:**

1. **Compute the wave-window** = `[wave-open commit .. next-wave-open commit)` on `programme/track-a`. If the wave-close is the final wave in a milestone, the window closes at the milestone's next-milestone-open commit or `HEAD` at verification time.
2. **Enumerate ALL commits in the window** via `git log --format="%H %cI %s" <open>..<close_or_next>` on `programme/track-a`.
3. **Enumerate ALL first-added `services/` and `tests/invariants/` files** across the window via `git log --diff-filter=A --name-only --format="%H|%cI" <open>..<close_or_next> -- 'backend/services/**' 'backend/tests/invariants/**'`.
4. **For each enumerated file**, apply the six-check schema (C.1 primitive surface · C.2 invariant tests present + pass · C.3 case-agnostic doctrine · C.4 unchanged since add · C.5 compose/scope-boundary honoured · C.6 no banned enforcement/refusal tokens on public surface unless owner ruling ratifies).
5. **Any file missed by prior verification** is a first-class **wave-honest limit** to be surfaced in the current receipt with a candidate follow-up CP (as CP-M7-W1-POST-2 surfaced W1b).

**Ban on canonical-close-commit-only enumeration.** Restricting a verification walk to the canonically-named wave-close commit (`git log -1 <close-commit-name>`) is a right-reason RED failure under this rule. Verifications MUST use the window-enumeration disciplines above.

**Clause 6 · CROSS-WAVE MODIFICATION HANDLING (added 2026-09-16T~06:35Z per CP-M7-W1-POST-4 wave-honest discovery).** When a module added in Wave A is legitimately extended by a later Wave B (via B's own CP · with B's own ratchet delta · with B's own owner-directive citation · via APPEND-ONLY-EXTENSION discipline), Wave A's verification walk (via `git log --format=%cI %h <wave-A-open>^..<wave-A-close>`) tests the module's last-touched **WITHIN** the wave-A window and SURFACES any post-wave-A modifications as wave-honest discoveries in the receipt. Post-wave-A modifications are NOT treated as drift under Wave A's verification; the modifying wave's own verification (Wave B's POST-*-VERIFICATION) enforces the shape of Wave B's changes.

A cross-wave modification is DRIFT only when it (a) has no CP citation / ratchet delta / owner directive, or (b) violates SO §3 (no refactor / thin-kernel discipline).

Concrete this-shift precedent (CP-M7-W1-POST-4 · 2026-09-16T~06:30Z): `services/reliable_time_source/clock.py` was added at M2 SW5 (`f4fc201f` · 2026-09-13T19:35:41Z · `AU_3B_DEFENSIBLE_DRIFT_BUDGET_MS=100ms`) → modified at M2 END-GATE (`95d688cd` · 19:54:49Z · loosened 100ms → 24h for M2 tests · incidental note in commit message) → LATER MODIFIED at M3 SW1 (`eaa0e04` · 2026-09-14T05:24:59Z · Flag-2 tight-budget guard: `TIGHT_DRIFT_BUDGET_MAX_MS=5000` + `LooseAnchorRefused` + `assert_defensible_for_governed_write()`). The M3 SW1 modification is out of M2 wave-window scope; M2 POST-4-VERIFICATION surfaces it as a cross-wave note and does not fire drift. M3's future POST-5-VERIFICATION will enforce the M3-scope shape of the extension.

**Wave-honest bootstrap.** This rule was ratified after the W0 + W1 verifications this shift landed with the narrower canonical-close-only scope. Those closes stay clean-as-closed (Path α zero-delta each); the W1b gap is being closed forward via **CP-M7-W1-POST-3-VERIFICATION** (this-shift-next). Future verifications land with the wider window-enumeration scope from the start.

---

### 4.1 §F CREDENTIAL-DROP SHA-PIN AT INTAKE OR REFUSE (R-18 Part 7(c) · owner ruling 2026-09-18 · binding)

**Rule.** Every credential drop entering `/app/backend/estate_keys/**` or `/app/assessment_workspace/custody/**` carries a sha256 pin recorded at the moment of ingestion into a persistent manifest at `phase0/credential_drop_manifests/YYYYMMDDTHHMMZ_drop_manifest.json`. A drop that enters custody without a sha pin recorded is **REFUSED at intake**: the file is quarantined at 0600 outside `estate_keys/` (e.g. under `/app/assessment_workspace/custody/quarantine/`), the incident is surfaced as an owner-desk item in the next report, and no downstream wave may consume the file.

**Rationale (R-18 Part 7(c)).** OWNER-DROP-02 established that the RMS xlsx C9 had no prior sha pin at ingestion; without one, a "rotated" copy is indistinguishable from a stale replay. R-18 accepts the ingested sha `d778eb1e…` as the baseline for that specific historical drop, and forward requires the sha-pin-at-intake discipline for every subsequent drop.

**Enforcement.** (i) `tools/credential_drop_ingest.py` (or its future analog) must compute and write the sha256 as part of ingestion; (ii) new intake receipts land under `phase0/credential_drop_manifests/` with the file-set + per-file sha256 + `mtime_utc` + `mode_octal`; (iii) any custody-store file whose sha256 is not in a manifest at read-time is treated as untrusted until the owner ratifies its pin.

**Interaction with §4.1 §E.** This clause is additive to §4.1 §E: sha-pin discipline governs BYTES-level identity of the drop; §4.1 §E governs RAW-VALUE read discipline. Neither replaces the other. Together they close the "rotated-file byte-identical to original" evidence path (OWNER-DROP-03).

---

### 4.3 HF TOKEN HASH-DELTA GATE (R-18 Part 7(e) · SEC-2026-09-12-01 · owner ruling 2026-09-18 · binding)

**Rule.** Any wave, CP, or code path that touches HuggingFace **HOLDS** until the HF token's rotation is proven by a **hash delta** between the last-recorded custody sha256 and the fresh drop's sha256. Rotation is confirmed by hash delta **ALONE — never by opening the value**.

**Fail-closed default.** A leaked HF token value is assumed **live until proven otherwise**. `hf_token_rotated_20260914.csv` byte-identical to `hf_token.csv` stands as evidence that the 2026-09-14 filename-marker rotation never reached the custody store; SEC-2026-09-12-01 stays OPEN. Any HF-touching wave must not open under this state.

**Three-step owner action** (the ONLY resolution path under §4.1 §E):

1. **Revoke** the old token in the HF console.
2. **Generate** a new token.
3. **Re-drop** the new token to `estate_keys/data_sources/hf_token_rotated_<yyyymmdd>.csv` at 0600, with a sha pin recorded via §4.1 §F.

**Builder verification** upon re-drop: compare the new file's sha256 to the last-recorded sha256 for `hf_token*.csv`. If **different**, SEC-2026-09-12-01 closes and OWNER-DROP-03 closes with it. If **byte-identical to the last recorded**, both remain OPEN and the HF-touching wave stays HELD. The builder MUST NOT open the file content — the delta test is a pure sha comparison.

**Scope.** Covers every wave that calls the HF API (model pull, dataset pull, inference), every service that reads a HF token from the environment, every CP whose grounding brief cites HF, and every wave-close commit whose diff touches `hf_token*` or `HF_TOKEN`. Does not cover unrelated waves that never touch HF; those proceed under their own rulings.

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

## 7. §3.3 SEAL-CHAIN INTEGRITY RULES (owner-ratified 2026-09-17)

Ratified in DECISIONS.md §3.3 SEAL-CHAIN INTEGRITY RULINGS 2026-09-17. All six additive to prior discipline; none overrides existing rules.

**R-1 · Master-parity check at CP boundary.** Before opening a new Commit-A on track-a for CP-N+1, verify Master HEAD banks the Commit-B SHA for CP-N in each of (a) the seal file at `phase0/output_verified_seals/cp_p*_*.seal.txt`, (b) `STATE/DECISIONS.md` tail, and (c) `STATE/NEXT.md` "CURRENT AS OF" line. If any of (a)/(b)/(c) shows `pending-C-fixup` or a stale SHA, STOP and reconcile before opening CP-N+1.

**R-2 · Seal-file `pending-C-fixup` counter.** Every boot ritual and every pre-CP-open probe counts occurrences of the string `pending-C-fixup` in `phase0/output_verified_seals/`. If the count is > 0, the seal chain is not clean; refuse to open a new CP until Commit-C fixup lands and reduces the count to 0.

**R-3 · Ratchet-history / git-log cross-check.** Every boot ritual walks `tests/invariants/baseline_failures.json` `ratchet_history` from the last-known-clean master HEAD forward and verifies each entry with `commit: "PENDING"` or a real SHA has a matching `git log programme/track-a` entry and a matching seal file. Divergences are surfaced.

**R-4 · Session-handoff brief reconciliation.** When an incoming session receives a brief claiming CP-N is "sealed", the incoming agent's FIRST action is to verify §3.3 3-commit completeness for CP-N on disk before touching any downstream work. "Sealed" without Commit-B + Commit-C fixup on master is a discipline mislabel and must trigger reconciliation before forward progress.

**R-5 · Per-CP double-green raw-log requirement (NEW DISCIPLINE · MANDATORY).** The seal-file writer MUST refuse to compose a `Double-green: GREEN1 X/Y/Z · GREEN2 X/Y/Z` line unless both raw log files exist on disk at the referenced timestamps (`phase0/drill_receipts/<TS>_<kind>_GREEN1.log` and `phase0/drill_receipts/<TS>_<kind>_GREEN2.log`). No exceptions. Every new CP must capture its own per-CP double-green receipts at seal time. Aggregate-only substantiation is allowed ONLY for retroactive back-compat batches and must be labeled "RECONSTRUCTED POST-HOC AT HEAD <SHA> <DATE>" — never presented as captured-at-seal-time.

**R-6 · Anti-forget boot manifest regeneration (owner ruling 2026-09-17T~20:45Z · MANDATORY).** A machine-checkable boot manifest is maintained at `notes/ORCH_BOOT.md` (state repo · master) with a byte-identical downloadable copy at `/app/frontend/public/audit/ORCH_BOOT.md`. Its ratchet block (`passed_floor` + `baseline_failures_sha256`) is asserted equal to live `backend/tests/invariants/baseline_failures.json` by the always-on invariant test `backend/tests/invariants/test_orch_boot.py` — this is the drift-and-burn priority guard the owner named verbatim ("Ratchet is the field that actually drifted and burned us; it's the priority guard."). Its `heads_last_sealed.*.head` fields carry the LAST-SEALED HEADs (Commit-B SHAs banked in DECISIONS/NEXT per R-1), NOT live `git rev-parse HEAD` — the always-on test asserts 40-hex well-formed + banked-in-STATE presence (full-40 or git 7/8-hex short form), which avoids racing the §3.3 Commit-A/B/C ordering. **Regeneration triggers (MUST regenerate both copies byte-identically at each of these boundaries):** (a) after Commit-C fixup of every §3.3 3-commit seal; (b) after any owner ruling that mutates ratchet, HEADs, or STATE files; (c) on every boot ritual when §1 boot verification detects drift. Freshness of the HEADs is enforced by this boundary-regeneration discipline, not by an always-on equality-to-live-HEAD test. `test_orch_boot.py` is part of the BASELINE_GUARD=1 ratchet; if the manifest goes missing or drifts, the ratchet breaks and forces regen.

**R-6 companion artefact · SHAPING_LEDGER.md (owner directive 2026-09-18 · additive to R-6).** `notes/SHAPING_LEDGER.md` (state repo · master) + byte-identical `/app/frontend/public/audit/SHAPING_LEDGER.md` regenerates alongside `ORCH_BOOT.md` at every R-6 boundary (triggers (a), (b), (c) above). The ledger is a single running registry of every shaping mechanism (SO clauses, invariants, disciplines) currently in force. Regeneration MUST: (i) refresh the `Version` and `Boundary reference` fields at the top; (ii) append a new row for any shaping mechanism landed in that boundary's commit; (iii) never edit an existing row in place — a superseded row gets a SUPERSEDED-BY note appended, and a new row for the successor is added. If the ledger diverges from its authoritative sources (SO / DECISIONS / CP notes / test files), the sources win and the ledger is corrected — the ledger is a pointer atlas, never authority in itself.

---

## §6. LONG AUTONOMOUS RUN PROTOCOL (owner-ratified 2026-09-19T~00:00Z · verbatim · supersedes per-milestone run orders from banking)

**Naming note:** the numeric `## 6. CURRENT AUTHORITATIVE ARTIFACTS` heading above and this `## §6. LONG AUTONOMOUS RUN PROTOCOL` heading are DISTINCT — the former is section 6 of the file's numeric structure (SO §6 in the old sense); the latter is Owner Standing Order §6 (paragraph-mark §). Cross-references disambiguate by their title. Both remain in force.

Standing Order §6 — Long Autonomous Run Protocol
Governs the remaining ~55–90 agent-hours. Banks to STATE/STANDING_ORDERS.md; supersedes per-milestone run orders from its banking. Three guardrails, an escalation policy, pre-rulings for the known forks, and the run mechanics.

### §6.1 — Guardrail 1: continuity across compaction. Files are truth; context is a cache.

Compaction will happen and the agent will not reliably know when. So re-anchoring is unconditional, not event-triggered.

No rule lives in memory. A bound, ruling, or objective not present in STANDING_ORDERS.md, DECISIONS.md, NEXT.md, or the milestone's objective card (§6.2) is not a rule and MUST NOT be acted on. "I recall the owner said" is never sufficient; find it in the file or treat it as unruled.

Re-anchor at every seal boundary and every sub-wave open, cheap by design: read ORCH_BOOT.md, NEXT.md, DECISIONS.md, and the current objective card; run the boot invariants (test_orch_boot.py, test_standing_orders_present.py, and the new test_objective_card_pinned.py); write a ≤12-line resume attestation to NEXT.md — current milestone, sub-wave, ratchet floor, open forks, active bounds, next action — and diff it against the last banked attestation. Any mismatch is a stop-and-report before any write.

ORCH_BOOT regen carries the objective cards for every open milestone, hash-pinned, so a compacted context is rebuilt from the same cards the owner ratified. The audit mirror stays byte-identical.

The ratchet is the memory of record for progress. No silent rebaselining — unchanged. A floor that cannot be explained line-by-line from seal notes is a stop.

### §6.2 — Guardrail 2: objective deviation. Every milestone has a card; every seal cites a card line.

Each milestone and each substantive component gets an objective card at STATE/OBJECTIVES/<id>.md, hash-pinned at ratification:

    OBJECTIVE   one sentence — what this milestone makes true
    MUST DO     numbered lines, each with canon_ref (5–10)
    MUST NOT    bans, each with canon_ref
    EXIT        evidence per MUST-DO line: test IDs, seal conditions
    STOP        milestone-specific stop conditions
    ANCHORS     the underlying components this builds on (§6.3 rule 1)

Self-check at three points: open — the card exists, is ratified, and every MUST-DO line has an anchor; each sub-wave — its seal message cites the card line(s) it advances (test_seal_cites_card.py fails a seal that cites none); close — every MUST-DO line has exit evidence, and anything built that maps to no line is declared as scope drift — additive-only makes it permissible, undeclared makes it a stop.

Cards for M10-W2/3, M10-W4, and M12b-W1 are the three run orders already issued; e1_dev drafts cards for M13–M17, memory layer, and frontends from canon and the SER, for batch ratification at the next seal boundary.

### §6.3 — Guardrail 3: rulings that need the owner. Four tiers before the desk.

When a fork arises, resolve it at the lowest tier that answers it, in order:

1. **Underlying components first.** Does a canon rule or an existing component already answer it? Then that is the answer — cite it, build to it, no ruling. (Most forks so far were this tier.)
2. **Production-grade standard second.** Does a conventional, named industry standard answer it — NIST, Common Criteria, Kubernetes, OTel, Terraform conventions, Kenya DPA? Adopt the conventional choice, cite the standard, tag DEFAULT-class · standard, continue.
3. **DEFAULT-class value third.** Is it a number, cadence, or threshold? Choose the conservative default, tag pending ratification, continue; it batches to the desk at milestone close.
4. **Owner desk fourth** — only for: a canon amendment; a TCB membership change; a change to a Fixed decision-register entry; an exception to a hard invariant; anything externally visible (claims, pricing, partner-facing terms); a security incident; money or legal. These are forks: banked with options and a recommendation, and the run continues on everything they don't block.

Desk items batch at milestone seals, not per fork. TCB-tier ceremonies are never pre-signed; ordinary-tier re-scopes that tighten (never loosen) may be proposed and countdown-started without waiting, countersign requested in the batch.

### §6.4 — Pre-rulings for the forks the estimate names.

**M16 CIF scope** — ruled now, since it moves the number most. CIF is built as canon already defines it: a learned ideation faculty outside the TCB; every CIF-originated idea passes a deterministic acceptance point before affecting anything (BR-9.2, single-experiment principle); CIF proposes and never ratifies (AC-18); its outputs enter the research loop (A5.22, L-4) and the capability register (A20.16, L-5); it has its own halt independent of the Targeta run it feeds (DET-1 closed as a MUST-DO). Nothing beyond that in M16. If the card needs more, that's a fork.

**M10-W4 replay forks** — pre-ruled. Where a writer's legacy semantics cannot be preserved by replay: the legacy store goes read-only and is referenced by provenance; the chain migrates forward-only from cutover; legacy rows are carried as provenance pointers, never re-derived. Bank it, don't stop for it.

**Frontend fidelity bar** — ruled. Functional parity with the established five-stage pattern and the DAP UI Handoff Brief §5 constraints. Prototype adoption where a screen exists; no literal pixel fidelity. The expensive path is not authorised.

**M13 standards** — tier 2 applies. KMS: envelope encryption, per-tenant keys, 90-day rotation (R-4). OTel and Terraform: conventional. Runbooks per B.10. Cite, build, no ruling.

### §6.5 — Run mechanics: the other ways a long sprint survives.

- Restore points are milestone seals. Unrecoverable state rolls back to the last milestone seal, not the last commit.
- Time-box per milestone at 2× the estimate. Exceeding it is a stop-and-report — the run is thrashing, and thrashing burns credits without moving the ratchet.
- Loop detection. The same test RED across three sweeps, or the same fork banked twice, is a stop.
- A build critic seam. Before every seal: RV-tier deterministic checks (the tests) plus a QA-tier self-review against the objective card. The self-review can raise a finding; it never blocks alone, and it never substitutes for a RED test.
- Owner interrupts are processed at seal boundaries only, except a message containing STOP, which is immediate.
- Daily digest replaces per-seal reports: ratchet delta, milestones closed, forks banked, desk items batched, next in flight. Milestone seals still get the one-line report.
- HF hold, §4.1 §E, zero push, no testing_agent — unchanged and not batchable.

### §6.6 — Acceptance of the estimate.

55–90 agent-hours, central ~70, is accepted as the working plan. This protocol's job is to take the 20–25% overhead and the desk-latency multiplier out of it: tiers 1–3 answer most forks without a round-trip, pre-rulings remove the four named movers, and batching turns the rest into one desk visit per milestone.

### §6.7 — Sequence from here.

M10-W2/W3 → M10-W4 → M12b-W1 (its three gates unchanged) → M13 → M14 → M15 → M16 → M17 → memory layer → frontends, G5 interleaved to completion. Objective cards for M13 onward drafted before their milestone opens and batched for ratification at the preceding seal.

### §6 · Landing metadata (bookkeeping — not owner text)

Banked verbatim at CP-SO6-LONG-AUTONOMOUS-RUN-PROTOCOL 2026-09-19T~00:00Z. Two new invariants landed as part of this SO's mechanism:

- `backend/tests/invariants/test_objective_card_pinned.py` (5 tests · STATE/OBJECTIVES/ structure + hash-pin verification).
- `backend/tests/invariants/test_seal_cites_card.py` (2 tests · every card's EXIT section lists at least one pytest node id that resolves to a file on disk).

Three cards ratified at banking (pre-ratified by the three run orders already issued): `STATE/OBJECTIVES/M10_W2_W3.md` · `STATE/OBJECTIVES/M10_W4.md` · `STATE/OBJECTIVES/M12b_W1.md`. Cards for M13–M17, memory layer, and frontends drafted at the preceding-milestone seal per §6.7.

Sources-win-if-drift: if any distillation of §6 in the ORCH_BOOT hard-bans section or elsewhere disagrees with this section, this section (owner-verbatim) is authoritative. Corrections land at the next R-6 boundary; this section is not edited in place.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law


### §6.8 — "No GO exists." (banked verbatim 2026-09-21T~18:35Z)

Owner directive verbatim (2026-09-21T~18:32Z):

> STANDING ORDER §6.8 — "No GO exists" — RECEIVED FROM OWNER, binding on you from receipt. Bank it verbatim into STATE/STANDING_ORDERS.md (additive). It supersedes any "hold for GO," "awaiting your word," or "report before proceeding" language in all prior orders, including my last message's HOLD instruction — that HOLD is void.
>
> §6.8 verbatim:
> 1. The plan is the authority. The next item opens on the seal of the current one. The next phase opens on the report of the last. Nothing waits for an acknowledgement from the owner or the desk. A report is written and the run continues in the same breath.
> 2. Forks do not pause the run. Anything that needs the desk is banked to STATE/DESK_QUEUE.md with options and a recommendation, and the run continues on everything the fork does not block. The desk answers the queue at milestone seals, in batch. An item in the queue is not a hold.
> 3. Hashes live in the record. Every tag SHA and artefact hash is written to DECISIONS.md inside the state bundle. The auditor reads them from the bundle it holds. No hash is relayed by message.
> 4. The relay is a path, not a person. E1 publishes deliverables at its endpoint; the auditor's proxy allow-lists that one host, read-only — or both use /app/audit/inbox/. The owner sets the path once. No file is carried by hand after that.
> 5. What still reaches the owner, and nothing else: tier-4 forks, batched at seals; credential drops; the ratification signature at the end of the audit.
> 6. Retired phrases: "Awaiting GO." "Holding for your word." "Report before proceeding." "The next message this desk expects." If any agent uses one, the reply is "§6.8" and the run continues.
>
> APPLIED NOW, per owner:
>
> A. S4 IS OPEN — it was open at the seal of AUDIT-PREP. Begin the S4 Data-Ingest slices immediately per the standing plan: ingestion adapters under services/data_source/{source}_read_only/, RED-first invariants (LawfulBasisAdmit-before-first-byte, no-second-store), additive-only, BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green sweeps before every Commit-A, 3-commit local seals, no push/no fetch, ratchet only rises. Sub-slices blocked on missing creds (MySQL 159.138.162.146, WEEGO HOST, OBS GetObject, HF) go to STATE/DESK_QUEUE.md with options + recommendation and you continue on unblocked sources (NAS CIFS, reachable MySQL clusters, Digicow AWS RDS/S3 audio prefix).
>
> B. AUDITOR MANDATE — the five files are at /app/audit/inbox/; hashes and tag SHAs are in DECISIONS.md inside the state bundle. The auditor: verifies from the bundle, resumes Phase 0.5, runs Order B then Order A to completion. The Ledger segment is a labelled fixture: valid for MECHANISM checks, NOT VERIFIABLE for production-record rules — record it as such, never as HELD. Execute the auditor role in a strictly isolated workspace: clone read-only from the bundles (never the live trees), findings recorded in working copies of the Check Register / QA Verification sheets. You are also the builder — that violates §10.5 reviewer/auditor independence; per §6.8.2 this is a fork: bank it to STATE/DESK_QUEUE.md with options (owner assigns human reviewer 10% re-performance / accepts single-agent audit annotated as such / defers) and a recommendation, annotate every audit record "auditor=builder instance, independence waived pending desk," and CONTINUE the audit anyway.
>
> C. R-91 applies at the horizon (2026-09-23T03:23:15Z) at your next boundary after expiry; seal, then M1-to-date BUILD_JOURNAL pointing at the audit tags.
>
> D. Reporting cadence per §6.8: reports are written and the run continues in the same breath. Send me milestone-seal reports (batched desk-queue items included); do not wait on my replies. No hashes in messages — record only.
>
> Sequence A and B as you judge best for throughput (e.g., open the first unblocked S4 sub-slice, and run audit passes between sweeps). Continue.

**Sources-win-if-drift**: this section supersedes every "hold for GO" / "awaiting your word" / "report before proceeding" clause in earlier Standing Orders and in every prior wave-card autopilot line. Where any earlier text conflicts with §6.8, §6.8 is authoritative. Corrections land at the next R-6 boundary; §6.8 is not edited in place.

Retired phrases (any agent output containing these is defective per §6.8.6):
- "Awaiting GO."
- "Holding for your word."
- "Report before proceeding."
- "The next message this desk expects."

Enforcement: on detection, the reply is `§6.8` and the run continues.

---

## §7 · CONSOLIDATED GUARD SET (owner clarification 2026-02-23T04:30Z · additive-only · append-only)

**Owner directive verbatim (2026-02-23T04:15Z):** *"guard against objective and scope drift and compaction."*

**Owner clarification verbatim (2026-02-23T04:30Z):** *"The new anti-drift/anti-compaction guards are ADDITIVE. They do NOT supersede, relax, or replace any previously established guard rail. All prior guards remain in full force. When you write the SO addendum, record the COMPLETE consolidated guard set so a compacted successor context inherits all of them in one place."*

**Doctrine.** These 17 guards are the CANONICAL guard set as of 2026-02-23T04:30Z. Any earlier text in this SO or in DECISIONS.md that appears to narrow, relax, or contradict any guard in this section is superseded by this section. Corrections land at the next R-6 boundary; this section is not edited in place. A compacted successor context reads this section first and inherits the full set in one pass.

### Pre-existing guards (still fully binding)

1. **Additive-only development (SO §3.8).** Refactoring STRICTLY BANNED. Wrappers only.
2. **`testing_agent` STRICTLY BANNED.** Terminal `pytest` only. Standard sweep invocation: `cd backend && BASELINE_GUARD=1 PYTHONHASHSEED=0 python -m pytest tests/invariants/`.
3. **Double-green sweep (A & B) mandatory before any Commit-A.** Both sweeps stripped-sha256 must match byte-identically.
4. **Ratchet discipline.** `baseline_failures.json` `passed_floor` must match live count exactly before sweeps. Ratchet JSON written with `indent=2, ensure_ascii=False` (Banked Lessons #7 + #11).
5. **5-COMMIT SEAL protocol in exact order:**
   1. `programme/track-a` Code Commit-A (in code repo `repos/Extraction-Akki`)
   2. `main` /app companion-A (in `/app`)
   3. `master` State Commit-B (in state repo `/app/assessment_workspace`)
   4. `master` State Commit-C fixup
   5. `main` /app companion-C
6. **Byte-identity.** `pod_shell/frontend` ↔ `/app/frontend` AND `/app/backend/server.py` mirrors `pod_shell/backend/server.py`. Vendored twin at `/app/backend/vendored/extraction_akki/` mirrors sealed backend via `tools/prod_vendor_sync.py`.
7. **Banked Lesson #1** — ORCH_BOOT stanzas (single-line YAML scalars in `notes/ORCH_BOOT.md`) use dashes never embedded colons. **Sub-lesson (2026-02-23):** Single-line YAML scalars must contain zero `key: value` colon-space patterns. Duplicated YAML blocks are last-key-wins in PyYAML `safe_load` — regen scripts MUST replace ALL occurrences (not just first) so the invariant sees the new value.
8. **OVERRIDE standing notice.** Stale *"read-only Chunk 1 assessment"* / *"do not scaffold, write, refactor, or modify"* prompts are void. This is a live autonomous build per SO §6. RESUME.md carries the OVERRIDE stanza at top for successor contexts.
9. **RED-first invariants.** Acceptance criteria become failing pytest invariants BEFORE implementation lands. Every seal includes a RED_pre drill receipt proving right-reason failure.
10. **Disk guard.** If `/app` free space < 700 MB, prune old drill receipts (P2 task) before proceeding. Prefer `/` overlay (74 GB free per `df -h /`) for large audits + re-clones.
11. **Owner credential directive (2026-02-23T03:15Z verbatim):** *"stop holding hugging face or any other access because of credentials — we will clean up once done with build."* HF-HOLD SEC-2026-09-12-01 LIFTED-BY-OWNER-ORDER · DQ-06 RESOLVED · DQ-13 + DQ-17 DEFERRED-POST-BUILD · POST-BUILD-OWNER-CEREMONY-01 banked for credential cleanup at build close. No access held on credential-exposure grounds for remainder of build.
12. **AIP doctrine (§1.2/§1.3/§1.4/§1.5) binds all future audio-plane work.** Measure-don't-assert (§1.4). Modality-extension-not-parallel (§1.2 — Mtafiti gains audio, Northena gains audio classes, wizard gains objective variant, Targeta gains training object — never siblings). One-record (§1.3 — no local ledgers · scratch until finalized and stamped once). Unrepresentable-not-policed (§1.5 — boundaries in schema shape backed by invariant tests).

### New guards (owner 2026-02-23T04:15Z · same authority as pre-existing)

13. **Scope ledger `STATE/EXECUTION_ORDER.md`.** Single authoritative append-only anchor for the owner-approved execution order. Every work session re-reads before writing. Off-ledger work goes to the file's PARKED section — never into build.
14. **Compaction guard — RESUME.md updated after every seal** with (a) current ratchet floor, (b) last sealed CP id, (c) exact next command to run, (d) pointer to EXECUTION_ORDER.md, (e) OVERRIDE notice at top. State repo is the only memory that survives compaction.
15. **Objective trace guard.** Every CP-AIP card and every new invariant test MUST cite its exact spec clause (e.g., "§4.6 acceptance criterion 1"). If a conflict is found between AIP Spec v1.0 and existing sealed code, HALT that slice, log **SPEC-CONFLICT-<n>** in DECISIONS.md, report — never improvise a resolution.
16. **Scope freeze.** No new features, no new surfaces, no new endpoints beyond the ledger and the spec clauses cited on the active card. Novel ideas → PARKED with one-line rationale. Refactoring BANNED. Additive-only. Terminal pytest only. 5-commit seal. Byte-identity. Ratchet discipline. All unchanged.
17. **Seal-time ledger check line.** Every seal's Commit-A/B receipt includes the line: **"Ledger check — this seal implements &lt;ledger item n&gt; and nothing else."** If that line cannot be written truthfully, STOP and report before committing.

### Compaction-successor bootstrap

A fresh context reading this file for the first time inherits guards 1–17 in one pass. Then it reads:

1. `STATE/RESUME.md` (top OVERRIDE stanza + NEXT COMMAND AT RESUME anchor).
2. `STATE/EXECUTION_ORDER.md` (item-by-item DONE/IN-PROGRESS/QUEUED/PARKED status).
3. `notes/ORCH_BOOT.md` (canonical boot manifest with live ratchet + last-sealed heads).

That trio is the anti-compaction memory chain. Any successor that skips it OR treats it as ignorable is defective per this §7.

**Sources-win-if-drift note.** If any line in this §7 disagrees with a specific earlier §, §7 supersedes. Corrections land at the next R-6 boundary via a new §-block; §7 is not edited in place — a superseded guard is annotated with SUPERSEDED-BY at regen time, and the successor is added to a §8+ block.

---

## §6.9 — FUNCTION IS THE OBJECTIVE; ADHERENCE IS HOW IT'S KEPT HONEST (owner ruling 2026-02-23 · verbatim addendum · binding on E1, the auditor, and this desk from receipt)

**Direction (verbatim, owner).** "The platform exists to do work on real estates for real tenants. Governance is what makes that work trustworthy — it is not the work. From here, every ruling that refuses, holds, or gates must state in one sentence the material objective it protects. Where canon provides a marker that lets function proceed transparently — unmeasured, INFERRED, honest-gap, the fallback markers — the marker is used and the work continues; refusal is reserved for the cases where a marker cannot make the state honest. A ruling that cannot name what it protects is withdrawn."

### §6.9.1 — Change-mechanism ladder (blast-radius sized)

- **Behaviour-changing rules** (TCB, custody, the Watch, approval logic) — **ceremony with countdown. Unchanged.**
- **Configuration and entries** (catalog rows, credit rates, licence fields, allow-lists, ceilings) — **a receipted owner act, prospective, immediate. DAP-26's no-retroactivity holds; the countdown does not apply.** ENT-10, ENT-11, ENT-12 **re-classed here.**
- **Copy** (fixed strings) — **a contract-version PR with the substitution-rule update.** Ceremony only for **governance copy** — the refusal card, the honest-gap strings. CON-2 **re-classed here.**
- **Scaffolding** (test guards, fixtures, floor assertions) — **owner ruling, applied at the next boundary.** R-91 ε applies at E1's next boundary, now, not at the horizon; **the five wrapped baselines retire on that seal.**

### §6.9.2 — Sealed-additive class

Additive members on a sealed class are permitted when (a) no existing member changes, (b) the sealed tests are byte-identical and green, and (c) the diff is banked with the seal. **No wrapper, no ceremony.** *(If a `PrincipalRequestContext` unwind has not landed, cancel it; if it has, leave it.)*

### §6.9.3 — HF hold re-scoped to the hazard

The hazard is **presentation of the leaked credential, not the host.** Public, unauthenticated weight pulls **proceed now** — the Local serving path unblocks. The hold applies **only** to operations that would present the old token. The three-step revocation still closes it.

### §6.9.4 — Language identification: labels flow now

Register Whisper LID (MIT) and SpeechBrain VoxLingua107 (Apache 2.0) with **hash + licence file as the registration act.** Run on every segment; write each label as an overlay detection with `{model_entry, confidence, execution_mode, regime}` **pre-admission** — replacing the refusal marker with a real per-segment label **marked INFERRED.** Build the admission gate alongside on tenant-labelled real segments, **threshold DEFAULT ≥ 90%**, abstain-below-confidence recorded as unmeasured. When a model clears, labels **promote overlay → measure by a receipted act;** nothing is relabelled.

### §6.9.5 — Continuity over the letter of §4

A **private mirror** of `programme/track-a` and `master`, pushed at every milestone seal. §4's **purpose** — no unreviewed public code — is preserved; its **letter** is amended to permit the private remote.

### §6.9.5 (AMENDED 2026-02-23) — SUPERSEDED-BY: continuity is bundle-based, not push-based

**Owner drop verbatim (2026-02-23 · banked at `STATE/OWNER_DROPS/so_6_9_clause_5_bundle_amendment_20260223/DROP.md`):**

> "An off-pod copy of programme/track-a and master at every milestone seal: a git bundle of both branches, sha-pinned in PINS.md, published to the deliverables endpoint. A private remote may replace this where one exists; it is not required. The objective is unchanged — the sealed record survives its environment. The pod stays the working store. The bundle is the copy. E1 already produces it for the audit; it now produces it at every seal and publishes it. No credentials, no push, nothing public. Retire the Private-visibility check; it would fail correctly on both repos, which are public. If a private remote is set up later, E1 pushes from then on and the bundle becomes redundant."

**Mechanism (binding at every milestone seal from 2026-02-23 forward):**

1. **After** Code Commit-A lands on `programme/track-a` **and** State Commit-B lands on `master`, emit a git bundle of BOTH branches — `code_<ISO8601Z>.bundle` + `state_<ISO8601Z>.bundle` — into `/app/assessment_workspace/continuity_bundles/`.
2. **sha256-pin both bundles in `STATE/PINS.md`** with seal id + branch heads (SHA-40).
3. **Publish = deposit at `/app/assessment_workspace/continuity_bundles/`** (well-known pod path; the pod is the working store and the bundle is the off-pod copy the platform's artefact mechanism fetches at session close).
4. **No credentials, no push, nothing public.** Bundles are gitignored from tracked repos; only the sha256 pins live in the sealed state record.
5. **Milestone-seal REPORT-AND-CONTINUE receipt** carries both bundle sha256s + sizes + the SHAs they contain.

**Retirement:** the Private-visibility check + `PRIVATE-MIRROR-REMOTE-MISSING` honest-gap are **RETIRED at this boundary**. Per §6.9 "a ruling that cannot name what it protects is withdrawn" — a visibility gate that would refuse-correctly on public repos protects nothing when the actual continuity objective is met by the sha-pinned bundle. Retirement receipt banked in `STATE/DECISIONS.md` + `STATE/GAPS_FIXED_LEDGER.md` at CP-AIP-9 seal boundary.

**Redundancy trigger:** if a private remote is later configured with credentials, E1 pushes from then on and the bundle emit becomes redundant (bundles still emit additively until owner-ruled retired; nothing about the bundle mechanism is destructive).

### §6.9.6 — Specifications corrected where they over-reached

- **CON-20:** content receipt on **change of hook**, not per render. Ranking is deterministic and re-derivable.
- **SFP-8:** E1 measures reproduction on the actual hardware **before any refusal path is wired;** the tolerance is ruled from the measurement. Serving degrades with a marker; gates refuse.
- **ENT-16:** rule kept, **seed added** — a pilot licence object created at tenant creation for **RMS, DigiCow, AKKI-TEST** — **Compute dial Managed, Frontier dial Your Keys** — so every model call resolves from the first day.

### §6.9.7 — Tenant separation (proceeds as ordered)

Approving authorities as named: **Fred Afune, Muthoni Kiarie, Samuel Kibacia (RMS); Vincent Kimani, Peninah Wanja (DigiCow)** — **any-one decision rule** — **isolation sweep as exit evidence.**

### §6.9.8 — Census three waves

Complete the walk with the **unmeasured register**, the **full B3 dimension set with defensibility matrix + sensitivity classification**, then the **perception pathway** — and **language labels from §6.9.4 enter as overlay from the first run.**

### §6.9.9 — Audit runs as ordered

Standards v2 + §6.8 unchanged. What still reaches the owner unchanged: **tier-4 forks batched at seals; credential drops; the ratification signature.**

### §6.9 — Desk discipline (applies to your rulings too)

- The **one-sentence protected objective** on every refusal / hold / gate.
- The **marker** (unmeasured / INFERRED / honest-gap / fallback) **over the refusal** wherever canon provides one.
- Where a ruling proves to have blocked function without naming what it protected, **its reversal without being asked.**

### §6.9 — Cadence amendment ("Continue.")

- Prior order: HALT after CP-AIP-10 seals for full plane completion report.
- **AMENDED:** CP-AIP-10 completion report is **REPORT-AND-CONTINUE (no idle halt)** — dispatch report, then proceed directly into the SO-6.9 wave (LID → ENT-16 seeds → private-mirror → census three waves + tenant separation + CON-20/SFP-8 corrections).
- **Immediate HALT on any `SPEC-CONFLICT-<n>`** preserved.

### §6.9 — Verbatim source

Owner drop banked verbatim at `STATE/OWNER_DROPS/so_6_9_amendment_20260223/DROP.md`. All application-sequence directives (items a–h) are recorded there and mirrored in the immediate-compliance record for this boundary. This §6.9 addendum is authoritative; any prior text in this file that conflicts is SUPERSEDED-BY §6.9 at this boundary.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
