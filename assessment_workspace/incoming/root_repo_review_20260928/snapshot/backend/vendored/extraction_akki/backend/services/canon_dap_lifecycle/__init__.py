"""services.canon_dap_lifecycle · G5-v5 Family C DAP lifecycle and principal model.

Registers `Final[...]` load-bearing vocabulary for DAP rows in the v5 Master
Requirements Registry · System Rules Registry sheet (sha-pinned custody
workbook sha256 `00072c5829d3d89399cc5ca64661b405ac8a3cd0b43d0081f0d5f0bce109619d`).

Family C first sub-slice registers Tier A (`dap_backend_spec_v1`-sourced ·
SRR rows 315..344 · DAP-1..DAP-30 · admission-and-metering base rules ·
domain `DAP (composition — see Doc 0 Component 17)`).

Tier B sub-slices follow:
- DAP-31..36 (Security Amendments · Trojan Whisper · SRR rows 349..354 · domain `DAP`)
- DAP-37..38 (Pruning & Unlearning Amendment · SRR rows 473..474 · domain `O13 Data & Intelligence Acquisition`)

## SRR-status disclosure

All 38 DAP rows carry `status=PROPOSED` on the v5 SRR sheet — not CANON.
They are being landed under the owner's explicit G5-v5 sequencing directive
(2026-09-21T~01:00Z at state commit `a30db4f7`) that named DAP-1..38 as the
queue after Family B (Doc 5 Northena) with standing GO through the G5 family
queue. That inclusion is the ratification-by-sequencing signal for the
vocabulary seat; the vocabulary is authored FROM the SRR statement
byte-verbatim per Ruling 3 (rule text governs). The status field is
preserved verbatim as `PROPOSED` in the row-shared metadata so any
downstream row-status audit sees the truth.

Standing bounds: additive-only per SO §3.8 · closed-vocab per SO §3.10-α ·
zero external I/O · deterministic.
"""
