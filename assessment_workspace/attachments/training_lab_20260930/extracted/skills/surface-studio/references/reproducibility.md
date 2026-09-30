# Reproducibility contract
| Operation | Contract | Canon |
|---|---|---|
| Resolve | Identical content plan from identical versioned inputs | DR-R2 pattern |
| Assemble | Byte-identical content record and preview for the same cache key (page-state hash, role, voice, spec hash, policy version); proven by `build.py --prove` | #19 warm-serve; template 1.0 |
| Serve | Same key → same bytes; regeneration only on key change | #19/#20 |
No wall-clock timestamps enter the record; `as_of` comes from the page state and `build_stamp` from the spec.
