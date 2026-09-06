"""W-G5c-COMPUTE-RESIDUALS · extended DOM enumeration for chart-state click-through.

Extends `tools/compute_v2_dom_enum.py` (which captured only the default
`s.computeChart='door'` state) by switching the `<sc-raw-select
value="{{ computeChart }}">` through all three states (`door`/`week`/`state`)
and capturing rendered visible text at each state. This is prep for the
`W-G5c-COMPUTE-RESIDUALS-r1` chart-caption + per-bar rules, whose 8 target
strings (`'of 2,880 hrs available'`, `'2,880 hrs this month'`, 4 week-state
per-bar labels, 2 state-state per-bar labels) are behind the chart-selector
state and therefore absent from the compute-v2 probe artefact.

Also re-captures all default-state (`door`) strings + tile-notes for
completeness, so the residuals wave has ONE probe artefact that covers all
17 target strings for the rule-must-match-rendered-DOM invariant.

Output: /app/assessment_workspace/tools/compute_residuals_dom_map.json
        shape: {
          "chart_states_enumerated": ["door", "week", "state"],
          "per_state": {"door": {total, unique, byText}, "week": {...}, "state": {...}},
          "byText_union": {text -> occurrences across all states},
        }
"""
import sys, time, json, os
sys.path.insert(0, "/opt/plugins-venv/lib/python3.11/site-packages")
from playwright.sync_api import sync_playwright

XFF = "127.0.0.1, pod-lb, cf-edge"

def install(context):
    def handler(route, request):
        url = request.url
        if url.startswith("https://akki-reuse-assess.preview.emergentagent.com"):
            new_url = url.replace("https://akki-reuse-assess.preview.emergentagent.com", "http://localhost:8001")
            try:
                headers = dict(request.headers); headers["x-forwarded-for"] = XFF
                resp = context.request.fetch(new_url, method=request.method, headers=headers, data=request.post_data)
                route.fulfill(status=resp.status, headers=resp.headers, body=resp.body())
            except Exception as e:
                route.fulfill(status=502, body=f"{e}")
        else:
            route.continue_()
    context.route("**/*", handler)


def click_label(page, label):
    page.evaluate(rf"""() => {{
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const els = Array.from(doc.querySelectorAll('span, div')).filter(s => (s.textContent||'').trim() === '{label}');
        for (const s of els) {{
            let el = s.parentElement || s;
            for (let i=0; i<12 && el; i++) {{
                const style = (el.getAttribute('style') || '').replace(/\s/g, '');
                if (style.includes('cursor:pointer')) {{ el.click(); return; }}
                el = el.parentElement;
            }}
        }}
    }}""")


def set_chart_state(page, state_value):
    """Programmatically switch the compute-chart <select> to a specific state
    and dispatch the change event so React updates.

    Returns the JS return value directly (not None) so the caller can branch on
    the boolean.
    """
    return page.evaluate(rf"""() => {{
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        // Try native <select> first; some sc-raw-select impls render as native.
        const selects = Array.from(doc.querySelectorAll('select'));
        for (const sel of selects) {{
            const opts = Array.from(sel.options).map(o => o.value).sort().join(',');
            if (opts === 'door,state,week') {{
                sel.value = '{state_value}';
                sel.dispatchEvent(new Event('input', {{bubbles: true}}));
                sel.dispatchEvent(new Event('change', {{bubbles: true}}));
                return true;
            }}
            // Fallback: check option TEXT labels rather than values.
            const labels = Array.from(sel.options).map(o => (o.textContent||'').trim()).sort().join('|');
            if (labels === 'Hours by door|Hours by state|Hours by week') {{
                const wanted = {{'door':'Hours by door','week':'Hours by week','state':'Hours by state'}}['{state_value}'];
                const target = Array.from(sel.options).find(o => (o.textContent||'').trim() === wanted);
                if (target) {{
                    sel.value = target.value;
                    sel.dispatchEvent(new Event('input', {{bubbles: true}}));
                    sel.dispatchEvent(new Event('change', {{bubbles: true}}));
                    return true;
                }}
            }}
        }}
        return false;
    }}""")


def enumerate_dom(page):
    """Return {total, unique, byText} of visible text nodes in the prototype iframe."""
    return page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
        const nodes = [];
        let n;
        while ((n = walker.nextNode())) {
            const t = (n.nodeValue || '').trim();
            if (t.length < 1) continue;
            if (t.length > 300) continue;
            if (!n.parentElement) continue;
            if (n.parentElement.tagName === 'SCRIPT' || n.parentElement.tagName === 'STYLE') continue;
            const p = n.parentElement;
            const grandparent = p.parentElement;
            const gp2 = grandparent && grandparent.textContent || '';
            nodes.push({
                text: t,
                parentTag: p.tagName,
                parentTestId: p.getAttribute('data-testid') || '',
                parentClass: (p.className || '').slice(0, 40),
                parentText: (p.textContent || '').slice(0, 200),
                grandparentText: gp2.slice(0, 300),
            });
        }
        const byText = {};
        for (const nd of nodes) {
            if (!byText[nd.text]) byText[nd.text] = [];
            byText[nd.text].push(nd);
        }
        return { total: nodes.length, unique: Object.keys(byText).length, byText };
    }""")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox","--disable-dev-shm-usage"])
    context = browser.new_context(viewport={"width":1600,"height":900}, extra_http_headers={"X-Forwarded-For": XFF})
    install(context)
    page = context.new_page()
    page.goto("http://localhost:3000/", wait_until="domcontentloaded", timeout=60000)
    for _ in range(60):
        n = page.evaluate("""() => {const i=document.querySelector('[data-testid="v8-prototype-iframe"]');return i&&i.contentDocument&&i.contentDocument.body?i.contentDocument.body.textContent.length:0;}""")
        if n >= 100_000: break
        time.sleep(0.5)
    time.sleep(2)

    click_label(page, "Admin"); time.sleep(1.5)
    click_label(page, "Registry"); time.sleep(2)
    page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const btns = Array.from(doc.querySelectorAll('button')).filter(b => (b.textContent||'').trim().startsWith('Go to Registry'));
        if (btns.length) btns[0].click();
    }"""); time.sleep(2)
    click_label(page, "Compute Connected"); time.sleep(3)

    # First: enumerate the DEFAULT rendered state (whatever s.computeChart is on load).
    default_dom = enumerate_dom(page)
    print(f"default (pre-switch) · total={default_dom['total']} · unique={default_dom['unique']}")

    per_state = {"__default__": default_dom}
    for state in ["door", "week", "state"]:
        ok = set_chart_state(page, state)
        if not ok:
            print(f"WARN: set_chart_state({state!r}) could not locate the compute-chart select · skipping")
            per_state[state] = {"total": 0, "unique": 0, "byText": {}, "error": "select_not_found"}
            continue
        time.sleep(1.5)  # allow React to re-render after change event
        dom = enumerate_dom(page)
        per_state[state] = dom
        print(f"state={state!r} · total={dom['total']} · unique={dom['unique']}")

    # Union byText across default + all three chart states (occurrences summed).
    byText_union = {}
    for state, dom in per_state.items():
        for text, entries in dom.get("byText", {}).items():
            if text not in byText_union:
                byText_union[text] = 0
            byText_union[text] += len(entries)

    out = {
        "chart_states_enumerated": ["door", "week", "state"],
        "per_state": per_state,
        "byText_union": byText_union,
    }
    with open("/app/assessment_workspace/tools/compute_residuals_dom_map.json", "w") as fw:
        json.dump(out, fw, indent=2)

    # Report: which of the 17 residuals targets are covered
    targets = [
        # r1 chart captions (3)
        "1,240 hrs committed",
        "of 2,880 hrs available",
        "2,880 hrs this month",
        # r1 per-bar labels (11)
        "645 hrs · 52%", "298 hrs · 24%", "174 hrs · 14%", "99 hrs · 8%", "24 hrs · 2%",
        "274 hrs · 38%", "339 hrs · 47%", "65 hrs · 9%", "43 hrs · 6%",
        "1,240 hrs · 43%", "1,640 hrs · 57%",
        # r2 tile notes (3)
        "43% of the month", "wall-clock across 4 GPUs", "quoted against, not reserved",
    ]
    found, missing = [], []
    for t in targets:
        if t in byText_union:
            found.append(t)
        else:
            missing.append(t)
    print(f"\n=== RESIDUALS TARGET COVERAGE ===")
    print(f"found {len(found)}/{len(targets)}, missing {len(missing)}")
    for m in missing:
        print(f"  MISSING: {m!r}")
    browser.close()
