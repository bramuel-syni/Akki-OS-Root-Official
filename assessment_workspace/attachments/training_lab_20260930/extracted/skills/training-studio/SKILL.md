---
name: training-studio
description: The expert + production-manager skill for model training commissions on Targeta (Doc 17, C.20). Use whenever an organisation wants a model trained, fine-tuned or adapted on estate material — "train a model to…", "fine-tune for our archive", "can we get transcription accuracy up on…", an Objective Wizard commission, a calibration or full training run, a recipe comparison, a training technical report, or a MOAC evidence pack. The expert turns intent into a TargetOutcome with register strata, per-stratum two-dimensional acceptance and a sealed test set, and designs the two-arm recipe comparison; the manager runs calibration first, quotes with a confidence interval, keeps the manifest 100% classed with lawful basis, reports every stratum plainly, and assembles the MOAC request. It never declares a run accepted, a recipe adopted, or a model admitted. Not for inference, extraction, or document production.
---

# training-studio

Template: akki-skill 1.0 (`template.json`). Self-contained; imports nothing from other skills.

## What this skill is for
Turning "we need a model that does X on our material" into a commission Targeta can run and MOAC can judge, then running it to a record a reader can act on. The engines hold the decisions (eligibility, floors, yield gate, MOAC, the Owner's recipe verdict); this skill holds the judgment that makes those decisions easy to take and impossible to fudge.

## The expert: four lenses, one library
The expert half is one expert with four lenses (`references/lenses/`): **professor** (is it true; MDE, intervals, seeds, the cause), **researcher** (what one comparison is worth the recipe seat; counterfactual arms; literature priors), **industry** (will it run; capture conditions, monitors, owner, rollback), **entrepreneur** (is it the best use of the budget; value per stratum, stop-loss, phased path, kill criteria). Lenses argue in the record and route disagreements to the objective owner; only the professor's MDE finding blocks, because it is arithmetic.

Depth comes from the content layer the lenses read: `references/playbooks/` (ASR, document, text/LLM, tabular, embeddings: metric, hidden axes, levers in priority order, recipe defaults, monitoring, value), `policies/levers.json` (every lever: when, expected effect with evidence class, cost, preconditions, failure signature, what it does not fix), `policies/priors.json` (sample-efficiency and variance priors per task family), `policies/cause-map.json` (diagnosed cause → levers in order). Direction = objection + lever: every objection carries its remedy priced. All expected effects are priors with a class until a postmortem makes them house-observed on this estate.

## The six stages
1. **Brief** — `references/brief.md`. Purpose is always `train`; the setting decides staged reporting and whether the objective owner reads unattended.
2. **Model** — `objective.json`: TargetOutcome (task, modality, population by register strata with `test_set_ref` and `test_n`, baseline per stratum with receipt, two-dimensional acceptance per stratum, gate policy), the **Collection Schema** (unit, fields, quality gates, labelling protocol, admission rule; A17.20), and `materials` (every source with class, lawful basis, basis_ref, hash, receipt) backed by `materials-index.jsonl`: one row per example with its provenance. Objective counts must equal index counts. Grammar in `references/model.md`. A target without a sealed test set per stratum is rejected at definition, not at run time.
2b. **Objective critique** (`scripts/critique.py`, runs in every build) — the four lenses against the objective: MDE per stratum vs gap (blocker if unverifiable, with the test-set size that would fix it), sealed-set custody, seeds; value per stratum, prior cost vs cap, stop-loss, phased path; capture conditions, monitors, owner seat; literature prior and the comparison rule. Output `critique-table.json` and `critique.md`, each row with lens, class, severity (note | escalate | blocker), proposed lever and what resolves it.
3. **Direction** — `verdict.json`: 2–4 candidates, each tagged with the lens that proposed it, assembled from `references/directions.md`; one adopted; `objections_accepted` and `objections_overruled` recorded against the critique; manifest of load-bearing assumptions. Routine commissions run under `FR-training-calibrate-first-v1`.
4. **Specification** — `plan.json`: stages (calibration → comparison → quote → full), arms, milestones with done-conditions and owners. Values by reference only; a literal threshold, volume or budget in the plan is a blocker. The recipe seat ships `empty` (A17.2).
5. **Production** — `scripts/build.py <fixture> <build> [--prove] [--interrupt-after=STn] [--partial-ruling=REF]`. Resolve → validate → critique → manifest → notebook → calibration → **diagnosis** (cause per stratum with its test: leakage, undetectable, label-noise, distribution shift, data-limited, overfit, method-limited) → **comparison on the lever the diagnosis chose** (with-vs-without, on the smallest valid stratum, with the two-arm MDE stated; adoption evidence is insufficient when the delta is below it) → quote → operational plan → value case → report → review → freeze → qa. The runner talks only to `scripts/backend.py`: `StubBackend` exercises the pipeline and says so in every artefact; `RealBackend` is the adapter contract for the trainer runner (A17.12) and raises with it (A17.9 execution-mode check first).
6. **Gates and delivery** — outcome set `pass | finding-not-blocking | blocked`. Delivery: `run-record.json`, `training-manifest.jsonl` (per-example provenance, hashed), `notebook.jsonl` (WPW-3/4 event capture, hash-chained), `technical-report.md` (WPW-8 skeleton), `review.html` (calibration curves, no runtime), `moac-pack-request.json` (evidence per criterion, no verdict), the completion-certificate template (issued only after a full run), `build-manifest.json`. Revision: `scripts/revise.py` bumps the objective version, detects manifest strikes, rebuilds. Interruption: partial record retained; report blocked until the objective owner's partial ruling is referenced.

## What the expert half must demonstrate
`references/capabilities.md`: objective shaping and critique, stratification, evaluation statistics, comparison design that follows the cause, failure diagnosis with tests, operational planning, value modelling, honesty about ingredients (A17.16) and about priors (every expected effect classed).

## Seasoning
`scripts/postmortem.py` scores each lens's falsifiable predictions against actuals when a full run lands: examples-to-floor (professor), comparison winner and whether it was even detectable (researcher), whether the first production failure was on a monitored signal (industry), value realised within 30% (entrepreneur). Hit rates per lens weight the lenses over commissions (cif_spec §10); a confirmed lever effect becomes house-observed with the run record as its receipt. The skill starts with good priors and the loop that corrects them; it does not start corrected.

## Discretion
`references/discretion.md`. Permitted without escalation: calibration volumes within policy, sampling floors for small strata, which stratum hosts the comparison, milestone wording, report wording, bounded repair (≤3 passes). Reserved: the comparison verdict (Owner, A17.6), recipe adoption, MOAC acceptance, model admission, release, spend over cap, filling the recipe seat without evidence, naming a production base model before census (A17.11).

## Non-negotiables
- Every stratum is reported, failed as plainly as passed. A missing stratum is a blocker.
- The runner never writes a verdict; the comparison lays both arms side by side with the parity test and the compute-to-convergence figure, and leaves the field `pending Owner ruling`.
- Quotes carry a confidence interval, never a point estimate; over-cap routes to a named person and never proceeds.
- The manifest is 100% classed with lawful basis and hash or the run does not start.
- A stub run carries `stub: true` and a status of `stub` or `interrupted`, never one that reads as real; its report opens by saying so.

## Layout
```
training-studio/
├── SKILL.md · template.json
├── references/   brief · model · directions · capabilities · discretion · reproducibility · gates · backend-contract
│   ├── lenses/     professor · researcher · industry · entrepreneur
│   └── playbooks/  asr · document · text · tabular · embeddings
├── policies/     run-policy · levers · priors · cause-map
├── schemas/      objective · brief · verdict · plan
├── scripts/      studio (resolve) · validate · critique · stats · manifest · notebook · backend · run · diagnosis · report · review · freeze · qa · build · revise · postmortem
├── fixtures/asr-register-adapter/   audio · brief · objective · verdict · plan · materials-index.jsonl
├── fixtures/dairy-record-classifier/ document · same shape
├── evals/data/   hypothetical actuals to exercise postmortem scoring
└── evals/evals.json · run_evals.py (fourteen mechanical evals: failure modes, one per lens, postmortem)
```
