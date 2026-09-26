# Akki — all35assurance promises

Product promise#N is distinct from S-N. Read-only assessment; closure scenarios below have NOT been executed.



## S-1

> The system will observe every actor, input, and action across the estate and the AI it runs, with no path by which any of the three reaches the estate or a model outside that observation.

**Bound/ruling:** Structural — held by two independent proofs (static, runtime), not a numeric bound

**Requirement links:** ["REQ-408"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Enumerate and instrument every admitted actor/input/action boundary, including model, tool, internal handoff and estate adapters; bind enforcement to a receipted inventory rather than only the LLM router.

**Acceptance demonstration:** Attempt one authenticated route/tool crossing outside the admitted observer map: block it before side effect; normal crossings produce correlated actor/input/action observations.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-2

> The system will detect the machine-speed attack, the slow play beneath every threshold, and the authorised attack that never breaks a rule — each by a distinct, named mechanism.

**Bound/ruling:** Unruled — detection latency per shape not confirmed to a value

**Requirement links:** ["REQ-409"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Wire separate fast deterministic, longitudinal conduct and whole-pattern intent mechanisms into the existing certificate process; establish bounded measured detection evidence for each, without claiming omniscience.

**Acceptance demonstration:** Run three controlled no-estate-data drills: machine-speed violation, individually subthreshold sequence and individually authorized harmful pattern; verify the named mechanism and evidence for each.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-3

> The system will route probabilistic suspicion to friction, a narrowed envelope, or the mirage, and will convict only once the actor's own conduct converts suspicion into certainty.

**Bound/ruling:** Ruled mechanism — mirage entry threshold is baseline-period-deferred (Doc 3 Rulings)

**Requirement links:** ["REQ-410"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Connect suspicious cases to reversible friction/mirage and require the actor's observed conduct plus ratified evidence to authorize stronger response; no score-to-sever shortcut.

**Acceptance demonstration:** Submit high-suspicion but uncertified conduct: permit only the reversible ladder; repeat with a valid closed-registry signal and check distinct authority/evidence.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-4

> The system will act on a four-rung ladder — annotate, shape, contain, sever — bounded by a blast budget per window and a friction budget on legitimate work.

**Bound/ruling:** Ruled mechanism, values unruled — blast-budget share and friction ceiling named, not set

**Requirement links:** ["REQ-411"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Connect ladder decisions to real enforcement with tenant/actor/window blast and friction accounting that survives concurrent actions.

**Acceptance demonstration:** Race multiple legitimate-but-suspicious requests at a window boundary; ensure aggregate friction/blast ceilings hold and the correct non-sever response is recorded.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-5

> The system will make every autonomous act reversible, bounded, and witnessed — a time-to-live on every action, atomic act-and-attest, peer-countersigned.

**Bound/ruling:** Unruled — action time-to-live named, no value confirmed

**Requirement links:** ["REQ-412"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Make action/attestation one effective durable boundary with actual rollback/expiry, an independent peer countersignature and no destructive rollback of the ledger.

**Acceptance demonstration:** Interrupt between proposed act and attestation, then restart: no unreceipted action becomes effective; expiry reverses the permitted action while evidence remains.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-6

> The system will write every verdict, action, attestation, and mark to the one authoritative record before the next gate is crossed, including its own mistakes.

**Bound/ruling:** Structural; timing qualitative — “before the next gate,” no numeric latency confirmed

**Requirement links:** ["REQ-413"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Bind every verdict/action/mark/attestation producer to the authoritative writer and acknowledgement gate; reconcile legacy best-effort mirrors versus effective runtime decisions.

**Acceptance demonstration:** Fail the writer before the next governed crossing; the next crossing refuses, and the attempted operation is distinguishable from a committed act.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-7

> SPECIFICATION GAP — no mechanism specified. Doc 3's plain-language promise states the platform “learns from every attack it defeats”; every A5 clause on learning (A5.7, A5.8, A5.12) constrains what may NOT happen. None specifies what does update, on what evidence, at what layer.

**Bound/ruling:** Closed by Watch Learning Amendment L-2, L-4. R-15 (initial library) and R-16 (ratifier, cadence) open.

**Requirement links:** ["REQ-414"]

**Gap:** Historical specification gap is partially superseded by Watch Learning structures, but distributed evidence-to-requirement loop closure is still unproven.

**Work to deliver:** Complete the already-specified Watch Learning loop: observation→CIF proposal→Solva grounded requirement→independent human ceremony→versioned library, with no hot-path self-training admission.

**Acceptance demonstration:** Replay an unsure case: it stays on the reversible floor until a grounded, ratified requirement exists; identical later conduct resolves through that version without rewriting past actions.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new (spec-closed, 13 Sep 2026)"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-8

> The system will exercise every response rail on a standing drill cadence — full loop, both engines, latencies measured — and a rail not demonstrated firing is not in force.

**Bound/ruling:** Ruled mechanism, cadence value unruled

**Requirement links:** ["REQ-415"]

**Gap:** Standing drill counters/receipts surfaces exist, but this assessment run did not execute drills; firing proof remains inherited evidence only.

**Work to deliver:** Bank actual end-to-end scheduled drill receipts for each response rail, both detection and response, with timestamps and disablement of unproved rails. A test helper is not a standing operational drill.

**Acceptance demonstration:** Withhold a rail's qualifying drill receipt: it cannot be marked in force. Execute the full safe drill and verify measured detection-to-action latency and restoration.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-9

> The system will, on release from the mirage, replay the actor's mirage-period work against the real platform, or tell them plainly it did not land.

**Bound/ruling:** Ruled mechanism — reconciliation mode is baseline-period-deferred

**Requirement links:** ["REQ-416"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Connect mirage exit to authorized production replay with per-operation idempotency, scope checks and explicit non-landed outcomes.

**Acceptance demonstration:** Perform permitted writes in mirage, then release twice: each authorized real effect occurs at most once; denied effects remain absent and the actor receives an explicit non-landed record.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-10

> The system will restore Ledger continuity within 3,600 seconds, under independent countersign, following any continuity-affecting incident.

**Bound/ruling:** Ruled — CA1-N5, RTO 3,600s, DEFAULT-class, revisable on incident evidence

**Requirement links:** ["REQ-417"]

**Gap:** A bound/helper/incident shape is not operational proof of the timed restoration or notification duty; actual independent recovery/delivery evidence remains required.

**Work to deliver:** Demonstrate real Ledger recovery under the3600-second bound with an independent countersigner and verified pre/post chain continuity; separately rule RPO and whole-site loss.

**Acceptance demonstration:** Disable the primary writer infrastructure in an approved recovery exercise; restore a verified head within the bound using a countersigner not dependent on that infrastructure.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-11

> The system will issue breach notification within 72 hours of a qualifying incident, to the parties and authorities the incident requires.

**Bound/ruling:** Ruled — CA1-N2, 72-hour duty

**Requirement links:** ["REQ-418"]

**Gap:** A bound/helper/incident shape is not operational proof of the timed restoration or notification duty; actual independent recovery/delivery evidence remains required.

**Work to deliver:** Connect incident qualification, required recipients, approved content, reliable timers and durable delivery acknowledgements for the72-hour notification duty.

**Acceptance demonstration:** Start a qualifying incident with an unavailable delivery channel; exercise retry/escalation and bank timestamped receipt for every required recipient within the duty period.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-12

> The system will fail closed independent of the Watch — custody gates fail closed on their own, with or without the Watch above them.

**Bound/ruling:** Structural

**Requirement links:** ["REQ-419"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Validate independent refusal at each custody/TCB gate with Watch unavailable, preserving the explicitly safe-open registry-read exception and standing containment state.

**Acceptance demonstration:** Stop Watch without altering custody configuration; a prohibited egress still refuses while previously committed permitted registry reads remain correctly marked.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-13

> The system will never let detection hold power to act, or response hold judgement to interpret — Macho asserts facts only; Mkono executes signed policy only; one verdict is the sole interface.

**Bound/ruling:** Structural

**Requirement links:** ["REQ-420"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Enforce capability/credential separation between Macho assertions and Mkono signed-policy actions across every caller, with the sole typed verdict interface.

**Acceptance demonstration:** Give Macho a valid detection record but no response authority: direct action is impossible; give Mkono a malformed/score-bearing judgment payload: it refuses interpretation and action.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-14

> The system will never unlock its maximum autonomous force from a signal an outsider could fabricate — only from a closed, six-member registry of unfakeable signals.

**Bound/ruling:** Structural; registry membership is baseline-period-deferred

**Requirement links:** ["REQ-421"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Bind maximum force exclusively to the six admitted unfakeable signals, with authenticity, freshness and provenance checks on the signals' producers.

**Acceptance demonstration:** Fabricate outsider-controlled content resembling a signal and replay an old signal: neither unlocks maximum force; an admitted current signal follows its recorded policy.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-15

> The system will never let loss of behavioural conformance alone convict an actor — the worst it can do to an innocent actor is return them to baseline verification.

**Bound/ruling:** Structural, constitutional per A5.7 — not tunable

**Requirement links:** ["REQ-422"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Keep behavioral-conformance loss outside conviction/severance inputs and wire the bounded return-to-baseline path.

**Acceptance demonstration:** An otherwise legitimate principal drifts from its profile with no unfakeable signal: restore baseline verification without severance or irreversible sanction.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-16

> The system will hold a ruled, deterministic floor beneath every adaptive layer, moved only by a delayed, two-signature ceremony that is itself a monitored tripwire.

**Bound/ruling:** Structural — floor values are the conservative defaults during the baseline period

**Requirement links:** ["REQ-423"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Connect adaptive proposals to immutable deterministic floors and the delayed two-signature witnessed ceremony, preserving current in-force policy through partial apply.

**Acceptance demonstration:** A learner or single operator proposes a weaker floor; no live change occurs before the required delay/signatures; a failed apply leaves the prior floor effective.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-17

> The system will never delete — the Watch can stop anything and erase nothing; destruction remains solely the separately-authorised act specified elsewhere.

**Bound/ruling:** Structural

**Requirement links:** ["REQ-424"]

**Gap:** Watch-side no-delete posture is present, but separately authorized erasure pathways remain permissible and must be governed/proven separately.

**Work to deliver:** Preserve Watch stop/contain authority without deletion capability; independently authorize any retention erasure and keep its own custody record.

**Acceptance demonstration:** Exercise every Watch action with delete-capable APIs instrumented: none invokes destruction; a separately lawful erasure follows the distinct authorization path.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-18

> The system will hold behavioural-conformance profiles as non-exportable, tenant-keyed, purpose-bound armoury — never rendered to any surface, export, or analytic, including the Watch's own console.

**Bound/ruling:** Structural; retention posture is baseline-period-deferred

**Requirement links:** ["REQ-425"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Enforce tenant-keyed encryption, purpose/use controls and non-exportability of conformance profiles across API, console, exports, analytics and logs.

**Acceptance demonstration:** Request another tenant's profile and attempt same-tenant operator export/console rendering; all refuse without profile content entering error logs or analytics.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-19

> The system will have its own liveness attested by a component holding no Watch credentials, will treat Watch silence itself as an alarm, and will subject its own records to a standing break-in test that must fail.

**Bound/ruling:** Structural; break-in test cadence unruled

**Requirement links:** ["REQ-426"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Deploy and demonstrate a genuinely independent liveness witness and standing tamper probe whose credentials cannot administer Watch.

**Acceptance demonstration:** Stop or tamper with Watch while its own credentials are unavailable: the independent witness alarms; the break-in probe cannot modify protected records.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-20

> The system will execute every task under exactly one authority's identity and scope — a task that could see like security and decide like governance is unrepresentable, not merely forbidden.

**Bound/ruling:** Structural — unrepresentable, not policy-enforced

**Requirement links:** ["REQ-427"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Propagate one immutable authority/scope per task through every async job and handoff; reject mixed security/governance scope rather than merely logging it.

**Acceptance demonstration:** Try to construct or mutate a task into a dual role across a handoff: construction/consumption refuses before privileged effects.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-21

> The system will let the mirage deceive outward only — every mirage interaction writes truthfully marked records, and mirage state shares no store with production.

**Bound/ruling:** Structural — mirage entry threshold is baseline-period-deferred (cross-ref S-3)

**Requirement links:** ["REQ-428"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Separate mirage storage/credentials from production and stamp truthful mirage provenance on every record and replay proposal.

**Acceptance demonstration:** Correlate one actor's simultaneous mirage and production sessions: no shared mutable store or crosswrite; auditors see genuine mirage markers even where outward interaction is deceptive.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Present"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/macho.py", "start_line": 82, "end_line": 178, "sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_sha256": "821f854e23f284646f3eebcbe638e03f10dea4be1be10f38d8f92f9e0f34bad3", "reviewer_end_line": 178}, {"file": "backend/vendored/extraction_akki/backend/services/watch/mkono.py", "start_line": 94, "end_line": 189, "sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_sha256": "ae71b38a6ba02c602133d8a21380a5b1e1f60dd88bb31de3d244049b17f1dd0d", "reviewer_end_line": 189}]



## S-22

> The system will inspect what leaves, not only who sends it — every output leaving a component boundary is checked for controlled-unit content and tagged ADVISORY where it recommends, ranks, proposes, or evaluates an action.

**Bound/ruling:** Ruled — reproduction threshold and probe design are R-8 (DEFAULT-class, conservative, revised on evidence)

**Requirement links:** ["REQ-429"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Apply controlled-unit inspection and advisory classification to every component-output boundary, not just the final LLM response.

**Acceptance demonstration:** Attempt a tool result, report, recommendation and internal handoff containing controlled material or untagged action advice: enforce the correct boundary-specific redaction/refusal/tag.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/dap/boundary.py", "start_line": 21, "end_line": 86, "sha256": "9daf16166571121857366916ecd3c69bca2987e4b0b5825b15f6c59b7cf219ae", "reviewer_sha256": "9daf16166571121857366916ecd3c69bca2987e4b0b5825b15f6c59b7cf219ae", "reviewer_end_line": 86}]



## S-23

> The system will treat a coalition as one actor — cumulative conduct across principals sharing a party, a mandate lineage, or a detected coordination signature is evaluated jointly, not per principal.

**Bound/ruling:** Structural for shared-party and shared-lineage membership; coordination-signature threshold is R-11 — inferred, friction-only under A5.2

**Requirement links:** ["REQ-430"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Derive party/mandate/coordination aggregation from authoritative identity and receipted conduct, with cross-principal atomic budgets and tenant-safe linkage.

**Acceptance demonstration:** Split a prohibited cumulative pattern across principals under one party or mandate; the aggregate gate triggers without combining unrelated tenant identities.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/dap/coalition.py", "start_line": 35, "end_line": 217, "sha256": "309bf1011db1de12ae1ed1007aa508e7eb3109dc71ef5a281796b4ee11e3b4ad", "reviewer_sha256": "309bf1011db1de12ae1ed1007aa508e7eb3109dc71ef5a281796b4ee11e3b4ad", "reviewer_end_line": 217}]



## S-24

> The system will hold the raiser of a finding to the same conformance as its target — a finding is conduct; the friction it causes is charged to the raiser's budget, not the target's; a finding not borne out accrues drift on the raiser; and no agent-raised finding, at any count, is an input to severance.

**Bound/ruling:** Structural — A5.2's registry unchanged; friction debit follows A5.14's existing budget

**Requirement links:** ["REQ-431"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Charge finding-induced friction to the raiser's governed budget, record unsupported-finding drift, and exclude finding volume from severance authority.

**Acceptance demonstration:** Flood a legitimate target with agent findings: target budget is not exhausted, raiser costs/drift accrue, and no count of findings itself permits severance.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/research_queue.py", "start_line": 74, "end_line": 123, "sha256": "f4eb134c14902160961a204a5cda41c0780f4aa5a6c153939f35a0a9ae067b54", "reviewer_sha256": "f4eb134c14902160961a204a5cda41c0780f4aa5a6c153939f35a0a9ae067b54", "reviewer_end_line": 123}]



## S-25

> The system will bound what the estate releases in total — across all parties, all operations, all time — so that no combination of parties can reconstruct what none of them is entitled to. Breaching the bound is a floor violation, severance-eligible without inference.

**Bound/ruling:** Ruled — the budget itself is R-7; per-run (ε, δ) is R-9. The floor never learns (A5.8)

**Requirement links:** ["REQ-432"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Connect lifetime estate release accounting and ruled DP/distance parameters to every actual release, with concurrency-safe irreversible spend and no party-reset bypass.

**Acceptance demonstration:** Two parties concurrently approach the estate ceiling through different output operations: aggregate admission cannot overspend; refusal occurs before release and later recall never refunds prior privacy loss.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/dap/coalition.py", "start_line": 35, "end_line": 217, "sha256": "309bf1011db1de12ae1ed1007aa508e7eb3109dc71ef5a281796b4ee11e3b4ad", "reviewer_sha256": "309bf1011db1de12ae1ed1007aa508e7eb3109dc71ef5a281796b4ee11e3b4ad", "reviewer_end_line": 217}]



## S-26

> The system will remove a unit's influence from every artefact that carried it when the right to that unit ends — by re-derivation or recall, findable by registry query, with the release budget's prior consumption left unrefunded.

**Bound/ruling:** Ruled where sharded (SISA); R-12 open for the unsharded, uneconomic-retrain case

**Requirement links:** ["REQ-488", "REQ-472", "REQ-473"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Complete provenance-indexed withdrawal to affected model/report/compacted artifacts, recall delivery notices or re-derivation, re-admission and no release-budget refund.

**Acceptance demonstration:** Revoke a unit used by multiple artifact hashes; registry query finds every descendant, no old artifact is served, replacement passes its own gates, and spent budget remains spent.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/dap/pruning_unlearning.py", "start_line": 102, "end_line": 149, "sha256": "c5f638f1bb1828fd544bdbb0dfeed818967234be472f21956f3235b5ffa2ca70", "reviewer_sha256": "c5f638f1bb1828fd544bdbb0dfeed818967234be472f21956f3235b5ffa2ca70", "reviewer_end_line": 149}]



## S-27

> The system will serve exactly the model it registered — pressure may make it slower, never different — and will say on the record which engine, its own or a provider's, produced every answer.

**Bound/ruling:** R-13 (validation cadence, DEFAULT-class) open; floor explicitly not imposable on the frontier gateway tier — receipt records the boundary instead (V-4)

**Requirement links:** ["REQ-489", "REQ-474", "REQ-475"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Connect hash-verified registered weights/configuration to the real serving engine and controlled-pressure replay, recording actual engine/model provenance with each output.

**Acceptance demonstration:** Hold input/seed/parameters constant under allowed memory/load/hardware placement changes: token output remains exact or serving explicitly refuses; silent precision/context/model substitution fails.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/serving_floor/sfp_8.py", "start_line": 49, "end_line": 75, "sha256": "e334aac03989fc39ec5a8c75d5c437e83e8b2e2c73ba7df78f725b74081e16da", "reviewer_sha256": "e334aac03989fc39ec5a8c75d5c437e83e8b2e2c73ba7df78f725b74081e16da", "reviewer_end_line": 75}]



## S-28

> The system will never act on a verdict it cannot evidence — every Watch action carries a certificate a human can read, and every behaviour it learns to recognise entered its vocabulary through ceremony, not through silent training.

**Bound/ruling:** R-15 (initial certificate library seed) and R-16 (ratifying role, research-queue cadence) open; severance still unlocks only from A5.2's registry — a certificate never does

**Requirement links:** ["REQ-490", "REQ-478", "REQ-479", "REQ-480", "REQ-481", "REQ-482"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Bind actual action authorization to ratified evidence-only certificates and ceremony-versioned requirements; preserve the bounded foundation ladder for uncertified cases.

**Acceptance demonstration:** A learned high-confidence verdict without a valid certificate cannot escalate beyond the foundation policy; a valid certificate references accessible observations and the applicable library version.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/schema_verdict.py", "start_line": 15, "end_line": 31, "sha256": "49dd296e63f82409aa59f1baca50919ddf662ef467c8fa0887022a1d3c7f29bf", "reviewer_sha256": "49dd296e63f82409aa59f1baca50919ddf662ef467c8fa0887022a1d3c7f29bf", "reviewer_end_line": 31}]



## S-29

> The system will admit no new class of action into the world without ceremony on the record — every action names the admission it acts under, and no learner ratifies its own.

**Bound/ruling:** R-17 (class granularity, initial register) open. Learning itself is deliberately ungoverned; exercise is governed at the seams. AC-1's four ceilings are not admissible classes under any ceremony.

**Requirement links:** ["REQ-491", "REQ-483", "REQ-484", "REQ-485", "REQ-486", "REQ-487"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Connect minimum capability admission and four fixed ceilings to all actual agent outputs/actions; separate class proposal from independent ratification and clear admissions on a new artifact hash.

**Acceptance demonstration:** A model proposes its own new class: it cannot ratify or execute beyond foundation authority; a replaced artifact cannot inherit previous admitted classes implicitly.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/watch/capability_admission.py", "start_line": 69, "end_line": 81, "sha256": "4e69f08d72a24d95bd2f80b00540be99eeb3ae82c145ac21d603537223d6b6d7", "reviewer_sha256": "4e69f08d72a24d95bd2f80b00540be99eeb3ae82c145ac21d603537223d6b6d7", "reviewer_end_line": 81}]



## S-30

> The system will make what it holds smaller without losing what it can prove — every compaction is decided by rule, receipted, anchored to its sources, and says on reload what it no longer contains.

**Bound/ruling:** R-19 (triggers), R-20 (retention rule set v1) open; R-21 (user-memory class, consent model) owner input — class ships disabled until ruled

**Requirement links:** ["REQ-541", "REQ-542", "REQ-543", "REQ-544", "REQ-545", "REQ-546", "REQ-547", "REQ-548", "REQ-549", "REQ-550", "REQ-551"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Complete durable compaction publication after receipt, anchored class-preserving reload, loss disclosure and rights-withdrawal propagation to every derived memory artifact.

**Acceptance demonstration:** Fail the ledger before compacted artifact publication, tamper the stored artifact hash, then revoke a cited source: respectively preserve source, refuse reload and recall/rederive the descendant.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/memory/compaction_v1/operations.py", "start_line": 173, "end_line": 190, "sha256": "268a0c43d356449fd7c868e471aecf615552966e249f80073e7ec1daeb330f6b", "reviewer_sha256": "268a0c43d356449fd7c868e471aecf615552966e249f80073e7ec1daeb330f6b", "reviewer_end_line": 190}]



## S-31

> One licence reaches every listed model the buyer's settings admit, resolved at the single chokepoint, metered on the one Ledger, with unlimited local use and no silent fallback — what the buyer sees is what was used.

**Bound/ruling:** R-24 (reseller agreements, counsel) gates reseller-frontier rows only; R-25–R-31 commercial and DEFAULT values open; Local and Your Keys ship without R-24

**Requirement links:** ["REQ-492", "REQ-493", "REQ-494", "REQ-495", "REQ-496", "REQ-497", "REQ-498", "REQ-499", "REQ-500", "REQ-501", "REQ-502", "REQ-503", "REQ-504", "REQ-505", "REQ-506", "REQ-507", "REQ-508", "REQ-509", "REQ-510", "REQ-511", "REQ-512", "REQ-513", "REQ-514", "REQ-515", "REQ-516", "REQ-517", "REQ-518", "REQ-519", "REQ-520", "REQ-521", "REQ-522", "REQ-523", "REQ-524", "REQ-525", "REQ-526", "REQ-527", "REQ-528", "REQ-529", "REQ-530", "REQ-531", "REQ-532", "REQ-533", "REQ-534", "REQ-535", "REQ-536", "REQ-537", "REQ-538", "REQ-539", "REQ-540"]

**Gap:** Entitlement projection logic is structurally present, but producer wiring across all dispatch paths is incomplete/unproven; “projection true” alone does not prove full closure.

**Work to deliver:** Wire owner admission/licence/catalog producers into the existing single chokepoint and derived meter projection; implement correct dials, historical pricing, rollover, scoped keys, ceilings and truthful local fallback.

**Acceptance demonstration:** Run a ruled licence across local, own-key and reseller options; pause/reprice/exhaust/revoke concurrently; each call uses only an admitted path, emits correct terms-versioned quantities and disclosed fallback, with invoice derivable from ledger events.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/entitlement_service_v1/chokepoint_resolver.py", "start_line": 55, "end_line": 149, "sha256": "81900080f03c6daa697d33faa368dd88aad7d3b83f3af07ed83faffe06cb00ba", "reviewer_sha256": "81900080f03c6daa697d33faa368dd88aad7d3b83f3af07ed83faffe06cb00ba", "reviewer_end_line": 149}, {"file": "backend/vendored/extraction_akki/backend/services/portal_operational/entitlements.py", "start_line": 37, "end_line": 116, "sha256": "565bd86546a3a033871f87c1cb10000362fa00d65c44c041482fd60092941f8d", "reviewer_sha256": "565bd86546a3a033871f87c1cb10000362fa00d65c44c041482fd60092941f8d", "reviewer_end_line": 116}]



## S-32

> Every record the platform writes is attributed to an admitted principal whose identity was authenticated and propagated by construction — never to a caller-supplied string, never to a default actor.

**Bound/ruling:** R-22 (rotation default), R-23 (legacy route shapes) DEFAULT-class open

**Requirement links:** ["REQ-552", "REQ-553", "REQ-554", "REQ-555", "REQ-556", "REQ-557", "REQ-558", "REQ-559", "REQ-560", "REQ-561", "REQ-562", "REQ-563", "REQ-564"]

**Gap:** Principal scaffolding exists, but JWT alone is not an admitted trust-domain principal; admission+propagation guarantees remain incomplete.

**Work to deliver:** Audit every record producer for authenticated, admitted, immutable principal context through services/jobs; remove caller-string/default-actor paths without inventing an admission merely from a JWT.

**Acceptance demonstration:** An authenticated but unadmitted identity and a caller-forged principal both fail to write; an admitted task retains its original principal through asynchronous handoffs and cannot mutate it.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/contracts/principal_v1.py", "start_line": 27, "end_line": 117, "sha256": "4769c643157bac3a9595ff7124f3d0dd16368576143ae7445e1a8d02a872efe3", "reviewer_sha256": "4769c643157bac3a9595ff7124f3d0dd16368576143ae7445e1a8d02a872efe3", "reviewer_end_line": 117}]



## S-33

> Nothing a surface says is improvised: every string has a stated purpose and a class; every number comes from a measured field; generated prose is anchored and gated; and where a surface has several true things to say, the one it says first is chosen by rule, and the reason is on record.

**Bound/ruling:** R-32 (Generated surfaces) owner; R-33 (salience classes v1), R-34 (hold), R-35 (retention) DEFAULT-class

**Requirement links:** ["REQ-565", "REQ-566", "REQ-567", "REQ-568", "REQ-569", "REQ-570", "REQ-571", "REQ-572", "REQ-573", "REQ-574", "REQ-575", "REQ-576", "REQ-577", "REQ-578", "REQ-579", "REQ-580", "REQ-581", "REQ-582", "REQ-583", "REQ-584", "REQ-585", "REQ-586", "REQ-587", "REQ-588", "REQ-589", "REQ-590", "REQ-591", "REQ-592", "REQ-593", "REQ-594", "REQ-595"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Connect actual prototype/string slots to registered class/purpose/dependencies, typed rendering, generated-text output gates and deterministic salience receipts; preserve the owner-approved R32 whitelist.

**Acceptance demonstration:** A dependency is unavailable and competing true messages apply: render governed not-measured/refusal copy and record salience reason; uncatalogued generated text or an invented numeric zero cannot ship.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/content_registry/content_registry_vocabulary.py", "start_line": 88, "end_line": 106, "sha256": "10f8d9fbe54307f4391c7a4e17e6bfa0fe27f0b03235c10adfc40636048f82f0", "reviewer_sha256": "10f8d9fbe54307f4391c7a4e17e6bfa0fe27f0b03235c10adfc40636048f82f0", "reviewer_end_line": 106}]



## S-34

> The platform knows, per record, which checks it passed and which it failed; no figure about cleanliness is shown without its checks; nothing that failed structural validity or carries a sentinel enters training or anchors a fact; and every source's strata reconcile to its record count.

**Bound/ruling:** R-38 (sentinel threshold), R-39 (fuzzy tolerance), R-40 (media thresholds) DEFAULT-class

**Requirement links:** ["REQ-618", "REQ-619", "REQ-620", "REQ-621", "REQ-622", "REQ-623", "REQ-624", "REQ-625", "REQ-626", "REQ-627", "REQ-628", "REQ-629", "REQ-630", "REQ-631", "REQ-632"]

**Gap:** Scoped mechanisms exist or are specified, but end-to-end closure with immutable receipts, full producer wiring, and race/refusal proofs remains incomplete.

**Work to deliver:** Implement source-snapshot/pack-bound per-record checks and four-stratum eligibility with explicit incomplete-assessment policy; wire training/fact-anchor consumers and preserve originals/repair lineage.

**Acceptance demonstration:** An unreachable record, sentinel, structural failure, duplicate and reversible defect enter the same assessment: none is silently Clean; the published partition/coverage reconciles and forbidden units cannot train or anchor fact.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/mtafiti/quality_profiler.py", "start_line": 77, "end_line": 112, "sha256": "3fbf07eda79d99fd0d988a0ad1daaf2479d11aca499f0dcf1c0dc12f4fdb6d8a", "reviewer_sha256": "3fbf07eda79d99fd0d988a0ad1daaf2479d11aca499f0dcf1c0dc12f4fdb6d8a", "reviewer_end_line": 112}]



## S-35

> What governance costs is measured and stated: which material entered the window and what was left out, why an entity was withheld from an external model, how fast each class of request is served, how often memory served it warm, and the quality delta of the governed path against the bare model — on every release, in numbers.

**Bound/ruling:** R-41–R-46 DEFAULT-class floors, budgets and thresholds; first-article measurement sets baselines

**Requirement links:** ["REQ-633", "REQ-634", "REQ-635", "REQ-636", "REQ-637", "REQ-638", "REQ-639", "REQ-640", "REQ-641", "REQ-642", "REQ-643", "REQ-644", "REQ-645", "REQ-646", "REQ-647", "REQ-648"]

**Gap:** CC metrics fields and contracts exist, but no fresh release-cycle measurement was executed in this run; metrics promise remains unproven here.

**Work to deliver:** Implement governed entity-knowledge routing, deterministic unit assembly/loss, actual request/ledger/availability measurements and an isolated EX-governed paired capability benchmark before making measured release claims.

**Acceptance demonstration:** Re-derive the same window and exclusions, test admitted/denied disclosure, measure the named tier on actual hardware and run both paths for every held-out task; absent measurements remain absent, never zero cost or claimed compliance.

**Status and limits:** {"status": "PARTIAL", "scope": "read-only code+source assessment", "confidence": "medium", "authority": "Absent → new"} No runtime/API/DB/provider/model/GPU calls executed in this pass; conclusions are bounded to inspected artifacts and prior receipts.

**Code evidence:** [{"file": "backend/vendored/extraction_akki/backend/services/solva_v2/intent_audit.py", "start_line": 15, "end_line": 38, "sha256": "e1f7b3ced1163ae7a2c7c2b4f38720d6c4600151f119feb472ae6ee630934c2f", "reviewer_sha256": "e1f7b3ced1163ae7a2c7c2b4f38720d6c4600151f119feb472ae6ee630934c2f", "reviewer_end_line": 38}]


