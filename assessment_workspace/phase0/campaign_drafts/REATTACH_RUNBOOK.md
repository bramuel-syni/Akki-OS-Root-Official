# REATTACH_RUNBOOK · Campaign session pickup after context loss

**Purpose.** A concise "how the next session adopts the two active campaigns" runbook so reconciliation is MECHANICAL regardless of context loss between now (launch) and 2026-09-09 (window close).

**Authority — owner ruling verbatim (2026-09-06T~12:32Z):**

> "Bank a REATTACH RUNBOOK (how the next session adopts the campaigns: adopt env vars, reconcile paths, what to check first) so reconciliation is mechanical regardless of context loss."

---

## Section 1 · First-touch checks (run these in order before touching anything else)

1. **STATE tails** — read the last 200 lines of `STATE/DECISIONS.md` + `STATE/NEXT.md` (anti-compaction rule). Confirm the two campaigns' close entries exist and note the current-marker.
2. **Ratchet floor** — `python3 -c "import json; m=json.load(open('/app/assessment_workspace/repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json')); print(m['counts_at_baseline']['passed'], m['invariants_enforced_when_baseline_guard_1']['passed_floor'])"` — both numbers MUST match. Any divergence means an in-flight bump was interrupted.
3. **Git state on both branches** —
   ```
   cd /app/assessment_workspace/repos/Extraction-Akki && git status --short && git log --oneline -n 5
   cd /app/assessment_workspace && git status --short | head -20 && git log --oneline -n 5
   ```
   A dirty working tree on either branch is a signal to reconcile bookkeeping FIRST.

## Section 2 · Adopt environment variables

Set these BEFORE invoking any reconcile command:

```bash
export AKKI_ENV=development
export AKKI_HOST_JOURNAL_ROOT=/home/akki/akki_journal        # host-side · on each GPU host
export AKKI_CAMPAIGN_HOST_LOCK=/home/akki/akki_journal/host.lock   # host-side
export AKKI_ON_HOST_WATCHDOG_TARGETS_DIR=/home/akki/akki_journal   # cron sets this
export AKKI_ON_HOST_TRAINER_CMD='/home/akki/trainer.sh --resume-from %m --step %s --run-dir %r'  # host-side
export AKKI_LORA_MASKING_TIER=t1_full_mask
export AKKI_LORA_TABLE_CONTEXT=ussd_question_response
```

**Pod-side reconcile** does NOT need `AKKI_HOST_JOURNAL_ROOT` unless testing locally; the reconciler enumerates the host journal via SSH pull (see Section 4).

## Section 3 · Reconcile paths

| Location | What lives here | How the runbook reads it |
|---|---|---|
| `/app/assessment_workspace/phase0/campaign_drafts/CAMPAIGN_OBJECTIVES.md` | Campaign objectives + success criteria banked pre-launch | Reference (never edit) |
| `/app/assessment_workspace/phase0/campaign_drafts/campaign_a_baseline_ladder.json` | Campaign A manifest (akki-vm) | Reference (never edit) |
| `/app/assessment_workspace/phase0/campaign_drafts/campaign_b_method_ablations.json` | Campaign B manifest (akki-vm-ii) | Reference (never edit) |
| `phase0/wpw_notebook/{campaign-a_run_name,campaign-b_run_name}/notebook.jsonl` | Per-run Tier 1 events pulled from host | Read to verify wizard A2 evidence |
| `phase0/campaign_reports/CAMPAIGN_{A,B}_SUMMARY.md` | Post-window authored summary (does NOT exist until close) | Author at window close |
| Host `~/akki_journal/<run_id>/heartbeat.json` | On-host heartbeat · latest step + training_pid + at_utc | Read via SSH pull |
| Host `~/akki_journal/<run_id>/polls/poll_step_*.json` | Per-step poll receipts (loss + wall_clock) | Read via SSH pull |
| Host `~/akki_journal/<run_id>/ACTIVITY_SUMMARY.md` | Run sealed → present iff run is DONE | Read via SSH pull |
| Host `~/akki_journal/<run_id>/checkpoint_marker.json` | Latest checkpoint step + sha (adapter hash) | Read via SSH pull |
| Host `~/akki_journal/<run_id>/watchdog_restart_*.json` | Watchdog restart journal entries | Read via SSH pull · counts restarts per run |

## Section 4 · Adoptability check per run (mechanical)

For each `run_id` under `AKKI_HOST_JOURNAL_ROOT` on the host:

```python
from backend.services.campaign_infra import reconcile
verdict = reconcile.adoptability_of_campaign_run(run_id, max_staleness_s=1800)
# verdict['reason'] in { 'still_running', 'restart_from_checkpoint', 'sealed', 'never_started' }
```

Verdict handling:
- `still_running` → do nothing. Do NOT signal the process. Do NOT restart. Log the observation only.
- `restart_from_checkpoint` → the on-host watchdog SHOULD have already restarted it. Verify a recent `watchdog_restart_*.json` entry exists; if not, this pod session invokes the trainer with `--resume-from <checkpoint>` explicitly (extremely rare · usually the cron watchdog handles it).
- `sealed` → the run is DONE. Pull its notebook.jsonl + poll receipts + summary + checkpoint marker into `phase0/wpw_notebook/{campaign_id}_{run_name}/`.
- `never_started` → the run is next in the queue but hasn't been picked up yet. Verify the campaign runner is still active (`ps` on host).

## Section 5 · Wizard-evidence pull per sealed run (Objective 3)

For each `sealed` run, the reconciler produces per-run wizard-A1–A6 evidence:

1. **A1 (attach)** — verify `phase0/wpw_notebook/<run>/notebook.jsonl` first line is a WPW-1 attach event with `run_id` matching.
2. **A2 (events)** — verify ≥1 WPW-2..WPW-7 event per {checkpoint, anomaly, cost-checkpoint} phase.
3. **A3 (settlement)** — verify `phase0/tier2_reports/<run>.md` exists with acceptance-criteria MEASURED against held-out.
4. **A4 (novelty)** — Campaign-B only: verify `phase0/tier2_reports/<run>.md` carries `novelty_verdict` field vs paired Campaign-A baseline record.
5. **A5 (Tier 3 eligibility)** — verify `phase0/tier3_eligibility_verdicts/<run>.json` exists with `eligible: true|false` + `reason` fields · **publication remains BLOCKED pending R1/R2/R3**.
6. **A6 (refused-run)** — if any `phase0/wpw_notebook/<run>/notebook.jsonl` ends in a WPW-fail event, verify its notebook + poll receipts + partial checkpoint marker were STILL retained.

## Section 6 · Ratchet floor discipline during the window

The campaign is expected to progress WITHOUT touching the invariant test ratchet. If any run causes a test regression, that is a bug in the runner (recovery-not-interference or masking-tier-refusal). Response:

1. Stop the campaign on the affected host (touch a `PAUSE` file that the on-host watchdog respects — see host runbook).
2. Fix the invariant regression via tests-first RED-then-GREEN cycle.
3. Ratchet floor MOVES UP if tests are added; NEVER moves down (that is the discipline).
4. Resume the campaign only after double-green.

## Section 7 · Window-close deliverables (author at 2026-09-09T23:59Z)

1. `phase0/campaign_reports/CAMPAIGN_A_SUMMARY.md` — table of 7 baseline_records + Tier 2 settlement + Tier 3 verdict for each Campaign-A run.
2. `phase0/campaign_reports/CAMPAIGN_B_SUMMARY.md` — table of 7 runs (1 reference + 6 ablations) + Tier 2 settlement + novelty_verdict + Tier 3 verdict for each Campaign-B run.
3. A single close entry in `STATE/DECISIONS.md` naming: (i) what settled, (ii) what refused/crashed (A6 evidence), (iii) which Tier 3 verdicts came back eligible-but-blocked, (iv) any wave-honest-limits surfaced during execution.
4. Ratchet stayed monotonic-up · window ended at the same floor or higher.

## Section 8 · Emergency abort (owner ruling required)

If owner orders the campaign paused OR aborted mid-window:
1. On each host: SSH in and touch `~/akki_journal/PAUSE` — the on-host watchdog and campaign runner both respect this (charter this as follow-on if not already enforced).
2. Verify all training PIDs stop cleanly via `retire_heartbeat` per run.
3. Bank the abort ruling verbatim in `STATE/DECISIONS.md`.
4. Move active runs' notebook.jsonl + partial checkpoint markers into `phase0/wpw_notebook/aborted/`.

## Section 9 · DATA GATE reminder (never forget)

**t1_full_mask is admitted ONLY under `AKKI_ENV=development`.** `sandbox` and `production` are NOT admitted. Any reconcile action that would trigger a governed extraction under a non-development env MUST fail via `MaskingTierNotAdmitted` — this is frozen by `test_execute_governed_lora_run_raises_on_parked_tier` (invariant asserts `AKKI_ENV=sandbox` still refuses).

The reconcile module NEVER re-triggers extractions; it only reads on-host journal + on-host checkpoint markers.

---

*Authored 2026-09-06T~12:50Z pre-launch per owner's STEP 5 directive.*
