# M6 Sub-wave 10 · W-M6-FULL-TRAINING-RUNS · grounding brief

# ⚠️ MANDATORY HALT-TO-OWNER AT SUB-WAVE OPEN ⚠️

**No CP-M6-10-* work fires until the owner rules on real-estate audio access.**  This grounding brief exists to surface the halt, enumerate the concrete decision surfaces, and STOP.

---

**Opened at UTC:** 2026-09-16T~03:07Z
**Canon scope:** Audio Intelligence Plane §11.6 (full training runs).
**Track-a HEAD at open:** `7b45a89014c75610d61dbee876909d77ec82749d` (CP-M6-9-2 · Sub-wave 9 close).
**Master HEAD at open:** `89371cddc618060a840a322e9bb20bf7cb05d2e6` (§3.3 · CP-M6-9-2 Commit B · fixup at Commit C).
**Ratchet floor at open:** 4358 (verified on disk).
**M6 §15 walk position:** 10 of 10 sub-waves (final).
**HALT trigger reference:** M6 §E.5 HALT boundary (real estate voice/biometric material · SO §2 ratified HALT-TRIGGER 2026-09-15T~19:07Z verbatim, banked in STATE/NEXT.md line 1479).

---

## §A · HALT surface — concrete decision surfaces for owner ruling

The M6 §E.5 HALT is triggered when *"a §6.3 P100 harness scenario, a §5.3 clustering step, or a §7 verification path would call for actual estate audio, embeddings, or per-speaker enrolment corpora"*.  §11.6 full training runs cannot proceed without touching one or more of the following surfaces:

### A.1 · Estate audio corpus scope (§4.1 language IDs · §4.3 channel classes)

**Question for owner:** Which estate audio corpus is in-scope for the first full training run?

- **Option A · Single-language single-channel small corpus** (e.g., studio · single language ID · single condition class).  Simplest.  Serves as calibration training only; extrapolation to full production is a follow-on.
- **Option B · Full-language full-channel corpus per §4.1 P059..P062 + §4.3 P066..P068 vocabulary** (studio / field / telephone band × all resident language IDs · all detected code-switch patterns).  Full canon coverage.  Highest §6.3 P100 four-leakage-path exposure.
- **Option C · Chartered small-real-material fixture** (e.g., a small owner-authored subset with §6.4 P102 read-scope enforcement · synthetic + real interleaved).  Middle path.

### A.2 · Audio-bytes-retention path ruling (Path A/B/C · currently pending)

**Question for owner:** Which retention path applies to the training-run-output character stream + intermediate features + trainer state?

- **Path A · No estate audio bytes at rest post-ingestion.**  Character stream + Register + Codec artefacts only.  Training happens in-flight against the character stream; no audio bytes on trainer disk.
- **Path B · Time-boxed retention with §6.4 P102 read-scope enforcement.**  Bytes at rest for a bounded window (e.g., 24h) with automatic purge; read-scope conjunctive four-conditions enforced on every access.
- **Path C · Long-term retention under Watch/tamper-alarm surface.**  Bytes at rest indefinitely with §16 Watch tamper-alarm signing + external witness on every access.

### A.3 · §6.3 P100 four-leakage-path harness exercise mode

**Question for owner:** Is the §6.3 P100 four-leakage-path harness exercised against synthetic-only fixtures for the first full training run, or against a small chartered real-material fixture with §6.4 P102 read-scope enforcement?

- **Mode I · Synthetic-only** (matches CP-M6-3-2 discipline).  Harness proves the boundary; no real-material fixture crosses.
- **Mode II · Chartered real-material fixture with §6.4 P102 read-scope enforcement**.  Boundary tested against a small owner-approved real fixture; §6.4 read-boundary refuses on any leakage-path scenario.

### A.4 · Trainer host + custody path

**Question for owner:** Which GPU host (akki-vm · akki-vm-ii) is authorized for the first full training run, and does the JUMP root credential rotation to JSON (SEC halt) block the training initiation?

- The current SEC halt suspends boundary probes.  Whether training-run initiation is also blocked by the same halt is an owner call: training can run without probe verification (probes are observational after the boundary is set, not gating), but the audit trail is weaker.

---

## §B · Discovery on §11.6 canon coverage

Note: at authoring time of this brief, `Akki_OS_Audio_Intelligence_Plane_Specification_v1_0.txt` was checked for a §11.6 header.  A search of the file returned §11.1 (P171..P178 · CP-M6-7-2), §11.2 (P179..P180 · CP-M6-8-1), §11.3 (P181..P182 · CP-M6-8-2), §11.4 (P184..P188 · CP-M6-7-3) — but a bare §11.6 header was not immediately located in the canon text file.  **This may indicate that §11.6 is a placeholder in the M6 grounding brief that resolves to a canon section under a different numbering** (candidates: §11.5 P189..P192 · §11.6 P193..P196 · §14 · §15).  Owner ruling on which canon section governs "full training runs" is a fourth decision surface:

### A.5 · §11.6 canon-section resolution

**Question for owner:** Which canon section governs "full training runs" if §11.6 is a placeholder?

- **Option 1 · §11.5** (or whatever the canon paragraph immediately after §11.4 P188 is).
- **Option 2 · §15** (build sequence · full-training-runs as a build item).
- **Option 3 · Amendment or supplementary spec** (e.g., Training Capacity spec at `notes/canon_training_capacity_v1_requirements.md` if such a note exists).

This resolution ruling is required before any invariant text can be authored verbatim.

---

## §C · What lands if owner rules

If the owner rules with a concrete section and Options A/B/C/I/II, sub-wave 10 walks as:

1. **CP-M6-10-1 · Training-run manifest carrier + refusals** (opens SW-10).  Ratified inputs from owner ruling → frozen manifest dataclass.  Refuses on scope drift.  Composes with CP-M6-8-1 CalibrationOutput + CP-M6-8-2 MilestoneList + CP-M6-9-1 CommissionViewSnapshot.
2. **CP-M6-10-2 · Training-run initiator seam + §6.3 P100 real-boundary invariants** (mid).  Pluggable seam for the trainer; harness at real boundary if Mode II; synthetic-only if Mode I.  §6.4 P102 read-scope enforcement wired.
3. **CP-M6-10-3 · Training-run completion + spend/quote reconciliation** (closes SW-10).  Composes with V113e CI-mandatory · V118 CostQuoteWithCI · V122 reads-only Commission View update at run-close.  Ratchet target: +25..+35 across three CPs.

If the owner does NOT rule, sub-wave 10 remains at the HALT indefinitely.  M6 remains at 9/10 sub-waves closed · ratchet floor 4358 · no code lands.

---

## §D · What this shift DOES bank

- This grounding brief (surface the halt).
- Owner-desk items in DECISIONS + NEXT (already updated by CP-M6-9-2 seal).
- The four decision surfaces above · verbatim in this brief for the owner's next turn.

**This shift DOES NOT bank:**

- Any test file for CP-M6-10-*.
- Any mechanism file under `services/audio_plane_v1/` for CP-M6-10-*.
- Any ratchet bump beyond CP-M6-9-2's 4358.
- Any boundary probe beyond #61.
- Any code commit on `programme/track-a` beyond CP-M6-9-2's Commit A.

---

## §E · Wave-honest limits (surfaced now for the owner's decision)

1. **The mid-turn Codec-choice decision (§13 line 193) is unresolved.**  Canon §14/§15 (v1.0 baseline) proposal is adopt-open-codec; owner may override with train-estate-specific.  A codec choice ruling is intertwined with SW-10 A.1 corpus scope but is not the primary SW-10 gate — the gate is real-estate audio access.
2. **The mid-turn cluster-naming-validation decision (§13 line 192) is unresolved** (owner: commissioned internally OR delegated to external evaluation partner).  Not gating SW-10 directly but interacts with §5.3 clustering step outputs.
3. **The mid-turn wizard-B-2/B-3-landing-state decision (§13 line 188) is unresolved** (extend existing state machine OR stand sibling).  Not gating SW-10 directly.
4. **§14 Interface Summary line 200 is blank** — the canon text file's §14 header carries "Item" / "Specification" / "Service" fragments, suggesting a table that may be extracted incompletely.  If the owner rules on SW-10 and a §14 table is later confirmed to carry SW-10-relevant contracts, sub-wave 10 walk may need one additional CP for §14 verbatim contract enforcement.  Flagged for owner awareness.

---

## §F · Owner-desk items outstanding (unchanged by this HALT)

- **SEC incident ratification** in `STATE/DECISIONS.md` (`sec_incident_jump_cred_leak_20260915T222935Z`).
- **JUMP root credential rotation** (+ optional custody-format migration from CSV to JSON).
- **Admin SG binds for CD + Visitors** + NAS-username spelling correction (`bramuel` vs `bramwel`).
- **BC tier selection · DAP R-2/R-3/R-6 · Rules-Service R-2 · Watch-Learning R-15(b)/16(b)/17(b) · S-24/S-27/28/29 build charters · D9 receipt-unify · Amendment 8 HOLD · SEC rotations · R-17(a) (non-blocking) · Audio-bytes-retention Path A/B/C · D10 · D11 · WPW R-2 · R-14 candidate-serving-engine** — all unchanged from prior milestone-boundary reports.

---

## §G · Onward

**HALT.  Await owner ruling on §A.1..§A.5 decision surfaces.  No CP-M6-10-* work fires until ruling banked in DECISIONS.md.**

If owner does not rule this turn: shift closes with M6 at 9/10 sub-waves complete · ratchet floor 4358 · SW-10 chartered but held.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
