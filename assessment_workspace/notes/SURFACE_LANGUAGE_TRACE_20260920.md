# Surface-language provenance trace — Step 2 report (WAVE R-69)

**Date:** 2026-09-20T~09:36Z (post-Commit-C fixup `23ff5808` · Step 3 sealed · Step 2 now executed)
**Owner directive banked at:** `STATE/DECISIONS.md` `2026-09-20T~08:56Z · OWNER DISPOSITION` — verbatim ruling: *"Surface-language ruling — trace it, don't bank it. Zero grep hits is the important fact here, not an inconvenience. Banking text now, on my say-so, would create the exact provenance fault this exercise exists to catch — a rule with no origin, now doubly sourced because I said so and something else cited it. Find where the citation entered — which document, which commit, whose hand. If it traces to a real conversation the owner had elsewhere, it gets banked from that source, dated correctly. If it traces to nothing, that's the finding, and every place downstream that assumed this rule was real needs checking for what it did on that assumption. Report before continuing autonomous work that depends on it."*
**Owner plan-approval banked at:** `STATE/DECISIONS.md` `2026-09-20T~08:56Z · OWNER PLAN-APPROVAL RULING` — verbatim: *"(b) TRACE RETURNS NOTHING → do NOT full-halt. Bank the finding + the downstream-assumption audit (every place that cited or acted on the phantom rule, and what it did on that assumption), REPORT it to me for the owner, then: PROCEED on work that does not depend on the surface-language rule; HOLD only work that does depend on it until the owner sees the report. That is the owner's wording exactly ('report before continuing autonomous work that depends on it')."*

## §1 · Scope

Trace the citation *"2026-09-08 surface language (owner ruling)"* — cited by the owner's `2026-09-20T~08:24Z` disposition as one of three "owner ruling" citations with no record on this desk. The prior 06fcc405 direct-answers digest reported *"NOT FOUND · zero grep hits anywhere in tree"* — this report performs the exhaustive 5-location re-trace ratified by owner at plan-approval.

**Locations traced (all 5):**
1. CODE — `/app/assessment_workspace/repos/Extraction-Akki` @ `programme/track-a` HEAD `31d414bd540632e52cb050321b71b29b730a0f1e`
2. STATE — `/app/assessment_workspace` @ `master` HEAD `23ff5808` (Step 3 Commit-C fixup this-wave)
3. Sibling — `/app/assessment_workspace/repos/RMS-IQ-Core-2` @ `main` HEAD `ea5aa019521eee22ad4f8ea29efdfa2af357be3b`
4. Sibling — `/app/assessment_workspace/repos/Akki-OS-V1` @ `main` HEAD `8c361903cdd319bfdc0709de3f4392f5bfa3956b`
5. Sibling — `/app/assessment_workspace/repos/Akki-Executive-Core` @ `main` HEAD `5844eee95d5faffea0dcab98bd4fe5e8d1419f32`

**Quarantine flag (owner-specified · special-flag):** `/app/assessment_workspace/repos/Akki-Executive-Final` @ `main` HEAD `bba80ab5d07e5b7ba300e13e26a8e1cf7a60869e` — read-only grep permitted for trace only; not one of the 5 working locations.

**Phrase set (exact + near variants):** `surface language` · `surface-language` · `surface wording` · `surface copy` · combined with the date `2026-09-08` where relevant.

**Method:** for each repo (a) working-tree recursive case-insensitive grep with `--exclude-dir=.git`, (b) full-history pickaxe `git log --all -S <phrase>`.

## §2 · Results table

| Location | HEAD | `surface language` (WT) | `surface-language` (WT) | `surface wording` (WT) | `surface copy` (WT) | `git log -S "surface language"` (all-branches) | `git log -S "surface-language"` (all-branches) |
|---|---|---|---|---|---|---|---|
| CODE Extraction-Akki | `31d414bd` | **1 hit** `docs/stage_a_proposals/census_dimensions.md:272` (common-noun rationale, CD-E5 router path) | 0 | 0 | **1 hit** `docs/stage_a_proposals/ui_1_stage_a.md:1049` (compound noun "developer-surface copy" in G-11 BINDING COPY gate) | 1 commit `a73a3ea` "docs(stage_a): census-dimensions mini-phase Stage A proposal (CD-E1..E4 Tier-1 · CD-E5 Tier-2 · Owner Message 565)" | 0 |
| STATE `/app/assessment_workspace` | `23ff5808` | trace-metadata-only (17 hits — all in reporter docs: `notes/DIRECT_ANSWERS_TO_OWNER_20260920.md`, `notes/ORCH_BOOT.md`, `phase0/credential_drop_manifests/20260920T0856Z_owner_drops_manifest.json`, `STATE/NEXT.md`, `STATE/DECISIONS.md` — every hit is either the owner's disposition text, the trace instructions, or this-wave planning) | trace-metadata-only (all in same reporter docs) | 0 | **3 hits** — all part of the 2026-08-25 Solva/Solver vocabulary correction (`notes/w5_grounding_brief.md:5`, `notes/close_report_template.md:52`, `STATE/DECISIONS.md:1177`) — **UNRELATED**, different date, different concept, fully cited to owner correction 2026-08-25 | trace-metadata commits only (WAVE R-69 commits `04fcf6de` / `bbdfef1c` / `9c0dd840` / `23ff5808` / `168f3c16` / `06fcc405` — all reporter/plan/instruction commits) | trace-metadata-only |
| Sibling RMS-IQ-Core-2 | `ea5aa019` | **1 hit** — SAME file, SAME line as CODE (identical `census_dimensions.md:272`) | 0 | 0 | **1 hit** — SAME file, SAME line as CODE (identical `ui_1_stage_a.md`) | 1 commit `a73a3ea` (identical to CODE — same Stage-A authoring event) | 0 |
| Sibling Akki-OS-V1 | `8c361903` | **1 hit** — SAME file, SAME line as CODE + 1 mirrored copy at `frontend/public/downloads/ui_1_stage_a.md:446` | 0 | 0 | **2 hits** — same G-11 line at `docs/stage_a_proposals/ui_1_stage_a.md:446` + mirrored copy at `frontend/public/downloads/ui_1_stage_a.md:446` (same compound noun) | 1 commit `a73a3ea` (identical Stage-A authoring event) | 0 |
| Sibling Akki-Executive-Core | `5844eee9` | **0** | **0** | **0** | **0** | **0** | **0** |
| Quarantine Akki-Executive-Final | `bba80ab5` | **0** | **0** | **0** | **0** | **0** | **0** — **quarantine flag CLEAR (source does NOT live in quarantine)** |

## §3 · Every hit contextualised (not a citation, none of them)

### §3.1 · `census_dimensions.md:272` (CODE + RMS-IQ-Core-2 + Akki-OS-V1 · same file)

Verbatim (line 272):
> **Statement:** router mounts at `/api/census/dimensions/*` (matches Owner-visible surface language in TF close §6). Alternative was `/api/mtafiti/dimensions/*` (matches internal Mtafiti registry pattern). Chosen `/api/census/dimensions/*` because the surface concept is "census outputs", not "Mtafiti internals".

Section header (line ~262): `### §5.5 CD-E5 [Tier 2] · Router mount path (disclosure-only, no ruling required)`.

**Verdict:** **Common-noun usage** ("Owner-visible surface language" = "the wording the owner sees"). Cites **TF close §6** as its source — not "2026-09-08". Not a rule invocation. Not a MUST/MUST-NOT. Tier-2 disclosure-only with **no owner ruling required** at that E-item. Cannot be the origin of the phantom citation.

### §3.2 · `ui_1_stage_a.md:1049` (CODE) / `ui_1_stage_a.md:446` (Akki-OS-V1 + mirror)

Verbatim (excerpted):
> G-11 | **BINDING COPY verbatim (charCodeAt AST guard)** | All BINDING COPY strings from UI Spec v2.2 §10 + A1 verbatim door labels + A1.4 verbatim In-progress/Ready copy + A1.7 verbatim CTA renames + A1.6 verbatim **developer-surface copy** + A1.2 verbatim shapes/commits + A2.2 verbatim refusal copy render byte-identical …

**Verdict:** **Compound noun** — "developer-surface copy" = "copy shown on the developer surface". Attribution is `A1.6 verbatim` (canon anchor, not 2026-09-08). Not a "surface language rule" — it's the BINDING COPY discipline anchored to UI Spec v2.2 §10 + Owner charCodeAt anti-slop precedent. Cannot be the origin.

### §3.3 · STATE "surface language"/"surface-language" 17-odd hits — all trace-metadata

Every occurrence lives inside reporter documents produced **within this wave (R-69) or the two preceding CCS3-close commits `06fcc405`/`168f3c16`**:
- `notes/DIRECT_ANSWERS_TO_OWNER_20260920.md` — the direct-answer digest that FIRST reported the null-finding (**recursive self-reference**).
- `notes/ORCH_BOOT.md` — R-6 boundary regen for CP-STALENESS-CEREMONY seal narrative (mentions Step 2 opens next).
- `phase0/credential_drop_manifests/20260920T0856Z_owner_drops_manifest.json` — Principal-Model-Spec drop manifest cites the trace-don't-bank ruling in its `owner_directive_verbatim_anchor` field.
- `STATE/NEXT.md` — R-68/R-69/R-70 markers referencing the trace as an in-flight or upcoming step.
- `STATE/DECISIONS.md` — owner disposition + plan-approval + Commit-B banking sections + Step 5-6-7-8-9 execution-order listing.

None of these predate the trace itself; each is either the report of the null-finding or the instructions to perform the trace. **They cannot be the origin of the phantom citation** — they are the reaction to the question about it.

### §3.4 · STATE "surface copy" 3 hits — 2026-08-25 Solva/Solver vocabulary correction (unrelated)

- `STATE/DECISIONS.md:1177` — OWNER CORRECTION 2026-08-25: *"Solva not Solver. The reasoning faculty's name is SOLVA — everywhere. Apply now, before CP3 lands: backend package is services/solva/ … test names, receipt kinds, purpose IDs …, surface copy, and any register/notes references all say Solva."*
- `notes/w5_grounding_brief.md:5` — cites the 2026-08-25 correction verbatim.
- `notes/close_report_template.md:52` — makes the Solva-vs-Solver vocabulary check a standing close-report line.

**Verdict:** Different date (2026-08-25), different concept (naming discipline for one atomic word), different owner ruling — fully cited to a REAL, banked, dated owner correction. **Not the phantom.**

### §3.5 · CODE "MUST … surface" grep — all legitimate

Sampled hits: `rehome.test.js:677/851/863/1008` ("internal wave names must never appear on the user surface" — A1 wave-name-hiding canon), `salvage/askconsole_retirement_2026-07-31/RETIREMENT_NOTE.md:5` (canon shell root ruling — Owner never lands on a pre-canon surface), `memory/PRD.md:186` (SYSTEMIC gate registry surfaces), `memory/ORCHESTRATOR_CONTINUITY.md:58` (DPO wizard_transcript held-class enumeration surface — Phase 8 Stage B-5a), various registry AST guards and Phase-8 stage-A gates. **All cite named canon anchors (A1, §6.3, UI Spec v2.2, canon retirement note, held-class registry, etc.). None cite "2026-09-08 surface language".**

## §4 · The five dated 2026-09-08 directives — inventory (none carries a "surface language" rule)

Each authoritative 2026-09-08-dated owner directive is verified in-place at `STATE/DECISIONS.md`. Confirmed scopes:

1. **`2026-09-08T~04:20Z` (l.6424)** — OWNER DIRECTIVE · Compaction-proof discipline · STANDING_ORDERS.md chartered. Scope: SO §1-§6 headers, pointer wiring, invariant tests. **No surface-language content.**
2. **`2026-09-08T~04:40Z` (l.6468)** — Master Requirements Traceability Audit LANDED (deliverable + per-source detail files). **No surface-language content.**
3. **`2026-09-08T~04:50Z` (l.6513)** — OWNER DIRECTIVE · W-WINDOW-FILL-RESTORE-2 AUTHORIZED (training-window scheduling: 12h aisca chunks, chained dispatcher launcher, quiet log discipline). **No surface-language content.**
4. **`2026-09-08T~05:15Z` (l.6532)** — OWNER DIRECTIVE · MISSION-FRAMED REPORTING · 4 artifacts drop. Scope: reporting shape (4 sections: what-we-are-building / verified gaps / missing requirements / generate-to-close). **No surface-language content.**
5. **`2026-09-08T~06:15Z` (l.6561)** — OWNER DIRECTIVE · Pipeline defect challenge + new drop + rulings (STEP 1-5: literal-grep audit → new-drop ingest → 5-ratified-9-defaults-1-coupled-4-open rulings → master-audit rebuild → W-REGISTRY-FULL-BUILD from clean floor 3006 · prototype v3 = binding design; Doc 0 v2 = binding). **No surface-language content.** The prototype-v3-binding ruling lives in STEP 5 of this directive — which is why the owner's disposition ruled *"prototype_v3 binding: DATE-CORRECTED to 2026-09-08T06:15Z"* (Step 5 of this wave will land the date-correction erratum additively).

**None of the five carries any rule about "surface language". The scope of each is disjoint from copy/wording concerns.**

## §5 · Historical pickaxe — one authoring event only

`git log --all -S "surface language"` returns **exactly one commit** in each of the three repos that carry `census_dimensions.md`: `a73a3ea` — *"docs(stage_a): census-dimensions mini-phase Stage A proposal (CD-E1..E4 Tier-1 · CD-E5 Tier-2 · Owner Message 565)"*. This is the authoring event of `census_dimensions.md` itself (Owner Message 565 asked for the mini-phase Stage-A proposal). The phrase entered the tree at that commit as a **common-noun rationale**, not as a citation to a 2026-09-08 ruling.

`git log --all -S "surface-language"` (hyphenated form) returns **zero commits in every repo**.

Akki-Executive-Core + Akki-Executive-Final: **zero history hits under any variant.** Quarantine excluded.

## §6 · Verdict — PROVENANCE FAULT CONFIRMED · null trace

**The "2026-09-08 surface language (owner ruling)" citation has NO origin anywhere in any of the 5 working locations or the quarantine.**

- Zero content ever added anywhere that reads as a rule with that name and that date.
- Zero commit ever authored such a ruling.
- The only tree occurrences are (a) two common-noun/compound-noun usages in `census_dimensions.md` (TF close §6 anchored) and `ui_1_stage_a.md` (UI Spec v2.2 §10 + A1.6 anchored), (b) the 2026-08-25 Solva/Solver vocabulary correction using "surface copy" as a compound noun, and (c) recursive trace-metadata (this-wave reporter documents).
- No prior document ever cited a "2026-09-08 surface language" rule as an evidence anchor for anything.
- No sibling repo (RMS-IQ-Core-2 · Akki-OS-V1 · Akki-Executive-Core) carries such a rule.
- No quarantined repo (Akki-Executive-Final) carries such a rule — **quarantine flag CLEAR.**

**Owner ruling honored (verbatim from disposition):** *"If it traces to nothing, that's the finding, and every place downstream that assumed this rule was real needs checking for what it did on that assumption."*

## §7 · Downstream-assumption audit (per owner ruling)

**Question:** does any downstream document, gate, spec, or piece of code reason as though a "2026-09-08 surface language" rule exists?

**Method:** grep across STATE + CODE + siblings for any file with a MUST / MUST-NOT / SHALL / rule / gate / attestation that would have depended on the phantom rule. Combined with a review of every file that mentions "surface language"/"surface-language" for citation-form usage.

**Findings:**

1. **No MUST / MUST-NOT / SHALL / rule / gate / attestation anywhere in the 5 locations invokes "surface language" as its evidence anchor.** All "MUST … surface" hits cite named canon anchors (A1 wave-name-hiding, UI Spec v2.2 §10 BINDING COPY, canon retirement note, held-class registry, Phase-8 stage-A gates, registry AST walkers) — none cite the phantom.

2. **The two common-noun/compound-noun hits (`census_dimensions.md:272` + `ui_1_stage_a.md:1049`)** cite TF close §6 + UI Spec v2.2 §10 + A1.6 — not the phantom. Their reasoning is grounded in real, banked anchors.

3. **The recursive-self-reference trace-metadata hits** are reports OF the null-finding, not products OF a rule that was assumed to exist. The owner's disposition, the plan-approval, the direct-answers digest, the ORCH_BOOT R-6 narrative, the Principal-Model-Spec drop manifest, the R-68/R-69/R-70 NEXT markers, the WAVE R-69 Step 2/8 references — every one of them treats the citation as an unresolved trace target, not as an established rule.

4. **No frontends work has been drafted yet.** The OS-prototype frontends card (Step 8) has NOT been authored — it is a scheduled upcoming step. Therefore no MUST-DO/MUST-NOT line has yet been drafted that could lean on the phantom. **Step 8 dependence-check gate can now be satisfied on its face: since the card has not been written yet, and there is no upstream rule to inherit, the card can proceed cleanly from Front End Integration Brief + banked rulings alone.**

5. **The DAP portal work is HELD (per owner disposition) by the auth/session/tenancy gap — not by §2.1 and not by the surface-language phantom.** No cross-dependency.

6. **The 2026-08-25 Solva/Solver vocabulary correction** is a real, banked, grounded rule that ADDRESSES a "surface copy" concern (all copy must say "Solva"). Any place that cites the phantom might have been intending to invoke *that* rule — but the audit reveals **zero such misfires**: every "Solva" application in the tree cites the 2026-08-25 correction correctly.

**Verdict:** **NO DOWNSTREAM ARTEFACT DEPENDS ON THE PHANTOM RULE.** No corrections required in-tree. No gate to invalidate. No drift to reverse. The provenance fault is CONTAINED — it never propagated into any binding claim, MUST-DO, MUST-NOT, gate, test, or downstream ruling.

## §8 · Consequences for WAVE R-69 remaining steps

- **Step 5 (Mechanical Errata Seal · additive):** independent of the phantom · **proceeds this-turn.**
- **Step 6 (G5 continuation · DAP-numbered mappings unprovisional now):** independent of the phantom · **proceeds.**
- **Step 7 (α-gap hardening wave · TrustReceiptV1 + OuterGateReceiptV1 → SO §3.10-α frozen=True):** independent of the phantom · **proceeds.**
- **Step 8 (OS-prototype frontends card):** dependence-check GATE per owner ruling — **CLEAR** on this trace. The card has not been drafted yet; when it is, it will derive cleanly from Front End Integration Brief + banked rulings; no line will lean on the phantom. **Step 8 may proceed** when reached in sequence.
- **Step 9 (Principal Model Wave):** independent of the phantom (auth/session/tenancy + principal-store + credential-plane scope) · **proceeds** when reached, with interlude-marker discipline if budget insufficient.

## §9 · Owner-visible summary (mission-framed)

- **What was being checked:** whether a "2026-09-08 (owner ruling) — surface language" citation has any real origin anywhere in the workspace or its five repos (including quarantine).
- **Verified gap:** the citation is a phantom. Zero grep hits for the phrase as a citation; zero commits that authored such a rule; zero downstream document/gate/spec/test that acted on the assumption the rule exists; zero drift or misfire found in the audit. The 5 real 2026-09-08 directives all cover disjoint scopes (compaction discipline · traceability audit · window-fill authorization · mission-framed reporting · pipeline defect+drop).
- **Missing requirement:** none. The absence itself is the finding.
- **Generate-to-close plan:** bank this trace report and the null-finding + downstream-assumption audit at `STATE/DECISIONS.md` and `STATE/NEXT.md` R-71. Do NOT invent an owner ruling to bank. Continue WAVE R-69 execution order immediately: Step 5 (mechanical errata seal), then Steps 6+7 in interleave, then Step 8 (dependence-check clear on this trace), then Step 9. **Owner sees this report; if the owner recalls the ruling from an off-record channel, the ruling gets banked from that source with the correct date at any time — this null-finding does not preclude that later banking.**

## §10 · Anti-slop note

Every claim in §2, §3, §5, §7 is grounded in a specific file:line or `git log -S` result taken at this-turn in the terminal. No inference. No paraphrase of an unread source. If a claim about "no downstream lean" is wrong, it fails at the file that would have carried the lean — and I invite the owner to name any such file for verification. The audit does not shift the burden of proof onto the owner: it puts every negative claim on a specific file:line ANCHOR of the audit result.

**End of trace report.**
