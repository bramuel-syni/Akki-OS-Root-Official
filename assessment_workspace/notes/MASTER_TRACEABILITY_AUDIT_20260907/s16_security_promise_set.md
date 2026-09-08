# S16 · Security Assurance Promise Set S-1..S-25 + composite · Detail

**Source:** `canon/drops/20260907/raw/security_assurance_promise_set.xlsx` (sha256 `f824056d…`) · extracted at `canon/drops/20260907/extracted/text/security_assurance_promise_set.md` · verbatim quotes preserved in `notes/ingest_20260907/canon_security_promise_set_requirements.md`. Umbrella of Doc 3 Promise #6 (composite).

**Total rows: 26** (1 composite umbrella + 25 promises).

## §A · Row-by-row classification

| Row ID | Doc / Anchor | Promise (compressed) | Status (verbatim) | This audit classification | Code path / donor / gap · Evidence |
|---|---|---|---|---|---|
| S-comp | Doc 3 · Promise #6 | Continuously watches everything | **By design** (composite) | INVENTORY (composite; true iff S-1..S-21 hold) | — |
| S-1 | Doc 3 · A3 | Observe every actor/input/action with no bypass path | **Present** (Structural) | REUSE | RMS `synisense/watch/observe.py` (donor, ~500 LOC) + Extraction-Akki `backend/services/watch/` skeleton · LIFT-ADAPT · dual proofs (static + runtime) charter |
| S-2 | Doc 3 · A3 | Detect machine-speed attack, slow-play, authorised attack each by distinct mechanism | **Present** (Ruled mechanism, latency unruled) | REUSE (partial) | Grey Mirror donor at Exec-Core `grey_mirror/` (~300 LOC); slow-play + auth-attack mechanisms NEW |
| S-3 | Doc 3 · A5.6 · C1 | Route probabilistic suspicion to friction/narrowed/mirage; convict only on actor's conduct converting suspicion to certainty | **Present** (Ruled; mirage entry threshold baseline-period-deferred) | REUSE | Exec-Core `mirage/entry.py` (donor); mirage entry threshold ruling deferred (DEFAULT-PENDING-OVERRIDE) |
| S-4 | Doc 3 · A5.14 | Four-rung ladder (annotate/shape/contain/sever) bounded by blast + friction budgets | **Present** (Ruled mechanism, values unruled) | REUSE | RMS `watch/ladder.py` skeleton; blast-budget share + friction ceiling ruled-value pending |
| S-5 | Doc 3 · A5.3 | Every autonomous act reversible/bounded/witnessed · TTL + atomic act-and-attest + peer-countersigned | **Present** (Ruled; TTL value unconfirmed) | PARTIAL | Watch severance receipts exist in `phase0/severances/`; TTL value not set; peer-countersign NEW |
| S-6 | Doc 3 · A3 · A5.5 | Write every verdict/action/attestation/mark to Ledger BEFORE next gate | **Present** (Structural; timing qualitative) | PARTIAL | Ledger append exists; "before next gate" precondition check NEW |
| S-7 | Doc 3 · A1 (gap) | "Learns from every attack it defeats" | **Absent → gap** (no mechanism specified anywhere) | NEW | Charter **W-S7-LEARNING-MECHANISM** in master §E.3 |
| S-8 | Doc 3 · A5.13 · A3 | Standing drill cadence · full loop · both engines · latencies measured · un-demonstrated rail = not in force | **Present** (Ruled mechanism; cadence unruled) | PARTIAL | Drill discipline exists (mechanical RED per wave close); watch-specific drill cadence NEW |
| S-9 | Doc 3 · C1 | On release from mirage, replay actor's mirage-period work OR tell them plainly it did not land | **Present** (Ruled; reconciliation mode baseline-period-deferred) | NEW | Mirage-release replay NEW; adverse-action notice pattern GDPR Art. 22 |
| S-10 | Wave E · CA1-N5 | Restore Ledger continuity within 3,600s under independent countersign | **Present** (Ruled; CA1-N5, RTO 3600s, DEFAULT-class) | PARTIAL | Ratchet CA1-N5 landed W6 CP2 (test_ca1_n5_rto_landed exists); Ledger continuity mechanism partly wired |
| S-11 | Wave E · CA1-N2 | Breach notification within 72 hours to required parties + authorities | **Present** (Ruled; CA1-N2, 72-hour duty) | NEW | Breach notification workflow NEW · Kenya DPA + GDPR Art. 33 anchor |
| S-12 | Doc 3 · A5.9 | Fail closed independent of Watch · custody gates fail closed with or without Watch above | **Present** (Structural) | DONE | Shield chokepoint fails closed (BR-1.5 STATUS Met); dispatcher fails closed on child-death (test_dispatcher_advances_on_dead_trainer green) |
| S-13 | Doc 3 · A5.1 · C2 | Detection holds no power to act; response holds no judgement to interpret · Macho asserts, Mkono executes, one verdict | **Present** (Structural) | REUSE | Exec-Core Watch Macho/Mkono split (~800 LOC); import-assertion linter for two-faculty seam · charter W-WATCH-TWO-FACULTY-SEAM |
| S-14 | Doc 3 · A5.2 | Never unlock max autonomous force from outsider-fabricable signal · closed 6-member registry | **Present** (Structural; membership deferred) | NEW | Six-member unfakeable-signal registry NEW · Solva cross-ref |
| S-15 | Doc 3 · A5.7 | Loss of behavioural conformance alone never convicts · worst outcome for innocent = return to baseline | **Present** (Structural, constitutional) | REUSE (doctrine) | Watch verdict grammar preserves this; test_watch_never_convicts_on_conformance_alone NEW |
| S-16 | Doc 3 · A5.8 | Ruled deterministic floor beneath every adaptive layer · moved only by delayed 2-sig ceremony (monitored tripwire) | **Present** (Structural; floor values conservative default during baseline period) | PARTIAL | Ratchet floor + 2-commit pattern approximate this; formal 2-signatory ceremony NEW |
| S-17 | Doc 3 · A3 · A5.3 | Never delete · Watch stops nothing erases · destruction is separately-authorised act | **Present** (Structural) | DONE | Append-only phase0 records; deletion refused across watch and ledger paths |
| S-18 | Doc 3 · A5.12 | Behavioural-conformance profiles as non-exportable · tenant-keyed · purpose-bound · never rendered anywhere including Watch console | **Present** (Structural; retention posture deferred) | NEW | Non-exportable profile storage NEW · schema + never-render invariant NEW |
| S-19 | Doc 3 · A5.9 · C3 | Own liveness attested by non-Watch component · Watch silence itself is alarm · standing break-in test must fail | **Present** (Structural; break-in test cadence unruled) | NEW | Liveness attestation + break-in test discipline NEW |
| S-20 | Doc 3 · A5.10 · A5.11 | Every task under one authority · a task that could see-like-security + decide-like-governance is unrepresentable | **Present** (Structural — unrepresentable not policy-enforced) | REUSE | Exec-Core executor role scoping (donor ~200 LOC); unrepresentability at code level NEW |
| S-21 | Doc 3 · A5.5 · C1 | Mirage deceives outward only · every mirage interaction writes truthfully marked records · mirage state shares no store with production | **Present** (Structural) | REUSE | Exec-Core mirage store isolation (donor ~400 LOC) · charter W-MIRAGE-STORE-ISOLATION |
| S-22 | Doc 3 (proposed A5.15) · DAP-33 · via Trojan/Whisper W-1 | Inspect what leaves not only who sends · every output at component boundary checked for controlled-unit content · tagged ADVISORY where recommends/ranks/proposes/evaluates | **Absent → new** (Ruled; reproduction threshold + probe design are R-8, DEFAULT-class conservative) | NEW | Charter **W-S22-COMPONENT-BOUNDARY-INSPECTION** in master §E.3 |
| S-23 | Doc 0 Att 3 · Doc 3 (proposed A5.18) · DAP-34 · via Trojan/Whisper W-4 | Treat coalition as one actor · cumulative conduct across principals sharing party/mandate lineage/coordination-signature evaluated jointly | **Absent → new** (Structural for shared-party + shared-lineage; coordination-signature threshold is R-11 friction-only under A5.2) | NEW | Charter **W-S23-COALITION-JOINT-EVALUATION** in master §E.3 |
| S-24 | Doc 3 (proposed A5.17) · via Trojan/Whisper W-3 | Raiser of a finding held to same conformance as target · friction charged to raiser's budget · finding not borne out accrues drift on raiser · agent-raised finding never input to severance | **Absent → new** (Structural; A5.2 registry unchanged; friction debit follows A5.14) | NEW | Charter **W-S24-RAISER-CONFORMANCE** in master §E.3 |
| S-25 | DAP-35, DAP-36 · Doc 0 Att 7 new mandatory baseline · via Trojan/Whisper W-7, W-8 | Bound what estate releases in total across parties/operations/time · no combination reconstructs what none entitled to · breach = floor violation, severance-eligible without inference | **Absent → new** (Ruled; budget = R-7; per-run (ε, δ) = R-9; floor never learns per A5.8) | NEW | Charter **W-S25-CUMULATIVE-DISCLOSURE** / **W-ESTATE-RELEASE-BUDGET** (E.1) |

## §B · Unruled bounds (6 · from Trojan/Whisper Amendment 4)

Named but with mechanism only; no numeric value. Each is a follow-on ruling-required item — none currently blocking, but each becomes a wave-level charter when a numeric value lands.

1. **S-2 detection latency per attack shape** · DEFAULT-PENDING-OVERRIDE
2. **S-4 blast-budget share** · DEFAULT-PENDING-OVERRIDE
3. **S-4 friction ceiling** · DEFAULT-PENDING-OVERRIDE
4. **S-5 action time-to-live** · DEFAULT-PENDING-OVERRIDE
5. **S-19 attestation-continuity interval** · DEFAULT-PENDING-OVERRIDE
6. **S-19 break-in test cadence** · DEFAULT-PENDING-OVERRIDE

## §C · S16 rollup

| Bucket | Rows | % of 26 |
|---|--:|---:|
| DONE | 3 | 11.5% |
| PARTIAL | 5 | 19.2% |
| REUSE | 8 | 30.8% |
| NEW | 10 | 38.5% |

**Interpretation:** S-1..S-6, S-12..S-21 core promises are Doc 3 CANON with substantial reuse pool (Watch stack in Exec-Core + RMS + partial in Extraction-Akki). S-22..S-25 (Trojan/Whisper new promises) are all NEW; each becomes an E.3 wave. S-7 (learning-mechanism gap) is the highest-impact single unresolved item; without a mechanism ruling, the platform's plain-language promise "learns from every attack" is unfalsifiable.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law.
