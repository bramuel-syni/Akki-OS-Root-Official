# Whitepaper Wizard Spec v1 (banked source of truth)

## Files
- `spec.docx` — raw docx bytes, sha256 in `spec.docx.sha256`. **AUTHORITATIVE.**
- `spec.extracted.txt` — text extracted via `python-docx` (paragraphs + tables preserved). **DERIVED ARTIFACT** — for verbatim quotation in test docstrings after spot-check against `spec.docx`.
- `spec.docx.sha256` — sha256 of `spec.docx` (banked 2026-08-31).

## Ingest discipline
- The docx is authoritative.
- The extracted text is derived. Verbatim quotes in downstream test docstrings must be spot-checked against the docx.

## Provenance
- Source URL: https://customer-assets-cm19k8pv.emergentagent.net/job_amazing-gates-8/artifacts/cxm0vm8t_Whitepaper_Wizard_Spec_v1.docx
- Downloaded: 2026-08-31 (W-WPW-v1-a per SPRINT_PLAN.md)
- Discipline banked: owner ruling 2 (prior session · "Bank BOTH: raw docx bytes ... AND the extracted text alongside it")
