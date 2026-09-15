# W-M6-CLUSTERING-HUMAN-VALIDATION · Wave close

**Wave sealed at UTC:** 2026-09-15T~21:22Z
**Milestone:** M6 · Sub-wave 5 (§5.3 P089 V59)
**Track-a HEAD at wave close:** `62e5a1d` · **Master HEAD:** `fe024740` (landed under STANDING_ORDERS §3.3 · commit C-fixup pinned the master SHA · NO SEAL WITHOUT BOTH SHAs rule satisfied)
**Ratchet delta:** 4213 → 4240 (+27) across three CPs

---

## §A · What we built

Discharged **Audio-Plane §5.3 P089 (V59) in full** — the clustering + human-validation clause.  Three CPs · three frozen mechanisms · one end-to-end invariant lock:

> §5.3 P089 (V59) verbatim:
>
> *"Unsupervised clustering over the character stream yields candidate strata. A cluster asserts that a distinct variant exists — not what it is called. Naming and validation are human work applied to a sample, commissioned like any other qualified work with quoted cost."*

### CP-M6-5-1 · Unsupervised clustering algorithm registration (clause 1)

Landed `services/audio_plane_v1/clustering.py` — a pluggable clustering seam over the CP-M6-3-1 `CharacterRegister.entries`.

- `CandidateStratum` (frozen 3-carrier: `stratum_id` · `member_attribute_names` · `backend_name`).  **No `human_name` / `label` / `display_name` / `speaker_name` carrier** — §5.3 clause 2 verbatim discipline enforced at construction.
- `ClusteringBackend` (Protocol · case-agnostic duck-typing).
- `UnratifiedInferredClusteringBackend` (placeholder refuses live invocation with `[INFERRED-pending-ratification]` marker per D10 pluggable-seam discipline — same pattern as CP-M6-1-1..1-4).
- `cluster_character_register(*, character_register, backend)` — refuses `CharacterRegisterEmptyError` on empty register; delegates to backend and returns verbatim output.

Ratchet 4213 → 4220 (+7).  Seal: `cp_m6_5_1_clustering_registration.seal.txt`.

### CP-M6-5-2 · Sampled human validation loop mechanism (clause 3 + §16.2 P249)

Landed `services/audio_plane_v1/human_validation.py` — the sampling + validation-record + verdict-binding mechanism, provable with synthetic fixtures.  **MECHANISM ONLY** per owner ruling 2026-09-15T~20:37Z: real human validators binding real samples is post-unblock owner activity.

- `COMMISSIONING_CHANNELS = frozenset({"internal", "external_partner"})` — §16.2 P249 verbatim two-set.
- `VALIDATION_VERDICTS = frozenset({"variant_confirmed", "variant_refused", "ambiguous"})` — closed refusal grammar.
- `sample_stratum_for_human_validation(*, stratum, sample_size, rng_seed)` — deterministic sampler via `random.Random(seed).sample`.  Same `(stratum, sample_size, rng_seed)` → byte-identical output.
- `HumanValidationTask` (frozen 5-carrier · refuses invalid channel).
- `HumanValidationVerdict` (frozen 4-carrier · closed-set verdict · **`named_by_human: Optional[str] = None`** preserves §5.3 clause 2 *"not what it is called"* until owner-unblocked real binding).
- `ValidatedStratum` (frozen 3-carrier · ISO-8601 UTC bound_at).
- `derive_task_id` + `bind_verdict_to_stratum` (refuses `VerdictTaskIdMismatchError` on cross-binding; preserves frozen `CandidateStratum` reference).

Ratchet 4220 → 4232 (+12).  Seal: `cp_m6_5_2_human_validation_loop.seal.txt`.

### CP-M6-5-3 · Cluster-stability invariants end-to-end (clause 2)

Landed `services/audio_plane_v1/cluster_stability.py` — the §5.3 clause 2 discipline gate discharged as end-to-end invariants composing CP-M6-5-1 + CP-M6-5-2 carriers.

- `HUMAN_NAME_ATTRIBUTE_NAMES` (frozen 5-tuple: `human_name` · `label` · `display_name` · `speaker_name` · `cluster_name`) — negative-scan attribute set.
- `assert_cluster_carries_no_human_name(*, cluster)` — refuses `ClusterHumanNameLeakError` on any non-None attribute in the set; None-valued attributes pass (canonical *"not what it is called"* value).
- `assert_clustering_is_deterministic(*, backend, character_register)` — runs `backend.cluster(entries=…)` twice; refuses `ClusteringNonDeterministicError` on stratum_id sequence divergence.
- `assert_validated_stratum_preserves_candidate(*, validated, original_candidate)` — refuses `ValidatedStratumMutatedError` on frozen-dataclass value inequality.

Ratchet 4232 → 4240 (+8).  Seal: `cp_m6_5_3_cluster_stability.seal.txt`.

---

## §B · How much to go (M6)

Sub-waves 1..5 sealed.  M6 remaining scope (per grounding brief `notes/M6_AUDIO_PLANE_PRODUCTION_BUILD_grounding_brief.md`):

- **Sub-wave 6** · W-M6-OBJECTIVE-WIZARD-COLLECTION-SCHEMA · §8, §9, §12.1 · N7 fold-in.
- Remaining §15 items after sub-wave 6.
- **M6 seal** on full §15 walk close.
- **M7 opens** thereafter (W0..W9 · already ratified · MILESTONE_PROMISE_BINDING_20260915).

**Sub-wave count:** 5 of ~10 sub-waves sealed (M6 grounding brief lists 10 sub-waves + P2-deferred items).

**Ratchet trajectory:** 4105 (M6 open · 2026-09-15T~17:50Z) → 4240 (post sub-wave 5 · 2026-09-15T~21:22Z) → target ~4300 post sub-wave 6.

---

## §C · Decisions taken

1. **Sub-wave 5 opened autonomously** under owner's synthetic-fixtures-only HALT boundary (established at CP-M6-3-2 open).  All three CPs held that discipline: every `CandidateStratum`, `HumanValidationTask`, `HumanValidationVerdict`, and `ValidatedStratum` used in tests was hand-built with `mat://synthetic/` provenance.  No real estate voice/biometric material referenced.
2. **§5.3 clause 3 discharged as MECHANISM only** per owner ruling 2026-09-15T~20:37Z (`STATE/DECISIONS.md`).  Real human validators binding real samples is deferred to post-unblock owner activity; the mechanism is complete end-to-end with `named_by_human=None` verdicts.
3. **STANDING_ORDERS §3.3 executed cleanly across all three CPs.**  Every CP used the 3-commit pattern (Commit A code → Commit B state · master TBD → Commit C fixup · master landed).  Every seal file at final state carries both track-a and master SHAs.  Every DECISIONS entry carries both SHAs.  Every NEXT.md CURRENT AS OF pin carries the track-a SHA.  The partial-seal drift class that the CP-M6-4-2 reconciliation exposed is now closed by mechanism, not by discipline.
4. **§5.3 clause 2 discipline elevated from schema-level to end-to-end invariant.**  CP-M6-5-1 landed the schema-level gate (no human-readable name carrier on `CandidateStratum`).  CP-M6-5-2 preserved the discipline in-flight via `named_by_human=None` default.  CP-M6-5-3 promoted it to an end-to-end assertion (`assert_cluster_carries_no_human_name`) that fires across the full cluster → sample → verdict → bind lifecycle and refuses any human-readable name leak on any cluster-like carrier.
5. **Determinism gate landed at CP-M6-5-3** as a first-class stability property of clustering backends (not just a nice-to-have).  A backend that emits different stratum_id sequences across two consecutive runs on identical input refuses at the invariant boundary — because downstream sample/verdict/bind receipts lose their binding to a stable stratum identity otherwise.

---

## §D · Discoveries not envisioned at planning

1. **`ValidatedStratum` immutability was under-anchored at CP-M6-5-2.**  The CP-M6-5-2 bind path stores `stratum` by reference; the frozen dataclass makes mutation impossible in-lifecycle.  But there is no CP-M6-5-2 invariant that asserts *"the bound candidate matches the original at bind time"* — a caller could construct a `ValidatedStratum(candidate_stratum=different)` directly.  CP-M6-5-3 `assert_validated_stratum_preserves_candidate` fills this gap.
2. **The four leak-vocabulary attribute names are not exhaustive.**  CP-M6-5-3 also gates on `cluster_name` in addition to the four in the CP-M6-5-3 grounding brief (human_name / label / display_name / speaker_name).  The frozen 5-tuple is banked as a module constant `HUMAN_NAME_ATTRIBUTE_NAMES` and can be extended by owner ratification without breaking the invariant contract.
3. **Boundary probe pattern held perfectly at 49 consecutive timeouts.**  CD (`citizen_digital` 159.138.164.103:3306) and Visitors (`visitors` 110.238.75.83:3306) both FAIL at ~6.0s across all 49 probes with `errno=null` (Python `socket.timeout`).  The MySQL SG openings ratified 2026-09-15T~04:25Z have not yet materialised in the network.  Admin escalation is banked at `notes/ADMIN_BINDS_20260915.md` and surfaced to owner directly.

---

## §E · Recommendations to make the experience better, in line with the mission

1. **Publish a §5.3 discipline compliance stamp on every future clustering / character-register / audio-plane surface.**  When sub-wave 6 (Objective Wizard) lands, it will need to bind objectives to clusters — that binding must go through `assert_cluster_carries_no_human_name` before any objective-cluster tuple is persisted.  Wire the CP-M6-5-3 gate into the sub-wave 6 write-path, not as a downstream sanity check.
2. **Consider a canon-anchored "unratified backend registry" surface** — every pluggable seam in M6 sub-wave 1 (Language ID · Code-switch · Channel condition · Synthesis attributes) and sub-wave 5 (Clustering) has an `Unratified*InferredBackend` placeholder.  A registry listing which backends the owner has ratified (and which are still `[INFERRED-pending-ratification]`) would give a single-glance view of what audio-plane capabilities are truly live vs. pending owner ratification.  This is off the current wave-plan critical path but would materially help the M6 → M7 seal-story.
3. **Escalate the CD + Visitors admin bind timeout to a P0 owner-desk item.**  The MySQL SG openings for `citizen_digital` and `visitors` were ratified 22 hours ago (2026-09-15T~04:25Z).  Egress has been open the whole time (per NEXT.md pins).  49 consecutive probe timeouts × ~6.0s each is not a network-latency issue — the ingress rules never landed.  This is not blocking sub-wave 6 (which is offline/synthetic per §8/§9/§12.1), but it is blocking the M6 → M7 transition where live audio ingest across the estate becomes the critical path.

---

## §F · Wave discipline receipts (roll-up)

| CP | RED | GREEN 1 | GREEN 2 | Seal | Boundary probes | Track-a HEAD | Master HEAD |
|---|---|---|---|---|---|---|---|
| CP-M6-5-1 | `20260915T204426Z_wm6_5_1_RED_pre_impl.log` (7 right-reason) | `20260915T204525Z_wm6_5_1_double_green_run1.log` 4220 passed | `20260915T204730Z_wm6_5_1_double_green_run2.log` (byte-match; stripped-sha256 `62f3312e…`) | `cp_m6_5_1_clustering_registration.seal.txt` | #44 open · #45 seal (both FAIL) | `ed0c740` | `94cf67c4` |
| CP-M6-5-2 | `20260915T205629Z_wm6_5_2_RED_pre_impl.log` (12 right-reason) | `20260915T205748Z_wm6_5_2_double_green_run1.log` 4232 passed | `20260915T205951Z_wm6_5_2_double_green_run2.log` (byte-match; stripped-sha256 `fe75bcb7…`) | `cp_m6_5_2_human_validation_loop.seal.txt` | #46 open · #47 seal (both FAIL) | `7ed9ad9` | `88b388c8` |
| CP-M6-5-3 | `20260915T211102Z_wm6_5_3_RED_pre_impl.log` (8 right-reason) | `20260915T211517Z_wm6_5_3_double_green_run1.log` 4240 passed | `20260915T211722Z_wm6_5_3_double_green_run2.log` (byte-match; stripped-sha256 `42277b58…`) | `cp_m6_5_3_cluster_stability.seal.txt` | #48 open · #49 seal (both FAIL) | `62e5a1d` | `fe024740` |

**Discipline held across all three CPs:** tests-first double-green byte-match · ratchet monotonic-up · word-boundary executive-domain negative-scan CLEAN · §3.1 P038 tokens-not-waveforms preserved · §5.3 clause 2 preserved throughout · no LLM/HTTP/filesystem · no refactor of prior CPs · refusal-family cohesion (all three CPs use plain `Exception` subclasses with canon-anchored docstrings) · §3.3 3-commit pattern executed cleanly · never push · terminal pytest only · `testing_agent` BANNED · position-redaction hard-lock preserved · synthetic-fixtures-only.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
