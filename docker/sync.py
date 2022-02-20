"""
@File      : docker/sync.py
@Author    : Skeleton_321
@CreateDate: 2022/2/16 20:40
by IntelliJ IDEA
"""
from subprocess import CalledProcessError
import subprocess
import datetime
import logging
import sys

from lib.client import sync_client
from lib.utils import proxy_invoke, get

import info


def get_file_path(refs: str, output_dir: str):
    j = proxy_invoke(logging, get, "get",
                     url=f"https://hub.spigotmc.org/stash/projects/SPIGOT/repos/builddata/raw/info.json?at={refs}"
                     ).json()
    return f"{output_dir}/spigot-{j['minecraftVersion']}.jar"


with sync_client(name="Spigot", client_name=info.name) as client:
    subprocess.run(
        f"rm -rf {client.resources.workspace}/*.jar", shell=True, check=True)
    for version in info.versions:
        json = client.get(f"https://hub.spigotmc.org/versions/{version}.json").json()
        remote_build = json["name"]
        if client.need_skip(version, remote_build, []):
            continue
        client.info(f"{version} find a newer build {remote_build}")
        try:
            subprocess.run(
                args=["java", "-jar", "/workspace/buildtools.jar", "--rev",
                      version, "--output-dir", client.resources.workspace],
                stdout=sys.stdout,
                stderr=sys.stdout,
                encoding="utf-8",
                check=True
            )
            with open(get_file_path(json["refs"]["BuildData"], client.resources.workspace), "rb") as fp:
                client.submit(
                    stream=fp,
                    version=version,
                    build=0,
                    core_version=f"build{remote_build}",
                    release=True,
                    update_time=datetime.datetime.now()
                )
            client.append(version, remote_build)
        except CalledProcessError as e:
            client.error("build failed. ")
        client.info(f"{version} is up-to-date. ")
