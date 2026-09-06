# Doc 0 Part 2 vs Live Build · Delta Table

**Authored:** 2026-09-06T~17:40Z  
**Source of live build claims:** STATE/DECISIONS.md (append-only ratchet history, 45 entries at commit fd55c7b), STATE/NEXT.md, STATE/BUILD_JOURNAL (Extraction-Akki repo), current ratchet floor **2978**, and Doc 0 Part 2 (component registry with per-BR statuses).

**Discipline:** every row cites the Doc 0 status verbatim ("Met" / "Partial" / "Not Met" / "Not confirmed"), then the observed programme state, then the delta ("Doc 0 stale" · "Doc 0 accurate" · "Programme lacks" · "Programme has more than Doc 0 credits"). No inferences — where the programme has not built the specific object, that is stated.

## §A · Aggregate

- **16 components** in Doc 0 Part 2
- **36 BR-x.y** build requirements
- Doc 0 tallies per its own statuses: Met 16 · Partial 9 · Not Met 4 · Not confirmed 7 (per direct count of the "STATUS" strings in doc0_governance_architecture.txt)
- **Programme evidence anchor: ratchet floor 2978** (invariants held under `BASELINE_GUARD=1` in Extraction-Akki `backend/tests/invariants/`, 2978 passing tests)

## §B · Per-BR delta

| BR | Requirement (short) | Doc 0 STATUS | Live-build reality (with anchor) | DELTA |
|---|---|---|---|---|
| **1 · SyniSense (Shield)** | | | | |
| BR-1.1 | Every code path to external model client routes through single chokepoint (negative-scan build test) | Met — A5.1 | **Consistent with programme.** Chokepoint is Extraction-Akki's `backend/services/chokepoint/` (single-crossing enforcement); negative-scan invariants live in `tests/invariants/` under the current 2978 ratchet. Programme has NOT rebuilt the chokepoint per Doc 0 — the shield_train wave is a downstream user of the chokepoint pattern. | **Doc 0 accurate.** |
| BR-1.2 | Chokepoint policy in configuration a subject cannot alter at runtime; integrity verified at load | Partial — build-time only; runtime integrity unspecified | **No runtime integrity check observed in programme.** Extraction-Akki's `masking_policy.v0.json` (just amended in W-SMS-Body-Emit) IS a governed config artefact but does NOT have a load-time signature/hash check against the Rule Registry. | **Doc 0 accurate; programme lacks runtime integrity check (G-6 dep).** |
| BR-1.3 | Trust receipt schema carries invoking-principal identity + reliable timestamp | Not Met — A5.7 omits both | **Programme confirms.** Trust receipts observed in programme (e.g., shield_train receipts under `phase0/shield_train_receipts/`) do NOT carry a first-class `invoking_principal_id` or reliable-time-source timestamp — they carry ISO datetimes from `datetime.now(UTC)` per instance. FPT_STM.1 reliable-time control does not exist. | **Doc 0 accurate; G-8 open.** |
| BR-1.4 | Every asset passing crossing carries typed custody classification | Partial — distinguished in practice but not typed queryable attribute | **Programme confirms.** In shield_train the "custody class" is a categorical tag (e.g., `class: pii-direct` in the ledger) but is not exposed via a queryable interface across all subsystems; each subsystem re-derives from the JSON. | **Doc 0 accurate; G-3 open.** |
| BR-1.5 | Chokepoint fails closed on any internal error | Met — consistent with A5.6 structural-impossibility | **Consistent with programme.** Extraction-Akki row_executor + chokepoint pattern refuses-by-construction. Not separately enumerated as stated failure type per G-11. | **Doc 0 accurate.** |
| **2 · Solva** | | | | |
| BR-2.1 | Two-faculty seam enforced by import assertion | Met — #31 | **Not directly evidenced in current programme.** Solva itself has not been built in the Extraction-Akki repo; Solva is chartered in canon but not yet wave-shipped. The chokepoint's own build-time gate (negative scan) IS the analogous mechanism for the shield boundary. | **Doc 0 credits Solva; programme has not built Solva engine yet.** Wave-honest limit — Solva is a future wave. |
| BR-2.2 | Solva's role in "innovate" outcome recorded as joint with CIF | Partial | Not applicable to current programme (Solva not built). | **N/A yet.** |
| BR-2.3 | ThinkLab reasoning trace retained from first commit | Met — #31 | Not applicable to current programme. | **N/A yet.** |
| **3 · Northena** | | | | |
| BR-3.1 | Objective-freeze single shared implementation | Met — Promise #32 | Not directly built in Extraction-Akki. Objective-freeze semantics analogue exists in programme via `campaign_infra` (frozen queue manifests) but is per-campaign, not a shared cross-subsystem primitive. | **Doc 0 credits Northena; programme has campaign-local analogue but not the shared primitive.** |
| BR-3.2 | Progressive disclosure checkpoint states outcomes | Not confirmed | Not applicable yet. | **N/A yet.** |
| **4 · Mtafiti (Registry)** | | | | |
| BR-4.1 | Extend from estate sources to full asset class (models, artifacts, receipts, rules) each with named owner | Not Met — G-3 open | Programme confirms: estate connection exists (DB Data API) but no unified asset registry covering models + artefacts + receipts + rules. Trained artefacts (A-0-v1 adapter sha256 `49735d51ea…`) are banked in phase0 receipts but not in a queryable asset registry. | **Doc 0 accurate; G-3 open.** |
| BR-4.2 | Registry exposes asset classification scheme in enumerable form | Partial | Same as BR-4.1. | **Doc 0 accurate.** |
| **5 · Targeta** | | | | |
| BR-5.1 | Model acceptance: every criterion or refuse in full | Met — MOAC Promise #22 | Programme has NOT built MOAC (Model Output Acceptance Committee) as a first-class subsystem. Targeta itself is chartered but not yet wave-shipped. The programme's shield-train seeds trainers and produces adapters, but there is NO acceptance gate between adapter production and registry entry — DAP-31 (T-1 amendment) explicitly names this gap. | **Doc 0 credits MOAC; programme has NOT built MOAC yet.** |
| BR-5.2 | Yield wall detects/optimises but cannot grant acceptance | Met — 19A.2 | Not applicable yet (Targeta not built). | **N/A yet.** |
| BR-5.3 | Acceptance policy stated as named SFP | Not Met — G-7 open | N/A yet. | **N/A yet.** |
| **6 · Mkondo** | | | | |
| BR-6.1 | Every subsystem-to-subsystem hand-off crosses registered checkpoint (generalised) | Partial — Promise #32 marked Partial in canon; G-13 open | **Programme confirms.** Only the ThinkLab → Task Manager crossing has a registered contract per canon; programme has campaign_infra dispatch which is a per-campaign analogue but not a subsystem-crossing checkpoint. | **Doc 0 accurate; G-13 open.** |
| BR-6.2 | Malformed hand-off surfaces as finding at point of hand-off | Met for one crossing | N/A generally yet. | **Doc 0 accurate.** |
| BR-6.3 | No-dual-hatted-task rule enforced at hand-off checkpoint | Named as Promise #32 feature | Not enforced generally in programme. | **Doc 0 accurate.** |
| **7 · The Watch (Grey Mirror + Watch)** | | | | |
| BR-7.1 | Grey Mirror / Watch separated behind shared verdict interface | Met — Macho/Mkono | Not built in programme yet. Watch waves chartered in original Wave C but not yet shipped. | **Doc 0 credits Watch; programme has NOT built Watch.** |
| BR-7.2 | Watch's own trust domain described distinct from observed | Partial — isolation exists, ADV_ARC description not confirmed | N/A yet. | **N/A yet.** |
| BR-7.3 | Watch policy changes via slowest countdown + external witness | Met — stated explicitly | N/A yet. | **N/A yet.** |
| BR-7.4 | Grey Mirror learned pattern-matching excluded from Watch decision | Not confirmed | N/A yet. | **N/A yet.** |
| **7 · Watch amendments (from Trojan/Whisper)** | | | | |
| — | **AMENDMENT 6 (2026-09-05): The Watch upgraded to full Reference Monitor instance.** | Amended · not yet reflected in Doc 0 Part 2 text | N/A yet (Watch not built). | **Doc 0 v1 stale — Trojan/Whisper Amendment 6 supersedes Component 7's "Reference-Monitor-adjacent" tag.** |
| **8 · The Ledger** | | | | |
| BR-8.1 | Ledger retains records of refused operations on same terms as accepted | Met — WPW-7 pattern | Programme has append-only receipts pattern (phase0/*.json), but no unified Ledger subsystem. Refused-operation receipts do exist in shield_train dispatch_error records (banked this session at `phase0/gpu_receipts/20260906T160900Z_diagnosis/`). Pattern matches. | **Doc 0 accurate for pattern; programme has NOT built named "Ledger" subsystem.** |
| BR-8.2 | Append-only hash-chained structure independently verifiable | Met in structure | Programme uses append-only files but NO hash chaining across records observed. Independent verifiability by non-writer NOT demonstrated. | **Doc 0 accurate ("Met in structure"); programme lacks hash chain.** |
| BR-8.3 | Ledger writer included in TCB enumeration | Not Met — G-1 open (no TCB enumeration) | Same as G-1. | **Doc 0 accurate; G-1 open.** |
| **9 · CIF (Conditioned Ideation Faculty)** | | | | |
| BR-9.1 | CIF excluded from TCB by test | Met by doctrine | Not applicable — CIF not built in programme. | **Doc 0 credits by doctrine; programme has NOT built CIF.** |
| BR-9.2 | CIF-originated idea passes deterministic acceptance point | Met | N/A yet. | **N/A yet.** |
| BR-9.3 | CIF's MUST/MUST-NOT set carries assessment procedure | Not confirmed | N/A yet. | **N/A yet.** |
| **10 · Critic Seam (Doc 19A)** | | | | |
| BR-10.1 | QA-tier findings don't block execution; routed to deterministic decision | Met — QA-1 | Not built in programme yet as a first-class Critic Seam. | **Doc 0 credits Critic Seam; programme has NOT built Critic Seam.** |
| BR-10.2 | Seam outcome set stated per check | Partial | N/A yet. | **N/A yet.** |
| **11 · MOAC** | | | | |
| BR-11.1 | MOAC criteria not alterable by the evaluated run | Met | Not built. | **Doc 0 credits MOAC; programme has NOT built MOAC.** |
| BR-11.2 | MOAC non-bypassability + tamper-resistance demonstrated in security-arch description | Not Met — G-6 open | Not built. | **Doc 0 accurate; G-6 open.** |
| **12 · Manage Rules** | | | | |
| BR-12.1 | Every customer rule change through ceremony; full version history | Met — Promise #27 | Not built. | **Doc 0 credits Manage Rules; programme has NOT built Manage Rules.** |
| BR-12.2 | No customer rule can relax a STRUCTURAL/MECHANICAL system rule | Partial | Not built. Cross-check: Registry `Enforcement Class` column is UNPOPULATED (see `canon_system_rules_registry_inventory.md` §F) — so RBM-6 has nothing to check against anyway. | **Doc 0 accurate; programme prerequisite (Registry classification) also missing.** |
| **13 · Whitepaper Wizard** | | | | |
| BR-13.1 | Tier-3 eligibility outcome set stated (results / methods / both / not) | Met — WPW-11 | **Programme has shipped Tiers 1+2 of Whitepaper Wizard** (per DECISIONS.md — Wave WPW-v1-d closed at ratchet 2924 base with invariants including notebook entries, contemporaneous emit, evidence-class discipline). **Tier 3 (two-path eligibility) NOT YET SHIPPED.** | **Programme has more than Doc 0 credits AT tiers 1+2 (18 controls' worth banked); Tier 3 eligibility path unspecified in programme yet.** |
| BR-13.2 | Every notebook entry carries timestamp + link + evidence class | Met — WPW-4 | **Programme confirms.** WPW-4 evidence class (`measured / estimated / observed`) is a live invariant. Banked at ratchet 2978. | **Doc 0 accurate; programme delivers.** |
| BR-13.3 | Wizard cannot alter training state; build-time zero-influence check | Met — WPW-2 with A2 acceptance | **Programme confirms.** Zero-influence invariant is a live gate in `tests/invariants/`. | **Doc 0 accurate; programme delivers.** |
| **14 · Connect Wizard** | | | | |
| BR-14.1 | Rights recorded at connection setup as explicit PIP for downstream | Met in function | Not built as a first-class Connect Wizard. Programme uses DB credentials via `estate_keys/` but this is deployment-level, not a governed onboarding checkpoint. | **Doc 0 credits Connect Wizard function; programme has NOT built Connect Wizard as a checkpoint.** |
| **15 · Agent-Deploy Wizard** | | | | |
| BR-15.1 | Checkpoint outcome set stated (deploy / lower rung / defer) | Not confirmed | Not built. | **N/A yet.** |
| **16 · Deck Rendering Engine** | | | | |
| BR-16.1 | Byte-identical output for identical DeckSpec input (build-time verified) | Met — DR-R2 | Not built. | **Doc 0 credits Deck Rendering Engine; programme has NOT built it.** |
| BR-16.2 | 14 controls carry explicit owning subsystem field | Partial | N/A yet. | **N/A yet.** |

## §C · Delta summary

**Categories:**

1. **Doc 0 accurate and programme built (Doc 0 = Met, programme evidences):**
   - BR-1.1 (chokepoint non-bypassability negative-scan)
   - BR-1.5 (chokepoint fail-closed)
   - BR-13.2 (Whitepaper Wizard notebook timestamps + evidence class)
   - BR-13.3 (Whitepaper Wizard zero-influence)
   - Effective count: **4 fully-accurate BRs**.

2. **Doc 0 accurate and programme partial/gap-open (Doc 0 = Partial or Not Met, programme confirms gap):**
   - BR-1.2 (runtime integrity check missing · G-6)
   - BR-1.3 (trust receipt AU-3 elements · G-8)
   - BR-1.4 (typed custody attribute · G-3)
   - BR-4.1 (asset inventory extension · G-3)
   - BR-4.2 (asset classification scheme · G-3)
   - BR-6.1 (generalised hand-off contract · G-13)
   - BR-8.2 (Ledger hash chain independently verifiable)
   - BR-8.3 (TCB enumeration · G-1)
   - BR-11.2 (MOAC security-arch description · G-6)
   - BR-12.2 (customer/system-rule conflict enforcement)
   - Effective count: **10 accurate-but-gap-open BRs**.

3. **Doc 0 credits a component the programme has NOT built (Doc 0 = Met/Partial for a component that is Doc-canon but Wave-not-yet-shipped):**
   - Solva (BR-2.1, BR-2.2, BR-2.3) — 3 BRs on unbuilt component
   - Northena (BR-3.1, BR-3.2) — 2 BRs, only campaign-level analogue in programme
   - Targeta (BR-5.1, BR-5.2, BR-5.3) — 3 BRs on unbuilt component (MOAC / yield wall)
   - The Watch (BR-7.1..BR-7.4) — 4 BRs on unbuilt Watch
   - Ledger (BR-8.1 pattern, BR-8.2 partial) — programme has append-only receipts pattern but no unified Ledger subsystem
   - CIF (BR-9.1..BR-9.3) — 3 BRs on unbuilt CIF
   - Critic Seam (BR-10.1, BR-10.2) — 2 BRs on unbuilt seam
   - MOAC (BR-11.1) — same as Targeta
   - Manage Rules (BR-12.1, BR-12.2) — 2 BRs on unbuilt customer rule surface
   - Connect Wizard (BR-14.1) — 1 BR on unbuilt onboarding
   - Agent-Deploy Wizard (BR-15.1) — 1 BR on unbuilt deployment step
   - Deck Rendering Engine (BR-16.1, BR-16.2) — 2 BRs on unbuilt renderer
   - Effective count: **~28 BRs credited to components the programme has NOT built**.

4. **Doc 0 stale (superseded by Trojan/Whisper amendments 2026-09-05):**
   - Component 7 (Watch) — tag "Reference-Monitor-adjacent" superseded by Amendment 6 (full Reference Monitor instance).
   - Attribute 3 — needs "coalition" principal class addition per W-4.
   - Attribute 7 — needs Estate Release Budget mandatory-baseline instance per W-7.
   - Component MOAC / Component 7 build reqs — new build requirement (fail-closed A5.9 per Amendment 7) needs adding to Attribute 11 instantiation.
   - Doc 0 needs Rules Service added as component 17 (per Rules Service Spec §5 — "six engines plus three" replaces "six engines plus two").
   - Effective count: **5 Doc-0-stale points**.

5. **Programme has MORE than Doc 0 credits:**
   - Whitepaper Wizard Tiers 1+2 shipped with more invariants than the 3 BRs in Doc 0 enumerate (WPW spec has 18 controls; Doc 0 lifts 3). Programme's ratchet at 2978 includes many invariants beyond just BR-13.1/13.2/13.3 — the WPW-4/WPW-7 (refused-run retention) pattern is invariant-enforced. This is Doc-0-undercredits-programme rather than Doc-0-stale.
   - Shield-train pipeline (Extraction-Akki current programme) sits DOWNSTREAM of the SyniSense chokepoint pattern and adds: masking policy governance with drawer lifecycle (first drawer cycle proven this session · Ruling #5(a) landed), multi-table extraction with per-table refuse-by-construction, dispatcher heartbeat/queue-completion pattern, campaign v2 corpus-consistency ruling, dispatcher double-setsid fix (this session). None of these are in Doc 0 Part 2 (which describes canon components; shield-train is a subsystem-USE not a subsystem-DEFINITION).
   - Effective count: programme has **~20+ invariants operationally enforced under the 2978 floor** that Doc 0 Part 2 does not describe because Part 2 is per-canon-component, not per-actual-code-file.

## §D · Bottom line for owner sequencing

- **Doc 0 v1 status column is accurate on the components the programme has already built or is downstream of** (Shield chokepoint + Whitepaper Wizard T1+T2).
- **Doc 0 v1 status column is aspirational on the components the programme has NOT built yet** (Solva · Targeta / MOAC · Northena · The Watch · CIF · Critic Seam · Manage Rules · Connect Wizard · Agent-Deploy Wizard · Deck Rendering Engine · unified Ledger). For these, Doc 0 says "Met" or "Partial" because canon has been WRITTEN, not because code has been shipped. The delta is not stale — it is a spec-vs-implementation gap, which is what a ratification round exists to close.
- **Doc 0 v1 is stale on 5 points** superseded by Trojan/Whisper amendments and by Rules Service Spec introduction — these should be folded into Doc 0 v1.1 on the same ratification.
- **The programme has enforced 2978 invariants** under BASELINE_GUARD=1, of which the majority live inside Extraction-Akki (Shield-adjacent + Whitepaper Wizard + campaign infra + shield-train). None of these will regress: adding new components does not lower the floor.
