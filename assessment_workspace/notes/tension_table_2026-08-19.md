# Tension & Ambiguity Table — Owner Order 2026-08-19 · v7 Ingest Cycle · FL-P2-26

Owner directive verbatim: *"HTML, reproduce exactly as is. surface tensions or ambiguity."*

Every row below names a **collision between "reproduce exactly as is" and something already binding on this estate** (a standing owner ruling, a canon, a built surface, or the Canon Addendum). Each row proposes a default. **None of these defaults are applied yet — the owner rules first.**

## Legend

- **Prototype (v7)** — what the standalone HTML shows or claims.
- **Standing** — owner ruling, canon, built surface, or Addendum entry currently binding.
- **Proposed default** — what I would do absent an owner ruling. Marked **[A]** for the safer reading, **[B]** for the other honest reading; I recommend **[A]** unless annotated otherwise.

---

## §1 · Load-bearing tensions (must resolve before mass reproduction)

### T1 · "Reproduce exactly as is" vs the no-fabrication rule (FL-P2-13)

**Prototype (v7):** Every figure in the standalone HTML is seeded demo data. Registry claims "86.4 TB across 12 sources, 78% measured at census #4"; Compute claims "1,240 hrs committed of 2,880 available"; LLMs & Trained Models lists five named models (Claude Sonnet 5, TRN-007, EMB-002, Long-context eval, SUM-001) with 128,400 monthly calls and KES 1.9M spend; Shield reports 4,182 crossings this week with receipts R-4390 etc; Grey Mirror shows suspects ACT-1189, ACT-1043, marked accounts, bait BR-77. None correspond to anything on the estate.

**Standing:** FL-P2-13 (assessment, 2026-08-15) established the "no-fabrication" ruling — the built estate MAY NOT render a figure that does not trace to a durable record on disk. The Registry-A4 cycle just closed on this rule: the built Registry renders only what `phase0/data_connection_records/*_FINAL.json` + `phase0/commissioning_records/*_ACCEPTED.json` support, and every approximation carries `is_approximate=True`. The invariant test `test_response_never_carries_fabricated_or_secret_tokens` explicitly blocks "Acme Holdings", "1,245,802" etc.

**The collision:** verbatim reproduction of v7 = shipping every one of those demo figures into the built surface = a violation of FL-P2-13 in every screen.

**Proposed defaults:**
- **[A · recommended]** Reproduce **structure, layout, page-pattern, copy grammar, navigation, walk affordances, wizard shapes, chip vocabularies, chart shapes** exactly as v7 shows. Bind **real records** where they exist (2 DBs, 1 host, 0 models — as the current Registry already does). Where v7 shows demo content with no real counterpart, render **honest empty** with the drawn-not-blank sentence pattern ("Not yet measured — drawn, never left blank"), and keep the surface fully reproduced.
- **[B]** Ship v7 exactly, including every demo figure, with a global "prototype content" banner and a per-figure demo marker. Treat the whole estate as an offline preview until real records exist for each figure.

**Recommendation: [A].** [B] compounds FL-P2-13 estate-wide and hands the owner a demo interface, not an operating estate. [A] preserves the grammar the prototype teaches while telling the truth about what is measured. **Owner ruling needed.**

---

### T2 · v7 nav taxonomy vs Canon 5 five-pillar identities

**Prototype (v7):** Nine nav groups arranged under four tabs (Work · Build · 3rd Party Apps · Admin). 29 direct destinations plus ~30 ceremony/walk/wizard states. Registry is one destination under `estate` (siblings: Shield, Grey Mirror). See `notes/prototype_inventory_v7.md` §1.

**Standing:** Canon 5 (Interface Architecture, `notes/canon_5_requirements.md`) frames the surface in **five pillars** — Northena (direction/scope), Solva (reasoning), Targeta (training), Mtafiti (research/retrieval), Watch (Mkondo/security). These are **identities**, not menu items. Prior standing rulings FL-P1-15..19 (label-vs-identity handling) said pillar identities live behind the surface; menu labels are what the operator sees.

**The collision:** v7's nav labels (Manage Estate, Approvals, Build Your Resources, Your Resources, Performance Management…) do not name the five pillars. The mapping v7↔Canon 5 is:
- Northena ⇒ implicitly inside `workstudio` + `thinklab` (framing) and `estate` (Registry census scope).
- Solva ⇒ inside `thinklab`.
- Targeta ⇒ inside `build.train` + `approvals.modeladmission`.
- Mtafiti ⇒ inside `workstudio.analyze` (Data Suite) + `build.extract`.
- Watch ⇒ `estate.greymirror` + the `watch` group hook + the whole Grey Mirror surface.

**Proposed defaults:**
- **[A · recommended]** Use v7's labels verbatim on the surface (Manage Estate, Approvals, Board 360 etc.). Maintain a canonical mapping table (this file, §T2) so the pillar identities survive behind the labels. No "Northena tab" on the UI; pillar identity is a routing/telemetry concept.
- **[B]** Add small pillar chips inside each screen ("this screen belongs to Solva") — extra decoration, no functional change.

**Recommendation: [A].** Owner has not asked for pillar labels visible. [B] adds surface noise without changing behaviour. **Confirm A is acceptable.**

---

### T3 · Prototype tech (single-file HTML) vs the built React estate

**Prototype (v7):** 1.31 MB standalone HTML with an inline React app compiled to `React.createElement` calls; no external routes, no fetch, no server. Loads and runs from disk with no dependency.

**Standing:** Our operating estate is React SPA + FastAPI + Aurora Data API behind a strict IP allowlist (`SPINE_ALLOWED_IPS=34.16.56.64`). All copy passes through JSX components; every screen fetches its facts from `/api/*` endpoints; every endpoint is gated by the allowlist middleware.

**The collision:** "Reproduce exactly as is" admits two literal readings:
- **[A · recommended]** **React parity.** Rebuild the v7 surfaces as JSX components inside `/app/frontend/src/components/`, backed by `/api/*` endpoints that serve real records; treat the v7 HTML as the reference oracle (grammar, copy, layout, page pattern, chip vocabulary). Same policy as Registry-A4.
- **[B]** **Literal HTML.** Serve the v7 HTML file as a static asset from the pod-shell frontend (or from the FastAPI backend) at a route like `/prototype/v7.html`. Zero binding to real records; zero fabrication risk since the surface is labelled a prototype.

**Recommendation: [A].** [B] gets us zero of the actual product; it's a museum exhibit next to a working estate. [A] is what we did for Registry — it works. **Confirm A.**

---

### T4 · Registry brief PDF vs v7 Registry section — do they agree?

**Prototype (v7):** Registry sits at `estate.estate` with three interior tabs by internal `tab` key: `measure` (DATA CONNECTED), `compute` (COMPUTE CONNECTED), `llms` (LLMs & Trained Models). Copy grammar matches the fixture PDF (`fixtures/screen_mockups_v7.pdf`) verbatim — same page pattern (fluid left + 300px right context panel), same content rules, same approximation glyph.

**Standing:** The Registry-A4 build shipped **exactly this** structure this cycle (Extraction-Akki `0c417f2` on track-a). Six Playwright screenshots at `phase0/drill_receipts/screenshots/20260819T151700Z_*.jpeg` show the surface conforming to both the PDF and v7.

**The collision:** none for the tab shape. **Sub-tension**: v7's internal tab key `measure` for DATA CONNECTED (vs. our built `data-connected`). Copy-facing label is identical; internal test-id is not. Trivial to reconcile if owner wants the internal key `measure` too.

**Proposed default:**
- **[A · recommended]** Keep the internal key `data-connected` (matches label; better testid vocabulary; already committed). Note v7's `measure` in a mapping comment.
- **[B]** Rename to `measure` for verbatim parity with v7.

**Recommendation: [A].** No functional difference; test-ids should reflect labels. **Non-blocking, but flag for owner sign-off.**

---

### T5 · Promise Table (50 rows) vs the built thin-kernel registers

**Prototype (v7) / Promise Table:** 31 canon promises + 8 A-series (built-without-canon) + 5 N-series (new candidates) + 6 enhancements. The v7 HTML renders surfaces that would host ~31 of these (Data Shield, Reasoning Shield, Access Shield, Grey Mirror, Shield, Manage Rules ceremony, Board 360, Exco 360, Documents suite, Rule Books Library, Collab, Spend Requests, "Walk this →" affordance, Cost Ledger, Model Admission, model-registry, training runs, etc.).

**Standing (currently built on the estate):**
- **Data-source connect** (Promise #12) — Present. Two databases live.
- **Registry (single-source, single-host)** (Promise #14 partial · #13 partial · #10 partial) — Present via `services.registry_facts` + Registry.jsx.
- **Compute connect** (Promise #10) — Present (akki-vm connected/hardened/accepted).
- **IP-allowlist gate** (adjacent to Promise #1 but NOT the masked-crossing gate) — Present.
- **Reflection-before-commit stubs** (Promise #11) — Not built.
- **The Watch, Grey Mirror, Shield surfaces** (Promises #1 masked-crossing, #6, #7, #8, #16, #17, #18, #26, #27) — Not built.
- **Training, Model Admission, Model Registry** (Promises #22–#25, #30) — Not built.
- **All A-series (Board 360, Exco 360, Documents, Rule Books Library, Collab, Spend Requests, ThinkLab→Task hand-off, Walk this →)** — Not built.
- **All N-series (retention enforcement, breach notification, individual access-and-erasure, residency, ledger continuity)** — Not built.

**The collision:** v7's copy assumes ~90% of the platform exists. The built estate has ~5% of it. Rendering v7 verbatim = shipping ~90% empty behaviour behind ~90% present-tense copy, i.e. lying on-screen.

**Proposed defaults:**
- **[A · recommended]** Per-surface **build register** (like the Promise Table) governs which v7 screens are ready to ship. Rules:
  1. If a surface has a durable record class already writable and readable in the built estate, ship it verbatim (grammar) with **real records** (Registry, Compute, LLMs).
  2. If a surface has no durable record class yet, ship the surface **shell** (nav destination, page pattern, page-topline copy, empty-state sentence) with the drawn-not-blank sentence. Do NOT ship the demo rows.
  3. If a surface is a **ceremony** (rule-book update, actor admit, spend approval), ship the wizard shell (all v7 chip/step copy) but do not accept commits until the ceremony's backing record class exists — the ceremony surfaces as "not yet in service".
  4. If a surface is behavioural (Shield gates, Watch containment, Grey Mirror bait), the surface itself is the last thing to ship — the mechanisms come first. Do not ship the surface alone.
- **[B]** Ship v7 as-is (full demo). Add a global "prototype content · not the live estate" banner. Owner + operators use it as a walk-through, not as an interface.

**Recommendation: [A].** [B] compounds T1. [A] is what Registry-A4 already demonstrates. **Owner ruling needed** on whether [A] is acceptable as the standing pattern.

---

## §2 · Structural tensions (Addendum-adjacent)

### T6 · Canon Addendum §1 confirmed closures — legitimate or new fabrication?

**Prototype (v7):** Six "Absent → added" promises (#4, #17, #19/#20/#21, #24, #25, #26) show as small additions on their surfaces — e.g. the audit trail Overview stating "2+ independently-governed units", Registry showing "58% reduced to reusable memory", per-turn warm/fresh tag.

**Standing:** Canon Addendum 1 §1 explicitly confirms these six build-side additions as legitimate closures of pre-existing canon promises — **not** rewrites of the canon. Recorded as CA1-001..CA1-006 in `notes/canon_addendum_1_requirements.md`.

**Proposed default:**
- **[A · recommended]** Treat these six additions as REQUIRED sentences on the corresponding surfaces (per Addendum §1). They do NOT violate FL-P2-13 because they cite a canon promise; the promise is the record. Reproduce verbatim.

**Non-tension, but requires reading Addendum §1 before we render.**

---

### T7 · Canon Addendum §2 six new amendments — must ship

**Prototype (v7):** Some Addendum §2 items are already visible in v7 (Cost Ledger surface fragments, model re-check dates, etc.). Others are NOT.

**Standing:** Addendum §2 records **six binding amendments** (CA1-007..CA1-012) that add to the canon. Every one is a required capability the platform must gain:
- CA1-007 · dry-run preview between Review and Adopt (Doc 2 · #2)
- CA1-008 · Cost Ledger surface with named lever sequence (Doc 11 · #9)
- CA1-009 · generalised handoff contract for every cross-app crossing (Doc 15 · #32)
- CA1-010 · "lower the standard" scoped to session with logged expiry (Doc 4 · #8)
- CA1-011 · standing re-check date per in-service model (Doc 13 · #22)
- CA1-012 · Watch staleness-flagging extended to rulebooks/baselines (Doc 15 · #27)

**The collision:** these are canon-of-record REQUIREMENTS, not enhancements. Any reproduction of v7 must incorporate them.

**Proposed default:**
- **[A · recommended]** Every reproduction of the affected surfaces MUST carry the Addendum §2 amendment. Where v7's copy already reflects it (e.g. per-model re-check dates), reproduce verbatim. Where v7's copy does not yet reflect it (e.g. no visible Cost Ledger), the reproduction ADDS the surface, guided by Addendum §2's Delivery Experience wording.

**Owner ruling needed** on whether we ship the extension as part of this cycle or defer.

---

### T8 · CA1-A8 "Walk this →" custody load-bearing question

**Prototype (v7):** `WALKS` constant defines four walk stories (bait, crossing, rule, broken). Each renders as an in-place drill-in that shows evidence AT the point of any figure or claim.

**Standing:** Canon Addendum §3 CA1-A8-q1 (marked "load-bearing" in the source doc): *"Does 'Walk this →' inherit the source data's custody rules, so a viewer without access to the underlying estate region is refused the same way Document 1's chokepoint would refuse them — or can it leak view access to material the viewer isn't otherwise entitled to see? This is the load-bearing question: an unscoped trace affordance is a second, ungoverned path to the same data Document 1 built one chokepoint specifically to control."*

**The collision:** shipping the "Walk this →" affordance without a resolved custody scope = building a second data path that circumvents Doc 1's chokepoint. Zero-fabrication + zero-leak discipline (FL-P2-13, FL-P1-08) forbids this.

**Proposed default:**
- **[A · recommended]** **DO NOT ship** the "Walk this →" affordance yet. Ship the surface pattern but leave the affordance as "not yet available — resolves after Doc 1 chokepoint custody scoping" per Addendum §1's drawn-not-blank pattern.
- **[B]** Ship the affordance scoped to only the CURRENT user's identity from the IP-allowlist source (i.e. no custody hierarchy exists yet; every user sees everything). Trace becomes a viewing feature until we build the shield.

**Recommendation: [A].** [B] is what the prototype implies but formally opens the second chokepoint. **Owner ruling needed** — this one blocks a v7 pattern that runs across every surface.

---

### T9 · CA1-N-series (retention · breach · access-and-erasure · residency · ledger continuity)

**Prototype (v7):** Zero surfaces exist for N1..N5. The Promise Table §"New Promise Candidates" names all five as future promises.

**Standing:** Addendum §3 CA1-N1..CA1-N5 explicitly says "no built instance". Nothing to reproduce.

**Proposed default:**
- **[A · recommended]** These are Chunk-3 assessment rows classed as BUILD (net-new). They do not enter the v7 reproduction cycle. No tension; no action this cycle.

**Non-tension. Recorded for the row-map.**

---

## §3 · Grammar tensions

### T10 · Copy grammar — plain sentences first, measures behind

**Prototype (v7):** Universally applies this pattern: every stat has a plain-sentence caption above and the number below with a small note. Headline decks use crimson emphasis on the load-bearing figure. Approximate figures use `≈`. Un-measured figures are drawn (hatched bars, "not yet measured — drawn, never left blank").

**Standing:** The Registry brief PDF and the Registry-A4 build both apply this grammar. Our built Registry.jsx honours it: crimson emphasis, `≈`, hatched vs solid bars, "drawn, never left blank" sentence.

**Non-tension. Continue.**

### T11 · Role switcher

**Prototype (v7):** Three role personas (Compliance Owner, Watch Officer, Operator) shown as static chips in the header. No role-based auth flow; no permission enforcement.

**Standing:** Track-B (auth) is deferred (FL-P2-15). Our built Registry.jsx renders the same three chips as static decoration.

**Non-tension. Continue static rendering.**

### T12 · Wizard grammar

**Prototype (v7):** Two ceremony wizards (`rulebook`, `actor`) with the same shape: chips per step, guard clauses (e.g. hard-line refuses to be a "propose here"), a summary card, a Filed/Admitted done state. Plus the Connect wizard (`CONNECT_STAGES`) with five stages.

**Standing:** Our ConnectWizard already implements the single-panel paste-and-connect version per OWNER SIMPLIFICATION RULING (2026-08-18). v7's Connect wizard has five sequential stages instead — this is a REGRESSION back to the wizard form the owner explicitly retired.

**The collision:** literal reproduction re-introduces the multi-step wizard the owner killed.

**Proposed default:**
- **[A · recommended]** Keep the single paste-and-connect panel (already built). Note v7's five-stage sequence in a comment but do NOT reproduce it, citing the 2026-08-18 owner ruling as the tiebreaker.
- **[B]** Ship both — a paste-first primary path plus a "step by step" secondary path.

**Recommendation: [A].** Owner-ruling collision — owner already ruled against the five-stage form. **Owner may re-open if desired.**

---

## §4 · Scope tensions

### T13 · v7 has ~58 surfaces; the built estate has 2 — how much do we reproduce?

**Prototype (v7):** ~28 nav destinations + ~30 ceremony/walk/wizard states = ~58 distinct rendered surfaces.

**Standing:** Registry (3 tabs) + ConnectWizard (1 panel). Total 4 rendered surfaces on the estate today.

**Proposed default:**
- **[A · recommended]** Per T5, ship only the surfaces whose backing record class exists in the built estate. Concretely, from v7 that means: Registry (already shipped this cycle) and ConnectWizard (already shipped). Plus, unambiguous **collision-free extensions** from v7 that can be added now with real records:
  - **T13-safe-1** · v7 shows the same "record with commissioning + hardening receipts" pattern that our compute detail card already renders. No new surface needed.
  - **T13-safe-2** · v7 Registry topline includes stat cells for "Verified schemas", "Channel", "Provenance" which our built topline already includes. Match.
  - **T13-safe-3** · v7 has a "Reading the mix" context panel adjacent to the Visual band. Our built Registry already includes this — no delta.
  - **T13-safe-4** · v7 includes a `JUST CONNECTED` sage announcement row in the compute-connected tab. Our built COMPUTE CONNECTED already renders this row for akki-vm.

  So this cycle produces NO NEW SURFACES beyond Registry-A4 that are collision-free.
- **[B]** Ship the empty shells of all ~28 nav destinations, each with drawn-not-blank content. Big-visible outline, small-visible content.

**Recommendation:** [A] for now (Registry-A4 already done). [B] is defensible but needs a scope class + LOC ruling from the owner before we begin.

---

### T14 · Watch and Grey Mirror surfaces

**Prototype (v7):** `GM` constant (40 kB), Grey Mirror overview + monitor + response + people sub-surfaces. Rich enough to be usable as a Watch UI oracle.

**Standing:** No Watch mechanism exists in the built estate. Canon 3 + Canon 8 + Addendum §1 CA1-006 all frame the Watch as a specific mechanism (bait, containment ladder, self-check drill, external witness). None built.

**Proposed default:**
- **[A · recommended]** DO NOT ship a Watch surface at all until the Watch mechanism exists. A UI without its mechanism is stage scenery; per FL-P2-13, this violates the no-fabrication rule structurally (the surface asserts a Watch exists that doesn't).

**Non-tension by proposed default, but the owner may want to see the shell.**

---

## §5 · Summary — recommendation matrix

| # | Tension | Owner ruling required? | Proposed default |
|---|---|---|---|
| T1 | Reproduce exactly vs FL-P2-13 zero-fabrication | **YES · load-bearing** | [A] structure + grammar verbatim; real records where available; drawn-not-blank where not |
| T2 | v7 nav labels vs Canon 5 pillar identities | soft yes | [A] labels verbatim; pillars behind |
| T3 | Prototype tech vs React estate | **YES** | [A] React parity, v7 as oracle |
| T4 | Registry brief vs v7 Registry | non-blocking | [A] internal `data-connected` key (built) |
| T5 | Promise Table vs built kernel | **YES · load-bearing** | [A] per-surface build register; ship shells with real facts, not demo rows |
| T6 | Addendum §1 confirmed closures | non-blocking | [A] reproduce as canon-required sentences |
| T7 | Addendum §2 six amendments | **YES · scope decision** | [A] treat as canon; ship where evidence exists |
| T8 | Walk this → custody | **YES · load-bearing** | [A] DO NOT ship the affordance until Doc 1 chokepoint custody scoping resolved |
| T9 | N-series new promises | non-blocking | [A] Chunk-3 assessment rows; no v7 reproduction impact |
| T10 | Copy grammar | non-tension | continue |
| T11 | Role switcher static | non-tension | continue |
| T12 | Wizard grammar (Connect) | **YES** | [A] keep paste-panel; v7 five-stage retired |
| T13 | 58 surfaces vs 2 built | **YES · scope** | [A] no new surfaces this cycle; Registry-A4 covers it |
| T14 | Watch/Grey Mirror surface | **YES** | [A] do not ship until Watch mechanism exists |

**Blocking rulings (must arrive before mass reproduction begins): T1, T3, T5, T7, T8, T12, T13, T14.**

## §6 · What I would proceed with meanwhile (unambiguous, collision-free, extends what's built)

Per the owner's Sequence D allowance for unambiguous collision-free extensions:

1. **None as further code this cycle.** The Registry-A4 build already committed today (`0c417f2` + `0709be7` on track-a, `d3747ea` on assessment master) IS the collision-free extension. Every other v7 destination sits behind one of the ruling-required tensions above.
2. **Continuing artifact ingest** into the notes (this file, `promise_table_inventory.md`, `files_9_inventory.md`, `canon_addendum_1_requirements.md`, `prototype_inventory_v7.md`, `tension_table_2026-08-19.md`) is a pure notes-side task that carries no code impact and no fabrication risk. Committed to assessment master alongside the artifacts themselves.
3. **`test_credentials.md` refreshed** (`/app/memory/test_credentials.md`) so any future testing agent knows the estate is IP-allowlist gated (no login). Not a code change.

No production-code touch this cycle absent owner rulings on the load-bearing tensions above.
