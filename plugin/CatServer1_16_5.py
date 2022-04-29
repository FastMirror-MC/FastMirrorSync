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
class CatServer1_16_5(Plugin):
    @staticmethod
    def name() -> str:
        return "CatServer1_16_5"

    def client_name(self) -> str:
        return "CatServer"

    def get_ci_url(self) -> str:
        return "https://jenkins.rbqcloud.cn:30011/job/CatServer-1.16.5"

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
                # loliserver你们是真的一点人事不干啊
                url=f'{json["url"].replace("http://cdn.ci.loliidc.cn:30011", "https://jenkins.rbqcloud.cn:30011")}artifact/{asset["relativePath"]}',
                version=version,
                build=build,
                release=release,
                update_time=json["timestamp"] // 1000
            )
            if status:
                self.write(version, build)
            break
        self.info(f"{version} is up-to-date.")
