"""services.canon_rules_service.rbm_roc_vocabulary · Family D · RBM-1..23 + ROC-1..11.

Registers `Final[...]` load-bearing vocabulary for the Rules Service canonical
rows (RBM rulebook engine + RBM-23 Watch-learning amendment + ROC rule
criteria) as authored in the v5 Master Requirements Registry · System Rules
Registry sheet (sha-pinned custody workbook sha256
`00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`).

## Owner cross-references (2026-09-21T~06:15Z R-91 NO-EXPEDITE ruling)

RBM-8 (this module · SRR row 295) is the ceremony rule the owner cited as
the mechanic governing R-91's frozen horizon: "System-TCB ceremony: as RBM-7
plus slowest countdown and external witness with no credentials over the
component." R-91 applies at frozen horizon `2026-09-23T03:23:15Z` under
this mechanic — waiver forbidden per owner ruling ("Waiving it because the
sweep already proved green is exactly the argument every future shortcut
would make; the mechanic's value is that it doesn't yield to a good result").

Standing bounds: additive-only per SO §3.8 · closed-vocab per SO §3.10-α ·
zero external I/O · deterministic.
"""

from __future__ import annotations

from typing import Final

# ═══════════════════════════════════════════════════════════════════════════
# Registry-shape · closed vocabularies
# ═══════════════════════════════════════════════════════════════════════════

RBM_RULE_IDS: Final[tuple[str, ...]] = tuple(f"RBM-{i}" for i in range(1, 24))
RBM_RULE_COUNT: Final[int] = 23
RBM_TIER_A_RULE_IDS: Final[tuple[str, ...]] = tuple(f"RBM-{i}" for i in range(1, 23))
RBM_TIER_A_RULE_COUNT: Final[int] = 22
RBM_TIER_A_METADATA: Final[dict[str, str]] = {
    "promise_source": "rulebook_engine_spec_v1",
    "domain": "Rules Service",
    "status": "PROPOSED",
    "objective": "O2 Security & Intent",
}
RBM_TIER_A_ROW_START: Final[int] = 288
RBM_TIER_A_ROW_END: Final[int] = 309

RBM_TIER_B_RULE_IDS: Final[tuple[str, ...]] = ("RBM-23",)
RBM_TIER_B_METADATA: Final[dict[str, str]] = {
    "promise_source": "watch_learning_v1",
    "domain": "O2 Security & Intent",
    "status": "PROPOSED",
}

ROC_RULE_IDS: Final[tuple[str, ...]] = tuple(f"ROC-{i}" for i in range(1, 12))
ROC_RULE_COUNT: Final[int] = 11
ROC_METADATA: Final[dict[str, str]] = {
    "promise_source": "rule_criteria_spec_v1",
    "domain": "Rules Service",
    "status": "PROPOSED (pending ratification)",
}
ROC_ROW_START: Final[int] = 277
ROC_ROW_END: Final[int] = 287


# ═══════════════════════════════════════════════════════════════════════════
# RBM-1..RBM-22 (Tier A · rulebook_engine_spec_v1)
# ═══════════════════════════════════════════════════════════════════════════

RBM_1_SRR_ROW: Final[int] = 288
RBM_1_STATEMENT: Final[str] = "Rule authored with full field set — ID, origination, owner, enforcement class, domain, tier, assessment procedure — or authoring refuses to save"

RBM_2_SRR_ROW: Final[int] = 289
RBM_2_STATEMENT: Final[str] = "Drafting assistance may propose; only the named human author confirms before a rule enters PROPOSED"

RBM_3_SRR_ROW: Final[int] = 290
RBM_3_STATEMENT: Final[str] = "Mnemonic prefix reserved centrally before first use; collision refused at reservation"

RBM_4_SRR_ROW: Final[int] = 291
RBM_4_STATEMENT: Final[str] = "Tier declared at authoring: system-TCB, system-ordinary, or customer"

RBM_5_SRR_ROW: Final[int] = 292
RBM_5_STATEMENT: Final[str] = "Impact record produced before countersign — every dependent rule, checkpoint, component, profile"

RBM_6_SRR_ROW: Final[int] = 293
RBM_6_STATEMENT: Final[str] = "Every adopted or customer rule checked against system rules; refused if it relaxes a STRUCTURAL/MECHANICAL rule"

RBM_7_SRR_ROW: Final[int] = 294
RBM_7_STATEMENT: Final[str] = "System-ordinary/customer ceremony: propose, impact record, countersign, cancellable countdown, apply, re-verify"

# RBM-8 · CEREMONY MECHANIC · owner-cited in R-91 NO-EXPEDITE ruling (2026-09-21T~06:15Z)
RBM_8_SRR_ROW: Final[int] = 295
RBM_8_STATEMENT: Final[str] = "System-TCB ceremony: as RBM-7 plus slowest countdown and external witness with no credentials over the component"
RBM_8_IS_R91_CEREMONY_ANCHOR: Final[bool] = True

# Owner directive this-session (2026-09-21T~06:35Z): "when you author RBM-8,
# its invariant should reflect exactly that: ceremony windows are rigid, no
# shortening path exists in code, and the R-91 window you are currently
# honoring is the live evidence receipt."
RBM_8_CEREMONY_WINDOW_IS_RIGID: Final[bool] = True
RBM_8_NO_SHORTENING_PATH_IN_CODE: Final[bool] = True
RBM_8_R91_LIVE_EVIDENCE_HORIZON_UTC: Final[str] = "2026-09-23T03:23:15Z"
RBM_8_R91_IS_LIVE_EVIDENCE_RECEIPT: Final[bool] = True

# Grep-negative ban anchor: no code path shortens the ceremony countdown.
# Per RBM-8 statement + SO §6.6 verbatim: "a countdown cut short is what FAIL
# looks like" + owner NO-EXPEDITE ruling verbatim: "The countdown that cannot
# be shortened is the ceremony (RBM-8; SER C.5 I-4)".
RBM_8_CEREMONY_SHORTENING_WATCHED_PATTERNS: Final[tuple[str, ...]] = (
    "shorten_ceremony_countdown",
    "expedite_ceremony_apply",
    "waive_ceremony_countdown",
    "bypass_ceremony_horizon",
    "fast_forward_ceremony",
)
RBM_8_CEREMONY_SHORTENING_WATCHED_PATTERN_COUNT: Final[int] = 5


def scan_for_ceremony_shortening_path(code: str) -> tuple[str, ...]:
    """Grep-negative watcher: emits patterns found in `code` that would shorten
    the RBM-8 ceremony countdown. A ceremony window is rigid; no shortening
    path exists in code (owner directive 2026-09-21T~06:35Z). This scanner
    guards that invariant: any hit is a defect. Returns an empty tuple on
    clean input.

    Deterministic · pure-data-in · zero I/O · zero subprocess."""
    return tuple(p for p in RBM_8_CEREMONY_SHORTENING_WATCHED_PATTERNS if p in code)


RBM_9_SRR_ROW: Final[int] = 296
RBM_9_STATEMENT: Final[str] = "Either signatory may cancel before countdown expires; cancellation recorded with identity and reason"

RBM_10_SRR_ROW: Final[int] = 297
RBM_10_STATEMENT: Final[str] = "Apply is atomic: status, Registry entry, Ledger record, rule-version stamp — all four or none"

RBM_11_SRR_ROW: Final[int] = 298
RBM_11_STATEMENT: Final[str] = "Re-verify runs the assessment procedure after apply; failure raises a finding, never a silent rollback"

RBM_12_SRR_ROW: Final[int] = 299
RBM_12_STATEMENT: Final[str] = "Amendment is a new version through full ceremony; prior version retained, never overwritten"

RBM_13_SRR_ROW: Final[int] = 300
RBM_13_STATEMENT: Final[str] = "Retirement is through ceremony; retired rule keeps status and history; destruction attestation where required"

RBM_14_SRR_ROW: Final[int] = 301
RBM_14_STATEMENT: Final[str] = "Library rule book: versioned, cites source clause, every rule in RBM-1's format — uncited rule is not admissible"

RBM_15_SRR_ROW: Final[int] = 302
RBM_15_STATEMENT: Final[str] = "Profile: named bundle of rule books per business type, versioned, changed through system-ordinary ceremony"

RBM_16_SRR_ROW: Final[int] = 303
RBM_16_STATEMENT: Final[str] = "At onboarding, business type selected and matching profile presented as recommendation, marked as such"

RBM_17_SRR_ROW: Final[int] = 304
RBM_17_STATEMENT: Final[str] = "Adoption instantiates rule-book rules as customer rules via customer-tier ceremony, after RBM-6's conflict check"

RBM_18_SRR_ROW: Final[int] = 305
RBM_18_STATEMENT: Final[str] = "Registry is the authoritative store — every ROC-10 field, append-only per ROC-11"

RBM_19_SRR_ROW: Final[int] = 306
RBM_19_STATEMENT: Final[str] = "Assessment procedure runnable on demand and on schedule; Statement of Applicability is a Registry view"

RBM_20_SRR_ROW: Final[int] = 307
RBM_20_STATEMENT: Final[str] = "Registry queryable by ID, objective, promise, tier, status, enforcement class, domain, rule book, profile, tenant"

RBM_21_SRR_ROW: Final[int] = 308
RBM_21_STATEMENT: Final[str] = "Rules Service's own rules are system-TCB tier; no path alters them outside RBM-8's ceremony"

RBM_22_SRR_ROW: Final[int] = 309
RBM_22_STATEMENT: Final[str] = "Every Rules Service action writes an audit record with all six AU-3 elements"


# ═══════════════════════════════════════════════════════════════════════════
# RBM-23 (Tier B · watch_learning_v1 · Certificate requirements amendment)
# ═══════════════════════════════════════════════════════════════════════════

RBM_23_SRR_ROW: Final[int] = 483
RBM_23_STATEMENT: Final[str] = (
    "Certificate requirements are a named rule class of tier system-TCB — they determine Mkono's "
    "inputs. Each is authored with RBM-1's full field set, enters force only through RBM-8's "
    "ceremony (the platform's slowest countdown; an external witness holding no credentials over "
    "the Watch), and is amended or retired only through RBM-12 and RBM-13. Every requirement "
    "carries its provenance — the Ledger references of the incidents it was formed from — and "
    "the library is queryable under RBM-20."
)


# ═══════════════════════════════════════════════════════════════════════════
# ROC-1..ROC-11 (Tier A · rule_criteria_spec_v1)
# ═══════════════════════════════════════════════════════════════════════════

ROC_1_SRR_ROW: Final[int] = 277
ROC_1_STATEMENT: Final[str] = "Definition of a rule — addressable, a requirement not an explanation, falsifiable"

ROC_2_SRR_ROW: Final[int] = 280
ROC_2_STATEMENT: Final[str] = "Rule proliferation forbidden — cite, never reissue, an already-ratified rule"

ROC_3_SRR_ROW: Final[int] = 281
ROC_3_STATEMENT: Final[str] = "POSITIONAL ID scheme — [Part][Section].[Sequence]"

ROC_4_SRR_ROW: Final[int] = 282
ROC_4_STATEMENT: Final[str] = "MNEMONIC ID scheme — [prefix]-[Sequence], for named sub-mechanisms only"

ROC_5_SRR_ROW: Final[int] = 283
ROC_5_STATEMENT: Final[str] = "Scheme exclusivity — one ID scheme per rule population"

ROC_6_SRR_ROW: Final[int] = 284
ROC_6_STATEMENT: Final[str] = "Mnemonic prefixes reserved in the Registry before first use"

ROC_7_SRR_ROW: Final[int] = 285
ROC_7_STATEMENT: Final[str] = "Status axis — CANON · RULED · DEFAULT · PROPOSED · OPEN, exactly five"
ROC_7_STATUS_AXIS: Final[tuple[str, ...]] = ("CANON", "RULED", "DEFAULT", "PROPOSED", "OPEN")
ROC_7_STATUS_AXIS_COUNT: Final[int] = 5

ROC_8_SRR_ROW: Final[int] = 286
ROC_8_STATEMENT: Final[str] = "Enforcement-class axis — STRUCTURAL · MECHANICAL · MEASURED · CEREMONIAL · ADVISORY"
ROC_8_ENFORCEMENT_CLASS_AXIS: Final[tuple[str, ...]] = ("STRUCTURAL", "MECHANICAL", "MEASURED", "CEREMONIAL", "ADVISORY")
ROC_8_ENFORCEMENT_CLASS_AXIS_COUNT: Final[int] = 5

ROC_9_SRR_ROW: Final[int] = 287
ROC_9_STATEMENT: Final[str] = "Domain axis — six engines, four outside-the-six categories, Cross-Cutting"

ROC_10_SRR_ROW: Final[int] = 278
ROC_10_STATEMENT: Final[str] = "A single standing Rule Registry with the required fields per rule"

ROC_11_SRR_ROW: Final[int] = 279
ROC_11_STATEMENT: Final[str] = "Registry is append-only on the Ledger's custody discipline"
