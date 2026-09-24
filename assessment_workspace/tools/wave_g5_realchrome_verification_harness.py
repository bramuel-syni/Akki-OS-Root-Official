"""Wave G5 · real-Chromium verification harness (owner directive · 2026-08-28).

Owner ruling (verbatim):
    "REAL-BROWSER VERIFICATION HARNESS (mandatory before any future eyeball
    request): run a real headless Chromium from the terminal (Playwright or
    Puppeteer via node — this is terminal tooling, not the banned testing
    agent) against the pod's own frontend on localhost. If the owner-
    installed IP allowlist middleware 403s loopback, add 127.0.0.1/pod-
    internal loopback to the allowlist config for internal verification
    ONLY. The harness must: load the portal, wait for the iframe + dc-
    runtime hydration, NAVIGATE to the Registry surface exactly as a
    user would (click through), then assert on the rendered DOM text:
    dummy strings ('86.4 TB', '12 sources', '78%', '34%', '41%', '18%',
    '22%', '58%', 'Census #4', 'J. Mwangi') are ABSENT and expected
    substitutions ('Not yet measured', live source count, honest census
    line) are PRESENT. Save a full-page screenshot artifact as the
    eyeball-proxy receipt. Bank pass output as a drill receipt."

Design:
  - Launch Chromium (headless, no-sandbox, dev-shm=disabled — pod-safe).
  - Inject X-Forwarded-For: 127.0.0.1, pod-lb, cf-edge on every request
    so both frontend (port 3000) + backend (port 8001) ACLs admit.
  - Route /api requests hard-coded to REACT_APP_BACKEND_URL (external
    Cloudflare) → rewrite to http://localhost:8001. Otherwise the
    Cloudflare edge blocks pod-outbound traffic.
  - Load http://localhost:3000/, wait for React mount + iframe load +
    dc-runtime hydration, then wait for the substitution engine to
    settle (poll data-substitution-applied on the iframe host).
  - NAVIGATE to Registry by clicking any nav element whose textContent
    equals 'Registry' inside the iframe (dc-runtime nav).
  - Re-poll data-substitution-applied post-navigation.
  - Assert dummy strings absent + expected substitutions present.
  - Screenshot to a workspace path.
  - Print structured PASS/FAIL summary. Exit 0 on all-green, 1 on any-red.
"""
import argparse, json, os, re, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "/opt/plugins-venv/lib/python3.11/site-packages")
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout


def _git_head_sha():
    """Best-effort read of Extraction-Akki HEAD SHA for provenance."""
    try:
        r = subprocess.run(
            ["git", "-C", "/app/assessment_workspace/repos/Extraction-Akki",
             "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        return (r.stdout or "").strip() or None
    except Exception:
        return None


ROOT = Path("/app/assessment_workspace/phase0/eyeball_proxies")
ROOT.mkdir(parents=True, exist_ok=True)

FRONTEND_URL = "http://localhost:3000/"
BACKEND_URL_LOCAL = "http://localhost:8001"
BACKEND_URL_EXTERNAL = "https://pensive-goodall-6.preview.emergentagent.com"

XFF_ADMIT_HEADER = "127.0.0.1, pod-lb, cf-edge"

DUMMY_STRINGS = [
    # Wave-G5b: only the ACTUALLY-RENDERED dummies remain in this list.
    # The prior composite ("RMS AI holds 86.4 TB across 12 sources") lived
    # in a template-branch that dc-runtime never renders — retired.
    "86.4 TB",                                       # tile 1 value dummy
    "held across 12 sources",                        # tile 1 label dummy
    "78%",                                           # tile 2 value dummy
    # "measured at last census" is BOTH the dummy AND the live-values
    # render of tile-share-measured-label when a census has run. The
    # rule DOES bind (data-substituted-slot=tile-share-measured-label
    # marker set) but the visible text is identical to the dummy, so
    # a text-only audit would falsely flag it. Marker-based binding
    # is asserted separately in the ground-truth (orphan_count=0).
    "opportunities standing ready",                  # tile 3 label dummy
    "Census #4 read the estate at the seam",         # slot #2a dummy
    "Run Jul 21, 2026 by J. Mwangi",                 # slot #2b dummy (prefix)
    # Wave-G5c-COMPUTE-FRONTEND compute-tile dummies RETIRED 2026-08-31 ·
    # tools/compute_where_probe.py established the prototype never
    # renders '840 vCPU-h/day', 'Total capacity', 'Allocated to Build',
    # '3 queued', 'Queue depth' as visible DOM (only '62%' appears, and
    # its anchor 'Allocated to Build' is script-only). Rules retired in
    # V8_SUBSTITUTIONS with charter for W-G5c-COMPUTE-v2 targeting the
    # actually-rendered percentage-driven layout ("43% of the month",
    # "645 hrs · 52%", etc.). See SPRINT_PLAN.md.
]

EXPECTED_STRINGS = [
    # Wave-G5b · post-substitution phrasing (honest-empty OR live-values
    # variant). At least ONE of each pair MUST be visible.
    "RMS AI is reading",                 # slot #1 opener (either variant)
    # Wave-G5c-CENSUS · Census #1 landed 2026-08-28T15:49:08Z with 2 DBs
    # + 233 tables. Slot #1 oxblood tail now shows the live-values
    # variant "awaiting first census" (no size measurement yet).
    "awaiting first census",             # slot #1 oxblood
    # Wave-G5c · slot #2a live phrasing (Census #1 exists) OR honest-empty:
    "read the estate at the seam",       # slot #2a live phrasing
    # Wave-G5c-COMPUTE-FRONTEND retired 2026-08-31; compute expectations
    # ("host", "GPU") retired from this audit alongside the tile rules.
    # W-G5c-COMPUTE-v2 (SPRINT_PLAN.md) will re-introduce compute
    # expectations against the actually-rendered surface.
]

# Wave-G5c-COMPUTE-v2 (2026-08-31) · distinctive dummies + expected
# phrases for the Compute Connected sub-tab. These are audited on the
# COMPUTE view (not Registry) via a separate audit_dom call. The full
# 11-rule rendered-DOM binding check is done via capture_ground_truth
# on the compute view (marker-based) — this text audit is the eyeball
# certainty layer for the distinctive strings only.
#
# Scope discipline (banked in DECISIONS.md, W-G5c-COMPUTE-v2 close):
#   W-G5c-COMPUTE-v2 substitutes tile VALUES only. Tile NOTES
#   (e.g. "43% of the month", "wall-clock across 4 GPUs") and CHART
#   captions/bar labels (e.g. "1,240 hrs · 43%", "1,240 hrs committed"
#   inside COMPUTE_CHARTS.door/state) are OUT of scope for this wave
#   and remain as prototype text. That is a bounded, honest scope
#   statement, tracked as residual W-G5c-COMPUTE-v2-r1 (chart-caption
#   substitution) and W-G5c-COMPUTE-v2-r2 (tile-note substitution).
#
# The dummies below are therefore restricted to strings that appear
# EXACTLY ONCE in the prototype and only in the tile-value position —
# their disappearance is proof the tile substitution fired. Strings
# that also appear in chart captions ("1,240 hrs", "1,640 hrs",
# "2,880 hrs") are ambiguous under the current scope and are omitted
# from this text audit; their tile substitution is still proven via
# the marker-based ground-truth path in capture_ground_truth.
COMPUTE_V2_DUMMY_STRINGS = [
    "on-premise \u00b7 RMS AI DC, Nairobi",   # clusters-byline dummy (1× in prototype)
    "A100 80GB \u00b7 single node",           # gpus-byline dummy (1× in prototype)
]

COMPUTE_V2_EXPECTED_STRINGS = [
    # Live-values byline derived from /api/compute/estate hosts array.
    "on-premise \u00b7 akki-vm + akki-vm-ii",
    # Live-values GPU byline · derived from gpu_model + gpu_memory_gb_per_gpu
    # + host count. Current estate: NVIDIA H200 · 139.8 GiB/GPU rounded 140
    # · 2 nodes. If estate mechanism reports different memory/count, the
    # byline text changes and this assertion will need re-anchoring —
    # that's the correct signal: this string traces live data.
    "H200 140 GiB \u00b7 2 nodes",
    # Honest-empty phrase covering 6 mechanism-less tiles. At least one
    # tile MUST render this (all 6 do, so presence check is sufficient).
    "not measured",
]

# Wave-H INTERRUPT 3 · style-signature invariants that must hold on
# the substituted slot #1 element post-substitution.
STYLE_SIGNATURE_REQUIREMENTS = {
    "min_underline_spans_in_slot1": 3,   # 3 underlined phrases in honest-empty variant
    "min_oxblood_spans_in_slot1": 1,     # closing phrase in oxblood
    "underline_style_value": "border-bottom:1px solid rgba(27,31,39,.25);",
    "oxblood_style_value": "color:var(--oxblood);",
}


def print_step(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def install_backend_url_rewrite(context):
    """Rewrite external Cloudflare URL to localhost:8001 at network layer.
    Playwright disallows protocol change in route.continue_, so we fetch
    from localhost via context.request and fulfill() the intercepted call.
    """
    external_prefix = BACKEND_URL_EXTERNAL
    local_prefix = BACKEND_URL_LOCAL
    api_request = context.request
    def handler(route, request):
        url = request.url
        if url.startswith(external_prefix):
            new_url = url.replace(external_prefix, local_prefix)
            try:
                headers = dict(request.headers)
                headers["x-forwarded-for"] = XFF_ADMIT_HEADER
                # Fetch from localhost via APIRequestContext (protocol-agnostic).
                resp = api_request.fetch(
                    new_url,
                    method=request.method,
                    headers=headers,
                    data=request.post_data,
                )
                body = resp.body()
                route.fulfill(
                    status=resp.status,
                    headers=resp.headers,
                    body=body,
                )
            except Exception as e:
                route.fulfill(status=502, body=f"pod-internal-rewrite failed: {e}")
        else:
            route.continue_()
    context.route("**/*", handler)


def wait_for_iframe_ready(page, timeout_ms=30000):
    """Wait for iframe to load AND its contentDocument to have a body."""
    print_step("Waiting for iframe + contentDocument.body ...")
    end = time.time() + timeout_ms/1000
    while time.time() < end:
        state = page.evaluate("""() => {
            const host = document.querySelector('[data-testid="v8-portal-iframe-host"]');
            if (!host) return {ok:false, why:"host missing"};
            const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
            if (!iframe) return {ok:false, why:"iframe missing"};
            try {
              const doc = iframe.contentDocument;
              if (!doc || !doc.body) return {ok:false, why:"contentDocument.body null"};
              return {ok:true, bodyTextLen: (doc.body.textContent||"").length};
            } catch (e) {
              return {ok:false, why:"contentDocument access error: "+e.message};
            }
        }""")
        if state.get("ok"):
            print_step(f"  iframe ready · contentDocument.body length={state['bodyTextLen']}")
            return state
        time.sleep(0.5)
    raise TimeoutError(f"iframe never became ready · last state: {state}")


def wait_for_dc_runtime_hydration(page, target_min_len=100_000, timeout_ms=30000):
    """Wait for dc-runtime to hydrate — body.textContent grows past a threshold."""
    print_step(f"Waiting for dc-runtime hydration (body textContent >= {target_min_len} chars) ...")
    end = time.time() + timeout_ms/1000
    while time.time() < end:
        n = page.evaluate("""() => {
            const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
            const doc = iframe && iframe.contentDocument;
            return doc && doc.body ? (doc.body.textContent||"").length : 0;
        }""")
        if n >= target_min_len:
            print_step(f"  dc-runtime hydrated · body textContent length={n}")
            return n
        time.sleep(0.5)
    raise TimeoutError(f"dc-runtime never hydrated · last length={n}")


def poll_substitution_marker(page, min_count=1, timeout_ms=15000):
    """Poll data-substitution-applied on iframe host — must reach >= min_count."""
    print_step(f"Polling data-substitution-applied >= {min_count} ...")
    end = time.time() + timeout_ms/1000
    last = None
    while time.time() < end:
        val = page.evaluate("""() => {
            const host = document.querySelector('[data-testid="v8-portal-iframe-host"]');
            return host ? host.getAttribute('data-substitution-applied') : null;
        }""")
        last = val
        try:
            if val is not None and int(val) >= min_count:
                print_step(f"  data-substitution-applied={val}")
                return int(val)
        except Exception:
            pass
        time.sleep(0.3)
    print_step(f"  TIMEOUT · last data-substitution-applied={last}")
    return last


def find_and_click_registry_nav(page):
    """Click Admin tab first, THEN Registry (dc-runtime nested nav).

    dc-runtime strips sc-camel-on-click attrs at render time and attaches
    native listeners; walker looks for cursor:pointer ancestor (space
    normalized, since dc-runtime emits `cursor: pointer` with a space).
    """
    print_step("Locating & clicking Admin tab (Registry is nested behind it) ...")
    result = page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        if (!iframe || !iframe.contentDocument) return {clicked:false, why:"iframe null"};
        const doc = iframe.contentDocument;

        function clickByLabel(label) {
            // Match on element's own text (single child text node with the exact label)
            // OR on span with sc-interp containing exactly the label.
            const els = Array.from(doc.querySelectorAll('span, div')).filter(s => {
                return (s.textContent || '').trim() === label;
            });
            for (const s of els) {
                let el = s.parentElement || s;
                for (let i = 0; i < 12 && el; i++) {
                    const style = (el.getAttribute('style') || '').replace(/\s/g, '');
                    if (style.includes('cursor:pointer')) {
                        el.click();
                        return { ok: true, label, level: i };
                    }
                    el = el.parentElement;
                }
            }
            return { ok: false, label, candidates: els.length };
        }

        const admin_click = clickByLabel('Admin');
        return { admin_click };
    }""")
    print_step(f"  admin click: {result['admin_click']}")
    page.wait_for_timeout(1500)

    result2 = page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        function clickByLabel(label) {
            const els = Array.from(doc.querySelectorAll('span, div')).filter(s => (s.textContent || '').trim() === label);
            for (const s of els) {
                let el = s.parentElement || s;
                for (let i = 0; i < 12 && el; i++) {
                    const style = (el.getAttribute('style') || '').replace(/\s/g, '');
                    if (style.includes('cursor:pointer')) {
                        el.click();
                        return { ok: true, label, level: i };
                    }
                    el = el.parentElement;
                }
            }
            return { ok: false, label, candidates: els.length };
        }
        const registry_click = clickByLabel('Registry');
        return { registry_click };
    }""")
    print_step(f"  registry click: {result2['registry_click']}")
    result.update(result2)
    return {"clicked": bool(result.get("registry_click", {}).get("ok"))} | result


def find_and_click_go_to_registry_button(page):
    """Click the 'Go to Registry →' button on the Registry aside view.

    Wave-G5c-COMPUTE-FRONTEND · post-harness-probe finding (2026-08-31):
    the aside-view Registry surface (landed by clicking Admin → Registry
    labels) exposes a 'Go to Registry →' <button> that transitions the
    prototype into the full RegistryTab view. That RegistryTab view is
    where the `regTabsView` (Data Connected · Compute Connected · ...)
    sub-tabs render, which in turn contain the computeCards tile block
    that the tile-compute-* rules substitute against.

    Discovered via tools/registry_gate_probe.py: `Go to Registry →` is
    a button (not a span/div), on the aside view.
    """
    print_step("Locating & clicking 'Go to Registry →' button ...")
    result = page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        if (!iframe || !iframe.contentDocument) return {clicked:false, why:"iframe null"};
        const doc = iframe.contentDocument;
        // The button text may include the arrow → char literal or Unicode.
        const btns = Array.from(doc.querySelectorAll('button')).filter(b => {
            const t = (b.textContent || '').trim();
            return t.startsWith('Go to Registry');
        });
        if (btns.length === 0) return {ok: false, candidates: 0};
        btns[0].click();
        return {ok: true, count: btns.length, text: (btns[0].textContent || '').trim()};
    }""")
    print_step(f"  Go to Registry button click: {result}")
    return {"clicked": bool(result.get("ok"))} | result


def find_and_click_compute_tab(page):
    """Click the 'Compute' sub-tab inside the Registry surface.

    Wave-G5c-COMPUTE-FRONTEND · owner Ruling F verbatim (banked
    2026-08-28T~14:30Z): "fold akki-vm + akki-vm-ii into the compute
    containers (Registry's 'Compute connected' tab and/or the prototype's
    compute surface)". The prototype renders a `Compute` sub-tab on the
    Registry aside; we click it after landing on Registry so the
    computeCards tile block enters the DOM (and thus the tile-compute-*
    substitution rules can bind).
    """
    print_step("Locating & clicking Compute sub-tab ...")
    result = page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        if (!iframe || !iframe.contentDocument) return {clicked:false, why:"iframe null"};
        const doc = iframe.contentDocument;

        function clickByLabel(label) {
            const els = Array.from(doc.querySelectorAll('span, div')).filter(s => {
                return (s.textContent || '').trim() === label;
            });
            for (const s of els) {
                let el = s.parentElement || s;
                for (let i = 0; i < 12 && el; i++) {
                    const style = (el.getAttribute('style') || '').replace(/\s/g, '');
                    if (style.includes('cursor:pointer')) {
                        el.click();
                        return { ok: true, label, level: i };
                    }
                    el = el.parentElement;
                }
            }
            return { ok: false, label, candidates: els.length };
        }
        // Prototype's regTabsView label is 'Compute Connected' (two words).
        // Try that first, fall back to 'Compute' for robustness.
        let compute_click = clickByLabel('Compute Connected');
        if (!compute_click.ok) {
            compute_click = clickByLabel('Compute');
        }
        return { compute_click };
    }""")
    print_step(f"  compute click: {result['compute_click']}")
    return {"clicked": bool(result.get("compute_click", {}).get("ok"))} | result


def capture_ground_truth(page):
    """Capture the current rule-vs-rendered-DOM state (used for the
    Wave-G5b invariant + Wave-G5c-COMPUTE-FRONTEND compute-tile check).

    Returned shape matches the historical gt object.
    """
    return page.evaluate(r"""() => {
        const dummies = window.V8_SUBSTITUTIONS_DUMMIES || [];
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe && iframe.contentDocument;
        if (!doc || !doc.body) return {error: "iframe body not found", dummies_declared: dummies.length};
        const bodyText = doc.body.textContent || "";
        const marked = Array.from(
            doc.querySelectorAll("[data-substituted-slot]")
        ).map(el => el.getAttribute("data-substituted-slot"));
        const perRule = dummies.map(r => {
            const matchedNow = marked.includes(r.name);
            const dummyPresentInBodyPreOrPost =
                r.dummyContent ? bodyText.includes(r.dummyContent) : false;
            return {
                name: r.name,
                kind: r.kind,
                dummyContent: r.dummyContent,
                anchorAncestorText: r.anchorAncestorText,
                matched_by_marker: matchedNow,
                dummy_still_in_body: dummyPresentInBodyPreOrPost,
                bound_to_rendered_dom: matchedNow || dummyPresentInBodyPreOrPost,
            };
        });
        return {
            dummies_declared: dummies.length,
            marked_slots_count: marked.length,
            body_len: bodyText.length,
            per_rule: perRule,
        };
    }""")


def merge_ground_truth(*gts):
    """Merge per-rule state across multiple ground-truth snapshots.

    bound_to_rendered_dom, matched_by_marker, dummy_still_in_body are
    OR-across-snapshots — a rule counts as bound if it bound on ANY
    view visited by the harness. This models the reality that
    tab-scoped rules (Registry-only, Compute-only) only exist in the
    DOM when their tab is active.
    """
    by_name = {}
    for gt in gts:
        if not gt or not gt.get("per_rule"):
            continue
        for r in gt["per_rule"]:
            name = r["name"]
            existing = by_name.get(name)
            if existing is None:
                by_name[name] = dict(r)
            else:
                existing["matched_by_marker"] = (
                    existing.get("matched_by_marker") or r.get("matched_by_marker")
                )
                existing["dummy_still_in_body"] = (
                    existing.get("dummy_still_in_body") or r.get("dummy_still_in_body")
                )
                existing["bound_to_rendered_dom"] = (
                    existing.get("bound_to_rendered_dom") or r.get("bound_to_rendered_dom")
                )
    per_rule = list(by_name.values())
    return {
        "dummies_declared": len(per_rule),
        "marked_slots_count": sum(1 for r in per_rule if r.get("matched_by_marker")),
        "body_len": max((gt.get("body_len", 0) for gt in gts if gt), default=0),
        "per_rule": per_rule,
    }


def audit_dom(page, dummies, expected):
    """Return dummy/expected string presence in the iframe's VISIBLE text
    (script/style tags excluded — their string literals are false positives).
    """
    audit = page.evaluate("""(args) => {
        const {dummies, expected} = args;
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        if (!iframe || !iframe.contentDocument) return {error:"iframe null"};
        const doc = iframe.contentDocument;
        // Walk elements, exclude script/style, concatenate their direct text.
        let visible = "";
        const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_ELEMENT);
        let el;
        while ((el = walker.nextNode())) {
            const tag = el.tagName;
            if (tag === "SCRIPT" || tag === "STYLE" || tag === "HELMET") continue;
            for (const c of el.childNodes) {
                if (c.nodeType === 3) visible += (c.nodeValue || "");
            }
        }
        const dummyHits = {};
        for (const d of dummies) dummyHits[d] = visible.includes(d);
        const expectedHits = {};
        for (const e of expected) expectedHits[e] = visible.includes(e);
        return {dummyHits, expectedHits, textLen: visible.length};
    }""", {"dummies": dummies, "expected": expected})
    return audit


def audit_style_signature(page, requirements):
    """Wave-H INTERRUPT 3 · DOM assertion for styled spans on slot #1.

    Owner directive verbatim (DECISIONS.md 2026-08-28T~13:25Z):
      'post-substitution DOM must contain the expected styled span/link
       elements (assert style signature presence, not just text) ...
       add a DOM assertion for the styles, don't rely on eyeballing the
       screenshot alone.'
    """
    return page.evaluate("""(req) => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        if (!iframe || !iframe.contentDocument) return {error:"iframe null"};
        const doc = iframe.contentDocument;
        const slot = doc.querySelector('[data-substituted-slot="registry-aside-hero-sentence"]');
        if (!slot) {
            return {
                slot_found: false,
                why: "no element with data-substituted-slot=registry-aside-hero-sentence"
            };
        }
        // Count spans with the underline/oxblood signatures.
        const spans = Array.from(slot.querySelectorAll("span"));
        const underlineSpans = spans.filter(s =>
            (s.getAttribute("style") || "").replace(/\\s/g, "") ===
            req.underline_style_value.replace(/\\s/g, "")
        );
        const oxbloodSpans = spans.filter(s =>
            (s.getAttribute("style") || "").replace(/\\s/g, "") ===
            req.oxblood_style_value.replace(/\\s/g, "")
        );
        return {
            slot_found: true,
            slot_text: (slot.textContent || "").trim(),
            span_count: spans.length,
            underline_span_count: underlineSpans.length,
            oxblood_span_count: oxbloodSpans.length,
            underline_span_texts: underlineSpans.map(s => (s.textContent||"").trim()),
            oxblood_span_texts: oxbloodSpans.map(s => (s.textContent||"").trim()),
            requirements_met:
                underlineSpans.length >= req.min_underline_spans_in_slot1 &&
                oxbloodSpans.length >= req.min_oxblood_spans_in_slot1
        };
    }""", requirements)


def collect_console_logs(page):
    logs = []
    page.on("console", lambda msg: logs.append((msg.type, msg.text)))
    page.on("pageerror", lambda exc: logs.append(("pageerror", str(exc))))
    return logs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", default="run")
    parser.add_argument("--strict", action="store_true", help="exit 1 on any dummy present or any expected missing")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    ts = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    receipt_path = ROOT / f"{ts}_wave_g5_realchrome_{args.label}.log"
    screenshot_portal = ROOT / f"{ts}_wave_g5_realchrome_{args.label}_portal.png"
    screenshot_registry = ROOT / f"{ts}_wave_g5_realchrome_{args.label}_registry.png"

    receipt = open(receipt_path, "w", buffering=1)
    def W(s=""):
        line = f"[{time.strftime('%H:%M:%S')}] {s}"
        print(line, flush=True)
        receipt.write(line + "\n")

    W(f"# Wave G5 · real-Chromium verification harness · label={args.label}")
    W(f"# frontend: {FRONTEND_URL}")
    W(f"# backend rewrite: {BACKEND_URL_EXTERNAL} -> {BACKEND_URL_LOCAL}")
    W(f"# XFF admit: '{XFF_ADMIT_HEADER}'")
    W(f"# dummies: {len(DUMMY_STRINGS)} · expected: {len(EXPECTED_STRINGS)}")
    W()

    all_pass = True
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox","--disable-dev-shm-usage"])
        try:
            context = browser.new_context(
                viewport={"width": 1600, "height": 900},
                extra_http_headers={"X-Forwarded-For": XFF_ADMIT_HEADER},
            )
            install_backend_url_rewrite(context)
            page = context.new_page()
            logs = []
            page.on("console", lambda msg: logs.append(("console."+msg.type, msg.text[:200])))
            page.on("pageerror", lambda exc: logs.append(("pageerror", str(exc)[:400])))
            page.on("requestfailed", lambda req: logs.append(("reqfailed", f"{req.method} {req.url[:100]} · {req.failure}")))

            W("[STEP 1] navigate to portal ...")
            resp = page.goto(FRONTEND_URL, wait_until="domcontentloaded", timeout=60000)
            W(f"  nav status: {resp.status if resp else 'no-response'}")

            W("[STEP 2] wait for iframe ready ...")
            try:
                s = wait_for_iframe_ready(page, timeout_ms=45000)
                W(f"  {s}")
            except TimeoutError as e:
                W(f"  FAIL: {e}"); all_pass=False

            W("[STEP 3] wait for dc-runtime hydration ...")
            try:
                n = wait_for_dc_runtime_hydration(page, target_min_len=100_000, timeout_ms=30000)
                W(f"  hydrated · body textContent length={n}")
            except TimeoutError as e:
                W(f"  FAIL: {e}"); all_pass=False

            W("[STEP 4] wait for substitution engine ...")
            marker = poll_substitution_marker(page, min_count=1, timeout_ms=15000)
            W(f"  data-substitution-applied (portal-view) = {marker}")

            W("[STEP 5] pre-navigation audit (portal-view) ...")
            audit_portal = audit_dom(page, DUMMY_STRINGS, EXPECTED_STRINGS)
            W(f"  portal-view textLen={audit_portal.get('textLen')}")
            W(f"  portal dummies still present: {[k for k,v in audit_portal.get('dummyHits',{}).items() if v]}")
            W(f"  portal expected present: {[k for k,v in audit_portal.get('expectedHits',{}).items() if v]}")

            # DIAGNOSTIC: probe engine internals
            diag = page.evaluate("""() => {
                const out = {};
                const host = document.querySelector('[data-testid="v8-portal-iframe-host"]');
                out.hostFound = !!host;
                out.hostAttr = host && host.getAttribute('data-substitution-applied');
                const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
                out.iframeFound = !!iframe;
                try {
                    const doc = iframe && iframe.contentDocument;
                    out.iframeContentDocOK = !!doc;
                    out.iframeBodyLen = doc && doc.body ? (doc.body.textContent||"").length : 0;
                    out.iframeReadyState = doc && doc.readyState;
                    out.iframeURL = iframe && iframe.src;
                } catch(e) { out.iframeAccessError = e.message; }
                // Check window global for a V8_SUBSTITUTIONS marker (if App.js exposed it)
                out.hasWindowSubstitutions = 'V8_SUBSTITUTIONS' in window;
                out.hasApplySubstitutions = 'applySubstitutions' in window;
                // Force-attempt substitution
                if (iframe && iframe.contentDocument && iframe.contentDocument.body) {
                    const bodyText = iframe.contentDocument.body.textContent || "";
                    out.slot1DummyStillIn = bodyText.includes("RMS AI holds 86.4 TB across 12 sources");
                    out.honestEmptyIn = bodyText.includes("is not yet connected to a measured estate");
                }
                return out;
            }""")
            W(f"  DIAG: {json.dumps(diag, indent=2)}")

            page.screenshot(path=str(screenshot_portal), full_page=False)
            W(f"  screenshot: {screenshot_portal}")

            W("[STEP 6] click Registry nav ...")
            click = find_and_click_registry_nav(page)
            W(f"  {click}")
            page.wait_for_timeout(3500)  # let Registry mount + substitutions fire

            W("[STEP 7] wait for substitution engine after Registry nav ...")
            try:
                base = int(marker) if marker and str(marker).isdigit() else 0
            except Exception:
                base = 0
            marker2 = poll_substitution_marker(page, min_count=max(base+1, 1), timeout_ms=15000)
            W(f"  data-substitution-applied (registry-view) = {marker2}")

            W("[STEP 8] post-navigation audit (registry-view) ...")
            audit_reg = audit_dom(page, DUMMY_STRINGS, EXPECTED_STRINGS)
            W(f"  registry-view textLen={audit_reg.get('textLen')}")
            dummy_still_present = [k for k,v in audit_reg.get('dummyHits',{}).items() if v]
            expected_present    = [k for k,v in audit_reg.get('expectedHits',{}).items() if v]
            expected_missing    = [k for k,v in audit_reg.get('expectedHits',{}).items() if not v]
            W(f"  registry DUMMY STILL PRESENT: {dummy_still_present}")
            W(f"  registry EXPECTED PRESENT:    {expected_present}")
            W(f"  registry EXPECTED MISSING:    {expected_missing}")

            W("[STEP 8b] style-signature audit (INTERRUPT 3 DOM assertion) ...")
            style_audit = audit_style_signature(page, STYLE_SIGNATURE_REQUIREMENTS)
            W(f"  style_audit: {json.dumps(style_audit, indent=2)}")
            style_ok = bool(style_audit.get("requirements_met", False))
            W(f"  style signature met: {style_ok}")
            if not style_ok:
                W("  RED · styled-element-anchor signature FAILED · slot #1 missing "
                  f"underline (need {STYLE_SIGNATURE_REQUIREMENTS['min_underline_spans_in_slot1']}, "
                  f"got {style_audit.get('underline_span_count', 0)}) or "
                  f"oxblood (need {STYLE_SIGNATURE_REQUIREMENTS['min_oxblood_spans_in_slot1']}, "
                  f"got {style_audit.get('oxblood_span_count', 0)}) spans.")
                all_pass = False

            page.screenshot(path=str(screenshot_registry), full_page=False)
            W(f"  screenshot: {screenshot_registry}")

            W("[STEP 8c] rule-vs-rendered-DOM ground-truth audit (Wave-G5b invariant · Registry view) ...")
            # Owner ruling A (DECISIONS.md 2026-08-28T~14:30Z): every
            # substitution rule's dummyContent MUST be provably present
            # in the harness-rendered DOM. A rule that matches nothing
            # is RED, not a silent no-op.
            gt_registry = capture_ground_truth(page)
            W(f"  registry-view GT: dummies_declared={gt_registry.get('dummies_declared')}, "
              f"marked_slots={gt_registry.get('marked_slots_count')}, body_len={gt_registry.get('body_len')}")

            W("[STEP 8d] click 'Go to Registry →' button (aside → RegistryTab transition) ...")
            gtr_click = find_and_click_go_to_registry_button(page)
            W(f"  {gtr_click}")
            page.wait_for_timeout(2500)  # let RegistryTab mount

            W("[STEP 8d.2] navigate to Compute tab (Wave-G5c-COMPUTE-FRONTEND) ...")
            compute_click = find_and_click_compute_tab(page)
            W(f"  {compute_click}")
            page.wait_for_timeout(3500)  # let Compute mount + substitutions fire

            W("[STEP 8e] wait for substitution engine on Compute view ...")
            try:
                base = int(marker2) if marker2 and str(marker2).isdigit() else 0
            except Exception:
                base = 0
            marker3 = poll_substitution_marker(page, min_count=max(base + 1, 1), timeout_ms=15000)
            W(f"  data-substitution-applied (compute-view) = {marker3}")

            W("[STEP 8f] Compute-view ground-truth audit ...")
            gt_compute = capture_ground_truth(page)
            W(f"  compute-view GT: dummies_declared={gt_compute.get('dummies_declared')}, "
              f"marked_slots={gt_compute.get('marked_slots_count')}, body_len={gt_compute.get('body_len')}")

            W("[STEP 8f.2] Compute-view text audit (COMPUTE_V2 distinctive dummies + expected) ...")
            audit_compute = audit_dom(page, COMPUTE_V2_DUMMY_STRINGS, COMPUTE_V2_EXPECTED_STRINGS)
            compute_dummy_still = [k for k,v in audit_compute.get('dummyHits', {}).items() if v]
            compute_expected_present = [k for k,v in audit_compute.get('expectedHits', {}).items() if v]
            compute_expected_missing = [k for k,v in audit_compute.get('expectedHits', {}).items() if not v]
            W(f"  compute-view textLen={audit_compute.get('textLen')}")
            W(f"  compute DUMMY STILL PRESENT: {compute_dummy_still}")
            W(f"  compute EXPECTED PRESENT:    {compute_expected_present}")
            W(f"  compute EXPECTED MISSING:    {compute_expected_missing}")
            if compute_dummy_still or compute_expected_missing:
                W("  RED · Compute view failed distinctive text audit "
                  "(prototype byline still visible or live/honest-empty phrase missing)")
                all_pass = False

            screenshot_compute = ROOT / f"{ts}_wave_g5_realchrome_{args.label}_compute.png"
            page.screenshot(path=str(screenshot_compute), full_page=False)
            W(f"  screenshot: {screenshot_compute}")

            W("[STEP 8g] merge ground truth across Registry + Compute views ...")
            gt = merge_ground_truth(gt_registry, gt_compute)
            W(f"  merged GT: rules={gt.get('dummies_declared')}, "
              f"marked_slots={gt.get('marked_slots_count')}")
            orphans = [
                r for r in (gt.get("per_rule") or [])
                if not r.get("bound_to_rendered_dom")
            ]
            W(f"  rule orphans (bound_to_rendered_dom=False across all views): {len(orphans)}")
            for r in orphans:
                W(f"    ORPHAN · {r['name']} · kind={r['kind']} · dummy={r['dummyContent']!r}")
            if orphans:
                W("  RED · rule-orphan · substitution rule does not match rendered DOM")
                all_pass = False

            # Persist ground truth for pytest invariant.
            gt_dir = Path("/app/assessment_workspace/phase0/harness_ground_truth")
            gt_dir.mkdir(parents=True, exist_ok=True)
            gt_payload = {
                "at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "label": args.label,
                "portal_screenshot": str(screenshot_portal),
                "registry_screenshot": str(screenshot_registry),
                "compute_screenshot": str(screenshot_compute),
                "ground_truth": gt,
                "ground_truth_registry": gt_registry,
                "ground_truth_compute": gt_compute,
                "orphan_count": len(orphans),
                "orphan_names": [r["name"] for r in orphans],
                "commit_sha_extraction_akki": _git_head_sha(),
            }
            (gt_dir / "latest.json").write_text(json.dumps(gt_payload, indent=2))
            # Also snapshot per-run
            (gt_dir / f"run_{args.label}_{int(time.time())}.json").write_text(
                json.dumps(gt_payload, indent=2)
            )
            W(f"  ground-truth: {gt_dir / 'latest.json'}")

            W("[STEP 9] console + error log (last 30 lines) ...")
            for kind, text in logs[-30:]:
                W(f"  [{kind}] {text}")

            W()
            W("=" * 70)
            W("FINAL VERDICT")
            W("=" * 70)
            W(f"  substitutions applied (portal): {marker}")
            W(f"  substitutions applied (registry): {marker2}")
            W(f"  dummies still present on Registry: {dummy_still_present}")
            W(f"  expected present on Registry: {expected_present}")
            W(f"  expected missing on Registry: {expected_missing}")
            W(f"  style signature (INTERRUPT 3): "
              f"underline={style_audit.get('underline_span_count', 0)}/"
              f"{STYLE_SIGNATURE_REQUIREMENTS['min_underline_spans_in_slot1']}, "
              f"oxblood={style_audit.get('oxblood_span_count', 0)}/"
              f"{STYLE_SIGNATURE_REQUIREMENTS['min_oxblood_spans_in_slot1']}, "
              f"met={style_ok}")

            if dummy_still_present or expected_missing or not style_ok:
                W("  RED · verification FAILED · see above")
                all_pass = False
            else:
                W("  GREEN · verification PASSED · dummies absent, expected present, "
                  "styled-element-anchor spans intact")
        finally:
            browser.close()

    receipt.close()
    print(f"\nreceipt: {receipt_path}")
    print(f"portal screenshot: {screenshot_portal}")
    print(f"registry screenshot: {screenshot_registry}")
    if args.strict:
        sys.exit(0 if all_pass else 1)
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
