import React, { useState, useEffect, useCallback } from "react";
import StatusBadge from "@/components/dap/StatusBadge";
import BackendPending from "@/components/shared/BackendPending";
import LoadingState from "@/components/shared/LoadingState";
import { ChevronDown, ChevronUp, RotateCcw, AlertTriangle, CheckCircle, Square, Send, Clock } from "lucide-react";
import { useAuth } from "@/pages/dap/DAPLayout";
import { tryGet, tryPost } from "@/lib/apiClient";
import {
  STOP_CONFIRM,
  PARTY_HALTED_KIND_LINE,
  PARTY_HALTED_WHAT_NEXT,
  IN_APPROVAL_WAITING_TPL,
  EXPIRED_DATE_TPL,
  EXPIRED_WAITED_TPL,
  EXPIRED_MEANING_TPL,
  EXPIRED_WHAT_NEXT_TPL,
  BLOCK_KIND_REQUEST,
  BLOCK_KIND_CHECK,
  BLOCK_KIND_ESTATE,
  BLOCK_ESTATE_REASON,
  BLOCK_WHATNEXT_REQUEST,
  BLOCK_WHATNEXT_CHECK,
  BLOCK_WHATNEXT_ESTATE_TPL,
} from "@/strings/lifecycleStrings";

/**
 * Request Lifecycle — Journey v2 conformance pass.
 *
 * Wired to:
 *   GET  /api/portal/requests           — principal-scoped history
 *   GET  /api/portal/requests/{id}      — detail
 *   POST /api/portal/requests           — submit new request
 *   POST /api/portal/requests/{id}/stop — request-scoped stop
 *   POST /api/portal/requests/{id}/retry — bounded-3 retry
 *
 * THREE Blocked kinds: request, check, estate (§5, §11) — plus Interrupted
 * (own rail state, platform fault) and party_halted (own rail state).
 * Stopped terminal state (Executing → Stopped, charged-to-point-of-stop,
 * receipted).
 *
 * HARD OMISSIONS (owner-ruled):
 * - NO "Waited N days" in any post-decision Sign-off block (Approved/Refused)
 * - NO partial-release UI
 * - NO owner-turnaround metrics
 * - NO approver identity anywhere (DAP-15)
 * - NO remaining-budget reason lines (DAP-35)
 */

const MODE_VERB = {
  processed: "Open report", finetune: "Download model",
  skills: "Download skill", raw: "Download data"
};

const BLOCK_KIND_META = {
  request: {
    kindLine: BLOCK_KIND_REQUEST,
    whatNext: BLOCK_WHATNEXT_REQUEST,
    showCopy: true,
    showProgress: true,
  },
  check: {
    kindLine: BLOCK_KIND_CHECK,
    whatNext: BLOCK_WHATNEXT_CHECK,
    showCopy: true,
    showProgress: true,
  },
  estate: {
    kindLine: BLOCK_KIND_ESTATE,
    fixedReason: BLOCK_ESTATE_REASON,
    showCopy: false,
    showProgress: false,
  },
};

// Sample requests — reference state machine (used when backend endpoints not yet mounted)
const SAMPLE_REQUESTS = [
  {
    id: "ftn-2026-0118", objective: "Train on the cleared complaint files to route by urgency.",
    status: "Executing", pct: 41, eta: "~6h to completion", mode: "finetune",
    agreement: "Agreement MER-007", submitted: "submitted 5 Sep 2026", submittedBy: "R. Adeyemi",
    scope: "Audio", signoffRequired: true, approvedDate: "12 Sep 2026", approvedByRole: "records authority",
  },
  {
    id: "prc-2026-0109", objective: "Find out which branches drive repeat complaints, this quarter.",
    status: "Executing", stageIndex: 2, stageCount: 4, stageLabel: "Analyzing", eta: "~40 min",
    mode: "processed", agreement: "Agreement MER-002", submitted: "submitted 16 Sep 2026", submittedBy: "T. Mwangi",
    scope: "Audio", signoffRequired: false,
  },
  {
    id: "ftn-2026-0119", objective: "Train on IVR prompts to flag automated-menu drop-off.",
    status: "In Approval", mode: "finetune", agreement: "Agreement MER-007",
    submitted: "submitted 13 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
    submittedAtISO: "2026-09-13", windowEndsAtISO: "2026-09-28",
    dataOwner: "Digicow",
    signoffReason: "This request needs sign-off because it includes IVR prompts. Under Agreement MER-007, Digicow has to approve any use of them.",
    spendCeilingBreach: false,
  },
  {
    id: "ftn-2026-0121", objective: "Train on branch chat logs to flag escalation risk.",
    status: "In Approval", mode: "finetune", agreement: "Agreement MER-007",
    submitted: "submitted 5 Sep 2026", submittedBy: "A. Osei", scope: "Audio",
    submittedAtISO: "2026-09-05", windowEndsAtISO: "2026-09-19",
    dataOwner: "Digicow",
    spendCeilingBreach: true,
    spendCeilingReason: "Organisation ceiling reached for this period. Spend-ceiling breach folds into In Approval.",
  },
  {
    id: "int-2026-0001", objective: "Extract quality metrics from the call recordings.",
    status: "Interrupted (platform fault)", mode: "processed",
    agreement: "Agreement MER-002", submitted: "submitted 17 Sep 2026", submittedBy: "R. Adeyemi",
    scope: "Audio", retryAttempts: 2, maxRetries: 3,
    interruptReason: "Upstream compute node unreachable. Bounded auto-retry in progress.",
  },
  {
    id: "ftn-2026-0120", objective: "Train on radio segments to detect ad breaks.",
    status: "Ready", mode: "finetune", agreement: "Agreement MER-007",
    submitted: "submitted 10 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
    modelId: "MDL-2026-0120", baseModel: "meridian-audio-base-v3",
    targetsSet: "88%", targetsAchieved: "91%", weightsHash: "sha256:7be2a0\u2026d914",
    signoffRequired: true, approvedByRole: "records authority", approvedDate: "14 Sep 2026",
  },
  {
    id: "prc-2026-0111", objective: "Find out which time-of-day produces the most complaint escalations.",
    status: "Retrieved", mode: "processed", agreement: "Agreement MER-002",
    submitted: "submitted 13 Sep 2026", submittedBy: "R. Adeyemi", scope: "Text",
    retrievedAt: "18 Sep 2026",
  },
  {
    id: "ftn-2026-0117", objective: "Train on the call recordings to classify caller intent at 88% accuracy or better.",
    status: "Refused", mode: "finetune", agreement: "Agreement MER-007",
    submitted: "submitted 2 Sep 2026", submittedBy: "A. Osei", scope: "Audio",
    refusalReason: "The call recordings contain spoken account details, and Digicow would not release a model trained on them under this agreement. That reason is recorded rather than left implicit.",
  },
  {
    id: "prc-2026-0104", objective: "Find out complaint volume by branch, last quarter.",
    status: "Expired", mode: "processed", agreement: "Agreement MER-002",
    submitted: "submitted 19 Aug 2026", submittedBy: "R. Adeyemi",
    submittedAtISO: "2026-08-18", expiredAtISO: "2026-09-02", expiredAtDisplay: "2 Sep 2026",
    dataOwner: "Digicow",
    addressedTo: "the records authority at Digicow",
    signoffReason: "This request needed sign-off because it includes complaint files. Under Agreement MER-002, Digicow had to approve any use of them.",
  },
  {
    id: "skl-2026-0047", objective: "Build a skill to summarise complaint threads by branch.",
    status: "Blocked", mode: "skills", agreement: "Agreement MER-007",
    submitted: "submitted 5 Sep 2026", submittedBy: "T. Mwangi", scope: "Text",
    blockedAt: "14 Sep 2026, 03:12", blockKind: "estate",
    dataOwner: "the data governance office at Digicow",
  },
  {
    id: "prc-2026-0102", objective: "Find out average time-to-close by branch, last quarter.",
    status: "Blocked", mode: "processed", agreement: "Agreement MER-002",
    submitted: "submitted 12 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
    blockedAt: "13 Sep 2026, 17:40", blockKind: "request",
    blockReason: "There isn't enough time-to-close data recorded for last quarter to answer this by branch.",
    blockRef: "PRC-2026-0102-B1",
    dataOwner: "Digicow",
  },
  {
    id: "ftn-2026-0122", objective: "Train on the cleared complaint files to identify repeat callers.",
    status: "party_halted", mode: "finetune", agreement: "Agreement MER-007",
    submitted: "submitted 8 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
    blockedAt: "15 Sep 2026, 11:04",
    blockedBy: "R. Adeyemi",
    pctAtStop: 63,
    blockRef: "FTN-2026-0122-B1",
    dataOwner: "Digicow",
    signoffRequired: true, approvedByRole: "records authority", approvedDate: "12 Sep 2026",
  },
  // Stopped terminal state (Executing → Stopped)
  {
    id: "prc-2026-0115", objective: "Find out which branches have the most incomplete complaint records.",
    status: "Stopped", mode: "processed", agreement: "Agreement MER-002",
    submitted: "submitted 14 Sep 2026", submittedBy: "R. Adeyemi", scope: "Audio",
    stoppedAt: "16 Sep 2026, 09:22", pctAtStop: 28,
  },
];

const ALL_STATES = [
  "In Approval", "Executing", "Ready", "Retrieved", "Refused",
  "Blocked", "Expired", "Interrupted (platform fault)",
  "Blocked \u00b7 request", "Blocked \u00b7 check", "Blocked \u00b7 estate",
  "party_halted", "Stopped",
];

const RAIL_ROW = [
  ["Total", "Total"], ["In Approval", "In Approval"], ["Executing", "Executing"],
  ["Ready", "Ready"], ["Retrieved", "Retrieved"], ["Refused", "Refused"],
  ["Blocked", "Blocked"], ["Expired", "Expired"], ["Interrupted (platform fault)", "Interrupted"],
  ["party_halted", "Stopped by you"], ["Stopped", "Stopped"],
];

function daysBetween(isoA, isoB) {
  const a = new Date(isoA);
  const b = isoB ? new Date(isoB) : new Date();
  return Math.max(0, Math.round((b - a) / 86_400_000));
}

/* ── Submit Form ───────────────────────────────────────── */
function SubmitForm({ onSubmitted }) {
  const { user } = useAuth();
  const [objectiveText, setObjectiveText] = useState("");
  const [units, setUnits] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!objectiveText.trim()) return;
    setSubmitting(true);
    setError(null);
    setResult(null);
    const unitList = units.trim() ? units.split(",").map((u) => u.trim()).filter(Boolean) : [];
    const res = await tryPost("/api/portal/requests", { objective_text: objectiveText, units: unitList });
    setSubmitting(false);
    if (res.ok) {
      setResult(res.data);
      setObjectiveText("");
      setUnits("");
      if (onSubmitted) onSubmitted();
    } else if (res.status === 422) {
      setError(`Governed refusal: ${JSON.stringify(res.data)}`);
    } else if (res.status === 404) {
      setError("Endpoint not yet mounted on this backend instance (POST /api/portal/requests returns 404).");
    } else if (res.status === 401) {
      setError("Authentication required. Please sign in.");
    } else {
      setError(res.error || `Unexpected response: ${res.status}`);
    }
  }, [objectiveText, units, onSubmitted]);

  if (!user) return null;

  return (
    <div data-testid="request-submit-form" className="rounded-lg border p-4 mb-6" style={{ borderColor: "var(--line)", background: "white" }}>
      <h2 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>
        <Send size={14} className="inline mr-1.5" />
        Submit a new request
      </h2>
      <form onSubmit={handleSubmit}>
        <div className="space-y-3">
          <div>
            <label htmlFor="objective-text" className="text-xs block mb-1" style={{ color: "var(--ink2)" }}>
              Objective (frozen once submitted)
            </label>
            <textarea
              id="objective-text"
              data-testid="submit-objective-text"
              value={objectiveText}
              onChange={(e) => setObjectiveText(e.target.value)}
              placeholder="Describe what you need from the data estate..."
              className="w-full text-sm px-3 py-2 rounded border resize-none"
              style={{ borderColor: "var(--hair)", minHeight: "80px" }}
              required
            />
          </div>
          <div>
            <label htmlFor="submit-units" className="text-xs block mb-1" style={{ color: "var(--ink2)" }}>
              Units (comma-separated, optional)
            </label>
            <input
              id="submit-units"
              data-testid="submit-units"
              value={units}
              onChange={(e) => setUnits(e.target.value)}
              placeholder="unit-a, unit-b"
              className="w-full text-sm px-3 py-2 rounded border"
              style={{ borderColor: "var(--hair)" }}
            />
          </div>
          <button
            type="submit"
            data-testid="submit-request-btn"
            disabled={submitting || !objectiveText.trim()}
            className="text-xs px-4 py-2 rounded font-medium transition-colors disabled:opacity-50"
            style={{ background: "var(--blue)", color: "white" }}
          >
            {submitting ? "Submitting\u2026" : "Submit request"}
          </button>
        </div>
      </form>
      {result && (
        <div data-testid="submit-result" className="mt-3 rounded p-3 text-xs" style={{ background: "rgba(29,122,110,.06)", color: "var(--sage)" }}>
          Request accepted. Outcome: {result.outcome || "accepted"}. Authority: {result.authority || "delegated"}.
        </div>
      )}
      {error && (
        <div data-testid="submit-error" className="mt-3 rounded p-3 text-xs" style={{ background: "rgba(184,57,91,.06)", color: "var(--oxblood)" }}>
          {error}
        </div>
      )}
    </div>
  );
}

/* ── Request Card ──────────────────────────────────────── */
function RequestCard({ req, onRefresh }) {
  const [expanded, setExpanded] = useState(false);
  const [stopDialogOpen, setStopDialogOpen] = useState(false);
  const [stopLoading, setStopLoading] = useState(false);
  const [stopResult, setStopResult] = useState(null);
  const [retryLoading, setRetryLoading] = useState(false);
  const [retryResult, setRetryResult] = useState(null);
  const blockMeta = req.blockKind ? BLOCK_KIND_META[req.blockKind] : null;

  const waitDays = req.submittedAtISO ? daysBetween(req.submittedAtISO, null) : null;
  const resolvedKindLine = blockMeta ? blockMeta.kindLine : null;
  const resolvedWhatNext = (() => {
    if (!blockMeta) return null;
    if (req.blockKind === "estate") return BLOCK_WHATNEXT_ESTATE_TPL(req.dataOwner || "the data owner");
    return blockMeta.whatNext || null;
  })();

  // Stop handler — wired to POST /api/portal/requests/{id}/stop
  const handleStop = useCallback(async () => {
    setStopLoading(true);
    const res = await tryPost(`/api/portal/requests/${req.id}/stop`);
    setStopLoading(false);
    if (res.ok) {
      setStopResult(res.data);
      setStopDialogOpen(false);
      if (onRefresh) onRefresh();
    } else if (res.status === 409) {
      setStopResult({ error: true, detail: res.data?.detail || "Request is not currently Executing." });
    } else {
      setStopResult({ error: true, detail: res.error || `Stop failed (${res.status})` });
    }
  }, [req.id, onRefresh]);

  // Retry handler — wired to POST /api/portal/requests/{id}/retry
  const handleRetry = useCallback(async () => {
    setRetryLoading(true);
    const res = await tryPost(`/api/portal/requests/${req.id}/retry`);
    setRetryLoading(false);
    if (res.ok) {
      setRetryResult(res.data);
      if (onRefresh) onRefresh();
    } else {
      setRetryResult({ error: true, detail: res.data?.detail || res.error || `Retry failed (${res.status})` });
    }
  }, [req.id, onRefresh]);

  return (
    <div
      data-testid={`request-card-${req.id}`}
      className="rounded-lg border overflow-hidden transition-shadow hover:shadow-sm"
      style={{ borderColor: "var(--line)", background: "white" }}
    >
      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs font-mono" style={{ color: "var(--ink3)" }}>{req.id}</span>
              <StatusBadge status={req.status} />
              {req.status === "Blocked" && req.blockKind && (
                <StatusBadge status={`Blocked \u00b7 ${req.blockKind}`} />
              )}
            </div>
            <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>{req.objective}</p>
          </div>
          <button
            data-testid={`request-expand-${req.id}`}
            onClick={() => setExpanded(!expanded)}
            className="p-1 rounded hover:bg-black/5 transition-colors"
            aria-label={expanded ? "Collapse" : "Expand"}
          >
            {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>
        </div>

        <div className="flex flex-wrap gap-3 text-xs" style={{ color: "var(--ink3)" }}>
          <span>{req.mode && MODE_VERB[req.mode] ? MODE_VERB[req.mode] : req.mode}</span>
          <span>&middot;</span>
          <span>{req.agreement}</span>
          <span>&middot;</span>
          <span>{req.submitted}</span>
        </div>

        {/* In Approval: spend-ceiling breach folded in with reason */}
        {req.status === "In Approval" && req.spendCeilingBreach && (
          <div className="mt-2 text-xs p-2 rounded" style={{ background: "rgba(176,141,46,.08)", color: "var(--brass)" }}>
            <AlertTriangle size={12} className="inline mr-1" />
            {req.spendCeilingReason}
          </div>
        )}

        {/* In Approval: waiting line (TC-INA-06) */}
        {req.status === "In Approval" && req.windowEndsAtISO && waitDays != null && (
          <p data-testid={`in-approval-waiting-${req.id}`} className="mt-2 text-xs" style={{ color: "var(--brass)" }}>
            {IN_APPROVAL_WAITING_TPL(
              req.dataOwner || "the data owner",
              new Date(req.windowEndsAtISO).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }),
              waitDays
            )}
          </p>
        )}

        {/* Interrupted state with retry counter + retry action */}
        {req.status === "Interrupted (platform fault)" && (
          <div className="mt-2">
            <div className="flex items-center gap-2 text-xs p-2 rounded" style={{ background: "rgba(184,57,91,.06)", color: "var(--oxblood)" }}>
              <RotateCcw size={12} />
              <span>
                Auto-retry attempt {req.retryAttempts || 0} of {req.maxRetries || 3}
                {(req.retryAttempts || 0) >= (req.maxRetries || 3) && " \u2014 exhausted, resolves to Blocked \u00b7 check"}
              </span>
            </div>
            {(req.retryAttempts || 0) < (req.maxRetries || 3) && (
              <button
                data-testid={`retry-btn-${req.id}`}
                onClick={handleRetry}
                disabled={retryLoading}
                className="mt-2 flex items-center gap-1.5 text-xs px-2.5 py-1 rounded border transition-colors hover:bg-blue-50 disabled:opacity-50"
                style={{ borderColor: "var(--blue)", color: "var(--blue)" }}
              >
                <RotateCcw size={10} /> {retryLoading ? "Retrying\u2026" : "Retry"}
              </button>
            )}
            {retryResult && retryResult.error && (
              <p className="mt-1 text-[10px]" style={{ color: "var(--oxblood)" }}>{retryResult.detail}</p>
            )}
          </div>
        )}

        {/* Executing: progress + Stop action (TC-BLK-24) */}
        {req.status === "Executing" && (
          <div className="mt-2">
            {req.pct != null && (
              <>
                <div className="flex items-center justify-between text-xs mb-1" style={{ color: "var(--ink3)" }}>
                  <span>{req.stageLabel || "Processing"}</span>
                  <span>{req.eta}</span>
                </div>
                <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "var(--line)" }}>
                  <div className="h-full rounded-full transition-all" style={{ width: `${req.pct}%`, background: "var(--accent)" }} />
                </div>
              </>
            )}
            {req.stageIndex != null && req.pct == null && (
              <div className="flex items-center justify-between text-xs" style={{ color: "var(--ink3)" }}>
                <span>Step {req.stageIndex} of {req.stageCount} &mdash; {req.stageLabel}</span>
                <span>{req.eta}</span>
              </div>
            )}
            <button
              data-testid={`stop-btn-${req.id}`}
              onClick={() => setStopDialogOpen(true)}
              className="mt-2 flex items-center gap-1.5 text-xs px-2.5 py-1 rounded border transition-colors hover:bg-red-50"
              style={{ borderColor: "var(--oxblood)", color: "var(--oxblood)" }}
            >
              <Square size={10} /> Stop
            </button>
          </div>
        )}

        {/* Stop confirm dialog (TC-BLK-24) — request-scoped copy, NEVER party-halt framing */}
        {stopDialogOpen && (
          <div data-testid={`stop-confirm-${req.id}`} className="mt-2 border rounded-lg p-3" style={{ borderColor: "var(--oxblood)", background: "rgba(184,57,91,.04)" }}>
            <p className="text-sm mb-3" style={{ color: "var(--ink)" }}>
              {STOP_CONFIRM}
            </p>
            <div className="flex gap-2">
              <button
                data-testid={`stop-confirm-yes-${req.id}`}
                className="text-xs px-3 py-1.5 rounded font-medium text-white disabled:opacity-50"
                style={{ background: "var(--oxblood)" }}
                disabled={stopLoading}
                onClick={handleStop}
              >
                {stopLoading ? "Stopping\u2026" : "Stop"}
              </button>
              <button
                data-testid={`stop-confirm-cancel-${req.id}`}
                className="text-xs px-3 py-1.5 rounded border"
                style={{ borderColor: "var(--hair)", color: "var(--ink2)" }}
                onClick={() => setStopDialogOpen(false)}
              >
                Cancel
              </button>
            </div>
            {stopResult && stopResult.error && (
              <p className="mt-2 text-[10px]" style={{ color: "var(--oxblood)" }}>{stopResult.detail}</p>
            )}
          </div>
        )}

        {/* Stopped terminal state — charged-to-point-of-stop, receipted */}
        {req.status === "Stopped" && (
          <div className="mt-2 text-xs p-2 rounded" style={{ background: "rgba(27,31,39,.04)", color: "var(--ink2)" }}>
            <Square size={10} className="inline mr-1" style={{ color: "var(--oxblood)" }} />
            Stopped{req.stoppedAt ? ` at ${req.stoppedAt}` : ""}.
            {req.pctAtStop != null && ` Charged to ${req.pctAtStop}% completion.`}
            {" "}Receipted.
          </div>
        )}

        {/* Ready state */}
        {req.status === "Ready" && req.modelId && (
          <div className="mt-2 text-xs" style={{ color: "var(--ink3)" }}>
            <span>Model: {req.modelId} &middot; Base: {req.baseModel}</span>
            {req.weightsHash && <span className="ml-2 font-mono">{req.weightsHash}</span>}
          </div>
        )}
      </div>

      {/* Expanded drawer */}
      {expanded && (
        <div className="border-t px-4 py-3 text-sm space-y-3" style={{ borderColor: "var(--line)", background: "var(--surface)" }}>
          {req.submittedBy && <p style={{ color: "var(--ink2)" }}>Submitted by {req.submittedBy}</p>}
          {req.scope && <p style={{ color: "var(--ink3)" }}>Scope: {req.scope}</p>}

          {/* In Approval drawer (TC-INA-06) */}
          {req.status === "In Approval" && (
            <div data-testid={`drawer-in-approval-${req.id}`} className="mt-1 space-y-2">
              {req.signoffReason && (
                <p className="text-sm" style={{ color: "var(--ink2)" }}>{req.signoffReason}</p>
              )}
              {req.windowEndsAtISO && waitDays != null && (
                <p className="text-sm" style={{ color: "var(--brass)" }}>
                  {IN_APPROVAL_WAITING_TPL(
                    req.dataOwner || "the data owner",
                    new Date(req.windowEndsAtISO).toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" }),
                    waitDays
                  )}
                </p>
              )}
            </div>
          )}

          {/* Blocked drawer — three kinds: request / check / estate */}
          {req.status === "Blocked" && blockMeta && (
            <div
              data-testid={`drawer-blocked-${req.blockKind}-${req.id}`}
              className="border-l-4 p-3 rounded"
              style={{ borderColor: "var(--oxblood)", background: "rgba(184,57,91,.04)" }}
            >
              {blockMeta.showProgress === true && req.pctAtStop != null && (
                <div className="mb-2">
                  <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "var(--line)" }}>
                    <div className="h-full rounded-full" style={{ width: `${req.pctAtStop}%`, background: "var(--oxblood)" }} />
                  </div>
                  <p className="text-[10px] mt-0.5" style={{ color: "var(--oxblood)" }}>
                    Stopped at {req.pctAtStop}% &middot; {req.blockedAt}
                  </p>
                </div>
              )}
              <p data-testid={`block-kind-line-${req.id}`} className="text-xs font-medium mb-1" style={{ color: "var(--oxblood)" }}>
                {resolvedKindLine}
              </p>
              {req.blockKind === "estate" && (
                <p className="text-sm" style={{ color: "var(--ink2)" }}>{BLOCK_ESTATE_REASON}</p>
              )}
              {(req.blockKind === "request" || req.blockKind === "check") && req.blockReason && (
                <p className="text-sm" style={{ color: "var(--ink2)" }}>{req.blockReason}</p>
              )}
              {req.blockRef && req.blockKind !== "estate" && (
                <p className="text-xs font-mono mt-1" style={{ color: "var(--ink3)" }}>Reference {req.blockRef}</p>
              )}
              {resolvedWhatNext && (
                <p data-testid={`block-whatnext-${req.id}`} className="text-xs mt-2" style={{ color: "var(--ink3)" }}>{resolvedWhatNext}</p>
              )}
              {blockMeta.showCopy && (
                <button data-testid={`copy-new-request-${req.id}`} className="mt-2 text-xs px-3 py-1.5 rounded border transition-colors hover:bg-white" style={{ borderColor: "var(--hair)", color: "var(--ink)" }}>
                  Copy into a new request
                </button>
              )}
            </div>
          )}

          {/* party_halted drawer — own rail state, NOT a Blocked variant */}
          {req.status === "party_halted" && (
            <div data-testid={`drawer-party-halted-${req.id}`} className="border-l-4 p-3 rounded" style={{ borderColor: "var(--oxblood)", background: "rgba(184,57,91,.04)" }}>
              {req.pctAtStop != null && (
                <div className="mb-2">
                  <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "var(--line)" }}>
                    <div className="h-full rounded-full" style={{ width: `${req.pctAtStop}%`, background: "var(--oxblood)" }} />
                  </div>
                  <p className="text-[10px] mt-0.5" style={{ color: "var(--oxblood)" }}>Stopped at {req.pctAtStop}% &middot; {req.blockedAt}</p>
                </div>
              )}
              <p data-testid={`party-halted-kind-line-${req.id}`} className="text-xs font-medium mb-1" style={{ color: "var(--oxblood)" }}>{PARTY_HALTED_KIND_LINE}</p>
              {req.blockedBy && <p className="text-xs mt-1" style={{ color: "var(--ink3)" }}>Stopped by {req.blockedBy}</p>}
              {req.blockRef && <p className="text-xs font-mono mt-1" style={{ color: "var(--ink3)" }}>Reference {req.blockRef}</p>}
              <p data-testid={`party-halted-whatnext-${req.id}`} className="text-xs mt-2" style={{ color: "var(--ink3)" }}>{PARTY_HALTED_WHAT_NEXT}</p>
              <button data-testid={`copy-new-request-${req.id}`} className="mt-2 text-xs px-3 py-1.5 rounded border transition-colors hover:bg-white" style={{ borderColor: "var(--hair)", color: "var(--ink)" }}>
                Copy into a new request
              </button>
            </div>
          )}

          {/* Stopped drawer — terminal state, receipted */}
          {req.status === "Stopped" && (
            <div data-testid={`drawer-stopped-${req.id}`} className="border-l-4 p-3 rounded" style={{ borderColor: "var(--ink3)", background: "rgba(27,31,39,.04)" }}>
              <p className="text-xs font-medium mb-1" style={{ color: "var(--ink)" }}>
                This request was stopped by the requester.
              </p>
              {req.pctAtStop != null && (
                <p className="text-xs" style={{ color: "var(--ink2)" }}>Charged to {req.pctAtStop}% of execution. Receipted.</p>
              )}
              {req.stoppedAt && <p className="text-xs" style={{ color: "var(--ink3)" }}>Stopped at {req.stoppedAt}</p>}
            </div>
          )}

          {/* Expired drawer (TC-EXP-02) */}
          {req.status === "Expired" && (
            <div data-testid={`drawer-expired-${req.id}`} className="p-3 rounded space-y-2" style={{ background: "rgba(27,31,39,.04)" }}>
              <p data-testid={`expired-date-line-${req.id}`} className="text-sm font-medium" style={{ color: "var(--ink)" }}>
                {EXPIRED_DATE_TPL(req.expiredAtDisplay || "")}
              </p>
              <p data-testid={`expired-waited-line-${req.id}`} className="text-sm" style={{ color: "var(--ink2)" }}>
                {EXPIRED_WAITED_TPL(
                  req.submittedAtISO && req.expiredAtISO ? daysBetween(req.submittedAtISO, req.expiredAtISO) : 14
                )}
              </p>
              {req.addressedTo && <p className="text-sm" style={{ color: "var(--ink3)" }}>It was addressed to {req.addressedTo}.</p>}
              {req.signoffReason && <p className="text-sm" style={{ color: "var(--ink3)" }}>{req.signoffReason}</p>}
              <p data-testid={`expired-meaning-${req.id}`} className="text-sm" style={{ color: "var(--ink2)" }}>{EXPIRED_MEANING_TPL(req.dataOwner || "the data owner")}</p>
              <p data-testid={`expired-whatnext-${req.id}`} className="text-sm" style={{ color: "var(--ink2)" }}>{EXPIRED_WHAT_NEXT_TPL(req.dataOwner || "the data owner")}</p>
              <button data-testid={`copy-new-request-${req.id}`} className="mt-1 text-xs px-3 py-1.5 rounded border transition-colors hover:bg-white" style={{ borderColor: "var(--hair)", color: "var(--ink)" }}>
                Submit again as a new request
              </button>
            </div>
          )}

          {/* Refused drawer — NO "Waited N days" (hard omission) */}
          {req.status === "Refused" && req.refusalReason && (
            <div className="border-l-4 p-3 rounded" style={{ borderColor: "var(--ink)", background: "rgba(27,31,39,.03)" }}>
              <p className="text-sm" style={{ color: "var(--ink2)" }}>{req.refusalReason}</p>
            </div>
          )}

          {/* Retrieved */}
          {req.status === "Retrieved" && req.retrievedAt && (
            <p className="mt-1" style={{ color: "var(--sage)" }}>
              <CheckCircle size={12} className="inline mr-1" />
              Retrieved {req.retrievedAt}
            </p>
          )}

          {/* Sign-off block — NO "Waited N days" (hard omission), NO approver identity (DAP-15) */}
          {req.approvedByRole && req.status !== "In Approval" && (
            <p className="mt-1" style={{ color: "var(--ink3)" }}>
              Approved by {req.approvedByRole} on {req.approvedDate}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

/* ── Main component ────────────────────────────────────── */
export default function RequestLifecycle() {
  const { user } = useAuth();
  const [filter, setFilter] = useState("Total");
  const [liveRows, setLiveRows] = useState(null);
  const [liveError, setLiveError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchRequests = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    const res = await tryGet("/api/portal/requests");
    setLoading(false);
    if (res.ok && res.data && Array.isArray(res.data.rows)) {
      setLiveRows(res.data.rows);
      setLiveError(null);
    } else if (res.status === 404) {
      setLiveError("Endpoint not yet mounted (GET /api/portal/requests returns 404). Showing reference state machine.");
      setLiveRows(null);
    } else if (res.status === 401) {
      setLiveError("Authentication required for request history.");
      setLiveRows(null);
    } else {
      setLiveError(res.error || "Failed to fetch requests.");
      setLiveRows(null);
    }
  }, [user]);

  useEffect(() => { fetchRequests(); }, [fetchRequests]);

  const requests = liveRows && liveRows.length > 0 ? liveRows : SAMPLE_REQUESTS;
  const usingLive = liveRows !== null && liveRows.length > 0;

  const counts = {};
  for (const r of requests) {
    counts[r.status] = (counts[r.status] || 0) + 1;
  }
  counts["Total"] = requests.length;

  const filtered = filter === "Total"
    ? requests
    : requests.filter((r) => r.status === filter);

  return (
    <div data-testid="request-lifecycle" className="max-w-5xl mx-auto px-8 py-10">
      <h1
        data-testid="request-lifecycle-title"
        className="text-xl font-semibold mb-1"
        style={{ color: "var(--ink)", fontFamily: "var(--head)" }}
      >
        Request Lifecycle
      </h1>
      <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
        Every request passes through a state machine. This view shows the full lifecycle.
      </p>

      {/* Submit form (JWT-gated) */}
      <SubmitForm onSubmitted={fetchRequests} />

      {/* State machine legend */}
      <div data-testid="state-machine-legend" className="mb-6">
        <h2 className="text-sm font-medium mb-3" style={{ color: "var(--ink)" }}>State Legend</h2>
        <div className="flex flex-wrap gap-2">
          {ALL_STATES.map((s) => (
            <StatusBadge key={s} status={s} />
          ))}
        </div>
      </div>

      {/* Rail counts */}
      <div data-testid="request-rail" className="rounded-lg border mb-6" style={{ borderColor: "var(--line)", background: "white" }}>
        <div className="grid grid-cols-11 text-center">
          {RAIL_ROW.map(([key, label]) => (
            <button
              key={key}
              data-testid={`rail-${key.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`}
              onClick={() => setFilter(key)}
              className={`py-3 text-xs transition-colors border-b-2 ${
                filter === key ? "font-semibold" : "hover:bg-black/[.02]"
              }`}
              style={{
                borderBottomColor: filter === key ? "var(--blue)" : "transparent",
                color: filter === key ? "var(--ink)" : "var(--ink3)",
              }}
            >
              <span className="block text-lg font-semibold">{counts[key] || 0}</span>
              <span>{label}</span>
            </button>
          ))}
        </div>
      </div>

      {loading && <LoadingState message="Loading requests\u2026" />}

      {/* Request cards */}
      <div className="space-y-3" data-testid="request-list">
        {filtered.map((req) => (
          <RequestCard key={req.id} req={req} onRefresh={fetchRequests} />
        ))}
        {filtered.length === 0 && !loading && (
          <div className="text-center py-8">
            <p className="text-sm" style={{ color: "var(--ink3)" }}>No requests in this state.</p>
          </div>
        )}
      </div>

      {/* Backend status notice */}
      {liveError && (
        <div data-testid="request-backend-notice" className="mt-8 rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
          <p className="text-xs font-medium mb-1" style={{ color: "var(--brass)" }}>
            <Clock size={12} className="inline mr-1" />
            Endpoint not yet mounted
          </p>
          <p className="text-xs" style={{ color: "var(--ink3)" }}>{liveError}</p>
        </div>
      )}
      {!liveError && !usingLive && !loading && (
        <div className="mt-8 rounded-lg border p-4" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
          <p className="text-xs font-medium mb-1" style={{ color: "var(--brass)" }}>Reference state machine</p>
          <p className="text-xs" style={{ color: "var(--ink3)" }}>
            The requests shown above are the reference state machine rendered from the DAP design specification.
            Once the backend portal endpoints are mounted, this view will display real request data.
          </p>
        </div>
      )}
    </div>
  );
}
