READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# BUILD_STRATEGY_20260913.md

**Standing.** Supersession-form delta over `/app/assessment_workspace/BUILD_STRATEGY.md` (Aug-14, 250,939 B). Aug-14 original preserved unchanged. This file records M0-canon-delta impacts on the build strategy without rewriting the full plan.

**Precedence.** Delta rows here supersede Aug-14 rows referencing the same wave/CP/service. Silent-in-delta rows carry the Aug-14 strategy unchanged.

**Scope of delta.** Structural additions to the plan post-Aug-14: M0..M5 milestone spine (owner-ratified 2026-09-13) · Phase_C_Systematic_Build_Plan (W-REGISTRY-EXTENSION-G3, W-SOLVA-V2-LIFT, W-DAP-STACK) · Serving_Integrity_Amendment fold-in · C3 batch ratification · sequencing adjustment (Registry+DAP CLOSE BLOCK = M1 with CP10 + G-3 pulled forward).

---

## §A · M0..M5 milestone spine (verbatim from `MILESTONE_PROMISE_BINDING_20260913.md`)

- **M0** — canon-delta extractions + supersession-form deliverables + book-keeping refresh. **Discharges no runtime promise; discharges SO §2 engagement discipline + Canon-1 §4.11.**
- **M1 · Registry+DAP CLOSE BLOCK (owner-adjusted 2026-09-13)** — W-DAP-STACK 2A..2H (DAP-1..DAP-30 core; DAP-31/32+ conformance with SFP-8 dependency marker) PLUS pulled-forward Registry CP10 real-Chromium DOM proof PLUS G-3 full-closure remainder. **Discharges DAP-Spec §9 A1..A9 fully; A10 partial (remainder in M5); Promise #4/#22/#25; Doctrines §4.1/§4.9/§4.11; S-22/23/25 partials.**
- **M2** — Rules-Service (4 sub-waves) + 7 remaining Doc-0 Attribute waves (Attr 1/2/3/6/7/8/10/11/12; Attr 4/9 rolled into Rules-Service). **Discharges Promises #22/27/29; Doc-0 Attrs 1-12; Amendments 6/7; SFP-8 admission; TCB serving-integrity-gate row; FP hash-mismatch row.**
- **M3** — Watch Doc-03 62-row mechanism + Pruning + Agent-Containment (AC-1..12 + AC-13/14). **Discharges S-1..S-27 (except S-7 gap); AC-1..AC-14; RBM-20; DAP-A10 (partial); S-10/S-11 recovery+notification.**
- **M4** — Assistant surfaces (W-JOURNEY-ASSISTANT candidate) + registered-handoff-contract generalisation. **Fully discharges Promise #32; Canon-5 §14; Canon-6 §3/§6/§12; DAP-20 boundary; A5.7+ receipt extension.**
- **M5** — Data-Suite-v2 donor lift + Audio-POC. **Discharges DAP-A10 remainder; Promise #12 (fully); Audio-Plane §1.2.**

## §B · Sequencing adjustment (owner-ratified 2026-09-13)

**Prior sequence** (from `PHASE_C_SYSTEMATIC_BUILD_PLAN.md` and `LEVERAGE_AND_GAP_INVENTORY_20260913.md §G.2`):
- M2 · W-REGISTRY-FULL-BUILD CP10 close
- M3 · G-3 full-closure remainder (Mtafiti-side asset-inventory generalisation, orphan)

**New sequence (M1 = Registry+DAP CLOSE BLOCK):**
- **M1 block = DAP 2A..2H → Registry CP10 (Chromium DOM proof) → G-3 full-closure remainder** — all inside the block, then STOP for BLOCK COMPLETION REPORT before M2 opens.
- Rationale: `[framing, not canon]` — the Registry and DAP surfaces compose the same custody rails (chokepoint · admission · trust-domain · metering · ledger); closing them together avoids interleaved half-states.

**CP10 HOLD status:** Marked **LIFT-BY-AUTONOMY-DIRECTIVE 2026-09-13** per the owner's autonomy authorisation this session — visible + reversible on record.

## §C · Ratchet floor progression (target, contingent on block execution)

| Point | Floor | Waves closed |
|---|--:|---|
| Start of session 2026-09-13 | 3562 | up to and including W-SOLVA-V2-LIFT |
| Post-M0 close | 3562 (unchanged; document-only) | — |
| Post-DAP 2A | +N (target) | +1 |
| Post-DAP 2H | +∑N | +8 |
| Post-CP10 close | +M | +1 |
| Post-G-3 remainder | +K | +1 |
| **Block completion target** | **~3562 + Σ (documented in block-completion report)** | +10 |

## §D · DEFAULT-PENDING-OVERRIDE markers to land tests-first in block

Per C4 ruling (5 OPEN owner-inputs → tests-first with markers):
- `SEC_R7_ESTATE_RELEASE_BUDGET = DEFAULT-PENDING-OVERRIDE` (blocks DAP-6 / SFP-6 / Attr-7 production-grade).
- `DAP_R2_APPROVING_AUTHORITY = DEFAULT-PENDING-OVERRIDE` (blocks DAP-14 named routing).
- `DAP_R6_PRICING_MODEL = DEFAULT-PENDING-OVERRIDE` (blocks DAP-22 pricing/billing production-grade).
- `WPW_R2_EXTERNAL_RELEASE_SIGNATORY = DEFAULT-PENDING-OVERRIDE` (blocks WPW Tier 3 · outside block).
- `RULES_R2_SECOND_SIGNATORY = DEFAULT-PENDING-OVERRIDE` (blocks Rules-Service ceremony R-2 · outside block, M2).
- `DAP_R3_PER_PARTY_CEILINGS = DEFAULT-PENDING-OVERRIDE` (COUPLED — dependent on Sec R-7).

Also per C5 (DPO-S2 reflection HALT stays):
- `SOLVA_V2_REFLECTION = HALT_NOT_IMPLEMENTED_ERROR` (Solva-V2 reflection.run() raises NotImplementedError until owner ratifies one of 3-5 candidates in `notes/DPO_S2_REFLECTION_CANDIDATES_20260913.md`).
- Any DAP row genuinely requiring reflection's semantic content carries a **declared dependency marker**, not a guess.

Also per SIA:
- `SIA_R14_COLIBRI_ENGINE_ADMISSION = DEFAULT-PENDING-OVERRIDE` (deliberately unruled; awaits appliance benchmark + TCB ceremony).

## §E · Flip-forbidden invariants (R-C1 / R-C2 / DPO-1 linkage) — carried per PHASE_C plan

- **R-C1**: `controlled_determination_basis = custody_class_fallback` (Rules-Service not yet built) → any test flipping this fails.
- **R-C2**: `au_3b_defensible = False` (reliable time source not yet built) → any DAP metered/timestamped row asserting `au_3b_defensible=True` fails.
- **DPO-1 linkage**: The `controlled` custody-class value maps to DAP R-1, not Document 4.

## §F · What has NOT changed from Aug-14 BUILD_STRATEGY

- Extraction-Akki remains the spine repo (84 services on `programme/track-a`).
- Two-commit local pattern preserved (track-a for code · master for state) NEVER push.
- SO §3 tests-first discipline preserved.
- Ratchet is monotonic.
- `testing_agent` BANNED — terminal pytest only under `BASELINE_GUARD=1`.

## §G · What HAS changed (delta summary)

1. Serving Integrity Amendment introduces SFP-8 conformance dependency + A5.7+ receipt fields + AC-13/14.
2. Security_Assurance_Promise_Set v2 adds S-27.
3. C3 batch ratifies 12 DEFAULT rows → RATIFIED.
4. M1 becomes the Registry+DAP CLOSE BLOCK (pulls CP10 + G-3 forward).
5. R-1/R-3/R-5 (Doc-0) self-flipped RESOLVED in files_15 delta.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
