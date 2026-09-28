"""C.13 closure wave — server-derived key scoping + provenance
separation + TTL enforcement package.

Owner ruling 2026-09-19T~17:54Z item (b) verbatim:
    "A tightly-scoped C.13 closure wave before the memory layer. I can't
     confirm closed — there's no evidence on disk, and nothing in this
     programme closes by assertion. Scope: server-derived keys from
     (tenant, run, objective) with cross-key reads refused; provenance
     separated from content and immutable; TTL enforcement. Tests
     first, then seal."

Canon 8 §W11 structural role separation preserved:
  - key_derivation.py: derive_scoped_key ONLY (pure sha256 derivation)
  - provenance.py: shape re-export ONLY (delegates to contracts/*)
  - ttl.py: is_expired predicate ONLY
  - read_refusal.py: assert_scoped_key_matches_expected + refusal
    exception type ONLY

Additive-only per SO §3.8. Not TCB (owner-outstanding · defers to
memory layer boundary).
"""

__all__: tuple[str, ...] = ()
