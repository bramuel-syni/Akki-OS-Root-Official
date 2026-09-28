import React from "react";
import { AlertCircle } from "lucide-react";

/**
 * Honest "backend pending" state — rendered when the spec requires a screen
 * but no backing endpoint exists in the contract.
 */
export default function BackendPending({ surface, detail }) {
  return (
    <div
      data-testid="backend-pending"
      className="flex flex-col items-center justify-center py-16 px-6 text-center"
    >
      <div
        className="w-12 h-12 rounded-full flex items-center justify-center mb-4"
        style={{ background: "rgba(176,141,46,.12)" }}
      >
        <AlertCircle size={24} style={{ color: "var(--brass, #b08d2e)" }} />
      </div>
      <h3
        data-testid="backend-pending-title"
        className="text-base font-semibold mb-2"
        style={{ color: "var(--ink, #1b1f27)" }}
      >
        Backend pending
      </h3>
      <p
        data-testid="backend-pending-surface"
        className="text-sm mb-1"
        style={{ color: "var(--ink2, #3d4350)" }}
      >
        {surface}
      </p>
      {detail && (
        <p
          data-testid="backend-pending-detail"
          className="text-xs max-w-md"
          style={{ color: "var(--ink3, #5b6270)" }}
        >
          {detail}
        </p>
      )}
    </div>
  );
}
