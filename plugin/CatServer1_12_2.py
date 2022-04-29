
from lib.plugin import GithubApiPlugin


class CatServer1_12_2(GithubApiPlugin):

    @staticmethod
    def name() -> str:
        return "CatServer1_12_2"

    def client_name(self) -> str:
        return "CatServer"

    def get_version(self, json) -> str:
        return "1.12.2"

    def get_core_version(self, json) -> str:
        return json["tag_name"]

    def get_build_number(self, json) -> int:
        ver = self.get_core_version(json)
        return ver[ver.rfind('.') + 1:]

    @staticmethod
    def get_asset(json) -> dict:
        return json["assets"][0]

    @staticmethod
    def get_api_url() -> str:
        return "https://api.github.com/repos/Luohuayu/CatServer/releases"
