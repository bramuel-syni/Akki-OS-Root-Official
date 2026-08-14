# Canon 7 — Integration Service and Quality Rulebook — Extracted Requirements

Source: `/app/assessment_workspace/canon/text/Akki_Canon_7_Integration_and_Quality.txt`
(extracted from `Akki_Canon_7_Integration_and_Quality.docx`). Row IDs `C7-###`.

## Part I — Scope

- **C7-001 (§1)**: Doc 7 specifies (a) how EXTERNAL callers (integrations, third-party applications, licensees) reach the platform's governed intelligence surface, and (b) the QUALITY RULEBOOK — every defect class the platform recognises and how each is closed.
- **C7-002 (§1)**: The custody boundary (Doc 1 §6) is the SAME BOUNDARY every caller crosses — first-party surfaces, third-party integrations, employees, licensees. No caller reaches the estate by any other route.

## Part II — The Custody Boundary Contract

### §3–§8

- **C7-003 (§3 Scoped key)**: Every registered application (Doc 5 §24) holds a scoped key. The scope names: standing objective, memory-plane parameters, model classes callable, refusal shapes to expect.
- **C7-004 (§3)**: Keys are issued through the SAME REGISTRATION FLOW for every caller (first-party or third-party). No back-channel issuance path.
- **C7-005 (§4 Boundary crossing)**: Every crossing is (a) authenticated by scoped key, (b) admitted by Northena (Doc 3 §3), (c) receipted with a trust receipt (Doc 3 §21), (d) subject to input-seat inspection under governance and Watch identities.
- **C7-006 (§5 Answer envelope)**: The response envelope carries: the answer object (or refusal), class chips per claim (Doc 5 §2.1), grounding markers (Doc 5 §2.3), trust receipt id, refusal receipt id if applicable, memory-plane write-back status.
- **C7-007 (§5)**: The answer envelope is stable across versions — additions are strictly additive; no field is repurposed. Version-bumping is ceremony (Doc 3 §37).
- **C7-008 (§6 Three refusal shapes exposed)**: External callers MUST be able to distinguish the three refusal shapes (Doc 3 §17) in the response envelope. Silently collapsing to one refusal is a defect.
- **C7-009 (§7 Webhook)**: Every application registers a webhook that receives compliance-record notifications for events the application caused. The webhook contract is stable and versioned.
- **C7-010 (§8 No warm-up)**: The first call from a registered application is governed identically to the thousandth (Doc 6 §8). No warm-up mode, no bootstrap mode, no unobserved period.

## Part III — Reference Application Identity

### §9–§10

- **C7-011 (§9)**: Akki ships a REFERENCE APPLICATION (Doc 5 §36). It registers itself as an application through the standard flow. It holds NO PRIVILEGED PATH.
- **C7-012 (§10)**: The reference app's key is rotated on the same cadence as any other application's. Its declarations enter the same declarations table.

## Part IV — The Memory Plane

### §19–§23

- **C7-013 (§19 Per-application plane)**: Every application has its own memory plane — a scoped, plane-keyed store the application writes to and reads from. Ownership is the application's; visibility is the estate holder + compliance (Doc 9 §3 memory-plane rows).
- **C7-014 (§19)**: The plane is NOT part of the estate. It is per-application, and its contents do not leak across applications.
- **C7-015 (§20 Retrieval scope)**: Retrieval scope is configured per-application: which estate regions may be retrieved for this app's admits.
- **C7-016 (§21 Write-back)**: Write-back is on/off per application. When on, a per-cycle volume ceiling AND a total storage ceiling BOTH bind. Reaching either ceiling stops write-back and surfaces the state.
- **C7-017 (§22 Retention)**: A per-application retention setting binds how long memory-plane rows persist. Retention expiry deletes with certificate (Doc 5 §22).
- **C7-018 (§23 Precompute)**: Precompute parameters (what the plane pre-materialises for latency reasons) are configured under ceremony.
- **C7-019 (§23)**: The Watch reads plane ACTIVITY as behaviour (Doc 9 §3), never plane CONTENT as data.

## Part V — Buyer / Customer Path

### §24–§27

- **C7-020 (§24 Buyer path)**: A buyer of a data product from the shelf reaches the shelf through the same governed boundary. Every step is receipted.
- **C7-021 (§25 Acquisition)**: Acquisition is a scoped licence issuance — the buyer receives a scoped key, the deliverable, and its full attestation set (Doc 4 §41–§42).
- **C7-022 (§26 Consumption record)**: The buyer sees what they have consumed against their licence — same record, licensee-side reading.
- **C7-023 (§27)**: No commercial relationship, however large, varies the boundary (Doc 1 §13).

## Part VI — The Critic Seam

### §31–§34

- **C7-024 (§31 Standing quality layer)**: The Critic Seam evaluates every worker output against a rubric registered in the platform's registry (Doc 4 §21).
- **C7-025 (§31 Rubric)**: The rubric is versioned. Its version at time-of-evaluation is stamped on every Critic Seam output.
- **C7-026 (§32 Amendments)**: New failure classes are added by amendment to the rubric — never by a parallel checklist (Canon 2 §18). CIF's pre-ship checklist is one such amendment class.
- **C7-027 (§33 Calibration)**: The Critic Seam's own calibration is measured. When its calibration is stale (measured drift beyond a ceremony-set bound), the Compliance Console surfaces it (Doc 5 §18).
- **C7-028 (§34 Independence)**: The Critic Seam and the reviewed worker must satisfy the independence rule (Doc 3 §18) — different base or materially different context.

## Part VII — Defect Taxonomy

### §40–§48

Every defect class recognised by the platform. Row IDs `C7-D#`.

- **C7-D01 (§40.1 D-Ledger)**: A response emitted with an unwritten ledger row (Doc 3 §32). Closes by re-issuing the response after the row lands, OR by rolling back the response.
- **C7-D02 (§40.2 D-Manifest)**: A verdict/answer shipped without its manifest (Canon 2 §8). Closes by attaching the manifest OR retracting the verdict.
- **C7-D03 (§40.3 D-Chip)**: A claim rendered without its class chip (Doc 5 §2.2). Closes by re-rendering with the chip.
- **C7-D04 (§40.4 D-Grounding)**: A fact stored without resolvable source (Doc 1 §4.9). Closes by rejecting the fact at the boundary.
- **C7-D05 (§40.5 D-Fabricated-Absence)**: An unmeasured region rendered as empty/clean/zero (Doc 4 §6). Closes by re-rendering as "not yet measured".
- **C7-D06 (§40.6 D-Confident-Caveat)**: A confident answer shipped with a caveat (Doc 3 §14.2). Closes by refusing at the correct class OR downgrading the class before ship.
- **C7-D07 (§40.7 D-Bypass)**: An operation on the estate that bypassed Northena (Doc 3 §4). Closes by rolling back the operation AND retiring the bypass path (never by patching it).
- **C7-D08 (§41.1 D-Second-Record)**: A service maintaining a second account of events (Doc 1 §4.3). Closes by consolidating to the one record.
- **C7-D09 (§41.2 D-Runtime-Human)**: A person in the runtime path of an operation (Doc 1 §4.7). Closes by redesign — moving the person to declaration/approval, never to runtime.
- **C7-D10 (§41.3 D-Frozen-Mutation)**: A frozen objective mutated in place (Doc 3 §5). Closes by re-admitting under the mutated shape and reversing the mutation.
- **C7-D11 (§41.4 D-Independence)**: A same-base same-context reviewer (Doc 3 §18). Closes by re-review with a properly independent reviewer.
- **C7-D12 (§41.5 D-Rule-Paper)**: A rule with zero automated checks quoted as if in force (Doc 5 §23). Closes by adding a check OR retiring the rule OR downgrading its stated status.
- **C7-D13 (§42.1 D-No-Warmup-Violation)**: An application observed treating first calls differently from steady-state (Doc 6 §8). Closes by removing the warm-up path.
- **C7-D14 (§42.2 D-Untraceable-Adapter)**: An adapter whose lineage cannot be resolved (Doc 4 §28). Closes by retirement.
- **C7-D15 (§42.3 D-MOAC-Missing)**: An adapter shipped without its MOAC scorecard (Doc 4 §26). Closes by rolling back the ship.
- **C7-D16 (§42.4 D-Verdict-Curation)**: A validation sample drawn from curated composition rather than uncurated (Doc 1 §4.10 / Doc 4 §27). Closes by re-drawing from uncurated composition AND publishing whatever it says.
- **C7-D17 (§43.1 D-Console-Interior)**: A surface rendering another authority's interior (Doc 9 §4). Closes by removing the render.
- **C7-D18 (§43.2 D-Watch-Interior)**: The Watch Console rendering thresholds / mark placement / profile internals / mirage construction (Doc 5 §34-A constitutional negatives). Closes by removing the render.
- **C7-D19 (§43.3 D-Behavioural-Register)**: A biometric register acquiring a field for individual identification (Doc 1 §4.2). Closes by rejecting the field's addition at build time; the schema is unrepresentable-by-design.
- **C7-D20 (§43.4 D-Bio-Watch-Merge)**: The Watch's behavioural-conformance parameters (Doc 8) placed in the biometric register OR vice versa (Doc 1 §4.2). Closes by separation.
- **C7-D21 (§44 D-Handoff)**: An unregistered handoff between services or authorities (Doc 9 §6). Closes by registering the handoff OR removing it.
- **C7-D22 (§45.1 D-Dual-Hat)**: A task class mapped to more than one authority (Doc 9 §5). Closes by splitting the task into two.
- **C7-D23 (§45.2 D-Cross-Auth-Credential)**: A credential scope spanning both authorities (Doc 9 §5). Closes by structural removal — the scope is unrepresentable.
- **C7-D24 (§46 D-Missing-Attestation)**: A deliverable shipped without its contents/privacy/quality attestations (Doc 4 §41–§42). Closes by attaching all three OR retracting the deliverable.
- **C7-D25 (§47 D-Refusal-Silent-Collapse)**: An external caller unable to distinguish the three refusal shapes (Doc 3 §17). Closes by re-emitting with the correct shape.
- **C7-D26 (§48 D-Reset-Absent)**: A CIF pre-ship checklist that has not been re-verified after a coach correction (Canon 2 §10.2). Closes by re-verification AND checklist amendment.

## Part VIII — Enforcement of the Rulebook

### §50–§52

- **C7-029 (§50 Build gates)**: Every defect class listed above has a corresponding build gate wherever a class is unrepresentable at code level (§4.2). Failing gates fail the build.
- **C7-030 (§51 Runtime detection)**: Runtime detection produces a defect row in the record. A defect row triggers the resolution path named by the class.
- **C7-031 (§52 Standing queries)**: Standing queries (per Doc 1 §4.3 record discipline) surface defects for compliance-owner review. A rising defect trend triggers a ceremony (Doc 3 §22).

## Part IX — What the Rulebook Does NOT Do

### §55

- **C7-032 (§55)**: The Rulebook does not INVENT new defect classes at runtime. New classes enter by ceremony (Doc 3 §22).
- **C7-033 (§55)**: The Rulebook does not TOLERATE a defect. Every recognised defect has a resolution path; the tolerance is the resolution, not the sitting.
- **C7-034 (§55)**: The Rulebook does not RANK defects by severity as if some were acceptable. Severity affects the CADENCE of the resolution; it does not license the defect to persist.
- **C7-035 (§55)**: The Rulebook does not RE-ROUTE a defect to memory instead of the record.
