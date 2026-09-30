# Akki skill template — contract v1.0

A skill is a self-contained package pairing an expert responsibility (proposes, designs, interprets) with a production-manager responsibility (plans, runs, reports, delivers). Packages copy this shape and own their copy. They do not import from each other or from this template; conformance is checked by `conformance.py`, which reads a package and reports, and never by a shared runtime.

## Required layout
```
<skill>/
├── SKILL.md              operating knowledge; frontmatter name + description
├── template.json         {"template": "akki-skill", "version": "1.0", "skill": "<name>", "domain": "<component or C.n>"}
├── references/           the domain's judgment: brief, model grammar, libraries with examples, direction rules, discretion, gates
├── schemas/              JSON Schema for every input artefact; a verdict schema with candidates[], manifest[], confirmed_by
├── policies/             thresholds, voices, plate or run policies — every numeric constant the scripts use
├── scripts/              resolve · validate · produce (render|run|assemble) · freeze · qa · build · revise
├── fixtures/<commission>/ brief.json, <model>.json, verdict.json, <spec>.json
└── evals/evals.json      ≥ 4 evals, at least one per failure mode: missing evidence, stub backend, interrupted run, stale assumption, over-authority request
```

## Six stages, in order
1. Brief — six dimensions: purpose, audience, setting, content, brand/tone, outputs.
2. Model — the single source of facts; every figure carries `class` and `receipt`.
3. Direction — a CIF verdict record: candidates with `verdict ∈ {adopt, reject, rank, defer}`, one adopted, a manifest of load-bearing assumptions (`class ∈ {fact, recalled, inferred}`, `source`, `flips[]`), `confirmed_by`. Routine commissions run under a `frame_ref`.
4. Specification — references only; a literal value where a reference belongs is a blocker.
5. Production — deterministic code; a resolved plan is written before anything executes.
6. Gates and delivery — blockers stop release; review items are routed, never auto-fixed; delivery includes a build manifest.

## Outcome set (Critic Seam shape)
Every gate result is one of `pass`, `finding-not-blocking`, `blocked`. There is no `decision` output type anywhere in a skill's outputs.

## Reserved and permitted
`references/discretion.md` lists what the skill may choose within a commission and what it must escalate. Acceptance, admission, eligibility, release, over-ceiling spend, rule application and any Watch action are reserved everywhere.

## Stub honesty
Run-class skills (they execute something) record `backend ∈ {real, stub}` and, where relevant, `execution_mode`; a stub run carries `stub: true` and a status of `stub` or `interrupted`, never one that reads as real. Read-class skills (they compose from records) record `source ∈ {live, snapshot, stub}`; a stub source yields `servable: false`. Either way a stub can never move a status or be served.

## Reproducibility
`references/reproducibility.md` names the domain's contract (byte-identical, within-tolerance, replayable) and cites its canon line. Volatile fields (timestamps, run ids) are held outside the hashed content.

## Proof
`scripts/build.py <fixture> <out> --prove` runs the pipeline twice and asserts the domain's contract; `scripts/revise.py` demonstrates a preserved design and a manifest strike.
