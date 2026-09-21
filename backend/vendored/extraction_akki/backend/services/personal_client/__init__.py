"""services.personal_client · Personal Client tenant-of-one surface (C.23).

MILESTONE 8 (M17) third sub-wave · scope: session composition +
ask emission surface for the personal-client-as-reference-application
built on the Integration Console issued-key model.

Sub-modules land wave-by-wave per M17.md sub_wave_order:

    W1 (sealed · code head `16ca02c4`):     contracts/application_contract_v0.py
    W2 (sealed · code head `a84e5986`):     services/integration_console/key_issuance.py
    W3 (this wave):                         services/personal_client/session.py + contracts/personal_client_session_v0.py
    W4 (pending):                           services/personal_client/governance_invariants.py
    W5 (pending):                           tests/invariants/test_m17_w5_seal_integration.py

Canon 8 §W11 structural role separation is preserved: this
package hosts ONLY the session composition + ask emission surface.
It MUST NOT import any principal-data / user-memory surface
(R-21 hard ban until owner ruling); MUST NOT expose any decision
surface (AC-18); MUST NOT import learned/model-client surfaces
(Canon 4 §22 rung-1 discipline extended to client surface). All
three separations are AST-enforced by the M17-W3 invariant test
file.

SO §3.8 thin-kernel additive-only: this package is a new tree;
no sealed module is edited.
"""
