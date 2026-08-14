# Domain 5.2 — Direction and Record

Scope (instruction §5.2): Admit's validity sequence · freeze · Gate's
set-membership · Converge · ledger row contract · append-only enforcement ·
stamp-audit absorption channel.

Spine cited: **Extraction-Akki** (≡ RMS-IQ-Core-2 byte-identical on all files below).

## Rows classified in this domain

| Row | Capability | Class | Evidence | Note |
|---|---|---|---|---|
| **C1-020** | One record — exactly one, append-only single ledger | **REUSE** | `backend/services/northena/ledger.py:63-65` `insert_one` only; `NORTHENA_LEDGER_COLLECTION` single collection; test `backend/tests/invariants/test_northena_ledger_retention.py:37-62` grep-forbids delete/purge/expire | Chunk-2 Claim 4 CONFIRMED |
| **C1-021** | No service keeps a local log constituting a second account | **REUSE** | wider invariant `backend/tests/invariants/test_no_unauthorized_deletion_path.py` (154 L) whitelists only `services/retention/authorized_deletion.py`; `insert_one`-only pattern verified in `northena/ledger.py`; test cleanup delete_many calls in `test_instance_fixture_b_walkthrough.py:54,109` are non-production | one whitelist entry (retention) is the only authorized deletion path |
| **C1-025** | Single owner per value — computed once, carried forward as fact | **REUSE** | Mtafiti owns measurement (never Solva), Targeta owns plans (never Mtafiti), Solva owns reasoning traces (never Northena) — enforced via engine-wall tests `backend/tests/invariants/test_reasoning_faculty_isolation.py`, `test_targeta_invariants.py::test_yield_candidate_never_carries_floor_or_raw_measure` | wall discipline present |
| **C1-062 · C1-063 · C1-064 · C1-065 · C1-066 · C1-067** | Operating loop (questions → answered/gaps → commissioned → extraction changes what round can answer) | **PARTIAL** | Northena admit + wizard admission_handoff + Targeta plans are in place (see rows below). The **loop as an end-to-end orchestration** — with gap ranking by carried demand evidence, no priority list by hand — is **BUILD** (need `services/targeta/gap_candidate_filer.py` from Akki-OS-V1 harvested to close). | Chunk-2 harvest item |
| **C3-004** | Northena is deterministic — no model, no learned weights | **REUSE** | `backend/services/northena/admit.py:1-168` uses only `_REQUIRED_KEYS` list + dataclass validation; no `litellm`/`shield_invoke` in `services/northena/*.py`; `backend/tests/invariants/test_northena_invariants.py` covers | verified |
| **C3-005** | Northena computes one thing: verdict on every operation | **REUSE** | `admit.py:107 compile_and_freeze` returns admit/refuse LedgerRow; `gate.py`; `converge.py`; `state_machine.py` orchestrate | 3-verdict alphabet at `admit.py:139-146` (admit path) + `156-165` (refuse path) |
| **C3-006** | Universality — every operation flows through Northena; no bypass | **REUSE** | there is one entry surface `wizard/admission_handoff.py` for user work + `services/service_1/*` for scheduled work — both call `northena.admit`; enforced by dependency direction | check completeness in Chunk 4 |
| **C3-007** | Objective freeze on admit; immutable for the run; amendment = new admission | **REUSE** | `admit.py:88-104` `FrozenArtifact.__setitem__/__delitem__` raise `TypeError("FrozenArtifact is immutable (§4/N-INV-4)")`; `admit.py:133-138` uses `MappingProxyType`-style wrapper | unrepresentable-not-policed at code level |
| **C3-008** | Every actor (human user, agent, service) declared before operations | **MODIFY (spec-seam) / BUILD** | `northena/admit.py:_validate_completeness` `_REQUIRED_KEYS = ("artifact_type","artifact_id","artifact_version","lawful_basis","scope")` — five fields, but **NOT declaration**. The word "declaration" in the codebase means the Mtafiti per-source declaration baseline (Canon 4 §7, `services/mtafiti/declaration.py`) — a different concept. Executive-Core has `frontend/src/pages/home/HomeUndeclared.jsx` (a UI stub) but no server-side capture. | **Carry-forward (a) RESOLVED**: Canon 3 §6.1 actor declaration capture is unimplemented across all four repos. The admit five-field check is Canon 3 §7 (admit content), not Canon 3 §6.1 (declaration). Chunk 4 must decide whether to (i) BUILD an actor-declaration seat, or (ii) MODIFY admit._validate_completeness to require a sixth field. |
| **C3-009** | Re-declaration supersedes; no overwrite | **BUILD** | ledger pattern present (append-only); the declaration schema itself is missing (see C3-008) | derived from C3-008 |
| **C3-010** | Admit consults declaration as an input | **BUILD** | same as C3-008 | " |
| **C3-011** | Three-verdict alphabet: ADMIT · HOLD · REFUSE | **REUSE** | `contracts/northena_ledger.py::LedgerRow` (verdict = "admitted" / "held" / "refused") + `admit.py:139-166` writes both paths | " |
| **C3-012** | ADMIT carries frozen objective + permitted scope + standards + receipt id + timestamp — bound before execution | **REUSE** | `admit.py:133-146` binds `FrozenArtifact` + admit row before returning; `LedgerArtifactRef` carries `(kind,id,version)` per `contracts/northena_ledger.py::LedgerArtifactRef` | ordering enforced by returning after `await ledger_record(row)` |
| **C3-013** | HOLD has a named holding reason; canonical example rule-change-in-force | **PARTIAL** | HOLD row shape exists in `LedgerRow` schema; **rule-change countdown → held-run wiring** is at `services/checker/{effective_delay,rule_change_request,state_machine}.py` — enforced via `test_govern_g_g1_to_g_g8.py` and `test_phase3_sc3_govern_live.py`. HOLD payload lists the specific rule id + version | REUSE for infra; validate the pause-on-countdown behaviour in Chunk 4 |
| **C3-014** | REFUSE first-class output; carries reason + what would satisfy + receipt id | **REUSE** | `admit.py:156-166` refuse path writes `LedgerRow(stage="admit", decision="refused", reason=...)`; `_validate_completeness().refusal_reason()` at admit.py:56-59 produces the deterministic composite reason string | " |
| **C3-015** | Every admit/hold/refuse is a ledger row (contract-grade; no field omitted) | **REUSE** | `LedgerRow` at `backend/contracts/northena_ledger.py` — Pydantic model with `extra="forbid"`; test `test_northena_ledger_row_v0.py` covers the frozen contract | " |
| **C3-043** | Northena ledger writer authority (writer=Northena in the record matrix) | **REUSE** (writer-side) | `services/northena/ledger.py:63` is the sole writer to `NORTHENA_LEDGER_COLLECTION`. The Canon-9 authority binding is doctrinal (5.9); the code binding is here. | pairs with 5.9 |
| **C3-044** | Every admit/hold/refuse/retry/outcome produces a ledger row BEFORE response returns to caller | **REUSE** | ordering enforced in `admit.py:146,166` — `await ledger_record(row)` PRECEDES `return row`; also in `gate.py`, `converge.py` | verified |
| **C3-045** | Ledger rows immutable — correction is by new row citing id, never field mutation | **REUSE** | `LedgerRow` Pydantic model with `frozen=True` (per `contracts/northena_ledger.py::LedgerRow` config); no `update_one`/`update_many` referring to the northena ledger anywhere in `services/` | enforced |
| **C3-023 · C3-024 · C3-025** | Solva stated-at-class + no confident-with-caveat + reasoning trace (writer) | **REUSE** (writer-side; the assertion boundary belongs to 5.3) | `services/solva_depth/trace.py` writes traces to the ledger; test `backend/tests/invariants/test_solva_trace_ledger_integration.py` covers | trace ledger integration verified |

## Stamp-audit absorption channel

`backend/tests/invariants/test_ledger_absorbs_outer_gate_and_v2_via_stamp_audit.py` — the ledger absorbs outer-gate and v2 events via a stamp-audit row shape. This closes the Canon-1 §4.3 "no service keeps a second account" gap for the outer-gate and v2-gate services (they emit stamps that land on the northena ledger, not their own).

Row class: **REUSE**.

## Domain 5.2 subtotals

- REUSE: 18 rows
- MODIFY / spec-seam (C3-008 · C3-009 · C3-010): 3 rows (**declaration seam resolved as MODIFY-or-BUILD** — see note under C3-008)
- BUILD: 3 rows (loop end-to-end orchestration; declaration surface)
- N/A-DOCTRINE: 0

The Chunk-2 spec-seam is now bound: `C3-008 · C3-009 · C3-010` are the actor-declaration surface — unimplemented. Both a code citation (admit.py) and a canon citation (§6.1) present.
