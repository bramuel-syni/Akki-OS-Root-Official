READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# SYSTEM_OBJECTIVES_AND_PROMISES_CHARTER.md

**Purpose.** A canon-grounded articulation of what this system is trying to do (Objective) and what it commits to (Promises), traced to verbatim canon clauses. Produced as a read-only bank artifact — no code, no ratchet touch, W2 hard-stopped.

**Date.** 2026-09-13 · **Amended.** 2026-09-13 (Phase B — second grounding pass, close declared absences per owner ruling D)
**Author.** Session agent, resumed from fork; all quotations sourced by opening the named file in this session (STANDING_ORDERS §1 boot protocol).
**Provenance.** Every factual claim below is either (a) a verbatim quote from a canon file opened in this session, cited with its file path and section, or (b) explicitly tagged `[framing, not canon]` — session framing that is not present in any canon file. Nothing else is smuggled in. `[framing, not canon]` tagging is a **standing practice** (owner ruling this session): no silent normalisation of framing into canon, ever.
**Standing.** This is a notes/ bank artifact. It does not amend canon; it reads it. Where a promise is stated below, it points to canon; canon binds, this document does not.

---

## §0. Provenance and Precedence

### §0.1 Session-opened source set (this is what "grounded" means below)

The following files were opened, and read, in this session under the discipline of STANDING_ORDERS §1. Every quotation below is drawn from one of them. **Phase B (2026-09-13) added Canon 1, 3, 5, 6, 7 first-hand and completed Doc-0 Part 3 full-text.**

| Short name in body | On-disk path | Origin |
|---|---|---|
| `Canon-1` | `canon/text/Akki_Canon_1_Custody_Platform.txt` | canon docx converted to txt (Phase B first-hand) |
| `Canon-3` | `canon/text/Akki_Canon_3_Governance_Engines.txt` | canon docx converted to txt (Phase B first-hand) |
| `Canon-4` | `canon/text/Akki_Canon_4_Operating_Engines.txt` | canon docx converted to txt |
| `Canon-5` | `canon/text/Akki_Canon_5_Interface_Architecture.txt` | canon docx converted to txt (Phase B first-hand) |
| `Canon-6` | `canon/text/Akki_Canon_6_User_Journeys.txt` | canon docx converted to txt (Phase B first-hand) |
| `Canon-7` | `canon/text/Akki_Canon_7_Integration_and_Quality.txt` | canon docx converted to txt (Phase B first-hand) |
| `Canon-8` | `canon/text/Akki_Canon_8_The_Watch.txt` | canon docx converted to txt |
| `Canon-9` | `canon/text/Akki_Canon_9_Mkondo_Charter.txt` | canon docx converted to txt |
| `Doc-0` | `canon/drops/20260909/extracted/text/Akki_Governance_Architecture_v1.txt` | drop 2026-09-09, spec-ID `akki_governance_architecture_v1` (per `notes/spec_id_index.md`); Parts 1–3 now full-text first-hand (Phase B) |
| `DAP-Spec` | `canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` | drop 2026-09-09, spec-ID `dap_backend_spec_v1` (per `notes/spec_id_index.md`) |
| `Audio-Plane` | `canon/text/Akki_OS_Audio_Intelligence_Plane_Specification_v1_0.txt` | canon docx converted to txt |
| `OpVal-v1.1` | `repos/Extraction-Akki/docs/requirements/operating_values_v1_1.md` | governed artifact in Extraction-Akki, dated 2026-07-15 |
| `STANDING_ORDERS` | `STATE/STANDING_ORDERS.md` | permanent operational law |

### §0.2 Phase B closure statement

Every canon document referenced by any citation in this charter has now been opened first-hand this session. The 2026-09-13 Phase A "partially read" declaration for Doc-0 Part 3 is closed by first-hand read of lines 360–528 (§3.7 below carries the tabular findings). The Phase A "not opened this session" declaration for Canon 1, 3, 5, 6, 7 (originally §0.3) is closed by first-hand read of each file. **§0.3 is retired; the charter no longer carries cross-quotes from canon it did not open first-hand.**

### §0.4 Precedence order used in this document

Per owner directive (this session): where canon layers rather than conflicts, the working order is:

1. **STANDING_ORDERS.md** — permanent operational law. Overrides nothing in canon on canon's own subject matter, but binds session conduct absolutely (session boot, engagement, build, runtime, GPU, custody).
2. **Canon-1 §5 Precedence** (verbatim, now first-hand): "Doctrine. The twelve above. A specification that contradicts a doctrine is defective. / The promise register. Part VI. A behaviour that breaks a promise is wrong even if it satisfies a specification. / This canon's specifications. The governance, operating, interface, journey, and integration detail carried in the documents that make up this set. / Implementation convenience. Never decisive." And: "Where the two authorities' canons meet, the resolution rule is fixed: within the security domain the Watch canon governs; within the governance domain this canon and its companions govern; at every seam, the peerage clauses of Document 8 and the matrix of Document 9 decide."
3. **Doc-0 (`akki_governance_architecture_v1`)** — the authoritative governance architecture, twelve attributes as a dependency stack. Doc-0 Part 3 §Standing states: "This document is the layer every other Akki specification instantiates ... Where a future specification appears to conflict with a definition in Part 1, Part 1 governs, on the principle Document 16 already applies platform-wide: the foundation does not yield to what was built on it."
4. **Domain specs** — DAP-Spec (`dap_backend_spec_v1`) for the external-party acquisition surface; Audio-Plane for audio modality. Each governs its own domain and explicitly disclaims parallel machinery (Audio-Plane §1.2).
5. **OpVal-v1.1** and **Canon-9 (Mkondo Charter)** — ground the objective and promise language. OpVal-v1.1 fixes evidence classes (FACT/NORM/DEFAULT) for every value; Canon-9 fixes the record matrix and identity register cited by both authorities as the same document.

**Where two canon sources genuinely disagree**, this document does NOT silently pick a winner. It quotes both, marks the divergence, and flags it for owner ruling. See §5 (Divergences and Findings). Phase B (2026-09-13) confirmed: no genuine two-source conflict surfaced across the eight canon files plus Doc-0 Part 3.

---

## §1. Objective

### §1.1 The objective, stated in the system's own words

The canon carries no single sentence titled "The Objective," so this section quotes what canon does say, in the order the dependency stack (Doc-0 Part 1) requires.

**What Akki is** — `Doc-0 Part 1 §Definition`, verbatim:

> "Akki is a governance operating system: software that lets an organisation's AI act on its data and models while making the constraints on that action structurally enforced, evidenced, and answerable to a named authority — rather than policed by review after the fact."

**What the operating chain is accountable for** — `Canon-4 §1`, verbatim:

> "Production is accountable for one thing: that estate material becomes governed intelligence at a stated standard, repeatably, with every unit traceable to its source. Failure looks like output that exists but does not meet the promised standard, cannot be reproduced, or cannot be traced back to what produced it."

**What the second authority is for** — `Canon-8 §1`, verbatim:

> "The Watch is the platform's security authority. It stands beside the governing authority — the six engines of Documents 2 through 4 — as a peer, subordinate to nothing, and it answers the one question the governors structurally cannot: not *was this permitted*, but *was this intended, and is this actor, input, and action what it claims to be?*"

**What the orchestration substrate holds** — `Canon-9 §1`, verbatim:

> "Two authorities now stand on one substrate: the governing authority of Documents 2 through 4, and the Watch of Document 8. Both mint records; both read records; both staff work from shared capacity. Every ambiguity that arises between them is one of three questions — who writes this record, who may read it, and under whose identity is this task acting — and scattering the answers across five documents recreates the ambiguity this charter exists to remove."

### §1.2 The objective, synthesized

`[framing, not canon]` — the following synthesis is the session agent's articulation. It attempts to compress the four verbatim clauses above; the clauses bind, not the synthesis:

> Akki turns an organisation's estate material into governed intelligence — at a stated, measured standard, per-claim traceable to source — while making the constraints on that action structurally enforced, evidenced, and answerable to a named authority. Two authorities stand on one substrate: a governing authority that mines, measures, targets, reasons, and delivers; and a security authority (the Watch) that answers "was this intended, and is this actor what it claims to be?" — as a peer, never a subordinate, with the record matrix and identity register of the Mkondo Charter as the seam neither can silently redraw.

**Provenance of every word above:**
- "governance operating system" / "structurally enforced, evidenced, and answerable to a named authority" — verbatim from `Doc-0 Part 1 §Definition`.
- "estate material becomes governed intelligence at a stated standard, repeatably, with every unit traceable to its source" — verbatim from `Canon-4 §1`.
- "was this intended, and is this actor, input, and action what it claims to be" / "peer, subordinate to nothing" — verbatim from `Canon-8 §1`.
- "Two authorities now stand on one substrate" / "record matrix" / "identity register" — verbatim from `Canon-9 §1`.

### §1.3 What the objective is NOT

`[framing, not canon]`, grounded by exclusion clauses in canon:

- **Not a document platform, not an audio platform, not an "AI product."** Doc-0 Part 1 fixes Akki as a governance operating system — a category. Domain-specific instantiation (audio, documents, structured records) is a modality extension, not the platform itself. Grounded in `Canon-4 §28` ("the pipeline is the same whichever data dimensionality the material belongs to: audio, documents, structured records, images, or any other modality the estate holds") and `Audio-Plane §1.2` ("The audio plane introduces no sibling services").
- **Not a policing-after-the-fact regime.** Doc-0 Part 1 says "structurally enforced ... rather than policed by review after the fact." The distinction is not aesthetic — Canon-4 §23.1 makes it concrete: "The laundering case is not policed at runtime; it is unrepresentable."
- **Not one authority governing another.** Canon-8 §W12 verbatim: "Peer, not subordinate — Neither authority commands the other or writes the other's law." Canon-9 §1 verbatim: "Both authorities stand on it equally; the witness watches both across it."

---

## §2. Promises Traced to Canon

Each promise below is a verbatim canon clause (or a set of them) followed by a one-sentence session-agent gloss. The gloss is `[framing, not canon]`; the clause binds.

The promises are numbered P1–P12 for reference in this charter only; canon does not carry that numbering. Standing-order-derived promises are numbered P-SO-1 and P-SO-2 and labelled as **standing-order-derived operational law**, distinct from canon-doc-derived promises, per owner directive (this session).

### P1 — One record, per the matrix

**Canon-1 §4.3** (Phase B, first-hand), verbatim:
> "There is exactly one record. Nothing maintains a second. Every admission, measurement, commission, operation, answer, refusal, rule change, and access grant writes to a single append-only ledger. No service keeps a local log constituting a separate account of what happened. Working state — a partial count mid-census, a draft not yet committed — is scratch, not record; it becomes record only when finalised and stamped, and the moment of stamping is itself recorded."

**Canon-9 §2**, verbatim (cross-cites Canon-1 §4.3, now itself first-hand):
> "What the law forbids is a second, competing account of the same events. What it requires is exactly this matrix: one authoritative account per record class, with a single writing authority and named readers."

**Canon-9 §3**, verbatim (the matrix header row):
> "Every record class in the platform, its single writer, and its readers. A second writer to any class is a defect on sight; a reader not listed does not read; additions to this matrix are ceremony, and the matrix version in force is stamped on every audit answer."

**Canon-3 §9.3** (Phase B, first-hand), verbatim:
> "The writer exposes append and nothing else. No update path and no delete path exist within the retention window. A correction is a new entry referencing what it corrects, never an edit of what was written. Out-of-scope and refused items are recorded — a system that drops what it declined cannot show what it declined, and the ability to show that is a substantial part of what the record is for."

**Doc-0 §8 (Ledger), BR-8.1**, verbatim:
> "The Ledger accepts and retains records of refused operations on the same terms as accepted ones — a refusal is as much a record as a success."

**Gloss** `[framing, not canon]`: one authoritative account per record class, one writer, named readers, refusals recorded on the same terms as successes. Append-only writer exposes append and nothing else.

### P2 — Detect, never decide

**Doc-0 Attribute 10 §Definition**, verbatim:
> "Decision authority, the power to admit or refuse an operation, may be held only by components on the deterministic side of this line. A learned component may detect, score, rank, propose, or draft; it may not decide."

**Canon-4 §6**, verbatim:
> "Learning detects; the governed matrix decides; the declaration baseline floors; the admission gate admits. This is the single rule that keeps learning from laundering authority into the measure — the learned component produces detections, never verdicts."

**Canon-4 §2 (bullet 1)**, verbatim:
> "Learning never decides. Learned components appear at exactly three points — Mtafiti's inference overlay, Targeta's yield layer, Solva's reasoning faculty. At each, the thing it could corrupt is placed structurally out of its reach: the verdict is a governed lookup, the eligible set is a permutation-checked type, the assertion class is a function with no confidence parameter."

**Canon-8 §W1**, verbatim:
> "The eyes never act; the hand never judges. Detection asserts facts; response executes policy; one verdict is the only interface between them."

**Gloss** `[framing, not canon]`: learning may inform (detect, score, rank, propose, draft); it may never hold the admit/refuse authority. The mechanism at each of the three legitimate learning sites is structural, not review-based.

### P3 — Assertion floor: reasoning strength cannot raise a class

**Canon-4 §23**, verbatim:
> "A conclusion inherits the floor of its load-bearing units' classes. If any load-bearing unit is utterance-class, the conclusion is utterance-class — the weakest load-bearing unit sets the ceiling for the whole. An utterance-class conclusion is asserted as 'was stated,' never as fact. The phrasing is a function of the class, not of how confident Solva happens to be. Reasoning strength is not an input to the class. The computation reads the units' governed classes alone."

**Canon-4 §23.1**, verbatim:
> "The class computation takes the load-bearing units and nothing else — no confidence, no reasoning strength, no evidence weight. The laundering case is not policed at runtime; it is unrepresentable. 'The evidence is overwhelming, assert the utterance as fact' cannot be expressed, because the function computing the class has no parameter through which reasoning strength could ever enter. The signature is the guard, and a signature assertion in the test suite is what keeps it one."

**Doc-0 Component 2 (Solva) §BR-2.1**, verbatim:
> "The two-faculty seam is enforced by an import assertion, not a coding convention — one faculty cannot invoke the other's authority even inadvertently, because the import itself is the enforcement point."

**Canon-8 §W2**, verbatim:
> "Certainty never exceeds evidence. Structural certainty is assertable only from signals an outsider cannot fabricate. Everything externally steerable caps at reversible containment, whatever its score."

**Gloss** `[framing, not canon]`: the class of any output is set mechanically by the class of its load-bearing units; no reasoning strength, however overwhelming, can push a claim above what its evidence supports. The Watch borrows the same discipline whole for its own certainty computation (W2).

### P4 — Two authorities, one substrate, peer standing

**Canon-8 §W12**, verbatim:
> "Peer, not subordinate. Neither authority commands the other or writes the other's law. Disagreement — permitted but not intended — resolves by temporary, reversible containment plus a person, and the disagreement itself is a record."

**Canon-9 §1**, verbatim (excerpted, already cited under §1.1):
> "Both authorities stand on it equally; the witness watches both across it. A question this charter answers is answered here — never by recollection, and never differently in two places."

**Canon-8 §W11**, verbatim:
> "One task, one identity. Every task executes under exactly one authority's identity and scope. Capacity is shared across time; execution is never shared within a task."

**Canon-9 §5**, verbatim:
> "The register's enforcement is structural: no credential scope exists that spans both authorities, so defect D8 — Document 7 §47 — is unrepresentable rather than policed."

**Canon-7 §47** (Phase B, first-hand — the D8 row of the defect classes table), verbatim:
> "D8 · Dual-identity execution | A task holding, or a code path permitting, more than one authority's identity or scope within a single execution — including any evidence crossing between the authorities outside the matrix of Document 9."

**Gloss** `[framing, not canon]`: governance and the Watch are structural equals, held apart by unrepresentable-dual-identity, resolved on disagreement by containment plus a person, with disagreement itself becoming a record. Canon 7 §47 D8 confirmed first-hand.

### P5 — Every autonomous act is reversible, bounded, and witnessed

**Canon-8 §W3**, verbatim:
> "Every autonomous act is reversible, bounded, and witnessed. A time-to-live on every action; a blast budget on every window; act-and-attest atomically, peer-countersigned. Destroy does not exist in the Watch."

**Canon-8 §19 (Blast budget row)**, verbatim:
> "Blast budget — autonomous action per rolling window | ≤ 5% of active actors per hour | DEFAULT · dual-control | Excess queues for human release"

**Canon-8 §W3 (continued)**, verbatim:
> "An action that expires unless renewed converts the false positive from a harm into a delay; a budget converts the autoimmune attack — tricking the immune system into suspending the business — from an outage into a bounded cost; atomic attestation makes weaponizing the Watch impossible to do quietly, which for a detection system is the property that matters. And a power the tool structurally lacks cannot be turned: the Watch can stop anything and erase nothing — deletion remains solely the authority act of Document 3 §27."

**Canon-3 §27** (Phase B, first-hand — Authorized Deletion), verbatim:
> "Deletion is the only path by which material may leave the record, and it is an authority act rather than an operational one. A request names its scope and its reason, carries dual control, and runs a waiting period during which it can be cancelled — the same shape as a rule change, because deletion is the most consequential change a governance value can undergo. It ends in a destruction attestation: what was deleted, under whose authority, on what date, by what method, with a ledger reference."

**Gloss** `[framing, not canon]`: TTL + blast budget + atomic peer-countersigned attestation. The Watch cannot delete; deletion is a governance-authority act. Canon 3 §27 confirmed first-hand.

### P6 — Fail-closed as the reference-monitor default; per-component posture declared

**Doc-0 Attribute 11 §BA-11.2**, verbatim:
> "Every reference monitor and every component inside the Trusted Computing Base fails closed, without exception: an evaluation that cannot complete is a refusal, because a reference monitor that fails open on internal error is not tamper-resistant against the specific attack of inducing that error."

**Doc-0 Attribute 11 §BA-11.1**, verbatim:
> "Every component's failure types are enumerated — the specific ways it can fail to complete an evaluation — rather than covered by a single unqualified 'handles failures gracefully' statement that names no failure and specifies no state."

**DAP-Spec DAP-28**, verbatim:
> "Every gate in DAP fails closed. An approval service that cannot be reached, a metering write that cannot complete, a terms resolution that returns nothing, a ceiling check that errors — each refuses the operation. No path returns estate data, an artefact, or a query result when a governing check could not complete."

**Canon-8 §W10**, verbatim:
> "The service whose compromise would mean going unobserved must be incapable of unobserved existence — and equally incapable of failing anything open. Custody gates fail closed on their own, per Document 1 §4.1, with or without the Watch above them."

**Canon-1 §4.1** (Phase B, first-hand — Fail-closed custody), verbatim:
> "If a custody control cannot execute, the operation does not happen. When material must be de-identified before an external model may see it, and de-identification cannot run, the call is not made. The operation returns a refusal naming the cause. This is enforced structurally: no configuration flag changes it, no code path bypasses it, and an automated build gate fails the build if a path around the control is introduced. Custody controls fail closed; cost optimisations fail transparent."

**Gloss** `[framing, not canon]`: fail-closed is the default posture for every reference monitor and every TCB component; every component enumerates its failure types explicitly; custody gates are structurally independent of the Watch. Canon 1 §4.1 confirmed first-hand.

**Finding**: Doc-0 Part 3 (Phase B, first-hand full-text) STATUS AS OF row for G-11 (line 518 verbatim): `G-11 | failure_posture_v1 | Spec-drafted — platform default plus two departures specified. Not built.` The doctrine is canon; the per-component enumeration is a documented gap in Doc-0 Part 3, spec-drafted in `failure_posture_v1`, not yet built.

### P7 — Objective-blindness of measurement (Mtafiti's foundational rule)

**Canon-4 §3**, verbatim:
> "It is objective-blind: it measures the estate as it is, without reference to any particular objective, so targeting and convergence both read one measure that serves every objective equally. A measure computed per objective would have to be recomputed per objective — and two objectives could then disagree about the same source, which is not a disagreement the platform can afford to have unresolved."

**Canon-4 §10 (invariant 1)**, verbatim:
> "The census is exhaustive and objective-blind; one measure serves every objective."

**Canon-4 §4**, verbatim:
> "The census walks the estate exhaustively and objective-blind, producing one candidate source record per discovered source."

**Gloss** `[framing, not canon]`: measurement is a single, shared reading of the estate, not per-request or per-objective; two objectives never disagree about the same source because they are computed against the same measure.

### P8 — Every output states the strongest provenance its form permits, and no more

**Canon-4 §2 (bullet 3)**, verbatim:
> "Every output states the strongest provenance its form permits, and no more. Per-claim where the form preserves it, floor-over-load-bearing where it composes, ingredient manifest where training destroys it. No form is mis-promised."

**Canon-4 §36 (Five Forms table)**, verbatim (excerpted key rows):
> "Qualified data | Per-claim provenance — the strongest form, offered wherever the output preserves it."
> "Composed conclusion | Floor-over-load-bearing — Solva's assertion boundary applied, the class stated plainly."
> "Model | Training destroys per-claim provenance entirely — what remains is the training-data unit set, complete and recorded, which is what Model Output Acceptance requires in place of it."

**Canon-4 §36 (closing clause)**, verbatim:
> "No form is mis-promised. The one shape that cannot carry provenance at all is not offered as an output form."

**Gloss** `[framing, not canon]`: provenance shape is intrinsic to output form; a form that cannot carry provenance at all is not an offered form.

### P9 — Unmeasured is a first-class value; stale returns unknown

**Canon-4 §4.1**, verbatim:
> "Unmeasured is a first-class value. A dimension not measured is recorded as unmeasured, never as zero, absent, or clean. A blank that reads as clean makes the whole instrument dishonest."

**Canon-4 §8**, verbatim:
> "A stale or un-censused region returns unknown to a feasibility query, never a fabricated distribution. No objective freezes against an estate the system has not measured."

**DAP-Spec DAP-30**, verbatim:
> "Browse degrades rather than refuses: where the census is stale or partially unavailable, DAP returns what it has, marked as stale with its as-of time, and never silently presents an incomplete estate as complete."

**Gloss** `[framing, not canon]`: silence is never treated as clean; the system is measurably honest about what it has not seen.

### P10 — Self-proving: drills are the audit, standing cadence, no human assembly

**Canon-8 §W14**, verbatim:
> "Self-proving, or not in force. Every response rail demonstrates itself firing on a standing drill cadence — full loop, both engines, latencies measured, results as receipts. A rail not demonstrated firing is not in force, whatever the inventory claims."

**Canon-8 §19 (Drill pass row)**, verbatim:
> "Drill pass — both latencies in bound, correct verdict, correct action, release verified | 100%; a failed drill is a P1 | FACT | The rail is out of force until re-demonstrated"

**Canon-8 §14 (Interplay: CIF row)**, verbatim:
> "the drills operate under CIF's own self-certification bound"

**Gloss** `[framing, not canon]`: a rail is not in force because it exists; it is in force because it demonstrated itself firing on cadence, receipted.

### P11 — Non-bypassability of the boundary chokepoint

**Doc-0 Component 1 (SyniSense) §BR-1.1**, verbatim:
> "Every code path capable of reaching the external model client is enumerated and shown to route through the single chokepoint function; violation fails the build via negative-scan test."

**Canon-4 §33.3**, verbatim:
> "Perception calls route through the boundary governor. Speech and vision providers are consumed through SyniSense's perception router, so material crossing a model boundary is receipted whatever its modality happens to be."

**Canon-9 §6 (Chokepoint → model row)**, verbatim:
> "Custody chain per Document 3 §13.1 with the input seat's verdict preceding invocation; a hold here renders through the refusal taxonomy; receipt is the trust receipt plus the verdict."

**Canon-3 §13.1** (Phase B, first-hand — The Chokepoint sequence), verbatim (excerpted, four steps of the seven-step sequence):
> "Provider selection. Resolved from configuration ... De-identify. The inbound payload transits the de-identifier, which strips identifiers to placeholder tokens and records the mapping in a per-request custody envelope. Between de-identification and invocation sits the Watch's input seat, specified in Document 8: every payload bound for a model is scored for hostility and provenance before the call is made ... Invoke with metering. The call is made and per-call metering is emitted to the telemetry stream. Re-identify. Output transits the re-identifier against the same custody envelope. An unmatched token raises rather than passing through — a placeholder that cannot be resolved is an error, never a value."

**Canon-3 §13**, verbatim:
> "One function is the only place a model is invoked. Everything else that wants a model calls that function. The invariant is not that developers should route through it; the invariant is that a build fails if any other module imports the model client."

**Gloss** `[framing, not canon]`: exactly one path exists from an organisation's perimeter to any external model, verified by negative-scan build test. Canon 3 §13 and §13.1 confirmed first-hand.

### P12 — Objective freeze on commissioned jobs

**Doc-0 Component 3 (Northena) §BR-3.1**, verbatim:
> "The objective-freeze mechanism is a single, shared implementation invoked identically by every subsystem that hands off a job, not a per-caller reimplementation of the same guarantee."

**DAP-Spec DAP-18**, verbatim:
> "Every extraction is a commissioned job with a frozen objective. Objective freeze applies at commission: after commission, no path — including the portal's own assistance chat — may widen the job's scope. A wider scope is a new job."

**Audio-Plane §10.2**, verbatim (partial):
> "The test set precedes the training. An Outcome without an existing, stratified test set is rejected at definition time. The gate decision is recorded on the Outcome at definition — not decided ad hoc at ship time."

**Gloss** `[framing, not canon]`: a job's objective and its acceptance conditions are frozen at commission; a wider scope is a new job. Applied to training (Audio-Plane) as strictly as to extraction (Northena, DAP).

### Standing-order-derived promises (operational law, distinct from canon-doc-derived)

Per owner directive (this session): the two clauses below are **standing-order-derived operational law**, not canon-doc-derived promises. They are cited so that their provenance is transparent — they bind session conduct absolutely, but they are not clauses of Doc-0/Canon-4/Canon-8/Canon-9 etc.

### P-SO-1 — Alive is not done

**`STANDING_ORDERS §3.1`**, verbatim (owner directive "BUILD GO" 2026-09-13):
> "**ALIVE IS NOT DONE.** The existence of a heartbeat, a running PID, a directory on disk, or a filename in that directory is NOT proof of completion. Completion requires an OUTPUT ARTIFACT — a seal file whose contents, when parsed, prove the specific real work-kind that just finished. A seal read that does not parse `Kind:` and refuse non-real kinds silently promotes stubs, synthetic fixtures, and unfinished runs to success. This is banned."

**Gloss** `[framing, not canon]`: this is the platform's operational answer to silent-success as a completion attack surface. It layers with — but is distinct from — Canon-4 §4.1's "Unmeasured is a first-class value": Canon-4 §4.1 is about missing dimensions of measurement in the estate; SO §3.1 is about missing evidence of work completion in the runtime. Both refuse silence as clean.

### P-SO-2 — No run without a progress signal

**`STANDING_ORDERS §3.2`**, verbatim (owner directive "W1 CP breakdown approval" 2026-09-13):
> "**NO RUN WITHOUT A PROGRESS SIGNAL** — every commissioned run must emit a progress signal within its SLA or the supervisor raises a starvation alarm and HALTS the run."

**Gloss** `[framing, not canon]`: the runtime supervisor is DATA-only — a HALT verdict binds callers to stop dispatching but never kills a process. Zero-influence discipline preserved (per SO §3.2 clause 3, verbatim: "A HALT verdict is DATA — the runtime supervisor NEVER kills any process").

---

## §3. Product Feature Set

`[framing, not canon]` on the term "Product Feature Set" — canon does not use this phrase. The closest canon frame is `Doc-0 Part 2` titled **"Product Component Registry & Build Requirements"** which enumerates 16 named components. This section reads those components (plus Canon-9's charter classes and DAP-Spec's operations) as the product's feature set, cited verbatim.

### §3.1 The six governing engines

From `Doc-0 Part 2 Components 1–6` — the six engines constituting the governing authority:

| # | Name (canon) | Instantiates (Doc-0 tags) | Canon-4 role |
|---|---|---|---|
| 1 | SyniSense ("Shield") | Subsystem · Reference Monitor · Governed Triad (custody class) · Audit Record | Boundary governor (§33.3 "Perception calls route through the boundary governor. Speech and vision providers are consumed through SyniSense's perception router") |
| 2 | Solva | Subsystem · Determinism Boundary | Depth: reasoning and assertion floor (§19 "Solva judges whether reasoning is sound, whether preservation is sufficient, and whether an output asserts within its defensibility") |
| 3 | Northena | Subsystem · Governed Triad (operation integrity) | Direction: admission, gating, convergence, ledger writes (Canon-9 §5 task-identity register: "Admission · gating · convergence · ledger writes \| Governance · Northena") |
| 4 | Mtafiti ("the Registry") | Subsystem · Governed Triad (asset inventory, partial) | Discovery and measurement (Canon-4 §3 "Mtafiti censuses the estate exhaustively and writes the Registry: what exists, at what sensitivity, and how defensibly each source can be relied upon") |
| 5 | Targeta | Subsystem · Determinism Boundary · Mandatory Baseline | Targeting: reads the measured Registry and decides where to mine and in what order (Canon-4 §11) |
| 6 | Mkondo — Task & Job Orchestration | Subsystem · Governed Triad (operation hand-off) · Checkpoint | Orchestration; Canon-9 is the Mkondo Charter, which is the record matrix and handoff contract set |

**Source-linked verbatim excerpts** for each component's build requirements are in `Doc-0 Part 2 §§1–6` (lines 198–263 of the Doc-0 text file). This charter does not duplicate them — Doc-0 is canon; this charter reads it.

### §3.2 The second authority

From `Doc-0 Part 2 Component 7 (The Watch)` and `Canon-8` whole:

| Sub-component | Canon role |
|---|---|
| Macho (the eyes) | Detection, scoring, verdict assertion — no powers. `Canon-8 §5` "Macho observes, scores, and asserts facts. It holds no powers: it cannot block, throttle, mark, reroute, or notify. Its sole output is the verdict." |
| Mkono (the hand) | Deterministic mapping from verdict to action — no judgement. `Canon-8 §7` "Mkono executes signed policy tables against verdicts. It contains no model, no content parsing, no reasoning surface." |
| The verdict | The single interface between Macho and Mkono. `Canon-8 §6` (contract-grade verdict row: `verdict identity · detector · pinned version`, `actor · trace reference`, `signal class`, `certainty class`, `score · window · evidence references`). |
| Sarabi (the mirage) | Misdirection arm — synthetic continuation for suspected-not-certain actors. `Canon-8 §11`. |
| The signature substrate | Behavioural signature per actor. `Canon-8 §9`. Constitutionally non-exportable (`W13`). |
| The witness | External attestation; watchdog holding no Watch credentials. `Canon-8 §16`. |

### §3.3 The orchestration substrate (Canon-9 Mkondo)

Per `Canon-9 §3` (the record matrix), the platform's record classes and their single writers:

| Record class | Writer (canon) | Readers (canon) |
|---|---|---|
| Run ledger rows | Northena | Both authorities; compliance surfaces |
| Trust receipts | SyniSense | Both authorities; the receipt's own consumer |
| Census and registry records | Mtafiti | Both authorities; every surface by proof link |
| Mining plans | Targeta | Governing authority; auditors |
| Reasoning traces · intent audits | Solva | Both authorities |
| Declarations | Admission (Northena), from the actor | Both authorities |
| Rules · registries · ceremonies | The rules service | Both authorities; both consoles |
| Verdicts | Macho | Mkono; both consoles; auditors |
| Action records | Mkono | Both authorities; both consoles |
| Attestations · drill receipts | Watch workers · the witness | Everyone with assurance standing |
| Marks | Mkono | Every gate, on every pass |
| Behavioural profiles | The signature substrate | No surface, ever |
| Memory-plane rows | The owning application, via its plane | The estate holder; compliance |

**Note.** Canon-9 §3 explicitly does NOT list an "audio" or any per-modality record class. This is intentional: `Audio-Plane §1.2` "Modality extension, not parallel machinery" ⇒ audio records fold into existing classes (census/registry, reasoning traces, etc.), never a sibling class. See §4 below.

Per `Canon-9 §5` (the task-identity register): 8 task classes each map to exactly one authority's identity and scope (e.g., "Admission · gating · convergence · ledger writes | Governance · Northena", "Sensing · scoring · reconciliation · verdict minting | Watch · Macho"). Task classes with unmapped identity do not run.

Per `Canon-9 §6` (handoff contracts): 7 registered crossings (admission→extraction; chokepoint→model; verdict→response; containment→decision; mirage release→reconciliation; disagreement→resolution; Watch findings→CIF), each with what crosses, in what shape, under whose identity, with what receipt.

### §3.4 Cross-cutting platform infrastructure

From `Doc-0 Part 2 Components 8–16`:

| # | Component | Instantiates |
|---|---|---|
| 8 | The Ledger | Audit Record (primary instantiation) · Trusted Computing Base |
| 9 | CIF — Conditioned Ideation Faculty | Determinism Boundary (primary instantiation) · Trusted Computing Base (explicit exclusion) |
| 10 | The Critic Seam (Document 19A) | Checkpoint · Determinism Boundary |
| 11 | MOAC (Model Output Acceptance Criteria) | Reference Monitor (partial) · Mandatory Baseline |
| 12 | Manage Rules (customer rule books) | Authority & Change Control (customer-facing instantiation) |
| 13 | Whitepaper Wizard | Checkpoint · Control / Invariant · Audit Record |
| 14 | Connect Wizard | Checkpoint (admission) |
| 15 | Agent-Deploy Wizard | Checkpoint |
| 16 | Deck Rendering Engine | Control / Invariant · Determinism Boundary |

Verbatim scope statements for each are in `Doc-0 Part 2 §§8–16`. This charter reads Doc-0; it does not duplicate it.

### §3.5 Delivery / acquisition surfaces

From `DAP-Spec §4` — the six crossing profiles that constitute the External-Party Data Access Portal:

| Operation | Governing gate | Approval | Grounded at |
|---|---|---|---|
| Browse estate | Mtafiti census; progressive disclosure | None — standing terms | DAP-Spec DAP-6 |
| Connect workspace (API key) | SyniSense chokepoint; the pull seam | None for uncontrolled; per-request if controlled | DAP-Spec DAP-7 |
| Processed intelligence | SyniSense chokepoint; Solva's assertion floor | None for uncontrolled; per-request if controlled | DAP-Spec DAP-8 |
| Fine-tune model | Targeta; artefact egress | Always — artefact egress | DAP-Spec DAP-9, DAP-10 |
| Develop skills | Doc 18 callable skill files; artefact egress | Always — artefact egress | DAP-Spec DAP-10 |
| Download raw data | Outer gate (Promise #25) — not the ordinary crossing | Always for controlled; owner-configurable otherwise | DAP-Spec DAP-11 |

DAP-Spec `§7 Composition Map` states verbatim: "DAP owns no invariant of its own. Every guarantee it makes is a guarantee of a component it composes, exercised through this surface." DAP is a composition, not an engine.

`DAP-Spec §11 Standing` states verbatim: "DAP is the first instance of a generic Data & Intelligence Acquisition Platform. Nothing in §1–§9 is specific to RMS except the named estate; a second estate owner adopting this platform inherits every requirement here and configures §5's owner-side settings for its own estate." Case-agnostic core; RMS is one instance.

### §3.6 Named consoles

From `Canon-8 §13` (Watch Console — four panels: State / Record / Under watch / Decisions) and `Canon-9 §5` (Console sessions | The console's authority | Trust Center under governance; Watch Console under Watch). Full-surface specification is `Canon-5 Part VII‑A §34-A..34-C` (Phase B, first-hand): "The Watch Console is the security authority's one surface ... It is a peer to the Trust Center, never a tab inside it: the two authorities' consoles share the record and share nothing else, and access to each runs under its own authority's identity per the matrix in Document 9." Four panels: State, Record, Under watch, Decisions.

### §3.7 Doc-0 Part 3 (Gap Register) — first-hand, full-text (Phase B)

Doc-0 Part 3 was read first-hand lines 360–528 in Phase B. Doc-0 §3.7 opens with the STATUS AS OF header (line 364 verbatim):

> "STATUS AS OF 9 SEPTEMBER 2026"
> "'Spec-drafted' and 'spec-closed' both mean documentation exists; neither means code exists. This table is a pointer, not a re-statement — each closing document carries its own full reasoning, which this update does not duplicate."

**The full STATUS AS OF table (Doc-0 Table 3, lines 508–520 verbatim, all thirteen gaps)**:

| ID | Closing document | State |
|---|---|---|
| G-1 | tcb_enumeration_v1 | Spec-drafted — 27 components evaluated, R-3 resolved as a consequence. Not built. |
| G-2 | security_architecture_v1 (partial) | Partial — the reference-monitor half is drafted; general subsystem classification remains open. |
| G-3 | dap_backend_spec_v1 DAP-1/DAP-2 (external-party case only) | Partial — general triad formalisation and Mtafiti's full asset-inventory extension remain open. |
| G-4 | Not yet drafted | Open. |
| G-5 | dap_backend_spec_v1 §4 (DAP case only) | Partial — general case (MOAC, chokepoint) remains open. |
| G-6 | security_architecture_v1 | Spec-drafted — seven reference monitors assessed, SEC-1 through SEC-7 close what was missing. Not built. |
| G-7 | security_function_policies_v1 | Spec-drafted — seven SFPs named; R-2 resolved as no-violation. Not built. |
| G-8 | Security_Promise_Set_Amendments.docx, Amendment 3 | Spec-closed. Not built. |
| G-9 | Rules Service RBM-7/RBM-8 | Spec-closed. Not built. |
| G-10 | determinism_inventory_v1 | Spec-drafted — 16 components classified, Article 14 mapped. Not built. |
| G-11 | failure_posture_v1 | Spec-drafted — platform default plus two departures specified. Not built. |
| G-12 | trust_domains_v1 | Spec-drafted — R-5 resolved by cross-reference to the appliance spec. Not built. |
| G-13 | handoff_registry_v1 | Spec-drafted. Not built. |

**The four Rulings (Doc-0 Table 4, lines 523–527 verbatim)**:

| ID | Ruling |
|---|---|
| R-1 | TCB membership test (G-1): ratify the test proposed in Attribute 1 — deterministic and protection-critical — or set a different one before the list is published. |
| R-2 | RESOLVED, 9 Sep 2026 (security_function_policies_v1): re-checking Doc 4 A5.5 against Doc 3 A5.2 found no violation — "lower the standard" is Solva's query-recalibration option for the party asking a question, not a bar a measured subject can weaken. A5.2 itself is explicitly unalterable by the party it measures. Neither original option was needed; the SFP-naming work G-7 also asked for proceeds separately, in the same document. |
| R-3 | The Watch's TCB membership (G-1): the service in full, or its deterministic response half only, with Grey Mirror's detection half excluded as learned under Attribute 10. |
| R-5 | Deployment model (G-12): shared infrastructure with tenant separation, dedicated per tenant, or both, with the boundary stated per deployment. |

---

## §4. Audio Job Placement

### §4.1 Framing (canon-first)

`Audio-Plane §1.2`, verbatim (this is the single most binding clause for §4):

> "**Modality extension, not parallel machinery.** The audio plane introduces no sibling services. Mtafiti gains an audio modality; Northena gains audio data classes; the wizard gains an objective variant; Targeta gains a training object. Anything in this document that reads as a parallel to an existing service is rule proliferation and must be collapsed into the existing service before build."

`Canon-4 §28`, verbatim:

> "What follows in this Part, and the transform layer in Part VI, describes what happens once fresh extraction has been triggered — the pipeline is the same whichever data dimensionality the material belongs to: audio, documents, structured records, images, or any other modality the estate holds. The layers, the unit contract, and qualification below apply identically across all of them."

`Audio-Plane §1.3`, verbatim:

> "**One record.** Mtafiti and Northena collaborate to produce a single record, written once. Working state — loss curves, intermediate metrics, partial coverage counts — is scratch, not truth; it becomes record only when finalized and stamped. No local ledger exists."

`Audio-Plane §1.1`, verbatim:

> "**An audio file is a data estate, and the framing is recursive.** The archive is an estate; a programme is an estate; a single file is an estate. Segments are rows; the extractable layers — content, language, condition, prosody, occurrence, code-switch, music, group-level character — are columns; no schema exists until one is declared. Census, admission, registry, and record apply at every scale."

### §4.2 Where an audio job slots into the platform primitives

`[framing, not canon]` — this section maps the case-agnostic platform primitives (built through W0/W1/W1b/W1c per fork context) to the canon extension points named by Audio-Plane §1.2. The map is the session agent's; the anchors are canon.

| Platform primitive (this session's language) | Canon anchor (verbatim clause / spec ID) | What audio adds |
|---|---|---|
| `job_kind` registry / `kind_registry` **[framing, not canon]** | `Canon-4 §32` "Long work survives interruption. Jobs checkpoint, and re-dispatch is idempotent — the same job submitted twice produces neither two sets of units nor two charges." | Register an audio-modality job kind whose contract is: input = audio segment; output = normalised unit (Canon-4 §30) + character stream (Audio-Plane §5.2). Follows Audio-Plane §1.2's "Targeta gains a training object" and the Objective-Wizard variant of §8. |
| `SourceConnector` / `Synology` interface **[framing "SourceConnector", operational "Synology"; NEITHER is canon]** | `Canon-4 §33` "Perception calls route through the boundary governor. Speech and vision providers are consumed through SyniSense's perception router, so material crossing a model boundary is receipted whatever its modality happens to be." | The audio codec service (Audio-Plane §3, "audio_codec ... registered like any other perception model") plugs into SyniSense's perception router. No sibling router — Audio-Plane §1.2 forbids it. |
| Generic `AttributeStreamBundle_v0` **[framing, not canon]** | `Canon-4 §30` "The normalised unit is a frozen contract with flat field names, and it admits structured sources exactly as it admits perceived ones — a structured record becomes a unit without perception, carrying a text modality and a free locator. **No second intake contract exists anywhere in the platform.** Every unit carries five rings: content, provenance, relational edges, context, and defensibility." | Audio-Plane §3.1 states: "Tokenization exposes two separable streams per segment: the content stream (what was said — input to ASR/NER) and the character stream (how it was said — input to the Character Register). The character stream is retained and routed, never discarded as noise." Both streams land in the same five-ring unit; the character stream is a column, not a sibling unit. |
| `RetentionPolicy` **[framing, not canon]** | `Canon-8 §20` "the profile drift ceiling and **the profile retention posture** (W13) ... Until ruled, the conservative default holds in each case: the tightest ceiling, the shortest retention" | Audio-Plane §6.2 fixes register custody: "Stored as description, not exemplar. Centroids, distributions, frequencies. Never stored audio; never per-utterance speaker embeddings. Embeddings used during clustering are destroyed after cluster assignment." This is a retention rule expressed at schema level (§6.3 "The register write path exposes no field through which an instance-level representation can be stored") — "Unrepresentable, not policed" (§1.5). |
| Generic Capability / `capability registry` **[framing, not canon]** | `Doc-0 Attribute 4 §BA-4.3` "Every control carries a status from the fixed set defined in rule_criteria_spec_v1 — CANON, RULED, DEFAULT, PROPOSED, or OPEN — and that status is current, not aspirational." Also `OpVal-v1.1 §Preamble` fixes an evidence-class taxonomy — FACT / NORM / DEFAULT. | Audio-modality perception models register as `Rung 3 · Small owned models` under `Canon-4 §40`: "Estate-fine-tuned perception and domain models — speech, diarisation, classifiers — registry-pinned." OpVal-v1.1 §1 fixes concrete model choices (whisper-large-v3, LoRA adapters, spaCy `en_core_web_trf`, Silero VAD, pyannote diarisation, faster-whisper runtime, multilingual-e5 embeddings) each with an evidence class. Every model is registered, not implicit. |

### §4.3 Operational status (NOT canon)

Per the owner's directive (this session): the W2 mount blockers are included here **only** to state their operational-status shape, tagged as such — they do not dominate §4. Any reader whose question is about the canon placement of audio should read §4.1 and §4.2; §4.3 is a status footnote.

**Status footnote (operational, not canon)**:

- **W2 (real audio job mount)** is currently hard-stopped by three owner rulings pending (fork-context banked in `STATE/DECISIONS.md`, per fork brief):
  1. **Storage Path A/B/C ruling** — where converged audio units land on-host (path variants deferred to owner).
  2. **NAS network path** — Synology FileStation reach via sysadmin bastion / VPN, mapped in `SourceConnector` interface but not wired.
  3. **3-station confirm** — three-station smoke of the real audio mount before it counts as in-force (per P10 self-proving discipline: `Canon-8 §W14` "Every response rail demonstrates itself firing on a standing drill cadence").

None of these blockers is a canon question. They are owner rulings and infrastructure paths, banked in State/Decisions. Canon has already told us where audio slots (§4.1); operations tells us when W2 is safe to open.

### §4.4 What Audio-Plane conforms to, and what OpVal-v1.1 pins as FACT

Two clauses that surface where the audio modality carries an **architectural absolute** the platform enforces universally through it:

`OpVal-v1.1 §12.F1c`, verbatim:
> "**F1c** · **Perception has NO efficiency valve** — ASR NEVER serves degraded without its per-language gate. Registry-pinned at deployment. **Class: FACT** (architectural absolute)."

`OpVal-v1.1 §12.F1a`, verbatim:
> "**F1a** · ASR per-language WER degradation ≤ **1.0pp absolute** on held-out sets per language for any serving-efficiency change (quantization or successor). **Class: NORM.**"

`Audio-Plane §3.3`, verbatim (acceptance criteria):
> "Round-trip fidelity is measured and recorded per codec version before that version serves any commission. A downstream artifact lacking codec_version in provenance is rejected at the registry boundary. An unsupported-condition input produces a refusal with a stated reason and no output artifact."

**Gloss** `[framing, not canon]`: audio is not exempted from the platform's floor discipline (Canon-4 §13 "A source below the floor is excluded, full stop"); every audio artifact carries provenance-bound codec_version; per-language WER regressions are gated architecturally, not merely alarmed.

---

## §5. Divergences, Conflicts, and Findings

Per owner directive: do not silently resolve conflicts. Flag them. Quote both. Mark for owner ruling if genuine.

### §5.1 Genuine conflicts — none found across the full canon read

Phase A (2026-09-13, first pass) and Phase B (2026-09-13, this session) together opened Canon 1–9, Doc-0 Parts 1–3, DAP-Spec, Audio-Plane, OpVal-v1.1, and STANDING_ORDERS first-hand. No clause of one directly contradicts a clause of another. Phase B specifically closed the previous absence-based caveat: every clause the charter cites has now been read in this session.

**Load-bearing surfaces surfaced by Phase B that Phase C must anchor to** (not conflicts — refinements):

- `Canon-3 §22` (Four Classes of governed values: Rails, Rules, Engine settings, Registries) — LOAD-BEARING for W-REGISTRY-FULL-BUILD. Every governed value belongs to exactly one class, and change velocity + verification method differ by class.
- `Canon-3 §22.1` (Entitlement rules as ABAC) — LOAD-BEARING for W-DAP-STACK / DAP-14. The requester side matches against Mtafiti's sensitivity classification (canon: "The content side is already built: the sensitivity classification Mtafiti assigns during census, specified in Document 4, is exactly the resource attribute this match runs against. No new classification exists; entitlement reads the one already there.").
- `Canon-7 §35–§40` (Function & Promise Registry) — LOAD-BEARING for every wave. Every named function in the platform registers here with function_id/governor/mandate/promise/service_trace/surface/enforcement/cost/dependencies/ladder_rung/owner. Three standing queries (Redundancy / Orphans / Gaps) run on every registry change. Canon 7 §37 (Derivation Rules): "No gate without a promise. No promise without a service trace. No journey step without enforcement. New functions register before they land."
- `Canon-7 §18–§27` (Memory Layer / Memory Plane) — LOAD-BEARING for W-DAP-STACK, especially DAP-13 (API key issuance) and DAP-24 (cumulative extraction history). Every integration key is issued with exactly one memory plane; write-back class inherits internal-only rights at birth (Canon 7 §21.2).
- `Canon-7 §41–§46` (Critic Seam, three tiers) — LOAD-BEARING for Solva-v2 lift. Tier 1 deterministic verification; Tier 2 critic pass; Tier 3 human calibration. Design principles: "Detect, never decide. Canon is the oracle. Zero loop drag. Halving, not zeroing — stated honestly. The critic is calibrated like a model, because it is one. The layer pays rent."
- `Canon-7 §47` (D8 defect class) — first-hand confirmed. Dual-identity execution is a defect class, name it on sight.
- `Canon-7 §48-49` (Canon before Ruling; Every phase closes on disk) — matches STANDING_ORDERS discipline verbatim.

### §5.2 Terminology-collision watch — same word, different subjects

Called out so future readers do not confuse them:

**"Peer"** — used in two distinct senses across the canon:
- `Canon-8 §W12` and `Canon-9 §1` use "peer" for the **inter-authority** relation between governance and the Watch: peer standing, neither commands the other.
- `Canon-4 §34.1` uses "peer" (as a negative) for the **intra-governance** relation between the two services (Build the asset / Serve the objective): verbatim, "Neither service is a peer standing beside the other. The second depends entirely on what the first has already built; the first has no dependency on the second at all."

These are not in conflict — they concern different pairs. Flagged so a Chunk-3-style row does not conflate them.

**"Objective"** — used in three distinct senses:
- `Canon-4 §11` uses "objective" for the customer/user request that Targeta serves ("reach objective-satisfying, floor-meeting intelligence in fewer mined units").
- `Doc-0 Part 1 §Definition` uses no equivalent term at the platform level; the platform's north star is stated as a category ("governance operating system"), not an objective.
- This charter's §1 title uses "Objective" at the meta-level (system objective). That meta-usage is **`[framing, not canon]`**; canon reserves "objective" for task-level.

**"Register"** — used in two distinct senses in Audio-Plane vs. Canon-4:
- `Canon-4 §8` ("The Registry") = Mtafiti's asset inventory: "One record per source, carrying existence, sensitivity, the defensibility measure, and a freshness stamp."
- `Audio-Plane §5.1` ("The Character Register") = group-level acoustic knowledge store: "A registry-modality store of learned, group-level audio characteristics, built from the character stream."

Both are "registry-modality" stores under Mtafiti's discipline (Audio-Plane §5.1 says so verbatim: "Same doctrine as the fact registry ... Mtafiti's qualification-and-index doctrine applied to acoustic observations — an extension, not a sibling"). Not a conflict; a naming echo that Audio-Plane §1.2 forecloses ("no sibling services").

### §5.3 Layering, not conflict — SO §3.1 vs Canon-4 §4.1

Both refuse silence-as-clean, but they measure different silences:

- `Canon-4 §4.1` (canon): "Unmeasured is a first-class value. A dimension not measured is recorded as unmeasured, never as zero, absent, or clean." — subject: estate measurement dimensions.
- `STANDING_ORDERS §3.1` (operational law): "**ALIVE IS NOT DONE.** The existence of a heartbeat, a running PID, a directory on disk, or a filename in that directory is NOT proof of completion." — subject: runtime work completion.

They layer. SO §3.1 is the runtime-level answer to a completion attack surface; Canon-4 §4.1 is the measurement-level answer to a data-honesty attack surface. Same doctrine, two domains.

### §5.4 Doc-0 Component 6 (Mkondo) BR-6.1 vs Canon-9 §6 — G-13 adjudication (Phase B, resolved)

- `Doc-0 Component 6 §BR-6.1 STATUS`: "Partial — Promise #32 is itself marked Partial in canon: 'one concrete instance … no generalised registered handoff contract per crossing.' See G-13."
- `Canon-9 §6` provides a table of **seven** registered handoff contracts (admission→extraction; chokepoint→model; verdict→response; containment→decision; mirage release→reconciliation; disagreement→resolution; Watch findings→CIF).
- `Doc-0 Part 3 STATUS AS OF` (Phase B first-hand, line 520 verbatim): `G-13 | handoff_registry_v1 | Spec-drafted. Not built.`

**Adjudication question (per owner Amendment 1, this session)**: do Canon-9 §6's seven registered handoff contracts carry HR-x IDs?

**Answer**: **NO**. First-hand grep across `canon/text/Akki_Canon_9_Mkondo_Charter.txt` for `HR-[0-9]|HR‑[0-9]|handoff_registry` returned zero matches (Phase B this session). Canon-9 §6 labels its rows in prose ("Admission → extraction", "Chokepoint → model", "Verdict → response", "Containment → decision", "Mirage release → reconciliation", "Disagreement → resolution", "Watch findings → CIF"), not by handoff_registry_v1's HR-1..HR-7 identifiers.

**Owner ruling applied (Amendment 1 NO branch, verbatim)**: "the seven are built artifacts (real registered subsystem-pair contracts in code), i.e. G-13 is implementation-advanced beyond the spec record. Record that in the Build Status column (currently blank for exactly this) — do NOT conflate with spec-drafted status."

**Recorded state for G-13**:

| ID | Spec-record (Doc-0 §STATUS AS OF, verbatim) | Build Status (per owner ruling, Phase B) |
|---|---|---|
| G-13 | `handoff_registry_v1` — Spec-drafted. Not built. | Implementation-advanced beyond the spec record. Seven registered subsystem-pair contracts articulated in Canon-9 §6 (prose form, no HR-x IDs). Distinct from and not conflated with spec-drafted status. |

**Earlier §5.4 (Phase A) "near-collision" framing is superseded.** No collision exists between Doc-0 and Canon-9 §6: the two are different documentation surfaces (Doc-0 = gap register pointing to `handoff_registry_v1` as the spec closure; Canon-9 = the doctrinal articulation of the seven crossings that surface as built artifacts). The Build Status column carries what the Spec-record does not, and does not overwrite it.

### §5.5 Declared absences — closed (Phase B)

Phase A (2026-09-13, first pass) listed sixteen canon-referenced clauses that were quoted through session-opened sources rather than opened first-hand: Canon 1 §4.1, §4.3, §12; Canon 3 §5-§8, §6.1, §9, §13.1, §22, §22.1, §24, §27; Canon 5 Part VII‑A; Canon 7 Part II, Part IV, §47; and Doc-0 Part 3.

**All sixteen are now first-hand (Phase B, 2026-09-13, this session).** Every clause quoted in this charter has been read from the source file in this session, and the "cited as quoted in" caveats formerly attached to those clauses have been removed (see charter body §2 P1, P4, P5, P6, P11 for the amended first-hand citations). §0.3 (canon-not-opened list) is retired; §3.7 carries the full Doc-0 Part 3 STATUS AS OF and rulings tables first-hand; §5.4 carries the G-13 adjudication.

**No further absence carries into Phase C.** Per owner Amendment 2 (this session, verbatim): "Once B is complete the §5.5 declared absences are closed. Do NOT carry them into the C plan as 'explicit plan risks.'"

---

## §6. What This Charter Comes Down To

`[framing, not canon]`, paraphrased in Canon-9's own closing style:

Akki turns estate material into governed intelligence at a stated standard, with every unit traceable to its source, while making the constraints on that action structurally enforced — not policed after the fact. Two authorities stand on one substrate as peers. The governing authority mines, measures, targets, reasons, and delivers; the Watch answers "was this intended, and is this actor what it claims to be?" — subordinate to nothing, autonomous but reversible, bounded, witnessed. Learning may detect at three named points; it never decides. Reasoning strength cannot raise a claim above what its evidence supports. Silence is never treated as clean. Fail-closed is the default; the chokepoint is non-bypassable; the record matrix says who writes and who reads, and additions to it are ceremony. Audio is a modality of the same platform, not a sibling of it — Mtafiti gains a modality, Northena gains data classes, the wizard gains an objective variant, Targeta gains a training object. Rails not demonstrated firing on cadence are not in force.

Every clause above traces back to canon opened in this session. What does not — this synthesis, and the platform-primitive names in §4.2 — is tagged `[framing, not canon]` so that the boundary between canon and articulation is never quiet.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
