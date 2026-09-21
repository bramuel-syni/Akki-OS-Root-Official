"""KMS package · M13-W2 tier-2 standards · §6.4 pre-ruling 4 verbatim.

Structural role separation (Canon 8 §W11 · one-task-one-identity):

- `envelope.py` — wraps/unwraps DEKs and encrypts/decrypts data under
  a per-tenant master key. Does NOT mint master keys.
- `tenant_key_registry.py` — mints and lists per-tenant master keys.
  Does NOT wrap data.
- `rotation_scheduler.py` — schedules and executes 90-day rotations.
  Does NOT decrypt data.

AST invariants enforce these bans at
tests/invariants/test_m13_w2_kms_envelope_and_rotation.py.
"""
