"""services.canon_dap_lifecycle.dap_tier_b_vocabulary · Family C Tier B · DAP-31..DAP-38.

Registers `Final[...]` load-bearing vocabulary for DAP-31..DAP-38 (Data Access
Partner Tier B amendments · Security Amendments 31..36 · Pruning & Unlearning
37..38) as authored in the v5 Master Requirements Registry · System Rules
Registry sheet (sha-pinned custody workbook sha256
`00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`).

## Tier B source breakdown

- DAP-31..DAP-36 (SRR rows 349..354) · promise `Security_Amendments_Trojan_Whisper.docx` · domain `DAP`
- DAP-37..DAP-38 (SRR rows 473..474) · promise `Pruning & Unlearning Amendment` · domain `O13 Data & Intelligence Acquisition`

All 8 rows carry `status=PROPOSED` on the SRR sheet — landed under owner
G5-v5 sequencing directive (2026-09-21T~01:00Z at `a30db4f7`) that named
DAP-1..38 as the queue after Family B + COMPLETION SPRINT directive
(2026-09-21T~06:10Z) re-affirmed continuation. Rule statements byte-verbatim
from SRR "Statement" column per Ruling 3 (rule text governs).

Standing bounds: additive-only per SO §3.8 · closed-vocab per SO §3.10-α ·
zero external I/O · deterministic.
"""

from __future__ import annotations

from typing import Final

# ═══════════════════════════════════════════════════════════════════════════
# Registry-shape · closed vocabulary of DAP Tier B rule IDs
# ═══════════════════════════════════════════════════════════════════════════

DAP_TIER_B_RULE_IDS: Final[tuple[str, ...]] = tuple(f"DAP-{i}" for i in range(31, 39))
DAP_TIER_B_RULE_COUNT: Final[int] = 8

DAP_TIER_B_SECURITY_AMENDMENT_RULE_IDS: Final[tuple[str, ...]] = tuple(f"DAP-{i}" for i in range(31, 37))
DAP_TIER_B_SECURITY_AMENDMENT_ROW_START: Final[int] = 349
DAP_TIER_B_SECURITY_AMENDMENT_ROW_END: Final[int] = 354
DAP_TIER_B_SECURITY_AMENDMENT_METADATA: Final[dict[str, str]] = {
    "promise_source": "Security_Amendments_Trojan_Whisper.docx",
    "domain": "DAP",
    "status": "PROPOSED",
    "objective": "O13 Data & Intelligence Acquisition",
}

DAP_TIER_B_PRUNING_UNLEARNING_RULE_IDS: Final[tuple[str, ...]] = ("DAP-37", "DAP-38")
DAP_TIER_B_PRUNING_UNLEARNING_ROW_START: Final[int] = 473
DAP_TIER_B_PRUNING_UNLEARNING_ROW_END: Final[int] = 474
DAP_TIER_B_PRUNING_UNLEARNING_METADATA: Final[dict[str, str]] = {
    "promise_source": "Pruning & Unlearning Amendment",
    "domain": "O13 Data & Intelligence Acquisition",
    "status": "PROPOSED",
    "objective": "O13 Data & Intelligence Acquisition",
}


# ═══════════════════════════════════════════════════════════════════════════
# DAP-31..DAP-36 · Security Amendments (Trojan Whisper)
# ═══════════════════════════════════════════════════════════════════════════

DAP_31_SRR_ROW: Final[int] = 349
DAP_31_STATEMENT: Final[str] = "Artefact egress distance gate — no weights/skill file leaves without passing a reproduction probe"

DAP_32_SRR_ROW: Final[int] = 350
DAP_32_STATEMENT: Final[str] = "Admission integrity for entering base models — provenance, hash, mirage behavioural probe"

DAP_33_SRR_ROW: Final[int] = 351
DAP_33_STATEMENT: Final[str] = "Every DAP operation's output passes A5.15 before return to the party (browse exempt)"

DAP_34_SRR_ROW: Final[int] = 352
DAP_34_STATEMENT: Final[str] = "Coalition membership recorded at admission; classes (a)/(b) deterministic, class (c) labelled suspicion"

DAP_35_SRR_ROW: Final[int] = 353
DAP_35_STATEMENT: Final[str] = "Estate release budget — ruled ceiling on total release across all parties/operations/time; floor violation on breach"

DAP_36_SRR_ROW: Final[int] = 354
DAP_36_STATEMENT: Final[str] = "Differentially private training (DP-SGD) by default for every fine-tune; non-DP requires approval + stricter gate"


# ═══════════════════════════════════════════════════════════════════════════
# DAP-37..DAP-38 · Pruning & Unlearning Amendment
# ═══════════════════════════════════════════════════════════════════════════

DAP_37_SRR_ROW: Final[int] = 473
DAP_37_STATEMENT: Final[str] = (
    "A fine-tuned artefact MAY be pruned — magnitude pruning or an equivalent structural reduction "
    "— between MOAC acceptance and DAP-31's distance gate, as a ruled optional step. Pruning is a "
    "second, empirical reduction in memorisation surface on top of DAP-36's differentially private "
    "training; it is never a substitute for it, and this document does not present it as one. A "
    "pruned artefact MUST re-pass MOAC's acceptance criteria — pruning can degrade performance below "
    "the accepted bar, and acceptance is re-evaluated, not assumed to survive the change. A pruned "
    "artefact's hash differs from its pre-pruning hash; it is a new artefact for every purpose DAP-10 "
    "and DAP-31 govern, including a fresh pass through the distance gate at the ruled threshold. "
    "Pruning ratio and method are ruled values, ratified alongside DAP-31's own probe parameters."
)

DAP_38_SRR_ROW: Final[int] = 474
DAP_38_STATEMENT: Final[str] = (
    "When a unit's rights status changes to withdrawn — consent revoked, licence expired, or an "
    "equivalent event — every artefact whose training manifest cites that unit is identified via the "
    "registry (a query, per RBM-20's design, not a search) and is either re-derived without the unit "
    "or recalled. Re-derivation trains a replacement artefact excluding the withdrawn unit, using the "
    "same run configuration recorded in the original training manifest, and passes it through DAP-31 "
    "and MOAC as a new artefact before it replaces the original in the registry. Recall withdraws the "
    "original artefact's registry entry and, where the artefact was already delivered under DAP-10, "
    "notifies the receiving party that the artefact's rights basis has changed. A unit's contribution "
    "to the estate release budget (DAP-35) is NOT refunded on unlearning — the privacy loss from the "
    "original release already occurred; unlearning restores the artefact's cleanliness going forward, "
    "not the budget already spent."
)
