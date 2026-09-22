/**
 * ResponseRequiredBadge — additive overlay badge for the sealed
 * A'''-cont-A response-required queue.
 *
 * PHASE 3 continuation A'''-cont-B · CP-CENSUS-AUTONOMY-RESPONSE-
 * REQUIRED-BADGE-UI. Renders a compact numeric badge (pending count)
 * that opens an inline panel listing every pending item with its
 * ACTIONABLE unblock text parsed from the A''''-marker prefix
 * `[UNBLOCK action_class=<code>] <detail>` embedded inside the sealed
 * queue's reason_text field.
 *
 * Owner directive verbatim (2026-09-22T~19:40Z at A'''' opening):
 *   "the owner-answerable item text for blocked slices should carry
 *    the exact unblock action (e.g., 'grant obs:object:GetObject on
 *    na7p4* for user BramwelMwalo') so the badge in A'''-cont-B is
 *    actionable, not just informative — put that in the item payload
 *    schema now if it needs a field."
 *
 * Owner directive verbatim (2026-09-22T~21:21Z at Phase 3 closure):
 *   "Proceed: A'''-cont-B (badge + polling on real producer data)"
 *
 * Additive over sealed A'''-cont-A endpoints. Never fabricates counts;
 * displays exactly what the sealed queue returns via the sealed
 * A''''-cont-A producer-bridge path.
 *
 * Wire-up:
 *   - Reads a JWT from localStorage (`akki.jwt` · A'' precedent).
 *   - Uses useResponseRequiredList hook to poll pending items.
 *   - Click badge → toggle panel.
 *   - Resolve button → POST /resolve · triggers refetch.
 *
 * Mount: additive overlay in App.js above the sealed prototype iframe,
 * alongside CensusAutonomyDrawer (byte-identical twin across
 * pod_shell + /app/frontend).
 */
import { useEffect, useMemo, useState } from "react";
import { useResponseRequiredList } from "@/hooks/useResponseRequiredList";

const JWT_STORAGE_KEY = "akki.jwt";

// The sealed A'''' marker regex — the badge parses `reason_text` and
// renders the structured owner-answerable action. This regex mirrors
// the sealed Python `_MARKER_RE` in
// `services.census_autonomy.data_source_adapter` verbatim (JS-side
// re-implementation is unavoidable · both must match byte-for-byte).
const UNBLOCK_MARKER_RE = /^\[UNBLOCK action_class=([a-z_]+)\] (.+?)(?:$|\n)/;

function parseUnblockAction(reasonText) {
  if (!reasonText) return null;
  const m = UNBLOCK_MARKER_RE.exec(reasonText);
  if (!m) return null;
  return { actionClass: m[1], actionDetail: m[2] };
}

function useJwtFromStorage() {
  const [jwt, setJwt] = useState(() => {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem(JWT_STORAGE_KEY);
  });
  useEffect(() => {
    if (typeof window === "undefined") return;
    const onStorage = () => {
      setJwt(window.localStorage.getItem(JWT_STORAGE_KEY));
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);
  return jwt;
}

async function postResolve({ jwt, itemId, resolverId, resolutionText, resolvedState }) {
  const resp = await fetch(
    `${process.env.REACT_APP_BACKEND_URL}/api/portal/census/response-required-items/${encodeURIComponent(itemId)}/resolve`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${jwt}`,
      },
      body: JSON.stringify({
        resolver_id: resolverId,
        resolution_text: resolutionText,
        resolved_state: resolvedState,
      }),
    }
  );
  if (!resp.ok) {
    throw new Error(`resolve failed: HTTP ${resp.status}`);
  }
  return resp.json();
}

function ItemRow({ item, onResolved, jwt, disabled }) {
  const [expanded, setExpanded] = useState(false);
  const [resolutionText, setResolutionText] = useState("");
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState(null);
  const action = useMemo(() => parseUnblockAction(item.reason_text), [item.reason_text]);

  async function resolve(kind) {
    if (busy) return;
    setBusy(true);
    setErr(null);
    try {
      await postResolve({
        jwt,
        itemId: item.item_id,
        resolverId: "ui.response_required_badge",
        resolutionText: resolutionText.trim() || `resolved via A'''-cont-B badge (${kind})`,
        resolvedState: kind === "accept" ? "RESOLVED_ACCEPTED" : "RESOLVED_REJECTED",
      });
      onResolved();
    } catch (e) {
      setErr(String(e));
      setBusy(false);
    }
  }

  return (
    <div
      data-testid={`response-required-badge-item-${item.item_id}`}
      style={{
        borderTop: "1px solid rgba(255,255,255,0.08)",
        padding: "10px 12px",
        fontSize: 12,
        color: "#e5e7eb",
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontFamily: "monospace", color: "#9ca3af", fontSize: 10 }}>
            {item.refusal_code} · {item.tenant_id} · {item.census_run_id}
          </div>
          {action ? (
            <div style={{ marginTop: 4 }}>
              <span
                data-testid={`response-required-badge-item-action-class-${item.item_id}`}
                style={{
                  display: "inline-block",
                  padding: "1px 6px",
                  borderRadius: 4,
                  background: "rgba(239, 68, 68, 0.15)",
                  color: "#fca5a5",
                  fontFamily: "monospace",
                  fontSize: 10,
                  marginRight: 6,
                }}
              >
                {action.actionClass}
              </span>
              <span data-testid={`response-required-badge-item-action-detail-${item.item_id}`}>
                {action.actionDetail}
              </span>
            </div>
          ) : (
            <div style={{ marginTop: 4, color: "#9ca3af" }}>{item.reason_text}</div>
          )}
        </div>
        <button
          data-testid={`response-required-badge-item-expand-${item.item_id}`}
          onClick={() => setExpanded((e) => !e)}
          disabled={disabled}
          style={{
            border: "1px solid rgba(255,255,255,0.14)",
            background: "transparent",
            color: "#e5e7eb",
            borderRadius: 4,
            padding: "2px 8px",
            fontSize: 11,
            cursor: "pointer",
          }}
        >
          {expanded ? "collapse" : "resolve"}
        </button>
      </div>
      {expanded && (
        <div style={{ marginTop: 8 }}>
          <textarea
            data-testid={`response-required-badge-item-resolution-text-${item.item_id}`}
            value={resolutionText}
            onChange={(e) => setResolutionText(e.target.value)}
            placeholder="resolution notes · verbatim owner-answerable action taken"
            rows={2}
            style={{
              width: "100%",
              background: "rgba(0,0,0,0.4)",
              border: "1px solid rgba(255,255,255,0.14)",
              borderRadius: 4,
              padding: 6,
              color: "#e5e7eb",
              fontSize: 11,
              fontFamily: "inherit",
            }}
          />
          <div style={{ display: "flex", gap: 6, marginTop: 6 }}>
            <button
              data-testid={`response-required-badge-item-resolve-accepted-${item.item_id}`}
              onClick={() => resolve("accept")}
              disabled={busy}
              style={{
                background: "#10b981",
                color: "#000",
                border: 0,
                borderRadius: 4,
                padding: "3px 10px",
                fontSize: 11,
                cursor: busy ? "wait" : "pointer",
              }}
            >
              {busy ? "..." : "accept"}
            </button>
            <button
              data-testid={`response-required-badge-item-resolve-rejected-${item.item_id}`}
              onClick={() => resolve("reject")}
              disabled={busy}
              style={{
                background: "rgba(239, 68, 68, 0.25)",
                color: "#fca5a5",
                border: 0,
                borderRadius: 4,
                padding: "3px 10px",
                fontSize: 11,
                cursor: busy ? "wait" : "pointer",
              }}
            >
              reject
            </button>
          </div>
          {err && (
            <div
              data-testid={`response-required-badge-item-error-${item.item_id}`}
              style={{ color: "#fca5a5", marginTop: 6, fontSize: 11 }}
            >
              {err}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function ResponseRequiredBadge() {
  const jwt = useJwtFromStorage();
  const { items, count, error, triggerRefetch } = useResponseRequiredList(jwt);
  const [open, setOpen] = useState(false);

  if (!jwt) return null;

  return (
    <div
      data-testid="response-required-badge-container"
      style={{
        position: "fixed",
        top: 12,
        right: 12,
        zIndex: 9998,
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-end",
        gap: 6,
        pointerEvents: "auto",
      }}
    >
      <button
        data-testid="response-required-badge-toggle"
        onClick={() => setOpen((o) => !o)}
        style={{
          display: "flex",
          alignItems: "center",
          gap: 6,
          background: count > 0 ? "#ef4444" : "rgba(30, 30, 30, 0.85)",
          color: count > 0 ? "#000" : "#e5e7eb",
          border: "1px solid rgba(255,255,255,0.14)",
          borderRadius: 999,
          padding: "4px 10px",
          fontSize: 12,
          fontWeight: 600,
          cursor: "pointer",
          boxShadow: "0 4px 12px rgba(0,0,0,0.35)",
        }}
      >
        <span>response required</span>
        <span
          data-testid="response-required-badge-count"
          style={{
            background: count > 0 ? "#000" : "rgba(255,255,255,0.1)",
            color: count > 0 ? "#ef4444" : "#e5e7eb",
            borderRadius: 999,
            padding: "0 6px",
            fontFamily: "monospace",
          }}
        >
          {count}
        </span>
      </button>

      {open && (
        <div
          data-testid="response-required-badge-panel"
          style={{
            width: 380,
            maxHeight: 480,
            overflowY: "auto",
            background: "rgba(15, 15, 20, 0.96)",
            border: "1px solid rgba(255,255,255,0.14)",
            borderRadius: 8,
            boxShadow: "0 8px 24px rgba(0,0,0,0.5)",
            color: "#e5e7eb",
            fontSize: 12,
          }}
        >
          <div
            style={{
              padding: "10px 12px",
              borderBottom: "1px solid rgba(255,255,255,0.08)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span style={{ fontWeight: 600 }}>Response-required queue</span>
            <button
              data-testid="response-required-badge-refresh"
              onClick={triggerRefetch}
              style={{
                background: "transparent",
                border: "1px solid rgba(255,255,255,0.14)",
                color: "#e5e7eb",
                borderRadius: 4,
                padding: "2px 8px",
                fontSize: 11,
                cursor: "pointer",
              }}
            >
              refresh
            </button>
          </div>
          {error && (
            <div
              data-testid="response-required-badge-error"
              style={{ padding: "10px 12px", color: "#fca5a5" }}
            >
              {error}
            </div>
          )}
          {items.length === 0 && !error && (
            <div
              data-testid="response-required-badge-empty"
              style={{ padding: "10px 12px", color: "#9ca3af" }}
            >
              no pending items · queue is empty.
            </div>
          )}
          {items.map((item) => (
            <ItemRow
              key={item.item_id}
              item={item}
              jwt={jwt}
              onResolved={triggerRefetch}
            />
          ))}
        </div>
      )}
    </div>
  );
}
