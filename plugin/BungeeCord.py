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

    @staticmethod
    def get_ci_url() -> str:
        return "https://ci.md-5.net/job/BungeeCord"

    def get_version(self, json) -> str:
        return "general"

    @staticmethod
    def get_asset(json) -> dict:
        return {i["displayPath"].lower(): i for i in json["artifacts"]}["bungeecord.jar"]

    @staticmethod
    def get_is_release(json) -> bool:
        return True
