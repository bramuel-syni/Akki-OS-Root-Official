# DQ-11 hygiene probe · /app/backend/.env · 2026-09-22T06:15:00Z

## Trigger
Owner directive at CENSUS-3-F.2 seal boundary (2026-09-22T~06:10Z): "check NOW whether the tracked /app/backend/.env currently contains any live secret in working tree or history — if yes, that is an immediate hygiene event: bank it, flag rotation to the desk queue".

## Method
Read-only probe. Values NOT printed; only key names + length + character-diversity heuristic + regex-pattern shape hits. No secret material captured in transcript, terminal, or receipt.

## Findings — WORKING TREE + HEAD identical

`sha256(/app/backend/.env) = b7eaee7678122d9a...` matches HEAD.

### Secrets present (must rotate)

- **`EMERGENT_LLM_KEY`** · len=30 · unique-chars=20 · high entropy. **LIVE** — used by backend for LLM inference.
- **`JWT_SECRET`** · len=64 · unique-chars=41 · high entropy. **LIVE** — used to sign session JWTs; past-history holders can forge tokens.

### Placeholder-only (safe · no rotation)

- `TIGRIS_ACCESS_KEY_ID` · len=2 · unique=1 · placeholder (likely `""`).
- `TIGRIS_SECRET_ACCESS_KEY` · len=2 · unique=1 · placeholder.

### Not-secrets (paths / config / IPs)

`MONGO_URL` (local URI), `DB_NAME`, `CORS_ORIGINS`, `TIGRIS_ENDPOINT` (public URL), `SSH_PRIVATE_KEY_PATH`+`SSH_PUBLIC_KEY_PATH` (paths — actual keys under `/app/backend/estate_keys/` custody-guarded), `HARDEN_SH_PATH`, `HARDENING_RECEIPT_DIR`, `ACCEPTANCE_SH_PATH`, `SPINE_ALLOWED_IPS`, `SPINE_TRUSTED_PROXY_HOPS`, `ESTATE_KEYS_DIR`, `INTENT_RECORDS_DIR`, `POD_EGRESS_IP` (empty), `ALLOWLIST_MODE`, `OWNER_ALLOWLIST_IPS`, `AKKI_*_HOST/PORT/USERNAME/OS/HOSTNAME/HOSTS` (config), `AKKI_VM_*_SSH_PRIVATE_KEY_PATH` (paths — private-key material lives at `/app/backend/estate_keys/gpu_hosts/` custody-guarded), `AKKI_GPU_*`, `GPU_CONNECT_MODE`.

## History

- `dc48d53131be` (2026-09-19 · frontend feat) · sha256 `b7eaee7678122d9a...` · **2 secrets present**.
- `e214236a8df9` (2026-09-19 · W10 allowlist) · sha256 `bfec5f9c270be743...` · **2 secrets present** (subset of current file · 781 bytes vs 2684 bytes).
- No older tracked versions of `backend/.env`.

Historical divergence: `e214236a8df9` predates `dc48d53131be`; the SK-class keys were introduced at `e214236a8df9` and carried forward.

## Owner-side actions triggered

1. **ROTATION-REQUIRED** (owner-side · new DQ-13 in DESK_QUEUE.md):
   - Rotate `EMERGENT_LLM_KEY` at the emergent management console (Profile → Manage plan → Universal Key).
   - Rotate `JWT_SECRET` — invalidates all outstanding session tokens (users must re-login) but that is the correct fail-safe posture after historical leak.
2. **CP-DOT-ENV-HYGIENE seal** (agent-side · scheduled to ride post-R-91 boundary · new DQ-12 in DESK_QUEUE.md):
   - `git rm --cached /app/backend/.env` on `/app` main.
   - Introduce `/app/backend/.env.local` untracked-from-birth for future sensitive keys.
   - Supervisor sources both `.env` (public config) + `.env.local` (secrets).
   - Existing tracked history stays — new secrets never land in git again.
3. **CP-VEND-HUAWEI-OBS** (agent-side · DQ-11 cure · unblocks CENSUS-3-F.2.1 · authored this-turn per owner ruling): `services.secret_hygiene.huawei_obs_vend` reads OBS AK/SK/endpoint from `custody/credentials/rms_connection_creds_v1.xlsx#Huawei Creds` in-memory at process start; injects into OBS client bind directly; never writes any secret to any .env; custody-cat guard applies.

## Bounds
Zero secret material captured or transmitted. This receipt records only key-names + length + entropy heuristic + pattern class hits. Rotation is owner-side.

<!-- 20260922T061500Z_dot_env_hygiene_probe.md END -->
