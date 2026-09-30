# The determinism contract

Three promises, kept separately because they need different machinery.

| Promise | Meaning | Kept by |
|---|---|---|
| 1. Content consistency | The same approved facts, calculations and claims appear across every output | The content model and ID-linked references. Specs cannot hold values; `validate.py` blocks retyped numbers; the workbook's Checks sheet cross-checks formulas against the resolver's calculations. |
| 2. Layout repeatability | The frozen specification produces the same layout in a defined rendering environment | The resolved plan: every zone, colour, font and backend is literal before any renderer runs. Renderers make no decisions. |
| 3. Binary reproducibility | Rebuilding produces byte-identical files | `freeze.py`: normalise every OOXML package (sorted entries, fixed zip timestamps, `docProps` stamped with `build_stamp`, `TotalTime` zeroed) *recursively* — chart data workbooks embedded in a pptx carry their own timestamps — then hash. `build.py --prove` builds twice and asserts equality. |

## What has to be pinned for promise 3

- `build_stamp` in every spec: the timestamp written into the files.
- `seed`: settles every free choice in the variation space.
- Dependency versions: recorded in `build-manifest.json` (python-pptx,
  python-docx, openpyxl, matplotlib, LibreOffice). A different LibreOffice
  can recalculate to different bytes; the manifest makes that visible.
- Fonts: names only are written into the files; the reader's Office renders
  them. The theme's safe list keeps QA text-fit estimates honest.
- Chart images (docx PNG, html SVG) are produced with metadata stripped and a
  fixed `svg.hashsalt`, so they repeat within a matplotlib version.

Verified on the board-pack fixture: four outputs, two builds, identical
hashes, including the workbook after a LibreOffice recalc.

## Freeze also means "don't reinterpret"

The resolved plan, the verdict and the build manifest are deliverables.
Revisions create a new content version, a new resolved plan and a new
manifest; nothing is edited in place and nothing is regenerated from the
original prompt. Generated images are kept with the build, not re-drawn.

## Where creativity and determinism meet

The direction stage is non-deterministic by design and happens once, before
the freeze. After the verdict is recorded, the whole path is code. The seed
gives freshness *between* commissions without any variation *within* a
commission's rebuilds.
