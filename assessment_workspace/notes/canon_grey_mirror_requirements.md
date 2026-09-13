READ STATE/STANDING_ORDERS.md FIRST — permanent standing law

# canon_grey_mirror_requirements.md

**Filed:** 2026-09-13 (document lane, ratchet unchanged).
**Source discipline:** Grounded first-hand from canon corpus.  Every requirement below cites its canon origin verbatim.  `[framing, not canon]` on any interpretive glue.
**Owner ruling context:** owner side-directive 2026-09-13 to update grey-mirror requirements alongside two new artefact drops (Security_Assurance_Promise_Set v3 + Watch_Learning_Amendment_v1) — folded here where they connect.

## §0 · Corpus scanned first-hand this pass

Files opened (grep and read):

- `canon/text/Akki_Canon_9_Mkondo_Charter.txt` — Canon-9 §6 handoff row for `Mirage release → reconciliation`.
- `canon/drops/20260910/extracted/text/Akki_Governance_Architecture_v1_from_15.txt` — Doc-0 §7 "The Watch (Grey Mirror + the Watch)".
- `canon/drops/20260910/extracted/text/Ratification_Record_v1.txt` — Ruling R-3 resolution (Grey Mirror is NOT TCB).
- `canon/drops/20260909/extracted/text/Security_Architecture_Description_v1.txt` — the Watch narrative.
- `canon/drops/20260909/extracted/text/TCB_Enumeration_v1.txt` — TCB in/out list.
- `canon/drops/20260909/extracted/text/Determinism_Inventory_v1.txt` — determinism labels.
- `canon/drops/20260913/owner_drop_2/Watch_Learning_Amendment_v1.docx` — the new 13 Sep amendment (L-1..L-5, S-7 close, S-28/S-29 new).
- Track-a `services/grey_mirror/` (`__init__.py`, `router.py`) — current implementation.

## §1 · What "Grey Mirror" means in canon (identity + scope)

**Doc-0 §7 (Akki_Governance_Architecture_v1_from_15.txt lines 264-267) — verbatim:**

> "7.  The Watch (Grey Mirror + the Watch)
> Instantiates: Subsystem, outside the six · Reference-Monitor-adjacent · Trust Domain · Checkpoint
> SCOPE
> Intent and security monitoring. Grey Mirror is the detection half — mirage, marks, baits, a continuous self-test. The Watch proper is the response half — state, record, an action ladder of annotate, shape, contain, sever — behind one verdict interface."

`[framing, not canon]` — The name "Grey Mirror" refers to the DETECTION HALF of the Watch subsystem; it is NOT a separate subsystem.  Grey Mirror + Mkono (response half) both live under "the Watch" umbrella, behind one verdict interface.

## §2 · Numbered requirements

Each row is one atomic normative statement.  `SOURCE` cites the verbatim origin.  `STATUS` reflects on-disk canon or amendment state as of 2026-09-13.

### R-GM-1 · Separable components behind one verdict interface

**Statement (verbatim):** "Grey Mirror's detection role and the Watch's decision-and-enforcement role are implemented as separable components behind the shared verdict interface, not fused such that separating them would require a rewrite."

**Source:** Doc-0 §7 BR-7.1 (Akki_Governance_Architecture_v1_from_15.txt line 269).  Derives Attribute 5, BA-5.1.

**Status:** Met — the Macho (detection) / Mkono (response) split is named explicitly, one verdict interface.

### R-GM-2 · Watch's own trust domain distinct from what it observes

**Statement (verbatim):** "The Watch's own trust domain — its separate task-identity, its own record classes — is described as a domain distinct from the domains it observes, with the boundary between them stated."

**Source:** Doc-0 §7 BR-7.2 (line 271).  Derives Attribute 12, BA-12.1.

**Status:** Partial — isolation exists (separate task-identity, external witness); ADV_ARC-sense domain description not confirmed.  Gap G-12.

### R-GM-3 · Watch's own governing policy passes slowest change-control tier

**Statement (verbatim):** "Changes to the Watch's own governing policy pass through the platform's slowest change-control tier, with an external witness holding no Watch credentials, as a documented procedure rather than an informal norm."

**Source:** Doc-0 §7 BR-7.3 (line 273).  Derives Attribute 9, BA-9.1.

**Status:** Met.

### R-GM-4 · Grey Mirror's learned pattern-matching excluded from Watch's decision authority

**Statement (verbatim):** "Grey Mirror's detection mechanisms, where they rely on learned pattern-matching rather than fixed signatures, are classified as learned and excluded from the Watch's own decision authority — detection may propose a finding; only the Watch's deterministic response half acts on it."

**Source:** Doc-0 §7 BR-7.4 (line 275).  Derives Attribute 10, BA-10.1.

**Status:** Gap G-10 (was: "Not confirmed").  **Amended 13 Sep 2026 by Watch_Learning_Amendment_v1 L-1..L-4** (see §4 below): certificate-on-verdict + certificate-requirement-library + mirage-as-certificate-ground + research-loop close the gap between "detection proposes" and "deterministic response acts" by inserting a deterministic certificate gate at the verdict interface.  `[framing, not canon]` "spec-closed, not built" per the amendment's own §5 promise table.

### R-GM-5 · Grey Mirror is NOT TCB (Ruling R-3 resolved 9 Sep 2026)

**Statement (verbatim):** "R-3 | RESOLVED, 9 Sep 2026 (tcb_enumeration_v1): the Watch's response half (Mkono) is TCB; Grey Mirror's detection half is not, consistent with BR-7.4. Applied by the mechanical test, not decided fresh — Owner sign-off is the ceremony act, not a re-litigation."

**Source:** `Ratification_Record_v1.txt` line 526.

**Status:** Ratified.

### R-GM-6 · Grey Mirror's tools of trade

**Statement (verbatim):** "Grey Mirror is the detection half — mirage, marks, baits, a continuous self-test."

**Source:** Doc-0 §7 line 267.

**Status:** Named.  Implementation: track-a `services/grey_mirror/router.py` currently routes to Watch verdict interface (fabric only).

### R-GM-7 · Mirage release → reconciliation handoff (Canon-9 §6)

**Statement (verbatim):** "Mirage release → reconciliation | Release verdict crosses to the replay-or-notify duty under the ruled posture; discharge is receipted; the friction budget is debited."

**Source:** `Akki_Canon_9_Mkondo_Charter.txt` line 66 (Canon-9 §6 handoff table).

**Status:** Canon-fixed contract; implementation not yet inventoried.  `[framing, not canon]` this row prescribes the exact hand-off between Watch mirage release and the reconciliation duty — replay-or-notify — with receipted discharge and friction-budget debit.  It sits alongside four other Watch-side handoffs in Canon-9 §6.

### R-GM-8 · Watch findings → CIF handoff (Canon-9 §6)

**Statement (verbatim):** "Watch findings → CIF | Findings cross as detection input under CIF's own origination port; nothing crosses back but ratified frames through the coach seat."

**Source:** `Akki_Canon_9_Mkondo_Charter.txt` line 68 (Canon-9 §6 handoff table).

**Status:** Canon-fixed contract.  `[framing, not canon]` grey-mirror finding routes to CIF exactly ONCE at its origination port; return traffic is limited to ratified frames — an asymmetric handoff.

### R-GM-9 · Response ladder is fixed

**Statement (verbatim, Doc-0 §7):** "The Watch proper is the response half — state, record, an action ladder of annotate, shape, contain, sever — behind one verdict interface."

**Source:** Doc-0 §7 lines 266-267.

**Status:** Named.  `[framing, not canon]` the four-rung ladder (annotate · shape · contain · sever) is the ONLY response vocabulary; Grey Mirror proposes verdicts consumed by this fixed ladder.

## §3 · Amendments folded in (2026-09-13 Watch Learning Amendment)

The 13 Sep 2026 `Watch_Learning_Amendment_v1` inserts five amendments to the Watch stack.  Requirements pertinent to Grey Mirror:

### R-GM-10 · Certificate on the verdict (A5.19 · new)

**Statement (verbatim from `Watch_Learning_Amendment_v1` L-1):** "Every verdict Grey Mirror passes to Mkono MUST carry a certificate: the set of observed data points that satisfy a ratified certificate requirement (A5.20) for the behaviour asserted, with the requirement's ID and references to the observation records."

**Schema:** `certificate = {requirement_id, data_points[], observation_refs[]}`.  Deterministic satisfaction test — a lookup, not reasoning.

**Impact on R-GM-4:** the seam that separates "detection proposes" from "response acts" now has a deterministic-lookup gate — Grey Mirror stays learned; the certificate gate between Grey Mirror and Mkono is deterministic.  Article 14(c) evidenced structurally.

### R-GM-11 · Mirage as Certificate Ground (A5.21 · new)

**Statement (verbatim, L-3):** "The mirage is the certificate ground: a controlled environment in which a behaviour with a ratified requirement can be provoked and its data points collected without exposure to real estate data."

**Impact on R-GM-6 + R-GM-7:** the mirage now has TWO roles — the original release-and-reconcile flow (Canon-9 §6) AND a certificate-ground role for admission-time and requirement-formation.

### R-GM-12 · Certificate check fail-closed posture

**Statement (from Watch_Learning_Amendment_v1 amended `failure_posture_v1`):** "Certificate check cannot complete (library unreadable; requirement unresolvable) → fail-closed for certified actions: only the foundation floor remains — the reversible ladder, and severance from A5.2's signals alone.  Preserved: the verdict, the failed-check event is recorded."

**Source:** Watch_Learning_Amendment_v1 Table 2 (Placement in Standing Enumerations) row `failure_posture_v1`.

**Status:** Spec-closed 2026-09-13; not built.

## §4 · Current implementation state (`services/grey_mirror/`)

Present on track-a (surveyed 2026-09-13):

- `services/grey_mirror/__init__.py` — package marker.
- `services/grey_mirror/router.py` — router surface (fabric).

`[framing, not canon]` No certificate-gate mechanism exists yet.  No mirage-as-certificate-ground scenario registry exists yet.  Requirements R-GM-10, R-GM-11, R-GM-12 are BUILDING BLOCKS that land INSIDE the existing **W-WATCH-STACK** wave (M3 · Doc-3 62 BUILD rows) per `MILESTONE_PROMISE_BINDING_20260913.md §M3`.  Owner constraint 2026-09-13: no new waves; these requirements ride existing W-WATCH-STACK verdict-interface + mirage rows when M3 opens.

## §5 · Cross-reference to M2 sub-waves in flight

None of the Grey-Mirror requirements are LOAD-BEARING on the currently-open M2 sub-waves (W-M2-SW1 Rule-Registry-Bootstrap [CLOSED] · W-M2-SW2 Rules-Service-Ceremony [CLOSED] · W-M2-SW3 Rule-Book-Library [in RED/design phase]).  Additive touch-points to note when those M2 sub-waves land:

| M2 sub-wave | Grey-Mirror touch-point | Status |
|---|---|---|
| W-M2-SW1 Rule-Registry-Bootstrap (CLOSED) | Rule-registry accepts finite enforcement classes.  Certificate requirements (RBM-23) are `tier system-TCB` — a countdown tier, not an enforcement-class value — so no schema change needed. | Additive-compatible |
| W-M2-SW2 Rules-Service-Ceremony (CLOSED) | Certificate requirements pass RBM-8 ceremony · which is the same countdown/witness/second-signatory ceremony that SW2 already builds.  `system_tcb` business-type is already in the v1 taxonomy. | Additive-compatible |
| W-M2-SW3 Rule-Book-Library (in flight) | If SW3 seeds a rule-book file, it can carry RBM-23 records at TCB-tier.  Certificate requirements are a NEW rule class per L-2 but registry is generic. | Additive-compatible |
| W-DOC0-ATTR7-BASELINE (imminent) | L-3 adds "mirage as certificate ground" at admission time.  W-DOC0-ATTR7 currently scopes to serving-integrity floor.  When ATTR7 lands, add a follow-on wave-honest limit acknowledging certificate ground not yet built. | Add limit-marker; not blocking |
| W-DOC0-ATTR8-AUDIT-AU3 (imminent) | Certificate records are AU-3 subjects (§8 of Doc-0).  Additive record class in AU-3 linter. | Additive |
| W-SFP-8-SERVING-INTEGRITY (imminent) | DAP-32+ extended by L-3 to include per-requirement provocation scenarios.  SFP-8 declared-dependency marker on DAP-32+ stays valid; the extension is orthogonal to serving-path integrity itself. | Non-blocking |

## §6 · Delta vs prior state (no prior extracted requirements file)

Prior state: no `notes/canon_grey_mirror_requirements.md` existed.  This is the FIRST extraction pass filed.  Delta = created-from-nothing.

`[framing, not canon]` when the amendment lands as a built wave, requirements R-GM-10, R-GM-11, R-GM-12 will move from "spec-closed" to "built"; that update belongs in the wave-close note, not silently here.

## §7 · What the owner may want to check

If the owner has a specific new grey-mirror requirement in mind that is NOT in the canon corpus (nor in the 13 Sep amendment), it is not represented above.  Please rule.

---

READ STATE/STANDING_ORDERS.md FIRST — permanent standing law
