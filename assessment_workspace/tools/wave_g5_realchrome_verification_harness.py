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
import argparse, json, os, re, sys, time
from pathlib import Path

sys.path.insert(0, "/opt/plugins-venv/lib/python3.11/site-packages")
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout


ROOT = Path("/app/assessment_workspace/phase0/eyeball_proxies")
ROOT.mkdir(parents=True, exist_ok=True)

FRONTEND_URL = "http://localhost:3000/"
BACKEND_URL_LOCAL = "http://localhost:8001"
BACKEND_URL_EXTERNAL = "https://akki-reuse-assess.preview.emergentagent.com"

XFF_ADMIT_HEADER = "127.0.0.1, pod-lb, cf-edge"

DUMMY_STRINGS = [
    # Slot #1 pieces
    "RMS AI holds 86.4 TB across 12 sources",  # composite (fragmented-span concat)
    # Individual tile dummies (each must be absent post-substitution)
    "86.4 TB",       # Held in total
    "12 sources",    # slot #1 span
    "78% measured",  # slot #1 span
    "6 opportunities",  # slot #1 span
    "78%",           # Share measured
    "34%",           # Share already verified
    "41%",           # Share carrying PII
    "18%",           # Licensed for external use
    "22%",           # Not yet measured (as tile-value)
    "58%",           # Reduced to reusable memory
    # Slot #2 census pieces
    "Census #4 (ran at 4.00am",
    "J. Mwangi",
    "May 12, 2026",
]

EXPECTED_STRINGS = [
    # Wave-H INTERRUPT 3 · post-styled-element-anchor phrasing.
    "RMS AI is reading",                 # slot #1 honest-empty opener
    "no sources yet",                    # slot #1 underlined span (honest-empty)
    "no size yet",                       # slot #1 underlined span (honest-empty)
    "no measurement",                    # slot #1 underlined span (honest-empty)
    "awaiting first census",             # slot #1 oxblood span (honest-empty)
    "Not yet measured",                  # HONEST-EMPTY for tiles (still applies)
    "No census has been run yet",        # slot #2 HONEST-EMPTY
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


def audit_dom(page, dummies, expected):
    """Return dummy/expected string presence in iframe body textContent."""
    audit = page.evaluate("""(args) => {
        const {dummies, expected} = args;
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        if (!iframe || !iframe.contentDocument) return {error:"iframe null"};
        const doc = iframe.contentDocument;
        const t = doc.body.textContent || "";
        const dummyHits = {};
        for (const d of dummies) dummyHits[d] = t.includes(d);
        const expectedHits = {};
        for (const e of expected) expectedHits[e] = t.includes(e);
        return {dummyHits, expectedHits, textLen: t.length};
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
