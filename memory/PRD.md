# Akki — continuity record

## Mission and original requirements

Operate and assess the governed Akki extraction platform against its on-disk Canon. The owner requires a deep, evidence-based account of what is actually implemented, wired, executed, incomplete, or unverified. No assumptions, invented data, or completion inferred from heartbeat/test counts.

**Critical boundary:** E1 wires connector descriptors into the Census Autonomy Service. Akki's infrastructure executes estate pulls and training. This pod is never the estate data path.

## Architecture

- FastAPI `/app/backend/server.py` assembles routes from the canonical backend when present or `/app/backend/vendored/extraction_akki/backend` otherwise.
- React `/app/frontend/src` has native `/dap` and `/os` routes and historical prototype-related code.
- MongoDB configuration is environment-owned; filesystem records also exist under `assessment_workspace/phase0`.
- Primary rules, amendments, decisions, historical receipts, and build records are under `/app/assessment_workspace`.
- Do not conflate a connected GPU, a reachable pod SSH identity, and a completed training job.

## Current task — 2026-09-25

Owner approved read-only Canon-to-code review before GPU remediation. Audit scope: `/app/assessment_workspace/notes/canon_code_audit_20260925/SCOPE.md`.

Status: **VERIFIED FINDINGS REPORT DELIVERED; EXHAUSTIVE AUDIT STILL OPEN.** Earlier handoff conclusions were independently challenged, not copied. The report does not claim all Canon clauses, amendments, historical records or execution paths have been discharged.

## Audit artifacts — 2026-09-25

Under `/app/assessment_workspace/notes/canon_code_audit_20260925/`:

- `REPORT.md`: detailed positive/negative functional findings, file-and-line citations, limitations and priorities.
- `SCOPE.md`: owner's verbatim request, proposed scope and approval.
- `source_inventory.json`, `read_coverage.json`: 119 Canon files inventoried; 15 source texts fully read, byte-equal duplicates identified and later Document-0 ruling differences reviewed. Reading is explicitly distinct from clause-to-code verification.
- `runtime_get_receipt.json` and `get_00.json`–`get_09.json`: ten current external preview GETs, response hashes; 215 OpenAPI paths / 228 operations.
- `authenticated_read_receipt.json` and `auth_get_00.json`–`auth_get_06.json`: existing operator login 200 and seven read-only portal checks.
- `autonomy_result_receipt.json`: all 12 local autonomous result payloads carry the placeholder execution note; no new job submitted.
- `akki-audit-desktop.jpeg` (1920×800), `akki-audit-mobile.jpeg` (390×844), console log: existing DAP baseline, mobile sidebar/content squeeze.
- `report_validation.json`: explicit prefixed source citations checked for existence/range and hashed; shorthand references not mechanically resolved. No invalid checked citations at close. Bibliographic checks are not application regression tests.

Audit-only extraction utility: `/app/assessment_workspace/tools/canon_code_audit_inventory_20260925.py`. It does not access estates. Generated corpora are documentary derivatives, not additional operational stores.

## Verified findings / corrections

1. GPUs: real key hardening and successful historical GPU work are evidenced. Current hardware failure or pod-key mismatch was NOT established; no GPU login/auth/key changes attempted. Real text-training receipt includes its historical owner-authorized build bypass; do not erase either the successful work or that limitation.
2. Runtime inventory: 1,004 Python files, 130 immediate service directories (excluding `__pycache__`), 52 JSX page files. These counts are NOT capability-completion percentages. Helpers may execute through transitive consumers.
3. Autonomous census: adapters, registration/bridges and scheduling entry point exist; the inspected permitted engine branch writes a placeholder result then COMPLETE without calling the adapter/job executor. Historical result payloads reproduce this. Legacy real census/training paths do not cure this specific consumer gap.
4. Census 4: retained metadata-only pass shows 8 clusters, 41 databases, 2,642 tables and 428,786,937 ESTIMATED rows; null counts deferred, Digicow RDS not walked. Its recorded direct-pod path is not evidence of current architecture compliance and must not be repeated.
5. Authenticated portal census list returns only [1,2,3]; detail 4 is 404 while `/api/census/latest` returns 4. Anonymous legacy census reads expose topology despite the newer portal read gate; this difference is confirmed by GETs and the owner read-gating instruction retained in `routers/portal_census.py:26-31`. Registry component does fetch an API; stale backend projection and source literals must be distinguished from wholesale frontend fabrication.
6. Portal requests/entitlements are mounted but have STUBBED bindings. Submit returns 202 acknowledgement without persisted commission; entitlement handlers return null licence, empty rows/badges, and allowance derived from an empty event list / fixed period.
7. Callable-skill provision/store/gate exists; query answer is STUBBED via `answer_stub`. DAP skill read hook exists but reads `localStorage.dap_jwt`, unlike normal login's `sessionStorage.akki_access_token`; static mismatch not browser-replayed.
8. Actual LLM crossing file is `services/chokepoint/llm.py`, NOT handoff's nonexistent `services/synisense/shield/llm.py`. Real crossing mechanics exist; receipt-failure and input-score wiring limitations remain.
9. Training has distinct paths: legacy LoRA passes None dependencies; campaign production trainer supplies real dependencies but its traced consumer is an older pod launch tool; language-cognition helper returns a commission handle rather than launching. No blanket “all training mocked” verdict.
10. Real TCB/triad/classification, five-class Mtafiti inventory, Northena run records, Watch split, Targeta deterministic filtering, CIF proposal routing, audio provenance/clustering/calibration contracts exist. This is not proof of every broader end-to-end promise. Several older documentary “not built” conclusions are stale.

No application features were added or bugs fixed. Existing gaps remain intentionally unchanged under the approved read-only scope.

## Priorities

- P0: Complete remaining Canon/amendment/Master Requirements Registry row mapping and authority reconciliation. Trace remaining Solva, memory, rule service, budget/model admission, universal handoffs and all UI paths. Do not relabel unreviewed areas “not built.” See report §13.
- P1: Only after the audit, diagnose an evidenced GPU identity issue through Akki's existing pipeline; user authorized recovery, not speculative host changes. Then correct existing autonomous executor/descriptor and registry/portal joins against approved scope—no competing pod extraction path.
- P2: Actual content-quality/FK/dedup measures, language-cognition corpus/calibration/MOAC/admission, source-aligned regression suites and responsive defects. DQ-25/HF/location blockers from old notes are historical until freshly evidenced.

## Verification limits

No application changes or estate access in this audit. Verification was source examination, external API read checks and desktop/mobile observation; no current full-suite pass claim. Historical test results must retain their original scope and timestamp. The vendored `test_*.py` match is a production `services/training/test_set_seal.py` module, not the historical full suite. Test credentials were documented from existing source; only operator login was tested. Never request new credentials or reset accounts just to reproduce this audit.

Potential improvement after audit: expose measured/estimated/not-read freshness from existing Mtafiti receipts on the existing registry, without creating a second authority.