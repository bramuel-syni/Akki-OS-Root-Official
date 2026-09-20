# Grounding Brief — CP-PRINCIPAL-MODEL-WAVE · WAVE R-69 Step 9

**Wave chartered:** 2026-09-20T~08:56Z (owner disposition · PRINCIPAL MODEL WAVE SCOPED · banked verbatim at `STATE/DECISIONS.md 2026-09-20T~08:56Z`).

**Spec source (custody-held · sha-pinned):**
- File: `custody/owner_drops/20260920T0856Z/Principal_Model_Spec_v1.docx`
- sha256: `056caa00b5eb8c4d75abe1e2d2653cee590682e946c87a1bbf43693cb7c8787c`
- Size: 14,976 bytes
- Banked at custody drop `bbdfef1c` (Step 4 · §4.1 §F manifest at `phase0/credential_drop_manifests/20260920T0856Z_owner_drops_manifest.json`).

**Interlude discipline (owner-authorized verbatim 2026-09-20T~09:48Z):** "interlude marker discipline restated — if context budget insufficient for full RED→GREEN→double-green→3-Commit cycle in one turn, land INTERLUDE marker at Commit-A boundary; Commits-B+C follow at next opportunity. Better to interlude than truncate mid-wave."

**Principal-wave-seal significance (owner ruling this-session verbatim):** "principal-wave seal is the last gate on DAP portal frontend work — when it seals, report prominently. Owner's two outstanding conditions were: (1) principal wave seals clean on its own evidence; (2) surface-language trace resolved. The trace is resolved-clean [at `e099ced1` · Step 2]. The wave seal is the last gate on DAP portal frontend work."

## §A · Wave scope (SO §6.4 NOTHING-BEYOND · from spec verbatim)

**In-scope:** A principal store; a credential plane; request-context propagation carrying principal identity to every downstream write; the trust-domain boundary DAP-5 requires (spec §Scope verbatim).

**Not in scope:** DAP's own admission ceremony, approval routing, or metering — those consume this capability and are specified in `dap_backend_spec_v1` (canon, sha `e675990a…`, confirmed 20 Sep 2026 · spec §Scope verbatim).

## §B · 13 PRIN requirements (verbatim from spec · quotable in invariant docstrings per SO §2.5)

### §B.1 · The Principal Store (spec §2)

- **PRIN-1** [DAP-1, DAP-2, DAP-3] "The store holds three principal kinds, each with its own mandate: organisation (DAP-1's fields — legal identity, governance posture, terms, trust-domain identifier, admission-time mandate); individual (a named person acting under an organisation, with a mandate scoped by that organisation); and agent (an autonomous non-human principal, admitted separately from its operator, carrying its own stated scope of autonomy). An individual or agent MUST reference the organisation it acts under; it MUST NOT exist without one."
- **PRIN-2** [DAP-1] "Admission of any principal is a governed act. An organisation is admitted only by the estate owner's named authority. An individual or agent is admitted only by a principal already holding authority to admit under its own organisation's terms. No principal self-admits."
- **PRIN-3** [DAP-2, DAP-3] "Every principal carries a behavioural-signature state under the Watch, present from its first request — an agent's machine-speed attack shape applies from admission, not from some later point at which it is judged to need watching."
- **PRIN-4** "Mandate is immutable once frozen at admission, on Northena's existing objective-freeze mechanism (Promise #32). Changing what a principal is admitted to do is a new admission event, not an edit to the old one."

### §B.2 · The Credential Plane (spec §3)

- **PRIN-5** [DAP-13] "Credentials are issued per principal, never per organisation — an organisation with five individuals has five credentials, each independently revocable in one act, none of which reveals or touches the others."
- **PRIN-6** "Credential material is never persisted in a form any component can read back. The plane issues and can revoke; it cannot recover or display a previously issued credential. A credential shown once and lost is reissued, never recovered."
- **PRIN-7** "A credential is bound to exactly one trust-domain identifier (§4) at issuance. It cannot be presented to resolve identity outside that domain."
- **PRIN-8** [DAP R-4 precedent] "Rotation default: 90 days, DEFAULT-class, per the existing platform convention for API key lifetime. Revocation is unconditional and immediate on the estate owner's act, regardless of rotation schedule."

### §B.3 · The Trust-Domain Boundary (spec §4)

- **PRIN-9** [DAP-5, Attribute 12] "The principal's domain and the estate's domain share no identifier resolution, no store, and no credential — verbatim DAP-5. A unit identifier meaningful inside the estate MUST NOT resolve to anything in the principal's domain except through an operation the consuming component's own spec permits."
- **PRIN-10** "Every record the platform writes on a principal's behalf carries that principal's trust-domain identifier. A write with no resolvable trust-domain identifier is refused, not defaulted to the estate's own domain."

### §B.4 · Request-Context Propagation (spec §5)

- **PRIN-11** "Every request entering the platform on behalf of a principal carries that principal's identity through to every service it touches, by construction — not by convention, not by a caller choosing to pass it along. A downstream write with no principal in its calling context fails closed rather than writing under a default or empty actor."
- **PRIN-12** "The Ledger's `actor` field is populated only from propagated principal context, never from a caller-supplied string. Existing entries written before this component exists are not retroactively altered — the fix is prospective, consistent with how every other prospective-only correction in this canon has been handled."
- **PRIN-13** "Principal context is read-only once it enters propagation for a given request. A service receiving it cannot widen, narrow, or substitute the principal it was given — the same discipline Northena's objective freeze already applies to scope."

## §C · Acceptance list (§6 spec · restated verbatim as this wave's unblocks)

| DAP requirement | Unblocked by |
| --- | --- |
| **DAP-13** (keys per principal) | §3 credential plane |
| **DAP-14** (controlled request routing) | §2 principal store + §5 propagation |
| **DAP-21** (metered event, party principal field) | §5 propagation, PRIN-12 specifically |
| **DAP-22** (terms resolved per party agreement) | §2 principal store |
| **DAP-23** (per-party ceiling) | §2 + §5 |
| **DAP-24** (cumulative extraction history) | §2 + §5 |
| **DAP-25** (owner configuration per party) | §2 principal store |
| **DAP-27** (suspend a party) | §2 — suspension is a state on the principal store |

**Not fully unblocked:** DAP-4's slow-play detection depends on cumulative history (above) but per DAP Backend Engineering Brief D-3 finding, three further parameters are missing beyond what this wave provides. This wave makes slow-play detection possible; it does not complete it. Track separately (LIM-1).

## §D · Placement in standing enumerations (§7 spec verbatim)

| Document | Entry |
| --- | --- |
| **`tcb_enumeration_v1`** | IN: admission (PRIN-2), the credential plane's issue/revoke decision (PRIN-5, PRIN-6), and propagation's fail-closed check (PRIN-11) — each deterministic, each falsifying a guarantee on failure. OUT: nothing learned exists in this component; there is no drafting half to exclude. |
| **`failure_posture_v1`** | Propagation context absent → fail-closed, no default actor (PRIN-11). Credential plane unreachable → fail-closed on issue and on revoke — revoke fail-closed means the credential is treated as still valid only until revocation is confirmed, never silently treated as already revoked. |
| **Master Requirements Registry** | PRIN-1 through PRIN-13 at next refresh. |

## §E · Limitations (§8 spec verbatim)

- **LIM-1** Does not complete DAP-4's slow-play detector — D-3's missing parameters are separate work.
- **LIM-2** Does not decide the reliable-time-source gap (D-16). Metering attribution becomes principal-correct under this wave; metering becomes defensible only once a reliable time source exists.
- **LIM-3** Does not build DAP's own admission ceremony, approval routing, or crossing profiles. Those are `dap_backend_spec_v1`'s, consuming this.
- **LIM-4** Is a specification, not a build. Sealing this wave means the tests above pass double-green and byte-match — it does not mean the wave has been independently audited or operated at scale.

## §F · Rulings (§9 spec · owner-ratified as R-22/R-23 this-session)

- **R-22 · Credential rotation default (PRIN-8):** 90 days, DEFAULT-class · consistent with the existing API-key convention. **Owner-ratified verbatim as ruling this-session.**
- **R-23 · Existing team-endpoint route shapes disposition:** `/api/team/access_register` and `/api/team/constitutional_seats` are **kept as read views over the new principal store**, not retired outright, so nothing consuming them breaks. **Owner-ratified verbatim as ruling this-session.**

## §G · Wave sequence (this-turn INTERLUDE per owner budget discipline)

1. **Grounding brief author** (this document · landing this-turn).
2. **RED-first test authoring** at `backend/tests/invariants/test_principal_model_v1.py` — 13 invariants (PRIN-1..PRIN-13 · each with verbatim docstring per SO §2.5). Landing this-turn.
3. **RED verification** — run `pytest tests/invariants/test_principal_model_v1.py -v` → expect ALL 13 fail right-reason (ModuleNotFoundError on `services.principal_store` etc.). Landing this-turn.
4. **RED receipt banked** at `phase0/drill_receipts/YYYYMMDDTHHMMZ_principal_model_wave_RED_pre.log`. Landing this-turn.
5. **INTERLUDE marker at pre-Commit-A boundary** (this-turn · state master notes-only commit banking grounding + tests + RED receipt).

### Deferred to subsequent turn (Commits-A/B/C completion)

6. **Implementation modules** on `programme/track-a`:
   - `backend/services/principal_store/` — Principal store (3 kinds: organisation, individual, agent · admission ceremony · behavioural-signature state · mandate freeze on Northena Promise #32 objective-freeze mechanism).
   - `backend/services/credential_plane/` — Credential issue/revoke · per-principal (never per-organisation) · non-recoverable material · trust-domain binding · 90-day DEFAULT-class rotation.
   - `backend/services/request_context/` — Request-context propagation · principal identity carried by-construction (not by caller-supplied convention) · fail-closed on downstream write with no principal · Ledger `actor` field populated only from propagated context.
   - `backend/services/trust_domain/` — Trust-domain identifier boundary · principal-domain ≠ estate-domain · write refusal on unresolvable trust-domain identifier.
   - `backend/contracts/principal_v1.py` — Principal contract (SO §3.10-α closed-schema: `frozen=True`, `extra='forbid'` from day one, per α-gap discipline just landed at CP-ALPHA-GAP-HARDENING).
7. **Read-view retention** (R-23 verbatim): `/api/team/access_register` + `/api/team/constitutional_seats` refactored as read-views over principal store · shape stays byte-identical.
8. **Targeted GREEN verification** — run RED tests · expect all 13 pass.
9. **Mutation-site sweep** — grep for any post-construction mutations on Principal contract / receipt classes; adapt per owner mutation-site discipline (fresh instances at call sites; production mutations = FINDING).
10. **Full-suite regression sweep** — run `pytest tests/invariants/` · expect all pass (ratchet 5532 + 13 new = 5545 target · verify no regressions).
11. **Contract-snapshot parity** — regenerate if needed (though frozen=True is schema-preserving per α-gap wave empirical fact).
12. **Ratchet bump** in `baseline_failures.json`: 5532 → 5545 (+13 exactly) · ratchet_history append.
13. **Double-green BASELINE_GUARD=1 byte-identical sweep** · stripped-sha256 IDENTICAL run1+run2 against post-bump baseline.
14. **Pre-Commit-A ORCH_BOOT.md ratchet-only regen** per M16-W3 corrected order (5532→5545 + baseline_sha update · audit mirror sync).
15. **§3.3 3-Commit Seal on dual branches:**
    - Commit-A on `programme/track-a` — code + tests + drill receipts + ratchet bump.
    - Commit-B on `master` — state banking (DECISIONS + NEXT + this grounding brief already banked at interlude).
    - Commit-C fixup on `master` — banks Commit-B SHA + ORCH_BOOT R-6 boundary regen advancing heads_last_sealed + POD audit mirror sync + R-76 marker flip ⏳→✅ SEALED.
16. **Post-Commit-C `test_orch_boot` verification** — confirm banking chain intact.
17. **PROMINENT PRINCIPAL-WAVE-SEAL REPORT TO OWNER** per owner ruling verbatim (owner two-outstanding-conditions verbatim: principal-wave seals clean on its own evidence [this seal] + surface-language trace resolved [already resolved-clean at `e099ced1`] · wave seal is the last gate on DAP portal frontend work · DAP portal work UNBLOCKS at this seal).

## §H · Canon anchors verbatim

- **Owner disposition 2026-09-20T~08:56Z** (α-gap hardening wave APPROVED + PRINCIPAL MODEL WAVE SCOPED + Principal_Model_Spec_v1 accepted as ratifiable draft).
- **Owner ruling 2026-09-20T~09:48Z** (Step 9 PRINCIPAL MODEL WAVE authorized · 13 PRIN requirements PRIN-1..PRIN-13 RED-first with verbatim docstrings per SO §2.5 · R-22 90-day DEFAULT-class as ruling · R-23 team endpoints as read-views as ruling · interlude marker discipline authorized).
- **Owner ruling this-session (GO)** (Step 8 strictly before Step 9 · principal-wave seal is last gate on DAP portal frontend work · when seals, report prominently).
- **spec source:** `Principal_Model_Spec_v1.docx` sha `056caa00b5eb…` (Table 0 row 0-3 quoted verbatim in §Scope + §Status + §Date).
- **Northena Promise #32** (objective-freeze mechanism · PRIN-4 anchor).
- **DAP-1, DAP-2, DAP-3, DAP-5, DAP-13** (spec bindings on PRIN-1/2/3/5/7/9).
- **DAP-4** (LIM-1: slow-play detector not completed by this wave · D-3 parameters separate).
- **DAP R-4** (rotation precedent · PRIN-8 anchor).
- **Attribute 12** (PRIN-9 anchor).
- **`dap_backend_spec_v1`** (canon · sha `e675990a…` · Step 9 wave consumes this; DAP's own ceremonies consume the principal capability landed here).
- **DAP-13, DAP-14, DAP-21, DAP-22, DAP-23, DAP-24, DAP-25, DAP-27** (8 DAP requirements unblocked by this wave's landing · spec §6 verbatim).
- **`tcb_enumeration_v1`** (spec §7 IN: PRIN-2 + PRIN-5 + PRIN-6 + PRIN-11 · OUT: nothing).
- **`failure_posture_v1`** (spec §7: propagation-context-absent → fail-closed no default actor · credential-plane-unreachable → fail-closed on issue AND on revoke).
- **Master Requirements Registry** (PRIN-1..PRIN-13 to add at next refresh · spec §7).
- **SO §2.5** (docstrings quote requirements verbatim · docstrings ride tests never substitute).
- **SO §3.3** (3-Commit Seal on dual branches at wave close).
- **SO §3.8** (thin-kernel additive-only).
- **SO §3.10-α** (closed-schema discipline · Principal contract lands with `frozen=True` + `extra='forbid'` from day one per α-gap hardening precedent set at CP-ALPHA-GAP-HARDENING seal `8c944ee7/b8225536/32fe6df2`).
- **SO §6.4** (NOTHING-BEYOND · scope frozen at 13 PRIN requirements · not DAP's own admission ceremony / approval routing / metering · not DAP-4 completion · not reliable-time-source).
- **SO §6.7** (sequence WAVE R-69 Step 9 LAST · principal-wave seal is the last gate on DAP portal frontend work).
- **CP-ALPHA-GAP-HARDENING** (`8c944ee7/b8225536/32fe6df2`) — TrustReceiptV1 + OuterGateReceiptV1 landed frozen=True this-wave · Principal contract lands frozen=True from day one following this precedent · empirical fact: Pydantic v2 `model_json_schema()` byte-identical between frozen=True/False so no snapshot regen impact.
- **M16-W3 corrected order** — pre-Commit-A ORCH_BOOT ratchet-only regen precedent (applied at Step 7 CP-ALPHA-GAP-HARDENING · applies again at Step 9 pre-Commit-A boundary).

## §I · Interlude discipline (this-turn INTERLUDE)

**Owner authorization verbatim (2026-09-20T~09:48Z):**
> "if context budget insufficient for full RED→GREEN→double-green→3-Commit cycle in one turn, land INTERLUDE marker at Commit-A boundary; Commits-B+C follow at next opportunity. Better to interlude than truncate mid-wave."

**This-turn scope (INTERLUDE at pre-Commit-A boundary):**
- Grounding brief (this document · lands this-turn).
- RED-first test authoring (13 tests · verbatim docstrings · lands this-turn).
- RED verification receipt (banked this-turn).
- INTERLUDE marker on `master` (state banking · lands this-turn).

**Deferred to subsequent turn (Commit-A/B/C · fresh budget):**
- Implementation modules (§G items 6-7).
- GREEN verification + mutation-site sweep + full-suite (§G items 8-9).
- Ratchet bump + double-green byte-identical (§G items 10-13).
- Pre-Commit-A ORCH_BOOT ratchet-only regen (§G item 14).
- §3.3 3-Commit Seal on dual branches (§G item 15).
- Post-seal `test_orch_boot` verification (§G item 16).
- PROMINENT PRINCIPAL-WAVE-SEAL REPORT TO OWNER (§G item 17).

## §J · Standing bounds still binding

- Zero push · terminal pytest only · **no `testing_agent` STRICTLY BANNED**.
- CWD constraint: `pytest` invocations run strictly from `/app/assessment_workspace/repos/Extraction-Akki/backend/`.
- Additive-only per SO §3.8. New modules added; no sealed contract shape edited.
- Three-repo discipline preserved (CODE `programme/track-a` + STATE `master` + POD `main`).
- Ratchet monotonic-up · never rebaselined silently (Canon 8 §W8).
- Stop-conditions #1/#2/#3 discipline · §6.4 pre-ruling NOT triggered · MEM-R-053 CROWN BAN NOT triggered.

## §K · Anti-slop note

Every fact in this brief traces to a paragraph or table row in `Principal_Model_Spec_v1.docx` (sha `056caa00b5eb…`) opened this-turn, or to a banked owner ruling in STATE/DECISIONS.md quoted verbatim. Every PRIN-1..PRIN-13 text in §B is quoted verbatim from the spec's numbered paragraph · not paraphrased · quotable in the invariant docstring per SO §2.5.

**End of grounding brief.**
