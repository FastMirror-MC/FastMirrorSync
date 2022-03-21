"""
@File      : plugin/Arclight.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 8:29
by IntelliJ IDEA
"""
import re

from lib.http import aio_download
from lib.log import logger
from lib.plugin import Plugin
from lib.version import integer_version

# 1.17、1.16、1.14被标记为LEGACY，故不同步。
ver_map = {
    "1.18": "arclight-18",
    # "1.17": "arclight-17",
    "1.16": "arclight-16",
    # "1.15": "arclight-15",
    # "1.14": "arclight"
}


@logger
@integer_version("./config")
@aio_download
class Arclight(Plugin):
    # __download_enable__ = False
    # __submit_enable__ = False
    @staticmethod
    def name() -> str:
        return "Arclight"

    async def run(self) -> None:
        for version, slug in ver_map.items():
            self.info(f"check {version}...")
            api = f"https://ci.appveyor.com/api/projects/IzzelAliz/{slug}"
            url = f"{api}/history?recordsNumber=20"
            for json in (await self.get(url))["builds"]:
                if json["status"] != "success":
                    continue
                build = json["buildNumber"]
                if not self.need_update(version, build):
                    continue
                self.info(f"{version} has a new build {build}.")
                job_id = (await self.get(f"{api}/build/{json['version']}"))["build"]["jobs"][0]["jobId"]
                artifacts_url = f"https://ci.appveyor.com/api/buildjobs/{job_id}/artifacts"
                iteration = filter(
                    lambda i: re.match(r'.*?arclight-forge-(?:\d+\.\d+\.\d+-?)+(?:-SNAPSHOT)?\.jar', i) is not None,
                    [v["fileName"] for v in await self.get(artifacts_url)]
                )
                artifact = next(iteration)
                await self.submit(
                    url=f"{artifacts_url}/{artifact}",
                    version=version,
                    build=build,
                    release=True,
                    update_time=json["updated"].replace("+00:00", "Z")
                )
                self.write(version, build)
            self.info(f"{version} is up-to-date.")
