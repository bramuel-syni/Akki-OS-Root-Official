import React from "react";
import { useParams } from "react-router-dom";
import BackendPending from "@/components/shared/BackendPending";

/**
 * Connect Resources — DAP §4.3
 * 4 destinations: key, agents, compute, models
 * Mostly backend pending.
 */

const VIEWS = {
  key: {
    title: "Workspace API Key",
    detail: "Issue and revoke a workspace key. No endpoint exists for API key management. The 'shown once, never stored' guarantee is a backend property that must be confirmed.",
  },
  agents: {
    title: "Your AI Agent",
    detail: "Register an AI agent with its own account and monitoring. No route exists for agent registration.",
  },
  compute: {
    title: "Your Compute",
    detail: "POST /api/connect/gpu returns the declaration → hardening → acceptance handshake. This endpoint exists but requires a form submission flow. Wiring deferred to full request lifecycle integration.",
  },
  models: {
    title: "Your Models & Recipes",
    detail: "POST /api/connect/intent records a model/recipe connection intent. This endpoint exists but requires a form submission flow. Wiring deferred to full request lifecycle integration.",
  },
};

export default function ConnectResources() {
  const { tab } = useParams();
  const view = VIEWS[tab] || VIEWS["key"];

  return (
    <div data-testid={`connect-resources-${tab}`} className="max-w-5xl mx-auto px-8 py-10">
      <h1
        data-testid="connect-resources-title"
        className="text-xl font-semibold mb-1"
        style={{ color: "var(--ink)", fontFamily: "var(--head)" }}
      >
        Connect Resources
      </h1>
      <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
        {view.title}
      </p>
      <BackendPending surface={view.title} detail={view.detail} />
    </div>
  );
}
