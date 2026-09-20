import React from "react";

/**
 * Loading state — per FE Integration Brief §6.
 * Italic ink3, in place, no skeleton shimmer.
 */
export default function LoadingState({ message = "Reading…" }) {
  return (
    <div data-testid="loading-state" className="flex items-center justify-center py-12">
      <p className="text-sm italic" style={{ color: "var(--ink3, #5b6270)" }}>
        {message}
      </p>
    </div>
  );
}
