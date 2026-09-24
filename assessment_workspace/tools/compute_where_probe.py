"""Where in the prototype's DOM does '840 vCPU-h/day' actually render?
Search on multiple surfaces: portal, after Admin, after Registry aside,
after 'Go to Registry' button, after Compute Connected.
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

def search(page, label):
    return page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const dummies = ['840 vCPU-h/day', 'Total capacity', '62%', 'Allocated to Build', '3 queued', 'Queue depth'];
        const results = {};
        const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
        const hits = {d: {}};
        for (const d of dummies) hits[d] = { count: 0, parent_tags: [] };
        let node;
        while ((node = walker.nextNode())) {
            const t = (node.nodeValue || '');
            for (const d of dummies) {
                if (t.trim() === d || (t.includes(d) && node.parentElement && node.parentElement.tagName !== 'SCRIPT')) {
                    if (node.parentElement && node.parentElement.tagName === 'SCRIPT') continue;
                    hits[d].count++;
                    if (hits[d].parent_tags.length < 3) {
                        hits[d].parent_tags.push(node.parentElement && node.parentElement.tagName);
                    }
                }
            }
        }
        return hits;
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

    print("--- portal surface ---")
    print(json.dumps(search(page, "portal"), indent=2))

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
    print("--- after Admin click ---")
    print(json.dumps(search(page, "admin"), indent=2))

    click_label("Registry"); time.sleep(2)
    print("--- after Admin → Registry click (aside view) ---")
    print(json.dumps(search(page, "reg_aside"), indent=2))

    page.evaluate(r"""() => {
        const iframe = document.querySelector('[data-testid="v8-prototype-iframe"]');
        const doc = iframe.contentDocument;
        const btns = Array.from(doc.querySelectorAll('button')).filter(b => (b.textContent||'').trim().startsWith('Go to Registry'));
        if (btns.length) btns[0].click();
    }""")
    time.sleep(2)
    print("--- after Go to Registry button ---")
    print(json.dumps(search(page, "reg_tab"), indent=2))

    click_label("Compute Connected"); time.sleep(3)
    print("--- after Compute Connected click ---")
    print(json.dumps(search(page, "compute"), indent=2))

    browser.close()
