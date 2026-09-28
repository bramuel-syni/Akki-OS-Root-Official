"""services.canon_doc1_chokepoint.chokepoint_vocabulary · G5-v5 Family A first sub-slice.

Registers `Final[...]` load-bearing vocabulary for A5.1..A5.9 (Doc 1 · M12
chokepoint · CANON) as authored in the v5 Master Requirements Registry ·
System Rules Registry sheet · rows R2..R10 (sha-pinned custody workbook
sha256 `00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`).

The rule text is extracted verbatim from the source `.docx` at
`fixtures/files_9_extracted/01_Custody_and_the_Crossing_Part_1_The_Chokepoint.docx`
(sha256 `a33588298100c6224366623e64ac8632b48294649e57ad43cf67ee6730f97844`).
The v5 SRR "Source (file:line)" column cites `.md:LINE-N` for each row; the
extension differs (`.docx` on disk vs `.md` cited) but the filename byte-matches
otherwise. Per Ruling 3 erratum extended this-session (state commit `afd0f3c7`
2026-09-21T03:42:00Z) the pointer shape is a HINT and the rule text governs.

For all 9 A5.1..A5.9 rows the SRR "Enforcement Class" column is EMPTY per
Ruling 3 erratum ("class column is a HINT · rule text governs"). Therefore
V7 rows are authored strictly from the rule text.

## Rules registered (Ruling 5 · SRR rows R2..R10 verbatim)

- A5.1 · The single chokepoint (row R2)
- A5.2 · The custody sequence (row R3)
- A5.3 · The per-request envelope does not outlive the call (row R4)
- A5.4 · Tenant-scoped entity resolution (row R5)
- A5.5 · The outbound network is closed except at the crossing (row R6)
- A5.6 · Structural impossibility, not policed prohibition (row R7)
- A5.7 · The trust receipt (row R8)
- A5.8 · Two custody pathways, both receipted, neither bypassing the other (row R9)
- A5.9 · Grounding failure is a refusal, not a degraded answer (row R10)

## Grep-negative scanner anchors (where rule text states them)

- A5.1 · `scan_for_non_chokepoint_model_invocation` — rule says an
  "automated negative-scan test that fails the build if any module other
  than the chokepoint function imports or invokes the model client".
- A5.3 · `scan_for_envelope_persistence` — rule says the envelope is
  "never persisted to disk as a standing record, never shared between
  requests, and never available to any consumer after the call completes".
- A5.5 · `scan_for_outbound_network_outside_crossing` — rule says "No
  other module in the platform holds outbound network capability" and a
  "static-analysis build gate that fails the build if any module other
  than the crossing acquires outbound network capability".
- A5.7 · `scan_for_credential_at_receipt` — rule says "the credential
  used to reach the model is never logged or included".
- A5.9 · `scan_for_degraded_answer_on_grounding_failure` — rule says
  "refusal, not a weaker answer offered anyway" and "never a silent
  partial" where model output cannot be grounded in permitted material.

Pure-data-in scanners (no I/O · no exception · no network): each takes a
text blob, returns a tuple of `(line_no, matched_pattern)` hits, empty
tuple when no watched pattern is present. Watch-pattern tuples are
themselves `Final[tuple[str, ...]]` closed-vocabs.

Standing bounds: additive-only per SO §3.8 · closed-vocab per SO §3.10-α ·
zero external I/O · deterministic.
"""

from __future__ import annotations

from typing import Final

# ═══════════════════════════════════════════════════════════════════════════
# Registry-shape · closed vocabulary of Doc 1 A5 CANON rule IDs
# ═══════════════════════════════════════════════════════════════════════════

DOC1_A5_RULE_IDS: Final[tuple[str, ...]] = (
    "A5.1",
    "A5.2",
    "A5.3",
    "A5.4",
    "A5.5",
    "A5.6",
    "A5.7",
    "A5.8",
    "A5.9",
)
DOC1_A5_RULE_COUNT: Final[int] = 9

DOC1_A5_ROW_SHARED_METADATA: Final[dict[str, str]] = {
    "objective": "O1 Custody & Confidentiality",
    "promise": "#1 — NO LEAKAGE OF CONFIDENTIAL INFORMATION",
    "doc": "Doc 1",
    "status": "CANON",
    "domain": "SyniSense",
    "relationship": "Base canon",
}


# ═══════════════════════════════════════════════════════════════════════════
# A5.1 · The single chokepoint · SRR row R2
# Rule: "There is exactly one function in the entire codebase that invokes
#        the external model client. ... enforced by an automated negative-scan
#        test that fails the build if any module other than the chokepoint
#        function imports or invokes the model client. The guarantee is placed
#        at the narrowest point in the system rather than the most convenient."
# ═══════════════════════════════════════════════════════════════════════════

A5_1_STATEMENT: Final[str] = "The single chokepoint"
A5_1_SOURCE_FILE_LINE: Final[str] = (
    "01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:67"
)
A5_1_INVARIANT_EXACTLY_ONE_MODEL_CLIENT_INVOCATION: Final[bool] = True
A5_1_INVARIANT_ENFORCED_BY_NEGATIVE_SCAN_BUILD_GATE: Final[bool] = True
A5_1_INVARIANT_GUARANTEE_AT_NARROWEST_POINT_NOT_ORCHESTRATOR: Final[bool] = True

NON_CHOKEPOINT_MODEL_INVOCATION_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "import_model_client_outside_chokepoint",
    "invoke_model_client_outside_chokepoint",
    "direct_llm_call_bypass_chokepoint",
    "engine_calls_model_client_without_crossing",
    "orchestrator_invokes_model_client",
)


def scan_for_non_chokepoint_model_invocation(text: str) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors A5.1's grep-negative ban ("fails the build if any module other
    than the chokepoint function imports or invokes the model client").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in NON_CHOKEPOINT_MODEL_INVOCATION_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# A5.2 · The custody sequence · SRR row R3
# Rule: "Every model invocation transits three steps in fixed order, and no
#        path is authorised to skip any of them: De-identify. ... Invoke. ...
#        Re-identify."
# ═══════════════════════════════════════════════════════════════════════════

A5_2_STATEMENT: Final[str] = "The custody sequence"
A5_2_SOURCE_FILE_LINE: Final[str] = (
    "01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:69"
)
A5_2_STEPS: Final[tuple[str, ...]] = ("de-identify", "invoke", "re-identify")
A5_2_STEP_COUNT: Final[int] = 3
A5_2_INVARIANT_FIXED_ORDER_NO_SKIP: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# A5.3 · The per-request envelope does not outlive the call · SRR row R4
# Rule: "The token-to-value mapping is held in a custody envelope scoped to
#        that single request. ... never persisted to disk as a standing
#        record, never shared between requests, and never available to any
#        consumer after the call completes."
# ═══════════════════════════════════════════════════════════════════════════

A5_3_STATEMENT: Final[str] = "The per-request envelope does not outlive the call"
A5_3_SOURCE_FILE_LINE: Final[str] = (
    "01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:77"
)
A5_3_INVARIANT_ENVELOPE_SCOPED_TO_SINGLE_REQUEST: Final[bool] = True
A5_3_INVARIANT_ENVELOPE_NEVER_PERSISTED_TO_DISK: Final[bool] = True
A5_3_INVARIANT_ENVELOPE_NEVER_SHARED_BETWEEN_REQUESTS: Final[bool] = True
A5_3_INVARIANT_ENVELOPE_NEVER_AVAILABLE_AFTER_CALL_COMPLETES: Final[bool] = True

ENVELOPE_PERSISTENCE_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "persist_envelope",
    "save_custody_envelope",
    "store_token_to_value_mapping",
    "cache_envelope_across_requests",
    "envelope_available_after_call_completes",
)


def scan_for_envelope_persistence(text: str) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors A5.3's grep-negative ban (envelope "never persisted to disk as a
    standing record, never shared between requests, and never available to any
    consumer after the call completes").
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in ENVELOPE_PERSISTENCE_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# A5.4 · Tenant-scoped entity resolution · SRR row R5
# Rule: "De-identification is not limited to what a general-purpose identifier
#        recogniser happens to detect. Each tenant supplies the set of entities
#        that must be recognised for their instance ... This tenant entity set
#        is the same mechanism Promise #2 (Document 2) allows the DPO to extend
#        with declared-confidential terms."
# ═══════════════════════════════════════════════════════════════════════════

A5_4_STATEMENT: Final[str] = "Tenant-scoped entity resolution"
A5_4_SOURCE_FILE_LINE: Final[str] = (
    "01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:81"
)
A5_4_INVARIANT_TENANT_SUPPLIES_ENTITY_SET: Final[bool] = True
A5_4_INVARIANT_EXTENDS_GENERIC_RECOGNISER: Final[bool] = True
A5_4_INVARIANT_PROMISE_2_MECHANISM_SHARED: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# A5.5 · The outbound network is closed except at the crossing · SRR row R6
# Rule: "Exactly one path leaves the organisation's perimeter, and it is the
#        custody boundary. No other module in the platform holds outbound
#        network capability. ... a network-layer allowlist that refuses
#        outbound connections originating from anywhere except the crossing,
#        and a static-analysis build gate ... Compute does not leave the
#        perimeter either."
# ═══════════════════════════════════════════════════════════════════════════

A5_5_STATEMENT: Final[str] = "The outbound network is closed except at the crossing"
A5_5_SOURCE_FILE_LINE: Final[str] = (
    "01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:83"
)
A5_5_INVARIANT_EXACTLY_ONE_OUTBOUND_PATH: Final[bool] = True
A5_5_INVARIANT_NETWORK_LAYER_ALLOWLIST_REFUSES_ELSEWHERE: Final[bool] = True
A5_5_INVARIANT_STATIC_ANALYSIS_BUILD_GATE: Final[bool] = True
A5_5_INVARIANT_COMPUTE_STAYS_INSIDE_PERIMETER: Final[bool] = True

OUTBOUND_NETWORK_OUTSIDE_CROSSING_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "outbound_network_capability_outside_crossing",
    "module_holds_outbound_socket_outside_crossing",
    "acquire_outbound_capability_bypass_crossing",
    "engine_opens_outbound_connection_not_via_crossing",
    "outbound_connection_originating_elsewhere_than_crossing",
)


def scan_for_outbound_network_outside_crossing(text: str) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors A5.5's grep-negative ban ("No other module in the platform holds
    outbound network capability" + build gate on modules acquiring outbound
    network capability outside the crossing).
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in OUTBOUND_NETWORK_OUTSIDE_CROSSING_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# A5.6 · Structural impossibility, not policed prohibition · SRR row R7
# Rule: "The platform's enforcement doctrine is that a prohibition enforced by
#        review is eventually violated, whereas a prohibition enforced by a
#        function signature, a type, or a schema cannot be violated without
#        the violation failing to compile or failing to persist."
# ═══════════════════════════════════════════════════════════════════════════

A5_6_STATEMENT: Final[str] = "Structural impossibility, not policed prohibition"
A5_6_SOURCE_FILE_LINE: Final[str] = (
    "01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:89"
)
A5_6_INVARIANT_STRUCTURAL_ENFORCEMENT_NOT_REVIEW: Final[bool] = True
A5_6_INVARIANT_SIGNATURE_TYPE_OR_SCHEMA_LEVEL: Final[bool] = True
A5_6_INVARIANT_DOCTRINE_STATED_IN_DOC_16: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# A5.7 · The trust receipt · SRR row R8
# Rule: "A trust receipt is emitted per invocation. ... the credential used to
#        reach the model is never logged or included; its presence is surfaced
#        only as a boolean probe at module load ... the receipt is signed and
#        bound to the organisation alone ... the receipt is written to the one
#        authoritative record."
# ═══════════════════════════════════════════════════════════════════════════

A5_7_STATEMENT: Final[str] = "The trust receipt"
A5_7_SOURCE_FILE_LINE: Final[str] = (
    "01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:91"
)
A5_7_INVARIANT_RECEIPT_EMITTED_PER_INVOCATION: Final[bool] = True
A5_7_INVARIANT_CREDENTIAL_NEVER_LOGGED_OR_INCLUDED: Final[bool] = True
A5_7_INVARIANT_CREDENTIAL_SURFACED_AS_BOOLEAN_PROBE_ONLY: Final[bool] = True
A5_7_INVARIANT_RECEIPT_SIGNED_BOUND_TO_ORGANISATION: Final[bool] = True
A5_7_INVARIANT_RECEIPT_WRITTEN_TO_ONE_AUTHORITATIVE_RECORD: Final[bool] = True

CREDENTIAL_AT_RECEIPT_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "log_credential_in_receipt",
    "receipt_includes_credential_value",
    "trust_receipt_contains_secret",
    "receipt_serialises_credential_string",
    "credential_written_to_receipt_field",
)


def scan_for_credential_at_receipt(text: str) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors A5.7's grep-negative ban ("the credential used to reach the model
    is never logged or included" in the trust receipt).
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in CREDENTIAL_AT_RECEIPT_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)


# ═══════════════════════════════════════════════════════════════════════════
# A5.8 · Two custody pathways, both receipted, neither bypassing the other · SRR row R9
# Rule: "The platform has two custody pathways: the synthesis path through the
#        chokepoint ... and the perception path through the perception router ...
#        Both emit receipts. Neither pathway is a way around the other. ... both
#        paths carry the same custody obligation."
# ═══════════════════════════════════════════════════════════════════════════

A5_8_STATEMENT: Final[str] = (
    "Two custody pathways, both receipted, neither bypassing the other"
)
A5_8_SOURCE_FILE_LINE: Final[str] = (
    "01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:101"
)
A5_8_PATHWAYS: Final[tuple[str, ...]] = ("synthesis", "perception")
A5_8_PATHWAY_COUNT: Final[int] = 2
A5_8_INVARIANT_BOTH_EMIT_RECEIPTS: Final[bool] = True
A5_8_INVARIANT_NEITHER_BYPASSES_THE_OTHER: Final[bool] = True
A5_8_INVARIANT_SAME_CUSTODY_OBLIGATION_ON_BOTH: Final[bool] = True


# ═══════════════════════════════════════════════════════════════════════════
# A5.9 · Grounding failure is a refusal, not a degraded answer · SRR row R10
# Rule: "Where the model returns something that cannot be grounded in permitted
#        material, the correct behaviour is refusal, not a weaker answer
#        offered anyway. ... a complete answer is one that is both re-identified
#        and grounded, and the absence of either yields a defined refusal,
#        never a silent partial."
# ═══════════════════════════════════════════════════════════════════════════

A5_9_STATEMENT: Final[str] = "Grounding failure is a refusal, not a degraded answer"
A5_9_SOURCE_FILE_LINE: Final[str] = (
    "01_Custody_and_the_Crossing_Part_1_The_Chokepoint.md:103"
)
A5_9_INVARIANT_REFUSAL_ON_UNGROUNDED_ANSWER: Final[bool] = True
A5_9_INVARIANT_NO_SILENT_PARTIAL: Final[bool] = True
A5_9_INVARIANT_COMPLETE_ANSWER_IS_REIDENTIFIED_AND_GROUNDED: Final[bool] = True
A5_9_INVARIANT_PROMISE_8_FULL_STATEMENT: Final[bool] = True

DEGRADED_ANSWER_ON_GROUNDING_FAILURE_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "soften_when_ungrounded",
    "return_weaker_answer_on_grounding_failure",
    "silent_partial_when_source_missing",
    "degrade_answer_when_cannot_ground",
    "offer_hedged_reply_without_grounding",
)


def scan_for_degraded_answer_on_grounding_failure(text: str) -> tuple[tuple[int, str], ...]:
    """Return `((line_no, pattern), ...)` for each watched pattern found in
    `text`; empty tuple on clean input. Pure function; no I/O; deterministic.

    Anchors A5.9's grep-negative ban ("refusal, not a weaker answer offered
    anyway" and "never a silent partial" where model output cannot be grounded
    in permitted material).
    """
    hits: list[tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pat in DEGRADED_ANSWER_ON_GROUNDING_FAILURE_WATCHED_PATTERNS:
            if pat in line:
                hits.append((line_no, pat))
    return tuple(hits)
