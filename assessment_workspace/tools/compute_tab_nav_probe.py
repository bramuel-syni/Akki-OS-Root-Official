"""Runtime-only probe for compute-tab nav resolution.

Goal: find the click sequence that sets `s.appOpen='estate'` in the
prototype, thereby activating `isRegistryGroup && isRegEstate` and
rendering `regTabsView` (with Compute Connected tab).

Byte-identity discipline: NO edits to v8_prototype.html. Only click
handlers already wired in the prototype.
"""
from __future__ import annotations

import json
import sys
import time

sys.path.insert(0, "/opt/plugins-venv/lib/python3.11/site-packages")
from playwright.sync_api import sync_playwright


CLICK_BY_LABEL_JS = r"""
(lbl) => {
    const doc = document.querySelector('[data-testid="v8-prototype-iframe"]').contentDocument;
    const els = Array.from(doc.querySelectorAll('span, div, button')).filter(s => (s.textContent||'').trim() === lbl);
    for (const s of els) {
        let el = s.parentElement || s;
        for (let i=0; i<15 && el; i++) {
            const st = (el.getAttribute('style') || '').replace(/\s/g,'');
            if (st.includes('cursor:pointer') || el.tagName === 'BUTTON') {
                el.click();
                return { ok: true, tag: el.tagName, level: i };
            }
            el = el.parentElement;
        }
    }
    return { ok: false, candidates: els.length };
}
"""

TAB_HITS_JS = r"""
() => {
    const doc = document.querySelector('[data-testid="v8-prototype-iframe"]').contentDocument;
    const targets = ['Data Connected', 'Compute Connected', 'LLMs & Trained Models', '840 vCPU-h/day', 'Total capacity', 'Queue depth', 'Allocated to Build', '62%', '3 queued'];
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
}
"""


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        ctx = browser.new_context(viewport={"width": 1600, "height": 900},
            extra_http_headers={"X-Forwarded-For": "127.0.0.1, pod-lb, cf-edge"})
        page = ctx.new_page()
        page.goto("http://localhost:3000/", timeout=60000)
        time.sleep(6)

        sequence = ["Admin", "Registry", "Registry"]
        for i, lbl in enumerate(sequence, 1):
            r = page.evaluate(CLICK_BY_LABEL_JS, lbl)
            print(f"[{i}] click {lbl!r}: {r}")
            time.sleep(2.5)
            hits = page.evaluate(TAB_HITS_JS)
            print(f"    hits after click: {hits}")
            print()

        # If tabs are present, click "Compute Connected"
        hits = page.evaluate(TAB_HITS_JS)
        if "Compute Connected" in hits:
            r = page.evaluate(CLICK_BY_LABEL_JS, "Compute Connected")
            print(f"click Compute Connected: {r}")
            time.sleep(2.5)
            hits2 = page.evaluate(TAB_HITS_JS)
            print(f"    hits after Compute Connected click: {hits2}")

        browser.close()
        return 0


if __name__ == "__main__":
    sys.exit(main())
