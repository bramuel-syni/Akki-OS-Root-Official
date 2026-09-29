# M2 — Grey Mirror and the Watch: readiness, implementation and closure

29 September 2026. Owner directive: “finish M2 cleanly in one autonomous run … same three steps
as M1 (readiness review, implementation, testing) … same depth of front end as Registry.”
Governing source: `Akki_Goal_Roadmap_v1.md` §M2 (M2.1–M2.4, M2-T1–T5, Gate G2). Design source:
Canon 8 *The Watch* (read in full: §§1–21, `notes/chunk1_20260918/canon_text/Akki_Canon_8_The_Watch.txt`).

## Outcome

**G2 verdict: PASS on the currently admitted path inventory (three commission gates + the Watch
console), with the standing limits in §6 recorded — not an all-clear.** Every declared rail on that
inventory now has a full-loop receipt and a measured effect: detect → verdict → policy row → real
gate effect → append-only record → console → witness digest → release by its own authority. M2-T1
and M2-T2 were drilled live in iteration 62; M2-T2 (severance release authority), M2-T3, M2-T4 and
M2-T5 were drilled live in this run (`tests/census_operational/test_watch_m2_live_drill.py`, 8/8) and
independently re-verified (iteration 63: 29/29 live backend, all four panels at 1920×800 and 390×844,
zero overflow). Offline isolated-store proofs: `test_watch_commission_gate.py` (6) +
`test_watch_m2_full_loop.py` (8). **Opens M3.**

## 1. Authoritative design read — what Canon 8 requires of this milestone

| Canon 8 | Requirement (verbatim anchor) | Where it now lives |
|---|---|---|
| §6/§7 two engines | eyes never act, hand never judges; deterministic ladder annotate/shape/contain/sever; sever only from the closed six-signal registry | `macho.py`, `mkono.py` (reused unchanged); gate detectors are `externally_steerable` by construction; `tripwire.convict` is the only structural path |
| §7 ceilings | blast budget, friction budget as measured numbers | `console_projection.budgets` (State gauges; DEFAULT ceilings named) |
| §7 hysteresis | contain-release-contain is a reportable anomaly | `_detect` stamps `anomaly: contain_release_contain` on the detection row |
| §10 the mark | minted on conviction, binds identity/credentials/session/device/behaviour/content hashes; every gate evaluates mark state on every pass; de-marking is human, dual-control | `tripwire.convict` → `mark.mint_mark`; `commission_gate.sever_state` evaluated first in `_enforce` at all three boundaries; `decisions.act` executes release only on two distinct operators |
| §11/§12 mirage | Sarabi degrades into a tripwire, never a hole; lies outward never inward; shares no store with production (measured, not filtered); innocent release carries the reconciliation duty; silent success-that-wasn’t is never an exit | `tripwire.plant` measures store disjointness against 7 production stores before planting; touches are truthfully-marked `MirageTouch_v0` rows; the decoy is on record one-way (hash); release always writes a notice with `attempts_not_landed` (notify posture — owner default until ruled) |
| §13 console | four panels; State never renders all-clear; Record three lanes + evidence walk that renders broken when incomplete; Under watch curves/mirage/marked/re-declaration/de-mark routing; Decisions dual control, side-by-side records; negative space | four bound views (§3); `never_all_clear` string; `walk.complete=False` renders “Walk incomplete”; no thresholds/placement/dimensions on any surface |
| §15 disagreement | containment first, a person resolves from Decisions with both records side by side | Decisions item carries `watch_record` and `governance_record` columns |
| §16 witness | workers attest each other’s digests; break-in test on schedule must fail | `witness_binding.attest_action` at every mint; `witness_binding.break_in` via `POST /api/portal/watch/witness/break-in` (measured `passed`; drift → `TamperAlarm_v0`, proven offline) |
| §17 truth conditions | totality of sight on the inventory; verdict coverage; response determinism; fail-closed independent of the Watch | `crossing()` fails 503 closed when the feed cannot be written; custody gates (`admission_path`) were never conditioned on the Watch |
| §14 CIF / A5.22 | detection findings CIF may metabolise; proposes-never-ratifies; versioned requirement | `learning_loop.propose` → `services.cif` (detection → acceptance point → L-4 routing) → `research_queue` → Decisions → `ratify` writes `watch_requirements/v{n}.json`; detectors read the ratified version; old verdicts keep their label |
| §20 ruled values | five owner-only values; conservative defaults until ruled | mirage entry threshold NOT autonomous (highest bar), reconciliation mode = notify, six-member registry unchanged, thresholds DEFAULT until `requirements=v1` |

## 2. Reuse crosswalk — the work was connection, not a new engine

Read word for word before any code: `services/watch/{macho,mkono,mark,mirage,mirage_artifacts,
mirage_provocation,persistence,sever_signals,witness,continuity,containment,certificate_library,
research_queue,capability_admission,router}.py`, `services/cif/{detection,acceptance_point,
output_routing}.py`, `services/grey_mirror/router.py`, `routers/{watch_operational,census_operational}.py`,
`contracts/{watch_action_v0,mark_v0,mirage,mirage_artifact_v0,sever_certainty_signal_v0,
witness_identity,cif_proposal_v0}.py`, drills `canon_8_25`, `canon_8_26`, and the Nexus fragments
`mirror` (L8441–8691) and `watch` (L7233–7360).

| Existing mechanism | Found state | Change made |
|---|---|---|
| `commission_gate` (iteration 62) | contain/shape effects, lazy release on the subject’s next crossing, no sever, no mark check, no notice | sever/mark check first on every pass; tripwire hook; reconcile on every read; notices; witness attestation at mint; requirements label; hysteresis flag |
| `mark.mint_mark` / `mark_hits_for_hash` | writer + reader only; no gate consulted marks | consumed by `sever_state`; de-mark = dual-control `release` row (mark file untouched, §43) |
| `mirage.plant_mirage/record_touch` | legacy `engage_mirage` on the W10 verdict grammar | reused the writers; conviction goes through the CP-C2 `MachoVerdict(structural_certainty)` + registry signal instead of the legacy action grammar |
| `mirage_artifacts` bleed check | only compared env-set dirs (nothing when defaults apply) | `tripwire.isolation_check` compares the effective mirage dir with all 7 effective production dirs; result recorded on the `mirage_planted` row |
| `witness.attest_watch_action`, `run_standing_break_in_test` | implemented, never called by a live path; no identity registered | `witness_binding` registers `wi_gate_record_witness` (note declares no Watch/governance credentials and the pod placement gap) and binds both |
| `research_queue.run_research_loop_step`, `cif.*` | order-enforcing loop + CIF surfaces, no producer | `learning_loop` is the producer; human ratification is the Decisions dual-control item |
| `watch_operational.state_for` | records + counts only | full four-panel projection (`console_projection`) on the same records |
| Legacy `/api/watch/*` mutation routes | 409 quarantine | unchanged (verified 401/409) |
| Nexus `mirror`/`watch` fragments | bound only for the Record view; State tiles “—”, Under watch static sample text `ACT-1189`, Decisions empty | all bindings filled from the envelope; L7300 sample text replaced by the real marked lines; one additive footer link on L7353 for the research-loop entry (the prototype has no other control for it) |

No new detector, ledger, effector class or verdict grammar was invented. Thresholds remain seam
defaults; the closed registry is untouched; `destroy` still does not exist.

## 3. UI/UX contract — the four constitutional panels, bound to one record

| Panel (route) | Fragment lines | Bindings now real |
|---|---|---|
| State `/watch/state` | L8453–8573 tiles/G2/G3/chart, L8617–8660 ledger, L8665–8691 aside | `waiting/actors/sessions`, `allowed/refused/flagged`, `checks/exceptions/recovery` with “Behind the” popovers; chart select Activity (crossings per boundary) / Responses (per action class); budget gauges in the chart foot; ledger rows with state chips and the evidence walk drawer; `never_all_clear` one-liner |
| Record `/watch/record` | L7236–7255 | lanes All/Observation/Action/Decision; rows carry lane (noted/acted/held), state (Recorded / In effect / Held / Released / Executed), “The notice we sent →” where a notice exists, “Walk this →” with the six-step walk; refresh chip |
| Under watch `/watch/under-watch` | L7262–7301 | per-principal nine-day refusal curves (inline SVG), “Watch closer” (read-only evidence), “Ask for an updated declaration” (real notice + record), mirage copy/findings (isolation measurement, live decoys, touches; no construction/placement), Marked (real subjects, standing, 6 dimensions bound, notified; no dimension values), “Request removal of the mark” → Decisions |
| Decisions `/watch/decisions` | L7305–7353 | items ranked by blast, Review expands “The Watch’s record” / “Governance’s record” (or “Research loop”), one-line note required, Approve (n of 2) / Decline / Acknowledge only; executed/declined items show the ✓ line; footer with open/closed counts and the live requirements label + research-loop entry |
| Bell (all OS pages) | L38–68 | Watch notices for the signed-in principal merged with work notices (“Work and Watch notices”) |

Layout, CSS and DOM of the owner prototype are unchanged; bindings and data-testids only. Verified at
1920×800 and 390×844 with zero horizontal overflow (iteration 63).

## 4. Implementation (files)

Backend `services/watch/`: `commission_gate.py` (extended), new `tripwire.py`, `decisions.py`,
`notices.py`, `learning_loop.py`, `witness_binding.py`, `console_projection.py`; `operational_reads.py`
(envelope); `routers/watch_operational.py` (routes below); `services/enforce/census_identity.py`
(one-way `session_ref`/`device_ref` for mark dimensions — never the raw token or agent string).

Routes (all tenant-bound; operator/master_admin unless stated): `GET /api/portal/watch/state`
(+ legacy aliases), `GET /api/portal/watch/notices` (any admitted member, own only),
`POST /api/portal/watch/decisions/{id}` `{act: approve|decline|acknowledge, note}`,
`POST /api/portal/watch/requests/demark`, `POST /api/portal/watch/requests/redeclaration`,
`POST /api/portal/watch/learning/propose`, `POST /api/portal/watch/mirage/plant`,
`POST /api/portal/watch/witness/break-in`.

Frontend `components/prototype/`: `watchStateModel.js`, `watchRecordModel.js`, `watchUnderModel.js`,
`watchDecisionsModel.js`, `useWatchRecords.js` (+ `useWatchNotices`), wiring in
`useNexusExperience.jsx`; `OwnerMarkup.jsx` interpolation now tolerates whitespace around an exact
`{{ }}` binding (needed for the curve element the prototype places as a bare text node).

Stores (append-only, env-overridable like the existing Watch stores): `phase0/watch_observations/`,
`watch_decisions/`, `watch_notices/`, `watch_requirements/`, plus the existing verdict/action/mark/
sever-signal/mirage/witness stores.

## 5. Drill pack — M2-T1…T5, live on the deployed backend

Subjects: `demo.analyst` (T1/T2, iteration 62), `demo.dpo` as the isolated severance subject
(this run), approvers `demo.operator` + `demo.master_admin`. Nothing was dispatched to any worker:
every gate crossing used an invalid phase or a decoy descriptor.

| Run | Evidence | Result |
|---|---|---|
| M2-T1 Detect and respond | iteration 62: `mv_gate_ccfd9202c812`→`ma_gate_63fd3485b58f` (fast_violation→shape, 429 with receipt); `mv_gate_adb54a6af141`→`ma_gate_0aa280248082` (slow_play→contain, 409 with receipt); this run: `mv_gate_505031dd5f5e`→`ma_gate_505031dd5f5e` (mirage_incrimination→sever, 403, walk complete with witness `wa_gate_614e33314bea`) | PASS on the three named detectors; response latency inline (same request) |
| M2-T2 Legitimate use and release | benign operator traffic: zero verdicts (offline `test_benign_operator_traffic_stays_within_friction_budget`; live iteration 62 T2); high suspicion (8 refusals) reached `contain`, never `sever`; expiry release reconciled on READ with notice (`expired_clean`, `attempts_not_landed`) — see §5a; severance release only by two distinct operators (`wd_1be2814bcdf4`: acknowledge → open, first approval → open, same approver again → 409, second approver → executed → DPO’s next crossing reached the handler, 422) | PASS |
| M2-T3 Mirage and marks | decoy planted with isolation measured against 7 stores (`mr_gate_ce1aa789274a`); touch `mt_gate_505031dd5f5e` recorded truthfully; artefact in the isolated store; mark `mark_gate_505031dd5f5e` (6 dimensions) checked at `census.plan`, `language_cognition.commission`, `census.commission` → 403 each with an effect receipt, reads unaffected (200), no dimension or hash in any response; overlap → planting refused (offline) | PASS |
| M2-T4 Failure and response integrity | feed unwritable → 503 fail-closed, handler outcome never leaves (offline); witness gap → `witness_gap` row (incident, not a log miss); break-in via production writer refused (`write_once_violation`), `immutability_measurement=passed` live; on-disk drift → `TamperAlarm_v0` (offline); console acknowledgement left protection active (live) | PASS |
| M2-T5 Learn without self-authorising | `cif_watch_71a04299eb53` authored → acceptance point → `research_loop_appended` → grounding `watch.learning_loop.citation_resolution` → `wd_6ac4580d762a`; one approval did nothing; two distinct approvals wrote `watch_requirements/v1.json`; new verdicts cite `requirements=v1`, the earlier verdicts still say `thresholds=DEFAULT_PENDING_OWNER_RULING` (offline proof of replay under the version and of unchanged history) | PASS — non-GPU change only; GPU-dependent learning remains M9 |

### 5a. Expiry release of the T1 innocent (analyst)

`ma_gate_0aa280248082` (contain, TTL 3600 s from 07:21:20Z) — see the addendum at the end of this
note for the reconciliation row written at the first read after 08:21:20Z.

## 6. Standing limits — recorded, not hidden

- **Admitted path inventory is three commission gates + the console.** Mark evaluation at
  authentication, invocation and egress gates is not yet in the inventory (M3+ extends and reruns it).
- **Independent watchdog not placed.** The record witness runs in the application pod; “Watch silence
  is itself an alarm” needs a separately deployed watchdog (candidate: akki-vm, no Watch credentials).
- **Learned detectors not wired**; behavioural signature (§9) and profile custody are not built.
  Detectors are deterministic counters under DEFAULT thresholds, now versioned as `requirements=v1`.
- **Mirage entry above containment is not autonomous** (owner has not ruled the entry threshold;
  highest bar holds). The misdirection arm exists only as the tripwire path.
- **Jittered bands not implemented**; hysteresis is flagged, not enforced as a cooldown.
- **Budget gauges measure drill traffic**: after the analyst’s release the friction gauge will show the
  drill’s effects on a released-clean subject as friction (a standing finding by §19 — the ceiling is
  DEFAULT class and the subject was a drill actor, but the gauge is not softened).
- Two escaped-isolation artefacts from the first offline test run (three stray witness attestations
  for tmp actions; one `p-analyst` notice) were removed from the real stores before any drill.

## 7. Verification and read limits

Offline: `pytest tests/census_operational/test_watch_commission_gate.py test_watch_m2_full_loop.py`
(14 passed, isolated stores). Live: `test_watch_m2_live_drill.py` 8/8; iteration 63 (`test_reports/
iteration_63.json`) 29/29 live backend, four panels desktop+mobile, bell, zero overflow. Frontend
unit suites unchanged: 31/31. Not read this increment: `services/watch/{input_seat,fitness,
route_recheck_failure,route_staleness_flag,ledger_chain_break_signal,signature_primitive,
schema_verdict}.py` beyond signatures — none is on the admitted M2 path.
