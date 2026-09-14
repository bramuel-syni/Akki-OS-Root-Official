READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M3 · Block-close manifest — 2026-09-14T09:24Z

**Block:** M3 · Assurance & Safety Surfaces.
**Scope per `MILESTONE_PROMISE_BINDING_20260913.md §M3`:** W-WATCH-STACK · W-AGENT-CONTAINMENT · W-PRUNING-UNLEARNING · (W-REGISTRY-FULL-BUILD CP10 held).

## Sub-wave ledger

| SW | Wave | Canon | Ratchet | Notes |
|---:|---|---|---:|---|
|  1 | Flag-2 tight-budget defensible-write | Doc-0 Attr-7 · owner directive 2026-09-13 | 3714→3719 (+5) | ReliableClock write-boundary refuse |
|  2 | W-WATCH-STACK core · four-rung ladder | Doc-0 §7 · BR-7.1 · BR-7.4 | 3719→3725 (+6) | Learned→Deterministic gate |
|  3 | Watch Learning L-1/L-2 · certificate library | Watch_Learning_Amendment_v1 L-1/L-2 (A5.19 · A5.20 · RBM-23) | 3725→3732 (+7) | S-7 spec close begins; R-15/R-16 markers |
|  4 | Watch Learning L-3 · mirage as certificate ground | Watch_Learning_Amendment_v1 L-3 (A5.21) + DAP-32+ | 3732→3740 (+8) | Mirage provocation battery |
|  5 | Watch Learning L-4 · research queue | Watch_Learning_Amendment_v1 L-4 (A5.22 · A5.7+) | 3740→3746 (+6) | S-13 seam; AC-16 |
|  6 | Watch Learning L-5 · capability admission | Watch_Learning_Amendment_v1 L-5 (A20.16 · AC-17 · AC-18) | 3746→3753 (+7) | S-29 landing; R-17 marker |
|  7 | W-AGENT-CONTAINMENT AC-1..AC-12 | `agent_containment_spec_v1` AC-1..AC-12 | 3753→3759 (+6) | narrow-start + ContainmentEnvironment |
|  8 | W-PRUNING-UNLEARNING | `Pruning_Unlearning_Amendment_v1` DAP-37 · DAP-38 | 3759→3765 (+6) | S-26 discharge; R-12 marker |
|  9 | SIA V-3 · AC-13 + AC-14 | `Serving_Integrity_Amendment_v1` §C V-3 | 3765→3772 (+7) | Session-freeze contain; SFP-8-conforming path |
| 10 | BCA · S-10/S-11/BC-1/BC-2 verbatim pin | `Business_Continuity_Annex_v1` §1/§2/§3 | 3772→3782 (+10) | 3600 s + 72 h + quarterly cadence + countersigner independence |
| 11 | DAP-33/DAP-34/DAP-35 M3-remainder pin | MPB §M3 · R-8/R-11 baseline_period + R-7 BLOCKED | 3782→3790 (+8) | S-22/S-23/S-25 M3 remainder canon anchors |
| 12 | M3 block-completion composite pin | MPB §M3 verbatim | 3790→3797 (+7) | Every close-note + every PENDING-OVERRIDE marker + ratchet_history coherence + S-24 honest gap |

**M3 total delta:** 3714 → **3797** (+83 across 12 sub-waves).
**M3 discipline:** strict tests-first RED-before-mechanism held on every sub-wave (SW12 included).  Every sub-wave has its own mechanical RED log, byte-identical double-green, Rider 1 (pip freeze + collect-only), two-commit local (track-a code + master state), no push.

## Promises discharged (verbatim citations)

* **S-7** (Watch Learning) — spec closed via SW3/SW5 (A5.20 deterministic gate + A5.22 research queue).
* **S-10** (Ledger continuity RTO 3,600 s) + **BC-1** (countersigner independence) + **BC-2** (quarterly DEFAULT cadence) — pinned in SW10 to Wave E CP-E1 CA1-N5 mechanism.
* **S-11** (Breach notification 72 h) — pinned in SW10 to Wave E CP-E2 CA1-N2 mechanism.
* **S-22 (DAP-33)** · **S-23 (DAP-34)** · **S-25 (DAP-35/36)** M3 remainders — SW11 canon-anchor pin over M1 mechanism; R-8/R-11 baseline_period + R-7 BLOCKED preserved.
* **S-26** (Pruning · DAP-37/DAP-38) — SW8 mechanism.
* **S-27** (Serving integrity) — SFP-8 gate at M2 SW6 composed with AC-14 at SW9.
* **S-28** (Verdict certificate) — SW3 A5.19 schema + A5.20 gate.
* **S-29** (Capability admission ceremony) — SW6 A20.16 register + AC-17/AC-18.
* **AC-1..AC-12** — SW7 mechanism.
* **AC-13** (session-freeze contain) + **AC-14** (SFP-8-conforming path) — SW9.
* **AC-15..AC-18** — folded across SW3 (AC-15), SW5 (AC-16), SW6 (AC-17/AC-18).

## Open items carried forward (silent flip forbidden by SW12 composite pin)

* **R-7** (estate release budget number) — BLOCKED on Security owner-input.  Mechanism marker `DEFAULT-PENDING-OVERRIDE` on both `disclosure_budget.DEFAULT_RELEASE_BUDGET` and `coalition.DEFAULT_ESTATE_WIDE_BUDGET`.
* **R-11** (coordination-signature threshold) — DEFAULT-class "baseline_period" per owner ruling 2026-09-08; canon anchor pinned.
* **R-8** (Watch reproduction-probe threshold) — DEFAULT-class "baseline_period" per same owner ruling; canon anchor pinned.
* **R-12** (Pruning re-derive vs recall for non-sharded runs) — DEFAULT-class re-derivation; `PENDING-OVERRIDE` marker on recall action.
* **R-15** (Certificate library initial seed) — SW3 marker preserved.
* **R-16** (Research-queue ratifier + cadence) — SW5 marker preserved.
* **R-17** (Capability admission class granularity + initial register) — SW6 marker preserved.
* **BC-3** (RPO) + **BC-4** (site-loss / off-site backup) — `DEFAULT-PENDING-OVERRIDE`.
* **S-24 (A5.17 raiser-held-to-target-conformance)** — canon anchor pinned in SW12; mechanism DEFERRED beyond SW11 (honest gap).
* **R-13** (SIA reference-validation cadence) — DEFAULT-class monthly; auto-ratified under C3 batch.
* **R-14** (SIA Colibri engine admission) — OPEN; deliberately unruled.

## Security / owner-side items still USER-VERIFICATION-PENDING

* `SEC-2026-09-12-01` — leaked HF token (owner-side rotation).
* `SEC-2026-09-13-T4-01` — JUMP password leaked in structure-inspection script.
* `SEC-2026-09-13-T4-03` — RADIO credential briefly captured in pty echo.
* `SEC-2026-09-13-T4-04` — DB password leaked (empty-header keyword-redaction miss).
* `SEC-2026-09-13-T4-05` — Partial AWS Access Key ID stem in on-disk filename.

None of these blocked M3 code+tests work; all remain awaiting owner-side rotation.

## Queued post-M3 tasks (not started)

* **Connectivity setup pass** (NAS SMB via tunnel or JUMP-install fallback · SSH Radio + Transcription server · Huawei OBS S3-compatible endpoint enumeration).  Deferred per owner directive 2026-09-14 ("don't interrupt E1").  Do NOT start until explicit owner GO relayed.
* **W-REGISTRY-FULL-BUILD CP10** wave-close — remains on owner HOLD; drafted close test still shelved-untracked.

## Stopped before M4 per owner standing order

The next active step (M4 · W-JOURNEY-ASSISTANT) is not opened this turn and is not scoped.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
