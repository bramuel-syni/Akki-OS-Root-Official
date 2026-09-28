import React from "react";

const STATUS_META = {
  "In Approval": { color: "var(--brass, #b08d2e)", bg: "rgba(176,141,46,.14)" },
  "Executing": { color: "var(--accent, #4c5fd5)", bg: "rgba(76,95,213,.12)" },
  "Ready": { color: "var(--gate, #7c3aaf)", bg: "rgba(124,58,175,.12)" },
  "Retrieved": { color: "var(--sage, #1d7a6e)", bg: "rgba(29,122,110,.12)" },
  "Refused": { color: "var(--ink, #1b1f27)", bg: "rgba(27,31,39,.08)" },
  "Blocked": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.12)" },
  "Expired": { color: "var(--ink3, #5b6270)", bg: "var(--surface2, #ede8da)" },
  "Interrupted (platform fault)": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.08)" },
  // Three Blocked kinds per Ruling 2 (2026-09-20T~19:00Z): request / check / estate.
  // Interrupted (platform fault) is its own rail state (above), NOT a Blocked kind.
  // party_halted is its own rail state (below), NOT a Blocked kind — carries its
  // existing drawer copy from services/dap_lifecycle/party_halted_kind.py.
  // suspended is a principal state (DAP-27, PRIN-1), a different axis, and NEVER
  // renders in the Blocked reason grammar — surfaces only via suspension notices.
  "Blocked \u00b7 request": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.12)" },
  "Blocked \u00b7 check": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.10)" },
  "Blocked \u00b7 estate": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.08)" },
  // party_halted rail state · own drawer · not a Blocked variant.
  "party_halted": { color: "var(--oxblood, #b8395b)", bg: "rgba(184,57,91,.10)" },
};

export default function StatusBadge({ status }) {
  const meta = STATUS_META[status] || { color: "var(--ink3)", bg: "rgba(27,31,39,.06)" };
  return (
    <span
      data-testid={`status-badge-${status?.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
      className="inline-flex items-center text-xs font-medium px-2.5 py-1 rounded-full whitespace-nowrap"
      style={{ color: meta.color, background: meta.bg }}
    >
      {status}
    </span>
  );
}
