# Canon 7 · Akki Integration Service and Quality Rulebook · Requirements Checklist

**Source:** `/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_7_Integration_and_Quality.txt` (298 lines)
**Doc title verbatim:** `Akki Integration Service and Quality Rulebook — The contract every application meets, entitlement enforcement, the memory layer, the Function & Promise Registry, the Critic Seam, and the discipline the build itself is held to`
**Rule set:** 2c · atomic single-line rule + one-line rationale + section anchor.
**Convention:** `Canon 7 §X.Y` = section X.Y of Canon 7.
**Cross-refs surfaced (Task-3 targeted checks):** Canon 3 §6.1, Canon 3 §13.1, Canon 3 §22, Canon 3 §22.1, Canon 3 §27, Canon 4 §49, Canon 8 (whole), Canon 9 (matrix).

---

## PART I · The Integration Chain

### §1 Scope

- **C7-R-001 · Integration surface enumeration.** Canon 7 specifies the answering service, the async delivery contract, the memory layer, the applications specified fully enough to demonstrate the platform's contract, the Function & Promise Registry, the Critic Seam, and the defect classes and process rules binding owner/builder/system. *Rationale:* fixes the enumerated scope of the integration rulebook. *Canon 7 §1.*
- **C7-R-002 · Integration accountability sentence.** Integration is accountable for one thing: intelligence reaches its consumers under the rights and masking in force, and consumption returns value the organisation can account for. *Rationale:* single accountability sentence for the whole integration chain. *Canon 7 §1.*
- **C7-R-003 · Integration failure classes (three).** Failure looks like capability that exists but nothing consumes, consumption that escapes its rights envelope, or value that leaves unmetered. *Rationale:* enumerated failure modes for the chain. *Canon 7 §1.*

### §2 The Standard the Chain Holds

- **C7-R-004 · Governance inline everywhere.** Governance travels inline, everywhere; no response shape separates a claim from its class on any path (sync, async, artefact). *Rationale:* class-with-claim invariant at every hop. *Canon 7 §2.*
- **C7-R-005 · Refusal ≠ error, distinguished by body discriminator.** A refusal is a governed outcome, not an error; distinguished by a discriminator in the body, never by a status code; an infrastructure fault is never rendered as a refusal. *Rationale:* fault/refusal separation is structural, not by HTTP code. *Canon 7 §2.*
- **C7-R-006 · Single-derivation rule.** Where a rule is enforced at two points, both import the same module; a negative scan prevents reimplementation. *Rationale:* prevents same-rule-implemented-twice divergence. *Canon 7 §2.*
- **C7-R-007 · No partial egress on cancellation, but always recorded.** Nothing partial egresses, including on cancellation; a cancelled run is still recorded. *Rationale:* perimeter is absolute; ledger is complete. *Canon 7 §2.*

## PART II · The Answering Service

### §3 What It Is

- **C7-R-008 · Answering-service scope.** The answering service carries admission, composition, grounding, the async lifecycle, cancellation, and the refusal machinery; it is the surface every integrated application meets and the surface the platform's own reference application sits on. *Rationale:* fixes the surface every application shares. *Canon 7 §3.*

### §4 Admission and the Fork

- **C7-R-009 · Pre-anything admission checks (three).** A request is checked for completeness, admissibility, and entitlement before anything else happens. *Rationale:* admission is the earliest gate. *Canon 7 §4.*
- **C7-R-010 · Validation envelope for missing external fields.** An external request missing any required field is refused with the validation envelope; a shaped work order arrives already complete. *Rationale:* wizard-frozen work orders skip validation refusal because the wizard could not have frozen them otherwise. *Canon 7 §4.*
- **C7-R-011 · Entitlement is the third check.** Entitlement — whether the requester's own attributes satisfy the rules governing the content — runs alongside completeness, not after; an incomplete AND unentitled request is refused for both reasons together. *Rationale:* parallel-check design; no sequential leak of one refusal reason. *Canon 7 §4 · cross-ref Canon 3 §22.1.*
- **C7-R-012 · Declaration check at admission.** Every calling application and every agent acting through one carries the declaration Canon 3 §6.1 requires (standing objective, capabilities, risks); missing or stale declaration refuses with its own named reason. *Rationale:* declaration is what the Watch reconciles conduct against; check it once at the boundary. *Canon 7 §4 · cross-ref Canon 3 §6.1 & Canon 8.*
- **C7-R-013 · Baseline-verified-anywhere-else is skipped-elsewhere.** Declaration is checked at admission because a baseline verified anywhere later is a baseline some path skips. *Rationale:* single-point verification rationale. *Canon 7 §4.*
- **C7-R-014 · Warm/fresh fork happens once.** The warm/fresh fork happens at admission, once; an ask servable from qualified intelligence already held is answered synchronously; one requiring fresh extraction returns the async contract. *Rationale:* single fork point prevents downstream re-derivation. *Canon 7 §4.*
- **C7-R-015 · Fork determination is a Registry feasibility query.** The warm/fresh determination comes from the feasibility query against the Registry — a membership and convergence test, never an estimate. *Rationale:* estimate-forks would drift; membership tests do not. *Canon 7 §4.*
- **C7-R-016 · Downstream honours the fork.** Everything downstream honours the admission fork rather than re-deriving it, because a second derivation could disagree with the first. *Rationale:* prevents consumer-facing contradictions. *Canon 7 §4.*

### §5 Admission Refusal

- **C7-R-017 · Refusal reasons enumerated and versioned.** Refusal reason sets are files, versioned in sequence, with the highest version in force. *Rationale:* enables reasoning about past refusals under old versions. *Canon 7 §5.*
- **C7-R-018 · Refusal version recoverability.** A refusal issued under an earlier version stays interpretable after the set grows because the version it was issued under is always recoverable. *Rationale:* forward-compatibility for past refusals. *Canon 7 §5.*
- **C7-R-019 · Closed refusal taxonomy.** Every refusal resolves to a named reason in the set; no ad-hoc refusal path exists and no module composes a refusal string of its own. *Rationale:* refusal grammar is closed; ad-hoc strings are unreachable. *Canon 7 §5.*
- **C7-R-020 · Watch refusals join same taxonomy.** The Watch's refusals join the closed taxonomy the same way every family joins it: a versioned addition to the reason registry, never a parallel grammar. *Rationale:* one refusal grammar across governance and security. *Canon 7 §5 · cross-ref Canon 8.*
- **C7-R-021 · Watch fault ≠ refusal.** A Watch fault, like any fault, is never dressed as a refusal. *Rationale:* preserves the fault/refusal split even for security events. *Canon 7 §5.*

#### §5.1 Actor-appropriate paths forward

- **C7-R-022 · Refusal offers only reader-executable actions.** A refusal offers only what its reader can actually do; offering an approval route where none exists, or an action this actor cannot perform, converts a refusal into a dead end dressed as a door. *Rationale:* refusal is a door with a reachable handle. *Canon 7 §5.1.*
- **C7-R-023 · Evidence-floor three-actions rule.** Where a conclusion falls below an objective's floor, the three available actions are exactly: accept as recorded statement, narrow the objective, or lower the standard. *Rationale:* fixed action set for evidence-floor refusals. *Canon 7 §5.1.*
- **C7-R-024 · Every refusal cell carries non-empty path forward.** Every refusal cell (including cells unreachable from live dispatch today) carries a non-empty path forward, asserted by a standing test. *Rationale:* future-reached cells still speak properly. *Canon 7 §5.1.*

#### §5.2 Entitlement refusal

- **C7-R-025 · Entitlement refusal is distinct named reason.** An entitlement refusal is a distinct named reason in the closed taxonomy, never folded into an evidence-floor refusal and never sharing its wording. *Rationale:* different reason ⇒ different handling. *Canon 7 §5.2.*
- **C7-R-026 · Evidence-floor actions do not apply to entitlement.** Accepting, narrowing, or lowering the standard are never offered on entitlement refusals. *Rationale:* actions must fit the reason class. *Canon 7 §5.2.*
- **C7-R-027 · Escalatable entitlement offers one action.** An escalatable entitlement rule offers exactly one action — request access from the authority the rule names. *Rationale:* points reader at the correct authority. *Canon 7 §5.2.*
- **C7-R-028 · Absolute entitlement offers no action.** An absolute entitlement rule offers no action, identically to any other absolute refusal. *Rationale:* absoluteness is uniform across refusal families. *Canon 7 §5.2.*
- **C7-R-029 · Refusal names rule in compliance-owner's words.** The entitlement refusal names the rule in the compliance owner's own words, never a generic "access denied". *Rationale:* a generic message teaches the requester nothing about alternate paths. *Canon 7 §5.2.*

### §6 The Shared-Derivation Pattern

- **C7-R-030 · One-module-owns-rule + negative scan.** Where a rule is enforced at more than one point, one module owns it and every caller imports that module; a negative scan prevents reimplementation elsewhere. *Rationale:* structural prevention beats convention. *Canon 7 §6.*
- **C7-R-031 · Shape-and-admission shared derivation.** The shaping surface and the admission surface share a single derivation, preventing shaping from freezing an objective the transform layer must later refuse. *Rationale:* prevents execution-time discovery of infeasibility. *Canon 7 §6.*

### §7 Grain and Form Compatibility

- **C7-R-032 · Explicit grain × form matrix.** Not every grain is available for every output form; the matrix is explicit rather than discovered by trial. *Rationale:* declarative combinability, not empirical. *Canon 7 §7.*
- **C7-R-033 · Qualified data grain allowability.** Qualified data supports per-claim and aggregated grains only; never synthesized-whole. *Rationale:* synthesized-whole from qualified data is a composed conclusion, a different form entirely. *Canon 7 §7.*
- **C7-R-034 · Composed conclusion grain.** A composed conclusion supports synthesized-whole only. *Rationale:* form-grain binding for composed conclusions. *Canon 7 §7.*
- **C7-R-035 · Knowledge artefact grain.** A knowledge artefact supports per-claim and aggregated. *Rationale:* form-grain binding for knowledge artefacts. *Canon 7 §7.*
- **C7-R-036 · Callable skill grain.** A callable skill answers per-claim or synthesized-whole depending on the query it receives. *Rationale:* form-grain binding for callable skills. *Canon 7 §7.*
- **C7-R-037 · Incompatible combos refused with path forward.** An incompatible grain × form combination is refused at the point it is chosen, with a path forward naming the form that supports the requested grain. *Rationale:* refusal-with-alternative pattern. *Canon 7 §7.*

### §8 Provenance Preservation

- **C7-R-038 · Declarative provenance floor per form.** Each output form declares the minimum provenance standard its transform can preserve; the rule table is declarative, evaluated by the shaping wizard in conversation. *Rationale:* declarative rules evaluate in shaping, no execution needed. *Canon 7 §8.*
- **C7-R-039 · Below-floor refuses during shaping.** A below-floor combination refuses during shaping, never at execution. *Rationale:* refusal arrives before commitment. *Canon 7 §8.*

### §9 Licence Class

- **C7-R-040 · Licence classes are configuration, versioned.** Licence class names, commissioner mappings, and per-feed attributes are configuration held in versioned files with the highest version in force. *Rationale:* licence taxonomy grows with commercial agreements without frozen contract events. *Canon 7 §9.*
- **C7-R-041 · Single-source licence selection.** Class derivation, the selection filter, and every per-feed standing attribute are read from one place, consumed identically by packaging, standing declaration table, and outer gate. *Rationale:* prevents distributed copies from disagreeing. *Canon 7 §9.*

### §10 Composition

- **C7-R-042 · Two composition paths matching two forms.** There are exactly two composition paths, matching two forms: qualified-data packaging and composed-conclusion reasoning. *Rationale:* form → path fixed. *Canon 7 §10.*
- **C7-R-043 · Qualified data packaging steps.** Qualified data path: selection by reach → standard filter → licence class → packaging → export through outer gate. *Rationale:* fixed ordered pipeline. *Canon 7 §10.*
- **C7-R-044 · Per-claim provenance end-to-end.** Per-claim provenance stays intact end-to-end in the qualified data path. *Rationale:* preserves provenance through packaging. *Canon 7 §10.*
- **C7-R-045 · Standard is an input filter, not downstream check.** Below-floor units never enter the deliverable at all; the standard is an input filter, not a downstream check. *Rationale:* filter-first prevents floor-violating units from entering. *Canon 7 §10.*
- **C7-R-046 · Composed conclusion five-stage.** A composed conclusion is reasoned through five-stage composition over selected units; the load-bearing set is identified; the conclusion's class is computed as the floor over that set. *Rationale:* structured reasoning path. *Canon 7 §10.*
- **C7-R-047 · Trace mandatory for composed conclusions.** The trace is mandatory for composed conclusions; the class travels inline with the answer. *Rationale:* trace + class travel with every answer. *Canon 7 §10.*
- **C7-R-048 · Deterministic fallback beneath every model reach.** Every composition that reaches for a model carries a deterministic fallback beneath it. *Rationale:* prevents degradation to unbounded output when top rung unavailable. *Canon 7 §10.*
- **C7-R-049 · Mechanical composer preserved byte-identical.** The mechanical composer is preserved byte-identical as the fallback for model-reaching compositions. *Rationale:* fallback stability is guaranteed by byte-identity, not by re-derivation. *Canon 7 §10.*

### §11 Grounding

- **C7-R-050 · Grounding is proven, not asserted.** A sentence that cannot be anchored to material is not a weaker sentence — it is a refusal. *Rationale:* unanchored ⇒ refuse, not lower confidence. *Canon 7 §11.*
- **C7-R-051 · Per-sentence anchor map for composed output.** Composed output carries a per-sentence anchor map and a gate enforces it. *Rationale:* enforcement is at sentence granularity. *Canon 7 §11.*
- **C7-R-052 · Grounding-gate-failure-path cell required.** Grounding is protected by its own cell suite including a cell asserting the failure path: an ungrounded composition refuses rather than degrading. *Rationale:* a gate whose failure path has never been tested has never been shown to close. *Canon 7 §11.*
- **C7-R-053 · Class-honesty negative scan.** A negative scan over the whole answering service prevents a composition from ever misstating the class it is answering at. *Rationale:* structural prevention of class-inflation. *Canon 7 §11.*

### §12 Telemetry

- **C7-R-054 · Sidecar telemetry per model-reaching composition.** Every model-reaching composition emits a sidecar record carrying the mode, the metering, and the outcome — separately from the answer itself. *Rationale:* telemetry lifecycle independent of answer envelope. *Canon 7 §12.*

## PART III · Delivery

### §13 The Async Contract

- **C7-R-055 · Fork determines contract entirely.** The admission fork determines the contract entirely: warm returns synchronous full response; fresh returns an accepted acknowledgement carrying objective identity, status, delivery estimate, and quote where applicable. *Rationale:* single fork drives everything downstream. *Canon 7 §13.*

#### §13.1 States

- **C7-R-056 · Late refusal is first-class terminal.** Accepted, then refused, is a normal terminal state, never a failure. *Rationale:* governance can conclude "refuse" late. *Canon 7 §13.1.*
- **C7-R-057 · Late refusal render as governed refusal.** A run admitted then found inadmissible (estate change, rule change, floor not reached) has not failed; integrating applications render it as a governed refusal. *Rationale:* consumer-side rendering rule. *Canon 7 §13.1.*
- **C7-R-058 · Sub-stages are not states.** Mining and transforming are deliberately not exposed as distinct states. *Rationale:* prevents pipeline-internal state changes from becoming breaking consumer changes. *Canon 7 §13.1.*

### §14 Thin Webhook, Governed Fetch

- **C7-R-059 · Webhook payload contents (four items).** The webhook payload carries the event, the objective identity, the trace identity, and the status; it never carries claim content. *Rationale:* content transits egress-gated channels, not push. *Canon 7 §14.*
- **C7-R-060 · Result fetched over authenticated key.** The result is fetched over the application's own authenticated key, with scope enforced server-side. *Rationale:* pull-based enforcement of scope. *Canon 7 §14.*
- **C7-R-061 · Polling is the fallback.** Polling the objective endpoint is the fallback wherever a webhook cannot be received. *Rationale:* content-fetch path is required, webhook is optional. *Canon 7 §14.*
- **C7-R-062 · Push-with-content would be uncontrolled egress.** Pushing claims to an application-configured URL would be an egress path the gates do not control; the webhook is thin for that reason. *Rationale:* preserves egress control point. *Canon 7 §14.*

### §15 Idempotency

- **C7-R-063 · Idempotency key required on every external submission.** An idempotency key is required on every external submission. *Rationale:* structural retry-safety. *Canon 7 §15.*
- **C7-R-064 · Duplicate resolves to existing state.** A retried request must not double-commission or double-charge; the same key resolves to the same objective, and a duplicate returns existing state rather than creating a second one. *Rationale:* prevents commercial double-hit. *Canon 7 §15.*
- **C7-R-065 · Idempotency at boundary, never in worker.** Idempotency runs at the boundary, never in the worker. *Rationale:* worker-level guard would still admit two objectives; boundary guard prevents admission entirely. *Canon 7 §15.*

### §16 Cancellation

- **C7-R-066 · Cancellation requires no reason.** Cancellation requires no reason; it references the commissioned terms and halts queued work while retaining what has completed. *Rationale:* no interrogation of the cancelling party. *Canon 7 §16.*
- **C7-R-067 · Cancellation invariants (two).** Nothing partial egresses on cancellation; the cancelled run is still recorded. *Rationale:* deterministic cancellation properties. *Canon 7 §16.*

### §17 Versioning and Sandbox

- **C7-R-068 · Envelopes frozen and additive.** Envelopes are frozen and additive; a field is added, a shape is never mutated. *Rationale:* backwards-compat guarantee. *Canon 7 §17.*
- **C7-R-069 · Breaking change = new path version.** A breaking change is a new path version. *Rationale:* consumers built against current contract keep working indefinitely. *Canon 7 §17.*
- **C7-R-070 · Sandbox mode set at registration.** Sandbox is a key mode set at registration, served entirely from fixture estate. *Rationale:* fixture estate provides realistic sandbox behaviour. *Canon 7 §17.*
- **C7-R-071 · Sandbox exercises full contract.** Sandbox exercises the full contract — including every refusal shape and the whole async lifecycle — before real material moves. *Rationale:* engineers must see every refusal shape before production. *Canon 7 §17.*
- **C7-R-072 · Only sandbox-vs-prod difference is the estate.** The only difference between sandbox and production is the estate behind it, and nothing else. *Rationale:* prevents contract-teaching mismatch. *Canon 7 §17.*

## PART IV · The Memory Layer

### §18 The Promise

- **C7-R-073 · Memory-plane per integration key.** Every integrated application receives a durable, governed memory plane that grows in proportion to its own use. *Rationale:* memory scales with usage, not anticipation. *Canon 7 §18.*
- **C7-R-074 · Zero memory infrastructure on integrator side.** The application arrives stateless and becomes knowledgeable; zero memory infrastructure is built on the application's own side. *Rationale:* platform provides the memory service. *Canon 7 §18.*
- **C7-R-075 · Estate holder full visibility.** Every application's memory is visible, receipted, rights-bound, and revocable to the estate holder. *Rationale:* integration deepens without governance thinning. *Canon 7 §18.*
- **C7-R-076 · Platform knows objective, not application.** The platform knows the objective and does not know the application — not what it renders, not what it does with what it receives, not who its users are. *Rationale:* allows N integrations without platform-surface warping. *Canon 7 §18.*

### §19 The Plane

- **C7-R-077 · One integration key = one memory plane.** Every integration key is issued with exactly one memory plane: a durable, instance-scoped, key-scoped partition, created at commissioning and existing for the key's entire lifetime. *Rationale:* one-plane-one-key cardinality. *Canon 7 §19.*

#### §19.1 Isolation

- **C7-R-078 · Plane isolation by construction.** The persistence layer refuses any read or write not scoped to a key's own plane — the same scoped-accessor pattern that enforces instance isolation. *Rationale:* isolation is at the store, not the caller. *Canon 7 §19.1.*
- **C7-R-079 · Cross-plane read unexpressible.** A cross-plane read does not exist as an operation to be permitted or denied; it cannot be expressed at all. *Rationale:* unrepresentable, not policed. *Canon 7 §19.1 · cross-ref Canon 1 §4.2.*
- **C7-R-080 · Sharing only via Registry.** Sharing happens only through the Registry, by rights-bound publication; no direct path between planes, no aggregate view. *Rationale:* Registry is the single publication channel. *Canon 7 §19.1.*

#### §19.2 Ledger-reconstructible

- **C7-R-081 · Every plane op writes a ledger row.** Every plane operation (read, write, retention change, revocation) writes a ledger row. *Rationale:* enables per-plane reconstruction. *Canon 7 §19.2.*
- **C7-R-082 · Plane reconstructible from ledger.** A plane can be reconstructed entirely from the ledger. *Rationale:* answers "what did this application know at time T" verifiably. *Canon 7 §19.2.*

#### §19.3 Revocation and deletion

- **C7-R-083 · Key revocation freezes plane.** Key revocation freezes the plane: no reads, no writes. *Rationale:* immediate access removal without evidence destruction. *Canon 7 §19.3.*
- **C7-R-084 · Plane deletion follows instance deletion ceremony.** Plane deletion follows the instance's own deletion ceremony — two-person approval, single authorised path, destruction attestation. *Rationale:* deletion is the authority act of Canon 3 §27. *Canon 7 §19.3 · cross-ref Canon 3 §27.*
- **C7-R-085 · Revoked key: published survives, unpublished deletes.** A revoked application's contributed units survive in the Registry iff they were published; unpublished contributions delete with the plane. *Rationale:* unpublished material was the application's working material under estate governance. *Canon 7 §19.3.*

### §20 Two Memories, Separated by Provenance

- **C7-R-086 · Reuse decided at write time, not read time.** What may be reused across keys is decided when the material is written, not when it is later read. *Rationale:* deciding at read time makes the boundary a policy each reader must apply; deciding at write time makes it a store property. *Canon 7 §20.*
- **C7-R-087 · Mixed-provenance stays in plane (customer framing).** Where provenance is mixed or unclear, the material stays in the plane; the estate may take the fact stripped of its framing, and the framing never travels. *Rationale:* fail-closed toward the customer's own thinking. *Canon 7 §20.*
- **C7-R-088 · Cross-key inquiry opacity.** One key never learns that another asked, what it asked, or the shape of its inquiry, even where its own answers improve from the shared estate underneath. *Rationale:* inquiry privacy across keys. *Canon 7 §20.*

### §21 The Write-Back Contract

- **C7-R-089 · Write-back turns query surface into memory service.** An application may contribute derived context, corrections, and conclusions back to its own plane. *Rationale:* memory accumulates rather than evaporating between calls. *Canon 7 §21.*

#### §21.1 Shape

- **C7-R-090 · Contributions land as qualified units (five-ring shape).** Every contribution lands as a qualified unit in the five-ring shape: content, provenance (the application, its key, calls it derived from), defensibility class, context, re-derivation handle. *Rationale:* uniform contribution shape enables downstream reasoning. *Canon 7 §21.1.*
- **C7-R-091 · No free-form blobs.** No free-form blobs are accepted. *Rationale:* uniformity requirement. *Canon 7 §21.1.*
- **C7-R-092 · Incomplete contribution rejects at boundary.** An incomplete contribution rejects at the API boundary — not stored and flagged, rejected outright. *Rationale:* prevents malformed accumulation that surfaces late. *Canon 7 §21.1.*

#### §21.2 Class and rights at birth

- **C7-R-093 · Contribution class distinct, internal-only rights.** Contributed units carry a distinct class and inherit internal-only rights at birth; rights default closed. *Rationale:* not exportable until explicitly made so. *Canon 7 §21.2.*
- **C7-R-094 · Defensibility capped at cited sources.** Defensibility is capped at what the cited sources support; an application citing inferred material cannot mint corroborated fact from it. *Rationale:* reasoning outside platform can't raise class more than reasoning inside it. *Canon 7 §21.2.*

#### §21.3 Visibility and setting

- **C7-R-095 · Plane-local by default.** Contributions are plane-local by default: visible only to the contributing application, invisible to reference application/briefs/other consumers. *Rationale:* default-private write-back. *Canon 7 §21.3.*
- **C7-R-096 · Write-back is a commissioning choice.** Write-back is a commissioning choice — on (with per-cycle volume ceiling) or off — visible to the compliance officer, as is volume actually written. *Rationale:* explicit commissioning ceremony. *Canon 7 §21.3.*

### §22 Publication

- **C7-R-097 · Publication is separate, never automatic.** Promoting a contributed unit from plane-local to Registry-visible is a separate act, never automatic. *Rationale:* an automatic promotion would let an application author estate record from outside. *Canon 7 §22.*
- **C7-R-098 · Publication passes quality gates + rights + release review.** Publication passes the quality gates of its output class, carries its rights, and passes release review where instance governance values require. *Rationale:* enforces boundary between working material and estate record. *Canon 7 §22.*

### §23 Usage-Proportional Persistence

- **C7-R-099 · Working set grows from observed use.** The working set grows from observed use, never from anticipation. *Rationale:* retention is proportional to usage. *Canon 7 §23.*
- **C7-R-100 · What retains: retention rules.** Units and partitions read repeatedly retain hot; repeated query shapes gain precomputed results; untouched strata never replicate into the plane. *Rationale:* three retention behaviours by use pattern. *Canon 7 §23.*
- **C7-R-101 · Working set holds references, not copies.** The working set holds references and derived read-structures — never copies that would escape rights binding. *Rationale:* prevents rights-drift via copies. *Canon 7 §23.*
- **C7-R-102 · Registry remains source of record.** Evicting an entry loses nothing; the Registry remains the source of record throughout. *Rationale:* eviction is safe. *Canon 7 §23.*
- **C7-R-103 · Memory growth reports per plane per cycle.** Memory growth reports per plane per cycle (units retained, precomputes held, storage consumed) to the application dashboard and to the compliance record simultaneously. *Rationale:* dual-audience reporting is enforced. *Canon 7 §23.*

### §24 The Integration Wizard

- **C7-R-104 · Integration = commissioning + memory plane.** Integrating an application is commissioning a standing objective with a memory plane attached; one flow, one ledgered act. *Rationale:* one act, not two. *Canon 7 §24.*
- **C7-R-105 · Three memory-specific additions to standard commissioning.** Runs the platform's standard objective-shaping with three memory-specific additions. *Rationale:* memory adds three steps only. *Canon 7 §24.*
- **C7-R-106 · No warm-up unobserved period.** The first call lands in the compliance record like every call after it; there is no warm-up period in which an integration runs unobserved. *Rationale:* observation from call one. *Canon 7 §24.*
- **C7-R-107 · Asymmetric re-scoping.** Widening retrieval scope or raising a ceiling re-enters the wizard at the scope step and re-commissions; tightening applies without ceremony. *Rationale:* ceremony scales with risk direction. *Canon 7 §24.*
- **C7-R-108 · Scope changes are ledger events either way.** Scope changes are ledger events in both directions; the asymmetry lives only in the ceremony. *Rationale:* record completeness invariant. *Canon 7 §24.*

### §25 Governance Visibility

- **C7-R-109 · Per-application view in compliance record.** The compliance record gains a per-application view in the same table shape as estate governance classes: scope, rights ceiling, write-back setting/volumes, storage growth, call activity, every scope change with ledger receipt. *Rationale:* per-application audit view uniform with governance. *Canon 7 §25.*
- **C7-R-110 · Contributed-unit volumes + publications as line items.** Contributed-unit volumes and publication events are line items, and publication passing release review cites its review record directly. *Rationale:* line-item traceability. *Canon 7 §25.*
- **C7-R-111 · Plane freeze/deletion as ceremony records.** Plane freeze and deletion appear as ceremony records. *Rationale:* freeze/deletion carry ceremony receipts. *Canon 7 §25.*
- **C7-R-112 · Nothing about memory is invisible to estate holder.** Nothing about an application's memory is invisible to the estate holder, ever. *Rationale:* full-visibility invariant. *Canon 7 §25.*

### §26 Quality Treatment of Contributed Units

- **C7-R-113 · Contributed units have their own quality row.** Contributed units are a transformation output class and carry their own quality row exactly as any other class does. *Rationale:* uniform quality shape across classes. *Canon 7 §26.*
- **C7-R-114 · Publication binds quality row.** Publication is where the quality row binds; plane-local contributions are sampled rather than gated, but nothing enters the Registry without passing the row first. *Rationale:* sampled locally, gated at publication. *Canon 7 §26.*

### §27 The Seam Contract

- **C7-R-115 · Named/typed/classed fields at seam.** Every field that crosses the seam is named, typed, and classed. *Rationale:* prevents undocumented seam mutation. *Canon 7 §27.*
- **C7-R-116 · Latency classes declared per operation with bounds.** Latency classes are declared per operation with bounds. *Rationale:* one-promise-across-different-shapes guarantees broken promise. *Canon 7 §27.*
- **C7-R-117 · Identity enforcement at seam, not downstream.** Identity enforcement sits at the seam itself, never downstream of it; aggregate promises are void if identifying material can cross alongside them. *Rationale:* boundary enforcement. *Canon 7 §27.*
- **C7-R-118 · Identical terms to internal use.** External seam runs on identical terms to internal use; no lighter-weight path for machines. *Rationale:* lighter machine path becomes the ungoverned path. *Canon 7 §27.*
- **C7-R-119 · Scope enforced server-side per call.** Scope is enforced server-side on every call; a key's reach is a property of the key as the platform itself holds it, never a caller-supplied parameter. *Rationale:* client-supplied scope is client-controlled boundary. *Canon 7 §27.*
- **C7-R-120 · Watch verdict seam is contract-grade.** The verdict seam between the Watch's two engines — and the record classes both authorities write — are named/typed/classed rows in Canon 9's matrix, consumed identically to every other contract. *Rationale:* Watch surface is a first-class seam. *Canon 7 §27 · cross-ref Canon 8 & Canon 9.*
- **C7-R-121 · Integration sees governed refusal only, never Watch interior.** An integration never sees the Watch's interior; it sees at most a governed refusal that a mark or hold produced, indistinguishable in shape from any other. *Rationale:* Watch mechanics stay opaque to integrators. *Canon 7 §27.*

## PART V · Applications on the Platform

### §28 What a Reference Application Is

- **C7-R-122 · Reference applications are not platform surfaces.** Reference applications are applications, specified fully because they demonstrate the platform's contract for every future application. *Rationale:* prevents them being seen as platform features. *Canon 7 §28.*
- **C7-R-123 · Reference apps use Integration-Console-issued keys on identical terms.** Each reference application consumes the platform through an Integration-Console-issued key, on identical terms to any third party (including Syni-built). *Rationale:* no in-house shortcut. *Canon 7 §28.*

### §29 The Developer Surface (three steps)

- **C7-R-124 · Three-step developer contract.** Contract-forward in three steps: register, first call, administer. *Rationale:* fixes the developer journey. *Canon 7 §29.*

#### §29.1 Register

- **C7-R-125 · Registration content.** Registration captures the application, its objective, the class of intelligence it reads; key grants stated plainly in the wizard's scope words; webhook URL and sandbox toggle set here. *Rationale:* register step contents. *Canon 7 §29.1.*

#### §29.2 First call

- **C7-R-126 · First-call response contract.** First call returns response with governance inline: class travels with every claim; refusal envelope is visible in its own shape; trace identity resolves to the same record the compliance audit reads. *Rationale:* teach the full contract at hello-world. *Canon 7 §29.2.*
- **C7-R-127 · Sandbox first-call parity.** Sandbox serves from fixture estate; full contract (including every refusal shape and async lifecycle) is exercised before real material moves. *Rationale:* engineers meeting first refusal in production handle it badly. *Canon 7 §29.2.*

#### §29.3 Administer

- **C7-R-128 · Administer view scope.** Applications, keys, usage, refusal health, and objective lifecycle are administered in one place. *Rationale:* unified admin. *Canon 7 §29.3.*
- **C7-R-129 · Refusal health is first-class view.** Refusal health is a first-class view, not an error log; rising refusal rate is read as information, never suppressed as noise. *Rationale:* refusals are information about objective fit. *Canon 7 §29.3.*

### §30 The Reference Application

- **C7-R-130 · Preset output form.** Reference application output is preset — composed conclusion, for a person, synthesized whole, at their floor; no output picker. *Rationale:* choosing output form is a commissioning act. *Canon 7 §30.*
- **C7-R-131 · Three visually distinct refusal-adjacent states.** Not-extracted-yet, evidence-cannot-support, and something-broke render as three visually distinct states; the third shares nothing (components, colour, layout) with the first two. *Rationale:* fault/refusal legibility for non-technical readers. *Canon 7 §30.*
- **C7-R-132 · Export = same artefact with class markings intact.** Export is a rendering of the same artefact with class markings intact; not a second product and not a re-shaping. *Rationale:* different form/grain is a new objective. *Canon 7 §30.*

### §31 The Buyer Path

- **C7-R-133 · Buyer promise.** Buyer promise: know what you are buying, acquire it lawfully, use it with confidence. *Rationale:* buyer contract sentence. *Canon 7 §31.*
- **C7-R-134 · Friction-as-assurance.** The friction of acquisition renders as the assurance that makes the data theirs. *Rationale:* re-framing of buyer friction. *Canon 7 §31.*

#### §31.1 Shaping within offerability

- **C7-R-135 · Shaping agent proposes within offerability.** The shaping agent works within offerability (owned estate only, licence class, disclosure limits) and may propose. *Rationale:* steering toward cheaper feasible shape is sales, not laundering. *Canon 7 §31.1.*
- **C7-R-136 · Buyer shaping ≠ operator shaping.** This is the one place the shaping agent's posture differs from its operator variant (operator asks, never proposes). *Rationale:* fixed divergence point between operator and buyer variants. *Canon 7 §31.1.*
- **C7-R-137 · Shape-outside-offerability is refused with reason.** A shape outside offerability is refused with the reason. *Rationale:* offerability is boundary of proposability. *Canon 7 §31.1.*
- **C7-R-138 · Buyer never sets lawful basis.** The buyer never sets lawful basis; use-purpose drives licence class instead. *Rationale:* prevents buyer laundering of lawful basis. *Canon 7 §31.1.*
- **C7-R-139 · Live price/delivery updates.** Price and delivery time compute live and move as the shape moves. *Rationale:* trade-off stays visible while it can still be changed. *Canon 7 §31.1.*

#### §31.2 Acquisition

- **C7-R-140 · Outer gate five checks = acquisition.** Acquisition is rendered as the outer gate's five checks: rights, irreversibility, cumulative disclosure, licence issue, receipt. *Rationale:* five-check chokepoint. *Canon 7 §31.2.*
- **C7-R-141 · No partial egress at outer gate.** Nothing partial egresses here either. *Rationale:* perimeter invariant. *Canon 7 §31.2.*

#### §31.3 The deliverable

- **C7-R-142 · Per-claim class + publicly resolvable receipt.** The deliverable carries per-claim class on every item and a receipt resolving publicly by trace identity — the same record any audit sees. *Rationale:* dual-audience deliverable. *Canon 7 §31.3.*
- **C7-R-143 · Receipt cannot aid reversal.** The receipt renders the fact and the fingerprint of the transform only; never anything that could aid reversal. *Rationale:* protects transform confidentiality. *Canon 7 §31.3.*

### §32 The Customer Portal

- **C7-R-144 · Portal scope enforced at persistence layer.** Scope is enforced at the persistence layer; a query outside the customer's own account does not execute. *Rationale:* interface-layer enforcement is bypassable by any new code path. *Canon 7 §32.*
- **C7-R-145 · Purchased intelligence carries licence label + quality card.** Purchased intelligence carries its licence label and its quality card — what was bought, at what standard, under what terms to use it. *Rationale:* buyer holds the labelled truth about the thing. *Canon 7 §32.*
- **C7-R-146 · Consumption metered at boundary.** Consumption is metered at the boundary. *Rationale:* unmetered consumption is unpriceable. *Canon 7 §32.*

## PART VI · Traces and Failure

### §33 Three Traces, End to End

#### §33.1 A call arrives and is answered

- **C7-R-147 · Warm-fork end-to-end trace.** Warm-fork trace: key resolves to objective version/memory plane/rights envelope → admission checks completeness + feasibility → retrieval draws from evidence partitions within plane's retrieval scope → boundary chokepoint (de-identify/invoke/re-identify/receipt) if a model is reached → grounding gate enforces anchor map → assertion boundary computes class as floor over load-bearing units → answer returns with class inline and trace identity resolvable → Ledger records the call. *Rationale:* canonical warm-fork trace. *Canon 7 §33.1 · cross-ref Canon 3 §13.1.*
- **C7-R-148 · Warm-fork alt paths.** Warm-fork alt outcomes: not-extracted-yet refusal (offers to file the work); evidence-cannot-support refusal (names specific reason); ungrounded refusal (rather than degrading); retrieval timeout (surfaces on the fault channel, never dressed as either kind of refusal). *Rationale:* alt-outcome enumeration for warm fork. *Canon 7 §33.1.*

#### §33.2 A fresh objective is delivered

- **C7-R-149 · Fresh-fork end-to-end trace.** Fresh-fork trace: admission → accepted ack with objective identity/estimate/quote → work dispatches → thin webhook (event + objective id + trace id + status; no content) → application fetches over own authenticated key (scope server-side) → outer gate runs five checks and mints receipt → deliverable carries per-claim class → receipt resolves publicly by trace identity. *Rationale:* canonical fresh-fork trace. *Canon 7 §33.2.*
- **C7-R-150 · Fresh-fork alt paths.** Fresh-fork alt outcomes: cancellation (nothing partial egresses, cancellation recorded); post-acceptance refusal (same refusal envelope as governed terminal); retry (idempotency key resolves to existing objective, not a second). *Rationale:* alt-outcome enumeration for fresh fork. *Canon 7 §33.2.*

#### §33.3 Application contributes and later publishes

- **C7-R-151 · Contribute-publish end-to-end trace.** Contribute trace: application writes derived conclusion back → API boundary checks five-ring shape (content, provenance including calls it derived from, class, context, re-derivation handle) → class capped at what cited sources support → unit lands plane-local with internal-only rights, invisible to every other consumer → write lands in Ledger and per-application compliance view; publish trace: quality row passed → rights carried → release review passed if governance requires → unit becomes Registry-visible. *Rationale:* canonical write-back + publication trace. *Canon 7 §33.3.*
- **C7-R-152 · Contribute-publish alt paths.** Alt outcomes: incomplete contribution rejects at boundary (not stored and flagged); cited sources insufficient (class capped, not full-value); volume ceiling reached (further writes refuse for the cycle); key revoked (plane freezes, unpublished contributions delete alongside). *Rationale:* alt-outcome enumeration for contribute/publish. *Canon 7 §33.3.*

### §34 Failure

- **C7-R-153 · Fault ≠ refusal (restated).** A fault is distinct from a refusal everywhere in this contract; the distinction is never blurred for convenience. *Rationale:* semantic separation. *Canon 7 §34.*
- **C7-R-154 · Fault vs refusal meaning.** A refusal is the system working correctly and declining; a fault is the system failing to evaluate a request at all. *Rationale:* fixes the semantic definitions. *Canon 7 §34.*
- **C7-R-155 · Retry-after-fault is safe by construction.** A retried request after a fault is safe by construction, everywhere idempotency applies. *Rationale:* caller retrying-on-fault and getting refusal has learned the request was in fact evaluated in between. *Canon 7 §34.*

## PART VII · The Function & Promise Registry

### §35 What It Is

- **C7-R-156 · Registry: single canonical versioned artefact.** One canonical, versioned artefact registers every named function in the platform — gate, engine behaviour, worker obligation, console guarantee — with the promise it protects and its full accounting. *Rationale:* single source of function truth. *Canon 7 §35.*
- **C7-R-157 · Registry lifecycle.** Registry begins as a governed document and, on dispatch, graduates to a machine-readable artefact. *Rationale:* two-phase lifecycle. *Canon 7 §35.*
- **C7-R-158 · Registry consumers (three).** Registry is the single source every standing query runs against, the input the sequencing harness optimises over, and the operating context a model worker itself receives. *Rationale:* three explicit consumer roles. *Canon 7 §35.*
- **C7-R-159 · Function governor scope.** Every function belongs to one of the six engines, to the Watch, or to a named surface for an interface-level guarantee. *Rationale:* limits governor space. *Canon 7 §35.*
- **C7-R-160 · No new top-level category without ratification.** No new top-level category is added without explicit ratification. *Rationale:* prevents shadow governor classes. *Canon 7 §35.*

### §36 Schema — One Row Per Function

- **C7-R-161 · Registry row: 11 mandatory fields.** All 11 fields are mandatory: function_id, governor, mandate, promise, service_trace, surface, enforcement, cost, dependencies, ladder_rung, owner. *Rationale:* a row missing any field is not a registered function. *Canon 7 §36.*
- **C7-R-162 · function_id · stable, namespaced, never reused.** function_id is stable, namespaced under its owning engine or surface, never reused. *Rationale:* stable identity across time. *Canon 7 §36.*
- **C7-R-163 · governor · one of six/Watch/surface.** governor is one of the six engines, the Watch, or a named surface; no new top-level without ratification. *Rationale:* enforces governor closed set. *Canon 7 §36.*
- **C7-R-164 · mandate · "Built to …" active voice.** mandate is one active-voice testable sentence stating what, never how. *Rationale:* what-not-how testability. *Canon 7 §36.*
- **C7-R-165 · promise · observable-breach phrasing.** promise is phrased so its breach is observable; many functions may cite one promise; no function may cite zero. *Rationale:* observability + non-zero cardinality. *Canon 7 §36.*
- **C7-R-166 · service_trace · invalid ⇒ orphan.** service_trace is the service sentence and journey step this promise secures; empty or invalid trace is an orphan. *Rationale:* orphan-detection rule. *Canon 7 §36.*
- **C7-R-167 · surface · where the function acts.** surface is module path / route / contract / console element. *Rationale:* localizes the function on disk. *Canon 7 §36.*
- **C7-R-168 · enforcement · mechanism class (closed set).** enforcement is a mechanism class from a closed set: byte-identity lock, structural walk, negative scan, runtime check, end-to-end cell, type-level wall, or constraint architecture — natural-language-only is not a legal value. *Rationale:* explicit ban on NL-only enforcement. *Canon 7 §36.*
- **C7-R-169 · cost · execution time class + burden + FP rate.** cost is execution time class, maintenance burden, false-positive rate where known; unknown is a legal initial value replaced by measurement. *Rationale:* cost data is enterable then measurable. *Canon 7 §36.*
- **C7-R-170 · dependencies · ordered-before functions/data.** dependencies are functions or data this one requires ordered-before it — the input to sequencing. *Rationale:* enables sequencing harness. *Canon 7 §36.*
- **C7-R-171 · ladder_rung · justified placement.** ladder_rung is the implementing rung; written justification is required for any placement above the cheapest plausible one. *Rationale:* prevents rung inflation (D4). *Canon 7 §36.*
- **C7-R-172 · owner · change authority.** owner is the change authority for the row. *Rationale:* named authority per row. *Canon 7 §36.*

### §37 Derivation Rules

- **C7-R-173 · No gate without a promise.** A function whose promise field cannot be honestly filled is not refactored into legitimacy; it is retired. *Rationale:* orphan-gate rule. *Canon 7 §37.*
- **C7-R-174 · No promise without a service trace.** A promise serving no journey step of any service sentence is either mis-stated or evidence of drift — escalated, never papered over. *Rationale:* traceless promise is defect. *Canon 7 §37.*
- **C7-R-175 · No journey step without enforcement.** Every step of every service journey resolves to at least one registered function protecting it; an unprotected step is reported as exposed liability, never assumed safe. *Rationale:* liability surfacing rule. *Canon 7 §37.*
- **C7-R-176 · New functions register before landing.** Any proposal introducing a gate or worker obligation includes its registry row as part of its own ruling surface, not as a follow-up. *Rationale:* register-first discipline. *Canon 7 §37.*

### §38 The Three Standing Queries

- **C7-R-177 · Standing queries run on every change + on cadence.** The three standing queries run on every registry change and on a standing cadence. *Rationale:* cadence + change-triggered. *Canon 7 §38.*
- **C7-R-178 · Query results are reports, not automations.** Retiring or merging a function executes through the platform's ruling process, never automatically. *Rationale:* automation prevents human judgement. *Canon 7 §38.*
- **C7-R-179 · Redundancy query.** Two or more functions sharing the same promise and the same surface = merge/retire candidates, ranked by cost. *Rationale:* redundancy detection. *Canon 7 §38.*
- **C7-R-180 · Orphans query.** A function with an empty or invalid promise or service trace = retirement candidate on sight. *Rationale:* orphan detection. *Canon 7 §38.*
- **C7-R-181 · Gaps query.** A promise or journey step with no function enforcing it = exposed-liability report surfaced before an incident finds it. *Rationale:* liability detection. *Canon 7 §38.*

### §39 Population Is Archaeology, Not Authorship

- **C7-R-182 · Registry populates by extraction only.** Registry populates by extraction from what already exists — engine mandate documents, rulings record, close-report gate rosters. *Rationale:* archaeology, not authorship. *Canon 7 §39.*
- **C7-R-183 · Missing promise ⇒ orphan finding, never invention.** Where extraction finds a gate whose promise cannot be recovered, that is an orphan finding, never an invitation to write one in. *Rationale:* prevents synthetic promise creation. *Canon 7 §39.*

### §40 The Registry Pays Rent

- **C7-R-184 · Registry restructured on stall.** Registry rent = the three standing queries; if it stops retiring functions/finding gaps/cheapening sequences over a sustained period, it is itself restructured. *Rationale:* rent doctrine on the Registry itself. *Canon 7 §40.*
- **C7-R-185 · One artefact, one schema; second layer = D5.** A second layer above Registry is a defect on sight. *Rationale:* meta-spiral prevention. *Canon 7 §40.*

## PART VIII · The Critic Seam

### §41 What It Is

- **C7-R-186 · Critic Seam mechanises half of quality.** Critic Seam mechanises the mechanisable half of quality assurance — verification of worker output against the on-disk record. *Rationale:* honesty about scope. *Canon 7 §41.*
- **C7-R-187 · Deliberately does not attempt the other half.** The layer deliberately does not attempt the non-mechanisable half. *Rationale:* honest scope boundary. *Canon 7 §41.*

#### §41.1 The mechanisable split

- **C7-R-188 · Verifications mechanise; frame changes do not.** Every catch this layer makes is a verification — truth existed on disk and the worker diverged from it. Frame changes are a change to canon, not a divergence from it. *Rationale:* fixes what the layer can and cannot catch. *Canon 7 §41.1.*
- **C7-R-189 · Frame authority sits outside Critic scope.** Frame authority sits permanently outside this layer's scope. *Rationale:* prevents scope creep into canon-editing. *Canon 7 §41.1.*

### §42 Design Principles

- **C7-R-190 · Detect, never decide.** The layer emits findings; every consequence is a ruling made elsewhere. *Rationale:* prevents unmandated governor. *Canon 7 §42.*
- **C7-R-191 · Canon is the oracle.** All deterministic verification resolves against the on-disk record — never against a summary, a context window, or another model's recollection. *Rationale:* oracle discipline. *Canon 7 §42.*
- **C7-R-192 · Zero loop drag.** The layer adds no turns and never blocks execution mid-flight; deterministic checks run as cells at submission boundaries; the critic runs asynchronously between turns; findings arrive with the artefacts they review, never before. *Rationale:* async by construction. *Canon 7 §42.*
- **C7-R-193 · Halving, not zeroing — stated honestly.** Claim is that it catches the record-verifiable half and measurably shrinks what remains; never claim it catches everything. *Rationale:* honest advertisement. *Canon 7 §42.*
- **C7-R-194 · Critic calibrated like a model.** Catch rate and false-alarm rate per worker class are versioned, measured numbers, maintained by human sampling on an ongoing basis. *Rationale:* prevents unmeasured layer. *Canon 7 §42.*
- **C7-R-195 · Critic pays rent (shrink or retire).** Its catch-and-false-alarm ledger stands as any function's; if it stops catching and starts noising, it shrinks or retires by ruling. *Rationale:* structural rent. *Canon 7 §42.*
- **C7-R-196 · No layer sits above Critic.** No layer sits above the Critic, ever. *Rationale:* prevents infinite regress. *Canon 7 §42.*

### §43 Tier One — Deterministic Record Verification

- **C7-R-197 · Six check families at both boundaries.** Six mechanical check families run at both submission boundaries and on ruling documents at landing time. *Rationale:* boundary coverage. *Canon 7 §43.*
- **C7-R-198 · Each check emits pass/finding row.** Each check emits a pass or a finding row. *Rationale:* uniform output shape. *Canon 7 §43.*
- **C7-R-199 · Acceptance requires all six families at both boundaries.** Acceptance requires all six families to run at both boundaries; a run without them is incomplete. *Rationale:* prevents partial adoption. *Canon 7 §43.*
- **C7-R-200 · Findings cross-referenced, never duplicated.** Findings are cross-referenced and never duplicated. *Rationale:* prevents finding-noise. *Canon 7 §43.*
- **C7-R-201 · Tier-One checks register with own rows.** The checks themselves register in the Function & Promise Registry with their own rows — they are functions, and they pay rent like every other one. *Rationale:* Critic checks are first-class registered functions. *Canon 7 §43.*
- **C7-R-202 · Residual conceded.** Tier One verifies form and existence, not pertinence — an artefact written to the letter of its schema can still cite real hashes for irrelevant objects. *Rationale:* honesty about residual. *Canon 7 §43.*
- **C7-R-203 · Tier One alone is dishonest.** Adopting Tier One alone buys the cheap half of the guarantee while advertising the whole of it. *Rationale:* two tiers designed as a pair. *Canon 7 §43.*

### §44 Tier Two — The Critic Pass

- **C7-R-204 · Independent model reviews each proposal/close.** An independent model instance reviews each proposal and close report against a fixed rubric, asynchronously, after landing. *Rationale:* post-landing review. *Canon 7 §44.*
- **C7-R-205 · Output shape: classed, cited, non-blocking findings.** Findings report is classed, cited, never blocking, never editing. *Rationale:* detection, not decision. *Canon 7 §44.*

#### §44.1 Independence

- **C7-R-206 · Critic never shares worker conversation.** The critic never shares the worker's conversation; context is exactly the artefact, the canon set, the authorising instrument, and the rubric — never worker reasoning/drafts/self-justification. *Rationale:* prevents blind-spot inheritance. *Canon 7 §44.1.*
- **C7-R-207 · No worker critiques its own output.** No worker critiques its own output. *Rationale:* independence rule. *Canon 7 §44.1.*
- **C7-R-208 · Base-model share: context isolation + seeded audits.** Where both instances share a base model, independence is held by context isolation alone, and seeded audits measure whether that isolation is sufficient. *Rationale:* measure isolation, don't assume. *Canon 7 §44.1.*
- **C7-R-209 · Critic runs at cheapest sufficient rung, per artefact.** The critic runs one review per artefact rather than per token; cost per review held as a standing metric. *Rationale:* prevents rung inflation on critic itself. *Canon 7 §44.1.*
- **C7-R-210 · Findings carry honesty grammar.** A finding states what it checked, what it found, at what confidence class, with citations; an unclassed finding is itself a finding. *Rationale:* recursive honesty rule. *Canon 7 §44.1.*

#### §44.2 Three failure modes, structural answers

- **C7-R-211 · Rubber-stamping answered by seeded-defect audits.** Found-nothing is credible only from a critic whose detection is measured against known positives. *Rationale:* prevents look-at-nothing critic. *Canon 7 §44.2.*
- **C7-R-212 · Noise answered by false-alarm ledger.** A critic repeatedly ruled to make non-findings has its rubric tightened or scope shrunk, by ruling. *Rationale:* prevents rewarded-for-finding drift. *Canon 7 §44.2.*
- **C7-R-213 · Infinite regress stopped by construction.** The critic's findings are subject only to deterministic checks and human sampling; there is no critic of the critic, and proposing one is itself a finding. *Rationale:* halts regress. *Canon 7 §44.2.*

### §45 Tier Three — Human Calibration

- **C7-R-214 · Human reviewing role compresses, does not disappear.** Three lightweight instruments produce versioned numbers; the matrix's stratified human samples double as the critic's calibration. *Rationale:* one calibration mechanism, three consumers. *Canon 7 §45 · cross-ref Canon 4 §49.*
- **C7-R-215 · Stale calibration renders uncalibrated at surface.** A critic whose calibration has gone stale past its window renders findings marked uncalibrated — the same honesty rule as model confidence. *Rationale:* uniform staleness handling. *Canon 7 §45.*
- **C7-R-216 · One calibration form, three consumers.** Fact-confidence calibration, build-time critic ledger, and production critic per-class ledger are the same versioned, staleness-marked form. *Rationale:* single-mechanism doctrine. *Canon 7 §45.*
- **C7-R-217 · Second parallel calibration is D5.** A second, parallel calibration mechanism anywhere is a defect on sight. *Rationale:* meta-spiral prevention. *Canon 7 §45.*

### §46 What This Layer Is Not (5 exclusions)

- **C7-R-218 · Not a governor.** Holds no mandate, asserts nothing about the estate, gates nothing but form. Veto-authority proposals are rejected in advance. *Rationale:* forbids Critic becoming governance. *Canon 7 §46.*
- **C7-R-219 · Not a replacement for the human seat.** Frame changes are constitutionally outside a canon-verifying layer's reach; the largest course corrections are frame changes, and this layer catches none of them by design. *Rationale:* honesty about non-coverage. *Canon 7 §46.*
- **C7-R-220 · Not inline.** Nothing here adds a synchronous step to any serving path, or a turn to any loop. *Rationale:* async-only rule. *Canon 7 §46.*
- **C7-R-221 · Not a new meta-artefact class.** Reuses platform's standing machinery — query patterns, registry rows, calibration-ledger form — rather than inventing its own. *Rationale:* reuse-over-invention. *Canon 7 §46.*
- **C7-R-222 · Not a zero-residual claim.** It halves the residual measurably and repeatedly; its dashboard is built to show misses, not hide them. *Rationale:* honesty invariant. *Canon 7 §46.*

## PART IX · Discipline

### §47 Defect Classes (D1–D8)

- **C7-R-223 · Defects reportable on sight by anyone.** Named defect classes are reportable on sight by anyone (owner, builder, system). *Rationale:* everyone-can-file discipline. *Canon 7 §47.*
- **C7-R-224 · D1 · Orphan gate.** A function with no honest promise, or no service trace. *Rationale:* orphan-gate definition. *Canon 7 §47.*
- **C7-R-225 · D2 · NL-only enforcement.** A rule whose only enforcement is prose interpretation, with no machine-checked twin. *Rationale:* NL-only ban. *Canon 7 §47.*
- **C7-R-226 · D3 · Curated verdict.** Any selection of validation material by favourability rather than measured composition. *Rationale:* corpus-selection defect. *Canon 7 §47.*
- **C7-R-227 · D4 · Rung inflation.** Model-ladder placement above cheapest-sufficient, with no written justification on record. *Rationale:* rung-inflation defect. *Canon 7 §47.*
- **C7-R-228 · D5 · Meta-spiral.** A second governance layer above one that already exists; a governance artefact that has stopped paying rent. *Rationale:* meta-spiral defect. *Canon 7 §47.*
- **C7-R-229 · D6 · Service conflation.** A platform function optimised for an end-user persona rather than for a service sentence — the wrong job, done well. *Rationale:* mis-optimisation defect. *Canon 7 §47.*
- **C7-R-230 · D7 · Invented schedule or scope.** Sequencing, deferral, or workstreams introduced without explicit instruction — binding on ruling authority and builder alike, no exception. *Rationale:* invented-schedule defect. *Canon 7 §47.*
- **C7-R-231 · D8 · Dual-identity execution.** A task holding, or a code path permitting, more than one authority's identity or scope within a single execution — including evidence crossing between authorities outside Canon 9's matrix. *Rationale:* dual-identity defect. *Canon 7 §47 · cross-ref Canon 8 W11 & Canon 9.*

### §48 Canon Before Ruling

- **C7-R-232 · Canon-before-ruling doctrine (restated).** No decision proceeds from memory or summary where the governing document exists; unread canon is read before ruling — binding on ruling authority and builder alike, no exception. *Rationale:* Canon 1 §4.11 applied here. *Canon 7 §48.*
- **C7-R-233 · Recollection-as-fact is the exact failure this rule prevents.** A recollection presented as fact, where the written record exists and was simply not consulted, is the exact failure this rule exists to prevent. *Rationale:* named failure mode. *Canon 7 §48.*

### §49 Every Phase Closes on Disk

- **C7-R-234 · Phase opens with proposal on disk.** A phase opens with a proposal written to disk. *Rationale:* on-disk shape. *Canon 7 §49.*
- **C7-R-235 · Phase closes with close report + gate roster + hashes + registry attest + conformance + self-audit.** A phase closes with a close report carrying its gate roster with results, its artefact hashes, its registry attestation, a conformance table, and a self-audit. *Rationale:* six-part close report shape. *Canon 7 §49.*
- **C7-R-236 · No close report on disk ⇒ not closed.** A phase with no on-disk close report is not closed, whatever a conversation about it concluded. *Rationale:* on-disk primacy. *Canon 7 §49.*
- **C7-R-237 · Self-audit "reviewed" ≠ evidence.** A self-audit row whose evidence is "reviewed" or "checked manually" is not evidence; evidence column names a test identifier, gate result, or artefact hash. *Rationale:* verifiable evidence rule. *Canon 7 §49.*
- **C7-R-238 · Every ruling lands the same day.** Every ruling lands the same day as a file citing what it rules on; a ruling that exists only in conversation does not exist. *Rationale:* same-day-file discipline. *Canon 7 §49.*
- **C7-R-239 · New function registers row before landing.** Every new function registers its row before it lands, as part of the same ruling surface rather than as follow-up. *Rationale:* register-before-land. *Canon 7 §49.*
- **C7-R-240 · Build journal carries no undocumented window.** A gap in the build journal is closed by a reconciliation entry enumerating every change landed within it, with citations; an undocumented window is itself a violation. *Rationale:* time-continuity discipline. *Canon 7 §49.*

### §50 What This Specification Comes Down To

- **C7-R-241 · One-fork-once-at-boundary.** A request is answered warm or forked fresh, once, at the boundary; every consumer downstream honours that fork rather than re-deriving it. *Rationale:* summary rule 1. *Canon 7 §50.*
- **C7-R-242 · Refusal is governed, never error, never dead-end.** A refusal is a governed outcome carrying a named reason and an action the reader can actually take — never an error, and never a dead end dressed as a door. *Rationale:* summary rule 2. *Canon 7 §50.*
- **C7-R-243 · Application memory usage-proportional + isolated + visible.** Application memory grows from what it actually uses, stays isolated by construction rather than discipline, and is visible to the estate holder in full. *Rationale:* summary rule 3. *Canon 7 §50.*
- **C7-R-244 · Every function has a promise + trace, or retired.** Every function can state the promise it protects and the journey step that promise secures, or it is retired. *Rationale:* summary rule 4. *Canon 7 §50.*
- **C7-R-245 · No trust to memory where record exists.** Nothing about how the platform was built is trusted to memory where the record already exists to be read instead. *Rationale:* summary rule 5. *Canon 7 §50.*

---

## Extraction summary

- **Total rules extracted:** 245 (C7-R-001 through C7-R-245).
- **Coverage:** §§1–50 inclusive; every subsection with substantive material has at least one rule.
- **Cross-refs surfaced for Task-3 targeted checks:** Canon 1 §4.2 (unrepresentable), Canon 1 §4.11 (canon before ruling), Canon 3 §6.1 (declaration), Canon 3 §13.1 (boundary chokepoint), Canon 3 §22 (Registries governance), Canon 3 §22.1 (entitlement rules), Canon 3 §27 (deletion ceremony), Canon 4 §49 (calibration mechanism), Canon 8 (whole — Watch), Canon 9 (matrix).
- **Absence findings:** none — every section number encountered in the text is represented.
