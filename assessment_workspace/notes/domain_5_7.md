# Domain 5.7 — Interface

Scope (instruction §5.7): five consoles · two day-zero dashboards · shaping
wizard · Trust Center · eight global rules · four response classes · visual
system fixed values · reference application's three lenses. Score the v6
prototype against Canon 5 properly here.

Inputs weighed:
- The v6 prototype (`/app/assessment_workspace/prototype/prototype.html` — 8 nav groups / 32 items / 4 tabs / 5 APPs).
- Executive-Core frontend (`Akki-Executive-Core/frontend/src/` — 597 files, 392 `.jsx`, incl. work_studio components, 5 protective-layer detectors, chat UI, HandoffActions).
- Core repos' thin frontends (RMS-IQ-Core-2 / Extraction-Akki have `frontend/` with 119/125 files — mostly demo/registry pages: `UseDataVerdictDemoPage.jsx`, `UseDataVerdictPanel.jsx`, `pages/registry/*`, `pages/use_data/*`, ui1c/d/e live-preview surfaces).

Every Canon-5 row classified.

## Rows classified in this domain

### Language of the surface (§2, §3, §9)

| Row | Capability | Class | Evidence (prototype / Executive-Core / core repos) |
|---|---|---|---|
| **C5-002 · C5-003** | Class chip inseparable from every claim | **BUILD** across all three inputs | prototype: no class chip pattern found by string search over `EVIDENCE_KINDS` (which classifies evidence *for* claims but not chip rendering per claim); Executive-Core: `frontend/src/components/work_studio/overlay/DocumentOverlay.jsx` has "citation chips" via `_archived/e4_doc_routes/components/reading/CitationChip.jsx` (archived); Core repos: `frontend/src/pages/use_data/UseDataVerdictPanel.jsx` has verdict-panel rendering. **NO single chip component in the same shape across the three.** |
| **C5-004** | Grounding marker walks the proof | **BUILD** (partial in Executive-Core) | Executive-Core `frontend/src/components/work_studio/overlay/SignalsPanel.jsx` + `RelatedDocuments.jsx` — proof-walk pattern exists but not as a standalone marker component |
| **C5-005 · C5-006 · C5-007** | Refusal card verbatim copy: "Not to the standard you asked for" / "Accept as recorded statement · Narrow the objective · Lower the standard" / "A refusal is the system keeping its promise" | **BUILD** (verbatim string not found) | Chunk 1 §3.5 flagged this; string search across prototype.html + all four repos returns no verbatim match. Refusal MACHINERY exists (Canon 3/5 refusal envelope + refusal_family_classifier), but the specific Canon-5 §3.1 fixed copy is unshipped. |
| **C5-008** | Agent-assumed chip (amber, scope resolvable inline) | **BUILD** | not found by string search anywhere |
| **C5-009** | Dormant capability rendered UNLIT + "what would activate this" | **PARTIAL** | prototype's `RESTRICTED = {hrstuff, datashield, reasoningshield, accessshield}` renders sage/green (dormant-adjacent) but has no "what would activate" statement per screen |

### The Five Consoles (§10)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C5-010 · C5-011 · C5-012** | Five consoles: EXTRACTION · COMPLIANCE · INTEGRATION · ADMINISTRATION · WATCH | **BUILD (all five named)** | prototype uses a different taxonomy (WorkStudio/ThinkLab/Collab/Monitor/Trust/Registry/Build/3rd-Party) — see Chunk 1 §3 mapping. NO surface labelled "Extraction Console", "Compliance Console", "Integration Console", "Administration Console" in the prototype OR Executive-Core OR core-repo frontends. The Canon-5 five-console architecture is entirely BUILD from a naming/organisation standpoint even where sub-capabilities exist elsewhere. |

### Extraction Console (§12-§19)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C5-013** | Registry Dashboard — holdings + composition + unmeasured + dormant unlit | **PARTIAL** | prototype: `estate` (Registry > Data Estate); core repos: `frontend/src/pages/registry/*` — a registry surface exists but Canon 5 §12.1 four-quadrant shape is BUILD |
| **C5-014** | Model catalogue with MOAC scorecards | **BUILD** | prototype: `models` (Registry > Models) exists as nav; NO MOAC scorecard rendering anywhere; Chunk-2 flagged MOAC as BUILD |
| **C5-015 · C5-016** | Shaping Wizard 5-step + Freeze | REUSE (backend, wizard flow) / **PARTIAL** frontend | backend REUSE (5.6); frontend prototype has `openExtractWizard` — actual 5-step visual is BUILD |
| **C5-017** | Sampling first-class + throwaway unless promoted | REUSE (backend) / BUILD (surface) | " |
| **C5-018** | Batch Board with quarantined batches + resolution path | **BUILD (surface); backend HARVEST** | backend depends on batch_quarantine.py harvest (5.4); surface is BUILD |
| **C5-019** | Registry Administration source-connector flow | REUSE (backend) / **PARTIAL** surface | prototype: `connect` (Registry > Connect); Executive-Core has richer connectors |
| **C5-020** | Quality Observation — Critic Seam scorecard incl. stale calibration | **BUILD (surface); backend HARVEST** | depends on critic_pass harvest (5.4/5.5) |
| **C5-021** | Opportunity Briefs (advisory-throughout) | REUSE (backend) | prototype: `ideas` (Monitor > Ideas by Akki); backend at `services/opportunity_briefs/*` |

### Compliance Console (§20-§23)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C5-022** | Compliance Home — ceremony countdown + refusals feed + quarantines + deletions | **BUILD (as a single home)** | prototype's Trust Center exposes `rules, datashield, reasoningshield, accessshield` — different shape from Canon 5 §20; ceremony-countdown surface is BUILD |
| **C5-023** | Prove-one-run action | **BUILD** | infrastructure at 5.6 C3-047 |
| **C5-024** | Retention & Rights | **PARTIAL** | retention backend REUSE; surface BUILD |
| **C5-025 · C5-026** | Compliance Rulebook — every rule w/ automated-checks count; "rule on paper" surfaced | **PARTIAL** | prototype: `rules` (Trust Center > Manage Rules) exposes rule-change; the "rule on paper" flag surface is BUILD |

### Integration Console (§24-§27)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C5-027 · C5-028 · C5-029 · C5-030** | Register / First-call / Administer / Dual-actor scoping | **BUILD (5.7)** / REUSE (backend) | prototype: `appsnew, appsfrequent, appsconnected, appsrequests` — a browsable APP CATALOGUE, not Canon-5 §24-§27 Integration Console shape. The scoped-key issuance backend REUSE; the console shape BUILD |

### Administration Console (§29-§34)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C5-031 · C5-032 · C5-033 · C5-034 · C5-035 · C5-036** | Home + Change-a-Rule + What-I've-Changed + Roles & Rights + Counter-Sign Duties + Verification Runner | **BUILD (as one console)** | pieces exist across the prototype (`rules`) and Executive-Core (`admin_users.py`, MFA); Canon-5 six-panel Home is BUILD |

### Watch Console (§34-A)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C5-037 · C5-038 · C5-039 · C5-040 · C5-041** | Four panels: State / Record / Under-Watch / Decisions | **BUILD** | no surface labelled "Watch" in any input — confirmed at 5.8 |
| **C5-042** | Constitutional negatives (no thresholds / no mark placement / no profile internals / no mirage construction) | **BUILD** | " |

### Reference App (§36-§39)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C5-043 · C5-044** | Reference App registered as an application; DESIGNED not demo | **PARTIAL** | prototype's `chat` is a chat surface; Executive-Core has richer chat (`frontend/src/pages/chat/*` — chat surface is the closest match). Neither presents itself explicitly as "Reference App" |
| **C5-045 · C5-046 · C5-047 · C5-048** | Three lenses over one object: Answer / Reasoning / Raw trail | **BUILD** | prototype's chat renders conversation + per-conversation DataShield report; NO progressive-disclosure three-lens over one object. Executive-Core's `solva_v2` has narration + engines but no three-lens surface |
| **C5-049 · C5-050 · C5-051** | Answer card (evidence strip + honesty strip + actions); actions Break-it-down / Draft the memo / Walk the proof | **PARTIAL** | prototype exposes actions per screen but no unified Answer Card with all three strips |

### Pillars + Control Band (§40-§42)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C5-052** | Five pillars: LEAD · WORK · BUILD · 3RD PARTY · LEARN | **BUILD (Lead+Learn missing)** | prototype: Work / Build / 3rd Party Apps / Admin — no "Lead" or "Learn" |
| **C5-053** | Lead pillar apps include ThinkLab, Monitor, Pulse, News | **PARTIAL** — ThinkLab+Monitor present in prototype; **Pulse and News absent everywhere** |
| **C5-054** | Work pillar: Chat, Analyze, Documents | REUSE (prototype has all three under WorkStudio) |
| **C5-055** | Build pillar: Train, Studio, Extract | **PARTIAL** — Train/Extract in prototype; **Studio (Canon 5 §42 "designed, not sourced") entirely absent** across all inputs. Executive-Core has `work_studio` but that is a document-compilation wizard, NOT the Canon-5 §42 Studio (Chunk 2 Q7.2) |
| **C5-056** | 3rd Party pillar hosts registered external applications | REUSE | prototype `thirdparty` + Executive-Core admin surfaces |
| **C5-057** | Learn pillar hosts learning surfaces | **BUILD** | not present anywhere |
| **C5-058 · C5-059** | Control band: CONNECT · ESTATE MAP · RULEBOOK · ACCESS · WATCH — same across every session | **BUILD (partial)** | prototype: `connect, estate, rules` present (under Registry/Trust); ACCESS control-band item = access-shield in prototype (partial); WATCH entirely BUILD |
| **C5-060** | Studio DESIGNED not sourced | **BUILD** | as C5-055 |

### Shape of every surface (§43-§45)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C5-061** | Every surface reads from one record | REUSE-doctrine | ledger is the source; no private stores |
| **C5-062** | No override / no emergency / no bypass on any surface | REUSE-doctrine | no bypass path in any repo |
| **C5-063** | "Insufficient measurement" render (never zero / never asterisk) | **PARTIAL** | Mtafiti verdict + composition support the state; the render UNI-FORM across every surface is BUILD |
| **C5-064** | Absence-of-artefact as its own state | **PARTIAL** | same shape |
| **C5-065** | Standard components use same copy in every context | **BUILD (component library)** |

### What interfaces do NOT do (§46)

| Row | Capability | Class | Evidence |
|---|---|---|---|
| **C5-066 · C5-067 · C5-068 · C5-069 · C5-070** | No cross-authority interior / no bypass / no per-tenant personalisation / no claim without class chip / no unmeasured-as-measured | REUSE-doctrine | discipline in place across the invariant suite |

## Two Day-Zero dashboards

The two Day-Zero dashboards Canon 6 §4 names are (i) Registry Dashboard (Extraction Console) and (ii) Trust Center. Both partial:

- **Registry Dashboard**: REUSE (backend) + PARTIAL (surface) — mapped to prototype `estate`.
- **Trust Center**: REUSE (backend rules) + PARTIAL (surface) — mapped to prototype `rules`; ceremony countdown + refusals feed + Verification Runner integration is BUILD.

## Eight global rules

Canon 5 does not enumerate literally "eight global rules" — this phrase is a synthesis of §43-§46 shape-of-every-surface and §9-§10 language-of-the-surface fixed values. Mapped as REUSE-doctrine (C5-061 through C5-070) with the specific component-library items BUILD.

## Four response classes

- ANSWERED · HELD · REFUSED · REFUSED-with-honesty-shape (three refusal shapes per §3.2). Backend REUSE; surface envelope PARTIAL.

## Visual system fixed values

**BUILD as a shared library.** Currently: prototype uses its own tokens (sage/green for restricted), Executive-Core uses its own component library, core repos are demo-thin. A shared visual system does not exist.

## Domain 5.7 subtotals

- REUSE (backend contracts / doctrinal disciplines held): 12 rows
- PARTIAL (backend REUSE + surface BUILD): 13 rows
- BUILD (surface only): 25 rows
- REUSE-doctrine: 5 rows

**Overall: Canon 5's interface is the domain with the highest BUILD share** — most of the surface architecture is not shipped in Canon-5 shape anywhere; the prototype exposes SIMILAR capability under different naming/organisation.

## Prototype → Canon 5 mapping table

Verbatim from Chunk-1 `prototype_inventory.md` §3.3 with each row now given a class:

| Prototype key | Canon 5 anchor | Class |
|---|---|---|
| `chat` (WorkStudio > Chat) | §36 Reference App | PARTIAL |
| `analyze` | §40 Work > Analyze | PARTIAL |
| `documents` | §40 Work > Documents | PARTIAL |
| `tasks` | (no direct Canon 5 anchor) | BUILD-or-RETIRE — application territory |
| `clarity, strategy, hypothesis, perspective` (ThinkLab) | §40 Lead > ThinkLab (Canon 5 lists ThinkLab but not the four sub-tools) | BUILD (sub-tool naming) |
| `mentions, emails, projects` (Collab) | (no direct anchor) | BUILD-or-RETIRE |
| `hrstuff` (Collab > HR Stuff — RESTRICTED) | (no anchor) | RETIRE |
| `performance, signals, ideas` (Monitor) | §40 Lead > Monitor / Pulse | PARTIAL — `ideas` maps to §19 Opportunity Briefs |
| `rules` (Trust Center > Manage Rules) | §23 Compliance Rulebook | PARTIAL |
| `datashield, reasoningshield, accessshield` (Trust > *Shield) | (no direct anchor — Canon 5 §20-§23 uses different names) | BUILD (rename to Canon-5 taxonomy) |
| `estate` | §12.1 Registry Dashboard | PARTIAL |
| `models` | §12.2 Models catalogue | PARTIAL |
| `compute` | (no direct Canon 5 anchor) | BUILD-or-RETIRE |
| `connect` | §41 Control band Connect | PARTIAL |
| `train, agentbuild, extract, youragents` (Build) | §40 Build pillar | PARTIAL (Extract) + BUILD (Studio, Agents) |
| `appsnew, appsfrequent, appsconnected, appsrequests` | §24-§27 Integration Console | BUILD (reshape) |

## Absences observed vs Canon 5

- No "Lead" pillar as a labelled pillar (prototype has ThinkLab + Monitor but not under a "Lead" label).
- No "Learn" pillar anywhere.
- No "News", "Pulse" surfaces.
- No "Watch Console".
- No "Studio" per Canon 5 §42 (Executive-Core's work_studio is document-compilation, not application-composer — Chunk 2 §Claim 7 in `claims_verification.md`).
- No verbatim refusal-card copy anywhere.
- No unified three-lens Answer/Reasoning/Raw-trail surface.
- No horizontal Control Band with all five items (Connect / Estate Map / Rulebook / Access / Watch).
