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
