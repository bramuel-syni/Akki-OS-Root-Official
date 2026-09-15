READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-CENSUS-CANON-ALIGN · Wave-Close Report (END-OF-WAVE format per SO §2)

**Wave:** W-CENSUS-CANON-ALIGN (pre-census discipline-alignment · Option-α)
**Opened:** 2026-09-15T~02:12Z
**Sealed:** 2026-09-15T~03:22Z
**Ratchet:** 3979 → **4018** (+39 across CP-C1..CP-C6)
**Seal:** `phase0/output_verified_seals/census_canon_align.seal.txt` (Kind: `census_canon_align`)

---

## 1 · Progress made

Six sequential CPs landed, each under strict tests-first discipline (verbatim canon quote in module docstring + test docstring, mechanical RED with right-reason failure captured before mechanism, double-green byte-match at the tally line, ratchet manifest bump in tandem, two-commit pattern of Commit A on `programme/track-a` + Commit B on `master`).

| CP  | Focus                                                                        | Module(s) landed                                                              | Δ ratchet     | Track-a  | Master   |
|-----|------------------------------------------------------------------------------|-------------------------------------------------------------------------------|---------------|----------|----------|
| C1  | `SourceCandidate` frozen 4-carrier + deterministic sensitivity classifier   | `contracts/canon_census_source_candidate.py` + `services/census_canon/source_candidate_classifier.py` | 3979→3986 (+7) | `c45d0c3` | `a1c389a` |
| C2  | `Unmeasured` first-class sentinel + `Measurement` frozen 6-carrier + `FullOrSampled` + `SampledPopulationInvalid` | `contracts/canon_census_measurement.py`                                       | 3986→3993 (+7) | `112de26` | `f573284` |
| C3  | `CensusRun` frozen 4-carrier + `generate_census_run_id` deterministic sha256 | `services/census_canon/census_run.py`                                         | 3993→3999 (+6) | `e2a710c` | `c8c64eb` |
| C4  | Append-only registry write path (`SourceRecord` frozen 10-carrier + `RegistryStore` + `register_source_candidate` deterministic id) | `services/census_canon/registry_write.py`                                     | 3999→4005 (+6) | `5fcee76` | `14a0ec2` |
| C5  | `JobManifest` frozen 5-carrier per S5 reframe + `compute_manifest_fingerprint` | `contracts/census_job_manifest.py`                                            | 4005→4012 (+7) | `d552c31` | `6b2a307` |
| C6  | `SourceStratumMeasurement` frozen 8-dimension + `ActivationList` + `compute_activation_list` | `services/census_canon/stratum_measurement.py` + `services/census_canon/activation_list.py` | 4012→4018 (+6) | `0053b16` | *(this commit)* |

Every canon-required capability the census walk needs is now type-frozen. The census machinery is in place; the walk itself is next.

---

## 2 · How much to go

The wave is **closed** as chartered. Two follow-on items remain **before** the actual census run:

- **Item-3 · live census run** (Promise #12) — Chartered but **egress-window-blocked** at wave close (current UTC 03:22, window closed since 02:00, reopens 08:00). Runs read-only against reachable connectors (NAS 16 channels, OBS google-transcripts, weego + ussd MySQLs) and produces registry records + owner-facing report. Fires at first 08:00 UTC re-open.
- **Live SSH GPU re-verification** (non-blocking follow-on to CP-C3's GPU-AVAILABLE ruling) — same 08:00 UTC re-open. Reaffirms the on-disk prior evidence with a live-timestamped snapshot. Not blocking Item-3.

The chartered wave-honest-limits (E.1..E.7) are the follow-on backlog and are recorded in the seal file for the next wave-planning turn.

---

## 3 · Decisions taken

Three owner rulings landed inside this wave and are banked verbatim in `DECISIONS.md`:

1. **2026-09-15T~02:05Z · Option-α RATIFIED** — owner verbatim: *"go as recomended - a (run this on the GPUs). Build what needs to be built to run this."* The wave opened on this authorization.
2. **2026-09-15T~02:35Z · Re-grounding pack** — three plan-confirmation answers (Y CP-C2 Commit B first + non-egress CP walk while window is closed + Y hold at census run if window still closed). This ruling formalised the egress-hold protocol.
3. **2026-09-15T~02:45Z · GPU protocol SUPERSEDES bind-gap framing** — the owner corrected the bind-gap posture with a verified fact (*"Connected GPU has CUDA and Pytorch, this was confirmed from previous run."*). Verification protocol executed in order: pod = `no_gpu_visible` (as expected — governance pod, not compute pod); estate hosts `akki-vm` + `akki-vm-ii` = **`gpu_present`** cited from 4 on-disk evidence artefacts (2 first-heartbeat CSVs + 2 health-check snapshots) + DECISIONS 2026-09-06T~14:20Z (torch 2.11.0+cu128 · CUDA 12.8 · 2×H200 SURVIVED). `BLOCKER-CENSUS-GPU-BIND-01` (CP-C1) + `GPU-INV-01` (CP-C2) BOTH retired at CP-C3 close. New standing verdict: **`GPU-AVAILABLE` across two estate hosts · 4×NVIDIA H200 · 140.4 GiB VRAM each · CUDA 12.8 · torch 2.11.0+cu128**.

Two main-agent-side design decisions inside the wave (both frozen by invariants):

- **Existence is encoded by presence in the RegistryStore, not as a field** — Canon-4 §8 names four carrier concepts, but "existence" is naturally a presence property rather than a boolean field. Encoding it as presence-in-store keeps the record shape aligned with §8's literal reading and prevents the accidental "existence=False but record still stored" contradiction.
- **JobManifest is DATA-ONLY this wave (§E.4)** — runtime orchestration is a deliberate follow-on. Structurally enforced by an invariant that scans for banned runtime-shaped attribute names on the dataclass. Prevents mission creep between planning and shape.

---

## 4 · Discoveries not envisioned at planning

Three findings landed during the wave that were not in the grounding brief:

1. **Verbatim rule extends to whitespace fidelity in test assertions.** Two CPs (C3 + C5) initially wrapped their canon quotes across multiple lines in module docstrings for source-readability, and the `... in doc` substring assertion refused the line-wrap. Fix banked as a standing micro-pattern (CP-C3 close ruling): canon quotes stay on single un-wrapped lines in docstrings; assertions test byte-for-byte against the canon phrase.
2. **`CensusRun` and `Measurement` share the SampledPopulationInvalid clause.** The Canon-4 §4.1 P30 verbatim clause *"a sampled measurement is never presented as a full-population one"* was originally read as measurement-level (CP-C2). CP-C3 discovered the clause fires at the run level too — a SAMPLED walk with population <= 0 is not a valid census run. The exception is now shared across both levels.
3. **Owner-side pause is not a fault state.** The user paused mid-CP-C3 for owner-side reasons and instructed resume with a new fact (GPU-AVAILABLE). The corrective ritual is: re-execute SO §1 boot ritual (baseline green run + DECISIONS/NEXT re-read) BEFORE touching any file, then continue from the exact unsealed step. This preserves both crash-recovery safety and mid-flow continuity.

---

## 5 · Recommendations to make the experience better, in line with the mission

Three recommendations, each traceable to a specific gap surfaced by the wave:

1. **Charter `W-CENSUS-RUNTIME-ORCHESTRATION` for follow-on wiring.** CP-C5 landed `JobManifest` as data-only per §E.4. The next natural wave binds existing audio-poc surfaces (`recording_inventory`, `transcript_inventory`, `pairing_registry`) as registered plane implementations behind a `JobManifest`, then wires them onto the CP-C4 registry via CP-C6 `SourceStratumMeasurement` output-field carriers. Value: converts the frozen contracts landed here into an actual runnable job for arbitrary future estate instances (S5 reframe realised in code, not only in shape).
2. **Live SSH GPU re-verification is cheap and non-blocking.** The owner's GPU-AVAILABLE ruling was corroborated by 4 on-disk prior receipts, but a live 20-second SSH probe (`nvidia-smi --query-gpu=name,memory.total,driver_version,cuda_version --format=csv,noheader`) against both hosts at 08:00 UTC re-open provides a fresh timestamped receipt for future waves' evidence chain. Bank as `phase0/gpu_inventory/<yyyymmddThhmmssZ>_live_ssh_verification.json` per the GPU inventory schema already in place. Zero blocker impact.
3. **Consider a `verbatim-quote` pytest plugin for the standing rule enforcement.** The whitespace-fidelity micro-corrections at CP-C3 + CP-C5 could be prevented by a lint that scans module docstrings for canon quotes and refuses line-wrap inside a quoted region. Owner-side is currently the arbiter of paraphrase-not-spec; a small plugin could catch the common source-readability tension before RED. Optional, low-cost, pre-emptive.

---

## Appendix A · Wave metrics (rider 1 locked at seal)

- **pip-freeze lines:** 192 (unchanged vs W-DATA-SUITE-V2-LIFT close — no dependency additions this wave)
- **pytest --collect-only tests collected:** 4019 (was 3982 at last wave close)
- **Rider 1 receipts:**
  - `phase0/wave_riders/w_census_canon_align/rider1_pip_freeze_20260915T032100Z.txt`
  - `phase0/wave_riders/w_census_canon_align/rider1_pytest_collect_20260915T032100Z.log`

## Appendix B · CP invariant counts (bank + carry)

| CP  | Invariants added | Cross-benefit | Ratchet delta |
|-----|-----------------:|--------------:|--------------:|
| C1  | 6                | +1            | +7            |
| C2  | 6                | +1            | +7            |
| C3  | 6                | 0             | +6            |
| C4  | 6                | 0             | +6            |
| C5  | 6                | +1            | +7            |
| C6  | 6                | 0             | +6            |
| **Total** | **36**    | **+3**        | **+39**       |

Cross-benefits come from `NON_CONTRACT_UTILITY_MODULES` exemption additions in `test_frozen_contract_snapshot_parity.py` (one per contracts-module landing that is a `@dataclass(frozen=True)` rather than a pydantic BaseModel).

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
