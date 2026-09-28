"""W-RELEASE-GATE-PILOT-LIFT · CP-RG2 · TokenizationReceipt frozen 7-carrier.

Discharge anchors (verbatim on single un-wrapped lines):

- R-15(a) · DECISIONS.md 2026-09-15T~03:55Z · Effect 2 (owner verbatim):
      "People's names are tokenized before anything leaves — placeholder tokens per custody class (Pull Seam identity-never-crosses). named_persons_verdict resolves to TOKENIZED for release purposes; build/wire the tokenization step into the transcript release path (tests-first)."

- Pull Seam §2 P1 · P015.s6 (canon source-file:
  canon/drops/20260914_pull_seam/extracted/The_Pull_Seam_STRUCTURED.txt · P015.s6):
      "There is no configuration in which estate data is transferred to compute outside the perimeter."

Shape (frozen · exactly seven carriers · exact order):

- `receipt_id`        : `str` · deterministic sha256-derived (`tr_<64-hex>`).
- `transcript_id`     : `str` · foreign-key reference to the tokenized transcript.
- `tokenized_at_utc`  : `str` · ISO-8601 UTC.
- `token_count`       : `int` · number of DISTINCT named-person tokens emitted.
- `token_table_ref`   : `str` · OPAQUE reference (`tt_<64-hex>`) to the custody
                                token-table row. NOT the mapping.
- `custody_class`     : `str` · custody-class label (per R-15(a): "placeholder
                                tokens per custody class"; initial value
                                `"named_person"`).
- `algorithm_version` : `str` · version of the tokenization algorithm
                                (e.g. `"tokenize_named_persons_v1"`).

Identity-never-crosses invariant (P015.s6): NONE of these carriers IS or
CONTAINS the placeholder → name mapping. The mapping is retrievable only via
`services.de_identify.tokenize_named_persons.get_token_table(receipt_id)`.

Landing in `NON_CONTRACT_UTILITY_MODULES` (test_frozen_contract_snapshot_parity.py):
frozen `@dataclass` — no pydantic BaseModel — frozen-contract-parity does not apply.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TokenizationReceipt:
    """Frozen carrier for one tokenization pass over a transcript.

    Field order is fixed. Mutation after construction raises FrozenInstanceError.
    Adding a field is a snapshot-parity event even though `tokenization_receipt.py`
    is in NON_CONTRACT_UTILITY_MODULES.
    """

    receipt_id: str
    transcript_id: str
    tokenized_at_utc: str
    token_count: int
    token_table_ref: str
    custody_class: str
    algorithm_version: str
