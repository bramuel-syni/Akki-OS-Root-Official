# NON_CLAIMS_REGISTER.md — explicit non-requirements the platform does NOT promise

**Purpose:** track claims that spec authors deliberately state as **NOT** made, so
downstream work never silently treats them as solved. Owner directive
2026-09-08T~06:15Z (banked in DECISIONS.md):

> Owner rule: LIM-1..5 NOT requirements — track in distinct NON-CLAIMS register
> "so nobody later assumes condition 3 was solved". 13th spec, untracked in 1,192.

This register is **not counted in the requirement rollup**. Rows here are
explicit non-claims — reading them as met requirements is a defect.

**Created:** 2026-09-09
**Owner directives banked:** 2026-09-08T~06:15Z · 2026-09-09T~11:40Z (proceed straight through)
**Ratchet floor at creation:** 3017

---

## Register schema

| Field | Meaning |
|---|---|
| id | Non-claim identifier as declared in source spec (e.g. `LIM-1`) |
| spec | Source spec ID (from `notes/spec_id_index.json`) |
| verbatim | Word-for-word claim text from source |
| condition_ref | Which spec-section condition this non-claim is scoped against |
| status | Always `NON-CLAIM` — never `PROPOSED`, `RULED`, `DONE`, `PARTIAL` |
| never_mistake_for | The requirement class this must NEVER be mistaken as |
| citation | Absolute path + line-range in the source doc |

---

## Rows

### `agent_containment_spec_v1` · §5 What This Does Not Claim (word-for-word)

Source doc: `canon/drops/20260910/raw/Agent_Swarm_Containment_Governance_Model_v1.docx` (sha256 `2824796d06d7…`, extracted text `canon/drops/20260910/extracted/text/Agent_Swarm_Containment_Governance_Model_v1.txt`).

| id | spec | verbatim | condition_ref | status | never_mistake_for | citation |
|---|---|---|---|---|---|---|
| LIM-1 | agent_containment_spec_v1 | Does not solve condition 3. Graduated response and bounded sampling reduce exposure; they do not guarantee detection of a sufficiently capable, motivated agent concealing intent. | §3 condition 3 (discrimination problem) · §4 AC-4..AC-6 | NON-CLAIM | a completed detection-of-novel-danger requirement | `canon/drops/20260910/extracted/text/Agent_Swarm_Containment_Governance_Model_v1.txt` §5 |
| LIM-2 | agent_containment_spec_v1 | Does not cover defending an unaffiliated public asset against an attacker with no admission event. Every mechanism here depends on a declared mandate existing to measure conduct against. | §1 scope · Table 0 scope-note | NON-CLAIM | an anti-attacker perimeter capability | `canon/drops/20260910/extracted/text/Agent_Swarm_Containment_Governance_Model_v1.txt` §5 |
| LIM-3 | agent_containment_spec_v1 | Is architecture and specification, verified for internal consistency and cited against published research — not an independently audited, red-teamed, or operationally proven system. No detection-accuracy figure, no track record, is claimed anywhere in this document. | Spec-wide | NON-CLAIM | an evidenced operational track record or accuracy metric | `canon/drops/20260910/extracted/text/Agent_Swarm_Containment_Governance_Model_v1.txt` §5 |
| LIM-4 | agent_containment_spec_v1 | AC-8's structural-separation guarantee is confirmed only for actors operating inside Akki's own six engines. Extending it to an arbitrary external agent's action space is a per-deployment engineering task, not a property this document can promise in advance of that work. | §4 AC-8 · §3 condition 4 partial | NON-CLAIM | a universal structural-separation guarantee for external agents | `canon/drops/20260910/extracted/text/Agent_Swarm_Containment_Governance_Model_v1.txt` §5 |
| LIM-5 | agent_containment_spec_v1 | Does not specify a vocabulary, tool set, or task scope for any particular agent. §4 specifies the mechanism by which a scope is granted, observed, and expanded — never a specific scope itself, which is deployment-specific work against a real system. | §4 AC-2 · AC-3 | NON-CLAIM | a shipped agent tool-vocabulary or task-scope registry | `canon/drops/20260910/extracted/text/Agent_Swarm_Containment_Governance_Model_v1.txt` §5 |

---

## Counts

| Class | Count |
|---|--:|
| NON-CLAIMS total | 5 |
| From `agent_containment_spec_v1` | 5 |

---

## Rule (banked)

**Rows in this register are never counted in requirement-rollup denominators.**
A downstream doc that reads a NON-CLAIM as a requirement is a defect. If a
NON-CLAIM later gets ruled *into* the requirement base (e.g., LIM-3 becomes a
"must be independently red-teamed" requirement), it moves out of this register
by explicit owner ruling banked in `STATE/DECISIONS.md`.

---

**Read `STATE/STANDING_ORDERS.md` first — permanent standing law.**
