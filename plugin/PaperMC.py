"""
@File      : plugin/PaperMC.py
@Author    : Skeleton_321
@CreateDate: 2022/2/23 17:03
by IntelliJ IDEA
"""
from lib.http import aio_download
from lib.log import logger
from lib.plugin import Plugin
from lib.version import integer_version


@logger
@integer_version("./config")
@aio_download
class PaperMCApiPlugin(Plugin):
    @staticmethod
    def get_project_name() -> str:
        pass

    async def run(self) -> None:
        base_url = f"https://papermc.io/api/v2/projects/{self.get_project_name()}"
        for version in (await self.get(base_url))["versions"]:
            builds: list = (await self.get(f"{base_url}/versions/{version}"))["builds"]
            builds.sort()
            for build in builds[:20]:
                if not self.need_update(version, build):
                    continue

                self.info(f"{version} find a new build: {build}")
                url = f"{base_url}/versions/{version}/builds/{build}"
                json = await self.get(url)
                application = json["downloads"]["application"]
                status = await self.submit(
                    url=f'{url}/downloads/{application["name"]}',
                    version=version,
                    build=build,
                    update_time=json["time"],
                    release=json["channel"] == "default",
                    checksum=application["sha256"],
                    mode="sha256"
                )
                if status:
                    self.write(version, build)
            self.info(f"{version} is up-to-date.")

