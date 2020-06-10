import asyncio

import pytest

from busypie import wait, SECOND

done = False


@pytest.mark.asyncio
async def test_wait_until_done():
    await asyncio.gather(wait_till_done(), set_done())


async def set_done():
    global done
    await asyncio.sleep(0.5)
    done = True


async def wait_till_done():
    global done
    await wait().at_most(0.6, SECOND).until_async(lambda: done)
    assert done
