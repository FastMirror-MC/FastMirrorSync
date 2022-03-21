"""
@File      : plugin/Purpur.py
@Author    : Skeleton_321
@CreateDate: 2022/2/23 17:30
by IntelliJ IDEA
"""
from lib.http import aio_download
from lib.log import logger
from lib.plugin import Plugin
from lib.version import integer_version


@logger
@integer_version("./config")
@aio_download
class Purpur(Plugin):
    @staticmethod
    def name() -> str:
        return "Purpur"

    async def run(self) -> None:
        api_url = "https://api.purpurmc.org/v2/purpur"
        for version in (await self.get(api_url))["versions"]:
            json = (await self.get(f"{api_url}/{version}"))["builds"]

            build = int(json["latest"])
            if not self.need_update(version, build):
                continue

            job = await self.get(f"{api_url}/{version}/{build}")
            if job["result"] != "SUCCESS":
                continue
            self.info(f"{version} find a new build {build}")
            status = await self.submit(
                url=f"{api_url}/{version}/{build}/download",
                version=version,
                build=build,
                release=True,
                update_time=job["timestamp"] // 1000,
                checksum=job["md5"],
                mode="md5"
            )
            if status:
                self.write(version, build)
            self.info(f"{version} is up-to-date.")
