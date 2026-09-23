/**
 * useBuildSkillProvisioning — DAP BuildSkill polling hook.
 *
 * CP-SKILLS-LAYER-SERIES-CLOSE (PHASE 4 · c-vi · Slice 5).
 *
 * Consumes the sealed A18.2 persistence state via the additive backend
 * route `/api/dap/buildskill/provisioning-records`. Returns EXACTLY what
 * the route returns (records[], count). Never fabricates: no synthetic
 * default records array, no cached fallback that could drift from the
 * sealed store — every call is a fresh fetch. `// no fabrication` here
 * per the banked lesson from useCensusRunState.js discipline (never
 * fabricates when the endpoint is unreachable — surfaces the error
 * separately and preserves the previous records).
 *
 * Owner boundary directive verbatim (2026-02-23 · slice open):
 *   "the buildskill surface must show real provisioning state or
 *    honest-gap, and the boundary report must include the tester
 *    walkthrough — the concrete steps a human takes and what they see."
 *
 * Owner R-102 verbatim: "productized-or-honest-gap — the USER-visible bar."
 *
 * Env discipline: uses `process.env.REACT_APP_BACKEND_URL` verbatim.
 * Never hardcodes an origin.
 */
import { useCallback, useEffect, useRef, useState } from "react";

// Paired-equality anchor with backend router's
// PROVISIONING_RECORDS_ROUTE_PATH Final constant. Any drift here fires
// the invariant test's paired-equality pin RED right-reason.
const PROVISIONING_RECORDS_ROUTE_PATH = "/api/dap/buildskill/provisioning-records";

const POLL_INTERVAL_MS = 30000; // 30s · slower than the census badge (15s)
                                 // because provisioning changes are rare.

export function useBuildSkillProvisioning(jwtToken, { autoPoll = true } = {}) {
  const [records, setRecords] = useState([]);
  const [count, setCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastFetchedAt, setLastFetchedAt] = useState(null);
  const intervalRef = useRef(null);

  const fetchOnce = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const base = process.env.REACT_APP_BACKEND_URL || "";
      const url = `${base}${PROVISIONING_RECORDS_ROUTE_PATH}`;
      const headers = { Accept: "application/json" };
      if (jwtToken) {
        headers["Authorization"] = `Bearer ${jwtToken}`;
      }
      const resp = await fetch(url, { headers });
      if (!resp.ok) {
        setError(
          `Request refused (status ${resp.status}). Prior view preserved.`
        );
        setLoading(false);
        return;
      }
      const body = await resp.json();
      // Never fabricates: only set state from the body shape the sealed
      // store produced. Missing keys yield empty arrays / zero count.
      const fetchedRecords = Array.isArray(body?.records) ? body.records : [];
      const fetchedCount =
        typeof body?.count === "number" ? body.count : fetchedRecords.length;
      setRecords(fetchedRecords);
      setCount(fetchedCount);
      setLastFetchedAt(new Date().toISOString());
    } catch (e) {
      setError(
        `Could not reach the buildskill surface. Prior view preserved.`
      );
    } finally {
      setLoading(false);
    }
  }, [jwtToken]);

  useEffect(() => {
    if (!autoPoll) return () => {};
    fetchOnce();
    intervalRef.current = setInterval(fetchOnce, POLL_INTERVAL_MS);
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [autoPoll, fetchOnce]);

  return {
    records,
    count,
    loading,
    error,
    lastFetchedAt,
    triggerRefetch: fetchOnce,
  };
}

export default useBuildSkillProvisioning;
