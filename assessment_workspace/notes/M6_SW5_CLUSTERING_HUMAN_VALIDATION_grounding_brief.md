# M6 · Sub-wave 5 · W-M6-CLUSTERING-HUMAN-VALIDATION · Grounding brief

**Wave:** W-M6-CLUSTERING-HUMAN-VALIDATION (M6 sub-wave 5).
**Canon anchor:** Audio-Plane v1.0 §5.3 · P089 · V59.
**Sequence position:** §15 P233 (row 5): *"Requires 1–4."* — sub-waves 1, 2, 3, 4 all COMPLETE as of CP-M6-4-4 seal 2026-09-15T~20:32Z.
**Grounding brief authored:** 2026-09-15T~20:37Z, this-shift.

---

## §A · Verbatim owner authorization (2026-09-15T~20:37Z)

> "Proceed to Sub-wave 5 — author the grounding brief with verbatim §5.3 anchors, then walk CP-M6-5-1..5-3 tests-first under the standing HALT boundary (synthetic fixtures only; the instant any mechanism needs real estate voice/biometric material, HALT to owner). Note for the human-validation loop CP: build the MECHANISM (sampling, validation record, verdict binding) — actual human validators binding real samples is a post-unblock owner activity; the mechanism must be provable with synthetic fixtures."

> "Your Discovery-1 recommendation is RATIFIED under the owner's standing 'requisite guardrails' mandate — it strengthens discipline with zero scope impact. Amend STANDING_ORDERS with the one-line post-seal receipt rule: 'No CP may be reported "sealed" in any summary or handoff unless BOTH commit SHAs (track-a Commit A + master Commit B) are recorded in the seal/DECISIONS entry.' Bank the amendment with this message as §A authorization." (Now STANDING_ORDERS §3.3 · in force.)

Standing HALT boundary carry-forward (owner ruling 2026-09-15T~19:04Z, still in force): synthetic-fixtures-only in tests; instant a mechanism requires real estate voice/biometric material to validate, **HALT to owner** — that is a genuine owner-input decision point per SO §1.

Standing carry-forward state (owner update 2026-09-15T~20:35Z): allowlist OWNER-TEMP-EXEMPTION (permissive) still in force; D10 LID backend still UNRATIFIED (pluggable-seam-until-ratified applies to clustering backend); Path α/β α-pending default for ingestion sources; 5 NAS audio-bearing shares + radio 10.10.55.x + dark channels + ActRecord null-audio all still parked owner-desk; BC packet, D9, Watch-Learning set, DAP R-2/R-3/R-6, sensitivity declarations, SEC rotations all still pending owner. Boundary-probe cadence stays every-CP (44+ consecutive CD/Visitors timeouts expected until admin SG opening lands).

---

## §B · Verbatim canon anchor (§5.3)

**Audio-Plane v1.0 §5.3 · P089 · V59 (verbatim on single un-wrapped line):**

> "Unsupervised clustering over the character stream yields candidate strata. A cluster asserts that a distinct variant exists — not what it is called. Naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost."

**Auxiliary verbatim clauses that bind sub-wave 5:**

- §15 P233 · V145 · TABLE-ROW-06: *"5 | Clustering + sampled human validation (§5.3) | Requires 1–4."* — prerequisite for open.
- §16.2 P249 · V157: *"Cluster naming validation: commissioned internally or delegated to an external evaluation partner where one exists (§5.3)."* — governs the human validation seam.

**Three distinct load-bearing clauses in P089 (each becomes a CP anchor):**

1. **"Unsupervised clustering over the character stream yields candidate strata"** — CP-M6-5-1 anchors here. Clustering runs over the character-register carrier from CP-M6-3-1 (`CharacterRegister.entries`, in the four `REGISTER_LAYER_VALUES`). Emits candidate strata.
2. **"A cluster asserts that a distinct variant exists — not what it is called"** — CP-M6-5-3 anchors here (cluster-stability invariant). A cluster's IDENTITY is "distinct variant exists", not a human-readable name.
3. **"Naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost"** — CP-M6-5-2 anchors here. Human-validation loop is a commissioned-work mechanism; the mechanism (sampling · validation record · verdict binding · quoted-cost pointer) is code, but the actual human bindings are owner-activity.

---

## §C · CP breakdown

### CP-M6-5-1 · Unsupervised clustering algorithm registration (§5.3 clause 1)

**Anchor:** §5.3 clause 1 verbatim: *"Unsupervised clustering over the character stream yields candidate strata."*

**New behaviour:** register a pluggable clustering algorithm seam that operates over `CharacterRegister.entries` (from CP-M6-3-1) and emits `CandidateStratum` records. **NO backend chosen** at this CP — the seam refuses live invocation with `[INFERRED-pending-ratification]` marker per D10 pluggable-seam discipline (already anchored at CP-M6-1-1 language identifier).

**Estimated CP scope (target +7 invariants):**
- `cluster_character_register(*, character_register, backend) -> Tuple[CandidateStratum, ...]` — pluggable seam.
- `CandidateStratum` — frozen 3-carrier dataclass: `stratum_id` (opaque string) · `member_attribute_names` (Tuple[str, ...]) · `backend_name` (str). No human-readable name carrier (per §5.3 clause 2).
- `ClusteringBackend` — Protocol with `.name` + `.cluster(entries) -> Tuple[CandidateStratum, ...]`.
- `UnratifiedInferredClusteringBackend` — placeholder refuses with `[INFERRED-pending-ratification]` marker.
- Refusals: `CharacterRegisterEmptyError` · `ClusteringBackendUnratifiedError`.
- Invariants (target 7):
    1. module_fabric_present (5 exports).
    2. cluster_character_register accepts empty backend Protocol — refuses `ClusteringBackendUnratifiedError` on `UnratifiedInferredClusteringBackend`.
    3. CandidateStratum frozen 3-carrier shape + no `human_name` / `label` / `display_name` carrier (§5.3 clause 2 negative-scan).
    4. cluster_character_register refuses `CharacterRegisterEmptyError` on empty `CharacterRegister`.
    5. cluster_character_register invokes the backend and returns its verbatim output (composition trust).
    6. CandidateStratum member_attribute_names is a Tuple of attribute_name strings referencing CharacterRegister entries.
    7. §3.1 P038 tokens-not-waveforms negative-scan CLEAN on `CandidateStratum` fields.

**Wave-honest limits:** no LLM invocation · no HTTP call · no filesystem write · no audio bytes cross the seam · case-agnostic · synthetic fixtures only.

### CP-M6-5-2 · Sampled human validation loop mechanism (§5.3 clause 3)

**Anchor:** §5.3 clause 3 verbatim: *"Naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost."* + §16.2 P249 · V157: *"Cluster naming validation: commissioned internally or delegated to an external evaluation partner where one exists (§5.3)."*

**New behaviour:** the sampling + validation-record + verdict-binding **mechanism**. Actual human validators binding real samples is post-unblock owner activity; the mechanism must be provable with synthetic fixtures (owner ruling 2026-09-15T~20:37Z).

**Estimated CP scope (target +8..+10 invariants):**
- `sample_stratum_for_human_validation(*, stratum, sample_size, rng_seed) -> Tuple[str, ...]` — deterministic sampler (`rng_seed` in, deterministic sample out; same seed → same sample).
- `HumanValidationTask` — frozen 5-carrier dataclass: `task_id` · `stratum_id` · `sample_attribute_names` (Tuple[str, ...]) · `quoted_cost_reference` (opaque str pointing to a commissioned-work quote entry) · `commissioning_channel` (str · closed-set: `{"internal", "external_partner"}` per P249).
- `HumanValidationVerdict` — frozen 4-carrier dataclass: `task_id` · `verdict` (closed-set: `{"variant_confirmed", "variant_refused", "ambiguous"}`) · `named_by_human` (Optional[str] · None until owner binds real validators — "not what it is called" is preserved in-flight) · `commissioning_receipt_ref` (opaque str).
- `bind_verdict_to_stratum(*, stratum, verdict) -> ValidatedStratum` — verdict-binding mechanism.
- `ValidatedStratum` — frozen 3-carrier dataclass: `candidate_stratum` · `verdict` · `bound_at_utc` (str · ISO-8601).
- Refusals: `SampleSizeInvalidError` · `SampleSizeExceedsStratumError` · `RngSeedInvalidError` · `CommissioningChannelInvalidError` · `VerdictClosedSetViolationError` · `VerdictTaskIdMismatchError`.
- Invariants (target 8..10):
    1. module_fabric_present.
    2. sample_stratum_for_human_validation deterministic on same seed (same seed → byte-identical sample).
    3. sample_stratum_for_human_validation different on different seeds (basic anti-degenerate).
    4. sample_stratum_for_human_validation refuses `SampleSizeInvalidError` on 0 / negative.
    5. sample_stratum_for_human_validation refuses `SampleSizeExceedsStratumError` on size > stratum members.
    6. HumanValidationTask frozen 5-carrier shape + closed-set `commissioning_channel`.
    7. HumanValidationTask refuses `CommissioningChannelInvalidError` on unknown channel.
    8. HumanValidationVerdict frozen 4-carrier shape + closed-set `verdict`.
    9. bind_verdict_to_stratum refuses `VerdictTaskIdMismatchError` when verdict.task_id ≠ task_id derived from stratum.
    10. bind_verdict_to_stratum produces `ValidatedStratum` with the original `CandidateStratum` unchanged (immutability preserved).

**Post-unblock owner activity:** actual human validators binding real samples happens AFTER (a) owner ratifies clustering backend (§D10) AND (b) commissioning process is stood up (P249). The mechanism itself is provable with synthetic fixtures TODAY.

### CP-M6-5-3 · Cluster stability invariants (§5.3 clause 2)

**Anchor:** §5.3 clause 2 verbatim: *"A cluster asserts that a distinct variant exists — not what it is called."*

**New behaviour:** invariants that bind the cluster-carrier discipline through the sub-wave:
- No cluster has a `human_name` / `label` / `display_name` field.
- `CandidateStratum` and `ValidatedStratum` both carry `stratum_id` (opaque) as their identity; naming is orthogonal.
- Cluster stability: same clustering-backend + same character-register → same stratum_ids (byte-identical).
- A `ValidatedStratum` never mutates its `candidate_stratum` (frozen preservation).

**Estimated CP scope (target +7 invariants):**
- `assert_cluster_carries_no_human_name(cluster) -> None` — negative-scan gate on `human_name` / `label` / `display_name` / `speaker_name` fields on any cluster object.
- `assert_clustering_is_deterministic(*, backend, character_register) -> None` — runs `backend.cluster(entries)` twice and asserts byte-identical stratum_id sequences.
- `assert_validated_stratum_preserves_candidate(*, validated) -> None` — asserts `validated.candidate_stratum` is unchanged.
- Refusals: `ClusterHumanNameLeakError` · `ClusteringNonDeterministicError` · `ValidatedStratumMutatedError`.
- Invariants (target 7):
    1. module_fabric_present.
    2. assert_cluster_carries_no_human_name passes on well-formed CandidateStratum.
    3. assert_cluster_carries_no_human_name refuses on cluster with `human_name` / `label` / `display_name` / `speaker_name` carrier.
    4. assert_clustering_is_deterministic passes on synthetic deterministic backend.
    5. assert_clustering_is_deterministic refuses on synthetic non-deterministic backend (produces different stratum_ids across runs).
    6. assert_validated_stratum_preserves_candidate passes on bind-produced ValidatedStratum.
    7. §5.3 clause 2 end-to-end: `cluster` → `sample` → `verdict.named_by_human=None` → `bind` path never introduces a human-readable cluster name.

**W-M6-CLUSTERING-HUMAN-VALIDATION SUB-WAVE 5 target delta:** 3 CPs · target +22..+25 invariants · ratchet 4213 → ~4235..4238 target.

---

## §D · Pluggable-seam & duck-type discipline

- Clustering algorithm backend (`ClusteringBackend`) is a Protocol · duck-typed · no coupling to a specific ML library.
- `UnratifiedInferredClusteringBackend` placeholder refuses live invocation per D10 pattern (already established at CP-M6-1-1, CP-M6-1-2, CP-M6-1-3, CP-M6-1-4).
- `CharacterRegister` carrier is the CP-M6-3-1 shape (already sealed); we compose against it, we do not modify it (no-refactor).
- Human-validation task/verdict carriers are pure data — no HTTP/filesystem/LLM in the sub-wave.
- All test fixtures are synthetic: synthetic CharacterRegisters, synthetic clustering backends (deterministic + non-deterministic reference implementations for gate tests), synthetic HumanValidationTasks/Verdicts. **HALT to owner** the instant a mechanism would need real estate voice/biometric material to validate.

---

## §E · Wave-honest limits

- **Synthetic fixtures only.** No real audio, no real speaker embeddings, no real biometric material. All test cases construct their own `CharacterRegister` instances and synthetic backends.
- **HALT-check.** Any CP whose invariants would require real material to validate → HALT to owner per SO §1. This sub-wave is explicitly authored to be provable with synthetic fixtures (per owner ruling 2026-09-15T~20:37Z).
- **No LLM / HTTP / filesystem write** in any sub-wave 5 module. The clustering seam is pluggable — the backend Protocol boundary is where those live if/when a live backend is ratified.
- **No mutation of prior CPs.** CP-M6-3-1 `CharacterRegister` unchanged. CP-M6-4-1..4-4 codec service surface unchanged. Compose-not-modify.
- **Position-redaction hard-lock preserved.** No SEC re-leak class emerges from the sub-wave's fixtures (all inputs are synthetic attribute-name strings).
- **§5.3 clause 2 is a first-class discipline gate.** No cluster object anywhere in sub-wave 5 carries a human-readable name field. CP-M6-5-3 anchors this end-to-end with `assert_cluster_carries_no_human_name`.
- **§3.1 P038 tokens-not-waveforms preserved.** No `audio_bytes` / `waveform` / `samples` / `raw_audio` carriers anywhere in sub-wave 5.

---

## §F · Commit protocol

Per SO §3 (build discipline) + §3.1 (ALIVE IS NOT DONE) + §3.2 (progress signal — not applicable, no runtime supervisor in sub-wave 5) + **§3.3 (NO SEAL WITHOUT BOTH SHAs — NEW · in force from 2026-09-15T~20:35Z)**:

At every CP seal:
1. RED receipt banked under `phase0/drill_receipts/` before mechanism lands (right-reason ModuleNotFoundError expected).
2. GREEN 1 + GREEN 2 back-to-back under `BASELINE_GUARD=1` at ratchet_target.
3. Byte-match property confirmed (raw byte-length identical + stripped-sha under a consistent strip algorithm).
4. Boundary probe fired at CP open + CP seal (every-CP cadence per owner ruling).
5. Wave rider (pip freeze + collect-only) banked to `phase0/wave_riders/w_m6_clustering_human_validation_cpN/`.
6. Seal file authored at `phase0/output_verified_seals/cp_m6_5_N_<slug>.seal.txt` with **both SHAs at seal completion (§3.3)** — no TBD.
7. Commit A on `programme/track-a` (code + baseline_failures.json bump).
8. Commit B on `master` (seal + receipts + probes + wave riders + DECISIONS + NEXT + PINS as needed).
9. DECISIONS entry banks BOTH SHAs per §3.3.
10. NEXT.md CURRENT AS OF pin banks the track-a SHA per §3.3.
11. Never push. Local commits are the record. `testing_agent` BANNED — terminal pytest only.

---

## §G · Onward after sub-wave 5

Sub-wave 6 opens on sub-wave 5 seal · W-M6-OBJECTIVE-WIZARD-COLLECTION-SCHEMA · §8, §9, §12.1 · Objective Wizard audio variant + Collection Schema type + registry namespace + N7 fold-in.

Interleave options unchanged: M3 W-BC-DYNAMIC-RECOVERY-BUILD · M2 W-PULL-SEAM-RECEIPT-UNIFY.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
