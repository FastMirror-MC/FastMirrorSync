"""
@File      : src/client/client.py
@Author    : Skeleton_321
@CreateDate: 2022/2/5 21:52
by IntelliJ IDEA
"""
from __future__ import annotations

import os
import uuid
import logging
import sys
from io import BytesIO

from requests import Response

from .persistence import ResourceManager
from .utils import *


__all__ = ["sync_client"]


submit_url = os.getenv("SUBMIT_URL")
if submit_url == "" or submit_url is None:
    logging.error("environment variable SUBMIT_URL is required.")
    logging.error("example: https://localhost/submit")
    exit(-1)


class sync_client:
    def __init__(self, name, client_name=None, level=logging.INFO):
        client_name = client_name if client_name is not None else name
        self.name = name
        self.client_id = str(uuid.uuid5(uuid.NAMESPACE_X500, client_name))
        self.resources = ResourceManager(name, level)

        self.need_skip = self.resources.config.is_skipped
        self.set = self.resources.config.set
        self.append = self.resources.config.append

        self.debug = self.resources.log.debug
        self.info = self.resources.log.info
        self.warning = self.resources.log.warning
        self.error = self.resources.log.error
        self.exception = self.resources.log.exception
        self.critical = self.resources.log.critical

    def __enter__(self):
        self.__start_time__ = get_mills_time()
        self.info(f"task {self.name} start.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.info(f"task {self.name} finished in {(get_mills_time() - self.__start_time__) / 1000}s.")
        if exc_type is not None:
            self.exception("exit with exception.", exc_info=exc_type)
        self.resources.config.save()

    def get(self, url, stream=False):
        return proxy_invoke(
            self, get, "get", 1,
            url=url, timeout=360, verify=False, headers={"User-Agent": USERAGENT}, stream=stream)

    def download_and_submit(
            self,
            url: str,
            version: str,
            build: int,
            release: bool,
            update_time: datetime.datetime | str | int,
            checksum: str = None,
            mode: str = None,
            core_version: str = None,
            unittest: bool = False
    ):
        self.info(f'download {self.name}-{version}-{core_version} at {url}')
        with BytesIO() as stream:
            if not unittest:
                res: Response = self.get(url, True)
                if res is None:
                    return None
                for chunk in res.iter_content(chunk_size=1024 * 128):
                    print('.', end='', file=sys.stderr, flush=True)
                    stream.write(chunk)
                print(file=sys.stderr, flush=True)
                if if_file_invalid(self, stream, checksum, mode):
                    self.error("file verification failed.")
                    return None
            else:
                self.warning("download is skipped because of unittest.")
            # submit
            self.submit(
                version=version,
                core_version=core_version,
                build=build,
                release=release,
                update_time=update_time,
                stream=stream,
                unittest=unittest
            )

    def submit(
            self,
            version: str,
            build: int,
            release: bool,
            update_time: datetime.datetime | str | int,
            stream,
            core_version: str = None,
            unittest: bool = False
    ):
        if type(update_time) == int:
            update_time: datetime.datetime = datetime.datetime.fromtimestamp(update_time)
        if type(update_time) == datetime.datetime:
            update_time: str = dt2str(update_time)

        if core_version is None:
            core_version = f"build{build}"

        params = {
            "name": self.name,
            "version": version,
            "coreVersion": core_version,
            "build": build,
            "release": release,
            "updateTime": update_time,
            "sha1": get_checksum(stream)
        }
        headers = {
            "token": self.resources.token,
            "clientId": self.client_id
        }

        self.info(f"try submit {self.name}-{version}-{core_version}.")
        self.info(f"submit to: {submit_url}")
        self.info(f"info: {params}")

        if unittest:
            return

        stream.seek(0, 0)
        proxy_invoke(
            log=self, callback=post, url=submit_url, sign="submit", params=params,
            headers=headers, files={"file": stream}
        )
