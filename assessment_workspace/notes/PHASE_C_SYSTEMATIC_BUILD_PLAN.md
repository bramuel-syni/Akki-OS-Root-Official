READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# PHASE_C_SYSTEMATIC_BUILD_PLAN.md

**Purpose.** A systematic build plan for three named waves — W-REGISTRY-FULL-BUILD, W-DAP-STACK, W-SOLVA-V2-LIFT — grounded on the amended `SYSTEM_OBJECTIVES_AND_PROMISES_CHARTER.md` (Phase B) and constrained by the platform-vs-job separation doctrine and the W1/W1b/W1c Work-Supervisor primitives.

**Date.** 2026-09-13 (Phase C, per owner ruling D this session).
**Standing.** Document-only. NO code, NO tests, NO ratchet movement, NO egress. All standing orders unchanged: SO §2 DECISION-POINT reporting; SO §3 no-silence; SO §4 local commits only / NEVER push; `BASELINE_GUARD=1`; ratchet 3503 untouched; `testing_agent` BANNED (terminal pytest only).
**Provenance.** Every canon anchor below is verbatim-cited from a file opened first-hand this session (see charter §0.1). `[framing, not canon]` tagging is standing practice — no silent normalisation.

---

## §0. Precedence, discipline, and what this plan is NOT

### §0.1 Standing discipline that binds Phase C

Recited so no reader mistakes it for negotiable:

- **W-SOLVA-V2-LIFT is a STANDALONE wave** (owner Amendment 1 · Phase C, this session, verbatim): "as a STANDALONE component in this same wave, NOT a sub-component of Registry or DAP (owner's explicit instruction: lift the donor pool from Akki-Executive-Core as a standalone reasoning component)". This plan draws Solva as a peer wave to Registry and DAP, sequenced by dependency only.
- **Platform vs. job separation** — Canon-1 §4.6 verbatim: "New capability extends an existing component. It does not create a sibling. When the platform gains the ability to handle a new kind of material, the registry gains a modality, not a sibling registry. When it gains a new class of recorded event, the record gains a data class, not a second ledger. A proposed component that would need its own record, its own rules, and its own approval path is a sibling, and it is wrong." Applied here: Registry (platform), DAP (composition surface, per DAP-Spec §7), Solva-v2 (an engine's own reasoning core) each extend without proliferating.
- **W1/W1b/W1c primitives are the substrate** (fork context, banked at ratchet 3503): case-agnostic Work-Supervisor with `job_kind` registration, generic `AttributeStreamBundle_v0` (5-ring unit contract, Canon-4 §30), `SourceConnector` interface, `RetentionPolicy` object, generic capability registration under registry evidence classes (OpVal-v1.1 FACT/NORM/DEFAULT). Every wave in this plan binds to these primitives without adding a parallel substrate.
- **Function & Promise Registry rent** — Canon-7 §37 verbatim: "No gate without a promise. No promise without a service trace. No journey step without enforcement. New functions register before they land." Every new function or checkpoint proposed in this plan registers its F&P row on the same ruling surface, not as a follow-up.
- **Two-commit pattern** — STANDING_ORDERS §3 verbatim: "Commit A (code): repos/Extraction-Akki/ on branch programme/track-a. Commit B (state): /app/assessment_workspace/ on branch master — STATE, notes, phase0 receipts, canon drops, prototypes. Never push."
- **Double-green byte-match to close** — STANDING_ORDERS §3 verbatim: "BASELINE_GUARD=1 python -m pytest under the repo root, run twice back-to-back, byte-identical tally. Both receipts banked."
- **Alive-is-not-done** — STANDING_ORDERS §3.1 (charter P-SO-1). Every wave close in this plan produces an `output_verified_seal` with a real work-kind, not a heartbeat.
- **No run without a progress signal** — STANDING_ORDERS §3.2 (charter P-SO-2). Every commissioned run binds to `runtime_supervisor.record_progress`.

### §0.2 What this plan does NOT do

- Does not propose code. Every wave below is described as scope + gating tests + close conditions, not implementation.
- Does not touch the ratchet. Ratchet 3503 is banked; every wave close appends a new floor per the ratchet-monotonic-up discipline of STANDING_ORDERS §3.
- Does not open W2 (audio real-mount). W2 remains hard-stopped on owner rulings (charter §4.3).
- Does not egress. The bastion `${bastion.jump_server_radio_system}` handle is banked (0600, non-echoed, `/app/backend/estate_keys/bastion/`); it appears only where materially load-bearing in §D (deferred SourceConnector touchpoint under the egress-window constraint), and no operation is scheduled here.

### §0.3 Two named risks carried through every wave

Per owner Amendment 3 (Phase C, this session, verbatim):

**Risk R-C1 · Rules Service dependency (spec-complete, unbuilt)**

- **Statement.** Until the Rules Service exists, DAP-14 controlled-unit determination falls back to custody class alone (per DAP-Spec §8 dependency table: "Rules Service (rulebook_engine_spec_v1) | Specified, not built | DAP's controlled-unit determination reads the estate's rule books. Until the Rules Service is built, controlled status is determined by custody class alone.").
- **Bounds what W-DAP-STACK can claim at launch.** Approval routing for controlled requests operates on custody class only; entitlement rules per Canon-3 §22.1 are read from the Registries-class store but the runtime Rules Service that administers ceremony changes to those registries is not in force.
- **Owner.** Rules Service build. Blocked on ROC ratification (pending owner ruling).
- **Cross-reference.** Doc-0 Part 3 STATUS AS OF (charter §3.7, first-hand): `G-9 | Rules Service RBM-7/RBM-8 | Spec-closed. Not built.` Two-tier procedure ratified in `rulebook_engine_spec_v1` §RBM-7 (tier one, system rules) and §RBM-8 (tier two, TCB rules); not yet code.

**Risk R-C2 · Reliable time source dependency (Doc-0 G-8 fix)**

- **Statement.** DAP-21 metering defensibility requires a reliable, tamper-resistant time source shared across the system (Doc-0 Attribute 8 §TA-8.1 verbatim, first-hand: "Every audit record's timestamp derives from a reliable, tamper-resistant time source shared across the system — a record whose time field cannot be trusted cannot establish AU-3(b), regardless of how precise the field's format is.").
- **Bounds what W-REGISTRY-FULL-BUILD and W-DAP-STACK can claim.** Both waves write metered, timestamped records; neither meters defensibly until the reliable-time control exists. Metered rows written under a non-reliable time source are still ledgered (P1: refusals recorded on the same terms as successes), but AU-3(b) is not established for them.
- **Owner.** Platform / infra.
- **Cross-reference.** Doc-0 Part 3 STATUS AS OF (charter §3.7, first-hand): `G-8 | Security_Promise_Set_Amendments.docx, Amendment 3 | Spec-closed. Not built.`

These risks are stated at Phase C so no wave close inside the plan claims defensibility it does not have. Each wave's gating tests below cite whichever risk bounds it explicitly; no risk is silently absorbed.

---

## §W-REGISTRY-FULL-BUILD — the full asset inventory

### §1 Canon anchor and gap it closes

`Doc-0 Attribute 3 BA-3.1` (first-hand, Phase B) verbatim:
> "Every principal belongs to a stated class — human role, application, or subsystem acting under its own authority — and carries a mandate whose source can be named."

`Doc-0 Component 4 (Mtafiti) BR-4.1 STATUS` verbatim:
> "**Not Met** — current coverage is estate sources only (Promises #12, #13). See G-3."

`Doc-0 Part 3 STATUS AS OF` (first-hand, Phase B) verbatim:
> `G-3 | dap_backend_spec_v1 DAP-1/DAP-2 (external-party case only) | Partial — general triad formalisation and Mtafiti's full asset-inventory extension remain open.`

`Canon-3 §22` (Four Classes of governed values, Phase B first-hand): every governed value is exactly one of Rails / Rules / Engine settings / Registries, with distinct change velocity and verification method per class.

`Canon-3 §22.1` (Entitlement rules, Phase B first-hand): "The content side is already built: the sensitivity classification Mtafiti assigns during census, specified in Document 4, is exactly the resource attribute this match runs against. No new classification exists; entitlement reads the one already there."

`Canon-7 §35–§40` (Function & Promise Registry, Phase B first-hand): every named function in the platform registers here with the eleven mandatory fields.

**What this wave closes**: G-3's mechanical half — extending Mtafiti's registry scope from estate sources to the full asset class Attribute 3 defines (models, artifacts, receipts, rules), each entry carrying a named owner, with custody class carried as a typed, queryable attribute per BR-1.4 and BR-4.1 rather than a description in prose.

### §2 Scope

Six touchpoints, ordered by dependency:

**CP-R1 · Registry schema — the extended asset class**
- Extend Mtafiti's registry per `Doc-0 BR-4.1` and `BR-4.2`.
- Asset classes covered: estate sources (already Met), models (from Canon-4 §33.2 model registry), artifacts (from Canon-3 §16, trust receipts as governed artefacts), receipts (from Canon-3 §9, ledger rows), rules (from Canon-3 §22 four classes).
- Every entry carries a named owner (Canon-3 §22 taxonomy Owner field).

**CP-R2 · Custody class as a typed, queryable attribute (`Doc-0 BR-1.4`)**
- Custody class is a first-class typed field on every asset record, not prose. Canon-3 §22.1 requires this because entitlement match reads it directly.
- Custody-class enumeration is finite (per `Doc-0 TA-3.1`: "A finite, named list of principal classes, asset classes, and operations exists and can be produced on request").

**CP-R3 · Class enumeration surface (`Doc-0 TA-3.1`, `BR-4.2`)**
- Publish the finite, named class list — principals, assets, operations, custody classes — producible on request. Not a re-derivation from source code.

**CP-R4 · Four-class governance-value taxonomy binding (`Canon-3 §22`)**
- Every governed value on the platform is tagged with its class: Rails (build-time only), Rules (setup+ceremony), Engine settings (versioned deployment), Registries (upload/validate/version).
- The taxonomy binds change velocity + verification method per class; the registry surface must respect it.

**CP-R5 · Function & Promise Registry population (`Canon-7 §35–§40`)**
- Every function this wave lands (writer, reader, class-enumeration surface, taxonomy tagger) registers its F&P row before landing.
- Three standing queries wired: Redundancy, Orphans, Gaps.
- Registry pays rent: F&P Registry itself registers with a rent metric per Canon-7 §40.

**CP-R6 · Ledger-scoped visibility (`Canon-3 §9.2`, `Canon-9 §3 matrix`)**
- Registry writes appear in the Ledger under the canonical writer per the record matrix — Mtafiti for census/registry records — not a new writer.
- Confirms no second writer per Canon-9 §3: "A second writer to any class is a defect on sight."

### §3 Grounding tests (RED before code, per STANDING_ORDERS §3)

Tests-first, mechanical RED. No code lands without a drill receipt on the pre-implementation tree.

- `test_registry_covers_full_asset_class.py` — mechanical: enumerate asset kinds present today, assert models/artifacts/receipts/rules each have at least one record with a named owner. RED against current tree (estate sources only).
- `test_custody_class_is_typed_queryable.py` — mechanical: query the registry for `custody_class` as a typed field on N records; RED if the field is absent or free-text.
- `test_governance_value_classification.py` — mechanical: every governed value on-disk has exactly one of Rails/Rules/Engine settings/Registries as its class tag. RED against untagged values.
- `test_fp_registry_no_orphan.py` — mechanical: every new function this wave introduces has a registered F&P row before it lands. RED if any function lands without one.
- `test_fp_registry_no_gap.py` — mechanical: every journey step Canon-6 enumerates has ≥1 registered function protecting it (Canon-7 §37 "No journey step without enforcement").
- `test_registry_writer_is_mtafiti.py` — mechanical: no second writer to census/registry records; matches Canon-9 §3 matrix row `Census and registry records | Mtafiti | Both authorities; every surface by proof link`.

### §4 Close conditions

- All CP-R1..CP-R6 tests pass double-green byte-match under `BASELINE_GUARD=1`.
- Ratchet floor bumped from 3503 to `3503 + N` (N = count of new invariants); `baseline_failures.json` `counts_at_baseline.passed` and `invariants_enforced_when_baseline_guard_1.passed_floor` update in tandem; ratchet_history entry appended.
- `output_verified_seal` written with `Kind: registry_full_build` (SO §3.1).
- Close report at `notes/W_REGISTRY_FULL_BUILD_close.md` — note: a Phase A file exists at that path (fork banked, dated 2026-09-09); the close artifact for this wave will supersede it with a new dated close, retaining lineage.
- Doc-0 §STATUS AS OF row for G-3 remains "Partial" until the general triad formalisation half also closes (which is a documentary wave, not this build wave); this wave closes the mechanical half.

### §5 Risks this wave carries

- **R-C2 (reliable time source)**: registry writes are timestamped; without R-C2 resolved, AU-3(b) is not established for those timestamps. Documented in wave-honest limits §E of the wave's own grounding brief (STANDING_ORDERS §3).

---

## §W-DAP-STACK — the full DAP stack, DAP-1..30

### §1 Canon anchor and what this wave is

`DAP-Spec §7 Composition Map` (first-hand) verbatim:
> "DAP owns no invariant of its own. Every guarantee it makes is a guarantee of a component it composes, exercised through this surface."

`DAP-Spec §11 Standing` verbatim:
> "DAP is the first instance of a generic Data & Intelligence Acquisition Platform. Nothing in §1–§9 is specific to RMS except the named estate; a second estate owner adopting this platform inherits every requirement here and configures §5's owner-side settings for its own estate."

`Canon-1 §12 S4` (first-hand, Phase B) verbatim: "The data buyer | Intelligence products that can be verified independently before being relied upon — never raw data."

`Canon-3 §22.1` (first-hand, Phase B): entitlement rules are ABAC over Mtafiti's sensitivity classification.

`Canon-7 Part IV §18–§27` (Memory Layer / Plane, first-hand, Phase B): every integration key carries exactly one memory plane, plane isolation is by construction, ledger-reconstructible.

**What this wave is**: the composition wave. DAP-1..30 are requirements per `dap_backend_spec_v1`; every one is a guarantee of a component DAP composes. This wave does not build primitives — it wires primitives into the six DAP crossing profiles.

### §2 Scope, mapped to DAP-Spec requirement IDs

Grouped by DAP-Spec's own §5 back-end services structure:

**Wave 2A · External-party principal + admission (DAP-1..4)**
- DAP-1: external party as organisation-level principal with legal identity, governance posture, terms, trust domain, admission-time mandate.
- DAP-2: party principal with mandate, mark state, behavioural signature under the Watch.
- DAP-3: external-agent admission (autonomous non-human principal).
- DAP-4: slow-play detection — a first-class cumulative-history attack shape.
- **Canon anchors**: Doc-0 Attribute 3 (extends the governed triad); Canon-8 §W9 (declaration baseline); Canon-8 §W11 (task-identity register — D8 unrepresentable).

**Wave 2B · Trust-domain separation + keys (DAP-5, DAP-13)**
- DAP-5: trust-domain boundary; the external party's domain and the estate's domain share no identifier resolution, no store, no credential.
- DAP-13: API keys per party principal, revocable single-act, stated lifetime (R-4), non-transferable, never in any record.
- **Canon anchors**: Doc-0 Attribute 12 (Trust Domain); Canon-3 §16 (Key Custody and Receipts); Canon-3 §13.1 (chokepoint credential-branching rule).

**Wave 2C · The six crossing profiles (DAP-6..11)**
- DAP-6: Browse — aggregates only, no unit contents, not a crossing.
- DAP-7: Connect workspace — chokepoint pull seam; query in, de-identified results out; estate data MUST NOT leave under this operation.
- DAP-8: Processed intelligence — derived output only; source units in receipt not reconstructable from output.
- DAP-9: Fine-tune — compute-to-data only; NO configuration flag permits inverse. Owner ruling anchor.
- DAP-10: Artefact egress — model registry, rights posture stamped, hash recorded, terms cited.
- DAP-11: Raw download — outer-gate crossing (Promise #25), redaction as gate not prompt, per-unit evidence record.
- **Canon anchors**: Canon-3 §12-13 (SyniSense chokepoint); Canon-3 §19-20 (Two Perimeters / Outer Gate five checks); Canon-4 §34-36 (five output forms and provenance-preservation rule); Canon-7 Part III §13-17 (async contract, thin webhook, idempotency, cancellation, versioning, sandbox).

**Wave 2D · Approval + spend (DAP-14..17, DAP-23)**
- DAP-14: controlled requests route to the estate owner's named approving authority; request does not execute while pending.
- DAP-15: approval decisions recorded with identity/decision/reason; unanswered request expires unexecuted, not proceeded-by-default.
- DAP-16: fine-tune and skill-development requests always require approval (artefact egress); raw download always requires approval for controlled.
- DAP-17: standing approval for named party + scope + window — revocable single-act; MUST NOT cover controlled units unless it names them explicitly.
- DAP-23: spend against a party's ceiling evaluated before execution; ceiling breach routes to spend request, not silent fail or over-budget execute.
- **Canon anchors**: Canon-3 §22.1 (entitlement rules as the governing rule); Canon-3 §24 (change ceremony for standing approvals as governed rules); Doc-0 Attribute 9 (Authority & Change Control).
- **Carries R-C1 (Rules Service)**: DAP-14 controlled-unit determination falls back to custody class alone at launch (per DAP-Spec §8 dependency).

**Wave 2E · Extraction commission + assistance chat (DAP-18..20)**
- DAP-18: every extraction is a commissioned job with a frozen objective; objective freeze applies at commission.
- DAP-19: every job routes to the engine that governs its operation per §4 and MUST NOT execute through any other path.
- DAP-20: assistance chat MAY help shape / identify scope / understand terms before commission. It MUST NOT approve, widen scope after commission, or decide any gate.
- **Canon anchors**: Canon-3 §6 (Admit — freeze is atomic, artifact is immutable for the run); Doc-0 BR-3.1 (objective-freeze shared mechanism); Canon-5 §14-16 (Extraction Console shaping wizard pattern).

**Wave 2F · Metering + receipts (DAP-21..24)**
- DAP-21: every §4 operation emits metered event with operation/access/quantity/terms/party/timestamp. Written before result returned.
- DAP-22: terms attach at three levels, most-specific-first; every receipt cites terms identifier applied.
- DAP-23: (covered in Wave 2D above — spend ceiling).
- DAP-24: cumulative extraction history per party is a first-class queryable record; retained for full admission.
- **Canon anchors**: Doc-0 Attribute 8 (Audit Record — AU-3 six elements); Canon-3 §16 (trust receipts).
- **Carries R-C2 (reliable time source)**: DAP-21 metering defensibility requires the time control; not defensible without it.

**Wave 2G · Owner configuration (DAP-25..27)**
- DAP-25: estate owner configures per custody class + per operation whether unavailable / available on approval / available under standing terms. Default: unavailable.
- DAP-26: owner sets default terms per custody class, per-party overrides, per-party ceilings. Changes take effect through Rules Service ceremony; MUST NOT retroactively alter receipts already issued.
- DAP-27: owner can suspend party — halts every in-flight and future operation in one act. In-flight jobs stop and are recorded as stopped, not silently completed.
- **Canon anchors**: Canon-3 §22 (four classes taxonomy); Canon-3 §24 (change ceremony); Canon-3 §27 (Authorized Deletion; suspension is a related governance act).
- **Carries R-C1 (Rules Service)**: DAP-26 rules-service ceremony not in force until R-C1 resolved.

**Wave 2H · Failure posture (DAP-28..30)**
- DAP-28: every DAP gate fails closed.
- DAP-29: metered event that cannot be written to the Ledger refuses the operation it meters. Unrecorded extraction is not permitted to have happened.
- DAP-30: browse degrades rather than refuses (stale/partially unavailable census returns what it has, marked stale with as-of time).
- **Canon anchors**: Doc-0 Attribute 11 (Failure Posture — fail-closed for TCB); Canon-1 §4.1 (fail-closed custody); Canon-4 §4.1 (unmeasured is a first-class value); charter P6, P9.

### §3 Grounding tests (RED before code)

One RED test per DAP-N requirement, plus the ten Build Acceptance A1..A10 from DAP-Spec §9. Highlights:

- `test_dap_9_no_inverse_configuration.py` — mechanical: attempt, by every available configuration, to move estate data to compute outside the perimeter for a fine-tune job. RED if any configuration permits it. (DAP-Spec A1.)
- `test_dap_6_browse_boundary.py` — mechanical: every browse path returns aggregates only. No path yields unit contents or a sample. (DAP-Spec A2.)
- `test_dap_14_approval_gate_fail_closed.py` — mechanical: unreachable approval service refuses the operation and records the refusal, never proceeds by default. (DAP-Spec A3.)
- `test_dap_21_metering_completeness.py` — mechanical: one job of each of the six operations produces exactly one metered event with all required fields, each written before result is returned. (DAP-Spec A4.)
- `test_dap_4_slow_play_detection.py` — mechanical: scripted sequence of individually-permitted requests exceeding aggregate entitlement is detected against cumulative history and raised, not evaluated per request. (DAP-Spec A5.)
- `test_dap_18_objective_freeze.py` — mechanical: assistance chat cannot widen a commissioned job's scope. Wider scope is a new job. (DAP-Spec A6.)
- `test_dap_27_suspension_stops_inflight.py` — mechanical: party suspension halts every in-flight job; each recorded as stopped. (DAP-Spec A7.)
- `test_dap_5_trust_domain_no_cross_resolution.py` — mechanical: estate unit identifier does not resolve from party's domain outside a permitted operation. Attempt recorded. (DAP-Spec A8.)
- `test_dap_13_key_hygiene.py` — mechanical: no key material in any record, receipts, or metered events. (DAP-Spec A9.)
- `test_dap_10_artefact_egress.py` — mechanical: fine-tune on controlled units produces weights carrying rights posture, hash, derivation, and terms cited. (DAP-Spec A10.)

### §4 Close conditions

- All wave gates (2A..2H) pass their sub-gates; the ten A1..A10 all pass double-green byte-match under `BASELINE_GUARD=1`.
- Ratchet floor bumped per wave; ratchet_history appended.
- `output_verified_seal` written per sub-wave with `Kind: dap_stack_{2A..2H}`.
- Close reports for each sub-wave at `notes/W_DAP_STACK_{2A..2H}_close.md`.
- Wave-close roll-up in DECISION-POINT format per STANDING_ORDERS §2 (END-OF-WAVE format).

### §5 Risks this wave carries

- **R-C1 (Rules Service)**: at launch, DAP-14 falls back to custody class alone; DAP-26 rule ceremony not in force. Both stated in the wave grounding brief as wave-honest limits.
- **R-C2 (reliable time source)**: DAP-21 metered timestamps are not defensible under AU-3(b) until R-C2 resolved. Stated in wave-honest limits.

### §6 Sequencing note (owner Amendment 2 — no plan risks from Phase A absences)

Phase A's declared canon absences are closed in Phase B. This plan does NOT carry them as explicit plan risks. The only risks Phase C carries are R-C1 and R-C2 above, both named-owner-attached.

---

## §W-SOLVA-V2-LIFT — standalone reasoning component

### §1 Canon anchor and why this is a standalone wave

Owner Amendment 1 (Phase C, this session, verbatim): "W-SOLVA-V2-LIFT — as a STANDALONE component in this same wave, NOT a sub-component of Registry or DAP (owner's explicit instruction: lift the donor pool from Akki-Executive-Core as a standalone reasoning component)."

`Canon-4 §19` (Solva) verbatim:
> "Solva judges whether reasoning is sound, whether preservation is sufficient, and whether an output asserts within its defensibility. It is the one engine that genuinely reasons — the direction governor is deterministic, targeting's learning is walled from eligibility, discovery's inference only detects. Solva is where actual judgement lives in the platform, and it never extracts and never reaches into the operator primitives that do: it issues operations, interprets results, and governs depth."

`Canon-4 §20-§27` (The Two Faculties + Assertion Boundary) — the seam that makes reasoning safe to hold.

`Canon-7 §41–§46` (Critic Seam, Phase B first-hand) — three tiers; Tier 2 the critic pass is an independent model instance reviewing each artefact.

**What this wave is**: lift the reasoning donor pool from `repos/Akki-Executive-Core` (fork context: "lift the donor pool from Akki-Executive-Core as a standalone reasoning component") into a reasoning core that instantiates Solva's two-faculty seam. Not a Registry sub-wave, not a DAP sub-wave — a peer engine wave, sequenced by dependency only.

### §2 Scope

**CP-S1 · Two-faculty seam, import-asserted (Canon-4 §20)**
- Reasoning faculty and assertion boundary as two modules with a one-way import boundary.
- Doc-0 BR-2.1 verbatim (first-hand): "The two-faculty seam is enforced by an import assertion, not a coding convention — one faculty cannot invoke the other's authority even inadvertently, because the import itself is the enforcement point."

**CP-S2 · Assertion boundary function signature (Canon-4 §23.1)**
- Class-computation function takes load-bearing units and nothing else. No confidence parameter, no reasoning strength parameter, no evidence-weight parameter.
- Canon-4 §23.1 verbatim: "The signature is the guard, and a signature assertion in the test suite is what keeps it one."
- Build order: assertion boundary FIRST, with its parameterless signature, BEFORE the reasoning faculty is bound to it (Canon-4 §23.1).

**CP-S3 · Load-bearing set function returns unit references only (Canon-4 §22)**
- Function that identifies load-bearing units returns unit refs — carries NO class decision.
- Canon-4 §22 verbatim: "A load-bearing function that returned a class would have collapsed the two faculties into one — Solva chooses the units; it does not choose what those units imply."

**CP-S4 · Refusal is actionable (Canon-4 §24)**
- Refusal below-floor states what was asked, the supported class, and what would raise it.
- Offers exactly three actions: accept the result as a recorded statement, narrow the objective, or lower the standard.
- Canon-4 §24 verbatim: "Offering anything else would be offering something the system cannot actually deliver."

**CP-S5 · Trace mandatory from first commit (Canon-4 §26)**
- Every extraction-time judgement produces a trace: reasoning path across stages, load-bearing units, computed class at boundary, conclusion itself.
- Canon-4 §26 verbatim: "It is the auditability that justifies letting a component reason at all, and it exists from the first commit."

**CP-S6 · Intent audit — declared vs. demonstrated (Canon-4 §21.1)**
- Solva opens with intent-audit record: situation class declared vs situation class demonstrated by conduct.
- Divergence tracked as session unfolds; emissions the Watch reads under Canon-8.

**CP-S7 · Critic Seam Tier 2 binding (Canon-7 §44)**
- Solva's output submits to Tier 2 asynchronous critic pass — independent model instance, never sharing worker's conversation, context = artefact + canon + authorising instrument + rubric.
- Canon-7 §44.1 verbatim: "A critic reading the author's rationale inherits the author's frame, which is the blind-spot-sharing failure this whole design exists to avoid."
- Critic findings: classed, cited, never blocking, never editing.

**CP-S8 · Donor pool lift from Akki-Executive-Core**
- Case-agnostic lift only. Any executive-domain tokens (executive briefs, executive dashboards, executive persona language) are `[framing, not canon]` in this platform context and are stripped — Canon-1 §4.6 doctrine: extension, not proliferation.
- What lifts: reasoning primitives (candidate weighing, tension surfacing per Canon-4 §21, reflection producing load-bearing set), NOT domain shells.

### §3 Grounding tests (RED before code)

- `test_solva_two_faculty_import_boundary.py` — mechanical: reasoning module does not import assertion module's class computation; assertion module does not import reasoning faculty's confidence field. Both fail-to-compile if violated.
- `test_solva_assertion_boundary_signature.py` — mechanical: class-computation function has exactly one parameter type: load-bearing unit references. No confidence/strength/weight parameter present in signature.
- `test_solva_load_bearing_returns_refs_only.py` — mechanical: load-bearing function return type is `Sequence[UnitRef]`, no class field.
- `test_solva_refusal_offers_three_actions.py` — mechanical: below-floor refusal envelope carries exactly `accept_as_stated`, `narrow_objective`, `lower_standard`.
- `test_solva_trace_from_first_commit.py` — mechanical: any Solva session produces a trace file whose contents parse under the trace schema; trace-less session is a defect.
- `test_solva_intent_audit_captured.py` — mechanical: intent audit record present per session with declared/demonstrated fields distinct.
- `test_solva_critic_seam_context_isolation.py` — mechanical: critic invocation carries only artefact+canon+authorising+rubric; NEVER the worker's own reasoning drafts.
- `test_solva_donor_lift_is_case_agnostic.py` — mechanical: negative-scan over lifted modules for executive-domain tokens; RED if any survive.

### §4 Close conditions

- CP-S1..CP-S8 pass double-green byte-match; ratchet bumped.
- `output_verified_seal` per CP with `Kind: solva_v2_lift_{S1..S8}`.
- Close report at `notes/W_SOLVA_V2_LIFT_close.md`.
- Standing invariant: any subsequent Solva change re-runs CP-S1..CP-S8 as regression gate (Canon-4 §26: trace exists from first commit; the invariant does not soften after the first commit).

### §5 Risks this wave carries

- **R-C2 (reliable time source)**: Solva trace entries carry timestamps; without R-C2 resolved, AU-3(b) is not established for trace entries. Documented in wave-honest limits.
- **No R-C1 dependency**: Solva does not require Rules Service — it reads governed matrices and floors through opaque handles (Canon-4 §23 verbatim: "The floor and the class verdict are read-only. Solva reads them; it never sets or relaxes them").

---

## §D. Sequencing map (dependency only, not schedule)

Sequenced by what each wave requires from another. **Phases can proceed in parallel where their dependency arrow is not present** — this plan proposes no schedule (STANDING_ORDERS §6 forbids invented sequencing; owner sequences waves at ruling time).

```
                    W1c primitives (banked, ratchet 3503)
                            |
      +---------------------+---------------------+
      |                     |                     |
  W-REGISTRY-FULL-BUILD  W-SOLVA-V2-LIFT     W-DAP-STACK (2A..2H)
      |                     |                     |
      |                     |                     |
      +----------+----------+                     |
                 |                                |
                 +---> Wave 2A..2B relies on Registry CP-R1..R3
                       Wave 2D..2E relies on Solva CP-S1..S5
                       (Solva handles reasoning under DAP's processed-intelligence
                        crossing DAP-8, Canon-4 §36 Composed conclusion form)
```

- **W-REGISTRY-FULL-BUILD** depends only on W1c primitives (banked). Starts as soon as owner rules.
- **W-SOLVA-V2-LIFT** depends only on W1c primitives (banked). Independent of W-REGISTRY (does not require Registry's asset-class extension to instantiate its two-faculty seam).
- **W-DAP-STACK 2A..2B** depend on Registry CP-R1..R3 (external-party principal + trust domain + typed custody class field).
- **W-DAP-STACK 2C..2H** depend on Solva CP-S1..S5 for DAP-8 (Processed intelligence), because that crossing is bounded by Solva's assertion floor (DAP-Spec §7 Composition Map: "Solva — reasoning | Processed intelligence, held to the assertion floor").
- **Bastion / additional-data-system as future SourceConnector** (per owner directive this session): the retrieved handle `${bastion.jump_server_radio_system}` is banked at 0600, non-echoed. **Not load-bearing for W-REGISTRY / W-DAP / W-SOLVA at this planning stage**; noted here only so a future SourceConnector touchpoint has its handle already available. Egress against on-prem may run only in the window **11:00–05:00** (owner ruling this session, verbatim: "any egress against the on-prem environment / additional data system is permitted ONLY within the window 11:00–05:00 (avoid interrupting daily operation). Operations that do not affect day-to-day system function may run anytime."). Recorded here as a STANDING OPERATIONAL CONSTRAINT.

---

## §E. Two risks, restated for the wave-close roll-up

For the END-OF-WAVE report (STANDING_ORDERS §2, plain-language format) that each wave close produces, the two named dependency risks below MUST appear in "Discoveries not envisioned at planning" and/or "Recommendations to make the experience better":

**R-C1 · Rules Service (spec-complete, unbuilt)**
- Owner: Rules Service build; blocked on ROC ratification (pending owner ruling).
- Impact this wave: DAP-14 controlled-unit determination falls back to custody class alone at launch (per DAP-Spec §8 dependency table verbatim); DAP-26 rule ceremony not in force.
- Cross-reference: Doc-0 §STATUS AS OF row for G-9 (charter §3.7 first-hand): `G-9 | Rules Service RBM-7/RBM-8 | Spec-closed. Not built.`

**R-C2 · Reliable time source (Doc-0 G-8 fix)**
- Owner: platform / infra.
- Impact this wave: W-REGISTRY and W-DAP-STACK both write metered, timestamped records; neither meters defensibly under AU-3(b) until this control exists.
- Cross-reference: Doc-0 §STATUS AS OF row for G-8 (charter §3.7 first-hand): `G-8 | Security_Promise_Set_Amendments.docx, Amendment 3 | Spec-closed. Not built.`

---

## §F. Commit protocol for each wave (STANDING_ORDERS §3, restated)

- **Commit A (code)** — `/app/assessment_workspace/repos/Extraction-Akki/` on branch `programme/track-a`. Never push.
- **Commit B (state)** — `/app/assessment_workspace/` on branch `master`. Every wave close writes:
  - `notes/W_{WAVE}_grounding_brief.md` (opens the wave, with verbatim owner quote in §A and wave-honest-limits in §E per STANDING_ORDERS §3)
  - `notes/W_{WAVE}_close.md` (closes the wave, with double-green receipts banked)
  - `phase0/drill_receipts/{RED}.txt` (RED receipt)
  - `phase0/drill_receipts/{GREEN_1}.txt` and `phase0/drill_receipts/{GREEN_2}.txt` (double-green)
  - `repos/Extraction-Akki/backend/tests/invariants/baseline_failures.json` (ratchet bump + ratchet_history entry)
  - `STATE/DECISIONS.md` (verbatim owner ruling for the wave, if any)
- **Never push.** Local commits are the record.

---

## §G. What this plan does not decide

Owner rulings this plan does NOT preempt:

- Which wave opens first (STANDING_ORDERS §3 discipline: no invented sequencing). Owner sequences at ruling time.
- R-C1 / R-C2 resolution paths (deferred to Rules Service ratification and platform/infra ruling respectively).
- Whether the bastion / additional-data-system becomes a live SourceConnector at any point in this plan (currently: banked handle only, not load-bearing here).
- W2 mount blockers (Path A/B/C storage, NAS network path, 3-station confirm). W2 remains hard-stopped per charter §4.3 until owner rules.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
