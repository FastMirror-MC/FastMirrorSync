"""
@File      : src/sponge.py
@Author    : Skeleton_321
@CreateDate: 2022/2/6 4:09
by IntelliJ IDEA
"""
import datetime
import logging
import re

from lib.client import sync_client


__all__ = ["execute"]


def get_core_version(ver: str, version: str):
    return ver[len(version) + 1:]


def get_build(ver: str):
    return 0 if (builds := re.findall(r'(?:RC|BETA-)(\d+)', ver)) is None else builds[0]


def execute(name, project):
    with sync_client(name, level=logging.INFO) as client:
        base_url = f"https://dl-api-new.spongepowered.org/api/v2/groups/org.spongepowered/artifacts/{project}"
        for version in client.get(base_url).json()["tags"]["minecraft"]:
            url = f"{base_url}/versions"

            json = client.get(f"{url}?tags=minecraft:{version}&offset=0&limit=10").json()
            for ver, artifact in json["artifacts"].items():
                if artifact["tagValues"]["minecraft"] != version:
                    continue

                core_version = get_core_version(ver, version)
                if client.need_skip(version, core_version, []):
                    continue

                client.info(f"{version} find a newer version: {core_version}")

                json = client.get(f"{url}/{ver}").json()

                asset = None
                for i in json["assets"]:
                    if i["classifier"] == "universal" or (i["classifier"] == "" and i["extension"] == "jar"):
                        asset = i
                        break
                if asset is None:
                    client.warning(f"{ver} hasn't available assets. skipped.")
                    continue

                client.download_and_submit(url=asset["downloadUrl"], version=version, build=get_build(ver),
                                           release=True,
                                           update_time=datetime.datetime.now(), checksum=asset["sha1"], mode="sha1",
                                           core_version=core_version)
                client.append(version, core_version)
                break
            client.info(f"{version} up-tp-date.")
