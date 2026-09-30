# Trainer backend contract (for the A17.12 runner build)
`scripts/backend.py` defines `TrainerBackend` with three calls. The runner uses nothing else, so the real adapter replaces the stub without touching the runner.

| Call | Input | Returns | Rules |
|---|---|---|---|
| `calibrate(stratum, volume, manifest_slice_ref, arm)` | one stratum, one volume, a slice reference into the hashed manifest | accuracy, coverage, gpu_hours, checkpoint_ref | evaluates on the sealed test set only; checkpoints every N steps per recipe (C.20.6); reads go through the custody seam (Doc 1) |
| `compare(stratum, volume, arms, manifest_slice_ref)` | the smallest valid stratum, the last calibration volume, two optimizers | per arm: calibrate result + compute_to_convergence_gpu_hours | identical data, base model, eval set, compute cap (A17.5); never a verdict |
| `full(per_stratum_examples, recipe_version, manifest_ref)` | the quoted volumes, the ruled recipe, the manifest hash | completion-certificate fields (policy.completion_certificate.fields) | never called before the Owner verdict is recorded and the objective owner's milestones are agreed; budget exhaustion halts and discards unless the recipe declares partial artefacts acceptable (C.20.6) |

Environment: `AKKI_EXECUTION_MODE ∈ {cuda, cpu}` read at import; unset or invalid raises (A17.9); `execution_mode` attributed in the run record and telemetry. Reproducibility: seed-fixed re-run within policy tolerance; second-run evidence lands in the MOAC pack under C8-repro. The adapter returns numbers; eligibility, acceptance and admission are computed and ruled elsewhere.
