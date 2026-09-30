# M6-T4 · skill really callable — boundary proven to a receipted hold; grounded result HELD by ruling · 2026-09-30

Owner rulings (2026-09-30, this wave): **1a** target = the DIGICOW sealed artefact; **2b** caller = the existing DIGICOW
operator plus one key grant; **3b** hold the answering executor until a QA model is admitted; **4b** no re-admission
ceremony on the live hosts yet; **5a** thumbnails first, then M6-T4 in phases, terminal pytest only (no testing agent).

## What is now bound (tools/m6_skill_binding.py · receipt `skill_binding_DIGICOW_20260930T184037Z.json`)

| Record | Value |
|---|---|
| Corpus slice (write-once) | `akki://artifact/DIGICOW/req-97999a0b46d2f51564b85dcd05d871a2/qualified-units` · sha256 `64a6938a…` · 341,643 B · class `utterance` · terminal `ready · VERIFIED_RESULT_RECORDED` (M3-T1, 2026-09-29) |
| Key grant | `6090156f3b936c22e8267fff` → `demo.operator@demo.digicow.example.com` · class `external` · path `governed_extract` · floor `utterance` · scope `digicow_rds` · grantor `owner-ruling:M6-T4:2026-09-30:2b` · lawful basis = the DIGICOW rights anchor `activation_receipt:2d1bde6e…` · ledger row emitted by the existing grant service (`engineer_key_grants`, single source; the JWT derives it at login) |
| Skill | `1a03977aeac14421a980890f6622c91f` · floor `utterance` · scope `digicow_rds` · `POST /api/callable_skill/1a03977aeac14421a980890f6622c91f/query` · `callable_skills` insert-only (TF-E4 (b) α) |

No account, password, role, runtime descriptor, signer, ceremony record or Ledger authority was created or changed. Both
steps are idempotent (re-running the tool returns the same grant and skill).

## The call through the ordinary boundary (LIVE preview, `tests/m6_callable_skill/test_m6_t4_boundary_live.py` · 11 passed)

`POST /api/callable_skill/{skill_id}/query` · bearer = DIGICOW operator · `Idempotency-Key: k-m6t4-001` · `{"query": "Which training questions mention milk yield?"}`

```
HTTP 409  {"query_id": "skill-query-e0780842f560d00446c52cd27cbae27302648b922f4e574a2f03c237d4ac9c39",
           "skill_id": "1a03977aeac14421a980890f6622c91f",
           "query_sha256": "c7117264a6bbef85369c7951bd349f271b48f83d1de79605eaf36cb6d5ef3689",
           "intent_receipt_ref": "054adddeb52d93c6700e53fa60f501601f10a31c6cf1ac24e2fcefd7e462784a",
           "outcome": "held", "reason_code": "SKILL_NATIVE_PLAN_REQUIRED",
           "execution_verified": false, "delivery_verified": false,
           "history": [{"receipt_ref": "054addde…", "event": "skill.query.intent", "reason_code": "SKILL_QUERY_INTENT_RECORDED"},
                       {"receipt_ref": "d7bfa674…", "event": "skill.query.view",   "reason_code": "SKILL_NATIVE_PLAN_REQUIRED"}]}
```

Gate order exercised for real: identity (JWT) → provisioning record → `check_scope(external, governed_extract, utterance, digicow_rds)`
→ tenant-bound portal scope → idempotent intent recorded on the tenant Ledger (`054addde…`) → native runtime plan lookup →
**first-class hold, receipted (`d7bfa674…`)**. The raw question is never persisted or forwarded (sha256 only). No answer,
no artefact ref, no class label is fabricated.

Also proven on this path (all live):

- **Duplicate retry, same key → same `query_id`, same `intent_receipt_ref`, identical history** — no duplicate effect (the
  M6-T5 duplicate rule on the skill path).
- Same key, different question → 409 conflict (frozen command); missing `Idempotency-Key` → 422 `SKILL_QUERY_IDEMPOTENCY_REQUIRED`
  before any effect; blank query → 422 by contract.
- `POST …/query-intents` → 201 held; `GET …/queries/{id}` restates the same held query without executing anything.
- Anonymous → 401; authenticated RMS operator without the grant → 403 `auth_scope_insufficient`; unknown skill → 404
  `skill_not_found`; responses carry `Cache-Control: no-store`.

## Why the outcome is a hold, and exactly what a grounded result still needs

`query_plans.resolve` finds no `plan` receipt whose request is `skill_request(provisioning, …)`; the native runtime binds
executors `{'source'}` only (`extraction_runtime/factory.py`), both DIGICOW runtimes are admitted for `kinds=['source']`,
the worker signer holds no `activation:observation:skill_response`, no signer holds `activation:observation:anchor` for
answers, and no `quality_register` / `context_window` / eligibility / Mkondo-handoff producers exist for `skill`. Under
rulings 3b/4b these are intentionally **not built** in this wave. To unhold M6-T4 (in order):

1. Owner admits a QA-capable executor (ruling 3) and re-runs the DIGICOW ceremony with `kinds=[source, skill]` and the
   extra signer permissions (ruling 4).
2. Control plane: skill commission (Plan `kind=skill`/`solva`, purposes `answering`, groups scope/expenditure/answering with
   the interim stand-in), `BoundedEngineAdapter(kind='skill', engine='solva')`, eligibility + handoff providers.
3. Runtime: worker skill mode over the sealed `units.jsonl` → answer artefact + `skill_response` grounding; inspector on the
   other host signs `anchor` observations against the plan's snapshot hashes; quality/context receipts.
4. Re-run the same live suite: the identical call must then return `200 · ready · GROUNDED_SKILL_RESULT_VERIFIED` with
   `defensibility.class` inline — same caller, same key grant, same skill_id, no code change at the boundary.

## Finding recorded (not changed)

`POST /api/transform/callable_skill/provision` carries no identity gate (any caller can insert a provisioning record).
Provisioning alone grants nothing — every query is gated on the caller's own key grant — but the route should require an
operator/engineer identity before skills are provisioned by anyone other than an owner tool. Left as-is pending a ruling.
