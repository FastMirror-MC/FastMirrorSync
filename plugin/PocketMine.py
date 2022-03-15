"""
@File      : plugin/PocketMine.py
@Author    : Skeleton_321
@CreateDate: 2022/2/23 17:24
by IntelliJ IDEA
"""
from lib.plugin import GithubApiPlugin


class PocketMine(GithubApiPlugin):
    @staticmethod
    def name() -> str:
        return "PocketMine"

    @staticmethod
    def get_api_url() -> str:
        return "https://api.github.com/repos/pmmp/PocketMine-MP/releases"

    def get_version(self, json) -> str:
        return "general"

    def get_core_version(self, json) -> str:
        return json["tag_name"]

    def get_build_number(self, json) -> int:
        return 0

    @staticmethod
    def get_asset(json) -> dict:
        tmp = list(filter(lambda o: "phar" in o["name"], json["assets"]))
        return None if len(tmp) < 1 else tmp[0]
