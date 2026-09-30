# Existing JWT consumer regression — 2026-09-26

## M1 regression addition — 2026-09-28

The observed sign-in stall was an app reload waiting on long-running census
BackgroundTasks, not bad credentials. Keep the existing supervised census worker
as the sole queue executor. Verify complete login JSON + auth/me + overview while
an external census is pending and across an app reload. No duplicate UI polling
may continually abort the same in-flight read. Credentials, tokens, roles, cookie
architecture and seed logic remain unchanged; no arbitrary auth timer was added.

This slice preserves the existing bearer-token transport and account/password
logic. The integration playbook's generic new-cookie-auth/seeding instructions
are NOT an instruction to replace Akki's established authentication.

- Read `memory/test_credentials.md`; do not create/reset accounts.
- Verify existing operator/analyst login and `/api/auth/me` through the public
  REACT_APP_BACKEND_URL. Never log access/refresh tokens or password hashes.
- Signed-out `/dap`: show sign-in state without requesting protected overview.
- Sign in: request overview using the existing sessionStorage bearer token.
- Sign out during a pending overview: abort the read; no stale identity/data may
  reappear. Repeat operator→signed-out→analyst; analyst cannot submit work.
- Genuine invalid/expired bearer tokens must still receive backend401; do not
  suppress server enforcement or disguise errors with cached authenticated data.
- Backend JWT/seed/hash/CORS/session code is unchanged. No new auth credentials.

## M7/M8 read-only readiness — 2026-09-30

- Login accepts JSON `email`/`password`; TokenPair returns `access_token`,
  `refresh_token`, `token_type`, `identity` (not `token`). Both retained operator
  logins and normal browser RMS sign-in passed; the historical403 is not
  reproduced. No allowlist or authentication configuration was changed.
- Current census-list envelope is `tenant_id` + `records`, not `rows`;
  detail uses `record_id`, not the historical numeric `census_number` contract.
- Read-only test credentials are supplied through process environment variables
  `M7_READINESS_{RMS,DIGICOW}_{EMAIL,PASSWORD}` from the retained credential record.
  No registration, rotation, user-reset, or privileged business action is tested.
- The generic integration playbook is not a new Akki product ruling. Missing
  cookies, create-only seeding and a specific five-attempt lockout are not treated
  as M7/M8 acceptance failures absent an applicable requirement. Repeated failed
  logins without rate limiting remain a separately tracked hardening observation.