"""services.answering_service.webhook_delivery · signed webhook delivery.

MILESTONE 5 · M14-W4 · new module authored at CP-M14-W4.

Design (owner tier-1 ruling · direct analogy to Option-D on DAP-7 ·
"a code path is a code path"):

    PURE DATA-IN. The answering-service NEVER holds a signing
    capability — not a key, not a callable, not a partial. What crosses
    into this module is inert data (payload_ref + signature bytes).
    The signing act stays physically inside the Watch trust boundary.

Canon anchors:
- **Canon 17 §4** verbatim: answering-service triangle: ask · delivery
  · webhook_endpoint. Every delivery carries a signature that binds the
  delivered payload to the tenant.
- **Canon 8 §W10** (watcher-watched-from-outside): the Watch signature
  primitive is Watch-trust-boundary-only. This module:
    - CANNOT import `services.watch.signature_primitive` (module ban ·
      AST-enforced by test 6 of M14-W4 + test 7 of M14-W4 + the global
      trust-boundary invariant `test_ed25519_keys_are_held_only_by_
      watch_trust_boundary` in test_m12b_w1_ed25519_primitive_
      determinism.py).
    - CANNOT accept any parameter that could be a signer callable or a
      key (AST-enforced by test 7 of M14-W4 · closed banned-parameter-
      name tuple + no `Callable` import + no `signature_primitive`
      reference).
- **Canon 8 §W11** (one-task-one-identity): structural role separation.
  This module attaches an opaque signature; it does NOT sign, does NOT
  hold keys, does NOT wrap / unwrap KMS envelopes (envelope operations
  stay at `services.kms.envelope` · AST-enforced by test 6 of M14-W4).
- **Canon 8 §Line 31** ("signature is the guard"): verify-side is a
  predicate over `canonical_delivery_bytes(delivery)` and returns
  True / False · never raises.
- **BR-2.1 alignment**: the signing capability physically does not
  cross into answering-service. Enforcement is structural (bytes-in),
  not conventional. Callers inside the Watch trust boundary compute
  canonical bytes via `canonical_bytes_for_delivery(...)`, sign once,
  and pass the resulting `signature: bytes` here.
- **Retry semantics**: the caller redelivers the same (canonical bytes,
  signature) pair across attempts. Attempt metadata (retry counters,
  next-attempt timestamps) lives OUTSIDE the signed envelope. The
  signed 6-field tuple (`delivery_id`, `tenant_id`, `ask_id`,
  `webhook_endpoint_id`, `payload_ref`, `delivered_at`) is fixed per
  `delivery_id`.
- **SO §3.8** (thin-kernel additive-only): new module surface
  consuming sealed pre-M14 surfaces without editing.
- **SO §3.10-α** (closed-schema discipline): canonical bytes are
  deterministic sorted-key JSON over the closed 6-field
  `_SIGNATURE_BEARING_FIELDS` tuple. `Delivery_v0` itself is
  extra=forbid + frozen=True at collections.deliveries.
"""
from __future__ import annotations

import json
from typing import Any, Dict

# CANON 8 §W10 STRUCTURAL BAN (AST-enforced by M14-W4 tests 6 + 7 and
# by the global trust-boundary invariant):
#   - DO NOT `import services.watch.signature_primitive`.
#   - DO NOT `from services.watch.signature_primitive import ...`.
#   - DO NOT accept any signer / key / callable-shaped parameter.
# CANON 8 §W11 STRUCTURAL BAN (AST-enforced by M14-W4 test 6):
#   - DO NOT `import services.kms.envelope`.
#   - DO NOT `from services.kms.envelope import wrap_dek | unwrap_and_decrypt`.

from services.answering_service.collections.asks import Ask_v0
from services.answering_service.collections.deliveries import Delivery_v0
from services.answering_service.collections.webhook_endpoints import (
    WebhookEndpoint_v0,
)


# Signature-bearing fields · closed tuple · SO §3.10-α. Canonical bytes
# are deterministic sorted-key JSON over these fields ONLY. Excludes
# `signature` (chicken-and-egg) and `state` (set post-signing).
_SIGNATURE_BEARING_FIELDS: tuple[str, ...] = (
    "delivery_id",
    "tenant_id",
    "ask_id",
    "webhook_endpoint_id",
    "payload_ref",
    "delivered_at",
)


def canonical_delivery_bytes(delivery: Delivery_v0) -> bytes:
    """Return canonical bytes over the 6 signature-bearing fields of a
    constructed `Delivery_v0`.

    Deterministic sorted-key JSON. Same bytes across runs and machines.
    Excludes `signature` (chicken-and-egg) and `state` (post-signing).
    """
    doc = delivery.model_dump()
    filtered: Dict[str, Any] = {
        k: doc[k] for k in _SIGNATURE_BEARING_FIELDS if k in doc
    }
    return json.dumps(filtered, sort_keys=True, ensure_ascii=True).encode(
        "utf-8"
    )


def canonical_bytes_for_delivery(
    *,
    delivery_id: str,
    tenant_id: str,
    ask_id: str,
    webhook_endpoint_id: str,
    payload_ref: str,
    delivered_at: str,
) -> bytes:
    """Return the same canonical bytes given the 6 signature-bearing
    fields directly · pre-Delivery-construction · avoids chicken-and-
    egg with `signature`.

    Callers inside the Watch trust boundary compute these bytes, sign
    them once with the tenant's Ed25519 signing key, and pass the
    resulting signature into `deliver_webhook(...)` as `signature:
    bytes` (inert data).
    """
    filtered = {
        "delivery_id": delivery_id,
        "tenant_id": tenant_id,
        "ask_id": ask_id,
        "webhook_endpoint_id": webhook_endpoint_id,
        "payload_ref": payload_ref,
        "delivered_at": delivered_at,
    }
    return json.dumps(filtered, sort_keys=True, ensure_ascii=True).encode(
        "utf-8"
    )


def deliver_webhook(
    *,
    ask: Ask_v0,
    endpoint: WebhookEndpoint_v0,
    payload_ref: str,
    signature: bytes,
    delivery_id: str,
    delivered_at: str,
) -> Delivery_v0:
    """Attach an opaque signature to a `Delivery_v0` record.

    PURE DATA-IN per Canon 8 §W10 + BR-2.1. This module does NOT sign,
    does NOT hold keys, and accepts NO callable / signer / key
    parameter. The caller (inside the Watch trust boundary) MUST have
    signed `canonical_bytes_for_delivery(...)` over the exact
    signature-bearing fields with the tenant's Ed25519 signing key and
    pass the resulting signature bytes here.

    The signature is stored hex-encoded on the `Delivery_v0` row
    (`signature` field). Verification uses
    `services.watch.signature_primitive.watch_verify(pub_bytes,
    canonical_delivery_bytes(delivery), bytes.fromhex(
    delivery.signature))` — Canon 8 §Line 31 predicate.

    Cross-tenant guard: `ask.tenant_id` MUST equal `endpoint.tenant_id`
    (enforced at the module level · refused with ValueError).
    """
    if ask.tenant_id != endpoint.tenant_id:
        raise ValueError(
            f"M14-W4 · cross-tenant delivery refused · "
            f"ask.tenant_id={ask.tenant_id!r} != "
            f"endpoint.tenant_id={endpoint.tenant_id!r}"
        )

    return Delivery_v0(
        delivery_id=delivery_id,
        tenant_id=ask.tenant_id,
        ask_id=ask.ask_id,
        webhook_endpoint_id=endpoint.webhook_endpoint_id,
        state="sent",
        signature=signature.hex(),
        payload_ref=payload_ref,
        delivered_at=delivered_at,
    )
