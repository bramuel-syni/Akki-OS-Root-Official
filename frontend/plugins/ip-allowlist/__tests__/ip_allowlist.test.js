/**
 * ip_allowlist.test.js — SECURITY GATING invariants (frontend surface).
 *
 * Owner stop-order 2026-08-14: source-IP allowlist is the ONE access
 * mechanism for the estate's UI as well as its API. The dev-server (or
 * production static server) MUST refuse non-allowlisted addresses with
 * the exact plain sentence and HTTP 403 text/plain — same grammar as the
 * FastAPI middleware in the spine repo.
 *
 * This file freezes the pure `check(headers, env)` function. Middleware
 * wiring in craco.config.js is a thin adapter over it.
 *
 * Tests-first: MUST fail with MODULE_NOT_FOUND before implementation.
 */
const { test } = require("node:test");
const assert = require("node:assert/strict");

const EXACT_REFUSAL_SENTENCE = "This surface answers allowlisted addresses only.";

const CF_EDGE = "172.71.255.34";
const GCP_LB = "136.110.244.150";

const ALLOWED = "34.16.56.64";
const OTHER_ALLOWED = "34.170.12.145";
const DISALLOWED = "9.9.9.9";

function xff(clientIp, spoofedPrefix) {
  const prefix = spoofedPrefix ? spoofedPrefix + "," : "";
  return `${prefix}${clientIp},${CF_EDGE},${GCP_LB}`;
}

function loadModule() {
  return require("../check.js");
}

// -------- module surface --------

test("module exports check() and EXACT refusal sentence", () => {
  const m = loadModule();
  assert.equal(typeof m.check, "function", "check() missing");
  assert.equal(m.REFUSAL_SENTENCE, EXACT_REFUSAL_SENTENCE, "refusal sentence must be exact");
});

// -------- pass path --------

test("allowed IP at trusted position → allowed:true", () => {
  const { check } = loadModule();
  const r = check(
    { "x-forwarded-for": xff(ALLOWED) },
    { SPINE_ALLOWED_IPS: ALLOWED, SPINE_TRUSTED_PROXY_HOPS: "2" }
  );
  assert.equal(r.allowed, true);
});

test("multiple allowlisted addresses all pass", () => {
  const { check } = loadModule();
  for (const ip of [ALLOWED, OTHER_ALLOWED]) {
    const r = check(
      { "x-forwarded-for": xff(ip) },
      { SPINE_ALLOWED_IPS: `${ALLOWED}, ${OTHER_ALLOWED}`, SPINE_TRUSTED_PROXY_HOPS: "2" }
    );
    assert.equal(r.allowed, true, `${ip} in allowlist but rejected`);
  }
});

// -------- refuse path --------

test("disallowed IP → allowed:false, exact sentence, 403", () => {
  const { check } = loadModule();
  const r = check(
    { "x-forwarded-for": xff(DISALLOWED) },
    { SPINE_ALLOWED_IPS: ALLOWED, SPINE_TRUSTED_PROXY_HOPS: "2" }
  );
  assert.equal(r.allowed, false);
  assert.equal(r.status, 403);
  assert.equal(r.body, EXACT_REFUSAL_SENTENCE);
  assert.equal(r.contentType, "text/plain; charset=utf-8");
});

test("spoofed leftmost XFF entries do NOT defeat the allowlist", () => {
  const { check } = loadModule();
  const spoofed = xff(DISALLOWED, `${ALLOWED},1.1.1.1`);
  const r = check(
    { "x-forwarded-for": spoofed },
    { SPINE_ALLOWED_IPS: ALLOWED, SPINE_TRUSTED_PROXY_HOPS: "2" }
  );
  assert.equal(r.allowed, false, "leftmost-XFF spoof accepted (BAD)");
});

test("trusted position is xff[-3] when hops=2", () => {
  const { check } = loadModule();
  const passing = `1.1.1.1,2.2.2.2,${ALLOWED},${CF_EDGE},${GCP_LB}`;
  const failing = `${ALLOWED},2.2.2.2,3.3.3.3,${CF_EDGE},${GCP_LB}`;
  assert.equal(
    check({ "x-forwarded-for": passing }, { SPINE_ALLOWED_IPS: ALLOWED, SPINE_TRUSTED_PROXY_HOPS: "2" }).allowed,
    true
  );
  assert.equal(
    check({ "x-forwarded-for": failing }, { SPINE_ALLOWED_IPS: ALLOWED, SPINE_TRUSTED_PROXY_HOPS: "2" }).allowed,
    false
  );
});

// -------- fail-closed --------

test("missing XFF header → refuse", () => {
  const { check } = loadModule();
  const r = check({}, { SPINE_ALLOWED_IPS: ALLOWED, SPINE_TRUSTED_PROXY_HOPS: "2" });
  assert.equal(r.allowed, false);
});

test("XFF chain shorter than hops+1 → refuse (topology violation)", () => {
  const { check } = loadModule();
  const short = `${ALLOWED},${CF_EDGE}`;
  const r = check({ "x-forwarded-for": short }, { SPINE_ALLOWED_IPS: ALLOWED, SPINE_TRUSTED_PROXY_HOPS: "2" });
  assert.equal(r.allowed, false);
});

test("empty SPINE_ALLOWED_IPS → refuse everything", () => {
  const { check } = loadModule();
  const r = check(
    { "x-forwarded-for": xff(ALLOWED) },
    { SPINE_ALLOWED_IPS: "", SPINE_TRUSTED_PROXY_HOPS: "2" }
  );
  assert.equal(r.allowed, false);
});

test("undefined SPINE_ALLOWED_IPS → refuse everything", () => {
  const { check } = loadModule();
  const r = check(
    { "x-forwarded-for": xff(ALLOWED) },
    { SPINE_TRUSTED_PROXY_HOPS: "2" }
  );
  assert.equal(r.allowed, false);
});

test("whitespace-only allowlist entries are stripped", () => {
  const { check } = loadModule();
  const r = check(
    { "x-forwarded-for": xff(ALLOWED) },
    { SPINE_ALLOWED_IPS: `  ${ALLOWED} ,  , ,  `, SPINE_TRUSTED_PROXY_HOPS: "2" }
  );
  assert.equal(r.allowed, true);
});

test("refusal body never leaks allowlist or caller IP", () => {
  const { check } = loadModule();
  const r = check(
    { "x-forwarded-for": xff(DISALLOWED) },
    { SPINE_ALLOWED_IPS: ALLOWED, SPINE_TRUSTED_PROXY_HOPS: "2" }
  );
  assert.ok(!r.body.includes(ALLOWED), "leaked allowlist entry");
  assert.ok(!r.body.includes(DISALLOWED), "leaked caller IP");
  assert.equal(r.body, EXACT_REFUSAL_SENTENCE);
});
