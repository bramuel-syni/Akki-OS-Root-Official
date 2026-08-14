# ORCHESTRATOR.md — Orchestrator's (owner-side) recovery file

**Last refreshed:** 2026-08-14 · Owner rulings on console-access + credential-delivery + WS-BUILD-CONNECT-GPU received. FL-P2-03 SUPERSEDED-TO-ACCEPTANCE, FL-P2-04 CLOSED path (a). WS-BUILD-CONNECT-GPU built tests-first on `programme/track-a` HEAD `dad2faa` (7 commits atop `b150c21`; **52/52 gating tests green**). Surface reachable at `https://akki-reuse-assess.preview.emergentagent.com/register/connect/gpu` behind owner-bearer-token auth. End-to-end UI drill against mock sshd banked (`failed (ours; retry)` grammar branch confirmed). Pod egress IP: `34.16.56.64`.

**Discipline:** mirror of the builder's STATE/ discipline. Update the top of this file at every builder reply; the reply and this file MUST agree.

---

## 1 · POSTURE

**Current phase / track.** WS-BUILD-CONNECT-GPU code-complete + end-to-end drill green. `programme/track-a` HEAD `dad2faa` — 7 sequential tests-first commits (parity + record-matrix + task-identity + declaration + custody wiring + seam + hardening orchestrator + connect-gpu router + service). 52/52 gating tests pass. Baseline `b150c21` preserved. Spine app running at pod preview URL. Assessment-repo `master` HEAD `a450d8f` (pending this cycle's follow-up commit for ruling verbatim + fidelity ledger updates + STATE refresh + drill assets).

**In-flight instruction (orchestrator → builder).** 2026-08-14 · connect-gpu-build cycle: (1) append verbatim ruling · (2) mark FL-P2-03 SUPERSEDED-TO-ACCEPTANCE and FL-P2-04 CLOSED path (a) in ledger · (3) build WS-BUILD-CONNECT-GPU tests-first · (4) wire spine app to serve at preview URL behind owner bearer auth · (5) mock-sshd drill against 127.0.0.1:2222 · (6) commit on both branches · (7) reply with gating tests + drill receipts + owner-access credential + URL path + scope-class confirmation.

**Last builder report received.** 2026-08-14 · Phase-1 hardening cycle (previous reply): 26+9 gating tests green, hardening orchestrator code-complete under path (a) discipline, FL-P2-03 precondition-gap surfaced.

---

## 2 · AWAITING-FROM-OWNER (priority order)

1. **[HIGHEST · Phase-0 gating] VM bootstrap credentials via the WS-BUILD-CONNECT-GPU surface.** Owner enters at `https://akki-reuse-assess.preview.emergentagent.com/register/connect/gpu` using the owner access token (see NEXT.md for how the pod operator hands it over). Form: Host Name · Username · Password · Public IP · [Private IP · OS · Deploy Date]. Submit fires the seven-stage pipeline automatically; four-questions after-state renders on completion. Bootstrap password transits ONCE, retired within the same submit call.
2. **Reference screenshot as file** — TRANSCRIPTION-GRADE currently IN FORCE (Q1(c) ruling). Re-open FL-P1-14 on file arrival if pixels contradict transcription.
3. **Vendor confirmation on 4×H200 + ~30 TB HSS provisioning** — owner-side action, out of this workspace's scope per standing policy. On green: real VM credentials arrive via the WS-BUILD-CONNECT-GPU surface; Phase-0 executes end-to-end.

## 3 · AWAITING-FROM-BUILDER — no in-flight cycle at this reply

Standing queue:
- On real VM credentials arriving via the WS-BUILD-CONNECT-GPU surface: verify seven-stage pipeline completes (or renders correct failure grammar on §6 mismatch). Bank commissioning record; pin `checkpoint_14d_utc` (deploy_date + 14d) in PINS.
- If real acceptance renders `held` (§6 mismatch): escalate to vendor via owner; do NOT modify `phase0/acceptance.sh` to accommodate a smaller SKU (owner ruling: 1× is not a fallback).
- Phase-2 slice: on Phase-0 green → hash manifest → admit representative slice → FL-P1-02 focused read → slice report.

## 4 · VERIFICATION DEBT — builder claims not yet independently orchestrator-verified

**Orchestrator has NOT independently re-run any audit or test this cycle. All numbers below are builder-side runs.**

| Claim | Source | Verification path (orchestrator can execute) | Status |
|---|---|---|---|
| 52/52 Phase-1 gating tests pass on `programme/track-a` HEAD `dad2faa` (26 A0/A1/seam + 9 hardening + 17 connect-gpu) | Builder-side pytest at commit boundary | `cd repos/Extraction-Akki && git checkout dad2faa && python3 -m pytest backend/tests/invariants/ -v` (10 test files listed in NEXT.md) — expect 52 passed. | Builder-verified; orchestrator NOT independently re-run. |
| Right-reason failure evidence for connect-gpu (`ea3d874` commit) — 15/15 pipeline tests fail at collection with ImportError before service lands | `phase0/drill_receipts/20260814T140000Z_connect_gpu_right_reason_failure.log` | `git checkout ea3d874 && pytest backend/tests/invariants/test_connect_gpu_*.py` — expect 15 ImportError + 2 scope pass. | Builder-verified. |
| UI drill against mock sshd (127.0.0.1:2222) renders `failed (ours; retry)` end-to-end | `phase0/drill_receipts/20260814T140516Z_connect_gpu_ui_drill.json` + 5 screenshots under `screenshots/` | Re-run via Playwright at the same URL with token + mock pw. | Builder-verified this cycle. |
| Password never persists (searched receipts + commissioning records + PINS + backend logs; zero hits) | `grep -rc <mock_pw>` executed this cycle | Same grep. | Builder-verified this cycle. |
| Surface reachable at pod preview URL behind bearer auth | `curl` this cycle: HTTP 200 on `/register/connect/gpu`; HTTP 401 on unauthed `POST /api/connect/gpu` | Same curls. | Builder-verified this cycle. |
| Owner access token generated at `/app/backend/.owner_credentials` (mode 0600) | Backend startup log: `owner-token: generated new .owner_credentials (mode 0600); prefix=fd97993e...` | `ls -la /app/backend/.owner_credentials`. | Builder-verified this cycle. |
| Egress IP `34.16.56.64` | 4-service curl | Same. | Re-verified 2 cycles ago; unchanged infra. |
| Fixture sha256s | `sha256sum fixtures/*` | Same. | Verified 2 cycles ago. |
| Citation audit `104/104 file · 1772/1772 canon · 0 failed` | `tools/citation_audit.py` at `7c9a544` | Same. | 2 cycles stale; NOT re-run this cycle. |
| Completeness audit PASS | `tools/completeness_audit.py` at `7c9a544` | Same. | 2 cycles stale; NOT re-run this cycle. |
| `phase0/acceptance.sh` unchanged (frozen at §6 spec) | `git log -p phase0/acceptance.sh` | Same. | Builder-verified. Owner ruling explicit: 1× is not a fallback. |
| Real VM hardening + acceptance under path (a) | FALSE — never executed against a real VM | Awaits real credentials via the surface. | Structurally verified; live behaviour unverified. |

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
13. **[NEW] WS-BUILD-CONNECT-GPU scope ceiling** — S/M class. One connection type on one existing tile. If it grows past M, STOP and say why. Governed by `test_connect_gpu_scope_S_or_M.py` (LOC ceiling + banned-generic-name grep).
14. **[NEW] Product surface discipline** — spine app runs at pod preview URL behind owner-bearer-token auth. Token generated once at `/app/backend/.owner_credentials` (mode 0600, never committed to any repo, never appears in logs or STATE). Pod operator hands it over.
