# Security Amendments · Line-by-Line Extraction

Two amendment change registers:
1. **Security_Promise_Set_Amendments.docx** (files_12) · 8 amendments · 2026-09-03
2. **Security_Amendments_Trojan_Whisper.docx** (files_13) · 10 amendments · 4 new promises · 5 rulings · 2026-09-05

## §A · Promise Set Amendments (2026-09-03) · 8 items

Source: `canon/drops/20260907/extracted/text/Security_Promise_Set_Amendments.txt`. All text below is verbatim from the source document.

### Amendment 1 · S-7 Marked as a Specification Gap, Not a Promise
- **TARGET** S-7 ("Learn"), Security Assurance Promise Set
- **CURRENT** "Update the behavioural signature from every contained incident — above the floor, never at it." Stated as a Present promise.
- **AMENDED** Status changed to Absent → gap. No learning mechanism specified: Doc 3 A1 states platform "learns from every attack it defeats," but every A5 clause touching learning (A5.7, A5.8, A5.12) constrains what may not happen. None specifies what does update, on what evidence, or at what layer.
- **PRINCIPLE** A promise cannot be asserted from the absence of a prohibition.

### Amendment 2 · Recovery and Notification Given a Document Home
- **TARGET** S-10, S-11
- **CURRENT** Both cited only as Wave E rulings (CA1-N5, CA1-N2) with no document text.
- **AMENDED** Proposed as a new Part D of Document 3 ("Recovery & Notification"), housing S-10 and S-11 as formally specified promises. Origination class RATIFIED-EXTERNAL under rule_criteria_spec_v1 §3.
- **PRINCIPLE** A ruled value without a document home is real but unreadable.

### Amendment 3 · "Never Run in Shadow" Relocated Out of the Assurance Set
- **TARGET** A5.4, previously drafted as candidate S-item
- **AMENDED** Removed from security assurance set entirely. Relocated to `akki_governance_architecture_v1` Attribute 9 (Authority & Change Control) as a build requirement on how the Watch is deployed and changed.
- **PRINCIPLE** The assurance set states what the running system does; A5.4 states a condition on deployment itself — a different register.

### Amendment 4 · Six Unruled Bounds Carried Explicitly
- **TARGET** S-2, S-4, S-5, S-19 — Bound/Ruling column
- **AMENDED** Each bound marked Unruled in its own row rather than implied resolved by the existence of a mechanism: detection latency per attack shape (S-2); blast-budget share and friction ceiling (S-4); action time-to-live (S-5); attestation-continuity interval and break-in test cadence (S-19).
- **PRINCIPLE** A named bound with a described mechanism is not the same as a ruled value.

### Amendment 5 · "No Standard" Claim Narrowed to What's True
- **TARGET** S-14, S-15 — Standard column
- **AMENDED** Corrected to cite legal analogues: GDPR Art. 22 and Kenya Data Protection Act 2019 s.35, both establishing right against solely-automated adverse decisions. Marked explicitly as legal analogues, not security-conformance standards.
- **PRINCIPLE** Absence of a security standard is not absence of any standard.

### Amendment 6 · The Watch Upgraded to a Full Reference Monitor Instance
- **TARGET** `akki_governance_architecture_v1` Part 2 Component 7 (The Watch)
- **CURRENT** Tagged "Reference-Monitor-adjacent" — partial instantiation of Attribute 6.
- **AMENDED** Upgraded to full Reference Monitor instantiation. Doc 3 demonstrates all three defining properties: **complete mediation** via A3's totality of sight; **tamper-resistance** via C3's external witness + break-in test; **verifiability** via A2's Mkono "small enough to verify exhaustively."
- **PRINCIPLE** Under-classifying a strong instance is as much an accuracy failure as over-claiming a weak one. G-6's cross-monitor description requirement remains open for MOAC, the distance gate, and the format gate.

### Amendment 7 · A5.9 Added to Attribute 11's Instantiation
- **TARGET** Doc 0 Attribute 11 (Failure Posture), Component 7 build requirements
- **AMENDED** Added as build requirement citing A5.9 (S-12): "the system will fail closed independent of the Watch — custody gates fail closed on their own, with or without the Watch above them." Tagged Attribute 11, status Met.
- **PRINCIPLE** A5.9 is explicitly a failure-posture statement; its absence from Attribute 11 was an oversight.

### Amendment 8 · Scope Statement Required for Eradication, Communication, and Evidence Custody
- **TARGET** Document 3 scope
- **CURRENT** Silent. Doc 3 specifies detect, contain, record, prove, and reconcile. It does not address eradication, external communication, or evidence custody for proceedings — all required by NIST SP 800-61's incident lifecycle.
- **AMENDED** Recommend explicit scope statement in Doc 3, resolving one of two ways: (a) name these three as deliberately out of Watch's scope with named separate function identified; OR (b) declare them open gaps if no such function exists.
- **PRINCIPLE** Silence on a standard lifecycle's remaining stages reads as completeness. Silence needs resolution, not ambiguity by omission.

## §B · Trojan Artefacts & Whisper Threats Amendments (2026-09-05) · 10 items + 4 promises + 5 rulings

Source: `canon/drops/20260907/extracted/text/Security_Amendments_Trojan_Whisper.txt`.

### §B.1 · The two threat classes (verbatim §1)

**Trojan artefacts** — "A model, adapter, or skill file is a container. Under DAP-9 a base model enters the estate's compute; under DAP-10 trained weights leave it. Estate data memorised into weights during training, then egressed as 'the model,' crosses no network boundary, touches no canary, violates no mandate. The data leaves inside the artefact. Conversely, a model arriving already backdoored carries its payload in latent form until a trigger fires, and until then has no conduct to observe."

**Whisper threats** — "A principal acting within a captured, allowable mandate whose output carries the harm: a recommendation that steers a human or another agent to a wrong action; an output that leaks controlled content in permitted form; a finding manufactured to harass a legitimate actor, exhaust the friction budget, or desensitise an operator. A swarm compounds each: coordinated recommendations manufacture consensus; distributed extraction stays under every per-principal threshold; many principals raising the same false finding read as independent corroboration."

**Residual limit stated once** — "a coalition whose membership is only inferred — a coordination signature across otherwise-unrelated parties — can, under A5.2, only ever be routed to friction and the mirage. It cannot be severed on that inference. W-7 is the answer: the coalition is not caught; it is bounded."

### §B.2 · Trojan Artefacts amendments (T-1, T-2)

#### T-1 · Artefact Egress Distance Gate (DAP-31)
- **TARGET** `dap_backend_spec_v1` — new DAP-31, extending DAP-10. Generalises Doc 17 §17.4c.
- **DAP-31 (verbatim):** "No artefact — model weights, adapter, skill file — passes egress until it has been shown, by a probe run as a gate, to sit at or beyond a ruled minimum distance from every controlled unit in its training manifest. The probe samples controlled units from the manifest (sample size ruled), queries the artefact under conditions designed to elicit reproduction, and scores each unit's reproduction. The artefact fails if any sampled unit's score exceeds the ruled threshold. Failure refuses egress, records which units were reproduced and at what score, and returns the artefact to the training job's owner as not registrable. The gate runs after acceptance (MOAC) and before registry entry; an artefact that fails is never registered, and an unregistered artefact cannot leave. The artefact is held in estate compute throughout — it does not leave to be tested. Threshold, sample size, and probe design are ruled values (§5 R-8), and the probe's own code and parameters are system-TCB tier under the Rules Service."
- **DERIVATION** Doc 17 §17.4c generalised; Shokri et al. 2017 (membership inference); Carlini et al. 2021 (training-data extraction); Doc 0 Attribute 7 (fail-closed, non-lowerable).

#### T-2 · Admission Integrity for Entering Base Models (DAP-32)
- **TARGET** `dap_backend_spec_v1` — new DAP-32, extending DAP-9. Uses Doc 3 C1 (mirage) and A5.2 (canary touch).
- **DAP-32 (verbatim):** "A base model entering under DAP-9 is admitted as an artefact principal, carrying: provenance — source, publisher, licence, in the form Document 20's register requires; a cryptographic hash recorded at admission, such that a changed model is a new admission; and a behavioural probe completed before contact with any estate unit. The probe runs the model in the mirage — a synthetic estate sharing no store with production — against a ruled battery: canary prompts constructed to elicit exfiltration or exceed declared scope; trigger scanning for input patterns producing anomalous output deviation; and capability comparison against the party's declaration. A model that touches a canary has produced an unfakeable signal under A5.2 and is refused with certainty. A model exhibiting trigger-dependent behaviour or materially exceeding declared capability is refused with the probe record written. A refused model's hash is retained so that re-submission is recognised. Battery composition and deviation thresholds are ruled values (§5 R-8)."

### §B.3 · Whisper Threats amendments (W-1..W-8)

#### W-1 · Output-Content Gate (A5.15 + DAP-33)
- **TARGET** Doc 3 new A5.15 · `dap_backend_spec_v1` new DAP-33
- **A5.15 (verbatim):** "Every output that leaves a component boundary — a result returned to a principal, a recommendation surfaced to a human, a finding raised to the Watch, a message from one agent to another — passes an output gate before it leaves. The gate is deterministic and sits on the deterministic side of the verdict seam. It performs two checks and no judgement. Content: the output is scored for reproduction of controlled units against the read set of the job that produced it, using the DAP-31 probe applied to text and structured output; an output exceeding the ruled reproduction threshold is refused — the job returns a refusal with the reason, never a redacted output. Advisory tagging: any output that recommends, ranks, proposes, or evaluates an action is tagged ADVISORY and carries the producing principal's identity, the output's content hash, and the units it drew on. The tag is metadata. The gate does not decide whether advice is good; it establishes what the advice contains and who gave it."
- **DAP-33 (verbatim):** "Every operation's output under §4 of dap_backend_spec_v1 passes A5.15 before return to the party. Browse output is exempt — it is aggregate only under DAP-6 and carries no unit content by construction."

#### W-2 · Recommendation Provenance (A5.16)
- **A5.16 (verbatim):** "When a principal takes an action within a ruled window after receiving an ADVISORY-tagged output (A5.15), the action's record carries that output as an input: the recommending principal, the output's content hash, and the interval between recommendation and action. 'Walk this →' from the action reaches the recommendation. When the action is subsequently found non-conformant — refused at a gate, flagged by the Watch, reversed by ceremony, or reconciled as harmful by the mirage — the recommending principal's behavioural signature takes drift proportionate to the recommendation's role, alongside and not instead of the acting principal's. A principal whose ADVISORY outputs repeatedly precede non-conformant actions is, by that record, non-conformant: the pattern is conduct. The window is a ruled value (§5 R-10). Where a human is the acting principal, the action record surfaces the recommendation to them at the point of action, so that acting on advice is a visible choice, not an ambient one."

#### W-3 · Finding Provenance and Sybil Rules (A5.17)
- **A5.17 (verbatim):** "Findings are two classes and are never merged. Class D findings are raised by the Watch's own deterministic detectors — mark hit, canary touch, attestation failure, witness-write attempt, floor violation, mirage incrimination — and carry certainty per A5.2. Class A findings are raised by any learned component, agent, or party principal, and are advisory to the Watch. A Class A finding: carries the raising principal's identity and its conformance at the time of raising; is collapsed, together with every other Class A finding against the same target from principals sharing a party, mandate lineage, or coalition (A5.18), into a single finding — consensus from one lineage is one voice, not many; causes friction to its target that is debited against the raiser's friction budget under A5.14, not the target's; and, where not borne out — the target cleared by mirage reconciliation, or the finding expired without corroboration by a Class D signal — accrues drift on the raiser's signature. No Class A finding, at any count and from any number of raisers, is an input to severance. A5.2's registry is unchanged by this amendment."

#### W-4 · Coalition as a Principal (Att 3 addition + A5.18 + DAP-34)
- **Attribute 3 addition (verbatim):** "A coalition is a principal class: a set of principals evaluated as one for cumulative-conduct purposes. Membership arises three ways. (a) Shared party — every principal admitted under one external party. Structural, deterministic. (b) Shared mandate lineage — a principal admitted by, delegated from, or operating under another's mandate, to any depth. Structural, deterministic. (c) Detected coordination signature — timing correlation, complementary scope, shared targets, across principals related by neither (a) nor (b). Inferred, probabilistic."
- **A5.18 (verbatim):** "Cumulative extraction history (DAP-24), slow-play detection (DAP-4, S-2), and finding collapse (A5.17) evaluate at coalition level. For classes (a) and (b), membership is a graph fact from admission records and the evaluation is deterministic. For class (c), a coordination signature is a Watch detection whose input is inference: it routes the coalition's members to friction and the mirage under A5.6, and under A5.2 may never trigger severance. A class (c) coalition's yield is bounded by the release budget (DAP-35), not by its detection."
- **DAP-34 (verbatim):** "Coalition membership under classes (a) and (b) is recorded at admission and queryable by the estate owner at any time. A party is informed at admission that every principal under it is evaluated jointly with every other. Class (c) membership is recorded when detected and is visible to the owner as a suspicion, labelled as such."

#### W-5 · Structural Independence of Review (QA-3 amended)
- **QA-3 amended (verbatim):** "No principal reviews the output of another principal in the same coalition under A5.18 classes (a) or (b). Independence is a structural property of the review assignment — different party, different mandate lineage — verified against the coalition graph at the moment of assignment, never declared by the reviewer or the reviewed. Where no structurally independent reviewer exists for an output, the review is escalated to a Tier 1 deterministic check (RV-1 through RV-6) where one applies, or to a human, and the absence of an independent reviewer is recorded as a finding against the assignment, not against either principal."

#### W-6 · Mirage Isolation Extended to Outputs (C1 amended)
- **C1 addition (verbatim):** "A principal in the mirage is isolated in both directions. Its outputs of every kind reach no principal outside the mirage: they are intercepted at the output gate (A5.15), captured as mirage records — truthfully marked as such — and, on release without incrimination, replayed or reported under the reconciliation duty exactly as the principal's other mirage-period work is. For the duration of a principal's containment, every member of its coalition under A5.18 classes (a) and (b) is placed under a narrowed envelope, so that neither the contained principal's silence nor its absence signals its state to the swarm. Coalition members are informed of the narrowed envelope as ordinary friction, not as a consequence of another member's containment."

#### W-7 · Estate Release Budget (DAP-35 + Att 7 new mandatory-baseline instance)
- **TARGET** `dap_backend_spec_v1` new DAP-35 · Doc 0 Attribute 7 new mandatory-baseline instance · Rules Service system-TCB tier
- **DAP-35 (verbatim):** "Each estate carries a release budget: a ruled ceiling on the total information released from the estate across all parties, all operations, and all time. The budget is expressed in the estate's natural units per data type — audio-hours, text tokens, units — for raw and derived releases, and as a differential-privacy budget (ε, δ) for derived outputs and artefacts, consumed per release by the mechanism that produced them. Every metered event (DAP-21) debits the budget before the operation returns its result. An operation that would exceed the budget is refused before execution, and the attempt is recorded as a floor violation — an unfakeable signal under A5.2, severance-eligible without any inference about the requester. The budget is a mandatory baseline under Document 0 Attribute 7: set by the estate owner through the system-TCB ceremony; not lowerable by any party or by any operation; identical for every party; and, under A5.8, it never learns — no conformance history, standing approval, or party agreement moves it. Budget consumption is a first-class record queryable by the owner at any time. The remaining budget is never disclosed to any party: disclosure would itself be a release."

#### W-8 · Differentially Private Training by Default (DAP-36)
- **DAP-36 (verbatim):** "Every fine-tune under DAP-9 trains with a differentially private optimiser — DP-SGD or a ruled equivalent — by default. The per-run privacy parameter (ε, δ) is a ruled value, and each run's consumption is debited against the estate release budget (DAP-35) by the optimiser's privacy accountant at run completion. The clipping norm, noise multiplier, and resulting (ε, δ) are recorded on the training manifest and on the registry entry for the resulting artefact. A run without differential privacy is permitted only by explicit estate-owner approval per run, recorded as such under DAP-14's discipline; its artefact is then gated by DAP-31 at a stricter ruled threshold, and its release is debited against the budget in natural units at a ruled multiplier reflecting the absence of a formal bound."

### §B.4 · Rulings required by Trojan/Whisper (R-7 through R-11)

- **R-7** — "The estate release budget (DAP-35): its size per estate, in natural units per data type and as (ε, δ). The single most consequential value an estate owner sets under this document."
- **R-8** — "The reproduction threshold, sample size, and probe design for DAP-31 and A5.15; the battery composition and deviation thresholds for DAP-32. Proposed as DEFAULT-class values set conservatively and revised on evidence."
- **R-9** — "The per-run differential-privacy parameter (ε, δ) for DAP-36, and the natural-unit multiplier applied to approved non-DP runs."
- **R-10** — "The recommendation window for A5.16 — how long after an ADVISORY output an action is attributed to it."
- **R-11** — "The coordination-signature threshold for A5.18 class (c) — the suspicion level at which a set of otherwise-unrelated principals is routed to friction as a coalition."

Sequencing note: "R-7 is needed before any party is admitted commercially under DAP: without a budget, DAP-35 has nothing to enforce. R-8 through R-11 are needed before the corresponding gates are built, and each is proposed as a DEFAULT-class value so that building is not blocked on a final number."

### §B.5 · What remains open after these amendments (verbatim §6)

Three things stated explicitly so they are not rediscovered:
1. A class (c) coalition — coordination inferred, not structural — is bounded by DAP-35 and frictioned by A5.18, and is never severed on that inference. **This is by design under A5.2 and should not be "fixed"**: the alternative is severing on suspicion, which is the condition A5.7 exists to prevent.
2. A recommendation whose harm is not detected — the action it caused passes every gate and is never reconciled as harmful — leaves no drift on the recommender. A5.16 attributes consequence; it does not evaluate advice.
3. The release budget bounds what leaves the estate. It does not bound what a party learns from what it legitimately received and combines with data it already holds outside the estate.

### §B.6 · Build Acceptance Criteria (Table 2 of Trojan/Whisper doc, verbatim)

12 tests, B1-B12, each with a Test and a Pass criterion. Full table preserved in the extracted .txt file. Key tests:
- B1 · DAP-31: seeded verbatim controlled units on egress → probe reproduces above threshold; egress refused
- B2 · DAP-32: seeded trigger on admission → trigger detected in mirage; refused; hash retained
- B3 · A5.15: request whose faithful output reproduces controlled unit → output refused with reason
- B4 · A5.15/A5.16: agent recommends → human acts → action later refused → both signatures take drift
- B5 · A5.17: 5 agents under one party raise same finding → collapsed to one; friction debited to party
- B6 · A5.17: Class A finding expires without Class D corroboration → raiser drift; target not
- B7 · A5.18: two lineages of one party extract complementary scopes → slow-play at coalition level
- B8 · W-5: assign reviewer from reviewed's lineage → refused; escalated; absence recorded
- B9 · W-6: contained agent emits message to coalition member → intercepted; member narrowed silently
- B10 · DAP-35: two parties each under ceiling, combined exceeds estate budget → 2nd release refused; floor violation
- B11 · DAP-36: DP fine-tune → (ε, δ), clipping norm, noise multiplier recorded; budget debited
- B12 · DAP-35: party attempts to read remaining budget → refused; attempt recorded
