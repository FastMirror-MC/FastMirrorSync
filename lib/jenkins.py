"""
@File      : src/lib/jenkins.py
@Author    : Skeleton_321
@CreateDate: 2022/2/6 1:52
by IntelliJ IDEA
"""
import logging

from .client import sync_client


def execute(name: str, api: str,
            get_artifact, get_version, need_skip, get_release,
            level: int = logging.INFO, unittest=False):
    with sync_client(name=name, level=level) as client:
        api = f"{api}/lastSuccessfulBuild/api/json"
        json = client.get(api).json()
        build = json["number"]
        version = get_version(json)
        release = get_release(json)

        while True:
            if len(json["artifacts"]) < 1:
                client.warning(f"this build(#{build}) has no artifact. skipped. ")
                break
            if json["result"] != "SUCCESS":
                break
            artifact = get_artifact(json)

            if need_skip(client, version, build):
                break
            client.info(f"find a newer build {build}")
            client.download_and_submit(url=f'{json["url"]}artifact/{artifact["relativePath"]}', version=version,
                                       build=build, release=release, update_time=json["timestamp"] // 1000,
                                       unittest=unittest)
            client.set(version, build)
            break
        client.info(f"{version} is up-to-date.")
