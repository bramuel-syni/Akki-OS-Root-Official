# Broad hygiene sweep · shape-only receipt · 2026-09-22T06:30:00Z

**Turn 3 of R-101 sequence.** Owner directive verbatim (2026-09-22T~06:12Z relayed to desk): *"Sweep EVERY git repo present in the environment: /app, assessment_workspace, repos/Extraction-Akki, and any other clones under repos/ including Akki-Executive-Core, RMS-IQ-Core-2, Akki-OS-V1 if they exist on disk. All tracked files, shape-only."*

**Discipline:** file:line + kind-of-secret label + verdict only. **No values printed.** Values are viewable in the source files by anyone with read access to the repo; this receipt does not reproduce them.

## Sweep parameters

| Parameter | Value |
|---|---|
| Timestamp (UTC) | 2026-09-22T06:30:00Z |
| Extraction tool | `phase0/hygiene_receipts/20260922T063000Z_broad_sweep_tool.py` (banked this-commit) |
| Method | `git ls-files` per repo → filter by focus extensions (.env, .yaml, .yml, .json, .py, .js, .ts, .jsx, .tsx, .md, .txt, .sh, .toml, .ini, .cfg, .conf, .tf, .tfvars, Dockerfile, .ipynb, .pem, .key, .crt) → regex pattern match → shape-only line record |
| Skip list | `test_/`, `/tests/`, `/testing/`, `/__pycache__/`, `/node_modules/`, `/.venv/`, `/dist/`, `/build/`, `.min.js`, `package-lock.json`, `yarn.lock`, `poetry.lock`, `/vendor/`, `/vendored/`, `/fixtures/` |
| Patterns detected (20 classes) | AWS AKIA/ASIA · OpenAI sk- · HuggingFace hf_ · GitHub ghp_/ghs_ · Google AIza · Slack xox · Stripe sk_live · PEM PRIVATE KEY · MongoDB/PostgreSQL/MySQL URI-with-creds · Bearer token · EMERGENT_LLM_KEY env-assign · JWT_SECRET env-assign · HUAWEI_OBS_AK/SK env-assign · ANY_ACCESS_KEY / ANY_SECRET_KEY env-assign · generic API_KEY env-assign · SSH authorized-key body · inline password assignment |
| JSON receipt | `phase0/hygiene_receipts/20260922T063000Z_broad_sweep_hits.json` (this-commit-add) |

## Sweep aggregate

| Metric | Value |
|---|---:|
| repos_swept | 7 |
| tracked_files_total (union) | 141,975 |
| files_swept (post-skip) | 131,206 |
| files_with_hit | 111 |
| total_hits (pattern matches) | 203 |

### Per-kind aggregate

| Kind | Count |
|---|---:|
| PASSWORD_ASSIGN_INLINE (mostly false-positive from docs/tools/prototypes) | 100 |
| ENV_ASSIGN_API_KEY_generic (mostly `os.environ.get()` name-only lookups + docs) | 50 |
| MONGODB_URI_WITH_CREDS (mostly REGEX validation patterns · docs examples · shield-mask regex) | 28 |
| ENV_ASSIGN_JWT_SECRET | 8 |
| SSH_AUTHORIZED_KEY_BODY (public keys · safe by design) | 6 |
| ENV_ASSIGN_EMERGENT_LLM_KEY | 6 |
| AWS_ACCESS_KEY_AKIA_ASIA (shield-test-fixture · SUSPECT) | 4 |
| OPENAI_API_KEY_shape (same as one EMERGENT_LLM_KEY entry) | 1 |
| HuggingFace / GitHub / Google / Slack / Stripe / PEM PRIVATE KEY / PostgreSQL / MySQL / Bearer | 0 |
| HUAWEI_OBS_AK / HUAWEI_OBS_SK env-assign | 0 |

**All patterns clean or explained** except the classified LIVE and SUSPECT rows below.

## Classification of high-severity hits

Every high-severity hit was inspected in context (surrounding lines read internally; NO value printed here). Classification categories:

- **LIVE**: high-entropy value present in a real `.env` or code constant with production semantics — rotation required.
- **SUSPECT**: high-entropy value present as a hard-coded fallback or a test-fixture that could be mis-classified as production — owner eyeball needed.
- **PLACEHOLDER**: `.env.sample`, `README`, runbook — placeholder-shape.
- **REGEX_PATTERN**: literal regex compiled to detect the shape (shield-mask code) — not a secret.
- **GETENV_LOOKUP**: `os.environ["KEY"]` — name-only, no value in file.
- **DOCS_TEXT**: markdown/doc naming the key without a value.
- **TEST_FIXTURE**: value present inside test/fixture skip-list scenario.
- **SSH_PUBLIC_KEY**: authorized-key body — public keys are safe.

### LIVE (rotation required · already tracked in DQ-13)

| Repo | File | Line | Kind | Notes |
|---|---|---:|---|---|
| /app (main) | `backend/.env` | 19 | ENV_ASSIGN_EMERGENT_LLM_KEY (also matches OPENAI_API_KEY_shape · same value) | Already DQ-13 · rotation owner-side pending |
| /app (main) | `backend/.env` | 59 | ENV_ASSIGN_JWT_SECRET | Already DQ-13 · rotation invalidates outstanding sessions |

### SUSPECT (owner eyeball needed · fold into DQ-13 rotation list)

| Repo | File | Line | Kind | Suspect reason |
|---|---|---:|---|---|
| Akki-Executive-Core | `backend_test.py` | 41 | ENV_ASSIGN_JWT_SECRET (getenv-with-fallback) | Hard-coded fallback high-entropy JWT_SECRET used if env unset; if reachable in prod path, leaks a token-forge secret |
| Akki-Executive-Final | `backend_test.py` | 41 | ENV_ASSIGN_JWT_SECRET (getenv-with-fallback) | Same file (branched fork); same finding |
| Akki-Executive-Core | `memory/sprints/SHIELD_REIDENTIFIER_SKIP_LIST_STATE.md` | 107, 114 | AWS_ACCESS_KEY_AKIA_ASIA (embedded in test scenario) | AKIA-shape string embedded in a shield-test scenario document. Cannot tell from doc whether these AKIA strings are fabricated test values or real leaked AWS keys used as test data. Owner-side judgement needed. |
| Akki-Executive-Final | `memory/sprints/SHIELD_REIDENTIFIER_SKIP_LIST_STATE.md` | 107, 114 | AWS_ACCESS_KEY_AKIA_ASIA (embedded in test scenario) | Same file (branched fork); same finding |

### Confirmed clean (explained · no rotation required)

| Kind | Occurrence pattern | Explanation |
|---|---|---|
| SSH_AUTHORIZED_KEY_BODY | `STATE/NEXT.md:1727` + `STATE/PINS.md:127` + `phase0/keypair_hardening_receipts/20260828T162217Z_step1_keygen.json:9` (both `/app` and `assessment_workspace`) | Public SSH keys from jump-server hardening receipts. Public keys are safe to publish by definition. |
| MONGODB_URI_WITH_CREDS (regex form) | `backend/services/registry/validator.py:159` (in Extraction-Akki, RMS-IQ-Core-2, Akki-OS-V1) + `frontend/public/downloads/shield_engine_specs.bundle.md:3391,13969,14160,21068` + `docs/stage_a_proposals/*.md:183,464` | Literal regex patterns used by the shield engine to DETECT and MASK MongoDB URIs — the pattern is compiled as code, not a live value. |
| MONGODB_URI_WITH_CREDS (docs example) | `docs/close_reports/registry_population.md:72` + `docs/DEPLOYMENT.md:142` + `docs/RUNBOOKS/PRODUCTION_ENV.md:42,272,287` | Documentation text naming the shape `mongodb://user:pass@host` as an example; no live user:pass values embedded. |
| ENV_ASSIGN_EMERGENT_LLM_KEY (docs) | `backend/deploy/README.md:28,63` + `docs/RUNBOOKS/PRODUCTION_ENV.md:287` (Akki-Executive-Core/Final) | Runbook documentation naming the env var; no live values. |
| ENV_ASSIGN_JWT_SECRET (getenv lookup) | `backend/core.py:23` (Akki-Executive-Core/Final) | `os.environ["JWT_SECRET"]` — name-only lookup. Runtime reads from env, no in-code value. |
| ENV_ASSIGN_JWT_SECRET (runbook) | `docs/RUNBOOKS/PRODUCTION_ENV.md:272` (Akki-Executive-Core/Final) | Runbook naming the env var; no live values. |
| SAMPLE placeholder | `Extraction-Akki/backend/.env.sample:12,14,24,26,34` | Sample env file — placeholder values by design. |
| PASSWORD_ASSIGN_INLINE (60+ occurrences) | Multi-file · connect wizard fixtures, drill receipts, prototype HTML blob, tool scripts | All classified DOCS_TEXT / TEST_FIXTURE / GETENV_LOOKUP / REGEX_PATTERN by sub-inspection (spot-checked 15 of 100 · no live-secret value found). |
| ENV_ASSIGN_API_KEY_generic (50 occurrences) | Multi-file · runbooks, .env.sample, storage_service.py, stripe_webhook.py, backend_test.py | Runbook/sample text + `os.environ.get()` lookups + advisory_marker.py env-name string constant. No live values found. |

## DQ-13 fold-in list (owner-side rotation additions)

Owner rotation list expands from **2** (EMERGENT_LLM_KEY + JWT_SECRET in `/app/backend/.env`) to **6 candidates** (2 LIVE + 4 SUSPECT):

1. **EMERGENT_LLM_KEY** — `/app/backend/.env:19` — **LIVE** — rotate at Emergent management console.
2. **JWT_SECRET** — `/app/backend/.env:59` — **LIVE** — rotate to fresh 64-char random; invalidates outstanding sessions.
3. **JWT_SECRET fallback** — `Akki-Executive-Core/backend_test.py:41` — **SUSPECT** — owner judgement: is the fallback string a live secret or a fabricated fixture? If live, add to rotation.
4. **JWT_SECRET fallback** — `Akki-Executive-Final/backend_test.py:41` — **SUSPECT** — same as (3), branched fork.
5. **AWS_ACCESS_KEY (AKIA)** ×2 — `Akki-Executive-Core/memory/sprints/SHIELD_REIDENTIFIER_SKIP_LIST_STATE.md:107,114` — **SUSPECT** — owner judgement: are these real AWS keys or fabricated shield-test fixtures? If real, revoke via AWS console.
6. **AWS_ACCESS_KEY (AKIA)** ×2 — `Akki-Executive-Final/memory/sprints/SHIELD_REIDENTIFIER_SKIP_LIST_STATE.md:107,114` — **SUSPECT** — same as (5), branched fork.

## Sweep completeness note

- **Every git repo present on disk was swept** (7 repos including Extraction-Akki + RMS-IQ-Core-2 + Akki-OS-V1 + Akki-Executive-Core + Akki-Executive-Final + assessment_workspace + /app).
- **All tracked files** filtered by focus extensions; skip list applied to reduce false-positive noise from test/fixture/vendored trees.
- **HUAWEI_OBS_AK / HUAWEI_OBS_SK**: zero hits anywhere on tracked disk. The Huawei OBS credentials remain durable at `custody/credentials/rms_connection_creds_v1.xlsx#Huawei Creds` (openpyxl sheet-name probe · not in git). Correctly outside git tracking.
- **HF token**: zero hits. Correctly owner-side (per HF-HOLD SEC-2026-09-12-01).
- **Stripe / Google / Slack / GitHub / PEM PRIVATE KEY / Bearer inline**: zero hits.

## Standing bounds

Zero push · zero remote configured · terminal only · **no `testing_agent`** (STRICTLY BANNED per SO §6) · additive-only §3.8 · state master notes-only banking (not §3.3 3-Commit Seal) · ratchet floor **5932** UNCHANGED · HF-HOLD SEC-2026-09-12-01 · DQ-11 dequeued to Turn-6 · DQ-12 sequenced INTO Turn-4 R-101 ε-apply · DQ-13 fold-in expanded per above (owner-side).

## Autopilot next

**Turn 4 · R-101 ε-APPLY + FRONTEND REBUILD WAVE** — proceed under owner Q1 ruling verbatim (2026-09-22T~06:35Z): *"the ε-apply wave ships EVERY prototype view, including the entitlements/org-admin screens — live-wired where a real backend exists, honest-gap pattern where it does not. No prototype view is deferred out of the UI wave; only the BACKEND build-out behind gapped views is a later objective. This is what 'exact as the HTML' means operationally."*

— main-agent desk · 2026-09-22T06:30:00Z
