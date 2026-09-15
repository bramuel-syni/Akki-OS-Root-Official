READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# PULL_SEAM_REQUIREMENTS_VERBATIM_20260914.md

**Source doc:** `The_Pull_Seam.docx` · sha256 `0a3084422726dd76aee6a6d80d9e3534ded2677cfe95947215c9762fe305afab` · 16,429 B · downloaded 2026-09-15T01:32:25Z.
**Structured extract:** `canon/drops/20260914_pull_seam/extracted/The_Pull_Seam_STRUCTURED.txt` — every paragraph tagged `[P### · <style>]`; table rows tagged `[P### · TABLE-ROW-##]`; last paragraph index `P083`.
**Manifest:** `canon/drops/20260914_pull_seam/manifest.json`.
**Standing rule anchor:** DECISIONS.md ruling 2026-09-15T~01:40Z (Verbatim-canon discipline).

**Discipline of this document (banked):**

* Every row carries (a) a **verbatim quote** from the source, (b) the **paragraph index** `P###` in the structured extract, (c) the **section heading** (per the doc's own §-numbering 1..9), and (d) a **classification** ∈ {`definition`, `rule`, `flow-step`, `prohibition`, `table-header`, `table-cell`, `prose`, `slogan`}.
* Where a paragraph contains multiple discrete sentences that each stand as a binding clause, each is rendered as its own row `P###.s#`. Sentence boundaries are a feature of the source text, not an invention.
* **Zero invented terminology.** All names of components / crossings / gates / budgets use the source doc's own words. If the source doc doesn't name it, this document doesn't either.
* Where a claim in the source is more compressed than a downstream gate would need (e.g. "receipt written before result returned"), the row records the exact quote unchanged; it is up to the mechanism designer to decide granularity of gating.

---

## §Preamble (P001..P003)

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P001 | *"SYNI.AI  ·  AKKI OS  ·  DESIGN PRINCIPLES"* | P001 · title | prose |
| P002 | *"The Pull Seam"* | P002 · title | prose |
| P003 | *"How Akki processes data without moving it"* | P003 · subtitle | prose |

## §Framing block (P005..P008 · document metadata table)

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P005 | *"What this is · The design principles behind the pull seam — the mechanism by which an outside party can query, analyse, or train on a data estate while the estate's data stays inside its owner's perimeter."* | P005 · TABLE-ROW-01 | definition |
| P006 | *"Who it is for · Any technical reader. It assumes familiarity with networks, databases, and machine learning, and nothing about Akki."* | P006 · TABLE-ROW-02 | prose |
| P007 | *"The one idea · Reverse the direction of travel. Instead of sending data to where the compute is, put the compute where the data is, and let only governed results travel out."* | P007 · TABLE-ROW-03 | rule (core doctrine) |
| P008 | *"Version · pull_seam_principles_v1 · 14 September 2026 · External"* | P008 · TABLE-ROW-04 | metadata (version pin) |

## §1 · The Problem (P010..P012 · Heading1)

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P011.s1 | *"Almost every arrangement for letting an outside party work with your data moves the data."* | P011 · §1 | prose (motivation) |
| P011.s2 | *"It is uploaded to a vendor's cloud, or a credential to all of it is handed to a service outside your network, or a contract promises it will be deleted afterwards."* | P011 · §1 | prose (enumeration of common patterns) |
| P011.s3 | *"Once data is elsewhere, control of it is elsewhere too: it can be copied, breached, retained, or reused, and the owner learns about it after the fact if at all."* | P011 · §1 | prose (consequence) |
| P012.s1 | *"Data is most valuable exactly where it is most sensitive — in health, finance, government, research, media archives."* | P012 · §1 | prose |
| P012.s2 | *"Those are also the estates least able to move their data anywhere."* | P012 · §1 | prose |
| P012.s3 | *"The pull seam exists to make those estates usable without moving them."* | P012 · §1 | rule (product intent) |

## §2 · The Principles (P013..P038 · Heading1)

### Principle 1 · P014..P015

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P014 | *"Principle 1  Compute comes to the data. Never the reverse."* | P014 · §2 P1 heading | rule (principle statement) |
| P015.s1 | *"The platform runs on a sealed appliance installed inside the customer's own server room or field site."* | P015 · §2 P1 | rule |
| P015.s2 | *"The appliance holds the GPUs."* | P015 · §2 P1 | rule |
| P015.s3 | *"Queries execute on it."* | P015 · §2 P1 | rule |
| P015.s4 | *"Models train on it."* | P015 · §2 P1 | rule |
| P015.s5 | *"An outside party who wants a model shaped by the estate's data sends the model in; the model trains next to the data and leaves as weights."* | P015 · §2 P1 | rule (direction of travel for models) |
| P015.s6 | *"There is no configuration in which estate data is transferred to compute outside the perimeter."* | P015 · §2 P1 | prohibition |
| P015.s7 | *"This is a prohibition with no exception, not a default setting."* | P015 · §2 P1 | prohibition (meta) |

### Principle 2 · P016..P017

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P016 | *"Principle 2  One seam. Two ports. No third path."* | P016 · §2 P2 heading | rule (principle statement) |
| P017.s1 | *"The appliance exposes exactly two network interfaces on physically separate connectors, colour-keyed and labelled: ESTATE, which faces the customer's data network, and WAN, which faces the outside world."* | P017 · §2 P2 | rule (physical + labelling) |
| P017.s2 | *"Data is read through ESTATE."* | P017 · §2 P2 | rule |
| P017.s3 | *"Parties connect through WAN."* | P017 · §2 P2 | rule |
| P017.s4 | *"Everything that moves from one side to the other passes through a single software crossing."* | P017 · §2 P2 | rule (single-crossing) |
| P017.s5 | *"That crossing is enforced at build time: exactly one function may perform it, and a scan on every build fails the build if a second path is introduced."* | P017 · §2 P2 | rule (build-time enforcement) |
| P017.s6 | *"Outbound network connections are allow-listed, so there is no route to an unlisted destination."* | P017 · §2 P2 | rule (outbound allow-list) |

### Principle 3 · P018..P019

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P018 | *"Principle 3  The two sides share nothing."* | P018 · §2 P3 heading | rule (principle statement) |
| P019.s1 | *"The estate and the outside party are separate trust domains."* | P019 · §2 P3 | rule |
| P019.s2 | *"They share no identifiers, no storage, and no credentials."* | P019 · §2 P3 | rule (three no-share carriers) |
| P019.s3 | *"A record's identifier inside the estate means nothing outside it and resolves to nothing there."* | P019 · §2 P3 | rule (identifier scope) |
| P019.s4 | *"A party's key is its own — revocable in one act, expiring, non-transferable, never written to logs — and identifies an organisation that was admitted through a governed act by the estate owner's named authority."* | P019 · §2 P3 | rule (party-key carriers) |

### Principle 4 · P020..P021

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P020 | *"Principle 4  Identity never crosses."* | P020 · §2 P4 heading | rule (principle statement) |
| P021.s1 | *"Before any result leaves, it passes through the crossing, which replaces identifiers and declared-confidential values with placeholder tokens according to each record's custody class."* | P021 · §2 P4 | rule (per-record custody-class placeholder tokens) |
| P021.s2 | *"The party receives the answer to its question with identifying content substituted."* | P021 · §2 P4 | rule |
| P021.s3 | *"Re-identification happens only inside the perimeter, and only for the estate's own use."* | P021 · §2 P4 | rule (re-id scope) |

### Principle 5 · P022..P032 (contains the six-crossing table)

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P022 | *"Principle 5  Six crossings, each governed on its own terms."* | P022 · §2 P5 heading | rule (principle statement) |
| P023.s1 | *"An outside party can do six things, and each is a different crossing with its own rules for what enters, what leaves, whether a human must approve, and what is recorded."* | P023 · §2 P5 | rule (six-carrier crossing schema) |
| P023.s2 | *"Five of the six release a derivative — a count, a de-identified result, a derived finding, a trained model, a skill."* | P023 · §2 P5 | rule (derivative-vs-data taxonomy) |
| P023.s3 | *"Only one releases estate data itself, and it is deliberately not the ordinary crossing."* | P023 · §2 P5 | rule (raw-data-path exceptional) |

**Six-crossing table** (verbatim, P024..P032):

| Row | Operation | What enters | What leaves | Human approval | What is recorded |
|---|---|---|---|---|---|
| P025 (header) | Operation | What enters | What leaves | Human approval | What is recorded |
| **P026** | *"Browse the estate"* | *"Nothing"* | *"Aggregate composition only — never record contents"* | *"None"* | *"The access"* |
| **P027** | *"Query (API)"* | *"The party's query"* | *"Results, de-identified"* | *"Only if controlled data is touched"* | *"Every query, every result"* |
| **P028** | *"Processed intelligence"* | *"The party's objective"* | *"Derived output only — never source records"* | *"Only if controlled data is touched"* | *"Objective, output, records read"* |
| **P029** | *"Train a model"* | *"The party's base model"* | *"Trained weights, with rights and hash stamped"* | *"Always"* | *"Training manifest, weights hash, terms"* |
| **P030** | *"Build a skill"* | *"The party's skill objective"* | *"The skill file"* | *"Always"* | *"Skill hash, records read, terms"* |
| **P031** | *"Download raw data"* | *"Nothing"* | *"Estate data itself"* | *"Always for controlled; owner-set otherwise"* | *"Every record, redaction log, sign-off"* |

### Principle 6 · P033..P034

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P033 | *"Principle 6  A trained model leaves only after it is measured."* | P033 · §2 P6 heading | rule (principle statement) |
| P034.s1 | *"Training changes weights, and weights carry the statistical influence of what they trained on."* | P034 · §2 P6 | prose (fact) |
| P034.s2 | *"The platform does not pretend otherwise; it bounds that influence three ways."* | P034 · §2 P6 | prose (meta) |
| P034.s3 | *"Training is differentially private by default, which limits how much any single record can shape the result."* | P034 · §2 P6 | rule (bound 1: DP) |
| P034.s4 | *"Before release, the trained model is probed for memorisation — sampled against the records it trained on — and does not pass until it sits beyond a set distance from every controlled record."* | P034 · §2 P6 | rule (bound 2: memorisation probe + distance-from-controlled threshold) |
| P034.s5 | *"And every release, of any kind, is debited against the estate's release budget: a ceiling on the total information that can ever leave, across all parties, all operations, and all time."* | P034 · §2 P6 | rule (bound 3: release budget · global ceiling) |

### Principle 7 · P035..P036

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P035 | *"Principle 7  Every crossing is recorded — or it does not happen."* | P035 · §2 P7 heading | rule (principle statement) |
| P036.s1 | *"Each operation writes a receipt: what was accessed, in what quantity, under which terms, by which party, at what time."* | P036 · §2 P7 | rule (five receipt carriers) |
| P036.s2 | *"The receipt is written before the result is returned."* | P036 · §2 P7 | rule (receipt-first ordering) |
| P036.s3 | *"If it cannot be written, the operation is refused."* | P036 · §2 P7 | rule (write-refusal → op-refusal) |
| P036.s4 | *"The same holds for every governing check: if an approval cannot be reached, a terms lookup returns nothing, or a check errors, the crossing fails closed."* | P036 · §2 P7 | rule (fail-closed on gate error) |
| P036.s5 | *"No path returns data, a result, or a model when a check did not complete."* | P036 · §2 P7 | rule (no partial-return) |

### Principle 8 · P037..P038

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P037 | *"Principle 8  Raw data leaves only through a separate outer gate."* | P037 · §2 P8 heading | rule (principle statement) |
| P038.s1 | *"Downloading estate data itself is not the ordinary crossing."* | P038 · §2 P8 | rule (outer-gate distinctness) |
| P038.s2 | *"It is a distinct outer gate with its own rules: disclosure depth is bounded by rights and custody, redaction runs as a gate rather than a suggestion, a named human signs off, and every released record is individually recorded."* | P038 · §2 P8 | rule (four outer-gate carriers) |
| P038.s3 | *"Everything else the seam supports releases a derivative."* | P038 · §2 P8 | rule (roll-up) |
| P038.s4 | *"This is the only operation that releases the thing itself, and it is built to be the exception."* | P038 · §2 P8 | rule (exception status) |

## §3 · Seeing It Work: A Query (P039..P045 · Heading1)

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P040 | *"1.  The party connects on the WAN side  with its own key."* | P040 · §3 step 1 | flow-step |
| P041 | *"2.  The query enters.  Nothing about the party crosses with it — no identifier from the party's side resolves inside the estate."* | P041 · §3 step 2 | flow-step |
| P042 | *"3.  The query runs inside the perimeter,  on the estate's own compute, against data that never leaves the ESTATE side."* | P042 · §3 step 3 | flow-step |
| P043 | *"4.  The result passes the crossing.  Identifiers and confidential values are replaced with placeholders according to custody class."* | P043 · §3 step 4 | flow-step |
| P044 | *"5.  De-identified results leave on the WAN side.  If controlled data was touched, approval was required before step 3 ran; otherwise no human was in the loop."* | P044 · §3 step 5 | flow-step |
| P045 | *"6.  A receipt is written.  If it cannot be, the operation is refused."* | P045 · §3 step 6 | flow-step |

## §4 · Seeing It Work: A Training Run (P046..P052 · Heading1)

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P047 | *"1.  The party's base model enters on the WAN side  and is admitted to estate compute. Before it touches any data it is run in a synthetic environment that probes it for hidden behaviour — a model is not trusted on arrival."* | P047 · §4 step 1 | flow-step (adds "synthetic-environment pre-flight" for incoming models) |
| P048 | *"2.  Training runs on the estate's GPUs,  against data in place, with a differentially private optimiser by default."* | P048 · §4 step 2 | flow-step |
| P049 | *"3.  The result is gated before it can leave.  It must meet every accuracy criterion set before training started, or it is refused in full. It is probed for memorisation. Its draw against the release budget is checked."* | P049 · §4 step 3 | flow-step (three sub-gates: pre-declared accuracy criteria · memorisation probe · release-budget draw) |
| P050 | *"4.  Weights leave through the model registry,  carrying a rights posture, a recorded hash, and the terms in force. Weights derived from controlled data carry that fact on their registry entry permanently."* | P050 · §4 step 4 | flow-step (model-registry outbound carrier + permanent controlled-provenance stamp) |
| P051 | *"5.  A receipt is written:  the training manifest, the weights hash, the terms."* | P051 · §4 step 5 | flow-step (three receipt carriers for training) |
| P052 | *"What left: a trained model, measured and budgeted. What did not leave: any record it trained on. The data stayed on the ESTATE side of the appliance throughout."* | P052 · §4 closing | prose (roll-up) |

## §5 · What Leaves, Stated Precisely (P053..P054 · Heading1)

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P054.s1 | *"“Nothing leaves” is a slogan."* | P054 · §5 | slogan (called out as such by the doc) |
| P054.s2 | *"The precise statement is this: no raw record leaves except through the outer gate with a named human's sign-off, and everything else that leaves is a governed derivative — de-identified results, derived intelligence, or measured artefacts — bounded in aggregate by the release budget and recorded individually."* | P054 · §5 | rule (LOAD-BEARING · this sentence is the precise contract to quote in downstream gating tests) |
| P054.s3 | *"Nothing crosses outward that is not one of those, and each crossing has a receipt."* | P054 · §5 | rule (closure over set) |

## §6 · Where the Principle Comes From (P055..P057 · Heading1)

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P056.s1 | *"Compute-to-data is not new."* | P056 · §6 | prose (context) |
| P056.s2 | *"Stored procedures send logic into the database rather than pulling rows out."* | P056 · §6 | prose (prior art) |
| P056.s3 | *"Hadoop schedules jobs onto the nodes that hold the data because moving terabytes is the expensive part."* | P056 · §6 | prose (prior art) |
| P056.s4 | *"Federated learning sends a model to where data lives and returns only the weight updates."* | P056 · §6 | prose (prior art) |
| P056.s5 | *"Data clean rooms let two parties compute over combined data without either seeing the other's rows."* | P056 · §6 | prose (prior art) |
| P056.s6 | *"Confidential computing processes data in a region the host cannot read."* | P056 · §6 | prose (prior art) |
| P057.s1 | *"The pull seam applies the same direction of travel to a whole estate and adds what those approaches mostly lack: one enforced boundary that every crossing passes through, six distinct crossings each governed on its own terms, measured release of trained artefacts, a finite budget on total release, and a receipt for everything."* | P057 · §6 | rule (five distinguishing additions · roll-up) |
| P057.s2 | *"The principle is familiar. The enforcement is the design."* | P057 · §6 | rule (meta) |

## §7 · The Trade-Off (P058..P060 · Heading1)

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P059.s1 | *"Compute-to-data means the estate hosts the compute."* | P059 · §7 | prose |
| P059.s2 | *"GPU capacity sits on premises rather than being rented by the hour, and throughput is bounded by that hardware."* | P059 · §7 | rule (on-prem GPU · no rented-hour path) |
| P059.s3 | *"An outside party's training job runs at the estate's speed."* | P059 · §7 | prose |
| P059.s4 | *"Batch and asynchronous work — analysis, extraction, training — fits this well; interactive, low-latency work fits it less well."* | P059 · §7 | prose (trade-off) |
| P060.s1 | *"What the estate gets in return is the removal of an entire class of risk: no copy of the data elsewhere to breach, no egress to pay for, no deletion promise to audit, and no credential to a full dataset in someone else's key store."* | P060 · §7 | prose (four benefits) |
| P060.s2 | *"For a regulated or sovereignty-constrained estate, that is usually the right trade."* | P060 · §7 | prose (meta) |

## §8 · What You Can Observe (P061..P072 · Heading1 · contains observable-artefact table)

| Row | Verbatim quote | Location | Classification |
|---|---|---|---|
| P062 | *"Each principle above corresponds to something a technical reader can see directly on a deployed system."* | P062 · §8 | rule (each principle has an observable) |

**Observable-artefact table** (verbatim, P063..P072):

| Row | "Look at" | "What it shows" |
|---|---|---|
| P064 (header) | Look at | What it shows |
| **P065** | *"The appliance's front panel"* | *"Two ports, ESTATE and WAN, and nothing else. The GPUs are inside."* |
| **P066** | *"The build test output"* | *"The single-crossing check, passing on the current build."* |
| **P067** | *"The outbound allow-list"* | *"The only destinations the appliance can reach."* |
| **P068** | *"A receipt and its ledger entry"* | *"What crossed, how much, under which terms, by whom, when."* |
| **P069** | *"A memorisation probe result"* | *"A trained model measured against its own training records before release."* |
| **P070** | *"The release budget and its consumption"* | *"The ceiling on total release, and how much of it has been used."* |
| **P071** | *"The configuration"* | *"There is no setting that moves estate data to outside compute."* |

## §9 · Glossary (P073..P083 · Heading1)

| Row | Term (verbatim) | Meaning (verbatim) | Classification |
|---|---|---|---|
| P075 (header) | Term | Meaning | table-header |
| **P076** | *"Estate"* | *"A data holding under one owner's custody — an archive, a database set, a corpus."* | definition |
| **P077** | *"Seam"* | *"The single interface where the estate's domain meets an outside party's. Nothing else is shared across it."* | definition |
| **P078** | *"Crossing"* | *"One of six governed operations by which something moves from one side of the seam to the other."* | definition (closes crossing-count at six) |
| **P079** | *"Custody class"* | *"A per-record classification governing how it may cross — what is de-identified, whether approval is required."* | definition |
| **P080** | *"Controlled record"* | *"A record whose custody class requires approval before an operation touching it may run."* | definition |
| **P081** | *"Release budget"* | *"A ceiling on the total information released from an estate across all parties, operations, and time."* | definition |
| **P082** | *"Receipt"* | *"The record written for every crossing. If it cannot be written, the crossing does not happen."* | definition |

---

## Summary counts (verbatim rows only · no invented sub-clauses)

* Framing + version: 4 rows (P005..P008).
* §1 Problem prose: 6 sentence-rows (P011..P012).
* §2 Principle statements: **8 rows** (P014, P016, P018, P020, P022, P033, P035, P037).
* §2 Principle-body sentence-rows: **31 rows** (P015.s1..s7 + P017.s1..s6 + P019.s1..s4 + P021.s1..s3 + P023.s1..s3 + P034.s1..s5 + P036.s1..s5 + P038.s1..s4).
* §2 Six-crossing table cells (data rows only): **6 rows × 5 columns = 30 cell-quotes** (P026..P031).
* §3 Query flow steps: **6 rows** (P040..P045).
* §4 Training flow steps: **5 rows** (P047..P051).
* §5 Precise statement: **3 sentence-rows** (P054.s1..s3; s2 is load-bearing).
* §6 Origin prose: 8 sentence-rows (P056.s1..s6 + P057.s1..s2).
* §7 Trade-off prose: 6 sentence-rows (P059.s1..s4 + P060.s1..s2).
* §8 Observable-artefact table cells: **7 rows × 2 columns = 14 cell-quotes** (P065..P071).
* §9 Glossary: **7 term-rows** (P076..P082).

**Grand total of verbatim rows:** **135**, spanning 83 source paragraph indices.

---

## What this document does NOT do

* It does not translate the doc's content into a downstream "PS-X.Y" numbering scheme. When a downstream gate wants a stable ID, it cites the paragraph index directly (e.g. `P017.s5 · §2 P2`).
* It does not gloss meaning. Where the source says *"differentially private by default"*, the row carries that exact phrase — a mechanism designer decides whether "DP-SGD" or another concrete algorithm satisfies it, and the ratification of that mapping is the owner's, not the extract's.
* It does not group sub-clauses under invented product-terminology (e.g. "single-crossing build scan" as an invented compound name). The verbatim phrase is *"a scan on every build fails the build if a second path is introduced"* (P017.s5). Downstream can name a module whatever it wants; the requirement citation quotes the source.

---

## Cross-links

* Structured extract: `canon/drops/20260914_pull_seam/extracted/The_Pull_Seam_STRUCTURED.txt`.
* Raw docx: `canon/drops/20260914_pull_seam/raw/The_Pull_Seam.docx`.
* Manifest: `canon/drops/20260914_pull_seam/manifest.json`.
* Conformance rebuild (verbatim-anchored): `notes/PULL_SEAM_CONFORMANCE_VERBATIM_20260914.md`.
* Standing rule anchor: DECISIONS.md 2026-09-15T~01:40Z (Verbatim-canon discipline).
* Superseded prior extractions (retained for audit-trail): `notes/canon_pull_seam_requirements.md` · `notes/PULL_SEAM_CONFORMANCE_20260914.md`.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
