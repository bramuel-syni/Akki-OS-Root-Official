READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_security_architecture_description_v1_requirements.md

**Source.** `canon/drops/20260909/raw/files_14.zip` → `Security_Architecture_Description_v1.docx` sha256 `2d41f6001d…` · 16,440 B. Extracted text `canon/drops/20260909/extracted/text/Security_Architecture_Description_v1.txt`.
**Spec id.** `security_architecture_v1`. Draft for owner ratification · closes **Doc 0 G-6**.
**Requirement answered (verbatim, Table 0 R0).** *"Common Criteria ADV_ARC.1: for every reference monitor, demonstrate non-bypassability, self-protection, domain separation, and secure initialisation."*
**Scope (verbatim, Table 0 R1).** Every candidate reference monitor named in `tcb_enumeration_v1`: SyniSense's chokepoint, Watch's Mkono, MOAC, DAP-31 distance gate, DAP-32 admission probe, QA-2 format gate.

---

## §A · New Security-Function-Policy rules (SEC-1..SEC-7 verbatim)

- **SEC-1** [Closes 1.1 gap]: *"SyniSense's custody-sequence policy and network allowlist MUST be integrity-verified at load — a signature or hash comparison against the value recorded in the Rule Registry — so that a runtime modification is detected, not merely prevented by the absence of an edit path."*
- **SEC-2** [Self-protection]: *"MOAC's acceptance criteria MUST be held in versioned, Rules-Service-governed configuration — the same discipline as SyniSense's custody policy — with integrity verified at load. No criterion is editable by the run it measures, by construction rather than by convention."*
- **SEC-3** [Domain separation]: *"MOAC operates entirely within Targeta's boundary and reads only the run artefacts Targeta produces. It does not query Solva, Mtafiti, or any other engine to reach its decision."*
- **SEC-4** [Secure initialisation]: *"MOAC MUST refuse to evaluate — not default-accept, not skip — if its criteria configuration is unset or fails integrity verification at load, on the same pattern as A17.9's execution-mode raise."*
- **SEC-5** [Non-bypassability, demonstrated not asserted]: *"Every path by which a run's result could be treated as accepted MUST be enumerated and shown to pass through MOAC's evaluation, in a build-time test comparable to SyniSense's negative-scan gate."*
- **SEC-6** [Secure initialisation, DAP-31]: *"DAP-31's probe MUST refuse to run — and MUST refuse egress by default in that state — if the reproduction threshold, sample size, or probe design values are unset. Absence of configuration is a refusal condition, not a bypass."*
- **SEC-7** [Secure initialisation, DAP-32]: *"DAP-32's battery MUST refuse to admit a model — default to refusal, not default to pass — if battery composition or deviation thresholds are unset."*

**Absorption note (verbatim §7):** *"SEC-4, SEC-6, and SEC-7 are the same rule applied three times: an unconfigured gate refuses. Worth ratifying once, as a platform-wide default under Attribute 11 (Failure Posture), rather than as three separate clauses that happen to say the same thing — flagged for the Failure Posture Enumeration (document 5 of this set) to absorb."* → Absorbed into **FP-2** at `canon_failure_posture_enumeration_v1_requirements.md §A`.

## §B · Reference-monitor property summary (§9, Table 8 verbatim)

| Monitor | Non-bypass | Self-protect | Domain sep. | Init |
|---|---|---|---|---|
| SyniSense chokepoint | Met | Partial (SEC-1) | Met | Met |
| Watch — Mkono | Met | Met | Met | Met |
| External witness | N/A | Met | Met | Ruling pending |
| MOAC | Proposed (SEC-5) | Proposed (SEC-2) | Proposed (SEC-3) | Proposed (SEC-4) |
| DAP-31 distance gate | Met | Met | Met | Proposed (SEC-6) |
| DAP-32 admission probe | Met | Met | Met | Proposed (SEC-7) |
| QA-2 format gate | Inferred | Open | Inferred | Open |

## §C · Grey Mirror exclusion (§3 verbatim)

*"Grey Mirror is not itself evaluated as a reference monitor. Per `tcb_enumeration_v1`, Macho is learned and holds no decision authority — 'it cannot block, throttle, mark, reroute, or notify. Its sole output is a verdict' (A2, verified verbatim). ADV_ARC.1 applies to components that mediate and decide; Macho detects and proposes."*

## §D · Amendments folded

- `Serving_Integrity_Amendment_v1 V-2` extends SEC-4/SEC-6/SEC-7 refuse-if-unset pattern **from configuration to the serving substrate** — DAP-31+/DAP-32+ inherit an SFP-8-conforming path or refuse.

## §E · Milestone binding

- **M2** — SEC-1..SEC-7 fold into Rules-Service catalog (verify SEC-1 hash-check at load) + W-DOC0-ATTR6-REFERENCE-MONITOR (governance-side second RM instance per Security_Promise_Set_Amendments Amendment 6).
- **M2** — QA-2 format gate `Open`/`Open` rows carried as `DEFAULT-PENDING-OVERRIDE` (lowest priority per §9).
- **M1** — DAP-31 + DAP-32 rows already in M1 building list; SEC-6/SEC-7 wire on 2E/2H close.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
