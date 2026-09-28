import React from "react";

/**
 * Honest empty state — per FE Integration Brief §6.
 * Bordered card with a full sentence explaining *why* it is empty
 * and *when* it will fill.
 */
export default function HonestEmpty({ message }) {
  return (
    <div
      data-testid="honest-empty"
      className="border rounded-lg p-5 my-4"
      style={{ borderColor: "var(--hair, #d5cebe)", background: "var(--surface, #f0ece1)" }}
    >
      <p className="text-sm" style={{ color: "var(--ink2, #3d4350)" }}>
        {message}
      </p>
    </div>
  );
}
