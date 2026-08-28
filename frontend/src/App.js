import "@/App.css";
import { useEffect, useRef, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

/**
 * App.js — Wave G4 · V8 LITERAL adoption · owner Wave G3 REJECT corrections.
 *
 * Owner verdict verbatim (2026-08-28T~11:45Z, banked in DECISIONS.md):
 *   A. Dummy data still the same - see screen shot.
 *   B. Legacy screens should be retired as all components built should
 *      naturally fit this front end without dumping old screens that
 *      create confusion. On the topline statistics, i need practical
 *      data points that speak to everyday users using the system.
 *
 * Three corrections applied here:
 *
 *   Correction 1 — Slot #1 root-cause: the "RMS AI holds ..." sentence is
 *                  fragmented across five nested inline <span> elements
 *                  (border-bottom underlines on "86.4 TB", "12 sources",
 *                  "78% measured", "6 opportunities"). A per-text-node
 *                  regex cannot span multiple text nodes. The fix uses
 *                  ELEMENT-ANCHOR substitution: find the element whose
 *                  full textContent equals the sentence, then assign
 *                  textContent (whole-element replacement). Plus
 *                  MutationObserver re-application (idempotent) so the
 *                  substitution survives portal → Registry → back →
 *                  Registry navigation.
 *
 *   Correction 2 — EVERY topline statistic tile on the Registry surface
 *                  (10 tiles: Held in total, Sources connected, Share
 *                  measured, Data types present, Languages observed,
 *                  Share already verified, Share carrying PII, Licensed
 *                  for external use, Not yet measured, Reduced to reusable
 *                  memory) gets substituted in place. Values are practical
 *                  data points from live data or HONEST-EMPTY
 *                  ("Not yet measured"). Layout untouched.
 *
 *   Correction 3 — Legacy pod component routes retired from routing. The
 *                  V8 front end (PortalIframe) is now the ONLY user-facing
 *                  surface. Any non-root hit lands on the portal.
 *                  Component source files at pod_shell/frontend/src/
 *                  components/*.jsx are RETAINED on disk (donor material
 *                  for wiring real data into V8 surfaces in later waves),
 *                  but are no longer imported here — tree-shaking drops
 *                  them from the shipped bundle.
 *
 * Visual-proof marker: the iframe host <div> in the OUTER document
 * carries a `data-substitution-applied` attribute (monotonic counter of
 * substitutions applied across the session lifetime). This is INVISIBLE
 * bookkeeping on the outer document — not inside the prototype's DOM —
 * so it does not violate the no-engineering-vocab-on-surface rule.
 */

// ---------------------------------------------------------------------------
// Substitution engine
// ---------------------------------------------------------------------------

function _sourcesPhrase(sources) {
  if (sources == null || sources === 0) return "no sources connected yet";
  if (sources === 1) return "1 connected source";
  return `${sources} connected sources`;
}

function _tablesPhrase(tables) {
  if (tables == null || tables === 0) return "no tables read yet";
  if (tables === 1) return "with 1 table read";
  return `with ${tables.toLocaleString()} tables read`;
}

/**
 * V8_SUBSTITUTIONS — the explicit slot substitution map.
 *
 * Rule shapes:
 *   kind='element-anchor' — find the element whose textContent equals
 *                           `dummyContent`. Replace its textContent with
 *                           render(vals). Handles fragmented-span slots.
 *
 *   kind='text-node' — find the text node whose value matches the
 *                      regex `signature`. Replace its nodeValue with
 *                      render(vals). For single-node slots.
 *
 *   kind='tile-value' — find the text node whose trimmed value equals
 *                       `dummy`, verify one ancestor contains `label`
 *                       (to disambiguate value collisions), and replace
 *                       its nodeValue with render(vals). Preserves the
 *                       tile's card layout (label + note stay).
 *
 * Every rule is idempotent: if the target already carries the desired
 * text, the engine skips the mutation. This is required because
 * setting textContent/nodeValue triggers a MutationObserver event
 * which re-invokes applySubstitutions.
 */
const V8_SUBSTITUTIONS = [
  {
    kind: "styled-element-anchor",
    name: "registry-aside-hero-sentence",
    // Slot #1 · Registry header greeting sentence.
    // Wave-H · INTERRUPT 3 (2026-08-28T~13:25Z) + harness finding
    // (2026-08-28T~14:12Z, banked in DECISIONS.md next entry):
    //   dc-runtime renders the plain interpolated string from JS
    //   `estate.greeting` at data-dc-tpl="343" as a single
    //   <span class="sc-interp"> — NOT the multi-span styled variant
    //   that exists elsewhere in the prototype's static HTML. Our job
    //   is to REPLACE the plain-string render with the styled variant
    //   (3 underlined figure phrases + 1 oxblood phrase) that owner
    //   INTERRUPT 3 called out as "by design".
    //
    // dummyContent matches what dc-runtime ACTUALLY renders on the
    // Registry surface (verified via real-Chromium probe 2026-08-28).
    dummyContent:
      "86.4 TB across 12 sources \u2014 78% measured, with 6 opportunities standing ready.",
    // renderFragments returns an ordered list of {kind, value} where kind is:
    //   "text"      -> plain text node (no styling)
    //   "underline" -> span with border-bottom:1px solid rgba(27,31,39,.25)
    //   "oxblood"   -> span with color:var(--oxblood)
    // The prototype's typographic treatment is preserved byte-for-byte on
    // both live-values and honest-empty variants.
    renderFragments: (v) => {
      const hasLive = v.estateSources != null || v.estateTables != null;
      if (!hasLive) {
        // Honest-empty variant · typographic treatment consistent with
        // prototype design language (3 underlined phrases + 1 oxblood).
        return [
          { kind: "text", value: "RMS AI is reading " },
          { kind: "underline", value: "no sources yet" },
          { kind: "text", value: ", " },
          { kind: "underline", value: "no size yet" },
          { kind: "text", value: " \u2014 " },
          { kind: "underline", value: "no measurement" },
          { kind: "text", value: ", " },
          { kind: "oxblood", value: "awaiting first census" },
          { kind: "text", value: "." },
        ];
      }
      // Live-values variant · real figures in underline spans, closing
      // phrase in oxblood.
      const sourcesPhrase = _sourcesPhrase(v.estateSources);
      const tablesPhrase = _tablesPhrase(v.estateTables);
      return [
        { kind: "text", value: "RMS AI is reading " },
        { kind: "underline", value: sourcesPhrase },
        { kind: "text", value: ", holding " },
        { kind: "underline", value: tablesPhrase },
        { kind: "text", value: " \u2014 " },
        { kind: "underline", value: "size and completeness not yet measured" },
        { kind: "text", value: ", " },
        { kind: "oxblood", value: "awaiting first census" },
        { kind: "text", value: "." },
      ];
    },
  },
  {
    kind: "text-node",
    name: "registry-census-footer",
    // Slot #2 · census footer text node (single-node before trailing span).
    signature:
      /Every figure on this page traces to a census measurement\. First census May 12, 2026[^]*?J\. Mwangi \u00b7\s*$/,
    render: () =>
      "Every figure on this page traces to a census measurement. No census has been run yet \u00b7 ",
  },
  // Ten topline tiles (Wave G4 CORRECTION 2 · scope expansion).
  // Labels are literal (as they appear in dc-runtime measureCards).
  // Dummy values are the tile's rendered value string.
  {
    kind: "tile-value",
    name: "tile-held-in-total",
    label: "Held in total",
    dummy: "86.4 TB",
    render: () => "Not yet measured",
  },
  {
    kind: "tile-value",
    name: "tile-sources-connected",
    label: "Sources connected",
    dummy: "12",
    // Only tile with an honest live counterpart (data_sources.length).
    render: (v) => (v.estateSources == null ? "Not yet measured" : String(v.estateSources)),
  },
  {
    kind: "tile-value",
    name: "tile-share-measured",
    label: "Share measured",
    dummy: "78%",
    render: () => "Not yet measured",
  },
  {
    kind: "tile-value",
    name: "tile-data-types-present",
    label: "Data types present",
    dummy: "5",
    render: () => "Not yet measured",
  },
  {
    kind: "tile-value",
    name: "tile-languages-observed",
    label: "Languages observed",
    dummy: "7",
    render: () => "Not yet measured",
  },
  {
    kind: "tile-value",
    name: "tile-share-already-verified",
    label: "Share already verified",
    dummy: "34%",
    render: () => "Not yet measured",
  },
  {
    kind: "tile-value",
    name: "tile-share-carrying-pii",
    label: "Share carrying PII",
    dummy: "41%",
    render: () => "Not yet measured",
  },
  {
    kind: "tile-value",
    name: "tile-licensed-for-external-use",
    label: "Licensed for external use",
    dummy: "18%",
    render: () => "Not yet measured",
  },
  {
    kind: "tile-value",
    name: "tile-not-yet-measured",
    label: "Not yet measured",
    dummy: "22%",
    render: () => "Not yet measured",
  },
  {
    kind: "tile-value",
    name: "tile-reduced-to-reusable-memory",
    label: "Reduced to reusable memory",
    dummy: "58%",
    render: () => "Not yet measured",
  },
];

function _findAncestorContainingText(node, label, root) {
  let anc = node.parentNode;
  while (anc && anc !== root) {
    const tc = anc.textContent || "";
    if (tc.includes(label)) return anc;
    anc = anc.parentNode;
  }
  return null;
}

function applySubstitutions(doc, vals) {
  if (!doc || !doc.body) return 0;
  let count = 0;

  for (const rule of V8_SUBSTITUTIONS) {

    // Wave-H INTERRUPT 3 · styled-element-anchor · rebuild container's
    // children preserving prototype inline span structure (underline +
    // oxblood). Owner directive verbatim (DECISIONS.md 2026-08-28T~13:25Z):
    //   "reusing the prototype's own inline markup IS the literal-adoption
    //    standard ... post-substitution DOM must contain the expected
    //    styled span/link elements (assert style signature presence, not
    //    just text)."
    if (rule.kind === "styled-element-anchor") {
      const fragments = rule.renderFragments(vals);
      if (!fragments || fragments.length === 0) continue;
      const desiredFullText = fragments.map((f) => f.value).join("");
      const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_ELEMENT);
      let el;
      const dummyTrim = rule.dummyContent.trim();
      const markerAttr = "data-substituted-slot";
      const markerVal = rule.name;
      // Priority 1: element already marked → check if desired changed.
      // Priority 2: original dummy match → mark + substitute.
      const marked = doc.querySelector(`[${markerAttr}="${markerVal}"]`);
      const target =
        marked ||
        (() => {
          let candidate = null;
          while ((candidate = walker.nextNode())) {
            const tc = (candidate.textContent || "").trim();
            if (tc === dummyTrim) return candidate;
          }
          return null;
        })();
      if (!target) continue;
      // Skip if already at desired.
      if ((target.textContent || "").trim() === desiredFullText.trim()) continue;
      const newChildren = fragments.map((f) => {
        if (f.kind === "text") return doc.createTextNode(f.value);
        const span = doc.createElement("span");
        // Set style attribute verbatim to match prototype signature so a
        // downstream style-signature scan finds an exact match.
        if (f.kind === "underline") {
          span.setAttribute(
            "style",
            "border-bottom:1px solid rgba(27,31,39,.25);"
          );
        } else if (f.kind === "oxblood") {
          span.setAttribute("style", "color:var(--oxblood);");
        }
        span.textContent = f.value;
        return span;
      });
      target.replaceChildren(...newChildren);
      target.setAttribute(markerAttr, markerVal);
      count++;
      continue;
    }

    const desired = rule.render(vals);
    if (desired == null) continue;

    if (rule.kind === "element-anchor") {
      // Whole-element textContent replacement — handles fragmented spans.
      // Idempotency emerges from state: after mutation, textContent equals
      // desired ≠ dummyContent, so subsequent walks find no match.
      const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_ELEMENT);
      let el;
      const dummyTrim = rule.dummyContent.trim();
      while ((el = walker.nextNode())) {
        const tc = (el.textContent || "").trim();
        if (tc !== dummyTrim) continue;
        if (el.textContent !== desired) {
          el.textContent = desired;
          count++;
        }
        break;
      }
      continue;
    }

    if (rule.kind === "text-node") {
      // Idempotency emerges from state: after mutation, node.nodeValue no
      // longer matches rule.signature.
      const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) {
        const text = node.nodeValue;
        if (!text || text.length < 4) continue;
        if (rule.signature.test(text)) {
          if (node.nodeValue !== desired) {
            node.nodeValue = desired;
            count++;
          }
          break;
        }
      }
      continue;
    }

    if (rule.kind === "tile-value") {
      // Match ONLY on trimmed === rule.dummy (not desired). This avoids a
      // collision where an unrelated tile whose LABEL text happens to
      // equal `desired` (e.g., the "Not yet measured" tile's label
      // colliding with the HONEST-EMPTY rendering of every other tile)
      // is mistaken for the target. Idempotency emerges from state:
      // after mutation, nodeValue equals desired ≠ dummy.
      const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) {
        const trimmed = (node.nodeValue || "").trim();
        if (trimmed !== rule.dummy) continue;
        const anc = _findAncestorContainingText(node, rule.label, doc.body);
        if (!anc) continue;
        if (node.nodeValue !== desired) {
          node.nodeValue = desired;
          count++;
        }
        break;
      }
      continue;
    }
  }

  return count;
}

// ---------------------------------------------------------------------------
// PortalIframe — the single user-facing surface (Wave G4 CORRECTION 3).
// ---------------------------------------------------------------------------

function PortalIframe() {
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
    const liveValues = { estateSources: null, estateTables: null };

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
      try {
        const backend = process.env.REACT_APP_BACKEND_URL || "";
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

// ---------------------------------------------------------------------------
// App — single-surface routing (Wave G4 CORRECTION 3).
// All paths (root + wildcard) render <PortalIframe/>. The 15 legacy
// deep-link routes are retired. Component source files retained.
// ---------------------------------------------------------------------------

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<PortalIframe />} />
          <Route path="*" element={<PortalIframe />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
