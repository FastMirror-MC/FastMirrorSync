"""
@File      : src/purpur.py
@Author    : Skeleton_321
@CreateDate: 2022/2/6 4:01
by IntelliJ IDEA
"""
from lib.client import sync_client


with sync_client("Purpur") as client:
    api_url = "https://api.purpurmc.org/v2/purpur"
    for version in client.get(api_url).json()["versions"]:
        json = client.get(f"{api_url}/{version}").json()["builds"]

        build = int(json["latest"])
        if client.need_skip(version, build, 0):
            continue
        job = client.get(f"{api_url}/{version}/{build}").json()
        if job["result"] != "SUCCESS":
            continue
        client.info(f"{version} find a newer build: #{build}")
        client.download_and_submit(url=f"{api_url}/{version}/{build}/download", version=version, build=build,
                                   release=True, update_time=job["timestamp"] // 1000, checksum=job["md5"], mode="md5")
        client.set(version, build)
        client.info(f"{version} is up-to-date")
