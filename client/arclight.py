"""
@File      : src/arclight.py
@Author    : Skeleton_321
@CreateDate: 2022/2/5 23:39
by IntelliJ IDEA
"""
import logging

from lib import github


def get_version(tag: str):
    return tag[0:tag.find('/')]


def get_core_version(tag: str):
    return tag[tag.find('/') + 1:]


def get_build(tag: str):
    return int(tag[tag.rfind('.') + 1:])


github.execute(name="Arclight", api="https://api.github.com/repos/IzzelAliz/Arclight/releases",
               get_version=lambda o: get_version(o["tag_name"]),
               get_core_version=lambda o: get_core_version(o["tag_name"]), get_build=lambda o: get_build(o["tag_name"]),
               get_asset=lambda o: o["assets"][0], level=logging.DEBUG)
