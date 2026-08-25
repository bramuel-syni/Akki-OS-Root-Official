# T8 · What is "Walk this →" allowed to reveal? · Evidence from Docs 01/02/07/16

Owner Order 2026-08-19 sprint deliverable §5 · Owner question on T8: *"What's your question?"*

## The record — what the docs say (verbatim)

### Doc 01 · Custody & Crossing Pt 1 · A5.7–A5.8 · Trust receipt shape

> **A5.7 · The trust receipt [CANON]** A trust receipt is emitted per invocation. It is the key-custody envelope: evidence that the call happened and under what custody, constructed so that:
> - the receipt records that de-identification was applied and re-identification completed;
> - the receipt is signed and bound to the organisation alone, such that it cannot be reproduced or forged elsewhere;
> - the receipt is written to the one authoritative record (there is exactly one record; Document 16 §5 holds the record-ownership matrix).

> **A5.8 · Two custody pathways, both receipted, neither bypassing the other [CANON]** The platform has two custody pathways: the synthesis path through the chokepoint (text and structured payloads to a language model), and the perception path through the perception router (for example, audio reaching a model that reads it). Both emit receipts. Neither pathway is a way around the other.

### Doc 01 · destruction of the per-request envelope

> The per-request envelope is genuinely destroyed, verifiably. There must be no path — log, cache, trace, debug dump, error handler — through which the mapping survives the call. An error thrown mid-crossing must not spill the envelope into a stack trace or a retained error object.

### Doc 07 · A5.4–A5.5 · What "trace" is (Solva/five-ring shrink), and the faithfulness constraint

> **A5.4 · The trace exists from the first commit and joins to the record [CANON].** Every extraction-time judgement produces a trace carrying its reasoning path, its load-bearing units, and its computed class. The trace is not instrumentation added later — it is the auditability that justifies letting a component reason at all — and it carries a trace identifier joining it to the unit-level intelligence and to the record (Document 4, Document 5). **Unit and audit stay in separate envelopes with separate lifecycles, joined by identity rather than embedded, so a unit and its trace can be retained, exported, and expired independently.**

> **A5.5 · The trace is the executed reasoning, never a post-hoc narrative [RULED].** The trace must record the reasoning stages that were actually executed — the frame, the candidates, the tension surfaced, the reflection, the load-bearing set — not a summary written about the reasoning after the fact. … This is a genuine engineering constraint on how the trace is produced, and it is **load-bearing for the promise's honesty**.

### Doc 02 · B5.6 · Cumulative disclosure across the two items

> **B5.6 · Cumulative disclosure across the two items [RULED]** Two items that are each independently clean can, in principle, jointly reveal something neither reveals alone … At the re-association seam, the platform checks that the combination of File 1 and File 2 does not jointly disclose what each independently withheld — specifically, the material preservation and intent captured are checked for the potential to re-identify when paired, even where each file passed independently.

### Doc 16 · §5 · Record-ownership matrix

> The Ledger's ownership (Document 5), the Watch's own record classes (Documents 3, 14), the dual-file record's account (Document 2), the disclosure record (Document 6), and the cost/trace records (Documents 4, 11) are all classes in this one matrix. Where any document asked "who owns this record," the answer is: **one writer per class**, named here, never answered from memory and never differently in two places.

### Canon Addendum §3 · CA1-A8 (Universal claim-to-evidence trace)

> **A8 · Universal claim-to-evidence trace · Beyond canon — built ("Walk this →")**
> **Promise:** Any number, claim, or state anywhere on the platform can be traced to the mechanism or evidence behind it, in place, without losing your spot on the page.
> **Delivery Experience:** User can from any figure or claim, click once to reveal what produced it — the same affordance everywhere on the platform.
> **Open Design Question (load-bearing):** Does "Walk this →" inherit the source data's custody rules, so a viewer without access to the underlying estate region is refused the same way Document 1's chokepoint would refuse them — or can it leak view access to material the viewer isn't otherwise entitled to see? This is the load-bearing question: **an unscoped trace affordance is a second, ungoverned path to the same data Document 1 built one chokepoint specifically to control.**

## Reading the record

Three findings from the corpus, one qualifier, and one silence:

### F1 — The docs specify precisely what the receipt/trace object contains, and it is metadata + a governed trace, never raw record contents.

- **Trust receipt (Doc 01 A5.7)** = "evidence that the call happened and under what custody" + "records that de-identification was applied and re-identification completed" + signature bound to the org + one-authoritative-record location. **It does not carry the underlying identifiers; the per-request envelope is verifiably destroyed** (Doc 01 explicit-destruction paragraph).
- **Extraction-time trace (Doc 07 A5.4–A5.5)** = "the reasoning path, the load-bearing units, and its computed class" + a **trace identifier that joins to the unit** — but "Unit and audit stay in **separate envelopes** with **separate lifecycles**, joined by identity rather than embedded, so a unit and its trace can be **retained, exported, and expired independently**."

**Consequence:** what "Walk this →" is architecturally shaped to reveal is the **receipt/trace object** (actor · time · purpose · masking tier · what class of unit · what evidence class the claim carries · what rule fired · the receipt/trace ID). It is NOT architecturally shaped to reveal the **five-ring unit's content payload** — that is a distinct envelope on a distinct lifecycle.

### F2 — Post-hoc narrative is explicitly forbidden.

Doc 07 A5.5 is a [RULED] load-bearing honesty constraint: the trace records only executed reasoning, never a description-about-reasoning. **Any "Walk this →" implementation that composed a story from the outputs alone (rather than replaying the actual trace object) would be canon-illegal**, regardless of custody.

### F3 — Cumulative disclosure is a known named risk.

Doc 02 B5.6 codifies that two independently-clean items can jointly re-identify. "Walk this →" that composes multiple governed traces into a single view could re-open this risk even if each individual trace is receipt-only. **The re-association seam check specified for the DPO dual-file custody applies by analogy to any trace composition.**

### Qualifier — the underlying unit CAN be reached by clicking through, but only via the normal chokepoint.

Doc 07 A5.4's phrase *"and can follow any unit back to the precise place in the source it came from"* (in the "reader can see the trace behind it" paragraph) tells us the source can be reached from the trace. It does not tell us the trace UI is the way to reach it. The record-ownership matrix (Doc 16 §5) plus Doc 01 A5.8's "no bypass path" instruction is decisive: **any read of the underlying source content must transit the same chokepoint as any other read, bearing the viewer's permissions and mask tier.**

Which means "Walk this →" MAY offer a link to the underlying unit — but clicking that link is not a Walk-this action; it is a normal chokepoint-gated read that returns success or a refusal card exactly as any other read would.

### Silence — no essay uses the string "Walk this →"

The affordance is Addendum-only (CA1-A8). The 16 essays don't mention it by name. That means:
- The essays don't grant it any special reveal capability, and
- The essays don't forbid it either — they set the frame the affordance must sit inside.

The load-bearing question isn't *whether* to ship "Walk this →"; it is *how* to scope its reveal so it doesn't become the second data path Doc 01 built one chokepoint to prevent.

## The answer to be delivered to the owner

Given F1 + F2 + F3 + the qualifier + the silence:

**"Walk this →" is architecturally allowed to reveal the governed receipt/trace object only — actor · time · purpose · mask tier · unit class · evidence class · rule fired · receipt/trace ID · reasoning path (verbatim executed, per Doc 07 A5.5) — and MAY offer a link into the underlying unit that reopens the normal chokepoint read.** Clicking that link is not a Walk-this action; it is a fresh chokepoint-gated read that returns the unit content only if the viewer's permissions and mask tier permit it, otherwise a refusal card.

**"Walk this →" is NOT architecturally allowed to reveal the underlying record content in place, because:**
- the per-request envelope is verifiably destroyed at crossing time (Doc 01);
- the unit and its trace live in separate envelopes with separate lifecycles (Doc 07 A5.4);
- record-ownership is one-writer-per-class (Doc 16 §5) — a UI that composes reveal from more than one class must clear the re-association seam (Doc 02 B5.6);
- an in-place reveal that bypasses the chokepoint is the exact "second data path" Doc 01 A5.8 forbids.

## The question the owner asked ("what's your question?") — reformulated

Given the record above pins the affordance to receipt/trace + a chokepoint-gated deep-link, the only questions **left for the owner to rule** are:

- **Q1 · Read-through link on/off.** Does "Walk this →" carry the deep-link into the underlying unit (returning refusal for insufficient permissions) — or does it stop at the receipt/trace object and require a separate app-shell action to open the unit? Default recommendation: **link ON**, because it preserves flow and Doc 01 A5.8's "no bypass" is honoured by making the click a normal chokepoint read.
- **Q2 · Composability across classes.** May "Walk this →" render two trace envelopes side-by-side (e.g. a crossing receipt AND a Solva trace for the same claim)? Doc 02 B5.6 says compositions must clear a re-association check. Default recommendation: **compose from the same-actor, same-window scope only** (no cross-actor composition) until the re-association check is written.
- **Q3 · What the receipt-only view of a refused crossing shows.** Doc 01 says every crossing has a receipt including refusals. Does "Walk this →" on a refusal show the reason chain and the rule that fired? Default recommendation: **yes, verbatim** — Promise-Table §"Refusals are work done" and Doc 15 §"a block is the rules working, not a failure" both require it.

If the owner rules on Q1 · Q2 · Q3, W9 can proceed to build "Walk this →" custody-scoped, tests-first, without T8 remaining open.

## Impact on T8's original tension row

**T8 [A] recommendation stands:** do not ship the affordance until Q1 · Q2 · Q3 are ruled. The scope resolves the ambiguity but does not eliminate the need for an owner call on the read-through link.

**T8 [B] is now off the table:** the docs are not silent — an unscoped affordance that "shows the underlying record contents in place" is canon-illegal under Doc 01 A5.8 + Doc 07 A5.4 + Doc 16 §5.
