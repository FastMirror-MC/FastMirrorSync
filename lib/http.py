"""
@File      : lib/http.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 13:51
by IntelliJ IDEA
"""
from __future__ import annotations

import datetime
import json
from io import BytesIO

import aiohttp

from lib import log, module
from lib.config import get_token, get_submit_url
from lib.utils import datetime2str, get_checksum, if_file_invalid

__all__ = ["aio_submit", "aio_download"]

USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 " \
            "Safari/537.36 Edg/97.0.1072.76"
session = aiohttp.ClientSession()


async def client_close():
    await session.close()


async def __request__(self, sign, retry, method, handler, **kwargs):
    self.debug(f"{sign}: {kwargs['url']}")
    kwargs["timeout"] = 60 if "timeout" not in kwargs else kwargs["timeout"]
    kwargs["headers"] = {
        "User-Agent": USERAGENT} if "headers" not in kwargs else kwargs["headers"]

    for i in range(retry):
        try:
            async with method(**kwargs) as response:
                if 200 <= response.status <= 300:
                    return await handler(response)
                self.warning(
                    f"{kwargs['url']} failed(code={response.status}).")
                self.warning(await response.text())
                return None
        except aiohttp.ClientError as e:
            self.exception(
                f"exception occurred at {sign}. retry({i + 1}/{retry})", exc_info=e)
    return None


def get_json():
    async def closure(response: aiohttp.ClientResponse):
        try:
            return await response.json()
        except json.decoder.JSONDecodeError as e:
            print(response.text())
            raise e

    return closure


def download_file(stream):
    async def closure(response: aiohttp.ClientResponse):
        stream.write(await response.read())
        return stream

    return closure


async def get(self, url, sign="get", retry=3, handler=None, **kwargs):
    kwargs["url"] = url
    return await __request__(self, sign, retry, session.get, get_json() if handler is None else handler, **kwargs)


async def post(self, url, sign="post", retry=3, handler=None, **kwargs):
    kwargs["url"] = url
    return await __request__(self, sign, retry, session.post, get_json() if handler is None else handler, **kwargs)


async def submit(self,
                 version: str,
                 build: int,
                 release: bool,
                 update_time: datetime.datetime | str | int,
                 stream,
                 core_version: str = None):
    if type(update_time) == int:
        update_time: datetime.datetime = datetime.datetime.fromtimestamp(
            update_time)
    if type(update_time) == datetime.datetime:
        update_time: str = datetime2str(update_time)

    if core_version is None:
        core_version = f"build{build}"
    pass
    params = {
        "name": self.name(),
        "version": version,
        "coreVersion": core_version,
        "build": build,
        "release": "true" if release else "false",
        "updateTime": update_time,
        "sha1": get_checksum(stream)
    }
    headers = {
        "token": get_token(),
        "clientId": self.client_id()
    }

    log.info(f"try submit {self.name()}-{version}-{core_version}.")
    log.info(f"submit to: {get_submit_url()}")
    log.info(f"info: {params}")

    if not getattr(self, "__submit_enable__", True) or getattr(self, "__debug_mode__", False):
        return True
    stream.seek(0, 0)

    async def handler(response):
        print("submit success.")
        return True

    return await self.post(
        url=get_submit_url(),
        sign="submit",
        params=params,
        headers=headers,
        data={"file": stream},
        handler=handler
    )


async def download(self, url, stream, checksum: str = None, mode: str = None):
    if getattr(self, "__download_enable__", True) and not getattr(self, "__debug_mode__", False):
        res = await self.get(url, sign="download", handler=download_file(stream))
        if res is None:
            self.error("server has no response.")
            return False
        if if_file_invalid(stream, checksum, mode):
            self.error("inconsistent checksum.")
            return False
    else:
        self.warning("download and checksum test are disable.")
    return True


async def download_and_submit(self,
                              url: str,
                              version: str,
                              build: int,
                              release: bool,
                              update_time: datetime.datetime | str | int,
                              core_version: str = None,
                              checksum: str = None,
                              mode: str = None):
    log.info(
        f'download {self.name()}-{version}-{core_version if core_version is not None else build} at {url}')
    with BytesIO() as stream:
        if not await download(self, url, stream, checksum, mode):
            return
        await submit(
            self=self,
            version=version,
            core_version=core_version,
            build=build,
            release=release,
            update_time=update_time,
            stream=stream
        )
    pass


@module.register("submit")
def aio_submit(cls):
    module.mount(cls, get)
    module.mount(cls, post)
    module.mount(cls, submit)


@module.register("download")
def aio_download(cls):
    module.mount(cls, get)
    module.mount(cls, post)
    module.override(cls, download_and_submit, "submit")
