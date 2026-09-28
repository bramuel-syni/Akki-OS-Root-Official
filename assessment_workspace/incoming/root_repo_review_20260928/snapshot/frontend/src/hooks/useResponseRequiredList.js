/**
 * useResponseRequiredList — real-producer-data polling hook.
 *
 * PHASE 3 continuation A'''-cont-B · CP-CENSUS-AUTONOMY-RESPONSE-
 * REQUIRED-BADGE-UI. Consumes the sealed A'''-cont-A endpoint
 * `GET /api/portal/census/response-required-items` and returns
 * EXACTLY what the endpoint returns (items[], count). Never
 * fabricates.
 *
 * Owner directive verbatim (2026-09-22T~19:40Z at A'''' opening):
 *   "the owner-answerable item text for blocked slices should carry
 *    the exact unblock action ... so the badge in A'''-cont-B is
 *    actionable, not just informative — put that in the item payload
 *    schema now if it needs a field."
 *
 * Owner directive verbatim (2026-09-22T~21:21Z at Phase 3 closure):
 *   "Proceed: A'''-cont-B (badge + polling on real producer data)"
 *
 * The sealed A'''' adapter embeds the actionable unblock action inside
 * the sealed queue's `reason_text` field via the machine-parseable
 * marker prefix `[UNBLOCK action_class=<code>] <detail>` — the badge
 * consumes that marker to render the actionable owner-answerable item.
 *
 * Never fabricates: no synthetic progress, no synthetic items, no
 * count interpolation. When the endpoint returns HTTP 4xx/5xx, the
 * previous items are preserved and an error is surfaced separately
 * (banked lesson from A'' useCensusRunState.js discipline).
 *
 * Env discipline: uses `process.env.REACT_APP_BACKEND_URL` verbatim.
 * Never hardcodes an origin.
 */
import { useEffect, useRef, useState } from "react";

const POLL_INTERVAL_MS = 15000;

export function useResponseRequiredList(jwtToken, { autoPoll = true } = {}) {
  const [items, setItems] = useState([]);
  const [count, setCount] = useState(0);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const activeRef = useRef(true);
  const [refetchTick, setRefetchTick] = useState(0);

  const triggerRefetch = () => setRefetchTick((t) => t + 1);

  useEffect(() => {
    activeRef.current = true;
    if (!jwtToken) {
      setItems([]);
      setCount(0);
      setError(null);
      return () => {
        activeRef.current = false;
      };
    }

    async function fetchOnce() {
      setLoading(true);
      try {
        const resp = await fetch(
          `${process.env.REACT_APP_BACKEND_URL}/api/portal/census/response-required-items`,
          {
            headers: { Authorization: `Bearer ${jwtToken}` },
          }
        );
        if (!activeRef.current) return;
        if (!resp.ok) {
          setError(`response-required-items fetch failed: HTTP ${resp.status}`);
          setLoading(false);
          return;
        }
        const doc = await resp.json();
        if (!activeRef.current) return;
        // Store REAL producer data verbatim; do NOT derive fabricated fields.
        setItems(Array.isArray(doc.items) ? doc.items : []);
        setCount(typeof doc.count === "number" ? doc.count : 0);
        setError(null);
        setLoading(false);
      } catch (e) {
        if (!activeRef.current) return;
        setError(String(e));
        setLoading(false);
      }
    }

    fetchOnce();
    if (!autoPoll) {
      return () => {
        activeRef.current = false;
      };
    }
    const handle = setInterval(fetchOnce, POLL_INTERVAL_MS);
    return () => {
      activeRef.current = false;
      clearInterval(handle);
    };
  }, [jwtToken, autoPoll, refetchTick]);

  return { items, count, error, loading, triggerRefetch };
}
