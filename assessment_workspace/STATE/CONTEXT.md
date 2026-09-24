# CONTEXT.md — Running narrative

## DESIGN LAWS · Standing rules (add-only ledger)

- **REFERENCE-NOT-COPY** — Owner Ruling 2026-08-19 (DECISIONS.md · A8/T8-part). Any trace, preview, embed, walk, or adjacent-render resolves through the governed read path with entitlement checked at the point of access; never an embedded copy, never an in-place reveal. Applies estate-wide (traces, previews, embeds, walks — every future adjacent-render pattern). The operative principle is the SINGLE CHOKEPOINT: an in-place content reveal is a second read path that never re-checks entitlement at point of access. The correction supersedes any reasoning based on "envelope destroyed at crossing" — the envelope covers a single de-identification mapping, not the general reveal question. Reads across the wave plan onto W3 (Data Shield telemetry), W5 (refusal-card evidence links), W6 (Cost Ledger lever attribution), W7 (Model Admission acceptance evidence), W8 (rules-updates rule-tree), W9 (Walk-this ×∞) — recorded as a cross-wave gate.


## W10 · Completion Wave · CLOSED · 2026-08-26T09:30Z

**Composite (authoritative · Owner correction #4)**: **52.49 %** · mechanism 54.45 % (280.4 / 515) + interface 47.93 % (27.8 / 58) · blend 0.7×mech + 0.3×iface. Method + delta enumeration in `tools/w10_cp9_composite_recompute.py`; locked by `test_w10_cp9_composite_lock.py` (5/5 green).

**Wave-close cohort**: **261/261 green** across 43 test files (W7 CP1..CP7 + W8 CP1..CP6 + W9 CP1..CP5 + W10 CP1..CP9 + all frozen contracts + parity map + composed-conclusion count). Log at `phase0/drill_receipts/20260826T091500Z_w10_wave_close_green.log`.

**Extraction-Akki HEAD**: `programme/track-a` @ `d4ba30c` (CP8) → CP9 close commit pending. **Assessment-master HEAD**: `a809fe7` (CP8) → close commit pending.

**Delivered**:
- Canon 8 mechanism fabric fully wired: Ruling-1 firing drill (CP1) · Grey Mirror §15-§16 BUILD not LIFT (CP2) · Watch drills + §32.8 no-self-cert fitness (CP3) · Reserved-Decisions §19 + §32.6 no-machine-execution panel (CP4) · Witness fabric §9 + §33 with tamper alarms (CP5).
- Doc 14 §33 CA1-005 whitepaper drafter BUILD not LIFT · 150-LOC lid honored (CP6) · same-commit DoD respected (parity 58→59).
- Doc 14 §§21-45 register expansion · 4 rows → 28 rows · 24 new rows anchored to Canon 4 §§ verbatim (CP7).
- Governance + Watch + Grey-Mirror React frontends wired at /governance, /watch, /grey-mirror · substantive DOM asserts · 32/32 CP8 tests green · HTML snapshots banked for owner-side rendering (CP8).
- **/api/openapi.json** now serves at 200 (49 paths · docs_url/redoc_url disabled · response-boundary sanitizer intact) — cheap CP9 optional fix.

**R9 owner ruling (2026-08-26T09:20Z)**: preview allowlist strict-flip verified — owner IP 41.90.172.155 admits · unknown IP (203.0.113.99) refuses with sentence + 403 · no-XFF refuses. R8 permissive mode is RESCINDED at wave close per its own sunset clause. Fail-closed posture restored.

**Interleaved query answered informationally (2026-08-26T08:20Z)**: audio-trainer × GPU readiness — NOT BUILT (perception-side ASR/diarisation wired but no training pipeline · GPU connect real 7-stage but `.env` currently points at mock SSH · trainer deferred beyond W10 · ~W10-scale wave of its own if pursued). No CP scope change.

**Outstanding beyond W10 (all non-blocking to close)**:
- FL-P4-W8-01 · CA1-N2 + CA1-N3 (14 policy questions · breach + erasure).
- FL-P4-W9-01 · CA1-N5 (1 policy question · continuity attestation).
- Doc14-020 · Canon 4 §38 rights-unclear grammar · OPEN-SLOT (N-series pattern · new at W10 CP7).
- Audio trainer + real GPU credential wiring (informational only · not booked).

**Design laws unchanged**: REFERENCE-NOT-COPY still binding · every W10 surface renders with source_path citations · raw signing material sanitized out at every response boundary (Owner Order 2026-08-25 §4 · verified via `test_endpoints_never_return_raw_credentials_or_secrets`).


**Last updated:** 2026-08-19 · Owner Data-API delivery cycle CLOSED · first DATA connection LIVE for `digicow_live` + `ndume` on cluster `db-restore-603-cluster` (eu-west-1) via RDS Data API · engine detected `aurora-mysql` (MySQL 8.0.42 / Aurora MySQL 3.10.3) · 235 tables inventoried (125 + 110), top-25 by rows per DB banked with approximate row counts (`information_schema.tables`), 5 structural reads per DB (column names + types only — **zero record contents read**) · programme/track-a HEAD `746dece` (was `f87b769`) · assessment-repo HEAD pending this-cycle commit (was `e2b5efe`) · engine-detect production defect fixed tests-first (FL-P2-24 CLOSED · +7 gating assertions, 141 total backend cohort green, 0 regressions) · secret sweep hit_count=0 on /app, /tmp, /var/log/supervisor, /root, /etc, both git worktrees, both git histories, /root/.emergent/tool_outputs, /root/.emergent/automation_output.


## COMPACTION-RECOVERY + Owner Data-API delivery cycle · 2026-08-19

**Compaction / restart occurred mid-execution** of the aurora-inventory forced-engine retry (background bash pid=989 from the prior cycle). Cold-read from disk performed against STATE/ before touching anything.

**On disk at recovery start (verified):**
- `phase0/drill_receipts/20260819T152331Z_aurora_connect_and_inventory.log` — first pipeline pass over the production `services.connect.rds_data_submit` path against the owner's ARNs. SELECT 1 returned YES for BOTH databases (`digicow_live`, `ndume`); production engine detector returned `engine=unknown` from `version='8.0.42'` (defect: no engine-probe existed) → `table_count=0` recorded because inventory branch used engine-typed SQL. Initial records superseded by the retry.
- `phase0/drill_receipts/20260819T152509Z_aurora_inventory_mysql.log` — retry through a throwaway script that forced `engine=mysql` and issued `SELECT @@version, @@version_comment, @@aurora_version` (engine probe) before the inventory SQL. Captured: `version='8.0.42'`, `version_comment='6252a59a'`, `aurora_version='3.10.3'`. digicow_live: 125 tables (top-1 = `ussd_users` ≈ 2,285,264 rows / 747.7 MB). ndume: 110 tables (top-1 = `breedings` ≈ 184,348 rows / 155.8 MB). Full top-25 by rows per DB + 5 structural reads per DB (column names + types only, from `information_schema.columns`; **no record contents were read** — that waits on a data-handling agreement per owner note "read access to all records… **first pass STRUCTURE ONLY**").
- `phase0/data_connection_records/data_source_{digicow_live,ndume}_20260819T152513Z_FINAL.json` — final ledgered records, sha256-stamped, engine=`mysql` (throwaway's classification; production now reads this as `aurora-mysql` after this cycle's fix), engine_version="8.0.42 (Aurora MySQL)".
- `/app/backend/estate_keys/data_sources/aws_iam_user_AKIAXGH5.json` mode 0600, `git check-ignore -v` exit 0 (gitignored via `backend/estate_keys/.gitignore`).
- The throwaway inventory-retry script was garbage-collected before recovery (`/tmp/tmp*.sh` gone). The receipt log itself is the artifact.

**Owner Data-API values (from the recovery message; matched byte-for-byte against on-disk FINAL JSON records):**
- region: `eu-west-1`
- cluster_arn: `arn:aws:rds:eu-west-1:494452543252:cluster:db-restore-603-cluster`
- secret_arn: `arn:aws:secretsmanager:eu-west-1:494452543252:secret:rds/data/api/user/secrets-8rZuVc`
- databases: `digicow_live`, `ndume`
- owner note: **"read access to all records in those two databases"** (this first pass STRUCTURE ONLY; record-level access deferred pending owner's data-handling agreement — recorded as an honest posture, not a refusal).

**Sweep at recovery (before any code change) — hit_count = 0:**
- Full-length AWS access key across `/app`, `/tmp`, `/var/log/supervisor`, `/root`, `/etc`, both git worktrees, both git histories, `/root/.emergent/tool_outputs/*`, `/root/.emergent/automation_output/*`, `/app/assessment_workspace/phase0/**` — all **0** hits (excluding the custody file which is expected and mode-0600 + git-ignored).
- Full-length AWS secret access key across the same axes — **0** hits (custody file excluded).

**Cycle executed post-recovery (tests-first, with right-reason receipt banked BEFORE implementation):**

1. **FL-P2-24 OPENED** recording the fact that the throwaway retry script bypassed the production `services.connect.rds_data_submit.submit()` path. Not silently reconciled — the honest record shows the retry ran via a throwaway. The inventory receipts are trusted because they measured a real cluster and the row counts + column shapes are `information_schema` output, but the honest ledger records that the pipeline that produced them was not the production path.
2. **Root cause named:** `rds_data_submit`'s engine detection never probed `@@aurora_version`. It hardcoded `engine='aurora'` and had no `engine_version` field, so an off-band wrapper's classification `engine='unknown'` on the real `8.0.42` cluster went unfixed and the inventory retry had to bypass. Fixed tests-first this cycle:
   - Right-reason failure receipt: `phase0/drill_receipts/20260819T153408Z_engine_detect_right_reason_failure.log` — 7 new engine-detect tests fail on `AttributeError: _probe_engine absent` + hardcoded `engine='aurora'`; 17 pre-existing rds_data tests remain green.
   - Track-a commits (tests-first, then implementation):
     - `8c9304d` Phase 1 tests-first · 7 new engine-detect gating assertions using the REAL captured strings (`version='8.0.42'`, `version_comment='6252a59a'`, `aurora_version='3.10.3'`) — proves engine must classify as `aurora-mysql`, engine_version must carry both the MySQL version and the Aurora version.
     - `746dece` Phase 1 implementation · `_probe_engine(client, payload) → (engine, engine_version)` with MySQL-shape probe (`SELECT @@version, @@version_comment, @@aurora_version`) then PostgreSQL-shape fallback (`SELECT version(), aurora_version()`), no exception escapes, `("unknown", None)` if both fail. `submit()` wires the probe result into the response and the persisted record; failure branch records `engine='unknown'` since the probe never fires.
   - Green receipt: `phase0/drill_receipts/20260819T154016Z_engine_detect_green.log` — 24/24 rds_data_submit green (17 prior + 7 engine-detect) + 106/106 cycle cohort green (ip_allowlist_middleware + estate_keys_and_connect_estate + credentials_paste_parser + rds_data_submit + remote_harden_sudo_invocation + harden_sh_defeats_include_precedence + connect_gpu_acceptance_wired + connect_gpu_pipeline + connect_gpu_scope_S_or_M). **Zero regressions.**
   - **FL-P2-24 CLOSED same cycle** citing commit `746dece`. The next run against this cluster now needs no bypass; the production path classifies `8.0.42 + aurora_version=3.10.3` as `aurora-mysql`.
3. **STATE refreshed** (this note + DECISIONS.md entry + PINS.md DATA CONNECTED block).
4. **Assessment-repo master commit** carrying STATE + FINAL JSONs + drill receipts (right-reason + green + inventory + pre-inventory pipeline).

**Standing invariants unchanged this cycle:**
- `SPINE_ALLOWED_IPS=34.16.56.64` unmodified. Owner's client `/32` still not received; FL-P2-09 remains OPEN.
- Pod egress IP still `35.225.230.28` from the prior cycle (rotation continues; irrelevant to Data API — HTTPS out via boto3 with no VPC peering).
- Estate ed25519 private key mode 0600, never committed, never in return values.
- No push in either direction (Owner Clarification 1 unchanged).
- No LLM transit for creds: `test_module_declares_no_llm_or_forbidden_libraries` remains green on `rds_data_submit`; `_probe_engine` calls only `client.execute_statement` (boto3), no external HTTP client, no shield, no LLM SDK, no logging of payload values.
- The five previously-superseded records (`data_source_synthetic-nonexistent_*.json`, `data_source_x_*.json`, `data_source_akki-aurora_20260818T201249Z.json` from earlier cycles' failure-branch dry runs) are retained on disk as their own honest history.

**Not-yet-live (deferred to next cycle, honestly noted, unchanged from prior):**
- Registry `DATA CONNECTED` tab still renders the honest-empty-state sentence in the current pod. The two `digicow_live` / `ndume` records are on disk and PINS-referenced, but the frontend wiring that would render them as record rows is the P1 A4-Registry-honest-state increment (deferred, sized separately, next cycle).
- Record-level access (`SELECT * FROM …`) is NOT exercised this cycle; the pass read `information_schema` only. Awaiting owner's data-handling agreement to admit any records into the estate.


## Owner Phase-0 Execute cycle · 2026-08-18 · bootstrap credentials received via channel

Owner delivered the AISCA VM bootstrap credentials directly through this channel (their prerogative; their operator /32 never entered the estate allowlist so the surface was unreachable to them). The bootstrap password entered the pod as `BOOTSTRAP_SSH_PASSWORD` env-grade for the duration of exactly one Python process per submit call; never argv, never disk, never STATE, never log, never ledger row. Referenced everywhere by sha256[:12] = `c508af8a9e7c`.

**Preflight** (2026-08-18T18:08:53Z): TCP 41.173.184.244:22 reachable (bash `</dev/tcp/…` exit 0). Pod egress this cycle: `35.184.53.215` (rotation from `35.225.230.28` last cycle → `104.198.214.223` → `34.170.12.145` → original `34.16.56.64`). VM's Security Group already permits our current egress (preflight passed without SG changes).

**Pipeline stages · timestamps · outcomes:**

| Stage | Time (UTC) | Verdict |
|---|---|---|
| credential_intake (ledger event only) | 2026-08-18T18:10:34.66Z | ok |
| declaration_fire (actor `infrastructure.vm.akki-vm`, scope `archive.ingestion`) | 2026-08-18T18:10:34.66Z | ok |
| **first attempt: hardening → remote_harden** (bare bash invocation as ubuntu; /etc/ssh/sshd_config not writable → exit 11) | 2026-08-18T18:10:52.37Z | **FAILED** |
| tests-first fix: sudo -n prefix (`test_remote_harden_sudo_invocation.py` · 2 assertions) + implementation (spine commits `8baf4c2` → `41c8bf2`) | 2026-08-18T18:12:36 – 18:13:04Z | 14/14 hardening-suite green |
| **retry: hardening → external_probe** (harden.sh ran clean as root but external probe returned `permission denied (publickey,password)` because sshd_config.d/50-cloud-init.conf carries `PasswordAuthentication yes` and OpenSSH takes the first obtained value) | 2026-08-18T18:13:28.39Z | **FAILED** |
| tests-first fix: dropin at `/etc/ssh/sshd_config.d/00-akki-no-password.conf` (sort key beats 50-cloud-init.conf) — `test_harden_sh_defeats_include_precedence.py` · 3 assertions + phase0/harden.sh update (spine commit `f91246d`) | 2026-08-18T18:15:07 – 18:15:23Z | 3/3 dropin gate green |
| key-only re-harden (bootstrap already retired → pipeline's `key_install` step would refuse, so ran the pipeline primitives `_do_remote_harden` → `_do_external_probe` → `_write_receipt` under the estate key) — same primitives, same ledger shape, not ad-hoc shell | 2026-08-18T18:16:31 – 18:16:47Z | **hardening attested · external_probe: password_refused** |
| **LEAK NEUTRALIZED** (probe timestamp) | **2026-08-18T18:16:47Z** | **password auth dead server-wide** |
| acceptance.sh (uploaded via scp under estate key, invoked via `sudo -n bash`, output parsed by `services.compute_seam.acceptance_parser.parse_output`) | 2026-08-18T18:17:47 – 18:17:52Z | exit 2 · HELD |
| vendor evidence gather (nvidia-smi, mounts, lsblk, sshd -T) | 2026-08-18T18:18:12Z | evidence banked verbatim |
| commissioning record write · PINS update | 2026-08-18T18:19:23Z | complete |
| leak sweep (grep -F fixed string, `git grep -F -I`, `git log -S`) across /app, /tmp, /var/log/supervisor, /root, both git worktrees + both histories | post-commit | **hit_count = 0** |

**§6 acceptance verdict — HELD → escalated to vendor** (zero data movement; standing "1× is not a fallback" preserved):

| §6 requirement | Ordered | Delivered | Delta |
|---|---|---|---|
| Password auth dead | yes | **yes** (sshd -T: passwordauthentication no, kbdinteractive no) | **GREEN** |
| GPUs | 4× H200 NVLink | 2× H200 (indexes 0/1), NVLink active on both (26.562 GB/s per link) | **MISS · 2 short** |
| HSS storage | ~30 TB writable at /mnt/hss | 5.9 TB at /mnt/volume_dkgjrkx (wrong mount name, 5× under) | **MISS** |
| vCPU | 84 | 36 | **MISS · 48 under** |
| Memory | 948 GB | 460 GB | **MISS · 488 under** |
| Ephemeral scratch | ≥10 TB at /mnt/ephemeral | absent (root disk 74 GB only) | **MISS** |

**Deliverables (all local; no push):**
- Commissioning record: `phase0/commissioning_records/commissioning_akki-vm_20260818T181923Z_FINAL.json` sha256 `7e08cdb4e4bb5091a3c4687e3af7aab6936de6f405dd806c3756f50fee70bf81`
- Hardening receipts: `phase0/drill_receipts/hardening_20260818T18{1034,1308,1631}Z/` (three progressions: fail → fail → attested)
- Vendor-evidence bundle: `phase0/drill_receipts/20260818T181808Z_vendor_evidence.log`
- Acceptance run: `phase0/drill_receipts/20260818T181742Z_acceptance_run.log`
- Right-reason receipts: `20260818T181236Z_sudo_invocation_right_reason_failure.log`, `20260818T181507Z_harden_dropin_right_reason_failure.log`
- Green receipts (implicit in the per-file test-suite outputs and commit trailers)

**Standing invariants unchanged:**
- `SPINE_ALLOWED_IPS=34.16.56.64` unmodified. Owner's client /32 still not received (FL-P2-09 remains OPEN). Deployment stays refusing the public.
- `phase0/acceptance.sh` untouched (frozen at §6 spec — only `phase0/harden.sh` and `services.compute_seam.hardening.py` changed).
- Estate ed25519 private key mode 0600, never committed, never in return values.
- Password sha256[:12] = `c508af8a9e7c` referenced by prefix only; plaintext never in any file, log, STATE row, ledger row, receipt body, or reply.
- No push in either direction.

**Not-yet-live (deferred to next cycle, honestly noted):**
- COMPUTE CONNECTED tab does not yet render the real commissioning record. The record is on disk and PINS-referenced; the Registry `Compute connected` tab still shows the honest-empty-state sentence. Per owner rule 4, "if that tab wiring is not yet live, note it as next-cycle and don't rush it" — noted.


## COMPACTION-RECOVERY NOTE · 2026-08-14T02:1x UTC (this cycle)

Cold-read verification completed per owner's recovery-check directive:
- STATE/DECISIONS.md carries most recently: owner course-correction ("piecing together… progressive journey", line 467); 5-step wizard cycle closure (lines 485-488); Owner Simplification ruling verbatim at line 496 ("keep this simple - i need to be able to key in the creds i get form the Aisca system…"). Recovery received the ruling on disk; no re-send needed.
- programme/track-a HEAD confirmed as `f83b509` (pre-simplification baseline: 90 backend + 12 allowlist + 21 rehome = 123/123 green). Assessment-repo HEAD `3eb21c6`. Estate keypair custody intact (private mode 0600, never committed). IP allowlist unchanged (`SPINE_ALLOWED_IPS=34.16.56.64`).
- Deposit found on-disk: `backend/tests/invariants/test_credentials_paste_parser.py` (15 pre-compaction failing tests). Compaction interrupted the simplification build immediately after test scaffolding.

**Cycle executed post-recovery (tests-first with right-reason receipts BEFORE each implementation):**

1. Updated the paste-parser test file per Owner Q2 addendum (custody: response never carries the password back; password_captured signal only) — added 3 explicit gating tests (`test_endpoint_response_never_carries_password_verbatim`, `test_endpoint_response_signals_password_captured_false_when_absent`, `test_router_does_not_persist_or_log_password`) alongside the 15 pre-existing tests. 18/18 fail with `ModuleNotFoundError: No module named 'services.credentials_paste'` — right-reason receipt: `phase0/drill_receipts/20260815T015421Z_credentials_paste_parser_right_reason_failure.log`.
2. Implemented `backend/services/credentials_paste/{__init__.py, parser.py, router.py}` — pattern-only parser (case-insensitive synonym table; label:value + label=value; auto-detect via per-kind label counting with documented compute tie-break); router strips password/api_key from response, returns `password_captured` boolean; empty paste → 400. NO LLM SDK, NO HTTP client, NO subprocess, NO synisense reference (proved by static + runtime gating). 18/18 green.
3. Rewrote the frontend gating (`pod_shell/frontend/__tests__/rehome.test.js`) — retired 5-step-nav testids, added single-panel invariants (connect-panel / connect-paste-input / connect-parse / connect-submit / chip-auto-detect / '•••• captured' sentinel / parse-missing-fields / manual-field-* / provisioning-card-toggle / no-LLM-endpoint reference / live parse-paste probe). 6/23 fail right-reason before wizard collapse — receipt: `phase0/drill_receipts/20260815T015855Z_single_panel_right_reason_failure.log`.
4. Rewrote `ConnectWizard.jsx` (both `/app/frontend/src/components/ConnectWizard.jsx` live pod copy AND `pod_shell/frontend/src/components/ConnectWizard.jsx` repo copy) — 623 → 451 lines (−172, −28%). Single panel with type chips, paste textarea, deterministic parse call, confirm-then-connect view, ask-again grammar, provisioning card one-tap aside, and post-submit result views (handshake walk for compute, intent-recorded for non-compute). 23/23 rehome + 12/12 allowlist + 108/108 backend = **143/143 gating tests green** at programme/track-a HEAD `c490ce9`.
5. Playwright render-tree screenshots (via page.route interception fulfilling `/api/*` from the local backend with XFF spoof; CRA dev-server hit at 127.0.0.1:3000 also passes the allowlist under the same spoof) captured at `phase0/drill_receipts/screenshots/20260815T021700Z_{single_panel_open, paste_parsed_confirm, paste_parsed_with_provisioning_card, handshake_walk_result}.jpeg`.
6. No-LLM-transit hard-rule proof banked at `phase0/drill_receipts/20260815T021348Z_no_llm_transit_proof.log` — five axes: (a) parser module source has no forbidden import patterns; (b) router module source has no forbidden substrings; (c) live probe response omits sentinel password (grep count 0); (d) backend logs omit sentinel (grep count 0); (e) frontend source has no LLM-endpoint reference.

Standing invariants confirmed unchanged this cycle:
- `SPINE_ALLOWED_IPS=34.16.56.64` unmodified. Deployment stays refusing the public (owner client `/32` still not received; FL-P2-09 remains OPEN pending owner disposition).
- Pod egress IP has rotated AGAIN to `35.225.230.28` (was `104.198.214.223` last cycle; was `34.170.12.145` cycle before that). Recorded in PINS.
- Estate ed25519 private key remains at `${ESTATE_KEYS_DIR}/estate_ed25519` mode 0600; never committed; never in return values.
- `phase0/acceptance.sh` frozen at §6 SKU spec (untouched this cycle).
- No push in either direction (Owner Clarification 1 unchanged).
- Password never appeared in any commit, log, STATE row, or ledger entry; sentinel scans clean.


## Standing owner instruction · 2026-08-14 · POSTURE CORRECTION

Verbatim from the course-correction reply:
> "I worry you are more focussed on whats missing than piecing together what you have. to drive a progressive journey."

**Binding standing posture (applies to every cycle from now on until explicitly rescinded):**

- **Assemble the progressive journey from what exists.** Piece together from the fixture materials, guide figures, and prior decisions rather than gating on what has not yet arrived.
- **Escalate only TRUE blockers.** Missing paint colours, missing screenshots that repeat information already in a written spec, or ambiguities that can be resolved by reading the brief carefully are NOT true blockers.
- **Change is tone and initiative, NOT evidence standards.** Honesty discipline unchanged: no fabrication, no invented fixture material, no papering over conflicts, still escalate-and-stop on genuine ruling conflicts.
- **When in doubt between reporting-and-waiting vs building-and-reporting: choose building-and-reporting, provided the fixture materials contain enough grammar to build honestly.**


## Course-correction event · 2026-08-14 · fixture-drop follow-on

Owner course-corrected the fixture-drop cycle with three rulings + one build proposal:

1. **FL-P2-14 CLOSED BY OWNER.** The "19 pages" was the owner's claude.ai prototype, not a missing deck. The fixture set (5-page written brief + Registry screenshots + AISCA guide figures) IS the fixture. Stop chasing it.
2. **Standing posture correction** (recorded above).
3. **Wizard is generic.** Prior build shipped Compute-chip -> straight to a 7-field form; the brief specifies FIVE conversational steps for ALL kinds. Rebuild the wizard to the brief's 5-step grammar, tests-first.
4. **Provisioning-card proposal** from AISCA Fig 10/11: generate estate keypair in seam custody; render public key + pod egress IP as a card BEFORE credentials are keyed; owner pastes public key into VM Access + adds both /32 rows at creation; VM becomes key-reachable from first boot.

**Executed this cycle (tests-first, both banked with right-reason receipts before implementation):**

- Backend: `services/estate_keys/keypair.py` (idempotent ed25519 openssh keypair custody, private mode 0600, never in return values). `services/connect_estate/router.py` with `GET /api/connect/estate-facts` + `POST /api/connect/intent`. Both mounted in pod-shell server behind the IP allowlist middleware.
- Frontend: `ConnectWizard.jsx` rewritten as a 5-step state machine with per-type branches at Step 2, provisioning card at compute Step 2, GPU form at compute Step 3, name-in-the-estate's-words at Step 4, handshake walk at compute Step 5, honest intent record at non-compute Step 5. Registry unchanged from the previous cycle.
- Scope reported both ways: strict L (2 new contracts) vs cohesive M (one incremental surface per owner's phrasing). Built under the cohesive reading per owner's "ships NOW" imperative.
- 123/123 total gating tests green (90 backend python + 33 frontend node --test).
- Six Playwright screenshots banked under `phase0/drill_receipts/screenshots/20260814T190000Z_*.jpeg` proving all 5 steps + non-compute honest Step 5.
- Fidelity ledger: FL-P2-14 CLOSED-BY-OWNER, FL-P2-16 CLOSED (wizard grammar), FL-P2-17 CLOSED (provisioning card), FL-P2-18 CLOSED (posture correction).
- IP allowlist unchanged: `SPINE_ALLOWED_IPS=34.16.56.64` per owner's strict directive.
- Live provisioning-card content this cycle (rotates on pod restart):
  - Estate public-key fingerprint: `SHA256:TpJcdNAQ4iSQKK5inwPueOM6Qak5NcsD5XhZpWorZ+c`
  - Pod egress IP: `104.198.214.223` (was `34.170.12.145` earlier this session; STATE previously pinned `34.16.56.64`)

**Track-a commits this cycle:** `760c53d` (tests-first · 33 assertions), `5f67591` (backend implementation · 12/12 green), `f83b509` (frontend implementation · 21/21 rehome green).

**Assessment-repo master commit:** pending this cycle's follow-up (STATE + fidelity ledger + phase0 receipts + DECISIONS appendix + screenshots).


## Fixture-drop event · 2026-08-14 · Screen mockups v7 delivery

Owner dropped `fixtures/screen_mockups_v7.pdf` (sha256 `418ad0e3...`, 195,644 bytes) plus a textual description of 4 inline screenshots covering the Registry surface (three tabs + role switcher + "+ Connect") and the Connect wizard (conversation-not-form drawer with 4 suggestion chips + free-text + Send). Owner directed reconciliation orders: (a) re-shape GPU credential entry to honor the wizard grammar (Compute path collects same 7 ordered fields, submit machinery unchanged); (b) Registry three tabs render HONEST current state, not the mockup's demo-org figures (A4 increment, next cycle); (c) role switcher = static presentation (Track-B auth deferred); (d) scope check on (a).

**Discrepancy flagged as FL-P2-14 OPEN:** owner said "19 pages plus 4 inline screenshots" - actual PDF is 5 pages of pure text (Registry Feature & Component Brief, zero embedded images); the 4 inline screenshots weren't accessible as job assets. Owner's inline textual description stands as the binding visual reference; PDF stands as the written spec. Written spec + inline description was sufficient for this build.

**Executed this cycle:**

1. Fixture pinned in PINS.md as file-cleared (upgraded from transcription-grade for Registry surface + Connect wizard grammar). Full page-by-page inventory at `fixtures/screen_mockups_inventory.md`.
2. Scope check for (a): **M class** (2 components + 0 new contracts + 1 integration surface, unchanged) - within WS-BUILD-CONNECT-GPU scope ceiling.
3. Test-suite migration:
   - `pod_shell/frontend/__tests__/rehome.test.js` grew from 9 to 15 gating assertions.
   - 7 retained (unchanged), 2 migrated (root '/' now → Registry; AdminSurface retired), 6 new (Registry testids + wizard shape + Compute path + endpoint unchanged + zero fabricated numbers + honest empty state).
   - Right-reason failure receipt banked at `phase0/drill_receipts/20260814T180000Z_registry_wizard_right_reason_failure.log`: 7/15 fail with right-reason errors before implementation lands.
4. Implementation on `programme/track-a`:
   - `src/App.js` → root '/' renders `<Registry />` (was `<AdminSurface />`).
   - `src/components/Registry.jsx` NEW: header (Akki · ESTATE + role switcher chips + user glyph), title deck, tab bar (DATA CONNECTED · COMPUTE CONNECTED · LLMS & TRAINED MODELS with 2px active underline), "+ Connect" button pushed right, empty-panel body honoring Content Rule 3.
   - `src/components/ConnectWizard.jsx` NEW: right-hand drawer with "Connect something new" + "A conversation, not a form" deck, 4 suggestion chips, free-text + Send, Compute path branches to the SAME 7 ordered GPU fields with masked password → POST to unchanged `/api/connect/gpu`.
   - `src/components/AdminSurface.jsx` DELETED (superseded).
5. Live-proof:
   - Preview URL: 4/4 route families still refused with HTTP 403 + exact sentence (allowlist unchanged).
   - Local FE with allowed XFF: `/` → 200 SPA shell; `/register/connect/gpu` → 404 retirement notice.
   - Local BE with allowed XFF: `/api/deliverables` → 200 JSON; `POST /api/connect/gpu {}` → 422 Pydantic (same payload contract).
   - Playwright: 4 screenshots banked at `phase0/drill_receipts/screenshots/20260814T181000Z_*.jpeg`; all 20 required data-testids present in rendered tree.
6. Green receipt banked at `phase0/drill_receipts/20260814T181500Z_registry_wizard_green.log`. 105/105 gating tests green.
7. Fidelity ledger: FL-P2-11 CLOSED (fixture upgrade), FL-P2-12 CLOSED (wizard-not-form), FL-P2-13 CLOSED (demo-data-vs-honest-state), FL-P2-14 OPEN (page-count discrepancy), FL-P2-15 CLOSED (role switcher static).
8. IP allowlist unchanged: `SPINE_ALLOWED_IPS=34.16.56.64` per owner's strict directive.

**Track-a commits this cycle:** `65964b0` (tests-first · Registry + wizard invariants), `aeb2be0` (implementation · Registry + wizard 15/15 green).

**Assessment-repo master commit:** pending this cycle's follow-up (STATE + fidelity ledger + phase0 receipts + fixture inventory + PDF + DECISIONS appendix).


## Compaction / recovery event · 2026-08-14 · mid-stop-order execution

Third compaction / restart occurred mid-execution of the Owner Stop-Order (queued: revoke token → build IP allowlist middleware tests-first → re-home form → propose IP-pinned access mechanism → commit both repos). Post-compaction recovery sequence executed:

1. **Security verification (P0, before anything else).**
   - `/app/backend/.owner_credentials` — verified DELETED (was still present at recovery start; deleted this session; backend restarted; deleted again to discard the auto-mint that spine_auth performed at import).
   - `/app/backend/spine_auth.py` — verified DELETED (token machinery retired estate-wide).
   - `/app/memory/test_credentials.md` — verified SCRUBBED (no 64-hex tokens anywhere; scrubbed content replaced with IP-pinned access posture).
   - Old compromised token probe on `/api/connect/gpu` → HTTP 403 (was HTTP 422 = accepted before revocation).
   - Leak hunt: 0 hits across `/app` filesystem (excluding pycache), 0 hits in spine repo git-grep, 0 hits in `/var/log/supervisor/*.log`, 0 hits in STATE/notes/phase0.

2. **Lockdown verification.**
   - `services/ip_allowlist/middleware.py` (spine repo) exists · 16/16 gating tests green.
   - `plugins/ip-allowlist/{check.js, middleware.js}` (pod-shell frontend) exists · 12/12 gating tests green.
   - `SPINE_ALLOWED_IPS=34.16.56.64` + `SPINE_TRUSTED_PROXY_HOPS=2` present in `/app/backend/.env` (single source of truth read by both backend and frontend craco config).
   - Live proof · preview URL: `/`, `/register/connect/gpu`, `/api/deliverables`, `/api/connect/gpu`, `/static/*` all return HTTP 403 `text/plain` with the exact sentence `"This surface answers allowlisted addresses only."` (refusal branch, pod egress `34.170.12.145` NOT in allowlist per owner's strict `34.16.56.64` directive).
   - Live proof · 127.0.0.1 with crafted XFF: allowed IP at `xff[-3]` → 200; disallowed IP at `xff[-3]` → 403; spoofed leftmost XFF entries on allowed IP → still allowed; spoofed leftmost XFF entries on disallowed IP → still refused (spoof resistance intact).

3. **Cold-read of STATE/ this recovery cycle.**
   - DECISIONS.md carries Rulings 1/2/3, Orchestrator A/B/C, Build Order 01, Owner Clarifications 1-3, prior WS-BUILD-CONNECT-GPU rulings, AND the new Owner Stop-Order Ruling (verbatim reconstruction) plus the Orchestrator shared-defect ruling appended this cycle.
   - PINS.md carries prior repo/canon/fixture pins; refreshed this cycle with new HEAD SHA, egress-IP surprise notation, updated gating count.
   - NEXT.md updated to reflect completed stop-order execution and the awaited owner reply.
   - Fidelity ledger appended: FL-P2-08 CLOSED (minted-credential retirement), FL-P2-09 OPEN (pod-egress rotation), FL-P2-10 CLOSED (empirical trust-boundary discovery).

4. **Re-home completion status.**
   - `/register/connect/gpu` retired at edge (dev-server middleware returns HTTP 404 `text/plain` `"This route has been retired."`).
   - `/app/frontend/src/App.js` — root `/` → `<AdminSurface />` · catch-all `*` → `<NotFound />`.
   - `/app/frontend/src/components/AdminSurface.jsx` — new. Tile grid + detail card + embedded GPU form. NO token state anywhere.
   - `/app/frontend/src/components/ConnectGpu.jsx` — deleted (retired token-gated variant).
   - Empirical header trust boundary discovered before code landed (see Phase 0 drill receipts + FL-P2-10).
   - Right-reason failure receipts banked for BOTH new invariants (IP allowlist + re-home) before implementation.
   - Pod-shell mirror committed at `pod_shell/` in Extraction-Akki (production-code discipline preserved: source of truth remains `/app/{backend,frontend}` since those are what run; the mirror is the git-tracked record on programme/track-a).

5. **Commits this cycle.**
   - programme/track-a: `e25cfe3` (IP allowlist tests-first), `93ed48e` (IP allowlist implementation), `d2a3a01` (re-home tests-first), `acc25a8` (re-home + pod-shell mirror).
   - assessment-repo master: pending this cycle's commit (STATE + fidelity ledger + phase0 receipts + DECISIONS appendix).

**Resume point (per NEXT.md):** deliver stop-order completion report to owner including security-verification results, live-vs-test proof rollup, commit SHAs, and the two-sentence access-mechanism proposal.


## Compaction / recovery event · 2026-08-14 · post-fixture-arrival

Second compaction / restart occurred after fixture-arrival cycle (queued message: FIXTURES ARRIVED — download + hash + extract + clear FIXTURE PENDING + update DoDs + extract SOPs + escalate-and-stop on conflicts). Cold-read from disk performed against STATE/ before resuming.

**Present on disk (verified):**
- STATE/{CONTEXT,PINS,DECISIONS,NEXT}.md — all four; DECISIONS.md carries Rulings 1/2/3, Orchestrator A/B/C, Build Order 01 verbatim (dated 2026-08-14), and Owner Clarifications 1-3 (no-push · VM SSH access to be granted · fixtures re-upload).
- `BUILD_STRATEGY.md` — 2441 lines at commit `42b241c` (v1.1 self-contained assembly).
- `REUSE_ASSESSMENT.md` — 53,479 bytes, accepted.
- `notes/fidelity_ledger.md` — 101 lines, 8+7+12+1+1+2 = 31 rows CLOSED (owner's 27 + FL-R1-01/FL-P1-20 retained + FL-P2-01/02 opened during Part-2 drafting).
- `fixtures/Akki_Prototype_v7_Design_Brief.md` — 18,791 bytes · sha256 `063f2b470d74dcd30ad43b4645c4e656edaa7fb1185198a4116ad5328a9717b4`.
- `fixtures/AISCA_GPU_Access_Guide.pdf` — 535,169 bytes · sha256 `0f6b6e0f692494e18a65df655fddf48f45839005dc7aa6b988239b8f90e157f3`.
- `fixtures/reference_screenshot_transcription.md` — created this recovery cycle from owner's inline transcription (Q1(c) ruling · 2026-08-14) · sha256 `d3ae9a6cf598a38333b5c11d6d73dc9069dc3671fb31598f2e594dfb002fc949` · grade AUTHORITATIVE-UNTIL-FILE-ARRIVES.
- `phase0/` — commissioning_checklist.md · acceptance.sh · commissioning_record_template.md · A0-A1_report.md · drill_receipts/20260814T120336Z_declaration_refusal_firing.log.
- Extraction-Akki clone with branch `programme/track-a` (baseline `b150c21`); Phase-1 code + tests staged on disk (7 new files under `backend/`) — pending commit on `programme/track-a`.
- Pod egress IP re-verified fresh via 4 curl services: **`34.16.56.64`** (unchanged; no IPv6).

**Missing / requires immediate action:**
- **Corrections commit (post-`42b241c`) NOT YET MADE on assessment repo.** `BUILD_STRATEGY.md` at HEAD still carries the three defects Build Order 01 named:
  - Line 1742: "Nine XL items" (stale count).
  - Line 2017: "Placeholder — Part 2 has not been drafted yet".
  - Line 1939 (FL-OQ-04) and Line 2165 (§Appendix C5-010..C5-012 row): "four consoles" phrasing.
  Working papers `notes/strategy_sections.md` and `notes/fidelity_ledger.md` carry the corrected content (uncommitted); BUILD_STRATEGY.md needs a re-assembly + commit.
- Fixture SHA-256 hashes not yet in `PINS.md` (attachment-status line still records "NOT yet delivered").
- Item DoDs across BUILD_STRATEGY.md interface items still read `FIXTURE PENDING`; awaiting binding-acceptance-criteria extraction from v7 brief + transcription, and `test_four_questions_topline_present` addition to their new-invariants lists.
- AISCA GPU SOP not yet extracted / reconciled against Order §6 (escalate-and-stop on conflict per owner's Q2(a) ruling).
- Phase-1 test/code files (`backend/contracts/*.py`, `backend/services/declaration/*`, `backend/services/compute_seam/*`, `backend/tests/invariants/actor_declaration_*`) staged on `programme/track-a` but NOT YET committed — HEAD still at `b150c21`. Owner's Q3 ruling this cycle covers ONLY the assessment-repo master commit; `programme/track-a` phase-1 commit is a separate cycle and stays untouched here.
- FL-P1-14 in the ledger reads `CLOSED — fixture is the attached screenshot plus the attached v7 brief`; this now needs the transcription-cleared vs file-cleared grade distinction per owner's Q1(c) ruling.

**Resume point (per owner's plan-confirmation rulings):**
1. Extract binding acceptance criteria from v7 brief + transcription into `fixtures/binding_acceptance_criteria.md`.
2. Extract AISCA SOP into `fixtures/aisca_sop_extraction.md`; reconcile against Order §6 bindings; escalate-and-stop on any conflict.
3. Update PINS.md (fixture hashes + attachment-status flip).
4. Update fidelity_ledger.md FL-P1-14 with transcription-cleared vs file-cleared grade distinction; add fixture-arrival log row FL-P1-14a.
5. Rewrite `FIXTURE PENDING` markers across BUILD_STRATEGY.md item DoDs to cite the extracted criteria; add `test_four_questions_topline_present` to console items' new-invariants lists.
6. Apply the three Build-Order-01 corrections in BUILD_STRATEGY.md (via assembly tool re-run, since notes/ already carry the corrected content).
7. Re-run citation_audit.py + completeness_audit.py.
8. Refresh backend/deliverables snapshots.
9. Commit on assessment-repo `master` (linear record per owner's Q3 ruling); update NEXT.md.
10. Reply to owner with the phase-1/fixture report + fresh egress IP.


## Where we are

- **Execution authorized** on branch `programme/track-a` in Extraction-Akki (baseline `b150c21`, never rewritten). Production-code prohibition lifted ONLY for this branch per Build Order 01.
- **All 27 fidelity-ledger rows CLOSED** by Build Order 01 rulings; ledger frozen.
- **Three corrections applied** (§10.F stale placeholder replaced; XL count 9→7 reconciled; Canon 5 §10 "exactly five consoles" verified — extraction was fine, premise was paraphrase defect).
- **Phase 1 A0/A1 tests-first GREEN** — 26/26 gating tests pass; declaration-refusal drill banks Ruling-1 precondition (a).
- **Compute seam built** (folded into Phase 1 per Owner Clarification 2) with tests-first discipline; ready for credentials.
- **Pod egress IP** `34.16.56.64` reported for VM allowlist.
- **Rulings issued:** Ruling 1, Ruling 2, Ruling 3/Instruction 02, Orchestrator Rulings A/B/C, Build Order 01, Owner Clarifications 1-3. All verbatim in `DECISIONS.md`.
- **No push** (Owner Clarification 1). Local git history IS the record.
- Prohibitions still in force for anything OFF `programme/track-a`: no production code, no scaffolding, no canon edits.

## Attachment gap (recorded per Owner Clarification 3 · 2026-08-14)

The three fixtures referenced by Build Order 01 — reference screenshot, `Akki_Prototype_v7_Design_Brief.md`, `AISCA_GPU_Access_Guide.pdf` — were NOT delivered with the order and had NOT arrived as of Owner Clarification 3 (re-upload signalled). Per the order's own text "every FIXTURE PENDING clears on their arrival in the workspace," FL-P1-14's substantive closure is CONDITIONAL. Fixture-bound work (A4 operating surface, Track-B console items, Watch Console §6 verbatim consumption) is BLOCKED until they land. **Nothing in A0-A3 is blocked.**

## Deliverable manifest (current)

- `/app/assessment_workspace/REUSE_ASSESSMENT.md` (450 lines) — Chunk-3 accepted.
- `/app/assessment_workspace/BUILD_STRATEGY.md` — Chunk-4 v1.2 self-contained (re-assembled after Build Order 01 + rulings).
- `/app/assessment_workspace/phase0/` — commissioning_checklist.md · acceptance.sh · commissioning_record_template.md · A0-A1_report.md · drill_receipts/.
- `/app/assessment_workspace/repos/Extraction-Akki/` (branch `programme/track-a`, baseline `b150c21`):
  - `backend/contracts/actor_declaration.py`, `backend/contracts/record_matrix.py`, `backend/contracts/task_identity.py`
  - `backend/services/declaration/`, `backend/services/compute_seam/`
  - 7 new invariant tests + parity-seat snapshot in `backend/tests/invariants/`
  - `backend/tools/report_egress_ip.sh`, `backend/tools/ssh_preflight.py`, `backend/tools/run_acceptance_via_seam.py`.
- Working papers on disk (feeding BUILD_STRATEGY.md assembly):
  - `notes/strategy_items_part1.md`, `strategy_items_part2.md`, `strategy_sections.md`, `fidelity_ledger.md` (closed), `row_to_item_index.md`.
- Assembly tool: `tools/assemble_build_strategy.py`.
- STATE/ current across CONTEXT · PINS · DECISIONS · NEXT.

## Audit posture (current)

- Citation audit: 104/104 file · 1778/1778 canon · **0 failed** (post-remediation, includes BUILD_STRATEGY.md).
- Completeness audit: PASS — every non-REUSE row assigned; every item has 7 fields; BUILD_STRATEGY.md self-contained.
- Phase-1 gating tests: **26/26 pass** on `programme/track-a`. Ruling-1 precondition (a) demonstrated firing (declaration-scoped refusal observable in the ledger via drill).
- Zero regressions introduced: only new files added to Extraction-Akki, no existing code modified.

## Downloadable snapshot (2026-08-14 · Orchestrator delivery-logistics directive)

The two deliverables are served READ-ONLY through the pod template's FastAPI backend as **snapshots** (not a live mount of this workspace). Refresh discipline: after each material change to either document, re-copy from `/app/assessment_workspace/` to `/app/backend/deliverables/` and update the snapshot commit literal in the listing endpoint.

- `https://pensive-goodall-6.preview.emergentagent.com/api/deliverables/BUILD_STRATEGY.md`
- `https://pensive-goodall-6.preview.emergentagent.com/api/deliverables/REUSE_ASSESSMENT.md`
- Listing at `/api/deliverables` returns snapshot commit + size + URL for each.

## Citation-drift root cause (Orchestrator Ruling A — retained record)

Chunk-1 extraction from the `.docx` archives numbered content paragraphs consecutively BEYOND the canon's real `[Heading]` boundaries — sub-paragraph counting was not reset when a new heading appeared, so `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for all future work: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

Remediation trail: `tools/drift_map.py` + `tools/drift_apply.py` + `tools/drift_downstream.py`; edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`; FL-P1-20 retained as the defect+remediation record.

## Recovery event · 2026-08-14T09:24Z (historical)

Context compaction / restart occurred ~2026-08-14T09:24Z. Recovery from disk + queued brief succeeded; all subsequent work is captured above.

## Deliverable manifest

- `/app/assessment_workspace/REUSE_ASSESSMENT.md` (450 lines) — Chunk-3 accepted.
- `/app/assessment_workspace/BUILD_STRATEGY.md` (2442 lines) — Chunk-4 v1.1 self-contained assembly.
- Working papers on disk (feeding the assembly):
  - `notes/strategy_items_part1.md` (838 lines, 47 items).
  - `notes/strategy_items_part2.md` (628 lines, 55 items).
  - `notes/strategy_sections.md` (269 lines).
  - `notes/fidelity_ledger.md` (102 lines, 27 open items, frozen).
  - `notes/row_to_item_index.md` (405 lines, 591 rows → 102 items, 0 named gaps).
- Assembly tool: `tools/assemble_build_strategy.py`.
- STATE/ current across CONTEXT · PINS · DECISIONS · NEXT.

## Downloadable snapshot (2026-08-14 · Orchestrator delivery-logistics directive)

The two deliverables are served READ-ONLY through the pod template's FastAPI backend as **snapshots of commit `42b241c`** (not a live mount of this workspace). Snapshot copies live at `/app/backend/deliverables/{BUILD_STRATEGY.md,REUSE_ASSESSMENT.md}`; served via `GET /api/deliverables/{filename}` with a two-name allowlist. Identity verified byte-for-byte via sha256 against the workspace originals at snapshot time.

- `https://pensive-goodall-6.preview.emergentagent.com/api/deliverables/BUILD_STRATEGY.md` — 244,199 bytes, sha256 `86af07ce…c820688`.
- `https://pensive-goodall-6.preview.emergentagent.com/api/deliverables/REUSE_ASSESSMENT.md` — 53,479 bytes, sha256 `36314268…d427327a`.
- Listing endpoint: `https://pensive-goodall-6.preview.emergentagent.com/api/deliverables` returns snapshot commit + size + URL for each.

**Refresh discipline.** If either working document is amended (e.g., after a new Ruling), re-copy the file from `/app/assessment_workspace/` to `/app/backend/deliverables/` and update the snapshot commit in `CONTEXT.md` and in the `/api/deliverables` listing endpoint literal. Do NOT symlink the workspace live — the snapshot boundary is deliberate.

## Audit posture at v1.1 assembly

- Citation audit (now includes BUILD_STRATEGY.md): 104/104 file · **1778/1778 canon · 0 failed**.
- Completeness audit (now validates BUILD_STRATEGY.md self-contained): PASS — every non-REUSE row assigned; every work item has 7 fields; BUILD_STRATEGY.md self-contained confirmed.
- Cold-read recovery test: STATE/ is self-sufficient; verified.

## Ruling-3 (Instruction 02) effects on the interface strategy

- **Donor fixed:** Extraction-Akki frontend (44 production pages across 12 menu groups + 10 shell/component files — verified via direct `find` at HEAD `b150c21`).
- **Grammar fixed:** tile-grid-plus-detail-card ("Admin surface"). Reference screenshot pending — noted as fixture-pending dependency on every interface item.
- **Reclassification:** Chunk-3 Canon-5 interface rows previously BUILD (Part 2) now split — 13 items reclassified to HARVEST or MODIFY (Part 1); Watch-related items stay BUILD (Part 2).
- **Watch Console exception:** REMAINS BUILD (Part 2). Fourth group of four app tiles: `State` · `Record` · `Under Watch` · `Decisions` per Canon 8 §13. Watch-officer-role gated, sessions under Watch identity per Canon 9. **NEVER nested under Trust Center** — placement constraint encoded in the item DoD.
- **Rendering decisions:** Every label-vs-canon-identity mismatch lands in `fidelity_ledger.md` as a `RENDERING DECISION` row.

## Citation-drift root cause (Orchestrator Ruling A)

Chunk-1 extraction from the `.docx` archives numbered content paragraphs consecutively BEYOND the canon's real `[Heading]` boundaries — sub-paragraph counting was not reset when a new heading appeared, so `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for future work: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

Remediation trail: `tools/drift_map.py` + `tools/drift_apply.py` + `tools/drift_downstream.py`; edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`; FL-P1-20 retained as the defect+remediation record.

## Recovery event · 2026-08-14T09:24Z

Context compaction / restart occurred ~2026-08-14T09:24Z after Step-1 completion. Recovery performed from disk + the queued Chunk-4 brief. On-disk verification (per queued recovery protocol) passed: STATE/ intact · REUSE_ASSESSMENT.md 450 lines · notes/ 32 files (post-Ruling-A drift-tools) · repos/ 4 pinned clones · canon/ 9 extracted `.txt`.

## Ruling-3 (Instruction 02) effects on the interface strategy

- **Donor fixed:** Extraction-Akki frontend (44 production pages across 12 menu groups + 10 shell/component files — verified via direct `find` at HEAD `b150c21`).
- **Grammar fixed:** tile-grid-plus-detail-card ("Admin surface"). Reference screenshot pending — noted as fixture-pending dependency on every interface item.
- **Reclassification:** Chunk-3 Canon-5 interface rows previously BUILD (Part 2) now split — 13 items reclassified to HARVEST or MODIFY (Part 1); Watch-related items stay BUILD (Part 2).
- **Watch Console exception:** REMAINS BUILD (Part 2). Fourth group of four app tiles: `State` · `Record` · `Under Watch` · `Decisions` per Canon 8 §13. Watch-officer-role gated, sessions under Watch identity per Canon 9. **NEVER nested under Trust Center** — placement constraint encoded in the item DoD.
- **Rendering decisions:** Every label-vs-canon-identity mismatch lands in `fidelity_ledger.md` as a `RENDERING DECISION` row.

## Citation-drift root cause (Orchestrator Ruling A)

Chunk-1 extraction from the `.docx` archives numbered content paragraphs consecutively BEYOND the canon's real `[Heading]` boundaries — sub-paragraph counting was not reset when a new heading appeared, so `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for future work: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

Remediation trail: `tools/drift_map.py` + `tools/drift_apply.py` + `tools/drift_downstream.py`; edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`; FL-P1-20 retained as the defect+remediation record.

## Recovery event · 2026-08-14T09:24Z

Context compaction / restart occurred ~2026-08-14T09:24Z after Step-1 completion. Recovery performed from disk + the queued Chunk-4 brief. On-disk verification (per queued recovery protocol) passed: STATE/ intact · REUSE_ASSESSMENT.md 450 lines · notes/ 32 files (post-Ruling-A drift-tools) · repos/ 4 pinned clones · canon/ 9 extracted `.txt`.

## What Ruling 1 changes

- **Binding transition condition on the purpose-gate contradiction (Open Question #1)**: Executive-Core's `services/synisense/shield/purpose_validator.validate_purpose()` (at `client.py:63`) is NOT stripped until BOTH (a) the actor-declaration check (Canon 3 §6.1, Assessment C3-008/C3-009/C3-010) AND (b) the Watch's reconciler are DEMONSTRATED FIRING. This turns Open Question #1 from an open governance call into a conditional strip whose enabling conditions are named.
- **Implicit resolution of Open Question #2 (actor declaration seam)**: because Ruling 1 makes the declaration check a precondition for the purpose-gate strip, the declaration check is confirmed a BUILD item (not left open or absorbed elsewhere). Cite: DECISIONS.md Ruling 1.
- **Executive-Core purpose gate posture**: RETAINED as a canon-compliant surface at Executive-Core HEAD until the two demonstrations fire. Not classified RETIRE until the transition condition is met.

## Open Questions status (from REUSE_ASSESSMENT.md §8)

| OQ | Status after Ruling 1 |
|---|---|
| 1. Purpose-gate contradiction | **PARTIALLY ANSWERED** — retention is conditional, strip is enabled by two demonstrated-firings. Fidelity-ledger entry for the strip itself remains. |
| 2. Admit-declaration seam | **ANSWERED (implicit)** — declaration check WILL be built. |
| 3. Rule-change re-verify step | OPEN — remains in fidelity ledger. |
| 4. Canon 5 four vs five consoles | OPEN — remains in fidelity ledger. |
| 5. Studio canonical scope | OPEN — remains in fidelity ledger. |
| 6. Eight vs five global rules | OPEN — remains in fidelity ledger. |
| 7. Cohort surface's canonical home | OPEN — remains in fidelity ledger. |
| 8. Work_studio storage coupling | OPEN — remains in fidelity ledger. |
| 9. Akki-OS-V1 non-canonical harvest items (partitions, sequencing_harness, far_endpoint) | OPEN — remains in fidelity ledger. |
| 10. Executive-Core post-IF-1 catch-up | OPEN — remains in fidelity ledger. |

## Current activity

- BUILD_STRATEGY.md ASSEMBLED. Chunk 4 complete at freeze. Awaiting owner response on 27 open fidelity-ledger items.

## Historical: recovery event · 2026-08-14T09:24Z (superseded by assembly notes above)

Context compaction / restart occurred ~2026-08-14T09:24Z after Step-1 completion. Recovery performed from disk + the queued Chunk-4 brief. All Chunk-4 work post-recovery is documented in the assembly manifest at the top of this file.

## Ruling-2 effects on the item universe

Four WIRING items promoted (were folded); Part-1 item count 30 → 34, grand total 85 → 89.
- `WS-WIRE-CRITIC-INTO-ANSWERING` — critic_pass in-flight on the answering path (harvest lands code, wiring puts it in the request path).
- `WS-WIRE-PARITY-EXTENSION` — frozen-contract-snapshot parity discipline extended to every NEW contract this programme creates.
- `WS-WIRE-REFUSAL-FAMILY` — existing refusal-family taxonomy (`memory/memory_refusal_reasons.v0.json` + `memory/refusal.py`) wired to Canon 5 §9.2 refusal card surface.
- `WS-WIRE-LEDGER-MATRIX` — Northena ledger's sole-writer position promoted to Canon 9 §6-§18 record-matrix-governed writer.

Estimation discipline is now stranger-checkable (see Ruling 2 §1 in DECISIONS.md).
`WS-REBUILD-WORK-STUDIO-STORAGE` remains in Part 1 as a REBUILD row; its REVERSAL COST explicitly addresses user-data migration reversibility.
`fidelity_ledger.md` opens alongside Part 1 at `/app/assessment_workspace/notes/fidelity_ledger.md`; append during Part 2; freeze at BUILD_STRATEGY.md assembly.

## Ruling-3 (Instruction 02) effects on the interface strategy

- **Donor fixed:** Extraction-Akki frontend (44 production pages across 12 menu groups + 10 shell/component files — verified via direct `find` at HEAD `b150c21`).
- **Grammar fixed:** tile-grid-plus-detail-card ("Admin surface"). Reference screenshot pending — noted as fixture-pending dependency on every interface item.
- **Reclassification:** Chunk-3 Canon-5 interface rows previously BUILD (Part 2) now split — most reclassify to HARVEST or MODIFY (Part 1) with the Extraction-Akki donor page identified; Watch-related rows stay BUILD.
- **Watch Console exception:** REMAINS BUILD (Part 2). Fourth group of four app tiles: `State` · `Record` · `Under Watch` · `Decisions` per Canon 8 §13. Watch-officer-role gated, sessions under Watch identity per Canon 9. **NEVER nested under Trust Center** — placement constraint encoded in the item DoD.
- **Rendering decisions:** Every label-vs-canon-identity mismatch lands in `fidelity_ledger.md` as a `RENDERING DECISION` row.
- **Interface reclassification impact on item counts:** 13 Canon-5 items reclassified from Part-2 BUILD to Part-1 HARVEST/MODIFY, WS-BUILD-CONSOLE-WATCH stays Part-2 BUILD with new placement constraint, 11 Canon-5 items retain Part-2 BUILD status (no Extraction-Akki donor found). Part-1 total: 34 → 47 items; Part-2 total: 55 → 42 items. Grand total remains 89.

## Citation audit result at Part-1 close

Latest audit (post Orchestrator-Ruling-A remediation): **102/102 file citations verified · 854/854 canon citations verified · 0 failed.**

**Root cause of the initial drift (recorded per Orchestrator Ruling A):** Chunk-1 extraction from the `.docx` archives numbered content paragraphs consecutively BEYOND the canon's real `[Heading]` boundaries — sub-paragraph counting was not reset when a new heading appeared, so `Cn-0MM (§XX)` row IDs recorded sub-paragraph counters, not heading numbers. Prevention for Part 2: only cite `[Heading]`-numbered sections that literally appear in the extracted canon text; run `citation_audit.py` before every submission.

Remediation trail: `tools/drift_map.py` + `tools/drift_apply.py` + `tools/drift_downstream.py`; edit log at `tools/drift_edits.log`; xref at `tools/drift_xref.json`; FL-P1-20 retained as the defect+remediation record.

## Doctrinal frame

- The four-test review discipline (Ruling 1 preamble) — every parameter of success is met by a named mechanism; quality discipline held exactly as canon; no build credit spent without survivable reason; nothing lands that canon does not keep. Every work item in Part 1 must satisfy all four tests.
- Canon 9 record matrix + task-identity register + handoff contract discipline — every item cites its record classes (as Canon-9 rows from `canon_9_requirements.md`) and its task identity, even though the register itself is BUILD.
- Canon 4 §32 quality matrix + Canon 3 §31 verification packs — every item states its QUALITY EVIDENCE against these.
- "Code complete" / "tests pass" are forbidden phrasings in Definition of Done (per owner instruction).

## Repos / SHAs / paths — see PINS.md
