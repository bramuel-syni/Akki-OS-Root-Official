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
    detail: "Workspace key management is not available yet. No key has been issued.",
  },
  agents: {
    title: "Your AI Agent",
    detail: "Agent registration is not available yet. No agent has been connected.",
  },
  compute: {
    title: "Your Compute",
    detail: "Connecting additional compute is not available from this workspace yet. Existing compute is unchanged.",
  },
  models: {
    title: "Your Models & Recipes",
    detail: "Connecting an outside model or recipe is not available from this workspace yet. Existing models are unchanged.",
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
