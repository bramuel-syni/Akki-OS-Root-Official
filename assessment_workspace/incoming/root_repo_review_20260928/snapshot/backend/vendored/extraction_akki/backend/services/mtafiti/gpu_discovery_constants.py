"""Mtafiti GPU-Discovery pinned constants.

W-MTAFITI-GPU-DISCOVERY · CP1 kernel.

Owner ruling this session (banked in STATE/DECISIONS.md · CP1 defaults):

  MTAFITI_GPU_SAMPLING_SEED = 20260909
    Traceable to the ruling date (2026-09-09 evening); used everywhere
    the adaptive walker draws pseudo-random samples so C4-013
    repeatability is preserved.

  POLICY_ID = "mtafiti-gpu-discovery-v1"
    The pinned sampling-policy identifier — every emitted manifest
    carries it verbatim so an auditor can re-derive the walk from
    (seed, policy_id, inputs).

Neither constant is derived from wall-clock, os.environ, or any live
signal. They are laws, not defaults.
"""
from __future__ import annotations


MTAFITI_GPU_SAMPLING_SEED: int = 20260909
"""Ruling-date-anchored pseudo-random seed. C4-013 repeatability."""


POLICY_ID: str = "mtafiti-gpu-discovery-v1"
"""Pinned sampling-policy identifier — banked in DECISIONS.md."""


MTAFITI_PII_HASH_SALT: str = "mtafiti-gpu-discovery-v1-pii-hash-salt-20260912"
"""Pinned salt for the PII redaction hash. Determinism, not secrecy.

Rotating this constant re-hashes every persisted redaction token — a
deliberate lever, not a bug. If the owner rotates it, all downstream
mtafiti sample manifests must be re-derived. C4-013 preserved by the
salt being a value, not a wall-clock read.
"""
