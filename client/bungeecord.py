"""
@File      : src/bungeecord.py
@Author    : Skeleton_321
@CreateDate: 2022/2/6 3:50
by IntelliJ IDEA
"""
from lib import jenkins

jenkins.execute(name="BungeeCord", api="https://ci.md-5.net/job/BungeeCord",
                get_artifact=lambda json: {i["displayPath"].lower(): i for i in json["artifacts"]}["bungeecord.jar"],
                get_version=lambda json: "general",
                need_skip=lambda client, version, build: client.need_skip(version, build, 0),
                get_release=lambda json: True)
