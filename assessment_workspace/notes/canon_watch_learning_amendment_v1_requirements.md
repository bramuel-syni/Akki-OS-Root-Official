READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_watch_learning_amendment_v1_requirements.md

**Filed:** 2026-09-13.
**Source:** `canon/drops/20260913/owner_drop_2/Watch_Learning_Amendment_v1.docx` · sha256 `eb8a0bec26a519b3cad97d412514775c6560b5553079d8e5802dfe8b2f69a9f1` · registered in `canon/drops/20260913/MANIFEST.md`.
**Applies to (verbatim, per amendment §1 table):** Doc 3 (A2 verdict interface enriched + new A5.19–A5.22) · `rulebook_engine_spec_v1` (new RBM-23) · `dap_backend_spec_v1` (DAP-32 extended) · Doc 20 (new A20.16) · `agent_containment_spec_v1` (new AC-15..AC-18) · Security Assurance Promise Set (S-7 closed, S-28 + S-29 new).

## §0 · Summary the owner asked for

- **S-7 status change:** *"Absent → gap"* → **"Absent → new (spec-closed, 13 Sep 2026)"** — CLOSED AT SPEC LEVEL by L-2 (A5.20 + RBM-23) and L-4 (A5.22 research loop).  Not built.  R-15 (initial library seed) + R-16 (ratifying role + research-queue cadence) are new OPEN rulings.
- **S-28 (new):** *"The system will never act on a verdict it cannot evidence — every Watch action carries a certificate a human can read, and every behaviour it learns to recognise entered its vocabulary through ceremony, not through silent training."*
- **S-29 (new):** *"The system will admit no new class of action into the world without ceremony on the record — every action names the admission it acts under, and no learner ratifies its own."*  Open ruling R-17 (class granularity, initial register).
- **New open rulings:** R-15, R-16, R-17.

## §1 · Requirements list (verbatim, numbered)

### L-1 · The Certificate on the Verdict

**R-WLA-1 · A5.19 verdict certificate**
> "Every verdict Grey Mirror passes to Mkono MUST carry a certificate: the set of observed data points that satisfy a ratified certificate requirement (A5.20) for the behaviour asserted, with the requirement's ID and references to the observation records."

**Schema:** `certificate = {requirement_id, data_points[], observation_refs[]}`.  Runtime check is a deterministic satisfaction test — a lookup, not reasoning.  Seam sits at the verdict interface.

Derivation: Doc 3 A2 · A5.2 (no confidence parameter) · Doc 4 A2/A5.5 (assertion floor) · CP-S2 · EU AI Act Article 14(c).

### L-2 · Certificate Requirements as a Rule Class (S-7 CLOSER)

**R-WLA-2 · A5.20 deterministic certificate gate**
> "A certificate requirement is a deterministic gate: the named set of data points that must be observed for a verdict to assert a named behaviour.  Requirements are formed from data points collected in this environment — live, or in the mirage (A5.21) — and are formed under [ceremony]."

**R-WLA-3 · RBM-23 certificate-requirement rule class**
> "Certificate requirements are a named rule class of tier system-TCB — they determine Mkono's inputs.  Each is authored with RBM-1's full field set, enters force only through RBM-8's ceremony (the platform's slowest countdown; an external witness holding no credentials over the Watch)."

**Impact:** rule class RBM-23 is a NEW rule-class registered in the Rule Registry (M2 W-M2-SW1 scope).  Tier is `system_tcb` — 7-day countdown.  `[framing, not canon]` — the current M2-SW1 registry accepts arbitrary rule ids; RBM-23 rows are additively-compatible.

Derivation: A5.8 (floor never learns) · A5.12 (profile protection) · RBM-4 · RBM-8 · `rule_criteria_spec_v1` (EXTENSION-class) · BR-7.3.

### L-3 · The Mirage as Certificate Ground

**R-WLA-4 · A5.21 mirage as certificate ground**
> "The mirage is the certificate ground: a controlled environment in which a behaviour with a ratified requirement can be provoked and its data points collected without exposure to real estate data.  Data points collected in the mirage are admissible for requirement formation."

**R-WLA-5 · DAP-32+ admission battery extended per certificate library**
> "The admission battery includes, for every ratified certificate requirement applicable to entering models, the provocation scenario that would produce its data points.  An entering model that produces a certified behaviour fails admission.  The battery grows with the library."

**R-WLA-6 · AC-15 pre-scope certificate ground**
> "Before an agent receives any scope beyond admission, it runs the certificate ground for the four ceilings (AC-1 a–d) and every applicable ratified requirement.  A certified failure withholds scope."

Derivation: Doc 3 C1 · DAP-32 · AC-1 · AC-2 · pre-deployment capability-elicitation practice.

### L-4 · The Research Loop

**R-WLA-7 · A5.22 unsure-case queue**
> "Every unsure case — a verdict with no applicable requirement, or an action routed under AC-4 — enters the research queue with its full observation record.  The loop has three roles and one order: CIF proposes what the pattern means — a candidate requirement, or a candidate benign pattern; Solva grounds the proposal; a human ratifies."

**R-WLA-8 · AC-16 containment feeds research queue**
> "The containment environment feeds AC-4 and AC-6 unsure cases to the research queue.  A ratified outcome re-classes prior identical cases in the record — the classification, never the actions taken, which stand as taken."

**Mechanism note:** research queue keyed to Ledger refs · CIF proposal → Solva grounding → ceremony · benign-pattern registry alongside the requirement library.  LIM-1 stands as written.

Derivation: BR-9.1 · BR-9.2 (CIF's single-experiment principle) · Doc 4 A2/A5.5 · Solva V2 CP-S1..CP-S8 · AC-4 · AC-6 · RBM-8.

### L-5 · Capability Admission (certify EXERCISE, not learning)

**R-WLA-9 · A20.16 capability-class register on every artefact**
> "Every registered artefact carries a capability-class register: the enumerated set of action and output classes it is admitted to exercise.  The register is seeded at admission with the minimum its stated purpose requires (AC-2's narrow start), grows only through RBM-8's ceremony."

**R-WLA-10 · AC-17 per-action citation + first-exercise foundation floor**
> "Every action or output an agent produces MUST cite the admitted capability class it exercises, carrying a certificate on A5.19's schema evidencing that the action is within the class's admitted conditions.  An action citing no admitted class is a first exercise: it is handled at the reversible-only foundation floor; observation records feed the research queue."

**R-WLA-11 · AC-18 learner may propose, never ratify**
> "A model or agent MAY propose admission of a capability class for itself.  It MUST NOT ratify one.  A proposal enters the research loop (A5.22): Solva grounds it, a human ratifies through RBM-8.  No path exists by which a learner admits its own capability.  AC-1's four ceilings are not admissible under any ceremony."

Derivation: DAP-37 (new hash = new artefact) · BR-9.2 · AC-1..AC-3 · A5.15 · A5.19 · A5.22 · RBM-2 · Instrumental convergence (Omohundro 2008, Bostrom 2012).

## §2 · Placement in standing enumerations (verbatim from amendment Table 2)

**R-WLA-12 · TCB placement**
> "IN: the certificate gate at the verdict interface — deterministic; its failure falsifies S-28.  The certificate library is TCB-tier configuration, on the same footing as Mkono's policy tables.  Grey Mirror stays OUT, as before."

**R-WLA-13 · Determinism inventory**
> "Certificate gate: Deterministic.  Research loop: CIF proposes (Learned); Solva's grounding seam decides (Deterministic); a human ratifies.  Article 14(c) verdict updated per S-28."

**R-WLA-14 · Failure posture**
> "Certificate check cannot complete (library unreadable; requirement unresolvable) → fail-closed for certified actions: only the foundation floor remains — the reversible ladder, and severance from A5.2's signals alone.  Preserved: the verdict, the failed-check event is recorded."

**R-WLA-15 · Capability admission TCB placement**
> "Capability admission (L-5): tcb_enumeration_v1: the capability register is TCB-tier configuration; the per-action citation check is IN — a deterministic lookup.  determinism_inventory_v1: the learner proposes (Learned); Solva's seam grounds (Deterministic); a human ratifies."

**R-WLA-16 · Master Requirements Registry addition**
> "A5.19–A5.22, RBM-23, A20.16, AC-15–AC-18, S-28, S-29 at next refresh."

## §3 · Rulings opened by this amendment (open, owner-input required)

**R-WLA-17 · R-15 — initial certificate library seed**
> "Recommended: seed it from behaviours canon already names — DAP-32's canary-touch and trigger classes, and the four AC-1 ceilings (self-replication, resource acquisition, credential escalation, oversight tampering) — each entering through RBM-8."

**R-WLA-18 · R-16 — ratifying role + research-queue cadence**
> "Recommended: the Watch's existing external witness (C3) as the witness role, per the Rules Service's own R-3 recommendation; the ratifier is a named role — owner input required."

**R-WLA-19 · R-17 — capability-class granularity + initial register**
> "Recommended: seed a deployment's register from the action vocabulary and tool surface it already declares at admission — one class per tool or output type — and never define a class finer than a seam can enforce."

## §4 · S-7 determination (owner-relevant, per side-directive)

**S-7 gap is CLOSED at spec level as of 2026-09-13.**  Evidence:

1. Watch_Learning_Amendment_v1 §1 table row: *"S-7 | The system will learn from every attack it defeats. | Gap → spec-closed. Mechanism: L-2 (the requirement library, under ceremony) and L-4 (the research loop). Not built."*
2. Security_Assurance_Promise_Set v3 (sha256 `51d52ebd...`) row S-7 col `Implementation Status`: **"Absent → new (spec-closed, 13 Sep 2026)"** (was: "Absent → gap" in v2 `72a4e762...`).
3. Security_Assurance_Promise_Set v3 row S-7 col `Bound / Ruling`: **"Closed by Watch Learning Amendment L-2, L-4.  R-15 (initial library) and R-16 (ratifier, cadence) open."**

**Impact on coverage:** S-7 moves from spec-gap → chartered requirement.  Owner-relevant scope change.  Coverage count remains 27 chartered promises with S-7 now on the chartered side + 2 new (S-28, S-29) for a total of 29 chartered promises.

## §5 · Cross-reference to Grey-Mirror requirements

Folded into `notes/canon_grey_mirror_requirements.md` §3 as R-GM-10 (certificate on verdict), R-GM-11 (mirage as certificate ground), R-GM-12 (certificate check fail-closed).

## §6 · Existing-wave home mapping (owner constraint: no new waves / no plan change)

Every requirement in this file is filed INTO the existing wave that already owns it per `MILESTONE_PROMISE_BINDING_20260913.md`.  No new waves; no resequencing.  `[flag]` marks a requirement whose home wave is already CLOSED — surfaced for owner visibility, not reopened.

| ID | Requirement | Existing home wave | Wave status | Notes |
|---|---|---|---|---|
| R-WLA-1  | L-1 · A5.19 verdict certificate schema | **W-WATCH-STACK** (M3 · Wave C · 62 rows) | Not opened | Rides the existing verdict-interface row (Doc-3 A2 enriched, not replaced) |
| R-WLA-2  | L-2 · A5.20 deterministic certificate gate | **W-WATCH-STACK** (M3) | Not opened | Same row as R-WLA-1; deterministic-lookup mechanism |
| R-WLA-3  | L-2 · RBM-23 certificate-requirement rule class | **W-M2-SW1 W-RULE-REGISTRY-BOOTSTRAP** + **W-M2-SW2 W-RULES-SERVICE-CEREMONY** | **CLOSED** (this session) | `[flag]` — RBM-23 as a NAMED rule class is a NEW rule class the registry accepts additively.  Generic ceremony (SW2) already handles `system_tcb` tier for RBM-8.  Filing RBM-23 into the registry itself lands INSIDE W-M2-SW4 W-286-RULE-ENUMERATION-CLASSIFY (still to open). |
| R-WLA-4  | L-3 · A5.21 mirage as certificate ground | **W-WATCH-STACK** (M3 · mirage subsystem) | Not opened | Extends the existing mirage row |
| R-WLA-5  | L-3 · DAP-32+ per-requirement provocation | **W-DAP-STACK 2H** (M1 · component boundary + composition close) | **CLOSED** | `[flag]` — DAP-32+ declared-dependency marker on SFP-8 already landed at 2H close.  L-3's provocation-scenario extension is an ADDITION on top of a closed wave.  Owner: whether to fold into a subsequent DAP-STACK sub-wave or leave as a documentary extension is a scope question. |
| R-WLA-6  | L-3 · AC-15 pre-scope certificate ground | **W-AGENT-CONTAINMENT** (M3 · AC-1..AC-12) | Not opened | AC-15 is a NEW AC row.  `[framing, not canon]` — owner-constraint no new waves means AC-15 rides W-AGENT-CONTAINMENT even though the wave was defined for AC-1..AC-12; the wave's Doc-3-anchored scope naturally extends when new AC rows are added to Doc-3. |
| R-WLA-7  | L-4 · A5.22 unsure-case research queue | **W-WATCH-STACK** (M3) | Not opened | Extends the existing S-13 detection-vs-decide seam (Macho/Mkono verdict handoff) |
| R-WLA-8  | L-4 · AC-16 containment feeds research queue | **W-AGENT-CONTAINMENT** (M3) | Not opened | New AC row (see R-WLA-6 note) |
| R-WLA-9  | L-5 · A20.16 capability-class register | **W-WATCH-STACK** (M3 · Doc-20 parallel to Doc-3) | Not opened | A20 is Doc-20 ownership within Watch-adjacent scope |
| R-WLA-10 | L-5 · AC-17 per-action citation + first-exercise floor | **W-AGENT-CONTAINMENT** (M3) | Not opened | New AC row (see R-WLA-6 note) |
| R-WLA-11 | L-5 · AC-18 learner may propose, never ratify | **W-AGENT-CONTAINMENT** (M3) | Not opened | New AC row |
| R-WLA-12 | TCB placement (certificate gate IN · Grey Mirror OUT) | **W-WATCH-STACK** (M3 · Doc-3 A2 seam) | Not opened | Doc-3 A2 seam · tcb_enumeration_v1 update at next refresh |
| R-WLA-13 | Determinism inventory (certificate gate Deterministic) | **W-WATCH-STACK** (M3) | Not opened | determinism_inventory_v1 update at next refresh |
| R-WLA-14 | failure_posture_v1 (fail-closed for certified actions) | **W-WATCH-STACK** (M3) | Not opened | failure_posture_v1 update at next refresh |
| R-WLA-15 | L-5 · capability admission TCB placement | **W-AGENT-CONTAINMENT** (M3) + **W-WATCH-STACK** (M3) | Not opened | Cross-wave rider |
| R-WLA-16 | Master Requirements Registry addition | Documentary; no wave | — | Registry refresh at next Doc-drop cycle |
| R-WLA-17 | R-15 initial certificate library seed | Owner-input ruling (goes into `RULING_LEDGER.md`) | — | Open — production close awaits owner input |
| R-WLA-18 | R-16 ratifier role + research cadence | Owner-input ruling | — | Open |
| R-WLA-19 | R-17 capability-class granularity | Owner-input ruling | — | Open |

## §7 · Flags surfaced (do NOT reopen; owner-visible)

- **`[flag]` W-DAP-STACK 2H is CLOSED** but L-3's DAP-32+ extension (per-requirement provocation scenarios) sits inside 2H's scope.  This is a documentary extension of an already-banked wave.  Owner: rule whether to (a) fold as extension-of-close in a note only, or (b) open a small documentary-only follow-on close-note against 2H's evidence file.
- **`[flag]` W-M2-SW1 + W-M2-SW2 are CLOSED** and already accept RBM-23 as a NEW rule id additively — no re-work needed.  RBM-23 rows themselves will be filed at W-M2-SW4 W-286-RULE-ENUMERATION-CLASSIFY.
- **`[flag]` W-AGENT-CONTAINMENT scope was defined for AC-1..AC-12**; four new AC rows (AC-15..AC-18) land INSIDE that same wave when it opens.  No new wave.

## §8 · M2-in-flight load-bearing check

None of L-1..L-5 invalidate an already-landed or in-flight M2 sub-wave.  All impacts are ADDITIVE.  M2 continues unchanged.

## §8 · What this amendment does NOT do (verbatim from amendment tail)

> "What this amendment does not do: it does not make Grey Mirror deterministic — it stays learned, and stays out of the TCB.  It does not let a certificate unlock severance — A5.2's registry alone does that, unchanged.  It does not claim to read a behaviour it has never seen.  It does not..."

Preserved: Grey Mirror stays learned · not TCB · severance still unlocks only from A5.2's registry · a behaviour never seen has no certificate and falls back to foundation-floor handling.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
