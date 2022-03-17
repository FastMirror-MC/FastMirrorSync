"""
@File      : plugin/Spigot.py
@Author    : Skeleton_321
@CreateDate: 2022/2/23 17:40
by IntelliJ IDEA
"""
import datetime
import os

from lib.http import aio_submit
from lib.log import logger
from lib.plugin import Plugin
from lib.version import string_version
from lib import __cache_root_path__
import docker

mc_versions = [
    "1.18",
    "1.18.1",
    "1.17",
    "1.17.1",
    "1.16.5",
    "1.16.4",
    "1.16.3",
    "1.16.2",
    "1.16.1",
    "1.15.2",
    "1.15.1",
    "1.15",
    "1.14.4",
    "1.14.3",
    "1.14.2",
    "1.14.1",
    "1.14",
    "1.13.2",
    "1.13.1",
    "1.13",
    "1.12.2",
    "1.12.1",
    "1.12",
    "1.11.2",
    "1.11.1",
    "1.11",
    "1.10.2",
    "1.9.4",
    "1.9.2",
    "1.9",
    "1.8.8",
    "1.8.3",
    "1.8",
]
client = docker.from_env()

cache_path = f"{__cache_root_path__}/spigot"

if not os.path.exists(cache_path):
    os.makedirs(cache_path)


@logger
@aio_submit
@string_version("./config")
class Spigot(Plugin):
    @staticmethod
    def name() -> str:
        return "Spigot"

    async def ci(self, ver):
        container = client.containers.get(f"spigot-{ver}")
        container.start()
        filename = None
        for line in container.attach(stdout=True, stderr=True, stream=True):
            log = line.decode().strip()
            if "Saved as" in log and "spigot" in log:
                filename = log[log.rfind('/') + 1:]
            self.info(f"[{ver}] {log}")
        return filename

    async def run(self) -> None:
        async def task(version):
            json = await self.get(f"https://hub.spigotmc.org/versions/{version}.json")
            build = json["name"]
            if not self.need_update(version, build):
                return
            self.info(f"{version} has a new build {build}.")
            filename = await self.ci(version)
            if not filename:
                self.info(f"{version} build failed. ")
                return
            with open(f"{cache_path}/{version}/{filename}", "rb") as stream:
                await self.submit(
                    version=version,
                    build=build,
                    release=True,
                    update_time=datetime.datetime.now(),
                    stream=stream
                )
        for v in mc_versions:
            await task(v)
