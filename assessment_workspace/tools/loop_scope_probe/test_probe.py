import asyncio
import pytest


@pytest.mark.asyncio
async def test_report_loop_id(_probe_fixture_loop):
    """Print test-body loop id vs fixture-body loop id."""
    test_loop = asyncio.get_running_loop()
    fixture_loop = _probe_fixture_loop
    print(f"[TEST_BODY] loop id={id(test_loop)} running={test_loop.is_running()} closed={test_loop.is_closed()}", flush=True)
    print(f"[COMPARISON] fixture_loop_id={id(fixture_loop)}  test_loop_id={id(test_loop)}  SAME={id(fixture_loop) == id(test_loop)}", flush=True)
    print(f"[COMPARISON] fixture_loop_closed={fixture_loop.is_closed()}  test_loop_closed={test_loop.is_closed()}", flush=True)
