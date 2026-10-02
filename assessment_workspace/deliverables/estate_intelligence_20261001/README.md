# Owner report pair — final delivery

## Preferred downloads after reported Bad Gateway
- `/downloads/RMS_Estate_Report.pptx`
- `/downloads/RMS_Estate_Report.docx`
- `/downloads/RMS_Estate_Reports.zip` — both exact files in one download.

These static frontend paths avoid the API upstream and contain unchanged report bytes. Files are under `/app/frontend/public/downloads/`; regenerate them with `publish_downloads.py`. All three were independently verified through actual browser download events, hashes and ZIP parity in `test_reports/iteration_78.json`. Original API routes were responding during rechecks; the precise intermittent gateway trigger remains unconfirmed.

User requested one combined, detailed, articulate and rigorous PPTX/Word pair, without UI embedding:
1. Estate intelligence, with duplication primarily here.
2. Non-English, non-music audio and text quantities, hours, volumes and quality, at a standard appropriate for a global AI lab.
3. A broad opportunity portfolio, beyond context-as-a-service and open-source enablement.

## Files
- `backend/deliverables/RMS_Estate_Intelligence_and_Language_Opportunities.pptx` — **43 slides**.
- `backend/deliverables/RMS_Estate_Intelligence_and_Language_Opportunities.docx` — **24 rendered A4 pages**.
- Direct paths: `/api/deliverables/RMS_Estate_Intelligence_and_Language_Opportunities.pptx` and the same stem with `.docx`. Use the current frontend environment URL as the host. Existing allowlisted attachment route only; no UI embedding or new report dashboard.

## Accounting discipline
- Candidate staged audio: **3,958 files, 529.3379 header-duration hours, 36,516,920,948 bytes**, across eight folder labels. Header readability is not an audio-quality grade. Music/language purity and independently qualified speech hours are unknown.
- Companion staged transcripts: **3,939 files, 37,192,774 bytes**. They are not automatically aligned to all audio hours.
- Separate transcript assembly: **157,513 natural units, 27,329,904 characters, 4,521 source files**, seven language labels. Natural splits reconcile to 129,984 / 8,280 / 18,980 / 269. Added canaries are separate and not counted as natural inventory.
- Do not add overlapping storage inventories or text populations. Database grades are not speech-quality grades. Conditional language-ID accuracy is shown separately from coverage/correct-of-all. The incomplete waveform measurement's stale progress is not a verified quality dataset.
- Twelve opportunity analyses cover users, value, prerequisites, delivery/economic model and success criteria. Rights and demand are not presumed. No revenue forecast, legal certification or whole-estate eligible-corpus total is invented.

## Reproduction and verification
- `evidence/`: pinned retained records; hashes appear in Word appendix B. No new corpus read, model run or dataset cleanup was launched.
- `build_report.py`: single source for the coherent deck/paper narrative, data model, charts, source references and specification.
- `commission/`: native document-studio brief, content, direction verdict and deck/paper specifications.
- `release/a/out/` and `release/b/out/`: reproducible final outputs. `release-build.log`: native schema/validation/QA PASS and byte-identical proof. No validators were weakened.
- `finalize_statistics.py`: deterministic correction of Word extended properties only, leaving document body untouched; applied to both reproducible outputs. `finalized_release_manifest.json` is the authoritative final checksum/size manifest.
- Final checks: `/app/test_reports/iteration_77.json` plus `/app/test_reports/pytest/iteration_77_finalized.xml` (**9 passed**); downloadable files exactly match both finalized builds; correct MIME and attachment headers, ZIP integrity, LibreOffice conversion, 43 slides / 24 pages, source quantities and absence of unresolved tokens verified.
- Independent content review found the uncertainty qualifications appropriate. Contact-sheet visual review completed; the text model's potentially misleading multi-series Word chart was replaced with an explicit metric table, and the PPT uses clear conditional/coverage/correct-of-all statements.
- DOCX metadata issue from the first verification was corrected. Text statistics use a documented OOXML tokenizer; Word may recalculate them on opening.
- No mocked API or invented measurement in this delivery. Remaining data-quality/rights/language/music gaps are disclosed evidence limitations, not document defects to patch with made-up values.

## Final hashes
- PPTX: `dfdecac561ad62527aae0c37d6735a7b60ff897e860fd45d66629c85d8f7e480`
- DOCX: `5f85e6b342ddc3cb824973f2c3578636a5598550d9ead26efd8bae03188234f0`