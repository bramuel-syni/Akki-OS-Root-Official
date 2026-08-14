// craco.config.js
const path = require("path");
const fs = require("fs");
require("dotenv").config();

// Owner stop-order 2026-08-14: source-IP allowlist replaces the retired
// token gate. SPINE_ALLOWED_IPS lives in /app/backend/.env as the single
// source of truth (both the FastAPI middleware and this dev-server
// middleware read from that file). Loaded into process.env so the
// dev-server middleware sees the same values.
try {
  const spineEnv = require("dotenv").parse(
    fs.readFileSync("/app/backend/.env", "utf8")
  );
  if (spineEnv.SPINE_ALLOWED_IPS !== undefined) {
    process.env.SPINE_ALLOWED_IPS = spineEnv.SPINE_ALLOWED_IPS;
  }
  if (spineEnv.SPINE_TRUSTED_PROXY_HOPS !== undefined) {
    process.env.SPINE_TRUSTED_PROXY_HOPS = spineEnv.SPINE_TRUSTED_PROXY_HOPS;
  }
} catch (err) {
  // File missing → SPINE_ALLOWED_IPS stays unset → fail-closed refuse in middleware.
}

const { makeIPAllowlistMiddleware } = require("./plugins/ip-allowlist/middleware.js");
const { makeRetiredRoutesMiddleware } = require("./plugins/retired-routes/middleware.js");

// Check if we're in development/preview mode (not production build)
// Craco sets NODE_ENV=development for start, NODE_ENV=production for build
const isDevServer = process.env.NODE_ENV !== "production";

// Environment variable overrides
const config = {
  enableHealthCheck: process.env.ENABLE_HEALTH_CHECK === "true",
};

// react-scripts@5 emits webpack-dev-server v4 options; strip/translate them for v5.
function makeDevServerV5Compatible(devServerConfig) {
  const {
    https,
    onAfterSetupMiddleware,
    onBeforeSetupMiddleware,
    onListening,
    setupMiddlewares,
    ...compatibleConfig
  } = devServerConfig;

  compatibleConfig.server =
    typeof https === "object"
      ? { type: "https", options: https }
      : https
        ? "https"
        : "http";
  compatibleConfig.headers = {
    ...compatibleConfig.headers,
    "Cross-Origin-Resource-Policy": "same-origin",
  };

  if (onBeforeSetupMiddleware || setupMiddlewares) {
    compatibleConfig.setupMiddlewares = (middlewares, devServer) => {
      if (onBeforeSetupMiddleware) {
        onBeforeSetupMiddleware(devServer);
      }

      return setupMiddlewares
        ? setupMiddlewares(middlewares, devServer)
        : middlewares;
    };
  }

  compatibleConfig.onListening = (devServer) => {
    devServer.close ??= (callback) => devServer.stopCallback(callback);

    if (onListening) {
      onListening(devServer);
    }
    if (onAfterSetupMiddleware) {
      onAfterSetupMiddleware(devServer);
    }
  };

  return compatibleConfig;
}

// Conditionally load health check modules only if enabled
let WebpackHealthPlugin;
let setupHealthEndpoints;
let healthPluginInstance;

if (config.enableHealthCheck) {
  WebpackHealthPlugin = require("./plugins/health-check/webpack-health-plugin");
  setupHealthEndpoints = require("./plugins/health-check/health-endpoints");
  healthPluginInstance = new WebpackHealthPlugin();
}

let webpackConfig = {
  eslint: {
    configure: {
      extends: ["plugin:react-hooks/recommended"],
      rules: {
        "react-hooks/rules-of-hooks": "error",
        "react-hooks/exhaustive-deps": "warn",
      },
    },
  },
  webpack: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
    configure: (webpackConfig) => {

      // Add ignored patterns to reduce watched directories
        webpackConfig.watchOptions = {
          ...webpackConfig.watchOptions,
          ignored: [
            '**/node_modules/**',
            '**/.git/**',
            '**/build/**',
            '**/dist/**',
            '**/coverage/**',
            '**/public/**',
        ],
      };

      // Add health check plugin to webpack if enabled
      if (config.enableHealthCheck && healthPluginInstance) {
        webpackConfig.plugins.push(healthPluginInstance);
      }
      return webpackConfig;
    },
  },
};

webpackConfig.devServer = (devServerConfig) => {
  // Add health check endpoints if enabled
  if (config.enableHealthCheck && setupHealthEndpoints && healthPluginInstance) {
    const originalSetupMiddlewares = devServerConfig.setupMiddlewares;

    devServerConfig.setupMiddlewares = (middlewares, devServer) => {
      // Call original setup if exists
      if (originalSetupMiddlewares) {
        middlewares = originalSetupMiddlewares(middlewares, devServer);
      }

      // Setup health endpoints
      setupHealthEndpoints(devServer, healthPluginInstance);

      return middlewares;
    };
  }

  return devServerConfig;
};

// Wrap with visual edits (automatically adds babel plugin, dev server, and overlay in dev mode)
if (isDevServer) {
  try {
    const { withVisualEdits } = require("@emergentbase/visual-edits/craco");
    webpackConfig = withVisualEdits(webpackConfig);
  } catch (err) {
    if (err.code === 'MODULE_NOT_FOUND' && err.message.includes('@emergentbase/visual-edits/craco')) {
      console.warn(
        "[visual-edits] @emergentbase/visual-edits not installed — visual editing disabled."
      );
    } else {
      throw err;
    }
  }
}

// Run last so it also wraps whatever devServer withVisualEdits leaves in place.
const configureDevServer = webpackConfig.devServer;
webpackConfig.devServer = (devServerConfig) => {
  const configured =
    typeof configureDevServer === "function"
      ? configureDevServer(devServerConfig)
      : devServerConfig;

  // IP ALLOWLIST — installed at the OUTERMOST wrapper so no upstream
  // transform (withVisualEdits, health-check, v5-compat) can drop it.
  // Runs FIRST for every request: UI, HMR, static, SPA fallback, everything.
  const priorSetupMiddlewares = configured.setupMiddlewares;
  configured.setupMiddlewares = (middlewares, devServer) => {
    if (priorSetupMiddlewares) {
      middlewares = priorSetupMiddlewares(middlewares, devServer);
    }
    middlewares.unshift({
      name: "spine-retired-routes",
      path: "/",
      middleware: makeRetiredRoutesMiddleware(),
    });
    middlewares.unshift({
      name: "spine-ip-allowlist",
      path: "/",
      middleware: makeIPAllowlistMiddleware(process.env),
    });
    return middlewares;
  };

  return makeDevServerV5Compatible(configured);
};

module.exports = webpackConfig;
