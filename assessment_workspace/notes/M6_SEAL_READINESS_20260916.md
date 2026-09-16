READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# M6 seal-readiness note · 2026-09-16T~16:45Z

**Owner directive verbatim (2026-09-16T~08:35Z):** *"M6/M8 seal-readiness notes: one compact note each stating exactly what single set of owner inputs stands between current state and the milestone seal."*

**Purpose.** State exactly what single set of owner inputs stands between the current state of M6 · W-M6-AUDIO-PLANE-V1-PRODUCTION-BUILD and the milestone seal. Nothing else.

---

## §1 · Current M6 state (from-disk verified at 2026-09-16T~16:45Z)

- **M6 opened** 2026-09-15T~17:50Z (per NEXT pin + `notes/M6_OPEN_REPORT_20260915.md` · Path α/β decision flagged).
- **9 sub-waves sealed** (SW1..SW9) across `services/audio_plane_v1/*` between 2026-09-15T~18:05Z and 2026-09-16T~03:20Z (approximate close chain per DECISIONS + ratchet_history).
- **1 sub-wave DEFERRED** (SW-10 · Full-training runs · verbatim owner ruling 2026-09-16T~03:08Z: "SW-10 DEFERRED-TO-CLOSE + M7 OPENS"; grounding brief pre-authored at `notes/M6_SW10_FULL_TRAINING_RUNS_grounding_brief.md`).
- **M6 verification walk COMPLETE** — CP-M7-W1-POST-8-VERIFICATION closed clean 2026-09-16T~07:10Z (M6 wave-window `b105aa0..7b45a89` · 28 CP commits · 253 file-scoped invariants pass in 2.19s · Path α clean · zero-delta · receipt at `phase0/m7_w1_post_8_verification/verification_receipt_20260916.json`).
- **Ratchet at M6 verification-walk close:** 4384.
- **Ratchet at M8 latest close (CP-M8-CTCC-1):** 4400.
- **Ratchet at M7 W9 CP1 close (this shift):** **4406** (Path C default corpus_deliverable_v1).

---

## §2 · The single set of owner inputs blocking the M6 seal

**Ruling #5 · Audio-Plane §5.3 + §6.3 + §7 release-gate lift** — three sub-verdicts required together (per RULING_LEDGER row 22 · reiterated verbatim in every Release-Gate seal since 2026-09-14):

| Sub-verdict | What owner rules | Purpose in M6 seal |
|---|---|---|
| **kdpa_verdict** | KDPA compliance tier admission for the three release-gate categories currently refused-by-default: `biometric_embedding`, `named_identity`, `speaker_labeled_audio`. | Closes M6 §5.3 clustering + §6.3 P100 four-leakage-path harness release path. |
| **named_persons_verdict** | Named-persons tier admission at TOKENIZED / RESTRICTED / OPEN with tokens' custody policy. | Closes M6 §7 voice-verification enrolment corpus admission. |
| **transfer_basis** | Transfer-basis ruling for cross-perimeter carrier movement of any of the above tiers. | Closes M6 SW-10 full-training-runs release path (the deferred sub-wave). |

**Format expected** (per prior owner correction 2026-09-13): the ruling lands as three verbatim strings from a closed allowed-values set (values are specified in `notes/canon_dap_backend_spec_v1_requirements.md` R-15/R-16/R-17 canon extractions).

**Standing constraint held meanwhile** (verbatim owner reasserted this shift): *"no training on estate audio, no biometric material, no enforcement hard-gate, no speculative shapes beyond existing owner law."*

---

## §3 · What is NOT blocking M6 seal (from-disk verified)

- **M6 mechanism build** — 9/10 sub-waves sealed. Only SW-10 (Full-training runs) deferred, and SW-10 is DEFERRED not blocked-on-mechanism: it's blocked on Ruling #5 via §5.3/§6.3/§7 chain.
- **M6 platform-integrity verification** — CP-M7-W1-POST-8-VERIFICATION closed clean same-shift; 253 M6 invariants passing; zero cross-wave drift; append-only discipline verified across all 28 CP commits.
- **M6 sub-wave 5+6 (§5-§7 invention layer)** — Character Register + clustering + human-validation modules all landed (per W2..W9 triage §1 W5 row: `services/audio_plane_v1/{character_register,register_read_boundary,register_write_boundary,clustering,cluster_stability,human_validation}.py` all extant with +69 invariants combined).
- **M6 §14 P216 dedup-path** — CP-M6-2-2 seals it (4141→4150 · +9 invariants).
- **M6 §4 ingest stages 1..4** — all four pluggable seams sealed (language ID · code-switch detector · channel condition profiler · synthesis attribute capturer · +29 invariants combined).
- **M6 §5 Character Register schema (§5.1 + §5.2 four layers)** — CP-M6-3-1 seals it (+7 invariants).
- **M6 §6.3 P100 four-leakage-path harness framework** — CP-M6-3-2 seals it (+8 invariants · synthetic-fixtures-only).
- **M6 §13 commission view** — CP-M6-9-1/9-2 seals it (+16 invariants · V119c internals-projection refusal + V121 modality leaf + V122c reads-only allow-list defence).

---

## §4 · One paragraph · exactly what the owner needs to do

**Land the Ruling #5 three-sub-verdict ruling** (kdpa_verdict + named_persons_verdict + transfer_basis) as verbatim strings from the closed allowed-values set specified in canon `DAP_Backend_Spec_v1` §R-15/R-16/R-17. That single ruling unblocks:

1. SW-10 (Full-training runs) — the last deferred sub-wave of M6.
2. §5.3 clustering release-gate path.
3. §6.3 P100 harness release path.
4. §7 voice-verification enrolment corpus admission path.

After the ruling lands and SW-10 seals under §3.3 protocol, M6 seal is authorable as a wave-close report of shape identical to prior wave-closes (5 sections END-OF-WAVE format) with the M-family verification-walk backbone (`notes/M7_VERIFICATION_ROLLUP_20260916.md` §1 wave-window verification table row for M6) as the platform-integrity story.

**Nothing else is blocking.** No engineering work, no unratified design, no missing carrier, no missing invariant. One owner ruling.

---

## §5 · Wave-honest limits

- **W.1** SW-10 grounding brief is pre-authored at `notes/M6_SW10_FULL_TRAINING_RUNS_grounding_brief.md` — the mechanism can be authored tests-first the moment Ruling #5 lands, without further owner input.
- **W.2** SW-10 will consume the corpus_deliverable_v1 shape SEALED this shift at CP-M7-W9-CONTRACT-1 (Path C default in force per §C.2; upgrades to Path A/B ride the same Ruling #5 sub-verdicts).
- **W.3** M6-open Path α/β decision (per `notes/M6_OPEN_REPORT_20260915.md`) does not add a second blocker — Path α-pending was the default already exercised through all 9 sealed sub-waves.

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
