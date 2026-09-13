READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# JOURNEY_AND_ASSISTANT_AUDIT_20260913.md — interim, read-only

**Purpose.** Answer the owner's question — "is the natural, guided, collaborative agent-shaped journey I've been using also how the *end-user* is designed to experience this platform through its wizards and embedded assistant?" — with first-hand canon citations and no smoothing.

**Standing.** Interim audit. Read-only. Grounded on canon files opened this session (Canon 4/5/6/7/9, Doc-0 Part 2, DAP-Spec, Audio-Plane). `[framing, not canon]` tagging is standing practice.

**Date.** 2026-09-13.

---

## §1 What canon actually prescribes for the end-user journey

### §1.1 Setup (a) Registry onboarding, (b) source connect/train

**Canon-6 §3 Setup**, verbatim (first-hand):
> "A guided sequence captures the organisation's identity, the compliance owner's contact, the six governed seam values — each explained in one plain sentence with a recommended default — and the source list with the rights held on each. The review step states plainly that these choices are permanently recorded, and that changing any of them later requires two approvals."

> "Then, source by source: connect, test, and — for structured sources — confirm the mapping sample. This is the Extraction Console's Registry Administration screen, specified in Document 5 Part IV, walked once per source rather than all at once."

> "The whole journey is a working morning, and it ends with a signed setup record rather than a configuration file."

**Canon anchor for the registry side**: `Doc-0 Part 2 §14 Connect Wizard`, verbatim (first-hand):
> "The onboarding checkpoint through which an organisation's data sources connect to Mtafiti's registry: rights recorded at setup, a per-source profile maintained from first connection."
> BR-14.1: "Rights recorded at connection setup are the explicit policy information point every downstream checkpoint touching that source draws from — not re-derived or re-asked-for at each later checkpoint."

**Read**: Canon explicitly makes source-onboarding a *guided sequence*, not a form dump. The Connect Wizard is a checkpoint, not a chat surface — but Canon-6 §3 frames the walking-through of it as guided.

### §1.2 (c) Shape / declare an objective

**Canon-5 §14 Commission — The Shaping Wizard**, verbatim (first-hand):
> "Layout: a chat pane on one side, an objective draft rail on the other."
> "Chat. The operator states intent; the agent asks for mandatory fields and never proposes on them. An estate-check chip renders inline before any feasibility-dependent question is asked."
> "Draft rail. Three dimensions — entry, reach, output — plus the envelope, each field in one of three visual states: filled with a check, open and muted, or agent-assumed with the amber chip."
> "Sample action. Run a sample becomes available once reach is drafted."
> "Mandatory fields — reach, the four output fields, done-condition, budget, lawful basis — are asked, never pre-filled. Preference fields may carry agent recommendations, but the mandatory set never does. Every turn is grounded in a real estate read; no fabricated availability, ever, under any circumstance."

**This is the exact shape of what the owner has been experiencing**: chat pane + draft rail + agent asking, not pre-filling, every turn grounded in real reads.

**Canon-6 §6 Commissioning**, verbatim (first-hand):
> "The objective wizard — the Extraction Console's Commission screen, Document 5 §14 — turns a need into governed work in five steps: the need stated in plain words; scope selected from what the registry says actually exists; standards and rights confirmed against explained defaults; a plan preview — extraction volume as a range, reusable stock already identified, expected coverage of the goal, and what cannot be covered, all shown before any commitment; and commissioning itself, with a confirmation stating precisely what becomes permanent at that moment."

### §1.3 External-party version — DAP assistance chat

**DAP-Spec DAP-20**, verbatim (first-hand):
> "The portal's assistance chat MAY help a party shape an objective, identify relevant scope, or understand terms, before commission. It MUST NOT approve, widen scope after commission, or decide any gate. It proposes; the gates decide."

**DAP-Spec DAP-18**, verbatim (first-hand):
> "Every extraction is a commissioned job with a frozen objective. Objective freeze applies at commission: after commission, no path — including the portal's own assistance chat — may widen the job's scope. A wider scope is a new job."

**Read**: the external-party portal has a bounded assistance chat carrying the same collaboration-before-commission doctrine as the operator-facing Shaping Wizard, but with the sharper constraint that it never touches a gate.

### §1.4 (d) Reach an outcome — the working rhythm

**Canon-6 §11 Mining as a Practice**, verbatim (first-hand):
> "questions arrive from the business, and are asked of the estate ↓ most are answered ── the rest produce filed gaps, carrying their own demand evidence ↓ gaps accumulate and rank themselves — no one maintains a priority list ↓ objectives are commissioned against the top of that list, priced with their coverage stated ↓ the resulting extraction changes what the next round of questions can be answered from"

**Canon-6 §12 What Every Journey Above Has in Common**, verbatim (first-hand):
> "One record ... One boundary ... Three verdicts, never more. Every step in every journey above resolves to answered, held, or refused — never a fourth outcome invented to smooth over an awkward moment. Provenance that survives the whole path ... A loop that compounds."

## §2 Wizard-by-wizard shape (guided collaboration vs form-config surface)

| Component | Canon source | Shape it carries | Fits owner's "guided-collaboration" mental model? |
|---|---|---|---|
| **Setup guided sequence** | Canon-6 §3 | "guided sequence ... each explained in one plain sentence with a recommended default" | **Yes** — canonically guided. |
| **Connect Wizard** | Doc-0 §14 | Onboarding *checkpoint* with rights recorded at setup, per-source profile. Not a chat surface. | **Partial** — a guided walkthrough per Canon-6 §3, but the wizard itself is a checkpoint mechanism, not a chat/assistant. |
| **Shaping / Commission Wizard** | Canon-5 §14 | "chat pane on one side, an objective draft rail on the other. Agent asks mandatory fields, never proposes on them." | **Yes** — this is the exact pattern the owner describes, in canon. |
| **DAP assistance chat** | DAP-Spec DAP-20 | Chat that MAY help shape/scope/understand before commission; MUST NOT decide gates. | **Yes, bounded** — external-party variant of the same doctrine. |
| **Whitepaper Wizard (WPW)** | Doc-0 §13 | "A research observer attached to every training run: a contemporaneous notebook, a technical report, a white paper on eligibility." BR-13.3: "The wizard cannot alter training state, schedule, parameters, or outcomes — verified by a build-time zero-influence check". | **No — this is NOT a user-collaboration wizard.** It is an audit/observation satellite. `[framing, not canon]`: calling it a "wizard" in the user-collab sense misreads its role — its whole invariant is *not influencing* the user or the system. |
| **Agent-Deploy Wizard** | Doc-0 §15 | "The deployment step in the model-ladder progression, evaluating whether a given capability rung is appropriate for a given deployment context before proceeding." | **Underspecified in canon.** Doc-0 §15 STATUS verbatim: "Not confirmed — scope of function beyond 'a step in the ladder' was not detailed further in canon material located for this document. Recorded as an open item, not a resolved gap." Canon does not establish a chat/journey shape for this wizard. |
| **Deck Rendering Engine** | Doc-0 §16 | "Deterministic rendering ... byte-identical output for identical DeckSpec input". | **Not applicable** — not a user surface at all, an output invariant. |
| **Solva user-facing journey** | Canon-4 §24, §26; Canon-5 §29 | Refusal envelope with three explicit actions ("accept the result as a recorded statement, narrow the objective, or lower the standard"); answer card as the user-facing artifact of Solva's judgement. | **Partial** — the *contract shape* of Solva's engagement with the user is canon-fixed (three actions on refusal), but no chat/assistant surface for Solva itself is specified. The user meets Solva through the answer card (Canon-5 §29), not through a Solva-chat. |

## §3 Core adjudication — is "embedded assistant / guided collaboration" the platform's INTENDED UX doctrine?

**Read from canon (first-hand)**: Yes for the *objective-shaping* path — Canon-5 §14 and Canon-6 §3/§6 establish it as the intended shape for Setup, Commission, and (through DAP-20) external-party equivalents. **No** for the platform as a whole — Whitepaper Wizard is deliberately non-influencing, Agent-Deploy Wizard is underspecified, and Solva has no chat surface.

**Canon's own invariant that binds every journey** (Canon-6 §12, first-hand): "Three verdicts, never more. Every step in every journey above resolves to answered, held, or refused — never a fourth outcome invented to smooth over an awkward moment." The guided journeys land on the same three verdicts as every non-guided path. So even where canon extends guidance, it does not soften the gates.

**Explicit boundary in canon**: DAP-20 verbatim: "It proposes; the gates decide." This is the doctrinal boundary — an assistant may propose, ask, scope, and explain, but never decide.

`[framing, not canon]`: The owner's "connected systems, shape the census objective" experience with me maps cleanly onto Canon-5 §14 + Canon-6 §3–§6. The intent is canon-native. The gap (below) is coverage.

## §4 GAPS — plainly stated (SO §3 no-silence)

### §4.1 Agent-Deploy Wizard is canonically underspecified

Doc-0 §15 STATUS verbatim: "Not confirmed — scope of function beyond 'a step in the ladder' was not detailed further in canon material located for this document. Recorded as an open item, not a resolved gap."

A user deploying an agent has no canon-specified guided/chat surface. The wizard exists as a *checkpoint* (Doc-0 §15 Instantiates: Checkpoint) but its user-facing shape is not designed.

### §4.2 Registry onboarding has a guided walkthrough (Canon-6 §3) but no assistant

Canon-6 §3 says "guided sequence ... source by source: connect, test, and — for structured sources — confirm the mapping sample" — but the Connect Wizard itself (Doc-0 §14) is a checkpoint mechanism, not a chat/assistant. The owner's experience of *me talking them through the connection* is not specified anywhere as a shipped surface. It is closer to the Setup guided sequence (Canon-6 §3) than to the Shaping Wizard chat pane (Canon-5 §14).

### §4.3 Solva has no user-facing chat surface

Solva's user contract is canon-fixed (Canon-4 §24 three actions on refusal; Canon-5 §29 answer card), but the *conversational* engagement of "walk me through why the answer stopped here and what I should do" is not a designed surface. The user meets Solva through the answer card and the refusal envelope, not through a Solva-chat.

### §4.4 No unifying "embedded assistant doctrine" spans all wizards

The pattern exists in three canon-specified sites:
1. Setup guided sequence (Canon-6 §3)
2. Shaping Wizard (Canon-5 §14)
3. DAP assistance chat (DAP-20)

but it does not extend uniformly to Whitepaper Wizard (deliberately non-influencing), Agent-Deploy Wizard (underspecified), Deck Rendering (not user-facing), or Solva (no chat). A user's experience of guided-collaboration therefore varies by which wizard they touch, and canon does not smooth that variation.

### §4.5 Registry onboarding vs. Shaping Wizard — chat asymmetry

The Setup / Connect flow is a *guided sequence* — steps and defaults, explained plainly, but not a live chat pane. The Shaping Wizard is a *chat pane + draft rail*. These are two different collaboration modes. The owner has been experiencing chat-mode with me for both connection and objective-shaping; canon codifies chat-mode only for objective-shaping.

## §5 Candidate future wave (name only; do NOT fold into W-REGISTRY without owner ruling)

**`W-JOURNEY-ASSISTANT`** `[framing, not canon]`: a wave that would extend the Shaping-Wizard chat-mode collaboration pattern (Canon-5 §14) uniformly to (a) Setup / Connect onboarding, (b) Agent-Deploy Wizard, and (c) a Solva-facing "walk me through the answer" surface, all inheriting the same doctrinal boundary from DAP-20 ("it proposes; the gates decide"). This would close §4.1–§4.5.

**Explicit non-decision**: this candidate wave is **noted, not proposed for the current cycle**. Owner directive this session: "If this reveals a candidate future wave (e.g., a journey/assistant layer), name it but do not fold it into W-REGISTRY without an owner ruling." Done.

## §6 Bottom line for the owner

- The natural, guided, chat-shaped experience the owner has been having is **canon-native** — Canon-5 §14 designs it explicitly for the Shaping / Commission Wizard, and Canon-6 §3 and DAP-20 extend the collaboration mindset to Setup and to external-party portals.
- It is **NOT uniform** across the platform. Three components (Shaping Wizard, DAP assistance chat, Setup) carry it; three components (Whitepaper Wizard, Agent-Deploy Wizard, Deck Rendering Engine) do not — for different reasons (deliberate non-influence, underspecified, not user-facing). Solva has a user contract but no chat surface.
- Where canon codifies the pattern, the gates remain hard: an assistant proposes, never decides (DAP-20). This is not negotiable.
- If the owner wants that collaboration-with-assistant shape everywhere — Registry onboarding, Agent-Deploy, a Solva-explain surface — that is a candidate future wave (§5), not a Registry sub-scope, and it needs an owner ruling before it can be folded in.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
