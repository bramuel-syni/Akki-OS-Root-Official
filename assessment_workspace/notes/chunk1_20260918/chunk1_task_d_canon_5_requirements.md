# Canon 5 · Akki Interface Architecture · Requirements Checklist

**Source:** `/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_5_Interface_Architecture.txt` (547 lines · 47,130 B · sha256 `d0f17bab1bee9bad478950b491a0764a92363ce6fcba82c7d16822840eaf7780`)
**Doc title verbatim:** `Akki Interface Architecture`
**Rule set:** 2c · atomic single-line rule + one-line rationale + section anchor.

---

## Part I · The Design Law

- **C5-R-001 · Governance felt as trust, not machinery.** Experience must make governed intelligence usable by non-analysts. *Canon 5 §1.*
- **C5-R-002 · No surface mirrors internals.** Interface rendering the build (engines/gates/phases) is a defect regardless of fidelity. *Canon 5 §1.*
- **C5-R-003 · Register is professional, not consumer.** Simple (one primary action per screen; 1–3 steps to complete anything) but seasoned (dense info on calm layout, every number with provenance, no marketing chrome); progressive disclosure is house standard. *Canon 5 §1.*
- **C5-R-004 · Eight global rules bind every surface.** A violating screen is not exception-candidate — it is wrong. *Canon 5 §2.*
- **C5-R-005 · Rule 2.1 · No build state on any surface.** No phase badges, gate names, fixture names, or engine names appear as navigation; user never meets "Mtafiti" etc. *Canon 5 §2.1.*
- **C5-R-006 · Rule 2.2 · Class with claim.** Wherever a claim appears, its defensibility class appears adjacent, in plain language, in the headline position; no render path in which claim is separable from class. *Canon 5 §2.2.*
- **C5-R-007 · Rule 2.3 · Refusal rendering.** A governed refusal occupies the answer position with warning treatment; names the gap; shows what was asked vs the class the material supports; offers only actions the reader can actually take; never rendered as an error. *Canon 5 §2.3.*
- **C5-R-008 · Rule 2.4 · Four response classes, never conflated.** Answered · Held (not yet extracted) · Refused (evidence cannot support) · Fault (something broke) — no two share a component, colour, or layout. *Canon 5 §2.4.*
- **C5-R-009 · Refused names one family, not one reason.** Evidence-floor refusal + entitlement refusal (D7 §5.2) render through identical card — only words inside differ. *Canon 5 §2.4.*
- **C5-R-010 · Rule 2.5 · Agent-assumed marking.** Any value an agent supplied carries an amber agent-assumed chip visible through to commit; seam between user-said and agent-inferred stays visible to moment of commitment. *Canon 5 §2.5.*
- **C5-R-011 · Rule 2.6 · One trace thread.** Every intelligence element links to its trust receipt by trace identity; public receipt is read-only and IS the same record compliance audit reaches — never a summary generated separately. *Canon 5 §2.6.*
- **C5-R-012 · Rule 2.7 · Plain language.** No configuration syntax, enumeration values, or serialised data on any surface — one exception: Integration Console contract views where the contract itself is the product being shown. *Canon 5 §2.7.*
- **C5-R-013 · Rule 2.8 · Visual family.** Calm header carrying product + person's role; quiet defaults; at most one attention card per exceeded threshold; bordered row lists; minimal chrome; calm by default — system brings user what needs them, does not present dashboard of everything. *Canon 5 §2.8.*
- **C5-R-014 · Application boundary is mechanical.** Person not running the platform touches a surface → surface is an application → enters through Integration Console; internal privilege is a key class enforced server-side, never a back door. *Canon 5 §3.*
- **C5-R-015 · Reference application is not a platform surface.** Consumes platform through Integration-Console-issued key; demonstrates contract every future application follows; one implementation of asking, never the definition. *Canon 5 §3.*
- **C5-R-016 · Commerce is application layer entirely.** No buyer touches console or extraction machinery; buyer is end-user of commercial product which itself passes governed boundary as any third party; no privileged path anywhere. *Canon 5 §3.*
- **C5-R-017 · Three motions.** Verification (compliance owner, continuously — checking governance holds) · Exploration (business users — finding what estate supports before budget) · Consumption (anyone with a question — receiving answer with own defensibility). Every screen belongs to exactly one motion. *Canon 5 §4.*
- **C5-R-018 · Day-zero success = both dashboards live + populated simultaneously at close of onboarding.** Test objectives at commissioning verify parameters, never produce value; mining is verification, never demonstration. *Canon 5 §4.*

## Part II · The Visual System

- **C5-R-019 · Palette is fixed.** 13 tokens with hex values enumerated in §5 — no ad-hoc values, no per-surface variants. *Canon 5 §5.*
- **C5-R-020 · Palette values.** `--paper` #faf9f2 (application background) · `--surface` #f2f0e9 · `--surface-2` #ece9e1 · `--line` #ddd9ce · `--ink` #1a211d (body text) · `--ink-2` #3e4642 · `--ink-3` #6b7370 (tertiary, timestamps, unmeasured) · `--blue` #1e3a5f (headings, primary actions, platform identity) · `--blue-deep` #131f30 · `--oxblood` #7e3038 (refusals, absolute states, destructive) · `--oxblood-2` #8c3a34 · `--brass` #8a6a38 (held states, criteria crossings) · `--sage` #2e6b4f (measured-and-sound, acceptance passed). *Canon 5 §5.*
- **C5-R-021 · Oxblood reserved for refusal + destruction.** Never emphasis, branding, or CTA; without reading, a person must conclude refused or irreversible. *Canon 5 §5.*
- **C5-R-022 · State colour rendering.** Answered = `--sage` text + 2px left rule, never filled bg · Held = filled `--surface` + 3px left rule brass · Refused = filled `--surface-2` + 3px left rule oxblood + three actions · Fault = `--ink-2` neutral, dashed 1px border, retry, no refusal-family colour · Not yet measured = hatched fill 6% opacity, present in every estate view at full weight. *Canon 5 §6.*
- **C5-R-023 · Fault shares no colour/border/component with Refused.** Person must tell at a glance whether system said no or system broke. *Canon 5 §6.*
- **C5-R-024 · Typography families.** `display` Georgia serif (headings, artifact titles) · `body` system-ui (all interface text) · `mono` ui-monospace (identifiers, digests, receipts, contract views). *Canon 5 §7.*
- **C5-R-025 · Type sizes.** h1 24px/700 (surface title, one per surface) · h2 18px/600 (section) · body 13px/400 · body-lg 14px/400 (prose, refusals, plain-language rule statements) · label 11px/600 · micro 10px/500 · mono 12px/400. *Canon 5 §7.*
- **C5-R-026 · Identifiers render in mono.** A trace identity in proportional face invites transcription error. *Canon 5 §7.*
- **C5-R-027 · Layout widths.** Reading measure 720px (prose, refusals, rules) · content width 1280px (dense tables) · panel width 380px (evidence panels, drawers). Prose never exceeds 720px regardless of viewport = layout defect. *Canon 5 §8.*
- **C5-R-028 · Four layout structures.** Register (1fr 300px) · Ledger (full-width tabular) · Wizard (720px centred, one decision at a time) · Board (repeat(3,1fr) equal-weight cards). *Canon 5 §8.*
- **C5-R-029 · Figure component is the only permitted way to render a number describing estate/artefact/measurement.** Renderings: `measured 1,284` · `estimated ≈ 1,300 (est.)` · `unmeasured — not measured`. Never bare text; measurement class is part of the figure, not a footnote. *Canon 5 §9.1.*
- **C5-R-030 · Refusal card has binding copy.** Title "Not to the standard you asked for." · three actions "Accept as recorded statement · Narrow the objective · Lower the standard" · footer "A refusal is the system keeping its promise." — verbatim wherever this card renders; never paraphrased/shortened/restyled. *Canon 5 §9.2.*
- **C5-R-031 · Agent-assumed chip specification.** "Agent assumed — confirm or change" · amber · 11px label weight · attached to any agent-filled field · survives to commit review unchanged — value agent-assumed at draft is never quietly reclassified as user-supplied by confirming the screen. *Canon 5 §9.3.*
- **C5-R-032 · Four designed states.** Not yet measured (hatched fill --ink-3, present at true visual weight — never smaller/omitted) · Coverage gap (named specifically + offer to file) · Refused (the refusal card) · Dormant capability (visible + named + what would activate it — never hidden). *Canon 5 §9.4.*

## Part III · The Surface Taxonomy

- **C5-R-033 · Exactly five consoles, capability-defined not by named person.** Extraction · Compliance · Integration · Administration · Watch. Console is capability set, not job title. *Canon 5 §10.*
- **C5-R-034 · Watch Console owned by the Watch authority.** Specified in Part VII-A + Document 8. *Canon 5 §10.*
- **C5-R-035 · One sidebar across whole product with role-based landings.** Each console opens to screen its primary user needs first, never a generic dashboard. *Canon 5 §11.*
- **C5-R-036 · No figure appears anywhere in the product without a path to where it came from.** Shapes more of interface than any aesthetic; forces every tile/table cell/chart to carry a receipt link; makes proof walk the most-used interaction, not an audit feature. *Canon 5 §11.*
- **C5-R-037 · Every screen carries breadcrumb + census-in-force chip + contextual access to reference application.** *Canon 5 §11.*
- **C5-R-038 · Registry Dashboard — the warehouse floor.** Estate manager's home; topline highlights each with note + measurement link · distribution view + insight card · estate table (source, data type, volume, languages, rights, condition, last measured, share extracted); any row opens to profile · standing opportunity briefs + coverage-to-objective bars + extraction activity. *Canon 5 §12.1.*
- **C5-R-039 · Trust Center — the warehouse of rules.** Compliance owner's home; specified fully in Part V; two dashboards together = what "day zero" means. *Canon 5 §12.2.*

## Part IV · The Extraction Console

- **C5-R-040 · Extraction Home layout.** Header (product + role + Commission-objective action) · status line ("Running normally. One item needs you.") · at most one attention card per exceeded threshold with Review action · running list (objective name, entry type + stage, budget consumed) · capacity strip. *Canon 5 §13.*
- **C5-R-041 · No dashboards or charts by default.** Exceptions only on threshold crossings; everything else stays quiet. *Canon 5 §13.*
- **C5-R-042 · Commission wizard = chat pane + objective draft rail.** Chat: operator states intent; agent asks mandatory fields, never proposes on them; estate-check chip renders inline before any feasibility-dependent question. Rail: three dimensions (entry/reach/output) + envelope; three field states (filled with check · open + muted · agent-assumed with amber chip). Envelope line lists done-condition + budget + lawful basis until supplied. Sample action available once reach drafted. *Canon 5 §14.*
- **C5-R-043 · Mandatory fields asked, never pre-filled.** Reach + four output fields + done-condition + budget + lawful basis never agent-assumed. Preference fields may carry agent recommendations. Every turn grounded in a real estate read; no fabricated availability, ever. *Canon 5 §14.*
- **C5-R-044 · Commit review structure.** "You supplied" rows · "Agent assumed" rows (amber chip + change link) · feasibility verdict success card ("Floor feasible — {n}% of in-scope estate meets your standard") · grounding marker (sample-grounded or estimate-grounded) · envelope line · Freeze objective action. Frozen is immutable — changed intent = new objective. *Canon 5 §15.*
- **C5-R-045 · Sampling is a first-class narrow-reach objective.** Grounds the full commit; exists because full extraction has resource commitment and feasibility honestly returns unknown on un-censused reach — sample converts unknown into evidence. *Canon 5 §16.*
- **C5-R-046 · Sample cost draws objective's budget + shown doing so.** Sample result is evidence, not a promise. *Canon 5 §16.*
- **C5-R-047 · Registry Administration screen.** View census state by estate region; trigger or schedule census passes; un-censused regions marked honestly as unknown, never as empty. *Canon 5 §17.*
- **C5-R-048 · Quality observation inside running status.** Mining-stage visibility; per-objective yield + class distribution as extraction proceeds; threshold-crossing attention cards. *Canon 5 §18.*
- **C5-R-049 · Opportunity Briefs = recommendation surface, consumer of Registry census, advisory not governed.** *Canon 5 §19.*
- **C5-R-050 · Briefs home card is quiet.** One line — estate analysis current-as-of date + briefs count + new-since-last-census count — one action Explore; threshold-attention rules do not apply. *Canon 5 §19.1.*
- **C5-R-051 · Brief content structure.** Three sections: What exists (census slice) · What it could become (2-3 product shapes, each with real-world precedent + one line on how monetised) · What is missing (rights + consent basis + licensing preconditions honest gaps). One action: Shape as objective, pre-fills wizard with brief's reach. *Canon 5 §19.3.*
- **C5-R-052 · Briefs rules.** Every grounding-line number is a live registry read verbatim; generation layer selects facts, never produces facts of its own; no render path drops advisory marker; briefs sit outside trust-receipt + trace system entirely; regenerate on census change; superseded brief marked stale, never deleted. *Canon 5 §19.4.*

## Part V · The Compliance Console

- **C5-R-053 · Trust Center Home structure.** Lookup (single field — look up any run/claim/acquisition by trace) · Attention (problems stated honestly with binding pattern) · three always-present cards (runs with lawful basis · refusals this month with link · retention windows past due). *Canon 5 §20.*
- **C5-R-054 · Adversarial to comfort.** Overruns/unset rules/refusals surfaced as problems + evidence governance bites — never behind all-green summary. Same record every user's audit view reaches; read-only; nothing reconstructed for display. *Canon 5 §20.*
- **C5-R-055 · Prove-One-Run structure.** Banner with lawfulness (lawful-basis ref + commissioner + statement that objective was frozen and immutable) · 5 record rows each resolving to record beneath. Read-only, IS the record itself; export for regulator on request. *Canon 5 §21.*
- **C5-R-056 · Retention-unset banner.** Rendered before anything else: "No deletion rule is set. The system holds everything indefinitely and append-only until you set a retention window. This is a decision only you can make — the system won't guess a duration." *Canon 5 §22.*
- **C5-R-057 · Held classes render separately addressable.** Ledger rows / wizard transcripts / delivered artefacts each carry their own row so compliance owner scopes one window across all or splits per class. *Canon 5 §22.*
- **C5-R-058 · Setting retention window here becomes a governed rule.** Versioned, dated, recorded like every other control change. *Canon 5 §22.*
- **C5-R-059 · Compliance Console owns writes to compliance rule classes.** Retention windows · disclosure thresholds (group size, distinct-value count, privacy budget) · lawful-basis registry · source-standing table · entitlement rules. *Canon 5 §23.*
- **C5-R-060 · Rendering reuses plain-language rule pattern.** Rule as sentence + current behaviour + what changes + record with date; re-used not redesigned; entitlement rule is written/changed/proven exactly the same way, not a special case. *Canon 5 §23.*

## Part VI · The Integration Console

- **C5-R-061 · Register-an-Application fields.** Application name · class choice (internal or external) · path choice with one-line grants; key grants panel = plain-terms statement of what key permits (class, path, floor, scope) + statement all enforced server-side on every call; optional webhook (event + status only, never content); sandbox toggle = fixture-estate key mode; Issue-key action; issuance + revocation emit ledger rows. *Canon 5 §24.*
- **C5-R-062 · First Call — Contract structure.** Request block (endpoint + ask + standard + scope) · side-by-side response panels (Answered: outcome + trace identity + claim + defensibility inline + provenance; Refused: identical envelope shape distinguished only by body discriminator with what-was-asked + supported class + what would raise it) · async variant note (fresh-extraction ask returns accepted ack with objective identity + delivery estimate; status in Administer). *Canon 5 §25.*
- **C5-R-063 · Sample payload marked as illustration + fixture-schema-gated.** Parses through platform's own frozen contracts; unmarked sample = hidden mock, prohibited. *Canon 5 §25.*
- **C5-R-064 · Claim never separable from class in any response shape.** Infrastructure faults return server error, never rendered as refusals. *Canon 5 §25.*
- **C5-R-065 · Administer layout.** At most one attention card (application name + refusal rate + plain-language cause + Review) · applications list (name + class badge + path + key + calls + refusal rate); extract-path rows show acquisitions + rights state; long-running objectives show lifecycle state. *Canon 5 §26.*
- **C5-R-066 · Refusal health reads as a signal, not error log.** Rising refusal rate says something real about integration's objective (scope too wide, floor too high for estate). *Canon 5 §26.*
- **C5-R-067 · Key scope enforced server-side on every call.** *Canon 5 §26.*
- **C5-R-068 · Two roles, one console, identical screens, different scope.** Enforcement server-side, never view-layer filtering alone. *Canon 5 §27.*
- **C5-R-069 · External-scope denials are access-control class.** Carry reason + detail; never carry outcome key; never render through refusal card — denial and refusal are different things and must never look the same. *Canon 5 §27.*
- **C5-R-070 · External engineer vs buyer distinction.** External engineer = integrating partner's engineer wiring partner system to governed boundary — platform-operator action by outside party, legitimately seeing scoped console view. Buyer = purely end-user of commercial application, sees no console at all. *Canon 5 §27.*
- **C5-R-071 · Governed boundary contract summary.** Application registration + key issuance + scope bounds + usage & refusal-health monitoring. *Canon 5 §28.*
- **C5-R-072 · Boundary enforces for every caller with no first-party exception.** Inner gate on live query or full outer gate on governed extract · server-side key scope on every call · four response classes. Bypass appearance = defect, never a tier of service. *Canon 5 §28.*
- **C5-R-073 · No price/quote/offer/catalogue/order/buyer-account exists on Integration Console or boundary.** Commercial-application concerns entirely; platform charges nothing + knows no buyer. *Canon 5 §28.*
- **C5-R-074 · Administration Console owns internal cost + capacity.** Fleet apportionment · cost-per-unit telemetry. Owns no commercial price; commercial price never appears on a platform surface. *Canon 5 §28.*

## Part VII · The Administration Console

- **C5-R-075 · Administration Home.** Pending banner (governance seams awaiting values + items awaiting counter-signature; binding pattern "Two rules are waiting on your decision before they can take effect." + Review; never placeholder count) · Prompt "What do you want to do?" · Six action buttons: Assign a role · Change a rule · Manage keys and access · Update the taxonomy · Set pricing · Apportion capacity · Footer "See everything I've changed — every action is recorded." *Canon 5 §29.*
- **C5-R-076 · Buttons + sentences only on this surface.** No dashboards, no version strings, no configuration syntax. *Canon 5 §29.*
- **C5-R-077 · Change-a-Rule structure.** The rule (one sentence in everyday language + short paragraph of current behaviour + plain options with natural labels) · What changes (1-2 natural-language sentences including — where true — that nothing running now changes + that it can be switched back) · natural-language Commit button; committable rule writes new versioned record server-side, recorded + reversible; rule not yet committable through surface states so honestly — surface never a bypass. *Canon 5 §30.*
- **C5-R-078 · What-I've-Changed screen.** Confirmation (plain line for latest change) · Rows (recent actions in words + who + when; counter-signed changes show both identities); full diff opens on demand behind collapsed link, never primary display. Trail is append-only + readable by compliance surface. *Canon 5 §31.*
- **C5-R-079 · Administration Console owns operational rule classes.** Pricing models + tier locks · fleet apportionment · classification taxonomy. Compliance rule classes render here read-only + marker "owned by Compliance". Two consoles, one rulebook, no ambiguity. *Canon 5 §32.*
- **C5-R-080 · Roles-and-Rights.** Changes plain-language + consequence-visible + ledgered — change-a-rule pattern applied identically to role grants. *Canon 5 §33.*
- **C5-R-081 · Counter-sign duties symmetry.** Administration-side operational change loosening protection requires Compliance counter-sign; Compliance-initiated loosening requires Administration counter-sign; check binds in both directions; no hierarchy between consoles; neither loosens protection alone. *Canon 5 §34.*
- **C5-R-082 · Signature attestation form.** "Signed by {initiator} · counter-signed by {checker} · recorded with both identities." *Canon 5 §34.*
- **C5-R-083 · Dual-control honesty note.** While one person holds both roles (small deployment), dual control is ceremony not substance; seam is built regardless because it is cheap now and expensive to retrofit later. *Canon 5 §34.*

## Part VII-A · The Watch Console

- **C5-R-084 · Watch Console = security authority's one surface.** Watch officer (write); compliance owner read-only. Peer to Trust Center, never a tab inside it; two authorities' consoles share the record and share nothing else; access under own authority's identity per Doc 9 matrix. *Canon 5 §34-A.*
- **C5-R-085 · No build state; screen speaks organisation's language.** The watch · the record · under watch · decisions. Watch's internal engine and arm names never appear here. *Canon 5 §34-A.*
- **C5-R-086 · Four panels.** State (two live latency figures against bounds + population by class + trust standing + two spend gauges [autonomous-action budget + friction budget] + health of watch + last drill + anything currently held; band built never to render all-clear — all-clear on real estate = rendering defect) · Record (verdict stream in three lanes: noted-no-action [restraint record] · noted-and-acted [each carrying policy row + live expiry countdown; actions released clean visible as false-positive record] · held [certainty events]; drills appear in same lanes marked for what they are; row expands to full evidence walk: signal → verdict with replay → policy row → action → outcome → witness; row that cannot complete walk renders broken not dressed) · Under-watch (accumulation view — actors whose noted events individually dismissible + collectively a shape; each curve's signal mix + time at elevation; promote suspect to misdirection; observe live misdirection sessions as occupancy + findings never construction; review the marked; file re-declaration request; de-marking is dual-control routing to Decisions) · Decisions (reserved for people, ranked by blast radius, each with walk pre-opened: containment-to-severance promotions · expiry extensions · de-mark requests with both signatures · authorities' disagreements side by side · ceremony watch cancellable from here; item aging past class bound escalates itself; class repeatedly reaching = policy defect to redefine). *Canon 5 §34-B.*
- **C5-R-087 · What Watch Console never renders.** No thresholds/trip points/jitter bands render, ever · no canary or mark placement detail (record shows tripwire was touched, never where others sit) · no behavioural profile (trust standing yes, shape of person's habits never) · no misdirection construction · console itself watched (session receipted + viewers enveloped like any actor + anomalies land in its own record). *Canon 5 §34-C.*
- **C5-R-088 · Watch Console posture = Trust Center's own, inherited whole.** Read-only for assurance, adversarial to comfort. A Watch Console that only shows green is marketing, not security. *Canon 5 §34-C.*

## Part VIII · The Consequence-Class Checker

- **C5-R-089 · Consequence attached to rule class, not to role.** Preserves compliance independence; check binds symmetrically not downhill from senior console. *Canon 5 §35.*
- **C5-R-090 · Direction of signature follows direction of loosening, never org chart.** *Canon 5 §35.*
- **C5-R-091 · Pending items render on both consoles' banners simultaneously.** Counter-signing console sees full plain-language consequence statement before signing — never a bare approval button with substance hidden. *Canon 5 §35.*
- **C5-R-092 · Single-person-dual-role honesty.** Dual control is ceremony not substance while true; seam built regardless. *Canon 5 §35.*

## Part IX · The Reference Application

- **C5-R-093 · Reference application is not platform surface.** Application specified because it demonstrates platform's contract for future applications; Integration-Console-issued key on identical terms to any third party including Syni. Nothing privileged. *Canon 5 §36.*
- **C5-R-094 · Ask surface: one plain question centred.** "What do you need to know?" · answer reader can act on + defend. Output preset: composed conclusion, for a person, synthesized whole, at their floor. No output picker — choosing an output form is a commissioning act belonging to Extraction Console. *Canon 5 §37.*
- **C5-R-095 · Class in headline position wherever a claim is.** Plain language; never a buried score. *Canon 5 §37.*
- **C5-R-096 · Three lenses = progressive disclosure over one object.** Answer (finding + per-claim marking + honesty strip) · Reasoning (evidence strip: which units + how composed) · Raw trail (full trace = same record compliance audit reaches, resolvable by anyone holding trace identity). All three lenses read one object — executive's summary and auditor's trail structurally incapable of disagreeing. *Canon 5 §37.1.*
- **C5-R-097 · Three refusal classes visually distinct.** Not-extracted-yet · evidence-cannot-support · something-broke; the third shares nothing with the first two — not components, not colour, not layout. Reader tells without reading a word whether platform declined or platform failed. *Canon 5 §37.2.*
- **C5-R-098 · Export = same artefact with class markings intact.** Not a second product; not a re-shaping. Different form/grain = new objective; rule prevents analytics drift through export. *Canon 5 §37.3.*
- **C5-R-099 · Machine form for integrating applications.** Identical object as structured envelope · all three refusal shapes as first-class response types, not error codes an application interprets — named shapes it is expected to render. *Canon 5 §37.4.*
- **C5-R-100 · Application must handle a decline at build time.** Prevents wrapper swallowing refusal + substituting plausible generated answer. *Canon 5 §37.4.*
- **C5-R-101 · Any commercial application reaches platform output only through governed boundary.** Scoped external key + full outer gate + disclosure-budget debit — identical to any third-party caller in every respect. *Canon 5 §38.*
- **C5-R-102 · Sample shown to prospective buyer is an egress.** Passes full outer gate + debits cumulative-disclosure budget or it is exactly the assembly attack the disclosure ledger exists to catch. No disclosure-free sample path under any commercial pressure. *Canon 5 §38.*

## Part X · The Environment

- **C5-R-103 · Environment is application layer, not platform layer.** Carries organisation's own name; every surface inside reaches platform through identical Integration-Console boundary any third party uses; no platform decision optimises this layer directly. *Canon 5 §39.*
- **C5-R-104 · Design agenda: sourced vs designed.** Consoles + reference application = sourced (ratified specification); environment pillars = original design; a builder must not mistake confidence of prose for confidence of ratified spec. *Canon 5 §39.*
- **C5-R-105 · Five pillars + Control band.** Pillars: Lead (ThinkLab, Monitor, Pulse, News) · Work (Chat, Analyze, Documents) · Build (Extract, Train, Studio) · 3rd Party (org-built + vendor-integrated) · Learn (capability-building programmes). Control band spans all five: Connect · Estate Map · Rulebook · Access · Watch — governs every pillar including 3rd party. *Canon 5 §40.*
- **C5-R-106 · Control band is customer-facing presentation of the four real consoles.** Estate Map ← Extraction Console Registry Dashboard + Registry Administration; Rulebook ← Compliance rulebook + Administration operational rule classes; Connect ← Integration Console (registration + administration) [model + compute connection management is new]; Access ← Administration Console roles/rights/keys + counter-sign duties; Watch ← Doc 8 + Part VII-A. *Canon 5 §41.*
- **C5-R-107 · Sourced vs designed per application (§42).** Sourced: Extract · Chat · 3rd Party. Designed: Train · Studio · Analyze · Documents · ThinkLab · Monitor · Pulse · News · Learn. Sourced item = specification; designed item = brief. *Canon 5 §42.*
- **C5-R-108 · Designed surface still bound by every rule in Part I.** Eight global rules + four response classes + visual system apply identically; only field-level/screen-level spec is absent for designed surface; design law never optional. *Canon 5 §42.*
- **C5-R-109 · News binding rule.** Single Lead surface whose content originates outside perimeter; every item labelled as external at the item, always — Doc 3's boundary-governor provenance discipline applied here. *Canon 5 §42.*
- **C5-R-110 · Doc 5 does two visibly separate jobs.** Transcribes what is ratified + proposes what ratified platform makes possible; future ratification of designed surface supersedes this doc's proposal for it at the item without disturbing anything else. *Canon 5 §43.*

---

**Total extracted requirements for Canon 5:** 110.
