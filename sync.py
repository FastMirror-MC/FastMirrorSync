"""
@File      : /sync.py.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 8:29
by IntelliJ IDEA
"""
import asyncio
import importlib

from lib import log
from plugin import active
from plugin import *
__async_enable__ = False

plugins = {}


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

# loop = asyncio.get_event_loop()
# tasks = [run(getattr(importlib.import_module(f"plugin.{plugin}"), plugin)) for plugin in active]
# loop.run_until_complete(asyncio.wait(tasks))
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
