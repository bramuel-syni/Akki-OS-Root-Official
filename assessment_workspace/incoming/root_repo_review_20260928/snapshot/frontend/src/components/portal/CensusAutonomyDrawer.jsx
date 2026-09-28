/**
 * CensusAutonomyDrawer — additive React overlay for PHASE 3 continuation A''.
 *
 * Owner directive verbatim (this-turn):
 *   "the UI must show REAL scheduler state only — the running card polls
 *    the service's own state, never synthesized progress."
 *
 * This overlay sits OUTSIDE the prototype iframe (which is the design of
 * record per SO §3.8 additive-only — zero edits to the HTML prototype).
 * It renders:
 *   - A floating "Run census" button pinned bottom-right (companion to
 *     the prototype's own portal chrome).
 *   - A modal form (tenant_id + connect_source_descriptor +
 *     lawful_basis_admit_ref) that POSTs /api/portal/census/run.
 *   - A running-card that polls GET /api/portal/census/runs/{id}/state
 *     via the useCensusRunState hook and displays REAL state verbatim.
 *
 * All backend calls are JWT-gated via the JWT token stored in
 * localStorage under "jwt" (same convention as other portal surfaces).
 *
 * Standing bound: additive-only per SO §3.8 · never edits the prototype
 * HTML iframe · never synthesizes progress / ETA / random values.
 */
import React, { useState } from "react";
import { useCensusRunState } from "../../hooks/useCensusRunState";

const CENSUS_RUN_STATE_CODES = ["PENDING", "COMPLETE", "REFUSED"];

export function CensusAutonomyDrawer() {
  const [open, setOpen] = useState(false);
  const [tenantId, setTenantId] = useState("AKKI-TEST");
  const [sourceDescriptor, setSourceDescriptor] = useState('{"source": "manual-run"}');
  const [lawfulBasisRef, setLawfulBasisRef] = useState("/lawful_basis_admits/AKKI-TEST-fixture");
  const [censusRunId, setCensusRunId] = useState(null);
  const [submitError, setSubmitError] = useState(null);

  const jwt = typeof window !== "undefined" ? window.localStorage.getItem("jwt") : null;
  const { state, error: pollError } = useCensusRunState(censusRunId, jwt);

  async function submitRun() {
    setSubmitError(null);
    try {
      const body = {
        tenant_id: tenantId,
        connect_source_descriptor: JSON.parse(sourceDescriptor),
        lawful_basis_admit_ref: lawfulBasisRef,
      };
      const resp = await fetch(
        `${process.env.REACT_APP_BACKEND_URL}/api/portal/census/run`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...(jwt ? { "Authorization": `Bearer ${jwt}` } : {}),
          },
          body: JSON.stringify(body),
        }
      );
      const doc = await resp.json();
      if (resp.status === 202) {
        setCensusRunId(doc.census_run_id);
      } else {
        setSubmitError(
          `${doc.refusal_code || `HTTP ${resp.status}`}: ${doc.detail || "submission failed"}`
        );
      }
    } catch (e) {
      setSubmitError(String(e));
    }
  }

  // --- Render REAL state only (never synthesize). -----------------------
  function renderRunningCard() {
    if (!censusRunId) return null;
    if (!state) {
      return (
        <div data-testid="census-autonomy-running-card-unknown" style={styles.card}>
          <div style={styles.cardLabel}>census_run_id</div>
          <div style={styles.cardValue}>{censusRunId}</div>
          <div style={styles.cardStatus}>… awaiting scheduler pickup (real state not yet emitted)</div>
          {pollError && <div style={styles.error}>poll error: {pollError}</div>}
        </div>
      );
    }
    const status = state.status;
    if (!CENSUS_RUN_STATE_CODES.includes(status)) {
      return (
        <div data-testid="census-autonomy-running-card-invalid" style={styles.card}>
          <div style={styles.cardLabel}>census_run_id</div>
          <div style={styles.cardValue}>{censusRunId}</div>
          <div style={styles.error}>UNKNOWN STATUS FROM SCHEDULER: {String(status)}</div>
        </div>
      );
    }
    return (
      <div data-testid={`census-autonomy-running-card-${status.toLowerCase()}`} style={styles.card}>
        <div style={styles.cardLabel}>census_run_id</div>
        <div style={styles.cardValue}>{state.census_run_id}</div>
        <div style={{...styles.cardStatus, color: statusColor(status)}}>{status}</div>
        {status === "PENDING" && (
          <>
            <div style={styles.cardMeta}>tenant: {state.tenant_id}</div>
            <div style={styles.cardMeta}>trigger: {state.trigger}</div>
            <div style={styles.cardMeta}>enqueued: {state.enqueued_at_utc}</div>
          </>
        )}
        {status === "COMPLETE" && (
          <>
            <div style={styles.cardMeta}>tenant: {state.tenant_id}</div>
            <div style={styles.cardMeta}>completed: {state.completed_at_utc}</div>
            <pre style={styles.payload}>{JSON.stringify(state.payload, null, 2)}</pre>
          </>
        )}
        {status === "REFUSED" && (
          <>
            <div style={styles.cardMeta}>tenant: {state.tenant_id}</div>
            <div style={styles.cardMeta}>refusal_code: {state.refusal_code}</div>
            <div style={styles.cardMeta}>detail: {state.detail}</div>
          </>
        )}
      </div>
    );
  }

  return (
    <>
      <button
        data-testid="census-autonomy-open-drawer"
        onClick={() => setOpen(true)}
        style={styles.launcher}
        title="Run census — supervisor-managed persistent worker"
      >
        Run census
      </button>
      {open && (
        <div data-testid="census-autonomy-drawer" style={styles.drawerOverlay}>
          <div style={styles.drawer}>
            <div style={styles.drawerHeader}>
              <div style={styles.drawerTitle}>Run census</div>
              <button
                data-testid="census-autonomy-close-drawer"
                onClick={() => setOpen(false)}
                style={styles.close}
              >×</button>
            </div>
            {!censusRunId && (
              <div style={styles.form}>
                <label style={styles.label}>tenant_id</label>
                <input
                  data-testid="census-autonomy-tenant-id"
                  value={tenantId}
                  onChange={(e) => setTenantId(e.target.value)}
                  style={styles.input}
                />
                <label style={styles.label}>connect_source_descriptor (JSON)</label>
                <textarea
                  data-testid="census-autonomy-source-descriptor"
                  value={sourceDescriptor}
                  onChange={(e) => setSourceDescriptor(e.target.value)}
                  style={styles.textarea}
                  rows={3}
                />
                <label style={styles.label}>lawful_basis_admit_ref</label>
                <input
                  data-testid="census-autonomy-lawful-basis"
                  value={lawfulBasisRef}
                  onChange={(e) => setLawfulBasisRef(e.target.value)}
                  style={styles.input}
                />
                <button
                  data-testid="census-autonomy-submit-run"
                  onClick={submitRun}
                  style={styles.submit}
                >Run census</button>
                {submitError && (
                  <div data-testid="census-autonomy-submit-error" style={styles.error}>
                    {submitError}
                  </div>
                )}
              </div>
            )}
            {renderRunningCard()}
            {censusRunId && (
              <button
                data-testid="census-autonomy-new-run"
                onClick={() => setCensusRunId(null)}
                style={styles.secondary}
              >Queue another run</button>
            )}
          </div>
        </div>
      )}
    </>
  );
}

function statusColor(status) {
  if (status === "COMPLETE") return "#1d7a6e";
  if (status === "REFUSED") return "#b8395b";
  return "#5b6270";
}

const styles = {
  launcher: {
    position: "fixed", bottom: 24, right: 24, zIndex: 2147483000,
    padding: "10px 18px", background: "#16274a", color: "#f5f2ea",
    border: "none", borderRadius: 8, fontSize: 13, fontWeight: 600,
    cursor: "pointer", boxShadow: "0 8px 24px rgba(15,27,51,.28)",
    fontFamily: "Söhne, Helvetica Neue, Arial, sans-serif",
  },
  drawerOverlay: {
    position: "fixed", top: 0, left: 0, width: "100vw", height: "100vh",
    background: "rgba(15,27,51,.42)", zIndex: 2147483001,
    display: "flex", justifyContent: "flex-end",
  },
  drawer: {
    width: "min(460px, 94vw)", height: "100%", background: "#f5f2ea",
    padding: "24px 28px", overflowY: "auto",
    boxShadow: "-14px 0 48px rgba(15,27,51,.18)",
    fontFamily: "Söhne, Helvetica Neue, Arial, sans-serif",
    color: "#1b1f27",
  },
  drawerHeader: {
    display: "flex", justifyContent: "space-between", alignItems: "center",
    marginBottom: 16,
  },
  drawerTitle: { fontFamily: "Iowan Old Style, Georgia, serif", fontSize: 22 },
  close: {
    background: "transparent", border: "none", fontSize: 22, cursor: "pointer",
    color: "#5b6270",
  },
  form: { display: "flex", flexDirection: "column", gap: 6, marginBottom: 20 },
  label: { fontSize: 10, letterSpacing: ".08em", textTransform: "uppercase", color: "#5b6270", marginTop: 8 },
  input: {
    padding: "8px 11px", border: "1px solid #e4dfd3", borderRadius: 6,
    fontSize: 13, background: "#fff", fontFamily: "inherit", color: "#1b1f27",
  },
  textarea: {
    padding: "8px 11px", border: "1px solid #e4dfd3", borderRadius: 6,
    fontSize: 12, background: "#fff", fontFamily: "ui-monospace, Menlo, Consolas, monospace",
    color: "#1b1f27",
  },
  submit: {
    marginTop: 12, padding: "10px 16px", background: "#16274a", color: "#f5f2ea",
    border: "none", borderRadius: 7, fontSize: 13, fontWeight: 600, cursor: "pointer",
  },
  secondary: {
    marginTop: 12, padding: "8px 14px", background: "#fff", color: "#1b1f27",
    border: "1px solid #e4dfd3", borderRadius: 7, fontSize: 12, fontWeight: 600, cursor: "pointer",
  },
  card: {
    marginTop: 12, padding: "16px 18px", background: "#fff",
    border: "1px solid #e4dfd3", borderRadius: 11,
  },
  cardLabel: { fontSize: 10, letterSpacing: ".08em", textTransform: "uppercase", color: "#5b6270" },
  cardValue: { fontFamily: "ui-monospace, Menlo, Consolas, monospace", fontSize: 12, marginBottom: 10, color: "#1b1f27" },
  cardStatus: { fontFamily: "Iowan Old Style, Georgia, serif", fontSize: 20, marginBottom: 10 },
  cardMeta: { fontSize: 12, color: "#3d4350", marginBottom: 4 },
  payload: {
    marginTop: 8, padding: 10, background: "#f0ece1", borderRadius: 6,
    fontSize: 11, fontFamily: "ui-monospace, Menlo, Consolas, monospace",
    whiteSpace: "pre-wrap", wordBreak: "break-word",
  },
  error: { color: "#b8395b", fontSize: 12, marginTop: 8 },
};

export default CensusAutonomyDrawer;
