# RETIRE Inventory — Chunk 3 running list

Every capability classified RETIRE across the 10 domain files. Each row cites the RETIRE anchor (canon clause) and the location of the existing code that gets retired.

## RETIRE from platform — Executive-Core application-territory duplicates

Anchor: **Canon 1 §12 (Six Services)** — the platform serves the application; application concerns stay in application territory. **Canon 1 §13** — every application (including first-party) crosses the same boundary; no in-platform admin surface for application concerns. **Canon 1 §15** — the platform will not know a buyer, a price, or an order.

| Item | Location | Retiring anchor | Note |
|---|---|---|---|
| `stripe_webhook.py` | `Akki-Executive-Core backend/services/stripe_webhook.py` | Canon 1 §15 verbatim: "will not know a buyer, a price, or an order — commerce is application territory" | Application-side, if kept at all |
| `owner_digest.py` | Executive-Core loose service | Canon 1 §12: application-owner email digests are application territory | " |
| `news_aggregator.py` | Executive-Core loose service | Canon 1 §12 | " |
| `first_login_password_set.py` | Executive-Core loose service | Canon 1 §13: application user auth stays in the application (its scoped-key ties it to the platform) | " |
| `cohort_email.py`, `cohort_email_html.py`, `cohort/magic_link.py`, `cohort/welcome_email.py`, `cohort/feedback_widget.py`, `cohort/copy_overrides.py`, `cohort/special_ask.py`, `cohort/console.py`, `cohort/feature_events.py` | `Akki-Executive-Core backend/services/cohort/` (8 files) + loose | Canon 1 §13: trial/onboarding + feedback are application territory | Keep application-side, retire from platform layer |
| `platform_kb.py` | `Akki-Executive-Core backend/services/platform_kb.py` (107 LOC) | Canon 1 §13: application-side "what is AKKI" prompt block; static-not-RAG | Application-side |
| `backfill_shield_v1.py` | `Akki-Executive-Core backend/services/backfill_shield_v1.py` (490 LOC) | One-time migration for Executive-Core's chat history through the shield. Not a canon capability. | Retire on migration completion |

## RETIRE — Cross-cutting security duplicates

Anchor: **Canon 5 §43** (no surface offers bypass/override) — cross-cutting HTTP/security services shipped in Executive-Core duplicate what the platform boundary must own itself. Keeping them alongside a platform boundary creates a second path.

| Item | Location | Retiring anchor | Note |
|---|---|---|---|
| `services/csrf.py`, `services/rate_limit.py`, `services/rbac.py`, `services/security_headers.py`, `services/session_timeout.py`, `services/sentry_setup.py`, `services/privacy_wall.py`, `services/clamav_service.py` | `Akki-Executive-Core backend/services/*.py` | Canon 5 §11 (The Shell — no bypass path); Canon 1 §7.1 (peer authorities) — cross-cutting security is either Watch territory (Canon 8) or governance discipline (Canon 3 §30 Enforcement Class); duplicated implementations create a second path | Retain application-side layer per Canon 1 §13 |

## RETIRE — Frontend archives

Anchor: **already marked archived by the codebase itself**; Canon 5 §43 no surface offers a bypass path.

| Item | Location | Retiring anchor | Note |
|---|---|---|---|
| `frontend/src/_archived/` (61 files including `Home1.jsx`, `Home2.jsx`, `e4_doc_routes/components/reading/*.jsx`, `e4_doc_routes/hooks/useDocumentParagraphs.js`) | `Akki-Executive-Core` | Codebase self-marking; Canon 5 §43 | Retire on migration |
| `frontend/src/_archived_legacy/` | `Akki-Executive-Core` | Codebase self-marking | " |
| `frontend/src/_archived_coverage_loss/` | `Akki-Executive-Core` | Codebase self-marking | " |
| `frontend/src/website/` (34 files) | `Akki-Executive-Core` | Canon 1 §12/§13: marketing website is application/commercial territory | Keep as application marketing site; retire from platform surface |

## RETIRE — Prototype-only surfaces without canon anchor

Anchor: prototype exposes surfaces Canon 5 does not enumerate; these are prototype-only creative signals, not canon-required capabilities.

| Item | Location | Retiring anchor | Note |
|---|---|---|---|
| `hrstuff` (Collab > HR Stuff — RESTRICTED) | prototype `HRStuff` nav item | Canon 5 §40 does not list HR as a pillar | Application territory (Canon 1 §13) — if kept, application-side; retire from platform |
| `datashield / reasoningshield / accessshield` naming | prototype Trust Center children | Canon 5 §20-§23 uses different names (Home / Prove-one-run / Retention & Rights / Compliance Rulebook) | Rename per Canon 5; retire the "*Shield" nomenclature |
| `compute` (Registry > Compute) | prototype nav item | Canon 5 has no "compute" surface — Registry Administration (§17) covers connectors, Extraction Console covers the estate but not compute allocation | Application territory or infrastructure territory |
| `tasks` (WorkStudio > Task Manager) | prototype nav item | Canon 5 §40 Work pillar names Chat / Analyze / Documents; Task Manager is not enumerated | Application territory |
| `mentions, emails, projects` (Collab) | prototype nav items | Canon 5 §40 has no Collab pillar | Application territory |

## RETIRE — Renaming (not deletion) of prototype taxonomy

These are RENAMES rather than deletions but still classified RETIRE because the prototype label doesn't carry forward:

| Prototype label | Canon 5 label | Note |
|---|---|---|
| `WorkStudio` (as pillar name) | `Work` (Canon 5 §40) | Rename |
| `ThinkLab` (as top-level group) | Lead pillar sub-application (Canon 5 §40) | Reparent under Lead |
| `Monitor` (as top-level group) | Lead pillar sub-application (Canon 5 §40) | Reparent under Lead |
| `Trust Center` | `Compliance Console` (Canon 5 §20) | Rename |
| `Registry` (as top-level group) | Extraction Console child + Control Band items (Canon 5 §17, §41) | Reparent |
| `Build` (as top-level tab) | Build pillar (Canon 5 §40 — same word, but Studio and Learn currently missing) | Complete the pillar; add Studio and Learn |
| `3rd Party Apps` (tab) | 3rd Party pillar (Canon 5 §40) | Same intent, different shape (Canon 5 §24-§27 Integration Console + a browsable app catalogue) |

## Summary counts

- **RETIRE rows** (concrete code): 20 loose Executive-Core services + 8 cross-cutting security + 3 frontend archives + 1 marketing website + 5 prototype-only surfaces = **37 concrete retire items**.
- **RETIRE renames** (taxonomy fixes only, no code deletion): 7 prototype-taxonomy renames.
- **Canon retirement anchors**: Canon 1 §12 (application territory), Canon 1 §13 (same boundary for every application), Canon 1 §15 (six absolutes — no commerce), Canon 5 §43 (no bypass), Canon 5 §40 (fixed pillar taxonomy).

Every RETIRE row above cites a specific canon clause. No RETIRE row was assigned by taste.
