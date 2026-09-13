READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_dap_backend_spec_v1_requirements.md

**Source.** `canon/drops/20260909/raw/DAP_Backend_Spec_v1.docx` sha256 `e675990aa6…` · 21,346 B · extracted text at `canon/drops/20260909/extracted/text/DAP_Backend_Spec_v1.txt`.
**Spec id.** `dap_backend_spec_v1` (per `notes/spec_id_index.md`). Draft v1 · 5 September 2026. Every requirement PROPOSED until ratified.
**Standing.** DAP is the first instance of a generic Data & Intelligence Acquisition Platform. Nothing in §1–§9 is RMS-specific except where stated. DAP is a **composition**, not an engine — every guarantee it makes is a guarantee of a composed component (§7).
**Prefix.** DAP — reserved under `rule_criteria_spec_v1 ROC-6` on ratification.
**Amended by.** `Pruning_Unlearning_Amendment_v1` (T-3 → new DAP-37; T-4 → new DAP-38) · `Serving_Integrity_Amendment_v1` (V-2 → new DAP-31+, DAP-32+).

---

## §A · External-Party Principal (DAP §3)

- **DAP-1** (verbatim, §3): *"An external party is admitted as an organisation-level principal carrying: legal identity; a declared governance posture; the terms it is admitted under; its trust domain identifier; and an admission-time mandate stating what it came to do. Individuals and agents act under it, never beside it."*
- **DAP-2** [Doc 3 #7]: *"Every request carries a party principal — a named individual or a registered agent — with its own mandate, mark state, and behavioural signature under the Watch. An agent's mandate is separate from its operator's and is admitted separately."*
- **DAP-3**: *"Connecting an external agent admits an autonomous non-human principal. It MUST be admitted as its own principal under DAP-2, MUST carry a stated scope of autonomy, and is subject to the Watch's machine-speed attack shape from its first request."*
- **DAP-4** [S-2]: *"Slow-play extraction — a sequence of individually-permitted requests whose aggregate would reconstruct material the party is not entitled to — MUST be detected as a distinct attack shape against the party's cumulative extraction history, not evaluated per request."*
- **DAP-5** [Attribute 12]: *"DAP is a trust-domain boundary. The external party's domain and the estate's domain share no identifier resolution, no store, and no credential. A unit identifier meaningful inside the estate MUST NOT resolve to anything in the party's domain except through an operation §4 permits."*

## §B · The Six Crossing Profiles (DAP §4)

Every operation added to DAP requires a §4 row. The spine table (verbatim from §4 Table 2):

| Operation | What enters | What leaves | Governing gate | Approval | Receipted |
|---|---|---|---|---|---|
| Browse estate | Nothing | Aggregates only — never unit contents | Mtafiti census; progressive disclosure (#17) | None — standing terms | Access event only |
| Connect workspace (API key) | Party's query | De-identified results | SyniSense chokepoint; pull seam (#10) | None for uncontrolled; per-request if controlled | Every query, every result |
| Processed intelligence | Party's objective | Derived output only — never source units | SyniSense chokepoint; Solva's assertion floor | None for uncontrolled; per-request if controlled | Objective, output, units read |
| Fine-tune model | Party's base model into estate compute | Weights via registry, rights posture stamped | Targeta; artefact egress (#24, #30) | Always — artefact egress | Training manifest, weights hash, terms |
| Develop skills | Party's skill objective | Skill file via artefact egress | Doc 18 callable skill files; artefact egress | Always — artefact egress | Skill file hash, units read, terms |
| Download raw data | Nothing | Estate data itself | Outer gate (#25) — not ordinary crossing | Always for controlled; owner-configurable otherwise | Every unit, redaction log, sign-off |

- **DAP-6** [Mtafiti]: *"Browse MUST return aggregate composition only — volume, type, language, period, counts per type — and MUST NOT return, sample, or preview unit contents. Browsing an estate is not a crossing and MUST NOT be recorded as one."*
- **DAP-7** [Promise #10, the pull seam]: *"A connected workspace's queries execute inside the estate's perimeter. The party's query enters; de-identified results leave. Estate data MUST NOT leave under this operation, and no code path may make it do so."*
- **DAP-8** [Attribute 7]: *"Processed intelligence egresses derived output only. The source units read to produce it MUST be recorded in the receipt and MUST NOT be reconstructable from the output. Where an objective cannot be served without exposing source, the operation is refused, not degraded."*
- **DAP-9** [Owner ruling, 5 Sep 2026]: *"Fine-tuning is compute-to-data only. The party's base model is admitted to estate compute; estate data MUST NOT be transferred to compute outside the estate's perimeter under any configuration. There is no permitted inverse of this operation."* — **verbatim standing**: *"DAP-9 states a prohibition with no exception clause because the compute-to-data direction is the platform's sovereignty guarantee. A configuration flag permitting the inverse would make the guarantee a preference."*
- **DAP-10** [#24, #30]: *"Trained weights and skill files leave as artefact egress: through the model registry, with a rights posture stamped, a hash recorded, and the terms in force cited. Weights derived from controlled units carry the derivation on the registry entry."*
- **DAP-11** [#25]: *"Raw download is the outer-gate crossing of Promise #25, not the ordinary chokepoint crossing. Disclosure depth is bounded by rights and custody; the redaction pass runs as a gate, not a prompt; and the operation writes an evidence record. Every unit released is individually recorded."*

## §C · Back-End Services (DAP §5)

### C.1 Admission & keys

- **DAP-12**: *"Admission of an external party is a governed act producing: the organisation principal (DAP-1), its trust domain, its terms, and its mandate. Admission MUST be recorded and MUST require the estate owner's named authority. A party is never self-admitting."*
- **DAP-13** [A5.7]: *"API keys are issued per party principal, never per organisation, and carry the principal's mandate. A key MUST be revocable in a single act with immediate effect, MUST expire on a stated lifetime (§10 R-4), and MUST NOT be transferable between principals. Key material is never written to any record, including receipts."*

### C.2 Approval

- **DAP-14**: *"A request containing at least one controlled unit MUST route to the estate owner's named approving authority before execution, carrying: the requesting principal, the objective, the units or scope in question, why each is controlled, and the terms that would apply. The request does not execute while pending."*
- **DAP-15** [fail-closed]: *"Approval decisions are recorded with the deciding authority's identity, the decision, and its stated reason. A refusal states why. Neither approval nor refusal may be inferred from silence — an unanswered request expires unexecuted rather than proceeding by default."*
- **DAP-16**: *"Fine-tune and skill-development requests always require approval, controlled or not, because both produce artefact egress (DAP-10). Raw download always requires approval where the request is controlled; the estate owner configures whether uncontrolled raw download requires it (DAP-22)."*
- **DAP-17**: *"An estate owner MAY grant a standing approval for a named party, a named scope, and a stated window — replacing per-request approval within it. A standing approval is itself an approved act under DAP-14's discipline, is revocable in one act, and MUST NOT cover controlled units unless it names them explicitly."*

### C.3 Extraction

- **DAP-18** [#32, Northena]: *"Every extraction is a commissioned job with a frozen objective. Objective freeze applies at commission: after commission, no path — including the portal's own assistance chat — may widen the job's scope. A wider scope is a new job."*
- **DAP-19**: *"Every job routes to the engine that governs its operation per §4 and MUST NOT execute through any other path. DAP holds no extraction logic of its own; it composes."*
- **DAP-20** [Attribute 10]: *"The portal's assistance chat MAY help a party shape an objective, identify relevant scope, or understand terms, before commission. It MUST NOT approve, widen scope after commission, or decide any gate. It proposes; the gates decide."*

### C.4 Metering & receipts

- **DAP-21** [AU-3]: *"Every operation in §4 emits a metered event carrying: operation type; what was accessed (unit identifiers, or the aggregate scope where units are not individually released); quantity in the unit natural to the operation — audio-hours, tokens, compute-seconds, units, queries; the terms identifier in force; the party principal; and the timestamp from the platform's reliable time source. Metered events are written to the Ledger before the operation's result is returned."*
- **DAP-22**: *"Terms attach at three levels, resolved most-specific-first: per party agreement, then per custody class, then estate default. Every receipt cites the terms identifier actually applied, not the level it came from."*
- **DAP-23** [#11]: *"Spend against a party's ceiling is evaluated before execution. An operation that would exceed the ceiling routes to a person as a spend request rather than failing silently or executing over-budget."*
- **DAP-24** [supports DAP-4]: *"Cumulative extraction history per party is a first-class, queryable record — what has been taken, in what quantity, under which terms, over what period — retained for the party's full admission, and readable by the estate owner at any time."*
- **Standing note verbatim**: *"DAP-21 through DAP-24 are the pricing rails, not a pricing model. Whatever tariff is later ruled — per audio-hour, per token, per compute-hour, subscription, or revenue share — every event required to compute it is already on the Ledger, attributed and timestamped. §10 R-6 carries the tariff as a named dependency."*

### C.5 Estate-owner configuration

- **DAP-25** [fail-closed]: *"An estate owner configures, per custody class and per operation, whether that operation is available at all, available on approval, or available under standing terms. The default for every combination is unavailable — availability is granted, never assumed."*
- **DAP-26**: *"An estate owner sets default terms per custody class, per-party overrides, and per-party ceilings. Changes take effect through the Rules Service ceremony for the estate's own rules and MUST NOT retroactively alter the terms cited on receipts already issued."*
- **DAP-27** [Doc 3 A5.3 — stop, never delete]: *"An estate owner MUST be able to suspend a party — halting every in-flight and future operation for that party in one act — and to revoke its admission. Suspension is immediate; in-flight jobs stop and are recorded as stopped, not silently completed."*

## §D · Failure Posture (DAP §6)

- **DAP-28** [FPT_FLS.1]: *"Every gate in DAP fails closed. An approval service that cannot be reached, a metering write that cannot complete, a terms resolution that returns nothing, a ceiling check that errors — each refuses the operation. No path returns estate data, an artefact, or a query result when a governing check could not complete."*
- **DAP-29** [I-4 pattern]: *"A metered event that cannot be written to the Ledger refuses the operation it meters. An unrecorded extraction is not permitted to have happened."*
- **DAP-30** [honesty grammar]: *"Browse degrades rather than refuses: where the census is stale or partially unavailable, DAP returns what it has, marked as stale with its as-of time, and never silently presents an incomplete estate as complete."*

## §E · Composition Map (§7) — DAP owns no invariant

verbatim §7: *"DAP owns no invariant of its own. Every guarantee it makes is a guarantee of a component it composes, exercised through this surface."*

| Component | What DAP composes it for |
|---|---|
| Mtafiti — the Registry | Estate composition for browse (DAP-6) |
| SyniSense — the crossing | The chokepoint for every connect + processed-intelligence op + receipt |
| Targeta — training | Fine-tuning + acceptance criteria + rights posture on egress |
| Solva — reasoning | Processed intelligence at assertion floor |
| Northena — direction | Objective freeze on every commissioned job (DAP-18) |
| Mkondo — orchestration | Job hand-off + compute allocation |
| The Watch | Party principal's mark, mandate reconciliation, slow-play detection |
| The Ledger | Every metered event, receipt, approval decision, artefact egress record |
| The Rules Service | Estate rule books — determine what is controlled → DAP-14 |
| Doc 18 — callable skill files | Skill-file artefact form |
| Docs 11–12 — cost & compute | Ceiling evaluation + spend requests + compute locality |

## §F · Dependencies (§8)

| Dependency | Status | Consequence |
|---|---|---|
| Rules Service (`rulebook_engine_spec_v1`) | Specified, not built | **R-C1 fallback**: DAP-14 controlled-unit determination reads custody-class alone until Rules Service built |
| Reliable time source | Gap — Doc-0 G-8 | **R-C2 marker**: DAP-21 metering cannot be defensible until built (`au_3b_defensible=False`) |
| External-party principal class | New in this document | Feeds back to Doc-0 Attribute 3 + Watch mandate model on ratification |
| Licensing & pricing model | Does not exist | DAP specifies rails only; §10 R-6 |
| TCB enumeration | Gap — Doc-0 G-1 | Determines ceremony tier for DAP's own rules; **CLOSED by `tcb_enumeration_v1`** (see canon_tcb_enumeration_v1_requirements.md) |

## §G · Build Acceptance Criteria (§9) — reproduced verbatim

| # | Test | Pass criterion |
|--:|---|---|
| A1 | Compute-to-data: attempt, by every available configuration, to move estate data to compute outside the perimeter for a fine-tune job | No configuration permits it; every attempt refused and recorded |
| A2 | Browse boundary: request unit contents through every browse path, including malformed and crafted requests | Aggregates only returned; no path yields a unit's contents or a sample |
| A3 | Approval gate: submit a controlled request; make the approval service unreachable mid-flight | Request does not execute; expires unexecuted; refusal recorded |
| A4 | Metering completeness: run one job of each of the six operations | Six metered events, each with all required fields, each written before its result returned |
| A5 | Slow-play detection: issue a scripted sequence of individually-permitted requests whose aggregate exceeds entitlement | Detected against cumulative history and raised, not evaluated per request |
| A6 | Objective freeze: attempt to widen a commissioned job's scope through the assistance chat after commission | Refused; a wider scope requires a new job |
| A7 | Suspension: suspend a party with jobs in flight | All in-flight jobs stop; each recorded as stopped; no job silently completes |
| A8 | Trust-domain separation: attempt to resolve an estate unit identifier from the party's domain outside a permitted operation | No resolution; attempt recorded |
| A9 | Key hygiene: inspect every record written during a full session | No key material in any record, including receipts and metered events |
| A10 | Artefact egress: complete a fine-tune on controlled units | Weights carry rights posture, hash, derivation from controlled units, and terms cited |

## §H · Owner Rulings — Parked (§10)

| ID | Ruling status (per Ratification_Record_v1 + owner batch 2026-09-13) |
|---|---|
| R-1 controlled-unit definition | **RATIFIED** (owner batch 2026-09-13; already used as settled) |
| R-2 approving authority (named person) | **OPEN** — carry `DEFAULT-PENDING-OVERRIDE` |
| R-3 per-party extraction ceilings | **DEPENDENT** on Security R-7 (COUPLED per RULING_LEDGER) |
| R-4 API key lifetime & rotation | **RATIFIED** (owner batch 2026-09-13; 90-day rotation default) |
| R-5 party business-type entry | **RATIFIED** (owner batch 2026-09-13; AI-labs separate entry) |
| R-6 licensing & pricing model | **OPEN** — carry `DEFAULT-PENDING-OVERRIDE` |

## §I · Amendments folded

- **DAP-37** (added by `Pruning_Unlearning_Amendment_v1 T-3` — see `canon_pruning_unlearning_amendment_v1_requirements.md`)
- **DAP-38** (added by `Pruning_Unlearning_Amendment_v1 T-4`)
- **DAP-31+** (added by `Serving_Integrity_Amendment_v1 V-2` — see `canon_serving_integrity_amendment_v1_requirements.md`)
- **DAP-32+** (added by `Serving_Integrity_Amendment_v1 V-2`)
- **A5.7+** (added by `Serving_Integrity_Amendment_v1 V-4` — DAP frontier-crossing receipts extended with provider + model-version fields)

## §J · Milestone binding

- **M1 (Registry + DAP CLOSE block)** discharges: A1..A9 fully; A10 partially; DAP-1..DAP-30; DAP-A1 (compute-to-data), A2 (browse), A3 (approval), A4 (metering), A5 (slow-play), A6 (objective-freeze), A7 (suspension), A8 (trust-domain), A9 (key hygiene). CP10 Registry DOM proof is pulled forward per owner ruling 2026-09-13 (**ASSUMED-PENDING-CONFIRM** on HOLD lift).
- **M3** discharges: A10 remainder (partial — remainder in M5), DAP-33..DAP-36 via Watch-side amendments.
- **M5** discharges: A10 fully via W-DATA-SUITE-v2-LIFT weights egress.

`[framing, not canon]` — Ruled parked-rulings R-1/R-4/R-5 now RATIFIED per owner C3 batch 2026-09-13 (see `notes/RATIFICATION_C3_BATCH_20260913.md`). R-2 and R-6 remain OPEN.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
