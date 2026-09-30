# Reproducibility contract
| Operation | Contract | Canon |
|---|---|---|
| Resolve | Identical resolved plan from identical versioned inputs | DR-R2 |
| Render (pptx, docx, xlsx, html) | Byte-identical files in the fixed build environment; OOXML normalised recursively (embedded chart workbooks included); proven by `build.py --prove` | DR-R2, gate_determinism |
| Recalc | LibreOffice output normalised; version pinned in build-manifest | — |
| Chart images | matplotlib PNG/SVG with metadata stripped and fixed hashsalt; repeat within a matplotlib version | — |
Volatile fields (timestamps, TotalTime) are stamped from `build_stamp` or zeroed before hashing.
