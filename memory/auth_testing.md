# auth_testing.md

**Auth model on the spine surface (`https://akki-reuse-assess.preview.emergentagent.com`):**

- **Type:** bearer-token, no cookies, no sessions, no CSRF class.
- **Frontend flow:** owner pastes token into the "OWNER ACCESS" card → saved to `localStorage.owner_token` → every axios call includes header `Authorization: Bearer <token>`.
- **Backend gate:** `/api/connect/*` routes carry FastAPI dependency `Depends(require_owner)` from `/app/backend/spine_auth.py`. Non-bearer → 401. Bad-bearer → 403. Bearer + malformed payload → 422. Bearer + good payload → 200 + pipeline fires.
- **Rate limit:** in-memory per-IP sliding window: **30 requests / 60 s** on `/api/connect/*`. Exceeded → 429.
- **Rotation:** delete `/app/backend/.owner_credentials`, `sudo supervisorctl restart backend`, new token generated on startup.

**What is NOT auth on this surface:**
- No password DB. No user accounts. No signup. No email/password login. No OAuth. No SSO.
- No Rafay console credential is stored, echoed, or verified here. Standing owner policy: no external-console credential enters this workspace.
- No JWT signing / rotation — the token is a static shared secret, one owner, one pod.

**Test scenarios worth exercising (read-only):**
- Unauthed load of `/register/connect/gpu` → login card renders.
- Bad-token paste → localStorage saves it → axios sends it → API returns 401/403 (frontend surfaces error) → owner has to sign out and try again.
- Good token → tile grid + detail card render in fixture grammar.
- Sign out button clears `localStorage.owner_token` and returns to login card.

**Test scenarios to avoid (would fire the pipeline):**
- Submitting the Connect · GPU form. Only the owner submits, and only once, with real vendor credentials.

**Endpoints protected by `require_owner`:**
- `POST /api/connect/gpu`

**Endpoints unauthenticated (deliverables API):**
- `GET /api/deliverables`
- `GET /api/deliverables/{name}` (allowlisted: `BUILD_STRATEGY.md`, `REUSE_ASSESSMENT.md`)
- `GET /api/` (hello world)
- `GET /api/status`
- `POST /api/status`
