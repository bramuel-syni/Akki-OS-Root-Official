# Iteration 92 — main-agent evidence adjudication (2026-10-05)

Original agent report is retained unchanged. Its 23/23 executed tests passed.

## Dispatch log finding: historical error, not a post-fix recurrence
- `/var/log/supervisor/backend.err.log` lines 43040–43069 place the last cited
  MALPHA_SCOPE_INVALID at **09:15:19 UTC**, before the patch.
- Lines 43070–43079 show the changed validator/NER files hot-reloaded and startup
  completed at **09:29:53 UTC**.
- The normal existing cron then dispatched listener it.5 at **09:30:29**, story_text
  it.9 at **09:30:39**, and story_voice it.10 at **09:30:45**. IDs respectively:
  `m9j-2bc0eea34925`, `m9j-dade36472f5e`, `m9j-82202771c7fd`.
- The report itself independently observed these new running jobs through the
  read-only API. Therefore its un-timestamped inference that the new validator
  still fails was unsupported. No second validator change or ad-hoc tick needed.
- Historical `resume_from` in that error was an absent OPTIONAL field spuriously
  reported by the old symmetric-difference expression, not proof it was rejected.

## Health routes: documentation corrected, no invented endpoint
- Confirmed current shell does not mount routers.health or a Shield health route,
  and does not invoke `warmup_or_warn`. Those URLs return 404.
- Updated touched loader comments and the existing unmounted health-router header
  to state current wiring truth. Existing allowlists GET is reachable but is NOT
  NER readiness. No health functionality is claimed newly implemented.
- Operational readiness wiring remains an explicit pre-existing capability gap,
  not silently added to this bounded no-new-route work package.

## Test isolation correction
- Reviewed both new test files; they alter no application code.
- Added local audit sink/model-cache isolation for NER failure branches; real
  small-model smoke now fails rather than skips if unavailable.
- Existing supervisor suite uses a scratch DB and intercepted WPW events; no live
  user declarations/admissions/native annotations were intentionally mutated.
- Offline fake-client tests are **MOCKED**; they do not establish semantic-reader
  quality, full network containment, or a successful paid frontier replay.

## Final verification
- `pytest` over the two new iteration-92 suites plus the existing supervisor
  offline suite: **28 passed**, 0 failed/skipped, 4.60s.
- JUnit: `test_reports/pytest/iteration_92_final.xml`.
- Additional loader tests cover OSError/RuntimeError/MemoryError without runtime
  repair, missing NER component and successful preferred-transformer selection.
- Final source checks: 31 unique MA rows, 7/7 governing source files found;
  0 MALPHA_SCOPE_INVALID entries after fixed-code reload; 3 native launch successes.
- Read-only native host probes ~09:41: all three expected training PIDs alive,
  GPU utilization vm0=100%, vm1=85%, vm-ii0=37%; resident vm-ii1 unchanged.
- No complete semantic capability, global network isolation, audio anonymisation
  or HTTP readiness endpoint is certified by this bounded regression suite.