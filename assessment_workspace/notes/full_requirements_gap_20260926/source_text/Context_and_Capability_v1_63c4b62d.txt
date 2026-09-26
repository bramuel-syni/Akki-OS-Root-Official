[B1] AKKI PLATFORM  ·  AMENDMENT  ·  DOCUMENTS 1, 7, 8, 11 AND THE MEMORY LAYER

[B2] Context and Capability

[B3] context_and_capability_v1 — the six operational gaps between the context-preservation nets as designed and as measured

[B4R1] What exists | Document 1: extract-intent → de-identify → invoke → re-identify, meaning extracted before masking. Document 7: the five-ring unit, the re-extraction handle, qualification partitioning, the executed trace. Document 8: one write path, the unit as frozen seam, warm serving synchronous and full, fresh fetch async for the unconverged slice only. Document 11: local-first cascade. Together these are the nets against three failures — capability lost at the crossing, context thinned, work slowed.

[B4R2] What is missing | Six things that only appear in operation: a routing rule for objectives that need a model's own knowledge of a masked entity; a rule for which units enter the window when not all fit; a throughput floor for the Ledger writer; a latency budget and a warm-serve ratio as reported numbers; an availability requirement for the three services that can stop everything; and a benchmark that measures what governance costs. Plus two documentation gaps.

[B4R3] What this adds | Eight requirements, three of them numbers with DEFAULT values, one standing objective card, four named audit checks, and one citation correction. Nothing here changes a guarantee; everything here makes a guarantee measurable or closes the one place a guarantee could be undone at the last step.

[B4R4] Principle | A net that is designed and not measured is a belief. Each requirement below either rules a number, rules the one missing decision, or produces the evidence.

[B4R5] Date | 27 September 2026

[B5] 1   Definitions

[B6] Entity-knowledge objective  an objective whose intent, as extracted by Solva before de-identification, requires a model's own knowledge about a specific real-world entity — not the estate's material about it — and that entity is in a controlled custody class.

[B7] Window  the material assembled for one model call: the frozen objective, the qualified units selected, and the frame.

[B8] Assembly  the deterministic selection and ordering of qualified units into the window when the qualified set exceeds it.

[B9] Request class  one of: warm (served from stored qualified intelligence, synchronous); fresh (unconverged slice, asynchronous); controlled (awaiting an approval decision). Every request is exactly one.

[B10] Gate service  a service whose unavailability refuses every operation that depends on it: the Rules Service, the Ledger writer, the credential plane.

[B11] Governed path / bare path  the same model called through the platform with every gate engaged, and called directly with no gate, on the same task.

[B12] 2   Routing for Entity-Knowledge Objectives

[B13] Document 1's sequence preserves meaning across the crossing. It cannot give a frontier model its own knowledge of an entity whose name it never sees. Today nothing decides what to do with an objective that needs exactly that.

[B14] CC-1  The intent extractor (Document 1) classes every objective as entity-knowledge or not, from the extracted intent, before de-identification. The class is recorded on the frozen objective and is not revisable downstream.  [Doc 1; Doc 5 freeze]

[B15] CC-2  An entity-knowledge objective on a controlled entity routes to the Local catalog by requirement, not by cascade preference. It crosses to a frontier model only under an owner approval recorded against the entity's custody class (DAP-14 pattern), and then crosses with the entity unmasked for that call only, receipted as such. Absent the approval, the objective is served locally or refused with the reason stated — never served by a frontier model with the entity masked and the result presented as complete.  [Doc 11 A5.4; DAP-7; A5.5]

[B16] CC-3  Where an entity-knowledge objective is served locally and the local model's knowledge of the entity is insufficient, the answer states that the entity was withheld from external models by custody class, in a fixed string from the Content Registry. The reader learns why the answer is bounded; the platform does not guess to fill it.  [CON-2; A5.5]

[B17] 3   Window Assembly

[B18] Document 7 makes every unit complete and re-derivable. Document 8 makes what the model reads stable. Neither says which units are read when there are more than the window holds. That is the one step at which context is actually thinned, and it must be a rule, not an implementation choice.

[B19] CC-4  Assembly is a deterministic ranking of the qualified units for the frozen objective, in this order: units the objective's frame names as load-bearing; then by defensibility class, highest first; then by relational proximity to the objective's named entities and scope (the unit's relational-edges ring); then by recency of the unit's source position. Ties break by unit identifier. The same objective and the same qualified set produce the same window.  [Doc 7 A5.1; Doc 8 A5.3]

[B20] CC-5  When units are left out, the window carries a loss statement: counts of excluded units by defensibility class, and the re-extraction handles of the ten highest-ranked exclusions. The statement travels with the trace. An answer composed from a window with a loss statement states that material was excluded and by what rule — in the same fixed-string form compaction uses on reload.  [MEM-8; Doc 7 A5.4]

[B21] CC-6  No learned component reorders or filters the window after assembly. The drafting model reads what assembly produced. A retrieval or reranking model may propose a ranking rule change through the research queue; it never ranks live.  [Attribute 10; A5.22]

[B22] 4   Numbers That Must Exist

[B23] CC-7  Ledger writer throughput floor. Per tenant, the writer sustains not fewer than R-41 receipts per second at a per-receipt latency not exceeding R-42, measured under load on the deployed hardware before the tenant is opened to users, and re-measured at every image release. A measured figure below the floor is a release blocker for that tier. The figure is on the tenant's operations surface.  [B.4; DAP-21]

[B24] CC-8  Latency budget per request class. Warm: end-to-end, gates engaged, not exceeding R-43. Fresh: acknowledgement within R-44, with the delivery estimate the async contract already requires (Doc 8 B5.3). Controlled: the time to the approving authority's queue not exceeding R-43; the decision time is the human's and is reported, not budgeted. Budgets are measured on the governed path at the 95th percentile and reported per tenant per period.  [Doc 8 B5.3]

[B25] CC-9  Warm-serve ratio. The share of requests served from stored qualified intelligence without a fresh fetch, per tenant per period, on the usage surface next to the latency figures. It is the number that says whether Document 8's promise is being kept; a falling ratio is investigated, not explained away.  [Doc 8 A5.4]

[B26] 5   Availability of Gate Services

[B27] Fail-closed is the correct posture and it makes every gate service a single point of refusal. Correct refusal at scale is still an outage. The three services that can stop everything need an availability requirement and a stated form of resilience; nothing else in the platform does at this stage.

[B28] CC-10  The Rules Service, the Ledger writer, and the credential plane each carry an availability target (R-45) and a stated resilience form: the Rules Service serves its last-verified rule set from a signed local copy when its store is unreachable, with changes refused until reconnection; the Ledger writer runs active-standby with a mirrored Ledger device on tiers that have one, and failover is a receipted event; the credential plane refuses issue and revoke when unreachable but continues to *verify* presented credentials from its sealed cache, so existing sessions continue and no new credential is minted blind.  [FP-1; D-19; PB-15]

[B29] CC-11  Unavailability of a gate service is surfaced on the tenant's operations surface as such, with the fixed string for the affected request classes. It is never presented as a request failure attributable to the requester.  [A5.5; CON-2]

[B30] 6   The Capability Benchmark — a Standing Objective Card

[B31] Every argument that governance costs only what custody and the record are worth is design reasoning until this runs.

[B32] CC-12  A fixed task set of not fewer than 200 tasks across four classes — retrieval, synthesis, multi-step reasoning, entity-heavy — with reference answers, held under the estate owner's custody and never used for training. Each task runs through the governed path and the bare path on the same model and seed. Quality is scored by a deterministic rubric per class against the references; latency is measured end to end. The delta per class, quality and latency, is reported per release.  [standing card]

[B33] CC-13  A quality delta beyond R-46 in any class is a release finding: the release ships only with the delta stated on the release note and a named cause — masking, window assembly, cascade routing, or refusal — each of which has a lever in this amendment. A delta with no named cause does not ship.

[B34] CC-14  The benchmark runs under the Execution Standard: denominator the task set, artefact one row per task per path, acceptance the reconciliation and the rubric scripts, re-performance by a second instance on a seeded sample. The report is the artefact, and the release note cites its hash.  [EX-1 to EX-15]

[B35] 7   Documentation Corrections

[B36] CC-15  memory_compaction_v1 is amended to state that the unit it compacts is Document 7's five-ring normalised unit; that facts kept by hash pointer are kept by the unit's re-extraction handle; and that a compacted lineage is a derived artefact over units, never a parallel representation of them. MEM-1 through MEM-11 are unchanged in effect; the citation is added.  [Doc 7 A5.1, A5.2]

[B37] CC-16  Four named checks are added to the audit's surface list (Audit Standards v2 §6), verified as functional demonstrations by a party holding no builder credential: (a) shrink a unit and regenerate it from its re-extraction handle — identical content ring; (b) submit degraded material and show it lands unqualified, never in an evidence partition; (c) serve a warm objective and show it returned synchronous and full within the budget; (d) submit an objective containing a controlled entity and show the extracted meaning crossed with the entity masked and re-identified inside — or, if entity-knowledge, that CC-2 routed it.  [Audit Standards v2]

[B38] 8   Placement

[B39R1] Document | Entry

[B39R2] tcb_enumeration_v1 | IN: the entity-knowledge classification decision (CC-1, CC-2) and window assembly (CC-4) — deterministic; failure falsifies S-35. OUT: any proposing model under CC-6; the benchmark harness (evidence producer).

[B39R3] determinism_inventory_v1 | Window assembly: Deterministic. Routing: Deterministic on a Solva-extracted class.

[B39R4] failure_posture_v1 | Amended per CC-10: the three gate services gain stated resilience forms. Assembly cannot rank (qualified set unreadable) → refuse, never serve an unranked window. Benchmark harness unavailable → release note states no measurement; the release does not ship as “measured.”

[B39R5] Content Registry | Fixed strings for CC-3, CC-5, CC-11 registered at the ordinary ceremony tier.

[B39R6] Master Requirements Registry | CC-1 through CC-16 and S-35 at this refresh.

[B40] 9   New Promise

[B41R1] ID | Promise | Rests on

[B41R2] S-35 | What governance costs is measured and stated: which material entered the window and what was left out, why an entity was withheld from an external model, how fast each class of request is served, how often memory served it warm, and the quality delta of the governed path against the bare model — on every release, in numbers. | CC-1 to CC-16. Bounds: R-41 to R-46. Scope edge: the human decision time on a controlled request is reported, not promised.

[B42] 10   What This Does Not Claim

[B43] LIM-1  It does not remove the cost of masking. An entity-knowledge objective on a controlled entity is served locally or by approval; that is slower or narrower than an unmasked frontier call, and CC-3 says so on the surface rather than hiding it.

[B44] LIM-2  It does not guarantee the numbers. R-41 to R-46 are ruled floors and budgets; a deployment that misses them is a deployment that is told so, not one that is quietly declared fine.

[B45] LIM-3  It does not make the benchmark's rubric perfect. A deterministic rubric measures what it measures; the reference set is versioned and its coverage is stated with each report.

[B46] 11   Rulings

[B47] R-41  Ledger writer throughput floor, receipts per second per tenant. Recommend 500 on Start, 5,000 on Grow, from first-article measurement. DEFAULT-class.

[B48] R-42  Per-receipt write latency ceiling. Recommend 10 ms at the 95th percentile. DEFAULT-class.

[B49] R-43  Warm end-to-end budget and controlled time-to-queue. Recommend 2 s at the 95th percentile on Start; 1 s on Grow. DEFAULT-class.

[B50] R-44  Fresh acknowledgement budget. Recommend 500 ms. DEFAULT-class.

[B51] R-45  Gate-service availability target. Recommend 99.9% measured monthly per tenant, with the resilience forms in CC-10 as the mechanism. DEFAULT-class.

[B52] R-46  Capability delta threshold per class before a release is a finding. Recommend 3 points on a 100-point rubric for retrieval and synthesis, 5 for reasoning and entity-heavy. DEFAULT-class until the first three benchmark runs set a baseline.

[B53] Design note. Three of these gaps were closed by rules and three by numbers. The rules could have been written on the first day; the numbers could not, because they come from hardware and load the platform did not have. That is the normal shape of this kind of amendment, and it is why the benchmark is a standing card and not a one-time test: the numbers change with every release, and a governance layer that cannot state its own cost on each one is asking to be trusted in exactly the way it forbids everything else to be.
