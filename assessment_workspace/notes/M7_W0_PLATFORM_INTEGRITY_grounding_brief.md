READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M7-W0-VERIFICATION · Grounding brief · 2026-09-16T~03:52Z

**Wave:** W-M7-W0-VERIFICATION (M7 W0 platform integrity walk).
**Type:** VERIFICATION WALK — not a mechanism build.
**Predecessor:** M6 SW-9 close (CP-M6-9-2 · ratchet 4358 · track-a `7b45a890`).
**Concurrent:** W-M7-UTILIZATION-72H · LIVE from 2026-09-16T03:41:28Z.

---

## §A · Owner authorization verbatim (2026-09-16T~03:08Z)

> "M7 OPENS per the ratified tree (W0 platform integrity → W1 generalisation → W2..W9). Author the M7-open milestone-boundary note + W0 grounding brief, then walk autonomously under all standing guardrails."

**Also (2026-09-15T~04:12Z verbatim):**
> "Then M7 open: same pattern — reframe-activation note + W0 platform integrity → W1 generalisation → W2+ as unblocked."

## §B · Verbatim canon anchors

**STANDING_ORDERS.md §3.1 · "ALIVE IS NOT DONE" (banked 2026-09-13 · verbatim owner directive "BUILD GO"):**

> **ALIVE IS NOT DONE.** The existence of a heartbeat, a running PID, a directory on disk, or a filename in that directory is NOT proof of completion. Completion requires an OUTPUT ARTIFACT — a seal file whose contents, when parsed, prove the specific real work-kind that just finished. A seal read that does not parse `Kind:` and refuse non-real kinds silently promotes stubs, synthetic fixtures, and unfinished runs to success. This is banned.

**Binding contract on every seal read (STANDING_ORDERS §3.1):**

> 1. Every sealing check in the codebase MUST route through `services.output_verified_seal.is_real_seal(run_dir)` (or the sibling `parse_seal` primitive when the caller needs the parsed payload). Bare filename-existence checks against `ACTIVITY_SUMMARY.md` are banned.
> 2. A "real seal" is a file that (a) exists at the canonical `ACTIVITY_SUMMARY.md` path (case-insensitive), (b) carries a `Kind:` line in its body, and (c) whose `Kind:` value names a real-work kind — NOT `stub`, `synthetic`, `unfinished`, `test_fixture`, or the empty string.
> 3. Every seal write MUST route through `services.output_verified_seal.output_verified_seal(run_dir, kind=..., body=...)`. The writer emits `Kind: <value>` as a first-class field in the body. A write without a kind is refused (`ValueError`).
> 4. Silent-success attack surface enumerated at W0 open (2026-09-13 · 6 code sites, all refactored in this wave):
>      - `services/campaign_infra/reconcile.py::_is_sealed`
>      - `services/campaign_infra/run_queue.py::_is_run_sealed`
>      - `services/orchestrator_resilience/orphan_detector.py::_has_sealing_marker`
>      - `services/orchestrator_resilience/adopt.py::can_adopt` (direct `.exists()` on line 85)
>      - `services/orchestrator_resilience/watchdog.py` (via `_od._has_sealing_marker` on line 126)
>      - `services/campaign_infra/on_host_logging.py::write_run_summary` (writer side — emits `Kind:` on every write)
> 5. Invariant `test_output_verified_seal.py` freezes this contract. Adding a new seal read/write in the codebase without routing through `output_verified_seal` is a right-reason RED failure under BASELINE_GUARD=1.

**ROADMAP §A.12 W0 verbatim (banked 2026-09-13):**

> Fixes six specific code sites where the platform conflates process-liveness with work-progress. Full anatomy in `notes/SILENT_FAILURE_ROOTCAUSE_AND_LAYER_MAP.md §1`. Delivers:
>
> - Parse `Kind:` field in every seal predicate.
> - Introduce `output_verified_seal(run_dir)` composite predicate.
> - **New STANDING ORDER: "Alive != done."** — appended to STANDING_ORDERS.md.

## §C · Wave scope · VERIFICATION WALK (this shift)

**Goal.** Verify from-disk that the SO §3.1 contract is still enforced at M6-9-2-close state (track-a `7b45a890` · ratchet 4358). Verification is a parse-not-paraphrase read against the current tree. Findings drive one of two outcomes:

- **Path α · Clean verification:** produce a verification receipt (JSON) enumerating every seal read/write site + confirming each routes through the primitive · close W0 as zero-delta verification seal (no ratchet bump · no `test_*` file added · verification-receipt in phase0 only) · single master commit banks the receipt.
- **Path β · Drift discovered:** any seal-check surface that bypasses the primitive is a first-class integrity defect. Author `test_wm7_w0_<n>_<site>.py` per drift · mechanical RED · route the surface through `is_real_seal` / `output_verified_seal` primitive · double-green byte-match at seal · ratchet monotonic-up · §3.3 3-commit per CP.

**Case-agnostic verification steps (this shift · autonomous):**

1. **Enumerate current seal-read sites** via `grep -Rn` over `services/` for the token union: `ACTIVITY_SUMMARY\.md`, `_is_sealed`, `_is_run_sealed`, `_has_sealing_marker`, `is_real_seal`, `parse_seal`, `output_verified_seal`, `Kind:`. Include `.py` and `.md` (invariants). Exclude vendor + tests directories from the SITE list (but include tests in the primitive-coverage set).
2. **Confirm the 6 W0-refactored sites are still routed** (regression-hunt via file-open, not just filename): each of the 6 sites listed in SO §3.1 clause 4 must import `output_verified_seal` primitive (or route through it via composition).
3. **Enumerate NEW seal-read/write surfaces added since 2026-09-13** — anything under `services/` matching the token union with commit date > 2026-09-13 (via `git log -p --since="2026-09-13" services/` for the seal-read tokens). Each new site MUST route through the primitive.
4. **Confirm `test_output_verified_seal.py` is still present + healthy** in `tests/invariants/` (from `git ls-files tests/invariants/` + baseline pass count includes the 31 W0 invariants).
5. **Bank verification receipt** at `phase0/m7_w0_verification/verification_receipt_20260916.json` with schema:
   ```
   { generated_at_utc, ratchet_floor, track_a_head, master_head,
     sites: [ { path, symbol, routes_through_primitive: bool, evidence: <grep-line-ref> } ],
     new_sites_since_w0_close: [ ... same shape, plus commit_sha, commit_date ],
     w0_invariant_present: bool,
     w0_invariant_count: int (expected 31),
     verdict: "clean" | "drift",
     drift_items: [ ... ] }
   ```
6. **If verdict=clean:** author `notes/W_M7_W0_close.md` (5-section END-OF-WAVE format) + single master commit banks (a) grounding brief (this file) (b) verification receipt (c) close report (d) NEXT.md pin update. No track-a commit (no code change). Not a §3.3 case since no seal file lands.
7. **If verdict=drift:** each drift is a CP: `CP-M7-W0-<n>` · tests-first RED → mechanism → double-green → seal → §3.3 3-commit.

## §D · Wave-honest limits

- **Verification walk depth**: reads current-shift tree HEAD. It does NOT re-run the 2026-09-13 W0 mechanical RED drill; that receipt is durable at `phase0/drill_receipts/20260913T060000Z_w0_output_verified_seal_RED.log` and the double-green at `phase0/drill_receipts/20260913T063000Z_w0_output_verified_seal_double_green.log`.
- **Case-agnostic scope**: the walk covers seal read/write surfaces regardless of what work-kind they seal. It does NOT enumerate every `Kind:` value in use across seal files (that is a §6 audit surface). It DOES verify that the writer emits `Kind:` and the reader parses `Kind:`.
- **Concurrent utilization job**: the sampler and workload processes on akki-vm / akki-vm-ii are NOT `services/**` surfaces — they live in `tools/` (state-repo). Their launch discipline is banked in `notes/M7_UTIL_72H_LAUNCH_RECOVERY_20260916.md`; whether to add an invariant enforcing the base64-launcher idiom is a CANDIDATE CP for W0 if a drift-adjacent concern surfaces during this walk.

## §E · Concrete owner-facing decision surfaces

None at grounding-brief authoring. Verification is case-agnostic. If Path β fires (drift), each drift-CP is autonomous per SO §3 unless the drift itself touches load-bearing PII / custody / owner-desk item; in that case, HALT-to-owner per SO §2 ambiguity discipline.

## §F · Commit protocol (per §3.3)

- **Path α (clean · this shift target):** ONE state commit on master carrying:
  1. `notes/M7_OPEN_REPORT_20260916.md` (this-shift · already authored).
  2. `notes/M7_W0_PLATFORM_INTEGRITY_grounding_brief.md` (this file).
  3. `phase0/m7_w0_verification/verification_receipt_20260916.json` (banked at walk close).
  4. `notes/W_M7_W0_close.md` (5-section END-OF-WAVE format · plain product language).
  5. `STATE/NEXT.md` pin update.
  6. `STATE/DECISIONS.md` W0 verification-close entry.
  Commit message: `W-M7-W0-VERIFICATION · verification walk · verdict={clean|drift} · sites=N · ratchet unchanged 4358`.
- **Path β (drift · this shift or next):** per §3.3 three-commit pattern per CP.
  - Commit A on `programme/track-a`: code fix + tests-first invariant.
  - Commit B on `master`: state + notes + seal file (master SHA TBD).
  - Commit C on `master`: fixup (master SHA landed).

## §G · GPU utilization check-in interleave (owner ruling 2026-09-16T~03:08Z)

Check-in `python3 tools/m7_util_72h_orchestrator.py check_in` fires at:
- **W0 open** (this authoring · covered by recovery close at 03:44:44Z).
- **W0 seal** (Path α or first Path β CP close).
- Continuously as W-M7-W0-VERIFICATION progresses if wall-clock > 30 min.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
