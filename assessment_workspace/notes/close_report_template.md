# Wave close-report template — effective W6

Standing template for every wave close from W6 forward. Owner Ruling
2026-08-25 (W6 GO) + Orchestrator Ruling 2026-08-25 (path (a)).

## Sections (mandatory)

1. **Owner orders logged** (verbatim, dated, all in STATE/DECISIONS.md).
2. **Register rows targeted this wave** (row IDs + count + state at close).
3. **Reuse pulls cited** (source repo:file:LOC → destination · class REUSE/ADAPT/BUILD).
4. **Per-mechanism test delta**:
   - Net-new invariants (by file · count · one-line each).
   - Amended invariants (docstring pointers to the amendment ruling).
   - **Right-reason failure receipts** banked (paths).
   - **Green receipts** banked (paths).
   - **Live E2E receipts** banked (paths + real receipt IDs).
5. **SHAs** — every commit on programme/track-a in the wave + STATE commit(s) on assessment_workspace@master.
6. **Fidelity ledger — findings this wave** (opened rows + closed rows).
7. **LOC vs re-baselined budget** (per-checkpoint delta + total · % of stop-and-report line).
8. **Screenshots · what banked** (path + one-line description each). If IP-allowlist refused the screenshot tool, name it and give the curl-with-XFF alternative receipts.
9. **Vocabulary check** — spot-check canon vocabulary is uniform (naming corrections applied).
10. **Deferred to owner ruling** (numbered list · one line each).

## Wave-close cohort assembly (Orchestrator Ruling 2026-08-25)

The wave-close green-cohort MUST be assembled by grep — no hand-curated list. This closes the scoping gap discovered as FL-P4-W4-01.

```bash
cd /app/assessment_workspace/repos/Extraction-Akki/backend
python3 -m pytest \
    $(ls tests/invariants/test_*_frozen*.py tests/invariants/test_*_contract*.py tests/invariants/test_*.py 2>/dev/null | sort -u) \
    -v 2>&1 | tee /app/assessment_workspace/phase0/drill_receipts/<timestamp>_w<N>_wave_close_green.log | tail -3
```

Or more broadly (all invariants + specifically both snapshot patterns):

```bash
python3 -m pytest tests/invariants/ -k "frozen or contract or invariant or w<N> or <the-wave-topic>" -v
```

The close report §4 must cite the log path and confirm the cohort included every `test_*_frozen*.py` + `test_*_contract*.py` present at wave-close SHA.

## LOC accounting rules

- Actuals = git-measured `insertions` across the wave's commits on programme/track-a (via `git show --stat --format=` and sum).
- The wave's own re-baselined estimate (from notes/status_and_wave_plan.md §7 table) is the stop-and-report line.
- Cross the stop-and-report line → CP-close-commit + report to orchestrator before continuing.
- Overrun at close (if not stopped) is named honestly with a "why" line.

## Vocabulary check (§9)

Every wave close spot-checks canon vocabulary against any owner corrections. Since Solva vs Solver was flagged in W5, every subsequent close report must include a two-line vocabulary check (name what was corrected + confirm uniform application across code · tests · surface copy · receipts).
