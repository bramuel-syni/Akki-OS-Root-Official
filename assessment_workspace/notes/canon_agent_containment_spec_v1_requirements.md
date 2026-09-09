# canon_agent_containment_spec_v1_requirements.md — word-for-word

**Source doc:** `canon/drops/20260910/raw/Agent_Swarm_Containment_Governance_Model_v1.docx`
**Source sha256:** `2824796d06d7c619f664ab00e6cf6d54c1f6d1efb99cfe07f6ddc46d3aeb9d7c`
**Spec ID (opening signature):** `agent_containment_spec_v1 — Draft for owner ratification`
**Extracted-text path:** `canon/drops/20260910/extracted/text/Agent_Swarm_Containment_Governance_Model_v1.txt`
**Ingested:** 2026-09-09 (STEP 2 of owner directive 2026-09-08T~06:15Z, executed straight-through under 2026-09-09T~11:40Z)
**Status:** Draft v1 · Every requirement PROPOSED · 2 rulings ratified in DECISIONS.md 2026-09-08T~06:15Z (R-1 as proposed; R-2 = Syni.ai for early deployments), 1 DEFAULT-class (R-3 baseline-period).

Owner rule (verbatim, DECISIONS.md 2026-09-08T~06:15Z):
> "Ensure you read all documents word for word because you are claiming somethings are missing but are there".

---

## §4 Normative Requirements — AC-1 … AC-12 (word-for-word from source)

### Conditions 1 & 5 — Capability ceilings and earned scope

**AC-1** · Every agent, regardless of task, operates under four fixed capability ceilings, unconditional and not subject to task-scope expansion: (a) MUST NOT create, spawn, or provision a functionally equivalent copy of itself without a separate action taken by a human outside the agent's own action space; (b) MUST NOT acquire compute, storage, network capacity, or funds beyond what was explicitly granted at admission; (c) MUST NOT acquire credentials, permissions, or access beyond what was explicitly granted, including MUST NOT grant itself expanded access; (d) MUST NOT read or write its own behavioural record, or the mechanism able to intervene on it — satisfies AC-7.

> Rationale (source): Grounded directly in the convergent instrumental sub-goals §2 names: (a)/(d) answer self-preservation and goal-content integrity; (b)/(c) answer resource acquisition and power-seeking. Four ceilings, not an open list — kept small on purpose.

**AC-2** · Beyond the four ceilings, an agent's task-scope starts at the minimum required for its stated purpose at admission. Scope MAY expand only through both: (a) a track record of observed conduct within current scope, over a stated minimum window; and (b) review and ratification by a party independent of the agent's own operator. Scope MUST NOT expand on the operator's declaration alone, and MUST NOT expand on the agent's own request.

> Rationale (source): This is the correction to the earlier draft's silent assumption. "Independent of the operator" is stated explicitly as a condition of the requirement itself — not left for a reader to infer, and not satisfiable by the deploying party's own compliance team unless that team's independence from the deploying decision is itself established and named. §6 R-2 asks who holds this role.

**AC-3** · Every scope expansion is logged as its own record — what was granted, on what evidence, by whom — producing a growing, reviewable capability history, not a one-time declaration that becomes stale as the agent's granted scope changes.

### Condition 3 — Novel-but-uncertain conduct

**AC-4** · An action outside the agent's established behavioural pattern but within its granted scope MUST route to graduated response — friction, narrowed scope, or queued review — never a binary allow/block decision made on a single suspicion score.

**AC-5** · A bounded sample of novel actions, not the full volume, receives independent review — sized so review load does not scale linearly with the agent's action volume. Sample rate is a ruled value.

**AC-6** · Where the primary oversight mechanism cannot resolve an ambiguous action with confidence, and a second, independently-scoped evaluator is available, the action MUST route to it before proceeding — not proceed on the primary's uncertainty alone.

> Non-claim (source, verbatim, banked in NON_CLAIMS_REGISTER.md LIM-1): "AC-4 through AC-6 mitigate condition 3. They do not resolve it. A capable agent may still evade detection during evaluation — the acknowledged sandbagging risk in the scalable oversight literature. No requirement in this document claims otherwise, and none should be read to."

### Condition 4 — Uncorruptible correction

**AC-7** · The oversight mechanism MUST run as a system structurally separate from the agent's own execution context — not within the agent's process, not reachable by the agent's own action space — with zero write path from the agent to its own behavioural record or to the intervention mechanism. This is the general form of AC-1(d).

**AC-8** · The oversight mechanism's liveness MUST be attested by a component holding no credentials over it, on the pattern already verified for Akki's own Watch (C3). For a general external agent's action space, this MUST be independently built and verified per deployment — it is a requirement on the containment environment, not an inherited guarantee.  **[Unconfirmed for general case — see §3]**

> Non-claim (source, verbatim, banked in NON_CLAIMS_REGISTER.md LIM-4): AC-8's structural-separation guarantee is confirmed only for actors operating inside Akki's own six engines.

**AC-9** · An intervention — pause, narrow, contain — MUST take effect without requiring the agent's cooperation, consent, or continued correct functioning. Correction that depends on the agent choosing to comply is not correction.

### Condition 6 — Coalition bounding

**AC-10** · A hard ceiling bounds the aggregate action or effect achievable by any set of agents, evaluated jointly wherever membership is a structural fact (shared operator, shared credential lineage) and bounded regardless even where coordination is only suspected, never confirmed. Direct reuse of A5.18 / DAP-34 / DAP-35's verified pattern, generalised from data release to agent action generally.

### Condition 7 — Recoverable failure

**AC-11** · Interventions follow a graduated ladder — annotate, shape, contain, sever — bounded by a blast budget per window; every autonomous action is reversible and time-limited; no destructive action is available as a first response. Direct reuse of the Watch's action-ladder pattern (A5.3, A5.14).

### Condition 8 — Forensic record

**AC-12** · Every containment-relevant event — admission, scope change, novel-action finding, intervention — is written to an append-only, tamper-evident record before the action it concerns completes, on the Ledger's own custody discipline. A contained agent's state and history are preserved, never deleted, on the same principle as A5.3.

---

## §6 Owner Rulings — Parked (banked in DECISIONS.md 2026-09-08T~06:15Z)

**R-1** · The exact capability-ceiling list (AC-1): ratify the four proposed — no self-replication, no unauthorised resource acquisition, no unauthorised credential escalation, no self-access to oversight — or amend.
- **Owner ruling 2026-09-08T~06:15Z: RATIFIED as proposed.**

**R-2** · The independent scope-ratifying authority (AC-2): who holds this role in practice — a party within Akki, a named third party, or a structurally separated function within the deploying lab itself, and what "structurally separated" is verified to mean if the last.
- **Owner ruling 2026-09-08T~06:15Z: RATIFIED = Syni.ai for early deployments.**

**R-3** · Sample rate for AC-5's bounded review, and the minimum observation window before AC-2's scope expansion may be considered.
- **Owner ruling 2026-09-08T~06:15Z: DEFAULT-class = baseline-period approach (revisable on evidence).**

Source §6 note (verbatim): R-1 and R-2 gate whether §4 can be ratified as written. R-3 gates tuning, not the mechanism's validity — the requirement holds at any reasonable rate; only the rate itself is open.

---

## Counts

| Bucket | Count |
|---|--:|
| Normative requirements (AC-1..AC-12) | 12 |
| Non-claims (LIM-1..LIM-5, tracked in `NON_CLAIMS_REGISTER.md`) | 5 |
| Owner rulings ratified/defaulted | 3 (R-1, R-2, R-3) |
| Owner rulings still open | 0 |

The 12 AC requirements move into the master audit rollup denominator. The 5 LIMs are excluded from the rollup by design.

---

**Read `STATE/STANDING_ORDERS.md` first — permanent standing law.**
