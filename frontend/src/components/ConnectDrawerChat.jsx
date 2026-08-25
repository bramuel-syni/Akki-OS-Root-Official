import React, { useEffect, useMemo, useRef, useState } from "react";
import axios from "axios";

/**
 * ConnectDrawerChat — Right-side conversational drawer for the Connect flow.
 *
 * Owner Ruling 2026-08-19 (T12, verbatim):
 *   "paste and connect conversational wizard that assists connection,
 *    drawer chatbox right side on clicking connect."
 *
 * Behaviour
 *  - Opens as a fixed right-side drawer on top of Registry.
 *  - Opens with a single assistant turn asking what to connect (chip menu
 *    inline; free-text or paste both accepted in the same input).
 *  - PASTE runs the deterministic parser at /api/connect/parse-paste — no LLM
 *    transit for credential text (standing rule). The parser strips password
 *    + aws_secret_access_key server-side and returns *_captured signals; the
 *    browser holds the raw paste in local state only until POST — the chat
 *    log renders every credential as "•••• captured" from the parse turn
 *    forward.
 *  - Missing fields are asked as chat turns (one field per turn).
 *  - Confirmation turn ("is this the AISCA machine?" / analogous for data
 *    source / non-compute) fires the pipeline endpoint of the parsed kind:
 *      compute      -> POST /api/connect/gpu (handshake walk rendered as
 *                      three chat cards + four-questions card)
 *      data-source  -> POST /api/connect/data-source (four-questions card)
 *      llm/model    -> POST /api/connect/intent (recorded chat card)
 *  - Provisioning card (Sending it? Receiving it? aside) is a chat card
 *    triggered by the "Provisioning a new machine?" chip.
 *
 * Custody
 *  - Chat log NEVER carries a password or aws_secret_access_key value from
 *    the parse turn onward. The Registry surface never sees them.
 *  - `rawPaste` and `rawPassword` live only in local component state; on
 *    close they are cleared explicitly. No localStorage / sessionStorage.
 *
 * Visual grammar (v7 oracle exactly)
 *  - --paper #f5f2ea (drawer bg), --surface #f0ece1 (assistant turn),
 *    --surface2 #ede8da (user turn), --line #e4dfd3 (borders),
 *    --ink #1b1f27, --ink2 #3d4350, --ink3 #5b6270 (typographic ladder),
 *    --blue #16274a (primary), --sage #1d7a6e (ready/pass),
 *    --oxblood #b8395b (refuse/fail), --brass #b08d2e (aside)
 *  - --drawer-w min(460px, 94vw)
 *  - --shadow-drawer -14px 0 48px rgba(15,27,51,.18)
 *  - --head Iowan Old Style, Georgia, serif
 *  - --body Söhne, Helvetica Neue, Arial, sans-serif  (system fallback)
 */

const BACKEND = process.env.REACT_APP_BACKEND_URL;

// v7 tokens — literal so the grep-tests can verify pixel parity.
const TOK = {
  paper: "#f5f2ea",
  surface: "#f0ece1",
  surface2: "#ede8da",
  line: "#e4dfd3",
  ink: "#1b1f27",
  ink2: "#3d4350",
  ink3: "#5b6270",
  blue: "#16274a",
  blue2: "#0f1b33",
  sage: "#1d7a6e",
  oxblood: "#b8395b",
  brass: "#b08d2e",
  scrim: "rgba(15,27,51,.42)",
  shadowDrawer: "-14px 0 48px rgba(15,27,51,.18)",
  drawerW: "min(460px, 94vw)",
  head: "Iowan Old Style, Georgia, serif",
  body: "Söhne, Helvetica Neue, Arial, sans-serif",
};

const KIND_CHIPS = [
  { key: "auto", label: "Auto-detect", testid: "connect-drawer-kind-chip-auto" },
  { key: "data-source", label: "A data source", testid: "connect-drawer-kind-chip-data-source" },
  { key: "llm", label: "An LLM", testid: "connect-drawer-kind-chip-llm" },
  { key: "trained-model", label: "A trained model", testid: "connect-drawer-kind-chip-trained-model" },
  { key: "compute", label: "Compute", testid: "connect-drawer-kind-chip-compute" },
];

const COMPUTE_REQUIRED = ["host_name", "username", "public_ip"];
const COMPUTE_PW_REQUIRED = true;
const DATA_SOURCE_REQUIRED = ["region", "cluster_arn", "secret_arn"];
const DATA_SOURCE_SECRET_REQUIRED = true;

// Deterministic client-side pluck (mirrors server parser). Runs on the raw
// paste in local state; the plucked value is submitted once to the pipeline
// endpoint and never rendered into any chat turn.
function extractPasswordFromPaste(paste) {
  if (!paste) return "";
  const re = /^\s*(password|pass|pwd)\s*[:=]\s*(.+?)\s*$/im;
  const m = paste.match(re);
  return m ? m[2] : "";
}
function extractAwsSecretFromPaste(paste) {
  if (!paste) return "";
  const re = /^\s*(aws[_ ]?secret[_ ]?access[_ ]?key|secret[_ ]access[_ ]key|secret[_ ]key)\s*[:=]\s*(.+?)\s*$/im;
  const m = paste.match(re);
  return m ? m[2] : "";
}

function fieldReadout(fields, password_captured, aws_secret_captured) {
  // Plain-English "I read a host, a username, a masked password and two IPs" style.
  const bits = [];
  if (fields.host_name) bits.push("a host");
  if (fields.username) bits.push("a username");
  if (password_captured) bits.push("a masked password");
  if (aws_secret_captured) bits.push("a masked AWS secret access key");
  if (fields.aws_access_key_id) bits.push("an AWS access key ID");
  if (fields.region) bits.push("a region");
  if (fields.cluster_arn) bits.push("a cluster ARN");
  if (fields.secret_arn) bits.push("a Secrets Manager ARN");
  if (fields.database) bits.push("a database name");
  const ips = [];
  if (fields.public_ip) ips.push("public");
  if (fields.private_ip) ips.push("private");
  if (ips.length) bits.push(ips.length === 2 ? "two IPs (public and private)" : `a ${ips[0]} IP`);
  if (fields.os) bits.push("an OS");
  if (fields.deploy_date) bits.push("a deploy date");
  if (!bits.length) return "I couldn't pick anything out of that paste.";
  const list = bits.length === 1 ? bits[0]
    : bits.slice(0, -1).join(", ") + " and " + bits[bits.length - 1];
  return `I read ${list}.`;
}

function guessConfirmSentence(kind, fields) {
  if (kind === "compute") {
    const host = fields.host_name || "this machine";
    return `Is this the ${host} machine you want to admit into the estate?`;
  }
  if (kind === "data-source") {
    const db = fields.database || "database";
    const region = fields.region || "region";
    return `Is this the ${db} source in ${region} you want to connect over the RDS Data API?`;
  }
  if (kind === "llm") return "Is this the LLM you want to record intent for (goes live with its wave)?";
  if (kind === "trained-model") return "Is this the trained model you want to record intent for (goes live with its wave)?";
  return "Is this what you want to record?";
}

const KIND_LABEL = {
  compute: "compute",
  "data-source": "a data source",
  llm: "an LLM",
  "trained-model": "a trained model",
};

// ---------------------------------------------------------------------------
// Chat turn primitives
// ---------------------------------------------------------------------------

function AssistantTurn({ children, testid }) {
  return (
    <div data-testid={testid || "connect-drawer-chat-turn-assistant"}
         style={{ background: TOK.surface, border: `1px solid ${TOK.line}`,
                  borderRadius: 12, padding: "12px 14px", margin: "10px 0",
                  fontFamily: TOK.body, color: TOK.ink, fontSize: 14,
                  lineHeight: 1.5, maxWidth: "94%" }}>
      {children}
    </div>
  );
}

function UserTurn({ children, testid }) {
  return (
    <div data-testid={testid || "connect-drawer-chat-turn-user"}
         style={{ background: TOK.surface2, border: `1px solid ${TOK.line}`,
                  borderRadius: 12, padding: "10px 14px", margin: "10px 0 10px auto",
                  fontFamily: TOK.body, color: TOK.ink2, fontSize: 13,
                  lineHeight: 1.5, maxWidth: "82%", whiteSpace: "pre-wrap" }}>
      {children}
    </div>
  );
}

function Chip({ label, active, onClick, testid }) {
  return (
    <button type="button" data-testid={testid} onClick={onClick}
      style={{ padding: "6px 12px", borderRadius: 999,
               border: `1px solid ${active ? TOK.blue : TOK.line}`,
               background: active ? TOK.blue : "#fff",
               color: active ? "#fff" : TOK.ink2,
               cursor: "pointer", fontSize: 12, fontFamily: TOK.body,
               letterSpacing: 0.2, marginRight: 6, marginTop: 6 }}>
      {label}
    </button>
  );
}

function StatusPill({ status }) {
  const bg = status === "pass" ? TOK.sage :
             status === "fail" ? TOK.oxblood :
             status === "yes"  ? TOK.sage :
             status === "no"   ? TOK.oxblood : TOK.ink3;
  return (
    <span style={{ display: "inline-block", padding: "2px 8px", borderRadius: 999,
                   background: bg, color: "#fff", fontSize: 10, letterSpacing: 0.6,
                   textTransform: "uppercase" }}>{status || "—"}</span>
  );
}

// ---------------------------------------------------------------------------
// Chat cards (post-submit renderings)
// ---------------------------------------------------------------------------

function HandshakeStageCard({ testid, label, stage }) {
  const status = (stage && stage.status) || "untried";
  const border = status === "pass" ? TOK.sage : status === "fail" ? TOK.oxblood : TOK.line;
  return (
    <div data-testid={testid}
         style={{ background: "#fff", border: `1px solid ${TOK.line}`,
                  borderLeft: `4px solid ${border}`, borderRadius: 10,
                  padding: "10px 12px", margin: "8px 0" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ fontFamily: TOK.head, fontSize: 14, color: TOK.ink }}>{label}</div>
        <StatusPill status={status} />
      </div>
      {stage && stage.detail && (
        <div style={{ marginTop: 4, fontSize: 12, color: TOK.ink3, fontFamily: TOK.body }}>
          {stage.detail}
        </div>
      )}
    </div>
  );
}

function FourQuestionsCard({ result }) {
  // Four questions from the compute or data-source result.
  const q = result.four_questions || {
    link_working: result.link_working,
    found: !!(result.found && Object.keys(result.found).length),
    ready: result.ready,
    failure: result.failure || null,
  };
  const yes = (v) => v === true || v === "yes" ? "yes" : "no";
  return (
    <div data-testid="chat-card-four-questions"
         style={{ background: "#fff", border: `1px solid ${TOK.line}`,
                  borderRadius: 10, padding: "12px 14px", margin: "8px 0" }}>
      <div style={{ fontFamily: TOK.head, fontSize: 14, color: TOK.ink, marginBottom: 8 }}>
        The four questions
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
        <FQItem label="LINK WORKING" value={yes(q.link_working)} />
        <FQItem label="FOUND" value={q.found ? "yes" : "no"} />
        <FQItem label="READY" value={yes(q.ready)} />
        <FQItem label="FAILURE" value={q.failure || "none"} kind="text" />
      </div>
      {result.failure_sentence && (
        <div style={{ marginTop: 10, padding: 8, background: "#fdf2f5",
                      color: TOK.oxblood, borderRadius: 6, fontSize: 12,
                      fontFamily: TOK.body }}>
          {result.failure_sentence}
        </div>
      )}
    </div>
  );
}

function FQItem({ label, value, kind }) {
  const color = value === "yes" ? TOK.sage : value === "no" ? TOK.oxblood :
                value === "none" ? TOK.ink3 : TOK.oxblood;
  return (
    <div style={{ border: `1px solid ${TOK.line}`, borderRadius: 8, padding: "6px 10px" }}>
      <div style={{ fontSize: 10, letterSpacing: 1.2, color: TOK.ink3,
                    textTransform: "uppercase", fontFamily: TOK.body }}>{label}</div>
      <div style={{ fontFamily: TOK.head, fontSize: kind === "text" ? 14 : 18,
                    color, marginTop: 2 }}>{value}</div>
    </div>
  );
}

function ProvisioningCard({ facts }) {
  if (!facts) {
    return (
      <div data-testid="chat-card-provisioning"
           style={{ background: "#fff", border: `1px solid ${TOK.line}`,
                    borderRadius: 10, padding: 12, margin: "8px 0",
                    color: TOK.ink3, fontSize: 12, fontFamily: TOK.body }}>
        Reading provisioning facts from /api/connect/estate-facts…
      </div>
    );
  }
  return (
    <div data-testid="chat-card-provisioning"
         style={{ background: "#fff", border: `1px solid ${TOK.line}`,
                  borderLeft: `4px solid ${TOK.brass}`, borderRadius: 10,
                  padding: "12px 14px", margin: "8px 0", fontFamily: TOK.body }}>
      <div style={{ fontFamily: TOK.head, fontSize: 14, color: TOK.ink,
                    marginBottom: 8 }}>
        Provisioning aside · what to paste on the AISCA side
      </div>
      <KV label="PUBLIC KEY">
        <code data-testid="provisioning-card-public-key"
              style={{ fontSize: 11, wordBreak: "break-all", color: TOK.ink2 }}>
          {facts.estate_public_key}
        </code>
      </KV>
      <KV label="POD EGRESS IP">
        <code data-testid="provisioning-card-egress-ip"
              style={{ fontSize: 12, color: TOK.ink2 }}>{facts.pod_egress_ip}</code>
      </KV>
      <KV label="FINGERPRINT">
        <code data-testid="provisioning-card-fingerprint"
              style={{ fontSize: 11, color: TOK.ink2 }}>{facts.estate_public_key_fingerprint}</code>
      </KV>
    </div>
  );
}

function KV({ label, children }) {
  return (
    <div style={{ marginBottom: 6 }}>
      <div style={{ fontSize: 10, letterSpacing: 1.2, color: TOK.ink3,
                    textTransform: "uppercase" }}>{label}</div>
      <div style={{ fontSize: 13, color: TOK.ink }}>{children}</div>
    </div>
  );
}

function IntentRecordedCard({ record }) {
  return (
    <div data-testid="chat-card-intent-recorded"
         style={{ background: "#fff", border: `1px solid ${TOK.line}`,
                  borderLeft: `4px solid ${TOK.sage}`, borderRadius: 10,
                  padding: "12px 14px", margin: "8px 0",
                  fontFamily: TOK.body }}>
      <div style={{ fontFamily: TOK.head, fontSize: 14, color: TOK.ink }}>
        Intent recorded
      </div>
      <div style={{ marginTop: 6, fontSize: 13, color: TOK.ink2 }}>
        Recorded — this connection type goes live with its wave.
      </div>
      <div style={{ marginTop: 6, fontSize: 12, color: TOK.ink3 }}>
        Name: {record?.name || "—"}
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main drawer component
// ---------------------------------------------------------------------------

export default function ConnectDrawerChat({ onClose }) {
  // Session-only state. Never persisted. Cleared on unmount.
  const [turns, setTurns] = useState([]);
  const [kind, setKind] = useState("auto");
  const [input, setInput] = useState("");
  // rawPaste + rawPassword + rawAwsSecret held in refs so they are NEVER
  // visible in the chat state's dependency graph or a React devtool trace.
  const pasteCacheRef = useRef("");
  const pwCacheRef = useRef("");
  const awsCacheRef = useRef("");
  const [parsed, setParsed] = useState(null);      // fields + *_captured signals only
  const [awaitingConfirm, setAwaitingConfirm] = useState(false);
  const [askingField, setAskingField] = useState(null); // null | "field_name"
  const [manualPatch, setManualPatch] = useState({});   // non-secret overrides
  const [submitting, setSubmitting] = useState(false);
  const [provFacts, setProvFacts] = useState(null);
  const chatLogRef = useRef(null);

  // Opening turn
  useEffect(() => {
    setTurns([
      {
        role: "assistant",
        node: (
          <>
            <div style={{ fontFamily: TOK.head, fontSize: 16, color: TOK.ink,
                          marginBottom: 6 }}>
              What would you like to connect?
            </div>
            <div style={{ fontSize: 13, color: TOK.ink2, marginBottom: 8 }}>
              Pick a kind (or leave it on auto-detect) and paste the connection
              details in the chat. I read them deterministically — nothing here
              is sent to a model.
            </div>
            <div style={{ display: "flex", flexWrap: "wrap" }}>
              {KIND_CHIPS.map((c) => (
                <Chip key={c.key} label={c.label} testid={c.testid}
                      active={kind === c.key}
                      onClick={() => setKind(c.key)} />
              ))}
            </div>
            <div style={{ marginTop: 12, fontSize: 12, color: TOK.ink3 }}>
              Provisioning a new machine?{" "}
              <button type="button" data-testid="chip-show-provisioning-aside"
                      onClick={openProvisioning}
                      style={{ background: "transparent", border: "none",
                               color: TOK.brass, cursor: "pointer",
                               textDecoration: "underline", padding: 0,
                               fontSize: 12 }}>
                Show me what to paste on the AISCA side →
              </button>
            </div>
          </>
        ),
      },
    ]);
    // Preload provisioning facts (used only if the aside chip is clicked)
    axios.get(`${BACKEND}/api/connect/estate-facts`).then(
      (r) => setProvFacts(r.data),
      () => setProvFacts(null),
    );
    return () => {
      // Explicitly clear on unmount so credentials cannot survive close.
      pasteCacheRef.current = "";
      pwCacheRef.current = "";
      awsCacheRef.current = "";
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Auto-scroll chat log
  useEffect(() => {
    if (chatLogRef.current) chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
  }, [turns]);

  function push(role, node) {
    setTurns((prev) => [...prev, { role, node }]);
  }

  function openProvisioning() {
    push("assistant", (
      <>
        <div style={{ fontSize: 13, color: TOK.ink2, marginBottom: 6 }}>
          Sending it or receiving it — here is the estate&apos;s side, ready to paste.
        </div>
        <ProvisioningCard facts={provFacts} />
      </>
    ));
  }

  async function handleSend(text) {
    if (!text.trim()) return;
    // Detect paste (multi-line, or contains a `key: value` line)
    const isPaste = text.includes("\n") || /^\s*(host\s*name|username|pass(word)?|public\s*ip|private\s*ip|region|cluster_?arn|secret_?arn|aws)\b/im.test(text);
    // Log the USER turn — mask any credential-shaped lines before rendering.
    const maskedForLog = redactCredsForLog(text);
    push("user", maskedForLog);
    setInput("");
    if (isPaste) {
      // Cache raw paste (in ref, never in React state that renders)
      pasteCacheRef.current = text;
      pwCacheRef.current = extractPasswordFromPaste(text);
      awsCacheRef.current = extractAwsSecretFromPaste(text);
      await runParse(text);
    } else if (askingField) {
      // A missing-field answer
      setManualPatch((m) => ({ ...m, [askingField]: text.trim() }));
      const nextAsk = nextMissingField({
        ...parsed?.fields, ...manualPatch, [askingField]: text.trim(),
      }, effectiveKind(parsed?.kind, kind));
      setAskingField(nextAsk);
      if (nextAsk) {
        push("assistant", `Thanks. And ${humanField(nextAsk)}?`);
      } else {
        // All filled — go to confirmation
        setAwaitingConfirm(true);
        const eKind = effectiveKind(parsed?.kind, kind);
        push("assistant", (
          <>
            <div>{guessConfirmSentence(eKind, { ...parsed?.fields, ...manualPatch, [askingField]: text.trim() })}</div>
            <ConfirmButtons onConfirm={runSubmit} onCancel={() => {
              setAwaitingConfirm(false);
              push("assistant", "OK, no submit. Paste again or edit the fields to keep going.");
            }} />
          </>
        ));
      }
    } else {
      // Free text response before a paste — nudge them to paste
      push("assistant", "Paste the details in the chat when you have them — I read them deterministically. If you want me to guide you, tell me what kind of thing this is (data source, LLM, compute, trained model).");
    }
  }

  async function runParse(paste) {
    setSubmitting(true);
    try {
      const body = { paste, hint_kind: kind === "auto" ? null : kind };
      const r = await axios.post(`${BACKEND}/api/connect/parse-paste`, body);
      const data = r.data;
      setParsed(data);
      // Render the assistant's plain-English readout — with credentials
      // shown as "•••• captured" only, never plaintext.
      const readout = fieldReadout(data.fields || {}, data.password_captured, data.aws_secret_captured);
      const eKind = effectiveKind(data.kind, kind);
      const confirmSentence = guessConfirmSentence(eKind, data.fields || {});
      const nextAsk = nextMissingField({ ...data.fields }, eKind);
      push("assistant", (
        <>
          <div style={{ marginBottom: 6 }}>
            <strong>{readout}</strong>{" "}
            <span style={{ color: TOK.ink3 }}>(kind: {KIND_LABEL[eKind] || eKind})</span>
          </div>
          <ParseReadoutTable fields={data.fields || {}}
                             password_captured={data.password_captured}
                             aws_secret_captured={data.aws_secret_captured} />
          {nextAsk ? (
            <div style={{ marginTop: 8, color: TOK.ink2 }}>
              I still need {humanField(nextAsk)}. What is it?
            </div>
          ) : (
            <div style={{ marginTop: 8, color: TOK.ink2 }}>
              {confirmSentence}
              <ConfirmButtons onConfirm={runSubmit} onCancel={() => {
                push("assistant", "OK, no submit. Paste again or edit the fields to keep going.");
              }} />
            </div>
          )}
        </>
      ));
      setAskingField(nextAsk);
      setAwaitingConfirm(!nextAsk);
    } catch (e) {
      const detail = errDetailToString(e);
      push("assistant", (
        <div style={{ color: TOK.oxblood }}>
          I couldn&apos;t read that paste — {detail}. Ask again is the estate&apos;s
          default when it can&apos;t read. Try re-pasting with clear labels
          (Host Name / Username / Password / Public IP for compute; Region /
          Cluster ARN / Secret ARN for a data source).
        </div>
      ));
    } finally {
      setSubmitting(false);
    }
  }

  async function runSubmit() {
    setAwaitingConfirm(false);
    setSubmitting(true);
    push("user", "yes, connect it");
    const eKind = effectiveKind(parsed?.kind, kind);
    try {
      if (eKind === "compute") {
        const payload = {
          host_name: manualPatch.host_name || parsed?.fields?.host_name || "",
          username: manualPatch.username || parsed?.fields?.username || "",
          password: manualPatch.password || pwCacheRef.current,
          public_ip: manualPatch.public_ip || parsed?.fields?.public_ip || "",
          private_ip: manualPatch.private_ip || parsed?.fields?.private_ip || "",
          os: manualPatch.os || parsed?.fields?.os || "",
          deploy_date: manualPatch.deploy_date || parsed?.fields?.deploy_date || "",
        };
        const r = await axios.post(`${BACKEND}/api/connect/gpu`, payload);
        const data = r.data;
        const stages = data.stages || {};
        push("assistant", (
          <>
            <div style={{ marginBottom: 4 }}>
              Handshake walk — declaration then hardening then acceptance.
            </div>
            <HandshakeStageCard testid="chat-card-handshake-declaration" label="Declaration"
                                stage={stages.declaration} />
            <HandshakeStageCard testid="chat-card-handshake-hardening" label="Hardening"
                                stage={stages.hardening} />
            <HandshakeStageCard testid="chat-card-handshake-acceptance" label="Acceptance"
                                stage={stages.acceptance} />
            <FourQuestionsCard result={data} />
          </>
        ));
      } else if (eKind === "data-source") {
        const payload = {
          aws_access_key_id: manualPatch.aws_access_key_id || parsed?.fields?.aws_access_key_id || undefined,
          aws_secret_access_key: manualPatch.aws_secret_access_key || awsCacheRef.current || undefined,
          region: manualPatch.region || parsed?.fields?.region || "",
          cluster_arn: manualPatch.cluster_arn || parsed?.fields?.cluster_arn || "",
          secret_arn: manualPatch.secret_arn || parsed?.fields?.secret_arn || "",
          database: manualPatch.database || parsed?.fields?.database || undefined,
        };
        const r = await axios.post(`${BACKEND}/api/connect/data-source`, payload);
        push("assistant", (
          <>
            <div style={{ marginBottom: 4 }}>
              Connected to the data source — the four questions:
            </div>
            <FourQuestionsCard result={r.data} />
          </>
        ));
      } else {
        // LLM / trained-model → honest intent
        const payload = {
          kind: eKind,
          name: manualPatch.name || parsed?.fields?.name || `unnamed-${eKind}`,
          description: (pasteCacheRef.current || "").slice(0, 200),
        };
        const r = await axios.post(`${BACKEND}/api/connect/intent`, payload);
        push("assistant", <IntentRecordedCard record={r.data} />);
      }
    } catch (e) {
      const detail = errDetailToString(e);
      push("assistant", (
        <div style={{ color: TOK.oxblood }}>
          The estate couldn&apos;t accept that: {detail}. This is work done,
          not work lost — try again, or edit the fields and resend.
        </div>
      ));
    } finally {
      setSubmitting(false);
      // Zero out the raw creds — they've been submitted.
      pasteCacheRef.current = "";
      pwCacheRef.current = "";
      awsCacheRef.current = "";
    }
  }

  return (
    <>
      {/* Scrim */}
      <div onClick={onClose}
           style={{ position: "fixed", top: 0, right: 0, bottom: 0, left: 0,
                    background: TOK.scrim, zIndex: 240 }} />
      {/* Right-side drawer */}
      <aside data-testid="connect-drawer-chat"
             style={{ position: "fixed", top: 0, right: 0, bottom: 0,
                      width: TOK.drawerW, background: TOK.paper,
                      borderLeft: `1px solid ${TOK.line}`,
                      boxShadow: TOK.shadowDrawer, zIndex: 250,
                      display: "flex", flexDirection: "column",
                      fontFamily: TOK.body }}>
        {/* Header */}
        <header style={{ padding: "16px 20px", borderBottom: `1px solid ${TOK.line}`,
                         display: "flex", alignItems: "center",
                         background: TOK.paper }}>
          <div>
            <div style={{ fontFamily: TOK.head, fontSize: 18, color: TOK.ink }}>
              Connect
            </div>
            <div style={{ fontSize: 11, color: TOK.ink3, marginTop: 2,
                          letterSpacing: 0.3 }}>
              conversational · paste-assisted · nothing here reaches a model
            </div>
          </div>
          <div style={{ flex: 1 }} />
          <button type="button" data-testid="connect-drawer-close" onClick={onClose}
                  style={{ background: "transparent", border: "none",
                           fontSize: 22, cursor: "pointer", color: TOK.ink3,
                           padding: "4px 8px" }}>×</button>
        </header>

        {/* Chat log */}
        <div ref={chatLogRef} data-testid="connect-drawer-chat-log"
             style={{ flex: 1, padding: "8px 18px 12px", overflowY: "auto" }}>
          {turns.map((t, i) => (
            t.role === "assistant"
              ? <AssistantTurn key={i}>{t.node}</AssistantTurn>
              : <UserTurn key={i}>{t.node}</UserTurn>
          ))}
          {submitting && (
            <AssistantTurn testid="connect-drawer-chat-thinking">
              <span style={{ color: TOK.ink3, fontStyle: "italic" }}>
                Reading…
              </span>
            </AssistantTurn>
          )}
        </div>

        {/* Input */}
        <div style={{ padding: "12px 18px 18px", borderTop: `1px solid ${TOK.line}`,
                      background: TOK.paper }}>
          <div style={{ display: "flex", alignItems: "flex-end", gap: 8 }}>
            <textarea data-testid="connect-drawer-chat-input"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                          e.preventDefault();
                          handleSend(input);
                        }
                      }}
                      placeholder="Type your answer, or paste the connection details… Enter to send."
                      rows={2}
                      style={{ flex: 1, padding: "10px 12px",
                               border: `1px solid ${TOK.line}`, borderRadius: 8,
                               fontSize: 13, color: TOK.ink, background: "#fff",
                               fontFamily: TOK.body, resize: "vertical" }} />
            <button type="button" data-testid="connect-drawer-chat-send"
                    onClick={() => handleSend(input)}
                    disabled={submitting}
                    style={{ background: TOK.blue, color: "#fff",
                             padding: "10px 16px", border: "none",
                             borderRadius: 8, cursor: "pointer", fontSize: 13,
                             fontFamily: TOK.body }}>
              Send
            </button>
          </div>
          <div style={{ marginTop: 6, fontSize: 11, color: TOK.ink3 }}>
            The parse runs locally on the server — passwords and secret keys
            are stripped before any log line is written. Chat log stays
            session-only.
          </div>
        </div>
      </aside>
    </>
  );
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function ConfirmButtons({ onConfirm, onCancel }) {
  return (
    <div style={{ marginTop: 8, display: "flex", gap: 8 }}>
      <button type="button" data-testid="connect-drawer-confirm-yes"
              onClick={onConfirm}
              style={{ background: TOK.blue, color: "#fff", padding: "6px 14px",
                       border: "none", borderRadius: 999, cursor: "pointer",
                       fontSize: 12 }}>Yes, connect it</button>
      <button type="button" data-testid="connect-drawer-confirm-no"
              onClick={onCancel}
              style={{ background: "transparent", color: TOK.ink3,
                       padding: "6px 14px", border: `1px solid ${TOK.line}`,
                       borderRadius: 999, cursor: "pointer", fontSize: 12 }}>
        No, wait
      </button>
    </div>
  );
}

function ParseReadoutTable({ fields, password_captured, aws_secret_captured }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 12,
                    fontFamily: TOK.body, marginTop: 6 }}>
      <tbody>
        {Object.entries(fields || {}).map(([k, v]) => (
          <tr key={k}>
            <td style={{ color: TOK.ink3, paddingRight: 10, verticalAlign: "top",
                          fontSize: 11, letterSpacing: 0.2, textTransform: "uppercase" }}>
              {humanField(k)}
            </td>
            <td style={{ fontFamily: "ui-monospace, SFMono-Regular, monospace",
                          color: TOK.ink }}>
              {String(v)}
            </td>
          </tr>
        ))}
        {password_captured && (
          <tr>
            <td style={{ color: TOK.ink3, paddingRight: 10, fontSize: 11,
                          letterSpacing: 0.2, textTransform: "uppercase" }}>
              Password
            </td>
            <td data-testid="chat-parsed-password-captured"
                style={{ color: TOK.ink, fontFamily: "ui-monospace" }}>
              •••• captured (server-stripped; the chat log never carries it)
            </td>
          </tr>
        )}
        {aws_secret_captured && (
          <tr>
            <td style={{ color: TOK.ink3, paddingRight: 10, fontSize: 11,
                          letterSpacing: 0.2, textTransform: "uppercase" }}>
              AWS Secret Access Key
            </td>
            <td data-testid="chat-parsed-aws-secret-captured"
                style={{ color: TOK.ink, fontFamily: "ui-monospace" }}>
              •••• captured (server-stripped; the chat log never carries it)
            </td>
          </tr>
        )}
      </tbody>
    </table>
  );
}

function redactCredsForLog(paste) {
  // Redact `password:`, `pwd:`, and AWS secret lines before they land in the
  // chat log. Only the labelled value is masked; the rest of the paste is
  // preserved so the user can see what they sent.
  return String(paste || "").split("\n").map((line) => {
    if (/^\s*(password|pass|pwd)\s*[:=]/i.test(line)) {
      return line.replace(/([:=]\s*).*$/, "$1•••• captured");
    }
    if (/^\s*(aws[_ ]?secret[_ ]?access[_ ]?key|secret[_ ]access[_ ]key|secret[_ ]key)\s*[:=]/i.test(line)) {
      return line.replace(/([:=]\s*).*$/, "$1•••• captured");
    }
    return line;
  }).join("\n");
}

function humanField(k) {
  if (!k) return "";
  return k.replace(/_/g, " ")
    .replace(/\baws\b/i, "AWS")
    .replace(/\barn\b/i, "ARN")
    .replace(/\bid\b/i, "ID")
    .replace(/\bip\b/i, "IP")
    .replace(/\bos\b/i, "OS")
    .replace(/^./, (c) => c.toUpperCase());
}

function errDetailToString(e) {
  const d = e?.response?.data?.detail;
  if (typeof d === "string") return d;
  if (Array.isArray(d)) {
    // FastAPI 422 shape: [{loc: [...], msg: "...", type: "..."}, ...]
    return d.map((x) => x?.msg || JSON.stringify(x)).join("; ");
  }
  if (d && typeof d === "object") return JSON.stringify(d);
  return e?.message || "unknown error";
}

function nextMissingField(fields, eKind) {
  if (eKind === "compute") {
    for (const f of COMPUTE_REQUIRED) if (!fields[f]) return f;
    if (COMPUTE_PW_REQUIRED && !fields.__password_captured_hint) {
      // password requirement is signalled via parsed.password_captured; we
      // don't ask for it in-chat (it should have been in the paste).
    }
    return null;
  }
  if (eKind === "data-source") {
    for (const f of DATA_SOURCE_REQUIRED) if (!fields[f]) return f;
    return null;
  }
  // llm / trained-model — only name is required for the intent record
  if (!fields.name) return "name";
  return null;
}

function effectiveKind(parsedKind, chosenKind) {
  if (parsedKind) return parsedKind;
  return chosenKind === "auto" ? "compute" : chosenKind;
}
