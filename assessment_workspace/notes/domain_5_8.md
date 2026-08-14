# Domain 5.8 — The Watch (Canon 8)

Scope (instruction §5.8): input seat · envelope substrate · reconciler · cohort
reading · collision detector · tripwires · mark registry + gate evaluation ·
verdict contract · policy-table executor · response arms · mirage · signature
store · attestation + witness · drill harness · Watch Console.

Instruction: assume nothing exists; confirm absence by search across all four
repos; where anything adjacent exists, name it and judge foundation-or-distraction.
Do NOT deep-read.

## Method — absence search

Search performed against each repo's `git ls-files`:
- Term set A (Canon-8 named actors): `watch`, `macho`, `mkono`, `witness`, `mirage`, `honeytoken`, `containment`, `de[-_]mark`, `mark_registry`
- Term set B (Canon-8 named functions): `tripwire`, `reconciler`, `policy_table`, `cohort_reading`, `collision`, `attestation`, `drill_`, `behavioural_profile`
- Term set C (Watch Console surfaces): `WatchConsole`, `watch_officer`, `under_watch`, `noted_no_action`

## Results per element (per Canon-8 requirement row)

| Row | Canon 8 element | Presence in RMS-IQ-Core-2 / Extraction-Akki | Presence in Akki-OS-V1 | Presence in Akki-Executive-Core | Class |
|---|---|---|---|---|---|
| **C8-004 · C8-005** | Machine speed, cannot act unobserved | ABSENT | ABSENT | ABSENT | **BUILD** |
| **C8-006 · C8-007** | Proves own fitness / break-in tests | ABSENT (no `drill_*` service; no break-in test harness) | ABSENT | ABSENT | **BUILD** |
| **C8-008 · C8-055** | Seam: sensing produces verdict row → response consumes → action row (writer = Macho) | ABSENT | ABSENT | ABSENT (only `services/mtafiti/verdict.py` — different concept) | **BUILD** |
| **C8-009 · C8-010** | Macho sensor | ABSENT | ABSENT | ABSENT | **BUILD** |
| **C8-011 · C8-012 · C8-056** | Mkono responder + atomic act-and-attest | ABSENT | ABSENT | ABSENT | **BUILD** |
| **C8-013 · C8-059** | Witness (no authority credentials; alarms outward) | ABSENT | ABSENT | ABSENT | **BUILD** |
| **C8-014 · C8-057** | Register of marks — dimensions per §10; tenant-keyed; non-exportable; per-mark-class | ABSENT | ABSENT | ABSENT | **BUILD** |
| **C8-015** | Marks do NOT hold biometric identifiers (unrepresentable) | N/A-DOCTRINE (mark register itself absent) | ABSENT | ABSENT | **BUILD** (design rule for future register) |
| **C8-016** | De-mark entries carry two signatures | ABSENT | ABSENT | ABSENT | **BUILD** |
| **C8-017 · C8-018 · C8-058** | Behavioural profiles: parameters only; NO reader on any surface; W13 | ABSENT (no `behavioural_profile` or `signature_substrate`) | ABSENT | ABSENT | **BUILD** |
| **C8-019 · C8-020** | Containment — bounded, reversible, time-expiring | ABSENT (only `memory/JC_CONTAINMENT_PURGE_REPORT_2026_07_04.md` in Executive-Core — an operational memo, not implementation) | ABSENT | ABSENT | **BUILD** |
| **C8-021 · C8-022 · C8-023 · C8-024** | Mirage — planted credentials, honeytokens; innocent-inside vs guilty-inside; construction hidden | ABSENT (zero matches for `mirage/honeytoken/planted`) | ABSENT | ABSENT | **BUILD** |
| **C8-025 · C8-026** | Every containment/mirage has expiry; honest reconciliation | ABSENT | ABSENT | ABSENT | **BUILD** |
| **C8-027 · C8-028 · C8-029** | Reserved decisions (promote / extend / sign de-mark / resolve authority disagreement / cancel ceremony in countdown) | ABSENT | ABSENT | ABSENT | **BUILD** |
| **C8-030 · C8-031 · C8-032 · C8-033** | Watch officer's day: reading is the job; noted-no-action lane; officer NEVER tunes thresholds / browses profiles / sees mark placement / sees mirage internals | ABSENT | ABSENT | ABSENT | **BUILD** |
| **C8-034–C8-039** | Standing drills: seeded input, planted credential, containment expiring clean; fitness in receipts not attestation | ABSENT | ABSENT | ABSENT | **BUILD** |
| **C8-040–C8-044** | Peer authorities; consumption from shared record; disagreement resolution; new-entry-only correction; task identity per authority | ABSENT (backbone ledger exists — 5.2 — but the task-identity register is 5.9 BUILD) | ABSENT | ABSENT | **BUILD** |
| **C8-045–C8-054** | Constitutional negatives (10 explicit forbiddances) | N/A-DOCTRINE (they bind future implementation) | ABSENT | ABSENT | **BUILD** as design constraints |
| **C8-060–C8-065** | What the Watch does NOT do (six items) | N/A-DOCTRINE | ABSENT | ABSENT | **N/A-DOCTRINE** |
| **C8-066 · C8-067 · C8-068** | Interface with CIF — findings cross as detection input; only ratified frames cross back | ABSENT | ABSENT (no CIF implementation on the code side — Chunk 2 shaping evidence) | ABSENT | **BUILD** |
| **C8-069 · C8-070** | Boundary with Doc 9 | 5.9 mirror | 5.9 mirror | 5.9 mirror | **BUILD** |
| **C8-071 · C8-072** | The Watch's promise: makes the platform's OTHER promises viable | N/A-DOCTRINE | | | **N/A-DOCTRINE** |

**All 72 Canon-8 rows: BUILD or N/A-DOCTRINE. Zero REUSE.**

## Adjacencies observed — foundation or distraction?

| Adjacent surface | Location | Judgement |
|---|---|---|
| `rate_limit.py` | `Akki-Executive-Core backend/services/rate_limit.py` (referenced from `routers/auth.py:31`) | **Distraction for Canon 8.** Rate limiting is Canon 3 §30 Enforcement Class discipline, not Canon-8 behavioural authenticity. Foundation for API safety, not Watch. |
| `sentry_setup.py` | `Akki-Executive-Core backend/services/sentry_setup.py` | **Distraction.** Sentry is operator-side error monitoring, not Watch attestation. |
| `security_headers.py`, `csrf.py`, `session_timeout.py`, `privacy_wall.py`, `clamav_service.py`, `rbac.py` | `Akki-Executive-Core backend/services/*.py` | **Distraction.** These are cross-cutting HTTP/security surfaces. Canon 8's Watch is a peer AUTHORITY over behavioural authenticity, not a HTTP-layer defence. |
| `services/chat/protective_layer/__init__.py` (three FM detectors) | Executive-Core | **Foundation (partial).** The three concurrent `shield_invoke` classifiers detecting hypothesis_without_structure / ungrounded_factual_claim / fluency_mistaken_for_diagnosis at DRAFT time is closer in shape to Canon 8's sensing (Macho) than anything else — it senses BEHAVIOURAL failure modes at answer time. However: (i) it produces intervention TEMPLATES, not verdict rows; (ii) it has no seam to a separate responder (Mkono); (iii) it has no drill/attestation cadence. **A useful primitive to draw on, NOT the Watch itself.** |
| `services/signal_dedup.py`, `services/monitor/background_tracker.py` | Executive-Core | **Distraction.** Signal deduplication + engine-signal aggregation for monitor surfaces. Not Watch. |
| `services/inbox_routing/{classifier,routers}.py` | Executive-Core | **Distraction.** Email classification into work-context inboxes, not adversarial detection. |
| `services/backfill_shield_v1.py` | Executive-Core (Chunk-2 (d)) | **Distraction.** One-time chat-audit-row back-fill migration. Not Watch. |
| `.emergent/cron/watch_crons.sh` | all three core repos | **Distraction.** Build-environment cron for hygiene, unrelated to Canon 8. |
| `services/mtafiti/verdict.py` | all three core repos | **Distraction (name collision).** Mtafiti's measurement verdict (Canon 4 §10), not Canon-8 Watch verdict. |
| `contracts/commission_verdict.py` + `services/use_data/commission_verdict_engine.py` | RMS-IQ-Core-2 / Extraction-Akki | **Distraction (name collision).** Use-data commission verdict (Canon 4 §46 licence label), not Watch verdict. |
| `memory/audit/JC_TL_S0_deck_gate_verdict.md`, `memory/rules/DECK_ID_COLLISION_GUARD_RULE.md`, `memory/sprints/JC_CONTAINMENT_PURGE_REPORT_2026_07_04.md`, `backend/scripts/jc_mon_stage_3_gate_a_verdict.py` | Executive-Core | **Distraction.** Operational audit memos about the build (deck ID collision, container purge). Neither implements nor foreshadows Canon 8. |

## Domain 5.8 subtotals

- REUSE: 0
- MODIFY: 0
- RE-POINT: 0
- BUILD: 60 rows (every C8 row with implementable surface)
- N/A-DOCTRINE: 12 (constitutional-negatives cluster + "what the Watch does not do" cluster + doctrinal framing rows)

**Every implementable Canon-8 requirement is BUILD.** Executive-Core's `chat/protective_layer/` is the ONLY primitive shaped anything like Watch sensing, and it is a distraction-adjacent foundation — not a Watch component.
