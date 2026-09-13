# W1b · PLATFORM PRIMITIVES · Grounding brief

**Wave name:** `W1b-PLATFORM-PRIMITIVES`
**Wave opened:** 2026-09-13T07:20Z (immediately after W1 close).
**Base HEAD (Extraction-Akki `programme/track-a`):** `fcc9f43` (W1 close · ratchet 3392).
**Base HEAD (workspace `master`):** `070a8959` (W1 state).
**HARD STOP after W1b close:** do NOT open W2. W2 (job mount + real audio)
is BLOCKED pending owner storage Path A/B/C ruling, NAS network path,
and 3-station confirm.

---

## §A. Owner ruling verbatim (2026-09-13T~07:15Z · W1b charter approval)

> W1 accepted — clean close (3282→3392), case-agnostic kernel confirmed
> (the two anti-leak invariants are exactly the right guardrail),
> runtime supervisor landed before any dispatch, both standing orders
> banked. The narrow "signal"-ban refinement (ban terminate/kill, not
> the data-emission ProgressSignal) is sound and correctly documented
> in DECISIONS. Good work.
>
> CHARTER W1b as you scoped it — with ONE consistency refinement, same
> principle we applied to job_kind:
>
> CP5 refinement — keep the platform DOMAIN-AGNOSTIC. Do NOT bake an
> audio-specific AudioAttributeStreamBundle_v0 into the platform.
> Instead build a GENERIC AttributeStreamBundle_v0 abstraction in W1b
> (a bundle of named attribute streams with a declared schema,
> domain-neutral). The AUDIO-specific schema (the §1.1 eight columns:
> content/language/condition/prosody/occurrence/switch/music/character)
> is a DOMAIN schema that registers at W2 job-mount via the same
> registry mechanism as kind_registry — not resident in platform code.
> Add an anti-leak invariant mirroring CP1's (no audio tokens in the
> generic bundle module). Everything else in CP5 (the L2/L4 contract
> shells: TargetOutcome_v0, StratumAcceptance, CommissionSpec,
> Milestone, WorkerLane, WorkerJD) is genuinely generic — keep as-is.
>
> Synology connector (CP3): correct as scoped — a reusable
> SourceConnector IMPLEMENTATION (interface only, no live NAS call)
> is platform; the specific 10.10.55.55 host + creds are the JOB
> binding at W2, not platform. Hold that line.
>
> Approved W1b CP order: CP1 RetentionPolicy (four regimes +
> mismatch-refusal) → CP2 SourceConnector Protocol + read_only_guard
> → CP3 Synology FileStation impl (interface only) → CP4 Capability
> registry generalisation (fold layer_b.factory under the open-
> registry mechanism) → CP5 generic AttributeStreamBundle_v0 + L2/L4
> contract shells → CP6 wave close.
>
> Discipline: tests-first mechanical RED per CP, double-green
> BASELINE_GUARD=1 byte-match at wave close, ratchet monotonic from
> 3392, two-commit local, NO push, NO testing_agent, no refactor
> beyond what tests force, credentials 0600 (HF token never echoed).
>
> HARD STOP after W1b close: do NOT open W2. W2 (job mount + real
> audio) is BLOCKED pending the owner's storage Path A/B/C ruling,
> the NAS network path, and 3-station confirm. Report to me at the
> W1b double-green close. Keep intra-CP chatter inside the sprint
> plan. Go.

---

## §B. What we are building (one-paragraph mission synthesis)

W1b lands the remaining case-agnostic **platform primitives** that
gate W2 job-mount: (i) `RetentionPolicy` (four regimes with
mismatch-refusal by construction — SOURCE_UNTOUCHED /
WORKER_SCRATCH_PURGED / REGISTER_DESCRIPTIVE / DELIVERABLE_GOVERNED,
per the reframed roadmap §A.10), (ii) a `SourceConnector` Protocol
with `read_only_guard` mixin (generic), (iii) a Synology FileStation
implementation of that Protocol at interface level (no live NAS call
— specific host + creds are a W2 binding, not platform), (iv) a
generic `capability_registry` that generalises `layer_b.factory`'s
category/name pattern (compose-freeze; no `layer_b.factory` refactor),
(v) a generic `AttributeStreamBundle_v0` contract (bundle of named
attribute streams with a declared schema; domain schema registers at
W2 mount time — no audio schema in platform), and L2/L4 contract
shells (`TargetOutcome_v0`, `StratumAcceptance`, `CommissionSpec`,
`Milestone`, `WorkerLane`, `WorkerJD`). Zero-influence throughout.
Anti-leak invariants mirror CP1's kind-registry pattern.

---

## §C. CP breakdown (owner-approved)

- **CP1 · RetentionPolicy (four regimes + mismatch-refusal by construction).**
  New `services/governance_plane/retention_policy.py` exports
  `RetentionRegime` (closed enum: SOURCE_UNTOUCHED /
  WORKER_SCRATCH_PURGED / REGISTER_DESCRIPTIVE / DELIVERABLE_GOVERNED),
  `RetentionPolicy` (pydantic v2 frozen: artifact_class, regime,
  ttl_days, release_gate_verdicts_required), `RetentionMismatch`
  (ValueError), `register_policy(policy)`, `get_policy(artifact_class)`,
  `check_write_admissible(artifact_class, payload_class)` → raises
  `RetentionMismatch` on class↔regime violation (e.g. a
  `character-register-entry` writing an `audio_bytes` payload under
  regime REGISTER_DESCRIPTIVE). No I/O. ~12 invariants.

- **CP2 · SourceConnector Protocol + read_only_guard.**
  New `services/source_plane/connector.py` exports
  `SourceConnector` (typing.Protocol: list_paths, stat, open_read,
  close), `ReadOnlyGuard` (mixin/decorator refusing any method whose
  name matches a write pattern: put/write/delete/mkdir/rename/mv/rm),
  `SourceConnectorWriteRefused` (RuntimeError), `SourceHandle`
  (dataclass frozen: kind, uri, opened_at_utc). No live network calls.
  No credentials on the Protocol surface (credentials are supplied to
  concrete impls at W2 mount time). ~10 invariants.

- **CP3 · Synology FileStation impl (interface only).**
  New `services/source_plane/synology_file_station.py` exports
  `SynologyFileStationConnector` (implements `SourceConnector`, wraps
  `ReadOnlyGuard`). Constructor accepts `base_url`, `auth_ref`
  (opaque reference — NOT the actual credential), `timeout_seconds`.
  All methods raise `NotConfiguredForRuntime` when
  `AKKI_SYNOLOGY_ALLOWED_RUNTIME=1` is not set (interface-only wave;
  runtime is a W2 concern). Zero network I/O in any test. ~10
  invariants including anti-leak (no `10.10.55.55` / no NAS-specific
  IPs in module source; no owner-facing creds anywhere).

- **CP4 · Capability registry generalisation.**
  New `services/capability_registry.py` exports `register_capability
  (category, name, import_path)`, `get_capability(category, name)`,
  `list_categories()`, `list_capabilities_in(category)`,
  `CapabilityNotRegistered`, `_reset_capabilities_for_tests`. Generic
  — no asr/diarization/vision/audio tokens in the module source.
  Compose-freeze test: `layer_b.factory`'s three registries (asr /
  diarization / vision) can be RE-registered into the generic
  registry at test time and retrieved by (category, name) — proves
  strict superset without refactoring `layer_b.factory` (thin-kernel).
  ~10 invariants.

- **CP5 · Generic AttributeStreamBundle_v0 + L2/L4 contract shells.**
  New `services/attribute_stream_bundle/__init__.py` exports:
    - `AttributeStreamBundle_v0` (frozen pydantic: bundle_id,
      schema_ref (reference to a registered schema), streams (dict
      name -> stream metadata), sealed_at_utc). Generic — no audio
      column names in module source.
    - `AttributeStreamSchema` (frozen: schema_id, columns (tuple of
      (name, kind_hint) — no domain values)), `register_schema(schema)`,
      `get_schema(schema_id)`, `SchemaNotRegistered`. Domain schemas
      register at W2 mount time; platform ships zero registered
      schemas.
  New `services/contract_shells/__init__.py` exports the L2/L4
  contract shells (all generic, all frozen pydantic v2):
    - `TargetOutcome_v0`
    - `StratumAcceptance`
    - `CommissionSpec`
    - `Milestone`
    - `WorkerLane`
    - `WorkerJD`
  Fields are declared as generic strings/dicts — no domain
  vocabulary. Anti-leak invariant covers ALL new modules this CP.
  ~14 invariants.

- **CP6 · Wave close.**
  Owner-facing wave-close doc `notes/W1b_PLATFORM_PRIMITIVES_close.md`.
  Double-green byte-match receipt. Ratchet history entry. No new
  invariants beyond CP1-CP5.

**Estimated total: ~56 new invariants · ratchet 3392 → ~3448.**

---

## §D. Wave-honest limits (W1b)

1. **No live NAS reach.** CP3 is interface-only. Runtime calls raise
   `NotConfiguredForRuntime` unless `AKKI_SYNOLOGY_ALLOWED_RUNTIME=1`
   (deliberately never set in W1b). The IP + creds bind at W2, not
   here.
2. **No `layer_b.factory` refactor.** CP4 adds a generic registry
   and proves strict-superset via a compose-freeze test; the
   existing `layer_b.factory` module is untouched (thin-kernel).
3. **No domain schemas registered in platform.** CP5 registers ZERO
   schemas in `attribute_stream_bundle`. The eight-column audio
   schema binds at W2 mount, not here. Anti-leak invariants freeze
   the discipline.
4. **RetentionPolicy is a registry singleton for W1b tests.** Same
   pattern as `kind_registry`; production concurrency safety and
   audit trail are later refinements.
5. **`check_write_admissible` uses static class-vs-regime rules for
   W1b.** Fine-grained per-artifact byte-shape validation (e.g.
   "this REGISTER_DESCRIPTIVE artifact carries an audio blob")
   requires a payload-type system — deferred; W1b enforces the
   simpler artifact-class ↔ allowed-payload-classes mapping.
6. **`SourceConnector` Protocol carries no auth surface.** Concrete
   impls consume opaque `auth_ref` strings; the credential store is
   `/app/backend/estate_keys/` (custody boundary preserved).
7. **L2/L4 contract shells have no relational logic.** Contracts are
   frozen data. Applying them (validators, cross-manifest checks)
   is a follow-on concern.
8. **No new frontend surface.** All CPs are backend-only.
9. **No refactor beyond what tests force.** No existing module is
   changed unless a W1b test forces it (none anticipated).

---

## §E. Commit protocol

- Intra-CP: single code commit per CP once the CP's new invariants
  are green + no regression, `baseline_failures.json` updated with
  the wave-close ratchet increment held for CP6.
- **Wave close (CP6)** produces the double-green byte-match receipt
  and TWO commits: one to `programme/track-a` (final code + baseline
  ratchet_history entry with the wave-close SHA backfilled), one to
  workspace `master` (STATE/DECISIONS append,
  notes/W1b_PLATFORM_PRIMITIVES_close.md, this grounding brief).
- **NO push. Ever.**
- **NO testing_agent.** Terminal pytest under `BASELINE_GUARD=1` only.
- **Ratchet floor bumped in tandem** at wave close (3392 → new).
- **Report cadence:** silent through CP1-CP5; surface to owner at
  the W1b double-green close per owner's ruling.
- **HARD STOP after W1b close.** Do not scope, propose, or open
  W2.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
