/**
 * plugins/ip-allowlist/check.js — SPINE_ALLOWED_IPS + owner-layer decision.
 *
 * Owner stop-order 2026-08-14: source-IP allowlist replaces token gate.
 * Same trust-boundary math as the FastAPI middleware.
 *
 * W10 interleave (2026-08-26): owner-access path added without weakening
 * governance:
 *   - OWNER_ALLOWLIST_IPS · comma-separated additional IPs layered on
 *     SPINE_ALLOWED_IPS. Admits attributed to `layer: "owner"`.
 *   - ALLOWLIST_MODE=strict|permissive · 'permissive' admits all inbound
 *     (owner demo access) · default 'strict' preserves fail-closed.
 *
 * Every decision returns a `mode` + `layer` attribution so the caller
 * (middleware) can emit a structured log line (nothing silent).
 *
 * Trust boundary (empirical, 2026-08-14 preview topology):
 *   x-forwarded-for = [client-spoofable..., true-client-IP, CF-edge, GCP-LB]
 *   With SPINE_TRUSTED_PROXY_HOPS=2, trusted position is xff[-3].
 */
"use strict";

const REFUSAL_SENTENCE = "This surface answers allowlisted addresses only.";

function parseAllowlist(envValue) {
  if (envValue === undefined || envValue === null) return new Set();
  return new Set(
    String(envValue)
      .split(",")
      .map((p) => p.trim())
      .filter((p) => p.length > 0),
  );
}

function readMode(envValue) {
  if (envValue === undefined || envValue === null) return "strict";
  const norm = String(envValue).trim().toLowerCase();
  return norm === "permissive" ? "permissive" : "strict";
}

function trustedProxyHops(envValue) {
  const n = parseInt(envValue, 10);
  return Number.isFinite(n) ? n : 2;
}

function extractTrustedClientIp(xffHeader, hops) {
  if (!xffHeader) return null;
  const parts = String(xffHeader)
    .split(",")
    .map((p) => p.trim())
    .filter((p) => p.length > 0);
  if (parts.length < hops + 1) return null;
  return parts[parts.length - (hops + 1)];
}

function refuse(mode, clientIp) {
  return {
    allowed: false,
    mode,
    layer: "none",
    clientIp: clientIp || null,
    status: 403,
    body: REFUSAL_SENTENCE,
    contentType: "text/plain; charset=utf-8",
  };
}

function allow(mode, layer, clientIp) {
  return { allowed: true, mode, layer, clientIp: clientIp || null };
}

function check(headers, env) {
  const e = env || {};
  const mode = readMode(e.ALLOWLIST_MODE);
  const hops = trustedProxyHops(e.SPINE_TRUSTED_PROXY_HOPS);
  const xff = headers ? headers["x-forwarded-for"] : undefined;
  const clientIp = extractTrustedClientIp(xff, hops);

  // Permissive mode: admit everything · attributed to permissive layer
  // so audits distinguish it from strict admits.
  if (mode === "permissive") {
    return allow("permissive", "permissive", clientIp);
  }

  // Strict mode: fail-closed against composed allowlist.
  const spine = parseAllowlist(e.SPINE_ALLOWED_IPS);
  const owner = parseAllowlist(e.OWNER_ALLOWLIST_IPS);
  const composed = new Set([...spine, ...owner]);

  if (composed.size === 0 || !clientIp) {
    return refuse("strict", clientIp);
  }

  // Owner layer first (owner rulings dominate spine config in audit).
  if (owner.has(clientIp)) return allow("strict", "owner", clientIp);
  if (spine.has(clientIp)) return allow("strict", "spine", clientIp);
  return refuse("strict", clientIp);
}

module.exports = { check, REFUSAL_SENTENCE };
