import asyncio
import pytest_asyncio


@pytest_asyncio.fixture(autouse=True)
async def _probe_fixture_loop(capsys):
    loop = asyncio.get_running_loop()
    print(f"[FIXTURE] loop id={id(loop)} running={loop.is_running()} closed={loop.is_closed()}", flush=True)
    yield loop
