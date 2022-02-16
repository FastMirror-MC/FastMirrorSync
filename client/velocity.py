"""
@File      : src/velocity.py
@Author    : Skeleton_321
@CreateDate: 2022/2/6 4:19
by IntelliJ IDEA
"""
import logging

from lib.client import sync_client


with sync_client("Velocity", level=logging.INFO) as client:
    base_url = f"https://papermc.io/api/v2/projects/velocity"
    for version in client.get(base_url).json()["versions"]:
        builds: list = client.get(f"{base_url}/versions/{version}").json()["builds"]
        builds.sort()
        for build in builds:
            core_version = f"{version}_build{build}"
            if client.need_skip(version, core_version, []):
                continue
            
            client.info(f"{version} find a newer build: {build}")
            url = f"https://papermc.io/api/v2/projects/velocity/versions/{version}/builds/{build}"
            json = client.get(url).json()

            filename = json["downloads"]["application"]["name"]

            client.download_and_submit(url=f"{url}/downloads/{filename}", version="general", build=build,
                                       release=json["channel"] == "default", update_time=json['time'],
                                       checksum=json["downloads"]["application"]["sha256"], mode="sha256",
                                       core_version=core_version)
            client.append(version, core_version)
        client.info(f"{version} is up-to-date")
