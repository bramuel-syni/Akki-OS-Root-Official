# R-25 · Seat Pricing Structure · Fixed by ENT-47

**Status:** Structure FIXED by ENT-47 · Defaults R-26..R-30 continue as tagged placeholders · R-31 agent-seat decision pending · Future owner-requestable pricing worksheet noted (not built unrequested).

**Owner disposition verbatim (2026-09-20T~21:24Z · this-session non-interrupting note):**

> "R-25 seat pricing — structure fixed by ENT-47: seat price per period by dial combination · credits per seat per period · credit price · volume/term discounts · R-31 agent-seat decision. Defaults R-26..R-30 continue as tagged placeholders; swap-in is a ruling, not a rebuild. The owner may later request a pricing WORKSHEET (inputs: local cost per token, provider rates per frontier row, target margin, expected mix; output: clearing seat price per dial combination) — 'it calculates; it does not recommend.' Note it as a future owner-requestable artifact; do not build it unrequested."

**Authority chain:** R-25 (owner-held pending seat pricing structure) + ENT-47 (Entitlement Service Spec v1 seat pricing rule) + R-26..R-30 (owner-tagged placeholder defaults) + R-31 (agent-seat decision · unopened).

**E1 scope boundary:** Record the fixed structure. Note the pricing-worksheet as future owner-requestable. Do NOT build the worksheet unrequested. Do NOT propose seat prices. Do NOT do market-benchmarking.

---

## Fixed structure (per ENT-47 · owner disposition today reaffirms)

The R-25 seat pricing structure consists of **five load-bearing dials** in fixed composition:

1. **Seat price per period by dial combination.**
   - *"seat price per period"* — the recurring subscription fee per seat.
   - *"by dial combination"* — the price varies by the combination of ratified dial values (tier · model access · region · usage class · etc. · exact dial-set per Master Requirements Registry v5 seat-pricing dimension).
   - Encoded as a lookup: `dial_combination → seat_price_per_period`.
2. **Credits per seat per period.**
   - How many usage credits the seat's period-subscription includes.
   - Also a lookup: `dial_combination → credits_per_seat_per_period`.
3. **Credit price.**
   - Per-credit price for credits purchased beyond the seat's period allocation.
   - May vary by dial combination or may be flat (owner-ruling determined; structure allows either).
4. **Volume/term discounts.**
   - Structured discount schedule based on volume (seats × periods) and/or term commitment.
   - Discount ladder is per ratified schedule; ad-hoc discounts are RULING, not rebuild.
5. **R-31 agent-seat decision.**
   - Owner-held. Agent-seats (versus human-user-seats) — how they price, how they count, whether they are separate SKU. Not yet ratified.
   - Placeholder in R-25 structure: `agent_seat_treatment = "R-31-owner-held-pending"`.

**Owner default-classing (R-26..R-30):**
- R-26 · R-27 · R-28 · R-29 · R-30: each is a tagged placeholder default. Owner disposition verbatim: *"Defaults R-26..R-30 continue as tagged placeholders; swap-in is a ruling, not a rebuild."*
- E1 keeps the placeholders tagged in the Entitlement Service pricing lookup table. Replacing them with concrete values is a **ruling** — owner-authored specific value replaces the placeholder; the surrounding structure does NOT change.
- No wave opens on R-26..R-30 concrete-value speculation.

---

## Future owner-requestable pricing worksheet (deferred · noted at owner's disposition · NOT to be built unrequested)

Owner disposition verbatim: *"The owner may later request a pricing WORKSHEET (inputs: local cost per token, provider rates per frontier row, target margin, expected mix; output: clearing seat price per dial combination) — 'it calculates; it does not recommend.' Note it as a future owner-requestable artifact; do not build it unrequested."*

### Worksheet contract (registered · not implemented)

**Inputs** (all owner-provided at worksheet-request time · nothing is inferred):
- `local_cost_per_token`: numeric · owner-known local cost per token by model.
- `provider_rates_per_frontier_row`: numeric table · per model-frontier-row provider list price.
- `target_margin`: numeric · owner-set target margin (percentage or absolute).
- `expected_mix`: distribution · owner-modeled expected usage mix across dials.

**Output** (deterministic · pure function of inputs · zero recommendations):
- `clearing_seat_price_per_dial_combination`: lookup table `dial_combination → clearing_seat_price`. Computed by the worksheet's fixed algorithm from the four inputs above.

**Discipline (owner-verbatim clause · load-bearing):** *"it calculates; it does not recommend."*

**Implication for E1 when the request lands:**
- E1 authors the worksheet as a **pure function** of the four inputs. No heuristics, no benchmarking, no market-comparison lookups, no "recommended range" fields.
- Output is a computed lookup table. Owner reads it and makes the pricing ruling. E1 does not steer that ruling.
- Any deviation from pure calculation (e.g., "typical" bounds, "reasonable" ranges, "market" comparisons) IS a violation of the load-bearing clause.

### E1 procedural gate (NOT built unrequested)

E1 does NOT build the pricing worksheet unless owner explicitly requests it. This note records the CONTRACT so when the request lands, the shape is on record and the build is mechanical.

Request-shape (owner-authored at request time):
> "Build the R-25 pricing worksheet per the contract at STATE/PROCEDURES/R25_SEAT_PRICING_STRUCTURE.md."

Only then does E1 open a wave for the worksheet.

---

## Standing bounds unchanged

- E1 does NOT propose seat prices · does NOT do market-benchmarking · does NOT recommend numbers.
- E1 keeps R-26..R-30 placeholders tagged and separable-from-structure.
- Owner rulings replace placeholders; structure stays fixed.
- Pricing worksheet is future owner-requestable · NOT built unrequested · pure-function-only when built.
- Zero push · zero remote configured · terminal-only operations.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law. Consult ENT-47 banking at CP-ENTITLEMENT-BUILD-WAVE `c4bf7094/eff17295/7d1e66a9` for structure authority.
