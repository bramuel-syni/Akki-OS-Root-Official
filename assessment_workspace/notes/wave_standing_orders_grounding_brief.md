# Grounding brief — W-STANDING-ORDERS-COMPACTION-PROOF

**Wave id:** W-STANDING-ORDERS-COMPACTION-PROOF
**At:** 2026-09-08T~04:20Z
**Ratchet path:** 2997 → 3004 (+7)
**Two-commit pattern:** code+tests+baseline_failures.json → Extraction-Akki `programme/track-a`; STANDING_ORDERS.md + DECISIONS.md + NEXT.md + REATTACH_RUNBOOK.md + this brief + drill receipts → workspace `master`.

---

## §A · Owner directive verbatim

> "remember to keep this dicipline though out this build, should survive compaction".
>
> Make the discipline COMPACTION-PROOF as a small interject before/alongside the audit. Create `STATE/STANDING_ORDERS.md` — a single permanent file that any fresh/compacted session reads FIRST — and wire it so it cannot be missed:
>
> CONTENT (concise, imperative, no history — just standing law):
> 1. SESSION BOOT PROTOCOL: the CHUNK-1 problem statement is a STALE bootstrap brief — never re-run it, never re-clone, never wipe /app/assessment_workspace/. Boot sequence: read this file → last 300 lines STATE/DECISIONS.md + STATE/NEXT.md → verify repo HEADs + ratchet floor from baseline_failures.json → resume the in-flight work order from NEXT.md.
> 2. ENGAGEMENT DISCIPLINE (owner-ruled): owner-facing output is metrics-first — requirement → status → evidence path → %. Plain language, no machine jargon, no assumed emphasis. Requirements are never flattened: sub-clauses stay distinct, quoted verbatim in test docstrings. Ambiguity is never reflected back as an open question: state the ambiguity, apply ONE stated default, mark DEFAULT-PENDING-OVERRIDE.
> 3. BUILD DISCIPLINE: tests-first with mechanical RED drill receipt before implementation; double-green byte-match closes (BASELINE_GUARD=1, twice, identical tallies); ratchet floor monotonic-up; two-commit pattern (code → Extraction-Akki programme/track-a; STATE/notes/receipts → workspace master); NEVER push; terminal pytest only — testing_agent BANNED by owner; every owner ruling banked verbatim in DECISIONS.md before acting on it.
> 4. RUNTIME LAW: literal design adoption (byte-identical prototype, interpretation banned, substitutions against rendered DOM only, rule-matches-nothing = RED); no engineering vocabulary on product surfaces; pod runtime must mirror the repo (built-but-not-shipped is a failure); PII/credential custody (env/custody-file only, redacted everywhere, never committed — custody paths listed).
> 5. GPU OBLIGATIONS: full-consumption guarantee while a campaign window is open; never kill a training run mid-flight; idle GPUs = interrupt-priority restoration; credentials + host IPs live at the custody paths (list them: estate_keys/gpu_hosts/, estate_keys/data_sources/, .env host vars).
> 6. CURRENT AUTHORITATIVE ARTIFACTS: pointer list (MASTER_TRACEABILITY_AUDIT once complete, TRUE_STATE_OF_CODE, SURFACE_AUDIT_v2, SPRINT_PLAN, campaign manifests + REATTACH_RUNBOOK).
>
> WIRING so it survives compaction: (a) append a one-line pointer at the TOP and BOTTOM of STATE/DECISIONS.md and STATE/NEXT.md ("READ STATE/STANDING_ORDERS.md FIRST — permanent standing law"); (b) add an invariant test that STANDING_ORDERS.md exists, contains the six section headers, and that DECISIONS.md + NEXT.md carry the pointer lines (tests-first, floor from 2997); (c) reference it in the REATTACH_RUNBOOK. Commit via two-commit pattern.
>
> Then continue the MASTER TRACEABILITY AUDIT as ordered. Go.

## §B · Exact strings frozen by invariant

**Section headers (verbatim, one per row, must appear in STANDING_ORDERS.md):**

- `## 1. SESSION BOOT PROTOCOL`
- `## 2. ENGAGEMENT DISCIPLINE`
- `## 3. BUILD DISCIPLINE`
- `## 4. RUNTIME LAW`
- `## 5. GPU OBLIGATIONS`
- `## 6. CURRENT AUTHORITATIVE ARTIFACTS`

**Pointer line (exact bytes, verbatim owner-provided):**

`READ STATE/STANDING_ORDERS.md FIRST — permanent standing law`

The em-dash character is U+2014 (`—`), owner-provided.

## §C · Wiring targets

1. `/app/assessment_workspace/STATE/STANDING_ORDERS.md` — new file, six sections, permanent standing law, no history.
2. `/app/assessment_workspace/STATE/DECISIONS.md` — pointer line within first 5 non-empty lines AND within last 5 non-empty lines.
3. `/app/assessment_workspace/STATE/NEXT.md` — same as DECISIONS.md (pointer within first 5 non-empty and last 5 non-empty).
4. `/app/assessment_workspace/phase0/campaign_drafts/REATTACH_RUNBOOK.md` — text mentions `STATE/STANDING_ORDERS.md`.

## §D · Test scope (7 invariants, mechanical-RED first)

Test file: `backend/tests/invariants/test_standing_orders_present.py`

1. `test_standing_orders_file_exists` — file lives at the absolute workspace path.
2. `test_standing_orders_has_six_section_headers` — each of the six `## N. TITLE` headers appears verbatim.
3. `test_decisions_carries_pointer_near_top` — pointer line among first 5 non-empty lines of `STATE/DECISIONS.md`.
4. `test_decisions_carries_pointer_near_bottom` — pointer line among last 5 non-empty lines of `STATE/DECISIONS.md`.
5. `test_next_carries_pointer_near_top` — pointer line among first 5 non-empty lines of `STATE/NEXT.md`.
6. `test_next_carries_pointer_near_bottom` — pointer line among last 5 non-empty lines of `STATE/NEXT.md`.
7. `test_reattach_runbook_references_standing_orders` — REATTACH_RUNBOOK.md text mentions `STATE/STANDING_ORDERS.md`.

## §E · Wave-honest-limits

- STANDING_ORDERS.md is imperative-only; it does not paraphrase canon requirements. Requirements traceability is the MASTER audit's job.
- The invariant freezes shape (presence of headers + pointers + reference) but not word-for-word content of the six sections; the owner may edit content without breaking the invariant (edits still require ruling per §A).
- Pointer proximity is enforced at "first/last 5 non-empty lines" — chosen so that a compacted session cannot miss it while still allowing the file to open with a Markdown H1 title or trailing frontmatter.

## §F · Commit protocol

1. Author brief + test file → mechanical RED (`BASELINE_GUARD=0` initial red-check on the new test file alone, then full-suite RED under `BASELINE_GUARD=1` since baseline is unchanged and 7 new tests fail).
2. Create STANDING_ORDERS.md · prepend/append pointer to DECISIONS.md · prepend/append pointer to NEXT.md · reference in REATTACH_RUNBOOK.md.
3. Bump ratchet: `baseline_failures.json` `counts_at_baseline.passed` 2997 → 3004 AND `invariants_enforced_when_baseline_guard_1.passed_floor` 2997 → 3004 (tandem) · append `ratchet_history` entry.
4. Double-green under `BASELINE_GUARD=1`, byte-match on tally.
5. Commit A (Extraction-Akki `programme/track-a`): test file + `baseline_failures.json` bump + this brief (mirrored under `Extraction-Akki/notes/` if that path exists — else brief lives only in workspace `master` per two-commit pattern).
6. Commit B (workspace `master`): STANDING_ORDERS.md + DECISIONS.md + NEXT.md + REATTACH_RUNBOOK.md + drill receipts + this brief.
7. No push.
