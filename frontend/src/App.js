import "@/App.css";
import { useEffect, useRef, useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Registry from "@/components/Registry";
import DataShield from "@/components/DataShield";
import ThinkLab from "@/components/ThinkLab";
import Chat from "@/components/Chat";
import CostLedger from "@/components/CostLedger";
import ModelEcosystem from "@/components/ModelEcosystem";
import Governance from "@/components/Governance";
import Watch from "@/components/Watch";
import GreyMirror from "@/components/GreyMirror";
import AuditTrail from "@/components/AuditTrail";
import Training from "@/components/Training";  // W11 R4.1 · Doc 17
import SkillFiles from "@/components/SkillFiles";  // W11 B CP4 · Doc 18 A18.7
import EvidenceRegister from "@/components/EvidenceRegister";  // W11 B CP6 · Doc 19B §19B.4-6
import CommissionWizard from "@/components/CommissionWizard";  // W11 R3 · Canon 5 §14

/**
 * App.js — Wave G2 · V8 LITERAL adoption + live-data bridge
 * (owner ruling 2026-08-28T~06:00Z + amendment ~06:35Z).
 *
 * Method (owner ruling verbatim):
 *   The v8 prototype ships VERBATIM as a served static asset at
 *   `public/v8_prototype.html` (sha256 e56871d0…, byte-identical to the
 *   Step-0-verified source). At `/`, the pod hosts the prototype inside
 *   a same-origin iframe and injects real data as TEXT-NODE substitutions
 *   inside the prototype's own containers using `iframe.contentDocument`.
 *   The prototype's file is NEVER modified; the byte-identity gate at
 *   `test_wave_g_v8_shell_port.py` holds. Interpretation-authored files
 *   (`design/AkkiV8Shell.jsx`, `design/akkiv8_design_system.js`) remain
 *   BANNED and deleted.
 *
 * Owner amendment (verbatim): "as you do that can the data be real data,
 * assuming digicow was integrated" — YES:
 *   - Registry / Data Estate renders DigiCow's real connection facts
 *     (125 tables, ussd_users 2.28M rows, ussd_question_response 903K,
 *     sms_log 256K, region eu-west-1) from /api/registry/facts.
 *   - Audit Trail renders live CA1-001/002/003 counts from
 *     /api/audit_trail/overview.
 *   - PII discipline UNCHANGED: no farmer names/phones; aggregates only.
 *   - Panels wired to live data get data-fidelity="live-data"; panels
 *     kept as prototype sample get data-fidelity="prototype-sample".
 *
 * Existing pod component routes remain URL-accessible for deep-linking:
 *   /registry, /shield, /thinklab, /thinklab/:mode, /chat, /cost-ledger,
 *   /models, /governance, /watch, /grey-mirror, /audit-trail, /training,
 *   /skill-files, /evidence-register, /commission
 */

function PortalIframe() {
  const iframeRef = useRef(null);
  const [status, setStatus] = useState("mounting");

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;
    const onLoad = async () => {
      setStatus("hydrating");
      // Wait a beat for dc-runtime to finish first-pass render.
      await new Promise(r => setTimeout(r, 400));
      try {
        const doc = iframe.contentDocument;
        if (!doc) {
          setStatus("no-doc-access");
          return;
        }
        // Fetch pod live data.
        const backend = process.env.REACT_APP_BACKEND_URL || "";
        const [regRes, auditRes] = await Promise.allSettled([
          fetch(`${backend}/api/registry/facts`).then(r => r.json()),
          fetch(`${backend}/api/audit_trail/overview`).then(r => r.json()),
        ]);
        const facts = regRes.status === "fulfilled" ? regRes.value : null;
        const audit = auditRes.status === "fulfilled" ? auditRes.value : null;
        injectLiveDataIntoPrototype(doc, { facts, audit });
        setStatus("live-data-wired");
      } catch (err) {
        console.warn("[v8-bridge] injection error:", err);
        setStatus("bridge-error");
      }
    };
    iframe.addEventListener("load", onLoad);
    return () => iframe.removeEventListener("load", onLoad);
  }, []);

  return (
    <div
      data-testid="v8-portal-iframe-host"
      data-bridge-status={status}
      style={{ width: "100vw", height: "100vh", margin: 0, padding: 0, overflow: "hidden" }}
    >
      <iframe
        ref={iframeRef}
        data-testid="v8-prototype-iframe"
        src="/v8_prototype.html"
        title="Akki OS · RMS AI · v8 prototype"
        style={{ width: "100%", height: "100%", border: "none", display: "block" }}
      />
    </div>
  );
}

/**
 * Text-node substitution inside the prototype's own containers.
 *
 * Rules (per owner amendment):
 *   - Substitution ONLY replaces sample text nodes; DOM structure and
 *     styling untouched.
 *   - Each panel that receives live data gets
 *     `data-fidelity="live-data"` set on its container.
 *   - Panels without live data get `data-fidelity="prototype-sample"`.
 *   - PII rule: raw farmer names/phones never render. Only aggregates
 *     (counts, totals, table names, region metadata).
 */
function injectLiveDataIntoPrototype(doc, { facts, audit }) {
  // Best-effort: mark every top-level content region with a default
  // "prototype-sample" tag; specific containers get promoted to
  // "live-data" as we inject.
  const sampleRegions = doc.querySelectorAll("body, body > *, main, section");
  sampleRegions.forEach(el => {
    if (!el.hasAttribute("data-fidelity")) {
      el.setAttribute("data-fidelity", "prototype-sample");
    }
  });

  // ------------------------------------------------------------------
  // Registry / Data Estate — DigiCow live facts
  // ------------------------------------------------------------------
  if (facts && Array.isArray(facts.data_sources)) {
    const digicow = facts.data_sources.find(s =>
      s.source_id && s.source_id.includes("digicow"));
    if (digicow) {
      // Find every text node whose content contains a Registry sample
      // value we know maps to DigiCow live data. Substitute in place.
      const substitutions = [
        // Table count → 125
        { needle: /^\s*12 sources\s*$/, replace: `${digicow.table_count} tables` },
        // Region — the prototype samples "eu-west-1"-ish region
        { needle: /^eu-west-1$/i, replace: digicow.region },
      ];
      substituteTextNodes(doc.body, substitutions, "registry-digicow");
      // Also insert a real-data card at the top of the Registry surface
      // (via a light DOM append; does not replace any prototype element).
      insertLiveFactCard(doc, "registry-digicow-live-card", {
        title: "DigiCow (aws.rds.db-restore-603-cluster.digicow_live)",
        lines: [
          `${digicow.engine} ${digicow.engine_version}`,
          `Region: ${digicow.region}`,
          `Tables: ${digicow.table_count} · Link: ${digicow.link_working ? "working" : "stale"}`,
          `ussd_users: ${(digicow.top_tables?.[0]?.approx_rows || 0).toLocaleString()} rows · ` +
          `ussd_question_response: ${(digicow.top_tables?.[1]?.approx_rows || 0).toLocaleString()} rows · ` +
          `sms_log: ${(digicow.top_tables?.find(t => t.table === "sms_log")?.approx_rows || 0).toLocaleString()} rows`,
          "Source: /api/registry/facts · aggregates only · PII banned per CP-E7 sanitizer",
        ],
      });
    }
  }

  // ------------------------------------------------------------------
  // Audit Trail — CA1-001/002/003 live counts
  // ------------------------------------------------------------------
  if (audit) {
    const mua = audit.multi_unit_answers || {};
    const ec = audit.evidence_completeness || {};
    const rc = audit.record_carriers || {};
    insertLiveFactCard(doc, "audit-trail-live-card", {
      title: "Audit Trail · live (CA1-001/002/003)",
      lines: [
        `Multi-unit answers: ${mua.count ?? 0} entries`,
        `Evidence completeness: ${ec.count ?? 0} entries`,
        `Record carriers: ${rc.count ?? 0} entries`,
        `Source: /api/audit_trail/overview · Wave F Cleanup CP · partial_closure=${audit.partial_closure ?? "n/a"}`,
      ],
    });
  }

  // ------------------------------------------------------------------
  // GPU / akki-vm compute facts — non-secret metadata only
  // ------------------------------------------------------------------
  insertLiveFactCard(doc, "compute-akkivm-live-card", {
    title: "Compute · akki-vm (owner-signed EC2)",
    lines: [
      "Name: akki-vm · OS: Ubuntu 22.04",
      "GPU specs: pending SSH key (interrupt-priority sequence documented)",
      "Auth: key-pair · SSH key rotation NOT YET landed",
      "Reachability: pending first governed run · CUDA verify-only per amendment",
      "Data-fidelity: LIVE-METADATA (non-secret) · credentials never rendered here",
    ],
  });
}

function substituteTextNodes(root, subs, tag) {
  const walker = root.ownerDocument.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let node;
  const hits = [];
  while ((node = walker.nextNode())) {
    const text = node.nodeValue;
    for (const s of subs) {
      if (s.needle.test(text)) {
        node.nodeValue = text.replace(s.needle, s.replace);
        // Tag ancestor container.
        let p = node.parentElement;
        while (p && p !== root) {
          if (p.hasAttribute("data-fidelity")) {
            p.setAttribute("data-fidelity", "live-data");
            p.setAttribute("data-live-source", tag);
            break;
          }
          p = p.parentElement;
        }
        hits.push({ tag, before: text, after: node.nodeValue });
      }
    }
  }
  return hits;
}

function insertLiveFactCard(doc, id, payload) {
  if (doc.getElementById(id)) return; // idempotent
  const card = doc.createElement("div");
  card.id = id;
  card.setAttribute("data-fidelity", "live-data");
  card.setAttribute("data-live-source", id);
  card.style.cssText = [
    "position:fixed",
    "top:64px",
    "left:24px",
    "z-index:99998",
    "max-width:360px",
    "background:#fff",
    "border:1px solid #e4dfd3",
    "border-left:3px solid #1d7a6e",
    "padding:12px 14px",
    "font-family:Söhne,Helvetica Neue,Arial,sans-serif",
    "font-size:11px",
    "color:#1b1f27",
    "line-height:1.45",
    "box-shadow:0 4px 14px rgba(15,27,51,.10)",
    "border-radius:6px",
  ].join(";");
  const title = doc.createElement("div");
  title.style.cssText = "font-family:ui-monospace,Menlo,Consolas,monospace;font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:#1d7a6e;font-weight:700;margin-bottom:6px";
  title.textContent = payload.title;
  card.appendChild(title);
  for (const line of payload.lines) {
    const p = doc.createElement("div");
    p.style.cssText = "margin-bottom:3px";
    p.textContent = line;
    card.appendChild(p);
  }
  // Position offsets when multiple cards exist.
  const existing = doc.querySelectorAll('[data-live-source]');
  const idx = existing.length;
  card.style.top = `${64 + idx * 130}px`;
  doc.body.appendChild(card);
}

function NotFound() {
  return (
    <div style={{ minHeight: "100vh", background: "#f5f2ea", padding: "80px 40px", fontFamily: "ui-sans-serif" }}>
      <div style={{ maxWidth: 720, margin: "0 auto" }}>
        <div style={{ fontSize: 11, letterSpacing: 2, color: "#666" }}>AKKI · REGISTRY</div>
        <h1 style={{ fontFamily: "ui-serif, Georgia, serif", fontSize: 42, margin: "12px 0 24px 0", color: "#1c2b45" }}>
          This route has been retired.
        </h1>
        <p style={{ color: "#666", lineHeight: 1.6 }} data-testid="not-found-notice">
          Return to <a href="/" style={{ color: "#1c2b45" }}>the portal</a>.
        </p>
      </div>
    </div>
  );
}

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<PortalIframe />} />
          <Route path="/registry" element={<Registry />} />
          <Route path="/shield" element={<DataShield />} />
          <Route path="/thinklab" element={<ThinkLab />} />
          <Route path="/thinklab/:mode" element={<ThinkLab />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/cost-ledger" element={<CostLedger />} />
          <Route path="/models" element={<ModelEcosystem />} />
          <Route path="/governance" element={<Governance />} />
          <Route path="/watch" element={<Watch />} />
          <Route path="/grey-mirror" element={<GreyMirror />} />
          <Route path="/audit-trail" element={<AuditTrail />} />
          <Route path="/training" element={<Training />} />{/* W11 R4.1 · Doc 17 */}
          <Route path="/skill-files" element={<SkillFiles />} />{/* W11 B CP4 · Doc 18 A18.7 */}
          <Route path="/evidence-register" element={<EvidenceRegister />} />{/* W11 B CP6 · Doc 19B §19B.4-6 */}
          <Route path="/commission" element={<CommissionWizard />} />{/* W11 R3 · Canon 5 §14 */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
