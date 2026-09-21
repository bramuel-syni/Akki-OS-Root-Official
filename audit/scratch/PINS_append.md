

<!-- AUDIT-PREP-20260921 · 2026-09-21T18:20:00Z BEGIN -->

## Audit bundle sha256 pins · AUDIT-PREP-20260921 · 2026-09-21T18:20:00Z

Owner directive verbatim (2026-09-21T~17:35Z, reissue after O3 election):

> *"Pin both bundle shas in STATE/PINS.md."*

Bundles produced by local `git bundle create` on each repo at their respective annotated audit tags · zero remote · zero push · offline-reconstructable · included in `/app/audit/inbox/` alongside the filled workbook + ledger snapshot + verifier receipt-store tar.

| Repo | Workdir | Branch | Bundle file (in `/app/audit/inbox/`) | Refs bundled | Bundle sha256 |
|---|---|---|---|---|---|
| code · Extraction-Akki | `/app/assessment_workspace/repos/Extraction-Akki` | `programme/track-a` | `akki_audit_20260921_code.bundle` | `refs/heads/programme/track-a` @ `283524d89dd337d79014b114d575ced7baab6dfc` + `refs/tags/audit/code-20260921` @ tag-object `d02e76f4e4538e1747cbd26f3e5494b79066f5bb` (→ same commit) | `f1037cc7aee19dee048c75d8f04bfd2ca46737bda9eb792ac96ee2a95d964ad7` |
| state · assessment_workspace | `/app/assessment_workspace` | `master` | `akki_audit_20260921_state.bundle` | `refs/heads/master` @ `18b4d8566fa99292d07dee6b0b5c4f287040d499` + `refs/tags/audit/state-20260921` @ tag-object `3e14f1a3bcca45bddcbccd36cf2caf951d8c80ea` (→ same commit) | `7e6bb1aebe151a8ddcc6a3ddcb2cb06d3c69685864002fffc949f61eeedbaece` |

Both bundles verify with `git bundle verify` reporting *"is okay"* + *"The bundle records a complete history"*.

Companion deliverables (hashed for auditor cross-check, not bundle pins):

| Deliverable | Path | sha256 |
|---|---|---|
| Filled workbook (Builder Status col K, all 602 rows) | `/app/audit/inbox/Master_Requirements_Registry_QA_v2_builder_status.xlsx` | `8fde06a682f55d65ea55d26776facaad5070e33293a65aface2ed31e63e14b75` |
| Ledger snapshot (fixture chain, seq 1..6, tenant `AUDIT-FIXTURE-20260921`) | `/app/audit/inbox/ledger_snapshot_AUDIT-FIXTURE-20260921.json` | `ad2d70e920b128f5973aa265e2afc4fbec19ee6fe75acb5531473e0ae3a96a7a` |
| Verifier receipt-store deterministic tar (`--sort=name --mtime='UTC 2026-09-21' --owner=0 --group=0 --numeric-owner`) | `/app/audit/inbox/verifier_receipt_store.tar` | `136cb601ba35fa3b0c2e6ab48f9d374f9a45460ec169db6e59053aa1df1bb7b0` |
| Raw pre-fill workbook (matches owner cited `98240bde…a8a93f` verbatim) | `/app/audit/scratch/Master_Requirements_Registry_QA_v2.xlsx` (scratch, not tracked) | `98240bde0755bdd6aec9eb7022880be1ec94760e6367d193f9eedc1a41a8a93f` |

Standing bounds unchanged. Zero-push discipline unchanged.

<!-- AUDIT-PREP-20260921 · 2026-09-21T18:20:00Z END -->
