"""Browser checks without screenshots; never accesses estate hosts or commissions work."""
import asyncio
import json
import os
from pathlib import Path
from datetime import datetime, timezone
from playwright.async_api import async_playwright


async def main():
    base = os.environ['FIDELITY_BASE_URL'].rstrip('/')
    out = Path(os.environ['FIDELITY_REPORT_PATH'])
    errors, checks = [], []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(executable_path=os.environ['PLAYWRIGHT_CHROME_EXECUTABLE_PATH'],
                                           headless=True, args=['--no-sandbox'])
        context = await browser.new_context()
        page = await context.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
        await page.goto(base + '/dap', wait_until='networkidle')
        await page.get_by_test_id('census-email').fill(os.environ['FIDELITY_EMAIL'])
        await page.get_by_test_id('census-password').fill(os.environ['FIDELITY_PASSWORD'])
        await page.get_by_test_id('census-signin-submit').click()
        await page.get_by_text('2,642 tables recorded.', exact=False).wait_for(timeout=20000)
        for width in [320, 390, 768, 1024, 1440, 1920]:
            await page.set_viewport_size({'width': width, 'height': 844})
            for route in ['/dap', '/dap/census', '/dap/census?record=census-4', '/os', '/os/admin/estate',
                          '/os/admin/estate?view=history', '/os/admin/estate?view=history&record=cr-a29e3b7b16ae']:
                await page.goto(base + route, wait_until='networkidle')
                await page.locator('[data-testid^="owner-prototype-"]').wait_for()
                geometry = await page.evaluate('''() => ({width:document.documentElement.clientWidth,
                  scroll:document.documentElement.scrollWidth,
                  offenders:[...document.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>innerWidth+1)
                   .slice(0,8).map(e=>({tag:e.tagName,line:e.dataset.protoLine,text:(e.innerText||'').slice(0,70),right:e.getBoundingClientRect().right}))})''')
                checks.append({'width': width, 'route': route, 'pass': geometry['scroll'] <= width + 1, **geometry})
        canonical = await page.get_by_text('Run cr-a29e3b7b16ae', exact=True).count()
        # Exercise real disclosure/list state after rerenders; no queue mutation.
        await page.goto(base + '/os/admin/estate', wait_until='networkidle')
        for action in ['toggleCensusRead', 'toggleCensusCare', 'toggleCensusMix', 'toggleCensusHow']:
            await page.locator(f'[data-action="{action}"]').click()
        await page.locator('[data-action="openMeasured"]').first.click()
        await page.locator('[data-proto-line="5637"]').last.click()
        tabs = page.locator('[data-action="t.onClick"]')
        for i in range(await tabs.count()):
            await tabs.nth(i).click()
        await browser.close()
    expected = [e for e in errors if 'Failed to load resource: the server responded with a status of 401' in e]
    unexpected = [e for e in errors if e not in expected]
    result = {'at_utc': datetime.now(timezone.utc).isoformat(), 'method': 'headless browser geometry/interactions only; no screenshots or source operations',
              'layout_checks': checks, 'failed_layouts': [r for r in checks if not r['pass']],
              'canonical_run_id_visible': canonical > 0, 'console_errors': errors,
              'expected_anonymous_401_errors': expected, 'unexpected_errors': unexpected,
              'all_pass': not unexpected and all(r['pass'] for r in checks) and canonical > 0}
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'checks': len(checks), 'failed_layouts': result['failed_layouts'],
                      'canonical_run_id_visible': result['canonical_run_id_visible'], 'unexpected_errors': unexpected,
                      'all_pass': result['all_pass']}, indent=2))


if __name__ == '__main__':
    asyncio.run(main())