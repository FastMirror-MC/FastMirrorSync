"""
@File      : src/papermc.py
@Author    : Skeleton_321
@CreateDate: 2022/2/6 3:34
by IntelliJ IDEA
"""
import logging

from lib.client import sync_client


def execute(client_name, project, unittest=False):
    with sync_client(client_name, level=logging.INFO) as client:
        base_url = f"https://papermc.io/api/v2/projects/{project}"
        for version in client.get(base_url).json()["versions"]:
            builds: list = client.get(f"{base_url}/versions/{version}").json()["builds"]
            builds.sort()
            for build in builds:
                if client.need_skip(version, build, 0):
                    continue

                client.info(f"{version} find a newer build: {build}")
                url = f"https://papermc.io/api/v2/projects/{project}/versions/{version}/builds/{build}"
                json = client.get(url).json()

                client.download_and_submit(url=f'{url}/downloads/{json["downloads"]["application"]["name"]}',
                                           version=version, build=build, release=json["channel"] == "default",
                                           update_time=json['time'],
                                           checksum=json["downloads"]["application"]["sha256"], mode="sha256",
                                           unittest=unittest)
                client.set(version, build)
            client.info(f"{version} is up-to-date")
