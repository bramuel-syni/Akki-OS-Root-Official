/**
 * plugins/ip-allowlist/middleware.js — Express-style adapter over check().
 *
 * Used by craco.config.js `devServer.setupMiddlewares` to gate EVERY
 * incoming HTTP request to the CRA dev-server. Runs BEFORE all other
 * middlewares so no route survives outside the allowlist.
 */
"use strict";

const { check } = require("./check.js");

function makeIPAllowlistMiddleware(env) {
  return function ipAllowlistMiddleware(req, res, next) {
    const decision = check(req.headers, env || process.env);
    if (decision.allowed) return next();
    res.writeHead(decision.status, { "Content-Type": decision.contentType });
    res.end(decision.body);
  };
}

module.exports = { makeIPAllowlistMiddleware };
