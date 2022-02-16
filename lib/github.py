"""
@File      : src/lib/github.py
@Author    : Skeleton_321
@CreateDate: 2022/2/5 23:50
by IntelliJ IDEA
"""
import logging

from .client import sync_client


def execute(name: str, api: str,
            get_version, get_core_version, get_build, get_asset,
            level: int = logging.INFO, unittest=False):
    with sync_client(name, level=level) as client:
        for publish in client.get(api).json():
            version = get_version(publish)
            code_version = get_core_version(publish)
            build = get_build(publish)
            asset = get_asset(publish)
            release = not publish["prerelease"]
            update_time = publish["published_at"]

            if client.need_skip(version, code_version, []):
                continue

            client.info(f"{version} find a newer version: {code_version}")

            if asset is None:
                client.error(f"but cannot find available asset. skipped.")
                continue

            client.download_and_submit(url=asset["browser_download_url"], version=version, build=build, release=release,
                                       update_time=update_time, core_version=code_version, unittest=unittest)
            client.append(version, code_version)
            client.info(f"{version}-{code_version} is up-to-date.")
