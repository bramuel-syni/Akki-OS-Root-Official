"""services.gateway · M11-W2 · gateway-signed context header package.

Canon anchors (verbatim):
  v1.0 B.1 δ-1: gateway-signed X-Akki-Context header (HMAC-SHA256).
  v0.2 §3.1 + §4.3: gateway resolves tenant_id from authenticated session
  and injects on every request; clients cannot supply it.
"""
