"""
@File      : plugin/Pufferfish.py
@Author    : Skeleton_321
@CreateDate: 2022/3/22 15:51
by PyCharm
"""
from lib.plugin import JenkinsApiPlugin


class Pufferfish(JenkinsApiPlugin):
    def get_ci_url(self) -> str:
        return "https://ci.pufferfish.host/job/Pufferfish-1.18/"

    def get_version(self, json) -> str:
        return "1.18"

    def get_asset(self, json) -> dict:
        return json["artifacts"][0]

    def get_is_release(self, json) -> bool:
        return True
