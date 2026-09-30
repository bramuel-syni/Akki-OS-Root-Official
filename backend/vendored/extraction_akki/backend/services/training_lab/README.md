# Akki training laboratory

This is an evidence-first, **advisory** callable lab. It is not a universal trainer, independent professor, admission authority or unrestricted research agent.

## Callable contract
Use the existing admitted operator bearer identity and tenant context.

| Endpoint | Behaviour |
|---|---|
| `GET /api/training/lab/skills` | Five specialist roles, four deterministic tools, modality playbooks and holds |
| `POST /api/training/lab/runs` | Durable RMS assessment of existing staged data and/or historical aggregate evidence. Requires `Idempotency-Key`. Returns 202. |
| `GET /api/training/lab/runs/{id}` | Tenant-scoped evidence, measured inventory, reviews, receipts and blockers |
| `POST /api/training/lab/runs/{id}/review` | One explicit nonrecursive research correction pass over existing aggregates; idempotent |
| `POST /api/training/lab/skills/statistics/invoke` | Wilson counts, real paired/group bootstrap, power-law prior scenarios, empirical monitoring thresholds |
| `POST /api/training/lab/skills/music/invoke` | Classify caller-supplied calibrated event probabilities; **not audio inference** |
| `POST /api/training/lab/skills/value/invoke` | Discounted adoption-adjusted NPV, delay and next-best comparison; no spend approval |
| `POST /api/training/lab/skills/postmortem/invoke` | Score referenced predictions; no automatic prior/role-weight update |
| `GET/PUT /api/training/lab/watch` | Bounded development-checkpoint review opt-in; never starts training |

Background work is persisted in existing MongoDB collections `training_lab_runs`, `training_lab_watch`, `training_lab_webhooks` using the existing `MONGO_URL`/`DB_NAME`. Queue claims use compare-and-set leases. Lost dispatch acknowledgement/interrupt during review holds rather than blindly repeating worker actions/provider spend. Restarted queued/inspection work resumes on the next schedule tick. Idempotent replays are reads, not fresh Watch commissions.

The platform schedule is `/app/.emergent/crons.yml`. `/api/training/lab/cron` validates `WEBHOOK_CRON_SECRET`, deduplicates delivery IDs and immediately acknowledges before background processing. Actual recurring delivery must be observed before claiming an always-on service. Checkpoint payloads expose development aggregates only; max reviews per job limits provider cost. No polling thread/daemon is installed.

## Model boundary
`reviewers.py` delegates exclusively to `services.chokepoint.llm.invoke`, purpose `training_lab.advisory_review`, with per-role session IDs. Configuration in backend environment: `TRAINING_LAB_CONNECTION`, `TRAINING_LAB_MODEL_PROVIDER`, `TRAINING_LAB_MODEL`. Existing connected universal key is reused; not stored in source. Model selection fails closed for this purpose. No raw corpus, transcript, arbitrary client prompt, path, shell command or provider-supplied code is sent/executed.

Model advice is schema/reference checked. Numerical prose and unsupported URLs are flagged; numbers remain in deterministic evidence. This detects some mistakes, not arbitrary hallucinations. An incomplete/flagged review is `partial`/`review_required`, not cleanly accepted. Independent domain review remains necessary for quality claims.

## Source package and limits
The owner's archive is preserved under `assessment_workspace/attachments/training_lab_20260930`; the imported resource is `skill/`. Existing doc-studio/surface-studio were not overwritten. `INSTALL_MANIFEST.json` records original and installed hashes.

Corrections: Wilson interval honestly named; actual item/group bootstrap added; the runner now uses a bounded power-law prior-scenario fit rather than log-linear forecasts; unsupported forecasts are not clipped to available data; unavailable strata are excluded from partial cost recommendations and full-run affordability is false. Diagnosis remains explicitly unvalidated. No numeric monitor threshold is invented without calibration samples. Model playbooks and value/postmortem tools supplement, not retroactively validate, the synthetic examples.

The package's legacy `RealBackend` still refuses execution. Actual admitted worker dispatch is `lab_inspect`, read-only staged headers plus a SYNTHETIC H200 head smoke test. It does not train a music detector. All training, model activation and serving changes remain held until owner approval and qualified evidence.

Tests: `backend/tests/census_operational/test_training_lab_audio_scope_live_iteration70.py`, `backend/tests/m8_m9_completion/test_completion_offline.py`, plus `PYTHONPATH=<vendored backend> python skill/evals/run_evals.py`. Fixture tests are **MOCKED/SYNTHETIC**, not model acceptance.