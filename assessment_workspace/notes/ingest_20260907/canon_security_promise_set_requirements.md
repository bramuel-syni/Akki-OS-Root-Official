# Security Assurance Promise Set · Line-by-Line Extraction

**Source:** `canon/drops/20260907/raw/security_assurance_promise_set.xlsx` (sha256 `f824056d…`)  
**Extracted:** `canon/drops/20260907/extracted/text/security_assurance_promise_set.md`  
**Discipline:** every promise + standard + status + bound/ruling column reproduced verbatim from the xlsx.

Sheet 1 (`Security Assurance Set`): 27 rows. Sheet 2 (`Legend`): 7 rows.

## §A · Composite umbrella row

- **#6 · Promise #6 (Doc 3, composite):** "The platform continuously watches everything happening across the estate and the AI it runs…" — composite, true iff S-1 through S-21 all hold; false if any one fails, regardless of the others.
  - Standard: — (composite; see S-1..S-21)
  - Status: **By design**

## §B · S-1..S-21 (original set, per Doc 3)

| ID | Doc | Promise (verbatim) | Standard | Status | Bound/Ruling | Where It Lives |
|---|---|---|---|---|---|---|
| S-1 | Doc 3 | "The system will observe every actor, input, and action across the estate and the AI it runs, with no path by which any of the three reaches the estate or a model outside that observation." | NIST SP 800-53 SI-4 · CSF 2.0 DE.CM-01/09 | **Present** | Structural — two independent proofs (static, runtime) | A3 "Totality of sight"; A6 truth-condition 1 |
| S-2 | Doc 3 | "The system will detect the machine-speed attack, the slow play beneath every threshold, and the authorised attack that never breaks a rule — each by a distinct, named mechanism." | CC FAU_SAA.2 · NIST SI-4(24) · CSF DE.CM-09 | **Present** | Unruled — detection latency per shape not confirmed | A3 second property; #7 link |
| S-3 | Doc 3 | "The system will route probabilistic suspicion to friction, a narrowed envelope, or the mirage, and will convict only once the actor's own conduct converts suspicion into certainty." | CC FAU_ARP.1 · due-process analogues | **Present** | Ruled mechanism — mirage entry threshold baseline-period-deferred | A5.6; C1 |
| S-4 | Doc 3 | "The system will act on a four-rung ladder — annotate, shape, contain, sever — bounded by a blast budget per window and a friction budget on legitimate work." | CC FAU_ARP.1 · NIST IR-4 · CSF RS.MA | **Present** | Ruled mechanism, **values unruled** — blast-budget share and friction ceiling named, not set | A5.14 |
| S-5 | Doc 3 | "The system will make every autonomous act reversible, bounded, and witnessed — a time-to-live on every action, atomic act-and-attest, peer-countersigned." | NIST IR-4 · CC FPT_RCV | **Present** | Unruled — action TTL named, no value confirmed | A5.3 |
| S-6 | Doc 3 | "The system will write every verdict, action, attestation, and mark to the one authoritative record before the next gate is crossed, including its own mistakes." | NIST AU-2, AU-3 · CC FAU_GEN.1 · ISO 27001 8.15 | **Present** | Structural; timing qualitative — "before the next gate," no numeric latency confirmed | A3; A5.5 |
| S-7 | Doc 3 | ⚠ **SPECIFICATION GAP — no mechanism specified.** Doc 3's plain-language promise (A1) states platform "learns from every attack it defeats"; every A5 clause on learning (A5.7, A5.8, A5.12) constrains what may NOT happen. None specifies what does update, on what evidence, at what layer. | CC FAU_SAA (would require specified mechanism) · ISO 27001 5.27 · CSF 2.0 improvement functions | **Absent → gap** | Unruled — no mechanism exists to bound | Gap between A1 (plain-language promise) and A5 (constrains learning, never specifies it) |
| S-8 | Doc 3 | "The system will exercise every response rail on a standing drill cadence — full loop, both engines, latencies measured — and a rail not demonstrated firing is not in force." | NIST CA-7 · ISO 27001 8.16 · CC ATE | **Present** | Ruled mechanism, cadence value unruled | A5.13; A3 |
| S-9 | Doc 3 | "The system will, on release from the mirage, replay the actor's mirage-period work against the real platform, or tell them plainly it did not land." | Nearest: adverse-action notice · GDPR Art. 22; Kenya DPA 2019 s.35 | **Present** | Ruled mechanism — reconciliation mode baseline-period-deferred | C1, "reconciliation duty" |
| S-10 | Wave E · CA1-N5 (no document home yet — proposed Doc 3 Part D) | "The system will restore Ledger continuity within 3,600 seconds, under independent countersign, following any continuity-affecting incident." | NIST CP-10 / IR-4 · ISO 27001 5.29/5.30 · CSF 2.0 RC.RP | **Present** | Ruled — CA1-N5, RTO 3,600s, DEFAULT-class | Wave E ruling CA1-N5 |
| S-11 | Wave E · CA1-N2 | "The system will issue breach notification within 72 hours of a qualifying incident, to the parties and authorities the incident requires." | NIST IR-6 · ISO 27001 5.26 · Kenya DPA 2019 · GDPR Art. 33 | **Present** | Ruled — CA1-N2, 72-hour duty | Wave E ruling CA1-N2 |
| S-12 | Doc 3 | "The system will fail closed independent of the Watch — custody gates fail closed on their own, with or without the Watch above them." | CC FPT_FLS.1 · NIST SC-24 · IEC 61508 | **Present** | Structural | A5.9 parenthetical |
| S-13 | Doc 3 | "The system will never let detection hold power to act, or response hold judgement to interpret — Macho asserts facts only; Mkono executes signed policy only; one verdict is the sole interface." | CC FAU_ARP · detect-never-decide doctrine | **Present** | Structural | A5.1; C2 |
| S-14 | Doc 3 | "The system will never unlock its maximum autonomous force from a signal an outsider could fabricate — only from a closed, six-member registry of unfakeable signals." | No direct security-standard analogue — internal cross-ref to Solva (Doc 4) | **Present** | Structural; registry membership baseline-period-deferred | A5.2 |
| S-15 | Doc 3 | "The system will never let loss of behavioural conformance alone convict an actor — the worst it can do to an innocent actor is return them to baseline verification." | GDPR Art. 22 · Kenya DPA 2019 s.35 — legal analogues | **Present** | Structural, constitutional per A5.7 — not tunable | A5.7 |
| S-16 | Doc 3 | "The system will hold a ruled, deterministic floor beneath every adaptive layer, moved only by a delayed, two-signature ceremony that is itself a monitored tripwire." | NIST AC-3 · CC FDP_ACF · Doc 0 Att 7 | **Present** | Structural — floor values conservative defaults during baseline period | A5.8 |
| S-17 | Doc 3 | "The system will never delete — the Watch can stop anything and erase nothing; destruction remains solely the separately-authorised act specified elsewhere." | NIST AU-9 · CC FAU_STG.1 | **Present** | Structural | A3; A5.3 |
| S-18 | Doc 3 | "The system will hold behavioural-conformance profiles as non-exportable, tenant-keyed, purpose-bound armoury — never rendered to any surface, export, or analytic, including the Watch's own console." | NIST SC-28 · no direct standard for "never render to own console" | **Present** | Structural; retention posture baseline-period-deferred | A5.12 |
| S-19 | Doc 3 | "The system will have its own liveness attested by a component holding no Watch credentials, will treat Watch silence itself as an alarm, and will subject its own records to a standing break-in test that must fail." | CC ADV_ARC.1 self-protection · NIST SI-4 · reference-monitor tamper-resistance | **Present** | Structural; break-in test cadence unruled | A5.9; C3 |
| S-20 | Doc 3 | "The system will execute every task under exactly one authority's identity and scope — a task that could see like security and decide like governance is unrepresentable, not merely forbidden." | NIST AC-6 · CC FDP_ACC | **Present** | Structural — unrepresentable, not policy-enforced | A5.10; A5.11 |
| S-21 | Doc 3 | "The system will let the mirage deceive outward only — every mirage interaction writes truthfully marked records, and mirage state shares no store with production." | MITRE Engage · NIST SI-4 deception guidance | **Present** | Structural — mirage entry threshold baseline-period-deferred | A5.5; C1 |

## §C · S-22..S-25 (added by Trojan/Whisper amendments · 2026-09-05)

| ID | Doc | Promise (verbatim) | Standard | Status | Bound/Ruling | Where It Lives |
|---|---|---|---|---|---|---|
| S-22 | Doc 3 (proposed A5.15) · DAP-33 | "The system will inspect what leaves, not only who sends it — every output leaving a component boundary is checked for controlled-unit content and tagged ADVISORY where it recommends, ranks, proposes, or evaluates an action." | Solva assertion floor · DLP practice at component boundary — no direct security-conformance standard | **Absent → new** | Ruled — reproduction threshold and probe design are R-8 (DEFAULT-class, conservative, revised on evidence) | Security Amendments W-1; gate sits on deterministic side of verdict seam |
| S-23 | Doc 0 Att 3 · Doc 3 (proposed A5.18) · DAP-34 | "The system will treat a coalition as one actor — cumulative conduct across principals sharing a party, a mandate lineage, or a detected coordination signature is evaluated jointly, not per principal." | Sybil resistance (Douceur 2002) · Byzantine fault tolerance | **Absent → new** | Structural for shared-party and shared-lineage; coordination-signature threshold is R-11 (friction-only under A5.2) | Security Amendments W-4; coalition is connected component of admission graph |
| S-24 | Doc 3 (proposed A5.17) | "The system will hold the raiser of a finding to the same conformance as its target — a finding is conduct; the friction it causes is charged to the raiser's budget, not the target's; a finding not borne out accrues drift on the raiser; and no agent-raised finding, at any count, is an input to severance." | A5.2 · A5.14 · BFT source weighting | **Absent → new** | Structural — A5.2 registry unchanged; friction debit follows A5.14 | Security Amendments W-3; two finding classes D and A, never merged |
| S-25 | DAP-35, DAP-36 · Doc 0 Att 7 (new mandatory baseline) | "The system will bound what the estate releases in total — across all parties, all operations, all time — so that no combination of parties can reconstruct what none of them is entitled to. Breaching the bound is a floor violation, severance-eligible without inference." | Differential privacy (Dwork et al. 2006) · NIST SP 800-188 (2023) · DP-SGD (Abadi et al. 2016) | **Absent → new** | Ruled — the budget itself is R-7; per-run (ε, δ) is R-9. The floor never learns (A5.8) | Security Amendments W-7, W-8; converts coalition prevention from detection into ruling |

## §D · Legend (verbatim)

- **Scope** — Decomposes Promise #6 (Doc 3) into 21 assurance statements (S-1..S-21), plus S-22..S-25 added by the Security Amendments — Trojan Artefacts and Whisper Threats (5 Sep 2026). S-10, S-11 sourced from Wave E rulings with no document home yet. Promises #7 and #26 are unchanged and cited, not reproduced.
- **Standard column** — clause each promise answers to. [V]/[K]/[P] confidence not marked per-cell here; treat as [K] unless a document says otherwise.
- **Bound/Ruling column** — Structural = no numeric bound applies. Ruled = specific value set (cites the ruling). Baseline-period-deferred = Doc 3's mechanism (conservative default until defined observation period, then set by evidence). Unruled = bound named in A5 text with no value confirmed — a real gap.
- **Status colours** — Green = Present. Blue = Absent → new (ruled value, no document promise yet). Amber = Absent → gap (no mechanism specified anywhere). Grey = By design (composite/umbrella).
- **S-7** — The one promise marked as specification gap rather than asserted.
- **Removed from this set** — "Never run in shadow" (A5.4) — deployment doctrine, not runtime assurance. Relocated to Doc 0 Attribute 9 build requirements per Amendment 3.

## §E · Status tallies (this ingest wave)

- **Present (Structural or Ruled):** 20 · S-1, S-2, S-3, S-4, S-5, S-6, S-8, S-9, S-10, S-11, S-12, S-13, S-14, S-15, S-16, S-17, S-18, S-19, S-20, S-21
- **Absent → gap (no mechanism specified):** 1 · S-7 (LEARNING MECHANISM)
- **Absent → new (ruled, no document promise yet):** 4 · S-22, S-23, S-24, S-25
- **By design (composite umbrella):** 1 · #6
- **Total:** 26 rows in `Security Assurance Set` sheet (composite umbrella #6 + S-1..S-25)

## §F · Unruled bounds (6, per Trojan/Whisper Amendment 4)

Six named bounds with mechanism described but no numeric value confirmed (per Amendment 4, 2026-09-03):
1. S-2 detection latency per attack shape
2. S-4 blast-budget share
3. S-4 friction ceiling
4. S-5 action time-to-live
5. S-19 attestation-continuity interval
6. S-19 break-in test cadence
