"""
@File      : /sync.py.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 8:29
by IntelliJ IDEA
"""
import asyncio
import atexit
import importlib
import sys
import traceback

from lib import log
from lib import http
from plugin import active
from plugin import *

__async_enable__ = False


async def run(cls):
    try:
        async with cls() as o:
            await o.run()
    except Exception as e:
        log.exception(f"occurred exception at task {cls.name()}", exc_info=e)
        pass


async def main():
    if __async_enable__:
        await asyncio.wait([
            run(getattr(importlib.import_module(f"plugin.{plugin}"), plugin))
            for plugin in active
        ])
    else:
        for plugin in active:
            await run(getattr(importlib.import_module(f"plugin.{plugin}"), plugin))


@atexit.register
def exit_handler():
    loop.run_until_complete(http.client_close())
    loop.close()
    exc_type, exc_value, exc_tb = sys.exc_info()
    if exc_value is not None:
        traceback.print_exception(exc_type, exc_value, exc_tb)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
