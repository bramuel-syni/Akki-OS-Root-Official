# Exhibit plates and backend policy

Chart choice is message-driven. Say what the exhibit must show; the plate
follows. Construction law for the full set of 17 plates is in the companion
skill `akki-decks/references/plates-and-registers.md`; this file adds the
backend and editability policy the studio enforces.

| Message | Plate | pptx backend | docx / html | Editable in Office | Status |
|---|---|---|---|---|---|
| comparison across categories | bar | native chart | PNG / SVG | yes | built |
| trend over time | line | native chart | PNG / SVG | yes | built |
| composition | stacked_bar | native chart | PNG / SVG | yes | policy only |
| change from A to B | waterfall | native stacked bar with transparent base (python-pptx has no waterfall type) | PNG / SVG | yes, fragile | policy only |
| options side by side | comparison_table | native table | table | yes | built |
| one figure that matters | big_number | shapes + text | text | yes | built |
| qualitative scoring | harvey | shapes | SVG | yes | policy only |
| cause structure | driver_tree | shapes + connectors | SVG | yes | policy only |
| share × size | mekko | SVG image | SVG | **no** | policy only |
| sequence / seam | flow | SVG image | SVG | **no** | policy only |

## The rule

If PowerPoint can hold the form natively without hacks, deliver it native and
editable. Otherwise deliver native shapes if the form is geometric, or an SVG
image if it is not, and declare `editable: false`. A brief that requires
everything editable and a spec that asks for a non-editable plate is a
composition problem, not a rendering problem: change the plate or split the
message. Never degrade silently to a picture.

## Universal overlays, every plate, every format

- figure class printed at the exhibit: `[measured]`, `[estimated]`, `[sample]`
- receipt line: `Receipt R02: <what it resolves to>`
- so-what line where the voice requires it
- unmeasured territory hatched with a caption, never blank
- one accent colour per exhibit, reserved for the point being made
