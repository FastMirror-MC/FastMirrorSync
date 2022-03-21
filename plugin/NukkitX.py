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

    def get_ci_url(self) -> str:
        return "https://ci.opencollab.dev/job/NukkitX/job/Nukkit/job/master"

    def get_version(self, json) -> str:
        return "general"

    def get_is_release(self, json) -> bool:
        return True

    def get_asset(self, json) -> dict:
        return json["artifacts"][0]
