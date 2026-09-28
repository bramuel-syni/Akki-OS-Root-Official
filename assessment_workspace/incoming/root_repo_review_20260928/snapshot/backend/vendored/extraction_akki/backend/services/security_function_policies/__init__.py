"""services.security_function_policies · net-new backend package · G5-v5 SFP-1..7 first slice.

Package marker for the Security Function Policies vocabulary and scanners.
Registers rule-text-derived load-bearing `Final[...]` constants for SFP-1..7
and pure-data-in grep-negative scanners where the rule text explicitly
negates a specific behavior.

Ruling 5 authority (v5 SRR sheet only · sha256 `00072c58…`).
Owner ruling verbatim (2026-09-20T~23:12Z · this session): "canon_ref = v5
SRR only, class column bounded hint (V1→golden-input, V2→scan, V5→injection)
where the rule text already demands that shape; rule text governs; V7 rows
authored from rule text, never from the column."

Standing bounds: additive-only per SO §3.8 · zero remote configured ·
terminal `pytest` only · closed-vocab per SO §3.10-α.
"""
