# Canon 3 · Akki Governance Engines · Requirements Checklist

**Source:** `/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_3_Governance_Engines.txt` (309 lines · 35,923 B · sha256 `4f31f73b0972fe6b499d41ff2ab2fd30bbe8a177e969c6e091958bc500d1f019`)
**Doc title verbatim:** `Akki Governance Engines`
**Rule set:** 2c · atomic single-line rule + one-line rationale + section anchor.

---

## Part I · Two Axes, One Discipline

- **C3-R-001 · Canon 3 scope.** Specifies two of six engines: Northena (direction) and SyniSense (boundary); depth (Solva) is in Doc 4 because reasoning sits inside the extraction path. *Rationale:* fixes doc-3 scope. *Canon 3 §1.*
- **C3-R-002 · Three axes never collapse.** A governor performing another's function would create a single point at which a run could be admitted/bounded/asserted by the same logic. *Rationale:* structural three-way separation. *Canon 3 §1.*
- **C3-R-003 · Direction question.** Is this run still in scope, and is it done? Answered for every run, run after run, and recorded. *Canon 3 §1.*
- **C3-R-004 · Boundary question.** May this data cross this access point? Answered for every outbound model call, every egress. *Canon 3 §1.*
- **C3-R-005 · Deterministic-accountability standard.** Every run answerable deterministically: admitted because [fields valid] · gated because [scope held] · stopped because [condition met] · refused because [rule fired]. "Admitted because model scored highly" is the unauditable outcome this rule exists to prevent. *Canon 3 §2.*
- **C3-R-006 · Record is a contract, not a log.** Versioned, append-only, closed on every run. Refusals and drops recorded exactly as successes. *Canon 3 §2.*
- **C3-R-007 · No closed record = invalid run.** A run with no closed record is incomplete, non-auditable, and invalid. *Rationale:* central-claim liveness. *Canon 3 §2.*

## Part II · Northena — The Direction Governor

- **C3-R-008 · Northena responsibilities.** Keeps runs on-objective, brings each to a defined stop, writes the durable audit-grade record of direction; does not extract, does not reason. *Canon 3 §3.*
- **C3-R-009 · Two governing artifacts.** Portfolio Mandate (first-contact) + Objective Request (day-to-day); Northena governs run lifecycle, not what artifacts contain. *Canon 3 §3.*
- **C3-R-010 · Deterministic by construction.** No ML model, no learned weights, no adaptive behaviour; Northena is dynamic like a thermostat — the mechanism neither learns nor infers. *Canon 3 §4.*
- **C3-R-011 · Determinism enforced structurally.** No Northena module imports an ML library or a learned component; import assertion in CI. *Canon 3 §4.*
- **C3-R-012 · Judgement is delegated to depth governor through opaque handle.** Northena acts deterministically on the value returned; never reads internals; never performs inference itself. *Canon 3 §4.*
- **C3-R-013 · Four stages.** Admit · Gate · Converge · Ledger — the loop. *Canon 3 §5.*
- **C3-R-014 · Admit action.** Compiles a raw intent into a frozen governing artifact, validates deterministically, freezes atomically. *Canon 3 §5.*
- **C3-R-015 · Gate action.** Checks whether a sub-objective falls within the frozen artifact's declared scope, and routes on the result. Strict set-membership. *Canon 3 §5.*
- **C3-R-016 · Converge action.** Decides whether the run is done. Threshold check against done-condition or budget. *Canon 3 §5.*
- **C3-R-017 · Ledger writes the run.** Durable audit-grade record; no decision, only recording. *Canon 3 §5.*
- **C3-R-018 · Admit's five deterministic checks, in order.** Lawful basis present → declaration current → artifact complete against required fields → declared scope resolves against Registry → defensibility floor well-formed. Failure at any point refuses admission and writes reason; no downstream stage runs. *Canon 3 §6.1.*
- **C3-R-019 · Refusal reason strings enumerated.** `missing_lawful_basis` · `missing_declaration` · `incomplete_artifact` · `scope_unresolved` · `floor_malformed`. *Rationale:* the closed refusal enumeration. *Canon 3 §6.1.*
- **C3-R-020 · Lawful basis enforced at Admit, before any extraction.** Purpose limitation is an admission property, not a downstream filter. *Canon 3 §6.1.*
- **C3-R-021 · No actor enters undeclared.** Agent admitted against declared objective + capabilities + risks; person admitted against declared role + interests. Declaration frozen with the artifact; Watch reconciles realised behaviour against it (Doc 8); re-declaration through same admission path is legitimate exit from honest change. *Canon 3 §6.1.*
- **C3-R-022 · Undeclared actor gets default-restrictive envelope and nothing wider.** *Canon 3 §6.1.*
- **C3-R-023 · The freeze is atomic; artifact is immutable for the run.** A changed intent is a new admission, never an edit of a live one. *Canon 3 §6.2.*
- **C3-R-024 · Frozen artifact fields.** Type + identity + version + scope set (for Gate) + defensibility floor + done-condition + budget + lawful basis. *Canon 3 §6.2.*
- **C3-R-025 · Both admission paths write the Ledger.** Internal work order and external request both write a row carrying artifact ref + lawful-basis ref. *Canon 3 §6.2.*
- **C3-R-026 · External request completeness rule.** Arrives complete or is refused with the validation envelope; carries an idempotency key so retries neither double-commission nor double-charge. *Canon 3 §6.3.*
- **C3-R-027 · Work order requires envelope-complete before freeze.** Wizard fills the envelope; Admit checks + freezes. *Canon 3 §6.3.*
- **C3-R-028 · Gate is pure set-membership.** No inferential path exists in Gate; ambiguous membership is a compilation defect fixed at Admit. *Canon 3 §7.*
- **C3-R-029 · Gate's three routings.** Refuse (`out_of_scope`, recorded not silently dropped) · Warm serve (already converged, sync) · Fresh extract (unconverged, returns async contract). *Canon 3 §7.*
- **C3-R-030 · Warm/fresh fork made once at the boundary.** Never re-derived downstream. *Canon 3 §7.*
- **C3-R-031 · Converge decides on two threshold checks.** Done-condition met → terminate_success; budget exhausted → terminate_budget. No learned stopping. *Canon 3 §8.*
- **C3-R-032 · Northena owns the halt.** Depth governor may report it cannot reason further soundly, but stop decision and its record belong to Northena alone. *Canon 3 §8.*
- **C3-R-033 · Budget is a hard stop.** Nothing past the ceiling is billed; makes open-ended extraction commissionable. *Canon 3 §8.*
- **C3-R-034 · Ledger records everything.** Admission + outcome · every Gate routing + reason · every refusal or drop · convergence decision · absorbed defensibility stamp-audit entries. *Canon 3 §9.1.*
- **C3-R-035 · Ledger row shape.** `run_id` · `trace_id` · `stage` (admit/gate/converge) · `decision` (admitted/refused/warm/fresh/terminate_success/terminate_budget/continue) · `reason` (deterministic string · same inputs → same string) · `artifact_ref` (type/identity/version) · `lawful_basis_ref` · `stamp_audit` (optional absorbed side-channel entry) · `at` (timestamp). *Canon 3 §9.2.*
- **C3-R-036 · Ledger writer exposes append only.** No update path, no delete path within the retention window; correction = new entry, never edit. *Canon 3 §9.3.*
- **C3-R-037 · Out-of-scope and refused items are recorded.** A system dropping what it declined cannot show what it declined. *Canon 3 §9.3.*
- **C3-R-038 · stamp_audit is deliberately untyped, permissive.** Lets absorbed artefacts from later engines land without mutating the frozen contract; typing it would harden into mutation surface. Guarded by snapshot test so decision cannot be quietly reversed. *Canon 3 §9.4.*
- **C3-R-039 · Unit vs audit lifecycle separation.** stamp-audit joined by unit + trace identity rather than embedded; output and audit trail retain/export/expire independently. *Canon 3 §9.4.*
- **C3-R-040 · Three import-assertion dependency rules.** (i) No module imports ML/learned; (ii) state machine reaches reasoner only through handle; (iii) ledger writer exposes append only. *Canon 3 §10.*
- **C3-R-041 · Northena invariants (§11) are binding.** (i) Deterministic; (ii) inference belongs to depth governor through opaque handle; (iii) every run governed by exactly one frozen artifact with valid lawful basis; (iv) artifact immutable for run — changed intent = new admission; (v) Gate is strict set-membership; ambiguous = compile-time defect; (vi) Northena owns the halt; no run closes without closed audit-grade ledger; (vii) Ledger versioned/snapshot-asserted/append-only/immutable within retention window; (viii) out-of-scope + refused recorded, never silently dropped; (ix) axes never collapse — direction only. *Canon 3 §11.*

## Part III · SyniSense — The Boundary Governor

- **C3-R-042 · SyniSense functions.** Single chokepoint for every outbound model call; enforcement point of de-identify→invoke→re-identify chain; class-honesty guard on every governed response; closer of the refusal taxonomy. *Canon 3 §12.*
- **C3-R-043 · Scope is every model surface, not language alone.** Perception providers (speech, vision) route through it too; same custody + same receipt whatever the modality. *Canon 3 §12.*
- **C3-R-044 · One chokepoint function.** Only place a model is invoked; everything else calls that function. *Canon 3 §13.*
- **C3-R-045 · Build fails if any other module imports the model client.** Custody enforced at the invocation itself; chokepoint at narrowest point. *Canon 3 §13.*
- **C3-R-046 · Chokepoint sequence (7 steps).** Provider selection · De-identify · [Watch input-seat scoring] · Invoke with metering · Re-identify · Grounding gate (per-sentence anchor map) · Class-honesty check · Trust receipt. *Canon 3 §13.1.*
- **C3-R-047 · Sandbox vs production provider selection.** Sandbox mode = declared/labelled fixture provider; production credential + no provider configured = refuse (not fixture) — because synthetic-as-governed would violate claim-and-class separability. *Canon 3 §13.1.*
- **C3-R-048 · De-identify + per-request custody envelope.** Strips identifiers to placeholder tokens; records mapping in a per-request envelope that does not outlive the call. *Canon 3 §13.1 · §14.*
- **C3-R-049 · Watch input seat sits between de-identify and invoke.** Every payload bound for a model is scored for hostility and provenance before the call. Sensor + graded gate under the Watch's own authority; adds no second custody chain; verdicts land in the record. *Canon 3 §13.1.*
- **C3-R-050 · Metering is emitted per call.** To the telemetry stream at invoke time. *Canon 3 §13.1.*
- **C3-R-051 · Re-identify raises on unmatched token.** A placeholder that cannot be resolved is an error, never a value. *Canon 3 §13.1.*
- **C3-R-052 · Tenant-scoped entity resolution supplies entities to de-identifier.** So de-identification is never limited to what a general recogniser detects. *Canon 3 §14.*
- **C3-R-053 · Custody envelope does not persist beyond the call.** A persisting mapping would be a standing re-identification key. *Canon 3 §14.*
- **C3-R-054 · Purpose enforcement distributed across four mechanisms.** Data-blind prompts (templates contain no purpose-scoped data) · grounding gate as proof of purpose alignment (ungrounded = refuse) · closed refusal taxonomy · advisory-marker discipline (non-fact classes carry markers at write + render time). *Canon 3 §15.*
- **C3-R-055 · Trust receipt emitted per invocation.** Evidence the call happened, under what custody, without exposing credential. *Canon 3 §16.*
- **C3-R-056 · Credential never logged.** Presence surfaces only as boolean probe at module load; absence selects sandbox fixture; nothing downstream branches on credential value. *Canon 3 §16.*
- **C3-R-057 · Two custody pathways both emit receipts.** Synthesis path (through chokepoint) + perception path (through perception router); neither bypasses the other. *Canon 3 §16.*
- **C3-R-058 · Grounding is proven, not asserted.** Sentence that cannot be anchored to material is not a weaker sentence — it is a refusal. *Canon 3 §17.*
- **C3-R-059 · Model ladder must carry a lower-rung fallback.** Every model-reaching composition paired with mechanical composer preserved byte-identical as fallback — a top rung with no floor = unbounded quality point. *Canon 3 §17.*
- **C3-R-060 · Advisory outputs marked twice.** At write time by producing service; at render time by surface; a marker enforced only at write can be dropped by a renderer unaware it was load-bearing. *Canon 3 §17.*
- **C3-R-061 · SyniSense invariants (§18) are binding.** (i) chokepoint = only module invoking model client (negative-scan test); (ii) boundary contracts frozen — change is a seal event; (iii) every invocation transits de-identify→invoke→re-identify; (iv) refusal taxonomy is closed; no ad-hoc refusal path; (v) any highest-rung composition paired with byte-identical lower-rung fallback; (vi) prompt templates negative-scanned against tenant data on every build. *Canon 3 §18.*

## Part IV · The Two Perimeters

- **C3-R-062 · Two perimeters.** Inner gate (live path · per call · key scope enforced server-side · class carried inline) + Outer gate (extract · once at export · rights + irreversibility + cumulative disclosure + licence issue + receipt minting). *Canon 3 §19.*
- **C3-R-063 · Outer gate's five checks are distinct failure modes.** Rights · Irreversibility · Cumulative disclosure · Licence issue · Receipt. *Canon 3 §20.*
- **C3-R-064 · Raw media out of scope for direct export.** Irreversibility cannot be honoured on it. *Canon 3 §20.*
- **C3-R-065 · Cumulative disclosure prevents re-combination reconstruction.** Combined-with-prior-exports reconstruction check. *Canon 3 §20.*
- **C3-R-066 · Licence issued attached to deliverable.** *Canon 3 §20.*
- **C3-R-067 · Receipt records fact + fingerprint of transform.** Never anything that could aid reversal. *Canon 3 §20.*
- **C3-R-068 · Nothing partial egresses.** A cancelled run is ledgered; partial output does not leave — partial egress would make perimeter probabilistic. *Canon 3 §20.*
- **C3-R-069 · Cumulative disclosure arm operates on 3 thresholds.** Minimum group size · minimum distinct-value count within group · cumulative privacy budget. *Canon 3 §21.*
- **C3-R-070 · Single-packet refusal live from outset; cross-session arm closed awaiting thresholds.** Closed by construction (admit returns false when any of the three is unset/unparseable), never by configuration accident. *Canon 3 §21.*
- **C3-R-071 · Opening cumulative arm is a compliance decision.** Thresholds set → arm admits → new refusal path reachable → system begins persisting egress fingerprints across sessions (material change in what platform retains). *Canon 3 §21.*

## Part V · Governed Values

- **C3-R-072 · Four classes of governed value.** Rails · Rules · Engine settings · Registries — differ in change authority, change velocity, verification method. *Canon 3 §22.*
- **C3-R-073 · Rails.** Authored as code + contract; only through a build; never runtime-editable; not operable — observable only; hard-fail check (a rail without one does not exist). *Canon 3 §22.*
- **C3-R-074 · Rules.** Defined with type/bounds/recommended-default; set at setup, locked at approval; changed via propose → counter-sign → wait → apply → certificate; verified via live test packs per rule. *Canon 3 §22.*
- **C3-R-075 · Engine settings.** Declared with conditions of success; pinned per engine version; changed by engineers through versioned deployment; verified by version's evaluation verdict. *Canon 3 §22.*
- **C3-R-076 · Registries.** Schema defined once; rules reference by version; initial load at setup or first upload; upload/validate/difference/confirm/version lifecycle; validation report + live probe on drawn entries. *Canon 3 §22.*
- **C3-R-077 · Entitlement rules use attribute-based access control (ABAC).** Requester attributes matched against content attributes; role-based access is the simplified case, not a separate mechanism. *Canon 3 §22.1.*
- **C3-R-078 · Content-side attribute is Mtafiti's census-time classification.** No new classification exists; entitlement reads the one already there. *Canon 3 §22.1.*
- **C3-R-079 · Entitlement rules follow rule-change ceremony identically.** Proposed by compliance owner → counter-signed → wait → apply → demonstrated firing via Verification Runner. *Canon 3 §22.1.*
- **C3-R-080 · Two entitlement classes.** Escalatable (named authority may grant one-time or standing exception) · Absolute (no authority may waive). *Canon 3 §22.1.*
- **C3-R-081 · Watch operating-law values consume this taxonomy without extending.** Response policy tables + closed signal registries = Registries-class; runtime thresholds = Rules-class. Watch authors; this service administers change; neither writes the other's content. *Canon 3 §22.1.*
- **C3-R-082 · Promotion path has exactly one route.** Engine setting → rule; no third path — "it is only an engine setting" would otherwise route around every rule. *Canon 3 §23.*
- **C3-R-083 · Rule is never edited in place.** Change moves through a visible pipeline; the pipeline IS the governance. *Canon 3 §24.*
- **C3-R-084 · Rule-change ceremony (5 steps).** Propose (with reason; current + proposed on record) · Counter-sign (by second constitutional authority) · Wait (enforced countdown from consequence class, not fixed) · Apply (value updates + change certificate) · Re-verify (affected packs re-run · demonstrated firing). *Canon 3 §24.*
- **C3-R-085 · Watch-constitution changes carry slowest countdown + Watch itself observes.** Change touching Watch's sever-certainty registry, mark dimensions, or policy tables — slowest countdown the instance defines; proposal surfaced to Watch as monitored event the moment it is filed. *Canon 3 §24.*
- **C3-R-086 · Prior-rule-governed work keeps its rule version.** Record does not retroactively re-govern; a record that changed its own history would not be a record. *Canon 3 §24.*
- **C3-R-087 · Registries lifecycle asymmetric.** Additions take effect immediately; removals + edits require approval. Adding protection is safe by direction; removing/editing is the only change that can weaken a shield. *Canon 3 §25.*
- **C3-R-088 · Every run records which registry version was in force.** Without it, "was this term protected on a given date" has no answer. *Canon 3 §25.*

## Part VI · Retention, Deletion, Isolation

- **C3-R-089 · Retention default is indefinite append-only.** Stated as default; no deletion code path exists in direction-governor services; absence guarded by scan for deletion/purge/expiry tokens. *Canon 3 §26.*
- **C3-R-090 · Retention window is a compliance decision.** Unset state displayed on Trust Center as unset rule; opening window is itself a governed change; deletion mechanism built + test re-scoped alongside it, never simply removed. *Canon 3 §26.*
- **C3-R-091 · Deletion events recorded as entries, not mutations.** Preserves append-only guarantee. *Canon 3 §26.*
- **C3-R-092 · Deletion is authority act.** Names scope + reason; dual control; waiting period during which can be cancelled; same shape as rule change. *Canon 3 §27.*
- **C3-R-093 · Destruction attestation is the artefact regulators ask for.** What was deleted · under whose authority · date · method · ledger reference. Generated from record, not assembled afterwards. *Canon 3 §27.*
- **C3-R-094 · Retention holds bar deletion absolutely.** Material under hold facing deletion request produces absolute refusal naming the hold instrument; no seat lifts a hold from inside the system. *Canon 3 §27.*
- **C3-R-095 · Instance is a boundary.** Estate + rules + ledger + artefacts + memory planes belong to one instance and are unreachable from any other. *Canon 3 §28.*
- **C3-R-096 · Boundary enforced by scoped accessor at data layer.** Not by filter in application code — a filter is convention any new path can forget; scoped accessor is only way to reach data. *Canon 3 §28.*
- **C3-R-097 · Isolation asserted by structural walker.** Fails build where a query can reach across boundary. Multi-tenancy defended by discipline alone fails first hurried query. *Canon 3 §28.*
- **C3-R-098 · Onboarding context is per instance.** Rule values + registries + model registry entries + economics config all instance-scoped; two instances of same build can hold different values; neither can observe the other. *Canon 3 §28.*

## Part VII · Assurance

- **C3-R-099 · Trust Center is the compliance officer's home surface, read-only.** *Canon 3 §29.*
- **C3-R-100 · Design posture: adversarial to comfort.** Refusals appear as evidence governance bites; retention overruns + unset rules appear as problems; record itself, never a summary. *Canon 3 §29.*
- **C3-R-101 · Rule inventory.** Every rule in force with current setting + who set it + when + initial/changed + enforcement (which gates prove it). *Canon 3 §29.1.*
- **C3-R-102 · Rule with no proving gate = unenforced.** Displayed as such rather than counted among enforced. *Canon 3 §29.1.*
- **C3-R-103 · Respect record.** Refusals by class + held items + resolutions + authorised deletions + rule changes with ceremony stage + de-identification activity — each walkable to ledger receipt. *Canon 3 §29.2.*
- **C3-R-104 · Violation record unhidden.** Custody events + failed attempts + threshold breaches with disposition; compliance officer's work is dispositioning violations, not discovering them. *Canon 3 §29.3.*
- **C3-R-105 · Three enforcement classes.** Enforced (check runs, fails closed, emits receipt) · Attested (recorded human act — signature, instrument, counter-signature) · Monitored (measured + reported, non-blocking). *Canon 3 §30.*
- **C3-R-106 · Class is derived from taxonomy, never hand-set.** A typed-in field would make the honesty claim itself unverifiable. *Canon 3 §30.*
- **C3-R-107 · No class superior; surface reports without editorialising conversion.** *Canon 3 §30.*
- **C3-R-108 · Verification pack per rail — plain language, shows its proof.** Runs at commissioning + after every rule change; Master Admin + compliance officer watch each rail fire then sign commissioning record. *Canon 3 §31.*
- **C3-R-109 · A rail that cannot be demonstrated firing is not in force.** Pack is the difference between a rule that exists and a rule that works. *Canon 3 §31.*
- **C3-R-110 · Regulator pack generated from record, never assembled by hand.** Carries rules in force + enforcement class + counts + record for period + ceremony histories + destruction attestations + proof trails for nominated runs. Same record compliance officer reads daily. *Canon 3 §32.*
- **C3-R-111 · Governance orchestration summary (§33).** Admitted against frozen artifact with lawful basis or not started · routed by membership against declared set, never inference · stops on condition fixed before start · every model call transits one chokepoint de-identified out/re-identified back · everything leaving passes five checks + mints receipt · every decision in append-only record closed with run. *Canon 3 §33.*

---

**Total extracted requirements for Canon 3:** 111.
