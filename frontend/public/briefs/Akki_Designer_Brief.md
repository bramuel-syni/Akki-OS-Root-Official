# Akki — Product Experience Brief

**Audience:** senior product designer / UX lead  
**Purpose:** define the complete user experience Akki must deliver, including important capabilities not yet surfaced. This is a product and behaviour brief, not a wireframe, navigation map or instruction to copy a particular HTML layout.  
**Version:** 28 September 2026

## 1. The product we are designing

Akki helps an organisation turn the information it already owns into useful, defensible answers, decisions and completed work. People should be able to connect their estate in place, understand what can be relied on, ask for an outcome, collaborate on it, and receive a result whose evidence and permitted use are clear.

The experience should feel as fluent and capable as a leading AI application, while giving people something ordinary assistants often lack: continuity, trustworthy provenance, meaningful control, and accountability for what actually happened.

The promise is **not** “a dashboard for an AI infrastructure stack.” It is:

> “Tell Akki what you need to achieve. It understands the authorised material and context, does the permitted work, explains what needs your decision, and carries the result through to delivery without making you manage its machinery.”

### Product principles

1. **Outcome first.** Lead with the task, answer, decision or risk—not the engine performing it.
2. **No migration prerequisite.** Connect the organisation’s sources where they are. A read-only connection is not permission to export everything.
3. **Capable, not timid.** Preserve the full task and ambition. When something prevents progress, explain the particular limit and the next permissible action instead of shrinking the feature.
4. **Trust at the point of use.** Make it easy to inspect the support for a claim or the scope of an action. Do not surround ordinary work with technical evidence dumps.
5. **Continuity without surprise.** Changing tools must not silently change the objective, source scope, audience, task state or model capability.
6. **Human authority is explicit.** Assistance, a recommendation, a draft and an executed action are different states.
7. **Fast, truthful feedback.** Acknowledge immediately; show real progress when available. Never imply execution, completion, accuracy or certainty that has not been established.
8. **Quality is non-negotiable.** Performance improvements must not silently substitute a weaker model, discard important context or lower acceptance standards.

## 2. People and their jobs

| Person | Job they come to do | What success feels like |
|---|---|---|
| Individual knowledge worker | Answer a question, create an artefact, finish an assigned outcome | I can move from question to useful result without repeating myself; I know what is supported and what still needs my judgement. |
| Team lead / accountable owner | Assign work, coordinate contributors, remove blockers, demonstrate progress | I can see who owns the next action, what is at risk, and what evidence supports completion. |
| Executive / board participant | Understand performance, assess exceptions, make and revisit decisions | I receive a concise, current account and can inspect the material behind it without starting a research project. |
| Estate steward | Connect information, keep coverage current, manage source changes | I can tell what is connected, what has been measured, and what is still missing without exposing credentials or moving the estate. |
| Approver / compliance reviewer | Decide whether a particular use, cost, disclosure or exception is permitted | I see exactly what I am deciding, its impact and its limits; my decision cannot quietly authorise something broader. |
| Operational responder | Investigate a meaningful change or risk and take an authorised action | I receive relevant, attributable cases, not a stream of technical noise; I can act and verify the outcome. |

One person may hold several responsibilities. Role changes must not silently broaden access or mix organisations. The experience must work for a first-time user and for a returning expert without forcing everyone through the same explanatory steps.

## 3. Common experience contract

Every significant work item should answer, in the appropriate level of detail:

- What am I trying to achieve, and what will count as done?
- Who is accountable, and who may view, contribute, approve or receive it?
- Which sources and relevant dates does it depend on?
- What has actually happened, and when was that state last confirmed?
- What can I safely do next? Who owns any blocking decision?
- What will this action change, consume, disclose or commit?
- Can I pause, cancel, revise, resume or request a review—and with what consequences?

Show this information progressively. Most users need a readable statement and a clear action; specialist users may need the supporting history. Do not make cryptographic hashes, worker identifiers or schema versions the primary language.

### Distinguish these states

**Draft / saved / not saved; connected / connection not verified; discovered / measured / unmeasured; awaiting decision / denied / expired; accepted / queued / running / interrupted; partial result / ready for review / accepted; delivered / delivery unconfirmed; current / stale / withdrawn / superseded.**

These are semantic requirements, not a mandate for one enormous global status menu. Use the states relevant to each journey. Never turn “unavailable” into an empty list, zero cost, a clean health check or successful completion.

## 4. Required experience capabilities

Each capability below includes the user outcome, representative stories, the normal journey, and the conditions that design must cover. These are requirements to design for—not claims that every backend is already operational.

### E01 — Connect an estate safely, in place

**Outcome:** an authorised steward establishes a read-only link which Akki can use for census and, later, for separately scoped extraction.

**Stories**
- As a steward, I can name a source, identify its owner and organisation, supply the permitted connection details, and understand precisely what access I am granting.
- As an owner, I can confirm that connecting a source does not migrate it, modify it, train on it or permit unrestricted disclosure.
- As an operator, I can diagnose a failed connection without seeing secrets or being told “connected” merely because a form saved.

**Journey:** identify source and owner → choose the supported source type → provide or reference protected credentials → confirm the read-only scope and network boundary → validate through Akki’s authorised ingestion capability → review the actual connection result → continue to census when eligible.

**Experience requirements**
- Support a database, file/object store or another admitted source without pretending every connector is already available.
- Distinguish details saved, validation in progress, reachable, authenticated and usable for the permitted operation. Disclose the failing step safely.
- Display secrets as protected references once captured; do not return passwords or internal access tokens to the user.
- Offer update credentials, retry validation, pause use and disconnect only to authorised people. Show the impact before disconnecting.
- Do not replace a missing connector or unreachable worker with a file-upload workaround that changes the data boundary.
- A failure must state what is known about access or transfer. Say “not verified” when evidence cannot establish that nothing was read; do not promise more than the record proves.

**Acceptance:** a real connection outcome is attributable to the named source and scope; no source writes occur; later extraction still requires its own purpose and authority.

### E02 — Understand what the estate actually contains

**Outcome:** people can assess coverage, freshness and suitability before relying on the estate.

**Stories**
- As a steward, I can see which sources have been discovered, measured, partly measured or not measured.
- As an analyst, I can understand whether a figure is a complete count, a sample, an estimate permitted by the measure, or unknown.
- As a decision-maker, I can tell whether relevant information is stale or disputed before commissioning work.

**Journey:** review census readiness → start or observe the authorised census → see current coverage and exceptions → inspect a source or measurement → address a gap or request an allowed refresh → return to the intended work.

**Experience requirements**
- Census describes the estate independently of a particular objective; it is not a disguised extraction request or a per-question index rebuild.
- Show the population, measurement date, method and unmeasured portion behind important figures.
- Surface useful dimensions such as volume, media/language, age, personal-data presence, use restrictions and quality when genuinely measured.
- Full-estate coverage is an actual requirement. A bounded attempt or unsupported region must remain visibly incomplete until resolved.
- Source change, permission change and failed refresh must not silently leave an old result looking current.
- Support discovery of relevant sources without revealing resources the person is not allowed to know about.

**Acceptance:** two objectives read the same current estate measure; unknown remains unknown; no favourable coverage or cleanliness claim is inferred from absence of data.

### E03 — Turn intent into an agreed, executable outcome

**Outcome:** a natural request becomes a clear, bounded commission without requiring the user to understand orchestration.

**Stories**
- As a requester, I can describe the result I want in ordinary language and have only material ambiguities clarified.
- As an accountable owner, I can review the intended output, audience, permitted sources, due date, quality/evidence bar and resource limits before committing.
- As an approver, I can decide on a specific version of a request, rather than a moving target.

**Journey:** express intent → clarify missing essentials → review feasibility and material gaps → inspect scope, expected output and disclosed cost/limits → confirm or seek necessary decisions → receive an accepted commission or a specific explanation of what prevents it.

**Experience requirements**
- Reuse known authorised context. Do not ask repeatedly for information the person has already supplied.
- Preserve an editable draft before commitment. Saving a draft and commissioning work are separate actions with visible confirmation.
- Changes after commitment create a clearly identified revision and show whether renewed approval is required.
- State estimates and uncertainty honestly. Missing prices or permission are not zero cost or implicit approval.
- Keep the full intended outcome visible even when only part is currently feasible. Offer explicit alternatives without silently narrowing the commission.

**Acceptance:** the requester can tell exactly what was agreed, what remains undecided and whether work has started; retries do not create duplicate commissions.

### E04 — Carry work across capabilities without losing its meaning

**Outcome:** a person can move from conversation to analysis, document production or managed work without restarting or re-explaining.

**Stories**
- As a user, I can continue the same objective in another capability with its authorised evidence, constraints and relevant history intact.
- As a collaborator, I can tell which version I am continuing and what was intentionally excluded from the handoff.

**Journey:** work on an objective → choose the next useful capability → review the material consequences of the transition → continue with the same work identity and appropriate context → return without losing place.

**Experience requirements**
- Preserve the objective, source references, chosen output, evidence limitations and permissions—not just a copied text prompt.
- Explicitly disclose meaningful context loss, stale dependencies or scope changes before they affect the result.
- Never silently broaden the audience, switch model capability, enable external sharing or restart billable work during a handoff.
- Back, refresh, deep links and interruption must restore a coherent current state, not create a second job.
- A handoff can be refused or require approval; keep the original work accessible with a next action.

**Acceptance:** the same work can be traced through its transitions; unauthorised or withdrawn context never reappears merely because the user changed capabilities.

### E05 — Answers and analysis with inspectable support

**Outcome:** an answer is useful immediately, and its basis is available when it matters.

**Stories**
- As a user, I can distinguish what the evidence establishes, what a source reports, what is inferred and what remains unresolved.
- As an analyst, I can inspect a claim’s permitted supporting material and see conflicting or outdated evidence.
- As a user, I can correct the request, challenge an answer or ask for better support without losing the conversation.

**Journey:** ask within an authorised work context → receive a substantive answer or specific limitation → inspect a material claim → refine, compare alternatives or request additional authorised evidence → use the result in the next task.

**Experience requirements**
- Keep the answer readable; do not force users to decode internal class names or an unexplained confidence percentage.
- Make citations resolve to the relevant section, row or time span when permitted—not merely a document title.
- State meaningful omissions and assumptions. Do not imply that a partial search covered the whole estate.
- A refusal should explain the permitted next step without disclosing the protected information causing it.
- Streaming, when available, must not present provisional content as an accepted result or expose content awaiting permission.
- A correction should show what changed and whether prior derived results need reconsideration.

**Acceptance:** important claims can be inspected; missing, contradictory, stale or withdrawn support produces the required limitation instead of a confident invention.

### E06 — Useful documents, data and media—not just chat text

**Outcome:** people can work with actual artefacts and the relevant parts of multimodal sources.

**Stories**
- As an author, I can review, revise and compare a deliverable while retaining its sources and acceptance status.
- As a researcher, I can move from an audio-derived finding to its precise permitted time span, or from a document finding to its relevant page/region.
- As a recipient, I can tell which artefact version is current and which uses are permitted.

**Journey:** choose or generate the required artefact → inspect content and supporting material → revise or annotate → compare material changes → review and accept → deliver an authorised version.

**Experience requirements**
- Show meaningful file/version identity, freshness, evidence limitations and review state.
- Make search, inspection and copy/export availability consistent with the person’s rights.
- Unsupported media, failed perception and partial extraction must have explicit states; a blank preview is not “no content”.
- Distinguish editing a draft from altering the authoritative source. Do not imply that Akki rewrites a connected estate.
- Preserve accessibility in document/audio experiences, including text alternatives where available and keyboard-operable media controls.

**Acceptance:** the delivered version is identifiable, its supporting positions are navigable where permitted, and no unsupported format is silently treated as processed.

### E07 — Work that persists through ownership, interruption and completion

**Outcome:** a task is a durable commitment with a clear owner, current state and evidence of completion.

**Stories**
- As an owner, I can create and save a task, assign contributors, set an appropriate date and define what counts as done.
- As a contributor, I can add permitted evidence or raise a blocker without taking authority I do not hold.
- As a returning user, I can resume work after leaving or losing connectivity without losing accepted actions.

**Journey:** create/save draft → agree responsibility and outcome → commission eligible work → observe substantive updates → contribute or resolve a decision → submit a result for review → accept, request changes or close with a recorded reason.

**Experience requirements**
- Dates, ownership, saved state and completion evidence must be real, not decorative prototype values.
- Provide pause/cancel/retry/resume only when their semantics are supported. Explain effects already incurred and which actions are safe to repeat.
- Distinguish “stopped accepting new work” from “all running activity stopped”. An uncertain outcome needs reconciliation, not a blind retry.
- Preserve the original request and version history; do not silently edit an approved objective.
- A completed checklist, an executed process and an accepted business result are separate concepts.
- Show activity that changes decisions, not every machine event.

**Acceptance:** work survives refresh and re-entry; retry does not duplicate effects or charges; only the authorised acceptance evidence can establish completion.

### E08 — Coordinate the team and connect work to goals

**Outcome:** people understand how individual commitments contribute to organisational outcomes without fabricated productivity scores.

**Stories**
- As a lead, I can connect a work item to a genuine goal and identify the accountable owner and contributors.
- As a contributor, I can see my next obligations, dependencies and outstanding requests without seeing another person’s restricted work.
- As an executive, I can distinguish actual progress, overdue commitments, missing evidence and a metric that has not been measured.

**Journey:** inspect a goal → identify contributing work and owners → resolve a dependency or assign an authorised contribution → update evidence → review the effect on the goal → revisit the outcome at its actual reporting date.

**Experience requirements**
- Goal progress has a stated measurement basis. Do not average task completion into business success unless that is the adopted goal measure.
- Show dependency and blocker ownership. Avoid ambiguous “waiting” states with no responsible person or next step.
- Membership, delegation, reassignment and contribution rights must be explicit; a team display is not a grant of access.
- Label unmeasured execution scores and explain their calculation when supplied. Do not generate opaque employee rankings.
- Preserve goal history when ownership, measure or target changes.

**Acceptance:** a goal-to-task-to-evidence chain is inspectable, access remains scoped, and a change in the underlying evidence changes the displayed claim appropriately.

### E09 — Board and executive decision work

**Outcome:** leaders can understand the current position, examine supporting material and record decisions with follow-through.

**Stories**
- As a board participant, I can inspect a pack, ask a question and distinguish a draft answer from an authorised response.
- As a decision owner, I can connect a decision to the information considered and assign follow-up work.
- As a returning participant, I can identify what changed since the previous review.

**Journey:** review relevant signals and performance → inspect the permitted pack/version → ask or answer a question → consider alternatives and unresolved issues → record the authorised decision → follow resulting actions and later outcomes.

**Experience requirements**
- “Board” means governed packs, questions, minutes, decisions and follow-through—not an unrelated project-card board.
- Preserve authorship, versions, visibility and decision status. An AI suggestion must never appear as a board resolution.
- Provide an explicit unread/updated distinction without pretending that reading equals agreement.
- Keep sensitive contributions scoped to their permitted audience; sharing a pack does not automatically share all referenced sources.
- Where signatures, quorum or an approval process apply, explain the human obligation and its completion state without exposing internal ceremony machinery.

**Acceptance:** the decision’s basis, accountable person and follow-up are available; a later change does not rewrite what was considered at the time.

### E10 — Resolve a blocker where it interrupts the work

**Outcome:** a person can move from a clear reason to a permissible resolution without diagnosing infrastructure.

**Stories**
- As a requester, I can understand why work is held and whether the next action belongs to me, an approver or an estate operator.
- As an approver, I can evaluate the specific intended use and its consequences with enough context to decide.
- As a requester, I can return to the same work when the decision is made, without resubmitting blindly.

**Journey:** encounter a meaningful hold → inspect its cause and consequences → provide missing information, request a decision or contact the accountable party → record the outcome → resume or revise the same work when permitted.

**Experience requirements**
- Use plain-language explanations supported by the actual record. Hide forbidden details without hiding every useful next step.
- Keep “request approval”, “approve”, “retry” and “resolve” distinct. Do not show actions a person cannot take as successful affordances.
- Show expiration and material changes that invalidate an approval. Never automatically treat an old decision as approval for broader scope.
- A rejection preserves the request, rationale and allowed alternatives; it is not erased to make the interface look clean.

**Acceptance:** the action resolves the identified condition or reports why it did not; work resumes only after the governing decision is effective.

### E11 — An actionable Watch, not a technical alert feed

**Outcome:** people can recognise and manage consequential changes in the organisation’s work, use of information and operating environment.

**Stories**
- As a responder, I can see a case’s significance, affected work, evidence and owner before acting.
- As a user affected by a restriction or classification, I can understand the permitted explanation and request review.
- As a leader, I can see whether an action changed the situation or merely acknowledged an alert.

**Journey:** receive a relevant signal → inspect the case and related changes → distinguish observed facts from a recommendation → assign, request approval or take an authorised action → verify its effect → close or keep under review with a reason.

**Experience requirements**
- Group genuinely related events while retaining their individual evidence and time sequence. Do not merge unrelated cases for visual simplicity.
- Distinguish new, acknowledged, assigned, awaiting decision, action pending, effective, inconclusive and closed where applicable.
- “Read” or “dismiss notification” must not close the case or remove an active protection.
- Make the impact on the person’s work apparent. Do not expose hidden investigation details or other tenants’ activity.
- Important or irreversible actions require an appropriate consequence preview and authorisation.
- Notification delivery itself has a state; do not claim a person was notified merely because a message was queued.
- A recommendation must not automatically change permissions or enforcement merely because a model proposed it.

**Acceptance:** every displayed intervention corresponds to a real permitted action and a verified or explicitly uncertain effect; appeal/review does not silently suspend protections.

### E12 — Deliver, share, withdraw and correct responsibly

**Outcome:** the right recipient receives the intended version, with clear rights and an honest delivery outcome.

**Stories**
- As a sender, I can review the audience, content, version, expiry and use restrictions before delivery.
- As a recipient, I can understand what I received and whether it remains valid for the intended use.
- As an owner, I can withdraw access or correct a result and see which dependent work is affected.

**Journey:** choose result and intended recipient/use → review permitted disclosure → obtain required decision → deliver → confirm the actual receipt/access state → handle expiry, correction or withdrawal and dependent notifications.

**Experience requirements**
- Distinguish a created link, an attempted transfer, a confirmed delivery and a recipient’s acknowledgement.
- If delivery is uncertain, offer reconciliation rather than repeating a potentially completed transfer.
- Before withdrawal, explain which future access is prevented and which past disclosures cannot be undone. Do not promise universal deletion of recipients’ copies.
- Show a superseding version and why the earlier one should not be relied on. Restricted content must not leak through old previews or citations.
- A derivative report, answer or memory that depends on withdrawn material must not appear currently valid without the required reassessment.

**Acceptance:** permissions are checked at use, not just at creation; the exact delivery version and uncertain outcomes remain traceable.

### E13 — Transparent cost and resource commitment

**Outcome:** people know what they have authorised, what has been consumed and what remains available.

**Stories**
- As a requester, I can see material estimated costs and limits before committing work.
- As an owner, I can distinguish a reservation from an actual charge, and an unknown price from a zero price.
- As a reviewer, I can reconcile usage against the request and agreed terms without seeing another person’s restricted detail.

**Journey:** inspect disclosed estimate and limits → agree the permitted commitment → observe measured consumption → review the final usage record → resolve a discrepancy or request a supported adjustment.

**Experience requirements**
- Use clear units, currency, period and scope. A technical token count alone may not explain business cost.
- Show paused/blocked work and the cost already incurred; cancellation does not imply an automatic refund.
- Keep billed usage, estimates, remaining allowance and any issued invoice distinct.
- Explain when a request cannot proceed because its price, terms or allocation is unresolved.
- A rate or period change must not silently reprice historic work.

**Acceptance:** the displayed charge can be reconciled to actual work and the applicable terms; unknown usage cannot become a free or paid claim by default.

### E14 — Pick up work with the right context

**Outcome:** returning to a task feels continuous without creating unrequested personal memory or overstating recall.

**Stories**
- As a user, I can reopen a work item and understand what was retained, what changed and what needs re-checking.
- As a reviewer, I can inspect a retained summary’s sources and limitations before relying on it.

**Journey:** leave work → return → recover the authorised working context → see important changes or exclusions → re-establish missing material when permitted → continue.

**Experience requirements**
- Preserve task-specific context with its rights and source version. Do not promise that everything from every conversation is remembered.
- A compressed summary must not turn an inference into an established fact or conceal dropped material that matters to the objective.
- If rights expired or a source was withdrawn, explain the impact without displaying the removed content.
- General personal memory, cross-user recall and silent training are not implied by this feature; they require separately adopted policy and user controls.

**Acceptance:** restored context is scoped and current; a retained summary never bypasses current access or evidence requirements.

## 5. Additional high-value experience opportunities

These extend the user value of existing capabilities. They are **proposals for prioritisation**, not newly completed features and not permission to change the product’s architecture.

### V01 — “What changed since I last reviewed this?”
Show material changes to a task, evidence set, answer or pack, with their effect on the prior conclusion. Distinguish changed content, changed permission and changed confidence in the evidence. Let the user revisit the previous version when still permitted.

**Value:** faster re-entry and more reliable decisions without rereading entire artefacts.

### V02 — A scoped, unified find-and-resume experience
Find permitted work, artefacts, decisions and source references using the user’s language. Results show type, owner, current state and why they are relevant. Search must respect existence confidentiality and avoid exposing restricted titles or counts. Opening a result returns the person to the right version and place.

**Value:** less repeated work and fewer navigation dead ends across a capable product.

### V03 — A concise human handover
Prepare a reviewable handover containing the objective, work completed, important evidence, unresolved issues and next accountable action. The recipient receives only what they are entitled to see. Acceptance of responsibility is explicit; generating a handover does not reassign work.

**Value:** collaboration with continuity rather than forwarding unstructured conversation history.

### V04 — Compare candidate results before committing
Let users compare materially different drafts or supported options against the same objective and acceptance criteria. Highlight changed claims, sources, costs and unresolved trade-offs—not just visual text differences. No invented winner or accuracy score.

**Value:** better decisions and practical control over capable AI without weakening it.

### V05 — Review preferences that reduce noise
Allow permitted notification/channel preferences, grouping and quiet handling of non-urgent updates. Important decisions and mandatory governance notices remain visible according to policy. Show whether preferences were saved and what cannot be muted.

**Value:** sustained attention and trust rather than alert fatigue. This does not introduce an unapproved recurring-job or notification service.

## 6. Quality, performance and accessibility requirements

### Perceived speed without deception
- Keep navigation and ordinary controls responsive while long-running work proceeds.
- Acknowledge an accepted interaction immediately; separate local acknowledgment from server acceptance.
- Preserve stable layout dimensions. Avoid shifting controls as counts, evidence or messages arrive.
- Do not block unrelated work on a slow source or model operation.
- Display last-confirmed state during refresh only when clearly identified; never show another identity’s cached state.
- Cancel or ignore superseded requests; late responses must not overwrite the user’s current selection.
- Design for very large permitted work lists with bounded previews and genuine access to the full result set.

### Performance acceptance
The product owner and engineering team must agree explicit targets for interaction feedback, first useful output, completion latency and failure recovery. Compare like-for-like workloads using the same model/version, context budget, evidence standard, access scope and load. Report latency distributions and answer quality/refusal behaviour together. A quicker answer obtained through lost evidence or a weaker model is not a successful optimisation.

### Craft and accessibility
- Express hierarchy through purposeful typography, disciplined spacing and consistent semantic emphasis—not extra chrome.
- Keep important actions reachable and labels legible across desktop, tablet and narrow mobile widths. No horizontal document-level overflow or clipped critical content.
- Provide visible keyboard focus, coherent focus order, meaningful accessible names and an exit/return path for every overlay.
- Do not communicate status only by colour. Support reduced motion and readable contrast; treat WCAG 2.2 AA as the design acceptance target, not a certification already achieved.
- Keep error messages actionable, respectful and proportionate. Preserve safe inputs after recoverable failures.
- Localise dates, time zones, units and language when supported; never lose the original meaning or source attribution through translation.
- Use consistent verbs: save, submit, request approval, approve, execute, accept, deliver and withdraw mean different things.

## 7. What must remain behind the experience

Do not create applications, primary navigation entries or routine user tasks for:

- Worker admission, executors, transport protocols, model routing internals or orchestration stages.
- Ledger append operations, signature checks, hash chains, receipt compilation or certificate schemas.
- Token-window packing, compaction mechanisms, lineage traversal or raw policy-rule identifiers.
- Registry writers, connectors as software modules, queues, retry handlers or metering counters.

Translate these into meaningful outcomes when relevant: **connection verified; source not yet measured; permission expired; context omitted; approval needed; result changed; delivery unconfirmed; cost limit reached**. Provide technical trace detail only to authorised specialists when it helps them perform a real support or audit job.

## 8. Representative end-to-end journeys to design and demonstrate

1. **First trustworthy use:** connect a read-only source → inspect census coverage → ask for a bounded outcome → review terms/scope → obtain necessary approval → receive and inspect an evidenced result.
2. **From question to shared delivery:** ask → investigate a supported claim → produce a document → create owned follow-up work → review → deliver to an authorised recipient → return later to its current version.
3. **A blocked commission:** save intent → encounter missing approval → approver considers the exact scope → record a decision → resume the same work, or retain the denied request with permitted alternatives.
4. **A changed or withdrawn source:** identify affected answers/tasks → understand which claims changed → prevent unauthorised future use → notify where supported → produce and review an eligible replacement.
5. **A Watch case:** recognise a consequential signal → inspect evidence and affected work → assign or approve an intervention → verify the result → retain closure/review history.
6. **An interrupted operation:** lose connectivity or cancel → reopen → distinguish accepted work from unsent changes → reconcile an uncertain outcome → continue without duplicate execution, disclosure or charging.
7. **A goal and leadership review:** inspect a goal → trace contributing tasks and actual evidence → review a pack/question → record the decision → follow its accountable next actions.

For each, show first use, return use, insufficient rights, empty vs unknown data, partial results, a delayed response, a recoverable failure and a genuinely unavailable capability. Do not use simulated success as the design’s only demonstration path.

## 9. Requested designer deliverables

1. An outcome-led experience concept describing the product’s mental model and user responsibilities.
2. Journey maps for the seven scenarios above, including roles, decisions, data required, exceptions and recovery.
3. Feature/state inventories covering the fourteen capabilities; identify which controls are shared and which behaviours need specialist treatment.
4. High-fidelity interaction designs showing working, loading, partial, blocked, denied, stale, failed and completed states with realistic but clearly fictitious content.
5. Interaction specifications for navigation continuity, selection, edits, confirmation, cancellation, focus, deep links, permissions and undo where genuinely supported.
6. A concise content language guide and accessible component/state specifications.
7. An implementation handoff identifying the exact data and actions each experience requires—without prescribing a new backend architecture.
8. A prioritised list of unresolved product decisions. Do not solve a policy gap by silently inventing authority, numeric thresholds, employee scoring or external disclosure rights.

## 10. Implementation boundary at handoff

There is working frontend/backend support for scoped work records and history, some governance and billing interfaces, recorded blocker navigation, and parts of the source-aligned interaction shell. Backend control/verification mechanisms also exist that are not yet complete native user journeys.

**Do not assume the entire backend is integrated or operational.** Native estate execution, durable task submission, live team/goal/board/Watch feeds, complete cross-capability handoffs and several recovery/disclosure effects remain incomplete. Some positive integration tests use **SYNTHETIC/MOCKED** providers. Current local task intake is an unsaved draft, not a commissioned task.

This brief deliberately describes the intended finished experience. Engineering must implement the established requirements and real service effects, then validate the complete journeys. Passing existing test cases or reproducing a prototype screen is not the definition of product completion.