"""
@File      : src/nukkitx.py
@Author    : Skeleton_321
@CreateDate: 2022/2/6 2:03
by IntelliJ IDEA
"""
from lib import jenkins

jenkins.execute(name="NukkitXForBedrock", api="https://ci.opencollab.dev/job/NukkitX/job/Nukkit/job/master",
                get_artifact=lambda json: json["artifacts"][0], get_version=lambda json: "general",
                need_skip=lambda client, version, build: client.need_skip(version, build, 0),
                get_release=lambda json: True)
