"""
@File      : src/pocketmine.py
@Author    : Skeleton_321
@CreateDate: 2022/2/6 3:58
by IntelliJ IDEA
"""
import logging
from lib import github


def get_asset(json):
    for i in json["assets"]:
        if "phar" in i["name"]:
            return i
    return None


github.execute(name="PocketMine", api="https://api.github.com/repos/pmmp/PocketMine-MP/releases",
               get_version=lambda json: "general", get_core_version=lambda json: json["tag_name"],
               get_build=lambda json: 0, get_asset=get_asset, level=logging.DEBUG)
