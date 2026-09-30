# Intermediate representation — two layers

## Layer 1: the content model (`content.json`)

The single source of every fact, figure and claim. Shared by every output.

| Block | ID pattern | Required fields | Notes |
|---|---|---|---|
| receipts | `R01` | `resolves_to` | Where a number resolves to; replaces "Source:". Specific enough that someone could go and find it. |
| facts | `F001` | `label value unit class receipt` | `class` is measured / estimated / sample. |
| series | `S001` | `label categories values unit class receipt` | `values` is `{series_name: [..]}`; drives charts and tables. |
| options | `O1` | `name class receipt` + fields | Compared side by side; never a marked winner. |
| calculations | `K001` | `label formula inputs unit` | Arithmetic over facts (`F003 - F001`) or option fields (`option.capex`). Evaluated by the resolver and mirrored as live formulas in the workbook. |
| claims | `C001` | `text supports` | Sentences with references inside; `supports` lists the IDs that back them. |
| coverage | — | `covers cannot_say[]` | Feeds the mandatory coverage-and-limits page. |

Units known to the formatter: `GBPm GBP pct pp m FTE months years`. Add
others in `studio.fmt_value` so every format agrees on presentation.

## Reference grammar inside text

| Token | Resolves to |
|---|---|
| `{F003}` | the fact, formatted by its unit (`£142.3m`) |
| `{K001}` | the calculation, formatted by its unit (`20.2%`) |
| `{K004:min}` `{K004:max}` | min/max of an option-level calculation across its option inputs |
| `{C001}` | the claim's text, itself resolved |
| `{O1.headcount_delta}` | an option field |
| `{F006:F007:ratio}` | F006 / F007 as a percentage |
| `{content.title}` | a top-level content field |

An unresolvable token fails the resolve step. A literal number typed into a
spec outside these tokens is a validation blocker (`validate.py`
`retyped_numbers`), with narrow exemptions for dates, fiscal years, document
IDs and ordinals.

## Layer 2: format specs

One per output, each referencing the content model by `content_ref`
(`content_id@version`), the brief and the verdict. They hold structure and
pointers only.

- **deck.json** — slides, each of a type the voice lays out: `cover`,
  `exec_summary`, `section`, `assertion_exhibit`, `assertion_points`,
  `comparison`, `coverage_limits`, `appendix`, `hero`, `big_number`, `closing`.
  A voice lays out only the types it lists in `layouts`; using a type the
  voice does not lay out fails at resolve time.
- **paper.json** — sections of blocks: `para`, `figure`, `table`,
  `options_table`, `coverage_limits`, `receipts`.
- **workbook.json** — sheets of kinds: `cover`, `inputs`, `options_model`,
  `series`, `checks`.

Every spec carries `seed` and `build_stamp`. Two specs from one commission
share the seed so they share the look.

## The resolved plan

`scripts/studio.py` turns spec + content + brief + verdict + theme + voice
into `<type>.resolved.json`: every token substituted, every zone in inches,
every colour and font literal, every exhibit's backend chosen, the input file
hashes recorded. Renderers read only this. It is the frozen specification the
determinism contract is about.

## Cross-format transforms

A deck-to-paper or deck-to-workbook conversion is a spec-to-spec mapping over
the same content model, not a layout transplant. Findings become paragraphs
with their figures; option tables become a live model with the derivation as
formulas; receipts become the appendix in both. Write the new spec; the
content model does not change.
