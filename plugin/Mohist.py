"""
@File      : plugin/Mohist.py
@Author    : Skeleton_321
@CreateDate: 2022/3/21 22:05
by PyCharm
"""
from lib.plugin import JenkinsApiPlugin

versions = [
    "1.18.2",
    "1.16.5",
    "1.12.2",
    "1.7.10"
]


class Mohist(JenkinsApiPlugin):
    # __download_enable__ = False
    # __submit_enable__ = False

    def __init__(self):
        super().__init__()
        self.__current_version__ = versions[0]

    @staticmethod
    def name() -> str:
        return "Mohist"

    def get_version(self, json) -> str:
        return self.__current_version__

    def get_ci_url(self) -> str:
        return f"https://ci.codemc.io/job/MohistMC/job/Mohist-{self.__current_version__}"

    def get_asset(self, json) -> dict:
        return json["artifacts"][0]

    def get_is_release(self, json) -> bool:
        return True

    async def run(self) -> None:
        for version in versions:
            self.__current_version__ = version
            await super().run()
        pass
