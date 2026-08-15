# ORCHESTRATOR.md — Orchestrator's (owner-side) recovery file

**Last refreshed:** 2026-08-14 · Owner Simplification Ruling CLOSED. 5-step wizard collapsed to ONE paste-and-connect panel (Registry → + Connect). Deterministic local parser at `services/credentials_paste/` (pattern-only; NO LLM SDK, NO HTTP client, NO subprocess, NO synisense reference — proven by static gating + runtime monkeypatched sabotage). Custody rule (Q2 addendum) enforced: parse-paste response NEVER carries password back; `password_captured` boolean signal only; client keeps raw paste in own textarea memory and POSTs full credential set once to unchanged `/api/connect/gpu`. Confirmation view renders `•••• captured` sentinel; unparseable paste triggers ask-again grammar; manual fallback fields inline; provisioning card one-tap aside. Handshake walk survives ONLY as post-submit RESULT view. `programme/track-a` HEAD `c490ce9` (4 tests-first + implementation commits atop `f83b509`; **143/143 gating tests green**: 108 backend python + 12 frontend allowlist + 23 frontend rehome/single-panel). 4 Playwright screenshots + 5-axis no-LLM-transit proof banked. LOC delta: `ConnectWizard.jsx` 623 → 451 (−172, −28%). FL-P2-19/20/21 all CLOSED.

<!-- prior refresh header retained below for cross-reference -->
_prior:_ Owner course-correction cycle CLOSED. Wizard rebuilt to the brief's 5-step grammar (1 What → 2 How → 3 Credentials → 4 Name → 5 Attempt) for ALL resource kinds. Estate ed25519 keypair generated in seam key custody + provisioning card rendered at compute Step 2 (Fig 10/11 alignment). Non-compute Step 5 records honest ledgered intent via POST /api/connect/intent. `programme/track-a` HEAD `f83b509` (123/123 gating tests green: 90 backend python + 33 frontend node --test). This entire step-navigation surface is now RETIRED as the primary path per the Owner Simplification Ruling; the tests that gated its testids as navigation elements have been retired accordingly.

**Discipline:** mirror of the builder's STATE/ discipline. Update the top of this file at every builder reply; the reply and this file MUST agree.

---

## 1 · POSTURE

**Current phase / track.** Owner stop-order response cycle CLOSED · WS-BUILD-CONNECT-GPU access mechanism revised (minted bearer token → source-IP allowlist) · Connect GPU form re-homed from standalone `/register/connect/gpu` route to root `/` → Admin tab → tile grid → Connect tile → GPU form. `programme/track-a` HEAD `acc25a8` — 13 sequential tests-first + implementation commits (parity + record-matrix + task-identity + declaration + custody wiring + seam + hardening orchestrator + connect-gpu router + service + acceptance wire-through + parser + IP allowlist middleware + frontend re-home). 99/99 gating tests pass. Baseline `b150c21` preserved. Spine app running at pod preview URL behind source-IP allowlist middleware.

**In-flight instruction (orchestrator → builder).** 2026-08-14 · Owner stop-order response cycle: (1) revoke compromised token immediately; (2) scrub every leak site; (3) build IP allowlist middleware tests-first with empirically established header trust boundary; (4) re-home form under Admin surface tests-first; (5) propose ONE access mechanism to owner in exactly two sentences; (6) update STATE + fidelity ledger; (7) commit on BOTH repos. All executed.

**Last builder report received.** 2026-08-14 · Acceptance-wire-through cycle: 62/62 gating tests, real acceptance.sh wired through compute seam, isolated drill against mock sshd banked `held + escalated to the vendor` with real acceptance.sh output verbatim.

---

## 2 · AWAITING-FROM-OWNER (priority order)

1. **[HIGHEST · access-mechanism confirmation] Ratify the two-sentence access-mechanism proposal (NEXT.md).** IP-pinned; `SPINE_ALLOWED_IPS` env-var configured; every change is a ledger row; surface renders the current allowlist state as plain sentences.
2. **[HIGHEST · FL-P2-09 disposition] Confirm whether `34.16.56.64` is the intended owner client `/32` (not pod egress), or direct a different value.** Pod egress has rotated to `34.170.12.145` (verified live); the strict `34.16.56.64` directive stands until owner rules otherwise.
3. **VM bootstrap credentials via the WS-BUILD-CONNECT-GPU surface.** Owner enters at `https://akki-reuse-assess.preview.emergentagent.com/` → Admin tab → REGISTRY → Connect tile → GPU form. Blocked on owner's client-IP being on the allowlist (see #1 and #2 above).
4. **Reference screenshot as file** — TRANSCRIPTION-GRADE currently IN FORCE (Q1(c) ruling). Re-open FL-P1-14 on file arrival if pixels contradict transcription.
5. **Vendor confirmation on 4×H200 + ~30 TB HSS provisioning** — owner-side action, out of this workspace's scope per standing policy.

## 3 · AWAITING-FROM-BUILDER — no in-flight cycle at this reply

Standing queue:
- On owner-confirmed allowlist entry (owner's client `/32`): update `SPINE_ALLOWED_IPS`, restart both services, verify allow-branch from owner side, record allowlist change as a ledger row.
- On real VM credentials arriving via the WS-BUILD-CONNECT-GPU surface: verify seven-stage pipeline completes (or renders correct failure grammar on §6 mismatch). Bank commissioning record; pin `checkpoint_14d_utc` (deploy_date + 14d) in PINS.
- If real acceptance renders `held` (§6 mismatch): escalate to vendor via owner; do NOT modify `phase0/acceptance.sh` to accommodate a smaller SKU (owner ruling: 1× is not a fallback).
- Phase-2 slice: on Phase-0 green → hash manifest → admit representative slice → FL-P1-02 focused read → slice report.

## 4 · VERIFICATION DEBT — builder claims not yet independently orchestrator-verified

**Orchestrator has NOT independently re-run any audit or test this cycle. All numbers below are builder-side runs.**

| Claim | Source | Verification path (orchestrator can execute) | Status |
|---|---|---|---|
| 99/99 gating tests pass at `programme/track-a` HEAD `acc25a8` (78 backend python + 12 frontend allowlist + 9 frontend re-home) | Builder-side pytest + node --test at commit boundary | See NEXT.md §4 for the exact invocations | Builder-verified; orchestrator NOT independently re-run. |
| Right-reason failure evidence for IP allowlist middleware (16/16 ModuleNotFoundError before implementation) | `phase0/drill_receipts/20260814T145500Z_ip_allowlist_right_reason_failure.log` | `git checkout e25cfe3 && pytest backend/tests/invariants/test_ip_allowlist_middleware.py` — expect 16 ModuleNotFoundError. | Builder-verified this cycle. |
| Right-reason failure evidence for frontend re-home (6/9 assertion errors before implementation) | `phase0/drill_receipts/20260814T151000Z_rehome_right_reason_failure.log` | `git checkout d2a3a01 && node --test pod_shell/frontend/__tests__/rehome.test.js` — expect 6/9 fail with the specific assertion errors listed. | Builder-verified this cycle. |
| Empirical header trust-boundary discovery (xff[-3]) — probe endpoint installed and removed same session | Log entries in this cycle; probe endpoint no longer in source (`grep _probe/headers /app/backend/server.py` — 0 hits). | Same grep. | Builder-verified this cycle. |
| Pod egress-IP `34.170.12.145` (rotation from `34.16.56.64`) | 4-service curl this cycle | Same curls. | Builder-verified this cycle. |
| Compromised token dead (HTTP 403 across all routes) | Live curl probe with old bearer, `phase0/drill_receipts/20260814T151500Z_lockdown_and_rehome_green.log` | Same curl. | Builder-verified this cycle. |
| Lockdown covers UI + API + static + retired-route | 5-route live curl, `phase0/drill_receipts/20260814T151500Z_lockdown_and_rehome_green.log` | Same curls. | Builder-verified this cycle. |
| Spoof-resistance intact (leftmost XFF injection cannot defeat allowlist) | 3 unit tests + 2 live curls this cycle | Same tests + curls. | Builder-verified this cycle. |
| Fixture sha256s | `sha256sum fixtures/*` | Same. | Verified 2 cycles ago. |
| Citation audit `104/104 file · 1778/1778 canon · 0 failed` | `tools/citation_audit.py` at `7c9a544` | Same. | 3 cycles stale; NOT re-run this cycle. |
| Completeness audit PASS | `tools/completeness_audit.py` at `7c9a544` | Same. | 3 cycles stale; NOT re-run this cycle. |
| `phase0/acceptance.sh` unchanged (frozen at §6 spec) | `git log -p phase0/acceptance.sh` | Same. | Builder-verified. Owner ruling explicit: 1× is not a fallback. |
| Real VM hardening + acceptance under path (a) | FALSE — never executed against a real VM | Awaits owner allowlist confirmation + real credential entry via the re-homed form. | Structurally verified; live behaviour unverified. |

## 5 · STANDING RULES DIGEST — cold-orchestrator cheat sheet

1. **No push, ever** — Owner Clarification 1.
2. **Tests-first** — no implementation lands before its gating invariant test fails for the right reason.
3. **Escalate-and-stop on any conflict.** No owner-favoured interpretation.
4. **Thin-kernel floor** — nothing live bypasses record matrix + task identity register + declaration.
5. **Fixture grades** — transcription-cleared vs file-cleared distinguished.
6. **T1 guard** — Executive-Core purpose gate holds until BOTH declaration check AND Watch reconciler demonstrated firing.
7. **No fixture invention** — absence is a finding.
8. **STATE/ updated at every material step.** Never end a `programme/track-a` session with staged-uncommitted production work.
9. **Owner rulings only from the owner channel.**
10. **Repo-branch discipline** — production code on `programme/track-a` in Extraction-Akki; governing docs on assessment-repo `master`. `phase0/` frozen at §6 SKU spec.
11. **FL-P2-04 path (a) discipline** — bootstrap credential env-only, single-use, retired within session, never on argv/disk/STATE/logs/ledger row/receipt; external probe mandatory.
12. **FL-P2-03 SUPERSEDED-TO-ACCEPTANCE** — no console credential enters the workspace, ever. The go/no-go moves whole to `phase0/acceptance.sh` on first hardened login.
13. **WS-BUILD-CONNECT-GPU scope ceiling** — S/M class. One connection type on one existing tile. If it grows past M, STOP and say why. Governed by `test_connect_gpu_scope_S_or_M.py` (LOC ceiling + banned-generic-name grep).
14. **[REVISED · Owner stop-order 2026-08-14] Product surface discipline** — spine app runs at pod preview URL behind SOURCE-IP ALLOWLIST middleware (env-configured, not code-hardcoded). `SPINE_ALLOWED_IPS` in `/app/backend/.env` is the single source of truth for both FastAPI backend and CRA dev-server. Refusal grammar is one plain sentence at HTTP 403 text/plain across every route family. NO shared bearer token, NO minted credential, NO login card, NO `.owner_credentials` file ever exists again on the estate surface.
15. **[NEW · Orchestrator ruling 2026-08-14] Access-mechanism doctrine** — access mechanisms proposed to the owner default to inspectable config-not-secret grammars (IP allowlist, cert-pinned mTLS, hardware key). A shared bearer token is a smell to be refused unless explicitly ruled otherwise. Every allowlist change is a ledger row; the surface renders the current allowlist state as plain sentences.
