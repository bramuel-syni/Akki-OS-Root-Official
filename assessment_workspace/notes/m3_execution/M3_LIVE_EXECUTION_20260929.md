# M3 live execution — request → bounded extraction → verified result (DIGICOW pilot), 2026-09-29

Governing source: `Akki_Goal_Roadmap_v1.md` §M3; readiness `M3_DELIVERY_READINESS_REVIEW_20260929.md`;
ceremonies `ceremony_{AKKI-TEST,DIGICOW,RMS}_20260929T15*.json`. Owner rulings applied: approving
authority read from estate admission (interim-pilot stand-in for the unseated DigiCow groups, every
approval cites it); custody = the shared GPU-environment space (`/mnt/akki-storage-3388s`, no HTTPS
origin ruled); zero-rate pilot line `TERMS-PILOT-M3-DIGICOW-v0`; Path A applied to the PII-clean
censused unit (`digicow_rds`, census `cr-d2237ea30cb9`); worker keys generated on-host, approver /
rights-authority keys in estate custody. **RMS data is never extracted (owner instruction this run).**
E1 was a control plane throughout: every estate byte moved akki-vm → shared store; E1 saw metadata,
hashes and signed receipts only.

## What was wrong at the start of this run

`req-dfa250…` (previous session) failed on the worker with `ModuleNotFoundError` — the deep bundle lacked
`gpu_discovery_constants.py`; already patched in `worker_bundle.py` before hand-off. The drill script had
no syntax fault; the reported `JSONDecodeError` was a parse of that worker's truncated response.

## Defects found and fixed this run (all surfaced by the live path, each with an offline test or drill)

1. **Rights did not follow lineage.** The worker banked a signed `lineage` receipt for the sealed artefact,
   but no `rights` proof existed for the artefact itself, so `RightsGate.check` at the publish gate held
   every completed run at `NATIVE_RIGHTS_PROOF_REQUIRED` (canon test
   `test_transitive_native_lineage_and_current_release_hash` shows the intended shape). NEW
   `services/extraction_runtime/derived_rights.py`: after the independent runtime verifies the artefact,
   the estate **rights authority** (custody key admitted at the ceremony, permission
   `activation:observation:rights`) signs one `rights` observation for the artefact
   (`policy_ref` = the lawful-basis anchor, reason `RIGHTS_FOLLOW_ADMITTED_LINEAGE`), only if the recorded
   parents' rights are current (a withdrawn parent → `DESCENDANT_RIGHTS_WITHDRAWN`, no extension);
   idempotent per artefact identity. Called from `IndependentInspector.inspect` before the registry is
   written, so the publish gate and every later retrieve gate see a complete chain
   source → artefact.
2. **Re-verification drift.** The inspector stamped `freshness_stamp.logged_date = now()` on every call,
   so the canon's own `revalidate` at terminal-ready compared a "changed" registration
   (`ARTIFACT_REGISTRATION_CHANGED`). The stamp is now the recorded independence receipt's `issued_epoch`.
   Proven: 11 consecutive retrievals + a backend restart restate the identical registration.
3. **Proof-required holds closed the request.** `execution_records._state` mapped any post-dispatch hold to
   `Blocked` (closed, no retry) — including holds whose own `next_action` says "resolve the receipts". Holds
   ending `_REQUIRED` are now `Interrupted` (retry/stop permitted), like `_UNBOUND/_UNAVAILABLE`.
4. **Custody hold was masked.** `custody_delivery/service.py` turned the custodian's classified `Held`
   (`CUSTODY_ORIGIN_UNAVAILABLE`, from the shared-filesystem store having no HTTPS origin) into the generic
   `CUSTODY_PROVIDER_RESPONSE_INVALID`. The custodian's verdict now propagates, with honest public
   disclosures for `CUSTODY_ORIGIN_UNAVAILABLE` and the custodian mismatch codes.
5. `run_view` budget row for `active_compute` now shows consumed cpu-seconds (unit key `dimension:unit`).
6. Drill script break condition includes phase `ready`.

Offline: `tests/m3_commission/test_m3_offline_drill.py` 10/10 (new
`test_verified_artifact_receives_rights_along_worker_signed_lineage_and_withdrawn_parent_holds`).
Regression over m3_commission + portal_operational + non_gpu_flows + execution_spine +
execution_components + activation_controls: see `test_reports/pytest/m3_regression_20260929.log`
(`test_dispatch_blocks_on_connector_refusal` fails identically at git HEAD — pre-existing, unrelated).

## Live drill record (deployed backend, DIGICOW operator `demo.operator@demo.digicow.example.com`)

| Pack | Request | Evidence |
|---|---|---|
| **M3-T1 first bounded extraction, confirmed result** | `req-97999a0b46d2f51564b85dcd05d871a2` (draft `drf-aac5d6796e0df7488ba80e45`, table `digicow_live.training_questions`, max 200) | feasibility `warm / REGISTRY_MEMBERSHIP_MEASURED`; quote total `0` on `pilot.zero_rate.structured_records`; approvals: requester + 2× interim stand-in; dispatch `runtime:akki-vm` (cpu class); envelope acknowledged before effect; **worker complete in one advance**: 200 scanned / 200 qualified / 0 unqualified / 2 PII-floor redactions, 26,604 bytes read, 1.72 s wall, 0.38 cpu-s; sealed `units.jsonl` 341,643 B sha256 `64a6938a…` at `/mnt/akki-storage-3388s/akki/deliveries/req-9799…/…/units.jsonl`; independent inspection `inspection:2c2aeca9…` on **akki-vm-ii** (five rings, sha, size, etag all matched); registry record owner `org-2bb77fd82f6624d9` mandate `TERMS-PILOT-M3-DIGICOW-v0`; rights `62f5b6e4…` signed by rights authority `agent-99247932e93ec3da`; reservation settled `USAGE_RECONCILED`; metered + `usage_handoff non_model_consumption_only`; **terminal `ready · VERIFIED_RESULT_RECORDED`, evidence_mode measured**. My Work `Ready`, `permitted_actions=[result]`, `execution_verified=true`. |
| **M3-T3 interruption** | `req-393db89ef35ac94ccae17770f52b1c1f` (`shortcode_response`, max 20,000) | sizing basis now **measured** ("2 settled run(s)", 0.001875 s/unit); `advance` → `running`; requester **stop** at ~27 s → worker `cancelled · STOPPED_BY_REQUESTER` at 2,500 scanned (2,494 floor redactions), actual usage metered (12.23 s, 303,815 B, 1 cpu-s); terminal `cancelled · EXECUTOR_CANCELLED`; **no artefact published**; `stop` on a `Ready` request → 409. |
| **M3-T5 read-only means read-only** | `drill_T5_write_refusal_20260929T154432Z.json` | DELETE / UPDATE / DROP / INSERT sent to admitted runtime **akki-vm** → `refused · WRITE_VERB_REFUSED` before any connection; each refusal signed by `runtime:akki-vm` and banked (`3e1ae8e0…`, `5158e312…`, `38dd42c1…`, `93df3b69…`). |
| **M3-T5 identity after restart** | `req-9799…` | `work_id == request_id` across My Work list, `/commission`, `/run` (`work_order_ref c3451bef…` identical); after `supervisorctl restart backend`: `Ready / VERIFIED_RESULT_RECORDED`, registry stamp unchanged, `advance` restates `ready`. |
| **M3-T4 widened intent / negative paths** | `drill_T4_negative_paths_20260929T154709Z.log` | widened bounds → **version 2**, v1 immutable; revising a commissioned draft → 409; un-censused table → `unknown / TABLE_NOT_CENSUSED`, freeze refused 409; `users` table → floor `de_identified` on 6 personal columns; withdrawn draft cannot be frozen; duplicate freeze → 409; other-tenant analyst → 404 on the run, 403 on drafts; anonymous → 401. |
| **M3-T2 denied approval / seated approver** | offline only | `test_freeze_with_seated_groups_waits_for_the_seated_approver_and_refusal_keeps_the_job`; live DIGICOW has no seated authority (owner workbook lacks identity drops) — stand-in by ruling. |
| **M3.3 delivery** | `req-9799…` `POST /delivery` | custodian akki-vm-ii verified the sealed object size, then **held `CUSTODY_ORIGIN_UNAVAILABLE`**: the artefact rests in the tenant's shared store; no retrieval origin is ruled, so Akki issues no link and `delivery_verified=false`. This is the ruled pilot state, not a defect. RMS custody (Huawei OBS origin) is bound but RMS is out of extraction scope. |

## Standing limits (stated, not hidden)

- `req-c1f2738b3449081569aebfbfd537e2a6` (first completed run, pre-fix): its registry was written before rights
  existed and carries a call-time stamp; rights were later extended by operator tool `m3_extend_rights.py`
  (`4c086656…`) but the immutable registration cannot be restated, so it stays `Interrupted` with its real
  work metered. Not deleted, not rewritten.
- Custody grants for DIGICOW need an owner ruling on an HTTPS retrieval origin (or delivery is by mount).
  `CustodyBinding` binds one tenant's origin (RMS) — multi-tenant custody binding is an M7 item.
- Quality matrix rule `matrix.structured_records.v0:pending_first_verified_sample`: threshold is to be set from
  a human-verified sample of this first table (C4 §45); tripwires ran, no threshold invented.
- Sizing rate is now measured from 2 settled runs; GPU classes still declared-prior (no GPU job yet).
- Approving authorities for DigiCow (Vincent Kimani, Peninah Wanja) remain unseated — stand-in cited on
  every approval; seat them by the ceremony when identity drops arrive.
- No UI surface yet for commissioning (P1: wire DAP Request / My Work to `/api/portal/commission/*`).
- The M2 Watch inventory must be rerun as M3 added the `dap.commission` and `dap.delivery` gates (G2).

## Tools

`m3_live_drill.py` (draft/freeze/advance/run/stop/view), `m3_ledger_walk.py`, `m3_extend_rights.py`,
`m3_write_refusal_drill.py`, `m3_estate_ceremony.py`, `m3_seed_tenant_operator.py`.
