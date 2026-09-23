# OWNER DROP — Ruling (b) AKKI-RUNS-IT + Standing Directive 1 ASSISTANTS-DIALOGUE + Standing Directive 2 GAPS-FIXED-LEDGER — 2026-02-23

**Banked verbatim per SO §6.8 owner-drop discipline + §6.9 desk discipline. Fold-in at current CP-AIP-9 boundary; do not interrupt in-flight seal.**

---

## 1 · Ruling (b) verbatim — Akki runs it; E1 wires then steps back

> "E1 to wire it into Akki's autonomy so Akki runs it, then step back."

**Binding architecture rule (protected-objective per §6.9 desk discipline: protects tenant custody + the principle that Akki is the autonomous doer, not the build pod).**

1. **ALL** Akki-based training and census **EXECUTION** runs **inside the live Akki OS system** — via the **Census Autonomy Service / commissioned-job path** — within the tenant compute + custody boundary (§6, §7, ENT-16 Managed compute / Frontier Your Keys). Training compute, model weights, and the labelled corpus **never leave Akki's boundary; no third-party export.**
2. **E1's role = build and WIRE the seams** (LID detection, corpus ingestion+pairing, admission gate, training-run contract) **INTO the Census Autonomy Service so Akki runs them autonomously — then STEP BACK.** E1's pod is **never the training host and never a data path.** The 10 GB Q3 trial was a one-off read-cost probe; **no repeat.**
3. **Concretely:** the Whisper-LID + VoxLingua107 detection pass, the google-transcripts corpus census, and the CP-AIP-10 training seam **must be registered as Census Autonomy Service jobs** (engine + response queue + data-source adapter that already exist from Phase 3), so the running Akki system **schedules and executes them — not E1 by hand.** E1 builds the **job definitions, invariants, and wiring;** Akki **executes on its own cadence.** Verify autonomy actually picks them up (a receipt showing the autonomy engine ran the job), then step back.

## 2 · Standing Directive 1 verbatim — Objective-shaping dialogue is the assistants' work

> "note the natural back and forth you and i are having when shaping the objectives and evolving it both for training and census. This is the work of the assistants in census and training."

**Bank this as a first-class design principle and card it (extend, do not parallel — §1.2).**

- The iterative owner↔desk conversation that **PROPOSES** an objective, **REFINES** it against constraints, **RECORDS** decisions/defaults, and **EVOLVES** it as new data/leads arrive — that dialogue **IS the intended behavior of the Census Assistant and the Training Assistant.**
- Extend the existing **Objective Wizard (CP-AIP-6, sealed)** agent-interface + the **Census Autonomy conversational surface** to embody this: an assistant that conducts exactly this shape-and-evolve exchange with a tenant/owner — surfacing options with rationale, banking each decision as a one-record ledger entry, carrying **§6.9 markers (unmeasured / INFERRED / honest-gap)** rather than refusing, and re-deriving the objective as leads land (e.g., the way the na7p4 cost lead, the Newvault pairing, and the google-transcripts corpus each reshaped the plan).
- **Card two objectives (on-ledger, owner-directed, not PARKED):** `CP-AIP-ASSIST-CENSUS` and `CP-AIP-ASSIST-TRAINING`. Each: the assistant runs inside Akki autonomy, proposes/refines/evolves objectives conversationally, and every turn is a receipted decision. RED-first pins that assert:
  - a proposed objective without a recorded rationale is rejected;
  - an evolved objective supersedes additively (nothing relabelled/rewritten);
  - markers-over-refusal is enforced.
- **Sequence these into the ledger after the current AIP/§6.9 wave; report the card drafts before building.**

## 3 · Standing Directive 2 verbatim — Fix gaps as we go

> "Owner asked whether we are fixing code gaps as we go. Answer in your next report with a GAPS-FIXED ledger: every invariant trip, drift, YAML/JSON hazard, and honest-gap you have closed this run (additively), each with its one-sentence protected objective. Keep this ledger current at every seal going forward. Confirm nothing is being papered over — honest-gap-never-fake."

**Requirement:** Maintain `STATE/GAPS_FIXED_LEDGER.md` — append at every seal boundary. Each entry: kind (invariant trip / drift / YAML-hazard / JSON-hazard / honest-gap), one-sentence protected objective, additive fix mechanism, receipt anchor.

## 4 · Application sequence (item-by-item)

- **(b) autonomy-wiring** — recorded in `EXECUTION_ORDER.md` as the **execution rule** for all Akki training + census work from this boundary forward. `E1 pod is a build pod, not a training/execution host.` LID / corpus census / CP-AIP-10 training all register as Census Autonomy Service jobs. Verification of autonomy pickup is exit evidence (receipt from the autonomy engine's run log).
- **ASSIST cards** — `CP_AIP_ASSIST_CENSUS.md` + `CP_AIP_ASSIST_TRAINING.md` drafted at this boundary (owner-directed, NOT PARKED — on the active ledger). Sequenced **after** the current AIP/§6.9 wave (SO-6.9 wave items e2–e6). Draft card_sha256 + minimum required-shape sections banked at this-boundary; ratification report in next report-and-continue per owner directive.
- **GAPS-FIXED ledger** — new file `STATE/GAPS_FIXED_LEDGER.md` seeded at this boundary with the entries closed during this-turn CP-AIP-9 seal (ORCH_BOOT desync, DECISIONS pointer, R-91 ε scaffolding retirement, four drift-annotation invariant retirements, YAML fence-close bug in ORCH_BOOT.md). Kept current at every seal going forward.
- **§6.9 desk discipline** — every fold-in above carries a one-sentence protected-objective annotation.

## 5 · Sequencing amendment (adds to §6.9 cadence)

- **In-flight (unchanged):** CP-AIP-9-COMMISSION-VIEW seal completion (State-B → C-fixup → /app-C → mini-bank) → CP-AIP-10-TRAINING-RUNS seal.
- **CP-AIP-10 REPORT-AND-CONTINUE** per §6.9 cadence amendment — REPORT includes ASSIST card drafts (per Standing Directive 1) + GAPS-FIXED ledger (per Standing Directive 2) + full-plane completion report (CP-AIP-1..10) with Q1/Q2/Q3 summary + pending owner actions + PARKED list. **Owner to review card drafts before building.**
- **SO-6.9 wave (after CP-AIP-10):** LID (wire into Census Autonomy Service, not run in-pod) → ENT-16 pilot licence seeds → private mirror → census three waves + tenant separation + CON-20/SFP-8 corrections → **ASSIST cards build (after owner ratification of drafts).**

## 6 · One-sentence protected-objective annotations (§6.9 desk discipline)

- **Ruling (b) autonomy-wiring** protects: tenant custody + the principle that Akki is the autonomous doer, not the build pod; training compute + weights + corpus stay within Akki's boundary; E1 never becomes a data path.
- **ASSIST cards on-ledger (not PARKED)** protects: the objective-shape-and-evolve dialogue as first-class assistant behavior (not incidental to the wizard); receipted-decision discipline for every turn.
- **GAPS-FIXED ledger** protects: honest-gap-never-fake discipline; every trip / drift / hazard / honest-gap closed additively is visibly banked with its protected objective; no silent papering-over.
- **Autonomy-pickup receipt as exit evidence** protects: measured verification that the running Akki system actually schedules and executes registered jobs (never claimed without receipt).

## 7 · Received / banked timestamps

- Owner drop received: 2026-02-23, mid-CP-AIP-9 seal (immediately after /app companion Commit-A `4d57db1a6` landed).
- Banked verbatim in this file: **this same boundary (CP-AIP-9-COMMISSION-VIEW pre-State-B).**
- Execution: **ASSIST cards drafted at this boundary; ratification requested in CP-AIP-10 REPORT-AND-CONTINUE.** Autonomy-wiring recorded as execution rule in EXECUTION_ORDER.md at this boundary.
