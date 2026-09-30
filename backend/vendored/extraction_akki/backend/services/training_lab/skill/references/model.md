# Model grammar — TargetOutcome and materials
- `population.strata.STn`: label, share, `test_set_ref` (must resolve to a receipt), `test_n`, class, receipt. The test set precedes the training (Doc 17 §17.3).
- `baseline`: per-stratum accuracy and coverage from a recorded run, with receipt.
- `acceptance.per_stratum.STn`: `accuracy_floor` and `coverage_floor`. Both are required: a global threshold hides the "94% majority, 61% minority" failure (A17.19b). `gate_policy`: `gates` by default; `ships-documented` only as an explicit per-objective override.
- `collection_schema`: unit, fields, quality gates, labelling protocol, admission rule (A17.20's second artefact). Class estimated; receipt to the objective owner's sign-off.
- `materials.Mnn`: source, stratum, examples, class, lawful basis (consent | licence | contract | public-task), basis_ref, hash, receipt. Backed by `materials-index.jsonl`, one row per example: example_id, source, stratum, class, lawful_basis, basis_ref, content_hash (+ modality fields). Objective counts must equal index counts; a number without rows is a datasheet claim, not provenance. The manifest built from the index is hashed and its hash travels into the run record, the MOAC pack and the certificate (#24: every example traceable).
- `base_model`: the CI fixture only until the census names a production base (A17.10–11).
- `calculations`: named derivations; the resolver computes them.
- `coverage`: what the objective covers and what it cannot say.
Classes: measured / estimated / sample / observed. A trained model's guarantee is provenance of ingredients, never of assertions (A17.16).

## Lens inputs on the objective
- `task_family` and `modality_key`: select the priors and the playbook.
- `value.per_stratum`: value in the business's terms with its basis (entrepreneur).
- `production`: capture condition and monitor per stratum, owner seat, rollback, retrain cadence (industry).
- `annotator_agreement` per stratum (professor; label-noise test).
- `test_set_custody`: who sealed it, whether any training decision has seen it, reuse count (professor).
