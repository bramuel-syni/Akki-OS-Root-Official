

<!-- AUDIT-PREP-20260921 · state Commit-A · 2026-09-21T18:20:00Z BEGIN -->

## AUDIT-PREP-20260921 · owner-directed audit-target seal · 2026-09-21T18:20:00Z

Owner directive verbatim (2026-09-21T~17:35Z, reissued self-running after prior stop-and-report on Step 3b ledger block; owner elected the O3 fixture-via-sealed-code path):

> *"OWNER RESPONSE RECEIVED — the owner saw your stop-and-report (the 3b block finding was relayed verbatim with options O1-O4) and answered by REISSUING the audit-prep directive as SELF-RUNNING, with the ledger export still in scope and delivery expanded to FOUR hashed files. Read this as the owner electing the O3 path implicitly: complete step 3 via the sealed code paths, not fabrication. Execute now, self-running, steps 1-5 before any other work. Terminal-only, no testing agent, no push, no fetch, additive-only, ratchet floor 5858, R-91 untouched until post-horizon boundary."*

Full owner steps 1-5 executed in order:

### Step 1 · Annotated tags at sealed heads

| Tag | Repo | Points-to commit | Tag object SHA |
|---|---|---|---|
| `audit/code-20260921`  | `repos/Extraction-Akki` (`programme/track-a`) | `283524d89dd337d79014b114d575ced7baab6dfc` (CP-PROD-DEPLOY-SELF-CONTAINMENT · Commit-A) | `d02e76f4e4538e1747cbd26f3e5494b79066f5bb` |
| `audit/state-20260921` | `assessment_workspace` (`master`)             | `18b4d8566fa99292d07dee6b0b5c4f287040d499` (HUAWEI-OBS-ACCESS-DRILL + CP-ESTATE-INGESTION wave-card AUTHORED) | `3e14f1a3bcca45bddcbccd36cf2caf951d8c80ea` |

Both cut with `git tag -a` (annotated), local only, no push. Verified via `git rev-parse` and `git bundle verify`.

### Step 2 · Builder Status column filled on all 602 rows

Source workbook downloaded from
`https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/k5zn1120_Master_Requirements_Registry_QA_v2.xlsx`

- **Pre-fill workbook sha256**: `98240bde0755bdd6aec9eb7022880be1ec94760e6367d193f9eedc1a41a8a93f` — **matches** owner's cited prefix `98240bde…a8a93f` verbatim. **No discrepancy.**
- **Filled workbook sha256**: `8fde06a682f55d65ea55d26776facaad5070e33293a65aface2ed31e63e14b75`
- **Path**: `/app/audit/inbox/Master_Requirements_Registry_QA_v2_builder_status.xlsx`

Trace method (deterministic, banked at `/app/audit/tools/build_builder_status_v2.py`): for every rule, look for a verbatim rule-ID mention (with word-boundary hardening) in any invariant test file's content; for A5.x/B5.x/C5.x anchors additionally require the Doc-N context to co-occur in the file; if match found AND that test file is **not** in `baseline_failures.json` → **BUILT**; else if match found but file IS in `baseline_failures.json` → **PARTIAL**; else if the Domain resolves to a present service package under `backend/services/` → **PARTIAL** (service scaffolding, no invariant naming this rule); else → **NOT BUILT** (no citation).

- **Distribution**: **BUILT = 297 · PARTIAL = 293 · NOT BUILT = 12** (total 602).
- **NOT BUILT rows (all 12, honest)**: `A18.1..A18.3, A18.5, A18.8` (Doc 18 Skills layer cross-cutting), `BR-11.1, BR-11.2` (Governance Architecture · MOAC), `G-2, G-6, G-7` (Governance Architecture gap register — these are OPEN gaps flagged in the Build Status sheet itself), `AC-8, AC-9` (Agent Containment composition layer, outside the six).
- By-prefix table available at `/app/audit/scratch/builder_status_summary.json`.
- Only column K modified; every other cell (including all formula cells across all 10 sheets) is byte-identical to the source workbook — verified programmatically before save.

### Step 3 · Ledger fixture via SEALED code only

Prior stop-and-report finding recap: no production tenant chain exists at `audit/code-20260921` — no `receipts.jsonl`, no `seq-*.json`, no persisted chain anywhere under `/app`. Owner authorised path: generate an explicitly-labelled fixture through the sealed writer + verifier.

- **Tenant**: `AUDIT-FIXTURE-20260921` (labelled fixture, not production data).
- **Driver script**: `/app/audit/tools/generate_ledger_fixture.py` — **outside the sealed code tree**; imports only sealed modules from `repos/Extraction-Akki/backend/`; zero modification to `services/`, `contracts/`, or `tests/`.
- **Sealed surfaces used**: `contracts.ledger_credentials.LEDGER_VERIFIER_CRED_HANDLE`, `contracts.ledger_v1.LedgerRow / LedgerRowAt / canonical_row_bytes`, `services.ledger_emitter.emit_intent.LedgerIntent + emit_intent`, `services.ledger_writer.main.append_intent + OutOfOrderSeqRefused + compute_row_hash`, `services.ledger_verifier.receipt_store.VerifierReceiptStore`, `services.ledger_verifier.verify.verify_chain + VerifierReceipt`.
- **Segment bounds**: seq **1 → 6**, row_count = **6**, chain intact (`break_at_seq is None`), head hash `548b3d9bafcaec19ace23bc92520f03617dddde915c75d2120285f67ca7d78a0`.
- **Refused-operation rows**: **seq 3** (`event_type="refuse"`, `decision="refused"`, `reason_code="publication_gate_denied"` — from `services/memory/memory_refusal_reasons.v0.json`) and **seq 5** (`event_type="refuse"`, `decision="refused"`, `reason_code="composition_below_floor"` — from `services/compliance/refusal_families.v0.json`). Both are real refusal families in the sealed compliance registries.
- **Sealed-writer refusal path also exercised**: `append_intent(seq=99, prev_row.seq=6)` deliberately drove `OutOfOrderSeqRefused` (code `LEDGER-WRITER-001`); refusal captured under `sealed_writer_refusal_demonstration` in the snapshot. This is a **real** refusal raised by the sealed writer, not a hand-crafted row.
- **Verifier receipt store**: `/app/audit/inbox/verifier_receipt_store/akki.ledger.verifier.credential.v0/AUDIT-FIXTURE-20260921/seq-000000000006.json` — created via `VerifierReceiptStore(credential_handle=LEDGER_VERIFIER_CRED_HANDLE, storage_root=…)` with the positive-allowlist C3 gate honoured.
- **Chain snapshot**: `/app/audit/inbox/ledger_snapshot_AUDIT-FIXTURE-20260921.json` — carries provenance block with "not production data; generated 2026-09-21 via sealed ledger_writer/ledger_verifier; no production tenant chain existed at export time".
- **README**: `/app/audit/inbox/README_fixture.md` — auditor-facing explanation.
- **Track-a tree unchanged**: `git status` on Extraction-Akki still shows exactly the same 17 pre-existing `__pycache__/*.pyc` file modifications (all `Bin X → X` size-unchanged except `doc0_attributes/tcb.cpython-311.pyc` which shows `Bin 2996 → 3970` — carried over verbatim from before this wave; mtimes `2026-09-21T08:22Z` predate this wave). **Zero new tracked-file modifications introduced by this wave.**

### Step 4 · Delivery — all deliverables at `/app/audit/inbox/` + all five hashes

Owner asked for four hashes; two-repo topology forces five (two bundles). Count discrepancy flagged here as owner directed.

| # | Deliverable | Path | sha256 |
|---|---|---|---|
| 1 | Code bundle (Extraction-Akki: `programme/track-a` + tag `audit/code-20260921`) | `/app/audit/inbox/akki_audit_20260921_code.bundle` | `f1037cc7aee19dee048c75d8f04bfd2ca46737bda9eb792ac96ee2a95d964ad7` |
| 2 | State bundle (`assessment_workspace`: `master` + tag `audit/state-20260921`) | `/app/audit/inbox/akki_audit_20260921_state.bundle` | `7e6bb1aebe151a8ddcc6a3ddcb2cb06d3c69685864002fffc949f61eeedbaece` |
| 3 | Filled Master Requirements Registry (Builder Status col K, all 602 rows) | `/app/audit/inbox/Master_Requirements_Registry_QA_v2_builder_status.xlsx` | `8fde06a682f55d65ea55d26776facaad5070e33293a65aface2ed31e63e14b75` |
| 4 | Ledger snapshot (fixture chain, seq 1..6, tenant `AUDIT-FIXTURE-20260921`) | `/app/audit/inbox/ledger_snapshot_AUDIT-FIXTURE-20260921.json` | `ad2d70e920b128f5973aa265e2afc4fbec19ee6fe75acb5531473e0ae3a96a7a` |
| 5 | Verifier receipt store — deterministic tar (`--sort=name --mtime='UTC 2026-09-21' --owner=0 --group=0 --numeric-owner`) | `/app/audit/inbox/verifier_receipt_store.tar` | `136cb601ba35fa3b0c2e6ab48f9d374f9a45460ec169db6e59053aa1df1bb7b0` |

Provenance reference (not counted): raw pre-fill workbook sha256 `98240bde0755bdd6aec9eb7022880be1ec94760e6367d193f9eedc1a41a8a93f` (matches owner cited).

Both bundles verified with `git bundle verify` reporting *"is okay"*; both include their respective `refs/heads/…` HEAD and their `refs/tags/audit/…` tag; each records "a complete history".

Fixture provenance line (owner directive verbatim, banked in README + snapshot): *"audit fixture generated 2026-09-21 via sealed ledger_writer/ledger_verifier; not production data; no production tenant chain existed at export time."*

### Step 5 · State Commit-A (this entry) + PINS.md pin (paired append)

- Bundle sha pins for both bundles landed at `STATE/PINS.md` under a fresh `<!-- AUDIT-PREP-20260921 · 2026-09-21T18:20:00Z -->` block.
- BASELINE_GUARD=1 PYTHONHASHSEED=0 double-green byte-identical sweep on `programme/track-a`: **not applicable** — the track-a tree did **not** change during this wave (owner explicit: "if the track-a tree changed (it should NOT change in this wave — if it did, stop and report why first)"). Confirmed by `git status` on Extraction-Akki showing zero new tracked modifications (only the 17 pre-existing `.pyc` mods carried over from before this wave).
- No push. No fetch. No remote configured. Local `git tag -a` + `git bundle create` + `git commit` only.

### R-91 & standing bounds (unchanged this wave)

R-91 remains PARKED at horizon `2026-09-23T03:23:15Z` (~33h out at 2026-09-21T18:20Z). Not touched. Post-horizon boundary rule applies (per owner reissue §5): the M1-to-date BUILD_JOURNAL closure remains the exit artefact for the next boundary AFTER R-91 fires, pointing at the tags cut this wave.

Ratchet floor **5858** — unchanged this wave (no baseline mutation attempted). `baseline_failures.json` sha256 `5266564fdfa09d6977b1684293864ef361754444cfb6178f4e3fdb1b5e6117cb` — unchanged.

HF-HOLD SEC-2026-09-12-01 · R-24 UNLISTED · R-25 tagged · structural §3.8 guard on `services/request_context/context.py` sha-pin `ad0d9439…` · all unchanged.

### Autopilot next (per owner reissue §6 · HOLD)

- **HOLD**. Do not open any owner-gated S4 estate sub-slice without an explicit GO.
- Estate track resumes only on already-authorized gated items.
- Any future R-91 ε-apply at the horizon must, per owner reissue §5, seal-then-write the M1-to-date BUILD_JOURNAL as the exit artefact pointing at `audit/code-20260921` and `audit/state-20260921`.

**End of AUDIT-PREP-20260921 wave card.**

<!-- AUDIT-PREP-20260921 · state Commit-A · 2026-09-21T18:20:00Z END -->
