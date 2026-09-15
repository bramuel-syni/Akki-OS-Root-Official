READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# PENDING_RATIFICATIONS_LEDGER_20260915.md

**Purpose.** Owner information request 2026-09-15T~03:35Z (verbatim): *"For EACH pending owner item (R-7, R-13, R-14, R-15, R-16, R-17, BC-3, BC-4, S-24, plus drift items D7 codec_version / D9 receipt-before-result / D10/D11 silero+pyannote INFERRED, and D12): verbatim text of the pending ruling/marker from the ruling ledger or code docstring, source file+line, what behavior is currently defaulted, and exactly what ratifying it unblocks. Position-redaction applies as always."*

**Row-flip banking · 2026-09-15T~03:55Z ·** OWNER RULING PACKET LANDED (verbatim in `STATE/DECISIONS.md` same UTC · RULING_LEDGER row 18/19/20/21 in RATIFIED · Effect 1..11 detailed in DECISIONS). Four rows below FLIPPED from `OPEN` → `RATIFIED`; three rows explicitly clarified as STAYS-OPEN (R-17(a), R-15(b)/R-16(b)/R-17(b) — mnemonic-collision now resolved); BC-3/BC-4 direction changed from `static-number-pending` to `DYNAMIC-RECOVERY-PACKET-authored-awaits-ratification`.

**Compiled during** closed egress window (03:22 UTC seal → 08:00 UTC reopen). Non-egress work only. State/docs only; **no mechanism change, no ratchet change**.

**Position-redaction rule applied:** no PII, no secrets, no host IPs, no SSH usernames, no keys, no full paths inside credential custody. Aliases and citations only.

---

## §A · Ratification-Record openings (R-*, BC-*, S-* series)

### R-7 · Security · Estate release budget number

**Status:** ~~**OPEN · highest priority**~~ **→ RATIFIED (PILOT-OPEN) 2026-09-15T~03:55Z** (owner ruling packet · RULING_LEDGER row 18 in RATIFIED).

**Ratification value:** `PILOT-OPEN`. Owner-verbatim: *"budget state = PILOT-OPEN (owner-ratified, supersedes DEFAULT-PENDING-OVERRIDE refusal), BUT every release is still receipted AND debited into a running release ledger from day one — so when the pilot ends, the real budget number is set from measured usage, not guessed. The gate's refusal on unset-budget is replaced by pilot-mode admission WITH mandatory receipt+debit; a missing receipt still refuses (Pull Seam P7 unchanged)."*

**Prior verbatim anchor (kept for lineage):**
> "**Sec R-7 (estate release budget number)** | **OPEN — owner input · highest priority** | **STILL OPEN** — gates DAP R-3, DAP-6"

**Verbatim (`notes/RULING_LEDGER.md:66`):**
> "Security **R-7** | Estate release budget number (**highest priority** — gates DAP R-3, DAP-6, SFP-6)"

**Verbatim in-code marker (`backend/services/audio_poc/release_gate.py:12-15`):**
> "at wave open, the three other verdicts (KDPA · named-persons · transfer-basis) are all PENDING per owner still-blocked list. This means the release gate CURRENTLY refuses ALL transcript releases. CP-A5's writer will observe the refusal and HALT-with-blocker-note per grounding brief §G — that is the CORRECT posture until owner rulings land on R-7 / R-15 / R-16 / R-17."

**Behavior currently defaulted:**
- Estate-level release-budget accumulator lands with sentinel `RELEASE_BUDGET_NUMBER = DEFAULT-PENDING-OVERRIDE` (per PHASE_C R-C1/R-C2 marker rule, `notes/MILESTONE_PROMISE_BINDING_20260913.md:166`).
- `TranscriptArtefact.kdpa_verdict` remains PENDING at construction → `admit_transcript_release` raises `TranscriptVerdictPending` on every call → every transcript write-back deterministically refuses.
- Audio-POC gap-fill writer HALTs on write-back attempt with blocker note (correct structural posture, not defect).

**Ratifying R-7 unblocks:**
- **DAP-Spec `A5` slow-play detection · A10 artefact egress remainder** production-grade close (currently DEFAULT-PENDING sentinel).
- **DAP R-3** per-party ceilings (COUPLED · cannot be ruled alone per RULING_LEDGER COUPLED-1 clause).
- **DAP-6** pricing model (partially — gated on R-7 for the budget number).
- **SFP-6** serving-floor budget dependency.
- **S-25** estate-level release-budget promise from `MILESTONE_PROMISE_BINDING_20260913.md:311`.
- **Audio-POC BLOCKER-HF-A5-03** (release-gate KDPA verdict PENDING).

---

### R-13 · Serving-Integrity Amendment · Reference-validation cadence

**Status:** **RATIFIED** (2026-09-13 C3 batch).

**Verbatim (source: `notes/canon_serving_integrity_amendment_v1_requirements.md:69,76`):**
> "**Bound / Ruling**: R-13 (validation cadence, DEFAULT-class) open; floor explicitly **not imposable** on the frontier gateway tier — receipt records boundary."
> "**R-13** (DEFAULT-class): *'The reference-validation cadence for A20.15's operational check. Recommended default: on every engine version change and every artefact version change, plus a standing monthly run. DEFAULT-class — revisable on evidence, on Doc 3's own baseline-period pattern.'*"

**Verbatim owner-directive ratification (`notes/RATIFICATION_C3_BATCH_20260913.md:69`):**
> "SIA R-13 (validation cadence · monthly + per-version) | Recommended default (new spec, 2026-09-13) | **RATIFIED** — under same C3 en-masse ratification of recommended defaults."

**Behavior currently effective (RATIFIED, wired):**
- Validation cadence = **monthly + per-engine-version + per-artefact-version** (frozen by invariant in `backend/services/rulings/default_class_constants.py`).
- Frontier-gateway tier receipt records the boundary (as canon literally states: "not imposable on the frontier gateway tier").

**Ratifying R-13:** Already RATIFIED. No further owner action needed. **Listed here** because it appears on the standing pending-list *"Owner ratifications R-7/R-15/R-16/R-17/BC-3/BC-4/S-24/R-13/R-14"* (DECISIONS.md 2026-09-15T~02:35Z clause 4). That list references R-13 as a still-carried follow-on marker in the audio-plane end-to-end release-gate sequence, **NOT** as an unresolved ruling. Bank-clarification for the owner: this row is closed.

---

### R-14 · Serving-Integrity Amendment · Candidate serving engine admission

**Verbatim (source: `notes/canon_serving_integrity_amendment_v1_requirements.md:77`):**
> "**R-14** (open, deliberately unruled): *'Whether [the candidate serving engine · name scrubbed per owner ruling 2026-09-14] is admitted as the local rung's serving infrastructure. Not ruled here, and deliberately so: admission is gated on (a) the appliance benchmark — the smallest registered-family candidate on actual appliance hardware, per the appliance programme's own test discipline — and (b) the same admission ceremony any TCB-tier component undergoes. Neither has been run; ruling now would circumvent them.'*"

**Verbatim owner scrub-directive** (banked in `canon_serving_integrity_amendment_v1_requirements.md:6`, dated 2026-09-14):
> "*'In R-14, drop that engine's name, should not surface anywhere in the system or documentation'*"

**Verbatim (`notes/RATIFICATION_C3_BATCH_20260913.md:70`):**
> "**SIA R-14 (candidate serving engine admission)** | Deliberately unruled per amendment §7 | **STILL OPEN** — gated by appliance benchmark + TCB-tier admission ceremony"

**Behavior currently defaulted:**
- No candidate serving engine is admitted. Serving path uses the existing platform primitives (Solva-V2 seam + W1/W1b/W1c substrate).
- Any candidate-engine mention in code/docs replaced with neutral descriptor `[the candidate serving engine · name scrubbed per owner ruling 2026-09-14]`.

**Ratifying R-14 unblocks:**
- Local-rung serving infrastructure admission (specific engine → TCB-tier).
- SFP-8 serving-floor implementation binding to a named engine (currently binds to abstract "SFP-8-conforming serving path" per `MILESTONE_PROMISE_BINDING_20260913.md:15`).
- Registered-family candidate benchmarks on appliance hardware.

**Precondition to ratification (canon-literal):** (a) appliance benchmark completed against smallest registered-family candidate on real appliance hardware; (b) TCB-tier admission ceremony completed. Ruling before either would "circumvent them".

---

### R-15 · Named-persons verdict (release-gate) · AND · Watch Learning Amendment v1 · initial certificate-library seed

**⚠️ TWO DIFFERENT R-15 IDs live in the disk:**

**R-15(a) · Audio-POC release-gate KDPA-named-persons verdict.**

**Status:** ~~**OPEN · release-gate**~~ **→ RATIFIED (TOKENIZED) 2026-09-15T~03:55Z** (owner ruling packet · RULING_LEDGER row 19 in RATIFIED · wiring wave `W-RELEASE-GATE-PILOT-LIFT` CP-RG2).

**Ratification value:** `TOKENIZED`. Owner-verbatim: *"People's names are tokenized before anything leaves — placeholder tokens per custody class (Pull Seam identity-never-crosses). named_persons_verdict resolves to TOKENIZED for release purposes; build/wire the tokenization step into the transcript release path (tests-first)."*

**Prior verbatim anchor (kept for lineage):**

**Verbatim (`notes/W_AUDIO_POC_wave_close.md:85`):**
> "R-7 (KDPA), R-15 (named-persons), R-16 (transfer-basis), R-17 (licence class hardening) all PENDING on your side per still-blocked list. Until any of the three non-licence verdicts land, `admit_transcript_release` DETERMINISTICALLY refuses every write-back — which is the CORRECT structural posture, not a defect."

**Verbatim (`notes/W_AUDIO_POC_wave_close.md:118`):**
> "Ratify the three non-licence verdicts on `TranscriptArtefact` (R-7 KDPA · R-15 named-persons · R-16 transfer-basis) at your convenience. With `licence_class:owner_full_rights` (already ratified per Ruling #2), that unblocks the release-gate for `transcript_text_only` tier automatically — no code change needed."

**Behavior currently defaulted:** `TranscriptArtefact.named_persons_verdict = "PENDING"` at construction → `admit_transcript_release` raises `TranscriptVerdictPending` on any transcript release call. Every write-back deterministically refuses.

**Ratifying R-15(a) unblocks:** In combination with R-7 (KDPA) + R-16 (transfer-basis) + already-ratified R-17-licence, the release-gate for the SAFE tier `transcript_text_only` admits automatically. Audio-POC end-to-end gap-fill flow becomes runnable.

---

**R-15(b) · Watch Learning Amendment v1 · initial certificate-library seed.**

**Verbatim (`notes/MILESTONE_PROMISE_BINDING_20260913.md:13`):**
> "**Open rulings introduced by Watch Learning Amendment v1**: **R-15** (initial certificate library seed) · **R-16** (ratifier role + research cadence) · **R-17** (capability-class granularity). Filed in `RULING_LEDGER.md` (documentary; no wave)."

**Verbatim (`notes/MILESTONE_PROMISE_BINDING_20260913.md:12`):**
> "**S-7 status flip** (2026-09-13 · Watch Learning Amendment v1 L-2 + L-4) — was 'Absent → gap' per Amendment 1; now **'Absent → new (spec-closed, 13 Sep 2026)'**. Discharged **inside W-WATCH-STACK** (M3). Not built. Open owner-input rulings: R-15, R-16."

**Behavior currently defaulted:** M3 W-WATCH-STACK Watch Learning surface (`services/watch/`) carries the certificate-requirement library at Doc-3 A5 seam + A5.22 research loop with **empty seed** (spec-closed, not populated). Cadence unset.

**Ratifying R-15(b) unblocks:** Watch Learning surface goes from spec-closed to spec-and-seed-populated. Watch's own-liveness attestation + capability admission gain their initial certificate-library set for verdict-certificate emission (S-28 · S-29).

---

### R-16 · Transfer-basis verdict (release-gate) · AND · Watch Learning Amendment v1 · ratifier role + research cadence

**R-16(a) · Audio-POC release-gate KDPA-transfer-basis verdict.**

**Status:** ~~**OPEN · release-gate**~~ **→ RATIFIED (DERIVATIVE_ONLY_VIA_PULL_SEAM) 2026-09-15T~03:55Z** (owner ruling packet · RULING_LEDGER row 20 in RATIFIED · wiring wave `W-RELEASE-GATE-PILOT-LIFT` CP-RG3+CP-RG4).

**Ratification value:** `DERIVATIVE_ONLY_VIA_PULL_SEAM`. Owner-verbatim: *"transfer_basis resolves to derived-intelligence-only: derivatives (attributes, features, transcripts-as-derived-text with tokenized identities) may cross; raw estate data never does except via the outer gate."*

**Prior verbatim anchor (kept for lineage):**

**Verbatim (`notes/W_AUDIO_POC_wave_close.md:85,118`):** (same block as R-15(a) above).

**Behavior currently defaulted:** `TranscriptArtefact.transfer_basis = "PENDING"` at construction → `admit_transcript_release` raises `TranscriptVerdictPending`. Every write-back deterministically refuses.

**Ratifying R-16(a) unblocks:** In combination with R-7 + R-15(a) + R-17-licence, release-gate admits `transcript_text_only` tier. Same unblock as R-15(a) above.

---

**R-16(b) · Watch Learning Amendment v1 · ratifier role + research cadence.**

**Verbatim (`notes/MILESTONE_PROMISE_BINDING_20260913.md:13`):**
> "**R-16** (ratifier role + research cadence)"

**Behavior currently defaulted:** Watch Learning research-loop cadence unset; ratifier role for certificate-library additions unbound. `services/watch/` Learning surface accepts no additions currently (spec-closed).

**Ratifying R-16(b) unblocks:** Named ratifier role for the Watch Learning certificate-library ceremony. Research-loop cadence set. New certificates admissible into the library on the stated cadence with the ratified role countersigning.

---

### R-17 · Licence-class hardening (release-gate) · AND · Watch Learning Amendment v1 · capability-class granularity

**R-17(a) · Audio-POC release-gate licence-class hardening.**

**Verbatim (`notes/W_AUDIO_POC_wave_close.md:85`):**
> "R-17 (licence class hardening)"

**Behavior currently defaulted:** Canon-ratified `licence_class:owner_full_rights` (Ruling #2 · DECISIONS.md 2026-09-12T~12:00Z) admits the `transcript_text_only` tier when the other three verdicts land. `TranscriptArtefact.licence_class` accepts the ratified value; "hardening" refers to adding refusal-invariant granularity for other tiers or new classes.

**Ratifying R-17(a) unblocks:** Extended licence-class taxonomy admissibility for non-full-rights tiers. Not currently blocking end-to-end (the SAFE tier already has `owner_full_rights`); ratification unblocks tighter tiers.

---

**R-17(b) · Watch Learning Amendment v1 · capability-class granularity.**

**Verbatim (`notes/MILESTONE_PROMISE_BINDING_20260913.md:13`):**
> "**R-17** (capability-class granularity)"

**Behavior currently defaulted:** Watch Learning capability-admission surface (S-29 · L-5) carries default (coarse) capability-class granularity. Fine-grained per-capability admission ceremony rows unset.

**Ratifying R-17(b) unblocks:** Fine-grained capability-class granularity for the AC-15..AC-18 rows (M3 addendum). Enables the Watch Learning capability-admission ceremony at the granularity the owner specifies.

---

### BC-3 · Business Continuity Annex §3 · Recovery-point objective (RPO)

**Status:** ~~**OPEN · DEFAULT-PENDING-OVERRIDE**~~ **→ DYNAMIC-RECOVERY-PACKET-DIRECTION 2026-09-15T~03:55Z** (owner rejects the static-number framing · owner-verbatim: *"DO NOT SET A STATIC NUMBER · BUILD THE DYNAMIC-RECOVERY DECISION PACKET"*).

**Packet authored this turn:** `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md` (four tiers: GPU-checkpointing / ledger-WAL / WORM-artefacts / site-loss warm-standby · 18 invariants for post-ratification implementation wave `W-BC-DYNAMIC-RECOVERY-BUILD`).

**Owner ratifies THE PACKET** — the packet's per-tier RPO/RTO/cost matrix + Tier 3 lock-mode choice + Tier 4 site-loss regime + drill cadence — via the checklist in packet §J.

**Prior verbatim anchor (kept for lineage):**

**Verbatim (`notes/W_M3_SW10_BCA_S10_S11_BC1_BC2_close.md:42`):**
> "BC-3 (RPO) and BC-4 (site-loss) remain open per canon §3. This sub-wave preserves the DEFAULT-PENDING-OVERRIDE markers so that any silent flip breaks the ratchet."

**Verbatim in-code marker (`backend/services/business_continuity/anchors.py:91-92`):**
> "BC_3_PENDING_OVERRIDE: str = "DEFAULT-PENDING-OVERRIDE""
> "BC_4_PENDING_OVERRIDE: str = "DEFAULT-PENDING-OVERRIDE""

**Verbatim invariant discipline (`notes/W_M3_SW10_BCA_S10_S11_BC1_BC2_close.md:29`):**
> "BC-3 + BC-4 markers preserved as `DEFAULT-PENDING-OVERRIDE` — silent flip forbidden until owner rules RPO / site-loss."

**Behavior currently defaulted:**
- Recovery-point objective **unset**. `BC_3_PENDING_OVERRIDE = "DEFAULT-PENDING-OVERRIDE"` string sentinel.
- Any code path that would set a concrete RPO value → invariant-tested to raise; silent flip breaks the ratchet.
- Ledger continuity RTO (S-10) IS set at 3,600 s (RATIFIED · CA1-N5); it is the RPO (data-loss window) that awaits ruling.

**Ratifying BC-3 unblocks:**
- BCA §3 recovery-point ceremony: how much data-loss (in seconds/minutes) the continuity policy tolerates on restoration.
- Continuity policy JSON's currently-null `recovery_point_seconds` slot bind.
- End-to-end BCA §3 discharge (currently partial via S-10 RTO only).

---

### BC-4 · Business Continuity Annex §3 · Site-loss recovery

**Status:** ~~**OPEN · DEFAULT-PENDING-OVERRIDE**~~ **→ DYNAMIC-RECOVERY-PACKET-DIRECTION 2026-09-15T~03:55Z** (same owner ruling as BC-3 · packet §E proposes warm-standby with pilot-light + active-active as priced alternatives).

**Packet authored:** `notes/BC_DYNAMIC_RECOVERY_PACKET_20260915.md` §E (Tier 4 · Site loss) · quarterly restore-drill invariants §E.4.

**Prior verbatim anchor (kept for lineage):**

**Same verbatim sources as BC-3.**

**Behavior currently defaulted:**
- Site-loss recovery procedure **unset**. `BC_4_PENDING_OVERRIDE = "DEFAULT-PENDING-OVERRIDE"` string sentinel.
- Invariant refuses silent flip.

**Ratifying BC-4 unblocks:**
- BCA §3 site-loss recovery ceremony: named alternate site, restoration procedure, countersignature roster for cross-site restoration.
- End-to-end BCA §3 site-loss discharge (currently zero — no procedure exists).

---

### S-24 · Finding-raiser conformance

**Verbatim (`notes/MASTER_TRACEABILITY_AUDIT_20260907.md:241`):**
> "| **W-S24-RAISER-CONFORMANCE** | `S-24 · Doc 3 A5.2 · A5.14` | Finding-raiser held to same conformance as target · friction charged to raiser · agent-raised finding never input to severance | Two finding classes D and A tracked separately · never merged · drift accrues on raiser when finding not borne out | M |"

**Verbatim (`notes/MILESTONE_PROMISE_BINDING_20260913.md:310`):**
> "**`S-24` · Raiser held to same conformance as target** (proposed A5.17) — discharged by M3's Class-D/Class-A finding mechanism + lineage collapse."

**Status:** M3 W-WATCH-STACK Class-D / Class-A finding mechanism lands (spec-closed inside W-WATCH-STACK SW2 core), enforcing:
- Finding-raiser and finding-target both subject to same conformance measure.
- Friction charge accrues to raiser when the finding is not borne out.
- Class-D (drift) and Class-A (agent-raised) findings tracked separately, never merged.
- Agent-raised finding never input to severance rung.

**Verbatim in-code posture:** `services/watch/` carries the finding-mechanism scaffolding. The mechanism is spec-closed; **not built** per `MILESTONE_PROMISE_BINDING §M3` STATUS.

**Behavior currently defaulted:**
- Finding-raiser conformance-check pathway unset until Class-D/Class-A finding surface lands in W-WATCH-STACK's remainder.
- No agent-raised finding surface currently exists → S-24's "never input to severance" holds vacuously.

**Ratifying S-24 unblocks:**
- Class-D / Class-A finding surface production build (not just spec-close).
- Watch Class-D/Class-A drift-accrual accountant, currently absent.
- Proposed A5.17 canon-side landing of the raiser-conformance clause.

**On the pending list this row IS listed** *"Owner ratifications R-7/R-15/R-16/R-17/BC-3/BC-4/S-24/R-13/R-14"* — S-24 requires an owner ratification of the proposed A5.17 landing before the finding surface admits agent-raised findings into the closed six-signal registry (S-14 · A5.2).

---

## §B · Drift items from Audio Plane v1.0 audit (D7, D9, D10, D11) + D12

### D7 · TranscriptArtefact missing `codec_version` carrier

**Verbatim (`notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md:57`):**
> "D7 | `TranscriptArtefact` frozen 5-field: `tier, kdpa_verdict, named_persons_verdict, transfer_basis, licence_class`. **No `codec_version`.** | *'codec_version is a mandatory field of every downstream artifact's provenance. A transcript states which codec produced its tokens.'* | v1.0 §3.2 P048 | **DRIFT** on artefacts produced by the estate's own future codec. NOT-YET-IN-SCOPE for legacy OBS transcripts (no codec of ours produced them). **Recommended follow-on:** extend `TranscriptArtefact` with an optional `codec_version: Optional[str] = None` carrier that becomes MANDATORY when tier ∈ {estate-codec-produced}. **Owner rules on the extension.**"

**Verbatim (`notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md:44`):**
> "D4 | `TranscriptEntry` frozen 7-field ... same file-level shape; no `codec_version`, no `languages[]`. ... **NOT-YET-IN-SCOPE for existing OBS transcripts** — those were produced by a legacy path predating v1.0's codec_version mandate; they cannot retroactively carry `codec_version` because no codec produced them. **However for FUTURE transcripts produced by the estate's own audio pipeline, v1.0 §3.3 P055 will bite.** Registered as **DRIFT-FUTURE**."

**Behavior currently defaulted:**
- `TranscriptArtefact` frozen 5-field shape: `tier`, `kdpa_verdict`, `named_persons_verdict`, `transfer_basis`, `licence_class`. No `codec_version` slot.
- Legacy OBS transcripts (produced by pre-v1.0 external path) admissible without `codec_version` — correct per canon (canon rejects "downstream artifact lacking codec_version" — legacy artifacts are grandfathered, not "downstream" in v1.0's sense).
- Future estate-codec-produced transcripts have no compulsion path yet.

**Ratifying D7 unblocks:**
- `TranscriptArtefact` extension with `codec_version: Optional[str] = None`.
- Invariant addition making `codec_version` MANDATORY when tier ∈ {estate-codec-produced} (concrete tier list requires owner naming).
- Release-gate refusal path for future estate-codec artefacts lacking `codec_version`.
- v1.0 §3.3 P055 conformance for the future codec-service (N4 backlog).

---

### D9 · admit_transcript_release does not write receipt-before-result (Pull Seam drift)

**Verbatim (`notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md:59`):**
> "D9 | `admit_transcript_release` writes a receipt before returning? | *'Each operation writes a receipt … The receipt is written before the result is returned. If it cannot be written, the operation is refused.'* | Pull Seam §2 P7 (P036) | **NOT-YET-IN-SCOPE.** `admit_transcript_release` returns None on success; there is no explicit receipt-write step wired into the surface today. The audio-poc `gap_fill_writer.py` writes a distinct kind of receipt, but the release-gate itself does not. Marked as **DRIFT-PULL-SEAM** (this ties into the Pull Seam Stage-2 recommendation about the unified `Receipt.v0` schema)."

**Behavior currently defaulted:**
- `admit_transcript_release(artefact) -> None` returns silently on success; no receipt written by this function.
- Adjacent surface `services/audio_poc/gap_fill_writer.py::emit_gap_fill_receipt` writes a distinct receipt kind for the write-back flow.
- No unified `Receipt.v0` schema exists; each site produces its own local receipt shape.

**Ratifying D9 unblocks:**
- Pull Seam §2 P7 P036 verbatim compliance across every operation surface (universal receipt-before-result).
- Unified `Receipt.v0` schema landing.
- W-PULL-SEAM-RECEIPT-UNIFY wave charter (currently unchartered).
- Refusal-invariant for operations that cannot write their receipt (Pull Seam verbatim: "If it cannot be written, the operation is refused").

---

### D10 · Silero VAD · INFERRED · in-repo but not canon-named

**Verbatim (`notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md:65`):**
> "D10 | `services/perception/eab_1_pipeline/a1_vad.py` — **Silero VAD** wrapper; registry-pinned in `models_registry.v0.json` | Silero is not named in canon text. Canon-4 §50.1 M-11: *'Speaker overlap and call-in diarisation ⎢ Open diarisation stacks and overlap-aware recipes.'* (starting-point clause · unnamed) | Canon-4 §50.1 · M-11 | **INFERRED · in-repo but not canon-named.** Silero fits the 'open diarisation stacks' starting-point family but is not itself named. Requires owner ratification per Verbatim-canon standing rule."

**Behavior currently defaulted:**
- Silero VAD wired at `backend/services/perception/eab_1_pipeline/a1_vad.py`.
- Registry-pinned in `models_registry.v0.json` as an INFERRED starting-point in the "open diarisation stacks" family.
- Verbatim-canon standing rule (DECISIONS 2026-09-15T~01:40Z) flags this as pending owner ratification.

**Ratifying D10 unblocks:**
- Silero VAD formally admitted as the canon-named starting-point for VAD in the estate.
- INFERRED flag removed from the model spec citations.
- Canon §50.1 M-11 discharge with Silero as the named-adopted starting point.

**Alternative disposition:** owner may name a different VAD; current wiring falls under the "starting-point family, not adopted itself" clause and is subject to substitution on ratification.

---

### D11 · pyannote/speaker-diarization-3.1 · INFERRED · in-repo but not canon-named

**Verbatim (`notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md:66`):**
> "D11 | `services/layer_b/diarization/pyannote_provider.py` — **pyannote/speaker-diarization-3.1** | Same as D10 — canon names starting points but not this specific model | Canon-4 §50.1 · M-11 | **INFERRED · in-repo but not canon-named.** Same disposition as D10."

**Behavior currently defaulted:**
- pyannote/speaker-diarization-3.1 wired at `backend/services/layer_b/diarization/pyannote_provider.py`.
- Registry-pinned in `models_registry.v0.json` as an INFERRED starting-point.
- Verbatim-canon standing rule flags pending owner ratification.

**Ratifying D11 unblocks:**
- pyannote/speaker-diarization-3.1 formally admitted as the canon-named starting-point for speaker-diarization.
- INFERRED flag removed.
- Canon §50.1 M-11 diarization discharge with pyannote as the named-adopted starting point.

**Alternative disposition:** substitutable on owner naming; D10 + D11 typically ruled together (VAD + diarization pair).

---

### D12 · whisper-tiny + faster-whisper (ctranslate2) · CI-fixture straddle · POC gate

**Status:** ~~**STILL HELD · owner rules after census**~~ **→ APPROVED (bounded POC) 2026-09-15T~03:55Z** (owner ruling packet · RULING_LEDGER row 21 in RATIFIED).

**Ratification value:** APPROVED for bounded POC. Owner-verbatim: *"After the census completes: run the transcription pipe-proof with the canon CI fixture (whisper-tiny + faster-whisper) on a SMALL BOUNDED set of real NAS files (single-digit count), on the GPU hosts, all outputs labeled POC-NOT-PRODUCTION in provenance, receipts banked. Production model selection still follows census activation per §A17.11 — the POC does not pre-empt it."*

**Sequencing (owner verbatim):** fires AFTER census + AFTER `W-RELEASE-GATE-PILOT-LIFT` lands (so D12 outputs pass through the tokenized/derivative-only gate).

**Bounded parameters:**
- **File count:** single-digit count (owner verbatim).
- **Compute:** GPU hosts `akki-vm` / `akki-vm-ii` (per GPU-AVAILABLE verdict 2026-09-15T~02:45Z).
- **Provenance label:** `poc_flag = "POC-NOT-PRODUCTION"` on every output (owner-mandated).
- **Receipts:** banked under `phase0/d12_poc_receipts/<yyyymmddThhmmssZ>_<file_stem>.json`.

**Prior verbatim anchor (kept for lineage):**

**Verbatim (`notes/AUDIO_PLANE_V1_DRIFT_AUDIT_20260914.md:67`):**
> "D12 | Owner-suggested POC target: **whisper-tiny + faster-whisper (ctranslate2)** | Canon-17-19 §A17.10 (M-01, M-02): *'The registry seeds with whisper-tiny … backend: faster-whisper (ctranslate2) … CI CPU-mode ASR fixture model. NOT for production use.'* | Canon-17-19 §A17.10 | **MATCH for CI/POC path.** The POC therefore proceeds against the canon-named CI-fixture. Straddles the CI-vs-production line at the moment we transcribe REAL NAS bytes (production data on a CI model). Marked **DEFAULT-PENDING-OVERRIDE** — owner rules whether the POC on real data may run against the CI fixture, or a wave must charter production-model selection first."

**Verbatim owner reaffirmation this session (`STATE/DECISIONS.md` 2026-09-15T~02:35Z clause 2):**
> "**D12 (CI-fixture whisper-tiny transcription POC): still OPEN — do NOT run.** Owner rules after census results."

**Behavior currently defaulted:**
- D12 STILL HELD across the entire W-CENSUS-CANON-ALIGN wave.
- No transcription-POC work opened in the wave.
- `services/audio_poc/hf_transcribe.py` mechanism exists (routed to `router.huggingface.co/hf-inference/...`) but wired against the HF Inference-Providers routing — whisper-small was probed and not hosted under `hf-inference` (BLOCKER-HF-A5-01 · `notes/W_AUDIO_POC_wave_close.md:78`).
- Estate-side transcription-server host+creds MISSING BIND (blocker on standing list).

**Ratifying D12 unblocks:**
- POC transcription against real NAS bytes using the canon-CI-fixture (whisper-tiny + faster-whisper), producing gap-fill transcripts under the SAFE tier release-gate.
- OR alternatively — if the owner rules a production-model selection wave first — chartering `W-AUDIO-PROD-MODEL-SELECT` before any real-data transcription.
- Also gates the DECISIONS 2026-09-15T~02:45Z routing note: "future model-bearing waves route to akki-vm + akki-vm-ii via `services/training_runner/ssh_seam.py`" — D12's disposition names which model gets first flight.

**Owner-stated timing:** *"Owner rules after census results."* — D12 disposition unblocks post-Item-3-census.

---

## §C · Position-redaction acknowledgement

Every row above:
- Cites source-file paths and line numbers but does NOT echo credential material, host IPs, SSH usernames, key files, or PII of any kind.
- Preserves owner-side scrub directives verbatim (R-14 engine name scrub 2026-09-14; every occurrence rendered as neutral bracketed descriptor).
- Cites owner verbatim quotes with UTC-timestamped ruling anchors so the ledger can be cross-referenced against DECISIONS.md without re-quoting confidential ratification content.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
