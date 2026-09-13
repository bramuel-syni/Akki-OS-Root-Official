# W1b · Platform Primitives · Wave close

**Wave name:** `W1b-PLATFORM-PRIMITIVES`
**Wave opened:** 2026-09-13T07:20Z
**Wave closed:** 2026-09-13T08:10Z
**Extraction-Akki `programme/track-a` HEAD at close:** *pending final code SHA*
**Workspace `master` HEAD at close:** *pending state commit SHA*

---

## 1. Progress made

W1b landed the remaining case-agnostic **platform primitives** that
gate W2 job-mount. Six CPs delivered in strict tests-first order:

| CP | Scope | New invariants |
|:---|:---|---:|
| CP1 | `RetentionPolicy` (four regimes + mismatch-refusal by construction) | +16 |
| CP2 | `SourceConnector` Protocol + `ReadOnlyGuard` mixin + `SourceHandle` | +27 |
| CP3 | Synology FileStation impl (interface only · `NotConfiguredForRuntime` gate) | +14 |
| CP4 | Generic `capability_registry` (fold-friendly compose-freeze of layer_b.factory shape) | +15 |
| CP5 | Generic `AttributeStreamBundle_v0` (14) + L2/L4 contract shells (14) | +28 |
| **W1b total** |   | **+100** |

Ratchet: **3392 → 3492** (monotonic-up · BASELINE_GUARD=1 double-green
byte-match across three consecutive runs).

## 2. How much to go

**W1b is complete.** The platform-vs-job separation is now enforceable
by construction for every primitive on the W2 blocker list:

- Any Artifact class binds to exactly one retention regime; class↔payload
  mismatch is a `RetentionMismatch` at write-check time, not a
  runtime accident.
- Any source is behind a read-only Protocol; write-shaped method calls
  are refused by `ReadOnlyGuard` __getattribute__ interception.
- The Synology-specific concrete impl exposes zero live-NAS surface
  in W1b (runtime gated by `AKKI_SYNOLOGY_ALLOWED_RUNTIME=1`, never
  set here).
- Provider factories are generalisable via `capability_registry` —
  proven by compose-freeze against `layer_b.factory` (three registries
  re-expressible in the generic mechanism).
- `AttributeStreamBundle_v0` is fully domain-neutral; the eight-column
  audio schema lands as a REGISTERED schema at W2 mount, never in
  platform code.
- L2/L4 contract shells are frozen pydantic — pure data.

## 3. Decisions taken

- **CP5 domain-neutrality refinement applied verbatim.** The
  `AttributeStreamBundle_v0` module has NO audio-column tokens
  (content/language/condition/prosody/occurrence/switch/music/character)
  and NO domain tokens (audio/harvest/transcribe/etc.). Frozen by two
  anti-leak invariants.
- **CP3 is interface-only.** Runtime is gated by an exact-`"1"` env
  check (not truthy string) — the deliberate constrained gate
  prevents accidental enable via generic `os.environ.get()` semantics.
- **CP4 is a compose-freeze, not a refactor.** `layer_b.factory` is
  untouched; the compose test re-registers its three registries into
  the generic mechanism and verifies retrieval — strict superset
  proven without breaking any existing invariant.
- **RetentionPolicy construction invariants** enforce the shape rules
  (DELIVERABLE_GOVERNED ⇒ release_gate_verdicts_required=True;
  SOURCE_UNTOUCHED ⇒ ttl_days=None) — unsafe policies are
  unrepresentable, not just discouraged.
- **`SourceConnector` Protocol has no credential surface.** Concrete
  impls take `auth_ref` (opaque string reference to an estate_keys
  row), not the credential value. Enforced by an inspection test on
  Protocol method signatures.

## 4. Discoveries not envisioned at planning

- **A parallel-tool race on CP3 nearly corrupted the RED discipline.**
  The initial `mcp_execute_bash` for the RED capture and the
  `mcp_create_file` for the impl ran in parallel; by the time the
  pytest under-the-bash-tool executed, the impl was already on disk.
  Corrected by moving the impl aside, re-running the tests, banking
  the true RED receipt, then restoring the impl. Now noted in the
  drill_receipts log for that CP.
- **The `_domain_token` anti-leak invariant is more restrictive than
  it looks.** Multiple docstring re-writes were needed across CP2/CP3/
  CP5 because the anti-leak string search catches even module-level
  comments that mention the banned tokens. This is the intended
  behavior — banking it here so it doesn't surface as a surprise in
  W1c/W2.
- **The class-vs-payload table in RetentionPolicy has a natural
  extension point.** Adding a new payload class (e.g.
  `synthetic_row` for stub outputs) requires only touching
  `_ALLOWED_PAYLOADS` — the test suite forces every regime to declare
  its allowed set. This is the natural extension seam for later waves.
- **`SchemaNotRegistered` doubles as the conflict-rebind exception.**
  The natural fit — a lookup that resolves to a different schema than
  the caller expects is semantically "the schema they wanted is not
  registered." Reused rather than a second exception class.

## 5. Recommendations to make the experience better, in line with the mission

- **W2 GO checklist remains BLOCKED on three external items:**
  1. Owner storage Path A/B/C ruling (RetentionPolicy binding for
     `corpus-deliverable-audio-segment-bytes`).
  2. NAS network path (sysadmin bastion or VPN — pod cannot reach
     10.10.55.55 today).
  3. 3-station confirm (owner ratifies the 3-of-16 stations to run
     end-to-end at W2 CP1 mount).
  W1b does NOT open any of these; noted here so they surface cleanly
  when you decide to open W2.
- **Before W2 opens, run one owner-facing integration walkthrough**
  using ONLY registered platform primitives (no case-B mount yet).
  This proves the platform can express a synthetic job (register a
  `platform.generic` capability, mount a bundle against a generic
  schema, exercise a RetentionPolicy write-check, submit a manifest,
  admit it, watch a simulated progress signal) with no domain code.
  Interior-only, no NAS. Small, high-confidence, and would surface
  any last platform-side wiring gap before the case-B mount lands.
- **Consider a `pydantic v3 upgrade` on a later platform wave.** The
  frozen-model / field-validator patterns are stable enough now that
  the churn cost of a v3 bump is bounded. Not W1b scope.

---

## Discipline receipts

- Grounding: `notes/W1b_PLATFORM_PRIMITIVES_grounding_brief.md`
- Per-CP RED:
  - `phase0/drill_receipts/20260913T072500Z_w1b_cp1_retention_policy_RED.log`
  - `phase0/drill_receipts/20260913T073000Z_w1b_cp2_source_connector_RED.log`
  - `phase0/drill_receipts/20260913T074000Z_w1b_cp3_synology_RED.log`
  - `phase0/drill_receipts/20260913T075000Z_w1b_cp4_capability_registry_RED.log`
  - `phase0/drill_receipts/20260913T080000Z_w1b_cp5_bundle_and_shells_RED.log`
- Wave-close double-green:
  - `phase0/drill_receipts/20260913T081000Z_w1b_platform_primitives_wave_close_double_green.log`

## Standing law upheld

- Tests-first mechanical RED before every code change (CP3
  re-captured after parallel-tool race).
- Double-green byte-match at wave close.
- Ratchet monotonic-up (3392 → 3492).
- Two-commit local (code · state). NO push.
- NO testing_agent. NO deployment_agent.
- Terminal pytest under BASELINE_GUARD=1 only.
- No refactor beyond what tests forced.
- Zero-influence held: no dispatch surface, no live NAS reach.
- Credentials 0600, HF token never echoed, SEC-2026-09-12-01
  rotation still owed by owner post-session.
- **HARD STOP: W2 not opened.** Blocked on external items enumerated
  in §5.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
