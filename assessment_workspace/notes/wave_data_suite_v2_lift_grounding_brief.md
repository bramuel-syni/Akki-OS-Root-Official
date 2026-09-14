READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# W-DATA-SUITE-V2-LIFT · wave grounding brief

**Wave:** `W-DATA-SUITE-V2-LIFT` (M5 SW2 · Task 2 per owner-amended sequence 2026-09-14).
**Wave class:** M · milestone content · case-agnostic donor lift.
**Template:** `W-SOLVA-V2-LIFT` close (8 CPs · +31 invariants · CP-S2 landed FIRST · executive-domain token strip · HALTs on non-token-strippable constructs).
**Ratchet at open:** **3929** (banked at W-AUDIO-POC close).
**Author:** main agent · 2026-09-14T~14:00Z.
**Prior state:** W-AUDIO-POC closed at CP-A6 (track-a `dc498fd` · master state committed).

---

## §A · Owner authorization (verbatim, 2026-09-14)

**Task 2 GO** (this session):
> "TASK 2 (AFTER W-AUDIO-POC CLOSES): W-DATA-SUITE-V2-LIFT Step 2. Owner has given the GO. Defaults DPO-D1 and DPO-D2 stand as proposed (no amendments received). Author the grounding brief, then build CP-D1 through CP-D8: case-agnostic donor lift from `analyze_workspace/`. Steps 0 + 1 are already closed; Step 2 discovery is complete — build directly on that discovery output, do not redo discovery. Same discipline: tests-first, double-green, two-commit pattern, ratchet up only."

**§A citation** (from earlier ruling, owner directive 2026-09-14):
> "M5 SW1 = W-DATA-SUITE-V2-LIFT (the case-agnostic donor lift, same discipline as W-SOLVA-V2-LIFT). Its TECHNICAL contract is already owner-ratified ON DISK — lift it from `notes/MILESTONE_PROMISE_BINDING_20260913.md` §M5 + the Phase-C plan §M5/§lift + the Data-Suite donor path in the Executive donor repos. That banked, ratified plan IS the authorization for the technical scope; §A cites the owner M5-go quote above. Do NOT invent scope; do NOT ask the owner to re-paste a contract that's already banked."

**Standing constraints held** (from resume brief 2026-09-14):
> "ALL testing via terminal pytest ONLY … testing sub-agent is STRICTLY BANNED. Double-green byte-match required for every wave close. LOCAL COMMITS ONLY. Two-commit pattern: code on `programme/track-a`, state/docs on `master`. NEVER push to remote. POSITION-REDACTION ONLY. EGRESS WINDOW 11:00–05:00 EAT. Tests-first invariant development. Ratchet may only go UP from 3929."

**Standing defaults (banked previously, still in effect):**
* `DPO-D1`: surfaces 2 and 3 are Analyze-family sibling views (Rapid feed vs Deep-Dive synthesis).
* `DPO-D2`: W-TRUST-SURFACE-v2 and W-EXECUTIVE-SUITE-v2-LIFT are OUT-OF-SESSION-SCOPE (owner's sequence enumerated exactly two waves for M5).

---

## §B · Canon anchors

* **DAP-Spec §A10 · Artefact egress remainder** — discharged by this wave: exports carry rights posture + hash + derivation from controlled units + terms cited.
* **Canon-1 §4.6 · Extension not proliferation** — Data-Suite is one workspace surface family, not a proliferation of sibling engines.
* **Canon-3 §9.3 · Append-only ledger spirit** — Data-Suite analysis records never overwrite; each session emits a new snapshot.
* **Canon-4 §22 · UnitRefs only** — export payloads return `UnitRef`s / hash-anchored derivations, not raw content.
* **Solva-V2-LIFT precedent (2026-09-13)** — same discipline: parameterless boundary signature FIRST · engine-shell skeletons · word-boundary executive-domain negative-scan · HALT non-token-strippable donor constructs.

**Executive-domain negative-scan token set** (verbatim from `W_SOLVA_V2_LIFT_close.md §B`):
`ceo · cfo · cto · coo · boardroom · c-suite · c_suite · non-executive director · non_executive_director · chair notes · chair_notes · mckinsey · executive briefing · board briefing · board grade · board-grade · corporate governance`.

**Donor sources** (on-disk, `repos/Akki-Executive-Core/backend/services/`):
* `analyze_workspace/` — primary Data-Suite donor (case-agnostic assumption per Step 2 discovery banked earlier).
* `analysis_lifecycle.py` — analysis state-machine skeleton donor.
* `workbook_analyzer/` — Deep-Dive synthesis skeleton donor (Analyze surface tab 2).

`repos/Akki-Executive-Final/backend/services/` **remains excluded** per §M5 Q3 DPO (unchanged).

---

## §C · Mechanism scope

New package `backend/services/data_suite_v2/`.  Modules land across 8 CPs; CP-D1 lands FIRST (parameterless workspace-boundary signature per Solva-V2 CP-S2 precedent).

| CP | Order | Focus | New modules |
|--:|--:|---|---|
| **CP-D1** | **1st** | Parameterless workspace-boundary signature `compute_surface(workspace: WorkspaceState) -> SurfaceClass`. Exactly one parameter. `SurfaceClass` closed 3-value enum. Contract `contracts/data_suite_workspace.py` with `WorkspaceState` + `SurfaceClass`. | `workspace_boundary.py` + contract file |
| CP-D2 | 2nd | Two-faculty seam: workspace state machine vs surface renderer separated by import assertion. AST-parsed negative-scan. | `workspace_state_machine.py` + `surface_renderer.py` |
| CP-D3 | 3rd | Source-registry contract: Data-Suite reads working-files list as `Sequence[UnitRef]` (Canon-4 §22 shape); no raw source content in the record. | `source_registry.py` |
| CP-D4 | 4th | Three Analyze-tab contracts: `AnalyzeRapid`, `AnalyzeDeepDive`, `AnalyzeSources` — each a frozen dataclass with `tab_kind` Literal. Fourth tab (Export) refused at construction. | `analyze_tabs.py` |
| CP-D5 | 5th | Analysis-session record (Canon-3 §9.3 append-only spirit) — `AnalysisSession` frozen; new sessions never overwrite. Snapshot fingerprint deterministic. | `analysis_session.py` |
| CP-D6 | 6th | Export-artefact contract (discharges DAP-A10) — `ExportArtefact` with 4 required carriers: `rights_posture`, `derivation_hash`, `derivation_unit_refs: Sequence[UnitRef]`, `terms_cited: Sequence[str]`. Refuses release if any carrier is empty. | `export_artefact.py` + `export_gate.py` |
| CP-D7 | 7th | Analysis-lifecycle state machine (donor: `analysis_lifecycle.py`) — case-agnostic state names `{DRAFT, PROCESSING, READY, ARCHIVED}`; strict transition matrix; illegal transitions raise. | `analysis_lifecycle.py` |
| CP-D8 | 8th | Case-agnostic donor lift: engine-shell skeletons at `services/data_suite_v2/engines/` (`analyze_workspace_engine.py`, `deep_dive_engine.py`) + word-boundary executive-domain negative-scan across `services/data_suite_v2/` + HALT for any donor construct not token-strippable. | `engines/*` |

**Estimated ratchet delta:** +36 to +48 invariants (average 5–6 per CP).  Ratchet target: **3929 → 3965–3977**.

---

## §D · Wave-honest limits (declared at open)

1. **E.1** DPO-D1 default stands: surfaces 2 and 3 are Analyze-family sibling views. If owner amends later, `analyze_tabs.py` structure can accommodate a 4th tab without breaking the closed-Literal check (add value + update test).
2. **E.2** Only `analyze_workspace/` + `analysis_lifecycle.py` + `workbook_analyzer/` donor paths are walked in the negative-scan.  Other executive-domain packages (`ideas_engine/`, `open_questions/`, `work_studio/`) are out-of-scope for this wave (they're W-EXECUTIVE-SUITE-v2-LIFT candidates).
3. **E.3** Export mechanism this wave: contract-only (`ExportArtefact` shape + gate refusal on empty carriers).  Actual export payload rendering (CSV / PDF / …) is a follow-on.
4. **E.4** No LLM-invoking donor code is lifted.  If donor `analyze_workspace/` contains LLM calls, they are HALTED with `NotImplementedError` + "HALT" per Solva-V2 CP-S8 precedent.
5. **E.5** Trust-surface + Executive-Suite waves stay OUT-OF-SESSION per DPO-D2.
6. **E.6** Donor path in Executive-Final repo remains EXCLUDED per §M5 Q3 DPO.

---

## §E · Commit protocol

* **Per CP** (Solva-V2 precedent): Commit A on `programme/track-a` (code + tests + ratchet manifest bump) · Commit B on `master` (state: DECISIONS entry + NEXT refresh + drill receipts).
* **Wave close (CP-D8+)**: composite seal `phase0/output_verified_seals/data_suite_v2_lift.seal.txt` · `Kind: data_suite_v2_lift` · 5-section owner-facing report at `notes/W_DATA_SUITE_V2_LIFT_close.md`.
* **NEVER push.**

---

## §F · Decision points / stop conditions

Wave HALTS with a decision-point note if:
* Donor code cannot be case-agnostically re-shaped (raises `NotImplementedError` with HALT message — Solva-V2 precedent).
* Baseline ratchet regression at any CP double-green.
* Any file entering the ratchet path leaks credential-shaped content.

Otherwise wave proceeds autonomously per owner directive.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
