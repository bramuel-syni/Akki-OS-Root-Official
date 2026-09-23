# CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY · Comprehensive receipt

**Seal ID:** CP-CENSUS-THREE-WAVES-WITH-LID-OVERLAY-20260223
**Ledger item:** Item 5.11.c of `STATE/EXECUTION_ORDER.md`
**Owner anchor:** SO §6.9 amendment §6 item 8 verbatim
**Sealed at:** 2026-02-23T~14:05:00Z

## Owner canon verbatim

> "The census proceeds in its three waves — complete the walk with the
>  unmeasured register, the full B3 dimension set with the defensibility
>  matrix and sensitivity classification, then the perception pathway —
>  and language labels from item 4 enter it as overlay from the first run."

## Ratchet

- passed_floor: 6340 → 6350 (+10 canonical measured)
- baseline_failures.json sha256: e7eb57d0ba2b213b2f9b4361c6a45a6d51e39b07bbd94139314741dfaac80998
- ORCH_BOOT.md notes+audit byte-identical sha256: 20770a715ba63df78ca3d3eb18cac9984889fb9b4eff1678b4d30770a222cb09

## Double-green byte-identical

- BASELINE_GUARD=1 PYTHONHASHSEED=0 stripped_sha256: `c10b70efc5ab8c6086e83f3fb2f862bdb61ece2977bfee3684d882239c35ca88` IDENTICAL sweep_A + sweep_B
- Both sweeps: 6359 passed / 13 skipped / 0 failed / 520 warnings / ~199s each

## Sealed carriers composed (UNCHANGED per SO §3.8)

- `backend/services/audio_plane_v1/lid_wave_overlay_and_admission_v1.py` (CP-SO-6.9-LID-WAVE)

## New additive module

- `backend/services/audio_plane_v1/census_three_waves_v1.py` (~230 lines)

## Test module

- `backend/tests/invariants/test_cp_census_three_waves_with_lid_overlay.py` (10 pins)

## RED-first drill receipts

- RED_pre 10/10 failed 0.73s authentic ImportError right-reason
- GREEN_post 10/10 passed 0.73s
- sweep_A 6359 passed / 13 skipped / 0 failed / 199.49s
- sweep_B 6359 passed / 13 skipped / 0 failed / 199.34s

## Seal chain (fills in as commits land)

- Code Commit-A: `b9eb36d9` on programme/track-a
- /app companion Commit-A: `62ea504e` on main
- State Commit-B: *(this commit)*
- State Commit-C fixup: *(next)*
- /app companion Commit-C: *(next)*
- State mini-bank: *(this-seal RESUME.md rewrite at closure)*

## Ledger check

This seal implements Item 5.11.c of `STATE/EXECUTION_ORDER.md` and nothing else.
