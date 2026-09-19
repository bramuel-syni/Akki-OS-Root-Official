READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# ORCH_BOOT.md — Anti-forget boot manifest

**Owner ruling (verbatim, 2026-09-17T~20:45Z, banked in STATE/DECISIONS.md):**

> "Add a machine-checkable boot manifest whose ratchet field can never
>  silently drift, and whose HEAD fields cannot race with the §3.3 commit
>  protocol.  This file MUST be regenerated at every seal boundary (R-6)."

This file is the CANONICAL boot state for the orchestrator.  A byte-identical
downloadable copy is served at `/app/frontend/public/audit/ORCH_BOOT.md`.

The invariant test at
`repos/Extraction-Akki/backend/tests/invariants/test_orch_boot.py` enforces:

1. Both copies exist and are byte-identical.
2. `ratchet.passed_floor` equals live `baseline_failures.json.passed_floor`
   (drift-and-burn priority guard · always-on hard assertion).
3. `ratchet.baseline_failures_sha256` equals live sha256 of that file
   (paired byte-fingerprint · always-on hard assertion).
4. `heads_last_sealed.*.head` are well-formed 40-hex AND banked in
   STATE/DECISIONS.md or STATE/NEXT.md (last-sealed HEADs, NOT live
   `git rev-parse HEAD` — freshness is enforced by R-6 boundary
   regeneration, not by an always-on equality-to-live-HEAD test, per
   owner ruling refinement to avoid racing §3.3 Commit-A/B/C ordering).

Regenerate this file (both copies, byte-identically) at every §3.3
Commit-C fixup, at every owner ruling that mutates ratchet / HEADs /
STATE files, and on any boot ritual that detects drift.

---

```yaml
schema_version: 1
generated_at_utc: 2026-09-19T15:42:00Z
generator: main-agent Autopilot (CP-M17-W5-SEAL-INTEGRATION Commit-C fixup · state master · MILESTONE 8 FIFTH SUB-WAVE FULLY SEALED · MILESTONE 8 (M17 · Tenant Apps + Personal Client · C.23) FULLY CLOSED with one structural fork banked · banks Commit-B `8910ba9b53862b153a76cb11ddb5f5dc40ebd2bb` · state_repo.head advanced `40454bf8` → `8910ba9b` · code_repo.head remains `e3767b93f3fe14208f5ee9972fcab7081a818f35` on programme/track-a · ratchet 5452 unchanged at Commit-C · baseline_failures_sha256 `e51fc7bf70cae4510f4e28cc42756543f6d57146e9d1801dc81265e1ee665077` unchanged · owner Option-1 override banked this session 2026-09-19T11:29Z + owner PROCEED re-affirmed 2026-09-19T~14:35Z · Owner Desk Batch Digest published in this Commit-C fixup per M16 close discipline)
regeneration_reason: r6-boundary-regen-post-commit-c-fixup-at-cp-m17-w5-seal-integration-milestone-8-fifth-sub-wave-fully-sealed-milestone-close-with-fork-banked-and-owner-desk-batch-digest-published

ratchet:
  passed_floor: 5452
  counts_at_baseline_passed: 5452
  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json
  baseline_failures_sha256: e51fc7bf70cae4510f4e28cc42756543f6d57146e9d1801dc81265e1ee665077

heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: 8910ba9b53862b153a76cb11ddb5f5dc40ebd2bb
    sealed_at_utc: 2026-09-19T15:34:00Z
    seal_kind: "CP-M17-W5-SEAL-INTEGRATION · state Commit-B `8910ba9b53862b153a76cb11ddb5f5dc40ebd2bb` · banks Commit-A `e3767b93f3fe14208f5ee9972fcab7081a818f35` · MILESTONE 8 FIFTH SUB-WAVE · MILESTONE 8 (M17 · Tenant Apps + Personal Client · C.23) FULLY CLOSED with one structural fork banked · lands STATE/OBJECTIVES/M17.md W5 EXIT fill + milestone_status DRAFTED → CLOSED-WITH-FORK-BANKED + card_sha256 re-pin `18f8b942…` → `81ef46d46eb1b7e927294306abef8e6433464d3801974a4e7e7ab4f98fadd50b` + STATE/DECISIONS.md Commit-A banking section + STATE/NEXT.md §6 INTERLUDE MARKER R-55 + notes/M17_W5_HANDOFF_ID_MISMATCH_FORK_20260919.md fork-banking doc + notes/ORCH_BOOT.md R-6 boundary regen advancing code_head to Commit-A + audit copy re-sync · additive-only per SO §3.8 · ratchet 5452 unchanged at Commit-B (state files + fork-note only)"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: e3767b93f3fe14208f5ee9972fcab7081a818f35
    sealed_at_utc: 2026-09-19T15:33:00Z
    seal_kind: "CP-M17-W5-SEAL-INTEGRATION · Commit-A `e3767b93f3fe14208f5ee9972fcab7081a818f35` · MILESTONE 8 FIFTH SUB-WAVE · M17 milestone closing gate · MILESTONE 8 (M17 · Tenant Apps + Personal Client · C.23) FULLY CLOSED with one structural fork banked · integration seal binding W1..W4 end-to-end + milestone snapshot pin over ApplicationContract_v0.model_json_schema sha256 `ba1957dfbb38ba037ec6a57c52760f053e829451ccf6ee9c12b48ef4498b8d05` per SO §6.2 EXIT clause verbatim + all W1..W4 canon anchors preserved + SO §3.10-α + R-21 STATE/DECISIONS.md:12333+12366 + B-frontends-Q1 STATE/DECISIONS.md:12115 + M14-W4 pure-data-in + Canon 8 §W11 + M14-W2/W3 seam + M11 per-tenant DB discipline + SO §3.8 + SO §6.4 + SO §6.7 batch-ratification · new backend/tests/invariants/test_m17_w5_seal_integration.py (498 lines · 7 integration tests + `_FakeRepository` fake + factory helpers) · no new production module at W5 · baseline_failures.json ratchet bump 5445 → 5452 (+7) · AUTHENTIC RED-first cycle: RED v1 with Stop-condition #1 triggered + fork banked at notes/M17_W5_HANDOFF_ID_MISMATCH_FORK_20260919.md + tests 2 + 6 adjusted to AST-scan · RED v2 fork-adjusted · GREEN post-pin · pre-Commit-A double-green BASELINE_GUARD=1 stripped-sha256 `dfed12cd339b47a0f15b7286e677b05c1e280012966b3b388eee6f31f753f4d7` IDENTICAL both runs 5452 passed / 1 skipped / 438 warnings ~171s each against final baseline_failures.json sha256 `e51fc7bf70cae4510f4e28cc42756543f6d57146e9d1801dc81265e1ee665077` · additive-only per SO §3.8 · sealed W1..W4 M17 modules + M14/M11/M12b-W1/M16/W-M2-SW7/W1b-CP4 modules all NOT edited · Stop-condition #1 TRIGGERED at RED v1 · handled per SO §6.7 fork-banking · #2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · milestone_status DRAFTED → CLOSED-WITH-FORK-BANKED at Commit-B · card_sha256 re-pin at Commit-B · Owner Desk Batch Digest published at Commit-C fixup per M16 close discipline · Aggregate ratchet across M17: 5414 → 5452 (+38 · W1 +9 · W2 +7 · W3 +8 · W4 +7 · W5 +7)"

boot_sequence:
  - Read STATE/STANDING_ORDERS.md end-to-end.
  - Read last 300 lines of STATE/DECISIONS.md and all of STATE/NEXT.md.
  - Verify HEADs against `git rev-parse` for informational purposes only — this file's HEADs are LAST-SEALED, not live.
  - Verify ratchet floor + baseline sha256 against baseline_failures.json (hard-asserted by test_orch_boot.py).
  - Resume the in-flight work order at the top of STATE/NEXT.md.

regeneration_triggers_r6:
  - After Commit-C fixup of every §3.3 3-commit seal (CP boundary).
  - After any owner ruling that mutates ratchet, HEADs, or STATE files.
  - On every boot ritual when STANDING_ORDERS §1 boot verification detects drift.

authoritative_downloadable_copy_path: /app/frontend/public/audit/ORCH_BOOT.md
```

---

## HARD BANS / ANTI-DRIFT · plain-language narrative (Q1 · owner ruling 2026-09-18 · additive to R-6 boundary regen)

**Purpose.** A fresh or compacted session reads STANDING_ORDERS.md end-to-end per boot step 1, but this section carries the single-line high-frequency reminders so no critical ban is ever silently forgotten between reads. Sources always win if the summary diverges — every line here cites its authoritative source. If a line here contradicts its source, the source is right; correct this file at the next R-6 boundary.

### 1 · Commit / push discipline

- **Never push. Ever.** Local commits are the record. — *SO §4 · Owner Clarification 1 2026-08-14 · reaffirmed R-18 owner ruling 2026-09-18 Item 4.*
- **§3.3 3-commit seal or it is not sealed.** Commit-A code (`programme/track-a`) · Commit-B state (`master`) · Commit-C fixup (`master`) banks Commit-B SHA into DECISIONS + NEXT + `ORCH_BOOT.md` `heads_last_sealed.state_repo.head`. — *SO §3.3 + SO §7 R-1..R-6.*
- **A CP claimed "sealed" without both SHAs banked is a discipline mislabel.** Reconciliation before forward progress. — *SO §3.3 · Owner ruling 2026-09-15 Discovery-1 ratification.*
- **`pending-C-fixup` count in seal files must be 0.** — *SO §7 R-2.*
- **Every boot ritual runs the master-parity check** (R-1) and the ratchet-history/git-log cross-check (R-3). — *SO §7 R-1, R-3.*

### 2 · Testing discipline

- **Terminal pytest only. `testing_agent` is BANNED.** Curl / `python3 -c` are allowed for spot checks. — *SO §3.*
- **Tests-first mechanical RED before any code lands.** RED receipt banked under `phase0/drill_receipts/`. — *SO §3.*
- **Double-green byte-match to close every CP.** Both `BASELINE_GUARD=1` receipts identical, banked. — *SO §3 + SO §7 R-5 (per-CP raw logs mandatory).*
- **Full `BASELINE_GUARD=1` sweep BEFORE any §3.3 seal that banks rulings.** Targeted invariants supplement, never substitute. — *Owner ruling 2026-09-18 transparency item 1 · pre-seal standard added at ORCH_BOOT R-6 regen for owner-ruling seals + all subsequent seals.*
- **Ratchet floor monotonic-up.** `baseline_failures.json` `passed_floor` + `ratchet_history` append at every close. Silent rebaselining is banned. — *SO §3.*

### 3 · Code / build discipline

- **No refactor. Thin-kernel additive-only.** Sealed modules are not edited; new work extends via thin adapter layer. — *SO §3.8 · Owner ruling 2026-09-17 Tension (a) = Option C.*
- **Zero closed enum type — schema authoritative, Python tuple mirrors.** — *SO §3.10 · Owner ruling 2026-09-17 Tension (b) = Option α.*
- **Order of authority (top→bottom):** canon → Standing Orders → SER → contract schemas → code. — *SO §2.1 · R-18 owner ruling 2026-09-18 effect 1.*
- **T-c sequencing (α):** schema + AST + P-15 land BEFORE M11-W1; caller-flip at M12b-W1; new M11 callers target the new Watch schema from day one. — *Owner ruling 2026-09-18 Item 4.*

### 4 · Silent-success + progress-signal bans

- **ALIVE IS NOT DONE.** Heartbeat / PID / directory / filename presence is NEVER completion evidence. Every seal read routes through `services.output_verified_seal.is_real_seal`. Every seal write emits `Kind:` as first-class body field. — *SO §3.1.*
- **NO RUN WITHOUT A PROGRESS SIGNAL.** Every commissioned run binds `run_id` to `runtime_supervisor` progress-ring. HALT verdicts are DATA, not process-kills. — *SO §3.2.*

### 5 · Verification-walk scope

- **Wave-window commit enumeration on every verification walk.** `git log --format=... <open>..<close_or_next>` — never the canonically-named wave-close commit alone. — *SO §4.2 · Owner ruling 2026-09-16.*
- **Cross-wave modifications** carrying their own CP citation + ratchet delta + owner directive + append-only-extension discipline are NOT drift for the origin wave's walk. — *SO §4.2 Clause 6.*

### 6 · Credential custody

- **PII / credentials: never committed, never returned, never logged, never in test docstrings.** Redacted everywhere. — *SO §4.*
- **§E · Custody-file reads only via shape-only helper OR env-injection.** Direct `cat`/`head`/`tail`/`csv.reader+print`/`openpyxl+print`/`set -x` on a custody path = SEC violation. — *SO §4.1 §E · Owner ruling 2026-09-15T~22:30Z.*
- **§F · Sha-pin every credential drop at intake or refuse.** Manifests at `phase0/credential_drop_manifests/YYYYMMDDTHHMMZ_drop_manifest.json`. Sha-less drops are quarantined at 0600 outside `estate_keys/`. — *SO §4.1 §F · R-18 Part 7(c) · Owner ruling 2026-09-18.*
- **HF token hash-delta gate.** SEC-2026-09-12-01: any HF-touching wave HOLDS until rotation is proven by sha delta ALONE (never by opening the value). Three-step owner action = revoke → generate → re-drop with §F sha-pin. — *SO §4.3 · Owner ruling 2026-09-18.*

### 7 · GPU obligations

- **Full-consumption guarantee.** All 4 GPUs run high-utilization while a campaign window is open. Idle lanes are interrupt-priority. — *SO §5.*
- **Never kill a training run mid-flight.** Ownership passes through the run's `ACTIVITY_SUMMARY.md` seal, never via SIGKILL. — *SO §5.*
- **Idle-lane restoration** uses banked machinery in `tools/queue_followon_launcher.py` + `tools/on_host_queue_dispatcher.py` — no improvisation. — *SO §5.*

### 8 · Canon-before-ruling doctrine

- **No decision proceeds from memory or summary where the governing document exists.** Read the document, don't recall it. Binding on both ruling authority and builder — no exception for either. — *Canon 1 §4.11 · Canon 7 §48 · SO §3.*

### 9 · Standing autonomous-run bounds (from owner ruling 2026-09-18)

- **Item 2 · The measure.** Every task in every chunk names which of R-18 effect-15's gate conditions (errata landed · Watch contract schema · AST + P-15 green · `canon_ref` check active · D-16..D-19 banked) it feeds or is deferred. That is the only test of movement vs circling.
- **Item 3 · Standing authority.** Autonomous from CHUNK 1 close through Q1 → Q2 → M11-W1 → M12b-W1, subject to Items 4–5. Checkpoints = reports, not holds.
- **Item 6 · SEC-2026-09-12-01** stays owner-only. HF-touching waves HOLD; everything else proceeds.
- **Item 7 · Reporting.** Chunk-close: six-item summary + gate conditions advanced + ratchet + open forks. Gate-release: R-18 effect-15's conditions each with evidence. No other reports.

### 10 · Stop-and-report conditions (from owner ruling 2026-09-18 Item 5)

Fail closed on the affected fork, present options with a recommendation, continue on everything else. Do not hold the whole build on one fork. Triggers:

1. **RED ratchet or failed invariant.**
2. **Canon vs lower-layer conflict discovered.**
3. **Any proposal to amend canon, add a TCB member outside `tcb_enumeration_v1`'s method, change a Fixed decision-register entry, or carve an exception to a hard invariant.**
4. **A new rule-vs-rule tension of the T-a/T-b kind.**

### 11 · Assessment / read-only chunk discipline (from client instruction doc · Chunk-1 scope)

- **No production/application code during ingest+ground-truth chunks.** Only markdown notes under the chunk's `notes/chunk*_YYYYMMDD/` folder + throwaway analysis scripts under `/app/assessment_workspace/tools/`.
- **Every factual claim must come from files opened this session.** Never from a README, a filename, or prior knowledge.
- **Never merge two repos' same-named services in-head.** They are different until diffed.
- **Absence is a finding.** Report it explicitly, never leave a blank.
- **BUILD_JOURNAL / close reports are claims to verify later, not findings.**
- **Do not propose sequencing, phases, or build order.** — *D7 (Canon 7 §47) · client's binding rule.*

### 12 · Defect classes (from Canon 7 §47) — reportable on sight by anyone

- **D1** · orphan gate (function with no honest promise or service trace).
- **D2** · NL-only enforcement (rule with no machine-checked twin).
- **D3** · curated verdict (validation material selected by favourability).
- **D4** · rung inflation (model-ladder placement above cheapest-sufficient with no written justification).
- **D5** · meta-spiral (second governance layer above one that exists; artefact stopped paying rent).
- **D6** · service conflation (function optimised for end-user persona rather than service sentence).
- **D7** · invented schedule/scope (sequencing without explicit instruction).
- **D8** · dual-identity execution (task or code path spanning >1 authority's identity/scope within a single execution).

### 13 · Watch doctrines (from Canon 8 §4) — 14 hard bans on the security authority

W1 eyes-never-act/hand-never-judges · W2 certainty-never-exceeds-evidence (signature-as-guard) · W3 every-autonomous-act-reversible-bounded-witnessed (destroy does not exist) · W4 deployed-in-force-never-in-shadow · W5 one-record-two-readings · W6 suspicion-refined-not-accumulated · W7 conformance-grants-trust/non-conformance-never-convicts · W8 the-floor-never-learns · W9 no-actor-enters-undeclared · W10 watcher-watched-from-outside · W11 one-task-one-identity · W12 peer-not-subordinate · W13 profile-is-armory-not-inventory · W14 self-proving-or-not-in-force.

### 14 · Structural-impossibility doctrine (from Canon 1 §4.2)

**Unrepresentable, not policed.** Where a state must never occur, the system is built so the state cannot be expressed (function signature, type, schema). Reviewed prohibitions are eventually violated; structural impossibility beats vigilance.

### Sources-win-if-drift note

If any line above disagrees with its cited source, the source is authoritative. This section is a distillation for boot-ritual convenience — never a replacement for reading `STANDING_ORDERS.md`, the referenced canon sections, or the DECISIONS entry for the specific owner ruling. Corrections land at the next R-6 boundary regen; this section is not edited in place — a superseded line is annotated with SUPERSEDED-BY at regen time, and the successor is added.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
