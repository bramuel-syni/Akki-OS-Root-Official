"""W-EXPORT-ARTEFACT-RENDER · CP-EXR1 · Export render + release-gate composition.

Discharge anchors (verbatim on single un-wrapped lines):

- Canon-4 §22 · canon/text/Akki_Canon_4_Operating_Engines.txt line 118 verbatim:
      "The function returns unit references only. It carries no class decision. A load-bearing function that returned a class would have collapsed the two faculties into one — Solva chooses the units; it does not choose what those units imply."

- DAP-Spec §A10 · via CP-D6 substrate · verbatim:
      "exports must carry rights posture + hash + derivation from controlled units + terms cited"

- R-7 · DECISIONS 2026-09-15T~03:55Z · Effect 1 verbatim:
      "every release is still receipted AND debited into a running release ledger from day one — so when the pilot ends, the real budget number is set from measured usage, not guessed. The gate's refusal on unset-budget is replaced by pilot-mode admission WITH mandatory receipt+debit; a missing receipt still refuses (Pull Seam P7 unchanged)."

- R-15(a) · DECISIONS 2026-09-15T~03:55Z · Effect 2 verbatim:
      "People's names are tokenized before anything leaves — placeholder tokens per custody class (Pull Seam identity-never-crosses). named_persons_verdict resolves to TOKENIZED for release purposes; build/wire the tokenization step into the transcript release path (tests-first)."

- R-16(a) · DECISIONS 2026-09-15T~03:55Z · Effect 3 verbatim:
      "Set transfer_basis: DERIVATIVE_ONLY_VIA_PULL_SEAM for the transcript-text-only tier — the Pull Seam is the model-facing seam; source data does not cross; only derivatives (tokenized transcripts) cross"

- Pull Seam §2 P7 · P036 verbatim:
      "The receipt is written before the result is returned. If it cannot be written, the operation is refused."

Contract:

    render_export_and_release(*, export_kind, rows, rights_posture,
                              derivation_hash, derivation_unit_refs,
                              terms_cited, named_persons, transcript_id,
                              kdpa_verdict, licence_class,
                              release_receipt_id, release_budget_state,
                              usage_quantity, usage_unit, debited_by_party)
        -> Tuple[bytes, ReleaseLedgerDebit]

Ordering (P036 receipt-before-result):
    1. Validate `export_kind` in {"csv", "pdf"} (closed-set discipline) —
       else `ExportKindUnknown`.
    2. Compose `ExportArtefact` + `admit_export` (DAP-A10) — may raise
       `ExportRefused` naming the empty carrier.
    3. Tokenize `named_persons` if non-empty (R-15(a)) — via
       `tokenize_named_persons`.
    4. Compose `TranscriptArtefact` with `transfer_basis =
       DERIVATIVE_ONLY_VIA_PULL_SEAM` (R-16(a)) and `named_persons_verdict
       = TOKENIZED` if tokenized else `DPO-APPROVED`.
    5. `admit_transcript_release_pilot_open` — writes the debit (== the
       receipt) BEFORE any payload bytes are rendered. May raise
       `TranscriptTierRefused / TranscriptVerdictPending /
       TranscriptVerdictUnknown / ReceiptMissingRefused /
       BudgetStateRefused` — on any refusal, NO payload bytes are
       rendered and NO debit is written for the refused branch.
    6. Render payload bytes (CSV or PDF).
    7. Return `(payload_bytes, debit)`.
"""
from __future__ import annotations

import csv
import io
from typing import Sequence, Tuple

from contracts.release_budget import ReleaseBudgetState, ReleaseLedgerDebit
from services.audio_poc.release_gate import (
    TranscriptArtefact,
    SAFE_TRANSCRIPT_TIER,
    admit_transcript_release_pilot_open,
)
from services.data_suite_v2.export_artefact import ExportArtefact
from services.data_suite_v2.export_gate import admit_export
from services.de_identify.tokenize_named_persons import tokenize_named_persons


# Closed set of admissible export kinds this wave.  Owner directive
# (2026-09-15T~15:35Z verbatim): "no scope creep into new export types
# beyond what the Data-Suite surfaces already declare".  Additional kinds
# are follow-on waves.
EXPORT_KINDS_ACCEPTABLE: frozenset = frozenset({"csv", "pdf"})


class ExportKindUnknown(Exception):
    """Raised when `export_kind` is outside `EXPORT_KINDS_ACCEPTABLE`.

    Closed-set discipline mirrors CP-RG3 named_persons_verdict pattern.
    Extending the acceptable set is an owner-ratified snapshot-parity event.
    """


def _pdf_escape(s: str) -> bytes:
    """Escape a Python str for a PDF literal string.

    Escapes: backslash, open paren, close paren.  Encodes as latin-1 with
    non-latin-1 chars mapped to '?' (ASCII-safe payload; PDF-1.4 literal
    strings are byte-oriented and latin-1 covers the ASCII surface this
    wave produces).
    """
    escaped = (
        s.replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )
    return escaped.encode("latin-1", errors="replace")


def _render_csv(
    *,
    rights_posture: str,
    derivation_hash: str,
    derivation_unit_refs: Sequence[str],
    terms_cited: Sequence[str],
    rows: Sequence[Sequence[str]],
) -> bytes:
    """Render CSV payload with a 4-line preamble carrying the DAP-A10 carriers.

    Preamble shape (each preamble line begins with '#' for downstream parsers
    to recognise as metadata):

        #rights_posture,<value>
        #derivation_hash,<value>
        #derivation_unit_refs,<refs joined by ';'>
        #terms_cited,<terms joined by ';'>

    Then the data rows follow, one per line.  UTF-8 encoded.  No timestamps
    embedded — CSV payload is deterministic across calls with byte-identical
    inputs (Canon-4 §22 UnitRefs-only + wave §D.E.6).
    """
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["#rights_posture", rights_posture])
    w.writerow(["#derivation_hash", derivation_hash])
    w.writerow(["#derivation_unit_refs", ";".join(derivation_unit_refs)])
    w.writerow(["#terms_cited", ";".join(terms_cited)])
    for row in rows:
        w.writerow(list(row))
    return buf.getvalue().encode("utf-8")


def _render_pdf(
    *,
    rights_posture: str,
    derivation_hash: str,
    derivation_unit_refs: Sequence[str],
    terms_cited: Sequence[str],
    rows: Sequence[Sequence[str]],
) -> bytes:
    """Render a minimal PDF-1.4 single-page ASCII text stream.

    No external deps.  Hand-rolled with exact XREF byte offsets.  Contains
    a preamble carrying the four DAP-A10 carriers, then one line per data
    row.  Passes basic PDF-1.4 shape checks: starts `%PDF-1.4`, ends
    `%%EOF`, single page object.
    """
    text_lines = [
        f"Rights: {rights_posture}",
        f"Hash: {derivation_hash}",
        f"UnitRefs: {';'.join(derivation_unit_refs)}",
        f"TermsCited: {';'.join(terms_cited)}",
        "",
    ]
    text_lines.extend(" | ".join(str(c) for c in row) for row in rows)

    # Build the content stream: a text object with each line as a Tj
    # showing on its own line via T* (line-move).
    content = b"BT\n/F1 10 Tf\n50 750 Td\n14 TL\n"
    for line in text_lines:
        content += b"(" + _pdf_escape(line) + b") Tj T*\n"
    content += b"ET\n"

    def _obj(n: int, body: bytes) -> bytes:
        return f"{n} 0 obj\n".encode("ascii") + body + b"\nendobj\n"

    header = b"%PDF-1.4\n%\xff\xff\xff\xff\n"
    obj1 = _obj(1, b"<< /Type /Catalog /Pages 2 0 R >>")
    obj2 = _obj(2, b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    obj3 = _obj(
        3,
        b"<< /Type /Page /Parent 2 0 R "
        b"/Resources << /Font << /F1 4 0 R >> >> "
        b"/MediaBox [0 0 612 792] /Contents 5 0 R >>",
    )
    obj4 = _obj(4, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    obj5_body = (
        f"<< /Length {len(content)} >>\nstream\n".encode("ascii")
        + content
        + b"endstream"
    )
    obj5 = _obj(5, obj5_body)

    # Compute cumulative byte offsets for the XREF table.
    offsets = []
    running = len(header)
    for obj in (obj1, obj2, obj3, obj4, obj5):
        offsets.append(running)
        running += len(obj)

    xref_offset = running
    xref = b"xref\n0 6\n0000000000 65535 f \n"
    for off in offsets:
        xref += f"{off:010d} 00000 n \n".encode("ascii")

    trailer = (
        b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n"
        + f"{xref_offset}\n".encode("ascii")
        + b"%%EOF\n"
    )

    return header + obj1 + obj2 + obj3 + obj4 + obj5 + xref + trailer


def render_export_and_release(
    *,
    export_kind: str,
    rows: Sequence[Sequence[str]],
    rights_posture: str,
    derivation_hash: str,
    derivation_unit_refs: Sequence[str],
    terms_cited: Sequence[str],
    named_persons: Sequence[str],
    transcript_id: str,
    kdpa_verdict: str,
    licence_class: str,
    release_receipt_id: str,
    release_budget_state: ReleaseBudgetState,
    usage_quantity: int,
    usage_unit: str,
    debited_by_party: str,
) -> Tuple[bytes, ReleaseLedgerDebit]:
    """Render an export payload and route through the release gate under
    pilot rules.

    See module docstring for the ordering discipline (P036 receipt-before-
    result).  On any refusal (from step 1..5), NO payload bytes are rendered
    and NO debit is written for the refused branch.

    On success, returns `(payload_bytes, debit)`.
    """
    # Step 1: closed-set discipline on export_kind.
    if export_kind not in EXPORT_KINDS_ACCEPTABLE:
        raise ExportKindUnknown(
            f"export_kind {export_kind!r} outside acceptable set "
            f"{sorted(EXPORT_KINDS_ACCEPTABLE)}; extending the set is an "
            "owner-ratified snapshot-parity event"
        )

    # Step 2: DAP-A10 admit (may raise ExportRefused naming empty carrier).
    art_export = ExportArtefact(
        rights_posture=rights_posture,
        derivation_hash=derivation_hash,
        derivation_unit_refs=tuple(derivation_unit_refs),
        terms_cited=tuple(terms_cited),
    )
    admit_export(art_export)

    # Step 3: R-15(a) tokenization if names declared.
    if named_persons:
        transcript_text = "\n".join(
            " | ".join(str(c) for c in row) for row in rows
        )
        tokenized_text, _tok_receipt = tokenize_named_persons(
            transcript_id=transcript_id,
            transcript_text=transcript_text,
            named_persons=named_persons,
        )
        # Split back to rows preserving the pipe delimiter used above.
        effective_rows = [
            line.split(" | ") for line in tokenized_text.split("\n")
        ]
        named_persons_verdict = "TOKENIZED"
    else:
        effective_rows = [list(row) for row in rows]
        named_persons_verdict = "DPO-APPROVED"

    # Step 4: Compose TranscriptArtefact (R-16(a) DERIVATIVE_ONLY_VIA_PULL_SEAM).
    art_transcript = TranscriptArtefact(
        tier=SAFE_TRANSCRIPT_TIER,
        kdpa_verdict=kdpa_verdict,
        named_persons_verdict=named_persons_verdict,
        transfer_basis="DERIVATIVE_ONLY_VIA_PULL_SEAM",
        licence_class=licence_class,
    )

    # Step 5: P036 receipt-before-result — admit + record debit BEFORE render.
    debit = admit_transcript_release_pilot_open(
        art_transcript,
        release_receipt_id=release_receipt_id,
        release_budget_state=release_budget_state,
        usage_quantity=usage_quantity,
        usage_unit=usage_unit,
        debited_by_party=debited_by_party,
    )

    # Step 6: Render payload bytes (receipt already written).
    if export_kind == "csv":
        payload = _render_csv(
            rights_posture=rights_posture,
            derivation_hash=derivation_hash,
            derivation_unit_refs=derivation_unit_refs,
            terms_cited=terms_cited,
            rows=effective_rows,
        )
    else:  # pdf (closed-set means only these two are reachable)
        payload = _render_pdf(
            rights_posture=rights_posture,
            derivation_hash=derivation_hash,
            derivation_unit_refs=derivation_unit_refs,
            terms_cited=terms_cited,
            rows=effective_rows,
        )

    # Step 7: return.
    return payload, debit
