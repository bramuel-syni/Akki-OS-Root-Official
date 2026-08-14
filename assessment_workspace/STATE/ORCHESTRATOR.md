# ORCHESTRATOR.md — Orchestrator's (owner-side) recovery file

**Last refreshed:** 2026-08-14 · Owner rulings received on FL-P2-03 (CLOSED, freeze upheld, provenance explained; console visibility check is builder's immediate next action) and FL-P2-04 (CLOSED path (a) — hardening executes through the seam). Hardening orchestrator built tests-first on `programme/track-a` (HEAD `ad65211` · 35/35 gating tests green atop baseline `b150c21`). FL-P2-03 console-check **precondition gap detected** — no Rafay console credentials in workspace; escalated with URL + auth mechanism report. Pod egress IP still `34.16.56.64`; allowlist confirmed sole /32 by owner.

**Discipline:** mirror of the builder's STATE/ discipline. Update the top of this file at every builder reply; the reply and this file MUST agree. A cold orchestrator reading only this file (plus CONTEXT · DECISIONS · PINS · NEXT) can resume without asking a question.

---

## 1 · POSTURE

**Current phase / track.** `programme/track-a` HEAD `ad65211` — 5 commits atop `b150c21`: tests-first A0/A1/seam · implementation A0/A1/seam · seam scaffolding tools · tests-first hardening orchestrator · implementation hardening orchestrator. Working tree clean. 35/35 gating tests pass at HEAD. Compute seam + FL-P2-04 path (a) hardening are code-complete and awaiting credentials. Assessment-repo `master` HEAD `14ab087` (pending this cycle's follow-up commit for owner ruling + STATE refresh + FL-P2-03 console-check log + right-reason failure logs).

**In-flight instruction (orchestrator → builder).** 2026-08-14 · owner-ruling-execution cycle: (1) append verbatim ruling to DECISIONS.md · (2) FL-P2-03 console check — precondition audit first, report console URL + auth mechanism, NEVER provision · (3) finalize hardening module per path (a) conditions (bootstrap credential env-only, single-run, retired within session, never on disk/STATE/logs) · (4) continue Phase 1 + seam commits on `programme/track-a` · (5) update ORCHESTRATOR + NEXT · (6) reply with console-check result, hardening status, track-a commit log, Phase-1 deliverable report.

**Last builder report received.** 2026-08-14 · Phase-1 commit + fixture-cycle CLOSE (previous reply): 3 track-a commits (tests-first ordering; parity-extension + record-matrix + task-identity thin kernel + declaration + custody wiring + compute seam scaffolded), plus optional-hardening front-end added to `acceptance.sh` awaiting FL-P2-04 ruling.

---

## 2 · AWAITING-FROM-OWNER (priority order)

1. **[BLOCKING FL-P2-03 EXECUTION] Rafay Console credentials for FL-P2-03 visibility check.** Console URL is `https://console.rafay.dev/` (tenant-agnostic React SPA; AISCA has no separate subdomain). Auth mechanisms exposed by the SPA: (a) email + password, (b) "Login with SSO" (email domain auto-detects OIDC/SAML federated IdP — likely path for the AISCA foundation tenant). No credentials of any kind have ever been provided in this workspace. Owner must hand over EITHER (i) email + password for the AISCA tenant, OR (ii) IdP-federated credentials + a note on which IdP (Okta / Azure AD / Google Workspace), OR (iii) an API-key for read-only tenant introspection (Rafay generates these under user profile settings — sufficient for HSS + Catalog inspection via the API even without console UI login). See NEXT.md for the exact evidence request I'll produce once any of these arrive.
2. **[HIGH] SSH credentials + VM host IP** for the compute seam. Env-var slots on `programme/track-a`: `VM_HOST`, `VM_USER`, `SSH_PRIVATE_KEY_PATH`, `SSH_PUBLIC_KEY_PATH`, `SSH_CONNECT_TIMEOUT`, `HARDEN_SH_PATH`, `HARDENING_RECEIPT_DIR`, `BOOTSTRAP_SSH_PASSWORD` (single-use, retired within the hardening session).
3. **VM provisioning day** — starts the +14d checkpoint clock (Build Order 01 §6). Sequencing per FL-P2-03 ruling: builder does console visibility check first; on green, Phase-0 executes TODAY under path (a); on not-green, stop stands and owner takes it to vendor.
4. **Reference screenshot as file** — TRANSCRIPTION-GRADE currently IN FORCE (Q1(c) ruling). Owner asked to re-send as file; not yet arrived.

## 3 · AWAITING-FROM-BUILDER — no in-flight cycle at this reply

Standing queue (blocked on rulings above):
- On Rafay console credentials arriving: perform read-only FL-P2-03 visibility check (HSS ~30 TB · Catalog for 4×H200 entry); produce screenshot-grade evidence (HTML snapshots + parsed catalog listing); go/no-go REPORT to owner before ANY provisioning.
- On SSH credentials + BOOTSTRAP_SSH_PASSWORD arrival: populate `backend/.env` on `programme/track-a`; run `services.compute_seam.hardening.run()` (6 ordered steps · external probe mandatory); then run `run_acceptance_via_seam.py` (Phase-0 acceptance ledgered end-to-end); ledger commissioning record with hardening section + acceptance section.
- Phase-2 slice: on Phase-0 green → hash manifest → admit representative slice end-to-end → FL-P1-02 focused read → slice report.

## 4 · VERIFICATION DEBT — builder claims not yet independently orchestrator-verified

**Orchestrator has NOT independently re-run any audit or test this cycle. All numbers below are builder-side runs.**

| Claim | Source | Verification path (orchestrator can execute) | Status |
|---|---|---|---|
| 35/35 Phase-1 gating tests pass on `programme/track-a` HEAD `ad65211` (26 A0/A1/seam + 9 hardening orchestrator) | Builder-side pytest run at commit boundary | `cd repos/Extraction-Akki && git checkout ad65211 && python3 -m pytest backend/tests/invariants/test_actor_declaration_v0_contract_frozen.py backend/tests/invariants/test_record_matrix_thin_kernel.py backend/tests/invariants/test_task_identity_thin_kernel.py backend/tests/invariants/test_parity_seat_extends_thin_kernel.py backend/tests/invariants/test_admit_refuses_undeclared_actor.py backend/tests/invariants/test_compute_seam_no_unledgered_exec.py backend/tests/invariants/test_compute_seam_artifact_hash_verified.py backend/tests/invariants/test_hardening_orchestrator.py -v` — expect 35 passed. | Builder-verified; orchestrator NOT independently re-run this cycle. |
| Right-reason failure evidence for Phase-1 (`2b08b39` commit) — 7/7 tests fail at collection with ModuleNotFoundError before implementation lands | `phase0/drill_receipts/20260814T120336Z_pre_implementation_right_reason_failure.log` | `git checkout 2b08b39 && pytest backend/tests/invariants/{7 test files}` — expect 7 ImportError. | Builder-verified; orchestrator NOT independently re-run. |
| Right-reason failure evidence for hardening orchestrator (`abf6328` commit) — 9/9 tests fail at collection with ImportError before hardening.py lands | `phase0/drill_receipts/20260814T130000Z_hardening_orchestrator_right_reason_failure.log` | `git checkout abf6328 && pytest backend/tests/invariants/test_hardening_orchestrator.py` — expect 9 ImportError. | Builder-verified; orchestrator NOT independently re-run. |
| Declaration-refusal drill firing (Ruling-1 precondition (a)) | `phase0/drill_receipts/20260814T120336Z_declaration_refusal_firing.log` | Independent operator re-runs the drill. | Builder-verified; orchestrator NOT independently re-run. |
| Hardening orchestrator credential-secrecy invariants (no bootstrap-pw on argv / in ledger row / in receipt / in env after return; mid-run failure blocks data movement; external probe mandatory) | 9 runtime + structural assertions in `test_hardening_orchestrator.py` | Same test file run. | Builder-verified; orchestrator NOT independently re-run. |
| FL-P2-03 console URL + auth mechanism (`https://console.rafay.dev/` — email+password OR SSO auto-detect via email domain; AISCA has no separate subdomain) | Live curl + web search this cycle | Same curl commands; owner can validate by opening URL in a browser. | Builder-fresh-verified this cycle. Orchestrator can independently open the URL. |
| Egress IP `34.16.56.64` | 4-service curl | Same. | Re-verified fresh LAST cycle by builder; NOT re-verified this cycle by builder OR orchestrator. Confidence: high. Owner confirmed as sole /32. |
| Fixture sha256s | `sha256sum fixtures/*` | Same command. | Builder-verified last cycle; orchestrator NOT independently re-run. |
| Citation audit `104/104 file · 1772/1772 canon · 0 failed` | `tools/citation_audit.py` at `7c9a544` | `python3 tools/citation_audit.py` | Builder-verified LAST cycle at `7c9a544`; **orchestrator has NOT independently re-run.** |
| Completeness audit PASS | `tools/completeness_audit.py` at `7c9a544` | `python3 tools/completeness_audit.py` | Builder-verified LAST cycle at `7c9a544`; **orchestrator has NOT independently re-run.** |
| `programme/track-a` HEAD `ad65211` with 5 tests-first commits atop `b150c21` | `git log --oneline programme/track-a` this cycle | Same command. | Builder-verified this reply. Working tree clean. |
| Hardening orchestrator successfully hardens a real VM under path (a) | FALSE — has never executed against a live VM | Cannot verify until VM credentials + BOOTSTRAP_SSH_PASSWORD arrive. | Structurally verified via mocked-outcome test suite; live behaviour unverified. |

## 5 · STANDING RULES DIGEST — cold-orchestrator cheat sheet

1. **No push, ever** — Owner Clarification 1. Local commits are the record.
2. **Tests-first** — no implementation lands before its gating invariant test fails for the right reason (Build Order 01 §5). Applies uniformly on `programme/track-a`.
3. **Escalate-and-stop on any conflict** between governing artifacts (Q2(a)). Never owner-favoured interpretation.
4. **Thin-kernel floor** — nothing live bypasses record matrix + task identity register + declaration.
5. **Fixture grades** — transcription-cleared vs file-cleared are different governance states.
6. **T1 guard** — Executive-Core purpose gate stands until BOTH declaration check AND Watch reconciler demonstrated firing.
7. **No fixture invention** — absence is a finding, never a blank.
8. **STATE/ updated at every material step.** Never end a `programme/track-a` session with staged-uncommitted production work.
9. **Owner rulings only from the owner channel** — unlogged ruling = "not lawfully happened".
10. **Repo-branch discipline** — production code ONLY on `programme/track-a` inside Extraction-Akki; assessment/governing documents on assessment-repo `master`. `phase0/` frozen at Order-§6 spec — 1×H200 SKU is NOT a fallback (owner ruled explicitly).
11. **FL-P2-04 path (a) discipline (NEW):** bootstrap credential env-only; single-use; retired within session; NEVER on argv / disk / STATE / logs / ledger row / receipt; external probe (password-refused from pod) mandatory evidence; mid-run failure = VM unhardened = no data movement.
12. **FL-P2-03 read-only ceiling (NEW):** console visibility check is READ-ONLY. Never provision anything; provisioning happens only on green check AND per §6 spec exactly.
