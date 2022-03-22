"""
@File      : plugin/Sponge.py
@Author    : Skeleton_321
@CreateDate: 2022/3/14 20:56
by IntelliJ IDEA
"""
import datetime
import re

from lib.http import aio_download
from lib.log import logger
from lib.plugin import Plugin
from lib.version import string_version


def get_core_version(ver: str, version: str):
    return ver[len(version) + 1:]


def get_build(ver: str):
    builds = re.findall(r'(?:RC|BETA-)(\d+)', ver)
    return 0 if not builds else builds[0]


@logger
@string_version("./config")
@aio_download
class SpongeApiPlugin(Plugin):
    @staticmethod
    def get_project_name() -> str:
        pass

    async def run(self):
        base_url = f"https://dl-api-new.spongepowered.org/api/v2/groups/org.spongepowered/artifacts/{self.get_project_name()}"
        for version in (await self.get(base_url))["tags"]["minecraft"]:
            url = f"{base_url}/versions"
            json = await self.get(f"{url}?tags=minecraft:{version}&offset=0&limit=10")
            for ver, artifact in json["artifacts"].items():
                if artifact["tagValues"]["minecraft"] != version:
                    continue
                core_version = get_core_version(ver, version)
                if not self.need_update(version, core_version):
                    continue

                self.info(f"{version} find a new version: {core_version}")

                json = await self.get(f"{url}/{ver}")
                asset = None
                for i in json["assets"]:
                    if i["classifier"] == "universal" or (i["classifier"] == "" and i["extension"] == "jar"):
                        asset = i
                        break

                if asset is None:
                    self.warning(f"{ver} hasn't available assets. skipped.")
                    continue

                status = await self.submit(
                    url=asset["downloadUrl"],
                    version=version,
                    build=get_build(ver),
                    core_version=core_version,
                    release=True,
                    update_time=datetime.datetime.now(),
                    checksum=asset["sha1"],
                    mode="sha1"
                )
                if status:
                    self.write(version, core_version)
            self.info(f"{version} is up-to-date")
