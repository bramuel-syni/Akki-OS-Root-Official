# W-Multi-Table-Extract · grounding brief

**Authored:** 2026-09-06T~14:35Z (post-W-Shield-Train-run close, mid-launch)
**Discipline:** STRICT tests-first · mechanical RED before impl · double-green from floor 2924 · two-commit pattern · no push.

---

## §Authority · owner ruling verbatim (2026-09-06T~14:XXZ, via user proxy)

> "Ruling on the blocker: (a) Charter and EXECUTE W-Multi-Table-Extract NOW, this session. Rationale: option (b) would silently rewrite the owner-approved campaign design — the corpus-mix ablation (USSD-only vs USSD+SMS) is one of Campaign B's declared hypotheses; substituting USSD-only everywhere deletes that experiment. The owner approved the design; we build to it. (b) is not authorized.
>
> Execution notes:
> 1. STRICT tests-first as always: multi-table extraction in row_executor (UNION or sequential per-table extract + composed corpus — pick the design that keeps the refuse-unclassified-by-construction property per table; sms_log columns must be classified in masking_policy before a single row crosses — extend the policy if sms_log wasn't fully covered in the build wave, cautious-default on anything ambiguous).
> 2. Extract the ussd_plus_sms corpora (deduplicated + raw variants per manifest), bank held-out slices BEFORE staging (same preflight discipline), stage to akki-vm-ii with sha256 verification, and update the on-host campaign queue so B-REF-3B, B2–B6 run as authored. Do NOT disturb the running B1 — queue behind it.
> 3. Reconcile the manifest bookkeeping: B1 ran first as an in-scope substitution — bank the reorder rationale so the campaign record reflects what actually happened (B1 promoted, B-REF queued second) rather than pretending the original order held.
> 4. While you're touching akki-vm-ii's queue, verify Campaign A's queue on akki-vm needs nothing (it's single-table USSD throughout — should be clean).
> 5. Double-green from floor 2924, receipts, two-commit pattern, then STAND DOWN per runbook — no pod-side polling after the queue is verified healthy.
>
> Also bank the wave-honest limits you listed (loss/PPL-only eval, per-epoch checkpoints, in-memory batch fetch, HF adapter format) as chartered follow-ons in the sprint plan."

---

## §A · Design decision · sequential per-table extract + composed corpus

**Not UNION at SQL level.** SQL UNION would require:
- Column-aliasing gymnastics (USSD has `option_string`+`question_string`+`value_chain`; SMS has `sms_title`+`sms_sent`) — the masking-policy lookup is by table+column, so aliasing loses the policy attachment.
- Cross-column PII-shape checks would fire on a heterogenous row (harder to reason about).
- One receipt covers two tables — worse for audit granularity.

**Sequential per-table extract + composed corpus preserves:**
- `row_executor`'s refuse-unclassified-by-construction property PER TABLE (each `execute_row_bearing_query` call runs its own policy check on its own bare SELECT).
- One row-bearing chokepoint receipt PER TABLE (better audit granularity).
- The `training_text` field composition is table-shape-specific and lives at pipeline level, not row_executor level (`_compose_training_text_ussd(row)` vs `_compose_training_text_sms(row)`).
- SQL stays simple: bare `SELECT c1, c2 FROM table` per table, ORDER BY id for determinism.

---

## §B · sms_log classification extension

sms_log schema (via `information_schema.columns`, no rows read):

| Column | Type | Class (from build wave) | Action |
|---|---|---|---|
| `id` | int | quasi-identifier | exclude |
| `county_name` | varchar | quasi-identifier | exclude |
| `subcounty` | varchar | quasi-identifier | exclude |
| `ward` | varchar | quasi-identifier | exclude |
| `farmer_name` | varchar | pii | exclude |
| `phone_number` | mediumtext | pii | exclude |
| `sms_sent` | longtext | **UNCLASSIFIED (this wave adds)** | **`non-pii-text` + `mask_regex_scrub`** (cautious default — SMS body may embed PII; regex belt-and-braces scrubs phone/ID patterns) |
| `created_at` | date | quasi-identifier | exclude |
| `sms_id` | int | quasi-identifier | exclude |
| `clints_id` | int | quasi-identifier | exclude |
| `sms_title` | varchar | non-pii-text | mask_regex_scrub |
| `created_on_dt` | timestamp | quasi-identifier | exclude |
| `breeding_id` | int | quasi-identifier | exclude |

**Emit columns for sms_log (after this wave):** `sms_sent, sms_title` (both mask_regex_scrub).

**Row count:** 1,268,229 rows in `digicow_live.sms_log`. Slice_size=30000 keeps parity with Campaign A's ussd extraction.

**Cautious-default rationale (banked):** longtext free-text bodies from an SMS system can and do embed customer phone numbers, National ID numbers, breeder-farm identifiers, and cash-transfer references. The `mask_regex_scrub` action fires the same PII-shape regex + refusal already used on `option_string`/`question_string` — any surviving PII shape post-scrub causes `CorpusIntegrityRefusal` from `build_masked_corpus_file`. This IS the cautious default the owner mandated.

---

## §C · Composition (execute_governed_lora_run extension)

Signature (backward-compatible):
```python
def execute_governed_lora_run(
    tier, recipe_version, base_model_id, material_admit_ref,
    host_slug,
    table_context,     # str OR list[str] · list triggers multi-table path
    slice_size,        # per-table slice_size (uniform)
    backend_execute, ssh_seam,
    corpus_variant=None,  # optional · 'deduplicated' | 'raw' | None
):
```

Multi-table composition (in order):
1. Admission gate — unchanged.
2. Normalize `table_context` to `tables: list[str]`.
3. For each `t` in `tables`:
   a. Build SELECT from ledger emit-columns of `t` (`include` OR `mask_regex_scrub` action).
   b. Call `row_executor.execute_row_bearing_query(...)` per-table — fires its own chokepoint receipt.
   c. Compose per-table training_text via table-shape-specific formatter:
      - `ussd_question_response`: `f"[value_chain: {vc}]\nQ: {qs}\nA: {opt}"` (unchanged)
      - `sms_log`: `f"[sms_topic: {title}]\n{body}"`
4. Concatenate composed rows in table order.
5. If `corpus_variant == "deduplicated"` OR (default when multi-table): dedupe by sha256 of `training_text` (first-occurrence-wins to preserve order).
6. Deterministic 20% tail split (unchanged).
7. Bank held-out slice hash PREFLIGHT (unchanged).
8. Build masked corpus files + stage to host (unchanged).
9. Return handle with per-table extraction receipt paths named individually.

---

## §D · production_trainer variant mapping

`default_trainer_fn` reads `manifest_entry.corpus_variant` (verbatim from manifest) and maps to `(tables, dedup_flag)`:

| Manifest `corpus_variant` | tables (list) | dedup | Used by |
|---|---|---|---|
| `ussd_deduplicated` | `["ussd_question_response"]` | True | B1 (already ran, single-table path) |
| `ussd_plus_sms_deduplicated` | `["ussd_question_response","sms_log"]` | True | B-REF, B3, B4, B5, B6 |
| `ussd_plus_sms_raw` | `["ussd_question_response","sms_log"]` | False | B2 |

Unknown variant → raise typed refusal.

---

## §E · On-host queue dispatcher

New artifact `tools/on_host_queue_dispatcher.py` deployed to `~/akki_journal/`. Reads a queue manifest at `~/akki_journal/queue/<campaign_id>.json` and dispatches serially with dependency-wait via `ACTIVITY_SUMMARY.md` polling. Fires trainers detached via `subprocess.Popen(setsid, nohup)` on host (no ssh; already on host). Writes its own heartbeat at `~/akki_journal/queue/dispatcher_heartbeat.json` every 60s.

Queue manifest shape:
```json
{
  "campaign_id": "campaign-b-method-ablations-20260906",
  "generated_at_utc": "2026-09-06T14:XXZ",
  "runs": [
    {
      "run_name": "B-REF-3B",
      "run_id": "shield-train-...",
      "wait_for_run_id": "shield-train-campaign-b-method-ablations-20260906-20260906T141344Z",  # B1
      "trainer_args": {...}
    },
    ...
  ]
}
```

Dispatcher tight-loop:
1. Iterate runs in order.
2. If `wait_for_run_id`, poll `~/akki_journal/<wait_for_run_id>/ACTIVITY_SUMMARY.md` every 60s.
3. When present (or absent for first): invoke on_host_trainer.py with `trainer_args`.
4. Wait for that run's `ACTIVITY_SUMMARY.md` before advancing.
5. On completion: seal queue with `queue_completed.md`.

Injection: `_seam_override` / `_sleep_override` for tests.

---

## §F · Wave-honest-limits (banked pre-close)

1. **On-host queue dispatcher is fire-once-per-campaign.** If the dispatcher process dies (host reboot, OOM), the campaign stalls until manual re-fire. The `on_host_watchdog.sh` handles individual TRAINER restarts but not dispatcher restarts. Chartered follow-on: `W-Queue-Watchdog` (dispatcher-level restart, symlink-atomic queue state).
2. **B-REF-3B's held-out slice will differ from B1's held-out slice** because the extraction pool differs (USSD+SMS vs USSD-only). This is CORRECT: the ablation is a corpus-mix ablation, not a held-out-slice ablation. The Campaign-A A-2-3B baseline_record for cross-ablation comparison uses A's held-out slice (USSD-only), not B-REF's.
3. **Cross-table PII correlation** (e.g. same phone number appearing in ussd_question_response's ussd_user table and sms_log's phone_number column) is NOT checked — both columns are `exclude`d by policy so no cross-table PII leak is possible via the emitted corpus. Chartered follow-on: `W-Cross-Table-Consistency-Check` for future waves that emit multiple identifier columns.
4. **Dedup is by training_text sha256** (not fuzzy semantic dedup). Two SMS with identical body but different `sms_title` will BOTH pass dedup (different training_text). Two SMS with identical `sms_title` + `sms_sent` will collapse. Cautious behavior: over-representation of identical messages is training-signal noise, not privacy risk.
5. **B2 (raw / dedup=off) MAY include exact-duplicate rows across USSD+SMS.** If a phone-message body happens to match a USSD option string byte-for-byte, both stay in the raw corpus (that's the definition of raw). B2's ideation hypothesis explicitly names this as the effect being ablated.
6. **Ruling #5 (2026-09-06T11:34:00Z) unchanged this wave · SMS emit = `sms_title` only.** `sms_log.sms_sent` (the longtext SMS body) remains parked in `masking_policy.v0.json::clarification_drawer` with `cautious_default_applied='exclude'`, pending explicit owner ruling on either (a) INCLUDE with mask_regex_scrub (treat like `question_string`, accept residual leakage risk from regex-non-caught names) or (b) EXCLUDE (drop from training corpus entirely). This session's owner ruling on multi-table charter did NOT override Ruling #5. Consequence: Campaign B's ussd_plus_sms corpus-mix ablation compares USSD-full vs USSD-full+SMS-topics-only (title strings only, avg ~40 chars — meaningful but weaker signal than USSD Q+A pairs). If owner rules Ruling #5(a) in a subsequent session, a follow-on wave can re-extract Campaign B with full `sms_sent` content and re-run the corpus-mix ablation.

---

## §G · Sprint plan follow-on charters (added)

The prior wave's wave-honest-limits become chartered follow-ons (banked in SPRINT_PLAN.md this wave):
1. `W-TaskEval-v1` — task-shaped held-out eval (accuracy on option-picking; distributional shift metrics; per-value-chain slicing).
2. `W-Gradient-Step-Checkpoint` — mid-epoch resume via `save_strategy='steps'`.
3. `W-Row-Stream-Extractor` — bounded-memory row extraction for >1M row waves.
4. `W-Adapter-Tensor-Persist` — `.pt` tensor persistence + adapter registry.

Plus this wave adds:
5. `W-Queue-Watchdog` — dispatcher-level restart + queue-state symlink atomicity.
6. `W-Cross-Table-Consistency-Check` — for future multi-emitter-column waves.

---

## §H · Campaign B reorder reconciliation

**Reality banked:**
- B1-CORPUS-USSD-ONLY promoted to first-run (2026-09-06T14:13:44Z) as in-scope single-table substitute when B-REF-3B blocked on multi-table gap.
- On W-Multi-Table-Extract close: B-REF-3B, B2-DEDUP-OFF, B3-RANK-8, B4-RANK-32, B5-CTX-512, B6-CTX-2048 queue in that manifest order behind B1 via on-host dispatcher.
- Bookkeeping file `phase0/campaign_drafts/campaign_b_run_order_reconciliation.json` names the actual sequence + rationale.

Owner instruction paraphrased: "B1 promoted, B-REF queued second — bank the reorder rationale so the campaign record reflects what actually happened".

---

## §I · Campaign A queue verification

Campaign A on akki-vm is single-table USSD throughout (all rungs A-0-0p5B, A-1-1p5B, A-2-3B, A-3-7B use `ussd_deduplicated`). No queue update needed for A. `run_queue` on akki-vm can dispatch A-1, A-2, A-3 in order behind A-0 via the same `on_host_queue_dispatcher.py` artifact. Deploy dispatcher + Campaign-A queue.json to akki-vm too, for parity.

---

## §J · Commit protocol

- Code lands on `Extraction-Akki` branch `programme/track-a` (local commit; NEVER pushed).
- STATE + receipts + brief + reconciliation JSON + sprint plan land on workspace `master` (local commit; NEVER pushed).
- Double-green from floor 2924 → target floor after this wave. Ratchet_history append + counts_at_baseline.passed + invariants_enforced_when_baseline_guard_1.passed_floor in tandem.
- Receipts: mechanical RED · double-green run1 · double-green run2 · extraction receipts for USSD+SMS · queue dispatch launch receipt · dispatcher heartbeat evidence.
