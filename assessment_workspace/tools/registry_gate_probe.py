"""Probe: does 'Go to Registry →' button trigger regTabsView render?"""
import sys, time, json
sys.path.insert(0, "/opt/plugins-venv/lib/python3.11/site-packages")
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    ctx = browser.new_context(viewport={"width": 1600, "height": 900},
        extra_http_headers={"X-Forwarded-For": "127.0.0.1, pod-lb, cf-edge"})
    page = ctx.new_page()
    page.goto("http://localhost:3000/", timeout=60000)
    time.sleep(6)
    page.evaluate(r"""() => {
        const doc = document.querySelector('[data-testid="v8-prototype-iframe"]').contentDocument;
        const els = Array.from(doc.querySelectorAll('span, div')).filter(s => (s.textContent||'').trim() === 'Admin');
        for (const s of els) { let el = s.parentElement || s; for (let i=0; i<12 && el; i++) { if (((el.getAttribute('style')||'').replace(/\s/g,'')).includes('cursor:pointer')) { el.click(); return; } el = el.parentElement; } }
    }""")
    time.sleep(2)
    # click "Go to Registry →" button
    r = page.evaluate(r"""() => {
        const doc = document.querySelector('[data-testid="v8-prototype-iframe"]').contentDocument;
        const btns = Array.from(doc.querySelectorAll('button')).filter(b => (b.textContent||'').trim().startsWith('Go to Registry'));
        if (btns.length === 0) return { ok: false, candidates: 0 };
        btns[0].click();
        return { ok: true, count: btns.length, text: (btns[0].textContent||'').trim() };
    }""")
    print(f"click 'Go to Registry →' button: {r}")
    time.sleep(3.5)
    # Now check for tabs
    hits = page.evaluate(r"""() => {
        const doc = document.querySelector('[data-testid="v8-prototype-iframe"]').contentDocument;
        const targets = ['Data Connected', 'Compute Connected', 'LLMs & Trained Models', '840 vCPU-h/day', 'Total capacity', 'Queue depth', 'Allocated to Build', '62%', '3 queued', 'DATA CONNECTED', 'COMPUTE CONNECTED'];
        const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_ELEMENT);
        const out = {};
        let el;
        while ((el = walker.nextNode())) {
            if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') continue;
            for (const c of el.childNodes) {
                if (c.nodeType === 3) {
                    const t = (c.nodeValue||'').trim();
                    for (const target of targets) {
                        if (t === target) out[target] = (out[target]||0)+1;
                    }
                }
            }
        }
        return out;
    }""")
    print(f"tab-label / tile hits after Go-to-Registry: {hits}")

    # If Compute Connected label present, click it
    if "Compute Connected" in hits:
        page.evaluate(r"""() => {
            const doc = document.querySelector('[data-testid="v8-prototype-iframe"]').contentDocument;
            const els = Array.from(doc.querySelectorAll('div')).filter(s => (s.textContent||'').trim() === 'Compute Connected');
            for (const el of els) {
                const st = (el.getAttribute('style')||'').replace(/\s/g,'');
                if (st.includes('cursor:pointer')) { el.click(); return; }
            }
        }""")
        time.sleep(2.5)
        hits2 = page.evaluate(r"""() => {
            const doc = document.querySelector('[data-testid="v8-prototype-iframe"]').contentDocument;
            const targets = ['840 vCPU-h/day', 'Total capacity', 'Queue depth', 'Allocated to Build', '62%', '3 queued'];
            const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_ELEMENT);
            const out = {};
            let el;
            while ((el = walker.nextNode())) {
                if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE') continue;
                for (const c of el.childNodes) {
                    if (c.nodeType === 3) {
                        const t = (c.nodeValue||'').trim();
                        for (const target of targets) {
                            if (t === target) out[target] = (out[target]||0)+1;
                        }
                    }
                }
            }
            return out;
        }""")
        print(f"computeCards hits after Compute Connected click: {hits2}")

    browser.close()
