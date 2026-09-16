READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W6 verification note · DAP sale surface (R-6/R-7 bindings) · 2026-09-16T~17:25Z

**Owner directive verbatim (2026-09-16T~08:35Z):** *"FIRE whatever is BUILDABLE-NOW or PARTIALLY-BUILDABLE, in dependency order."*

**W6 status per M7 W2..W9 triage §1:** ⚠ **PARTIALLY-BUILDABLE / MOSTLY-DONE** — R-7/R-15(a)/R-16(a) already discharged; R-6 pricing carrier remains blocked. This verification note documents the extant modules and pins R-6 pricing as the single remaining owner-input.

---

## §1 · Charter mapping (W6 → extant modules)

**W6 charter:** DAP sale surface (R-6 pricing · R-7 disclosure budget).

| W6 clause | Ratified status | Extant module(s) |
|---|---|---|
| **R-7 PILOT_OPEN** | ✅ Ratified 2026-09-15 in W-RELEASE-GATE-PILOT-LIFT (owner ruling verbatim: R-7 PILOT_OPEN). | `services/release_gate/release_ledger.py` (`record_debit`) + `services/audio_poc/release_gate.py` (`admit_transcript_release_pilot_open` composition wired at CP-RG4). |
| **R-15(a) TOKENIZED** | ✅ Discharged same wave (2026-09-15). | `services/audio_poc/release_gate.py` (tokenized-named-persons composition). |
| **R-16(a) DERIVATIVE_ONLY_VIA_PULL_SEAM** | ✅ Discharged same wave (2026-09-15). | `services/audio_poc/release_gate.py` (derivative-only pull-seam composition). |
| **R-7 disclosure budget** | ✅ Discharged. | `services/dap/disclosure_budget.py` + `services/dap/metering.py`. |
| **R-6 pricing** | ❌ **OWNER-DESK P2 (BLOCKED-ON-OWNER-INPUT)**. | Not yet authored. |

---

## §2 · POST-2 from-disk existence check (this verification)

From-disk verified 2026-09-16T~17:25Z at track-a HEAD `757c0c5a407cd6ddf0472ff2eda88a5eecfa1a7b`:

- `services/release_gate/release_ledger.py` EXISTS.
- `services/audio_poc/release_gate.py` EXISTS.
- `services/dap/disclosure_budget.py` EXISTS.
- `services/dap/metering.py` EXISTS.

All 4 modules present. POST-2 CLEAN for the discharged clauses.

---

## §3 · The single owner input blocking W6 full seal

**R-6 pricing carrier ruling.** Owner needs to land the pricing shape for the DAP sale surface. Format expected: a frozen carrier with `price_unit_ref: str` (opaque · case-agnostic) + `price_amount_minor_units: int` (non-negative) + `currency_ref: str` (opaque). Runtime enforcement fires only when caller invokes (preventive-charter pattern matching CP-M8-CTCC-1).

Until R-6 lands, W6 remains in PARTIALLY-BUILDABLE state: R-7/R-15(a)/R-16(a) closed via existing modules; R-6 pricing carrier chartered-forward.

---

## §4 · Verdict

**W6 CHARTER 3/4 SATISFIED via extant modules.** Remaining 1/4 (R-6 pricing) is BLOCKED-on-owner-input. No new W6 CP authorable this-shift; R-6 pricing carrier will be authored the moment the ruling lands (matches CP-M8-CTCC-1 preventive-charter pattern).

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
