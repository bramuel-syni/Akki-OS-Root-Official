"""services.enforce · M11-W3 · thin-adapter gate layer.

Canon anchors (verbatim):
  R-18 Tension (a) Option C (owner-ruled 2026-09-17T~15:45Z) · thin adapter:
    "Adapters at services/enforce/<entity>_gate.py (W3+) call the paired
    M9 refuser first, then a Repository op."
  v1.0 B.2 · Every data-plane access via services.data.repository.

Each `<entity>_gate.py` is the ONLY surface permitted to dual-import
`services.data.repository` AND a `services.platform_control_plane.*`
refuser — enforced by
`backend/tests/invariants/test_m11w1_data_layer_sole_motor_importer.py::
test_m11w1_enforce_gate_is_sole_dual_importer_surface`.

W3 scope (control-plane · 10 entities):
  tenant, workspace, user, role_assignment, service_account, role_registry,
  session_binder, break_glass_session, audit_event, audit_event_types.
"""
