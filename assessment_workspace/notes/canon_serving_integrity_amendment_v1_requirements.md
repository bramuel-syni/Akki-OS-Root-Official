READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_serving_integrity_amendment_v1_requirements.md

**Source.** `canon/drops/20260913/raw/Serving_Integrity_Amendment_v1.docx` sha256 `56af9f09c93e38ad8b80c6f70cd07c1dc03efba8c9661d2d9e717d54b3144269` · 15,863 B (owner-attached 2026-09-13).
**Spec id.** `serving_integrity_v1` (per §1 opening line).
**Standing.** 4 amendments · 1 new promise · 2 rulings · 13 September 2026. Governs **Akki-controlled serving paths only**. The frontier tier (Doc 14's gateway-only class: OpenAI, Anthropic, Google) runs on engines outside the platform's control; the floor cannot be imposed there — V-4 makes the receipt record which side of the boundary answered.
**Origin honesty condition (verbatim, Table 0 R2).** *"Identified while evaluating the Colibri inference engine (JustVugg/colibri, Apache 2.0), whose stated invariant — placement decides speed, never semantics — named the gap. The invariant is adopted as platform doctrine. The engine itself is NOT adopted by this amendment; admission of any specific engine is R-14."*
**Applies to (verbatim, Table 0 R0).** *"Doc 20 (new A20.15) · security_function_policies_v1 (new SFP-8) · dap_backend_spec_v1 (DAP-31, DAP-32 conformance clauses) · Targeta's evaluation path · agent_containment_spec_v1 (new AC-13, AC-14) · the trust receipt (Doc 1 A5.7, as amended by Security_Promise_Set_Amendments Amendment 3)."*
**What this closes (verbatim, Table 0 R1).** *"An unnamed gap: no rule anywhere governs the serving path between the registry and the gates. A5.8 forbids silent recalibration of rules; the registry hashes artefacts; MOAC accepts a specific model — nothing requires that the model served is, semantically, the one that was accepted."*

---

## §A · V-1 — The Serving Floor

**TARGET.** Doc 20 — new A20.15 (next free clause after existing fourteen). `security_function_policies_v1` — new SFP-8 (eighth named policy).

### A.1 · A20.15 (verbatim normative text)

> *"A registered artefact MUST be served semantics-stable: identical input, identical seed, identical sampling parameters produce identical output from the identical registered artefact, regardless of memory placement, hardware tier, concurrent load, or streaming vs. batched invocation. Where placement changes throughput or latency, the record MUST state so; semantics are not permitted to change unstated. Verified: (1) load-time hash of the served artefact against the registered hash — mismatch refuses to serve; (2) periodic reference validation — token-exact reproduction against a reference implementation on a scheduled cadence — failure refuses to serve; (3) a receipt field on every response naming the serving engine, its version, and its conformance state at the time of response. Values ruled at (§5 R-13)."*

### A.2 · SFP-8 (verbatim normative text) — The Serving Floor

> *"Subjects: any serving path executing a registered artefact. Objects: the artefact's semantics — precision, routing behaviour, context window, sampling. Operations: serve, degrade, refuse. Rule: degradation affects latency only, never semantics; a serving path that cannot prove semantic conformance refuses rather than serves. Anchor: Doc 3 A5.8 — the same no-silent-recalibration ethos applied one layer down, to the substrate under the rules layer, so the rules are administered on the model they were tested on."*

- **DERIVATION** (verbatim): *"Colibri's design rule ('insufficient fast memory may reduce speed; it must not quietly redefine the model'), generalised from one engine's internal discipline into a platform floor. A5.8 — the same no-silent-recalibration ethos, at the rules layer."*
- **PRINCIPLE** (verbatim): *"'We tested the model' is only worth something if the tested model is the one running. Pressure may make it slower, never different."*

## §B · V-2 — Gate Verdicts Inherit the Path That Computed Them

**TARGET.** `dap_backend_spec_v1` DAP-31 and DAP-32; Targeta's acceptance evaluations (MOAC, the yield wall's per-stratum accuracy).

- **DAP-31+** (verbatim): *"The reproduction probe MUST execute on an SFP-8-conforming serving path. A probe result computed on a non-conforming path is not a valid gate decision."*
- **DAP-32+** (verbatim): *"Battery results are valid only from an SFP-8-conforming path — deviation observed in the mirage is attributable to the model under test because the engine is required to contribute none."*
- **TGT+** (verbatim): *"Acceptance evaluations — MOAC's verdict, the yield wall's per-stratum measurements — run on SFP-8-conforming serving only."*
- **MECHANISM** (verbatim): *"Each gate's runner asserts the serving path's conformance — load-time hash check passed, reference validation current — before treating its own output as a decision. The posture on failure is FP-2's platform default: an unverifiable gate is a closed gate."*
- **DERIVATION** (verbatim): *"FP-2 (unconfigured gate refuses, platform-wide); SEC-4, SEC-6, SEC-7's refuse-if-unset pattern, extended from configuration to the serving substrate."*
- **PRINCIPLE** (verbatim): *"A gate's verdict inherits the integrity of the path that computed it."*

## §C · V-3 — Containment Freeze, and Serving the Contained Agent

**TARGET.** `agent_containment_spec_v1` — new **AC-13** and **AC-14**, extending AC-11 (graduated ladder) and AC-12 (record).

- **AC-13** (verbatim): *"'Contain' for a running agent session MAY be implemented as session freeze: the agent's inference state (prefix or recurrent-state checkpoint) is persisted, the session halts, and resumption restores the deepest surviving checkpoint. Stop without destroy (A5.3) is preserved: neither the artefact nor the session state is deleted. Reversibility (AC-11) is satisfied at deeper granularity than restart-from-turn-zero."*
- **AC-14** (verbatim): *"A contained agent's model MUST be served on an SFP-8-conforming path, so that behavioural deviation measured by detection is attributable to the agent, never to engine drift. A containment trigger computed from a non-conforming path is a finding, not a decision — the finding routes to review; the decision requires conformance."*
- **MECHANISM** (verbatim): *"Prefix and recurrent-state session checkpointing as implemented in current MoE serving engines — agent sessions restore from the deepest surviving checkpoint. Conformance assertion as in V-2."*
- **DERIVATION** (verbatim): *"A5.3 ('destroy does not exist in the Watch'); AC-11, AC-12; the checkpoint mechanism observed in the evaluated engine, adopted as a mechanism option, not as the engine."*
- **PRINCIPLE** (verbatim): *"Containing an agent means freezing its world, not burning it."*

## §D · V-4 — The Frontier Boundary, On the Record

**TARGET.** The trust receipt — Doc 1's A5.7 (as already amended once — principal identity + timestamp — by `Security_Promise_Set_Amendments Amendment 3`). Doc 14's gateway-only class.

- **A5.7+** (verbatim): *"Every frontier crossing's receipt MUST additionally record the provider and the provider-stated model version that served the response. SFP-8 is explicitly not imposable on gateway-only serving; the receipt records which side of the boundary an answer came from, so an audit can distinguish an Akki-controlled result from a provider-controlled one without having to reconstruct it. This does not weaken the boundary; it acknowledges it, on the record."*
- **MECHANISM** (verbatim): *"Provider and model-version fields read from the API response envelope and written into the existing receipt structure — an extension of fields, not a new record."*
- **DERIVATION** (verbatim): *"Doc 14 C5.1/C5.2 (the gateway-only licence class, providers named); this amendment's own honesty condition."*
- **PRINCIPLE** (verbatim): *"A control honest about its edge is worth more than one that pretends to reach everywhere."*

## §E · S-27 (new Watch-composite promise)

Reproduced verbatim from `Security_Assurance_Promise_Set_v2.xlsx` R28 (col "Promise"):

> **S-27** · *"The system will serve exactly the model it registered — pressure may make it slower, never different — and will say on the record which engine, its own or a provider's, produced every answer."*

- **Standard**: A5.8 (no silent recalibration, rules layer) · SEC-1/SEC-2 load-time integrity pattern · FDP_ACC.1 form (SFP-8) · invariants under Attribute 11 FP-2 posture.
- **Bound / Ruling**: R-13 (validation cadence, DEFAULT-class) open; floor explicitly **not imposable** on the frontier gateway tier — receipt records boundary.
- **Where it lives**: Serving Integrity Amendment V-1 (A20.15, SFP-8), V-2 (gate conformance), V-4 (receipt fields); TCB entry and failure-posture entries added.
- **System features**: (a) Artefact hash verified against register before first token; (b) Token-exact reproduction check on demand + schedule; (c) Response envelope carries provider + model-version fields for frontier crossings; (d) Failure = fail-closed refuse-to-serve.
- **User requirements**: *"User can (estate owner) trust that the model tested is the model running, under any load / User can (any consumer) see which engine — Akki-controlled or provider — produced any answer."*

## §F · Rulings (§7)

- **R-13** (DEFAULT-class): *"The reference-validation cadence for A20.15's operational check. Recommended default: on every engine version change and every artefact version change, plus a standing monthly run. DEFAULT-class — revisable on evidence, on Doc 3's own baseline-period pattern."*
- **R-14** (open, deliberately unruled): *"Whether the Colibri engine itself is admitted as the local rung's serving infrastructure. Not ruled here, and deliberately so: admission is gated on (a) the appliance benchmark — the smallest registered-family candidate on actual appliance hardware, per the appliance programme's own test discipline — and (b) the same admission ceremony any TCB-tier component undergoes. Neither has been run; ruling now would circumvent them."*

## §G · Placement in Standing Enumerations (§6)

- **`tcb_enumeration_v1`** addition (verbatim, Table 2 R1): *"IN: the serving-integrity gate — load-time hash verification plus conformance assertion. Deterministic; its failure falsifies S-27. OUT: the serving engine's bulk (scheduler, cache, placement logic) — deterministic, but its correctness is what the gate verifies; only the verification is TCB."*
- **`failure_posture_v1`** addition (verbatim, Table 2 R2): *"Serving path, semantic integrity unverifiable (hash mismatch; reference validation stale or failed) → fail-closed: refuse to serve. Preserved state: the artefact untouched, the refusal reason, the failed validation record."*

## §H · What this amendment does not do (verbatim §7)

*"It does not adopt any engine (R-14 gates that). It does not impose the floor on frontier serving (V-4 records the boundary instead). It does not make serving fast — the floor governs integrity, not performance. It does not require an internal open-source engine; SFP-8's properties are engine-agnostic. And it does not overrule Doc 20 — Doc 20 still governs the register; A20.15 governs what happens after registration."*

## §I · Milestone binding

- **M0** — this extraction file itself; supplement to `MILESTONE_PROMISE_BINDING_20260913.md`.
- **M1** — DAP-31+ / DAP-32+ conformance clauses land as **declared dependency markers** (per owner C5 disposition: reflection stays HALTed → any row genuinely requiring reflection's semantic content carries a declared dependency, not a guess). DAP §9 acceptance criteria A1..A10 unaffected in scope — SFP-8 conformance is a serving-path dependency, not a §9 pass criterion.
- **M2** — SFP-8 lands as an 8th named security-function-policy in the Rules-Service scope; TCB `serving-integrity gate` row lands in W-DOC0-ATTR1-TCB; FP entry lands in W-DOC0-ATTR11 (Failure Posture).
- **M3** — AC-13 + AC-14 land in W-AGENT-CONTAINMENT (in addition to AC-1..AC-12).
- **M4** — A5.7+ receipt-fields extension composes into DAP-20 assistance-chat + Journey-Assistant handoff surfaces.
- **M5** — V-2 TGT+ (Targeta acceptance evaluations SFP-8-conforming) lands as a dependency marker in W-DATA-SUITE-v2-LIFT.

`[framing, not canon]` — **R-13 default (monthly cadence) is auto-ratified under the C3 batch 2026-09-13** (Section 4-analog: recommended defaults en-masse ratified). R-14 remains OPEN per the amendment's own instruction.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
