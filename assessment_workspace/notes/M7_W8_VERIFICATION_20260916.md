READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W8 verification note · Release-gate ADMISSIBLE lift (Ruling #5 verdicts) · 2026-09-16T~17:25Z

**Owner directive verbatim (2026-09-16T~08:35Z):** *"FIRE whatever is BUILDABLE-NOW or PARTIALLY-BUILDABLE, in dependency order."*

**W8 status per M7 W2..W9 triage §1:** ❌ **BLOCKED-on-<Ruling-#5 sub-verdicts>**. This verification note documents the ratified refusal surface + the exact Ruling #5 sub-verdict shape the owner needs to land.

---

## §1 · Charter mapping (W8 → extant refusal surface)

**W8 charter:** Release-gate ADMISSIBLE lift (Ruling #5 sub-verdicts: `kdpa_verdict` · `named_persons_verdict` · `transfer_basis` · biometric_embedding · named_identity · speaker_labeled_audio tier lifts).

**Extant ratified constraint (current refusal surface):**
- `services/audio_poc/release_gate.py` refuses tiers `{biometric_embedding, named_identity, speaker_labeled_audio}` by default per RULING_LEDGER row 22 (unchanged since 2026-09-14).
- Verbatim RULING_LEDGER row 22 status: Ruling #5 three sub-verdicts PENDING (reiterated verbatim in every subsequent Release-Gate seal).

---

## §2 · POST-2 from-disk existence check (this verification)

From-disk verified 2026-09-16T~17:25Z at track-a HEAD `757c0c5a407cd6ddf0472ff2eda88a5eecfa1a7b`:

- `services/audio_poc/release_gate.py` EXISTS AND contains the tier discriminators `biometric_embedding` / `named_identity` / `speaker_labeled_audio` (verified by `grep -l` on the module source).
- Refusal-by-default pattern is authored and gating.

POST-2 CLEAN for the refusal surface.

---

## §3 · The single set of owner inputs blocking W8 seal

**Ruling #5 three-sub-verdict landing** (matches M6 seal-readiness note §2 blocker):

| Sub-verdict | Allowed values (verbatim from `notes/canon_dap_backend_spec_v1_requirements.md` R-15/R-16/R-17 canon extractions) | What it lifts |
|---|---|---|
| **kdpa_verdict** | KDPA tier admission with owner-ratified custody policy. | `biometric_embedding` refusal-by-default. |
| **named_persons_verdict** | Named-persons tier admission at TOKENIZED / RESTRICTED / OPEN with tokens' custody policy. | `named_identity` refusal-by-default. |
| **transfer_basis** | Transfer-basis ruling for cross-perimeter carrier movement. | `speaker_labeled_audio` refusal-by-default. |

**Format expected** (per prior owner correction 2026-09-13): each sub-verdict lands as a verbatim string from a closed allowed-values set (values are specified verbatim in the DAP Backend Spec v1 canon extractions).

**Ratified refusal semantics stay in force until Ruling #5 lands.** This is the "no enforcement hard-gate" standing line held in reverse: the default is refusal, the lift is caller-invoked once the ruling is anchored.

---

## §4 · Verdict

**W8 CHARTER 0/3 SATISFIED and 1/1 REFUSAL-SURFACE SATISFIED.** The refusal surface is authored and gating; the lift is blocked on Ruling #5. No new W8 CP authorable this-shift; the tier-lift authoring will follow the Ruling #5 landings.

**Same blocker as M6 seal-readiness note §2.** Ruling #5 lands once → unblocks M6 seal + W8 seal + M7 W9 Path A/B upgrades simultaneously.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
