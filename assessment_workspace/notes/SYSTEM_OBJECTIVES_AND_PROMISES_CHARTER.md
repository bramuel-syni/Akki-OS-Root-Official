READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# SYSTEM_OBJECTIVES_AND_PROMISES_CHARTER.md

**Purpose.** A canon-grounded articulation of what this system is trying to do (Objective) and what it commits to (Promises), traced to verbatim canon clauses. Produced as a read-only bank artifact — no code, no ratchet touch, W2 hard-stopped.

**Date.** 2026-09-13
**Author.** Session agent, resumed from fork; all quotations sourced by opening the named file in this session (STANDING_ORDERS §1 boot protocol).
**Provenance.** Every factual claim below is either (a) a verbatim quote from a canon file opened in this session, cited with its file path and section, or (b) explicitly tagged `[framing, not canon]` — session framing that is not present in any canon file. Nothing else is smuggled in.
**Standing.** This is a notes/ bank artifact. It does not amend canon; it reads it. Where a promise is stated below, it points to canon; canon binds, this document does not.

---

## §0. Provenance and Precedence

### §0.1 Session-opened source set (this is what "grounded" means below)

The following files were opened, and read, in this session under the discipline of STANDING_ORDERS §1. Every quotation below is drawn from one of them:

| Short name in body | On-disk path | Origin |
|---|---|---|
| `Canon-4` | `canon/text/Akki_Canon_4_Operating_Engines.txt` | canon docx converted to txt |
| `Canon-8` | `canon/text/Akki_Canon_8_The_Watch.txt` | canon docx converted to txt |
| `Canon-9` | `canon/text/Akki_Canon_9_Mkondo_Charter.txt` | canon docx converted to txt |
| `Doc-0` | `canon/drops/20260909/extracted/text/Akki_Governance_Architecture_v1.txt` | drop 2026-09-09, spec-ID `akki_governance_architecture_v1` (per `notes/spec_id_index.md` row `akki_governance_architecture_v1`) |
| `DAP-Spec` | `canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt` | drop 2026-09-09, spec-ID `dap_backend_spec_v1` (per `notes/spec_id_index.md`) |
| `Audio-Plane` | `canon/text/Akki_OS_Audio_Intelligence_Plane_Specification_v1_0.txt` | canon docx converted to txt |
| `OpVal-v1.1` | `repos/Extraction-Akki/docs/requirements/operating_values_v1_1.md` | governed artifact in Extraction-Akki, dated 2026-07-15 |
| `STANDING_ORDERS` | `STATE/STANDING_ORDERS.md` | permanent operational law |

### §0.2 Session-opened but partially read

- **Doc-0 Part 3 (Gap Register)** was opened in this session but the second half of the text file was truncated by the viewing tool. Lines 1–359 (Parts 1 and 2, whole) were read verbatim; lines 360-forward (Part 3) were sampled by grep for gap identifiers G-1, G-8, G-10, G-11, G-12, G-13 only. This charter does not cite Doc-0 Part 3 text that was not surfaced in this session; where a gap is referenced, only the grep-visible identifier and one-line summary is used.

### §0.3 Canon documents not opened in this session (findings, not fillers)

The following canon documents are referenced by cross-quote from other canon sources but were NOT opened in this session:

- **Canon 1** (Custody Platform). Referenced by `Canon-9 §2` ("Document 1 §4.3 holds: there is exactly one record") and by `Canon-8 §W10` ("Custody gates fail closed on their own, per Document 1 §4.1"). Not opened here.
- **Canon 3** (Governance Engines). Referenced by `Canon-8 §W2` and `Canon-9 §3` (via table notes: "Contract-grade per Document 3 §9"), and by `Canon-8 §W8` ("with the Watch itself among the observers per Document 3 §24"). Not opened here.
- **Canon 5, 6, 7** (Interface Architecture, User Journeys, Integration/Quality). Referenced by `Canon-8 §13` ("Document 5 Part VII‑A") and `Canon-9 §3` ("Per Document 7 Part IV"). Not opened here.

**Consequence.** Any promise below that rests on a Canon 1/3/5/6/7 clause is cited **as it is quoted in a source opened this session** (e.g., "quoted in Canon-9 §2"), never as a first-hand read. Absence of a first-hand read is stated explicitly; it is not papered over.

### §0.4 Precedence order used in this document

Per owner directive (this session): where canon layers rather than conflicts, the working order is:

1. **STANDING_ORDERS.md** — permanent operational law. Overrides nothing in canon on canon's own subject matter, but binds session conduct absolutely (session boot, engagement, build, runtime, GPU, custody).
2. **Doc-0 (`akki_governance_architecture_v1`)** — the authoritative governance architecture, twelve attributes as a dependency stack. Where a governance term is defined, Doc-0's definition governs.
3. **Domain specs** — DAP-Spec (`dap_backend_spec_v1`) for the external-party acquisition surface; Audio-Plane for audio modality. Each governs its own domain and explicitly disclaims parallel machinery (Audio-Plane §1.2).
4. **OpVal-v1.1** and **Canon-9 (Mkondo Charter)** — ground the objective and promise language. OpVal-v1.1 fixes evidence classes (FACT/NORM/DEFAULT) for every value; Canon-9 fixes the record matrix and identity register cited by both authorities as the same document.

**Where two canon sources genuinely disagree**, this document does NOT silently pick a winner. It quotes both, marks the divergence, and flags it for owner ruling. See §5 (Divergences and Findings).

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

**Canon-9 §2**, verbatim:
> "Document 1 §4.3 holds: there is exactly one record, and nothing maintains a second. What the law forbids is a second, competing account of the same events. What it requires is exactly this matrix: one authoritative account per record class, with a single writing authority and named readers."

**Canon-9 §3**, verbatim (the matrix header row):
> "Every record class in the platform, its single writer, and its readers. A second writer to any class is a defect on sight; a reader not listed does not read; additions to this matrix are ceremony, and the matrix version in force is stamped on every audit answer."

**Doc-0 §8 (Ledger), BR-8.1**, verbatim:
> "The Ledger accepts and retains records of refused operations on the same terms as accepted ones — a refusal is as much a record as a success."

**Gloss** `[framing, not canon]`: one authoritative account per record class, one writer, named readers, refusals recorded on the same terms as successes.

**First-hand read caveat**: the "Document 1 §4.3" text itself was NOT opened in this session; it is quoted through `Canon-9 §2`. Absence noted.

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

**Gloss** `[framing, not canon]`: governance and the Watch are structural equals, held apart by unrepresentable-dual-identity, resolved on disagreement by containment plus a person, with disagreement itself becoming a record. The "Document 7 §47" defect class D8 was NOT read first-hand in this session — cited as quoted in Canon-8 §W11 and Canon-9 §5.

### P5 — Every autonomous act is reversible, bounded, and witnessed

**Canon-8 §W3**, verbatim:
> "Every autonomous act is reversible, bounded, and witnessed. A time-to-live on every action; a blast budget on every window; act-and-attest atomically, peer-countersigned. Destroy does not exist in the Watch."

**Canon-8 §19 (Blast budget row)**, verbatim:
> "Blast budget — autonomous action per rolling window | ≤ 5% of active actors per hour | DEFAULT · dual-control | Excess queues for human release"

**Canon-8 §W3 (continued)**, verbatim:
> "An action that expires unless renewed converts the false positive from a harm into a delay; a budget converts the autoimmune attack — tricking the immune system into suspending the business — from an outage into a bounded cost; atomic attestation makes weaponizing the Watch impossible to do quietly, which for a detection system is the property that matters. And a power the tool structurally lacks cannot be turned: the Watch can stop anything and erase nothing — deletion remains solely the authority act of Document 3 §27."

**Gloss** `[framing, not canon]`: TTL + blast budget + atomic peer-countersigned attestation. The Watch cannot delete; deletion is a governance-authority act (Document 3 §27, NOT opened this session — cited as quoted in Canon-8).

### P6 — Fail-closed as the reference-monitor default; per-component posture declared

**Doc-0 Attribute 11 §BA-11.2**, verbatim:
> "Every reference monitor and every component inside the Trusted Computing Base fails closed, without exception: an evaluation that cannot complete is a refusal, because a reference monitor that fails open on internal error is not tamper-resistant against the specific attack of inducing that error."

**Doc-0 Attribute 11 §BA-11.1**, verbatim:
> "Every component's failure types are enumerated — the specific ways it can fail to complete an evaluation — rather than covered by a single unqualified 'handles failures gracefully' statement that names no failure and specifies no state."

**DAP-Spec DAP-28**, verbatim:
> "Every gate in DAP fails closed. An approval service that cannot be reached, a metering write that cannot complete, a terms resolution that returns nothing, a ceiling check that errors — each refuses the operation. No path returns estate data, an artefact, or a query result when a governing check could not complete."

**Canon-8 §W10**, verbatim:
> "The service whose compromise would mean going unobserved must be incapable of unobserved existence — and equally incapable of failing anything open. Custody gates fail closed on their own, per Document 1 §4.1, with or without the Watch above them."

**Gloss** `[framing, not canon]`: fail-closed is the default posture for every reference monitor and every TCB component; every component enumerates its failure types explicitly; custody gates are structurally independent of the Watch. "Document 1 §4.1" not read first-hand — cited as quoted in Canon-8.

**Finding (absence-is-a-finding)**: Doc-0 Part 3 Gap Register lists `G-11 · Failure Posture · Documentary | Failure types not enumerated per component; posture not declared per checkpoint.` (surfaced by grep this session, line 502 of `Doc-0`). The doctrine is canon; the per-component enumeration is a documented gap in Doc-0 Part 3.

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

**Gloss** `[framing, not canon]`: exactly one path exists from an organisation's perimeter to any external model, verified by negative-scan build test. "Document 3 §13.1" not opened first-hand this session — quoted in Canon-9 §6.

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

From `Canon-8 §13` (Watch Console — four panels: State / Record / Under watch / Decisions) and `Canon-9 §5` (Console sessions | The console's authority | Trust Center under governance; Watch Console under Watch). Full-surface specifications are in `Document 5 Part VII‑A` per Canon-8 §13 — NOT opened first-hand this session.

### §3.7 Findings/gaps surfaced by Doc-0 Part 3 (grep-only in this session)

Per §0.2, Doc-0 Part 3 was not fully read. Grep against lines 360–520 surfaced the following gap identifiers with their one-line summaries (canonical, per Doc-0's own gap-register format):

- `G-1 | 1 · TCB | Documentary | No enumerated, published list of Trusted Computing Base members.`
- `G-8 | 8 · Audit Record | Mechanical | Trust receipt specification omits principal identity and timestamp; no reliable-time control.`
- `G-10 | 10 · Determinism Boundary | Documentary | No per-component deterministic/learned inventory; ruling loop not mapped to Article 14's five capabilities.`
- `G-11 | 11 · Failure Posture | Documentary | Failure types not enumerated per component; posture not declared per checkpoint.`
- `G-12 | 12 · Trust Domain | Documentary · Ruling | Domains not described as a set; deployment model unstated.`
- `G-13 | 6 · Mkondo, Checkpoint | Mechanical | Job hand-off contract is instantiated once (ThinkLab → Task Manager); not generalised across crossings.`

**Note.** These are canon's own gap records, not this charter's. Canon-9 §6 (the seven registered handoff contracts) appears — on the face of it — to address G-13. This charter does not adjudicate whether G-13 is now closed; that is a Doc-0 Part 3 re-read for a later session, and the grep-only read here is honestly labelled.

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

### §5.1 Genuine conflicts — none found in the eight sources read this session

After reading Canon-4, Canon-8, Canon-9, Doc-0 Parts 1–2 (Part 3 grep-only), DAP-Spec, Audio-Plane, OpVal-v1.1, and STANDING_ORDERS in this session, no clause of one directly contradicts a clause of another. This is stated as a finding, not as certainty: Canon 1, Canon 3, Canon 5, Canon 6, Canon 7 were NOT opened this session (§0.3), and a Canon-1/3/5/6/7 clause could still disagree with what is quoted above. Absence-is-a-finding.

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

### §5.4 Doc-0 Component 6 (Mkondo) BR-6.1 vs Canon-9 §6

- `Doc-0 Component 6 §BR-6.1 STATUS`: "Partial — Promise #32 is itself marked Partial in canon: 'one concrete instance … no generalised registered handoff contract per crossing.' See G-13."
- `Canon-9 §6` provides a table of **seven** registered handoff contracts (admission→extraction; chokepoint→model; verdict→response; containment→decision; mirage release→reconciliation; disagreement→resolution; Watch findings→CIF), each with "what crosses, in what shape, under whose identity, with what receipt."

**Assessment** `[framing, not canon]`: On the face of it, Canon-9 §6 addresses Doc-0's G-13 by generalising the handoff contract set. Doc-0 was banked in the 2026-09-09 drop; Canon-9's Mkondo Charter appears to be later canon material that carries what Doc-0 flagged missing. This is not adjudicated here — a Doc-0 Part 3 re-read (with full-text view rather than grep-only) is what is needed to close G-13 as a resolved item. Flagged, not resolved.

### §5.5 Absences (findings, not fillers)

The following canon-referenced clauses were NOT opened first-hand this session; quotations from them in the charter above are cited **as they are quoted in a session-opened source**. These are absences to close in the next reading pass:

- `Canon 1 §4.1` (custody gates fail-closed) — quoted in `Canon-8 §W10`.
- `Canon 1 §4.3` (one record law) — quoted in `Canon-9 §2`.
- `Canon 1 §12` (service sentences) — referenced in `Canon-8 §1` ("Every Watch function traces to this sentence, exactly as every governance function traces to a service sentence of Document 1 §12").
- `Canon 3 §5–§8` (admission→extraction custody chain) — quoted in `Canon-9 §6`.
- `Canon 3 §6.1` (frozen declarations at admission) — quoted in `Canon-8 §W9` and `Canon-9 §3` table note.
- `Canon 3 §9` (contract-grade ledger rows) — quoted in `Canon-9 §3` table note.
- `Canon 3 §13.1` (SyniSense chokepoint) — quoted in `Canon-9 §6`.
- `Canon 3 §22` (Registries-class policy tables) — quoted in `Canon-8 §7`.
- `Canon 3 §22.1` (entitlement rules on sensitivity classification) — quoted in `Canon-4 §4.1`.
- `Canon 3 §24` (change ceremony with Watch as observer) — quoted in `Canon-8 §W8`.
- `Canon 3 §27` (deletion authority) — quoted in `Canon-8 §W3`.
- `Canon 5 Part VII‑A` (Watch Console surface spec) — quoted in `Canon-8 §13`.
- `Canon 7 Part II` (governed boundary at delivery) — quoted in `Canon-4 §34.3`.
- `Canon 7 Part IV` (memory-plane rows) — quoted in `Canon-9 §3` table note.
- `Canon 7 §47` (defect class D8 — dual-hatted task) — quoted in `Canon-8 §W11` and `Canon-9 §5`.
- `Doc-0 Part 3` (Gap Register) — grep-only this session; full text pending.

These are marked so a follow-on reading pass knows exactly what to open.

---

## §6. What This Charter Comes Down To

`[framing, not canon]`, paraphrased in Canon-9's own closing style:

Akki turns estate material into governed intelligence at a stated standard, with every unit traceable to its source, while making the constraints on that action structurally enforced — not policed after the fact. Two authorities stand on one substrate as peers. The governing authority mines, measures, targets, reasons, and delivers; the Watch answers "was this intended, and is this actor what it claims to be?" — subordinate to nothing, autonomous but reversible, bounded, witnessed. Learning may detect at three named points; it never decides. Reasoning strength cannot raise a claim above what its evidence supports. Silence is never treated as clean. Fail-closed is the default; the chokepoint is non-bypassable; the record matrix says who writes and who reads, and additions to it are ceremony. Audio is a modality of the same platform, not a sibling of it — Mtafiti gains a modality, Northena gains data classes, the wizard gains an objective variant, Targeta gains a training object. Rails not demonstrated firing on cadence are not in force.

Every clause above traces back to canon opened in this session. What does not — this synthesis, and the platform-primitive names in §4.2 — is tagged `[framing, not canon]` so that the boundary between canon and articulation is never quiet.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
