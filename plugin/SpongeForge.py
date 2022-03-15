"""
@File      : plugin/SpongeForge.py
@Author    : Skeleton_321
@CreateDate: 2022/3/14 21:08
by IntelliJ IDEA
"""
from .Sponge import SpongeApiPlugin


class SpongeForge(SpongeApiPlugin):
    @staticmethod
    def name() -> str:
        return "SpongeForge"

    @staticmethod
    def get_project_name():
        return "spongeforge"
