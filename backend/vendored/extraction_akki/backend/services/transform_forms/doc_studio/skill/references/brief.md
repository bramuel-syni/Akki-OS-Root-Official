# The brief — six dimensions

Capture all six before proposing a direction. A brief is `brief.json`
(schema: `schemas/brief.schema.json`). The direction manifest cites brief
fields as its sources, so what you write here is what flip detection watches.

| Dimension | What it determines | Field |
|---|---|---|
| Purpose | The decision, understanding or action the document must enable. One of: decide, persuade, report, explain, inspire, align, document. | `purpose.kind`, `purpose.statement` |
| Audience | Knowledge of the subject, what they prioritise, expected level of detail | `audience.*` |
| Use setting | Live presentation, unattended reading, workshop, printed, ongoing operational use, minutes available | `setting.*` |
| Content | What material exists: evidence, narrative, financial, diagrams, imagery, appendix | `content.*` |
| Brand and tone | Which house, formality, expressiveness, how much variation is allowed | `brand.*` |
| Output requirements | Formats, roles, editability, navigation, delivery constraints | `outputs[]`, `constraints` |

## Why the setting is its own dimension

The same facts for the same board produce different documents when the pack
is emailed ahead versus presented live. Unattended reading needs printed
so-what lines and a paper; a live pitch needs pacing and fewer words per
slide. Printing forbids full-bleed fields and dark backgrounds on content
pages. These are manifest-level assumptions (see `directions.md`), which is
why they must be captured explicitly rather than inferred later.

## What to ask when the brief is thin

Ask one question at a time and prefer the question whose answer changes the
direction most: usually setting, then audience priorities. Do not ask about
palette, fonts or layout; those are chosen by the voice and the seed.
