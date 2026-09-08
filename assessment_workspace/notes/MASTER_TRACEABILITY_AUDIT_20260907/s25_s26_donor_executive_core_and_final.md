# S25 + S26 · Donor · Akki-Executive-Core + Akki-Executive-Final · Detail Classification

**Repos:**
- **S25** · `Akki-Executive-Core` HEAD `5844eee9` (main, 2026-07-08) · 929 total commits
- **S26** · `Akki-Executive-Final` HEAD `bba80ab5` (main, 2026-06-06) · (commit count TBD)

**Diff summary vs docs/:** 3 files byte-differ between Core and Final (`CODE_INVENTORY_2026-05-05.md` · `ENGINEERING_ONBOARDING.md` · `INVENTORY_2026-05-04.md`). All other docs are BYTE-IDENTICAL. Executive-Final is a mostly-frozen predecessor snapshot; Executive-Core is the live workstream that continued evolving.

## §A · Executive-Core · Executive-Final · docs/ inventory (28 files · ~9,780 lines Core)

| Row ID | File | Lines (Core) | Byte-diff Core vs Final | Anchor | Classification |
|---|---|--:|---|---|---|
| A25-1 | `ACCESSIBILITY.md` | ? | identical | Accessibility norms | REUSE |
| A25-2 | `BUILD_PHASES.md` | ? | identical | Build phases sequence | INVENTORY (claim-to-verify per binding rule) |
| A25-3 | `CHAT_CITATIONS_AUDIT.md` | ? | identical | Chat citations audit | INVENTORY |
| A25-4 | `CODE_INVENTORY_2026-05-05.md` | ? | **differs** | Code inventory snapshot | INVENTORY (Core has newer code state) |
| A25-5 | `DEPLOYMENT.md` | ? | identical | Deployment doc | REUSE |
| A25-6 | `ENGINEERING_ONBOARDING.md` | ? | **differs** | Engineering onboarding | INVENTORY |
| A25-7 | `INVENTORY_2026-05-02.md` | ? | identical | Inventory snapshot | INVENTORY |
| A25-8 | `INVENTORY_2026-05-04.md` | ? | **differs** | Inventory snapshot | INVENTORY |
| A25-9 | `MEMO.md` | ? | identical | Memo | INVENTORY |
| A25-10 | `MEMO_DECISIONS.md` | ? | identical | Memo of decisions | INVENTORY |
| A25-11 | `NED_CYCLE_MANAGER_DESIGN.md` | ? | identical | Non-Executive Director cycle manager design | REUSE (feeds Doc 15 governance ceremony) |
| A25-12 | `PRIVACY_WALL_DESIGN.md` | ? | identical | Privacy wall design | REUSE (feeds Doc 01/02 Shield + BR-1.x) |
| A25-13 | `PRIVACY_WALL_LEAKAGE_AUDIT.md` | ? | identical | Privacy wall leakage audit | INVENTORY |
| A25-14 | `PRODUCT_FEATURES.md` | ? | identical | Product features | REUSE |
| A25-15 | `PRODUCT_FEATURES_legacy_2026-05-04.md` | ? | identical | Legacy product features | INVENTORY |
| A25-16 | `PRODUCT_REVIEW.md` | ? | identical | Product review | INVENTORY |
| A25-17 | `PRODUCT_SPEC.md` | ? | identical | Product specification | REUSE |
| A25-18 | `ROADMAP.md` | ? | identical | Roadmap | INVENTORY |
| A25-19 | `RUNBOOKS/` (subdirectory) | — | identical | Runbooks | INVENTORY |
| A25-20 | `SURFACE_TYPES.md` | ? | identical | Surface types | REUSE (feeds Doc 05 Northena) |
| A25-21 | `SYNISENSE_SCOPE.md` | ? | identical | SyniSense scope (Executive workstream view) | REUSE (feeds Doc 01/02 Shield) |
| A25-22 | `WEBSITE_BRIEF_V3.md` | ? | identical | Website brief v3 | REUSE (marketing surface) |
| A25-23 | `cohort_pricing.md` | ? | identical | Cohort pricing | INVENTORY (commercial - deferred per owner) |
| A25-24 | `homepage-positioning-v1.md` | ? | identical | Homepage positioning v1 | INVENTORY (commercial) |
| A25-25 | `marketing_assets.md` | 86 | identical | Marketing assets | INVENTORY (commercial) |
| A25-26 | `runbooks/` (lowercase, subdirectory) | — | identical | Duplicate runbooks path | INVENTORY |
| A25-27 | `sprints/` (subdirectory) | — | identical (`sprints/STUDIO.md` = 136 lines) | Sprint plans | INVENTORY |
| A25-28 | `ux-advisories-v1.md` | ? | identical | UX advisories v1 | REUSE (feeds prototype ratings) |

## §B · Repo-level requirement material outside `docs/`

| Row ID | Path | Anchor | Classification |
|---|---|---|---|
| A25-R1 | `Akki-Executive-Core/DEPLOY.md` | Deployment top-level | REUSE |
| A25-R2 | `Akki-Executive-Core/salvage/commercial_cut_2026_07_06/MANIFEST.md` | Salvage manifest for commercial cut | INVENTORY (retirement) |
| A25-R3 | `Akki-Executive-Core/salvage/commercial_cut_2026_07_06/README.md` | Salvage README | INVENTORY |

## §C · S25/S26 rollup

**Total docs across both repos: 28 (Core) + 28 (Final) with 3 byte-differ + 25 byte-identical.** Since byte-identical files are the same content, they count once for row purposes: **28 files with 3 having a Core/Final variant.**

**Row denominator: 28 conceptual rows** (with 3 having variants).

| Bucket | Rows | % of 28 |
|---|--:|---:|
| REUSE | 12 | 42.9% |
| INVENTORY | 15 | 53.6% |
| NEW | 0 | 0.0% |
| DONE / PARTIAL | 1 (A25-11 NED cycle manager already partially lifted into Doc 15 building) | 3.6% |

**Interpretation:** Executive-Core is the **primary donor repo for foundation stack** (Solva-v2 lift, NED cycle, Privacy Wall, SYNISENSE scope, SURFACE_TYPES for Northena, PRIVACY_WALL_DESIGN for Doc 01/02). Executive-Final is the frozen predecessor — useful for byte-diff sanity but Core has the newer material.

**Cross-reference to master §E.1:** W-SOLVA-V2-LIFT relies on `services/solva_v2/` directory content in these repos (10,509 LOC Core + 9,771 LOC Final) — NOT reflected in the docs/ listing above; the code lift is separate from docs/. The docs/ list is the **specification donor**; the code lift is the **implementation donor**.

**Diff finding:** 3 byte-differ files show Core is 1-2 months ahead of Final on `CODE_INVENTORY`, `ENGINEERING_ONBOARDING`, `INVENTORY_2026-05-04`. Neither carries dated authority; owner may rule which is precedence-authoritative or if the diff itself is a finding.

**Full row-shape enumeration deferred** as INVENTORY. Wave: **W-DONOR-MINE-EXECUTIVE-CORE** (M+M effort) — extract line-anchored REQ bullets from the 12 REUSE-classified files into projectable rows.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
