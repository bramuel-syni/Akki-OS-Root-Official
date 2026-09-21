"""services.cif · CIF (Conditioned Ideation Faculty · Doc-9).

MILESTONE 7 (M16) opens the CIF sub-tree per SO §6.4 pre-ruling
verbatim ("M16 CIF scope — ruled now, since it moves the number
most.  CIF is built as canon already defines it: a learned ideation
faculty outside the TCB; every CIF-originated idea passes a
deterministic acceptance point before affecting anything (BR-9.2,
single-experiment principle); CIF proposes and never ratifies
(AC-18); its outputs enter the research loop (A5.22, L-4) and the
capability register (A20.16, L-5); it has its own halt independent
of the Targeta run it feeds (DET-1 closed as a MUST-DO).  Nothing
beyond that in M16.").

Sub-modules land wave-by-wave per M16.md sub_wave_order:

    W1 (sealed · code head `ff000d58`): contracts/cif_proposal_v0.py
    W2 (this wave):                     services/cif/detection.py
    W3:                                 services/cif/acceptance_point.py
    W4:                                 services/cif/output_routing.py
    W5:                                 services/cif/halt.py

SO §3.8 thin-kernel additive-only: this package is a new tree; no
sealed module is edited.
"""
