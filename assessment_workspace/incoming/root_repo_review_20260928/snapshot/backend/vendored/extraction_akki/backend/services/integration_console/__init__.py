"""services.integration_console · Integration Console (Canon 7 §28).

MILESTONE 8 (M17) second sub-wave · scope: deterministic
key-issuance surface for the reference-application-on-issued-key
model per STATE/AUTONOMOUS_RUN_PLAN.md §11 verbatim ("Reference
application on the Integration-Console-issued-key model (Canon 7
§28)").

Sub-modules land wave-by-wave per M17.md sub_wave_order:

    W1 (sealed · code head `16ca02c4`): contracts/application_contract_v0.py
    W2 (this wave):                     services/integration_console/key_issuance.py
    W3 (pending):                       services/personal_client/session.py + contracts/personal_client_session_v0.py
    W4 (pending):                       services/personal_client/governance_invariants.py
    W5 (pending):                       tests/invariants/test_m17_w5_seal_integration.py

Canon 8 §W11 structural role separation is preserved: this
package hosts ONLY the deterministic key-issuance surface.  It
MUST NOT persist keys (persistence stays at M11 tenant DBs
consumed by W3); MUST NOT compose sessions (W3); MUST NOT sign
session tokens (signing stays under sealed M12b-W1 primitive at
any authoring point that requires it, not at issuance).  All
three separations are AST-enforced by the M17-W2 invariant test
file.

SO §3.8 thin-kernel additive-only: this package is a new tree;
no sealed module is edited.
"""
