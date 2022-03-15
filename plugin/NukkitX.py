"""
@File      : plugin/NukkitX.py
@Author    : Skeleton_321
@CreateDate: 2022/2/23 17:00
by IntelliJ IDEA
"""
from lib.plugin import JenkinsApiPlugin


class NukkitX(JenkinsApiPlugin):
    @staticmethod
    def name() -> str:
        return "NukkitX"

    @staticmethod
    def get_ci_url() -> str:
        return "https://ci.opencollab.dev/job/NukkitX/job/Nukkit/job/master"

    def get_version(self, json) -> str:
        return "general"

    @staticmethod
    def get_is_release(json) -> bool:
        return True

    @staticmethod
    def get_asset(json) -> dict:
        return json["artifacts"][0]
