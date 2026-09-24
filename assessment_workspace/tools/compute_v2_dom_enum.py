"""Deep DOM enumeration of the Compute Connected sub-tab.

Objective: enumerate EVERY visible text node on that surface so W-G5c-COMPUTE-v2
can author rules ONLY against dummies with a unique, stable anchor.

For each dummy, capture:
  - trimmed text
  - parent tag / data-testid / class (first 40 chars)
  - immediate ancestor's textContent (up to 300 chars) — for anchor authorship
  - depth (how many ancestors from body)

Write output to /app/assessment_workspace/tools/compute_v2_dom_map.json
"""
import sys, time, json, os
sys.path.insert(0, "/opt/plugins-venv/lib/python3.11/site-packages")
from playwright.sync_api import sync_playwright

XFF = "127.0.0.1, pod-lb, cf-edge"

def install(context):
    def handler(route, request):
        url = request.url
        if url.startswith("https://pensive-goodall-6.preview.emergentagent.com"):
            new_url = url.replace("https://pensive-goodall-6.preview.emergentagent.com", "http://localhost:8001")
            try:
                headers = dict(request.headers); headers["x-forwarded-for"] = XFF
                resp = context.request.fetch(new_url, method=request.method, headers=headers, data=request.post_data)
                route.fulfill(status=resp.status, headers=resp.headers, body=resp.body())
            except Exception as e:
                route.fulfill(status=502, body=f"{e}")
        else:
            route.continue_()
    context.route("**/*", handler)


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

    def click_label(label):
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

    click_label("Admin"); time.sleep(1.5)
    click_label("Registry"); time.sleep(2)
    page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const btns = Array.from(doc.querySelectorAll('button')).filter(b => (b.textContent||'').trim().startsWith('Go to Registry'));
        if (btns.length) btns[0].click();
    }"""); time.sleep(2)
    click_label("Compute Connected"); time.sleep(3)

    dom = page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        // Walk visible text nodes
        const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
        const nodes = [];
        let n;
        while ((n = walker.nextNode())) {
            const t = (n.nodeValue || '').trim();
            if (t.length < 1) continue;
            if (t.length > 300) continue;  // narrative paragraphs skipped for this pass
            if (!n.parentElement) continue;
            if (n.parentElement.tagName === 'SCRIPT' || n.parentElement.tagName === 'STYLE') continue;
            // Only include if this text node is inside the RegistryTab-Compute-Connected
            // area (approximate: some ancestor mentions "Compute Connected" tab or the
            // compute pane. Instead of trying to isolate, we just capture all visible
            // text — the compute view is the only major visible surface right now).
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
        // Dedupe by text
        const byText = {};
        for (const nd of nodes) {
            if (!byText[nd.text]) byText[nd.text] = [];
            byText[nd.text].push(nd);
        }
        return { total: nodes.length, unique: Object.keys(byText).length, byText };
    }""")
    with open("/app/assessment_workspace/tools/compute_v2_dom_map.json", "w") as fw:
        json.dump(dom, fw, indent=2)
    print(f"total visible text nodes: {dom['total']}, unique: {dom['unique']}")
    # print unique texts sorted alphabetically
    for k in sorted(dom['byText'].keys()):
        occurrences = len(dom['byText'][k])
        p = dom['byText'][k][0]
        print(f"  [{occurrences}] {k!r:<70} · in <{p['parentTag']}> · ...{p['grandparentText'][-90:]!r}")
    browser.close()
