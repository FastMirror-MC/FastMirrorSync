"""
@File      : plugin/LightfallClient.py
@Author    : Skeleton_321
@CreateDate: 2022/2/23 16:53
by IntelliJ IDEA
"""
from lib.plugin import GithubApiPlugin


class LightfallClient(GithubApiPlugin):
    @staticmethod
    def name() -> str:
        return "lightfall-client"

    def get_build_number(self, json) -> int:
        tag = json["tag_name"]
        return int(tag[tag.find('-') + 1:])

    def get_version(self, json) -> str:
        tag = json["tag_name"]
        return tag[0:tag.find('-')]

    @staticmethod
    def get_asset(json) -> dict:
        return json["assets"][0]

    @staticmethod
    def get_api_url() -> str:
        return "https://api.github.com/repos/ArclightPowered/lightfall-client/releases"
