async def run_test(page, output_dir, page_url):
    await page.set_viewport_size({"width": 390, "height": 844})
    try:
        await page.goto('https://pensive-goodall-6.preview.emergentagent.com/dap', wait_until='domcontentloaded')
        login = await page.request.post('https://pensive-goodall-6.preview.emergentagent.com/api/auth/login', data={'email':'demo.operator@demo.rms.example.com','password':'demo-operator-pw'})
        token = (await login.json())['access_token']
        await page.evaluate('(t) => sessionStorage.setItem("akki_access_token", t)', token)
        await page.goto('https://pensive-goodall-6.preview.emergentagent.com/dap/extract/processed?request=req-a92839f21269929d3cbea3860a17caf2', wait_until='networkidle')
        drawer = page.get_by_test_id('dap-work-detail')
        await drawer.wait_for(state='visible')
        assert 'recorded history' in (await drawer.inner_text()).lower()
        assert await page.get_by_test_id('prototype-mobile-nav').count() == 0
        await page.get_by_test_id('dap-work-detail-close').click()
        await drawer.wait_for(state='hidden')
        await page.get_by_test_id('prototype-mobile-nav').wait_for(state='visible')
        print('PASS loaded request detail, factual history, close control and restored mobile navigation')
    except Exception as exc:
        print('FAIL', repr(exc))
