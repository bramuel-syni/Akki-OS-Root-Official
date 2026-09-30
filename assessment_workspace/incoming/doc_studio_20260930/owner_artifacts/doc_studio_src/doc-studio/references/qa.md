# QA — mechanical blockers and editorial review, kept apart

## Blockers (measurable; fail the build or the release)

Before rendering (`validate.py`):
- schema failures on any input file
- an unresolvable reference, or a literal number typed into a spec
- an exhibit without a receipt or without a figure class
- a title over the voice's character limit
- a voice-required slide missing (executive summary, coverage-and-limits, appendix)
- a comparison that marks a winner in a voice that forbids it
- a verdict with no confirmer, or whose adopted id is not an adopted candidate

After rendering (`qa.py`):
- OOXML validation failures (the pptx/docx skills' validators)
- pptx text that does not fit its box, estimated from font metrics with 10% slack on serifs
- any formula error after recalc; any `MISMATCH` on the workbook's Checks sheet

## Review (judgment; never auto-fixed)

Emitted in `validate-report.json` as questions:
- Read only the titles in order: do they tell the whole story?
- Does each exhibit prove its title, or decorate it?
- Is each title a full-sentence assertion? (heuristic flag, not a rule)
- Is a slide dense enough that it should split?
- Does the paper stand alone when read unattended?
- Are the key assumptions the reader would want to change the ones highlighted?

A reviewing agent answers these against the thumbnails and returns *edits to
the specs*, never edits to the rendered files.

## Repair bounds

At most three repair passes per build. Each pass is a spec or voice change,
then a full rebuild. If blockers remain after three, stop and report them;
do not shrink fonts, do not drop the coverage page, do not hand-edit XML.

## Visual QA

Render thumbnails (`soffice --convert-to pdf` then `pdftoppm`) and look at
every page fresh. Overflow and collisions are the commonest defects and are
always user-visible. A layout defect is fixed in the voice's grid layouts so
it is fixed for every future commission, not on the slide.
