/**
 * plugins/ip-allowlist/middleware.js — Express-style adapter over check().
 *
 * Used by craco.config.js `devServer.setupMiddlewares` to gate EVERY
 * incoming HTTP request to the CRA dev-server. Runs BEFORE all other
 * middlewares so no route survives outside the allowlist.
 *
 * W10 interleave (2026-08-26): every decision is logged via
 * console.log with the `ip_allowlist_decision` prefix (nothing silent).
 */
"use strict";

const { check } = require("./check.js");

function logDecision(decision, path) {
  // Structured log line · same grammar as the FastAPI middleware.
  console.log(
    "ip_allowlist_decision decision=%s mode=%s layer=%s client_ip=%s path=%s",
    decision.allowed ? "admit" : "refuse",
    decision.mode || "strict",
    decision.layer || "none",
    decision.clientIp || "<none>",
    path || "<none>",
  );
}

function makeIPAllowlistMiddleware(env) {
  return function ipAllowlistMiddleware(req, res, next) {
    const decision = check(req.headers, env || process.env);
    logDecision(decision, req.url);
    if (decision.allowed) return next();
    res.writeHead(decision.status, { "Content-Type": decision.contentType });
    res.end(decision.body);
  };
}

module.exports = { makeIPAllowlistMiddleware };
