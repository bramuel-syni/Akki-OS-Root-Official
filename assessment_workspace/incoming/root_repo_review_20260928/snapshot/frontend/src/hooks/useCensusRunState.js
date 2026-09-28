/**
 * useCensusRunState — real-scheduler-state polling hook.
 *
 * Owner directive verbatim (PHASE 3 continuation A''):
 *   "the UI must show REAL scheduler state only — the running card polls
 *    the service's own state, never synthesized progress."
 *
 * This hook polls GET /api/portal/census/runs/{census_run_id}/state
 * every POLL_INTERVAL_MS and returns EXACTLY what the endpoint returns.
 * It never fabricates progress, ETA, or random values. When the endpoint
 * returns 404 (unknown id), state is set to null. When the poll fails
 * (network error), the previous state is preserved and an error is
 * surfaced separately.
 *
 * Backend contract: services/census_autonomy/state_reader.py returns
 *   { status: "PENDING" | "COMPLETE" | "REFUSED", ...fields }
 * or null → 404.
 */
import { useEffect, useRef, useState } from "react";

const POLL_INTERVAL_MS = 5000;

export function useCensusRunState(censusRunId, jwtToken) {
  const [state, setState] = useState(null);
  const [error, setError] = useState(null);
  const activeRef = useRef(true);

  useEffect(() => {
    activeRef.current = true;
    if (!censusRunId) {
      setState(null);
      setError(null);
      return () => { activeRef.current = false; };
    }

    async function fetchOnce() {
      try {
        const resp = await fetch(
          `${process.env.REACT_APP_BACKEND_URL}/api/portal/census/runs/${encodeURIComponent(censusRunId)}/state`,
          {
            headers: jwtToken
              ? { "Authorization": `Bearer ${jwtToken}` }
              : {},
          }
        );
        if (!activeRef.current) return;
        if (resp.status === 404) {
          setState(null);
          setError(null);
          return;
        }
        if (!resp.ok) {
          setError(`state fetch failed: HTTP ${resp.status}`);
          return;
        }
        const doc = await resp.json();
        if (!activeRef.current) return;
        // Store REAL state verbatim; do not derive progress percent.
        setState(doc);
        setError(null);
      } catch (e) {
        if (!activeRef.current) return;
        setError(String(e));
      }
    }

    fetchOnce();
    const handle = setInterval(fetchOnce, POLL_INTERVAL_MS);
    return () => {
      activeRef.current = false;
      clearInterval(handle);
    };
  }, [censusRunId, jwtToken]);

  return { state, error };
}
