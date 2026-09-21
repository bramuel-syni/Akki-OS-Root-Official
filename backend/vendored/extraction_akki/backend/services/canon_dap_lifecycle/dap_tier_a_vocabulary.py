"""services.canon_dap_lifecycle.dap_tier_a_vocabulary · Family C Tier A · DAP-1..DAP-30.

Registers `Final[...]` load-bearing vocabulary for DAP-1..DAP-30 (Data Access
Partner backend spec v1 · Tier A base admission-and-metering rules · promise
column `dap_backend_spec_v1` · domain `DAP (composition — see Doc 0 Component
17)` · objective `O13 Data & Intelligence Acquisition` · status PROPOSED) as
authored in the v5 Master Requirements Registry · System Rules Registry
sheet · rows 315..344 (sha-pinned custody workbook sha256
`00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`).

Rule statements are extracted verbatim from the SRR "Statement" column. The
SRR "Source (file:line)" column pins `dap_backend_spec_v1` (the DAP backend
spec v1 document referenced by the workbook · promise column identical).
Per Ruling 3 erratum the class column is a HINT; the rule text governs.

For all 30 DAP-1..DAP-30 rows the SRR "Enforcement Class" column is EMPTY
per Ruling 3 erratum. Rows are authored strictly from the rule text.

## SRR-status disclosure

DAP-1..DAP-30 carry `status=PROPOSED` on the SRR sheet — not CANON. They
land under the owner's G5-v5 sequencing directive (2026-09-21T~01:00Z at
state commit `a30db4f7`) that named DAP-1..38 as the queue after Family B
with standing GO through the G5 family queue; the COMPLETION SPRINT
directive (2026-09-21T~06:10Z) re-affirmed continuation. Status field
preserved verbatim as `PROPOSED` in row-shared metadata.

## Rules registered (Ruling 5 · SRR rows 315..344 verbatim)

- DAP-1 (row 315) · External party admitted as organisation-level principal ...
- DAP-2 (row 316) · Every request carries a party principal ...
- DAP-3 (row 317) · Connecting an external agent admits an autonomous non-human principal ...
- DAP-4 (row 318) · Slow-play extraction detected against cumulative history ...
- DAP-5 (row 319) · DAP is a trust-domain boundary ...
- DAP-6 (row 320) · Browse returns aggregate composition only ...
- DAP-7 (row 321) · Connected workspace: party's query enters, de-identified results leave ...
- DAP-8 (row 322) · Processed intelligence egresses derived output only ...
- DAP-9 (row 323) · Fine-tuning is compute-to-data only ...
- DAP-10 (row 324) · Trained weights/skill files leave as artefact egress ...
- DAP-11 (row 325) · Raw download is the outer-gate crossing (#25) ...
- DAP-12 (row 326) · Admission of an external party is a governed act ...
- DAP-13 (row 327) · API keys per party principal ...
- DAP-14 (row 328) · Controlled request routes to named approving authority ...
- DAP-15 (row 329) · Approval decisions recorded with authority, decision, reason ...
- DAP-16 (row 330) · Fine-tune and skill-development always require approval ...
- DAP-17 (row 331) · Standing approval possible, revocable in one act ...
- DAP-18 (row 332) · Every extraction is a commissioned job with a frozen objective (#32)
- DAP-19 (row 333) · Every job routes to its governing engine per §4 ...
- DAP-20 (row 334) · Assistance chat may shape pre-commission ...
- DAP-21 (row 335) · Every operation emits a metered event ...
- DAP-22 (row 336) · Terms resolve most-specific-first ...
- DAP-23 (row 337) · Spend against ceiling evaluated before execution ...
- DAP-24 (row 338) · Cumulative extraction history per party is first-class ...
- DAP-25 (row 339) · Every custody-class/operation combination defaults unavailable ...
- DAP-26 (row 340) · Owner sets terms/ceilings per custody class and party ...
- DAP-27 (row 341) · Owner can suspend a party in one act ...
- DAP-28 (row 342) · Every gate fails closed ...
- DAP-29 (row 343) · A metered event that cannot be written to the Ledger refuses the operation ...
- DAP-30 (row 344) · Browse degrades rather than refuses ...

Standing bounds: additive-only per SO §3.8 · closed-vocab per SO §3.10-α ·
zero external I/O · deterministic.
"""

from __future__ import annotations

from typing import Final

# ═══════════════════════════════════════════════════════════════════════════
# Registry-shape · closed vocabulary of DAP Tier A rule IDs
# ═══════════════════════════════════════════════════════════════════════════

DAP_TIER_A_RULE_IDS: Final[tuple[str, ...]] = tuple(f"DAP-{i}" for i in range(1, 31))
DAP_TIER_A_RULE_COUNT: Final[int] = 30
DAP_TIER_A_SRR_ROW_START: Final[int] = 315
DAP_TIER_A_SRR_ROW_END: Final[int] = 344

DAP_TIER_A_ROW_SHARED_METADATA: Final[dict[str, str]] = {
    "objective": "O13 Data & Intelligence Acquisition",
    "promise_source": "dap_backend_spec_v1",
    "status": "PROPOSED",
    "domain": "DAP (composition — see Doc 0 Component 17)",
    "relationship": "New — not in base registry",
}


# ═══════════════════════════════════════════════════════════════════════════
# DAP-1..DAP-30 · statement + SRR row · byte-verbatim from Ruling-5 authority
# ═══════════════════════════════════════════════════════════════════════════

DAP_1_SRR_ROW: Final[int] = 315
DAP_1_STATEMENT: Final[str] = "External party admitted as organisation-level principal with identity, posture, terms, domain, mandate"

DAP_2_SRR_ROW: Final[int] = 316
DAP_2_STATEMENT: Final[str] = "Every request carries a party principal with its own mandate, mark state, behavioural signature"

DAP_3_SRR_ROW: Final[int] = 317
DAP_3_STATEMENT: Final[str] = "Connecting an external agent admits an autonomous non-human principal with its own stated scope"

DAP_4_SRR_ROW: Final[int] = 318
DAP_4_STATEMENT: Final[str] = "Slow-play extraction detected against cumulative history, not evaluated per request"

DAP_5_SRR_ROW: Final[int] = 319
DAP_5_STATEMENT: Final[str] = "DAP is a trust-domain boundary — no shared identifier resolution, store, or credential with the party"

DAP_6_SRR_ROW: Final[int] = 320
DAP_6_STATEMENT: Final[str] = "Browse returns aggregate composition only — never unit contents, sample, or preview"

DAP_7_SRR_ROW: Final[int] = 321
DAP_7_STATEMENT: Final[str] = "Connected workspace: party's query enters, de-identified results leave, estate data never leaves"

DAP_8_SRR_ROW: Final[int] = 322
DAP_8_STATEMENT: Final[str] = "Processed intelligence egresses derived output only; source units recorded, not reconstructable"

DAP_9_SRR_ROW: Final[int] = 323
DAP_9_STATEMENT: Final[str] = "Fine-tuning is compute-to-data only — no configuration permits the inverse"

DAP_10_SRR_ROW: Final[int] = 324
DAP_10_STATEMENT: Final[str] = "Trained weights/skill files leave as artefact egress with rights posture, hash, terms cited"

DAP_11_SRR_ROW: Final[int] = 325
DAP_11_STATEMENT: Final[str] = "Raw download is the outer-gate crossing (#25) — redaction as a gate, evidence record written"

DAP_12_SRR_ROW: Final[int] = 326
DAP_12_STATEMENT: Final[str] = "Admission of an external party is a governed act requiring the estate owner's named authority"

DAP_13_SRR_ROW: Final[int] = 327
DAP_13_STATEMENT: Final[str] = "API keys per party principal, revocable in one act, expiring, non-transferable, never logged"

DAP_14_SRR_ROW: Final[int] = 328
DAP_14_STATEMENT: Final[str] = "Controlled request routes to named approving authority before execution; does not execute pending"

DAP_15_SRR_ROW: Final[int] = 329
DAP_15_STATEMENT: Final[str] = "Approval decisions recorded with authority, decision, reason; no execution on silence"

DAP_16_SRR_ROW: Final[int] = 330
DAP_16_STATEMENT: Final[str] = "Fine-tune and skill-development always require approval; raw download always if controlled"

DAP_17_SRR_ROW: Final[int] = 331
DAP_17_STATEMENT: Final[str] = "Standing approval possible, revocable in one act, must name controlled units explicitly to cover them"

DAP_18_SRR_ROW: Final[int] = 332
DAP_18_STATEMENT: Final[str] = "Every extraction is a commissioned job with a frozen objective (#32)"

DAP_19_SRR_ROW: Final[int] = 333
DAP_19_STATEMENT: Final[str] = "Every job routes to its governing engine per §4; DAP holds no extraction logic of its own"

DAP_20_SRR_ROW: Final[int] = 334
DAP_20_STATEMENT: Final[str] = "Assistance chat may shape pre-commission; cannot approve, widen scope, or decide any gate"

DAP_21_SRR_ROW: Final[int] = 335
DAP_21_STATEMENT: Final[str] = "Every operation emits a metered event with all required fields, written before result returned"

DAP_22_SRR_ROW: Final[int] = 336
DAP_22_STATEMENT: Final[str] = "Terms resolve most-specific-first: party, then custody class, then estate default"

DAP_23_SRR_ROW: Final[int] = 337
DAP_23_STATEMENT: Final[str] = "Spend against ceiling evaluated before execution; over-ceiling routes to a person"

DAP_24_SRR_ROW: Final[int] = 338
DAP_24_STATEMENT: Final[str] = "Cumulative extraction history per party is first-class, queryable, retained for full admission"

DAP_25_SRR_ROW: Final[int] = 339
DAP_25_STATEMENT: Final[str] = "Every custody-class/operation combination defaults unavailable — availability is granted, not assumed"

DAP_26_SRR_ROW: Final[int] = 340
DAP_26_STATEMENT: Final[str] = "Owner sets terms/ceilings per custody class and party; changes never alter receipts already issued"

DAP_27_SRR_ROW: Final[int] = 341
DAP_27_STATEMENT: Final[str] = "Owner can suspend a party in one act — halts all in-flight and future operations, recorded"

DAP_28_SRR_ROW: Final[int] = 342
DAP_28_STATEMENT: Final[str] = "Every gate fails closed — no result returned when a governing check cannot complete"

DAP_29_SRR_ROW: Final[int] = 343
DAP_29_STATEMENT: Final[str] = "A metered event that cannot be written to the Ledger refuses the operation it meters"

DAP_30_SRR_ROW: Final[int] = 344
DAP_30_STATEMENT: Final[str] = "Browse degrades rather than refuses — stale data marked as stale, never presented as complete"
