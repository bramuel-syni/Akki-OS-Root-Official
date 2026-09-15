READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

> **SUPERSEDED — 2026-09-15T~01:40Z.** This document was authored under an
> invented `PS-P1.1..PS-P8.5` sub-numbering scheme with prose gloss instead
> of verbatim canon text. It is superseded by
> `notes/PULL_SEAM_REQUIREMENTS_VERBATIM_20260914.md` per owner ruling
> 2026-09-15T~01:40Z (Verbatim-canon discipline). Downstream references
> MUST use the verbatim document. This file is retained for audit-trail
> continuity only.

# canon_pull_seam_requirements.md

**Source doc:** `canon/drops/20260914_pull_seam/extracted/The_Pull_Seam.txt`
**Provenance:** downloaded 2026-09-15T01:32:25Z from owner-provided customer-assets URL · sha256 `0a3084422726dd76aee6a6d80d9e3534ded2677cfe95947215c9762fe305afab` · manifest at `canon/drops/20260914_pull_seam/manifest.json`.
**Version string (verbatim):** *"pull_seam_principles_v1 · 14 September 2026 · External"*
**One-idea statement (verbatim, §The one idea):** *"Reverse the direction of travel. Instead of sending data to where the compute is, put the compute where the data is, and let only governed results travel out."*

---

## Requirement numbering convention

`PS-<n>.<m>` where n = section, m = sub-clause within that section. Each row cites the exact section anchor from the source doc so a downstream test's docstring can carry the verbatim quote (Owner Standing Condition 1 · 2026-08-26).

---

## §2 · The Principles

### Principle 1 · Compute comes to the data. Never the reverse.

* **PS-P1.1** *"The platform runs on a sealed appliance installed inside the customer's own server room or field site."* (§2 P1)
* **PS-P1.2** *"The appliance holds the GPUs."* (§2 P1) — on-premises compute; no rented GPU-hour path allowed.
* **PS-P1.3** *"Queries execute on it."* (§2 P1)
* **PS-P1.4** *"Models train on it."* (§2 P1)
* **PS-P1.5** *"An outside party who wants a model shaped by the estate's data sends the model in; the model trains next to the data and leaves as weights."* (§2 P1)
* **PS-P1.6** *"There is no configuration in which estate data is transferred to compute outside the perimeter. This is a prohibition with no exception, not a default setting."* (§2 P1) — build-time enforcement, not runtime toggle.

### Principle 2 · One seam. Two ports. No third path.

* **PS-P2.1** *"The appliance exposes exactly two network interfaces on physically separate connectors."* (§2 P2)
* **PS-P2.2** *"colour-keyed and labelled: ESTATE, which faces the customer's data network, and WAN, which faces the outside world."* (§2 P2)
* **PS-P2.3** *"Data is read through ESTATE."* (§2 P2)
* **PS-P2.4** *"Parties connect through WAN."* (§2 P2)
* **PS-P2.5** *"Everything that moves from one side to the other passes through a single software crossing."* (§2 P2)
* **PS-P2.6** *"That crossing is enforced at build time: exactly one function may perform it, and a scan on every build fails the build if a second path is introduced."* (§2 P2)
* **PS-P2.7** *"Outbound network connections are allow-listed, so there is no route to an unlisted destination."* (§2 P2)

### Principle 3 · The two sides share nothing.

* **PS-P3.1** *"The estate and the outside party are separate trust domains."* (§2 P3)
* **PS-P3.2** *"They share no identifiers, no storage, and no credentials."* (§2 P3)
* **PS-P3.3** *"A record's identifier inside the estate means nothing outside it and resolves to nothing there."* (§2 P3)
* **PS-P3.4** *"A party's key is its own — revocable in one act, expiring, non-transferable, never written to logs."* (§2 P3)
* **PS-P3.5** *"identifies an organisation that was admitted through a governed act by the estate owner's named authority."* (§2 P3)

### Principle 4 · Identity never crosses.

* **PS-P4.1** *"Before any result leaves, it passes through the crossing."* (§2 P4)
* **PS-P4.2** *"which replaces identifiers and declared-confidential values with placeholder tokens according to each record's custody class."* (§2 P4)
* **PS-P4.3** *"The party receives the answer to its question with identifying content substituted."* (§2 P4)
* **PS-P4.4** *"Re-identification happens only inside the perimeter, and only for the estate's own use."* (§2 P4)

### Principle 5 · Six crossings, each governed on its own terms.

*"An outside party can do six things, and each is a different crossing with its own rules for what enters, what leaves, whether a human must approve, and what is recorded."* (§2 P5)

The six-row table (§2 P5 table, rows verbatim in the requirement text):

| # | Operation | What enters | What leaves | Human approval | What is recorded |
|--:|---|---|---|---|---|
| **PS-P5.1** | Browse the estate | Nothing | Aggregate composition only — never record contents | None | The access |
| **PS-P5.2** | Query (API) | The party's query | Results, de-identified | Only if controlled data is touched | Every query, every result |
| **PS-P5.3** | Processed intelligence | The party's objective | Derived output only — never source records | Only if controlled data is touched | Objective, output, records read |
| **PS-P5.4** | Train a model | The party's base model | Trained weights, with rights and hash stamped | Always | Training manifest, weights hash, terms |
| **PS-P5.5** | Build a skill | The party's skill objective | The skill file | Always | Skill hash, records read, terms |
| **PS-P5.6** | Download raw data | Nothing | Estate data itself | Always for controlled; owner-set otherwise | Every record, redaction log, sign-off |

* **PS-P5.7** *"Five of the six release a derivative — a count, a de-identified result, a derived finding, a trained model, a skill. Only one releases estate data itself, and it is deliberately not the ordinary crossing."* (§2 P5)

### Principle 6 · A trained model leaves only after it is measured.

* **PS-P6.1** *"Training changes weights, and weights carry the statistical influence of what they trained on."* (§2 P6) — no denial that weights encode data statistics.
* **PS-P6.2** *"Training is differentially private by default, which limits how much any single record can shape the result."* (§2 P6)
* **PS-P6.3** *"Before release, the trained model is probed for memorisation — sampled against the records it trained on."* (§2 P6)
* **PS-P6.4** *"[and] does not pass until it sits beyond a set distance from every controlled record."* (§2 P6)
* **PS-P6.5** *"every release, of any kind, is debited against the estate's release budget."* (§2 P6)
* **PS-P6.6** *"a ceiling on the total information that can ever leave, across all parties, all operations, and all time."* (§2 P6) — the release budget is a single global ceiling.

### Principle 7 · Every crossing is recorded — or it does not happen.

* **PS-P7.1** *"Each operation writes a receipt: what was accessed, in what quantity, under which terms, by which party, at what time."* (§2 P7) — five carriers.
* **PS-P7.2** *"The receipt is written before the result is returned."* (§2 P7) — receipt-first ordering, load-bearing.
* **PS-P7.3** *"If it cannot be written, the operation is refused."* (§2 P7) — write-refusal → op-refusal.
* **PS-P7.4** *"if an approval cannot be reached, a terms lookup returns nothing, or a check errors, the crossing fails closed."* (§2 P7) — fail-closed on every gate.
* **PS-P7.5** *"No path returns data, a result, or a model when a check did not complete."* (§2 P7) — no partial return.

### Principle 8 · Raw data leaves only through a separate outer gate.

* **PS-P8.1** *"Downloading estate data itself is not the ordinary crossing. It is a distinct outer gate with its own rules."* (§2 P8) — outer gate is a separate mechanism, not a mode of the ordinary crossing.
* **PS-P8.2** *"disclosure depth is bounded by rights and custody."* (§2 P8)
* **PS-P8.3** *"redaction runs as a gate rather than a suggestion."* (§2 P8) — redaction refusal, not redaction advisory.
* **PS-P8.4** *"a named human signs off."* (§2 P8) — named authority, not group.
* **PS-P8.5** *"every released record is individually recorded."* (§2 P8) — per-record ledger, not batch.

---

## §3 · Query flow (numbered)

* **PS-Q1** *"The party connects on the WAN side with its own key."* (§3.1)
* **PS-Q2** *"The query enters. Nothing about the party crosses with it — no identifier from the party's side resolves inside the estate."* (§3.2)
* **PS-Q3** *"The query runs inside the perimeter, on the estate's own compute, against data that never leaves the ESTATE side."* (§3.3)
* **PS-Q4** *"The result passes the crossing. Identifiers and confidential values are replaced with placeholders according to custody class."* (§3.4)
* **PS-Q5** *"De-identified results leave on the WAN side. If controlled data was touched, approval was required before step 3 ran; otherwise no human was in the loop."* (§3.5)
* **PS-Q6** *"A receipt is written. If it cannot be, the operation is refused."* (§3.6)

## §4 · Training flow (numbered)

* **PS-T1** *"The party's base model enters on the WAN side and is admitted to estate compute. Before it touches any data it is run in a synthetic environment that probes it for hidden behaviour — a model is not trusted on arrival."* (§4.1) — synthetic-env pre-flight for incoming models.
* **PS-T2** *"Training runs on the estate's GPUs, against data in place, with a differentially private optimiser by default."* (§4.2)
* **PS-T3** *"The result is gated before it can leave. It must meet every accuracy criterion set before training started, or it is refused in full. It is probed for memorisation. Its draw against the release budget is checked."* (§4.3) — pre-declared acceptance criteria, refuse-in-full on miss.
* **PS-T4** *"Weights leave through the model registry, carrying a rights posture, a recorded hash, and the terms in force. Weights derived from controlled data carry that fact on their registry entry permanently."* (§4.4)
* **PS-T5** *"A receipt is written: the training manifest, the weights hash, the terms."* (§4.5)

---

## §5 · What leaves — precise statement (single-sentence anchor)

* **PS-S5.1** *"no raw record leaves except through the outer gate with a named human's sign-off, and everything else that leaves is a governed derivative — de-identified results, derived intelligence, or measured artefacts — bounded in aggregate by the release budget and recorded individually."* (§5) — this sentence is load-bearing and can be quoted verbatim in a gating test docstring.

Sub-clauses:
* **PS-S5.1a** No raw record leaves except through outer gate with named human sign-off.
* **PS-S5.1b** Everything else that leaves is a governed derivative in the closed set {de-identified results, derived intelligence, measured artefacts}.
* **PS-S5.1c** Governed derivatives are bounded in aggregate by the release budget.
* **PS-S5.1d** Governed derivatives are recorded individually.

---

## §8 · Observable-corresponding artefacts

Each row below is a claim the doc makes about what a technical reader can *directly observe* — each maps to a gate-able invariant.

* **PS-O1** *"The appliance's front panel — Two ports, ESTATE and WAN, and nothing else. The GPUs are inside."* (§8)
* **PS-O2** *"The build test output — The single-crossing check, passing on the current build."* (§8)
* **PS-O3** *"The outbound allow-list — The only destinations the appliance can reach."* (§8)
* **PS-O4** *"A receipt and its ledger entry — What crossed, how much, under which terms, by whom, when."* (§8)
* **PS-O5** *"A memorisation probe result — A trained model measured against its own training records before release."* (§8)
* **PS-O6** *"The release budget and its consumption — The ceiling on total release, and how much of it has been used."* (§8)
* **PS-O7** *"The configuration — There is no setting that moves estate data to outside compute."* (§8)

---

## §9 · Glossary (frozen terminology)

* **PS-G-Estate** — *"A data holding under one owner's custody — an archive, a database set, a corpus."* (§9)
* **PS-G-Seam** — *"The single interface where the estate's domain meets an outside party's. Nothing else is shared across it."* (§9)
* **PS-G-Crossing** — *"One of six governed operations by which something moves from one side of the seam to the other."* (§9) — the crossing taxonomy is closed at six.
* **PS-G-CustodyClass** — *"A per-record classification governing how it may cross — what is de-identified, whether approval is required."* (§9)
* **PS-G-ControlledRecord** — *"A record whose custody class requires approval before an operation touching it may run."* (§9)
* **PS-G-ReleaseBudget** — *"A ceiling on the total information released from an estate across all parties, operations, and time."* (§9)
* **PS-G-Receipt** — *"The record written for every crossing. If it cannot be written, the crossing does not happen."* (§9)

---

## Summary counts

* **Principle-level requirements:** 8 principles · 41 sub-clauses (P1.1..P8.5).
* **Flow-level requirements:** §3 query 6 steps + §4 training 5 steps = 11.
* **Precise-leave sub-clauses:** 4 (S5.1a..d).
* **Observables:** 7 (O1..O7).
* **Glossary terms:** 7 (G-Estate..G-Receipt).
* **Grand total:** **70 numbered requirements** to consider for future gating invariants.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
