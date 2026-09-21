import { useEffect, useRef, useState } from "react";
import { applySubstitutions } from "@/lib/v8SubstitutionEngine";

/**
 * OSPrototype — PortalIframe wrapper restored from pod_shell V8-shell-port.
 *
 * R-91 CP-APP-JS-UNIFY · Option A · substitution engine restored into the
 * React tree via @/lib/v8SubstitutionEngine.js (37 named rules, window
 * .V8_SUBSTITUTIONS_DUMMIES exposure, MutationObserver re-application).
 *
 * This component wraps /v8_prototype.html in an iframe, fetches live values
 * from 3 backend endpoints, and drives the substitution engine against the
 * iframe's contentDocument on every dc-runtime re-render.
 *
 * data-testid="v8-portal-iframe-host" — harness sentinel (outer div)
 * data-testid="v8-prototype-iframe"   — iframe element
 */
export default function OSPrototype() {
  const iframeRef = useRef(null);
  // Monotonic counter of successful substitutions this session — surfaced
  // as data-substitution-applied on the outer iframe host div so external
  // harnesses can prove substitutions actually ran without reading into
  // the prototype's DOM.
  const [substitutionsApplied, setSubstitutionsApplied] = useState(0);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    let observer = null;
    let scheduled = false;
    const liveValues = {
      estateSources: null,
      estateTables: null,
      lastCensus: null,
      totalVolume: null,
      shareMeasured: null,
      opportunities: null,
      compute: null,
    };

    const applyAll = () => {
      if (scheduled) return; // Debounce burst mutations from dc-runtime.
      scheduled = true;
      const run = () => {
        scheduled = false;
        const doc = iframe.contentDocument;
        if (!doc || !doc.body) return;
        const count = applySubstitutions(doc, liveValues);
        // Wave-H · harness instrumentation: emit a console line each time
        // applyAll runs so the real-Chromium harness can see the engine's
        // liveness independently of React state.
        try {
          console.log(
            `wave_g5_substitutions applyAll_run count=${count} bodyLen=${(doc.body.textContent || "").length}`
          );
        } catch (_) {
          /* no-op */
        }
        if (count > 0) {
          setSubstitutionsApplied((prev) => prev + count);
        }
      };
      if (typeof window !== "undefined" && window.requestAnimationFrame) {
        window.requestAnimationFrame(run);
      } else {
        setTimeout(run, 0);
      }
    };

    const onLoad = async () => {
      // Pull live values (silent — HONEST-EMPTY fallback fires when null).
      const backend = process.env.REACT_APP_BACKEND_URL || "";

      // (1) Registry facts — connected sources + table count.
      try {
        const res = await fetch(`${backend}/api/registry/facts`);
        if (res.ok) {
          const facts = await res.json();
          if (facts && Array.isArray(facts.data_sources)) {
            liveValues.estateSources = facts.data_sources.length;
            let tables = 0;
            for (const s of facts.data_sources) {
              if (typeof s.table_count === "number") tables += s.table_count;
            }
            liveValues.estateTables = tables;
          }
        }
      } catch (_) {
        /* silent */
      }

      // (2) Wave-G5c · census status line + estate scale from live
      // census output (owner Stage 3 wiring: Registry reads from
      // /api/census/latest wherever the census provides the truer
      // figure). Census manifest fields land as:
      //   lastCensus.number    ← census_id
      //   lastCensus.date      ← finished_at_utc (formatted)
      //   lastCensus.author    ← initiator
      //   lastCensus.notMeasuredPct  ← honest-empty (census walks
      //     aggregates, not size-in-bytes)
      // estateTables also updates from rollup.table_count (census is
      // authoritative once it has run — walks EVERY table, not the
      // truncated top-25 in the connection record).
      try {
        const res = await fetch(`${backend}/api/census/latest`);
        if (res.ok) {
          const body = await res.json();
          const c = body && body.census;
          if (c && c.census_id != null) {
            const finished = (c.finished_at_utc || "").slice(0, 10);
            liveValues.lastCensus = {
              number: c.census_id,
              date: finished || "recent",
              author: c.initiator || "owner",
              notMeasuredPct: "size",
            };
            if (c.rollup && typeof c.rollup.table_count === "number") {
              liveValues.estateTables = c.rollup.table_count;
            }
            if (c.rollup && typeof c.rollup.database_count === "number") {
              // Census "sees" databases as sources when the connection
              // record hasn't been widened yet.
              if (liveValues.estateSources == null
                  || liveValues.estateSources < c.rollup.database_count) {
                liveValues.estateSources = c.rollup.database_count;
              }
            }
          }
        }
      } catch (_) {
        /* silent */
      }

      // (3) Wave-G5c-COMPUTE-BACKEND · compute descriptor.
      try {
        const res = await fetch(`${backend}/api/compute/estate`);
        if (res.ok) {
          const body = await res.json();
          if (body && Array.isArray(body.hosts)) {
            liveValues.compute = body;
          }
        }
      } catch (_) {
        /* silent */
      }

      // Give dc-runtime time for the first render pass.
      await new Promise((r) => setTimeout(r, 400));
      applyAll();

      // Re-apply on every subsequent dc-runtime re-render (tab switch,
      // Registry mount, drawer open, etc.). Idempotent → safe.
      try {
        const doc = iframe.contentDocument;
        if (doc && doc.body) {
          observer = new MutationObserver(applyAll);
          observer.observe(doc.body, {
            childList: true,
            characterData: true,
            subtree: true,
          });
        }
      } catch (_) {
        /* no-op */
      }
    };

    iframe.addEventListener("load", onLoad);
    return () => {
      iframe.removeEventListener("load", onLoad);
      if (observer) observer.disconnect();
    };
  }, []);

  return (
    <div
      data-testid="v8-portal-iframe-host"
      data-substitution-applied={substitutionsApplied}
      style={{ width: "100vw", height: "100vh", margin: 0, padding: 0, overflow: "hidden" }}
    >
      <iframe
        ref={iframeRef}
        data-testid="v8-prototype-iframe"
        src="/v8_prototype.html"
        title="Akki OS \u00b7 RMS AI"
        style={{ width: "100%", height: "100%", border: "none", display: "block" }}
      />
    </div>
  );
}
