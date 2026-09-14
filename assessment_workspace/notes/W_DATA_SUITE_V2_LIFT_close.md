READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-DATA-SUITE-V2-LIFT · wave-close report

**Wave:** `W-DATA-SUITE-V2-LIFT` (M5 SW2 · Task 2 per owner-amended sequence 2026-09-14).
**Wave opened:** 2026-09-14T~14:00Z · ratchet floor **3929** (post-W-AUDIO-POC close).
**Wave closed:** 2026-09-14T~15:11Z · ratchet floor **3979** (+50 invariants across CP-D1..CP-D8).
**Seal:** `phase0/output_verified_seals/data_suite_v2_lift.seal.txt` · `Kind: data_suite_v2_lift` · byte-match TRUE (Green1 3979 · Green2 3979).
**Two-commit pattern held every CP.** Local commits only. Never pushed.

---

## 1 · Progress made

Case-agnostic Data-Suite workspace family landed as a coherent primitive set — every module carries a canon anchor, every contract is frozen, every state machine is closed-enum with an explicit transition matrix, every refusal names the missing carrier.

**Eight CPs, all sealed with a double-green byte-match and a monotonic-up ratchet:**

| CP | Focus | Landed | Invariants | Track-a |
|---|---|---|--:|---|
| CP-D1 | Parameterless workspace-boundary signature (lands FIRST per Solva-V2 CP-S2 precedent) | `contracts/data_suite_workspace.py` (WorkspaceState + SurfaceClass) · `services/data_suite_v2/workspace_boundary.py` | 8 (7 new + 1 cross-benefit) | `ed0265f` |
| CP-D2 | Workspace state machine · case-agnostic 4-state linear pipeline | `services/data_suite_v2/workspace_state_machine.py` | 6 | `6df2a40` |
| CP-D3 | Source-registry contract · UnitRefs-only (Canon-4 §22) | `services/data_suite_v2/source_registry.py` | 6 | `2b002df` |
| CP-D4 | Three Analyze-tab contracts (rapid/deep_dive/sources) · export refused universally | `services/data_suite_v2/analyze_tabs.py` | 6 | `cdcab77` |
| CP-D5 | Analysis-session record · Canon-3 §9.3 append-only | `services/data_suite_v2/analysis_session.py` | 6 | `aebec40` |
| CP-D6 | Export-artefact contract · discharges DAP-Spec §A10 | `services/data_suite_v2/export_artefact.py` + `export_gate.py` | 6 | `7202916` |
| CP-D7 | Analysis-lifecycle state machine · case-agnostic donor re-shape · type-separated from D2 | `services/data_suite_v2/analysis_lifecycle.py` | 6 | `3dc0d63` |
| CP-D8 | Case-agnostic donor lift · engine skeletons · executive-domain negative-scan | `services/data_suite_v2/engines/{analyze_workspace_engine,deep_dive_engine}.py` | 6 | `6549c31` |

**Ratchet chain (monotonic-up, byte-identical tally at every double-green):**

    3929 → 3937 → 3943 → 3949 → 3955 → 3961 → 3967 → 3973 → 3979

**Guardrails held whole wave:** no push · no `testing_agent` · no refactor · no wipe · no re-clone · no head/cat/sed on custody · terminal `pytest` only · EAT-window compliant (no live-egress work required this wave).

**DAP-Spec §A10 discharge concretely landed** — `ExportArtefact` frozen 4-carrier + `admit_export` refuses release naming the missing carrier via `ExportRefused`.

**Canon-3 §9.3 append-only spirit concretely landed** — `append_session` refuses a colliding `session_id` at the surface; no overwrite path exists.

**Canon-4 §22 UnitRefs-only concretely enforced** — `SourceRef` (CP-D3), `AnalyzeDeepDive` (CP-D4, hash-only-no-raw-text), `AnalyzeSources` (CP-D4, unit-refs-only), `ExportArtefact.derivation_unit_refs` (CP-D6).

**Executive-domain word-boundary negative-scan clean across `services/data_suite_v2/`** — token set lifted verbatim from `W_SOLVA_V2_LIFT_close.md §B`.

**In-session tests-first discipline correction (CP-D4).** A prior turn banked a GREEN result (6 passed) as `RED_pre_impl`. This session detected the mislabel via SO §1 parse-not-paraphrase, temp-removed the mechanism, captured the true right-reason `ModuleNotFoundError × 6` as a `v2_true` receipt, deleted the false receipt, and resumed the close on a clean tree. The corrective ritual + audit-trail note are banked in `STATE/DECISIONS.md` 2026-09-14T~14:36Z; the corrective posture is a standing pattern going forward (parse RED receipt content, do not trust its filename).

---

## 2 · How much to go

**W-DATA-SUITE-V2-LIFT itself:** DONE. All 8 CPs sealed, wave closed, seal banked, owner-facing report (this document) landed. No CP left open.

**M5 sprint (this session's plan):** essentially complete. The M5 sequence was:
* Step 0 · HF-token rotation ledger update — DONE (session-earlier).
* Step 1 · W-HYGIENE-HF-TOKEN-GUARD hardening wave — DONE (ratchet 3851 → 3858, +7).
* Task 1 · W-AUDIO-POC — DONE (ratchet 3858 → 3929, +71 across CP-A1..A6, WAVE CLOSED).
* Task 2 · W-DATA-SUITE-V2-LIFT — DONE (ratchet 3929 → 3979, +50 across CP-D1..CP-D8, WAVE CLOSED · this document).
* M5 close · full sprint completion report (M0→M5) — NEXT.

**Owner-side items still tracked (do not block this wave; wave respected them):**
* SEC-2026-09-12-01, SEC-2026-09-14-04 (HF), SEC-2026-09-13-T4-01/03/04/05, SEC-2026-09-14-01/02/03 (JUMP, RADIO, NAS, DB) — credential rotations awaiting user action.
* Missing binds: Transcription-server host+creds · RADIO routing (JUMP-side route to 10.10.19.0/24) · security-group openings for 5 closed MySQL hosts.
* Pending owner ratifications: R-7, R-15, R-16, R-17, BC-3, BC-4, S-24, R-13, R-14 (release-gate verdicts, still `DEFAULT-PENDING-OVERRIDE`).
* 165 quarantined D1a-1 legacy tests (leave quarantined per owner directive).
* Blocker BLOCKER-HF-A5-01 (HF hf-inference provider does not host whisper-small).
* Blocker BLOCKER-HF-A5-02 (NAS-to-bytes SMB plumbing follow-on).

---

## 3 · Decisions taken

1. **DPO-D1 default applied · surfaces 2 and 3 are Analyze-family sibling views.** No owner amendment received; the default stands. `analyze_tabs.py` structure can accommodate a 4th tab later without breaking the closed-Literal check.
2. **DPO-D2 default applied · W-TRUST-SURFACE-v2 + W-EXECUTIVE-SUITE-v2-LIFT stay OUT-OF-SESSION-SCOPE.** No owner amendment received; the two waves the M5 sequence enumerated (this one and W-AUDIO-POC) are the only two waves this session opens.
3. **Wave-honest limit §E.4 applied · engine skeletons HALT.** Both engines (`analyze_workspace_engine`, `deep_dive_engine`) expose a `run()` that raises `NotImplementedError` with `HALT` in the message. Donor's LLM/HTTP/DB plumbing was not lifted this wave; a future wave will replace the skeleton with the real case-agnostic mechanism. This is the Solva-V2 CP-S8 precedent.
4. **CP-D7 lifecycle enum is type-separated from CP-D2 workspace lifecycle.** Even though the state names coincide (`DRAFT/PROCESSING/READY/ARCHIVED`), `AnalysisLifecycleState` and `WorkspaceLifecycleState` are distinct enum classes. An invariant asserts `A is not W` and `A.DRAFT is not W.DRAFT` so callers cannot accidentally cross the two lifecycles.
5. **CP-D4 tests-first discipline restored in-session.** A prior turn's false `RED_pre_impl` receipt (GREEN mislabelled) was detected via SO §1 content parsing, remediated by mechanism roll-back + true-RED capture + false-receipt deletion, and the corrective ritual banked as a standing pattern in `DECISIONS.md`.

---

## 4 · Discoveries not envisioned at planning

1. **Prior-turn tests-first violation was silently on disk at wave open.** The wave's own SO §1 boot ritual caught it (parse RED receipt content, not filename). This confirms the value of the two-tier discipline check that the ALIVE-IS-NOT-DONE ban (SO §3.1) already codified for seals — the same "parse-don't-paraphrase" rule now applies to RED receipts as well. The corrective ritual is banked as a standing pattern in `DECISIONS.md` 2026-09-14T~14:36Z and reinforced in `STATE/NEXT.md`.
2. **State-side commits for CP-D1..CP-D3 lagged behind track-a.** Track-a had committed D1..D3 (`ed0265f`/`6df2a40`/`2b002df`) at wave open, but the master (state) commits for those CPs were not yet on disk (grounding brief was untracked; DECISIONS.md had no D1..D3 entries; drill receipts were untracked). Backfilled in Commit B of the CP-D4-close batch — 20 files, 9,943 insertions. Going forward, per-CP Commit-A and Commit-B should land in the same session turn to keep the two branches lock-step.
3. **The donor `analysis_lifecycle.py` (Executive-Core) does not itself carry an explicit state machine.** Its "lifecycle" is implicit (upload → active → session-close via a `status: "purged"` set). CP-D7's canonical 4-state re-shape (`DRAFT/PROCESSING/READY/ARCHIVED`) is therefore a case-agnostic *canonicalisation*, not a token-strip of a donor state enum. The wave-honest limit — module is contract-only; donor's async/GridFS/HTTP mechanics stay out-of-scope — is now the standing anchor for any future wave that lifts the real mechanics.
4. **Executive-domain negative-scan was trivially green at RED time for CP-D8** (rglob on `services/data_suite_v2/` returned no forbidden tokens because the wave was itself token-clean by construction). Per Solva-V2 CP-S8 precedent this is expected: negative-scans that trivially pass at RED time still gate against future regressions. The right-reason RED for CP-D8 was the missing engine skeletons (5 failed / 1 passed).
5. **Baseline runtime is now ~118s ± 2s** for `BASELINE_GUARD=1 python -m pytest tests/invariants/` (3979 tests). Every CP's double-green pair matched byte-for-byte on tally counts (`3979 passed, 1 skipped, 438 warnings`) with the timing digits being the only difference between run1 and run2. Not a concern; simply worth noting as the pod's steady-state pytest cost.

---

## 5 · Recommendations to make the experience better, in line with the mission

1. **Fold the parse-RED-receipt corrective ritual into SO §3 explicitly.** SO §3 currently says "No code lands without a drill receipt showing the tests failing for the right reason on the pre-implementation tree." A one-liner addition — "Parse the receipt's content; a receipt whose body shows `passed` under a `RED` filename is itself a tests-first violation that must be rolled back before the CP can close" — would prevent recurrence in future forks. Banked as a candidate SO §3 amendment for owner ratification.
2. **Land the two engine-skeleton follow-ons (`W-DATA-SUITE-ANALYZE-WORKSPACE-REAL` and `W-DATA-SUITE-DEEP-DIVE-REAL`) as a paired wave.** Both engines currently HALT; both are chartered as the *case-agnostic real mechanism* replacement. Pairing them keeps the Analyze surface coherent (rapid tab + deep-dive tab both come alive together instead of one at a time).
3. **Land `W-EXPORT-ARTEFACT-RENDER` as a small follow-on.** CP-D6 landed the contract + gate; actual export payload rendering (CSV/PDF/…) is out-of-wave (§E.3 wave-honest limit). Small scope, high user-visible value.
4. **Ratify the release-gate verdicts R-7 / R-15 / R-16 / R-17 (BLOCKER-HF-A5-03 · escalated from W-AUDIO-POC).** These are the same DAP-A10 category as the ExportArtefact carriers this wave landed; ratifying them lets the Audio-POC release gate move from `PENDING` to real verdicts, unlocking the audio-plane end-to-end.
5. **Consider chartering `W-TESTS-FIRST-GUARD-INVARIANT` as a small hardening wave** that lands an invariant which parses any `*_RED_pre_impl.log` under `phase0/drill_receipts/` and refuses green tallies (an automated version of the parse-not-paraphrase corrective ritual). Cost: a handful of invariants. Payoff: this class of prior-turn violation becomes structurally impossible.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
