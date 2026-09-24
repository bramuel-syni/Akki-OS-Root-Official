"""Probe: after Admin→Go to Registry→Compute Connected, what's in the DOM?

Answers: does computeCards render '840 vCPU-h/day', '62%', '3 queued',
'Total capacity', 'Allocated to Build', 'Queue depth'?
Also: what does compute view look like at the tile-1 element level?
"""
import sys, time
sys.path.insert(0, "/opt/plugins-venv/lib/python3.11/site-packages")
from playwright.sync_api import sync_playwright

XFF = "127.0.0.1, pod-lb, cf-edge"

def install_backend_url_rewrite(context):
    def handler(route, request):
        url = request.url
        if url.startswith("https://pensive-goodall-6.preview.emergentagent.com"):
            new_url = url.replace(
                "https://pensive-goodall-6.preview.emergentagent.com",
                "http://localhost:8001",
            )
            try:
                headers = dict(request.headers); headers["x-forwarded-for"] = XFF
                resp = context.request.fetch(new_url, method=request.method,
                                            headers=headers, data=request.post_data)
                route.fulfill(status=resp.status, headers=resp.headers, body=resp.body())
            except Exception as e:
                route.fulfill(status=502, body=f"{e}")
        else:
            route.continue_()
    context.route("**/*", handler)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox","--disable-dev-shm-usage"])
    context = browser.new_context(viewport={"width": 1600, "height": 900},
                                  extra_http_headers={"X-Forwarded-For": XFF})
    install_backend_url_rewrite(context)
    page = context.new_page()
    page.goto("http://localhost:3000/", wait_until="domcontentloaded", timeout=60000)
    # Wait for hydration
    for _ in range(60):
        n = page.evaluate("""() => {
            const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
            return iframe && iframe.contentDocument && iframe.contentDocument.body
                ? iframe.contentDocument.body.textContent.length : 0;
        }""")
        if n >= 100_000: break
        time.sleep(0.5)
    time.sleep(2)
    # Click Admin
    page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const els = Array.from(doc.querySelectorAll('span, div')).filter(s => (s.textContent||'').trim() === 'Admin');
        for (const s of els) {
            let el = s.parentElement || s;
            for (let i=0; i<12 && el; i++) {
                const style = (el.getAttribute('style') || '').replace(/\s/g, '');
                if (style.includes('cursor:pointer')) { el.click(); return; }
                el = el.parentElement;
            }
        }
    }""")
    time.sleep(1.5)
    # Click Registry
    page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const els = Array.from(doc.querySelectorAll('span, div')).filter(s => (s.textContent||'').trim() === 'Registry');
        for (const s of els) {
            let el = s.parentElement || s;
            for (let i=0; i<12 && el; i++) {
                const style = (el.getAttribute('style') || '').replace(/\s/g, '');
                if (style.includes('cursor:pointer')) { el.click(); return; }
                el = el.parentElement;
            }
        }
    }""")
    time.sleep(2)
    # Click Go to Registry
    page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const btns = Array.from(doc.querySelectorAll('button')).filter(b => (b.textContent||'').trim().startsWith('Go to Registry'));
        if (btns.length) btns[0].click();
    }""")
    time.sleep(2)
    # Click Compute Connected
    page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const els = Array.from(doc.querySelectorAll('span, div')).filter(s => (s.textContent||'').trim() === 'Compute Connected');
        for (const s of els) {
            let el = s.parentElement || s;
            for (let i=0; i<12 && el; i++) {
                const style = (el.getAttribute('style') || '').replace(/\s/g, '');
                if (style.includes('cursor:pointer')) { el.click(); return; }
                el = el.parentElement;
            }
        }
    }""")
    time.sleep(3)
    # Now probe: what's in the compute view?
    result = page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        // Search for expected dummies
        const dummies = ['840 vCPU-h/day', 'Total capacity', '62%', 'Allocated to Build', '3 queued', 'Queue depth'];
        const results = {};
        for (const d of dummies) {
            // Count occurrences in visible text
            const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
            let node, hits = 0;
            const contexts = [];
            while ((node = walker.nextNode())) {
                const t = (node.nodeValue || '');
                if (t.includes(d)) {
                    hits++;
                    // Get parent element info for context
                    let anc = node.parentElement;
                    let ancInfo = '';
                    if (anc) {
                        const tag = anc.tagName;
                        const cls = anc.className || '';
                        const testId = anc.getAttribute('data-testid') || '';
                        ancInfo = `<${tag}${testId?` data-testid="${testId}"`:''}${cls?` class="${cls.slice(0,30)}"`:''}>`;
                    }
                    if (contexts.length < 3) contexts.push({text: t.slice(0, 100), parent: ancInfo});
                }
            }
            results[d] = { hits, contexts };
        }
        // Also count elements with 'compute' related classes
        const anyComputeCards = doc.querySelectorAll('[data-testid*="compute" i], [class*="compute" i]').length;
        return { results, anyComputeCards, bodyLen: (doc.body.textContent || '').length };
    }""")
    import json
    print(json.dumps(result, indent=2))
    browser.close()
