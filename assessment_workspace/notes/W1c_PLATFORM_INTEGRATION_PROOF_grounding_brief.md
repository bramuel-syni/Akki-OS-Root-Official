# W1c · Platform Integration Proof · Grounding brief

**Wave name:** `W1c-PLATFORM-INTEGRATION-PROOF`
**Wave opened:** 2026-09-13T08:20Z (immediately after W1b close).
**Base HEAD (Extraction-Akki `programme/track-a`):** `0512a06` (W1b close · ratchet 3492).
**Base HEAD (workspace `master`):** `84163dac` (W1b state).
**HARD STOP after W1c close:** W2 stays BLOCKED (Path A/B/C · NAS · 3-station).

---

## §A. Owner ruling verbatim (2026-09-13T~08:15Z · W1c charter)

> RULING: proceed with option (a) — the interior-only platform
> integration proof — but land it as a COMMITTED end-to-end
> integration invariant, not a throwaway demo. This is the "prove it
> actually works, not stubs" step the whole programme is built
> around, so it must be permanent and regression-guarding.
>
> Scope (call it a small wave, e.g. W1c-PLATFORM-INTEGRATION-PROOF):
> one tests-first integration invariant (or a tight set) that drives
> the FULL platform spine end-to-end with a generic (non-domain)
> capability and NO NAS:
> - register a `platform.generic` capability in the capability
>   registry,
> - register a generic schema + mount an `AttributeStreamBundle_v0`
>   against it,
> - exercise a `RetentionPolicy` write-check (prove a payload/regime
>   mismatch is refused by construction),
> - submit a `JobManifest` (generic kind),
> - run it through `admit_job_with_governance` (prove admit on a
>   valid manifest AND a governance veto on an invalid one, with
>   the ledger row banked),
> - feed a SIMULATED stalled run state to the runtime supervisor and
>   prove it emits a `HaltVerdict` + starvation alarm; and a healthy
>   simulated run passes,
> - prove a bare (no-`Kind:`) seal is refused as not-real via the
>   admission precondition path (W0 primitive exercised through the
>   full surface).
> Assert the whole chain composes and that "done" is only reached via
> `output_verified_seal`. Produce an owner-inspectable trace/artifact
> of the run (a plain-language step-by-step of what happened, banked
> under phase0/ or notes/) so there's concrete evidence the platform
> works.
>
> Discipline: mechanical RED first, double-green BASELINE_GUARD=1
> byte-match, ratchet monotonic from 3492, two-commit local, NO push,
> NO testing_agent, no domain/audio code, credentials 0600.
>
> HARD STOP after this proof closes: do NOT open W2. Report to me at
> the integration-proof double-green close with the ratchet delta
> and the inspectable trace. Go.

---

## §B. What we are building (one-paragraph mission synthesis)

W1c is a **single-CP integration proof wave**: one test file
containing a tight set of invariants that drive every W1 + W1b
primitive end-to-end through the full platform spine, using ONLY a
generic (non-domain) capability. The invariants verify the chain
composes correctly (each step's output is the valid input to the
next), that failure paths refuse cleanly at each construction site,
that "done" is reachable ONLY via `output_verified_seal`, and that a
plain-language step-by-step trace is emitted to
`phase0/integration_proofs/w1c_integration_proof_trace.md` as an
owner-inspectable durable artifact.

---

## §C. Single-CP breakdown

- **CP1 · Integration invariant.**
  New `tests/invariants/test_w1c_platform_integration_proof.py` —
  a tight set of invariants that walk the full spine:
    1. **Registration path.** `kind_registry.register_kind("platform.generic")`
       (already seeded) + `capability_registry.register_capability(
       "platform.generic", "IntegrationProbe",
       "collections:OrderedDict")` + `attribute_stream_bundle.
       register_schema(...)` + `governance_plane.retention_policy.
       register_policy(...)`.
    2. **Bundle mount path.** Construct `AttributeStreamBundle_v0`
       against the registered schema.
    3. **RetentionPolicy mismatch-refusal.** Assert
       `check_write_admissible("register.generic.descriptive",
       "audio_bytes")` raises `RetentionMismatch` (REGISTER_DESCRIPTIVE
       does not admit byte payloads).
    4. **Admission happy path.** Build a valid `JobManifest`, run
       `admit_job_with_governance(m, rules=[LicenceClassRequired,
       DispatchIntentConfigured, OutputContractNamesRealKind],
       ledger_root=...)` → verdict.admitted is True; no ledger row
       banked.
    5. **Governance veto path.** Build a manifest with
       `output_contract.expected_kind="stub"` → verdict.admitted is
       False; verdict.refusal.kind == "governance_veto";
       verdict.refusal.rule_name == "output_contract_names_real_kind";
       ledger row banked at ledger_root.
    6. **Bare-seal precondition-refusal path (W0 compose freeze).**
       Build a manifest with a `precondition_seals` entry pointing
       at a run_dir containing an ACTIVITY_SUMMARY.md WITHOUT a
       `Kind:` line → `admit_job_with_governance` returns refusal
       kind `precondition_seal_not_real` (W0 silent-success ban
       inherited through the full stack).
    7. **Runtime supervisor · stalled path.** Simulate a run with
       flatline output_bytes across the SLA window →
       `output_verification_watchdog` returns
       `HaltVerdict(reason="starvation_output_flatline")`.
       Simulate a run with no signals ever →
       `HaltVerdict(reason="starvation_no_signal")`.
    8. **Runtime supervisor · healthy path.** Simulate a run with
       fresh signals and growing output → watchdog returns None.
    9. **Real-seal completion path.** Call
       `output_verified_seal(run_dir, kind="training_run_complete",
       body={...})` then `is_real_seal(run_dir) is True`;
       exercise the writer + reader through the primitive.
    10. **Trace artifact emitted.** The invariant emits a
        plain-language step-by-step Markdown trace to
        `phase0/integration_proofs/w1c_integration_proof_trace.md`
        with named sections for each step above. Content is
        deterministic (no timestamps in the persisted file to
        avoid gratuitous diffs on re-runs).

- **CP2 · Wave close.**
  Wave-close doc `notes/W1c_PLATFORM_INTEGRATION_PROOF_close.md`,
  double-green byte-match receipt, ratchet history entry, banked
  trace artifact under `phase0/integration_proofs/`.

**Estimated total: ~10 new invariants · ratchet 3492 → ~3502.**

---

## §D. Wave-honest limits (W1c)

1. **No domain/audio code.** All fixtures use generic, non-domain
   strings: `platform.generic`, `register.generic.descriptive`,
   `test.generic.v0`, `training_run_complete`. Anti-leak test
   optional but the file's tokens are inspection-ready.
2. **No NAS reach.** SynologyFileStation is exercised only at
   construction (inert) if at all; the wave never sets
   `AKKI_SYNOLOGY_ALLOWED_RUNTIME`.
3. **No real dispatch.** The runtime supervisor is exercised
   against SIMULATED progress signals in `tmp_path` — same
   discipline as CP2b in W1.
4. **Trace file is deterministic.** No timestamps in the persisted
   trace file. Each re-run overwrites with byte-identical content
   so the ratchet doesn't churn.
5. **No refactor beyond what tests force.** No existing module is
   changed unless the CP1 invariant forces it (none anticipated).
6. **Single test file.** Consolidating into one file makes the
   integration proof easy to read + reason about + git-review.

---

## §E. Commit protocol

- CP1 + CP2 close together (single-CP wave): TWO commits at close.
  Code (test file + trace artifact + baseline_failures.json) to
  Extraction-Akki `programme/track-a`. State (this brief +
  wave-close doc + DECISIONS append) to workspace `master`.
- **NO push. NO testing_agent. NO deployment_agent.**
- Terminal pytest under BASELINE_GUARD=1 only.
- Ratchet floor bumped in tandem at wave close (3492 → new).
- Report cadence: silent through CP1; surface at CP2 double-green.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
