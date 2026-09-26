async def run_test(page, output_dir, page_url):
    await page.set_viewport_size({"width": 1920, "height": 800})
    responses = []
    page.on('response', lambda r: responses.append({'path': '/api/portal/census/overview', 'status': r.status}) if '/api/portal/census/overview' in r.url else None)
    try:
        await page.goto('https://pensive-goodall-6.preview.emergentagent.com/dap', wait_until='networkidle')
        await page.evaluate('() => { sessionStorage.clear(); window.dispatchEvent(new Event("akki-session-changed")); }')
        await page.get_by_test_id('census-signin').wait_for()
        print('PASS signed-out overview calls:', len(responses))
        for email, password in [('demo.operator@demo.rms.example.com','demo-operator-pw'), ('demo.analyst@demo.rms.example.com','demo-analyst-pw')]:
            await page.get_by_test_id('census-email').fill(email)
            await page.get_by_test_id('census-password').fill(password)
            async with page.expect_response(lambda r: '/api/auth/login' in r.url) as login_info:
                await page.get_by_test_id('census-signin-submit').click()
            login_response = await login_info.value
            assert login_response.status == 200
            await page.get_by_test_id('census-signin').wait_for(state='hidden')
            await page.goto('https://pensive-goodall-6.preview.emergentagent.com/dap/extract/processed', wait_until='networkidle')
            await page.get_by_test_id('dap-request-submit').wait_for()
            if 'analyst' in email:
                assert await page.get_by_test_id('dap-request-submit').is_disabled()
                assert await page.locator('[data-testid^="dap-work-id-"]').count() == 0
                print('PASS analyst write disabled; no operator requests visible')
            else:
                assert await page.get_by_test_id('dap-request-submit').is_enabled()
                print('PASS operator scope loaded')
            await page.get_by_test_id('prototype-account-trigger').click()
            await page.get_by_test_id('prototype-account-signout').click()
            await page.get_by_test_id('census-signin').wait_for()
            await page.wait_for_load_state('networkidle')
            print('PASS signed out cleanly')
        print('OVERVIEW RESPONSES', responses)
        assert not any(r['status'] == 401 for r in responses)
        print('PASS no overview401 across complete operator and analyst session transitions')
    except Exception as exc:
        print('FAIL', str(exc))
