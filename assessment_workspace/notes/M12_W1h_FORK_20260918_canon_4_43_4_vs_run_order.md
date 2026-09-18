# M12-W1h fork · Canon 4 §43.4 vs Owner Run Order · banked 2026-09-18T~19:50Z

## The fork

**Owner Run Order 2026-09-18T~15:30Z (banked in STATE/DECISIONS.md line 13000 verbatim):**

> "W1h (D-17 inner perimeter + D-16 local-first cascade)"

**Canon 4 §43.4 verbatim (from `/app/assessment_workspace/notes/chunk1_20260918/canon_text/Akki_Canon_4_Operating_Engines.txt` lines 277-280):**

> "43.4 Local-cascade offload
>
> Where a metered frontier model carries workload a cheaper local model could filter, a cascade — local model drafts, the frontier model handles only what the local model cannot — reduces spend. Cascades carry a documented failure mode: when too many items escalate, each escalated item pays twice, and the cascade becomes net-negative.
>
> **A cascade builds only against demonstrated cost pressure. No cascade scaffolding, draft-model acquisition, or routing machinery is built before metered telemetry on a named seam shows spend exceeding a threshold set at that time — no threshold is defined in advance of the evidence.**
>
> Its shape, once triggered: a local model drafts, a deterministic acceptance check decides, and the frontier model is invoked only on rejects — the acceptance check is rung-one machinery, not a second model's judgement. The cascade emits its double-pay rate from its first run and retires if escalation makes it net-negative against the pre-cascade baseline."

**Canon 1 §A5.5 (already anchored in W1g) verbatim:**

> "Exactly one path leaves the perimeter, and it is the custody boundary. Nothing else in the platform holds outbound network capability ... Where an external frontier model is genuinely required, the custody boundary governs that single crossing."

**D-17 verbatim (DECISIONS.md line 11773):**

> "Frontier model access is gateway-only with customer-held provider accounts by default. Anchor: Doc 14 C5.2. Platform-provider accounts (i.e. Akki-held keys in front of a customer workload) are used ONLY under a reseller agreement reviewed by counsel. D-10 AMENDED: any prior D-10 language authorising platform-provider-account default use for frontier calls is superseded by D-17."

## Interpretations

### Reading A · CANON-COMPATIBLE STRUCTURAL PROHIBITIONS (DEFAULT-class)

W1h lands the ENFORCEMENT of D-16 + D-17 as **structural prohibitions**, not as cascade machinery. Specifically:

1. **Canon 4 §43.4 structural gate**: no cascade module exists in `services/`. AST + file scan enforces: no file named `cascade`, `local_draft`, `escalate_on_reject`, `cheap_first`, etc.
2. **Cost-pressure receipt gate**: cascade admission requires `phase0/cost_pressure_receipts/<seam>.json` — currently empty (no cost pressure demonstrated yet). Test asserts the directory is empty OR contains only manifest-shape files.
3. **D-17 inner perimeter**: static test that every provider entry in `llm_endpoint_allowlist.v0.json` for a FRONTIER provider (anthropic/openai/google, not `emergent`) is annotated `key_class: "customer-held"` (default) or `key_class: "reseller-authorized"` (only if paired with counsel-review receipt file present).
4. **D-10 supersession recorded**: DECISIONS.md carries the D-10 amendment note (already present at line 11773 — asserted verbatim).
5. **C.19.6 reversal recorded**: DECISIONS.md carries the C.19.6 model-policy reversal note (already present via R-18 Part 4 — asserted verbatim).
6. **Frontier-only-through-chokepoint AST re-assertion**: the existing W1a/W5 sole-importer discipline is re-anchored to Canon 1 §A5.5 verbatim ("the custody boundary governs that single crossing") in a new companion test — additive coverage of the existing invariant, but with the Canon 1 §A5.5 anchor now explicit.

**No cascade machinery is built.** No `local_draft`, no `escalate_on_reject`, no routing table for `frontier|local`.

**Why this is Canon-compatible**: Canon 4 §43.4 forbids BUILDING the machinery, not ENFORCING the prohibition. Reading A builds the enforcement (structural prohibition) — which is what the doctrine requires until cost pressure lands.

### Reading B · LITERAL CASCADE MACHINERY BUILD

W1h builds `services/cascade/local_draft.py` + `services/cascade/router.py` + acceptance-check tests, per the LITERAL Run Order.

**Why this is Canon-INCOMPATIBLE**: Canon 4 §43.4 verbatim: *"No cascade scaffolding, draft-model acquisition, or routing machinery is built before metered telemetry on a named seam shows spend exceeding a threshold set at that time."* No metered telemetry has been demonstrated. Building this now = canon violation.

**This reading requires an OWNER RULING** to amend Canon 4 §43.4 or to carve an exception. Per SO §3 order of authority (canon → Standing Orders → SER → contract schemas → code): canon wins, so Reading B is not admissible without ratification.

### Reading C · SKIP W1h ENTIRELY

Skip W1h and jump to W1i (TCB golden-input byte-identical tests). Note W1h as "canon-blocked pending cost-pressure telemetry".

**Why this is under-honest**: The Run Order asks W1h to be closed. Reading A satisfies the Run Order's INTENT (banking D-16 + D-17 into the enforcement surface) while respecting Canon 4 §43.4's build-prohibition. Reading C leaves the D-16/D-17 doctrines only in DECISIONS.md, unenforced by tests. That's a discipline miss the owner has repeatedly named as failure class.

## Recommendation · DEFAULT-class = Reading A

Land Reading A as W1h. It is canon-compatible, does not require an owner ruling, and satisfies the Run Order's intent (D-16 + D-17 landed in the enforcement surface). Reading B held banked for the day cost-pressure telemetry arrives.

**Modified Stop Discipline application** (owner ruling 2026-09-18T~17:30Z verbatim): *"For non-consequential forks, bank the fork, take your own recommendation (tagged DEFAULT-class), and continue on everything else."*

This fork qualifies as **non-consequential** because Reading A is canon-compatible; it does not amend canon, does not add a TCB member, does not carve an exception. It's a routine interpretive choice between three readings, one of which is doctrinally-correct.

**Autopilot continues NON-STOP.** Reading A becomes the CP-M12-W1h implementation. If the owner later rules Reading B is desired with a cost-pressure receipt already banked, Reading B lands as its own subsequent cycle without disturbing the Reading A structural prohibition (which stays as the fallback should the cascade ever be retired).
