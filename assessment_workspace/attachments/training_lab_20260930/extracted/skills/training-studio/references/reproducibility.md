# Reproducibility contract
| Operation | Contract | Canon |
|---|---|---|
| Resolve | Identical resolved plan from identical versioned inputs (hash-checked in build-manifest) | DR-R2 pattern |
| Stub run | Content-identical run record across builds; volatile fields (run_id) excluded from the hash | template 1.0 |
| Real run | Seed-fixed re-run within tolerance: accuracy ±0.002, coverage ±0.002 (policy); hashes recorded, never asserted equal | C.8 standard training criteria; C.20.10 reproducibility test; PyTorch does not guarantee bitwise determinism across releases or CPU/GPU |
| Report | Identical bytes from an identical run record | — |
`build.py --prove` applies the stub contract to stub builds and the tolerance contract to real builds.
