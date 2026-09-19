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
generated_at_utc: 2026-09-19T08:56:00Z
generator: main-agent Autopilot (CP-M14-W5-SEAL-INTEGRATION Commit-C fixup R-6 boundary regen · heads_last_sealed.state_repo.head advanced to Commit-B 9e673215 · code_repo.head remains Commit-A 1b019041 · ratchet 5344 · baseline_failures_sha256 03714f66… · MILESTONE 5 FIFTH SUB-WAVE FULLY SEALED · M14 MILESTONE FULLY CLOSED · milestone_status CLOSED · card_sha256 eb3ff591… · post-Commit-C fixup regen)
regeneration_reason: r6-boundary-regen-commit-c-fixup-at-cp-m14-w5-seal-integration-m14-milestone-fully-closed-state-head-advance-to-9e673215

ratchet:
  passed_floor: 5344
  counts_at_baseline_passed: 5344
  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json
  baseline_failures_sha256: 03714f66519f17042f645ae66b9191412f656a8753f61f0c27272aaf1b13e846

heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: 9e6732150a8078b2cf4f9ea66ff975756eabd023
    sealed_at_utc: 2026-09-19T08:54:00Z
    seal_kind: "CP-M14-W5-SEAL-INTEGRATION · state Commit-B `9e673215` · banks Commit-A `1b019041` · MILESTONE 5 FIFTH SUB-WAVE SEALED · M14 MILESTONE FULLY CLOSED · milestone_status DRAFTED → CLOSED · ratchet 5338→5344 · total M14 ratchet 5311→5344 (+33) · card_sha256 re-pinned eb3ff591… reflecting CLOSED state"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: 1b019041d55a1ce2a22c54e08df66d9f5064cec7
    sealed_at_utc: 2026-09-19T08:50:00Z
    seal_kind: "CP-M14-W5-SEAL-INTEGRATION · Commit-A `1b019041` · Milestone 5 FIFTH SUB-WAVE (M14 MILESTONE CLOSING GATE) · Integration seal binding W1..W4 sub-wave surfaces end-to-end per SO §6.2 EXIT clause · NEW tests/invariants/test_m14_w5_seal_integration.py (6 tests including milestone happy-path handoff→admit→ask→confirm→sign→deliver→verify + cross-tenant refusal + dual-hatted refusal + single-writer ledger count + canonical bytes snapshot pin 40af13fe…) · baseline_failures.json 5338→5344 · pre-Commit-A double-green 6892491a… · autopilot R-33"

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
