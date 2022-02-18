"""
@File      : src/lightfallclient.py
@Author    : Skeleton_321
@CreateDate: 2022/2/18 23:13
by IntelliJ IDEA
"""
from lib import github


def get_build(tag: str):
    return tag[tag.find('-') + 1:]


def get_version(tag: str):
    return tag[0:tag.find('-')]


def get_core_version(tag: str):
    return f"build{get_build(tag)}"


github.execute(
    name="lightfall-client",
    api="https://api.github.com/repos/ArclightPowered/lightfall-client/releases",
    get_build=lambda o: get_build(o["tag_name"]),
    get_version=lambda o: get_version(o["tag_name"]),
    get_core_version=lambda o: get_core_version(o["tag_name"]),
    get_asset=lambda o: o["assets"][0]
)
