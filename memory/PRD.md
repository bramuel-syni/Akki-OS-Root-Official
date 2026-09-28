# Akki — product requirements and current continuity

## Original problem statement

Deeply understand, assess and operate Akki Extraction under strict architectural
and governance rules. Wire DAP requests, work history and entitlement lifecycles
to actual engines; reconcile the 648-row requirements assessment against genuine
closure evidence rather than fixtures or claims. Preserve frozen Canon contracts,
one authoritative append-only ledger, and 100% fidelity to owner HTML prototypes.

## Users and boundaries

- Estate owners/tenant approving authorities commission governed read-only census
  and separately scoped extraction, answers, evaluation and delivery.
- Work users consume scoped results/history; operators administer controls and
  independent inspectors establish evidence without inheriting worker authority.
- **E1 is NEVER the estate-data execution path.** E1 wires admitted descriptors;
  a local subprocess or HTTPS source SDK does not itself establish an external
  admitted runtime. Do not manufacture admissions, signatures or trust roots.
- Owner authorises independent non-GPU work; no fresh blanket approval is needed.
  GPU/SSH recovery remains PARKED; no blind retries or credential changes.
- English only. Keep source credentials in ignored custody, not chat/reports/UI.
- Source requirement text is immutable; hardening is a versioned derivative.
- A schema, chat ruling, ordinary login or historical fixture is not a live
  signed approval. Use existing rulings/defaults before requesting owner decisions.

## Architecture

- React frontend, FastAPI, MongoDB. URLs/credentials/database configuration use
  existing environment variables. API routes use `/api`.
- Bootstrap: `/app/backend/server.py`; runtime:
  `/app/backend/vendored/extraction_akki/backend/`.
- Canonical ledger: `services/ledger_writer/{principal_control,mongo_control}.py`.
- Coordination: `services/northena/execution_*.py`; Mkondo native handoffs;
  Mtafiti registry; `services/activation/`; `services/non_gpu_governance/`.
- DAP: `routers/portal_requests.py`, `services/portal_operational/`.
- Census: `services/census_autonomy/` including `census_router.py`,
  `jump_dispatch.py`, `rds_data_dispatch.py`, `obs_dispatch.py`,
  `non_gpu_census_worker.py`, `census_dq_producer.py`.
- UI: owner prototype/OwnerMarkup composition. Do not redesign CSS/layout/DOM.
- Credentials unchanged: `/app/memory/test_credentials.md`; estate access is
  held in ignored `/app/backend/estate_keys/owner_20260928/`.

## Current checkpoint — 2026-09-28, descriptor requirements review

Owner: “Attached are some of the requirements. NAS - mounted on: /mnt/nfs-share.
You now have data to close alot of the gaps. What is pending from me?”
Then quoted the previous “everything verified”, ~35% and live census report.

Reviewed files (20).zip: six JSON schemas (source/query/worker/inspection/custody
descriptors and admission record) plus an 18-entry inventory. All six schemas
pass Draft 2020-12 meta-validation. Direct workbook inspection: all 18 location
cells and all 18 status cells blank. These are contracts/inventory, not populated
verified descriptors or signed admissions. Originals retained unchanged at
`assessment_workspace/incoming/requirements_files20/`, hashes in report below.

Authoritative current owner-action reconciliation:
`assessment_workspace/notes/descriptor_requirements_20260928/OWNER_PENDING.md`.

### Owner dependencies, limited to affected work
- Workbook explicitly lacks identity drops for RMS Fred Afune / Muthoni Kiarie /
  Samuel Kibacia and DigiCow Vincent Kimani / Peninah Wanja. Recover custody refs
  first; missing identity/mandate evidence goes through existing tenant custody.
- artists_app previously denied; owner earlier said “ok”. Do not assert GRANT was
  applied. Only continuing denial after confirmed update needs narrow admin access.
- Historical missing-source clauses: SV extension 11, ROC 11, deck DR-R10/R13 two.
  New archive contains none. Recovery is E1's first task, then precise owner sources.
- Seven historical decision rows are EP-1–4 adoption, A18.6 async delivery, BC-3/4
  continuity policy — NOT seven numeric thresholds. Reconcile existing rulings;
  only genuinely missing policy decisions return to owner at their affected gate.
- AISCA/GPU administrator dependency stays parked, not a non-GPU blanket blocker.

### Engineering work, not more owner inputs
- Verify NAS mount host/admitted-worker/read-only scope; mount path alone proves
  neither NFS/CIFS nor successful census. Do not request SMB password by default.
- Populate descriptor inventory and pin recovered actual worker/inspection/custody
  evidence; recover D-18 pilot and AKKI-TEST records, not replace existing authority.
- Platform-principal MT-13 workflow and explicitly SYNTHETIC test estates are E1
  build tasks; DigiCow tenant web access is engineering/admission wiring.
- Qualify worker separation/admissions, real DQ/extraction/answers/metering/delivery.

### Evidence corrections
- Prior report records real aggregate reads: RMS 20 databases/1,015 tables/~257M
  estimated rows on six hosts; DigiCow 239 tables/~5.9M estimated rows; OBS 106
  bucket listing. These are HISTORICAL, not rerun in this review, not full content
  census or full product/security/admitted-runtime certification.
- Current RDS/OBS dispatchers call SDKs directly; hash-derived worker receipt IDs
  and execution_location strings are not signed runtime admission/independence.
  These findings are engineering follow-up, not credential requests or live fixes.
- ~35% is an unreconciled estimate; old remaining shares total 93%. Do not assert
  built-and-proven programme percentage until row-level reconciliation. No new %.
- Broader positive answer/model/custody/governance fixtures remain
  **SYNTHETIC/MOCKED**; live end-to-end acceptance is not established.
- This turn changed assessment/continuity documentation only. No app/config/auth/
  credentials/UI changed, no source/GPU reads, no new admission or certificate.
  Prior 733-test result is historical, not a new regression run.

## Continuity and priorities

- `ROADMAP.md`: latest P0/P1/P2 ownership and historical roadmap.
- `CHANGELOG.md`: implementation/review history and verification.
- `ARCHIVE_PRD_BEFORE_DESCRIPTOR_REVIEW.md`: exact prior 761-line PRD preserved;
  includes detailed 2026-09-27/28 controls/UI/non-GPU implementation checkpoints.
- `ARCHIVE_PRD_BEFORE_ACTIVATION_CONTROLS.md`: earlier history.
- Original audit: `notes/full_requirements_gap_20260926/REQUIREMENT_GAPS_648.csv`.
- Decision ownership: `notes/consolidated_fix_plan_20260926/DECISION_AND_BLOCKER_REGISTER.md`.
- Accepted owner v1.1 activation inputs remain final desk handoff; no generic
  revision questionnaire. See `notes/live_activation_v1_3_artifact_review/revision_v1_1/`.
- Next: versioned descriptor/admission integration and evidence reconciliation,
  admitted non-GPU mount/source verification, then real governed path proofs.
  Preserve current authority, prototype fidelity and parked GPU boundary.