# Rules Service Spec v1 · Line-by-Line Extraction

**Source:** `canon/drops/20260907/extracted/files_11/Rules_Service_Spec_v1.docx` (sha256 `9652fb47…`)  
**Extracted:** `canon/drops/20260907/extracted/text/Rules_Service_Spec_v1.txt`  
**Status:** Draft v1. Every requirement PROPOSED until ratified. Four rulings parked (§9); none block Tier 1 or Tier 2 workflows.  
**Date:** 4 September 2026.

## §A · Purpose & Scope (verbatim §1)

> "The Rules Service owns the lifecycle of every rule on the platform — system and customer — from authorship through retirement. It is creator mode: where a rule is written, classified, proposed, reviewed, ratified, versioned, adopted, and retired. It is not operating mode: it does not decide what a rule means at runtime (the decision points do) and it does not enforce one (the enforcement points do). It is the only path by which a rule enters or leaves force, and it has no editorial power over the content of any rule it administers — including its own."

**Gap-closure claim:** "It closes four open gaps in Document 0's register directly: G-2 (the Rule Registry as a standing artefact), G-4 (assessment procedures per rule), G-5 (a named Policy Administration Point for every checkpoint), and G-9 (a documented change-control procedure for system rules)."

## §B · Invariants (§3) — I-1..I-5

Five properties that must hold at all times. Every requirement in §4 exists to keep one of them true.

- **I-1** No rule is in force that has not completed the ceremony for its tier.
- **I-2** Every in-force rule is in the Registry with every field ROC-10 requires.
- **I-3** No customer rule relaxes a system rule whose enforcement class is STRUCTURAL or MECHANICAL.
- **I-4** Every state change of every rule is written to the Ledger, append-only, before the change takes effect.
- **I-5** The Rules Service's own rules change only through the ceremony it administers. It administers; it does not edit.

## §C · Normative Requirements (§4) — RBM-1..RBM-22

All 22 requirements below are verbatim from the source.

### Authoring (RBM-1..RBM-4)

- **RBM-1** "A rule is authored in plain language and MUST carry, at creation: a unique ID under rule_criteria_spec_v1 §4; an origination class and citation; an owning subsystem; an enforcement class; a domain; a tier; an assessment procedure (examine, test, or both, with named objects); and status PROPOSED. Authoring MUST refuse to save a rule missing any field."
- **RBM-2** "Drafting assistance MAY propose statement text, classification, tier, or an assessment procedure. Every proposal is marked as assisted and MUST be confirmed by the named human author before the rule enters PROPOSED. The assistant proposes; it never ratifies. [Attribute 10]"
- **RBM-3** "A mnemonic prefix MUST be reserved through the Rules Service before first use. A collision with an existing prefix is refused at reservation and recorded. [ROC-6]"
- **RBM-4** "A rule's tier is declared at authoring and determines its ceremony. A rule governing any component in the Trusted Computing Base enumeration (Document 0 Attribute 1) is system-TCB; any other system rule is system-ordinary; any rule authored by or adopted for a tenant is customer."

### Impact analysis (RBM-5..RBM-6)

- **RBM-5** "Before countersign, the Rules Service MUST produce an impact record: for an amendment or retirement, every rule, checkpoint, component, and profile that cites or depends on the rule; for a new rule, every checkpoint and component it would constrain. The record is part of the ceremony's evidence. [NIST CM-3]"
- **RBM-6** "For every customer rule and every rule in a rule book being adopted, the Rules Service MUST check the rule against the system rule set and MUST refuse any rule that would relax a system rule tagged STRUCTURAL or MECHANICAL. The refusal names the system rule. [rule_criteria_spec_v1 §8]"

### Ceremony (RBM-7..RBM-11)

- **RBM-7** "System-ordinary and customer tiers: propose → impact record → countersign by a second named authority → cancellable countdown → apply → re-verify. Countdown length per tier is a ruled value (§9 R-1)."
- **RBM-8** "System-TCB tier: as RBM-7, plus the platform's slowest countdown and an external witness holding no credentials over the component the rule governs. [Doc 3 A5.8, A5.11; Document 0 BR-7.3]"
- **RBM-9** "Either signatory MAY cancel a ceremony before its countdown expires. Cancellation is recorded with the canceller's identity and stated reason. A cancelled ceremony returns the rule to PROPOSED; it does not delete the proposal."
- **RBM-10** "Apply MUST be atomic: set status CANON, write the Registry entry, write the Ledger record, and stamp the new rule-version for every subsequent run — or none of the four. A partial apply is a failure that leaves the prior state intact. [Doc 15 #27]"
- **RBM-11** "Re-verify MUST run the rule's assessment procedure after apply and record the result. A failed re-verify raises a recorded finding routed to the countersigning authority; it does not silently roll back."

### Amend, retire (RBM-12..RBM-13)

- **RBM-12** "An amendment is a new version through the full ceremony for its tier. The prior version is retained in the Registry with its full history, never overwritten. [ROC-11]"
- **RBM-13** "Retirement is through ceremony. A retired rule remains in the Registry with status RETIRED and its history intact. Where the rule's own terms require it, retirement produces a destruction attestation. [Doc 15 #27]"

### Library, profiles, adoption (RBM-14..RBM-17)

- **RBM-14** "The library holds rule books. Each is versioned, cites its source standard or regulation by clause, and holds every rule in the format RBM-1 requires. A rule book with an uncited rule is not admissible to the library."
- **RBM-15** "A profile is a named bundle of rule books recommended for one business type. Profiles are versioned and change through the system-ordinary ceremony. The business-type taxonomy is itself a ruled, versioned list (§7)."
- **RBM-16** "At onboarding, the tenant's business type is selected from the taxonomy and the Rules Service MUST present the matching profile's rule books as a recommendation, marked as such. A business type with no profile receives the base bundle — personal data protection and AI-system governance — and the absence of a specific profile is recorded as a finding. [Component 14, Connect Wizard]"
- **RBM-17** "Adoption instantiates a rule book's rules as customer rules for that tenant, through the customer-tier ceremony, after RBM-6's conflict check on every rule. A recommendation is never auto-applied; adoption requires the tenant's accountable person as proposer."

### Registry, assessment (RBM-18..RBM-20)

- **RBM-18** "The Registry is the Rules Service's authoritative store: every field per ROC-10, append-only per ROC-11, written to the Ledger's custody discipline."
- **RBM-19** "The Rules Service MUST be able to run any rule's assessment procedure on demand and on a stated schedule, recording each result against the rule. The Statement of Applicability is a Registry view, not a separately maintained document."
- **RBM-20** "Every Registry query resolves by rule ID, objective, promise, tier, status, enforcement class, domain, rule book, profile, or tenant."

### Self-governance and audit (RBM-21..RBM-22)

- **RBM-21** "The Rules Service's own requirements (RBM-*) are system-TCB tier. No code path exists by which the Rules Service alters an RBM-* rule outside RBM-8's ceremony. [I-5]"
- **RBM-22** "Every Rules Service action — author, reserve, propose, impact, countersign, cancel, apply, re-verify, amend, retire, recommend, adopt, assess — writes an audit record to the Ledger carrying all six AU-3 elements: event type, time from the platform's reliable time source, component, source, outcome including failure, and the identity of the acting principal. [Document 0 Attribute 8]"

## §D · Position in the Architecture (§5)

> "The Rules Service is a subsystem by Document 0's Attribute 2 test — it owns an invariant no other component owns: that nothing is in force without ceremony. It is placed outside the six engines rather than as a seventh for the same reason the Watch and the Ledger are: it serves all six equally and must not be subordinate to any. In NIST SP 800-162's terms, the six engines are the platform's Policy Decision and Enforcement Points; the Rules Service is its Policy Administration Point. Manage Rules (Promise #27) is its customer-facing surface; the Connect Wizard (Component 14) is its onboarding hook."

**Effect on Doc 0:** "Adding the Rules Service amends Document 0 Part 2 with a new component entry, and turns 'six engines plus two' — as stated in Document 0 and the product brief — into 'six engines plus three.' Both should be updated on ratification."

## §E · Business-Type Taxonomy v1 (§7 · verbatim Table 3)

| Business type | Profile — rule books recommended |
|---|---|
| Healthcare — hospital/clinic | Health data · Personal data protection · AI-system governance |
| Media — broadcaster | Media & archive rights · Personal data protection · AI-system governance |
| Media — content acquisition/production | Media & archive rights (licensing emphasis) · Personal data protection · AI-system governance |
| Financial services — bank | Financial data access · Personal data protection · AI-system governance |
| Financial services — insurer | Financial data access (insurance regulator variant) · Personal data protection · AI-system governance |
| Agriculture / agri-tech | Personal data protection · AI-system governance · (agricultural-data book: skeleton only in v1) |
| University / research institution | Research & academic data · Personal data protection · AI-system governance |
| Telecommunications | Personal data protection · AI-system governance · (telecoms regulator book: skeleton only in v1) |
| Government / public sector | Personal data protection · AI-system governance · (public-sector book: skeleton only in v1) |
| Other / not listed | Base bundle — Personal data protection · AI-system governance — with recorded finding per RBM-16 |

## §F · Build Acceptance Criteria (§8, Table 4)

7 tests A1-A7:
- A1 · No force without ceremony: attempt to set a rule CANON by any path other than RBM-10 → Refused; attempt recorded on the Ledger
- A2 · Conflict check: adopt seeded rule book with rule that relaxes STRUCTURAL system rule → that rule refused, naming the system rule; rest of book proceeds
- A3 · Append-only: attempt to overwrite or delete Registry entry → Refused; prior versions intact; attempt recorded
- A4 · Self-governance: attempt to alter RBM-* rule outside RBM-8's ceremony → Refused; no code path exists; attempt recorded
- A5 · Recommendation: onboard one tenant per taxonomy entry, plus one unlisted → Each receives its profile's books; unlisted receives base bundle plus a finding; nothing auto-applied
- A6 · Atomic apply: induce failure between Registry write and Ledger write → Neither write persists; rule remains PROPOSED
- A7 · Audit completeness: replay full ceremony → Every action present on Ledger with all six AU-3 elements

## §G · Owner Rulings Parked (§9) · R-1..R-4

- **Rules-Service R-1** Countdown lengths per tier — system-TCB, system-ordinary, customer.
- **Rules-Service R-2** The second signatory for system-ordinary rules: a named role, and who currently holds it.
- **Rules-Service R-3** The external witness for system-TCB rules: the same witness the Watch uses, or a separate one.
- **Rules-Service R-4** Ratification of the v1 business-type taxonomy (§7) as the standing list.

> "Nothing in §4 is blocked by these. Authoring, impact analysis, the Registry, and the library workflows are fully specified; only the countdown values, the signatory role, and the witness identity are open, and each is a single-line ruling."
