# Iteration 59 — main-agent resolutions and final checks

Original reports58/59 retained, not rewritten to hide failures.

1. **CORS resolved**: captured exact rewritten preview Origin on real OPTIONS,
   configured only frontend+one exact proxy alias, removed temporary logging.
   Correct-origin pass/unlisted400 proved in subsequent live pytest.
2. **Drawer navigation resolved**: test found real click obstruction. Inspected
   elementsFromPoint: original OS `8934/9400` drawer over Nexus `9720`. Suppressed
   duplicate outer `dwOpen`, not by changing click strength. Actual desktop and
   mobile button clicks now navigate to the same selected census ID.
3. **Source CTA was present**: category must first be selected. Verified actual
   `registry-source-link-{source_ref}` (label “Open the source →”) and counted one
   source API request per child click, with modal open. Earlier selector absence
   is not a remaining product defect.
4. **Status filters belong to overview**, not Watch Record's original lane bar.
   Correct node is8597; initial main script mistakenly selected8612 and was
   discarded. Actual Refused filter works; ledger rows needed `gmIsLedger=true`
   and that binding was repaired. Watch Record retains All/Observation/Action/
   Decision lanes, not a fabricated duplicate filter set.
5. **Mobile**: Watch skinny-column and overview negative-margin overflow fixed.
   Final screenshots checked actual populated overview + drawer at1920×800 and
   390×844 with overflow[] at both. Refresh node corrected to7241; authenticated
   GET returned200 after click.
6. **Transport diagnostic persistence**: corrected; all5 isolated MOCKED tests
   pass. This does not establish OBS/full-census success.
7. **Placement**: live idempotent replay without worker_id returned original
   `cr-d5d34eb632a9`, worker `akki-vm`, duplicate=true; no duplicate dispatch.

Final backend suite:28 pass,2 existing python-multipart deprecation warnings.
Evidence: `pytest/pytest_iteration_59_resolution.xml`. Existing frontend suites:
NexusFragment/nexusWork,9 pass. One early test batch ran during deliberate backend
restart and hit502/warm-up; readiness then asserted401 and all28 passed. No source
submission was added by these tests beyond the idempotent replay.

Final browser logs:
- `automation_output/20260929_010206/console_20260929_010206.log`: source CTA1request.
- `automation_output/20260929_010625/console_20260929_010625.log`: actual desktop census navigation (later filter locator was wrong).
- `automation_output/20260929_010712/console_20260929_010712.log`: drawer desktop/mobile overflow[] and actual mobile census navigation.
- `automation_output/20260929_011145/console_20260929_011145.log`: overview filters,
  desktop/mobile overflow[] and manual refresh200.

M1 gate still OPEN; M2 physical detection/action/witness/restoration acceptance
NOT RUN; vm-ii language-cognition training NOT LAUNCHED. See milestone notes.