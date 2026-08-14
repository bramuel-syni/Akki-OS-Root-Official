# ORCHESTRATOR.md — Orchestrator's (owner-side) recovery file

**Last refreshed:** 2026-08-14 · fixture-arrival cycle CLOSED at assessment-repo `master` HEAD `7c9a544`. Two AISCA SOP conflicts against Order §6 formally ESCALATED per Q2(a); awaiting owner rulings before Phase-0 acceptance can execute. Interface stream unblocked and complete (BAC-1..BAC-13 applied to every interface item DoD; every console item carries `test_four_questions_topline_present` on its must-write-first list). Corrections applied.

**Discipline:** mirror of the builder's STATE/ discipline. Update the top of this file at every builder reply; the reply and this file MUST agree. A cold orchestrator reading only this file (plus CONTEXT · DECISIONS · PINS · NEXT) can resume without asking a question.

---

## 1 · POSTURE

**Current phase / track.** Assessment-repo `master` HEAD `7c9a544` (fixture-arrival cycle) · BUILD_STRATEGY.md 2447 lines / 250,939 bytes / sha256 `182ef43…f152d` · audits `104/104 file · 1772/1772 canon · 0 failed` · completeness PASS. Programme-track-a Phase-1 code + 26/26 gating tests staged UNCOMMITTED on branch (separate cycle per Q3). Compute seam scaffolded, awaiting credentials.

**In-flight instruction (orchestrator → builder).** No new instruction from orchestrator in this cycle; fixture-arrival cycle CLOSED. Standing: (a) await owner rulings on FL-P2-03 / FL-P2-04 (AISCA SOP conflicts); (b) await SSH credentials + host IP; (c) await VM provisioning day; (d) refresh ORCHESTRATOR.md at the top of every reply.

**Last builder report received.** 2026-08-14 · fixture-cycle CLOSE (this reply): three fixtures on disk, BAC-1..BAC-13 extracted, three Build-Order-01 §1 corrections applied via re-assembly, ledger FL-P1-14 grade-split + FL-P1-14a/P2-03/P2-04/P2-05 rows, snapshot endpoint updated to `7c9a544`, pod egress IP re-verified `34.16.56.64`.

---

## 2 · AWAITING-FROM-OWNER

- **(a) Screenshot as file** — TRANSCRIPTION-GRADE currently IN FORCE (Q1(c) ruling · 2026-08-14). Owner asked to re-send as file; not yet arrived. Re-open FL-P1-14 on file arrival if pixels contradict transcription; refresh BAC-1..BAC-13 accordingly.
- **(b) SSH credentials + VM host IP** for the compute seam. Allowlist target = pod egress IP `34.16.56.64` (re-verified fresh this cycle). Env-var slots: `SSH_PRIVATE_KEY_PATH`, `VM_HOST`, `VM_USER`, `SSH_ALLOWLIST_EGRESS_IPS` (never in chat / STATE / commit).
- **(c) VM provisioning day** — starts the +14d checkpoint clock (Build Order 01 §6). `STATE/PINS.md` currently reads `AWAITING PROVISIONING DATE`.
- **(d) Ruling on FL-P2-03 (AISCA SOP SKU mismatch)** — SOP documents 1×H200/20vCPU/240GB/3TB; Order §6 mandates 4×H200 NVLink/84vCPU/948GB/12TB. Blocks Phase-0 acceptance until the provisioning path for Order-§6 SKU is confirmed.
- **(e) Ruling on FL-P2-04 (AISCA SOP credential-handoff gap)** — SOP hands over Password; Order §6 requires key-only + password-dead + bootstrap credentials retired before data moves. Owner ruling needed on whether `acceptance.sh` extends to cover the hardening or owner-side hands run it.

## 3 · AWAITING-FROM-BUILDER — no new cycle in flight

Standing deliverables (queued behind rulings above):
- On FL-P2-03/04 rulings: update `fixtures/aisca_sop_extraction.md` §5, `phase0/acceptance.sh`, `commissioning_checklist.md`; close FL-P2-03/04; re-audit; commit on `master`.
- On SSH credentials + host IP arrival: populate `backend/.env` on `programme/track-a`, run compute-seam preflight through the seam, execute `acceptance.sh` through the seam, ledger commissioning record, pin +14d checkpoint deadline.
- Independent cycle: commit Phase-1 A0/A1 code on `programme/track-a` (7 staged files at baseline `b150c21`).
- Phase-2 slice: on Phase-0 + Phase-1 clean → hash manifest of archive source → admit representative slice end-to-end → FL-P1-02 focused read → slice report with evidence-based checkpoint targets.

## 4 · VERIFICATION DEBT — builder claims not yet independently orchestrator-verified

| Claim | Source | Verification path | Status |
|---|---|---|---|
| 26/26 Phase-1 gating tests pass on `programme/track-a` | `phase0/A0-A1_report.md` | `cd repos/Extraction-Akki && git checkout programme/track-a && pytest backend/tests/invariants/ -v` — code still uncommitted on branch. | Unverified — awaits commit + independent run. |
| Declaration-refusal drill firing | `phase0/drill_receipts/20260814T120336Z_declaration_refusal_firing.log` | Independent operator re-runs the drill. | Unverified — receipt exists. |
| Egress IP `34.16.56.64` | 4-service curl (`ifconfig.me · icanhazip · api.ipify · checkip.aws`) | `tools/report_egress_ip.sh` re-run. | RE-VERIFIED fresh this cycle — 4/4 agree; no IPv6. Confidence: high. |
| Fixture sha256s | `sha256sum fixtures/*` | Owner recomputes on file arrival (screenshot); brief + PDF file-cleared. | VERIFIED fresh this cycle: 3/3 hashes recorded in PINS + ledger + ORCHESTRATOR. |
| Citation audit `104/104 file · 1772/1772 canon · 0 failed` | `tools/citation_audit.py` post-reassembly | `python3 tools/citation_audit.py` | RE-VERIFIED fresh this cycle at HEAD `7c9a544`. |
| Completeness audit PASS | `tools/completeness_audit.py` post-reassembly | `python3 tools/completeness_audit.py` | RE-VERIFIED fresh this cycle at HEAD `7c9a544`. |
| BUILD_STRATEGY.md at HEAD carries 3 corrections | Committed this cycle | Grep `Nine XL`, `Part 2 has not been drafted`, `27 open items` — must all be zero; `four consoles` remains only inside the FL-OQ-04 historical paraphrase-defect note (retained by owner ruling). | VERIFIED. Zero stale hits outside the historical retention. |
| BUILD_STRATEGY.md sha256 at snapshot endpoint | `curl /api/deliverables` | `sha256sum /app/backend/deliverables/BUILD_STRATEGY.md` | VERIFIED: `182ef43…f152d`, 250,939 bytes, `snapshot_commit=7c9a544`. |
| AISCA SOP → Order §6 reconciliation clean | FALSE — Conflicts A + B (FL-P2-03/04) | Owner rulings on FL-P2-03/04. | ESCALATED, awaiting rulings. |
| `programme/track-a` HEAD moved from `b150c21` | FALSE — HEAD still baseline | `git log programme/track-a --oneline` | KNOWN. Q3 scoped this cycle to assessment-repo `master`. Phase-1 branch commit is a separate cycle. |

## 5 · STANDING RULES DIGEST — cold-orchestrator cheat sheet

1. **No push, ever** — Owner Clarification 1. Local commits are the record.
2. **Tests-first** — no implementation lands before its gating invariant test fails for the right reason (Build Order 01 §5).
3. **Escalate-and-stop on any conflict** between governing artifacts (Q2(a)). Never owner-favoured interpretation, never smooth the seam.
4. **Thin-kernel floor** — nothing live bypasses record matrix + task identity register + declaration (Build Order 01 §4 A0).
5. **Fixture grades** — `transcription-cleared` vs `file-cleared` are different governance states (Q1(c)); FL-P1-14 records the distinction.
6. **T1 guard** — Executive-Core purpose gate stands until BOTH declaration check AND Watch reconciler demonstrated firing (Ruling 1). Wave-10 strip is a Canon-3 §24 ceremony (FL-R1-01).
7. **No fixture invention** — absence is a finding, never a blank (canon binding + Build Order 01 §7).
8. **STATE/ updated at every material step** — CONTEXT · PINS · DECISIONS · NEXT · ORCHESTRATOR agree at all times.
9. **Owner rulings only from the owner channel** — unlogged ruling = "not lawfully happened" (Ruling 1 four-test discipline · DECISIONS.md preamble).
10. **Repo-branch discipline** — production code ONLY on `programme/track-a` inside Extraction-Akki; assessment/governing documents on assessment-repo `master` (Q3 ruling).
