"""R-88..R-90 · CP-CONTENT-REGISTRY-WAVE · load-bearing vocabulary registration for CON-1..CON-31 (Content Registry Spec v1 §2 The Three Classes + §3 The Registry + §4 The Resolver + §5 The Slot Model / Salience + §6 The Generated Path + §7 Storage & Persistence + §8 Erasure & Retention + §9 Freshness).

R-90 third slice (this commit): additively extends the module with §6 (CON-22) + §7 (CON-23..CON-26) + §8 (CON-27..CON-28) + §9 (CON-29..CON-31) + grep-negative ban #4..#7 anchor scanners (softening · templated-text-storage · generated-text-as-render-dependency · unsupported-claim-state).

R-89 second slice: additively extended the module with §4 (CON-12..CON-14) + §5 (CON-15..CON-21) + grep-negative ban #3 anchor scanner.

R-88 first slice · CP-CONTENT-REGISTRY-WAVE · load-bearing vocabulary registration for CON-1..CON-11 (Content Registry Spec v1 §2 The Three Classes + §3 The Registry).

Owner Ruling 4 verbatim (banked in STATE/DECISIONS.md OWNER RULINGS anchor · 2026-09-20T~19:00Z · re-affirmed at `1250c39a` + R-86 Commit-C `e40047f4` + R-87 Commit-C `9823a520` + R-88 HUNT banking `80e42629`):

    "R-88+ CP-CONTENT-REGISTRY-WAVE (Ruling 4 · CON-1..31 · 7-category grep-negative bans + R-32 surface-list binding on Generated-class)."

Owner 7-category grep-negative ban set verbatim: "no improvised copy · no numbers from generated prose · no engagement signals in ranking · no softening of unsupported claims · templated text never stored · no generated text stored · no unsupported claims."

Owner R-32 surface list verbatim: "chat answers · recommendation bodies · notification bodies — nothing else." Matches CON-22 SRR statement byte-verbatim.

R-88 first-slice scope (SO §6.4 NOTHING-BEYOND): this module registers the vocabulary for CON-1..CON-11 as Final[...] constants so downstream slices (R-89 CON-12..21 · R-90 CON-22..31) + FE-FIX-READY-shaped specifications + auditors + reviewers have a single source of truth. Slice per HUNT banking at `80e42629`.

## What is registered (CON-1..CON-11 · SRR §2 + §3)

- **CON-1** · Every string that reaches a surface belongs to exactly one content entry and exactly one class.
  - `CONTENT_CLASSES: Final[tuple[str, ...]] = ("Fixed", "Templated", "Generated")` — the three-class enumeration.
  - `IMPROVISED_COPY_REFUSED: Final[bool] = True` — a component composing text outside the registry is refused by the resolver.
  - `STRING_WITHOUT_ENTRY_DOES_NOT_RENDER: Final[bool] = True` — no entry means no render.

- **CON-2** · Fixed entries render their text verbatim.
  - `FIXED_RENDER_VERBATIM: Final[bool] = True`.
  - `FIXED_TEXT_CHANGE_REQUIRES_CEREMONY: Final[bool] = True` — the text is a contract; ceremony changes it, not code.

- **CON-3** · Templated entries render only from named dependencies that resolve to verified fields.
  - `TEMPLATED_DEPENDENCIES_ONLY: Final[bool] = True`.
  - `TEMPLATED_NO_VALUES_OUTSIDE_DEPENDENCIES: Final[bool] = True` — a Templated string contains no value that is not a dependency.

- **CON-4** · Every Templated entry carries an honest-gap variant for each dependency that may be null.
  - `TEMPLATED_HONEST_GAP_VARIANT_REQUIRED: Final[bool] = True`.
  - `TEMPLATED_MUST_NOT_ESTIMATE_DEFAULT_OR_INFER: Final[bool] = True` — the template MUST NOT estimate, default, or infer a missing value.

- **CON-5** · Generated entries carry a class ceiling of inference or advisory and never fact.
  - `GENERATED_CLASS_CEILING_VALUES: Final[tuple[str, ...]] = ("inference", "advisory")`.
  - `GENERATED_NEVER_FACT_CLASS: Final[bool] = True`.
  - `GENERATED_EVERY_SENTENCE_ANCHORS: Final[bool] = True` — every sentence in a Generated string anchors to material by provenance reference; an unanchored sentence is refused by Solva's classing.

- **CON-6** · A number on any surface comes from a Templated dependency or a Fixed string.
  - `NUMBER_SOURCES_ALLOWED: Final[tuple[str, ...]] = ("Templated", "Fixed")`.
  - `GENERATED_MUST_NOT_INTRODUCE_NUMBERS: Final[bool] = True` — prose may wrap a number, never mint one.

- **CON-7** · Which surfaces may carry Generated entries at all is a ruled list (R-32).
  - `R32_GENERATED_SURFACE_WHITELIST: Final[tuple[str, ...]] = ("chat_answer", "recommendation_body", "notification_body")` — three surfaces · nothing else.
  - `GENERATION_REQUEST_FROM_UNLISTED_SURFACE_REFUSED: Final[bool] = True` — a surface not on the list has no Generated entries.

- **CON-8** · A content entry carries specific mandatory fields.
  - `CONTENT_ENTRY_MANDATORY_FIELDS: Final[tuple[str, ...]]` — 7-field ordered tuple per SRR statement.

- **CON-9** · A slot entry carries specific mandatory fields.
  - `SLOT_ENTRY_MANDATORY_FIELDS: Final[tuple[str, ...]]` — 5-field ordered tuple per SRR statement.
  - `SLOT_EMPTY_CANDIDATE_LIST_RENDERS_NOTHING: Final[bool] = True`.

- **CON-10** · The registry is read-only to every component except the ceremony engine.
  - `REGISTRY_READ_ONLY_EXCEPT_CEREMONY: Final[bool] = True` — templates, prompt versions, candidate lists, and ranking rule versions change only through ceremony.

- **CON-11** · An objective is mandatory on every entry.
  - `OBJECTIVE_MANDATORY: Final[bool] = True`.
  - `OBJECTIVE_MUST_BE_ONE_SENTENCE: Final[bool] = True` — an entry whose objective cannot be stated in one sentence is refused at ceremony.

## What is NOT touched (additive-only per SO §3.8)

- `services/content_registry/` package tree does not yet exist. This wave creates it net-new. Nothing sealed is edited.
- The FE surfaces are not touched by this wave (backend vocabulary registration only). FE consumption of the R-32 whitelist and the class enumeration comes later via specialist-dispatch when downstream FE waves open (precedent: R-87 FE-FIX-READY spec).

Canon anchors verbatim:
- Owner Ruling 4 (2026-09-20T~19:00Z · STATE/DECISIONS.md line 20421 anchor · re-affirmed `1250c39a` / `e40047f4` / `9823a520` / `80e42629`).
- Master Requirements Registry v5 System Rules Registry sheet (sha256 `00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d` · rows 566-576 for CON-1..CON-11) — ratified authority per Ruling 5.
- Content Registry Spec v1 custody docx at `custody/owner_drops/20260920T1600Z/Content_Registry_Spec_v1.docx` — cited for §-numbering only (§2 The Three Classes covers CON-1..CON-7; §3 The Registry covers CON-8..CON-11).
- Ruling 3 erratum discipline: "class column is a HINT · rule text governs" — SRR Enforcement Class column is empty for all 31 CON rows; classification derives from statement text.
- CP-BLOCKED-VOCABULARY-CORRECTION seal `200c2c63/b4526572/9823a520` (R-87 · establishes vocabulary-registration-via-Final-constants pattern this wave inherits).
- SO §2.5 verbatim-docstring · §3 tests-first · §3.3 3-Commit Seal · §3.8 additive-only · §3.10-α Final[...] closed-vocab.
"""

from __future__ import annotations

from typing import Final, List, Tuple


# ═══════════════════════════════════════════════════════════════════════════
# §2 The Three Classes · CON-1..CON-7
# ═══════════════════════════════════════════════════════════════════════════

# ── CON-1 · SRR row 566 · "Every string that reaches a surface belongs to
# exactly one content entry and exactly one class. A string with no entry
# does not render. Improvised copy — a component composing text outside
# the registry — is refused by the resolver."

#: CON-1 · three-class enumeration. Slot entries (CON-9) are a separate
#: concept — they reference candidate content entries but are not
#: themselves a class.
CONTENT_CLASSES: Final[Tuple[str, ...]] = ("Fixed", "Templated", "Generated")

#: CON-1 · grep-negative ban #1 (7-category bans · anchor). "Improvised
#: copy — a component composing text outside the registry — is refused
#: by the resolver."
IMPROVISED_COPY_REFUSED: Final[bool] = True

#: CON-1 · "A string with no entry does not render."
STRING_WITHOUT_ENTRY_DOES_NOT_RENDER: Final[bool] = True


# ── CON-2 · SRR row 567 · "Fixed entries render their text verbatim. The
# text is a contract; changing it is a contract-version change through
# the Rules Service ceremony at the ordinary tier."

#: CON-2 · Fixed class · verbatim rendering.
FIXED_RENDER_VERBATIM: Final[bool] = True

#: CON-2 · Fixed text is a contract; ceremony changes it, not code.
FIXED_TEXT_CHANGE_REQUIRES_CEREMONY: Final[bool] = True


# ── CON-3 · SRR row 568 · "Templated entries render only from named
# dependencies that resolve to verified fields. A Templated string
# contains no value that is not a dependency. The template is versioned;
# a version change is a contract-version change through ceremony."

#: CON-3 · Templated class · dependency-only rendering.
TEMPLATED_DEPENDENCIES_ONLY: Final[bool] = True

#: CON-3 · "A Templated string contains no value that is not a
#: dependency."
TEMPLATED_NO_VALUES_OUTSIDE_DEPENDENCIES: Final[bool] = True


# ── CON-4 · SRR row 569 · "Every Templated entry carries an honest-gap
# variant for each dependency that may be null. When a dependency is
# null, the variant renders. The template MUST NOT estimate, default,
# or infer a missing value."

#: CON-4 · honest-gap variant required per null-able dependency.
TEMPLATED_HONEST_GAP_VARIANT_REQUIRED: Final[bool] = True

#: CON-4 · "The template MUST NOT estimate, default, or infer a missing
#: value." — closed to inference, defaulting, or estimation on nulls.
TEMPLATED_MUST_NOT_ESTIMATE_DEFAULT_OR_INFER: Final[bool] = True


# ── CON-5 · SRR row 570 · "Generated entries carry a class ceiling of
# inference or advisory and never fact. Every sentence in a Generated
# string anchors to material by provenance reference; an unanchored
# sentence is refused by Solva's classing."

#: CON-5 · Generated class ceiling · SO §3.10-α Final[tuple] closed-vocab.
#: Two members only: "inference" · "advisory". Never "fact".
GENERATED_CLASS_CEILING_VALUES: Final[Tuple[str, ...]] = ("inference", "advisory")

#: CON-5 · "never fact" — the excluded class.
GENERATED_NEVER_FACT_CLASS: Final[bool] = True

#: CON-5 · every sentence anchors · unanchored sentence refused by
#: Solva's classing.
GENERATED_EVERY_SENTENCE_ANCHORS: Final[bool] = True


# ── CON-6 · SRR row 571 · "A number on any surface comes from a
# Templated dependency or a Fixed string. A Generated string MUST NOT
# introduce a number the surface does not already carry as a verified
# field. Prose may wrap a number, never mint one."

#: CON-6 · grep-negative ban #2 anchor · number sources are exactly two.
NUMBER_SOURCES_ALLOWED: Final[Tuple[str, ...]] = ("Templated", "Fixed")

#: CON-6 · Generated must not introduce a number the surface does not
#: already carry as a verified field. "Prose may wrap a number, never
#: mint one."
GENERATED_MUST_NOT_INTRODUCE_NUMBERS: Final[bool] = True


# ── CON-7 · SRR row 572 · "Which surfaces may carry Generated entries
# at all is a ruled list (R-32). A surface not on the list has no
# Generated entries, and a generation request from it is refused."

#: CON-7 · R-32 Generated surface whitelist · three surfaces · nothing
#: else. Owner-ratified. Matches CON-22 SRR statement byte-verbatim.
#: Any addition requires Canon 3 §24 4-step rule-change ceremony, not
#: a code edit.
R32_GENERATED_SURFACE_WHITELIST: Final[Tuple[str, ...]] = (
    "chat_answer",
    "recommendation_body",
    "notification_body",
)

#: CON-7 · a generation request from an unlisted surface is refused.
GENERATION_REQUEST_FROM_UNLISTED_SURFACE_REFUSED: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# §3 The Registry · CON-8..CON-11
# ═══════════════════════════════════════════════════════════════════════════

# ── CON-8 · SRR row 573 · "A content entry carries: entry identifier;
# surface; class; objective — one sentence stating what the string is
# for; template version or prompt version; dependencies, as named
# verified fields; honest-gap variants; ..."

#: CON-8 · content entry shape · 7 mandatory fields in order. Ordering
#: is stable per Final[tuple] discipline.
CONTENT_ENTRY_MANDATORY_FIELDS: Final[Tuple[str, ...]] = (
    "entry_identifier",
    "surface",
    "class",
    "objective",
    "template_version_or_prompt_version",
    "dependencies",
    "honest_gap_variants",
)


# ── CON-9 · SRR row 574 · "A slot entry carries: slot identifier;
# surface; ordered candidate list; ranking rule version; hold rule
# (§5). A slot with an empty candidate list renders nothing."

#: CON-9 · slot entry shape · 5 mandatory fields in order.
SLOT_ENTRY_MANDATORY_FIELDS: Final[Tuple[str, ...]] = (
    "slot_identifier",
    "surface",
    "ordered_candidate_list",
    "ranking_rule_version",
    "hold_rule",
)

#: CON-9 · empty candidate list renders nothing.
SLOT_EMPTY_CANDIDATE_LIST_RENDERS_NOTHING: Final[bool] = True


# ── CON-10 · SRR row 575 · "The registry is read-only to every component
# except the ceremony engine. Templates, prompt versions, candidate
# lists, and ranking rule versions change only through ceremony. A
# model, a wizard, or a subsystem MAY NOT edit the registry directly."

#: CON-10 · registry is read-only except for the ceremony engine.
REGISTRY_READ_ONLY_EXCEPT_CEREMONY: Final[bool] = True


# ── CON-11 · SRR row 576 · "An objective is mandatory on every entry.
# An entry whose objective cannot be stated in one sentence is refused
# at ceremony — a string nobody can say the purpose of is a string
# nobody can say is still needed."

#: CON-11 · objective mandatory on every entry.
OBJECTIVE_MANDATORY: Final[bool] = True

#: CON-11 · objective must be stateable in ONE sentence at ceremony.
OBJECTIVE_MUST_BE_ONE_SENTENCE: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# §4 The Resolver · CON-12..CON-14 (R-89 second slice)
# ═══════════════════════════════════════════════════════════════════════════

# ── CON-12 · SRR row 577 · "Rendering is a pure function of (entry, entry
# version, dependency values). For Fixed and Templated entries it returns
# the string. For Generated entries it returns a generation request
# carrying the prompt version, the class ceiling, the required anchors,
# and the dependencies the prose may reference — and the drafting
# component's output re-enters the resolver for classing and gating
# before it becomes a string. No parameter exists through which a
# learned component's output can alter what a Fixed or Templated entry
# renders."

#: CON-12 · rendering purity: pure function of the 3-tuple below.
RENDERING_IS_PURE_FUNCTION: Final[bool] = True

#: CON-12 · rendering input tuple · 3-field ordered per SRR statement
#: byte-order: (entry, entry version, dependency values).
RENDERING_INPUT_TUPLE: Final[Tuple[str, ...]] = (
    "entry",
    "entry_version",
    "dependency_values",
)

#: CON-12 · generation request shape · 4-field ordered per SRR statement
#: byte-order: (prompt_version, class_ceiling, required_anchors,
#: dependencies). Every Generated render produces one such request
#: which re-enters the resolver for classing and gating.
GENERATION_REQUEST_MANDATORY_FIELDS: Final[Tuple[str, ...]] = (
    "prompt_version",
    "class_ceiling",
    "required_anchors",
    "dependencies",
)

#: CON-12 · drafting output re-enters the resolver for classing and
#: gating before it becomes a string.
LEARNED_OUTPUT_REENTERS_RESOLVER: Final[bool] = True

#: CON-12 · closure clause: "No parameter exists through which a
#: learned component's output can alter what a Fixed or Templated
#: entry renders." (SO §3.10-α closed-vocab discipline anchor.)
LEARNED_CANNOT_ALTER_FIXED_OR_TEMPLATED_RENDER: Final[bool] = True


# ── CON-13 · SRR row 578 · "A learned component MAY propose a new
# template, a new candidate, or a re-ordering, through the research
# queue. The proposal is ratified by ceremony or it is nothing.
# Proposals never take effect on proposal."

#: CON-13 · learned components propose ONLY through the research queue.
LEARNED_PROPOSALS_VIA_RESEARCH_QUEUE: Final[bool] = True

#: CON-13 · "ratified by ceremony or it is nothing" — a proposal
#: without ceremony is not a change.
PROPOSAL_RATIFIED_BY_CEREMONY_OR_NOTHING: Final[bool] = True

#: CON-13 · "Proposals never take effect on proposal."
PROPOSALS_NEVER_TAKE_EFFECT_ON_PROPOSAL: Final[bool] = True


# ── CON-14 · SRR row 579 · "The resolver fails closed. A missing
# dependency renders the honest-gap variant; a missing entry renders
# nothing; a Generated string that fails classing or the gate is
# refused with the platform's one refusal card. Nothing is improvised
# to fill a space."

#: CON-14 · resolver fails closed on every ambiguity path.
RESOLVER_FAILS_CLOSED: Final[bool] = True

#: CON-14 · missing dependency → honest-gap variant renders (CON-4
#: dependency binding).
MISSING_DEPENDENCY_RENDERS_HONEST_GAP: Final[bool] = True

#: CON-14 · missing entry → nothing renders (CON-1 dependency binding).
MISSING_ENTRY_RENDERS_NOTHING: Final[bool] = True

#: CON-14 · Generated string that fails classing or the gate → refused
#: with the platform's ONE refusal card (single canonical card, not
#: per-surface variants).
GENERATED_FAILS_CLASSING_OR_GATE_REFUSED_WITH_ONE_REFUSAL_CARD: Final[bool] = True

#: CON-14 · closure clause: "Nothing is improvised to fill a space."
#: (CON-1 grep-negative ban #1 reinforcement.)
IMPROVISED_FILL_REFUSED: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# §5 The Slot Model · CON-15..CON-21 (R-89 second slice)
# ═══════════════════════════════════════════════════════════════════════════

# ── CON-15 · SRR row 580 · "Every candidate on a slot is assigned one
# salience class at render time, by the ranking rule, from its
# dependencies: Class 1 — a decision is required now (a job stopped at
# a limit, an approval pending on the reader, a ceiling or threshold
# crossed, a refusal the reader has not seen); Class 2 — something
# changed since the reader last saw this surface (a delta on a
# dependency, a status transition); Class 3 — an opportunity or capacity
# the reader can act on (room for more work, allowance available,
# resources idle); Class 4 — steady state (nothing pending, nothing
# changed, nothing to claim). The definitions are ruled (R-33) and
# versioned."

#: CON-15 · salience class count · exactly four classes per SRR
#: statement.
SALIENCE_CLASS_COUNT: Final[int] = 4

#: CON-15 · salience class canonical definitions · one-line per class
#: extracted byte-verbatim from SRR statement (semicolon-split).
SALIENCE_CLASS_DEFINITIONS: Final[Tuple[Tuple[int, str], ...]] = (
    (1, "a decision is required now"),
    (2, "something changed since the reader last saw this surface"),
    (3, "an opportunity or capacity the reader can act on"),
    (4, "steady state"),
)

#: CON-15 · R-33 ranking rule is ruled AND versioned (definitions
#: change only through Canon 3 §24 4-step rule-change ceremony).
RANKING_RULE_R33_VERSIONED: Final[bool] = True


# ── CON-16 · SRR row 581 · "The hook is the eligible candidate with
# the lowest salience class. Ties resolve by the candidate list's
# order, which is fixed in the slot entry. The ranking is
# deterministic: the same dependency values produce the same hook."

#: CON-16 · hook selection primary rule · lowest salience class
#: (Class 1 < Class 2 < Class 3 < Class 4).
HOOK_SELECTION_LOWEST_SALIENCE_CLASS: Final[bool] = True

#: CON-16 · hook tie-breaker · candidate list order (fixed in slot
#: entry per CON-9 SLOT_ENTRY_MANDATORY_FIELDS.ordered_candidate_list).
HOOK_TIES_RESOLVE_BY_CANDIDATE_LIST_ORDER: Final[bool] = True

#: CON-16 · ranking is deterministic · same dependency values → same
#: hook (no non-determinism, no randomness).
RANKING_IS_DETERMINISTIC: Final[bool] = True


# ── CON-17 · SRR row 582 · "An ineligible candidate — any dependency
# null — is never the hook while an eligible candidate exists in any
# class. If no candidate is eligible, the slot renders the honest-gap
# variant of the first-listed candidate. A gap is never headlined
# over a fact."

#: CON-17 · eligibility rule · any dependency null → candidate
#: ineligible.
INELIGIBLE_CANDIDATE_ANY_DEP_NULL: Final[bool] = True

#: CON-17 · eligibility precedence · ineligible candidate is NEVER
#: the hook while an eligible candidate exists in any class.
INELIGIBLE_CANDIDATE_NEVER_HOOK_WHILE_ELIGIBLE_EXISTS: Final[bool] = True

#: CON-17 · fallback rule · no eligible candidate → honest-gap variant
#: of the first-listed candidate renders.
NO_ELIGIBLE_RENDERS_FIRST_CANDIDATE_HONEST_GAP: Final[bool] = True

#: CON-17 · closure clause · "A gap is never headlined over a fact."
GAP_NEVER_HEADLINED_OVER_FACT: Final[bool] = True


# ── CON-18 · SRR row 583 · "No engagement measure — views, dwell,
# clicks, replies — and no learned signal enters the ranking rule.
# The rule reads verified fields only. Salience is about what the
# reader must know to decide, not what the reader is likely to look
# at."

#: CON-18 · grep-negative ban #3 (7-category bans) anchor · four
#: canonical forbidden engagement measures per SRR statement
#: byte-order.
ENGAGEMENT_SIGNALS_FORBIDDEN_IN_RANKING: Final[Tuple[str, ...]] = (
    "views",
    "dwell",
    "clicks",
    "replies",
)

#: CON-18 · no learned signal enters the ranking rule (parallel to
#: engagement-signal ban).
LEARNED_SIGNALS_FORBIDDEN_IN_RANKING: Final[bool] = True

#: CON-18 · positive rule statement · ranking rule reads verified
#: fields only.
RANKING_RULE_READS_VERIFIED_FIELDS_ONLY: Final[bool] = True


# ── CON-19 · SRR row 584 · "A hook holds until a candidate of a lower
# class becomes eligible or the hook's own dependencies change. A slot
# does not flap between candidates of equal class on unrelated
# updates. Hold values are ruled (R-34)."

#: CON-19 · hook-hold rule · hook holds until lower class eligible
#: OR hook's own dependencies change.
HOOK_HOLDS_UNTIL_LOWER_CLASS_ELIGIBLE_OR_DEPS_CHANGE: Final[bool] = True

#: CON-19 · anti-flap · no flap between candidates of equal class on
#: unrelated updates.
NO_FLAP_ON_UNRELATED_UPDATES: Final[bool] = True

#: CON-19 · R-34 · hold values are ruled AND versioned (change through
#: ceremony only).
HOLD_VALUES_RULED_R34: Final[bool] = True


# ── CON-20 · SRR row 585 · "Choosing a hook writes a content receipt
# carrying the salience trace: every candidate, its class, its
# eligibility, and the rule version. The surface exposes the trace on
# demand — 'why this first' — so a reader or overseer can see what
# the slot chose not to lead with."

#: CON-20 · hook choice writes a content receipt.
HOOK_CHOICE_WRITES_CONTENT_RECEIPT: Final[bool] = True

#: CON-20 · content receipt carries the salience trace.
CONTENT_RECEIPT_CARRIES_SALIENCE_TRACE: Final[bool] = True

#: CON-20 · salience trace per-candidate shape · 4-field ordered per
#: SRR statement byte-order: (candidate, class, eligibility, rule_version).
SALIENCE_TRACE_FIELDS: Final[Tuple[str, ...]] = (
    "candidate",
    "class",
    "eligibility",
    "rule_version",
)

#: CON-20 · surface exposes trace on demand ("why this first").
SURFACE_EXPOSES_TRACE_ON_DEMAND: Final[bool] = True


# ── CON-21 · SRR row 586 · "A hook is advisory. It directs attention;
# it never gates an action, and a component MUST NOT treat the hook's
# class as an input to any decision the platform makes."

#: CON-21 · hook is advisory · directs attention only.
HOOK_IS_ADVISORY: Final[bool] = True

#: CON-21 · hook never gates an action.
HOOK_NEVER_GATES_ACTION: Final[bool] = True

#: CON-21 · closure clause · hook class MUST NOT be an input to any
#: decision the platform makes (SO §3.10-α closed-vocab discipline
#: for the hook-class output surface).
HOOK_CLASS_NOT_INPUT_TO_PLATFORM_DECISION: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# §6 The Generated Path · CON-22 (R-90 third slice)
# ═══════════════════════════════════════════════════════════════════════════

# ── CON-22 · SRR row 587 · "A chat answer, a recommendation body, or a
# notification body is a Generated entry on a surface R-32 permits. It
# passes Solva's classing, the A5.15 gate, and — where it recommends an
# action — carries A5.16 provenance. Within it, findings are ordered by
# the same salience classes as §5, applied by the resolver to the
# anchored findings before the drafting component composes prose
# around them. The model writes the sentences; it does not choose the
# order."

#: CON-22 · Generated findings on R-32 surfaces are ordered by §5
#: salience classes BEFORE the drafting component composes prose.
GENERATED_R32_SURFACES_ORDERED_BY_SALIENCE: Final[bool] = True

#: CON-22 · resolver orders anchored findings by salience-class before
#: drafting component composes prose (see §5 CON-15 salience classes).
GENERATED_RESOLVER_ORDERS_FINDINGS_BEFORE_DRAFTING: Final[bool] = True

#: CON-22 · closure clause · "The model writes the sentences; it does
#: not choose the order." — the model has NO ordering authority.
GENERATED_MODEL_WRITES_SENTENCES_NOT_ORDER: Final[bool] = True

#: CON-22 · Generated-string gate chain · ordered per SRR statement
#: byte-order: Solva classing → A5.15 gate → A5.16 provenance
#: (last only where the string recommends an action).
GENERATED_GATES: Final[Tuple[str, ...]] = (
    "solva_classing",
    "a5_15_gate",
    "a5_16_provenance_where_recommends_action",
)


# ═══════════════════════════════════════════════════════════════════════════
# §7 Storage & Persistence · CON-23..CON-26 (R-90 third slice)
# ═══════════════════════════════════════════════════════════════════════════

# ── CON-23 · SRR row 588 · "A displayed Generated string is stored as
# an artefact by hash with: class, anchors, prompt version, model
# identity and version (A5.7+, V-4), the content receipt. It is
# retrievable by hash for as long as the retention rule holds (R-35).
# A reader may see the anchors of any Generated string on demand."

#: CON-23 · displayed Generated string stored as artefact by hash
#: (audit + retrieval, NOT for re-render input · see CON-26 ban #6).
GENERATED_STRING_STORED_AS_ARTEFACT_BY_HASH: Final[bool] = True

#: CON-23 · Generated artefact mandatory fields · 5-field ordered
#: per SRR statement byte-order.
GENERATED_ARTEFACT_MANDATORY_FIELDS: Final[Tuple[str, ...]] = (
    "class",
    "anchors",
    "prompt_version",
    "model_identity_and_version",
    "content_receipt",
)

#: CON-23 · artefact retrievable by hash for as long as R-35
#: retention rule holds.
GENERATED_ARTEFACT_RETRIEVABLE_BY_HASH: Final[bool] = True

#: CON-23 · retention rule anchor (R-35 · ruled + versioned).
GENERATED_RETENTION_RULE_R35: Final[bool] = True

#: CON-23 · reader-visibility rule · "A reader may see the anchors of
#: any Generated string on demand."
READER_MAY_SEE_ANCHORS_ON_DEMAND: Final[bool] = True


# ── CON-24 · SRR row 589 · "A Generated string that would state a
# fact the anchors do not support is refused before display, not
# softened. Softening — hedging an unsupported claim into plausibility
# — is the slop this document exists to prevent, and A5.5 already
# forbids the silent downgrade it amounts to."

#: CON-24 · refusal-before-display rule (unsupported facts refused
#: BEFORE render · NOT softened into plausibility).
GENERATED_UNSUPPORTED_FACT_REFUSED_BEFORE_DISPLAY: Final[bool] = True

#: CON-24 · grep-negative ban #4 anchor · softening (hedging an
#: unsupported claim into plausibility) is forbidden.
SOFTENING_IS_FORBIDDEN: Final[bool] = True

#: CON-24 · grep-negative ban #7 anchor · unsupported claims are
#: forbidden (refused before display).
UNSUPPORTED_CLAIMS_FORBIDDEN: Final[bool] = True

#: CON-24 · A5.5 binding · silent downgrade of an unsupported claim
#: is forbidden.
A5_5_BINDING_FORBIDS_SILENT_DOWNGRADE: Final[bool] = True


# ── CON-25 · SRR row 590 · "A Templated string is not stored as text.
# Its content receipt records template version and dependency values
# by reference; the string is re-derived on demand (CON-12). Storing
# the text would create a second copy that can disagree with its own
# inputs."

#: CON-25 · grep-negative ban #5 anchor · Templated string NOT stored
#: as text (only its content receipt with template_version +
#: dependency_values_by_reference).
TEMPLATED_STRING_NOT_STORED_AS_TEXT: Final[bool] = True

#: CON-25 · Templated content receipt shape (not the text itself).
TEMPLATED_CONTENT_RECEIPT_STORES_TEMPLATE_VERSION_AND_DEPENDENCY_VALUES_BY_REFERENCE: Final[bool] = True

#: CON-25 · Templated string re-derived on demand per CON-12 pure
#: function.
TEMPLATED_STRING_REDERIVED_ON_DEMAND: Final[bool] = True

#: CON-25 · rationale · "Storing the text would create a second copy
#: that can disagree with its own inputs."
STORING_TEMPLATED_TEXT_CREATES_DIVERGENCE_RISK: Final[bool] = True


# ── CON-26 · SRR row 591 · "A Generated string is stored per CON-23.
# A Fixed string is stored once, as the contract. A hook choice is
# stored as its trace (CON-20)."

#: CON-26 · Fixed string stored once as the contract text (single
#: canonical source · ceremony-changed).
FIXED_STRING_STORED_ONCE_AS_CONTRACT: Final[bool] = True

#: CON-26 · hook-choice stored as its trace per CON-20 salience trace.
HOOK_CHOICE_STORED_AS_TRACE_PER_CON_20: Final[bool] = True

#: CON-26 · grep-negative ban #6 anchor · Generated text stored as
#: artefact-by-hash (CON-23) BUT NEVER stored as an input to a
#: subsequent render (avoids downgrade of Generated-as-provenance
#: into pseudo-Fact).
GENERATED_TEXT_NOT_STORED_AS_INPUT_TO_SUBSEQUENT_RENDER: Final[bool] = True

#: CON-26 · storage rule summary by class · 3-pair ordered tuple
#: (Fixed → once-as-contract · Templated → not-as-text (CON-25) ·
#: Generated → as-artefact-by-hash (CON-23)).
STORAGE_RULES_BY_CLASS: Final[Tuple[Tuple[str, str], ...]] = (
    ("Fixed", "stored_once_as_contract"),
    ("Templated", "not_stored_as_text"),
    ("Generated", "stored_as_artefact_by_hash"),
)


# ═══════════════════════════════════════════════════════════════════════════
# §8 Erasure & Retention · CON-27..CON-28 (R-90 third slice)
# ═══════════════════════════════════════════════════════════════════════════

# ── CON-27 · SRR row 592 · "Erasure reaches Generated artefacts. When
# a unit's rights are withdrawn, every Generated artefact whose anchors
# cite it is found by provenance and recalled or re-derived without
# it, on the mechanism DAP-38 and MEM-9 already define."

#: CON-27 · erasure reaches Generated artefacts (not siloed away).
ERASURE_REACHES_GENERATED_ARTEFACTS: Final[bool] = True

#: CON-27 · withdrawal triggers a provenance-driven anchor trace to
#: find every affected Generated artefact.
WITHDRAWAL_TRIGGERS_ANCHOR_TRACE: Final[bool] = True

#: CON-27 · affected Generated artefact recalled OR re-derived
#: without the withdrawn unit.
GENERATED_ARTEFACT_RECALLED_OR_REDERIVED_WITHOUT_WITHDRAWN_UNIT: Final[bool] = True

#: CON-27 · erasure mechanism authority · DAP-38 + MEM-9 (2-tuple
#: byte-verbatim from SRR statement).
ERASURE_MECHANISM_DAP_38_AND_MEM_9: Final[Tuple[str, ...]] = ("DAP-38", "MEM-9")


# ── CON-28 · SRR row 593 · "Retention of Generated artefacts follows
# a ruled default (R-35) and is subject to erasure precedence, on
# MEM-9's rule."

#: CON-28 · retention default is R-35 (owner-ruled + versioned).
RETENTION_DEFAULT_R35: Final[bool] = True

#: CON-28 · erasure precedence over retention per MEM-9 rule.
ERASURE_PRECEDENCE_OVER_RETENTION_PER_MEM_9: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# §9 Freshness · CON-29..CON-31 (R-90 third slice)
# ═══════════════════════════════════════════════════════════════════════════

# ── CON-29 · SRR row 594 · "A Templated entry re-renders when any
# dependency changes. Dependency changes are the Ledger's own events —
# metered events, status transitions, receipts — so a surface is
# current to the record without a scheduler for any dependency that
# emits an event."

#: CON-29 · Templated entry re-renders when ANY dependency changes.
TEMPLATED_RERENDERS_ON_ANY_DEPENDENCY_CHANGE: Final[bool] = True

#: CON-29 · Ledger event types that trigger re-render · 3-tuple
#: byte-verbatim from SRR statement (metered_events · status_transitions
#: · receipts).
LEDGER_EVENT_TYPES_TRIGGERING_RERENDER: Final[Tuple[str, ...]] = (
    "metered_events",
    "status_transitions",
    "receipts",
)

#: CON-29 · scheduler NOT needed for any dependency that emits an
#: event (event-driven freshness).
SCHEDULER_NOT_NEEDED_FOR_EVENT_EMITTING_DEPENDENCY: Final[bool] = True


# ── CON-30 · SRR row 595 · "A schedule exists only for an entry with
# a dependency that emits no event. The schedule and its interval are
# recorded on the entry. A scheduled entry displays its as-of time."

#: CON-30 · schedule exists ONLY for entries with non-event
#: dependencies (bounded scope).
SCHEDULE_ONLY_FOR_ENTRY_WITH_NON_EVENT_DEPENDENCY: Final[bool] = True

#: CON-30 · schedule + interval recorded ON THE ENTRY (not in a
#: sidecar · single source of truth).
SCHEDULED_ENTRY_RECORDS_SCHEDULE_AND_INTERVAL_ON_ENTRY: Final[bool] = True

#: CON-30 · scheduled entry MUST display its as-of time (visibility
#: of freshness).
SCHEDULED_ENTRY_DISPLAYS_AS_OF_TIME: Final[bool] = True


# ── CON-31 · SRR row 596 · "If a trigger source is unreachable, the
# last rendered string displays with a visible stale marker and its
# as-of time. It is never silently held as current — the one
# degradation this platform permits, marked as the Browse census
# already is."

#: CON-31 · unreachable trigger source → last render displays with
#: STALE marker.
UNREACHABLE_TRIGGER_DISPLAYS_STALE_MARKER: Final[bool] = True

#: CON-31 · stale marker requirements · visible indicator + as-of
#: time (both required for the marker to count as staleness signal).
STALE_MARKER_REQUIRES_VISIBLE_INDICATOR_AND_AS_OF_TIME: Final[bool] = True

#: CON-31 · silent hold of a stale value as current is forbidden.
SILENT_HOLD_AS_CURRENT_FORBIDDEN: Final[bool] = True

#: CON-31 · stale-marking is the ONE degradation this platform
#: permits (SO §3.10-α closed-vocab discipline · Browse census is
#: the reference example).
STALE_MARKING_IS_THE_ONE_DEGRADATION_PERMITTED: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# Pure-data-in scanner helpers (additive-only · aid grep-negative sweeps)
# ═══════════════════════════════════════════════════════════════════════════

def scan_for_improvised_copy_patterns(text: str) -> List[Tuple[int, str]]:
    """CON-1 grep-negative helper · pure-data-in scanner returning a list
    of (line_no, matched_pattern) hits for a given text buffer.

    Callers (downstream slice authors · reviewers) pass a file body and
    receive the hit list. Empty list = clean · non-empty list =
    nonconformant.

    Watched patterns (heuristic layer only · not exhaustive · downstream
    slices extend the set):

    - `render_text(` — direct text-composition outside registry.
    - `format_string(` — free-form string composition.
    - `template_literal_render(` — bypassing registry.

    Signature is intentionally pure-data-in: no filesystem access, no
    logging, no side effects. Line numbers are 1-based to match editor
    conventions.
    """
    hits: List[Tuple[int, str]] = []
    watched = (
        "render_text(",
        "format_string(",
        "template_literal_render(",
    )
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in watched:
            if pattern in line:
                hits.append((lineno, pattern))
    return hits


def scan_for_generated_number_introduction(text: str) -> List[Tuple[int, str]]:
    """CON-6 grep-negative helper · pure-data-in scanner for patterns
    that would introduce a number in a Generated string without a
    Templated/Fixed anchor.

    Watched patterns (heuristic layer only):
    - `mint_number(` — direct number introduction.
    - `synthesize_figure(` — figure synthesis.
    - `estimate_value(` — estimation.

    Any hit indicates a candidate CON-6 violation. Not proof — the
    reviewer confirms the caller context.
    """
    hits: List[Tuple[int, str]] = []
    watched = (
        "mint_number(",
        "synthesize_figure(",
        "estimate_value(",
    )
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in watched:
            if pattern in line:
                hits.append((lineno, pattern))
    return hits


def scan_for_engagement_signals_in_ranking(text: str) -> List[Tuple[int, str]]:
    """CON-18 grep-negative helper (7-category ban #3 anchor) ·
    pure-data-in scanner for patterns that would import an engagement
    measure or learned signal into a ranking-rule code path.

    Watched patterns (heuristic layer · SRR statement byte-verbatim
    engagement measures + learned-signal families the ranking rule
    MUST NOT read):

    - `views_count(`
    - `dwell_seconds(`
    - `click_rate(`
    - `reply_rate(`
    - `learned_score(`
    - `engagement_score(`
    - `predicted_ctr(`

    Any hit inside a call chain rooted at a ranking-rule function is a
    candidate CON-18 violation. Not proof — the reviewer confirms the
    caller context. Callers pass a file body and receive the hit list.
    Empty list = clean.

    Signature is intentionally pure-data-in: no filesystem access, no
    logging, no side effects. Line numbers are 1-based to match editor
    conventions.
    """
    hits: List[Tuple[int, str]] = []
    watched = (
        "views_count(",
        "dwell_seconds(",
        "click_rate(",
        "reply_rate(",
        "learned_score(",
        "engagement_score(",
        "predicted_ctr(",
    )
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in watched:
            if pattern in line:
                hits.append((lineno, pattern))
    return hits


def scan_for_softening_of_unsupported_claims(text: str) -> List[Tuple[int, str]]:
    """CON-24 grep-negative helper (7-category ban #4 anchor) ·
    pure-data-in scanner for patterns that would soften an unsupported
    claim into plausibility (the slop CON-24 exists to prevent).

    Watched patterns (heuristic layer · softening families):

    - `soften_claim(`
    - `hedge_claim(`
    - `downgrade_confidence(`
    - `approximate_as(`
    - `roughly_state(`

    Any hit indicates a candidate CON-24 violation. Not proof — the
    reviewer confirms the caller context. Callers pass a file body and
    receive the hit list. Empty list = clean.
    """
    hits: List[Tuple[int, str]] = []
    watched = (
        "soften_claim(",
        "hedge_claim(",
        "downgrade_confidence(",
        "approximate_as(",
        "roughly_state(",
    )
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in watched:
            if pattern in line:
                hits.append((lineno, pattern))
    return hits


def scan_for_unsupported_claim_state(text: str) -> List[Tuple[int, str]]:
    """CON-24 grep-negative helper (7-category ban #7 anchor) ·
    pure-data-in scanner for patterns that would state a claim
    without an anchor/provenance.

    Watched patterns (heuristic layer · unsupported-claim families):

    - `state_without_anchor(`
    - `assert_unsupported(`
    - `claim_without_provenance(`
    - `fact_without_source(`

    Any hit indicates a candidate CON-24 violation. Not proof — the
    reviewer confirms the caller context.
    """
    hits: List[Tuple[int, str]] = []
    watched = (
        "state_without_anchor(",
        "assert_unsupported(",
        "claim_without_provenance(",
        "fact_without_source(",
    )
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in watched:
            if pattern in line:
                hits.append((lineno, pattern))
    return hits


def scan_for_templated_text_storage(text: str) -> List[Tuple[int, str]]:
    """CON-25 grep-negative helper (7-category ban #5 anchor) ·
    pure-data-in scanner for patterns that would store a Templated
    string as text (violating CON-25's "not stored as text" rule).

    Watched patterns (heuristic layer · templated-text-storage families):

    - `store_templated_text(`
    - `cache_rendered_template(`
    - `persist_rendered_string(`
    - `save_template_output(`

    Any hit indicates a candidate CON-25 violation. Not proof — the
    reviewer confirms the caller context.
    """
    hits: List[Tuple[int, str]] = []
    watched = (
        "store_templated_text(",
        "cache_rendered_template(",
        "persist_rendered_string(",
        "save_template_output(",
    )
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in watched:
            if pattern in line:
                hits.append((lineno, pattern))
    return hits


def scan_for_generated_text_as_render_dependency(text: str) -> List[Tuple[int, str]]:
    """CON-26 grep-negative helper (7-category ban #6 anchor) ·
    pure-data-in scanner for patterns that would use a stored
    Generated string as an INPUT to a subsequent render (violating
    CON-26's ban on Generated text becoming a render dependency ·
    Generated storage per CON-23 is for audit/retrieval only).

    Watched patterns (heuristic layer · generated-as-dependency families):

    - `use_generated_as_dependency(`
    - `consume_generated_string_as_input(`
    - `generated_as_template_variable(`
    - `inject_generated_into_template(`

    Any hit indicates a candidate CON-26 violation. Not proof — the
    reviewer confirms the caller context.
    """
    hits: List[Tuple[int, str]] = []
    watched = (
        "use_generated_as_dependency(",
        "consume_generated_string_as_input(",
        "generated_as_template_variable(",
        "inject_generated_into_template(",
    )
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in watched:
            if pattern in line:
                hits.append((lineno, pattern))
    return hits
