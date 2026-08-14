# Canon 4 — Akki Operating Engines — Extracted Requirements

Source: `/app/assessment_workspace/canon/text/Akki_Canon_4_Operating_Engines.txt`
(extracted from `Akki_Canon_4_Operating_Engines.docx`). Row IDs `C4-###`.

## Part I — Scope

- **C4-001 (§1)**: Doc 4 specifies OPERATING engines (Mtafiti — Measurement, Targeta — Targeting) and the two named services they compose into with the governance engines: (S-A) the extraction/census service and (S-B) the answering service. Also specifies the two named seams and the MOAC (Model Acceptance Card).
- **C4-002 (§1)**: Where Doc 3 (governance) and Doc 4 (operating) touch, precedence follows Doc 1 §5. Doc 4 does not redefine any governance verdict or ledger class.

## Part II — Mtafiti (Measurement)

### §5–§10

- **C4-003 (§5 Charter)**: Mtafiti measures WHAT THE ESTATE ACTUALLY CONTAINS, at whatever scale (whole org, department, archive, single file — Doc 1 §1.1).
- **C4-004 (§5 Objective-blind)**: Mtafiti measures without reference to any objective. It measures the ESTATE, never the ANSWER. Reads for Watch tripwire coverage, never writes for them (Doc 9 §3).
- **C4-005 (§6 Three states)**: Every measured region is rendered in EXACTLY one of three states: Measured — sound; Measured — degraded (limitation named); Not yet measured. Absence of measurement is NEVER rendered as empty/clean/zero (Doc 1 §9.1).
- **C4-006 (§6)**: A degraded measurement carries the LIMITATION as a first-class field — the reason the number is degraded is visible wherever the number is shown.
- **C4-007 (§7 Two-layer defensibility)**: Defensibility is produced in two layers: a DECLARATION layer (deterministic, per source, always available — the FLOOR) and an INFERENCE layer (signals detected in content — corroboration and contested status).
- **C4-008 (§7)**: Inference contributes ONLY after its own accuracy has been proven on the tenant's own material. Until then, declaration STANDS ALONE.
- **C4-009 (§7)**: Neither layer decides what a measurement means. Meaning is a governed, versioned lookup — never a model's output.
- **C4-010 (§8 Census records)**: Mtafiti writes census/registry records (Doc 9 §3). Readers: both authorities + every surface by proof link. Every figure in every surface must trace to a census row.
- **C4-011 (§9 Composition)**: Mtafiti produces composition-by-strata: by language, era, source, condition, evidence class. Real counts, not estimated fractions unless flagged.
- **C4-012 (§9)**: A composition figure that would be quoted below Mtafiti's confidence floor RENDERS AS "insufficient measurement" — never as zero.
- **C4-013 (§10 Repeatable)**: Every Mtafiti measurement is repeatable — same inputs, same time-boundary, same declaration set → same measured output.

## Part II — Targeta (Targeting)

### §11–§15

- **C4-014 (§11 Charter)**: Targeta plans extraction — WHICH material, WHICH order, WHICH standards, WITHIN WHICH rights — against a frozen objective. Writes mining plans (Doc 9 §3). Readers = governing authority + auditors. Watch neither reads to steer nor writes.
- **C4-015 (§11 Objective-bound)**: Targeta operates ONLY on frozen objectives (Doc 3 §5). Never plans against an amending or drafting objective.
- **C4-016 (§12 Plan artefact)**: The mining plan lists: reused stock already usable, extraction volume as a range, expected coverage of the goal, what CANNOT be covered and why. All four are required.
- **C4-017 (§12 Reuse-first)**: Targeta must identify reusable prior extractions before proposing new work. Reusing prior work is preferred over re-extraction whenever the standards match. Non-reuse must state why.
- **C4-018 (§13 Coverage figure)**: The coverage figure is a MEASURED anticipation drawn from Mtafiti composition, not a projection. It is stated as a RANGE, never a point estimate.
- **C4-019 (§14 Plan preview)**: The Shaping Wizard (Doc 5 §14) renders the plan preview in the commissioning flow. No commitment occurs before the preview is shown.
- **C4-020 (§15 Plan versioning)**: A plan is versioned. A material change (scope broadening, standard change, source addition) is a NEW plan superseding by ledger row, never a mutation.

## Part III — The Two Services

### §16 (Service A — extraction/census)

- **C4-021 (§16)**: S-A composes: Northena (admit the extraction objective) + Mtafiti (measure applicable regions) + Targeta (plan) + workers (execute) + SyniSense (any outbound leg) + Solva (any reasoning-intensive step) + rules (Compliance Rulebook enforcement).
- **C4-022 (§16 Terminus)**: S-A ends in a FROZEN UNIT CONTRACT — the deliverable's contents, licence label, privacy attestation, quality card, proof trail bound together and receipted.
- **C4-023 (§16 Shelf)**: Deliverables land on the shelf as they complete: datasets, briefs, standing feeds, occurrence indexes. Each carries its full attestations (per Doc 6 §7).

### §17 (Service B — answering)

- **C4-024 (§17)**: S-B composes: Northena (admit the ask) + retrieval against measured/committed material + Solva (reasoning when needed) + SyniSense (any outbound model call) + presentation.
- **C4-025 (§17 Loopback)**: S-B calls back into S-A ONLY for what has not yet converged. It does not RE-DO S-A's work; it commissions new S-A work when the current answer requires it.

## Part III — The Two Seams

### §18–§19

- **C4-026 (§18 Seam-1 — admit → extract)**: The frozen objective and declaration cross as a whole artefact from Northena's admit row to Targeta's plan input. Registered handoff contract (Doc 9 §6). Receipt = the admit row.
- **C4-027 (§19 Seam-2 — chokepoint → model)**: The custody chain (Doc 3 §13.1) plus the input seat's verdict PRECEDES model invocation. A hold verdict at the seat RENDERS as the refusal card. Registered handoff contract (Doc 9 §6). Receipt = trust receipt + verdict.
- **C4-028 (§19)**: NO OTHER CHANNEL exists between the engines and the models. Any additional handoff surface is a defect (Doc 7 defect D-class).

## Part IV — Workers

### §20–§23

- **C4-029 (§20)**: Workers execute extraction, annotation, verification, and adapter-training steps under Targeta's plan and Northena's admit. Each worker's obligations are registered in the Function & Promise Registry (Doc 1 §8).
- **C4-030 (§20)**: A worker's output must carry a manifest (Canon 2 §8) — every claim traces to source and states its evidence class.
- **C4-031 (§21 The Critic Seam)**: The Critic Seam is the standing quality layer applied to worker output — evaluates against the rubric registered in the platform's registry. Every accepted worker output passes the Critic Seam.
- **C4-032 (§21)**: A shipped worker output that has not passed the Critic Seam is a defect. Retroactive Critic Seam runs are re-verifications, not permission grants.
- **C4-033 (§22 Independence rule)**: The Critic Seam and its target must satisfy Solva-pattern independence (Doc 3 §18) — different base or materially different context. Same-base same-context critique is inadmissible.
- **C4-034 (§23 Quarantine)**: A worker output failing the Critic Seam enters QUARANTINE. Quarantined batches surface on the Batch Board (Canon 5) with status and resolution path. Resolution = re-run, redirect, or write off; each is a ledger event.

## Part V — Adapters and Models

### §24–§29

- **C4-035 (§24)**: As labelled material accumulates, adapters train on it. Every trained adapter enters the registry (Canon 5 §12.2 Models) with base model, training lineage, inherited rights, scorecard, version history.
- **C4-036 (§25)**: Before any adapter exists for a given class, the surface says so PLAINLY rather than rendering an empty error (Doc 6 §8).
- **C4-037 (§26 MOAC — Model Acceptance Card)**: Every accepted adapter carries the six-criterion MOAC scorecard with real measured numbers. The six criteria are (§26.1–§26.6):
    - **C4-037a (§26.1)**: Accuracy on the tenant's uncurated measured composition (Doc 1 §4.10).
    - **C4-037b (§26.2)**: Coverage across strata Mtafiti has measured.
    - **C4-037c (§26.3)**: Refusal behaviour under Solva-pattern (§17) — measured refuse-rate on out-of-scope prompts.
    - **C4-037d (§26.4)**: Provenance integrity of the training data (Doc 1 §4.9).
    - **C4-037e (§26.5)**: Cost per operation, measured on real load.
    - **C4-037f (§26.6)**: Time to answer at the 95th percentile, measured under the platform's load pattern.
- **C4-038 (§27 Independent evidence)**: MOAC evidence is drawn from an UNCURATED sample of the tenant's material (Doc 1 §4.10). Curated benchmarks are inadmissible for MOAC.
- **C4-039 (§28 Rights lineage)**: Every adapter carries its full training lineage back to rights-held source material. An adapter whose lineage cannot be resolved is a defect and does not ship.
- **C4-040 (§29 Version history)**: Adapters version like every other artefact — supersede by new row, never mutate. Prior versions remain queryable.

## Part V — Extraction and Census

### §30–§34

- **C4-041 (§30 Census)**: Census is the first act on a source — measures composition, quality, condition. Result feeds Mtafiti records (Doc 9 §3).
- **C4-042 (§30)**: Census runs are re-runnable and idempotent within a stated time boundary. Repeat census on the same source at a later boundary produces a NEW census row that supersedes.
- **C4-043 (§31 Extraction admit)**: An extraction admit carries the objective, the plan (Targeta), and the standards (Rulebook) — Northena admits or refuses on that whole artefact.
- **C4-044 (§31 Ledger)**: Extraction runs write to the run ledger like any other operation. Batches carry batch ids; batch-level events (start/complete/quarantine/release) are ledger rows.
- **C4-045 (§32 Sampling)**: Sampling is a first-class capability (Doc 6 §5 pre-purchase exploration) — a user may request a sample against a candidate objective BEFORE commissioning. Sampling runs under a scoped admission, is receipted, and its output is throwaway unless promoted by a new admission.
- **C4-046 (§33 Delivery)**: Extraction deliverables land on the shelf as they complete (Doc 6 §7). Delivery is receipted; the licence label and privacy attestation travel with the deliverable to the recipient.
- **C4-047 (§32 Batching, Holds, and Ceilings)**: The Extraction Console renders a batch board (Canon 4 §32) with every batch's status (in progress / released / quarantined / re-running) and resolution path.
- **C4-048 (§34.2 Frozen artefact crossing)**: Seam-1 (admission → extraction) crosses the WHOLE frozen artefact — objective, declaration, plan, standards, rights — never a subset.

## Part VI — Operating Loop Details

### §35

- **C4-049 (§35 Question flow)**: The loop's beats (Doc 6 §11) render operationally as: incoming questions → S-B → answered / held / refused; unanswered → gap file with demand evidence → gap ranking → gap becomes an extraction commission → S-A → registry update → next question round pulls from the updated registry.
- **C4-050 (§35 Gap ranking)**: Gaps rank themselves by demand evidence carried on them — attempts to ask, refusals, near-misses. No priority list is maintained by hand.
- **C4-051 (§35 Loop self-limits)**: The loop is a healthy self-limit — when the gap list stops producing high-demand candidates, the estate has been mined to its current questions' depth (Doc 1 §10).

## Part VI — Standards and Rights

### §36–§39

- **C4-052 (§36 Standards)**: Every objective carries a STANDARD — the minimum evidence class its outputs must meet. Standards are rulebook-set defaults with per-objective override under ceremony.
- **C4-053 (§37 Rights)**: Every source carries the rights held on it — declared at Setup (Doc 6 §3). Extraction against a source is bounded by its rights.
- **C4-054 (§38 Rights-unclear)**: Rights-unclear material is a first-class state (Doc 1 §1.1). It ADMITS to inspection but does NOT ADMIT to extraction for external delivery until the rights state is resolved.
- **C4-055 (§39 Rights resolution)**: Resolution of rights state is a ceremony-grade event — a legal or contract determination lands as a ledger row citing the artefact evaluated. Rights DO NOT resolve by inference.

## Part VII — Trust and Verifiability

### §40–§42

- **C4-056 (§40 Verifiability)**: Every deliverable is independently verifiable by its licensee. Provided outputs include the proof pack sufficient for offline verification (Doc 3 §33).
- **C4-057 (§41 Contents attestation)**: Every dataset/brief/feed carries a CONTENTS attestation — what the deliverable contains and what it does not.
- **C4-058 (§41)**: What it does NOT contain is stated as explicitly as what it does. Absence is a first-class fact.
- **C4-059 (§42 Privacy attestation)**: Every deliverable carries a privacy attestation — the mask levels applied, the residual re-identification risk, the rules consulted.
- **C4-060 (§42 Quality card)**: Every deliverable carries a quality card mirroring the MOAC (§26) at the deliverable level — the six criteria measured on THIS deliverable, not on the model that produced it.

## Part VIII — What Operating Engines Do NOT Do

### §43

- **C4-061 (§43)**: Mtafiti does not decide what a measurement means (Doc 1 §9.2). Only a governed lookup does.
- **C4-062 (§43)**: Targeta does not admit or refuse; that is Northena's authority.
- **C4-063 (§43)**: Workers do not modify a frozen objective mid-run.
- **C4-064 (§43)**: The Critic Seam does not adopt a new class of failure on its own authority (per Canon 2 CIF's origination-port constraint).

## Part IX — Enforcement (§44)

- **C4-065 (§44 Build gates)**: Static checks — no worker writes to the frozen objective; no adapter ships without MOAC; no deliverable ships without contents/privacy/quality attestations; no census result quotes a figure below its confidence floor.
- **C4-066 (§44 Runtime)**: Every extraction admit produces a plan; every plan produces a ledger row; every worker output produces a manifest; every deliverable produces attestations. Missing any = failed operation, not a warning.
- **C4-067 (§45 MOAC drift)**: When a MOAC criterion drifts materially against a prior reading, the adapter is re-scored. Drift is measured against the tenant's currently measured composition, not against a historical benchmark.
- **C4-068 (§45)**: The most recent MOAC reading is the ONE accuracy claim in circulation for that adapter — whatever it turns out to be.
