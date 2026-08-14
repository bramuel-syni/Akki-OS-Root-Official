/**
 * plugins/retired-routes/middleware.js — dev-server 404 for retired paths.
 *
 * Owner stop-order 2026-08-14: /register/connect/gpu is retired. The
 * dev-server responds with HTTP 404 text/plain at the edge for this path
 * so any client-side React-Router fallthrough cannot even attempt to
 * render it.
 */
"use strict";

const RETIRED_PATHS = new Set([
  "/register/connect/gpu",
]);

const RETIRED_NOTICE = "This route has been retired.";

function makeRetiredRoutesMiddleware() {
  return function retiredRoutesMiddleware(req, res, next) {
    // Match exact path OR path?query OR path with trailing slash variant.
    const pathOnly = String(req.url || "").split("?")[0].replace(/\/+$/, "") || "/";
    if (RETIRED_PATHS.has(pathOnly)) {
      res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      res.end(RETIRED_NOTICE);
      return;
    }
    return next();
  };
}

module.exports = { makeRetiredRoutesMiddleware, RETIRED_PATHS, RETIRED_NOTICE };
