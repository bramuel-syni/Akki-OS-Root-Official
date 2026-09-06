# Canon Document 0 · Line-by-Line Requirement Extraction

**Source:** `canon/drops/20260907/raw/doc0_governance_architecture.docx` (sha256 `4fe658f2…`)  
**Extracted text:** `canon/drops/20260907/extracted/text/doc0_governance_architecture.txt`  
**Discipline:** every requirement carries a verbatim quote and a section citation. Absence is a finding (marked ⚠).

## §A · Part 1 — The 12 Governance Attributes

Each attribute has a Definition, Governing Standard, Behavioural Specification (BA-n.1..n.3), and Technical Specification (TA-n.1..n.3). Dependency stack: 1→2→3→4→5→6→7,8; 9 depends on 4; 10 depends on 1,2; 11 depends on 5,6; 12 depends on 1-9.

### Attribute 1 · Trusted Computing Base
Definition: "The totality of mechanisms — code, configuration, and process — whose correct operation the system's guarantees depend on." (Doc 0 §1)  
Standard: TCSEC (DoD 5200.28-STD, 1985), §3.2 (B2) and §3.3 (B3). [V]

- **BA-1.1** "TCB membership is decided by a stated, applied test, not by convenience or by which team owns a component. This document proposes: a component is in the TCB if and only if it is deterministic and its failure would falsify a guarantee this document or a document it governs makes." (Doc 0 §1 BA-1.1)
- **BA-1.2** "TCB membership is reviewed under the same authority and change-control discipline as any governed control (Attribute 9), and a component's addition to or removal from the TCB is itself a recorded event." (Doc 0 §1 BA-1.2)
- **BA-1.3** "The TCB is enumerable on request — a named, current list exists, not an inference from doctrine." (Doc 0 §1 BA-1.3)
- **TA-1.1** "No component outside the TCB can modify a component inside it. This is the isolation property…" (Doc 0 §1 TA-1.1)
- **TA-1.2** "The TCB is minimised by design: a learned or non-protection-critical component is excluded even where it is operationally central…" (Doc 0 §1 TA-1.2)
- **TA-1.3** "Every interface the TCB exposes to components outside it is declared and enumerated…" (Doc 0 §1 TA-1.3)

### Attribute 2 · Subsystem
Standard: ISO/IEC/IEEE 42010 cl. 5 [P]; Common Criteria ADV_TDS + ADV_FSP [K].
- **BA-2.1** "For every outcome the system guarantees, exactly one subsystem can be named as accountable for it." (Doc 0 §2 BA-2.1)
- **BA-2.2** "A subsystem's classification — whether it enforces, merely supports, or is non-interfering with respect to governance — is stated, not left to be inferred…" (Doc 0 §2 BA-2.2)
- **BA-2.3** "A subsystem composed of other subsystems' outputs, with no outcome of its own, is not a subsystem; it is a composite…" (Doc 0 §2 BA-2.3)
- **TA-2.1** "A subsystem's interface is declared, and every access to it from outside originates through that interface — there is no side channel…" (Doc 0 §2 TA-2.1)
- **TA-2.2** "A subsystem's internal state and logic are not readable or alterable by another subsystem except through the declared interface's own operations." (Doc 0 §2 TA-2.2)
- **TA-2.3** "A subsystem's interfaces are enumerated in a form that could be checked mechanically against what actually accepts calls at runtime…" (Doc 0 §2 TA-2.3)

### Attribute 3 · Governed Triad — Principal · Asset · Operation
Standard: Common Criteria FDP_ACC.1 + FDP_ACF.1 [V]; NIST SP 800-162 [K]; ISO/IEC 27001:2022 A.5.9 [P].
- **BA-3.1** "Every principal belongs to a stated class — human role, application, or subsystem acting under its own authority — and carries a mandate whose source can be named." (Doc 0 §3 BA-3.1)
- **BA-3.2** "Every asset carries a custody class as a first-class, typed attribute, not a description that happens to appear in prose near it." (Doc 0 §3 BA-3.2)
- **BA-3.3** "Every operation the system performs is named once, consistently, and maps to exactly one checkpoint (Attribute 5) where it is evaluated." (Doc 0 §3 BA-3.3)
- **TA-3.1** "The three classes are enumerable: a finite, named list of principal classes, asset classes, and operations exists and can be produced on request…" (Doc 0 §3 TA-3.1)
- **TA-3.2** "A principal that is also an asset — a model, which acts and is also protected — is tagged with both roles explicitly…" (Doc 0 §3 TA-3.2)
- **TA-3.3** "Asset and principal identifiers are stable across the system…" (Doc 0 §3 TA-3.3)

### Attribute 4 · Control / Invariant
Standard: NIST SP 800-53 Rev 5 + SP 800-53A [V for AU-3, K catalog]; ISO/IEC 27001:2022 cl. 6.1.3(d) [P].
- **BA-4.1** "Every control carries an assessment procedure: a stated method — examine the artefact, test the behaviour, or both…" (Doc 0 §4 BA-4.1)
- **BA-4.2** "Every control has one named owning subsystem, recorded as a field of the control itself…" (Doc 0 §4 BA-4.2)
- **BA-4.3** "Every control carries a status from the fixed set defined in rule_criteria_spec_v1 — CANON, RULED, DEFAULT, PROPOSED, or OPEN — and that status is current, not aspirational." (Doc 0 §4 BA-4.3)
- **TA-4.1** "Every control carries a unique, stable identifier, under the naming and scheme-exclusivity discipline of rule_criteria_spec_v1 §4." (Doc 0 §4 TA-4.1)
- **TA-4.2** "A control's satisfaction is, wherever the underlying property allows it, machine-checkable — expressed so that the assessment procedure can be automated…" (Doc 0 §4 TA-4.2)
- **TA-4.3** "A control's history — proposed, ratified, amended, retired — is retained in the Rule Registry (rule_criteria_spec_v1 §6), append-only…" (Doc 0 §4 TA-4.3)

### Attribute 5 · Checkpoint
Standard: NIST SP 800-162 §2 (PEP/PDP/PIP/PAP) [K]; OASIS XACML 3.0 [K].
- **BA-5.1** "Every checkpoint's decision role (PDP) and enforcement role (PEP) are named separately, even where the same subsystem performs both…" (Doc 0 §5 BA-5.1)
- **BA-5.2** "Every checkpoint's outcome set is stated explicitly — which of pass, refuse, route, modify, defer, or annotate are possible at this checkpoint…" (Doc 0 §5 BA-5.2)
- **BA-5.3** "Every checkpoint's policy administration point (PAP) — where the rules it evaluates are authored and changed — is named, and is governed under Attribute 9." (Doc 0 §5 BA-5.3)
- **TA-5.1** "Every checkpoint's policy information point (PIP) — where the attribute values it evaluates come from — is named and is itself either inside the Trusted Computing Base or explicitly documented as a trust dependency…" (Doc 0 §5 TA-5.1)
- **TA-5.2** "A checkpoint's decision and enforcement, where co-located in one component, are nonetheless separable in the design…" (Doc 0 §5 TA-5.2)
- **TA-5.3** "Identical inputs to a checkpoint, with identical attribute state, produce identical outcomes — a checkpoint whose decision depends on unstated context has an undeclared, and therefore unauditable, policy information point." (Doc 0 §5 TA-5.3)

### Attribute 6 · Reference Monitor
Standard: NIST SP 800-53 AC-25 [V]; TCSEC reference validation mechanism [V]; Common Criteria ADV_ARC.1 [K].
Three defining properties: **complete mediation (non-bypassability) · tamper-resistance · verifiability**.
- **BA-6.1** "For every reference monitor, every path from before it to after it is enumerated, and each is shown to pass through the monitor's evaluation — non-bypassability is demonstrated per path, not asserted of the monitor as a whole." (Doc 0 §6 BA-6.1)
- **BA-6.2** "A reference monitor's governing policy — what it checks, and against what — is changed only through the ceremony specified under Attribute 9, never by a code edit made by a party subject to the monitor's own mediation." (Doc 0 §6 BA-6.2)
- **BA-6.3** "A security architecture description exists, in the sense required by ADV_ARC.1, for every reference monitor in the system…" (Doc 0 §6 BA-6.3)
- **TA-6.1** "A reference monitor's own code and configuration are held outside the reach of any principal it mediates…" (Doc 0 §6 TA-6.1)
- **TA-6.2** "A reference monitor is small enough that its complete logic can be read and independently verified in a single sitting by a qualified reviewer…" (Doc 0 §6 TA-6.2)
- **TA-6.3** "A reference monitor's secure initialisation is itself specified: what state it starts in, what must be true before it will evaluate its first request…" (Doc 0 §6 TA-6.3)

### Attribute 7 · Mandatory Baseline
Standard: TCSEC MAC (division B1+) [K]; Common Criteria FDP_IFC.1/IFF.1 paired with FDP_ACC.1/ACF.1 [K]; NIST SP 800-53 AC-3/AC-4 [K].
Four defining properties: **set by authority distinct from the measured · unlowerable by the measured · identical for the class · refusal on failure (not degraded pass)**.
- **BA-7.1** "Every mandatory baseline is stated as a named policy over the governed triad…" (Doc 0 §7 BA-7.1)
- **BA-7.2** "No baseline's value is alterable by the principal or subsystem being measured against it. A mechanism that allows a subject to adjust the standard it is held to, even temporarily or within stated limits, is a discretionary threshold and must be named as one…" (Doc 0 §7 BA-7.2)
- **BA-7.3** "Falling below a mandatory baseline produces refusal. A partial, degraded, or best-effort result returned in place of refusal is evidence the baseline in question is not, in fact, mandatory." (Doc 0 §7 BA-7.3)
- **TA-7.1** "A baseline's value is held in versioned, ceremony-governed configuration (Attribute 9), not in a code path the measured component's own logic can branch on or adjust." (Doc 0 §7 TA-7.1)
- **TA-7.2** "A baseline applies identically to every principal in its stated class — there is no code path that grants a specific principal a reduced baseline outside the ceremony that would authorise it for the whole class." (Doc 0 §7 TA-7.2)
- **TA-7.3** "Where a system offers something that looks like a lowered baseline — a relaxed standard for a bounded session, for instance — it is implemented and labelled as a distinct, discretionary threshold, with its own authority and its own ceiling, never as the mandatory baseline itself with an exception clause." (Doc 0 §7 TA-7.3)

### Attribute 8 · Audit Record
Standard: NIST SP 800-53 AU-3 [V verified verbatim], AU-9, AU-10 [K]; Common Criteria FAU_GEN.1.2, FAU_STG.1, FPT_STM.1, FAU_SAR.1 [K].
Six AU-3 elements: (a) what event, (b) when, (c) where, (d) source, (e) outcome, (f) identity of principal.
- **BA-8.1** "Every audit record establishes all six AU-3 elements: event type, time, location or component, source, outcome — including failure outcomes, not successes only — and the identity of the principal…" (Doc 0 §8 BA-8.1)
- **BA-8.2** "Audit records are generated for both successful and refused operations at every checkpoint. A record scheme that only captures what a checkpoint permitted cannot demonstrate non-bypassability…" (Doc 0 §8 BA-8.2)
- **BA-8.3** "Audit records are available for review through a stated capability, not only reconstructable by someone with direct access to the underlying store." (Doc 0 §8 BA-8.3)
- **TA-8.1** "Every audit record's timestamp derives from a reliable, tamper-resistant time source shared across the system…" (Doc 0 §8 TA-8.1)
- **TA-8.2** "Audit records are protected from undetected modification and deletion, through append-only storage, cryptographic chaining, or an equivalent mechanism…" (Doc 0 §8 TA-8.2)
- **TA-8.3** "Audit records are bound to their generating principal such that they cannot be forged as having originated elsewhere — non-repudiation is a property of the record's construction, not an assumption made about the store it lives in." (Doc 0 §8 TA-8.3)

### Attribute 9 · Authority & Change Control
Standard: NIST SP 800-53 CM-3, CM-5 [K]; Common Criteria ALC_CMC, ALC_CMS [K]; ISO/IEC 27001:2022 A.8.32 [P].
- **BA-9.1** "Every control and every mandatory baseline names the authority empowered to change it. Where that authority is a role rather than an individual, the role is named, and who currently holds it is a matter of record, not inference." (Doc 0 §9 BA-9.1)
- **BA-9.2** "A change to a control or a baseline is preceded by a documented review of its impact — what depends on the thing being changed, and what changing it could break — before it is approved, not discovered afterward." (Doc 0 §9 BA-9.2)
- **BA-9.3** "A change to a control or a baseline, once approved, is retained as a record: what changed, who approved it, when, and why, on the append-only discipline specified for the Rule Registry." (Doc 0 §9 BA-9.3)
- **TA-9.1** "Every controlled item — a control, a baseline, a piece of governed configuration — carries a unique, stable identity under configuration management, distinct from its current value…" (Doc 0 §9 TA-9.1)
- **TA-9.2** "Access to make a change is logically restricted to the named authority's own credentials or role — the restriction is enforced by the system, not observed as a matter of practice." (Doc 0 §9 TA-9.2)
- **TA-9.3** "The scope of what is under this discipline — which documents, which configuration, which code paths — is itself explicitly declared…" (Doc 0 §9 TA-9.3)

### Attribute 10 · Determinism Boundary ("detect, never decide")
Standard: no mature conformance standard (self-declared). Closest practice: Simplex architecture (Sha, 2001); ISO/IEC TR 5469:2024; EU AI Act Art. 14 [K]; NIST AI RMF 1.0 (Govern/Map/Measure/Manage).
Article 14 five capabilities: (a) understand-and-monitor · (b) automation-bias awareness · (c) correct interpretation · (d) override · (e) halt-to-safe-state.
- **BA-10.1** "Every subsystem and every component within a subsystem is classified deterministic or learned, and that classification is a matter of record, not an inference…" (Doc 0 §10 BA-10.1)
- **BA-10.2** "For every learned component, the specific structural mechanism that denies it decision authority is named…" (Doc 0 §10 BA-10.2)
- **BA-10.3** "Human oversight, where a human rather than a deterministic component is the check on a learned component's output, is implemented to the standard of EU AI Act Article 14: the overseer can understand the system's limitations, is positioned to notice automation bias rather than merely warned about it, can correctly interpret what the system produced, can override or disregard it in a specific instance, and can halt the system to a safe state — five distinct capabilities, not one 'a human is in the loop' statement standing in for all five." (Doc 0 §10 BA-10.3)
- **TA-10.1** "A verified, deterministic decision module can override any learned component's recommendation, and the override path itself is inside the Trusted Computing Base…" (Doc 0 §10 TA-10.1)
- **TA-10.2** "The boundary between a learned component's output and a deterministic component's decision is a structural seam — an interface a learned component's output must cross, checked on the deterministic side — not a convention observed by the code that happens to call both." (Doc 0 §10 TA-10.2)
- **TA-10.3** "Learned components are excluded from the Trusted Computing Base by the membership test given under Attribute 1: not deterministic, therefore not eligible, regardless of how central their function is to the system's value." (Doc 0 §10 TA-10.3)

### Attribute 11 · Failure Posture
Standard: Common Criteria FPT_FLS.1 [K]; NIST SP 800-53 SC-24 [K]; IEC 61508 [P].
Two postures: **fail-closed · fail-safe-open** (per component, not uniform).
- **BA-11.1** "Every component's failure types are enumerated — the specific ways it can fail to complete an evaluation…" (Doc 0 §11 BA-11.1)
- **BA-11.2** "Every reference monitor and every component inside the Trusted Computing Base fails closed, without exception…" (Doc 0 §11 BA-11.2)
- **BA-11.3** "Where a component fails safe-open — correctly, because the safe direction is to proceed toward recomputation or an equivalently recoverable state rather than to block — that choice is declared for that component specifically, with the reasoning on record…" (Doc 0 §11 BA-11.3)
- **TA-11.1** "The state preserved across a failure is specified per component…" (Doc 0 §11 TA-11.1)
- **TA-11.2** "Where a recovery time objective applies — a maximum duration a governed capability may be unavailable before the unavailability itself becomes a breach of a mandatory baseline — it is a stated, ratified value, not an assumption." (Doc 0 §11 TA-11.2)
- **TA-11.3** "A component's failure posture is testable: the failure can be induced under controlled conditions and the resulting state checked against what was specified, rather than the posture being a claim that is only ever exercised by accident." (Doc 0 §11 TA-11.3)

### Attribute 12 · Trust Domain
Standard: Common Criteria ADV_ARC.1 (domain separation) [K]; NIST SP 800-53 SC-2, SC-3, SC-7 [K]; ISO/IEC 27017:2015 [P].
- **BA-12.1** "Every trust domain in the system is named — the platform domain, each tenant's domain, and any domain (such as an internal monitoring function) that is deliberately isolated even from the platform's own primary domain…" (Doc 0 §12 BA-12.1)
- **BA-12.2** "The deployment model — whether multiple tenants share infrastructure with logical separation, or each tenant's instance is physically or virtually dedicated — is explicitly stated…" (Doc 0 §12 BA-12.2)
- **BA-12.3** "Under the NIST AI Risk Management Framework's Map function — establishing the context and boundary of a specific AI system before its risks can be measured — every governed AI capability in the system has a stated trust domain as part of that context…" (Doc 0 §12 BA-12.3)
- **TA-12.1** "Every boundary between trust domains — inbound from outside the platform, and internal between subsystems that do not share a domain — has a managed interface: a declared, monitored point of crossing, with no undeclared path between domains." (Doc 0 §12 TA-12.1)
- **TA-12.2** "Data and identifiers do not resolve across trust domains by default — a principal or asset identifier meaningful in one tenant's domain does not, without an explicit, governed crossing, resolve to anything in another tenant's domain or in the platform domain." (Doc 0 §12 TA-12.2)
- **TA-12.3** "A domain that is isolated from the platform's own primary domain by design — a monitoring function whose isolation from what it monitors is the point — has that isolation itself specified: what it shares with the domain it observes, and, more importantly, what it deliberately does not." (Doc 0 §12 TA-12.3)

## §B · Part 2 — Product Component Registry & Build Requirements

**16 components · 36 BR-x.y build requirements.**

Component (Instantiates) → BR-x.y (derives from) STATUS

1. **SyniSense ("Shield")** — Subsystem · Reference Monitor · Governed Triad (custody class) · Audit Record
   - BR-1.1 Every code path to external model client routes through the single chokepoint function; violation fails the build via negative-scan test. [Att 6 · TA-6.1 non-bypassability] · **STATUS Met** — A5.1
   - BR-1.2 Chokepoint custody-sequence logic and closed-network allowlist in configuration a subject cannot alter at runtime; integrity verified at load. [Att 6 · TA-6.1 self-protection runtime] · **STATUS Partial** — build-time gates exist (A5.5); runtime integrity verification unspecified. See G-6.
   - BR-1.3 Trust receipt schema carries invoking-principal identity and reliable timestamp. [Att 8 · BA-8.1 AU-3 six elements] · **STATUS Not Met** — A5.7's content omits both. See G-8.
   - BR-1.4 Every asset passing crossing carries explicit typed custody classification consumed by de-identification logic. [Att 3 · BA-3.2] · **STATUS Partial** — custody classes distinguished in practice but not confirmed as typed queryable attribute. See G-3.
   - BR-1.5 Chokepoint fails closed on any internal error. [Att 11 · BA-11.2] · **STATUS Met** — consistent with A5.6's structural-impossibility doctrine; not separately enumerated as stated failure type. See G-11.

2. **Solva** — Subsystem · Determinism Boundary
   - BR-2.1 Two-faculty seam enforced by import assertion, not coding convention. [Att 10 · TA-10.2] · **STATUS Met** — #31.
   - BR-2.2 Solva's role in any "innovate" outcome recorded as joint with CIF's governance. [Att 10 · BA-10.1] · **STATUS Partial** — joint-delivery principle stated; per-instance mechanism not confirmed. See G-10.
   - BR-2.3 Reasoning trace retained from first commit of a ThinkLab session. [Att 6 · TA-6.3 verifiability] · **STATUS Met** — #31.

3. **Northena** — Subsystem · Governed Triad (operation integrity)
   - BR-3.1 Objective-freeze mechanism is single shared implementation invoked identically by every subsystem. [Att 3 · BA-3.3] · **STATUS Met** — Promise #32.
   - BR-3.2 Progressive disclosure's checkpoint states possible outcomes (full/partial/deferred). [Att 5 · BA-5.2] · **STATUS Not confirmed** from canon material located — open item.

4. **Mtafiti ("the Registry")** — Subsystem · Governed Triad (asset inventory, partial)
   - BR-4.1 Registry asset coverage extended from estate sources to full asset class (models, artifacts, receipts, rules), each with named owner. [Att 3 · BA-3.1 ISO 27001 A.5.9] · **STATUS Not Met** — Promises #12, #13 cover estate sources only. See G-3.
   - BR-4.2 Registry exposes asset classification scheme in a form producible on request. [Att 3 · TA-3.1] · **STATUS Partial** — census/connection specified; published class list not located.

5. **Targeta** — Subsystem · Determinism Boundary · Mandatory Baseline
   - BR-5.1 Model acceptance requires every stated criterion satisfied; failing any criterion refuses in full. [Att 7 · BA-7.3] · **STATUS Met** — MOAC Promise #22.
   - BR-5.2 Yield wall detects and optimises but cannot itself grant acceptance. [Att 10 · TA-10.1] · **STATUS Met** — 19A.2.
   - BR-5.3 Acceptance policy stated as named SFP over the triad. [Att 7 · BA-7.1] · **STATUS Not Met** — no named SFP located. See G-7.

6. **Mkondo (Task & Job Orchestration)** — Subsystem · Governed Triad (operation hand-off) · Checkpoint
   - BR-6.1 Every job hand-off between subsystems (not only ThinkLab→Task-Manager) crosses registered hand-off checkpoint carrying commissioned, shape, identity, receipt. [Att 3 · BA-3.3] · **STATUS Partial** — Promise #32 Partial in canon: one concrete instance, no generalised registered handoff contract. See G-13.
   - BR-6.2 Unregistered or malformed hand-off surfaces as finding at point of hand-off. [Att 5 · BA-5.1] · **STATUS Met for one instantiated crossing**; not yet true generally.
   - BR-6.3 No-dual-hatted-task rule enforced at hand-off checkpoint. [Att 3 · BA-3.3] · **STATUS Named as Promise #32 feature; enforcement mechanism not independently confirmed beyond one crossing.**

7. **The Watch (Grey Mirror + the Watch)** — Subsystem (outside the six) · Reference-Monitor-adjacent · Trust Domain · Checkpoint  
   **⚠ AMENDED by Trojan/Whisper Amendment 6 · 2026-09-05: upgraded to full Reference Monitor instantiation.**
   - BR-7.1 Grey Mirror's detection and Watch's decision-and-enforcement implemented as separable components behind shared verdict interface. [Att 5 · BA-5.1] · **STATUS Met** — Macho/Mkono split.
   - BR-7.2 Watch's own trust domain described as distinct from domains it observes. [Att 12 · BA-12.1] · **STATUS Partial** — isolation exists; ADV_ARC-sense description not confirmed. See G-12.
   - BR-7.3 Changes to Watch's own governing policy pass through platform's slowest change-control tier with external witness holding no Watch credentials. [Att 9 · BA-9.1] · **STATUS Met** — stated explicitly. See G-9 general case.
   - BR-7.4 Grey Mirror's learned pattern-matching classified as learned and excluded from Watch's decision authority. [Att 10 · BA-10.1] · **STATUS Not confirmed** — Watch-specific instance of G-10.

8. **The Ledger** — Audit Record (primary) · Trusted Computing Base
   - BR-8.1 Ledger accepts and retains records of refused operations on same terms as accepted. [Att 8 · BA-8.2] · **STATUS Met** — WPW-7 pattern.
   - BR-8.2 Append-only hash-chained structure independently verifiable. [Att 8 · TA-8.2] · **STATUS Met in structure**; independent verifiability by non-writer not separately confirmed.
   - BR-8.3 Ledger writer included in TCB enumeration required under Attribute 1. [Att 1 · BA-1.3] · **STATUS Not Met** — no TCB enumeration exists. See G-1.

9. **CIF (Conditioned Ideation Faculty)** — Determinism Boundary (primary) · TCB (explicit exclusion)
   - BR-9.1 CIF excluded from TCB by Attribute 1 membership test — learned, therefore ineligible. [Att 1 · TA-1.2] · **STATUS Met by doctrine**; not yet recorded as applied instance of a published TCB test (test itself unpublished). See G-1, G-10.
   - BR-9.2 Every CIF-originated idea adopted into a run passes through deterministic acceptance point. [Att 10 · TA-10.1] · **STATUS Met.**
   - BR-9.3 CIF's own MUST/MUST-NOT set carries assessment procedure. [Att 4 · BA-4.1] · **STATUS Not confirmed** — CIF's rule-by-rule enumeration not located.

10. **The Critic Seam (Document 19A)** — Checkpoint · Determinism Boundary
    - BR-10.1 QA-tier findings do not block execution on their own; routed to deterministic decision point. [Att 10 · BA-10.1] · **STATUS Met** — QA-1.
    - BR-10.2 Seam's outcome set stated per check. [Att 5 · BA-5.2] · **STATUS Partial** — RV/QA naming implies outcome set; explicit enumeration not located.

11. **MOAC** — Reference Monitor (partial) · Mandatory Baseline
    - BR-11.1 MOAC's acceptance criteria not alterable by the run being evaluated. [Att 7 · BA-7.2] · **STATUS Met.**
    - BR-11.2 MOAC's non-bypassability and tamper-resistance demonstrated in security architecture description. [Att 6 · TA-6.1/TA-6.2] · **STATUS Not Met** — asserted in doctrine, not demonstrated. See G-6.

12. **Manage Rules** — Authority & Change Control (customer-facing)
    - BR-12.1 Every customer rule change preceded by stated ceremony; retained in full version history. [Att 9 · BA-9.1/BA-9.3] · **STATUS Met** — Promise #27.
    - BR-12.2 No customer rule authored can relax a system rule tagged STRUCTURAL or MECHANICAL. [rule_criteria_spec_v1 §8] · **STATUS Partial** — principle stated; enforcement at proposal time not separately confirmed.

13. **Whitepaper Wizard** — Checkpoint · Control/Invariant · Audit Record · 18 controls
    - BR-13.1 Tier-3 eligibility outcome set stated explicitly (eligible via results / methods / both / not eligible). [Att 5 · BA-5.1] · **STATUS Met** — WPW-11.
    - BR-13.2 Every notebook entry carries timestamp, link to run artefact, evidence class (measured/estimated/observed). [Att 8 · BA-8.1] · **STATUS Met** — WPW-4.
    - BR-13.3 Wizard cannot alter training state/schedule/parameters/outcomes; verified by build-time zero-influence check. [Att 2 · TA-2.2] · **STATUS Met** — WPW-2 with A2 acceptance criteria.

14. **Connect Wizard** — Checkpoint (admission)
    - BR-14.1 Rights recorded at connection setup are explicit PIP every downstream checkpoint draws from. [Att 5 · TA-5.1] · **STATUS Met in function**; not independently confirmed as named PIP for other checkpoints.

15. **Agent-Deploy Wizard** — Checkpoint
    - BR-15.1 Checkpoint outcome set stated (deploy at requested rung / lower rung / defer). [Att 5 · BA-5.1] · **STATUS Not confirmed** — scope beyond "a step in the ladder" not detailed. Open item.

16. **Deck Rendering Engine** — Control/Invariant · Determinism Boundary · 14 controls (DR-R1..DR-R14)
    - BR-16.1 Byte-identical output for identical DeckSpec input is build-time verified. [Att 10 · TA-10.3] · **STATUS Met** — DR-R2.
    - BR-16.2 Fourteen controls carry explicit owning subsystem field. [Att 4 · BA-4.2] · **STATUS Partial** — ownership implied by document; explicit field not confirmed.

## §C · Part 3 — Gap Register (G-1 .. G-13)

Ordered by Attribute-dependency (Part 1 §0). G-13 placed by attribute dependency, not discovery order.

| ID | Attribute | Kind | Gap (verbatim from Table 2) |
|---|---|---|---|
| G-1 | 1 · TCB | Documentary | No enumerated, published list of Trusted Computing Base members. |
| G-2 | 2 · Subsystem | Documentary | No architecture description; the Watch's placement and the composite promises' ownership are undocumented decisions. |
| G-3 | 3 · Governed Triad | Documentary · Mechanical | No formal principal/asset/operation classes prior to this document; asset inventory covers estate sources only. |
| G-4 | 4 · Control | Documentary | No assessment procedure on any of the 272 rules; no Statement of Applicability. |
| G-5 | 5 · Checkpoint | Documentary | Decision/enforcement/information-point roles named only for the Watch. |
| G-6 | 6 · Reference Monitor | Documentary · Mechanical | No security architecture description; runtime tamper-resistance unaddressed beyond the chokepoint's build-time gates. |
| G-7 | 7 · Mandatory Baseline | Documentary · Ruling | No named security function policies; the evidence floor's lowering path is subject-alterable. |
| G-8 | 8 · Audit Record | Mechanical | Trust receipt specification omits principal identity and timestamp; no reliable-time control. |
| G-9 | 9 · Authority | Documentary | System-rule change control is "Owner ratifies," with no CM-3-style procedure or declared scope. |
| G-10 | 10 · Determinism Boundary | Documentary | No per-component deterministic/learned inventory; ruling loop not mapped to Article 14's five capabilities. |
| G-11 | 11 · Failure Posture | Documentary | Failure types not enumerated per component; posture not declared per checkpoint. |
| G-12 | 12 · Trust Domain | Documentary · Ruling | Domains not described as a set; deployment model unstated. |
| G-13 | 6 · Mkondo, Checkpoint | Mechanical | Job hand-off contract is instantiated once (ThinkLab → Task Manager); not generalised across crossings. |

Each gap carries a Statement, Consequence, and Fix Specified (draft normative language) in Doc 0 §3. Fixes summarised in `GAPS_TO_WAVES.md`.

## §D · Part 3 — Rulings Required

Four decisions Doc 0 surfaces and does not make. Nothing in Parts 1-3 is blocked by them; each affects the fix named against it.

- **R-1** TCB membership test (G-1): ratify the test proposed in Attribute 1 — deterministic and protection-critical — or set a different one before the list is published.
- **R-2** "Lower the standard" (G-7): re-home its authority under Attribute 9's ceremony so the evidence floor remains mandatory, OR reclassify it as a discretionary threshold distinct from the assertion floor.
- **R-3** The Watch's TCB membership (G-1): the service in full, or its deterministic response half only, with Grey Mirror's detection half excluded as learned under Attribute 10.
- **R-5** Deployment model (G-12): shared infrastructure with tenant separation, dedicated per tenant, or both, with the boundary stated per deployment.

Note: R-4 was resolved into G-9's two-tier fix directly and required no separate ruling. No ruling is attached to G-13: its fix is a build task, not a judgement call.

## §E · Standing

Doc 0 §4 Standing (verbatim): "This document is the layer every other Akki specification instantiates. … Where a future specification appears to conflict with a definition in Part 1, Part 1 governs, on the principle Document 16 already applies platform-wide: the foundation does not yield to what was built on it."

**Draft v1, dated 1 September 2026, for owner ratification.**
