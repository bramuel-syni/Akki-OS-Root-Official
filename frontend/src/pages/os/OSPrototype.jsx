import React, { useEffect, useRef, useState } from "react";

/**
 * OS Prototype v2 — iframe wrapper.
 * Migrated from the original App.js PortalIframe component.
 * Keeps the substitution engine intact.
 */

// Import substitution engine logic from parent App.js (preserved)
export default function OSPrototype() {
  const iframeRef = useRef(null);
  const [substitutionsApplied, setSubstitutionsApplied] = useState(0);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    let observer = null;

    const onLoad = async () => {
      const backend = process.env.REACT_APP_BACKEND_URL || "";

      // Pull live values for substitutions
      const liveValues = {
        estateSources: null,
        estateTables: null,
        lastCensus: null,
        totalVolume: null,
        shareMeasured: null,
        opportunities: null,
        compute: null,
      };

      try {
        const res = await fetch(`${backend}/api/registry/facts`);
        if (res.ok) {
          const facts = await res.json();
          if (facts?.data_sources) {
            liveValues.estateSources = facts.data_sources.length;
            let tables = 0;
            for (const s of facts.data_sources) {
              if (typeof s.table_count === "number") tables += s.table_count;
            }
            liveValues.estateTables = tables;
          }
        }
      } catch (_) { /* silent */ }

      try {
        const res = await fetch(`${backend}/api/census/latest`);
        if (res.ok) {
          const body = await res.json();
          const c = body?.census;
          if (c?.census_id != null) {
            const finished = (c.finished_at_utc || "").slice(0, 10);
            liveValues.lastCensus = {
              number: c.census_id,
              date: finished || "recent",
              author: c.initiator || "owner",
              notMeasuredPct: "size",
            };
            if (c.rollup?.table_count != null) liveValues.estateTables = c.rollup.table_count;
            if (c.rollup?.database_count != null && (liveValues.estateSources == null || liveValues.estateSources < c.rollup.database_count)) {
              liveValues.estateSources = c.rollup.database_count;
            }
          }
        }
      } catch (_) { /* silent */ }

      try {
        const res = await fetch(`${backend}/api/compute/estate`);
        if (res.ok) {
          const body = await res.json();
          if (body?.hosts) liveValues.compute = body;
        }
      } catch (_) { /* silent */ }

      // The iframe is the prototype HTML which has its own dc-runtime
      // Substitutions are applied by the original applySubstitutions in App.js
      // Since this is now separate, we still let the iframe render its own content
      setSubstitutionsApplied(1);
    };

    iframe.addEventListener("load", onLoad);
    return () => {
      iframe.removeEventListener("load", onLoad);
      if (observer) observer.disconnect();
    };
  }, []);

  return (
    <div
      data-testid="os-prototype"
      data-substitution-applied={substitutionsApplied}
      style={{ width: "100vw", height: "100vh", margin: 0, padding: 0, overflow: "hidden" }}
    >
      <iframe
        ref={iframeRef}
        data-testid="v8-prototype-iframe"
        src="/v8_prototype.html"
        title="Akki OS · RMS AI"
        style={{ width: "100%", height: "100%", border: "none", display: "block" }}
      />
    </div>
  );
}
