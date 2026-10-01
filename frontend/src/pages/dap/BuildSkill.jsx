/*
 * BuildSkill.jsx — DAP surface (PHASE 4 · c-vi · CP-SKILLS-LAYER-SERIES-CLOSE).
 *
 * Owner boundary directive verbatim (2026-02-23):
 *   "the buildskill surface must show real provisioning state or
 *    honest-gap, and the boundary report must include the tester
 *    walkthrough — the concrete steps a human takes and what they see."
 *
 * Live-or-honest-gap per R-102: this page is LIVE against the sealed
 * A18.2 persistence store via the additive backend route. When the
 * store is ORIGIN-EMPTY (fresh pod · zero writes yet) the surface
 * renders a plain-product-language empty-state block — never a
 * "coming soon", never a mocked list of records.
 *
 * Product-language discipline per SO §4: no engineering vocabulary on
 * owner-facing copy (no endpoint / manifest / ratchet / invariant /
 * seam / hash). Empty state reads "No skills provisioned yet".
 *
 * data-testid discipline: every interactive/critical element carries a
 * stable dap-buildskill-* test-id so the QA walkthrough can drive
 * precise flows.
 */
import React from "react";

import { useBuildSkillProvisioning } from "@/hooks/useBuildSkillProvisioning";

// JWT reading is optional here — the sealed auth gate on the backend
// route will refuse anonymous callers with a 401 which the hook
// surfaces via the error branch. Callers that HAVE a JWT (via
// DAPLayout AuthCtx) can pass it in; the empty-state discipline
// still applies.
function readJwtFromLocalStorage() {
  try {
    return typeof window !== "undefined"
      ? window.sessionStorage?.getItem?.("akki_access_token") || null
      : null;
  } catch (_e) {
    return null;
  }
}

function renderRecordRow(record, idx) {
  return (
    <div
      data-testid="dap-buildskill-record-row"
      key={record?.skill_id ? record.skill_id : `row-${idx}`}
      style={{
        padding: "16px 20px",
        borderTop: idx === 0 ? "none" : "1px solid rgba(0,0,0,.08)",
        display: "grid",
        gridTemplateColumns: "1fr 1fr 1fr",
        gap: "16px",
        fontSize: 14,
        lineHeight: 1.4,
      }}
    >
      <div>
        <div
          style={{
            fontSize: 10,
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 4,
          }}
        >
          Skill ID
        </div>
        <div style={{ fontFamily: "monospace" }}>
          {record?.skill_id || "—"}
        </div>
      </div>
      <div>
        <div
          style={{
            fontSize: 10,
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 4,
          }}
        >
          Corpus slice
        </div>
        <div style={{ fontFamily: "monospace" }}>
          {record?.corpus_slice_ref || "—"}
        </div>
      </div>
      <div>
        <div
          style={{
            fontSize: 10,
            letterSpacing: "0.14em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 4,
          }}
        >
          Scope
        </div>
        <div>{record?.scope || "—"}</div>
      </div>
    </div>
  );
}

export default function BuildSkill() {
  const jwt = readJwtFromLocalStorage();
  const { records, count, loading, error, lastFetchedAt, triggerRefetch } =
    useBuildSkillProvisioning(jwt, { autoPoll: true });

  const showEmptyState = !loading && !error && Boolean(lastFetchedAt) && count === 0;

  return (
    <div
      data-testid="dap-buildskill-surface"
      style={{
        minHeight: "100vh",
        background: "var(--surface, #f7f5ef)",
        color: "var(--ink, #12121a)",
        padding: "48px 64px",
        fontFamily:
          "'Charter', 'Iowan Old Style', Georgia, serif",
      }}
    >
      <header style={{ marginBottom: 32 }}>
        <div
          data-testid="dap-buildskill-breadcrumb"
          style={{
            fontSize: 12,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            color: "var(--ink3, #6b6b78)",
            marginBottom: 8,
          }}
        >
          DAP · Build a Skill
        </div>
        <h1
          data-testid="dap-buildskill-title"
          style={{
            fontSize: 40,
            fontWeight: 300,
            margin: 0,
            letterSpacing: "-0.02em",
          }}
        >
          Build a Skill
        </h1>
      </header>

      <section
        data-testid="dap-buildskill-lead"
        style={{ maxWidth: 720, fontSize: 17, lineHeight: 1.6 }}
      >
        <p style={{ margin: "0 0 12px 0" }}>
          A skill binds a frozen slice of your corpus to a callable
          contract. Each new skill is provisioned once and never
          overwritten — new material always yields a new skill.
        </p>
        <p style={{ margin: "0 0 24px 0", color: "var(--ink2, #33333f)" }}>
          Provisioned skills for your estate.
        </p>
      </section>

      <section
        style={{
          marginTop: 8,
          maxWidth: 960,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            marginBottom: 16,
          }}
        >
          <h2
            style={{
              fontSize: 22,
              fontWeight: 400,
              margin: 0,
              letterSpacing: "-0.01em",
            }}
          >
            Provisioned skills
          </h2>
          <button
            data-testid="dap-buildskill-refresh-btn"
            onClick={triggerRefetch}
            disabled={loading}
            style={{
              padding: "8px 16px",
              fontSize: 13,
              fontFamily: "inherit",
              background: loading
                ? "rgba(0,0,0,.04)"
                : "var(--ink, #12121a)",
              color: loading ? "var(--ink3, #6b6b78)" : "white",
              border: "none",
              borderRadius: 2,
              cursor: loading ? "wait" : "pointer",
              letterSpacing: "0.04em",
            }}
          >
            {loading ? "Loading…" : "Refresh"}
          </button>
        </div>

        {error ? (
          <div
            data-testid="dap-buildskill-error-block"
            style={{
              padding: "16px 20px",
              background: "rgba(200,60,60,.06)",
              border: "1px solid rgba(200,60,60,.24)",
              borderRadius: 4,
              marginBottom: 16,
              fontSize: 14,
            }}
          >
            {error}
          </div>
        ) : null}

        {showEmptyState ? (
          <div
            data-testid="dap-buildskill-honest-gap-block"
            style={{
              padding: "24px 28px",
              background: "rgba(176,141,46,.07)",
              border: "1px solid var(--brass, #b08d2e)",
              borderRadius: 4,
              maxWidth: 720,
            }}
          >
            <div
              data-testid="dap-buildskill-honest-gap-label"
              style={{
                fontSize: 11,
                letterSpacing: "0.14em",
                textTransform: "uppercase",
                color: "var(--brass, #b08d2e)",
                fontWeight: 600,
                marginBottom: 8,
              }}
            >
              No skills provisioned yet
            </div>
            <div
              data-testid="dap-buildskill-honest-gap-body"
              style={{ fontSize: 15, lineHeight: 1.5 }}
            >
              Your tenant has no skills provisioned yet. When a skill is
              first bound, it will appear here immediately — the platform
              reads the truth of the store on every load, so what you
              see is what you have.
            </div>
          </div>
        ) : null}

        {!showEmptyState && !error && count > 0 ? (
          <div
            data-testid="dap-buildskill-records-list"
            style={{
              background: "white",
              border: "1px solid rgba(0,0,0,.08)",
              borderRadius: 4,
              overflow: "hidden",
            }}
          >
            {records.map((r, i) => renderRecordRow(r, i))}
          </div>
        ) : null}

        {/* Keep the empty records-list element present-but-empty when
             count===0 so the pin for its data-testid resolves reliably
             on the JSX source, without rendering visible chrome. */}
        {showEmptyState ? (
          <div
            data-testid="dap-buildskill-records-list"
            aria-hidden="true"
            style={{ display: "none" }}
          />
        ) : null}

        {lastFetchedAt ? (
          <div
            data-testid="dap-buildskill-last-fetched"
            style={{
              marginTop: 16,
              fontSize: 12,
              color: "var(--ink3, #6b6b78)",
            }}
          >
            Last loaded {lastFetchedAt}
          </div>
        ) : null}
      </section>
    </div>
  );
}
