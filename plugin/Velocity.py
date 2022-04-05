"""
@File      : plugin/Velocity.py
@Author    : Skeleton_321
@CreateDate: 2022/3/14 21:16
by IntelliJ IDEA
"""
from lib.http import aio_download
from lib.log import logger
from lib.plugin import Plugin
from lib.version import string_version


@logger
@string_version("./config")
@aio_download
class Velocity(Plugin):
    @staticmethod
    def name() -> str:
        return "Velocity"

    async def run(self) -> None:
        base_url = f"https://papermc.io/api/v2/projects/velocity"
        for version in (await self.get(base_url))["versions"]:
            builds = (await self.get(f"{base_url}/versions/{version}"))["builds"][-20:]
            builds.sort()
            for build in builds:
                core_version = f"{version}_build{build}"
                if not self.need_update(version, core_version):
                    continue
                self.info(f"{version} find a newer build: {build}")
                url = f"https://papermc.io/api/v2/projects/velocity/versions/{version}/builds/{build}"
                json = await self.get(url)
                application = json["downloads"]["application"]
                status = await self.submit(
                    url=f'{url}/downloads/{application["name"]}',
                    version="general",
                    build=build,
                    core_version=core_version,
                    update_time=json["time"],
                    release=json["channel"] == "default",
                    checksum=application["sha256"],
                    mode="sha256"
                )
                if status:
                    self.write(version, core_version)
            self.info(f"{version} is up-to-date")
