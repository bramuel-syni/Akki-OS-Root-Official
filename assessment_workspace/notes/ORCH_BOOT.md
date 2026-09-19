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
generated_at_utc: 2026-09-19T20:55:00Z
generator: main-agent Autopilot (CP-MEMORY-COMPACTION-V1-W3-TCB-REGISTRATION Commit-C fixup · state master · advances state_repo.head `36357003b01cb963d2cf01c0a30f63797c0688b2` → new Commit-B `9092674d07931f3b7ab04188ce71f40a19c1cf90` · code_repo.head stays at Commit-A `ebebc46f75494dbaa16efacd7b077c47afcb69f1` · ratchet 5485 unchanged · marker R-63 flips ⏳→✅ · MEM-R-053 CROWN BAN NOT triggered · owner OPTION 1 verbatim + owner CLARIFICATION verbatim · W3 FULLY SEALED · W4 opens next · staleness clock T-~14.8h)
regeneration_reason: r6-boundary-regen-post-commit-c-fixup-at-cp-memory-compaction-v1-w3-tcb-registration-advancing-state-head

ratchet:
  passed_floor: 5485
  counts_at_baseline_passed: 5485
  baseline_failures_path_rel: repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json
  baseline_failures_sha256: b3705ed9bc782ce8e6baa4fa794dada7bb8d1e103dfbf92d0d6649182cd26b84

heads_last_sealed:
  state_repo:
    workdir: /app/assessment_workspace
    branch: master
    head: 9092674d07931f3b7ab04188ce71f40a19c1cf90
    sealed_at_utc: 2026-09-19T20:55:00Z
    seal_kind: "CP-MEMORY-COMPACTION-V1-W3-TCB-REGISTRATION · state Commit-B `9092674d07931f3b7ab04188ce71f40a19c1cf90` · banks Commit-A `ebebc46f75494dbaa16efacd7b077c47afcb69f1` · memory-layer follow-on wave W3 · owner OPTION 1 ratification 2026-09-19T~20:20Z verbatim + owner CLARIFICATION 2026-09-19T~20:35Z verbatim · state-side landing includes STATE/DECISIONS.md Commit-A banking section (W3 scope + owner OPTION 1 + owner CLARIFICATION + amendment method verification per module docstring line 24 + files landed + RED/GREEN receipts + pre-Commit-A double-green byte-identical + transparency banking of ensure_ascii=False intermediate + canon anchors MEM-2/MEM-3/MEM-7 + Spec §4 Table 3 + tcb.py docstring line 24 + Doc-0 Attribute 1 + Canon 8 §W11 + SO §3.8 + SO §6.4 NOTHING-BEYOND + M16 R-3 precedent + owner rulings + Stop-conditions NOT triggered + autopilot next W4 → CCS1/CCS2/CCS3 → HALT before frontends) + STATE/NEXT.md R-63 marker + notes/ORCH_BOOT.md R-6 boundary regen advancing code_head to Commit-A + audit copy re-sync byte-identical · additive-only per SO §3.8 · ratchet 5485 unchanged at Commit-B state files only Commit-A carried the +3"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: ebebc46f75494dbaa16efacd7b077c47afcb69f1
    sealed_at_utc: 2026-09-19T20:50:00Z
    seal_kind: "CP-MEMORY-COMPACTION-V1-W3-TCB-REGISTRATION · Commit-A `ebebc46f75494dbaa16efacd7b077c47afcb69f1` · memory-layer follow-on wave W3 · owner OPTION 1 ratification 2026-09-19T~20:20Z verbatim ('W3 (TCB registration): strictly via tcb_enumeration_v1's method — MEM-3 retention engine IN, MEM-7 reload verifier IN, drafting component OUT. Additive edit to the enumeration per its own amendment rules; cite the ingest directive in the seal.') + owner CLARIFICATION 2026-09-19T~20:35Z verbatim ('MEM-3 retention rule engine IN, MEM-7 reload verifier IN, drafting component OUT — these are the owner's INGEST directive classifications verbatim. tcb.py is a sealed W-M2-SW7 module — verify the enumeration's own amendment method permits additive entries without editing sealed logic (M16 precedent: R-3 2026-09-09 enumeration banking handled cif entries — check how that landed and follow the same shape).') · new backend/tests/invariants/test_memory_compaction_v1_w3_tcb_registration.py (3 tests: MEM-3 IN + MEM-7 IN + MEM-2 OUT · is_in_tcb() semantics + entry uniqueness + reason-cites-canon-anchor) · additive edit backend/services/doc0_attributes/tcb.py::_TCB_ENTRIES appending 3 TCBEntry tuple entries (component_ids mem.retention_engine + mem.reload_verifier + mem.drafting_component matching dotted-notation convention of existing entries) · ADDITIVE AMENDMENT PER MODULE DOCSTRING LINE 24 VERBATIM: 'Seeded from tcb_enumeration_v1 + R-3 ratification. Additive: any future ratification appends a new entry.' — no ceremony required beyond tuple append; matches M16 R-3 2026-09-09 precedent shape (Mkono IN + Grey Mirror OUT pure-tuple-append) · sealed W-M2-SW7 logic NOT edited: TCBEntry pydantic model unchanged · get_tcb_current() unchanged · is_in_tcb() unchanged · TCB_VERSION unchanged · module docstring unchanged · baseline_failures.json ratchet 5482 → 5485 (+3 exactly · zero wizard trigger since not a contracts/*.py file) · AUTHENTIC RED-first: RED at drill_receipts/20260919T203612Z (3/3 fail right-reason) → GREEN at drill_receipts/20260919T203633Z (3/3 pass · 0.75s) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 `5b4ec526cd517afd1bacf829edbc5f81a88c485839a0b3896e0179bcf333dc52` IDENTICAL across drill_receipts/20260919T204630Z_run1 + 20260919T204933Z_run2 (both 58452 bytes raw · 58445 bytes stripped · 5485 passed/1 skipped/438 warnings · ~175s each) against FINAL baseline_failures.json sha256 `b3705ed9bc782ce8e6baa4fa794dada7bb8d1e103dfbf92d0d6649182cd26b84` · transparency banking: earlier pair drill_receipts/20260919T203803Z_run1 + 20260919T204107Z_run2 was against an intermediate baseline_failures.json content (Python json.dump ensure_ascii=False mistake produced sha256 a7fc2320 · fully reverted via git checkout and re-authored with ensure_ascii=True to preserve Unicode escape encoding · test outcomes identical · stripped-sha256 identical across all 4 runs) · additive-only per SO §3.8 · sealed services/doc0_attributes/tcb.py::TCBEntry model NOT edited · sealed method logic NOT edited · sealed services/memory/compaction_v1/* NOT edited · sealed M10-W4e memory modules NOT edited · sealed M14/M11/M16/M17/W-M2-SW7/W-7bB modules all NOT edited · Canon anchors verbatim: MEM-2 [Doc 4 A2 A5.5 C.19 I-2] + MEM-3 [Attribute 10 A5.5 Doc 5 objective freeze] + MEM-7 [SFP-8 FP-2] + Spec §4 Table 3 (TCB additions IN/OUT verbatim) + tcb.py docstring line 24 amendment method verbatim + Doc-0 Attribute 1 TCB definition + Canon 8 §W11 structural role separation + SO §3.8 thin-kernel additive-only + SO §6.4 NOTHING-BEYOND (scope frozen at 3 entries) + M16 R-3 2026-09-09 precedent shape + owner MEMORY GO ruling verbatim + owner OPTION 1 ratification verbatim + owner CLARIFICATION verbatim · Stop-conditions NOT triggered · MEM-R-053 CROWN BAN NOT triggered"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: 67b5e070e017ecbbd8645df87d42966721fa082d
    sealed_at_utc: 2026-09-19T20:22:00Z
    seal_kind: "CP-MEMORY-COMPACTION-V1-W2-HARD-BANS-GREP-NEGATIVE · Commit-A `67b5e070e017ecbbd8645df87d42966721fa082d` · memory-layer follow-on wave W2 · owner OPTION 1 ratification 2026-09-19T~20:20Z verbatim (W2 grep-negative hard bans as invariants via AST/grep-negative over backend/**/*.py per ingest directive · summarise-with-model-delete-original convergence ban is crown one · STOP not test tweak if triggered) · new backend/tests/invariants/test_memory_compaction_v1_hard_bans_grep_negative.py (6 grep-negative tests MEM-R-048..MEM-R-053 · scanner + regex helper · scope backend/**/*.py excluding tests + compaction_v1 + phase0 + __pycache__) · baseline_failures.json ratchet 5476 → 5482 (+6 exactly · zero wizard trigger) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 `edb0d556398107f1683a000b92552f9f09361adb1d01be31fd79fdb8cd75af55` IDENTICAL across drill_receipts/20260919T201614Z_run1 + 20260919T201953Z_run2 · additive-only per SO §3.8 · Canon anchors MEM-R-047..MEM-R-053 + Canon 8 §W11 + SO §3.8 + SO §6.4 NOTHING-BEYOND · MEM-R-053 CROWN BAN NOT triggered"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: b1d1183674856c99e85d64b4fbd22a1508ffc4c9
    sealed_at_utc: 2026-09-19T19:57:00Z
    seal_kind: "CP-MEMORY-COMPACTION-V1-BUILD-WAVE · Commit-A `b1d1183674856c99e85d64b4fbd22a1508ffc4c9` · MEMORY LAYER FIRST BUILD WAVE · owner MEMORY GO ruling banked verbatim · new backend/services/memory/compaction_v1/ sub-package (7 files) matches c13_scope precedent · new test_memory_compaction_v1_property_tests.py (7 property tests) · baseline_failures.json ratchet 5469→5476 · pre-Commit-A double-green byte-identical stripped-sha256 03aace2f · additive-only per SO §3.8 · Canon anchors MEM-1..MEM-11 + Spec §2/§4/§5/§7 + Canon 3 §9.3 + Canon 8 §W11 + Canon 4 §22 + SO §3.10-α + SO §3.8 + SO §6.4 · Stop-conditions NOT triggered"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: f57f6c68e765096bd8bc69f8fbfdf96679e5280a
    sealed_at_utc: 2026-09-19T19:05:00Z
    seal_kind: "CP-M17-W6-HANDOFF-ID-ADAPTER-AND-TYPE-TAG · Commit-A `f57f6c68e765096bd8bc69f8fbfdf96679e5280a` · M17-W5 STRUCTURAL FORK CLOSED · owner ruling 2026-09-19T~17:54Z Owner Desk Batch item (f) verbatim ratifying scope (`Handoff-ID adapter + ID-domain type-tagging (ho_ slot rejects non-ho_ prefixes, tests first)`) · Option (i) additive-adapter extension per M17_W5_HANDOFF_ID_MISMATCH_FORK doc verbatim · new backend/services/personal_client/handoff_binding.py (5-surface: HandoffId str-subclass type-tag with ho_ slot regex-enforcing __new__ + HandoffIdRefused + HandoffBindingRefused fail-closed sentinels + derive_handoff_id deterministic pure-data-in adapter mapping pcs_<suffix>→ho_<suffix> + emit_ask_with_handoff seam-routing wrapper delegating to sealed M14-W3 insert_ask under caller-supplied M11 t_<tenant_id> repository) · new backend/tests/invariants/test_m17_w6_handoff_binding_adapter_and_type_tag.py (7 tests: module_surface + derive_handoff_id_deterministic + derive_handoff_id_rejects_non_pcs + handoffid_class_rejects_non_ho + emit_ask_with_handoff_routes_where_sealed_fails + AST_bans_decision_write_surface + AST_zero_import_m17_w3_and_learned_surfaces) · baseline_failures.json ratchet 5462→5469 (+7 exactly · zero wizard trigger since not a contracts/*.py file) · AUTHENTIC RED-first at drill_receipts/20260919T184633Z (7/7 fail right-reason ModuleNotFoundError) → GREEN at drill_receipts/20260919T184858Z (7/7 pass · 0.77s) · pre-Commit-A double-green byte-identical BASELINE_GUARD=1 stripped-sha256 `00a516263feb56c9495080b671efe06a9693c4eda4684191fc2bdf7cbebe9843` IDENTICAL across drill_receipts/20260919T185617Z_run1 + 20260919T185924Z_run2 (both 58129 bytes · 5469 passed/1 skipped/438 warnings · ~168s each) against final baseline_failures.json sha256 `cb15b9803afb33e738e87ba7de9531bd1ef49e3828215adf551ba00905ea2360` · additive-only per SO §3.8 · sealed M17-W3 session.py NOT edited (thin-adapter discipline · adapter is new authoritative runtime path per fork Option (i) verbatim) · sealed M14-W3 asks.py NOT edited (consumed via identity import) · sealed M17-W1/W2/W4/W5/M14/M11/M16/W-M2-SW7/W-7bB modules all NOT edited · Canon 8 §W11 structural role separation AST-enforced · Canon 5 interface architecture · Canon 4 §22 rung-1 discipline · Canon 3 §9.3 append-only · AC-18 · R-21 · HR-2 · SO §3.10-α · SO §6.4 NOTHING-BEYOND · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · M17 milestone_status CLOSED-WITH-FORK-BANKED → CLOSED at Commit-B via M17.md update (fork closed on seal per owner ratification) · notes/M17_W5_HANDOFF_ID_MISMATCH_FORK_20260919.md status flips OPEN-OPTION-(ii)-APPLIED → CLOSED-BY-M17-W6-OPTION-(i)-LANDED at Commit-B"
  code_repo:
    workdir: /app/assessment_workspace/repos/Extraction-Akki
    branch: programme/track-a
    head: 996139b75bff6df67c93bceb65951cf44aba71a8
    sealed_at_utc: 2026-09-19T18:35:00Z
    seal_kind: "CP-CLEANUP-STATE-DISCIPLINE · Commit-A `996139b75bff6df67c93bceb65951cf44aba71a8` · CLEANUP SUB-WAVE · code hygiene per owner ruling 2026-09-19T~17:54Z item (c) verbatim (cleanup slotted between C.13 seal and memory layer with four bullets · this Commit-A implements code-side scope) · 14 files changed (12 new + 1 deleted + 1 modified): REMOVED-FROM-TRACKING backend/services/reliable_time_source/__pycache__/clock.cpython-311.pyc via git rm --cached (matches owner 'gitignore .pyc' verbatim · already in .gitignore · was tracked before .gitignore addition · zero test impact since Python auto-regenerates .pyc) + MODIFIED docs/registry/queries/q4_mechanical.md (benign list-sort order drift bank) + NEW backend/phase0/drill_receipts/20260919T182051Z + 20260919T182712Z + 20260919T183214Z (C.13 wave receipts housekeeping pickup + this-CP pre-commit narrow sweep GREEN receipt) + NEW backend/services/economics/tier_lock.v1397..v1406.json (10 files · economics ledger runtime snapshot pickup continuing v1..v1406 tracked-file pattern) · additive-only per SO §3.8 · NO sealed module edited · NO test file edited · NO contract file edited · NO invariant file edited · ratchet 5462 UNCHANGED · pre-commit narrow sweep GREEN 28/28 at phase0/drill_receipts/20260919T183214Z_cp_cleanup_state_discipline_code_hygiene_precommit_narrow_sweep_GREEN.log · Stop-conditions #1/#2/#3 NOT triggered · §6.4 pre-ruling NOT triggered · owner PROCEED re-affirmed 2026-09-19T~18:14Z verbatim"

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
