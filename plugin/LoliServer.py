"""
@File      : plugin/LoliServer.py
@Author    : Skeleton_321
@CreateDate: 2022/3/21 22:58
by PyCharm
"""
from lib.plugin import JenkinsApiPlugin


class LoliServer(JenkinsApiPlugin):
    @staticmethod
    def name() -> str:
        return "LoliServer"

    def get_ci_url(self) -> str:
        return "http://nat.loliidc.cn:33644/job/LoliServer1.16"

    def get_version(self, json) -> str:
        return "1.16.5"

    def get_is_release(self, json) -> bool:
        return True

    def get_asset(self, json) -> dict:
        for asset in json["artifacts"]:
            if "server" in asset["fileName"]:
                return asset
