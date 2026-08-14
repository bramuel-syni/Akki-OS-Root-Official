/**
 * plugins/ip-allowlist/check.js — pure SPINE_ALLOWED_IPS decision function.
 *
 * Owner stop-order 2026-08-14: the same trust-boundary math the FastAPI
 * middleware applies. This module contains no I/O and is safe to test
 * with vanilla `node --test`. The craco-dev-server middleware in
 * ../middleware.js is a thin adapter over it.
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
      .filter((p) => p.length > 0)
  );
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

function refuse() {
  return {
    allowed: false,
    status: 403,
    body: REFUSAL_SENTENCE,
    contentType: "text/plain; charset=utf-8",
  };
}

function allow() {
  return { allowed: true };
}

function check(headers, env) {
  const allowlist = parseAllowlist(env ? env.SPINE_ALLOWED_IPS : undefined);
  const hops = trustedProxyHops(env ? env.SPINE_TRUSTED_PROXY_HOPS : undefined);
  const xff = headers ? headers["x-forwarded-for"] : undefined;
  const clientIp = extractTrustedClientIp(xff, hops);
  if (allowlist.size === 0) return refuse();
  if (!clientIp) return refuse();
  if (!allowlist.has(clientIp)) return refuse();
  return allow();
}

module.exports = { check, REFUSAL_SENTENCE };
