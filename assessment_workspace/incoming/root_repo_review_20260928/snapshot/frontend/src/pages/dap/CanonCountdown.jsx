import React, { useState, useEffect } from "react";
import LoadingState from "@/components/shared/LoadingState";
import { tryGet } from "@/lib/apiClient";
import { Clock, AlertCircle, Shield } from "lucide-react";

/**
 * CanonCountdown — R-91 live evidence horizon countdown surface.
 *
 * Consumes GET /api/canon/rules/rbm-8-ceremony-mechanic BYTE-VERBATIM.
 * Per owner CONDITION (e): no client-side rewriting of:
 *   - r91_live_evidence_horizon_utc
 *   - ceremony_window_is_rigid
 *   - no_shortening_path_in_code
 *   - r91_is_live_evidence_receipt
 *
 * Displays exactly what the endpoint returns. Zero client-side rewriting.
 */

export default function CanonCountdown() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [errorStatus, setErrorStatus] = useState(null);

  useEffect(() => {
    tryGet("/api/canon/rules/rbm-8-ceremony-mechanic").then((res) => {
      setLoading(false);
      if (res.ok) {
        setData(res.data);
      } else {
        setErrorStatus(res.status);
        setError(res.error || `Endpoint returned ${res.status}`);
      }
    });
  }, []);

  if (loading) return <LoadingState message="Reading RBM-8 ceremony mechanic\u2026" />;

  return (
    <div data-testid="canon-countdown" className="max-w-5xl mx-auto px-8 py-10">
      <h1
        data-testid="canon-countdown-title"
        className="text-xl font-semibold mb-1"
        style={{ color: "var(--ink)", fontFamily: "var(--head)" }}
      >
        <Clock size={20} className="inline mr-2" />
        R-91 Ceremony Countdown
      </h1>
      <p className="text-sm mb-6" style={{ color: "var(--ink3)" }}>
        Live evidence horizon surface. Values below are rendered BYTE-VERBATIM from the backend.
      </p>

      {errorStatus === 404 && (
        <div data-testid="countdown-pending" className="rounded-lg border p-5" style={{ borderColor: "var(--brass)", background: "rgba(176,141,46,.04)" }}>
          <div className="flex items-center gap-2 mb-2">
            <AlertCircle size={16} style={{ color: "var(--brass)" }} />
            <p className="text-sm font-medium" style={{ color: "var(--brass)" }}>Endpoint not yet mounted</p>
          </div>
          <p className="text-xs" style={{ color: "var(--ink3)" }}>
            GET /api/canon/rules/rbm-8-ceremony-mechanic returns 404. The R-99 canon rules router is committed but not mounted on this backend instance.
          </p>
        </div>
      )}

      {error && errorStatus !== 404 && (
        <div className="rounded-lg border p-4" style={{ borderColor: "var(--oxblood)", background: "rgba(184,57,91,.04)" }}>
          <p className="text-xs" style={{ color: "var(--oxblood)" }}>{error}</p>
        </div>
      )}

      {data && (
        <div className="space-y-4">
          {/* Main countdown card */}
          <div data-testid="countdown-horizon-card" className="rounded-lg border p-6" style={{ borderColor: "var(--line)", background: "white" }}>
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full flex items-center justify-center" style={{ background: "rgba(22,39,74,.08)" }}>
                <Shield size={20} style={{ color: "var(--blue)" }} />
              </div>
              <div>
                <p className="text-sm font-medium" style={{ color: "var(--ink)" }}>Live Evidence Horizon</p>
                <p className="text-[10px] font-mono" style={{ color: "var(--ink3)" }}>RBM-8 · Ceremony Mechanic</p>
              </div>
            </div>

            {/* BYTE-VERBATIM fields — no client-side rewriting */}
            <div className="space-y-3">
              {data.r91_live_evidence_horizon_utc != null && (
                <div data-testid="countdown-horizon-utc" className="rounded border p-3" style={{ borderColor: "var(--line)" }}>
                  <p className="text-[10px] uppercase tracking-widest mb-1" style={{ color: "var(--ink3)" }}>r91_live_evidence_horizon_utc</p>
                  <p className="text-lg font-mono font-semibold" style={{ color: "var(--blue)" }}>
                    {String(data.r91_live_evidence_horizon_utc)}
                  </p>
                </div>
              )}

              {data.ceremony_window_is_rigid != null && (
                <div data-testid="countdown-rigid" className="rounded border p-3" style={{ borderColor: "var(--line)" }}>
                  <p className="text-[10px] uppercase tracking-widest mb-1" style={{ color: "var(--ink3)" }}>ceremony_window_is_rigid</p>
                  <p className="text-sm font-mono font-medium" style={{ color: data.ceremony_window_is_rigid ? "var(--oxblood)" : "var(--sage)" }}>
                    {String(data.ceremony_window_is_rigid)}
                  </p>
                </div>
              )}

              {data.no_shortening_path_in_code != null && (
                <div data-testid="countdown-no-shortening" className="rounded border p-3" style={{ borderColor: "var(--line)" }}>
                  <p className="text-[10px] uppercase tracking-widest mb-1" style={{ color: "var(--ink3)" }}>no_shortening_path_in_code</p>
                  <p className="text-sm font-mono font-medium" style={{ color: "var(--ink)" }}>
                    {String(data.no_shortening_path_in_code)}
                  </p>
                </div>
              )}

              {data.r91_is_live_evidence_receipt != null && (
                <div data-testid="countdown-receipt" className="rounded border p-3" style={{ borderColor: "var(--line)" }}>
                  <p className="text-[10px] uppercase tracking-widest mb-1" style={{ color: "var(--ink3)" }}>r91_is_live_evidence_receipt</p>
                  <p className="text-sm font-mono font-medium" style={{ color: "var(--ink)" }}>
                    {String(data.r91_is_live_evidence_receipt)}
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Raw JSON — full transparency, byte-verbatim */}
          <div data-testid="countdown-raw" className="rounded-lg border p-4" style={{ borderColor: "var(--line)", background: "var(--surface)" }}>
            <p className="text-[10px] uppercase tracking-widest mb-2" style={{ color: "var(--ink3)" }}>Raw response (byte-verbatim)</p>
            <pre className="text-xs overflow-x-auto whitespace-pre-wrap" style={{ color: "var(--ink2)", fontFamily: "var(--mono, monospace)" }}>
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
