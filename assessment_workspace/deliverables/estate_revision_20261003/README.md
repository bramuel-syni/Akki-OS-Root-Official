# Updated RMS Estate and Language Review — 3 October 2026

## Released files

Native commission `com-1f3a3606e140`, version 5, build `bld-d6cb1af0f370`.
All formats: validation PASS, QA PASS, byte-identical double build.

- Word: `/downloads/RMS_Estate_and_Language_Review_Updated_2026-10-03.docx`
- Excel: `/downloads/RMS_Estate_and_Language_Review_Updated_2026-10-03.xlsx`
- PowerPoint: `/downloads/RMS_Estate_and_Language_Review_Updated_2026-10-03.pptx`

`finalized_release_manifest.json` records exact hashes, sizes, source evidence snapshot
hash, code repair hashes and the final test receipt. Standard unversioned links are
also updated; date-suffixed copies preserve this delivered snapshot.

## Scope and limitations

Interim accessible-estate baseline: OBS snapshot 01:40 UTC and NAS snapshot 01:38 UTC.
The database measurement is the existing banked census; its historical measurement
date is retained. This release does not claim that every folder or file was sampled.
Inaccessible or restore-required content has no inferred hours or language labels.
Model-derived confidence intervals describe sampling uncertainty, not model error,
nonresponse bias, certification or guarantees. Storage-class shares apply only to
the class-observed subset. Net invoice-backed savings remain unverified.

## Native production and review trail

The estate-intelligence producer assembled newer source evidence and authored v3.
The table-selector numeric check was repaired without permitting unrelated literal
figures. Mechanical QA then caught receipt/coverage overflow. Font-metric pagination
fixed it without dropping evidence or weakening QA; full receipt text is in the appendix.

`submitted_revision.json` and `final_submitted_revision.json` were applied through
the native commission revision API, preserving earlier drafts and builds. The
independent review of v4 is retained in `final_independent_review.json`; it requested
alignment of the pilot count and some wording. Version 5 corrects those findings.
The advisory suggesting missing F015/F018/F009/F082 tokens was not substantiated:
they exist in the frozen evidence, resolve correctly, and were explicitly tested.
There is no claimed independent-model ACCEPT for v5; final mechanical and targeted
editorial checks, and Office-file/download integrity, passed.

## Verification

Testing-agent initial report: `/app/test_reports/iteration_81.json`.
Final targeted suite: `/app/test_reports/pytest/iter81_final.xml` — 8 passed.
Public stable links additionally downloaded by curl; exact SHA256 matches the native
released artifacts. DOCX, XLSX and PPTX reopen with their Office parsers; no unresolved
figure tokens or spreadsheet formula errors found. Representative final evidence,
coverage and receipt slides inspected visually. App UI and owner HTML unchanged.

## Next evidence improvement

Continue accessible-folder samples; prioritise large or wide-interval strata; add
independent human labels (including abstentions); reconcile duration estimators.
Handle access grants, restorations and missing inventory separately, without holding
back work on content already accessible. No new compute, storage moves or deletions
were launched to produce this revision.