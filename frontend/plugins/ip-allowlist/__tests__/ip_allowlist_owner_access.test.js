/**
 * ip_allowlist_owner_access.test.js — W10 interleave.
 *
 * Extends the frontend allowlist plugin to accept the same owner-access
 * layers the Python middleware got (OWNER_ALLOWLIST_IPS + ALLOWLIST_MODE)
 * so the preview surface is consistently governed.
 *
 * Preserves all existing gating invariants in ip_allowlist.test.js.
 */
"use strict";
const { test } = require("node:test");
const assert = require("node:assert/strict");

const REFUSAL_SENTENCE = "This surface answers allowlisted addresses only.";
const CF_EDGE = "172.71.255.34";
const GCP_LB = "136.110.244.150";
const ALLOWED = "34.16.56.64";
const OWNER = "41.90.172.155";
const DISALLOWED = "9.9.9.9";

function xff(clientIp) {
  return `${clientIp},${CF_EDGE},${GCP_LB}`;
}

const { check } = require("../check.js");


// ---------- OWNER_ALLOWLIST_IPS layered on SPINE_ALLOWED_IPS ----------

test("owner IP admitted via OWNER_ALLOWLIST_IPS layer", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED, OWNER_ALLOWLIST_IPS: OWNER };
  const d = check({ "x-forwarded-for": xff(OWNER) }, env);
  assert.equal(d.allowed, true, `owner IP not admitted: ${JSON.stringify(d)}`);
});

test("spine IP still admitted when owner layer present", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED, OWNER_ALLOWLIST_IPS: OWNER };
  const d = check({ "x-forwarded-for": xff(ALLOWED) }, env);
  assert.equal(d.allowed, true);
});

test("unknown IP still refused with both layers populated (strict)", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED, OWNER_ALLOWLIST_IPS: OWNER };
  const d = check({ "x-forwarded-for": xff(DISALLOWED) }, env);
  assert.equal(d.allowed, false);
  assert.equal(d.status, 403);
  assert.equal(d.body, REFUSAL_SENTENCE);
});

test("owner allowlist accepts multiple entries comma-separated", () => {
  const env = {
    SPINE_ALLOWED_IPS: ALLOWED,
    OWNER_ALLOWLIST_IPS: "10.0.0.1, " + OWNER + ",10.0.0.2",
  };
  const d = check({ "x-forwarded-for": xff(OWNER) }, env);
  assert.equal(d.allowed, true);
});

test("owner allowlist admit carries layer attribution", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED, OWNER_ALLOWLIST_IPS: OWNER };
  const d = check({ "x-forwarded-for": xff(OWNER) }, env);
  assert.equal(d.allowed, true);
  assert.equal(d.layer, "owner", `admit not attributed to owner layer: ${JSON.stringify(d)}`);
});

test("spine allowlist admit carries spine layer attribution", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED, OWNER_ALLOWLIST_IPS: OWNER };
  const d = check({ "x-forwarded-for": xff(ALLOWED) }, env);
  assert.equal(d.allowed, true);
  assert.equal(d.layer, "spine");
});


// ---------- ALLOWLIST_MODE=permissive ----------

test("permissive mode admits any IP", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED, ALLOWLIST_MODE: "permissive" };
  const d = check({ "x-forwarded-for": xff(DISALLOWED) }, env);
  assert.equal(d.allowed, true, `permissive failed to admit: ${JSON.stringify(d)}`);
});

test("permissive mode admits without any XFF header", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED, ALLOWLIST_MODE: "permissive" };
  const d = check({}, env);
  assert.equal(d.allowed, true);
});

test("permissive mode admit carries permissive layer attribution", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED, ALLOWLIST_MODE: "permissive" };
  const d = check({ "x-forwarded-for": xff(DISALLOWED) }, env);
  assert.equal(d.allowed, true);
  assert.equal(d.mode, "permissive");
  assert.equal(d.layer, "permissive");
});

test("permissive mode normalizes case and whitespace", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED, ALLOWLIST_MODE: "  Permissive  " };
  const d = check({ "x-forwarded-for": xff(DISALLOWED) }, env);
  assert.equal(d.allowed, true);
});

test("mode absent defaults to strict", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED };
  const d = check({ "x-forwarded-for": xff(DISALLOWED) }, env);
  assert.equal(d.allowed, false);
  assert.equal(d.status, 403);
});

test("unknown mode value defaults to strict (fail-closed)", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED, ALLOWLIST_MODE: "loose" };
  const d = check({ "x-forwarded-for": xff(DISALLOWED) }, env);
  assert.equal(d.allowed, false);
});


// ---------- refuse decisions carry mode attribution ----------

test("strict refuse carries mode=strict", () => {
  const env = { SPINE_ALLOWED_IPS: ALLOWED };
  const d = check({ "x-forwarded-for": xff(DISALLOWED) }, env);
  assert.equal(d.allowed, false);
  assert.equal(d.mode, "strict");
});


// ---------- empty allowlist under permissive still admits ----------

test("permissive admits even when both allowlists empty", () => {
  const env = { SPINE_ALLOWED_IPS: "", OWNER_ALLOWLIST_IPS: "", ALLOWLIST_MODE: "permissive" };
  const d = check({ "x-forwarded-for": xff(DISALLOWED) }, env);
  assert.equal(d.allowed, true);
});
