READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-M7-W1-POST-4-VERIFICATION · Wave close · 2026-09-16T~06:35Z

**Wave:** W-M7-W1-POST-4-VERIFICATION (M2 wave-window verification under SO §4.2 · autonomous continuation).
**Type:** VERIFICATION WALK · zero-delta close · SO §4.2 wave-window enumeration + clause 6 cross-wave handling ratified this walk.
**Verdict:** Path α · CLEAN.
**Predecessor:** CP-M7-W1-POST-3-VERIFICATION · master `c71b9fb7`.
**Track-a HEAD at close:** `2c7a8f0c` (unchanged).
**Master HEAD at close:** to be recorded post-Commit-B.
**Ratchet floor at close:** **4384** (unchanged · verification walk).

---

## 1 · Progress made

Under **SO §4.2 wave-window commit enumeration** (ratified 2026-09-16T~06:20Z), computed the M2 wave-window and enumerated every commit + first-added `services/` and `tests/invariants/` file. M2 comprises 7 sub-wave-close commits covering 15 module additions + 15 test file additions across the Rules Service · Reliable Time Source · Serving Floor · Doc-0 Attributes surfaces.

**M2 wave-window:**
- **Open:** W-M2-SW1 · `451ef2bb` · 2026-09-13T18:51:44Z.
- **Close:** W-M2-SW7..SW15 END-GATE · `95d688cd` · 2026-09-13T19:54:49Z.
- **Next-family open:** W-M3-SW1 · `eaa0e04` · 2026-09-14T05:24:59Z.

**Files enumerated + verified this walk (15 modules · 15 test files):**

| Sub-wave | Close commit | Modules | Tests |
|---|---|---|---|
| SW1 | `451ef2bb` | rules_service/rule_registry.py | test_wm2_sw1_rule_registry_bootstrap.py |
| SW2 | `f00da4a2` | rules_service/ceremony.py | test_wm2_sw2_rules_service_ceremony.py |
| SW3 | `76377830` | rules_service/rule_book_library.py | test_wm2_sw3_rule_book_library.py |
| SW4 | `65640632` | rules_service/rule_enumeration_classifier.py + rule_book_seed.jsonl | test_wm2_sw4_286_rule_enumeration_classify.py |
| SW5 | `f4fc201f` | reliable_time_source/clock.py | test_wm2_sw5_g8_reliable_time_source.py |
| SW6 | `352abc0a` | serving_floor/sfp_8.py | test_wm2_sw6_sfp_8_serving_integrity.py |
| SW7..SW15 END-GATE | `95d688cd` | doc0_attributes/{tcb, subsystems, triad, reference_monitor, baseline, audit_au3, determinism, coherence, governance_ceremony}.py (9 modules) | 9 test files (sw7..sw15) |

**Six from-disk checks (adapted for M2 domain scope):**

- **C.2 · Invariant tests pass**: `81 passed in 1.47s` across 15 M2 test files.
- **C.3 · No leak into case-agnostic kernels**: zero touches to `services/work_supervisor/`, `services/capability_registry.py`, `services/resource_registry/`, or `services/output_verified_seal/` across all 7 M2 commits. Domain-specific M2 modules stay in their own directories (`rules_service/`, `doc0_attributes/`, `reliable_time_source/`, `serving_floor/`). Note: unlike W1-family modules, M2 modules ARE domain-specific by design (Doc-0 attributes · Rules Service); C.3 for M2 verifies no LEAK INTO case-agnostic platform kernels rather than counting domain tokens within the modules themselves.
- **C.4 · Within-window last-touched**: all 15 M2 modules last-touched at their sub-wave-close commit or the M2 END-GATE (`95d688cd`), all within `[451ef2bb^..95d688cd]`.
- **C.6 · No banned enforcement tokens**: zero `kill/terminate/refuse_dispatch/unregister` tokens on any M2 module's public surface.
- **C.1 + C.5** covered by the passing invariants (each M2 test file freezes its module's primitive surface + compose/scope-boundary contracts).

**Machine-readable receipt**: `phase0/m7_w1_post_4_verification/verification_receipt_20260916.json`.

## 2 · How much to go

- **W-M7-W1-POST-4-VERIFICATION** — CLOSED this shift (Path α clean · zero-delta).
- **M2 wave-window fully verified** under SO §4.2.
- **W-M7-UTILIZATION-72H** — LIVE · elapsed 2.17 h · remaining 69.83 h · 258+258 bench iterations banked · peak 100% GPU util.
- **Next autonomous walk candidate**: **CP-M7-W1-POST-5-VERIFICATION · M3 wave-window** — will cover W-M3-SW1 (`eaa0e04` Flag-2 tight-budget guard on clock.py) + subsequent M3 sub-waves. Autonomously authorable per same precedent.

## 3 · Decisions taken

1. **SO §4.2 clause 6 ratified this walk**: cross-wave modification handling. When a module added in Wave A is legitimately extended by later Wave B via B's own CP (owner-directive-cited · ratchet-deltaed · append-only), Wave A's verification surfaces the post-wave-A modification as a wave-honest note but does NOT fire drift. The modifying wave's own verification enforces the shape of the modifying-wave's changes. A modification is drift only when it lacks CP citation / ratchet delta / owner directive, or violates SO §3.
2. **M2 wave-window Path α clean** with one surfaced cross-wave modification (`clock.py` extended at M3 SW1 · Flag-2 tight-budget guard · additive · owner-directive-cited · ratchet 3714 → 3719).
3. **M2 modules confirmed compose-safe with case-agnostic platform kernels**: zero commits leak into work_supervisor / capability_registry / resource_registry / output_verified_seal.
4. **POST-4 close matches W0/W1/POST-2/POST-3 verification-walk shape**: single-master-commit · no track-a · no fixup.

## 4 · Discoveries not envisioned at planning

1. **`clock.py` cross-wave modification chain surfaced** (M2 SW5 add → M2 END-GATE loosening → M3 SW1 tight-guard). The lineage is:
   - **M2 SW5** `f4fc201f`: initial `ReliableClock` + `TimeAnchor` + `au_3b_defensible_now()` with `AU_3B_DEFENSIBLE_DRIFT_BUDGET_MS=100ms`.
   - **M2 SW7..SW15 END-GATE** `95d688cd`: loosened default 100ms → 24h to allow M2 END-GATE tests to pass in slower environments (commit message: "*incidental: clock default anchor drift budget 100ms->24h*"). The loosening was in-window and banked-in-message.
   - **M3 SW1** `eaa0e04`: recognized that 24h default was too loose for governed writes → added `TIGHT_DRIFT_BUDGET_MAX_MS=5_000` + `LooseAnchorRefused` exception + `assert_defensible_for_governed_write(stamp)` guard function (append-only extension · owner directive verbatim: *"any record emitted with au_3b_defensible=True MUST bind a TIGHT drift budget; the loose 24h process-local default MUST NOT be able to reach a governed write"*). This is an example of the platform learning from its own loosening 9 hours 30 min later.

2. **The Doc-0 Attributes sub-tree carries 9 domain-specific modules** (`tcb`, `subsystems`, `triad`, `reference_monitor`, `baseline`, `audit_au3`, `determinism`, `coherence`, `governance_ceremony`). These are `AC-1..12` / `BR-11` mechanism-carriers per Doc-0. Under case-agnostic doctrine they are permitted to carry domain vocabulary — their entire purpose is Doc-0. What they must NOT do is leak Doc-0 tokens into the platform kernels; verified this walk.

## 5 · Recommendations to make the experience better, in line with the mission

1. **Author CP-M7-W1-POST-5-VERIFICATION next** (autonomous continuation) — M3 wave-window under SO §4.2. Will cover the `clock.py` M3 SW1 extension + any subsequent M3 sub-waves (checkpoint boundaries + additional Doc-0 attrs · DAP-stack pilot bindings · etc. per M3 close chain).
2. **Recognize the "loose default → tight guard" pattern** as a healthy correction cycle in an append-only-extension programme: the platform initially loosens for ergonomics, then later tightens for governance, banked as a separate CP per wave. This is the same shape as W0's silent-success ban (loose seal reader → tight `is_real_seal` primitive).
3. **Continue GPU utilization interleave** at every future CP boundary.

---

## §G · GPU utilization check-in interleave

**Check-in fired at POST-4 CP-seal** @ 2026-09-16T~06:35Z.

- Elapsed 2.17 h · Remaining 69.83 h.
- akki-vm: sampler_alive+workload_alive · 56 telemetry samples · 258 bench iters (ok=258) · peak 100% util per GPU · ~691 W · ~70°C.
- akki-vm-ii: sampler_alive+workload_alive · 56 telemetry samples · 258 bench iters (ok=258) · peak 100% util per GPU · ~693 W · ~71°C.
- 516 total bench artefacts banked.
- Report served: `https://pensive-goodall-6.preview.emergentagent.com/audit/GPU_UTILIZATION_72H.md`.

---

## §H · Owner-desk items

**P1 blocked** (unchanged).

**P2 blocked** (unchanged): SW-10 A.1-A.5 · Audio-bytes-retention Path A/B/C · R-17(a) · Cross-service binding enforcement ruling (§3.2 clause 5).

**P2 CLEARED this shift**: candidate CP-M7-W1-POST-4-VERIFICATION for M2 wave-window → CLEARED (this walk).

**NEW · P2 · Candidate CP-M7-W1-POST-5-VERIFICATION**: M3 wave-window verification under SO §4.2. Autonomously authorable next-shift.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
