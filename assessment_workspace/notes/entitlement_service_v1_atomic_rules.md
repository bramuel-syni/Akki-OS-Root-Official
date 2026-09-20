# Entitlement Service Spec v1 — Atomic Rules Extract

**Source**: `custody/owner_drops/20260920T1300Z/Entitlement_Service_Spec_v1.docx`
**Source sha256**: `46c3670eaf157173cb19e505d595b77d4458cc0f4b8f5aa6a055921b08fcfe04` (byte-verified against drop manifest `phase0/credential_drop_manifests/20260920T1300Z_entitlement_service_v1_drop_manifest.json`)
**Extracted at**: 2026-09-20T~15:00Z under CP-ENTITLEMENT-WAVE-SETUP (WAVE R-81 open · state-side extract preceding Commit-A code programme/track-a)
**Extraction method**: `python-docx` iteration over `Document.paragraphs`, style + text preserved verbatim; every ENT-N line reproduced as printed in the docx (no paraphrase, no re-flow, no punctuation change).
**Extraction receipt**: `phase0/spec_hunt_receipts/20260920T1500Z_entitlement_service_v1_extract.log`

Cross-reference targets:
- Master Requirements Registry v3 (564-row sheet) — expected ENT-1..ENT-49 as 49 rows in `System Rules Registry` sheet per drop manifest verification field `expected_families_added: ["ENT-1..ENT-49 (49 rows)"]`.
- Frontend fixed-strings register `/app/frontend/src/strings/entitlementStrings.js` (specialist-authored) — ENT-23/26/34 byte-match verified 2026-09-20T~15:00Z (see §Cross-check).

---

## §1  Definitions (12 defined terms · normative for this document)

- **Licence** — a terms object attached to one organisation principal (PRIN-1), resolved at the per-party-agreement level of DAP-22. Carries: plan, seat count, the two dials, credits per seat per period, pooled-credits flag, ceilings, period, renewal date, status.
- **Seat** — one individual principal (PRIN-1) or one agent principal acting under the licensed organisation. Seats are counted; the licence states how many.
- **Dial** — one of two buyer-set settings on a licence: the Compute dial (Managed or Yours) and the Frontier dial (Managed or Your Keys).
- **Catalog** — the platform's list of models available under any licence. One row per model.
- **Access class** — the source of a catalog row: local-served (a registered open-weight base served on platform or connected-tier compute), reseller-frontier (frontier capacity supplied through a provider reseller channel), customer-key (a frontier model reached under the buyer's own provider credential), or customer-model (a registered artefact the buyer brought or trained).
- **Credit** — the unit in which frontier usage is expressed to the buyer. Every reseller-frontier row carries one credit rate. Credits are a presentation of metered tokens, never a separate ledger.
- **Allowance** — the credits a seat, or a pooled organisation, holds for the current period.
- **Pool** — the organisation-level allowance when the pooled-credits flag is set; seats draw on it subject to per-seat soft limits.
- **Ceiling** — a hard limit that refuses further use in the period: a seat ceiling, an organisation ceiling, or a fairness ceiling. A soft limit warns; a ceiling refuses.
- **Fairness ceiling** — a concurrency or priority limit on local-served use. Never a token cap.
- **Period** — the licence's billing interval. Default: one calendar month.
- **Unlimited** — local-served use with no token cap in the period. Bounded only by a fairness ceiling. The word is used on a surface only where this definition holds.

---

## §2  Positioning Rules · ENT-1..ENT-4

- **ENT-1**  The licence is expressed to buyers and users in models: what is listed, what is included, what costs credits, what runs on their key. No surface names governance as the thing being sold.  `[Positioning]`
- **ENT-2**  Every governing mechanism that the licence relies on is presented as a feature included with every licence — the feature services in §12 — and no feature service is withheld by plan. Withholding a receipt, a ledger entry, or the shield from a cheaper plan would make governance a tier; it is a property.  `[Attribute 4; A5.5]`
- **ENT-3**  "Every model" on a surface means every catalog row with status listed whose access class the licence's dials admit. The phrase is never used to imply a model the dials exclude.  `[ENT-1]`
- **ENT-4**  "Unlimited" on a surface is used only for local-served use under the definition in §1. Frontier use is never described as unlimited.  `[§1]`

## §3  The Licence Object · ENT-5..ENT-8

- **ENT-5**  A licence is a terms object on exactly one organisation principal. It is created by the estate owner's admission act (PRIN-2) and resolves at DAP-22's first level, per-party agreement, ahead of custody-class and estate defaults.  `[PRIN-1, PRIN-2, DAP-22]`
- **ENT-6**  A licence carries, as required fields: plan identifier; seat count; Compute dial; Frontier dial; credits per seat per period; pooled-credits flag; seat soft limit; organisation ceiling; period; renewal date; status ∈ {active, suspended, expired}. A licence missing any required field does not resolve, and a call under it refuses.  `[FP-2]`
- **ENT-7**  A change to any licence field takes effect through the Rules Service ceremony at the ordinary tier and applies prospectively only. It MUST NOT alter the terms identifier cited on any receipt already issued.  `[DAP-26, RBM-8]`
- **ENT-8**  Suspension is a status on the licence, set by the estate owner in one act, refusing every subsequent call under it immediately. Suspension does not touch receipts, credits already recorded, or the catalog.  `[DAP-27]`

## §4  The Catalog · ENT-9..ENT-13

- **ENT-9**  Every catalog row carries: model identifier (a registry reference, hash-pinned per Doc 20); access class; status ∈ {listed, paused, retired}; residency; and, for reseller-frontier rows only, one credit rate. No other pricing field exists on a row.  `[Doc 20; ENT-1]`
- **ENT-10**  Adding a model is two acts: admission to the registry under Doc 20's base-registration rule and the DAP-32 admission battery where the model is an entering artefact; then a catalog row at the ordinary ceremony tier. Neither act alone lists a model.  `[Doc 20; DAP-32; RBM-8]`
- **ENT-11**  Retiring a model is a status change to retired. Calls to a retired row refuse with a fixed reason. Receipts citing the row are unaffected; the row is never deleted.  `[B.4; DAP-26]`
- **ENT-12**  Re-rating a reseller-frontier row changes one number through the ordinary ceremony tier, prospectively. A credit rate is never applied to usage metered before the change took effect.  `[DAP-26]`
- **ENT-13**  The catalog is read-only to every component except the ceremony engine. No surface, wizard, or assistant writes a catalog row.  `[RBM-5]`

## §5  The Two Dials · ENT-14..ENT-15

- **ENT-14**  The dials are the only plan-level variation. There is one licence SKU; a dial setting is a field on it, not a separate product.  `[ENT-6]`
- **ENT-15**  Setting the Frontier dial to Your Keys does not remove reseller-frontier rows from the catalog; it removes them from what the licence admits (ENT-3). A buyer may hold both: reseller-frontier for models they have no key for, customer-key for those they do, resolved per row (ENT-19).

## §6  Resolution at the Chokepoint · ENT-16..ENT-19

Preamble (verbatim): "Every call to any model already passes through exactly one function (A5.1, sealed at M12; PRIN-11 propagation). Entitlement resolution is a step inside that function, before dispatch. It is deterministic, and it fails closed."

- **ENT-16**  Before dispatch, the chokepoint resolves, in order: the calling principal (from propagated context, PRIN-11); its organisation's licence (ENT-5); the licence status (ENT-6); the catalog row for the requested or cascade-selected model (ENT-9); whether the row's access class is admitted by the licence's dials (ENT-3); and, for reseller-frontier rows, whether allowance remains (ENT-22). Any link that does not resolve refuses the call. No default licence, default row, or default allowance exists.  `[A5.1; PRIN-11; FP-2]`
- **ENT-17**  Resolution is a pure function of (principal, licence, catalog row, allowance state) with no parameter through which any learned component's output can enter. The cascade (D-16) may select the model; it cannot alter what the licence admits.  `[Attribute 10; A5.2 pattern]`
- **ENT-18**  There is no second path by which a model is reached under a licence. The existing negative-scan test (A5.1) is the proof; this document adds no new route and permits none.  `[A5.1]`
- **ENT-19**  Where a model is reachable under more than one access class for the same licence — reseller-frontier and customer-key — the customer-key row is selected. The buyer's own key is preferred over platform capacity whenever both exist.

## §7  Metering and the Bill · ENT-20..ENT-23

- **ENT-20**  Every call under a licence emits the metered event DAP-21 already specifies, with the licence identifier as the terms identifier in force. No entitlement-specific event type exists.  `[DAP-21]`
- **ENT-21**  The bill for a period is a query over the Ledger's metered events for the licence. There is no second billing store. An invoice line that cannot be derived from a receipted event does not exist.  `[B.4; DAP-29]`
- **ENT-22**  Credits are debited by computing metered tokens × the row's credit rate at the time of the event, from the Ledger. Allowance remaining is a derived value, recomputed from events, never a stored counter that can drift from them.
- **ENT-23**  Quantities always display; money displays only when measured. A reseller or provider that does not report cost yields cost_total null, rendered as the fixed string "cost · not yet measured". Credits, being derived from tokens and a known rate, are always measured and always display.  `[FE brief §2.1]`
  - **Fixed string** (binding on frontend + backend): `cost · not yet measured`

## §8  Credits, Limits, and Exhaustion · ENT-24..ENT-28

- **ENT-24**  A seat's allowance is credits per seat per period. With the pooled flag set, seats draw on the organisation pool subject to the seat soft limit; without it, each seat's allowance is its own.
- **ENT-25**  A seat soft limit warns the seat and its organisation admin at a ruled threshold (R-27) and does not refuse. An organisation ceiling refuses. Reaching a ceiling is a refusal, and a refusal is a first-class response, never an error (FE brief §2.2).  `[DAP-23]`
- **ENT-26**  When allowance is exhausted, the cascade (D-16) stops escalating to reseller-frontier rows and serves the job on a local-served row. The response carries the fixed string "Frontier allowance used · served locally". It MUST NOT serve locally without the string, and it MUST NOT refuse the job when a local-served row can serve it.  `[A5.5; D-16]`
  - **Fixed string** (binding on frontend + backend): `Frontier allowance used · served locally`
- **ENT-27**  Top-up is a purchase recorded as a prospective terms delta through the ordinary ceremony tier (ENT-7). Allowance is never extended by any component other than the ceremony engine.
- **ENT-28**  Unused allowance rolls over for exactly one period and then lapses (R-26, DEFAULT-class). Rolled-over credits are consumed before the current period's.

## §9  Unlimited Local · ENT-29..ENT-31

- **ENT-29**  Local-served rows carry no token cap in any period, under either Compute dial. The only limits are fairness ceilings: concurrent requests per seat and queue priority by plan, at ruled values (R-28).  `[§1 Unlimited]`
- **ENT-30**  On the Yours Compute dial, no platform-side fairness ceiling applies; the connected-tier data plane's own capacity is the only bound.  `[D-18]`
- **ENT-31**  Local-served rows are registered open-weight bases under Doc 20 or customer-model rows. The platform serves nothing under "unlimited" that it does not hold the right to serve without per-use cost.  `[Doc 20]`

## §10  Managed Frontier Through Reseller Channels · ENT-32..ENT-34

- **ENT-32**  Reseller-frontier capacity is supplied only under a written reseller or marketplace agreement with the provider, reviewed by counsel (R-24). A reseller-frontier row MUST NOT be set to listed before the agreement covering its provider is on record.  `[D-17]`
- **ENT-33**  The chokepoint is the only caller of any reseller channel. The crossing receipt records provider and model version (A5.7+, V-4). Capacity is pooled across licences on the platform side; attribution to a licence is by the metered event, never by a per-licence provider account.  `[A5.7; V-4]`
- **ENT-34**  A reseller channel that is unreachable or refuses is a closed gate for that row. The cascade serves the job on a local-served row with the fixed string "Frontier unavailable · served locally", or refuses if no local-served row can serve it. It never retries silently on a different provider.  `[FP-2; A5.5]`
  - **Fixed string** (binding on frontend + backend): `Frontier unavailable · served locally`

## §11  Bring Your Own · ENT-35..ENT-40

Sub-heading (verbatim): "Your keys"

- **ENT-35**  A provider credential the buyer supplies is held by the credential plane under envelope encryption, bound to the buyer's trust-domain identifier, usable by the chokepoint and by nothing else, never displayable after entry, and revocable in one act. Rotation replaces it; recovery does not exist.  `[PRIN-5, PRIN-6, PRIN-7]`
- **ENT-36**  Keys are held at organisation scope by default; a seat-scoped key is permitted and takes precedence for that seat (R-29).
- **ENT-37**  Every call under a customer key passes the custody sequence — masking before send, re-identification only inside — exactly as a call under platform capacity does. The buyer's key changes who is billed by the provider; it changes nothing about what leaves.  `[DAP-7; A5.1]`
- **ENT-38**  Calls under a customer key are metered for quantities (DAP-21). cost_total is null unless the provider reports it; no platform estimate is substituted.  `[ENT-23]`

Sub-heading (verbatim): "Your models and compute"

- **ENT-39**  A model the buyer brings or trains enters the catalog as a customer-model row only through registry admission: hash pin, the DAP-32 admission battery, and serving under the SFP-8 floor. It is listed only for the buyer's own licence unless separately admitted for wider listing.  `[Doc 20; DAP-32; SFP-8]`
- **ENT-40**  Compute consumed by a customer-model row on the Managed Compute dial is metered in GPU-seconds and drawn against a compute allowance on the licence (R-30). On the Yours dial it is the buyer's own compute and is not metered against the licence.

## §12  Feature Services Included With Every Licence

Preamble (verbatim): "These are the mechanisms the licence stands on, presented to the buyer as what they are worth. Each cites the component that provides it. Per ENT-2, none is withheld by plan."

*(No numbered ENT rules in §12 — narrative feature-service enumeration only. Referenced by ENT-2 as the mechanism list.)*

## §13  Seats, Organisations, Agents · ENT-41..ENT-42

- **ENT-41**  A seat is an individual or agent principal under the licensed organisation (PRIN-1). Seat count is a licence field; admitting a seat beyond the count refuses.  `[PRIN-1, PRIN-2]`
- **ENT-42**  An agent occupies a seat unless the licence carries an agent count as a separate field (R-31). An agent's use is metered to the agent principal, attributable to the organisation, under the agent's own mandate and containment (AC-1 ceilings apply irrespective of licence).  `[DAP-3; AC-1]`

## §14  Surfaces · ENT-43..ENT-46

- **ENT-43**  The model picker lists every catalog row admitted by the licence with one badge per row — Included · Local, Credits · Frontier, or Your key — and Auto at the top. Paused and retired rows do not appear. Rows the dials exclude do not appear.  `[ENT-3; FE brief §2]`
  - **Fixed badge strings** (binding on frontend picker): `Included · Local` | `Credits · Frontier` | `Your key` | `Auto`
- **ENT-44**  The usage surface shows credits remaining, tokens by model, and the fixed strings in ENT-23, ENT-26, and ENT-34 verbatim where they apply. It never renders a number that is not derived from the Ledger.  `[ENT-21, ENT-22]`
- **ENT-45**  The organisation admin surface manages seats, keys, pool, soft limits, and ceilings. It cannot edit the catalog or a credit rate (ENT-13).  `[ENT-13]`
- **ENT-46**  Every refusal on these surfaces routes through the platform's one refusal card with its binding copy. No entitlement-specific refusal component exists.  `[FE brief §2.2]`

## §15  Managing the Catalog · ENT-47..ENT-49

Preamble (verbatim): "The operating burden on the platform side is deliberately small, and this section fixes it so it stays small."

- **ENT-47**  Three numbers govern pricing across the whole scheme: seat price per period (by dial combination, R-25), credits per seat per period, and credit price. No model-specific plan, bundle, or exception exists.
- **ENT-48**  The operations on the catalog are exactly: add (ENT-10), pause, retire (ENT-11), re-rate (ENT-12). Each is a ceremony at the ordinary tier and each is receipted.
- **ENT-49**  No component of this service stores state that is not either a licence field, a catalog row, a credential in the plane, or a Ledger event. Any proposed store outside those four is out of spec.

## §16  Placement in the Standing Enumerations

*(No numbered ENT rules — placement narrative referenced by other canon anchors.)*

## §17  New Promise

*(No numbered ENT rules — companion promise banking referenced by Security Assurance Promise Set v5 S-31/S-32.)*

## §18  What This Does Not Claim · LIM-1..LIM-5

- **LIM-1**  It is not a payment processor. It produces a bill from the Ledger; collecting payment is conventional and outside this document.
- **LIM-2**  It does not set prices. R-25 to R-30 are commercial values; this document fixes where they apply and how they are changed, not what they are.
- **LIM-3**  It does not clear provider terms. ENT-32 makes listing conditional on an agreement counsel has reviewed; it does not assert what any provider permits.
- **LIM-4**  It does not guarantee frontier availability. It guarantees that unavailability is visible and that local service continues (ENT-34).
- **LIM-5**  "Unlimited" is bounded by fairness ceilings on Managed Compute. That is stated in §1 and on every surface that uses the word; it is not a hidden cap.

## §19  Rulings · R-24..R-31

- **R-24**  Reseller and marketplace agreements with frontier providers. Gates every reseller-frontier row (ENT-32). Counsel; owner signature. Nothing else in this document waits on it — Local and Your Keys ship without it.
- **R-25**  Seat price per period by dial combination, and the discount for Yours Compute and Your Keys. Commercial. Candidate answer to R-6.
- **R-26**  Rollover: recommend one period. `DEFAULT-class`.
- **R-27**  Seat soft-limit threshold: recommend 80% of allowance. `DEFAULT-class`.
- **R-28**  Fairness ceiling values on Managed Compute: concurrent requests per seat and priority tiers. Recommend baseline-period approach on measured load. `DEFAULT-class`.
- **R-29**  Key scope: recommend organisation by default, seat-scoped permitted with precedence (ENT-36). `DEFAULT-class`.
- **R-30**  Compute allowance for customer-model rows on Managed Compute, in GPU-seconds per seat per period. `DEFAULT-class`, baseline-period approach.
- **R-31**  Whether agents count as seats or carry a separate count. Product decision. Recommend: seats by default; separate count available at organisation size.

**Design note** (verbatim, spec closing): "The service is small on purpose. Its entire state is four things that already exist or are trivially bounded — a licence, a catalog row, a credential, a Ledger event — and its only decision is a pure function at a point every call already passes through. If a build of this service grows a queue, a cache of balances, a second event type, or a route around the chokepoint, it has left the specification."

---

## Cross-check · Fixed strings vs `/app/frontend/src/strings/entitlementStrings.js`

**Specialist-authored file** (read-only cross-check per sprint-order Task 4 · this desk MUST NOT edit `/app/frontend/*` except `/app/frontend/public/audit/`):

| ENT | Fixed string (spec docx verbatim)              | JS constant                    | Bytes match? |
|-----|------------------------------------------------|--------------------------------|--------------|
| ENT-23 | `cost · not yet measured`                     | `ENT_23_COST_NOT_MEASURED`     | ✅ (`\u00b7` = U+00B7 MIDDLE DOT · UTF-8 `c2 b7`) |
| ENT-26 | `Frontier allowance used · served locally`    | `ENT_26_FRONTIER_EXHAUSTION`   | ✅ |
| ENT-34 | `Frontier unavailable · served locally`       | `ENT_34_FRONTIER_UNAVAILABLE`  | ✅ |

**Verification method** (banked at `phase0/spec_hunt_receipts/20260920T1500Z_entitlement_service_v1_extract.log`): python3 script iterated `Document.paragraphs`, compared UTF-8 byte string against the JS file's `\u00b7`-escaped constants. All three matched byte-for-byte inside their respective ENT paragraph body.

**Owner rule (verbatim, from drop manifest `banked_reason` field)**: "adds S-31 + S-32 to Security Assurance Promise Set" — fixed-string binding on frontend surfaces is a substitution-rule discipline registered via ENT-44 and enforced structurally at any downstream test that reads the picker or usage surface.

**Additional binding badge strings** discovered in ENT-43 body: `Included · Local` | `Credits · Frontier` | `Your key` | `Auto` — these are also fixed strings on the model picker surface; the specialist has not yet registered them in `entitlementStrings.js` (flagged for owner as an OPEN CROSS-CHECK ITEM at wave-close report; not this-desk's write scope).

---

## Sub-wave sequence anchor (per sprint order 2026-09-20T~15:00Z)

**CP-ENTITLEMENT-WAVE-SETUP** (this wave, R-81 · own 3-Commit Seal):
1. This atomic-rules extract (state-side)
2. Objective card `STATE/OBJECTIVES/ENTITLEMENT.md`
3. RED-first property tests `backend/tests/invariants/test_entitlement_service_v1_property_tests.py` (11 tests · ENT-13/16/17/18/19/22/26/32/34/35/49)
4. Grep-negative hard bans in same test file
5. Fixed-string substitution-rule attestations (ENT-23/26/34 byte-match) — one attestation test per string

**CP-ENTITLEMENT-BUILD-WAVE** (next wave, R-82 · own 3-Commit Seal · out of scope this wave):
- Local + Your-Keys paths only (Managed Frontier reseller-channel UNLISTED pending R-24 counsel review · LIM-3 verbatim)
- R-26..R-30 defaults tagged pending owner ratification (rollover 1 period · soft-limit 80% · fairness ceilings baseline · key scope organisation · compute allowance GPU-seconds)
- R-31 seats-as-default with separate agent count available at organisation size
- Implementation modules `services/entitlement_service_v1/` compose principal_store + credential_plane + Ledger (per §12 feature-services) · no new identity system · no new metering path · no new bill

**HARD HOLDS not built at CP-ENTITLEMENT-BUILD-WAVE**:
- R-24 reseller/marketplace agreements (counsel · owner signature) — every reseller-frontier row stays UNLISTED until on record per ENT-32
- R-25 pricing values (commercial)
- Managed Frontier reseller-channel path (`services/entitlement_service_v1/reseller_channel.py` not authored until R-24 rules)

---

## Standing bounds honoured by this extract

- **Zero paraphrase** — every ENT-N line, LIM-N line, R-N ruling, defined term, and preamble is byte-verbatim from the docx source (python-docx iteration preserving whitespace and typographic characters including the U+00B7 middle dot in fixed strings).
- **SO §4.1 §F sha-pinning** — source docx sha256 recorded at file head and byte-verified against drop manifest.
- **SO §4.1 §E custody** — source stays at `custody/owner_drops/20260920T1300Z/` immutable; this extract is a state-side note only.
- **SO §3.8 thin-kernel additive-only** — this extract adds a NEW file; edits no sealed contract or writer.
- **SO §6.4 NOTHING-BEYOND** — scope frozen at 49 ENT + 12 defined terms + 8 rulings R-24..R-31 + 5 LIM + 4 badge fixed-strings; no re-derivation, no synthesis, no cross-registry mapping (that lives at G5 continuation P2 backlog against 564-row registry v3).
- **Frontend write-ban** — this desk did NOT edit `/app/frontend/*` at this wave. Only READ from `/app/frontend/src/strings/entitlementStrings.js` for cross-check verification.

END OF EXTRACT.
