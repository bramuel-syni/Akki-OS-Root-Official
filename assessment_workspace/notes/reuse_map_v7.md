# Reuse Map · v7 surfaces + backend mechanisms across the 5 repos

Owner Order 2026-08-19 · FL-P2-27 · Sprint deliverable §1.

## Access status

| Repo | URL | Access | Pinned SHA | Last commit |
|---|---|---|---|---|
| RMS-IQ-Core-2 | `github.com/bramuel-syni/RMS-IQ-Core-2` | ✅ public | `ea5aa01` | 2026-08-01 |
| Akki-OS-V1 | `github.com/bramuel-syni/Akki-OS-V1` | ✅ public | `8c36190` | 2026-08-14 |
| Extraction-Akki | `github.com/bramuel-syni/Extraction-Akki` | ✅ public · **target** | `0709be7` (programme/track-a) | 2026-08-25 |
| Akki-Executive-Core | `github.com/bramuel-syni/Akki-Executive-Core` | ✅ public | `5844eee` | 2026-07-08 |
| **Akki-Executive-Final** | `github.com/bramuel-syni/Akki-Executive-Final` | ❌ **HTTP 404 · private or non-existent at that URL** | — | — |

**Blocking finding: `Akki-Executive-Final` cannot be reached from the pod.** `curl -sI https://github.com/bramuel-syni/Akki-Executive-Final` returns `HTTP/2 404`. The GitHub API returns 404 too, whereas `Akki-Executive-Core` returns 200 under the same account. Either the repo is private (needs an access token dropped into the pod) or the URL differs. Owner disposition needed: (a) confirm the URL, or (b) grant access. Sprint proceeds against the four accessible repos; if Executive-Final holds v7-aligned components as the owner suggests ("could have elements you can reuse"), the sprint's reuse grades will improve once access lands.

## Reuse-grade legend

- **LIFT** — copy the file/module as-is; small path/import tweaks only.
- **ADAPT** — a component or service exists but needs shaping (rename, wire to real facts endpoint, replace demo data with real records, or trim to v7 nav).
- **REBUILD** — nothing directly usable in the repos; must be built fresh (tests-first) against the v7 oracle + 17-doc requirements.

## §1 · Frontend fabric reuse map (v7 constants → repo components)

Every row below names a v7 constant/surface (from `notes/prototype_inventory_v7.md`), the repo file/module that could back it, and the reuse grade.

| v7 surface | v7 constant | Best repo path | Grade | Notes |
|---|---|---|---|---|
| Registry (3 tabs) | `CHARTS`, `EST_GROUPS`, `BRIEF`, `BRIEF_SUB` (estate slice) | `Extraction-Akki/pod_shell/frontend/src/components/Registry.jsx` (built this cycle) + `RMS-IQ-Core-2/frontend/src/pages/registry/` | **LIFT** (built) · **ADAPT** (RMS registry pages carry composition-by-language, condition, rights-class charts already) | Registry-A4 already lives. RMS pages carry chart shapes that match v7 CHARTS. |
| Connect wizard (v7 5-stage) | `CONNECT_KINDS`, `CONNECT_CHIPS`, `CONNECT_STAGES`, `WIZ` | `Extraction-Akki/pod_shell/frontend/src/components/ConnectWizard.jsx` (paste panel, current) + `Akki-Executive-Core/frontend/src/components/chat/` (drawer + streaming chat) | **ADAPT** — T12 rework: single-panel → right-side drawer chat that assists paste-and-connect | See wave W1 in §status_and_wave_plan. Owner ruled T12 explicitly. |
| Shield · Data / Reasoning / Access | `TRUST`, `GOV`, `RB_CATS`, `RULES_IN_FORCE`, `RAILS` | `RMS-IQ-Core-2/backend/services/synisense/shield/` (mechanism) + `Akki-Executive-Core/frontend/src/components/synisense/` + `.../governance/` (surface) | **ADAPT** — surface exists; must be re-tabbed to v7's four-questions grammar and bound to real gate telemetry | Data Shield ~ masked-crossing gate (Doc 1); Reasoning Shield ~ evidence gate (Doc 4); Access Shield ~ seat matrix (Doc 15). Governance surface reusable. |
| Grey Mirror / Watch | `GM`, `PATTERNS`, `WALKS[bait]` | `RMS-IQ-Core-2/backend/services/synisense/shield/` (partial), `Akki-Executive-Core/frontend/src/components/synisense/` | **REBUILD** — no full Grey Mirror mechanism exists. Some watch primitives in shield service. | Doc 3 (Intent & Security Monitoring) mechanism must land before any Grey Mirror surface. |
| Rules Updates ceremony | `WIZ[rulebook]`, `RB_CATS`, `RULES_IN_FORCE` | `Akki-Executive-Core/frontend/src/components/governance/` | **ADAPT** — governance surface exists; ceremony wizard must be built to v7 grammar. | Doc 15 rule-book update ceremony. |
| Model Admission ceremony | `WIZ[actor]` (model kind), acceptance criteria | `Akki-Executive-Core/backend/services/sandbox_generation.py` + `.../analysis_lifecycle.py` + `.../monitor/` | **ADAPT** — sandbox + monitor primitives exist; ceremony surface not built. | Doc 13 six-criterion acceptance. CA1-011 amendment (standing re-check date). |
| Board 360 / Exco 360 | new v7 constants (PAGE_TOPLINE + monitor group) | `Akki-Executive-Core/frontend/src/website/pages/Exco360.jsx`, `Exco360Voice.jsx` | **ADAPT** — marketing/website surface exists; must be re-wired into the app shell with real records from Docs 13/14/15 mechanisms | CA1-A1 + CA1-A2. |
| Documents suite | v7 `NAV.workstudio.documents` | `Akki-Executive-Core/frontend/src/pages/DocumentsPage.jsx` + `.../components/documents/` + backend `.../services/documents/` + deck-* modules | **LIFT** (with adapter) — full documents pipeline including deck generation, lineage, retrieval already built | CA1-A3. |
| Chat / Analyze / ThinkLab | v7 `NAV.workstudio.{chat,analyze}`, `NAV.thinklab.*` | `Akki-Executive-Core/frontend/src/components/chat/`, `.../components/analyze/`, `.../components/thinklab/`, `.../pages/Chat.jsx`, `AnalyzeJournal.jsx`, `.../services/chat/`, `.../services/analyze_workspace/` | **LIFT** — surfaces + backends exist for the primary Work-tab destinations | These are ~40% of v7's nav destinations. |
| Cohort / Collab | v7 `NAV.collab.*` | `Akki-Executive-Core/frontend/src/components/cohort/`, `.../components/collab/`, `.../services/cohort/`, `.../services/inbox_routing/` | **LIFT** | CA1-A5. |
| Ideas / Signals | v7 `NAV.monitor` sub-nav (P360_SUBS: performance/signals/ideas) | `Akki-Executive-Core/backend/services/ideas_engine/` + `.../signal_dedup.py` | **ADAPT** — service exists; UI wire is Exco360 sub-nav | — |
| Trace / Walk this → | `WALKS`, "Walk this →" affordance | `Akki-Executive-Core/frontend/src/components/trace/`, `.../components/walkin/` | **ADAPT** — walk primitives exist; T8 custody scope must resolve before shipping | See notes/t8_walk_this_scope.md. |
| Highlights / Pulse | `BRIEF` two-page reads | `Akki-Executive-Core/frontend/src/components/highlights/`, `.../pulse/`, `.../pages/Pulse.jsx` | **LIFT** | Directly maps to v7's per-surface highlight cards. |
| Trust surface / Trust Center | `TRUST`, `FQ_TOPLINE.wstate` | `Akki-Executive-Core/frontend/src/components/trust/`, `.../components/synisense/` | **ADAPT** | Was `trust` group in v6; folded into `estate` in v7. |
| Onboarding / Origin | `WIZ[actor]` (person kind) | `Akki-Executive-Core/frontend/src/components/onboarding/`, `.../components/origin/`, `.../pages/InviteAccept.jsx`, `FirstSession.jsx` | **ADAPT** — full onboarding exists; must be reframed to v7's actor-declaration ceremony | — |
| Tasks / Task Manager | v7 `NAV.workstudio.tasks` | `Akki-Executive-Core/frontend/src/components/tasks/` (referenced via `services/tasks/`) | **LIFT** | CA1-A7 hand-off contract (CA1-009) must be added on top. |
| Approvals · Spend Requests | new v7 surface | `Akki-Executive-Core/frontend/src/pages/RespondToChecklist.jsx` + `.../components/cycle/` (approval flow primitives) | **ADAPT** | CA1-A6. Auto-approve ceiling per CA1-A6-q1. |
| Auth / Session / RBAC | ambient (v7 shows static personas) | `Akki-Executive-Core/backend/services/rbac.py`, `csrf.py`, `session_timeout.py`, `first_login_password_set.py` + `Extraction-Akki/backend/services/ip_allowlist/` | **REBUILD (blended)** — track-B auth still deferred. IP-allowlist stays; RBAC lifts when track-B unfreezes. | FL-P2-08 CLOSED (owner-token retired); RBAC untouched. |

**Layout / shell primitives:**

| Element | v7 | Best repo path | Grade |
|---|---|---|---|
| App shell (top tabs + role switcher + nav groups) | `TABS`, `NAV`, `ROLES` header | `Akki-Executive-Core/frontend/src/components/shell/`, `.../components/layout/` | **ADAPT** — full shell + layout primitives exist |
| Two-column band (fluid left + 300px right context) | fixture page pattern §2 | Registry.jsx (built) | **LIFT** — reuse `TwoColBand`, `Divider`, `SectionTitle`, `StatGrid`, `Headliner`, `VisualBars`, `ContextPanel`, `Chip` from the Registry we shipped |
| Detail card (KV grid + close) | v7 detail cards | Registry.jsx (built) | **LIFT** — reuse `KV`, `FQ`, `ComputeDetailCard`, `DataSourceDetailCard` patterns |
| Hatched-bar / drawn-not-blank | `CHARTS` HATCH sentinel | Registry.jsx (built) | **LIFT** |

## §2 · Backend mechanism reuse map (17-doc requirements → repo services)

| 17-doc requirement class | Best repo module | Grade | Wave (see §3) |
|---|---|---|---|
| Doc 1 · Chokepoint (masked crossings, single exit gate, receipts) | `RMS-IQ-Core-2/backend/services/synisense/shield/` (masking primitives) + `Akki-Executive-Core/backend/services/privacy_wall.py` | **ADAPT** | W3 |
| Doc 2 · DPO declaration + two-item dual-file custody | `RMS-IQ-Core-2/backend/services/compliance/`, `.../data_source/` | **ADAPT** | W3 |
| Doc 3 · Intent + Security Monitoring (Watch/Grey Mirror) | `RMS-IQ-Core-2/backend/services/synisense/` (partial) | **REBUILD** — mechanism missing | W6 |
| Doc 4 · Reasoning, Grounding, Solver (Solva) | `Akki-OS-V1/backend/services/solva_depth/`, `Akki-Executive-Core/backend/services/solva_v2/` | **ADAPT** | W5 |
| Doc 5 · Direction / Scope / Focus Pt 1 (Northena) | `RMS-IQ-Core-2/backend/services/northena/` + `Akki-OS-V1/.../northena/` | **ADAPT** | W4 |
| Doc 6 · Progressive Disclosure (minimal-sufficient) | `Akki-Executive-Core/backend/services/analyze_workspace/` context selection primitives | **ADAPT** | W5 |
| Doc 7 · Five-ring unit (shrinkage) | `RMS-IQ-Core-2/backend/services/perception/` + `.../layer_a,b,c/` | **ADAPT** | W5 |
| Doc 8 · Warm/fresh fork (memory & retrieval) | `Akki-Executive-Core/backend/services/platform_kb.py` + `.../continue_chat.py` | **ADAPT** | W5 |
| Doc 9 · Connection + census | **Extraction-Akki `services/connect_estate/`, `services/connect/`, `services/data_source/` + `services/registry_facts/`** | **LIFT** — this cycle | W1/W2 (built) |
| Doc 10 · Comprehensive Registry + Opportunity Briefs | `Extraction-Akki/services/registry_facts/` (partial) + `RMS-IQ-Core-2/backend/services/opportunity_briefs/` | **ADAPT** | W2 |
| Doc 11 · Cost ladder + deflation law | `RMS-IQ-Core-2/backend/services/economics/` (tier_lock.v*.json + cost lever config) + `Akki-Executive-Core/backend/services/rate_limit.py` | **ADAPT** — rich economics data present | W6 (Cost Ledger surface = CA1-008) |
| Doc 12 · In-perimeter execution + reflection-before-commit | `Extraction-Akki/services/compute_seam/`, `services/connect_gpu/` (built) + `Akki-Executive-Core/backend/services/job_queue.py` | **ADAPT** | W2 (compute connected) built |
| Doc 13 · Autonomous training (Targeta) | `RMS-IQ-Core-2/backend/services/targeta/` + `Akki-Executive-Core/backend/services/sandbox_generation.py` | **ADAPT** | W7 (Model Admission) |
| Doc 14 · Model ecosystem + baseline curation + white paper | `Akki-Executive-Core/backend/services/analysis_lifecycle.py` + `.../deck_*.py` | **ADAPT** | W7 |
| Doc 15 · Platform Orchestration + Governance Ceremony | `Akki-Executive-Core/backend/services/monitor/`, `.../cycle_lifecycle.py`, `.../cycle_permissions.py` + `RMS-IQ-Core-2/backend/services/master_admin/` | **ADAPT** | W8 (Rules Updates ceremony) |
| Doc 16 · Cross-cutting orchestration | `Akki-Executive-Core/backend/services/inbox_routing/` + `.../work_studio/` | **ADAPT** | W9 |
| CA1-N1 · Retention enforcement | `RMS-IQ-Core-2/backend/services/retention/` (declarative present, enforcement missing) | **ADAPT** | W6 |
| CA1-N2 · Breach notification | none | **REBUILD** | W8 |
| CA1-N3 · Individual access & erasure | none | **REBUILD** | W8 |
| CA1-N4 · Residency enforcement | region tag exists on data-source records; enforcement missing | **ADAPT** | W3 |
| CA1-N5 · Ledger continuity | none | **REBUILD** | W9 |

## §3 · Top reuse highlights

**High-reuse (LIFT) wins:**
1. **Akki-Executive-Core `frontend/src/components/{documents,chat,analyze,cohort,collab,thinklab,trace,walkin,shell,layout,highlights,pulse}/`** — the full v7 Work + Build surface fabric, largely LIFT-able onto the estate.
2. **Akki-Executive-Core `backend/services/{documents,chat,analyze_workspace,cohort,ideas_engine,monitor,sandbox_generation,solva_v2,platform_kb,job_queue,inbox_routing,work_studio}/`** — the mechanisms behind those surfaces.
3. **RMS-IQ-Core-2 `backend/services/{northena,mtafiti,targeta,perception,solva_depth,outer_gate,synisense,retention,economics,opportunity_briefs,layer_a/b/c,census_dimensions}/`** — the direction/reasoning/training/economics kernel already exists.
4. **Extraction-Akki `pod_shell/frontend/src/components/{Registry.jsx,ConnectWizard.jsx}` + `backend/services/{registry_facts,connect,connect_estate,credentials_paste,estate_keys,ip_allowlist,data_source}/`** — the connect + registry surfaces we just shipped, already binding real records.
5. **RMS-IQ-Core-2 `frontend/src/pages/registry/`** — v6-era Registry pages that carry the exact chart shapes v7 wants (composition-by-language, rights-class, condition), plus the `EngineCard`, `LedgerTable`, `ClassBadge`, `RefusalCard`, `RetentionPostureBadge`, `TrustReceiptLink` primitives.

**Blockers requiring REBUILD (nothing to lift):**
- Doc 3 Grey Mirror / Watch mechanism (bait, containment ladder, self-check drill, external witness). Some Shield primitives exist but the Grey Mirror surface's supporting mechanism is missing.
- CA1-N2 breach notification path.
- CA1-N3 individual access & erasure.
- CA1-N5 ledger continuity + RTO attestation.

## §4 · Executive-Final honest gap

Owner note said "could have elements you can reuse to avoid redoing." If Executive-Final holds:
- v7-aligned react components (FOURQ/GM/GOV/EST_GROUPS/WALKS in tsx/jsx form)
- backend Watch/Grey Mirror mechanism (Doc 3)
- N-series primitives (retention enforce, breach notification, erasure)

… the sprint's REBUILD count drops and W6/W8 shrink materially. Until Executive-Final is accessible, the wave sizes in `notes/status_and_wave_plan.md` reflect worst-case with the four accessible repos.
