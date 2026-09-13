READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W_SOLVA_V2_LIFT_grounding_brief.md — wave open

**Wave label:** `W-SOLVA-V2-LIFT` — banked per standing owner ruling 2026-09-06T~19:20Z ("Solva-v2 lift queues immediately behind Registry") + this session's Phase C plan §W-SOLVA-V2-LIFT + owner directive 2026-09-13.

**Wave opens:** 2026-09-13 · ratchet floor **3531** (post-W-REGISTRY-EXTENSION-G3).

**Standalone.** Not a sub-component of Registry or DAP (owner reinforced this session). Peer wave; depends only on W1c primitives (banked at 3503) — independent of W-REGISTRY-EXTENSION-G3.

---

## §A · Canon anchors (first-hand, this session)

- **Canon-4 §19 (Solva)**, verbatim: "Solva judges whether reasoning is sound, whether preservation is sufficient, and whether an output asserts within its defensibility. It is the one engine that genuinely reasons — the direction governor is deterministic, targeting's learning is walled from eligibility, discovery's inference only detects. Solva is where actual judgement lives in the platform, and it never extracts and never reaches into the operator primitives that do: it issues operations, interprets results, and governs depth."
- **Doc-0 Component 2 §BR-2.1 (two-faculty seam)**, verbatim: "The two-faculty seam is enforced by an import assertion, not a coding convention — one faculty cannot invoke the other's authority even inadvertently, because the import itself is the enforcement point."
- **Canon-4 §23.1 (parameterless assertion-boundary signature)**, verbatim: "The class computation takes the load-bearing units and nothing else — no confidence, no reasoning strength, no evidence weight. The laundering case is not policed at runtime; it is unrepresentable. 'The evidence is overwhelming, assert the utterance as fact' cannot be expressed, because the function computing the class has no parameter through which reasoning strength could ever enter. The signature is the guard, and a signature assertion in the test suite is what keeps it one."
- **Canon-4 §22 (load-bearing set)**, verbatim (paraphrase-quoted for scope): "A load-bearing function that returned a class would have collapsed the two faculties into one — Solva chooses the units; it does not choose what those units imply."
- **Canon-4 §24 (three-action refusal envelope)**, verbatim (paraphrase-anchored): the refusal envelope offers exactly three actions — accept the result as a recorded statement, narrow the objective, or lower the standard. "Offering anything else would be offering something the system cannot actually deliver."
- **Canon-4 §26 (trace mandatory from first commit)**, verbatim: "It is the auditability that justifies letting a component reason at all, and it exists from the first commit."
- **Canon-4 §21.1 (intent audit)**: Solva opens with intent-audit record: situation class declared vs demonstrated by conduct; divergence tracked as session unfolds.
- **Canon-7 §44.1 (Critic Seam Tier 2 context isolation)**, verbatim: "A critic reading the author's rationale inherits the author's frame, which is the blind-spot-sharing failure this whole design exists to avoid."

## §B · CP-S1..CP-S8 · order matters — CP-S2 lands FIRST

Owner directive verbatim: "CP-S2 FIRST: the parameterless assertion-boundary signature must be built and asserted BEFORE the load-bearing reasoning function — this is the seam that proves Solva cannot fabricate."

| CP | Focus | File(s) | Grounding invariants |
|--:|---|---|--:|
| **CP-S2 (FIRST)** | Parameterless assertion-boundary signature (Canon-4 §23.1) built and its signature-guard test asserted BEFORE anything else binds to it. | `contracts/solva_reasoning.py`, `services/solva_v2/assertion_boundary.py` | 5 |
| CP-S1 | Two-faculty seam via import assertion (Doc-0 BR-2.1). Reasoning faculty cannot inadvertently invoke assertion boundary's authority; assertion boundary cannot import reasoning faculty. | `services/solva_v2/reasoning_faculty.py` | 3 |
| CP-S3 | Load-bearing function returns unit references ONLY (Canon-4 §22). Return type is `Sequence[UnitRef]`; NO class field on load-bearing return. | `services/solva_v2/reasoning_faculty.py::identify_load_bearing_units()` | 3 |
| CP-S4 | Three-action refusal envelope (Canon-4 §24): `accept_as_stated` · `narrow_objective` · `lower_standard`. Nothing else. | `contracts/solva_reasoning.py::RefusalEnvelope` | 4 |
| CP-S5 | Trace present from the first commit (Canon-4 §26): every Solva session emits a trace envelope parseable under the schema. | `services/solva_v2/trace.py` + `contracts/solva_reasoning.py::SolvaTrace` | 3 |
| CP-S6 | Intent audit — declared vs demonstrated (Canon-4 §21.1): the audit record carries both fields distinctly. | `services/solva_v2/intent_audit.py` + `contracts/solva_reasoning.py::IntentAuditRecord` | 3 |
| CP-S7 | Critic Seam Tier 2 binding (Canon-7 §41-46): critic invocation carries only `{artefact, canon, authorising_instrument, rubric}` — NEVER the author's rationale. | `services/solva_v2/critic_seam.py` + `contracts/solva_reasoning.py::CriticInvocation` | 4 |
| CP-S8 | Donor pool lift from `Akki-Executive-Core` — case-agnostic. Only the STRUCTURAL engine-step-name pattern (candidate_generation · tension_detector · reflection) is lifted as case-agnostic skeletons. Executive-domain tokens (board / CEO / diagnosis / chair / McKinsey / LOCKED_QUESTIONS / triangulation-by-sector / refusal-category-`out_of_scope`) are STRIPPED. Content that requires re-authoring beyond token-stripping is HALTED (see §D). | `services/solva_v2/engines/` | 5 |
| Snapshot parity | `contracts/solva_reasoning.py` registered in `CONTRACT_TO_SNAPSHOT` (headline + secondaries). | `tests/invariants/*.contract_snapshot.json` | 1 |

**Target invariants added: ~31.** Ratchet target 3531 → ~3562.

## §C · Donor-lift discipline (CP-S8)

Two categories:

**(1) LIFTABLE case-agnostic (token-stripped, no re-authoring):**
- Engine-step-name structural pattern: `candidate_generation`, `tension_detector`, `reflection` as skeleton engine files.  Each is a case-agnostic English word for a canon-recognisable reasoning primitive (Canon-4 §21 "candidate weighing, tension surfacing").
- Naming discipline: skeletons import from `contracts/solva_reasoning.py` (canon-grounded contracts), not from any donor-domain module.

**(2) HALTED (case-agnostic form ambiguous — owner ruling requested):**
- **Reflection `LOCKED_QUESTIONS`** in `Akki-Executive-Core/backend/services/solva_v2/engines/reflection.py`: three specific questions about "diagnosis" that require re-authoring, not token-stripping, to become case-agnostic. `[framing, not canon]`: canon does not fix a reflection-question set.
- **Refusal categories** in `Akki-Executive-Core/backend/services/solva_v2/engines/refusal.py`: donor uses `{clean, jailbreak_attempt, out_of_scope}` which does not map to Canon-4 §24's three actions `{accept_as_stated, narrow_objective, lower_standard}` — these are two different refusal shapes. `[framing, not canon]`: Canon-4 §24 is authoritative; donor's shape is executive-product-specific.
- **Triangulation-by-sector** in donor: `sector_tag` matching is domain-specific.
- **LLM adapter proxy / probability weighting** with LLM calls: cross-boundary integration outside this wave's platform-primitive scope.

For (2), CP-S8 lands **skeleton engines with `NotImplementedError`** that name the primitive but refuse fabrication until the case-agnostic form is owner-ruled.  No silent domain content is smuggled in.

## §D · HALTs raised at wave open

None yet.  If a HALT arises during CP execution, it will be logged in the wave-close honest-limits §C and reported to the owner in the close DECISION-POINT.

## §E · Honest limits (declared)

- **DPO-S1 · Refusal categories** — Canon-4 §24 three-action set adopted; donor's `{clean, jailbreak_attempt, out_of_scope}` NOT lifted (different refusal shape).
- **DPO-S2 · Reflection questions** — donor's LOCKED_QUESTIONS NOT lifted (executive-domain). Reflection engine skeleton lands as `NotImplementedError` awaiting owner-ruled case-agnostic reflection contract.
- **DPO-S3 · No LLM binding** — this wave lands the structural boundary and typed contracts; wiring an actual LLM adapter is a subsequent wave's concern and would introduce integration risk outside thin-kernel scope.
- **R-C1 · Rules Service unbuilt** — Solva reads floor and matrix through opaque handles; Canon-4 §23 verbatim "The floor and the class verdict are read-only. Solva reads them; it never sets or relaxes them." So no R-C1 direct dependency; noted for transparency.
- **R-C2 · Reliable time source unbuilt** — trace entries carry timestamps; `SolvaTrace.au_3b_defensible=False` invariant asserted on trace records (mirrors CP-R6's R-C2 marker discipline).

## §F · Discipline standing

- **BASELINE_GUARD=1** tests-first: RED banked at `phase0/drill_receipts/YYYYMMDDTHHMMSSZ_solva_v2_lift_RED_pre_impl.log`.
- **Double-green byte-match** at close.
- **`output_verified_seal Kind: solva_v2_lift`**.
- **Two-commit pattern**: Commit A (code, `programme/track-a`) + Commit B (state, `master`). NEVER push.
- **testing_agent BANNED.**
- **No egress. No Radio traffic.** T4 remains HELD.
- **W-JOURNEY-ASSISTANT** stays out of scope.
- **DAP-STACK** stays gated behind this wave per Phase C §D.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
