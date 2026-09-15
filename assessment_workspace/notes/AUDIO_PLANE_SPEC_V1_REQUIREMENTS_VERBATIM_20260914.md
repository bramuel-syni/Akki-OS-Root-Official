READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# AUDIO_PLANE_SPEC_V1_REQUIREMENTS_VERBATIM_20260914.md

**Source doc:** `Akki_OS_Audio_Intelligence_Plane_Specification_v1_0.docx` · sha256 `b6ad57b369ad3125f25a81f0790d5226a7630206092ea096023d04650cbe43a9` · 26,623 B · downloaded 2026-09-15T01:41:13Z.
**Parallel .md rendering:** `Audio_Intelligence_Plane.md` · sha256 `c8ee75ae756004af5dd68d48b94376f3b9005aaf5ee3f413ed456566d2da2c5e` · 30,767 B · PARITY_TRUE (34/34 probes).
**Structured extract:** `canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec_STRUCTURED.txt` — 253 lines · last paragraph P253 · table rows preserved verbatim.
**Self-declared status (P005 verbatim):** *"consolidated build specification. It supersedes the working drafts (Audio Capability Spec v1.0 and Addendum v1.1.2) and is the single reference for build."*
**Discipline anchor:** DECISIONS.md 2026-09-15T~01:40Z (Verbatim-canon discipline).

**Row format:** `RowID · verbatim quote · paragraph anchor · classification`. Classification ∈ {`definition`, `rule`, `prohibition`, `flow-step`, `capability-spec`, `contract-cell`, `open-decision`, `verify-item`, `prose`, `heading`}.

---

## §Preamble (P001..P005)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V01 | *"SYNI.AI   ·   ENGINEERING SPECIFICATION"* | P001 | prose |
| V02 | *"The Audio Intelligence Plane"* | P002 · title | prose |
| V03 | *"Extraction · Learning · Training · Invention — end to end"* | P003 · subtitle | prose (four-function loop) |
| V04 | *"Including the Commission View surface adjustment across all extraction types · v1.0"* | P004 · subtitle | prose |
| V05 | *"Status of this document: consolidated build specification. It supersedes the working drafts (Audio Capability Spec v1.0 and Addendum v1.1.2) and is the single reference for build. Behavioural clauses state what the system must and must not do, including on failure. Technical clauses state contracts and acceptance criteria. Items requiring verification against current code before build are marked [VERIFY] and collected in §16."* | P005 | rule (supersession + build-reference status + [VERIFY] convention) |

## §1 · Governing Doctrine (P010..P021)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V06 | *"Five principles govern every clause in this specification. Where a later clause appears to conflict with one of these, the principle wins and the clause is defective."* | P011 | rule (principle-supremacy) |
| V07 · §1.1 | *"An audio file is a data estate, and the framing is recursive"* | P012 · Heading3 | heading |
| V08 · §1.1 | *"The archive is an estate; a programme is an estate; a single file is an estate. Segments are rows; the extractable layers — content, language, condition, prosody, occurrence, code-switch, music, group-level character — are columns; no schema exists until one is declared. Census, admission, registry, and record apply at every scale."* | P013 | rule (recursive framing) |
| V09 · §1.2 | *"Modality extension, not parallel machinery"* | P014 · Heading3 | heading |
| V10 · §1.2 | *"The audio plane introduces no sibling services. Mtafiti gains an audio modality; Northena gains audio data classes; the wizard gains an objective variant; Targeta gains a training object. Anything in this document that reads as a parallel to an existing service is rule proliferation and must be collapsed into the existing service before build."* | P015 | rule (extension-not-proliferation; anti-sibling) |
| V11 · §1.3 | *"One record"* | P016 · Heading3 | heading |
| V12 · §1.3 | *"Mtafiti and Northena collaborate to produce a single record, written once. Working state — loss curves, intermediate metrics, partial coverage counts — is scratch, not truth; it becomes record only when finalized and stamped. No local ledger exists. If a measured throughput ceiling ever demands relief, the relief is batched stamping (one row certifying N events with a digest), which remains a single record. That change is made only when a measurement demands it."* | P017 | rule (one-record doctrine · no local ledger · batched-stamping only on measured relief) |
| V13 · §1.4 | *"Measure, do not assert"* | P018 · Heading3 | heading (load-bearing) |
| V14 · §1.4 | *"No data-volume requirement, accuracy expectation, or cost figure is quoted without a measurement behind it. The calibration stage exists to convert assertions into measurements before commitment."* | P019 | rule (measure-not-assert) |
| V15 · §1.5 | *"Unrepresentable, not policed"* | P020 · Heading3 | heading |
| V16 · §1.5 | *"Safety boundaries are enforced by making the violating state impossible to express in the contract — the pattern established by the assertion floor — not by review after the fact. The Character Register write path (§6) and the voice identity distance gate (§7) both follow this pattern."* | P021 | rule (unrepresentable-not-policed) |

## §2 · Capability Statement and Plane Overview (P022..P035)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V17 | *"Given governed access to an audio estate, the plane provides four functions in one loop:"* | P023 | rule (four-function loop preamble) |
| V18 | *"Extraction — audio is converted into provenance-paired facts: transcripts, entities, occurrences, and character observations."* | P024 | capability-spec (function 1) |
| V19 | *"Learning — a Character Register accumulates group-level knowledge of how the estate's languages and audio behave."* | P025 | capability-spec (function 2) |
| V20 | *"Training — model production is commissioned against a falsifiable Target Outcome, planned and priced before compute is spent, with per-example provenance."* | P026 | capability-spec (function 3) |
| V21 | *"Invention — synthesized voice identities are constructed from the register: authentically of the language, provably of no individual."* | P027 | capability-spec (function 4) |
| V22 | *"Each function feeds the next: extraction populates the register; the register defines the strata training plans against; trained models improve extraction; invention consumes the register's learned layers. The loop is the capability."* | P029 | rule (loop-is-the-capability) |
| V23 | *"Flow of a commission, end to end:"* | P030 | prose |
| V24 | *"Objective Wizard session → compile {TargetOutcome, Collection Schema}"* | P031 | flow-step |
| V25 | *"→ Sampling & Reflection (calibration) → proposed Milestones + priced quote"* | P032 | flow-step |
| V26 | *"→ Owner agrees milestones → Commission opens"* | P033 | flow-step |
| V27 | *"→ Collection → Register update → Curriculum → Training runs → Certificates"* | P034 | flow-step |
| V28 | *"→ Commission View reports against milestones throughout → Commission sealed"* | P035 | flow-step |

## §3 · Tokenized Audio Representation (P036..P056)

### §3.1 · Behaviour (P037..P041)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V29 | *"All downstream audio work — extraction, character analysis, training — operates on discrete token sequences produced by a neural audio codec, not on waveforms."* | P038 | rule (tokens-not-waveforms) |
| V30 | *"Tokenization exposes two separable streams per segment: the content stream (what was said — input to ASR/NER) and the character stream (how it was said — input to the Character Register). The character stream is retained and routed, never discarded as noise."* | P039 | rule (two-stream contract; content stream + character stream; both retained) |
| V31 | *"Control markers (language, register, segment type) are splice-able tokens, enabling one model per estate rather than one per language, and native handling of code-switched speech."* | P040 | rule (splice-able control markers; one-model-per-estate; native code-switch) |
| V32 | *"Failure behaviour: audio in an unsupported condition fails closed with a stated reason. The codec never silently degrades quality."* | P041 | rule (fail-closed-with-stated-reason; no-silent-degrade) |

### §3.2 · Technical contract (P042..P051)

| Row | Contract item (verbatim) | Specification (verbatim) | Anchor | Classification |
|---|---|---|---|---|
| V33 | *"Service"* | *"perception/audio_codec/ — registered like any other perception model; census-visible; runs in-perimeter on tenant compute."* | P045 · TABLE-ROW-02 | contract-cell (service path · in-perimeter compute) |
| V34 | *"Input"* | *"Audio segment (bounds per ingestion segmentation) + declared or detected condition profile."* | P046 · TABLE-ROW-03 | contract-cell |
| V35 | *"Output"* | *"{ content_tokens[], character_stream, codec_version } · Target token rate 50–100 tokens/second of audio."* | P047 · TABLE-ROW-04 | contract-cell (output shape + token-rate target) |
| V36 | *"Provenance"* | *"codec_version is a mandatory field of every downstream artifact's provenance. A transcript states which codec produced its tokens."* | P048 · TABLE-ROW-05 | contract-cell (codec_version mandatory) |
| V37 | *"Pretraining"* | *"The codec pretrains unsupervised on unlabelled estate audio, under the standard commissioned-job contract."* | P049 · TABLE-ROW-06 | contract-cell |
| V38 | *"[VERIFY]"* | *"Perception router contract: where model registration occurs, and whether the router carries a second output stream per segment or the character stream requires its own artifact type."* | P050 · TABLE-ROW-07 | verify-item |

### §3.3 · Acceptance criteria (P053..P056)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V39 | *"Round-trip fidelity is measured and recorded per codec version before that version serves any commission."* | P054 | rule (per-version fidelity measurement) |
| V40 | *"A downstream artifact lacking codec_version in provenance is rejected at the registry boundary."* | P055 | rule (registry-boundary rejection) |
| V41 | *"An unsupported-condition input produces a refusal with a stated reason and no output artifact."* | P056 | rule (refuse-with-stated-reason) |

## §4 · Extraction Layer (P057..P075)

### §4.1 · Language identification (P058..P063)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V42 | *"Behaviour: every segment carries a real language signal. The current plumbing value (language_hint: None) is retired."* | P059 | rule (language_hint: None is retired) |
| V43 | *"A lightweight offline language identifier (CPU-viable, in-perimeter) runs at segment level during ingestion."* | P060 | capability-spec (CPU-viable · in-perimeter · segment-level · ingestion) |
| V44 | *"Recorded per segment: languages[], confidences, and code-switch points where multiple languages occur in one utterance."* | P061 | rule (per-segment shape: languages[] + confidences + switch points) |
| V45 | *"The signal routes downstream model selection (ASR path, NER path, de-identification path) and is written into provenance."* | P062 | rule (LID routes downstream model selection) |
| V46 | *"[VERIFY] Segment boundaries in current ingestion — confirm the unit to which a language label attaches."* | P063 | verify-item |

### §4.2 · Code-switch points as facts (P064..P065)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V47 | *"Switch points (position, from-language, to-language, context class) are registered facts with provenance — not preprocessing metadata. They populate the register's code-switch layer and stratify test sets."* | P065 | rule (four switch-point fields · facts-not-metadata) |

### §4.3 · Condition profiling (P066..P067)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V48 | *"Channel condition — studio / field / telephone band, transmission artefacts, background class — is derived per segment at first ingestion. It is cheap to compute, directly predictive of extraction error, and required for training stratification. It is captured at first ingestion because re-ingesting an estate to recover it is the unaffordable mistake."* | P067 | rule (condition-profile captured-at-first-ingestion · unaffordable-to-defer) |

### §4.4 · Synthesis-relevant attribute capture (P068..P069)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V49 | *"During the same ingestion pass, group-level acoustic attributes required by any future synthesis capability (pitch statistics, energy contours, duration patterns) are captured, subject to the custody conditions of §6.4. This forecloses nothing and costs little; omitting it forecloses the invention function or forces re-ingestion."* | P069 | rule (synthesis-substrate capture at same-pass; subject to §6.4) |

### §4.5 · Deduplication as augmentation (P070..P071)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V50 | *"The occurrence index already identifies repeated content. Its output contract is extended: for each deduplicated item, the instance condition map — the set of channel/time/condition variants under which identical content occurred — is retained. One canonical extraction is stored; the variant set enters training curricula as a designated robustness stratum at zero acquisition cost. No new detection work; this is a change to what dedup keeps."* | P071 | rule (dedup instance-condition-map contract extension) |

### §4.6 · Acceptance criteria (P072..P075)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V51 | *"No segment leaves ingestion without languages[], condition profile, and (where applicable) switch points in provenance."* | P073 | rule (three-carrier ingestion invariant) |
| V52 | *"A deduplicated item without its instance condition map fails the ingestion invariant test."* | P074 | rule (dedup + instance-condition-map invariant) |
| V53 | *"Baseline-tier capture (§9.2) runs for all admitted material regardless of any active objective."* | P075 | rule (baseline capture is unconditional) |

## §5 · The Character Register — Learning (P076..P089)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V54 · §5.1 | *"A registry-modality store of learned, group-level audio characteristics, built from the character stream. Same doctrine as the fact registry: every entry carries provenance to source material and an occurrence count. It is Mtafiti's qualification-and-index doctrine applied to acoustic observations — an extension, not a sibling (§1.2)."* | P078 | definition (Character Register) |
| V55 · §5.2 layer-1 | *"Phonetic ⎢ Per-lexeme pronunciation variants, frequency, regional distribution. ⎢ Curriculum; extraction lexicons; evaluation stratification"* | P082 · TABLE-ROW-02 | contract-cell |
| V56 · §5.2 layer-2 | *"Prosodic ⎢ Intonation contours, stress, rate distributions, pause structure. ⎢ Training; programme-type classification"* | P083 · TABLE-ROW-03 | contract-cell |
| V57 · §5.2 layer-3 | *"Condition ⎢ Channel and environment profiles. ⎢ Stratification; error prediction"* | P084 · TABLE-ROW-04 | contract-cell |
| V58 · §5.2 layer-4 | *"Code-switch ⎢ Switch-point patterns, language pairs, context classes. ⎢ Training; test-set design"* | P085 · TABLE-ROW-05 | contract-cell |
| V59 · §5.3 | *"Unsupervised clustering over the character stream yields candidate strata. A cluster asserts that a distinct variant exists — not what it is called. Naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost."* | P089 | rule (unsupervised clustering + commissioned human naming) |

## §6 · Register Custody Boundary (P090..P102)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V60 · §6.1 | *"Organic characteristics are anatomical — vocal tract length, formant structure, glottal source, fundamental frequency range. They cannot be acquired or shed; they are what speaker verification keys on; they are biometric. They are never registered."* | P092 | prohibition (organic characteristics never registered) |
| V61 · §6.1 | *"Learned characteristics are acquired from a speech community — phonological inventory, pronunciation variants, prosody, code-switching habits. They are group properties by construction. Only learned characteristics may be registered."* | P093 | rule (only learned may be registered) |
| V62 · §6.2 cond-1 | *"Acquired, not anatomical. The attribute is learnable by a speaker from a different background."* | P095 | rule (condition 1) |
| V63 · §6.2 cond-2 | *"Shared. Observed across at least N distinct speakers. N is a governed seam value; its default inherits the platform minimum-group-size parameter unless the tenant sets a register-specific value."* | P096 | rule (condition 2 · N is a seam value) |
| V64 · §6.2 cond-3 | *"Non-reconstructive in combination. Tested against attribute combinations, not attributes in isolation: language + region + age band + one distinctive feature can reach a single person even when each attribute is group-level."* | P097 | rule (condition 3 · combinatorial re-id test) |
| V65 · §6.2 cond-4 | *"Stored as description, not exemplar. Centroids, distributions, frequencies. Never stored audio; never per-utterance speaker embeddings. Embeddings used during clustering are destroyed after cluster assignment. Provenance points to material, not to speaker identity."* | P098 | rule (condition 4 · description-only · embedding destruction after clustering) |
| V66 · §6.3 | *"The register write path exposes no field through which an instance-level representation can be stored: the schema cannot represent a voiceprint. Unrepresentable, not policed (§1.5). An automated invariant test attempts each known leakage path (small stratum, idiolect marker, narrowing combination, exemplar storage) and must fail to store all of them on every change to the register code."* | P100 | rule (leakage-path invariant test · four leakage paths named) |
| V67 · §6.4 | *"Habitual fillers, characteristic phrasings, and idiosyncratically pronounced words are learned but individuating. They fail condition 2 or 3 and are excluded. "Learned" alone is never sufficient; the four conditions are conjunctive."* | P102 | rule (idiolect rule · four-conditions-are-conjunctive) |

## §7 · Synthesized Voice Identity — Invention (P103..P122)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V68 · §7.1 | *"Learned characteristics are inherited from the register — this is what makes the voice sound like a speaker of the language rather than a foreigner reading it."* | P105 | rule (learned = inherited) |
| V69 · §7.1 | *"Organic characteristics are constructed — vocal tract parameters, F0 range, formant structure, glottal parameters are chosen as a point in acoustic space that no real speaker occupies."* | P106 | rule (organic = constructed) |
| V70 · §7.1 | *"This is the inverse of a voice clone. A clone copies the organic and frequently gets the learned wrong; this gets the learned right and owns the organic outright."* | P107 | rule (inverse-of-voice-clone) |
| V71 · §7.2 | *"Every constructed identity is scored against every speaker representation derivable from the corpus using standard speaker-verification methods. A minimum distance from all of them is required. Below threshold, the identity is rejected and resampled. There is no override. The threshold value and the verification method are recorded with the identity."* | P109 | rule (distance gate · mandatory · fail-closed · no override · method + threshold recorded) |
| V72 · §7.3 | *"A passing identity is issued a certificate stating that the voice is provably derived from no individual, naming the method, the threshold, and the corpus version scored against. The certificate is a first-class sellable artifact."* | P111 | rule (certificate is a first-class sellable artefact) |
| V73 · §7.4 comp-1 | *"Acoustic identity ⎢ Constructed organic parameters (§7.1)."* | P115 · TABLE-ROW-02 | contract-cell |
| V74 · §7.4 comp-2 | *"Speech character ⎢ Inherited from register — phonetic and prosodic layers."* | P116 · TABLE-ROW-03 | contract-cell |
| V75 · §7.4 comp-3 | *"Interaction character ⎢ Turn-taking, formality, code-switch behaviour — inherited from register."* | P117 · TABLE-ROW-04 | contract-cell |
| V76 · §7.4 | *"Each identity is a versioned artifact with a ledger entry. Changing one is a ceremony with the standard waiting period, because audience recognition accrues to the voice and recognition is the asset. Identities never drift."* | P120 | rule (versioned artefact · change-by-ceremony · never-drift) |
| V77 · §7.5 | *"Rendering requires a synthesis stack, which is a separate build from recognition. What this specification requires now is non-foreclosure: the identity specification (attribute schema, distance method, certificate format) is defined, and §4.4's ingestion capture ensures the substrate exists when rendering is built."* | P122 | rule (rendering-is-separate-build; non-foreclosure obligation only) |

## §8 · The Objective Wizard — Schema Compiler (P123..P145)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V78 · §8.1 | *"No business user hand-writes a Target Outcome. The Objective Wizard — a new variant of the existing shaping wizard, reusing its agent interface, guards, session persistence, and ledger sidecar — elicits an objective in plain language and compiles two governed artifacts:"* | P125 | rule (no hand-written Outcomes; wizard variant) |
| V79 · §8.1 outputs | *"TargetOutcome (§10) — handed to the Training Planner."* | P126 | contract-cell |
| V80 · §8.1 outputs | *"Collection Schema (§9) — the data dictionary for this objective: which data points are extracted from the sound, at what granularity, at what quality bar."* | P127 | contract-cell |
| V81 · §8.2 elicit-1 | *"The question the model must answer — operational and falsifiable."* | P129 | rule (elicitation carrier 1) |
| V82 · §8.2 elicit-2 | *"The population — resolved against existing register strata; unresolved populations are flagged as unmeasured and generate census work."* | P130 | rule (elicitation carrier 2 · unresolved → census) |
| V83 · §8.2 elicit-3 | *"The acceptance bar — per stratum, two-dimensional (§10), with the gate-or-document decision recorded explicitly."* | P131 | rule (per-stratum acceptance · two-dimensional) |
| V84 · §8.2 elicit-4 | *"The collection consequences — the wizard derives required columns, shows which are already collected (baseline tier), which exist but are uncollected, and the cost of collecting them. The owner sees the price of the schema before commissioning."* | P132 | rule (price-before-commission) |
| V85 · §8.3 | *"Propose. The agent side may propose novel data points no prior objective collected. This is where innovation enters."* | P134 | rule (propose stage) |
| V86 · §8.3 | *"Qualify. A proposed column never enters collection directly. It is admitted as a candidate: collected on a sample only, its evidence of value measured against the objective — the same qualification path any fact travels."* | P135 | rule (qualify stage; measured against objective) |
| V87 · §8.3 | *"Graduate. Qualified candidates graduate into the objective tier for that commission. Graduation into the baseline tier is ceremony-governed (proposal, countersignature, waiting period), because a baseline column is paid on every hour ingested for the life of the estate."* | P136 | rule (graduate stage · baseline promotion is ceremony-governed) |
| V88 · §8.3 | *"The compile stage is deterministic throughout: the agent proposes; only qualified columns compile. Mechanical guards prove against a stub agent before any LLM is plugged in, per the existing standing disposition."* | P137 | rule (deterministic compile; mechanical-guards-before-LLM) |
| V89 · §8.4 | *"The wizard cannot emit an artifact the downstream contracts would refuse. Rejected at compile, not warned:"* | P139 | rule (compile-time rejection preamble) |
| V90 · §8.4 | *"An Outcome without an existing test_set_ref."* | P140 | rule (rejection 1) |
| V91 · §8.4 | *"An acceptance bar missing the per-stratum dimension."* | P141 | rule (rejection 2) |
| V92 · §8.4 | *"A Collection Schema requiring a column whose capture violates the custody conditions of §6.2."* | P142 | rule (rejection 3) |
| V93 · §8.5 | *"Every session stamps to the ledger via the existing turn-ledger pattern under a distinct data class (objective_session), including options considered and rejected — which is what makes a later "why was the model built this way" answerable. Compiled artifacts hand off to Targeta through the existing admission-handoff pattern. Objective → schema → plan → run is one provenance chain."* | P144 | rule (turn-ledger stamping · options-considered-and-rejected · handoff to Targeta) |
| V94 · §8.5 [VERIFY] | *"[VERIFY] The B-2/B-3 landing state of the current wizard, before choosing between extending the existing state machine with an objective variant or standing up a sibling machine sharing the agent interface and ledger sidecar."* | P145 | verify-item |

## §9 · The Collection Schema (P146..P152)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V95 · §9.1 | *"The declared data dictionary of a commission: what is extracted from the sound, for what purpose, at what quality bar. It is the admission standard of the audio estate, per objective (§1.1). It has two tiers."* | P148 | definition (Collection Schema) |
| V96 · §9.2 | *"Standing, objective-independent, collected at first ingestion for all admitted material. Membership criterion: cheap to collect now, unaffordable to collect later. Contents at v1.0: language identification, code-switch points, condition profile, dedup instance condition map, synthesis-relevant group-level acoustics (§4). Changes to the baseline are seam-governed — ceremony, countersignature, waiting period — because silently narrowing the baseline is how an estate quietly becomes unre-readable."* | P150 | rule (baseline tier · unconditional · v1.0 five-item content set · seam-governed changes) |
| V97 · §9.3 | *"Declared per commission by the Objective Wizard. Collected against material already in governed scope, priced before collection starts, recorded in the commission's registry namespace. Candidate columns enter through propose–qualify–graduate (§8.3) only."* | P152 | rule (objective tier · priced-before-collection · candidates through §8.3 only) |

## §10 · The Target Outcome (P153..P169)

### §10.1 · Schema (P154..P164 · verbatim TargetOutcome block)

| Row | Verbatim field | Verbatim description | Anchor | Classification |
|---|---|---|---|---|
| V98 | *"task"* | *"operational statement of what the model must do"* | P156 | contract-cell |
| V99 | *"domain"* | *"context of use"* | P157 | contract-cell |
| V100 | *"population"* | *"defined by reference to register strata, not labels"* | P158 | contract-cell |
| V101 | *"acceptance"* | *"threshold per stratum; two-dimensional (accuracy, coverage)"* | P159 | contract-cell |
| V102 | *"gate_policy"* | *"per Outcome: missed stratum gates release | ships documented"* | P160 | contract-cell |
| V103 | *"test_set_ref"* | *"must exist before the Outcome is accepted"* | P161 | contract-cell (LOAD-BEARING) |
| V104 | *"constraints"* | *"latency, compute budget, deployment target"* | P162 | contract-cell |

### §10.2 · Binding rules (P165..P169)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V105 | *"Population is register-defined. "Language L, accent clusters 1–4, telephone band and studio, adult" — never "speakers of L." This is what makes coverage computable."* | P166 | rule (register-defined population; no label populations) |
| V106 | *"Acceptance is per stratum. A single global threshold hides the failure that matters: 94% on the majority variant and 61% on the rest passes one test and fails the one that decides whether the work reaches the people it was built for."* | P167 | rule (per-stratum acceptance; no global threshold) |
| V107 | *"The test set precedes the training. An Outcome without an existing, stratified test set is rejected at definition time."* | P168 | rule (test-set-precedes-training) |
| V108 | *"The gate decision is recorded on the Outcome at definition — not decided ad hoc at ship time."* | P169 | rule (gate decision at definition time) |

## §11 · The Training Planner (P170..P192)

### §11.1 · Architecture (P171..P178)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V109 | *"The existing planner pattern is reused unchanged: a deterministic core computes eligibility; a learned layer may only reorder an already-eligible set it receives stripped of the values that decided eligibility; a gate compares learned output against the deterministic baseline; every plan is reproducible from its recorded inputs."* | P172 | rule (planner-pattern reused · four-carrier architecture · reproducibility) |
| V110 · table | *"Object · Source locations · Register strata"* | P175 · TABLE-ROW-02 | contract-cell (extraction vs training) |
| V111 · table | *"Floor · Defensibility class · Acceptance threshold — accuracy × coverage"* | P176 · TABLE-ROW-03 | contract-cell |
| V112 · table | *"Output · Mining plan · Training plan + curriculum + milestones"* | P177 · TABLE-ROW-04 | contract-cell |

### §11.2 · Sampling & Reflection (calibration) (P180..P181)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V113 | *"Data requirements for low-resource fine-tuning are empirical; no analytical answer exists. The first commissioned stage is therefore a calibration: train at three to four data volumes, evaluate per stratum against the test set, fit the scaling curve, extrapolate to the acceptance threshold. Only then is the full run quoted, with a stated confidence interval — never a point estimate. A plan without a calibration stage is rejected. The first job prices the real job."* | P181 | rule (mandatory first stage · calibration procedure · plan-without-calibration rejected · confidence interval not point estimate) |

### §11.3 · Milestones (P182..P183)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V114 | *"Sampling & Reflection has two customers. It prices the real job, and it authors the accountability structure: its output to the objective owner is not a curve but a proposed milestone list — the checklist of what must be done, in what order, for the commission to succeed. Each milestone carries a done-condition and an owner. The objective owner reviews and agrees the list at commission; from that point, all reporting is against it. Accountability is set before spend, not discovered during."* | P183 | rule (milestone-list contract · done-condition + owner per milestone · accountability set before spend) |

### §11.4 · Planner outputs (P184..P188)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V115 | *"Coverage report — per target stratum: hours available, quality distribution, gaps, cost of closing each gap."* | P185 | contract-cell |
| V116 | *"Curriculum — ordering and weighting across strata derived from the register, not from the corpus's natural distribution, which is always skewed toward whatever occurred most. The dedup instance condition map enters as a designated robustness stratum."* | P186 | rule (curriculum from register not corpus; dedup map = robustness stratum) |
| V117 | *"Proposed milestone list (§11.3)."* | P187 | contract-cell |
| V118 | *"Cost quote with a stated confidence interval."* | P188 | contract-cell (confidence interval mandatory) |

### §11.5 · Provenance through training (P189..P190)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V119 | *"Every training example carries its provenance into the training manifest. Consequences: rights are enforceable per example; an example whose rights lapse is identifiable and the affected models enumerable; and "the trained model is the customer's property" is a statement backed by a manifest, not an assertion."* | P190 | rule (per-example provenance · manifest-backed rights) |

### §11.6 · Run governance (P191..P192)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V120 | *"Training runs are commissioned jobs under the existing contract: quoted before start, metered during, certificated on completion. The completion certificate records compute consumed, data touched, manifest hash, and per-stratum results against the Outcome. Failed strata are reported as plainly as passed ones."* | P192 | rule (four-carrier completion certificate · failed as plainly as passed) |

## §12 · Record and Registry Integration (P193..P197)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V121 · §12.1 | *"Per commission, a scoped namespace within the registry holds: the Collection Schema (versioned), collected data points mapped against it — with declared-but-not-yet-collected as first-class state — the strata referenced by the Outcome, and coverage state per stratum. Reads compose with the global registry; writes are namespace-scoped. On close, the namespace is sealed, not deleted: it is the record of what was collected and why, and the next objective's wizard session queries prior schemas and coverage so the second project starts from the first project's map."* | P195 | rule (per-commission namespace · declared-but-not-yet-collected first-class · sealed-not-deleted) |
| V122 · §12.2 | *"Training-workflow operations stamp into the one ledger under training-specific data classes: collection events, calibration runs, curriculum decisions, milestone status changes, run certificates. The workflow's view of "its" record is a scoped lens filterable by commission ID — a view, not a store. Working state (loss curves, intermediate metrics, partial counts) is scratch until finalized and stamped once (§1.3)."* | P197 | rule (one-ledger · scoped lens · scratch-until-stamped) |

## §13 · Surface Specification — the Commission View (P198..P210)

| Row | Verbatim quote | Anchor | Classification |
|---|---|---|---|
| V123 · §13.1 | *"This surface adjustment applies to all commissioned work on the platform — extraction, census, and training commissions alike, across every extraction type. No modality receives its own UI, and no surface is a rendering of backend internals: rendering internals quietly commits the backend to building displayable versions of its own machinery."* | P200 | rule (universal surface · no modality-specific UI · no backend-internals rendering) |
| V124 · §13.2 | *"The surface is milestones. The artifacts are evidence behind them."* | P202 | rule (surface = milestones) |
| V125 · §13.2 | *"At Sampling & Reflection, the proposed milestone list is presented to the objective owner for agreement. Commission does not open until it is agreed."* | P203 | rule (commission does not open before milestone agreement) |
| V126 · §13.2 | *"The Commission View reports against the agreed checklist: each milestone with its done-condition and owner; status in plain terms — done, on track, behind, missed. Missed is shown as plainly as done."* | P204 | rule (missed = as plain as done · closed 4-state status set) |
| V127 · §13.2 | *"Spend against quote is shown at the same plain level."* | P205 | rule |
| V128 · §13.2 | *"Technical material — calibration results, strata coverage, Collection Schema state — is drill-down evidence for whoever asks why a milestone reads as it does. It is never the front page."* | P206 | rule (technical material as drill-down only) |
| V129 · §13.3 | *"Modality appears at exactly one leaf: evidence inspection. Where provenance resolves to a recording, the source plays at its timestamp rather than rendering as a page region — the existing trust-receipt pattern ("a disputed number is answered by playing the tape"), unchanged."* | P208 | rule (modality-at-one-leaf · trust-receipt pattern quotation) |
| V130 · §13.4 | *"Milestones are records with done-conditions; the platform already stamps events. No new machinery is built for display. Any surface element in this section found to require new backend computation beyond reading existing artifacts is out of specification and must be removed or re-specified."* | P210 | rule (no-new-backend-computation for display) |

## §14 · Interface Summary (P211..P224 · master contract table)

| Row | Surface (verbatim) | Contract (verbatim) | Anchor |
|---|---|---|---|
| V131 | *"audio_codec"* | *"audio in → { content_tokens, character_stream, codec_version }; fail-closed on unsupported condition."* | P214 · TABLE-ROW-02 |
| V132 | *"Language ID"* | *"segment → { languages[], confidences, switch_points }; written to provenance."* | P215 · TABLE-ROW-03 |
| V133 | *"Occurrence index (ext.)"* | *"dedup item → + instance condition map."* | P216 · TABLE-ROW-04 |
| V134 | *"Character Register"* | *"Write path: schema cannot represent instance-level identity (§6.3). Read path: strata queries for planner and evaluation."* | P217 · TABLE-ROW-05 |
| V135 | *"Objective Wizard"* | *"session → { TargetOutcome, CollectionSchema }; deterministic compile; compile-time rejection of contract-violating artifacts; session stamped to ledger."* | P218 · TABLE-ROW-06 |
| V136 | *"TargetOutcome"* | *"Rejected without existing test_set_ref; acceptance per stratum; gate_policy recorded at definition."* | P219 · TABLE-ROW-07 |
| V137 | *"Training Planner"* | *"Outcome → { coverage report, curriculum, milestone list, quote ± interval }; reproducible plan_id; plan without calibration stage rejected."* | P220 · TABLE-ROW-08 |
| V138 | *"Training run"* | *"Commissioned-job contract; completion certificate incl. manifest hash and per-stratum results."* | P221 · TABLE-ROW-09 |
| V139 | *"Voice identity"* | *"register strata + constructed organic parameters → identity; distance gate mandatory, fail-closed; certificate issued on pass; versioned; change by ceremony."* | P222 · TABLE-ROW-10 |
| V140 | *"Commission View"* | *"Reads milestones, statuses, spend, and existing artifacts only; introduces no new backend computation."* | P223 · TABLE-ROW-11 |

## §15 · Build Sequence (P225..P240 · in full)

| Row | # (verbatim) | Item (verbatim) | Rationale for position (verbatim) | Anchor |
|---|---|---|---|---|
| V141 | *"1"* | *"Ingestion capture: language ID, code-switch points, condition profile, synthesis attributes (§4.1–4.4)"* | *"Everything downstream consumes these; only cheap at first ingestion. Deferral cost is a full re-pass over the estate."* | P229 · TABLE-ROW-02 |
| V142 | *"2"* | *"Dedup instance condition map (§4.5)"* | *"Contract change to existing machinery; near-zero new detection work."* | P230 · TABLE-ROW-03 |
| V143 | *"3"* | *"Character Register schema + custody invariant harness (§6)"* | *"The boundary must exist before the first cluster is stored; retrofitting means rebuilding from source."* | P231 · TABLE-ROW-04 |
| V144 | *"4"* | *"Codec service (§3)"* | *"Unsupervised pretraining starts on unlabelled audio while labelled work proceeds elsewhere."* | P232 · TABLE-ROW-05 |
| V145 | *"5"* | *"Clustering + sampled human validation (§5.3)"* | *"Requires 1–4."* | P233 · TABLE-ROW-06 |
| V146 | *"6"* | *"Objective Wizard variant + Collection Schema type + registry namespace (§8, §9, §12.1)"* | *"The planner must never accept a hand-authored Outcome once the wizard exists; building the planner first invites the malformed-input class the compile stage makes impossible."* | P234 · TABLE-ROW-07 |
| V147 | *"7"* | *"TargetOutcome type + planner core (§10, §11.1, §11.4)"* | *"Requires register strata to plan against and the wizard to author Outcomes."* | P235 · TABLE-ROW-08 |
| V148 | *"8"* | *"Sampling & Reflection machinery + milestone records (§11.2–11.3)"* | *"Requires 7 and a test set."* | P236 · TABLE-ROW-09 |
| V149 | *"9"* | *"Commission View (§13)"* | *"Reads records created in 8; by §13.4 it cannot precede them."* | P237 · TABLE-ROW-10 |
| V150 | *"10"* | *"Full training runs under the commissioned-job contract (§11.6)"* | *"Last by construction — the planner refuses to run earlier."* | P238 · TABLE-ROW-11 |
| V151 | *"P2"* | *"Voice identity rendering; music register"* | *"Phase 2. Non-foreclosure is guaranteed by item 1 and §7.5."* | P239 · TABLE-ROW-12 |

## §16 · Verification Register and Open Decisions (P241..P251 · in full)

### §16.1 · [VERIFY] items (P242..P245)

| Row | Verbatim quote | Anchor |
|---|---|---|
| V152 | *"Perception router contract — model registration point; whether a second output stream per segment is carried or the character stream needs its own artifact type (§3.2)."* | P243 |
| V153 | *"Ingestion segment boundaries — the unit a language label attaches to (§4.1)."* | P244 |
| V154 | *"Wizard B-2/B-3 landing state — extend the existing state machine with an objective variant, or stand a sibling machine on the shared agent interface and ledger sidecar (§8.5)."* | P245 |

### §16.2 · Open decisions (owner: product) (P246..P251)

| Row | Verbatim quote | Anchor |
|---|---|---|
| V155 | *"N for the shared-attribute condition (§6.2.2): inherit the platform minimum-group-size seam value, or set a register-specific one."* | P247 |
| V156 | *"Platform default for gate_policy (§10.1) where an Outcome does not set it: missed stratum gates release, or ships documented. This default silently decides how minority-variant quality is treated under schedule pressure."* | P248 |
| V157 | *"Cluster naming validation: commissioned internally or delegated to an external evaluation partner where one exists (§5.3)."* | P249 |
| V158 | *"Codec choice: adopt an existing open codec versus training estate-specific — a trade the Sampling & Reflection machinery can itself answer once built (§3, §11.2)."* | P250 |
| V159 | *"Baseline tier contents (§9.2): the v1.0 set is the proposal; every addition is paid on every hour ingested, every omission is paid at re-ingestion."* | P251 |

## §Closing (P253)

| Row | Verbatim quote | Anchor |
|---|---|---|
| V160 | *"End of specification. This document is the single build reference for the Audio Intelligence Plane; the working drafts it consolidates are retired."* | P253 |

---

## Summary counts

* **Total verbatim rows:** **160** (V01..V160).
* **Sentence-split rows within one paragraph** are numbered as separate V-rows only where the sentence stands as a discrete rule (P015 → V07..V10 style is used sparingly; most rows are whole-paragraph quotes).
* **[VERIFY] items:** 4 (V38, V46, V94, V152..V154). §16.1 collects three of them; V38 also appears in §3.2 P050.
* **Open decisions (owner: product):** 5 (V155..V159 · §16.2).
* **Build sequence items:** 11 (V141..V151 · §15 · numbered 1..10 + P2).
* **Interface Summary contract cells:** 10 (V131..V140 · §14).
* **Six-crossing-style closed-set fields:** N/A (this spec is not the Pull Seam · no six-crossing table here).
* **Named models in the doc:** **zero** — this is confirmed and covered in `notes/CANON_MODEL_SPECS_VERBATIM_20260914.md`.

---

## Cross-links

* Structured extract: `canon/drops/20260914_audio_plane_v1/extracted/Audio_Plane_Spec_STRUCTURED.txt`.
* Raw docx: `canon/drops/20260914_audio_plane_v1/raw/Akki_OS_Audio_Intelligence_Plane_Specification_v1_0.docx`.
* Raw md: `canon/drops/20260914_audio_plane_v1/raw/Audio_Intelligence_Plane.md`.
* Manifest: `canon/drops/20260914_audio_plane_v1/manifest.json`.
* Owner-facing answer on model choice: `notes/CANON_MODEL_SPECS_VERBATIM_20260914.md`.
* Drift audit vs built work: `notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md`.
* Standing rule: DECISIONS.md 2026-09-15T~01:40Z (Verbatim-canon discipline).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
