"""
@File      : plugin/BungeeCord.py
@Author    : Skeleton_321
@CreateDate: 2022/2/22 8:32
by IntelliJ IDEA
"""
from lib.plugin import JenkinsApiPlugin


class BungeeCord(JenkinsApiPlugin):
    @staticmethod
    def name() -> str:
        return "BungeeCord"

    def get_ci_url(self) -> str:
        return "https://ci.md-5.net/job/BungeeCord"

    def get_version(self, json) -> str:
        return "general"

    def get_asset(self, json) -> dict:
        return {i["displayPath"].lower(): i for i in json["artifacts"]}["bungeecord.jar"]

    def get_is_release(self, json) -> bool:
        return True
