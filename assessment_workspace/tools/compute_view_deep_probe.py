"""Deeper probe · what's ACTUALLY rendered on the Compute Connected view?
Dump the enclosing container's structure + all visible text nearby.
"""
import sys, time, json
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
    context = browser.new_context(viewport={"width": 1600, "height": 900}, extra_http_headers={"X-Forwarded-For": XFF})
    install(context)
    page = context.new_page()
    page.goto("http://localhost:3000/", wait_until="domcontentloaded", timeout=60000)
    for _ in range(60):
        n = page.evaluate("""() => {const i=document.querySelector('[data-testid="v8-prototype-iframe"]');return i&&i.contentDocument&&i.contentDocument.body?i.contentDocument.body.textContent.length:0;}""")
        if n >= 100_000: break
        time.sleep(0.5)
    time.sleep(2)
    # nav path
    for label in ['Admin', 'Registry']:
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
        time.sleep(1.5)
    # click Go to Registry
    page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const btns = Array.from(doc.querySelectorAll('button')).filter(b => (b.textContent||'').trim().startsWith('Go to Registry'));
        if (btns.length) btns[0].click();
    }""")
    time.sleep(2)
    # click Compute Connected
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
    # Deep dump: find the 62% node and dump its 8-level ancestor chain textContent
    result = page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
        let node, out = null;
        while ((node = walker.nextNode())) {
            const t = (node.nodeValue || '').trim();
            if (t === '62%') {
                // ignore script
                if (node.parentElement && node.parentElement.tagName === 'SCRIPT') continue;
                out = { text: t };
                let anc = node.parentElement;
                let chain = [];
                for (let i=0; i<10 && anc; i++) {
                    chain.push({
                        tag: anc.tagName,
                        cls: (anc.className || '').slice(0, 60),
                        testId: anc.getAttribute('data-testid') || '',
                        childElCount: anc.children.length,
                        textContent: (anc.textContent || '').slice(0, 200),
                    });
                    anc = anc.parentElement;
                }
                out.chain = chain;
                break;
            }
        }
        // Also list all visible content around any regTabsView / computeCards markers
        const regTabsMatch = Array.from(doc.querySelectorAll('*')).filter(el => {
            const t = (el.textContent || '').trim();
            return t.startsWith('Compute Connected') || t.startsWith('Data Connected') || t === 'Compute Connected';
        }).slice(0, 5);
        const nearby = regTabsMatch.map(el => ({
            tag: el.tagName,
            testId: el.getAttribute('data-testid') || '',
            childCount: el.children.length,
            text: (el.textContent || '').slice(0, 300),
        }));
        // Sample text nodes with attention_mask (interesting text)
        const sampleText = [];
        const walker2 = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
        let n;
        while ((n = walker2.nextNode())) {
            const t = (n.nodeValue || '').trim();
            if (t.length < 3) continue;
            if (n.parentElement && (n.parentElement.tagName === 'SCRIPT' || n.parentElement.tagName === 'STYLE')) continue;
            if (t.includes('%') || t.includes('vCPU') || t.includes('GPU') || t.includes('Compute') || t.includes('capacity') || t.includes('queue')) {
                sampleText.push({t, parentTag: n.parentElement && n.parentElement.tagName});
                if (sampleText.length >= 15) break;
            }
        }
        return { chain: out, nearby, sampleText };
    }""")
    print(json.dumps(result, indent=2))
    browser.close()
