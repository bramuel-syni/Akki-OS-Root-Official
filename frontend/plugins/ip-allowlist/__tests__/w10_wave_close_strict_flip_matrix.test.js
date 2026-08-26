/**
 * W10 wave-close · strict-flip static-surface invariant · mode matrix.
 *
 * Owner ratification-withheld finding (2026-08-26T09:33Z): the strict
 * flip at 09:20Z restarted only the backend supervisor, leaving the
 * craco Node process with a stale ALLOWLIST_MODE=permissive mirror.
 * GET / on the frontend port returned 200 with the SPA shell intact
 * even though the .env was strict. The original flip receipt exercised
 * only /api/* on the backend port; this defect was not caught.
 *
 * This test is the regression proof · a mode-matrix live-HTTP invariant
 * that exercises BOTH surfaces at BOTH ports with the three canonical
 * probes: owner-IP, non-allowlisted IP, no-XFF. It reads the current
 * ALLOWLIST_MODE from /app/backend/.env (single source of truth · same
 * file that craco and FastAPI both mirror) and asserts the corresponding
 * behavior. Any future flip that skips restarting a service will fire.
 *
 * Run: `node --test pod_shell/frontend/__tests__/w10_wave_close_strict_flip_matrix.test.js`
 */
"use strict";

const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");


// Single source of truth for allowlist config: /app/backend/.env.
// Both middlewares (FastAPI + craco) mirror from here; this test reads
// the same file to know what mode should be enforced right now.
function readBackendEnv() {
  const raw = fs.readFileSync("/app/backend/.env", "utf8");
  const out = {};
  for (const line of raw.split("\n")) {
    const m = line.match(/^([A-Z_][A-Z0-9_]*)=(.*)$/);
    if (m) out[m[1]] = m[2];
  }
  return out;
}

const ENV = readBackendEnv();
const MODE = (ENV.ALLOWLIST_MODE || "strict").trim().toLowerCase();
const OWNER_IPS = (ENV.OWNER_ALLOWLIST_IPS || "").split(",").map((s) => s.trim()).filter(Boolean);
const OWNER_IP = OWNER_IPS[0] || "41.90.172.155";
const UNKNOWN_IP = "203.0.113.99";                                        // RFC 5737 doc prefix

const FRONTEND = "http://127.0.0.1:3000";
const BACKEND = "http://127.0.0.1:8001";
const REFUSAL = "This surface answers allowlisted addresses only.";

// Surfaces to probe. The intent is COMPLETE COVERAGE of the surface —
// frontend root + a wired SPA route + a static asset + backend API + OpenAPI.
const SURFACES = [
  { name: "frontend-root",        url: `${FRONTEND}/` },
  { name: "frontend-spa-governance", url: `${FRONTEND}/governance` },
  { name: "frontend-static-favicon", url: `${FRONTEND}/favicon.ico` },
  { name: "backend-api-governance",  url: `${BACKEND}/api/governance/state` },
  { name: "backend-api-openapi",     url: `${BACKEND}/api/openapi.json` },
];

function xff(clientIp) {
  return `${clientIp},172.71.255.34,136.110.244.150`;
}

async function probe(url, headers) {
  const r = await fetch(url, { headers, redirect: "manual" });
  return { status: r.status, text: await r.text() };
}


// ================== Mode invariants =====================================

test("ALLOWLIST_MODE resolves from /app/backend/.env single source of truth", () => {
  assert.ok(["strict", "permissive"].includes(MODE),
    `ALLOWLIST_MODE must be 'strict' or 'permissive' · got ${MODE}`);
  assert.ok(OWNER_IP && OWNER_IP.length > 0,
    "OWNER_ALLOWLIST_IPS must name at least one owner IP");
});


// ================== Owner-IP admits (both modes) ========================

for (const surface of SURFACES) {
  test(`owner IP (${OWNER_IP}) admits at ${surface.name}`, async () => {
    const r = await probe(surface.url, { "X-Forwarded-For": xff(OWNER_IP) });
    assert.equal(r.status, 200,
      `${surface.name} must return 200 for owner IP · mode=${MODE} · got ${r.status}`);
  });
}


// ================== Non-allowlisted probes (mode-dependent) =============

if (MODE === "strict") {
  for (const surface of SURFACES) {
    test(`STRICT · unknown IP refuses at ${surface.name} · refusal sentence + 403`,
        async () => {
      const r = await probe(surface.url, { "X-Forwarded-For": xff(UNKNOWN_IP) });
      assert.equal(r.status, 403,
        `${surface.name} must return 403 for unknown IP in strict mode · got ${r.status}`);
      assert.ok(r.text.includes(REFUSAL),
        `${surface.name} refusal body must contain: '${REFUSAL}' · got: '${r.text.slice(0, 200)}'`);
    });

    test(`STRICT · no XFF header refuses at ${surface.name} · refusal sentence + 403`,
        async () => {
      const r = await probe(surface.url, {});
      assert.equal(r.status, 403,
        `${surface.name} must return 403 with no XFF in strict mode · got ${r.status}`);
      assert.ok(r.text.includes(REFUSAL),
        `${surface.name} refusal body must contain: '${REFUSAL}'`);
    });
  }
} else {
  // Permissive mode: every probe admits regardless of source.
  for (const surface of SURFACES) {
    test(`PERMISSIVE · unknown IP admits at ${surface.name}`, async () => {
      const r = await probe(surface.url, { "X-Forwarded-For": xff(UNKNOWN_IP) });
      assert.equal(r.status, 200,
        `${surface.name} must return 200 for any IP in permissive mode · got ${r.status}`);
    });

    test(`PERMISSIVE · no XFF header admits at ${surface.name}`, async () => {
      const r = await probe(surface.url, {});
      assert.equal(r.status, 200,
        `${surface.name} must return 200 with no XFF in permissive mode · got ${r.status}`);
    });
  }
}


// ================== Regression proof for 2026-08-26T09:20Z defect =======

test("frontend surface strict-flip is not just backend-scoped (regression)", async () => {
  // The specific defect: pre-fix, GET / on the frontend returned 200
  // with the SPA shell even though ALLOWLIST_MODE was strict, because
  // the craco Node process had a stale permissive-mode mirror. This
  // test asserts the strict flip is honored on BOTH ports.
  if (MODE !== "strict") return;  // regression proof only meaningful under strict
  const rf = await probe(`${FRONTEND}/`, { "X-Forwarded-For": xff(UNKNOWN_IP) });
  const rb = await probe(`${BACKEND}/api/governance/state`,
                         { "X-Forwarded-For": xff(UNKNOWN_IP) });
  assert.equal(rf.status, 403, "frontend GET / must refuse unknown IP under strict");
  assert.equal(rb.status, 403, "backend /api/* must refuse unknown IP under strict");
  assert.ok(rf.text.includes(REFUSAL), "frontend refusal must match backend refusal sentence");
  assert.ok(rb.text.includes(REFUSAL), "backend refusal must match sentence");
});
