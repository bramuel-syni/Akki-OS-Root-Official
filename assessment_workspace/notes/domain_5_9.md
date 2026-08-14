# Domain 5.9 — Orchestration (Canon 9 · Mkondo Charter)

Scope (instruction §5.9): record matrix · task-identity register · handoff
contracts. Search all four repos for anything resembling a record-class
registry or identity-per-task discipline; classify honestly (likely BUILD).

## Method — absence search

Term set searched across `git ls-files` of all four repos:
- Canon-9 named: `mkondo`, `orchestrat`, `task_identity`, `record_matrix`, `record_class`, `handoff`, `charter`, `writer_of`, `authority_bound`, `task_class`
- Content-based: `grep -rln 'record_class\|task_identity\|writer_authority\|WRITER_MAP\|RECORD_MATRIX' backend/`

## Result

| Match | Location | Nature |
|---|---|---|
| `backend/routers/handoff.py` | RMS-IQ-Core-2, Akki-OS-V1, Extraction-Akki | Wizard→extraction admission handoff route (Doc 4 §18 Seam-1). Read-only route (test `test_handoff_route_readonly.py`). This is ONE specific handoff, not the Canon-9 handoff CONTRACT REGISTRY. |
| `backend/services/wizard/admission_handoff.py` | RMS-IQ-Core-2, Akki-OS-V1, Extraction-Akki | Wizard→admission handoff logic (Seam-1). Same as above. |
| `docs/handoff/*` | All three core repos | Handoff DOCUMENTS (canon originals, uiux briefs, seam runbook). Not code. |
| `docs/mandates/akki_os_pack_v1/AkkiOS_*_Orchestration_Brief_v1.0.md` | RMS-IQ-Core-2, Extraction-Akki | Orchestration BRIEFS (Governance / Integration / Production). Not code. |
| `memory/ORCHESTRATOR_CONTINUITY.md` | All three core repos | An orchestration continuity memo (build-runbook), not the Canon-9 charter. |
| `backend/services/solva_voice_audit/orchestration/*` | Akki-Executive-Core | Solva-narration state-machine orchestration. Unrelated to Canon 9. |
| `frontend/src/components/shell/HandoffActions.jsx` | Akki-Executive-Core | UI actions for handoff. Not the charter. |
| Content grep `RECORD_MATRIX` / `WRITER_MAP` / `task_identity` / `writer_authority` | ZERO matches across all four repos |

**Neither the record matrix, nor the task-identity register, nor the handoff-contract registry exists in any of the four repos.**

## Adjacencies that are STRUCTURAL FOUNDATION (not distraction)

| Adjacent surface | Location | Judgement |
|---|---|---|
| `backend/contracts/*` frozen contracts + snapshot parity (32+ contracts) | All three core repos | **Foundation.** The parity-seat pattern (`test_frozen_contract_snapshot_parity.py`) is directly transferable to Canon-9 record-class registry entries. Every record-class writer→readers matrix row could be enforced by a snapshot-parity seat. |
| `services/registry_context/{reader,injector,prompt_builder}.py` (Akki-OS-V1 unique — Chunk 2 harvest) | Akki-OS-V1 | **Foundation.** A readable-registry pattern that could hold the Canon-9 task-identity register or the record matrix. |
| `services/partitions/session_working_set.py` (Akki-OS-V1 unique) | Akki-OS-V1 | **Foundation, narrow.** Session-scoped partitioning primitive. |
| `services/service_1/*` batching + ledger discipline | All three core repos | **Foundation.** Task-classification-by-batch already exists; extending to per-task authority identity is a matter of adding the authority column. |
| `services/northena/ledger.py` writer-side authority binding | All three core repos | **Foundation.** Northena is already the sole writer to the run ledger; the "writer = Northena" cell of the Canon-9 record matrix is DE FACTO enforced by dependency structure. |
| `services/auth/engineer_scope.py` + `session_binding.py` + `dependencies.py` | RMS-IQ-Core-2 / Akki-OS-V1 / Extraction-Akki | **Foundation for task-identity register.** Scoped-key + session identity primitives exist; a task-class → authority mapping table on top is BUILD. |

## Rows classified in this domain

Every Canon-9 row lands here.

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C9-001** | Mkondo maintains three registers + enforces them | **BUILD** | absent |
| **C9-002** | Structure-only; holds no opinion about content | **BUILD-design-rule** | " |
| **C9-003** | Answers to matrix questions answered HERE, never from memory | **BUILD-doctrine** | " |
| **C9-004 · C9-005** | One-record law + one writer per class | REUSE-doctrine (northena ledger is the writer) | 5.2 anchor |
| **C9-006–C9-018** | Record matrix (each writer→readers row) | **BUILD** | 13 rows, all absent as a NAMED matrix; individual writer/reader bindings exist implicitly per current code structure |
| **C9-019–C9-022** | Reading discipline (Watch reads governance for estate protection only; governance reads Watch for assurance only; neither surface renders the other's interior) | **BUILD** | ties to 5.8 |
| **C9-023–C9-035** | Task-identity register (each task class → EXACTLY one authority's identity; enforcement STRUCTURAL) | **BUILD** | 13 rows, all absent |
| **C9-036–C9-042** | Handoff contracts — admission→extraction, chokepoint→model, verdict→response, containment→decision, mirage release→reconciliation, disagreement→resolution, Watch findings→CIF | **PARTIAL for one (§18 admit→extract via wizard handoff); the other six are BUILD** | wizard/admission_handoff.py exists (C9-036 partial); the seven contracts as a registered artefact + registered-handoff invariant test are BUILD |
| **C9-043–C9-047** | Change & precedence — same ceremony, slowest countdown class for matrix changes, precedence where docs disagree, silence-is-finding | **BUILD** | ceremony machinery exists (checker) but no Canon-9-specific instance |
| **C9-048–C9-050** | One account per record class / one identity per task / one contract per crossing — held in one short document both authorities cite; seamlessness from reads, boundaries from writes; nobody ever answers matrix question from memory | **BUILD-doctrine** | Canon-9's own conclusion |

## Domain 5.9 subtotals

- REUSE: 0 (except C9-004/C9-005 doctrinally via northena ledger)
- REUSE-doctrine: 2
- PARTIAL: 1 (C9-036 admission→extraction handoff exists)
- BUILD: 45 rows
- BUILD-doctrine (design constraint): 2

**Nearly all of Canon 9 is BUILD.** Foundation primitives exist (registry_context, frozen-contract-snapshot parity, ledger append-only, engineer_scope) that would make the build cheap — the wiring together is the work.
