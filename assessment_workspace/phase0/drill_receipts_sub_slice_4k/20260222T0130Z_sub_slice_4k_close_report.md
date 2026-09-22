# Turn 4 sub-slice 4k · CLOSE REPORT · CP-R91-RETIRE-SUPERSEDE partial-retirement

- **Timestamp:** 2026-02-XXT01:15:00Z
- **Scope (achieved):** Partial-retirement of 2 v8-substitution baselines from `baseline_failures[]` + `known_r91_closure_scheduled_receipt_drift_annotations` per RESUME.md 4j-close scope. **Ratchet floor 6080 → 6086 (+6 measured: +4 new invariants + 2 absorbed retirements)** monotonic-up.
- **Scope (deferred):** Retirement of 3 R-91 mirror-drift baselines (ship_manifest_dod + 2 wave_g_pod_shell_frontend_mirror) remains queued behind CP-APP-JS-UNIFY card closure (frontmatter `milestone_status: SCHEDULED` unchanged; retire when App.js mirror drift closes end-to-end).
- **Sealed carriers LEFT UNCHANGED per SO §3.8:**
  - `tests/invariants/test_baseline_drift_annotations_present.py` (R-86 5-property enforcement · MIRROR_DRIFT_NODEIDS frozenset unchanged · property 4 set-equality preserved because retired v8-substitution nodeids are NOT in MIRROR_DRIFT_NODEIDS by design)
  - `tests/invariants/test_r88_baseline_annotation_total_coverage.py` (R-88 total-coverage · both properties preserved by removing retired nodeids from BOTH `baseline_failures[]` AND R-88 annotation field IN THE SAME COMMIT · orphan-annotation avoided)
- **RED-first authentic cycle:**
  - RED-pre `20260222T0100Z_cp_r91_retire_supersede_RED_pre.log` — 1 collection error · right-reason `ModuleNotFoundError: No module named 'services.baseline_retirement_supersede'` (test authored BEFORE any implementation).
  - GREEN-post `20260222T0105Z_cp_r91_retire_supersede_GREEN_post.log` — 4/4 pass + all sealed R-86 (5) + R-88 (2 + 6 cp10) properties GREEN post-retirement = **18/18 pass in 0.96s**.
- **Pre-Commit-A double-green byte-identical BASELINE_GUARD=1 PYTHONHASHSEED=0:**
  - SweepA `20260222T0120Z` — 6087 passed / 1 skipped / 520 warnings / 176.15s · stripped_sha256 `796d3bac14c87ce8ec0902b106a6a78dc102b9c007ac31fd7d727d09825f30ed`
  - SweepB `20260222T0125Z` — 6087 passed / 1 skipped / 520 warnings / 176.52s · stripped_sha256 `796d3bac14c87ce8ec0902b106a6a78dc102b9c007ac31fd7d727d09825f30ed` **IDENTICAL**
  - 6087 = 6086 floor + 1 above-floor (1 of 3 remaining R-91 mirror-drift baselines transiently GREEN in real bytes at this-sweep; other 2 currently RED, expected per pod_shell mirror-drift on live App.js).
- **4 invariants landed** at `tests/invariants/test_r91_v8_substitution_retirement_guard.py`:
  1. `test_retired_v8_substitution_nodeids_absent_from_baseline_failures`
  2. `test_retired_v8_substitution_nodeids_absent_from_r88_annotations`
  3. `test_supersede_module_declares_retired_nodeids_verbatim`
  4. `test_r86_mirror_drift_property_4_set_equality_preserved_post_retirement`
- **Files landed this-seal (per SO §6.4 NOTHING-BEYOND):**
  - Code Commit-A (`repos/Extraction-Akki` · `programme/track-a`):
    - NEW `backend/services/baseline_retirement_supersede/__init__.py`
    - NEW `backend/services/baseline_retirement_supersede/v8_substitution_retire.py` (RETIRED_V8_SUBSTITUTION_NODEIDS 2-tuple + RETIREMENT_SEAL_SLICE + RETIREMENT_ATTESTATION 6-anchor dict)
    - NEW `backend/tests/invariants/test_r91_v8_substitution_retirement_guard.py` (4 invariants · SO §2.5 verbatim-docstring)
    - MODIFY `backend/tests/invariants/baseline_failures.json`:
      - `baseline_failures[]`: 5 → 3 entries (2 v8-substitution retired)
      - `known_r91_closure_scheduled_receipt_drift_annotations`: 3 → 1 keys (2 v8-substitution retired; cp10-harness retained)
      - `counts_at_baseline.failed`: 5 → 3
      - `counts_at_baseline.passed`: 6080 → 6086 (+6 measured)
      - `invariants_enforced_when_baseline_guard_1.passed_floor`: 6080 → 6086
      - +1 schema-complete `ratchet_history` entry
      - new sha256 `47e9c03bb779936e4ba3bb7626e647dcd08b6b10eeae2b012fde9dad44757ecc` was `6b1e2395f34f7ebe655dc93e85ca3e58d0fc4add8b77488643e5c0a295a7c3f3`
    - ADD `backend/phase0/drill_receipts_sub_slice_4k/` (RED-pre + GREEN-post + sweepA + sweepB + this close report)
  - /app main companion Commit-A:
    - NEW `backend/vendored/extraction_akki/backend/services/baseline_retirement_supersede/*` (2 files byte-identical mirror per `prod_vendor_sync`)
    - MODIFY `backend/vendored/extraction_akki/backend/tests/invariants/test_r91_v8_substitution_retirement_guard.py` — vendored twin does NOT carry tests/ per `_INCLUSION_POLICY`; check the sync doesn't sync tests. Only 2 new services + 1 changed baseline_failures.json in vendored twin.
    - Wait: baseline_failures.json is also excluded from vendored (it's under tests/invariants/). Only 2 services are actually needed in vendored.
    - MODIFY `backend/vendored/extraction_akki/MANIFEST.json` (structural_sha256 regen)
    - MODIFY `frontend/public/audit/ORCH_BOOT.md` (ratchet block regen 6086 · sha256 `260862d5…` byte-identical to notes copy)
    - Submodule pointer advance for `assessment_workspace/repos/Extraction-Akki` → 4k Commit-A sha
  - State Commit-B (`master`):
    - APPEND `STATE/DECISIONS.md` (owner R-106 CENSUS AUTONOMY SERVICE ruling verbatim + this-seal record + GPU orphan attestation)
    - APPEND `STATE/NEXT.md` 4k §6 marker
    - APPEND `STATE/PINS.md` post-4k reference block
    - REWRITE `STATE/RESUME.md` (position → PHASE 3 CENSUS AUTONOMY SERVICE NEXT · ratchet 6086)
    - MODIFY `notes/ORCH_BOOT.md` (ratchet block 6086 · heads_last_sealed advance at Commit-C fixup)
    - ADD `phase0/drill_receipts_sub_slice_4k/` mirror
  - State Commit-C fixup — R-6 boundary regen advancing `heads_last_sealed.state_repo.head` + `heads_last_sealed.code_repo.head`
  - /app main Commit-C companion — audit ORCH_BOOT byte-identical mirror sync post-fixup
- **DESK_QUEUE effect:**
  - DQ-18 · CP-R91-RETIRE-SUPERSEDE · **partially CLOSED** (v8-substitution leg retired this-slice; mirror-drift leg queued behind CP-APP-JS-UNIFY closure)
  - All other items unchanged (DQ-17 P0 owner rotation · DQ-19 + DQ-20 P1 owner approving-authorities · DQ-05/-06/-13 owner-exclusive)
- **Standing bounds:** zero push · terminal pytest+curl only · no `testing_agent` (STRICTLY BANNED per SO §6) · additive-only §3.8 · three-repo · ratchet monotonic-up floor 6086 · HF-HOLD SEC-2026-09-12-01 · R-101 preserved WHAT partially honored (mirror closure done at 4h · v8-substitution retirement leg done at 4k · mirror-drift retirement leg queued behind CP-APP-JS-UNIFY closure) · R-102 productized-or-honest-gap satisfied · R-103 amendment applied · R-104 approving authorities named-but-unseated · R-105 partial-retirement design executed · **R-106 CENSUS AUTONOMY SERVICE banked** · §6.8 report-and-continue.
- **Autopilot next:** PHASE 3 CENSUS AUTONOMY SERVICE opens IMMEDIATELY per R-106 verbatim: (1) refactor `STATE/OBJECTIVES/CENSUS_PRODUCTIZATION.md` with 8 mandatory design goals as MUST-DOs + ops proof as EXIT · (2) supervisor-managed persistent `census_scheduler` worker process (supervisord program) · (3) additive `services/census_autonomy/*` engine porting estate_census v3 logic · (4) mid-run decision queue + UI badge integration · (5) live progress observable via polling/SSE · (6) RED-first invariants for scheduler-existence + tenant-scoping + refusal-paths + no-agent-dependency · (7) ops proof at PHASE 3 SEAL: pod-restart-resume + AKKI-TEST end-to-end no-agent run receipt.
