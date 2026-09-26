# Existing JWT consumer regression — 2026-09-26

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