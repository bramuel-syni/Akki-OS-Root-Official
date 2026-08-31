"""Probe: identify which 'Registry' click leads to isRegistryGroup=true."""
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

    # Step 1: click Admin
    page.evaluate(r"""() => {
        const doc = document.querySelector('[data-testid="v8-prototype-iframe"]').contentDocument;
        const els = Array.from(doc.querySelectorAll('span, div')).filter(s => (s.textContent||'').trim() === 'Admin');
        for (const s of els) { let el = s.parentElement || s; for (let i=0; i<12 && el; i++) { if (((el.getAttribute('style')||'').replace(/\s/g,'')).includes('cursor:pointer')) { el.click(); return; } el = el.parentElement; } }
    }""")
    time.sleep(2.5)

    # After Admin click: enumerate ALL "Registry"-text elements with their context
    reg_elements = page.evaluate(r"""() => {
        const doc = document.querySelector('[data-testid="v8-prototype-iframe"]').contentDocument;
        const els = Array.from(doc.querySelectorAll('*')).filter(el => (el.textContent || '').trim() === 'Registry');
        return els.slice(0, 10).map((el, idx) => ({
            idx, tag: el.tagName,
            parent_tag: el.parentElement ? el.parentElement.tagName : '',
            parent_style_first_60: (el.parentElement && el.parentElement.getAttribute('style') || '').slice(0, 60),
            has_cursor_pointer_ancestor: (() => {
                let cur = el.parentElement; for (let i=0; i<10 && cur; i++) {
                    if (((cur.getAttribute('style')||'').replace(/\s/g,'')).includes('cursor:pointer')) return true;
                    cur = cur.parentElement;
                } return false;
            })(),
            grandparent_first_120: el.parentElement && el.parentElement.parentElement ? (el.parentElement.parentElement.textContent || '').trim().slice(0, 120) : '',
        }));
    }""")
    print(f"'Registry' text nodes after Admin click: {len(reg_elements)}")
    for r in reg_elements:
        print(f"  [{r['idx']}] tag={r['tag']} parent_tag={r['parent_tag']} clickable={r['has_cursor_pointer_ancestor']}")
        print(f"      grandparent_text[:120]: {r['grandparent_first_120']!r}")
    browser.close()
