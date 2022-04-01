"""
@File      : plugin/LoliServer.py
@Author    : Skeleton_321
@CreateDate: 2022/3/21 22:58
by PyCharm
"""
from lib.log import logger
from lib.plugin import Plugin
from lib.http import aio_download
from lib.version import integer_version


@logger
@aio_download
@integer_version("./config")
class LoliServer(Plugin):
    @staticmethod
    def name() -> str:
        return "LoliServer"

    def get_ci_url(self) -> str:
        return "https://cdn.ci.loliidc.cn:30011/job/LoliServer-1.16.5"

    def get_version(self, json) -> str:
        return "1.16.5"

    def get_is_release(self, json) -> bool:
        return True

    def get_asset(self, json) -> dict:
        for asset in json["artifacts"]:
            if "server" in asset["fileName"]:
                return asset

    async def run(self) -> None:
        json = await self.get(f"{self.get_ci_url()}/lastSuccessfulBuild/api/json")
        build = json["number"]
        version = self.get_version(json)
        release = self.get_is_release(json)

        while True:
            if len(json["artifacts"]) < 1:
                self.warning(
                    f"this build(#{build}) has no artifact. skipped. ")
                break
            if json["result"] != "SUCCESS":
                break
            if not self.need_update(version, build):
                break

            asset = self.get_asset(json)
            self.info(f"{version} find a new build {build}")
            status = await self.submit(
                # loliserver这次的ci可能是nginx那边没转发Protocol，返回的API里面URL用的http
                url=f'{json["url"].replace("http://", "https://")}artifact/{asset["relativePath"]}',
                version=version,
                build=build,
                release=release,
                update_time=json["timestamp"] // 1000
            )
            if status:
                self.write(version, build)
            break
        self.info(f"{version} is up-to-date.")
