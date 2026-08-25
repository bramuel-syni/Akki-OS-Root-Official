# Training-run rates register · W7 CP1

Adapter-training-run economics anchor.

Anchors:
- Doc 13 §20 — workers execute adapter-training steps under Targeta's plan.
- Doc 14 §32 — licence-verified baseline curation carries rate on record.
- MOAC.5 (Canon 4 §26.5) — cost per operation, measured on real load.

## Discipline

- OWNER-SUPPLIED FACTS or ABSENT. Never invent a rate (Canon 1 §4.4).
- One rate per file. Filename convention: `<training_id>.json`.
- Row schema (see services/cost_ledger/rates.py::rate_for_training_run):
  ```json
  {
    "training_id": "adapter-<name>-<yyyy-mm>",
    "kind": "adapter_training_gpu_hour" | "adapter_labelling_per_1k_tokens" | ...,
    "rate_per_gpu_hour": <number>,           // OR rate_per_1k_tokens, etc.
    "currency": "USD",
    "authored_at": "<ISO-8601 UTC>",
    "source": "<owner_channel_reference>",
    "notes": "<optional short note>"
  }
  ```
- Banned fields: `key`, `api_key`, `secret`, `token`, `credential` (Owner Order 2026-08-25 §4).

## State at W7 CP1 open

**HONESTLY ABSENT.** No rate rows on record. The Cost Ledger will render training
quantities with the HONEST_GAP_SENTENCE until the owner authors rates here.
