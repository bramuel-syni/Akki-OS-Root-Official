# Registers by objective — families, voices, libraries

Index the library by what the document must *do*, not by whose style it
resembles. "McKinsey-type" and "Accenture-type" are voices inside families.

## Objective → family → structural defaults

| Objective | Family | Structural defaults | Voices (curated) |
|---|---|---|---|
| decide | strategy | assertion titles, one exhibit per slide, SCQA executive summary, coverage-and-limits, appendix with receipts | **strategy-house** (built), boutique (dense frameworks, 2×2s) |
| persuade | pitch | hero numbers, proof points, momentum arc, imagery slots | tech-consultancy (bold sans, one hot accent), founder (dark, large type) |
| report | dashboard | status boards, RAG, Harvey balls, dense tables, variance | ops-grid, finance-ledger |
| explain | editorial | progressive build, diagrams, stepwise reveal | textbook, field-guide |
| inspire | keynote | one line per slide, full-bleed structure field on statement slides, big-number slots, minimal furniture | **keynote-cinematic** (built), editorial-poster |
| align | workshop | timelines, swimlanes, RACI, decision logs | facilitator, PMO |
| document | dossier | numbered sections, reference tables, appendices | legal, assurance |

Two voices exist in code: `strategy-house` (decide) and `keynote-cinematic`
(inspire/persuade). They sit at opposite ends of the density and type-scale
range, and the same content model renders in both with no renderer change,
which is the test the grid had to pass. Build `dashboard` next (dense, tabular),
then the rest.

The two fixtures demonstrate a CIF re-entry: the "Future-state" direction was
deferred on the board pack with a named condition; the all-hands brief met the
condition and the direction re-entered and was adopted (`fixtures/launch-keynote/verdict.json`).

## A voice file declares

- `structural`: title style and length, exhibits per slide, words per slide,
  required slide types, whether a winner may be marked, whether so-what is
  required.
- `grid` and `layouts`: 12 columns × 16 rows; zones per slide type in grid
  units. Change layout here, never in a renderer.
- `compatibility`: allowed palettes and type pairs from the theme's variation
  space, and `veto` combinations with a stated reason. The resolver steps
  deterministically past a veto.
- `plate_policy`: per plate, the backend per output format and whether the
  delivered object is editable.

## Libraries the direction stage assembles from

| Library | Examples | Where |
|---|---|---|
| Narrative patterns | recommendation-and-evidence; problem-and-solution; progress-and-exceptions; learning-and-practice; vision-then-journey | `verdict.candidates[].assembly.narrative` |
| Page compositions | cover, exec summary, section, assertion+exhibit, assertion+points, comparison, coverage-and-limits, appendix; (to add) hero statement, editorial spread, process, dense reference | voice `layouts` |
| Information graphics | plates in `plates.md` | voice `plate_policy` |
| Visual treatments | palettes, type pairs, cover compositions, divider treatments | theme `variation_space` |
| Experience features | speaker notes, section summaries, navigation, workbook legend | renderer features, declared per voice |

A direction is an *assembly* of one item from each library that the
compatibility rules permit. The model chooses the assembly; it does not
invent items. That is what keeps the output seasoned: the ingredients are
curated, the combination is chosen for the brief, and the seed settles the
remaining free choices repeatably.

## The house

`themes/house-neutral.json` holds the constant core (number font, number
formats, furniture, safe fonts) and the variation space. Every output is
recognisably the house because the core never varies; no two commissions look
templated because the seed and the direction vary the rest. Encode a client's
brand as a new theme with the same shape.
